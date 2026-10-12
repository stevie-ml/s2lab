"""
Surprise Economy: Does High Mean S2 Correlate with Spread-Out Surprises?

Hypothesis: Poems with high mean S2 (many surprises overall) should show
lower lag-1 autocorrelation — surprises are spread out, not clustered.
Poems with low mean S2 (few surprises) may cluster what few surprises they
have — like concentrated wealth in an unequal economy.

Uses existing corpus_results.json — no GPT-2 inference needed.
"""

import json
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
CORPUS_FILE = ROOT / "results" / "corpus_results.json"

def lag_ac(series, lag=1):
    """Pearson autocorrelation at given lag."""
    n = len(series)
    if n < lag + 10:
        return None
    x = series[:-lag]
    y = series[lag:]
    mx = statistics.mean(x)
    my = statistics.mean(y)
    sx = statistics.stdev(x)
    sy = statistics.stdev(y)
    if sx == 0 or sy == 0:
        return None
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y)) / len(x)
    return cov / (sx * sy)

def artifact_free(tokens):
    """Return s2 values for tokens that are not stanza-break artifacts."""
    return [t["s2"] for t in tokens if t.get("p_newline", 0) < 0.9]

def gini(values):
    """Gini coefficient of absolute S2 values (measure of inequality)."""
    vals = sorted(abs(v) for v in values if v is not None)
    if not vals:
        return None
    n = len(vals)
    cumsum = 0
    for i, v in enumerate(vals):
        cumsum += v * (2 * i - n + 1)
    return cumsum / (n * sum(vals)) if sum(vals) > 0 else 0

def pearson(xs, ys):
    """Pearson correlation between two lists."""
    n = len(xs)
    if n < 5:
        return None, None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs)
    sy = statistics.stdev(ys)
    if sx == 0 or sy == 0:
        return None, None
    corr = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)
    # approximate p-value via t-distribution
    t_stat = corr * math.sqrt(n - 2) / math.sqrt(max(1e-12, 1 - corr**2))
    return corr, t_stat

def main():
    data = json.loads(CORPUS_FILE.read_text())

    results = []
    for poem in data:
        meta = poem["metadata"]
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        af = artifact_free(tokens)
        if len(af) < 15:
            continue

        mean_s2 = statistics.mean(af)
        std_s2 = statistics.stdev(af) if len(af) > 1 else 0
        pos_ratio = sum(1 for v in af if v > 0) / len(af)
        ac1 = lag_ac(af, lag=1)
        ac2 = lag_ac(af, lag=2)
        gini_val = gini(af)

        # "Surprise concentration": how much of the total positive S2 mass
        # is concentrated in the top 10% of tokens?
        pos_vals = sorted([v for v in af if v > 0], reverse=True)
        if pos_vals:
            top10_n = max(1, len(pos_vals) // 10)
            top10_mass = sum(pos_vals[:top10_n])
            total_pos = sum(pos_vals)
            concentration = top10_mass / total_pos if total_pos > 0 else 0
        else:
            concentration = 1.0

        results.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta["era"],
            "n_af": len(af),
            "mean_s2": round(mean_s2, 4),
            "std_s2": round(std_s2, 4),
            "pos_ratio": round(pos_ratio, 4),
            "lag1_ac": round(ac1, 4) if ac1 is not None else None,
            "lag2_ac": round(ac2, 4) if ac2 is not None else None,
            "gini": round(gini_val, 4) if gini_val is not None else None,
            "top10_concentration": round(concentration, 4),
        })

    print(f"Poems analyzed: {len(results)}")

    # Global correlation: mean_s2 vs lag1_ac
    valid_ac = [(row["mean_s2"], row["lag1_ac"]) for row in results
                if row["lag1_ac"] is not None]
    corr_ac, t_ac = pearson([v[0] for v in valid_ac], [v[1] for v in valid_ac])
    print(f"\n== Global: mean S2 vs lag-1 AC ==")
    print(f"N = {len(valid_ac)}, r = {corr_ac:.4f}, t = {t_ac:.2f}")
    if corr_ac is not None:
        direction = "NEGATIVE (high S2 → spread surprises)" if corr_ac < 0 else "POSITIVE (high S2 → clustered surprises)"
        print(f"Direction: {direction}")

    # Mean S2 vs Gini
    valid_g = [(row["mean_s2"], row["gini"]) for row in results if row["gini"] is not None]
    corr_gini, t_gini = pearson([v[0] for v in valid_g], [v[1] for v in valid_g])
    print(f"\n== Global: mean S2 vs Gini inequality ==")
    print(f"N = {len(valid_g)}, r = {corr_gini:.4f}, t = {t_gini:.2f}")

    # Mean S2 vs concentration
    valid_c = [(row["mean_s2"], row["top10_concentration"]) for row in results]
    corr_conc, t_conc = pearson([v[0] for v in valid_c], [v[1] for v in valid_c])
    print(f"\n== Global: mean S2 vs top-10% concentration ==")
    print(f"N = {len(valid_c)}, r = {corr_conc:.4f}, t = {t_conc:.2f}")

    # Stratify by quartile of mean S2
    results_sorted = sorted(results, key=lambda x: x["mean_s2"])
    n = len(results_sorted)
    q1 = results_sorted[:n//4]
    q2 = results_sorted[n//4:n//2]
    q3 = results_sorted[n//2:3*n//4]
    q4 = results_sorted[3*n//4:]

    print(f"\n== Quartile Analysis ==")
    print(f"{'Quartile':<12} {'n':>4} {'mean S2':>9} {'mean lag1-AC':>14} {'mean Gini':>11} {'top10 conc':>12}")
    for label, group in [("Q1 (low)", q1), ("Q2", q2), ("Q3", q3), ("Q4 (high)", q4)]:
        ac_vals = [row["lag1_ac"] for row in group if row["lag1_ac"] is not None]
        g_vals = [row["gini"] for row in group if row["gini"] is not None]
        c_vals = [row["top10_concentration"] for row in group]
        print(
            f"{label:<12} "
            f"{len(group):>4} "
            f"{statistics.mean(row['mean_s2'] for row in group):>9.3f} "
            f"{statistics.mean(ac_vals) if ac_vals else 0:>14.4f} "
            f"{statistics.mean(g_vals) if g_vals else 0:>11.4f} "
            f"{statistics.mean(c_vals):>12.4f}"
        )

    # Era-level: compare mean S2 and lag-1 AC
    era_data = defaultdict(list)
    for row in results:
        era_data[row["era"]].append(row)

    print(f"\n== Era-Level: mean S2 vs lag-1 AC ==")
    era_rows = []
    for era, group in era_data.items():
        if len(group) < 2:
            continue
        era_mean_s2 = statistics.mean(row["mean_s2"] for row in group)
        ac_vals = [row["lag1_ac"] for row in group if row["lag1_ac"] is not None]
        mean_ac = statistics.mean(ac_vals) if ac_vals else None
        gini_vals = [row["gini"] for row in group if row["gini"] is not None]
        mean_gini = statistics.mean(gini_vals) if gini_vals else None
        conc_vals = [row["top10_concentration"] for row in group]
        mean_conc = statistics.mean(conc_vals)
        era_rows.append({
            "era": era,
            "n": len(group),
            "mean_s2": round(era_mean_s2, 3),
            "mean_ac1": round(mean_ac, 4) if mean_ac is not None else None,
            "mean_gini": round(mean_gini, 4) if mean_gini is not None else None,
            "mean_conc": round(mean_conc, 4),
        })

    era_rows.sort(key=lambda x: x["mean_s2"], reverse=True)
    print(f"{'Era':<22} {'n':>4} {'mean S2':>9} {'lag1-AC':>9} {'Gini':>8} {'top10%':>8}")
    for er in era_rows:
        print(
            f"{er['era']:<22} "
            f"{er['n']:>4} "
            f"{er['mean_s2']:>9.3f} "
            f"{er['mean_ac1'] if er['mean_ac1'] is not None else 'N/A':>9} "
            f"{er['mean_gini'] if er['mean_gini'] is not None else 'N/A':>8} "
            f"{er['mean_conc']:>8.4f}"
        )

    # Top/bottom poems by concentration
    results_sorted_conc = sorted(results, key=lambda x: x["top10_concentration"])
    print(f"\n== Most Egalitarian Surprises (lowest top-10% concentration) ==")
    for row in results_sorted_conc[:10]:
        print(f"  {row['title'][:45]:<45} {row['author'][:25]:<25} mean_s2={row['mean_s2']:+.3f} conc={row['top10_concentration']:.3f} ac1={row['lag1_ac']}")

    print(f"\n== Most Concentrated Surprises (highest top-10% concentration) ==")
    for row in results_sorted_conc[-10:]:
        print(f"  {row['title'][:45]:<45} {row['author'][:25]:<25} mean_s2={row['mean_s2']:+.3f} conc={row['top10_concentration']:.3f} ac1={row['lag1_ac']}")

    # Era correlation test
    era_s2 = [er["mean_s2"] for er in era_rows if er["mean_ac1"] is not None]
    era_ac = [er["mean_ac1"] for er in era_rows if er["mean_ac1"] is not None]
    era_corr, era_t = pearson(era_s2, era_ac)
    print(f"\n== Era-level correlation: mean S2 vs lag-1 AC ==")
    print(f"N eras = {len(era_s2)}, r = {era_corr:.4f}, t = {era_t:.2f}")

    # Save results
    out = {
        "n_poems": len(results),
        "global_correlations": {
            "mean_s2_vs_lag1_ac": {"r": round(corr_ac, 4) if corr_ac is not None else None,
                                    "t": round(t_ac, 2) if t_ac is not None else None,
                                    "n": len(valid_ac)},
            "mean_s2_vs_gini": {"r": round(corr_gini, 4) if corr_gini is not None else None,
                                 "t": round(t_gini, 2) if t_gini is not None else None,
                                 "n": len(valid_g)},
            "mean_s2_vs_top10_conc": {"r": round(corr_conc, 4) if corr_conc is not None else None,
                                       "t": round(t_conc, 2) if t_conc is not None else None,
                                       "n": len(valid_c)},
        },
        "quartile_analysis": [
            {"quartile": "Q1_low",
             "mean_s2": round(statistics.mean(row["mean_s2"] for row in q1), 3),
             "mean_ac1": round(statistics.mean(row["lag1_ac"] for row in q1 if row["lag1_ac"] is not None), 4),
             "mean_conc": round(statistics.mean(row["top10_concentration"] for row in q1), 4)},
            {"quartile": "Q2",
             "mean_s2": round(statistics.mean(row["mean_s2"] for row in q2), 3),
             "mean_ac1": round(statistics.mean(row["lag1_ac"] for row in q2 if row["lag1_ac"] is not None), 4),
             "mean_conc": round(statistics.mean(row["top10_concentration"] for row in q2), 4)},
            {"quartile": "Q3",
             "mean_s2": round(statistics.mean(row["mean_s2"] for row in q3), 3),
             "mean_ac1": round(statistics.mean(row["lag1_ac"] for row in q3 if row["lag1_ac"] is not None), 4),
             "mean_conc": round(statistics.mean(row["top10_concentration"] for row in q3), 4)},
            {"quartile": "Q4_high",
             "mean_s2": round(statistics.mean(row["mean_s2"] for row in q4), 3),
             "mean_ac1": round(statistics.mean(row["lag1_ac"] for row in q4 if row["lag1_ac"] is not None), 4),
             "mean_conc": round(statistics.mean(row["top10_concentration"] for row in q4), 4)},
        ],
        "era_data": era_rows,
        "era_level_correlation": {"r": round(era_corr, 4) if era_corr is not None else None,
                                   "t": round(era_t, 2) if era_t is not None else None,
                                   "n": len(era_s2)},
        "per_poem": results,
    }

    out_file = ROOT / "results" / "surprise_economy.json"
    out_file.write_text(json.dumps(out, indent=2))
    print(f"\nSaved to {out_file}")
    return out

if __name__ == "__main__":
    main()
