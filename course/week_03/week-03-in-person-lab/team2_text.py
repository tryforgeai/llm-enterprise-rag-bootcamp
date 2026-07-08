"""
Team 2 — Text pipeline.

Extracts text from each PDF page, chunks it with a sliding window,
embeds chunks with sentence-transformers, and stores a FAISS index.

Usage:
    python team2_text.py --pdf data/PRML.pdf
    python team2_text.py --pdf data/PRML.pdf --chunk-size 512 --overlap 50
    python team2_text.py --pdf data/PRML.pdf --max-pages 85
"""

import argparse
from pathlib import Path

import numpy as np
from tqdm import tqdm

from utils import (
    ensure_dirs,
    build_faiss_index,
    save_faiss_index,
    save_meta,
    INDICES_DIR,
)

MIN_CHUNK_CHARS = 50


def extract_text_by_page(pdf_path: str, max_pages: int = None) -> list:
    import pdfplumber

    print(f"Extracting text from {pdf_path}" + (f" (first {max_pages} pages)" if max_pages else "") + "...")
    pages = []
    with pdfplumber.open(pdf_path) as pdf:
        page_iter = pdf.pages[:max_pages] if max_pages else pdf.pages
        for i, page in enumerate(tqdm(page_iter, desc="Extracting")):
            text = page.extract_text() or ""
            pages.append({"page": i + 1, "text": text})
    non_empty = sum(1 for p in pages if p["text"].strip())
    print(f"Extracted text from {len(pages)} pages ({non_empty} non-empty)")
    return pages


def chunk_pages(pages: list, chunk_size: int = 512, overlap: int = 50) -> list:
    chunks = []
    chunk_id = 0
    for page_info in pages:
        text = page_info["text"].strip()
        if not text:
            continue
        page_num = page_info["page"]
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            # Snap end to word boundary
            if end < len(text):
                last_space = chunk_text.rfind(" ")
                if last_space > chunk_size // 2:
                    chunk_text = chunk_text[:last_space]
            if len(chunk_text.strip()) >= MIN_CHUNK_CHARS:
                chunks.append({
                    "chunk_id": chunk_id,
                    "page": page_num,
                    "text": chunk_text.strip(),
                    "char_start": start,
                })
                chunk_id += 1
            step = max(1, len(chunk_text) - overlap)
            start += step
    print(f"Created {len(chunks)} chunks from {len(pages)} pages")
    return chunks


def embed_chunks(chunks: list, model_name: str = "all-MiniLM-L6-v2", batch_size: int = 64) -> np.ndarray:
    from sentence_transformers import SentenceTransformer

    print(f"\nLoading sentence-transformers model ({model_name})...")
    model = SentenceTransformer(model_name)
    texts = [c["text"] for c in chunks]
    print(f"Embedding {len(texts)} chunks...")
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        normalize_embeddings=True,
        convert_to_numpy=True,
    )
    print(f"Text embeddings: {embeddings.shape}")
    return embeddings


def main():
    parser = argparse.ArgumentParser(description="Team 2: Text embedding pipeline")
    parser.add_argument("--pdf", default="data/PRML.pdf", help="Path to input PDF")
    parser.add_argument("--chunk-size", type=int, default=512, help="Characters per chunk")
    parser.add_argument("--overlap", type=int, default=50, help="Overlap between consecutive chunks")
    parser.add_argument("--model", default="all-MiniLM-L6-v2", help="sentence-transformers model name")
    parser.add_argument("--max-pages", type=int, default=85, help="Maximum pages to embed (0 = all pages)")
    parser.add_argument("--force-rebuild", action="store_true", help="Recompute even if index exists")
    args = parser.parse_args()

    ensure_dirs()

    index_path = INDICES_DIR / "text.index"
    meta_path = INDICES_DIR / "text_meta.json"

    if index_path.exists() and not args.force_rebuild:
        print(f"Text index already exists at {index_path} — skipping.")
        print("Use --force-rebuild to recompute.")
        return

    pages = extract_text_by_page(args.pdf, max_pages=args.max_pages if args.max_pages > 0 else None)
    chunks = chunk_pages(pages, chunk_size=args.chunk_size, overlap=args.overlap)
    embeddings = embed_chunks(chunks, model_name=args.model)

    # Trim stored text to 300 chars for display; full text stays in memory during pipeline only
    meta = [
        {
            "chunk_id": c["chunk_id"],
            "page": c["page"],
            "text": c["text"][:300],
            "char_start": c["char_start"],
        }
        for c in chunks
    ]

    index = build_faiss_index(embeddings)
    save_faiss_index(index, index_path)
    save_meta(meta, meta_path)
    print(f"\nSaved text index ({index.ntotal} vectors, dim={embeddings.shape[1]}) → {index_path}")
    print("Team 2 pipeline complete.")


if __name__ == "__main__":
    main()
