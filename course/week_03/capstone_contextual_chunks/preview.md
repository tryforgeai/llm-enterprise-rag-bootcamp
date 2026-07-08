# Contextual Chunk Preview

## Chunk 0 | pages 1-5

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', pages 1-5, under 'Capstone Project Briefs'. It should be retrieved for questions involving these local terms: pillar, page, building, learned, contents, capstone, supportvectors, all.

**Original chunk preview**

[Page 1]
Capstone Project Briefs
Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys
Asif Qamar

[Page 2]
pepal leaves publisher
www.supportvectors.ai
All rights reserved. The contents in this document are the intellectual property of SupportVectors. No
part of it can be shared at all without the explicit permission of the author.
First draft, April 9, 2026

[Page 3]
Contents
Building What You Have Learned 3
The Open Casebook 15
The Field Medic’s Library 29
The Stack Overflow Oracle 43
The Earnings Analyst 57
The Legislative Cartographer 69
The Patent Prospector 77
The Clinical Trial Matchmaker 87
The Compliance Sentinel 97
The Maintenance Oracle 109
The Humanitarian Dispatch 119
The Newsroom Verifier 129
The Pharmacovigilance Monitor 139
The Curriculum Weaver 151
The Procurement Analyst 163
The Research Synthesizer 177
The Environmental Auditor 183
The Revenue C

## Chunk 1 | pages 5-6

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', pages 5-6, under 'Building What You Have Learned'. It should be retrieved for questions involving these local terms: retrieval, readings, system, one, capstone, project, ago, retrieve.

**Original chunk preview**

. . . 9
Bring-Your-Own-Project Guidance . . . . . . . . . . . . 9
Timeline and Deliverables . . . . . . . . . . . . . . . . . 10
Essential Readings . . . . . . . . . . . . . . . . . . . . . . 11
Oliver Twist’s List of Readings . . . . . . . . . . . . . . . 11
A Calibration Note . . . . . . . . . . . . . . . . . . . . . . 12
The map is not the territory.
Alfred Korzybski
The best retrieval system is the
one that knows what it does
not know—and has the
architecture to go find out.
Course maxim
A Gentle Re-Entry

[Page 6]
4 capstone project briefs
Hermann Ebbinghaus showed more
than a century ago that memory de-
cays exponentially without retrieval
practice. The forgetting curve is
not a metaphor; it is measured data.
The only reliable countermeasure
is spaced repetition —and a capstone
project is the most intense form of it.
You will retrieve every concept you
have learned, in context, und

## Chunk 2 | pages 6-6

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', page 6, under '4 capstone project briefs'. It should be retrieved for questions involving these local terms: guardrails, semantic, capstone, project, chunking, retrieval, structured, bridge.

**Original chunk preview**

entity–relation webs, request-side and response-
side guardrails, query transformation, semantic caching, the structured
bridge of Text-to-SQL, and—this final week—the discipline of evalua-
tion that binds it all together. Each week planted a seed. The capstone
project is the season in which those seeds bear fruit.
This document presents your capstone project options: twelve distinct
applications, each designed to integrate every pillar of the course. You
will design chunking strategies for real corpora, build cascaded retrieval
pipelines, enrich your knowledge layer with at least one advanced
technique (RAPTOR, GraphRAG, or derivative artifacts), implement
guardrails and response grounding, bridge structured and unstructured
data with Text-to-SQL, and evaluate everything with the rigor this
course demands.
Think of these twelve projects as your project of last resort: if you cannot
conc

## Chunk 3 | pages 6-7

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', pages 6-7, under '4 capstone project briefs'. It should be retrieved for questions involving these local terms: retrieval, every, metrics, build, recall, least, one, response.

**Original chunk preview**

rary token windows, but boundaries that a
domain expert would recognize
• Build a cascaded retrieval pipeline that moves from cheap, broad
recall (BM25, keyword) through dense semantic search to expensive,
precise re-ranking—and justify every stage

[Page 7]
building what you have learned 5
• Enrich your knowledge layer with at least one advanced technique:
RAPTOR hierarchical summaries, GraphRAG entity–relation extrac-
tion, or derivative artifacts that rewrite your corpus into multiple
complementary views
• Implement guardrails on both request and response sides—catching
adversarial or off-topic queries before they reach the retriever, and
grounding every response in retrieved evidence with auditable cita-
tions
• Bridge structured and unstructured data by integrating Text-to-SQL
or structured query interfaces alongside your document retrieval, so
the system can answer questions that l

## Chunk 4 | pages 7-8

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', pages 7-8, under '4 capstone project briefs'. It should be retrieved for questions involving these local terms: retrieval, project, must, chunking, capstone, demonstrate, corpus, embedding.

**Original chunk preview**

ve Pillars: Cross-Cutting Requirements
Every capstone project must exercise five interdependent pillars .
No project is complete unless it demonstrates mastery of each.
Pillar 1: Retrieval Architecture
A RAG system is only as good as its retrieval . Your project must
demonstrate a thoughtful, multi-stage retrieval pipeline:
• Chunking: Choose a strategy appropriate to your corpus. Fixed-size
token windows are the baseline; your capstone must go beyond
them. Consider semantic chunking (split at topic boundaries), re-
cursive chunking, or document-structure-aware chunking (sections,
headings, paragraphs). Justify your choice with evidence.
• Embedding model selection : Choose an embedding model and
defend it. Compare at least two (e.g., OpenAI text-embedding-3-large

[Page 8]
6 capstone project briefs
vs. an open-source model like bge-large or e5-mistral-7b). Report
embedding quality on yo

## Chunk 5 | pages 8-8

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', page 8, under '6 capstone project briefs'. It should be retrieved for questions involving these local terms: query, retrieval, demonstrate, nodes, summaries, answers, questions, corpus.

**Original chunk preview**

nodes are
chunks; parent nodes are summaries of clusters. Demonstrate that
RAPTOR retrieval answers “big picture” questions that chunk-level
retrieval misses.
GraphRAG Extract entities and relationships from your corpus and
build a knowledge graph. Show that graph-based retrieval answers
multi-hop questions (“which suppliers share a common risk factor?”)
that vector search alone cannot.
Derivative Artifacts Rewrite your corpus into complementary views:
executive summaries, glossaries, FAQ pairs, comparison tables, or
domain-specific indices. Show that querying these artifacts improves
answer quality for specific question types.
You may implement more than one. Projects that demonstrate two
or more enrichment techniques, with measured comparison, will be
recognized.
Pillar 3: Query & Response Intelligence
The space between the user ’s question and the system ’s answer is
where intelligenc

## Chunk 6 | pages 8-9

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', pages 8-9, under '6 capstone project briefs'. It should be retrieved for questions involving these local terms: query, report, project, must, transformation, document, semantic, queries.

**Original chunk preview**

our project must demonstrate:
• Query transformation : At least one technique—query rewriting,
HyDE (hypothetical document embeddings), query decomposition,
or step-back prompting. Report the retrieval improvement from
transformation vs. raw query.

[Page 9]
building what you have learned 7
Semantic caching is an optional
but encouraged addition. If your
domain has repetitive queries (e.g.,
compliance questions, maintenance
lookups), implement a semantic
cache and report the hit rate and la-
tency savings.
• Request-side guardrails: Detect and handle off-topic, adversarial, or
nonsensical queries before they reach the retriever.
• Response grounding: Every claim in the system’s response must be
traceable to a retrieved chunk. Implement citation generation and
faithfulness checking. Report the percentage of responses that are
fully grounded.
• Response-side guardrails: Detect and suppress

## Chunk 7 | pages 9-9

**Context**

This chunk is from 'Capstone Project Briefs Enterprise RAG: Building What You Have Learned — Seventeen Capstone Journeys Asif Qamar', page 9, under '6 capstone project briefs'. It should be retrieved for questions involving these local terms: structured, retrieval, report, metrics, generated, pillar, project, data.

**Original chunk preview**

riate content in the generated re-
sponse.
Pillar 4: The Structured Bridge
Not all knowledge lives in prose . Every project has structured data
alongside its document corpus—databases, spreadsheets, APIs with
tabular responses, or metadata catalogs. Your project must:
• Identify the structured data in your domain (e.g., patient databases,
patent metadata, financial transaction logs, sensor readings).
• Implement a Text-to-SQL or structured query interface that translates
natural language questions into database queries.
• Demonstrate the router: given a user question, does the system route
to document retrieval, structured query, or both? Report routing
accuracy on a test set.
• Show at least one question that requires both structured and unstruc-
tured retrieval to answer correctly.
Pillar 5: Evaluation as Discipline
Evaluation is not a post-hoc checklist. It is embedded in the design.
