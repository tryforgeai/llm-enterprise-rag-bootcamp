#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
import logging
from typing import Dict, List

from response_grounding.claim_extractor import ClaimExtractor
from response_grounding.exploratory_retriever import ExploratoryRetriever
from response_grounding.groundedness_evaluator import GroundednessEvaluator
from response_grounding.pii_guardrail import PIIGuardrail
from response_grounding.response_refiner import ResponseRefiner
from response_grounding.toxicity_guardrail import ToxicityGuardrail

logger = logging.getLogger(__name__)


class ResponseGroundingPipeline:
    """End-to-end pipeline: grounding, exploratory retrieval, refactor, guardrails.

    Flow: extract claims, evaluate against initial RAG documents, re-evaluate
    ungrounded claims with exploratory retrieval, build a revised response from
    grounded claims only, then apply PII and toxicity guardrails to both
    original and revised outputs.
    """

    def __init__(
        self,
        claim_extractor: ClaimExtractor,
        groundedness_evaluator: GroundednessEvaluator,
        exploratory_retriever: ExploratoryRetriever,
        response_refiner: ResponseRefiner,
        pii_guardrail: PIIGuardrail,
        toxicity_guardrail: ToxicityGuardrail,
    ) -> None:
        """Inject all stage implementations.

        Args:
            claim_extractor: Splits the response into claims.
            groundedness_evaluator: Scores claims against document lists.
            exploratory_retriever: Fetches extra documents for failed claims.
            response_refiner: Builds the revised answer from grounded claims.
            pii_guardrail: Redacts PII (runs before toxicity).
            toxicity_guardrail: Reduces toxic content.
        """
        self.claim_extractor = claim_extractor
        self.groundedness_evaluator = groundedness_evaluator
        self.exploratory_retriever = exploratory_retriever
        self.response_refiner = response_refiner
        self.pii_guardrail = pii_guardrail
        self.toxicity_guardrail = toxicity_guardrail

    def run(self, response_text: str, initial_documents: List[str]) -> Dict[str, object]:
        """Execute the full pipeline on one response and its evidence set.

        Args:
            response_text: Original model response to verify and optionally clean.
            initial_documents: Chunks or documents paired with the query in RAG.

        Returns:
            Dictionary with:

            * ``claims``: extracted claim strings.
            * ``initial_groundedness_score``: score before exploratory retrieval.
            * ``final_groundedness_score``: score after re-checking ungrounded claims.
            * ``claim_results``: per-claim status and best edge.
            * ``original_response``: guardrail-sanitized original text.
            * ``revised_response``: refactored text from grounded claims only, then
              guardrail-sanitized.
        """
        claims = self.claim_extractor.extract(response_text)
        logger.info(f"Extracted the following claims: \n\n{claims}\n\n from the following response: \n\n{response_text}")
        initial_result = self.groundedness_evaluator.evaluate(claims, initial_documents)

        final_claim_results = list(initial_result["claim_results"])  # shallow copy for updates
        for claim_result in final_claim_results:
            if bool(claim_result["is_grounded"]):
                continue

            claim = str(claim_result["claim"])
            exploratory_chunks = self.exploratory_retriever.retrieve(claim)
            exploratory_documents = [
                c.chunk_text for c in exploratory_chunks if c.chunk_text.strip()
            ]
            reevaluated = self.groundedness_evaluator.evaluate([claim], exploratory_documents)
            reevaluated_claim = reevaluated["claim_results"][0]

            # Merge improved groundedness after exploratory retrieval.
            if bool(reevaluated_claim["is_grounded"]):
                claim_result["is_grounded"] = True
                claim_result["best_entailment_probability"] = reevaluated_claim["best_entailment_probability"]
                claim_result["best_edge"] = reevaluated_claim["best_edge"]

        grounded_claims = [str(row["claim"]) for row in final_claim_results if bool(row["is_grounded"])]
        final_score = len(grounded_claims) / len(claims) if claims else 1.0

        revised_response = self.response_refiner.refine(grounded_claims)

        cleaned_original = self._apply_guardrails(response_text)
        cleaned_revised = self._apply_guardrails(revised_response)

        return {
            "claims": claims,
            "initial_groundedness_score": initial_result["groundedness_score"],
            "final_groundedness_score": final_score,
            "claim_results": final_claim_results,
            "original_response": cleaned_original,
            "revised_response": cleaned_revised,
        }


    def _apply_guardrails(self, text: str) -> str:
        """Apply PII redaction then toxicity cleanup.

        Args:
            text: String to sanitize.

        Returns:
            Text after :class:`PIIGuardrail` then :class:`ToxicityGuardrail`.
        """
        pii_sanitized = self.pii_guardrail.apply(text)
        toxicity_sanitized = self.toxicity_guardrail.apply(pii_sanitized)
        return toxicity_sanitized