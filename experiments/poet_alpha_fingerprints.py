"""
Poet-Level α Arc Fingerprints and the Pre-Climax Dip

Building on alpha_arc_within_poem.md which found:
- Global α arc slope = +0.213 (r = 0.888) — GPT-2's predictions concentrate as poems progress
- A systematic DIP at deciles 7-8 (1.394, 1.386) before the final peak (1.451)
- 76% of individual poems show rising α

This experiment asks:
1. Do individual poets have characteristic α arc shapes (fingerprints)?
2. Is the pre-climax dip universal, or concentrated in specific eras/poets?
3. What is the lexical character of the dip zone vs. the final peak zone?

A flat or falling α arc (poet resists GPT-2 concentration) would indicate a poet who
systematically avoids teaching the model their idiom — strategic opacity.
A steep rising arc indicates "earned Liberation" — the poem first makes GPT-2 confident,
then defeats its concentrated predictions.
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/poet_alpha_fingerprints.json"

MIN_POEMS = 3    # minimum poems per poet to include in poet-level analysis
MIN_TOKENS = 20  # minimum non-artifact tokens per poem
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
    n = len(xs)
    if n < 3:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    ssxx = sum((x - mx) ** 2 for x in xs)
    ssxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if ssxx == 0:
        return None, None
    slope = ssxy / ssxx
    ssy = sum((y - my) ** 2 for y in ys)
    r = ssxy / math.sqrt(ssxx * ssy) if ssxx * ssy > 0 else None
    return slope, r


def classify_arc(decile_means):
    """Classify the shape of an α arc from 10 decile means."""
    if not decile_means or len(decile_means) < 5:
        return "insufficient"
    vals = decile_means
    n = len(vals)
    # Overall slope
    xs = list(range(n))
    slope, r = linear_slope(xs, vals)
    if slope is None:
        return "flat"
    # Find position of minimum and maximum
    min_pos = vals.index(min(vals))
    max_pos = vals.index(max(vals))
    # Classify
    if abs(slope) < 0.05:
        return "plateau"
    if slope > 0.15 and r is not None and r > 0.7:
        return "ramp"
    if slope < -0.15 and r is not None and r < -0.7:
        return "descent"
    # Dome: max in middle, falls at end
    if max_pos in [3, 4, 5, 6] and vals[-1] < vals[max_pos] - 0.1:
        return "dome"
    # Valley: min in middle, rises at end
    if min_pos in [3, 4, 5, 6] and vals[-1] > vals[min_pos] + 0.1:
        return "valley"
    if slope > 0:
        return "rising"
    return "falling"


def extract_poem_alpha_arc(poem):
    """Extract per-decile α values and lexical data for a poem."""
    tokens = poem.get("tokens", [])
    # Filter artifact tokens (stanza-break artifact)
    clean = [t for t in tokens if t.get("p_newline", 0) < 0.9 and t.get("token", "").strip()]
    if len(clean) < MIN_TOKENS:
        return None

    n = len(clean)
    decile_alphas = defaultdict(list)
    decile_s2 = defaultdict(list)
    # Track lexical info for dip zone (deciles 6-7) vs peak zone (deciles 8-9)
    zone_tokens = {"dip": [], "peak": []}

    for i, t in enumerate(clean):
        pos_frac = i / n
        decile = min(int(pos_frac * N_DECILES), N_DECILES - 1)

        alts = t.get("alternatives", [])
        if alts:
            probs = [a["prob"] for a in alts]
            alpha = fit_zipf_exponent(probs)
            if alpha is not None:
                decile_alphas[decile].append(alpha)

        s2 = t.get("s2")
        if s2 is not None:
            decile_s2[decile].append(s2)

        # Lexical zone annotation
        if decile in [6, 7]:
            zone_tokens["dip"].append({
                "token": t.get("token", ""),
                "s2": s2,
                "entropy": t.get("entropy"),
                "rank": t.get("rank"),
            })
        elif decile in [8, 9]:
            zone_tokens["peak"].append({
                "token": t.get("token", ""),
                "s2": s2,
                "entropy": t.get("entropy"),
                "rank": t.get("rank"),
            })

    # Build decile summaries
    decile_means_alpha = []
    decile_means_s2 = []
    for d in range(N_DECILES):
        if decile_alphas[d]:
            decile_means_alpha.append(statistics.mean(decile_alphas[d]))
        else:
            decile_means_alpha.append(None)
        if decile_s2[d]:
            decile_means_s2.append(statistics.mean(decile_s2[d]))
        else:
            decile_means_s2.append(None)

    # Compute arc slope
    valid_x = [i for i, v in enumerate(decile_means_alpha) if v is not None]
    valid_y = [decile_means_alpha[i] for i in valid_x]
    slope, r = linear_slope(valid_x, valid_y) if len(valid_x) >= 3 else (None, None)

    # Dip metric: how much does α drop at deciles 6-7 vs adjacent deciles 5 and 8?
    dip_metric = None
    vals = [v for v in decile_means_alpha if v is not None]
    if len(decile_means_alpha) >= 10:
        pre = [decile_means_alpha[d] for d in [4, 5] if decile_means_alpha[d] is not None]
        dip = [decile_means_alpha[d] for d in [6, 7] if decile_means_alpha[d] is not None]
        post = [decile_means_alpha[d] for d in [8, 9] if decile_means_alpha[d] is not None]
        if pre and dip and post:
            dip_metric = statistics.mean(dip) - (statistics.mean(pre) + statistics.mean(post)) / 2
            # Negative = dip (the dip zone is BELOW the surrounding zones)

    arc_type = classify_arc([v for v in decile_means_alpha if v is not None])

    return {
        "decile_alpha": decile_means_alpha,
        "decile_s2": decile_means_s2,
        "arc_slope": slope,
        "arc_r": r,
        "arc_type": arc_type,
        "dip_metric": dip_metric,  # negative = dip exists
        "n_tokens": n,
        "zone_dip_avg_s2": statistics.mean([t["s2"] for t in zone_tokens["dip"] if t["s2"] is not None]) if zone_tokens["dip"] else None,
        "zone_peak_avg_s2": statistics.mean([t["s2"] for t in zone_tokens["peak"] if t["s2"] is not None]) if zone_tokens["peak"] else None,
        "zone_dip_avg_rank": statistics.mean([t["rank"] for t in zone_tokens["dip"] if t.get("rank") is not None]) if zone_tokens["dip"] else None,
        "zone_peak_avg_rank": statistics.mean([t["rank"] for t in zone_tokens["peak"] if t.get("rank") is not None]) if zone_tokens["peak"] else None,
        "zone_dip_avg_entropy": statistics.mean([t["entropy"] for t in zone_tokens["dip"] if t.get("entropy") is not None]) if zone_tokens["dip"] else None,
        "zone_peak_avg_entropy": statistics.mean([t["entropy"] for t in zone_tokens["peak"] if t.get("entropy") is not None]) if zone_tokens["peak"] else None,
    }


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Group by author and era
    poet_poems = defaultdict(list)
    era_poems = defaultdict(list)
    all_arcs = []

    for poem in corpus:
        meta = poem.get("metadata", {})
        author = meta.get("author", "unknown")
        era = meta.get("era", "unknown")
        arc = extract_poem_alpha_arc(poem)
        if arc is None:
            continue
        arc["title"] = meta.get("title", "?")
        arc["author"] = author
        arc["era"] = era
        all_arcs.append(arc)
        poet_poems[author].append(arc)
        era_poems[era].append(arc)

    print(f"Processed {len(all_arcs)} poems with sufficient tokens")

    # --- Global pre-climax dip analysis ---
    all_dips = [a["dip_metric"] for a in all_arcs if a["dip_metric"] is not None]
    global_dip_mean = statistics.mean(all_dips) if all_dips else None
    global_dip_negative_pct = sum(1 for d in all_dips if d < 0) / len(all_dips) if all_dips else None

    print(f"\n=== GLOBAL PRE-CLIMAX DIP ===")
    print(f"Mean dip metric: {global_dip_mean:.4f} (negative = dip exists)")
    print(f"Fraction of poems with dip (metric < 0): {global_dip_negative_pct:.1%}")

    # Compare zone metrics: dip zone vs peak zone
    dip_s2 = [a["zone_dip_avg_s2"] for a in all_arcs if a["zone_dip_avg_s2"] is not None]
    peak_s2 = [a["zone_peak_avg_s2"] for a in all_arcs if a["zone_peak_avg_s2"] is not None]
    dip_rank = [a["zone_dip_avg_rank"] for a in all_arcs if a["zone_dip_avg_rank"] is not None]
    peak_rank = [a["zone_peak_avg_rank"] for a in all_arcs if a["zone_peak_avg_rank"] is not None]
    dip_entropy = [a["zone_dip_avg_entropy"] for a in all_arcs if a["zone_dip_avg_entropy"] is not None]
    peak_entropy = [a["zone_peak_avg_entropy"] for a in all_arcs if a["zone_peak_avg_entropy"] is not None]

    print(f"\n=== DIP ZONE (dec 6-7) vs PEAK ZONE (dec 8-9) ===")
    print(f"Avg S₂: dip={statistics.mean(dip_s2):.3f}, peak={statistics.mean(peak_s2):.3f}" if dip_s2 and peak_s2 else "")
    print(f"Avg rank: dip={statistics.mean(dip_rank):.0f}, peak={statistics.mean(peak_rank):.0f}" if dip_rank and peak_rank else "")
    print(f"Avg entropy: dip={statistics.mean(dip_entropy):.3f}, peak={statistics.mean(peak_entropy):.3f}" if dip_entropy and peak_entropy else "")

    # --- Poet-level fingerprints ---
    poet_fingerprints = {}
    for author, poems in poet_poems.items():
        if len(poems) < MIN_POEMS:
            continue

        # Average decile α across poems
        avg_decile_alpha = []
        for d in range(N_DECILES):
            vals = [p["decile_alpha"][d] for p in poems if p["decile_alpha"][d] is not None]
            avg_decile_alpha.append(statistics.mean(vals) if vals else None)

        slopes = [p["arc_slope"] for p in poems if p["arc_slope"] is not None]
        dips = [p["dip_metric"] for p in poems if p["dip_metric"] is not None]
        arc_types = [p["arc_type"] for p in poems]

        # Classify average arc
        valid_vals = [v for v in avg_decile_alpha if v is not None]
        avg_arc_type = classify_arc(valid_vals)
        avg_slope, avg_r = linear_slope(
            [i for i, v in enumerate(avg_decile_alpha) if v is not None],
            [v for v in avg_decile_alpha if v is not None]
        ) if len([v for v in avg_decile_alpha if v is not None]) >= 3 else (None, None)

        era = poems[0]["era"] if poems else "unknown"
        poet_fingerprints[author] = {
            "n_poems": len(poems),
            "era": era,
            "avg_decile_alpha": avg_decile_alpha,
            "avg_arc_slope": avg_slope,
            "avg_arc_r": avg_r,
            "avg_arc_type": avg_arc_type,
            "mean_dip_metric": statistics.mean(dips) if dips else None,
            "pct_rising": sum(1 for s in slopes if s and s > 0) / len(slopes) if slopes else None,
            "individual_arc_types": {t: arc_types.count(t) for t in set(arc_types)},
        }

    print(f"\n=== POET α ARC FINGERPRINTS (poets with ≥{MIN_POEMS} poems) ===")
    # Sort by slope
    sorted_poets = sorted(
        [(a, v) for a, v in poet_fingerprints.items() if v["avg_arc_slope"] is not None],
        key=lambda x: x[1]["avg_arc_slope"],
        reverse=True
    )
    print(f"\n{'Author':<35} {'Era':<20} {'Slope':>8} {'Type':<12} {'Dip':>8} {'n':>4}")
    print("-" * 95)
    for author, fp in sorted_poets:
        dip = f"{fp['mean_dip_metric']:.3f}" if fp['mean_dip_metric'] is not None else "  N/A"
        slope = f"{fp['avg_arc_slope']:.3f}" if fp['avg_arc_slope'] is not None else "  N/A"
        print(f"{author:<35} {fp['era']:<20} {slope:>8} {fp['avg_arc_type']:<12} {dip:>8} {fp['n_poems']:>4}")

    # --- Era-level dip analysis ---
    era_dip_stats = {}
    for era, poems in era_poems.items():
        if len(poems) < 2:
            continue
        dips = [p["dip_metric"] for p in poems if p["dip_metric"] is not None]
        slopes = [p["arc_slope"] for p in poems if p["arc_slope"] is not None]
        if not dips:
            continue
        era_dip_stats[era] = {
            "n": len(poems),
            "mean_dip": statistics.mean(dips),
            "pct_dip": sum(1 for d in dips if d < 0) / len(dips),
            "mean_slope": statistics.mean(slopes) if slopes else None,
        }

    print(f"\n=== ERA-LEVEL DIP ANALYSIS (n≥3) ===")
    # Sort by mean dip (most negative = strongest dip)
    era_sorted = sorted(
        [(e, v) for e, v in era_dip_stats.items() if v["n"] >= 3],
        key=lambda x: x[1]["mean_dip"]
    )
    print(f"{'Era':<25} {'n':>4} {'Mean Dip':>10} {'%Dip':>7} {'Mean Slope':>12}")
    print("-" * 65)
    for era, stats in era_sorted:
        slope_str = f"{stats['mean_slope']:.3f}" if stats['mean_slope'] is not None else "  N/A"
        print(f"{era:<25} {stats['n']:>4} {stats['mean_dip']:>10.3f} {stats['pct_dip']:>6.1%} {slope_str:>12}")

    # --- Save output ---
    output = {
        "global": {
            "n_poems": len(all_arcs),
            "mean_dip_metric": global_dip_mean,
            "pct_poems_with_dip": global_dip_negative_pct,
            "dip_zone_avg_s2": statistics.mean(dip_s2) if dip_s2 else None,
            "peak_zone_avg_s2": statistics.mean(peak_s2) if peak_s2 else None,
            "dip_zone_avg_rank": statistics.mean(dip_rank) if dip_rank else None,
            "peak_zone_avg_rank": statistics.mean(peak_rank) if peak_rank else None,
            "dip_zone_avg_entropy": statistics.mean(dip_entropy) if dip_entropy else None,
            "peak_zone_avg_entropy": statistics.mean(peak_entropy) if peak_entropy else None,
        },
        "poet_fingerprints": poet_fingerprints,
        "era_dip_stats": era_dip_stats,
        "individual_poems": [{
            "title": a["title"],
            "author": a["author"],
            "era": a["era"],
            "arc_slope": a["arc_slope"],
            "arc_type": a["arc_type"],
            "dip_metric": a["dip_metric"],
        } for a in all_arcs],
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
