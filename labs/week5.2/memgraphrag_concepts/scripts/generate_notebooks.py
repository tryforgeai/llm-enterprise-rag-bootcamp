#!/usr/bin/env python3
"""Generate MemGraphRAG concept notebooks."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK_DIR = ROOT / "docs" / "notebooks"


def md(source: str) -> dict:
    return {"cell_type": "markdown", "metadata": {}, "source": source.splitlines(keepends=True)}


def code(source: str) -> dict:
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source.splitlines(keepends=True),
    }


NOTEBOOKS = {
    "01_memgraphrag_overview.ipynb": [
        md(
            "# MemGraphRAG Overview\n\n"
            "MemGraphRAG addresses three failure modes of naive GraphRAG:\n\n"
            "1. **Thematic irrelevance** — off-topic triples pollute the graph.\n"
            "2. **Logical inconsistency** — contradictory facts appear across chunks.\n"
            "3. **Structural fragmentation** — equivalent entities remain disconnected.\n\n"
            "The framework stores knowledge in a **three-layer global memory**:\n\n"
            "- **Schema layer** — abstract `(head_type, relation, tail_type)` patterns.\n"
            "- **Fact layer** — concrete `(head_entity, relation, tail_entity)` triples.\n"
            "- **Passage layer** — source text chunks that ground every fact.\n\n"
            "We will build this pipeline on the *Attention Is All You Need* paper (`data/attention.pdf`)."
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_PDF, resolve_llm_settings\n\n"
            "settings = resolve_llm_settings()\n"
            "print('Corpus:', DEFAULT_PDF)\n"
            "print('LLM:', settings.model)\n"
            "print('Endpoint:', settings.base_url)"
        ),
        md(
            "## Two Phases\n\n"
            "1. **Offline indexing** — agents extract into global memory and project a hierarchical graph.\n"
            "2. **Online retrieval** — multi-layer filtering + Personalized PageRank ranks passages for QA."
        ),
    ],
    "02_document_ingestion.ipynb": [
        md(
            "# Document Ingestion\n\n"
            "GraphRAG starts by turning source PDFs into passage-level chunks that preserve local context "
            "while staying small enough for LLM extraction.\n\n"
            "Set `INGEST_MODE` below to ingest either a single file (`attention.pdf`) or every PDF "
            "recursively under `data/`."
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_DATA_DIR, DEFAULT_PDF\n"
            "from memg_concepts.document import (\n"
            "    build_passages,\n"
            "    build_passages_from_dir,\n"
            "    discover_pdfs,\n"
            "    load_pdf_text,\n"
            ")\n\n"
            'INGEST_MODE = "single"  # "single" for one PDF, "directory" for all PDFs under data/\n\n'
            'if INGEST_MODE == "directory":\n'
            "    pdfs = discover_pdfs(DEFAULT_DATA_DIR)\n"
            '    print(f"Found {len(pdfs)} PDF(s) under {DEFAULT_DATA_DIR}")\n'
            "    for pdf in pdfs:\n"
            '        print(f"  {pdf.relative_to(DEFAULT_DATA_DIR)}")\n'
            "else:\n"
            "    raw_text = load_pdf_text(DEFAULT_PDF)\n"
            "    print(f'Characters loaded: {len(raw_text):,}')\n"
            "    print(raw_text[:500])"
        ),
        code(
            'if INGEST_MODE == "directory":\n'
            "    passages = build_passages_from_dir(\n"
            "        DEFAULT_DATA_DIR,\n"
            "        chunk_size=800,\n"
            "        chunk_overlap=120,\n"
            "        max_chunks_per_doc=12,\n"
            "    )\n"
            "else:\n"
            "    passages = build_passages(\n"
            "        DEFAULT_PDF,\n"
            "        chunk_size=800,\n"
            "        chunk_overlap=120,\n"
            "        max_chunks=12,\n"
            "    )\n\n"
            'print(f"Passages: {len(passages)}")\n'
            "for passage in passages[:3]:\n"
            '    print(passage.passage_id, f"[{passage.source}]", passage.text[:140], "...")'
        ),
        md(
            "These passages become the **Passage layer** (`M_pas`) in global memory."
        ),
    ],
    "03_knowledge_extraction.ipynb": [
        md(
            "# Knowledge Extraction with the LLM\n\n"
            "Extraction is a **two-stage OpenIE pipeline** — the LLM is never asked to "
            "\"generate schemas\":\n\n"
            "1. **Named Entity Recognition** — pull the salient entities out of the passage.\n"
            "2. **RDF triple extraction** — build `(subject, predicate, object)` triples that "
            "reuse those entities.\n\n"
            "A lightweight **entity-typing** pass then labels each entity, and the abstract "
            "**schemas** `(head_type, relation, tail_type)` are *derived* from the typed facts "
            "afterward.\n\n"
            "The configured model is `openai/gpt-oss-20b` on the bootcamp endpoint."
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_PDF\n"
            "from memg_concepts.document import build_passages\n"
            "from memg_concepts.extraction import (\n"
            "    derive_schema_triples,\n"
            "    extract_from_passage,\n"
            "    extract_named_entities,\n"
            "    extract_open_triples,\n"
            "    to_fact_triples,\n"
            "    type_entities,\n"
            ")\n\n"
            "passages = build_passages(DEFAULT_PDF, max_chunks=4)\n"
            "sample = passages[2]\n"
            "print(sample.text[:400])"
        ),
        code(
            "# Stage 1 + 2: NER, then RDF triples that reuse the named entities.\n"
            "entities = extract_named_entities(sample)\n"
            "print('Named entities:', entities)\n\n"
            "triples = extract_open_triples(sample, entities)\n"
            "print('OpenIE triples:', triples[:8])\n\n"
            "# Entity typing turns raw entities into a type lookup.\n"
            "print('Entity types:', type_entities(entities, sample))"
        ),
        code(
            "# The full pipeline: NER -> triples -> typing -> typed facts.\n"
            "extraction = extract_from_passage(sample)\n"
            "facts = to_fact_triples(extraction.facts, sample.passage_id)\n\n"
            "# Schemas are DERIVED from the typed facts, not emitted by the LLM.\n"
            "schemas = derive_schema_triples(extraction.facts)\n"
            "print('Facts:', [f.key() for f in facts])\n"
            "print('Derived schemas:', [s.key() for s in schemas])"
        ),
        md(
            "Schemas fall out of entity typing, so they always stay grounded in the facts and "
            "passages that produced them."
        ),
    ],
    "04_three_layer_memory.ipynb": [
        md(
            "# Three-Layer Global Memory\n\n"
            "Global memory co-evolves with the indexing graph:\n\n"
            "- frequent schemas become **stable** and filter noise\n"
            "- conflicting facts are detected and resolved using passage evidence"
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_PDF\n"
            "from memg_concepts.document import build_passages\n"
            "from memg_concepts.extraction import extract_from_passage, to_fact_triples\n"
            "from memg_concepts.memory import GlobalMemory\n\n"
            "memory = GlobalMemory()\n"
            "for passage in build_passages(DEFAULT_PDF, max_chunks=10):\n"
            "    memory.add_passage(passage)\n"
            "    extraction = extract_from_passage(passage)\n"
            "    for fact in to_fact_triples(extraction.facts, passage.passage_id):\n"
            "        memory.add_fact(fact)\n\n"
            "conflicts = memory.detect_conflicts()\n"
            "removed = memory.resolve_conflicts(conflicts)\n"
            "# Build the schema layer programmatically from the surviving facts.\n"
            "memory.derive_schemas()\n"
            "print('Summary:', memory.summary())\n"
            "print('Conflicts resolved:', len(removed))"
        ),
        code(
            "stable = memory.stable_schemas(min_freq=2)\n"
            "active = memory.active_facts(min_schema_freq=2)\n"
            "print('Stable schemas:', list(stable.keys())[:8])\n"
            "print('Active facts:', list(active.keys())[:8])"
        ),
    ],
    "05_memory_graph.ipynb": [
        md(
            "# Memory-Derived Indexing Graph\n\n"
            "After conflict resolution, memory is projected into a heterogeneous graph with:\n\n"
            "- type and schema nodes\n"
            "- entity nodes and fact edges\n"
            "- passage evidence links\n"
            "- optional similarity bridges between entities"
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_PDF\n"
            "from memg_concepts.embeddings import EmbeddingModel\n"
            "from memg_concepts.pipeline import build_index\n\n"
            "index = build_index(DEFAULT_PDF, max_chunks=10)\n"
            "print('Memory:', index.memory.summary())\n"
            "print('Graph:', index.graph.summary())"
        ),
        code(
            "import networkx as nx\n\n"
            "G = nx.Graph()\n"
            "for node_id, node in index.graph.nodes.items():\n"
            "    G.add_node(node_id, kind=node.kind.value, label=node.label)\n"
            "for edge in index.graph.edges:\n"
            "    G.add_edge(edge.source, edge.target, relation=edge.relation, weight=edge.weight)\n\n"
            "print('Connected components:', nx.number_connected_components(G))\n"
            "print('Sample edges:', [(e.source, e.relation, e.target) for e in index.graph.edges[:6]])"
        ),
        code(
            "import matplotlib.pyplot as plt\n"
            "from matplotlib.patches import Patch\n\n"
            "KIND_COLORS = {\n"
            "    'type': '#4C78A8',\n"
            "    'entity': '#F58518',\n"
            "    'schema': '#54A24B',\n"
            "    'passage': '#B279A2',\n"
            "}\n\n"
            "labels = {}\n"
            "for node_id, data in G.nodes(data=True):\n"
            "    if data['kind'] == 'passage':\n"
            "        chunk = index.graph.nodes[node_id].metadata.get('chunk_index', '?')\n"
            "        labels[node_id] = f'P{chunk}'\n"
            "    else:\n"
            "        label = data['label']\n"
            "        labels[node_id] = label if len(label) <= 24 else label[:21] + '...'\n\n"
            "node_colors = [KIND_COLORS.get(G.nodes[n]['kind'], '#999999') for n in G.nodes()]\n"
            "pos = nx.spring_layout(G, seed=42, k=1.2)\n\n"
            "fig, ax = plt.subplots(figsize=(12, 8))\n"
            "nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax, alpha=0.9)\n"
            "nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, ax=ax)\n"
            "nx.draw_networkx_edges(G, pos, ax=ax, alpha=0.5, width=1.5)\n"
            "edge_labels = {(u, v): d.get('relation', '') for u, v, d in G.edges(data=True)}\n"
            "nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, ax=ax)\n\n"
            "legend_handles = [Patch(facecolor=color, label=kind) for kind, color in KIND_COLORS.items()]\n"
            "ax.legend(handles=legend_handles, title='Node kind', loc='upper left', bbox_to_anchor=(1.02, 1))\n"
            "ax.set_title('Heterogeneous indexing graph')\n"
            "ax.axis('off')\n"
            "plt.tight_layout()\n"
            "plt.show()"
        ),
    ],
    "06_adjacency_matrix_ppr.ipynb": [
        md(
            "# Adjacency Matrix and Personalized PageRank\n\n"
            "MemGraphRAG retrieval seeds a heterogeneous graph and propagates importance with PPR:\n\n"
            "$$\\mathbf{v}^{(k+1)} = (1-\\lambda)\\mathbf{W}\\mathbf{v}^{(k)} + \\lambda\\mathbf{v}^{(0)}$$\n\n"
            "where $\\mathbf{W}$ is the row-normalized transition matrix derived from the adjacency matrix."
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "import numpy as np\n"
            "from memg_concepts.adjacency import build_adjacency_matrix\n"
            "from memg_concepts.config import DEFAULT_PDF\n"
            "from memg_concepts.pipeline import build_index\n"
            "from memg_concepts.retrieval import retrieve\n\n"
            "index = build_index(DEFAULT_PDF, max_chunks=10, schema_freq_threshold=1)\n"
            "matrices = build_adjacency_matrix(index.graph)\n"
            "print('Memory:', index.memory.summary(min_schema_freq=index.schema_freq_threshold))\n"
            "print('Graph:', index.graph.summary())\n"
            "print('Nodes:', len(matrices.node_ids))\n"
            "print('Adjacency shape:', matrices.adjacency.shape)\n"
            "print('Non-zero adjacency entries:', np.count_nonzero(matrices.adjacency))"
        ),
        code(
            "from memg_concepts.models import NodeKind\n\n"
            "df = matrices.to_dataframe()\n\n"
            "# Nodes are ordered passages first, then schemas/types/entities.\n"
            "# Passages never connect directly to other passages — only to entities via evidence edges.\n"
            "print('Passage × passage block (first 8×8) — expected all zeros:')\n"
            "display(df.iloc[:8, :8])\n\n"
            "passage_ids = [nid for nid in matrices.node_ids if index.graph.nodes[nid].kind == NodeKind.PASSAGE][:4]\n"
            "entity_ids = [nid for nid in matrices.node_ids if index.graph.nodes[nid].kind == NodeKind.ENTITY][:4]\n"
            "print('Passage × entity block — non-zero where evidence links exist:')\n"
            "df.loc[passage_ids, entity_ids]"
        ),
        md(
            "## Transition Matrix\n\n"
            "Each row of the adjacency matrix is normalized by out-degree to obtain the random-walk transition matrix $\\mathbf{W}$."
        ),
        code(
            "row_sums = matrices.transition.sum(axis=1)\n"
            "print('Row sums (should be ~1):', row_sums[:8])\n\n"
            "query = 'How does multi-head attention work?'\n"
            "evidence = retrieve(query, index.memory, index.graph, index.embedder)\n"
            "top = sorted(evidence.scores.items(), key=lambda x: x[1], reverse=True)[:10]\n"
            "for node_id, score in top:\n"
            "    label = index.graph.nodes[node_id].label\n"
            "    kind = index.graph.nodes[node_id].kind.value\n"
            "    print(f'{score:.4f} [{kind}] {node_id}: {label[:70]}')"
        ),
        md(
            "## Multi-Layer Reset Vectors\n\n"
            "MemGraphRAG seeds PPR from three query-aware layers before propagation:\n\n"
            "- **$P_{init}(p)$** — passage embedding similarity\n"
            "- **$P_{init}(e)$** — entity embedding similarity (hub-suppressed)\n"
            "- **$P_{init}(t)$** — type nodes linked to schema matches\n\n"
            "The combined reset is $\\mathbf{v}^{(0)} = \\mathrm{normalize}(P_{init}(p) + P_{init}(e) + P_{init}(t) + P_{init}(schema))$."
        ),
        code(
            "import pandas as pd\n"
            "from memg_concepts.models import NodeKind\n"
            "from memg_concepts.pagerank import normalize_reset\n"
            "from memg_concepts.retrieval import (\n"
            "    build_query_init_vectors,\n"
            "    propagation_history_table,\n"
            "    run_lambda_sweep,\n"
            "    summarize_scores_by_kind,\n"
            ")\n\n"
            "query = 'How does multi-head attention work?'\n"
            "inits = build_query_init_vectors(query, index.memory, index.graph, index.embedder, matrices)\n\n"
            "entity_count = sum(1 for node in index.graph.nodes.values() if node.kind == NodeKind.ENTITY)\n"
            "print(f'Entity nodes in graph: {entity_count}')\n"
            "if entity_count == 0:\n"
            "    print(\n"
            "        'P_init(e) is empty because the graph has no entity nodes. '\n"
            "        'That happens when active_facts is 0 — usually LLM extraction failed or '\n"
            "        'no facts survived conflict resolution. Re-run the build_index cell and '\n"
            "        'check Memory summary above.'\n"
            "    )\n\n\n"
            "def init_table(layer, kind: NodeKind) -> pd.DataFrame:\n"
            "    rows = []\n"
            "    for node_id, idx in matrices.node_index().items():\n"
            "        node = index.graph.nodes[node_id]\n"
            "        if node.kind != kind:\n"
            "            continue\n"
            "        score = float(layer[idx])\n"
            "        if score <= 0:\n"
            "            continue\n"
            "        rows.append({'node_id': node_id, 'label': node.label, 'score': score})\n"
            "    if not rows:\n"
            "        return pd.DataFrame(columns=['node_id', 'label', 'score'])\n"
            "    return pd.DataFrame(rows).sort_values('score', ascending=False).reset_index(drop=True)\n\n\n"
            "print('P_init(p) — passages')\n"
            "display(init_table(inits.passage, NodeKind.PASSAGE))\n"
            "print('P_init(e) — entities')\n"
            "display(init_table(inits.entity, NodeKind.ENTITY))\n"
            "print('P_init(t) — types')\n"
            "display(init_table(inits.type, NodeKind.TYPE))\n\n"
            "v0 = normalize_reset(inits.combined)\n"
            "print('Combined v^(0) mass by kind:', summarize_scores_by_kind(v0, index.graph, inits.node_ids))"
        ),
        md(
            "## Lambda Sweep — 10 Propagation Steps\n\n"
            "Iterate $\\mathbf{v}^{(k+1)} = (1-\\lambda)\\mathbf{W}\\mathbf{v}^{(k)} + \\lambda\\mathbf{v}^{(0)}$ "
            "for $\\lambda \\in \\{0.1, 0.3, 0.5, 0.7, 0.9\\}$ and track how probability mass flows across "
            "passages, entities, types, and schemas."
        ),
        code(
            "lambdas = (0.1, 0.3, 0.5, 0.7, 0.9)\n"
            "num_steps = 10\n"
            "sweeps = run_lambda_sweep(matrices, inits.combined, lambdas=lambdas, num_steps=num_steps)\n\n"
            "mass_rows = []\n"
            "for damping, history in sweeps.items():\n"
            "    for step, scores in enumerate(history):\n"
            "        totals = summarize_scores_by_kind(scores, index.graph, inits.node_ids)\n"
            "        mass_rows.append({'lambda': damping, 'step': step, **totals})\n"
            "mass_df = pd.DataFrame(mass_rows)\n\n"
            "fig, axes = plt.subplots(1, len(lambdas), figsize=(18, 4), sharey=True)\n"
            "for ax, damping in zip(axes, lambdas):\n"
            "    subset = mass_df[mass_df['lambda'] == damping]\n"
            "    for kind in ['passage', 'entity', 'type', 'schema']:\n"
            "        if kind in subset.columns:\n"
            "            ax.plot(subset['step'], subset[kind], marker='o', label=kind)\n"
            "    ax.set_title(f'λ={damping}')\n"
            "    ax.set_xlabel('step')\n"
            "    ax.legend(fontsize=8)\n"
            "axes[0].set_ylabel('probability mass')\n"
            "plt.suptitle(f'PPR mass flow by node kind ({num_steps} steps)')\n"
            "plt.tight_layout()\n\n"
            "mass_df"
        ),
        code(
            "# Top nodes after 10 steps at λ=0.5 (passages, entities, types)\n"
            "propagation_history_table(\n"
            "    sweeps[0.5],\n"
            "    index.graph,\n"
            "    inits.node_ids,\n"
            "    kinds=(NodeKind.PASSAGE, NodeKind.ENTITY, NodeKind.TYPE),\n"
            ").sort_values('step_10', ascending=False).head(20)"
        ),
        md(
            "PPR spreads query relevance along fact, schema, and evidence edges so globally important passages rise even when direct embedding similarity is weak."
        ),
    ],
    "07_memory_guided_qa.ipynb": [
        md(
            "# Memory-Guided Question Answering\n\n"
            "The final step combines retrieved passages and entities into an LLM prompt."
        ),
        code(
            "%run supportvectors-common.ipynb\n\n"
            "from memg_concepts.config import DEFAULT_PDF\n"
            "from memg_concepts.pipeline import build_index, query_index\n\n"
            "index = build_index(DEFAULT_PDF, max_chunks=12)\n"
            "questions = [\n"
            "    'What problem does the Transformer solve compared to recurrent models?',\n"
            "    'What are the main components of multi-head attention?',\n"
            "    'How is positional information injected in the Transformer?',\n"
            "]\n"
            "questions"
        ),
        code(
            "for question in questions:\n"
            "    evidence, result = query_index(index, question)\n"
            "    print('=' * 80)\n"
            "    print('Q:', question)\n"
            "    print('Passages:', result.passage_ids)\n"
            "    print('A:', result.answer)"
        ),
    ],
}


def main() -> None:
    NOTEBOOK_DIR.mkdir(parents=True, exist_ok=True)
    for name, cells in NOTEBOOKS.items():
        notebook = {
            "cells": cells,
            "metadata": {
                "kernelspec": {
                    "display_name": "Python 3",
                    "language": "python",
                    "name": "python3",
                },
                "language_info": {"name": "python", "pygments_lexer": "ipython3"},
            },
            "nbformat": 4,
            "nbformat_minor": 5,
        }
        path = NOTEBOOK_DIR / name
        path.write_text(json.dumps(notebook, indent=1))
        print("wrote", path)


if __name__ == "__main__":
    main()
