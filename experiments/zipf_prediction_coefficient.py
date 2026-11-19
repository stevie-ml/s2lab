"""
Zipf Coefficient of Prediction Distributions:
Measuring the Power-Law Shape of GPT-2's Uncertainty

For each token position, the top-10 alternatives form a probability distribution.
In natural language, word-rank distributions follow Zipf's law:
  P(rank r) ∝ r^(-α)

We fit this exponent α (Zipf coefficient) to the top-10 alternatives at each
token position, then ask:
  1. Does α correlate with S2?
  2. Do different eras have characteristic α profiles?
  3. Is "super-Zipfian" (α >> 1) concentration different from "sub-Zipfian"
     (α << 1) diffusion in terms of what poets do?

A steep prediction distribution (high α) means the model is very confident
in its top-1 prediction relative to lower-ranked ones — classic "ambush" territory.
A flat prediction distribution (low α) means the model is diffuse and uncertain —
any choice is roughly equally (un)expected.

The key new question: Do poets who specialize in ambush (high S2 when α is high)
differ from those who specialize in fog (high S2 when α is low)?
"""

import json
import math
import statistics
from collections import defaultdict

def fit_zipf_exponent(probs):
    """
    Fit Zipf exponent α via log-log regression on rank vs. probability.
    P(r) ≈ C * r^(-α)
    log P(r) = log C - α * log r
    Returns α (positive = power law decay, higher = steeper).
    """
    if len(probs) < 2:
        return None
    # Normalize so they sum to 1
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    if len(normed) < 2:
        return None

    # Log-log regression
    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]  # rank 1-indexed
    log_probs = [math.log(p) for p in normed]

    mean_lr = sum(log_ranks) / n
    mean_lp = sum(log_probs) / n

    numer = sum((log_ranks[i] - mean_lr) * (log_probs[i] - mean_lp) for i in range(n))
    denom = sum((log_ranks[i] - mean_lr) ** 2 for i in range(n))

    if denom == 0:
        return None
    return -numer / denom  # negative because P decreases with rank


def zipf_r2(probs, alpha):
    """R² of the Zipf fit."""
    if alpha is None or len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_probs = [math.log(p) for p in normed]

    # Predicted values
    log_c = statistics.mean(log_probs) + alpha * statistics.mean(log_ranks)
    pred = [log_c - alpha * lr for lr in log_ranks]

    ss_res = sum((log_probs[i] - pred[i]) ** 2 for i in range(n))
    mean_lp = statistics.mean(log_probs)
    ss_tot = sum((lp - mean_lp) ** 2 for lp in log_probs)

    if ss_tot == 0:
        return 1.0
    return 1 - ss_res / ss_tot


def classify_zipf(alpha):
    """Classify the prediction distribution by Zipf coefficient."""
    if alpha is None:
        return "unknown"
    if alpha >= 2.5:
        return "hyper_zipf"      # steeper than Zipf, very concentrated
    elif alpha >= 1.5:
        return "super_zipf"      # steeper than natural language
    elif alpha >= 0.8:
            return "near_zipf"   # natural language-like
    elif alpha >= 0.3:
        return "sub_zipf"        # flatter, diffuse
    else:
        return "anti_zipf"       # nearly flat, maximally uncertain


def main():
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    # Per-era aggregates
    era_alpha = defaultdict(list)
    era_s2_by_class = defaultdict(lambda: defaultdict(list))
    era_highS2_class = defaultdict(lambda: defaultdict(int))

    # Zipf class vs S2 aggregates (global)
    class_s2 = defaultdict(list)
    class_entropy = defaultdict(list)
    class_rank = defaultdict(list)
    class_top1_prob = defaultdict(list)
    class_actual_prob = defaultdict(list)

    # Token-level stats for the analysis
    all_tokens = []

    for item in corpus:
        meta = item["metadata"]
        era = meta.get("era", "unknown")
        tokens = item.get("tokens", [])

        for tok in tokens:
            # Skip newline artifacts and control
            if tok.get("p_newline", 0) >= 0.9:
                continue
            if era in ("control", "prose_control"):
                continue

            alts = tok.get("alternatives", [])
            if len(alts) < 3:
                continue

            probs = [a["prob"] for a in alts]
            alpha = fit_zipf_exponent(probs)
            if alpha is None:
                continue

            r2 = zipf_r2(probs, alpha)
            zclass = classify_zipf(alpha)
            s2 = tok.get("s2", 0)
            entropy = tok.get("entropy", 0)
            rank = tok.get("rank", -1)
            top1_prob = probs[0] if probs else 0
            actual_prob = tok.get("prob", 0)

            era_alpha[era].append(alpha)
            era_s2_by_class[era][zclass].append(s2)
            if s2 >= 2.0:
                era_highS2_class[era][zclass] += 1

            class_s2[zclass].append(s2)
            class_entropy[zclass].append(entropy)
            class_rank[zclass].append(rank if rank >= 0 else 15)
            class_top1_prob[zclass].append(top1_prob)
            class_actual_prob[zclass].append(actual_prob)

            all_tokens.append({
                "era": era,
                "alpha": alpha,
                "r2": r2,
                "zclass": zclass,
                "s2": s2,
                "entropy": entropy,
                "rank": rank,
                "top1_prob": top1_prob,
                "actual_prob": actual_prob,
                "token": tok.get("token", "")
            })

    # --- Summary statistics ---
    print(f"\nTotal tokens analyzed: {len(all_tokens)}")
    print(f"Eras covered: {len(era_alpha)}")

    print("\n=== ZIPF CLASS DISTRIBUTION ===")
    classes = ["hyper_zipf", "super_zipf", "near_zipf", "sub_zipf", "anti_zipf"]
    total = len(all_tokens)
    for c in classes:
        n = len(class_s2[c])
        pct = 100 * n / total if total > 0 else 0
        mean_s2 = statistics.mean(class_s2[c]) if class_s2[c] else float("nan")
        mean_ent = statistics.mean(class_entropy[c]) if class_entropy[c] else float("nan")
        mean_rank = statistics.mean(class_rank[c]) if class_rank[c] else float("nan")
        mean_t1p = statistics.mean(class_top1_prob[c]) if class_top1_prob[c] else float("nan")
        high_s2_pct = 100 * sum(1 for s in class_s2[c] if s >= 2.0) / n if n > 0 else 0
        print(f"{c:15s}: n={n:6d} ({pct:5.1f}%) | mean_S2={mean_s2:+.3f} | "
              f"high_S2%={high_s2_pct:.1f} | H={mean_ent:.2f} | "
              f"rank={mean_rank:.1f} | top1_p={mean_t1p:.3f}")

    # --- Era analysis ---
    print("\n=== ERA ZIPF PROFILES (mean α, sorted) ===")
    era_stats = []
    for era, alphas in era_alpha.items():
        if len(alphas) < 50:
            continue
        mean_alpha = statistics.mean(alphas)
        std_alpha = statistics.stdev(alphas) if len(alphas) > 1 else 0
        # What fraction of tokens in this era are hyper/super Zipf?
        n_steep = sum(1 for a in alphas if a >= 1.5)
        pct_steep = 100 * n_steep / len(alphas)
        # What fraction are sub/anti Zipf?
        n_flat = sum(1 for a in alphas if a < 0.8)
        pct_flat = 100 * n_flat / len(alphas)
        # Mean S2 for this era
        all_s2 = []
        for c in classes:
            all_s2.extend(era_s2_by_class[era][c])
        mean_s2 = statistics.mean(all_s2) if all_s2 else float("nan")
        era_stats.append((era, mean_alpha, std_alpha, pct_steep, pct_flat, mean_s2, len(alphas)))

    era_stats.sort(key=lambda x: x[1], reverse=True)
    print(f"{'Era':25s} | mean_α | std_α | steep% | flat%  | mean_S2 | n")
    print("-" * 85)
    for era, ma, sa, ps, pf, ms2, n in era_stats:
        print(f"{era:25s} | {ma:6.3f} | {sa:5.3f} | {ps:6.1f} | {pf:6.1f} | {ms2:+.3f}  | {n}")

    # --- The key cross-analysis ---
    print("\n=== ZIPF CLASS × S2 LEVEL (global) ===")
    s2_buckets = [
        ("very_neg", lambda s: s < -3),
        ("neg",      lambda s: -3 <= s < 0),
        ("low_pos",  lambda s: 0 <= s < 2),
        ("high_pos", lambda s: 2 <= s < 5),
        ("extreme",  lambda s: s >= 5),
    ]
    # Build matrix
    matrix = {}
    for c in classes:
        matrix[c] = {}
        n_c = len(class_s2[c])
        for bname, bfn in s2_buckets:
            cnt = sum(1 for s in class_s2[c] if bfn(s))
            matrix[c][bname] = 100 * cnt / n_c if n_c > 0 else 0

    header = f"{'Class':15s}" + "".join(f" | {b[0]:9s}" for b, _ in s2_buckets)
    print(header)
    print("-" * (15 + 14 * len(s2_buckets)))
    for c in classes:
        row = f"{c:15s}"
        for bname, _ in s2_buckets:
            row += f" | {matrix[c][bname]:9.1f}"
        print(row)

    # --- Save results ---
    results = {
        "n_tokens": len(all_tokens),
        "class_summary": {
            c: {
                "n": len(class_s2[c]),
                "mean_s2": statistics.mean(class_s2[c]) if class_s2[c] else None,
                "mean_entropy": statistics.mean(class_entropy[c]) if class_entropy[c] else None,
                "mean_rank": statistics.mean(class_rank[c]) if class_rank[c] else None,
                "mean_top1_prob": statistics.mean(class_top1_prob[c]) if class_top1_prob[c] else None,
                "high_s2_pct": 100 * sum(1 for s in class_s2[c] if s >= 2.0) / len(class_s2[c]) if class_s2[c] else None,
                "s2_distribution": {
                    bname: 100 * sum(1 for s in class_s2[c] if bfn(s)) / len(class_s2[c])
                    for bname, bfn in s2_buckets
                } if class_s2[c] else {}
            }
            for c in classes
        },
        "era_profiles": {
            era: {
                "mean_alpha": ma,
                "std_alpha": sa,
                "pct_steep": ps,
                "pct_flat": pf,
                "mean_s2": ms2,
                "n_tokens": n
            }
            for era, ma, sa, ps, pf, ms2, n in era_stats
        }
    }

    with open("results/zipf_prediction_coefficient.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to results/zipf_prediction_coefficient.json")


if __name__ == "__main__":
    main()
