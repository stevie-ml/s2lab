"""
Surprise Decay Curve: How quickly does S2 return to baseline after a spike?

After a high-S2 event at position t, we track S2 at t+1, t+2, ..., t+15.
This reveals the temporal "half-life" of poetic surprise and whether different
eras have characteristic recovery profiles (fast vs slow vs oscillating).

Builds on: post_surprise_signature.md (t+1 only), entropy_after_surprise.md
Extends: measures multi-step decay, not just immediate aftermath.
"""

import json
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/surprise_decay_curve.json"
S2_THRESHOLD = 2.0        # high-S2 spike
MAX_LAG = 15              # track up to 15 tokens after spike
MIN_POEM_TOKENS = 25      # minimum poem length after filtering
MIN_ERA_EVENTS = 20       # minimum events per era for reliable stats

def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def filter_token(tok):
    """Exclude stanza-break artifacts (high p_newline tokens)."""
    return tok.get("p_newline", 0) < 0.9

def compute_poem_baseline(tokens):
    """Compute mean and std of S2 for a poem (filtered tokens only)."""
    vals = [t["s2"] for t in tokens if filter_token(t)]
    if len(vals) < 5:
        return None, None
    return statistics.mean(vals), statistics.stdev(vals)

def get_decay_window(tokens, spike_idx, max_lag):
    """
    Get the S2 values at lag 0, 1, ..., max_lag from spike_idx.
    Only include artifact-filtered tokens (skip stanza breaks).
    Returns list of (lag, s2) pairs; stops at poem end or if we run out.
    """
    window = [(0, tokens[spike_idx]["s2"])]
    lag = 0
    for i in range(spike_idx + 1, len(tokens)):
        if tokens[i].get("p_newline", 0) >= 0.9:
            # stanza break — counts as a lag but we skip its s2
            continue
        lag += 1
        if lag > max_lag:
            break
        window.append((lag, tokens[i]["s2"]))
    return window

def run():
    data = load_data()

    # --- Per-era decay curves ---
    era_lag_s2 = defaultdict(lambda: defaultdict(list))  # era -> lag -> [s2]
    era_events = defaultdict(int)

    # --- Global decay curve ---
    global_lag_s2 = defaultdict(list)

    # --- Per-poem recovery metrics ---
    poem_records = []

    for poem in data:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        lang = meta.get("language", "en")
        if lang != "en":
            continue

        tokens = poem.get("tokens", [])
        filtered_tokens = [t for t in tokens if filter_token(t)]
        if len(filtered_tokens) < MIN_POEM_TOKENS:
            continue

        baseline_mean, baseline_std = compute_poem_baseline(tokens)
        if baseline_mean is None:
            continue

        # Find all high-S2 spikes
        spike_positions = [
            i for i, t in enumerate(tokens)
            if filter_token(t) and t["s2"] >= S2_THRESHOLD
        ]

        for spike_idx in spike_positions:
            window = get_decay_window(tokens, spike_idx, MAX_LAG)
            if len(window) < 3:
                continue  # not enough post-spike data

            spike_s2 = window[0][1]

            # Record decay values
            for lag, s2 in window:
                era_lag_s2[era][lag].append(s2)
                global_lag_s2[lag].append(s2)

            era_events[era] += 1

            # Compute recovery time: lags until S2 drops below (baseline + 0.5 * std)
            recovery_threshold = baseline_mean + 0.5 * (baseline_std or 1.0)
            recovery_lag = None
            for lag, s2 in window[1:]:  # start at t+1
                if s2 <= recovery_threshold:
                    recovery_lag = lag
                    break

            poem_records.append({
                "title": meta.get("title", ""),
                "era": era,
                "spike_s2": spike_s2,
                "baseline_mean": baseline_mean,
                "recovery_lag": recovery_lag,  # None if not recovered within window
                "window_len": len(window),
            })

    # --- Compute global decay curve (mean S2 by lag) ---
    global_decay = {}
    global_lag0_mean = statistics.mean(global_lag_s2[0]) if global_lag_s2[0] else 1.0
    for lag in range(0, MAX_LAG + 1):
        vals = global_lag_s2[lag]
        if vals:
            mean_s2 = statistics.mean(vals)
            global_decay[lag] = {
                "n": len(vals),
                "mean_s2": round(mean_s2, 4),
                "pct_of_spike": round(mean_s2 / global_lag0_mean * 100, 1) if global_lag0_mean else 0,
            }

    # --- Compute per-era decay and recovery stats ---
    era_stats = {}
    for era, lag_data in era_lag_s2.items():
        n_events = era_events[era]
        if n_events < MIN_ERA_EVENTS:
            continue

        lag0_mean = statistics.mean(lag_data[0]) if lag_data.get(0) else 1.0

        decay_curve = {}
        for lag in range(0, MAX_LAG + 1):
            vals = lag_data.get(lag, [])
            if vals:
                m = statistics.mean(vals)
                decay_curve[lag] = {
                    "n": len(vals),
                    "mean_s2": round(m, 4),
                    "pct_of_spike": round(m / lag0_mean * 100, 1) if lag0_mean else 0,
                }

        # Half-life: lag at which mean S2 drops to 50% of spike value
        half_life = None
        for lag in range(1, MAX_LAG + 1):
            if lag in decay_curve:
                pct = decay_curve[lag]["pct_of_spike"]
                if pct <= 50:
                    half_life = lag
                    break

        # Recovery ratio at lag 5: what % of spike value remains
        pct_at_5 = decay_curve.get(5, {}).get("pct_of_spike", None)
        pct_at_10 = decay_curve.get(10, {}).get("pct_of_spike", None)

        era_stats[era] = {
            "n_events": n_events,
            "spike_mean": round(lag0_mean, 4),
            "pct_at_lag1": decay_curve.get(1, {}).get("pct_of_spike"),
            "pct_at_lag2": decay_curve.get(2, {}).get("pct_of_spike"),
            "pct_at_lag5": pct_at_5,
            "pct_at_lag10": pct_at_10,
            "half_life_lag": half_life,
            "decay_curve": decay_curve,
        }

    # --- Recovery time distribution (poem-level) ---
    recovery_times = [r["recovery_lag"] for r in poem_records if r["recovery_lag"] is not None]
    unrecovered = sum(1 for r in poem_records if r["recovery_lag"] is None)

    if recovery_times:
        median_recovery = sorted(recovery_times)[len(recovery_times) // 2]
        mean_recovery = statistics.mean(recovery_times)
        pct_recover_by_1 = sum(1 for x in recovery_times if x <= 1) / len(recovery_times) * 100
        pct_recover_by_3 = sum(1 for x in recovery_times if x <= 3) / len(recovery_times) * 100
        pct_recover_by_5 = sum(1 for x in recovery_times if x <= 5) / len(recovery_times) * 100
    else:
        median_recovery = mean_recovery = pct_recover_by_1 = pct_recover_by_3 = pct_recover_by_5 = 0

    results = {
        "global_decay": global_decay,
        "era_stats": era_stats,
        "recovery_summary": {
            "total_spikes": len(poem_records),
            "recovered_within_window": len(recovery_times),
            "unrecovered": unrecovered,
            "median_recovery_lag": median_recovery,
            "mean_recovery_lag": round(mean_recovery, 2) if recovery_times else 0,
            "pct_recover_by_lag1": round(pct_recover_by_1, 1),
            "pct_recover_by_lag3": round(pct_recover_by_3, 1),
            "pct_recover_by_lag5": round(pct_recover_by_5, 1),
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {OUTPUT_PATH}")

    # Print key findings
    print("\n=== GLOBAL DECAY CURVE ===")
    print(f"{'Lag':>4}  {'Mean S2':>8}  {'% of spike':>12}  {'N':>6}")
    for lag in range(0, min(16, MAX_LAG + 1)):
        d = global_decay.get(lag, {})
        if d:
            print(f"{lag:>4}  {d['mean_s2']:>8.3f}  {d['pct_of_spike']:>11.1f}%  {d['n']:>6}")

    print(f"\n=== RECOVERY SUMMARY ===")
    rs = results["recovery_summary"]
    print(f"Total high-S2 spikes analyzed: {rs['total_spikes']}")
    print(f"Median recovery lag: {rs['median_recovery_lag']}")
    print(f"Mean recovery lag: {rs['mean_recovery_lag']}")
    print(f"% recovered by lag 1: {rs['pct_recover_by_lag1']}%")
    print(f"% recovered by lag 3: {rs['pct_recover_by_lag3']}%")
    print(f"% recovered by lag 5: {rs['pct_recover_by_lag5']}%")

    print(f"\n=== ERA RECOVERY PROFILES (sorted by lag-5 %) ===")
    era_sorted = sorted(era_stats.items(), key=lambda x: x[1].get("pct_at_lag5") or 999)
    print(f"{'Era':25}  {'N':>5}  {'lag1%':>6}  {'lag5%':>6}  {'lag10%':>7}  {'half-life':>9}")
    for era, s in era_sorted:
        hl = s.get("half_life_lag")
        hl_str = str(hl) if hl else ">15"
        p1 = s.get("pct_at_lag1")
        p5 = s.get("pct_at_lag5")
        p10 = s.get("pct_at_lag10")
        p1_str = f"{p1:.1f}" if p1 is not None else "—"
        p5_str = f"{p5:.1f}" if p5 is not None else "—"
        p10_str = f"{p10:.1f}" if p10 is not None else "—"
        print(f"{era:25}  {s['n_events']:>5}  {p1_str:>6}  {p5_str:>6}  {p10_str:>7}  {hl_str:>9}")

if __name__ == "__main__":
    run()
