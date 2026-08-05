#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------

"""Semantic chunker wrapper for Chonkie."""

from typing import List, Any

from chonkie import SemanticChunker


class SemanticChunkerWrapper:
    """Wrapper class for Chonkie semantic chunking.
    
    This class handles the creation of semantic chunks from parent chunks
    using Chonkie's SemanticChunker.
    
    Attributes:
        chunker: Chonkie SemanticChunker instance
    """
    
    def __init__(self):
        """Initialize the semantic chunker with default settings."""
        self.chunker = SemanticChunker()
    
    def chunk(self, text: str) -> List[Any]:
        """Create semantic chunks from a text string.
        
        Args:
            text: The text to chunk semantically
            
        Returns:
            List of semantic chunks from Chonkie
        """
        return self.chunker.chunk(text)

