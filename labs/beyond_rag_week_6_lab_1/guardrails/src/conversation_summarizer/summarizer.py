"""
Conversation summarization functionality using LLM models.

This module provides functions for generating abstractive summaries of conversation history
with support for progressive summarization and SQLite storage.
"""

import sqlite3


def abstractive_summarize_conversation(force_update: bool = False) -> str:
    """Generate abstractive summary of conversation history using LLM, fetching conversation from sqlite."""
    # Connect to SQLite database and fetch conversation history
    conn = sqlite3.connect("conversation_history.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_query, response FROM conversation ORDER BY id ASC")
    rows = cursor.fetchall()
    conn.close()

    # Build conversation history as alternating user and bot turns
    conversation_history = []
    for user_query, response in rows:
        conversation_history.append(f"You: {user_query}")
        if response:
            conversation_history.append(f"Bot: {response}")

    # Return existing summary if conversation hasn't grown much
    if not force_update and len(conversation_history) <= 2:
        return "Not enough conversation to summarize."

    if not conversation_history:
        return "No previous conversation."

    # Progressive summarization: combine existing summary with recent entries
    recent_entries = conversation_history[-4:]  # Last 4 entries
    conversation_text = "\n".join(recent_entries)

    system_prompt = """You are an expert conversation summarizer. Create a concise, coherent summary that captures:
1. Main topics discussed about animals/animal wisdom
2. Key questions asked and insights shared  
3. The conversational flow and context

Previous summary: {existing_summary}

Recent conversation:
{recent_conversation}

Generate a brief, coherent summary (2-3 sentences) that combines the previous summary with recent discussion. Focus on animal-related topics, quotes, and user interests."""

    # For this function, we don't have a running summary, so we use a placeholder
    existing_summary = "Starting new conversation."

    prompt = system_prompt.format(
        existing_summary=existing_summary,
        recent_conversation=conversation_text
    )

    try:
        import ollama
        response = ollama.generate(
            model="gemma2:2b",  # Or your preferred summary model
            prompt=prompt,
            options={"temperature": 0.3, "max_tokens": 150}
        )
        new_summary = response['response'].strip()
        return new_summary

    except Exception as e:
        print(f"⚠️  Abstractive summarization error: {e}")
        # Fallback to simple recent context
        return " | ".join(conversation_history[-3:])
