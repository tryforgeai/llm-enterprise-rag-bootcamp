# Chunking Pipeline
This topic walks through a three-notebook sequence in `docs/notebooks` that builds from fundamentals to an end-to-end chunking pipeline.

## Notebooks
1. **Docling basics**  
   Intro to using Docling to chunk documents based on markup boundaries.  
   Notebook: `docs/notebooks/01-docling_chunking.ipynb`

2. **Contextual and late chunking**  
   Explores contextual and late chunking with an entire document treated as a single parent chunk.  
   Notebook: `docs/notebooks/02-contextual_and_late_chunking.ipynb`

3. **Chunking pipeline use case**  
   Demonstrates a real pipeline: Docling creates parent chunks, Chonkie refines to semantic boundaries, then two paths:  
   - **Contextual chunking**: contextualize the semantic chunks from Chonkie  
   - **Late chunking**: use Jina embeddings with mean pooling, informed by Chonkie’s semantic boundaries over parent-chunk tokens  
   Notebook: `docs/notebooks/03-chunking_pipeline.ipynb`
