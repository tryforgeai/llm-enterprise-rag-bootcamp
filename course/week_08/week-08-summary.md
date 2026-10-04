# Week 08 Summary — The Personal Equation: Measure the Measurer Before You Measure the Machine

**Date:** 2026-08-01 · **Source:** `uploads/the-personal-equation.pdf` (*The Personal Equation — Seven small experiments you are going to fail*, SupportVectors, 29 pp) and `uploads/the-measure-of-all-things.pdf` (*The Measure of All Things*, full 169-page five-act edition)

---

## TL;DR

The whole week compresses into one sentence:

> **Measure the measurer first — and the deepest metric of all is: does it know what it doesn't know?**

Week 07 taught us how to measure **retrieval** (the yardstick plus the six-metric staircase). This week turns the lens on **the generator itself**, and then on **the world after deployment**.

The full lecture expands Week 07's four acts into **five**, adding Act V, "The Observatory":

```
Opening   The Personal Equation   (seven small experiments you are going to fail)
Act III   The Generator           (RAGAS floor → FActScore/RAGChecker → ALCE)
Act IV    The Frontier            (judge 2.0, RGB, epistemic humility, multi-hop, evolving sets, agentic)
Act V     The Observatory         (offline gate + online drive + drift + ratchet)  — new
Coda      The Evaluation Map      (wire every low score back to "which component to fix")
```

The opening is unusual by design: **students fail seven times with their own hands first**, and each failure maps to a metric taught that afternoon. Not theory-then-example — observe the bias in yourself, then name it.

---

## Opening: The Personal Equation

### The historical anchor

Greenwich, 1796. The Astronomer Royal, **Maskelyne**, fires his assistant **Kinnebrook** because Kinnebrook's recorded transit times are consistently "slow."

In 1823, **Bessel** discovers it was never negligence — **every observer's nervous system carries a stable, measurable personal bias.** He writes it as a correction term and names it **the personal equation**.

> The lesson is not "fire the biased instrument." It is **measure it, write down its equation, and subtract it.**

**Every LLM judge you will ever hire has its own personal equation** — a preference for verbosity, for the first answer shown, for its own house style.

Classroom rules: everything anonymous and aggregated (hands, slips of paper, half the room); **the room itself is the data**. "Fail warmly" — the point is not that you are flawed, but that **every measuring instrument is**, and today you are the instrument.

> The opening names two victims: an assistant astronomer who lost his career to experiment 1, and GPT-4o, which lost 30 points of factual precision to experiment 4.

### Seven experiments → seven metrics

| # | What you experienced | What it's called | The metric it points to |
|---|---|---|---|
| 1 | Eyes closed, estimate 60 seconds — wrong in the **same direction** both rounds | Judge bias = the personal equation | calibrate on a gold set, pin the version, **subtract don't fire** |
| 2 | Eight 90% confidence intervals; roughly 50% actually contain the truth | Over-confidence | **ECE**, reliability diagrams, temperature scaling |
| 3 | "How many of each animal did Moses take on the ark?" — everyone says "two." It was **Noah** | Intrinsic hallucination | claim-level entailment |
| 4 | Read an Australia passage mentioning only Sydney/Melbourne; half the room answers "capital = Canberra" — **which never appears** | **Parametric leakage** (negative-rejection failure) | unanswerable test sets, **negative rejection rate**, the Calabi–Yau probe |
| 5 | A fake bio: "Einstein, an Ohio plumber born in 1961." People still answer "relativity / 1879 / Germany" | Entity collision | **FActScore**-style atomic decomposition |
| 6 | A double question (founding year grounded, headcount not); the slips sort themselves into three piles | The trichotomy (answer · hedge · refuse) | sufficiency-conditioned accuracy, abstention quality |
| 7 | Two quizzes of equal difficulty: under +1/0/**0** everyone guesses; under +1/0/**−1** "pass" blooms across the room | **Goodhart at the grading desk** | abstention-aware scoring (CRAG's +1/0/−1) |

### Experiment 1: bias is not variance

The real lesson on this slide is the **bias–variance distinction**. Round one looks like random noise. Round two is designed to make you notice both rounds erred in the **same direction** — and "variance" collapses into "bias" on the spot.

**They are handled in opposite ways:** variance washes out with averaging and repeated sampling; **bias never washes out, no matter how many times you average. It can only be measured and subtracted.**

> **"You do not have errors. You have *an* error."**
> **"Subtract, don't fire."**

The hidden premise: **you will never get an unbiased instrument.** Maskelyne's mistake was not employing a biased assistant — it was believing an unbiased one existed.

**One important caveat:** a clock offset is a constant; **judge bias is non-stationary** — it drifts with prompt, with domain, and above all with vendors quietly updating models. So the machine version of the correction term **has a shelf life**: pin the version, freeze a calibration set, and monitor Cohen's κ (alarm on drift > 0.05).

### Experiment 2: over-confidence, and the interval that could not fail

Eight questions, each with a **90% confidence interval**:

| # | Question | Truth | What an honest interval looks like |
|---|---|---|---|
| 3 | Length of the Nile | ~6,650 km | 5,500–7,500 |
| 4 | Royal Observatory Greenwich founded | **1675** | 1600–1750 |
| 5 | Weight of a blue whale's heart | the one preserved specimen ~180 kg | 50–300 kg (most anchor far too low) |
| 6 | Keys on a concert piano | **88** | should be narrow — commonly known |
| 7 | First TREC conference | **1992** | 1985–2000 |
| 8 | Height of Denali | **6,190 m** | 5,000–7,000 |

**What actually happened in the room:** half the class gave **point estimates** — a single number, an interval of width zero, the extreme of over-confidence, hit rate ≈ 0 (some wrote 80 or 83 for the piano). Those who gave intervals made them far too narrow, hitting 2–3 of 8 (88 written as 100–250, the whole interval above the truth; the whale heart as 2–5 kg, off by one to two orders of magnitude; the Nile consistently guessed low and TREC consistently guessed recent — **systematic bias, echoing experiment 1**).

Claimed 90% confidence, actual ~25–40% coverage → the reliability diagram sags below the diagonal → **that gap is ECE.**

**War story (the interval that could not fail):** an early Spark MLlib regression returned a prediction interval from **−∞ to +∞ at 95% confidence** — **perfectly calibrated, never wrong, and utterly useless.**

> **Calibration and sharpness are two orthogonal axes.** Score only calibration and you can max it out by widening; score only sharpness and you can cheat by narrowing. Hence a **proper scoring rule (Brier)** that punishes both. The goal is **calibrated *and* sharp**: humble enough to be right, narrow enough to be useful.

The machine version of the infinite interval has two incarnations: **over-hedging** (train only for faithfulness and you get "it is possible that…", faithful and useless) and **abstaining on everything** (a perfect NRR with zero coverage). So this week treats abstention as a **dial, not a switch**, and finds the operating point on a **risk–coverage curve**.

### Experiment 3: the Moses illusion (intrinsic hallucination)

Cognitive science calls it the **Moses illusion** — when the substituted word is semantically close to the correct one (Moses and Noah both carry an "ark smell"), the comprehension system waves it through without checking.

The conditions — "immediately, in unison, shout on three" — **deliberately force System 1** and cut out the step where you go back and check the evidence. Read it slowly to yourself and you catch Noah.

**The RAG parallel:** an LLM runs in that buzzer-beating state by default (autoregressive decoding, no built-in verification step). So mitigating hallucination means **bolting on System 2** — CoT self-checking before, or claim-level entailment after.

Distinguish **intrinsic** (contradicts the evidence, as here) from **extrinsic** (adds information the evidence never contained).

**The trap:** "two of each" is perfectly consistent with the ark story on its own, so **a naive faithfulness check passes it.** Only entailment-checking against the question's actual referent (Moses) catches it.

> **Same confidence, same grammar, wrong referent.**
> Fluency and correctness are decoupled — which is why you cannot eyeball hallucination.

### Experiment 4: correct ≠ grounded (the most important line of the week)

The purest test of parametric leakage. The Australia passage mentions Sydney, Melbourne, Perth, Brisbane, 1788, 1901 — **Canberra never appears.**

Three traps:

1. The passage repeatedly uses "financial centre" and "cultural **capital**," priming the word *capital* to lure you into answering.
2. "Commit it to paper as you would defend it" removes the hedging escape route.
3. **The decisive one — the leaked Canberra is actually correct in the real world.** Precisely because it is right, you never get suspicious.

Which establishes the week's hardest rule:

> **Correctness ≠ groundedness.** An answer can be entirely correct and still be a grounding failure. **The most dangerous form of parametric leakage is "factually right but unsupported"** — and any check that just looks at whether the answer is right will pass it.

**The full-marks answer** (formalised as the trichotomy in Act III):

> **"The passage doesn't say — though it's commonly known to be Canberra."**

Answer from the evidence (negative rejection) **plus** label the prior explicitly as a prior. The point is **putting the prior in the right drawer rather than letting it impersonate evidence.**

> **Evidence in the window, a lifetime of priors behind it.**
> Negative rejection is not a feature you fix once — it is **a contest re-won on every generation**, so it must be measured continuously. (RGB measures ChatGPT-class systems at just **43–45%**.)

### Experiment 5: the mechanism of entity collision

Why do people still answer "relativity" after reading the plumber bio?

1. **A name is an extremely strong retrieval key**, carrying a dense cluster of high-frequency, high-confidence priors (relativity / 1879 / Germany / Nobel). "Plumber / Dayton / 1961" are low-frequency weak associations and simply lose the competition.
2. **The Bayesian view** — `posterior ∝ likelihood(evidence) × prior`. "Einstein = physicist" is an **extremely sharp prior spike**; even counter-prior evidence barely moves the posterior.
3. Leakage happens where **strong prior × counter-prior evidence** intersect most violently — which is why questions 1 and 2 (best known for / born when and where) leak and question 3 (six years as an apprentice, no competing prior) does not.
4. Inside a transformer, entity tokens activate high-weight association pathways that **can overwhelm attention to the context.**

**The defence** = Week 06's response-side grounding (every claim must find support in the evidence) **plus** this week's FActScore claim-level verification.

> **Any query carrying a famous entity name is a high-risk zone for entity collision.**

### Experiment 6: the trichotomy — The Friend

Given a passage saying "Meridian Cartworks was founded in 2011," ask "what year was it founded, and how many employees does it have today?" — **the founding is grounded, the headcount is not.**

The slips sort into three piles: those who answered both (inventing a headcount), those who hedged ("a few hundred?"), and those who answered what was grounded and flagged the gap.

**That is the complete trichotomy of honest generation: answer / hedge / refuse**, each used in its right place.

A good RAG system is the third pile, with better manners:

> *"Founded in 2011. The headcount isn't in what you gave me — let's find out."*

> **Honesty is not refusal. It is using the right verb for each half of the question.**

Instruments: **sufficiency-conditioned accuracy** (read accuracy separately by whether the evidence was sufficient) and abstention quality.

### Experiment 7: Goodhart at the grading desk

Two quizzes of equal difficulty. The rule changes from **+1 / 0 / 0** (no penalty for a wrong answer) to **+1 / 0 / −1** (a wrong answer costs you), and abstention blooms immediately — **the knowledge didn't change, the incentive did.**

1. **Honesty is a rational response to the scoring rule, not a personality trait** — guessing strictly dominates when wrong answers are free.
2. "Right = 1, wrong-or-blank = 0" is **the exam models sit for their entire lives**, so **we trained them into guessers with our own hands.**
   > **They guess because we paid them to.**
3. **The fix is to change the rule, not the model** — abstention-aware scoring, CRAG's **+1 / 0 / −1**. The ratio of penalty to reward **is an implicit confidence threshold** (a hospital pricing a wrong answer at −10 raises the threshold and buys more abstention).
4. This is the course's thesis `argmax_θ E[μ(q,θ)]` demonstrated on humans: **the metric μ you choose shapes the system θ. Choose the wrong metric and you build the wrong system.**

#### The academic backbone: Why Language Models Hallucinate

> Kalai, Nachum, Vempala & Zhang (OpenAI, 2025-09, arXiv:2509.04664) turns experiment 7 into a mathematical result.

Two causal stages: **pre-training** produces hallucination from **statistical pressure** even on perfect data (false statements are statistically indistinguishable from facts); **post-training** sustains it because mainstream benchmarks **penalise uncertainty.**

The result worth memorising:

> **The Generation–Classification Inequality: generative error rate ≥ 2 × classification error rate (minus a calibration term).**
> **Generating correct text is inherently harder than judging whether text is correct.**

This inequality is the unifying floor under much of the week — it explains Act III's **small-verifier pattern** (verification costs less than half of generation, so having a small model check a large model claim by claim is economics, not a trick), and it echoes RAGChecker's bidirectional entailment.

The proposed solution is isomorphic to the week's thesis: **socio-technical — change the scoring of mainstream benchmarks rather than adding yet another hallucination benchmark.** Reward appropriate uncertainty, penalise confident errors more heavily, watch calibration rather than accuracy, and for high-stakes use RAG plus a confidence threshold.

---

## Act III: The Generator — From Judging the Pantry to Judging the Chef

> A great chef makes a good meal from ordinary ingredients; a bad one ruins perfect ones. The six retrieval metrics judge only whether the right evidence arrived; this act judges whether the LLM used it well.

This is the **metric-side counterpart** of Week 06's response-side conscience (the claim–evidence bipartite graph).

### RAGAS: four metrics (a floor, not a ceiling)

| Metric | What it measures |
|---|---|
| **Faithfulness** | decompose the answer into claims, verify each against the retrieved context, report the supported fraction. Backend can be an LLM (flexible but circular) or classic NLI (cheaper and more conservative — the DeBERTa entailment model from Week 06) |
| **Answer relevancy** | reverse-generate synthetic questions from the answer, measure cosine similarity to the original. Answering a different question → relevancy ≈ 0 |
| **Context precision** | among the chunks handed to the LLM, are the relevant ones ranked first? (retrieval ordering, seen from the generation side) |
| **Context recall** | decompose the ground-truth answer into claims; can each be attributed to some retrieved chunk? Miss a key passage and this drops |

> **Quiz 7, "the fluent non-answer":** asked about refunds, the system answers about shipping — and every sentence is perfectly supported by the documents. → **Faithfulness stays high; answer relevancy collapses.**
> One is measured against the evidence, the other against the question. **You need both** — a grounded non-answer fools the first completely.

### RAGAS's five limitations

1. **Circular LLM dependence and self-enhancement bias** — the model scores itself generously. Hire "Kepler, not Ptolemy": a judge from a different model family.
2. **Context-window blindness** — it sees only what was passed in, never the ten better chunks retrieval missed (that's Act II's job).
3. **No claim granularity** — a sentence containing 3+ independently falsifiable claims can pass as a whole.
4. **Unstable scores** — GPT-4, Claude and Llama disagree, and vendors update quietly.
5. **No attribution verification** — it checks consistency with the context, not whether each claim cites the right passage.

**The accompanying discipline, evaluator pinning:** pin the judge to a dated checkpoint, maintain a **frozen calibration set of 50–200 items**, re-run it on a schedule. **Cohen's κ drifting by more than 0.05 means the evaluator moved.**

> **RAGAS grew up (2025):** answer relevancy → response relevancy (a "no comment" now scores 0); context relevance → rank-aware context precision@k + context recall; new noise sensitivity and factual correctness (claim-level F1 against a reference — quietly abandoning pure reference-free evaluation); plus a multi-turn schema. **Two of the five complaints are partly addressed; three remain.**

### FActScore: the sharpest advance since RAGAS

Answer → atomic facts → verify each → report the supported fraction. In 2023, ChatGPT-generated biographies scored just **58%** factual precision.

Three years on, that number has been moved by **retrieval and abstention**, not scale alone:

- 2026 reasoning models with browsing: **~99%** claim precision (GPT-5 system card, ~1% error)
- GPT-4o-class non-reasoning models: **62–71%** (HalluLens LongWiki 71%)
- **But tail knowledge without retrieval remains brutal** — SimpleQA Verified tops out at **72.1%**, most frontier models land at **29–55%**, and DeepMind's FACTS aggregate is about **69%**

### RAGChecker: the diagnostic you reach for after the telemetry alarms

Decompose both the answer and the ground truth into atomic claims and check **bidirectional entailment**:

- **Retrieval diagnostics** — claim recall (did the evidence arrive?), context precision
- **Generation diagnostics** — faithfulness, hallucination, noise sensitivity, context utilization, plus one nobody else measures: **self-knowledge** (correct but not present in the retrieved evidence = answered from parametric memory, hinting at contamination or in-parameter domain knowledge)

Its key finding: the **faithfulness–gullibility trade-off** — the more a model trusts its context, the more faithful it is *and* the more easily noise leads it astray. **So faithfulness and noise sensitivity must be read on the same screen.**

> **RAGAS is telemetry. RAGChecker is the diagnostic instrument.**

### The economics of checking: the small-verifier pattern

| Verifier | Number |
|---|---|
| **MiniCheck** | GPT-4 accuracy at roughly **1/400** the cost |
| **HHEM** | cheap enough to run on every claim in production; powers public hallucination leaderboards |
| **Lynx** | **87.4%** on HaluBench, edging past GPT-4o |

**Routing:** a small verifier on every answer → RAGChecker on a sample → a frontier judge only for dimensions no specialised verifier covers.

> **Slippers at home, good shoes out of doors.**

### ALCE: is the citation itself correct?

Extends claim-level checking to **citation quality** — did each claim cite the right passage?

ChatGPT-class systems reach about **50% citation recall** on ASQA, and worse on ELI5 — **roughly one citation in two is suspect**, even when the answer is right.

In enterprise settings **citation accuracy is a deployment gate**: a footnote that does not hold up is worse than no footnote. (Automatic metrics agree with humans at 85% / 78% — good enough, not sacred.)

---

## Act IV: The Frontier

### Frontier 1 · LLM-as-a-Judge 2.0

Evaluation is a **specific task** and deserves a purpose-built model rather than a rented frontier one.

**Why not rent a general frontier model as your judge** (note: a specialised judge is also an LLM — just small, fine-tuned and local) — five reasons:

1. **Too expensive** — $500–2,000 per run for 10,000 items means you only dare evaluate quarterly; a local specialised judge has ≈ zero marginal cost and can watch hourly.
2. **Data leakage** — every answer and every piece of evidence goes out to an external API.
3. **Specialised is more accurate** — a **7B judge fine-tuned on 5,000 domain annotations beats prompted GPT-4** on human agreement in that domain.
4. **Uncontrollable and drifting** — vendors update models quietly, so the ruler changes under you; APIs cannot be version-pinned, local checkpoints can.
5. **Bias and collusion** — same model family means evaluator collusion and inflated scores.

The theoretical justification is the Generation–Classification Inequality: **checking is cheaper than generating, so a small verifier suffices.**

**Four specialised judges, each fixing one defect:**

| Judge | The innovation |
|---|---|
| **Prometheus 2** | open-source, runs locally, no API leakage. Two modes: direct assessment (absolute scoring against the rubric you supply) and pairwise ranking. **72–85%** agreement with humans |
| **AutoJ** | fixes **position bias** — shuffles order automatically |
| **JudgeLM** | fixes *what a judge should learn from* — the training data is human **evaluative judgements**, not good answers |
| **G-Eval** | fixes **calibration** — CoT plus probability-weighted score tokens, yielding smooth continuous scores (CoT adds 8–12 points of agreement at 3–5× token cost) |

> Prometheus 2 takes a physician's ordering of HHH: **harmless first, then honest, then helpful.** Example: answering "what is relativity?" with the field equations `G_μν = 8πT_μν` is honest and harmless — and useless to a ten-year-old. **A rubric lets you encode helpfulness into the score.**

**Four judge biases → antidotes:**

| Bias | Symptom | Antidote |
|---|---|---|
| Length | longer answers win | write concision into the rubric |
| Position | **40–60 point** swings between A/B orderings | run both orderings, average, keep only consistent pairs |
| Self-preference | can flip the ranking outright | different model family |
| Style over substance | — | anchor the rubric with examples; reason before scoring |

**Three iron rules:** different model family · average both orderings · never trust a single judge.

#### Cohen's κ by hand (the page most worth memorising)

100 items; the judge labels "grounded / fabricated" against human ground truth. `κ = (p_o − p_e) / (1 − p_e)`:

| Judge | Computation | κ | Verdict |
|---|---|---|---|
| **The deceptive judge** | p_o = 0.75; p_e = 0.75×0.70 + 0.25×0.30 = 0.60 | **(0.75−0.60)/0.40 = 0.375** | **reject** — 75% raw agreement is a bluff; 60 points of it was luck |
| **The lazy judge** (always says "grounded") | p_o = 0.70, but p_e = 1.0×0.70 = 0.70 | **0** | exposed on the spot as having zero skill |
| **The reliable judge** | p_o = 0.90; p_e = 0.70² + 0.30² = 0.58 | **0.762** (substantial) | **ship it** |

> **Raw agreement is fooled by class imbalance; κ subtracts luck and leaves only skill.**
> Enterprise rule: **reject any judge with κ < 0.6.** Absolute numbers reported externally must come from a judge that clears the bar.

(Use Kendall's τ for rank agreement, Krippendorff's α for multiple judges.)

**Two benchmark results worth keeping:**

- **JudgeBench** (350 hard pairs with objective right answers): the best conventional judge scores **~64%**, reasoning-model judges **~75%**, and fine-tuned open judges barely beat chance — **on hard pairs, today's judges are guessing.**
- **PoLL (Panel of LLM evaluators):** three heterogeneous small judges voting reach **κ 0.763, beating a single GPT-4's 0.627** at roughly **1/7** the cost. **Diversity beats scale** — exactly the "average several observers to cancel the personal equation" move.

⚠️ Watch for **preference leakage**: a generator and judge from the same family or with a distillation lineage inflate scores. **That is contamination, not an edge case.**

### Frontier 2 · The four RGB capabilities RAGAS never measures

| Capability | What it tests | Benchmark level |
|---|---|---|
| **Noise robustness** | can it ignore near-miss distractors? | good systems > 80%, naive < 50% |
| **Negative rejection** | can it abstain when there is no answer? | ChatGPT-class: **43–45%** |
| **Information integration** | can it synthesise across documents? | — |
| **Counterfactual robustness** | one document says port 480, the rest say 48 — does it flag the contradiction or follow blindly? | Rule: **contradiction is a first-class citizen** — surface the conflict, cite both sides, let the user adjudicate |

> **Quiz 9 · the Calabi–Yau test:** a company that sells network switches, whose RAG enthusiastically and correctly explains superstring geometry → **a negative-rejection failure.** The answer came from parametric memory, and Week 06's **response gate should have stopped it.**

**"Fabricating from noise" is still majority behaviour, and the most dangerous enterprise failure mode.**

### Frontier 3 · Epistemic humility (the hardest section of the week)

- **A mark of maturity: a system that never says "I don't know" is dangerous.** The lecturer's provocation still stands — hundreds of students, hundreds of systems, and he has never seen an enterprise RAG honestly say it.
- **Negative Rejection Rate (NRR)** — build a query set the corpus cannot answer and measure honest abstention. **Deployment threshold in regulated industries: > 70%.**
  > **A mechanism without measurement is just hope; without it, a guardrail is decoration.**
- **A 2025 warning (AbstentionBench)** — o1/R1-style **reasoning fine-tuning *reduces* abstention**, and scale does not fix it. Always report **in pairs**: rejection rate on unanswerables **plus** over-rejection rate on answerables (either one alone can be gamed).
- **Sufficiency-conditioned accuracy** — in RAG, "unanswerable" is **a property of the retrieved set, not of the question.** Label pairs sufficient/insufficient (an autorater does this at 93%) and read them apart: frontier models are excellent under sufficient context, and under insufficient context **they fail to abstain and answer anyway, guessing right 35–62% of the time from parametric memory.** A blended average hides the vice.
- **ECE** — the weighted gap between stated confidence and actual accuracy, bin by bin. Perfect is 0; modern LLMs run **0.05–0.15**; **larger instruction-tuned models are often worse** (confidence goes up without accuracy). The signature pattern: the high-confidence bin is over-confident by 15 points and dominates the error — **which is precisely the danger zone, because users listen hardest to confident answers.** Fixes: **temperature scaling (cheapest and most effective)**, Platt, isotonic.
- **Risk–coverage curves** — answer only above a confidence threshold, sweep the threshold, plot the curve. **Convex = well calibrated** (abstaining on a small slice buys a large drop in error). One sweep: answering everything gives **12% risk**; answering 60% drops it to **3%**.
  > CRAG prices one hallucination at one forgone correct answer; a hospital prices it at **ten** — **the same curve, two prices, opposite operating points.**
- **Conformal abstention (from vibes to a contract)** — compute nonconformity scores on a held-out set, sort, take the `⌈(n+1)(1−α)⌉`-th as the threshold → **a distribution-free coverage guarantee** (80–90% factuality while retaining most of the content). This is an **SLA-grade certificate** — but it assumes exchangeability with production traffic, and **drift expires the certificate.**

### Frontier 4 · Multi-hop

Information integration, contradiction detection, bridge inference (Doc A: drug X inhibits enzyme Y; Doc B: enzyme Y is overexpressed in disease Z → bridge: X may treat Z).

Benchmarks: HotpotQA / MuSiQue / 2WikiMultihopQA / **MultiHop-RAG** (ground truth annotated per hop, so you can **score the path, not just the endpoint**) / BRIEF (compress into atomic propositions and see whether the answer survives).

### Frontier 5 · Evaluation sets that fight back

**ARES** — 150 human annotations plus synthetic expansion plus **PPI (prediction-powered inference)**, giving each metric a **confidence interval**. Synthetic buys coverage; a little human annotation buys calibration.

**Mutation operators** evolve the question bank: flip the expected answer (tests negative rejection), add constraints, add ambiguity (tests disambiguation), require multi-hop, inject distractors.

Tools: **Giskard RAGET** (generates directly from the knowledge base), **DeepEval** (a RAGAS superset). **Keep the ruler from ossifying.**

### Frontier 6 · Agentic / trajectory evaluation

> Two agents reach the same correct answer; one reasoned, one guessed. Scoring only the endpoint cannot tell them apart — and the guesser collapses on the next hard question. This is the **Illusion of Competence.**

**Three levels:**

| Level | What it measures | Limitation |
|---|---|---|
| **L1 system efficiency** | latency / tokens / tool calls / cost per query | operational only; says nothing about quality |
| **L2 session outcome** | task success / answer correctness / satisfaction | tells you whether it worked, **not why** (it may have guessed) |
| **L3 node-level precision** | right tool? well-formed query? sound step? | **the diagnostic power lives here** |

> **L1 example:** asked for the hotel expense cap, Agent A (2s / 1 retrieval / 1k tokens / $0.01) and Agent B (25s / 8 retrievals / 7k / $0.12) both answer $250 → L1 says A wins, but **fast and cheap can also be wrong.**
>
> **L3 example:** "Who is the CEO of the company that acquired our largest supplier?" (correct: Maria Chen). L2 only says right or wrong; if the answer comes back David Lee, **L3 localises it to "the multi-hop reasoning held, entity disambiguation broke"** (Beta Holdings vs Beta Technologies), which is a fixable finding.
>
> **Medical example:** "Is this patient suitable for drug X?" answered "not recommended" — L2 scores both runs correct, but L3 distinguishes the good process (checked allergies and contraindications) from the bad one (never read the record, guessed right from general knowledge). **In high-stakes settings those two must never score the same.**

**TRACE** scores trajectories: process efficiency (steps / tokens / tool calls), cognitive quality (planning, hypotheses), and per-step evidence grounding.

#### pass@k vs pass^k: one log file, two opposite conclusions

```
pass@k = 1 − (1−p)^k     the optimist's number: at least one success in k tries
pass^k = p^k             the engineer's number: k consecutive customers all served
```

At p = 0.7: **pass@3 = 0.973, pass@8 ≈ 0.9999** (tends to 1); **pass^3 = 0.343, pass^8 ≈ 5.8%** (tends to 0).

> "Give me eight tries and I'll almost certainly succeed once" vs "serving eight customers in a row without a failure happens 5.8% of the time."
>
> **A harness with a verifier and retries lives on the optimistic curve (pass@k); a customer-facing agent lives on the engineering curve (pass^k).**

GPT-4o on τ-retail falls from **~61% at k=1 to ~25%** — **"70% success" does not mean 70% done; it means three out of ten customers are comprehensively broken.**

The trap: reporting "pass@8 = 99%" is close to worthless for production **unless you have a reliable verifier to pick the right one out of the eight candidates.**

A five-step refund chain: 0.9 per step → `0.9⁵ ≈ 59%`, `0.9¹⁰ ≈ 35%`. **"90% per step" is not a 90% process.**

> **Quiz 10 (computed exactly, without replacement):** 10 runs with 7 successes and 3 failures; sample 3 —
> **pass@3** = 1 − C(3,3)/C(10,3) = 1 − 1/120 = **119/120 ≈ 99.2%**
> **pass^3** = C(7,3)/C(10,3) = 35/120 ≈ **29.2%**
> **The customer SLA is pass^3 ≈ 29.2%.** pass@3 ≈ 99.2% licenses only "given retries and a reliable verifier, at least one output will likely be right."
> (Note: the exact without-replacement values 99.2% / 29.2% differ from the independent approximations 97.3% / 34.3%.)

**Attribution is hard:** **MAST** (14 failure modes; **verification failures are as common as capability failures**) and **Who&When** (identifying the culpable agent succeeds only **53.5%** of the time, the culpable step **14.2%** — post-hoc forensics is unsolved). **So instrument every stage at runtime** and turn "who failed" into a lookup in your own telemetry.

**The working stack:** an offline gate (gold set + NDCG + RAGAS + FActScore + ECE blocking the merge) plus online drivers (thumbs, shadow judge, human spot checks, interleaving). Tooling: LangSmith / Phoenix / Langfuse / W&B.

> **The cold industry number:** more than half of organisations have agents in production, quality is the top obstacle, and **roughly 70% of RAG systems still have no systematic evaluation. You are not going to be in that 70%.**

### The warning that runs through everything · Goodhart

| Optimise only for | What the system learns to arbitrage | Defence |
|---|---|---|
| faithfulness | **hedge inflation** — endless "it is possible that…" | pair with relevancy + informativeness |
| citation recall | **citation padding** | pair with precision; write concision into the rubric |
| a length-biased judge | **length gaming** | length-normalised judge |
| a judge from the generator's family | **evaluator collusion** | the three iron rules |

**The defence kit: metric ensembles + adversarial eval + red-teaming the metric itself + a held-out golden judge that is never used for training.**

> **Kelvin measures, Cameron warns, and Goodhart explains how the warning comes true.**

### The economics of an answer (the Pareto frontier)

An answer costing $5 and 30 seconds may be worse than one costing $0.05 and 2 seconds at 85% quality. Report cost@quality, quality@cost, tokens-per-correct-answer, and the CFO's **dollars-per-correct-answer**. **A system below the frontier should not ship.**

### Multi-turn

Contextual faithfulness, context-switch handling, turn efficiency.

**MTRAG** (the first human-generated end-to-end multi-turn RAG benchmark: 110 conversations, 7.7 turns on average, **~25% unanswerable**) finds that systems degrade in later turns, unanswerables are the hardest case, and retrieving on the raw last-turn query is far worse than on a rewritten one. **Splitting the same facts across turns costs ~39% performance** — the model guesses early, locks in, and never revisits.

---

## Act V: The Observatory (new this week)

> Evaluation no longer ends where production begins — **the observatory never closes.**

One organ, two rhythms:

- **Offline (gate the merge)** — an eval suite becomes infrastructure on the day it can **block a merge.** Every PR runs the gold-set regression (deterministic assertions plus pinned judge metrics); a larger suite runs nightly; a refresh runs weekly.
- **Online (drive improvement)** — canaries score live traffic with **implicit signals**: **a rewrite is a downvote, a copy-paste into an email is an upvote, closing the tab is voting with your feet.**
- **The ratchet** — every production failure becomes a **permanent, versioned test case** the gate rejects forever after.
- Passing offline while sliding online: **that divergence is itself a metric — the world is leaving your test set.**

### Drift: the slow emergency

Generation stays fluent while retrieval starves. Over months, structured tasks stay stable while **RAG tasks drift 25–75%**, with the drift concentrated in retrieval-coupled paths.

**The default move: the domain-classifier bet** (really a classifier two-sample test — if a classifier can separate the two populations, the distributions differ, and AUC is the effect size):

1. At launch, freeze the embeddings of **1,000–5,000** queries as class 0 = reference (**and leave them frozen**);
2. Sample an equal number of live embeddings this week as class 1;
3. Train a **simple** classifier (logistic regression / small MLP / GBDT) to separate them, with cross-validation;
4. Read the AUC — **≈ 0.5 means no drift (the bet you want to lose); > 0.6–0.7 raises an alarm**;
5. Run it daily or weekly, plot AUC over time, set a threshold;
6. On alarm: find which queries look most like class 1 (new topics, new user segments) → re-measure Recall / nDCG on the drifted slice → refresh the eval set, re-embed, or rebuild the index.

Notes: keep the two sample sizes matched · use the **same embedding model** for reference and live · keep the reference frozen long enough to detect slow drift · **it tells you something changed, not whether it got better or worse** (go back to retrieval metrics to find out).

> This is Act I's **eval decay, fitted with a needle** — read daily, rather than discovered at the post-mortem.

### Shadow / Canary / Interleave

- **Shadow** — mirror traffic without serving it; compare judge win rate, cost, latency, and retrieval overlap (Jaccard). **The most cost-effective diagnostic for an index-rebuild migration.**
- **Canary** — 1–10% of traffic behind pre-registered gates, with automatic rollback and the old index kept warm.
- **Interleaving** — blend two rankers' results into one session and credit by clicks; **detects the same preference with 10–100× less traffic** (an afternoon instead of ten days).

### The CFO metric

Cost per correct answer: `5¢/query × 78% correct = 6.4¢ per correct answer`; `40¢ × 88% = 45¢` — paying 7× for 10 points of quality is a judgement the x-axis cannot make for you.

> **You are buying correct answers, not queries. Do the division first, then compare.**

### Closing the triangle

Red-teaming becomes a regression suite in CI, scored **in pairs** (attack success rate plus benign false-positive rate) — because the cheapest way to drive ASR down is **over-blocking**, paid for by legitimate queries.

The maturity metric is **time-to-detection for a novel attack pattern** — one number an attacker cannot Goodhart on your behalf.

---

## Coda: The Evaluation Map — Reading the Dashboard Under Pressure

> **Every component has a failure mode, every failure mode has a metric, and every low score is a diagnosis — a ticket.**

From a red dashboard to the cheapest next step:

| Symptom | Diagnosis | Action |
|---|---|---|
| **NDCG low but answer FActScore high** | the generator is coping; **the reranker is starving it** | fix the reranker |
| **Faithfulness low, context recall high** | **the generator's fault** | retrain / fine-tune / replace (prompt engineering won't save it) |
| **Context recall low** | the evidence never arrived | fix chunking / retrieval (downstream cannot compensate) |
| **ECE high** | the confidence is dishonest | temperature-scale the confidence head / regress verbalised confidence on a calibration set |
| **Negative rejection low** | it answers when it should abstain | tighten the **request gate and grounding strictness** (Week 06's two dials) |

### The deepest metric

Not faithfulness, not NDCG, but the one from the opening — **does it know what it doesn't know?**

> 95% faithfulness with 20% NRR sounds glorious **right up until it meets the one question it cannot answer and lies.** In a courtroom, a hospital or on a trading desk, that lie is the only metric that matters.

**The last word belongs to the user:**

> The measure of a system is not its **best performance on a curated benchmark** but its **worst performance on a query nobody anticipated** (NPS, satisfaction, thumbs).
> **Build the eval set to find those queries before your users do.**

### Three reference stacks

| Stack | Contents |
|---|---|
| **The seminar stack** (one weekend, $0) | pytrec_eval + RAGAS + RAGChecker on 20 sampled failures + a hand-rolled risk–coverage curve — every concept in the course, on one laptop |
| **The startup stack** (lean, self-hosted) | Langfuse for tracing + promptfoo gating merges + MiniCheck per claim + RAGET-seeded question bank (rewrites plus injected unanswerables) + Phoenix/Evidently for drift |
| **The regulated-enterprise stack** | everything self-hosted and version-pinned · PPI-certified intervals against a standing human audit sample · conformal abstention recalibrated quarterly |

> **Tools are opinions frozen into software. Validity is decided by the judge, not the library.**

### How the five load-bearing papers form one system

```
RAGAS (what to measure, module by module)
  → FActScore (is each atomic fact reliable — the 58% wake-up call)
  → RGB (the generator's four capabilities)
  → On Calibration of Modern Neural Networks (Guo et al., ICML — the theoretical root of ECE, temperature scaling, reliability diagrams)
  → Prometheus 2 (an open local judge, for scale)
```

**Remove any one and it leaks.**

---

## Closing: Holding Kelvin and Cameron Together

- **Kelvin:** you only know it once you measure it — without measurement you are changing things on instinct.
- **Cameron:** not everything that counts can be counted — an all-green dashboard can still miss a fatal long-tail error, a misleading tone, or over-confidence at the critical moment.

The engineer stands between them:

> **Build the ruler → evaluate layer by layer → evaluate the judge itself → and, more important than every metric on the wall, build a system that knows when it does not know.**
>
> **The danger was never that the system doesn't know. It is that it doesn't know and still sounds completely certain.**

---

## What to take away

1. **Measure the measurer first.** Your judge has a personal equation, and it is **non-stationary** — pin the version, freeze a calibration set, alarm on κ drift > 0.05.
2. **Correct ≠ grounded.** A factually right but unsupported answer is a grounding failure, and any "is the answer right?" check will pass it.
3. **Reject judges with κ < 0.6.** Raw agreement is fooled by class imbalance (75% agreement can be κ = 0.375).
4. **A jury beats a bigger judge** — three heterogeneous small judges reach κ 0.763 vs a single GPT-4's 0.627, at 1/7 the cost.
5. **Small verifiers first** — MiniCheck reaches GPT-4 accuracy at ~1/400 the cost; reserve the frontier judge for dimensions nothing specialised covers.
6. **Read faithfulness alongside answer relevancy and noise sensitivity** — a grounded non-answer fools the first, and the most faithful models are the most easily misled by noise.
7. **Abstention is a dial, not a switch** — find the operating point on a risk–coverage curve, and always report NRR together with the over-rejection rate. Regulated deployment threshold: NRR > 70%.
8. **Customer-facing agents report pass^k, not pass@k** — 70% per run leaves 29% across three consecutive customers.
9. **Shipping is not the end of evaluation** — offline gate + online implicit signals + a daily domain-classifier drift probe (AUC ≈ 0.5 lets you sleep) + a failure ratchet.
10. **Divide before you compare on cost** — you are buying correct answers, not queries.

---

## Positioning in one sentence

Last week we measured retrieval; this week we measure **the generator itself, and the world after launch.** The chain: RAGAS (the floor) → FActScore / ALCE (claims and citations) → Judge 2.0 + the four RGB capabilities → NRR / ECE / risk–coverage (epistemic humility) → multi-hop, evolving test sets and trajectory evaluation → the Observatory (offline gate + online drive + drift + ratchet), with the Evaluation Map wiring every low score back to where the next engineering hour should go.

**The thesis is unchanged: you cannot improve what you cannot measure. And the deepest metric is whether it knows what it doesn't know.**
