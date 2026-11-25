"""
Alternative Space Volatility: How stable is GPT-2's prediction window
across consecutive token positions within a poem?

For each consecutive pair of tokens (t, t+1), compute Jaccard similarity
between their top-10 alternative sets. High similarity = model stays in a
stable vocabulary "groove". Low similarity = volatile, rapidly shifting
prediction space.

Questions:
1. Does prediction-space volatility correlate with S2 at position t+1?
   (Do high-S2 moments tend to follow volatile prediction spaces, or stable ones?)
2. Do different eras maintain different levels of prediction-space stability?
3. Within a poem, how does volatility evolve? (Does the model "settle in"?)
4. Do high-avg-S2 poets produce more volatile prediction spaces?
"""

import json
import statistics
from collections import defaultdict

CORPUS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/alternative_space_volatility.json"
ARTIFACT_THRESHOLD = 0.90  # p_newline threshold
MIN_TOKENS_FOR_POEM = 15


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def run():
    with open(CORPUS_FILE) as f:
        corpus = json.load(f)

    # Per-poem volatility records
    poem_stats = []

    # Token-level records: (jaccard_with_prev, s2, era, author)
    token_records = []

    # Era-level aggregates
    era_records = defaultdict(list)
    poet_records = defaultdict(list)

    for poem in corpus:
        era = poem["metadata"]["era"]
        author = poem["metadata"]["author"]

        # Filter to artifact-free, non-whitespace tokens
        tokens = [
            t for t in poem["tokens"]
            if t["p_newline"] < ARTIFACT_THRESHOLD
            and t["token"].strip() not in ("", "\n", "\r")
        ]

        if len(tokens) < MIN_TOKENS_FOR_POEM:
            continue

        # Build alternative sets for each token
        alt_sets = []
        for tok in tokens:
            alt_tokens = frozenset(a["token"].strip().lower() for a in tok["alternatives"])
            alt_sets.append(alt_tokens)

        # Compute Jaccard between consecutive positions
        jacc_values = []
        for i in range(1, len(tokens)):
            j = jaccard(alt_sets[i - 1], alt_sets[i])
            jacc_values.append(j)
            s2 = tokens[i]["s2"]
            entropy = tokens[i]["entropy"]
            pos_frac = i / len(tokens)

            rec = {
                "jaccard": j,
                "s2": s2,
                "entropy": entropy,
                "pos_frac": pos_frac,
                "era": era,
                "author": author,
            }
            token_records.append(rec)
            era_records[era].append(rec)
            poet_records[author].append(rec)

        avg_jacc = statistics.mean(jacc_values)
        std_jacc = statistics.stdev(jacc_values) if len(jacc_values) > 1 else 0.0
        avg_s2 = statistics.mean(t["s2"] for t in tokens)

        poem_stats.append({
            "title": poem["metadata"]["title"],
            "author": author,
            "era": era,
            "n_tokens": len(tokens),
            "avg_jaccard": round(avg_jacc, 4),
            "std_jaccard": round(std_jacc, 4),
            "avg_s2": round(avg_s2, 4),
        })

    print(f"Processed {len(poem_stats)} poems, {len(token_records)} token transitions")

    # 1. Jaccard vs S2 bins
    s2_bins = [
        ("Very low (<-3)", float("-inf"), -3),
        ("Low (-3 to -1)", -3, -1),
        ("Neutral (-1 to 1)", -1, 1),
        ("High (1 to 3)", 1, 3),
        ("Very high (3-5)", 3, 5),
        ("Extreme (5+)", 5, float("inf")),
    ]

    s2_bin_stats = []
    for name, lo, hi in s2_bins:
        recs = [r for r in token_records if lo < r["s2"] <= hi]
        if not recs:
            continue
        jacc_vals = [r["jaccard"] for r in recs]
        s2_bin_stats.append({
            "band": name,
            "n": len(recs),
            "mean_jaccard": round(statistics.mean(jacc_vals), 4),
            "median_jaccard": round(statistics.median(jacc_vals), 4),
        })

    # 2. Era-level volatility profile
    era_stats = {}
    for era, recs in era_records.items():
        if len(recs) < 20:
            continue
        jacc_vals = [r["jaccard"] for r in recs]
        s2_vals = [r["s2"] for r in recs]
        era_stats[era] = {
            "n": len(recs),
            "mean_jaccard": round(statistics.mean(jacc_vals), 4),
            "mean_s2": round(statistics.mean(s2_vals), 4),
            "pct_stable": round(sum(1 for j in jacc_vals if j > 0.3) / len(jacc_vals), 4),
            "pct_volatile": round(sum(1 for j in jacc_vals if j == 0.0) / len(jacc_vals), 4),
        }

    # 3. Within-poem positional profile (how volatility evolves)
    # Bin by poem position fraction [0..1) in 10 deciles
    pos_decile_jacc = defaultdict(list)
    pos_decile_s2 = defaultdict(list)
    for r in token_records:
        decile = min(int(r["pos_frac"] * 10), 9)
        pos_decile_jacc[decile].append(r["jaccard"])
        pos_decile_s2[decile].append(r["s2"])

    positional_profile = []
    for d in range(10):
        jacc_vals = pos_decile_jacc[d]
        s2_vals = pos_decile_s2[d]
        positional_profile.append({
            "decile": d,
            "n": len(jacc_vals),
            "mean_jaccard": round(statistics.mean(jacc_vals), 4) if jacc_vals else 0,
            "mean_s2": round(statistics.mean(s2_vals), 4) if s2_vals else 0,
        })

    # 4. Poet-level: avg jaccard vs avg s2 (poets with ≥50 transitions)
    poet_stats = {}
    for author, recs in poet_records.items():
        if len(recs) < 50:
            continue
        jacc_vals = [r["jaccard"] for r in recs]
        s2_vals = [r["s2"] for r in recs]
        poet_stats[author] = {
            "n": len(recs),
            "mean_jaccard": round(statistics.mean(jacc_vals), 4),
            "mean_s2": round(statistics.mean(s2_vals), 4),
            "pct_stable": round(sum(1 for j in jacc_vals if j > 0.3) / len(jacc_vals), 4),
        }

    # 5. Top/bottom poems by volatility
    poem_stats_sorted_by_jacc = sorted(poem_stats, key=lambda x: x["avg_jaccard"])
    most_volatile = poem_stats_sorted_by_jacc[:10]
    most_stable = poem_stats_sorted_by_jacc[-10:]

    # 6. Correlation between poem avg_jaccard and avg_s2
    if len(poem_stats) > 2:
        n = len(poem_stats)
        mean_j = statistics.mean(p["avg_jaccard"] for p in poem_stats)
        mean_s2 = statistics.mean(p["avg_s2"] for p in poem_stats)
        cov = sum((p["avg_jaccard"] - mean_j) * (p["avg_s2"] - mean_s2) for p in poem_stats) / n
        std_j = statistics.stdev(p["avg_jaccard"] for p in poem_stats)
        std_s2 = statistics.stdev(p["avg_s2"] for p in poem_stats)
        poem_level_r = round(cov / (std_j * std_s2), 4) if std_j and std_s2 else 0.0
    else:
        poem_level_r = 0.0

    # 7. Token-level correlation: jaccard vs s2
    if len(token_records) > 2:
        n = len(token_records)
        mean_j = statistics.mean(r["jaccard"] for r in token_records)
        mean_s2 = statistics.mean(r["s2"] for r in token_records)
        cov = sum((r["jaccard"] - mean_j) * (r["s2"] - mean_s2) for r in token_records) / n
        std_j = statistics.stdev(r["jaccard"] for r in token_records)
        std_s2 = statistics.stdev(r["s2"] for r in token_records)
        token_level_r = round(cov / (std_j * std_s2), 4) if std_j and std_s2 else 0.0
    else:
        token_level_r = 0.0

    output = {
        "summary": {
            "n_poems": len(poem_stats),
            "n_transitions": len(token_records),
            "mean_jaccard_overall": round(statistics.mean(r["jaccard"] for r in token_records), 4),
            "pct_zero_overlap": round(sum(1 for r in token_records if r["jaccard"] == 0.0) / len(token_records), 4),
            "pct_full_overlap": round(sum(1 for r in token_records if r["jaccard"] == 1.0) / len(token_records), 4),
            "token_level_r_jaccard_vs_s2": token_level_r,
            "poem_level_r_jaccard_vs_s2": poem_level_r,
        },
        "s2_bin_stats": s2_bin_stats,
        "era_stats": era_stats,
        "positional_profile": positional_profile,
        "poet_stats": poet_stats,
        "most_volatile_poems": most_volatile,
        "most_stable_poems": most_stable,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Results saved to {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    result = run()

    print("\n=== SUMMARY ===")
    s = result["summary"]
    print(f"Poems: {s['n_poems']}, Transitions: {s['n_transitions']}")
    print(f"Mean Jaccard: {s['mean_jaccard_overall']}")
    print(f"Zero overlap %: {s['pct_zero_overlap']:.1%}")
    print(f"Token-level r(Jaccard, S2): {s['token_level_r_jaccard_vs_s2']}")
    print(f"Poem-level r(Jaccard, S2): {s['poem_level_r_jaccard_vs_s2']}")

    print("\n=== Jaccard by S2 Band ===")
    for b in result["s2_bin_stats"]:
        print(f"  {b['band']:25s}: mean Jaccard = {b['mean_jaccard']:.4f} (n={b['n']})")

    print("\n=== Top 5 Most Volatile Eras ===")
    era_sorted = sorted(result["era_stats"].items(), key=lambda x: x[1]["mean_jaccard"])
    for era, stats in era_sorted[:5]:
        print(f"  {era:25s}: Jaccard={stats['mean_jaccard']:.3f}, S2={stats['mean_s2']:.3f}, stable%={stats['pct_stable']:.2%}")

    print("\n=== Top 5 Most Stable Eras ===")
    for era, stats in era_sorted[-5:]:
        print(f"  {era:25s}: Jaccard={stats['mean_jaccard']:.3f}, S2={stats['mean_s2']:.3f}, stable%={stats['pct_stable']:.2%}")
