# T001 Install Local Agent-First Bootstrap Structure

Status: done

## Goal

Install a local agent-first project structure without relying on the unavailable external GitHub repo.

## Context

The requested repository, `tryforgeai/agent-first-project-bootstrap`, returned 404 through the GitHub API in this environment. The project still needs the bootstrap pattern: strong `AGENTS.md`, source-of-truth plan, task queue, decision log, trace templates, and eval templates.

## Done Criteria

- `AGENTS.md` includes startup sequence and end-of-turn checks.
- `PROJECT_PLAN.md` exists.
- `tasks/index.md` exists with initial tasks.
- `templates/` contains decision, trace, eval, and weekly note templates.
- `decisions/` records the bootstrap decision.

## Result

Implemented local Markdown-first bootstrap for this Obsidian project.
