"""
Surprise Density: Run-Length Analysis of Conformist Intervals Between S2 Spikes
================================================================================
For each poem, identify 'spike' tokens (S2 above threshold) and measure
the gap (run length) between consecutive spikes.

New angle: the autocorrelation and Markov analyses describe *how much*
sequential structure surprise has. This experiment asks a more geometric
question: **how long are the 'quiet stretches' between moments of deviation?**

Key questions:
1. Do run lengths follow a geometric distribution (Bernoulli i.i.d. model)?
2. Do different eras have different mean run lengths (i.e., different 'surprise density')?
3. Does higher surprise density (shorter runs) correlate with modernist/experimental poetry?
4. Are 'burst' distributions (heavy-tailed runs with occasional very long silences)
   more common in formal poetry?
"""

import json
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "findings/spike_density_runlength.json"
ARTIFACT_THRESHOLD = 0.9
SPIKE_THRESHOLD = 0.5    # S2 > this = spike
MIN_TOKENS = 20
MIN_POEMS_FOR_ERA = 2


def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def get_clean_s2(poem):
    return [
        t["s2"]
        for t in poem["tokens"]
        if t.get("p_newline", 0) < ARTIFACT_THRESHOLD
    ]


def get_run_lengths(s2_seq, threshold=SPIKE_THRESHOLD):
    """
    Return list of inter-spike gap lengths.
    A 'gap' is the number of non-spike tokens between consecutive spikes.
    Also return: spike positions, spike density.
    """
    is_spike = [s > threshold for s in s2_seq]
    spike_positions = [i for i, v in enumerate(is_spike) if v]

    if len(spike_positions) < 2:
        return [], spike_positions, 0.0

    gaps = []
    for i in range(1, len(spike_positions)):
        gap = spike_positions[i] - spike_positions[i - 1] - 1
        gaps.append(gap)

    density = len(spike_positions) / len(s2_seq)
    return gaps, spike_positions, density


def geometric_fit_quality(gaps):
    """
    If gaps are geometrically distributed with parameter p,
    E[gap] = (1-p)/p.
    Fit p from the mean and compute log-likelihood ratio vs. geometric null.
    Returns (p_hat, deviation_score) where deviation_score > 0 means
    heavier-tailed than geometric.
    """
    if len(gaps) < 5:
        return None, None

    mean_gap = statistics.mean(gaps)
    if mean_gap <= 0:
        return None, None

    p_hat = 1.0 / (mean_gap + 1)

    # Fraction of 'long' gaps (> 3 * mean) — heavier than geometric expects
    expected_heavy = (1 - p_hat) ** int(3 * mean_gap + 1)
    actual_heavy = sum(1 for g in gaps if g > 3 * mean_gap) / len(gaps)
    deviation = actual_heavy - expected_heavy
    return p_hat, deviation


def run():
    data = load_data()

    era_results = defaultdict(lambda: {
        "poem_count": 0,
        "densities": [],
        "mean_gaps": [],
        "median_gaps": [],
        "all_gaps": [],
        "max_gaps": [],
        "p_hats": [],
        "heavy_tail_deviations": [],
        "burst_scores": [],
    })

    poet_results = defaultdict(lambda: {
        "era": "",
        "poem_count": 0,
        "densities": [],
        "mean_gaps": [],
    })

    poem_details = []

    for poem in data:
        meta = poem["metadata"]
        era = meta["era"]
        title = meta.get("title", "")
        author = meta.get("author", "unknown")

        s2_seq = get_clean_s2(poem)
        if len(s2_seq) < MIN_TOKENS:
            continue

        gaps, spikes, density = get_run_lengths(s2_seq, SPIKE_THRESHOLD)
        if len(gaps) < 3:
            continue

        mean_gap = statistics.mean(gaps)
        median_gap = statistics.median(gaps)
        max_gap = max(gaps)
        p_hat, heavy_dev = geometric_fit_quality(gaps)

        # Burstiness coefficient B = (sigma - mu) / (sigma + mu)
        # B = 0 → Poisson, B = 1 → maximally bursty, B = -1 → hyper-regular
        if len(gaps) >= 5:
            mu = statistics.mean(gaps)
            sigma = statistics.stdev(gaps)
            burst_score = (sigma - mu) / (sigma + mu) if (sigma + mu) > 0 else None
        else:
            burst_score = None

        poem_details.append({
            "title": title,
            "author": author,
            "era": era,
            "n_tokens": len(s2_seq),
            "n_spikes": len(spikes),
            "density": round(density, 4),
            "mean_gap": round(mean_gap, 2),
            "median_gap": round(median_gap, 2),
            "max_gap": max_gap,
            "p_hat": round(p_hat, 4) if p_hat else None,
            "heavy_tail_deviation": round(heavy_dev, 4) if heavy_dev is not None else None,
            "burst_score": round(burst_score, 4) if burst_score is not None else None,
        })

        era_results[era]["poem_count"] += 1
        era_results[era]["densities"].append(density)
        era_results[era]["mean_gaps"].append(mean_gap)
        era_results[era]["median_gaps"].append(median_gap)
        era_results[era]["all_gaps"].extend(gaps)
        era_results[era]["max_gaps"].append(max_gap)
        if p_hat is not None:
            era_results[era]["p_hats"].append(p_hat)
        if heavy_dev is not None:
            era_results[era]["heavy_tail_deviations"].append(heavy_dev)
        if burst_score is not None:
            era_results[era]["burst_scores"].append(burst_score)

        if era != "control":
            poet_results[author]["era"] = era
            poet_results[author]["poem_count"] += 1
            poet_results[author]["densities"].append(density)
            poet_results[author]["mean_gaps"].append(mean_gap)

    # Summarize era results
    era_summary = []
    for era, vals in era_results.items():
        n = vals["poem_count"]
        if n < MIN_POEMS_FOR_ERA:
            continue
        era_summary.append({
            "era": era,
            "n": n,
            "mean_density": round(statistics.mean(vals["densities"]), 4),
            "mean_mean_gap": round(statistics.mean(vals["mean_gaps"]), 2),
            "mean_median_gap": round(statistics.mean(vals["median_gaps"]), 2),
            "global_mean_gap": round(statistics.mean(vals["all_gaps"]), 2),
            "mean_max_gap": round(statistics.mean(vals["max_gaps"]), 1),
            "mean_burst_score": round(statistics.mean(vals["burst_scores"]), 4) if vals["burst_scores"] else None,
            "mean_heavy_tail": round(statistics.mean(vals["heavy_tail_deviations"]), 4) if vals["heavy_tail_deviations"] else None,
        })

    era_summary.sort(key=lambda x: x["mean_density"], reverse=True)

    # Summarize poet results
    poet_summary = []
    for poet, vals in poet_results.items():
        if vals["poem_count"] < 2:
            continue
        poet_summary.append({
            "poet": poet,
            "era": vals["era"],
            "n": vals["poem_count"],
            "mean_density": round(statistics.mean(vals["densities"]), 4),
            "mean_mean_gap": round(statistics.mean(vals["mean_gaps"]), 2),
        })

    poet_summary.sort(key=lambda x: x["mean_density"], reverse=True)

    # Gap distribution analysis (all poetry vs control)
    poetry_gaps = []
    control_gaps = []
    for poem in poem_details:
        if poem["era"] == "control":
            control_gaps.append(poem["mean_gap"])
        else:
            poetry_gaps.append(poem["mean_gap"])

    results = {
        "threshold": SPIKE_THRESHOLD,
        "min_tokens": MIN_TOKENS,
        "total_poems": len(poem_details),
        "poetry_mean_gap": round(statistics.mean(poetry_gaps), 2) if poetry_gaps else None,
        "control_mean_gap": round(statistics.mean(control_gaps), 2) if control_gaps else None,
        "poetry_mean_density": round(statistics.mean(
            p["density"] for p in poem_details if p["era"] != "control"
        ), 4),
        "era_summary": era_summary,
        "poet_summary": poet_summary[:20],
        "poem_details": sorted(poem_details, key=lambda x: x["density"], reverse=True),
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {OUTPUT_PATH}")
    print(f"\nAnalyzed {len(poem_details)} poems")
    print(f"\nPoetry mean inter-spike gap: {results['poetry_mean_gap']} tokens")
    print(f"Control mean inter-spike gap: {results['control_mean_gap']} tokens")
    print(f"\nTop 10 eras by surprise density (spikes per token):")
    for e in era_summary[:10]:
        print(f"  {e['era']:25s} density={e['mean_density']:.4f}  mean_gap={e['mean_mean_gap']:.1f}  burst={e.get('mean_burst_score', 'n/a')}")

    return results


if __name__ == "__main__":
    run()
