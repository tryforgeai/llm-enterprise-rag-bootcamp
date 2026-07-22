# Align Governance With Week 06 Without Advancing The Product Version

Status: accepted

Date: 2026-07-18

## Context

The repository's course artifacts have advanced through Week 06, but the root version roadmap still described active course / Week 03. Week 03 representation work, Week 04 derived retrieval artifacts, Week 05 graph-shaped learning artifacts, Week 06 guardrail work, and Curriculum Weaver Lite now materially exceed the roadmap's original scope.

At the same time, the defining v0.1 exit criteria remain incomplete: the first 10 agentic RAG eval cases, Avaloka memory-scope policy, a canonical saved trace, and a runnable minimal trace-and-eval loop do not yet exist as durable project artifacts.

## Decision

Align the roadmap's stage and scope with Week 06 while retaining the v0.1 version label. Mark T014 done because all of its declared criteria are checked and supported by artifacts. Keep T011, T015, and T020 doing because each still has explicit incomplete criteria.

## Consequences

- Course progress is no longer understated by the governance layer.
- The project does not claim v0.2 maturity merely because later course experiments exist.
- Product completion remains tied to trace, eval, memory-policy, and baseline evidence.
- Future task reviews should distinguish chronological course completion from agent-first product-version readiness.
- Future agents have a lightweight `docs/knowledge/` layer for active traps and non-obvious fixes.

## Affected Files

- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`
- `tasks/index.md`
- `tasks/T014-week-03-class-capture.md`
- `README.md`
- `AGENTS.md`
- `PROJECT_PLAN.md`
- `docs/knowledge/gotchas.md`
- `docs/knowledge/fix-log.md`

## Follow-Up Checks

- Create and review the first 10 agentic RAG eval cases under `evals/`.
- Define Avaloka memory scopes and use rules.
- Save at least one canonical agent trace under `traces/`.
- Implement the minimal trace-and-eval loop.
- Benchmark Avaloka Memory Reader V0 before approving retrieval architecture changes.
