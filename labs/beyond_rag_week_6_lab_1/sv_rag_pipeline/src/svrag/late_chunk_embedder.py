#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""Late chunk embedder using Jina AI models."""

from typing import List, Dict, Any

from transformers import AutoTokenizer, AutoModel
import torch

import os
import requests
from dotenv import load_dotenv
load_dotenv()


class LateChunkEmbedder:
    """Class for creating late chunk embeddings using Jina AI models.
    
    This class implements the late chunking approach where embeddings are
    created from the parent chunk context, preserving semantic relationships
    that might be lost during semantic chunking.
    
    Attributes:
        model_name: Name of the Jina embedding model to use
        tokenizer: AutoTokenizer instance for the model
        model: AutoModel instance for generating embeddings
        device: Device to run the model on (cuda/cpu/mps)
    """
    
    def __init__(self, model_name: str = "jinaai/jina-embeddings-v2-base-en", is_local: bool = True):
        """Initialize the late chunk embedder with a Jina model.
        
        Args:
            model_name: Name of the Jina embedding model to use
            is_local: Whether the model is local or not - non-local is supported only during inference time, not during chunking.  
        """
        self.is_local = is_local
        if self.is_local:
            self.model_name = model_name
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, 
                trust_remote_code=True
            )
            self.model = AutoModel.from_pretrained(
                model_name, 
                trust_remote_code=True, 
                output_hidden_states=True
            )
            
            # Determine device
            if torch.cuda.is_available():
                self.device = "cuda"
            elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
                self.device = "mps"
            else:
                self.device = "cpu"
            
            self.model.to(self.device)
            self.model.eval()
        else: 
            # call the jina api by doing a python POST call where below is the equivalent curl call
            # that returns a json that contains a data field as a list of dictionaries where
            # each dictionary contains an embedding field with the embedding of the corresponding string
            # of the input list of strings in the input field
            '''
            curl --location 'http://feynman:8123/embed/v1/embeddings' \
            --header 'Content-Type: application/json' \
            --data '{
                    "model": "jinaai/jina-embeddings-v2-base-en",
                    "input": [
                        "Ray Serve is a scalable model serving framework.",
                        "vLLM is optimized for high-throughput inference."
                    ]
            }'
            '''
            # so here just initialize the model name and the host and port.  The
            # actual call is done in the encode_query method
            self.model_name = model_name
            self.host = os.getenv("EMBEDDING_HOST", "feynman")
            self.port = int(os.getenv("EMBEDDING_PORT", "8123"))
            self.base_url = f"http://{self.host}:{self.port}/embed-text/v1/embeddings"

    def embed_parent_chunk(self, parent_chunk: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create embeddings for semantic chunks within a parent chunk.
        
        This method implements late chunking by:
        1. Tokenizing and embedding the entire parent chunk
        2. Extracting embeddings for each semantic chunk based on character offsets
        3. Averaging token embeddings that overlap with each semantic chunk
        
        Args:
            parent_chunk: Dictionary containing parent chunk data with keys:
                - id: Parent chunk identifier
                - text: Full text of the parent chunk
                - semantic_chunks: List of semantic chunk dictionaries with:
                    - id: Semantic chunk identifier
                    - text: Text content
                    - start_char: Starting character index
                    - end_char: Ending character index
                    
        Returns:
            List of enriched chunk dictionaries with embeddings, containing:
                - semantic_id: Semantic chunk identifier
                - parent_id: Parent chunk identifier
                - parent_text: Full parent chunk text
                - text: Semantic chunk text
                - num_tokens: Number of tokens in the semantic chunk
                - embedding: Vector embedding as a list
        """
        if not self.is_local:
            # raise an exception that embedding chunks is not supported for non-local models
            raise Exception("Embedding chunks is not supported for non-local models!!")

        text = parent_chunk["text"]
        sem_chunks = parent_chunk["semantic_chunks"]
        
        # Tokenize the parent chunk with offset mapping
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=False, 
            return_offsets_mapping=True
        )
        
        # Move inputs to device
        inputs = {k: v.to(self.device) if isinstance(v, torch.Tensor) else v 
                 for k, v in inputs.items()}
        
        # Save offsets separately
        offsets = inputs.pop("offset_mapping")[0].cpu().tolist()
        
        # Generate embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        token_embs = outputs.last_hidden_state.squeeze(0)
        
        # Create enriched semantic chunks
        enriched_semantics = []
        for sc in sem_chunks:
            s, e = sc["start_char"], sc["end_char"]
            
            # Find token indices that overlap with this semantic chunk
            indices = [
                i for i, (ts, te) in enumerate(offsets) 
                if te > s and ts < e
            ]
            
            if not indices:
                continue
            
            # Average the embeddings of overlapping tokens
            emb = token_embs[indices].mean(dim=0).cpu().numpy()
            
            enriched_semantics.append({
                "semantic_id": sc["id"],
                "parent_id": parent_chunk["id"],
                "parent_text": parent_chunk["text"],
                "text": sc["text"],
                "num_tokens": len(indices),
                "embedding": emb.tolist(),
            })
        
        return enriched_semantics
    
    def encode_query_non_local(self, query: str) -> List[float]:
        """Encode a query string into an embedding vector.
        
        Args:
            query: The query string to encode
            
        Returns:
            Embedding vector as a list of floats
        """
        response = requests.post(self.base_url, json={"model": self.model_name, "input": [query]})
        return response.json()["data"][0]["embedding"]

    def encode_query(self, query: str) -> List[float]:
        """Encode a query string into an embedding vector.
        
        Args:
            query: The query string to encode
            
        Returns:
            Embedding vector as a list of floats
        """
        if not self.is_local:
            return self.encode_query_non_local(query)
        
        # Else use the local model
        # Use the model's encode method if available, otherwise tokenize and embed
        if hasattr(self.model, 'encode'):
            return self.model.encode(query).tolist()
        else:
            inputs = self.tokenizer(query, return_tensors="pt", truncation=True)
            inputs = {k: v.to(self.device) if isinstance(v, torch.Tensor) else v 
                     for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Use mean pooling for query embedding
            embedding = outputs.last_hidden_state.mean(dim=1).squeeze(0).cpu().numpy()
            return embedding.tolist()

