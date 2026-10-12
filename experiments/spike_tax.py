"""
The Spike Tax: Does a High-S2 Token Create a Local Recovery Period?

After a token with extreme S2 (high positive), do the subsequent tokens
have systematically lower S2 (a 'tax' or 'recovery period')?

Hypothesis: If poets are managing reader expectation, they may provide
'relief' after a highly surprising token — a predictable word that lets
the reader re-anchor. The context window explanation: high-S2 tokens appear
in contexts where GPT-2 was very confident. After such a token appears,
does GPT-2 update its predictions to incorporate the surprise, creating
a more uncertain context (lower entropy = potentially lower S2)?

Uses existing corpus_results.json — no GPT-2 inference needed.
"""

import json
import math
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORPUS_FILE = ROOT / "results" / "corpus_results.json"

def artifact_free_tokens(tokens):
    """Return tokens that are not stanza-break artifacts."""
    return [t for t in tokens if t.get("p_newline", 0) < 0.9]

def pearson(xs, ys):
    n = len(xs)
    if n < 5:
        return None, None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs)
    sy = statistics.stdev(ys)
    if sx == 0 or sy == 0:
        return None, None
    corr = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)
    t_stat = corr * math.sqrt(n - 2) / math.sqrt(max(1e-12, 1 - corr**2))
    return corr, t_stat

def main():
    data = json.loads(CORPUS_FILE.read_text())

    # For each poem, look at how S2 of token t predicts S2 of token t+k (k=1,2,3)
    # Focus on tokens ABOVE the 90th percentile in S2 (the "spike" tokens)
    # and measure mean S2 of the k tokens that follow

    # Aggregate across all poems
    all_pairs_lag1 = []  # (s2_t, s2_t1) for each adjacent pair
    spike_recovery = {1: [], 2: [], 3: []}  # after-spike S2 values at each lag
    non_spike_recovery = {1: [], 2: [], 3: []}  # control: after non-spike tokens

    # For binned analysis
    bins = [(-20, -5), (-5, -2), (-2, 0), (0, 2), (2, 5), (5, 20)]
    bin_labels = ["< -5", "-5 to -2", "-2 to 0", "0 to 2", "2 to 5", "> 5"]
    bin_following = {label: [] for label in bin_labels}

    all_poems_spikes = []

    for poem in data:
        tokens = poem.get("tokens", [])
        af = artifact_free_tokens(tokens)
        if len(af) < 20:
            continue

        s2s = [t["s2"] for t in af]

        # Find spike threshold (90th percentile)
        threshold = sorted(s2s)[int(0.9 * len(s2s))]

        for i in range(len(s2s)):
            s2_t = s2s[i]

            # Classify into bin
            for lo, hi in bins:
                label = bin_labels[bins.index((lo, hi))]
                if lo <= s2_t < hi or (hi == 20 and s2_t >= lo):
                    if i + 1 < len(s2s):
                        bin_following[label].append(s2s[i+1])
                    break

            # Lag-1 pairs
            if i + 1 < len(s2s):
                all_pairs_lag1.append((s2_t, s2s[i+1]))

            # Spike vs non-spike recovery
            is_spike = s2_t >= threshold
            for k in [1, 2, 3]:
                if i + k < len(s2s):
                    if is_spike:
                        spike_recovery[k].append(s2s[i+k])
                    else:
                        non_spike_recovery[k].append(s2s[i+k])

        # Track top spikes
        if s2s:
            top_s2 = max(s2s)
            peak_idx = s2s.index(top_s2)
            all_poems_spikes.append({
                "poem": poem["metadata"]["title"],
                "author": poem["metadata"]["author"],
                "era": poem["metadata"]["era"],
                "peak_s2": round(top_s2, 3),
                "peak_token": af[peak_idx]["token"] if peak_idx < len(af) else "?",
                "s2_lag1": round(s2s[peak_idx+1], 3) if peak_idx+1 < len(s2s) else None,
                "s2_lag2": round(s2s[peak_idx+2], 3) if peak_idx+2 < len(s2s) else None,
                "s2_lag3": round(s2s[peak_idx+3], 3) if peak_idx+3 < len(s2s) else None,
            })

    print(f"Total poems analyzed: {len(all_poems_spikes)}")
    print(f"Total lag-1 pairs: {len(all_pairs_lag1)}")

    # Lag-1 correlation
    lag1_corr, lag1_t = pearson([p[0] for p in all_pairs_lag1], [p[1] for p in all_pairs_lag1])
    print(f"\n== Global lag-1 S2 correlation ==")
    print(f"r = {lag1_corr:.4f}, t = {lag1_t:.2f}, N = {len(all_pairs_lag1)}")

    # Spike vs non-spike recovery
    print(f"\n== Spike Recovery Analysis ==")
    print(f"(spike = top 10% S2 for each poem)")
    print(f"{'Lag':<6} {'Spike mean S2(t+k)':>20} {'Non-spike mean S2(t+k)':>24} {'Diff':>8}")
    for k in [1, 2, 3]:
        if spike_recovery[k] and non_spike_recovery[k]:
            spike_m = statistics.mean(spike_recovery[k])
            ns_m = statistics.mean(non_spike_recovery[k])
            diff = spike_m - ns_m
            print(f"  +{k}   {spike_m:>20.4f} {ns_m:>24.4f} {diff:>8.4f}")

    # Binned analysis
    print(f"\n== Mean S2(t+1) by S2(t) bin ==")
    print(f"{'S2(t) range':<14} {'n':>6} {'mean S2(t+1)':>14} {'median S2(t+1)':>16}")
    for label in bin_labels:
        vals = bin_following[label]
        if vals:
            print(f"  {label:<12} {len(vals):>6} {statistics.mean(vals):>14.4f} {statistics.median(vals):>16.4f}")

    # After highest peak in each poem
    print(f"\n== S2 After Each Poem's Highest Spike ==")
    all_with_lag = [p for p in all_poems_spikes if p["s2_lag1"] is not None]
    all_with_lag.sort(key=lambda x: x["peak_s2"], reverse=True)

    peak_s2s = [p["peak_s2"] for p in all_with_lag]
    lag1_vals = [p["s2_lag1"] for p in all_with_lag]
    lag2_vals = [p["s2_lag2"] for p in all_with_lag if p["s2_lag2"] is not None]
    lag3_vals = [p["s2_lag3"] for p in all_with_lag if p["s2_lag3"] is not None]

    print(f"Mean S2(peak): {statistics.mean(peak_s2s):.3f}")
    print(f"Mean S2(peak+1): {statistics.mean(lag1_vals):.3f}")
    if lag2_vals:
        print(f"Mean S2(peak+2): {statistics.mean(lag2_vals):.3f}")
    if lag3_vals:
        print(f"Mean S2(peak+3): {statistics.mean(lag3_vals):.3f}")

    print(f"\nTop 15 spikes and their immediate successors:")
    print(f"{'Poem':<40} {'Peak S2':>9} {'Token':<15} {'S2+1':>8} {'S2+2':>8} {'S2+3':>8}")
    for p in all_with_lag[:15]:
        print(
            f"  {p['poem'][:38]:<38} "
            f"{p['peak_s2']:>9.2f} "
            f"{repr(p['peak_token']):<15} "
            f"{p['s2_lag1'] if p['s2_lag1'] is not None else 'N/A':>8} "
            f"{p['s2_lag2'] if p['s2_lag2'] is not None else 'N/A':>8} "
            f"{p['s2_lag3'] if p['s2_lag3'] is not None else 'N/A':>8}"
        )

    # How often does S2 drop after a peak?
    drops = sum(1 for p in all_with_lag if p["s2_lag1"] < p["peak_s2"])
    print(f"\nS2 drops after peak: {drops}/{len(all_with_lag)} ({100*drops/len(all_with_lag):.0f}%)")
    big_drops = sum(1 for p in all_with_lag if p["s2_lag1"] < 0 and p["peak_s2"] > 5)
    print(f"Peak > 5 that go negative at t+1: {big_drops}/{sum(1 for p in all_with_lag if p['peak_s2'] > 5)}")

    # Save results
    out = {
        "n_poems": len(all_poems_spikes),
        "lag1_correlation": {"r": round(lag1_corr, 4) if lag1_corr else None, "t": round(lag1_t, 2) if lag1_t else None},
        "spike_recovery": {
            str(k): {
                "spike_mean": round(statistics.mean(spike_recovery[k]), 4) if spike_recovery[k] else None,
                "nonspike_mean": round(statistics.mean(non_spike_recovery[k]), 4) if non_spike_recovery[k] else None,
                "diff": round(statistics.mean(spike_recovery[k]) - statistics.mean(non_spike_recovery[k]), 4) if spike_recovery[k] and non_spike_recovery[k] else None,
            }
            for k in [1, 2, 3]
        },
        "binned_s2_following": {
            label: {
                "n": len(bin_following[label]),
                "mean": round(statistics.mean(bin_following[label]), 4) if bin_following[label] else None,
                "median": round(statistics.median(bin_following[label]), 4) if bin_following[label] else None,
            }
            for label in bin_labels
        },
        "top_peaks": all_with_lag[:30],
    }

    out_file = ROOT / "results" / "spike_tax.json"
    out_file.write_text(json.dumps(out, indent=2))
    print(f"\nSaved to {out_file}")

if __name__ == "__main__":
    main()
