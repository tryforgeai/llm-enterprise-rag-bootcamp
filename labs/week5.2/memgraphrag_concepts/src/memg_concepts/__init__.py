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
from memg_concepts.config import DEFAULT_DATA_DIR, DEFAULT_PDF, resolve_llm_settings
from memg_concepts.document import build_passages_from_dir, discover_pdfs
from memg_concepts.pipeline import MemGraphRAGIndex, build_index, query_index
from dotenv import load_dotenv

load_dotenv()

config = ConfigurationMixin().load_config()



__all__ = [
    "config",
    "DEFAULT_DATA_DIR",
    "DEFAULT_PDF",
    "resolve_llm_settings",
    "build_passages_from_dir",
    "discover_pdfs",
    "MemGraphRAGIndex",
    "build_index",
    "query_index",
]
