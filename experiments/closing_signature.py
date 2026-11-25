"""
Closing-Signature Hypothesis
==============================
Since Q4_III (closing conformity) was the most era-discriminating arc feature,
this experiment asks: can the LAST 20% of a poem's tokens alone classify literary
era better than the full 8-dim arc?

Builds on: findings/arc_era_classifier.md
Hypothesis: If Q4_III is most discriminating, then a classifier using only the
closing segment should outperform the full-arc 2.4× improvement over chance.

Design:
1. Split each poem into: opening (first 20%), middle (20–80%), closing (last 20%)
2. Compute Type I%, Type II%, Type III%, avg S2, entropy profile for each segment
3. Build nearest-centroid classifiers for each segment and their combinations
4. Compare accuracy across: closing-only vs opening-only vs middle-only vs full arc
5. Identify which eras have most distinctive "closing signatures"
"""

import json
import math
import sys
from collections import defaultdict


def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)


def clean_tokens(tokens):
    """Filter stanza-break artifact positions."""
    return [
        t for t in tokens
        if t.get("p_newline", 0) < 0.9 and "\n" not in t["token"]
    ]


def segment_features(segment, global_median_entropy):
    """
    Compute closing/opening/middle feature vector for a token segment.
    Returns a 6-dim feature vector:
      [type_I%, type_II%, type_III%, avg_s2, avg_entropy, entropy_volatility]
    """
    if len(segment) < 5:
        return None

    n = len(segment)
    type_I = sum(
        1 for t in segment
        if t["s2"] > 0 and t["rank"] > 10 and t["entropy"] < global_median_entropy
    )
    type_II = sum(
        1 for t in segment
        if t["s2"] > 0 and t["entropy"] >= global_median_entropy
    )
    type_III = sum(
        1 for t in segment
        if t["s2"] <= 0 and t["rank"] <= 10 and t["entropy"] < global_median_entropy
    )

    avg_s2 = sum(t["s2"] for t in segment) / n
    avg_h = sum(t["entropy"] for t in segment) / n
    # Entropy volatility: std of entropy within segment
    if n > 1:
        h_var = sum((t["entropy"] - avg_h) ** 2 for t in segment) / (n - 1)
        h_std = math.sqrt(h_var)
    else:
        h_std = 0.0

    return [type_I / n, type_II / n, type_III / n, avg_s2, avg_h, h_std]


def compute_poem_features(poem_tokens, min_clean_tokens=20):
    """
    Compute opening/middle/closing feature vectors for a single poem.
    Returns dict with 'opening', 'middle', 'closing', 'full', 'n_clean'
    """
    clean = clean_tokens(poem_tokens)
    n = len(clean)
    if n < min_clean_tokens:
        return None

    # Global median entropy for this poem (used for Type I/III classification)
    entropies = sorted(t["entropy"] for t in clean)
    median_h = entropies[n // 2]

    # Segment boundaries
    opening_end = max(1, int(n * 0.20))
    closing_start = min(n - 1, int(n * 0.80))

    opening = clean[:opening_end]
    middle = clean[opening_end:closing_start]
    closing = clean[closing_start:]

    opening_feat = segment_features(opening, median_h)
    middle_feat = segment_features(middle, median_h)
    closing_feat = segment_features(closing, median_h)
    full_feat = segment_features(clean, median_h)

    if opening_feat is None or closing_feat is None or full_feat is None:
        return None

    return {
        "n_clean": n,
        "opening": opening_feat,
        "middle": middle_feat,
        "closing": closing_feat,
        "full": full_feat,
        # Combined: opening + closing (bypass the middle)
        "open_close": opening_feat + closing_feat,
        # 8-dim arc (compatible with arc_era_classifier baseline)
        # just use closing alone as the main test
    }


def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))


def compute_centroid(vectors):
    if not vectors:
        return None
    n = len(vectors)
    dim = len(vectors[0])
    return [sum(v[i] for v in vectors) / n for i in range(dim)]


def leave_one_out(poems_by_era, feature_key):
    """
    Run leave-one-out nearest-centroid classification using feature_key.
    Returns (accuracy, correct, total, per_era_results).
    """
    # Gather all poems with this feature
    all_poems = []
    for era, poems in poems_by_era.items():
        for p in poems:
            feat = p["features"].get(feature_key)
            if feat is not None:
                all_poems.append({"era": era, "feat": feat, **p})

    # Filter eras with >= 3 valid poems
    era_poem_map = defaultdict(list)
    for p in all_poems:
        era_poem_map[p["era"]].append(p)
    valid_eras = {era: poems for era, poems in era_poem_map.items() if len(poems) >= 3}

    if len(valid_eras) < 2:
        return 0.0, 0, 0, {}

    # Compute era centroids
    centroids = {
        era: compute_centroid([p["feat"] for p in poems])
        for era, poems in valid_eras.items()
    }

    correct = 0
    total = 0
    per_era = defaultdict(lambda: {"correct": 0, "total": 0, "wrong": []})

    for poem in all_poems:
        true_era = poem["era"]
        if true_era not in valid_eras:
            continue

        era_poems = valid_eras[true_era]
        other_feats = [p["feat"] for p in era_poems if p is not poem]
        if len(other_feats) < 2:
            continue

        # Recompute centroid without this poem
        temp_centroids = dict(centroids)
        temp_centroids[true_era] = compute_centroid(other_feats)

        # Find nearest
        best_era = None
        best_dist = float("inf")
        for era, centroid in temp_centroids.items():
            d = euclidean_dist(poem["feat"], centroid)
            if d < best_dist:
                best_dist = d
                best_era = era

        is_correct = best_era == true_era
        if is_correct:
            correct += 1
        per_era[true_era]["total"] += 1
        per_era[true_era]["correct"] += (1 if is_correct else 0)
        if not is_correct:
            per_era[true_era]["wrong"].append(best_era)
        total += 1

    acc = correct / total if total > 0 else 0.0
    return acc, correct, total, dict(per_era)


def main():
    corpus = load_corpus()

    poems_data = []
    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        feats = compute_poem_features(poem["tokens"])
        if feats is None:
            continue
        poems_data.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": era,
            "features": feats,
        })

    print(f"Poems with sufficient clean tokens: {len(poems_data)}")

    # Group by era for analysis
    by_era = defaultdict(list)
    for p in poems_data:
        by_era[p["era"]].append(p)

    # === Classification comparison ===
    print("\n=== Nearest-Centroid Era Classification Accuracy ===")
    print(f"{'Feature Set':<25} {'Acc':>8} {'Corr/Tot':>12} {'vs Chance':>12}")

    results = {}
    for feat_key in ["full", "opening", "middle", "closing", "open_close"]:
        acc, corr, tot, per_era = leave_one_out(by_era, feat_key)
        n_classes = len([e for e, ps in by_era.items()
                         if sum(1 for p in ps if p["features"].get(feat_key) is not None) >= 3])
        chance = 1.0 / n_classes if n_classes > 0 else 0
        ratio = acc / chance if chance > 0 else 0
        print(f"  {feat_key:<23} {acc:>7.1%} {corr:>6}/{tot:<5}  {ratio:.2f}× chance")
        results[feat_key] = {
            "accuracy": acc,
            "correct": corr,
            "total": tot,
            "n_classes": n_classes,
            "chance": chance,
            "improvement_over_chance": ratio,
            "per_era": per_era,
        }

    # === Per-era closing accuracy ===
    closing_res = results["closing"]["per_era"]
    print("\n=== Per-Era Accuracy with Closing-Only Classifier (sorted by accuracy) ===")
    print(f"{'Era':<30} {'N':>5} {'Acc':>8} {'Confused with'}")
    era_rows = []
    for era, res in closing_res.items():
        n = res["total"]
        acc = res["correct"] / n if n > 0 else 0
        confused = max(set(res["wrong"]), key=res["wrong"].count) if res["wrong"] else "—"
        era_rows.append((era, n, acc, confused))
    era_rows.sort(key=lambda x: -x[2])
    for era, n, acc, confused in era_rows:
        print(f"  {era:<28} {n:>5} {acc:>7.1%}  {confused}")

    # === Closing segment profiles per era ===
    print("\n=== Closing Segment Profiles by Era ===")
    print(f"{'Era':<25} {'N':>4} {'I%':>7} {'II%':>7} {'III%':>7} {'AvgS2':>7} {'AvgH':>7}")
    era_closing_profiles = {}
    for era, poems in sorted(by_era.items(), key=lambda x: len(x[1]), reverse=True):
        closing_feats = [p["features"]["closing"] for p in poems
                         if p["features"].get("closing") is not None]
        if len(closing_feats) < 3:
            continue
        n = len(closing_feats)
        dim = len(closing_feats[0])
        centroid = [sum(f[i] for f in closing_feats) / n for i in range(dim)]
        I_pct, II_pct, III_pct, avg_s2, avg_h, h_std = centroid
        era_closing_profiles[era] = {
            "n": n,
            "type_I": round(I_pct, 4),
            "type_II": round(II_pct, 4),
            "type_III": round(III_pct, 4),
            "avg_s2": round(avg_s2, 3),
            "avg_entropy": round(avg_h, 3),
            "entropy_volatility": round(h_std, 3),
        }
        print(f"  {era:<23} {n:>4} {I_pct:>7.1%} {II_pct:>7.1%} {III_pct:>7.1%} {avg_s2:>7.3f} {avg_h:>7.3f}")

    # === Opening vs Closing divergence ===
    print("\n=== Opening vs Closing Divergence (Type I% difference) ===")
    print("Positive = more surprise in opening; Negative = more surprise in closing (volta)")
    print(f"{'Era':<25} {'N':>4} {'Open I%':>9} {'Close I%':>9} {'Δ(Open-Close)':>14}")
    divergence_rows = []
    for era, poems in by_era.items():
        opening_feats = [p["features"]["opening"] for p in poems
                         if p["features"].get("opening") is not None]
        closing_feats = [p["features"]["closing"] for p in poems
                         if p["features"].get("closing") is not None]
        if len(opening_feats) < 3 or len(closing_feats) < 3:
            continue
        open_I = sum(f[0] for f in opening_feats) / len(opening_feats)
        close_I = sum(f[0] for f in closing_feats) / len(closing_feats)
        delta = open_I - close_I
        divergence_rows.append((era, len(opening_feats), open_I, close_I, delta))
    divergence_rows.sort(key=lambda x: -x[4])  # Most front-loaded first
    for era, n, o_I, c_I, delta in divergence_rows:
        print(f"  {era:<23} {n:>4} {o_I:>9.1%} {c_I:>9.1%} {delta:>+14.3f}")

    # Save results
    output = {
        "classification_comparison": {
            k: {
                "accuracy": v["accuracy"],
                "correct": v["correct"],
                "total": v["total"],
                "n_classes": v["n_classes"],
                "chance_baseline": v["chance"],
                "improvement_over_chance": round(v["improvement_over_chance"], 3),
            }
            for k, v in results.items()
        },
        "era_closing_profiles": era_closing_profiles,
        "per_era_closing_accuracy": {
            era: {
                "n": res["total"],
                "accuracy": res["correct"] / res["total"] if res["total"] > 0 else 0,
                "confused_with": max(set(res["wrong"]), key=res["wrong"].count)
                    if res["wrong"] else None,
            }
            for era, res in closing_res.items()
        },
    }

    with open("results/closing_signature.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/closing_signature.json")


if __name__ == "__main__":
    main()
