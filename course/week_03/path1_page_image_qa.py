#!/usr/bin/env python3
"""Path #1: PDF page images -> image retrieval -> vision QA.

This is the visual pipeline from the Week 03 representation tournament:

    PDF -> page PNGs -> image/text embedding retrieval -> top-k page images
    -> OpenAI vision model answer

For retrieval, this script uses a CLIP-like SentenceTransformer model so the
question text and page images live in the same embedding space. For answering,
it sends the retrieved page images plus the question to an OpenAI vision-capable
model. If you use an OpenAI-compatible Qwen endpoint, set OPENAI_BASE_URL in
.env and pass the Qwen vision model name with --vision-model.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from openai import OpenAI
from PIL import Image


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_PDF = SCRIPT_DIR / "PRML.pdf"
DEFAULT_PAGES_DIR = SCRIPT_DIR / "data" / "pages"
DEFAULT_OUT = SCRIPT_DIR / "runs" / "path1_page_image_answer.json"
DEFAULT_MODEL_ID = "TomoroAI/tomoro-colqwen3-embed-4b"
DEFAULT_BASELINE_MODEL_ID = "clip-ViT-B-32"


@dataclass(frozen=True)
class RetrievedPage:
    rank: int
    score: float
    page: int
    image_path: str


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def openai_client() -> OpenAI:
    load_env_file(PROJECT_ROOT / ".env")
    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError(f"OPENAI_API_KEY not found. Expected it in {PROJECT_ROOT / '.env'}")
    return OpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
        base_url=os.environ.get("OPENAI_BASE_URL") or None,
    )


def existing_page_images(pages_dir: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in pages_dir.glob("page_*.png")
            if path.is_file() and path.stat().st_size > 0
        ]
    )


def page_number_from_path(path: Path, fallback: int) -> int:
    match = re.search(r"page_(\d+)", path.stem)
    if not match:
        return fallback
    return int(match.group(1))


def render_with_pymupdf(pdf_path: Path, pages_dir: Path, dpi: int, max_pages: int | None) -> None:
    try:
        import fitz
    except ImportError as exc:
        raise RuntimeError("PyMuPDF is not installed.") from exc

    doc = fitz.open(str(pdf_path))
    zoom = dpi / 72.0
    matrix = fitz.Matrix(zoom, zoom)
    limit = min(len(doc), max_pages) if max_pages else len(doc)
    pages_dir.mkdir(parents=True, exist_ok=True)
    for page_index in range(limit):
        pix = doc[page_index].get_pixmap(matrix=matrix, alpha=False)
        pix.save(str(pages_dir / f"page_{page_index + 1:04d}.png"))


def render_with_pdf2image(pdf_path: Path, pages_dir: Path, dpi: int, max_pages: int | None) -> None:
    try:
        from pdf2image import convert_from_path
    except ImportError as exc:
        raise RuntimeError("pdf2image is not installed.") from exc

    pages_dir.mkdir(parents=True, exist_ok=True)
    images = convert_from_path(
        str(pdf_path),
        dpi=dpi,
        first_page=1,
        last_page=max_pages,
    )
    for page_index, image in enumerate(images, start=1):
        image.save(pages_dir / f"page_{page_index:04d}.png")


def render_with_qlmanage(pdf_path: Path, pages_dir: Path) -> None:
    """Mac fallback: qlmanage usually creates a first-page thumbnail only."""
    pages_dir.mkdir(parents=True, exist_ok=True)
    command = ["qlmanage", "-t", "-s", "1200", "-o", str(pages_dir), str(pdf_path)]
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    candidates = sorted(pages_dir.glob("*.png"))
    if not candidates:
        raise RuntimeError("qlmanage did not produce a PNG thumbnail.")
    candidates[0].rename(pages_dir / "page_0001.png")


def ensure_page_images(
    pdf_path: Path,
    pages_dir: Path,
    render_engine: str,
    dpi: int,
    max_pages: int | None,
) -> list[Path]:
    pages = existing_page_images(pages_dir)
    if pages:
        return pages[:max_pages] if max_pages else pages

    errors = []
    engines = [render_engine] if render_engine != "auto" else ["pymupdf", "pdf2image", "qlmanage"]
    for engine in engines:
        try:
            if engine == "pymupdf":
                render_with_pymupdf(pdf_path, pages_dir, dpi, max_pages)
            elif engine == "pdf2image":
                render_with_pdf2image(pdf_path, pages_dir, dpi, max_pages)
            elif engine == "qlmanage":
                render_with_qlmanage(pdf_path, pages_dir)
            else:
                raise ValueError(f"Unknown render engine: {engine}")
            pages = existing_page_images(pages_dir)
            if pages:
                return pages[:max_pages] if max_pages else pages
        except Exception as exc:
            errors.append(f"{engine}: {exc}")

    raise RuntimeError(
        "Could not render PDF pages.\n"
        + "\n".join(errors)
        + "\n\nInstall PyMuPDF (`pip install pymupdf`) or pdf2image+poppler, "
        "or provide pre-rendered PNGs in --pages-dir."
    )


def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def load_clip_model(model_name: str):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "sentence-transformers is required for page-image retrieval. "
            "Install it or run from the course virtualenv."
        ) from exc
    return SentenceTransformer(model_name)


def retrieve_pages_with_sentence_transformers(
    question: str,
    image_paths: list[Path],
    retrieval_model: str,
    top_k: int,
    batch_size: int,
) -> list[RetrievedPage]:
    model = load_clip_model(retrieval_model)
    images = [Image.open(path).convert("RGB") for path in image_paths]
    image_vectors = np.asarray(
        model.encode(images, batch_size=batch_size, show_progress_bar=True),
        dtype=np.float32,
    )
    question_vector = np.asarray(
        model.encode([question], show_progress_bar=False),
        dtype=np.float32,
    )[0]

    unit_images = normalize_rows(image_vectors)
    unit_question = question_vector / max(np.linalg.norm(question_vector), 1e-12)
    scores = unit_images @ unit_question
    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        RetrievedPage(
            rank=rank,
            score=float(scores[index]),
            page=page_number_from_path(image_paths[int(index)], fallback=int(index) + 1),
            image_path=str(image_paths[index]),
        )
        for rank, index in enumerate(top_indices, start=1)
    ]


def select_device(requested: str) -> str:
    if requested != "auto":
        return requested
    try:
        import torch
    except ImportError:
        return "cpu"
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def tensor_to_device(batch, device: str):
    if hasattr(batch, "to"):
        return batch.to(device)
    if isinstance(batch, dict):
        return {
            key: value.to(device) if hasattr(value, "to") else value
            for key, value in batch.items()
        }
    return batch


def model_output_to_tensor(output):
    if hasattr(output, "last_hidden_state"):
        return output.last_hidden_state
    if isinstance(output, (tuple, list)):
        return output[0]
    return output


def late_interaction_scores(query_vectors, image_vectors) -> np.ndarray:
    """MaxSim late-interaction scores for one query against many image pages."""
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("torch is required for ColQwen3 late interaction.") from exc

    if not torch.is_tensor(query_vectors):
        query_vectors = torch.as_tensor(query_vectors)
    if not torch.is_tensor(image_vectors):
        image_vectors = torch.as_tensor(image_vectors)

    if query_vectors.ndim == 2:
        query_vectors = query_vectors.unsqueeze(0)
    if image_vectors.ndim == 2:
        image_vectors = image_vectors.unsqueeze(0)

    query = torch.nn.functional.normalize(query_vectors[0].float(), dim=-1)
    pages = torch.nn.functional.normalize(image_vectors.float(), dim=-1)
    scores = torch.einsum("qd,npd->nqp", query, pages).max(dim=-1).values.sum(dim=-1)
    return scores.detach().cpu().numpy()


def load_colqwen3_model(model_name: str, device: str):
    try:
        import torch
        from transformers import AutoModel, AutoProcessor
    except ImportError as exc:
        raise RuntimeError(
            "ColQwen3 retrieval requires torch and transformers. "
            "Run from the course virtualenv or install those packages."
        ) from exc

    dtype = torch.float16 if device in {"cuda", "mps"} else torch.float32
    processor = AutoProcessor.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(
        model_name,
        torch_dtype=dtype,
        trust_remote_code=True,
    ).to(device)
    model.eval()
    return model, processor


def process_colqwen3_images(processor, images: list[Image.Image]):
    if hasattr(processor, "process_images"):
        return processor.process_images(images)
    return processor(images=images, return_tensors="pt", padding=True)


def process_colqwen3_queries(processor, queries: list[str]):
    if hasattr(processor, "process_queries"):
        return processor.process_queries(queries)
    return processor(text=queries, return_tensors="pt", padding=True)


def retrieve_pages_with_colqwen3(
    question: str,
    image_paths: list[Path],
    retrieval_model: str,
    top_k: int,
    batch_size: int,
    device: str,
) -> list[RetrievedPage]:
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("torch is required for ColQwen3 retrieval.") from exc

    resolved_device = select_device(device)
    model, processor = load_colqwen3_model(retrieval_model, resolved_device)

    query_batch = tensor_to_device(
        process_colqwen3_queries(processor, [question]),
        resolved_device,
    )
    with torch.no_grad():
        query_vectors = model_output_to_tensor(model(**query_batch))

    image_vectors_batches = []
    for start in range(0, len(image_paths), batch_size):
        batch_paths = image_paths[start : start + batch_size]
        images = [Image.open(path).convert("RGB") for path in batch_paths]
        image_batch = tensor_to_device(
            process_colqwen3_images(processor, images),
            resolved_device,
        )
        with torch.no_grad():
            image_vectors_batches.append(model_output_to_tensor(model(**image_batch)).detach().cpu())

    image_vectors = torch.cat(image_vectors_batches, dim=0)
    scores = late_interaction_scores(query_vectors.detach().cpu(), image_vectors)
    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        RetrievedPage(
            rank=rank,
            score=float(scores[int(index)]),
            page=page_number_from_path(image_paths[int(index)], fallback=int(index) + 1),
            image_path=str(image_paths[int(index)]),
        )
        for rank, index in enumerate(top_indices, start=1)
    ]


def retrieve_pages(
    question: str,
    image_paths: list[Path],
    retrieval_model: str,
    top_k: int,
    batch_size: int,
    retrieval_backend: str = "colqwen3",
    device: str = "auto",
) -> list[RetrievedPage]:
    if retrieval_backend == "sentence-transformers":
        return retrieve_pages_with_sentence_transformers(
            question=question,
            image_paths=image_paths,
            retrieval_model=retrieval_model,
            top_k=top_k,
            batch_size=batch_size,
        )
    if retrieval_backend == "colqwen3":
        return retrieve_pages_with_colqwen3(
            question=question,
            image_paths=image_paths,
            retrieval_model=retrieval_model,
            top_k=top_k,
            batch_size=batch_size,
            device=device,
        )
    raise ValueError(f"Unknown retrieval backend: {retrieval_backend}")


def image_to_data_url(path: Path, max_side: int) -> str:
    image = Image.open(path).convert("RGB")
    image.thumbnail((max_side, max_side))
    tmp_path = path.with_suffix(".qa_resized.jpg")
    image.save(tmp_path, format="JPEG", quality=85)
    encoded = base64.b64encode(tmp_path.read_bytes()).decode("ascii")
    tmp_path.unlink(missing_ok=True)
    return f"data:image/jpeg;base64,{encoded}"


def answer_from_pages(
    client: OpenAI,
    question: str,
    retrieved: list[RetrievedPage],
    vision_model: str,
    max_image_side: int,
) -> str:
    content = [
        {
            "type": "input_text",
            "text": (
                "Answer the question using only the retrieved PDF page images. "
                "If the pages do not contain enough evidence, say what is missing. "
                "Cite page numbers from the provided labels.\n\n"
                f"Question: {question}"
            ),
        }
    ]
    for item in retrieved:
        content.append(
            {
                "type": "input_text",
                "text": f"Retrieved page {item.page}, score={item.score:.4f}",
            }
        )
        content.append(
            {
                "type": "input_image",
                "image_url": image_to_data_url(Path(item.image_path), max_image_side),
            }
        )

    response = client.responses.create(
        model=vision_model,
        input=[{"role": "user", "content": content}],
    )
    return response.output_text


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Question to ask against the PDF page images.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--pages-dir", type=Path, default=DEFAULT_PAGES_DIR)
    parser.add_argument(
        "--render-engine",
        choices=["auto", "pymupdf", "pdf2image", "qlmanage"],
        default="auto",
    )
    parser.add_argument("--dpi", type=int, default=144)
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--top-k", type=int, default=3)
    parser.add_argument(
        "--retrieval-backend",
        choices=["colqwen3", "sentence-transformers"],
        default="colqwen3",
    )
    parser.add_argument("--retrieval-model", default=DEFAULT_MODEL_ID)
    parser.add_argument("--device", default="auto")
    parser.add_argument("--vision-model", default="gpt-4.1-mini")
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--max-image-side", type=int, default=1600)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args(argv)


def main() -> int:
    args = parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    page_paths = ensure_page_images(
        pdf_path=pdf_path,
        pages_dir=args.pages_dir.expanduser().resolve(),
        render_engine=args.render_engine,
        dpi=args.dpi,
        max_pages=args.max_pages,
    )
    if not page_paths:
        print("No page images found or rendered.", file=sys.stderr)
        return 1

    retrieved = retrieve_pages(
        question=args.question,
        image_paths=page_paths,
        retrieval_model=args.retrieval_model,
        top_k=args.top_k,
        batch_size=args.batch_size,
        retrieval_backend=args.retrieval_backend,
        device=args.device,
    )
    client = openai_client()
    answer = answer_from_pages(
        client=client,
        question=args.question,
        retrieved=retrieved,
        vision_model=args.vision_model,
        max_image_side=args.max_image_side,
    )

    payload = {
        "path": "path1_page_image",
        "question": args.question,
        "pdf": str(pdf_path),
        "pages_dir": str(args.pages_dir.expanduser().resolve()),
        "retrieval_model": args.retrieval_model,
        "retrieval_backend": args.retrieval_backend,
        "device": args.device,
        "vision_model": args.vision_model,
        "top_k": args.top_k,
        "answer": answer,
        "retrieved": [asdict(item) for item in retrieved],
    }
    args.out.expanduser().resolve().parent.mkdir(parents=True, exist_ok=True)
    args.out.expanduser().resolve().write_text(
        json.dumps(payload, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(answer)
    print(f"\nSaved run JSON: {args.out.expanduser().resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
