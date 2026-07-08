# T008: Benchmark Avaloka Memory Reader V0

Status: todo

## Goal

Measure the existing deterministic Avaloka memory reader before adding embeddings, hybrid retrieval, reranking, RAPTOR, or GraphRAG.

## Scope

- Create at least 30 labeled retrieval cases.
- Include hard negatives, no-match, stale-memory, safety-priority, tone, and avoid-response cases.
- Run the existing deterministic reader as the baseline.
- Record Recall@5, MRR, NDCG@5, unsafe retrievals, stale retrievals, no-match precision, and latency.
- Classify misses by likely intervention: tags, query transformation, embeddings, reranking, or graph-shaped retrieval.

## Done When

- A versioned retrieval dataset exists.
- Baseline metrics are saved as a durable report.
- At least five representative failures are traced.
- The next retrieval component is selected from measured failures, or the current reader is retained if it is sufficient.

