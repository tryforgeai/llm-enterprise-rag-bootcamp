#!/usr/bin/env python3
"""Build a small local retrieval index for Week 04 artifact comparison.

This is deliberately simple and offline:
- input: local JSON artifacts under course/week_04/artifacts
- output: local_retrieval_index.json with sparse TF-IDF vectors

It is not a replacement for SV cluster embeddings or Qdrant. It is the first
debuggable version of the experiment so retrieval behavior is visible.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"
OUT = ARTIFACTS / "local_retrieval_index.json"

STOPWORDS = {
    "the",
    "and",
    "for",
    "that",
    "with",
    "this",
    "from",
    "are",
    "into",
    "used",
    "use",
    "how",
    "what",
    "why",
    "can",
    "its",
    "their",
    "while",
    "chapter",
    "section",
}


def load_json(name: str) -> dict:
    with (ARTIFACTS / name).open("r", encoding="utf-8") as f:
        return json.load(f)


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9\-']+", text.lower())
    return [t.strip("-'") for t in tokens if len(t.strip("-'")) > 2 and t not in STOPWORDS]


def keyword_text(keywords: list[str] | None) -> str:
    return " ".join(keywords or [])


def make_records() -> list[dict]:
    records: list[dict] = []

    raw_chunks = load_json("raw_chunks_sample.json")["chunks"]
    for chunk in raw_chunks:
        index_text = " ".join(
            [
                chunk["title"],
                chunk["chunk_text"],
                keyword_text(chunk.get("keywords")),
            ]
        )
        records.append(
            {
                "record_id": chunk["chunk_id"],
                "artifact_type": "raw_chunk",
                "source_id": chunk["source_id"],
                "title": chunk["title"],
                "index_text": index_text,
                "display_text": chunk["chunk_text"],
                "source_pointer": chunk["source_pointer"],
            }
        )

    summaries = load_json("abstractive_summaries.json")["summaries"]
    for summary in summaries:
        index_text = " ".join(
            [
                summary["title"],
                summary["summary"],
                summary["retrieval_use"],
                keyword_text(summary.get("key_concepts")),
            ]
        )
        records.append(
            {
                "record_id": summary["summary_id"],
                "artifact_type": "abstractive_summary",
                "source_id": summary["source_id"],
                "title": summary["title"],
                "index_text": index_text,
                "display_text": summary["summary"],
                "source_pointer": summary["source_pointer"],
            }
        )

    propositions = load_json("dense_x_propositions.json")["propositions"]
    for proposition in propositions:
        index_text = " ".join(
            [
                proposition["text"],
                keyword_text(proposition.get("keywords")),
            ]
        )
        records.append(
            {
                "record_id": proposition["proposition_id"],
                "artifact_type": "proposition",
                "source_id": "dense_x",
                "title": "Dense-X proposition",
                "index_text": index_text,
                "display_text": proposition["text"],
                "source_pointer": proposition["source_pointer"],
            }
        )

    qa_pairs = load_json("qa_pairs.json")["qa_pairs"]
    for qa in qa_pairs:
        index_text = " ".join(
            [
                qa["question"],
                qa["answer"],
                keyword_text(qa.get("keywords")),
            ]
        )
        records.append(
            {
                "record_id": qa["qa_id"],
                "artifact_type": "qa_pair",
                "source_id": qa["source_id"],
                "title": qa["question"],
                "index_text": index_text,
                "display_text": qa["answer"],
                "source_pointer": qa["source_pointer"],
                "artifact_pointer": qa.get("artifact_pointer"),
            }
        )

    return records


def build_index(records: list[dict]) -> dict:
    doc_tokens = [tokenize(r["index_text"]) for r in records]
    doc_freq: Counter[str] = Counter()
    for tokens in doc_tokens:
        doc_freq.update(set(tokens))

    n_docs = len(records)
    idf = {
        term: round(math.log((n_docs + 1) / (df + 1)) + 1.0, 6)
        for term, df in sorted(doc_freq.items())
    }

    indexed_records = []
    for record, tokens in zip(records, doc_tokens):
        tf = Counter(tokens)
        weights = {
            term: (1.0 + math.log(count)) * idf[term]
            for term, count in tf.items()
        }
        norm = math.sqrt(sum(v * v for v in weights.values())) or 1.0
        vector = {
            term: round(value / norm, 6)
            for term, value in sorted(weights.items())
        }
        indexed_records.append({**record, "tokens": sorted(tf), "vector": vector})

    return {
        "created": "2026-06-27",
        "index_type": "local_sparse_tfidf_cosine",
        "note": "Offline teaching index. Replace vector field with SV/Qdrant embeddings for production experiments.",
        "record_count": len(indexed_records),
        "artifact_types": sorted({r["artifact_type"] for r in indexed_records}),
        "idf": idf,
        "records": indexed_records,
    }


def main() -> None:
    records = make_records()
    index = build_index(records)
    OUT.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT} with {len(records)} records.")


if __name__ == "__main__":
    main()
