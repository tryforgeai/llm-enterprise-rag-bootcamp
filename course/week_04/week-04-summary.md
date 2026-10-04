# Week 04 Summary — The Understudy: Search-Native Text and the Derivative Artifact

**Date:** 2026-06-27 · **Source:** `resources/week-4-summer-lesson-plan.pdf` (Asif Qamar, SupportVectors), Dense X Retrieval & RAPTOR papers, and the Week 04 experiments (T016, T017)

---

## TL;DR

The whole week compresses into one sentence:

> **We search derived artifacts; we show original results.**

Weeks 01–03 all quietly assumed the same thing: whatever we index *is* the author's text. Semantic chunking cut the original differently. Contextual retrieval decorated the original. Late chunking pooled the original in latent space. **The substrate never changed.**

Week 04 abandons that assumption and the posture of the course shifts with it. We stop asking "how do I cut the document well?" and start asking:

> **What if the best thing to search is text the document never literally said?**

The design principle the whole week obeys:

> **Do not wait for the user's query to match your documents. Manufacture documents that match your user's queries.**

---

## Act I: The Purpose Problem

One claim, made to stick: **text resists search not by accident but by design**, because every text was written for someone, and that someone was never the search engine.

### Meera and Ravi

Two students preparing for the IIT entrance exam. **Meera** reads physics to *understand* it — she lingers on Newton's third law until she can feel the symmetry of forces, she derives, she doubts, she rebuilds. **Ravi** has a coach and ten thousand past questions. He drills until the instant he sees "two blocks, one pulley, coefficient of friction μ," his hand is already moving. He is not understanding the problem. **He is matching it.**

Who is right? Trick question — **purpose dictates representation.** Test deep conceptual transfer, Meera wins. Test "two hundred questions in three hours," Ravi wins and it isn't close. This is not a parable against Ravi; his representation is correct *for his purpose*. The error would be confusing his purpose with Meera's.

The punchline for us:

```
A textbook is written for Meera.
RAG at query time is Ravi.
```

A textbook builds understanding cumulatively, each idea resting on the last. RAG needs to look at a short question and instantly reach the passage that answers it. **When you index a Meera-text for a Ravi-task you get a mismatch — and that mismatch is the silent cause of half the bad RAG demos any of us has ever seen.** The fix is not to read the textbook better. The fix is to manufacture Ravi's flashcards from it, and index those.

### Every text wears a costume

Same underlying finding — *a drug reduced thirty-day mortality by four percent* — written in six different rooms:

| Costume | Written for | What it does to the claim |
| --- | --- | --- |
| **The paper hedges** | A skeptical peer reviewer | IMRaD splits it: the number lives in Results, the meaning in Discussion, and the Abstract softens both to "may suggest a modest benefit" |
| **The legal brief forecloses** | An adversary | Anticipates objections, buries the operative clause in "notwithstanding the foregoing" |
| **The earnings call consensus-softens** | Shareholders and lawyers at once | Responsibility distributed, every claim wears a helmet |
| **The press release** | A buyer | Sells |
| **The textbook** | A learner | Teaches |
| **The tweet** | An audience | Provokes |

Six costumes, one truth — and the unsettling part: the user's query, *"does the drug reduce deaths?"*, matches **none of them well.**

> **The query is naked. The text is in costume.** Retrieval is the awkward party where the naked query must recognize a friend through six disguises.

### Search-native text

**Search-native text** — text shaped so a blunt query lands on it — is almost never the raw text. The searcher is an audience who arrived *after* the writing was done, speaking a different dialect: short, declarative, impatient, phrased as a question.

Raw text and the ideal search artifact can share almost no words:

```
Query:  "Can the licensor end the contract early?"
Source: "notwithstanding the provisions of Section 12(b), the Licensor
         retains the irrevocable right to terminate"
```

Same meaning, **disjoint vocabulary.** An embedding model bridges some of that gap — that is what it's for — but not all of it.

### The geometric reason: embedding dilution

This is the mechanism the whole week rests on. A paragraph asserting *n* distinct claims does not embed near any one of them. To a first approximation:

```
e_para ≈ (1/n) · Σ e_i
```

where each `e_i` is the embedding of one self-contained claim. A pointed query `q` sits near one vertex `e_k`. Its similarity to the paragraph is therefore a **diluted** quantity:

```
cos(q, e_para) ≈ (1/n) · Σ cos(q, e_i)  ≤  cos(q, e_k)
```

because the one term that matters, `cos(q, e_k)`, is averaged down by *n − 1* irrelevant neighbours.

Geometrically: the mean of several semantically distinct vectors lands in the **interior of their convex hull** — away from every vertex. The paragraph embedding *is* that interior point. **This is not a flaw in the embedding model; it is arithmetic.** (Treat it as heuristic, not theorem — real pooling is nonlinear — but the direction is exactly right.)

**Factoid extraction is the antidote:** index `e_k` on its own and the dilution disappears.

---

## Act II: The Derivative Artifacts — and the Proof

Four artifacts, plus the pattern that makes them safe. Deliberately interrupted in the middle by a measurement, so nobody takes superiority on faith.

### 1. Factoids (propositions) — the atoms of meaning

**A factoid is the smallest textual unit that still means something.** The chemistry analogy is more than decorative: a molecule is the smallest unit retaining the properties of a substance. Split water and you get hydrogen and oxygen — useful, but **no longer wet.** A factoid is the semantic molecule: split it and you have fragments no longer *about* anything.

The canonical example:

> Berlin, situated on the banks of the River Spree, serves as the capital of Germany and is its most populous city, with a metropolitan population exceeding six million residents. The city has been a center of European politics since reunification in 1990.

This one paragraph hides **at least five factoids** — Berlin sits on the Spree; Berlin is the capital of Germany; Berlin is Germany's most populous city; Berlin's metropolitan population exceeds six million; Berlin has been a political center since 1990. Each is complete and standalone, and **not one appears in the paragraph as an isolated sentence.** "The capital of Germany" is welded into a longer clause. Extraction is the act of prying it loose and resolving the pronouns so it can stand in the index with no memory of its paragraph.

**The craft lives in that self-containment.** A lazy extractor returns *"It is the capital"* — useless, because "it" has been severed from "Berlin." A good extractor returns *"Berlin is the capital of Germany."* This is why factoid extraction is the part of the pipeline that rewards prompt optimization most; production prompts come out of heavy **DSPy-driven tuning** over one's own corpus, precisely because the gap between a self-contained factoid and a dangling fragment is the gap between a retrievable thought and noise.

Scale reference from Dense X Retrieval: **FactoidWiki yields ~2.25 propositions per sentence** — a measure of how much meaning ordinary prose compresses, and how many retrieval targets passage-level indexing hides.

### 2. Passage rewrites — the source's understudy

> Academic prose is written to be argued, legal prose to be defended, corporate prose to be forgotten.

A **passage rewrite** reformulates a span in plain, direct, search-friendly language **without changing its meaning**. We keep the original; the rewrite is a *shadow document*, indexed alongside it — invisible to the user, highly visible to the retriever.

```
Original: Notwithstanding the provisions of Section 12(b), the Licensor retains
          the irrevocable right to terminate this Agreement upon thirty (30)
          calendar days' written notice.

Rewrite:  The licensor can terminate the agreement with 30 days' written
          notice, regardless of Section 12(b).
```

The real risk, named honestly: **simplification sheds precision.** "Irrevocable" is a legal term of art the plain rewrite drops. The risk is defused by the core pattern below — the rewrite only *finds* the clause; the original is what the generator reads and cites.

> **The rewrite is the bait; the original is the evidence.** The understudy auditions for the retriever so the star can take the stage.

### 3. QA pairs — planting query-shaped objects

The most mischievous artifact, and the most direct attack on the costume problem. Given a chunk, have an LLM generate the plausible questions that chunk could answer, paired with answers, and embed both.

Why it works: retrieval is a matching problem, and **matching is easiest when both sides speak the same dialect.** Ordinarily a dense retriever performs a *cross-genre* comparison — a question measured against declarative prose. If the indexed object was itself derived from a question, the comparison becomes **same-genre: question against question.** You have planted a query-shaped decoy the retriever should find.

A good pipeline generates **three to eight questions per chunk**, varied along three axes:

- **specificity** — from "what does this section discuss?" to "what learning rate did experiment 3 use?"
- **formulation** — keyword-ish to natural-language
- **abstraction** — factual to interpretive

Each pair stores a **pointer back to its source chunk**, because at generation time the model must see the chunk, not the synthetic question.

**The failure mode to inspect by eye:** a careless synthetic question can mislead the retriever, promising an answer the source does not actually contain. Generation hygiene matters.

> **HyDE is the mirror image.** QA pairs make the *index* question-shaped at ingestion time. HyDE makes the *query* document-shaped at query time — hallucinate a hypothetical answer, embed that, retrieve against it. Both close the same genre gap from opposite ends. You can do both.

### 4. The core pattern — what makes all of this safe

> **Retrieve against the derivative. Generate from the source.**
> **Every derivative artifact carries a pointer home.**

The factoid, the rewrite, the QA pair — each is a **better lure** than the raw chunk for some class of query, and each is a **worse thing to actually quote.** So we never quote them. They win the retrieval; the original passage gives the testimony.

This is what bounds the blast radius. Because the source is always what the model reads and cites, **a clumsy rewrite or an over-eager factoid can cost you a retrieval miss but never a fabricated citation.**

It is also the clean resolution of the Meera–Ravi tension: we never threw the textbook away. Ravi's flashcards *index* the understanding; Meera's text still *is* the understanding. The cram sheet did not replace learning — it pointed back to it.

### And the quiet part, said out loud

> **The bake-off is not derived-instead-of-raw; it is derived-in-addition-to-raw.**

The raw-chunk index **never leaves the system.** Some queries — "what does §4.2 actually say?" — are best served by the original passage, and the raw index is exactly where they land. We are not demolishing Week 03's work. **We are giving it colleagues.** The question for each representation is only: *what is it paying rent for?*

---

## Act III: Altitude — Summaries and RAPTOR

Everything in Act II is **local** — factoids, rewrites, and QA pairs operate at the altitude of a single passage. But some questions cannot be answered from any one passage however well extracted, **because their answer is not *in* the document; it is *about* the document.**

### Abstractive summarization is a change of altitude, not a compression

"Compression" suggests the same content packed tighter into a smaller box. Summarization is not that. **It is ascent in a balloon:** you rise, and large structures invisible from the ground swim into view — the shape of the coastline, the pattern of the fields — while the fine details that filled your vision vanish. **You trade resolution for scope. Neither view is truer.**

So summaries are the **complement** of factoids, never their replacement:

```
Factoids  sacrifice context   for precision
Summaries sacrifice precision for context
```

Some queries are unanswerable from the ground — "what is this report about?", "what are the main findings?", "how does this policy differ from the last version?" No single chunk contains the answer, **because the answer is distributed across the whole.**

Philip Anderson's **"More Is Different"** names the principle: at each level of scale, qualitatively new properties appear that are invisible at the level below. **A document's theme is an emergent property of its chunks — present in none of them, visible only from altitude.**

**Three engineering decisions:**

| Decision | The choice |
| --- | --- |
| **Granularity** | Summarize per chunk, per section, per document, per corpus — each a different artifact with different retrieval behaviour |
| **Faithfulness** | An abstractive summary can hallucinate, and **for RAG a confident false summary is worse than none.** Must be enforced by prompting, verification, or citation requirements |
| **Indexing** | Summaries usually live in **their own namespace**, because their retrieval characteristics are too different from chunks to blend |

Once you accept that **altitude is a dial**, the question becomes: why choose one setting? Per-section answers "what does the methods section cover?"; per-document answers "what is this paper's contribution?"; per-corpus answers "what is this whole collection about?" Each is cheap relative to its value, and each catches a band of thematic queries the others miss. And once you have summaries at several fixed altitudes, **you are one small step from making altitude continuous.** That step is RAPTOR.

### RAPTOR: the zoom lens

Sarthi et al., *Recursive Abstractive Processing for Tree-Organized Retrieval.* Five lines:

```
1. Start with leaf-level chunks.
2. Cluster nearby chunks by embedding similarity.
3. Summarize each cluster into a new node.
4. Repeat: cluster the summaries, summarize the clusters.
5. Stop at a single root (or a few high-level nodes).
```

The result is a tree. Leaves are fine-grained chunks; middle nodes are progressively more abstract summaries; the root is a synopsis of the whole. **At retrieval time you search every level at once:**

| Query type | Lands on |
| --- | --- |
| Factual — "what learning rate?" | A **leaf** |
| Thematic — "what is the overall methodology?" | A **middle node** |
| Global — "what is this collection about?" | The **root** |

> **The query chooses the magnification. The index is a zoom lens, not a fixed focal length.**

Picture a galaxy. From inside you see individual stars — the leaves. Pull back and the stars blur into spiral arms — the middle nodes. Pull back further and the whole galaxy is a single bright coin — the root. **No magnification is the true one; each answers a different question about the same object.**

The **Matryoshka parallel is exact**: a Matryoshka embedding is one vector meaningful at many dimensionalities; RAPTOR is one corpus retrievable at many resolutions. Matryoshka gives multi-resolution *vectors*; RAPTOR gives multi-resolution *text*.

**The detail to file away:** RAPTOR's clustering is **soft, overlapping Gaussian-mixture assignment over UMAP-reduced embeddings** — a chunk may belong to more than one cluster, because a paragraph can be about more than one thing. That soft clustering is the hinge into Week 05.

### The idea to carry out of the room: definitive articles

Run RAPTOR over a **single document** and its upper nodes are summaries of that document. Run it over a **corpus** — a hundred papers, a thousand support tickets, every internal memo on a topic — and **the clusters no longer respect document boundaries.** A cluster gathers the chunks that are *about the same thing*, drawn from wherever they live. Its summary is therefore something new: not a digest of any one source, but a **synthesis across all of them — a definitive article on a topic that no single document contains.**

Ask a shelf — PRML and Hastie–Tibshirani–Friedman's *Elements of Statistical Learning* together — "what is overfitting?" A naive system returns Bishop's best chunk *or* ESL's best chunk. A corpus-level RAPTOR node returns **one coherent answer that has already reconciled both treatments into a single canonical paragraph.**

That is the **definitive-article property**, and it is why this is not "summarization with extra steps." It is Anderson's *More Is Different* cashed out in retrieval: the corpus-level article is an **emergent object** — it exists in none of the source documents and could not, because it is a property of the collection, not of any member. We are literally manufacturing the encyclopedia entry the corpus never wrote about itself.

And that is where the week stops **on purpose.** To build that article well you eventually want to cluster not by raw embedding proximity but by **relational structure** — which entities and ideas are genuinely connected across documents. That is community detection over a graph, and it gets its own day.

---

## The PRML bake-off: how the week proves itself

The lesson plan's designated measurement, and the reason PRML is "the ideal villain."

**Corpus:** Bishop's PRML, §1.1–3.2 — the polynomial curve-fitting narrative through model selection and bias–variance.

**The question:** *Why does polynomial regression overfit on a small dataset?*

**Why this question is cruel:** Bishop never answers it in one sentence. He *shows* it — fits M = 0, 1, 3, 9; displays the M = 9 curve thrashing through every point; tabulates the coefficients **w\*** exploding to enormous magnitudes; and only then introduces regularization. The causal answer is **the whole arc of §1.1.** The sentence you actually want —

> "a high-degree polynomial has more free parameters than data points, so it fits the noise, and its coefficients blow up"

— **exists nowhere in Bishop as a sentence.** It is distributed across a figure, a table, and three paragraphs. A textbook written for Meera, asked a Ravi question.

**Three rules that keep the bake-off honest** (a strong embedder on a lexically rich query can make the naive baseline look better than it is, and a deflated demo teaches nothing):

1. **Use queries with real vocabulary mismatch.** Bishop writes "coefficients become large"; a student asks *"why do the weights blow up when the curve gets too wiggly?"* The derived path has normalized that dialect; the raw chunks have not. That is where the gap widens.
2. **Include synthesis queries.** *"What is the relationship between model complexity, dataset size, and overfitting here?"* Its answer spans three chunks. Raw chunking returns one fragment; the derived path — and later RAPTOR — assembles the whole.
3. **Score answer-ability, not topical relevance.** The question is not "did a related chunk come back" but **"could you actually answer, self-contained, from what came back?"** That is the metric under which derivatives win honestly.

### The Centroid Tug-of-War

The dilution inequality, proved with bodies instead of a whiteboard. Tape out a patch of floor as embedding space:

- **Five volunteers are fact-vertices** — "on the Spree," "capital," "most populous," "six million," "political center since 1990" — standing spread apart, because their meanings are distinct.
- **A sixth student is the paragraph**, and by the rule of the game must stand at the *average* of the five positions. They end up marooned in the middle, an arm's length from everyone and close to no one.
- **A seventh student is the query** — "What is the population of Berlin?" — and reaches for its nearest neighbour. With only the paragraph indexed, the closest thing in the room is that lonely centroid student. **The match is distant; you can see the reach.**
- **Then we factoid-extract.** The paragraph dissolves, its five vertices step forward as independent points, and the query walks straight up to the "six million" vertex. **The distance collapses in front of the whole class.**

That shrinking gap is `cos(q, e_k) ≥ cos(q, e_para)` made kinesthetic. The equation and the student walking from the marooned centroid to the "six million" vertex are the same sentence, told twice.

---

## The four labs

| Lab | What gets built | The metric that matters |
| --- | --- | --- |
| **1. The PRML bake-off, instrumented** | Ingest PRML Ch. 1–3 three ways — (a) raw-chunk index, (b) factoid index, (c) QA-pair index. Keep all three live and **fuse** their results. 20 queries in three bands: pointed factual / vocabulary-mismatch / synthesis | Recall@k, MRR, and — most important — a **human answer-ability judgement**. Hold embedding model, chunker, and top-k **fixed** across all three arms; the only variable that may change is the representation |
| **2. Factoid and QA extraction pipelines** | Two LLM extractors over a 50-chunk sample: one decomposing chunks into self-contained factoids, one generating 3–8 QA pairs per chunk | **Read the artifacts.** Find the factoid that still says "it" instead of "Berlin." Find the synthetic question whose answer the source doesn't contain. These are invisible in aggregate metrics and obvious on the page |
| **3. A RAPTOR tree at two altitudes** | Implement cluster–summarize–recurse for 2–3 levels over the same chapters; aim Lab 1's synthesis queries at different levels and watch where they land | Does tree depth actually improve recall on the synthesis band? **Keep the cost ledger open** — how many summarization calls did two levels cost, and what would a nightly rebuild cost at corpus scale? |
| **4. The multi-representation tournament** | Combine raw chunks, factoids, QA pairs, and RAPTOR nodes behind one fused retriever. Then **ablate** — remove each representation in turn and measure the system-level drop | An honest table: one row per representation, one column per query band, showing where each artifact earns its storage and ingestion cost. **Some representation will contribute almost nothing on your corpus; that is a finding, not a failure** |

**Expected shape of the result:** raw chunks hold their own on the pointed band, derivatives pull ahead on the mismatch band, and the synthesis band is where everyone struggles and RAPTOR earns its keep.

---

## The day's rhythm

> **Surprise first, mechanism second, principle last: the order is the pedagogy.**

```
Frame            Why raw text resists search — purpose, audience, IMRaD, the naked query
Toolkit, part 1  Factoids as the atoms; embedding dilution as the enemy
Proof            The PRML bake-off (palpable difference) + the Centroid Tug-of-War (why)
Toolkit, part 2  Rewrites, QA pairs, "retrieve the derivative, generate from the source"
Altitude         Abstractive summaries; RAPTOR's zoom lens
Corpus           Definitive articles synthesized across documents — the bridge to GraphRAG
```

Note the deliberate interruption: we meet the toolkit, **break into it immediately with the proof**, and only complete the toolkit once no one doubts it is needed.

---

## What we actually built — and the honest gap

Our Week 04 work (T016, T017) implemented **Act II's local artifacts** end to end on real infrastructure. **Act III — RAPTOR — we did not build.**

### Built: four-artifact comparison — `course/week_04/retrieval_artifact_comparison/`

A real (not simulated) RAG demo over three sources — PRML Ch. 2, PRML Ch. 3, and the Dense-X paper — indexing **four artifact types in one shared vector space**. Final SV embedding index: **49 records, 1024-d**, via `Qwen/Qwen3-Embedding-0.6B` on the classroom cluster.

| Artifact type | Records | | Source | Records |
| --- | ---: | --- | --- | ---: |
| QA pair | 22 | | Dense-X | 24 |
| Abstractive summary | 11 | | PRML Ch. 2 | 13 |
| Proposition | 10 | | PRML Ch. 3 | 12 |
| Raw chunk | 6 | | | |

Full pipeline, no TF-IDF fallback:

```
raw chunks → SV chat QA generation → SV embedding index
→ SV query embedding → cosine top-k → SV chat grounded answer
```

Two query runs, both topped by QA pairs:

- `What is a proposition in Dense-X?` → `qa_dense_x_002` at **0.8703**
- `What is the goal of proposition-level retrieval?` → `svqa_raw_dense_x_002_2` at **0.8795**

The same-genre effect working as predicted — **and also a warning.** Those scores are inflated relative to other artifact types precisely *because* question-to-question is an easier match than question-to-evidence. Ranking four artifact types in one undifferentiated space means QA pairs win on score without necessarily winning on answer-ability. The lesson plan's Lab 4 ablation is the correct response to this, and we haven't run it.

The 7-question eval set (`artifacts/eval_questions.json`) is worth reading because each question **names its expected artifact behavior in advance** — a written prediction:

| Question shape | Predicted winner |
| --- | --- |
| "What is a proposition in Dense-X?" | QA pair / proposition — atomic definition |
| "Why can proposition-level retrieval help RAG?" | QA pair / summary — causal explanation, not a definition |
| "What does PRML Chapter 2 teach?" | Abstractive summary — no chunk answers a chapter-level query |
| "What is the beta distribution used for in PRML Chapter 2?" | QA pair — direct fact |

Supporting artifacts: `source_manifest.json`, `abstractive_summaries.json`, `dense_x_propositions.json`, `qa_pairs.json`, `generated_qa_pairs_sv.json` (12 pairs via `openai/gpt-oss-20b`), `raw_chunks_sample.json`, `local_retrieval_index.json` (37-record TF-IDF baseline), `sv_embedding_index.json`. Builder: `scripts/build_local_retrieval_index.py`.

### Built: Xennials FactoidWiki — `course/week_04/task_02_xennials_factoid_wiki/`

The same idea on a live web source, reproducing FactoidWiki construction at small scale. Wikipedia "Xennials" → 6 sections → **11 section-aware raw chunks** → **88 factoids** (`Qwen/Qwen3-VL-8B-Instruct`) → **88 QA pairs** → a **187-record, 1024-d** index covering all three artifact types, plus a Streamlit UI for browsing, search, and grounded synthesis.

The ratio is the finding: **11 raw chunks became 187 index records (~17×).** Small corpus, but that fan-out is the cost side of the whole week, and it is the same curve as the Dense-X corpus arithmetic below.

This 187-record index then became the corpus for our agentic-RAG eval baseline (`evals/`) — Week 04 built the test corpus Weeks 06–07 are graded against.

### Built: chunking pipeline — `course/week_04/chunking_pipeline/`

Docling-based, three notebooks (`01-docling_chunking`, `02-contextual_and_late_chunking`, `03-chunking_pipeline`) — closing out the Week 03 contextual/late-chunking thread as working code.

### Not built

| Lesson-plan item | Status |
| --- | --- |
| **Passage rewrites** | Not implemented. The one local artifact we skipped entirely — and the one most relevant to any corpus with legal or policy prose |
| **Lab 1 as specified** | Partially. We used PRML Ch. 2–3 with our own questions, not §1.1–3.2 with the overfitting question, and we never scored the **vocabulary-mismatch** or **synthesis** bands — which is exactly where the lesson plan says derivatives are supposed to pull ahead |
| **Answer-ability judgement** | Not scored. We measured cosine score and, later, recall — never "could you answer self-contained from what came back" |
| **Lab 3 — RAPTOR tree** | Not built. No cluster–summarize–recurse, no multi-altitude retrieval, no cost ledger |
| **Lab 4 — ablation tournament** | Not run. We have four representations in one index and **no evidence about which are paying rent** |

Per `PROJECT_PLAN.md`, RAPTOR is "an available intervention, not a default milestone" — so skipping it is a decision, not an oversight. But Labs 1, 3, and 4 are all still open, and Lab 4 is the cheapest and most informative of the three.

---

## Dense X Retrieval: the numbers behind the factoid claim

The paper the week's factoid idea comes from (Chen et al., EMNLP 2024). Worth separating what it proves from what it doesn't.

**The headline:** proposition-level indexing beats passage-level by **+10.1 Recall@20** on unsupervised retrievers (+2.7 on supervised).

**Two findings that change who should care:**

1. **Unsupervised retrievers gain a lot; supervised retrievers gain little.** SimCSE and Contriever see +12.0 and +9.3 Recall@5 (35.0% / 22.5% relative). DPR — trained on NQ, TQA, WebQ, SQuAD — does *slightly worse* with propositions on three of its four training sets. **Propositions are a generalization fix, not a universal upgrade.** If your retriever was fine-tuned on your own query–passage pairs, expect much less.
2. **The gain is a long-tail gain.** Propositions win big on rare entities and the gap closes as entity frequency rises (~25% of the 20,000 test queries target entities with frequency ≤ 3). **For head entities, passage retrieval is already fine.**

**Downstream**, at a fixed 500-token budget with LLaMA-2-7B, propositions beat passages by **+4.1 / +3.2 / +2.7 / +2.8 EM** (SimCSE / Contriever / DPR / GTR); sentences land roughly halfway. The largest gap is in the **100–200 word** window — roughly 10 propositions, 5 sentences, or 2 passages. Beyond ~500 words the three granularities converge. *This is the information-density mechanism, and it is why the lesson plan insists on the prompt budget.*

**Corpus arithmetic — the cost side:**

| Unit | # units | Avg. words |
| --- | ---: | ---: |
| Passages | 41,393,528 | 58.5 |
| Sentences | 114,219,127 | 21.0 |
| Propositions | 256,885,003 | 11.2 |

**Propositions cost ~6.2× more index records than passages.** Any proposal to propositionize an enterprise corpus has to carry this number.

**Quality of generated propositions** (manual analysis, 50 random passages) — note where the weakness is:

| Error | GPT-4 | Propositionizer (Flan-T5-large) |
| --- | ---: | ---: |
| Not faithful | 0.7% | 1.3% |
| Not minimal | 2.9% | 2.0% |
| **Not stand-alone** | **4.9%** | **3.1%** |

A Flan-T5-large distilled from 42k GPT-4-generated pairs matches GPT-4 closely. **Self-containment is the weak axis** — exactly the property the whole approach depends on, and exactly the thing Lab 2 tells you to find by eye.

---

## The result that matters: our first measurement failed

Week 04 wrote down a prediction. `evals/cases/EV-001.json` records it verbatim:

> "Week 04 predicted QA-pair and factoid artifacts outrank the raw chunk for query-shaped questions; this case measures whether that holds."

Baseline run (`evals/results/latest.md`, 2026-08-14, **lexical** retriever, k=5, 187 records):

| Metric | Value |
| --- | ---: |
| cases passed | 6 / 10 |
| mean recall@5 | 0.3333 |
| mean nDCG@5 | 0.3773 |
| mean MRR | 0.6 |
| decision accuracy | 0.9 |
| negative rejection rate | 0.6667 |

**EV-001 — "What is a Xennial?" — recall@5 = 0.0.** The simplest possible question against a corpus built specifically to answer it.

The obvious explanation was **tested and disproved**: a stemmer was bolted onto the tokenizer with everything else held constant, and recall@5 stayed at 0.0 — the top-5 merely reshuffled to other non-definition records.

The actual cause: after stopword removal the query is the single term `xennial`. **Forty-three records contain it, most at the same term frequency**, so BM25 has no discriminating signal left and the ranking collapses onto document-length normalization. Gold record `fact_xennials_lead_01_07` is already singular and still loses, **2.50 against 2.77, purely on length** (24 tokens vs. 14).

Three things follow:

1. **Better artifacts do not fix a retriever with no signal to rank on.** A one-term query gives a lexical scorer nothing to discriminate with. This points at dense retrieval or query expansion, not at the tokenizer.
2. **Atomizing the corpus made this worse, not better.** 88 factoids each containing `xennial` at similar term frequency is *precisely* the condition under which BM25 degenerates. **Fine-grained indexing amplifies the many-near-identical-records failure mode** — a cost the lesson plan does not discuss, because it assumes a dense retriever throughout.
3. **The week's claim was never a lexical claim.** Dense X measured dense dual-encoder retrievers; we measured a lexical one and got the opposite outcome. Not a contradiction — a scope correction, and a reminder of the lesson plan's own instruction to hold everything fixed but the representation.

The cheap next experiment is already staged: all 187 records carry a `Qwen/Qwen3-Embedding-0.6B` vector and `--retriever dense` is implemented. Only the query vector is missing, which needs the classroom endpoint — **one session, while course-network access lasts** (`tasks/T025`).

---

## Engineering constraints this week produces

1. **Index-time generation moves hallucination upstream.** A query-time guardrail cannot catch a fact invented during indexing. Any propositionizer needs a faithfulness check against the source span *before* the record enters the index — the lesson plan's faithfulness decision, applied to factoids rather than just summaries.
2. **~3–5% not-stand-alone is a measured rate, not a theoretical risk.** At Wikipedia scale it is background noise. On a small high-stakes corpus it is an incident. **We need a validator, not just a generator.**
3. **Summaries get their own namespace.** Their retrieval characteristics are too different from chunks to blend — and our 49-record index blends them, which is likely part of why QA pairs dominate the score.
4. **The pointer home is not optional.** Every record in both Week 04 indexes carries a `source_pointer` / `source_url`. This is what bounds the blast radius: a derivative can cost a miss, never a fabricated citation.
5. **Every derived index needs a rent check.** Generation cost, storage, and staleness are all real; 6.2× fan-out means 6.2× the invalidation surface. Lab 4's ablation table is the only honest way to decide what stays.

---

## Open questions for the team

1. If QA pairs systematically outscore other artifact types (0.87–0.88 in our runs), should artifact types be ranked in one shared space at all — or retrieved in separate namespaces and fused (RRF) with type-aware weights?
2. What is the dedup / near-duplicate strategy when 88 factoids from one article all contain the same head term? EV-001 says this is the dominant failure mode, not a corner case.
3. How do we cover the questions the QA-pair generator *didn't* generate? More generation, HyDE at query time, or a non-query-shaped arm?
4. Is a passage-rewrite index worth building for our own prose, given the precision-shedding risk — and does the core pattern really defuse it in practice?
5. What is the regeneration policy when a source changes? Factoids, rewrites, QA pairs, and summaries are all stale-able.
6. Does an LLM-generated factoid need a stored faithfulness score, and may retrieval use it?
7. Cheapest useful RAPTOR: two levels over one document, or skip to corpus-level clustering where the definitive-article property actually appears?

---

## Readings

**Essential:**

- **Chen et al.** — *Dense X Retrieval: What Retrieval Granularity Should We Use?* The source of the factoid idea; establishes retrieval granularity as a design variable with measurable consequences.
- **Sarthi et al.** — *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* Retrieval resolution should match query abstraction. **Pay attention to the soft clustering — it is the hinge to Week 05.**
- **Bishop** — *PRML* §1.1–3.2. The bake-off corpus. Re-read the polynomial curve-fitting narrative *specifically as a retrieval problem.*
- **Ma et al.** — *Multi-Vector Retrieval as a Multi-Representation Learning Problem.* Formalizes the whole week: one document, multiple vectors, each capturing a different aspect.

**Optional:** Gao et al. (HyDE) · Wang et al. (InPars / synthetic query generation) · Dhuliawala et al. (Chain-of-Verification) · Asai et al. (Self-RAG) · Anderson, *More Is Different* (1972) — four pages of physics explaining why a corpus has properties no document has.

---

## Where this sits in the arc

```
Week 01 — the RAG pipeline end to end
Week 02 — why vector space works at all
Week 03 — how the source document gets cut, or preserved, before it enters that space
Week 04 — whether we index the source at all, or artifacts manufactured from it
Week 05 — from the book to the library: soft clustering returns as network analysis,
          community detection, GraphRAG and Memory-GraphRAG
```

For three weeks we treated the document as **the thing to be indexed.** Week 04 treats it as **raw material** — a substrate from which to manufacture better things to index.

> **Text is written for a reader; search needs an artifact written for the query. So we manufacture the artifact, we search it — alongside the raw chunks, never in their place — and we show the reader the original. We retrieve the derivative. We generate from the source.**

---

## Follow-ups

- `tasks/T025` — run the dense-retriever arm on EV-001 while course-network access lasts. Cheapest intervention; its result decides whether query expansion / hybrid / reranker are worth trying.
- **Lab 4 (unrun)** — ablate our four existing representations. We have the index; we have no evidence about which representations earn their cost.
- **Lab 1 bands (unrun)** — score the vocabulary-mismatch and synthesis bands, with answer-ability rather than cosine. This is where the week's claim is supposed to be visible.
- `tasks/T027` — Week 04 **and** Week 05 class notes (`course/week_04/week-04.zh.md`, `course/week_05/week-05.zh.md`). This document is the team summary, not the course note.
- `tasks/T026` — answerability / abstention gate. EV-006 answered a question it should have refused, at confidence 1.0.
