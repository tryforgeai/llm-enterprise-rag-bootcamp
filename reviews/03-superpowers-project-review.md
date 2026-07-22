# Superpowers Project Review

Date: 2026-06-01

## Verdict

The project is well scaffolded, but not yet execution-ready. It has strong source-of-truth docs, clear agent-first direction, and an audit-passing governance structure. The next risk is false confidence: the docs describe the intended loop, but the project does not yet contain the eval cases, memory policy, or traces needed to prove the loop works.

From a Superpowers perspective, the project needs less planning and more verification artifacts.

## What Is Strong

- `AGENTS.md` gives future agents a clear startup sequence.
- `docs/product/product-vision.md` defines the agent-first mission and boundaries.
- `docs/product/version-roadmap.md` correctly names v0.1 and v0.2.
- `docs/decisions/decision-log.md` records the major governance decisions.
- `tasks/index.md` exposes the next work instead of hiding it in chat.
- The installed `agent-first-project-bootstrap` audit reports `100/100`.

## Execution Gaps

### P1 — v0.1 exit criteria are not met

`docs/product/version-roadmap.md` says v0.1 exits when:

- first 10 eval cases exist
- Avaloka memory scope policy exists
- at least one example trace exists

Those are not present yet. `evals/` and `traces/` have no files, and the memory policy is still only a task.

### P1 — T002 is the next forcing function

The first 10 eval cases should come before the runnable demo. Without evals, the demo will optimize for plausible output instead of verified behavior.

Recommended order:

1. Finish `T002`.
2. Finish `T003`.
3. Then start `T004`.

### P2 — T004 needs an implementation plan before coding

The minimal agentic RAG demo is multi-step and behavior-sensitive. Before implementation, write a Superpowers-style plan with exact files, commands, expected outputs, and verification checks.

Suggested path:

```text
docs/superpowers/plans/2026-06-01-minimal-agentic-rag-demo.md
```

### P2 — Verification commands are too scattered

The project has an audit command in `docs/engineering/harness-engineering-setup.md`, but no single verification checklist for the current milestone.

Recommended milestone verification:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/agent-first-project-bootstrap/scripts/agent-first.mjs" audit .
find evals -type f | wc -l
find traces -type f | wc -l
test -f avaloka-applications/02-memory-scope-policy.md
```

### P2 — Garden false positives should not block work

The document gardening tool flags RAG mentions as stale candidates. For this project, most of those are false positives because RAG is the course subject.

Keep `garden` in report-only mode until `T005` is resolved.

## Recommended Superpowers Flow

Use this sequence:

1. Use `writing-plans` for `T002` if creating the eval set becomes large enough to need task-by-task work.
2. Use `writing-plans` before implementing `T004`.
3. Use `verification-before-completion` at every milestone.
4. Do not claim v0.1 is complete until the exit criteria are verified from files.

## Next Best Move

Create the first 10 eval cases in `evals/`.

The cases should cover:

- 3 factual retrieval cases
- 2 safety or guardrail cases
- 2 memory-use cases
- 2 decision-policy cases
- 1 tone and compassion case

Each case should name expected evidence, expected decision, safety/memory concerns, pass criteria, and fail criteria.
