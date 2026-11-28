"""
Animal Vocabulary and S₂: Do creature names carry distinctive information-theoretic signatures?

Hypothesis: Animal names in poetry represent a form of Straussian deviation —
GPT-2 is trained on general prose and does not expect specific animal names where
they appear. Poets who deploy animal imagery (Hughes, Lawrence, Oliver, Keats) are
consistently surprising the model by naming creatures in contexts where abstractions
or connectives would be more statistically expected.

Sub-hypotheses:
  1. Wild animals have higher S₂ than domestic animals (less statistically expected)
  2. Predatory animals (hawk, wolf, snake) have higher S₂ than prey animals (lamb, dove, sparrow)
  3. Mythological/extinct creatures have the highest S₂ (most unexpected)
  4. Animal names have higher S₂ in poetry than in prose control texts
"""

import json
import re
from collections import defaultdict

RESULTS_FILE = "results/corpus_results.json"

# Animal vocabulary organized by category
ANIMAL_VOCAB = {
    "birds_wild": [
        "hawk", "falcon", "eagle", "raven", "crow", "nightingale", "thrush",
        "swallow", "swift", "heron", "crane", "owl", "osprey", "kite",
        "finch", "robin", "wren", "lark", "magpie", "jay", "starling",
        "vulture", "condor", "albatross", "petrel", "swift", "martin",
        "Hawk", "Falcon", "Eagle", "Raven", "Crow", "Nightingale", "Owl",
        "Lark", "Swallow", "Heron", "Crane", "Robin", "Wren",
    ],
    "birds_domestic": [
        "dove", "pigeon", "sparrow", "hen", "cock", "rooster", "chicken",
        "goose", "duck", "swan", "peacock", "turkey",
        "Dove", "Pigeon", "Sparrow", "Hen", "Goose", "Duck", "Swan", "Peacock",
    ],
    "mammals_predatory": [
        "wolf", "fox", "tiger", "lion", "bear", "leopard", "panther",
        "jaguar", "lynx", "wildcat", "weasel", "mink", "otter",
        "Wolf", "Fox", "Tiger", "Lion", "Bear", "Leopard", "Panther",
        "tyger", "Tyger",  # Blake's tiger spelling
    ],
    "mammals_prey": [
        "deer", "rabbit", "hare", "mouse", "rat", "vole", "mole",
        "squirrel", "chipmunk", "lamb", "sheep", "fawn", "gazelle",
        "antelope", "buck", "doe", "stag",
        "Deer", "Rabbit", "Hare", "Mouse", "Lamb", "Sheep", "Stag",
    ],
    "mammals_domestic": [
        "horse", "dog", "cat", "cow", "bull", "ox", "donkey", "ass",
        "mule", "goat", "pig", "hog",
        "Horse", "Dog", "Cat", "Cow", "Bull",
    ],
    "reptiles_amphibians": [
        "snake", "serpent", "viper", "cobra", "python", "lizard",
        "crocodile", "alligator", "turtle", "tortoise", "toad", "frog",
        "newt", "salamander",
        "Snake", "Serpent", "Lizard", "Crocodile", "Turtle", "Toad", "Frog",
    ],
    "insects_arachnids": [
        "bee", "wasp", "fly", "moth", "butterfly", "beetle", "ant",
        "grasshopper", "cricket", "spider", "scorpion", "tick",
        "caterpillar", "worm", "maggot", "locust", "dragonfly",
        "Bee", "Moth", "Butterfly", "Spider", "Ant",
    ],
    "aquatic": [
        "fish", "whale", "shark", "dolphin", "seal", "walrus", "octopus",
        "squid", "crab", "lobster", "shrimp", "clam", "oyster", "mussel",
        "salmon", "trout", "pike", "eel", "cod",
        "Fish", "Whale", "Shark", "Dolphin", "Seal", "Octopus",
        "Pike", "Salmon",
    ],
    "mythological": [
        "dragon", "griffin", "phoenix", "unicorn", "sphinx", "basilisk",
        "leviathan", "behemoth", "kraken", "chimera", "centaur", "minotaur",
        "Dragon", "Phoenix", "Unicorn", "Sphinx", "Leviathan",
    ],
}

# Flatten for lookup
ALL_ANIMAL_TOKENS = {}
for category, tokens in ANIMAL_VOCAB.items():
    for token in tokens:
        ALL_ANIMAL_TOKENS[token] = category

# Also check lowercase/stripped variants
def get_animal_category(token_str):
    """Return category name or None."""
    t = token_str.strip()
    if t in ALL_ANIMAL_TOKENS:
        return ALL_ANIMAL_TOKENS[t]
    if t.lower() in ALL_ANIMAL_TOKENS:
        return ALL_ANIMAL_TOKENS[t.lower()]
    return None


def main():
    with open(RESULTS_FILE) as f:
        all_results = json.load(f)

    # Separate poetry from prose control
    poetry_tokens = []
    prose_tokens = []
    animal_hits = []  # (token, s2, surprisal, entropy, category, poem_title, author, era, top_pred)

    for poem in all_results:
        meta = poem.get("metadata", {})
        era = meta.get("era", "")
        is_prose = era == "control"
        title = meta.get("title", "")
        author = meta.get("author", "")

        for tok in poem.get("tokens", []):
            token_str = tok.get("token", "")
            s2 = tok.get("s2", 0)
            surprisal = tok.get("surprisal", 0)
            entropy = tok.get("entropy", 0)
            # top prediction comes from alternatives list
            alts = tok.get("alternatives", [])
            top_pred = alts[0]["token"] if alts else ""

            if is_prose:
                prose_tokens.append(s2)
            else:
                poetry_tokens.append(s2)

            cat = get_animal_category(token_str)
            if cat is not None:
                animal_hits.append({
                    "token": token_str,
                    "s2": s2,
                    "surprisal": surprisal,
                    "entropy": entropy,
                    "category": cat,
                    "title": title,
                    "author": author,
                    "era": era,
                    "top_pred": top_pred,
                    "is_prose": is_prose,
                })

    # Corpus baselines
    n_poetry = len(poetry_tokens)
    n_prose = len(prose_tokens)
    avg_poetry_s2 = sum(poetry_tokens) / n_poetry if n_poetry else 0
    avg_prose_s2 = sum(prose_tokens) / n_prose if n_prose else 0

    # Split animal hits into poetry and prose
    animal_poetry = [h for h in animal_hits if not h["is_prose"]]
    animal_prose = [h for h in animal_hits if h["is_prose"]]

    # By category stats
    cat_stats = defaultdict(list)
    for h in animal_poetry:
        cat_stats[h["category"]].append(h["s2"])

    print("=" * 60)
    print("ANIMAL VOCABULARY S2 ANALYSIS")
    print("=" * 60)
    print(f"\nCorpus baselines:")
    print(f"  Poetry avg S₂: {avg_poetry_s2:.3f} (n={n_poetry:,})")
    print(f"  Prose avg S₂:  {avg_prose_s2:.3f} (n={n_prose:,})")
    print(f"\nAnimal tokens found:")
    print(f"  In poetry: {len(animal_poetry)}")
    print(f"  In prose:  {len(animal_prose)}")

    print("\nBy category (poetry only):")
    print(f"  {'Category':<25} {'N':>5} {'Avg S₂':>9} {'% +S₂':>8} {'Max S₂':>9}")
    print(f"  {'-'*60}")

    category_rows = []
    for cat, vals in sorted(cat_stats.items(), key=lambda x: -sum(x[1]) / len(x[1])):
        n = len(vals)
        avg = sum(vals) / n
        pct_pos = sum(1 for v in vals if v > 0) / n * 100
        max_s2 = max(vals)
        category_rows.append((cat, n, avg, pct_pos, max_s2))
        print(f"  {cat:<25} {n:>5} {avg:>+9.3f} {pct_pos:>7.1f}% {max_s2:>9.2f}")

    # Overall animal average
    all_animal_s2 = [h["s2"] for h in animal_poetry]
    if all_animal_s2:
        avg_all = sum(all_animal_s2) / len(all_animal_s2)
        pct_pos_all = sum(1 for v in all_animal_s2 if v > 0) / len(all_animal_s2) * 100
        print(f"\n  {'ALL ANIMALS':<25} {len(all_animal_s2):>5} {avg_all:>+9.3f} {pct_pos_all:>7.1f}%")
        print(f"  Corpus average:            {avg_poetry_s2:>+9.3f}")
        print(f"  Animal premium:            {avg_all - avg_poetry_s2:>+9.3f}")

    # Top high-S2 animal moments
    top_moments = sorted(animal_poetry, key=lambda x: -x["s2"])[:20]
    print("\nTop 20 high-S₂ animal moments:")
    print(f"  {'Token':<15} {'S₂':>8} {'Category':<25} {'Expected':<15} {'Poem'}")
    print(f"  {'-'*85}")
    for h in top_moments:
        poem_short = h["title"][:30] if h["title"] else "?"
        pred_short = repr(h["top_pred"])[:12] if h["top_pred"] else "?"
        print(f"  {h['token']:<15} {h['s2']:>+8.2f} {h['category']:<25} {pred_short:<15} {poem_short}")

    # Cross-category predator vs prey
    predator_cats = ["mammals_predatory", "reptiles_amphibians", "birds_wild"]
    prey_cats = ["mammals_prey", "birds_domestic", "insects_arachnids"]

    predator_vals = [h["s2"] for h in animal_poetry if h["category"] in predator_cats]
    prey_vals = [h["s2"] for h in animal_poetry if h["category"] in prey_cats]

    if predator_vals and prey_vals:
        pred_avg = sum(predator_vals) / len(predator_vals)
        prey_avg = sum(prey_vals) / len(prey_vals)
        print(f"\nPredator vs Prey comparison:")
        print(f"  Predatory animals avg S₂: {pred_avg:+.3f} (n={len(predator_vals)})")
        print(f"  Prey animals avg S₂:      {prey_avg:+.3f} (n={len(prey_vals)})")
        print(f"  Predator premium:          {pred_avg - prey_avg:+.3f}")

    # Wild vs domestic
    wild_cats = ["birds_wild", "mammals_predatory", "mammals_prey", "reptiles_amphibians",
                 "insects_arachnids", "aquatic", "mythological"]
    domestic_cats = ["birds_domestic", "mammals_domestic"]
    wild_vals = [h["s2"] for h in animal_poetry if h["category"] in wild_cats]
    domestic_vals = [h["s2"] for h in animal_poetry if h["category"] in domestic_cats]

    if wild_vals and domestic_vals:
        wild_avg = sum(wild_vals) / len(wild_vals)
        dom_avg = sum(domestic_vals) / len(domestic_vals)
        print(f"\nWild vs Domestic:")
        print(f"  Wild animals avg S₂:     {wild_avg:+.3f} (n={len(wild_vals)})")
        print(f"  Domestic animals avg S₂: {dom_avg:+.3f} (n={len(domestic_vals)})")
        print(f"  Wild premium:             {wild_avg - dom_avg:+.3f}")

    # Save results
    results = {
        "baselines": {
            "poetry_avg_s2": avg_poetry_s2,
            "prose_avg_s2": avg_prose_s2,
            "n_poetry_tokens": n_poetry,
            "n_prose_tokens": n_prose,
        },
        "animal_counts": {
            "poetry": len(animal_poetry),
            "prose": len(animal_prose),
        },
        "by_category": [
            {"category": cat, "n": n, "avg_s2": avg, "pct_positive": pct, "max_s2": mx}
            for cat, n, avg, pct, mx in category_rows
        ],
        "all_animal_avg_s2": avg_all if all_animal_s2 else None,
        "animal_premium": (avg_all - avg_poetry_s2) if all_animal_s2 else None,
        "predator_avg_s2": pred_avg if predator_vals else None,
        "prey_avg_s2": prey_avg if prey_vals else None,
        "wild_avg_s2": wild_avg if wild_vals else None,
        "domestic_avg_s2": dom_avg if domestic_vals else None,
        "top_moments": [
            {
                "token": h["token"],
                "s2": h["s2"],
                "category": h["category"],
                "top_pred": h["top_pred"],
                "poem": h["title"],
                "author": h["author"],
                "era": h["era"],
            }
            for h in top_moments
        ],
    }

    with open("results/animal_vocabulary_s2.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to results/animal_vocabulary_s2.json")
    return results


if __name__ == "__main__":
    main()
