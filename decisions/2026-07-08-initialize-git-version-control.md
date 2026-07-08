# Initialize Git Version Control

Status: accepted
Date: 2026-07-08

## Context

The project had an agent-first document scaffold but was not yet a Git repository. Future agents need a durable history for project documents, labs, decisions, task updates, and evaluation artifacts.

## Decision

Initialize this project as a local Git repository and use a conservative `.gitignore` to exclude local secrets, system files, dependency folders, caches, and generated runtime output.

## Consequences

- Project history can now be reviewed with Git.
- `.env`, `.DS_Store`, local tool session folders, cache folders, virtual environments, dependencies, build outputs, logs, nested `.git` metadata, and generated lab artifacts should stay untracked.
- The empty nested Git metadata in `course/week_03/week-03-in-person-lab/` was preserved as an ignored `.git.nested-backup-20260708/` folder so the lab source can be tracked by the root repository.
- Course notes, governance docs, tasks, labs, evals, traces, templates, and decision records remain eligible for version control.

## Affected Files

- `.gitignore`
- `docs/decisions/decision-log.md`
- `tasks/index.md`
- `tasks/T018-initialize-git-version-control.md`
- `decisions/2026-07-08-initialize-git-version-control.md`

## Follow-Up Checks

- Review `git status --short` before the first commit.
- Confirm no secrets are staged.
