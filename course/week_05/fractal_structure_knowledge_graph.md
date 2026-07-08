# Fractal Structure Knowledge Graph

## Source

- week: 05
- lesson theme: GraphRAG, communities, finite fractal hierarchy
- source text: pasted class note about "Fractal Structure — But in the Real World"
- created: 2026-07-04

## One-Sentence Summary

Knowledge graphs can exhibit a finite fractal-like structure: subjects contain topics, topics contain subtopics, and those nested communities can be detected with graph community algorithms such as Leiden and summarized by GraphRAG.

## Core Idea

The lesson's argument is:

```text
knowledge graph
-> contains communities within communities
-> has finite self-similar hierarchy
-> can be partitioned by community detection
-> can be summarized at multiple altitudes
-> supports GraphRAG global sensemaking
```

This is "fractal, but in the real world": not infinite mathematical recursion, but a finite number of meaningful levels.

## Schema Triples

```text
<Document, contains, Section>
<Section, discusses, Concept>
<Concept, has-property, GraphProperty>
<Concept, analogous-to, Concept>
<Concept, contrasts-with, Concept>
<Concept, contains, Concept>
<Algorithm, optimizes, Metric>
<Algorithm, detects, Concept>
<Algorithm, repairs, AlgorithmProblem>
<System, uses, Algorithm>
<System, summarizes, Concept>
<Person, proposed, Concept>
<Metric, measures, GraphProperty>
```

## Entity Types

- `DOCUMENT`
- `SECTION`
- `CONCEPT`
- `GRAPH_PROPERTY`
- `ALGORITHM`
- `METRIC`
- `SYSTEM`
- `PERSON`
- `PROBLEM`
- `METHOD`

## Fact Triples

```text
<knowledge graph, has-property, fractal structure>
<fractal structure, means, communities within communities>
<fractal structure, is, statistical finite self-similarity>
<mathematical fractal, has-property, infinite self-similarity>
<real network, has-property, finite zoom depth>

<knowledge city, contains, continents>
<continents, include, sciences>
<continents, include, law>
<continents, include, humanities>
<science, contains, physics>
<science, contains, biology>
<science, contains, computer science>
<computer science, contains, systems>
<computer science, contains, theory>
<computer science, contains, machine learning>
<machine learning, contains, vision>
<machine learning, contains, language>
<machine learning, contains, reinforcement learning>

<knowledge graph, contains, dense communities>
<knowledge graph, contains, sparse bridges>
<knowledge graph, contains, local hubs>
<community, contains, subcommunities>
<community, resembles, miniature whole graph>

<Barabasi, associated-with, scale invariance>
<scale invariance, describes, subtopics within topics within subjects>
<large knowledge graphs, exhibit, scale invariance>

<Microsoft GraphRAG, builds, hierarchy>
<Microsoft GraphRAG, summarizes, corpus at multiple altitudes>
<Microsoft GraphRAG hierarchy, has-depth, 2-4 levels>
<finite zoom depth, is, design parameter>
<too many hierarchy levels, summarizes, noise>

<community, is, vertices more densely connected internally than externally>
<Newman, introduced, modularity>
<modularity, measures, relational surplus>
<modularity, compares, actual edges against expected random edges>
<high modularity, indicates, real communities>
<community detection, optimizes, modularity>

<RAPTOR, clusters, chunks>
<RAPTOR, uses, embedding proximity>
<modularity, clusters, vertices>
<modularity, uses, relational surplus>
<RAPTOR, asks, who sounds alike>
<modularity, asks, who is wired together>
<mature architecture, keeps, RAPTOR>
<mature architecture, keeps, graph community detection>

<Louvain algorithm, optimizes, modularity>
<Louvain algorithm, shuffles, vertices between communities>
<Louvain algorithm, collapses, communities into super-vertices>
<Louvain algorithm, can-output, internally disconnected communities>

<Leiden algorithm, repairs, Louvain pathology>
<Leiden algorithm, guarantees, well-connected communities>
<Leiden algorithm, builds, hierarchy>
<Leiden algorithm, detects, communities in entity graph>
<Microsoft GraphRAG, uses, Leiden algorithm>
<Leiden algorithm, is-engine-of, Microsoft GraphRAG>
```

## Retrieval Questions This Graph Can Answer

### Why can GraphRAG summarize at multiple levels?

Because knowledge graphs can contain communities within communities. If those communities are meaningful for a finite number of levels, GraphRAG can summarize leaf communities, then summarize parent communities, creating multiple abstraction levels.

### What algorithm does Microsoft GraphRAG use for community detection?

Microsoft GraphRAG uses Leiden to detect communities in the entity graph.

### Why does the lesson prefer Leiden over Louvain?

Louvain optimizes modularity but can produce internally disconnected communities. Leiden adds a refinement step and guarantees well-connected communities, which makes the communities safer to summarize.

### How is RAPTOR different from graph community detection?

RAPTOR clusters chunks by embedding proximity: "who sounds alike?" Graph community detection clusters graph vertices by relational surplus: "who is wired together?"

## GraphRAG Interpretation

This note belongs to the Week 5 idea:

```text
passage retrieval
-> derived artifacts
-> graph of entities and relations
-> community hierarchy
-> community summaries
-> global sensemaking answers
```

The main caution is that the hierarchy should stop when subdivisions stop being meaningful. Real-world fractal structure is finite, so recursive summarization should be treated as a design parameter, not an infinite process.

## Avaloka Application

Avaloka memory can use this pattern carefully:

```text
user memories
-> themes, events, values, relationships, practices
-> memory graph
-> communities of related patterns
-> summaries at safe scopes
-> retrieval only when relevant and permitted
```

Potential useful communities:

- recurring emotional patterns
- trusted practices
- project themes
- relationship contexts
- values and boundaries

The safety requirement is to preserve provenance and scope. A memory community summary should not expose raw private memories unless the current intent and privacy policy allow it.

