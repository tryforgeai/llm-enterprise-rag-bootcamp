#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
from typing import Dict, List


class ClaimDocumentMatrixBuilder:
    """Constructs the Cartesian product of claims and evidence documents.

    Each matrix element represents one (claim, document) pair to be scored in
    later semantic filtering and entailment stages.
    """

    def build(self, claims: List[str], documents: List[str]) -> List[Dict[str, object]]:
        """Build the claim-document matrix for pairwise evaluation.

        Args:
            claims: Ordered list of claim strings extracted from the response.
            documents: Ordered list of chunk or document texts used as evidence.

        Returns:
            A list of edge dictionaries. Each dict has keys ``claim_index``,
            ``document_index``, ``claim``, and ``document``.
        """
        matrix: List[Dict[str, object]] = []
        for claim_index, claim in enumerate(claims):
            for document_index, document in enumerate(documents):
                matrix.append(
                    {
                        "claim_index": claim_index,
                        "document_index": document_index,
                        "claim": claim,
                        "document": document,
                    }
                )
        return matrix
