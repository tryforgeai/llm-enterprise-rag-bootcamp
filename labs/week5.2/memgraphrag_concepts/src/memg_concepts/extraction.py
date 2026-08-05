#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Two-stage OpenIE extraction for MemGraphRAG demos.

This module follows the OpenIE pipeline used by the reference MemGraphRAG /
HippoRAG implementation rather than jointly asking the LLM for schemas and
facts in a single call:

    Passage
        |
        v
    Named Entity Recognition (LLM call 1)
        |
        v
    RDF triple extraction        (LLM call 2)
        |
        v
    Entity typing                (LLM call 3)
        |
        v
    Facts  (head_entity, relation, tail_entity, head_type, tail_type)
        |
        v
    Schemas (head_type, relation, tail_type)   <-- derived programmatically

The LLM is never asked to "generate ontology schemas". Schemas (the abstract
`(head_type, relation, tail_type)` patterns) are constructed afterward by
abstracting typed facts to their entity types. See :func:`derive_schema_triples`
and :meth:`memg_concepts.memory.GlobalMemory.derive_schemas`.
"""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import BaseModel, Field

from memg_concepts.config import resolve_llm_settings
from memg_concepts.llm import make_openai_client
from memg_concepts.models import FactTriple, Passage, SchemaTriple


# ---------------------------------------------------------------------------
# Output models
# ---------------------------------------------------------------------------
class ExtractedFact(BaseModel):
    head_entity: str
    relation: str
    tail_entity: str
    head_type: str
    tail_type: str


class PassageExtraction(BaseModel):
    """Everything produced for a single passage.

    ``schemas`` are intentionally absent: they are not produced by the LLM and
    are derived downstream from the typed ``facts``.
    """

    named_entities: list[str] = Field(default_factory=list)
    open_triples: list[list[str]] = Field(default_factory=list)
    facts: list[ExtractedFact] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Prompts (mirroring the reference OpenIE prompts)
# ---------------------------------------------------------------------------
NER_SYSTEM_PROMPT = (
    "Your task is to extract named entities from the given paragraph. "
    "Respond with a JSON object with a single key 'named_entities' whose value "
    "is a list of entity strings."
)

NER_EXAMPLE_PASSAGE = (
    "Radio City is India's first private FM radio station and was started on "
    "3 July 2001. It plays Hindi, English and regional songs. Radio City "
    "recently forayed into New Media in May 2008 with the launch of a music "
    "portal - PlanetRadiocity.com."
)

NER_EXAMPLE_OUTPUT = {
    "named_entities": [
        "Radio City",
        "India",
        "3 July 2001",
        "Hindi",
        "English",
        "May 2008",
        "PlanetRadiocity.com",
    ]
}

TRIPLE_SYSTEM_PROMPT = (
    "Your task is to construct an RDF (Resource Description Framework) graph "
    "from the given passage and named entity list. Respond with a JSON object "
    "with a single key 'triples' whose value is a list of triples, where each "
    "triple is a list of exactly three strings [subject, predicate, object] "
    "representing a relationship in the RDF graph.\n\n"
    "Pay attention to the following requirements:\n"
    "- Each triple should contain at least one, but preferably two, of the "
    "named entities in the list.\n"
    "- Clearly resolve pronouns to their specific names to maintain clarity."
)

TRIPLE_EXAMPLE_OUTPUT = {
    "triples": [
        ["Radio City", "located in", "India"],
        ["Radio City", "is", "private FM radio station"],
        ["Radio City", "started on", "3 July 2001"],
        ["Radio City", "plays songs in", "Hindi"],
        ["Radio City", "plays songs in", "English"],
        ["Radio City", "forayed into", "New Media"],
        ["Radio City", "launched", "PlanetRadiocity.com"],
        ["PlanetRadiocity.com", "is", "music portal"],
    ]
}

TYPING_SYSTEM_PROMPT = (
    "Your task is to assign a short, general ontology type to each named "
    "entity. Use a lowercase snake_case single-token type such as: person, "
    "organization, model, method, mechanism, metric, dataset, task, tool, "
    "date, location, or concept. Respond with a JSON object with a single key "
    "'typed_entities' whose value is a list of objects, each with keys "
    "'entity' and 'entity_type'."
)

DEFAULT_ENTITY_TYPE = "concept"


def _chat(messages: list[dict[str, str]], *, max_tokens: int) -> str:
    """Plain chat completion returning raw assistant text.

    We deliberately avoid ``instructor``'s JSON-schema mode here: the local
    ``gpt-oss`` reasoning model tends to return empty or truncated ``content``
    under strict schema enforcement, whereas a plain completion reliably emits a
    JSON object (usually inside a ```json code fence).
    """
    settings = resolve_llm_settings()
    client = make_openai_client(settings)
    response = client.chat.completions.create(
        model=settings.model,
        messages=messages,
        temperature=settings.temperature,
        max_tokens=max_tokens,
    )
    return (response.choices[0].message.content or "").strip()


def _parse_json_object(text: str) -> dict[str, Any]:
    """Best-effort extraction of a single JSON object from model output."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```[a-zA-Z0-9]*\n?", "", cleaned)
        cleaned = re.sub(r"\n?```$", "", cleaned).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start != -1 and end != -1 and end > start:
        cleaned = cleaned[start : end + 1]
    parsed = json.loads(cleaned)
    if not isinstance(parsed, dict):
        raise ValueError("Expected a JSON object")
    return parsed


def _norm_relation(relation: str) -> str:
    return re.sub(r"\s+", "_", relation.strip().lower()).strip("_")


def _clean_triples(raw_triples: Any) -> list[list[str]]:
    """Normalize raw JSON triples into ``[subject, predicate, object]`` lists.

    Handles both list-form triples (``["a", "rel", "b"]``) and object-form
    triples (``{"subject": ..., "predicate": ..., "object": ...}``) that models
    sometimes emit despite the prompt.
    """
    cleaned: list[list[str]] = []
    if not isinstance(raw_triples, list):
        return cleaned
    for triple in raw_triples:
        parts: list[str] = []
        if isinstance(triple, dict):
            for key in ("subject", "predicate", "object"):
                if key in triple:
                    parts.append(str(triple[key]).strip())
        elif isinstance(triple, (list, tuple)):
            parts = [str(part).strip() for part in triple]
        if len(parts) == 3 and all(parts):
            cleaned.append(parts)
    return cleaned


# ---------------------------------------------------------------------------
# Stage 1 — Named Entity Recognition
# ---------------------------------------------------------------------------
def extract_named_entities(passage: Passage) -> list[str]:
    try:
        text = _chat(
            [
                {"role": "system", "content": NER_SYSTEM_PROMPT},
                {"role": "user", "content": NER_EXAMPLE_PASSAGE},
                {"role": "assistant", "content": json.dumps(NER_EXAMPLE_OUTPUT)},
                {"role": "user", "content": passage.text},
            ],
            max_tokens=2048,
        )
        data = _parse_json_object(text)
        raw = data.get("named_entities", [])
    except Exception:
        return _fallback_named_entities(passage)
    return _dedupe_preserve_order(str(e).strip() for e in raw if str(e).strip())


# ---------------------------------------------------------------------------
# Stage 2 — RDF triple extraction
# ---------------------------------------------------------------------------
def extract_open_triples(passage: Passage, entities: list[str]) -> list[list[str]]:
    user_prompt = (
        "Convert the paragraph into a JSON object with a 'triples' list. "
        "The paragraph and its named entity list are given below.\n\n"
        f"Paragraph:\n```\n{passage.text}\n```\n\n"
        f"Named entities:\n{json.dumps({'named_entities': entities})}"
    )
    try:
        text = _chat(
            [
                {"role": "system", "content": TRIPLE_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Convert the paragraph into a JSON object with a "
                        "'triples' list.\n\n"
                        f"Paragraph:\n```\n{NER_EXAMPLE_PASSAGE}\n```\n\n"
                        f"Named entities:\n{json.dumps(NER_EXAMPLE_OUTPUT)}"
                    ),
                },
                {"role": "assistant", "content": json.dumps(TRIPLE_EXAMPLE_OUTPUT)},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=4096,
        )
        data = _parse_json_object(text)
        raw_triples = data.get("triples", [])
    except Exception:
        return _fallback_triples(passage)
    return _clean_triples(raw_triples)


# ---------------------------------------------------------------------------
# Stage 3 — Entity typing
# ---------------------------------------------------------------------------
def type_entities(entities: list[str], passage: Passage | None = None) -> dict[str, str]:
    """Assign a coarse ontology type to each entity.

    Returns a mapping of ``entity_lowercase -> type``. Types are what later let
    us abstract facts into schemas; they are *not* an ontology emitted by the
    LLM in one shot, but a lightweight per-entity typing pass.
    """
    if not entities:
        return {}
    context = f"\n\nContext passage:\n```\n{passage.text}\n```" if passage else ""
    try:
        text = _chat(
            [
                {"role": "system", "content": TYPING_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Assign a type to each entity in the list.\n\n"
                        f"Entities:\n{json.dumps({'entities': entities})}{context}"
                    ),
                },
            ],
            max_tokens=2048,
        )
        data = _parse_json_object(text)
        raw_typed = data.get("typed_entities", [])
    except Exception:
        return _fallback_entity_types(entities)
    typed: dict[str, str] = {}
    for item in raw_typed:
        if not isinstance(item, dict):
            continue
        name = str(item.get("entity", "")).strip()
        etype = _norm_relation(str(item.get("entity_type", ""))) or DEFAULT_ENTITY_TYPE
        if name:
            typed[name.lower()] = etype
    for entity in entities:
        typed.setdefault(entity.strip().lower(), DEFAULT_ENTITY_TYPE)
    return typed


# ---------------------------------------------------------------------------
# Assembly — combine stages into typed facts
# ---------------------------------------------------------------------------
def _assemble_facts(
    triples: list[list[str]],
    entity_types: dict[str, str],
    entities: list[str],
) -> list[ExtractedFact]:
    entity_set = {e.strip().lower() for e in entities}
    facts: list[ExtractedFact] = []
    seen: set[tuple[str, str, str]] = set()
    for triple in triples:
        if len(triple) != 3:
            continue
        head, relation, tail = (part.strip() for part in triple)
        if not (head and relation and tail):
            continue
        # RDF requirement: a triple should mention at least one named entity.
        if entity_set and head.lower() not in entity_set and tail.lower() not in entity_set:
            continue
        norm_relation = _norm_relation(relation)
        dedupe_key = (head.lower(), norm_relation, tail.lower())
        if dedupe_key in seen:
            continue
        seen.add(dedupe_key)
        facts.append(
            ExtractedFact(
                head_entity=head,
                relation=norm_relation,
                tail_entity=tail,
                head_type=entity_types.get(head.lower(), DEFAULT_ENTITY_TYPE),
                tail_type=entity_types.get(tail.lower(), DEFAULT_ENTITY_TYPE),
            )
        )
    return facts


def extract_from_passage(passage: Passage) -> PassageExtraction:
    """Run the full NER -> triples -> typing pipeline for a passage."""
    entities = extract_named_entities(passage)
    triples = extract_open_triples(passage, entities)
    entity_types = type_entities(entities, passage)
    facts = _assemble_facts(triples, entity_types, entities)
    return PassageExtraction(
        named_entities=entities,
        open_triples=triples,
        facts=facts,
    )


# ---------------------------------------------------------------------------
# Fallbacks (used when the LLM / structured parsing is unavailable)
# ---------------------------------------------------------------------------
def _fallback_named_entities(passage: Passage) -> list[str]:
    """Grab capitalized spans as a crude NER stand-in."""
    candidates = re.findall(r"\b(?:[A-Z][\w.-]+(?:\s+[A-Z][\w.-]+)*)\b", passage.text)
    return _dedupe_preserve_order(c.strip() for c in candidates if len(c) > 1)[:20]


def _fallback_triples(passage: Passage) -> list[list[str]]:
    """Parse ``(a, rel, b)`` patterns straight from the text."""
    triples: list[list[str]] = []
    for match in re.findall(r"\(([^,]+),\s*([^,]+),\s*([^)]+)\)", passage.text):
        left, relation, right = (part.strip() for part in match)
        if left and relation and right:
            triples.append([left, relation, right])
    return triples[:8]


def _fallback_entity_types(entities: list[str]) -> dict[str, str]:
    return {entity.strip().lower(): DEFAULT_ENTITY_TYPE for entity in entities if entity.strip()}


def _dedupe_preserve_order(items) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            ordered.append(item)
    return ordered


# ---------------------------------------------------------------------------
# Conversions to core models
# ---------------------------------------------------------------------------
def to_fact_triples(items: list[ExtractedFact], passage_id: str) -> list[FactTriple]:
    return [
        FactTriple(
            head_entity=item.head_entity.strip(),
            relation=item.relation.strip().lower(),
            tail_entity=item.tail_entity.strip(),
            head_type=item.head_type.strip().lower(),
            tail_type=item.tail_type.strip().lower(),
            passage_id=passage_id,
        )
        for item in items
        if item.head_entity and item.relation and item.tail_entity
    ]


def derive_schema_triples(items: list[ExtractedFact]) -> list[SchemaTriple]:
    """Abstract typed facts into schema patterns.

    Schemas are *derived*, not generated: each fact ``(h:H, r, t:T)`` yields the
    schema ``(H, r, T)``. Duplicates are collapsed.
    """
    derived: dict[str, SchemaTriple] = {}
    for item in items:
        head_type = item.head_type.strip().lower()
        relation = item.relation.strip().lower()
        tail_type = item.tail_type.strip().lower()
        if not (head_type and relation and tail_type):
            continue
        schema = SchemaTriple(head_type=head_type, relation=relation, tail_type=tail_type)
        derived[schema.key()] = schema
    return list(derived.values())


def extraction_to_json(extraction: PassageExtraction) -> str:
    return json.dumps(extraction.model_dump(), indent=2)
