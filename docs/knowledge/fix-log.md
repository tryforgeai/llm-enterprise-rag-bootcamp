# Fix Log

This file records non-obvious governance and implementation fixes with their root cause and verification evidence.

## 2026-07-18 — Align Roadmap And Task State With Week 06

Status: Active

### Problem

The roadmap reported active Week 03 after course work had advanced through Week 06, and T014 remained active after all of its done criteria were satisfied.

### Root Cause

Course artifacts advanced faster than the governance review rhythm.

### Fix

Updated the roadmap stage and progress snapshot, retained v0.1 until its product exit criteria are met, marked T014 done, refreshed the near-term project plan, and added lightweight team-memory files.

### Verification

- `node "${CODEX_HOME:-$HOME/.codex}/skills/agent-first-project-bootstrap/scripts/agent-first.mjs" audit .`
- `node "${CODEX_HOME:-$HOME/.codex}/skills/agent-first-project-bootstrap/scripts/agent-first.mjs" brief .`
- `git diff --check`

### Follow-Up

- Complete T002, T003, T004, and T008.
- Resolve T005 so generic gardening output is less noisy for this RAG-centered repository.

## 2026-07-18 — Make Repository Verification Clone-Portable

Status: Active

### Problem

Week 03 tests lacked a local dependency lock, Curriculum Weaver loaded Playwright and Chrome from one machine, and several committed files contained user-specific absolute paths.

### Root Cause

Experiments were validated incrementally in local tool environments without a repository-level portability pass.

### Fix

Added locked Python and Node dependency manifests, made the browser smoke test self-hosting and Playwright-managed, changed scripts and metadata to repository-relative paths, and documented clone-to-test commands.

### Verification

- `cd course/week_03 && uv sync --frozen && uv run pytest`
- `npm ci && npx playwright install chromium && npm test`
- repository-wide absolute-path scan
- clean-copy verification outside the working checkout

### Follow-Up

- Keep generated trace and eval metadata repository-relative before committing it.
