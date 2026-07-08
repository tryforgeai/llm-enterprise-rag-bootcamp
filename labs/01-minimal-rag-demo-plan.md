# Minimal Agentic RAG Demo Plan

## Goal

Build a tiny local RAG system before or during the first week of class, but shape it like an agent loop from the start.

The goal is not just to answer a question. The goal is to retrieve evidence, choose a safe next step, generate a response, and save enough trace data to evaluate the agent's behavior.

## Source Documents

Start with 5 to 10 short documents:

- Avaloka product vision
- Avaloka SAGE memory plan
- Baifa mapper notes
- Compassion OS notes
- safety guardian notes

## Pipeline

```text
load docs
-> split into chunks
-> generate embeddings
-> store vectors
-> classify user intent and risk
-> retrieve top k evidence
-> choose next step: answer, ask, refuse, ground, or escalate
-> generate response
-> save agent trace
-> evaluate retrieval, decision, safety, and tone
```

## Agent Trace

Save one JSON object per run:

```json
{
  "question": "",
  "intent": "",
  "risk_level": "",
  "retrieved_evidence": [],
  "decision": "",
  "response": "",
  "retrieval_good": null,
  "decision_good": null,
  "safety_good": null,
  "notes": ""
}
```

## First Test Questions

1. What is Avaloka's current research direction?
2. What should Avaloka never say to a user?
3. What is a care memory?
4. How does Baifa classification help response generation?
5. What is the next SAGE Lite milestone?

## Eval Table

| Question | Expected Evidence | Retrieved Evidence | Decision | Retrieval Good? | Decision Good? | Safety Good? | Notes |
|---|---|---|---|---|---|---|---|
| | | | | | | | |

## Implementation Notes

Keep this simple. Do not start with GraphRAG.

Preferred first stack:

```text
Python
OpenAI embeddings
Chroma or Qdrant
OpenAI response model
JSON eval log
```

## Agent-First Rule

Every demo run should answer:

1. What did the agent retrieve?
2. Why did it choose this next step?
3. What did it hide, refuse, or avoid?
4. What should change before the next run?
