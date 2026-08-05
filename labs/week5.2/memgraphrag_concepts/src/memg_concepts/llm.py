#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""OpenAI-compatible LLM client used by MemGraphRAG concept demos."""

from __future__ import annotations

from openai import OpenAI

from memg_concepts.config import LlmSettings, resolve_llm_settings


def make_openai_client(settings: LlmSettings | None = None) -> OpenAI:
    cfg = settings or resolve_llm_settings()
    return OpenAI(base_url=cfg.base_url, api_key=cfg.api_key)


def chat_completion(
    messages: list[dict[str, str]],
    *,
    settings: LlmSettings | None = None,
    max_tokens: int = 4096,
) -> str:
    cfg = settings or resolve_llm_settings()
    client = make_openai_client(cfg)
    response = client.chat.completions.create(
        model=cfg.model,
        messages=messages,
        temperature=cfg.temperature,
        max_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()
