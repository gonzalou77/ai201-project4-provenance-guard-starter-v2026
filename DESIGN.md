# Provenance Guard — design, written before the code

Milestone 1. Nothing here is built yet. Every number marked *(predicted)* is a
guess I will check against real output in Milestone 4, and the thresholds are
provisional until then.

---

## 1. The path a piece of text takes

```
POST /submit  {"text", "creator_id"}
   │
   ├─ 1. Gate         app.py::submit
   ├─ 2. Identify     uuid4 -> content_id
   ├─ 3. Signal one   detector.model_signal(text)    -> model_score
   ├─ 4. Signal two   stylometry.style_signal(text)  -> style_score
   ├─ 5. Combine      scoring.combine_signals(...)   -> combined_score
   ├─ 6. Label        scoring.score_to_label(...)    -> guess + label text
   └─ 7. Record+reply audit.log_decision(...), then JSON back to the caller
```

| # | Stage | What it adds |
|---|---|---|
| 1 | **Gate** (rate limiter in unit 8, then input checks in `submit`) | Decides whether this is a request at all. Bad input is refused with a 4xx and `audit.log_rejection`, so a refusal still leaves a trace. Nothing downstream ever sees an empty, non-string or enormous `text`. |
| 2 | **Identify** | A `content_id` (uuid4). It is the only handle `/appeal` has, so it is made before any scoring and every later step carries it. |
| 3 | **Signal one — model** | `model_score` 0–1, higher = more AI. How predictable gpt2 finds the text. |
| 4 | **Signal two — style** | `style_score` 0–1, higher = more AI. The shape of the text (sentence-length spread, vocabulary repetition, punctuation), with no understanding of meaning. |
| 5 | **Combine** | `combined_score` 0–1. One number from two. This is the step that decides which kind of wrong the service prefers to be (section 4). |
| 6 | **Label** | `guess` (`human` / `unsure` / `ai`) and the sentence a writer reads. This is where a number becomes something said to a person. |
| 7 | **Record and reply** | One audit entry with all nine fields (`status: "decided"`), and a response carrying the label plus both raw signal scores. |

The appeal is a second, short path: `POST /appeal` -> check the `content_id`
exists (`audit.entries_for`) -> `audit.log_appeal` (status `under_review`) ->
confirm. It never re-scores anything and never edits the original entry; the
log is append-only.

The order matters for diagnosis: signals run before combine, and both raw scores
are kept, so when a label is wrong I can tell which stage made it wrong.

---

## 2. What the two signals measure

### Signal one — `detector.py` (given)

- **Measures:** perplexity of the text under gpt2, squashed to 0–1. Low
  perplexity (the model could have guessed the next word) -> high AI score.
- **Why it might differ:** a language model writes by choosing likely next
  words, so its output is, on average, text a language model finds likely.
  People reach for odd words, change direction, and name specific things.
- **What it can't see:**
  - **Predictable is not the same as machine-written.** It rewards common words
    in short ordinary sentences. A second-language writer sticking to words
    they're sure of, a younger writer, anyone writing plainly on purpose, all
    score as machine-like. That is the false-positive person.
  - Text a model has memorised (a famous speech, scripture, boilerplate) is
    very predictable and reads as AI even though a human wrote it.
  - Rare-word, ornate prose reads as *human*. So AI text rewritten with
    unusual vocabulary slips through.
  - It reads only the first `DETECTOR_MAX_TOKENS` (400, about 300 words). Anything
    after that is invisible to it, so AI text can hide behind a human opening
    and vice versa.
  - gpt2 is old. Text from a newer model need not look predictable to it.
  - Very short text gives an unstable reading.

### Signal two — `stylometry.py` (mine)

- **Measures:** three things about the text as text, flipped so that higher
  means more AI-like and combined into one 0–1 score:
  - sentence-length spread (stdev / mean of words per sentence; low spread -> AI-ish)
  - type-token ratio (unique words / total words; low variety -> AI-ish)
  - punctuation density (semicolons, dashes and the like, which vary most
    between writers; the direction is to be set once I see real data)
- **Why it might differ:** "most likely next word" repeated over a paragraph
  tends to produce even, mid-length sentences and a narrower vocabulary. Human
  writing is lumpier: a three-word sentence next to a forty-word one.
- **What it can't see:**
  - **It cannot read.** It has no idea what the text says, so anything that
    changes the shape and not the substance moves it: adding typos (raises
    variety), chopping or joining sentences, pasting in a quotation.
  - Naturally uniform humans score as AI: technical documentation, legal prose,
    lists, a writer who simply keeps sentences even.
  - Type-token ratio falls as text grows, so length itself looks like a signal.
  - One sentence has no spread. That needs a defined return value rather than a
    `statistics.stdev` crash.
  - It shares a blind spot with signal one: plain, short-sentence writing looks
    AI to both. The signals are different measurements, but they do not fail
    independently on this person.

Each blind spot is a cheap evasion or an unfair accusation, and unit 8's attack
set is built from them.

---

## 3. The false positive, followed through

**Who:** Ana, a student writing English as her second language. She writes about
120 words by hand, in short plain sentences, with vocabulary she knows.

| Stage | What happens to her text |
|---|---|
| Gate | Passes. She is over the minimum length. |
| Signal one | Common words, short sentences -> low perplexity -> `model_score` ≈ 0.80 *(predicted)* |
| Signal two | Even sentence lengths, repeated vocabulary -> `style_score` ≈ 0.70 *(predicted)* |
| Combine | `combined_score` ≈ 0.75 *(predicted)* |
| Label | At the starter's 0.65 threshold this is **high-confidence AI**. |

**What the label says to her.** With the starter's placeholder text, nothing
useful: a verdict and no way out. So the design decision is that the AI label
may never read as a finding. Draft (final wording is Milestone 5):

> "This looks like it may have been written with AI help. We can't be sure, and
> we get this wrong, especially for writers who keep their sentences short and
> simple. If you wrote it yourself, tell us and a person will look."

**What she can do.** She sends `POST /appeal` with the `content_id` from her
response and a sentence of reasoning. The item moves to `under_review`, the
appeal sits in the log after the original decision, and she gets a
confirmation. Gaps I can already see and need to close:

1. She needs the `content_id`. It must be in the submit response and the label
   must point her at the appeal, so it is returned with `status` and an
   `appeal` hint.
2. An appeal only records; it re-labels nothing, so her public label stays "AI"
   while `under_review`. I have to decide whether `/appeal` changes what a
   reader sees. For now it only changes `status`, and I'm accepting that.
3. Nothing promises a time or an outcome. The confirmation has to say a person
   will look and not pretend it's instant.

**What this decides about the numbers.** Accusing Ana costs her a lot; missing
one AI essay costs the site a little. So:

- `AI_THRESHOLD` goes up from 0.65, provisionally **0.75**. A text must score
  clearly AI to be called AI. The plain-writer region becomes **unsure**.
- The combining rule should require the *two signals to agree* before the
  result can reach the AI label. If signal one says 0.9 and signal two says 0.3
  the answer is "unsure", never "ai".
- The unsure wording must not accuse, because Ana may land there too.

All of this is checked in Milestone 4 by adding a plain human paragraph to the
four calibration inputs and seeing where it actually lands.

---

## 4. The contract

Both endpoints take and return JSON. Scores are floats 0.0–1.0 rounded to 4
places, **higher always means more likely AI**.

### `POST /submit`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `text` | string | yes | at least 20 words, at most 50,000 characters |
| `creator_id` | string | yes | non-empty after trimming, at most 128 characters |

**Response — 200**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | uuid4. The handle for `/appeal`. |
| `guess` | `"human"` \| `"unsure"` \| `"ai"` | machine-readable verdict |
| `confidence` | float | `max(combined_score, 1 - combined_score)`, so always 0.5–1.0. Low means "close to the middle", and it applies to `unsure` too. |
| `label` | string | the full sentence a reader sees |
| `model_score` | float | signal one |
| `style_score` | float | signal two |
| `combined_score` | float | output of `scoring.combine_signals` |
| `status` | string | always `"decided"` on this endpoint |
| `truncated` | bool | true if signal one only read the first part of the text |
| `appeal` | string | `"POST /appeal with this content_id"` |

**Errors** (always `{"error": "<code>", "message": "<sentence for a person>"}`;
each is also written with `audit.log_rejection`)

| Status | `error` | When |
|---|---|---|
| 400 | `invalid_request` | body isn't a JSON object; `text` or `creator_id` missing, not a string, or empty |
| 413 | `text_too_long` | more than 50,000 characters |
| 422 | `text_too_short` | under 20 words |
| 429 | `rate_limited` | unit 8; shape already set in `app.py` |
| 503 | `detector_unavailable` | `DetectorUnavailable`: the model couldn't load |

No bad input may produce a 500.

### `POST /appeal`

**Request**

| Field | Type | Required | Rules |
|---|---|---|---|
| `content_id` | string | yes | must exist in the log |
| `reasoning` | string | yes | non-empty, at most 2,000 characters |

`creator_id` is not sent. It is read from the original decision's log entry.

**Response — 200**

| Field | Type | Meaning |
|---|---|---|
| `content_id` | string | echoed |
| `status` | `"under_review"` | |
| `message` | string | plain confirmation: a person will look, nothing has been re-scored |

**Errors:** 400 `invalid_request` (bad body, missing or empty field), 404
`unknown_content_id` (no such decision), both with the same error shape as above
and both logged. A second appeal on the same item is accepted and appended; the
log keeps both.

### Read-back: could someone build against this without asking me?

Questions a builder would ask, and the answers now in the contract:

- *What does `confidence` mean for `unsure`?* It's `max(combined, 1 - combined)`
  for every label. No special case, no nulls.
- *Is `creator_id` optional?* No. Required, so rate limiting and the log always
  have an owner.
- *Which status for a too-short or too-long text?* 422 and 413, spelled out.
- *Does an appeal change the label?* No. It changes `status` only.
- *What are the allowed `guess` values?* Exactly three.
- *Which way do scores run?* Higher is more AI, everywhere.
- *Can someone appeal for another person's text?* Yes — there's no login, so
  `content_id` is the only credential. I'm accepting that for this project and
  noting it as a known gap.

Still open and deliberately deferred: the exact thresholds (Milestone 5), the
combining rule's weights (Milestone 4), and the final label wording.
