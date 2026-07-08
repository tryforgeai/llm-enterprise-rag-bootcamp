# Task 2: Xennials FactoidWiki

This demo turns the Wikipedia page for Xennials into a small FactoidWiki-style RAG system.

Source:

```text
https://en.wikipedia.org/wiki/Xennials
```

## Pipeline

```text
Wikipedia page
-> section-aware raw chunks
-> SV chat factoid extraction
-> SV chat QA pair generation
-> SV embedding index
-> cosine search
-> SV chat grounded answer
```

## SV Cluster Endpoints

Chat / LLM:

```text
POST http://10.0.10.51:8000/v1/chat/completions
model = Qwen/Qwen3-VL-8B-Instruct
```

Text embeddings:

```text
POST http://10.0.10.51:8000/embed-text/v1/embeddings
model = Qwen/Qwen3-Embedding-0.6B
```

## Run The Pipeline

From this directory:

```bash
python3 sv_factoid_wiki.py all
```

Or run step by step:

```bash
python3 sv_factoid_wiki.py ingest
python3 sv_factoid_wiki.py factoids
python3 sv_factoid_wiki.py qa
python3 sv_factoid_wiki.py index
python3 sv_factoid_wiki.py search "What birth years are commonly used for Xennials?"
python3 sv_factoid_wiki.py answer "What makes Xennials different from Millennials?"
```

## Run The UI

Streamlit is not bundled in the current Codex Python runtime. Install it in your project environment first:

```bash
python3 -m pip install -r requirements.txt
```

Then:

```bash
streamlit run app.py
```

## Data Files

Generated files live in `data/`:

- `xennials_raw_sections.json`
- `xennials_raw_chunks.json`
- `xennials_factoids.json`
- `xennials_qa_pairs.json`
- `xennials_sv_embedding_index.json`

## What To Look For

- Raw chunks preserve section context.
- Factoids are atomic, self-contained facts.
- QA pairs are query-shaped objects.
- The embedding index stores all artifact types in one searchable space.
- The answer step sends retrieved evidence to the SV chat model and asks it to answer only from evidence.
