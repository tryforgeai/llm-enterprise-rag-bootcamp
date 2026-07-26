# T021 Week 07 Class Capture

Status: doing

Date: 2026-07-25

## Goal

Capture Week 07 material on evaluating RAG systems from retrieval to reasoning: how to build an EVAL set, the six classical retrieval metrics, statistical significance and retrieval diversity, generation-side evaluation (RAGAS, claim-level entailment, LLM-as-a-Judge, RGB abilities), and the frontier (abstention calibration, multi-hop, evolutionary test sets, agentic/trajectory eval, Goodhart's law, cost). Connect it to Avaloka's Memory Reader benchmark (T008) and the evidence-driven architecture-escalation rule.

## Working File

`course/week-07.zh.md`

## Source

`course/week_07/summer-week-7-lesson-plan.pdf` (*The Measure of All Things — Evaluating RAG Systems from Retrieval to Reasoning*, Asif Qamar / SupportVectors, first draft 2026-07-18)

## Done Criteria

- [x] Lesson-plan PDF is read in full (31 pages) and summarized.
- [x] EVAL-set construction method recorded (0-4 graded relevance, SME cherry-pick recipe, 200/1000 scale, SME Summit, eval decay).
- [x] Optimisation goal argmax_θ E[μ(q,θ)] recorded with θ/μ/Q meaning.
- [x] Six classical retrieval metrics recorded as a staircase (Precision/Recall → MRR → MAP → AUC-PR → nDCG) with the nDCG three-layer + normalisation and the gain-convention caveat.
- [x] The nDCG@K ↔ Recall@K diagnostic pair recorded.
- [x] Statistical vs practical significance (paired bootstrap/permutation, N≈500-1000, nDCG 0.02-0.05 threshold) and retrieval diversity / MMR recorded.
- [x] RAGAS four metrics and its five limitations recorded.
- [x] Claim-level entailment (FActScore 58%, ALCE citation accuracy 40-75%) recorded.
- [x] LLM-as-a-Judge 2.0 (Prometheus-2, judge biases, Cohen's κ<0.6 reject, rule of three) recorded.
- [x] RGB four abilities recorded.
- [x] Six frontiers recorded (ECE/abstention, multi-hop, evolutionary test sets, agentic/trajectory, Goodhart, cost).
- [x] Evaluation Map connecting metrics back to Weeks 1-6 recorded.
- [x] Agent-capability, Avaloka-application, and review-question sections drafted.
- [ ] Live classroom discussion / instructor's spoken commentary is still missing — only the lesson-plan PDF has been captured (class is today, 2026-07-25).
- [ ] A Week 07 eval artifact is created: a real retrieval-metric baseline (Recall@5, MRR, nDCG@5 + nDCG↔Recall diagnosis) on Memory Reader V0 or the Xennials FactoidWiki demo.
- [ ] Avaloka application section is revised from "initial mapping" to a concrete EVAL-set + ECE/negative-rejection design.

## 2026-07-25 Update

Created the first Week 07 record from the lesson-plan PDF (pre-class capture):

- Act I: EVAL set as the yardstick, gold vs cherry-picked construction, SME (not engineer) authorship, 200/1000 scale, eval decay, evaluation as the AI engineer's own job, and the argmax_θ E[μ(q,θ)] optimisation goal.
- Act II: the six-metric staircase with the seashell/cave analogies, the nDCG three layers (exponential gain, cumulative, log-discount) plus normalisation, the Järvelin-Kekäläinen vs Burges gain-convention caveat, and the nDCG↔Recall diagnostic pair.
- Interlude: BEIR/MTEB/MSMARCO, paired bootstrap/permutation significance, statistical vs practical significance, and MMR for diversity.
- Act III: RAGAS four metrics + five limitations, FActScore/ALCE claim-level entailment, Prometheus-2 and judge biases with Cohen's κ calibration and the judge rule of three, and the RGB four abilities.
- Act IV: six frontiers (ECE/abstention calibration, multi-hop/synthesis, evolutionary test-set generation, agentic/trajectory three-layer eval, Goodhart's law reward-hacking modes, cost dimension).
- Evaluation Map table connecting every metric back to Weeks 1-6.
- Drafted agent-capability (measurable self-doubt via ECE + negative rejection), Avaloka mapping (Memory Reader V0 baseline for T008, Avaloka EVAL set via SME Summit, honest "I don't know" via ECE), and a nine-item pre-class self-test.
