# T011 Week 02 Class Capture

Status: doing

Date: 2026-06-13

## Goal

Capture Week 02 material on softmax, negative log-likelihood, attention, contextual embeddings, pooling, anisotropy, contrastive learning, and multimodal retrieval.

## Working File

`course/week-02.zh.md`

## Done Criteria

- [x] Portal-map learning objectives are summarized.
- [x] Core equations and intuitions are recorded.
- [x] Week 01 overlap and Week 02 additions are distinguished.
- [x] Required and optional reading lists are recorded.
- [x] One agent capability is identified.
- [x] Avaloka Memory Reader implications are recorded.
- [x] Classroom examples and calculations are added.
- [x] Code or notebook experiments are recorded.
- [ ] At least one Week 02 eval artifact is created.

## 2026-06-15 Update

Captured the Saturday afternoon embedding-space evaluation lesson:

- cosine similarity histogram as a diagnostic for semantic retrieval quality
- anisotropic raw BERT versus more isotropic MiniLM / Sentence-BERT
- fine-tuned subject encoder as task-shaped embedding space
- definitions of `mean`, `std`, `intra`, `inter`, and `gap`
- key result that the fine-tuned encoder had the largest same/different separation
- Avaloka implication: future embedding retrieval must be judged by same-class versus hard-negative separation, not by isolated successful examples
