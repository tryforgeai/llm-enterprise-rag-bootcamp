---
type: Metric
title: MRR (Mean Reciprocal Rank)
description: The rank at which the first relevant result appears in the retrieval list — cares only about "how fast can we find one usable answer."
resource: course/week_07/summer-week-7-lesson-plan.pdf
tags: [retrieval, ranking, week-07, six-metric-ladder]
sources:
  - id: week07-lesson
    resource: course/week_07/summer-week-7-lesson-plan.pdf
    author: Asif Qamar
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# MRR (Mean Reciprocal Rank)

## Definition

For each query, find the rank position of the first relevant result and take its reciprocal, $1/rank$. MRR is the average of this reciprocal across all queries. A hit at position 1 scores 1.0, a hit at position 2 scores 0.5, and so on — higher rank, higher score.[^week07-lesson]

## Division of labor with NDCG@5

MRR only cares about how quickly the first relevant result shows up, which suits scenarios where "just one correct answer is enough" (e.g. FAQ retrieval). NDCG@5 cares about the ranking quality of the entire top-5 list, which suits RAG scenarios that need multiple pieces of evidence to support one composite answer. The two are usually reported together because they answer different questions.

## Where it's used

- Quickly diagnosing whether a retrieval system is failing to find anything at all — an MRR near 0 means even the first relevant result rarely ranks near the top, making it a more sensitive early warning signal than NDCG.

## Points still needing human verification

- [ ] Whether the lecture had a dedicated worked example or "war story" for MRR (not yet covered in the page-by-page Week 07 notes) — needs catching up or comparing notes with a classmate.

[^week07-lesson]: *Summer Week 7 Lesson Plan*, SupportVectors, 2026.
