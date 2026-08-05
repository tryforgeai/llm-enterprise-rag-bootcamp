"""
Query Rewriter Module

This module provides functionality for rewriting and enhancing user queries using local LLM models,
incorporating conversation context and retrieved knowledge to create more informative queries.
"""

from .rewriter import rewrite_query_with_context

__all__ = ["rewrite_query_with_context"]
