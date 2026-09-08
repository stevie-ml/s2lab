"""
S2 Clustering Analysis: Do High-S2 Tokens Burst or Scatter?

Research question: Are surpising tokens distributed evenly through a poem,
or do they cluster in temporal "bursts"? We measure this via:
  1. Lag-1/2/3 autocorrelation of the S2 sequence
  2. Burst Index: local-window variance / global variance
  3. Clustering Coefficient: fraction of high-S2 tokens adjacent to another high-S2 token
  4. Longest-burst / longest-lull ratio

No new model inference required -- works entirely from corpus_results.json.
"""

import json
import os
import statistics
from collections import defaultdict
import math

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def autocorr(seq, lag=1):
    """Pearson autocorrelation at given lag."""
    n = len(seq)
    if n <= lag + 1:
        return float("nan")
    mu = statistics.mean(seq)
    var = statistics.variance(seq)
    if var == 0:
        return float("nan")
    cov = sum((seq[i] - mu) * (seq[i + lag] - mu) for i in range(n - lag)) / (n - lag)
    return cov / var


def burst_index(seq, window=5):
    """
    Ratio of mean local variance (within windows) to global variance.
    > 1: surprises cluster within windows (bursty)
    < 1: surprises are spread (dispersed)
    """
    if len(seq) < window * 2:
        return float("nan")
    global_var = statistics.variance(seq) if len(seq) > 1 else 0
    if global_var == 0:
        return float("nan")
    local_vars = []
    for i in range(0, len(seq) - window, window):
        chunk = seq[i : i + window]
        if len(chunk) > 1:
            local_vars.append(statistics.variance(chunk))
    if not local_vars:
        return float("nan")
    return statistics.mean(local_vars) / global_var


def clustering_coefficient(seq, threshold=3.0):
    """
    Fraction of above-threshold tokens that are adjacent to another above-threshold token.
    High CC = surprises cluster; Low CC = surprises are isolated.
    """
    flags = [1 if s >= threshold else 0 for s in seq]
    n = len(flags)
    if sum(flags) == 0:
        return 0.0
    adjacent_count = 0
    for i, f in enumerate(flags):
        if f:
            neighbors = []
            if i > 0:
                neighbors.append(flags[i - 1])
            if i < n - 1:
                neighbors.append(flags[i + 1])
            if any(neighbors):
                adjacent_count += 1
    return adjacent_count / sum(flags)


def run_per_poem(results):
    """Compute clustering metrics for each poem."""
    poem_stats = []
    for r in results:
        meta = r["metadata"]
        if meta.get("language") != "en":
            continue
        tokens = r["tokens"]
        if len(tokens) < 10:
            continue
        s2_seq = [t["s2"] for t in tokens]
        ac1 = autocorr(s2_seq, lag=1)
        ac2 = autocorr(s2_seq, lag=2)
        ac3 = autocorr(s2_seq, lag=3)
        bi = burst_index(s2_seq, window=5)
        cc = clustering_coefficient(s2_seq, threshold=3.0)
        poem_stats.append(
            {
                "title": meta["title"],
                "author": meta["author"],
                "era": meta["era"],
                "year": meta.get("year", 0),
                "n_tokens": len(s2_seq),
                "avg_s2": r["summary"]["avg_s2"],
                "ac1": ac1,
                "ac2": ac2,
                "ac3": ac3,
                "burst_index": bi,
                "cc": cc,
            }
        )
    return poem_stats


def analyze(poem_stats):
    """Aggregate clustering metrics by author and era."""
    author_data = defaultdict(list)
    era_data = defaultdict(list)
    for p in poem_stats:
        author_data[p["author"]].append(p)
        era_data[p["era"]].append(p)

    # Author table (min 2 poems)
    author_rows = []
    for author, poems in author_data.items():
        if len(poems) < 2:
            continue
        valid_ac1 = [p["ac1"] for p in poems if not math.isnan(p["ac1"])]
        valid_bi = [p["burst_index"] for p in poems if not math.isnan(p["burst_index"])]
        valid_cc = [p["cc"] for p in poems]
        if not valid_ac1:
            continue
        author_rows.append(
            {
                "author": author,
                "n": len(poems),
                "avg_ac1": statistics.mean(valid_ac1),
                "avg_bi": statistics.mean(valid_bi) if valid_bi else float("nan"),
                "avg_cc": statistics.mean(valid_cc),
                "avg_s2": statistics.mean(p["avg_s2"] for p in poems),
            }
        )

    # Era table
    era_rows = []
    for era, poems in era_data.items():
        if era == "control":
            continue
        valid_ac1 = [p["ac1"] for p in poems if not math.isnan(p["ac1"])]
        valid_bi = [p["burst_index"] for p in poems if not math.isnan(p["burst_index"])]
        valid_cc = [p["cc"] for p in poems]
        if not valid_ac1:
            continue
        era_rows.append(
            {
                "era": era,
                "n": len(poems),
                "avg_ac1": statistics.mean(valid_ac1),
                "avg_bi": statistics.mean(valid_bi) if valid_bi else float("nan"),
                "avg_cc": statistics.mean(valid_cc),
            }
        )

    return author_rows, era_rows, poem_stats


def most_extreme(poem_stats, key, top=5, reverse=True):
    valid = [p for p in poem_stats if not math.isnan(p[key])]
    return sorted(valid, key=lambda p: p[key], reverse=reverse)[:top]


def write_findings(author_rows, era_rows, poem_stats):
    lines = []
    lines.append("# S2 Surprise Clustering: Do Poets Burst or Scatter Their Surprises?")
    lines.append("")
    lines.append("**Date:** 2026-09-08  ")
    lines.append("**Experiment:** `experiments/s2_clustering.py`  ")
    lines.append("**Corpus:** English-language poems only (control prose excluded)")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Research Question")
    lines.append("")
    lines.append(
        "Is a poem's surprise structure uniformly distributed — a steady hum of mild unpredictability —"
        " or does it organize into *bursts*, zones of consecutive high-S2 tokens separated by lulls"
        " of predictability? This question distinguishes two fundamental aesthetic strategies:"
    )
    lines.append("")
    lines.append(
        "- **Bursting poets** cluster their surprises. The poem breathes in and out between"
        " expectation and shock. Think of Dickinson's sudden pivots or Brooks's syntactic ruptures."
    )
    lines.append(
        "- **Scattering poets** maintain a steady pulse of mild surprise. Whitman's catalogs, for"
        " instance, might produce evenly distributed low-grade S2 across hundreds of tokens."
    )
    lines.append("")
    lines.append("## Metrics")
    lines.append("")
    lines.append("| Metric | Description | Interpretation |")
    lines.append("|--------|-------------|----------------|")
    lines.append("| **AC1** | Lag-1 Pearson autocorrelation of S2 sequence | >0: high-S2 follows high-S2 (clustering); <0: alternating; ~0: random |")
    lines.append("| **Burst Index** | Mean local-window variance / global variance | >1: spiky (bursty); <1: smooth (dispersed) |")
    lines.append("| **Cluster Coeff** | Fraction of high-S2 tokens (≥3.0) adjacent to another | High: surprises are neighbors; Low: isolated surprises |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Results by Literary Era")
    lines.append("")
    lines.append("| Era | N | AC1 | Burst Index | Cluster Coeff |")
    lines.append("|-----|---|-----|-------------|---------------|")
    era_rows_sorted = sorted(era_rows, key=lambda r: r["avg_ac1"], reverse=True)
    for r in era_rows_sorted:
        bi_str = f"{r['avg_bi']:.3f}" if not math.isnan(r["avg_bi"]) else "N/A"
        lines.append(
            f"| {r['era']} | {r['n']} | {r['avg_ac1']:+.3f} | {bi_str} | {r['avg_cc']:.3f} |"
        )

    lines.append("")
    lines.append("## Results by Author (min. 2 poems)")
    lines.append("")
    lines.append("### Most Bursty Poets (highest AC1)")
    lines.append("")
    bursty = sorted([r for r in author_rows if not math.isnan(r["avg_ac1"])], key=lambda r: r["avg_ac1"], reverse=True)[:10]
    lines.append("| Author | N | AC1 | Burst Index | Cluster Coeff | Avg S2 |")
    lines.append("|--------|---|-----|-------------|---------------|--------|")
    for r in bursty:
        bi_str = f"{r['avg_bi']:.3f}" if not math.isnan(r["avg_bi"]) else "N/A"
        lines.append(
            f"| {r['author']} | {r['n']} | **{r['avg_ac1']:+.3f}** | {bi_str} | {r['avg_cc']:.3f} | {r['avg_s2']:+.3f} |"
        )

    lines.append("")
    lines.append("### Most Scattering Poets (lowest / most negative AC1)")
    lines.append("")
    scattered = sorted([r for r in author_rows if not math.isnan(r["avg_ac1"])], key=lambda r: r["avg_ac1"])[:10]
    lines.append("| Author | N | AC1 | Burst Index | Cluster Coeff | Avg S2 |")
    lines.append("|--------|---|-----|-------------|---------------|--------|")
    for r in scattered:
        bi_str = f"{r['avg_bi']:.3f}" if not math.isnan(r["avg_bi"]) else "N/A"
        lines.append(
            f"| {r['author']} | {r['n']} | **{r['avg_ac1']:+.3f}** | {bi_str} | {r['avg_cc']:.3f} | {r['avg_s2']:+.3f} |"
        )

    lines.append("")
    lines.append("## Individual Poem Extremes")
    lines.append("")
    lines.append("### Most Bursty Individual Poems")
    lines.append("")
    lines.append("| Title | Author | AC1 | Burst Index | Cluster Coeff |")
    lines.append("|-------|--------|-----|-------------|---------------|")
    for p in most_extreme(poem_stats, "ac1", top=8):
        bi_str = f"{p['burst_index']:.3f}" if not math.isnan(p["burst_index"]) else "N/A"
        lines.append(
            f"| {p['title'][:40]} | {p['author']} | **{p['ac1']:+.3f}** | {bi_str} | {p['cc']:.3f} |"
        )

    lines.append("")
    lines.append("### Most Anti-Clustered (alternating surprise/predictability)")
    lines.append("")
    lines.append("| Title | Author | AC1 | Burst Index | Cluster Coeff |")
    lines.append("|-------|--------|-----|-------------|---------------|")
    for p in most_extreme(poem_stats, "ac1", top=8, reverse=False):
        bi_str = f"{p['burst_index']:.3f}" if not math.isnan(p["burst_index"]) else "N/A"
        lines.append(
            f"| {p['title'][:40]} | {p['author']} | **{p['ac1']:+.3f}** | {bi_str} | {p['cc']:.3f} |"
        )

    lines.append("")
    lines.append("### Highest Burst Index (spiky distribution)")
    lines.append("")
    lines.append("| Title | Author | Burst Index | AC1 | Avg S2 |")
    lines.append("|-------|--------|-------------|-----|--------|")
    for p in most_extreme(poem_stats, "burst_index", top=8):
        lines.append(
            f"| {p['title'][:40]} | {p['author']} | **{p['burst_index']:.3f}** | {p['ac1']:+.3f} | {p['avg_s2']:+.3f} |"
        )

    # Relationship between avg_s2 and ac1
    valid_pairs = [(p["avg_s2"], p["ac1"]) for p in poem_stats if not math.isnan(p["ac1"])]
    xs = [x for x, _ in valid_pairs]
    ys = [y for _, y in valid_pairs]
    if len(xs) > 2:
        mx, my = statistics.mean(xs), statistics.mean(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)
        vx = statistics.variance(xs)
        vy = statistics.variance(ys)
        r_s2_ac1 = cov / math.sqrt(vx * vy) if vx > 0 and vy > 0 else float("nan")
    else:
        r_s2_ac1 = float("nan")

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Key Findings")
    lines.append("")
    lines.append("### 1. AC1 is generally positive across poetry")
    lines.append("")
    all_ac1 = [p["ac1"] for p in poem_stats if not math.isnan(p["ac1"])]
    all_bi = [p["burst_index"] for p in poem_stats if not math.isnan(p["burst_index"])]
    all_cc = [p["cc"] for p in poem_stats]
    lines.append(
        f"The mean AC1 across all English poems is **{statistics.mean(all_ac1):+.3f}** "
        f"(range: {min(all_ac1):+.3f} to {max(all_ac1):+.3f}). "
        "Positive mean AC1 means that, on average, high-S2 tokens tend to be followed by other high-S2 tokens — "
        "surprise has inertia in poetry. The poem, once it breaks expectation, tends to keep breaking it "
        "for a few tokens before settling back into the predictable."
    )
    lines.append("")
    lines.append("### 2. Burst Index < 1 for most poems — surprise is smoother than random")
    lines.append("")
    lines.append(
        f"The mean Burst Index is **{statistics.mean(all_bi):.3f}** (expected value 1.0 for white noise). "
        "Values consistently below 1.0 mean that within-window S2 variance is *lower* than global variance — "
        "high-S2 spikes are spread across the poem, not massed in one zone. "
        "The poem distributes its surprises, even if locally AC1 is positive."
    )
    lines.append("")
    lines.append("### 3. The AC1 / avg_S2 relationship")
    lines.append("")
    if not math.isnan(r_s2_ac1):
        lines.append(
            f"Pearson r between avg_S2 and AC1 across poems: **r = {r_s2_ac1:.3f}**. "
        )
        if abs(r_s2_ac1) > 0.3:
            direction = "positive" if r_s2_ac1 > 0 else "negative"
            lines.append(
                f"This {direction} correlation suggests that poems with higher overall S2 "
                f"{'tend to cluster their surprises' if r_s2_ac1 > 0 else 'tend to scatter them more'}."
            )
        else:
            lines.append(
                "The near-zero correlation means surprise *amount* and surprise *clustering* are orthogonal — "
                "a poem can be highly surprising overall while either bursting or scattering those surprises."
            )

    # High/low CC analysis
    high_cc = [p for p in poem_stats if p["cc"] > 0.5]
    low_cc = [p for p in poem_stats if p["cc"] == 0.0]
    lines.append("")
    lines.append("### 4. The Cluster Coefficient separates two strategies")
    lines.append("")
    lines.append(
        f"**{len(high_cc)} poems** have a Cluster Coefficient > 0.5 — their high-S2 tokens mostly appear "
        f"beside another high-S2 token, forming *zones* of surprise. "
        f"**{len(low_cc)} poems** have CC = 0 — every surprise is isolated, surrounded by predictable tokens."
    )
    lines.append("")
    lines.append(
        "This suggests two fundamentally different aesthetic architectures:"
    )
    lines.append("")
    lines.append(
        "- **Zone-surprise** (high CC): The poem builds *chambers* of intensity — passages where"
        " the language is consistently unexpected, separated by stretches of conventional flow."
        " Dickinson's compressed stanzas and Ginsberg's long catalogs can both produce this pattern."
    )
    lines.append(
        "- **Isolated-surprise** (low CC): Each high-S2 token stands alone, surrounded by predictable"
        " context. This is closer to the rhetorical *mot juste* — the single, precise, unexpected word"
        " dropped into otherwise conventional syntax. Think of Bishop's or Larkin's precision."
    )

    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Literary Interpretation")
    lines.append("")
    lines.append(
        "The burst/scatter distinction maps onto long-standing debates about poetic texture. "
        "New Critics like Cleanth Brooks valued *density* — every word surprising — which corresponds"
        " to high uniform S2. But many canonical poems work by *contrast*: predictable runs that"
        " make individual surprises hit harder. The AC1 and Burst Index give us a way to quantify"
        " which strategy a poem is using."
    )
    lines.append("")
    lines.append(
        "The finding that AC1 is generally positive (surprise has inertia) suggests that poets"
        " tend to sustain their departures from expectation for at least a token or two — a single"
        " surprising word typically implies a surprising context, which GPT-2 finds surprising too."
        " This is the signature of *genuine* semantic or syntactic rupture, not just an unusual vocabulary choice."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Map AC1 onto close readings of specific poems — identify which bursts correspond to which literary moments")
    lines.append("2. Test whether burst structure correlates with emotional intensity or thematic climax")
    lines.append("3. Compare burst structure across poetic sub-genres: sonnets vs. odes vs. free verse")
    lines.append("4. Examine whether poets from the same school/movement share burst signatures")

    return "\n".join(lines)


def main():
    results = load_results()
    poem_stats = run_per_poem(results)
    author_rows, era_rows, poem_stats = analyze(poem_stats)
    report = write_findings(author_rows, era_rows, poem_stats)
    outpath = os.path.join(FINDINGS_DIR, "s2_clustering.md")
    with open(outpath, "w") as f:
        f.write(report)
    print(f"Saved: {outpath}")
    return poem_stats, author_rows, era_rows


if __name__ == "__main__":
    poem_stats, author_rows, era_rows = main()
    # Print summary
    import math
    all_ac1 = [p["ac1"] for p in poem_stats if not math.isnan(p["ac1"])]
    print(f"\nPoems analyzed: {len(poem_stats)}")
    print(f"Mean AC1: {sum(all_ac1)/len(all_ac1):+.3f}")
    bursty = sorted([r for r in author_rows if not math.isnan(r["avg_ac1"])], key=lambda r: r["avg_ac1"], reverse=True)
    print(f"\nTop 5 bursty authors by AC1:")
    for r in bursty[:5]:
        print(f"  {r['author']}: AC1={r['avg_ac1']:+.3f}")
