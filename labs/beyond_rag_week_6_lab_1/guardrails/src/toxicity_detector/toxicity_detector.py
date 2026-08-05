# =============================================================================
#  Filename: toxicity_guardrail_simplified.py
#
#  Short Description: Simplified toxicity detection guardrail.
#
#  Creation date: 2025-09-01
#  Author: Simplified Version
# =============================================================================

import re
from typing import Dict, List, Optional
from enum import Enum

# Third-party import (kept as requested)
from detoxify import Detoxify


class GuardrailErrorCode(Enum):
    """Error codes for guardrail violations."""
    INVALID_INPUT_EMPTY = "INVALID_INPUT_EMPTY"
    TOXICITY = "TOXICITY"


class QueryGuardrailError:
    """Represents a guardrail validation error."""
    
    def __init__(self, error_code: GuardrailErrorCode, error_message: str):
        self.error_code = error_code
        self.error_message = error_message


class ToxicityGuardrail:
    """
    Guardrail that detects toxicity, profanity, and offensive language in text.
    
    Uses a combination of:
    - Word-based filtering for common profanity
    - Detoxify model for comprehensive toxicity detection
    
    Attributes:
        profanity_words: Set of profanity words to check for
        toxicity_threshold: Threshold above which content is considered toxic
        mask_char: Character used to mask profanity
    """
    
    def __init__(
        self,
        custom_word_list: Optional[List[str]] = None,
        toxicity_threshold: float = 0.5,
        mask_char: str = "*"
    ):
        """
        Initialize the toxicity guardrail.
        
        Args:
            custom_word_list: Additional profanity words to check for
            toxicity_threshold: Threshold for toxicity detection (0-1)
            mask_char: Character used to mask profanity
        """
        # Validate inputs
        if not (0.0 <= toxicity_threshold <= 1.0):
            raise ValueError("Toxicity threshold must be between 0 and 1")
        
        if not mask_char or len(mask_char) != 1:
            raise ValueError("Mask character must be a single character")
        
        # Basic profanity word list
        self.profanity_words = {
            "fuck", "shit", "damn", "hell", "ass", "bitch",
            "bastard", "crap", "piss", "cock", "dick", "pussy",
            "idiot", "stupid", "dumb", "moron", "retard"
        }
        
        # Add custom words if provided
        if custom_word_list:
            self.profanity_words.update(word.lower() for word in custom_word_list)
        
        # Create regex pattern for word boundary matching
        pattern = r'\b(' + '|'.join(re.escape(word) for word in self.profanity_words) + r')\b'
        self.word_boundary_pattern = re.compile(pattern, re.IGNORECASE)
        
        self.toxicity_threshold = toxicity_threshold
        self.mask_char = mask_char
        
        # Initialize Detoxify model
        print("Loading toxicity detection model...")
        try:
            self.toxicity_model = Detoxify("original")
            print("Toxicity model loaded successfully.")
        except Exception as e:
            raise RuntimeError(f"Failed to load Detoxify model: {e}")
    
    def validate(self, text: Optional[str]) -> Optional[QueryGuardrailError]:
        """
        Check if the input text contains toxicity or profanity.
        
        Args:
            text: The input string to validate
            
        Returns:
            QueryGuardrailError if toxicity detected, None otherwise
        """
        # Check for empty input
        if not text or not text.strip():
            return QueryGuardrailError(
                error_code=GuardrailErrorCode.INVALID_INPUT_EMPTY,
                error_message="Input text cannot be empty"
            )
        
        # Check for explicit profanity words
        if self._contains_profanity(text):
            return QueryGuardrailError(
                error_code=GuardrailErrorCode.TOXICITY,
                error_message="Your query contains language that violates our content policy"
            )
        
        # Check using Detoxify model
        if self._is_toxic(text):
            return QueryGuardrailError(
                error_code=GuardrailErrorCode.TOXICITY,
                error_message="Your query contains language that violates our content policy"
            )
        
        return None
    
    def is_toxic(self, text: str) -> bool:
        """Simple boolean check for toxicity."""
        return self.validate(text) is not None
    
    def get_toxicity_score(self, text: str) -> float:
        """Get the toxicity score (0-1) for the given text."""
        if not text or not text.strip():
            return 0.0
        
        try:
            result = self.toxicity_model.predict(text)
            return result.get("toxicity", 0.0)
        except Exception as e:
            print(f"Error getting toxicity score: {e}")
            return 0.0
    
    def mask_profanity(self, text: str) -> str:
        """
        Mask profanity words in the text.
        
        Args:
            text: Input text that may contain profanity
            
        Returns:
            Text with profanity words masked
        """
        if not text:
            return ""
        
        def replace_match(match):
            word = match.group(0)
            if len(word) <= 2:
                return word[0] + self.mask_char
            return word[0] + self.mask_char * (len(word) - 2) + word[-1]
        
        return self.word_boundary_pattern.sub(replace_match, text)
    
    def _contains_profanity(self, text: str) -> bool:
        """Check if text contains explicit profanity words."""
        return bool(self.word_boundary_pattern.search(text.lower()))
    
    def _is_toxic(self, text: str) -> bool:
        """Check if text is toxic using the Detoxify model."""
        try:
            result = self.toxicity_model.predict(text)
            toxicity_score = result.get("toxicity", 0.0)
            return toxicity_score > self.toxicity_threshold
        except Exception as e:
            print(f"Error predicting toxicity: {e}")
            return False
    
    def get_detailed_scores(self, text: str) -> Dict[str, float]:
        """
        Get detailed toxicity scores for different categories.
        
        Returns:
            Dictionary with toxicity scores for different categories
        """
        if not text or not text.strip():
            return {}
        
        try:
            return self.toxicity_model.predict(text)
        except Exception as e:
            print(f"Error getting detailed scores: {e}")
            return {}


# Example usage and testing
if __name__ == "__main__":
    print("Initializing ToxicityGuardrail...")
    
    try:
        guardrail = ToxicityGuardrail()
        print("ToxicityGuardrail initialized successfully.")
    except Exception as e:
        print(f"Failed to initialize: {e}")
        exit(1)
    
    # Test cases
    test_texts = [
        "This is a clean sentence.",
        "This is fucking awful!",
        "Go to hell, you idiot.",
        "I love puppies and kittens.",
        "You are stupid and ugly.",
        "Kill them all!",
        "What the duck?",
        "",  # Empty string
        "   ",  # Whitespace only
    ]
    
    print("\n" + "="*50)
    print("TOXICITY DETECTION RESULTS")
    print("="*50)
    
    for text in test_texts:
        print(f"\nText: '{text}'")
        
        # Validation check
        result = guardrail.validate(text)
        is_toxic = result is not None
        print(f"Is Toxic: {is_toxic}")
        
        if result:
            print(f"Error: {result.error_message}")
        
        # Get toxicity score if text is valid
        if text and text.strip():
            score = guardrail.get_toxicity_score(text)
            print(f"Toxicity Score: {score:.3f}")
            
            # Show masked version
            masked = guardrail.mask_profanity(text)
            if masked != text:
                print(f"Masked: '{masked}'")
            
            # Show detailed scores
            detailed = guardrail.get_detailed_scores(text)
            if detailed:
                print("Detailed scores:", {k: f"{v:.3f}" for k, v in detailed.items()})
    
    print("\nTesting complete.")
