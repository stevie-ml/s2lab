"""
S₂ Zone Topology: Isolated Spikes vs. Sustained High-S₂ Zones

Previous analyses treated surprise events as isolated spikes (using an isolation
criterion that excluded tokens within ±8 of another spike). But what happens if
we relax that and ask: do high-S₂ moments cluster into sustained *zones* of
consecutive deviance, or do they remain single-token events?

This experiment characterizes the *topology* of surprise in poems:

  - "Spikes": isolated single-token high-S₂ events (run length = 1)
  - "Zones":  runs of ≥2 consecutive high-S₂ tokens forming a sustained
              region of informational deviance

Questions:
  1. What fraction of surprise events are isolated vs. zoned?
  2. How long are zones when they occur?
  3. Does zone density differ across eras?
  4. What text actually appears in sustained zones?
  5. Is zone length correlated with zone intensity (mean S₂)?

Threshold: S₂ > 0.5 for inclusion in a high-S₂ region.
Zone = maximal consecutive run of ≥2 tokens above threshold.
Spike = exactly 1 consecutive token above threshold.
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def find_runs(token_data, threshold=0.5):
    """
    Find maximal consecutive runs of tokens with s2 >= threshold.
    Returns list of dicts: {tokens, s2_values, mean_s2, max_s2, length, text}
    """
    runs = []
    i = 0
    n = len(token_data)
    while i < n:
        tok = token_data[i]
        if tok.get("s2", 0) >= threshold:
            # Start a run
            run_tokens = [tok]
            j = i + 1
            while j < n and token_data[j].get("s2", 0) >= threshold:
                run_tokens.append(token_data[j])
                j += 1
            s2_vals = [t["s2"] for t in run_tokens]
            text = "".join(t["token"] for t in run_tokens)
            runs.append({
                "length": len(run_tokens),
                "mean_s2": statistics.mean(s2_vals),
                "max_s2": max(s2_vals),
                "text": text,
                "tokens": [t["token"] for t in run_tokens],
                "s2_values": s2_vals,
                "start_idx": i,
            })
            i = j
        else:
            i += 1
    return runs


def classify_run(run):
    return "spike" if run["length"] == 1 else "zone"


def main():
    results = load_results()
    poems = [r for r in results if r.get("metadata", {}).get("era") != "control"]
    print(f"Analyzing {len(poems)} poems (control excluded)...")

    # Global accumulators
    all_spikes = []
    all_zones = []
    era_stats = defaultdict(lambda: {"spikes": [], "zones": [], "poems": 0})

    zone_examples = []  # (length, mean_s2, text, title, author)

    for poem in poems:
        token_data = poem.get("tokens", [])
        if not token_data:
            continue

        runs = find_runs(token_data, threshold=0.5)
        spikes = [r for r in runs if r["length"] == 1]
        zones  = [r for r in runs if r["length"] >= 2]

        all_spikes.extend(spikes)
        all_zones.extend(zones)

        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        author = meta.get("author", "Unknown")
        title = meta.get("title", "")
        era_stats[era]["spikes"].extend(spikes)
        era_stats[era]["zones"].extend(zones)
        era_stats[era]["poems"] += 1

        for z in zones:
            zone_examples.append({
                "length": z["length"],
                "mean_s2": z["mean_s2"],
                "max_s2": z["max_s2"],
                "text": z["text"],
                "title": title,
                "author": author,
                "era": era,
            })

    # ── Global Summary ──────────────────────────────────────────────────────────
    n_spikes = len(all_spikes)
    n_zones  = len(all_zones)
    n_events = n_spikes + n_zones
    pct_isolated = 100 * n_spikes / n_events if n_events else 0
    pct_zoned    = 100 * n_zones  / n_events if n_events else 0

    zone_lengths = [z["length"] for z in all_zones]
    zone_mean_s2 = [z["mean_s2"] for z in all_zones]
    spike_s2     = [s["mean_s2"] for s in all_spikes]

    print("\n=== GLOBAL TOPOLOGY ===")
    print(f"Total high-S₂ events (S₂ ≥ 0.5):  {n_events}")
    print(f"  Isolated spikes (length=1):        {n_spikes}  ({pct_isolated:.1f}%)")
    print(f"  Sustained zones  (length≥2):       {n_zones}   ({pct_zoned:.1f}%)")
    print()
    if zone_lengths:
        print(f"Zone lengths: min={min(zone_lengths)}, max={max(zone_lengths)}, "
              f"mean={statistics.mean(zone_lengths):.2f}, "
              f"median={statistics.median(zone_lengths):.1f}")
        print(f"Zone mean S₂: {statistics.mean(zone_mean_s2):.3f}")
        print(f"Spike mean S₂: {statistics.mean(spike_s2):.3f}")

    # ── Zone length distribution ────────────────────────────────────────────────
    from collections import Counter
    length_dist = Counter(zone_lengths)
    print("\n=== ZONE LENGTH DISTRIBUTION ===")
    print(f"{'Length':<8} {'Count':<8} {'%':<8}")
    total_zones = len(zone_lengths)
    for length in sorted(length_dist.keys()):
        pct = 100 * length_dist[length] / total_zones
        print(f"{length:<8} {length_dist[length]:<8} {pct:.1f}%")

    # ── Top longest zones ───────────────────────────────────────────────────────
    zone_examples.sort(key=lambda x: x["length"], reverse=True)
    print("\n=== TOP 15 LONGEST ZONES ===")
    print(f"{'Len':<5} {'Mean S₂':<9} {'Author':<22} {'Era':<20} {'Text'}")
    for ex in zone_examples[:15]:
        text_preview = repr(ex["text"])[:50]
        print(f"{ex['length']:<5} {ex['mean_s2']:<9.2f} {ex['author']:<22} {ex['era']:<20} {text_preview}")

    # ── Highest-intensity zones (mean S₂, min length 3) ────────────────────────
    intense_zones = [z for z in zone_examples if z["length"] >= 3]
    intense_zones.sort(key=lambda x: x["mean_s2"], reverse=True)
    print("\n=== TOP 15 MOST INTENSE ZONES (length≥3, ranked by mean S₂) ===")
    print(f"{'Len':<5} {'Mean S₂':<9} {'Max S₂':<9} {'Author':<22} {'Text'}")
    for ex in intense_zones[:15]:
        text_preview = repr(ex["text"])[:50]
        print(f"{ex['length']:<5} {ex['mean_s2']:<9.2f} {ex['max_s2']:<9.2f} {ex['author']:<22} {text_preview}")

    # ── Era breakdown ───────────────────────────────────────────────────────────
    print("\n=== ERA BREAKDOWN ===")
    print(f"{'Era':<25} {'Poems':<7} {'Spikes':<8} {'Zones':<8} {'Zone%':<8} "
          f"{'AvgZoneLen':<12} {'AvgZoneS₂'}")
    era_rows = []
    for era, stats in era_stats.items():
        sp = len(stats["spikes"])
        zo = len(stats["zones"])
        total = sp + zo
        zone_pct = 100 * zo / total if total else 0
        avg_len = (statistics.mean([z["length"] for z in stats["zones"]])
                   if stats["zones"] else 0)
        avg_s2 = (statistics.mean([z["mean_s2"] for z in stats["zones"]])
                  if stats["zones"] else 0)
        era_rows.append((era, stats["poems"], sp, zo, zone_pct, avg_len, avg_s2))

    era_rows.sort(key=lambda x: x[4], reverse=True)
    for row in era_rows:
        era, n_poems, sp, zo, zone_pct, avg_len, avg_s2 = row
        print(f"{era:<25} {n_poems:<7} {sp:<8} {zo:<8} {zone_pct:<8.1f} "
              f"{avg_len:<12.2f} {avg_s2:.3f}")

    # ── Correlation: zone length vs zone intensity ──────────────────────────────
    if len(all_zones) >= 10:
        # Spearman-like rank correlation
        paired = [(z["length"], z["mean_s2"]) for z in all_zones]
        lengths_r = [p[0] for p in paired]
        s2s_r = [p[1] for p in paired]
        n = len(paired)
        mean_l = statistics.mean(lengths_r)
        mean_s = statistics.mean(s2s_r)
        cov = sum((l - mean_l) * (s - mean_s) for l, s in zip(lengths_r, s2s_r)) / n
        std_l = statistics.stdev(lengths_r)
        std_s = statistics.stdev(s2s_r)
        corr = cov / (std_l * std_s) if std_l and std_s else 0
        print(f"\n=== ZONE LENGTH vs. ZONE INTENSITY ===")
        print(f"Pearson r (length vs mean_s2): {corr:.3f}  (n={n})")
        print("  r > 0: longer zones are more intense on average")
        print("  r < 0: longer zones dilute peak intensity (regression to mean)")

    # ── Zone inter-arrival gaps ─────────────────────────────────────────────────
    inter_gaps = []
    for poem in poems:
        token_data = poem.get("tokens", [])
        if not token_data:
            continue
        runs = find_runs(token_data, threshold=0.5)
        for k in range(len(runs) - 1):
            gap = runs[k + 1]["start_idx"] - (runs[k]["start_idx"] + runs[k]["length"])
            inter_gaps.append(gap)

    if inter_gaps:
        print(f"\n=== GAP BETWEEN CONSECUTIVE HIGH-S₂ EVENTS ===")
        print(f"n gaps: {len(inter_gaps)}")
        print(f"Mean gap:   {statistics.mean(inter_gaps):.2f} tokens")
        print(f"Median gap: {statistics.median(inter_gaps):.1f} tokens")
        print(f"Min gap:    {min(inter_gaps)} tokens")
        print(f"Max gap:    {max(inter_gaps)} tokens")
        short_gaps = sum(1 for g in inter_gaps if g <= 3)
        print(f"Gaps ≤ 3 tokens (tightly clustered): {short_gaps} ({100*short_gaps/len(inter_gaps):.1f}%)")

    # ── Poet-level zone rate ────────────────────────────────────────────────────
    poet_stats = defaultdict(lambda: {"spikes": 0, "zones": 0, "zone_s2": []})
    for poem in poems:
        author = poem.get("metadata", {}).get("author", "Unknown")
        token_data = poem.get("tokens", [])
        runs = find_runs(token_data, threshold=0.5)
        for r in runs:
            if r["length"] == 1:
                poet_stats[author]["spikes"] += 1
            else:
                poet_stats[author]["zones"] += 1
                poet_stats[author]["zone_s2"].append(r["mean_s2"])

    print("\n=== POET ZONE RATES (≥2 poems) ===")
    poet_rows = []
    seen_poets = defaultdict(int)
    for poem in poems:
        seen_poets[poem.get("metadata", {}).get("author", "")] += 1

    for author, stats in poet_stats.items():
        if seen_poets[author] < 2:
            continue
        total = stats["spikes"] + stats["zones"]
        if total < 5:
            continue
        zone_rate = 100 * stats["zones"] / total
        avg_zone_s2 = (statistics.mean(stats["zone_s2"])
                       if stats["zone_s2"] else 0)
        poet_rows.append((author, stats["spikes"], stats["zones"], zone_rate, avg_zone_s2))

    poet_rows.sort(key=lambda x: x[3], reverse=True)
    print(f"{'Author':<28} {'Spikes':<8} {'Zones':<8} {'Zone%':<8} {'AvgZoneS₂'}")
    for row in poet_rows[:20]:
        author, sp, zo, zone_rate, avg_s2 = row
        print(f"{author:<28} {sp:<8} {zo:<8} {zone_rate:<8.1f} {avg_s2:.3f}")

    return {
        "n_poems": len(poems),
        "n_spikes": n_spikes,
        "n_zones": n_zones,
        "pct_isolated": pct_isolated,
        "pct_zoned": pct_zoned,
        "zone_lengths": zone_lengths,
        "zone_mean_s2": zone_mean_s2,
        "spike_mean_s2": spike_s2,
        "top_zones": zone_examples[:20],
    }


if __name__ == "__main__":
    main()
