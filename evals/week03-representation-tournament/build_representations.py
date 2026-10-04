#!/usr/bin/env python3
"""Build the competing representations of PRML for the Week 03 tournament.

Three text representations are produced from one identical source parse, so
that the only variable between arms is *where the boundaries fall and what
context each unit carries* -- not the parser, not the cleanup, not the encoder.

    fixed        fixed-length character windows with overlap (the lab baseline)
    semantic     lexical-cohesion boundary detection (TextTiling, Hearst 1997)
    contextual   fixed windows + a deterministic, locally-derived context prefix

A fourth arm, ``page_image``, needs CLIP/SigLIP2 and is built by the in-person
lab (``course/week_03/week-03-in-person-lab/team1_visual.py``). This script only
emits its page manifest so the runner can score it on the same footing.

Design constraints, per PROJECT_PLAN.md and evals/README.md:

* Standard library only. Deterministic. No network, no API key, no model.
* Every number the runner prints must be reproducible from committed files.
* Source of truth is the committed parse at
  ``course/week_03/data/indices/text_meta.json`` -- not a fresh pypdf run --
  so that a parser upgrade cannot silently move the baseline.

Usage::

    python3 evals/week03-representation-tournament/build_representations.py
    python3 evals/week03-representation-tournament/build_representations.py --chunk-size 800
"""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
TOURNEY_DIR = Path(__file__).resolve().parent
DATA_DIR = TOURNEY_DIR / "data"
TEXT_META = (
    REPO_ROOT / "course" / "week_03" / "data" / "indices" / "text_meta.json"
)
PAGE_IMAGE_META = (
    REPO_ROOT / "course" / "week_03" / "data" / "indices" / "clip_meta.json"
)

DOCUMENT_TITLE = "Pattern Recognition and Machine Learning (Bishop)"

DEFAULT_CHUNK_SIZE = 512
DEFAULT_OVERLAP = 50

# TextTiling parameters. Block size is in sentences.
SEMANTIC_BLOCK = 4
SEMANTIC_MIN_CHARS = 250
SEMANTIC_MAX_CHARS = 1600

STOPWORDS = {
    "a", "about", "an", "and", "are", "as", "at", "be", "been", "but", "by",
    "can", "did", "do", "does", "for", "from", "had", "has", "have", "how",
    "i", "if", "in", "into", "is", "it", "its", "may", "more", "most", "no",
    "not", "of", "on", "one", "or", "other", "our", "out", "over", "same",
    "so", "some", "such", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "this", "those", "to", "up", "use", "used",
    "was", "we", "were", "what", "when", "where", "which", "while", "who",
    "will", "with", "would", "you", "your",
}


# --------------------------------------------------------------------------
# Source parse
# --------------------------------------------------------------------------

def load_page_text(meta_path: Path) -> dict[int, str]:
    """Rebuild per-page text from the committed 512-char chunk metadata.

    The lab index stored overlapping windows plus a ``char_start`` offset, so
    the original page string is recoverable by replaying the windows in offset
    order. This is lossless for the committed artifact and avoids depending on
    a PDF parser at eval time.
    """
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    by_page: dict[int, list[dict[str, Any]]] = defaultdict(list)
    for row in meta:
        by_page[int(row["page"])].append(row)

    pages: dict[int, str] = {}
    for page, rows in by_page.items():
        buf = ""
        for row in sorted(rows, key=lambda r: int(r["char_start"])):
            start = int(row["char_start"])
            text = row["text"]
            if start <= len(buf):
                buf = buf[:start] + text
            else:
                buf = buf + " " * (start - len(buf)) + text
        pages[page] = buf
    return pages


# --------------------------------------------------------------------------
# Section map -- the basis for page-level gold evidence
# --------------------------------------------------------------------------

SECTION_HEADER = re.compile(
    r"^(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.?\s*([A-Za-z].*?)\s*\d{0,3}$"
)
# Back matter starts after chapter 14 and must break the forward-fill, or the
# exercises, five appendices, references and index all get attributed to
# section 14.5 and quietly poison every gold page set drawn from it.
BACK_MATTER_HEADER = re.compile(
    r"^(?:\d{1,3}\s+)?"
    r"(Exercises|References|Index|INDEX|REFERENCES"
    r"|[A-E]\.\s*[A-Z][A-Za-z ]+)"
    r"\s*(?:\d{1,3})?$"
)


def derive_section_map(pages: dict[int, str]) -> dict[str, Any]:
    """Map every PDF page to the book section that owns it.

    PRML prints the current section in the running header of odd pages and the
    chapter on even pages. Reading the headers back out and forward-filling
    gives a page -> section assignment derived from the book's own typography
    rather than from anyone's judgement, which is what makes the gold auditable.
    """
    anchors: dict[int, tuple[str, str]] = {}
    for page in sorted(pages):
        body = pages[page].strip()
        if not body:
            continue
        first = body.split("\n")[0].strip()
        back = BACK_MATTER_HEADER.match(first)
        if back:
            label = re.sub(r"\s+", " ", back.group(1)).strip()
            anchors[page] = ("back-matter", label.title())
            continue
        match = SECTION_HEADER.match(first)
        if match:
            anchors[page] = (match.group(1), match.group(2))

    page_to_section: dict[int, str] = {}
    current: str | None = None
    for page in sorted(pages):
        if page in anchors:
            number, title = anchors[page]
            current = f"{number} {title}"
        if current:
            page_to_section[page] = current

    spans: dict[str, list[int]] = defaultdict(list)
    for page, section in page_to_section.items():
        spans[section].append(page)

    def describe(pgs: list[int]) -> dict[str, Any]:
        return {
            "pdf_page_start": min(pgs),
            "pdf_page_end": max(pgs),
            "pdf_pages": sorted(pgs),
            "page_count": len(pgs),
        }

    body = {
        s: describe(p) for s, p in spans.items() if not s.startswith("back-matter")
    }
    non_body = {
        s: describe(p) for s, p in spans.items() if s.startswith("back-matter")
    }
    return {
        "note": (
            "Derived from PRML running headers, forward-filled. PDF page "
            "numbers (1-749), not printed page numbers; the offset between "
            "them drifts across the book, so printed numbers are not used. "
            "'non_body' holds exercises, appendices, references and index; "
            "those pages are never gold and the 'Exercises' bucket is "
            "discontinuous by nature, so its start/end span is meaningless."
        ),
        "header_anchor_pages": len(anchors),
        "sections": dict(sorted(body.items(), key=lambda kv: kv[1]["pdf_page_start"])),
        "non_body": dict(sorted(non_body.items(), key=lambda kv: kv[1]["pdf_page_start"])),
        "page_to_section": {str(p): s for p, s in sorted(page_to_section.items())},
    }


# --------------------------------------------------------------------------
# Whitespace repair
# --------------------------------------------------------------------------

WORD_RE = re.compile(r"[A-Za-z]+")
# The page rebuild pads gaps with spaces to honour char_start offsets; collapse
# the long runs so they do not dominate a fixed window's character budget.
NBSP_RUN = re.compile(r"[ \t]{3,}")


def build_vocabulary(pages: dict[int, str], min_count: int = 3) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for text in pages.values():
        for token in WORD_RE.findall(text.lower()):
            if 2 <= len(token) <= 14:
                counts[token] += 1
    return {w: c for w, c in counts.items() if c >= min_count}


def resegment(token: str, vocab: dict[str, int], total: float) -> list[str]:
    """Split a run-together token using a Viterbi max-likelihood word split.

    pypdf drops inter-word spacing on roughly 10% of PRML tokens
    ("Theproblemofsearchingforpatterns"). Left alone this silently penalises
    every text arm and would be mistaken for a chunking result. The repair is
    applied identically to all three text arms so it cannot become a confound.
    """
    lower = token.lower()
    n = len(lower)
    best = [(-math.inf, 0)] * (n + 1)
    best[0] = (0.0, 0)
    for end in range(1, n + 1):
        for start in range(max(0, end - 18), end):
            prev_score = best[start][0]
            if prev_score == -math.inf:
                continue
            piece = lower[start:end]
            count = vocab.get(piece)
            if count is None:
                continue
            # Length bonus discourages shredding into many tiny words.
            score = prev_score + math.log(count / total) + 3.0
            if score > best[end][0]:
                best[end] = (score, start)
    if best[n][0] == -math.inf:
        return [token]
    pieces: list[str] = []
    cursor = n
    while cursor > 0:
        start = best[cursor][1]
        pieces.append(token[start:cursor])
        cursor = start
    return list(reversed(pieces))


def repair_spacing(text: str, vocab: dict[str, int], total: float) -> str:
    def replace(match: re.Match[str]) -> str:
        token = match.group(0)
        if len(token) <= 14:
            return token
        return " ".join(resegment(token, vocab, total))

    return WORD_RE.sub(replace, text)


# --------------------------------------------------------------------------
# Representations
# --------------------------------------------------------------------------

def chunk_fixed(
    page_text: dict[int, str],
    page_to_section: dict[int, str],
    size: int,
    overlap: int,
) -> list[dict[str, Any]]:
    """Fixed-length character windows, page-scoped. The lab's Team 2 baseline."""
    chunks: list[dict[str, Any]] = []
    step = max(1, size - overlap)
    for page in sorted(page_text):
        text = page_text[page].strip()
        if not text:
            continue
        for start in range(0, max(1, len(text)), step):
            window = text[start : start + size]
            if len(window.strip()) < 40:
                continue
            chunks.append(
                {
                    "chunk_id": f"fixed-{len(chunks):05d}",
                    "pages": [page],
                    "section": page_to_section.get(page, "unmapped"),
                    "text": window,
                    "index_text": window,
                }
            )
            if start + size >= len(text):
                break
    return chunks


SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n{2,}")


def split_sentences(text: str) -> list[str]:
    parts = [p.strip() for p in SENT_SPLIT.split(text) if p and p.strip()]
    return [p for p in parts if len(p) > 1]


def content_terms(text: str) -> Counter[str]:
    return Counter(
        t for t in WORD_RE.findall(text.lower())
        if t not in STOPWORDS and len(t) > 2
    )


def cosine(a: Counter[str], b: Counter[str]) -> float:
    if not a or not b:
        return 0.0
    shared = set(a) & set(b)
    if not shared:
        return 0.0
    num = sum(a[t] * b[t] for t in shared)
    da = math.sqrt(sum(v * v for v in a.values()))
    db = math.sqrt(sum(v * v for v in b.values()))
    return num / (da * db) if da and db else 0.0


def chunk_semantic(
    page_text: dict[int, str],
    page_to_section: dict[int, str],
    block: int = SEMANTIC_BLOCK,
) -> list[dict[str, Any]]:
    """TextTiling-style boundary detection driven by lexical cohesion.

    For every sentence gap, compare the term vectors of the ``block`` sentences
    on each side. Deep local minima in that similarity curve are topic shifts.
    The tiling is reset at section boundaries, which bounds the search and
    stops a boundary from being declared across a chapter break.

    This is the classical, model-free formulation (Hearst 1997). It is a real
    semantic chunker in the boundary-detection sense while staying inside the
    stdlib-only constraint, so the arm runs anywhere the eval runs.
    """
    # Group pages into contiguous section runs.
    runs: list[tuple[str, list[int]]] = []
    for page in sorted(page_text):
        section = page_to_section.get(page, "unmapped")
        if runs and runs[-1][0] == section:
            runs[-1][1].append(page)
        else:
            runs.append((section, [page]))

    chunks: list[dict[str, Any]] = []
    for section, pages in runs:
        sentences: list[tuple[str, int]] = []
        for page in pages:
            for sentence in split_sentences(page_text[page]):
                sentences.append((sentence, page))
        if not sentences:
            continue

        vectors = [content_terms(s) for s, _ in sentences]
        gaps = len(sentences) - 1
        scores: list[float] = []
        for gap in range(gaps):
            left = Counter()
            for v in vectors[max(0, gap - block + 1) : gap + 1]:
                left.update(v)
            right = Counter()
            for v in vectors[gap + 1 : gap + 1 + block]:
                right.update(v)
            scores.append(cosine(left, right))

        boundaries = set()
        if scores:
            mean = sum(scores) / len(scores)
            sd = math.sqrt(sum((s - mean) ** 2 for s in scores) / len(scores))
            cutoff = mean - sd / 2
            for gap in range(gaps):
                left_ok = gap == 0 or scores[gap] <= scores[gap - 1]
                right_ok = gap == gaps - 1 or scores[gap] <= scores[gap + 1]
                if scores[gap] < cutoff and left_ok and right_ok:
                    boundaries.add(gap)

        buffer: list[tuple[str, int]] = []
        def flush() -> None:
            if not buffer:
                return
            text = " ".join(s for s, _ in buffer)
            pages_used = sorted({p for _, p in buffer})
            chunks.append(
                {
                    "chunk_id": f"semantic-{len(chunks):05d}",
                    "pages": pages_used,
                    "section": section,
                    "text": text,
                    "index_text": text,
                }
            )
            buffer.clear()

        for i, item in enumerate(sentences):
            buffer.append(item)
            current_len = sum(len(s) + 1 for s, _ in buffer)
            at_boundary = i in boundaries and current_len >= SEMANTIC_MIN_CHARS
            if at_boundary or current_len >= SEMANTIC_MAX_CHARS:
                flush()
        flush()
    return chunks


def chunk_contextual(
    fixed_chunks: list[dict[str, Any]],
    section_map: dict[str, Any],
    vocab: dict[str, int],
) -> list[dict[str, Any]]:
    """Fixed windows plus a deterministic, locally-derived context prefix.

    Mirrors ``course/week_03/contextual_chunk_pdf.py``: the prefix is computed
    from document title, page span, owning section, and the chunk's own salient
    terms. No LLM call, so there is nothing for a model to hallucinate into the
    context -- which also makes this arm answer open question 4 from the week
    note by construction rather than by evaluation.
    """
    sections = section_map["sections"]
    chunks: list[dict[str, Any]] = []
    for chunk in fixed_chunks:
        page = chunk["pages"][0]
        section = chunk["section"]
        span = sections.get(section)
        # Salient terms are filtered against the corpus vocabulary. Without
        # this the prefix fills up with parser debris ("estepevaluatep"),
        # which would hand the contextual arm noise instead of context.
        section_words = set(WORD_RE.findall(section.lower()))
        terms = [
            t
            for t, _ in content_terms(chunk["text"]).most_common(40)
            if vocab.get(t, 0) >= 5 and t not in section_words
        ][:8]
        where = (
            f"pages {span['pdf_page_start']}-{span['pdf_page_end']}"
            if span
            else f"page {page}"
        )
        context = (
            f"This passage is from '{DOCUMENT_TITLE}', PDF page {page}, "
            f"in section '{section}' ({where}). "
            f"Salient terms: {', '.join(terms)}."
        )
        chunks.append(
            {
                "chunk_id": f"contextual-{len(chunks):05d}",
                "pages": chunk["pages"],
                "section": section,
                "context": context,
                "text": chunk["text"],
                "index_text": f"{context}\n{chunk['text']}",
            }
        )
    return chunks


def page_image_manifest(
    meta_path: Path, page_to_section: dict[int, str]
) -> list[dict[str, Any]]:
    """Emit the page-image arm's units so the runner can score it identically.

    The vectors themselves live in the lab's FAISS indices and need CLIP or
    SigLIP2 to query. This manifest is the page-level skeleton the runner joins
    those scores onto.
    """
    if not meta_path.exists():
        return []
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    return [
        {
            "chunk_id": f"page-{int(row['page']):05d}",
            "pages": [int(row["page"])],
            "section": page_to_section.get(int(row["page"]), "unmapped"),
            "image_path": row.get("image_path", ""),
            "text": "",
            "index_text": "",
        }
        for row in meta
    ]


# --------------------------------------------------------------------------

def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    count = 0
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE)
    parser.add_argument("--overlap", type=int, default=DEFAULT_OVERLAP)
    parser.add_argument(
        "--no-repair-spacing",
        action="store_true",
        help="skip whitespace repair (use to measure how much the parser costs)",
    )
    parser.add_argument("--out", type=Path, default=DATA_DIR)
    args = parser.parse_args(argv)

    if not TEXT_META.exists():
        print(f"missing source parse: {TEXT_META}", file=sys.stderr)
        print(
            "Run course/week_03/week-03-in-person-lab/team2_text.py first.",
            file=sys.stderr,
        )
        return 1

    print(f"reading  {TEXT_META.relative_to(REPO_ROOT)}")
    raw_pages = load_page_text(TEXT_META)
    print(f"         {len(raw_pages)} pages with text")

    vocab = build_vocabulary(raw_pages)
    if args.no_repair_spacing:
        pages = {p: NBSP_RUN.sub("  ", t) for p, t in raw_pages.items()}
        print("spacing  repair SKIPPED")
    else:
        total = float(sum(vocab.values())) or 1.0
        pages = {
            p: NBSP_RUN.sub("  ", repair_spacing(t, vocab, total))
            for p, t in raw_pages.items()
        }
        before = sum(
            1 for t in raw_pages.values() for w in WORD_RE.findall(t) if len(w) > 14
        )
        after = sum(
            1 for t in pages.values() for w in WORD_RE.findall(t) if len(w) > 14
        )
        print(
            f"spacing  repaired run-together tokens: {before} -> {after} "
            f"(vocab {len(vocab)})"
        )

    # Derived after repair so that section titles read "An Alternative View of
    # EM" rather than the parser's "AnAlternativeViewofEM".
    section_map = derive_section_map(pages)
    page_to_section = {
        int(p): s for p, s in section_map["page_to_section"].items()
    }
    print(
        f"sections {len(section_map['sections'])} derived from "
        f"{section_map['header_anchor_pages']} running-header anchors"
    )

    out = args.out
    out.mkdir(parents=True, exist_ok=True)
    (out / "prml_section_map.json").write_text(
        json.dumps(section_map, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    fixed = chunk_fixed(pages, page_to_section, args.chunk_size, args.overlap)
    semantic = chunk_semantic(pages, page_to_section)
    contextual = chunk_contextual(fixed, section_map, vocab)
    page_images = page_image_manifest(PAGE_IMAGE_META, page_to_section)

    stats: dict[str, Any] = {
        "document_title": DOCUMENT_TITLE,
        "source_parse": str(TEXT_META.relative_to(REPO_ROOT)),
        "pages": len(pages),
        "spacing_repaired": not args.no_repair_spacing,
        "chunk_size": args.chunk_size,
        "overlap": args.overlap,
        "arms": {},
    }

    for name, rows in (
        ("fixed", fixed),
        ("semantic", semantic),
        ("contextual", contextual),
        ("page_image", page_images),
    ):
        if not rows:
            print(f"{name:11s} skipped (no source artifact)")
            continue
        count = write_jsonl(out / f"chunks.{name}.jsonl", rows)
        lengths = [len(r["text"]) for r in rows if r["text"]]
        stats["arms"][name] = {
            "units": count,
            "mean_chars": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "min_chars": min(lengths) if lengths else 0,
            "max_chars": max(lengths) if lengths else 0,
            "distinct_pages": len({p for r in rows for p in r["pages"]}),
        }
        info = stats["arms"][name]
        print(
            f"{name:11s} {count:6d} units  mean {info['mean_chars']:7.1f} chars  "
            f"{info['distinct_pages']} pages"
        )

    (out / "build_stats.json").write_text(
        json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nwrote    {out.relative_to(REPO_ROOT)}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
