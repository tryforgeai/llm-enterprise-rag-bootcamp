# T027 Write Week 04 And Week 05 Class Notes

Status: todo

Created: 2026-08-14

## The Gap

`course/` has written notes for weeks 01, 02, 03, 06, 07, 08, and 09. Weeks 04 and 05 have no note file at all.

Both weeks produced real work, so the evidence exists and only the note is missing:

**Week 04** (`course/week_04/`) — the derived-artifact retrieval experiment. Raw chunks versus propositions versus QA pairs versus abstractive summaries, over PRML and the Dense-X paper, plus the Xennials FactoidWiki demo, the embedding index, and two browser demos. Tasks T016 and T017 are marked done.

**Week 05** (`course/week_05/`) — graph-shaped learning artifacts: `carry_forward_knowledge_graph` and `fractal_structure_knowledge_graph`, plus the lesson plan PDF.

## Why It Matters Now

The Week 04 artifacts are the corpus the eval baseline runs against. EV-001's failure is a direct test of the Week 04 hypothesis that query-shaped artifacts outrank raw chunks — and the note that would have recorded that hypothesis and its predicted failure modes does not exist. The reasoning is currently only in commit messages and file names.

Week 05 matters for the opposite reason: it is the graph week, and `PROJECT_PLAN.md` explicitly defers GraphRAG. The note should record *why* it was deferred while the material was fresh, so the deferral is a decision rather than an omission.

## Done Criteria

- `course/week-04.zh.md` and `course/week-05.zh.md` exist and follow `templates/weekly-note.md`.
- Each answers the five README questions, especially "what agent capability does this unlock".
- Week 04's note states the artifact-comparison hypothesis and links to the EV-001 result as the first measurement of it.
- `course/00-course-overview.md` links both.
