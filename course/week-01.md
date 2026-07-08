# Week 01 Notes

[中文版](week-01.zh.md)

## Lecture Summary

The course presents enterprise RAG as one end-to-end pipeline rather than a collection of isolated techniques:

```text
raw document
-> ingestion
-> retrieval
-> enrichment
-> scalable architecture
-> safety and trust
-> evaluation
-> measured, trustworthy answer
```

The pipeline also creates a bridge from unstructured documents to structured data.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/01-course-journey.png]]

## Concepts

### Course Journey: Fourteen Instruments, One Pipeline

1. **Foundations**
   - Getting started
   - How the machine learns

2. **Ingestion**
   - Chunking
   - The slide describes chunking as "the first irreversible cut"

3. **Retrieval**
   - Retrieval pipeline
   - Query transformation

4. **Enrichment**
   - Derivative artifacts
   - RAPTOR
   - GraphRAG

5. **Architecture & Speed**
   - Scale determines architecture
   - Semantic cache

6. **Safety & Trust**
   - Request guardrails
   - Response grounding

7. **Proof & Frontier**
   - Evaluation and metrics
   - Text-to-SQL

### Initial Interpretation

- RAG quality is determined by the whole pipeline, not only the model or vector database.
- Chunking is called irreversible because later retrieval can only work with the structure preserved during ingestion.
- Trustworthy answers require both request-time controls and evidence-grounded responses.
- Evaluation is part of the pipeline, not a final optional check.

### What Is RAG?

RAG stands for **Retrieval-Augmented Generation**.

The course describes it as giving a language model an open book at the moment it answers. Instead of relying only on knowledge stored in the model's frozen parameters, the system retrieves relevant material from selected documents and includes it as context for generation.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/02-what-is-rag.png]]

Minimal flow:

```text
user question
-> retrieve relevant document passages
-> give question + passages to the language model
-> generate an answer grounded in those passages
```

Key distinction:

```text
model training
= changes what is stored in model parameters

RAG
= supplies external evidence at answer time
```

RAG does not automatically guarantee correctness. The system can still retrieve the wrong passages, omit important evidence, or generate claims unsupported by the retrieved context.

### Why RAG Will Not Die

Course claim:

> The context window is not a filing cabinet. It is a desk. You still need the library.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/03-rag-will-not-die.png]]

Interpretation:

- A context window is temporary working space.
- A document or knowledge system is the larger library.
- Even a very large context window does not automatically select the most relevant, current, authorized, and trustworthy evidence.
- RAG provides the search, selection, filtering, and evidence-delivery layer between the library and the model's desk.

```text
knowledge library
-> retrieve relevant evidence
-> place selected evidence in context window
-> reason and answer
```

The first working system in the course will be a semantic-search-to-answer loop. The course will also explain the economic intuition for when RAG is more appropriate than fine-tuning.

Initial RAG versus fine-tuning distinction:

| Need | RAG | Fine-tuning |
|---|---|---|
| Frequently changing facts | Strong fit | Expensive to update repeatedly |
| Source attribution | Easier to preserve | Knowledge source is less visible |
| Private document access | Can retrieve at answer time | Training may create privacy and deletion concerns |
| Behavior or style change | Limited | Often a stronger fit |
| Quick knowledge update | Re-index documents | Retrain or continue training |

### How The Machine Learns: Embedding Refresher

This module takes a first-principles look at how embeddings are trained and what it means to turn meaning into geometry.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/04-how-the-machine-learns.png]]

Working mental model:

```text
text or other input
-> embedding model
-> numerical vector
-> position in a high-dimensional space
```

"Meaning into geometry" means that the model learns a space where vector relationships can serve as signals for semantic relationships:

- related items should often be closer
- unrelated items should often be farther apart
- directions and neighborhoods can encode useful patterns

An embedding is not meaning itself. It is a learned numerical representation optimized by a model and training objective. Its geometry may preserve some relationships while losing or distorting others.

Topics to capture as the lecture continues:

- What training objective creates the embedding space?
- What counts as a positive or negative training pair?
- Which similarity or distance measure is used?
- When does geometric closeness fail to match human meaning?
- How does the training data affect retrieval quality?

### Everything Downstream Rests On The Embedding Space

The embedding space is the foundation for multiple downstream techniques:

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/05-embedding-space-foundation.png]]

| Technique | Dependency on embedding geometry |
|---|---|
| Retrieval | Relevant queries and documents must be close under the chosen similarity measure. |
| Reranking | Candidate ordering depends on whether relevance signals are represented correctly. |
| Semantic caching | Similar requests must land close enough to justify reusing a result. |
| Clustering | Meaningful groups require useful neighborhoods and separation in vector space. |

Key course principle:

> If we misread the geometry, later techniques become guesswork.

Practical implication: do not choose an embedding model or similarity threshold only because it is popular. Test its neighborhoods, false positives, false negatives, and domain-specific behavior.

### Chunking: The First Cut

Chunking divides documents into units that can be embedded, indexed, retrieved, and passed to a model.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/06-chunking-first-cut.png]]

This is one of the most consequential pipeline decisions because it defines the information units available to retrieval:

```text
raw document
-> choose boundaries
-> create chunks
-> embed and index chunks
```

Important trade-off:

- chunks that are too small may lose context and relationships
- chunks that are too large may mix topics, weaken retrieval precision, and consume excess context
- poor boundaries may separate a claim from its explanation, qualifier, table, heading, or source
- overlap may preserve continuity but increases storage, duplicate retrieval, and token usage

### Why The First Projection Is Called Irreversible

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/07-chunking-irreversible.png]]

Course principle:

> No reranker, prompt, or stronger model can recover information that the indexed chunks failed to preserve.

More precise engineering interpretation:

- Downstream components cannot recover context missing from the current index.
- If the original source documents are retained, the system can reprocess and re-chunk them.
- Therefore, preserve raw sources, chunking configuration, parser version, and provenance so ingestion can be reproduced.

Chunking establishes the ceiling for the current retrieval index. Better reranking can reorder available chunks, but it cannot retrieve a relationship that was destroyed or omitted during ingestion.

### The Retrieval Pipeline

The course presents retrieval as a multi-stage engine rather than a single vector search:

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/08-retrieval-pipeline.png]]

```text
query
-> sparse retrieval: BM25 / SPLADE
-> dense retrieval: embedding similarity
-> fuse candidate sets
-> reranking cascade
-> final evidence
```

Two complementary lanes:

- **Sparse retrieval** preserves exact lexical signals such as names, IDs, rare terms, and keywords.
- **Dense retrieval** finds semantic similarity even when the query and document use different wording.

Fusion aims for broad recall. A reranking cascade then applies increasingly careful and usually more expensive models to a shrinking candidate set.

Working principle:

```text
early stages: fast and broad
later stages: slower and precise
```

### One Retriever Is Never Enough

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/09-one-retriever-not-enough.png]]

Keyword and semantic retrieval fail in different ways:

- sparse retrieval may miss paraphrases and conceptual matches
- dense retrieval may miss exact identifiers, rare terms, negation, or precise lexical constraints

A production architecture combines both lanes and escalates to expensive scoring only when the expected quality gain justifies the cost.

This is a recall-versus-precision design:

```text
multiple retrievers
-> diverse candidate pool
-> fusion and deduplication
-> progressively stronger scoring
-> small final evidence set
```

### Cost-Aware Escalation Ladder

Course metaphor:

> District court to Supreme Court. Cheap retrievers handle the volume; the cross-encoder hears only the hardest cases.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/10-retrieval-escalation-ladder.png]]

A likely four-stage pattern:

```text
1. sparse and dense retrieval: cheap, parallel, high recall
2. candidate fusion and deduplication
3. lightweight reranking or filtering
4. cross-encoder reranking: expensive, small candidate set
```

A cross-encoder evaluates the query and candidate together, which often gives stronger relevance judgments than comparing independently produced embeddings. The trade-off is higher latency and compute cost.

The escalation policy should consider:

- query difficulty or ambiguity
- disagreement between retrievers
- confidence margin between candidates
- safety or business importance
- latency and cost budget

### Query Transformation: The Translator

Query transformation is a staged pipeline that rewrites a user's messy or ambiguous question into one or more queries the retriever can answer.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/11-query-transformation.png]]

```text
original user question
-> interpret intent and context
-> clarify, normalize, decompose, or expand
-> produce retrieval queries
-> run retrieval
```

Possible transformation operations include:

- resolving pronouns or conversational references
- normalizing abbreviations, names, and terminology
- translating user language into domain vocabulary
- decomposing a multi-part question into subqueries
- generating multiple query variants
- adding constraints such as time, product, source, or jurisdiction

Important distinction:

- **Query transformation** changes the search request to improve evidence retrieval.
- **Response generation** answers the user after evidence has been retrieved.

The transformation must preserve user intent. A fluent rewrite that subtly changes the question can retrieve convincing but irrelevant evidence.

Useful trace fields:

```text
original_query
interpreted_intent
transformed_queries
transformation_reason
retrieval_results_per_query
```

The retriever only sees the version of the question admitted by this translation layer. Query transformation is therefore a retrieval control point, not harmless preprocessing.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/12-query-transformation-six-stage.png]]

The course will build a six-stage query pipeline:

1. **Correction**
   - Fix spelling, malformed text, and obvious input noise.
2. **Context injection**
   - Add relevant conversational or application context.
3. **Jargon expansion**
   - Expand abbreviations and map user language to domain terminology.
4. **Rewriting**
   - Produce a clearer retrieval-oriented query.
5. **Multi-hop decomposition**
   - Split questions that require several facts or reasoning steps.
6. **HyDE**
   - Generate a hypothetical answer or document, embed it, and retrieve real documents similar to that hypothetical representation.

Each stage can improve retrieval, but each can also introduce intent drift. The trace should preserve the input and output of every applied stage.

### Derivative Artifacts: The Prism

Derivative artifacts are distilled, search-oriented views generated from source material and indexed alongside or instead of raw text.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/13-derivative-artifacts.png]]

Examples from the course:

- factoids
- search-friendly rewrites
- question-answer pairs
- summaries

```text
source document
-> derive multiple searchable views
-> link each artifact to its source
-> index raw and/or derived views
```

Why this may help:

- user questions may resemble a generated QA pair more than the source prose
- summaries support higher-level retrieval
- factoids expose atomic claims
- search-friendly rewrites bridge difficult wording

Trust requirement: derivative artifacts are generated interpretations, not primary evidence. Every artifact should retain source provenance, artifact type, generator/version, and a path back to the original text.

### Why Multiple Representations Help

Users ask semantically related questions in many different shapes. A single representation of a document may align well with only some of them.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/14-derivative-artifacts-many-shapes.png]]

For one source passage, the index might contain:

```text
raw passage
+ concise summary
+ atomic factoids
+ likely user questions
+ search-friendly rewrite
```

These representations create several semantic entry points back to the same source. This can increase recall when the user's phrasing is closer to a derived question or summary than to the original prose.

Costs and risks:

- larger index and ingestion cost
- duplicate candidates from the same source
- generated artifacts may contain errors or lose qualifiers
- misleading artifacts may improve similarity while reducing factual fidelity

Required controls:

- attach a shared source ID to all representations
- deduplicate or group candidates by source
- score the original passage before final grounding
- measure recall gain against index size, latency, and false-positive rate

### RAPTOR: Adjustable Retrieval Resolution

RAPTOR stands for **Recursive Abstractive Processing for Tree-Organized Retrieval**.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/15-raptor-adjustable-focal-length.png]]

A flat index stores chunks at roughly one level of detail. RAPTOR recursively groups related chunks and creates summaries, forming a tree with multiple abstraction levels.

```text
detailed source chunks
-> embed and cluster related chunks
-> summarize each cluster
-> embed and cluster the summaries
-> repeat into higher-level summaries
-> retrieve from appropriate tree levels
```

The tree acts like an adjustable focal length:

- narrow factual question -> retrieve detailed leaf chunks
- section-level question -> retrieve intermediate summaries
- broad thematic question -> retrieve higher-level summaries
- complex question -> combine evidence across levels

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/16-raptor-zoom-lens.png]]

The instructor's retrieval-scale analogy:

| Technique | Lens | Best suited for |
| --- | --- | --- |
| Factoids / derivative artifacts | microscope | isolated facts, entities, values, and exact details |
| RAPTOR | zoom lens | moving between source details and hierarchical summaries |
| GraphRAG | telescope | relationships, communities, patterns, and themes spread across the corpus |

These techniques are complementary rather than direct replacements. The right choice depends on the resolution and structure required by the question.

Example:

```text
"What exact threshold was used?"
-> detailed chunk

"What is the document's overall safety strategy?"
-> higher-level summaries plus supporting chunks
```

Why it may help: some questions require local details, while others require understanding information distributed across a long document.

Risks and costs:

- summary generation may omit qualifiers or introduce errors
- tree construction adds ingestion cost
- changed source documents may require tree updates
- broad summaries still need links to supporting source chunks
- not every corpus benefits enough to justify the complexity

### GraphRAG: Whole-Corpus Sense-Making

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/17-graphrag-telescope.png]]

GraphRAG transforms unstructured text into a knowledge graph and uses graph structure to support retrieval:

```text
documents
-> extract entities, relationships, and claims
-> construct a knowledge graph
-> detect related communities
-> generate summaries for those communities
-> answer local or corpus-wide questions
```

Unlike baseline vector retrieval, which searches for chunks similar to the query, GraphRAG can organize evidence around connected entities and communities.

Example question types:

- local: "What relationships does organization X have with project Y?"
- multi-hop: "How is person A indirectly connected to policy B?"
- global: "What major themes and groups appear across the entire corpus?"
- sense-making: "Which communities disagree, and what evidence explains the disagreement?"

Why the instructor calls it a telescope: it helps the system see structures and themes distributed across many documents rather than only examining one matching passage.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/18-graphrag-whole-corpus-structure.png]]

Choosing between RAPTOR and GraphRAG:

| Need | Prefer |
| --- | --- |
| Retrieve the same material at different abstraction levels | RAPTOR |
| Summarize sections or an entire long document | RAPTOR |
| Follow entity-to-entity relationships | GraphRAG |
| Discover communities, networks, or corpus-wide themes | GraphRAG |
| Need both hierarchy and relationships | combine selectively after evaluation |

The deciding question is whether the missing signal is **resolution** or **structure**:

```text
resolution problem -> RAPTOR
relationship / corpus-structure problem -> GraphRAG
```

#### Connection to SAGE

The paper [SAGE: A Framework of Precise Retrieval for RAG](https://arxiv.org/abs/2503.01713) focuses on improving the precision of a conventional chunk-and-vector retrieval pipeline:

Durable project memory: [SAGE paper note](../resources/papers/2503.01713-sage.md)

```text
semantic chunking
-> vector retrieval and reranking
-> dynamically select chunks at the relevance-score drop
-> LLM feedback adjusts whether more or fewer chunks are needed
```

SAGE and GraphRAG address different failure modes:

| Framework | Primary problem |
| --- | --- |
| SAGE | retrieving semantically complete chunks while reducing missing and noisy context |
| GraphRAG | reasoning over entities, relationships, communities, and corpus-wide structure |

They are potentially complementary. SAGE-style semantic segmentation could improve the text units used before graph extraction, while its adaptive selection or feedback ideas could help some local retrieval paths. GraphRAG remains responsible for graph construction and global community reasoning.

Important evidence boundary: the SAGE paper cites the GraphRAG paper, but does not present a direct SAGE-versus-GraphRAG experiment. Its reported comparisons include RAPTOR, not GraphRAG. Combining the two is therefore an architectural inference that would require its own evaluation.

Risks and costs:

- entity and relationship extraction can be incomplete or incorrect
- graph construction and community summarization add substantial ingestion cost
- changing documents requires graph maintenance
- generated relationships and community reports need provenance back to source text
- GraphRAG is unnecessary when questions are mainly simple factual lookups

### Scale Decides Architecture

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/19-scale-decides-architecture.png]]

Architecture should be selected from the demonstrated shape and scale of the problem. Every additional component must justify its cost through measurable improvement.

```text
start with the smallest complete system
-> observe failures in traces and evals
-> classify the failure
-> add the component that addresses it
-> verify that the component improves outcomes
```

Example escalation logic:

| Observed failure | Candidate response |
| --- | --- |
| relevant facts are not retrieved | improve chunking, embeddings, or hybrid retrieval |
| too much or too little context is retrieved | adaptive selection or SAGE-style feedback |
| questions require different levels of summary | RAPTOR |
| questions require relationships or corpus-wide structure | GraphRAG |
| behavior remains systematically wrong despite good evidence | consider prompting, tools, policy logic, then fine-tuning |

This principle prevents architecture from being selected because a technique is fashionable. Complexity must earn its place through domain-specific evals.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/20-architecture-inundation.png]]

The instructor connects this to Galileo's square-cube law: a design that works at one scale may fail at another because costs and constraints do not grow at the same rate.

The practical rule is not to design immediately for maximum scale. Start with a naive but measurable baseline, then escalate only when evidence shows where it fails.

Before adding a component, require:

1. an observed failure in traces or evals
2. a named metric the component should improve
3. an estimate of latency, token, maintenance, and privacy cost
4. a comparison against the current baseline
5. a removal criterion if the expected improvement does not appear

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/21-shapley-style-component-test.png]]

The instructor proposes a Shapley-style test for whether each component earns its place. In practical engineering terms, this is an ablation and marginal-contribution discipline:

```text
measure baseline
-> add one component
-> rerun the same eval set
-> remove or disable the component
-> compare quality and cost deltas
-> retain only when marginal value justifies marginal cost
```

Suggested component scorecard:

| Measure | Baseline | With component | Delta |
| --- | --- | --- | --- |
| retrieval recall / precision | | | |
| grounded answer quality | | | |
| safety failures | | | |
| p50 / p95 latency | | | |
| input and output tokens | | | |
| infrastructure cost | | | |
| maintenance and debugging burden | | | |

For interacting components, test multiple relevant orders or combinations when feasible. A component may have little value alone but meaningful value with another component. This is why "Shapley-style" is broader than a single one-at-a-time benchmark, although an exact Shapley-value calculation is usually unnecessary for an early product.

### Semantic Cache

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/22-semantic-cache.png]]

A semantic cache reuses prior work when a new query has sufficiently similar meaning, even if its wording differs.

```text
new query
-> create embedding
-> search cached query embeddings
-> verify similarity and cache scope
-> cache hit: reuse retrieval or answer
-> cache miss: run pipeline and store eligible result
```

Two useful cache levels:

| Cache level | Reuses | Main trade-off |
| --- | --- | --- |
| retrieval cache | evidence identifiers or ranked results | safer, but evidence may become stale |
| response cache | final generated answer | faster and cheaper, but more likely to reuse an inappropriate or outdated answer |

Correctness requires more than an embedding threshold. A cache key or eligibility check may also need:

- tenant or user scope
- knowledge-index version
- prompt and model version
- safety-policy version
- locale and response mode
- permissions and memory scope
- time-to-live and invalidation rules

Avaloka boundary: do not semantically reuse personalized answers across users. Responses involving private memory, emotional state, crisis risk, health context, or changing user circumstances should bypass shared response caching. Begin, if needed, with public and stable knowledge retrieval caching.

The instructor suggests that a mature workload may serve roughly 90% of queries from cache. Treat this as a workload-dependent production hypothesis to measure, not a universal constant.

If the hit rate is actually that high, the architecture changes materially:

```text
semantic cache = primary serving path
full retrieval and generation = cache-fill / fallback path
```

Implications:

- average latency and inference cost can fall dramatically
- model capacity is concentrated on novel or changed questions
- cache quality determines most user experiences
- a false semantic hit can repeatedly distribute the same wrong answer
- stale entries can survive knowledge, prompt, model, or policy updates
- invalidation, versioning, observability, and cache warming become core architecture
- cache-hit and cache-miss traffic need separate evals and monitoring

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/23-semantic-cache-playing-with-fire.png]]

The course implementation target includes:

1. a domain-fine-tuned embedding model
2. a similarity threshold tuned against precision and recall
3. safeguards for five semantic-cache failure modes

Here, fine-tuning applies to the embedder used to judge query equivalence, not necessarily to the answer-generating model.

Threshold selection creates an asymmetric trade-off:

```text
lower threshold
-> more cache hits and savings
-> more false semantic matches

higher threshold
-> fewer false matches
-> more cache misses and full-pipeline cost
```

For sensitive applications, optimize the threshold for the cost of a false hit rather than maximizing hit rate alone. The exact five failure-mode categories have not yet appeared in the captured slides and should be added from the instructor's definition rather than inferred.

Evaluate:

- cache hit rate
- false-hit rate
- answer-equivalence rate for semantic matches
- latency and token savings
- stale-answer rate
- cross-user or permission leakage
- safety-policy bypasses
- cache-hit versus cache-miss quality

### Request Guardrails

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/24-request-guardrails.png]]

Request guardrails form a gatehouse before the model. The course target is a sixteen-gate input pipeline that inspects every incoming request before it can reach model inference.

The guardrail objective is **Helpful, Harmless, and Honest (HHH)**:

| Principle | Operational meaning |
| --- | --- |
| Helpful | address the user's legitimate intent and provide a useful next step |
| Harmless | avoid preventable harm, unsafe actions, privacy violations, and harmful escalation |
| Honest | ground factual claims, disclose uncertainty and limitations, and avoid fabricated confidence |

These goals must be balanced. Helpfulness does not override safety, harmlessness should not require deception, and honesty includes saying when the system does not know.

```text
incoming request
-> ordered guardrail checks
-> block, sanitize, constrain, route, or approve
-> only approved request reaches retrieval and the model
```

Why guard before generation:

- reject prohibited or dangerous requests early
- prevent prompt injection from reaching tools or private retrieval
- enforce authentication, authorization, tenant, and memory boundaries
- classify risk and route high-risk requests differently
- avoid unnecessary model and retrieval cost
- produce a trace of which gate made the decision

For privacy-sensitive systems, some gates must run before retrieving user memory. A later refusal does not undo an unnecessary private-data access.

The exact sixteen gates have not yet appeared in the captured material. Record the instructor's actual sequence when shown rather than inventing a substitute list.

Suggested trace fields:

- request ID and policy version
- gate name and order
- pass, block, transform, or route result
- reason code and confidence
- redacted evidence used by the gate
- final route and whether retrieval/model execution occurred

### Response Grounding

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/25-response-grounding.png]]

A fluent and confident response may still be unsupported. The generator should not be the sole judge of whether its own answer is grounded.

```text
generated answer
-> extract factual claims
-> map each claim to retrieved evidence
-> verify entailment, provenance, and freshness
-> pass, revise, retrieve again, qualify, or refuse
-> release only the grounded response
```

Grounding checks should distinguish:

- directly supported claims
- reasonable but explicit inferences
- unsupported claims
- claims contradicted by evidence
- claims requiring fresher or higher-authority evidence

The verifier should be meaningfully separated from generation through independent evidence checks, a different prompt or model, deterministic rules, citations, or an external evaluator. Using another LLM alone does not guarantee independence.

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/26-assertion-evidence-graph.png]]

The course implementation target is:

- a three-tier verification hierarchy
- an assertion-evidence graph
- LLM-as-judge at the top of the hierarchy

An assertion-evidence graph represents the response as auditable structure:

```text
assertion node
-> supported_by -> source passage
-> derived_from -> permitted memory or artifact
-> contradicted_by -> conflicting evidence
-> verification_status -> supported / inferred / unsupported / contradicted
```

Every factual assertion must point to evidence or be prevented from leaving the system. This enables sentence- or claim-level revision instead of accepting or rejecting the entire response as one block.

Response grounding primarily enforces the **Honest** part of HHH, while request guardrails and safe routing support **Harmless**. A response still needs to remain **Helpful**, including offering an appropriate alternative or next step when the original request cannot be fulfilled.

The hierarchy should reserve expensive, probabilistic judgment for cases that simpler checks cannot settle. The exact three tiers have not yet appeared in the captured slides and should be recorded from the instructor's specification.

Suggested metrics:

- claim-level support rate
- citation correctness and completeness
- contradiction rate
- unsupported-claim rate
- appropriate abstention rate
- grounding-related retry and escalation rate

### Evaluation And Metrics

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/27-evaluation-and-metrics.png]]

A RAG system needs separate yardsticks for retrieval and generated answers. A good answer score cannot diagnose a retrieval failure, and a good retrieval score does not guarantee a grounded answer.

Retrieval metrics:

| Metric | What it emphasizes |
| --- | --- |
| MRR | how early the first relevant result appears |
| MAP | precision across the ranked positions containing relevant results, averaged across queries |
| NDCG | ranking quality when relevance can have multiple grades, with higher-ranked results weighted more |

Answer and RAG-pipeline metrics:

| Metric / framework | What it emphasizes |
| --- | --- |
| RAGAS | automated evaluation of RAG dimensions such as context relevance, faithfulness, and answer relevance |
| FActScore | decomposes generated text into atomic facts and measures how many are supported by a reliable source |

Evaluation should follow the pipeline:

```text
retrieval
-> ranking metrics
-> context quality
-> claim grounding and factuality
-> answer usefulness
-> safety and operational metrics
```

For an agent-first system, also measure:

- whether the correct next action was selected
- whether memory access obeyed scope and permission
- whether the response was Helpful, Harmless, and Honest
- whether the system appropriately asked, abstained, refused, or escalated
- latency, token cost, cache behavior, and retry rate

Do not collapse all dimensions into one score before inspecting the individual failure signals.

### Text-to-SQL: The Structured-Data Bridge

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/28-text-to-sql.png]]

Text-to-SQL extends evidence access from unstructured documents to structured databases:

```text
natural-language question
-> identify intent and allowed data scope
-> retrieve relevant schema and business definitions
-> generate SQL
-> validate permissions, syntax, and query plan
-> execute in a constrained read-only environment
-> ground the answer in returned rows
```

This is related to RAG because the system must retrieve schema, table relationships, metric definitions, and example queries before generating useful SQL.

Essential controls:

- read-only database credentials by default
- table, column, row, and tenant permissions
- allowlisted operations and query templates where possible
- parameterization and injection defenses
- query complexity, timeout, and result-size limits
- SQL parsing or dry-run validation before execution
- audit logs connecting the question, SQL, result, and answer
- explicit confirmation before any write-capable operation

Text-to-SQL evaluation should include execution correctness, result correctness, permission compliance, efficiency, and whether the final natural-language answer faithfully represents the returned data.

### Course Outcome

![[Projects/LLM and Enterprise RAG Bootcamp/course/assets/week-01/29-course-outcome.png]]

The course's stated three-month outcome is architectural judgment about retrieval:

```text
know what to build
+ know how much architecture the scale requires
+ know how to prove it works
```

For this project, that means using Avaloka's existing capabilities as the baseline, instrumenting them, evaluating real failures, and escalating architecture only when evidence supports the change.

## Code / Lab Notes

Source record:

- [2026-06-06 shared course record](sources/2026-06-06-shared-chat-record.md)

### Text Semantic Search With SentenceTransformers

The teaching project identified in the shared record is SupportVectors' `rag_to_riches`, a rapid tutorial for learning the basic RAG retrieval path.

The lab first embeds the corpus:

```python
embeddings = embedder.encode(sentences, convert_to_tensor=True)
```

It then embeds a query and performs semantic search:

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

Conceptual flow:

```text
query text
-> query embedding
-> compare against corpus embeddings
-> rank by vector similarity
-> return top-k corpus IDs and scores
-> look up original source text
```

`corpus_id` identifies the original item in `sentences`. The relevance score indicates how close the query and corpus item are under the embedding model's similarity function.

The important distinction is:

```text
keyword search -> match lexical form
semantic search -> match learned representational similarity
```

Semantic similarity is probabilistic. A high score is not proof that a result is correct, permitted, current, or safe to use.

### Image Search With CLIP

The later lab creates an embedding index for images using:

```python
model = SentenceTransformer("clip-ViT-B-32")
```

CLIP places text and images in a comparable embedding space:

```text
images -> image embeddings
text query -> text embedding
-> compare across modalities
-> retrieve semantically related images
```

The image index is conceptually:

```text
image filename + image embedding
```

The course example can reuse precomputed image embeddings because image embedding is more expensive than loading an existing vector. This is cached embedding computation, not semantic answer caching.

### Lab Evidence Boundary

The shared conversation includes image-only slides or notebook screenshots about hallucination, confidential and unseen information, historical indexing, vector language, embedding variants, and a Jabber text example. Their captions are recorded in the source note, but exact image content remains to be recovered from the original recording or notebook.

## Agent Capability Unlocked

An agent can treat knowledge access as a measured pipeline:

```text
ingest -> retrieve -> enrich -> decide -> guard -> ground -> evaluate
```

This gives the agent more than retrieval. It gives it a path for transforming queries, selecting evidence, applying safety boundaries, and measuring answer quality.

Embeddings give the agent semantic lookup: it can retrieve related items even when the query and source use different words. This capability is probabilistic and must be evaluated with domain-specific examples.

Because retrieval, reranking, caching, and clustering all depend on this space, embedding evaluation is a foundation-level agent eval rather than a low-level implementation detail.

Multimodal embeddings extend that lookup across data types. An agent can use text to retrieve images when both modalities share a learned vector space, but permission, sensitivity, provenance, and grounding rules still apply after similarity search.

Chunking controls what evidence the agent can retrieve at all. Hybrid retrieval improves the agent's recall by combining exact-match and semantic signals, while reranking improves which evidence reaches the final reasoning step.

A cost-aware retrieval ladder lets the agent reserve expensive judgment for uncertain or high-stakes cases rather than paying maximum cost for every query.

Query transformation gives the agent a translation layer between human language and retrieval-system language. It should ask for clarification when ambiguity cannot be resolved safely rather than silently inventing intent.

Derivative artifacts give the agent multiple retrieval surfaces for the same source. They can improve recall, but final answers should ground claims in original or verified source material rather than treating generated summaries or QA pairs as unquestioned truth.

RAPTOR gives the agent multi-resolution retrieval. It can search for a precise detail or retrieve a higher-level synthesis depending on the question.

## Evidence / Memory / Tool / Eval Needed

- Evidence: source documents, chunks, retrieved passages, and grounding citations
- Memory: not defined yet; memory must follow separate scope and privacy rules
- Tool: embedding model, ingestion pipeline, retriever, query transformer, cache, guardrails, and evaluator
- Eval: embedding neighborhood quality, retrieval quality, grounding, safety, latency, and end-to-end answer quality

## Questions

- Why is chunking considered the first irreversible cut?
- What are the fourteen instruments represented by the seven pipeline stages?
- At what scale does architecture need to change?
- How are request guardrails evaluated separately from response grounding?
- Why is Text-to-SQL grouped with evaluation and frontier topics?
- How should a RAG system behave when retrieval finds no reliable evidence?
- How do we measure whether the generated answer is actually grounded in the retrieved passages?
- At what corpus size or context length does retrieval become economically better than sending all documents?
- Which problems should use RAG, fine-tuning, or both?
- What exactly is the training objective for the embedding model shown in class?
- Why does distance or angle between vectors represent semantic similarity?
- What information is lost when meaning is compressed into a fixed-size vector?
- How should we inspect an embedding neighborhood before trusting retrieval?
- Should retrieval, caching, and clustering use the same embedding model and threshold?
- How do we detect when the embedding space works poorly for a specialized domain?
- Which three embedding variants did the instructor compare, and what task is each intended for?
- Which embedding model and similarity function does the `rag_to_riches` text lab use?
- Does `util.semantic_search` normalize vectors or select cosine similarity automatically in this notebook?
- How should multimodal retrieval be evaluated when text and images are only loosely related?
- Which image metadata and privacy rules must survive embedding and indexing?
- Which chunking strategy will the course use as the baseline?
- How should chunk size and overlap be evaluated instead of guessed?
- How are sparse and dense results fused?
- Which rerankers are used at each stage, and what is their latency/cost?
- What metric decides whether the retrieval funnel improved quality?
- How does the system decide that a query is hard enough to require a cross-encoder?
- What candidate counts are used before and after each stage?
- How should latency, cost, recall, and precision be evaluated together?
- Which query transformations are deterministic and which use an LLM?
- How do we evaluate whether a transformed query preserved the user's intent?
- When should the system ask a clarifying question instead of rewriting automatically?
- Should every transformed query and its retrieved results be saved in the trace?
- At which of the six transformation stages can retrieval be skipped?
- How is HyDE evaluated when the hypothetical answer contains incorrect assumptions?
- Are derivative artifacts embedded in the same index as raw chunks or routed separately?
- How does the system prevent generated factoids and summaries from becoming false evidence?
- How many representations per source provide useful recall before duplication becomes harmful?
- Should reranking score the derivative artifact, the original source, or both?
- How does RAPTOR choose which abstraction level to retrieve?
- Does the course use tree traversal or search across all tree nodes?
- How are summary errors detected and traced back to source chunks?
- What evals show that RAPTOR beats simpler chunk plus reranker retrieval?

## Avaloka Application

Avaloka should not treat memory retrieval as one vector search call. Its future knowledge path should be designed as a complete pipeline:

```text
approved source or memory
-> privacy-aware ingestion
-> retrieval and query transformation
-> enrichment with care and safety context
-> bounded next-step decision
-> request and response guardrails
-> grounded response
-> trace and eval
```

The strongest immediate lesson is that Avaloka's safety, retrieval, and evaluation layers must be designed together.

For Avaloka, RAG could provide an approved "open book" containing product knowledge, care principles, safety rules, and selected user-safe memories. The model should not treat every retrieved item as permission to expose it; retrieval and response permission remain separate decisions.

The text semantic-search lab is the smallest prototype of an Avaloka retrieval path:

```text
approved documents or memories
-> embeddings
-> query embedding
-> top-k retrieval
-> original evidence lookup
```

Avaloka must extend the teaching skeleton:

```text
semantic search
-> permission and memory-scope filter
-> sensitivity filter
-> reranker
-> grounding check
-> HHH guardian
-> trace and eval
```

For a future multimodal path, images and screenshots may contain private or sensitive evidence. Image similarity must never bypass authorization, provenance, retention, or response-disclosure rules.

The desk/library metaphor also applies to Avaloka:

- context window: the small set of evidence currently placed on the desk
- knowledge and approved memory stores: the library
- retrieval policy: the librarian deciding what may be brought to the desk
- response guardrail: the rule deciding what may be said to the user

## Follow-Up Tasks

- Record the teacher's explanation of why chunking is irreversible.
- Map each of the fourteen instruments to the seven course stages as they are introduced.
- Add specific metrics when the evaluation module is explained.
- Build the semantic-search-to-answer loop shown in the foundation module.
- Capture the teacher's cost comparison between RAG and fine-tuning.
- Create a small Avaloka embedding-neighborhood test before choosing a production embedding model.
- Reproduce the `rag_to_riches` text semantic-search lab and save the environment, model name, corpus, query, and ranked output.
- Recover the instructor's three embedding categories from the notebook or recording.
- Add a small CLIP text-to-image eval with relevant, ambiguous, and sensitive-image cases.
- Preserve Avaloka raw sources and ingestion metadata so documents can be re-chunked.
- Compare sparse-only, dense-only, and hybrid retrieval on the same Avaloka eval questions.
- Escalate Avaloka's safety-sensitive or low-confidence retrieval cases to a stronger reranker.
- Add original and transformed query fields to Avaloka retrieval traces.
- Keep every Avaloka derivative artifact linked to its approved source and never expose it as raw user memory.
- Evaluate whether question-style artifacts improve Avaloka retrieval without increasing unsupported claims.
- Delay RAPTOR for Avaloka until broad questions fail with simpler retrieval and traces show a real multi-resolution need.

## Afternoon Foundation: Transformer Internals And LARQL Preparation

Source record:

- [2026-06-06 afternoon Transformer and LARQL record](sources/2026-06-06-afternoon-transformer-larql-record.md)

### Hugging Face Access Lessons

The afternoon setup work separated three different concerns:

```text
CLI authentication
!= TLS certificate trust
!= gated-model repository authorization
```

- `hf auth login` authenticates the local CLI with a Hugging Face token.
- The reported `CERTIFICATE_VERIFY_FAILED` error came from the local Python certificate chain and a corporate proxy certificate, not from an invalid Hugging Face token.
- A successful login still did not authorize `google/gemma-3-4b-it`; the account must separately accept or receive access to the gated Gemma repository.

Useful commands:

```bash
hf auth login
hf auth whoami
hf download google/gemma-3-4b-it
```

Do not store access tokens in this project.

### Transformer Block Mental Model

The Illustrated Transformer provides the visual foundation:

- Query: what the current token is looking for
- Key: what each available token offers for matching
- Value: the information retrieved from matching tokens
- causal mask: prevents a generated token from seeing future positions
- multi-head attention: learns several relationship views in parallel
- residual stream: carries and accumulates contributions across layers
- MLP/FFN: transforms each token position and writes learned features

The simplified data flow is:

```text
token representation
-> causal multi-head self-attention
-> add attention contribution to residual stream
-> MLP / FFN feature transformation
-> add FFN contribution to residual stream
-> next Transformer block
```

Core equations:

```text
A = softmax(QK^T / sqrt(d_k))
Z = AV
x' = x + Attention(x)
x'' = x' + MLP(x')
```

Useful first approximation:

```text
attention -> exchange information across token positions
MLP / FFN -> transform and write features
residual stream -> preserve the evolving shared state
```

### Why This Matters For LARQL

LARQL is studying the path between internal model features and output behavior:

```text
attention contribution
+ FFN contribution
-> residual-stream trajectory
-> output-token ranking
```

Its read-only commands can help compare different views:

- `DESCRIBE`: inferred feature associations
- `WALK`: movement through feature neighborhoods
- `TRACE`: answer trajectory and layer contributions
- `INFER`: actual next-token behavior

This creates a useful falsification question:

> Does the internal association reported by browsing agree with the model's behavior under inference, paraphrase, negation, and ambiguous context?

Internal traces can explain or diagnose model behavior. They do not establish current truth, source provenance, or permission to expose information.

### Agent Capability Unlocked

The agent can gain a second kind of trace:

```text
external trace
-> retrieved evidence, decisions, safety checks, answer

internal research trace
-> layer trajectory, attention/FFN contribution, token preference
```

For Avaloka, internal tracing may eventually help investigate unsafe associations or overconfident language. External grounding, Care Card permissions, and HHH review remain authoritative for production behavior.

### Follow-Up

- Complete Hugging Face access approval for a supported small model.
- Read The Illustrated Transformer before deeper LARQL implementation work.
- Preserve the read-only boundary in task T009.
- Compare `DESCRIBE`, `WALK`, `TRACE`, and `INFER` on public or synthetic cases.
- Never put Hugging Face tokens or private Avaloka memory into course files or model patches.
