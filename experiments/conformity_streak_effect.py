"""
Conformity Streak Before Surprise: The Spring-Tension Model

Hypothesis: The longer a poet maintains model-conforming tokens (low S2) before
a surprise spike, the larger the spike when it comes. Like compressing a spring —
the longer the wind-up of conformity, the bigger the release.

We define a "conformity streak" as consecutive tokens with S2 < threshold
immediately preceding a high-S2 spike.

Extends pre_peak_setup.md (which looked at the 8-token window average) by measuring
exact run lengths and testing the correlation with spike height.
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/conformity_streak_effect.json"

SPIKE_THRESHOLD = 2.0        # S2 >= 2.0 to qualify as a spike
CONFORMITY_THRESHOLD = 0.5   # S2 < 0.5 to count as "conforming"
NEWLINE_THRESHOLD = 0.9      # exclude structural newline positions


def compute_streaks_for_poem(tokens):
    """For each spike in a poem, compute the conformity streak length before it."""
    # Filter artifact positions
    clean = [t for t in tokens if t.get("p_newline", 0) < NEWLINE_THRESHOLD]
    if len(clean) < 3:
        return []

    s2_values = [t["s2"] for t in clean]
    results = []

    for i, tok in enumerate(clean):
        if tok["s2"] < SPIKE_THRESHOLD:
            continue

        # Walk backward counting consecutive conforming tokens
        streak = 0
        j = i - 1
        while j >= 0 and clean[j]["s2"] < CONFORMITY_THRESHOLD:
            streak += 1
            j -= 1

        # Also record the token before the streak (what ended the last spike)
        pre_streak_s2 = clean[j]["s2"] if j >= 0 else None

        results.append({
            "token": tok["token"],
            "s2": tok["s2"],
            "surprisal": tok["surprisal"],
            "entropy": tok["entropy"],
            "streak_length": streak,
            "pre_streak_s2": pre_streak_s2,
            "position": tok["position"],
        })

    return results


def bin_analysis(all_spikes):
    """Group spikes by streak length bucket and compute mean S2."""
    buckets = defaultdict(list)
    for sp in all_spikes:
        sl = sp["streak_length"]
        if sl == 0:
            bucket = "0"
        elif sl == 1:
            bucket = "1"
        elif sl <= 3:
            bucket = "2-3"
        elif sl <= 6:
            bucket = "4-6"
        elif sl <= 10:
            bucket = "7-10"
        else:
            bucket = "11+"
        buckets[bucket].append(sp["s2"])

    order = ["0", "1", "2-3", "4-6", "7-10", "11+"]
    table = []
    for b in order:
        vals = buckets[b]
        if not vals:
            continue
        mean_s2 = sum(vals) / len(vals)
        table.append({
            "bucket": b,
            "count": len(vals),
            "mean_s2": round(mean_s2, 3),
            "median_s2": round(sorted(vals)[len(vals) // 2], 3),
            "max_s2": round(max(vals), 3),
        })
    return table


def correlation(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    if sx == 0 or sy == 0:
        return 0.0
    return cov / (sx * sy)


def main():
    with open(CORPUS_PATH) as f:
        data = json.load(f)

    all_spikes = []
    poem_profiles = []

    for poem in data:
        meta = poem.get("metadata", {})
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        spikes = compute_streaks_for_poem(tokens)
        all_spikes.extend(spikes)

        if spikes:
            avg_streak = sum(s["streak_length"] for s in spikes) / len(spikes)
            avg_s2 = sum(s["s2"] for s in spikes) / len(spikes)
            long_plateau_spikes = sum(1 for s in spikes if s["streak_length"] >= 5)
            poem_profiles.append({
                "title": meta.get("title", "Unknown"),
                "author": meta.get("author", "Unknown"),
                "era": meta.get("era", "unknown"),
                "n_spikes": len(spikes),
                "avg_streak": round(avg_streak, 2),
                "avg_spike_s2": round(avg_s2, 3),
                "long_plateau_pct": round(long_plateau_spikes / len(spikes), 3),
                "max_streak": max(s["streak_length"] for s in spikes),
            })

    # Overall stats
    total_spikes = len(all_spikes)
    streak_lengths = [s["streak_length"] for s in all_spikes]
    spike_s2s = [s["s2"] for s in all_spikes]

    r = correlation(streak_lengths, spike_s2s)

    # Bin table
    bin_table = bin_analysis(all_spikes)

    # Long-plateau examples (streak >= 10)
    long_plateau_examples = sorted(
        [s for s in all_spikes if s["streak_length"] >= 10],
        key=lambda x: -x["s2"]
    )[:20]

    # Zero-streak examples (immediate spike after another spike)
    zero_streak_examples = sorted(
        [s for s in all_spikes if s["streak_length"] == 0],
        key=lambda x: -x["s2"]
    )[:15]

    # Poem-level: does avg_streak predict avg_spike_s2?
    if poem_profiles:
        poem_streaks = [p["avg_streak"] for p in poem_profiles]
        poem_s2s = [p["avg_spike_s2"] for p in poem_profiles]
        poem_r = correlation(poem_streaks, poem_s2s)
    else:
        poem_r = 0.0

    # Era breakdown
    era_groups = defaultdict(list)
    for p in poem_profiles:
        era_groups[p["era"]].append(p)

    era_table = []
    for era, poems in sorted(era_groups.items()):
        avg_streak = sum(p["avg_streak"] for p in poems) / len(poems)
        avg_s2 = sum(p["avg_spike_s2"] for p in poems) / len(poems)
        era_table.append({
            "era": era,
            "n_poems": len(poems),
            "avg_streak": round(avg_streak, 2),
            "avg_spike_s2": round(avg_s2, 3),
        })

    # Top "spring tension" poems (highest avg_streak × avg_spike_s2)
    for p in poem_profiles:
        p["tension_score"] = round(p["avg_streak"] * p["avg_spike_s2"], 3)
    top_tension = sorted(poem_profiles, key=lambda x: -x["tension_score"])[:15]

    result = {
        "total_spikes_analyzed": total_spikes,
        "total_poems": len(poem_profiles),
        "overall_correlation_streak_vs_s2": round(r, 4),
        "poem_level_correlation": round(poem_r, 4),
        "streak_distribution": {
            "mean_streak": round(sum(streak_lengths) / len(streak_lengths), 2) if streak_lengths else 0,
            "pct_zero_streak": round(sum(1 for s in streak_lengths if s == 0) / len(streak_lengths), 3),
            "pct_1_streak": round(sum(1 for s in streak_lengths if s == 1) / len(streak_lengths), 3),
            "pct_5plus_streak": round(sum(1 for s in streak_lengths if s >= 5) / len(streak_lengths), 3),
            "pct_10plus_streak": round(sum(1 for s in streak_lengths if s >= 10) / len(streak_lengths), 3),
            "max_streak": max(streak_lengths) if streak_lengths else 0,
        },
        "bin_table": bin_table,
        "era_breakdown": era_table,
        "top_tension_poems": top_tension,
        "long_plateau_examples": long_plateau_examples,
        "zero_streak_examples": zero_streak_examples,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Done. Analyzed {total_spikes} spikes across {len(poem_profiles)} poems.")
    print(f"Overall correlation (streak_length vs spike_s2): r = {r:.4f}")
    print(f"Poem-level correlation: r = {poem_r:.4f}")
    print("\nBin table:")
    for row in bin_table:
        print(f"  Streak {row['bucket']:>5}: n={row['count']:>5}, mean_s2={row['mean_s2']:.3f}")


if __name__ == "__main__":
    main()
