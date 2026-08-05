#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""Data models for the chunking pipeline."""

from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class ParentChunk:
    """Data class representing a parent chunk from Docling.
    
    Attributes:
        id: Unique identifier for the parent chunk
        text: The text content of the parent chunk
        semantic_chunks: List of semantic chunks derived from this parent chunk
    """
    id: int
    text: str
    semantic_chunks: List[Dict[str, Any]]


@dataclass
class SemanticChunk:
    """Data class representing a semantic chunk from Chonkie.
    
    Attributes:
        id: Unique identifier for the semantic chunk within its parent
        text: The text content of the semantic chunk
        start_char: Starting character index in the parent chunk
        end_char: Ending character index in the parent chunk
    """
    id: int
    text: str
    start_char: int
    end_char: int


@dataclass
class EnrichedChunk:
    """Data class representing an enriched chunk with embedding.
    
    Attributes:
        semantic_id: Unique identifier for the semantic chunk
        parent_id: Identifier of the parent chunk
        parent_text: Full text of the parent chunk
        text: Text content of the semantic chunk
        num_tokens: Number of tokens in the semantic chunk
        embedding: Vector embedding for the semantic chunk
        pdf_name: Name of the source PDF file
        folder_name: Name of the folder containing the PDF
    """
    semantic_id: int
    parent_id: int
    parent_text: str
    text: str
    num_tokens: int
    embedding: List[float]
    pdf_name: str
    folder_name: str


@dataclass
class ReferencedChunk:
    """Data class representing a chunk referenced in a RAG response.
    
    Attributes:
        semantic_id: Unique identifier for the semantic chunk
        parent_id: Identifier of the parent chunk
        similarity_score: Similarity score from vector search
        pdf_name: Name of the source PDF file
        folder_name: Name of the folder containing the PDF
        semantic_text: Text content of the semantic chunk
        parent_text: Full text of the parent chunk
    """
    semantic_id: int
    parent_id: int
    similarity_score: float
    pdf_name: str
    folder_name: str
    semantic_text: str
    parent_text: str


@dataclass
class RAGResponse:
    """Data class representing a structured RAG response.
    
    Attributes:
        answer: The generated answer text from the LLM
        referenced_chunks: List of chunks that were used to generate the answer
        query: The original user query
    """
    answer: str
    referenced_chunks: List[ReferencedChunk]
    query: str

