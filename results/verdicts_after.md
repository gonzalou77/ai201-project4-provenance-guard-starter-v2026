# Run log — after

- Produced by: `eval_checks.py::main` (criteria 4 and 5 live; 1, 2, 3 judged from `run_2026-11-04_1930_after.md`, written by `run_eval.py::main`)
- 2026-11-04 19:33 · service http://127.0.0.1:5055
- Identical output across the three trials of criteria 1-3: **yes**

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing labelled AI | 0 of 10 | 0/10 | 0/10 | 0/10 | **MET** |
| 2. Clearly-AI and clearly-human text told apart | gap ≥ 0.30, ≥ 3/5 AI labelled ai, 0 labelled human | gap 0.33, 0/5 ai, 0 human | gap 0.33, 0/5 ai, 0 human | gap 0.33, 0/5 ai, 0 human | **MISSED** |
| 3. All three labels reachable; unsure not a dumping ground | 3 of 3 labels, ≤ 8 of 20 unsure | 3/3 labels, 16/20 unsure | 3/3 labels, 16/20 unsure | 3/3 labels, 16/20 unsure | **MISSED** |
| 4. Appeal always changes status and is recorded | 10/10 real + 5/5 unknown | 10/10 + 5/5 | 10/10 + 5/5 | 10/10 + 5/5 | **MET** |
| 5. Bad input never crashes and is always logged | 10/10, 0 5xx, ping ok | 10/10 | 10/10 | 10/10 | **MET** |

---

## Real output, trial 1

### 1. My own writing

Produced by `run_eval.py::main` (scenario "own writing"), trial 1.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8687,
    "model_score": 0.8174,
    "style_score": 0.92,
    "combined_score": 0.8687,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Yesterday I went to the store near my house. I needed milk and eggs an"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8007,
    "model_score": 0.7497,
    "style_score": 0.8516,
    "combined_score": 0.8007,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "My brother is learning to drive. He practices in the parking lot every"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8053,
    "model_score": 0.8099,
    "style_score": 0.8007,
    "combined_score": 0.8053,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "I like my new job. The people are friendly and the work is not too har"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8994,
    "model_score": 0.818,
    "style_score": 0.9809,
    "combined_score": 0.8994,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "The bus was late again this morning. I stood at the stop for twenty mi"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.7444,
    "model_score": 0.6999,
    "style_score": 0.7889,
    "combined_score": 0.7444,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "We cleaned the garage on Saturday. It took all day because there was s"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8544,
    "model_score": 0.2582,
    "style_score": 0.033,
    "combined_score": 0.1456,
    "label": "We think this was probably written by a person.",
    "sent": "Three weeks into the allotment and I've learned one thing: slugs don't"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6345,
    "model_score": 0.399,
    "style_score": 0.332,
    "combined_score": 0.3655,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "My grandmother never wrote a recipe down. You watched. You got a slap "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8526,
    "model_score": 0.2606,
    "style_score": 0.0343,
    "combined_score": 0.1474,
    "label": "We think this was probably written by a person.",
    "sent": "I failed my driving test twice, which my sister will never let me forg"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.7293,
    "model_score": 0.3448,
    "style_score": 0.1966,
    "combined_score": 0.2707,
    "label": "We think this was probably written by a person.",
    "sent": "Not sure why I'm writing this at 2am. The fridge hums. Something about"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5735,
    "model_score": 0.5881,
    "style_score": 0.2649,
    "combined_score": 0.4265,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "There's a crack in the pavement outside my building shaped like Florid"
  }
]
```

### 2. Clear AI

Produced by `run_eval.py::main` (scenario "clear AI"), trial 1.

```json
[
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8193,
    "model_score": 0.8225,
    "style_score": 0.816,
    "combined_score": 0.8193,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Effective time management is a critical skill that can significantly i"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.8288,
    "model_score": 0.9281,
    "style_score": 0.7294,
    "combined_score": 0.8288,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Climate change represents one of the most pressing challenges facing h"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.7653,
    "model_score": 0.8327,
    "style_score": 0.698,
    "combined_score": 0.7653,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "In today's rapidly evolving digital landscape, cybersecurity has becom"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6,
    "model_score": 0.8753,
    "style_score": 0.5045,
    "combined_score": 0.6,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Regular physical exercise offers numerous benefits for overall health "
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.7281,
    "model_score": 0.7013,
    "style_score": 0.7549,
    "combined_score": 0.7281,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Reading is a valuable habit that provides many advantages for personal"
  }
]
```

### 2. Clear human

Produced by `run_eval.py::main` (scenario "clear human"), trial 1.

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.7081,
    "model_score": 0.3882,
    "style_score": 0.1956,
    "combined_score": 0.2919,
    "label": "We think this was probably written by a person.",
    "sent": "Dad's truck smelled like wet dog and peppermints. Every Saturday, same"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6493,
    "model_score": 0.4308,
    "style_score": 0.2705,
    "combined_score": 0.3507,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "The thing nobody tells you about moving abroad is the small stuff. Not"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.6184,
    "model_score": 0.3832,
    "style_score": 0.38,
    "combined_score": 0.3816,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Lena says I overthink everything and she's right, obviously, but try t"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5297,
    "model_score": 0.4825,
    "style_score": 0.5769,
    "combined_score": 0.5297,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Football in the rain, 1994. We lost nine–nil and I've never been proud"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5269,
    "model_score": 0.6097,
    "style_score": 0.444,
    "combined_score": 0.5269,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "Okay so the cat knocked over the plant AGAIN, and this time there was "
  }
]
```

### 3. Label coverage

Produced by `run_eval.py::main` (scenario "label coverage"), trial 1.

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.8246,
    "model_score": 0.2187,
    "style_score": 0.1321,
    "combined_score": 0.1754,
    "label": "We think this was probably written by a person.",
    "sent": "Honestly? I hated my first week at the bakery. Flour in my eyebrows, D"
  },
  {
    "status": 200,
    "guess": "unsure",
    "confidence": 0.5182,
    "model_score": 0.1564,
    "style_score": 0.88,
    "combined_score": 0.5182,
    "label": "We can't tell whether this was written by a person or with an AI tool. That isn't a judgement against you: plain, simple writing and some formal styles look like this to our checks. If you'd like, you can ask for a person to take a look.",
    "sent": "The ferryman kept his lantern lit through the long gale. The harbourma"
  },
  {
    "status": 200,
    "guess": "ai",
    "confidence": 0.9009,
    "model_score": 0.8983,
    "style_score": 0.9036,
    "combined_score": 0.9009,
    "label": "This looks like it may have been written with an AI tool. We can't be sure, and we get this wrong, especially with plain, short-sentence writing. If you wrote it yourself, you can appeal and a person will read your reasoning.",
    "sent": "The implementation of the proposed framework requires careful consider"
  }
]
```

### 4. Appeal path

Produced by `eval_checks.py::run_4` calling `app.py::appeal`, trial 1.

```json
[
  {
    "kind": "real id",
    "content_id": "4bcce8fb-c343-40b6-8249-1e11a6338919",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "4bcce8fb-c343-40b6-8249-1e11a6338919",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "24f2f7cf-8d53-471c-b3e3-dc0e9020f0fc",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "24f2f7cf-8d53-471c-b3e3-dc0e9020f0fc",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "8b32e565-3a15-4e65-b355-b3ccbed2debb",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "8b32e565-3a15-4e65-b355-b3ccbed2debb",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "051ead8c-39cf-450b-8b84-b6ebd1bec476",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "051ead8c-39cf-450b-8b84-b6ebd1bec476",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "3cd7899c-5ed1-4389-ba6f-c2fbf9cc9a96",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "3cd7899c-5ed1-4389-ba6f-c2fbf9cc9a96",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "e6bbb46f-0dd7-45a0-b4c9-1b62f8269181",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "e6bbb46f-0dd7-45a0-b4c9-1b62f8269181",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "03b4bb43-fdee-4e1b-9ffe-5e6128e631b6",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "03b4bb43-fdee-4e1b-9ffe-5e6128e631b6",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "f5ea6685-e34d-4b80-835c-54e8155a0b15",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "f5ea6685-e34d-4b80-835c-54e8155a0b15",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "47c0711a-8376-49b5-a8b1-d7fec6e13616",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "47c0711a-8376-49b5-a8b1-d7fec6e13616",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "real id",
    "content_id": "2c3bd121-6d5e-4d12-a25b-a6127187c19f",
    "submit_status": 200,
    "appeal_status": 200,
    "appeal_body": {
      "content_id": "2c3bd121-6d5e-4d12-a25b-a6127187c19f",
      "message": "Your appeal is recorded and a person will read it. Nothing has been re-scored, and the original decision stays in the record.",
      "status": "under_review"
    },
    "original_entry_unchanged": true,
    "appeal_entries_after_decision": 1,
    "ok": true
  },
  {
    "kind": "unknown id",
    "content_id": "eval-unknown-1-1-7f38387b-95ae-4d44-8348-269b3164f30b",
    "appeal_status": 404,
    "appeal_body": {
      "error": "unknown_content_id",
      "message": "We have no decision with that content_id. Check it matches the one in your submission response."
    },
    "under_review_entries": 0,
    "ok": true
  },
  {
    "kind": "unknown id",
    "content_id": "eval-unknown-1-2-2cecf508-8820-4a5a-b367-dc418f0606a2",
    "appeal_status": 404,
    "appeal_body": {
      "error": "unknown_content_id",
      "message": "We have no decision with that content_id. Check it matches the one in your submission response."
    },
    "under_review_entries": 0,
    "ok": true
  },
  {
    "kind": "unknown id",
    "content_id": "eval-unknown-1-3-5d27ce9b-e458-46f2-a462-f327eea71179",
    "appeal_status": 404,
    "appeal_body": {
      "error": "unknown_content_id",
      "message": "We have no decision with that content_id. Check it matches the one in your submission response."
    },
    "under_review_entries": 0,
    "ok": true
  },
  {
    "kind": "unknown id",
    "content_id": "eval-unknown-1-4-e13b578e-7cea-420e-9b77-b1b45e609f37",
    "appeal_status": 404,
    "appeal_body": {
      "error": "unknown_content_id",
      "message": "We have no decision with that content_id. Check it matches the one in your submission response."
    },
    "under_review_entries": 0,
    "ok": true
  },
  {
    "kind": "unknown id",
    "content_id": "eval-unknown-1-5-81cffcd7-b55e-4674-b110-643fe766d72a",
    "appeal_status": 404,
    "appeal_body": {
      "error": "unknown_content_id",
      "message": "We have no decision with that content_id. Check it matches the one in your submission response."
    },
    "under_review_entries": 0,
    "ok": true
  }
]
```

### 5. Bad input

Produced by `eval_checks.py::run_5` calling `app.py::submit`, trial 1.

```json
[
  {
    "case": "not JSON",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "JSON list",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "no text",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "empty text",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "whitespace text",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "text is a number",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "no creator_id",
    "status": 400,
    "error": "invalid_request",
    "expected": [
      400,
      "invalid_request"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "19 words",
    "status": 422,
    "error": "text_too_short",
    "expected": [
      422,
      "text_too_short"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "50,001 chars",
    "status": 413,
    "error": "text_too_long",
    "expected": [
      413,
      "text_too_long"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "case": "500,000 chars",
    "status": 413,
    "error": "text_too_long",
    "expected": [
      413,
      "text_too_long"
    ],
    "logged_as_rejected": true,
    "ok": true
  },
  {
    "after the ten": "POST /ping answers",
    "ok": true,
    "5xx_count": 0
  }
]
```