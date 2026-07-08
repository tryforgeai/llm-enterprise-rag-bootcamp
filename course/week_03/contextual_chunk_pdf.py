#!/usr/bin/env python3
"""Create regular and contextual chunks from a PDF.

This is a local, deterministic version of Anthropic-style Contextual Retrieval:

1. Extract page text from a PDF.
2. Split text into overlapping chunks.
3. Add a short metadata/context prefix to each chunk.
4. Write both regular chunks and contextual chunks as JSONL.

It does not call any network API. The contextual prefix is generated from local
document metadata, page/section hints, and simple keyword extraction.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_PDF = Path("/Users/rosso.han/Downloads/rag-capstone-projects (1).pdf")
DEFAULT_OUT_DIR = Path(__file__).resolve().parent / "capstone_contextual_chunks"
MIN_CHUNK_CHARS = 120

STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "also",
    "and",
    "are",
    "because",
    "been",
    "being",
    "between",
    "both",
    "but",
    "can",
    "could",
    "did",
    "does",
    "doing",
    "each",
    "for",
    "from",
    "had",
    "has",
    "have",
    "having",
    "her",
    "here",
    "his",
    "how",
    "into",
    "its",
    "more",
    "most",
    "not",
    "of",
    "off",
    "our",
    "out",
    "over",
    "own",
    "same",
    "she",
    "should",
    "such",
    "than",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "they",
    "this",
    "those",
    "through",
    "too",
    "under",
    "until",
    "use",
    "used",
    "using",
    "very",
    "was",
    "were",
    "what",
    "when",
    "where",
    "which",
    "while",
    "who",
    "will",
    "with",
    "you",
    "your",
}


@dataclass
class PageText:
    page: int
    text: str
    section: str | None


@dataclass
class RegularChunk:
    chunk_id: int
    page_start: int
    page_end: int
    section: str | None
    char_start: int
    char_end: int
    text: str


@dataclass
class ContextualChunk:
    chunk_id: int
    page_start: int
    page_end: int
    section: str | None
    context: str
    chunk_text: str
    index_text: str


def normalize_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_pdf_pages(pdf_path: Path) -> list[PageText]:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf_path))
    pages: list[PageText] = []
    current_section: str | None = None
    for idx, page in enumerate(reader.pages, start=1):
        text = normalize_text(page.extract_text() or "")
        heading = detect_heading(text)
        if heading:
            current_section = heading
        pages.append(PageText(page=idx, text=text, section=current_section))
    return pages


def detect_title(pages: list[PageText], fallback: str) -> str:
    for page in pages[:3]:
        lines = [line.strip() for line in page.text.splitlines() if line.strip()]
        if lines:
            title = " ".join(lines[:3])
            return re.sub(r"\s+", " ", title)[:180]
    return fallback


def detect_heading(text: str) -> str | None:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:10]:
        cleaned = re.sub(r"\s+", " ", line)
        if len(cleaned) < 6 or len(cleaned) > 120:
            continue
        if re.match(r"^(chapter|project|journey|part|section|appendix)\b", cleaned, re.I):
            return cleaned
        if re.match(r"^\d+(\.\d+)*\s+\S+", cleaned):
            return cleaned
        words = cleaned.split()
        if 2 <= len(words) <= 12:
            titled = sum(1 for w in words if w[:1].isupper())
            if titled / len(words) >= 0.65:
                return cleaned
    return None


def page_stream(pages: Iterable[PageText]) -> tuple[str, list[tuple[int, int, str | None]]]:
    """Return joined text plus spans mapping global char positions to pages."""
    parts: list[str] = []
    spans: list[tuple[int, int, str | None]] = []
    offset = 0
    for page in pages:
        header = f"\n\n[Page {page.page}]\n"
        part = header + page.text
        start = offset
        end = start + len(part)
        parts.append(part)
        spans.append((page.page, end, page.section))
        offset = end
    return "".join(parts).strip(), spans


def page_for_offset(spans: list[tuple[int, int, str | None]], offset: int) -> tuple[int, str | None]:
    for page, end, section in spans:
        if offset <= end:
            return page, section
    if spans:
        page, _, section = spans[-1]
        return page, section
    return 1, None


def split_chunks(
    full_text: str,
    spans: list[tuple[int, int, str | None]],
    *,
    chunk_size: int,
    overlap: int,
) -> list[RegularChunk]:
    chunks: list[RegularChunk] = []
    start = 0
    chunk_id = 0
    while start < len(full_text):
        target_end = min(len(full_text), start + chunk_size)
        end = snap_to_boundary(full_text, start, target_end, chunk_size)
        text = full_text[start:end].strip()
        if len(text) >= MIN_CHUNK_CHARS:
            page_start, section = page_for_offset(spans, start)
            page_end, _ = page_for_offset(spans, end)
            chunks.append(
                RegularChunk(
                    chunk_id=chunk_id,
                    page_start=page_start,
                    page_end=page_end,
                    section=section,
                    char_start=start,
                    char_end=end,
                    text=text,
                )
            )
            chunk_id += 1
        if end >= len(full_text):
            break
        start = max(start + 1, end - overlap)
    return chunks


def snap_to_boundary(full_text: str, start: int, target_end: int, chunk_size: int) -> int:
    if target_end >= len(full_text):
        return len(full_text)
    window = full_text[start:target_end]
    for pattern in ("\n\n", ". ", "? ", "! ", "\n"):
        idx = window.rfind(pattern)
        if idx > chunk_size * 0.55:
            return start + idx + len(pattern)
    idx = window.rfind(" ")
    if idx > chunk_size * 0.55:
        return start + idx + 1
    return target_end


def keywords(text: str, limit: int = 8) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text.lower())
    counts = Counter(w for w in words if w not in STOPWORDS)
    return [word for word, _ in counts.most_common(limit)]


def build_contextual_chunks(chunks: list[RegularChunk], *, document_title: str) -> list[ContextualChunk]:
    contextual: list[ContextualChunk] = []
    for chunk in chunks:
        key_terms = ", ".join(keywords(chunk.text)) or "none"
        section = chunk.section or "unknown section"
        if chunk.page_start == chunk.page_end:
            page_text = f"page {chunk.page_start}"
        else:
            page_text = f"pages {chunk.page_start}-{chunk.page_end}"
        context = (
            f"This chunk is from '{document_title}', {page_text}, under '{section}'. "
            f"It should be retrieved for questions involving these local terms: {key_terms}."
        )
        contextual.append(
            ContextualChunk(
                chunk_id=chunk.chunk_id,
                page_start=chunk.page_start,
                page_end=chunk.page_end,
                section=chunk.section,
                context=context,
                chunk_text=chunk.text,
                index_text=f"{context}\n\n{chunk.text}",
            )
        )
    return contextual


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_preview(path: Path, regular: list[RegularChunk], contextual: list[ContextualChunk], limit: int) -> None:
    lines = ["# Contextual Chunk Preview", ""]
    for reg, ctx in zip(regular[:limit], contextual[:limit]):
        lines.extend(
            [
                f"## Chunk {reg.chunk_id} | pages {reg.page_start}-{reg.page_end}",
                "",
                "**Context**",
                "",
                ctx.context,
                "",
                "**Original chunk preview**",
                "",
                reg.text[:900].strip(),
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create regular and contextual chunks from a PDF.")
    parser.add_argument("--pdf", type=Path, default=DEFAULT_PDF, help="Input PDF path")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="Output directory")
    parser.add_argument("--chunk-size", type=int, default=1800, help="Target characters per chunk")
    parser.add_argument("--overlap", type=int, default=250, help="Character overlap between chunks")
    parser.add_argument("--preview-limit", type=int, default=8, help="Number of chunks in Markdown preview")
    args = parser.parse_args()

    if args.overlap >= args.chunk_size:
        raise ValueError("--overlap must be smaller than --chunk-size")
    if not args.pdf.exists():
        raise FileNotFoundError(args.pdf)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    pages = extract_pdf_pages(args.pdf)
    title = detect_title(pages, args.pdf.stem)
    full_text, spans = page_stream(pages)
    regular = split_chunks(full_text, spans, chunk_size=args.chunk_size, overlap=args.overlap)
    contextual = build_contextual_chunks(regular, document_title=title)

    write_jsonl(args.out_dir / "regular_chunks.jsonl", (asdict(c) for c in regular))
    write_jsonl(args.out_dir / "contextual_chunks.jsonl", (asdict(c) for c in contextual))
    write_preview(args.out_dir / "preview.md", regular, contextual, args.preview_limit)

    stats = {
        "pdf": str(args.pdf),
        "document_title": title,
        "pages": len(pages),
        "non_empty_pages": sum(1 for p in pages if p.text.strip()),
        "characters": len(full_text),
        "chunk_size": args.chunk_size,
        "overlap": args.overlap,
        "chunks": len(regular),
        "regular_chunks": str(args.out_dir / "regular_chunks.jsonl"),
        "contextual_chunks": str(args.out_dir / "contextual_chunks.jsonl"),
        "preview": str(args.out_dir / "preview.md"),
    }
    (args.out_dir / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    main()
