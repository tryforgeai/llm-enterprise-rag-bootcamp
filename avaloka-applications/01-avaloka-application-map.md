# Avaloka Application Map

This document maps bootcamp concepts to Avaloka AI.

## Current Assessment

Avaloka already appears to practice many of the course's core ideas, even when it does not use the newest implementation techniques:

- intent, emotional-state, and risk-aware routing
- scoped use of memory and wisdom
- bounded next-step decisions
- guardian review
- safety and privacy boundaries
- traces and eval-oriented thinking
- Helpful, Harmless, and Honest response goals

The course should therefore be used to name, instrument, test, and selectively upgrade existing capability rather than rebuild Avaloka from zero.

Full evidence-based review:

- [Avaloka AI Week 01 Capability Audit](../reviews/04-avaloka-week-01-capability-audit.md)

Current implementation summary:

| Area | Assessment |
| --- | --- |
| agent routing, crisis handling, planning, guardian | existing and comparatively strong |
| sparse care memory, lifecycle, bounded retrieval | existing or partial in developer mode |
| developer trace and behavior evals | existing, but not normalized into one trace schema |
| embeddings, vector search, hybrid retrieval, reranking | missing from the active implementation |
| claim-level response grounding | partial |
| RAPTOR, GraphRAG, semantic response cache | missing and intentionally deferred |
| formal retrieval metrics | missing; selected as the next experiment |

Important naming boundary: Avaloka's SAGE-style companion memory is not the same system as the course paper [SAGE: A Framework of Precise Retrieval for RAG](https://arxiv.org/abs/2503.01713). Avaloka currently implements the memory direction, not the paper's precise-retrieval pipeline.

## Embeddings

Avaloka use:

- embed user-safe care facts
- embed internal wisdom principles
- embed Baifa and compassion OS notes
- embed podcast and lecture summaries
- embed future audio/video transcripts

Week 02 embedding lesson added a measurement rule: an embedding model is not acceptable just because a few examples look semantically close. Before using an embedder for Avaloka retrieval, compare same-intent or same-memory-class pairs against different-intent or hard-negative pairs.

Useful diagnostics:

| Metric | Avaloka meaning |
| --- | --- |
| random-pair mean cosine | whether the model thinks too many unrelated memories are similar |
| random-pair std | whether similarities are meaningfully spread out |
| intra similarity | how close genuinely related care memories, wisdom notes, or intent examples are |
| inter similarity | how far unrelated or unsafe-to-mix examples are |
| gap = intra - inter | whether the embedder separates useful matches from distractors |

For Avaloka, a high raw cosine score is not enough. The model must show separation between permitted, relevant memories and nearby-but-wrong memories, especially for hard negatives such as similar wording with different risk, different user context, different permission scope, or stale facts.

Expected first embedding experiment:

```text
labeled Avaloka query/memory pairs
-> encode with candidate embedding model
-> compute same-class and different-class cosine histograms
-> measure intra / inter / gap
-> run retrieval metrics and safety checks
-> compare against deterministic Memory Reader V0
```

## Retrieval

Avaloka use:

- retrieve relevant care facts from long-term memory
- retrieve relevant wisdom principles
- retrieve safety rules and forbidden moves
- retrieve prior eval failures

## Retrieval Funnel

Potential Avaloka flow:

```text
user input
-> crisis classifier
-> Baifa / emotional state classifier
-> memory query
-> wisdom query
-> retrieve candidate facts
-> rerank for safety and usefulness
-> inject 3-5 facts into response generator
-> guardian review
```

## Agent-First Loop

Avaloka should treat retrieval as one part of an agent loop:

```text
user input
-> classify intent, risk, and emotional state
-> retrieve memory, wisdom, safety rules, and prior eval failures
-> decide next step: answer, ask, ground, refuse, escalate, or use tool
-> generate response with limited evidence
-> guardian review
-> save trace
-> run evals on retrieval, decision, safety, and tone
```

Key agent decisions:

- when to use memory
- when not to use memory
- when to ask a clarifying question
- when to refuse unsafe framing
- when to ground the user in practical care
- when to escalate to crisis support
- when to update or forget a memory

## GraphRAG

Possible graph nodes:

- user pain pattern
- care memory
- wisdom principle
- Baifa mind state
- antidote
- response move
- safety boundary
- eval case
- source document

Possible edges:

- `evidenced_by`
- `supports_response_move`
- `contraindicates`
- `maps_to_mind_state`
- `answered_by_principle`
- `failed_in_eval`
- `supersedes`

## Architecture Escalation

Avaloka should begin with the smallest observable agent loop and add retrieval architecture only when traces and evals expose a specific limitation:

```text
basic retrieval + safety rules + trace + eval
-> improve chunking and reranking when evidence is missed
-> add adaptive context selection when noise becomes measurable
-> add RAPTOR when questions require multiple abstraction levels
-> add GraphRAG when relationships and corpus-wide structure are required
-> consider fine-tuning only when behavior failures persist despite good evidence
```

Each new component must improve a named eval, justify its latency and cost, and preserve source provenance and privacy boundaries.

## Semantic Cache

Potentially cache:

- retrieval results for stable public source material
- embeddings for unchanged source documents
- approved, non-personalized informational answers with short TTLs

Do not share-cache:

- answers containing user memories
- emotional-state or crisis assessments
- personalized spiritual or care guidance
- permission-sensitive evidence
- responses generated under outdated safety policies

Cache identity must include the relevant user or tenant scope, source-index version, model and prompt version, safety-policy version, and permissions. A semantically similar question is not automatically safe to treat as the same situation.

If cache hits become the majority path, Avaloka must treat cache behavior as a first-class product surface. Measure cache-hit and cache-miss quality separately, invalidate entries after knowledge or safety-policy changes, and prevent one incorrect semantic match from becoming a repeatedly served failure.

If Avaloka eventually fine-tunes an embedder for cache matching, train and evaluate it on domain-specific query pairs, including hard negatives that sound similar but require different care or safety responses. Tune the threshold to minimize harmful false hits rather than maximizing cache-hit rate.

## RAG Evals

Avaloka questions:

- Did retrieval find the right care facts?
- Did it avoid unsafe memories?
- Did it retrieve wisdom without sounding religious or doctrinal?
- Did the final answer stay natural and compassionate?
- Did guardian catch bad output?

Evaluation layers:

| Layer | Example measures |
| --- | --- |
| retrieval | recall@k, MRR, MAP, NDCG |
| grounding | claim support, citation correctness, contradiction rate, FActScore-style atomic factuality |
| answer | relevance, completeness, clarity, RAGAS-style dimensions |
| agent decision | correct answer, ask, abstain, refuse, ground, escalate, or tool-use choice |
| safety and memory | HHH rubric, privacy leakage, forbidden memory access, crisis-routing accuracy |
| operations | latency, token cost, cache hit and false-hit rates, retries |

Agent behavior questions:

- Did the agent choose the right next step?
- Did it use memory only when appropriate?
- Did it avoid raw private memory exposure?
- Did it refuse or redirect unsafe requests?
- Did it preserve warmth while staying bounded?

## Multimodal

Future Avaloka use:

- ingest podcasts
- summarize Buddhist lectures
- process user audio diaries
- process video transcripts
- extract emotional moments from voice notes

## Text-to-SQL

Potential internal uses:

- analyze guardrail and crisis-routing frequencies
- inspect retrieval and eval results over time
- answer product questions from structured traces
- examine memory-policy compliance without exposing raw private content

Keep the initial implementation read-only and scoped to approved analytical views. Retrieve schema and metric definitions, validate generated SQL before execution, enforce tenant and row permissions, and ground the final answer in the returned rows.

## Guardrails

Avaloka's top-level guardian rubric is **Helpful, Harmless, and Honest**:

- helpful: understand the user's actual need and offer a useful, compassionate next step
- harmless: avoid unsafe advice, privacy violations, crisis minimization, and harmful spiritual framing
- honest: ground factual claims, identify uncertainty, and never invent memories, authority, or certainty

Avaloka guardrails:

- no medical diagnosis
- no karma blame
- no spiritual bypass
- no crisis minimization
- no hidden prompt disclosure
- no raw private memory exposure

Request-side ordering matters:

```text
authenticate and authorize
-> detect crisis, medical, abuse, and prompt-injection risk
-> determine allowed memory scope
-> retrieve only permitted evidence
-> generate under the selected safety policy
-> guardian review
```

Each gate should return a structured decision and reason code. High-risk or unauthorized requests should be blocked or rerouted before private memory retrieval and model generation.

## Response Grounding

Avaloka's guardian should verify evidence as well as safety and tone:

```text
draft response
-> identify factual, personal-memory, and safety-sensitive claims
-> connect each claim to permitted evidence
-> mark direct support, inference, uncertainty, or contradiction
-> revise, retrieve again, ask, abstain, or escalate
```

Claims about a user's history must point to permitted memory records. Health, crisis, or practice guidance must use approved sources and preserve uncertainty. Unsupported warmth is acceptable as conversational expression; unsupported factual certainty is not.

Represent grounding as an assertion-evidence graph rather than a single answer score. Each factual claim should carry evidence IDs, provenance, permission scope, freshness, and verification status. Use cheaper deterministic checks first and escalate ambiguous or high-risk claims to an independent judge.

## Personal Research Question

Can Avaloka combine:

```text
SAGE-style memory
+ RAG-style knowledge retrieval
+ Compassion OS
+ Baifa mapper
+ guardian eval
```

into a reliable long-term AI companion architecture?

## Next Measured Experiment

Benchmark the current deterministic Memory Reader V0 before installing a new retrieval stack:

```text
labeled Avaloka memory queries
-> deterministic reader baseline
-> Recall@5 / MRR / NDCG@5
-> privacy, stale-memory, no-match, and latency checks
-> failure classification
-> smallest justified retrieval upgrade
```

Task: [T008: Benchmark Avaloka Memory Reader V0](../tasks/T008-benchmark-avaloka-memory-reader.md)
