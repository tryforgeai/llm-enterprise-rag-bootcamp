# Week 05 — When the Library Becomes a City: Networks, Communities, and the Many Meanings of GraphRAG

*Class summary. Source: Week 5 lesson plan (SupportVectors, Enterprise RAG).*

**The one line of the week:** large graphs develop emergent structure — communities, hubs, small worlds — that no individual edge contains. Every variant of GraphRAG is an attempt to harvest that structure for retrieval, and every variant must pay for the harvest. *The structure is real, the harvest is expensive, and the engineering art is knowing which queries deserve it.*

Week 4 took us from the book to the library. Week 5 goes further: extract the entities in a corpus and the relationships between them, and the volumes dissolve into a web with boulevards, back alleys, dense neighborhoods and famous landmarks. The library becomes a city — and a city can be studied.

---

## Act I — The mathematics of the city

No mention of retrieval all morning. That's deliberate: every piece reappears in the afternoon's systems with its serial numbers barely filed off.

**Euler's move (Königsberg, 1736).** Throw away distance and shape, keep only connection. `G = (V, E)`. The contrast that runs through the day: embeddings live in geometry, graphs live in topology; each sees what the other cannot.

**Adjacency and degree.** `A_ij = 1` if an edge exists (weights in knowledge graphs). `(A²)_ij` counts two-step paths. Row sums give degree `k_i = Σ_j A_ij`; high degree = hub. Every algorithm of the day is linear algebra on `A` in costume.

**Two kinds of randomness.** Erdős–Rényi gives a Poisson degree distribution — everyone middle class, no hubs, tail dies factorially. Barabási–Albert measured real networks and found a power law, `P(k) ~ k^(-γ)`, γ ≈ 2–3: straight on log–log where Poisson falls off a cliff. The generative story is **preferential attachment** — networks grow, and newcomers link to the already-well-connected. Hubs aren't anomalies; they're what growth plus preference always manufactures. Two consequences: hubs make networks **navigable** (short routes pass through them) and **noisy to expand around** (touch a hub, touch everything it touches).

**Small worlds.** Milgram's letters arrived in ~6 hops. Watts–Strogatz: rewire a few edges of a clustered lattice at random and path lengths collapse while clustering barely drops. Knowledge has the same shape — subjects contain topics contain subtopics, with rare cross-domain edges as Granovetter's **weak ties**. New information arrives over those rare bridges. Remember this; it returns as Critique C.

**"Fractal, but in the real world."** Both halves are load-bearing. *Fractal*: communities-within-communities recurs at every altitude, so a hierarchy can exist at all. *Real world*: you get perhaps **2–4 meaningful levels** before a "community" is three houses. This is why Microsoft GraphRAG's hierarchy is 2–4 deep — ask for more and you're summarizing noise.

**Modularity, Louvain, Leiden.** A community is denser internally than *chance* predicts:

```
Q = (1/2m) Σ_ij [ A_ij − (k_i k_j / 2m) ] δ(c_i, c_j)
```

`A_ij` is the edge that's there; `k_i k_j / 2m` is what you'd expect under degree-preserving random rewiring. Modularity sums the surplus. Exact maximization is NP-hard. **Louvain** moves vertices to increase `Q`, then collapses communities and repeats — fast, but it can emit internally *disconnected* communities. **Leiden** repairs this with a refinement phase. Circle the name: Leiden is literally the engine inside Microsoft GraphRAG.

**The Laplacian.** `L = D − A`, and `xᵀLx = Σ_(i,j)∈E (x_i − x_j)²` — the sum of squared disagreements across edges. It's a **smoothness meter**; `ẋ = −Lx` is diffusion on a graph. Door left ajar on purpose: the afternoon's retrieval engine is a first cousin of this diffusion.

---

## Act II — The web of knowledge: triplets, types, three layers

**Triplets.** `T = ⟨head, relationship, tail⟩`. Why not quadruplets? Because the destination is a graph — an edge joins two vertices. The arity is the price of admission to every theorem from Act I.

**Fact vs. schema (ontological) triplets** — the distinction the evening's paper is built on:

```
⟨Einstein, born-in, Germany⟩  ⇝  ⟨person, born-in, country⟩
```

captured by a **typing function** `φ(e) = t`. Facts are isolated and scattered; the types beneath them are the invisible glue.

**The three-layer reading of a corpus:**

| Layer | Contents |
|---|---|
| **Schemas** | types and typed relationships — the ontological skeleton |
| **Facts** | specific entities and their specific relationships |
| **Passages** | the raw chunks — what Weeks 1–4 retrieved over |

Passages ground facts; facts instantiate schemas; schemas gather facts; facts point home to passages.

**Who extracts — the Scooby-Doo problem.** Pre-LLM, SMEs hand-crafted triplets: curated, domain-bounded, priced in man-years. LLMs made extraction cheap and simultaneously noisy — the machine transcribes whatever the text says, including the margin note "pending Scooby-Doo's review," now a fact sitting next to the physics. Curation filters at authorship time; extraction defers the filtering problem to you.

**Hubs return: the generic-entity problem.** In a knowledge graph we can name the hubs precisely — *United States, Microsoft, Protein, Person*. Preferential attachment guarantees them; extraction noise inflates them. Expand two hops from "USA" and you've retrieved the encyclopedia.

---

## Act III — The many meanings of GraphRAG

### 1. The oldest meaning: neighbor expansion

Keep a graph on the side; at query time find the query's entities, walk one or two hops, append the neighbors. Genuinely useful for **multi-hop factual queries** ("who is the CEO of the company that acquired X?"). But it is *local* — it never sees communities or themes, and it degrades exactly when the graph gets interesting, because two hops passes through a hub and a hub's neighborhood is everything.

### 2. Microsoft GraphRAG (2024) — "From Local to Global"

The question: what about queries whose answer is in no passage? *"What are the underlying leitmotifs of this novel?"* Themes are emergent, passages are local — every architecture from Weeks 1–4 is structurally incapable of answering.

1. **Extract** — LLM sweeps chunk by chunk into one corpus-level entity graph. Entity resolution ("FDA" vs. "Food and Drug Administration") is unglamorous and load-bearing: resolve poorly and every downstream step inherits the fracture.
2. **Detect** — Leiden over the entity graph → the 2–4 level hierarchy.
3. **Summarize** — a narrative summary per leaf community, merged upward. The stroke of genius: a community summary is a derivative artifact whose subject is *a piece of the corpus's structure*. Give it 2,000 physics papers and the thermodynamics community's summary is the definitive textbook chapter as this corpus would write it.
4. **Map–reduce at query time** — ask each summary, synthesize the partials.

**RAPTOR vs. GraphRAG:** same hunger (global sense), same move (cluster, then summarize, recursively), different substrate — RAPTOR gathers passages that *sound alike*, GraphRAG gathers entities that *interact*.

**The invoice.** One public-domain book through Microsoft's code ≈ **$1,000**. An LLM call per chunk at extraction, then leaf summaries, merged summaries, summaries of summaries — and when the corpus changes it all rots and the meter restarts. Every successor system is an answer to this bill.

### 3. The in-betweens, at altitude

- **LazyGraphRAG** — Microsoft's own second thought. *Defer*: light indexing up front, expensive summarization at query time over the touched subgraph. Indexing cost falls ~2 orders of magnitude. Fine print: benchmarks report averages, and the truly global query is exactly where query-time localization silently returns an *incomplete* answer rather than a wrong one — the harder failure to catch.
- **LightRAG** — dual-level retrieval over an entity–relation graph, built for incremental updates and low cost. The ecosystem declaring the original pipeline over-built for many corpora.
- **HippoRAG** — hippocampal indexing theory. Entity graph, no community pyramid; at query time seed the query's entities and run **personalized PageRank**. The morning's diffusion operator, put to work.

### 4. MemGraphRAG — three diseases and a shared memory

**Diagnosis.** One root defect: *isolated, fragment-level extraction* — each chunk processed alone with no global view. (Community detection builds themes *afterwards*, out of whatever the isolated extractions produced, and hopes for the best.) Three diseases: **thematic irrelevance** (the copyright notice filed beside the physics), **logical inconsistency** (contradictions bubble into summaries and sit there looking confused), **structural fragmentation** (the key idea that never enters the graph in one piece).

**Cure, two commitments.** A **shared memory** — the three layers in one persistent global store every agent reads and writes during processing. And a **society of agents**: extraction (all three layers at once, every fact keeping an evidence link home), conflict detection, conflict resolution. The **conflict taxonomy**: *granularity* (Berkeley vs. United States — containment), *temporal* (both true, time-indexed), *mutually exclusive* (only one survives).

**Construction.** Schemas land in a staging area; a schema is promoted to the stable pool only when `Freq(s) ≥ τ`. The core thesis, baldly: **frequency determines significance**. Promoted schemas bring their facts; facts bring their passages. Everything else is let go.

**The self-experiment (running the paper on itself).** Twelve passages → **38 fact triplets, 27 distinct schemas**. Champion at frequency 5: `⟨method, uses, technique⟩` — "sunrises." At frequency 3: `⟨process, causes, deficiency⟩`, carrying the paper's entire diagnosis. At frequency 1: the paper's three agents — its titular machinery — sitting *exactly beside* `⟨work, licensed-under, license⟩`, the CC-BY notice. **Identical frequency, opposite worth.**

Walk the staircase: τ=4 leaves one schema and five disconnected edges — structural fragmentation, the very disease the paper set out to cure; τ=3 restores the diagnosis; τ=2 restores PageRank; and the only threshold that readmits the three agents is τ=1, which readmits the copyright notice holding their hand. **No rung gives signal without noise, because signal and noise share the same frequency.** Not a small-corpus artifact: STEM knowledge is Zipfian, and the most valuable things are often said exactly once. And the amputation happens at *graph-building* time — **you cannot retrieve what was never admitted to the graph.**

**Retrieval: three cities of lights.** No communities, no summaries. Embed every triplet as text, embed the query, and wave it over three cities — schema, fact, passage. Bulbs light by cosine similarity:

```
Entities:  P_init(e) = (1/|F_e|) Σ_{f∈F_e} Sim(q, f)
Types:     P_init(t) = (1/|S_t|) Σ_{s∈S_t} Sim(q, s) · 1/log(deg(t)+1)
Passages:  P_init(p) = α·Sim(q, d_p) + σ( Σ_{e∈E_p} IDF(e) / (|E_p|+1) ),  α = 0.05
```

Three choices worth naming: **mean, not sum**, for entities — summing would hand runaway scores to hubs; **hub suppression** for types — a log damper, a leash not a muzzle (degree 10→100 moves the penalty only 1→2); and for passages a 95% **dampening** plus an **IDF-weighted entity density** through a sigmoid. The bet: the rich information lives in the upper two layers; passages are grounding, not the main current.

**The honey and the springs.** Scores are then redistributed by personalized PageRank. Build `A` over all cross-layer links, form `W = D⁻¹A` (*split, don't dump*), stack the initial scores into `v⁽⁰⁾` — **semantic energy** — and iterate:

```
v^(k+1) = (1−λ) W v^(k) + λ v^(0),     λ = 1/2
```

The query is where you pour the honey, and the seed nodes are **springs, not a one-time pour**: each round half of what a node holds flows outward in proportion to `W`, while `λv⁽⁰⁾` re-injects the original energy at the seeds. Traveling honey halves at every hop (½, ¼, ⅛), so it glazes a one-or-two-hop neighborhood before the leash yanks it back — that is what "λ prevents semantic drift" means mechanically. Nobody ever *walks* the graph; you let the honey settle and skim the richest pools.

Convergence is a contraction (Banach), error shrinking like `(1−λ)^k` — ten rounds gives ≈0.1%. **One knob, two jobs:** λ sets both locality and convergence speed. Result: ten-ish sparse matrix–vector products, no community detection, no summaries, **no LLM calls at query time** — **0.061s** per retrieval, against 1.6s for HippoRAG and 11s for LightRAG. The $1,000 invoice, answered in sixty milliseconds. (For the GNN-minded: precisely APPNP — PPR as a propagation rule, minus learned weights.)

### Three critiques, one disease

A fair reading credits before it cuts: the diagnosis is real and well measured, and the machinery is genuinely nice. Then:

- **A — "grounding" is a category error.** When passages underdetermine the answer, the resolution agent still always resolves, and the LLM judge's parametric priors lean it one way: the judge stops reading and starts remembering. "Grounded" means traceable to *some* text, never to *true* text. Underneath: correlated errors — all three agents run on the same LLM, so the "society of agents" is one model wearing three prompts. Wikipedia-derived benchmarks can't catch it, because on the hard cases the parametric fallback and the gold answer coincide by construction.
- **B — contradictions should be first-class citizens.** Two departments reporting different revenue for the same quarter isn't noise to average away — it's a finding. And the taxonomy convicts itself: temporal facts are both true, granularity pairs deserve a subsumption edge; only mutually-exclusive is real contradiction. The resolution agent discards true information in two of its own three cases. *They built a seismograph and wired it to erase earthquakes from the record.* The fix is nearly free: let detection **annotate** — a `conflicts-with` edge, both provenances, a confidence, a temporal validity — instead of letting resolution delete. This also dissolves Critique A: never commit at construction time and you never invoke the fallible judge.
- **C — frequency is not importance.** Frequency counts repetition; it has never measured importance. Note the irony: in the construction half frequency is *signal* (rare schemas executed), in the retrieval half it is *noise* (hub suppression penalizes the common, IDF rewards the rare, mean-not-sum refuses to reward repetition). Their retrieval side would boost the very gem their construction side erased. Fix, again nearly free: the candidate tier already exists. **Demote, don't delete.**

**Through-line.** Each critique is an eager, information-destroying commitment made at construction time — the moment with the *least* context — when it could be deferred to query time, the moment with the most. Three words: **preserve, then decide.**

---

## The practitioner's ledger

**The pattern — global sensemaking.** GraphRAG earns its keep on exactly one class of query: the one whose answer is a property of the corpus's *structure*, not of any passage in it. "What are the major regulatory concerns across these 500 earnings calls?" The signature: a human answering it would have to read everything and form a mental model — and the mental model *is* the entity graph with its communities. Concretely: analytical dashboards fed by sensemaking queries, periodic corpus briefings, investigation and root-cause work where contradictions and weak ties are the gems.

**The anti-patterns** — name them without mercy, because the field's disappointments are mostly mis-routed queries.

- **The point query.** A single passage answers; plain retrieval finds it in milliseconds for a fraction of a cent. Routing it through community summaries is using a telescope to read your wristwatch — slower, costlier, often *worse*, because synthesis blurs the crisp local fact.
- **The small corpus.** Emergence needs mass. You cannot detect ocean currents in a bathtub. Below hundreds of documents the Weeks 1–4 cascade is strictly better.
- **The real-time lane.** Map–reduce is seconds-per-query and the pipeline is a batch animal. (MemGraphRAG's 60ms helps, but construction cost and freshness burden remain.)
- **The everything-graph.** Shunting the whole corpus through construction because the demo was impressive.

**The sidecar.** GraphRAG is always a sidecar — it extends the motorcycle, never replaces it. So you route: **high-value documents into the graph** (the contracts, the filings, the research collection, the customer-voice corpus — the rest of the swamp stays in the plain index, perfectly retrievable, unmapped), and **high-value queries through the graph** (a router classifies local vs. global using the litmus pair — "what are the leitmotifs?" = global, "what happened at the end?" = local). The global minority, perhaps **5–15%**, is escorted to the sidecar — and those few are disproportionately the queries executives ask, the ones that define your system's intelligence ceiling.

**Capex–opex:** full GraphRAG pays at indexing with cheap queries; Lazy pays per query with cheap indexing. Database engineers ran this trade for decades under the name *materialized views*, and the answer was always the same: it depends how often the view is read. **Precomputation is a bet on query volume.** And keep the ledger honest about quality too: GraphRAG **amplifies extraction quality** — garbage in, confidently narrated garbage out.

---

## Labs

1. **Corpus → graph.** LLM extraction over 50–100 chunks into NetworkX. Before any algorithm: *look*. Degree distribution on log–log, find the heavy tail yourself, confirm hubs are generic entities, find three entity-resolution failures and measure how merging them changes the hub list.
2. **Communities and the hierarchy.** Leiden at 2–3 resolution levels; measure modularity against a degree-preserving random rewiring (structure is a surplus over chance, so compute the chance). At what level does subdivision stop being meaningful?
3. **Community summaries and one global question.** A small Microsoft-GraphRAG pipeline with the cost ledger open and every LLM call counted. Map–reduce vs. plain top-k on the same global question — the gap is the sensemaking gap, and you'll have paid for it.
4. **Honey by hand.** Three-layer graph over a dozen passages; implement the three initializations, iterate ten times printing `‖v⁽ᵏ⁺¹⁾ − v⁽ᵏ⁾‖` to see Banach's `(0.5)^k`. Vary τ to reproduce the staircase; vary λ to feel locality change (0.1 wanders, 0.9 never leaves home).
5. **Router tournament.** Query set spanning point / mid-scope thematic / truly global, run through the Weeks 1–4 cascade, the Lab 3 pipeline, the Lab 4 miniature, and a routed hybrid. The deliverable is the honest table: which machinery pays rent on which band — with point-queries-through-the-graph *measured*, not merely believed.

---

## Essential readings

Edge et al., **From Local to Global** (the foundational paper) · Wu et al., **MemGraphRAG** (KDD 2026 — read with the three critiques in hand) · Traag et al., **From Louvain to Leiden** · Barabási & Albert, **Emergence of Scaling in Random Networks** · Barabási, **Network Science** (free online; Ch. 2, 4, 9) · Gutiérrez et al., **HippoRAG**.

*Optional:* Newman (modularity) · Watts & Strogatz (small worlds) · Granovetter (weak ties) · LazyGraphRAG + BenchmarkQED · Broido & Clauset (*Scale-Free Networks Are Rare*) · Anderson (*More Is Different*) · Gasteiger et al. (APPNP).

---

## The take-away

> Large graphs develop emergent structure — communities within communities, hubs, small worlds — that no edge contains. A knowledge graph inherits that structure from knowledge itself. Every GraphRAG is a bet that harvesting the structure is worth the invoice; the good architect routes the sensemaking few to the graph, keeps the point-query many on the plain index — and **preserves, before deciding**.

The morning's mathematics returns in the afternoon with its serial numbers intact: Leiden inside Microsoft's pipeline, the degree distribution inside hub suppression, the Laplacian's diffusion inside personalized PageRank.
