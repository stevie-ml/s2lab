"""
S2 Arc Within Poems: How Poets Budget Surprise Across the Poem's Arc

Building on the Rupture-Pivot framework (rupture_pivot_poet_profiles.md) which
established that poets differ in how much they use each mechanism globally, this
experiment asks: does the BALANCE between rupture and pivot SHIFT over the course
of a poem?

Two hypotheses:
  H1 (Front-loading): Poets establish surprising choices early (ruptures dominant in
     Q1), then use uncertainty-collapsing surprises (pivots) to guide closure in Q4.
  H2 (Back-loading): Poems open with uncertain contexts (pivots) and build toward
     confident-context departures (ruptures) as the poet's own imagery creates certainty.
  H0 (Flat): The RP balance is uniform across the poem's arc.

Also tests:
  - Does total S2 "budget" (sum of positive S2 values) concentrate in any quartile?
  - Is average entropy different across quartiles? (entropy arc)
  - Which eras show the strongest arc effects?

Method:
  For each poem with ≥60 clean (non-artifact) tokens:
    1. Remove stanza-break artifact tokens (p_newline >= 0.9)
    2. Divide remaining tokens into four quartiles (Q1=beginning...Q4=end)
    3. For each quartile:
       - Mean S2, max S2, positive-S2 fraction
       - Mean entropy
       - Among high-S2 events (S2 > 1.5):
           * rupture rate: fraction where entropy_t < 4.0 (confident context)
           * pivot rate: fraction where entropy_t >= 7.0 (uncertain context)
           * RP local index = mean Δentropy for rupture events - mean Δentropy for pivot events
    4. Aggregate across poems by quartile
    5. Analyze arc direction and compare by era
"""

import json
import numpy as np
from collections import defaultdict

ARTIFACT_THRESHOLD = 0.9
MIN_CLEAN_TOKENS = 60
S2_HIGH_THRESHOLD = 1.5
CONF_ENTROPY_THRESH = 4.0
UNC_ENTROPY_THRESH = 7.0


def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)


def get_clean_tokens(poem):
    """Return tokens filtered of stanza-break artifact positions."""
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < ARTIFACT_THRESHOLD]


def quartile_stats(tokens):
    """
    Divide tokens into 4 quartiles and compute stats for each.
    Returns a list of 4 dicts.
    """
    n = len(tokens)
    if n < 4:
        return None

    results = []
    for q in range(4):
        start = (q * n) // 4
        end = ((q + 1) * n) // 4
        q_tokens = tokens[start:end]

        s2_vals = [t["s2"] for t in q_tokens]
        ent_vals = [t["entropy"] for t in q_tokens]

        q_result = {
            "n": len(q_tokens),
            "mean_s2": np.mean(s2_vals),
            "max_s2": max(s2_vals),
            "pos_s2_frac": np.mean([1 if s > 0 else 0 for s in s2_vals]),
            "s2_budget": sum(s for s in s2_vals if s > 0),
            "mean_entropy": np.mean(ent_vals),
            "n_high_s2": 0,
            "n_rupture": 0,
            "n_pivot": 0,
            "rupture_deltas": [],
            "pivot_deltas": [],
        }

        # Compute rupture/pivot stats using consecutive token pairs within quartile
        for i in range(len(q_tokens) - 1):
            t = q_tokens[i]
            t1 = q_tokens[i + 1]
            # Only use consecutive positions (not across lines/gaps)
            if abs(t1["position"] - t["position"]) > 3:
                continue

            s2 = t["s2"]
            ent = t["entropy"]
            delta = t1["entropy"] - t["entropy"]

            if s2 > S2_HIGH_THRESHOLD:
                q_result["n_high_s2"] += 1
                if ent < CONF_ENTROPY_THRESH:
                    q_result["n_rupture"] += 1
                    q_result["rupture_deltas"].append(delta)
                elif ent >= UNC_ENTROPY_THRESH:
                    q_result["n_pivot"] += 1
                    q_result["pivot_deltas"].append(delta)

        results.append(q_result)

    return results


def compute_rp_index(q_result):
    """Compute RP index for a quartile if possible."""
    if q_result["rupture_deltas"] and q_result["pivot_deltas"]:
        return np.mean(q_result["rupture_deltas"]) - np.mean(q_result["pivot_deltas"])
    return None


def main():
    corpus = load_corpus()

    # Per-quartile aggregation
    quartile_aggs = [
        defaultdict(list) for _ in range(4)
    ]
    era_quartile_s2 = defaultdict(lambda: [[] for _ in range(4)])
    era_quartile_entropy = defaultdict(lambda: [[] for _ in range(4)])
    era_quartile_rp = defaultdict(lambda: [[] for _ in range(4)])

    poem_results = []
    skipped = 0

    for poem in corpus:
        meta = poem["metadata"]
        lang = meta.get("language", "en")
        if lang != "en":
            continue

        clean_tokens = get_clean_tokens(poem)
        if len(clean_tokens) < MIN_CLEAN_TOKENS:
            skipped += 1
            continue

        quartiles = quartile_stats(clean_tokens)
        if quartiles is None:
            skipped += 1
            continue

        era = meta.get("era", "unknown")
        author = meta.get("author", "Unknown")
        title = meta.get("title", "Unknown")

        for q_idx, q_data in enumerate(quartiles):
            quartile_aggs[q_idx]["mean_s2"].append(q_data["mean_s2"])
            quartile_aggs[q_idx]["mean_entropy"].append(q_data["mean_entropy"])
            quartile_aggs[q_idx]["pos_s2_frac"].append(q_data["pos_s2_frac"])
            quartile_aggs[q_idx]["s2_budget"].append(q_data["s2_budget"])

            rp = compute_rp_index(q_data)
            if rp is not None:
                quartile_aggs[q_idx]["rp_index"].append(rp)
                era_quartile_rp[era][q_idx].append(rp)

            era_quartile_s2[era][q_idx].append(q_data["mean_s2"])
            era_quartile_entropy[era][q_idx].append(q_data["mean_entropy"])

        # Poem-level arc profile
        poem_arc = {
            "title": title,
            "author": author,
            "era": era,
            "n_clean": len(clean_tokens),
        }
        for q_idx, q_data in enumerate(quartiles):
            poem_arc[f"q{q_idx+1}_mean_s2"] = q_data["mean_s2"]
            poem_arc[f"q{q_idx+1}_mean_entropy"] = q_data["mean_entropy"]
            poem_arc[f"q{q_idx+1}_pos_frac"] = q_data["pos_s2_frac"]

        # Compute arc direction: Q4 mean_s2 - Q1 mean_s2
        poem_arc["s2_arc"] = quartiles[3]["mean_s2"] - quartiles[0]["mean_s2"]
        poem_arc["entropy_arc"] = quartiles[3]["mean_entropy"] - quartiles[0]["mean_entropy"]
        poem_results.append(poem_arc)

    # --- Global quartile summary ---
    print(f"\nAnalyzed: {len(poem_results)} poems (skipped {skipped})")
    print(f"\n{'='*60}")
    print("GLOBAL QUARTILE PROFILES")
    print(f"{'='*60}")
    print(f"{'Quartile':<10} {'Mean S2':>10} {'Mean H':>10} {'Pos S2%':>10} {'RP Index':>12} {'n':>6}")
    print(f"{'-'*60}")

    q_labels = ["Q1 (begin)", "Q2 (e.mid)", "Q3 (l.mid)", "Q4 (end)"]
    for q_idx, label in enumerate(q_labels):
        agg = quartile_aggs[q_idx]
        mean_s2 = np.mean(agg["mean_s2"])
        mean_ent = np.mean(agg["mean_entropy"])
        pos_frac = np.mean(agg["pos_s2_frac"])
        n_rp = len(agg["rp_index"])
        rp = np.mean(agg["rp_index"]) if n_rp > 0 else float('nan')
        n = len(agg["mean_s2"])
        print(f"{label:<10} {mean_s2:>+10.4f} {mean_ent:>10.4f} {pos_frac:>9.1%} {rp:>+12.4f} {n:>6}")

    # --- S2 arc direction ---
    s2_arcs = [p["s2_arc"] for p in poem_results]
    print(f"\n{'='*60}")
    print("S2 ARC DISTRIBUTION (Q4 mean S2 - Q1 mean S2)")
    print(f"{'='*60}")
    print(f"  Mean arc:    {np.mean(s2_arcs):+.4f}")
    print(f"  Median arc:  {np.median(s2_arcs):+.4f}")
    print(f"  Front-loaded (negative arc): {np.mean([1 if a < 0 else 0 for a in s2_arcs]):.1%}")
    print(f"  Back-loaded  (positive arc): {np.mean([1 if a > 0 else 0 for a in s2_arcs]):.1%}")
    print(f"  Flat (|arc| < 0.3):          {np.mean([1 if abs(a) < 0.3 else 0 for a in s2_arcs]):.1%}")

    # --- Entropy arc direction ---
    ent_arcs = [p["entropy_arc"] for p in poem_results]
    print(f"\nEntropy arc (Q4 - Q1):")
    print(f"  Mean: {np.mean(ent_arcs):+.4f}  Median: {np.median(ent_arcs):+.4f}")

    # --- Era-level arc analysis ---
    print(f"\n{'='*60}")
    print("ERA-LEVEL QUARTILE PROFILES (eras with ≥5 poems)")
    print(f"{'='*60}")
    print(f"{'Era':<20} {'Q1 S2':>8} {'Q2 S2':>8} {'Q3 S2':>8} {'Q4 S2':>8} {'Arc':>8} {'n':>5}")
    print(f"{'-'*63}")

    era_rows = []
    for era, q_s2_lists in era_quartile_s2.items():
        ns = [len(q) for q in q_s2_lists]
        if min(ns) < 5:
            continue
        q_means = [np.mean(q) for q in q_s2_lists]
        arc = q_means[3] - q_means[0]
        era_rows.append((era, q_means, arc, min(ns)))

    era_rows.sort(key=lambda x: x[2])  # Sort by arc (most negative = most front-loaded)
    for era, q_means, arc, n in era_rows:
        print(f"{era:<20} {q_means[0]:>+8.3f} {q_means[1]:>+8.3f} {q_means[2]:>+8.3f} {q_means[3]:>+8.3f} {arc:>+8.3f} {n:>5}")

    # --- Extreme front-loaded / back-loaded poems ---
    poem_results.sort(key=lambda p: p["s2_arc"])
    print(f"\n{'='*60}")
    print("MOST FRONT-LOADED POEMS (S2 declines from Q1 to Q4)")
    print(f"{'='*60}")
    for p in poem_results[:8]:
        print(f"  Arc={p['s2_arc']:+.3f}  {p['author'][:25]}: {p['title'][:40]}")

    print(f"\n{'='*60}")
    print("MOST BACK-LOADED POEMS (S2 builds from Q1 to Q4)")
    print(f"{'='*60}")
    for p in sorted(poem_results, key=lambda p: p["s2_arc"], reverse=True)[:8]:
        print(f"  Arc={p['s2_arc']:+.3f}  {p['author'][:25]}: {p['title'][:40]}")

    # --- Save results ---
    output = {
        "n_analyzed": len(poem_results),
        "global_quartile_means": {},
        "poem_arcs": poem_results,
        "era_quartile_summary": {},
    }
    for q_idx, label in enumerate(["Q1", "Q2", "Q3", "Q4"]):
        agg = quartile_aggs[q_idx]
        output["global_quartile_means"][label] = {
            "mean_s2": float(np.mean(agg["mean_s2"])),
            "mean_entropy": float(np.mean(agg["mean_entropy"])),
            "pos_s2_frac": float(np.mean(agg["pos_s2_frac"])),
            "rp_index": float(np.mean(agg["rp_index"])) if agg["rp_index"] else None,
            "n_poems": len(agg["mean_s2"]),
        }
    for era, q_s2_lists in era_quartile_s2.items():
        if min(len(q) for q in q_s2_lists) >= 3:
            output["era_quartile_summary"][era] = {
                f"Q{q+1}_mean_s2": float(np.mean(q_s2_lists[q])) if q_s2_lists[q] else None
                for q in range(4)
            }
            output["era_quartile_summary"][era]["arc"] = (
                float(np.mean(q_s2_lists[3]) - np.mean(q_s2_lists[0]))
                if q_s2_lists[0] and q_s2_lists[3] else None
            )
            output["era_quartile_summary"][era]["n"] = min(len(q) for q in q_s2_lists)

    with open("results/s2_arc_within_poem.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to results/s2_arc_within_poem.json")
    return output


if __name__ == "__main__":
    main()
