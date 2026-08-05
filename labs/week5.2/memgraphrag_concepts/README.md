# MemGraphRAG Concepts

A walk through [**MemGraphRAG**](https://arxiv.org/abs/2606.00610) — a memory-based multi-agent framework for Graph Retrieval-Augmented Generation.

The demos default to the [*Attention Is All You Need*](data/attention.pdf) paper as the corpus. You can also ingest every PDF recursively under `data/`. Extraction and question answering use a bootcamp-hosted OpenAI-compatible LLM.

---

## What You Will Learn

MemGraphRAG organizes knowledge in a **three-layer global memory**:

| Layer | Contents | Example |
|-------|----------|---------|
| **Schema** | Abstract ontology patterns | `(model, uses, mechanism)` |
| **Fact** | Concrete entity triples | `(Transformer, uses, attention)` |
| **Passage** | Source text chunks | Chunk from `attention.pdf` |

The notebook sequence covers:

1. Why naive GraphRAG suffers from thematic irrelevance, logical inconsistency, and structural fragmentation
2. Offline indexing: extraction → global memory → heterogeneous indexing graph
3. Online retrieval: multi-layer filtering ($P_{init}(p)$, $P_{init}(e)$, $P_{init}(t)$), adjacency matrix, transition matrix, and **Personalized PageRank (PPR)** with configurable $\lambda$
4. Grounded question answering over retrieved passages

---

## Requirements

- [uv](https://docs.astral.sh/uv/) installed
- Python 3.12+
- WireGuard activated (for bootcamp model access)
- Jupyter Lab or Notebook

---

## Setup

From the project root:

```bash
cd memgraphrag_concepts
uv sync
```

Optional: copy environment overrides into `.env` if you use a different endpoint.

| Variable | Default | Purpose |
|----------|---------|---------|
| `GPT_OSS_API_BASE` | `http://10.0.10.51:8000/v1` | OpenAI-compatible API base URL |
| `GPT_OSS_MODEL` | `openai/gpt-oss-20b` | Model name passed to the API |
| `OPENAI_API_KEY` | `not-needed` | API key (dummy value is fine for local servers) |
| `LLM_TEMPERATURE` | `0.0` | Sampling temperature for extraction and QA |

---

## Corpus and Model

- **Default corpus:** `data/attention.pdf` (`DEFAULT_PDF`)
- **Corpus directory:** `data/` (`DEFAULT_DATA_DIR`) — place one or more PDFs here; subfolders are supported
- **LLM:** `openai/gpt-oss-20b` at `http://10.0.10.51:8000/v1`

Notebooks that call the LLM (`03`–`07`) require the model server to be running and reachable.

### Single PDF vs. directory ingestion

By default, notebooks and `build_index()` use the single demo file `data/attention.pdf`. To ingest all PDFs under `data/` recursively:

- In **notebook 02**, set `INGEST_MODE = "directory"`.
- In the **Python API**, pass `data_dir` instead of a single file path:

```python
from memg_concepts.config import DEFAULT_DATA_DIR, DEFAULT_PDF
from memg_concepts.document import build_passages, build_passages_from_dir, discover_pdfs
from memg_concepts.pipeline import build_index

# Single PDF (default)
passages = build_passages(DEFAULT_PDF, max_chunks=12)
index = build_index(DEFAULT_PDF, max_chunks=12)

# All PDFs under data/ (recursive)
pdfs = discover_pdfs(DEFAULT_DATA_DIR)
passages = build_passages_from_dir(DEFAULT_DATA_DIR, max_chunks_per_doc=12)
index = build_index(data_dir=DEFAULT_DATA_DIR, max_chunks_per_doc=12)
```

Directory mode assigns globally unique passage IDs (for example `attention_p_0000`) and records each passage's `source` as its path relative to `data/`. Use `max_chunks_per_doc` to cap chunks per file and optional `max_chunks_total` to cap the full corpus.

---

## Running the Notebooks

Run the notebooks **in order**:

| # | Notebook | Description |
|---|----------|-------------|
| 1 | `01_memgraphrag_overview.ipynb` | Framework overview and configuration |
| 2 | `02_document_ingestion.ipynb` | Load and chunk PDFs (`INGEST_MODE`: single file or `data/` tree) |
| 3 | `03_knowledge_extraction.ipynb` | LLM schema and fact extraction |
| 4 | `04_three_layer_memory.ipynb` | Schema filtering and conflict resolution |
| 5 | `05_memory_graph.ipynb` | Build the heterogeneous indexing graph |
| 6 | `06_adjacency_matrix_ppr.ipynb` | Adjacency / transition matrices, $P_{init}$ reset vectors, PPR propagation, and $\lambda$ sweep (0.1–0.9) |
| 7 | `07_memory_guided_qa.ipynb` | Retrieval-grounded question answering |


---

## Python API (without notebooks)

You can run the full pipeline from Python:

```python
from memg_concepts.config import DEFAULT_DATA_DIR, DEFAULT_PDF
from memg_concepts.pipeline import build_index, query_index

# Single PDF (default)
index = build_index(DEFAULT_PDF, max_chunks=12)

# Or: all PDFs recursively under data/
# index = build_index(data_dir=DEFAULT_DATA_DIR, max_chunks_per_doc=12)

evidence, result = query_index(
    index,
    "What are the main components of multi-head attention?",
)

print("Passages:", result.passage_ids)
print("Answer:", result.answer)
```

`build_index()` performs passage chunking, LLM extraction, memory construction, and graph building. Pass either `pdf_path` for one file or `data_dir` for a recursive corpus. `query_index()` runs memory-guided retrieval and generates an answer.

### Personalized PageRank and multi-layer reset

Notebook `06` and `retrieval.py` implement the paper's query-aware PPR seeding. For a query, the library builds separate reset vectors over all graph nodes:

| Vector | Layer | Source |
|--------|-------|--------|
| `P_init(p)` | Passages | Embedding similarity to the query |
| `P_init(e)` | Entities | Embedding similarity with hub suppression |
| `P_init(t)` | Types | Schema-linked signal with hub suppression |

These are combined into $\mathbf{v}^{(0)}$, then propagated for $n=10$ steps via:

$$\mathbf{v}^{(k+1)} = (1-\lambda)\mathbf{W}\mathbf{v}^{(k)} + \lambda\mathbf{v}^{(0)}$$

```python
from memg_concepts.adjacency import build_adjacency_matrix
from memg_concepts.config import DEFAULT_PDF
from memg_concepts.models import NodeKind
from memg_concepts.pipeline import build_index
from memg_concepts.pagerank import normalize_reset
from memg_concepts.retrieval import (
    build_query_init_vectors,
    propagation_history_table,
    retrieve,
    run_lambda_sweep,
    summarize_scores_by_kind,
)

index = build_index(DEFAULT_PDF, max_chunks=10)
matrices = build_adjacency_matrix(index.graph)
query = "How does multi-head attention work?"

# Per-layer reset vectors for attention.pdf graph nodes
inits = build_query_init_vectors(
    query, index.memory, index.graph, index.embedder, matrices
)
v0 = normalize_reset(inits.combined)
print("v^(0) mass by kind:", summarize_scores_by_kind(v0, index.graph, inits.node_ids))

# Lambda sweep: 10 propagation steps at λ = 0.1, 0.3, …, 0.9
sweeps = run_lambda_sweep(matrices, inits.combined, num_steps=10)
top_at_step_10 = propagation_history_table(
    sweeps[0.5],
    index.graph,
    inits.node_ids,
    kinds=(NodeKind.PASSAGE, NodeKind.ENTITY, NodeKind.TYPE),
).sort_values("step_10", ascending=False)

# Full retrieval (converged PPR + ranked passages/entities)
evidence = retrieve(query, index.memory, index.graph, index.embedder, damping=0.5)
```

Key helpers:

| Module | Function | Purpose |
|--------|----------|---------|
| `retrieval.py` | `build_query_init_vectors()` | Build $P_{init}(p)$, $P_{init}(e)$, $P_{init}(t)$ and combined $\mathbf{v}^{(0)}$ |
| `retrieval.py` | `run_lambda_sweep()` | Run fixed-step PPR for multiple $\lambda$ values |
| `retrieval.py` | `propagation_history_table()` | Per-node scores across propagation steps |
| `retrieval.py` | `summarize_scores_by_kind()` | Aggregate probability mass by node kind |
| `pagerank.py` | `iterate_pagerank()` | Run $k$ PPR update steps and return score history |
| `pagerank.py` | `personalized_pagerank()` | Run PPR to convergence |

---

## Project Structure

```text
memgraphrag_concepts/
├── data/
│   └── attention.pdf              # Default demo corpus (add more PDFs or subfolders as needed)
├── docs/
│   ├── index.md                   # MkDocs landing page
│   └── notebooks/                 # Concept walkthrough notebooks
├── src/
│   └── memg_concepts/             # Supporting library
│       ├── config.py              # LLM and path settings
│       ├── document.py            # PDF discovery, loading, and chunking
│       ├── extraction.py          # LLM schema/fact extraction
│       ├── memory.py              # Three-layer global memory
│       ├── graph_builder.py       # Heterogeneous indexing graph
│       ├── adjacency.py           # Adjacency / transition matrices
│       ├── pagerank.py            # PPR iteration (iterate_pagerank, personalized_pagerank)
│       ├── retrieval.py           # P_init vectors, lambda sweep, memory-guided retrieval
│       ├── qa.py                  # Answer generation
│       └── pipeline.py            # End-to-end helpers
├── scripts/
│   └── generate_notebooks.py      # Regenerate notebook files
├── pyproject.toml
└── config.yaml
```

---

## Reference

- MemGraphRAG paper: [arXiv:2606.00610](https://arxiv.org/abs/2606.00610)
- Official implementation: [XMUDeepLIT/MemGraphRAG](https://github.com/XMUDeepLIT/MemGraphRAG)
