"""
What my test runs. UNIT 8, MILESTONE 3.

`run_eval.py` runs every scenario here three times. Which criterion each one
serves (criteria.md):

    1  false positives     "own writing"
    2  score spread        "clear AI" and "clear human"
    3  label coverage      "label coverage", plus all of the pieces above
    4  the appeal path     NOT here: an appeal needs a content_id from an
                           earlier submission and a look at the log, which this
                           file can't express. It's in eval_checks.py.
    5  bad input           NOT here either: two of its ten requests aren't dict
                           bodies (a JSON list, a body that isn't JSON) and this
                           file only holds dicts. Also in eval_checks.py.

!! THE STAND-INS BELOW ARE NOT MY WRITING. !!

Criterion 1 is meaningless unless the ten pieces were written by me, and the
five "clear human" pieces are meant to be a real person's too. All fifteen were
written by Claude, imitating plain writers and distinctive ones. They are here
so the whole pipeline could be run and checked end to end. Replace MY_WRITING
(and ideally HUMAN_CLEAR) with real pieces of my own and re-run BEFORE trusting
any verdict on criteria 1 or 2.

The five AI pieces are genuinely AI-generated (by Claude), which is what
criterion 2 asks for.

A "texts" scenario sends each string as {"text": ..., "creator_id":
f"eval_{name[:12]}_{i}"}. Names below differ in their first twelve characters so
no two scenarios share a creator_id and borrow each other's rate limit.
"""

from calibration import INPUTS as CALIBRATION

# ── Criterion 1: my own writing ──────────────────────────────────────────────
# Five plain, short-sentence pieces (the kind the design expects to be accused)
# and five more distinctive ones. STAND-INS: see the note at the top.
MY_WRITING = [
    # plain
    "Yesterday I went to the store near my house. I needed milk and eggs and "
    "some bread. The store was very busy because it was Friday. I waited in "
    "line for ten minutes. Then I paid and walked home. I made eggs for dinner "
    "and watched a movie.",

    "My brother is learning to drive. He practices in the parking lot every "
    "Sunday. He is a little nervous but he is getting better. Last week he did "
    "not hit any cones. My dad sits next to him and gives advice. We are all "
    "proud of him.",

    "I like my new job. The people are friendly and the work is not too hard. "
    "I start at nine and finish at five. On Fridays we eat lunch together in "
    "the kitchen. My manager says I am doing well. I hope to stay here for a "
    "long time.",

    "The bus was late again this morning. I stood at the stop for twenty "
    "minutes. It was cold and it started to rain. When the bus came it was "
    "full. I had to stand all the way to school. I was tired when I got there.",

    "We cleaned the garage on Saturday. It took all day because there was so "
    "much stuff. We found old toys and some books. My mom wanted to keep "
    "everything but my dad said no. In the end we gave a lot to charity. The "
    "garage looks much bigger now.",

    # distinctive
    "Three weeks into the allotment and I've learned one thing: slugs don't "
    "care about my plans. The beans I babied since March? Gone overnight. "
    "Still, there's a particular quiet at six a.m., dew on everything, the "
    "neighbour's radio murmuring something about cricket, and I'll take that "
    "over a clean spreadsheet any day.",

    "My grandmother never wrote a recipe down. You watched. You got a slap on "
    "the wrist if you measured anything. 'A handful,' she'd say, and her "
    "handful was nothing like mine, so my first batch of dumplings could have "
    "been used to patch a roof. She laughed for a week.",

    "I failed my driving test twice, which my sister will never let me forget, "
    "and honestly the second time was the examiner's fault — who schedules a "
    "left turn across a bus lane at rush hour? Anyway, third time lucky. I "
    "parallel parked on the first go and nearly cried.",

    "Not sure why I'm writing this at 2am. The fridge hums. Something about "
    "the week — the meeting that went sideways, the call I didn't return, the "
    "dog staring at me like I'd personally cancelled walks forever. Tomorrow "
    "I'll fix at least one of those. Probably the dog.",

    "There's a crack in the pavement outside my building shaped like Florida, "
    "and every morning I step over it, and every morning I think: someone "
    "should fix that. Nobody will. In a few years it'll be the thing I "
    "remember about this street, not the faces, not the noise. The crack.",
]

# ── Criterion 2: clearly AI and clearly human ────────────────────────────────
AI_CLEAR = [
    "Effective time management is a critical skill that can significantly "
    "improve both personal and professional outcomes. By prioritizing tasks, "
    "setting clear goals, and minimizing distractions, individuals can enhance "
    "their productivity and reduce stress. Furthermore, it is important to "
    "regularly review progress and adjust strategies as needed to ensure "
    "continued success.",

    "Climate change represents one of the most pressing challenges facing "
    "humanity today. It is essential that governments, businesses, and "
    "individuals work together to reduce greenhouse gas emissions and "
    "transition to sustainable energy sources. Additionally, investing in "
    "innovative technologies can help mitigate the impacts of a changing "
    "climate for future generations.",

    "In today's rapidly evolving digital landscape, cybersecurity has become "
    "more important than ever before. Organizations must implement robust "
    "security measures to protect sensitive data from unauthorized access. "
    "Moreover, employee training plays a vital role in preventing breaches and "
    "ensuring that best practices are consistently followed across the entire "
    "company.",

    "Regular physical exercise offers numerous benefits for overall health and "
    "well-being. It can improve cardiovascular health, strengthen muscles, and "
    "boost mental clarity. In addition, maintaining a consistent exercise "
    "routine can help individuals manage weight, reduce the risk of chronic "
    "diseases, and enhance their quality of life over time.",

    "Reading is a valuable habit that provides many advantages for personal "
    "growth and development. It expands vocabulary, improves concentration, "
    "and fosters empathy by exposing readers to diverse perspectives. "
    "Furthermore, making time for reading each day can serve as an effective "
    "way to relax and reduce stress after a long day.",
]

# STAND-INS, not a real person's writing: see the note at the top.
HUMAN_CLEAR = [
    "Dad's truck smelled like wet dog and peppermints. Every Saturday, same "
    "drill: he'd hand me a thermos, I'd pretend to be awake, and we'd rattle "
    "out to the lake before the fog lifted. He never talked. Not once. But "
    "he'd tap the dashboard twice when a heron went by, and that was the whole "
    "conversation.",

    "The thing nobody tells you about moving abroad is the small stuff. Not "
    "the visa. Not the language. It's standing in a supermarket aisle for ten "
    "minutes because you can't work out which one is the milk. I cried over a "
    "carton. A carton! A kind woman pointed. I still think about her.",

    "Lena says I overthink everything and she's right, obviously, but try "
    "telling that to the part of my brain currently rehearsing a conversation "
    "with my landlord that will never happen. He's fine. The leak's fixed. I "
    "am a grown adult holding a cold cup of tea and arguing with a ghost.",

    "Football in the rain, 1994. We lost nine–nil and I've never been prouder. "
    "Marcus in goal, absolutely soaked, screaming at a seagull. Coach just "
    "stood there with his umbrella, shaking his head, grinning. You don't "
    "forget that. You don't forget who stood in the mud with you.",

    "Okay so the cat knocked over the plant AGAIN, and this time there was "
    "soil in the bed, in my shoe, and, somehow, in the butter dish. I don't "
    "know how. I don't want to know how. She sat in the middle of it looking "
    "as pleased as a cat can look, which is very.",
]

SCENARIOS = [
    {"name": "own writing", "criterion": 1, "texts": MY_WRITING},
    {"name": "clear AI", "criterion": 2, "texts": AI_CLEAR},
    {"name": "clear human", "criterion": 2, "texts": HUMAN_CLEAR},
    {
        "name": "label coverage",
        "criterion": 3,
        # One input known to land in each band, so every label is exercised
        # each trial. The other half of criterion 3 (at most 8 of the 20
        # pieces above are "unsure") is worked out from the scenarios above.
        "texts": [
            CALIBRATION["clear_human"],
            CALIBRATION["even_formal"],
            CALIBRATION["clear_ai"],
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    seen = {}
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")
        else:
            prefix = scenario["name"][:12]
            if prefix in seen:
                problems.append(
                    f"scenario {i} ('{scenario['name']}') shares its first twelve "
                    f"characters with '{seen[prefix]}', so they'd share creator_ids "
                    f"and a rate limit"
                )
            seen[prefix] = scenario["name"]

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
