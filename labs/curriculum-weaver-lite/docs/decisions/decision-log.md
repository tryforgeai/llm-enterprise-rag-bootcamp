# Decision Log

This file records accepted product, business, architecture, and process decisions.

If documents conflict, follow the newest accepted decision here, then update affected docs.

## Decision Template

```md
## YYYY-MM-DD — Decision Title

Status: Accepted / Superseded / Rejected

### Context

What changed or what question needed a decision?

### Decision

What did we decide?

### Rationale

Why is this the right decision now?

### Consequences

What changes because of this?

### Affected Docs

- 
```

## Initial Decisions

## 2026-06-27 — Establish Agent-First Project Governance

Status: Accepted

### Context

The project needs a clear source-of-truth structure for humans and agents.

### Decision

Use `README.md`, `AGENTS.md`, `docs/product/product-vision.md`, `docs/product/version-roadmap.md`, `docs/decisions/decision-log.md`, validation runbooks, quality checklists, and document gardening as the project governance scaffold.

### Rationale

Agents can only reliably execute what is visible in the repository.

### Consequences

Future meaningful direction changes must update the decision log and affected source-of-truth docs.

### Affected Docs

- `README.md`
- `AGENTS.md`
- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`

## 2026-06-27 — Build Step 1 As A Pedagogy-First UI Demo

Status: Accepted

### Context

The course project needs to practice LLM, RAG, memory, agent, and evaluation ideas, but the first milestone must be quick and visible. Starting with ingestion, embeddings, vector databases, or frameworks would hide the central learning experience behind infrastructure.

### Decision

Build Step 1 as a static UI demo for learning self-attention. The demo shows student profile, diagnosis, prerequisite-aware learning path, lesson source cards, quiz, learner-memory update, and trace.

### Rationale

The main project thesis is pedagogy-first: the system should decide what the learner is ready to understand next before retrieval tries to find material.

### Consequences

Step 1 uses static JSON-like data in `app.js`. Step 2 may replace static components with real RAG, memory, LLM synthesis, evaluation, and tests after the UI flow is accepted.

### Affected Docs

- `README.md`
- `AGENTS.md`
- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `docs/product/quality-checklist.md`
