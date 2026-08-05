# Avaloka Memory Reader V0 Hardening Plan

Status: draft hardening slice

Purpose: make the current Memory Reader benchmark harder before any embedding, vector DB, graph retrieval, learned reranker, RAPTOR, or fine-tuning work is justified.

## Baseline Starting Point

The imported AvalokaAI synthetic Memory Reader benchmark currently reports:

- 48 / 48 passed
- Recall@5: 1.000
- MRR: 0.896
- nDCG@5: 0.999
- no-match precision: 1.000
- stale/deleted/superseded leakage: 0

This proves the deterministic reader is healthy on the current fixture distribution. It does not prove the reader is calibrated on harder, less-tagged, multilingual, partially answerable, or Dharma-boundary inputs.

## Hardening Objective

Add 30 cases that pressure the current reader without changing architecture first.

The hardening set should expose whether failures come from:

- missing tag or alias coverage;
- semantic paraphrase miss;
- no-tag cross-lingual recall gap;
- surface-overlap false positives;
- stale/fresh conflict handling;
- deleted or forbidden memory leakage;
- partial-answer overclaiming;
- safety-priority memory ranking;
- Baifa/Dharma boundary conflicts where a relevant memory should still be constrained by non-harm.

## Fixture Classes

| Class | Count | Intent |
|---|---:|---|
| cross-lingual no explicit tags | 5 | Chinese/English meaning maps to Care Card facts without `readerContext.tags`. |
| partial answer | 5 | Some requested facts are supported; other requested facts are unknown. |
| stale/fresh conflict | 5 | Fresh active memory must beat stale, deleted, or superseded matching memory. |
| Baifa/Dharma boundary conflict | 5 | Relevant memory cannot be used to justify karma blame, spiritual bypass, or false authority. |
| privacy/deletion probes | 5 | Deleted/private memories must not be confirmed, retrieved, or exposed. |
| hard negatives with surface overlap | 5 | Similar words must not override the real care context. |

## Use Rule

These cases are seed labels for the next runnable fixture expansion. Do not weaken expected relevance after failures appear unless a policy review proves the original label encoded the wrong behavior.

## Next Execution Sequence

1. Convert `cases.hardening.seed.jsonl` into AvalokaAI's runnable `evals/memory-reader-retrieval-cases.json` fixture shape.
2. Run `npm run eval:memory:reader` in AvalokaAI.
3. Mine failures and low-rank pressure signals.
4. Decide from measured failures whether deterministic aliases, semantic recall, lifecycle scoring, or policy labels need work.
5. Keep embeddings/graph/reranker default-deferred until the hardening set names a specific failure class.
