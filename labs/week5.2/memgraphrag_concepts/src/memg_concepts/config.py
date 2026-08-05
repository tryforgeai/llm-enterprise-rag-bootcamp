#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""LLM and embedding configuration for MemGraphRAG concept demos."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_DATA_DIR = PROJECT_ROOT / "data"
DEFAULT_PDF = DEFAULT_DATA_DIR / "attention.pdf"
DEFAULT_ARTIFACT_DIR = PROJECT_ROOT / "outputs" / "attention"


@dataclass(frozen=True)
class LlmSettings:
    base_url: str
    api_key: str
    model: str
    temperature: float = 0.0


@dataclass(frozen=True)
class EmbeddingSettings:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"


def resolve_llm_settings() -> LlmSettings:
    return LlmSettings(
        base_url=os.getenv("GPT_OSS_API_BASE", "http://10.0.10.51:8000/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "not-needed"),
        model=os.getenv("GPT_OSS_MODEL", "openai/gpt-oss-20b"),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.0")),
    )
