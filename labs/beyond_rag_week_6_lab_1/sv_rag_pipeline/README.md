# SV RAG Pipeline

This project implements a SupportVectors RAG (Retrieval-Augmented Generation) pipeline with:
- A chunking pipeline that converts PDFs into parent/semantic chunks and stores embeddings in Qdrant.
- A FastAPI service that queries the vector database and generates answers using an LLM.
- A Streamlit UI that calls the API and displays results with referenced chunks.

## High-level flow
1. **Chunking**: Convert PDFs to parent chunks (Docling) → semantic chunks (Chonkie) → late-chunk embeddings (Jina) → store in Qdrant.
2. **Retrieval**: Embed user queries (Jina or remote embedding service) → semantic search in Qdrant.
3. **Generation**: Build a prompt with retrieved context and generate a response via an OpenAI-compatible LLM endpoint (Ollama/vLLM).
4. **UI**: A Streamlit app queries the API and renders answers and chunk metadata.

## Project layout
- `chunking_main.py`: Entry point for running the chunking pipeline (root).
- `src/svrag/`: Pipeline, models, storage, and API/UI code.
- `data/`: PDF folders to be indexed (each subfolder can contain PDFs).
- `prompts/system_prompt.md`: System prompt template for RAG responses.
- `pyproject.toml`: Python dependencies for `uv`.

## Setup (uv + pyproject)
From the `sv_rag_pipeline` directory:

1. Create and sync a uv environment:
   - `uv sync`

2. Create a `.env` file:
   - Copy `./.env.example` to `./.env`.
   - Update values for your hosts, ports, and model settings.

`uv run` will use the `.venv` and dependencies from `pyproject.toml`.

## Running the processes (uv run)

### 1) Chunking pipeline
This processes all PDFs under `data/` and writes embeddings to Qdrant.

```
uv run chunking_main.py
```

If the script supports CLI flags or config, use them as needed and keep the Qdrant and embedding env vars set.

### 2) FastAPI RAG service
Starts the API that handles `/query`, `/search`, and `/health`.

```
uv run python -m svrag.service.response_generation_service --host 0.0.0.0 --port 8000 --reload
```

### 3) Streamlit UI
Launches the web UI that calls the FastAPI service.

```
uv run streamlit run src/svrag/ui/streamlit_ui.py
```

## Environment variables
`src/svrag` loads `.env` at runtime. The following variables are used in code; use `.env.example` as a baseline.

### Core paths
- `BOOTCAMP_ROOT_DIR`: Project root used to resolve `prompts/system_prompt.md`.
- `PYTHONPATH`: Helpful for IDEs; typically set to `.../sv_rag_pipeline/src`.
- `PROJECT_PYTHON`: Optional path to the venv python binary.

### Vector database (Qdrant)
- `QDRANT_HOST`: Qdrant host (default: `localhost`, from `.env.example`).
- `QDRANT_PORT`: Qdrant port (default: `6333`, code default).
- `QDRANT_COLLECTION_NAME`: Collection name (default: `supportvectors_ai_knowledge_base`, code default).

### Embeddings
- `EMBEDDING_MODEL`: Jina model name (default: `jinaai/jina-embeddings-v2-base-en`).
- `IS_LOCAL`: `true` uses local transformers for embeddings; `false` uses the remote embedding API for queries (default: `False`, from `.env.example`).
- `EMBEDDING_HOST`: Remote embedding service host (default: `10.0.10.51`, from `.env.example`).
- `EMBEDDING_PORT`: Remote embedding service port (default: `8123`, from `.env.example`).

### LLM / OpenAI-compatible endpoint (Ollama or vLLM)
- `OLLAMA_MODEL`: Model name (default: `openai/gpt-oss-20b`, from `.env.example`).
- `OLLAMA_HOST`: LLM host (default: `10.0.10.51`, from `.env.example`).
- `OLLAMA_PORT`: LLM port (default: `8123`, from `.env.example`).
- `OPENAI_API_KEY`: Required only if your endpoint needs auth (Ollama ignores it, but the client expects a value).

### API service
- `API_HOST`: FastAPI bind host (default: `0.0.0.0`).
- `API_PORT`: FastAPI bind port (default: `8000`).
- `SYSTEM_PROMPT_PATH`: Optional override for the prompt file path.
- `SIMILARITY_THRESHOLD`: Minimum similarity score filter (default: `0.7`).
- `TOP_K`: Max number of chunks to return (default: `5`).

### Streamlit UI
- `API_BASE_URL`: Base URL for the FastAPI service (default: `http://localhost:8000`).

## API endpoints
- `GET /health`: Service health check.
- `POST /query`: Generate an answer with referenced chunks.
- `POST /search`: Search only (no generation).

## Notes
- Ensure Qdrant and your LLM/embedding endpoints are running before starting the API.
- Populate `data/` with PDFs organized into subfolders before running the chunking pipeline.
