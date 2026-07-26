# Decision Log

This folder records detailed project decisions so the bootcamp work stays reproducible and agent-first.

Authoritative running decisions now live in `docs/decisions/decision-log.md`. This folder keeps detailed decision files when extra context is useful.

## When To Add A Decision

Add or update an entry when a change affects:

- project direction
- agent architecture
- learning priorities
- safety, privacy, memory, or guardrails
- eval strategy
- folder structure or recurring templates
- model, vector store, framework, or workflow choices

## Decisions

| Date | Status | Decision | File |
|---|---|---|---|
| 2026-06-01 | Accepted | Make the bootcamp project agent-first, with RAG as a substrate for agent behavior, traces, and evals. | [2026-06-01-agent-first-project.md](2026-06-01-agent-first-project.md) |
| 2026-06-01 | Accepted | Require important project decisions and direction changes to be recorded in this decision log. | [2026-06-01-decision-log-rule.md](2026-06-01-decision-log-rule.md) |
| 2026-06-01 | Accepted | Implement a local Markdown-first agent bootstrap because the requested GitHub repo was not publicly accessible from this environment. | [2026-06-01-local-agent-first-bootstrap.md](2026-06-01-local-agent-first-bootstrap.md) |
| 2026-06-01 | Accepted | Use the installed `agent-first-project-bootstrap` skill scaffold as the active project governance layer. | [2026-06-01-install-agent-first-bootstrap-skill.md](2026-06-01-install-agent-first-bootstrap-skill.md) |
| 2026-06-01 | Accepted | Make agent-first bootstrap checks a global Codex default through `~/.codex/AGENTS.md`. | [2026-06-01-global-codex-agent-first-default.md](2026-06-01-global-codex-agent-first-default.md) |
| 2026-06-06 | Accepted | Switch the project from pre-class preparation to active Week 01 course execution. | [2026-06-06-active-course-start.md](2026-06-06-active-course-start.md) |
| 2026-06-06 | Accepted | Add retrieval complexity only when traces and evals demonstrate a specific failure. | [2026-06-06-evidence-driven-architecture-escalation.md](2026-06-06-evidence-driven-architecture-escalation.md) |
| 2026-06-06 | Accepted | Treat existing Avaloka behavior as the baseline and use the course to formalize, evaluate, and selectively upgrade it. | [2026-06-06-avaloka-existing-capability-baseline.md](2026-06-06-avaloka-existing-capability-baseline.md) |
| 2026-06-06 | Accepted | Benchmark the deterministic Avaloka Memory Reader before adding advanced retrieval infrastructure. | [2026-06-06-benchmark-memory-reader-before-upgrade.md](2026-06-06-benchmark-memory-reader-before-upgrade.md) |
| 2026-06-07 | Accepted | Study LARQL as a read-only research and interpretability tool before any Avaloka adoption or model mutation. | [2026-06-07-study-larql-before-adoption.md](2026-06-07-study-larql-before-adoption.md) |
| 2026-06-13 | Accepted | Use an isolated, verified `uv` and Python 3.12.7 environment for SupportVectors classroom labs. | [2026-06-13-supportvectors-classroom-environment.md](2026-06-13-supportvectors-classroom-environment.md) |
| 2026-07-18 | Accepted | Align governance with Week 06 while keeping v0.1 active until trace, eval, memory-policy, and baseline criteria are complete. | [2026-07-18-align-governance-with-week-06.md](2026-07-18-align-governance-with-week-06.md) |
| 2026-07-18 | Accepted | Require locked, clone-portable Python and browser verification without machine-specific filesystem paths. | [2026-07-18-clone-portable-verification.md](2026-07-18-clone-portable-verification.md) |
| 2026-07-25 | Accepted | Advance governance to Week 07 evaluation while keeping v0.1 active until the real eval, trace, memory-policy, and baseline criteria are met. | [2026-07-25-week-07-evaluation-stage.md](2026-07-25-week-07-evaluation-stage.md) |
| 2026-07-26 | Accepted | Create a portable cross-project method toolkit while keeping course and lab artifacts as the evidence layer. | [2026-07-26-create-cross-project-method-toolkit.md](2026-07-26-create-cross-project-method-toolkit.md) |
