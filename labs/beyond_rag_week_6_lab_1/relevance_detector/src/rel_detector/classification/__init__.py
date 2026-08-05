"""
Relevance Detection Classification Module.

This module provides a complete system for training and evaluating relevance detection models
using Hugging Face transformers and following best practices.
"""

from .relevance_detector import RelevanceDetector, DataProcessor

__version__ = "0.1.0"

__all__ = [
    # Main classes
    "RelevanceDetector",
    "DataProcessor",
]
