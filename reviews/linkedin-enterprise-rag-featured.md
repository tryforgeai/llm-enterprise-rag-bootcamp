# Building Trustworthy Enterprise RAG and AI Agents

## Rosso Han

Engineering Leader | Applied AI, RAG, Agent Systems, Cloud Platforms

I build AI systems that move beyond promising demos: systems that retrieve permitted
evidence, make bounded decisions, leave useful traces, and improve through evaluation.

## The Enterprise Problem

Enterprise knowledge is fragmented across documents, operational systems, team context,
and changing policies. A fluent answer is not enough.

A useful enterprise AI system must:

- retrieve the right evidence within permission boundaries
- decide when to answer, ask, abstain, refuse, escalate, or use a tool
- expose provenance, uncertainty, and failure paths
- protect private and stale information
- measure quality before adding architectural complexity

RAG is not the product. It is the evidence layer inside an observable agent loop.

## Agent-First Architecture

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```

### Intent

Classify the request, task, risk, and allowed knowledge scope.

### Retrieve

Find permitted evidence using the smallest measurable retrieval strategy.

### Decide

Choose a bounded next step: answer, ask, retrieve again, abstain, refuse, escalate, or
use a tool.

### Respond

Generate a useful answer grounded in selected evidence and explicit policy.

### Trace

Record evidence, decisions, model and prompt versions, latency, and safety outcomes.

### Evaluate

Measure retrieval, grounding, decision quality, safety, privacy, tone, latency, and cost.

## Trust Requires More Than Retrieval

### Evaluation

- Retrieval: Recall@k, MRR, NDCG, no-match precision
- Grounding: claim support, contradiction rate, citation correctness
- Agent behavior: correct answer, ask, abstain, refuse, escalate, or tool-use decision
- Operations: latency, token cost, retries, cache quality

### Governance

- authenticate and authorize before private retrieval
- scope evidence by user, tenant, source version, and policy
- preserve provenance and freshness
- keep human approval for consequential actions
- provide repair and deterministic fallback paths

### Architecture Discipline

Start with the smallest complete and observable baseline. Add embeddings, hybrid search,
reranking, RAPTOR, or GraphRAG only when a named failure and fixed evaluation justify
the added cost.

## Evidence From The Work

### Demonstrated

- Built a mixed-format RAG knowledge system for Markdown, Excel, and Word documents,
  with 487 indexed chunks, persistent vector retrieval, and grounded generation.
- Built a nine-node AI automation workflow connecting CRM data, model reasoning,
  workflow updates, and notifications.
- Built Avaloka AI capabilities for risk routing, response planning, guardian review,
  repair, safe fallback, evidence-backed memory, diagnostics, and behavior evals.
- Verified 77 Avaloka AI tests and 200 Auralith tests on June 8, 2026.

### Active Experiments

- Normalize end-to-end agent traces.
- Benchmark deterministic memory retrieval using Recall@5, MRR, and NDCG@5.
- Add retrieval components only for measured semantic, ranking, or relationship failures.
- Connect final response claims to permitted evidence and verification status.

## Professional Focus

I bring together engineering leadership, distributed systems, AWS and event-driven
architecture, Applied AI, retrieval, guardrails, evaluation, and operational reliability.

My goal is practical: help teams turn enterprise knowledge and workflows into AI systems
that are measurable, governable, and dependable in real use.

LinkedIn: https://www.linkedin.com/in/rossohan/

