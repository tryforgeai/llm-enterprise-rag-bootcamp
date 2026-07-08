# T016 Week 04 Abstractive Summary Retrieval

Status: done

Date: 2026-06-27

## Goal

Build a Week 04 experiment that compares raw chunks, abstractive summaries, propositions, and QA pairs as retrieval artifacts.

## Why It Matters

Week 04 shifts from naive chunking toward derived artifacts. The goal is to learn by experience how different index objects answer different kinds of questions:

- raw chunks preserve local evidence
- propositions preserve atomic, self-contained facts
- QA pairs create query-shaped retrieval targets
- abstractive summaries create high-level conceptual retrieval targets

## Sources

- `course/week_04/prml_chapter_02_probability_distributions.md`
- `course/week_04/prml_chapter_03_linear_models_for_regression.md`
- `course/week_04/dense_x_retrieval_granularity.md`

## Scope

- Extract source texts into Markdown with page boundaries.
- Create a source manifest.
- Generate or draft derived artifacts:
  - raw chunks
  - abstractive summaries
  - propositions
  - QA pairs
- Create a local JSON index first.
- Add SV cluster embeddings and/or Qdrant only after the local-file version is understandable.
- Build a small UI to compare retrieval behavior across artifact types.

## Done When

- [x] PRML Chapter 2 text is extracted.
- [x] PRML Chapter 3 text is extracted.
- [x] Dense-X paper text is extracted.
- [x] Source manifest exists.
- [x] Abstractive summaries are created.
- [x] Propositions are created for the Dense-X paper.
- [x] QA pairs are created for all selected sources.
- [x] Local embedding/index artifact exists.
- [x] UI compares raw chunk, QA-pair, proposition, and summary retrieval.
- [x] At least five eval questions compare artifact behavior.

## Evidence

- Chapter selection: `course/week_04/prml-chapter-selection.md`
- Dense-X extracted Markdown: `course/week_04/dense_x_retrieval_granularity.md`
- Source manifest: `course/week_04/artifacts/source_manifest.json`
- Abstractive summaries: `course/week_04/artifacts/abstractive_summaries.json`
- Dense-X propositions: `course/week_04/artifacts/dense_x_propositions.json`
- QA pairs: `course/week_04/artifacts/qa_pairs.json`
- Representative raw chunks: `course/week_04/artifacts/raw_chunks_sample.json`
- Local retrieval index: `course/week_04/artifacts/local_retrieval_index.json`
- SV embedding index: `course/week_04/artifacts/sv_embedding_index.json`
- Eval questions: `course/week_04/artifacts/eval_questions.json`
- Retrieval comparison UI: `course/week_04/retrieval_artifact_comparison/index.html`
- Real RAG server: `course/week_04/retrieval_artifact_comparison/server.py`
- Real RAG README: `course/week_04/retrieval_artifact_comparison/README.md`
- Current QA-pair mini demo: `course/week_04/qa_pair_embedding_demo/index.html`

## 2026-06-27 Update

Created the source foundation:

- extracted PRML Chapter 2 into `course/week_04/prml_chapter_02_probability_distributions.md`
- extracted PRML Chapter 3 into `course/week_04/prml_chapter_03_linear_models_for_regression.md`
- extracted Dense-X Retrieval into `course/week_04/dense_x_retrieval_granularity.md`
- created `course/week_04/artifacts/source_manifest.json`
- kept local JSON/file-based storage as the first implementation target before Qdrant

## 2026-06-27 Update 2

Created the first runnable local artifact-comparison layer:

- drafted abstractive summaries for PRML Chapter 2, PRML Chapter 3, and Dense-X
- drafted proposition-level Dense-X factoids
- drafted QA-pair retrieval artifacts across all selected sources
- added representative raw chunks for comparison
- added `course/week_04/scripts/build_local_retrieval_index.py`
- generated a 37-record local TF-IDF/cosine index
- added `course/week_04/retrieval_artifact_comparison/index.html`

Validation:

- JSON artifacts parse with `python3 -m json.tool`
- local index rebuilds successfully
- UI JavaScript passes bundled Node syntax check

## 2026-06-27 Update 3

Added `course/week_04/artifacts/eval_questions.json` with seven retrieval eval questions. Each eval item names the target source, the expected artifact behavior, and expected matching records. This completes the first local-file version of the experiment; SV cluster embeddings and Qdrant remain a future upgrade path rather than a blocker.

## 2026-06-27 Update 4

Upgraded the retrieval comparison page into a real embedding-backed RAG demo:

- added `course/week_04/retrieval_artifact_comparison/server.py`
- added UI controls to build an SV embedding index and query it
- embedded 37 retrieval artifacts with `Qwen/Qwen3-Embedding-0.6B` through the SV cluster endpoint
- wrote the 1024-dimensional dense embedding index to `course/week_04/artifacts/sv_embedding_index.json`
- verified real query embedding/search with: `What is a proposition in Dense-X?`

Observed top result:

- `qa_dense_x_002` scored `0.8703`
- this demonstrates the expected QA-pair behavior: query-shaped artifacts can rank very strongly when the user question matches their generated question form

The demo currently returns extractive evidence. LLM synthesis is intentionally left as the next layer because it requires an explicit API-key/provider decision.

## 2026-06-27 Update 5

Converted the demo to SV-only RAG:

- removed the TF-IDF/browser fallback from the UI
- added SV chat-backed QA-pair generation through `/api/generate-qa`
- generated 12 QA pairs with `openai/gpt-oss-20b`
- saved generated QA pairs to `course/week_04/artifacts/generated_qa_pairs_sv.json`
- rebuilt the SV embedding index with 49 records
- added SV chat answer synthesis through `/api/answer`

Verified full pipeline:

```text
raw chunks -> SV chat QA generation -> SV embedding index -> SV query embedding -> cosine top-k -> SV chat grounded answer
```

Test query:

```text
What is the goal of proposition-level retrieval?
```

Observed:

- top record: `svqa_raw_dense_x_002_2`
- score: `0.8795`
- generated answer: proposition-level retrieval removes unnecessary context while keeping facts complete enough for a downstream answer generator
