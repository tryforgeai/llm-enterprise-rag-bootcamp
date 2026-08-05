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
import re
from functools import lru_cache
from pathlib import Path
from typing import List

import instructor
from openai import OpenAI
from pydantic import BaseModel, Field

_DEFAULT_BASE_URL = "http://localhost:11434/v1"
_DEFAULT_MODEL = "gpt-oss:20b"


@lru_cache(maxsize=1)
def _claim_extractor_system_prompt() -> str:
    """Load the COSTAR system prompt from ``prompts/claim_extractor_system_prompt.md``."""
    # ``claim_extractor.py`` → ``src/response_grounding`` → ``src`` → project root
    project_root = os.getenv("PROJECT_ROOT_DIR")
    path = Path(project_root) / "prompts" / "claim_extractor_system_prompt.md"
    return path.read_text(encoding="utf-8").strip()


class ClaimExtraction(BaseModel):
    """Structured claim list returned by the extraction LLM."""

    claims: List[str] = Field(
        default_factory=list,
        description=(
            "Ordered factual, verifiable claims from the input; one string per claim."
        ),
    )


class ClaimExtractor:
    """Extracts discrete claims from response text using a local LLM.

    Uses ``instructor`` around an OpenAI-compatible client (e.g. Ollama) with a
    Pydantic response model. If structured extraction fails, falls back to
    sentence-boundary splitting.
    """

    def __init__(self) -> None:
        raw_client = OpenAI(
            base_url=os.getenv("CLAIM_EXTRACTOR_BASE_URL", _DEFAULT_BASE_URL),
            api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        )
        self._client = instructor.from_openai(
            raw_client,
            mode=instructor.Mode.JSON,
        )
        self._model = os.getenv("CLAIM_EXTRACTOR_MODEL", _DEFAULT_MODEL)

    def extract(self, response_text: str) -> List[str]:
        """Extract individual claims from the full response text.

        Args:
            response_text: Raw assistant or RAG-generated response.

        Returns:
            A list of non-empty claim strings, in order of appearance.
        """
        if not response_text or not response_text.strip():
            return []

        try:
            result = self._client.chat.completions.create(
                model=self._model,
                response_model=ClaimExtraction,
                messages=[
                    {
                        "role": "system",
                        "content": _claim_extractor_system_prompt(),
                    },
                    {"role": "user", "content": response_text},
                ],
                temperature=0.0,
            )
            claims = [
                c.strip()
                for c in result.claims
                if isinstance(c, str) and c.strip()
            ]
            if claims:
                return claims
        except Exception:
            pass

        return self._fallback_sentence_split(response_text)

    def _fallback_sentence_split(self, response_text: str) -> List[str]:
        """Fallback extractor based on sentence boundaries."""
        raw_claims = re.split(r"[.!?]\s+|\n+", response_text.strip())
        return [claim.strip() for claim in raw_claims if claim and claim.strip()]
