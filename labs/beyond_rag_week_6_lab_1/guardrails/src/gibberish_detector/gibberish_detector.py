# =============================================================================
#  Filename: gibberish_guardrail_simplified.py
#
#  Short Description: Simplified GibberishGuardrail with spaCy and wordfreq.
#
#  Creation date: 2025-09-01
#  Author: Simplified Version
# =============================================================================

import math
import re
from collections import Counter
from typing import Dict, Tuple, Optional
from enum import Enum

# Third-Party Imports (kept as requested)
import spacy
from spacy.tokens import Doc
from wordfreq import zipf_frequency

# Local import
from gibberish_detector.gibberish_smashes import GIBBERISH_SMASHES


class GuardrailErrorCode(Enum):
    """Error codes for guardrail violations."""
    INVALID_INPUT_EMPTY = "INVALID_INPUT_EMPTY"
    INVALID_INPUT_TOO_SHORT = "INVALID_INPUT_TOO_SHORT"
    GIBBERISH_EXACT_MATCH = "GIBBERISH_EXACT_MATCH"
    GIBBERISH_DETECTED = "GIBBERISH_DETECTED"


class QueryGuardrailError:
    """Represents a guardrail validation error."""
    
    def __init__(self, error_code: GuardrailErrorCode, error_message: str):
        self.error_code = error_code
        self.error_message = error_message


class GibberishGuardrail:
    """
    Detects potential gibberish in English text using heuristic features.

    This guardrail analyzes text using a combination of linguistic features:
    - Out-of-vocabulary (OOV) word rate (using spaCy)
    - Average word frequency (using wordfreq's Zipf scale)
    - Character-level Shannon entropy
    - Detection of improbable consecutive consonant clusters
    - Detection of common keyboard-smash patterns

    Args:
        oov_weight: Weight for the OOV feature
        freq_weight: Weight for the frequency score feature
        ent_weight: Weight for the entropy score feature
        cluster_weight: Weight for the cluster detection feature
        pattern_weight: Weight for the keyboard pattern feature
        threshold: Score >= this is considered gibberish
        min_length: Minimum character length for valid input
    """

    # Class-level regex patterns
    _URL_RE = re.compile(
        r"\b(?:https?|ftp)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]*[-A-Za-z0-9+&@#/%=~_|]",
        re.IGNORECASE
    )
    _CLUSTER_RE = re.compile(r"[^aeiouy\s]{5,}", re.IGNORECASE)

    def __init__(
        self,
        oov_weight: float = 0.20,
        freq_weight: float = 0.20,
        ent_weight: float = 0.10,
        cluster_weight: float = 0.15,
        pattern_weight: float = 0.35,
        threshold: float = 0.80,
        min_length: int = 3,
    ):
        """Initialize the GibberishGuardrail."""
        
        # Validate inputs
        weights_sum = sum([oov_weight, freq_weight, ent_weight, cluster_weight, pattern_weight])
        if abs(weights_sum - 1.0) > 0.0001:
            raise ValueError(f"Feature weights must sum to 1.0, got {weights_sum}")
            
        if not (0.0 <= threshold <= 1.0):
            raise ValueError(f"Threshold must be between 0 and 1, got {threshold}")
            
        self.weights = {
            'oov': oov_weight,
            'freq': freq_weight,
            'ent': ent_weight,
            'cluster': cluster_weight,
            'pattern': pattern_weight,
        }
        self.threshold = threshold
        self.min_length = max(0, min_length)

        # Load spaCy model
        try:
            print("Loading spaCy model 'en_core_web_sm'...")
            self._nlp = spacy.load("en_core_web_sm", disable=["parser", "ner"])
            print("spaCy model loaded successfully.")
        except OSError as e:
            raise RuntimeError(
                "Failed to load spaCy model 'en_core_web_sm'. "
                "Install with: python -m spacy download en_core_web_sm"
            ) from e

    def _mask_urls(self, text: str) -> str:
        """Replace URLs with placeholder token."""
        if not text:
            return ""
        try:
            return self._URL_RE.sub("[URL]", text)
        except Exception:
            print("Warning: Error during URL masking, returning original text")
            return text

    def score(self, text: str) -> Tuple[float, Dict[str, float]]:
        """
        Calculate gibberish score for the given text.
        
        Returns:
            Tuple of (score, feature_details) where score is 0-1 
            (0 = normal text, 1 = likely gibberish)
        """
        if not text or not text.strip():
            return 1.0, {
                'oov': 1.0, 'freq': 1.0, 'ent': 1.0, 
                'cluster': 0.0, 'pattern': 0.0
            }

        # Preprocess text
        masked_text = self._mask_urls(text)
        if not masked_text.strip():
            return 1.0, {
                'oov': 1.0, 'freq': 1.0, 'ent': 1.0, 
                'cluster': 0.0, 'pattern': 0.0
            }

        # Process with spaCy
        doc = self._nlp(masked_text)

        # Calculate individual feature scores
        oov_score = self._calculate_oov_score(doc)
        freq_score = self._calculate_freq_score(doc)
        entropy_score = self._calculate_entropy_score(masked_text)
        cluster_score = self._calculate_cluster_score(masked_text)
        pattern_score = self._calculate_pattern_score(masked_text)

        feature_scores = {
            'oov': oov_score,
            'freq': freq_score,
            'ent': entropy_score,
            'cluster': cluster_score,
            'pattern': pattern_score,
        }

        # Calculate weighted total score
        weighted_score = sum(self.weights[k] * v for k, v in feature_scores.items())
        final_score = max(0.0, min(1.0, weighted_score))

        return final_score, feature_scores

    def validate(self, text: Optional[str]) -> Optional[QueryGuardrailError]:
        """
        Validate text for gibberish content.

        Returns:
            QueryGuardrailError if gibberish detected, None if text is valid
        """
        # Check for None or empty input
        if text is None:
            return QueryGuardrailError(
                GuardrailErrorCode.INVALID_INPUT_EMPTY,
                "Input text cannot be None"
            )

        stripped_text = text.strip()
        if not stripped_text:
            return QueryGuardrailError(
                GuardrailErrorCode.INVALID_INPUT_EMPTY,
                "Input text cannot be empty or whitespace only"
            )

        # Check minimum length
        if len(stripped_text) < self.min_length:
            return QueryGuardrailError(
                GuardrailErrorCode.INVALID_INPUT_TOO_SHORT,
                f"Input text is too short (minimum {self.min_length} characters)"
            )

        # Check exact pattern matches
        text_lower = stripped_text.lower()
        if text_lower in GIBBERISH_SMASHES:
            return QueryGuardrailError(
                GuardrailErrorCode.GIBBERISH_EXACT_MATCH,
                "Input matches known keyboard gibberish pattern"
            )

        # Calculate heuristic score
        score, details = self.score(stripped_text)

        if score >= self.threshold:
            return QueryGuardrailError(
                GuardrailErrorCode.GIBBERISH_DETECTED,
                f"Gibberish score ({score:.3f}) exceeds threshold ({self.threshold:.3f})"
            )

        return None

    def is_gibberish(self, text: str) -> bool:
        """Simple boolean check for gibberish."""
        return self.validate(text) is not None

    # --- Feature Calculation Methods ---

    def _calculate_oov_score(self, doc: Doc) -> float:
        """Calculate ratio of out-of-vocabulary alphabetic tokens."""
        alpha_tokens = [token for token in doc if token.is_alpha]
        if not alpha_tokens:
            return 1.0
        
        oov_count = sum(1 for token in alpha_tokens if token.is_oov)
        return oov_count / len(alpha_tokens)

    def _calculate_freq_score(self, doc: Doc) -> float:
        """Calculate score based on average word frequency using Zipf scale."""
        alpha_tokens = [token.text.lower() for token in doc if token.is_alpha]
        if not alpha_tokens:
            return 1.0

        total_zipf = sum(zipf_frequency(word, "en") for word in alpha_tokens)
        avg_zipf = total_zipf / len(alpha_tokens)
        
        # Convert Zipf frequency to score (higher Zipf = more common = lower score)
        # Zipf scale: very common words ~7, rare words ~1-2, gibberish ~0
        score = max(0.0, min(1.0, (3.0 - avg_zipf) / 3.0))
        return score

    def _calculate_entropy_score(self, text: str) -> float:
        """Calculate character-level Shannon entropy score."""
        letters = [c.lower() for c in text if c.isalpha()]
        if not letters:
            return 1.0

        # Calculate Shannon entropy
        total_letters = len(letters)
        char_counts = Counter(letters)
        entropy = -sum(
            (count / total_letters) * math.log2(count / total_letters)
            for count in char_counts.values()
        )

        # Normal English text has entropy around 3.5-4.5
        # Score lower for values in this range
        if 3.0 <= entropy <= 4.5:
            return 0.0
        else:
            # Distance from normal range
            distance = abs(entropy - 3.75)  # 3.75 is middle of normal range
            score = min(1.0, distance / 1.5)
            return score

    def _calculate_cluster_score(self, text: str) -> float:
        """Score 1.0 if long consonant clusters found, 0.0 otherwise."""
        return 1.0 if self._CLUSTER_RE.search(text) else 0.0

    def _calculate_pattern_score(self, text: str) -> float:
        """Score 1.0 if common keyboard patterns found, 0.0 otherwise."""
        text_lower = text.lower()
        return 1.0 if any(pattern in text_lower for pattern in GIBBERISH_SMASHES) else 0.0


# Example usage
if __name__ == "__main__":
    # Initialize guardrail
    guardrail = GibberishGuardrail()
    
    # Test cases
    test_cases = [
        "Hello world, how are you?",  # Normal text
        "asdfasdf",                   # Keyboard smash
        "qwertyuiop",                 # Keyboard row  
        "xkjvhxckvjhxcvkjh",         # Random gibberish
        "The quick brown fox",        # Normal sentence
        "bcdfghjklmnp",              # Consonant cluster
        "aaaaaaaaaaaa",              # Repeated characters
        "This is a normal sentence with proper words",  # Long normal text
    ]
    
    print("Gibberish Detection Results:")
    print("=" * 50)
    
    for text in test_cases:
        result = guardrail.validate(text)
        score, details = guardrail.score(text)
        
        print(f"\nText: '{text}'")
        print(f"Score: {score:.3f} | Gibberish: {result is not None}")
        print(f"Feature scores: {details}")
        
        if result:
            print(f"Error: {result.error_message}")
