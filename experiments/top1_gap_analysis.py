"""
Top-1 Gap Analysis: The Distance Between the Best Guess and the Actual Choice
=============================================================================
Date: 2026-11-17

Motivation: S2 = surprisal - entropy measures how surprising a token is
relative to the AVERAGE model uncertainty. But there is another natural
baseline: the model's TOP prediction (rank-1 token). The "Top-1 Gap" (T1G)
measures how many extra bits the actual choice cost compared to the model's
single best guess.

T1G = surprisal(actual) - surprisal(top1)
    = -log2(prob_actual) - (-log2(prob_top1))
    = log2(prob_top1 / prob_actual)

This is DIFFERENT from S2:
  S2  = surprisal(actual) - entropy        [actual vs. average uncertainty]
  T1G = surprisal(actual) - surprisal(top1) [actual vs. best guess]

Relationship: T1G - S2 = entropy - surprisal(top1)
  = entropy + log2(prob_top1)
  = "how much MORE certain was the top-1 prediction than the average?"

This residual captures whether the model had one dominant guess (low entropy,
high top-1 probability → T1G >> S2) or was diffuse (high entropy, moderate
top-1 probability → T1G ≈ S2).

Research Questions:
1. What is the typical T1G in poetry vs. prose?
2. Do high-S2 and high-T1G co-occur, or are they dissociated?
3. Which eras maximize T1G? (Suggests poets choosing against dominant predictions)
4. What is the residual (T1G - S2) distribution? Does it reveal anything about
   how "clear" the model's prediction was at deviation points?
"""

import json
import math
import numpy as np
from pathlib import Path
from collections import defaultdict

RESULTS_FILE = Path(__file__).parent.parent / "results" / "corpus_results.json"
FINDINGS_DIR = Path(__file__).parent.parent / "findings"
OUTPUT_FILE = Path(__file__).parent.parent / "results" / "top1_gap_analysis.json"


def compute_top1_gap(token_data):
    """Compute Top-1 Gap for a single token."""
    prob_actual = token_data.get("prob", 0)
    alternatives = token_data.get("alternatives", [])
    p_newline = token_data.get("p_newline", 0)

    # Skip stanza-break artifact tokens
    if p_newline >= 0.9:
        return None
    # Skip newline tokens and near-zero prob
    if prob_actual <= 0 or not alternatives:
        return None

    prob_top1 = alternatives[0]["prob"]
    if prob_top1 <= 0:
        return None

    surprisal_actual = -math.log2(prob_actual)
    surprisal_top1 = -math.log2(prob_top1)
    top1_gap = surprisal_actual - surprisal_top1

    # Must be non-negative (actual is never more probable than top-1)
    if top1_gap < 0:
        top1_gap = 0.0

    return top1_gap


def analyze_corpus():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    all_tokens = []  # list of {t1g, s2, entropy, era, language, token, is_poetry}
    era_data = defaultdict(list)
    poet_data = defaultdict(list)

    # For the 2D scatter: high-gap/low-S2 and low-gap/high-S2 cases
    gap_gt_s2_tokens = []   # T1G >> S2: model had a clear favorite but was wrong
    s2_gt_gap_tokens = []   # S2 >> T1G: actual near top-1 but far from entropy

    for poem in corpus:
        meta = poem["metadata"]
        lang = meta.get("language", "en")
        era = meta.get("era", "unknown")
        author = meta.get("author", "Unknown")
        title = meta.get("title", "")
        is_poetry = era != "control"

        if lang != "en":
            continue

        poem_gaps = []
        for tok in poem.get("tokens", []):
            t1g = compute_top1_gap(tok)
            if t1g is None:
                continue
            s2 = tok.get("s2", 0)
            entropy = tok.get("entropy", 0)
            token_text = tok.get("token", "").strip()

            rec = {
                "t1g": t1g,
                "s2": s2,
                "entropy": entropy,
                "residual": t1g - s2,  # = entropy + log2(prob_top1) = "top-1 confidence advantage"
                "era": era,
                "is_poetry": is_poetry,
                "token": token_text,
                "author": author,
                "title": title,
            }
            all_tokens.append(rec)
            era_data[era].append(rec)
            poet_data[author].append(rec)
            poem_gaps.append(rec)

            # Classify into 2D categories
            if t1g > 3 and s2 < 1:
                gap_gt_s2_tokens.append(rec)
            elif s2 > 3 and t1g < 1:
                s2_gt_gap_tokens.append(rec)

    return {
        "all_tokens": all_tokens,
        "era_data": era_data,
        "poet_data": poet_data,
        "gap_gt_s2": gap_gt_s2_tokens,
        "s2_gt_gap": s2_gt_gap_tokens,
    }


def summarize(tokens):
    if not tokens:
        return {}
    t1g_vals = [t["t1g"] for t in tokens]
    s2_vals = [t["s2"] for t in tokens]
    res_vals = [t["residual"] for t in tokens]
    return {
        "n": len(tokens),
        "mean_t1g": np.mean(t1g_vals),
        "median_t1g": np.median(t1g_vals),
        "std_t1g": np.std(t1g_vals),
        "mean_s2": np.mean(s2_vals),
        "mean_residual": np.mean(res_vals),
        "high_t1g_ratio": sum(1 for x in t1g_vals if x > 5) / len(t1g_vals),
        "zero_gap_ratio": sum(1 for x in t1g_vals if x < 0.1) / len(t1g_vals),
    }


def top_tokens(tokens, field="t1g", n=10):
    sorted_toks = sorted(tokens, key=lambda x: x[field], reverse=True)
    return [
        {
            "token": t["token"],
            "t1g": round(t["t1g"], 3),
            "s2": round(t["s2"], 3),
            "residual": round(t["residual"], 3),
            "era": t["era"],
            "author": t["author"],
            "title": t["title"],
        }
        for t in sorted_toks[:n]
    ]


def main():
    data = analyze_corpus()
    all_tokens = data["all_tokens"]
    era_data = data["era_data"]
    poet_data = data["poet_data"]

    poetry_tokens = [t for t in all_tokens if t["is_poetry"]]
    prose_tokens = [t for t in all_tokens if not t["is_poetry"]]

    # Global summary
    global_summary = {
        "poetry": summarize(poetry_tokens),
        "prose": summarize(prose_tokens),
        "all": summarize(all_tokens),
    }

    # Era-level summaries (min 20 tokens)
    era_summaries = {}
    for era, tokens in era_data.items():
        if len(tokens) >= 20:
            era_summaries[era] = summarize(tokens)

    # Sort eras by mean T1G
    era_summaries_sorted = sorted(
        era_summaries.items(), key=lambda x: x[1]["mean_t1g"], reverse=True
    )

    # Poet-level summaries (min 50 tokens)
    poet_summaries = {}
    for poet, tokens in poet_data.items():
        if len(tokens) >= 50:
            poet_summaries[poet] = summarize(tokens)

    poet_summaries_sorted = sorted(
        poet_summaries.items(), key=lambda x: x[1]["mean_t1g"], reverse=True
    )

    # Correlation between T1G and S2
    t1g_arr = np.array([t["t1g"] for t in all_tokens])
    s2_arr = np.array([t["s2"] for t in all_tokens])
    corr = np.corrcoef(t1g_arr, s2_arr)[0, 1]

    # T1G distribution buckets
    buckets = [
        ("Zero gap (chose top-1)", 0, 0.1),
        ("Tiny gap (< 1 bit)", 0.1, 1.0),
        ("Small gap (1-3 bits)", 1.0, 3.0),
        ("Medium gap (3-6 bits)", 3.0, 6.0),
        ("Large gap (> 6 bits)", 6.0, float("inf")),
    ]
    bucket_stats = {}
    for label, lo, hi in buckets:
        toks = [t for t in all_tokens if lo <= t["t1g"] < hi]
        bucket_stats[label] = {
            "n": len(toks),
            "pct": len(toks) / len(all_tokens) * 100,
            "mean_s2": np.mean([t["s2"] for t in toks]) if toks else None,
            "mean_residual": np.mean([t["residual"] for t in toks]) if toks else None,
            "pct_poetry": sum(1 for t in toks if t["is_poetry"]) / len(toks) * 100 if toks else None,
        }

    # 2D quadrant analysis
    # Q1: High T1G + High S2 (chose against confident dominant prediction)
    # Q2: Low T1G + High S2 (actual near top-1 but entropy was high → unusual)
    # Q3: Low T1G + Low S2 (conformist: chose near top-1, entropy was average)
    # Q4: High T1G + Low S2 (chose far below top-1, but model was diffuse)
    t1g_thresh = 3.0
    s2_thresh = 1.0
    quad_counts = {
        "Q1_high_t1g_high_s2": sum(1 for t in all_tokens if t["t1g"] >= t1g_thresh and t["s2"] >= s2_thresh),
        "Q2_low_t1g_high_s2": sum(1 for t in all_tokens if t["t1g"] < t1g_thresh and t["s2"] >= s2_thresh),
        "Q3_low_t1g_low_s2": sum(1 for t in all_tokens if t["t1g"] < t1g_thresh and t["s2"] < s2_thresh),
        "Q4_high_t1g_low_s2": sum(1 for t in all_tokens if t["t1g"] >= t1g_thresh and t["s2"] < s2_thresh),
    }

    # Era Q1 rates
    era_q1_rates = {}
    for era, tokens in era_data.items():
        if len(tokens) >= 50:
            q1 = sum(1 for t in tokens if t["t1g"] >= t1g_thresh and t["s2"] >= s2_thresh)
            era_q1_rates[era] = round(q1 / len(tokens) * 100, 1)
    era_q1_sorted = sorted(era_q1_rates.items(), key=lambda x: x[1], reverse=True)

    # Examples: extreme high-T1G tokens
    top_t1g = top_tokens(all_tokens, field="t1g", n=20)
    # Q2 examples (low T1G, high S2: unusual pattern)
    q2_tokens = [t for t in all_tokens if t["t1g"] < 0.5 and t["s2"] > 2.0]
    # These are cases where: actual ≈ top-1 prediction BUT still high S2
    # This would mean entropy is VERY low AND actual ≈ top prediction
    # → meaning high S2 came from low entropy making everything surprising? No.
    # Wait: S2 = surprisal - entropy. If S2 is high and T1G is low, that means:
    # surprisal - entropy is high, but surprisal - surprisal(top1) is low.
    # So entropy ≈ surprisal(top1), meaning the top-1 itself has high surprisal (relative to entropy)
    # → entropy is LOW (confident model), top-1 also has moderately low probability,
    #   actual has approximately same probability as top-1. But S2 high → surprisal > entropy.
    # So: model had low entropy, top-1 had prob ≈ actual prob, but actual was still above entropy.
    # This is strange and might indicate floating point artifacts or tied predictions.

    result = {
        "global_summary": global_summary,
        "poetry_prose_gap": {
            "mean_t1g_diff": global_summary["poetry"]["mean_t1g"] - global_summary["prose"]["mean_t1g"],
            "t1g_s2_correlation": round(float(corr), 4),
        },
        "bucket_stats": bucket_stats,
        "quadrant_analysis": {
            "counts": quad_counts,
            "pcts": {k: round(v / len(all_tokens) * 100, 1) for k, v in quad_counts.items()},
            "t1g_threshold_bits": t1g_thresh,
            "s2_threshold_bits": s2_thresh,
        },
        "era_summaries_top20": {
            era: stats for era, stats in era_summaries_sorted[:20]
        },
        "era_q1_rates_top20": dict(era_q1_sorted[:20]),
        "poet_summaries_top15": {
            poet: stats for poet, stats in poet_summaries_sorted[:15]
        },
        "top_t1g_tokens": top_t1g,
        "q2_examples_count": len(q2_tokens),
    }

    # Round floats for readability
    def round_floats(obj):
        if isinstance(obj, dict):
            return {k: round_floats(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [round_floats(v) for v in obj]
        elif isinstance(obj, float):
            return round(obj, 4)
        return obj

    result = round_floats(result)
    OUTPUT_FILE.write_text(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    r = main()

    print("\n=== TOP-1 GAP ANALYSIS ===")
    print(f"\nGlobal Mean T1G  — Poetry: {r['global_summary']['poetry']['mean_t1g']:.3f} bits")
    print(f"                   Prose:  {r['global_summary']['prose']['mean_t1g']:.3f} bits")
    print(f"Gap (poetry-prose):        {r['poetry_prose_gap']['mean_t1g_diff']:.3f} bits")
    print(f"\nT1G vs S2 correlation: r = {r['poetry_prose_gap']['t1g_s2_correlation']:.4f}")

    print("\n=== T1G Distribution Buckets ===")
    for bucket, stats in r["bucket_stats"].items():
        print(f"  {bucket}: {stats['n']} ({stats['pct']:.1f}%) | mean S2={stats['mean_s2']:.3f}")

    print("\n=== Quadrant Counts ===")
    for q, pct in r["quadrant_analysis"]["pcts"].items():
        print(f"  {q}: {pct:.1f}%")

    print("\n=== Top 10 Eras by Mean T1G ===")
    for era, stats in list(r["era_summaries_top20"].items())[:10]:
        print(f"  {era:<25} T1G={stats['mean_t1g']:.3f}  S2={stats['mean_s2']:.3f}  residual={stats['mean_residual']:.3f}")

    print("\n=== Top Era Q1 Rates (High T1G + High S2) ===")
    for era, rate in list(r["era_q1_rates_top20"].items())[:10]:
        print(f"  {era:<25} {rate:.1f}%")

    print("\n=== Highest T1G Tokens (top 10) ===")
    for t in r["top_t1g_tokens"][:10]:
        print(f"  '{t['token']}' T1G={t['t1g']:.2f} S2={t['s2']:.2f} res={t['residual']:.2f} [{t['era']}] {t['author']}")

    print(f"\nResults saved to: {OUTPUT_FILE}")
