# Harness Engineering Setup

## Purpose

This project uses an agent-first operating model:

> Humans define direction, judgment, and acceptance criteria. Agents execute against repository-visible docs, checklists, tests, and feedback loops.

## Source of Truth

- `README.md` is the human entry point.
- `AGENTS.md` is the agent entry point.
- `docs/` contains active source-of-truth documents.
- `archive/` contains historical reference only.

## Required Project Definition

| Field | Value |
|---|---|
| Project | Curriculum Weaver Lite |
| Current stage | Course UI demo |
| Final vision | Pedagogy-first AI tutoring prototype for converting LLM/RAG learning materials into project-ready learning paths. |
| Current version | Step 1 |
| Next version | Step 2 |
| Target user | LLM/RAG bootcamp student and instructor reviewer. |
| First use case | Teach self-attention with a prerequisite-aware path. |
| Non-goals | No commercial scope, broad curriculum, production backend, or real student private data in Step 1. |
| Success criteria | Local UI shows profile, diagnosis, path, lesson, quiz, trace, and mastery update. |
| Safety/quality boundaries | Source-grounded, clear about demo limits, no invented citations or equations. |

## Agent-Readable Workflow

For each meaningful change:

1. Read `AGENTS.md`.
2. Read the relevant docs.
3. Check version authority: product vision, version roadmap, decision log.
4. Update source-of-truth docs when decisions change.
5. Add decision-log entries for meaningful direction changes.
6. Add or update checklists/tests for behavior changes.
7. Run verification.
8. Archive stale docs instead of leaving conflicting plans active.

## Do Not Do

- Do not rely on chat memory as source of truth.
- Do not keep conflicting plans active.
- Do not skip validation criteria.
- Do not implement features before the current stage requires them.
