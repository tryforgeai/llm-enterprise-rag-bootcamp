# Version Roadmap

## Version Authority

This document defines current and future versions. If it conflicts with older plans, follow the latest accepted decision in `docs/decisions/decision-log.md`.

## Current Active Version

| Field | Value |
|---|---|
| Version | v0.1 agent-first bootcamp scaffold |
| Stage | active course / Week 07; evaluation baseline in progress |
| Target user | Rosso building Avaloka AI with future agent assistance |
| First use case | Minimal agentic RAG loop for Avaloka course learning |
| Success criteria | Active docs and course artifacts are current through Week 07, while the first reusable trace, eval set, retrieval baseline, and Avaloka memory policy close the v0.1 agent-first loop. |

### Current Progress Snapshot

Course execution has advanced beyond the original scaffold scope, but the version remains v0.1 because its agent-first exit criteria are not yet complete.

Completed or materially demonstrated:

- Week 01 through Week 07 learning capture, with Week 02, Week 06, and Week 07 follow-ups still open.
- Week 03 representation experiments covering chunking, contextual chunks, page-image retrieval, text retrieval, and comparison tests.
- Week 04 derived retrieval artifacts covering raw chunks, propositions, QA pairs, summaries, embeddings, and the Xennials FactoidWiki demo.
- Week 05 graph-shaped learning artifacts.
- Week 06 request rails, ACL-bound retrieval, indirect-injection defenses, response grounding, abstention, and a runnable mocked Project Atlas pipeline.
- Week 07 evaluation capture plus runnable nDCG, precision-recall, and reranking evaluation demos.
- Curriculum Weaver Lite Step 1 static pedagogy-first UI demo.
- Clone-portable locked verification for Week 03 Python tests and the Curriculum Weaver browser smoke test.
- Cross-project method toolkit covering all methods taught or demonstrated
  through Week 07, with stable IDs, evidence links, maturity labels, and an
  adoption template.

Still required to close v0.1:

- Create the first 10 agentic RAG eval cases.
- Define Avaloka memory scopes and use rules.
- Save at least one canonical agent trace under `traces/`.
- Turn the minimal agentic RAG plan into a runnable trace-and-eval loop.
- Benchmark Avaloka Memory Reader V0 before selecting a retrieval upgrade.

### In Scope

- Agent-readable project scaffold.
- Week 01 through Week 07 lecture, code, question, and application capture, including explicit follow-ups where live-class or eval evidence is incomplete.
- Verified SupportVectors Python classroom environment.
- Product vision and version governance.
- Decision log and document gardening rules.
- Minimal agentic RAG lab plan.
- Trace and eval templates.
- First tasks for evals, memory scope policy, and demo implementation.
- Audit of existing Avaloka capabilities against Week 01 concepts.
- Week 03 representation and retrieval experiments.
- Week 04 derived-artifact retrieval experiments.
- Week 05 graph-shaped learning artifacts.
- Week 06 guardrail, grounding, refusal, and humility architecture walkthroughs.
- Week 07 retrieval and generation evaluation methods and runnable metric demos.
- Portable method catalog and project-adoption template.
- Curriculum Weaver Lite Step 1 UI demo and Step 2 proposal.

### Out of Scope

- Production deployment.
- Full GraphRAG implementation.
- Full Avaloka long-term memory system.
- Multi-agent swarm coordination tooling.
- Medical or crisis-support product claims.

### Exit Criteria

- `agent-first-project-bootstrap` audit passes or only reports accepted false positives.
- `docs/` has no unresolved template placeholders.
- The first 10 agentic RAG eval cases exist in `evals/`.
- Avaloka memory scope policy exists.
- At least one example agent trace exists in `traces/`.

## Next Version

| Field | Value |
|---|---|
| Version | v0.2 first runnable agentic RAG loop |
| Goal | Run a small Avaloka question through intent classification, retrieval, decision, response, trace, and eval. |
| Entry criteria | v0.1 governance is current, the first 10 eval cases and memory-scope policy exist, and at least one canonical trace demonstrates the full loop. |
| Major risks | Overbuilding infrastructure, skipping evals, or using memory without explicit scope rules. |

## Future Versions

| Version | Hypothesis | Do not start until |
|---|---|---|
| v0.3 memory scope and retrieval policy | Memory retrieval can be safe if scopes, permissions, and exposure rules are explicit. | v0.2 trace examples show how memory is used or misused. |
| v0.4 retrieval funnel experiments | Dense retrieval, sparse retrieval, reranking, and safety filtering can improve decision quality. | Baseline evals show retrieval failures worth fixing. |
| v0.5 graph-shaped retrieval | GraphRAG may help connect pain patterns, care memories, principles, and safety boundaries. | 20 to 50 traces reveal repeated graph-shaped failure modes. |

## Deferred Ideas

Ideas listed here are not active commitments.

- Full GraphRAG schema.
- Multimodal audio/video ingestion.
- Production-grade vector database.
- Multi-agent coordination with Beads, Agent Mail, or similar tools.
- Public-facing Avaloka companion behavior.
