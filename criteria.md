# Acceptance criteria — The Unofficial Guide

Five criteria that say what "working" means for this system, written in unit 1
**before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something
a person could plainly observe. *"Retrieval works"* is an opinion. *"For at
least 4 of my 5 test questions, the top results include a chunk containing the
answer"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a
stricter or looser one. A reason that says something about your corpus or your
pipeline earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## 1. Retrieved chunks contain the answer

For at least 4 of my 5 test questions, the retrieved chunks include one that
contains the answer.

**Why this target:**
<!-- e.g. "One of my questions is about a topic only two documents mention, so
     I expect that one to be hard." -->
Question 4 is about a hospital in Marchwood, which is only mentioned in one document.There are 9 close documents that would otherwise suggest the answer to be Brightwater(which is wrong). I expect that question to be hard, so I set the target at 4 of 5.

---

## 2. Every answer names a source

Every answer the system produces names at least one source document.

**Why this target:**
<!-- Why all five and not four? What about your setup makes that achievable —
     or what would have to go wrong for it not to be? -->

Looking at the generate.py code, it is clear that the system instructs the model to include a source document in the answer. Therefore, I expect that all five answers will name at least one source document. I just dont think the retrieved source documents would be right or wrong( which is my criteria 5), but it will surely name at least one source document. The only way it would not name a source document is if the system fails to generate an answer due to the gate refusing the question, which is not expected to happen for the questions in scope.

---

## 3. The relevance gate stops out-of-corpus questions

When I ask a question my documents clearly don't cover, the relevance gate
stops it and the system returns "I don't have enough information about that" —
in at least 4 of 5 tries.

<!-- The five questions are the ones in `OUT_OF_SCOPE` at the bottom of
     `questions.py`, and `run_eval.py` puts them through the gate and writes
     what happened into your run log. Swap them for your own if you'd rather —
     just keep five of them, or the "4 of 5" above has nothing to be 4 of. -->

**Why this target:**
<!-- What did your distances look like when you set the cutoff in Milestone 4?
     Was there a clean gap, or did the two groups overlap? -->

I set this at 4 of 5 before measuring anything, expecting the two groups to
sit far apart. They did — but only because the starter's five out-of-corpus
questions (Mongolia, diesel engines, the World Cup, ibuprofen, Rust) all
scored between 0.853 and 0.903 against my corpus, while my own five clustered
at 0.287 to 0.372. That is a gap of 0.457, and any cutoff between 0.38 and
0.82 refuses all five, so the criterion could not be missed and my Milestone 4
cutoff would have been an arbitrary number in a canyon.

So I replaced three of them with travel questions about places none of my
fourteen documents mention: a fish market in Bergen (0.467), a coastal walk in
Cape Town (0.499), and the best months to visit Barcelona (0.513). The gap is
now 0.372 to 0.467 — about 0.095. Narrow, but the two groups still don't
overlap.

I am keeping 4 of 5 rather than raising it to 5 of 5 because that 0.095 was
measured against the baseline chunker, and Milestone 3 replaces it. Different
chunks mean different embeddings mean different distances, and a margin that
thin can close. The one question of slack is for a near miss drifting under
the line after I re-chunk.

Note: These distances were measured with the baseline chunker. Milestone 3 replaces it, so all ten will move and I will re-measure them then.
---

## 4. Something about your chunks

<!-- YOU WRITE THIS ONE.

     How would you know if your chunks were the right size? Name something
     countable or observable.

     Examples of the right shape — don't copy these, they should come from
     what you actually saw in Milestone 3:
       - "At least 4 of 5 sampled chunks read as a complete thought, with no
          sentence cut in half at either end."
       - "No chunk is shorter than 200 characters, since anything below that
          in my corpus turned out to be a heading with no content under it." -->
At least 80% of the chunks in my index begin at a `##` heading or the start of
a sentence and end on terminal punctuation, and every chunk contains at least
one complete sentence of body text rather than a heading alone.

**Why this target:**

The baseline chunker cuts on a character count and ignores where sentences
end, and the damage is measurable: of its 51 chunks, exactly 1 is clean at
both ends. 64% do not end at a sentence boundary and 68% do not start at one.
The clearest example is `guide_eating.md#3`, which is 24 characters long and
reads in full: "d Sundays and after 5pm." That is the tail of "Elder Ness has
one shop, closed Sundays and after 5pm" — the opening hours survived and the
shop they belong to did not, so the fact is no longer retrievable by anything
that asks about Elder Ness.

I set 80% rather than 100% because my documents are 1,441 to 2,513 characters
built from 84 `##` sections averaging about 285 characters, and splitting on
those sections leaves the 14 document titles as fragments of 23 to 27
characters with no body under them. Some remainder is structural, not a
chunking mistake. I did not set it lower than 80% because the baseline is
already at 2% — anything under about 70% would be a target I could clear
without changing the chunker at all.

---

## 5. Your choice

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. It could be about
     speed, about refusals, about a particular kind of question your corpus
     handles badly, about source attribution being correct rather than merely
     present — anything, as long as it names a number or an observable
     outcome. -->

For all 5 of my test questions, the source document named in the answer
actually contains the fact the answer states not merely a document that
mentions the same town.

**Why this target:**

9 of my 14 documents end with an identical "Practical notes" paragraph that
says "The nearest full hospital is in Brightwater." `guide_accessibility.md`
line 45 contradicts all nine: "The nearest full hospital is in Marchwood.
Brightwater has a hospital." My test question 4 asks exactly this, so one
correct chunk is competing with nine near-identical decoys, and an answer
that cites `guide_kestrelford.md` for a hospital fact would be well-sourced
and wrong.

That is why this is not already covered by criterion 2. Criterion 2 only asks
that a source is named, and a confident citation of the wrong file passes it.
I set this at 5 of 5 rather than 4 of 5 because a wrong citation is worse
than a missing one — a missing source is visibly incomplete, while a wrong
one looks checked.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 2 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 1. Retrieved chunks contain the answer

         For at least 4 of my 5 test questions, the retrieved chunks include
         one that contains the answer.

         **Why this target:** ...

         > **Revised in unit 2:** For at least 4 of 5 questions, the top three
         > results contain the answer.
         >
         > **Why revised:** I couldn't judge "the chunks include one that
         > contains the answer" the same way twice — I scored two questions
         > differently on Monday than on Wednesday. The new version is
         > something I can actually check.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said 4 of 5 but got 2 of 5, so 2 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.

     The whole reason the originals stay visible is so someone can see what you
     said before you knew the answer.
     ───────────────────────────────────────────────────────────────────────── -->
