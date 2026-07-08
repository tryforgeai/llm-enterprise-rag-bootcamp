# Curriculum Weaver Lite Project Proposal

Date: 2026-06-27  
Status: Presentation draft  
Project type: LLM / RAG course project  

## 1. Project Title

**Curriculum Weaver Lite: A Pedagogy-First RAG Tutor for Learning Self-Attention**

## 2. One-Sentence Summary

Curriculum Weaver Lite helps a student learn a technical concept by modeling what they already know, identifying missing prerequisites, retrieving source-grounded learning material, generating a coherent learning path, and updating the learner model through quiz feedback.

## 3. Motivation

Most RAG education demos start from the content:

```text
documents -> chunks -> embeddings -> retrieval -> answer
```

That is useful, but it misses the central problem of teaching. A student does not simply need the most semantically similar chunk. The student needs the next concept they are ready to understand.

Curriculum Weaver Lite starts from pedagogy:

```text
student goal
-> learner model
-> prerequisite graph
-> diagnostic check
-> learning path
-> source-grounded lesson
-> quiz
-> learner model update
```

RAG is still important, but it is used as supporting infrastructure after the system understands the learner's goal and prerequisite gaps.

## 4. Research Inspiration

This project is inspired by recent work combining personalized tutoring, knowledge tracing, and RAG. For example, TutorLLM proposes combining Knowledge Tracing and Retrieval-Augmented Generation to personalize learning recommendations based on a student's learning state. The paper reports improved user satisfaction and quiz performance compared with general LLM use alone.

Curriculum Weaver Lite adapts that direction into a course-project-sized prototype focused on one topic: learning self-attention.

## 5. Core Hypothesis

The core hypothesis is:

> A prerequisite-aware learner model can produce a more useful learning path than similarity-based retrieval alone.

The project tests whether a system can:

- infer what the student already understands
- identify missing prerequisites
- order concepts pedagogically
- retrieve or attach source-grounded material at the right depth
- generate a lesson and quiz
- update mastery estimates after quiz interaction

## 6. First Learning Domain

The first domain is **self-attention** because it is central to modern LLMs and naturally connects to course topics:

- vectors
- dot product
- matrix multiplication
- softmax
- Query / Key / Value
- scaled dot-product attention
- self-attention
- multi-head attention
- transformer blocks

The first demo query is:

> I want to understand self-attention mathematically, with a small code example.

## 7. Target User

The target user is an AI engineering student in an LLM/RAG bootcamp.

The instructor reviewer is also an important audience. The project should make it easy for an instructor to inspect:

- what the learner is assumed to know
- why each learning step appears
- which sources support each lesson
- how quiz feedback changes the learner model
- where RAG, memory, evaluation, and agent logic fit

## 8. Product Experience

The project experience has five visible panels:

1. **Student Model**
   - choose learner profile
   - enter goal
   - show known and weak concepts

2. **Diagnostic**
   - estimate mastery over relevant prerequisites
   - show strong, developing, and weak areas

3. **Learning Path**
   - generate ordered prerequisite-aware path
   - skip concepts already mastered
   - include concepts below mastery threshold

4. **Lesson Studio**
   - explain why the concept comes next
   - show teaching explanation
   - show source cards
   - include code sketch
   - ask quiz question

5. **Agent Trace**
   - show parsed goal
   - show mastery threshold
   - show skipped concepts
   - show path rule
   - show retrieval mode

## 9. System Architecture

The final project architecture has these modules:

```text
Course Materials
-> Content Ingestion
-> Source Cards
-> Concept Graph
-> Learner Model / Memory
-> Diagnostic Agent
-> Retriever
-> Curriculum Planner
-> Lesson Synthesizer
-> Quiz Generator
-> Evaluator
-> Trace Dashboard
```

### Module 1: Content Ingestion

Ingest course materials such as:

- lecture notes
- papers
- textbook excerpts
- code notebooks
- tutorials

The ingestion pipeline should produce teaching units rather than arbitrary token chunks.

Possible teaching unit types:

- definition
- intuition
- derivation
- worked example
- code example
- quiz item

Each source card should contain:

- concept ID
- source name
- citation
- summary
- depth level
- source type
- supported learning objective

### Module 2: Concept Graph

The concept graph stores prerequisite relationships.

Example:

```text
vectors
-> dot product
-> matrix multiplication
-> softmax
-> Query / Key / Value
-> scaled dot-product attention
-> self-attention
-> multi-head attention
```

The concept graph is the main difference between Curriculum Weaver and ordinary RAG. It lets the system retrieve what is teachable next, not merely what is similar.

### Module 3: Learner Model / Memory

The learner model stores the student's current estimated mastery.

Example:

```json
{
  "dot_product": 0.82,
  "softmax": 0.46,
  "qkv": 0.32,
  "scaled_dot_product_attention": 0.12
}
```

Step 2 can begin with simple mastery scores. Later versions can experiment with Knowledge Tracing methods.

### Module 4: Diagnostic Agent

The diagnostic agent estimates what the student knows from:

- selected profile
- stated background
- diagnostic answers
- previous quiz history

It outputs:

- known concepts
- weak concepts
- missing prerequisites
- recommended starting point

### Module 5: Retriever

The retriever finds source cards for the next teachable concept.

It should use:

- BM25 for exact concept names
- embeddings for semantic matches
- metadata filters for concept, depth, source type, and format
- reranking for source quality and pedagogical fit

Retrieval should be constrained by the planner. The system should not retrieve advanced attention papers for a learner who has not yet understood softmax.

### Module 6: Curriculum Planner

The planner creates the learning path.

Inputs:

- target concept
- learner model
- concept graph
- mastery threshold
- available source cards

Outputs:

- ordered concept path
- skipped concepts
- included prerequisites
- lesson objectives
- reason for each step

Basic algorithm:

```text
1. Map goal to target concept.
2. Traverse prerequisite graph.
3. Remove mastered concepts.
4. Topologically order missing concepts.
5. Attach source cards by concept and depth.
6. Generate path trace.
```

### Module 7: Lesson Synthesizer

The lesson synthesizer uses an LLM to generate a lesson from retrieved source cards.

It must:

- cite sources
- match learner depth
- explain why the concept matters
- connect the concept to prerequisites
- include a small code or math example when appropriate
- avoid unsupported equations or invented citations

### Module 8: Quiz Generator

The quiz generator creates short checks after each lesson.

Quiz types:

- concept check
- short-answer explanation
- code reading
- equation interpretation

The quiz result updates the learner model.

### Module 9: Evaluator

The evaluator measures both RAG quality and teaching quality.

Retrieval metrics:

- Recall@k
- MRR
- NDCG

Pedagogy metrics:

- prerequisite correctness
- path coherence
- depth match
- lesson clarity

Grounding metrics:

- citation accuracy
- no hallucinated sources
- equation support

Learning metrics:

- quiz improvement
- mastery update accuracy
- student satisfaction

### Module 10: Trace Dashboard

The trace dashboard makes the agent behavior inspectable.

Trace fields:

- parsed goal
- target concept
- learner profile
- mastery estimates
- missing prerequisites
- retrieved source cards
- skipped concepts
- generated path
- quiz result
- updated mastery

## 10. Implementation Plan

### Step 1: UI Demo

Goal:

Show the learning experience before building the full intelligence.

Implemented scope:

- static UI
- static concept graph
- static source cards
- three learner profiles
- diagnostic display
- prerequisite-aware path
- lesson cards
- quiz interaction
- learner mastery update
- trace panel

Success criteria:

- the app opens locally
- user can complete the full flow
- desktop and mobile layouts work
- instructor can understand the pedagogy-first idea quickly

### Step 2: Real RAG + Memory + Evaluation

Goal:

Replace static demo data with real AI modules.

Planned scope:

1. Content ingestion from notes, papers, and tutorials.
2. Source card generation.
3. Concept graph storage.
4. Learner memory and mastery scores.
5. Diagnostic agent.
6. Hybrid retriever.
7. LLM lesson synthesizer.
8. Quiz generator and grader.
9. Evaluation dashboard.
10. UI tests and smoke tests.

### Step 3: Advanced Research Extensions

Possible extensions:

- Knowledge Tracing model
- RAPTOR summaries at multiple depths
- graph-based concept retrieval
- multi-agent tutoring roles
- teacher review dashboard
- multimodal source ingestion from lecture videos

These should only be added after Step 2 works.

## 11. Evaluation Plan

The project will compare Curriculum Weaver against a simple baseline.

Baseline:

> Ask a general LLM: "Teach me self-attention."

Curriculum Weaver:

> Use learner profile, prerequisite graph, source cards, path planner, lesson synthesis, quiz, and mastery update.

Evaluation questions:

- Does the path include necessary prerequisites?
- Does it skip concepts the learner already knows?
- Is the explanation at the right depth?
- Are sources visible and relevant?
- Does the quiz test the lesson objective?
- Does the trace explain the system's decision?

## 12. Deliverables

Final deliverables:

1. Working web demo.
2. Concept graph for self-attention.
3. Source card dataset.
4. Learner profiles.
5. RAG retriever.
6. Learner memory model.
7. LLM lesson synthesizer.
8. Quiz generator and evaluator.
9. Trace dashboard.
10. Test suite.
11. Final presentation and report.

## 13. Timeline

### Phase 1: UI Demo

Duration: 2-3 days

- build static UI
- create concept graph
- create source cards
- implement learning path flow
- add quiz and trace
- run smoke tests

### Phase 2: AI Modules

Duration: 1-2 weeks

- implement ingestion
- create retriever
- add learner memory
- add LLM lesson synthesis
- add quiz grading
- add evaluation dashboard
- add tests

### Phase 3: Presentation Polish

Duration: 2-3 days

- prepare demo script
- prepare slides
- compare baseline vs Curriculum Weaver
- document limitations and next steps

## 14. Risks And Mitigations

| Risk | Mitigation |
|---|---|
| Project becomes a generic chatbot | Keep prerequisite graph and learner model central |
| Too much time spent on infrastructure | Step 1 proves UI first; Step 2 adds modules incrementally |
| RAG retrieves irrelevant but similar chunks | Use concept and depth metadata filters |
| LLM invents citations | Require source cards and citation checks |
| Learning quality is hard to measure | Use quiz, path coherence, depth match, and source attribution metrics |
| Scope expands to entire ML curriculum | Keep first domain limited to self-attention |

## 15. Why This Is A Good Course Project

This project exercises the course topics without becoming a generic RAG demo.

It uses:

- LLMs for lesson synthesis and diagnostic interpretation
- RAG for source-grounded learning material
- memory for learner state
- agents for diagnosis, planning, retrieval, synthesis, and evaluation
- evaluation for both retrieval quality and learning quality
- UI testing for the complete learning flow

The key insight is:

> Educational RAG should retrieve the next teachable concept, not just the nearest chunk.

## 16. Presentation Outline

1. Problem: students have materials but no personalized learning path.
2. Why ordinary RAG is insufficient.
3. Pedagogy-first hypothesis.
4. Demo: self-attention learner flow.
5. Architecture: concept graph, learner memory, RAG, planner, synthesizer, evaluator.
6. Evaluation plan.
7. Current status.
8. Final deliverables.
9. Risks and next steps.

