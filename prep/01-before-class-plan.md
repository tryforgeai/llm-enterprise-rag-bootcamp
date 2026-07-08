# Before Class Plan

## Goal

Do not try to master RAG before class. Build a small working mental and code model so that every lecture connects to an agent capability for Avaloka AI.

## Seven-Day Preparation

### Day 1: Environment

- Confirm Python is installed.
- Confirm Jupyter or VS Code notebooks work.
- Confirm Git works.
- Confirm OpenAI API access works.
- Create a tiny notebook that calls one LLM endpoint.

### Day 2: Embeddings

- Learn what an embedding is.
- Run one embedding call.
- Compare two text snippets by cosine similarity.
- Write down what surprised me.

### Day 3: Vector Store

- Pick one local vector store: Chroma or Qdrant.
- Store 10 text chunks.
- Retrieve top 3 chunks for a query.

### Day 4: Minimal Agentic RAG

Build:

```text
question
-> embed query
-> retrieve top chunks
-> classify intent and risk
-> choose next step
-> send chunks + question to LLM
-> answer
-> save trace
```

### Day 5: Avaloka Docs Mini Knowledge Base

- Use a few Avaloka docs as source material.
- Chunk them.
- Embed them.
- Ask questions about Avaloka design, safety, and memory.

### Day 6: Simple Eval

Create 10 test questions:

- 5 factual retrieval questions
- 3 safety/guardrail questions
- 2 memory or product design questions

Record whether retrieval found the right evidence and whether the agent chose the right behavior.

### Day 7: Questions For Class

Prepare instructor questions around:

- chunking strategy
- embedding model choice
- multimodal retrieval
- GraphRAG
- RAG eval
- agent trace design
- answer / ask / refuse / escalate policies
- hallucination control
- privacy and memory

## Success Criteria Before Class

I can explain and run this loop:

```text
intent -> retrieve -> decide -> respond -> trace -> evaluate
```
