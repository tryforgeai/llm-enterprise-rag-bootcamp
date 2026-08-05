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
from typing import Any, List, Optional, Tuple

_DEFAULT_SPACY_MODEL = "en_core_web_sm"

_REGEX_PATTERNS: List[Tuple[str, str]] = [
    (r"\b[\w\.-]+@[\w\.-]+\.\w+\b", "[REDACTED_EMAIL]"),
    (r"\b(?:\+?\d{1,2}\s*)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}\b", "[REDACTED_PHONE]"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]"),
    (r"\b(?:\d[ -]*?){13,16}\b", "[REDACTED_CARD]"),
]

# spaCy NER labels treated as person / location-or-address-like PII.
_NER_LABELS_NAME = frozenset({"PERSON"})
_NER_LABELS_ADDRESS = frozenset({"GPE", "LOC", "FAC"})


class PIIGuardrail:
    """Redacts common PII from text using regex and optional spaCy NER.

    Regular expressions cover emails, phone-like numbers, SSN-like patterns,
    and long digit sequences. When a spaCy pipeline is available, named
    entities for people (``PERSON``) and location or facility-like spans
    (``GPE``, ``LOC``, ``FAC``) are redacted as names and addresses. Overlapping
    detections are merged into a single ``[REDACTED_PII]`` span.
    """

    def __init__(self, spacy_model: Optional[str] = None) -> None:
        """Load spaCy NER if the model is installed; otherwise regex-only.

        Args:
            spacy_model: Pipeline package name (e.g. ``en_core_web_sm``).
                Defaults to ``PII_SPACY_MODEL`` from the environment, or
                ``en_core_web_sm``.
        """
        model = spacy_model or os.getenv("PII_SPACY_MODEL", _DEFAULT_SPACY_MODEL)
        self._nlp: Optional[Any] = None
        try:
            import spacy

            self._nlp = spacy.load(model)
        except Exception:
            self._nlp = None

    def apply(self, text: str) -> str:
        """Replace detected PII substrings with fixed redaction tokens.

        Args:
            text: Raw response text that may contain PII.

        Returns:
            Sanitized text with regex- and NER-detected spans substituted.
        """
        spans: List[Tuple[int, int, str]] = []
        for pattern, replacement in _REGEX_PATTERNS:
            for match in re.finditer(pattern, text):
                spans.append((match.start(), match.end(), replacement))

        if self._nlp is not None:
            doc = self._nlp(text)
            for ent in doc.ents:
                if ent.label_ in _NER_LABELS_NAME:
                    spans.append((ent.start_char, ent.end_char, "[REDACTED_NAME]"))
                elif ent.label_ in _NER_LABELS_ADDRESS:
                    spans.append((ent.start_char, ent.end_char, "[REDACTED_ADDRESS]"))

        merged = _merge_spans(spans)
        out = text
        for start, end, replacement in sorted(merged, key=lambda x: x[0], reverse=True):
            out = out[:start] + replacement + out[end:]
        return out


def _merge_spans(spans: List[Tuple[int, int, str]]) -> List[Tuple[int, int, str]]:
    """Merge overlapping intervals; mixed replacement labels become generic PII."""
    if not spans:
        return []

    spans_sorted = sorted(spans, key=lambda x: (x[0], x[1]))
    merged: List[Tuple[int, int, str]] = []
    cur_s, cur_e, cur_r = spans_sorted[0]

    for start, end, repl in spans_sorted[1:]:
        if start < cur_e:
            cur_e = max(cur_e, end)
            cur_r = cur_r if cur_r == repl else "[REDACTED_PII]"
        else:
            merged.append((cur_s, cur_e, cur_r))
            cur_s, cur_e, cur_r = start, end, repl

    merged.append((cur_s, cur_e, cur_r))
    return merged
