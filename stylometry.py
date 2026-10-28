"""
Signal two: the style signal. ← YOU BUILD THIS IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are stubbed below because the brief names those three. They are
stubs, not implementations: what they compute is yours, and so is how you
combine them.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Why these might differ between human and AI writing: generated prose tends
toward even, mid-length sentences and a narrower band of vocabulary, because
that's what "most likely next word" produces on average. Human writing is
lumpier — a three-word sentence next to a forty-word one.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics

import config


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies: stdev / mean of words per sentence (the
    coefficient of variation). Raw scale, 0 upward; **higher means more
    human**. Roughly 0.2 is a text that marches in step, 0.7+ is lumpy.

    A single sentence has no spread, so it returns 0.0 — and `style_signal`
    treats that as "no evidence" rather than "machine-like".
    """
    lengths = [len(words(s)) for s in sentences(text)]
    lengths = [n for n in lengths if n > 0]
    if len(lengths) < 2:
        return 0.0
    return statistics.stdev(lengths) / statistics.mean(lengths)


TTR_WINDOW = 50


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words, 0–1; **higher means more varied vocabulary,
    more human**.

    Raw type-token ratio falls as text gets longer, so a long text and a short
    one aren't comparable. This averages it over sliding windows of
    `TTR_WINDOW` words instead, so length stops looking like a signal. Text
    shorter than one window is measured whole.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    if len(tokens) <= TTR_WINDOW:
        return len(set(tokens)) / len(tokens)
    ratios = [
        len(set(tokens[i:i + TTR_WINDOW])) / TTR_WINDOW
        for i in range(0, len(tokens) - TTR_WINDOW + 1, 10)
    ]
    return sum(ratios) / len(ratios)


# The marks that vary most between writers. Commas and full stops are left out
# on purpose: nearly everyone uses them at nearly the same rate.
_DISTINCTIVE_PUNCT = re.compile(r"[;:()\"!?…—–]|--")


def punctuation_density(text: str) -> float:
    """
    Distinctive punctuation (semicolons, colons, brackets, quotes, ! ? …,
    dashes) per 100 words. Raw scale, 0 upward; **higher means more human**.
    """
    n_words = len(words(text))
    if n_words == 0:
        return 0.0
    return 100 * len(_DISTINCTIVE_PUNCT.findall(text)) / n_words


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.** ← TODO

    Combine your three measures into one number. Same direction as
    `detector.model_signal`, so that `scoring.combine_signals` can treat them
    the same way — if one of your signals runs backwards, everything above it
    is wrong in a way that's hard to see.

    Two things to decide and write down:

      1. Which direction each measure points. Low spread means more AI-ish, so
         it needs flipping. Work out which of your three need that.
      2. How to get each onto a comparable scale. A raw type-token ratio sits
         between 0 and 1; a raw punctuation count doesn't. Adding them
         unscaled means whichever has the bigger numbers wins by default.

    Test it on the four calibration inputs from Milestone 4 — clearly AI,
    clearly human, plain conventional human writing, lightly-edited AI — before
    you trust it. Plain and ordinary, not formal: formal prose reads as *human*
    to signal one, and it is plain writing that gets accused.
    """
    sents = [s for s in sentences(text) if words(s)]

    # Each measure becomes an AI-ness score in 0–1 by a straight line between
    # two bounds: at or beyond the "human" bound it scores 0, at or beyond the
    # "AI" bound it scores 1. All three are flipped, because for each of them
    # a HIGH raw value means more human.
    #
    # ⚠️ The bounds were set by looking at five hand-written calibration inputs
    # (calibration.py), not at a real corpus. They are a starting point.
    parts = {
        "punct": _ramp(punctuation_density(text), human=4.0, ai=0.0),
        "ttr": _ramp(type_token_ratio(text), human=0.90, ai=0.65),
    }
    weights = {
        "spread": config.STYLE_WEIGHT_SPREAD,
        "ttr": config.STYLE_WEIGHT_TTR,
        "punct": config.STYLE_WEIGHT_PUNCT,
    }
    # One sentence has no spread to measure. Say nothing about it rather than
    # let "no evidence" read as "machine-like": drop it and re-weight the rest.
    if len(sents) >= 2:
        parts["spread"] = _ramp(sentence_length_spread(text), human=0.70, ai=0.20)
    else:
        del weights["spread"]

    total = sum(weights.values())
    score = sum(weights[k] * parts[k] for k in weights) / total
    return round(min(max(score, 0.0), 1.0), 4)


def _ramp(value: float, human: float, ai: float) -> float:
    """Straight line from 0 at `human` to 1 at `ai`, clamped. Either order."""
    return min(max((value - human) / (ai - human), 0.0), 1.0)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
