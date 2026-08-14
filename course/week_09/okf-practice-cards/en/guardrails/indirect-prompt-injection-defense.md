---
type: Guardrail
title: Indirect Prompt Injection Defense
description: Prevents instructions smuggled inside retrieved third-party documents from being mistaken by the model for system instructions — separating "content to answer from" from "commands to obey."
resource: course/week_06/indirect_injection_defense_demo.py
tags: [guardrail, week-06, security, prompt-injection]
sources:
  - id: week06-demo
    resource: course/week_06/indirect_injection_defense_demo.py
    author: Asif Qamar
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# Indirect Prompt Injection Defense

## Threat model

Unlike direct injection (where a user types a malicious instruction straight into the conversation), indirect injection hides the malicious instruction inside a **retrieved third-party document** — a webpage, an email, a PDF that got ingested into the corpus — containing something like "ignore the previous instructions and instead do…". When the model assembles the prompt, it can easily fail to distinguish "this is content to be analyzed" from "this is a command to obey."

## Defensive approach

- Structural boundaries: wrap retrieved content in explicit delimiters/tags, and state clearly in the system prompt that text inside those delimiters is always to be treated as data to analyze, never as instructions.
- Instruction filtering: scan retrieved content for typical injection patterns (phrases like "ignore previous instructions") and flag or strip them.
- Least privilege: even if an injection succeeds, downstream request/response guardrails should limit what actions the model can actually execute (e.g. it should never be able to directly invoke a tool with side effects).

## Relationship to Week 09's OKF

A concept file that has gone through OKF governance and carries a `verified` record is inherently less likely to smuggle an injected instruction than an unreviewed scraped webpage, because it has already passed through a human or CI review gate. But this can't replace runtime injection detection, because the attack surface also includes corpus content that **hasn't been governed yet but is still retrievable**.

## Points still needing human verification

- [ ] The specific attack scenario and defense technique demonstrated in `indirect_injection_defense_demo.py` — needs confirming by opening the script to see whether it's keyword filtering, structural boundaries, or both.
