"""
The calibration inputs from Milestone 4, and a table of what every stage says
about each.

    python calibration.py            # both signals and the combined score
    python calibration.py --raw      # the raw style measures too

The inputs are stand-ins I wrote to be recognisable examples of each kind, not
samples from real people. The two that matter most are `plain_human` (what gets
wrongly accused) and `edited_ai` (what gets wrongly let through), so swap in
your own writing for those before trusting any number this prints.
"""

import sys

INPUTS = {
    "clear_ai": (
        "The implementation of the proposed framework requires careful "
        "consideration of several key factors. First, it is important to note "
        "that the system must be able to handle a wide variety of different "
        "inputs. Additionally, the overall performance of the solution depends "
        "on a number of important variables. Furthermore, it is essential to "
        "ensure that the system remains scalable and efficient."
    ),
    "clear_human": (
        "Honestly? I hated my first week at the bakery. Flour in my eyebrows, "
        "Dev yelling about the proofing drawer, and a croissant I'd laminated "
        "so badly it looked like a map of Ohio. But then Tuesday: 4am, nobody "
        "else in yet, the ovens ticking, and I pulled a tray of rye that "
        "actually sounded right when I tapped it. Hollow. Like a knock on a "
        "good door."
    ),
    "plain_human": (
        "I went to the park with my dog on Saturday. The weather was nice and "
        "the sun was out. We walked for about an hour and then sat on a bench. "
        "My dog likes to chase the ducks by the pond. After that we went home "
        "and I made lunch. It was a good day and I was happy."
    ),
    "formal_human": (
        "The committee's reluctance, though understandable, rested on a "
        "misreading of the statute; its drafters had never imagined that a "
        "ferry licence might outlive the ferry. Nobody in the chamber said so. "
        "Instead, over three tedious afternoons, members argued about tonnage, "
        "about precedent, about whether a river can fairly be called a road at "
        "all — and the clerk, who knew better, kept his counsel and his tea."
    ),
    "edited_ai": (
        "The implementation of the proposed framework needs careful thought "
        "about a few key factors. First, the system has to handle lots of "
        "different inputs. It's also worth saying that overall performance "
        "depends on a number of important variables, and that's where most "
        "teams slip up. Scalability matters too. So does keeping things "
        "efficient — no point building something that falls over under load."
    ),
    # The next two are not the four standard inputs. They were added after the
    # first table showed the signals agreeing on everything, to find a case
    # where they split — which is what the combining rule exists to handle.
    "even_formal": (
        "The ferryman kept his lantern lit through the long gale. The "
        "harbourmaster logged each crossing in a ledger of dun vellum. The "
        "magistrate fined three smugglers for contraband tobacco. The curate "
        "preached on charity to a congregation of sodden fishermen. The widow "
        "Penhallow sold her late husband's nets to a cousin in Truro. The "
        "tide, indifferent to all of it, withdrew across the shingle."
    ),
    "varied_ai": (
        "Remote work is changing how teams collaborate. Here is what matters: "
        "communication, trust, and clear expectations. Does that sound simple? "
        "It is not — many organisations struggle with the transition, "
        "particularly when managers rely on visibility as a proxy for "
        "productivity (a habit that dies hard). Ultimately, the most "
        "successful teams treat flexibility as a skill to be developed, not a "
        "perk to be granted."
    ),
}


def main():
    import detector
    import scoring
    import stylometry

    raw = "--raw" in sys.argv
    head = f"{'input':<13}{'model':>7}{'style':>7}{'combined':>10}"
    if raw:
        head += "    spread    ttr  punct/100w"
    print(head)
    for name, text in INPUTS.items():
        m = detector.model_signal(text)
        s = stylometry.style_signal(text)
        c = scoring.combine_signals(m, s)
        row = f"{name:<13}{m:>7.3f}{s:>7.3f}{c:>10.3f}"
        if raw:
            row += (f"    {stylometry.sentence_length_spread(text):>6.3f}"
                    f"{stylometry.type_token_ratio(text):>7.3f}"
                    f"{stylometry.punctuation_density(text):>10.2f}")
        print(row)


if __name__ == "__main__":
    main()
