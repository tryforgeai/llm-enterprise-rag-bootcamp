# Local Agent-First Bootstrap

Status: accepted

Date: 2026-06-01

## Context

The requested repository, `https://github.com/tryforgeai/agent-first-project-bootstrap`, could not be read from this environment. GitHub API returned 404 for `tryforgeai/agent-first-project-bootstrap`, and direct archive download returned `Not Found`.

The project still needs the agent-first bootstrap pattern: a strong agent instruction file, source-of-truth plan, durable decisions, task queue, trace templates, and eval templates.

## Decision

Implement a local Markdown-first bootstrap instead of claiming the inaccessible external repo was installed.

This bootstrap uses:

- `AGENTS.md` for operating rules
- `PROJECT_PLAN.md` for current direction and rhythm
- `decisions/` for durable decisions
- `tasks/` for lightweight work tracking
- `templates/` for reusable decision, trace, eval, and weekly note formats
- `traces/` for agent run records
- `evals/` for eval cases and results

## Consequences

- The project is usable by future agents immediately.
- The setup does not depend on unavailable tools or private repo access.
- If the original bootstrap repo becomes accessible later, this local structure should be compared against it rather than overwritten blindly.
- If dedicated tools such as Beads, Beads Viewer, or Agent Mail are installed later, `tasks/` can be migrated into those tools.

## Affected Files

- `AGENTS.md`
- `PROJECT_PLAN.md`
- `README.md`
- `tasks/`
- `templates/`
- `traces/`
- `evals/`
- `decisions/index.md`

## Follow-Up Checks

- Compare this structure with the external bootstrap if access becomes available.
- Keep `AGENTS.md` project-specific and short enough for future agents to reread.
- Convert `tasks/` to a dedicated task tool only after the workflow proves useful.
