# Instructor Questions

## Embeddings

1. Which embedding models are used in the labs?
2. How should we choose between OpenAI, BGE, E5, GTE, Voyage, or multimodal embedding models?
3. How do we evaluate whether embeddings are good enough for a domain?

## Chunking

1. When should we use semantic chunking instead of fixed-size chunking?
2. How should we chunk spiritual, philosophical, or emotionally sensitive content?
3. How do we keep context without creating giant chunks?

## GraphRAG

1. When does GraphRAG become worth the complexity?
2. What graph schema is best for memory and care facts?
3. How do we combine vector retrieval and graph traversal?

## Evals

1. What is the smallest useful RAG eval suite?
2. How should LLM-as-a-judge be constrained?
3. How do we test safety, not just correctness?

## Agentic RAG

1. What is the smallest useful agentic RAG loop beyond retrieve-and-answer?
2. How should an agent decide between answering, asking a clarifying question, refusing, escalating, or using a tool?
3. What trace fields are most important for debugging agent behavior?

## Multimodal

1. How should audio/video be chunked for retrieval?
2. Should we embed transcript, audio features, visual frames, or summaries?
3. How do we evaluate video/audio comprehension quality?

## Avaloka-Specific

1. How would you design retrieval for a long-term emotional support companion?
2. How do we avoid retrieved memories making responses creepy?
3. How do we keep spiritual source material useful without sounding doctrinal?
4. How should Avaloka decide when not to use a retrieved memory?
