# Keep Secrets Out Of Git

Status: accepted
Date: 2026-07-08

## Context

The project now has a Git repository. API keys, access tokens, passwords, private certificates, service account files, and machine-specific environment values must stay local and must not be uploaded to Git.

## Decision

Use the ignored root `.env` file as the only place for real local secrets and machine-specific values. Commit `.env.example` with variable names only. Source code must read credentials from environment variables rather than hardcoding key or token values.

## Consequences

- `.env`, `.env.*`, private key files, service account JSON, credential JSON, `.envrc`, and local security reports remain ignored.
- `.env.example` documents required variables without values.
- The SV cluster OpenAI-compatible helper now reads `SV_OPENAI_API_KEY` or `OPENAI_API_KEY` from the environment.
- Agents must run a secret check before committing credential-related changes.

## Affected Files

- `.gitignore`
- `.env.example`
- `.env` (ignored local file)
- `AGENTS.md`
- `README.md`
- `labs/sv_ray_cluster_access/src/ray_cluster_access/sv_cluster_access_api.py`
- `labs/sv_ray_cluster_access/.env.example`
- `course/week_04/chunking_pipeline/.env.example`
- `docs/decisions/decision-log.md`
- `tasks/T019-keep-secrets-out-of-git.md`

## Follow-Up Checks

- Run `git ls-files '*.env' '.env.*' '**/.env' '**/.env.*'` before pushing.
- Run a hardcoded secret grep before commits that touch code or config.
