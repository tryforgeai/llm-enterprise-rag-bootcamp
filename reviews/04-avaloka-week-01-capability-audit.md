# Avaloka AI Week 01 Capability Audit

Status: Completed

Date: 2026-06-06

Avaloka repository reviewed:

`/Users/rosso.han/Documents/Obsidian Vault/Projects/Avaloka AI`

## Executive Verdict

Avaloka already implements much of the course's **agent and safety architecture**, but not most of its advanced **enterprise retrieval infrastructure**.

The strongest existing capabilities are:

1. risk-aware routing before generation
2. structured response planning and post-generation guardian review
3. sparse, evidence-backed care memory with lifecycle controls
4. developer diagnostics, prompt versioning, and behavior-focused evals
5. deliberate architecture escalation instead of premature complexity

The largest evidence-backed gaps are:

1. no active embedding, vector, hybrid, or reranking pipeline
2. no formal retrieval metrics such as Recall@k, MRR, MAP, or NDCG
3. no assertion-to-evidence grounding verifier for final responses
4. no RAPTOR, GraphRAG, or semantic response cache
5. no production server-side memory retrieval or user-facing memory controls

The right next move is not GraphRAG or fine-tuning. It is to benchmark the existing deterministic Memory Reader V0 on a fixed relevance dataset. Only then should Avaloka compare embeddings, hybrid retrieval, or reranking against the current baseline.

## Scope And Evidence Boundary

This audit compares the active Avaloka R1 implementation against the Week 01 course material. Archived Avaloka plans mentioning ChromaDB, BGE embeddings, or a vector store are historical proposals, not current capability.

The active Avaloka roadmap explicitly defers:

- full large-corpus RAG
- production graph databases
- learned graph readers
- fine-tuning

Evidence came from active product, research, engineering, prompt, runtime, test, and eval files. The audit does not treat a design document as implemented behavior unless corresponding runtime code exists.

## Capability Matrix

Status meanings:

- **existing**: working behavior is present in the active code path
- **partial**: the core idea exists, but production depth, measurement, or course-specific technique is incomplete
- **missing**: no active implementation was found
- **deferred**: intentionally outside the current R1 scope

| Course capability | Status | Avaloka evidence | Trace and eval evidence | Main gap or opportunity |
| --- | --- | --- | --- | --- |
| Agent-first loop | existing | `App.tsx`, `llm-shadow-server.mjs`, prompt registry, memory writer/reader/guardian | Per-message crisis, Baifa, compassion, guardian, memory, model, latency, and feedback fields | No single normalized end-to-end trace object covering every stage |
| Intent and risk classification | existing | local crisis gate, LLM crisis classifier, Dukkha Mapper, Baifa Mapper | Crisis and mapping fixtures; developer panels expose decisions | Classifiers are domain-specific and some local rules remain keyword-based |
| Decision and response planning | existing | Compassion OS planner chooses moves, stance, avoid list, and response hint | Compassion eval cases and developer diagnostics | No explicit general agent action taxonomy such as ask, retrieve again, abstain, or tool use |
| Request guardrails | partial | local crisis gate, LLM crisis classification, request limits, safe routing, prompt-injection tests | Crisis and safety evals exist | Not the course's full multi-gate request pipeline; auth, tenant, permission, and retrieval-scope gates are not productionized |
| Helpful, Harmless, Honest behavior | existing | quality checklist, Precepts Guardian, crisis fallback, response guardian | Guardian severity and forbidden-term checks | HHH is implemented as product policy, not yet measured as a stable three-axis scorecard |
| Response guardian and repair | existing | response generation -> guardian -> repair -> guardian -> safe fallback | Guardian result, severity, notes, repair attempt, and fallback are traced | Guardian can use the same model family as the generator and is not an independent evidence judge |
| Sparse evidence-backed memory | existing | Memory Writer, Memory Guardian, Care Card, evidence IDs, delete and supersede lifecycle | Writer, guardian, end-to-end, response, storage, and inspector coverage | Developer/localStorage research path only; no durable production review workflow |
| Scoped memory retrieval | partial | deterministic reader filters by tags, confidence, active status, evidence, staleness, and risk priority; result limit is five | Latest retrieved memory IDs appear in diagnostics and export | Client performs developer-mode retrieval and server trusts supplied facts; no server-side authorization boundary |
| Embeddings and vector retrieval | missing | Only future research and archived plans mention embeddings | No active embedding benchmark | Establish measured need before implementing |
| Chunking and ingestion | partial | Protected knowledge and content-ingestion checks exist | `content:check` validates required content and eval artifacts | No active runtime chunking strategy, chunk index, or chunk-quality eval |
| Sparse plus dense hybrid retrieval | missing | No active BM25, SPLADE, vector lane, fusion, or reranker | None | Consider only after the deterministic reader baseline exposes misses |
| Reranking cascade | missing | Deterministic score uses tag overlap, risk boost, confidence, occurrence, and recency | Unit tests cover ordering behavior | No learned cross-encoder or staged cost-aware reranking |
| Query transformation | partial | Dukkha, Baifa, and Compassion stages transform a raw message into domain representations | Their outputs are traced and evaluated | They transform response intent, not retrieval queries; no rewrite, expansion, decomposition, or HyDE |
| Derivative artifacts | partial | Care Cards distill conversations into sparse facts; derived knowledge documents and prompt-ready artifacts exist | Evidence IDs and memory kinds are inspectable | No systematic multiple representations such as generated Q&A, search rewrites, and hierarchical summaries |
| SAGE precise retrieval, arXiv 2503.01713 | missing | Avaloka uses a different SAGE-style memory research direction | No SAGE precise-retrieval experiment | Treat the two SAGE names as separate systems; compare only through explicit evals |
| RAPTOR | missing | No hierarchical summary tree or multi-level traversal | None | Add only if broad questions fail because one retrieval resolution is insufficient |
| GraphRAG | missing | Graph memory is discussed for future R2; no active entity/community graph runtime | None | Graph-shaped memory is not the same as GraphRAG; defer until relationship failures are observed |
| Scale-driven architecture | existing | R1 uses local JSON/localStorage, deterministic retrieval, and explicitly defers graph and fine-tuning | Roadmap and gap report define promotion conditions | Component-level cost and quality deltas are not yet collected consistently |
| Shapley-style component ablation | partial | Memory response eval compares with-memory and without-memory behavior | A/B structure exists for memory | No generalized ablation harness across router, retrieval, planner, guardian, and cache |
| Semantic response cache | missing | Prompt runtime has an exact in-process prompt-file cache only | No semantic hit, false-hit, TTL, or invalidation eval | Prompt caching must not be mistaken for semantic answer caching |
| Response grounding | partial | Memory candidates require evidence IDs; prompts constrain memory use; guardian checks policy and tone | Retrieved facts and memory IDs are visible to developers | Final claims are not split into assertions and linked to evidence; no entailment, contradiction, freshness, or citation verifier |
| Trace and observability | partial | Developer panels and export include stage outputs, model, latency, memory and guardian details | Memory Inspector summarizes store, writer, retrieval, lifecycle, and eval commands | Trace schema is distributed across message fields rather than one versioned pipeline trace |
| Evaluation harness | partial | Broad fixture coverage, live eval scripts, content gates, unit tests, stage attribution | Existing suites cover crisis, Baifa, compassion, guardian, memory, and responses | Mostly domain rules and heuristics; no formal retrieval or RAG answer-quality metrics and no persisted benchmark history |
| Text-to-SQL | missing | No active structured analytics query agent | None | Low priority for R1; useful later for read-only trace and eval analysis |
| Fine-tuning | deferred | Roadmap explicitly keeps fine-tuning out of R1 | None | Consider only after prompt, retrieval, grounding, and eval evidence show a persistent model behavior gap |

## Existing Strengths

### 1. Safety Is A Pipeline, Not A Prompt

Avaloka does not rely on one system prompt to handle risk. The active flow includes:

```text
local crisis detection
-> LLM crisis classification
-> domain mapping
-> compassion planning
-> response generation
-> guardian review
-> repair
-> second guardian review
-> safe fallback
```

That is already close to the course's request-guardrail and response-grounding mindset, even though the evidence verifier is incomplete.

### 2. Memory Has Writer/Reader Separation

The current memory design separates:

- candidate extraction
- evidence and privacy guardian checks
- Care Card storage
- deterministic retrieval
- bounded prompt injection
- lifecycle operations

This is materially more mature than simply appending chat history to a prompt.

### 3. Architecture Complexity Is Being Earned

Avaloka's active roadmap deliberately uses a small local store and deterministic reader before graph databases, embeddings, learned readers, or fine-tuning. This matches the course principle that scale and measured failure should decide architecture.

### 4. Behavior Is Observable

Developer mode exposes the outputs of crisis classification, Baifa mapping, compassion planning, guardian review, memory writing, memory retrieval, model choice, and latency. The Memory Inspector also reports lifecycle and retrieval state.

### 5. Evals Exist Before Advanced Retrieval

Avaloka already has fixed cases for safety, compassion, memory, and response behavior. That gives future retrieval changes a real comparison baseline instead of a demo-only success criterion.

## Evidence Gaps And Risks

### 1. Retrieval Quality Is Not Quantified

The deterministic reader has sensible rules, but there is no labeled relevance set and no Recall@k, MRR, MAP, or NDCG result. We therefore cannot say whether embeddings or reranking are needed, or whether they improve the current system.

### 2. Grounding Stops Before Final Claims

Memory records carry evidence IDs, but the final answer does not produce an assertion-evidence graph. A fluent response can still make an unsupported health, personal-history, or practice claim without a claim-level verifier catching it.

### 3. Production Trust Boundaries Are Incomplete

Developer-mode retrieval happens in the client, and the server accepts `retrievedCareFacts`. This is adequate for an R1 local experiment, but not for production authorization, provenance, or tamper resistance.

### 4. Guardian Logic Can Drift

Memory guardian logic exists in both server JavaScript and app TypeScript. Thresholds differ, and the documented `revise` state is not implemented consistently. Shared fixtures reduce risk, but one authoritative contract is still missing.

### 5. Eval Depth Is Uneven

Avaloka has many fixtures, but some verdicts rely on keywords and heuristics. There is no persisted run history, calibrated human rubric, independent judge benchmark, or formal retrieval measurement.

### 6. Documentation Slightly Lags Code

The active memory gap report contains a few stale subsection statements about missing inspector or lifecycle controls even though newer code and commits include them. Runtime evidence should remain authoritative, and the Avaloka report should be refreshed separately.

## SAGE Naming Boundary

Two different systems currently share the name SAGE:

| Name | Purpose |
| --- | --- |
| Avaloka SAGE-style memory | sparse long-term companion memory with writer, guardian, store, reader, and lifecycle |
| Course paper SAGE, arXiv 2503.01713 | precise retrieval for conventional RAG through better segmentation, selection, and feedback |

Avaloka has meaningful SAGE-style memory work, but it has not implemented the course paper's precise-retrieval pipeline. The overlap is conceptual: both try to preserve useful evidence and reduce noisy context. Their architecture and eval targets are different.

## Recommended Next Experiment

### Benchmark Memory Reader V0 Before Adding Embeddings

Create a fixed dataset of at least 30 Avaloka memory-retrieval queries containing:

- expected relevant memory IDs
- hard negatives with similar wording but different care implications
- no-match cases
- stale-memory cases
- safety-priority cases
- tone-preference and avoid-response cases

Run the current deterministic reader and record:

- Recall@5
- MRR
- NDCG@5
- unsafe or private retrieval count
- stale retrieval count
- no-match precision
- latency

Then classify failures:

```text
missing tags
-> alias or query-transformation problem

semantic paraphrase miss
-> embedding candidate

correct candidate ranked too low
-> reranking candidate

too much irrelevant context
-> selection or threshold problem

relationship or multi-hop miss
-> future graph candidate
```

Only compare an embedding or hybrid reader after this baseline exists. Promote the new component only if it improves the fixed eval without weakening privacy, safety, latency, or debuggability.

## Validation Performed

- Active Avaloka source, product, research, engineering, prompt, test, and eval files were inspected.
- `npm run content:check` passed on 2026-06-06.
- The full Vitest suite could not be rerun because Vitest needed to write a temporary file inside the Avaloka repository, which is outside the current workspace's writable boundary. The required approval was unavailable during this run.

