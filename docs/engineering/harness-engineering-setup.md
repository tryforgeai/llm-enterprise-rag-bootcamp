# Harness Engineering Setup

## Purpose

This project uses an agent-first operating model:

> Humans define direction, judgment, and acceptance criteria. Agents execute against repository-visible docs, checklists, traces, evals, and feedback loops.

## Source of Truth

- `README.md` is the human entry point.
- `AGENTS.md` is the agent entry point.
- `docs/` contains active governance documents.
- `course/`, `labs/`, `avaloka-applications/`, `evals/`, and `traces/` contain project work.
- `archive/` contains historical reference only.

## Required Project Definition

| Field | Value |
|---|---|
| Project | LLM and Enterprise RAG Bootcamp |
| Current stage | validation / learning system setup |
| Final vision | Turn bootcamp learning into Avaloka agent capabilities. |
| Current version | v0.1 agent-first bootcamp scaffold |
| Next version | v0.2 first runnable agentic RAG loop |
| Target user | Rosso building Avaloka AI with future agent assistance |
| First use case | Minimal agentic RAG loop for Avaloka course learning |
| Non-goals | Production deployment; full GraphRAG; full memory system; medical or crisis-treatment claims. |
| Success criteria | Active docs are coherent, eval cases exist, traces are saved, and future agents can recover direction. |
| Safety/quality boundaries | No raw private memory exposure, no diagnosis, no karma blame, no spiritual bypass, no crisis minimization. |

## Agent-Readable Workflow

For each meaningful change:

1. Read `AGENTS.md`.
2. Read `docs/product/product-vision.md`.
3. Read `docs/product/version-roadmap.md`.
4. Read `docs/decisions/decision-log.md`.
5. Check `tasks/index.md`.
6. Update source-of-truth docs when decisions change.
7. Add decision-log entries for meaningful direction changes.
8. Add or update traces, evals, or checklists for behavior changes.
9. Run verification.
10. Archive stale docs instead of leaving conflicting plans active.

## Verification Commands

Run the installed skill audit:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/agent-first-project-bootstrap/scripts/agent-first.mjs" audit .
```

Run document gardening in report-only mode:

```bash
node "${CODEX_HOME:-$HOME/.codex}/skills/agent-first-project-bootstrap/scripts/agent-first.mjs" garden .
```

## Do Not Do

- Do not rely on chat memory as source of truth.
- Do not keep conflicting plans active.
- Do not skip validation criteria.
- Do not implement features before the current stage requires them.
- Do not run document gardening with `--apply` without reviewing candidates first.
