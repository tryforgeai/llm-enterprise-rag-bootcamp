#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""PDF ingestion and passage chunking for MemGraphRAG demos."""

from __future__ import annotations

import re
from pathlib import Path

from pypdf import PdfReader

from memg_concepts.models import Passage


def discover_pdfs(data_dir: str | Path, *, recursive: bool = True) -> list[Path]:
    """Return PDF paths under ``data_dir``, sorted for reproducible ingestion."""
    root = Path(data_dir)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")
    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(root.glob(pattern))


def _source_label(pdf_path: Path, base_dir: Path | None = None) -> str:
    if base_dir is not None:
        try:
            return pdf_path.relative_to(base_dir).as_posix()
        except ValueError:
            pass
    return pdf_path.name


def _passage_id_prefix(pdf_path: Path, base_dir: Path) -> str:
    rel = pdf_path.relative_to(base_dir).with_suffix("")
    stem = rel.as_posix().replace("/", "_")
    slug = re.sub(r"[^\w.-]+", "_", stem).strip("_")
    return slug or "doc"


def load_pdf_text(pdf_path: str | Path) -> str:
    reader = PdfReader(str(pdf_path))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n".join(pages)


def chunk_text(
    text: str,
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
) -> list[str]:
    normalized = re.sub(r"\s+", " ", text).strip()
    if not normalized:
        return []

    chunks: list[str] = []
    start = 0
    while start < len(normalized):
        end = min(start + chunk_size, len(normalized))
        chunk = normalized[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= len(normalized):
            break
        start = max(end - chunk_overlap, start + 1)
    return chunks


def build_passages(
    pdf_path: str | Path,
    *,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    max_chunks: int | None = None,
    id_prefix: str | None = None,
    source: str | None = None,
) -> list[Passage]:
    """Chunk a single PDF into passages."""
    text = load_pdf_text(pdf_path)
    chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    if max_chunks is not None:
        chunks = chunks[:max_chunks]

    source_label = source if source is not None else Path(pdf_path).name
    prefix = f"{id_prefix}_" if id_prefix else ""
    return [
        Passage(
            passage_id=f"{prefix}p_{idx:04d}",
            text=chunk,
            source=source_label,
            chunk_index=idx,
        )
        for idx, chunk in enumerate(chunks)
    ]


def build_passages_from_dir(
    data_dir: str | Path,
    *,
    recursive: bool = True,
    chunk_size: int = 800,
    chunk_overlap: int = 120,
    max_chunks_per_doc: int | None = None,
    max_chunks_total: int | None = None,
) -> list[Passage]:
    """Chunk every PDF under ``data_dir`` into globally unique passages."""
    root = Path(data_dir)
    passages: list[Passage] = []
    for pdf_path in discover_pdfs(root, recursive=recursive):
        doc_passages = build_passages(
            pdf_path,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            max_chunks=max_chunks_per_doc,
            id_prefix=_passage_id_prefix(pdf_path, root),
            source=_source_label(pdf_path, root),
        )
        passages.extend(doc_passages)
        if max_chunks_total is not None and len(passages) >= max_chunks_total:
            return passages[:max_chunks_total]
    return passages
