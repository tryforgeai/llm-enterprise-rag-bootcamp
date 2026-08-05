#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
from dataclasses import dataclass
from typing import Any, List

from svrag.late_chunk_embedder import LateChunkEmbedder
from svrag.qdrant_storage import QdrantStorage


@dataclass(frozen=True)
class RetrievedChunk:
    """One hit from Qdrant with semantic chunk text and parent context.

    Attributes:
        chunk_text: Semantic chunk body (Qdrant payload ``text``).
        parent_chunk_text: Full parent section (Qdrant payload ``parent_text``).
        similarity_score: Nearest-neighbor score from vector search.
    """

    chunk_text: str
    parent_chunk_text: str
    similarity_score: float


class ExploratoryRetriever:
    """Retrieves extra evidence from the sv-rag-pipeline Qdrant index for ungrounded claims.

    Embeds the claim with the same :class:`LateChunkEmbedder` used at index time, queries
    the configured collection, and returns the top-``top_k`` neighbors with chunk and
    parent text from point payloads.
    """

    def __init__(
        self,
        qdrant_storage: QdrantStorage,
        embedder: LateChunkEmbedder,
        top_k: int = 3,
    ) -> None:
        """Wire Qdrant access, the query embedder, and result size.

        Args:
            qdrant_storage: Client bound to the RAG collection (see :class:`QdrantStorage`).
            embedder: Produces query vectors compatible with stored chunk embeddings.
            top_k: Maximum number of nearest chunks to return per claim.
        """
        self._storage = qdrant_storage
        self._embedder = embedder
        self.top_k = top_k

    def retrieve(self, claim: str) -> List[RetrievedChunk]:
        """Return the nearest Qdrant chunks for the claim.

        Args:
            claim: Claim text used as the retrieval query.

        Returns:
            Up to ``top_k`` results ordered by descending similarity. Payload fields
            ``text`` and ``parent_text`` are exposed as ``chunk_text`` and
            ``parent_chunk_text``.
        """
        query_vector = self._embedder.encode_query(claim)
        raw_hits: List[dict[str, Any]] = self._storage.search(
            query_vector, limit=self.top_k
        )
        chunks: List[RetrievedChunk] = []
        for hit in raw_hits:
            payload = hit.get("payload") or {}
            score = float(hit["score"]) if hit.get("score") is not None else 0.0
            chunk_text = str(payload.get("text") or "")
            parent_chunk_text = str(payload.get("parent_text") or "")
            chunks.append(
                RetrievedChunk(
                    chunk_text=chunk_text,
                    parent_chunk_text=parent_chunk_text,
                    similarity_score=score,
                )
            )
        return chunks
