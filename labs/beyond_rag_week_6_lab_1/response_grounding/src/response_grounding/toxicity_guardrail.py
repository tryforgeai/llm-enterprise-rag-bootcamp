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
from typing import Any, Dict, Optional

from openai import OpenAI

_DEFAULT_SANITIZE_BASE_URL = "http://localhost:11434/v1"
_DEFAULT_SANITIZE_MODEL = "gpt-oss:20b"


class ToxicityGuardrail:
    """Scores toxicity and sanitizes text when the score exceeds a threshold.

    If the ``detoxify`` package is available, loads Detoxify and uses its
    ``toxicity`` output. Otherwise uses a small keyword heuristic. In both
    cases, elevated scores trigger an LLM rewrite to remove toxicity while
    preserving the main meaning (with a small regex fallback if the model call
    fails).
    """

    def __init__(self, toxicity_threshold: float = 0.50) -> None:
        """Initialize threshold, Detoxify (if available), and the sanitizer client.

        Sanitizer LLM settings use ``TOXICITY_SANITIZE_BASE_URL`` and
        ``TOXICITY_SANITIZE_MODEL`` from the environment when present; if either
        is unset, defaults are local Ollama at ``http://localhost:11434/v1`` and
        model ``gpt-oss:20b``.

        Args:
            toxicity_threshold: Scores at or above this value trigger
                sanitization; below it, text is returned unchanged.
        """
        self.toxicity_threshold = toxicity_threshold
        self._detox_model = self._load_detoxify_model()
        sanitize_base_url = os.getenv("TOXICITY_SANITIZE_BASE_URL", _DEFAULT_SANITIZE_BASE_URL)
        self._sanitize_llm_model = os.getenv("TOXICITY_SANITIZE_MODEL", _DEFAULT_SANITIZE_MODEL)
        self._sanitize_client = OpenAI(
            base_url=sanitize_base_url,
            api_key=os.getenv("OPENAI_API_KEY", "ollama"),
        )

    def apply(self, text: str) -> str:
        """Return sanitized text if toxicity score meets or exceeds threshold.

        Args:
            text: Response text to inspect and possibly clean.

        Returns:
            Original ``text`` if below threshold; otherwise a non-toxic rewrite
            from the configured LLM (or a regex fallback if the call fails).
        """
        toxicity_score = self._score_toxicity(text)
        if toxicity_score < self.toxicity_threshold:
            return text
        return self._sanitize_toxic_text(text)

    def _load_detoxify_model(self) -> Optional[Any]:
        """Load Detoxify ``original`` model if the dependency is installed.

        Returns:
            A Detoxify model instance, or ``None`` if import or construction fails.
        """
        try:
            from detoxify import Detoxify  # type: ignore

            return Detoxify("original")
        except Exception:
            return None

    def _score_toxicity(self, text: str) -> float:
        """Compute a toxicity score in [0, 1].

        Args:
            text: Input to score.

        Returns:
            Detoxify ``toxicity`` probability when the model is loaded; otherwise
            a heuristic score based on a small blocklist of words.
        """
        if self._detox_model is not None:
            predictions: Dict[str, float] = self._detox_model.predict(text)
            return float(predictions.get("toxicity", 0.0))

        fallback_keywords = {"idiot", "stupid", "hate", "trash", "dumb"}
        lowered = text.lower()
        if any(word in lowered for word in fallback_keywords):
            return 0.90
        return 0.0

    def _sanitize_toxic_text(self, text: str) -> str:
        """Rewrite toxic text via a local OpenAI-compatible chat completion.

        Args:
            text: Text presumed toxic enough to require cleaning.

        Returns:
            Model output only (stripped). On failure, falls back to replacing a
            small blocklist with ``[CLEANED]``.
        """
        system = (
            "You rewrite the user's text to remove insults, slurs, hostility, and "
            "other toxic language while keeping the same factual claims and main "
            "point. Respond with only the rewritten text, no preamble or quotes."
        )
        try:
            completion = self._sanitize_client.chat.completions.create(
                model=self._sanitize_llm_model,
                messages=[
                    {"role": "system", "content": system},
                    {
                        "role": "user",
                        "content": f"Rewrite this to be respectful and non-toxic:\n\n{text}",
                    },
                ],
                temperature=0.2,
            )
            message = completion.choices[0].message
            rewritten = (message.content or "").strip()
            if not rewritten:
                return self._sanitize_toxic_text_regex_fallback(text)
            return rewritten
        except Exception:
            return self._sanitize_toxic_text_regex_fallback(text)

    def _sanitize_toxic_text_regex_fallback(self, text: str) -> str:
        toxic_words = ["idiot", "stupid", "hate", "trash", "dumb"]
        sanitized = text
        for word in toxic_words:
            sanitized = re.sub(rf"\b{word}\b", "[CLEANED]", sanitized, flags=re.IGNORECASE)
        return sanitized
