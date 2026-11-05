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

Provenance Guard is a small web service that reads a piece of writing and says
how likely it is that a person wrote it, in words a writer can understand, with
a way to appeal if it's wrong. It never says *who* wrote something. It gives a
guess from two weak signals and admits when it isn't sure.

The path a submission takes, from `POST /submit` to the label a reader sees
(the full reasoning is in [DESIGN.md](DESIGN.md)):

1. **The gate** (`app.py::submit`). The request must be a JSON object with a
   `text` of at least 20 words and at most 50,000 characters and a non-empty
   `creator_id`. Anything else is refused with a 400, 413 or 422 and written to
   the log as a rejection, so a refusal still leaves a trace.
2. **An id.** The submission gets a `content_id` (a uuid). It's the only handle
   `/appeal` has, so it's made before any scoring.
3. **Signal one, the model signal** (`detector.py::model_signal`). gpt2 runs on
   this machine and measures how predictable the text is. Output: `model_score`,
   0–1, higher = more AI-like.
4. **Signal two, the style signal** (`stylometry.py::style_signal`). Measures
   the shape of the text: sentence-length spread, vocabulary repetition and
   distinctive punctuation. Output: `style_score`, 0–1, same direction.
5. **The combining rule** (`scoring.py::combine_signals`). An equal-weight
   average of the two scores, capped at 0.60 if they disagree by more than
   0.35. Output: `combined_score`.
6. **The label** (`scoring.py::score_to_label`). Turns the combined score into
   a `guess` (`human`, `unsure` or `ai`) and a plain-language sentence. At or
   below 0.35 is human, at or above 0.75 is AI, and in between is unsure.
7. **The record and the reply** (`audit.py::log_decision`). One entry goes to
   `logs/audit.jsonl` with the timestamp, ids, both signal scores, the combined
   score, the guess, the label and a status. The response carries the same
   things back to the caller.

An appeal is a shorter path. `POST /appeal` takes the `content_id` and the
writer's reasoning, checks the decision exists, appends an `appeal` entry to the
log with status `under_review`, and confirms. It re-scores nothing and the
original decision is left in the log untouched.

**What it can't do yet.** Plain, short-sentence writing is read as AI by *both*
signals, so a person who writes that way can get the high-confidence AI label
(see the Sample Run, where one does). The label says so and points to the
appeal, but the underlying problem is the signals, not the wording.


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
| high-confidence human | 0.00 – 0.35 | We think this was probably written by a person. |
| unsure | 0.35 – 0.75 | We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look. |
| high-confidence AI | 0.75 – 1.00 | This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning. |

The ranges come from `config.py` (`HUMAN_THRESHOLD = 0.35`, `AI_THRESHOLD =
0.75`) and are printed by `scoring.label_ranges()`. The text is in
`scoring.py` (`LABEL_HUMAN`, `LABEL_UNSURE`, `LABEL_AI`). I raised
`AI_THRESHOLD` from the starter's 0.65 because accusing a real writer costs far
more than missing some AI text.

**All three are reachable.** Submitting the calibration inputs through
`POST /submit` gave `clear_human` → human (0.1754), `even_formal` → unsure
(0.5182) and `clear_ai` → ai (0.9009).

**Why I worded the "unsure" one this way:** It's the label a real writer is
most likely to read, so it opens with what we *don't* know, not with what we
suspect. It says "that isn't a judgement against you" before explaining why,
and the reason it gives is about our checks, which look at the shape of the
writing, not about the person. It never says "AI-generated" or "flagged".
"You can ask for a person to take a look" gives the reader something to do
rather than something to absorb. The high-confidence AI label follows the same
rules (it says "may have been", admits "we get this wrong", and names plain
short-sentence writing as the case it gets wrong most), because with my current
signals a person who wrote every word can still land there. That is not a
hypothetical: see the sample run below.



---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

*Run on port 5055 because another `app.py` was already on 5000. The text is a
plain paragraph I wrote about a walk with my dog, the kind of writing the
design says gets wrongly accused. The command below shows the body inline; I
actually sent it with `-d @plain_human.json`, a file generated from
`calibration.py`'s `plain_human` input, to avoid shell-quoting mistakes. The
text is identical.*

```bash
$ curl -X POST http://127.0.0.1:5055/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "I went to the park with my dog on Saturday. The weather was nice and the sun was out. We walked for about an hour and then sat on a bench. My dog likes to chase the ducks by the pond. After that we went home and I made lunch. It was a good day and I was happy.", "creator_id": "demo-plain_human"}'
```

```json
{
    "appeal": "POST /appeal with this content_id",
    "combined_score": 0.9091,
    "confidence": 0.9091,
    "content_id": "1d8bb36e-e070-4854-8b1c-2dd488c6b2a0",
    "guess": "ai",
    "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.",
    "model_score": 0.8743,
    "status": "decided",
    "style_score": 0.944
}
```

**This is a false positive, on purpose.** A person wrote that paragraph and the
service called it high-confidence AI, because both signals read short plain
sentences as machine-like. It is the case DESIGN.md predicted, and I kept it as
the sample so the appeal has something real to do.

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5055/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "1d8bb36e-e070-4854-8b1c-2dd488c6b2a0", "reasoning": "I wrote this myself, about a walk with my dog last weekend. English is my second language, so I keep my sentences short."}'
```

```json
{
    "content_id": "1d8bb36e-e070-4854-8b1c-2dd488c6b2a0",
    "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
    "status": "under_review"
}
```

An appeal with an id that doesn't exist is refused (404, `unknown_content_id`)
and logged, and one with empty reasoning gets a 400. Neither changes any status.

**What the log shows afterwards**

The log is append-only, so the original decision is unchanged and the appeal sits
after it. Both entries for that `content_id`, from
`curl http://127.0.0.1:5055/log` filtered to it:

```json
{
  "count": 2,
  "entries": [
    {
      "combined_score": 0.9091,
      "content_id": "1d8bb36e-e070-4854-8b1c-2dd488c6b2a0",
      "creator_id": "demo-plain_human",
      "guess": "ai",
      "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.",
      "model_score": 0.8743,
      "status": "decided",
      "style_score": 0.944,
      "timestamp": "2026-10-28T22:40:14+00:00"
    },
    {
      "content_id": "1d8bb36e-e070-4854-8b1c-2dd488c6b2a0",
      "creator_id": "demo-plain_human",
      "event": "appeal",
      "reasoning": "I wrote this myself, about a walk with my dog last weekend. English is my second language, so I keep my sentences short.",
      "status": "under_review",
      "timestamp": "2026-10-28T22:40:14+00:00"
    }
  ]
}
```

The `status` on the original entry still says `decided`, and the appeal entry
carries `under_review`. The item's current status is the status of its latest
entry. The appeal only records. It doesn't re-score or change the label the
writer was shown.

---

## How I Used AI

**Moment 1: the second signal and the combining rule**

- *What I asked for:* A style signal built from sentence-length spread,
  vocabulary variety and punctuation, and a rule for combining it with the
  model signal that wouldn't undo my Milestone 1 decision that wrongly accusing
  a writer is the expensive mistake.
- *What came back:* Working code for both, including a rule that caps the
  combined score at 0.60 when the two signals disagree by more than 0.35. Two
  problems showed up when I ran it. First, on my five calibration inputs the
  signals agreed everywhere, so there was no case where the disagreement rule
  could fire, and the cap I'd been handed was untested. Second, the style
  signal's scaling bounds had been picked while looking at those same five
  inputs, so it fit them by construction. It also ranked a lightly-edited AI
  paragraph as the *most* varied text in the set on vocabulary.
- *What I changed:* I added two inputs on purpose to find a real split
  (`even_formal`, where the model says human and style says AI, and
  `varied_ai`, the reverse). The cap still never fires on real text, so the
  README says it's checked only by calling the function directly. I gave
  type-token ratio the smallest weight (0.2) because of the edited-AI result,
  and the README says outright that the bounds were set by eye from seven
  inputs I wrote myself.

**Moment 2: checking what the AI told me it had pasted**

- *What I asked for:* A real sample run for the README: a submission, an
  appeal, and the log entries.
- *What came back:* Output that was correct in substance but not exactly what
  the server had returned. The first test I ran with a hand-typed request body
  had lost an apostrophe to shell quoting, so its `model_score` was 0.1288
  instead of the 0.156 from the calibration table, and the response I was about
  to paste had a field filled in from the log rather than copied from the
  server.
- *What I changed:* I had the request bodies generated straight from
  `calibration.py` and sent with `curl -d @file`, so the text under test is the
  text in the repo. I threw out the reconstructed response, ran the submit,
  the appeal and the log read-back again in one go, and pasted that output.
  Separately, one of the AI's test commands would have killed every Python
  process on the machine to restart the server; the tool refused it, and I
  switched to running my own test server on a different port and stopping
  only that one.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** 5 per minute, 60 per day, on `POST /submit` only
(`config.py::RATE_LIMIT_PER_MINUTE` and `RATE_LIMIT_PER_DAY`).

**Why those numbers and not others:** A real writer revising a piece
resubmits at most once a minute or so, because each edit takes longer than a
scoring run, so 5 a minute is well above anything an honest person does and 60
a day is a heavy working day. Each submission also costs about a second of
model time on this machine, so the limit protects the service as well as the
thresholds. I'm honest that it is not very hostile to a script that wants to
map my thresholds: finding the score boundary of one text by repeatedly editing
it takes a few dozen probes, and 60 a day is enough for that. What it does is
make a *flood* expensive, not a patient probe, and it can't stop a script that
changes its `creator_id` (below).

**What a caller counts as:** A `creator_id`, falling back to the caller's
address only when the request has no usable `creator_id`
(`app.py::rate_limit_key`). I kept that, rather than limiting by address,
because on my laptop every caller is `127.0.0.1`, so a per-address limit would
trip on the unit's own attack set and evaluation runs, which each use a fresh
`creator_id` per item. The cost is real and I saw it in the run below: the
three later submissions came from the same address as the flood and were not
limited at all, because they used different `creator_id`s. **One script
rotating through `creator_id`s looks like a crowd of separate people and is
never limited.** An address-based limit would catch that and wrongly lump a
shared household or school together. Neither is right; this one is easier to
test and weaker against an attacker.

**The run of status codes when I pushed past it:**

`python run_attacks.py --flood 15 --url http://127.0.0.1:5055` (one
`creator_id`, fifteen submissions in a burst). The first five went through and
the next ten were refused. Saved as
[results/flood_2026-11-02_1936.md](results/flood_2026-11-02_1936.md):

```
200 200 200 200 200 429 429 429 429 429 429 429 429 429 429
```

**The refusals are in the log.** After the flood, `GET /log` held all ten
rejections beside the five decisions, so the burst is visible and not just an
absence:

```json
{
  "creator_id": "flood_tester",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-03T00:36:18+00:00"
}
```

A request my own route refuses is logged the same way. A submission with no
`text` produced:

```json
{
  "creator_id": "demo-bad",
  "event": "rejected",
  "reason": "invalid_request",
  "status": "rejected",
  "timestamp": "2026-11-03T00:36:26+00:00"
}
```

Across that session the log gained 19 entries: 8 decisions (5 from the flood
and 3 more submissions), 10 `rate_limited` and 1 `invalid_request`.

**Could someone reconstruct a decision from one entry without my code?**
Mostly. A decision entry has all nine fields: timestamp, `content_id`,
`creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `label`
and `status`. From those a reader can see both signals, the number they
produced and the sentence the writer got, and check that the label matches the
score. Three things are *not* in it: the text that was scored (nothing links an
entry to its input except the `content_id` in the response), the thresholds and
weights in force at the time (if I change `config.py`, old entries can no
longer be explained by the new numbers), and whether the 0.60 split cap fired.
I left the entry shape alone because unit 8 compares runs from before and after
my change, and a different shape would make them incomparable.

---

## Attack Run — Before

Run on port 5055 with rate limiting on (5 a minute, 60 a day), the service as
it stood at the end of unit 7 plus the limiter. Nothing was changed before or
during the run. Produced by `python run_attacks.py --set attack_set --label
before --url http://127.0.0.1:5055`; the full report, with every response, is
[results/attack_run_2026-11-04_1912_before.md](results/attack_run_2026-11-04_1912_before.md),
and the log entries for the run are in
[results/audit_extract.json](results/audit_extract.json).

**56 attacks: 48 HELD, 8 BROKE.** No crashes and no 5xx. Each of the 56
requests left exactly one entry in the audit log (22 decisions and 34
rejections).

| Family | Attacks | HELD | BROKE |
|---|---|---|---|
| evasion (AI text trying to pass) | 10 | 7 | 3 |
| false_positive (real human writing) | 8 | 4 | 4 |
| prompt_injection | 6 | 5 | 1 |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |

**How I marked them.** Evasion: BROKE if the AI text got a `human` label.
False positive: BROKE if a person's writing was labelled `ai`. Injection: BROKE
if the label the attacker asked for came back. Malformed and flood: BROKE on a
crash, a 5xx, or a refusal with no log entry. The "Combined" column is the
`combined_score` from the audit log, which is the number the label is made
from. (`run_attacks.py` prints `confidence` as its "Score", which is
`max(combined, 1 - combined)` and not the same thing.)

| ID | Family | What it was going for | Status | Guess | Combined | Mark |
|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | unsure | 0.482 | **HELD** |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | human | 0.324 | **BROKE** |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | unsure | 0.470 | **HELD** |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | unsure | 0.706 | **HELD** |
| EV05 | evasion | both signals: heavy human editing pass | 200 | human | 0.297 | **BROKE** |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | unsure | 0.454 | **HELD** |
| EV07 | evasion | signal two: padding with punctuation | 200 | human | 0.344 | **BROKE** |
| EV08 | evasion | signal one: text below the token window | 422 | — | — | **HELD** |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | unsure | 0.618 | **HELD** |
| EV10 | evasion | signal two: repeated stanza structure | 200 | ai | 0.893 | **HELD** |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | unsure | 0.617 | **HELD** |
| FP02 | false_positive | human writing in a formal register | 200 | ai | 0.805 | **BROKE** |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | ai | 0.772 | **BROKE** |
| FP04 | false_positive | a student essay written to a rubric | 200 | ai | 0.773 | **BROKE** |
| FP05 | false_positive | technical documentation written by a person | 200 | ai | 0.862 | **BROKE** |
| FP06 | false_positive | a person imitating a formal template | 200 | unsure | 0.737 | **HELD** |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | unsure | 0.600 | **HELD** |
| FP08 | false_positive | very short genuine human submission | 422 | — | — | **HELD** |
| PI01 | prompt_injection | instruction to ignore the check | 200 | unsure | 0.400 | **HELD** |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | human | 0.193 | **BROKE** |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | unsure | 0.476 | **HELD** |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | unsure | 0.420 | **HELD** |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | unsure | 0.434 | **HELD** |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.592 | **HELD** |
| MF01 | malformed | text is only whitespace | 400 | — | — | **HELD** |
| MF02 | malformed | text is a single character | 422 | — | — | **HELD** |
| MF03 | malformed | text is control characters | 422 | — | — | **HELD** |
| MF04 | malformed | text is only punctuation | 422 | — | — | **HELD** |
| MF05 | malformed | text is a very long single word | 422 | — | — | **HELD** |
| MF06 | malformed | text is emoji only | 422 | — | — | **HELD** |
| MF07 | malformed | text is right-to-left script | 422 | — | — | **HELD** |
| MF08 | malformed | text is 60,000 characters | 413 | — | — | **HELD** |
| RQ01 | malformed | no text field at all | 400 | — | — | **HELD** |
| RQ02 | malformed | no creator_id | 400 | — | — | **HELD** |
| RQ03 | malformed | text is a number | 400 | — | — | **HELD** |
| RQ04 | malformed | text is a list | 400 | — | — | **HELD** |
| RQ05 | malformed | text is null | 400 | — | — | **HELD** |
| RQ06 | malformed | creator_id is an object | 400 | — | — | **HELD** |
| RQ07 | malformed | body is a JSON array, not an object | 400 | — | — | **HELD** |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | **HELD** |
| RQ09 | malformed | body is empty | 400 | — | — | **HELD** |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | — | — | **HELD** |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | — | — | **HELD** |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | **HELD** |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | **HELD** |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | **HELD** |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | **HELD** |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | **HELD** |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | — | — | **HELD** |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | — | — | **HELD** |

**What the table does not say.**

- **Most of the 7 evasion "holds" are weak.** Only EV10 was *caught* as AI.
  EV08 was refused for being too short, and five (EV01, EV03, EV04, EV06, EV09)
  came back `unsure`, so nothing flagged them, but nothing cleared them either.
  Counting only attacks that got the AI label, the service caught 1 of 9 AI
  texts it scored.
- **Three of the four false-positive holds are lucky or hollow.** FP08 was held
  only because a genuine short text was refused with a 422 and never judged. FP06
  scored 0.737, 0.013 under the 0.75 line that would have called it AI. FP07
  is the first time the 0.60 split cap fired on real text (model 0.8816, style
  0.5), but the average, 0.691, was already `unsure`, so the cap changed
  nothing.
- **RQ10 and RQ11 first came back 429 and never reached my route.** Requests
  with no usable `creator_id` all count against one shared address bucket, and
  five earlier rows had already filled it. I re-sent each alone after the window
  cleared (`results/attack_run_*_before-rerun-*.md`) and both got a 400 from the
  route, so both are marked HELD on that evidence.
- **The flood rows were refused for length before they were ever scored.** The
  first five FL01 rows came back 422 (the flood text is under 20 words), which
  still counts toward the limit; rows 6 to 12 came back 429. The limiter held,
  but this run didn't test the limiter against text the service would score.
- **The injection rows never worked as injections.** My service doesn't read
  instructions; the only place text can matter is the two signals. PI02 still
  got a `human` label at confidence 0.807 (model 0.2044, style 0.1815) on
  what is otherwise generic corporate prose with a fake `SYSTEM:` line in front,
  so something about that prefix moved both scores. That's for the diagnosis.
  PI05 tried to forge a log entry through the text. It failed because the text
  is never written to the log, and `json.dumps` escapes anything that is.

**Ten audit log entries from the run**

Chosen for the failures, not the easy cases: three AI texts that got a `human`
label (EV02, EV07, PI02), one where the signals split hard (EV01: model 0.1635,
style 0.8), four people's writing at or near the AI line (FP03, FP05, FP06,
FP07), and two rejections. The first rejection is a 429 from the
`flood_same_creator` rows. The second is a 429 for a request with no
`creator_id`, which the log can only record as `unknown` and which never
reached the route. Rejection entries carry fewer fields than decisions.

```json
{
  "combined_score": 0.3235,
  "content_id": "369d3157-01ef-401c-8098-8bf4622542cf",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5943,
  "status": "decided",
  "style_score": 0.0527,
  "timestamp": "2026-11-05T00:12:12+00:00"
},
{
  "combined_score": 0.3443,
  "content_id": "e73fda08-6b79-454a-9a48-db2e6b22337a",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.5862,
  "status": "decided",
  "style_score": 0.1024,
  "timestamp": "2026-11-05T00:12:13+00:00"
},
{
  "combined_score": 0.193,
  "content_id": "25f7c72d-3939-4019-90b2-3e7d2349a47a",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "label": "We think this was probably written by a person.",
  "model_score": 0.2044,
  "status": "decided",
  "style_score": 0.1815,
  "timestamp": "2026-11-05T00:12:16+00:00"
},
{
  "combined_score": 0.4818,
  "content_id": "f331454f-4442-4a46-b4a8-c777980c4fbf",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "model_score": 0.1635,
  "status": "decided",
  "style_score": 0.8,
  "timestamp": "2026-11-05T00:12:12+00:00"
},
{
  "combined_score": 0.7725,
  "content_id": "c8887639-277a-4e84-a826-e5c905cbdc36",
  "creator_id": "attacker_FP03",
  "guess": "ai",
  "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.",
  "model_score": 0.8051,
  "status": "decided",
  "style_score": 0.7398,
  "timestamp": "2026-11-05T00:12:14+00:00"
},
{
  "combined_score": 0.8618,
  "content_id": "29641be4-0691-43bc-ae17-ea2b4e7371d6",
  "creator_id": "attacker_FP05",
  "guess": "ai",
  "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.",
  "model_score": 0.8005,
  "status": "decided",
  "style_score": 0.9231,
  "timestamp": "2026-11-05T00:12:15+00:00"
},
{
  "combined_score": 0.7371,
  "content_id": "55b24520-14ae-49f2-a017-8676ac168be5",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "model_score": 0.8814,
  "status": "decided",
  "style_score": 0.5928,
  "timestamp": "2026-11-05T00:12:15+00:00"
},
{
  "combined_score": 0.6,
  "content_id": "a942a9f2-ae9c-41db-942a-266e46a66485",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "model_score": 0.8816,
  "status": "decided",
  "style_score": 0.5,
  "timestamp": "2026-11-05T00:12:15+00:00"
},
{
  "creator_id": "attacker_flood",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-05T00:12:17+00:00"
},
{
  "creator_id": "unknown",
  "event": "rejected",
  "limit": "5 per 1 minute",
  "reason": "rate_limited",
  "status": "rejected",
  "timestamp": "2026-11-05T00:12:17+00:00"
}
```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP03, "a non-native English speaker writing carefully": labelled
high-confidence AI, combined 0.7725.** Model 0.8051, style 0.7398, content id
`c8887639-277a-4e84-a826-e5c905cbdc36`. The person did the right thing, writing
slowly and carefully in a second language, and my two signals read exactly that
care as machine-made: common words in tidy, even sentences. Both signals
agreed, so the disagreement rule had nothing to catch. The label tells them it
"looks like it may have been written with an AI tool", and the one hint it
gives, that it's wrong "especially with plain, short-sentence writing", doesn't
describe what they wrote. They can appeal, but the appeal only records a
reason; the label stays up until a person decides to read it, and I haven't built
anything that does. FP05 (technical documentation, 0.862) scored higher, but a
person writing documentation can say what they are. A person writing in their
second language has the least room to argue back, and that is who the design
said would pay.

---

## Run Log and Verdicts

This is the service as it stood after the attack run, with nothing changed
since. Run on port 5055, rate limiting on. `python run_eval.py --label before`
sent criteria 1, 2 and 3 three times
([results/run_2026-11-04_1919_before.md](results/run_2026-11-04_1919_before.md)),
then `python eval_checks.py --label before` ran criteria 4 and 5 live three times
and judged all five ([results/verdicts_before.md](results/verdicts_before.md)).

**What I added to the starter tooling.** `scenarios.py` holds criteria 1 to 3.
Criteria 4 and 5 can't be written there: an appeal needs a content_id from an
earlier submission and a look at the log afterwards, and two of my bad-input
cases (a JSON list, a body that isn't JSON) aren't dict bodies. They are in
`eval_checks.py`, which also writes the verdicts because `run_eval.py` leaves
that column blank. I also added one field, `combined_score`, to what
`run_eval.py` records, because criterion 2's 0.30 gap is measured on it.

**⚠️ The writing in criteria 1 and 2 is not a person's.** I don't have ten
pieces of my own writing in the repo, so the ten in `scenarios.py::MY_WRITING`
and the five "clear human" pieces are stand-ins Claude wrote, imitating plain
and distinctive writers. The five clear-AI pieces really are AI-generated. So
**the verdicts on criteria 1 and 2 describe how the service treats imitations of
human writing, not mine.** The honest next step is to paste real pieces into
`MY_WRITING` and `HUMAN_CLEAR` and re-run before any fix is made, so the "before"
is real. Criteria 3, 4 and 5 don't depend on who wrote the text.

**The three trials were identical.** Every score, label and count matched across
all three, as expected: nothing in either signal is random. Nothing in the
pipeline is unstable.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled AI | 0 of 10 | 4/10 | 4/10 | 4/10 | **MISSED** |
| 2. Clearly-AI and clearly-human text told apart | gap ≥ 0.30, ≥ 3/5 AI labelled ai, 0 labelled human | gap 0.33, 3/5 ai, 0 human | gap 0.33, 3/5 ai, 0 human | gap 0.33, 3/5 ai, 0 human | **MET** |
| 3. All three labels reachable; unsure not a dumping ground | 3 of 3 labels, ≤ 8 of 20 unsure | 3/3 labels, 9/20 unsure | 3/3 labels, 9/20 unsure | 3/3 labels, 9/20 unsure | **MISSED** |
| 4. Appeal always changes status and is recorded | 10/10 real + 5/5 unknown | 10/10 + 5/5 | 10/10 + 5/5 | 10/10 + 5/5 | **MET** |
| 5. Bad input never crashes and is always logged | 10/10, 0 5xx, ping ok | 10/10 | 10/10 | 10/10 | **MET** |

**Real output from one trial**, pasted as text, naming the file and function
that produced it. Each is trial 1; the full file is `results/verdicts_before.md`.

**1.** Produced by `run_eval.py::main` (scenario "own writing"), trial 1:

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.8687, "model_score": 0.8174, "style_score": 0.92, "combined_score": 0.8687, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "Yesterday I went to the store near my house. I needed milk and eggs an"},
  {"status": 200, "guess": "ai", "confidence": 0.8007, "model_score": 0.7497, "style_score": 0.8516, "combined_score": 0.8007, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "My brother is learning to drive. He practices in the parking lot every"},
  {"status": 200, "guess": "ai", "confidence": 0.8053, "model_score": 0.8099, "style_score": 0.8007, "combined_score": 0.8053, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "I like my new job. The people are friendly and the work is not too har"},
  {"status": 200, "guess": "ai", "confidence": 0.8994, "model_score": 0.818, "style_score": 0.9809, "combined_score": 0.8994, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "The bus was late again this morning. I stood at the stop for twenty mi"},
  {"status": 200, "guess": "unsure", "confidence": 0.7444, "model_score": 0.6999, "style_score": 0.7889, "combined_score": 0.7444, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "We cleaned the garage on Saturday. It took all day because there was s"},
  {"status": 200, "guess": "human", "confidence": 0.8544, "model_score": 0.2582, "style_score": 0.033, "combined_score": 0.1456, "label": "We think this was probably written by a person.", "sent": "Three weeks into the allotment and I've learned one thing: slugs don't"},
  {"status": 200, "guess": "unsure", "confidence": 0.6345, "model_score": 0.399, "style_score": 0.332, "combined_score": 0.3655, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "My grandmother never wrote a recipe down. You watched. You got a slap "},
  {"status": 200, "guess": "human", "confidence": 0.8526, "model_score": 0.2606, "style_score": 0.0343, "combined_score": 0.1474, "label": "We think this was probably written by a person.", "sent": "I failed my driving test twice, which my sister will never let me forg"},
  {"status": 200, "guess": "human", "confidence": 0.7293, "model_score": 0.3448, "style_score": 0.1966, "combined_score": 0.2707, "label": "We think this was probably written by a person.", "sent": "Not sure why I'm writing this at 2am. The fridge hums. Something about"},
  {"status": 200, "guess": "unsure", "confidence": 0.5735, "model_score": 0.5881, "style_score": 0.2649, "combined_score": 0.4265, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "There's a crack in the pavement outside my building shaped like Florid"}
]
```

Four pieces came back `ai` (combined 0.869, 0.801, 0.805, 0.899): the first four
of the five plain, short-sentence pieces. The fifth, at 0.744, missed the 0.75
line by 0.006.

**2.** Produced by `run_eval.py::main` (scenario "clear AI"), trial 1:

```json
[
  {"status": 200, "guess": "ai", "confidence": 0.8193, "model_score": 0.8225, "style_score": 0.816, "combined_score": 0.8193, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "Effective time management is a critical skill that can significantly i"},
  {"status": 200, "guess": "ai", "confidence": 0.8288, "model_score": 0.9281, "style_score": 0.7294, "combined_score": 0.8288, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "Climate change represents one of the most pressing challenges facing h"},
  {"status": 200, "guess": "ai", "confidence": 0.7653, "model_score": 0.8327, "style_score": 0.698, "combined_score": 0.7653, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "In today's rapidly evolving digital landscape, cybersecurity has becom"},
  {"status": 200, "guess": "unsure", "confidence": 0.6, "model_score": 0.8753, "style_score": 0.5045, "combined_score": 0.6, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "Regular physical exercise offers numerous benefits for overall health "},
  {"status": 200, "guess": "unsure", "confidence": 0.7281, "model_score": 0.7013, "style_score": 0.7549, "combined_score": 0.7281, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "Reading is a valuable habit that provides many advantages for personal"}
]
```

**2 (continued).** Produced by `run_eval.py::main` (scenario "clear human"), trial 1:

```json
[
  {"status": 200, "guess": "human", "confidence": 0.7081, "model_score": 0.3882, "style_score": 0.1956, "combined_score": 0.2919, "label": "We think this was probably written by a person.", "sent": "Dad's truck smelled like wet dog and peppermints. Every Saturday, same"},
  {"status": 200, "guess": "unsure", "confidence": 0.6493, "model_score": 0.4308, "style_score": 0.2705, "combined_score": 0.3507, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "The thing nobody tells you about moving abroad is the small stuff. Not"},
  {"status": 200, "guess": "unsure", "confidence": 0.6184, "model_score": 0.3832, "style_score": 0.38, "combined_score": 0.3816, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "Lena says I overthink everything and she's right, obviously, but try t"},
  {"status": 200, "guess": "unsure", "confidence": 0.5297, "model_score": 0.4825, "style_score": 0.5769, "combined_score": 0.5297, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "Football in the rain, 1994. We lost nine–nil and I've never been proud"},
  {"status": 200, "guess": "unsure", "confidence": 0.5269, "model_score": 0.6097, "style_score": 0.444, "combined_score": 0.5269, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "Okay so the cat knocked over the plant AGAIN, and this time there was "}
]
```

Gap between the two means: 0.33, against a target of 0.30, so that is a pass by
0.03. Exactly 3 of 5 AI pieces were labelled `ai`, which is the minimum.

**3.** Produced by `run_eval.py::main` (scenario "label coverage"), trial 1:

```json
[
  {"status": 200, "guess": "human", "confidence": 0.8246, "model_score": 0.2187, "style_score": 0.1321, "combined_score": 0.1754, "label": "We think this was probably written by a person.", "sent": "Honestly? I hated my first week at the bakery. Flour in my eyebrows, D"},
  {"status": 200, "guess": "unsure", "confidence": 0.5182, "model_score": 0.1564, "style_score": 0.88, "combined_score": 0.5182, "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.", "sent": "The ferryman kept his lantern lit through the long gale. The harbourma"},
  {"status": 200, "guess": "ai", "confidence": 0.9009, "model_score": 0.8983, "style_score": 0.9036, "combined_score": 0.9009, "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.", "sent": "The implementation of the proposed framework requires careful consider"}
]
```

All three labels appeared. The miss is the other half: 9 of the 20 pieces in
criteria 1 and 2 were `unsure` (3 own, 2 AI, 4 clear-human), against at most 8.

**4.** Produced by `eval_checks.py::run_4` calling `app.py::appeal`, trial 1:

```json
[
  {"kind": "real id", "content_id": "21de1c80-7402-4421-bdd6-76c7639a9634", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "21de1c80-7402-4421-bdd6-76c7639a9634", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "5e905ef0-c003-4cce-af3d-6db2e021d7c4", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "5e905ef0-c003-4cce-af3d-6db2e021d7c4", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "6f763e80-d5be-4c98-bae3-c1bf64c7a405", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "6f763e80-d5be-4c98-bae3-c1bf64c7a405", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "6ee12c8c-8e51-4209-b873-f5f7e484f6f7", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "6ee12c8c-8e51-4209-b873-f5f7e484f6f7", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "f4d62dcf-4fe1-424e-8fb8-9e46424f4401", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "f4d62dcf-4fe1-424e-8fb8-9e46424f4401", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "677591c8-3cb0-424f-80d6-1c5ffc67421e", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "677591c8-3cb0-424f-80d6-1c5ffc67421e", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "7f1120d1-3c45-458f-b14b-dc3191b61cef", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "7f1120d1-3c45-458f-b14b-dc3191b61cef", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "255c425b-9f53-4cbb-b55a-36f1c1a1c167", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "255c425b-9f53-4cbb-b55a-36f1c1a1c167", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "91aaf936-3ce9-44e2-9998-12e7dde61cbb", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "91aaf936-3ce9-44e2-9998-12e7dde61cbb", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "real id", "content_id": "76ea5320-3abc-4f12-8ef5-96decfbc886c", "submit_status": 200, "appeal_status": 200, "appeal_body": {"content_id": "76ea5320-3abc-4f12-8ef5-96decfbc886c", "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.", "status": "under_review"}, "original_entry_unchanged": true, "appeal_entries_after_decision": 1, "ok": true},
  {"kind": "unknown id", "content_id": "eval-unknown-1-1-7cfb9f50-8d86-447e-a666-cc44438dfb12", "appeal_status": 404, "appeal_body": {"error": "unknown_content_id", "message": "We have no decision with that content_id. Check it matches the one in your submission response."}, "under_review_entries": 0, "ok": true},
  {"kind": "unknown id", "content_id": "eval-unknown-1-2-e12d08a3-803f-4395-9261-cb2278275f1a", "appeal_status": 404, "appeal_body": {"error": "unknown_content_id", "message": "We have no decision with that content_id. Check it matches the one in your submission response."}, "under_review_entries": 0, "ok": true},
  {"kind": "unknown id", "content_id": "eval-unknown-1-3-cf63599e-c3aa-40ae-b7c0-7ac737276504", "appeal_status": 404, "appeal_body": {"error": "unknown_content_id", "message": "We have no decision with that content_id. Check it matches the one in your submission response."}, "under_review_entries": 0, "ok": true},
  {"kind": "unknown id", "content_id": "eval-unknown-1-4-38d29b26-6995-4032-9b58-b8fdee266705", "appeal_status": 404, "appeal_body": {"error": "unknown_content_id", "message": "We have no decision with that content_id. Check it matches the one in your submission response."}, "under_review_entries": 0, "ok": true},
  {"kind": "unknown id", "content_id": "eval-unknown-1-5-36372042-7e38-4c21-93a9-ab44215cbfed", "appeal_status": 404, "appeal_body": {"error": "unknown_content_id", "message": "We have no decision with that content_id. Check it matches the one in your submission response."}, "under_review_entries": 0, "ok": true}
]
```

**5.** Produced by `eval_checks.py::run_5` calling `app.py::submit`, trial 1:

```json
[
  {"case": "not JSON", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "JSON list", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "no text", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "empty text", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "whitespace text", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "text is a number", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "no creator_id", "status": 400, "error": "invalid_request", "expected": [400, "invalid_request"], "logged_as_rejected": true, "ok": true},
  {"case": "19 words", "status": 422, "error": "text_too_short", "expected": [422, "text_too_short"], "logged_as_rejected": true, "ok": true},
  {"case": "50,001 chars", "status": 413, "error": "text_too_long", "expected": [413, "text_too_long"], "logged_as_rejected": true, "ok": true},
  {"case": "500,000 chars", "status": 413, "error": "text_too_long", "expected": [413, "text_too_long"], "logged_as_rejected": true, "ok": true},
  {"after the ten": "POST /ping answers", "ok": true, "5xx_count": 0}
]
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
