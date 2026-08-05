#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Embedding utilities for memory filtering and graph bridging."""

from __future__ import annotations

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.preprocessing import normalize

from memg_concepts.config import EmbeddingSettings


class EmbeddingModel:
    def __init__(self, settings: EmbeddingSettings | None = None) -> None:
        cfg = settings or EmbeddingSettings()
        self._backend = "hashing"
        self._hash_vectorizer = HashingVectorizer(
            n_features=384,
            alternate_sign=False,
            norm=None,
        )
        self._model = None
        try:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(cfg.model_name)
            self._backend = "sentence_transformer"
        except Exception:
            self._model = None

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.zeros((0, 0), dtype=np.float32)
        if self._backend == "sentence_transformer" and self._model is not None:
            vectors = self._model.encode(texts, normalize_embeddings=True)
            return np.asarray(vectors, dtype=np.float32)

        matrix = self._hash_vectorizer.transform(texts).toarray()
        return normalize(matrix, norm="l2", axis=1).astype(np.float32)

    @staticmethod
    def cosine_similarity(query_vec: np.ndarray, matrix: np.ndarray) -> np.ndarray:
        if matrix.size == 0:
            return np.zeros(0, dtype=np.float32)
        return matrix @ query_vec
