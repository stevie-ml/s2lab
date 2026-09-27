"""
Within-Poem Type Dynamics: The 2×2 Arc Across a Poem's Arc

Using the 2×2 taxonomy from surprise_taxonomy_2x2.py, this experiment asks:
Do poems shift between Type I (Definite Straussian Gap) and Type III
(Confirmed Prediction) as they progress from beginning → middle → end?

If poems build expectation early (high Type III) to spend it at the end
(high Type I), this would be a quantitative signature of the volta structure
in a broad sense — applicable beyond sonnets.

Method:
  - Divide each poem's tokens into thirds by position (1st third / 2nd / 3rd)
  - Classify each token via the 2×2 taxonomy (same thresholds as prior work)
  - Compute Type I%, Type III%, I−III contrast for each third
  - Aggregate across poems and eras
  - Identify individual poems with the most dramatic arc

Hypothesis: across all poetry, Type I% increases and Type III% decreases from
beginning to end — poets spend their conformity budget early, then deviate.
"""

import json
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
RANK_THRESHOLD = 10   # top-10 = "expected"
MIN_TOKENS = 30       # minimum artifact-free tokens to include a poem


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    top = alts[0]
    return top["token"] in ("\n", "\r\n", "\r") and top["prob"] >= 0.9


def classify_token(tok, entropy_median):
    if is_artifact(tok):
        return None
    h = tok["entropy"]
    rank = tok.get("rank", 9999)
    low_entropy = h < entropy_median
    expected = rank <= RANK_THRESHOLD
    if low_entropy and not expected:
        return "I"
    elif not low_entropy and not expected:
        return "II"
    elif low_entropy and expected:
        return "III"
    else:
        return "IV"


def type_stats(type_list):
    """Return dict of type→count and derived ratios."""
    counts = defaultdict(int)
    for t in type_list:
        counts[t] += 1
    total = sum(counts.values())
    if total == 0:
        return None
    pct_I   = counts["I"]   / total
    pct_III = counts["III"] / total
    contrast = pct_I - pct_III
    return {
        "n": total,
        "I":   round(pct_I * 100, 1),
        "II":  round(counts["II"] / total * 100, 1),
        "III": round(pct_III * 100, 1),
        "IV":  round(counts["IV"] / total * 100, 1),
        "contrast": round(contrast, 4),
    }


def run():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Step 1: compute corpus entropy median (for threshold)
    all_entropies = []
    for poem in data:
        for tok in poem["tokens"]:
            if not is_artifact(tok) and tok["entropy"] > 0:
                all_entropies.append(tok["entropy"])
    entropy_median = statistics.median(all_entropies)
    print(f"Corpus entropy median: {entropy_median:.3f} bits")
    print(f"Total poems: {len(data)}")

    # Step 2: classify tokens per poem, split into thirds
    poem_arcs = []
    skipped = 0
    for poem in data:
        meta = poem["metadata"]
        # Classify non-artifact tokens
        classified = []
        for tok in poem["tokens"]:
            qtype = classify_token(tok, entropy_median)
            if qtype is not None:
                classified.append((tok["position"], qtype))

        if len(classified) < MIN_TOKENS:
            skipped += 1
            continue

        # Split into thirds by position
        n = len(classified)
        t1 = classified[:n // 3]
        t2 = classified[n // 3: 2 * n // 3]
        t3 = classified[2 * n // 3:]

        s1 = type_stats([t for _, t in t1])
        s2 = type_stats([t for _, t in t2])
        s3 = type_stats([t for _, t in t3])

        if s1 and s2 and s3:
            poem_arcs.append({
                "title":  meta["title"],
                "author": meta.get("author", "Unknown"),
                "era":    meta.get("era", "unknown"),
                "year":   meta.get("year"),
                "n":      n,
                "first":  s1,
                "middle": s2,
                "last":   s3,
                "arc_I":  round(s3["I"] - s1["I"], 2),       # change in Type I% first→last
                "arc_III": round(s3["III"] - s1["III"], 2),   # change in Type III%
                "arc_contrast": round(s3["contrast"] - s1["contrast"], 4),  # change in I-III
            })

    print(f"Poems included: {len(poem_arcs)}, skipped (< {MIN_TOKENS} tokens): {skipped}")

    # Step 3: corpus-level arc
    print("\n--- Corpus-Level Arc (all poetry, artifact-free) ---")
    thirds = ["first", "middle", "last"]
    labels = ["1st third", "2nd third", "3rd third"]

    # Aggregate across all poems
    for third_key, label in zip(thirds, labels):
        all_I   = [p[third_key]["I"]   for p in poem_arcs]
        all_III = [p[third_key]["III"] for p in poem_arcs]
        all_contrast = [p[third_key]["contrast"] for p in poem_arcs]
        print(f"  {label}: Type I={statistics.mean(all_I):.1f}%  "
              f"Type III={statistics.mean(all_III):.1f}%  "
              f"I−III contrast={statistics.mean(all_contrast):.3f}")

    # Step 4: per-era arc
    print("\n--- Per-Era Arc (avg Type I% by third) ---")
    era_arcs = defaultdict(list)
    for p in poem_arcs:
        era_arcs[p["era"]].append(p)

    era_rows = []
    for era, poems in era_arcs.items():
        if len(poems) < 2:
            continue
        avg_I_first  = statistics.mean(p["first"]["I"]  for p in poems)
        avg_I_last   = statistics.mean(p["last"]["I"]   for p in poems)
        avg_III_first = statistics.mean(p["first"]["III"] for p in poems)
        avg_III_last  = statistics.mean(p["last"]["III"]  for p in poems)
        avg_arc_I = statistics.mean(p["arc_I"] for p in poems)
        era_rows.append({
            "era": era,
            "n": len(poems),
            "I_first":  round(avg_I_first, 1),
            "I_last":   round(avg_I_last, 1),
            "III_first": round(avg_III_first, 1),
            "III_last":  round(avg_III_last, 1),
            "arc_I":     round(avg_arc_I, 2),
        })

    era_rows.sort(key=lambda r: -r["arc_I"])
    print(f"{'Era':<22} {'N':>4}  {'I_first':>8}  {'I_last':>7}  {'ΔI':>6}  {'III_first':>10}  {'III_last':>9}")
    for r in era_rows:
        print(f"  {r['era']:<20} {r['n']:>4}  {r['I_first']:>7.1f}%  {r['I_last']:>6.1f}%  "
              f"{r['arc_I']:>+6.1f}  {r['III_first']:>9.1f}%  {r['III_last']:>8.1f}%")

    # Step 5: top poems by arc_I (biggest increase in Type I toward end)
    print("\n--- Top 15 Poems: Largest ΔType I (first→last third) ---")
    sorted_arcs = sorted(poem_arcs, key=lambda p: -p["arc_I"])
    for p in sorted_arcs[:15]:
        print(f"  {p['arc_I']:>+5.1f}  [{p['first']['I']:>5.1f}%→{p['last']['I']:>5.1f}%]  "
              f"{p['author']}: '{p['title']}'  ({p['era']}, n={p['n']})")

    # Step 6: top poems by arc_III (biggest decrease in Type III toward end)
    print("\n--- Top 15 Poems: Largest ΔType III (first→last third, most negative = most buildup-release) ---")
    sorted_arcs_III = sorted(poem_arcs, key=lambda p: p["arc_III"])
    for p in sorted_arcs_III[:15]:
        print(f"  {p['arc_III']:>+6.1f}  [{p['first']['III']:>5.1f}%→{p['last']['III']:>5.1f}%]  "
              f"{p['author']}: '{p['title']}'  ({p['era']}, n={p['n']})")

    # Step 7: arc_contrast distribution — is the mean significantly positive?
    arc_contrasts = [p["arc_contrast"] for p in poem_arcs]
    mean_arc = statistics.mean(arc_contrasts)
    stdev_arc = statistics.stdev(arc_contrasts)
    positive = sum(1 for x in arc_contrasts if x > 0)
    print(f"\n--- Arc Contrast (I−III change, first→last third) ---")
    print(f"  Mean ΔContrast: {mean_arc:+.4f}  Stdev: {stdev_arc:.4f}")
    print(f"  Poems where Type I % increases (arc_contrast > 0): {positive}/{len(poem_arcs)} = {100*positive/len(poem_arcs):.1f}%")

    # Step 8: return structured results for the findings file
    return {
        "entropy_median": entropy_median,
        "n_poems": len(poem_arcs),
        "corpus_arc": {
            third_key: {
                "I":   round(statistics.mean(p[third_key]["I"]   for p in poem_arcs), 2),
                "III": round(statistics.mean(p[third_key]["III"] for p in poem_arcs), 2),
                "contrast": round(statistics.mean(p[third_key]["contrast"] for p in poem_arcs), 4),
            }
            for third_key in thirds
        },
        "era_rows": era_rows,
        "top_arc_poems": [
            {"title": p["title"], "author": p["author"], "era": p["era"],
             "arc_I": p["arc_I"], "first_I": p["first"]["I"], "last_I": p["last"]["I"],
             "first_III": p["first"]["III"], "last_III": p["last"]["III"]}
            for p in sorted_arcs[:15]
        ],
        "arc_contrast_mean": round(mean_arc, 4),
        "arc_contrast_stdev": round(stdev_arc, 4),
        "pct_increasing": round(100 * positive / len(poem_arcs), 1),
    }


if __name__ == "__main__":
    results = run()
