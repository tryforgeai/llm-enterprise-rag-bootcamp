"""
Conversation Summarizer Module

This module provides functionality for generating abstractive summaries of conversation history
using LLM models, with support for progressive summarization and SQLite storage.
"""

from .summarizer import abstractive_summarize_conversation

__all__ = ["abstractive_summarize_conversation"]
