---
type: Metric
title: RAGAS Faithfulness
description: Breaks a generated answer into individual claims and entailment-checks each one against the retrieved context, reporting the fraction of claims that are actually supported.
resource: course/week_08/week-08.zh.md
tags: [generation, ragas, week-08, faithfulness]
sources:
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
  - id: ragas-paper
    resource: "Es et al. 2023, RAGAS"
    author: Es et al.
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# RAGAS Faithfulness

## Definition

Decomposes the generator's answer into individual, independently checkable claims, then entailment-checks each claim against the retrieved context, reporting the proportion of claims supported by that context. The backend can be an LLM (flexible but at risk of a self-reinforcing bias loop) or a classic NLI model (cheaper, more conservative).[^week08-notes]

## Floor, not ceiling

A high Faithfulness score only means the answer is faithful to the **retrieved** context. It does not guarantee:

- That the answer actually addresses the question (that's Answer relevancy's job — Quiz 7's "fluent evasion": asked about a refund, answered about shipping cost, every sentence perfectly supported by the document, yet Faithfulness stays high while Answer relevancy collapses)
- That the retrieved context itself is complete, or missed better evidence (that's Context recall's job)
- That claim granularity isn't being gamed (a single sentence containing 3 independently falsifiable claims can still be scored as "supported" overall)

## Where it's used

As the **floor metric** for generator-side evaluation — used as a first-pass regression gate, then layered with FActScore (finer atomic-claim granularity) and RAGChecker (bidirectional entailment plus dual retrieval/generation diagnostics) for finer-grained diagnosis.

## Points still needing human verification

- [ ] What the actual measured Faithfulness score is for our two gates (Week 06's request guardrail + response grounding), under RAGAS's default decomposition granularity — requires running an eval set to fill in this number.

[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
[^ragas-paper]: Es, S. et al. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*.
