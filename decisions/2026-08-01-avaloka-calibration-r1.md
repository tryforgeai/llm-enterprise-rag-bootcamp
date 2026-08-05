# Make Avaloka Calibration R1 The Next Execution Slice

Status: accepted

Date: 2026-08-01

## Context

Week 06 established the trust architecture: request-side gates, response-side grounding, useful refusal, and humble partial answers. Week 07 and Week 08 turned that architecture into measurement: build a domain gold set, measure retrieval with Recall/MRR/nDCG, measure generation with claim-level grounding, and calibrate abstention instead of trusting model self-reported confidence.

Avaloka already has a deterministic Memory Reader V0, scoped memory concepts, guardian review, and behavior evals, but it still lacks a fixed domain EVAL set, formal retrieval metrics, claim-level personal-memory grounding, and calibrated "I don't know" behavior. Adding embeddings, rerankers, RAPTOR, or GraphRAG before those measurements would violate the existing evidence-driven architecture decision.

## Decision

Make **Avaloka Calibration R1** the next execution slice.

The slice will establish the smallest measurable loop that lets Avaloka prove when it should answer, ask, abstain, refuse, or escalate:

1. Build a domain gold EVAL set for Care Card / memory-reader behavior.
2. Benchmark Memory Reader V0 before adding retrieval infrastructure.
3. Add unknown / abstention cases that measure whether Avaloka can avoid unsupported personal-memory claims.
4. Add Baifa / Dharma boundary cases that measure whether Avaloka avoids karma blame, spiritual bypass, unsupported authority, and unsafe religious overreach.
5. Define a calibration trace contract that records retrieval evidence, decision reasons, Baifa / Dharma boundary signals, grounding status, and answerability signals.
6. Use measured failures to choose the smallest justified next component.

Avaloka will not add GraphRAG, RAPTOR, a vector database, a learned reranker, or fine-tuning as part of this slice unless the Memory Reader baseline shows a specific failure class and the proposed component names its expected metric improvement, cost, comparison baseline, and removal criterion.

## Consequences

- The immediate work shifts from course-note capture to a measurable Avaloka evaluation scaffold.
- T008 becomes the active anchor task; T002 receives the first eval-case structure needed by T008.
- The first artifacts are schemas, rubrics, seed cases, and trace templates, not advanced retrieval infrastructure.
- Public benchmarks remain sanity checks only; Avaloka's own Care Card query distribution is the production-relevance authority.
- "Confidence" must be derived from retrieval, grounding, freshness, permission, and risk signals rather than model self-report.
- A system that over-refuses is still wrong; abstention metrics must be paired with over-refusal checks on answerable cases.

## Affected Files

- `docs/decisions/decision-log.md`
- `decisions/index.md`
- `decisions/2026-08-01-avaloka-calibration-r1.md`
- `PROJECT_PLAN.md`
- `tasks/index.md`
- `tasks/T002-first-agentic-rag-evals.md`
- `tasks/T008-benchmark-avaloka-memory-reader.md`
- `evals/avaloka-memory-reader-v0/`
- `evals/avaloka-unknown-calibration-v0/`
- `evals/avaloka-baifa-dharma-boundary-v0/`
- `templates/calibration-agent-trace.json`

## Follow-Up Checks

- Replace seed case placeholders with real Avaloka memory IDs before claiming a runnable Memory Reader baseline.
- Run Memory Reader V0 on the labeled set and publish Recall@5, MRR, nDCG@5, no-match precision, stale leakage, unsafe leakage, and latency.
- Add at least five traced failures before proposing embeddings, reranking, GraphRAG, or RAPTOR.
- Keep one held-out set controlled by the evaluation owner to avoid Goodhart overfitting.
