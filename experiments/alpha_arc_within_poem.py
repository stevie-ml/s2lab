"""
Within-Poem α (Zipf Coefficient) Arc: Does Prediction Concentration Change Over a Poem?

Building on two recent findings:
1. zipf_prediction_coefficient.md: α (Zipf exponent of top-10 prediction distribution)
   separates "high-stakes ambush" (high α) from "field escape" (low α) strategies.
2. liberation_arc_within_poem.md: Poems move from Anchoring-dominant openings to
   Liberation-dominant closings; the poem "teaches" GPT-2 its own grammar.

Key hypothesis: α should INCREASE over a poem's arc.
- Early poem: GPT-2 has minimal context → distributes probability broadly (low α)
- Late poem: GPT-2 has internalized the poem's idiom → concentrates on specific
  predictions (high α)

If confirmed, this provides a mechanistic explanation for the Liberation arc: late-poem
surprises achieve Liberation because α is now high — the poet defeats a concentrated
prediction. The poem earns its own Liberation by raising the stakes.

Secondary hypothesis: Era forms with strong Liberation arcs (villanelle, ballad)
should also show stronger α-increase arcs (the repetition actually sharpens
prediction concentration).
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/alpha_arc_within_poem.json"
MIN_TOKENS = 20   # minimum non-artifact tokens per poem
N_DECILES = 10


def fit_zipf_exponent(probs):
    """Fit Zipf exponent α via log-log regression on rank vs. probability."""
    if len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    if len(normed) < 2:
        return None

    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_probs = [math.log(p) for p in normed]

    mean_lr = sum(log_ranks) / n
    mean_lp = sum(log_probs) / n

    numer = sum((log_ranks[i] - mean_lr) * (log_probs[i] - mean_lp) for i in range(n))
    denom = sum((log_ranks[i] - mean_lr) ** 2 for i in range(n))

    if denom == 0:
        return None
    return -numer / denom


def linear_slope(xs, ys):
    """Return (slope, intercept, r) of least-squares line."""
    n = len(xs)
    if n < 3:
        return None, None, None
    mx, my = sum(xs) / n, sum(ys) / n
    ssxx = sum((x - mx) ** 2 for x in xs)
    ssxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if ssxx == 0:
        return None, None, None
    slope = ssxy / ssxx
    intercept = my - slope * mx
    # Pearson r
    ssy = sum((y - my) ** 2 for y in ys)
    if ssxx * ssy == 0:
        r = None
    else:
        r = ssxy / math.sqrt(ssxx * ssy)
    return slope, intercept, r


def classify_zipf(alpha):
    if alpha is None:
        return None
    if alpha >= 2.5:
        return "hyper_zipf"
    elif alpha >= 1.5:
        return "super_zipf"
    elif alpha >= 0.8:
        return "near_zipf"
    elif alpha >= 0.3:
        return "sub_zipf"
    else:
        return "anti_zipf"


def process_poem(poem):
    """Extract (normalized_position, alpha, s2, entropy) for clean tokens."""
    tokens = poem.get("tokens", [])
    # Filter artifacts
    clean = [t for t in tokens if t.get("p_newline", 0) <= 0.9]
    if len(clean) < MIN_TOKENS:
        return None

    n = len(clean)
    rows = []
    for i, tok in enumerate(clean):
        norm_pos = i / (n - 1) if n > 1 else 0.0
        alts = tok.get("alternatives", [])
        probs = [a["prob"] for a in alts] if alts else []
        alpha = fit_zipf_exponent(probs)
        if alpha is None:
            continue
        rows.append({
            "norm_pos": norm_pos,
            "alpha": alpha,
            "s2": tok.get("s2"),
            "entropy": tok.get("entropy"),
            "rank": tok.get("rank"),
        })
    return rows


def compute_decile_profile(rows):
    """Average α per decile [0–10%, 10–20%, …, 90–100%]."""
    buckets = [[] for _ in range(N_DECILES)]
    for row in rows:
        idx = min(int(row["norm_pos"] * N_DECILES), N_DECILES - 1)
        if row["alpha"] is not None:
            buckets[idx].append(row["alpha"])
    return [statistics.mean(b) if b else None for b in buckets]


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Exclude prose controls (no 'era' or era == 'prose_control')
    poems = [p for p in corpus if p.get("metadata", {}).get("era") != "prose_control"]

    # Per-poem analysis
    poem_arcs = []
    for poem in poems:
        meta = poem.get("metadata", {})
        rows = process_poem(poem)
        if rows is None or len(rows) < MIN_TOKENS:
            continue

        deciles = compute_decile_profile(rows)
        valid_deciles = [(i, v) for i, v in enumerate(deciles) if v is not None]
        if len(valid_deciles) < 5:
            continue

        xs = [i / (N_DECILES - 1) for i, _ in valid_deciles]
        ys = [v for _, v in valid_deciles]
        slope, intercept, r = linear_slope(xs, ys)

        # Compute mean α in first and last 3 deciles
        early_vals = [v for i, v in valid_deciles if i < 3]
        late_vals = [v for i, v in valid_deciles if i >= 7]
        early_alpha = statistics.mean(early_vals) if early_vals else None
        late_alpha = statistics.mean(late_vals) if late_vals else None

        poem_arcs.append({
            "title": meta.get("title", ""),
            "author": meta.get("author", ""),
            "era": meta.get("era", "unknown"),
            "year": meta.get("year"),
            "n_tokens": len(rows),
            "decile_alpha": deciles,
            "slope": slope,
            "r": r,
            "early_alpha": early_alpha,
            "late_alpha": late_alpha,
            "delta_alpha": (late_alpha - early_alpha) if (early_alpha and late_alpha) else None,
        })

    # Global decile profile
    decile_buckets = [[] for _ in range(N_DECILES)]
    for arc in poem_arcs:
        for i, v in enumerate(arc["decile_alpha"]):
            if v is not None:
                decile_buckets[i].append(v)

    global_decile = [statistics.mean(b) if b else None for b in decile_buckets]

    # Global slope
    xs = [i / (N_DECILES - 1) for i, v in enumerate(global_decile) if v is not None]
    ys = [v for v in global_decile if v is not None]
    global_slope, global_intercept, global_r = linear_slope(xs, ys)

    # Fraction of poems with increasing α arc
    increasing = sum(1 for a in poem_arcs if a["slope"] is not None and a["slope"] > 0)
    total_valid = sum(1 for a in poem_arcs if a["slope"] is not None)

    # Era-level profiles
    era_arcs = defaultdict(list)
    for arc in poem_arcs:
        era_arcs[arc["era"]].append(arc)

    era_summary = {}
    for era, arcs in era_arcs.items():
        slopes = [a["slope"] for a in arcs if a["slope"] is not None]
        deltas = [a["delta_alpha"] for a in arcs if a["delta_alpha"] is not None]
        early_alphas = [a["early_alpha"] for a in arcs if a["early_alpha"] is not None]
        late_alphas = [a["late_alpha"] for a in arcs if a["late_alpha"] is not None]
        era_summary[era] = {
            "n": len(arcs),
            "mean_slope": statistics.mean(slopes) if slopes else None,
            "mean_delta_alpha": statistics.mean(deltas) if deltas else None,
            "mean_early_alpha": statistics.mean(early_alphas) if early_alphas else None,
            "mean_late_alpha": statistics.mean(late_alphas) if late_alphas else None,
            "pct_increasing": 100 * sum(1 for s in slopes if s > 0) / len(slopes) if slopes else None,
        }

    # Top/bottom poems by slope
    sorted_arcs = sorted([a for a in poem_arcs if a["slope"] is not None], key=lambda a: a["slope"])
    strongest_decreasing = [{k: v for k, v in a.items() if k != "decile_alpha"} for a in sorted_arcs[:5]]
    strongest_increasing = [{k: v for k, v in a.items() if k != "decile_alpha"} for a in sorted_arcs[-5:]]

    # Correlation: α slope vs. Liberation arc slope
    # Load liberation arc data for cross-reference
    lib_data = {}
    try:
        with open("results/liberation_arc_within_poem.json") as f:
            lib_raw = json.load(f)
        for entry in lib_raw.get("per_poem", []):
            lib_data[entry.get("title", "")] = entry.get("arc_slope")
    except Exception:
        pass

    cross_ref = []
    for arc in poem_arcs:
        lib_slope = lib_data.get(arc["title"])
        if lib_slope is not None and arc["slope"] is not None:
            cross_ref.append({"alpha_slope": arc["slope"], "lib_slope": lib_slope})

    if cross_ref:
        alpha_slopes = [x["alpha_slope"] for x in cross_ref]
        lib_slopes = [x["lib_slope"] for x in cross_ref]
        _, _, cross_r = linear_slope(alpha_slopes, lib_slopes)
    else:
        cross_r = None

    result = {
        "n_poems": len(poem_arcs),
        "global_decile_alpha": global_decile,
        "global_slope": global_slope,
        "global_r": global_r,
        "pct_increasing_arc": 100 * increasing / total_valid if total_valid > 0 else None,
        "era_summary": era_summary,
        "strongest_decreasing_arcs": strongest_decreasing,
        "strongest_increasing_arcs": strongest_increasing,
        "alpha_liberation_correlation_r": cross_r,
        "n_crossref_poems": len(cross_ref),
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Analyzed {len(poem_arcs)} poems.")
    print(f"Global α decile profile: {[round(v, 3) if v else None for v in global_decile]}")
    print(f"Global slope: {global_slope:.4f} (r={global_r:.3f})")
    print(f"Poems with increasing α arc: {increasing}/{total_valid} ({100*increasing/total_valid:.1f}%)")
    print(f"α–Liberation arc correlation: r = {cross_r}")


if __name__ == "__main__":
    main()
