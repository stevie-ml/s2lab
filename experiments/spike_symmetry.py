"""
Spike Symmetry Analysis: Full temporal window around S2 spikes.

Pre-peak data (pre_peak_setup.py): lags -8..-1 → poet "lulls" before strike
Post-peak data (surprise_decay.py): lags +1..+10 → universal 1-token decay

This experiment: combine BOTH into a symmetric window (-8..+8)
and measure whether the "wind-up" and "decay" are symmetric,
and whether the asymmetry reveals distinct poet strategies.

Key metrics:
  pre_area   = sum(S2) over lags -8..-1
  post_area  = sum(S2) over lags +1..+8
  asymmetry  = post_area - pre_area  (positive = heavier tail after; negative = heavier before)
  setup_depth = mean(S2[-3..-1]) - poem_baseline_s2
  decay_depth = mean(S2[+1..+3]) - poem_baseline_s2
"""

import json
import numpy as np
from collections import defaultdict

SPIKE_THRESHOLD = 3.0
WINDOW = 8
MIN_ISOLATION = 4  # minimum tokens between spikes for "clean" analysis

def load_data():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def extract_windows(poem_data):
    """
    For every spike in a poem, extract the S2 window [-WINDOW..+WINDOW].
    Returns list of dicts with window data.
    """
    tokens = poem_data["tokens"]
    if not tokens:
        return []

    s2_vals = [t["s2"] for t in tokens]
    n = len(s2_vals)
    baseline = np.mean(s2_vals)
    poem_meta = poem_data["metadata"]

    windows = []
    spike_positions = [i for i, v in enumerate(s2_vals) if v >= SPIKE_THRESHOLD]

    for pos in spike_positions:
        # Skip if too close to edge
        if pos < WINDOW or pos + WINDOW >= n:
            continue
        # Skip if another spike is within WINDOW tokens (contaminated window)
        nearby = [p for p in spike_positions if p != pos and abs(p - pos) <= WINDOW]
        if nearby:
            continue

        window_vals = s2_vals[pos - WINDOW : pos + WINDOW + 1]
        assert len(window_vals) == 2 * WINDOW + 1

        pre = window_vals[:WINDOW]    # lags -8..-1
        peak = window_vals[WINDOW]    # lag 0
        post = window_vals[WINDOW+1:] # lags +1..+8

        windows.append({
            "era": poem_meta["era"],
            "author": poem_meta["author"],
            "title": poem_meta["title"],
            "peak_s2": peak,
            "baseline": baseline,
            "pre": pre,
            "post": post,
            "window": window_vals,
            "pre_area": sum(v - baseline for v in pre),
            "post_area": sum(v - baseline for v in post),
        })

    return windows

def analyze():
    data = load_data()
    all_windows = []
    for poem in data:
        if poem["metadata"].get("language", "en") != "en":
            continue
        all_windows.extend(extract_windows(poem))

    print(f"Total clean spikes analyzed: {len(all_windows)}")

    # ── 1. Global symmetric profile ──────────────────────────────────────
    lags = list(range(-WINDOW, WINDOW + 1))
    profile = np.zeros(2 * WINDOW + 1)
    for w in all_windows:
        profile += np.array(w["window"]) - w["baseline"]
    profile /= len(all_windows)

    print("\n=== Global Symmetric Profile (mean S2 relative to poem baseline) ===")
    print(f"{'lag':>4}  {'S2 (centered)':>14}")
    for i, lag in enumerate(lags):
        marker = " ◄ SPIKE" if lag == 0 else ""
        bar = "█" * int(max(0, profile[i] * 2)) + ("░" * int(max(0, -profile[i] * 2)))
        print(f"{lag:>4}  {profile[i]:>+8.3f}  {bar}{marker}")

    pre_profile = profile[:WINDOW]
    post_profile = profile[WINDOW+1:]

    pre_sum = pre_profile.sum()
    post_sum = post_profile.sum()
    print(f"\nPre-peak area (sum of centered S2, lags -8..-1):  {pre_sum:+.3f}")
    print(f"Post-peak area (sum of centered S2, lags +1..+8): {post_sum:+.3f}")
    print(f"Asymmetry (post - pre):  {post_sum - pre_sum:+.3f}")
    print(f"  → {'post-peak tail is heavier' if post_sum > pre_sum else 'pre-peak setup is deeper'}")

    # ── 2. Per-era asymmetry ──────────────────────────────────────────────
    era_windows = defaultdict(list)
    for w in all_windows:
        era_windows[w["era"]].append(w)

    print("\n=== Per-Era Asymmetry ===")
    print(f"{'era':<22} {'n':>5} {'pre_area':>10} {'post_area':>10} {'asymmetry':>10} {'interpretation'}")
    print("-" * 80)

    era_stats = []
    for era, ws in era_windows.items():
        pre_a = np.mean([w["pre_area"] for w in ws])
        post_a = np.mean([w["post_area"] for w in ws])
        asym = post_a - pre_a
        era_stats.append((era, len(ws), pre_a, post_a, asym))

    era_stats.sort(key=lambda x: x[4])  # sort by asymmetry

    for era, n, pre_a, post_a, asym in era_stats:
        if asym < -0.5:
            interp = "setup-dominant (poet winds up)"
        elif asym > 0.5:
            interp = "decay-dominant (reverb after spike)"
        else:
            interp = "symmetric"
        print(f"{era:<22} {n:>5} {pre_a:>+10.3f} {post_a:>+10.3f} {asym:>+10.3f}  {interp}")

    # ── 3. Per-poet asymmetry ─────────────────────────────────────────────
    poet_windows = defaultdict(list)
    for w in all_windows:
        poet_windows[w["author"]].append(w)

    print("\n=== Per-Poet Asymmetry (poets with ≥10 clean spikes) ===")
    print(f"{'author':<32} {'n':>5} {'pre_area':>10} {'post_area':>10} {'asymmetry':>10}")
    print("-" * 70)

    poet_stats = [(a, ws) for a, ws in poet_windows.items() if len(ws) >= 10]
    poet_stats.sort(key=lambda x: np.mean([w["post_area"] - w["pre_area"] for w in x[1]]))

    for author, ws in poet_stats:
        pre_a = np.mean([w["pre_area"] for w in ws])
        post_a = np.mean([w["post_area"] for w in ws])
        asym = post_a - pre_a
        print(f"{author:<32} {len(ws):>5} {pre_a:>+10.3f} {post_a:>+10.3f} {asym:>+10.3f}")

    # ── 4. Peak height vs asymmetry correlation ───────────────────────────
    peaks = [w["peak_s2"] for w in all_windows]
    asyms = [w["post_area"] - w["pre_area"] for w in all_windows]
    r = np.corrcoef(peaks, asyms)[0, 1]
    print(f"\nCorrelation between peak S2 height and asymmetry: r = {r:.3f}")

    # ── 5. Setup depth vs decay depth ────────────────────────────────────
    setup_depths = [np.mean(w["pre"][-3:]) - w["baseline"] for w in all_windows]
    decay_depths = [np.mean(w["post"][:3]) - w["baseline"] for w in all_windows]
    r2 = np.corrcoef(setup_depths, decay_depths)[0, 1]
    print(f"Correlation between setup depth (lags -3..-1) and decay depth (lags +1..+3): r = {r2:.3f}")
    print(f"Mean setup depth: {np.mean(setup_depths):+.3f}")
    print(f"Mean decay depth: {np.mean(decay_depths):+.3f}")

    # ── 6. Are isolated spikes more asymmetric than "routine" ones? ───────
    # Look at peak height vs. asymmetry quartile analysis
    sorted_by_peak = sorted(all_windows, key=lambda w: w["peak_s2"])
    q4 = len(sorted_by_peak) // 4
    quartiles = [
        sorted_by_peak[:q4],
        sorted_by_peak[q4:2*q4],
        sorted_by_peak[2*q4:3*q4],
        sorted_by_peak[3*q4:],
    ]
    print("\n=== Asymmetry by Peak Height Quartile ===")
    print(f"{'Quartile':<12} {'Avg peak S2':>12} {'Pre area':>10} {'Post area':>10} {'Asymmetry':>10}")
    labels = ["Q1 (low)", "Q2", "Q3", "Q4 (high)"]
    for label, q in zip(labels, quartiles):
        avg_peak = np.mean([w["peak_s2"] for w in q])
        avg_pre  = np.mean([w["pre_area"] for w in q])
        avg_post = np.mean([w["post_area"] for w in q])
        print(f"{label:<12} {avg_peak:>12.2f} {avg_pre:>+10.3f} {avg_post:>+10.3f} {avg_post-avg_pre:>+10.3f}")

    # ── 7. Full symmetric profile by era (selected) ───────────────────────
    selected_eras = ["haiku", "ballad", "romantic", "modernist", "new_york_school", "prose_poetry"]
    print("\n=== Symmetric Profile by Era (selected, centered relative to baseline) ===")
    print(f"{'lag':>4}", end="")
    for era in selected_eras:
        print(f"  {era[:12]:>12}", end="")
    print()
    print("-" * (6 + 14 * len(selected_eras)))

    era_profiles = {}
    for era in selected_eras:
        ws = era_windows.get(era, [])
        if not ws:
            era_profiles[era] = np.zeros(2 * WINDOW + 1)
            continue
        p = np.zeros(2 * WINDOW + 1)
        for w in ws:
            p += np.array(w["window"]) - w["baseline"]
        era_profiles[era] = p / len(ws)

    for i, lag in enumerate(lags):
        print(f"{lag:>4}", end="")
        for era in selected_eras:
            val = era_profiles[era][i]
            print(f"  {val:>+12.3f}", end="")
        print()

    return {
        "n_windows": len(all_windows),
        "global_pre_area": float(pre_sum),
        "global_post_area": float(post_sum),
        "global_asymmetry": float(post_sum - pre_sum),
        "mean_setup_depth": float(np.mean(setup_depths)),
        "mean_decay_depth": float(np.mean(decay_depths)),
        "peak_asym_correlation": float(r),
        "setup_decay_correlation": float(r2),
    }

if __name__ == "__main__":
    results = analyze()
    print("\n=== Summary ===")
    for k, v in results.items():
        print(f"  {k}: {v}")
