# Three-Minute Video Script

## Trustworthy Enterprise RAG and AI Agent Architecture

Target length: approximately three minutes  
Speaker: Rosso Han

## 0:00-0:25 | Why The Demo Is Not The Product

> Point to the title, then the complete diagram.

Enterprise RAG demos are easy to make impressive. Upload documents, retrieve similar
passages, and ask a language model for a polished answer. But a production system must
answer harder questions: Who is the user? Which sources are
authoritative? What information are they allowed to access? Should the system answer,
ask, abstain, refuse, escalate, or take an action?

That is why I treat RAG as the evidence layer inside a larger agent system.

## 0:25-1:00 | Identity, Authorization, And Scope

> Move from “Intent + Identity” into the first two control-plane steps.

The flow starts with intent and identity, not with vector search. The system first
understands the request, the user's role, tenant, business context, and potential risk.

Then it authorizes the request and defines the permitted knowledge scope. This must happen
before private retrieval. Asking a model not to mention restricted information after it
has already seen it is not an access-control boundary.

Security context is part of the query, and it must also be part of cache identity,
tracing, and evaluation.

## 1:00-1:35 | Documents And Permitted Retrieval

> Point to the Document Pipeline, then Permitted Retrieval.

The document pipeline must preserve meaning, not just extract text. Headings, tables,
metadata, versions, provenance, and deletion status can all change
the interpretation of a passage.

Retrieval then searches only permitted evidence. Depending on measured needs, that may
combine sparse and dense retrieval, metadata filters, freshness and authority signals,
reranking, and explicit no-match behavior.

The goal is not to find text that sounds related. It is to find evidence that is current,
allowed, and fit for the decision.

## 1:35-2:10 | Decide, Generate, And Verify

> Follow the control plane from Retrieve through Verify + Guard.

After retrieval, the agent chooses a bounded next step. It may answer, ask a clarifying
question, search another approved source, call a tool, abstain, refuse, or escalate to a
human.

If it generates a response, verification is a separate stage. Important claims should be
checked for evidence support, contradictions, freshness, safety, and uncertainty.
Unsupported certainty can trigger repair, another retrieval step, a question, or a safe
fallback.

This decision layer is what turns a retrieve-and-generate pipeline into an agent system.

## 2:10-2:40 | Trace, Evaluate, And Improve

> Sweep across the full-width Observability & Improvement layer.

Every stage should leave a useful trace: classification, authorization scope, evidence,
decision reason, model and prompt version, latency, cost, verification, and final action.

Evaluation should measure retrieval, grounding, agent decisions, safety, privacy, and
operations separately. When something fails, the team can identify whether the problem
came from ingestion, retrieval, ranking, policy, generation, or verification.

Measured failures should choose the next architecture component.

## 2:40-3:00 | Closing

> Return to the complete diagram and pause briefly.

The goal is not to build the most complicated RAG diagram. The goal is to build an AI
system whose behavior the organization can understand, measure, govern, and trust.

That is the engineering gap between an impressive enterprise AI demo and a dependable
enterprise AI product.

## Recording Notes

- Record in landscape 16:9 at 1080p or higher.
- Keep the architecture diagram full-screen and use a pointer or subtle zoom.
- Speak at approximately 135 to 145 words per minute.
- Pause briefly after “Security context is part of the query” and before the final
  sentence.
- Add captions because many LinkedIn viewers watch without sound.
