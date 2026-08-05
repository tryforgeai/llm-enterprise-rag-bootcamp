# response-grounding

Post-RAG verification for model answers: **claim-level groundedness** against retrieved evidence, **second-pass retrieval** from the same vector index when claims fail, **response refactoring** from grounded claims only, then **PII** and **toxicity** sanitization. Built for the SupportVectors stack and integrates with the **sv-rag-pipeline** package (Qdrant + `SVRAG`).

Python **3.12+**, managed with **uv**.

## What it does

The design target is a three-part pipeline after you already have a RAG answer and the chunks that were used to generate it:

1. **Groundedness**
   - Extract **claims** from the response (`ClaimExtractor`: OpenAI-compatible LLM + `instructor` / Pydantic, with sentence fallback).
   - Build a **claim × document** matrix (`ClaimDocumentMatrixBuilder`).
   - **Semantic filter** (`SemanticSimilarityFilter`): cosine similarity with `sentence-transformers` (default `all-MiniLM-L6-v2`), default threshold **0.5**; pairs below cutoff skip NLI.
   - **NLI** (`NLIEntailmentChecker`): cross-encoder (default `cross-encoder/nli-deberta-v3-base`); a claim is grounded if some retained edge is entailing above the configured threshold.
   - **Scores**: initial groundedness = fraction of grounded claims.

2. **Exploratory retrieval**
   - For each claim still ungrounded, `ExploratoryRetriever` embeds the claim with `LateChunkEmbedder`, searches **Qdrant** via `QdrantStorage` (same payloads as sv-rag indexing: `text`, `parent_text`), and re-runs groundedness on the new chunk texts.
   - **Final** groundedness score after these updates.
   - **Refactor** (`ResponseRefiner`): LLM rewrites from **grounded claims only** (OpenAI-compatible API; env overrides below).

3. **Response guardrails** (order preserved)
   - **PII** (`PIIGuardrail`): regexes plus optional **spaCy** NER (`en_core_web_sm` by default).
   - **Toxicity** (`ToxicityGuardrail`): **Detoxify** when installed, else a keyword heuristic; over-threshold text is rewritten via an LLM sanitizer.

`ResponseGroundingPipeline.run(response_text, initial_documents)` returns claims, initial/final groundedness scores, per-claim results (including supporting edges), plus **guardrail-sanitized** `original_response` and `revised_response`.

## Layout

| Module | Role |
|--------|------|
| `response_grounding_pipeline.py` | Orchestrates the full flow above. |
| `claim_extractor.py` | Claim segmentation. |
| `claim_document_matrix_builder.py` | Claim–document pairs for scoring. |
| `semantic_similarity_filter.py` | Embedding similarity gate before NLI. |
| `nli_entailment_checker.py` | Cross-encoder entailment. |
| `groundedness_evaluator.py` | Composes matrix → filter → NLI → per-claim results. |
| `exploratory_retriever.py` | Qdrant nearest chunks; `RetrievedChunk` exposes `chunk_text`, `parent_chunk_text`, `similarity_score`. |
| `response_refiner.py` | Revised answer from grounded claims. |
| `pii_guardrail.py` / `toxicity_guardrail.py` | Post-processing. |
| `main.py` | Batch demo: random sample of curriculum-style queries → `SVRAG.query` → grounding → **JSONL** under `outputs/`. |

## Setup

```bash
cd response_grounding
uv sync
```

`pyproject.toml` pulls **sv-rag-pipeline** from a local path by default (`../../llm_bootcamp_curriculum/sv_rag_pipeline`). Adjust `[tool.uv.sources]` if your clone lives elsewhere.

Copy `.env.example` to `.env` and set at least:

- **`BOOTCAMP_ROOT_DIR`**: project root (used by sv-rag prompts and for default **`outputs/`** placement when set).
- **`OPENAI_API_KEY`**: placeholder for clients that require a key (Ollama often uses a dummy value).

Optional tuning (see `.env.example` and module docstrings):

- **SVRAG**: `OLLAMA_MODEL`, `OLLAMA_HOST`, `OLLAMA_PORT`, `SVRAG_SIMILARITY_THRESHOLD` (default **0.7** in `main.py`), `SVRAG_TOP_K`.
- **Claim extraction / refiner / toxicity sanitizer**: `RESPONSE_REFINER_*`, `TOXICITY_SANITIZE_*`, model URLs for Ollama or other OpenAI-compatible servers.
- **NLI / PII**: `NLI_CROSS_ENCODER_MODEL`, `PII_SPACY_MODEL`.

## Running the batch demo

Requires a **Qdrant** instance and collection consistent with **`QdrantStorage`** (same embeddings as indexing), plus the **LLM** endpoints used by `SVRAG`, `ClaimExtractor`, `ResponseRefiner`, and toxicity sanitization (defaults target **Ollama** on `localhost:11434`).

```bash
export PYTHONPATH=src
uv run python -m response_grounding.main
```

Writes **`outputs/rag_grounding_batch.jsonl`**: one JSON object per line with `query`, optional `rag` (answer + referenced chunks with `chunk_text` / `parent_chunk_text`), `grounding_result`, or `error` if a step fails.

If `BOOTCAMP_ROOT_DIR` is unset, `outputs/` is created next to the project root resolved from `main.py` (parent of `src/`).

## Using the pipeline in code

```python
from response_grounding.response_grounding_pipeline import ResponseGroundingPipeline
# ... construct dependencies (ClaimExtractor, GroundednessEvaluator with matrix builder,
#     semantic filter, NLI checker, ExploratoryRetriever with Qdrant + embedder,
#     ResponseRefiner, PIIGuardrail, ToxicityGuardrail)

result = pipeline.run(
    response_text=model_answer,
    initial_documents=list_of_chunk_strings_from_rag,
)
```

