"""
S2 Spikiness Analysis — How "jagged" is a poem's surprise profile?

Instead of just average S2 (which most experiments use), this analyzes the
DISTRIBUTION of S2 within each poem:
  - std_s2 : standard deviation — the primary "spikiness" metric
  - max_s2  : the single most surprising token
  - range   : max_s2 - min_s2
  - peak_ratio : max_s2 / avg_s2 (how extreme is the peak vs average?)
  - coeff_var  : std_s2 / abs(avg_s2) — normalized variability

Hypotheses:
  1. Ballad/song poetry has low spikiness (rhythmic constraints reduce variance)
  2. Haiku and language poetry have high spikiness (concentrated moments)
  3. High avg_s2 and high spikiness correlate
  4. Prose control has low spikiness and low avg_s2
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")


def run_spikiness_analysis():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    poems = []
    for item in data:
        meta = item["metadata"]
        summary = item["summary"]
        era = meta.get("era", "unknown")
        if not era:
            era = "unknown"
        avg_s2 = summary["avg_s2"]
        std_s2 = summary["std_s2"]
        max_s2 = summary["max_s2"]
        min_s2 = summary["min_s2"]
        n = meta["n_tokens"]

        peak_ratio = max_s2 / avg_s2 if abs(avg_s2) > 0.01 else float("nan")
        s2_range = max_s2 - min_s2
        coeff_var = std_s2 / abs(avg_s2) if abs(avg_s2) > 0.01 else float("nan")

        poems.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": era,
            "avg_s2": avg_s2,
            "std_s2": std_s2,
            "max_s2": max_s2,
            "min_s2": min_s2,
            "peak_ratio": peak_ratio,
            "s2_range": s2_range,
            "coeff_var": coeff_var,
            "n_tokens": n,
        })

    # ── 1. Spikiness by era ──────────────────────────────────────────────────
    era_groups = {}
    for p in poems:
        era_groups.setdefault(p["era"], []).append(p)

    era_stats = []
    for era, ps in era_groups.items():
        avg_std = sum(p["std_s2"] for p in ps) / len(ps)
        avg_mean = sum(p["avg_s2"] for p in ps) / len(ps)
        avg_range = sum(p["s2_range"] for p in ps) / len(ps)
        avg_max = sum(p["max_s2"] for p in ps) / len(ps)
        era_stats.append({
            "era": era,
            "n": len(ps),
            "avg_s2": round(avg_mean, 3),
            "avg_std_s2": round(avg_std, 3),
            "avg_range": round(avg_range, 3),
            "avg_max_s2": round(avg_max, 3),
        })

    era_stats.sort(key=lambda x: x["avg_std_s2"], reverse=True)

    print("\n=== SPIKINESS BY ERA (sorted by std_s2, descending) ===\n")
    print(f"{'Era':<22} {'N':>3} {'Avg S2':>8} {'Std S2':>8} {'Range':>8} {'Max S2':>8}")
    print("-" * 65)
    for e in era_stats:
        print(f"{e['era']:<22} {e['n']:>3} {e['avg_s2']:>8.3f} {e['avg_std_s2']:>8.3f} {e['avg_range']:>8.3f} {e['avg_max_s2']:>8.3f}")

    # ── 2. Most and least spiky individual poems ──────────────────────────────
    sorted_by_std = sorted(poems, key=lambda p: p["std_s2"], reverse=True)
    # Exclude control prose
    poetry_only = [p for p in sorted_by_std if p["era"] != "control"]

    print("\n\n=== TOP 10 SPIKIEST POEMS (highest std_s2) ===\n")
    print(f"{'Title':<45} {'Author':<20} {'Era':<18} {'Std':>6} {'Avg':>6} {'Max':>6}")
    print("-" * 103)
    for p in poetry_only[:10]:
        print(f"{p['title'][:44]:<45} {p['author'][:19]:<20} {p['era']:<18} {p['std_s2']:>6.2f} {p['avg_s2']:>6.2f} {p['max_s2']:>6.2f}")

    print("\n\n=== TOP 10 MOST UNIFORM POEMS (lowest std_s2 in poetry) ===\n")
    print(f"{'Title':<45} {'Author':<20} {'Era':<18} {'Std':>6} {'Avg':>6} {'Max':>6}")
    print("-" * 103)
    for p in reversed(poetry_only[-10:]):
        print(f"{p['title'][:44]:<45} {p['author'][:19]:<20} {p['era']:<18} {p['std_s2']:>6.2f} {p['avg_s2']:>6.2f} {p['max_s2']:>6.2f}")

    # ── 3. Correlation: avg_s2 vs std_s2 ─────────────────────────────────────
    all_avg = [p["avg_s2"] for p in poems]
    all_std = [p["std_s2"] for p in poems]
    n = len(poems)
    mean_avg = sum(all_avg) / n
    mean_std = sum(all_std) / n
    cov = sum((a - mean_avg) * (s - mean_std) for a, s in zip(all_avg, all_std)) / n
    var_avg = sum((a - mean_avg) ** 2 for a in all_avg) / n
    var_std = sum((s - mean_std) ** 2 for s in all_std) / n
    r = cov / (var_avg ** 0.5 * var_std ** 0.5)

    print(f"\n\n=== CORRELATION: avg_s2 vs std_s2 ===")
    print(f"Pearson r = {r:.3f}")
    print(f"(+1 = high avg_s2 poems are always spiky; -1 = high avg_s2 poems are always uniform)")

    # ── 4. Spikiness quartiles ────────────────────────────────────────────────
    all_stds = sorted(p["std_s2"] for p in poetry_only)
    q1 = all_stds[len(all_stds) // 4]
    q2 = all_stds[len(all_stds) // 2]
    q3 = all_stds[3 * len(all_stds) // 4]

    print(f"\n\n=== S2 SPIKINESS DISTRIBUTION (poetry only, n={len(poetry_only)}) ===")
    print(f"  Q1 (25th pct): std_s2 = {q1:.2f}")
    print(f"  Q2 (median):   std_s2 = {q2:.2f}")
    print(f"  Q3 (75th pct): std_s2 = {q3:.2f}")
    print(f"  Min: {all_stds[0]:.2f} | Max: {all_stds[-1]:.2f}")

    # ── 5. Ballad special focus ───────────────────────────────────────────────
    ballads = [p for p in poems if p["era"] == "ballad"]
    if ballads:
        print(f"\n\n=== BALLAD FOCUS ===")
        for b in ballads:
            pct = sum(1 for x in all_stds if x < b["std_s2"]) / len(all_stds) * 100
            print(f"  '{b['title']}': std_s2={b['std_s2']:.3f} — {pct:.0f}th percentile (most uniform poetry)")

    # ── 6. Poems with extreme peaks (very high max_s2 but moderate avg) ──────
    print(f"\n\n=== POEMS WITH MOST CONCENTRATED PEAKS (high max/avg ratio) ===")
    peaked = [(p, p["max_s2"] / max(p["avg_s2"], 0.1)) for p in poetry_only if p["avg_s2"] > 0]
    peaked.sort(key=lambda x: x[1], reverse=True)
    print(f"{'Title':<45} {'Author':<20} {'Era':<18} {'Max':>6} {'Avg':>6} {'Ratio':>7}")
    print("-" * 108)
    for p, ratio in peaked[:10]:
        print(f"{p['title'][:44]:<45} {p['author'][:19]:<20} {p['era']:<18} {p['max_s2']:>6.2f} {p['avg_s2']:>6.2f} {ratio:>7.1f}×")

    return era_stats, poetry_only, r


if __name__ == "__main__":
    era_stats, poetry_only, r = run_spikiness_analysis()
