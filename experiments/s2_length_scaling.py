"""
S2 Scaling with Poem Length — Does surprise scale linearly with length,
or do longer poems show diminishing returns per token?

Hypothesis: Surprise is a finite resource; longer poems may show lower
S2 per token (habituation) or higher total surprise (accumulation).
We test for a power-law scaling relationship: total_S2 ~ length^alpha.
alpha > 1: super-linear (long poems pack more surprise per token)
alpha < 1: sub-linear (diminishing returns, habituation)
alpha = 1: no length effect
"""

import json
import math
import numpy as np
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
NEWLINE_PROB_THRESHOLD = 0.9  # artifact filter


def load_results():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def is_artifact(token_data):
    return token_data.get("p_newline", 0.0) > NEWLINE_PROB_THRESHOLD


def compute_poem_stats(poem):
    tokens = poem["tokens"]
    clean_tokens = [t for t in tokens if not is_artifact(t)]
    if not clean_tokens:
        return None

    s2_vals = [t["s2"] for t in clean_tokens]
    pos_s2 = [v for v in s2_vals if v > 0]

    n = len(clean_tokens)
    total_s2 = sum(pos_s2) if pos_s2 else 0
    avg_s2 = np.mean(s2_vals)
    max_s2 = max(s2_vals)
    pos_ratio = len(pos_s2) / n if n > 0 else 0

    # Gini coefficient of |s2| distribution
    abs_s2 = sorted([abs(v) for v in s2_vals])
    n_g = len(abs_s2)
    if n_g > 1 and sum(abs_s2) > 0:
        index = np.arange(1, n_g + 1)
        gini = (2 * np.dot(index, abs_s2)) / (n_g * sum(abs_s2)) - (n_g + 1) / n_g
    else:
        gini = 0.0

    return {
        "n_tokens": n,
        "n_tokens_raw": len(tokens),
        "total_pos_s2": total_s2,
        "avg_s2": avg_s2,
        "max_s2": max_s2,
        "pos_ratio": pos_ratio,
        "gini": gini,
        "era": poem["metadata"].get("era", "unknown"),
        "author": poem["metadata"].get("author", ""),
        "title": poem["metadata"].get("title", ""),
        "year": poem["metadata"].get("year"),
    }


def fit_power_law(lengths, totals):
    """Fit log(total) = alpha * log(length) + beta via OLS."""
    log_l = np.log(lengths)
    log_t = np.log([max(t, 1e-9) for t in totals])
    n = len(log_l)
    if n < 3:
        return None, None, None
    # OLS
    x = np.column_stack([log_l, np.ones(n)])
    coeffs, _, _, _ = np.linalg.lstsq(x, log_t, rcond=None)
    alpha, beta = coeffs
    # R^2
    log_t_pred = alpha * log_l + beta
    ss_res = np.sum((log_t - log_t_pred) ** 2)
    ss_tot = np.sum((log_t - np.mean(log_t)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0
    return alpha, beta, r2


def bin_by_length(stats, n_bins=5):
    lengths = [s["n_tokens"] for s in stats]
    if not lengths:
        return []
    edges = np.percentile(lengths, np.linspace(0, 100, n_bins + 1))
    edges = np.unique(edges)
    bins = []
    for i in range(len(edges) - 1):
        lo, hi = edges[i], edges[i + 1]
        in_bin = [s for s in stats if lo <= s["n_tokens"] <= hi]
        if not in_bin:
            continue
        avg_len = np.mean([s["n_tokens"] for s in in_bin])
        avg_s2_per_tok = np.mean([s["avg_s2"] for s in in_bin])
        avg_pos_ratio = np.mean([s["pos_ratio"] for s in in_bin])
        avg_max = np.mean([s["max_s2"] for s in in_bin])
        avg_gini = np.mean([s["gini"] for s in in_bin])
        bins.append({
            "range": f"{int(lo)}-{int(hi)}",
            "n_poems": len(in_bin),
            "avg_length": avg_len,
            "avg_s2_per_token": avg_s2_per_tok,
            "avg_pos_ratio": avg_pos_ratio,
            "avg_max_s2": avg_max,
            "avg_gini": avg_gini,
        })
    return bins


def era_scaling(stats):
    by_era = defaultdict(list)
    for s in stats:
        by_era[s["era"]].append(s)

    rows = []
    for era, poems in sorted(by_era.items(), key=lambda x: -len(x[1])):
        if len(poems) < 3:
            continue
        lengths = [p["n_tokens"] for p in poems]
        totals = [p["total_pos_s2"] for p in poems]
        alpha, beta, r2 = fit_power_law(lengths, totals)
        avg_len = np.mean(lengths)
        avg_s2 = np.mean([p["avg_s2"] for p in poems])
        rows.append({
            "era": era,
            "n": len(poems),
            "avg_len": round(avg_len, 1),
            "avg_s2": round(avg_s2, 3),
            "alpha": round(alpha, 3) if alpha is not None else None,
            "r2": round(r2, 3) if r2 is not None else None,
        })
    return sorted(rows, key=lambda x: (x["alpha"] or 0), reverse=True)


def main():
    data = load_results()
    # Filter English poems only
    en_poems = [p for p in data if p["metadata"].get("language", "en") == "en"]

    stats = []
    for poem in en_poems:
        s = compute_poem_stats(poem)
        if s and s["n_tokens"] >= 10:
            stats.append(s)

    stats.sort(key=lambda x: x["n_tokens"])

    # Global power law
    all_lengths = [s["n_tokens"] for s in stats]
    all_totals = [s["total_pos_s2"] for s in stats]
    alpha_global, beta_global, r2_global = fit_power_law(all_lengths, all_totals)

    # S2-per-token vs length power law
    all_avg_s2 = [s["avg_s2"] for s in stats]
    # use avg_s2 + offset to keep positive
    offset = abs(min(all_avg_s2)) + 1.0
    all_avg_s2_pos = [v + offset for v in all_avg_s2]
    alpha_per_tok, _, r2_per_tok = fit_power_law(all_lengths, all_avg_s2_pos)

    # Bins
    bins = bin_by_length(stats)

    # Era scaling
    era_rows = era_scaling(stats)

    # Length decile: extreme short vs long
    short_poems = sorted(stats, key=lambda x: x["n_tokens"])[:20]
    long_poems = sorted(stats, key=lambda x: x["n_tokens"])[-20:]

    short_avg = np.mean([s["avg_s2"] for s in short_poems])
    long_avg = np.mean([s["avg_s2"] for s in long_poems])
    short_pos = np.mean([s["pos_ratio"] for s in short_poems])
    long_pos = np.mean([s["pos_ratio"] for s in long_poems])
    short_gini = np.mean([s["gini"] for s in short_poems])
    long_gini = np.mean([s["gini"] for s in long_poems])

    result = {
        "n_poems": len(stats),
        "global_scaling": {
            "alpha": round(alpha_global, 4) if alpha_global else None,
            "r2": round(r2_global, 4) if r2_global else None,
            "interpretation": (
                "super-linear (long poems accumulate more surprise)" if alpha_global and alpha_global > 1
                else "sub-linear (diminishing returns)" if alpha_global and alpha_global < 1
                else "linear"
            )
        },
        "per_token_scaling": {
            "alpha": round(alpha_per_tok, 4) if alpha_per_tok else None,
            "r2": round(r2_per_tok, 4) if r2_per_tok else None,
        },
        "length_bins": bins,
        "era_scaling": era_rows,
        "short_vs_long": {
            "short_n": len(short_poems),
            "long_n": len(long_poems),
            "short_avg_len": round(np.mean([s["n_tokens"] for s in short_poems]), 1),
            "long_avg_len": round(np.mean([s["n_tokens"] for s in long_poems]), 1),
            "short_avg_s2": round(short_avg, 4),
            "long_avg_s2": round(long_avg, 4),
            "short_pos_ratio": round(short_pos, 4),
            "long_pos_ratio": round(long_pos, 4),
            "short_gini": round(short_gini, 4),
            "long_gini": round(long_gini, 4),
        }
    }

    import os
    os.makedirs("results", exist_ok=True)
    with open("results/s2_length_scaling.json", "w") as f:
        json.dump(result, f, indent=2)

    print(json.dumps(result, indent=2))
    return result


if __name__ == "__main__":
    main()
