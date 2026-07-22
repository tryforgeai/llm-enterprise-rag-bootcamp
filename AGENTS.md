# Agent Operating Rules

This project is agent first. Every agent working in this folder must preserve the project's learning trail, not just edit files.

## Startup Sequence

At the start of a session:

1. Read `README.md`.
2. Read `docs/product/product-vision.md`.
3. Read `docs/product/version-roadmap.md`.
4. Read `docs/decisions/decision-log.md`.
5. Read `docs/knowledge/gotchas.md` and `docs/knowledge/fix-log.md`.
6. Read `PROJECT_PLAN.md` for the working plan.
7. Read `tasks/index.md` before proposing or doing new work.
8. Inspect the specific course, lab, eval, trace, or application files related to the current task.

If context gets compacted or the work starts to drift, reread this file and `PROJECT_PLAN.md`.

## Source Of Truth

- Product/project direction: `docs/product/product-vision.md`
- Current version and scope: `docs/product/version-roadmap.md`
- Decision authority: `docs/decisions/decision-log.md`
- Working plan: `PROJECT_PLAN.md`
- Operating rules: `AGENTS.md`
- Detailed decisions: `decisions/`
- Active gotchas and important fixes: `docs/knowledge/`
- Work queue: `tasks/`
- Course notes: `course/`
- Labs and implementation plans: `labs/`
- Agent traces: `traces/`
- Eval cases and results: `evals/`
- Avaloka mappings: `avaloka-applications/`
- Historical material: `archive/`

## Secret Handling

Never commit API keys, access tokens, passwords, private certificates, service account files, or machine-specific `.env` files.

Use the root `.env` file for real secret values and local machine paths. Keep `.env.example` committed with variable names only. If a lab needs credentials, read them from environment variables loaded from `.env`; do not hardcode placeholder keys in source code.

Before committing, run a secret check:

```bash
git status --short
git ls-files '*.env' '.env.*' '**/.env' '**/.env.*'
git grep -n -E 'AKIA|sk-[A-Za-z0-9_-]{20,}|ghp_|github_pat_|xox[baprs]-|api_key\s*=\s*["'\''][^"'\'']+["'\'']|token\s*=\s*["'\''][^"'\'']+["'\'']' -- ':!*.md' ':!*.json' ':!*.lock' ':!*.ipynb'
```

## Agent-First Loop

Use this loop as the default frame:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

Every substantial note, lab, review, or implementation should make clear what the agent can perceive, retrieve, decide, do, trace, or evaluate after the work.

## Planning Rule

Do not jump straight from idea to implementation when the task changes project direction or architecture. First update the relevant source-of-truth doc, plan, task, decision, or template so the reasoning survives future sessions.

Small note additions can be direct edits.

## Task Rule

Use `tasks/index.md` as the lightweight task queue. Before creating a new task, check whether an existing task already covers it.

Task status values:

- `todo`
- `doing`
- `blocked`
- `done`
- `dropped`

When finishing meaningful work, update the relevant task status or add a follow-up task.

## Decision Logging Rule

Before finishing any work that changes project direction, architecture, scope, safety policy, evaluation strategy, memory policy, learning priorities, or folder structure, update the decision log.

Use `docs/decisions/decision-log.md` as the authoritative running log. Create a detailed file in `decisions/` when the change is important enough that future work should understand the reason.

## What Counts As Important

Record a decision when the work:

- changes the project goal or learning priority
- changes the agent-first architecture or loop
- changes safety, privacy, memory, or guardrail policy
- changes eval strategy or success criteria
- adds, removes, or renames major folders or recurring templates
- chooses a technical stack, model family, vector store, framework, or workflow
- rejects an attractive alternative, such as delaying GraphRAG

Small typo fixes, formatting-only edits, and routine note additions do not need a new decision entry.

## Trace And Eval Rule

Labs that simulate or implement agent behavior should save or reference:

- the user question or intent
- retrieved evidence
- decision made by the agent
- response or action
- safety and memory considerations
- eval result or follow-up note

Use `templates/agent-trace.json` and `templates/eval-case.md` when starting from scratch.

## Decision File Format

Use this naming pattern:

```text
decisions/YYYY-MM-DD-short-title.md
```

Each file should include:

- status: proposed, accepted, superseded, or rejected
- date
- context
- decision
- consequences
- affected files
- follow-up checks

## End-Of-Turn Checklist

Before final response:

1. Check whether the work changed an important project decision.
2. If yes, update `docs/decisions/decision-log.md`.
3. If the decision is new or materially changed, create or update a detailed decision file in `decisions/`.
4. Check whether `tasks/index.md` needs an update.
5. Mention decision or task log updates in the final response.
