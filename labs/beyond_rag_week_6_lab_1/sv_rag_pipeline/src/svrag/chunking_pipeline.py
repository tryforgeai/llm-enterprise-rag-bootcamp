#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""
Chunking Pipeline for RAG (Retrieval-Augmented Generation) System.

This module implements a multi-stage chunking pipeline that:
1. Uses Docling to create parent chunks from PDF documents
2. Uses Chonkie to create semantic chunks from parent chunks
3. Uses Jina AI's late chunking approach to create embeddings
4. Stores embeddings and metadata in Qdrant vector database

The pipeline processes PDF documents across multiple folders and creates
a searchable knowledge base with semantic chunk embeddings.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from svrag.models import EnrichedChunk
from svrag.document_converter import DocumentConverterWrapper
from svrag.semantic_chunker import SemanticChunkerWrapper
from svrag.late_chunk_embedder import LateChunkEmbedder
from svrag.qdrant_storage import QdrantStorage


class ChunkingPipeline:
    """Main pipeline class that orchestrates the entire chunking process.
    
    This class coordinates all stages of the chunking pipeline:
    1. Document conversion and parent chunking
    2. Semantic chunking
    3. Late chunk embedding generation
    4. Storage in Qdrant vector database
    
    Attributes:
        doc_converter: DocumentConverterWrapper instance
        semantic_chunker: SemanticChunkerWrapper instance
        embedder: LateChunkEmbedder instance
        storage: QdrantStorage instance
        data_dir: Directory containing PDF documents
    """
    
    def __init__(
        self,
        data_dir: str = "data",
        collection_name: str = "supportvectors_ai_knowledge_base",
        qdrant_host: str = "localhost",
        qdrant_port: int = 6333,
        embedding_model: str = "jinaai/jina-embeddings-v2-base-en"
    ):
        """Initialize the chunking pipeline.
        
        Args:
            data_dir: Path to directory containing PDF subfolders
            collection_name: Name of the Qdrant collection
            qdrant_host: Qdrant server host address
            qdrant_port: Qdrant server port
            embedding_model: Name of the Jina embedding model to use
        """
        self.data_dir = Path(data_dir)
        self.doc_converter = DocumentConverterWrapper()
        self.semantic_chunker = SemanticChunkerWrapper()
        self.embedder = LateChunkEmbedder(model_name=embedding_model)
        self.storage = QdrantStorage(
            collection_name=collection_name,
            host=qdrant_host,
            port=qdrant_port
        )
    
    def process_pdf(
        self, 
        pdf_path: str, 
        folder_name: str,
        pdf_name: str
    ) -> List[EnrichedChunk]:
        """Process a single PDF file through the entire pipeline.
        
        Args:
            pdf_path: Path to the PDF file
            folder_name: Name of the folder containing the PDF
            pdf_name: Name of the PDF file
            
        Returns:
            List of EnrichedChunk objects with embeddings
        """
        # Step 1: Convert PDF and create parent chunks
        parent_chunks_raw = self.doc_converter.convert_and_chunk(pdf_path)
        
        # Step 2: Create semantic chunks for each parent chunk
        parent_chunk_dict_list = []
        parent_chunk_id = 0
        
        for parent_chunk in parent_chunks_raw:
            parent_chunk_dict = {
                "id": parent_chunk_id,
                "text": parent_chunk.text,
                "semantic_chunks": []
            }
            
            # Create semantic chunks
            semantic_chunks = self.semantic_chunker.chunk(parent_chunk.text)
            semantic_chunk_id = 0
            
            for sem_chunk in semantic_chunks:
                semantic_chunk_dict = {
                    "id": semantic_chunk_id,
                    "text": sem_chunk.text,
                    "start_char": sem_chunk.start_index,
                    "end_char": sem_chunk.end_index
                }
                parent_chunk_dict["semantic_chunks"].append(semantic_chunk_dict)
                semantic_chunk_id += 1
            
            parent_chunk_dict_list.append(parent_chunk_dict)
            parent_chunk_id += 1
        
        # Step 3: Create late chunk embeddings
        all_enriched_chunks = []
        for parent_chunk_dict in parent_chunk_dict_list:
            enriched_semantics = self.embedder.embed_parent_chunk(parent_chunk_dict)
            
            # Convert to EnrichedChunk objects with metadata
            for es in enriched_semantics:
                enriched_chunk = EnrichedChunk(
                    semantic_id=es["semantic_id"],
                    parent_id=es["parent_id"],
                    parent_text=es["parent_text"],
                    text=es["text"],
                    num_tokens=es["num_tokens"],
                    embedding=es["embedding"],
                    pdf_name=pdf_name,
                    folder_name=folder_name
                )
                all_enriched_chunks.append(enriched_chunk)
        
        return all_enriched_chunks
    
    def process_all_documents(
        self, 
        output_file: Optional[str] = None,
        vector_size: int = 768
    ) -> int:
        """Process all PDF documents in the data directory.
        
        This method processes all PDF files across all subfolders in the
        data directory and stores them in Qdrant.
        
        Args:
            output_file: Optional path to JSONL file to save chunks
            vector_size: Size of embedding vectors for collection creation
            
        Returns:
            Total number of chunks processed
        """
        # Create Qdrant collection
        self.storage.create_collection(vector_size=vector_size)
        
        # Process all PDFs
        all_chunks = []
        point_id = 0
        
        # Iterate through all subfolders
        for folder_path in self.data_dir.iterdir():
            if not folder_path.is_dir():
                continue
            
            folder_name = folder_path.name
            
            # Process all PDFs in the folder
            for pdf_file in folder_path.glob("*.pdf"):
                pdf_name = pdf_file.name
                pdf_path = str(pdf_file)
                
                print(f"Processing: {folder_name}/{pdf_name}")
                
                try:
                    enriched_chunks = self.process_pdf(
                        pdf_path=pdf_path,
                        folder_name=folder_name,
                        pdf_name=pdf_name
                    )
                    
                    # Store in Qdrant
                    point_id = self.storage.insert_chunks(
                        enriched_chunks=enriched_chunks,
                        start_id=point_id
                    )
                    
                    all_chunks.extend(enriched_chunks)
                    
                except Exception as e:
                    print(f"Error processing {pdf_name}: {e}")
                    continue
        
        # Optionally save to JSONL file
        if output_file:
            os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
            with open(output_file, "w") as f:
                for chunk in all_chunks:
                    json.dump({
                        "semantic_id": chunk.semantic_id,
                        "parent_id": chunk.parent_id,
                        "parent_text": chunk.parent_text,
                        "text": chunk.text,
                        "num_tokens": chunk.num_tokens,
                        "embedding": chunk.embedding,
                        "pdf_name": chunk.pdf_name,
                        "folder_name": chunk.folder_name,
                    }, f)
                    f.write("\n")
        
        return len(all_chunks)
    
    def search(
        self, 
        query: str, 
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Search the knowledge base with a query string.
        
        Args:
            query: Search query string
            limit: Maximum number of results to return
            
        Returns:
            List of search results with scores and payloads
        """
        query_vector = self.embedder.encode_query(query)
        return self.storage.search(query_vector=query_vector, limit=limit)
