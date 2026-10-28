# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->



---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** How predictable gpt2 finds the text (perplexity), squashed
to 0–1. Higher means more AI-like. `detector.py::model_signal`, given.

**Why that might differ between human and AI writing:** A language model writes
by picking likely next words, so its output is text a model finds likely.
People pick odd words, turn abruptly, and name specific things.

**What it can't see:** Predictable is not the same as machine-written. It
rewards common words in short ordinary sentences, so plain human writing scores
as machine-like: my plain paragraph about walking a dog scored 0.874, against
0.898 for a paragraph of AI-style prose. It also reads only the first 400
tokens, and ornate prose full of rare words reads as human.

### Signal two — the style signal

**What it measures:** The shape of the text, three measures combined into 0–1
(higher means more AI-like). `stylometry.py::style_signal`.

| Measure | What it is | Counts as AI-like when | Weight |
|---|---|---|---|
| Sentence-length spread | stdev / mean of words per sentence | below 0.20 → 1.0, above 0.70 → 0.0 | 0.5 |
| Type-token ratio | unique / total words, averaged over 50-word windows so length doesn't masquerade as signal | below 0.65 → 1.0, above 0.90 → 0.0 | 0.2 |
| Distinctive punctuation | `; : ( ) " ! ? … —` per 100 words (commas and full stops left out on purpose) | 0 → 1.0, 4 or more → 0.0 | 0.3 |

A one-sentence text has no spread, so that measure is dropped and the other two
are re-weighted instead of treating "no evidence" as "machine-like".

**Why that might differ between human and AI writing:** Repeating "most likely
next word" tends to produce even, mid-length sentences and a narrow vocabulary.
Human writing is lumpier: a three-word sentence next to a forty-word one.

**What it can't see:** Anything about meaning. It reads shape only, so it is
moved by anything that changes shape without changing substance: typos,
chopped or joined sentences, a pasted quotation. It also shares signal one's
blind spot on plain writing: that same dog paragraph scored 0.944, the most
AI-like of anything I tried, because its sentences are even and it uses no
distinctive punctuation. And it reads uniform formal prose as AI (below).

**These bounds were set by eye, from seven inputs I wrote myself.** They are a
starting point, not a calibration.

### The combining rule

**The rule:** Average the two signals with equal weight. If they are more than
0.35 apart, cap the result at 0.60. The cap only lowers a score, and it sits
inside the unsure band, so a split between the signals can produce "unsure"
but never "high-confidence AI". Nothing mirrors it on the human side: wrongly
clearing AI text is the cheap error and wrongly accusing a writer is the
expensive one, so a disagreement never pushes a score toward AI.

**The numbers:** `WEIGHT_MODEL_SIGNAL = 0.5`, `WEIGHT_STYLE_SIGNAL = 0.5`,
`SPLIT_GAP = 0.35`, `SPLIT_CAP = 0.60`, all in `config.py`. Equal weights
because I have no evidence yet that either signal deserves more trust.

**Where it lives:** `scoring.py::combine_signals`

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**The calibration run.** `python calibration.py` runs both signals on seven
inputs I wrote as stand-ins (`calibration.py`). Scores are 0–1, higher = more
AI:

| Input | model | style | combined |
|---|---|---|---|
| clear_ai | 0.898 | 0.904 | 0.901 |
| clear_human | 0.219 | 0.132 | 0.175 |
| plain_human | 0.874 | 0.944 | 0.909 |
| formal_human | 0.382 | 0.151 | 0.266 |
| edited_ai | 0.526 | 0.348 | 0.437 |
| even_formal | 0.156 | 0.880 | 0.518 |
| varied_ai | 0.466 | 0.033 | 0.250 |

Clearly-AI and clearly-human text land 0.73 apart (0.901 and 0.175), and
formal human prose lands low at 0.266, so the signals do separate the easy
cases. Two rows are bad:

- **plain_human scores 0.909, slightly above clear_ai at 0.901.** Both signals
  agree, so no combining rule can fix it. Under any threshold that labels
  clear_ai as AI, this paragraph a person wrote is labelled AI too. At the
  moment I can't meet criterion 1 (no false positives) with these two signals.
- **edited_ai scores 0.437 and varied_ai scores 0.250.** The edited AI text
  drifts toward the middle, and the AI-written text with varied sentences and
  distinctive punctuation looks human to the style signal. Both are the cheap
  error for the site, but they're the evasions unit 8 will probe.

**A case where my two signals split, and what my rule does with it:**
`even_formal`, a paragraph in a formal, old-fashioned register with six
sentences of almost equal length. Signal one reads it as human (0.156, rare
words that gpt2 can't predict) while signal two reads it as AI (0.880, uniform
sentence lengths and no distinctive punctuation), a gap of 0.72. The average is
0.518, which is already below the 0.60 cap, so the cap does nothing here and the
result is a plain 0.518: "unsure", the honest outcome when two methods disagree
this much. **No input I tried actually triggers the cap.** It only fires when
the average is above 0.60 with a gap over 0.35 (for example 0.95 and 0.55, which
the function turns into 0.60), and I checked that by calling the function
directly rather than from real text. I kept it because it states the policy
(a split can't accuse), but it is unproven on real data.


---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human |  |  |
| unsure |  |  |
| high-confidence AI |  |  |

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

*Milestone 3 state: one signal wired in. `guess`, `confidence` and `label` are
placeholders, and `style_score` is `null` until Milestone 4. Run on port 5055
because another `app.py` was already on 5000.*

A plain paragraph I wrote about a walk with my dog:

```bash
$ curl -X POST http://127.0.0.1:5055/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the park with my dog on Saturday. The weather was nice and the sun was out. We walked for about an hour and then sat on a bench. My dog likes to chase the ducks by the pond. After that we went home and I made lunch. It was a good day and I was happy.", "creator_id": "demo-human"}'
```

```json
{
  "confidence": 0.5,
  "content_id": "b2264830-1ede-4f86-815e-a5975fcccf8e",
  "guess": "unsure",
  "label": "PLACEHOLDER — not scored yet.",
  "model_score": 0.8743,
  "status": "decided",
  "style_score": null
}
```

That `model_score` of 0.8743 is on a paragraph a person wrote. Signal one alone
scores plain writing as machine-like, which is the blind spot DESIGN.md names.
A machine-sounding paragraph ("The implementation of the proposed framework
requires careful consideration of several key factors…") scored 0.8864 through
the same route, so the two are barely separated.

Bad input is refused and logged rather than crashing:

```bash
$ curl -X POST http://127.0.0.1:5055/submit -H "Content-Type: application/json" -d '{"text": "too short", "creator_id": "demo"}'
```

```json
{"error":"text_too_short","message":"text needs at least 20 words to be read."}
```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5055/log?limit=5"
```

```json
{
  "count": 5,
  "entries": [
    {
      "combined_score": null,
      "content_id": "1648283c-2fae-4415-a03f-debdf7d89c43",
      "creator_id": "demo-ai",
      "guess": "unsure",
      "label": "PLACEHOLDER — not scored yet.",
      "model_score": 0.8864,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-10-28T22:32:25+00:00"
    },
    {
      "combined_score": null,
      "content_id": "b2264830-1ede-4f86-815e-a5975fcccf8e",
      "creator_id": "demo-human",
      "guess": "unsure",
      "label": "PLACEHOLDER — not scored yet.",
      "model_score": 0.8743,
      "status": "decided",
      "style_score": null,
      "timestamp": "2026-10-28T22:32:26+00:00"
    },
    {
      "creator_id": "demo",
      "event": "rejected",
      "reason": "text_too_short",
      "status": "rejected",
      "timestamp": "2026-10-28T22:32:26+00:00"
    },
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "invalid_request",
      "status": "rejected",
      "timestamp": "2026-10-28T22:32:26+00:00"
    },
    {
      "creator_id": "unknown",
      "event": "rejected",
      "reason": "invalid_request",
      "status": "rejected",
      "timestamp": "2026-10-28T22:32:26+00:00"
    }
  ]
}
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
