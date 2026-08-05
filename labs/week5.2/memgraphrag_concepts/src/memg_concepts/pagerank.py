#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Personalized PageRank for MemGraphRAG memory-guided retrieval."""

from __future__ import annotations

import numpy as np

from memg_concepts.adjacency import GraphMatrices


def normalize_reset(reset: np.ndarray) -> np.ndarray:
    """L1-normalize a reset vector; fall back to uniform if all zeros."""
    reset = np.asarray(reset, dtype=np.float64)
    total = reset.sum()
    if total <= 0:
        return np.ones_like(reset) / len(reset)
    return reset / total


def personalized_pagerank(
    matrices: GraphMatrices,
    reset: np.ndarray,
    *,
    damping: float = 0.5,
    max_iter: int = 50,
    tol: float = 1e-8,
) -> np.ndarray:
    if reset.shape[0] != matrices.transition.shape[0]:
        raise ValueError("reset vector size must match graph size")

    reset = normalize_reset(reset)

    scores = reset.copy()
    transition = matrices.transition.T
    for _ in range(max_iter):
        next_scores = (1.0 - damping) * transition @ scores + damping * reset
        if np.linalg.norm(next_scores - scores, ord=1) < tol:
            scores = next_scores
            break
        scores = next_scores
    return scores.astype(np.float32)


def iterate_pagerank(
    matrices: GraphMatrices,
    reset: np.ndarray,
    *,
    damping: float = 0.5,
    num_steps: int = 10,
) -> list[np.ndarray]:
    """Run a fixed number of PPR update steps and return score history.

    Implements v^(k+1) = (1 - λ) W v^(k) + λ v^(0) for k = 0 .. num_steps-1.
    The returned list has length num_steps + 1 (step 0 is the normalized reset).
    """
    if reset.shape[0] != matrices.transition.shape[0]:
        raise ValueError("reset vector size must match graph size")

    reset = normalize_reset(reset)
    scores = reset.copy()
    transition = matrices.transition.T
    history = [scores.copy()]
    for _ in range(num_steps):
        scores = (1.0 - damping) * transition @ scores + damping * reset
        history.append(scores.copy())
    return history


def hub_suppression_weight(degree: float) -> float:
    return 1.0 / np.log(degree + 1.0)
