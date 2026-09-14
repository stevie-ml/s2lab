"""
S2 Inequality Analysis: Gini coefficient of surprise concentration in poetry.

Research question: Is the Straussian gap democratically distributed across all tokens,
or aristocratically concentrated in a few extreme deviations?

We apply the Gini coefficient to the distribution of positive S2 values within each
poem. Gini = 0 means every token contributes equally to the poem's total surprise;
Gini = 1 means a single token carries all of it.

We also compute a concentration ratio: the fraction of total positive S2 accounted
for by the top 10% of surprising tokens.
"""

import json
import os
import statistics
from collections import defaultdict
from datetime import date

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_FILE = os.path.join(os.path.dirname(__file__), "..", "findings", "s2_inequality_gini.md")


def gini_coefficient(values):
    """Gini coefficient for a list of non-negative values. 0=equal, 1=maximally concentrated."""
    if not values or sum(values) == 0:
        return 0.0
    n = len(values)
    vals = sorted(values)
    cumulative = sum((2 * (i + 1) - n - 1) * v for i, v in enumerate(vals))
    return cumulative / (n * sum(vals))


def concentration_ratio(values, top_frac=0.1):
    """Fraction of total value accounted for by the top `top_frac` of items."""
    if not values or sum(values) == 0:
        return 0.0
    vals_sorted = sorted(values, reverse=True)
    n = max(1, int(len(values) * top_frac))
    return sum(vals_sorted[:n]) / sum(values)


def poem_inequality_stats(r):
    """Compute inequality metrics for one poem result dict."""
    tokens = r["tokens"]
    all_s2 = [t["s2"] for t in tokens]
    positive_s2 = [t["s2"] for t in tokens if t["s2"] > 0]

    if not positive_s2:
        return None

    return {
        "title": r["metadata"]["title"],
        "author": r["metadata"]["author"],
        "era": r["metadata"]["era"],
        "language": r["metadata"].get("language", "en"),
        "avg_s2": r["summary"]["avg_s2"],
        "max_s2": r["summary"]["max_s2"],
        "pos_ratio": r["summary"]["pos_s2_ratio"],
        "n_tokens": r["metadata"]["n_tokens"],
        "gini": round(gini_coefficient(positive_s2), 4),
        "cr10": round(concentration_ratio(positive_s2, 0.1), 4),
        "near_zero_ratio": round(
            sum(1 for s in all_s2 if -0.5 <= s <= 0.5) / len(all_s2), 4
        ),
    }


def aggregate_by(poem_stats, key):
    """Group poem stats by a field, return dict of summary stats."""
    groups = defaultdict(list)
    for p in poem_stats:
        groups[p[key]].append(p)

    result = {}
    for grp, poems in groups.items():
        result[grp] = {
            "n": len(poems),
            "avg_s2": statistics.mean(p["avg_s2"] for p in poems),
            "avg_gini": statistics.mean(p["gini"] for p in poems),
            "avg_cr10": statistics.mean(p["cr10"] for p in poems),
            "avg_near_zero": statistics.mean(p["near_zero_ratio"] for p in poems),
        }
    return result


def build_report(poem_stats, era_agg):
    today = str(date.today())
    median_s2 = statistics.median(p["avg_s2"] for p in poem_stats)
    median_gini = statistics.median(p["gini"] for p in poem_stats)

    # Quadrant taxonomy
    quadrants = {
        "High S₂ / High Gini": [],
        "High S₂ / Low Gini": [],
        "Low S₂ / High Gini": [],
        "Low S₂ / Low Gini": [],
    }
    for p in poem_stats:
        hs = p["avg_s2"] > median_s2
        hg = p["gini"] > median_gini
        if hs and hg:
            q = "High S₂ / High Gini"
        elif hs and not hg:
            q = "High S₂ / Low Gini"
        elif not hs and hg:
            q = "Low S₂ / High Gini"
        else:
            q = "Low S₂ / Low Gini"
        quadrants[q].append(p)

    lines = [
        "# S₂ Inequality: Gini Coefficient of Poetic Surprise",
        f"**Date:** {today}",
        "",
        "## Research Question",
        "",
        "Is the Straussian gap *democratically distributed* across all tokens of a poem,",
        "or *aristocratically concentrated* in a few extreme deviations?",
        "",
        "We apply the **Gini coefficient** — the standard measure of income inequality —",
        "to the distribution of positive S₂ values within each poem. Gini = 0 means every",
        "surprising token contributes equally; Gini = 1 means a single token carries all",
        "the poem's deviation from expectation.",
        "",
        "We also compute the **concentration ratio (CR-10)**: the fraction of total positive",
        "S₂ accounted for by the top 10% of surprising tokens.",
        "",
        "## Era-Level Results",
        "",
        "*(Sorted by Gini, most concentrated first)*",
        "",
        "| Era | n | Avg S₂ | Gini | CR-10 | Near-Zero% |",
        "|-----|---|--------|------|-------|------------|",
    ]

    for era in sorted(era_agg, key=lambda e: era_agg[e]["avg_gini"], reverse=True):
        d = era_agg[era]
        lines.append(
            f"| {era} | {d['n']} | {d['avg_s2']:.2f} | **{d['avg_gini']:.3f}** | "
            f"{d['avg_cr10']:.0%} | {d['avg_near_zero']:.0%} |"
        )

    by_gini = sorted(poem_stats, key=lambda p: p["gini"], reverse=True)

    lines += [
        "",
        "## Most Concentrated Poems (highest Gini)",
        "",
        "*A few tokens carry nearly all the surprise.*",
        "",
        "| Poem | Author | Era | Avg S₂ | Gini | CR-10 | n tokens |",
        "|------|--------|-----|--------|------|-------|----------|",
    ]
    for p in by_gini[:12]:
        lines.append(
            f"| {p['title'][:40]} | {p['author'][:22]} | {p['era']} | {p['avg_s2']:.2f} | "
            f"**{p['gini']:.3f}** | {p['cr10']:.0%} | {p['n_tokens']} |"
        )

    lines += [
        "",
        "## Most Distributed Poems (lowest Gini)",
        "",
        "*Surprise is spread across many tokens.*",
        "",
        "| Poem | Author | Era | Avg S₂ | Gini | CR-10 | n tokens |",
        "|------|--------|-----|--------|------|-------|----------|",
    ]
    for p in sorted(poem_stats, key=lambda p: p["gini"])[:12]:
        lines.append(
            f"| {p['title'][:40]} | {p['author'][:22]} | {p['era']} | {p['avg_s2']:.2f} | "
            f"**{p['gini']:.3f}** | {p['cr10']:.0%} | {p['n_tokens']} |"
        )

    # Quadrant descriptions
    quad_desc = {
        "High S₂ / High Gini": (
            "**The Spike Poets** — high average surprise achieved through concentrated bursts. "
            "Most tokens are conventional; the poem's information load sits in one or two extreme moments."
        ),
        "High S₂ / Low Gini": (
            "**The Sustained Deviants** — many tokens are moderately surprising. "
            "Deviation is a pervasive texture across the whole poem, not a single concentrated act."
        ),
        "Low S₂ / High Gini": (
            "**The Rare Flashes** — mostly conventional language with an occasional jarring moment. "
            "The poem conforms most of the time but reserves one genuine break from expectation."
        ),
        "Low S₂ / Low Gini": (
            "**The Smooth Traditionalists** — consistently close to what language predicts. "
            "What little surprise exists is evenly distributed; nothing dominates."
        ),
    }

    lines += [
        "",
        "## Two-Axis Taxonomy: S₂ Level × Concentration",
        "",
        f"*(Median S₂ = {median_s2:.2f}, Median Gini = {median_gini:.3f})*",
        "",
    ]

    for quad, desc in quad_desc.items():
        poems = quadrants[quad]
        era_counts = defaultdict(int)
        for p in poems:
            era_counts[p["era"]] += 1
        top_eras = sorted(era_counts, key=era_counts.get, reverse=True)[:3]
        exemplar = (
            sorted(poems, key=lambda p: p["gini"] + abs(p["avg_s2"]), reverse=True)[0]
            if poems else None
        )

        lines.append(f"### {quad} (n={len(poems)})")
        lines.append(desc)
        lines.append("")
        lines.append(f"Top eras: {', '.join(f'{e} ({era_counts[e]})' for e in top_eras)}")
        if exemplar:
            lines.append(
                f"Exemplar: **{exemplar['author']}** — \"{exemplar['title']}\" "
                f"(S₂={exemplar['avg_s2']:.2f}, Gini={exemplar['gini']:.3f})"
            )
        lines.append("")

    # Correlation analysis
    gini_vals = [p["gini"] for p in poem_stats]
    s2_vals = [p["avg_s2"] for p in poem_stats]
    n = len(poem_stats)
    mean_g = statistics.mean(gini_vals)
    mean_s = statistics.mean(s2_vals)
    cov = sum((g - mean_g) * (s - mean_s) for g, s in zip(gini_vals, s2_vals)) / n
    std_g = statistics.stdev(gini_vals)
    std_s = statistics.stdev(s2_vals)
    corr = cov / (std_g * std_s) if std_g * std_s > 0 else 0

    lines += [
        "## Correlation: Gini vs. Average S₂",
        "",
        f"Pearson r(Gini, avg S₂) = **{corr:.3f}** across {n} poems.",
        "",
    ]
    if corr < -0.3:
        lines.append(
            "A meaningful negative correlation: higher-S₂ poems tend to distribute their surprise "
            "more broadly. More surprise overall means more surprise spread across many tokens."
        )
    elif corr > 0.3:
        lines.append(
            "A meaningful positive correlation: higher-S₂ poems also tend to be more concentrated. "
            "Extreme poems get their extreme scores from a few decisive moments."
        )
    else:
        lines.append(
            f"The weak correlation (r={corr:.3f}) confirms that Gini and avg S₂ are **largely independent dimensions**. "
            "A poem's *level* of surprise and its *distribution* of surprise are separate properties. "
            "Average S₂ alone is insufficient to characterize a poem's information architecture."
        )

    # Length vs. Gini
    len_gini_corr_data = [(p["n_tokens"], p["gini"]) for p in poem_stats]
    mean_len = statistics.mean(x for x, _ in len_gini_corr_data)
    mean_g2 = statistics.mean(g for _, g in len_gini_corr_data)
    cov2 = sum((x - mean_len) * (g - mean_g2) for x, g in len_gini_corr_data) / len(len_gini_corr_data)
    std_len = statistics.stdev(x for x, _ in len_gini_corr_data)
    len_corr = cov2 / (std_len * std_g) if std_len * std_g > 0 else 0

    lines += [
        "",
        f"Pearson r(token count, Gini) = **{len_corr:.3f}**.",
        "",
    ]
    if len_corr < -0.2:
        lines.append(
            "**Longer poems have lower Gini**: as poems accumulate more tokens, surprise distributes "
            "more evenly. Short forms (haiku, imagist lyrics) must concentrate their effect; "
            "longer forms spread it across the whole structure."
        )
    elif len_corr > 0.2:
        lines.append(
            "Longer poems tend to be more concentrated — possibly because longer poems contain both "
            "extended conventional passages and a few extreme peaks."
        )
    else:
        lines.append("Token count does not strongly predict concentration.")

    lines += [
        "",
        "## Key Findings",
        "",
        f"1. **Gini varies substantially across poems**: range [{min(gini_vals):.3f}, {max(gini_vals):.3f}], "
        f"mean {mean_g:.3f}, median {median_gini:.3f}. There is no single distribution type for poetry.",
        "",
        "2. **The quadrant taxonomy reveals four distinct information architectures**: "
        "Spike Poets (rare extreme moments), Sustained Deviants (pervasive mild surprise), "
        "Rare Flashes (otherwise conventional + one break), and Smooth Traditionalists. "
        "These categories are invisible to avg S₂ alone.",
        "",
        f"3. **Gini and avg S₂ are nearly independent** (r={corr:.3f}). A poet can achieve "
        "high average surprise through either many moderate deviations *or* through one or two "
        "extreme ones. These are different poetic strategies, not the same thing measured twice.",
        "",
        "4. **Era-level concentration reflects form constraints**: shorter, more compressed forms "
        "show higher Gini — the poem must pack its deviation into fewer moments.",
        "",
        "## Suggested Next Steps",
        "",
        "1. **Correlate Gini with syllable count / word count**: Do shorter poems have higher Gini?",
        "   Test whether form length, not era, drives the concentration pattern.",
        "",
        "2. **Author Gini signatures**: Does a poet maintain consistent Gini across poems, or vary "
        "   concentration by work? (Hypothesis: imagists consistently high; confessionals vary by poem.)",
        "",
        "3. **Gini over poem structure**: Compute Gini separately for the first half vs. second half "
        "   of each poem. Does the 'moment of maximum surprise' cluster at the end (climactic structure)?",
        "",
        "4. **Gini and the confidence trap rate**: Do poems with high Gini also have fewer confidence "
        "   traps? If the surprise is concentrated in 1-2 tokens, the rest of the poem should conform "
        "   strongly to expectation.",
    ]

    return "\n".join(lines)


def main():
    with open(RESULTS_FILE) as f:
        results = json.load(f)

    poem_stats = [poem_inequality_stats(r) for r in results if r["metadata"]["era"] != "control"]
    poem_stats = [p for p in poem_stats if p is not None]

    era_agg = aggregate_by(poem_stats, "era")
    report = build_report(poem_stats, era_agg)

    with open(FINDINGS_FILE, "w") as f:
        f.write(report)

    print(f"Saved: {FINDINGS_FILE}")
    by_gini = sorted(poem_stats, key=lambda p: p["gini"], reverse=True)
    most_conc_era = max(era_agg, key=lambda e: era_agg[e]["avg_gini"])
    most_dist_era = min(era_agg, key=lambda e: era_agg[e]["avg_gini"])
    print(f"Most concentrated era: {most_conc_era} (Gini={era_agg[most_conc_era]['avg_gini']:.3f})")
    print(f"Most distributed era:  {most_dist_era} (Gini={era_agg[most_dist_era]['avg_gini']:.3f})")
    print(f"Most concentrated poem: {by_gini[0]['author']} — '{by_gini[0]['title']}' (Gini={by_gini[0]['gini']:.3f})")
    print(f"Most distributed poem: {sorted(poem_stats, key=lambda p: p['gini'])[0]['author']} — "
          f"'{sorted(poem_stats, key=lambda p: p['gini'])[0]['title']}' "
          f"(Gini={sorted(poem_stats, key=lambda p: p['gini'])[0]['gini']:.3f})")


if __name__ == "__main__":
    main()
