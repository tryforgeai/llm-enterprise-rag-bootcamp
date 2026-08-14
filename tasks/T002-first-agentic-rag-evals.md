# T002 First Agentic RAG Evals

Status: doing

Completed: 2026-08-14

## Goal

Create the first 10 eval cases for the minimal agentic RAG lab.

## What Was Built

Ten JSON cases in `evals/cases/`, a dependency-free runner at `evals/run_evals.py`, an adversarial fixture in `evals/fixtures/`, and a first measured baseline in `evals/results/`.

Actual split, wider than the original plan because Weeks 06 to 09 added guardrail and evaluation material:

- 4 retrieval cases, including one multi-hop case (EV-001 to EV-004)
- 2 abstention cases, one easy and one hard negative (EV-005, EV-006)
- 1 ambiguity/clarification case (EV-007)
- 1 indirect prompt-injection case (EV-008)
- 1 personal-data and memory-scope case (EV-009)
- 1 tool-use case (EV-010)

No tone or compassion case yet. Tone scoring needs a generator in the loop, which this baseline does not have.

## Done Criteria

- Eval cases live in `evals/`.
- Each case includes expected evidence, expected decision, safety concerns, and pass/fail criteria.
- The lab plan links to the eval set.

## Calibration R1 Seed Artifacts

- `evals/avaloka-memory-reader-v0/cases.seed.jsonl`
- `evals/avaloka-unknown-calibration-v0/cases.seed.jsonl`
- `evals/avaloka-baifa-dharma-boundary-v0/cases.seed.jsonl`

These are draft seed cases. They must be labeled with real Avaloka memory IDs before they become a runnable benchmark.

- [x] Eval cases live in `evals/`.
- [x] Each case includes expected evidence, expected decision, safety concerns, and pass/fail criteria.
- [x] The runner produces retrieval, decision, safety, and NRR metrics.
- [x] Each run writes one trace per case to `traces/<run_id>/`.
- [ ] The lab plan links to the eval set. Follow-up when `labs/01-minimal-rag-demo-plan.md` is turned into a runnable loop (T004).

## First Result

6 of 10 pass. Mean recall@5 0.333, nDCG@5 0.377, MRR 0.600, decision accuracy 0.900, safety pass rate 0.900, NRR 0.667.

Failures became T025 (EV-001, EV-002, and EV-008 retrieval) and T026 (EV-006 abstention).

## Verification Findings

A verification pass on the same day found and fixed two bugs that had made the first reported result look better than it was:

- `nDCG@k` capped the ideal ranking by results returned instead of by `k`, inflating scores on sparse queries.
- The `ground` decision read `min_distinct_evidence` from the case file, leaking the expected answer into the decision policy. EV-004's correct decision was guaranteed by its own config. Multi-hop intent is now detected from the question text; the decision function no longer sees the case file at all.

A third finding was that `pass_criteria` strings were never evaluated, so EV-002 declared a 0.4 recall bar, scored 0.333, and was reported as passing. Numeric bars now live in enforced `min_recall_at_k` and `min_distinct_evidence` fields. This is what moved the headline from 7/10 to 6/10.

## Follow-Ups

- T003 memory scopes needs its own case file once Avaloka memory records exist; EV-009 is only a stand-in.
- Week 08 generator metrics (FActScore, ECE, RAGAS faithfulness) are not implemented and need a model in the loop.
