# Reusable Method Catalog

This catalog is a selection guide, not a claim that every method is production
ready. Maturity labels mean:

- `concept`: explained in course material
- `demo`: represented by runnable or inspectable teaching code
- `integrated`: used in a multi-stage lab pipeline
- `validated`: compared with explicit project-level eval evidence

No method in this catalog should be treated as validated for a new domain until
it passes that domain's own held-out evaluation.

## Foundations

### F01 — Tokenization and normalization

- Problem: raw text cannot be compared, chunked, or modeled consistently.
- Method: normalize intentionally, tokenize, inspect token IDs and coverage.
- Use when: onboarding a language/domain or diagnosing broken chunk boundaries.
- Measure: token count, unknown/fragmentation rate, retrieval changes by language.
- Failure signal: names, code, Tibetan, or domain terms split beyond usefulness.
- Evidence: `resources/notebook-methods-kb.md`, `course/week_02/week-02.zh.md`.
- Maturity: `demo`.

### F02 — Softmax and temperature

- Problem: raw scores need a distribution; generation needs controllable
  exploration.
- Method: subtract the maximum for stability, divide logits by temperature,
  exponentiate, and normalize.
- Use when: explaining attention, sampling, or contrastive objectives.
- Measure: entropy, calibration, factuality, answer variance.
- Failure signal: treating decoding temperature as factual confidence.
- Evidence: `resources/notebook-methods-kb.md`, `course/week_02/week-02.zh.md`.
- Maturity: `demo`.

### F03 — Dense embeddings and similarity diagnostics

- Problem: lexical overlap misses semantic equivalence.
- Method: encode query and candidates; rank with cosine or normalized dot
  product; inspect random-pair and intra/inter-class score distributions.
- Use when: semantic matching is expected and a lexical baseline is insufficient.
- Measure: Recall@K, nDCG@K, intra/inter similarity gap.
- Failure signal: all vectors appear similarly close, or punctuation/domain
  changes dominate semantics.
- Evidence: `course/week_03/punctuation_embedding_test.py`,
  `resources/notebook-methods-kb.md`.
- Maturity: `demo`.

### F04 — Contrastive embedding fine-tuning

- Problem: general embeddings do not separate domain-relevant positives from
  hard negatives.
- Method: train paired or multi-negative examples with CoSENT, InfoNCE, or
  supervised contrastive objectives.
- Use when: a labeled set proves a stable domain-specific retrieval gap.
- Measure: held-out Recall/nDCG, cosine gap, robustness to hard negatives.
- Failure signal: gains exist only on synthetic or randomly split near-duplicates.
- Evidence: `resources/notebook-methods-kb.md`.
- Maturity: `demo`.

## Representation and chunking

### R01 — Fixed overlapping chunks

- Problem: documents exceed model and embedding limits.
- Method: split into deterministic windows and repeat a controlled overlap.
- Use when: establishing the first transparent text baseline.
- Measure: boundary-error rate, Recall@K, duplicated-token cost.
- Failure signal: answers require context outside the window or retrieval returns
  repeated neighboring chunks.
- Evidence: `course/week_03/contextual_chunk_pdf.py`,
  `course/week_03/path2_text_chunk_qa.py`.
- Maturity: `demo`.

### R02 — Structure-aware and hybrid chunking

- Problem: fixed windows destroy headings, lists, tables, or document hierarchy.
- Method: parse document structure first, then enforce token limits without
  discarding section metadata.
- Use when: source documents have reliable structural cues.
- Measure: heading retention, table integrity, Recall/nDCG by question type.
- Failure signal: parser errors or structure metadata costs more than it helps.
- Evidence: `course/week_04/chunking_pipeline/README.md`,
  `labs/beyond_rag_week_6_lab_1/sv_rag_pipeline/README.md`.
- Maturity: `integrated`.

### R03 — Semantic chunking

- Problem: fixed sizes split coherent ideas or combine unrelated ideas.
- Method: place boundaries where embedding or semantic similarity changes.
- Use when: prose topics change at irregular intervals.
- Measure: within-chunk coherence, chunk-size distribution, retrieval metrics.
- Failure signal: unstable thresholds create tiny fragments or oversized chunks.
- Evidence: `course/week_04/chunking_pipeline/`,
  `labs/beyond_rag_week_6_lab_1/sv_rag_pipeline/`.
- Maturity: `integrated`.

### R04 — Contextual chunks

- Problem: a chunk loses the title, subject, or referent needed to understand it.
- Method: prepend a compact document/section/keyword context before embedding.
- Use when: chunks contain pronouns, repeated terminology, or weak standalone
  meaning.
- Measure: retrieval lift versus the identical unprefixed chunks.
- Failure signal: generated context hallucinates facts or dominates the source.
- Evidence: `course/week_03/contextual_chunk_pdf.py`.
- Maturity: `demo`.

### R05 — Late chunking and parent-child context

- Problem: retrieval prefers small units while encoding and generation need
  broader context.
- Method: encode within a larger context and pool subspans, or retrieve child
  chunks while returning their parent context.
- Use when: cross-sentence references repeatedly cause misses.
- Measure: Recall/nDCG, grounding, context tokens, latency.
- Failure signal: extra context introduces distractors without retrieval lift.
- Evidence: `course/week_04/chunking_pipeline/`,
  `labs/beyond_rag_week_6_lab_1/sv_rag_pipeline/README.md`.
- Maturity: `integrated`.

### R06 — Page-image and multimodal representation

- Problem: text extraction loses layout, equations, diagrams, or visual evidence.
- Method: render pages; embed them with CLIP/SigLIP or multi-vector ColPali-style
  models; answer with a vision-language model.
- Use when: visual layout is evidence rather than decoration.
- Measure: page Recall@K, visual-question accuracy, latency and storage.
- Failure signal: image retrieval is expensive but no better than extracted text.
- Evidence: `course/week_03/path1_page_image_qa.py`,
  `course/week_03/week-03-in-person-lab/team1_visual.py`.
- Maturity: `demo`.

### R07 — RAPTOR hierarchical summaries

- Problem: questions require evidence at different levels of abstraction.
- Method: recursively cluster chunks and summarize each cluster, producing a tree
  whose leaves preserve details and whose higher nodes represent broader themes.
- Use when: long-corpus evals show that fixed-level retrieval misses global or
  cross-section answers.
- Measure: local/global query Recall and grounding against token/index cost.
- Failure signal: recursive summaries compound omissions or unsupported claims.
- Evidence: `course/week_01/week-01.md`, `course/week_01/week-01.zh.md`.
- Maturity: `concept`.

## Indexing and retrieval

### I01 — Lexical retrieval baseline

- Problem: the project needs an inspectable first retriever.
- Method: tokenize, count terms, and rank with overlap, TF-IDF, or BM25.
- Use when: building a baseline or exact identifiers matter.
- Measure: Recall@K, nDCG@K, latency.
- Failure signal: paraphrases consistently miss.
- Evidence: `course/week_04/scripts/build_local_retrieval_index.py`,
  `course/week_07/rerank_eval_demo.py`.
- Maturity: `demo`.

### I02 — Dense vector retrieval

- Problem: semantically related text uses different words.
- Method: store document embeddings, embed the query, rank by vector similarity,
  and retain provenance in payloads.
- Use when: semantic paraphrase matters.
- Measure: Recall@K, nDCG@K, index latency and cost.
- Failure signal: high similarity without factual relevance.
- Evidence: `course/week_03/path2_text_chunk_qa.py`,
  `labs/beyond_rag_week_6_lab_1/sv_rag_pipeline/`.
- Maturity: `integrated`.

### I03 — Multi-vector late interaction

- Problem: a single vector compresses away token- or region-level matches.
- Method: retain token/patch vectors and score query-to-document interactions
  using MaxSim-style aggregation.
- Use when: fine-grained text or visual matching fails with single vectors.
- Measure: Recall/nDCG lift against compute, storage, and latency.
- Failure signal: no material lift over the single-vector baseline.
- Evidence: `course/week_03/path1_page_image_qa.py`,
  `labs/sv_ray_cluster_access/src/ray_cluster_access/sv_cluster_access_api.py`.
- Maturity: `demo`.

### I04 — Derived retrieval artifacts

- Problem: source chunks are not shaped like user questions or atomic evidence.
- Method: index propositions, factoids, generated QA pairs, or summaries alongside
  raw chunks.
- Use when: evals reveal a mismatch between source form and query form.
- Measure: per-artifact Recall/nDCG, grounding, index expansion and generation
  cost.
- Failure signal: synthetic artifacts introduce unsupported facts.
- Evidence: `course/week_04/retrieval_artifact_comparison/`,
  `course/week_04/task_02_xennials_factoid_wiki/`.
- Maturity: `demo`.

### I05 — Retrieval funnel, hybrid search, and reranking

- Problem: one retriever cannot provide both broad recall and precise ordering.
- Method: retrieve a wide candidate set with lexical, dense, or both; merge or
  fuse scores; apply a stronger cross-encoder/LLM reranker to a bounded set.
- Use when: Recall@K is acceptable but nDCG/MRR shows weak ordering, or lexical
  and dense retrievers recover complementary evidence.
- Measure: candidate Recall, post-rerank nDCG/MRR, latency and cost.
- Failure signal: a reranker is blamed when the relevant document never entered
  the candidate set.
- Evidence: `course/week_01/week-01.md`, `course/week_07/rerank_eval_demo.py`.
- Maturity: `demo`.

### I06 — Semantic cache

- Problem: repeated or semantically equivalent requests waste generation cost
  and latency.
- Method: store query embeddings with scoped responses and provenance; reuse only
  when similarity, identity, permissions, freshness, and policy version pass.
- Use when: traffic analysis proves repeated safe requests.
- Measure: hit rate, false-hit rate, latency/cost saved, stale-answer rate.
- Failure signal: cross-user memory leakage or reuse after evidence/policy changes.
- Evidence: `course/week_01/week-01.md`, `course/week_01/week-01.zh.md`.
- Maturity: `concept`.

## Query processing

### Q01 — Intent, domain, and context-need classification

- Problem: not every request should enter the same retrieval path.
- Method: classify scope, risk, domain relevance, and whether conversational or
  external context is required.
- Use when: the system supports multiple actions or sensitive domains.
- Measure: per-class precision/recall, routing error severity.
- Failure signal: uncertain classifications silently trigger privileged actions.
- Evidence: `course/week_06/guardrailed_rag_pipeline_demo.py`,
  `labs/beyond_rag_week_6_lab_1/guardrails/`.
- Maturity: `integrated`.

### Q02 — Query normalization and rewriting

- Problem: spelling, references, or conversation make the raw query a poor search
  key.
- Method: normalize conservatively; resolve conversational references; generate
  a retrieval-focused rewrite while preserving the original.
- Use when: traces show recoverable query formulation failures.
- Measure: retrieval lift and semantic-drift rate.
- Failure signal: rewrite changes user intent or removes safety-relevant detail.
- Evidence: `labs/beyond_rag_week_6_lab_1/guardrails/`.
- Maturity: `integrated`.

### Q03 — Relevance classifier

- Problem: irrelevant or out-of-domain content should not proceed to expensive
  retrieval/generation.
- Method: train a sequence classifier, optimize its operating threshold, and
  calibrate on real held-out traffic.
- Use when: rules cannot capture a stable domain boundary.
- Measure: precision, recall, F1, PR curve, calibration and costly error rate.
- Failure signal: synthetic validation reports extreme accuracy that does not
  transfer to real inputs.
- Evidence: `labs/beyond_rag_week_6_lab_1/relevance_detector/`.
- Maturity: `demo`.

### Q04 — Multi-query, decomposition, and hypothetical-answer retrieval

- Problem: one raw query under-specifies facets, combines multiple questions, or
  poorly matches document language.
- Method: generate controlled query variants, decompose multi-hop questions, or
  embed a hypothetical answer; retrieve per query and fuse candidates while
  preserving the original intent.
- Use when: query-level traces show formulation or multi-hop recall failures.
- Measure: Recall/nDCG lift, drift rate, duplicate candidates, added cost.
- Failure signal: generated queries introduce assumptions not present in the
  user's request.
- Evidence: `course/week_01/week-01.md`, `course/week_01/week-01.zh.md`.
- Maturity: `concept`.

## Graph retrieval

### G01 — Entity-local GraphRAG

- Problem: an answer depends on relations around known entities.
- Method: seed relevant entities, traverse bounded neighborhoods, attach source
  chunks, and synthesize from the local subgraph.
- Use when: traces repeatedly reveal multi-entity relation failures.
- Measure: multi-hop answer accuracy, provenance coverage, traversal cost.
- Failure signal: entity extraction errors dominate or graph paths lack evidence.
- Evidence: `labs/week5.2/ms_graphrag/`.
- Maturity: `demo`.

### G02 — Community/global GraphRAG

- Problem: corpus-wide themes cannot be answered from a few local chunks.
- Method: cluster the entity graph, summarize communities, map a query over
  community reports, then reduce results.
- Use when: questions ask for global patterns, not isolated facts.
- Measure: theme coverage, faithfulness, cost and answer stability.
- Failure signal: community summaries obscure minority or recent evidence.
- Evidence: `labs/week5.2/ms_graphrag/`.
- Maturity: `demo`.

### G03 — DRIFT retrieval

- Problem: a broad question needs global orientation and local evidence.
- Method: use community context to generate follow-up directions, then perform
  local refinement and evidence retrieval.
- Use when: neither global summaries nor local search alone is sufficient.
- Measure: multi-step coverage, groundedness, query and token cost.
- Failure signal: generated follow-ups drift away from the original intent.
- Evidence: `labs/week5.2/ms_graphrag/`.
- Maturity: `demo`.

### G04 — Three-layer memory with Personalized PageRank

- Problem: facts, schemas, entity types, and passages need joint retrieval.
- Method: build schema, fact, and evidence layers; connect a heterogeneous graph;
  create query-aware reset probabilities; suppress hubs; rank with Personalized
  PageRank.
- Use when: evidence shows stable graph-shaped retrieval needs.
- Measure: passage/entity relevance, convergence, lambda sensitivity, grounding.
- Failure signal: heuristic extraction or conflict resolution creates false graph
  authority.
- Evidence: `labs/week5.2/memgraphrag_concepts/`.
- Maturity: `integrated`.

## Safety and grounding

### S01 — Cheap-first request gates

- Problem: malformed, secret-bearing, irrelevant, or unsafe input should not
  consume privileged or expensive stages.
- Method: run deterministic format/secret checks before model-based gates and
  short-circuit with a recorded reason.
- Use when: any pipeline accepts untrusted input.
- Measure: false allow/deny rates, blocked-stage cost, gate latency.
- Failure signal: gate order leaks secrets or performs retrieval before scope
  validation.
- Evidence: `course/week_06/guardrailed_rag_pipeline_demo.py`.
- Maturity: `demo`.

### S02 — PII and secret detection

- Problem: sensitive information may enter prompts or leave responses.
- Method: regex and checksums for structured identifiers; optional NER for names
  and addresses; redact rather than log raw values.
- Use when: processing user, enterprise, or memory data.
- Measure: entity-level precision/recall and residual exposure.
- Failure signal: regex-only rules over-redact ordinary numbers or miss variants.
- Evidence: `course/week_06/pii_redaction_demo.py`,
  `labs/beyond_rag_week_6_lab_1/response_grounding/`.
- Maturity: `integrated`.

### S03 — ACL pre-filtered retrieval

- Problem: unauthorized content can influence ranking or generation even if
  hidden later.
- Method: bind identity and permission scope into candidate filtering before
  similarity ranking.
- Use when: documents have different visibility.
- Measure: unauthorized retrieval rate must remain zero; authorized Recall@K.
- Failure signal: post-retrieval filtering or permissions supplied only in the
  prompt.
- Evidence: `course/week_06/guardrailed_rag_pipeline_demo.py`.
- Maturity: `demo`.

### S04 — Indirect prompt-injection defense

- Problem: retrieved documents can contain malicious instructions.
- Method: delimit and datamark retrieved content, explicitly classify it as data,
  and keep system policy outside the untrusted region.
- Use when: retrieving user-authored or external content.
- Measure: attack success rate and answer utility on clean content.
- Failure signal: trusting a chunk because its retrieval score is high.
- Evidence: `course/week_06/indirect_injection_defense_demo.py`.
- Maturity: `demo`.

### S05 — Claim-level groundedness with NLI

- Problem: answer-level scores hide individual unsupported claims.
- Method: extract atomic claims; build claim-document pairs; use semantic
  similarity as a cheap filter; apply NLI entailment to retained pairs.
- Use when: factual claims must be traceable to retrieved evidence.
- Measure: supported-claim fraction, claim precision/recall, NLI calibration.
- Failure signal: sentence splitting merges claims or NLI thresholds are treated
  as universal truth.
- Evidence: `labs/beyond_rag_week_6_lab_1/response_grounding/`.
- Maturity: `integrated`.

### S06 — Exploratory retrieval and grounded rewrite

- Problem: an answer contains useful but initially unsupported claims.
- Method: re-query the same authorized index for each failed claim, re-evaluate
  entailment, and rewrite using supported claims only.
- Use when: omission is preferable to unsupported fluency.
- Measure: groundedness lift, added latency, unsupported-claim residue.
- Failure signal: the second pass escapes the original permission or corpus scope.
- Evidence: `labs/beyond_rag_week_6_lab_1/response_grounding/`.
- Maturity: `integrated`.

### S07 — Abstain, hedge, refuse, or escalate

- Problem: the system lacks enough authorized evidence or confidence to answer.
- Method: map groundedness, risk, and calibrated uncertainty to a bounded action.
- Use when: the cost of a confident wrong answer is material.
- Measure: selective accuracy, coverage, unsafe-answer rate, escalation quality.
- Failure signal: a single arbitrary similarity threshold is called
  "confidence."
- Evidence: `course/week_06/guardrailed_rag_pipeline_demo.py`,
  `course/week_06/week-06.zh.md`.
- Maturity: `demo`.

## Evaluation

### E01 — Gold/EVAL set design

- Problem: architecture choices cannot be judged from anecdotes.
- Method: collect representative queries, graded relevance labels, expected
  evidence, answer constraints, safety cases, and held-out splits.
- Use when: before upgrading retrieval or generation.
- Measure: coverage by intent, difficulty, risk, source and time.
- Failure signal: generated test questions mirror the system that will be tested.
- Evidence: `course/week_07/week-07.zh.md`, `templates/eval-case.md`.
- Maturity: `concept`.

### E02 — Precision@K and Recall@K

- Problem: determine whether results are clean and whether relevant evidence was
  found.
- Method: compute relevant retrieved / retrieved and relevant retrieved / all
  relevant.
- Use when: diagnosing first-stage retrieval.
- Measure: both metrics by query slice; never report one alone.
- Failure signal: incomplete relevance judgments make Recall meaningless.
- Evidence: `course/week_07/week-07.zh.md`.
- Maturity: `demo`.

### E03 — MRR and MAP

- Problem: measure first-answer position and ranking across multiple relevant
  items.
- Method: reciprocal rank for the first relevant item; average precision across
  all relevant ranks.
- Use when: early success or multiple relevant documents matter.
- Measure: MRR/MAP with confidence intervals.
- Failure signal: MRR hides all relevant documents after the first.
- Evidence: `course/week_07/rerank_eval_demo.py`,
  `course/week_07/week-07.zh.md`.
- Maturity: `demo`.

### E04 — DCG and nDCG

- Problem: relevance is graded and top ranks matter more.
- Method: use gain `2^rel - 1`, logarithmic rank discount, and normalize by the
  ideal ranking.
- Use when: evaluating rerankers or graded relevance.
- Measure: nDCG@K by query and slice.
- Failure signal: inconsistent handling of queries with no relevant documents.
- Evidence: `course/week_07/ndcg_demo.py`.
- Maturity: `demo`.

### E05 — Precision-recall curve and AUC-PR

- Problem: a classifier or retriever needs a threshold under class imbalance.
- Method: sweep thresholds and plot precision versus recall; summarize with
  average precision/AUC-PR.
- Use when: relevant items are rare.
- Measure: curve shape and operating point, not only one scalar.
- Failure signal: choosing a threshold on the final test set.
- Evidence: `course/week_07/pr_curve_demo.py`.
- Maturity: `demo`.

### E06 — Stage-localized RAG diagnosis

- Problem: end-to-end answer failure does not identify the broken component.
- Method: evaluate candidate recall, ranking, context selection, generation,
  grounding, safety, and abstention separately.
- Use when: deciding what to fix next.
- Measure: Recall@K plus nDCG/MRR plus claim grounding and answer quality.
- Failure signal: replacing the generator to fix a retrieval miss.
- Evidence: `course/week_07/rerank_eval_demo.py`.
- Maturity: `demo`.

### E07 — Paired significance and practical effect

- Problem: metric movement may be noise or too small to justify complexity.
- Method: compare identical queries with paired bootstrap or permutation tests;
  report confidence intervals and absolute effect size.
- Use when: choosing between retrieval variants.
- Measure: statistical confidence, nDCG/Recall delta, latency and cost delta.
- Failure signal: declaring victory from an unpaired average increase.
- Evidence: `course/week_07/week-07.zh.md`.
- Maturity: `concept`.

### E08 — Grounding, citation, and judge evaluation

- Problem: retrieval metrics do not prove the answer is faithful.
- Method: evaluate atomic claim entailment and citation support; calibrate any
  LLM judge against human labels and inter-rater agreement.
- Use when: generated answers are evaluated.
- Measure: claim precision/recall, citation correctness, Cohen's kappa.
- Failure signal: the same model generates and judges without calibration.
- Evidence: `course/week_07/week-07.zh.md`,
  `labs/beyond_rag_week_6_lab_1/response_grounding/`.
- Maturity: `integrated`.

### E09 — Diversity, calibration, and trajectory evaluation

- Problem: redundant results, uncalibrated confidence, or bad intermediate
  actions are hidden by final-answer metrics.
- Method: add MMR/alpha-nDCG for diversity, ECE/selective accuracy for
  confidence, and node/trajectory checks for agent runs.
- Use when: the application returns varied evidence or takes multiple actions.
- Measure: diversity-aware relevance, ECE, abstention coverage, step success.
- Failure signal: optimizing one aggregate score until behavior degrades.
- Evidence: `course/week_07/week-07.zh.md`, `templates/agent-trace.json`.
- Maturity: `concept`.

## Agent and adaptive-learning loops

### A01 — Observable agent-first loop

- Problem: retrieve-and-answer systems hide intent, decisions, and failure
  location.
- Method: make `intent -> retrieve -> decide -> respond -> trace -> evaluate`
  explicit and persist inputs, evidence, decision, action and outcome.
- Use when: retrieval informs actions, memory, refusal, or tools.
- Measure: per-stage correctness, trace completeness, end-to-end utility.
- Failure signal: traces contain prose but omit evidence IDs and policy reasons.
- Evidence: `PROJECT_PLAN.md`, `templates/agent-trace.json`.
- Maturity: `concept`.

### A02 — Evidence-driven architecture escalation

- Problem: teams adopt advanced retrieval before proving the baseline failure.
- Method: require a failure, target metric, baseline, cost budget, safety impact,
  and removal criterion before adding complexity.
- Use when: proposing reranking, GraphRAG, RAPTOR, fine-tuning, or memory.
- Measure: paired metric lift and total system cost.
- Failure signal: architecture selected by novelty or demo quality.
- Evidence: `PROJECT_PLAN.md`,
  `decisions/2026-06-06-evidence-driven-architecture-escalation.md`.
- Maturity: `integrated`.

### A03 — Prerequisite-aware adaptive learning

- Problem: a fixed curriculum repeats mastered content or skips required
  concepts.
- Method: estimate mastery, recursively collect prerequisites, remove mastered
  nodes, topologically order the remainder, teach, quiz, and update mastery.
- Use when: building an explainable adaptive tutor.
- Measure: path correctness, source grounding, quiz gain and trace usefulness.
- Failure signal: mastery scores update without durable evidence.
- Evidence: `labs/curriculum-weaver-lite/app.js`.
- Maturity: `demo`.

### A04 — Bounded tool use and Text-to-SQL

- Problem: some intents require an action or structured database answer rather
  than retrieval-only prose.
- Method: classify tool intent, expose a narrow typed interface, generate a
  candidate call or SQL query, validate schema/permissions/read-only policy,
  execute in a bounded environment, and trace inputs and results.
- Use when: authoritative information lives behind a functional API or relational
  database.
- Measure: execution accuracy, unauthorized-operation rate, result grounding,
  latency.
- Failure signal: arbitrary SQL, write access, or hidden tool errors are passed
  directly to the user.
- Evidence: `course/week_01/week-01.md`, `course/week_01/week-01.zh.md`.
- Maturity: `concept`.

## Selection Ladder

Use this order unless eval evidence justifies skipping a step:

```text
lexical baseline
-> fixed chunks
-> dense retrieval
-> structure/semantic/contextual representation
-> hybrid retrieval or reranking
-> derived artifacts or multi-vector retrieval
-> graph retrieval
```

Safety, provenance, trace, and evaluation are not later rungs. They apply from
the first baseline.
