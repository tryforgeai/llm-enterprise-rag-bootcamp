# Evidence-Driven Architecture Escalation

Status: accepted

Date: 2026-06-06

## Context

The course introduces increasingly sophisticated retrieval systems, including hybrid retrieval, SAGE-style adaptive selection, RAPTOR, GraphRAG, and fine-tuning. Adding all of them preemptively would increase cost, latency, maintenance burden, and the number of failure modes before Avaloka has a measured baseline.

## Decision

Avaloka and bootcamp labs will begin with the smallest complete and observable architecture. New components may be added only in response to a demonstrated failure in traces or domain-specific evals.

Each proposed component must identify:

- the observed failure
- the eval and metric it should improve
- expected latency, token, maintenance, safety, and privacy costs
- the baseline used for comparison
- the condition under which the component will be removed

Evaluate marginal contribution with a Shapley-style ablation:

```text
baseline -> enable component -> rerun fixed evals -> disable component -> compare deltas
```

Record both quality and operating-cost changes. When components interact, test the most relevant combinations rather than assuming one-at-a-time results tell the complete story.

The default escalation order is:

```text
basic retrieval + safety + trace + eval
-> chunking, embeddings, hybrid retrieval, or reranking
-> adaptive context selection
-> RAPTOR for multi-resolution retrieval
-> GraphRAG for relationship and corpus-structure reasoning
-> fine-tuning only for persistent behavior failures with good evidence
```

This order is guidance, not a requirement to install every layer.

## Consequences

- Course techniques are treated as available interventions, not automatic architecture.
- GraphRAG and fine-tuning remain deferred until eval evidence supports them.
- Every architecture increase must be reversible and measurable.
- Project reviews should challenge components that cannot show a named benefit.
- Component reviews should use fixed eval sets and compare marginal quality against marginal cost.

## Affected Files

- `course/week_01/week-01.md`
- `avaloka-applications/01-avaloka-application-map.md`
- `PROJECT_PLAN.md`
- `docs/decisions/decision-log.md`

## Follow-Up Checks

- Establish a naive retrieval baseline in the minimal agentic RAG lab.
- Record latency, token cost, retrieval quality, grounding, and safety metrics.
- Require an eval failure before promoting RAPTOR, GraphRAG, or fine-tuning into the active plan.
