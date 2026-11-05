#!/usr/bin/env python3
"""
The rest of Milestone 3: criteria 4 and 5, and a verdict for all five.

    python app.py                                   # one terminal
    python run_eval.py --label before               # sends criteria 1, 2, 3
    python eval_checks.py --label before \\
        --run-file results/run_<stamp>_before.md    # runs 4 and 5, judges 1-5

Why this exists. run_eval.py can only send text, so it can't test an appeal
(which needs a content_id from an earlier submission, and a look at the log
afterwards) or two of my bad-input cases (a JSON list and a body that isn't
JSON are not dicts). run_eval.py also leaves the Verdict column blank. This
file does those three things, and writes results/verdicts_<label>.md.

Criteria 1, 2 and 3 are judged from the run file's recorded output. 4 and 5 are
run live, three trials each, against the same service.
"""

import argparse
import datetime as dt
import json
import re
import sys
import time
import uuid
from pathlib import Path

import requests

import config
import scenarios
import scoring

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass

TRIALS = 3
# The per-minute limit is per bucket, and requests with no usable creator_id
# share one bucket, so criterion 5's trials wait for it to clear.
BUCKET_WAIT = 62


# ── helpers ──────────────────────────────────────────────────────────────────

def log_entries(url):
    return requests.get(f"{url}/log", timeout=30).json()["entries"]


def load_run(path):
    """Read run_eval's report back into {scenario name: [trial1, trial2, ...]}."""
    text = Path(path).read_text(encoding="utf-8")
    body = text.split("## What actually came back", 1)[1]
    out = {}
    for section in re.split(r"(?m)^### ", body)[1:]:
        name, _, rest = section.partition("\n")
        blocks = re.findall(r"```json\n(.*?)\n```", rest, re.S)
        out[name.strip()] = [json.loads(b) for b in blocks]
    return out


def readme_has(label_text):
    return label_text in (config.ROOT / "README.md").read_text(encoding="utf-8")


# ── criteria 1-3, judged from run_eval's output ──────────────────────────────

def judge_1(run, t):
    """0 of 10 of my own pieces labelled `ai`."""
    results = run["own writing"][t]
    ai = sum(1 for r in results if r.get("guess") == "ai")
    return ai == 0, f"{ai}/{len(results)}"


def judge_2(run, t):
    """Mean combined gap >= 0.30, >= 3 of 5 AI pieces `ai`, none `human`."""
    ai, human = run["clear AI"][t], run["clear human"][t]
    mean = lambda rs: sum(r["combined_score"] for r in rs) / len(rs)
    gap = mean(ai) - mean(human)
    n_ai = sum(1 for r in ai if r.get("guess") == "ai")
    n_human = sum(1 for r in ai if r.get("guess") == "human")
    ok = gap >= 0.30 and n_ai >= 3 and n_human == 0
    return ok, f"gap {gap:.2f}, {n_ai}/5 ai, {n_human} human"


def judge_3(run, t):
    """All three labels produced, text matching the README, <= 8 of 20 unsure."""
    every = [r for name in ("own writing", "clear AI", "clear human", "label coverage")
             for r in run[name][t]]
    seen = {r.get("guess") for r in every}
    wanted = {"human": scoring.LABEL_HUMAN, "unsure": scoring.LABEL_UNSURE,
              "ai": scoring.LABEL_AI}
    texts_ok = all(r.get("label") == wanted.get(r.get("guess")) for r in every
                   if r.get("status") == 200)
    readme_ok = all(readme_has(v) for v in wanted.values())
    twenty = [r for name in ("own writing", "clear AI", "clear human")
              for r in run[name][t]]
    unsure = sum(1 for r in twenty if r.get("guess") == "unsure")
    labels = len(seen & set(wanted))
    ok = labels == 3 and texts_ok and readme_ok and unsure <= 8
    note = f"{labels}/3 labels, {unsure}/20 unsure"
    if not texts_ok or not readme_ok:
        note += ", label text mismatch"
    return ok, note


# ── criterion 4: the appeal path, live ───────────────────────────────────────

def run_4(url, trial):
    texts = scenarios.AI_CLEAR + scenarios.HUMAN_CLEAR
    records, good = [], 0
    for i, text in enumerate(texts, 1):
        creator = f"eval_appeal_t{trial}_{i}"
        sub = requests.post(f"{url}/submit", json={"text": text, "creator_id": creator},
                            timeout=90)
        cid = sub.json().get("content_id")
        before = [e for e in log_entries(url) if e.get("content_id") == cid]
        decision_before = next((e for e in before if "event" not in e), None)

        ap = requests.post(f"{url}/appeal", timeout=30,
                           json={"content_id": cid, "reasoning": f"eval trial {trial}: I wrote this."})
        after = [e for e in log_entries(url) if e.get("content_id") == cid]
        decision_after = next((e for e in after if "event" not in e), None)
        appeals = [k for k, e in enumerate(after) if e.get("event") == "appeal"]
        ok = (sub.status_code == 200 and ap.status_code == 200
              and ap.json().get("status") == "under_review"
              and decision_before is not None and decision_after == decision_before
              and len(appeals) == 1 and appeals[0] > after.index(decision_after)
              and after[appeals[0]].get("status") == "under_review")
        good += ok
        records.append({"kind": "real id", "content_id": cid, "submit_status": sub.status_code,
                        "appeal_status": ap.status_code, "appeal_body": ap.json(),
                        "original_entry_unchanged": decision_after == decision_before,
                        "appeal_entries_after_decision": len(appeals), "ok": ok})

    bad_good = 0
    for k in range(1, 6):
        fake = f"eval-unknown-{trial}-{k}-{uuid.uuid4()}"
        ap = requests.post(f"{url}/appeal", timeout=30,
                           json={"content_id": fake, "reasoning": "typo test"})
        under = [e for e in log_entries(url)
                 if e.get("content_id") == fake and e.get("status") == "under_review"]
        ok = ap.status_code == 404 and not under
        bad_good += ok
        records.append({"kind": "unknown id", "content_id": fake, "appeal_status": ap.status_code,
                        "appeal_body": ap.json(), "under_review_entries": len(under), "ok": ok})
    passed = good == 10 and bad_good == 5
    return passed, f"{good}/10 + {bad_good}/5", records


# ── criterion 5: bad input, live ─────────────────────────────────────────────

def bad_requests(trial):
    c = lambda n: f"eval_bad_t{trial}_{n}"
    valid = ("The quick brown fox jumps over the lazy dog while the afternoon sun "
             "slowly sets behind the old stone bridge near the river bend today.")
    short = " ".join(["word"] * 19)
    return [
        ("not JSON", {"data": "this is not json {", "headers": {"Content-Type": "application/json"}},
         400, "invalid_request"),
        ("JSON list", {"json": [1, 2, 3]}, 400, "invalid_request"),
        ("no text", {"json": {"creator_id": c(3)}}, 400, "invalid_request"),
        ("empty text", {"json": {"text": "", "creator_id": c(4)}}, 400, "invalid_request"),
        ("whitespace text", {"json": {"text": "  \n\t ", "creator_id": c(5)}}, 400, "invalid_request"),
        ("text is a number", {"json": {"text": 12345, "creator_id": c(6)}}, 400, "invalid_request"),
        ("no creator_id", {"json": {"text": valid}}, 400, "invalid_request"),
        ("19 words", {"json": {"text": short, "creator_id": c(8)}}, 422, "text_too_short"),
        ("50,001 chars", {"json": {"text": ("lorem " * 8400)[:50001], "creator_id": c(9)}},
         413, "text_too_long"),
        ("500,000 chars", {"json": {"text": ("lorem " * 84000)[:500000], "creator_id": c(10)}},
         413, "text_too_long"),
    ]


def run_5(url, trial):
    records, good = [], 0
    for name, kwargs, want_status, want_code in bad_requests(trial):
        n0 = len(log_entries(url))
        r = requests.post(f"{url}/submit", timeout=60, **kwargs)
        try:
            code = r.json().get("error")
        except ValueError:
            code = None
        new = log_entries(url)[n0:]
        logged = (len(new) == 1 and new[0].get("event") == "rejected"
                  and new[0].get("reason") == want_code)
        ok = r.status_code == want_status and code == want_code and logged
        good += ok
        records.append({"case": name, "status": r.status_code, "error": code,
                        "expected": [want_status, want_code], "logged_as_rejected": logged,
                        "ok": ok})
    ping = requests.post(f"{url}/ping", json={"message": "x"}, timeout=10).status_code == 200
    five_xx = sum(1 for r in records if r["status"] >= 500)
    records.append({"after the ten": "POST /ping answers", "ok": ping, "5xx_count": five_xx})
    return good == 10 and ping and five_xx == 0, f"{good}/10", records


# ── main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-file", required=True, help="the results/run_*.md from run_eval.py")
    ap.add_argument("--label", default="")
    ap.add_argument("--url", default=f"http://{config.HOST}:{config.PORT}")
    args = ap.parse_args()

    run = load_run(args.run_file)
    for name in ("own writing", "clear AI", "clear human", "label coverage"):
        if len(run.get(name, [])) != TRIALS:
            sys.exit(f"{args.run_file}: expected {TRIALS} trials of '{name}'")

    results = {k: [] for k in range(1, 6)}
    for t in range(TRIALS):
        for k, judge in ((1, judge_1), (2, judge_2), (3, judge_3)):
            results[k].append(judge(run, t))

    live_4, live_5 = [], []
    for t in range(1, TRIALS + 1):
        print(f"criterion 4, trial {t}...", flush=True)
        p4, n4, rec4 = run_4(args.url, t)
        results[4].append((p4, n4)); live_4.append(rec4)
        print(f"criterion 5, trial {t}...", flush=True)
        p5, n5, rec5 = run_5(args.url, t)
        results[5].append((p5, n5)); live_5.append(rec5)
        if t < TRIALS:
            print(f"  waiting {BUCKET_WAIT}s for the shared rate-limit bucket...", flush=True)
            time.sleep(BUCKET_WAIT)

    stable = all(
        json.dumps(run[name][0], sort_keys=True) == json.dumps(run[name][t], sort_keys=True)
        for name in run for t in range(1, TRIALS))

    spec = {
        1: ("My own writing labelled AI", "0 of 10"),
        2: ("Clearly-AI and clearly-human text told apart", "gap ≥ 0.30, ≥ 3/5 AI labelled ai, 0 labelled human"),
        3: ("All three labels reachable; unsure not a dumping ground", "3 of 3 labels, ≤ 8 of 20 unsure"),
        4: ("Appeal always changes status and is recorded", "10/10 real + 5/5 unknown"),
        5: ("Bad input never crashes and is always logged", "10/10, 0 5xx, ping ok"),
    }
    lines = [f"# Run log — {args.label}" if args.label else "# Run log", "",
             "- Produced by: `eval_checks.py::main` (criteria 4 and 5 live; 1, 2, 3 judged from "
             f"`{Path(args.run_file).name}`, written by `run_eval.py::main`)",
             f"- {dt.datetime.now().strftime('%Y-%m-%d %H:%M')} · service {args.url}",
             f"- Identical output across the three trials of criteria 1-3: **{'yes' if stable else 'NO'}**",
             "", "| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |", "|---|---|---|---|---|---|"]
    for k in range(1, 6):
        verdict = "MET" if all(p for p, _ in results[k]) else "MISSED"
        cells = " | ".join(n for _, n in results[k])
        lines.append(f"| {k}. {spec[k][0]} | {spec[k][1]} | {cells} | **{verdict}** |")

    def block(title, produced, data):
        return ["", f"### {title}", "", f"Produced by {produced}, trial 1.", "",
                "```json", json.dumps(data, indent=2, ensure_ascii=False), "```"]

    lines += ["", "---", "", "## Real output, trial 1"]
    lines += block("1. My own writing", "`run_eval.py::main` (scenario \"own writing\")", run["own writing"][0])
    lines += block("2. Clear AI", "`run_eval.py::main` (scenario \"clear AI\")", run["clear AI"][0])
    lines += block("2. Clear human", "`run_eval.py::main` (scenario \"clear human\")", run["clear human"][0])
    lines += block("3. Label coverage", "`run_eval.py::main` (scenario \"label coverage\")", run["label coverage"][0])
    lines += block("4. Appeal path", "`eval_checks.py::run_4` calling `app.py::appeal`", live_4[0])
    lines += block("5. Bad input", "`eval_checks.py::run_5` calling `app.py::submit`", live_5[0])

    config.RESULTS_DIR.mkdir(exist_ok=True)
    path = config.RESULTS_DIR / f"verdicts_{args.label or 'run'}.md"
    path.write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines[6:6 + 2 + 5]))
    print(f"\nWrote {path.relative_to(config.ROOT)}")


if __name__ == "__main__":
    main()
