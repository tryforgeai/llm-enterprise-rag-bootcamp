# T002 First Agentic RAG Evals

Status: doing

## Goal

Create the first 10 eval cases for the minimal agentic RAG lab.

## Suggested Split

- 3 factual retrieval cases
- 2 safety or guardrail cases
- 2 memory-use cases
- 2 decision-policy cases
- 1 tone and compassion case

## Done Criteria

- Eval cases live in `evals/`.
- Each case includes expected evidence, expected decision, safety concerns, and pass/fail criteria.
- The lab plan links to the eval set.

## Calibration R1 Seed Artifacts

- `evals/avaloka-memory-reader-v0/cases.seed.jsonl`
- `evals/avaloka-unknown-calibration-v0/cases.seed.jsonl`
- `evals/avaloka-baifa-dharma-boundary-v0/cases.seed.jsonl`

These are draft seed cases. They must be labeled with real Avaloka memory IDs before they become a runnable benchmark.
