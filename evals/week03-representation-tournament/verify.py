#!/usr/bin/env python3
"""Independent check on the tournament's numbers.

The metric implementations in ``run_tournament.py`` are re-derived here from
scratch -- different code, same definitions -- and compared against the run
report. This is the same discipline the main eval used in evals/README.md,
where an independent reimplementation caught two real bugs in nDCG and in the
decision function.

What is checked:

1. Every gold section named by a case exists in the section map.
2. Gold pages are inside the corpus and never fall in back matter.
3. Retrieved pages are distinct, within k, and inside the corpus.
4. recall@k, hit@k, MRR and nDCG@k recomputed from the recorded pages and
   gold sections match the reported values.
5. Arm-level means match the per-case values they claim to summarise.
6. The reported error type is consistent with the recorded outcome.
7. No case is simultaneously reported as passed and as having abstained.

Usage::

    python3 evals/week03-representation-tournament/verify.py
"""

from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path
from typing import Any

TOURNEY_DIR = Path(__file__).resolve().parent
DATA_DIR = TOURNEY_DIR / "data"
RESULTS = TOURNEY_DIR / "results" / "latest.json"
CASES_PATH = TOURNEY_DIR / "cases.jsonl"

TOLERANCE = 1e-4


def norm(name: str) -> str:
    """Spacing-insensitive section key, mirroring run_tournament."""
    return re.sub(r"[^a-z0-9]", "", name.lower())


def ref_recall(pages: list[int], gold: set[int]) -> float:
    if not gold:
        return 0.0
    hits = 0
    for page in set(pages):
        if page in gold:
            hits += 1
    return hits / len(gold)


def ref_mrr(pages: list[int], gold: set[int]) -> float:
    rank = 1
    for page in pages:
        if page in gold:
            return 1 / rank
        rank += 1
    return 0.0


def ref_ndcg(pages: list[int], gold: set[int], k: int) -> float:
    if not gold:
        return 0.0
    gain = 0.0
    position = 1
    for page in pages[:k]:
        if page in gold:
            gain += 1 / math.log(position + 1, 2)
        position += 1
    perfect = 0.0
    for position in range(1, min(len(gold), k) + 1):
        perfect += 1 / math.log(position + 1, 2)
    return gain / perfect if perfect > 0 else 0.0


def close(a: float, b: float) -> bool:
    return abs(float(a) - float(b)) <= TOLERANCE


def main() -> int:
    if not RESULTS.exists():
        print("no results/latest.json -- run run_tournament.py first", file=sys.stderr)
        return 1

    report = json.loads(RESULTS.read_text(encoding="utf-8"))
    section_map = json.loads((DATA_DIR / "prml_section_map.json").read_text(encoding="utf-8"))
    sections = section_map["sections"]
    by_norm = {norm(n): n for n in sections}
    non_body_pages = {
        p for info in section_map.get("non_body", {}).values() for p in info["pdf_pages"]
    }
    cases = {
        json.loads(line)["eval_id"]: json.loads(line)
        for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    k = report["k"]
    corpus_pages = set(range(1, 750))

    failures: list[str] = []
    checks = 0

    # 1 + 2: gold integrity
    for eval_id, case in cases.items():
        for name in case.get("gold_sections", []):
            checks += 1
            resolved = by_norm.get(norm(name))
            if resolved is None:
                failures.append(f"{eval_id}: gold section {name!r} not in section map")
                continue
            pages = set(sections[resolved]["pdf_pages"])
            if not pages <= corpus_pages:
                failures.append(f"{eval_id}: gold section {name!r} has out-of-range pages")
            if pages & non_body_pages:
                failures.append(
                    f"{eval_id}: gold section {name!r} overlaps back matter"
                )

    for arm in report["arms"]:
        if "skipped" in arm:
            continue
        name = arm["arm"]
        recalls, hits, mrrs, ndcgs, reads = [], [], [], [], []
        negatives_abstained = []

        for row in arm["cases"]:
            case = cases[row["eval_id"]]
            gold_sections = {
                by_norm[norm(s)]: set(sections[by_norm[norm(s)]]["pdf_pages"])
                for s in case.get("gold_sections", [])
                if norm(s) in by_norm
            }
            gold: set[int] = set().union(*gold_sections.values()) if gold_sections else set()
            pages = row["retrieved_pages"]

            # 3: retrieval shape
            checks += 1
            if len(pages) != len(set(pages)):
                failures.append(f"{name}/{row['eval_id']}: duplicate pages in top-k")
            if len(pages) > k:
                failures.append(f"{name}/{row['eval_id']}: {len(pages)} pages exceeds k={k}")
            if not set(pages) <= corpus_pages:
                failures.append(f"{name}/{row['eval_id']}: page outside 1-749")

            # 4: metric agreement
            checks += 4
            if not close(ref_recall(pages, gold), row["recall_at_k"]):
                failures.append(
                    f"{name}/{row['eval_id']}: recall {row['recall_at_k']} "
                    f"!= {ref_recall(pages, gold):.4f}"
                )
            if bool(set(pages) & gold) != row["hit_at_k"]:
                failures.append(f"{name}/{row['eval_id']}: hit@k disagrees")
            if not close(ref_mrr(pages, gold), row["mrr"]):
                failures.append(
                    f"{name}/{row['eval_id']}: mrr {row['mrr']} != {ref_mrr(pages, gold):.4f}"
                )
            if not close(ref_ndcg(pages, gold, k), row["ndcg_at_k"]):
                failures.append(
                    f"{name}/{row['eval_id']}: ndcg {row['ndcg_at_k']} "
                    f"!= {ref_ndcg(pages, gold, k):.4f}"
                )

            # 6 + 7: outcome consistency
            checks += 2
            if row["passed"] and row["abstained"] and not case.get("expect_abstain"):
                failures.append(
                    f"{name}/{row['eval_id']}: passed while abstaining on an "
                    "answerable case"
                )
            expected_error = {
                (True, True): "ok",
                (True, False): "over_answer",
            }.get((bool(case.get("expect_abstain")), row["abstained"]))
            if expected_error and row["error_type"] != expected_error:
                failures.append(
                    f"{name}/{row['eval_id']}: error_type {row['error_type']!r} "
                    f"expected {expected_error!r}"
                )

            reads.append(float(row["units_read"]))
            if case.get("expect_abstain"):
                negatives_abstained.append(1.0 if row["abstained"] else 0.0)
            else:
                recalls.append(row["recall_at_k"])
                hits.append(1.0 if row["hit_at_k"] else 0.0)
                mrrs.append(row["mrr"])
                ndcgs.append(row["ndcg_at_k"])

        # 5: aggregate agreement
        def mean(values: list[float]) -> float:
            return sum(values) / len(values) if values else 0.0

        for label, computed, reported in (
            ("mean_recall_at_k", mean(recalls), arm["mean_recall_at_k"]),
            ("hit_rate_at_k", mean(hits), arm["hit_rate_at_k"]),
            ("mean_mrr", mean(mrrs), arm["mean_mrr"]),
            ("mean_ndcg_at_k", mean(ndcgs), arm["mean_ndcg_at_k"]),
            ("mean_units_read", mean(reads), arm["mean_units_read"]),
            (
                "negative_rejection_rate",
                mean(negatives_abstained),
                arm["negative_rejection_rate"],
            ),
        ):
            checks += 1
            if not close(computed, reported):
                failures.append(
                    f"{name}: {label} reported {reported} != recomputed {computed:.4f}"
                )

        checks += 1
        recomputed_passed = sum(1 for row in arm["cases"] if row["passed"])
        if recomputed_passed != arm["cases_passed"]:
            failures.append(
                f"{name}: cases_passed {arm['cases_passed']} != {recomputed_passed}"
            )

    print(f"checks run: {checks}")
    if failures:
        print(f"FAILED: {len(failures)}")
        for failure in failures:
            print(f"  {failure}")
        return 1
    print("all checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
