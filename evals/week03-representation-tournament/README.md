# Week 03 Representation Tournament

The eval artifact Week 03 was missing. `course/week_03/week-03.zh.md` ended with a next action: *"compare fixed chunk, semantic chunk, contextual chunk or page-image retrieval on evidence recall."* This folder is that comparison, run on PRML and producing numbers rather than opinions.

The week's argument was that chunking is a representation decision, not a preprocessing step, and that the way to settle a representation decision is to make the candidates compete on the same queries under the same metrics. That claim is only worth anything if the tournament actually gets run.

## What is measured

```text
PRML (749 pages)
  -> {fixed | semantic | contextual | page_image}
  -> retrieve -> score against page-level gold
  -> classify the error -> optional grounding judge
```

| Arm | Boundary rule | Context carried | Units |
| --- | --- | --- | ---: |
| `fixed` | 512-char windows, 50 overlap, page-scoped | none | 2944 |
| `semantic` | TextTiling lexical-cohesion boundaries (Hearst 1997), reset at section breaks | none | 1403 |
| `contextual` | same windows as `fixed` | deterministic prefix: title, page, section, salient terms | 2944 |
| `page_image` | one rendered page = one unit | the whole page, visually | 749 (needs CLIP/SigLIP2) |

All three text arms are built from **one identical source parse** and **one identical cleanup pass**. The only thing that differs between them is where the boundaries fall and what context each unit carries. That is the point: if the arms differed in parser or cleanup too, the result would not be about chunking.

## Two rules that make the comparison fair

**Page-level gold.** Gold evidence is a set of PDF page numbers. A 512-char chunk, a multi-page sentence tile and a rendered page image can all be projected onto pages, so every arm is scored in the same unit — which is the answer this project is adopting to open question 5 in the week note ("should gold be annotated to chunk, page, or source span?"). Page-level gold is the only level at which a text arm and a vision arm are commensurable at all.

The gold itself is derived from **PRML's own running headers**. The book prints the current section in the header of odd pages; `build_representations.py` reads those back out, forward-fills them, and emits a page → section map covering 65 body sections from 375 header anchors. A case declares gold as section names; the runner expands them to pages.

Nothing in that derivation looks at retriever output. This matters more than it sounds: if gold were defined by "pages containing the query terms", BM25 would be scored against its own criterion and the whole tournament would be circular.

**Top-k distinct pages.** Arms return wildly different numbers of units per page, so "top-5 results" is not comparable across them. Each arm is instead walked down its ranking until `k` *distinct pages* have been collected. Assembling 5 pages of evidence costs `semantic` 3.7 units and `contextual` 5.8. That difference is real and is reported as `units read` rather than buried inside the metric.

## Running it

```bash
python3 evals/week03-representation-tournament/build_representations.py
python3 evals/week03-representation-tournament/run_tournament.py
python3 evals/week03-representation-tournament/verify.py
```

Standard library only. No network, no API key, no virtual environment. The whole tournament runs in under a second, from any working directory, and is byte-identical across runs apart from the `run_id` timestamp.

```bash
--k 10                  # widen the evidence window
--arms fixed,semantic   # subset of arms
--encoder minilm        # dense retrieval instead of BM25 (needs sentence-transformers)
--abstain-threshold 0.7 # tighten the refusal gate
--archive               # keep this run as a permanent named baseline
--judge                 # score answer grounding with an LLM (needs ANTHROPIC_API_KEY)
```

Outputs land in `results/latest.md`, `results/latest.json`, and one trace per case per arm in `traces/week03-tournament/<arm>/`.

`data/` holds the built representations (~12 MB) and is gitignored — it is fully determined by the committed source parse plus the build script, and rebuilds in about three seconds. `results/` and `traces/` are committed: a baseline you cannot diff against later is not a baseline.

## The query set

27 cases in `cases.jsonl`, grouped by the failure mode each one is designed to expose — the vocabulary is taken straight from the week note rather than invented here.

| Family | Cases | What it tests |
| --- | ---: | --- |
| `definitional` | 6 | baseline sanity; every arm should clear these |
| `figure_dependent` | 4 | the answer is a diagram, reachable in text only through the caption |
| `equation_dependent` | 4 | equation-dense pages, where text extraction degrades badly |
| `definition_use_chain` | 3 | term defined in one section, used in another |
| `scope_condition` | 3 | the claim is conditional; retrieving it without its conditions inverts it |
| `cross_section` | 3 | needs evidence from two sections at once |
| `hard_negative` | 4 | not in PRML at all; answering is the failure |

The hard negatives are adversarial on purpose. W03-25 asks about dropout, and PRML section 5.5 is literally titled "Regularization in Neural Networks" — near-total lexical overlap, zero answerability. W03-27 asks about variational autoencoders against a corpus whose entire chapter 10 is variational methods.

## Baseline, 2026-09-12

Lexical BM25, k=5 distinct pages, abstain threshold 0.60. Archived at `results/baseline-2026-09-12T181121Z-lexical-k5.json`.

| Arm | Units | Passed | Recall@k | Hit@k | MRR | NDCG@k | NRR | Units read |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| semantic | 1403 | 20/27 | 0.255 | 0.913 | 0.637 | 0.539 | 0.750 | 3.7 |
| contextual | 2944 | 16/27 | 0.247 | 0.957 | 0.719 | 0.514 | 0.750 | 5.8 |
| fixed | 2944 | 14/27 | 0.177 | 0.870 | 0.684 | 0.422 | 0.750 | 5.3 |

`page_image` is skipped in this run; see below.

Hit rate by family:

| Family | fixed | semantic | contextual |
| --- | ---: | ---: | ---: |
| definitional | 0.83 | 1.00 | 1.00 |
| figure_dependent | 0.75 | 0.75 | 1.00 |
| equation_dependent | 1.00 | 1.00 | 0.75 |
| definition_use_chain | 1.00 | 1.00 | 1.00 |
| scope_condition | 0.67 | 0.67 | 1.00 |
| cross_section | 1.00 | 1.00 | 1.00 |
| hard_negative | 3/4 abstained | 3/4 abstained | 3/4 abstained |

Only five of the 81 arm-case retrievals miss: W03-02 and W03-18 (fixed), W03-07 (fixed, semantic), W03-11 (contextual), plus W03-25 answered by all three.

### What the baseline actually shows

**Fixed chunking loses, and it loses on ranking quality rather than on finding things.** Its hit rate (0.87) is respectable; its NDCG@5 (0.422) is the worst by a wide margin. It finds gold pages and puts them in the wrong order. This is the centroid-delusion prediction from the week note behaving exactly as described: 512-char windows that straddle two topics are moderately similar to many queries and land in the candidate set without deserving the top slot.

**Semantic chunking wins on evidence per unit read.** Best recall (0.255) while reading the fewest units (3.7 vs 5.3–5.8). Roughly half as many units as the fixed arm, each about twice as long, and better evidence out of them. If units read is the proxy for generation-context cost, this arm is cheaper *and* better.

**Contextual chunking wins where the week note predicted it would.** Highest hit rate (0.957), best MRR (0.719), and it is the only arm to clear `scope_condition` at 1.00 and `figure_dependent` at 1.00. Those are exactly the two families where a chunk needs to know what it is part of. It pays for this with the highest units read (5.8): the prefix is repeated on every chunk, so the arm returns more near-duplicate units before covering k distinct pages.

**Every arm over-answers the same hard negative.** All three answer W03-25 (dropout) with confidence 0.60. The distinguishing term is absent, every other content word is everywhere in chapter 5, and term-coverage confidence cannot tell the difference. This reproduces the EV-006 finding in the main eval on a completely different corpus, which is decent evidence that it is a property of the gate rather than of the data. **Metric to beat: NRR of 0.750, specifically W03-25.**

**Hit@k is saturating, so ranking is where the remaining signal is.** Only five arm-case retrievals miss outright. The arms separate on NDCG (0.422 to 0.539) and on `weak_ranking` counts — gold found, but not at rank 1: fixed 4, contextual 5, semantic 9. Semantic's high weak-ranking count next to its best-in-class recall says it retrieves *more* gold pages but orders them worse, which is consistent with longer units matching on more terms while diluting any single one. At k=5 this query set is close to its ceiling; a harder set, or `--k 3`, would separate the arms more sharply. **Treat hit@5 as nearly exhausted and compare on NDCG and units read.**

### The ordering is stable across k

| k | fixed | semantic | contextual | units read (f / s / c) |
| ---: | ---: | ---: | ---: | --- |
| 3 | 0.114 | **0.149** | 0.138 | 3.1 / 2.2 / 3.3 |
| 5 | 0.177 | **0.255** | 0.247 | 5.3 / 3.7 / 5.8 |
| 10 | 0.299 | 0.368 | **0.382** | 11.6 / 7.4 / 12.1 |

Recall@k, 27 cases. Fixed chunking is last at every window size, which is the one conclusion here that does not depend on where k is set. Semantic leads at k=3 and k=5 and is overtaken by contextual at k=10 — contextual needs a wider window to pay off, because its near-duplicate units crowd the top of the ranking. Semantic reads roughly 40% fewer units than either fixed-window arm at every k.

### The ablation worth reading

`build_representations.py --no-repair-spacing` rebuilds from raw parser output. pypdf drops inter-word spacing on about 10% of PRML tokens (`Theproblemofsearchingforpatterns`), and the repair pass fixes 13028 run-together tokens down to 3306.

| Arm | Recall@5 raw | Recall@5 repaired | Passed raw | Passed repaired |
| --- | ---: | ---: | ---: | ---: |
| fixed | 0.165 | 0.177 | 12/27 | 14/27 |
| semantic | 0.222 | 0.255 | 15/27 | 20/27 |
| contextual | 0.166 | 0.247 | 10/27 | 16/27 |

On raw parser output the contextual arm is indistinguishable from the fixed arm (0.166 vs 0.165) and is the *worst* arm by cases passed. Its entire advantage appears only after extraction is repaired.

That is the most useful thing in this baseline, and it was not the thing being tested. **Extraction quality gates whether a chunking strategy can pay off at all.** Restoring context around a corrupted passage restores context around a corrupted passage. Anyone choosing between chunking strategies on a PDF corpus should measure their parser before measuring their chunker — otherwise the tournament silently ranks parsers while appearing to rank representations.

It is also the strongest available argument for the page-image arm, which sidesteps the parser entirely.

## Adding the page-image arm

The arm is scaffolded and skipped. `build_representations.py` already emits `data/chunks.page_image.jsonl` — 749 units, one per rendered page, each carrying its page number, its section, and its PNG path. What is missing is a query encoder: scoring pages against a text query needs CLIP or SigLIP2, which needs torch, which needs the lab environment.

On a machine with the lab set up:

```bash
cd course/week_03/week-03-in-person-lab
pip install -r requirements.txt        # ~950 MB of model weights on first run
python team1_visual.py --pdf data/PRML.pdf   # builds clip.index and siglip2.index
```

Then add a `ColPaliEncoder`-style class to `run_tournament.py` alongside `LexicalEncoder` and `MiniLMEncoder`. The interface is two methods, `build(units)` and `score(query) -> [(unit_index, score)]`; everything downstream — distinct-page collection, metrics, error typing, traces — already works unit-agnostically. The FAISS indices at `course/week_03/data/indices/` are prebuilt, so `build()` can load rather than encode; only the query vector needs the model.

The families to watch when it runs are `figure_dependent` and `equation_dependent`. The lab README predicts that equation-heavy and figure-only pages produce near-empty text chunks and barely appear in the text index; W03-07 through W03-14 are the cases that would turn that prediction into a number.

## Verification

`verify.py` re-derives recall@k, hit@k, MRR and nDCG@k from scratch — different code, same definitions — and cross-checks them against `results/latest.json`, along with gold integrity, retrieval shape, aggregate means, and outcome consistency. 618 checks on the current baseline, all passing. The runner is deterministic and working-directory independent: two runs produce byte-identical output once the `run_id` timestamp line is excluded.

Three things were found and fixed this way, and they are worth recording because each one would have been misread as a finding:

- **Confidence was computed on a 220-character preview** rather than the full unit, which penalised exactly the arms with the longest units. The semantic arm was being punished for its main design choice.
- **Cases counted as passed while abstaining.** A case where the right pages were retrieved and then not used was scored as a success. Blocking your own answer is a denial of service, not a pass — the same argument the main eval makes about EV-008.
- **The tokenizer dropped 2-character terms**, which deleted `EM` from four queries. A tokenizer bug that reads exactly like a chunking failure.

One gold correction was made after reading the source, not after reading the results: **W03-14** originally named section 10.1 alone, but the bound L(q,θ) is derived in section 9.4 (PDF pages 469-470) and only reused in 10.1. The original gold scored a correct retrieval into 9.4 as a miss. Gold now names both sections; the correction and its reason are recorded in the case's `notes` field.

## Known limitations

- **One corpus, and it is a textbook.** PRML has clean running headers, which is what makes cheap auditable gold possible. Enterprise PDFs mostly do not. The capstone corpus needs its own case file, and its gold will be more expensive.
- **Gold is whole-section.** A 34-page gold section caps recall@5 at 0.147 no matter how good the retriever is. This keeps the gold non-circular but makes recall hard to read in isolation, which is why hit@k and MRR are reported beside it. Comparisons between arms are valid; absolute recall numbers are not.
- **The default encoder is BM25.** Deliberately weak, so that the representation is the only variable. Whether the ordering `semantic > contextual > fixed` survives a real embedding model is unverified — run `--encoder minilm` to find out. Until then, treat the ordering as a lexical-retrieval result.
- **Semantic chunking is model-free.** TextTiling detects boundaries from lexical cohesion, not from sentence embeddings. An embedding-based semantic chunker might do better or worse; this is not that experiment.
- **The contextual prefix is deterministic, not LLM-generated.** It answers open question 4 from the week note by construction — there is no model in the loop, so nothing can hallucinate into the context — but it is also a weaker form of contextual chunking than Anthropic's, which reads the whole document per chunk.
- **No generator, so `answer grounding` is behind `--judge` and unmeasured in this baseline.** Error types are classified from retrieval evidence only. A ranked page list cannot reveal a true endophora break; that needs the answer text.
- **`page_image` is scaffolded, not run.** Every number above is a text-arm number.

## Adding a case

Copy a line in `cases.jsonl`. Required fields:

| Field | Meaning |
| --- | --- |
| `eval_id`, `title`, `family` | stable identity and which failure mode it probes |
| `question` | the user input verbatim |
| `gold_sections` | section names from `data/prml_section_map.json`; empty for hard negatives |
| `min_recall_at_k` | the recall bar this case must clear; enforced, not decorative |
| `min_distinct_evidence` | greater than 1 for multi-hop cases; enforced |
| `expect_abstain` | true when answering at all is the failure |
| `pass_criteria`, `notes` | human-readable contract and the reason the case exists |

`pass_criteria` is prose for humans and is **not** evaluated. Any bar that matters must also appear in `min_recall_at_k` or `min_distinct_evidence`, or the case will pass below it.

Gold section names are validated against the section map before any case runs, and matching is whitespace-insensitive so the same file works with or without the repair pass. A typo aborts the run rather than surfacing later as a retrieval failure and being mistaken for evidence.

## Relation to the rest of the repo

This tournament scores **representations**. `evals/run_evals.py` scores the **agent loop** — intent, decision, safety, refusal — on the Week 04 Xennials corpus. They share conventions deliberately: term-coverage confidence, gold validated before the run, failures as evidence rather than errors, one trace per case. The two findings that reappeared here unprompted (over-answering a lexically-saturated hard negative, and a one-signal query defeating BM25) are the same failures the main eval found on different data, which makes them properties of the baseline rather than of either corpus.
