# Method Adoption Record

Copy this file into the target repository and replace every placeholder.

## Identity

- Project:
- Date:
- Owner:
- Method ID and name:
- Status: proposed / experimenting / accepted / rejected / removed

## Problem

- User or system failure:
- Evidence that the failure exists:
- Affected query, user, risk, or document slices:
- Why the current baseline is insufficient:

## Baseline

- Current method:
- Dataset or eval set:
- Metrics:
- Latency:
- Cost:
- Safety and privacy behavior:

## Proposed Adaptation

- Inputs:
- Processing steps:
- Outputs:
- Configurable providers/models/stores:
- Provenance retained:
- Permission boundary:
- Failure and fallback behavior:

## Trace Contract

Record at minimum:

- original intent or question
- normalized or rewritten query
- identity and permission scope
- candidate and selected evidence IDs
- scores and thresholds
- decision and policy reason
- response or action
- safety checks
- latency and cost
- eval result

Do not persist secrets, raw private memory, or unnecessary PII.

## Evaluation Plan

- Primary metric:
- Guardrail metrics:
- Query slices:
- Held-out strategy:
- Paired comparison method:
- Minimum practical improvement:
- Maximum latency/cost regression:
- Stop condition:

## Decision

- Result:
- Evidence:
- Known limitations:
- Follow-up:
- Removal criterion:

## Source Links

- Toolkit method:
- Original course/lab evidence:
- External paper or documentation:
