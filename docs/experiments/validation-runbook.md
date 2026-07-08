# Validation Runbook

## Purpose

Validate whether the bootcamp project creates real value for Rosso and future agents by turning course material into reusable Avaloka agent capabilities.

First use case:

> Run a minimal agentic RAG loop for Avaloka learning: classify intent, retrieve evidence, decide next step, respond, save trace, and evaluate behavior.

## Current Stage

validation / learning system setup

## Success Criteria

- Each weekly note extracts at least one agent capability.
- First lab records agent traces.
- At least 10 eval cases cover retrieval, decision, memory, safety, and tone.
- Memory scope policy exists before richer memory retrieval.
- New agents can recover current direction from `README.md`, `AGENTS.md`, and `docs/`.

## Non-Goals

- Production deployment.
- Full GraphRAG.
- Full long-term memory system.
- Multi-agent swarm tooling.
- Medical diagnosis or crisis-treatment behavior.

## Participants / Test Subjects

Primary participant:

- Rosso using this project during the bootcamp.

Secondary test subject:

- A future agent asked to continue the work from repository docs only.

Boundary notes:

- Do not use real private user care memories in early tests.
- Use synthetic or project-approved examples until memory scope rules are defined.
- Treat safety failures as product failures, not prompt polish.

## Test Protocol

1. Pick one bootcamp concept or lab.
2. Extract the agent capability it unlocks.
3. Add or update one eval case.
4. Run or simulate one trace.
5. Record what evidence was retrieved, what decision was made, and what failed.
6. Update tasks or decisions if direction changed.

## Daily / Session Record

| Date | Source | Real use or test use | Trigger/context | Outcome score | Best moment | Failure/confusion | Wants to continue |
|---|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |  |

## Decision Rules

Continue if:

- the loop produces inspectable traces
- evals reveal useful failures
- safety and memory boundaries hold
- the course notes become easier for future agents to use

Pause or pivot if:

- project docs drift back into plain retrieve-and-answer RAG
- memory use is unclear or unsafe
- evals are skipped
- agents cannot recover direction from active docs
