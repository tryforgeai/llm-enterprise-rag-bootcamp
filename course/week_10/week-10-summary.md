# Week 10 Summary — The Library of Many Catalogues: Retrieval Architecture, from the Representation to the Verdict

**Date:** 2026-08-15 · **Source:** `course/summer-week-10-lesson-plan (1).pdf` (*Enterprise RAG: The Library of Many Catalogues — Retrieval Architecture, from the Representation to the Verdict*, Asif Qamar, SupportVectors, 29 pp, first draft 2026-08-15)

> ⚠️ **Backfill note:** `../week_11/week-11.zh.md` opens by recording that "Week 10 (8/15) has no record in the repo at all," and infers candidate topics (MemoryCraft / SkillCraft / a Secure Retrieval sequel). **None of those inferences hold.** The actual lesson plan was sitting loose in `course/` all along (with a ` (1)` suffix on the filename), and the subject is **retrieval architecture**. This document fills that gap.

---

## TL;DR

The whole week compresses into one sentence:

> **A retrieval system is not a search over documents. It is a portfolio of representations and a court of adjudication.**
>
> — many purpose-built projections of one corpus, and a cascade of judges that decides, **cheaply and then carefully**, which projection to trust.
>
> **Everything else today is that sentence, unpacked.**

This week cashes in the seed planted on the very first day in June: **retrieval is the load-bearing wall of RAG, because generation cannot cite what retrieval never surfaced.** Week 04's derivative artifacts, Week 05's graphs, Week 06's guardrails, Weeks 07–08's evaluation — every week has leaned on that wall, and today the wall gets its engineering.

The day's shape (eleven in the morning until half past eight at night — the retrieval side of the house, entire):

```
Act I     The Library        (foundations and the portfolio: the Mundaneum, the recall ceiling,
                              the tomographic principle, four altitudes, the instrument cabinet, the trained instrument)
Act II    The Second Corpus  (the derivative artifacts, and the long-context mirage)
Act III   The Court          (the judicial ladder and fusion in ranks, the question side,
                              the machine room, the seeing catalogue, the two-column ledger, the playbook)
```

---

## Act I: The Library — Foundations and the Portfolio

### Brussels, 1895: The Mundaneum

In September 1895 two Belgian lawyers, **Paul Otlet** and **Henri La Fontaine**, convened the first International Conference on Bibliography and began the *Répertoire Bibliographique Universel* — a card catalogue meant to record every document humanity had produced. They rebuilt Dewey's decimal classification into the **Universal Decimal Classification**, whose connective signs let a single card sit at the intersection of `statistics : agriculture : India : 1895` — **addressable from many directions at once.**

Then Otlet did the thing that concerns us: **he decided the book was the wrong unit.**

> His **monographic principle** directed that documents be decomposed — each fact copied onto its own standard 3-by-5 card, classified, and filed where any future question could find it. By the 1930s the drawers held some **sixteen million cards**.

**And people used it.** From 1912 the Institute answered queries by telegraph.

> Hear it with an engineer's ear: **a remote client, a multi-index knowledge base, retrieved evidence with provenance, and a latency of days.** — queries by post or telegraph, clerks walking the drawers, answers back by mail at **27 francs per thousand cards, some 1,500 queries a year.**

In 1934 Otlet's *Traité de documentation* sketched a *réseau* of desks and screens consulting a universal index over wires — **a networked terminal, described the year Turing was an undergraduate.**

The ending: the government withdrew support in 1934; in 1940 the occupiers cleared the halls for an art exhibition, **destroying some sixty-three tonnes of the collections.** Otlet died in 1944 believing his life's work had failed. The surviving drawers eventually found refuge in Mons.

**Here is the load-bearing lesson, and it is not "visionary anticipates the internet." It is this:**

> **Otlet did not build a search over documents. He built a portfolio of representations.**
>
> The same fact lived as a bibliographic entry by author, a classified card by subject-intersection, a clipping in a dossier, an image in the iconographic repertory, a line in an encyclopedic summary — **five purpose-built projections of one source, each manufactured because some class of future question would need exactly that projection.**
>
> And one thing was missing: **Otlet had no ranking.** A UDC class contained a card or it did not; within the drawer, cards sat in accession order.
>
> **The Mundaneum had the portfolio and lacked the court. Half of today is the half Otlet never built.**

> **The two engines that let us run Otlet's architecture at machine speed:** the LLM made **the manufacture of derivative representations cheap** (an iceberg of offline compute, invisible at query time), and sixty years of index structures made **search sublinear**. **His institution died because every projection and every query cost a clerk; ours costs electricity.**

### The thesis, and the recall ceiling

> **A retrieval system is two things joined:**
> **a portfolio of representations** — many purpose-built, lossy projections of one corpus, each manufactured because some class of query needs exactly that projection;
> **and a court of adjudication** — a cascade in which cheap judges narrow the field so that **expensive judges can afford to be careful**.
>
> Retrieval architecture is the discipline of deciding which representations to manufacture and how to adjudicate among them. **Scale decides how much of each you can afford; measurement decides which of them earn their place. One corpus, many catalogues.**

**Why is retrieval the load-bearing wall? Because of the recall ceiling.**

> A child loses her marbles in a sandbox and recovers them with a **bucket** and a **sieve**: **scoop wide, scoop generously, tolerate sand** — the sieve removes sand at leisure.
>
> **But if the scoop misses a marble, no sieve can recover it.**
>
> **Whatever recall you have at the first stage is a ceiling that nothing downstream can raise:** not a reranker, not a better prompt, not a bigger model. **Generation cannot cite what retrieval never surfaced.**

This is why **the scoop is tuned for recall and the sieve for precision**, and why the entire cascade of Act III is machinery for spending precision after recall has been secured.

> **Write it on the inside of your eyelids: only the scoop decides what is caught.**

### The tomographic principle and the four altitudes

**Why many catalogues rather than one better one?**

> A CT scanner **never photographs the tumor**. It takes hundreds of lossy projections — **each blind on its own** — and reconstructs what no single exposure contains.
>
> Each index in the portfolio is a projection of the corpus **at its own semantic angle**: the sparse lane sees the words on the page, the dense lane sees the meaning behind them, the factoid index sees the atomic claims, the summary index sees the theme. **Fusion is the reconstruction.**
>
> The kin are the **cubist portrait** (one man, many simultaneous angles), the **compound eye**, and **Rashomon**.
> What the principle is **not** is the **panopticon**: one eye claiming total sight. **A single index makes that claim; the portfolio refuses it, and the refusal is the whole architecture in one gesture.**

**The projections are needed because questions arrive at different altitudes:**

| Altitude | Wants | Example | Representation |
|---|---|---|---|
| **point** | one fact | "What was the Phase III enrollment?" | **factoid** |
| **contextual** | a passage with its surroundings intact | — | **chunk** |
| **thematic** | what runs through a document | "How does this vendor think about data residency?" | **summary** |
| **global** | what lives in the **structure** of the whole corpus and in no passage at all | "What are the major regulatory concerns across these five hundred transcripts?" | **community** |

> **A query that lands on the wrong altitude gets a confidently irrelevant answer:** the point query drowned in a summary; the global query answered from three quotes about one drug.
>
> Much of the routing and fusion machinery of the afternoon exists to **send each question to its own height** — or, better, **to let the query find its own level.**

### The instrument cabinet: every representation is a lossy projection

> Korzybski's **map is not the territory**, and every index is a map drawn for one journey.

**The sparse lineage** keeps a vocabulary-sized coordinate system: a document is a bag of weighted terms, and the inverted index makes lookup sublinear.
- **BM25** weights by term frequency saturating against document length, and its two constants (`k1`, `b`) have survived thirty years because they encode **a durable truth about how evidence accumulates.**
- What BM25 cannot do is **see synonymy**: the query says "cardiac," the page says "heart," and the postings never meet.
- **SPLADE** answers by **learning the expansion** — a masked-language-model head predicts, for each document, a sparse distribution over the whole vocabulary, so **the page about hearts carries weight on "cardiac" it never printed.** A sparse lane that has read the thesaurus — **and it keeps the inverted index and every operational virtue that comes with it.**

**The dense lineage** throws away the vocabulary coordinates and keeps a few hundred learned ones. A bi-encoder maps query and document into one space; relevance is a cosine. **This is the lane that closes the paraphrase gap** — and it inherits the geometry of high dimensions.

> **The two lineages are complementary, not competitive:** the sparse lane wins on **the rare term, the identifier, the exact phrase, the name that appears once**; the dense lane wins on **paraphrase and intent**.
> **This is precisely why hybrid retrieval, fused in ranks, beats either alone — the tomographic principle in its simplest, two-projection form.**

### Concentration of measure and the aperture doctrine

> In a thousand dimensions, **almost every pair of random vectors is nearly orthogonal**, and the cosine similarities of a real corpus, far from filling [−1, 1], **crowd into a narrow band** — typically somewhere between **0.2 and 0.9** depending on the embedder, with most mass in a sliver.

This is **concentration of measure**, and it has three practical consequences to carry into every threshold you ever set:

1. **An absolute similarity threshold is not portable across embedders.** 0.7 on one model is **a different aperture** from 0.7 on another, because the distributions differ.
2. **The differences between the top few candidates are small in absolute terms**, so **a reranker's discrimination matters more than the retriever's**, and calibration at the exit is not optional.
3. **The aperture doctrine** — a threshold is **a cone aperture** around the query direction: widen it and you admit more sand; narrow it and you lose marbles. **Set it on the sealed set, per embedder, per lane, and revisit it whenever the embedder changes.**

> Act II's **Berlin experiment** (0.64 versus 0.81–0.90 across a threshold of 0.7–0.8) is concentration of measure biting a real production system.

### The representations: Matryoshka, late interaction, and the cost knob

Two more ideas complete the cabinet, and **both changed the cost structure of the dense lineage rather than its accuracy** — which is why they belong in an architecture session and not merely a modeling one.

- **Matryoshka representation learning (MRL)** trains a single embedding whose **prefixes are themselves good embeddings**: the **first 128 dimensions of a 1,024-dimensional vector are a usable, cheaper projection of the same meaning.** **Dimensionality becomes a runtime knob** — scoop with 128 dimensions over millions of candidates, rescore the survivors at full width.
- **ColBERT's late interaction refuses to pool at all**: every token keeps its own vector, and relevance is the sum over query tokens of the maximum similarity to any document token (**MaxSim**). **The rare term that a pooled vector would average away keeps its vote.**
  > For years the objection was cost — a vector per token — and **by 2026 the objection has largely fallen: MUVERA reduces multi-vector search to single-vector MIPS with guarantees, and WARP and small ColBERTs collapsed the serving bill.** **The tournament, not the cost objection, now decides where ColBERT sits.**

**The contextualization lineage** closes the cabinet: Anthropic's **contextual retrieval** prepends a generated situating context to each chunk before embedding and BM25, **cutting top-20 retrieval failure by 35–67%** depending on the reranker; late chunking and then whole-document contextual encoders moved that context **from the prompt into the encoder itself.**
> **Watch that trend: some of the derivatives we manufacture by hand this afternoon are becoming the encoder's native output.**

### The trained instrument: DCL, curriculum, and the invariant

> **The embedder is not the glass; it is the mirror, and mirrors are ground for a purpose.**

Two forces shape the geometry: **alignment** pulls a query toward its positive; **uniformity** spreads everything else across the sphere so that no region is crowded. **InfoNCE** implements both as a line-up tournament:

$$L_{\text{InfoNCE}} = -\log \frac{\exp(s(q, d^+)/\tau)}{\sum_{j=1}^{N}\exp(s(q, d_j)/\tau)}$$

**Read it aloud: make the positive win the line-up.**

The subtlety is that **with the positive in the denominator**, the gradient on the positive is **throttled exactly when the model is already doing well** — **fifty times weaker**, in the monograph's worked case, precisely when it matters.

The fix is **decoupled contrastive learning (DCL): evict the positive from the denominator.**

$$L_{\text{DCL}} = -\frac{s(q, d^+)}{\tau} + \log\sum_{j \neq +}\exp(s(q, d_j)/\tau)$$

> **The positive leaves the line-up, and small batches stop being a tax** — the house loss for exactly that reason.

**Negatives arrive on a curriculum:** easy random negatives first, then BM25-mined, then dense-mined, **each stage stinging a little more**, with **distillation of a cross-encoder's margins (Margin-MSE)** as the load-bearing signal in serious recipes.

> ⚠️ **The false-negative trap:** mine negatives too hard and the "negatives" are often **unlabeled positives**, and **the loss punishes the model for being right.**
> The countermeasure is **positive-aware mining** (discard candidates that score too close to the positive) and **a denoising judge** (a cross-encoder) that vets the hard negatives before they are trusted.

**The two ideas of the morning meet in one rule — the MRL–DCL invariant:**

> Apply the decoupled loss **inside the Matryoshka summation, at every prefix width**, so that **the 128-dimensional scoop and the full-width rescore were trained by the same discipline**;
> and **regression-test that invariant** (recall at scoop depth on the sealed set) **before any embedder swap**, because **a silently rotting scoop is six marbles gone before the sieve ever sees them.**

**The 48-hour doctrine:** with synthetic pairs manufactured from your own corpus, a curriculum, and DCL, **a domain fine-tune is a two-day job** — and **you refuse it** when the corpus is generic, the domain is small, or **the yardstick does not yet exist to prove the swap honest.**

---

## Act II: The Second Corpus — Derivatives, and the Mirage

> The morning built the projections of **the corpus we were given**. The early afternoon **manufactures a second corpus** — the derivative artifacts, Otlet's cards mechanized — and then confronts the seduction that would abolish retrieval altogether: the million-token window.
>
> **Both halves turn on the same question: whose shape is the text in, the reader's or the examiner's?**

### The user is the examiner

> At IIT, I came second in applied electrodynamics, and the manner of it has instructed me for forty years. The classmate who came first went to the seniors and collected the **question banks** — roughly **forty questions this examiner actually asked**, recycled with small mutations. He compiled beautiful answers to those forty, memorized them, topped the exam, **and never opened a physics book again.**
>
> **I had optimized on learning the subject; he had optimized on answering the examiner.**
>
> **In retrieval architecture that is not a tragedy. It is the specification.**

**The user is the examiner:** a retrieval system faces a stream of questions **in a register it does not control**, and the corpus was written **with no examiner in mind** — textbooks for pedagogy, papers for reviewers, contracts for opposing counsel. **That is the register mismatch, and it is permanent.**

The orthodox response is to transform the query until it resembles the prose; we will do that too. **But the deeper move runs the other way:**

> **Do not wait for the query to match your documents; manufacture documents that match your queries.**
>
> Take the corpus offline, when compute is cheap and time is abundant, and recast every chunk into **the shapes a question can seize**.
> **Whatever intelligence you can spend on the still thing, spend it there — the iceberg of compute belongs below the waterline, invisible at query time.**

### The master pattern and the back-pointer

**One rule governs every artifact we manufacture:**

> # Retrieve the derivative, generate from the source

Rewrites, factoids, QA pairs, summaries, tree nodes, community summaries — **these are searched. The original passage is what the generator sees and cites.** The derivative exists to be found; the source exists to be quoted.

> A legal rewrite that dropped **"irrevocable"** — a term of art with case law attached — **is not evidence; it is bait.**

**And the load-bearing corollary: every derived artifact carries a pointer back to its origin, not as etiquette but as machinery.**

That **provenance back-pointer** does two jobs:

1. **It is the citation** — the clickable, auditable claim.
2. **It is the invalidation key** — when a source changes, you **walk the provenance graph in reverse** and learn exactly **which factoids die, which summaries have gone transitively stale, which tree nodes must be marked dirty.**

> **A derivative corpus without provenance is not an index; it is a rumor mill with vector search.**

> **Return to Brussels:** this part, entire, is **the monographic principle in period costume**. **The cards are the derivative corpus. The shelved book is the source. The clerk retrieves the derivative and cites the original. Everything else is mechanization.**

### The artifact inventory — one source, many representations, each against a named corpse

> **The discipline of the inventory is that no artifact earns its place by being interesting; it earns it by pointing at a specific way retrieval dies without it.**

| Artifact | The corpse it prevents | Notes |
|---|---|---|
| **Contextualized rewrites** | **endophora and armored register** (legalese, clinical shorthand) | the chunk restated in the question's register with pronouns resolved — **the source's understudy, auditioning for the retriever** |
| **Factoids** | **embedding dilution** | a five-claim paragraph embeds near the **centroid** of five meanings, **far from every vertex**; the pointed query lands near **one vertex** |
| **QA pairs** | **the cross-genre mismatch** | **the only artifact that puts a query-shaped object in the index.** Three to eight questions per chunk; **embed the question**, carry the answer and source ids in the payload. **The decoy the retriever should find.** |
| **Summaries** | **thematic queries shattering across chunks** | section, document, corpus altitudes, each its own index; **the summarizer is a reporter, not a judge — itemize disagreement, never reconcile it** |
| **RAPTOR nodes** | the zoom lens | cluster, summarize, recurse: a **discovered** hierarchy, **1.3–1.5× the leaf count**. Retrieve over the collapsed tree **so the query finds its own altitude** |
| **Community summaries** | the telescope | entities, Leiden communities, summaries at several resolutions, map-reduce at query time — **for the sensemaking question that lives in no passage** |
| **Governed concepts** | **the authority failure** | last week's guest, returned (see below) |

**The Berlin experiment (the empirical case for factoids):**

> The paragraph containing the answer scores **0.64** against the river query; the extracted factoid scores **0.81–0.90** — **and at a production threshold of 0.7–0.8, the paragraph holding the answer is silently dropped.**
>
> **Dense X industrialized this: FactoidWiki, 257 million propositions from 114 million sentences.**
> Discipline: **self-containment, an NLI faithfulness filter, a cap per chunk.**

> ⚠️ **RAPTOR's warning:** garbage clusters yield **confident garbage summaries** — and **the phantom cluster**, an accidental clump that **passes every per-chunk provenance check**, is a provenance failure **that only a topical-coherence check catches.**

> **Embeddings tell you passages sound alike; triplets tell you they are about the same things.**

> **The optical triad organizes the inventory: the factoid is the microscope, RAPTOR the zoom lens, GraphRAG the telescope. A well-run laboratory owns all three and knows which one it is holding.**

### The seventh artifact: the governed concept, seated

Last week's guest returns and **takes a seat in the inventory**. The governed concept is the derivative artifact refined so far that it **stops being a projection of the source and becomes an authored knowledge object**. **Its corpse is the authority failure** — retrieval returning text **that no one currently stands behind**, the superseded policy at cosine 0.91.

**Three properties that distinguish it from every other resident of the bestiary:**

1. **Repair is cheap, and cheapness changes behavior.** A wrong fact in an embedded corpus **waits for the quarterly re-ingestion**; a wrong fact in a bundle is **a one-line diff, merged in minutes, with `git blame` recording who fixed what.**
   > **We rebuild every other artifact; this is the only one we repair.**
2. **It serves a second retrieval mechanism beside embedding — navigation.** An agent walks the bundle's index files and follows its links **as a librarian walks stacks**, a graph traversal over curated objects — kin to GraphRAG's communities **but with the graph authored and reviewed rather than induced by clustering.**
3. **The review gate is structurally native** (carved over the door) — **the phantom cluster taught us that synthesis needs a coherence gate and we bolted one on; here the gate is the format's own workflow.**

**The gate has a dark twin:**

> An extraction agent can mint a concept **whose every field is well-formed, whose every cited source is real, and whose definition is a fluent interpolation that no version of the policy ever contained** — **the phantom concept**, the phantom cluster's descendant, **and more dangerous than its ancestor because a phantom that survives review is promoted**: stamped human-reviewed, elevated into the high-stakes query paths the tiers exist to protect.

The defenses are last week's, **aimed one stage earlier**: the reviewer checks **claim-to-source fidelity, not YAML hygiene**; an **entailment pass** — the same NLI machinery that filters factoids — **runs in CI on every knowledge pull request**; and **numbers get no prose at all**, because a quantitative claim belongs in an attested computation **where interpolation is structurally impossible.**

**And the ladder discipline:** the governed layer is **the top rung**, expensive in **sustained human attention**, **earned only for the governed core** — glossary, metric definitions, policies, runbooks, **the few hundred to few thousand concepts where the authority failure actually kills and a domain owner exists to hold the pen.**
> **An unreviewed bundle is chunks wearing a suit, and the suit makes it worse.**

> **The channel's honest debit column:** curation cost is real and recurring; `stale_after` is an alarm clock, not a maintenance crew; coverage is structurally partial; and the transformation itself can hallucinate. **The wager that agents change the economics of curation is open — no production postmortems yet — and we say so.**

### Two economics govern the inventory

**The sidecar doctrine:**

> **The graph is a sidecar, never the main road.** Global sensemaking is **5–15% of enterprise traffic** (our routers send **one to two percent** through it), **disproportionately the questions executives ask**, so it **defines the intelligence ceiling without being allowed to carry the highway.**

> **The thousand-dollar intern invoice** — an extraction job wired to the frontier API instead of the local cluster — taught the cost cliff; **LazyGraphRAG and HippoRAG 2 have since repealed much of the invoice**, so the doctrine is now **about traffic, not price.**

**The archaeology of top-K:**

> **Log the genealogy of every final result for a week and count.**
> **The finding, every time: most of the top results, most of the time, are not raw chunks.**
>
> **That is the single strongest argument for the multi-representation architecture, and it costs one week of logging to run on your own traffic.** Then keep it running as telemetry, and **let genealogy — never enthusiasm — decide which lenses stay.**

### The economics of the derivative corpus

> **Enthusiasm for lenses is not a budget.**

Raw chunks alone already carry **four indices** in the reference architecture (SPLADE, the 128-dimension scoop, full-dimension dense, ColBERT), and each artifact family arrives with indices of its own; **the total passes a dozen without anyone noticing the odometer.**

**So the discipline, stated as a rule and enforced as a gate: every index must earn its place through ablation.** Turn each index off; measure the staircase on the gold set; **an index whose absence nobody can measure is complexity without value.**

**The house rule of thumb for the build-or-don't decision:**

```
Artifact ROI ≈ (query-mix weight on that granularity) × (measured quality lift) − (build cost + storage cost),
                amortized over query volume
```

> Factoids shine on **fact-dense corpora with pointed traffic**; rewrites pay **only where a register gap exists**; RAPTOR is overkill for a tiny FAQ; **the graph sidecar needs sensemaking traffic to bill against.**
> The weights come from **your measured query distribution** — **the tyranny of the use case, in ledger form.**

**And the amortization has a denominator.**

> "Work hard once, enjoy for the rest of your life" **assumes the corpus sits still long enough to collect the interest** — and a regulatory feed that turns over **weekly**, or a ticket queue that turns over **hourly**, does not.
>
> **The churn calculus:** derivation cost per document × churn rate, against quality lift × query volume. **When churn wins, build fewer, cheaper, lazier artifacts** (LazyGraphRAG is exactly this trade, industrialized).

**Invalidation stratifies naturally:**

- **Local invalidation** — chunks, factoids, rewrites, QA pairs (delete by document id, re-derive)
- **Transitively stale** — summaries, tree nodes, community summaries (**mark dirty on write, rebuild lazily, bottom-up, asynchronously**)

> **Tiered freshness is not a compromise; it is the correct reading of how information decays at different altitudes.**

> 💡 **Say's Law holds in retrieval: supply creates its own demand.** Build the factoid index because the measured distribution was 80% point queries, and **watch the thematic share climb** as users discover the system can now be trusted with harder questions.
> **Design for the distribution you will create, and leave room in the router for sidecars not yet built.**

### Interlude: the long-context mirage

**Why retrieve at all, when the window holds a million tokens?**

> The seduction is real and **must be answered with evidence rather than doctrine.**

1. **NoLiMa** — needle-in-a-haystack benchmarks **look solved because the needle shares words with the question.** Remove the lexical overlap — NoLiMa — and **eleven of twelve frontier models lose half their accuracy by 32K tokens.**
   > **Context rot is not a corner case; it is the default when the answer must be inferred rather than matched.**
2. **The meter** — **a million tokens per question is dollars per question, every question, forever** — the iceberg of compute **dragged above the waterline and paid for at inference prices.**
3. **The library argument** — **you do not read the library to answer a question; you consult the catalogue.** And Otlet's clerks — **who could have read toward any answer** — **built the catalogues precisely because reading does not scale.**

**The honest synthesis:**

> At **cockroach scale** — ten thousand documents, one register, a handful of candidates — the long window is **a legitimate organ**; stuff whole documents and let the reranker choose.
> **Above that scale, retrieval is not competing with the window; it is what makes the window worth filling.**
>
> **The window is for holding evidence, not for finding it.**

---

## Act III: The Court, the Question, and the Machine Room

> The portfolio is built; **now the half Otlet never had.**

### The judicial ladder and fusion in ranks

> **The cascade is a court in which cheap judges narrow the docket so that expensive judges can afford to be careful.**

**The scoop:** each lane (SPLADE, the 128-dimension Matryoshka lane, ColBERT) **emits its top few hundred**; **recall is sacred here**, and the depths are chosen so that **the union rarely misses a marble.**

**Then fusion.** The lanes' scores are **incommensurable** — a BM25 score and a cosine **share no scale** — **so we fuse in ranks**, and the honest baseline is **reciprocal rank fusion**:

$$\text{RRF}(d) = \sum_{r \in \text{lanes}} \frac{1}{k + \text{rank}_r(d)}, \qquad k = 60$$

> **Read it:** a document ranked highly by **any** lane rises; **k damps the head** so that one lane's first place cannot dominate; and **k=60, from a three-author SIGIR paper of 2009, remains the default in essentially every engine.**

**Learned fusion** (tuned convex weights) beats RRF when you have the hold-out to tune it on — which brings the difficulty: **fusion weights and emission depths sit on a staircase you cannot differentiate** (a rank changes discretely).

**The house answer is the surrogate-surface method:** sample the parameter grid, fit a smooth surrogate to the measured nDCG at each point, and optimize the surrogate — **Bayesian optimization in a small number of dimensions, on the sealed set, with paired-bootstrap intervals so that a difference of 0.02 is not mistaken for signal.**

> **Universal suffrage before the yardstick exists:** until you have a gold set to tune on, **RRF at k=60 with equal lane weights is the constitution. Amend it only with evidence.**

### The reference cascade (copy as a starting point, then tune on your own yardstick)

```
SPLADE            Matryoshka 128-d      ColBERT              derivative indices
(the words meant)  (the cheap scoop)     (every token votes)  (factoid, QA, summary)
     └────────────────┴─────────────────────┴───────────────────┘
                each emits top few hundred          ← the scoop: recall is sacred
                            ↓
                Fusion in ranks (RRF, k=60) → a few hundred
                            ↓
            Parent-level dedup, then MMR    → a few dozen
                            ↓
       Full-dim rescore (+ ColBERT pass where earned) → 20–30
                            ↓
    Cross-encoder (on the SOURCE TEXT) → calibrated top 10   ← the verdict:
                                                               the decoy's job ended long ago
```

> **Latency at p95 stays under a second or two because every stage narrows before the next spends.**

**The clock budget, roughly:** lanes in parallel, tens of milliseconds each · fusion and dedup, single-digit milliseconds · the full-dimension rescore, tens · **the cross-encoder, one to several hundred** depending on docket depth and model — **unacceptable for a trading screen and free for a batch pipeline.**
> **Latency is not a performance metric; it is a structural constraint that decides which judges may sit.**

### Dedup, the decoy, and the supreme court

> **Before any judge speaks, one voice per witness.**

The derivative corpus **guarantees that a single source will arrive many times** — as its chunk, its factoid, its QA decoy, its rewrite — and **a reranker handed five costumes of one passage wastes five seats.**

**So collapse candidates sharing a parent before the sieve, then apply MMR for diversity among what remains.**

**Then the doctrine that trips more teams than any other:**

> # The decoy's job ends at retrieval
>
> When the cross-encoder arrives, **it must judge the source text against the query** — **never the synthetic question, never the rewrite, never the summary.**
>
> **A reranker grading the decoy is a court cross-examining the bait.**

**The supreme court itself** — the cross-encoder that reads little and thinks hard — **has become cheap enough that the question is no longer whether to seat it but how deep a docket to hand it** (rerank-2.5, Rerank 4, instruction-following, 32K windows); and **its verdict must be calibrated at the exit**, so that **a score of 0.8 means the same thing on Tuesday as it did at launch** and an abstention threshold can be trusted.

### The question side of the glass

> **Half the architecture stands on the query's side.** A query is **a description of a gap in someone's knowledge, typed in a hurry**, and it arrives broken in a small number of recurring ways.

**Six pathologies, six verbs:**

| Pathology | Verb | Notes |
|---|---|---|
| **Misspelled** | **correct** | cheap, deterministic, **first**; the sparse lane is unforgiving of a transposed letter |
| **Underspecified** | **expand** | "the policy" becomes "the 2026 reserving policy"; **pseudo-relevance feedback** and the session's own context supply what the user left out |
| **Overloaded** | **decompose** | two questions wearing one question mark → split, retrieve separately, recombine — **the multi-query fan-out** |
| **Ambiguous** | **disambiguate against the corpus** | "Java" is the island in one corpus and the language in another; **the corpus, not a dictionary, decides** |
| **Register-mismatched** | **rewrite** | the plain question restated in the corpus's dialect — **the read-time twin of the write-time rewrite artifact** |
| **Multi-hop** | **plan** | the question whose answer requires an intermediate answer first is decomposed into a chain and retrieved iteratively — **the seed of the agentic turn** |

**The transformation cascade applies these in order of cost**, and its most expensive resident is **HyDE** — **fabricate a hypothetical answer and embed that**, a document-shaped probe for a document-shaped index.

> **HyDE is generated QA pairs run at read time instead of write time** — one principle (**eliminate register mismatch by generating the missing side**), at two timings.
> **Use it last, with a capable model, knowing that a fabricated probe can fabricate a neighborhood.**

> **The transformation cascade is a pipeline of understanding run in order of cost:** cheap deterministic fixes first (spelling, normalization, acronym expansion), then classification (which pathology, which altitude, which route), then the LLM-mediated rewrites, **and HyDE last.** **Each stage should be able to short-circuit the rest — most queries need only the first.**

**Two doctrines from the derivative side return here in mirror image:**

> **The canonised query** — spelled, expanded, disambiguated — **is what every lane receives**, so that the lanes **vote on the same question**;
> and **the original query is what the cross-encoder judges against**, so that **a transformation which drifted from the user's intent cannot launder itself through the court.**
>
> **Transform for retrieval; judge against the truth.**

### The front door, the router, and the agentic turn

- **The semantic cache is the front door** — an embedder E and a threshold τ that decide **whether this question has, in effect, been asked before** — **serve, hint, or miss, never guess** — and it deserves its own day, **which it gets next week** (this is Week 11's subject).
- **The router** sends each question to the right catalogue and the right court: point and contextual traffic down the highway, thematic to the summary lanes, **the global minority to the graph sidecar**, schema questions to the structured store.
- **The agentic turn** (Search-R1 and its kin, **retrieval learned end-to-end by reinforcement**) is **the router's most expensive tier — a rung on the ladder and not a heresy.**
- **And the quietest optimization: sometimes the right answer is not to retrieve at all** — the parametric answer suffices, or the question is a greeting, or the cache has it — and **a system that retrieves reflexively pays for evidence it does not use.**

### The machine room

> **Recall is bought with milliseconds, and the exchange rate is set by the physics of finding a neighbor.**

- **Graph indexes (HNSW)** trade memory for speed · **disk-resident indexes (DiskANN)** trade latency for scale · **quantization** (product, scalar, down to one bit) trades precision for a budget line, **with the scoop-and-rescore pattern recovering what quantization loses.**

**Three doctrines keep the room honest:**

1. **Version skew** — **a query must never span embedder versions.** Migrate by **dual-write**, **serve from one index at a time**, and **never compare a v2 query against v1 vectors.**
2. **Poisoning** — **PoisonedRAG showed that five crafted documents in a corpus of millions can steer ninety percent of targeted answers**, so **treat every ingested document as untrusted code**, spotlight retrieved evidence, and **watch for silent retrieval collapse on polluted pools.**
3. **Access control** — **sync ACLs at index time and pre-filter at query time, never post-filter.** **A post-filtered top-K that removes eight of ten results has silently become a top-two, and the recall ceiling has fallen without anyone noticing.**

**Serving the middle judges is where most latency budgets are won or lost:** the full-dimension rescore over a few hundred candidates **is a matrix multiply that belongs on the same box as the index**; the ColBERT pass, when earned, **is where MUVERA's fixed-dimensional encodings and residual compression pay their way**; and **the cross-encoder's docket depth is the single knob that trades the most quality for the most milliseconds** — tune it on the yardstick, watch it on the dashboard, and **never let a demo's twenty-candidate docket silently become production's fifty.**

**Index operations complete the room:** the living catalogue must be **re-derived on churn via provenance keys**, migrated between engines by the **dual-write playbook**, and **rebuilt from the corpus and the recipes when — not if — something is lost.**

### The seeing catalogue, briefly

> Otlet collected pictures too, and so must we.

- **The two-tower lane (CLIP and its descendants)** sees **style** — it embeds images and text into one space and **cannot read a sentence in a diagram.**
- **The caption lane manufactures textual derivatives of every image** (Otlet's card, mechanized for pixels) **so that the whole derivative machinery applies.**
- **Then the OCR-free turn: ColPali retrieves page images by late interaction, skipping the parser entirely**, and the storage tax that once made this a luxury **has been repealed by the same compression that saved ColBERT.**

> **The exhibit joins the same docket: the cascade does not care whether a candidate began as a paragraph or a page.**

### Coupling the yardstick, and the two-column ledger

> **Nothing in this session is decidable without a yardstick, and the evaluation weeks were the preparation for today.**

- The gold set is **sealed, versioned, and hidden from the engineers**;
- every claim about a component is **a paired-bootstrap interval on that set, never a point estimate**;
- **public leaderboards are smoke tests, not instruments.**
- **The yardstick must be living:** a gold set frozen at launch **measures the users you no longer have**, and **Say's Law guarantees your users will change.**

**Then Pacioli's discipline from Venice, 1494, applied to architecture: every component posts twice.**

| Column | Contents | Who writes it |
|---|---|---|
| **One: the cost of presence** | build steps, data demanded, latency, maintenance, **the thing that can now break at two in the morning** | **vendors will itemize it for you eagerly** |
| **Two: the price of absence** | the query class that degrades without it, the metric that registers the degradation, **a failure a user actually sees** | **only measurement can write it** — an ablation, a tournament, an archaeology trace |

> **A component with a full first column and an empty second column is not infrastructure. It is decoration.**

### The playbook: scale decides, and every index earns its place

> **An old man under house arrest wrote the first page of this playbook.**

**Galileo, 1638:** scale a bone up in every dimension and **its strength grows as length squared while its weight grows as length cubed**; **the giant collapses under his own femur.** Haldane's mouse walks away; the horse splashes. The insect wears its skeleton outside and thrives; the elephant cannot.

> **Scale decides architecture — not taste, not fashion, not the latest post.**
>
> At **cockroach scale** (ten thousand documents, one register) **the exoskeleton** — tuned BM25, a generous window, one cross-encoder — **is not a compromise; it is correct.**
> Scale up to heterogeneous registers and a regulatory quality bar and new failure modes emerge, **in Anderson's exact sense: more is different** — and **the endoskeleton** (the portfolio, the derivative corpus, the court) **is what the new physics demands.**

**Then the process that tells you when to stop building: the escalation ladder.**

> **The naive baseline — BM25 plus an LLM — is sacred; it is the null hypothesis, and every component you add is a claim that the null is insufficient.**
> **Build the baseline after the yardstick, never before;** lock acceptability criteria **in writing**; **escalate one component at a time**, measuring at every rung; **run tournaments; ablate ruthlessly.**

**The rungs, for reference:**

```
L1  baseline (BM25 + LLM)
L2  dense lane
L3  hybrid fusion + one cross-encoder   ← where quality typically takes its first jump
L4  late interaction
L5  the full cascade
—— and around them, the rings ——
L6  derivative sidecars      L7  pre-retrieval intelligence
L8  grounding loops          L9  the graph sidecar
L10 the governed concept layer  ← earned only for the governed core, and only where an owner will actually review
```

**The ladder is a practical approximation to the Shapley value:**

$$\varphi_i = \sum_{S \subseteq N \setminus \{i\}} \frac{|S|!\,(n-|S|-1)!}{n!}\Big[v(S \cup \{i\}) - v(S)\Big]$$

> **The only fair division of credit, and the instrument that separates engineering from cargo cult.**
>
> **Build-up (the ladder) samples one ordering; tear-down (ablation) samples another; together they approximate the fair ledger** and expose the two named pathologies:
> - **The Kitchen Sink** — every arXiv technique, **adopted because it might help**
> - **The Sacred Cow** — the component kept **because it was expensive or championed**
>
> **If removing it changes nothing, the cow is beef. Every index must earn its place through ablation.**

---

## The benediction the whole day was building toward

> **What was destroyed in 1940 was not knowledge; it was representations of knowledge** — catalogues, summaries, the cards themselves — **and what made the loss irreversible was that Otlet's derivation pipeline was made of clerks and forty years.**
>
> **Ours can be re-run.**
>
> **Every index we built today is a derivative, regenerable from two things: the corpus, and the recipes this session has written down.**
> **Burn our Mundaneum and we re-derive it** — an iceberg of compute, a few days of pipeline time, a regression suite to prove the rebuild honest.
>
> **The corpus is the only irreplaceable artifact. Guard it, project it many ways, and let the court decide.**

**The closing motto:**

> **Scoop wide and sieve hard; manufacture what the examiner will ask; let cheap judges spend their pennies so the supreme court can afford its verdict; and let every index earn its place, or let it go.**
>
> **One corpus, many catalogues — and the discipline to know, by measurement, which of them to trust.**

---

## The stories and the doctrines they taught (the map the room reconstructed at the end of the day)

> **The stories were not decoration on the mathematics; they were the mathematics before it had notation.**

| Story | Doctrine |
|---|---|
| **The marbles in the sandbox** | **the recall ceiling**: only the scoop decides what is caught |
| **The Mundaneum** | one corpus, many catalogues; **the portfolio without the court** |
| **The CT scanner** | **the tomographic principle**: fusion is the reconstruction; refuse the panopticon |
| **The classmate's forty questions** | **the user is the examiner**; manufacture the derivative corpus |
| **The Berlin paragraph** | **embedding dilution**, and the factoid that rescues the silently dropped answer |
| **The legal rewrite that dropped "irrevocable"** | **retrieve the derivative, generate from the source** |
| **The thousand-dollar intern invoice** | **the sidecar doctrine**: telescopes are not for wristwatches |
| **The million-token bid** | **the long-context mirage**: the window holds evidence; it does not find it |
| **The scoreboard nobody could normalize** | **fuse in ranks**; RRF at k=60 |
| **The decoy on the witness stand** | **the decoy's job ends at retrieval**; rerank the source |
| **The suspiciously cheap terabyte** | **the machine room's ledger**; version skew and the pre-filtered ACL |
| **Galileo's giants** | **scale decides architecture**; exoskeleton to endoskeleton; every index earns its place |
| **The card that came back** | **the governed concept**, seventh artifact, top rung |

---

## What to take away

1. **A retrieval system = a portfolio of representations + a court of adjudication.** Deciding which projections to manufacture and how to adjudicate among them *is* the discipline of retrieval architecture.
2. **The recall ceiling is real: only the scoop decides what is caught.** No reranker, better prompt or bigger model can raise it. Tune the scoop for recall, the sieve for precision.
3. **Absolute similarity thresholds are not portable across embedders.** 0.7 is a different aperture on each model — set it on the sealed set, per embedder, per lane, and reset it whenever the embedder changes.
4. **The Berlin experiment is the number most worth remembering:** the paragraph holding the answer scores **0.64**, the extracted factoid **0.81–0.90** — and at a production threshold of 0.7–0.8, **the correct answer is silently dropped.**
5. **The master pattern: retrieve the derivative, generate from the source.** Every derivative carries a provenance back-pointer — it is **both the citation and the invalidation key.** A derivative corpus without provenance is "a rumor mill with vector search."
6. **Fuse in ranks, not in scores.** A BM25 score and a cosine share no scale. **RRF at k=60 with equal lane weights** is the constitution until a yardstick exists.
7. **The decoy's job ends at retrieval.** The cross-encoder must judge the **source text** — never the synthetic question, rewrite or summary. Also: **parent-level dedup goes before the sieve.**
8. **Pre-filter ACLs, never post-filter.** Post-filtering away eight of ten results has silently turned your top-K into a top-two.
9. **A query must never span embedder versions.** Migrate by dual-write and serve from one index at a time.
10. **Long context is not a substitute for retrieval.** NoLiMa: remove the lexical overlap and 11 of 12 frontier models lose half their accuracy by 32K. **The window holds evidence; it does not find it.**
11. **Every index must earn its place through ablation.** Vendors will write column one (the cost of presence) for you; **only measurement writes column two (the price of absence)** — and a component with an empty column two is decoration, not infrastructure.
12. **Scale decides architecture, not fashion.** At cockroach scale the exoskeleton (tuned BM25 + a generous window + one cross-encoder) is *correct*, not a compromise.
13. **The archaeology of top-K is worth one week:** log the genealogy of every final result and count — **most top results, most of the time, are not raw chunks.** That is the strongest single argument for the multi-representation architecture.

---

## Positioning in one sentence

Week 09 made the corpus something that could be governed; **this week gives the whole load-bearing wall its engineering**: from the representations (BM25 → SPLADE → dense → Matryoshka → ColBERT), through the second corpus (rewrites / factoids / QA pairs / summaries / RAPTOR / community summaries / governed concepts), to the court (fusion → dedup → rescore → cross-encoder), the question side (six pathologies and the transformation cascade), the machine room (HNSW / DiskANN / quantization and three doctrines), and the playbook that decides how much of any of it you can afford (Galileo's giants and the Shapley ledger).

**Next week: the semantic cache — the front door of the house we built today.**

---

## Readings

**Essential (read them in this order):**

| Paper | Why |
|---|---|
| **Cormack, Clarke & Büttcher, *Reciprocal Rank Fusion*** (SIGIR 2009) | Three authors, one page, **k = 60** — the constitution of the court until your hold-out set says otherwise. **Read it to see how little arithmetic beat learned fusion for a decade, and why.** |
| **Chen et al., *Dense X Retrieval*** (arXiv:2312.06648) | Propositions as the retrieval unit — **the monographic principle mechanized**, with FactoidWiki's 257 million cards. **The granularity argument in numbers; read it beside the Berlin experiment.** |
| **Yeh et al., *Decoupled Contrastive Learning*** (arXiv:2110.06848, ECCV 2022) | **The positive leaves the denominator.** Short, and it explains why the house loss is what it is and why small batches stopped being a tax. |
| **Sarthi et al., *RAPTOR*** (ICLR 2024) + **Edge et al., *From Local to Global*** (arXiv:2404.16130) | **The zoom lens and the telescope.** Re-read the GraphRAG paper from Week 05 with the sidecar doctrine and the LazyGraphRAG cost correction in hand. |
| **Modarressi et al., *NoLiMa*** (arXiv:2502.05167) | **The long-context mirage, measured.** This is the evidence you will need the next time someone tells you retrieval is obsolete. |

**Oliver Twist's List (optional):** Kusupati et al., *Matryoshka Representation Learning* (NeurIPS 2022, arXiv:2205.13147) — **dimensionality as a runtime cost knob** · Khattab & Zaharia, *ColBERT* (SIGIR 2020) + Dhulipala et al., *MUVERA* (arXiv:2405.19504) — **late interaction, and the theorem that reduced multi-vector search to single-vector MIPS: the cost objection, born and fallen** · Anthropic, *Introducing Contextual Retrieval* (2024) — **the highest-yield, lowest-glamour upgrade in the catalogue: a dollar per million tokens for a factor of three in retrieval failure** · Zou et al., *PoisonedRAG* (arXiv:2402.07867, USENIX Security 2025) — **five documents in millions, ninety percent steering** · Rayward, *The Universe of Information: The Work of Paul Otlet* (1975) — **the man who built our architecture by hand.**
