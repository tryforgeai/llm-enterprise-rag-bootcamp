# RAG for Newcomers: An Introduction

> A note before you start: you don't need any AI/ML background to read this. We'll build intuition first with everyday analogies, then walk through everything Week 1 of the course covers, station by station. By the end you'll have a map — not full technical mastery, but a clear sense of what each piece is for and where it fits.
>
> This version expands on an earlier draft — it now covers every topic from Week 1's materials (not just the headline ideas), and closes with a reading list linking to the actual papers behind the named techniques.

## RAG in one sentence

RAG stands for **Retrieval-Augmented Generation**.

The simplest way to picture it: **before the AI answers your question, hand it a book it can flip through — don't just make it answer from memory.**

A plain language model (the kind you chat with normally) answers using only what got baked into its parameters during training — like a well-read person who hasn't picked up a new book in a while, answering purely from memory. That creates two problems:

- It has no idea about your company's internal documents, what happened yesterday, or anything that appeared after its training cutoff.
- It sometimes misremembers, or — more dangerous — confidently makes something up that merely *sounds* plausible ("hallucination").

RAG's fix is unglamorous but effective: **before the model answers, go search a designated set of documents for anything relevant, hand that material to the model along with the question, and have it answer grounded in that evidence** — instead of guessing from memory alone.

```
User asks a question
  → search a document store for relevant passages
  → give the question + those passages to the model
  → the model generates an answer grounded in those passages
```

In short: **training a model = changing what's stored in its parameters. RAG = handing it extra reference material at answer time.**

One caveat worth internalizing early: RAG isn't a guarantee of correctness. The system can still retrieve the wrong passages, miss key evidence, or generate a claim the retrieved context doesn't actually support — these failure modes are exactly what the rest of the course is built to address, one pipeline stage at a time.

## Why RAG survives even as context windows keep growing

Models today can swallow hundreds of thousands — even millions — of words in one go. So why bother "searching first, then answering"?

The course frames the answer this way:

> The context window is not a filing cabinet — it's a desk. You still need a library.

Unpacked:

- The **context window** is just the model's current working surface — a small area holding whatever it's processing right now.
- The real **knowledge base / document store** is the library — vast, constantly updated, with mixed permissions and freshness.
- A bigger desk doesn't walk itself to the library and pick out the most relevant, current, authorized, and trustworthy volumes on your behalf.
- **RAG is that job** — the librarian standing between the library and the desk, searching, filtering, and delivering the evidence that actually matters.

So no matter how large the window gets, *deciding what the model should see* still needs a dedicated mechanism. That's RAG's reason for existing, and it's what this course systematically teaches.

## RAG vs. fine-tuning

A natural question: "why not just train the company's knowledge directly into the model?" — that's fine-tuning. RAG and fine-tuning aren't competitors; they solve different problems:

| Situation | RAG fits better | Fine-tuning fits better |
|---|---|---|
| Information changes often (prices, policy, live data) | ✅ just update the document store | Costly — needs retraining every time |
| Need to show *where* an answer came from | ✅ naturally traceable to a source | Knowledge is "baked in" — provenance is murky |
| Private or sensitive documents | ✅ retrieved on demand, permissions stay controllable | Data seen during training is harder to delete/scope |
| Changing *how* the model talks or behaves | Limited ability | ✅ better suited |

One-line summary: **RAG governs what the model knows; fine-tuning is better at governing how it talks and acts.** In practice, teams often combine both.

## How the course is structured: one pipeline, seven stages

The course doesn't teach RAG as a grab-bag of disconnected tricks ("use a vector database," "pick an embedding model"). It treats RAG as one **end-to-end pipeline**:

```
raw documents → ingestion → retrieval → augmentation → scalable architecture → security & trust → evaluation → measurable, trustworthy answers
```

Below is every topic Week 1 introduced, translated into plain language, organized by pipeline stage.

### 1. Foundations — how a machine "understands" text

A model doesn't literally read and comprehend text the way a person does. It converts text into a string of numbers (an **embedding**), and that number-string's *position* in an abstract space roughly stands in for what the text means — things with similar meaning end up positioned near each other. Nearly everything downstream (retrieval, reranking, caching, clustering) is built on top of this one layer, so the course spends real time on the idea before moving on: *"if we misread the geometry, everything built on top of it becomes a guess."*

### 2. Ingestion — Chunking, the first cut

A long document can't be handed whole to a retrieval system — it first gets sliced into small pieces (**chunks**). This step matters enormously; the course calls it **"the first irreversible cut"**: if the way you slice loses context that should have been kept, no amount of clever reranking or a stronger model downstream can recover it. As long as the *original* document is preserved, you can always re-chunk — but the live index can only ever be as good as the cut it was built from.

### 3. Retrieval — finding the right handful of passages

Retrieval needs to match both the user's literal wording (names, IDs, exact terms — **sparse retrieval**, e.g. BM25/SPLADE) and what the user actually *means*, even in different words (**dense/semantic retrieval**, via embeddings). Neither channel alone is reliable — the course frames it as a "traffic court to supreme court" escalation ladder: cheap, broad retrieval handles most queries; a slower, more expensive cross-encoder reranker is reserved for the hardest, highest-stakes cases.

This stage also covers **Query Transformation** — a translation layer that turns a user's vague or conversational question into something the retrieval system can actually work with: fixing typos, expanding abbreviations, splitting multi-part questions, generating multiple query variants, or even a technique called **HyDE** (generate a hypothetical answer first, embed *that*, then retrieve real documents similar to the hypothetical). Transformation must preserve the user's actual intent — a fluent rewrite that quietly changes the meaning of the question can retrieve confident-looking but irrelevant evidence.

### 4. Augmentation — improving the quality of what gets retrieved

Rather than indexing only raw text, this stage generates additional "views" of the same source material — atomic facts, question-answer pairs, summaries, search-friendly rewrites (the course calls these **derivative artifacts**, "a prism" splitting one document into many retrievable shapes) — so different phrasings of a question have more chances to find a match.

Two named techniques go further:

- **RAPTOR** (Recursive Abstractive Processing for Tree-Organized Retrieval) — like a **zoom lens**. It recursively clusters and summarizes chunks into a multi-level tree, so a narrow question can pull a precise leaf-level chunk while a broad question pulls a high-level summary.
- **GraphRAG** — like a **telescope**. It extracts entities and relationships into a knowledge graph, so questions about relationships, communities, or corpus-wide themes can be answered by reasoning over structure, not just similarity to one matching passage.

RAPTOR and GraphRAG solve different problems — resolution (RAPTOR) vs. relational/corpus-wide structure (GraphRAG) — and are meant to complement each other, not replace one another.

### 5. Scalable Architecture — right-sizing complexity

The course's core principle: **architecture should be earned by evidence, not assumed in advance.** Start with the simplest system that works, observe where it actually fails using traces and evals, then add exactly the component that fixes that specific failure — verified with something like a Shapley-style ablation test (measure baseline → add component → rerun → compare cost and quality). The instructor ties this to Galileo's square-cube law: a design that works at one scale can fail at another, because costs and constraints don't grow at the same rate.

This stage also covers **Semantic Cache** — reusing previous retrieval or generation results when a new query is semantically close enough to a past one, even with different wording. The course calls it "playing with fire": done carelessly, it can silently serve a stale, wrong, or cross-user-leaked answer. A mature system might serve ~90% of queries from cache — which means cache correctness, invalidation, and monitoring become first-class architecture concerns, not an afterthought.

### 6. Security & Trust — keeping the system honest

Two complementary layers:

- **Request Guardrails** — the gatekeeper *before* the model ever sees a request. The course's target is a sixteen-gate input pipeline built around the **HHH** principle: Helpful, Harmless, Honest. Guardrails reject dangerous requests early, block prompt injection before it reaches tools or private data, and enforce identity/permission/tenant boundaries — all *before* retrieval or generation happens, because a decision made after the fact can't undo data that was already improperly accessed.
- **Response Grounding** — checking *after* generation whether each factual claim in the answer is actually supported by the retrieved evidence, rather than trusting the generator to police itself. The course's target design is an **assertion-evidence graph**: every claim in an answer is a node that must point to supporting evidence, or it isn't allowed to leave the system. This lets the system revise or reject individual sentences instead of accepting or rejecting an entire answer as one block.

### 7. Proof & Frontier — evaluation and structured-data access

**Evaluation** has to measure retrieval and generation *separately* — a good final answer doesn't tell you whether retrieval worked, and good retrieval doesn't guarantee the answer stayed grounded in it. Retrieval quality uses ranking metrics (**MRR, MAP, NDCG**); answer/pipeline quality uses frameworks like **RAGAS** (automated scoring across context relevance, faithfulness, answer relevance) and **FActScore** (breaking an answer into atomic facts and checking how many are actually supported by a reliable source).

**Text-to-SQL** extends evidence access from unstructured documents to structured databases — turning a natural-language question into a validated, permission-checked, read-only SQL query, executed in a constrained environment, with the final answer generated from the returned rows. It belongs in this "frontier" bucket because it needs the same retrieval discipline (finding the right schema and business definitions first) plus a stricter layer of guardrails, since a bad query can do real damage.

## The hands-on experiments from Week 1

Two small coding exercises anchored the concepts:

- **Text semantic search with SentenceTransformers** — embed a small corpus of sentences, embed a query, and retrieve the top-k most similar sentences by vector similarity. This is the minimal working skeleton of the whole retrieval idea.
- **Image search with CLIP** — using a model (`clip-ViT-B-32`) that places text and images in the *same* embedding space, so a text query can retrieve semantically related images.

Both are small enough to run in an afternoon, and both make the "meaning becomes geometry" idea concrete rather than abstract.

## Mindset tips for someone just starting

- **You don't need to understand every term on day one.** Words like embedding, chunk, and reranker will feel unfamiliar at first — that's normal. Follow the pipeline order and each stage will properly introduce the concepts the next one depends on.
- **Hold onto the analogies more than the jargon.** This course itself leans hard on them — desk vs. library, the translator, microscope vs. zoom lens vs. telescope. Build the intuition first; the vocabulary will attach itself naturally afterward.
- **RAG is not a "bolt it on and you're done" black box.** It's closer to an ongoing engineering discipline that needs continuous tuning and verification — which is exactly why the course spends so much time on *how to evaluate* and *how to decide whether a component earned its place*, rather than just "how to stand up a demo."

If something in here catches your interest, feel free to jump straight to that section's course notes rather than reading everything in order — and ask questions any time.

## Further reading: the papers behind Week 1's named techniques

Only one paper is explicitly cited by title and link in the Week 1 course notes — **SAGE**. Everything else below is the original/canonical paper behind a technique or tool Week 1 *named and used*, added here because you asked for pointers to dig deeper — not because Week 1's notes cited them directly. Treat the SAGE link as primary-source-confirmed, and the rest as "the paper this name refers to."

**Explicitly cited in Week 1 notes:**

- Zhang, J., Li, G., & Su, J. (2025). *SAGE: A Framework of Precise Retrieval for RAG*. [arXiv:2503.01713](https://arxiv.org/abs/2503.01713) — dynamic, relevance-drop-aware chunk selection plus LLM feedback on context sufficiency; referenced when comparing against RAPTOR/GraphRAG.

**Canonical papers behind techniques named in Week 1 (not directly linked in the notes, added for reference):**

- Sarthi, P. et al. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval*. [arXiv:2401.18059](https://arxiv.org/abs/2401.18059)
- Edge, D. et al. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization*. [arXiv:2404.16130](https://arxiv.org/abs/2404.16130)
- Gao, L., Ma, X., Lin, J., & Callan, J. (2022). *Precise Zero-Shot Dense Retrieval without Relevance Labels* (HyDE). [arXiv:2212.10496](https://arxiv.org/abs/2212.10496)
- Es, S., James, J., Espinosa-Anke, L., & Schockaert, S. (2023). *RAGAS: Automated Evaluation of Retrieval Augmented Generation*. [arXiv:2309.15217](https://arxiv.org/abs/2309.15217)
- Min, S. et al. (2023). *FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation*. [arXiv:2305.14251](https://arxiv.org/abs/2305.14251)
- Formal, T., Piwowarski, B., & Clinchant, S. (2021). *SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking*. [arXiv:2107.05720](https://arxiv.org/abs/2107.05720)
- Reimers, N., & Gurevych, I. (2019). *Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks*. [arXiv:1908.10084](https://arxiv.org/abs/1908.10084) — the model family behind the SentenceTransformers exercise.
- Radford, A. et al. (2021). *Learning Transferable Visual Models From Natural Language Supervision* (CLIP). [arXiv:2103.00020](https://arxiv.org/abs/2103.00020) — the model behind the image-search exercise.
- Robertson, S., & Zaragoza, H. (2009). *The Probabilistic Relevance Framework: BM25 and Beyond*. (No arXiv version; classic IR reference — foundational to the sparse-retrieval side of the pipeline.)

**Background reading (not a paper, but named directly in Week 1's afternoon session on Transformer internals):**

- Alammar, J. *The Illustrated Transformer*. <https://jalammar.github.io/illustrated-transformer/> — the visual walkthrough Week 1 pointed to before covering attention, residual streams, and the Transformer block. The underlying paper it illustrates is Vaswani, A. et al. (2017), *Attention Is All You Need*, [arXiv:1706.03762](https://arxiv.org/abs/1706.03762).

*A couple of things Week 1's own notes flagged as still-unresolved and worth confirming with the instructor rather than assuming: the exact five failure modes of semantic caching, the precise sixteen request-guardrail gates, and the three-tier grounding-verification hierarchy — the notes intentionally left these as open questions rather than inventing specifics.*
