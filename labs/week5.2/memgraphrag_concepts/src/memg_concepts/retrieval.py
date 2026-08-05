#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Memory-guided retrieval using multi-layer filtering and PPR."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from memg_concepts.adjacency import GraphMatrices, build_adjacency_matrix
from memg_concepts.embeddings import EmbeddingModel
from memg_concepts.graph_builder import IndexingGraph
from memg_concepts.memory import GlobalMemory
from memg_concepts.models import NodeKind
from memg_concepts.pagerank import (
    hub_suppression_weight,
    iterate_pagerank,
    personalized_pagerank,
)


@dataclass(frozen=True)
class RetrievedEvidence:
    passage_ids: list[str]
    entity_ids: list[str]
    scores: dict[str, float]


@dataclass(frozen=True)
class QueryInitVectors:
    """Per-layer personalized PageRank reset vectors over the full graph."""

    passage: np.ndarray
    entity: np.ndarray
    type: np.ndarray
    schema: np.ndarray
    combined: np.ndarray
    node_ids: list[str]

    def by_kind(self, graph: IndexingGraph) -> dict[str, dict[str, float]]:
        """Return non-zero reset scores keyed by node kind and node id."""
        index = {node_id: idx for idx, node_id in enumerate(self.node_ids)}
        layers = {
            "passage": self.passage,
            "entity": self.entity,
            "type": self.type,
            "schema": self.schema,
            "combined": self.combined,
        }
        result: dict[str, dict[str, float]] = {}
        for layer_name, vector in layers.items():
            scores: dict[str, float] = {}
            for node_id, idx in index.items():
                value = float(vector[idx])
                if value > 0:
                    scores[node_id] = value
            result[layer_name] = scores
        return result


def _top_k(similarities: np.ndarray, labels: list[str], k: int, threshold: float) -> list[tuple[str, float]]:
    if not labels:
        return []
    ranked = sorted(
        ((label, float(score)) for label, score in zip(labels, similarities)),
        key=lambda item: item[1],
        reverse=True,
    )
    return [item for item in ranked[:k] if item[1] >= threshold]


def build_query_init_vectors(
    query: str,
    memory: GlobalMemory,
    graph: IndexingGraph,
    embedder: EmbeddingModel,
    matrices: GraphMatrices | None = None,
    *,
    top_k_passages: int = 5,
    top_k_entities: int = 8,
    similarity_threshold: float = 0.25,
) -> QueryInitVectors:
    """Build P_init(p), P_init(e), P_init(t), and the combined reset vector v^(0)."""
    matrices = matrices or build_adjacency_matrix(graph)
    node_ids = matrices.node_ids
    node_index = matrices.node_index()
    n = len(node_ids)

    passage_ids = [pid for pid, node in graph.nodes.items() if node.kind == NodeKind.PASSAGE]
    schema_labels = [node.label for node in graph.nodes.values() if node.kind == NodeKind.SCHEMA]
    schema_ids = [node_id for node_id, node in graph.nodes.items() if node.kind == NodeKind.SCHEMA]
    entity_ids = [node_id for node_id, node in graph.nodes.items() if node.kind == NodeKind.ENTITY]
    entity_labels = [graph.nodes[node_id].label for node_id in entity_ids]
    type_ids = [node_id for node_id, node in graph.nodes.items() if node.kind == NodeKind.TYPE]

    query_vec = embedder.encode([query])[0]
    passage_texts = [memory.passages[pid].text for pid in passage_ids]
    passage_scores = embedder.cosine_similarity(query_vec, embedder.encode(passage_texts))
    schema_scores = (
        embedder.cosine_similarity(query_vec, embedder.encode(schema_labels))
        if schema_labels
        else np.zeros(0)
    )
    entity_scores = (
        embedder.cosine_similarity(query_vec, embedder.encode(entity_labels))
        if entity_labels
        else np.zeros(0)
    )

    passage_init = np.zeros(n, dtype=np.float64)
    schema_init = np.zeros(n, dtype=np.float64)
    entity_init = np.zeros(n, dtype=np.float64)
    type_init = np.zeros(n, dtype=np.float64)

    for pid, score in _top_k(passage_scores, passage_ids, top_k_passages, similarity_threshold):
        passage_init[node_index[pid]] += score

    for sid, score in _top_k(schema_scores, schema_ids, 5, similarity_threshold):
        schema_init[node_index[sid]] += score * 0.8

    for eid, score in _top_k(entity_scores, entity_ids, top_k_entities, similarity_threshold):
        degree = float(matrices.out_degree[node_index[eid]])
        entity_init[node_index[eid]] += score * hub_suppression_weight(degree)

    for type_id in type_ids:
        linked_schemas = [
            sid for sid in schema_ids if graph.nodes[type_id].label in graph.nodes[sid].label
        ]
        if not linked_schemas:
            continue
        schema_signal = np.mean(
            [schema_init[node_index[sid]] for sid in linked_schemas if sid in node_index]
        )
        degree = float(matrices.out_degree[node_index[type_id]])
        type_init[node_index[type_id]] += schema_signal * hub_suppression_weight(degree)

    combined = passage_init + schema_init + entity_init + type_init
    if combined.sum() == 0 and passage_ids:
        best = int(np.argmax(passage_scores))
        passage_init[node_index[passage_ids[best]]] = 1.0
        combined = passage_init.copy()

    return QueryInitVectors(
        passage=passage_init.astype(np.float32),
        entity=entity_init.astype(np.float32),
        type=type_init.astype(np.float32),
        schema=schema_init.astype(np.float32),
        combined=combined.astype(np.float32),
        node_ids=node_ids,
    )


def summarize_scores_by_kind(
    scores: np.ndarray,
    graph: IndexingGraph,
    node_ids: list[str],
) -> dict[str, float]:
    """Aggregate probability mass by node kind."""
    totals = {kind.value: 0.0 for kind in NodeKind}
    for node_id, value in zip(node_ids, scores):
        totals[graph.nodes[node_id].kind.value] += float(value)
    return totals


def propagation_history_table(
    history: list[np.ndarray],
    graph: IndexingGraph,
    node_ids: list[str],
    *,
    kinds: tuple[NodeKind, ...] | None = None,
):
    """Build a wide dataframe of node scores across PPR steps."""
    import pandas as pd

    rows: list[dict[str, object]] = []
    for idx, node_id in enumerate(node_ids):
        node = graph.nodes[node_id]
        if kinds and node.kind not in kinds:
            continue
        row: dict[str, object] = {
            "node_id": node_id,
            "kind": node.kind.value,
            "label": node.label,
        }
        for step, scores in enumerate(history):
            row[f"step_{step}"] = float(scores[idx])
        rows.append(row)
    return pd.DataFrame(rows)


def run_lambda_sweep(
    matrices: GraphMatrices,
    reset: np.ndarray,
    *,
    lambdas: tuple[float, ...] = (0.1, 0.3, 0.5, 0.7, 0.9),
    num_steps: int = 10,
) -> dict[float, list[np.ndarray]]:
    """Run fixed-step PPR for each damping value λ."""
    return {
        damping: iterate_pagerank(matrices, reset, damping=damping, num_steps=num_steps)
        for damping in lambdas
    }


def retrieve(
    query: str,
    memory: GlobalMemory,
    graph: IndexingGraph,
    embedder: EmbeddingModel,
    *,
    top_k_passages: int = 5,
    top_k_entities: int = 8,
    similarity_threshold: float = 0.25,
    damping: float = 0.5,
) -> RetrievedEvidence:
    matrices = build_adjacency_matrix(graph)
    inits = build_query_init_vectors(
        query,
        memory,
        graph,
        embedder,
        matrices,
        top_k_passages=top_k_passages,
        top_k_entities=top_k_entities,
        similarity_threshold=similarity_threshold,
    )

    scores = personalized_pagerank(matrices, inits.combined, damping=damping)
    node_index = matrices.node_index()
    score_map = {node_id: float(scores[idx]) for node_id, idx in node_index.items()}

    passage_ids = [pid for pid, node in graph.nodes.items() if node.kind == NodeKind.PASSAGE]
    entity_ids = [node_id for node_id, node in graph.nodes.items() if node.kind == NodeKind.ENTITY]

    ranked_passages = sorted(
        [(pid, score_map[pid]) for pid in passage_ids],
        key=lambda item: item[1],
        reverse=True,
    )[:top_k_passages]
    ranked_entities = sorted(
        [(eid, score_map[eid]) for eid in entity_ids],
        key=lambda item: item[1],
        reverse=True,
    )[:top_k_entities]

    return RetrievedEvidence(
        passage_ids=[pid for pid, _ in ranked_passages],
        entity_ids=[eid for eid, _ in ranked_entities],
        scores=score_map,
    )
