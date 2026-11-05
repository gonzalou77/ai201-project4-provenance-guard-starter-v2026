# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-04 19:29
- Auto-marked BROKE (5xx, crash, no response): **0**
- Marked by hand: **56** — **52 HELD, 4 BROKE**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `6843dde2-c047-4b92-b3af-47e5052c0f77` | unsure | 0.518 | HELD |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `1f906e9e-0459-41ad-8222-77a4aa823712` | human | 0.676 | BROKE |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `905fd22c-bf88-4cb4-8f58-d6e0113a6560` | unsure | 0.530 | HELD |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `11b6e96d-15f8-4e42-b4da-f7d7a22d8e07` | unsure | 0.706 | HELD |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `e1c18e69-2660-4362-9646-4f02edde2e01` | human | 0.703 | BROKE |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `8c048d1e-ef12-48f9-bd40-bec4c98bb6c0` | unsure | 0.546 | HELD |
| EV07 | evasion | signal two: padding with punctuation | 200 | `2df3e19d-7833-41da-9274-634953c76a0d` | human | 0.656 | BROKE |
| EV08 | evasion | signal one: text below the token window | 422 | `—` | — | — | HELD |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `42ba8aea-8ce3-4c40-9a73-400e73635d5e` | unsure | 0.618 | HELD |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `0902d305-5c03-4aef-b623-43162511f6ab` | unsure | 0.893 | HELD |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `092d1dcb-e902-41c4-a9ec-e1a2c936e79e` | unsure | 0.617 | HELD |
| FP02 | false_positive | human writing in a formal register | 200 | `f69f194c-23bf-4c83-89b4-fd9adb9e03d0` | unsure | 0.805 | HELD |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `087ad1ea-18ce-4114-8f63-6d5d7769abe7` | unsure | 0.772 | HELD |
| FP04 | false_positive | a student essay written to a rubric | 200 | `081e7570-d693-4dd1-a5d7-f4cef74dc898` | unsure | 0.773 | HELD |
| FP05 | false_positive | technical documentation written by a person | 200 | `e7d9d6f4-8a6b-4789-9323-648329b5c7a0` | unsure | 0.862 | HELD |
| FP06 | false_positive | a person imitating a formal template | 200 | `6658e3a3-ac98-46ef-818e-494da6037b37` | unsure | 0.737 | HELD |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `24c8092c-231b-4cf7-980d-09335f4ff6ef` | unsure | 0.600 | HELD |
| FP08 | false_positive | very short genuine human submission | 422 | `—` | — | — | HELD |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `871a792b-170f-493e-b6b1-eb43b3d4b09b` | unsure | 0.600 | HELD |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `60e583b9-4ac7-484d-8441-f0600f133224` | human | 0.807 | BROKE |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `233a6434-82e2-4635-9e36-97162298eca8` | unsure | 0.524 | HELD |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `7dfe66d0-a2ed-4347-8770-1f6fdbdef57f` | unsure | 0.580 | HELD |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `0ff42000-9f9d-4d1a-afda-a9288f69b6c9` | unsure | 0.566 | HELD |
| PI06 | prompt_injection | instruction plus real human text | 200 | `30751b77-1c35-4bad-b1e7-4002dfc70dd2` | unsure | 0.592 | HELD |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — | HELD |
| MF02 | malformed | text is a single character | 422 | `—` | — | — | HELD |
| MF03 | malformed | text is control characters | 422 | `—` | — | — | HELD |
| MF04 | malformed | text is only punctuation | 422 | `—` | — | — | HELD |
| MF05 | malformed | text is a very long single word | 422 | `—` | — | — | HELD |
| MF06 | malformed | text is emoji only | 422 | `—` | — | — | HELD |
| MF07 | malformed | text is right-to-left script | 422 | `—` | — | — | HELD |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — | HELD |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — | HELD |
| RQ03 | malformed | text is a number | 400 | `—` | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | `—` | — | — | HELD |
| RQ05 | malformed | text is null | 400 | `—` | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — | HELD |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | `—` | — | — | HELD |
| RQ10 | malformed | body is form-encoded, not JSON | 429 | `—` | — | — | HELD |
| RQ11 | malformed | body is JSON claiming to be plain text | 429 | `—` | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — | HELD |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 422 | `—` | — | — | HELD |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — | HELD |

## How I marked them

The same rules as the "before" run, applied the same way.

- **evasion**, **prompt_injection**: BROKE if the label is `human`. `unsure`
  counts as HELD, but only weakly: nothing flagged it.
- **false_positive** (human text): BROKE if labelled `ai`. `unsure` is HELD
  because that label is written not to accuse.
- **malformed**, **flood_same_creator**: BROKE on any 5xx, crash, or a refusal
  that left no log entry. HELD otherwise.
- RQ10 and RQ11 came back 429 in the full run because requests with no usable
  `creator_id` share one bucket and it had filled. Re-sent alone later
  (`after-rerun-*` files) both reached the route and got a 400, so both are HELD.

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "6843dde2-c047-4b92-b3af-47e5052c0f77",
  "creator_id": "attacker_EV01",
  "guess": "unsure",
  "confidence": 0.5182,
  "model_score": 0.1635,
  "style_score": 0.8,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "1f906e9e-0459-41ad-8222-77a4aa823712",
  "creator_id": "attacker_EV02",
  "guess": "human",
  "confidence": 0.6765,
  "model_score": 0.5943,
  "style_score": 0.0527,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "905fd22c-bf88-4cb4-8f58-d6e0113a6560",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5301,
  "model_score": 0.6662,
  "style_score": 0.2736,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "11b6e96d-15f8-4e42-b4da-f7d7a22d8e07",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.7057,
  "model_score": 0.6114,
  "style_score": 0.8,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "e1c18e69-2660-4362-9646-4f02edde2e01",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.7027,
  "model_score": 0.3212,
  "style_score": 0.2733,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "8c048d1e-ef12-48f9-bd40-bec4c98bb6c0",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.5461,
  "model_score": 0.5727,
  "style_score": 0.3352,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "2df3e19d-7833-41da-9274-634953c76a0d",
  "creator_id": "attacker_EV07",
  "guess": "human",
  "confidence": 0.6557,
  "model_score": 0.5862,
  "style_score": 0.1024,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_EV08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "42ba8aea-8ce3-4c40-9a73-400e73635d5e",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.6183,
  "model_score": 0.7042,
  "style_score": 0.5325,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "0902d305-5c03-4aef-b623-43162511f6ab",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.8926,
  "model_score": 0.9792,
  "style_score": 0.8061,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "092d1dcb-e902-41c4-a9ec-e1a2c936e79e",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.6174,
  "model_score": 0.6175,
  "style_score": 0.6172,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "f69f194c-23bf-4c83-89b4-fd9adb9e03d0",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.8052,
  "model_score": 0.7387,
  "style_score": 0.8717,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "087ad1ea-18ce-4114-8f63-6d5d7769abe7",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.7725,
  "model_score": 0.8051,
  "style_score": 0.7398,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "081e7570-d693-4dd1-a5d7-f4cef74dc898",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.7731,
  "model_score": 0.8329,
  "style_score": 0.7133,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "e7d9d6f4-8a6b-4789-9323-648329b5c7a0",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.8618,
  "model_score": 0.8005,
  "style_score": 0.9231,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "6658e3a3-ac98-46ef-818e-494da6037b37",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.7371,
  "model_score": 0.8814,
  "style_score": 0.5928,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "24c8092c-231b-4cf7-980d-09335f4ff6ef",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.8816,
  "style_score": 0.5,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_FP08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "871a792b-170f-493e-b6b1-eb43b3d4b09b",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.6001,
  "model_score": 0.4625,
  "style_score": 0.3373,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "60e583b9-4ac7-484d-8441-f0600f133224",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.807,
  "model_score": 0.2044,
  "style_score": 0.1815,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": "BROKE"
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "233a6434-82e2-4635-9e36-97162298eca8",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.5244,
  "model_score": 0.5943,
  "style_score": 0.3569,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "7dfe66d0-a2ed-4347-8770-1f6fdbdef57f",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.5795,
  "model_score": 0.4998,
  "style_score": 0.3412,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "0ff42000-9f9d-4d1a-afda-a9288f69b6c9",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.5656,
  "model_score": 0.6401,
  "style_score": 0.2286,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "30751b77-1c35-4bad-b1e7-4002dfc70dd2",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.5918,
  "model_score": 0.5583,
  "style_score": 0.6254,
  "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
  "error": null,
  "verdict": "HELD"
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_MF07",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 429,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 422,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": "HELD"
}
```
