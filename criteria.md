# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

**How I'll test these.** Every criterion holds in each of three trials, not on
average. Test text goes through `POST /submit` like any caller's would, and
"labelled" always means the `guess` in the response. The human set is 10 pieces
I wrote myself, at least 5 of them plain, short-sentence writing (the kind I
expect to be accused), and the AI set is 10 pieces generated from prompts.

---
## 1. False positives: no piece of my own writing is labelled high-confidence AI

Of 10 pieces I wrote myself, **0** come back as `guess: "ai"`, in each of three
trials. At least 5 of the 10 are plain, short-sentence writing.

**Why this target:** On a writing site a wrong accusation costs a real person a
lot and a missed detection costs the site a little, so I'd rather be too
cautious than right more often. I set it at zero rather than "at most 1"
because the plain-writing pieces are the ones my first signal is most likely to
get wrong (see DESIGN.md), and a target I can't miss on the people most at risk
wouldn't be testing anything. If it fails, plain writing landing in "unsure"
instead is the outcome I'm designing for.

---

## 2. Score spread: clearly-AI and clearly-human text are told apart

Across 5 clearly-AI and 5 clearly-human pieces, the mean `combined_score` of the
AI pieces is at least **0.30 higher** than the mean of the human pieces, and at
least **3 of the 5** clearly-AI pieces are labelled `"ai"`. No clearly-AI piece
is labelled `"human"`. All three hold in each of three trials.

**Why this target:** A service that gives everything the same score isn't
detecting anything, and criterion 1 alone could be met by that. The gap is
deliberately smaller than the full 0–1 range because the two signals are weak
and I expect overlap. "3 of 5" and not "5 of 5" because missing some AI text is
the cheap error and I'm trading it for criterion 1; but calling clearly-AI text
human would mean the signals are broken, so that count is zero.

---

## 3. Label coverage: all three labels are reachable, and "unsure" isn't a dumping ground

Using real submissions through `POST /submit`, each of `"human"`, `"unsure"` and
`"ai"` is produced at least once in each of three trials, and the `label` text
in the response matches the README wording exactly. Over the 20 pieces from
criteria 1 and 2 (10 human, 10 AI), at most **8** (40%) are labelled `"unsure"`.

**Why this target:** The starter warns that a label can be unreachable by
construction: a weighted average with a stub signal can never go below about
0.25. A label no input can produce is a gap in the design, and I'd rather find
out from a test than from a user. The cap on "unsure" is there because widening
that band is the easy way to hit criterion 1 and it would quietly turn the
service into one that never says anything.

---

## 4. The appeal path: an appeal always changes status and is always recorded

For 10 appeals on 10 real `content_id`s, **10 of 10** return 200 with
`status: "under_review"`, and **10 of 10** appear in `GET /log` as an
`appeal` event after their original decision, with the original entry
unchanged. For 5 appeals using an unknown `content_id`, **5 of 5** return 404
and none of them produces an `under_review` entry.

**Why this target:** The appeal is the only thing between a wrong accusation and
nothing at all, so it has no tolerance for failing quietly. That's why it's 10
of 10 and not 9 of 10. The unknown-id half is there because the likeliest bug is
a typo'd `content_id` that looks like success while recording nothing.

---

## 5. Bad input: nothing I send can crash the service

I send 10 malformed requests: a body that isn't JSON, a JSON body that is a
list, `text` missing, `text` empty, `text` only whitespace, `text` as a number,
`creator_id` missing, `text` of 19 words, `text` of 50,001 characters, and
`text` of 500,000 characters. **0** return a 5xx, **10 of 10** return the status
and `error` code documented in DESIGN.md, and **10 of 10** leave a `rejected`
entry in the log. `POST /ping` still answers afterwards.

**Why this target:** A crash on malformed input is one of the most common real
failures, and next unit's attack set will send all of this and more. A refusal
that leaves no trace looks like a quiet afternoon, so "logged" is part of the
target and not an extra. The `/ping` check separates "my handler is broken" from
"the service is down" if something goes wrong.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
