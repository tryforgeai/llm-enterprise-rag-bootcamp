# T028 Deduplicate The Week 09 OKF Practice Cards

Status: todo

Created: 2026-08-14

## The Problem

`course/week_09/okf-practice-cards/` contains the same 11 cards four times, from repeated archive extractions:

```text
okf-practice-cards/            <- Chinese cards
okf-practice-cards/okf_cards/  <- Chinese cards, near-identical
okf-practice-cards/en/         <- English cards
okf-practice-cards/okf_cards 2/en/  <- English cards, near-identical
```

The two Chinese `index.md` files are byte-identical; the individual metric cards differ slightly, so a blind delete would lose edits.

All four copies were committed on 2026-08-14 rather than resolved at commit time, to avoid destroying unreviewed edits. Source `.zip` archives are now gitignored.

## The Irony Worth Recording

Week 09 taught that a knowledge unit's identity is its file path, and that a governed corpus is versioned like source code. The practice cards for that lesson are currently four unversioned copies with no canonical path. The cleanup is itself the exercise.

## How To Resolve

1. Diff the four copies per card and pick or merge the best version.
2. Keep one canonical layout, ideally `okf_cards/zh/` and `okf_cards/en/` with one shared `index.md`.
3. Validate the surviving cards against the OKF fields taught in `course/week-09.zh.md`: `type` is the only required field, but `title`, `description`, and provenance are what make a card findable.
4. Add `generated` and `verified` timestamps to each card, since that distinction is the week's central mechanism.
5. Delete the redundant trees in one commit that names what was kept and why.

## Done Criteria

- One copy of each card, at a stable path.
- No card lost content that existed in any of the four copies.
- Every card carries an honest `type`, `title`, `description`, and both timestamps.
