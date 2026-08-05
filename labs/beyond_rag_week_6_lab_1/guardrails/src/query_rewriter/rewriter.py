"""
Query rewriting functionality using LLM models.

This module provides functions for rewriting user queries to be more contextually informed
and suitable for downstream processing, incorporating conversation summaries and retrieved knowledge.
"""

import logging


def rewrite_query_with_context(query: str, summary: str = None, retrievals: list = None) -> str:
    """
    Rewrite the user query using local LLM, incorporating abstractive summary and/or retrieval context.
    Returns a contextually enriched, clarified query for downstream processing.
    Only the final rewritten query is returned; all other information is logged.
    Separate prompt flows for summary only, retrievals only, or both.
    """
    logger = logging.getLogger("query_rewrite")

    # Prepare retrieval context if provided
    retrieval_texts = []
    if retrievals is not None:
        for r in retrievals:
            if hasattr(r, "quote"):
                retrieval_texts.append(f"'{r.quote}' - {r.author}")
            elif hasattr(r, "text"):
                retrieval_texts.append(r.text)
            else:
                retrieval_texts.append(str(r))
    retrieval_context = "\n".join(retrieval_texts) if retrieval_texts else None

    logger.info("Conversation summary:\n%s", summary)
    logger.info("Relevant animal knowledge:\n%s", retrieval_context)
    logger.info("Original user query: %s", query)

    # Choose prompt flow based on which context(s) are present
    if summary and retrieval_context:
        prompt = f"""You are an expert assistant at rewriting user queries for a conversational AI about animal wisdom.

Given:
- The current user query (which may be ambiguous, refer to previous conversation, or lack context)
- A summary of the recent conversation
- Relevant animal quotes or facts retrieved from a knowledge base

Your task:
- Rewrite the user query to be clear, self-contained, and maximally informative for a language model.
- Incorporate relevant context from the conversation summary and retrieved animal knowledge.
- If the original query is ambiguous or references previous turns, resolve the ambiguity using the provided context.
- The rewritten query should be suitable for direct use by an LLM to generate a helpful answer.

Output ONLY the rewritten, contextually enriched query. Do not include any explanations or formatting.

Conversation summary:
{summary}

Relevant animal knowledge:
{retrieval_context}

Original user query:
{query}
"""
    elif summary and not retrieval_context:
        prompt = f"""You are an expert assistant at rewriting user queries for a conversational AI about animal wisdom.

Given:
- The current user query (which may be ambiguous, refer to previous conversation, or lack context)
- A summary of the recent conversation

Your task:
- Rewrite the user query to be clear, self-contained, and maximally informative for a language model.
- Incorporate relevant context from the conversation summary.
- If the original query is ambiguous or references previous turns, resolve the ambiguity using the provided context.
- The rewritten query should be suitable for direct use by an LLM to generate a helpful answer.

Output ONLY the rewritten, contextually enriched query. Do not include any explanations or formatting.

Conversation summary:
{summary}

Original user query:
{query}
"""
    elif retrieval_context and not summary:
        prompt = f"""You are an expert assistant at rewriting user queries for a conversational AI about animal wisdom.

Given:
- The current user query (which may be ambiguous, refer to previous conversation, or lack context)
- Relevant animal quotes or facts retrieved from a knowledge base

Your task:
- Rewrite the user query to be clear, self-contained, and maximally informative for a language model.
- Incorporate relevant context from the retrieved animal knowledge.
- If the original query is ambiguous or references previous turns, resolve the ambiguity using the provided context.
- The rewritten query should be suitable for direct use by an LLM to generate a helpful answer.

Output ONLY the rewritten, contextually enriched query. Do not include any explanations or formatting.

Relevant animal knowledge:
{retrieval_context}

Original user query:
{query}
"""
    else:
        # No context, just return the original query (or optionally, a minimal rewrite prompt)
        logger.info("No summary or retrievals provided; returning original query.")
        return query

    try:
        import ollama
        # Use Ollama to generate the rewritten query
        response = ollama.generate(
            model="llama3.2:latest",  # Use a strong local LLM for rewriting
            prompt=prompt,
            options={"temperature": 0.4, "max_tokens": 128}
        )
        rewritten = response['response'].strip()
        logger.info("Rewritten query: %s", rewritten)
        return rewritten
    except Exception as e:
        logger.error(f"Query rewriting error: {e}")
        # Fallback: return original query
        return query
