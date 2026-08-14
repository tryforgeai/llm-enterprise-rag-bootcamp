# T025 Fix The EV-001 Retrieval Failure

Status: todo

Created: 2026-08-14

## The Measured Failure

`evals/results/latest.md`, run of 2026-08-14, lexical retriever, k=5. Three of the four failing cases are retrieval failures:

- **EV-001**, recall@5 = 0.0. "What is a Xennial?" returns four Economic-activity records and one Lead record that gives the Oxford Dictionary date rather than a definition.
- **EV-002**, recall@5 = 0.333 against a bar of 0.4. Only two of the six conflicting birth-year sources are retrieved, so the agent cannot tell the user the sources disagree.
- **EV-008**, recall@5 = 0.0. Two injected records rank first and second and push the clean Technology evidence out of the window.

## Diagnosis, And The Wrong Diagnosis

The obvious explanation for EV-001 is that BM25 has no stemming, so singular "Xennial shoppers" beats plural "Xennials are a social cohort". **That explanation was tested and is wrong.** A crude stemmer was bolted onto the tokenizer with everything else held constant and recall@5 stayed at 0.0; the top-5 merely reshuffled to other non-definition records.

The actual cause: after stopword removal the query is the single term `xennial`. Forty-three records contain it, most at the same term frequency, so BM25 has essentially no discriminating signal and the ranking collapses onto document-length normalization — short records win. Gold record `fact_xennials_lead_01_07` is already singular and still loses at 2.50 against 2.77, purely on length (24 tokens versus 14).

This matters for what gets built next. A one-term query has no lexical signal to rank with at all, so no amount of lexical tuning fixes it. That points at dense retrieval or query expansion, not at the tokenizer.

## Escalation Rule Check

Per `PROJECT_PLAN.md`, an upgrade proposal must name:

| Field | Value |
|---|---|
| Failure addressed | recall@5 = 0.0 on EV-001 and EV-008; 0.333 on EV-002 |
| Metric expected to improve | mean recall@5, currently 0.333 |
| Comparison baseline | `evals/results/baseline-2026-08-14T155252Z-lexical.json` |
| Removal criterion | revert if mean recall@5 does not clear 0.6 with no regression in decision accuracy or NRR |

Cost columns (latency, tokens, maintenance, safety, privacy) must be filled in by whichever option is chosen.

## Candidate Interventions, Cheapest First

1. **Dense retrieval.** Cheaper than it looks: all 187 records in the Week 04 index already carry a 1024-dimension `Qwen/Qwen3-Embedding-0.6B` vector, and `--retriever dense` is already implemented. Only the query vector is missing, which needs the classroom endpoint at `10.0.10.51`. This is a one-session experiment while on the course network.
2. **Query expansion** for short queries, so a one-term question is not left with a single ranking signal.
3. **Hybrid lexical plus dense** with reciprocal rank fusion.
4. **Reranker** over the top-20.

Run option 1 first; it costs almost nothing and its result determines whether options 2 to 4 are worth considering. Do not start GraphRAG.

Note that option 1 cannot be run off the course network, so capture the result while class access is available.

## Separate Sub-Problem: EV-008

EV-008 is not a ranking-quality failure. The injected records genuinely are the best lexical match for the question, and the guardrail correctly refused them. The gap is that nothing re-retrieves clean evidence after the poisoned records are excluded. Fix by filtering flagged records and re-running retrieval before answering, not by changing the retriever.

## Done Criteria

- One intervention is implemented behind a runner flag so the baseline stays reproducible.
- `evals/results/` holds a before-and-after pair from the same case set.
- The result, including a negative result, is recorded in `docs/decisions/decision-log.md`.
