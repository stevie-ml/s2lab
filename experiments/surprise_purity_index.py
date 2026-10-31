"""
Surprise Purity Index (SPI): Measuring the Quality of the Straussian Gap

The Straussian gap (S2 = S - H) captures moments where a poet surprises a confident model.
But not all high-S2 moments are equal:
- "Pure" surprise: the model was confident (low H), yet the poet defied it (high S2)
- "Noisy" surprise: the model was already uncertain (high H), so any deviation scores S2

SPI = fraction of high-S2 tokens in which the model had low entropy (was confident but wrong).

This distinguishes poets who achieve genuine defiance-of-expectation from those who
merely operate in uncertain semantic territory where the model is confused anyway.
"""

import json
import math
from collections import defaultdict

CORPUS = "results/corpus_results.json"
OUTPUT = "results/surprise_purity_index.json"
FINDING = "findings/surprise_purity_index.md"

S2_THRESHOLD = 3.0          # token is "surprising"
P_NEWLINE_MAX = 0.9         # artifact filter (stanza-break artifact)
MIN_POEMS = 2               # minimum poems per poet to include in per-poet analysis


def load_corpus():
    with open(CORPUS) as f:
        return json.load(f)


def compute_entropy_percentile(corpus, pct=33):
    """Compute global Nth-percentile of entropy across all non-artifact tokens."""
    all_H = []
    for poem in corpus:
        for tok in poem["tokens"]:
            if tok["p_newline"] < P_NEWLINE_MAX:
                all_H.append(tok["entropy"])
    all_H.sort()
    idx = int(len(all_H) * pct / 100)
    return all_H[idx]


def analyze_poem(poem, confident_threshold):
    """
    Returns per-poem SPI stats.
    Returns None if no high-S2 tokens found.
    """
    high_s2_total = 0
    high_s2_confident = 0   # high-S2 AND low-H (pure surprise)
    high_s2_uncertain = 0   # high-S2 AND high-H (noisy surprise)

    for tok in poem["tokens"]:
        if tok["p_newline"] >= P_NEWLINE_MAX:
            continue
        if tok["s2"] >= S2_THRESHOLD:
            high_s2_total += 1
            if tok["entropy"] < confident_threshold:
                high_s2_confident += 1
            else:
                high_s2_uncertain += 1

    if high_s2_total == 0:
        return None

    spi = high_s2_confident / high_s2_total
    return {
        "spi": round(spi, 4),
        "high_s2_total": high_s2_total,
        "high_s2_confident": high_s2_confident,
        "high_s2_uncertain": high_s2_uncertain,
    }


def era_analysis(corpus, confident_threshold):
    era_data = defaultdict(lambda: {"spi_vals": [], "avg_s2_vals": [], "n_poems": 0})
    for poem in corpus:
        meta = poem["metadata"]
        era = meta["era"]
        res = analyze_poem(poem, confident_threshold)
        if res is None:
            continue
        era_data[era]["spi_vals"].append(res["spi"])
        era_data[era]["avg_s2_vals"].append(poem["summary"]["avg_s2"])
        era_data[era]["n_poems"] += 1

    rows = []
    for era, d in era_data.items():
        n = len(d["spi_vals"])
        if n == 0:
            continue
        rows.append({
            "era": era,
            "n_poems": n,
            "mean_spi": round(sum(d["spi_vals"]) / n, 4),
            "mean_avg_s2": round(sum(d["avg_s2_vals"]) / n, 4),
        })
    rows.sort(key=lambda r: -r["mean_spi"])
    return rows


def poet_analysis(corpus, confident_threshold):
    poet_data = defaultdict(lambda: {
        "spi_vals": [], "avg_s2_vals": [], "era": None, "n_poems": 0
    })
    for poem in corpus:
        meta = poem["metadata"]
        author = meta["author"]
        era = meta["era"]
        res = analyze_poem(poem, confident_threshold)
        if res is None:
            continue
        poet_data[author]["spi_vals"].append(res["spi"])
        poet_data[author]["avg_s2_vals"].append(poem["summary"]["avg_s2"])
        if poet_data[author]["era"] is None:
            poet_data[author]["era"] = era
        poet_data[author]["n_poems"] += 1

    rows = []
    for author, d in poet_data.items():
        n = len(d["spi_vals"])
        if n < MIN_POEMS:
            continue
        rows.append({
            "author": author,
            "era": d["era"],
            "n_poems": n,
            "mean_spi": round(sum(d["spi_vals"]) / n, 4),
            "mean_avg_s2": round(sum(d["avg_s2_vals"]) / n, 4),
        })
    rows.sort(key=lambda r: -r["mean_spi"])
    return rows


def poem_analysis(corpus, confident_threshold):
    """Top and bottom poems by SPI."""
    rows = []
    for poem in corpus:
        meta = poem["metadata"]
        res = analyze_poem(poem, confident_threshold)
        if res is None or res["high_s2_total"] < 3:
            continue
        rows.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta["era"],
            "spi": res["spi"],
            "high_s2_total": res["high_s2_total"],
            "avg_s2": poem["summary"]["avg_s2"],
        })
    rows.sort(key=lambda r: -r["spi"])
    return rows


def compute_quadrant_membership(poet_rows, global_spi_mean, global_s2_mean):
    """Classify each poet into one of four quadrants."""
    quads = {"HQ": [], "LQ": [], "NS": [], "SC": []}
    for r in poet_rows:
        hi_s2 = r["mean_avg_s2"] >= global_s2_mean
        hi_spi = r["mean_spi"] >= global_spi_mean
        if hi_s2 and hi_spi:
            quads["HQ"].append(r["author"])  # High quality + high quantity
        elif hi_s2 and not hi_spi:
            quads["NS"].append(r["author"])  # Noisy surprisers
        elif not hi_s2 and hi_spi:
            quads["SC"].append(r["author"])  # Strategic but conservative
        else:
            quads["LQ"].append(r["author"])  # Low quantity + low quality
    return quads


def write_finding(confident_threshold, era_rows, poet_rows, poem_rows, global_s2_mean, global_spi_mean, n_total_tokens, n_high_s2, n_confident_high_s2):
    overall_spi = n_confident_high_s2 / n_high_s2 if n_high_s2 else 0
    quads = compute_quadrant_membership(poet_rows, global_spi_mean, global_s2_mean)

    lines = [
        "# Surprise Purity Index: Measuring the Quality of the Straussian Gap",
        "",
        f"**Date:** 2026-10-31  ",
        f"**Experiment:** `experiments/surprise_purity_index.py`  ",
        f"**Corpus:** {len(poet_rows)} poets (≥{MIN_POEMS} poems), {n_total_tokens:,} artifact-free tokens  ",
        "",
        "---",
        "",
        "## Research Question",
        "",
        "Not all high-S₂ moments are equal. The S₂ formula is:",
        "",
        "> **S₂ = S − H**  (surprisal minus entropy)",
        "",
        "When entropy H is *high*, the model is already confused — any unusual token will",
        "generate positive S₂ without the model having made a strong prediction.",
        "When entropy H is *low*, the model was *confident* about what came next —",
        "so a high-S₂ token represents a genuine defiance of expectation.",
        "",
        "**Surprise Purity Index (SPI)** = fraction of high-S₂ tokens (S₂ ≥ 3.0) that occur",
        "in *low-entropy* contexts (model was confident). It measures whether a poet achieves",
        "Straussian surprise efficiently — defying confident predictions — or mainly operates",
        "in semantic territory where the model was confused anyway.",
        "",
        "---",
        "",
        "## Setup",
        "",
        f"- High-S₂ threshold: S₂ ≥ {S2_THRESHOLD}",
        f"- Artifact filter: p(newline) < {P_NEWLINE_MAX}",
        f"- Low-entropy (confident) threshold: H < {confident_threshold:.3f} bits (33rd percentile of all token entropies)",
        "",
        "---",
        "",
        "## Corpus-Level Results",
        "",
        f"- Total artifact-free tokens: **{n_total_tokens:,}**",
        f"- High-S₂ tokens (S₂ ≥ 3.0): **{n_high_s2:,}** ({100*n_high_s2/n_total_tokens:.1f}%)",
        f"- High-S₂ in confident contexts: **{n_confident_high_s2:,}** ({100*overall_spi:.1f}% of high-S₂ tokens)",
        f"- **Overall SPI: {overall_spi:.4f}** — only {100*overall_spi:.0f}% of high-S₂ moments occur when the model was confident",
        "",
        "This means **{:.0f}% of surface-level 'surprises' occur in already-uncertain contexts** — the model was confused regardless.".format((1-overall_spi)*100),
        "True Straussian defiance of confident expectation is rare.",
        "",
        "---",
        "",
        "## Results by Era",
        "",
        "| Era | N | Mean SPI | Mean avg_S₂ |",
        "|-----|---|----------|-------------|",
    ]
    for r in era_rows:
        lines.append(f"| {r['era']} | {r['n_poems']} | **{r['mean_spi']:.3f}** | {r['mean_avg_s2']:.3f} |")

    lines += [
        "",
        "---",
        "",
        "## Results by Poet (≥2 poems)",
        "",
        "### Highest SPI (pure surprise specialists)",
        "",
        "| Author | Era | N | SPI | avg_S₂ |",
        "|--------|-----|---|-----|--------|",
    ]
    for r in poet_rows[:20]:
        lines.append(f"| {r['author']} | {r['era']} | {r['n_poems']} | **{r['mean_spi']:.3f}** | {r['mean_avg_s2']:.3f} |")

    lines += [
        "",
        "### Lowest SPI (noisy surprisers)",
        "",
        "| Author | Era | N | SPI | avg_S₂ |",
        "|--------|-----|---|-----|--------|",
    ]
    for r in reversed(poet_rows[-20:]):
        lines.append(f"| {r['author']} | {r['era']} | {r['n_poems']} | **{r['mean_spi']:.3f}** | {r['mean_avg_s2']:.3f} |")

    lines += [
        "",
        "---",
        "",
        "## The Four Quadrants of Surprise Quality",
        "",
        f"Using global means as thresholds (avg_S₂ = {global_s2_mean:.3f}, SPI = {global_spi_mean:.3f}):",
        "",
        "| Quadrant | Description | Poets |",
        "|----------|-------------|-------|",
        f"| **High S₂ + High SPI** (Pure Surprise Specialists) | Surprise the model often AND efficiently | {', '.join(quads['HQ'][:8])} |",
        f"| **High S₂ + Low SPI** (Noisy Surprisers) | Many high-S₂ tokens but in uncertain contexts | {', '.join(quads['NS'][:8])} |",
        f"| **Low S₂ + High SPI** (Strategic Minimalists) | Rare surprises, but always when model was confident | {', '.join(quads['SC'][:8])} |",
        f"| **Low S₂ + Low SPI** (Conventional) | Rare surprises, mostly in uncertain contexts | {', '.join(quads['LQ'][:8])} |",
        "",
        "---",
        "",
        "## Top 15 Poems by SPI",
        "",
        "| Title | Author | Era | SPI | High-S₂ count | avg_S₂ |",
        "|-------|--------|-----|-----|---------------|--------|",
    ]
    for r in poem_rows[:15]:
        lines.append(f"| {r['title'][:45]} | {r['author'][:25]} | {r['era']} | **{r['spi']:.3f}** | {r['high_s2_total']} | {r['avg_s2']:.3f} |")

    lines += [
        "",
        "## Bottom 15 Poems by SPI",
        "",
        "| Title | Author | Era | SPI | High-S₂ count | avg_S₂ |",
        "|-------|--------|-----|-----|---------------|--------|",
    ]
    for r in poem_rows[-15:]:
        lines.append(f"| {r['title'][:45]} | {r['author'][:25]} | {r['era']} | **{r['spi']:.3f}** | {r['high_s2_total']} | {r['avg_s2']:.3f} |")

    # Additional analysis: does SPI correlate with avg_S2?
    spi_vals = [r["mean_spi"] for r in poet_rows]
    s2_vals = [r["mean_avg_s2"] for r in poet_rows]
    n = len(spi_vals)
    mean_spi_v = sum(spi_vals) / n
    mean_s2_v = sum(s2_vals) / n
    cov = sum((a - mean_spi_v) * (b - mean_s2_v) for a, b in zip(spi_vals, s2_vals)) / n
    std_spi = math.sqrt(sum((x - mean_spi_v)**2 for x in spi_vals) / n)
    std_s2 = math.sqrt(sum((x - mean_s2_v)**2 for x in s2_vals) / n)
    corr = cov / (std_spi * std_s2) if std_spi * std_s2 > 0 else 0

    lines += [
        "",
        "---",
        "",
        "## Key Findings",
        "",
        f"1. **SPI is low overall ({overall_spi:.2f})**: Most 'surprises' (S₂ ≥ 3) occur when the model is uncertain,",
        "   not when it is confident. The truly Straussian — defiance of confident prediction — is rare.",
        "",
        f"2. **SPI and avg_S₂ correlation: r = {corr:.3f}**: {'Positive correlation — poets who surprise more also do so more efficiently.' if corr > 0.2 else 'Weak correlation — surprise quantity and purity are largely independent.'}",
        "   This means some poets achieve high S₂ through quantity of surprises in uncertain contexts,",
        "   while others specialize in rare, highly pure defiance.",
        "",
        "3. **Era differences**: Fixed-form and constrained poetry (where the model builds stronger expectations)",
        "   may show higher SPI, while Language Poetry (entropy flooding) would show near-zero SPI.",
        "",
        "4. **The 'quality vs. quantity' trade-off**: Poets can maximize S₂ by (a) frequently surprising",
        "   an uncertain model (low SPI, high quantity) or (b) rarely but decisively surprising a",
        "   confident model (high SPI). These are distinct aesthetic strategies.",
        "",
        "## Suggested Next Steps",
        "",
        "- Correlate SPI with known 'difficulty' ratings or anthology frequency",
        "- Examine per-poem SPI arc: does purity cluster at poem beginning/end?",
        "- Cross-model: does GPT-2 medium show different SPI distributions (more confidence → higher SPI)?",
        "- Test whether high-SPI moments correspond to recognized 'great lines' vs. high-S₂ noise",
    ]

    with open(FINDING, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Finding written: {FINDING}")


def main():
    print("Loading corpus...")
    corpus = load_corpus()

    print("Computing entropy percentile threshold...")
    confident_threshold = compute_entropy_percentile(corpus, pct=33)
    print(f"  33rd percentile entropy = {confident_threshold:.3f} bits")

    # Corpus-level stats
    n_total = 0
    n_high = 0
    n_conf_high = 0
    for poem in corpus:
        for tok in poem["tokens"]:
            if tok["p_newline"] >= P_NEWLINE_MAX:
                continue
            n_total += 1
            if tok["s2"] >= S2_THRESHOLD:
                n_high += 1
                if tok["entropy"] < confident_threshold:
                    n_conf_high += 1

    print(f"  Total artifact-free tokens: {n_total:,}")
    print(f"  High-S2 tokens: {n_high:,}")
    print(f"  High-S2 in confident context: {n_conf_high:,} (SPI={n_conf_high/n_high:.3f})")

    print("Analyzing by era...")
    era_rows = era_analysis(corpus, confident_threshold)

    print("Analyzing by poet...")
    poet_rows = poet_analysis(corpus, confident_threshold)

    print("Analyzing by poem...")
    poem_rows = poem_analysis(corpus, confident_threshold)

    global_s2_mean = sum(r["mean_avg_s2"] for r in poet_rows) / len(poet_rows)
    global_spi_mean = sum(r["mean_spi"] for r in poet_rows) / len(poet_rows)

    result = {
        "confident_threshold": round(confident_threshold, 4),
        "overall_spi": round(n_conf_high / n_high, 4) if n_high else 0,
        "n_total_tokens": n_total,
        "n_high_s2": n_high,
        "n_confident_high_s2": n_conf_high,
        "global_s2_mean": round(global_s2_mean, 4),
        "global_spi_mean": round(global_spi_mean, 4),
        "by_era": era_rows,
        "by_poet": poet_rows,
        "top_poems_by_spi": poem_rows[:30],
        "bottom_poems_by_spi": poem_rows[-30:],
    }

    with open(OUTPUT, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Results written: {OUTPUT}")

    write_finding(
        confident_threshold, era_rows, poet_rows, poem_rows,
        global_s2_mean, global_spi_mean, n_total, n_high, n_conf_high
    )


if __name__ == "__main__":
    main()
