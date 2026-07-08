# LLM and Enterprise RAG Bootcamp

This project is the learning system of record for the SupportVectors LLM and Enterprise RAG Bootcamp.

The project goal is agent first: every concept should be translated into a capability that helps Avaloka AI perceive context, retrieve memory and knowledge, choose a safe next step, act, observe results, and improve through evals.

## Purpose

Use the bootcamp to build practical capability in:

- vector embeddings
- semantic search
- retrieval-augmented generation
- retrieval funnels
- GraphRAG and RAPTOR-style retrieval
- guardrails
- RAG evaluation
- multimodal ingestion for audio and video
- agentic retrieval, tool use, memory, and evaluation loops
- applying these ideas to Avaloka AI and future agent systems

## Project Rule

Every class note should answer five questions:

1. What did I learn?
2. How would I implement it in code?
3. What agent capability does this unlock?
4. What evidence, memory, tool, or eval does the agent need?
5. How does it apply to Avaloka AI or another real project?

## Secret Handling

Real API keys, access tokens, passwords, private certificates, service account files, and machine-specific paths belong in the ignored root `.env` file.

Use [.env.example](.env.example) as the committed template. Do not commit real secret values.

## Folder Structure

- `AGENTS.md` - operating rules for agents working in this project
- `PROJECT_PLAN.md` - source-of-truth project plan and operating rhythm
- `docs/` - active governance docs for product vision, version roadmap, decisions, validation, quality, and maintenance
- `course/` - course overview, syllabus, schedule, and weekly notes
- `prep/` - pre-course preparation plans and mini labs
- `avaloka-applications/` - mappings from course concepts to Avaloka AI
- `labs/` - coding lab notes, commands, and experiment logs
- `questions/` - questions to ask instructors or TAs
- `resources/` - links, papers, glossary, and reading notes
- `reviews/` - periodic project reviews and next actions
- `decisions/` - durable records of important direction, architecture, eval, memory, and safety decisions
- `tasks/` - lightweight task queue for agent-ready work
- `templates/` - reusable templates for decisions, weekly notes, traces, and eval cases
- `traces/` - saved agent runs and debugging traces
- `evals/` - evaluation cases and results
- `archive/` - historical or superseded docs only

## Decision Log Rule

Important decisions and direction changes must be recorded in `docs/decisions/decision-log.md`. Detailed decision files may also live in `decisions/`.

Add or update a decision when work changes project direction, agent architecture, scope, safety policy, evaluation strategy, memory policy, learning priorities, folder structure, or technical stack.

Routine note additions, typo fixes, and formatting-only edits do not need a decision entry.

## Read First

For humans:

1. `README.md`
2. `docs/product/product-vision.md`
3. `docs/product/version-roadmap.md`
4. `labs/01-minimal-rag-demo-plan.md`

For agents:

1. `AGENTS.md`
2. `docs/product/product-vision.md`
3. `docs/product/version-roadmap.md`
4. `docs/decisions/decision-log.md`
5. `tasks/index.md`

## Current Learning Priority

The course started on June 6, 2026. The current priority is to turn each live class into reusable agent capability:

```text
live class
-> capture concepts and code
-> identify one agent capability
-> add one Avaloka application
-> create or update one eval case
-> choose the next concrete lab task
```

Use `course/week-01.md` during or immediately after the first class.

Chinese version: `course/week-01.zh.md`.
