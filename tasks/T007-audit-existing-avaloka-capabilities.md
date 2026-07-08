# T007: Audit Existing Avaloka Capabilities

Status: done

## Goal

Determine which bootcamp concepts Avaloka already implements in behavior or architecture before proposing new technology.

## Scope

For each capability, record:

- status: existing, partial, missing, or unknown
- implementation evidence
- trace or observability evidence
- current eval coverage
- known failure modes
- whether a course technique could add measurable value

Initial capability list:

- intent and risk classification
- scoped memory retrieval
- retrieval and reranking
- request guardrails
- Helpful, Harmless, and Honest guardian behavior
- response grounding
- trace capture
- evaluation
- semantic cache
- multi-resolution or graph-shaped retrieval

## Done When

- [x] The capability matrix is added to the Avaloka application map or a linked audit.
- [x] At least three existing strengths and three evidence gaps are identified.
- [x] The next technical experiment is chosen from a measured gap.

## Result

Completed in:

- `reviews/04-avaloka-week-01-capability-audit.md`
- `decisions/2026-06-06-benchmark-memory-reader-before-upgrade.md`
- `tasks/T008-benchmark-avaloka-memory-reader.md`

The audit found strong agent routing, safety, memory lifecycle, trace, and behavioral eval capability. The first measured gap is retrieval evaluation, so the next experiment benchmarks the existing deterministic Memory Reader V0 before adding new retrieval infrastructure.
