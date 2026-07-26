# Product Vision

## Project

LLM and Enterprise RAG Bootcamp

## Final Vision

Use the SupportVectors LLM and Enterprise RAG Bootcamp to turn Avaloka AI into an agent-first system that can retrieve evidence, use memory safely, choose bounded next steps, save traces, and improve through evaluation.

The course is not only a learning archive. It is the project operating system
for extracting reusable agent capabilities from every lecture, lab, reading,
and instructor question, and for publishing those capabilities as a portable
method toolkit that can be adopted by future projects.

## Long-Term Target User

Primary user: Rosso, building Avaloka AI and related agent systems.

Secondary user: future coding or research agents that need to understand project direction without relying on chat history.

## Long-Term Problem

Avaloka needs more than plain LLM responses. It needs a disciplined loop for deciding when to retrieve, when to use memory, when to ask, when to refuse, when to escalate, and how to evaluate the outcome.

Without a visible project scaffold, course notes can become scattered context that future agents cannot reliably use.

Avaloka is not a greenfield RAG system. It already appears to embody many course principles through product behavior and safety design, even where it does not use the newest named techniques. The project should formalize and evaluate those existing capabilities before replacing them.

## First Use Case

Build a minimal agentic RAG learning loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

The first loop should use a small Avaloka knowledge base, save agent traces, and evaluate retrieval quality, decision quality, safety, memory use, and tone.

## Permanent Non-Goals

- Do not treat RAG as the final product.
- Do not start with GraphRAG before simple traces reveal graph-shaped needs.
- Do not build a production memory system before memory scope rules exist.
- Do not expose raw private memory in generated responses.
- Do not make medical, diagnostic, or crisis-treatment claims.
- Do not let archived or old chat context override active docs.

## Product Principles

- Agent behavior matters more than demo answers.
- Existing Avaloka behavior is the baseline, not an implementation to discard.
- Formal terminology and newer infrastructure do not automatically imply better product behavior.
- Retrieval must support safe decisions, not just fluent generation.
- Every important decision should leave a durable trace in docs.
- Evals should test behavior, safety, memory use, and tone.
- Keep the smallest loop inspectable before adding complexity.

## Safety / Quality / Taste Boundaries

Avaloka-related work must preserve warmth while staying bounded:

- no medical diagnosis
- no karma blame
- no spiritual bypass
- no crisis minimization
- no hidden prompt disclosure
- no raw private memory exposure
- no overclaiming course-derived capabilities before eval evidence exists

## What Would Make This A Success

- Each weekly note identifies an agent capability unlocked by the lesson.
- The first lab produces trace records, not only answers.
- At least 10 eval cases cover retrieval, decision, memory, safety, and tone.
- Memory scopes are explicit before richer memory retrieval.
- Active project direction can be recovered from `README.md`, `AGENTS.md`, and `docs/`.
- Future projects can select and adopt course methods through `toolkit/` without
  depending on this repository's machine paths, secrets, vendors, or application
  assumptions.
