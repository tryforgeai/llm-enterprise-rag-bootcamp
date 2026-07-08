#!/usr/bin/env python3
"""Build a small FactoidWiki-style RAG dataset from the Xennials Wikipedia page.

No third-party dependencies are required for the pipeline. The Streamlit app is
separate and optional.
"""

from __future__ import annotations

import argparse
import html
import json
import math
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
DATA.mkdir(exist_ok=True)

DEFAULT_TITLE = "Xennials"
DEFAULT_SOURCE_URL = "https://en.wikipedia.org/wiki/Xennials"
MEDIAWIKI_API = "https://en.wikipedia.org/w/api.php"

DEFAULT_SV_EMBED_URL = "http://10.0.10.51:8000/embed-text/v1/embeddings"
DEFAULT_SV_EMBED_MODEL = "Qwen/Qwen3-Embedding-0.6B"
DEFAULT_SV_CHAT_URL = "http://10.0.10.51:8000/v1/chat/completions"
DEFAULT_SV_CHAT_MODEL = "Qwen/Qwen3-VL-8B-Instruct"

RAW_SECTIONS_PATH = DATA / "xennials_raw_sections.json"
RAW_CHUNKS_PATH = DATA / "xennials_raw_chunks.json"
FACTOIDS_PATH = DATA / "xennials_factoids.json"
QA_PAIRS_PATH = DATA / "xennials_qa_pairs.json"
INDEX_PATH = DATA / "xennials_sv_embedding_index.json"

SKIP_HEADINGS = {
    "references",
    "external links",
    "further reading",
    "see also",
    "notes",
}


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def clean_text(text: str) -> str:
    text = html.unescape(text)
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    return value.strip("_") or "section"


class WikiArticleParser(HTMLParser):
    """Extract headings and paragraph/list text from Wikipedia article HTML."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.sections: list[dict[str, Any]] = []
        self.current_heading = "Lead"
        self.current_level = 1
        self.current_paragraphs: list[str] = []
        self.active_tag: str | None = None
        self.buffer: list[str] = []
        self.skip_depth = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_dict = dict(attrs)
        class_name = attrs_dict.get("class") or ""
        if tag in {"table", "style", "script"} or "navbox" in class_name or "infobox" in class_name:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag in {"h2", "h3", "h4", "p", "li"}:
            self.active_tag = tag
            self.buffer = []

    def handle_endtag(self, tag: str) -> None:
        if self.skip_depth:
            if tag in {"table", "style", "script"}:
                self.skip_depth = max(0, self.skip_depth - 1)
            return
        if tag != self.active_tag:
            return
        text = clean_text(" ".join(self.buffer))
        self.active_tag = None
        self.buffer = []
        if not text:
            return

        if tag in {"h2", "h3", "h4"}:
            heading = re.sub(r"\s*edit\s*$", "", text, flags=re.IGNORECASE).strip()
            if heading.lower() in SKIP_HEADINGS:
                self.flush_section()
                self.current_heading = heading
                self.current_paragraphs = []
                self.current_level = int(tag[-1])
                return
            self.flush_section()
            self.current_heading = heading
            self.current_level = int(tag[-1])
            return

        if self.current_heading.lower() not in SKIP_HEADINGS and len(text.split()) >= 6:
            self.current_paragraphs.append(text)

    def handle_data(self, data: str) -> None:
        if self.skip_depth or not self.active_tag:
            return
        self.buffer.append(data)

    def close(self) -> None:
        super().close()
        self.flush_section()

    def flush_section(self) -> None:
        if not self.current_paragraphs:
            return
        section_id = slugify(self.current_heading)
        self.sections.append(
            {
                "section_id": section_id,
                "heading": self.current_heading,
                "level": self.current_level,
                "paragraphs": self.current_paragraphs,
                "text": "\n\n".join(self.current_paragraphs),
            }
        )
        self.current_paragraphs = []


def fetch_wikipedia_html(title: str) -> str:
    params = urllib.parse.urlencode(
        {
            "action": "parse",
            "page": title,
            "format": "json",
            "prop": "text",
            "formatversion": "2",
        }
    )
    request = urllib.request.Request(
        f"{MEDIAWIKI_API}?{params}",
        headers={"User-Agent": "LLM-RAG-Bootcamp-FactoidWiki/0.1"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if "error" in payload:
        raise RuntimeError(payload["error"])
    return payload["parse"]["text"]


def ingest(title: str = DEFAULT_TITLE, source_url: str = DEFAULT_SOURCE_URL) -> dict[str, Any]:
    article_html = fetch_wikipedia_html(title)
    parser = WikiArticleParser()
    parser.feed(article_html)
    parser.close()

    payload = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "title": title,
        "source_url": source_url,
        "sections": parser.sections,
    }
    write_json(RAW_SECTIONS_PATH, payload)
    chunks = build_chunks_from_sections(payload)
    write_json(RAW_CHUNKS_PATH, chunks)
    return chunks


def approximate_tokens(text: str) -> list[str]:
    return re.findall(r"\w+|[^\w\s]", text)


def build_chunks_from_sections(sections_payload: dict[str, Any], max_tokens: int = 360) -> dict[str, Any]:
    chunks: list[dict[str, Any]] = []
    for section in sections_payload["sections"]:
        current: list[str] = []
        current_tokens = 0
        part = 1
        for paragraph in section["paragraphs"]:
            paragraph_tokens = len(approximate_tokens(paragraph))
            if current and current_tokens + paragraph_tokens > max_tokens:
                chunks.append(make_chunk(sections_payload, section, current, part))
                part += 1
                current = []
                current_tokens = 0
            current.append(paragraph)
            current_tokens += paragraph_tokens
        if current:
            chunks.append(make_chunk(sections_payload, section, current, part))

    return {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "title": sections_payload["title"],
        "source_url": sections_payload["source_url"],
        "chunking_strategy": "section-aware paragraph grouping with max token guardrail",
        "max_tokens": max_tokens,
        "chunks": chunks,
    }


def make_chunk(
    sections_payload: dict[str, Any],
    section: dict[str, Any],
    paragraphs: list[str],
    part: int,
) -> dict[str, Any]:
    chunk_id = f"xennials_{section['section_id']}_{part:02d}"
    section_anchor = section["heading"].replace(" ", "_")
    return {
        "chunk_id": chunk_id,
        "source_id": "xennials_wikipedia",
        "title": sections_payload["title"],
        "section": section["heading"],
        "section_id": section["section_id"],
        "part": part,
        "chunk_text": "\n\n".join(paragraphs),
        "source_url": f"{sections_payload['source_url']}#{section_anchor}" if section["heading"] != "Lead" else sections_payload["source_url"],
    }


def parse_chat_response(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        raise ValueError("Chat response did not include choices.")
    message = choices[0].get("message") or {}
    content = message.get("content") or message.get("reasoning_content") or message.get("reasoning")
    if not isinstance(content, str):
        raise ValueError("Chat response did not include message.content.")
    return content.strip()


def chat_complete(messages: list[dict[str, str]], max_tokens: int = 1200, temperature: float = 0.1) -> str:
    endpoint = os.environ.get("SV_CHAT_URL", DEFAULT_SV_CHAT_URL)
    model = os.environ.get("SV_CHAT_MODEL", DEFAULT_SV_CHAT_MODEL)
    body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return parse_chat_response(payload)


def extract_json_array(text: str, allow_repair: bool = True) -> list[Any]:
    stripped = text.strip()
    stripped = re.sub(r"^```(?:json)?", "", stripped, flags=re.IGNORECASE).strip()
    stripped = re.sub(r"```$", "", stripped).strip()
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not parse JSON array from model output: {text[:240]}")
    candidate = stripped[start : end + 1]
    try:
        parsed = json.loads(candidate)
    except json.JSONDecodeError:
        if not allow_repair:
            raise
        repaired = chat_complete(
            [
                {
                    "role": "system",
                    "content": (
                        "Repair the user's malformed JSON into a valid JSON array. "
                        "Return only valid JSON. Do not add markdown fences or commentary."
                    ),
                },
                {"role": "user", "content": candidate},
            ],
            max_tokens=1800,
            temperature=0.0,
        )
        return extract_json_array(repaired, allow_repair=False)
    if not isinstance(parsed, list):
        raise ValueError("Expected JSON array.")
    return parsed


def parse_factoid_lines(text: str) -> list[dict[str, Any]]:
    """Parse robust line-oriented factoid output.

    Expected line shape:
        factoid text || keyword1, keyword2 || question1; question2
    """
    rows: list[dict[str, Any]] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        line = re.sub(r"^[-*\d.)\s]+", "", line).strip()
        if not line or "||" not in line:
            continue
        parts = [part.strip() for part in line.split("||")]
        if len(parts) < 1 or not parts[0]:
            continue
        keywords = []
        questions = []
        if len(parts) >= 2:
            keywords = [item.strip() for item in parts[1].split(",") if item.strip()]
        if len(parts) >= 3:
            questions = [item.strip() for item in re.split(r";|\|", parts[2]) if item.strip()]
        rows.append(
            {
                "factoid_text": parts[0],
                "keywords": keywords,
                "questions": questions,
            }
        )
    return rows


def generate_factoids(max_chunks: int | None = None) -> dict[str, Any]:
    chunks_payload = read_json(RAW_CHUNKS_PATH)
    chunks = chunks_payload["chunks"][:max_chunks] if max_chunks else chunks_payload["chunks"]
    factoids: list[dict[str, Any]] = []

    for chunk in chunks:
        messages = [
            {
                "role": "system",
                "content": (
                    "You extract FactoidWiki-style factoids from source text. "
                    "Return plain text only, one factoid per line, with this exact delimiter format:\n"
                    "factoid text || keyword1, keyword2 || question1; question2\n"
                    "Each factoid must be atomic, self-contained, specific, and fully supported by the source. "
                    "Do not add facts not present in the source. Do not use markdown or numbering."
                ),
            },
            {
                "role": "user",
                "content": (
                    "Extract 4 to 8 factoids from this Wikipedia chunk.\n\n"
                    f"Article: {chunk['title']}\n"
                    f"Section: {chunk['section']}\n"
                    f"Chunk id: {chunk['chunk_id']}\n\n"
                    f"Text:\n{chunk['chunk_text']}"
                ),
            },
        ]
        output = chat_complete(messages, max_tokens=1400, temperature=0.1)
        parsed_factoids = parse_factoid_lines(output)
        if not parsed_factoids:
            raise ValueError(f"Could not parse factoid lines from model output: {output[:240]}")
        for index, item in enumerate(parsed_factoids, start=1):
            text = str(item.get("factoid_text") or "").strip()
            if not text:
                continue
            factoids.append(
                {
                    "factoid_id": f"fact_{chunk['chunk_id']}_{index:02d}",
                    "source_id": "xennials_wikipedia",
                    "source_chunk_id": chunk["chunk_id"],
                    "section": chunk["section"],
                    "factoid_text": text,
                    "keywords": [str(v) for v in item.get("keywords", []) if str(v).strip()],
                    "questions": [str(v) for v in item.get("questions", []) if str(v).strip()],
                    "source_url": chunk["source_url"],
                    "generated_by": os.environ.get("SV_CHAT_MODEL", DEFAULT_SV_CHAT_MODEL),
                }
            )

    payload = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "artifact_type": "factoids",
        "source_url": chunks_payload["source_url"],
        "factoids": factoids,
    }
    write_json(FACTOIDS_PATH, payload)
    return payload


def generate_qa_pairs() -> dict[str, Any]:
    factoids_payload = read_json(FACTOIDS_PATH)
    qa_pairs: list[dict[str, Any]] = []
    for factoid in factoids_payload["factoids"]:
        questions = factoid.get("questions") or []
        if not questions:
            messages = [
                {
                    "role": "system",
                    "content": "Generate two realistic user questions answered by the factoid. Return only a JSON array of strings.",
                },
                {"role": "user", "content": factoid["factoid_text"]},
            ]
            questions = [str(item) for item in extract_json_array(chat_complete(messages, max_tokens=400))]
        for index, question in enumerate(questions[:3], start=1):
            qa_pairs.append(
                {
                    "qa_id": f"qa_{factoid['factoid_id']}_{index}",
                    "source_id": "xennials_wikipedia",
                    "factoid_id": factoid["factoid_id"],
                    "source_chunk_id": factoid["source_chunk_id"],
                    "section": factoid["section"],
                    "question": question,
                    "answer": factoid["factoid_text"],
                    "keywords": factoid.get("keywords", []),
                    "source_url": factoid["source_url"],
                    "generated_by": factoid.get("generated_by"),
                }
            )

    payload = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "artifact_type": "qa_pairs",
        "source_url": factoids_payload["source_url"],
        "qa_pairs": qa_pairs,
    }
    write_json(QA_PAIRS_PATH, payload)
    return payload


def normalize_vector(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if not norm:
        return vector
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def parse_embedding_response(payload: Any) -> list[list[float]]:
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        vectors = []
        for item in payload["data"]:
            embedding = item.get("embedding") if isinstance(item, dict) else None
            if isinstance(embedding, list):
                vectors.append([float(v) for v in embedding])
        if vectors:
            return vectors
    if isinstance(payload, dict) and isinstance(payload.get("embeddings"), list):
        return [[float(v) for v in vector] for vector in payload["embeddings"]]
    raise ValueError("Unsupported embedding response shape.")


def embed_texts(texts: list[str], batch_size: int = 16) -> list[list[float]]:
    endpoint = os.environ.get("SV_EMBEDDING_URL", DEFAULT_SV_EMBED_URL)
    model = os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_EMBED_MODEL)
    vectors: list[list[float]] = []
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        body = json.dumps({"model": model, "input": batch}).encode("utf-8")
        request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(request, timeout=180) as response:
            vectors.extend(parse_embedding_response(json.loads(response.read().decode("utf-8"))))
    if len(vectors) != len(texts):
        raise ValueError(f"Expected {len(texts)} embeddings, got {len(vectors)}")
    return [normalize_vector(vector) for vector in vectors]


def index_text(*parts: Any) -> str:
    flattened: list[str] = []
    for part in parts:
        if isinstance(part, list):
            flattened.append(" ".join(str(v) for v in part))
        elif part:
            flattened.append(str(part))
    return " ".join(flattened)


def make_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    chunks = read_json(RAW_CHUNKS_PATH)["chunks"]
    for chunk in chunks:
        records.append(
            {
                "record_id": chunk["chunk_id"],
                "artifact_type": "raw_chunk",
                "source_id": chunk["source_id"],
                "section": chunk["section"],
                "title": f"{chunk['title']} / {chunk['section']}",
                "index_text": index_text(chunk["section"], chunk["chunk_text"]),
                "display_text": chunk["chunk_text"],
                "source_url": chunk["source_url"],
            }
        )

    factoids = read_json(FACTOIDS_PATH)["factoids"]
    for factoid in factoids:
        records.append(
            {
                "record_id": factoid["factoid_id"],
                "artifact_type": "factoid",
                "source_id": factoid["source_id"],
                "section": factoid["section"],
                "title": "Factoid",
                "index_text": index_text(factoid["factoid_text"], factoid.get("keywords"), factoid.get("questions")),
                "display_text": factoid["factoid_text"],
                "source_url": factoid["source_url"],
            }
        )

    qa_pairs = read_json(QA_PAIRS_PATH)["qa_pairs"]
    for qa in qa_pairs:
        records.append(
            {
                "record_id": qa["qa_id"],
                "artifact_type": "qa_pair",
                "source_id": qa["source_id"],
                "section": qa["section"],
                "title": qa["question"],
                "index_text": index_text(qa["question"], qa["answer"], qa.get("keywords")),
                "display_text": qa["answer"],
                "source_url": qa["source_url"],
                "factoid_id": qa["factoid_id"],
            }
        )

    return records


def build_index() -> dict[str, Any]:
    records = make_records()
    vectors = embed_texts([record["index_text"] for record in records])
    indexed = []
    for record, vector in zip(records, vectors):
        indexed.append({**record, "vector": vector})

    payload = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "artifact_type": "sv_embedding_index",
        "embedding_model": os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_EMBED_MODEL),
        "record_count": len(indexed),
        "vector_dimensions": len(indexed[0]["vector"]) if indexed else 0,
        "records": indexed,
    }
    write_json(INDEX_PATH, payload)
    return payload


def search(query: str, top_k: int = 8) -> list[dict[str, Any]]:
    index = read_json(INDEX_PATH)
    query_vector = embed_texts([query], batch_size=1)[0]
    results = []
    for record in index["records"]:
        results.append(
            {
                key: value
                for key, value in record.items()
                if key not in {"vector", "index_text"}
            }
            | {"score": cosine(query_vector, record["vector"])}
        )
    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:top_k]


def answer(query: str, top_k: int = 6) -> dict[str, Any]:
    results = search(query, top_k=top_k)
    evidence = "\n\n".join(
        f"[{index}] {item['artifact_type']} / {item['record_id']}\n"
        f"Section: {item['section']}\n"
        f"Source: {item['source_url']}\n"
        f"Evidence: {item['display_text']}"
        for index, item in enumerate(results, start=1)
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You answer from a mini FactoidWiki. Use only the provided evidence. "
                "If the evidence is insufficient, say what is missing. Cite evidence ids like [1]."
            ),
        },
        {"role": "user", "content": f"Question: {query}\n\nEvidence:\n{evidence}\n\nAnswer:"},
    ]
    return {
        "query": query,
        "answer": chat_complete(messages, max_tokens=800, temperature=0.1),
        "results": results,
    }


def run_all(max_chunks: int | None = None) -> None:
    chunks = ingest()
    print(f"Ingested {len(chunks['chunks'])} raw chunks.")
    factoids = generate_factoids(max_chunks=max_chunks)
    print(f"Generated {len(factoids['factoids'])} factoids.")
    qa = generate_qa_pairs()
    print(f"Generated {len(qa['qa_pairs'])} QA pairs.")
    index = build_index()
    print(f"Built embedding index with {index['record_count']} records and {index['vector_dimensions']} dimensions.")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["ingest", "factoids", "qa", "index", "search", "answer", "all"])
    parser.add_argument("query", nargs="?", default="What birth years are commonly used for Xennials?")
    parser.add_argument("--max-chunks", type=int, default=None, help="Limit factoid generation for quick tests.")
    parser.add_argument("--top-k", type=int, default=8)
    args = parser.parse_args()

    try:
        if args.command == "ingest":
            payload = ingest()
            print(f"Wrote {RAW_SECTIONS_PATH} and {RAW_CHUNKS_PATH}; chunks={len(payload['chunks'])}")
        elif args.command == "factoids":
            payload = generate_factoids(max_chunks=args.max_chunks)
            print(f"Wrote {FACTOIDS_PATH}; factoids={len(payload['factoids'])}")
        elif args.command == "qa":
            payload = generate_qa_pairs()
            print(f"Wrote {QA_PAIRS_PATH}; qa_pairs={len(payload['qa_pairs'])}")
        elif args.command == "index":
            payload = build_index()
            print(f"Wrote {INDEX_PATH}; records={payload['record_count']}; dims={payload['vector_dimensions']}")
        elif args.command == "search":
            print(json.dumps(search(args.query, top_k=args.top_k), ensure_ascii=False, indent=2))
        elif args.command == "answer":
            print(json.dumps(answer(args.query, top_k=args.top_k), ensure_ascii=False, indent=2))
        elif args.command == "all":
            run_all(max_chunks=args.max_chunks)
    except urllib.error.URLError as exc:
        print(f"Network error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
