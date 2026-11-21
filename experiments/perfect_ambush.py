"""
Perfect Ambush Analysis: High-α + High-S₂ Moments
===================================================
Follow-up to zipf_prediction_coefficient.md (2026-11-19).

The Zipf finding established two paths to poetic surprise:
  - High-α ambush: defeat a concentrated prediction
  - Low-α field-escape: leave even a diffuse probability field

This experiment identifies "perfect ambush" moments where BOTH conditions
for maximum Straussian impact align:
  1. The model is maximally concentrated (high α, hyper-Zipf context)
  2. The poet writes something far from the top prediction (high S₂)

These are the moments when the poet could have written the most predictable
word in the language — and chose something else instead.

We also characterize:
  - What the model expected (the top-1 prediction and its probability)
  - What the poet wrote (rank, semantic field)
  - The surrounding context
  - Per-era and per-author distribution of perfect ambush density
  - Within-poem α trajectories: does α shift across a poem's arc?
"""

import json
import math
import statistics
from collections import defaultdict


def zipf_alpha(alternatives: list) -> float | None:
    """
    Fit Zipf exponent α to the top-N alternative probabilities.

    Model: P(rank r) ≈ r^(-α)
    Log-linearised: log P = -α * log r + C
    Fit by OLS on log-log scale using ranks 1..N.
    Returns None if fewer than 3 alternatives.
    """
    probs = sorted([a["prob"] for a in alternatives], reverse=True)
    probs = [p for p in probs if p > 0]
    if len(probs) < 3:
        return None

    # Build log-log pairs
    log_ranks = [math.log(r) for r in range(1, len(probs) + 1)]
    log_probs = [math.log(p) for p in probs]

    n = len(log_ranks)
    sx = sum(log_ranks)
    sy = sum(log_probs)
    sxy = sum(x * y for x, y in zip(log_ranks, log_probs))
    sxx = sum(x * x for x in log_ranks)

    denom = n * sxx - sx * sx
    if denom == 0:
        return None
    slope = (n * sxy - sx * sy) / denom
    return -slope  # α = -slope


def classify_alpha(alpha: float) -> str:
    if alpha >= 2.5:
        return "hyper_zipf"
    if alpha >= 1.5:
        return "super_zipf"
    if alpha >= 0.8:
        return "near_zipf"
    if alpha >= 0.3:
        return "sub_zipf"
    return "anti_zipf"


def run():
    with open("results/corpus_results.json") as f:
        data = json.load(f)

    # -----------------------------------------------------------------
    # Pass 1: Per-token Zipf α and classification
    # -----------------------------------------------------------------
    perfect_ambush = []          # α ≥ 2.5, S₂ ≥ 5.0
    perfect_fulfillment = []     # α ≥ 2.5, S₂ ≤ -3.0  (prediction confirmed)
    per_era_ambush = defaultdict(list)
    per_author_ambush = defaultdict(list)

    # For within-poem α trajectory analysis
    poem_arcs = []

    for entry in data:
        era = entry["metadata"].get("era", "unknown")
        author = entry["metadata"].get("author", "Unknown")
        title = entry["metadata"].get("title", "Untitled")
        is_control = era == "control"

        toks = entry["tokens"]
        n = len(toks)

        poem_alphas = []
        for i, tok in enumerate(toks):
            alts = tok.get("alternatives", [])
            # Include the actual token as rank-0 info only if it appears in alts,
            # otherwise use alts as given (they are GPT-2's top predictions,
            # NOT including the actual token if it was not in top-10).
            alpha = zipf_alpha(alts)
            if alpha is None:
                poem_alphas.append(None)
                continue
            poem_alphas.append(alpha)

            s2 = tok["s2"]
            p_newline = tok.get("p_newline", 0.0)
            if p_newline >= 0.9:
                continue   # skip stanza-break artifact positions

            cat = classify_alpha(alpha)
            top1 = sorted(alts, key=lambda a: -a["prob"])[0] if alts else None

            record = {
                "author": author,
                "title": title,
                "era": era,
                "token": tok["token"],
                "s2": s2,
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "alpha": alpha,
                "alpha_class": cat,
                "rank": tok.get("rank", None),
                "top1_token": top1["token"] if top1 else None,
                "top1_prob": top1["prob"] if top1 else None,
                "position_in_poem": i / max(n - 1, 1),
                "position_index": i,
            }

            if alpha >= 2.5 and s2 >= 5.0 and not is_control:
                perfect_ambush.append(record)
                per_era_ambush[era].append(s2)
                per_author_ambush[author].append(s2)

            if alpha >= 2.5 and s2 <= -3.0 and not is_control:
                perfect_fulfillment.append(record)

        # Store poem arc (non-None alphas with their positional fraction)
        arc = [(i / max(n - 1, 1), a) for i, a in enumerate(poem_alphas) if a is not None]
        if len(arc) >= 10:
            poem_arcs.append({
                "author": author,
                "title": title,
                "era": era,
                "n_tokens": n,
                "arc": arc,
            })

    # -----------------------------------------------------------------
    # Pass 2: Within-poem α trajectory — does α change across poem arc?
    # -----------------------------------------------------------------
    # Divide poem into 5 quintiles; average α per quintile across all poems
    quintile_alphas = [[] for _ in range(5)]
    for poem in poem_arcs:
        for frac, alpha in poem["arc"]:
            q = min(int(frac * 5), 4)
            quintile_alphas[q].append(alpha)

    quintile_means = [
        statistics.mean(qs) if qs else float("nan")
        for qs in quintile_alphas
    ]

    # -----------------------------------------------------------------
    # Pass 3: Era-level perfect-ambush density
    # (perfect ambush count / total artifact-free tokens)
    # -----------------------------------------------------------------
    era_total_clean = defaultdict(int)
    for entry in data:
        era = entry["metadata"].get("era", "unknown")
        if era == "control":
            continue
        for tok in entry["tokens"]:
            if tok.get("p_newline", 0.0) < 0.9:
                era_total_clean[era] += 1

    era_ambush_density = {}
    for era, s2vals in per_era_ambush.items():
        total = era_total_clean.get(era, 1)
        era_ambush_density[era] = {
            "count": len(s2vals),
            "density": len(s2vals) / total,
            "mean_s2": statistics.mean(s2vals) if s2vals else 0,
            "max_s2": max(s2vals) if s2vals else 0,
        }

    # Author-level
    author_ambush_density = {}
    author_total = defaultdict(int)
    for entry in data:
        author = entry["metadata"].get("author", "Unknown")
        if entry["metadata"].get("era") == "control":
            continue
        for tok in entry["tokens"]:
            if tok.get("p_newline", 0.0) < 0.9:
                author_total[author] += 1
    for author, s2vals in per_author_ambush.items():
        total = author_total.get(author, 1)
        if total < 50:
            continue
        author_ambush_density[author] = {
            "count": len(s2vals),
            "density": len(s2vals) / total,
            "mean_s2": statistics.mean(s2vals) if s2vals else 0,
        }

    return {
        "perfect_ambush": sorted(perfect_ambush, key=lambda x: -x["s2"])[:100],
        "perfect_fulfillment": sorted(perfect_fulfillment, key=lambda x: x["s2"])[:20],
        "era_ambush_density": era_ambush_density,
        "author_ambush_density": author_ambush_density,
        "quintile_alpha_means": quintile_means,
        "n_perfect_ambush": len(perfect_ambush),
        "n_perfect_fulfillment": len(perfect_fulfillment),
    }


def print_report(results):
    print("=" * 80)
    print("PERFECT AMBUSH ANALYSIS: High-α + High-S₂ Moments in Poetry")
    print(f"  {results['n_perfect_ambush']} perfect ambush events (α≥2.5, S₂≥5.0)")
    print(f"  {results['n_perfect_fulfillment']} perfect fulfillment events (α≥2.5, S₂≤−3.0)")
    print("=" * 80)

    # --- Within-poem α trajectory
    print("\n## Within-Poem Zipf-α Trajectory")
    labels = ["Q1 (0-20%)", "Q2 (20-40%)", "Q3 (40-60%)", "Q4 (60-80%)", "Q5 (80-100%)"]
    for label, mean_a in zip(labels, results["quintile_alpha_means"]):
        bar = "█" * int(mean_a * 10)
        print(f"  {label}: α = {mean_a:.3f}  {bar}")

    # --- Top perfect ambush moments
    print("\n## Top Perfect Ambush Moments (α≥2.5, S₂≥5.0)")
    print(f"  {'Author':<35} {'Title':<35} {'Token':<12} {'Top1':<12} {'Top1p':>6} {'S₂':>6} {'α':>5}")
    print("  " + "-" * 115)
    for rec in results["perfect_ambush"][:25]:
        print(
            f"  {rec['author'][:34]:<35} {rec['title'][:34]:<35} "
            f"{repr(rec['token']):<12} {repr(rec['top1_token']):<12} "
            f"{rec['top1_prob']:6.3f} {rec['s2']:6.1f} {rec['alpha']:5.2f}"
        )

    # --- Era ambush density
    print("\n## Era Perfect-Ambush Density (perfect ambushes per 1000 clean tokens)")
    ranked = sorted(
        results["era_ambush_density"].items(),
        key=lambda x: -x[1]["density"]
    )
    for era, stats in ranked[:20]:
        density_per1k = stats["density"] * 1000
        bar = "█" * int(density_per1k * 2)
        print(
            f"  {era:<30} {stats['count']:4d} events  "
            f"{density_per1k:6.2f}/1k  avgS₂={stats['mean_s2']:5.2f}  {bar}"
        )

    # --- Author ambush density
    print("\n## Author Perfect-Ambush Density (top 20 by density)")
    ranked_authors = sorted(
        results["author_ambush_density"].items(),
        key=lambda x: -x[1]["density"]
    )
    for author, stats in ranked_authors[:20]:
        density_per1k = stats["density"] * 1000
        print(
            f"  {author[:40]:<42} {stats['count']:3d} events  "
            f"{density_per1k:6.2f}/1k  avgS₂={stats['mean_s2']:5.2f}"
        )

    # --- Perfect fulfillment examples (model confirmed)
    print("\n## Perfect Fulfillment Events (α≥2.5, S₂≤−3.0: model's confident prediction confirmed)")
    print(f"  {'Author':<35} {'Token':<12} {'Top1':<12} {'Top1p':>6} {'S₂':>6} {'α':>5}")
    print("  " + "-" * 85)
    for rec in results["perfect_fulfillment"][:10]:
        print(
            f"  {rec['author'][:34]:<35} "
            f"{repr(rec['token']):<12} {repr(rec['top1_token']):<12} "
            f"{rec['top1_prob']:6.3f} {rec['s2']:6.1f} {rec['alpha']:5.2f}"
        )


if __name__ == "__main__":
    results = run()
    print_report(results)
    with open("results/perfect_ambush.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/perfect_ambush.json")
