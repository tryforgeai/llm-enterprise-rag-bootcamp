---
type: Index
title: RAG Bootcamp Practice Bundle — Week 06/07/08 Concepts (English)
description: Ten practice OKF concept cards, re-binding Week 06 guardrails and Week 07/08 evaluation metrics as knowledge objects with provenance and trust tiers.
---

# RAG Bootcamp Practice Bundle (English)

This is a practice knowledge bundle that rewrites the evaluation metrics and guardrail mechanisms from earlier weeks as concept cards, following the Open Knowledge Format (OKF) spec covered in Week 09.

## Metrics (from Week 07 / Week 08)

- [NDCG@5](metrics/ndcg-at-5.md) — retrieval ranking quality (Week 07)
- [Recall@5](metrics/recall-at-5.md) — retrieval coverage (Week 07)
- [MRR](metrics/mrr.md) — rank of the first relevant result (Week 07)
- [RAGAS Faithfulness](metrics/ragas-faithfulness.md) — how faithful a generated answer is to retrieved context (Week 08)
- [FActScore](metrics/factscore.md) — claim-level factual precision (Week 08)
- [ECE](metrics/ece.md) — expected calibration error (Week 08)
- [NRR](metrics/nrr.md) — negative rejection rate (Week 08)

## Guardrails (from Week 06)

- [Response Grounding Gate](guardrails/response-grounding-gate.md) — output-side grounding / negative-rejection gate
- [PII Redaction Guardrail](guardrails/pii-redaction.md) — personal-information redaction
- [Indirect Prompt Injection Defense](guardrails/indirect-prompt-injection-defense.md) — defense against instructions smuggled in retrieved content

## Note

All ten cards below are **drafts** — the `generated` field is stamped as authored by an agent from class notes, and `verified` is empty, so the trust tier for every card currently sits at **unverified**. Per the rules covered today, that is the honest state to be in: you should check each card's formulas, thresholds, and sources yourself, then add a `human:rosso` entry to `verified` once confirmed — only then does a card actually graduate to human-reviewed.
