#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""End-to-end MemGraphRAG concept pipeline helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from memg_concepts.config import DEFAULT_DATA_DIR, DEFAULT_PDF
from memg_concepts.document import build_passages, build_passages_from_dir
from memg_concepts.embeddings import EmbeddingModel
from memg_concepts.extraction import extract_from_passage, to_fact_triples
from memg_concepts.graph_builder import IndexingGraph, build_indexing_graph
from memg_concepts.memory import GlobalMemory
from memg_concepts.qa import QAResult, answer_question
from memg_concepts.retrieval import RetrievedEvidence, retrieve


@dataclass
class MemGraphRAGIndex:
    memory: GlobalMemory
    graph: IndexingGraph
    embedder: EmbeddingModel
    schema_freq_threshold: int = 2


def build_index(
    pdf_path: str | Path = DEFAULT_PDF,
    *,
    data_dir: str | Path | None = None,
    recursive: bool = True,
    max_chunks: int | None = 12,
    max_chunks_per_doc: int | None = None,
    max_chunks_total: int | None = None,
    schema_freq_threshold: int = 2,
) -> MemGraphRAGIndex:
    if data_dir is not None:
        per_doc_limit = max_chunks_per_doc if max_chunks_per_doc is not None else max_chunks
        passages = build_passages_from_dir(
            data_dir,
            recursive=recursive,
            max_chunks_per_doc=per_doc_limit,
            max_chunks_total=max_chunks_total,
        )
    else:
        passages = build_passages(pdf_path, max_chunks=max_chunks)
    memory = GlobalMemory()
    for passage in passages:
        memory.add_passage(passage)
        extraction = extract_from_passage(passage)
        for fact in to_fact_triples(extraction.facts, passage.passage_id):
            memory.add_fact(fact)

    removed = memory.resolve_conflicts(memory.detect_conflicts())
    _ = removed
    # Schemas are constructed programmatically from the surviving typed facts,
    # not emitted by the LLM.
    memory.derive_schemas()
    embedder = EmbeddingModel()
    graph = build_indexing_graph(
        memory,
        embedder=embedder,
        similarity_threshold=0.82,
        min_schema_freq=schema_freq_threshold,
    )
    return MemGraphRAGIndex(
        memory=memory,
        graph=graph,
        embedder=embedder,
        schema_freq_threshold=schema_freq_threshold,
    )


def query_index(index: MemGraphRAGIndex, question: str) -> tuple[RetrievedEvidence, QAResult]:
    evidence = retrieve(
        question,
        index.memory,
        index.graph,
        index.embedder,
    )
    result = answer_question(question, evidence, index.memory, index.graph)
    return evidence, result
