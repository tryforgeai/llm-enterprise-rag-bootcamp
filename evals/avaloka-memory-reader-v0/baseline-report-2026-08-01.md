# Avaloka Memory Reader V0 Baseline Report

Date: 2026-08-01

Source repository: `/Users/soardulia/workspace/AvalokaAI`

Source command:

```bash
cd /Users/soardulia/workspace/AvalokaAI/app
npm run eval:memory:reader -- --json --output reports/memory-reader-v0-baseline-2026-08-01.json
```

Source fixture:

```text
/Users/soardulia/workspace/AvalokaAI/evals/memory-reader-retrieval-cases.json
```

Imported label bridge:

```text
evals/avaloka-memory-reader-v0/cases.labeled-from-avaloka.jsonl
```

## Result

| Metric | Value |
|---|---:|
| total cases | 48 |
| passed | 48 |
| failed | 0 |
| pass rate | 1.000 |
| Recall@3 | 1.000 |
| Recall@5 | 1.000 |
| MRR | 0.896 |
| nDCG@5 | 0.999 |
| no-match precision | 1.000 |
| unsafe retrieval count | 0 |
| stale retrieval count | 0 |
| deleted retrieval count | 0 |
| superseded retrieval count | 0 |
| p50 latency | 0.012 ms |
| p95 latency | 0.088 ms |

## Failure Taxonomy

| Failure class | Count |
|---|---:|
| none | 48 |
| missing_tag_or_alias | 0 |
| semantic_paraphrase_miss | 0 |
| hard_negative_false_hit | 0 |
| correct_candidate_ranked_low | 0 |
| no_match_false_positive | 0 |
| stale_or_inactive_leak | 0 |
| safety_priority_failure | 0 |
| fixture_or_contract_error | 0 |

## Interpretation

The deterministic Memory Reader V0 passes the current synthetic fixture set. This is useful as a first calibration anchor, but it is not proof that Avaloka is broadly calibrated.

The result means:

- deterministic tag/alias retrieval is healthy on the current fixture distribution;
- no-match, stale, deleted, superseded, and safety-priority guard cases are represented;
- the current fixture does not yet create enough retrieval ambiguity to expose ranking weakness;
- MRR and nDCG@5 are high, but the suite remains synthetic and should be hardened before architecture upgrades.

## Limitations

- The benchmark runs inside the AvalokaAI repository because the runnable Care Card fixture and Memory Reader implementation live there.
- The bootcamp repository imports labels and summary metrics, not the full runnable reader implementation.
- The fixture has 48 cases, not the future target of 100+ held-out cases.
- The benchmark evaluates retrieval selection, not final answer grounding or Baifa/Dharma response boundaries.

## Next Hardening Slice

Before adding embeddings, graph retrieval, learned rerankers, or fine-tuning, expand the eval frontier:

1. Add 30+ human-written cases that are not generated from the current deterministic tag pattern.
2. Add cross-lingual cases without explicit tags.
3. Add partial-answer cases where one memory is relevant but another requested fact is unknown.
4. Add Baifa/Dharma boundary cases to answer-quality and guardian evals.
5. Add a claim-grounding join report that checks whether final responses only use retrieved, active, allowed memory.
