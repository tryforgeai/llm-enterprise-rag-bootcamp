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
Streamlit UI for the SupportVectors RAG System.

This module provides a simple web interface for querying the RAG system through
the FastAPI service. Users can enter queries and view responses with referenced
chunks in a clean, tabular format.
"""

import os
from typing import Optional, Dict, Any

import pandas as pd
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()


# Configuration: API endpoint URL (defaults to localhost:8000)
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
QUERY_ENDPOINT = f"{API_BASE_URL}/query"


def query_rag_service(query: str, similarity_threshold: float = 0.7, top_k: int = 5) -> Optional[Dict[str, Any]]:
    """
    Send a query to the RAG FastAPI service and return the response.
    
    Args:
        query: The user's natural language query string.
        similarity_threshold: Minimum similarity score for retrieved chunks (0.0-1.0).
        top_k: Maximum number of chunks to retrieve.
        
    Returns:
        Dictionary containing the API response with 'answer', 'referenced_chunks', and 'query',
        or None if the request failed.
    """
    try:
        # Prepare the request payload
        payload = {
            "query": query,
            "similarity_threshold": similarity_threshold,
            "top_k": top_k
        }
        
        # Send POST request to the query endpoint
        response = requests.post(QUERY_ENDPOINT, json=payload, timeout=60)
        response.raise_for_status()  # Raise an exception for bad status codes
        
        return response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to RAG service: {e}")
        return None


def display_referenced_chunks(chunks: list) -> None:
    """
    Display referenced chunks in a formatted table.
    
    Args:
        chunks: List of referenced chunk dictionaries containing metadata and text.
    """
    if not chunks:
        st.info("No referenced chunks available.")
        return
    
    # Prepare data for the table display
    table_data = []
    for idx, chunk in enumerate(chunks, start=1):
        table_data.append({
            "Rank": idx,
            "Similarity Score": f"{chunk['similarity_score']:.3f}",
            "PDF": chunk['pdf_name'],
            "Folder": chunk['folder_name'],
            "Semantic Text": chunk['semantic_text'][:200] + "..." if len(chunk['semantic_text']) > 200 else chunk['semantic_text']
        })
    
    # Display as a dataframe table
    df = pd.DataFrame(table_data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Display full text in expandable sections
    st.subheader("Full Chunk Details")
    for idx, chunk in enumerate(chunks, start=1):
        with st.expander(f"Chunk {idx} - {chunk['pdf_name']} (Score: {chunk['similarity_score']:.3f})"):
            st.write("**Semantic Text:**")
            st.write(chunk['semantic_text'])
            st.write("**Parent Text:**")
            st.write(chunk['parent_text'])


def main():
    """
    Main Streamlit application entry point.
    
    Sets up the UI layout, handles user input, and displays RAG responses
    in a tabbed interface.
    """
    # Page configuration
    st.set_page_config(
        page_title="SupportVectors RAG System",
        page_icon="🔍",
        layout="wide"
    )
    
    # Title and description
    st.title("🔍 SupportVectors RAG System")
    st.markdown("Query the knowledge base using natural language questions.")
    
    # Sidebar for advanced options
    with st.sidebar:
        st.header("⚙️ Settings")
        similarity_threshold = st.slider(
            "Similarity Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.05,
            help="Minimum similarity score for retrieved chunks (0.0-1.0)"
        )
        top_k = st.slider(
            "Top K Results",
            min_value=1,
            max_value=20,
            value=5,
            step=1,
            help="Maximum number of chunks to retrieve"
        )
    
    # Main query input area
    query = st.text_input(
        "Enter your question:",
        placeholder="e.g., What is machine learning?",
        key="query_input"
    )
    
    # Submit button
    submit_button = st.button("Submit Query", type="primary", use_container_width=True)
    
    # Process query when button is clicked
    if submit_button:
        if not query.strip():
            st.warning("Please enter a question before submitting.")
        else:
            # Show loading spinner while processing
            with st.spinner("Processing your query..."):
                # Call the RAG service
                response = query_rag_service(
                    query=query,
                    similarity_threshold=similarity_threshold,
                    top_k=top_k
                )
            
            # Display results if response is available
            if response:
                # Create tabs for answer and referenced chunks
                tab1, tab2 = st.tabs(["📝 Answer", "📚 Referenced Chunks"])
                
                # Tab 1: Display the generated answer
                with tab1:
                    st.subheader("Generated Answer")
                    st.write(response.get("answer", "No answer generated."))
                    
                    # Show query info
                    st.divider()
                    st.caption(f"**Query:** {response.get('query', 'N/A')}")
                    st.caption(f"**Chunks Used:** {len(response.get('referenced_chunks', []))}")
                
                # Tab 2: Display referenced chunks in table format
                with tab2:
                    st.subheader("Referenced Chunks")
                    referenced_chunks = response.get("referenced_chunks", [])
                    display_referenced_chunks(referenced_chunks)


if __name__ == "__main__":
    main()
