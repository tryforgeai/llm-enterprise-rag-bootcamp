#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
"""
Convert PDF files in a directory (and subdirectories) to plain .txt files for GraphRAG indexing.
GraphRAG only supports .txt, .csv, .json — not PDF. Run this before `graphrag index`
if your input is PDF.

Usage:
  uv run python scripts/pdf_to_txt.py [input_dir] [output_dir]
  - input_dir:  folder containing PDFs (searched recursively, including subfolders)
  - output_dir: folder where .txt files are written (default: same as input_dir)

Examples:
  uv run python scripts/pdf_to_txt.py                          # cmp_docs/input -> cmp_docs/input
  uv run python scripts/pdf_to_txt.py sv_docs/data sv_docs/input   # sv_docs/data -> sv_docs/input
  Default input_dir: cmp_docs/input
"""

import sys
from pathlib import Path

import fitz  # pymupdf


def pdf_to_txt(input_dir: Path, output_dir: Path) -> list[Path]:
    input_dir = input_dir.resolve()
    output_dir = output_dir.resolve()
    if not input_dir.is_dir():
        raise SystemExit(f"Not a directory: {input_dir}")

    written: list[Path] = []
    for pdf_path in sorted(input_dir.rglob("*.pdf")):
        rel = pdf_path.relative_to(input_dir)
        txt_path = output_dir / rel.with_suffix(".txt")
        txt_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            doc = fitz.open(pdf_path)
            text = "\n".join(page.get_text() for page in doc)
            doc.close()
        except Exception as e:
            print(f"Error reading {pdf_path}: {e}", file=sys.stderr)
            continue
        txt_path.write_text(text, encoding="utf-8")
        written.append(txt_path)
        print(f"Wrote {txt_path.relative_to(output_dir)}")
    return written


def main() -> None:
    root = Path(__file__).resolve().parent.parent
    input_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "cmp_docs" / "input"
    input_dir = input_dir if input_dir.is_absolute() else root / input_dir
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else input_dir
    output_dir = output_dir if output_dir.is_absolute() else root / output_dir
    paths = pdf_to_txt(input_dir, output_dir)
    if not paths:
        print("No PDF files found.", file=sys.stderr)
        sys.exit(1)
    print(f"Converted {len(paths)} PDF(s) to .txt. You can run: uv run graphrag index --root ./<your_docs_dir>")


if __name__ == "__main__":
    main()
