# Curriculum Weaver Lite

Status: Step 1 UI demo

Curriculum Weaver Lite is a pedagogy-first course project demo. It shows how a tutoring system can turn a student's goal and background into a prerequisite-aware learning path.

The first demo focuses on one topic:

> Learn self-attention mathematically.

This version uses static data only. It intentionally avoids backend RAG, vector databases, PDF ingestion, and agent frameworks so the learning experience can be reviewed first.

## Demo Flow

1. Choose a student profile.
2. Review diagnostic answers and mastery estimates.
3. Generate a prerequisite-aware learning path.
4. Open a lesson with source cards and a code sketch.
5. Take a short quiz.
6. Watch the learner model update.

## Current Scope

- Static concept graph for self-attention.
- Three learner profiles: beginner, intermediate, advanced.
- Source-grounded lesson cards.
- Diagnostic and quiz simulation.
- Trace panel showing why each step was selected.

## Source Of Truth

- `docs/product/product-vision.md` defines the long-term project vision.
- `docs/product/project-proposal.md` is the presentation proposal for the whole course project.
- `docs/product/version-roadmap.md` defines Step 1 and Step 2 scope.
- `docs/decisions/decision-log.md` records accepted direction changes.
- `docs/product/quality-checklist.md` defines demo quality gates.

## Deferred Step 2 Scope

- Content ingestion from PDFs, papers, notes, and notebooks.
- Hybrid retrieval with BM25 and embeddings.
- Student memory / knowledge tracing.
- LLM lesson synthesis.
- Quiz generation and grading.
- RAG and pedagogy evaluation dashboard.
- Browser and UI test coverage.

## Run

Open `index.html` in a browser.

For local HTTP testing:

```bash
python3 -m http.server 4177
```

Then open `http://127.0.0.1:4177`.
