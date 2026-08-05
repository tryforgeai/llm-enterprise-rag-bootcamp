#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
"""FastAPI service for RAG-based response generation.

This module provides a REST API service that generates responses from user queries
using the SupportVectors RAG (Retrieval-Augmented Generation) system. The service
exposes endpoints for querying the knowledge base and retrieving relevant information
using semantic search and LLM-based generation.
"""

import os
from typing import Optional, List, Dict
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field

from svrag import SVRAG, LateChunkEmbedder, QdrantStorage
from svrag.models import RAGResponse, ReferencedChunk


# Request/Response Models
class QueryRequest(BaseModel):
    """Request model for query endpoint.
    
    Attributes:
        query: The user's natural language query string.
        similarity_threshold: Optional minimum similarity score for retrieved chunks.
            If not provided, uses the default from RAG system configuration.
        top_k: Optional maximum number of chunks to retrieve. If not provided,
            uses the default from RAG system configuration.
    """
    query: str = Field(..., description="The user's natural language query")
    similarity_threshold: Optional[float] = Field(
        default=0.7,
        ge=0.0,
        le=1.0,
        description="Minimum similarity score for retrieved chunks (0.0-1.0)"
    )
    top_k: Optional[int] = Field(
        default=5,
        ge=1,
        description="Maximum number of chunks to retrieve"
    )


class ReferencedChunkResponse(BaseModel):
    """Response model for referenced chunk information.
    
    Attributes:
        semantic_id: Unique identifier for the semantic chunk.
        parent_id: Identifier of the parent chunk.
        similarity_score: Similarity score from vector search (0.0-1.0).
        pdf_name: Name of the source PDF file.
        folder_name: Name of the folder containing the PDF.
        semantic_text: Text content of the semantic chunk.
        parent_text: Full text of the parent chunk.
    """
    semantic_id: int
    parent_id: int
    similarity_score: float
    pdf_name: str
    folder_name: str
    semantic_text: str
    parent_text: str

    @classmethod
    def from_referenced_chunk(cls, chunk: ReferencedChunk) -> "ReferencedChunkResponse":
        """Create a ReferencedChunkResponse from a ReferencedChunk model.
        
        Args:
            chunk: The ReferencedChunk instance to convert.
            
        Returns:
            A new ReferencedChunkResponse instance.
        """
        return cls(
            semantic_id=chunk.semantic_id,
            parent_id=chunk.parent_id,
            similarity_score=chunk.similarity_score,
            pdf_name=chunk.pdf_name,
            folder_name=chunk.folder_name,
            semantic_text=chunk.semantic_text,
            parent_text=chunk.parent_text
        )


class QueryResponse(BaseModel):
    """Response model for query endpoint.
    
    Attributes:
        answer: The generated answer text from the LLM.
        referenced_chunks: List of chunks that were used to generate the answer.
        query: The original user query.
    """
    answer: str
    referenced_chunks: List[ReferencedChunkResponse]
    query: str

    @classmethod
    def from_rag_response(cls, rag_response: RAGResponse) -> "QueryResponse":
        """Create a QueryResponse from a RAGResponse model.
        
        Args:
            rag_response: The RAGResponse instance to convert.
            
        Returns:
            A new QueryResponse instance.
        """
        return cls(
            answer=rag_response.answer,
            referenced_chunks=[
                ReferencedChunkResponse.from_referenced_chunk(chunk)
                for chunk in rag_response.referenced_chunks
            ],
            query=rag_response.query
        )




class HealthResponse(BaseModel):
    """Response model for health check endpoint.
    
    Attributes:
        status: Service status (typically "healthy").
        qdrant_connected: Whether Qdrant database is connected.
        ollama_configured: Whether Ollama is configured.
    """
    status: str
    qdrant_connected: bool
    ollama_configured: bool


# Global RAG system instance
_rag_system: Optional[SVRAG] = None


def get_rag_system() -> SVRAG:
    """Get or initialize the RAG system instance.
    
    This function implements a singleton pattern for the RAG system,
    initializing it on first access using environment variables or defaults.
    
    Returns:
        The initialized SVRAG instance.
        
    Raises:
        RuntimeError: If the RAG system cannot be initialized.
    """
    global _rag_system
    
    if _rag_system is None:
        try:
            # Get configuration from environment variables with defaults
            collection_name = os.getenv(
                "QDRANT_COLLECTION_NAME",
                "supportvectors_ai_knowledge_base"
            )
            qdrant_host = os.getenv("QDRANT_HOST", "localhost")
            qdrant_port = int(os.getenv("QDRANT_PORT", "6333"))
            embedding_model = os.getenv(
                "EMBEDDING_MODEL",
                "jinaai/jina-embeddings-v2-base-en"
            )
            ollama_model = os.getenv("OLLAMA_MODEL", "gpt-oss:20b")
            ollama_host = os.getenv("OLLAMA_HOST", "localhost")
            ollama_port = int(os.getenv("OLLAMA_PORT", "11434"))
            similarity_threshold = float(
                os.getenv("SIMILARITY_THRESHOLD", "0.7")
            )
            top_k = int(os.getenv("TOP_K", "5"))
            system_prompt_path = os.getenv("SYSTEM_PROMPT_PATH", None)
            is_local = os.getenv("IS_LOCAL", "False").lower() == "true"
            # Initialize components
            embedder = LateChunkEmbedder(model_name=embedding_model, is_local=is_local)
            storage = QdrantStorage(
                collection_name=collection_name,
                host=qdrant_host,
                port=qdrant_port
            )
            
            _rag_system = SVRAG(
                embedder=embedder,
                storage=storage,
                ollama_model=ollama_model,
                ollama_host=ollama_host,
                ollama_port=ollama_port,
                similarity_threshold=similarity_threshold,
                top_k=top_k,
                system_prompt_path=system_prompt_path
            )
        except Exception as e:
            raise RuntimeError(
                f"Failed to initialize RAG system: {e}"
            ) from e
    
    return _rag_system


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan events.
    
    This context manager handles startup and shutdown events for the FastAPI
    application, ensuring the RAG system is properly initialized and cleaned up.
    
    Args:
        app: The FastAPI application instance.
        
    Yields:
        None: Control is yielded back to the application runtime.
    """
    # Startup: Initialize RAG system
    try:
        get_rag_system()
        print("RAG system initialized successfully")
    except Exception as e:
        print(f"Warning: Failed to initialize RAG system at startup: {e}")
    
    yield
    
    # Shutdown: Cleanup if needed
    global _rag_system
    _rag_system = None


# Initialize FastAPI app
app = FastAPI(
    title="SupportVectors RAG API",
    description="REST API for querying the SupportVectors knowledge base using RAG",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health", response_model=HealthResponse)
def health_check(rag: SVRAG = Depends(get_rag_system)) -> HealthResponse:
    """Check the health status of the service.
    
    This endpoint verifies that the service is running and can connect to
    required dependencies (Qdrant and Ollama).
    
    Args:
        rag: The RAG system instance (injected via dependency).
        
    Returns:
        HealthResponse containing the service status and dependency connectivity.
    """
    try:
        # Try to access storage to verify Qdrant connection
        qdrant_connected = rag.storage is not None
        ollama_configured = rag.ollama_model is not None
        
        return HealthResponse(
            status="healthy",
            qdrant_connected=qdrant_connected,
            ollama_configured=ollama_configured
        )
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service unhealthy: {e}"
        )


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, rag: SVRAG = Depends(get_rag_system)) -> QueryResponse:
    """Generate a response to a user query using RAG.
    
    This endpoint processes a natural language query by:
    1. Embedding the query using the configured embedding model
    2. Performing semantic search in the Qdrant vector database
    3. Retrieving top-k relevant chunks above the similarity threshold
    4. Generating a response using the Ollama LLM with retrieved context
    
    Args:
        request: QueryRequest containing the user query and optional parameters.
        rag: The RAG system instance (injected via dependency).
        
    Returns:
        QueryResponse containing the generated answer and referenced chunk metadata.
        
    Raises:
        HTTPException: If the query cannot be processed or no relevant chunks are found.
    """
    try:
        # Temporarily override similarity_threshold and top_k if provided
        original_threshold = rag.similarity_threshold
        original_top_k = rag.top_k
        
        if request.similarity_threshold is not None:
            rag.similarity_threshold = request.similarity_threshold
        if request.top_k is not None:
            rag.top_k = request.top_k
        
        try:
            # Process the query
            rag_response = rag.query(request.query)
            response = QueryResponse.from_rag_response(rag_response)
        finally:
            # Restore original values
            rag.similarity_threshold = original_threshold
            rag.top_k = original_top_k
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=503,
            detail=f"Service error: {e}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {e}"
        )


@app.post("/search", response_model=List[ReferencedChunkResponse])
def search(
    request: QueryRequest,
    rag: SVRAG = Depends(get_rag_system)
) -> List[ReferencedChunkResponse]:
    """Search for relevant chunks without generating a response.
    
    This endpoint performs semantic search on the knowledge base and returns
    the retrieved chunks with their similarity scores. Useful for debugging
    or when you only need the retrieved context without LLM generation.
    
    Args:
        request: QueryRequest containing the user query and optional parameters.
        rag: The RAG system instance (injected via dependency).
        
    Returns:
        List of ReferencedChunkResponse objects containing retrieved chunks and scores.
        
    Raises:
        HTTPException: If the search cannot be performed.
    """
    try:
        # Temporarily override similarity_threshold and top_k if provided
        original_threshold = rag.similarity_threshold
        original_top_k = rag.top_k
        
        if request.similarity_threshold is not None:
            rag.similarity_threshold = request.similarity_threshold
        if request.top_k is not None:
            rag.top_k = request.top_k
        
        try:
            # Perform search only
            results = rag.search_only(request.query)
            
            # Convert results to ReferencedChunkResponse format
            search_results = []
            for result in results:
                payload = result['payload']
                search_results.append(ReferencedChunkResponse(
                    similarity_score=result['score'],
                    semantic_id=payload.get('semantic_id', 0),
                    parent_id=payload.get('parent_id', 0),
                    pdf_name=payload.get('pdf_name', 'Unknown'),
                    folder_name=payload.get('folder_name', 'Unknown'),
                    semantic_text=payload.get('text', ''),
                    parent_text=payload.get('parent_text', '')
                ))
        finally:
            # Restore original values
            rag.similarity_threshold = original_threshold
            rag.top_k = original_top_k
        
        return search_results
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {e}"
        )


@app.get("/")
def root() -> Dict[str, str]:
    """Root endpoint providing API information.
    
    Returns:
        Dictionary containing API name and version information.
    """
    return {
        "name": "SupportVectors RAG API",
        "version": "1.0.0",
        "description": "REST API for querying the SupportVectors knowledge base using RAG"
    }


def main():
    """Main function to start the FastAPI service.
    
    This function initializes and runs the FastAPI application using uvicorn.
    Host and port can be configured via command-line arguments or environment
    variables (API_HOST and API_PORT). Command-line arguments take precedence.
    
    Environment Variables:
        API_HOST: Host address to bind the server (default: "0.0.0.0")
        API_PORT: Port number to bind the server (default: 8000)
        
    Command-line Arguments:
        --host: Host address to bind the server (overrides API_HOST)
        --port: Port number to bind the server (overrides API_PORT)
        --reload: Enable auto-reload for development (default: False)
    """
    import argparse
    import uvicorn
    
    parser = argparse.ArgumentParser(
        description="Start the SupportVectors RAG API service"
    )
    parser.add_argument(
        "--host",
        type=str,
        default=os.getenv("API_HOST", "0.0.0.0"),
        help="Host address to bind the server (default: 0.0.0.0 or API_HOST env var)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("API_PORT", "8000")),
        help="Port number to bind the server (default: 8000 or API_PORT env var)"
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload for development (default: False)"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Starting SupportVectors RAG API Service")
    print("=" * 80)
    print(f"Host: {args.host}")
    print(f"Port: {args.port}")
    print(f"Reload: {args.reload}")
    print("=" * 80)
    print()
    
    uvicorn.run(
        "svrag.service.response_generation_service:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )


if __name__ == "__main__":
    main()
