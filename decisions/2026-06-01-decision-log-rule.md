# Decision Log Rule

Status: accepted

Date: 2026-06-01

## Context

Important direction changes can get lost in scattered notes. That is especially risky for an agent-first project because the important work is often not one code change, but a shift in policy, architecture, evaluation, memory handling, or learning priority.

The project needs a durable record that future agents and humans can read before changing direction.

## Decision

Important decisions and direction changes must be recorded in `decisions/`.

Agents working in this project must check whether their work changes project direction, architecture, scope, safety policy, evaluation strategy, memory policy, learning priorities, or folder structure. If it does, they must update `decisions/index.md` and create or update a decision file.

## Consequences

- The project gains a durable decision trail.
- Future agents can recover why a direction was chosen.
- Reviews can distinguish current strategy from outdated notes.
- Small edits stay lightweight because formatting-only or routine note changes do not require decision entries.

## Affected Files

- `AGENTS.md`
- `decisions/index.md`
- `decisions/2026-06-01-agent-first-project.md`
- `decisions/2026-06-01-decision-log-rule.md`
- `README.md`

## Follow-Up Checks

- Before final response, agents should check whether a decision log update is needed.
- During project review, inspect `decisions/index.md` before judging current direction.
- If a decision is replaced, mark the old decision as superseded and link to the newer one.
