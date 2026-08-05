#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""SupportVectors RAG (Retrieval-Augmented Generation) system for query processing."""

from pathlib import Path
from typing import List, Dict, Any, Optional
import os

from openai import OpenAI
from dotenv import load_dotenv

from svrag.models import RAGResponse, ReferencedChunk
from svrag.late_chunk_embedder import LateChunkEmbedder
load_dotenv()


class SVRAG:
    """SupportVectors RAG system for generating responses using vector search and LLM.
    
    This class implements a RAG pipeline that:
    1. Embeds user queries using Jina AI embedding model
    2. Performs nearest neighbor search on Qdrant vector database
    3. Retrieves top-k relevant chunks with similarity threshold filtering
    4. Generates responses using Ollama LLM with context from retrieved chunks
    
    Attributes:
        embedder: LateChunkEmbedder instance for query embedding
        storage: QdrantStorage instance for vector search
        system_prompt: System prompt template loaded from file
        ollama_model: Name of the Ollama model to use
        ollama_host: Host address for Ollama server
        ollama_port: Port for Ollama server
        similarity_threshold: Minimum similarity score for retrieved chunks
        top_k: Maximum number of chunks to retrieve
    """
    
    def __init__(
        self,
        embedder,
        storage,
        ollama_model: str = "gpt-oss:20b",
        ollama_host: str = "localhost",
        ollama_port: int = 11434,
        similarity_threshold: float = 0.7,
        top_k: int = 5,
        system_prompt_path: Optional[str] = None
    ):
        """Initialize the SVRAG system.
        
        Args:
            embedder: LateChunkEmbedder instance for creating query embeddings
            storage: QdrantStorage instance for vector search
            ollama_model: Name of the Ollama model to use (default: "gpt-oss:20b")
            ollama_host: Host address for Ollama server (default: "localhost")
            ollama_port: Port for Ollama server (default: 11434)
            similarity_threshold: Minimum similarity score for chunks (default: 0.7)
            top_k: Maximum number of chunks to retrieve (default: 5)
            system_prompt_path: Optional path to system prompt file. If None, uses
                prompts/system_prompt.md relative to project root
        """
        self.embedder: LateChunkEmbedder = embedder
        self.storage = storage
        self.ollama_model = ollama_model
        self.ollama_host = ollama_host
        self.ollama_port = ollama_port
        self.similarity_threshold = similarity_threshold
        self.top_k = top_k
        
        # Initialize OpenAI client to access Ollama via OpenAI-compatible API
        base_url = f"http://{ollama_host}:{ollama_port}/v1"
        self.llm_client = OpenAI(
            base_url=base_url,
            api_key="ollama"  # Ollama doesn't require auth, but OpenAI client needs a value
        )
        
        # Load system prompt
        if system_prompt_path is None:
            # Default to prompts/system_prompt.md relative to project root
            project_root_str = os.getenv("BOOTCAMP_ROOT_DIR")
            if project_root_str:
                project_root = Path(project_root_str)
            else:
                # Fallback to relative path if env var not set
                project_root = Path(__file__).parent.parent.parent.parent
            system_prompt_path = project_root / "prompts" / "system_prompt.md"
        
        self.system_prompt = self._load_system_prompt(system_prompt_path)
    
    def _load_system_prompt(self, prompt_path: Path) -> str:
        """Load system prompt from markdown file.
        
        Args:
            prompt_path: Path to the system prompt markdown file
            
        Returns:
            System prompt content as string
            
        Raises:
            FileNotFoundError: If the prompt file doesn't exist
        """
        prompt_file = Path(prompt_path)
        if not prompt_file.exists():
            raise FileNotFoundError(
                f"System prompt file not found: {prompt_file}. "
                f"Please create the file at {prompt_file.absolute()}"
            )
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def _format_retrieved_context(self, query: str, results: List[Dict[str, Any]]) -> str:
        """Format retrieved search results into context string for the prompt.
        
        Args:
            query: The user's query string
            results: List of search results with score and payload
            
        Returns:
            Formatted context string
        """
        context_parts = [
            f"Answer the user query {query} based on the following nearest text chunks found (itemized in decreasing order of semantic scores):"
        ]
        
        for result in results:
            payload = result['payload']
            score = result['score']
            semantic_chunk_text = payload.get('text', '')
            parent_chunk_text = payload.get('parent_text', '')
            
            context_parts.append(
                f"- {semantic_chunk_text} in the parent text chunk {parent_chunk_text} with a similarity score {score:.4f}"
            )
        
        return "\n".join(context_parts)
    
    def _build_prompt(self, user_query: str, retrieved_context: str) -> str:
        """Build the complete prompt by inserting query and context into system prompt.
        
        Args:
            user_query: The user's query string
            retrieved_context: Formatted context from retrieved chunks
            
        Returns:
            Complete prompt string
        """
        prompt = self.system_prompt.format(
            user_query=user_query,
            retrieved_context=retrieved_context
        )
        return prompt
    
    def _filter_results_by_threshold(
        self, 
        results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Filter search results by similarity threshold and limit to top_k.
        
        Args:
            results: List of search results with scores
            
        Returns:
            Filtered and limited list of results
        """
        # Filter by threshold
        filtered = [
            result for result in results 
            if result['score'] >= self.similarity_threshold
        ]
        
        # Limit to top_k
        return filtered[:self.top_k]
    
    def _create_referenced_chunks(
        self, 
        filtered_results: List[Dict[str, Any]]
    ) -> List[ReferencedChunk]:
        """Create ReferencedChunk objects from filtered search results.
        
        Args:
            filtered_results: List of filtered search results with scores and payloads
            
        Returns:
            List of ReferencedChunk objects
        """
        referenced_chunks = []
        for result in filtered_results:
            payload = result['payload']
            chunk = ReferencedChunk(
                semantic_id=payload.get('semantic_id', 0),
                parent_id=payload.get('parent_id', 0),
                similarity_score=result['score'],
                pdf_name=payload.get('pdf_name', 'Unknown'),
                folder_name=payload.get('folder_name', 'Unknown'),
                semantic_text=payload.get('text', ''),
                parent_text=payload.get('parent_text', '')
            )
            referenced_chunks.append(chunk)
        return referenced_chunks
    
    def query(self, user_query: str) -> RAGResponse:
        """Process a user query and generate a structured response using RAG.
        
        This method:
        1. Embeds the user query
        2. Searches for similar chunks in Qdrant
        3. Filters results by similarity threshold
        4. Formats context from retrieved chunks
        5. Generates response using Ollama LLM
        6. Returns structured response with answer and referenced chunk metadata
        
        Args:
            user_query: The user's query string
            
        Returns:
            RAGResponse object containing the answer and referenced chunk metadata
            
        Raises:
            ValueError: If no relevant chunks are found above the threshold
            RuntimeError: If Ollama API call fails
        """
        # Step 1: Embed the query
        query_embedding = self.embedder.encode_query(user_query)
        
        # Step 2: Search for similar chunks
        # Search for more than top_k to account for threshold filtering
        search_limit = max(self.top_k * 2, 10)
        search_results = self.storage.search(
            query_vector=query_embedding,
            limit=search_limit
        )
        # Step 3: Filter by threshold and limit to top_k
        filtered_results = self._filter_results_by_threshold(search_results)
        
        if not filtered_results:
            print(f"No relevant chunks found with similarity >= {self.similarity_threshold}. ")
            raise ValueError(
                f"No relevant chunks found with similarity >= {self.similarity_threshold}. "
                f"Try lowering the threshold or expanding the knowledge base."
            )
        
        # Step 4: Create referenced chunks metadata
        referenced_chunks = self._create_referenced_chunks(filtered_results)
        
        # Step 5: Format retrieved context
        retrieved_context = self._format_retrieved_context(user_query, filtered_results)
        
        # Step 6: Build prompt
        prompt = self._build_prompt(user_query, retrieved_context)
        
        # Step 7: Generate response using Ollama via OpenAI-compatible API
        try:
            response = self.llm_client.chat.completions.create(
                model=self.ollama_model,
                messages=[
                    {
                        'role': 'system',
                        'content': prompt
                    },
                    {
                        'role': 'user',
                        'content': user_query
                    }
                ]
            )
            
            answer = response.choices[0].message.content
            
            # Step 8: Return structured response with metadata
            return RAGResponse(
                answer=answer,
                referenced_chunks=referenced_chunks,
                query=user_query
            )
            
        except Exception as e:
            raise RuntimeError(
                f"Failed to generate response from Ollama: {e}. "
                f"Make sure Ollama is running at {self.ollama_host}:{self.ollama_port} "
                f"and the model '{self.ollama_model}' is available."
            ) from e
    
    def search_only(self, user_query: str) -> List[Dict[str, Any]]:
        """Search for relevant chunks without generating a response.
        
        This method is useful for debugging or when you only need the retrieved context.
        
        Args:
            user_query: The user's query string
            
        Returns:
            List of filtered search results with scores and payloads
        """
        # Embed the query
        query_embedding = self.embedder.encode_query(user_query)
        
        # Search for similar chunks
        search_limit = max(self.top_k * 2, 10)
        search_results = self.storage.search(
            query_vector=query_embedding,
            limit=search_limit
        )
        
        # Filter by threshold and limit to top_k
        return self._filter_results_by_threshold(search_results)
