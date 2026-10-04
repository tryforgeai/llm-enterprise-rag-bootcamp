# 2026-06-06 Shared Course Record

Status: Captured

Source:

- [ChatGPT shared conversation](https://chatgpt.com/share/6a24ac5d-c624-83e8-9e5e-68a060898004)

Captured on: 2026-06-06

## Purpose

This file preserves the durable learning content from the shared conversation and links it to the canonical Week 01 notes.

Canonical synthesized notes:

- [Week 01](../week_01/week-01.md)

Avaloka implementation comparison:

- [Avaloka AI Week 01 Capability Audit](../../reviews/04-avaloka-week-01-capability-audit.md)

## Coverage

The shared conversation contains:

- later Week 01 notes on HHH, evaluation, Text-to-SQL, and architecture judgment
- the decision to treat Avaloka's existing behavior as the baseline
- a workflow for mapping each lesson to Avaloka
- a text semantic-search lab using `SentenceTransformers`
- a course repository identified as `rag_to_riches`
- a multimodal semantic-search example using CLIP

The shared page includes image attachments whose visual contents are not exposed in the text export. Their captions include:

- RAG's role in the generation pipeline
- hallucination
- adding confidential and unseen information
- historical indexing
- vectors as machine language
- three kinds of embeddings
- a Jabber text example

Those captions are preserved here, but image-only details should be recovered from the original recording, notebook, or screenshots before being treated as exact lecture claims.

## Durable Learning Summary

### RAG And Hallucination

The course frames RAG as the layer that gives a model relevant external evidence at answer time. It can add private or previously unseen information without retraining the base model.

RAG reduces some causes of hallucination by supplying evidence, but does not guarantee truth. Retrieval can still miss evidence, return irrelevant passages, or provide context that the generator misuses.

### Semantic Search Lab

The lab uses this conceptual flow:

```text
corpus sentences
-> sentence embeddings
-> query embedding
-> vector similarity
-> ranked top-k results
-> corpus IDs
-> original source text
```

Representative code from the shared record:

```python
query_text = "a friendship with animals"
query = embedder.encode(query_text, convert_to_tensor=True)

from sentence_transformers import util

search_results = util.semantic_search(
    query_embeddings=query,
    corpus_embeddings=embeddings,
    top_k=3,
)
```

The result contains:

- `corpus_id`: the index of the original sentence
- `score`: the semantic relevance score

The code then uses `corpus_id` to recover the original text.

Key lesson:

> Semantic search retrieves by learned vector similarity rather than requiring an exact keyword match.

### Teaching Repository

The shared record identifies the SupportVectors repository `rag_to_riches` as the teaching project used for the lab.

Its learning progression is described as:

```text
keyword search
-> semantic search
-> sentence embeddings
-> vector similarity
-> search index
-> top-k retrieval
-> RAG
```

This is a teaching skeleton, not a complete production RAG architecture.

### Multimodal Semantic Search

The later lab moves from text retrieval to image retrieval with:

```python
model = SentenceTransformer("clip-ViT-B-32")
```

CLIP maps text and images into a comparable vector space:

```text
image -> vector
text query -> vector
-> cross-modal similarity
-> ranked images
```

The example creates an index of image filenames and image embeddings, then uses a text query to retrieve semantically related images.

Precomputed image embeddings are reused to avoid repeated embedding cost. This is embedding reuse, not the same thing as the semantic response cache discussed elsewhere in the course.

### Avaloka Boundary

For Avaloka, semantic similarity alone is insufficient:

```text
semantic retrieval
-> permission filter
-> sensitivity and memory-scope filter
-> reranking
-> grounding
-> HHH guardian
-> trace and eval
```

The key product rule is:

> Similarity does not imply permission to use or reveal the retrieved item.

Potential multimodal Avaloka sources include course screenshots, diagrams, handwritten notes, and user-provided images. Such a design must account for faces, addresses, medical information, workplace material, and other sensitive content.

## Course Learning Workflow

For future classes, use this fixed transformation:

```text
what the course taught
-> simple explanation
-> Avaloka mapping
-> existing implementation evidence
-> missing evidence or capability
-> whether the technique is justified now
-> next experiment or task
```

The governing question remains:

> Does this technique measurably make Avaloka more Helpful, Harmless, or Honest?

