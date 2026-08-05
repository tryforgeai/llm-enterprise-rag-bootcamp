#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""Document converter wrapper for Docling."""

import os
from typing import List, Any

from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker


class DocumentConverterWrapper:
    """Wrapper class for Docling document conversion and parent chunking.
    
    This class handles the conversion of PDF documents into structured
    parent chunks using Docling's HybridChunker.
    
    Attributes:
        converter: Docling DocumentConverter instance
        chunker: Docling HybridChunker instance
    """
    
    def __init__(self, max_tokens: int = 5000):
        """Initialize the document converter and chunker."""
        self.converter = DocumentConverter()
        self.chunker = HybridChunker(max_tokens=max_tokens)
    
    def convert_and_chunk(self, pdf_path: str) -> List[Any]:
        """Convert a PDF document and create parent chunks.
        
        Args:
            pdf_path: Path to the PDF file to process
            
        Returns:
            List of parent chunks from Docling's HybridChunker
            
        Raises:
            FileNotFoundError: If the PDF file does not exist
            Exception: If document conversion or chunking fails
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        doc = self.converter.convert(source=pdf_path).document
        parent_chunks = list(self.chunker.chunk(doc))
        return parent_chunks

