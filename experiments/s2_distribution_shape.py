"""
S2 Distribution Shape Analysis
===============================
Beyond mean S2: examining variance, skewness, kurtosis, and spike concentration
as poetic signatures. The hypothesis: poets differ not just in HOW surprising
their choices are on average, but in HOW they distribute that surprise.

Two archetypes:
  - "Sniper" poet: low spike rate, but extreme S2 when they fire (high kurtosis)
  - "Spreader" poet: many moderate surprises, low kurtosis

This maps onto aesthetic strategies: concentrated vs. distributed defamiliarization.
"""

import json
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

def compute_distribution_stats(s2_values):
    if len(s2_values) < 4:
        return None

    n = len(s2_values)
    mean = statistics.mean(s2_values)
    std = statistics.stdev(s2_values) if n > 1 else 0

    if std == 0:
        return None

    # Skewness (Fisher-Pearson)
    skewness = sum((x - mean)**3 for x in s2_values) / (n * std**3)
    # Excess kurtosis
    kurtosis = sum((x - mean)**4 for x in s2_values) / (n * std**4) - 3

    # Spike concentration: what fraction of cumulative positive S2 comes from
    # top 10% of tokens (by S2 value)?
    sorted_s2 = sorted(s2_values, reverse=True)
    top10_n = max(1, n // 10)
    top10_sum = sum(x for x in sorted_s2[:top10_n] if x > 0)
    total_pos_s2 = sum(x for x in s2_values if x > 0)
    spike_concentration = top10_sum / total_pos_s2 if total_pos_s2 > 0 else 0

    # Spike rate: proportion of tokens with S2 > 2 nats
    spike_rate = sum(1 for x in s2_values if x > 2) / n

    # Negative S2 depth: mean of negative S2 (how conformist are the conformist moments?)
    neg_s2 = [x for x in s2_values if x < 0]
    neg_depth = statistics.mean(neg_s2) if neg_s2 else 0

    # "Dynamic range": 95th percentile minus 5th percentile
    sorted_all = sorted(s2_values)
    p5 = sorted_all[int(0.05 * n)]
    p95 = sorted_all[int(0.95 * n)]
    dynamic_range = p95 - p5

    return {
        "n_tokens": n,
        "mean_s2": round(mean, 3),
        "std_s2": round(std, 3),
        "skewness": round(skewness, 3),
        "kurtosis": round(kurtosis, 3),
        "spike_concentration": round(spike_concentration, 3),
        "spike_rate": round(spike_rate, 3),
        "neg_depth": round(neg_depth, 3),
        "dynamic_range": round(dynamic_range, 3),
    }

def classify_poet_style(stats):
    """Classify into distribution archetypes."""
    k = stats["kurtosis"]
    spike_rate = stats["spike_rate"]
    conc = stats["spike_concentration"]

    if k > 3 and spike_rate < 0.15:
        return "Sniper (rare extreme spikes)"
    elif k < 0 and spike_rate > 0.2:
        return "Spreader (many moderate surprises)"
    elif conc > 0.6 and spike_rate < 0.2:
        return "Concentrated (few moments carry all the surprise)"
    elif stats["mean_s2"] < 0:
        return "Conformist (follows expectation)"
    else:
        return "Balanced"

def main():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Per-poem analysis
    poem_stats = []
    for poem in corpus:
        meta = poem["metadata"]
        tokens = poem["tokens"]
        s2_vals = [t["s2"] for t in tokens if "s2" in t]

        stats = compute_distribution_stats(s2_vals)
        if stats is None:
            continue

        stats["title"] = meta.get("title", "Unknown")
        stats["author"] = meta.get("author", "Unknown")
        stats["genre"] = meta.get("genre", "unknown")
        stats["style"] = classify_poet_style(stats)
        poem_stats.append(stats)

    # ── Per-author aggregation ────────────────────────────────────────────────
    author_data = defaultdict(list)
    for p in poem_stats:
        author_data[p["author"]].append(p)

    author_profiles = {}
    for author, poems in author_data.items():
        if len(poems) < 2:
            continue
        author_profiles[author] = {
            "n_poems": len(poems),
            "mean_s2": round(statistics.mean(p["mean_s2"] for p in poems), 3),
            "mean_std": round(statistics.mean(p["std_s2"] for p in poems), 3),
            "mean_kurtosis": round(statistics.mean(p["kurtosis"] for p in poems), 3),
            "mean_skewness": round(statistics.mean(p["skewness"] for p in poems), 3),
            "mean_spike_rate": round(statistics.mean(p["spike_rate"] for p in poems), 3),
            "mean_concentration": round(statistics.mean(p["spike_concentration"] for p in poems), 3),
            "mean_dynamic_range": round(statistics.mean(p["dynamic_range"] for p in poems), 3),
        }

    # ── Genre aggregation ─────────────────────────────────────────────────────
    genre_data = defaultdict(list)
    for p in poem_stats:
        genre_data[p["genre"]].append(p)

    genre_profiles = {}
    for genre, poems in genre_data.items():
        if len(poems) < 2:
            continue
        genre_profiles[genre] = {
            "n_poems": len(poems),
            "mean_s2": round(statistics.mean(p["mean_s2"] for p in poems), 3),
            "mean_kurtosis": round(statistics.mean(p["kurtosis"] for p in poems), 3),
            "mean_spike_rate": round(statistics.mean(p["spike_rate"] for p in poems), 3),
            "mean_concentration": round(statistics.mean(p["spike_concentration"] for p in poems), 3),
            "mean_dynamic_range": round(statistics.mean(p["dynamic_range"] for p in poems), 3),
        }

    # ── Extreme poems ─────────────────────────────────────────────────────────
    by_kurtosis = sorted(poem_stats, key=lambda x: x["kurtosis"], reverse=True)
    by_concentration = sorted(poem_stats, key=lambda x: x["spike_concentration"], reverse=True)
    by_dynamic_range = sorted(poem_stats, key=lambda x: x["dynamic_range"], reverse=True)
    by_spike_rate = sorted(poem_stats, key=lambda x: x["spike_rate"], reverse=True)

    return {
        "poem_stats": poem_stats,
        "author_profiles": author_profiles,
        "genre_profiles": genre_profiles,
        "top_kurtosis": by_kurtosis[:10],
        "top_concentration": by_concentration[:10],
        "top_dynamic_range": by_dynamic_range[:10],
        "top_spike_rate": by_spike_rate[:10],
        "bottom_kurtosis": by_kurtosis[-10:],
    }

if __name__ == "__main__":
    results = main()
    print(json.dumps(results, indent=2))
