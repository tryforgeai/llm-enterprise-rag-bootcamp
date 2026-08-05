#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#  -------------------------------------------------------------------------------------------------
"""Question answering over memory-guided retrieval results."""

from __future__ import annotations

from dataclasses import dataclass

from memg_concepts.graph_builder import IndexingGraph
from memg_concepts.llm import chat_completion
from memg_concepts.memory import GlobalMemory
from memg_concepts.retrieval import RetrievedEvidence


@dataclass(frozen=True)
class QAResult:
    question: str
    answer: str
    context: str
    passage_ids: list[str]
    entity_ids: list[str]


def build_context(
    evidence: RetrievedEvidence,
    memory: GlobalMemory,
    graph: IndexingGraph,
) -> str:
    passage_blocks = []
    for passage_id in evidence.passage_ids:
        passage = memory.passages[passage_id]
        passage_blocks.append(f"[{passage_id}] {passage.text}")

    entity_blocks = []
    for entity_id in evidence.entity_ids:
        node = graph.nodes[entity_id]
        entity_blocks.append(f"- {node.label} ({node.metadata.get('entity_type', 'entity')})")

    return (
        "Retrieved passages:\n"
        + "\n\n".join(passage_blocks)
        + "\n\nRelevant entities:\n"
        + "\n".join(entity_blocks)
    )


def answer_question(
    question: str,
    evidence: RetrievedEvidence,
    memory: GlobalMemory,
    graph: IndexingGraph,
) -> QAResult:
    context = build_context(evidence, memory, graph)
    answer = chat_completion(
        [
            {
                "role": "system",
                "content": (
                    "Answer the question using only the retrieved graph-grounded context. "
                    "Be concise and cite passage ids when possible."
                ),
            },
            {
                "role": "user",
                "content": f"Question: {question}\n\nContext:\n{context}",
            },
        ],
        max_tokens=2048,
    )
    return QAResult(
        question=question,
        answer=answer,
        context=context,
        passage_ids=evidence.passage_ids,
        entity_ids=evidence.entity_ids,
    )
