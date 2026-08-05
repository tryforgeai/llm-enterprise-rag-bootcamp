# Relevance Detection System

Training and evaluating a relevance detection model using Hugging Face transformers and labelled data consisting of relevant as well as irrelevant (out of domain) textual chunks.

## Features

- **Modular Design**: Clean separation of concerns with dedicated modules for data processing, model training, evaluation, and prediction
- **Hugging Face Integration**: Built on top of Hugging Face transformers and datasets libraries
- **Configurable**: Flexible configuration system with presets for different use cases
- **Production Ready**: Includes logging, error handling, and comprehensive evaluation metrics
- **CLI Interface**: Easy-to-use command-line interface for all operations
- **Threshold Optimization**: Automatic optimization of classification thresholds for optimal performance
- **Synthetic Data Generation**: Uses Ollama with Llama 3.1 to generate training data
- **ModernBERT Integration**: Fine-tunes ModernBERT-Large for high-performance relevance detection

## Prerequisites

Before running this codebase, ensure you have the following installed:

- Python 3.12 or higher
- [Ollama](https://ollama.ai/) for local LLM inference
- [uv](https://docs.astral.sh/uv/) for Python package management

## Setup and Running Procedure

Follow these steps in order to run the complete relevance detection pipeline:

### 1. Setup Ollama Locally

First, install and start Ollama on your local machine:

```bash
# Install Ollama (macOS/Linux)
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve
```

### 2. Pull Llama 3.1 Model

Download the Llama 3.1 model to make it available locally:

```bash
ollama pull llama3.1:latest
```

This model will be used by the synthetic data generator to create training data.

### 3. Install Dependencies

Navigate to the project root and install dependencies using uv:

```bash
cd relevance_detector
uv sync
```

This will create a virtual environment and install all required packages defined in `pyproject.toml`.

### 4. Generate Synthetic Data

Run the synthetic data generator to create training data:

```bash
uv run ./src/rel_detector/synth_data_generation/synthetic_data_generator.py
```

This script will:
- Connect to your local Ollama instance
- Use the Llama 3.1 model to generate positive samples (mammal-related content) and negative samples (non-mammal content)
- Save the data in `data/synthetic_data/synthetic_data.jsonl` format
- Create approximately 1000 training samples by default

### 5. Fine-tune the ModernBERT Model

Train the relevance detection model:

```bash
uv run ./src/rel_detector/classification/relevance_detector.py
```

This will:
- Load the ModernBERT-Large model from Hugging Face
- Use the synthetic data for training (80% training, 20% validation)
- Fine-tune the model for sequence classification
- Save the trained model to `models/relevance_detector/`
- Report training metrics and optimal threshold

### 6. Evaluate the Model

Open and run the Jupyter notebook to load and evaluate the fine-tuned model:

```bash
# Navigate to the notebooks directory
cd docs/notebooks

# Start Jupyter (if not already running)
jupyter notebook

# Open relevance_detector.ipynb
```

The notebook will:
- Load the trained model from `models/relevance_detector/`
- Evaluate performance on the validation set
- Demonstrate predictions on sample texts
- Show detailed metrics including accuracy, precision, recall, and F1-score

## Expected Results

After completing the pipeline, you should see:

- **Synthetic Data**: ~1000 samples in `data/synthetic_data/synthetic_data.jsonl`
- **Trained Model**: Saved in `models/relevance_detector/`
- **High Performance**: Accuracy, precision, and recall >99% on validation set
- **Sample Predictions**: Correct classification of mammal vs non-mammal content

## Data Format

The system generates and uses data in JSONL format:

```json
{"text": "Dolphins have been observed teaching each other complex hunting techniques.", "label": 1}
{"text": "The new smartphone app allows users to track their daily steps.", "label": 0}
```

Where:
- `text`: The input sentence to classify
- `label`: 1 for relevant (mammal-related), 0 for irrelevant (non-mammal)

## Model Architecture

The system uses ModernBERT-Large for sequence classification:

1. **Tokenization**: Converts text to token IDs using ModernBERT tokenizer
2. **Encoding**: Passes tokens through the ModernBERT backbone
3. **Classification**: Applies a classification head to predict relevance
4. **Thresholding**: Applies an optimized threshold for final predictions

## Training Process

1. **Data Loading**: Loads synthetic data and splits into training (80%) and validation (20%) sets
2. **Model Setup**: Initializes ModernBERT-Large for sequence classification
3. **Training**: Fine-tunes the model using the Hugging Face Trainer
4. **Threshold Optimization**: Finds the optimal classification threshold
5. **Evaluation**: Computes comprehensive metrics on the validation set
6. **Model Saving**: Saves the trained model, tokenizer, and configuration

## Evaluation Metrics

The system computes the following metrics:

- **Accuracy**: Overall classification accuracy
- **Precision**: Precision for the relevant class
- **Recall**: Recall for the relevant class
- **F1-Score**: Harmonic mean of precision and recall
- **Classification Report**: Detailed per-class metrics

## Troubleshooting

### Common Issues

1. **Ollama Connection Error**: Ensure Ollama is running (`ollama serve`) and the model is downloaded (`ollama pull llama3.1:latest`)

2. **CUDA Memory Issues**: The system automatically detects and uses the best available device (CUDA, MPS, or CPU)

3. **Dependency Issues**: Use `uv sync` to ensure all dependencies are properly installed

4. **Model Loading**: Ensure the training step completed successfully and the model was saved to `models/relevance_detector/`

### Performance Optimization

- For faster training: Reduce batch size or use a smaller model
- For better accuracy: Increase training epochs or use more synthetic data
- For memory efficiency: Enable gradient accumulation or use mixed precision

## API Reference

### RelevanceDetector

Main class for training and using relevance detection models.

#### Methods

- `train(freeze_backbone=False)`: Train the model
- `evaluate(dataset)`: Evaluate on a dataset
- `predict(text)`: Predict relevance of a single text
- `predict_batch(texts)`: Predict relevance of multiple texts
- `save_model()`: Save the trained model
- `load_model(model_path)`: Load a trained model

### DataProcessor

Handles data loading and preprocessing.

#### Methods

- `load_data()`: Load and split data

### SyntheticDataGenerator

Generates synthetic training data using Ollama.

#### Methods

- `generate_synthetic_data(length=1000)`: Generate synthetic data samples
- `_generate_samples_with_prompt()`: Generate samples using specific prompts

