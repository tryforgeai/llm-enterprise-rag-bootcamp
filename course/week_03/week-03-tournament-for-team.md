# Week 03 Companion — We Ran the Chunking Tournament

**Companion to:** `week-03-summary-for-team.md` · **Artifact:** `evals/week03-representation-tournament/`

---

The Week 03 summary makes a claim: chunking isn't preprocessing, it's a representation decision, and representation decisions should be settled by competition rather than by argument. That claim is worth nothing unless someone runs the competition. So we ran it.

Three chunking strategies, one corpus, one query set, one scoreboard. Fixed-size windows (the usual default), semantic boundaries detected from lexical cohesion, and contextual chunks that carry a prefix telling each chunk what it's part of. All three built from an identical parse and cleanup, so the only thing that differs is where the boundaries fall and what context each unit carries.

## What came out of it

**Fixed-size chunking lost — and lost in an interesting way.** It finds the right pages roughly as often as the others. It just orders them badly. This is the centroid-delusion failure from the week note showing up as a number: a window that straddles two topics is moderately similar to lots of queries, so it lands in the candidate set without ever deserving the top slot. If your retrieval feels vaguely-relevant rather than wrong, this is probably why.

**Semantic chunking was both cheaper and better.** It produced the best evidence while reading noticeably fewer chunks to get there. Half as many units, each about twice as long, and better results out of them. That matters beyond retrieval quality: fewer units read means less noise in the generation context.

**Contextual chunking won exactly where the week note predicted.** It was the only strategy to score perfectly on the two query families where a chunk needs to know what it belongs to — conditional claims, and questions whose answer lives in a figure. It pays for that with more near-duplicate chunks crowding the top of the ranking, so it needs a wider retrieval window before it pays off.

## The result we weren't looking for

The most useful finding wasn't the thing being tested.

Our PDF parser silently drops word spacing on a chunk of the corpus — `Theproblemofsearchingforpatterns`. We added a repair pass early on and mostly forgot about it. Turning it off as a sanity check produced the real headline: **without the repair, contextual chunking's entire advantage disappears.** It becomes indistinguishable from the naive fixed-window baseline.

Which makes sense once stated. Restoring context around a corrupted passage restores context around a corrupted passage.

The practical version: **measure your parser before you measure your chunker.** Otherwise your tournament quietly ranks extraction quality while appearing to rank representations — and you'll conclude that a chunking strategy doesn't work when what actually happened is that it never got readable text to work with.

It's also the strongest argument we have for page-image retrieval, which skips the parser entirely.

## What's still broken

Every strategy confidently answered a question the corpus can't answer. We asked about dropout; the book has a section titled "Regularization in Neural Networks" and nothing about dropout. Near-total word overlap, zero answerability, and our confidence signal couldn't tell the difference.

Worth flagging because this is the *same* failure our main eval hit on a completely different corpus. Two datasets, one failure — so it's the abstention gate that's wrong, not the data. Word overlap is a necessary signal for refusing to answer, and clearly not a sufficient one.

## If you want to run one on your own corpus

The harness is reusable and the setup is deliberately boring: standard library only, under a second, no API key, no model download. Two design choices are worth stealing.

**Score everything at page level.** A text chunk, a multi-page semantic tile, and a rendered page image can all be projected onto pages — and page is the only unit where a text pipeline and a vision pipeline can be compared at all.

**Derive gold from the document's own structure, never from query terms.** We read section boundaries out of the book's running headers. If you define gold as "pages containing the query words," your keyword retriever is being graded against its own answer key and the whole exercise is circular. This is the easiest mistake to make and the hardest to notice afterwards.

One more thing we'd pass on: we found three bugs in our own scoring before we found anything about chunking, and each one looked exactly like a real result on the way past. Build the independent metric re-check first. It's cheap, and it's the difference between a finding and a story.

---

Numbers, method, limitations, and how to add the page-image arm: `evals/week03-representation-tournament/README.md`
