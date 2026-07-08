# T019 - Keep Secrets Out Of Git

Status: done

## Why This Matters

The project uses LLM APIs, classroom endpoints, and local lab environments. Real keys and tokens must stay in local `.env` files so they do not leak through Git history or future pushes.

## Done Criteria

- Root `.env.example` exists with variable names only.
- `.gitignore` protects `.env`, secret file formats, local reports, and machine-specific files.
- Hardcoded API-key placeholder in source is replaced with environment-variable lookup.
- Agent and README rules explain where secrets belong.
- Decision log records the secret-handling policy.

## Notes

Completed on 2026-07-08. The ignored root `.env` was updated with empty variable names only.
