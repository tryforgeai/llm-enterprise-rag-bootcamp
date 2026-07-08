# Installed Agent-First Bootstrap Review

Date: 2026-06-01

## Verdict

`agent-first-project-bootstrap` is installed and usable. The installed copy at `~/.codex/skills/agent-first-project-bootstrap` passes `validate-skill`, and the current bootcamp project now passes the skill's `audit` with `100/100`.

The project is now structurally agent-first. The remaining work is content execution: eval cases, memory policy, traces, and the first runnable loop.

## What Changed

- Added the skill-standard `docs/` governance scaffold.
- Filled product vision, version roadmap, decision log, validation runbook, quality checklist, engineering setup, and archive README with project-specific content.
- Updated `README.md` and `AGENTS.md` to point future agents at the active source-of-truth docs.
- Recorded the installation decision in both `docs/decisions/decision-log.md` and `decisions/`.

## Audit Result

Command:

```bash
node ~/.codex/skills/agent-first-project-bootstrap/scripts/agent-first.mjs audit "/Users/rosso.han/Documents/Obsidian Vault/Projects/LLM and Enterprise RAG Bootcamp"
```

Result:

- Score: `100/100`
- Required files: all present
- Recommended directories: all present
- Warnings: none

## Findings

### P1 — No eval cases yet

The scaffold is ready, but `evals/` is still empty. Without eval cases, the project can talk about agent-first behavior but cannot verify it.

Fix: complete `T002` and create 10 eval cases across retrieval, decision, safety, memory use, and tone.

### P1 — Memory scope policy is still missing

Avaloka memory use is the highest-risk part of the architecture. The project already names private memory exposure as a boundary, but it still needs concrete memory scopes and allowed/forbidden uses.

Fix: complete `T003` before any richer memory retrieval experiment.

### P2 — No recorded agent traces yet

The project has trace templates, but no actual trace examples. That means GraphRAG, retrieval funnels, and memory policy are still being reasoned about without observed failures.

Fix: complete `T004` with at least one trace in `traces/`.

### P2 — Document gardening has RAG false positives

The skill's `garden` command treats RAG mentions as stale-direction candidates. In this project, RAG is the core subject, so those hits are mostly false positives.

Fix: complete `T005`; do not run `garden --apply` without manual review.

### P3 — There are two decision layers

The authoritative running log now lives in `docs/decisions/decision-log.md`, while detailed decision files live in root `decisions/`. This is workable, but future agents must preserve the distinction.

Fix: keep `docs/decisions/decision-log.md` as the index of accepted decisions and use root `decisions/` only for detail.

## Current Next Actions

1. Create 10 eval cases in `evals/`.
2. Define Avaloka memory scopes and use rules.
3. Run one minimal agentic RAG trace.
4. Decide whether to patch the skill's RAG stale-pattern heuristic.
