# Glossary

## Embedding

A numerical vector representation of text, image, audio, video, or other data.

## Vector Database

A system that stores embeddings and retrieves items by similarity.

## RAG

Retrieval-Augmented Generation. A system retrieves relevant context before asking an LLM to generate an answer.

## Retrieval Funnel

A multi-stage retrieval process, often moving from broad recall to reranking and filtering.

## Dense Retrieval

Retrieval using embeddings and vector similarity.

## Semantic Search

Retrieval that ranks items by similarity in a learned representation space rather than requiring exact keyword matches.

## Cosine Similarity

A similarity measure based on the angle between two vectors. It is commonly used to compare embeddings, although the exact scoring behavior depends on the model and retrieval library.

## Top-K Retrieval

Returning the `k` highest-ranked candidates from a retrieval stage.

## Corpus ID

An identifier or index that connects a retrieval result back to its original corpus item.

## Multimodal Embedding

A vector representation designed so different data types, such as text and images, can be compared in a shared or aligned representation space.

## CLIP

Contrastive Language-Image Pre-training. A model family trained to align images and text, enabling tasks such as text-to-image semantic search.

## Sparse Retrieval

Retrieval using lexical signals such as keywords, BM25, or token overlap.

## Reranking

Taking initial retrieved candidates and scoring them again with a stronger model or more precise method.

## GraphRAG

Retrieval that extracts entities and relationships from source text, organizes them into a knowledge graph, detects communities, and uses graph structure or community summaries to answer local, multi-hop, and corpus-wide questions.

## RAPTOR

Recursive Abstractive Processing for Tree-Organized Retrieval. It recursively embeds, clusters, and summarizes text into a tree so retrieval can use detailed chunks or higher-level summaries.

## SAGE

A precise-retrieval RAG framework combining semantic segmentation, relevance-score-gradient-based chunk selection, and LLM self-feedback to reduce missing and noisy retrieved context. It is complementary to graph-based corpus reasoning rather than a direct GraphRAG replacement.

## Ragas

A framework for evaluating RAG pipelines.

## MRR

Mean Reciprocal Rank. A ranking metric based on the reciprocal position of the first relevant result, averaged across queries.

## MAP

Mean Average Precision. A ranking metric that averages precision measured at relevant-result positions, then averages across queries.

## NDCG

Normalized Discounted Cumulative Gain. A ranking metric that supports graded relevance and discounts useful results appearing lower in the ranking.

## FActScore

A factual-precision metric that decomposes generated text into atomic facts and measures the percentage supported by a reliable knowledge source.

## Text-to-SQL

Translating a natural-language question into a constrained SQL query so an authorized structured database can answer it.

## LLM-as-a-Judge

Using an LLM to evaluate outputs, often with a strict rubric.

## Guardrail

A safety or quality control layer that constrains or reviews AI behavior.

## Helpful, Harmless, and Honest

A high-level AI behavior rubric: provide useful assistance, avoid preventable harm, and remain truthful about evidence, uncertainty, and limitations.

## Request Guardrail

A pre-model check that can approve, block, sanitize, constrain, or route an incoming request before retrieval, tool use, or generation.

## Response Grounding

Post-generation verification that important claims are supported by permitted, relevant, and sufficiently current evidence before the response is released.

## Assertion-Evidence Graph

A structured representation connecting each response claim to supporting, derived, or contradicting evidence and its verification status.

## Agent

A system that can interpret a goal or user state, choose a next step, use context or tools, observe results, and adjust future behavior.

## Agentic RAG

RAG used inside an agent loop. Retrieval informs a decision such as answer, ask, refuse, escalate, use a tool, update memory, or run an eval.

## Trace

A structured record of what the agent saw, retrieved, decided, produced, and how the result was evaluated.

## Semantic Cache

A cache that reuses responses or retrieval results based on semantic similarity, not exact text match.
