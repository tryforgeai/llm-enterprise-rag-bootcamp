# Week 03 Summary — Chunking as a Representation Decision

**Date:** 2026-06-20 · **Source:** `course/week_03/week-3-summer-lesson-plan.pdf`, in-class lab, and Week 03 experiments

---

## TL;DR

Chunking is not preprocessing. It is the first — and effectively irreversible — decision about *what counts as an independently retrievable unit of thought* in our corpus. Everything downstream (embeddings, reranking, prompts, bigger models) can only patch over a bad first projection.

The practical takeaway for us: stop treating chunk size as a tuning knob and start running a **representation tournament** — put fixed / semantic / contextual / late-chunked / page-image variants on the same query set and let retrieval metrics pick the winner.

---

## Core concepts

| Concept | What it means in practice |
| --- | --- |
| **Chunking as ontology** | A chunk boundary declares "this span is one retrievable idea." Get it wrong and no reranker saves you. |
| **First projection is lossy** | Text → boundary → embedding compresses structure into a fixed-dim vector. You cannot recover what the boundary cut. |
| **Mixing principle** | Two orthogonal ideas in one chunk average into a vector that represents neither. Query matches are "sort of relevant" to everything. |
| **Small-chunk amnesia** | Small chunks are purer but drop referents, conditions, definitions, negation, and safety scope. |
| **Centroid delusion** | Large heterogeneous chunks drift toward the center of the semantic space — moderately similar to many queries, genuinely answering none. Popular in top-k, useless in the answer. |
| **Query–chunk asymmetry** | Queries are short and sharp; chunks are long and diffuse. Matching them biases toward internally coherent chunks over actually-answering ones. |
| **Contextual chunking** | Repairs context in *text space*: chunk small, then prepend minimal necessary context. Readable and auditable, but costs an LLM call per chunk. |
| **Late chunking** | Repairs context in *latent space*: encode the whole document first, then pool token spans into chunk vectors. Elegant and cheap, but less interpretable. |
| **Page-image retrieval** | Don't flatten a 2D page into 1D text. ColPali/ColVision keep multiple patch vectors per page and use ColBERT-style MaxSim against query tokens. |

### What chunking actually breaks

Five failure modes worth naming in code review and in postmortems:

1. **Endophora** — anaphora/cataphora split across chunks. The chunk reads fluently but the referent is gone; the model fills the gap by guessing.
2. **Discourse structure** — retrieving the claim without the `however`, the concession, or the qualifier can invert the source's conclusion. Highest risk in papers, contracts, clinical results, and risk disclosures.
3. **Negation / scope failure** — `no significant evidence` loses `in patients under 65`; `if debt-to-income exceeds 43%` loses its condition. This is the dangerous one: no error signal, just a confident over-generalized answer.
4. **Definition–use chain** — §2.1 defines "Covered Losses," §7.4 uses it. Split them and the model sees ordinary English instead of a binding contractual term. This is why smaller is not automatically better.
5. **Bridging inference & genre blindness** — implicit scene relations get cut, and one 512-token policy gets applied indiscriminately to contracts, papers, fiction, and financial PDFs that each carry meaning differently.

**On the 512-token default:** it is a convenient engineering baseline, roughly one page (~300–400 tokens/page), not a semantic boundary. Treat it as the control arm, never as the conclusion.

---

## Experiments run this week

### 1. Punctuation sensitivity — `course/week_03/punctuation_embedding_test.py`

Tested whether embedding models see punctuation-controlled syntax or only lexical overlap, on three sentences:

```
1. Eats, shoots, and leaves.
2. Eats shoots and leaves.
3. A panda eats bamboo shoots and leaves.
```

| Model | cos(1,2) | cos(1,3) | cos(2,3) |
| --- | ---: | ---: | ---: |
| BERT (anisotropic) | 0.9041 | 0.7610 | 0.7908 |
| MiniLM (isotropic) | 0.9231 | 0.4605 | 0.5065 |

Split into two questions:

- `cos(2,3) > cos(1,3)` — does the model know the panda sentence is closer to the comma-free one? **Both pass.**
- `cos(2,3) > cos(1,2)` — does syntax beat lexical overlap? **Both fail.**

BERT's uniformly high scores also show the anisotropy/cone effect from Week 02. The finding is not "embeddings are broken" — it's a sharper failure: *models see topic and lexical relation but not punctuation-controlled syntax.* For legal, medical, regulatory, and safety-rule content, `not / unless / except / however / if / only when / , / ;` can all flip the meaning, and the embedding may not notice.

### 2. Visual vs. text retrieval on PRML — `course/week_03/week-03-in-person-lab/`

Two pipelines over Bishop's PRML, compared with `compare.py`:

| | Team 1 (Visual) | Team 2 (Text) |
| --- | --- | --- |
| Input | Page rendered to PNG @150 DPI | Parsed text, 512-char chunks / 50 overlap |
| Model | CLIP + SigLIP2 | sentence-transformers (MiniLM) |
| Sees | Text, figures, tables, layout, equations | Plain text only |
| Index | FAISS `IndexFlatIP` on L2-normalized vectors (= cosine) | same |

Cross-modal retrieval means a text query hits the image index directly — no OCR step. The asymmetry the overlap analysis surfaces: **equation-heavy and figure-only pages produce near-empty text chunks and barely appear in the text index at all.** Queries like "Gaussian mixture model diagram" or "hidden Markov model trellis" are effectively invisible to the text pipeline.

Also built standalone `path1_page_image_qa.py` (page-image retrieval + vision answer), `path2_text_chunk_qa.py` (text chunk retrieval + text answer), `qa_compare_app.py` (side-by-side), and `pdf_to_textbook.py` (PRML → Markdown textbook baseline). Page-image rendering verified continuous with no missing pages.

### 3. Contextual chunking baseline — `course/week_03/capstone_contextual_chunks/`

Capstone PDF (213 pages, 203 non-empty, ~335K chars) → 266 chunks at 1800 chars / 250 overlap, emitted in two variants:

- `regular_chunks.jsonl` — plain chunks
- `contextual_chunks.jsonl` — each chunk carries a context prefix with document title, page range, section, and local terms

The context prefix is generated **deterministically and locally** — no external API calls. This gives us a cheap contextual-chunking arm for the tournament without per-chunk LLM cost.

> Note: `contextual_chunk_pdf.py` defaults to `data/rag-capstone-projects.pdf`, which is deliberately not committed. Pass `--pdf` for other sources. Offline unit tests: `uv sync --frozen && uv run pytest` (fake model clients, no keys needed).

### 4. Representation tournament

These three representations were put into a measured competition on PRML — 27 queries, page-level gold, Recall@k / MRR / NDCG@k / error types. Semantic chunking wins on evidence per unit read; fixed chunking loses at every window size, and loses on ranking rather than on finding. The result worth reading is an ablation nobody was aiming for: the contextual arm's entire advantage disappears when text extraction is left unrepaired.

Written up separately in **`week-03-tournament-for-team.md`**; the artifact is at `evals/week03-representation-tournament/`.

---

## "RAG is dead" — what actually died

The Chroma and Turbopuffer talks are not arguing retrieval is obsolete. What failed is:

```
fixed chunk → vector top-k → stuff into prompt → hope
```

What did not fail: retrieval, evidence, context engineering, agentic search, grounding, eval. The direction is agentic retrieval — the agent decides what it needs, mixes vector / full-text / regex / metadata filters, searches over multiple turns, prunes noise, and hands clean evidence to a reasoning model.

Useful framing: **embeddings are cached compute.** Pre-understanding and indexing a corpus pays off only if that corpus gets queried repeatedly.

---

## Proposed default pipeline

Not a recipe — a candidate set to compete:

```
respect document markup / headings
→ semantic hierarchical chunking
→ contextual chunking where budget allows
→ late chunking before embedding
→ persist section, position, parentage, source metadata
→ let eval pick the winner
```

Every new corpus should get its own tournament:

```
corpus sample → held-out queries → gold evidence
→ competing representations
→ retrieval metrics + latency/cost + safety checks
→ winner or hybrid
```

**Metrics:** Recall@k, MRR, NDCG@k, hard-negative rate, scope-inversion error, definition-orphan error, visual-table retrieval accuracy, answer grounding, latency/cost, safety/privacy leakage.

**When page-image retrieval is worth it:** financial reports, scientific PDFs, scans, textbooks with tables/figures/equations, anything where layout carries meaning. **When it isn't:** character-exact matching, long-range cross-page reasoning, cheap large-scale indexing, plain prose. Usually the answer is a hybrid index, decided by evidence rather than argument.

---

## Implications for Avaloka

Default chunking is not safe for Care Cards and wisdom material. Different material types need different strategies:

| Material | Likely strategy |
| --- | --- |
| Care Card | Small but *complete* atomic memory — preserve permission, lifecycle, risk scope |
| Wisdom principle | Semantic chunk + context restoration, to avoid quoting out of context |
| Baifa / mind-state notes | Preserve definition–use chains and counterexamples |
| Eval failure records | Split by failure mode and decision point |
| Lecture PDFs, tables, scans | Consider page-image retrieval or a hybrid index |

**The headline risk:** chunking can strip the safety boundary and the gentle framing off a factual fragment.

```
Original:  When user is stable and not in acute distress, user likes gentle reminders.
Bad chunk: User likes gentle reminders.
```

The second looks clean and is dangerous — it lost `not in acute distress`. Our working definition:

```
small and complete = fact + referent + applicable condition
                   + prohibited condition + permission scope + source
```

Minimum chunk schema for Avaloka retrieval: source id, memory type, permission scope, risk scope, lifecycle status, created/updated time, related user intent, parent context, safety qualifiers, exact quoted evidence where needed.

---

## Open questions for the team

1. For mostly-text enterprise documents with a few tables, what's the minimum viable hybrid text + page-image experiment?
2. For permission- and safety-scoped memory, should chunk metadata participate in embedding, filtering, reranking — or only in final filtering?
3. How do we handle late chunking's max-context limit on long documents? Section-local late chunking first?
4. If contextual chunking uses an LLM to restore context, how do we evaluate that it didn't introduce interpretation absent from the source?
5. Should tournament gold evidence be annotated at chunk, page, or source-span level?

---

## Where this sits in the arc

```
Week 01 — the RAG pipeline end to end
Week 02 — why vector space works at all
Week 03 — how the source document gets cut, or preserved, before it enters that space
```
