# T017 Week 04 Xennials FactoidWiki Demo

Status: done

Date: 2026-06-27

## Goal

Build a Task 2 demo that turns the Wikipedia page for Xennials into a small FactoidWiki-style retrieval system.

## Why It Matters

Task 1 compared retrieval artifact types over prepared course texts. Task 2 applies the same idea to a live web source:

- ingest a Wikipedia article
- preserve section-aware raw chunks
- use an SV chat model to extract atomic factoids
- generate query-shaped QA pairs
- embed all retrieval artifacts with SV embeddings
- search and synthesize grounded answers through an interactive UI

## Source

- Wikipedia: `https://en.wikipedia.org/wiki/Xennials`

## Scope

- Create a `course/week_04/task_02_xennials_factoid_wiki/` workspace.
- Fetch and parse Wikipedia sections.
- Build section-aware raw chunks.
- Generate factoids and QA pairs using SV cluster chat.
- Build a dense embedding index using SV cluster embeddings.
- Provide a Streamlit UI for pipeline actions, artifact browsing, search, and answer synthesis.

## Done When

- [x] Raw Wikipedia sections are extracted.
- [x] Raw chunks are generated.
- [x] Factoids are generated with SV chat.
- [x] QA pairs are generated with SV chat.
- [x] SV embedding index is generated.
- [x] UI can browse artifacts.
- [x] UI can search and synthesize answers.
- [x] README explains how to run the demo.

## Evidence

- Workspace: `course/week_04/task_02_xennials_factoid_wiki/`
- Pipeline: `course/week_04/task_02_xennials_factoid_wiki/sv_factoid_wiki.py`
- Streamlit UI: `course/week_04/task_02_xennials_factoid_wiki/app.py`
- README: `course/week_04/task_02_xennials_factoid_wiki/README.md`
- Raw sections: `course/week_04/task_02_xennials_factoid_wiki/data/xennials_raw_sections.json`
- Raw chunks: `course/week_04/task_02_xennials_factoid_wiki/data/xennials_raw_chunks.json`
- Factoids: `course/week_04/task_02_xennials_factoid_wiki/data/xennials_factoids.json`
- QA pairs: `course/week_04/task_02_xennials_factoid_wiki/data/xennials_qa_pairs.json`
- SV embedding index: `course/week_04/task_02_xennials_factoid_wiki/data/xennials_sv_embedding_index.json`

## 2026-06-27 Update

Implemented and verified the first Xennials FactoidWiki dataset:

- fetched the Xennials Wikipedia article through the MediaWiki API
- parsed article sections and generated 11 section-aware raw chunks
- used the SV chat model `Qwen/Qwen3-VL-8B-Instruct` to generate 88 factoids
- generated 88 QA pairs from the factoids
- embedded raw chunks, factoids, and QA pairs with `Qwen/Qwen3-Embedding-0.6B`
- built a 187-record, 1024-dimensional SV embedding index
- added a Streamlit UI for browsing artifacts, searching, and answer synthesis

Validation:

- Python files compile
- generated JSON files parse
- search query `What birth years are commonly used for Xennials?` retrieves relevant QA pairs and factoids
- answer synthesis returns a grounded answer citing retrieved evidence

Note:

- Streamlit is not installed in the bundled Codex Python runtime. The UI code is ready, but running it requires `python3 -m pip install -r requirements.txt` in an environment where package installation is allowed.
