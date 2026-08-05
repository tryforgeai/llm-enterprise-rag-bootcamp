#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
'''
The data model of each batch of synthetic data
'''
from pydantic import BaseModel, Field

class SyntheticDataModel(BaseModel):
    text: str = Field(..., 
        description="""The sentence that is either about animals or quotes about animals,
        or something totally unrelated to animals""")
    label: int = Field(...,
        description="""The label of the synthetic data, 1 for positive and 0 for negative,
         where positive is about animals and quotes about animals,
          and negative is about anything else""")

class SyntheticDataBatchModel(BaseModel):
    batch: list[SyntheticDataModel] = Field(..., 
        description="The batch of synthetic data returned in one call to the ollama model")
