# Avaloka Memory Reader V0 Eval Set

Status: draft seed scaffold

Purpose: create the first fixed, versioned relevance set for benchmarking Avaloka's deterministic Memory Reader V0 before embeddings, hybrid retrieval, reranking, RAPTOR, or GraphRAG.

## Scope

This set measures whether memory retrieval finds the right Care Card evidence, ranks the most important evidence early, and avoids stale, unsafe, private, or irrelevant memory.

The seed cases in `cases.seed.jsonl` define the target coverage shape. `cases.labeled-from-avaloka.jsonl` is the first converted labeled set, generated from AvalokaAI's existing synthetic Memory Reader benchmark fixture at `evals/memory-reader-retrieval-cases.json`.

The converted set is suitable for schema-level inspection and cross-project planning. To make it the authoritative runnable baseline inside this bootcamp repository, either copy the matching Care Card fixture data or run the baseline inside the AvalokaAI repository and import its metric report.

## Coverage Targets

Minimum v0:

| Type | Count | Purpose |
|---|---:|---|
| factual-memory | 5 | Retrieve explicit user-approved care facts. |
| hard-negative | 5 | Avoid similar wording with different implication. |
| no-match | 5 | Return no memory / ask instead of inventing. |
| stale-or-superseded | 4 | Avoid outdated or superseded facts. |
| safety-priority | 4 | Surface high-risk memories early when allowed. |
| tone-or-preference | 3 | Use preferences without creepy over-personalization. |
| forbidden-or-private | 2 | Do not retrieve/use forbidden or unauthorized memories. |
| partial-answer | 2 | Answer supported parts and mark unknowns. |

Current converted set:

- `cases.seed.jsonl`: 12 seed template cases for future hand-labeling.
- `cases.labeled-from-avaloka.jsonl`: 48 labeled cases converted from AvalokaAI synthetic Memory Reader fixtures.
- `baseline-report-2026-08-01.md`: first Memory Reader V0 benchmark summary imported from the AvalokaAI runnable harness.
- `hardening-plan.md`: next eval-expansion plan for pressure-testing the clean baseline.
- `cases.hardening.seed.jsonl`: 30 harder seed cases covering cross-lingual no-tag, partial-answer, lifecycle conflict, Baifa/Dharma boundary, privacy/deletion, and surface-overlap probes.

## Primary Metrics

- `Recall@5`: did the reader find the relevant memories?
- `MRR`: did the first relevant memory appear early?
- `nDCG@5`: were high-value memories ranked above weak matches?
- `no_match_precision`: did no-evidence cases avoid spurious memory use?
- `stale_retrieval_count`: did stale or superseded memories leak in?
- `unsafe_or_private_retrieval_count`: did forbidden/private memories appear?
- `latency_ms`: can the deterministic reader remain product-feasible?

## Failure Classes

Use the smallest matching class:

- `missing_tag_or_alias`
- `semantic_paraphrase_miss`
- `correct_candidate_ranked_too_low`
- `irrelevant_context_selected`
- `stale_or_superseded_leak`
- `permission_scope_leak`
- `no_match_false_positive`
- `relationship_or_multihop_miss`

## Promotion Rule

Do not promote embeddings, reranking, GraphRAG, RAPTOR, or fine-tuning from this eval alone. First publish baseline metrics plus at least five representative traces. Any new component must name the failure class it fixes and improve the metric it targets without weakening safety, privacy, latency, or debuggability.

The hardening set should be converted into AvalokaAI's runnable fixture shape before it is used to justify architecture changes. Its purpose is to make failure visible, not to preserve a perfect score.
