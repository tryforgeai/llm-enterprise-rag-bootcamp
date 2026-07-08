#!/usr/bin/env python3
"""Convert a PDF into a text/Markdown textbook artifact.

Pipeline for the Week 03 PDF -> Text path:

    PDF -> parser -> text / Markdown -> optional page sections

The script prefers Docling when available because Docling tries to preserve
document structure such as headings, tables, and reading order. If Docling is
not installed, the script can fall back to pypdf for plain page text extraction.

Examples:

    python course/week_03/pdf_to_textbook.py
    python course/week_03/pdf_to_textbook.py course/week_03/PRML.pdf
    python course/week_03/pdf_to_textbook.py my.pdf --engine docling --format md
    python course/week_03/pdf_to_textbook.py my.pdf --engine pypdf --max-pages 20
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PDF = SCRIPT_DIR / "PRML.pdf"
DEFAULT_OUT_DIR = SCRIPT_DIR / "textbook"


@dataclass(frozen=True)
class ConversionResult:
    engine: str
    content: str
    page_count: int | None = None


def slugify(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-")
    return slug or "document"


def clean_extracted_text(text: str) -> str:
    """Light cleanup for extractor output while preserving paragraph breaks."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def convert_with_docling(pdf_path: Path, output_format: str) -> ConversionResult:
    try:
        from docling.document_converter import DocumentConverter
    except ImportError as exc:
        raise RuntimeError("Docling is not installed in this Python environment.") from exc

    converter = DocumentConverter()
    result = converter.convert(str(pdf_path))
    document = result.document

    if output_format == "md":
        if not hasattr(document, "export_to_markdown"):
            raise RuntimeError("Installed Docling document lacks export_to_markdown().")
        content = document.export_to_markdown()
    elif output_format == "txt":
        if hasattr(document, "export_to_text"):
            content = document.export_to_text()
        elif hasattr(document, "export_to_markdown"):
            content = document.export_to_markdown()
        else:
            raise RuntimeError("Installed Docling document has no text export method.")
    else:
        raise ValueError(f"Unsupported format for Docling: {output_format}")

    return ConversionResult(engine="docling", content=clean_extracted_text(content))


def convert_with_pypdf(
    pdf_path: Path,
    output_format: str,
    max_pages: int | None = None,
) -> ConversionResult:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("pypdf is not installed in this Python environment.") from exc

    reader = PdfReader(str(pdf_path))
    pages = reader.pages[:max_pages] if max_pages else reader.pages
    sections: list[str] = []

    for page_index, page in enumerate(pages, start=1):
        page_text = page.extract_text() or ""
        page_text = clean_extracted_text(page_text)
        if output_format == "md":
            sections.append(f"## Page {page_index}\n\n{page_text}")
        else:
            sections.append(f"[Page {page_index}]\n{page_text}")

    return ConversionResult(
        engine="pypdf",
        content="\n\n".join(sections).strip() + "\n",
        page_count=len(pages),
    )


def convert_pdf(
    pdf_path: Path,
    engine: str,
    output_format: str,
    max_pages: int | None,
) -> ConversionResult:
    if engine == "docling":
        return convert_with_docling(pdf_path, output_format)
    if engine == "pypdf":
        return convert_with_pypdf(pdf_path, output_format, max_pages=max_pages)
    if engine != "auto":
        raise ValueError(f"Unknown engine: {engine}")

    errors: list[str] = []
    try:
        return convert_with_docling(pdf_path, output_format)
    except Exception as exc:
        errors.append(f"Docling failed: {exc}")

    try:
        return convert_with_pypdf(pdf_path, output_format, max_pages=max_pages)
    except Exception as exc:
        errors.append(f"pypdf failed: {exc}")

    message = "\n".join(errors)
    raise RuntimeError(
        "No PDF parser succeeded.\n"
        f"{message}\n\n"
        "Install one parser in your environment, for example:\n"
        "  pip install docling\n"
        "or:\n"
        "  pip install pypdf"
    )


def write_outputs(
    result: ConversionResult,
    pdf_path: Path,
    out_dir: Path,
    output_format: str,
) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    suffix = ".md" if output_format == "md" else ".txt"
    output_path = out_dir / f"{slugify(pdf_path.stem)}.textbook{suffix}"

    header = ""
    if output_format == "md":
        header = (
            f"# {pdf_path.stem}\n\n"
            f"Source PDF: `{pdf_path}`\n\n"
            f"Parser engine: `{result.engine}`\n\n"
            "---\n\n"
        )
    else:
        header = (
            f"{pdf_path.stem}\n"
            f"Source PDF: {pdf_path}\n"
            f"Parser engine: {result.engine}\n\n"
        )

    output_path.write_text(header + result.content, encoding="utf-8")
    return output_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Convert PDF into a text/Markdown textbook file."
    )
    parser.add_argument(
        "pdf",
        nargs="?",
        type=Path,
        default=DEFAULT_PDF,
        help=f"PDF file to convert. Default: {DEFAULT_PDF}",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=DEFAULT_OUT_DIR,
        help=f"Output directory. Default: {DEFAULT_OUT_DIR}",
    )
    parser.add_argument(
        "--format",
        choices=["md", "txt"],
        default="md",
        help="Output format. Default: md",
    )
    parser.add_argument(
        "--engine",
        choices=["auto", "docling", "pypdf"],
        default="auto",
        help="Parser engine. Default: auto",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional page limit for quick tests. Applies to pypdf fallback.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    pdf_path = args.pdf.expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF not found: {pdf_path}", file=sys.stderr)
        return 2
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Input is not a PDF: {pdf_path}", file=sys.stderr)
        return 2

    try:
        result = convert_pdf(
            pdf_path=pdf_path,
            engine=args.engine,
            output_format=args.format,
            max_pages=args.max_pages,
        )
        output_path = write_outputs(
            result=result,
            pdf_path=pdf_path,
            out_dir=args.out_dir.expanduser().resolve(),
            output_format=args.format,
        )
    except Exception as exc:
        print(f"Conversion failed: {exc}", file=sys.stderr)
        return 1

    pages = f", pages={result.page_count}" if result.page_count is not None else ""
    print(f"Converted with {result.engine}{pages}")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
