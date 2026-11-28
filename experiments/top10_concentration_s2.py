"""
Top-10 Probability Concentration and Poetic Surprise

Research Question: Does the concentration of GPT-2's probability mass in its
top-10 predictions predict HOW poets violate expectations?

Standard entropy (H) measures uncertainty over ALL ~50,000 vocabulary tokens.
But we can also ask: what fraction of probability mass sits in the top 10 options?

  top10_coverage = sum(p_i for i in top 10 alternatives)

A high coverage position (e.g., 0.90) means 10 alternatives dominate.
A low coverage position (e.g., 0.20) means probability is spread across many words.

This distinction matters:
  - High-coverage surprise: poet violated a prediction where the model's
    probability mass was tightly focused → "precision shot" deviation
  - Low-coverage surprise: poet violated a prediction in a scattered field →
    deviation carries a different information signature

We also compute top10_entropy = H(top-10 sub-distribution) normalized,
to distinguish "focused on 1 of top-10" vs "even among top-10."

Hypotheses:
  1. High-coverage positions produce HIGHER S2 surprises (the model was
     "sure," so any deviation is amplified)
  2. Poetic genres differ in whether their surprises are precision shots
     vs scatter violations
  3. Some poets specialize in one mode; others mix both
"""

import json
import math
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"
OUT_PATH = Path(__file__).parent.parent / "results" / "top10_concentration_s2.json"


def top10_stats(alternatives):
    """Compute coverage and entropy of the top-10 alternatives distribution."""
    if not alternatives:
        return None, None
    probs = [a["prob"] for a in alternatives]
    coverage = sum(probs)
    # Entropy of the top-10 sub-distribution (normalized to sum to 1)
    if coverage <= 0:
        return 0.0, 0.0
    normed = [p / coverage for p in probs]
    top10_h = -sum(p * math.log2(p + 1e-12) for p in normed)
    return coverage, top10_h


def coverage_tier(cov):
    if cov is None:
        return "unknown"
    if cov >= 0.75:
        return "high"      # top-10 dominate
    elif cov >= 0.45:
        return "medium"
    else:
        return "low"       # very diffuse prediction


def analyze():
    with open(DATA_PATH) as f:
        corpus = json.load(f)

    # Aggregate stats
    tier_s2 = defaultdict(list)
    tier_top10h = defaultdict(list)
    era_data = defaultdict(lambda: {"high": [], "medium": [], "low": []})
    author_data = defaultdict(lambda: {"coverages": [], "s2s": []})

    # For cross-tabulation: (coverage_tier, s2_tier) counts and avg S2
    crosstab = defaultdict(list)

    # Precision-shot tokens: very high coverage + very high S2
    precision_shots = []  # (title, author, era, token, s2, coverage, expected)

    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        author = meta.get("author", "Unknown")
        title = meta.get("title", "")

        for tok in poem["tokens"]:
            # Skip stanza-break artifact
            if tok.get("p_newline", 0) >= 0.9:
                continue

            s2 = tok["s2"]
            alts = tok.get("alternatives", [])
            cov, h10 = top10_stats(alts)
            if cov is None:
                continue

            tier = coverage_tier(cov)
            tier_s2[tier].append(s2)
            tier_top10h[tier].append(h10)
            era_data[era][tier].append(s2)
            author_data[author]["coverages"].append(cov)
            author_data[author]["s2s"].append(s2)

            # S2 bin
            if s2 >= 5:
                s2_tier = "very_high"
            elif s2 >= 2:
                s2_tier = "high"
            elif s2 >= -1:
                s2_tier = "neutral"
            else:
                s2_tier = "low"
            crosstab[(tier, s2_tier)].append(s2)

            # Collect precision shots: high coverage + high S2
            if cov >= 0.75 and s2 >= 8.0:
                top_expected = alts[0]["token"] if alts else "?"
                precision_shots.append({
                    "title": title,
                    "author": author,
                    "era": era,
                    "token": tok["token"],
                    "s2": round(s2, 2),
                    "coverage": round(cov, 3),
                    "top_expected": top_expected,
                    "top_expected_prob": round(alts[0]["prob"] if alts else 0, 3),
                })

    # Sort precision shots by S2 descending
    precision_shots.sort(key=lambda x: -x["s2"])

    # Summarize per tier
    tier_summary = {}
    for tier in ["high", "medium", "low"]:
        vals = tier_s2[tier]
        h10_vals = tier_top10h[tier]
        if not vals:
            continue
        pos_ratio = sum(1 for v in vals if v > 0) / len(vals)
        tier_summary[tier] = {
            "n": len(vals),
            "avg_s2": round(statistics.mean(vals), 4),
            "median_s2": round(statistics.median(vals), 4),
            "std_s2": round(statistics.stdev(vals) if len(vals) > 1 else 0, 4),
            "pos_s2_ratio": round(pos_ratio, 4),
            "avg_top10h": round(statistics.mean(h10_vals), 4),
        }

    # Era-level coverage profiles (% of tokens in each tier + avg S2 per tier)
    era_summary = {}
    for era, tiers in era_data.items():
        total = sum(len(v) for v in tiers.values())
        if total < 30:
            continue
        era_summary[era] = {}
        for tier in ["high", "medium", "low"]:
            vals = tiers[tier]
            era_summary[era][f"{tier}_pct"] = round(len(vals) / total * 100, 1)
            era_summary[era][f"{tier}_avg_s2"] = (
                round(statistics.mean(vals), 3) if vals else None
            )
        # Overall avg S2 (artifact-free)
        all_s2 = [v for t in tiers.values() for v in t]
        era_summary[era]["avg_s2"] = round(statistics.mean(all_s2), 3) if all_s2 else None
        era_summary[era]["n"] = total

    # Author-level: "precision-shot rate" = % tokens with high coverage (≥0.75)
    # and "scatter deviation rate" = % tokens with low coverage AND high S2
    author_summary = {}
    for author, d in author_data.items():
        covs = d["coverages"]
        s2s = d["s2s"]
        if len(covs) < 50:
            continue
        pairs = list(zip(covs, s2s))
        precision_shot_n = sum(1 for c, s in pairs if c >= 0.75 and s >= 5)
        scatter_dev_n = sum(1 for c, s in pairs if c < 0.45 and s >= 5)
        total = len(pairs)
        author_summary[author] = {
            "n": total,
            "avg_coverage": round(statistics.mean(covs), 4),
            "avg_s2": round(statistics.mean(s2s), 4),
            "precision_shot_rate": round(precision_shot_n / total * 100, 2),
            "scatter_dev_rate": round(scatter_dev_n / total * 100, 2),
            "ps_to_sd_ratio": round(
                precision_shot_n / (scatter_dev_n + 1), 2
            ),  # +1 to avoid div/0
        }

    # Cross-tabulation summary
    crosstab_summary = {}
    for (cov_tier, s2_tier), vals in crosstab.items():
        key = f"{cov_tier}_cov__{s2_tier}_s2"
        crosstab_summary[key] = {
            "n": len(vals),
            "avg_s2": round(statistics.mean(vals), 3),
        }

    result = {
        "meta": {
            "corpus_size": len(corpus),
            "analysis": "top10_concentration_s2",
        },
        "tier_summary": tier_summary,
        "crosstab": crosstab_summary,
        "era_summary": era_summary,
        "author_summary": author_summary,
        "precision_shots_top30": precision_shots[:30],
    }

    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Saved → {OUT_PATH}")
    return result


if __name__ == "__main__":
    r = analyze()
    ts = r["tier_summary"]
    print("\n=== Top-10 Coverage Tier vs S2 ===")
    for tier, stats in ts.items():
        print(
            f"  {tier:7s} (n={stats['n']:6d}): "
            f"avg_S2={stats['avg_s2']:+.3f}  "
            f"pos%={stats['pos_s2_ratio']*100:.1f}%  "
            f"top10H={stats['avg_top10h']:.3f}"
        )
    print("\n=== Top-5 Precision-Shot Tokens ===")
    for ps in r["precision_shots_top30"][:5]:
        print(
            f"  '{ps['token']}' (S2={ps['s2']:.1f}, cov={ps['coverage']:.2f}) "
            f"← expected '{ps['top_expected']}' (p={ps['top_expected_prob']:.2f}) "
            f"| {ps['author']}, {ps['title'][:40]}"
        )
