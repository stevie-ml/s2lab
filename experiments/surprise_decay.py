"""
Surprise Decay Curves: How Does S2 Evolve After a High-S2 Spike?

Research question: After a poet makes a highly unexpected word choice (high S2),
what happens in the following N tokens? Does surprise quickly decay back to
baseline, or does the poet sustain an elevated region of unpredictability?

This characterizes two distinct poetic strategies:
  - "Isolated shock": spike then immediate return to expectation
  - "Surprise cascade": high S2 begets more high S2 -- momentum

Metrics:
  - Decay curve: mean S2 at lag k=1..10 after a spike (S2 ≥ threshold)
  - Half-life: at what lag k does mean S2 drop to 50% of spike height?
  - Aftershock index: mean S2 in the 5 tokens AFTER a spike / mean S2 overall
  - Momentum score: correlation between s2[t] and s2[t+1] conditioned on s2[t] ≥ threshold

No new model inference -- works entirely from corpus_results.json.
"""

import json
import os
import statistics
from collections import defaultdict
import math

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

SPIKE_THRESHOLD = 3.0  # S2 units to qualify as a "spike"
MAX_LAG = 10           # how many tokens after a spike to track


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def compute_decay_curve(tokens, threshold=SPIKE_THRESHOLD, max_lag=MAX_LAG):
    """
    For each spike position, record S2 at lags 0..max_lag.
    Returns a dict {lag: [s2_values]}.
    """
    s2_seq = [t["s2"] for t in tokens]
    n = len(s2_seq)
    lag_values = defaultdict(list)

    for i, s2 in enumerate(s2_seq):
        if s2 >= threshold:
            for lag in range(0, max_lag + 1):
                j = i + lag
                if j < n:
                    lag_values[lag].append(s2_seq[j])

    return lag_values


def mean_safe(lst):
    return statistics.mean(lst) if lst else float("nan")


def halflife(decay_means, spike_level):
    """
    Return the lag k at which mean drops to 50% of spike_level.
    Returns None if it never drops that low within max_lag.
    """
    half = spike_level * 0.5
    for k, v in sorted(decay_means.items()):
        if k > 0 and v <= half:
            return k
    return None


def aftershock_index(tokens, threshold=SPIKE_THRESHOLD, window=5):
    """
    Mean S2 in the window after a spike / global mean S2.
    > 1 means post-spike tokens are more surprising than average.
    """
    s2_seq = [t["s2"] for t in tokens]
    global_mean = mean_safe(s2_seq)
    if global_mean == 0 or math.isnan(global_mean):
        return float("nan")

    post_spike = []
    n = len(s2_seq)
    for i, s2 in enumerate(s2_seq):
        if s2 >= threshold:
            for lag in range(1, window + 1):
                j = i + lag
                if j < n:
                    post_spike.append(s2_seq[j])

    if not post_spike:
        return float("nan")

    return mean_safe(post_spike) / global_mean


def analyze_poem(poem):
    tokens = poem.get("tokens", [])
    if len(tokens) < 15:
        return None

    meta = poem.get("metadata", {})
    era = meta.get("era", "unknown")
    author = meta.get("author", "Unknown")
    title = meta.get("title", "Untitled")

    s2_seq = [t["s2"] for t in tokens]
    global_mean = mean_safe(s2_seq)
    spikes = [s2 for s2 in s2_seq if s2 >= SPIKE_THRESHOLD]
    if not spikes:
        return None

    spike_mean = mean_safe(spikes)
    decay = compute_decay_curve(tokens)
    decay_means = {lag: mean_safe(vals) for lag, vals in decay.items()}
    hl = halflife(decay_means, spike_mean)
    asi = aftershock_index(tokens)

    # lag-1 momentum: E[s2[t+1] | s2[t] >= threshold] - global_mean
    lag1_post_spike = decay_means.get(1, float("nan"))
    momentum = lag1_post_spike - global_mean if not math.isnan(lag1_post_spike) else float("nan")

    return {
        "era": era,
        "author": author,
        "title": title,
        "global_mean_s2": global_mean,
        "spike_mean_s2": spike_mean,
        "n_spikes": len(spikes),
        "n_tokens": len(s2_seq),
        "decay_means": decay_means,
        "halflife": hl,
        "aftershock_index": asi,
        "momentum": momentum,
    }


def main():
    data = load_results()
    results = []
    for poem in data:
        r = analyze_poem(poem)
        if r is not None:
            results.append(r)

    # ── Global decay curve ───────────────────────────────────────────────────
    global_lag = defaultdict(list)
    for r in results:
        for lag, val in r["decay_means"].items():
            if not math.isnan(val):
                global_lag[lag].append(val)

    global_decay = {lag: mean_safe(vals) for lag, vals in sorted(global_lag.items())}

    # ── By era ───────────────────────────────────────────────────────────────
    era_results = defaultdict(list)
    for r in results:
        era_results[r["era"]].append(r)

    era_summary = {}
    for era, poems in era_results.items():
        if len(poems) < 2:
            continue
        lag_by_era = defaultdict(list)
        for p in poems:
            for lag, val in p["decay_means"].items():
                if not math.isnan(val):
                    lag_by_era[lag].append(val)
        decay_curve = {lag: mean_safe(vals) for lag, vals in sorted(lag_by_era.items())}
        spike0 = decay_curve.get(0, float("nan"))
        hl = halflife(decay_curve, spike0)
        era_summary[era] = {
            "n": len(poems),
            "spike_level": spike0,
            "lag1": decay_curve.get(1, float("nan")),
            "lag3": decay_curve.get(3, float("nan")),
            "lag5": decay_curve.get(5, float("nan")),
            "halflife": hl,
            "avg_asi": mean_safe([p["aftershock_index"] for p in poems
                                  if not math.isnan(p["aftershock_index"])]),
            "avg_momentum": mean_safe([p["momentum"] for p in poems
                                       if not math.isnan(p["momentum"])]),
        }

    # ── By author ────────────────────────────────────────────────────────────
    author_results = defaultdict(list)
    for r in results:
        author_results[r["author"]].append(r)

    author_summary = {}
    for author, poems in author_results.items():
        if len(poems) < 2:
            continue
        lag_by_author = defaultdict(list)
        for p in poems:
            for lag, val in p["decay_means"].items():
                if not math.isnan(val):
                    lag_by_author[lag].append(val)
        dc = {lag: mean_safe(vals) for lag, vals in sorted(lag_by_author.items())}
        spike0 = dc.get(0, float("nan"))
        hl = halflife(dc, spike0)
        author_summary[author] = {
            "n": len(poems),
            "spike_level": spike0,
            "lag1": dc.get(1, float("nan")),
            "lag5": dc.get(5, float("nan")),
            "halflife": hl,
            "avg_asi": mean_safe([p["aftershock_index"] for p in poems
                                  if not math.isnan(p["aftershock_index"])]),
        }

    # ── Top "sustained surprise" poems ──────────────────────────────────────
    # Rank by aftershock index (highest = surprise cascade)
    ranked_poems = sorted(
        [r for r in results if not math.isnan(r["aftershock_index"])],
        key=lambda r: r["aftershock_index"],
        reverse=True
    )

    # ── Print results ────────────────────────────────────────────────────────
    print("=== GLOBAL SURPRISE DECAY CURVE ===")
    print(f"{'Lag':>4}  {'Mean S2':>8}")
    for lag, val in sorted(global_decay.items()):
        print(f"{lag:>4}  {val:>8.3f}")

    print("\n=== DECAY BY ERA (min 2 poems) ===")
    rows = sorted(era_summary.items(), key=lambda x: x[1]["avg_momentum"], reverse=True)
    print(f"{'Era':<25} {'N':>3} {'Spike':>7} {'Lag1':>6} {'Lag3':>6} {'Lag5':>6} {'Half-life':>9} {'ASI':>6} {'Momentum':>9}")
    for era, s in rows:
        hl = str(s["halflife"]) if s["halflife"] is not None else "≥10"
        print(f"{era:<25} {s['n']:>3} {s['spike_level']:>7.2f} {s['lag1']:>6.2f} {s['lag3']:>6.2f} {s['lag5']:>6.2f} {hl:>9} {s['avg_asi']:>6.2f} {s['avg_momentum']:>9.3f}")

    print("\n=== DECAY BY AUTHOR (min 2 poems) ===")
    author_rows = sorted(author_summary.items(), key=lambda x: x[1]["avg_asi"], reverse=True)
    print(f"{'Author':<30} {'N':>3} {'Spike':>7} {'Lag1':>6} {'Lag5':>6} {'Half-life':>9} {'ASI':>6}")
    for author, s in author_rows:
        hl = str(s["halflife"]) if s["halflife"] is not None else "≥10"
        print(f"{author:<30} {s['n']:>3} {s['spike_level']:>7.2f} {s['lag1']:>6.2f} {s['lag5']:>6.2f} {hl:>9} {s['avg_asi']:>6.2f}")

    print("\n=== TOP SUSTAINED-SURPRISE POEMS (highest aftershock index) ===")
    for r in ranked_poems[:15]:
        print(f"  ASI={r['aftershock_index']:.3f} | {r['author'][:25]:<25} | {r['title'][:40]:<40} | era={r['era']}")

    print("\n=== BOTTOM (isolated spikes — quick return to baseline) ===")
    for r in ranked_poems[-10:]:
        print(f"  ASI={r['aftershock_index']:.3f} | {r['author'][:25]:<25} | {r['title'][:40]:<40} | era={r['era']}")

    return {
        "global_decay": global_decay,
        "era_summary": era_summary,
        "author_summary": author_summary,
        "ranked_poems": ranked_poems,
    }


if __name__ == "__main__":
    main()
