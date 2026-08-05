#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
"""Entry point: sample RAG queries → SVRAG retrieval + generation → response grounding → JSONL."""

import json
import logging
import os
import random
from pathlib import Path
from typing import Any

from svrag import LateChunkEmbedder, QdrantStorage, SVRAG
from svrag.models import RAGResponse, ReferencedChunk

from response_grounding.claim_document_matrix_builder import ClaimDocumentMatrixBuilder
from response_grounding.claim_extractor import ClaimExtractor
from response_grounding.exploratory_retriever import ExploratoryRetriever
from response_grounding.groundedness_evaluator import GroundednessEvaluator
from response_grounding.nli_entailment_checker import NLIEntailmentChecker
from response_grounding.pii_guardrail import PIIGuardrail
from response_grounding.response_grounding_pipeline import ResponseGroundingPipeline
from response_grounding.response_refiner import ResponseRefiner
from response_grounding.semantic_similarity_filter import SemanticSimilarityFilter
from response_grounding.toxicity_guardrail import ToxicityGuardrail

logger = logging.getLogger(__name__)

_BOOTCAMP_ROOT = os.getenv("PROJECT_ROOT_DIR")
OUTPUT_DIR = (
    Path(_BOOTCAMP_ROOT) / "outputs"
    if _BOOTCAMP_ROOT
    else Path(__file__).resolve().parents[2] / "outputs"
)

# Diverse questions across AI foundations, LLMs, agents, and enterprise RAG (sv_rag_pipeline scope).
_QUERY_POOL: list[str] = [
    "What is the attention mechanism in transformer models and why is it important?",
    "How does fine-tuning a large language model differ from prompt engineering alone?",
    "What role does a vector database play in an enterprise retrieval-augmented generation system?",
    "How can an AI agent use external tools to complete multi-step tasks?",
    "What are the tradeoffs between semantic chunking and fixed-size chunking for RAG indexes?",
    "Why is grounding or verifying model outputs against retrieved evidence important in RAG?",
    "What is retrieval-augmented generation and how can it reduce hallucinations?",
    "How do teams typically evaluate quality and faithfulness of RAG systems in production?",
    "What capabilities distinguish an LLM-based agent from a simple conversational chatbot?",
    "What is the difference between encoder-only and decoder-only transformer architectures?",
    "How can hybrid retrieval combining dense and sparse signals improve recall in RAG?",
    "What operational and security considerations matter when deploying LLMs in enterprise settings?",
]


def _referenced_chunk_to_dict(chunk: ReferencedChunk) -> dict[str, Any]:
    return {
        "semantic_id": chunk.semantic_id,
        "parent_id": chunk.parent_id,
        "similarity_score": chunk.similarity_score,
        "pdf_name": chunk.pdf_name,
        "folder_name": chunk.folder_name,
        "chunk_text": chunk.semantic_text,
        "parent_chunk_text": chunk.parent_text,
    }


def _rag_to_record_dict(rag: RAGResponse) -> dict[str, Any]:
    return {
        "query": rag.query,
        "answer": rag.answer,
        "referenced_chunks": [_referenced_chunk_to_dict(c) for c in rag.referenced_chunks],
    }


def _initial_documents_from_rag(rag: RAGResponse) -> list[str]:
    return [c.semantic_text.strip() for c in rag.referenced_chunks if c.semantic_text.strip()]


def _preview(text: str, max_len: int = 120) -> str:
    t = text.replace("\n", " ").strip()
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def run_demo() -> None:
    """Run SVRAG on a random sample of queries, then the grounding pipeline, and write JSONL.

    For each sampled query: embed and search Qdrant, collect nearest chunks (with metadata),
    generate the RAG answer via the configured LLM backend, then evaluate and refine that
    answer with :class:`ResponseGroundingPipeline`. Each line in the output file is one JSON
    object with ``query``, optional ``rag`` / ``grounding_result``, or ``error``.

    Requires Qdrant (indexed collection), query embeddings, and the SVRAG LLM endpoint
    (default Ollama). Optional env: ``OLLAMA_MODEL``, ``OLLAMA_HOST``, ``OLLAMA_PORT``,
    ``SVRAG_SIMILARITY_THRESHOLD``, ``SVRAG_TOP_K``.

    Embedding mode matches ``svrag.service.response_generation_service``: when ``IS_LOCAL``
    is not set to ``true`` (case-insensitive), queries are embedded via the HTTP API at
    ``EMBEDDING_HOST`` / ``EMBEDDING_PORT`` (no local Jina download). Optional ``EMBEDDING_MODEL``
    defaults to ``jinaai/jina-embeddings-v2-base-en``.
    """
    random.seed()
    n_queries = min(10, len(_QUERY_POOL))
    queries = random.sample(_QUERY_POOL, n_queries)
    logger.info("Starting demo: %s queries (sampled from pool of %s)", n_queries, len(_QUERY_POOL))

    logger.info("Connecting to Qdrant …")
    qdrant_storage = QdrantStorage()
    logger.info(
        "Qdrant client ready (collection=%s, %s:%s)",
        qdrant_storage.collection_name,
        qdrant_storage.host,
        qdrant_storage.port,
    )

    is_local = os.getenv("IS_LOCAL", "False").lower() == "true"
    embedding_model = os.getenv("EMBEDDING_MODEL", "jinaai/jina-embeddings-v2-base-en")
    if is_local:
        logger.info(
            "Loading local embedding model %s (first run may download weights) …",
            embedding_model,
        )
    else:
        emb_host = os.getenv("EMBEDDING_HOST", "feynman")
        emb_port = os.getenv("EMBEDDING_PORT", "8123")
        logger.info(
            "Using remote embeddings (%s) at http://%s:%s …",
            embedding_model,
            emb_host,
            emb_port,
        )
    late_embedder = LateChunkEmbedder(model_name=embedding_model, is_local=is_local)
    logger.info("LateChunkEmbedder ready (is_local=%s).", is_local)

    ollama_host = os.getenv("OLLAMA_HOST", "localhost")
    ollama_port = int(os.getenv("OLLAMA_PORT", "11434"))
    ollama_model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
    logger.info(
        "Initializing SVRAG (LLM %s at %s:%s) …",
        ollama_model,
        ollama_host,
        ollama_port,
    )
    sv_rag = SVRAG(
        embedder=late_embedder,
        storage=qdrant_storage,
        ollama_model=ollama_model,
        ollama_host=ollama_host,
        ollama_port=ollama_port,
        similarity_threshold=float(os.getenv("SVRAG_SIMILARITY_THRESHOLD", "0.7")),
        top_k=int(os.getenv("SVRAG_TOP_K", "5")),
        system_prompt_path=f"{os.getenv('SVRAG_PROJECT_PATH')}/prompts/system_prompt.md",
    )
    logger.info("SVRAG ready.")

    logger.info(
        "Building grounding pipeline (spaCy, similarity model, NLI cross-encoder; "
        "first run may download models) …"
    )
    pipeline = ResponseGroundingPipeline(
        claim_extractor=ClaimExtractor(),
        groundedness_evaluator=GroundednessEvaluator(
            matrix_builder=ClaimDocumentMatrixBuilder(),
            semantic_filter=SemanticSimilarityFilter(),
            nli_checker=NLIEntailmentChecker(entailment_threshold=0.50),
        ),
        exploratory_retriever=ExploratoryRetriever(
            qdrant_storage=qdrant_storage,
            embedder=late_embedder,
            top_k=5,
        ),
        response_refiner=ResponseRefiner(),
        pii_guardrail=PIIGuardrail(),
        toxicity_guardrail=ToxicityGuardrail(toxicity_threshold=0.50),
    )
    logger.info("Grounding pipeline ready.")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / "rag_grounding_batch.jsonl"
    logger.info("Writing results to %s", out_path)

    with out_path.open("w", encoding="utf-8") as out:
        for i, query in enumerate(queries, start=1):
            logger.info("[%s/%s] Query: %s", i, n_queries, _preview(query))
            record: dict[str, Any] = {"query": query}
            try:
                logger.info("[%s/%s] RAG: retrieve + generate (may be slow) …", i, n_queries)
                rag_response = sv_rag.query(query)
                n_chunks = len(rag_response.referenced_chunks)
                ans_len = len(rag_response.answer or "")
                logger.info(
                    "[%s/%s] RAG done: %s chunks kept, answer length %s chars",
                    i,
                    n_queries,
                    n_chunks,
                    ans_len,
                )
                record["rag"] = _rag_to_record_dict(rag_response)
                initial_documents = _initial_documents_from_rag(rag_response)
                logger.info("[%s/%s] Grounding pipeline …", i, n_queries)
                grounding_result = pipeline.run(
                    response_text=rag_response.answer or "",
                    initial_documents=initial_documents,
                )
                init_g = grounding_result["initial_groundedness_score"]
                final_g = grounding_result["final_groundedness_score"]
                n_claims = len(grounding_result["claims"])
                logger.info(
                    "[%s/%s] Grounding done: %s claims, score %.3f → %.3f",
                    i,
                    n_queries,
                    n_claims,
                    float(init_g),
                    float(final_g),
                )
                record["grounding_result"] = grounding_result
            except Exception as exc:
                logger.exception("[%s/%s] Query failed", i, n_queries)
                record["error"] = {"type": type(exc).__name__, "message": str(exc)}

            out.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
            out.flush()
            logger.info("[%s/%s] Record flushed to disk.", i, n_queries)

    logger.info("Finished: %s records → %s", n_queries, out_path)
    print(f"Wrote {n_queries} records to {out_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s %(message)s",
        force=True,
    )
    run_demo()
