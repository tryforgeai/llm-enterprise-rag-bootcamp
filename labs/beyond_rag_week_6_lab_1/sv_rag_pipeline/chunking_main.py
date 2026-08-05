#!/usr/bin/env python3
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
Main script to run the chunking pipeline and save embeddings to Qdrant.

This script processes all PDF documents in the data directory, creates
embeddings using late chunking, and stores them in Qdrant vector database.
"""

import argparse
import sys
from pathlib import Path

from svrag import ChunkingPipeline


def main():
    """Main function to run the chunking pipeline."""
    parser = argparse.ArgumentParser(
        description="Run the chunking pipeline to process PDFs and store embeddings in Qdrant"
    )
    parser.add_argument(
        "--data-dir",
        type=str,
        default="data",
        help="Directory containing PDF subfolders (default: data)"
    )
    parser.add_argument(
        "--collection-name",
        type=str,
        default="supportvectors_ai_knowledge_base",
        help="Name of the Qdrant collection (default: supportvectors_ai_knowledge_base)"
    )
    parser.add_argument(
        "--qdrant-host",
        type=str,
        default="localhost",
        help="Qdrant server host (default: localhost)"
    )
    parser.add_argument(
        "--qdrant-port",
        type=int,
        default=6333,
        help="Qdrant server port (default: 6333)"
    )
    parser.add_argument(
        "--embedding-model",
        type=str,
        default="jinaai/jina-embeddings-v2-base-en",
        help="Jina embedding model name (default: jinaai/jina-embeddings-v2-base-en)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="output/late_chunks.jsonl",
        help="Optional path to JSONL file to save chunks (default: output/late_chunks.jsonl)"
    )
    parser.add_argument(
        "--vector-size",
        type=int,
        default=768,
        help="Size of embedding vectors (default: 768)"
    )
    parser.add_argument(
        "--no-jsonl",
        action="store_true",
        help="Skip saving to JSONL file"
    )
    parser.add_argument(
        "--test-query",
        type=str,
        help="Optional test query to search the knowledge base after processing"
    )
    
    args = parser.parse_args()
    
    # Validate data directory exists
    data_dir = Path(args.data_dir)
    if not data_dir.exists():
        print(f"Error: Data directory '{data_dir}' does not exist.")
        sys.exit(1)
    
    if not data_dir.is_dir():
        print(f"Error: '{data_dir}' is not a directory.")
        sys.exit(1)
    
    print("=" * 80)
    print("Chunking Pipeline - Processing PDFs and Storing Embeddings in Qdrant")
    print("=" * 80)
    print(f"Data directory: {data_dir}")
    print(f"Qdrant host: {args.qdrant_host}:{args.qdrant_port}")
    print(f"Collection name: {args.collection_name}")
    print(f"Embedding model: {args.embedding_model}")
    print(f"Vector size: {args.vector_size}")
    if not args.no_jsonl:
        print(f"Output file: {args.output_file}")
    print("=" * 80)
    print()
    
    # Initialize pipeline
    try:
        print("Initializing chunking pipeline...")
        pipeline = ChunkingPipeline(
            data_dir=str(data_dir),
            collection_name=args.collection_name,
            qdrant_host=args.qdrant_host,
            qdrant_port=args.qdrant_port,
            embedding_model=args.embedding_model
        )
        print("Pipeline initialized successfully.")
        print()
    except Exception as e:
        print(f"Error initializing pipeline: {e}")
        sys.exit(1)
    
    # Process all documents
    try:
        print("Starting document processing...")
        output_file = None if args.no_jsonl else args.output_file
        num_chunks = pipeline.process_all_documents(
            output_file=output_file,
            vector_size=args.vector_size
        )
        print()
        print("=" * 80)
        print(f"Processing complete! Processed {num_chunks} chunks.")
        print("=" * 80)
        print()
    except KeyboardInterrupt:
        print("\n\nProcessing interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during processing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Test query if provided
    if args.test_query:
        print("=" * 80)
        print(f"Testing search query: '{args.test_query}'")
        print("=" * 80)
        try:
            results = pipeline.search(query=args.test_query, limit=5)
            print(f"\nFound {len(results)} results:\n")
            for i, result in enumerate(results, 1):
                print(f"Result {i} (score: {result['score']:.4f}):")
                print(f"  PDF: {result['payload']['pdf_name']}")
                print(f"  Folder: {result['payload']['folder_name']}")
                print(f"  Text preview: {result['payload']['text'][:200]}...")
                print()
        except Exception as e:
            print(f"Error during search: {e}")
            import traceback
            traceback.print_exc()
    
    print("Pipeline execution completed successfully!")


if __name__ == "__main__":
    main()

