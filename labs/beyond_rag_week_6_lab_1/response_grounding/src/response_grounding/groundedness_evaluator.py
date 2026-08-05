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

from response_grounding.claim_document_matrix_builder import ClaimDocumentMatrixBuilder
from response_grounding.nli_entailment_checker import NLIEntailmentChecker
from response_grounding.semantic_similarity_filter import SemanticSimilarityFilter

class GroundednessEvaluator:
    """Runs the groundedness pipeline for a set of claims against documents.

    Composes matrix construction, semantic filtering, and entailment scoring.
    A claim is grounded if at least one retained edge is marked entailing.
    The groundedness score is the fraction of claims that are grounded.
    """

    def __init__(
        self,
        matrix_builder: ClaimDocumentMatrixBuilder,
        semantic_filter: SemanticSimilarityFilter,
        nli_checker: NLIEntailmentChecker,
    ) -> None:
        """Wire dependencies for the evaluation stages.

        Args:
            matrix_builder: Builds claim-document pairs.
            semantic_filter: Drops low-similarity pairs before NLI.
            nli_checker: Scores entailment for remaining pairs.
        """
        self.matrix_builder = matrix_builder
        self.semantic_filter = semantic_filter
        self.nli_checker = nli_checker

    def evaluate(self, claims: List[str], documents: List[str]) -> Dict[str, object]:
        """Evaluate all claims against the given evidence documents.

        Args:
            claims: Claims to verify (typically from :class:`ClaimExtractor`).
            documents: Evidence chunks or documents aligned with the RAG query.

        Returns:
            Dictionary with keys:

            * ``claim_results``: list of per-claim dicts with ``claim_index``,
              ``claim``, ``is_grounded``, ``best_entailment_probability``,
              and ``best_edge``.
            * ``groundedness_score``: float in [0, 1], ratio of grounded claims.
            * ``scored_edges``: all edges that passed semantic filter, with scores.

            For each claim, the edge with the highest entailment probability is
            selected as ``best_edge``. A claim is marked grounded only if that
            best edge is entailing. Claims with no retained edges are ungrounded
            with ``best_entailment_probability`` set to ``0.0`` and
            ``best_edge`` set to ``None``.

            If ``claims`` is empty, returns empty ``claim_results``,
            ``groundedness_score`` 1.0, and empty ``scored_edges``.
        """
        if not claims:
            return {"claim_results": [], "groundedness_score": 1.0, "scored_edges": []}

        matrix = self.matrix_builder.build(claims, documents)
        semantic_candidates = self.semantic_filter.filter_pairs(matrix)
        scored_edges = self.nli_checker.score_edges(semantic_candidates)

        claim_results: List[Dict[str, object]] = []
        grounded_count = 0

        for claim_index, claim in enumerate(claims):
            related_edges = [edge for edge in scored_edges if edge["claim_index"] == claim_index]
            if len(related_edges) > 0:
                best_edge = max(related_edges, key=lambda x: float(x["entailment_probability"]))
                best_probability = float(best_edge["entailment_probability"])
                is_grounded = best_edge["is_entailing"]
                if is_grounded:
                    grounded_count += 1
            else:
                best_edge = None
                best_probability = 0.0
                is_grounded = False

            claim_results.append(
                {
                    "claim_index": claim_index,
                    "claim": claim,
                    "is_grounded": is_grounded,
                    "best_entailment_probability": best_probability,
                    "best_edge": best_edge,
                }
            )

        groundedness_score = grounded_count / len(claims)
        return {
            "claim_results": claim_results,
            "groundedness_score": groundedness_score,
            "scored_edges": scored_edges,
        }
