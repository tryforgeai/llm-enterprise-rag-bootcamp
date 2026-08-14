---
type: Metric
title: FActScore
description: Breaks an answer into atomic, no-further-decomposable facts and verifies each one independently, reporting factual precision — finer-grained than RAGAS Faithfulness.
resource: course/week-08.zh.md
tags: [generation, hallucination, week-08, claim-level]
sources:
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
  - id: factscore-paper
    resource: "Min et al. 2023, FActScore (EMNLP)"
    author: Min et al.
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# FActScore

## Definition

Decomposes an answer into individual atomic facts (no further decomposable) and verifies each one independently, reporting the proportion of atomic facts that hold up. The original paper found that 2023-era ChatGPT-generated biographies had only **58%** factual precision — a number the lecture called a "wake-up bell."[^factscore-paper]

## Three years later (as cited in Week 08 lecture, p.97)

By 2026, factual precision is being driven up by "retrieval + abstention" rather than model scale alone:

- Reasoning models with browsing (per the GPT-5 system card): roughly 99% claim precision
- GPT-4o-tier non-reasoning models: 62–71%
- Retrieval-free tail knowledge: still brutal — SimpleQA Verified tops out at 72.1%, and most frontier models sit at 29–55%

## Division of labor with RAGAS Faithfulness

RAGAS Faithfulness checks whether a *sentence* is supported by context, which is easily gamed by a sentence containing multiple, partly-wrong claims. FActScore drops the granularity to the **atomic-fact** level, catching the mixed-correctness sentences that RAGAS can miss.[^week08-notes]

## Points still needing human verification

- [ ] What tool or process our own eval set uses to do "atomic fact decomposition" (whether it's LLM-based decomposition or something cheaper and rule-based) — needs to be filled in against the actual implementation.

[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
[^factscore-paper]: Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*. EMNLP.
