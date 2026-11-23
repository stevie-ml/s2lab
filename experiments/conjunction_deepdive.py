"""
Conjunction Deep-Dive: Coordinating vs Subordinating vs Adversative
Builds on syntactic_position_vs_s2.md finding that conjunctions show
high poetry-vs-prose S2 gap (Δ = +2.918), second only to adjectives/nouns.

Hypothesis: Adversative conjunctions (but, yet, nor, however) function as
volta markers — signaling semantic reversals — and should show higher S2
than additive (and) or disjunctive (or) conjunctions. Within subordinating
conjunctions, causal (because, since, for) vs temporal (when, while, after)
vs concessive (although, though, even if) may show different patterns.

No external POS library needed: we match by token text directly.
"""

import json
from collections import defaultdict

# --- Conjunction taxonomy ---
COORD_ADDITIVE    = {"and", "both", "also", "plus"}
COORD_ADVERSATIVE = {"but", "yet", "however", "nevertheless", "nonetheless",
                     "still", "though", "whereas", "while", "while"}
COORD_DISJUNCTIVE = {"or", "nor", "either", "neither", "else", "otherwise"}
COORD_CAUSAL      = {"so", "for", "therefore", "thus", "hence", "accordingly",
                     "consequently"}

SUB_CAUSAL        = {"because", "since", "as", "inasmuch"}
SUB_TEMPORAL      = {"when", "while", "after", "before", "once", "until",
                     "whenever", "as"}
SUB_CONCESSIVE    = {"although", "though", "even", "despite", "albeit",
                     "notwithstanding", "regardless"}
SUB_CONDITIONAL   = {"if", "unless", "whether", "provided", "assuming",
                     "supposing", "lest"}
SUB_RELATIVE      = {"that", "which", "who", "whom", "whose", "where",
                     "wherever", "whatever", "whoever"}

# Map to group name
_GROUPS = {
    "coord_additive":    COORD_ADDITIVE,
    "coord_adversative": COORD_ADVERSATIVE,
    "coord_disjunctive": COORD_DISJUNCTIVE,
    "coord_causal":      COORD_CAUSAL,
    "sub_causal":        SUB_CAUSAL,
    "sub_temporal":      SUB_TEMPORAL,
    "sub_concessive":    SUB_CONCESSIVE,
    "sub_conditional":   SUB_CONDITIONAL,
    "sub_relative":      SUB_RELATIVE,
}


def classify_token(text: str):
    """Return group name(s) for a token text, or empty list."""
    # Normalize: strip leading space, lowercase
    word = text.strip().lower()
    hits = []
    for group, members in _GROUPS.items():
        if word in members:
            hits.append(group)
    return hits


def artifact_free(tok: dict) -> bool:
    """True if the token is not a stanza-break artifact position."""
    return tok.get("p_newline", 1.0) < 0.9


def run():
    with open("results/corpus_results.json") as f:
        data = json.load(f)

    poetry_entries = [d for d in data if d["metadata"].get("era") != "control"]
    prose_entries  = [d for d in data if d["metadata"].get("era") == "control"]

    def accumulate(entries):
        group_s2   = defaultdict(list)
        group_surp = defaultdict(list)
        # Also track per-poet for adversative
        poet_adversative = defaultdict(list)
        era_adversative  = defaultdict(list)

        for entry in entries:
            author = entry["metadata"].get("author", "Unknown")
            era    = entry["metadata"].get("era", "unknown")
            for tok in entry["tokens"]:
                if not artifact_free(tok):
                    continue
                groups = classify_token(tok["token"])
                for g in groups:
                    group_s2[g].append(tok["s2"])
                    group_surp[g].append(tok["surprisal"])
                    if g == "coord_adversative":
                        poet_adversative[author].append(tok["s2"])
                        era_adversative[era].append(tok["s2"])

        summary = {}
        for g in _GROUPS:
            vals = group_s2[g]
            if not vals:
                summary[g] = {"n": 0, "avg_s2": None, "avg_surprisal": None}
                continue
            summary[g] = {
                "n": len(vals),
                "avg_s2": round(sum(vals) / len(vals), 4),
                "avg_surprisal": round(sum(group_surp[g]) / len(vals), 4),
                "pos_ratio": round(sum(1 for v in vals if v > 0) / len(vals), 4),
            }
        return summary, poet_adversative, era_adversative

    poetry_stats, poet_adv, era_adv = accumulate(poetry_entries)
    prose_stats, _, _               = accumulate(prose_entries)

    # Top/bottom poets by adversative conjunction S2
    poet_adv_avg = {
        p: round(sum(vals) / len(vals), 3)
        for p, vals in poet_adv.items() if len(vals) >= 3
    }
    top_poets    = sorted(poet_adv_avg.items(), key=lambda x: -x[1])[:10]
    bottom_poets = sorted(poet_adv_avg.items(), key=lambda x:  x[1])[:10]

    era_adv_avg = {
        e: round(sum(vals) / len(vals), 3)
        for e, vals in era_adv.items() if len(vals) >= 5
    }

    return {
        "poetry": poetry_stats,
        "prose":  prose_stats,
        "top_poets_adversative":    top_poets,
        "bottom_poets_adversative": bottom_poets,
        "era_adversative":          sorted(era_adv_avg.items(), key=lambda x: -x[1]),
        "n_poetry_texts": len(poetry_entries),
        "n_prose_texts":  len(prose_entries),
    }


def print_report(results):
    poetry = results["poetry"]
    prose  = results["prose"]

    print("=" * 72)
    print("CONJUNCTION DEEP-DIVE: S₂ by Conjunction Type  (artifact-free)")
    print(f"Poetry: {results['n_poetry_texts']} texts   "
          f"Prose: {results['n_prose_texts']} texts")
    print("=" * 72)

    ORDER = [
        "coord_additive", "coord_adversative", "coord_disjunctive",
        "coord_causal",
        "sub_causal", "sub_temporal", "sub_concessive",
        "sub_conditional", "sub_relative",
    ]

    print(f"\n{'Group':<22} {'Poet n':>7} {'Poet AvgS2':>10} {'Pros AvgS2':>10} "
          f"{'Δ S2':>8} {'Pos%':>6}")
    print("-" * 70)
    for g in ORDER:
        ps = poetry.get(g, {})
        pr = prose.get(g, {})
        n_p  = ps.get("n", 0)
        s2_p = ps.get("avg_s2")
        s2_r = pr.get("avg_s2")
        pos  = ps.get("pos_ratio", 0)
        if s2_p is None:
            print(f"{g:<22} {'—':>7}")
            continue
        delta = (s2_p - s2_r) if s2_r is not None else float("nan")
        print(f"{g:<22} {n_p:>7,} {s2_p:>+10.3f} "
              f"{(s2_r if s2_r is not None else float('nan')):>+10.3f} "
              f"{delta:>+8.3f} {pos:>5.0%}")

    print("\n\nTop 10 poets by adversative conjunction S₂ (n ≥ 3 tokens):")
    for poet, avg in results["top_poets_adversative"]:
        print(f"  {avg:+.3f}  {poet}")

    print("\nBottom 10 poets by adversative conjunction S₂:")
    for poet, avg in results["bottom_poets_adversative"]:
        print(f"  {avg:+.3f}  {poet}")

    print("\n\nEra-level adversative conjunction S₂ (n ≥ 5 tokens):")
    for era, avg in results["era_adversative"]:
        print(f"  {avg:+.3f}  {era}")

    return results


if __name__ == "__main__":
    results = run()
    print_report(results)
