"""
Temporal Evolution of S2 across Literary History.

Research question: Does the average S2 (Straussian gap) — the gap between
what language expects and what the poet chooses — change systematically
across literary history? Are poets becoming *more* or *less* surprising
relative to the contextual confidence of GPT-2?

Method:
- Use only English-language poems (same base model, gpt2)
- Exclude control prose texts
- Group by decade (using the year field)
- Compute group statistics: avg_s2, pos_s2_ratio, avg_surprisal, avg_entropy
- Fit a linear trend to detect directional drift
"""

import json
import math
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"


def load_english_poems(path):
    with open(path) as f:
        data = json.load(f)
    poems = []
    for entry in data:
        meta = entry["metadata"]
        lang = meta.get("language", "en")
        era = meta.get("era", "")
        author = meta.get("author", "")
        if lang != "en":
            continue
        if era == "control" or author == "Control":
            continue
        year = meta.get("year")
        if year is None:
            continue
        poems.append({
            "title": meta["title"],
            "author": author,
            "year": year,
            "era": era,
            "summary": entry["summary"],
        })
    return poems


def assign_period(year):
    """Assign a human-readable literary period label."""
    if year < 1700:
        return "Pre-1700"
    elif year < 1800:
        return "1700–1799"
    elif year < 1850:
        return "1800–1849 (Romantic)"
    elif year < 1900:
        return "1850–1899 (Victorian/Post-Romantic)"
    elif year < 1930:
        return "1900–1929 (Modernist)"
    elif year < 1960:
        return "1930–1959 (Mid-Century)"
    elif year < 1980:
        return "1960–1979 (Postmodern)"
    elif year < 2000:
        return "1980–1999 (Language/Late Postmodern)"
    else:
        return "2000–present (Contemporary)"


def assign_decade(year):
    return (year // 10) * 10


def group_stats(poems_list):
    if not poems_list:
        return None
    avg_s2_vals = [p["summary"]["avg_s2"] for p in poems_list]
    pos_ratio_vals = [p["summary"]["pos_s2_ratio"] for p in poems_list]
    surprisal_vals = [p["summary"]["avg_surprisal"] for p in poems_list]
    entropy_vals = [p["summary"]["avg_entropy"] for p in poems_list]
    max_s2_vals = [p["summary"]["max_s2"] for p in poems_list]

    n = len(avg_s2_vals)
    mean = lambda xs: sum(xs) / len(xs)
    return {
        "n": n,
        "mean_avg_s2": mean(avg_s2_vals),
        "mean_pos_s2_ratio": mean(pos_ratio_vals),
        "mean_surprisal": mean(surprisal_vals),
        "mean_entropy": mean(entropy_vals),
        "mean_max_s2": mean(max_s2_vals),
        "poems": [(p["title"], p["author"], p["year"], p["summary"]["avg_s2"]) for p in poems_list],
    }


def linear_trend(xs, ys):
    """Simple OLS slope and intercept."""
    n = len(xs)
    if n < 2:
        return None, None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None, None
    slope = num / den
    intercept = my - slope * mx
    return slope, intercept


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mx) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - my) ** 2 for y in ys))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


def main():
    poems = load_english_poems(RESULTS_PATH)
    print(f"English non-control poems loaded: {len(poems)}")
    print()

    # By period
    by_period = defaultdict(list)
    for p in poems:
        period = assign_period(p["year"])
        by_period[period].append(p)

    period_order = [
        "Pre-1700",
        "1700–1799",
        "1800–1849 (Romantic)",
        "1850–1899 (Victorian/Post-Romantic)",
        "1900–1929 (Modernist)",
        "1930–1959 (Mid-Century)",
        "1960–1979 (Postmodern)",
        "1980–1999 (Language/Late Postmodern)",
        "2000–present (Contemporary)",
    ]

    print("=" * 80)
    print("TEMPORAL EVOLUTION OF S2 BY LITERARY PERIOD")
    print("=" * 80)
    print(f"{'Period':<40} {'N':>3}  {'Avg S2':>8}  {'Pos%':>6}  {'Surprisal':>10}  {'Entropy':>8}")
    print("-" * 80)

    period_summary = []
    for period in period_order:
        poems_in = by_period.get(period, [])
        if not poems_in:
            continue
        stats = group_stats(poems_in)
        print(f"{period:<40} {stats['n']:>3}  {stats['mean_avg_s2']:>+8.4f}  {stats['mean_pos_s2_ratio']*100:>5.1f}%  {stats['mean_surprisal']:>10.4f}  {stats['mean_entropy']:>8.4f}")
        # Use a representative year (midpoint or median)
        rep_year = sum(p["year"] for p in poems_in) / len(poems_in)
        period_summary.append((period, rep_year, stats))

    # Trend line over individual poems
    print()
    all_years = [p["year"] for p in poems]
    all_s2 = [p["summary"]["avg_s2"] for p in poems]
    slope, intercept = linear_trend(all_years, all_s2)
    r = pearson_r(all_years, all_s2)
    print(f"Linear trend (all poems): slope = {slope:+.6f} S2/year, r = {r:.4f}")
    print(f"  => Predicted S2 shift 1800→2017: {slope * (2017 - 1800):+.4f}")
    print()

    # Same for pos_s2_ratio
    all_pos = [p["summary"]["pos_s2_ratio"] for p in poems]
    slope_p, intercept_p = linear_trend(all_years, all_pos)
    r_p = pearson_r(all_years, all_pos)
    print(f"Linear trend (pos_s2_ratio): slope = {slope_p:+.6f}/year, r = {r_p:.4f}")
    print()

    # Per-poem detail table
    print("=" * 80)
    print("ALL POEMS — Year, Title, Author, AvgS2")
    print("=" * 80)
    sorted_poems = sorted(poems, key=lambda p: p["year"])
    for p in sorted_poems:
        s = p["summary"]
        print(f"  {p['year']:>5}  {p['title'][:40]:<40}  {p['author'][:24]:<24}  avg_s2={s['avg_s2']:>+7.4f}  pos%={s['pos_s2_ratio']*100:>5.1f}%")

    print()
    print("=" * 80)
    print("OUTLIERS: Highest and Lowest avg_s2")
    print("=" * 80)
    sorted_by_s2 = sorted(poems, key=lambda p: p["summary"]["avg_s2"])
    print("LOWEST avg_s2 (most predictable / compressed):")
    for p in sorted_by_s2[:5]:
        print(f"  {p['year']}  {p['title'][:40]}  {p['author']}  avg_s2={p['summary']['avg_s2']:+.4f}")
    print()
    print("HIGHEST avg_s2 (most Straussian / resistant):")
    for p in reversed(sorted_by_s2[-5:]):
        print(f"  {p['year']}  {p['title'][:40]}  {p['author']}  avg_s2={p['summary']['avg_s2']:+.4f}")

    return {
        "poems": poems,
        "period_summary": period_summary,
        "trend_slope_s2": slope,
        "trend_r_s2": r,
        "trend_slope_pos": slope_p,
        "trend_r_pos": r_p,
    }


if __name__ == "__main__":
    results = main()
