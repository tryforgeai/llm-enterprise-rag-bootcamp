# Week 07 Summary — The Measure of All Things: Evaluating RAG from Retrieval to Reasoning

**Date:** 2026-07-25 · **Source:** `course/week_07/summer-week-7-lesson-plan.pdf` (*The Measure of All Things — Evaluating RAG Systems from Retrieval to Reasoning*, Asif Qamar, SupportVectors), live slide notes, and the Week 07 runnable demos (`course/week_07/ndcg_demo.py`, `pr_curve_demo.py`, `rerank_eval_demo.py`)

---

## TL;DR

The whole week compresses into one sentence:

> **You cannot improve what you cannot measure — and the yardstick is yours to build, not someone else's.**

For six weeks we have been **building**: Weeks 1–2 laid down "meaning as geometry" and the retrieval foundations, Week 3 chunked, Week 4 manufactured derivative artifacts, Week 5 turned the library into a city, Week 6 hung two gates on the door. One question was never asked rigorously: **does any of it work?**

The live subtitle said it best:

> *"Six weeks of building the library, the map, and the gates. Today we stop building — and start measuring."*

The crucial reframing: **evaluation is not the last step of the pipeline. It is the foundation every prior week has been resting on, unexamined.**

> *"A bridge engineer does not hand off load-testing — the load curves **are** the design. Evaluation is not downstream of AI engineering. **Evaluation is AI engineering.**"*

The whole day hangs on one equation:

```
argmax_θ  E_{q∼𝒬} [ μ(q, θ) ]
```

- **θ** = *every* knob — chunk size, embedder, retrieval mix, reranker, prompt, temperature. Not just model hyperparameters: the whole pipeline's architectural decisions.
- **μ(q, θ)** = a metric of goodness on query q.
- **𝒬** = **your own** query distribution — not someone else's benchmark.

The equation anchors all four acts: Act I builds **𝒬** (the gold dataset), Acts II–III define **μ** (six retrieval metrics plus generation metrics), Act IV warns that **μ, once on a wall, gets arbitraged** (Goodhart).

The day's shape:

```
Prologue  why measure at all       (whose job, the 80/20, the optimisation goal)
Act I     The Yardstick            (the gold dataset — ground truth before any metric)
Act II    The Staircase            (six retrieval metrics, each fixing the one below)
Interlude Signal & Noise           (significance, public benchmarks, diversity and MMR)
Act III   The Generator            (from judging the pantry to judging the chef)
Act IV    The Frontier             (calibration, multi-hop, agentic, Goodhart, cost)
Coda      The Evaluation Map       (wire every metric back to every prior week)
```

Two epigraphs frame the tension, and **you must hold both**:

> *"When you can measure what you are speaking about and express it in numbers, you know something about it."* — Kelvin, 1883
> *"Not everything that counts can be counted, and not everything that can be counted counts."* — Cameron, 1963

> Live framing: **"Today is Kelvin's day — but Cameron stands behind him all day, warning us about Goodhart."**

---

## Prologue: Whose Job Is Evaluation?

Three slides to break one mistaken belief.

**"Evaluation? That's QA's job."** — a pattern watched for twenty years: teams of senior engineers nod through this exact lecture, build RAG systems for months, then confess with genuine surprise: **no gold dataset ever got built.**

A useful metaphor for why the knowledge doesn't stick:

> *"The formulas do not leak out of heads because people are lazy. They leak because they were filed in the mental cabinet marked **someone else's concern** — and that cabinet leaks. Fix the drawer, and the concepts stay."*

**Why the old mental model fails here:**

| | Deterministic software | AI systems |
|---|---|---|
| Behaviour | same input, same output | a **distribution of answer quality** over a **distribution of queries** |
| Verdict | QA writes assertions; CI goes red or green | **no clean pass/fail line** |
| Drift | none | model version, prompt, stochastic decoding, corpus growth |

**The 80/20 of real AI work:** 80% of the effort goes to clean data, demonstrations, and the yardstick; 20% to the fashionable part — architecture, algorithm, model. At Cornerstone (100 million learning objects, 7,000 clients) the architecture was clear in the first meeting; the months went into **40 SMEs, 2 days each, a 10,000-query gold dataset.**

A counter-intuitive signal worth keeping:

> When hybrid search launched, one big client was **furious**: why does it work now, after years of complaints? **There is no better sign that your evaluation methodology is real than an angry client who finally sees the improvement.**

---

## Act I: The Yardstick — Ground Truth Before Any Metric

The milestone slide uses the periodic-table symbol **"Au"** — a pun on *gold dataset*.

> *"Before any metric, a gold dataset. Before any number, a ground truth **someone signed their name to**."*

"Someone signed their name to" is the live addition: it pins ground truth from an abstraction to something **a specific person vouched for and is accountable for**.

### What the gold dataset is

A curated set of queries **𝒬 = {q₁, …, qₙ}**, each annotated with its relevant documents and a **graded relevance score per pair — r ∈ {0, 1, 2, 3, 4}**, from irrelevant to perfect.

That 𝒬 is the same 𝒬 as in `E_{q∼𝒬}` above — **the gold dataset is your query distribution, instantiated.**

> *"Every retrieval metric we compute today **presupposes** this artefact. The notches on the ruler are the metrics; the ruler itself is the gold dataset."*

### The first way: watertight and unaffordable

Throw 1,000 queries at the engine; human evaluators tick-mark every returned result; for recall, separately list what **should** have come back.

Two knives kill it:

1. **Cost** — "nobody in a seven-engineer pod has time for it. The engineers will say: my job is to write code, not read a million documents. **They are right.**"
2. **Pathology (subtler, and more important)** — you planted ten beautiful articles as truth; the engine surfaces an even **better** one you never catalogued. It isn't in the answer key, so it counts as irrelevant, and **precision drops. The engine is penalised for doing its job.**

### The second way: the cherry-picked gold dataset (five steps)

1. **Hire SMEs, not engineers** — clinicians for medicine, professors for learning, compliance officers for finance. (Engineers will revolt.)
2. **SMEs author the queries** — from real intent: search logs, support tickets, real research. Not invented.
3. **Run a simple engine** (OpenSearch, whatever is at hand); take **top 100–200** candidates per query.
4. **Cherry-pick the best 25–30** of those 200 and **grade them 0–4**.
5. **Freeze at release; version; evolve** — add queries, adjust grades, retire stale ones.

> *"No human can scan a corpus. Anyone can scan two hundred candidates."*

The trick is in steps 3–4: **a simple engine cuts a million documents down to 200, turning impossible exhaustive annotation into a tractable scan.** The price is that recall's denominator is no longer "the truth of the whole corpus" but "the truth within these 200 candidates" — this is standard IR **pooling** (what TREC does). Theoretical completeness traded for practical feasibility. **Say so explicitly when you report the number: this is pooled recall, not absolute recall.**

### Size: minimum 200, shoot for 1,000

The "SME Summit" is the seed — gather 5–10 experts, buy breakfast and lunch, give them 8 hours, come out with ~100 debated graded judgements, then grow it over six months.

That number gets retroactively justified by statistics in the Interlude (power analysis, below).

### Two ways the ruler rots

- **Eval decay** — the corpus evolves; January's most-relevant document is superseded in June. **Stale judgements quietly poison every metric.** Refresh on a schedule.
- **Overfitting your own yardstick** — if engineers know the queries, even implicitly, they optimise for **those** queries. Keep a **held-out test set that only the evaluation lead controls.**

> *"A yardstick everyone has memorised is no longer a yardstick — **it is a target**."* (Goodhart returns in Act IV.)

### Against borrowing public benchmarks

> "MS MARCO is right there — let's evaluate on that." This is **testing a medicine on fever patients when your patients do not have fever.** Brilliant on the benchmark, catastrophic on your users.

The core argument is **distribution mismatch**: a public benchmark has its own 𝒬′. The θ that maximises on 𝒬′ may be exactly wrong on your 𝒬.

But this is **not a blanket rejection** — public benchmarks have one legitimate use: a **sanity check** of baseline competence. A thermometer calibration, not a proof of efficacy.

The logicians-on-a-train metaphor is the sharpest version: seeing a white sheep, they will only say *"there exists at least one sheep, on at least one side of its body, that appears white at the moment of observation."* **Public benchmarks license only that kind of claim.**

### Quiz 1: the asymmetry of the two halves

> Precision can be computed by tick-marking what the engine **returned**. Recall cannot. What extra knowledge does recall demand — and why is it so much more expensive?

**Answer: the expense is in the denominator.**

- **Precision**'s denominator is what the engine returned — a **closed, finite** set, sitting right in front of you.
- **Recall**'s denominator is **every relevant document in the corpus**, including what the engine never showed you. That is an **open** problem.

$$\text{Recall@}k = \frac{|\text{relevant in top }k|}{|\textbf{all relevant in corpus}|}$$

> *"Precision judges the bucket. Recall judges the bucket **against the beach** — and only the ground truth knows what the beach holds. That catalogue is the expensive artefact of Act I."*

This is why industry reports precision and nDCG freely but dodges absolute recall: recall's true value is essentially unobtainable on an open corpus, and can only be approximated within a frozen gold dataset.

---

## Act II: The Staircase — Six Retrieval Metrics

The milestone uses **"nG"** for nDCG.

> *"Six metrics, each fixing a blindness of the one below — from a bucket on a beach to the summit called NDCG."*

### Two metaphors run through the act

**Two children on a beach (precision / recall):** a bag of seashells thrown on the sand, some **buried**; each child gets a bucket: *go get me ten seashells.* Sarah returns 4 shells and 6 pebbles; Meera returns 7 shells and 3 pebbles. Meera did better — everybody says so. But **how much better, numerically?**

> A query partitions the corpus into seashells (relevant) and pebbles (not). The search engine is the child with the bucket, asked for its top k.

**Ali Baba's cave (rank awareness):** an aisle into the dark, shelves in order = ranks, treasure mixed with junk, and **the thieves may return — time is at a premium.**

### Metrics 1–2: Precision@k and Recall@k

**Precision's two blind spots:**

1. **Cutoff-sensitive** — ask for twenty shells instead of ten and the ranking can **reverse**. A single precision@k is not stable.
2. **Blind to the sand** — a pristine bucket of three, with seven shells still buried, scores a perfect 1.0.

**Recall** mnemonic: **R**ecall emphasises **R**elevance — all of it. Bury five blue shells, find three → 3/5 = 0.60.

The lecture hammers recall with three metaphors (beach, Rookie the golden retriever, and a neuropsychologist's test) because recall's defining property — *the denominator is everything relevant, and must be known in advance* — is the least intuitive. The third is the best: the lecturer's daughter, a clinical neuropsychologist, plants facts casually early in a conversation and asks two hours later what he remembers. **Testing the memory of ageing parents and testing a search engine's retriever are the same metric.**

### Three hard properties of k

With **n = total relevant, k = your cutoff**:

- **Ceilings** — if `k < n`, perfect recall is unreachable; if `n < k`, perfect **precision** is unreachable (max **n/k**).
- **Crossover** — at exactly `k = n`, perfect precision and perfect recall can coincide.
- **One-way street** — **recall is monotonically non-decreasing in k**: one more scoop may add a shell or a pebble, but never removes a shell already in the bucket.

> *"This is why retrieval sets k generously."*

**That one-way street is the mathematical basis of the two-phase architecture:** phase one only has to not miss (big k maximises recall); phase two only has to order well (the reranker lifts nDCG). The division of labour falls out of recall and precision reacting to k in opposite directions.

**When recall is the master:** in legal RAG, missing the one precedent that wins the case is catastrophic — **better 50 noisy documents with every precedent inside than 5 pristine ones missing the one that matters.** In medical RAG, a missed drug interaction can harm a patient.

### Quiz 2: ceilings, with numbers

> n = 10 shells buried. The child returns k = 20 items, of which 7 are true shells. (a) Precision@20? (b) Recall@20? (c) The **best possible** Precision@20?

**Answers:** (a) 7/20 = **0.35**; (b) 7/10 = **0.70**; (c) **10/20 = 0.50** — only ten shells exist in the world and the bucket has twenty slots, so ten slots are necessarily pebbles.

**Teaching point: a low Precision@k does not necessarily mean a bad system — k may simply exceed the number of relevant documents.** This child's 0.35 is already 70% of a theoretical ceiling of 0.5. **A precision number read in isolation will mislead you.**

### F1: the harmonic mean

$$F_1 = 2 \cdot \frac{P \cdot R}{P + R}$$

Return one always-relevant document: **P = 1.0, R = 0.1 → F₁ ≈ 0.18** (the arithmetic mean would give a comfortable-looking 0.55). Balanced at P = R = 0.5 → F₁ = 0.5. **The harmonic mean punishes imbalance: you cannot buy your way to a good F₁ with one perfect half.**

> *"Precision and recall are two **adversarial masters** — return the whole corpus for perfect recall, or one sure document for perfect precision; both are useless. Quote them **together**, always."*

### Why the staircase must keep climbing

Precision, recall and F₁ share two blindnesses:

- **Not rank-aware** — relevant docs at positions 1, 2, 3 score identically to positions 48, 49, 50.
- **Not grade-aware** — a Feynman Lectures chapter and a dry handbook entry both count as "relevant."

> *"Users do not read result lists uniformly. As the old search joke goes: governments hide their secrets on **page two** of the search results. Nobody ever visits."*

**Two blind spots = two directions of upgrade.**

### Metric 3: MRR — Ali Baba needs one jewel

$$MRR = \frac{1}{|Q|}\sum_{q\in Q}\frac{1}{r_q}, \qquad r_q = \text{rank of the first relevant result}$$

Rank 1 → 1.0; rank 3 → 0.33; rank 10 → 0.1; rank 100 → 0.01 (the system is essentially not helping).

**The key property: the penalty is convex.** Rank 1 → 2 halves the score; rank 10 → 11 barely registers.

> *"All the metric's sensitivity lives in the early ranks — exactly where the user's patience lives."*

**When to reach for it: navigational queries** — "what is the returns policy?" — one specific answer wanted; if result 1 is right, result 2 is unnecessary. Google, Amazon and internal search are dominated by navigational intent. Rule of thumb: **MRR > 0.3 roughly means the first relevant hit is typically in the top 3.**

**MRR's confession: Ali Baba does not take inventory.** Ten relevant documents in the corpus? MRR **cannot distinguish** the system that found one from the system that found all ten in a row — both have their first hit at rank 1, both score 1.0. For a user who wants to read them all, that is fatal.

### Metric 4: MAP — the greedy brother

Qasim is not content with the first jewel. He wants **every** diamond — **as early in his walk as possible.** He is the user doing research.

$$AP_q=\frac{1}{m}\sum_{i=1}^{m}\frac{i}{r_i}, \qquad MAP=\frac{1}{|Q|}\sum_q AP_q$$

> at the i-th relevant doc you've seen i treasures in r_i shelves — that ratio is precision at that moment of joy

The name is an average of averages ("mean mean precision would be correct but ugly"). Ideal day: four treasures on the first four shelves. Bad day: the same four at ranks **1, 4, 12, 37** — identical recall, wildly different AP.

**MAP's residual blind spot: still binary relevance** — it cannot tell rel=4 from rel=1.

### Metric 5: AUC-PR — the rare-needle metric

**Why not ROC:** ROC is signal-processing heritage — voltages down a noisy line. For RAG corpora it is the **wrong curve**: relevance is vanishingly rare (six documents in a million), so FPR's denominator is in the millions and **the false-positive rate looks angelic by default.**

> *"A trivial retriever that returns the empty set has a false-positive rate near zero — and looks superb on ROC. **Class imbalance is the assassin of ROC.**"*

The **PR curve**'s two axes (precision, recall) contain **no "ocean of irrelevant documents" denominator**, so it stays sensitive to a rare positive class.

- the careful child: precision stays high as recall climbs to 1.0 → **AUC-PR ≈ 0.86**
- the clumsy child: precision falls off a cliff immediately → **AUC-PR ≈ 0.32**
- the random baseline = **the base rate of relevance** (not 0.5)

**When to reach for it: whenever the positive class is rare relative to the corpus** — enterprise RAG, fraud detection, security events, recommenders.

> *"AUC-PR is the continuous generalisation of MAP, and it stays honest as your corpus grows — unlike ROC, it is not inflated by oceans of true negatives."*

### Metric 6: nDCG — the summit

**The jewels acquire prices:** rock 0, silver 1, gold 2, **diamond 4**. A diamond at rank 1 beats a silver at rank 1 — and both beat a diamond buried at rank 20, because the deeper Ali Baba walks, the higher the risk. **The same diamond is worth less the deeper it is found.**

> *"Double sensitivity — to **what** you find and **where** you find it. Our graded scores r ∈ {0,…,4} finally earn their keep."*

That last clause reaches back to Act I: the 0–4 grades the SMEs painstakingly assigned were used by none of the first five metrics, which are all binary. **nDCG is the first metric to actually use them** — which is why Act I insisted on 0–4 rather than 0/1.

**Read it inside-out: gain → cumulate → discount → normalise**

$$nDCG@k = \frac{DCG@k}{IDCG@k}, \qquad DCG@k = \sum_{i=1}^{k}\frac{2^{rel_i}-1}{\log_2(i+1)}$$

| Layer | Formula | What it does |
|---|---|---|
| **Gain** | `2^rel − 1` | the worth of the jewel — **exponential** in its grade |
| **Cumulative** | `Σ` | the knapsack total after k shelves |
| **Discounted** | `/ log₂(i+1)` | the deeper the cave, the less the same jewel is worth |
| **Normalised** | `/ IDCG` | divided by the best possible day in this cave |

**The gain layer is exponential by design:** rock 0 → 0; silver 1 → 1; gold 2 → 3; diamond 4 → **15**. **A diamond is fifteen times a silver, not four** — the exponential bakes in the intuition that top-tier relevance matters disproportionately.

> ⚠️ **Engineering trap: two conventions coexist.** Järvelin–Kekäläinen (2002) used linear gain `rel`; Burges (2005)'s `2^rel − 1` is the modern default (scikit-learn, pytrec_eval). **Check the formula when reading older papers — numbers do not compare across conventions.**

**The discount layer, with the best metaphor of the day:**

> *"I am willing to promise anyone a **million dollars on their 200th birthday** — you realise the present value is not much. The diamond at rank 20 is the same promise; log₂ writes the discount schedule."*

The logarithm is **gentle at the top of the list, harsh at the bottom**: rank 1 divides by 1 (no discount), rank 2 by 1.585, rank 20 by ~4.39. The **+1** spares position 1 a divide-by-zero.

**Three benefits of normalising:** perfect ranking = 1.0 (a clear ceiling, easy to read); every query lands in [0, 1] (comparable); averages cleanly across queries (unlike raw DCG, which is skewed by queries with more relevant documents). That is why it can serve as the cross-query headline metric.

### Quiz 4: compute nDCG by hand

> Relevance grades down the ranked list: **[0, 1, 0, 2, 1]**. Compute DCG, IDCG and NDCG at k = 5.

$$DCG = \tfrac{0}{1} + \tfrac{1}{1.585} + \tfrac{0}{2} + \tfrac{3}{2.322} + \tfrac{1}{2.585} = 0.631+1.292+0.387 = \mathbf{2.310}$$
$$IDCG_{[2,1,1,0,0]} = \tfrac{3}{1}+\tfrac{1}{1.585}+\tfrac{1}{2} = 3+0.631+0.5 = \mathbf{4.131}$$
$$NDCG = \tfrac{2.310}{4.131} \approx \mathbf{0.56}$$

> *"The gold at rank 4 is the tragedy: moved to rank 1, it alone contributes 3.0 instead of 1.29. One transposition, and NDCG jumps — **this is the number your reranker is paid to move.**"*

**0.56 = "a mediocre day, precisely measured."** Subjectively "fine"; objectively, 56% of what this set of documents could have delivered. That welds evaluation (Week 7) to the repair action (the reranker, Weeks 1–2) in one sentence.

(`course/week_07/ndcg_demo.py` reproduces it exactly: DCG = 2.310, IDCG = 4.131, nDCG = 0.559.)

### The most practical page of the week: the minimal diagnostic pair

| Symptom | Diagnosis | Action |
|---|---|---|
| **NDCG low, Recall high** | the documents are found but badly ordered | **fix the reranker** |
| **NDCG low, Recall low** | the documents are not found at all | **fix retrieval** — chunking, embedder, hybrid mix |
| **NDCG high, Recall high** | retrieval is healthy | celebrate, and move to Act III |

> *"If you have time for one number, make it NDCG. The other five are diagnostics — the footholds you consult when the summit number moves the wrong way. Both computable at every build; **the delta between builds is where improvement lives.**"*

**That last clause is the essence of continuous improvement:** the absolute nDCG matters less than the change after each modification.

### Quiz 5: the morning stand-up

> Your dashboard this morning: **Recall@50 = 0.91 (healthy), NDCG@10 dropped from 0.71 to 0.55 overnight.** A teammate proposes re-chunking the corpus. Is the teammate right?

**Answer: no.** Recall@50 = 0.91 says the relevant documents **are being found** — retrieval is not broken. Re-chunking is surgery on a healthy organ.

> *"The shells are in the bucket — **badly stacked**. Re-chunking attacks the wrong stage. Inspect the **reranker** first — a bad deploy, a version drift, a broken feature. The diagnostic pair just saved you a week of re-chunking a healthy corpus."*

**"Overnight" is the key clue** — a sudden change usually comes from a specific event (a deploy, a model update, an index rebuild), not slow data drift. Start with "what changed last night."

**The value of this page is not academic precision; it is not spending a week of engineering on the wrong stage.**

### The whole act in one picture

| Step (low → high) | In a sentence | Nature |
|---|---|---|
| **Precision@k** | purity of the returned set | binary · position-blind |
| **Recall@k** | completeness against the beach | binary · position-blind |
| **MRR** | how fast the first treasure | first hit only |
| **MAP** | all relevant docs, and early | rank-aware · still binary |
| **AUC-PR** | the whole trade-off curve | robust to rare positives |
| **NDCG** | graded gain, discounted by depth | rank-aware · graded |

> *"Two systems can share an NDCG and differ wildly in MRR."*
> — which is exactly why the other five are kept as diagnostics: the same headline number can hide very different failure modes.

---

## Interlude: Signal & Noise

The visual is **σ**.

> *"A 1.2-point improvement on 200 queries may be nothing at all. Before you celebrate, ask the statistics."*

### Public benchmarks, in their proper place

- **BEIR** — 18 datasets, 9 task types, headline metric NDCG@10. Biggest surprise: **BM25 (pure sparse) still beats dense retrievers on many out-of-domain tasks** — which is the hard evidence behind the enterprise default of **hybrid** retrieval.
- **MTEB** — 58 datasets; the leaderboard most cited when **choosing an embedding model**.
- **MS MARCO** — the classic passage-ranking benchmark, the base of the TREC-DL track.

> *"The deployment gate needs both: pass **your** gold-dataset threshold, and place respectably on the public boards. The first says it works for your users; the second says it is not inexplicably broken."*

### Power analysis closes the loop

> To detect a **1-point** absolute NDCG improvement with **80% power at α = 0.05** typically requires **N ≈ 500–1,000** queries.

**Act I's "shoot for 1,000" was never arbitrary — the SME summit was doing power analysis without naming it.**

Both directions have a trap:

- **Too small (< 200)** → underpowered; real improvements drown in noise and get discarded as useless.
- **Too large** → **trivial improvements become statistically significant.**

> The practical enterprise threshold: **0.02–0.05 absolute NDCG** is worth engineering effort. Below that, **statistical significance is not practical significance.**

Method: **paired bootstrap / permutation test.**

### The seventh dimension all six metrics miss: diversity

$$MMR = \arg\max_{d\in R\setminus S}\Big[\lambda\,\text{Sim}_1(d,q) - (1-\lambda)\max_{d'\in S}\text{Sim}_2(d,d')\Big]$$

**Ten near-duplicates can score perfect precision, recall and NDCG** — and serve a poor experience: homogeneous evidence, **an illusion of consensus that is really redundancy.** MMR picks each next result by relevance **minus** similarity to what is already picked.

Practical numbers: λ = 1 is ordinary top-k; **production λ ∈ [0.5, 0.8]**; diversity-aware retrieval lifts **multi-hop answer quality 6–12%**; but **λ < 0.3 hurts simple factoids.** Tune λ on the gold set; score diversity with **α-NDCG**.

**Again: tune by query intent** — multi-hop wants diversity, factoids want precision.

---

## Act III: The Generator — From Judging the Pantry to Judging the Chef

> *"The ingredients do not make the meal. Six metrics judged the pantry; now we judge the chef."*

**Why this is the pivotal turn:** even with perfect retrieval (nDCG = 1.0), the LLM can still ignore the evidence, fabricate, answer a different question, or cite the wrong source. **Retrieval metrics are blind to all of it** — they only judge what was handed to the LLM, never what the LLM made of it.

### RAGAS: four metrics and their limits

Four metrics: **faithfulness** (the generation-side counterpart of Week 6's response-side grounding), **answer relevancy** (reverse-generate n synthetic questions from the answer, measure cosine similarity to the original), **context precision**, **context recall**.

**Limits — do not treat it as the sole arbiter:**

1. **No claim-level granularity** — "Einstein was born in Ulm, in 1879, and won the Nobel in 1921" is one sentence containing 3+ independently falsifiable claims. If most sub-claims are supported the whole sentence passes, and **one wrong claim rides along free.**
2. **Scores are unstable across evaluator models** — GPT-4, Claude and Llama disagree, and vendors update models quietly mid-flight.
3. **No attribution verification** — it checks consistency with the context, not whether each claim cites the **right** passage.
4. **Evaluator pinning** — always pin the judge to a dated checkpoint; maintain a frozen, human-verified calibration set of 50–200 items and re-run it periodically. **If Cohen's κ drifts by more than 0.05, the evaluator has changed.**

**Verdict: use RAGAS as a diagnostic baseline — a floor no RAG system should fall below — not as the sole arbiter of quality.**

### Claim-level entailment: FActScore and ALCE

The most important advance in generation evaluation is **from answer level to claim level.**

- **FActScore** (EMNLP 2023): decompose the answer into atomic facts and verify each. ChatGPT-generated biographies score a **FActScore of just 58%** — nearly half of the atomic claims unsupported.
- **ALCE** extends this to citation quality: **citation accuracy of 40–75%**, i.e. roughly **one in three citations is wrong or missing**, even when the answer is correct. In enterprise settings citation accuracy is a **deployment gate.**

> **"A footnote that does not hold up is worse than no footnote at all."**

### LLM-as-a-Judge 2.0

Evaluation is a specific task and deserves a **purpose-built judge** rather than a rented frontier model. **Prometheus-2** (EMNLP 2024, open-source, runs locally): direct scoring against a user rubric plus pairwise ranking; **72–85% agreement with humans.**

**Four judge biases:** position, length, self-preference, and style over substance.

**Alignment with humans must be measured with Cohen's κ** (Landis–Koch: 0.41–0.60 moderate, 0.61–0.80 substantial). **Enterprise RAG rejects any judge with κ < 0.6.** Also: Kendall's τ for rank agreement, Krippendorff's α for multiple judges.

**Three iron rules for judges:**

1. the judge must be from a **different model family** than the generator;
2. for pairwise comparisons, **run both orderings** and average;
3. **never trust a single judge** — cross-validate with a second and spot-check by hand.

(A chain-of-thought judge adds 8–12 points of agreement at 3–5× the token cost — cheap judges for continuous monitoring, CoT judges for periodic deep checks.)

### The four RGB capabilities RAGAS cannot measure

The RGB benchmark (AAAI 2024) identifies four capabilities a RAG generator must have:

- **Noise robustness** — can it ignore documents that are topically related but contain no answer?
- **Negative rejection** — can it abstain when there is no answer?
- **Information integration** — can it synthesise across documents?
- **Counterfactual robustness** — can it spot a factual error in a retrieved document? (e.g. one document says port 480 while the rest say 48 — does it flag the contradiction or follow the context blindly?)

---

## Act IV: The Frontier

1. **Knowing when to say "I don't know"** — **ECE (Expected Calibration Error)**: the weighted gap between accuracy and confidence within each confidence bin. Perfect is 0; modern LLMs run **0.05–0.15**; **instruction tuning often makes it worse** (it raises confidence without raising accuracy). Pair it with a reliability diagram.
   > The lecturer's provocation: "I have never seen an enterprise RAG system honestly say 'I don't know'." Try the **Calabi–Yau test** — ask a switchgear manufacturer's RAG about Calabi–Yau manifolds.
2. **Multi-hop and synthesis** — classic metrics judge each retrieval independently and cannot measure integration. Benchmarks: HotpotQA / MuSiQue / 2WikiMultihopQA / **MultiHop-RAG** (the last provides a ground-truth evidence chain per hop, so you can score the **path**, not just the endpoint).
3. **Auto-evolving test set generation** — Giskard RAGET, DeepEval (a RAGAS superset plus G-Eval). The evolutionary angle: mutate seed questions into harder variants — add constraints, require multi-hop, inject distractors, flip the expected answer (to test negative rejection), add ambiguity (to test disambiguation).
4. **Agentic / trajectory evaluation** — agents plan, retrieve, call tools and iterate; scoring only the endpoint is dangerous. Three layers: end-to-end (correctness, satisfaction), trajectory quality, and **node-level precision** (at each decision point: right tool? well-formed query? sound reasoning step?). **The diagnostic power lives in the third layer.**
5. **Goodhart's Law — the most important warning of the day.** Once a metric goes on a wall, people optimise for it: *"when a measure becomes a target, it ceases to be a good measure."* RAG-specific reward hacking:

   | Optimise only for | What the system learns to arbitrage |
   |---|---|
   | faithfulness | **over-hedging** — "it is possible that…", technically faithful and useless |
   | citation recall | **over-citation** |
   | a length-biased judge | **over-writing** |
   | a judge from the generator's own family | **collusion** |

   **Defences:** metric ensembles, adversarial eval, red-teaming the metric itself, and **a held-out golden judge that is never used for training** (reserved for drift detection).
6. **Cost** — a frontier judge scoring 10,000 queries costs **$500–2,000 per run**; a self-hosted open judge on your own GPUs is near-zero marginal cost. **A 7B judge fine-tuned on 5,000 domain annotations beats prompted GPT-4 on in-domain agreement.**

---

## Coda: The Evaluation Map — Wiring Metrics Back to Six Weeks

The lecturer promoted this from a PDF appendix to a standalone **Coda** — connecting metrics back to each week's components is the deliberate finale, not a footnote.

| Component (week) | Failure mode | Metric |
|---|---|---|
| Embeddings & retrieval (W1–2) | poor retrieval quality | Recall@K, Precision@K, MRR, MAP, nDCG |
| Reranking (W2) | relevant results buried | precision, **nDCG** |
| Chunking (W3) | relevant information severed | context recall, information integration |
| Derivative artifacts (W4) | is the understudy worth it | Recall@K / context precision (before vs after) |
| GraphRAG & multi-hop (W5) | cross-document reasoning | information integration, multi-hop benchmarks |
| The two gates (W6) | request gate → noise; response gate → abstention, faithfulness | noise robustness; **FActScore** (the claim–evidence graph is the mechanism, FActScore is the metric) |
| Whole pipeline (this week) | end-to-end | answer correctness, satisfaction, ECE |

**The caveat on the last row:** end-to-end metrics capture the whole picture but **do not localise failure** — only component-level metrics do that.

---

## Eval artifacts produced this week

Three runnable demos in `course/week_07/`:

| File | What it does |
|---|---|
| `ndcg_demo.py` | unpacks nDCG layer by layer (gain / discount / contribution); reproduces Quiz 4's 0.559 |
| `pr_curve_demo.py` | PR curve and AUC-PR (approximated via Average Precision) |
| `rerank_eval_demo.py` | retrieval → reranker → metrics loop, with a `diagnose()` function written straight off the minimal-diagnostic-pair slide |

---

## What to take away

1. **Build the ruler before you talk about metrics.** Without a gold dataset, all six of Act II's metrics are meaningless — they *presuppose* that artefact.
2. **Use the five-step cherry-pick recipe**, and state explicitly in every report that the recall is **pooled**, not absolute. Minimum 200 queries, shoot for 1,000 (power analysis backs this).
3. **Watch nDCG@K day to day, with Recall@K as its diagnostic partner.** nDCG low + Recall high → fix the reranker; both low → fix retrieval. This one rule can save a week of re-chunking a healthy corpus.
4. **Confirm the gain convention before quoting nDCG** (linear vs `2^rel − 1`); numbers do not compare across conventions.
5. **Run a paired bootstrap before celebrating an improvement.** Suggested ship criterion: **nDCG gain ≥ 0.02–0.05 *and* statistically significant.**
6. **Public benchmarks are a sanity check only**; your own gold dataset is the verdict. The deployment gate needs both.
7. **Keep a held-out set that only the evaluation lead touches** — against overfitting, and against Goodhart.
8. **Go to claim level on the generation side.** Answer-level faithfulness lets one wrong claim ride along free. Make citation accuracy a deployment gate.
9. **Pin your judge, use a different model family, require κ ≥ 0.6**, and keep a golden judge that never touches training, for drift detection.

---

## Positioning in one sentence

Six weeks of building; this week we start measuring. **Get evaluation wrong and all six weeks hang in the air; get it right and the whole pipeline becomes a system you can steer.** This is the week you cross from RAG **practitioner** to RAG **engineer**.
