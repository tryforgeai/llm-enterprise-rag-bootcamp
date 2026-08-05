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
Main script to run the RAG response generation system.

This script allows querying the knowledge base using natural language questions
and generates responses using the SVRAG system with Ollama LLM.
"""

import argparse
import sys

from svrag import SVRAG, LateChunkEmbedder, QdrantStorage


def print_response(response, verbose: bool = False):
    """Print the RAG response in a formatted way.
    
    Args:
        response: RAGResponse object
        verbose: If True, print detailed metadata about referenced chunks
    """
    print("=" * 80)
    print("RAG RESPONSE")
    print("=" * 80)
    print(f"\nQuery: {response.query}\n")
    print("-" * 80)
    print("Answer:")
    print("-" * 80)
    print(response.answer)
    print()
    
    if verbose:
        print("=" * 80)
        print(f"REFERENCED CHUNKS ({len(response.referenced_chunks)} chunks)")
        print("=" * 80)
        for i, chunk in enumerate(response.referenced_chunks, 1):
            print(f"\nChunk {i}:")
            print(f"  Source: {chunk.folder_name}/{chunk.pdf_name}")
            print(f"  Similarity Score: {chunk.similarity_score:.4f}")
            print(f"  Semantic ID: {chunk.semantic_id}, Parent ID: {chunk.parent_id}")
            print(f"  Semantic Text Preview: {chunk.semantic_text[:200]}...")
            if chunk.parent_text != chunk.semantic_text:
                print(f"  Parent Text Preview: {chunk.parent_text[:200]}...")
            print()
    else:
        print("=" * 80)
        print(f"Referenced {len(response.referenced_chunks)} chunk(s)")
        print("=" * 80)
        for i, chunk in enumerate(response.referenced_chunks, 1):
            print(f"  {i}. {chunk.folder_name}/{chunk.pdf_name} (score: {chunk.similarity_score:.4f})")
    print()


def main():
    """Main function to run the RAG response generation."""
    parser = argparse.ArgumentParser(
        description="Query the knowledge base using RAG and generate responses"
    )
    parser.add_argument(
        "--query",
        type=str,
        help="Single query to process (if not provided, runs in interactive mode)"
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
        "--ollama-model",
        type=str,
        default="gpt-oss:20b",
        help="Ollama model name (default: gpt-oss:20b)"
    )
    parser.add_argument(
        "--ollama-host",
        type=str,
        default="localhost",
        help="Ollama server host (default: localhost)"
    )
    parser.add_argument(
        "--ollama-port",
        type=int,
        default=11434,
        help="Ollama server port (default: 11434)"
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.7,
        help="Minimum similarity score for retrieved chunks (default: 0.7)"
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Maximum number of chunks to retrieve (default: 5)"
    )
    parser.add_argument(
        "--system-prompt-path",
        type=str,
        default=None,
        help="Path to system prompt file (default: prompts/system_prompt.md)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Print verbose output including full chunk metadata"
    )
    parser.add_argument(
        "--search-only",
        action="store_true",
        help="Only perform search without generating LLM response"
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("RAG Response Generation System")
    print("=" * 80)
    print(f"Qdrant: {args.qdrant_host}:{args.qdrant_port}")
    print(f"Collection: {args.collection_name}")
    print(f"Embedding model: {args.embedding_model}")
    print(f"Ollama: {args.ollama_host}:{args.ollama_port}")
    print(f"Ollama model: {args.ollama_model}")
    print(f"Similarity threshold: {args.similarity_threshold}")
    print(f"Top-K: {args.top_k}")
    print("=" * 80)
    print()
    
    # Initialize components
    try:
        print("Initializing RAG system...")
        embedder = LateChunkEmbedder(model_name=args.embedding_model)
        storage = QdrantStorage(
            collection_name=args.collection_name,
            host=args.qdrant_host,
            port=args.qdrant_port
        )
        
        rag = SVRAG(
            embedder=embedder,
            storage=storage,
            ollama_model=args.ollama_model,
            ollama_host=args.ollama_host,
            ollama_port=args.ollama_port,
            similarity_threshold=args.similarity_threshold,
            top_k=args.top_k,
            system_prompt_path=args.system_prompt_path
        )
        print("RAG system initialized successfully.")
        print()
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Process queries
    if args.query:
        # Single query mode
        try:
            if args.search_only:
                print(f"Searching for: '{args.query}'")
                print()
                results = rag.search_only(args.query)
                print(f"Found {len(results)} results:\n")
                for i, result in enumerate(results, 1):
                    payload = result['payload']
                    print(f"Result {i} (score: {result['score']:.4f}):")
                    print(f"  PDF: {payload.get('pdf_name', 'Unknown')}")
                    print(f"  Folder: {payload.get('folder_name', 'Unknown')}")
                    print(f"  Text preview: {payload.get('text', '')[:200]}...")
                    print()
            else:
                print(f"Processing query: '{args.query}'")
                print()
                response = rag.query(args.query)
                print_response(response, verbose=args.verbose)
        except KeyboardInterrupt:
            print("\n\nQuery interrupted by user.")
            sys.exit(1)
        except Exception as e:
            print(f"\nError processing query: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        # Interactive mode
        print("Interactive mode - Enter queries (type 'quit' or 'exit' to stop)")
        print()
        try:
            while True:
                try:
                    query = input("Query: ").strip()
                    if not query:
                        continue
                    if query.lower() in ['quit', 'exit', 'q']:
                        print("\nExiting...")
                        break
                    
                    print()
                    if args.search_only:
                        results = rag.search_only(query)
                        print(f"Found {len(results)} results:\n")
                        for i, result in enumerate(results, 1):
                            payload = result['payload']
                            print(f"Result {i} (score: {result['score']:.4f}):")
                            print(f"  PDF: {payload.get('pdf_name', 'Unknown')}")
                            print(f"  Folder: {payload.get('folder_name', 'Unknown')}")
                            print(f"  Text preview: {payload.get('text', '')[:200]}...")
                            print()
                    else:
                        response = rag.query(query)
                        print_response(response, verbose=args.verbose)
                except KeyboardInterrupt:
                    print("\n\nInterrupted. Exiting...")
                    break
                except Exception as e:
                    print(f"\nError: {e}")
                    import traceback
                    traceback.print_exc()
                    print()
        except EOFError:
            print("\n\nExiting...")
    
    print("RAG system execution completed!")


if __name__ == "__main__":
    main()

