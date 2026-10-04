---
type: Metric
title: ECE (Expected Calibration Error)
description: Bins predictions and compares the model's stated confidence against actual accuracy in each bin, weighted across bins — measures whether a model is "confident when it should be, hesitant when it should be."
resource: course/week_08/week-08.zh.md
tags: [calibration, week-08, cognitive-humility]
sources:
  - id: week08-notes
    resource: course/week_08/week-08.zh.md
    author: agent-generated-notes
  - id: guo-calibration
    resource: "Guo et al. 2017, On Calibration of Modern Neural Networks (ICML)"
    author: Guo et al.
generated:
  by: agent/claude
  at: 2026-08-08
verified: []
---

# ECE (Expected Calibration Error)

## Definition

Bins the confidence values a model states into several ranges, and within each bin compares "the confidence the model claims" against "the accuracy actually observed," taking a weighted difference. Perfect calibration is 0; modern LLMs commonly fall in the 0.05–0.15 range, and **the bigger and more instruction-tuned the model, the worse it often gets** (confidence gets pushed up without accuracy keeping pace).[^week08-notes]

## In-class worked example (two bins)

The high-confidence bin showed roughly 15 points of overconfidence (stated confidence exceeded actual accuracy by 15 percentage points), and because this bin holds a large share of samples, it dominated the overall error — this is a textbook signature of modern LLMs, and also the most dangerous region, since users are most inclined to trust high-confidence answers.

## Fixes

- Temperature scaling — cheapest and most common
- Platt scaling
- Isotonic regression

## Relationship to the risk-coverage curve

Good ECE calibration is a precondition for the risk-coverage curve to be "convex" (abstaining on a small slice yields a large drop in error rate). A poorly calibrated model has an unreliable abstention signal to begin with, so its risk-coverage curve can degenerate into a straight line or even a concave shape.

## Points still needing human verification

- [ ] The exact number of bins and the weighting method (weighted by sample count per bin, or equal weight) used in the lecture's presentation — needs to be checked against Guo et al.'s original paper.

[^week08-notes]: *Week 08 Class Notes*, course notes, 2026-08-01.
[^guo-calibration]: Guo, C. et al. (2017). *On Calibration of Modern Neural Networks*. ICML.
