#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
from typing import Dict, List

import numpy as np
from sentence_transformers import SentenceTransformer

_DEFAULT_MODEL_NAME = "all-MiniLM-L6-v2"
_DEFAULT_SIMILARITY_THRESHOLD = 0.5


class SemanticSimilarityFilter:
    """First-level filter: drop claim-document pairs below a similarity cutoff.

    Similarity is cosine similarity between sentence-transformer embeddings of
    the claim and document text. Pairs strictly above ``similarity_threshold``
    are kept and annotated with a ``semantic_similarity`` field for downstream
    use.
    """

    def __init__(
        self,
        similarity_threshold: float = _DEFAULT_SIMILARITY_THRESHOLD,
        model_name: str = _DEFAULT_MODEL_NAME,
    ) -> None:
        """Initialize the filter with threshold and embedding model.

        Args:
            similarity_threshold: Minimum cosine similarity in [0, 1] required
                to keep a pair for deeper entailment checking.
            model_name: Name or path of a ``sentence-transformers`` model.
        """
        self.similarity_threshold = similarity_threshold
        self._model = SentenceTransformer(model_name)

    def filter_pairs(self, matrix: List[Dict[str, object]]) -> List[Dict[str, object]]:
        """Keep matrix edges whose claim-document similarity meets the threshold.

        Args:
            matrix: Edges from :class:`ClaimDocumentMatrixBuilder`, each with
                ``claim`` and ``document`` string values.

        Returns:
            A subset of edges, each extended with ``semantic_similarity`` (float).
        """
        if not matrix:
            return []

        claims = [str(edge["claim"]) for edge in matrix]
        documents = [str(edge["document"]) for edge in matrix]

        claim_emb = self._model.encode(
            claims,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        doc_emb = self._model.encode(
            documents,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        similarities = np.sum(claim_emb * doc_emb, axis=1)

        kept: List[Dict[str, object]] = []
        for edge, sim in zip(matrix, similarities, strict=True):
            score = float(sim)
            if score > self.similarity_threshold:
                enriched_edge = dict(edge)
                enriched_edge["semantic_similarity"] = score
                kept.append(enriched_edge)

        return kept
