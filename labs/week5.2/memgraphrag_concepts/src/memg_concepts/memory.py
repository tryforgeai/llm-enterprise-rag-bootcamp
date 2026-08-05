#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Three-layer global memory for MemGraphRAG concept demos."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from memg_concepts.models import FactTriple, Passage, SchemaTriple


@dataclass
class GlobalMemory:
    passages: dict[str, Passage] = field(default_factory=dict)
    schemas: dict[str, SchemaTriple] = field(default_factory=dict)
    schema_freq: Counter[str] = field(default_factory=Counter)
    facts: dict[str, FactTriple] = field(default_factory=dict)
    fact_to_passage: dict[str, str] = field(default_factory=dict)
    schema_to_facts: dict[str, set[str]] = field(default_factory=lambda: defaultdict(set))

    def add_passage(self, passage: Passage) -> None:
        self.passages[passage.passage_id] = passage

    def add_schema(self, schema: SchemaTriple) -> None:
        key = schema.key()
        self.schemas[key] = schema
        self.schema_freq[key] += 1

    def add_fact(self, fact: FactTriple) -> None:
        key = fact.key()
        self.facts[key] = fact
        self.fact_to_passage[key] = fact.passage_id
        schema_key = SchemaTriple(
            head_type=fact.head_type,
            relation=fact.relation,
            tail_type=fact.tail_type,
        ).key()
        self.schema_to_facts[schema_key].add(key)

    def derive_schemas(self) -> None:
        """Rebuild the schema layer programmatically from current facts.

        The LLM never emits schemas directly. Instead, each surviving fact
        ``(head:head_type, relation, tail:tail_type)`` is abstracted to the
        schema ``(head_type, relation, tail_type)``. Schema *frequency* is the
        number of distinct passages that support the pattern, which preserves
        the "appears across multiple passages" semantics used by
        :meth:`stable_schemas`.
        """
        self.schemas.clear()
        self.schema_freq.clear()
        self.schema_to_facts = defaultdict(set)
        passages_per_schema: dict[str, set[str]] = defaultdict(set)
        for fact_key, fact in self.facts.items():
            schema = SchemaTriple(
                head_type=fact.head_type,
                relation=fact.relation,
                tail_type=fact.tail_type,
            )
            schema_key = schema.key()
            self.schemas[schema_key] = schema
            self.schema_to_facts[schema_key].add(fact_key)
            passages_per_schema[schema_key].add(fact.passage_id)
        for schema_key, passage_ids in passages_per_schema.items():
            self.schema_freq[schema_key] = len(passage_ids)

    def stable_schemas(self, min_freq: int = 2) -> dict[str, SchemaTriple]:
        return {
            key: schema
            for key, schema in self.schemas.items()
            if self.schema_freq[key] >= min_freq
        }

    def active_facts(self, min_schema_freq: int = 2) -> dict[str, FactTriple]:
        stable = set(self.stable_schemas(min_schema_freq))
        active: dict[str, FactTriple] = {}
        for fact_key, fact in self.facts.items():
            schema_key = SchemaTriple(
                head_type=fact.head_type,
                relation=fact.relation,
                tail_type=fact.tail_type,
            ).key()
            if schema_key in stable or self.schema_freq[schema_key] >= min_schema_freq:
                active[fact_key] = fact
        return active

    def detect_conflicts(self, similarity_threshold: float = 0.85) -> list[set[str]]:
        """Group facts that share head entity and relation but disagree on tail."""
        buckets: dict[tuple[str, str], list[str]] = defaultdict(list)
        for key, fact in self.facts.items():
            buckets[(fact.head_entity.lower(), fact.relation)].append(key)

        groups: list[set[str]] = []
        for keys in buckets.values():
            if len(keys) < 2:
                continue
            tails = {self.facts[k].tail_entity.lower() for k in keys}
            if len(tails) > 1:
                groups.append(set(keys))
        return groups

    def resolve_conflicts(self, groups: list[set[str]]) -> list[str]:
        """Keep the fact supported by the longest passage evidence."""
        removed: list[str] = []
        for group in groups:
            ranked = sorted(
                group,
                key=lambda key: len(self.passages[self.fact_to_passage[key]].text),
                reverse=True,
            )
            for key in ranked[1:]:
                self.facts.pop(key, None)
                self.fact_to_passage.pop(key, None)
                removed.append(key)
        return removed

    def summary(self, min_schema_freq: int = 2) -> dict[str, int]:
        return {
            "passages": len(self.passages),
            "schemas": len(self.schemas),
            "stable_schemas": len(self.stable_schemas(min_freq=min_schema_freq)),
            "facts": len(self.facts),
            "active_facts": len(self.active_facts(min_schema_freq=min_schema_freq)),
        }
