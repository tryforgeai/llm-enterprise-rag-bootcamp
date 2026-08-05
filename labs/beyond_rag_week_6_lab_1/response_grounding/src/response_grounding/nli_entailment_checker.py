#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
import os
from typing import Any, Dict, List

import numpy as np
from sentence_transformers import CrossEncoder

_DEFAULT_CROSS_ENCODER_MODEL = "cross-encoder/nli-deberta-v3-base"


class NLIEntailmentChecker:
    """Scores claim-document pairs with a cross-encoder NLI model.

    Uses ``CrossEncoder`` (e.g. DeBERTa NLI): premise is the document text,
    hypothesis is the claim. ``entailment_probability`` is the softmax
    probability of the entailment class from the model head.
    """

    def __init__(
        self,
        entailment_threshold: float = 0.55,
        model_name: str | None = None,
    ) -> None:
        """Load the cross-encoder and resolve the entailment label index.

        Args:
            entailment_threshold: Minimum entailment probability in [0, 1] to
                treat an edge as supporting the claim.
            model_name: Hugging Face id for a cross-encoder NLI model. Defaults
                to ``NLI_CROSS_ENCODER_MODEL`` from the environment, or
                ``cross-encoder/nli-deberta-v3-base``.
        """
        self.entailment_threshold = entailment_threshold
        resolved = model_name or os.getenv("NLI_CROSS_ENCODER_MODEL", _DEFAULT_CROSS_ENCODER_MODEL)
        self._model = CrossEncoder(resolved)
        self._entailment_idx = _resolve_entailment_class_index(self._model)

    def score_edges(self, candidate_edges: List[Dict[str, object]]) -> List[Dict[str, object]]:
        """Score each candidate edge with entailment probability and a boolean flag.

        Args:
            candidate_edges: Edges that passed semantic pre-filtering; each must
                include ``claim`` and ``document`` strings.

        Returns:
            Edges extended with ``entailment_probability`` (float) and
            ``is_entailing`` (bool).
        """
        if not candidate_edges:
            return []

        pairs = [(str(edge["document"]), str(edge["claim"])) for edge in candidate_edges]
        probs = np.asarray(
            self._model.predict(
                pairs,
                show_progress_bar=False,
                convert_to_numpy=True,
                apply_softmax=True,
            ),
            dtype=np.float64,
        )
        if probs.ndim == 1:
            probs = probs.reshape(1, -1)
        if probs.shape[1] == 1:
            probabilities = probs[:, 0].astype(float)
        else:
            probabilities = probs[:, self._entailment_idx].astype(float)

        scored: List[Dict[str, object]] = []
        for edge, probability in zip(candidate_edges, probabilities, strict=True):
            prob = float(probability)
            enriched_edge = dict(edge)
            enriched_edge["entailment_probability"] = prob
            enriched_edge["is_entailing"] = prob >= self.entailment_threshold
            scored.append(enriched_edge)

        return scored


def _resolve_entailment_class_index(model: Any) -> int:
    cfg = model.model.config
    id2label = getattr(cfg, "id2label", None)
    if not id2label:
        return 1
    for key, label in id2label.items():
        idx = int(key) if not isinstance(key, int) else key
        if str(label).lower() == "entailment":
            return idx
    return 1
