#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Adjacency and transition matrices for MemGraphRAG graph propagation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from memg_concepts.graph_builder import IndexingGraph


@dataclass(frozen=True)
class GraphMatrices:
    node_ids: list[str]
    adjacency: np.ndarray
    transition: np.ndarray
    out_degree: np.ndarray

    def node_index(self) -> dict[str, int]:
        return {node_id: idx for idx, node_id in enumerate(self.node_ids)}

    def to_dataframe(self):
        import pandas as pd

        return pd.DataFrame(self.adjacency, index=self.node_ids, columns=self.node_ids)


def build_adjacency_matrix(graph: IndexingGraph) -> GraphMatrices:
    node_ids = graph.node_ids()
    index = {node_id: idx for idx, node_id in enumerate(node_ids)}
    n = len(node_ids)
    adjacency = np.zeros((n, n), dtype=np.float32)

    for edge in graph.edges:
        if edge.source not in index or edge.target not in index:
            continue
        i, j = index[edge.source], index[edge.target]
        adjacency[i, j] += edge.weight
        adjacency[j, i] += edge.weight

    out_degree = adjacency.sum(axis=1)
    transition = np.zeros_like(adjacency)
    for i in range(n):
        if out_degree[i] > 0:
            transition[i] = adjacency[i] / out_degree[i]
        else:
            transition[i, i] = 1.0

    return GraphMatrices(
        node_ids=node_ids,
        adjacency=adjacency,
        transition=transition,
        out_degree=out_degree,
    )
