#  -------------------------------------------------------------------------------------------------
#   Copyright (c) 2016-2025.  SupportVectors AI Lab
#   This code is part of the training material and, therefore, part of the intellectual property.
#   It may not be reused or shared without the explicit, written permission of SupportVectors.
#
#   Use is limited to the duration and purpose of the training at SupportVectors.
#
#   Author: SupportVectors AI Training Team
#  -------------------------------------------------------------------------------------------------
from rel_detector.classification.relevance_detector import RelevanceDetector

def main():
    model_path = "models/relevance_detector"
    
    # Initialize the detector with GPU optimizations
    detector = RelevanceDetector()

    # Load the trained model for evaluation
    detector.load_model(model_path)

    # Test predictions
    test_texts = [
        "Dolphins have been observed teaching each other complex hunting techniques.",
        "The new smartphone app allows users to track their daily steps.",
        "Elephants have a highly developed brain and are considered one of the smartest animals.",
        "The economy is expected to experience a significant downturn.",
        "What do you know about animals?",
        "What do you know about animals",
    ]
    
    print("\nTesting predictions:")
    for text in test_texts:
        result = detector.predict(text)
        print(f"Text: {text[:50]}...")
        print(f"  Relevant: {result['is_relevant']} (prob: {result['relevance_probability']:.3f})")
        print()

if __name__ == "__main__":
    main()