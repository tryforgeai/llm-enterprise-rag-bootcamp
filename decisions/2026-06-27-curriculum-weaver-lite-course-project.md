# Curriculum Weaver Lite Course Project

Status: accepted

Date: 2026-06-27

## Context

The course project needs to practice LLM, RAG, memory, agent tracing, evaluation, and UI testing. A generic chunking-and-embedding demo would not address the educational problem clearly enough.

## Decision

Create `labs/curriculum-weaver-lite/` as a pedagogy-first RAG tutor course project. The first domain is learning self-attention. Step 1 is a static UI demo. Step 2 replaces static intelligence with real ingestion, retrieval, learner memory, lesson synthesis, quiz evaluation, trace dashboard, and tests.

## Rationale

The project should demonstrate that educational RAG is not only about retrieving similar chunks. It should model the learner, identify missing prerequisites, retrieve source-grounded material at the right depth, and update the learner model through quiz feedback.

## Consequences

- Curriculum Weaver Lite belongs to the Bootcamp project under `labs/`, not the Avaloka AI repository root.
- The project remains a course lab, not a commercial product direction.
- Future work should update `tasks/T015-curriculum-weaver-lite.md` and preserve the lab's source-of-truth docs.

## Affected Files

- `labs/curriculum-weaver-lite/`
- `tasks/index.md`
- `tasks/T015-curriculum-weaver-lite.md`
- `docs/decisions/decision-log.md`
