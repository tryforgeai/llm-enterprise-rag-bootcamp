#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Build the heterogeneous indexing graph from global memory."""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from memg_concepts.embeddings import EmbeddingModel
from memg_concepts.memory import GlobalMemory
from memg_concepts.models import GraphEdge, GraphNode, NodeKind, SchemaTriple


@dataclass
class IndexingGraph:
    nodes: dict[str, GraphNode] = field(default_factory=dict)
    edges: list[GraphEdge] = field(default_factory=list)

    def add_node(self, node: GraphNode) -> None:
        self.nodes[node.node_id] = node

    def add_edge(self, edge: GraphEdge) -> None:
        self.edges.append(edge)

    def node_ids(self) -> list[str]:
        return list(self.nodes.keys())

    def summary(self) -> dict[str, int]:
        counts = {kind.value: 0 for kind in NodeKind}
        for node in self.nodes.values():
            counts[node.kind.value] += 1
        return {"nodes": len(self.nodes), "edges": len(self.edges), **counts}


def _entity_id(name: str) -> str:
    return f"ent:{name.lower().replace(' ', '_')}"


def _type_id(name: str) -> str:
    return f"type:{name.lower().replace(' ', '_')}"


def _schema_id(schema: SchemaTriple) -> str:
    return f"schema:{schema.head_type}:{schema.relation}:{schema.tail_type}"


def build_indexing_graph(
    memory: GlobalMemory,
    *,
    embedder: EmbeddingModel | None = None,
    similarity_threshold: float = 0.82,
    min_schema_freq: int = 2,
) -> IndexingGraph:
    graph = IndexingGraph()
    active_facts = memory.active_facts(min_schema_freq=min_schema_freq)

    for passage in memory.passages.values():
        graph.add_node(
            GraphNode(
                node_id=passage.passage_id,
                kind=NodeKind.PASSAGE,
                label=passage.text[:80] + ("..." if len(passage.text) > 80 else ""),
                metadata={"chunk_index": passage.chunk_index},
            )
        )

    for schema in memory.stable_schemas(min_freq=min_schema_freq).values():
        graph.add_node(
            GraphNode(
                node_id=_schema_id(schema),
                kind=NodeKind.SCHEMA,
                label=schema.key(),
            )
        )
        graph.add_node(
            GraphNode(
                node_id=_type_id(schema.head_type),
                kind=NodeKind.TYPE,
                label=schema.head_type,
            )
        )
        graph.add_node(
            GraphNode(
                node_id=_type_id(schema.tail_type),
                kind=NodeKind.TYPE,
                label=schema.tail_type,
            )
        )
        graph.add_edge(
            GraphEdge(
                source=_schema_id(schema),
                target=_type_id(schema.head_type),
                relation="head_type",
            )
        )
        graph.add_edge(
            GraphEdge(
                source=_schema_id(schema),
                target=_type_id(schema.tail_type),
                relation="tail_type",
            )
        )

    entity_names: list[str] = []
    entity_ids: list[str] = []
    for fact in active_facts.values():
        head_id = _entity_id(fact.head_entity)
        tail_id = _entity_id(fact.tail_entity)
        for entity_id, label, entity_type in [
            (head_id, fact.head_entity, fact.head_type),
            (tail_id, fact.tail_entity, fact.tail_type),
        ]:
            if entity_id not in graph.nodes:
                graph.add_node(
                    GraphNode(
                        node_id=entity_id,
                        kind=NodeKind.ENTITY,
                        label=label,
                        metadata={"entity_type": entity_type},
                    )
                )
                entity_names.append(label)
                entity_ids.append(entity_id)

        graph.add_edge(
            GraphEdge(source=head_id, target=tail_id, relation=fact.relation)
        )
        graph.add_edge(
            GraphEdge(
                source=head_id,
                target=_type_id(fact.head_type),
                relation="instance_of",
            )
        )
        graph.add_edge(
            GraphEdge(
                source=tail_id,
                target=_type_id(fact.tail_type),
                relation="instance_of",
            )
        )
        graph.add_edge(
            GraphEdge(
                source=head_id,
                target=fact.passage_id,
                relation="evidence",
                weight=0.8,
            )
        )
        graph.add_edge(
            GraphEdge(
                source=tail_id,
                target=fact.passage_id,
                relation="evidence",
                weight=0.8,
            )
        )

    if embedder and len(entity_ids) >= 2:
        vectors = embedder.encode(entity_names)
        sim = vectors @ vectors.T
        for i in range(len(entity_ids)):
            for j in range(i + 1, len(entity_ids)):
                if sim[i, j] >= similarity_threshold:
                    graph.add_edge(
                        GraphEdge(
                            source=entity_ids[i],
                            target=entity_ids[j],
                            relation="similarity",
                            weight=float(sim[i, j]),
                        )
                    )

    return graph
