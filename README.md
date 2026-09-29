# The Unofficial Guide

<!-- Replace this line with your name and which corpus you picked. -->
MITHUN VENKATESH GOWDA — I picked the "City Guides" corpora.

> **This file is your submission.** Fill it in as you go — most sections get
> written during the milestone that produces them, not at the end.
>
> How the starter works, and every command you'll need, is in `RUNNING.md`.
> Leave that file alone.
>
> **Paste everything as text.** No screenshots, no video. A typed table gets
> full credit; a picture of the same table gets none.
>
> Delete these instruction blocks as you replace them. The `<!-- -->` comments
> are notes to you and don't show up when the page renders — you can leave them
> or remove them.

---

# Unit 1

## What This Does

<!-- Three or four sentences. Which corpus you picked, and the kinds of
     questions your system answers. Write it for someone who has never seen
     this repo.

     Milestone 5. -->

## Chunking Strategy

**Chunk size:** one `##` section, whatever length that happens to be. The sections run 176 to 711 characters, median 297; with the document title prefixed on, the finished chunks run 174 to 762. `CHUNK_SIZE` stays at 800 but only as a ceiling for splitting a section that ever arrives longer than that.
**Overlap:** 0.

<!-- What about YOUR documents made you pick these numbers? Short posts and
     long sectioned guides don't want the same chunking, and "800 seemed
     reasonable" earns nothing. Point at something you noticed when you read
     the documents in Milestone 1.

     If you changed your mind partway through, say so and say why. That's worth
     more than pretending you got it right first time.

     Milestone 3. -->

When I read the documents, I noticed that every one is divided into `##` sections that are complete thoughts. The baseline chunker ignores those boundaries and cuts on a character count, so it splits some of those sections in half. That makes the answer to a question harder to find, because the fact is no longer in any single chunk. I set the chunk size at 800 characters because the longest section in my corpus is 711 characters, so no section will ever be split.

**Why one section and not smaller.** The median section is 297 characters — three or four sentences on a single topic. Splitting that again would separate a fact from the thing it is about, which is the failure I am already trying to fix.

**Why overlap is 0.** Overlap exists to repair a thought that a fixed-size window cut in half. Cutting at headings the author wrote means there is no half to rejoin, so the 120 characters of bleed-over would just be duplicated text making chunks blurrier.

**The text above the first `##`.** Ten documents have a real intro paragraph there, 123 to 250 characters; the other four have nothing but the title line. A heading-based splitter would walk straight past both. I make the intro paragraph its own chunk where there is one, so no text is silently dropped.

### Two things I changed after reading the chunks

Everything above was written before I coded. Printing five chunks and actually reading them changed my mind twice.

**The title-only documents.** My first version emitted the text above the first `##` as a chunk whenever there was any — and in four documents that text is only the title line. So `guide_walking.md#0` came out as a 23-character chunk reading `# Walking in the region`: a heading with nothing under it, which is the same fragment problem I was trying to fix arriving from a different direction. Those four now produce no intro chunk. That took the corpus from 98 chunks to 94, and the shortest chunk from 23 characters to 174.

**Every chunk now carries its document's `# title`.** This is the one I did not see coming. Applying the brief's test — could someone answer a question using only this chunk? — four of my five samples failed it. `## Where to stay` from `guide_corry_vale.md` reads "Perhaps thirty beds in the entire valley" and never says "Corry Vale". The sections don't repeat the town name, because the title already said it once at the top of the document. Splitting on headings threw that title away, so a chunk about a town could no longer be found by the name of that town.

I indexed the same 94 chunks twice to check this was worth doing, once with the title line and once without, and recorded where the chunk containing each answer ranked:

| Question | No title | With title |
|---|---|---|
| Best months to visit Brightwater | rank 5, 0.4541 | **rank 1, 0.2938** |
| When Halden Bay parking fills | rank 1, 0.3296 | rank 2, 0.3276 |
| How often Elder Ness floods | rank 1, 0.4362 | **rank 1, 0.3101** |
| Which town has a full hospital | rank 1, 0.3556 | rank 1, 0.3839 |
| Kestrelford pub food hours | rank 1, 0.2658 | **rank 1, 0.1936** |

It is not free. On the hospital question the title of `guide_accessibility.md` has nothing to do with hospitals, so it dilutes the chunk and the distance gets *worse*, 0.3556 to 0.3839. I kept it anyway: that chunk is rank 1 either way, whereas the Brightwater question was sitting in the last retrieved slot and is now first.

**Final numbers:** 94 chunks, 322 characters on average, shortest 174, longest 762.

## Sample Chunks

<!-- Five chunks, pasted as text. Label each one and name the file it came from
     AND the function that produced it — the grader checks your code against
     what you claim here.

     `python app.py chunks -n 5` prints all three for you. Copy them straight
     across.

     Milestone 3. -->

Printed by `python app.py chunks -n 5`.

**Chunk 1** — source: `guide_accessibility.md#0` — produced by: `chunker.py::split_documents`

```
# Getting around the region with limited mobility

An honest assessment rather than a promotional one. Some of these places are
difficult and it is better to know in advance.
```

**Chunk 2** — source: `guide_corry_vale.md#5` — produced by: `chunker.py::split_documents`

```
# Corry Vale

## Where to stay

Perhaps thirty beds in the entire valley, spread across two pubs and a handful of farmhouse rooms. In summer these are booked months ahead. Camping is permitted on two marked fields and nowhere else.
```

**Chunk 3** — source: `guide_givens_mill.md#2` — produced by: `chunker.py::split_documents`

```
# Givens Mill

## Getting around

Everything is on one street along the river. The mill is at one end and the church at the other, eight minutes apart. The riverside path continues in both directions for as far as you want to walk.
```

**Chunk 4** — source: `guide_kestrelford.md#4` — produced by: `chunker.py::split_documents`

```
# Kestrelford

## What to see

The market square on a Saturday morning is the main event and has run continuously since the 1400s. The parish church has a 13th-century tower you can climb for £2. The old trackbed walk runs six miles to the next village along an easy gradient and is the best half-day here.
```

**Chunk 5** — source: `guide_pellew_sands.md#6` — produced by: `chunker.py::split_documents`

```
# Pellew Sands

## When to go

June and September for the beach without the crowds. July and August are busy and the town is at its most itself, for better and worse. Winter is bleak, largely closed, and has a following among people who like that sort of thing.
```

Each of these names its own town, so each can be retrieved by that town's name and read on its own. That was not true before I added the title line — chunks 2 to 5 would have been an anonymous `## Where to stay` or `## What to see`.

## Sample Answer

<!-- One complete question and answer, pasted as text, with the source line
     visible. Milestone 4. -->

**Question:** If I need a full hospital rather than a minor injuries unit, which town do I go to?

**Answer:** produced by `app.py ask`, which is `store.py::search` → `gate.py::check` → `generate.py::answer_from_chunks`.

```
  (best distance 0.384, cutoff 0.4)

According to `guide_accessibility.md`, the nearest full hospital is in Marchwood.

However, `guide_givens_mill.md`, `guide_kestrelford.md`, `guide_marchwood.md`, and
`guide_thornby_wells.md` all state that the nearest full hospital is in Brightwater.
Because the documents disagree, both answers are given depending on the source used.

Sources retrieved: guide_accessibility.md, guide_givens_mill.md, guide_kestrelford.md, guide_marchwood.md, guide_thornby_wells.md
```

I picked this question because it is the one my corpus is worst at. Nine of my
fourteen documents end with an identical "Practical notes" paragraph saying
"The nearest full hospital is in Brightwater", and `guide_accessibility.md`
contradicts all nine: "The nearest full hospital is in Marchwood." So one
correct chunk is competing with nine near-identical decoys, and the answer
above is grounded — every filename it names really does contain the claim it is
attached to.

**My relevance cutoff:** `THRESHOLD = 0.40` in `config.py`.

<!-- The number you set in config.py, and how you got there.

     You ran five questions your corpus covers and the five in OUT_OF_SCOPE
     that it clearly doesn't, and wrote down the best distance for each. What
     did those two groups look like? Where was the gap? Put the actual numbers
     here — the table below wants all ten rows.

     Milestone 4. -->

Measured with `store.py::search`, top-k 5, baseline chunker (51 chunks).

| Question | In corpus? | Best distance |
|---|---|---|
| How often does the access road to Elder Ness flood? | yes | 0.287 |
| If I need a full hospital rather than a minor injuries unit, which town do I go to? | yes | 0.291 |
| What hours do the pubs in Kestrelford serve food? | yes | 0.343 |
| What are the best months to visit Brightwater? | yes | 0.369 |
| When do the parking lots in Halden Bay fill up on summer weekends? | yes | 0.372 |
| What time does the fish market in Bergen open? | no | 0.467 |
| How long is the coastal walk around Cape Town? | no | 0.499 |
| What are the best months to visit Barcelona? | no | 0.513 |
| How do I write a for loop in Rust? | no | 0.853 |
| Who won the 1994 World Cup? | no | 0.903 |

In-corpus questions cluster at **0.287–0.372**. Out-of-corpus questions start
at **0.467**, so the gap is 0.372 → 0.467, about 0.095 wide.

### Re-measured after Milestone 3

Re-chunking moved all ten numbers, so the table above no longer describes my
system. Same ten questions, same `store.py::search` at top-k 5, against the 94
heading-split chunks:

| Question | In corpus? | Best distance |
|---|---|---|
| What hours do the pubs in Kestrelford serve food? | yes | 0.194 |
| What are the best months to visit Brightwater? | yes | 0.294 |
| How often does the access road to Elder Ness flood? | yes | 0.310 |
| When do the parking lots in Halden Bay fill up on summer weekends? | yes | 0.325 |
| If I need a full hospital rather than a minor injuries unit, which town do I go to? | yes | 0.384 |
| How long is the coastal walk around Cape Town? | no | 0.409 |
| What time does the fish market in Bergen open? | no | 0.453 |
| What are the best months to visit Barcelona? | no | 0.533 |
| How do I write a for loop in Rust? | no | 0.836 |
| Who won the 1994 World Cup? | no | 0.975 |

In-corpus now runs **0.194 to 0.384** and out-of-corpus **0.409 to 0.975**. Every
in-corpus question got closer, which is what I wanted from the chunker. But the
out-of-corpus near-misses got closer too, so the gap narrowed from 0.095 to
**0.38390 → 0.40877, about 0.0249 wide**.

**Why 0.40.** Any number inside that gap refuses all five out-of-corpus
questions and wrongly refuses none of mine, so the gap decides almost
everything and I only had to pick where inside it. The midpoint is 0.3963 and I
went slightly above it, to 0.40, because the two errors are not equally
visible. Refusing a question I could have answered is the error a user notices
and is annoyed by; letting a near-miss through produces an answer that looks
fine. So I gave the in-corpus side the larger margin — 0.016 of headroom below
the cutoff, against 0.0088 above it.

The starter's 0.6 let three of my five out-of-corpus questions through, because
all three are travel questions about real places (Bergen, Cape Town,
Barcelona) that score far closer to a corpus of travel guides than the
far-field ones do. Rust and the World Cup would be refused by almost any
cutoff; those three are the ones that make the number matter.

**What this cutoff costs me.** I tried a sixth in-corpus question — "How much
does it cost to climb the church tower in Kestrelford, and what are its opening
hours?" — and the gate refused it at 0.4126, even though the top chunk really
does contain "£2". Worse, 0.4126 is *above* Cape Town's 0.40877, so there is no
cutoff anywhere that accepts this question and still refuses my out-of-corpus
set. My clean gap is clean for the ten questions I measured, not in general.
The compound phrasing seems to be what costs it: the answer to half the
question genuinely isn't in the corpus.

### Grounding

`GROUNDING_INSTRUCTION` in `generate.py` already covered the obvious things —
use only these documents, admit when they don't cover it, name the file. I
tightened it after this answer:

```
Q: Where is the nearest hospital if I am staying in Kestrelford?
A: According to `guide_kestrelford.md`, the nearest full hospital to
   Kestrelford is in Brightwater.
```

`guide_accessibility.md` was retrieved for that question and says the nearest
full hospital is in Marchwood, and that Kestrelford has only a minor injuries
unit. The answer is *grounded* — `guide_kestrelford.md` does say Brightwater —
but the model silently picked one of two contradicting sources and the reader
cannot tell. The starter's instruction has no rule for conflicts, and my corpus
has a known one. I added two rules:

- Only name a document that actually states the fact you are giving. Do not
  cite a document merely because it mentions the same place.
- If two documents disagree, say so and give both answers with their
  filenames. Do not silently pick one.

The same question now returns "The documents disagree on the location of the
nearest full hospital for Kestrelford" and names both files. All five of my
test questions still answer correctly.

### Top-k

Left at 5, but checked rather than inherited. The chunk containing the answer is at rank 1 for four of my five questions and rank 2 for the fifth, so top-k could be as low as 2. I tried it, because on the hospital question ranks 2 to 5 are all decoys carrying the wrong fact and I expected fewer chunks to help:

| top-k | Answer |
|---|---|
| 5 | "According to `guide_accessibility.md`, the nearest full hospital is in Marchwood." |
| 3 | "...you go to Marchwood (from `guide_accessibility.md`) or Brightwater (from `guide_givens_mill.md`)..." |
| 2 | "If you are in Givens Mill... Brightwater. If you are referring to the region generally... Marchwood." |

The opposite of what I expected: 5 gives the cleanest correct answer and
trimming it makes the model hedge. I kept 5.

## How I Used AI

<!-- Two specific moments. For each: what you asked for, what came back, and
     what you changed about it.

     "I asked Claude to write the chunking function from my notes. It ignored
     the overlap, so I added that myself" is the level of detail we're after.
     "I used AI to help me code" is not.

     Milestone 5. -->

**1.**

**2.**

<!-- ── Stretch features ─────────────────────────────────────────────────────
     Doing one? Say so here BEFORE you start. A feature this README never
     claims earns nothing.
     ───────────────────────────────────────────────────────────────────────── -->

---

# Unit 2

<!-- These sections get ADDED to what's already above. Don't delete or rewrite
     unit 1 — the point is that someone can see what you said before you knew
     how it went. -->

## Run Log — Before

<!-- Your five criteria, three runs each. `python run_eval.py --label before`
     runs the questions, puts the OUT_OF_SCOPE ones through the gate, and
     writes it all into results/ for you. Targets come from criteria.md; the
     verdict column is your call.

     Criterion 3 is measured in one deterministic pass rather than three, so
     the same number goes in all three run columns. That's correct, not lazy.

     Milestone 1. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

<!-- Underneath, paste the REAL output for each criterion from one of your
     runs — the actual text your system produced, not a description of it.
     Name the file and function that produced it. -->

## Verdicts

<!-- MET or MISSED for each of the five, against the target you wrote last
     unit — not a new one. Plus a sentence on how you decided. That sentence
     matters most where it was close.

     If your target said 4 of 5 and your runs came out 4, 3, 4, that's a MISS.
     The target has to hold, not show up occasionally.

     Milestone 2. -->

| # | Criterion | Verdict | How I decided |
|---|---|---|---|
| 1 |  |  |  |
| 2 |  |  |  |
| 3 |  |  |  |
| 4 |  |  |  |
| 5 |  |  |  |

## Diagnoses

<!-- For each miss: which stage caused it, and how. The stage alone isn't
     enough — you need the mechanism.

     Not a diagnosis: "Question 3 didn't work."
     A diagnosis:     "Question 3 asks about laundry costs. The answer is in
                       one sentence that got split across two chunks, so
                       neither chunk on its own contains it."

     The five stages: loading → chunking → embedding → retrieval → generation.

     Look for a pattern. If three misses all ask about numbers, that's one
     problem, not three.

     Missed nothing? Say so, then say honestly whether your targets were set
     low, and which one you'd tighten and to what.

     Milestone 3. -->

## The Improvement

**What I changed:**

**Why I picked it:**

<!-- Connect it to a specific diagnosis above in one sentence. If you can't,
     you picked a fix because it sounded impressive. -->

### Run Log — After

<!-- Same format, same five criteria, three runs each.
     `python run_eval.py --label after` -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Retrieved chunk contains the answer | 4 of 5 |  |  |  |  |
| 2. Every answer names a source | 5 of 5 |  |  |  |  |
| 3. Gate stops out-of-corpus questions | 4 of 5 |  |  |  |  |
| 4. | | | | | |
| 5. | | | | | |

**Did it help?**

<!-- Say plainly whether it did, and how you know. If it made things worse,
     say that — a change that backfired, honestly reported, earns full credit
     and is more interesting than one that worked. What matters is that you can
     tell.

     Milestone 4. -->

## What's Still Broken

<!-- For each criterion still missed after your fix: what you'd do about it,
     and why you stopped where you did.

     "I ran out of time" is fine if it's true. Pretending nothing is left is
     not.

     Milestone 5. -->

## What I'd Do Differently

<!-- Knowing what you know now — which of your five criteria would you write
     differently, and why?

     Milestone 5. -->
