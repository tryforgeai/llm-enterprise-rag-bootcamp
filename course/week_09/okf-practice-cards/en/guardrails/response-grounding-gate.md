---
type: Guardrail
title: Response Grounding Gate
description: An output-side gate that checks whether each claim in a generated answer can actually be traced back to retrieved evidence, before that answer reaches the user — preventing the model from "filling in" from parametric memory.
resource: course/week_06/guardrailed_rag_pipeline_demo.py
tags: [guardrail, week-06, grounding, negative-rejection]
sources:
  - id: week06-demo
    resource: course/week_06/guardrailed_rag_pipeline_demo.py
    author: Asif Qamar
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# Response Grounding Gate

## What it does

After an answer is generated but before it reaches the user, this gate checks whether each claim in the answer can be traced to supporting evidence in the context retrieved for that query. Unsupported claims are either stripped or flagged as "not in the material — here's general background instead." This gate maps directly onto the capability that Week 08's NRR metric is designed to measure.[^week08-notes]

## Division of labor with the Request Guardrail

The request guardrail intercepts on the **input side** (e.g. judging whether a question is in scope). The response grounding gate intercepts on the **output side** (judging whether the already-generated answer is actually grounded). Both are necessary — input-side filtering cannot catch parametric-memory content the model "recalls" during generation.

## What failure looks like (in-class example)

A company that sells network switches gets a RAG system that, when asked an unrelated question, eagerly and correctly launches into superstring geometry — exactly the case this gate is supposed to catch and didn't (the Calabi–Yau probe).

## Points still needing human verification

- [ ] The exact implementation of this gate in `guardrailed_rag_pipeline_demo.py` (whether it's claim-level entailment checking or coarser keyword matching) — needs to be confirmed by opening the script.

[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
