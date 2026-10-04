# Week 03 Representation Tournament

Run `2026-09-12T181342Z` · corpus `PRML (749 pages)` · encoder `lexical` · k=5 (distinct pages) · abstain threshold 0.6

Gold evidence is a set of PDF pages derived from PRML's running headers. Each arm is walked down its ranking until k distinct pages are collected, so `units read` is the cost of assembling the same amount of evidence.

## Leaderboard

| Arm | Units | Passed | Recall@k | Hit@k | MRR | NDCG@k | NRR | Units read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| semantic | 1403 | 20/27 | 0.255 | 0.913 | 0.637 | 0.539 | 0.750 | 3.7 |
| contextual | 2944 | 16/27 | 0.247 | 0.957 | 0.719 | 0.514 | 0.750 | 5.8 |
| fixed | 2944 | 14/27 | 0.177 | 0.870 | 0.684 | 0.422 | 0.750 | 5.3 |

- `page_image` skipped: page-image units carry no text; this arm needs CLIP/SigLIP2. See README 'Adding the page-image arm'.

## Hit rate by failure family

| Family | fixed | semantic | contextual |
| --- | ---: | ---: | ---: |
| cross_section | 1.00 | 1.00 | 1.00 |
| definition_use_chain | 1.00 | 1.00 | 1.00 |
| definitional | 0.83 | 1.00 | 1.00 |
| equation_dependent | 1.00 | 1.00 | 0.75 |
| figure_dependent | 0.75 | 0.75 | 1.00 |
| hard_negative | 3/4 abstained | 3/4 abstained | 3/4 abstained |
| scope_condition | 0.67 | 0.67 | 1.00 |

## Error types

| Error | fixed | semantic | contextual |
| --- | ---: | ---: | ---: |
| definition_orphan | 1 | 0 | 1 |
| off_target | 0 | 1 | 0 |
| ok | 14 | 13 | 15 |
| over_abstain | 5 | 1 | 4 |
| over_answer | 1 | 1 | 1 |
| partial_coverage | 2 | 2 | 1 |
| weak_ranking | 4 | 9 | 5 |

## Per-case hit@k

| Case | Family | fixed | semantic | contextual |
| --- | --- | :---: | :---: | :---: |
| W03-01 | definitional | hit | hit | hit |
| W03-02 | definitional | miss | hit | hit |
| W03-03 | definitional | hit | hit | hit |
| W03-04 | definitional | hit | hit | hit |
| W03-05 | definitional | hit | hit | hit |
| W03-06 | definitional | hit | hit | hit |
| W03-07 | figure_dependent | miss | miss | hit |
| W03-08 | figure_dependent | hit | hit | hit |
| W03-09 | figure_dependent | hit | hit | hit |
| W03-10 | figure_dependent | hit | hit | hit |
| W03-11 | equation_dependent | hit | hit | miss |
| W03-12 | equation_dependent | hit | hit | hit |
| W03-13 | equation_dependent | hit | hit | hit |
| W03-14 | equation_dependent | hit | hit | hit |
| W03-15 | definition_use_chain | hit | hit | hit |
| W03-16 | definition_use_chain | hit | hit | hit |
| W03-17 | definition_use_chain | hit | hit | hit |
| W03-18 | scope_condition | miss | miss | hit |
| W03-19 | scope_condition | hit | hit | hit |
| W03-20 | scope_condition | hit | hit | hit |
| W03-21 | cross_section | hit | hit | hit |
| W03-22 | cross_section | hit | hit | hit |
| W03-23 | cross_section | hit | hit | hit |
| W03-24 | hard_negative | abstain | abstain | abstain |
| W03-25 | hard_negative | ANSWERED | ANSWERED | ANSWERED |
| W03-26 | hard_negative | abstain | abstain | abstain |
| W03-27 | hard_negative | abstain | abstain | abstain |
