"""
Career S2 Trajectory: Do individual poets' information-theoretic signatures
evolve over their careers?

Unlike temporal_evolution_s2.md (which tracks across literary periods),
this tracks WITHIN individual careers — asking whether poets become more or
less surprising as they mature.

Method:
1. Group corpus poems by author (English only, excludes controls)
2. For authors with ≥3 poems spanning ≥5 years, compute per-poem S2 metrics
3. Fit linear regression: metric ~ year_within_career (normalized 0→1)
4. Report slope direction and magnitude
5. Identify specific tokens that shift (conformist early vs radical late, etc.)
"""

import json
import sys
from collections import defaultdict
import statistics

DATA_PATH = "results/corpus_results.json"
ARTIFACT_THRESHOLD = 0.9  # p_newline threshold for stanza-break artifact

EXCLUDE_AUTHORS = {
    "Control", "Synthetic (research test case)"
}


def artifact_free_tokens(poem_data):
    return [
        t for t in poem_data["tokens"]
        if t.get("p_newline", 0) < ARTIFACT_THRESHOLD
    ]


def poem_metrics(poem_data):
    tokens = artifact_free_tokens(poem_data)
    if not tokens:
        return None
    s2_vals = [t["s2"] for t in tokens]
    pos_s2 = [v for v in s2_vals if v > 0]
    high_s2 = [v for v in s2_vals if v > 2]
    entropy_vals = [t["entropy"] for t in tokens]
    return {
        "avg_s2": statistics.mean(s2_vals),
        "median_s2": statistics.median(s2_vals),
        "std_s2": statistics.stdev(s2_vals) if len(s2_vals) > 1 else 0,
        "pos_s2_ratio": len(pos_s2) / len(s2_vals),
        "high_s2_ratio": len(high_s2) / len(s2_vals),
        "max_s2": max(s2_vals),
        "avg_entropy": statistics.mean(entropy_vals),
        "n_tokens": len(tokens),
    }


def linreg_slope(xs, ys):
    """Simple OLS slope (demeaned)."""
    n = len(xs)
    if n < 2:
        return 0.0
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return 0.0
    return num / den


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return None
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs)
    sy = statistics.stdev(ys)
    if sx == 0 or sy == 0:
        return None
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / ((n - 1) * sx * sy)


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Group poems by author (English only, exclude controls)
    author_poems = defaultdict(list)
    for poem in data:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue
        author = meta["author"]
        if author in EXCLUDE_AUTHORS:
            continue
        metrics = poem_metrics(poem)
        if metrics is None:
            continue
        metrics["title"] = meta["title"]
        metrics["year"] = meta["year"]
        author_poems[author].append(metrics)

    # Filter: ≥3 poems, career span ≥5 years
    qualifying = {}
    for author, poems in author_poems.items():
        if len(poems) < 3:
            continue
        years = [p["year"] for p in poems]
        span = max(years) - min(years)
        if span < 5:
            continue
        qualifying[author] = sorted(poems, key=lambda p: p["year"])

    print(f"\n{'='*70}")
    print("CAREER S2 TRAJECTORY ANALYSIS")
    print(f"{'='*70}")
    print(f"Qualifying authors (≥3 poems, span ≥5 years): {len(qualifying)}")

    # For each qualifying author, compute trajectory slopes
    results = []
    for author, poems in qualifying.items():
        years = [p["year"] for p in poems]
        min_year, max_year = min(years), max(years)
        span = max_year - min_year

        # Normalize year to 0..1 within career
        t = [(y - min_year) / span for y in years]

        for metric in ["avg_s2", "pos_s2_ratio", "high_s2_ratio", "std_s2", "avg_entropy"]:
            vals = [p[metric] for p in poems]
            slope = linreg_slope(t, vals)
            r = pearson_r(t, vals)
            results.append({
                "author": author,
                "metric": metric,
                "n_poems": len(poems),
                "span_years": span,
                "slope": slope,
                "r": r,
                "min_year": min_year,
                "max_year": max_year,
                "years": years,
                "vals": vals,
            })

    # Focus on avg_s2 trajectories
    avg_s2_results = [r for r in results if r["metric"] == "avg_s2"]
    avg_s2_results.sort(key=lambda x: abs(x["slope"] or 0), reverse=True)

    print("\n### Per-Author avg_S2 Trajectory (career-normalized slope)")
    print(f"{'Author':<32} {'Poems':>5} {'Span':>5} {'Slope':>8} {'r':>6}  Early→Late")
    print("-" * 75)
    for r in avg_s2_results:
        early = r["vals"][0]
        late = r["vals"][-1]
        direction = "↑" if r["slope"] > 0 else "↓"
        r_str = f"{r['r']:.2f}" if r["r"] is not None else "N/A"
        print(f"{r['author']:<32} {r['n_poems']:>5} {r['span_years']:>5} {r['slope']:>+8.3f} {r_str:>6}  {early:+.2f}→{late:+.2f} {direction}")

    # Also check pos_s2_ratio trajectory
    pos_results = [r for r in results if r["metric"] == "pos_s2_ratio"]
    pos_results.sort(key=lambda x: abs(x["slope"] or 0), reverse=True)
    print("\n### pos_S2_ratio Trajectory (fraction of positive-S2 tokens)")
    print(f"{'Author':<32} {'Slope':>8} {'r':>6}  Early%→Late%")
    print("-" * 60)
    for r in pos_results[:12]:
        early = r["vals"][0]
        late = r["vals"][-1]
        r_str = f"{r['r']:.2f}" if r["r"] is not None else "N/A"
        print(f"{r['author']:<32} {r['slope']:>+8.3f} {r_str:>6}  {early:.0%}→{late:.0%}")

    # Per-poem breakdown for most interesting authors
    print("\n\n### Detailed Career Breakdown: Top Authors by |slope|")
    seen = set()
    for r in sorted(results, key=lambda x: abs(x["slope"] or 0), reverse=True):
        if r["metric"] != "avg_s2":
            continue
        author = r["author"]
        if author in seen:
            continue
        seen.add(author)
        if len(seen) > 5:
            break
        poems = qualifying[author]
        print(f"\n#### {author} ({r['min_year']}–{r['max_year']}, {r['n_poems']} poems, slope={r['slope']:+.3f})")
        print(f"  {'Year':>6}  {'avg_S2':>8}  {'pos%':>6}  {'std_S2':>8}  {'max_S2':>8}  Title")
        for p in poems:
            print(f"  {p['year']:>6}  {p['avg_s2']:>+8.3f}  {p['pos_s2_ratio']:>6.0%}  {p['std_s2']:>8.3f}  {p['max_s2']:>8.3f}  {p['title']}")

    # Aggregate: Do poets generally become more or less surprising?
    print("\n\n### Aggregate: Direction of avg_S2 change over career")
    rising = sum(1 for r in avg_s2_results if r["slope"] > 0)
    falling = sum(1 for r in avg_s2_results if r["slope"] < 0)
    print(f"  Rising S2 over career:  {rising}/{len(avg_s2_results)} poets")
    print(f"  Falling S2 over career: {falling}/{len(avg_s2_results)} poets")
    all_slopes = [r["slope"] for r in avg_s2_results]
    print(f"  Mean slope: {statistics.mean(all_slopes):+.4f}")
    if len(all_slopes) > 1:
        print(f"  Stdev slopes: {statistics.stdev(all_slopes):.4f}")

    # Ashbery special case — most poems, widest range
    print("\n\n### Ashbery Case Study (most poems in corpus)")
    ashbery_poems = qualifying.get("John Ashbery", [])
    if ashbery_poems:
        print(f"  {'Year':>6}  {'avg_S2':>8}  {'pos%':>6}  {'high%':>6}  {'std_S2':>8}  Title")
        for p in ashbery_poems:
            print(f"  {p['year']:>6}  {p['avg_s2']:>+8.3f}  {p['pos_s2_ratio']:>6.0%}  {p['high_s2_ratio']:>6.0%}  {p['std_s2']:>8.3f}  {p['title']}")
        years_n = [p["year"] for p in ashbery_poems]
        t_n = [(y - min(years_n)) / (max(years_n) - min(years_n)) for y in years_n]
        for metric in ["avg_s2", "pos_s2_ratio", "high_s2_ratio", "std_s2"]:
            vals = [p[metric] for p in ashbery_poems]
            slope = linreg_slope(t_n, vals)
            r = pearson_r(t_n, vals)
            r_str = f"{r:.2f}" if r is not None else "N/A"
            print(f"  Ashbery {metric:<20} slope={slope:+.4f}  r={r_str}")

    return results, qualifying


if __name__ == "__main__":
    results, qualifying = main()
