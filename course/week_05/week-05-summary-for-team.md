# Week 05 Summary — When the Library Becomes a City: Networks, Communities, and the Many Meanings of GraphRAG

**Date:** 2026-07-04 · **Source:** `course/week_05/week-5-summer-lesson-plan.pdf` (Asif Qamar, SupportVectors), the MemGraphRAG paper reading, and the Week 05 lab repos (`labs/week5.2/`)

---

## TL;DR

The whole week compresses into one sentence:

> **The structure is real, the harvest is expensive, and the engineering art is knowing which queries deserve it.**

Large graphs develop **emergent structure** — communities, hubs, small worlds — that **none of their individual edges contains**. A knowledge graph inherits that structure from knowledge itself. Every variant of GraphRAG is an attempt to harvest that emergent structure for retrieval, **and every variant must pay for the harvest.**

Week 04 climbed from the book to the library: we stopped indexing only what the author wrote and began manufacturing derivative artifacts. But a library is still a place where each volume stands alone, spine by spine. Week 05 does something different in kind:

> **Extract the entities in a corpus and the relationships between them, and the volumes dissolve. The library becomes a city.**

And a city can be studied. It has a mathematics — the mathematics of large graphs — and that mathematics is **not decoration**. The day's structure is the argument:

```
Morning   the mathematics of the city    (no mention of retrieval — deliberately)
Afternoon the corpus becomes a city      (triplets, types, three layers)
Evening   the boulevard of systems       (MS GraphRAG, MemGraphRAG)
Close     the ledger                     (patterns, anti-patterns, sidecar)
```

The morning's mathematics **reappears in the afternoon with its serial numbers barely filed off** — Leiden inside Microsoft's pipeline, the degree distribution inside hub suppression, the diffusion operator inside personalized PageRank. That recurrence is the pedagogy.

---

## Act I: The Mathematics of the City

Nothing in Act I mentions retrieval. That is deliberate — and every piece of it comes back after lunch.

### Euler's move

Graph theory was born in a city. Königsberg, 1736, four landmasses and seven bridges, and Euler settled the Sunday puzzle — **no** — by throwing away everything a mapmaker would keep: distances, island shapes, river widths. What remained were four dots and seven lines.

```
G = (V, E),  E ⊆ V × V
```

> **Embeddings live in geometry; graphs live in topology.** Euler's move — discard geometry, keep connectivity — is the move an embedding model refuses to make.

When we throw away the prose of a corpus and keep only its entities and relationships, **we are making Euler's move.** We will lose things; we will also see things no amount of prose-reading could show. That trade is the whole week.

### The adjacency matrix — where a graph becomes calculable

```
A_ij = 1 if an edge joins i and j, else 0     (weights in a knowledge graph)
```

Powers of `A` count walks: `(A²)_ij` is the number of two-step paths. **Every graph algorithm we meet today — community detection, PageRank, spectral analysis — is, under its costume, linear algebra on `A` or on matrices derived from it.**

The row sums give the first vital statistic, the **degree**:

```
k_i = Σ_j A_ij
```

> File this away: **MemGraphRAG's retrieval engine is, almost literally, "build A over three layers, normalize it, and iterate a matrix–vector product ten times."** The adjacency matrix is not background; it is the machine.

### Two kinds of randomness — and why real networks have hubs

| | Erdős–Rényi | Real-world networks |
| --- | --- | --- |
| **Model** | Flip a coin for every pair, probability `p` | Grow by **preferential attachment** |
| **Degree distribution** | Poisson, `P(k) = e^{-⟨k⟩}⟨k⟩^k / k!` | Power law / heavy tail, `P(k) ~ k^{-γ}`, γ ≈ 2–3 |
| **On log–log axes** | Plummets like a cliff | **Ruler-straight line** |
| **Hubs** | Essentially impossible — the tail dies factorially | **Expected.** Hubs are what growth-plus-preference manufactures, always |
| **Modularity achievable** | Q ≈ 0.32 (salt-and-pepper; close to what sparse randomness fakes) | Q ≈ 0.85 (fourteen clean neighborhoods on the LFR benchmark) |

**Barabási's deep contribution was not the observation but the generative story.** A new web page links to Wikipedia, not to a random page; a new paper cites the famous paper. The rich get richer — the Matthew effect — and rich-get-richer growth **provably** yields the power law.

Two consequences to hold, one for each half of the day:

1. **Hubs make networks navigable** — they are the airports through which short routes pass, and they are why small worlds are possible at all.
2. **Hubs make networks noisy to expand around** — touch a hub and you touch everything it touches, most of which has nothing to do with you.

> Consequence 2 is the one-line explanation of why naive neighbor-expansion GraphRAG **degrades exactly when the graph gets interesting.**

*(A calibration note the lesson plan insists on: Broido & Clauset, "Scale-Free Networks Are Rare" — real networks are heavy-tailed, but pristine power laws are rarer than the folklore claims. **Heavy tails and hubs survive the critique; exponent worship does not.**)*

### Small worlds and weak ties

Milgram's 1967 letters arrived in about **six** forwardings. Watts and Strogatz explained it: take a highly clustered lattice and **rewire just a few edges at random**. Clustering barely drops; path lengths collapse. A handful of bridges is enough to make a world small. Add Barabási's hubs and you have the architecture of essentially every real network.

Now translate to knowledge. STEM contains physics and CS; ML contains neural networks; within those, transformers, and within those, attention — dense neighborhoods at every level. **And the strands cross:** logistic regression lives simultaneously in ML, medicine, econometrics, and psychology; entropy belongs to thermodynamics, information theory, and language modeling.

> **Those cross-listings are the weak ties** — the long-range shortcuts of the knowledge city, **the bridge between provinces that a frequency filter is most tempted to cut.** (Remember this. It becomes Critique C.)

### Fractal structure — but in the real world

Both halves of the phrase are load-bearing.

- **The fractal half:** the communities-within-communities pattern is not an artifact of one level of description; it recurs, and the same detection machinery finds it at every level. That recursion is what lets Leiden hand us a **hierarchy** rather than a flat partition.
- **The real-world half:** you cannot keep zooming forever. A real network gives you perhaps **two, three, four meaningful levels** before "community" stops meaning anything. A neighborhood of three houses is just three houses.

> **The finite zoom depth is not a disappointment; it is a design parameter.** Microsoft GraphRAG's hierarchy is typically 2–4 levels deep precisely because that is how many levels of genuine structure a real entity graph holds. **Ask for more and you are summarizing noise.**

Scale-invariance is the mathematical name for something we already believe pedagogically — that subtopics sit within topics within subjects. When you feel a knowledge graph ought to have emergent themes at several granularities, **you are not being poetic. You are asserting scale-invariance, and the assertion is empirically true of large knowledge graphs.**

### Modularity, Louvain, and the algorithm to circle

A community is a set of vertices more densely connected internally than externally. More densely **than chance**. Newman's modularity:

```
Q = (1/2m) Σ_ij [ A_ij − k_i k_j / 2m ] δ(c_i, c_j)
```

Read the bracket aloud, because it carries the whole idea: `A_ij` is **the edge that is there**; `k_i k_j / 2m` is **the edge you would expect by chance** if the graph were randomly rewired while preserving everyone's degree. Modularity sums the **surplus of actual over expected**, over pairs inside the same community.

Exact maximization is NP-hard, so the field runs on good greedy algorithms:

| Algorithm | What it does | The catch |
| --- | --- | --- |
| **Louvain** (2008) | Shuffle vertices between communities when it raises Q; collapse each community to a super-vertex; repeat | **Can output communities that are internally disconnected** — islands filed under one name with no street between them |
| **Leiden** | Adds a refinement phase | **Guarantees every reported community is well-connected**, at every level of the hierarchy |

> **Circle the name.** Leiden is not algorithmic trivia. It is, literally, **the engine at the heart of Microsoft GraphRAG.** The morning's mathematics does not *resemble* the afternoon's system; **it is** the afternoon's system.

*(Family resemblance to Week 04: RAPTOR clustered chunks by embedding proximity; modularity clusters vertices by **relational surplus**. RAPTOR asks "who sounds alike?"; modularity asks "who is wired together?" Neither subsumes the other, which is why the mature architecture keeps both.)*

### The Laplacian — one definition, and a door left ajar

```
L = D − A          (D = diagonal matrix of degrees)

x ᵀ L x = Σ_(i,j)∈E (x_i − x_j)²
```

**The Laplacian is a smoothness meter:** zero when connected neighbors agree, growing with every edge that straddles a disagreement. Any process that smooths differences across edges — heat through a plate, a rumor through a village, **a score bleeding from a vertex to its neighbors** — is governed by this matrix. The diffusion equation on a graph is `ẋ = −Lx`.

Two things to carry:

- **The image:** the eigenvectors of `L` are the graph's standing waves; the **Fiedler vector** (second-smallest) is the gentlest way to split the graph in two — the split falls across the fewest, weakest edges, where the graph itself wants to come apart.
- **The teaser:** this afternoon a retrieval system will pour a query's relevance onto a few vertices and let it spread in a controlled way. **The machinery it reaches for is a first cousin of this diffusion: a random walk with a leash, named PageRank — personalized.**

---

## Act II: The Web of Knowledge — Triplets, Types, and Three Layers

### Knowledge is an interconnected web

```
G = { T_i },   T_i = ⟨head, relationship, tail⟩
```

Why triplets and not quadruplets? **Because the destination is a graph** — an edge joins two vertices, so a relation binds two things, with the relation riding on the edge. **The arity is not a modeling whim; it is the price of admission to every theorem from Act I.**

### Fact triplets vs. schema (ontological) triplets — the distinction the evening is built on

```
⟨Einstein, born-in, Germany⟩   ⇝   ⟨person, born-in, country⟩

typing function:  φ(e) = t     φ(Einstein) = person,  φ(Germany) = country
```

**Facts are isolated and scattered; the types beneath them are the invisible glue.** One schema gathers under itself a wide family of facts.

*(Philosophical footnote worth keeping: the Samkhya school, tracing to Kapila, held that **if a thing belonged to no category, we could not recognize it at all.** Recognition is categorization. Twenty-five centuries later the same instinct resurfaces wearing a KDD paper's notation, as the typing function φ. And a warning for the OO-minded: it rhymes with classes and objects, but **do not dig** — no inheritance, no methods, no properties.)*

**The payoff is a three-layer reading of any corpus:**

| Layer | Contents | Relation to the others |
| --- | --- | --- |
| **Schemas** | Types and typed relationships — the ontological skeleton | Schemas **gather** facts |
| **Facts** | Specific entities and their specific relationships, mined from passages | Facts **instantiate** schemas; facts **point home** to passages |
| **Passages** | The raw text — exactly what Weeks 1–4 have been retrieving over | Passages **ground** facts |

**MemGraphRAG lives entirely inside this picture. Park it somewhere safe.**

### Who extracts: the SME, the machine, and the Scooby-Doo problem

Pre-LLM, knowledge graphs were built by subject-matter experts hand-crafting triplets — effort that scaled with man-hours, which is why only governments, Google, and pharma could afford serious ones. Then LLMs arrived: ask for triplets and triplets pour out.

But play the comparison game. **The SME knows the context** — the result is domain-bounded, distilled, curated. **The machine transcribes whatever the text happens to say.** And corpora say all sorts of things. Somewhere in a margin sits an annotation — *pending Scooby-Doo's review* — and now `⟨document, pending-review-by, Scooby-Doo⟩` is a fact in your knowledge graph. Copyright notices, boilerplate footers, tracked-changes debris: the machine files them all, diligently, next to the physics.

> **Curation is a filter applied at authorship time; extraction defers the filtering problem to you.**

**The entire research lineage of Act III — from Microsoft's frequency-weighted edges to MemGraphRAG's promotion thresholds — is a series of attempts to answer the noise question the SME's salary used to answer.**

### Hubs return: the generic-entity problem

A knowledge graph extracted from a large corpus **is** a real-world network, so everything from Act I applies verbatim. And here we can say precisely who the hubs are: **the generic entities.** *United States. Microsoft. Protein. Person.* Preferential attachment guarantees their existence; **extraction noise inflates them further.**

> Expand two hops from "USA" and you have retrieved the encyclopedia.

**Every serious system this afternoon carries a scar shaped like this paragraph** — MemGraphRAG's logarithmic **hub suppression**, and the community-detection approaches quietly relying on modularity's `k_i k_j / 2m` term, **which is precisely a correction for expected hub-degree.**

> **The mathematics of Act I is not scenery; it is scar tissue.**

---

## Act III: The Many Meanings of GraphRAG

"GraphRAG" has meant more things than any name should be asked to mean. The walking tour, in order:

### 1. The oldest meaning: neighbor expansion

Keep a knowledge graph on the side; at query time extract the user's entities, find them in the graph, walk one or two hops, append the neighbors to the query. Call it **graph-augmented RAG** to keep it distinct.

**Genuinely useful for the right question** — multi-hop factual queries ("who is the CEO of the company that acquired X?") need exactly a relational bridge that embedding similarity does not supply.

**But mark its character: it is local.** It never sees the graph's large-scale structure, because **no walk of two hops sees a continent.** And the morning's hub warning, cashed in: walk two hops from any entity of interest and you will, with high probability, pass through a hub — **the expansion floods with generic noise precisely when the graph is large enough to be interesting.**

### 2. Microsoft GraphRAG (2024): harvesting the emergence

*Edge et al., "From Local to Global" — a title that is a thesis.*

**The question:** what about queries whose answer is not in any passage — the **global sensemaking** queries the literature calls query-focused summarization?

> *"What are the underlying leitmotifs of* The Mill on the Floss*?"* — work out where that query's embedding lands relative to the chunks. It pulls up nothing useful, **because no chunk says the theme.** Themes are emergent; passages are local. **Every architecture of Weeks 1–4 — chunks, factoids, rewrites, QA pairs — is structurally incapable of answering.**

**The litmus pair to keep permanently:**

| Query | Kind | Why |
| --- | --- | --- |
| *"What are the underlying leitmotifs of the novel?"* | **Global** | The answer is a property of the whole |
| *"What happened to Tom and Maggie at the end?"* | **Local** | A single passage answers: the flood took them |

**The pipeline, in four movements:**

1. **Extract.** An LLM sweeps chunk by chunk, extracting entities and relationships — fact triplets — merged into one corpus-level entity graph. **Entity resolution** (is "FDA" the same vertex as "Food and Drug Administration"?) is unglamorous and **load-bearing**: resolve poorly and the graph fragments, and every downstream step inherits the fracture.
2. **Detect.** Run **Leiden** over the entity graph — the circled name, optimizing exactly the modularity Q from the morning. Out comes the hierarchy: two to four meaningful levels, the fractal-but-real structure made operational.
3. **Summarize.** *The stroke of genius.* Write a narrative summary of each leaf community — what entities it contains, how they relate, what theme emerges — then merge leaf summaries into parent summaries, up the hierarchy. **The theme of each sub-community, which was emergent and unwritten, now has a place to live.** A community summary is a Week 04 derivative artifact **whose subject is a piece of the corpus's structure.**
4. **Map–reduce.** At query time the global question is put to the community summaries (**map**), and the partial answers are synthesized (**reduce**) into one global response.

**What the pipeline has actually manufactured** — the most beautiful idea of the week. Suppose the corpus is two thousand physics papers and Leiden finds a dense community whose entities are *entropy, the second law, Carnot cycle, Boltzmann distribution, free energy.* The community summary of that cluster is, in effect, **the definitive textbook chapter on thermodynamics as this corpus would write it** — nourished by every paper that contributed an edge.

> **RAPTOR versus GraphRAG in one breath:** same hunger (global sense), same move (cluster, then summarize, recursively), **different substrate** (embedding space versus entity graph). **RAPTOR gathered passages that sound alike; GraphRAG gathers entities that interact.** A methodology question — *"what is the overall approach of this study?"* — is RAPTOR's; a cross-document relational question — *"what are the major drug–gene interaction themes?"* — is GraphRAG's. **The mature system indexes both and routes.**

### 3. The invoice

> **One book, $1,000.**

When the GraphRAG paper came out, an intern was handed a single public-domain book — *The Brothers Karamazov* — and Microsoft's code, and asked for the OpenAI key "for a few LLM calls." The next morning: a bill for close to a thousand dollars. *(Perhaps he ran it a few times. But there is the datum.)*

Now scale to an enterprise corpus:

- **Extraction** is an LLM call **per chunk**
- **Community detection** is cheap by comparison but not free
- Then you owe **leaf summaries, merged summaries, summaries of summaries** — LLM calls all the way up the hierarchy
- And when the corpus changes, the graph and the summaries **rot**, and the meter starts again

> **Every architectural choice in the successor systems — Lazy's deferral, Light's slimming, Hippo's and MemGraph's refusal to do community detection at all — is an answer to this invoice.**

### 4. The in-betweens, at a respectful altitude

| System | The one design choice to remember | The fine print |
| --- | --- | --- |
| **LazyGraphRAG** | **Defer.** Lightweight indexing up front (noun-phrase extraction, a coarse graph); do the expensive summarization **at query time** over the subgraph the query touches. Indexing cost falls ~**two orders of magnitude**; benchmark quality holds | Benchmarks report **averages**, and the truly global query — whose answer is near nothing — is exactly where query-time localization can silently return an **incomplete** answer rather than a wrong one. That is the harder failure to catch |
| **LightRAG** | **Slim the machinery.** Dual-level retrieval over an entity–relation graph, engineered for incremental updates and low cost | Read it as the ecosystem's declaration that the original pipeline was **over-built for many corpora** |
| **HippoRAG** | **No community detection at all.** Inspired by hippocampal indexing theory: build an entity graph, seed the query's entities, run **personalized PageRank** to let relevance flow to structurally associated entities | *(Hippocampus, not hippopotamus — and no "Graph" in the name despite the graph at its heart.)* This is the morning's diffusion operator put to work, and **exactly what MemGraphRAG inherits** |

### 5. MemGraphRAG: three diseases and a shared memory

*Wu et al., the paper we gave a full public evening to.*

**The instructor's assessment, stated up front:** *a remarkable idea; in implementation, still a work in progress.* Very, very good at **diagnosing a disease**; the core ideas are beautiful. *(YouTube says it "completely wipes out traditional RAG." YouTube tends toward the hyperbolic.)*

**The diagnosis.** Existing GraphRAG methods share one root defect: **isolated, fragment-level extraction** — each chunk processed alone, in the dark, with no global view. *(A surprise on first reading: wasn't GraphRAG's whole point the global view? Not quite — community detection builds themes* afterwards*, out of whatever the isolated extractions produced, and hopes for the best.)* From that root defect, three diseases:

| Disease | What it looks like |
| --- | --- |
| **Thematic irrelevance** | The copyright notice in a thermodynamics book, the Scooby-Doo annotation — filed beside the physics as if it were physics |
| **Logical inconsistency** | Contradictions summarized together. Nothing in classic GraphRAG stops the top-level summary from reading *"Napoleon attacked Russia, which was good and bad."* Contradictions bubble to the top and sit there, looking confused |
| **Structural fragmentation** | The key idea that never makes it into the graph in one piece, because chunking took a knife to it. **Any time you chunk, you risk the apple with half a worm** |

**The cure, in two commitments:**

1. **Shared memory** — not RAM, but working memory in the agent-architecture sense: the three layers from Act II held in **one persistent global store that every agent reads and writes while the corpus is processed.** One-line thesis: *stop extracting in isolation; give every agent a shared, global context.*
2. **A society of agents** — an **extraction agent** (reads chunks, extracts all three layers at once, every fact keeping an evidence link home); a **conflict-detection agent** (scans the fact layer for contradictions); a **conflict-resolution agent** (adjudicates by scanning the corpus for provenance).

**The conflict taxonomy — three kinds:**

| Type | Example | What it actually is |
| --- | --- | --- |
| **Granularity** | John born in Berkeley vs. born in the United States | **Containment**, not contradiction |
| **Temporal** | Biden was president; Trump was president | **Both true**, time-indexed (46th; 45th and 47th) |
| **Mutually exclusive** | Einstein born 1879 vs. 1880 | **Genuine contradiction** — only one survives (1879) |

*And the hard question the taxonomy raises but does not ask loudly: what happens when the corpus offers irreconcilable statements — Berkeley vs. Fremont — and no third passage settles it? **Hold that. It returns as Critique A.***

**And the economic promise: no community detection at all.** Throw the pyramid away and you inherit the obvious question — you sit atop a giant three-layer graph; how do you make sense of it at query time? The answer is the classical machinery HippoRAG foreshadowed, **and it is why their retrieval finishes in about sixty milliseconds.**

### Building the graph: candidates, promotion, and the jury pool

The extraction agent fills a staging area — a bucket of **candidate schemas**. Nothing is promoted to the stable pool by default. A schema is promoted only when its empirical frequency clears a threshold:

```
Freq(s) ≥ τ
```

> **The construction phase's core thesis, stated baldly: frequency determines significance.** A recurring ontological pattern is probably important; a rare one is probably noise.

Promoted schemas bring their fact triplets; those facts bring their passages. **And the passages left behind?** A passage with no promoted fact becomes a lone island in the passage pool — a dead end **the structured retrieval will never reach** (plain RAG can still see it; the graph cannot).

> It is somewhat like jury duty — except that in jurisprudence the ones sent home are the happy ones. **In this graph, they are not.**

### The experiment: running the paper on itself

We took **the paper itself** as the corpus — a dozen good passages — and ran the paper's own pipeline on them. **12 passages → 38 fact triplets → 27 distinct schemas.** Then the schema frequency table, exactly as prescribed:

| Schema | Freq | Worth |
| --- | ---: | --- |
| `⟨method, uses, technique⟩` | **5** | *"Sunrises."* How many of us are impressed to learn that methods use techniques? |
| `⟨process, causes, deficiency⟩` | **3** | The schema carrying **the paper's entire diagnosis** — its three diseases. You would give it a star |
| The paper's **three agents** — its titular machinery | **1** | The long tail |
| `⟨work, licensed-under, license⟩` — **the CC-BY copyright notice** | **1** | Sitting *exactly beside* the three agents |

> **Identical frequency; opposite worth. A counter cannot tell the paper's title from its legal footer — they are the same number.**

**Walk the staircase:**

| τ | What survives |
| ---: | --- |
| **4** | **One schema of twenty-seven** — the banality — and its five surviving facts form five disconnected "X uses Y" edges: **a shattered graph that is itself a textbook case of structural fragmentation, the very disease the paper set out to cure** |
| **3** | The diagnosis and the architecture return |
| **2** | PageRank walks back in |
| **1** | The three agents and RAG's very purpose return — **holding hands with the copyright notice** |

> **There is no rung that gives signal without noise, because signal and noise share the same frequency.**

**Why this is not an artifact of a tiny corpus:** STEM knowledge is **Zipfian**. The most valuable things live far out in the tail, often said exactly once in a whole textbook — because anything anyone does creates a subfield, and **the bridges between fields are, by definition, rare.** Granovetter's weak ties, from the morning's margin.

**And the part you cannot engineer around: the amputation happens at graph-building time.** Be as clever as you like at retrieval; **you cannot retrieve what was never admitted to the graph.**

*In our surprisal idiom from Week 02: information content is `−log p`, concentrated precisely where frequency is lowest. **A frequency filter is therefore a surprisal-minimizer — an index optimized to forget its most informative facts.***

**Fairness demands the counterweight:** the paper's own pilot study shows that removing low-frequency triples **slightly improves accuracy** on their benchmark data, and our little experiment does not refute their tables. It illustrates what their tables **cannot show**: on a Zipfian technical corpus, frequency and importance are different quantities. **The idea is very good; they need a different proxy for importance.**

### Retrieval: three cities of lights

No communities, no summaries. Embed every triplet as plain text ("Einstein born in Germany"), embed the query as `q`, and:

> **You are on a night flight over three cities — a schema city, a fact city, a passage city — and the query is a wand waved over all three at once.** Bulbs light up by relevance. Three cities; one wand; a differential lighting.

*(A worry worth pre-empting: the query "Where was Einstein born?" shares no words with `⟨person, born-in, country⟩`. **It does not need to.** Semantic embedders are trained to be insensitive to wording. You never convert the query into triplets; you let the embeddings meet halfway.)*

**Three initializations — one per layer, each one honest idea in one equation:**

```
Entities:  P_init(e) = (1/|F_e|) Σ_{f∈F_e} Sim(q, f)
```

The **mean, not the sum**, is deliberate: summing would hand runaway scores to entities mentioned in many facts — **to hubs** — while the mean rewards relevance, not frequency of mention. *Note the quiet philosophical footnote: **the retrieval side of this paper is already suspicious of mere frequency.** Hold that for the critiques.*

```
Types:     P_init(t) = (1/|S_t|) Σ_{s∈S_t} Sim(q, s) · 1/log(deg(t)+1)     ← hub suppression
```

Act I's generic-entity problem, met head-on. A type like `person` has enormous degree and would dominate everything, **so you mute it, gently.** The logarithm makes the muting mild: take the degree from 10 to 100 and (in base 10) the penalty moves merely from 1 to 2. **A leash, not a muzzle.** *The heavy tail of the degree distribution wrote this equation; Barabási is its uncredited co-author.*

```
Passages:  P_init(p) = α·Sim(q, d_p) + σ( log( Σ_{e∈E_p} IDF(e) / (|E_p|+1) ) ),   α = 0.05
```

Two twists. **First, the dampening α = 0.05** — direct query-to-passage similarity is discounted by ninety-five percent, deliberately undervalued relative to the fact and schema worlds. **Second, an information-density term** — an IDF-weighted entity density, squashed through a sigmoid, so ordinary passages sit low and rare-entity-dense passages saturate toward one. *(The word "the" is in every document — be unimpressed. A passage dense with entities nobody has heard of — high value, who is this?)*

**Why throttle passages at all?** Because the authors are betting — and their ablations support them — that **the rich information lives in the upper two layers.** Passages are grounding, not the main current.

> The degenerate cases teach the design: with only the passage term, the whole apparatus **collapses into vanilla RAG** — the dam is what keeps the graph a graph. Conversely, if a query resonates with no fact and no schema and exactly one passage glows, **α's size is irrelevant — that passage still wins, and the system degrades gracefully to plain retrieval.** The discount shapes competition; it does not disqualify.

### The honey and the springs: semantic energy and personalized PageRank

The morning's last IOU, paid in full. **We do not simply pick the brightest bulbs.** Some of my meaning is out in my neighbors; **the graph knows things the individual scores do not.**

```
W = D⁻¹ A                              ← "split, don't dump": share along your edges in weighted proportion

v^(k+1) = (1−λ) W v^(k) + λ v^(0),     λ = 1/2
```

**Read it as a story, precisely, because the naive telling misleads.** The query is where you pour the honey. The seed nodes are **springs, not a one-time pour.** Each round, every node lets **half** of what it holds flow outward to its neighbors, split in proportion to W — **proportional spreading, a rumor diffusing, never a walker hunting a best path.** The other half is not hoarding — **it is the springs re-bubbling**, `λv⁽⁰⁾` re-injecting the original query-seeded energy at the seeds, every step.

Traveling honey halves at every hop — `1/2, 1/4, 1/8` — so it glazes a one-or-two-hop neighborhood before the leash yanks it back. **That is what "λ prevents semantic drift" means, mechanically: make the honey thick; it flows only this far.**

**Nobody ever walks the graph. You let the honey settle, then skim the richest pools — and the skim is the retrieval.**

**Measured on the lesson plan's figure (λ = 1/2):** 52% of the energy stays on the seed, 29% reaches its neighbors, 16% the second hop — **97% within two hops.** This is why λ = 1/2 is enough: in a small world with communities, **everything relevant is near.**

**Convergence:** the update is a contraction, and Banach's fixed-point theorem does the bookkeeping — error after `k` rounds shrinks like `(1−λ)^k`. With λ = 1/2 and ten rounds, `(0.5)^10 = 1/1024` — a tenth of a percent. **You do not iterate many times. You just stop.**

> **Why 0.061 seconds:** ten-ish sparse matrix–vector products over the stacked three-layer graph — no community detection, no summaries, **no LLM calls at query time.** The paper's Table 2 reports **0.061s** per retrieval, against **1.6s for HippoRAG** and **11s for LightRAG**. Savor the double duty: **one λ sets both locality (how far the honey travels) and convergence speed (error halving per step). One knob, two jobs — and the $1,000 Karamazov invoice answered in sixty milliseconds.**

*(For the GNN-minded: the iteration is precisely **APPNP** — Predict, then Propagate — PPR as a propagation rule, minus learned weights. And the honest answer to "could λ and α be learned?" — they could; here they are chosen.)*

---

## Three Critiques, One Disease

> *"I promised debate, not demolition."* The paper is impressive — the ideas are clean, the diagnosis is real and well measured, and the machinery (conflict taxonomy, candidate-to-stable promotion, hub suppression, information density) is genuinely nice. **A fair reading credits before it cuts.**

### Critique A: "grounding" is a category error

Return to the held question: irreconcilable conflict — Joe born in Berkeley, Joe born in Fremont, no third passage to adjudicate. **The resolution agent must pick one; their design always resolves.** It is sold as principled: fetch the provenance passages, let the evidence decide.

**But a passage is not truth — a passage is more text, with unmodeled reliability.** "Grounded" means *traceable to some text*, never *traceable to true text*. And when the passages underdetermine the answer, **the LLM judge's parametric priors lean it to one side: the judge stops reading and starts remembering.**

> The AI has made an automated decision it has, frankly, **no right to make** — that calls for **human-in-the-loop review**, not silent adjudication.

Underneath sits a **correlated-errors problem**: all three agents run on the same underlying LLM, so the verifier shares the generator's blind spots — **the "society of agents" is one model wearing three prompts.** And the Wikipedia-derived benchmarks cannot catch it: on the hard cases, **the parametric fallback and the gold answer coincide by construction.**

### Critique B: contradictions should be first-class citizens

> *"Three years of building RAG systems taught me the opposite: discovered contradictions are gems."*

Two departments reporting different revenue for the same quarter is **not noise to be averaged away — it is a finding.** Run the root-cause analysis.

**And the paper's own taxonomy convicts it.** Of its three conflict types, **two are not even contradictions:**

- **Temporal** facts are both true, time-indexed — **resolving destroys the index**
- **Granularity** pairs form an abstraction hierarchy — **the honest move is a subsumption edge, which enriches the graph**
- Only **mutually-exclusive** is genuine contradiction

> **So the resolution agent discards true information in two of its own three cases. They built a seismograph and wired it to erase earthquakes from the record.**

**The fix costs almost nothing** — they already attach weights and already run detection: **let detection annotate** — a `conflicts-with` edge, both provenances, a confidence, a temporal validity — **instead of letting resolution delete.**

> **Don't resolve the contradiction; promote it.**

And notice: **this dissolves Critique A**, because if you never commit at construction time, you never invoke the fallible judge at all — adjudication defers to query time, which has the disambiguating context, or to a human.

### Critique C: frequency is not importance

The self-experiment proved this by construction, so two sentences suffice: **the rare cross-domain gem appears once, not because it is unimportant but because bridges are rare;** frequency counts repetition, and has never once measured importance.

**But name the irony inside the paper**, because you only see it reading the paper whole:

| Half of the system | Theory of value |
| --- | --- |
| **Construction** | **Frequency is signal** — recurring schemas promoted, rare ones executed |
| **Retrieval** | **Frequency is noise** — hub suppression penalizes the common, IDF rewards the rare, the mean-not-sum in `P_init(e)` refuses to reward repetition |

> **Two opposite theories of value in one system: their retrieval side would boost the very gem their construction side erased.**

**The fix, again nearly free:** the candidate tier already exists as a staging area — **demote, don't delete**; keep sub-threshold schemas retrievable at lower weight. **The drawer exists; they keep it locked.**

### The through-line

**Three critiques, one disease.** The paper indicts GraphRAG for throwing information away in isolated local extraction — **and then commits the same sin three times:** a single adjudicated truth (the conflict erased), a single surviving fact (the loser erased), a single frequent schema set (the rare erased).

Each is an **eager, information-destroying commitment made at construction time — the moment with the least context — when it could be deferred to query time, the moment with the most.**

> # Preserve, then decide.
>
> Keep the conflict. Keep the rare. Defer judgment to the moment with the most relevant context. **A paper about not losing information should not lose the most interesting information it finds — and the fix is not a better threshold; it is the humility not to throw anything away until you have to.**

*(The meta-lesson under the whole evening: everything above — the extraction, the frequency table, the staircase — came from **sitting with an LLM and a dozen passages for an afternoon.** Papers make persuasive arguments with benchmarks; a small, honest experiment can still find the structural seam. **Do not only read papers. Run them** — and there is no data more poetically apt than the paper itself.)*

---

## The Practitioner's Ledger

> *Papers from academia are great; the enterprise reads them through different lenses — economics, feasibility, scalability.*

### The pattern: global sensemaking

GraphRAG approaches earn their keep on **exactly one class of query**, and we can now characterize it precisely:

> **The query whose answer is a property of the corpus's structure, not of any passage in it.**

- *"What are the underlying leitmotifs of this novel?"*
- *"What are the major regulatory concerns across these five hundred earnings calls?"*
- *"How do this year's product revenues compare to last year's, and where are we weak?"*
- *"What are the dominant themes and tensions across everything our customers wrote to us this quarter?"*

**The signature is always the same: a human answering it would need to have read everything and formed a mental model — and the mental model is the entity graph with its communities.** When the answer is thematic, comparative, distributional, or trend-shaped, **the community summaries or the energy-settled subgraph are the only artifacts in your entire architecture that even contain the answer.**

**Concretely:** strategic and analytical dashboards fed by sensemaking queries; periodic corpus briefings ("what changed in the literature this month?"); investigation and root-cause work, **where the contradictions and bridges — the weak ties — are precisely the gems**; and, always, the **hybrid** answer where one component comes from the graph, another from Text2SQL against the warehouse, another from plain retrieval.

### The anti-patterns — name them without mercy

> **The field's disappointments are mostly mis-routed queries.**

| Anti-pattern | Why it fails |
| --- | --- |
| **The point query** — *"What learning rate did experiment 3 use?"* · *"What is the termination clause notice period?"* | A single passage answers each; plain retrieval finds it in milliseconds for a fraction of a cent. Routing a point query through community summaries is **using a telescope to read your own wristwatch** — slower, costlier, and **often worse**, because the synthesis machinery can blur the crisp local fact it was never designed to serve |
| **The small corpus** | **Emergence needs mass.** Run Leiden on a three-page essay — fifteen entities, twenty edges — and you get three tiny "communities" whose summaries paraphrase the essay, at LLM prices. **You cannot detect ocean currents in a bathtub.** Below hundreds of documents, the Weeks 1–4 cascade is **not merely sufficient; it is strictly better** |
| **The real-time chat lane** | Full GraphRAG's map–reduce is **seconds per query**; graph freshness is a batch concern; **the pipeline is a batch animal.** Bolting it into search-as-you-type is an SLA violation waiting to be discovered. *(MemGraphRAG's sixty milliseconds is a genuine selling point here — but the construction cost and freshness burden remain)* |
| **The everything-graph** | *The gravestone.* Shunting your whole corpus through graph construction **because the demo was impressive** |

### The sidecar: high-value documents, high-value queries

> **GraphRAG, in any variant, is always a sidecar — it extends the motorcycle; it never replaces it. The economics allow nothing else.**

It is expensive to **build** (an LLM call per chunk, then the summary pyramid, then forever after **the freshness tax** — the world changes and the graph quietly rots), and expensive to **serve** unless you are Lazy (pay at query time) or Mem (paid at construction). So you route:

**High-value documents into the graph.** Not petabytes — and note, in practice you will not have petabytes of running prose; documents, images, and scans are what come in petabytes. **Select the sub-corpus whose global structure the organization actually needs to understand:** the contracts, the filings, the research collection, the customer-voice corpus. **The rest of the swamp stays in the plain index, perfectly retrievable, unmapped.**

**High-value queries through the graph.** A **router** — and after five weeks we can build one — classifies each query **local vs. global**, with the Mill-on-the-Floss litmus pair as its creed. The local majority flows through the standard cascade; **the global minority, perhaps five to fifteen percent, is escorted to the sidecar.** Those few are disproportionately **the queries executives ask — the ones that define your system's intelligence ceiling.**

> **The capex–opex frame:** full GraphRAG is **capital expenditure** (pay at indexing, cheap queries); LazyGraphRAG is **operational expenditure** (cheap indexing, pay per query). Database engineers have run this exact trade for decades under the name **materialized views**, and the answer has always been the same: **it depends on how often the view is read. Precomputation is a bet on query volume. Know your volume before you place the bet.**

**And keep the ledger honest about quality, not just money.** GraphRAG **amplifies extraction quality**: a noisy graph yields meaningless communities yields useless summaries — **garbage in, confidently narrated garbage out.** **Entity resolution is load-bearing.** And contradictions are worth preserving as annotated, first-class edges, because **in an enterprise the contradiction is often the single most valuable thing the graph will ever surface.**

---

## The Five Labs

| Lab | What gets built | The metric that matters |
| --- | --- | --- |
| **1. The corpus becomes a graph** | LLM extraction (entities + relationships) over **50–100 chunks**; consolidate into NetworkX. Then, **before any algorithm: look** | Plot the degree distribution on **log–log** and find the heavy tail **with your own eyes**; confirm the hubs are the generic entities; find **at least three entity-resolution failures** ("FDA" vs. "the FDA") and measure how merging them changes the hub list. **The morning's mathematics should stop being slides during this lab** |
| **2. Communities and the fractal-but-real hierarchy** | Run **Leiden** (`leidenalg`) at two or three resolution levels; inspect communities by eye for semantic coherence | Measure modularity at each level **against a degree-preserving random rewiring of the same graph** — structure is a **surplus over chance**, so compute the chance. Then test the finite-zoom claim: **at what level does subdivision stop being meaningful on your corpus? Two? Four?** |
| **3. Community summaries and one global question** | A small Microsoft-GraphRAG pipeline over the Lab 2 hierarchy: a summarization prompt per leaf community, merged upward once | **Keep the cost ledger open and visible — count every LLM call**; you are re-deriving the Karamazov invoice at classroom scale, on purpose. Then ask one genuinely global question, map–reduce over your summaries, and put the same question to plain top-k. **The gap is the sensemaking gap, and you will have paid for it** |
| **4. Honey by hand — a miniature MemGraphRAG** | Three-layer memory graph over a dozen passages; implement `P_init(e)`, `P_init(t)`, `P_init(p)`; iterate ten times | Print `‖v^(k+1) − v^(k)‖` per step and **see Banach's `(0.5)^k` with your own eyes.** Then: vary **τ** over the schema frequency table and **reproduce the staircase** *(spoiler: on a technical corpus, you cannot find a threshold that admits the gems without the copyright notices)*; vary **λ** to feel locality change — at λ = 0.1 the honey wanders, at λ = 0.9 it never leaves home |
| **5. The router tournament** | A query set spanning three bands — **point / mid-scope thematic / truly global** — run through (a) the Weeks 1–4 cascade alone, (b) Lab 3's community-summary pipeline, (c) Lab 4's miniature MemGraphRAG, (d) a **routed hybrid** with a simple LLM classifier | Score **answer-ability per band**. Your own judgment is the metric, **subjective on purpose**; sharper instruments arrive later. **The deliverable is the honest table: which machinery pays rent on which band — and the anti-pattern row, point-queries-through-the-graph, measured rather than merely believed** |

---

## What we actually have — and the honest gap

### The Week 05 artifacts in the repo

| Path | What it is |
| --- | --- |
| `course/week_05/carry_forward_knowledge_graph.{md,json}` | The "What Must You Carry Forward" section converted into a knowledge graph — 13 schema triples, **46 main nodes** across graph mathematics / knowledge representation / GraphRAG systems / architecture judgment, and 59 fact triples (79 nodes, 62 edges in the JSON). **Week 05's own method applied to Week 05's own content** |
| `course/week_05/fractal_structure_knowledge_graph.{md,json}` | The finite-fractal-hierarchy argument as a graph |
| `course/week_05/week-5-summer-lesson-plan.pdf` | The 45-page lesson plan (this document's source) |

**These are learning artifacts, not running systems** — and they are, pleasingly, an instance of the week's own three-layer idea: schema triples above, fact triples below, both pointing home to the lesson plan.

### The lab repos — obtained, scaffolded, not run by us

`labs/week5.2/` contains three course-provided projects:

| Repo | Covers | State |
| --- | --- | --- |
| **`memgraphrag_concepts/`** | Seven notebooks: overview → ingestion → knowledge extraction → three-layer memory → memory graph → **adjacency matrix + PPR** → memory-guided QA. Full `src/` package (`extraction`, `graph_builder`, `adjacency`, `pagerank`, `retrieval`, `qa`). Corpus: *Attention Is All You Need* | **Notebooks carry executed outputs — from the instructor's machine, not ours.** Our `outputs/` directory is empty |
| **`ms_graphrag/`** | Microsoft's official `graphrag` package against local LLMs (vLLM/Ollama + `nomic-embed-text`), with `pdf_to_txt.py` and `visualize_graphrag.py` | **Setup instructions only.** No `sv_docs/` index built |
| **`light_graphrag/`** | LightRAG (HKUDS) server + web UI | **Setup instructions only.** No `rag_storage/` |

### The number worth stealing from the instructor's notebooks

The `memgraphrag_concepts` notebooks **accidentally reproduce the staircase from the lesson plan**, and this is the most useful measurement we have from the week:

| Notebook | τ behavior | Memory | Graph |
| --- | --- | --- | --- |
| **05 — memory graph** | **τ = 2** (the package default in `pipeline.py`): 4 stable schemas of 80 | 10 passages, 80 schemas → **4 stable**, 112 facts → **12 active** | **31 nodes, 68 edges — and 6 connected components** |
| **06 — adjacency + PPR** | **τ = 1** (all admitted): 83 stable of 83 | 10 passages, 83 schemas → **83 stable**, 115 facts → **115 active** | **213 nodes, 750 edges** |

Read those two rows next to each other. **Ten passages of the *Attention* paper produce either a 213-node, 750-edge graph or a 31-node graph shattered into six components, depending largely on where τ sits.** *(The two notebooks are separate extraction runs — 80 vs. 83 schemas — so τ is the dominant variable, not the only one.)* That is the lesson plan's staircase — *"a shattered graph that is itself a textbook case of structural fragmentation, the very disease the paper set out to cure"* — reproduced as a number, on a real corpus, **at the package's own default threshold, without anyone intending to.**

**It is also the honest answer to "does the critique matter in practice?" It does: 89% of the facts (112 → 12) were dropped by one threshold.**

### Not done

| Lesson-plan item | Status |
| --- | --- |
| **Lab 1** — extraction over 50–100 chunks, log–log degree plot, entity-resolution failures | **Not run.** We have never plotted a degree distribution on our own corpus |
| **Lab 2** — Leiden at multiple resolutions, modularity vs. degree-preserving rewiring | **Not run.** No community detection anywhere in our repo |
| **Lab 3** — community summaries + one global question vs. plain top-k, with a cost ledger | **Not run.** The `ms_graphrag` scaffolding exists; no index was built |
| **Lab 4** — miniature MemGraphRAG, Banach convergence printed, τ and λ sweeps | **Not run by us** (the instructor's notebooks demonstrate the mechanism) |
| **Lab 5** — the router tournament | **Not run** — and this is the one that matters most for us, see below |

**`PROJECT_PLAN.md` says "Do not start with GraphRAG" and lists GraphRAG among "available interventions, not default milestones."** So the deferral is a **decision, not an omission**. This document records *why*: our corpus is a **bathtub** (187 records from one Wikipedia article), our failing eval is a **point query** ("What is a Xennial?"), and our open bug (EV-001) is a **retriever-signal problem**, not a structure problem. **Week 05's own ledger tells us not to build this yet.**

---

## What Week 05 actually changes for us

### 1. The router is the deliverable, not the graph

Lab 5 is the only Week 05 lab whose output we need **before** we need a graph. A local-vs-global classifier is useful even with **zero** graph-shaped indices, because it is the same routing decision that sits over our Week 04 representations (raw / factoid / QA pair / summary). **Build the router; let it tell us whether we have any global queries at all.**

### 2. "Preserve, then decide" is an architecture principle we can apply today

It generalizes past GraphRAG:

- **Week 04's derivative artifacts:** we already keep the raw index alongside the derived ones. Same principle, already obeyed.
- **Our eval harness:** EV-006 answered a question it should have refused, at confidence 1.0 (`tasks/T026`). **That is an eager commitment at the wrong moment.** Abstention *is* deferral.
- **Any dedup we do on the 88 Xennials factoids:** the Critique C fix — **demote, don't delete.** Keep near-duplicates at lower weight rather than dropping them.

### 3. Hubs explain EV-001 better than the tokenizer did

EV-001's diagnosis was: after stopword removal the query is the single term `xennial`; **43 records contain it at similar term frequency**, so BM25 has no discriminating signal and ranking collapses onto length normalization.

Week 05 gives that a name. **`xennial` is a hub in our corpus** — the generic entity every second record mentions. Week 04 said "fine-grained indexing amplifies the many-near-identical-records failure mode." Week 05 says the same thing in network language, **and supplies the mitigation the field already uses: hub suppression (`1/log(deg+1)`) and IDF-weighted information density.** Both are cheap, both are implementable against our existing index, and **neither requires a graph.**

### 4. Entity resolution is load-bearing before it is interesting

"FDA" vs. "the FDA" is Lab 1's exercise, but it is also **the reason a graph fragments and every downstream step inherits the fracture.** If we ever do build a graph over a real corpus, **entity resolution is the first cost, not a later polish.**

---

## Engineering constraints this week produces

1. **The invoice is a first-class design input.** An LLM call per chunk at extraction, plus the summary pyramid, plus the freshness tax. **$1,000 for one book is the datum to quote when anyone proposes graphing the swamp.**
2. **Construction-time thresholds are unrecoverable.** Be as clever as you like at retrieval; **you cannot retrieve what was never admitted to the graph.** Any filter applied at build time needs a demotion tier, not a delete.
3. **Frequency is not a proxy for importance on a Zipfian corpus** — and enterprise technical corpora are Zipfian. The cross-domain bridge appears once **because bridges are rare.**
4. **Contradictions are findings, not noise.** Model them as annotated `conflicts-with` edges with both provenances, a confidence, and a temporal validity. **In an enterprise the contradiction is often the single most valuable thing the graph will surface.**
5. **A "society of agents" on one underlying LLM is one model wearing three prompts.** Correlated errors mean the verifier shares the generator's blind spots. **Any multi-agent verification design we build needs genuinely different judges, or a human.**
6. **Emergence needs mass.** Below hundreds of documents, the Weeks 1–4 cascade is **strictly better**, not merely sufficient. Our current corpus is well below that line.
7. **GraphRAG is a sidecar, always.** High-value documents in; high-value queries through; everything else stays in the plain index.

---

## Open questions for the team

1. **Do we have any global queries?** Before any graph work: audit our eval set and any real user questions against the Mill-on-the-Floss litmus. If the answer is "essentially none," Week 05 is a **deferred capability with a written reason**, and that is a complete outcome.
2. **Is hub suppression worth porting to our lexical retriever now?** `1/log(deg+1)` has an obvious lexical analogue and EV-001 is exactly the failure it targets. Cheaper than the dense-retriever experiment in `T025` — should it run first, or alongside?
3. **What is our demote-don't-delete policy?** If we dedup the 88 Xennials factoids, do sub-threshold records stay retrievable at lower weight?
4. **Where does the router live?** A standalone classifier in front of the existing cascade, or a capability of the agent? Lab 5's tournament table is the same artifact as Week 04's unrun Lab 4 ablation — **can one experiment produce both?**
5. **If we ever build a graph, on what sub-corpus?** The week's answer is "the one whose global structure the organization needs to understand." **For us, is there one — or is our corpus still the demo corpus?**
6. **Does `MemGraphRAG`'s α = 0.05 passage dampening survive contact with our data?** Ninety-five percent discount on direct passage similarity is a strong prior about where information lives. Our 187 records are **only 11 raw chunks and 176 derived artifacts** from a single Wikipedia article — the "passage layer" is already mostly derivative, so the prior may not transfer.
7. **Entity resolution: buy, build, or defer?** It is load-bearing for anything graph-shaped and useful even without a graph.

---

## Readings

**Essential:**

- **Edge et al.** — *From Local to Global: A GraphRAG Approach to Query-Focused Summarization.* The foundational paper and the modern meaning of the name. **Pay particular attention to the experimental comparison with naive RAG on sensemaking tasks: it is the pattern/anti-pattern split, measured.**
- **Wu et al.** — *MemGraphRAG: Multi-Agent Knowledge Graph Construction with Shared Memory.* Read it **with the three critiques in hand**, especially the frequency-threshold construction and the conflict-resolution agent. **Then do what we did: run a dozen of its passages through its own pipeline and see what survives.**
- **Traag, Waltman & van Eck** — *From Louvain to Leiden: Guaranteeing Well-Connected Communities.* The detector inside Microsoft GraphRAG. **The guarantee is not a technicality; it is why the communities are meaningful enough to summarize.**
- **Barabási & Albert** — *Emergence of Scaling in Random Networks.* Four pages that changed how we see networks. **Your entity graph will exhibit this structure, and both its navigability and its noise problems follow from this paper.**
- **Barabási** — *Network Science* (free at networksciencebook.com). For this week: **Ch. 2** (graph theory), **Ch. 4** (scale-free), **Ch. 9** (communities).
- **Gutiérrez et al.** — *HippoRAG.* The bridge between the two deep stops. **Reading it makes MemGraphRAG's retrieval feel inevitable — which is exactly how good lineages read in retrospect.**

**Optional:** Newman, *Modularity and Community Structure* (where Q comes from) · Watts & Strogatz, *Collective Dynamics of 'Small-World' Networks* · Granovetter, *The Strength of Weak Ties* (the classic behind Critique C) · Edge et al., *LazyGraphRAG* + MSR *BenchmarkQED* (read the pair together) · Broido & Clauset, *Scale-Free Networks Are Rare* (the loyal opposition) · Anderson, *More Is Different* (re-read from Week 04) · Gasteiger et al., *Predict, then Propagate* (APPNP — MemGraphRAG's iteration, minus learned weights).

---

## Where this sits in the arc

```
Week 01 — the RAG pipeline end to end
Week 02 — why vector space works at all
Week 03 — how the source document gets cut, or preserved
Week 04 — whether we index the source at all, or artifacts manufactured from it
Week 05 — the corpus as a network: what emerges above the artifacts, and what it costs
Week 06 — the router instinct sharpened: which index does a question deserve?
```

Week 04 asked *what should we index?* and answered *artifacts written for the query.* **Week 05 asks a question no artifact can answer: what is true of the corpus that is true of no passage in it?** The answer is structure — communities, hubs, bridges — and structure must be **mined, summarized or diffused over, and paid for.**

> **Large graphs develop emergent structure — communities within communities, hubs, small worlds — that no edge contains. A knowledge graph inherits that structure from knowledge itself. Every GraphRAG is a bet that harvesting the structure is worth the invoice; the good architect routes the sensemaking few to the graph, keeps the point-query many on the plain index — and preserves, before deciding.**

---

## Follow-ups

- **Lab 5 / the router (highest value).** A local-vs-global classifier over our existing indices. Useful with zero graph work; produces the same honest table as Week 04's unrun Lab 4 ablation.
- **Hub suppression on the lexical retriever.** `1/log(deg+1)` + IDF density against the 187-record index. Directly targets EV-001. Cheap.
- `tasks/T025` — the dense-retriever arm on EV-001. Still the cheapest decisive experiment.
- `tasks/T026` — the answerability / abstention gate. Week 05 reframes this as **"preserve, then decide" applied to our own generator.**
- `tasks/T027` — this document is the **team summary**; the course notes `course/week_04/week-04.zh.md` and `course/week_05/week-05.zh.md` are still owed, and `course/00-course-overview.md` should link both.
- **A written decision record for deferring GraphRAG.** The reasoning in "What Week 05 actually changes for us" belongs in `decisions/` per `templates/decision.md`, so the deferral stays a decision.

---

## Sources

- `course/week_05/week-5-summer-lesson-plan.pdf` — Asif Qamar, SupportVectors, "When the Library Becomes a City," first draft July 4 2026
- `course/week_05/carry_forward_knowledge_graph.md`, `course/week_05/fractal_structure_knowledge_graph.md`
- `labs/week5.2/memgraphrag_concepts/` (notebooks 01–07), `labs/week5.2/ms_graphrag/`, `labs/week5.2/light_graphrag/`
- `evals/results/latest.md`, `evals/cases/EV-001.json`, `PROJECT_PLAN.md`, `tasks/T025`, `tasks/T026`, `tasks/T027`
