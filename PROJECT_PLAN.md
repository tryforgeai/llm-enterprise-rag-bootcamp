# Project Plan

## Mission

Use the SupportVectors LLM and Enterprise RAG Bootcamp to upgrade Avaloka AI into an agent-first system that can retrieve the right context, make safe next-step decisions, preserve useful traces, and improve through evals.

Authoritative direction lives in:

- `docs/product/product-vision.md`
- `docs/product/version-roadmap.md`
- `docs/decisions/decision-log.md`

## Current Strategy

Do not treat RAG as the product. Treat RAG as the evidence and memory substrate inside an agent loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

The course is useful when each concept becomes at least one of:

- agent behavior rule
- retrieval strategy
- memory schema
- safety or privacy guardrail
- eval case
- trace field
- implementation experiment
- instructor question

## Near-Term Milestone

Complete the Week 01 learning capture, then build and understand one minimal agentic RAG loop.

Minimum loop:

```text
question
-> classify intent and risk
-> retrieve relevant evidence
-> decide next step: answer, ask, refuse, ground, escalate, or use tool
-> generate response
-> save trace
-> evaluate retrieval, decision, safety, and tone
```

## Non-Goals For Now

- Do not start with GraphRAG.
- Do not build a full production memory system.
- Do not optimize infrastructure before the trace and eval loop exists.
- Do not add hidden complexity that makes the learning loop hard to inspect.

## Architecture Escalation Rule

Start with the smallest complete and observable baseline. Add a component only after traces or evals show a specific failure and the proposal names:

- the failure being addressed
- the metric expected to improve
- latency, token, maintenance, safety, and privacy costs
- the comparison baseline
- the removal criterion if improvement does not appear

RAPTOR, GraphRAG, and fine-tuning are available interventions, not default milestones.

## Success Criteria

The project is working when:

- weekly notes extract agent capabilities, not only concepts
- labs produce traces, not only answers
- evals test behavior and safety, not only retrieval correctness
- decisions explain why directions changed
- Avaloka mappings show what the course unlocks in the real product

## Operating Rhythm

For each course week:

1. Capture lecture concepts and code notes in `course/`.
2. Record questions while they are still fresh.
3. Extract one agent capability.
4. Add or update one eval case.
5. Add or update one Avaloka application mapping.
6. Update `tasks/index.md` with the next concrete lab action.
7. Record any important direction change in `docs/decisions/decision-log.md`.
