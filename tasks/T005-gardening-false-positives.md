# T005 Gardening False Positives

Status: todo

## Goal

Tune or document false positives from `agent-first-project-bootstrap` document gardening for this project.

## Context

The skill's `garden` command flags any active document mentioning RAG as a candidate superseded doc. That may make sense for projects where RAG was an old direction, but this bootcamp project is explicitly about enterprise RAG and agentic RAG.

## Done Criteria

- Decide whether to patch the local skill's stale patterns or document the false positives in project docs.
- Do not run `garden --apply` until candidates have been manually reviewed.
- If the skill is patched, validate it with `validate-skill`.
