#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
from svlearn.config.configuration import ConfigurationMixin

from dotenv import load_dotenv

# Export main chunking pipeline classes
from svrag.chunking_pipeline import ChunkingPipeline
from svrag.document_converter import DocumentConverterWrapper
from svrag.semantic_chunker import SemanticChunkerWrapper
from svrag.late_chunk_embedder import LateChunkEmbedder
from svrag.qdrant_storage import QdrantStorage
from svrag.models import ParentChunk, SemanticChunk, EnrichedChunk, RAGResponse, ReferencedChunk
from svrag.response_generation.sv_rag import SVRAG

load_dotenv()

config = ConfigurationMixin().load_config()


__all__ = [
    "ChunkingPipeline",
    "DocumentConverterWrapper",
    "SemanticChunkerWrapper",
    "LateChunkEmbedder",
    "QdrantStorage",
    "ParentChunk",
    "SemanticChunk",
    "EnrichedChunk",
    "RAGResponse",
    "ReferencedChunk",
    "SVRAG",
]
