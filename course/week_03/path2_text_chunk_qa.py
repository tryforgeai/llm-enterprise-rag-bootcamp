#!/usr/bin/env python3
"""Path #2: PDF -> text -> chunk -> embedding -> QA.

This is the text pipeline from the Week 03 representation tournament:

    PDF -> parser/textbook Markdown -> chunks -> text embeddings -> top-k chunks
    -> OpenAI text model answer

The script can read an already converted textbook Markdown file, or try to
extract text directly from the PDF with pypdf/Docling if those packages are
installed in the current environment.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from openai import OpenAI


SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parents[1]
DEFAULT_PDF = SCRIPT_DIR / "PRML.pdf"
DEFAULT_TEXTBOOK = SCRIPT_DIR / "textbook" / "PRML.textbook.md"
FALLBACK_TEXTBOOK = SCRIPT_DIR / "textbook_test" / "PRML.textbook.md"
DEFAULT_OUT = SCRIPT_DIR / "runs" / "path2_text_chunk_answer.json"


@dataclass(frozen=True)
class Chunk:
    chunk_id: int
    text: str
    source: str
    start_word: int
    end_word: int


@dataclass(frozen=True)
class RetrievedChunk:
    rank: int
    score: float
    chunk_id: int
    source: str
    text: str


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


def clean_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_with_pypdf(pdf_path: Path, max_pages: int | None = None) -> str:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError(
            "pypdf is not installed. Either install pypdf, install Docling, "
            "or run pdf_to_textbook.py first and pass --textbook."
        ) from exc

    reader = PdfReader(str(pdf_path))
    pages = reader.pages[:max_pages] if max_pages else reader.pages
    sections = []
    for page_index, page in enumerate(pages, start=1):
        sections.append(f"## Page {page_index}\n\n{page.extract_text() or ''}")
    return clean_text("\n\n".join(sections))


def extract_pdf_with_docling(pdf_path: Path) -> str:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise RuntimeError(
            "Docling is not installed. Install docling or use --engine pypdf."
        ) from exc

    result = DocumentConverter().convert(str(pdf_path))
    return clean_text(result.document.export_to_markdown())


def load_source_text(
    pdf_path: Path,
    textbook_path: Path | None,
    engine: str,
    max_pages: int | None,
) -> tuple[str, str]:
    if textbook_path and textbook_path.exists():
        return textbook_path.read_text(encoding="utf-8"), str(textbook_path)

    if DEFAULT_TEXTBOOK.exists():
        return DEFAULT_TEXTBOOK.read_text(encoding="utf-8"), str(DEFAULT_TEXTBOOK)
    if FALLBACK_TEXTBOOK.exists():
        return FALLBACK_TEXTBOOK.read_text(encoding="utf-8"), str(FALLBACK_TEXTBOOK)

    if engine == "docling":
        return extract_pdf_with_docling(pdf_path), f"{pdf_path} via docling"
    if engine == "pypdf":
        return extract_pdf_with_pypdf(pdf_path, max_pages=max_pages), f"{pdf_path} via pypdf"

    errors = []
    try:
        return extract_pdf_with_docling(pdf_path), f"{pdf_path} via docling"
    except Exception as exc:
        errors.append(f"Docling failed: {exc}")
    try:
        return extract_pdf_with_pypdf(pdf_path, max_pages=max_pages), f"{pdf_path} via pypdf"
    except Exception as exc:
        errors.append(f"pypdf failed: {exc}")
    raise RuntimeError("\n".join(errors))


def chunk_words(text: str, source: str, chunk_words: int, overlap_words: int) -> list[Chunk]:
    words = re.findall(r"\S+", text)
    chunks: list[Chunk] = []
    start = 0
    chunk_id = 0
    step = max(chunk_words - overlap_words, 1)
    while start < len(words):
        end = min(start + chunk_words, len(words))
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                text=" ".join(words[start:end]),
                source=source,
                start_word=start,
                end_word=end,
            )
        )
        if end == len(words):
            break
        start += step
        chunk_id += 1
    return chunks


def embed_texts(client: OpenAI, texts: list[str], model: str, batch_size: int) -> np.ndarray:
    vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        response = client.embeddings.create(model=model, input=batch)
        vectors.extend(item.embedding for item in response.data)
    return np.asarray(vectors, dtype=np.float32)


def normalize_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return matrix / norms


def retrieve_chunks(
    client: OpenAI,
    question: str,
    chunks: list[Chunk],
    embedding_model: str,
    top_k: int,
    batch_size: int,
) -> list[RetrievedChunk]:
    chunk_vectors = embed_texts(
        client,
        [chunk.text for chunk in chunks],
        model=embedding_model,
        batch_size=batch_size,
    )
    question_vector = embed_texts(
        client,
        [question],
        model=embedding_model,
        batch_size=1,
    )[0]

    unit_chunks = normalize_rows(chunk_vectors)
    unit_question = question_vector / max(np.linalg.norm(question_vector), 1e-12)
    scores = unit_chunks @ unit_question
    top_indices = np.argsort(scores)[::-1][:top_k]

    return [
        RetrievedChunk(
            rank=rank,
            score=float(scores[index]),
            chunk_id=chunks[index].chunk_id,
            source=chunks[index].source,
            text=chunks[index].text,
        )
        for rank, index in enumerate(top_indices, start=1)
    ]


def answer_from_chunks(
    client: OpenAI,
    question: str,
    retrieved: list[RetrievedChunk],
    answer_model: str,
) -> str:
    context = "\n\n".join(
        f"[chunk {item.chunk_id}, score={item.score:.4f}]\n{item.text}"
        for item in retrieved
    )
    prompt = (
        "Answer the question using only the retrieved textbook chunks. "
        "If the chunks do not contain enough evidence, say what is missing. "
        "Cite chunk ids in brackets.\n\n"
        f"Question: {question}\n\n"
        f"Retrieved chunks:\n{context}"
    )
    response = client.responses.create(
        model=answer_model,
        input=[{"role": "user", "content": [{"type": "input_text", "text": prompt}]}],
    )
    return response.output_text


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", help="Question to ask against the PDF textbook.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF)
    parser.add_argument("--textbook", type=Path, default=None)
    parser.add_argument("--engine", choices=["auto", "docling", "pypdf"], default="auto")
    parser.add_argument("--max-pages", type=int, default=None)
    parser.add_argument("--chunk-words", type=int, default=350)
    parser.add_argument("--overlap-words", type=int, default=60)
    parser.add_argument("--top-k", type=int, default=5)
    parser.add_argument("--embedding-model", default="text-embedding-3-small")
    parser.add_argument("--answer-model", default="gpt-4.1-mini")
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2

    client = openai_client()
    source_text, source_name = load_source_text(
        pdf_path=pdf_path,
        textbook_path=args.textbook.expanduser().resolve() if args.textbook else None,
        engine=args.engine,
        max_pages=args.max_pages,
    )
    chunks = chunk_words(source_text, source_name, args.chunk_words, args.overlap_words)
    if not chunks:
        print("No chunks produced.", file=sys.stderr)
        return 1

    retrieved = retrieve_chunks(
        client=client,
        question=args.question,
        chunks=chunks,
        embedding_model=args.embedding_model,
        top_k=args.top_k,
        batch_size=args.batch_size,
    )
    answer = answer_from_chunks(client, args.question, retrieved, args.answer_model)

    payload = {
        "path": "path2_text_chunk",
        "question": args.question,
        "source": source_name,
        "embedding_model": args.embedding_model,
        "answer_model": args.answer_model,
        "chunk_words": args.chunk_words,
        "overlap_words": args.overlap_words,
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
