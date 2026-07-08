# Install Agent-First Bootstrap Skill Scaffold

Status: accepted

Date: 2026-06-01

## Context

The local directory `/Users/rosso.han/Documents/Obsidian Vault/Projects/agent-first-project-bootstrap` contains a valid Codex skill with `SKILL.md`, scripts, templates, and OpenAI metadata.

The same skill is already installed at `/Users/rosso.han/.codex/skills/agent-first-project-bootstrap`. The installed copy passes `validate-skill`.

The current bootcamp project had a custom lightweight agent-first scaffold, but not the skill's standard `docs/` governance layout.

## Decision

Use the installed `agent-first-project-bootstrap` skill as the active governance scaffold for this project.

Keep the bootcamp-specific folders already created:

- `course/`
- `labs/`
- `avaloka-applications/`
- `tasks/`
- `templates/`
- `traces/`
- `evals/`
- `decisions/`

Add and maintain the skill-standard governance docs under `docs/`.

## Consequences

- `docs/product/product-vision.md`, `docs/product/version-roadmap.md`, and `docs/decisions/decision-log.md` become the active authority for direction and scope.
- `decisions/` remains a detailed decision-file library.
- Future agents should use `AGENTS.md` and `docs/` before reading working notes.
- The project can be audited with the installed skill's `audit` command.

## Affected Files

- `AGENTS.md`
- `README.md`
- `PROJECT_PLAN.md`
- `docs/`
- `archive/README.md`
- `decisions/index.md`

## Follow-Up Checks

- Run the skill audit after scaffold updates.
- Treat `garden --apply` as destructive enough to require human review of candidates first.
- Keep `docs/` concise; put detailed course work in existing project folders.
