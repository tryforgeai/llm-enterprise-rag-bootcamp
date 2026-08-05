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
This module contains the code for generating synthetic data for training the relevance detection tool.

The synthetic data is generated using the following approach:
    1. Use the locally running ollama model: llama3.1:latest
    2. Create positive samples for sentences that have something to do with animals/quotes about animals and
    negative samples for sentences that have nothing to do with animals/quotes about animals.
    3. The ollama model will be used to generate these positive and negative samples.
    4. The format of the data will be a JSONL file with each line having the following format:
        {"text": "positive_sentence", "label": "positive"}
        {"text": "negative sentence", "label": "negative"}
    5. The data will be saved in the data/synthetic_data/ directory.
    6. The data folder and sub-folder will be created if they don't exist.
'''
from pathlib import Path
from openai import OpenAI
import instructor
from instructor import patch
from rel_detector.synth_data_generation.synthetic_data_model import SyntheticDataBatchModel
import json

class SyntheticDataGenerator:
    def __init__(self, batch_size: int = 20):
        self.data_folder = "data/synthetic_data/"
        self.data_folder_path = Path(self.data_folder)
        self.data_folder_path.mkdir(parents=True, exist_ok=True)
        self.file_name = "synthetic_data.jsonl"
        self.file_path = self.data_folder_path / self.file_name
        self.ollama_model = "llama3.1:latest"
        self.batch_size = batch_size

    def _generate_samples_with_prompt(self, client, prompt: str, sample_type: str) -> list:
        """
        Generate samples using a specific prompt.
        
        Args:
            client: The OpenAI client instance
            prompt: The prompt to use for generation
            sample_type: Either 'positive' or 'negative' for logging purposes
            
        Returns:
            List of sample dictionaries with 'text' and 'label' fields
        """
        try:
            response: SyntheticDataBatchModel = client.chat.completions.parse(
                model=self.ollama_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                response_format=SyntheticDataBatchModel,
            )
            
            parsed_data = response.choices[0].message.parsed
            samples = parsed_data.batch
            
            print(f"Generated {len(samples)} {sample_type} samples")
            return samples
            
        except Exception as e:
            print(f"Error generating {sample_type} samples: {e}")
            return []

    def _get_positive_prompt(self, count: int) -> str:
        """Generate prompt for positive samples (mammal-related content)."""
        return f"""Generate exactly {count} positive samples (label 1) about mammals.

FORMAT: Return a JSON object with a "batch" array containing exactly {count} objects, each with "text" and "label" fields where label=1.

POSITIVE SAMPLES (label 1) - {count} required:
Write exactly {count} sentences about mammals only (dogs, cats, elephants, dolphins, whales, seals, lions, tigers, bears, etc.). Include animal behavior, facts, or quotes about mammals. NO birds, reptiles, fish, or insects.

Examples of good positive samples:
- "Dogs are known for their loyalty and companionship."
- "Elephants have excellent memories and strong family bonds."
- "Dolphins are highly intelligent marine mammals."
- "Lions are apex predators in the African savanna."

CRITICAL: You must return exactly {count} samples with label=1."""

    def _get_negative_prompt(self, count: int) -> str:
        """Generate prompt for negative samples (non-mammal content)."""
        return f"""Generate exactly {count} negative samples (label 0) about topics unrelated to mammals.

FORMAT: Return a JSON object with a "batch" array containing exactly {count} objects, each with "text" and "label" fields where label=0.

NEGATIVE SAMPLES (label 0) - {count} required:
Write exactly {count} sentences about topics completely unrelated to mammals, such as:
- Technology, computers, software
- Food, cooking, recipes
- Sports, games, entertainment
- Business, finance, economics
- Science (physics, chemistry, astronomy)
- History, politics, current events
- Art, music, literature
- Travel, geography, places
- Weather, nature (without animals)
- Daily activities, work, school

Examples of good negative samples:
- "Python is a popular programming language for data science."
- "The Great Wall of China is over 13,000 miles long."
- "Chocolate chip cookies are a classic American dessert."
- "Basketball was invented by Dr. James Naismith in 1891."

CRITICAL: You must return exactly {count} samples with label=0."""

    def generate_synthetic_data(self, length: int = 1000):
        '''
        Generate synthetic data for training the relevance detection tool.
        '''
        # Create a client for the ollama model using the OpenAI API
        client = patch(OpenAI(base_url="http://localhost:11434/v1"), mode=instructor.Mode.JSON)
        
        # Create the file if it doesn't exist
        if not self.file_path.exists():
            self.file_path.touch()

        # Count the total number of positive and negative samples generated
        total_positive_samples = 0
        total_negative_samples = 0
        
        # Generate data in batches
        for i in range(0, length, self.batch_size):
            batch_size_actual = min(self.batch_size, length - i)
            print(f"\n--- Batch {i//self.batch_size + 1} ---")
            
            # Generate positive samples
            positive_prompt = self._get_positive_prompt(batch_size_actual)
            positive_samples = self._generate_samples_with_prompt(client, positive_prompt, "positive")
            
            # Generate negative samples
            negative_prompt = self._get_negative_prompt(batch_size_actual)
            negative_samples = self._generate_samples_with_prompt(client, negative_prompt, "negative")
            
            # Validate batch balance
            expected_count = batch_size_actual
            actual_positive = len(positive_samples)
            actual_negative = len(negative_samples)
            
            print(f"Batch {i//self.batch_size + 1}: Positive samples: {actual_positive}/{expected_count}, Negative samples: {actual_negative}/{expected_count}")
            
            if actual_positive != expected_count or actual_negative != expected_count:
                print(f"WARNING: Expected {expected_count} of each type, but got {actual_positive} positive and {actual_negative} negative")

            # Save the synthetic data to the file
            with open(self.file_path, "a") as f:
                for sample in positive_samples + negative_samples:
                    f.write(json.dumps(sample.model_dump()) + "\n")

            # Update the total counts
            total_positive_samples += len(positive_samples)
            total_negative_samples += len(negative_samples)

        print("\n=== FINAL SUMMARY ===")
        print(f"Synthetic data saved to {self.file_path}")
        print(f"Total positive samples: {total_positive_samples}")
        print(f"Total negative samples: {total_negative_samples}")
        print(f"Balance ratio: {total_positive_samples/total_negative_samples:.2f}:1")

if __name__ == "__main__":
    generator = SyntheticDataGenerator()
    generator.generate_synthetic_data()

