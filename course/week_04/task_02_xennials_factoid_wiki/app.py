#!/usr/bin/env python3
"""Streamlit UI for the Xennials FactoidWiki demo."""

from __future__ import annotations

import json
from pathlib import Path

import streamlit as st

import sv_factoid_wiki as fw


st.set_page_config(
    page_title="Xennials FactoidWiki",
    page_icon="X",
    layout="wide",
)


def load_json_if_exists(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def status_card(label: str, path: Path, count: int | None = None) -> None:
    exists = path.exists()
    state = "ready" if exists else "missing"
    count_text = f" · {count}" if count is not None else ""
    st.metric(label, f"{state}{count_text}")


def artifact_counts() -> dict[str, int]:
    counts = {}
    sections = load_json_if_exists(fw.RAW_SECTIONS_PATH)
    chunks = load_json_if_exists(fw.RAW_CHUNKS_PATH)
    factoids = load_json_if_exists(fw.FACTOIDS_PATH)
    qa = load_json_if_exists(fw.QA_PAIRS_PATH)
    index = load_json_if_exists(fw.INDEX_PATH)
    counts["sections"] = len(sections.get("sections", [])) if sections else 0
    counts["chunks"] = len(chunks.get("chunks", [])) if chunks else 0
    counts["factoids"] = len(factoids.get("factoids", [])) if factoids else 0
    counts["qa_pairs"] = len(qa.get("qa_pairs", [])) if qa else 0
    counts["index_records"] = index.get("record_count", 0) if index else 0
    counts["dimensions"] = index.get("vector_dimensions", 0) if index else 0
    return counts


st.title("Xennials FactoidWiki")
st.caption("Wikipedia -> section-aware chunks -> SV factoids -> QA pairs -> embeddings -> grounded answer")

counts = artifact_counts()

with st.sidebar:
    st.header("Pipeline")
    st.caption("SV cluster only. No TF-IDF fallback.")

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("1. Ingest Wikipedia", use_container_width=True):
            with st.spinner("Fetching and chunking Xennials..."):
                fw.ingest()
            st.rerun()
        if st.button("3. Generate QA pairs", use_container_width=True):
            with st.spinner("Generating QA pairs from factoids..."):
                fw.generate_qa_pairs()
            st.rerun()
    with col_b:
        max_chunks = st.number_input("Factoid chunks", min_value=0, value=0, help="0 means all chunks")
        if st.button("2. Generate factoids", use_container_width=True):
            limit = int(max_chunks) or None
            with st.spinner("Calling SV chat for factoids..."):
                fw.generate_factoids(max_chunks=limit)
            st.rerun()
        if st.button("4. Build SV index", use_container_width=True):
            with st.spinner("Calling SV embedding model..."):
                fw.build_index()
            st.rerun()

    st.divider()
    st.write("Embedding model")
    st.code(fw.DEFAULT_SV_EMBED_MODEL)
    st.write("Chat model")
    st.code(fw.DEFAULT_SV_CHAT_MODEL)

top_metrics = st.columns(5)
with top_metrics[0]:
    status_card("Sections", fw.RAW_SECTIONS_PATH, counts["sections"])
with top_metrics[1]:
    status_card("Chunks", fw.RAW_CHUNKS_PATH, counts["chunks"])
with top_metrics[2]:
    status_card("Factoids", fw.FACTOIDS_PATH, counts["factoids"])
with top_metrics[3]:
    status_card("QA pairs", fw.QA_PAIRS_PATH, counts["qa_pairs"])
with top_metrics[4]:
    status_card("Index", fw.INDEX_PATH, counts["index_records"])

tab_search, tab_factoids, tab_chunks, tab_files = st.tabs(["Search + Answer", "Factoids", "Raw Chunks", "Files"])

with tab_search:
    query = st.text_input(
        "Question",
        value="What birth years are commonly used for Xennials?",
    )
    col_search, col_answer = st.columns([1, 1])
    with col_search:
        if st.button("Search", use_container_width=True):
            if not fw.INDEX_PATH.exists():
                st.error("Build the SV index first.")
            else:
                with st.spinner("Embedding query and searching..."):
                    st.session_state["results"] = fw.search(query, top_k=8)
                    st.session_state["answer"] = None
    with col_answer:
        if st.button("Synthesize answer", use_container_width=True):
            if not fw.INDEX_PATH.exists():
                st.error("Build the SV index first.")
            else:
                with st.spinner("Retrieving evidence and calling SV chat..."):
                    response = fw.answer(query, top_k=8)
                    st.session_state["results"] = response["results"]
                    st.session_state["answer"] = response["answer"]

    if st.session_state.get("answer"):
        st.subheader("SV LLM Answer")
        st.write(st.session_state["answer"])

    results = st.session_state.get("results") or []
    if results:
        st.subheader("Retrieved Evidence")
        for item in results:
            with st.container(border=True):
                st.write(f"**{item['score']:.4f}** · `{item['artifact_type']}` · {item['section']}")
                st.write(item["display_text"])
                st.caption(f"{item['record_id']} · {item['source_url']}")

with tab_factoids:
    factoids_payload = load_json_if_exists(fw.FACTOIDS_PATH)
    if not factoids_payload:
        st.info("Generate factoids first.")
    else:
        sections = sorted({item["section"] for item in factoids_payload["factoids"]})
        selected = st.multiselect("Filter sections", sections, default=sections)
        for factoid in factoids_payload["factoids"]:
            if factoid["section"] not in selected:
                continue
            with st.container(border=True):
                st.write(f"**{factoid['section']}** · `{factoid['factoid_id']}`")
                st.write(factoid["factoid_text"])
                if factoid.get("questions"):
                    st.caption("Questions: " + " / ".join(factoid["questions"][:3]))
                st.caption(factoid["source_url"])

with tab_chunks:
    chunks_payload = load_json_if_exists(fw.RAW_CHUNKS_PATH)
    if not chunks_payload:
        st.info("Ingest Wikipedia first.")
    else:
        for chunk in chunks_payload["chunks"]:
            with st.container(border=True):
                st.write(f"**{chunk['section']}** · `{chunk['chunk_id']}`")
                st.write(chunk["chunk_text"])
                st.caption(chunk["source_url"])

with tab_files:
    st.write("Generated artifacts")
    for path in [
        fw.RAW_SECTIONS_PATH,
        fw.RAW_CHUNKS_PATH,
        fw.FACTOIDS_PATH,
        fw.QA_PAIRS_PATH,
        fw.INDEX_PATH,
    ]:
        st.code(str(path))
        if path.exists():
            st.caption(f"{path.stat().st_size:,} bytes")
