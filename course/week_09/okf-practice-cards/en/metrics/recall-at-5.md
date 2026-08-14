---
type: Metric
title: Recall@5
description: Of all documents relevant to a query, what fraction shows up in the top 5 retrieved results — measures whether the things that should be found actually got found.
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, coverage, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# Recall@5

## Definition

Out of the full ground-truth set of documents relevant to a query, the fraction that appears among the top 5 results returned by the retrieval system.[^week07-lesson]

## On choosing k

k should match downstream usage: if the generator only takes the top 3 chunks into the prompt, measuring Recall@10 has no direct operational meaning. Recall@k should be measured with k equal to the number of chunks actually handed to the generator.

## Why it's the foundation of the six-metric ladder

Low recall is the problem most worth fixing first — it means **the evidence never entered the candidate pool in the first place**. No matter how strong the reranker or how faithful the generator downstream, neither can recover evidence that was never retrieved. Per Week 08's Evaluation Map: "Low context recall → fix chunking/retrieval; nothing downstream can compensate for evidence that never arrived."

## Points still needing human verification

- [ ] What k value Avaloka actually uses in production (i.e. how many chunks are passed to the generator) — needs to be confirmed against the retrieval pipeline config before fixing a default k for this card.

[^week07-lesson]: *Summer Week 7 Lesson Plan*, SupportVectors, 2026.
