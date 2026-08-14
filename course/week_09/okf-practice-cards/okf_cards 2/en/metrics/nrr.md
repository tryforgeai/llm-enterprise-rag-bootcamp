---
type: Metric
title: NRR (Negative Rejection Rate)
description: Tests a system with questions the corpus genuinely cannot answer, measuring whether it abstains honestly rather than fabricating a plausible-sounding answer from parametric memory.
resource: course/week-08.zh.md
tags: [abstention, guardrail-adjacent, week-08, cognitive-humility]
sources:
  - id: week08-notes
    resource: course/week-08.zh.md
    author: agent-generated-notes
  - id: rgb-paper
    resource: "Chen et al. 2024, RGB (AAAI)"
    author: Chen et al.
generated:
  by: claude-code/2.1.226
  at: 2026-08-08
verified: []
---

# NRR (Negative Rejection Rate)

## Definition

Construct a set of queries the corpus genuinely cannot answer, and measure the proportion of the time the system honestly abstains (says "I don't know" or "that's not in the material") on this set. Regulated industries typically require a deployment threshold of NRR **> 70%**.[^week08-notes]

## The Calabi–Yau probe (in-class example)

A company that sells network switches gets a RAG system that eagerly and correctly launches into superstring geometry when asked an unrelated question — a textbook negative-rejection failure: the answer came from the model's parametric memory rather than retrieved evidence, and should have been caught by the Week 06 response grounding gate. The RGB paper found ChatGPT-tier models only achieve **43–45%** negative rejection — "fabricating from noise" remains the default behavior for most models.[^rgb-paper]

## Must be reported as a pair

NRR alone is easy to game (a model can inflate this number by refusing to answer almost everything). It must always be reported alongside:

- The rejection rate on unanswerable questions (NRR itself)
- The **over-refusal rate** on answerable questions — to catch the model tipping into "won't answer anything"

## Points still needing human verification

- [ ] Whether our own "unanswerable query set" has already been constructed, and what topics it currently covers — needs checking against the evals directory.

[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
[^rgb-paper]: Chen, J. et al. (2024). *Benchmarking Large Language Models in Retrieval-Augmented Generation (RGB)*. AAAI.
