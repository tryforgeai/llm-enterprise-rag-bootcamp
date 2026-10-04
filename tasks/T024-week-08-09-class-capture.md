# T024 Week 08 And Week 09 Class Follow-Ups

Status: doing

Created: 2026-08-14

## Goal

Close the open follow-ups on the two most recent class captures. Both notes were written from lecture decks; the live-session detail and the hands-on labs are still missing.

## Week 08 — Generator Evaluation (2026-08-01)

`course/week_08/week-08.zh.md` covers *The Personal Equation* opening experiments and the five-act *Measure of All Things*, focused on the generator half: judge bias, FActScore, ECE, NRR, RAGAS faithfulness.

Open:

- Live discussion detail from the session.
- Lab implementation. None of the Week 08 generator metrics are implemented anywhere in the repository.
- The eval artifact the week asked for. `evals/` now measures retrieval, decision, and refusal, but no generated text is scored. FActScore, ECE, and faithfulness all need a model in the loop.

## Week 09 — Open Knowledge Format (2026-08-08)

`course/week_09/week-09.zh.md` covers the OKF specification, the governed corpus, and the enterprise entitlement pipeline (ACL, RBAC, ABAC, ReBAC, permission propagation through chunking, the two synchronized pipelines).

Open:

- The *Library in Your Head* prelude is transcribed from partial screenshots only; several of the 31 pages are missing.
- Lab implementation.
- The OKF practice cards in `course/week_09/okf-practice-cards/` were written but never validated against the spec's required fields. See T028 for the duplication problem.

## Agent Capability To Extract

Week 09 produced a design principle the project has now hit three times independently: any governed state must record *when* it was true, not only what it is. It shows up as `generated` versus `verified` timestamps in OKF, as per-request recomputation of the retrievable set, and as versioned entitlement descriptors.

This belongs in the Avaloka memory schema (T003) and in the trace format. A memory record without a verification timestamp cannot answer "was this still true when the agent used it?"

## Done Criteria

- Both notes' status lines reflect what is actually captured.
- At least one Week 08 generator metric is runnable against the eval set.
- The Week 09 timestamp principle is written into the T003 memory scope design.
