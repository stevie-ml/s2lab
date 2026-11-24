"""
Preposition Precision and S2: The Of-Override Effect

Research question: Do spatial/directional prepositions carry systematically higher S2
than common relational prepositions? When poets choose a specific spatial preposition
where GPT-2 expects a generic one (especially 'of'), does this produce a measurable
information-theoretic signature?

Hypothesis: Common prepositions (of/to/in/for/with/on) are highly expected (negative S2),
while spatial/directional prepositions (through/under/among/beneath/above/before) carry
positive S2 — the 'spatial precision premium.'

The 'Of-Override Effect': When a poet writes a spatial preposition and GPT-2 expected 'of',
this represents a deliberate choice to impose precise spatial/directional grammar where
conventional language would have used generic connection.
"""

import json
import sys
from collections import defaultdict, Counter

RESULTS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/preposition_spatial_s2.json"


COMMON_PREPS = {'of', 'to', 'in', 'for', 'with', 'on', 'at', 'by', 'from'}
SPATIAL_PREPS = {
    'through', 'upon', 'under', 'among', 'beneath', 'beside', 'beyond',
    'against', 'without', 'within', 'across', 'around', 'between',
    'above', 'below', 'over', 'into', 'behind', 'before', 'toward',
    'towards', 'outside', 'past', 'since', 'until', 'after', 'during', 'near'
}
ALL_PREPS = COMMON_PREPS | SPATIAL_PREPS


def run():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    # --- Global aggregation ---
    common_s2 = []
    spatial_s2 = []
    era_data = defaultdict(lambda: {"common": [], "spatial": []})
    of_tokens = []

    # --- Swap analysis: poet uses spatial, GPT-2 expected 'of' ---
    of_overrides = []  # spatial replaces 'of'
    prep_swaps = []    # any prep-to-prep swap

    for poem in data:
        meta = poem["metadata"]
        era = meta["era"]
        for tok in poem["tokens"]:
            word = tok["token"].strip().lower()
            p_nl = tok.get("p_newline", 1.0)
            if p_nl >= 0.9:
                continue
            if word in COMMON_PREPS:
                common_s2.append(tok["s2"])
                era_data[era]["common"].append(tok["s2"])
                if word == "of":
                    of_tokens.append(tok["s2"])
            elif word in SPATIAL_PREPS:
                spatial_s2.append(tok["s2"])
                era_data[era]["spatial"].append(tok["s2"])
                alts = tok.get("alternatives", [])
                if alts:
                    top_alt = alts[0]["token"].strip().lower()
                    if top_alt == "of":
                        of_overrides.append({
                            "actual": word,
                            "s2": tok["s2"],
                            "rank": tok["rank"],
                            "entropy": tok["entropy"],
                            "context": tok.get("context_before", "")[-35:],
                            "era": era,
                            "author": meta["author"],
                            "title": meta["title"][:45],
                        })
                    if top_alt in ALL_PREPS and top_alt != word:
                        prep_swaps.append({
                            "predicted": top_alt,
                            "actual": word,
                            "s2": tok["s2"],
                            "context": tok.get("context_before", "")[-35:],
                            "era": era,
                            "author": meta["author"],
                            "title": meta["title"][:45],
                        })

    of_overrides.sort(key=lambda x: -x["s2"])
    prep_swaps.sort(key=lambda x: -x["s2"])

    # --- Per-era spatial preposition breakdown ---
    era_stats = {}
    for era, d in era_data.items():
        nc = len(d["common"])
        ns = len(d["spatial"])
        if nc + ns < 15:
            continue
        era_stats[era] = {
            "n_common": nc,
            "avg_common_s2": sum(d["common"]) / nc if nc else None,
            "n_spatial": ns,
            "avg_spatial_s2": sum(d["spatial"]) / ns if ns else None,
            "gap": (sum(d["spatial"]) / ns if ns else 0) - (sum(d["common"]) / nc if nc else 0),
        }

    results = {
        "global": {
            "n_common": len(common_s2),
            "avg_common_s2": sum(common_s2) / len(common_s2),
            "n_spatial": len(spatial_s2),
            "avg_spatial_s2": sum(spatial_s2) / len(spatial_s2),
            "gap_bits": sum(spatial_s2) / len(spatial_s2) - sum(common_s2) / len(common_s2),
            "n_of_tokens": len(of_tokens),
            "avg_of_s2": sum(of_tokens) / len(of_tokens),
        },
        "of_override_count": len(of_overrides),
        "of_overrides_top": of_overrides[:25],
        "of_override_by_prep": dict(Counter(x["actual"] for x in of_overrides).most_common()),
        "prep_swap_count": len(prep_swaps),
        "prep_swaps_top": prep_swaps[:25],
        "swap_patterns": [
            {"predicted": k[0], "actual": k[1], "count": v}
            for k, v in Counter((x["predicted"], x["actual"]) for x in prep_swaps).most_common(20)
        ],
        "era_stats": era_stats,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    # Print summary
    g = results["global"]
    print("=== PREPOSITION SPATIAL PRECISION ANALYSIS ===")
    print(f"Common prepositions (of/to/in/for/with/on/at/by/from):")
    print(f"  n={g['n_common']}, avg S2={g['avg_common_s2']:+.3f}")
    print(f"Spatial prepositions (through/under/among/beside/etc.):")
    print(f"  n={g['n_spatial']}, avg S2={g['avg_spatial_s2']:+.3f}")
    print(f"Gap: {g['gap_bits']:+.3f} bits")
    print(f"'of' specifically: n={g['n_of_tokens']}, avg S2={g['avg_of_s2']:+.3f}")
    print()
    print(f"Of-Override events (spatial used where 'of' expected): {results['of_override_count']}")
    print(f"All prep-to-prep swaps: {results['prep_swap_count']}")
    print()
    print("Era gap ranking (spatial - common, nats where n>=20 each):")
    ranked = sorted(
        [(era, v) for era, v in era_stats.items() if v["n_spatial"] >= 3],
        key=lambda x: -x[1]["gap"],
    )
    for era, v in ranked[:15]:
        print(f"  {era:<22}: gap={v['gap']:+.3f}  (n_common={v['n_common']}, n_spatial={v['n_spatial']})")
    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    run()
