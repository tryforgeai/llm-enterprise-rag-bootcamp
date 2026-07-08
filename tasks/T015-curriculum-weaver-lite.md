# T015: Curriculum Weaver Lite Course Project

Status: doing

## Goal

Build a course project that demonstrates a pedagogy-first RAG tutor for learning self-attention.

## Why It Matters

This project practices LLM, RAG, learner memory, agent tracing, and evaluation while avoiding a generic chunking-first RAG demo. The central hypothesis is that educational RAG should retrieve the next teachable concept, not merely the nearest chunk.

## Scope

- Step 1 UI demo in `labs/curriculum-weaver-lite/`.
- Whole-project proposal in `labs/curriculum-weaver-lite/docs/product/project-proposal.md`.
- Static concept graph, source cards, learner profiles, diagnostic, learning path, lesson, quiz, and trace.
- Step 2 plan for real ingestion, hybrid retrieval, learner memory, LLM lesson synthesis, quiz evaluation, trace dashboard, and UI tests.

## Done When

- [x] Step 1 UI demo exists and can run locally.
- [x] Proposal covers the full project, not only Step 1.
- [x] Project lives under the Bootcamp `labs/` folder.
- [ ] Instructor feedback is captured.
- [ ] Step 2 module plan is converted into implementation tasks.
- [ ] Real RAG, memory, synthesis, evaluation, and UI tests are implemented or explicitly scoped for final delivery.

## Evidence

- Demo: `labs/curriculum-weaver-lite/index.html`
- Proposal: `labs/curriculum-weaver-lite/docs/product/project-proposal.md`
- Smoke test: `labs/curriculum-weaver-lite/scripts/smoke-test.cjs`

## 2026-06-27 Update

Created a separate proposal review page for instructor/project review:

- added `labs/curriculum-weaver-lite/proposal-review.html` as a standalone review page, separate from the interactive Step 1 demo
- added `labs/curriculum-weaver-lite/proposal-review.css` for the review-page visual system
- kept the existing demo UI/code path separate: `index.html`, `styles.css`, and `app.js` are not the proposal surface
- review page covers thesis, problem, hypothesis, architecture diagram, demo flow, Step 1 scope, Step 2 plan, and review questions
- verified the standalone review page in Chrome at desktop and mobile widths: title renders, architecture diagram is present, 5 flow cards are present, 4 review questions are present, and there are no console errors
