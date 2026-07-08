# Week 5 Carry-Forward Knowledge Graph

## Source

- week: 05
- lesson theme: GraphRAG foundations, network science, and retrieval architecture
- source text: pasted "What Must You Carry Forward" section plus Act I opening
- created: 2026-07-04

## One-Sentence Summary

Week 5 asks us to cross from RAG over passages to RAG over structure: learn graph mathematics, convert corpora into passages/facts/schemas, compare GraphRAG variants, and decide when graph-shaped retrieval earns its cost.

## Core Learning Path

```text
graph basics
-> adjacency matrix
-> degree distribution
-> real-world heavy-tailed networks
-> small worlds and fractal hierarchy
-> modularity and Leiden communities
-> knowledge graph layers
-> GraphRAG variants
-> Microsoft GraphRAG and MemGraphRAG
-> sidecar routing judgment
```

## Schema Triples

```text
<Concept, requires, Concept>
<Concept, contrasts-with, Concept>
<Concept, has-property, Concept>
<Formula, defines, Concept>
<Metric, diagnoses, GraphProperty>
<Algorithm, optimizes, Metric>
<Algorithm, repairs, Problem>
<System, uses, Algorithm>
<System, computes, Artifact>
<System, targets, QueryType>
<RetrievalMethod, handles, QueryType>
<RetrievalMethod, has-risk, Risk>
<Architecture, routes, QueryType>
```

## Main Nodes

### Graph Mathematics

- graph
- vertex
- edge
- adjacency matrix
- degree
- degree distribution
- Erdos-Renyi random graph
- Poisson distribution
- real-world network
- heavy-tailed distribution
- hub
- preferential attachment
- small-world phenomenon
- weak tie
- finite fractal hierarchy
- modularity
- Louvain
- Leiden
- graph Laplacian
- Fiedler vector

### Knowledge Representation

- corpus
- passage
- fact triplet
- schema triplet
- typing function
- three-layer corpus reading
- knowledge graph
- entity graph

### GraphRAG Systems

- query-time neighbor expansion
- Microsoft GraphRAG
- community summaries
- map-reduce querying
- MemGraphRAG
- shared memory
- semantic energy diffusion
- personalized PageRank
- Pinit(e)
- Pinit(t)
- Pinit(p)

### Architecture Judgment

- global sensemaking query
- point query
- high-value sub-corpus
- small corpus
- real-time latency floor
- sidecar architecture
- preserve then decide

## Fact Triples

```text
<graph, consists-of, vertices>
<graph, consists-of, edges>
<adjacency matrix, represents, graph connectivity>
<adjacency matrix, enables, linear algebra over graphs>
<degree, is-computed-from, row sum of adjacency matrix>
<degree distribution, diagnoses, large graph structure>

<Erdos-Renyi random graph, has-degree-distribution, Poisson distribution>
<Erdos-Renyi random graph, lacks, hubs>
<real-world network, has-degree-distribution, heavy-tailed distribution>
<real-world network, contains, hubs>
<preferential attachment, generates, hubs>
<preferential attachment, explains, heavy-tailed distribution>

<small-world phenomenon, combines, short paths>
<small-world phenomenon, combines, high clustering>
<weak tie, creates, long-range shortcut>
<knowledge, organized-as, communities within communities>
<finite fractal hierarchy, means, statistically self-similar finite levels>

<modularity, measures, community quality>
<modularity, compares, actual graph edges against random expectation>
<Louvain, optimizes, modularity>
<Louvain, permits, internally disconnected communities>
<Leiden, repairs, Louvain pathology>
<Leiden, guarantees, well-connected communities>

<graph Laplacian, is-defined-as, L = D - A>
<xT L x, measures, graph signal smoothness>
<Fiedler vector, indicates, natural graph split>

<fact triplet, describes, concrete entity relationship>
<schema triplet, describes, typed relationship pattern>
<typing function, maps, entity to type>
<three-layer corpus reading, contains, passages>
<three-layer corpus reading, contains, facts>
<three-layer corpus reading, contains, schemas>

<query-time neighbor expansion, computes, local graph neighborhood>
<Microsoft GraphRAG, computes, community summary hierarchy>
<Microsoft GraphRAG, uses, extraction>
<Microsoft GraphRAG, uses, Leiden communities>
<Microsoft GraphRAG, uses, hierarchical community summaries>
<Microsoft GraphRAG, uses, map-reduce querying>
<Microsoft GraphRAG, targets, global sensemaking query>

<MemGraphRAG, uses, shared memory>
<MemGraphRAG, builds, three-layer graph>
<MemGraphRAG, computes, Pinit(e)>
<MemGraphRAG, computes, Pinit(t)>
<MemGraphRAG, computes, Pinit(p)>
<Pinit(e), uses, mean over facts>
<Pinit(t), uses, hub suppression>
<Pinit(p), uses, dampened passage score with IDF density>
<MemGraphRAG, uses, personalized PageRank>
<personalized PageRank, redistributes, semantic energy>

<MemGraphRAG critique, includes, grounding as category error>
<MemGraphRAG critique, includes, contradictions as first-class citizens>
<MemGraphRAG critique, includes, frequency is not importance>
<preserve then decide, unites, MemGraphRAG critiques>

<GraphRAG, pays-rent-on, global synthesis over high-value sub-corpus>
<GraphRAG, anti-pattern-for, point queries>
<GraphRAG, anti-pattern-for, small corpora>
<GraphRAG, anti-pattern-for, real-time latency floors>
<sidecar architecture, routes, high-value graph queries>
<sidecar architecture, keeps, local point queries in plain retrieval>
```

## Important Retrieval Questions

### What must I know before implementing GraphRAG?

You need graph basics, adjacency matrices, degree distributions, hubs, small worlds, community detection, knowledge graph triplets, and the difference between local passage retrieval and global structure-aware retrieval.

### Why is degree distribution the first diagnostic?

It tells whether the graph behaves like random noise or a real-world network. Heavy tails and hubs change retrieval behavior: hubs help navigation, but naive neighbor expansion can flood retrieval with generic noise.

### Why does Microsoft GraphRAG use Leiden?

Microsoft GraphRAG needs meaningful communities to summarize. Leiden repairs Louvain's disconnected-community pathology and produces better-connected communities for hierarchical summaries.

### What does MemGraphRAG compute?

MemGraphRAG builds a three-layer graph over passages, facts, and schemas; initializes relevance over entities, types, and passages; then redistributes semantic energy through personalized PageRank.

### When should GraphRAG be a sidecar?

Use graph retrieval for high-value global sensemaking queries over a large enough corpus. Keep point queries, small corpora, and low-latency chat lanes on simpler retrieval unless evals prove otherwise.

## Agent-First Interpretation

This graph supports the project loop:

```text
intent
-> classify query as local, multi-hop, or global
-> retrieve using passage, artifact, tree, or graph index
-> decide whether graph machinery pays rent
-> respond with grounded evidence
-> trace which path was used
-> evaluate answerability and cost
```

Useful trace fields:

- query type: point, multi-hop, global sensemaking
- selected retrieval path
- graph statistics used: degree distribution, hubs, communities
- community detector and resolution
- whether graph sidecar was invoked
- retrieved passages, facts, schemas, and summaries
- cost and latency
- answerability score

## Avaloka Application

Avaloka can use the same architecture:

```text
memory notes / sessions / project context
-> entities, events, practices, values, themes
-> graph communities
-> scoped memory summaries
-> router chooses local retrieval or graph sensemaking
```

Graph retrieval is most useful for questions like:

- "What recurring pattern connects these memories?"
- "Which values and practices appear across this project?"
- "Where are there contradictions or unresolved tensions?"
- "What themes connect my learning, job search, and Avaloka?"

Plain retrieval is better for:

- "What did I write last week?"
- "What is the exact note about SAGE?"
- "Which file contains the Handshake prep?"

