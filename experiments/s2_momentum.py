"""
S₂ Momentum: Autocorrelation and Recovery in Poetic Surprise

When a poet writes a high-S₂ token, what happens next?

  1. AUTOCORRELATION: Does high S₂ at position t predict high S₂ at t+k?
     - Positive autocorr → surprise clusters (sustained surprising zones)
     - Negative autocorr → alternation (surprising then predictable, then surprising...)
     - Near-zero → surprise is randomly distributed

  2. RECOVERY LENGTH: After a S₂ spike, how many tokens until return to baseline?
     Captures whether surprise is punctuated (fast recovery) or sustained (slow recovery).

  3. MOMENTUM INDEX: Does S₂ tend to build (gradient > 0) or decay over the poem's arc?

Hypotheses:
  H1: Modernist poetry has positive autocorr (sustained surprise zones)
  H2: Ballads and formal verse have near-zero autocorr (isolated peaks)
  H3: Recovery length is shorter in compact forms (haiku, ballad) than in free verse
  H4: Autocorrelation is higher at short lags (local clustering) across all eras
"""

import json
import sys
import os
import statistics
import math
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")


def autocorr(series, lag):
    """Lag-k autocorrelation of a list of floats."""
    n = len(series)
    if n <= lag + 2:
        return float("nan")
    mean = statistics.mean(series)
    var = statistics.variance(series)
    if var < 1e-10:
        return float("nan")
    pairs = [(series[i] - mean) * (series[i + lag] - mean) for i in range(n - lag)]
    return (sum(pairs) / (n - lag)) / var


def recovery_lengths(series, threshold=None):
    """
    Find each token where S₂ > threshold (default: mean + 0.5 std).
    Return how many tokens until S₂ drops back below mean.
    """
    if len(series) < 5:
        return []
    mean = statistics.mean(series)
    try:
        std = statistics.stdev(series)
    except statistics.StatisticsError:
        return []
    if threshold is None:
        threshold = mean + 0.5 * std

    lengths = []
    i = 0
    while i < len(series):
        if series[i] > threshold:
            j = i + 1
            while j < len(series) and series[j] > mean:
                j += 1
            lengths.append(j - i)
            i = j
        else:
            i += 1
    return lengths


def poem_momentum(series):
    """
    Slope of a linear fit to the S₂ series (positive = surprise builds over poem).
    Returns slope normalized by series length.
    """
    n = len(series)
    if n < 4:
        return float("nan")
    xs = list(range(n))
    xbar = (n - 1) / 2
    ybar = statistics.mean(series)
    num = sum((xs[i] - xbar) * (series[i] - ybar) for i in range(n))
    den = sum((xs[i] - xbar) ** 2 for i in range(n))
    if den < 1e-10:
        return float("nan")
    return (num / den) * n  # normalized by length


def run():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    poems = []
    for item in data:
        meta = item["metadata"]
        tokens = item.get("tokens", [])
        if len(tokens) < 10:
            continue

        s2_series = [t["s2"] for t in tokens]

        ac1 = autocorr(s2_series, 1)
        ac2 = autocorr(s2_series, 2)
        ac5 = autocorr(s2_series, 5)
        rec = recovery_lengths(s2_series)
        avg_rec = statistics.mean(rec) if rec else float("nan")
        momentum = poem_momentum(s2_series)
        mean_s2 = statistics.mean(s2_series)

        poems.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta.get("era", "unknown"),
            "year": meta.get("year", 0),
            "n_tokens": len(s2_series),
            "mean_s2": mean_s2,
            "ac1": ac1,
            "ac2": ac2,
            "ac5": ac5,
            "avg_recovery": avg_rec,
            "momentum": momentum,
        })

    # ── Era-level aggregation ────────────────────────────────────────────
    era_groups = defaultdict(list)
    for p in poems:
        era_groups[p["era"]].append(p)

    print("=== ERA-LEVEL AUTOCORRELATION (lag-1, lag-2, lag-5) ===\n")
    print(f"{'Era':<22} {'n':>4} {'mean_s2':>8} {'AC(1)':>8} {'AC(2)':>8} {'AC(5)':>8} {'Rec.len':>8} {'Momentum':>9}")
    print("-" * 80)

    era_stats = {}
    for era, ps in sorted(era_groups.items()):
        n = len(ps)
        mean_s2 = statistics.mean(p["mean_s2"] for p in ps)
        ac1_vals = [p["ac1"] for p in ps if not math.isnan(p["ac1"])]
        ac2_vals = [p["ac2"] for p in ps if not math.isnan(p["ac2"])]
        ac5_vals = [p["ac5"] for p in ps if not math.isnan(p["ac5"])]
        rec_vals = [p["avg_recovery"] for p in ps if not math.isnan(p["avg_recovery"])]
        mom_vals = [p["momentum"] for p in ps if not math.isnan(p["momentum"])]

        ac1 = statistics.mean(ac1_vals) if ac1_vals else float("nan")
        ac2 = statistics.mean(ac2_vals) if ac2_vals else float("nan")
        ac5 = statistics.mean(ac5_vals) if ac5_vals else float("nan")
        avg_rec = statistics.mean(rec_vals) if rec_vals else float("nan")
        momentum = statistics.mean(mom_vals) if mom_vals else float("nan")

        era_stats[era] = {"n": n, "mean_s2": mean_s2, "ac1": ac1, "ac2": ac2, "ac5": ac5,
                          "avg_rec": avg_rec, "momentum": momentum}
        print(f"{era:<22} {n:>4} {mean_s2:>8.3f} {ac1:>8.3f} {ac2:>8.3f} {ac5:>8.3f} {avg_rec:>8.2f} {momentum:>9.3f}")

    # ── Top poems by autocorrelation ─────────────────────────────────────
    print("\n=== TOP 10 POEMS BY LAG-1 AUTOCORRELATION (highest surprise momentum) ===\n")
    sorted_by_ac1 = sorted([p for p in poems if not math.isnan(p["ac1"])], key=lambda p: p["ac1"], reverse=True)
    for p in sorted_by_ac1[:10]:
        print(f"  {p['ac1']:+.3f}  {p['title'][:45]:<45}  {p['author'][:20]:<20}  [{p['era']}]")

    print("\n=== BOTTOM 10 POEMS BY LAG-1 AUTOCORRELATION (alternating pattern) ===\n")
    for p in sorted_by_ac1[-10:]:
        print(f"  {p['ac1']:+.3f}  {p['title'][:45]:<45}  {p['author'][:20]:<20}  [{p['era']}]")

    # ── Recovery lengths ─────────────────────────────────────────────────
    print("\n=== TOP 10 POEMS BY RECOVERY LENGTH (slowest return to baseline) ===\n")
    sorted_by_rec = sorted([p for p in poems if not math.isnan(p["avg_recovery"])],
                           key=lambda p: p["avg_recovery"], reverse=True)
    for p in sorted_by_rec[:10]:
        print(f"  rec={p['avg_recovery']:5.2f}  {p['title'][:45]:<45}  {p['era']}")

    # ── Momentum ─────────────────────────────────────────────────────────
    print("\n=== POEMS WHERE SURPRISE BUILDS OVER TIME (positive momentum) ===\n")
    sorted_by_mom = sorted([p for p in poems if not math.isnan(p["momentum"])],
                           key=lambda p: p["momentum"], reverse=True)
    for p in sorted_by_mom[:8]:
        print(f"  mom={p['momentum']:+7.3f}  {p['title'][:45]:<45}  {p['era']}")
    print("\n=== POEMS WHERE SURPRISE DECAYS OVER TIME (negative momentum) ===\n")
    for p in sorted_by_mom[-8:]:
        print(f"  mom={p['momentum']:+7.3f}  {p['title'][:45]:<45}  {p['era']}")

    # ── Lag decay: how fast does autocorrelation fall off? ───────────────
    print("\n=== AUTOCORRELATION DECAY BY ERA (AC1 → AC2 → AC5) ===\n")
    print(f"{'Era':<22} {'AC1':>8} {'AC2':>8} {'AC5':>8} {'Decay rate':>12}")
    print("-" * 55)
    for era, stats in sorted(era_stats.items(), key=lambda x: x[1]["ac1"], reverse=True):
        ac1, ac2, ac5 = stats["ac1"], stats["ac2"], stats["ac5"]
        if not any(math.isnan(v) for v in [ac1, ac2, ac5]) and ac1 > 0:
            decay = (ac1 - ac5) / 4  # slope of AC decay per lag
        else:
            decay = float("nan")
        print(f"{era:<22} {ac1:>8.3f} {ac2:>8.3f} {ac5:>8.3f} {decay:>12.4f}")

    return poems, era_stats


if __name__ == "__main__":
    run()
