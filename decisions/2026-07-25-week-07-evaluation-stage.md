# Advance Governance Stage To Week 07 Evaluation

Status: accepted

Date: 2026-07-25

## Context

Week 07 introduced EVAL-set construction, classical retrieval metrics, statistical significance, generation evaluation, claim-level entailment, calibrated abstention, trajectory evaluation, and runnable metric demos. The active governance documents still identified Week 06 as current after the Week 07 commit was integrated.

## Decision

Advance the active course stage to Week 07 without advancing beyond product version v0.1. Prioritize one real retrieval baseline that connects the Week 07 curriculum to the existing first-eval-set and Memory Reader benchmark tasks.

## Consequences

- Week 07 is the current learning stage.
- Metric demos count as learning artifacts, not as the missing Avaloka baseline.
- T021 remains doing until its unchecked completion criteria are satisfied.
- Product-version advancement still depends on eval cases, memory policy, a canonical trace, and the minimal runnable loop.

## Affected Files

- `README.md`
- `PROJECT_PLAN.md`
- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`
- `tasks/T021-week-07-class-capture.md`

## Follow-Up Checks

- Create the Week 07 real retrieval baseline artifact.
- Connect its failure diagnosis to T008.
- Preserve T002 as the broader agent-behavior eval-set task.
