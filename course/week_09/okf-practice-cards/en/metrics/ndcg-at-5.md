---
type: Metric
title: NDCG@5
description: Normalized Discounted Cumulative Gain — measures whether the relevant documents in the top 5 retrieved results are ranked near the top, i.e. ranking quality rather than mere presence.
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, ranking, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# NDCG@5

## Definition

NDCG (Normalized Discounted Cumulative Gain) weights the top 5 retrieved results so that relevant documents ranked higher contribute more, with a logarithmic discount for lower ranks, then normalizes against the maximum possible gain under a perfect ranking — yielding a score between 0 and 1.[^week07-lesson]

## Why Recall alone isn't enough

Recall@5 only asks whether relevant documents made it into the top 5 — it doesn't care whether a hit landed at position 1 or position 5. NDCG@5 cares about **order**: for downstream systems that only pass the first few chunks into the prompt, a hit at rank 1 versus rank 5 has very different practical value. This is exactly why the six-metric ladder climbs from precision/recall up to NDCG.[^week08-notes]

## Where it's used

- One of the core optimization targets when fine-tuning a reranker.
- Read alongside RAGAS Context precision: low NDCG but high generator-side FActScore usually means "the generator can cope — the reranker is starving it." See Week 08's Evaluation Map stress-test reading rules.[^week08-notes]

## Points still needing human verification

- [ ] The exact discounted-gain formula ($\text{DCG}_k=\sum_{i=1}^k \frac{rel_i}{\log_2(i+1)}$) and the ideal-ranking baseline (IDCG) as presented in the original Week 07 slides — needs to be checked against the source deck.

[^week07-lesson]: *Summer Week 7 Lesson Plan*, SupportVectors, 2026.
[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
