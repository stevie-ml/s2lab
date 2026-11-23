"""
Line-Level S2 Momentum
======================
Token-level autocorrelation of S2 has been studied (s2_autocorrelation.md).
This experiment asks the same question at the LINE level:

  Within a poem, do high-S2 lines tend to be followed by high-S2 lines
  (clustering / positive momentum) or by low-S2 lines (alternation / recovery)?

Method:
- Reconstruct per-line S2 sequences from token data
- Use artifact-free S2 (exclude tokens where p_newline > 0.9)
- For each poem with ≥5 non-empty lines, compute lag-1 Pearson autocorrelation
- Aggregate momentum by poet, era, and form
- Identify representative poems at both extremes

Hypothesis: Lyric poems will show positive momentum (sustained high-S2 runs),
while ballads / fixed forms may show alternation (high and low lines interleave
per their formal constraints).
"""

import json
import math
import statistics
from collections import defaultdict

ARTIFACT_THRESHOLD = 0.9  # exclude tokens where p(newline) > this
MIN_LINES = 5             # minimum non-empty lines for autocorrelation
MIN_TOKENS_PER_LINE = 2   # skip very short lines (single punctuation etc.)


def pearson_lag1(seq):
    """Lag-1 Pearson autocorrelation of a sequence."""
    n = len(seq)
    if n < 3:
        return None
    x = seq[:-1]
    y = seq[1:]
    mx, my = statistics.mean(x), statistics.mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    sx = math.sqrt(sum((xi - mx) ** 2 for xi in x))
    sy = math.sqrt(sum((yi - my) ** 2 for yi in y))
    if sx == 0 or sy == 0:
        return None
    return num / (sx * sy)


def poem_line_s2_series(poem):
    """Return list of per-line mean artifact-free S2 values."""
    tokens = poem["tokens"]
    lines = []
    current_line = []

    for t in tokens:
        is_newline = (t["token"] == "\n" or t["token"].startswith("\n"))
        if is_newline:
            if len(current_line) >= MIN_TOKENS_PER_LINE:
                lines.append(current_line)
            current_line = []
        elif t["p_newline"] <= ARTIFACT_THRESHOLD:
            current_line.append(t["s2"])

    # flush last line
    if len(current_line) >= MIN_TOKENS_PER_LINE:
        lines.append(current_line)

    return [statistics.mean(line) for line in lines]


def classify_momentum(r):
    if r is None:
        return "insufficient data"
    if r >= 0.3:
        return "strong clustering"
    elif r >= 0.1:
        return "mild clustering"
    elif r >= -0.1:
        return "neutral"
    elif r >= -0.3:
        return "mild alternation"
    else:
        return "strong alternation"


def main():
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    poem_results = []
    era_results = defaultdict(list)
    author_results = defaultdict(list)

    for poem in corpus:
        meta = poem["metadata"]
        line_series = poem_line_s2_series(poem)

        if len(line_series) < MIN_LINES:
            continue

        r = pearson_lag1(line_series)
        if r is None:
            continue

        result = {
            "title": meta.get("title", "?"),
            "author": meta.get("author", "?"),
            "era": meta.get("era", "?"),
            "n_lines": len(line_series),
            "mean_s2": statistics.mean(line_series),
            "s2_std": statistics.stdev(line_series) if len(line_series) > 1 else 0,
            "lag1_autocorr": r,
            "classification": classify_momentum(r),
            "line_series": line_series,
        }
        poem_results.append(result)
        era_results[meta.get("era", "?")].append(r)
        author_results[meta.get("author", "?")].append(r)

    # Sort
    poem_results.sort(key=lambda x: x["lag1_autocorr"], reverse=True)

    print(f"Poems analyzed: {len(poem_results)}")
    print(f"\n--- Top 10 clustering poems (high positive momentum) ---")
    for p in poem_results[:10]:
        print(f"  r={p['lag1_autocorr']:.3f}  {p['author']} — {p['title']} ({p['n_lines']} lines)")

    print(f"\n--- Top 10 alternating poems (strong negative momentum) ---")
    for p in reversed(poem_results[-10:]):
        print(f"  r={p['lag1_autocorr']:.3f}  {p['author']} — {p['title']} ({p['n_lines']} lines)")

    print(f"\n--- Era-level momentum ---")
    era_means = {era: (statistics.mean(rs), len(rs)) for era, rs in era_results.items() if len(rs) >= 2}
    for era, (mean_r, n) in sorted(era_means.items(), key=lambda x: -x[1][0])[:20]:
        print(f"  {era}: mean r={mean_r:.3f}  (n={n} poems)")

    print(f"\n--- Author-level momentum (≥3 poems) ---")
    author_means = {a: (statistics.mean(rs), len(rs)) for a, rs in author_results.items() if len(rs) >= 3}
    for author, (mean_r, n) in sorted(author_means.items(), key=lambda x: -x[1][0]):
        print(f"  {author}: mean r={mean_r:.3f}  (n={n} poems)")

    # Classification breakdown
    classes = defaultdict(int)
    for p in poem_results:
        classes[p["classification"]] += 1
    print(f"\n--- Momentum classification breakdown ---")
    for cls, count in sorted(classes.items(), key=lambda x: -x[1]):
        pct = count / len(poem_results) * 100
        print(f"  {cls}: {count} ({pct:.0f}%)")

    overall_r = [p["lag1_autocorr"] for p in poem_results]
    print(f"\n--- Overall statistics ---")
    print(f"  N poems: {len(overall_r)}")
    print(f"  Mean r: {statistics.mean(overall_r):.4f}")
    print(f"  Median r: {statistics.median(overall_r):.4f}")
    print(f"  Stdev r: {statistics.stdev(overall_r):.4f}")
    print(f"  % positive: {sum(1 for r in overall_r if r > 0) / len(overall_r) * 100:.0f}%")
    print(f"  % strongly clustering (r≥0.3): {sum(1 for r in overall_r if r >= 0.3) / len(overall_r) * 100:.0f}%")
    print(f"  % strongly alternating (r≤-0.3): {sum(1 for r in overall_r if r <= -0.3) / len(overall_r) * 100:.0f}%")

    # Save results
    output = {
        "poems": [
            {k: v for k, v in p.items() if k != "line_series"}
            for p in poem_results
        ],
        "era_means": {era: {"mean_r": mr, "n": n} for era, (mr, n) in era_means.items()},
        "author_means": {a: {"mean_r": mr, "n": n} for a, (mr, n) in author_means.items()},
        "overall": {
            "n": len(overall_r),
            "mean_r": statistics.mean(overall_r),
            "median_r": statistics.median(overall_r),
            "stdev_r": statistics.stdev(overall_r),
        }
    }
    with open("results/line_s2_momentum.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/line_s2_momentum.json")


if __name__ == "__main__":
    main()
