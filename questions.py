"""
Your test questions.

Milestone 2 asks you to write five questions your system should be able to
answer from your corpus, specific enough to have a right answer.

  ✗ "What are good dining halls?"          — no right answer
  ✓ "What do students say about wait times at Commons during lunch?"

Fill in `QUESTIONS` below. `expects` is a word or short phrase you'd expect a
correct answer to contain — you'll use it in unit 2 when you build a scorer,
and having written it now means you decided what "correct" meant before you saw
any results.

`OUT_OF_SCOPE` holds five questions your documents clearly don't cover. You
need these in Milestone 4 to find where your relevance cutoff belongs, and
again in unit 2, where `run_eval.py` runs them through the gate and writes what
happened into your run log — that's the evidence for criterion 3.

Swap them for your own if you like. Keep five of them either way: criterion 3
names a target of "4 of 5", and four of three is not a thing.
"""

QUESTIONS = [
    {"question": "What are the best months to visit Brightwater?",
     "expects": "May and June"},
    {"question": "When do the parking lots in Halden Bay fill up on summer weekends?",
     "expects": "10am"},
    {"question": "How often does the access road to Elder Ness flood?",
     "expects": "six times a year"},
    {"question": "If I need a full hospital rather than a minor injuries unit, which town do I go to?",
     "expects": "Marchwood"},
    {"question": "What hours do the pubs in Kestrelford serve food?",
     "expects": "8:30"},
]

# Questions from a different world entirely. Your gate should refuse all five.
#
# There are five of these because criterion 3 in criteria.md names a target of
# "at least 4 of 5" — you need five things to try before you can report 4 of 5.
# `run_eval.py` runs these through retrieval and the gate on every eval and
# records what happened, so criterion 3 has evidence in the run log alongside
# the others. They cost no model calls: a refusal never reaches the model.
#
# Three of these are deliberately "near misses": travel questions about places
# that appear in none of my fourteen documents. The starter's original five
# were all far-field (Mongolia, diesel engines, the World Cup, ibuprofen,
# Rust) and every one of them scored 0.83-0.90 against my corpus, while my
# own questions scored 0.287-0.372. A gap that wide means any cutoff between
# 0.38 and 0.82 refuses all five, so criterion 3 could not be missed and the
# threshold choice in Milestone 4 would be arbitrary.
#
# Measured best distance for each, with the baseline chunker:
OUT_OF_SCOPE = [
    "What time does the fish market in Bergen open?",     # 0.467 — near miss
    "How long is the coastal walk around Cape Town?",     # 0.499 — near miss
    "What are the best months to visit Barcelona?",       # 0.513 — near miss,
                                                          #   mirrors my Q1
    "How do I write a for loop in Rust?",                 # 0.853 — far field
    "Who won the 1994 World Cup?",                        # 0.903 — far field
]

def answered() -> list[dict]:
    """The questions you've actually filled in."""
    return [q for q in QUESTIONS if q.get("question", "").strip()]
