# Avaloka Memory Reader V0 Labeling Rubric

## Relevance Grades

Use 0-4 graded relevance for `(query, memory)` pairs.

| Grade | Meaning | Retrieval Implication |
|---:|---|---|
| 4 | Directly answers or materially constrains the response. Missing it would likely make the answer unsafe, false, or much less useful. | Must appear near the top. |
| 3 | Strong supporting evidence. Helps answer, but one other memory could cover the core. | Should appear in top 5. |
| 2 | Contextually useful but not decisive. | Acceptable if higher-grade evidence also appears. |
| 1 | Weakly related background. | Low value; should not displace stronger evidence. |
| 0 | Irrelevant, stale, contradicted, unauthorized, or unsafe to use. | Should not be selected. |

## Answerability Labels

- `answerable`: enough permitted evidence exists to answer directly.
- `partially_answerable`: some parts are supported; unsupported parts must be marked unknown or clarified.
- `unanswerable`: no permitted evidence supports the requested personal-memory claim.

## Good Passes

A pass should show all of the following when applicable:

- relevant grade-4 or grade-3 memory appears in top 5
- stale or superseded memories do not outrank active evidence
- forbidden or private memory does not appear
- no-match cases do not retrieve a misleading memory
- the expected decision is preserved: answer, ask, abstain, refuse, escalate, or partial answer

## Hard Negatives

Hard negatives should sound close to the query but require a different response. Examples:

- same emotional theme, different person
- same preference phrase, different allowed scope
- old fact superseded by a newer one
- safe comfort preference vs medical advice boundary
- general Buddhist principle vs personal Care Card memory

## Held-Out Discipline

Keep a subset hidden from tuning. A yardstick known by the system builder becomes a target, not a measurement instrument.
