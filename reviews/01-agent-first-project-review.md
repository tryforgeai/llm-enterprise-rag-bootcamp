# Agent-First Project Review

Date: 2026-06-01

## Verdict

The project has a strong RAG learning spine, but it is not yet agent first. Right now the docs optimize for understanding embeddings, retrieval, GraphRAG, guardrails, and evals. That is useful, but Avaloka AI needs those topics to become an agent loop: sense intent, retrieve memory and knowledge, choose a safe action, produce or call something, observe the result, and improve through traces and evals.

The best next move is not to add complexity. Keep the first implementation tiny, but make it agent-shaped from day one.

## What Is Working

- The project has a concrete product anchor: Avaloka AI.
- The learning goal is practical, not abstract.
- The current RAG loop is small enough to build before class.
- Safety, memory, and evals are already treated as first-class topics.
- The instructor questions are strong and domain-specific.

## Main Gap

The current structure asks, "How do I build RAG?"

The agent-first structure should ask, "What does this let an agent do better?"

That changes the project from a course notes archive into a capability extraction system. Each week should produce at least one reusable artifact for Avaloka:

- agent behavior rule
- retrieval strategy
- memory schema
- eval case
- guardrail
- trace format
- tool boundary
- failure example

## Highest-Risk Issues

### 1. RAG can become the product instead of the agent substrate

If every lab stops at "retrieve chunks and answer," the project will miss the agent design layer. Avaloka does not just need answers. It needs decisions about when to use memory, when to ignore memory, when to ask a clarifying question, when to trigger a safety boundary, and when to decline.

Fix: every lab should include an agent decision field, not only retrieved evidence.

### 2. The first lab lacks action and observation

The current minimal RAG demo has load, chunk, embed, retrieve, answer, and trace. That is a good RAG loop, but an agent needs at least one decision point and one observation point.

Fix: add intent classification, next-step choice, safety decision, response, trace, and eval.

### 3. Evals are framed around retrieval quality more than agent behavior

Retrieval correctness is necessary, but Avaloka needs behavioral evals:

- Did the agent use memory only when appropriate?
- Did the agent avoid exposing raw private memory?
- Did it choose ask, answer, refuse, ground, or escalate correctly?
- Did it sound caring without overclaiming?
- Did it cite or summarize evidence faithfully?

Fix: maintain two eval tables: retrieval evals and agent behavior evals.

### 4. Memory needs explicit permission and freshness rules

The docs mention care memories and private memory exposure, but there is not yet a policy for which memories can be retrieved, shown, summarized, updated, or forgotten.

Fix: define memory scopes before building richer retrieval.

### 5. GraphRAG is tempting but premature

The graph ideas are directionally right. The risk is building schema before the simplest agent trace proves what relationships matter.

Fix: collect 20 to 50 traces first. Let the graph schema emerge from repeated failures and useful joins.

## Agent-First Target Loop

```text
user input
-> classify intent, risk, and emotional state
-> retrieve candidate memories, knowledge, safety rules, and prior failures
-> decide next step: answer, ask, ground, refuse, escalate, or use tool
-> generate response with limited evidence
-> guardian review
-> save trace
-> eval retrieval, behavior, safety, and tone
```

## Recommended Project Structure

Keep the current folders, but make their outputs more explicit:

- `course/`: notes plus "agent capability unlocked"
- `prep/`: setup tasks for the first agent loop
- `labs/`: runnable loops, traces, eval logs, and failure cases
- `avaloka-applications/`: architecture decisions and product mappings
- `questions/`: instructor questions grouped by agent capability
- `resources/`: glossary plus patterns worth reusing
- `reviews/`: periodic project reviews and next actions

## Next Seven Actions

1. Rename the first lab mentally from minimal RAG to minimal agentic RAG.
2. Add an agent trace schema before writing code.
3. Create 10 eval cases split across factual retrieval, safety, memory use, and behavior choice.
4. Define allowed memory scopes: public source, internal project note, user care memory, sensitive private memory, forbidden memory.
5. Add one decision policy: when should Avaloka answer, ask a question, refuse, or escalate?
6. During each lecture, extract one "agent rule" and one "eval case."
7. Delay GraphRAG until there are real traces showing graph-shaped failure modes.

## Review Score

Current state: 6.5/10 for agent-first readiness.

The foundation is good. The missing piece is converting every RAG concept into an agent behavior, trace, or eval. Once the first lab records decisions and failures, the project becomes much more valuable.
