"""
Team 1 — Visual pipeline.

Converts each PDF page to a PNG, then embeds the first 85 pages with CLIP and
SigLIP2 separately, storing two FAISS IndexFlatIP indices on disk.

Usage:
    python team1_visual.py --pdf data/PRML.pdf
    python team1_visual.py --pdf data/PRML.pdf --dpi 200 --force-rebuild
    python team1_visual.py --pdf data/PRML.pdf --max-pages 85
"""

import argparse
import shutil
import sys
import gc
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from tqdm import tqdm

from utils import (
    ensure_dirs,
    build_faiss_index,
    save_faiss_index,
    save_meta,
    l2_normalize,
    PAGES_DIR,
    INDICES_DIR,
)


def check_poppler():
    if shutil.which("pdftoppm") is None:
        print(
            "ERROR: poppler not found. Install it with:\n"
            "  brew install poppler\n"
            "Then re-run this script."
        )
        sys.exit(1)


def pdf_to_images(pdf_path: str, dpi: int = 150, max_pages: int = None) -> list:
    from pdf2image import convert_from_path

    label = f"first {max_pages}" if max_pages else "all"
    print(f"Converting PDF to images at {dpi} DPI ({label} pages)...")
    kwargs = {"last_page": max_pages} if max_pages else {}
    images = convert_from_path(pdf_path, dpi=dpi, **kwargs)
    image_paths = []
    for i, img in enumerate(tqdm(images, desc="Saving pages")):
        out_path = PAGES_DIR / f"page_{i + 1:04d}.png"
        img.save(out_path, "PNG")
        image_paths.append(str(out_path))
    print(f"Saved {len(image_paths)} page images to {PAGES_DIR}")
    return image_paths


def embed_with_clip(image_paths: list, batch_size: int = 16) -> np.ndarray:
    from transformers import CLIPProcessor, CLIPModel

    model_name = "openai/clip-vit-base-patch32"
    print(f"\nLoading CLIP model ({model_name})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = CLIPModel.from_pretrained(model_name).to(device)
    processor = CLIPProcessor.from_pretrained(model_name)
    model.eval()

    all_embeddings = []
    for i in tqdm(range(0, len(image_paths), batch_size), desc="Embedding with CLIP"):
        batch_paths = image_paths[i : i + batch_size]
        images = [Image.open(p).convert("RGB") for p in batch_paths]
        inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            feats = model.get_image_features(**inputs)
        all_embeddings.append(feats.cpu().numpy())

    embeddings = np.concatenate(all_embeddings, axis=0)
    embeddings = l2_normalize(embeddings)
    print(f"CLIP embeddings: {embeddings.shape}")

    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return embeddings


def embed_with_siglip2(image_paths: list, batch_size: int = 8) -> np.ndarray:
    from transformers import AutoProcessor, AutoModel

    model_name = "google/siglip2-base-patch16-224"
    print(f"\nLoading SigLIP2 model ({model_name})...")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AutoModel.from_pretrained(model_name).to(device)
    from transformers import AutoImageProcessor
    processor = AutoImageProcessor.from_pretrained(model_name)
    model.eval()

    all_embeddings = []
    for i in tqdm(range(0, len(image_paths), batch_size), desc="Embedding with SigLIP2"):
        batch_paths = image_paths[i : i + batch_size]
        images = [Image.open(p).convert("RGB") for p in batch_paths]
        inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            vision_inputs = {k: v for k, v in inputs.items() if "pixel" in k}
            out = model.vision_model(**vision_inputs)
            feats = out.pooler_output
        all_embeddings.append(feats.cpu().numpy())

    embeddings = np.concatenate(all_embeddings, axis=0)
    embeddings = l2_normalize(embeddings)
    print(f"SigLIP2 embeddings: {embeddings.shape}")

    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return embeddings


def main():
    parser = argparse.ArgumentParser(description="Team 1: Visual embedding pipeline")
    parser.add_argument("--pdf", default="data/PRML.pdf", help="Path to input PDF")
    parser.add_argument("--dpi", type=int, default=150, help="Rasterisation DPI")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size for CLIP")
    parser.add_argument("--max-pages", type=int, default=85, help="Maximum pages to embed (0 = all pages)")
    parser.add_argument("--force-rebuild", action="store_true", help="Recompute even if indices exist")
    args = parser.parse_args()

    check_poppler()
    ensure_dirs()

    clip_index_path = INDICES_DIR / "clip.index"
    clip_meta_path = INDICES_DIR / "clip_meta.json"
    siglip_index_path = INDICES_DIR / "siglip2.index"
    siglip_meta_path = INDICES_DIR / "siglip2_meta.json"

    max_pages = args.max_pages if args.max_pages > 0 else None

    # Collect or re-use page images (capped at max_pages)
    existing_pages = sorted(PAGES_DIR.glob("page_*.png"))
    if max_pages:
        existing_pages = existing_pages[:max_pages]
    if existing_pages and not args.force_rebuild:
        label = f"first {max_pages}" if max_pages else "all"
        print(f"Found {len(existing_pages)} existing page images ({label}) — skipping PDF conversion.")
        image_paths = [str(p) for p in existing_pages]
    else:
        image_paths = pdf_to_images(args.pdf, dpi=args.dpi, max_pages=max_pages)

    meta = [
        {"page": i + 1, "image_path": path}
        for i, path in enumerate(image_paths)
    ]

    # CLIP
    if clip_index_path.exists() and not args.force_rebuild:
        print(f"\nCLIP index already exists at {clip_index_path} — skipping.")
    else:
        clip_emb = embed_with_clip(image_paths, batch_size=args.batch_size)
        index = build_faiss_index(clip_emb)
        save_faiss_index(index, clip_index_path)
        save_meta(meta, clip_meta_path)
        print(f"Saved CLIP index ({index.ntotal} vectors) → {clip_index_path}")

    # SigLIP2
    if siglip_index_path.exists() and not args.force_rebuild:
        print(f"SigLIP2 index already exists at {siglip_index_path} — skipping.")
    else:
        siglip_emb = embed_with_siglip2(image_paths, batch_size=8)
        index = build_faiss_index(siglip_emb)
        save_faiss_index(index, siglip_index_path)
        save_meta(meta, siglip_meta_path)
        print(f"Saved SigLIP2 index ({index.ntotal} vectors) → {siglip_index_path}")

    print("\nTeam 1 pipeline complete (CLIP + SigLIP2, 85 pages).")


if __name__ == "__main__":
    main()
