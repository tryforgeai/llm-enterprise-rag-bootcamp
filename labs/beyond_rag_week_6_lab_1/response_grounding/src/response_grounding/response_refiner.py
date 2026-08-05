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
from typing import List

from openai import OpenAI

_DEFAULT_BASE_URL = "http://localhost:11434/v1"
_DEFAULT_MODEL = "gpt-oss:20b"


class ResponseRefiner:
    """Builds a revised assistant response from grounded claims using a local LLM.

    Calls an OpenAI-compatible chat API (e.g. Ollama). If the call fails or
    returns empty text, falls back to joining claims with periods so the
    pipeline still returns grounded content.
    """

    def __init__(self) -> None:
        """Configure the client from ``RESPONSE_REFINER_BASE_URL`` and
        ``RESPONSE_REFINER_MODEL`` when set; otherwise use local Ollama defaults.
        """
        base_url = os.getenv("RESPONSE_REFINER_BASE_URL", _DEFAULT_BASE_URL)
        self._model = os.getenv("RESPONSE_REFINER_MODEL", _DEFAULT_MODEL)
        self._client = OpenAI(
            base_url=base_url,
            api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        )

    def refine(self, grounded_claims: List[str]) -> str:
        """Synthesize a single reply from grounded claims via the LLM.

        Args:
            grounded_claims: Claims that passed groundedness (and optional
                exploratory) checks, in desired order.

        Returns:
            Model-written reply, or the legacy period-joined string on failure;
            a fixed message when ``grounded_claims`` is empty.
        """
        if not grounded_claims:
            return "No fully grounded claim was found to construct a revised response."

        claims_block = "\n".join(
            f"{i + 1}. {claim.strip()}" for i, claim in enumerate(grounded_claims)
        )
        try:
            completion = self._client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You write a clear, helpful assistant reply for the user. "
                            "You must ONLY use information from the numbered statements "
                            "below. Do not add facts, opinions, or details not supported by "
                            "those statements. Merge overlapping content naturally. "
                            "Output only the reply text, no preamble or list markers."
                        ),
                    },
                    {
                        "role": "user",
                        "content": (
                            "Write one cohesive response using only these verified "
                            f"statements:\n\n{claims_block}"
                        ),
                    },
                ],
                temperature=0.2,
            )
            text = (completion.choices[0].message.content or "").strip()
            if not text:
                return self._fallback_refine(grounded_claims)
            return text
        except Exception:
            return self._fallback_refine(grounded_claims)

    def _fallback_refine(self, grounded_claims: List[str]) -> str:
        return ". ".join(claim.rstrip(". ") for claim in grounded_claims) + "."
