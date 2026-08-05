#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""Qdrant vector database storage manager."""

from typing import List, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

from svrag.models import EnrichedChunk


class QdrantStorage:
    """Class for managing Qdrant vector database operations.
    
    This class handles the storage and retrieval of embeddings in Qdrant,
    including collection creation and point insertion.
    
    Attributes:
        client: QdrantClient instance
        collection_name: Name of the Qdrant collection
        host: Qdrant server host
        port: Qdrant server port
    """
    
    def __init__(
        self, 
        collection_name: str = "supportvectors_ai_knowledge_base",
        host: str = "localhost",
        port: int = 6333
    ):
        """Initialize Qdrant storage client.
        
        Args:
            collection_name: Name of the collection to use/create
            host: Qdrant server host address
            port: Qdrant server port
        """
        self.collection_name = collection_name
        self.host = host
        self.port = port
        self.client = QdrantClient(host=host, port=port)
    
    def create_collection(self, vector_size: int = 768):
        """Create a new collection in Qdrant if it doesn't exist.
        
        Args:
            vector_size: Size of the embedding vectors (default: 768 for jina-embeddings-v2-base-en)
        """
        try:
            self.client.get_collection(self.collection_name)
        except Exception:
            # Collection doesn't exist, create it
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )
    
    def insert_chunks(
        self, 
        enriched_chunks: List[EnrichedChunk],
        start_id: int = 0,
        batch_size: int = 1000
    ) -> int:
        """Insert enriched chunks into Qdrant in batches.
        
        Args:
            enriched_chunks: List of EnrichedChunk objects to insert
            start_id: Starting ID for the points (default: 0)
            batch_size: Number of chunks to insert per batch (default: 1000)
            
        Returns:
            The next available ID after insertion
        """
        current_id = start_id
        total_chunks = len(enriched_chunks)
        
        # Process chunks in batches
        for batch_start in range(0, total_chunks, batch_size):
            batch_end = min(batch_start + batch_size, total_chunks)
            batch_chunks = enriched_chunks[batch_start:batch_end]
            
            points = []
            for chunk in batch_chunks:
                point = PointStruct(
                    id=current_id,
                    vector=chunk.embedding,
                    payload={
                        "semantic_id": chunk.semantic_id,
                        "parent_id": chunk.parent_id,
                        "parent_text": chunk.parent_text,
                        "text": chunk.text,
                        "num_tokens": chunk.num_tokens,
                        "pdf_name": chunk.pdf_name,
                        "folder_name": chunk.folder_name,
                    }
                )
                points.append(point)
                current_id += 1
            
            # Insert batch
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
        
        return current_id
    
    def search(
        self, 
        query_vector: List[float], 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search for similar chunks in Qdrant.
        
        Args:
            query_vector: Query embedding vector
            limit: Maximum number of results to return
            
        Returns:
            List of search results with scores and payloads
        """
    
        query_response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit
        )
        
        return [
            {
                "score": point.score,
                "payload": point.payload
            }
            for point in query_response.points
        ]

