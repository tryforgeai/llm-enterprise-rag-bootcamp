# Benchmark The Existing Memory Reader Before Upgrading Retrieval

Status: accepted

Date: 2026-06-06

## Context

The Avaloka Week 01 capability audit found an active deterministic Care Card reader with safety-aware ranking, but no formal retrieval metrics. Embeddings, hybrid retrieval, reranking, RAPTOR, and GraphRAG are not active implementations.

Without a labeled baseline, adding one of those techniques would show that the architecture changed, not that retrieval improved.

## Decision

The first Avaloka course-integration experiment will benchmark Memory Reader V0 on a fixed relevance dataset.

The baseline must measure:

- Recall@5
- MRR
- NDCG@5
- unsafe or private retrievals
- stale retrievals
- no-match precision
- latency

An embedding, hybrid, reranking, or graph component may be proposed only after the baseline identifies the failure it is intended to fix.

## Consequences

- The current deterministic reader remains the comparison baseline.
- GraphRAG, RAPTOR, semantic cache, and fine-tuning remain deferred.
- Retrieval changes must preserve or improve privacy, safety, latency, and debuggability.
- Course implementation starts with measurement rather than infrastructure installation.

## Affected Files

- `reviews/04-avaloka-week-01-capability-audit.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `tasks/T007-audit-existing-avaloka-capabilities.md`
- `tasks/T008-benchmark-avaloka-memory-reader.md`
- `tasks/index.md`
- `docs/decisions/decision-log.md`

## Follow-Up Checks

- Build the labeled retrieval dataset.
- Save the deterministic baseline report.
- Map each important miss to the smallest plausible intervention.
- Reject any added component that does not improve its named metric.

