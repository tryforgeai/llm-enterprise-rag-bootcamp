---
type: Guardrail
title: PII Redaction Guardrail
description: Detects and redacts personally identifiable information (names, phone numbers, emails, ID numbers, etc.) before retrieved content enters a prompt or before an answer reaches the user.
resource: course/week_06/pii_redaction_demo.py
tags: [guardrail, week-06, privacy, pii]
sources:
  - id: week06-demo
    resource: course/week_06/pii_redaction_demo.py
    author: Asif Qamar
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# PII Redaction Guardrail

## What it does

After content is retrieved (or after an answer is generated), this guardrail detects personally identifiable information in the text — names, phone numbers, email addresses, ID/passport numbers — and redacts it per policy (replacing it with a placeholder, partial masking, or refusing to return that fragment entirely).

## Why this must be a separate, dedicated gate rather than a prompt-level instruction to "be careful about privacy"

Prompt-level constraints alone are unreliable — the model can still reproduce PII it retrieved, verbatim, during generation. The reliable approach is a deterministic rule set or a dedicated NER/PII detection model that mechanically filters text before it enters the prompt or before it leaves the system, rather than relying on the generating model to "behave."

## Relationship to enterprise corpus governance

If the upstream corpus was never given proper access-control tiering (which fields who can see), PII redaction can only ever be a last-resort patch. The more fundamental fix is to tag sensitive fields at the OKF concept level itself, restricting them from entering the searchable index in the first place.

## Points still needing human verification

- [ ] The exact detection method used in `pii_redaction_demo.py` (regex, an NER model, or a combination) and which PII types it supports — needs confirming by opening the script.
- [ ] Whether this gate is currently wired into Avaloka, and at which point in the pipeline.
