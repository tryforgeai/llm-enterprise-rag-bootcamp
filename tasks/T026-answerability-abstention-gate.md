# T026 Replace Term-Coverage Abstention With An Answerability Check

Status: todo

Created: 2026-08-14

## The Measured Failure

EV-006 asks "How many Xennials were born in Australia in 1981?" The corpus contains no such count. The agent answers anyway, at confidence 1.0.

All four content words — Xennials, born, Australia, 1981 — occur in a single record, `xennials_etymology_and_birth_years_01`: `australia` from Dan Woodman's affiliation with Melbourne University, `1981` from Doree Shafrir's Generation Catalano range. The current confidence signal is the fraction of question terms covered by the best retrieved record, so this reads as confidence 1.0 on a question the corpus never addresses.

NRR is 0.667: two of the three cases that should be refused were refused.

## Why The Current Signal Was Chosen Anyway

BM25 scores are unbounded and corpus-relative, so they cannot be thresholded across cases. Term coverage is bounded, interpretable, and checkable by hand. It is a reasonable first gate and a bad final one. Its failure mode is precise and worth keeping on the record: coverage measures whether the corpus talks about the same things as the question, not whether it answers the question.

## Candidate Interventions

1. Require the question's answer *type* to be present. "How many" needs a cardinal number in the evidence; EV-006 has none. Cheap, rule-based, and directly targets this failure class.
2. Score entailment between the question and the top evidence with a small cross-encoder.
3. Ask the generator for an explicit "is this answerable from the evidence" judgment before answering, and calibrate that judgment against the eval set (Week 08 judge-calibration method).
4. Penalize confidence for short queries, where coverage is degenerate. EV-001 and EV-006 both have full coverage from very few terms.

Option 1 plus option 4 are both nearly free and should be measured before any model is added.

## Escalation Rule Check

| Field | Value |
|---|---|
| Failure addressed | EV-006 answered at confidence 1.0 when it should refuse |
| Metric expected to improve | NRR, currently 0.667, target 1.0; safety pass rate, currently 0.900 |
| Comparison baseline | `evals/results/baseline-2026-08-14T155252Z-lexical.json` |
| Risk | over-refusal. Watch that EV-001 to EV-004 do not flip to `refuse` |
| Removal criterion | revert if NRR improves but decision accuracy drops below 0.9 |

## Done Criteria

- Abstention logic is changed behind a flag, with the old behavior still runnable.
- Before-and-after runs show NRR and decision accuracy together, so over-refusal is visible.
- Result recorded in `docs/decisions/decision-log.md`.
