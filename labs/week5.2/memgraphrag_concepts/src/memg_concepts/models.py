#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Core data models for MemGraphRAG three-layer memory and indexing graph."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal


class NodeKind(str, Enum):
    TYPE = "type"
    ENTITY = "entity"
    PASSAGE = "passage"
    SCHEMA = "schema"


@dataclass(frozen=True)
class SchemaTriple:
    head_type: str
    relation: str
    tail_type: str

    def key(self) -> str:
        return f"({self.head_type}, {self.relation}, {self.tail_type})"


@dataclass(frozen=True)
class FactTriple:
    head_entity: str
    relation: str
    tail_entity: str
    head_type: str
    tail_type: str
    passage_id: str

    def key(self) -> str:
        return f"({self.head_entity}, {self.relation}, {self.tail_entity})"


@dataclass
class Passage:
    passage_id: str
    text: str
    source: str
    chunk_index: int


@dataclass
class GraphNode:
    node_id: str
    kind: NodeKind
    label: str
    metadata: dict = field(default_factory=dict)


@dataclass
class GraphEdge:
    source: str
    target: str
    relation: str
    weight: float = 1.0


EdgeKind = Literal[
    "instance_of",
    "schema_align",
    "fact_link",
    "evidence",
    "type_bridge",
    "similarity",
]
