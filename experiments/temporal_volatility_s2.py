"""
Temporal Volatility of S2: How within-poem S2 spread changes across literary history.

The temporal_evolution study tracked mean S2 per era. This study adds the volatility
dimension (std_s2): do poets from certain eras show more or less variance in their
token-level surprisal profiles?

Hypothesis: Modernism may show *higher* volatility (extreme spikes against a conventional
backdrop) while Romanticism shows lower volatility (more uniform, elevated uncertainty).
"""

import json
import statistics
import sys

def load_data():
    with open("results/corpus_results.json") as f:
        return json.load(f)

ERA_ORDER = [
    "ancient", "old_english", "biblical", "metaphysical", "early_modern",
    "18th_century", "romantic", "victorian", "modernist", "imagist",
    "harlem_renaissance", "confessional", "mid_century", "beat",
    "new_york_school", "language", "postcolonial", "contemporary",
    "prose_poetry", "haiku", "japanese_classical",
]

DECADE_BINS = [
    (1600, 1699, "17th C"),
    (1700, 1799, "18th C"),
    (1800, 1849, "Early Romantic"),
    (1850, 1899, "Victorian"),
    (1900, 1929, "Modernist"),
    (1930, 1959, "Mid-Century"),
    (1960, 1979, "Postmodern"),
    (1980, 1999, "Late/Language"),
    (2000, 2026, "Contemporary"),
]

def bin_year(year):
    for lo, hi, label in DECADE_BINS:
        if lo <= year <= hi:
            return label
    return None

def analyze():
    data = load_data()

    # Filter to English poems with year and std_s2
    poems = []
    for item in data:
        meta = item["metadata"]
        summary = item["summary"]
        if meta.get("language", "en") != "en":
            continue
        year = meta.get("year")
        if year is None or year < 1600 or year > 2026:
            continue
        if "std_s2" not in summary:
            continue
        era = meta.get("era", "unknown")
        # Skip control/test corpora
        if era in ("control", "cliche_control", "parody", "parody_original",
                   "clerihew", "limerick", "double_dactyl", "nonsense",
                   "nursery_rhyme", "song_lyrics", "found_poetry"):
            continue
        poems.append({
            "title": meta["title"],
            "author": meta["author"],
            "year": year,
            "era": era,
            "decade_bin": bin_year(year),
            "avg_s2": summary["avg_s2"],
            "std_s2": summary["std_s2"],
            "max_s2": summary["max_s2"],
            "avg_surprisal": summary["avg_surprisal"],
            "pos_s2_ratio": summary["pos_s2_ratio"],
            "n_tokens": meta.get("n_tokens", 0),
        })

    print(f"Poems analyzed: {len(poems)}")

    # === Analysis 1: By decade bin ===
    from collections import defaultdict
    bins = defaultdict(list)
    for p in poems:
        if p["decade_bin"]:
            bins[p["decade_bin"]].append(p)

    print("\n=== Temporal Volatility by Period ===")
    print(f"{'Period':<20} {'N':>4} {'Mean S2':>8} {'Std S2 (mean)':>14} {'Max S2 (mean)':>14} {'Std S2 (SD)':>12}")
    print("-" * 76)

    period_results = []
    for lo, hi, label in DECADE_BINS:
        group = bins.get(label, [])
        if len(group) < 3:
            continue
        mean_s2 = statistics.mean(p["avg_s2"] for p in group)
        mean_std = statistics.mean(p["std_s2"] for p in group)
        mean_max = statistics.mean(p["max_s2"] for p in group)
        sd_std = statistics.stdev(p["std_s2"] for p in group) if len(group) > 1 else 0
        mid_year = (lo + hi) // 2
        print(f"{label:<20} {len(group):>4} {mean_s2:>8.3f} {mean_std:>14.3f} {mean_max:>14.3f} {sd_std:>12.3f}")
        period_results.append({
            "period": label, "mid_year": mid_year, "n": len(group),
            "mean_s2": round(mean_s2, 3), "mean_std_s2": round(mean_std, 3),
            "mean_max_s2": round(mean_max, 3), "sd_std_s2": round(sd_std, 3),
        })

    # === Analysis 2: Correlation year vs std_s2 ===
    years_with_std = [(p["year"], p["std_s2"]) for p in poems if p["decade_bin"]]
    n = len(years_with_std)
    xs = [x for x, _ in years_with_std]
    ys = [y for _, y in years_with_std]
    mean_x = statistics.mean(xs)
    mean_y = statistics.mean(ys)
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / n
    var_x = sum((x - mean_x) ** 2 for x in xs) / n
    var_y = sum((y - mean_y) ** 2 for y in ys) / n
    corr = cov / ((var_x * var_y) ** 0.5) if var_x * var_y > 0 else 0
    slope = cov / var_x if var_x > 0 else 0
    print(f"\n=== Linear Trend: Year vs Std_S2 ===")
    print(f"N = {n}, Pearson r = {corr:.4f}, slope = {slope:.6f} std_s2 per year")

    # === Analysis 3: Top volatile and stable poets ===
    from collections import defaultdict as dd
    poet_groups = dd(list)
    for p in poems:
        poet_groups[p["author"]].append(p)

    poet_stats = []
    for author, ps in poet_groups.items():
        if len(ps) < 2:
            continue
        poet_stats.append({
            "author": author,
            "n": len(ps),
            "mean_std_s2": statistics.mean(p["std_s2"] for p in ps),
            "mean_avg_s2": statistics.mean(p["avg_s2"] for p in ps),
            "era": ps[0]["era"],
            "year": ps[0]["year"],
        })

    poet_stats.sort(key=lambda x: x["mean_std_s2"], reverse=True)
    print("\n=== Most Volatile Poets (by mean std_s2 across poems) ===")
    print(f"{'Author':<30} {'N':>3} {'Mean Std_S2':>12} {'Mean Avg_S2':>12} {'Era':<20}")
    for p in poet_stats[:15]:
        print(f"{p['author']:<30} {p['n']:>3} {p['mean_std_s2']:>12.3f} {p['mean_avg_s2']:>12.3f} {p['era']:<20}")

    print("\n=== Most Stable Poets ===")
    for p in poet_stats[-10:]:
        print(f"{p['author']:<30} {p['n']:>3} {p['mean_std_s2']:>12.3f} {p['mean_avg_s2']:>12.3f} {p['era']:<20}")

    # === Analysis 4: Era-level mean_std vs mean_avg scatter ===
    print("\n=== Era: Mean S2 vs Volatility (S2/Volatility quadrant) ===")
    global_mean_s2 = statistics.mean(p["avg_s2"] for p in poems)
    global_mean_std = statistics.mean(p["std_s2"] for p in poems)
    print(f"Global mean S2 = {global_mean_s2:.3f}, global mean Std_S2 = {global_mean_std:.3f}")

    for r in period_results:
        q_s2 = "High S2" if r["mean_s2"] > global_mean_s2 else "Low S2"
        q_v = "HighVol" if r["mean_std_s2"] > global_mean_std else "LowVol"
        print(f"  {r['period']:<20}: {q_s2}, {q_v}  (S2={r['mean_s2']:.3f}, Std={r['mean_std_s2']:.3f})")

    # Save results
    results = {
        "n_poems": len(poems),
        "correlation_year_vs_std_s2": round(corr, 4),
        "slope_std_s2_per_year": round(slope, 6),
        "global_mean_s2": round(global_mean_s2, 3),
        "global_mean_std_s2": round(global_mean_std, 3),
        "period_results": period_results,
        "poet_stats": sorted(poet_stats, key=lambda x: x["mean_std_s2"], reverse=True),
    }
    with open("results/temporal_volatility_s2.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/temporal_volatility_s2.json")
    return results

if __name__ == "__main__":
    analyze()
