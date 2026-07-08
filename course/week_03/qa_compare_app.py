#!/usr/bin/env python3
"""Streamlit UI for comparing Path #1 page-image QA and Path #2 text-chunk QA."""

from __future__ import annotations

import json
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_PDF = SCRIPT_DIR / "PRML.pdf"
DEFAULT_PAGES_DIR = SCRIPT_DIR / "data" / "pages"
DEFAULT_TEXTBOOK = SCRIPT_DIR / "textbook" / "PRML.textbook.md"
FALLBACK_TEXTBOOK = SCRIPT_DIR / "textbook_test" / "PRML.textbook.md"
RUNS_DIR = SCRIPT_DIR / "runs"
DEFAULT_MODEL_ID = "TomoroAI/tomoro-colqwen3-embed-4b"


def shell_join(parts: list[str | Path]) -> str:
    return " ".join(shlex.quote(str(part)) for part in parts)


def build_path1_command(
    *,
    question: str,
    pdf: Path,
    pages_dir: Path,
    output: Path,
    top_k: int,
    max_pages: int | None,
    retrieval_backend: str,
    retrieval_model: str,
    vision_model: str,
) -> str:
    parts: list[str | Path] = [
        sys.executable,
        SCRIPT_DIR / "path1_page_image_qa.py",
        question,
        "--pdf",
        pdf,
        "--pages-dir",
        pages_dir,
        "--out",
        output,
        "--top-k",
        str(top_k),
        "--retrieval-backend",
        retrieval_backend,
        "--retrieval-model",
        retrieval_model,
        "--vision-model",
        vision_model,
    ]
    if max_pages:
        parts.extend(["--max-pages", str(max_pages)])
    return shell_join(parts)


def build_path2_command(
    *,
    question: str,
    pdf: Path,
    textbook: Path,
    output: Path,
    top_k: int,
    chunk_words: int,
    overlap_words: int,
    embedding_model: str,
    answer_model: str,
) -> str:
    parts: list[str | Path] = [
        sys.executable,
        SCRIPT_DIR / "path2_text_chunk_qa.py",
        question,
        "--pdf",
        pdf,
        "--textbook",
        textbook,
        "--out",
        output,
        "--top-k",
        str(top_k),
        "--chunk-words",
        str(chunk_words),
        "--overlap-words",
        str(overlap_words),
        "--embedding-model",
        embedding_model,
        "--answer-model",
        answer_model,
    ]
    return shell_join(parts)


def run_command(command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=SCRIPT_DIR.parents[1],
        check=False,
    )


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def render_result(st, title: str, result: dict[str, Any] | None, raw_output: str = "") -> None:
    st.subheader(title)
    if result is None:
        st.info("No result JSON yet.")
        if raw_output:
            st.code(raw_output)
        return

    st.markdown("**Answer**")
    st.write(result.get("answer", ""))
    st.markdown("**Retrieved evidence**")
    for item in result.get("retrieved", []):
        label = f"rank {item.get('rank')} | score {item.get('score'):.4f}"
        if "page" in item:
            label += f" | page {item.get('page')}"
            with st.expander(label):
                st.write(item.get("image_path"))
        else:
            label += f" | chunk {item.get('chunk_id')}"
            with st.expander(label):
                st.write(item.get("text", ""))
    st.caption(f"Run JSON: {result}")


def main() -> None:
    import streamlit as st

    st.set_page_config(page_title="PRML Representation Tournament", layout="wide")
    st.title("PRML Representation Tournament")
    st.caption("Compare Path #1 page-image retrieval against Path #2 text-chunk retrieval.")

    textbook_default = DEFAULT_TEXTBOOK if DEFAULT_TEXTBOOK.exists() else FALLBACK_TEXTBOOK

    with st.sidebar:
        st.header("Question")
        question = st.text_area(
            "Ask PRML",
            value="What series is PRML part of?",
            height=110,
        )
        pdf = Path(st.text_input("PDF", value=str(DEFAULT_PDF)))
        pages_dir = Path(st.text_input("Page images dir", value=str(DEFAULT_PAGES_DIR)))
        textbook = Path(st.text_input("Textbook Markdown", value=str(textbook_default)))
        top_k = st.slider("Top-k evidence", min_value=1, max_value=10, value=3)
        max_pages = st.number_input("Max pages for Path #1", min_value=0, value=20)

        st.header("Path #1")
        retrieval_backend = st.selectbox(
            "Visual retrieval backend",
            ["colqwen3", "sentence-transformers"],
            index=0,
        )
        retrieval_model = st.text_input("Visual retrieval model", value=DEFAULT_MODEL_ID)
        vision_model = st.text_input("Vision answer model", value="gpt-4.1-mini")

        st.header("Path #2")
        embedding_model = st.text_input("Text embedding model", value="text-embedding-3-small")
        answer_model = st.text_input("Text answer model", value="gpt-4.1-mini")
        chunk_words = st.number_input("Chunk words", min_value=50, max_value=2000, value=350)
        overlap_words = st.number_input("Overlap words", min_value=0, max_value=500, value=60)

        run_path1 = st.checkbox("Run Path #1", value=True)
        run_path2 = st.checkbox("Run Path #2", value=True)
        run_button = st.button("Run comparison", type="primary")

    RUNS_DIR.mkdir(parents=True, exist_ok=True)
    path1_output = RUNS_DIR / "ui_path1_page_image_answer.json"
    path2_output = RUNS_DIR / "ui_path2_text_chunk_answer.json"

    path1_command = build_path1_command(
        question=question,
        pdf=pdf,
        pages_dir=pages_dir,
        output=path1_output,
        top_k=top_k,
        max_pages=max_pages or None,
        retrieval_backend=retrieval_backend,
        retrieval_model=retrieval_model,
        vision_model=vision_model,
    )
    path2_command = build_path2_command(
        question=question,
        pdf=pdf,
        textbook=textbook,
        output=path2_output,
        top_k=top_k,
        chunk_words=chunk_words,
        overlap_words=overlap_words,
        embedding_model=embedding_model,
        answer_model=answer_model,
    )

    with st.expander("Commands"):
        st.code(path1_command)
        st.code(path2_command)

    path1_raw = ""
    path2_raw = ""
    if run_button:
        if run_path1:
            with st.spinner("Running Path #1 page-image QA..."):
                completed = run_command(path1_command)
                path1_raw = completed.stdout + completed.stderr
                if completed.returncode != 0:
                    st.error("Path #1 failed.")
        if run_path2:
            with st.spinner("Running Path #2 text-chunk QA..."):
                completed = run_command(path2_command)
                path2_raw = completed.stdout + completed.stderr
                if completed.returncode != 0:
                    st.error("Path #2 failed.")

    left, right = st.columns(2)
    with left:
        render_result(st, "Path #1: Page Image", read_json(path1_output), path1_raw)
    with right:
        render_result(st, "Path #2: Text Chunk", read_json(path2_output), path2_raw)


if __name__ == "__main__":
    main()
