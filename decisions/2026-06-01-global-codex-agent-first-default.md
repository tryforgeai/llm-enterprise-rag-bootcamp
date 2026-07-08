# Global Codex Agent-First Default

Status: accepted

Date: 2026-06-01

## Context

The `agent-first-project-bootstrap` skill was already installed in `~/.codex/skills`, but it did not appear in the current session's visible skill list. The assistant initially searched GitHub and local project files instead of checking installed local skills first.

## Decision

Use `~/.codex/AGENTS.md` as the global Codex rule file for this machine and add an agent-first project default:

- check local skills before web search
- prefer `agent-first-project-bootstrap` for project bootstrap/review/governance work
- run audit before inventing a scaffold
- run bootstrap when scaffold files are missing and the user wants implementation
- fill generated placeholders and re-run audit

## Consequences

- This behavior applies across future Codex projects unless a project-level `AGENTS.md` gives more specific instructions.
- New or under-scaffolded projects should become agent-first by default.
- The failure mode from this session should be less likely to repeat.

## Affected Files

- `/Users/rosso.han/.codex/AGENTS.md`
- `docs/decisions/decision-log.md`
- `decisions/2026-06-01-global-codex-agent-first-default.md`

## Follow-Up Checks

- Start a fresh Codex session later and confirm the global `AGENTS.md` behavior is included.
- If Codex exposes a more formal default-project-template mechanism later, migrate this rule there.
