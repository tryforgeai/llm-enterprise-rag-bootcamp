# Study LARQL Before Any Avaloka Adoption

Status: accepted

Date: 2026-06-07

## Context

LARQL presents transformer weights as a queryable vindex and supports browsing, residual tracing, reversible patches, inference, and model recompilation through LQL.

This is relevant to the course's work on embeddings, traces, evaluation, model knowledge, and Text-to-SQL-like interfaces. It may also support Avaloka research into safety associations and model behavior.

However, LARQL is a young project. Its graph-like edges are inferred from model internals rather than authoritative source records, and targeted weight edits may have effects that are not visible from one successful prompt.

## Decision

Add LARQL as a research and mechanistic-interpretability learning track.

Begin with a read-only reproduction that compares `DESCRIBE`, `WALK`, `TRACE`, and `INFER` on a fixed dataset. Do not integrate LARQL into Avaloka or perform production model edits until precision, consistency, locality, resource cost, and failure modes are measured.

## Consequences

- LARQL is not treated as a replacement for RAG, GraphRAG, Care Card memory, or grounding.
- External retrieval remains the source for current, private, attributable, and permission-scoped knowledge.
- Initial LARQL work uses public or synthetic prompts only.
- Mutation and compilation require a separate decision after read-only validation.

## Affected Files

- `resources/tools/larql-learning-note.md`
- `tasks/T009-study-larql-read-only.md`
- `tasks/index.md`
- `docs/decisions/decision-log.md`
- `decisions/index.md`

## Follow-Up Checks

- Reproduce the read-only workflow.
- Measure `DESCRIBE` to `INFER` agreement and false associations.
- Confirm resource requirements on the available machine.
- Reassess whether a synthetic patch experiment is justified.

