# Agent-First Project Direction

Status: accepted

Date: 2026-06-01

## Context

The project began as a learning system for the SupportVectors LLM and Enterprise RAG Bootcamp. The early structure focused on embeddings, retrieval, GraphRAG, guardrails, evals, and applying those ideas to Avaloka AI.

That is useful, but Avaloka AI needs these course concepts to become agent capabilities: perceiving intent, retrieving memory and knowledge, choosing safe next steps, using tools, saving traces, and improving through evals.

## Decision

Treat the project as agent-first.

RAG is not the final product. RAG is the evidence and memory substrate inside an agent loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

Every meaningful course note, lab, and application mapping should identify what agent capability it unlocks.

## Consequences

- Course notes must include agent capability, required evidence, memory, tools, and evals.
- Labs should save agent traces, not only retrieval traces.
- Evals should measure behavior choice, safety, tone, and memory use, not only retrieval correctness.
- GraphRAG should wait until traces reveal graph-shaped failure modes.

## Affected Files

- `README.md`
- `course/00-course-overview.md`
- `course/week-01.md`
- `prep/01-before-class-plan.md`
- `labs/01-minimal-rag-demo-plan.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `questions/instructor-questions.md`
- `resources/glossary.md`
- `reviews/01-agent-first-project-review.md`

## Follow-Up Checks

- Each weekly note should answer: what can an agent perceive, retrieve, decide, or do after this lesson?
- Each lab should produce a trace with retrieved evidence, decision, response, and eval results.
- Each review should check whether the work is drifting back into plain retrieve-and-answer RAG.
