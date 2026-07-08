#!/usr/bin/env python3
"""Real Week 04 RAG demo server backed by SV cluster embeddings.

Run from this directory:

    python3 server.py

Then open:

    http://127.0.0.1:4184/

The server keeps storage simple on purpose:
- artifacts live in ../artifacts/*.json
- real SV embedding index is written to ../artifacts/sv_embedding_index.json
- retrieval is cosine similarity over SV embedding vectors

No LLM generation is performed here. This version demonstrates the real
embedding/retrieval part of RAG; answer synthesis is an explicit next layer.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
WEEK_04 = HERE.parent
PROJECT_ROOT = WEEK_04.parents[1]
ARTIFACTS = WEEK_04 / "artifacts"
INDEX_PATH = ARTIFACTS / "sv_embedding_index.json"

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 4184
DEFAULT_SV_EMBED_URL = "http://10.0.10.51:8000/embed-text/v1/embeddings"
DEFAULT_SV_MODEL = "Qwen/Qwen3-Embedding-0.6B"
DEFAULT_SV_CHAT_URL = "http://10.0.10.51:8000/v1/chat/completions"
DEFAULT_SV_CHAT_MODEL = "openai/gpt-oss-20b"
GENERATED_QA_PATH = ARTIFACTS / "generated_qa_pairs_sv.json"


def load_env_file(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def load_local_env() -> None:
    for path in [PROJECT_ROOT / ".env", PROJECT_ROOT / ".env.local", WEEK_04 / ".env"]:
        load_env_file(path)


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def artifact_text(*parts: str | list[str] | None) -> str:
    flattened: list[str] = []
    for part in parts:
        if isinstance(part, list):
            flattened.append(" ".join(str(item) for item in part))
        elif part:
            flattened.append(str(part))
    return " ".join(flattened)


def make_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []

    for chunk in read_json(ARTIFACTS / "raw_chunks_sample.json")["chunks"]:
        records.append(
            {
                "record_id": chunk["chunk_id"],
                "artifact_type": "raw_chunk",
                "source_id": chunk["source_id"],
                "title": chunk["title"],
                "index_text": artifact_text(chunk["title"], chunk["chunk_text"], chunk.get("keywords")),
                "display_text": chunk["chunk_text"],
                "source_pointer": chunk["source_pointer"],
            }
        )

    for summary in read_json(ARTIFACTS / "abstractive_summaries.json")["summaries"]:
        records.append(
            {
                "record_id": summary["summary_id"],
                "artifact_type": "abstractive_summary",
                "source_id": summary["source_id"],
                "title": summary["title"],
                "index_text": artifact_text(
                    summary["title"],
                    summary["summary"],
                    summary.get("key_concepts"),
                    summary.get("retrieval_use"),
                ),
                "display_text": summary["summary"],
                "source_pointer": summary["source_pointer"],
            }
        )

    for proposition in read_json(ARTIFACTS / "dense_x_propositions.json")["propositions"]:
        records.append(
            {
                "record_id": proposition["proposition_id"],
                "artifact_type": "proposition",
                "source_id": "dense_x",
                "title": "Dense-X proposition",
                "index_text": artifact_text(proposition["text"], proposition.get("keywords")),
                "display_text": proposition["text"],
                "source_pointer": proposition["source_pointer"],
            }
        )

    for qa in read_json(ARTIFACTS / "qa_pairs.json")["qa_pairs"]:
        records.append(
            {
                "record_id": qa["qa_id"],
                "artifact_type": "qa_pair",
                "source_id": qa["source_id"],
                "title": qa["question"],
                "index_text": artifact_text(qa["question"], qa["answer"], qa.get("keywords")),
                "display_text": qa["answer"],
                "source_pointer": qa["source_pointer"],
                "artifact_pointer": qa.get("artifact_pointer"),
            }
        )

    if GENERATED_QA_PATH.exists():
        for qa in read_json(GENERATED_QA_PATH).get("qa_pairs", []):
            records.append(
                {
                    "record_id": qa["qa_id"],
                    "artifact_type": "qa_pair",
                    "source_id": qa["source_id"],
                    "title": qa["question"],
                    "index_text": artifact_text(qa["question"], qa["answer"], qa.get("keywords")),
                    "display_text": qa["answer"],
                    "source_pointer": qa["source_pointer"],
                    "generated_by": qa.get("generated_by"),
                }
            )

    return records


def normalize_vector(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector))
    if not norm:
        return vector
    return [value / norm for value in vector]


def cosine(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def parse_embedding_response(payload: Any) -> list[list[float]]:
    """Accept OpenAI-compatible and common lightweight embedding shapes."""
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        vectors = []
        for item in payload["data"]:
            if isinstance(item, dict) and isinstance(item.get("embedding"), list):
                vectors.append([float(value) for value in item["embedding"]])
        if vectors:
            return vectors

    if isinstance(payload, dict) and isinstance(payload.get("embeddings"), list):
        raw = payload["embeddings"]
        if raw and isinstance(raw[0], list):
            return [[float(value) for value in vector] for vector in raw]

    if isinstance(payload, list) and payload and isinstance(payload[0], list):
        return [[float(value) for value in vector] for vector in payload]

    raise ValueError(f"Unsupported embedding response shape: {type(payload).__name__}")


def parse_chat_response(payload: dict[str, Any]) -> str:
    choices = payload.get("choices") or []
    if not choices:
        raise ValueError("Chat response did not include choices.")
    message = choices[0].get("message") or {}
    content = message.get("content")
    if not isinstance(content, str):
        raise ValueError("Chat response did not include message.content.")
    return content.strip()


def chat_complete(
    messages: list[dict[str, str]],
    model: str,
    endpoint: str,
    max_tokens: int = 900,
    temperature: float = 0.2,
) -> str:
    headers = {"Content-Type": "application/json"}
    api_key = os.environ.get("SV_API_KEY") or os.environ.get("SUPPORTVECTORS_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    request_body = json.dumps(
        {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "stream": False,
        }
    ).encode("utf-8")
    request = urllib.request.Request(endpoint, data=request_body, headers=headers, method="POST")

    with urllib.request.urlopen(request, timeout=180) as response:
        payload = json.loads(response.read().decode("utf-8"))

    return parse_chat_response(payload)


def embed_texts(texts: list[str], model: str, endpoint: str, batch_size: int = 16) -> list[list[float]]:
    vectors: list[list[float]] = []
    headers = {"Content-Type": "application/json"}

    api_key = os.environ.get("SV_API_KEY") or os.environ.get("SUPPORTVECTORS_API_KEY")
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        request_body = json.dumps({"model": model, "input": batch}).encode("utf-8")
        request = urllib.request.Request(endpoint, data=request_body, headers=headers, method="POST")

        with urllib.request.urlopen(request, timeout=120) as response:
            response_payload = json.loads(response.read().decode("utf-8"))

        vectors.extend(parse_embedding_response(response_payload))

    if len(vectors) != len(texts):
        raise ValueError(f"Expected {len(texts)} vectors, got {len(vectors)}")

    return [normalize_vector(vector) for vector in vectors]


def build_sv_index(model: str, endpoint: str) -> dict[str, Any]:
    records = make_records()
    vectors = embed_texts([record["index_text"] for record in records], model=model, endpoint=endpoint)

    indexed_records = []
    for record, vector in zip(records, vectors):
        indexed_records.append({**record, "vector": vector})

    index = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "index_type": "sv_cluster_dense_embedding_cosine",
        "embedding_endpoint": endpoint,
        "embedding_model": model,
        "record_count": len(indexed_records),
        "vector_dimensions": len(indexed_records[0]["vector"]) if indexed_records else 0,
        "records": indexed_records,
    }
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return index


def load_sv_index() -> dict[str, Any] | None:
    if not INDEX_PATH.exists():
        return None
    return read_json(INDEX_PATH)


def retrieve(query: str, top_k: int, model: str, endpoint: str) -> dict[str, Any]:
    index = load_sv_index()
    if not index:
        raise FileNotFoundError("SV embedding index does not exist yet. Build the index first.")

    query_vector = embed_texts([query], model=model, endpoint=endpoint, batch_size=1)[0]
    ranked = []
    for record in index["records"]:
        ranked.append(
            {
                key: value
                for key, value in record.items()
                if key not in {"vector", "index_text"}
            }
            | {"score": cosine(query_vector, record["vector"])}
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    top_results = ranked[:top_k]
    return {
        "query": query,
        "model": model,
        "endpoint": endpoint,
        "top_k": top_k,
        "results": top_results,
        "extractive_answer": make_extractive_answer(query, top_results[:3]),
    }


def make_extractive_answer(query: str, results: list[dict[str, Any]]) -> str:
    if not results:
        return "No evidence was retrieved."

    evidence_lines = []
    for index, item in enumerate(results, start=1):
        evidence_lines.append(
            f"{index}. [{item['artifact_type']}/{item['source_id']}] {item['display_text']}"
        )

    return (
        f"Query: {query}\n\n"
        "Retrieved evidence:\n"
        + "\n".join(evidence_lines)
        + "\n\nThis is the extractive evidence view. Use /api/answer or the UI's "
        "\"Synthesize answer\" button for SV chat model synthesis."
    )


def synthesize_answer(query: str, results: list[dict[str, Any]], model: str, endpoint: str) -> str:
    evidence = "\n\n".join(
        f"[{index}] {item['artifact_type']} / {item['source_id']} / {item['record_id']}\n"
        f"Source: {item['source_pointer']}\n"
        f"Evidence: {item['display_text']}"
        for index, item in enumerate(results, start=1)
    )
    messages = [
        {
            "role": "system",
            "content": (
                "You are a retrieval-grounded study assistant. Answer only from the provided evidence. "
                "If the evidence is insufficient, say what is missing. Include short source ids in brackets."
            ),
        },
        {
            "role": "user",
            "content": f"Question: {query}\n\nEvidence:\n{evidence}\n\nAnswer concisely.",
        },
    ]
    return chat_complete(messages=messages, model=model, endpoint=endpoint, max_tokens=700, temperature=0.1)


def extract_json_array(text: str) -> list[Any]:
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()
    start = stripped.find("[")
    end = stripped.rfind("]")
    if start == -1 or end == -1 or end <= start:
        raise ValueError(f"Could not find JSON array in LLM output: {text[:200]}")
    return json.loads(stripped[start : end + 1])


def generate_qa_pairs(model: str, endpoint: str, questions_per_chunk: int = 3) -> dict[str, Any]:
    raw_chunks = read_json(ARTIFACTS / "raw_chunks_sample.json")["chunks"]
    qa_pairs: list[dict[str, Any]] = []

    for chunk in raw_chunks:
        messages = [
            {
                "role": "system",
                "content": (
                    "Generate retrieval-oriented QA pairs from the source chunk. "
                    "Return only a JSON array. Each item must have question, answer, and keywords fields. "
                    "Questions should sound like realistic user queries. Answers must be fully supported by the chunk."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Create {questions_per_chunk} QA pairs for this chunk.\n\n"
                    f"Source id: {chunk['source_id']}\n"
                    f"Title: {chunk['title']}\n"
                    f"Chunk:\n{chunk['chunk_text']}"
                ),
            },
        ]
        output = chat_complete(messages=messages, model=model, endpoint=endpoint, max_tokens=900, temperature=0.2)
        generated = extract_json_array(output)
        for index, item in enumerate(generated, start=1):
            question = str(item.get("question") or "").strip()
            answer = str(item.get("answer") or "").strip()
            if not question or not answer:
                continue
            keywords = item.get("keywords") if isinstance(item.get("keywords"), list) else []
            qa_pairs.append(
                {
                    "qa_id": f"svqa_{chunk['chunk_id']}_{index}",
                    "source_id": chunk["source_id"],
                    "question": question,
                    "answer": answer,
                    "keywords": [str(keyword) for keyword in keywords],
                    "source_pointer": chunk["source_pointer"],
                    "source_chunk_id": chunk["chunk_id"],
                    "generated_by": model,
                }
            )

    artifact = {
        "created": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "artifact_type": "sv_generated_qa_pairs",
        "chat_endpoint": endpoint,
        "chat_model": model,
        "qa_pairs": qa_pairs,
    }
    GENERATED_QA_PATH.write_text(json.dumps(artifact, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return artifact


class Handler(SimpleHTTPRequestHandler):
    server_version = "Week04RealRAG/1.0"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, directory=str(HERE), **kwargs)

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            self.write_json(self.status_payload())
            return
        super().do_GET()

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        try:
            payload = self.read_payload()
            if parsed.path == "/api/build-index":
                model = payload.get("model") or os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_MODEL)
                endpoint = payload.get("endpoint") or os.environ.get("SV_EMBEDDING_URL", DEFAULT_SV_EMBED_URL)
                index = build_sv_index(model=model, endpoint=endpoint)
                self.write_json(
                    {
                        "ok": True,
                        "record_count": index["record_count"],
                        "vector_dimensions": index["vector_dimensions"],
                        "model": index["embedding_model"],
                        "endpoint": index["embedding_endpoint"],
                    }
                )
                return

            if parsed.path == "/api/generate-qa":
                model = payload.get("model") or os.environ.get("SV_CHAT_MODEL", DEFAULT_SV_CHAT_MODEL)
                endpoint = payload.get("endpoint") or os.environ.get("SV_CHAT_URL", DEFAULT_SV_CHAT_URL)
                questions_per_chunk = int(payload.get("questions_per_chunk") or 3)
                artifact = generate_qa_pairs(
                    model=model,
                    endpoint=endpoint,
                    questions_per_chunk=questions_per_chunk,
                )
                self.write_json(
                    {
                        "ok": True,
                        "qa_count": len(artifact["qa_pairs"]),
                        "model": model,
                        "endpoint": endpoint,
                        "path": str(GENERATED_QA_PATH),
                        "qa_pairs": artifact["qa_pairs"],
                    }
                )
                return

            if parsed.path == "/api/search":
                query = str(payload.get("query") or "").strip()
                if not query:
                    self.write_json({"ok": False, "error": "Missing query."}, status=400)
                    return
                top_k = int(payload.get("top_k") or 8)
                model = payload.get("model") or os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_MODEL)
                endpoint = payload.get("endpoint") or os.environ.get("SV_EMBEDDING_URL", DEFAULT_SV_EMBED_URL)
                result = retrieve(query=query, top_k=top_k, model=model, endpoint=endpoint)
                self.write_json({"ok": True, **result})
                return

            if parsed.path == "/api/answer":
                query = str(payload.get("query") or "").strip()
                if not query:
                    self.write_json({"ok": False, "error": "Missing query."}, status=400)
                    return
                top_k = int(payload.get("top_k") or 5)
                embed_model = payload.get("embed_model") or os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_MODEL)
                embed_endpoint = payload.get("embed_endpoint") or os.environ.get("SV_EMBEDDING_URL", DEFAULT_SV_EMBED_URL)
                chat_model = payload.get("chat_model") or os.environ.get("SV_CHAT_MODEL", DEFAULT_SV_CHAT_MODEL)
                chat_endpoint = payload.get("chat_endpoint") or os.environ.get("SV_CHAT_URL", DEFAULT_SV_CHAT_URL)
                result = retrieve(query=query, top_k=top_k, model=embed_model, endpoint=embed_endpoint)
                answer = synthesize_answer(
                    query=query,
                    results=result["results"],
                    model=chat_model,
                    endpoint=chat_endpoint,
                )
                self.write_json(
                    {
                        "ok": True,
                        **result,
                        "answer": answer,
                        "chat_model": chat_model,
                        "chat_endpoint": chat_endpoint,
                    }
                )
                return

            self.write_json({"ok": False, "error": f"Unknown endpoint: {parsed.path}"}, status=404)
        except urllib.error.URLError as exc:
            self.write_json({"ok": False, "error": f"Embedding endpoint error: {exc}"}, status=502)
        except Exception as exc:  # Keep local demo failures visible in the UI.
            self.write_json({"ok": False, "error": str(exc)}, status=500)

    def status_payload(self) -> dict[str, Any]:
        index = load_sv_index()
        return {
            "ok": True,
            "mode": "sv_cluster_embedding" if index else "no_sv_index_yet",
            "default_endpoint": os.environ.get("SV_EMBEDDING_URL", DEFAULT_SV_EMBED_URL),
            "default_model": os.environ.get("SV_EMBEDDING_MODEL", DEFAULT_SV_MODEL),
            "default_chat_endpoint": os.environ.get("SV_CHAT_URL", DEFAULT_SV_CHAT_URL),
            "default_chat_model": os.environ.get("SV_CHAT_MODEL", DEFAULT_SV_CHAT_MODEL),
            "index_exists": bool(index),
            "index_path": str(INDEX_PATH),
            "generated_qa_exists": GENERATED_QA_PATH.exists(),
            "generated_qa_path": str(GENERATED_QA_PATH),
            "record_count": index.get("record_count") if index else 0,
            "vector_dimensions": index.get("vector_dimensions") if index else 0,
        }

    def read_payload(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0"))
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def write_json(self, payload: dict[str, Any], status: int = 200) -> None:
        data = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    load_local_env()
    host = os.environ.get("WEEK04_RAG_HOST", DEFAULT_HOST)
    port = int(os.environ.get("WEEK04_RAG_PORT", DEFAULT_PORT))
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Week 04 real RAG demo: http://{host}:{port}/")
    print(f"SV embedding endpoint: {os.environ.get('SV_EMBEDDING_URL', DEFAULT_SV_EMBED_URL)}")
    print(f"SV embedding model: {os.environ.get('SV_EMBEDDING_MODEL', DEFAULT_SV_MODEL)}")
    print(f"SV chat endpoint: {os.environ.get('SV_CHAT_URL', DEFAULT_SV_CHAT_URL)}")
    print(f"SV chat model: {os.environ.get('SV_CHAT_MODEL', DEFAULT_SV_CHAT_MODEL)}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
        sys.exit(0)


if __name__ == "__main__":
    main()
