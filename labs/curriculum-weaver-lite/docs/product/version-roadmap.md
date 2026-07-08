# Version Roadmap

## Version Authority

This document defines current and future versions. If it conflicts with older plans, follow the latest accepted decision in `docs/decisions/decision-log.md`.

## Current Active Version

| Field | Value |
|---|---|
| Version | Step 1 |
| Stage | Course UI demo |
| Target user | LLM/RAG bootcamp student and instructor reviewer |
| First use case | Teach self-attention with a prerequisite-aware learning path |
| Success criteria | Demo shows profile -> diagnosis -> path -> lesson -> quiz -> mastery update |

### In Scope

- Static concept graph for self-attention.
- Static source cards with citations.
- Three learner profiles.
- Diagnostic mastery estimates.
- Ordered learning path.
- Lesson, code sketch, quiz, and trace panels.
- Smoke test for desktop and mobile UI flow.

### Out of Scope

- Full PDF ingestion.
- Real vector database.
- LLM synthesis.
- Persistent student accounts.
- Broad ML curriculum.
- Production deployment.

### Exit Criteria

- The demo opens locally and runs the full student flow.
- Desktop and mobile layouts do not overlap.
- Source-of-truth docs explain Step 1 and Step 2.
- Smoke test passes with no console errors.

## Next Version

| Field | Value |
|---|---|
| Version | Step 2 |
| Goal | Replace static demo intelligence with real RAG, memory, lesson synthesis, evaluation, and tests |
| Entry criteria | Step 1 UI demo is reviewed and the desired learning flow is accepted |
| Major risks | Overbuilding infrastructure before proving pedagogy value; hallucinated citations; weak eval coverage |

## Future Versions

| Version | Hypothesis | Do not start until |
|---|---|---|
| Step 3 | Multi-topic Curriculum Weaver can teach multiple LLM/RAG concepts | Step 2 proves self-attention with real retrieval and evals |
| Step 4 | Adaptive student memory improves future path recommendations | Step 2 has reliable quiz and mastery traces |

## Deferred Ideas

Ideas listed here are not active commitments.

- 
- RAPTOR summaries.
- GraphRAG over course concepts.
- Multi-agent tutoring roles.
- Teacher review dashboard.
