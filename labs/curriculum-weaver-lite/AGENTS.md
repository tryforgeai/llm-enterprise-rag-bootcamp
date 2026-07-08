# AGENTS.md

This folder is a self-contained course-project demo for The Curriculum Weaver.

## Current Direction

Build a fast UI demo first, then replace static intelligence with real RAG, memory, evaluation, and tracing.

Current version:

- `Step 1`: static pedagogy-first UI demo for learning self-attention.

Next version:

- `Step 2`: full module implementation with ingestion, retrieval, student memory, LLM synthesis, quiz evaluation, trace dashboard, and tests.

## Required Reading

1. `README.md`
2. `docs/product/product-vision.md`
3. `docs/product/version-roadmap.md`
4. `docs/decisions/decision-log.md`
5. `docs/product/quality-checklist.md`
6. `index.html`
7. `styles.css`
8. `app.js`

## Version Authority

If documents conflict, follow:

1. newest accepted decision in `docs/decisions/decision-log.md`
2. current active version in `docs/product/version-roadmap.md`
3. final boundaries in `docs/product/product-vision.md`
4. implementation files

## Non-Goals For Step 1

- No full PDF ingestion.
- No production backend.
- No vector database.
- No multi-agent framework.
- No broad ML curriculum.
- No commercial positioning.

## Agent Workflow

- Keep Step 1 focused on the visible student learning experience.
- Do not add heavy infrastructure before the demo flow works.
- Preserve source-grounded lesson cards and learner-model traceability.
- When adding Step 2 modules, include tests for prerequisite ordering, source attribution, UI flow, and quiz/mastery updates.
