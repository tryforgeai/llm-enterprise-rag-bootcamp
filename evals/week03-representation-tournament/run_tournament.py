#!/usr/bin/env python3
"""Week 03 representation tournament.

Runs one query set against several competing representations of the same
corpus and reports where the evidence ends up.

    corpus -> {fixed | semantic | contextual | page_image}
           -> retrieve -> score against page-level gold
           -> classify the error -> optional grounding judge

The point of the tournament is stated in course/week-03.zh.md: do not argue
about which chunking strategy is better in theory, make them compete on the
same queries under the same metrics.

Two rules keep the comparison honest.

**Page-level gold.** Gold evidence is a set of PDF page numbers, derived from
PRML's own running headers by ``build_representations.py``. A chunk, a
sentence tile and a rendered page image can all be projected onto pages, so
every arm is scored in the same unit. Nothing in the gold derivation looks at
retriever output, so no arm is being scored against its own criterion.

**Top-k distinct pages.** Arms return different numbers of units per page, so
"top-5 results" is not comparable across arms. Each arm is instead walked down
its ranking until ``k`` *distinct pages* have been collected. A page-image arm
returns 5 pages from 5 units; a fixed-chunk arm may need 12 units to do the
same. That is a real cost difference, and it is reported as ``units_read``
rather than hidden inside the metric.

Usage::

    python3 evals/week03-representation-tournament/run_tournament.py
    python3 evals/week03-representation-tournament/run_tournament.py --k 10
    python3 evals/week03-representation-tournament/run_tournament.py --encoder minilm
    python3 evals/week03-representation-tournament/run_tournament.py --arms fixed,semantic
    python3 evals/week03-representation-tournament/run_tournament.py --judge   # needs an API key

Exit code is 0 whenever the run completes. Losing arms are evidence, not errors.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Sequence

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOURNEY_DIR = Path(__file__).resolve().parent
DATA_DIR = TOURNEY_DIR / "data"
RESULTS_DIR = TOURNEY_DIR / "results"
CASES_PATH = TOURNEY_DIR / "cases.jsonl"
TRACES_DIR = REPO_ROOT / "traces"

TEXT_ARMS = ("fixed", "semantic", "contextual")
ALL_ARMS = TEXT_ARMS + ("page_image",)

DEFAULT_K = 5
DEFAULT_ABSTAIN_THRESHOLD = 0.60

STOPWORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "been", "but", "by",
    "can", "did", "do", "does", "for", "from", "give", "had", "has", "have",
    "how", "i", "if", "in", "into", "is", "it", "its", "let", "look", "may",
    "more", "most", "no", "not", "of", "on", "one", "or", "other", "our",
    "out", "over", "same", "show", "so", "some", "such", "than", "that",
    "the", "their", "them", "then", "there", "these", "they", "this",
    "those", "to", "up", "use", "used", "uses", "using", "was", "we", "were",
    "what", "when", "where", "which", "while", "who", "will", "with",
    "would", "write", "you", "your",
}

WORD_RE = re.compile(r"[A-Za-z]+")


def normalize_section(name: str) -> str:
    """Collapse a section name to a spacing-insensitive key.

    Section titles are read out of the PDF's running headers, where the parser
    drops word spacing unpredictably ("TheEMAlgorithminGeneral" vs "The EM
    Algorithm in General"). Matching gold on the normalized form means the
    same cases.jsonl works whether or not whitespace repair is enabled, so the
    --no-repair-spacing ablation measures extraction quality instead of
    failing on a gold-name mismatch.
    """
    return re.sub(r"[^a-z0-9]", "", name.lower())


def section_lookup(sections: dict[str, Any]) -> dict[str, str]:
    return {normalize_section(name): name for name in sections}


def resolve_section(name: str, lookup: dict[str, str]) -> str | None:
    return lookup.get(normalize_section(name))


def tokenize(text: str) -> list[str]:
    # Minimum length 2, not 3. "EM" is the entire subject of four cases in
    # this set and a 3-character floor silently deletes it from the query --
    # a tokenizer bug that reads exactly like a chunking failure.
    return [
        t for t in WORD_RE.findall(text.lower())
        if t not in STOPWORDS and len(t) >= 2
    ]


# --------------------------------------------------------------------------
# Encoders
# --------------------------------------------------------------------------

class LexicalEncoder:
    """BM25 over ``index_text``. Standard library, deterministic, no network.

    Deliberately weak, in the same spirit as evals/run_evals.py: the tournament
    is a comparison between representations, and a weak shared encoder keeps
    the representation the only variable. Swap in ``--encoder minilm`` to check
    that the ranking between arms survives a stronger encoder.
    """

    name = "lexical-bm25"

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1 = k1
        self.b = b

    def build(self, units: Sequence[dict[str, Any]]) -> None:
        self.docs = [tokenize(u["index_text"]) for u in units]
        self.lengths = [len(d) for d in self.docs]
        self.avg_len = (sum(self.lengths) / len(self.lengths)) if self.lengths else 0.0
        self.freqs = [Counter(d) for d in self.docs]
        df: Counter[str] = Counter()
        for doc in self.docs:
            df.update(set(doc))
        n = len(self.docs)
        self.idf = {
            term: math.log(1 + (n - count + 0.5) / (count + 0.5))
            for term, count in df.items()
        }
        self.postings: dict[str, list[int]] = defaultdict(list)
        for i, doc in enumerate(self.docs):
            for term in set(doc):
                self.postings[term].append(i)

    def score(self, query: str) -> list[tuple[int, float]]:
        terms = tokenize(query)
        scores: dict[int, float] = defaultdict(float)
        for term in terms:
            idf = self.idf.get(term)
            if idf is None:
                continue
            for i in self.postings[term]:
                tf = self.freqs[i][term]
                denom = tf + self.k1 * (
                    1 - self.b + self.b * (self.lengths[i] / (self.avg_len or 1))
                )
                scores[i] += idf * (tf * (self.k1 + 1)) / (denom or 1)
        return sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))


class MiniLMEncoder:
    """Dense retrieval with sentence-transformers. Optional, needs the model.

    Present so the tournament can be re-run on a machine that has the lab
    environment, to check whether the ordering between representations is an
    artefact of the lexical encoder or survives a real embedding model.
    """

    name = "minilm-dense"

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        try:
            from sentence_transformers import SentenceTransformer  # type: ignore
        except ImportError as exc:  # pragma: no cover - environment dependent
            raise SystemExit(
                "--encoder minilm needs sentence-transformers:\n"
                "    pip install sentence-transformers\n"
                f"(import failed: {exc})"
            ) from exc
        self.model = SentenceTransformer(model_name)
        self.name = f"dense-{model_name.split('/')[-1]}"

    def build(self, units: Sequence[dict[str, Any]]) -> None:
        import numpy as np  # type: ignore

        self.matrix = self.model.encode(
            [u["index_text"] for u in units],
            batch_size=64,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True,
        )
        self._np = np

    def score(self, query: str) -> list[tuple[int, float]]:
        vector = self.model.encode(
            [query], convert_to_numpy=True, normalize_embeddings=True
        )[0]
        sims = self.matrix @ vector
        order = self._np.argsort(-sims)
        return [(int(i), float(sims[i])) for i in order[:200]]


def make_encoder(name: str) -> Any:
    if name == "lexical":
        return LexicalEncoder()
    if name == "minilm":
        return MiniLMEncoder()
    raise SystemExit(f"unknown encoder: {name}")


# --------------------------------------------------------------------------
# Metrics
# --------------------------------------------------------------------------

def recall_at_k(retrieved: Sequence[int], gold: set[int]) -> float:
    if not gold:
        return 0.0
    return len(set(retrieved) & gold) / len(gold)


def hit_at_k(retrieved: Sequence[int], gold: set[int]) -> bool:
    return bool(set(retrieved) & gold)


def mrr(retrieved: Sequence[int], gold: set[int]) -> float:
    for rank, page in enumerate(retrieved, start=1):
        if page in gold:
            return 1.0 / rank
    return 0.0


def ndcg_at_k(retrieved: Sequence[int], gold: set[int], k: int) -> float:
    if not gold:
        return 0.0
    dcg = sum(
        1.0 / math.log2(rank + 1)
        for rank, page in enumerate(retrieved[:k], start=1)
        if page in gold
    )
    ideal_hits = min(len(gold), k)
    idcg = sum(1.0 / math.log2(rank + 1) for rank in range(1, ideal_hits + 1))
    return dcg / idcg if idcg else 0.0


# --------------------------------------------------------------------------
# Error typing
# --------------------------------------------------------------------------

def classify_error(
    case: dict[str, Any],
    pages: Sequence[int],
    gold: set[int],
    gold_sections: dict[str, set[int]],
    page_to_section: dict[int, str],
    abstained: bool,
) -> str:
    """Name the failure using the Week 03 vocabulary, not a generic 'miss'.

    A ranked list of pages cannot reveal a true endophora break -- that needs
    the answer text -- so these labels describe *retrieval* pathologies only.
    ``--judge`` adds generation-side labels on top.
    """
    if case.get("expect_abstain"):
        return "ok" if abstained else "over_answer"
    if abstained:
        return "over_abstain"
    if not pages:
        return "empty_retrieval"

    covered = {
        name for name, pgs in gold_sections.items() if set(pages) & pgs
    }
    if not covered:
        landed = {page_to_section.get(p, "unmapped") for p in pages}
        if any(s.startswith("back-matter") for s in landed):
            return "definition_orphan"
        return "off_target"

    required = int(case.get("min_distinct_evidence", 1) or 1)
    if len(gold_sections) > 1 and len(covered) < min(required, len(gold_sections)):
        return "partial_coverage"
    if len(gold_sections) == 1 and required > 1:
        if len(set(pages) & gold) < required:
            return "partial_coverage"
    if set(pages[:1]) & gold:
        return "ok"
    return "weak_ranking"


# --------------------------------------------------------------------------
# Grounding judge (optional)
# --------------------------------------------------------------------------

def build_judge(enabled: bool, model: str) -> Callable[[str, str], dict[str, Any]] | None:
    """Return an answer-grounding judge, or None when the flag is off.

    Kept behind a flag on purpose. Every retrieval number in this tournament is
    reproducible offline from committed files; the moment a hosted model is in
    the loop that stops being true, so the default run does not call one.
    """
    if not enabled:
        return None
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise SystemExit(
            "--judge needs ANTHROPIC_API_KEY in the environment.\n"
            "The repository root .env is the intended home for it; never commit it."
        )
    try:
        import anthropic  # type: ignore
    except ImportError as exc:  # pragma: no cover - environment dependent
        raise SystemExit(f"--judge needs the anthropic package: {exc}") from exc

    client = anthropic.Anthropic(api_key=api_key)
    system = (
        "You grade retrieval evidence, not prose. Given a question and the "
        "retrieved passages, answer strictly as JSON with keys: "
        '"answerable" (bool: do the passages contain enough to answer), '
        '"grounded_fraction" (0-1: share of the answer the passages support), '
        '"missing" (short string: what is absent), '
        '"scope_risk" (bool: would answering from these passages drop a '
        "condition, qualifier or negation present in the source). "
        "Return JSON only."
    )

    def judge(question: str, evidence: str) -> dict[str, Any]:
        try:
            response = client.messages.create(
                model=model,
                max_tokens=400,
                system=system,
                messages=[
                    {
                        "role": "user",
                        "content": f"QUESTION:\n{question}\n\nRETRIEVED PASSAGES:\n{evidence[:12000]}",
                    }
                ],
            )
            raw = response.content[0].text.strip()
            raw = re.sub(r"^```(?:json)?|```$", "", raw, flags=re.MULTILINE).strip()
            return json.loads(raw)
        except Exception as exc:  # pragma: no cover - network dependent
            return {"error": str(exc)}

    return judge


# --------------------------------------------------------------------------
# Runner
# --------------------------------------------------------------------------

def load_units(arm: str) -> list[dict[str, Any]]:
    path = DATA_DIR / f"chunks.{arm}.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def top_k_pages(
    ranking: Sequence[tuple[int, float]],
    units: Sequence[dict[str, Any]],
    k: int,
) -> tuple[list[int], int, list[dict[str, Any]]]:
    """Walk the ranking until k distinct pages are collected.

    Returns the pages, how many units had to be read to get them, and the
    contributing units in order, for the trace.
    """
    pages: list[int] = []
    seen: set[int] = set()
    read = 0
    evidence: list[dict[str, Any]] = []
    for index, score in ranking:
        read += 1
        unit = units[index]
        fresh = [p for p in unit["pages"] if p not in seen]
        if not fresh:
            continue
        for page in fresh:
            if len(pages) >= k:
                break
            pages.append(page)
            seen.add(page)
        evidence.append(
            {
                "chunk_id": unit["chunk_id"],
                "pages": unit["pages"],
                "section": unit["section"],
                "score": round(float(score), 4),
                # Full text for scoring; the trace writer truncates. Measuring
                # confidence on a truncated preview silently penalises the arms
                # with the longest units, which is the opposite of the truth.
                "text": unit.get("text") or "",
                "preview": (unit.get("text") or "")[:220],
            }
        )
        if len(pages) >= k:
            break
    return pages, read, evidence


def term_coverage(question: str, evidence: Sequence[dict[str, Any]]) -> float:
    """Confidence proxy, matching the main eval's definition.

    Fraction of the question's content words covered by the single best
    retrieved unit. A similarity score cannot be thresholded across cases;
    this can, and it is inspectable by hand.
    """
    terms = set(tokenize(question))
    if not terms or not evidence:
        return 0.0
    best = 0.0
    for item in evidence[:3]:
        covered = terms & set(tokenize(item.get("text", "")))
        best = max(best, len(covered) / len(terms))
    return best


def run_arm(
    arm: str,
    cases: list[dict[str, Any]],
    section_map: dict[str, Any],
    encoder_name: str,
    k: int,
    abstain_threshold: float,
    judge: Callable[[str, str], dict[str, Any]] | None,
) -> dict[str, Any]:
    units = load_units(arm)
    if not units:
        return {"arm": arm, "skipped": "no chunk file; build it first"}
    if arm == "page_image" and not units[0].get("index_text"):
        return {
            "arm": arm,
            "skipped": (
                "page-image units carry no text; this arm needs CLIP/SigLIP2. "
                "See README 'Adding the page-image arm'."
            ),
        }

    page_to_section = {int(p): s for p, s in section_map["page_to_section"].items()}
    sections = section_map["sections"]
    lookup = section_lookup(sections)

    encoder = make_encoder(encoder_name)
    encoder.build(units)

    per_case: list[dict[str, Any]] = []
    for case in cases:
        gold_sections = {}
        for declared in case.get("gold_sections", []):
            resolved = resolve_section(declared, lookup)
            if resolved:
                gold_sections[resolved] = set(sections[resolved]["pdf_pages"])
        gold = set().union(*gold_sections.values()) if gold_sections else set()

        ranking = encoder.score(case["question"])
        pages, units_read, evidence = top_k_pages(ranking, units, k)
        confidence = term_coverage(case["question"], evidence)
        abstained = confidence < abstain_threshold or not pages

        metrics = {
            "recall_at_k": round(recall_at_k(pages, gold), 4),
            "hit_at_k": hit_at_k(pages, gold),
            "mrr": round(mrr(pages, gold), 4),
            "ndcg_at_k": round(ndcg_at_k(pages, gold, k), 4),
            "gold_pages": len(gold),
            "gold_sections_covered": sum(
                1 for pgs in gold_sections.values() if set(pages) & pgs
            ),
            "gold_sections_total": len(gold_sections),
            "units_read": units_read,
            "confidence": round(confidence, 4),
        }
        error = classify_error(
            case, pages, gold, gold_sections, page_to_section, abstained
        )

        bar = float(case.get("min_recall_at_k", 0.0) or 0.0)
        required_sections = int(case.get("min_distinct_evidence", 1) or 1)
        if case.get("expect_abstain"):
            passed = abstained
        else:
            # An abstention on an answerable case is a failure even when the
            # right pages were retrieved: the evidence was found and then not
            # used. Scoring it as a pass would hide a denial-of-service.
            passed = (
                not abstained
                and metrics["hit_at_k"]
                and metrics["recall_at_k"] >= bar
                and (
                    len(gold_sections) < 2
                    or metrics["gold_sections_covered"] >= min(required_sections, len(gold_sections))
                )
            )

        record = {
            "eval_id": case["eval_id"],
            "family": case["family"],
            "question": case["question"],
            "passed": passed,
            "error_type": error,
            "abstained": abstained,
            "retrieved_pages": pages,
            "retrieved_sections": [page_to_section.get(p, "unmapped") for p in pages],
            **metrics,
        }

        if judge is not None and not case.get("expect_abstain"):
            blob = "\n\n---\n\n".join(
                f"[page {e['pages']}] {e['preview']}" for e in evidence[:8]
            )
            record["grounding"] = judge(case["question"], blob)

        per_case.append(record)

        trace = {
            "run": arm,
            "encoder": encoder.name,
            "k": k,
            "case": case,
            "gold_pages": sorted(gold),
            "result": record,
            "evidence": [
                {key: value for key, value in item.items() if key != "text"}
                for item in evidence
            ],
        }
        trace_dir = TRACES_DIR / "week03-tournament" / arm
        trace_dir.mkdir(parents=True, exist_ok=True)
        (trace_dir / f"{case['eval_id']}.json").write_text(
            json.dumps(trace, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    answerable = [c for c in per_case if not _case_by_id(cases, c["eval_id"]).get("expect_abstain")]
    negatives = [c for c in per_case if _case_by_id(cases, c["eval_id"]).get("expect_abstain")]

    def mean(values: list[float]) -> float:
        return round(sum(values) / len(values), 4) if values else 0.0

    summary = {
        "arm": arm,
        "encoder": encoder.name,
        "units": len(units),
        "cases_passed": sum(1 for c in per_case if c["passed"]),
        "cases_total": len(per_case),
        "mean_recall_at_k": mean([c["recall_at_k"] for c in answerable]),
        "hit_rate_at_k": mean([1.0 if c["hit_at_k"] else 0.0 for c in answerable]),
        "mean_mrr": mean([c["mrr"] for c in answerable]),
        "mean_ndcg_at_k": mean([c["ndcg_at_k"] for c in answerable]),
        "mean_units_read": mean([float(c["units_read"]) for c in per_case]),
        "negative_rejection_rate": mean(
            [1.0 if c["abstained"] else 0.0 for c in negatives]
        ),
        "error_types": dict(Counter(c["error_type"] for c in per_case)),
        "by_family": {},
    }
    for family in sorted({c["family"] for c in per_case}):
        rows = [c for c in per_case if c["family"] == family]
        answerable_rows = [
            c for c in rows
            if not _case_by_id(cases, c["eval_id"]).get("expect_abstain")
        ]
        summary["by_family"][family] = {
            "cases": len(rows),
            "passed": sum(1 for c in rows if c["passed"]),
            "mean_recall_at_k": mean([c["recall_at_k"] for c in answerable_rows]),
            "hit_rate_at_k": mean(
                [1.0 if c["hit_at_k"] else 0.0 for c in answerable_rows]
            ),
        }
    summary["cases"] = per_case
    return summary


def _case_by_id(cases: list[dict[str, Any]], eval_id: str) -> dict[str, Any]:
    for case in cases:
        if case["eval_id"] == eval_id:
            return case
    return {}


def validate_cases(cases: list[dict[str, Any]], section_map: dict[str, Any]) -> None:
    """Abort on an unknown gold section.

    Same discipline as evals/README.md: a typo in gold must stop the run, not
    show up later as a retrieval failure and get mistaken for a finding.
    """
    lookup = section_lookup(section_map["sections"])
    problems = []
    for case in cases:
        for name in case.get("gold_sections", []):
            if resolve_section(name, lookup) is None:
                problems.append(f"{case['eval_id']}: unknown gold section {name!r}")
        if not case.get("gold_sections") and not case.get("expect_abstain"):
            problems.append(f"{case['eval_id']}: no gold and not marked expect_abstain")
    if problems:
        print("gold validation failed:", file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        raise SystemExit(2)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------

def render_markdown(report: dict[str, Any]) -> str:
    lines: list[str] = []
    add = lines.append
    add("# Week 03 Representation Tournament")
    add("")
    add(f"Run `{report['run_id']}` · corpus `{report['corpus']}` · "
        f"encoder `{report['encoder']}` · k={report['k']} (distinct pages) · "
        f"abstain threshold {report['abstain_threshold']}")
    add("")
    add("Gold evidence is a set of PDF pages derived from PRML's running headers. "
        "Each arm is walked down its ranking until k distinct pages are collected, "
        "so `units read` is the cost of assembling the same amount of evidence.")
    add("")

    arms = [a for a in report["arms"] if "skipped" not in a]
    skipped = [a for a in report["arms"] if "skipped" in a]

    add("## Leaderboard")
    add("")
    add("| Arm | Units | Passed | Recall@k | Hit@k | MRR | NDCG@k | NRR | Units read |")
    add("| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |")
    for arm in sorted(arms, key=lambda a: -a["mean_recall_at_k"]):
        add(
            f"| {arm['arm']} | {arm['units']} | "
            f"{arm['cases_passed']}/{arm['cases_total']} | "
            f"{arm['mean_recall_at_k']:.3f} | {arm['hit_rate_at_k']:.3f} | "
            f"{arm['mean_mrr']:.3f} | {arm['mean_ndcg_at_k']:.3f} | "
            f"{arm['negative_rejection_rate']:.3f} | {arm['mean_units_read']:.1f} |"
        )
    add("")
    if skipped:
        for arm in skipped:
            add(f"- `{arm['arm']}` skipped: {arm['skipped']}")
        add("")

    add("## Hit rate by failure family")
    add("")
    families = sorted({f for a in arms for f in a["by_family"]})
    add("| Family | " + " | ".join(a["arm"] for a in arms) + " |")
    add("| --- | " + " | ".join("---:" for _ in arms) + " |")
    for family in families:
        cells = []
        for arm in arms:
            info = arm["by_family"].get(family)
            if not info:
                cells.append("-")
            elif family == "hard_negative":
                cells.append(f"{info['passed']}/{info['cases']} abstained")
            else:
                cells.append(f"{info['hit_rate_at_k']:.2f}")
        add(f"| {family} | " + " | ".join(cells) + " |")
    add("")

    add("## Error types")
    add("")
    types = sorted({t for a in arms for t in a["error_types"]})
    add("| Error | " + " | ".join(a["arm"] for a in arms) + " |")
    add("| --- | " + " | ".join("---:" for _ in arms) + " |")
    for error in types:
        add(
            f"| {error} | "
            + " | ".join(str(a["error_types"].get(error, 0)) for a in arms)
            + " |"
        )
    add("")

    add("## Per-case hit@k")
    add("")
    add("| Case | Family | " + " | ".join(a["arm"] for a in arms) + " |")
    add("| --- | --- | " + " | ".join(":---:" for _ in arms) + " |")
    ids = [c["eval_id"] for c in arms[0]["cases"]] if arms else []
    for eval_id in ids:
        rows = {a["arm"]: next(c for c in a["cases"] if c["eval_id"] == eval_id) for a in arms}
        family = next(iter(rows.values()))["family"]
        cells = []
        for arm in arms:
            row = rows[arm["arm"]]
            if family == "hard_negative":
                cells.append("abstain" if row["abstained"] else "ANSWERED")
            else:
                cells.append("hit" if row["hit_at_k"] else "miss")
        add(f"| {eval_id} | {family} | " + " | ".join(cells) + " |")
    add("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=DEFAULT_K,
                        help="number of distinct pages to collect per arm")
    parser.add_argument("--encoder", default="lexical", choices=["lexical", "minilm"])
    parser.add_argument("--arms", default=",".join(ALL_ARMS))
    parser.add_argument("--abstain-threshold", type=float,
                        default=DEFAULT_ABSTAIN_THRESHOLD)
    parser.add_argument("--judge", action="store_true",
                        help="score answer grounding with an LLM judge (needs API key)")
    parser.add_argument("--judge-model", default="claude-sonnet-5")
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument(
        "--archive",
        action="store_true",
        help="also keep this run as a permanent named baseline for comparison",
    )
    args = parser.parse_args(argv)

    section_path = DATA_DIR / "prml_section_map.json"
    if not section_path.exists():
        print("missing representations; run build_representations.py first",
              file=sys.stderr)
        return 1
    section_map = json.loads(section_path.read_text(encoding="utf-8"))
    cases = [
        json.loads(line)
        for line in CASES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    validate_cases(cases, section_map)

    judge = build_judge(args.judge, args.judge_model)
    run_id = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H%M%SZ")

    arms: list[dict[str, Any]] = []
    for arm in [a.strip() for a in args.arms.split(",") if a.strip()]:
        print(f"running {arm} ...", file=sys.stderr)
        arms.append(
            run_arm(
                arm, cases, section_map, args.encoder, args.k,
                args.abstain_threshold, judge,
            )
        )

    report = {
        "run_id": run_id,
        "corpus": "PRML (749 pages)",
        "encoder": args.encoder,
        "k": args.k,
        "abstain_threshold": args.abstain_threshold,
        "judge": args.judge,
        "cases": len(cases),
        "arms": arms,
    }

    markdown = render_markdown(report)
    print(markdown)

    if not args.no_write:
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)
        (RESULTS_DIR / "latest.md").write_text(markdown, encoding="utf-8")
        (RESULTS_DIR / "latest.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        if args.archive:
            stem = f"baseline-{run_id}-{args.encoder}-k{args.k}"
            (RESULTS_DIR / f"{stem}.json").write_text(
                json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            (RESULTS_DIR / f"{stem}.md").write_text(markdown, encoding="utf-8")
            print(f"archived {stem}", file=sys.stderr)
        print(
            f"\nwrote {(RESULTS_DIR / 'latest.md').relative_to(REPO_ROOT)} "
            f"and traces/week03-tournament/",
            file=sys.stderr,
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
