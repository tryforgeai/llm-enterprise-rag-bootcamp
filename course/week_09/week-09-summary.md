# Week 09 Summary — When Knowledge Gets Its Papers: The Open Knowledge Format and the Governed Corpus

**Date:** 2026-08-08 · **Source:** `course/week_09/summer-week-9-lesson-plan.pdf` (*When Knowledge Gets Its Papers — The Open Knowledge Format and the Governed Corpus*, Asif Qamar, SupportVectors), the *The Library in Your Head* prelude deck (31 pp), and live notes from the afternoon's Module 5 on *Secure Retrieval / Enterprise Entitlement-RAG*

---

## TL;DR

The whole week compresses into one sentence:

> **The corpus was never a given — it has always been a choice. Move the intelligence of a knowledge system from query time to authoring time.**

Week 07 measured retrieval; Week 08 measured the generator. **This week steps back and asks what the thing being retrieved is actually made of.**

The sharpest compression of the day:

> *"Our trained instinct: chunk, embed, retrieve top-k — **the corpus as a given**. The quiet radicalism today: **refuse the given**. Manufacture the corpus into a shape worth retrieving from."*

There is no new mathematics this week. The close reading is of a young specification Google published on 12 June 2026: the **Open Knowledge Format (OKF)**.

The day's shape:

```
PROLOGUE   The Press Release     ("Is RAG dead?" — a question wrong in an instructive way)
ACT I      The Substrate         (bundle / concept / frontmatter, and the inversion)
ACT II     Trust                 (provenance, three tiers, attested computation)
ACT III    The Channel           (documents → a retrieval channel)
INTERLUDE  The Phantom           (the hallucinated concept — worse than a bad chunk)
ACT IV·CODA  The Other Bank      (experience → memory; the case against; the chiasmus)
```

The afternoon opens a separate module: **Module 5 · Secure Retrieval** (enterprise entitlement RAG), shifting from "how knowledge is modelled and trusted" to "how retrieval itself is constrained by security."

---

## Opening: The Library in Your Head

Continuing Week 08's trick of seven experiments you fail with your own hands, this time it is **eight walks through your own memory** — each confirms an instinct you already have, then tells you what field name it will get this afternoon.

> *"Close your eyes. You already know today's material — we only have to find where you keep it."*

| # | The thought experiment | The term being seeded |
|---|---|---|
| **I** | Before opening a heavy reference book, you already judged it by title, description and provenance | **a progressive-disclosure engine with a trust policy** → `index.md`, `verified` |
| **II** | A nine-hundred-page definitive treatise whose spine reads *Miscellany, Vol. XI* and whose back cover is blank — you would not even **slow down** | metadata failure → an honest `type`/`title`/`description` is a precondition for being found |
| **III** | If the library were decomposed into index cards — one fact per card, filed in a hierarchy, cross-referenced — how would you design it? | three questions → what goes on one card, how cards point to each other, who keeps them current |
| **III+** | **The reveal: it was built, in Brussels, in 1895.** Otlet and La Fontaine's **Mundaneum** — twelve million index cards under the Universal Decimal Classification, cross-referenced; mail or telegraph a question, clerks walked the drawers and posted back copied cards | **a search engine made of paper — running fifty years before the transistor** |
| **IV** | When you made study cards, the magic was never in **having** them — it was in **writing** them | **understanding happened at authoring time; the exam merely retrieved it** |
| **V** | Two ways to learn arrive on your desk: a shuffled stack of loose pages (each beginning and ending mid-thought) vs fewer, oversized self-contained cards — **the stack feels wrong before you have read a word** | the stack = **chunk**; the card = **concept** |
| **VI** | The department binder reads "**Currently**, RAG classes meet in the morning" — you hesitate. Where exactly does the hesitation live? | three missing clocks → `stale_after`, `generated`, `verified` |
| **VII** | An elegant, beautifully typeset, plausible-looking formula claims to compute the first 1,000 primes. **What would settle it?** | you would **run it** → attested computation |
| **VIII** | "Plant a pole at location X; at equinox noon it casts no shadow" — you cannot fly there or wait until March. Design the cheapest decisive test | strip the theatre and one decidable line remains |

### Three worth keeping separately

**Walk V's economics** — the one point in the whole prelude where the argument becomes an actual ledger:

> *"The fragment outsources the assembly to **you, at reading time**. The card was **made whole at writing time** — someone paid the assembly cost once, so every reader afterward pays nothing. The stack is cheap to produce and expensive to read — **a hundred times, by a hundred readers**. The card is expensive **once**."*

This is the first time "creation-time vs query-time intelligence" is argued as pure economics: not which is more elegant, but **who pays for understanding, and how many times.**

> **The unit of reading decides where understanding happens — at writing time, or at every reading, forever.**

And the closing line:

> *"When you bite into a fragment, you risk finding **half a thought** — and half a thought can be worse than none."*
> Nothing makes you keep looking; half makes you think you already have the whole answer. (A precise prophecy of the phantom concept.)

**Walk VI's three missing clocks:**

> Your hesitation lives in **three absences**: currently — **as of when?** · **Says who?** · **Has anyone confirmed it lately?**
> An undated "currently" is a **timestamp-shaped hole**. The ink does not fade when the schedule changes — **text does not visibly age.**
> *"The page might be perfectly right. Your unease is that **nothing on the page lets you tell**."*

That is the reason OKF exists: **not to make every sentence right, but to make every piece of knowledge carry enough fields that the question "how would I know?" can always be asked and answered.**

**Walk VII's asymmetry** — the single line most worth memorising this week:

> *"Notice the **asymmetry** you just enacted: **sentences** you weigh; **computations** you re-run."*
> Sentences you **weigh** — against provenance, author, verification records: probabilistic, social trust. Computations you **re-run** — no social judgement, just mechanical verification: black and white.
>
> **Claims earn trust from provenance. Numbers earn trust from re-execution. Two different kinds of trust, and they must never be conflated.**

---

## Prologue: What Actually Shipped

On 12 June 2026 two Google engineers published a blog post announcing OKF, and within a week every inbox was asking the same breathless question — **"Is RAG dead?"**

> *"The question is wrong — but wrong in an **instructive** way."*

**The demystifying statement — one of the most important lines of the day:**

> *"Not a vector-database killer. Read strictly, **not even software**. Knowledge laid down as **markdown files with YAML frontmatter**, versioned in git — readable by a human with `cat`, and by an agent with nothing at all."*
> *"So slight an artifact, so loud a conversation: it touched an **exposed nerve**."*

That exposed nerve is **the fragmented-context problem**. Before an enterprise agent can answer honestly it must know which table is the authoritative source of revenue, what finance precisely means by "recognized," which runbook the freshness alert points to, and which API was deprecated last quarter.

> *"None of it lives in one place — it is smeared across catalogs, **three generations of wikis**, docstrings, chat threads, and the heads of senior engineers."*

---

## Act I: The Substrate

### The load-bearing thesis

> Skills, memories, and retrieved knowledge are all, at bottom, the same thing — **curated text placed into context at the right moment** — resting on one substrate: **small, typed, cross-linked documents, owned and governed like source code.**

**The corollary that organises the day:**

> Point the format at an organization's **documents** → a **retrieval channel**: governed, curated, answerable.
> Point it at an agent's **experience** → a **memory store**: portable, reviewable, shared.
> **One format, two directions of flow.** — the coda closes the loop.

### Lineage and ratification

| Year | Ancestor | The problem it solved |
|---|---|---|
| 2024 | `llms.txt` | **who content is written for** (first mainstream admission that content should be authored for machine readers) |
| 2025 | `AGENTS.md` | **whether knowledge ships with the artifact** |
| 2025–26 | `SKILL.md` | **how procedure gets packaged** (frontmatter + markdown, loaded on demand) |
| 2025–26 | memory-as-files | **where an agent's own past lives** |
| 2026 | **OKF v0.1/v0.2** | the pattern, **ratified** |

> *"Every element already existed in folk practice. What did not: a public, vendor-neutral document precise enough that producer and consumer **interoperate without a meeting**."*
> *"The cleverness of OKF lies in **how little it dared to standardize**."*

Note the wording is **vendor-blessed**, not invented. **Its cleverness is not how much it standardized, but how little it dared to.**

### The deepest idea of the day: the inversion

> *"Classical RAG bets meaning can be **re-derived at query time**: chunk, embed, gamble that cosine similarity reassembles the author's understanding on the fly. OKF moves the intelligence to **authoring time**: the unit of retrieval becomes a **curated knowledge object**."*
> *"Understanding happens **once, at curation, under review** — not on every query, in the dark, **without appeal**."*

**"Without appeal"** is the easily-skipped but heaviest dimension here: query-time re-derivation is not just a fresh gamble every time, it is a gamble with **no appeal process** — nobody is present to check whether this particular similarity computation was reasonable. What authoring-time understanding adds is a layer of the **social**: review is a process with someone present, with a record, open to challenge and rejection.

### Why now, and not in 1996

> *"Wikis rot: curation is expensive and humans will not sustain it. What changed in 2025–26: **a worker who does not get bored** — the agent that drafts, cross-references, and opens the PR."*
> *"Elegant symmetry: **embeddings made raw retrieval cheap; agents made curated knowledge affordable.** The wager is open — hold it open all day."*

Authoring-time curation is not a new idea (the Mundaneum was this idea 130 years ago, and the wiki era shouted the same slogan). What changed is not the format but **who does the tedious, repetitive, never-ending curation work.**

> **Quiz 1:** "Our company launched wikis in 2009, 2015 and 2021. All three rotted within two years. Isn't OKF just wiki number four?"
> **Answer:** the one economic variable that changed is **the marginal cost of curation labour** — from "human attention" to "compute." But the critical answer must add: **production got cheaper; review is still a human bottleneck.** "The agent doesn't get bored" by itself only swaps the failure mode from "nobody writes" to "nobody reviews."

### Anatomy: bundle / concept / frontmatter / body

- A **knowledge bundle** is a directory tree of markdown files and nothing else. Git is the recommended skin (history, attribution, diffs).
- Two filenames are reserved at each level: `index.md` (a catalog listing, for progressive disclosure) and `log.md` (a chronological change history).
- Every other `.md` file is a **concept**: one knowledge unit, one file.

**Path as identity:**

> *"A concept's ID **is its file path**, minus `.md`. No UUID. No registry. No content hash. **The filesystem is the namespace.**"*
> *"The Unix instinct applied to knowledge: universal tooling (`grep`, `diff`, `mv`) — at the price of **rename fragility**."*

**Two things stapled together:**

```yaml
---
type: BigQuery Table   # the ONE required field in the whole spec
title: Customer Orders
description: One row per completed order.
resource: https://console.cloud.google...
tags: [sales, orders, revenue]
generated: { by: reference_agent/gemini, at: 2026-05-28T14:30:00Z }
---
# Schema
| Column   | Type   | Description      |
|----------|--------|------------------|
| order_id | STRING | Unique order id. |
```

> **Frontmatter** = the machine's half (the few fields you query and filter). **Body** = the reader's half (what humans and models actually read).

The only required field is **`type`** — a short, producer-invented string (`Metric`, `Playbook`, `BigQuery Table`) that consumers route on, and **must tolerate when the value is unknown**.

### Links: the graph hiding in the tree

> *"Concepts link with **ordinary markdown links**; the **kind** of relationship lives in the **prose around the link**. Edges are **untyped** — and the semantic-web tradition winces. The spec's answer: the reader is now a language model, and **language models read sentences**."*
> *"The most revealing choice in the spec: **prose now carries the semantics that formality used to carry**."*

**A red link is not an error but an invitation:**

> *"A link whose target does not exist is **not malformed** — it may simply represent not-yet-written knowledge. **The corpus is allowed to want things.**"*
> A red link is **the visible edge of the map**, where the next contributor digs.

### Economics in the layout

`index.md` looks like a small thing but is load-bearing — a catalog that is cheaper to read than the volumes. An agent reads the root index for a few hundred tokens, descends, and **opens only the two or three concepts the question needs.**

> *"**Value-of-information**, built into the directory layout — the same economics that govern skill loading and memory recall."*
> `log.md` is the same idea **pointed at time**: `index.md` is progressive disclosure along space, `log.md` along time.

The conformance bar is almost on the floor: a bundle conforms if **every concept has a parseable, non-empty `type`.** Strictness lives in exactly one place — **what consumers must tolerate.**

> **This is a spec that makes production easy and rejection hard: adopt first, accumulate rigour incrementally — the path JSON, markdown and HTTP all walked. Over-specified standards are the ones that die unadopted.**

---

## Act II: Trust — Provenance, Verification, Attestation

> **v0.1 describes a filesystem. v0.2 describes a society.**

Within weeks of the announcement the spec grew a second set of organs. The speed of the revision says what the authors learned first from real use: **once a corpus is written by agents, the question shifts from "what does this document say" to "why should I believe it."**

### Provenance without scores

```yaml
sources:
  - id: rev-policy
    resource: https://wiki.acme/finance/rr
    title: Revenue recognition policy
    author: team:finance-fpa
    last_modified: 2026-04-02
  - id: exec-rev-dash
    resource: dashboards/exec-revenue
    title: Executive revenue dashboard
    usage_count: 5000
usage_window: { from: 2026-06-01, to: 2026-06-30 }
```

Each source = **a resource, a stable id, and three optional credibility signals** (`author`, `usage_count` within a window, `last_modified`). Note that **none of the three is a score** — all are raw facts that can be independently verified.

**The design refusal:**

> *"No `credibility: 0.87`. A stored score is **subjective, unportable, stale on arrival**. Trust is **inferred at read time**, by each consumer, against its own policy."*
> *"The **personal equation**, applied to metadata: publish the raw readings, never the verdict — **the verdict embeds a judge, and judges do not travel**."*

(This is Week 08's personal equation returning: raw readings can be shared between observers; a corrected verdict has already baked in one observer's personal equation, and the error will not line up for anyone else.)

**Per-claim attribution uses an elegant device: markdown footnotes whose label is the source id.** A sentence carries `[^rev-policy]`, the frontmatter carries the matching source — **keyed, not positional**, because agents rewrite these documents constantly and a positional index silently misattributes the moment a list is reordered.

### Writer, confirmer, and three trust tiers

The trust family separates two questions our field habitually conflates: **who wrote this, and who verified it.**

- `generated` records the author.
- `verified` records zero or more confirmation events, each with an actor and a timestamp. Actors follow a three-part convention: `producer/version` for agents, `human:id` for people, `process:id` for automation.

**All three tiers are derived from the `verified` list:**

| Tier | Condition |
|---|---|
| **unverified** | no `verified` key at all — visibly a draft or a machine guess, never mistaken for anything else |
| **machine-confirmed** | only non-human verifiers (a nightly process re-checked it; nobody signed off) |
| **human-reviewed** | at least one `human:` actor present — **the heaviest token in the whole convention** |

**Three properties of a small machine:**

1. **Derived, not declared** — no tier field to forge or rot.
2. **Independently dated** — "regenerated **after** verification" is **mechanically visible** (`changed since review`: just compare two timestamps).
3. **Absence means, never excludes** — the corpus may hold drafts and hunches, clearly labelled.

> *"In the classical corpus, the hallucinated wiki page and the audited finance policy arrive **wearing the same clothes**."*

> **Quiz 3:** A concept is generated Aug 5 by `pipeline_agent/v3`, verified Aug 7 by `process:eval-nightly` — no one else. On Aug 8 the agent regenerates the body; no one re-verifies. Derive the tier on Aug 7, then after Aug 8.
> **Answer:** Aug 7 = **machine-confirmed** (only a `process:` actor). After Aug 8 = **demoted back to unverified** — the content's modification time is later than the only verification, so that verification no longer covers the current content. **What the paired dates expose is not whether the content is wrong, but whether verification kept up with it.**

### Lifecycle

> *"Knowledge ages like **milk**, not wine."*
> `status:` `draft` → `stable` → `deprecated` (deprecated concepts are kept for links and history)
> `stale_after:` an **absolute date**, **stamped at write time, when the shelf life is best known** — the author sets the expiry at the moment they understand the timeliness best.
> *"Retire a concept the way a library moves a book to the **annex** — not the way a database **drops a row**."*

### Attested computation: the spec's most original idea

**The most dangerous thing in an enterprise corpus is not an assertion but a number** — and an agent's temptation with a number is not to copy it wrong, but to **creatively recompute it**: a plausible-looking SQL query, wrong in exactly the way finance's recognition policy forbids.

```yaml
type: Attested Computation
runtime: bigquery           # fixes the execution environment
parameters:                 # declares semantics, not values
  - { name: fiscal_year, type: integer, required: true }
computation: computations/revenue.sql   # stored separately; the model can neither see nor edit it
executor:
  resource: references/skills/run-bq.md
  receipt: [job_id, executed_sql, result]
attester:
  resource: references/attesters/rev.py
  # deterministic code — no LLM, by rule
```

**The attestation principle — the sharpest line in the spec:**

> *"The model may supply **values for declared parameters**. It may **never** author or edit the computation."*
> *"The attester re-derives the expected binding and compares it to the receipt of what **actually ran** — a rewritten query **mechanically fails**."*
> *"'Did the sanctioned thing run' becomes a **string comparison** — the one link in the chain from which the LLM is **banished by design**."*

**The lineage: this is remote attestation, transplanted from trusted computing** — measure what ran, compare against what was blessed, gate on the comparison — moved from binaries onto SQL, **with the LLM as the untrusted host.**

> *"The model, creative and unreliable, fills **typed holes**; deterministic code **checks the paperwork**."*

**Keep the two axes apart (definition-trust vs run-trust):**

| | `verified` | attestation |
|---|---|---|
| Confirms | the **definition** matches policy | a single **run** produced this value the sanctioned way |
| Granularity | doc-level | per-call |
| Pace | slow (human verification) | at runtime |
| Storage | recorded in the bundle | **never stored** |

> *"A **stale definition can attest cleanly**; a **fresh definition still needs attestation on every run**. Conflating the axes **is how dashboards lie**."*

### Cashing the argument: four questions a chunk cannot answer

| Question | The chunk's answer | The concept's answer |
|---|---|---|
| **Who says so?** | uncredited | `generated.by`, `verified[].by`, footnote joins |
| **Is it still true?** | unknowable (text does not visibly age) | `stale_after`, `status`, source `last_modified` |
| **Has anyone checked?** | **silence** | a derived tier, sign-off dated |
| **Where did this number come from?** | **wherever the embedding landed** | one sanctioned computation, attested |

> *"These are the questions **every enterprise answer must survive**."*

(**This does not make chunking obsolete** — verbatim recall over large unstructured corpora is still its home ground.)

> **Quiz 4 (a trap):** To rank sources at query time, a teammate wants to read the trust score OKF stores. Which field holds it? (a) `credibility` (b) `trust_score` (c) `usage_count` (d) `verified.score`
> **Answer: none of them** — the premise is false. Ranking is **never computed or stored in the bundle**; it is computed at query time, by each consumer, against its own policy, from the raw signals in `sources`. What the question is really teaching designers: **"wanting a score" is a very natural, very common wrong impulse, and the format must be immune to it.**

---

## Act III: The Channel — Documents → a Retrieval Channel

> *"a derivative artifact with **a human gate built into its format**"*

### Naming the corpse: the authority failure

> *"Similarity retrieval has no notion of **authority**, **currency**, or **correction**. Three definitions of **recognized revenue** across five years: top-*k* returns the most **similar**, never the most **authoritative**. And when an error is found — **no unit to correct**."*
> *"Retrieval dies here not by missing text, but by **returning text no one currently stands behind**."*

**The corpse in the wild — cosine similarity 0.91:**

- a compliance answer from a **superseded policy**
- a metric from a **pre-reorganisation** deck
- an onboarding document naming a **decommissioned service**

All retrieved at 0.91.

> **Invisible to every metric of the last two weeks** — MRR, nDCG, Recall, RAGAS faithfulness are all blind here: the text is **genuinely relevant**, merely **no longer true, or no longer blessed**. **Our geometry has no axis for either.**

### A Week-1 debate, reopened

> Week 1 asked: to chunk or not to chunk? **The axis gains a third point.**
> **Chunk raw text** — meaning re-derived at query time.
> **VLM over the page** — the visual page kept whole.
> **Author into OKF** — the unit made whole **before it is ever retrieved**.
>
> *"One axis underneath: **where does understanding happen?** A chunk boundary **bites the apple and finds half a worm**; a concept is **born whole** — and an LLM integrity pass in CI can verify that wholeness."*

### The transformation: document → bundle, through a gate

```
documents → extraction agent → pull request → governed bundle → retrieval channel
```

> The agent proposes **typed, sourced** concepts; the output lands in a **pull request** reviewed by the **domain owner**. **Only the merged bundle is served.**
>
> *"The PR is **not plumbing** — it is an **epistemic event**: synthesized text is either promoted to governed knowledge, or refused. **Corrections return as diffs, not re-ingestions.**"*

### Three properties

1. **Repair is cheap** — a wrong fact is a **one-line diff**, not a quarterly re-ingestion.
2. **It enables navigation** — an agent walks the indexes and links like a librarian walking the stacks, in parallel with embeddings.
3. **The review gate is structurally native** — **merge is the promotion event**, recorded in `verified`, raising the tier mechanically.
   > *"Recall the phantom cluster: synthesis needs a coherence gate, and **we had to bolt one on**. Here the gate is **the format's native workflow**."*

### The ladder rule is a scoping rule

> Climbing this rung costs in **the currency that matters: sustained human attention.** Extraction is cheap for the agent; **review is expensive for the owner.**
>
> Climb only for the few thousand concepts that are **glossaries, metrics, policies, runbooks and API contracts** — the places where **authority failure is genuinely fatal and an owner holds the pen.**
>
> *"Leave the long tail — slide archives, ten million emails — to the **similarity machinery that handles bulk with grace**."*

### An honest accounting (the debit column, no cushions)

| Debit | |
|---|---|
| **Curation recurs** | a **rubber-stamped** bundle rots into the unaudited corpus it was meant to replace, **with an unearned halo of authority — which is worse** |
| `stale_after` | **is an alarm clock, not a maintenance team** |
| Coverage | structurally incomplete — **curators only answer the questions they anticipated** |
| Extraction itself | **hallucinates** (see the next section) |

**Against that debit column, one credit:**

> *"The only artifact that **gets better with age under use** — corrections accumulate as diffs. **The metal self-anneals.**"*
> (Annealing: controlled heating relieves a metal's internal stresses and makes it tougher. Under continuous use and correction, the corpus works out the stress points that use exposes — **the longer it runs, the fewer its errors** — provided human attention has not been cut off.)

> **Quiz 5:** The VP orders: "Convert all company knowledge — ten million emails, every deck, the wikis, the policy manual — to OKF by Q4."
> **Answer: policy manual, glossary, metric definitions — climb** (definitional, audited, owner-reviewed). **Ten million emails, slide archives — stay below** (**bulk without owners**). The deciding currency is **sustained human attention** — a rung is earned only where an owner will review, because **an unreviewed bundle is just chunks wearing a suit.**

---

## Interlude: The Phantom

### Anatomy

> An agent mints `recognized-revenue.md`: typed frontmatter, a crisp description, **three real sources**, every footnote joined. And the definition is **subtly wrong** — a plausible reconciliation of three **superseded** drafts; **a sentence no version of the policy ever contained.**
>
> *"Interpolating fluently between things that were each individually true — **exactly the way language models synthesize**."*

Note the line this draws between a phantom and merely stale information: **stale information was once true and is no longer; a phantom never appeared in any real document at any point in history.**

### Why it is worse than a bad chunk

> **The trust machinery is a machine for promoting trust.** A phantom that survives review gets merged, stamped human-reviewed, and **filtered into every high-stakes path the tiers were meant to protect.** A hallucinated chunk arrives **naked** and attracts ambient suspicion.
>
> *"The phantom arrives wearing **the review gate's own seal** — a faithfulness failure laundered by the governance process, and **governance is why it will be believed**."*

**The better-governed and more strictly reviewed the system, the more a phantom that slips through will be believed** — not a hole in the governance machinery, but a necessary by-product of it **working correctly.**

### Four defenses, none optional

1. **Review faithfulness, not form** — claims against sources, footnote by footnote. *"YAML hygiene is a **rubber stamp**."*
2. **Tool the faithfulness check itself** — an **entailment pass** over (sentence, cited passage) running in CI, blocking the merge the way tests block code. *"**Tests for knowledge PRs.**"*
3. **No prose room for numbers** — every quantitative claim must land in an attested computation. *"**A phantom cannot forge a receipt.**"* (The only one of the four that does not depend on a linguistic judgement.)
4. **Unverified must look unverified in every consumer surface** — *"or the tiers mean nothing."* (The first three are one-time gates at ingestion; the fourth is a promise re-paid on **every consumption**.)

### The sharpest moral

> *"**A gate concentrates vigilance — it does not replace it.** The format gives the reviewer everything — small diffs, typed claims, joined sources, expiry dates. What it cannot give is **attention**."*
> *"Every governance technique today is the same wager: that attention, **made cheap and pointed precisely**, will be paid. The phantom is **what collects when it is not**."*

---

## Act IV: The Other Bank — Experience → Memory

### Turn the substrate ninety degrees

> Act III pointed the format at **documents** and got a retrieval channel. Point it at an agent's **experience** and you get a **memory store**.
> *"Read the spec beside the memory literature and it reads like **that literature's missing appendix**."*
> *"File-based agent memory — standardized by a vendor that may **never have thought of it as memory at all**."*

### The cognitive map, rehoused

| Memory type | Nature | Bundle organ |
|---|---|---|
| **Semantic** | facts, tenseless | **concept files** — *learning faded to a timestamp* |
| **Episodic** | timestamped events | **`log.md`** — every directory tells its own history |
| **Procedural** | how-to, compiled | **playbook** — a `SKILL.md`, **to within a field name** |
| **Working** | the hot set in attention | **index traversal** — progressive disclosure is pagination |

**A moment of wonder — three lineages, one partition:**

> Google set out to describe **data catalogs** — and the trust problems of an agent-maintained corpus pushed them, **field by field**, onto a map cognitive science drew **fifty years ago**; the map agent folk practice **rediscovered**.
>
> *"When **three independent lineages** arrive at the same partition, **the partition is probably real**."*

(A classic **convergence argument**: top-down theory, bottom-up engineering trial-and-error, and externally-constrained design — three different methodologies with different motives converging on the same four-way split is better evidence of an objective structure than any one of them alone.)

### What the standard buys: three dividends

| Dividend | |
|---|---|
| **Portability** | framework-neutral; **accumulated knowledge stops being a hostage** |
| **Reviewability** | memory writes are diffs; unreviewed memory is **visibly second-class** — **a control surface against memory poisoning** |
| **Shared memory** | **one bundle serves a whole fleet** |

> *"The oncall agent's hard-won diagnosis, merged as a playbook, is recalled by an agent that **never lived the incident** — organizational memory, **non-metaphorically**."*

### Four verbs: write, recall, compact, forget

- **WRITE** — a commit; for anything that matters, a PR. **What deserves remembering = what survives review.**
- **RECALL** — **trust-weighted**: prefer human-reviewed, discount the stale, demand attestation for numbers.
- **COMPACT & FORGET** — consolidation by rewriting, **git is the undo**; `deprecated` = **the annex, not the shredder.**

### The quietest masterstroke: git as a governance machine

> **The spec's quietest masterstroke is what it did not build** — no role system, no ACLs, no approval workflow, because git hosting already has them, **tempered by two decades of code review.**

| git mechanism | Governance function |
|---|---|
| `CODEOWNERS` | domain ownership (a `/finance/` directory makes the finance team a required reviewer) |
| branch protection | nothing unreviewed reaches the served branch — **this is what makes the tiers mean something** |
| CI | frontmatter validation, link integrity, **the entailment pass** |
| releases | a **versioned** corpus ("the agent that gave that compliance answer in March was served by bundle v3.2" is auditable) |
| `revert` | **poisoning undone in one command** — not an archaeological dig through a vector index |

> *"'Knowledge curation becomes a normal software-engineering activity' — **not a metaphor: a reuse claim**, and the reused asset is **the social technology of code review**."*

### The maintenance loop: machines patrol, humans adjudicate

> Nightly: scan for stale concepts, re-check sources, draft refreshing diffs, **re-stamp what holds**, and open PRs where human judgement is needed.
> Staleness becomes a **queue**; the queue becomes a **dashboard**; the dashboard — **freshness debt** — **is trended weekly like test coverage.**
>
> *"Every step reads **standard fields**, so patrol tooling is **generic** — written once, pointed at any bundle. That is what 'agents change the economics' **cashes out to**."*

### Honesty about the seams (where the memory mapping breaks)

- **Recency-weighted recall** — OKF gives you **step functions, not decay curves**. *"Timestamps travel; **half-lives do not**"* — that curve is for the consumer to write.
- **Bitemporality** — "true in Q1, learned in Q3" has **no first-class place in the spec**. *"Two clocks; **the spec ticks one**."*

> *"A student who can **diagnose a spec's memory model** has learned the real lesson."*

> **Quiz 6:** Forty agents, each with a private `MEMORY.md`; the oncall agent's brilliant Tuesday-night diagnosis died with its session. You migrate them to one shared, PR-gated bundle.
> **Answer:** the raw entry is **episodic** (`log.md`); folded into a playbook it is **procedural** (with git holding the **uncompacted past**). The dividend bought is **shared memory** — **the fleet inherits one agent's Tuesday** — at the price **every gate charges**: review attention at merge, **or the bundle rots into a suit full of chunks.**

---

## Coda: The Case Against

A class that cannot make the case against its own subject has not finished thinking.

### The argument that stings most: a downgrade for human authors

> Those **analysts** — accustomed to **rich, zero-training tools** for carrying the identity of "knowledge author" — "a strange text format plus git" **trades their authoring experience for the machine's reading experience.**
>
> The rejoinder (agents mediate, humans review in rendered views) **concedes the core.**
>
> *"If mediation tooling does not materialize, **the knowledgeable will not write** — and the bundles become **a cage for machine summaries**."*

**The absurdity of that risk:** a governance format designed to defend against phantom concepts (knowledge hallucinated by agents) would, if human authors are deterred by the writing barrier, **end up containing only agent-generated content** — the very failure mode it was built to prevent, re-entering through a different door.

### The ceiling, and the ghost

> **The ceiling** — anything spatial, visual, or genuinely relational overflows the format; typed edges written out in prose are unreadable to **deterministic consumers.**
>
> **The ghost** — RDF, OWL, Dublin Core: the semantic web's déjà vu from thirty years ago.
>
> *"But **the ratio inverted**: RDF asked **authors** to carry the burden of formalization, and authors refused. OKF asks **almost nothing of authors** — now it is the **consumers** that read prose. That is why this time may be different."*

**What failed thirty years ago was not the goal but that implementation's choice of whose shoulders to put the burden on. This time the burden is on the right side.**

### The small print that isn't small (four unpaid bills)

1. **No pinned markdown dialect** — footnote joins may parse differently across consumers.
2. **Path as identity** — **renaming silently breaks inbound links.**
3. **Unauthenticated actors** — **`generated.by` asserts; nothing verifies it.**
4. **A flat human tier** — **the intern and the chief actuary sign with identical force.**

> *"Each **hardens an existing joint** rather than adding an **organ** — the mark of a minimal spec that drew its boundary in roughly the right place."*

### The sober forecast

| For | Against |
|---|---|
| free to try | **the authoring gap** |
| the cost of defection deliberately kept low | **no at-scale settlement published** |
| "sell the shovels" tooling arriving on schedule | **single-vendor stewardship** |
| **no articulated rival** | v0.1 → v0.2 in **eight weeks** — that is velocity **and instability** |

> *"The pattern is likely inevitable under any banner. **Formats are ratified by their second vendor, not their first.**"*

That gives a testable criterion for the future: **if other teams and other companies start adopting this pattern without being asked, that is the signal it has landed.**

### The closing figure: the chiasmus

> **Documents** → OKF → **a retrieval channel**: knowledge flowing **from the record toward use.**
> **Experience** → OKF → **memory**: knowledge flowing **from the moment of use back into the record.**
>
> *"RAG and memory are **two directions of one flow across one substrate** — reading the past, and writing it — **the same discipline, met from opposite banks**."*

A concrete example of where the crossing happens: a piece of knowledge about how to debug a class of failure can enter the **same** bundle from two opposite directions — **the document direction**: an engineer writes a runbook, it is reviewed and becomes a concept for future retrieval (record → use); **the memory direction**: an agent actually handles such an incident, and that experience is compacted, reviewed, and written back into the same format (use → record). Two different starting points, opposite directions, **and exactly the same machinery.**

### Promises kept

**THE WHAT:** a governed corpus — small, typed, cross-linked markdown concepts; **one required field**; trust in the frontmatter; **tiers derived at read time**; numbers backed by attestation; all of it in git behind **a human gate**.

> *"Knowledge with **papers to carry**: **typed, sourced, dated, and signed**."*
> (The four words map to Act I's `type`, Act II's `sources`/`verified.by`, `stale_after`/timestamps, and Act III's review-gate signature — the final explanation of the course's title.)

**THE HOW:** climb the ladder only for the governed core · review **faithfulness**, not form · **no prose for numbers** · **machines patrol, humans adjudicate** · and **measure the knowledge base itself**: **coverage, freshness debt, tier mix.**

> *"A gate concentrates vigilance, but it never replaces it. **Budget the attention, or the phantom collects.**"*

---

## The Afternoon: Module 5 · Secure Retrieval (Enterprise Entitlement-RAG)

> *"Building a secure retriever is **engineering**; **proving it stays secure** is the **discipline**."*

The methodological skeleton: **define the problem → do the mathematics → build it → then prove it.** This session covered Sections 1–2.

### 1.1 Traditional RAG's hidden assumption

```
d* = arg max sim(q, d)   over all d in D
```

> *"This formulation assumes **every document in D is available to the user**."*

Hidden in the formula everyone has been using is an assumption never written down: **`sim(q, d)` does not care who may see `d` — its domain has no variable for who is asking.**

### 1.2 Relevance does not imply authorization

> An employee asks: "What are the company's plans for **Project Phoenix**?" — the best semantic match may be an **executive-level acquisition document.**
>
> *"**The retriever did its job perfectly. That is precisely the problem.** A retriever that performs perfectly on a mixed corpus is **an efficient leak**."*

**The stronger the retriever and the better its semantic understanding, the more precisely and efficiently it leaks on an unconstrained mixed corpus.**

> This is the fourth appearance of the "similarity geometry is missing an axis" motif: Act III named three missing axes — **authority / currency / correction** — and this adds the fourth: **authorization.** The pathology is the same in all four: similarity only answers "does this text resemble the question," never "should this person see it, should it be believed, is it still in force."

### 1.3 The corrected formulation

```
D_u = { d ∈ D : Authorized(u, d) = 1 }     # user u's authorized sub-corpus
d*  = arg max sim(q, d)   over d ∈ D_u      # retrieval restricted to it
```

> *"**One subscript changes everything.** D became D_u — and **D_u is not a static property of the corpus**; it is recomputed **per user, per request, from live entitlements**."*

Note how small the formal change is: the parameter goes from `q` to `(q, u)` and a `subject to` clause is appended. But **the domain of `D` itself changed** — unauthorized documents never enter the candidate set at all, which is a categorically different fix from "add an authorization term to the ranking score."

> *"Note what the constraint is **not**: it is **not a term added to the ranking score**, and it is **not an instruction in the system prompt**."*
>
> As a weighted term, a highly relevant but unauthorized document could in principle offset its authorization penalty by being relevant enough. As a system-prompt instruction, it lives at the natural-language layer, where it can be bypassed or negotiated away by prompt injection.

### 1.4 The security principle: prevention vs suppression

| | **PREVENTION** | **SUPPRESSION** |
|---|---|---|
| Mechanism | unauthorized passages **never enter the context window** | the confidential passage enters the context; the model is asked to refuse |
| Nature | **deterministic infrastructure** | the secret now lives **inside a stochastic system** |
| Risk | nothing to leak, nothing to suppress, nothing to trust the model to do | **one prompt injection away** |
| In a word | a **control** | merely a **request** |

> *"A refusal generated **after** the LLM has already received confidential information is **not equivalent to preventing exposure**."*

Even if the model does successfully refuse this time, suppression has already failed — **the exposure happened one step earlier**: the confidential content left the boundary where it should have been physically isolated and entered a stage not governed by deterministic rules.

(**This is exactly the same design pattern as Act II's attestation principle**: take a constraint that must hold unconditionally and is not open to negotiation, and move it from "tell the model and hope it complies" to "the model never gets the opportunity to violate it.")

### 1.5 Six leakage surfaces

> **Retrieval is only the first of six places confidential information escapes.**

1. **Unauthorized retrieval** — the passage enters the candidate set
2. **Unauthorized LLM context** — the passage crosses into the prompt
3. **Generated-answer leakage** — the fact appears in the answer
4. ⚠️ **Citation / metadata leakage** — a title, filename or URL is exposed
5. ⚠️ **Cache leakage** — one user's privileged answer is served to another
6. ⚠️ **Logs / traces / observability leakage** — the secret lands in your SIEM

> **The three highlighted are the ones teams most often forget entirely.**

What makes those three ironic:

- **#4** — the **citation/provenance** mechanism built to increase trustworthiness and traceability (exactly the grounding best practice) becomes a side channel if it does no permission check of its own: a filename like `Project-Phoenix-Board-Deck.pptx` already leaks that such a document exists.
- **#5** — if the semantic cache key is not bound to the requester's authorization identity, an authorized user's answer gets served straight to an unauthorized user who merely asked a semantically similar question. **A bypass around every prevention mechanism.**
- **#6** — the **observability system** built to "prove the system is secure and make auditing easy" becomes another copy of the confidential data if it logs full prompts and contexts without access control. **Auditability and data minimisation are in direct conflict here.**

### The subtlest surface: a refusal can leak more than an answer

> *"I found `Acquisition-of-Company-X.pdf`, but you do not have permission to access it."*
>
> **Perfectly polite. Perfectly correct as a refusal. And it just told an ordinary employee that the company is acquiring Company X.**

**Two different refusals:**

- **content denial** — "you may not see **what is inside** this document"
- **resource-discovery denial** — "you may not even **know this document exists**"

> *"Your tests must distinguish the two. A system that denies content while **confirming the document exists** is still leaking."*

This is a mature pattern from classical security engineering transplanted wholesale: a login form must give the same message for "wrong password" and "no such user" (otherwise it enables username enumeration); HTTP uses 404 rather than 403 to hide a resource an unauthorized user should not know exists.

> ⚠️ **Note the direct conflict with the morning's OKF values:** OKF insists that tolerating red links is a virtue and that "absence means, never excludes" — encouraging transparency about what the corpus does and does not hold. This page demands the opposite for the most sensitive content: **you may not even acknowledge existence.** The two philosophies serve different goals: OKF optimises for **epistemic transparency**, this optimises for **information containment**. **The higher the classification, the more the design must run in the opposite direction.**

### 2.1 Three separate concerns

| | The question it answers | Components |
|---|---|---|
| **Authentication** | **Who are you?** | identity provider · token · session · tenant context |
| **Authorization** | **What are you allowed to access?** | ACL · role · attribute · relationship · policy engine |
| **Retrieval** | **Among what you may see, what is most relevant?** | embedding · lexical · hybrid · reranking |

> *"They can be implemented in one platform. But they must still be **reasoned about — and audited — as three layers**."*

These form a **strict dependency chain** mapping exactly onto 1.3's formula: authentication resolves `u`; authorization computes `Authorized(u,d)`; retrieval runs `arg max sim` inside the narrowed `D_u`.

**Why the separation matters:** if the three collapse into one opaque judgement (handing an LLM the single decision of "may this person see this answer"), a failure **cannot be localised** to a wrong identity, a wrong policy evaluation, or a retriever returning what it should not have.

### 2.2 Four permission models

| Model | Idea | Good for | Watch out for |
|---|---|---|---|
| **ACL** | **the resource names who may see it** | source-system ground truth; per-document exceptions | list size, **drift** |
| **RBAC** | **the job implies the scope** | coarse-grained gating; joiner-mover-leaver hygiene | **role explosion** |
| **ABAC** | **attributes compute permission** | classification, data residency, tenancy, device posture | **metadata quality** |
| **ReBAC** | **a path grants permission** | projects, folders, hierarchies, delegation | **graph traversal cost** |

**ACL** — `{"document_id": "DOC-731", "allow_users": ["u123"], "allow_groups": ["finance", "executives"]}`.
> **This is literally how SharePoint, Google Drive and Confluence store permission**, so ingestion here is a **copy**, not a **translation**. Whatever you prefer downstream, **this is what your ingestion layer meets first.**

**RBAC** — permission is a property of the **job**, not the person. Strength: joiners, movers and leavers update permission **as a side effect** of normal process. Weakness: `Engineer` cannot distinguish "an engineer on Project Falcon," producing combinatorial roles like `Engineer-Falcon-EMEA-Contractor` — **role explosion** growing roughly exponentially with the number of dimensions.
> *"The interesting boundaries are **project, region and classification**, not job title."*

**ABAC** — permission is **computed** from attributes of both sides:
```
user.department == document.department
  AND user.region IN document.allowed_regions
  AND user.clearance >= document.classification
```
Strength: **changing one attribute changes access everywhere at once.** Weakness: entirely dependent on metadata quality — if `document.classification` is unset or wrong, **ABAC fails silently, and it fails open unless you design otherwise.**

**ReBAC** — permission is **a path through a graph**: `Alice --member_of--> Engineering --works_on--> Project Falcon --contains--> roadmap.pdf`.
> Alice may read it **not because a list names her, and not because of her job title, but because a path exists from her to the document.**
> Weakness: graph traversal at query time is a **distributed-systems problem** (dedicated engines: OpenFGA, SpiceDB, both descended from Google's Zanzibar paper).
> *"Reach for ReBAC when your authorization question keeps turning into **'who is connected to what'**."*

> **The four models are not rivals — production systems layer them.** A typical stack: **RBAC for coarse gating, ABAC for classification and data residency, ReBAC or source-system ACLs for the detail — all normalized into one descriptor.**

### 2.3 The normalized security descriptor

> **Source systems disagree about permission. Your ingestion layer must make them agree.**

```json
{
  "document_id":    "DOC-731",
  "tenant":         "acme",
  "classification": "confidential",
  "allow_users":    ["u123"],
  "allow_groups":   ["finance", "executives"],
  "deny_users":     [],
  "regions":        ["US"],
  "projects":       ["phoenix"]
}
```

**"One shape, every source."** SharePoint, Drive, Confluence, Git and ServiceNow each express permission in a different dialect — **the index cannot filter in five dialects at once.**

Field by field: `allow_*` from ACL · `classification`/`regions` from ABAC · **`projects` is the ReBAC edge, flattened** (not a live graph traversal at query time, but a precomputed static field — trading refresh latency for query speed) · `tenant` is the hard isolation boundary · `deny` is the explicit negation.

**Three design rules:**

1. **Absent fields deny, never allow** (directly patching ABAC's fail-open hazard)
2. **Deny beats allow** (someone may be admitted via `finance` group membership while separately listed in `deny_users` for a conflict-of-interest review)
3. **The descriptor is versioned so a decision can be replayed later**

> Rule 3 is **the same design principle** as the morning's independent timestamping of writing and verification (`changed since review`): no governed state may keep only its current value; it must leave a **versioned historical snapshot** — because if a leak is discovered later, the only way to answer "what was the authorization decision at the time" is to roll the descriptor back to the version in force when that query ran.

### 2.4 Permission propagation during chunking

> **Content survives chunking effortlessly. Permissions do not — unless you make them.**

Chunking algorithms operate natively on a **text stream**; content is their direct product. Permissions hang off the **document object**, are not part of the text, and the chunking logic knows nothing about them.

> *"A common implementation error is **preserving document content while losing or incorrectly transforming source permissions**."*

**A red-team criterion you can write directly as a unit test:**

> *"If a chunk is retrieved **on its own**, can the system still say **who is allowed to see it**?"*

(Pull any chunk out of the vector store with no lookup back to the parent document, and check whether its own metadata suffices to answer the authorization question. **Metadata must travel on the object itself, not via an external pointer** — the second independent appearance of the same architectural instinct as OKF's "provenance and trust live in the concept's own frontmatter, not in a separate index.")

### 2.5 Two synchronized pipelines

| | Pipeline | Commentary |
|---|---|---|
| **CONTENT** | `documents → parse → chunk → embed → index` | **well understood. Every RAG team has built one.** |
| **ENTITLEMENT** | `ACLs / groups / relationships → normalize → synchronize → policy state` | **rarely built with the same care. And it changes far more often than the content does.** |

> **Consistency between these two pipelines *is* the security property.**
>
> A document indexed at **10:01** whose permissions change at **10:05** makes a query at **10:06** **a leak waiting to happen.**

**An attention mismatch worth noticing:** once written, content is mostly **static**; permissions change **continuously** (joiners, leavers, transfers, reclassification). **The pipeline that changes fastest and most needs careful synchronization gets the least engineering attention.**

This is also why permission revocation must take effect through **event-driven invalidation** rather than expiring slowly on a TTL.

---

## A thread running under the whole day

The architectural instinct that **"any governed state must be able to answer 'as of when is this a snapshot?' rather than being treated as a permanently current fact"** appeared **independently three times** today, in three unrelated settings:

1. OKF's `generated` vs `verified` timestamps (the `changed since review` mechanism)
2. `D_u` must be recomputed per request and cannot be a static property of the corpus
3. Content-index timestamp vs entitlement-change timestamp (10:01 / 10:05 / 10:06)

**Three different domains — knowledge trust, retrieval scope, access authorization — repeatedly and independently deriving the same principle.**

---

## What to take away

1. **Refuse to treat the corpus as a given.** The unit of retrieval can be a curated knowledge object rather than an arbitrary token window — understanding paid for **once at authoring time**, not re-gambled on every query.
2. **A chunk cannot answer four questions** — who says so, is it still true, has anyone checked, where did this number come from. These are what **every enterprise answer must survive.**
3. **Signals, never scores.** Publish independently verifiable raw readings (`author`/`usage_count`/`last_modified`); trust is inferred **at read time** by each consumer. **The verdict embeds a judge, and judges do not travel.**
4. **Derive the trust tier, don't declare it** — no tier field to forge or rot; `generated` later than `verified` demotes mechanically.
5. **Route numbers through attested computation.** The model may supply values for declared, typed parameters and **may never author or edit the computation.** "Did the sanctioned thing run" degrades to a **string comparison.**
6. **The ladder is a scoping rule** — climb only for the few thousand glossary, metric, policy and runbook concepts; leave the long tail to similarity. The currency is **sustained human attention**, and **an unreviewed bundle is just chunks wearing a suit.**
7. **A phantom concept is worse than a bad chunk** — it arrives wearing the review gate's own seal. All four defenses are required, and the only one not resting on a linguistic judgement is: **a phantom cannot forge a receipt.**
8. **Git is already a governance machine** — CODEOWNERS, branch protection, CI, releases, `revert`. Stop building role systems and approval workflows.
9. **Authorization is a hard constraint before retrieval**, not a term in the ranking score and not a line in the system prompt. A secret already in the context window is exposed even if it was not spoken this time.
10. **There are six leakage surfaces, not three.** Citation metadata, semantic cache, and observability logs are the three most often forgotten entirely. **Even a refusal can leak.**
11. **Consistency between the two pipelines is the security property** — entitlements change far faster than content, and usually get the least investment.

---

## Positioning in one sentence

Week 07 taught us to measure retrieval; Week 08 to measure the generator. **This week taught us that knowledge itself can be manufactured to be judgeable — typed, sourced, dated, and signed.**

At the centre is an inversion: move the intelligence from query time to authoring time. Trust comes in three tiers, **derived from evidence rather than declared**; a number's trust comes from **attested computation**, not from a language model's restatement; the most dangerous failure is not a naked hallucinated chunk but **a phantom concept that passed wearing the review stamp**; and one substrate with two directions of flow — documents into a retrieval channel, experience into memory — is **the same discipline met from opposite banks.**

The afternoon supplied the fourth axis missing from similarity geometry: **relevance does not imply authorization**, and a retriever that performs perfectly over a mixed corpus is **an efficient leak.**

---

## Appendix: OKF vs our Forge (Standards Library) — a post-class comparison

> Not class content. Read off the official Google Cloud announcement blog and `rr-standards/plugins/forge` directly. **Worth checking with someone on the team who knows Forge's original design intent.**

**In one line: OKF is a format specification; Forge is a software-engineering process framework.** Both are in the business of "giving knowledge structure," but they are not solving the same problem.

| Dimension | OKF | Forge |
|---|---|---|
| **Scope** | domain-agnostic; any knowledge fits | five hard-coded artifact types, serving the single scenario of "an engineer writing code" |
| **Typing** | `type` is the one required frontmatter field; a concept's shape is almost entirely the author's call | type is **mechanically derived from filename and path patterns**; each type has hard line limits and required sections |
| **Governance** | derived trust tiers + attested computation | `.policy.md` severity tables (blocking/advisory/informational) + golden test fixtures |
| **Versioning** | the blog does not discuss concept-level versions | every standard/policy/guide carries **semver**; `Implements: standard@version` declares coupling explicitly |
| **Navigation** | `index.md` progressive disclosure — **pull model** | mandatory AGENTS.md + `CLAUDE.md` injection + pre-tool-use hook — **push model** |
| **Organising axis** | around **concepts** (arbitrary knowledge entities) — close to semantic memory | around the **SDLC** (effort / deployable / product) — closer to procedural and episodic memory |

**Philosophically they are inverted: OKF makes the consumer (the agent) chew more prose in exchange for authorial freedom; Forge makes the author follow more structure in exchange for machine verifiability.**

**One thing worth noticing:** Forge's `COVERAGE.md` (a corpus coverage dashboard with five states — complete/draft/stub/absent/major-stale) **is essentially a real existing implementation of the freshness-debt dashboard from class** — it just monitors engineering standards documents rather than a general knowledge bundle.

**What Forge specifically lacks relative to OKF:**

1. **No machine-readable frontmatter** — type is derived from path rules, so the standards library cannot be consumed directly by anything outside the Forge ecosystem.
2. **No content-faithfulness layer of trust** — the severity table checks "is the code compliant," not "has this standard's text itself been verified by anyone." The standards documents themselves have no sources/verified-style provenance fields.
3. **No attested computation** — a specific number or threshold written into a standard has no mechanism to independently verify it is still correct.
4. **Platform coupling, not a portable format** — depends on Claude Code hooks, `CLAUDE.md` injection, and local plugin cache path lookup; OKF is deliberately designed for producer/consumer independence.
5. **No concept-level change history** — there is no equivalent of `log.md` ("this knowledge unit's own history"), only effort-level `.state.json`.

**The single most direct change:** add a YAML frontmatter layer (`type`, `sources`, `verified`) to each file in `standards/`, and rewrite TAXONOMY.md's path-derivation rules as frontmatter declarations. The standards library could then be consumed **simultaneously** by "humans / the Claude Code hook" and by "any OKF-conformant general consumer" — which is exactly the **producer/consumer independence** principle OKF keeps emphasising.

**Addendum: the official reference implementation `GoogleCloudPlatform/knowledge-catalog`** — OKF has a genuinely open-source, actively maintained reference implementation providing two CLIs: `enrich` (**auto-generates** OKF bundles from metadata sources such as BigQuery) and `visualize` (renders a bundle as an interactive force-directed graph in self-contained HTML), with three browsable sample bundles.
> Worth a second thought: **the class all day assumed humans write the markdown concepts, yet the official reference implementation's first use case is agent auto-generation** — another confirmation of "agents change the economics": **once the marginal cost of curation drops, the default answer to "who writes the concepts" may already have quietly shifted from "a person" to "an agent drafts, a person reviews."**

---

## Readings

**Required (a deliberately short list — it's a catch-up week):**

- **The OKF Specification, v0.2** — the spec itself, top to bottom, about a thousand lines of markdown. Focus on the conformance clauses and the trust family. **Being able to read a young standard closely is itself the professional skill this week teaches.**
- **McVeety & Hormati, *How the Open Knowledge Format can improve data sharing*** — the official announcement blog; read it for the framing (a vendor candidly naming the fragmented-context problem) and the LLM-wiki lineage it calls out.
- **Edge et al., *From Local to Global: A Graph RAG Approach*** (arXiv:2404.16130) — read against this week: a community summary is an **induced** graph artifact; an OKF bundle is an **authored and reviewed** one. **Knowing when to reach for which is the mark of the craft.**
- **Sumers et al., *Cognitive Architectures for Language Agents* (CoALA)** (arXiv:2309.02427) — the cleanest statement of the four-tier memory taxonomy we rehoused today.

**Optional:** the `llms.txt` proposal (2024) · Packer et al., *MemGPT* (arXiv:2310.08560) — the RAM-and-disk analogy behind progressive disclosure · the SLSA framework docs — which make "remote attestation transplanted onto SQL" concrete · the comment threads following the OKF announcement (June–July 2026) — where practice states the strongest case against, in its own words.
