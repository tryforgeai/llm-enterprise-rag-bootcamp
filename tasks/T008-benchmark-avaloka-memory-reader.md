# T008: Benchmark Avaloka Memory Reader V0

Status: doing

## Goal

Measure the existing deterministic Avaloka memory reader before adding embeddings, hybrid retrieval, reranking, RAPTOR, or GraphRAG.

## Scope

- Create at least 30 labeled retrieval cases.
- Include hard negatives, no-match, stale-memory, safety-priority, tone, and avoid-response cases.
- Run the existing deterministic reader as the baseline.
- Record Recall@5, MRR, NDCG@5, unsafe retrievals, stale retrievals, no-match precision, and latency.
- Classify misses by likely intervention: tags, query transformation, embeddings, reranking, or graph-shaped retrieval.

## Current Calibration R1 Artifacts

- `evals/avaloka-memory-reader-v0/README.md`
- `evals/avaloka-memory-reader-v0/labels.schema.json`
- `evals/avaloka-memory-reader-v0/rubric.md`
- `evals/avaloka-memory-reader-v0/cases.seed.jsonl`
- `evals/avaloka-memory-reader-v0/cases.labeled-from-avaloka.jsonl`
- `evals/avaloka-memory-reader-v0/hardening-plan.md`
- `evals/avaloka-memory-reader-v0/cases.hardening.seed.jsonl`
- `evals/avaloka-unknown-calibration-v0/README.md`
- `evals/avaloka-unknown-calibration-v0/cases.seed.jsonl`
- `evals/avaloka-baifa-dharma-boundary-v0/README.md`
- `evals/avaloka-baifa-dharma-boundary-v0/rubric.md`
- `evals/avaloka-baifa-dharma-boundary-v0/cases.seed.jsonl`
- `templates/calibration-agent-trace.json`

The seed cases are not yet a runnable baseline because their expected memory IDs must be replaced with real Avaloka Care Card memory IDs. `cases.labeled-from-avaloka.jsonl` is converted from the existing AvalokaAI synthetic Memory Reader benchmark and provides the first labeled cross-project eval bridge. `cases.hardening.seed.jsonl` adds the next 30 pressure cases for expanding the runnable fixture after the clean baseline.

## Done When

- A versioned retrieval dataset exists.
- Baseline metrics are saved as a durable report.
- At least five representative failures are traced.
- The next retrieval component is selected from measured failures, or the current reader is retained if it is sufficient.

