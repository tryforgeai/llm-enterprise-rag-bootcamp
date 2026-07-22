# Week 03 Representation Tournament

This folder contains the Week 03 chunking, page-image retrieval, text retrieval, and comparison experiments.

## Portable Test Setup

Install the locked Python environment and run the offline unit tests from this directory:

```bash
uv sync --frozen
uv run pytest
```

The unit suite uses fake model clients and does not require API keys or network calls after dependencies are installed.

Live retrieval and answer experiments may require model downloads, optional PDF-rendering packages, and credentials declared through the repository root `.env`. Never commit that file.

`contextual_chunk_pdf.py` defaults to `data/rag-capstone-projects.pdf`. That source is intentionally not committed; pass another repository-relative path with `--pdf` when needed.
