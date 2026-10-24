"""
Rupture vs. Pivot: Poet-Level Surprise Mechanism Profiles

Building on entropy_cascade_context.md, which found that S₂'s effect on
subsequent entropy reverses depending on context certainty:
  - Confident context (low entropy) + high S₂ → entropy INCREASES (Rupture/Liberation)
  - Uncertain context (high entropy) + high S₂ → entropy DECREASES (Pivot/Anchoring)

This experiment asks: do individual poets have a characteristic preference
for one mechanism over the other? Can we build a "Rupture-Pivot" score per poet?

Method:
  For each consecutive token pair (t, t+1):
    - Collect (s2_t, entropy_t, entropy_{t+1})
  For each poet (min 2 poems, 50+ high-S2 events):
    - Split high-S2 events (S₂ > 1.5) by context:
        * Confident: entropy_t < 4 bits
        * Uncertain: entropy_t >= 7 bits
    - Compute mean Δentropy (= entropy_{t+1} - entropy_t) in each context type
    - Rupture score  = mean Δentropy in confident-context high-S2 events  (positive = liberation)
    - Pivot score    = mean Δentropy in uncertain-context high-S2 events   (negative = anchoring)
    - RP index       = rupture_score - pivot_score  (higher = more rupture-dominant)
"""

import json
import sys
from collections import defaultdict
import numpy as np

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def extract_pairs(poem):
    """Extract consecutive (s2_t, entropy_t, entropy_{t+1}) triples."""
    tokens = poem["tokens"]
    pairs = []
    for i in range(len(tokens) - 1):
        t = tokens[i]
        t1 = tokens[i + 1]
        pairs.append({
            "s2_t": t["s2"],
            "entropy_t": t["entropy"],
            "entropy_t1": t1["entropy"],
        })
    return pairs

def compute_poet_profile(pairs, s2_threshold=1.5, conf_threshold=4.0, unc_threshold=7.0):
    """Compute rupture/pivot scores for a collection of token pairs."""
    rupture_deltas = []   # high-S2 events in confident context
    pivot_deltas = []     # high-S2 events in uncertain context
    all_high_s2_deltas = []

    for p in pairs:
        s2 = p["s2_t"]
        ent = p["entropy_t"]
        delta = p["entropy_t1"] - p["entropy_t"]

        if s2 > s2_threshold:
            all_high_s2_deltas.append(delta)
            if ent < conf_threshold:
                rupture_deltas.append(delta)
            elif ent >= unc_threshold:
                pivot_deltas.append(delta)

    result = {
        "n_high_s2": len(all_high_s2_deltas),
        "n_rupture_events": len(rupture_deltas),
        "n_pivot_events": len(pivot_deltas),
        "mean_delta_all": np.mean(all_high_s2_deltas) if all_high_s2_deltas else None,
    }

    if rupture_deltas:
        result["rupture_score"] = np.mean(rupture_deltas)
        result["rupture_std"] = np.std(rupture_deltas)
    else:
        result["rupture_score"] = None

    if pivot_deltas:
        result["pivot_score"] = np.mean(pivot_deltas)
        result["pivot_std"] = np.std(pivot_deltas)
    else:
        result["pivot_score"] = None

    if result["rupture_score"] is not None and result["pivot_score"] is not None:
        result["rp_index"] = result["rupture_score"] - result["pivot_score"]
    else:
        result["rp_index"] = None

    return result

def main():
    corpus = load_corpus()

    # Group by author
    by_author = defaultdict(lambda: {"poems": [], "pairs": [], "era": None})

    for poem in corpus:
        meta = poem["metadata"]
        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")
        if meta.get("language", "en") != "en":
            continue  # skip non-English for comparability

        by_author[author]["poems"].append(meta["title"])
        by_author[author]["era"] = era  # last era wins (most authors have one)
        pairs = extract_pairs(poem)
        by_author[author]["pairs"].extend(pairs)

    # Compute profiles for poets with enough data
    profiles = []
    MIN_HIGH_S2 = 30  # minimum high-S2 events for reliable estimate

    for author, data in by_author.items():
        prof = compute_poet_profile(data["pairs"])
        if prof["n_high_s2"] < MIN_HIGH_S2:
            continue
        profiles.append({
            "author": author,
            "era": data["era"],
            "n_poems": len(data["poems"]),
            "n_tokens": len(data["pairs"]),
            **prof,
        })

    # Sort by RP index (descending: most rupture-dominant first)
    profiles_with_rp = [p for p in profiles if p["rp_index"] is not None]
    profiles_with_rp.sort(key=lambda x: x["rp_index"], reverse=True)

    print(f"\n{'='*70}")
    print("RUPTURE vs. PIVOT: POET PROFILES")
    print(f"{'='*70}")
    print(f"Poets analyzed: {len(profiles_with_rp)}")
    print(f"\nRupture score = mean Δentropy when: S₂>1.5, entropy_t<4 (confident → liberation)")
    print(f"Pivot score   = mean Δentropy when: S₂>1.5, entropy_t≥7 (uncertain → anchoring)")
    print(f"RP index = rupture_score - pivot_score (positive = rupture-dominant)\n")

    print(f"{'Author':<25} {'Era':<20} {'Rupture':>8} {'Pivot':>8} {'RP idx':>8} {'n_hi-S2':>8}")
    print("-" * 80)
    for p in profiles_with_rp:
        rs = f"{p['rupture_score']:.3f}" if p['rupture_score'] is not None else "  —"
        ps = f"{p['pivot_score']:.3f}" if p['pivot_score'] is not None else "  —"
        rp = f"{p['rp_index']:.3f}" if p['rp_index'] is not None else "  —"
        print(f"{p['author']:<25} {p['era']:<20} {rs:>8} {ps:>8} {rp:>8} {p['n_high_s2']:>8}")

    # Era aggregates
    by_era = defaultdict(list)
    for p in profiles_with_rp:
        by_era[p["era"]].append(p["rp_index"])

    print(f"\n{'='*70}")
    print("ERA AGGREGATES (mean RP index)")
    print(f"{'='*70}")
    era_means = [(era, np.mean(vals), len(vals)) for era, vals in by_era.items() if len(vals) >= 1]
    era_means.sort(key=lambda x: x[1], reverse=True)
    print(f"{'Era':<25} {'Mean RP':>10} {'N poets':>8}")
    print("-" * 45)
    for era, mean_rp, n in era_means:
        bar = "█" * int(abs(mean_rp) * 5) if mean_rp > 0 else "░" * int(abs(mean_rp) * 5)
        print(f"{era:<25} {mean_rp:>10.3f} {n:>8}  {bar}")

    # Taxonomy: top rupture, top pivot, mixed
    quartile = len(profiles_with_rp) // 4
    top_rupture = profiles_with_rp[:quartile]
    top_pivot = profiles_with_rp[-quartile:]
    mixed = profiles_with_rp[quartile:-quartile]

    print(f"\n{'='*70}")
    print("TAXONOMY")
    print(f"{'='*70}")
    print(f"\nSTRONG RUPTURE (top {quartile} poets, RP index most positive):")
    for p in top_rupture[:10]:
        print(f"  {p['author']:<30} RP={p['rp_index']:.3f}  era={p['era']}")

    print(f"\nSTRONG PIVOT (top {quartile} poets, RP index most negative):")
    for p in top_pivot[-10:]:
        print(f"  {p['author']:<30} RP={p['rp_index']:.3f}  era={p['era']}")

    # Save results
    output = {
        "method": "rupture_pivot_poet_profiles",
        "s2_threshold": 1.5,
        "conf_threshold": 4.0,
        "unc_threshold": 7.0,
        "n_poets": len(profiles_with_rp),
        "profiles": profiles_with_rp,
        "era_aggregates": [
            {"era": era, "mean_rp_index": float(mean_rp), "n_poets": n}
            for era, mean_rp, n in era_means
        ],
    }
    with open("results/rupture_pivot_profiles.json", "w") as f:
        json.dump(output, f, indent=2, default=lambda x: round(float(x), 4) if isinstance(x, (float, np.floating)) else x)
    print(f"\nSaved to results/rupture_pivot_profiles.json")

if __name__ == "__main__":
    main()
