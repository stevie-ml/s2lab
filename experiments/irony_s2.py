"""
Experiment: Verbal Irony and S₂

Hypothesis: Verbal irony operates above the token level.
  Ironic lines use CONVENTIONAL tokens (low S₂) to express
  UNCONVENTIONAL meanings — hiding surprise from the surface model.

Design:
  1. Analyze paired passages: ironic version vs. literal paraphrase
  2. Mark "key ironic tokens" in each passage
  3. Compare S₂ at those tokens: ironic vs. literal
  4. Analyze mock-heroic poems (Pope) — high-register words in trivial contexts
  5. Examine the "unsaid" alternatives at ironic tokens — what did GPT-2 expect?

Expected finding: ironic tokens will have LOWER S₂ than their literal equivalents,
because the model has no access to context-level semantics. The semantic surprise
is invisible to the surface model.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine import analyze_poem, get_model
import json

# ── Paired passages: ironic vs. literal ───────────────────────────────────────
# Each pair shares the same emotional/semantic content but irony inverts the
# surface vocabulary. We mark "ironic tokens" and compare S₂ there.

PAIRS = [
    {
        "id": "great_war_1",
        "ironic": {
            "title": "Dulce et Decorum Est (closing lines)",
            "author": "Wilfred Owen",
            "year": 1920,
            "text": (
                "My friend, you would not tell with such high zest\n"
                "To children ardent for some desperate glory,\n"
                "The old Lie: Dulce et decorum est\n"
                "Pro patria mori."
            ),
            "ironic_tokens": ["glory", "Dulce", "decorum", "est"],
            "note": "Owen ironizes the Latin tag: 'sweet and fitting to die for one's country' — conventional sentiment vs. gas attack reality"
        },
        "literal": {
            "title": "Dulce et Decorum Est (literal paraphrase)",
            "author": "paraphrase",
            "year": 2024,
            "text": (
                "My friend, you would not tell with such high zest\n"
                "To children ardent for some desperate horror,\n"
                "The old Truth: Painful and shameful it is\n"
                "To die for one's country."
            ),
            "ironic_tokens": ["horror", "Truth", "Painful", "shameful"],
        }
    },
    {
        "id": "swift_praise",
        "ironic": {
            "title": "On the Death of Dr. Swift (ironic self-praise)",
            "author": "Jonathan Swift",
            "year": 1739,
            "text": (
                "Perhaps I may allow, the Dean\n"
                "Had too much satire in his vein;\n"
                "And seemed determined not to starve it,\n"
                "Because no age could more deserve it."
            ),
            "ironic_tokens": ["allow", "deserve"],
            "note": "Self-deprecatory framing ironizes the praise; 'no age could more deserve it' means the age deserves satire"
        },
        "literal": {
            "title": "On the Death of Dr. Swift (literal version)",
            "author": "paraphrase",
            "year": 2024,
            "text": (
                "Perhaps I may admit, the Dean\n"
                "Had too much anger in his vein;\n"
                "And seemed determined not to spare it,\n"
                "Because no age could more require it."
            ),
            "ironic_tokens": ["admit", "require"],
        }
    },
    {
        "id": "mock_heroic_pope",
        "ironic": {
            "title": "The Rape of the Lock (Canto I, opening)",
            "author": "Alexander Pope",
            "year": 1714,
            "text": (
                "What dire offence from am'rous causes springs,\n"
                "What mighty contests rise from trivial things,\n"
                "I sing—This verse to Caryl, Muse! is due:\n"
                "This, ev'n Belinda may vouchsafe to view."
            ),
            "ironic_tokens": ["dire", "mighty", "contests", "trivial"],
            "note": "Mock-heroic: epic vocabulary applied to a card game and a stolen curl"
        },
        "literal": {
            "title": "Mock-heroic control (literal epic)",
            "author": "paraphrase",
            "year": 2024,
            "text": (
                "What dire offence from warlike causes springs,\n"
                "What mighty contests rise from glorious things,\n"
                "I sing—This verse to Caesar, Muse! is due:\n"
                "This, ev'n Achilles may vouchsafe to view."
            ),
            "ironic_tokens": ["warlike", "glorious", "Caesar", "Achilles"],
        }
    },
    {
        "id": "housman_bitter",
        "ironic": {
            "title": "Here Dead We Lie",
            "author": "A.E. Housman",
            "year": 1922,
            "text": (
                "Here dead we lie because we did not choose\n"
                "To live and shame the land from which we sprung.\n"
                "Life, to be sure, is nothing much to lose;\n"
                "But young men think it is, and we were young."
            ),
            "ironic_tokens": ["nothing", "sure", "shame"],
            "note": "Bitter understatement: 'nothing much to lose' ironizes the sacrifice. 'shame the land' — dying is better than cowardice."
        },
        "literal": {
            "title": "Here Dead We Lie (literal paraphrase)",
            "author": "paraphrase",
            "year": 2024,
            "text": (
                "Here dead we lie because we chose to fight\n"
                "To live and serve the land from which we sprung.\n"
                "Life, we know, was everything to lose;\n"
                "But young men knew it too, and we were young."
            ),
            "ironic_tokens": ["fight", "serve", "everything"],
        }
    },
    {
        "id": "larkin_this_be",
        "ironic": {
            "title": "This Be The Verse",
            "author": "Philip Larkin",
            "year": 1971,
            "text": (
                "They fuck you up, your mum and dad.\n"
                "They may not mean to, but they do.\n"
                "They fill you with the faults they had\n"
                "And add some extra, just for you."
            ),
            "ironic_tokens": ["extra", "just"],
            "note": "Blunt register with ironic closing flourish: 'just for you' echoes a gift-giving cliché applied to inherited trauma"
        },
        "literal": {
            "title": "This Be The Verse (literal paraphrase)",
            "author": "paraphrase",
            "year": 2024,
            "text": (
                "They harm you deeply, your mum and dad.\n"
                "They may not mean to, but they do.\n"
                "They fill you with the faults they had\n"
                "And add some more, without relief."
            ),
            "ironic_tokens": ["more", "without"],
        }
    },
]

# ── Understatement corpus (a subtype of irony) ────────────────────────────────
UNDERSTATEMENT_PAIRS = [
    {
        "text": "It is a far, far better thing that I do, than I have ever done.",
        "note": "Dickens hero understatement before execution",
        "key_tokens": ["better", "ever"],
    },
    {
        "text": "I have measured out my life with coffee spoons.",
        "note": "Prufrock — monumentalizing the trivial",
        "key_tokens": ["measured", "coffee"],
    },
    {
        "text": "I am not afraid of storms, for I am learning how to sail my ship.",
        "note": "Alcott — calm framing of existential challenge",
        "key_tokens": ["afraid", "learning"],
    },
]

def run(save_path=None):
    results = {
        "experiment": "irony_s2",
        "hypothesis": "Verbal irony hides semantic surprise: ironic tokens have lower S₂ than their literal counterparts",
        "pairs": [],
        "summary": {}
    }

    ironic_key_s2 = []
    literal_key_s2 = []
    ironic_all_s2 = []
    literal_all_s2 = []

    for pair in PAIRS:
        print(f"\n── Pair: {pair['id']} ──")
        pair_result = {"id": pair["id"]}

        for variant in ("ironic", "literal"):
            p = pair[variant]
            print(f"  Analyzing {variant}: {p['title']}")
            analysis = analyze_poem(
                p["text"],
                title=p["title"],
                author=p["author"],
                year=p["year"],
            )

            tokens = analysis["tokens"]
            ironic_tokens_set = set(t.lower().strip() for t in p["ironic_tokens"])

            # Find S₂ at the designated "key" tokens
            key_s2 = []
            key_moments = []
            for td in tokens:
                tok = td["token"].strip().lower()
                if tok in ironic_tokens_set:
                    key_s2.append(td["s2"])
                    key_moments.append({
                        "token": td["token"],
                        "s2": td["s2"],
                        "surprisal": td["surprisal"],
                        "entropy": td["entropy"],
                        "top_alt": td["alternatives"][0]["token"] if td["alternatives"] else None,
                    })

            avg_all = analysis["summary"]["avg_s2"]
            avg_key = sum(key_s2) / len(key_s2) if key_s2 else None

            pair_result[variant] = {
                "title": p["title"],
                "avg_s2_all": avg_all,
                "avg_s2_key_tokens": round(avg_key, 4) if avg_key is not None else None,
                "key_moments": key_moments,
                "summary": analysis["summary"],
                "note": p.get("note", ""),
            }

            if variant == "ironic":
                ironic_all_s2.append(avg_all)
                if avg_key is not None:
                    ironic_key_s2.append(avg_key)
            else:
                literal_all_s2.append(avg_all)
                if avg_key is not None:
                    literal_key_s2.append(avg_key)

        pair_result["delta_avg_s2"] = round(
            pair_result["ironic"]["avg_s2_all"] - pair_result["literal"]["avg_s2_all"], 4
        )
        pair_result["delta_key_s2"] = round(
            (pair_result["ironic"]["avg_s2_key_tokens"] or 0)
            - (pair_result["literal"]["avg_s2_key_tokens"] or 0), 4
        )

        print(f"  Ironic avg S₂: {pair_result['ironic']['avg_s2_all']:.3f}  |  "
              f"Key tokens: {pair_result['ironic']['avg_s2_key_tokens']}")
        print(f"  Literal avg S₂: {pair_result['literal']['avg_s2_all']:.3f}  |  "
              f"Key tokens: {pair_result['literal']['avg_s2_key_tokens']}")
        print(f"  Δ avg_s2 = {pair_result['delta_avg_s2']:+.3f}  |  "
              f"Δ key_s2 = {pair_result['delta_key_s2']:+.3f}")

        results["pairs"].append(pair_result)

    # Grand summary
    grand_ironic_avg = sum(ironic_all_s2) / len(ironic_all_s2)
    grand_literal_avg = sum(literal_all_s2) / len(literal_all_s2)
    grand_ironic_key = sum(ironic_key_s2) / len(ironic_key_s2) if ironic_key_s2 else None
    grand_literal_key = sum(literal_key_s2) / len(literal_key_s2) if literal_key_s2 else None

    results["summary"] = {
        "grand_ironic_avg_s2": round(grand_ironic_avg, 4),
        "grand_literal_avg_s2": round(grand_literal_avg, 4),
        "grand_delta_avg": round(grand_ironic_avg - grand_literal_avg, 4),
        "grand_ironic_key_s2": round(grand_ironic_key, 4) if grand_ironic_key else None,
        "grand_literal_key_s2": round(grand_literal_key, 4) if grand_literal_key else None,
        "grand_delta_key": round(grand_ironic_key - grand_literal_key, 4) if (grand_ironic_key and grand_literal_key) else None,
        "hypothesis_supported": (grand_ironic_avg < grand_literal_avg),
        "n_pairs": len(PAIRS),
    }

    print("\n═══ GRAND SUMMARY ═══")
    print(f"  Ironic avg S₂  (all tokens): {grand_ironic_avg:.4f}")
    print(f"  Literal avg S₂ (all tokens): {grand_literal_avg:.4f}")
    print(f"  Δ = {grand_ironic_avg - grand_literal_avg:+.4f}")
    if grand_ironic_key and grand_literal_key:
        print(f"  Ironic key-token S₂:  {grand_ironic_key:.4f}")
        print(f"  Literal key-token S₂: {grand_literal_key:.4f}")
        print(f"  Key-token Δ = {grand_ironic_key - grand_literal_key:+.4f}")

    if save_path is None:
        save_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "results", "irony_s2.json"
        )
    with open(save_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {save_path}")
    return results


if __name__ == "__main__":
    run()
