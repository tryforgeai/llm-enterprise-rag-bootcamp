# Week 04 Real RAG Demo

This demo compares four retrieval artifact types over PRML Chapter 2, PRML Chapter 3, and the Dense-X paper:

- raw chunks
- abstractive summaries
- propositions
- QA pairs

This demo is SV-only. It does not include a TF-IDF fallback.

## Run

From this directory:

```bash
python3 server.py
```

Then open:

```text
http://127.0.0.1:4184/
```

The current server in this session is already running at that URL.

## Real RAG Flow

The demo uses two SV cluster capabilities:

- Chat / LLM: `POST http://10.0.10.51:8000/v1/chat/completions`
- Text embeddings: `POST http://10.0.10.51:8000/embed-text/v1/embeddings`

Default chat model:

```text
openai/gpt-oss-20b
```

Default embedding model:

```text
Qwen/Qwen3-Embedding-0.6B
```

## QA Pair Generation

Click `Generate QA pairs`.

The server sends raw chunks to the SV chat model with a prompt asking for retrieval-oriented QA pairs as JSON:

```json
[
  {
    "question": "What is a proposition in Dense-X?",
    "answer": "A proposition is an atomic, self-contained statement...",
    "keywords": ["proposition", "atomic", "retrieval unit"]
  }
]
```

The generated file is saved at:

```text
course/week_04/artifacts/generated_qa_pairs_sv.json
```

## Embedding Flow

The server sends each artifact's `index_text` to the SV cluster:

```http
POST http://10.0.10.51:8000/embed-text/v1/embeddings
Content-Type: application/json
```

The returned vectors are normalized and saved in:

```text
course/week_04/artifacts/sv_embedding_index.json
```

At query time:

1. The user question is embedded with the same SV model.
2. The query vector is compared with artifact vectors using cosine similarity.
3. Top results are grouped by artifact type in the UI.
4. The demo returns an extractive evidence answer with source pointers.

## Configure

Optional environment variables:

```bash
export SV_EMBEDDING_URL="http://10.0.10.51:8000/embed-text/v1/embeddings"
export SV_EMBEDDING_MODEL="Qwen/Qwen3-Embedding-0.6B"
export SV_API_KEY="..." # only if the classroom endpoint requires it
```

The server also reads `.env`, `.env.local`, and `course/week_04/.env` without printing secret values.

## Answer Synthesis

Click `Synthesize answer`.

The server:

1. embeds the query using the SV embedding model
2. retrieves top-k artifact records by cosine similarity
3. sends the retrieved evidence to the SV chat model
4. returns a grounded answer

The model is instructed to answer only from the provided evidence and cite short source ids.
