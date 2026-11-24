"""
Arc Fingerprint Era Classifier
===============================
Can the Q1→Q4 Type I% and Type III% arc pattern alone classify a poem's literary era?

Builds on findings/quarter_arc_mid_dip.md, which showed:
- Different eras have distinctive Q1→Q4 arc shapes
- Poets have consistent arc "fingerprints"
- Hypothesis C confirmed: arc patterns are measurable compositional signatures

This experiment:
1. Computes Q1→Q4 arcs for all poems with ≥40 artifact-free tokens
2. Computes era centroids
3. Tests nearest-centroid classification accuracy (leave-one-out)
4. Builds an arc distance matrix between eras
5. Finds "doubly constrained" eras (high Type I AND slow decline = most distinctive)

No torch/transformers needed — works from pre-computed corpus_results.json.
"""

import json
import math
import sys
from collections import defaultdict

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def compute_arc(tokens, n_quarters=4):
    """Compute Type I% and Type III% by quarter, excluding stanza-break artifacts."""
    # Filter artifact positions (p_newline > 0.9 OR newline token itself)
    clean = [t for t in tokens if t.get("p_newline", 0) < 0.9 and "\n" not in t["token"]]
    if len(clean) < 40:
        return None

    n = len(clean)
    q_size = n / n_quarters
    quarters_I = []
    quarters_III = []

    for q in range(n_quarters):
        start = int(q * q_size)
        end = int((q + 1) * q_size)
        segment = clean[start:end]
        if len(segment) == 0:
            quarters_I.append(0.0)
            quarters_III.append(0.0)
            continue

        # Type I: Definite Straussian Gap
        # surprise > 0 (unexpected choice) AND low entropy (confident context)
        median_entropy = sorted(t["entropy"] for t in clean)[n // 2]

        type_I = sum(
            1 for t in segment
            if t["s2"] > 0 and t["rank"] > 10 and t["entropy"] < median_entropy
        )
        type_III = sum(
            1 for t in segment
            if t["s2"] <= 0 and t["rank"] <= 10 and t["entropy"] < median_entropy
        )

        quarters_I.append(type_I / len(segment))
        quarters_III.append(type_III / len(segment))

    return {
        "I": quarters_I,
        "III": quarters_III,
        "delta_I": quarters_I[-1] - quarters_I[0],
        "delta_III": quarters_III[-1] - quarters_III[0],
        "n": n,
    }

def arc_to_feature_vector(arc):
    """8-dim feature vector from arc."""
    return arc["I"] + arc["III"]

def euclidean_dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))

def compute_centroid(vectors):
    if not vectors:
        return None
    n = len(vectors)
    return [sum(v[i] for v in vectors) / n for i in range(len(vectors[0]))]

def nearest_centroid_classify(feature, centroids_by_era, exclude_era=None):
    """Return predicted era using nearest centroid (Euclidean distance)."""
    best_era = None
    best_dist = float("inf")
    for era, centroid in centroids_by_era.items():
        if era == exclude_era:
            continue
        d = euclidean_dist(feature, centroid)
        if d < best_dist:
            best_dist = d
            best_era = era
    return best_era

def main():
    corpus = load_corpus()

    # Compute arcs for all poems
    poems_with_arcs = []
    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        arc = compute_arc(poem["tokens"])
        if arc is None:
            continue
        poems_with_arcs.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": era,
            "arc": arc,
            "feature": arc_to_feature_vector(arc),
        })

    print(f"Total poems with arcs: {len(poems_with_arcs)}")

    # Group by era
    by_era = defaultdict(list)
    for p in poems_with_arcs:
        by_era[p["era"]].append(p)

    eras_with_enough = {era: poems for era, poems in by_era.items() if len(poems) >= 3}
    print(f"Eras with ≥3 poems: {len(eras_with_enough)}")

    # Compute era centroids
    centroids = {}
    for era, poems in eras_with_enough.items():
        centroids[era] = compute_centroid([p["feature"] for p in poems])

    # === Leave-one-out cross-validation ===
    correct = 0
    total = 0
    per_era_results = defaultdict(lambda: {"correct": 0, "total": 0, "wrong": []})

    for poem in poems_with_arcs:
        true_era = poem["era"]
        if true_era not in eras_with_enough:
            continue

        # Recompute centroid without this poem
        era_poems = eras_with_enough[true_era]
        other_features = [p["feature"] for p in era_poems if p is not poem]
        if len(other_features) < 2:
            continue

        temp_centroids = dict(centroids)
        temp_centroids[true_era] = compute_centroid(other_features)

        predicted = nearest_centroid_classify(poem["feature"], temp_centroids)
        is_correct = predicted == true_era
        if is_correct:
            correct += 1
        per_era_results[true_era]["total"] += 1
        per_era_results[true_era]["correct"] += (1 if is_correct else 0)
        if not is_correct:
            per_era_results[true_era]["wrong"].append(predicted)
        total += 1

    overall_acc = correct / total if total > 0 else 0
    print(f"\nLeave-one-out accuracy: {correct}/{total} = {overall_acc:.3f} ({overall_acc*100:.1f}%)")
    print(f"Chance baseline (uniform): {1/len(eras_with_enough):.3f} ({100/len(eras_with_enough):.1f}%)\n")

    # === Per-era accuracy ===
    era_acc_list = []
    for era, res in per_era_results.items():
        acc = res["correct"] / res["total"] if res["total"] > 0 else 0
        most_confused = max(set(res["wrong"]), key=res["wrong"].count) if res["wrong"] else "—"
        era_acc_list.append((era, res["total"], acc, most_confused))

    era_acc_list.sort(key=lambda x: -x[2])

    print("=== Per-era accuracy (sorted) ===")
    print(f"{'Era':<30} {'N':>5} {'Acc':>8} {'Confused with'}")
    for era, n, acc, confused in era_acc_list:
        bar = "█" * int(acc * 20)
        print(f"{era:<30} {n:>5} {acc:>7.1%}  {confused}")

    # === Era centroid distance matrix ===
    print("\n=== Era Centroid Distances (top 10 most-similar pairs) ===")
    pairs = []
    era_list = list(centroids.keys())
    for i in range(len(era_list)):
        for j in range(i + 1, len(era_list)):
            e1, e2 = era_list[i], era_list[j]
            d = euclidean_dist(centroids[e1], centroids[e2])
            pairs.append((d, e1, e2))

    pairs.sort()
    print(f"{'Era 1':<25} {'Era 2':<25} {'Distance':>10}")
    for d, e1, e2 in pairs[:15]:
        print(f"{e1:<25} {e2:<25} {d:>10.4f}")

    print("\n=== Most Distant Era Pairs (most distinguishable) ===")
    for d, e1, e2 in pairs[-10:]:
        print(f"{e1:<25} {e2:<25} {d:>10.4f}")

    # === Era arc profiles ===
    print("\n=== Era Arc Profiles (Q1→Q2→Q3→Q4 Type I%) ===")
    print(f"{'Era':<25} {'N':>4} {'Q1':>7} {'Q2':>7} {'Q3':>7} {'Q4':>7} {'Δ(Q4-Q1)':>10} {'Shape'}")
    era_profiles = []
    for era, poems in sorted(eras_with_enough.items(), key=lambda x: -len(x[1])):
        arc_I = [p["arc"]["I"] for p in poems]
        mean_I = [sum(a[q] for a in arc_I) / len(arc_I) for q in range(4)]
        delta = mean_I[3] - mean_I[0]
        # Classify arc shape
        if delta < -0.03:
            shape = "deviate-early"
        elif delta > 0.03:
            shape = "volta"
        else:
            shape = "flat"
        min_q = mean_I.index(min(mean_I))
        if min_q in [1, 2]:
            shape += "+mid-trough"
        era_profiles.append((era, len(poems), mean_I, delta, shape))
        print(f"{era:<25} {len(poems):>4} {mean_I[0]:>7.1%} {mean_I[1]:>7.1%} {mean_I[2]:>7.1%} {mean_I[3]:>7.1%} {delta:>+10.3f}  {shape}")

    # === Best discriminating features ===
    print("\n=== Discriminability Analysis ===")
    # Compute variance of centroid values across eras (high variance = good discriminator)
    for feat_i, feat_name in enumerate(["Q1_I", "Q2_I", "Q3_I", "Q4_I",
                                          "Q1_III", "Q2_III", "Q3_III", "Q4_III"]):
        vals = [centroids[era][feat_i] for era in centroids]
        mean = sum(vals) / len(vals)
        var = sum((v - mean) ** 2 for v in vals) / len(vals)
        print(f"  {feat_name}: inter-era variance = {var:.6f}")

    # Save results
    output = {
        "n_poems": len(poems_with_arcs),
        "n_eras": len(eras_with_enough),
        "loo_accuracy": overall_acc,
        "correct": correct,
        "total": total,
        "chance_baseline": 1 / len(eras_with_enough),
        "per_era": {
            era: {
                "n": res["total"],
                "accuracy": res["correct"] / res["total"] if res["total"] > 0 else 0,
                "most_confused_with": max(set(res["wrong"]), key=res["wrong"].count)
                    if res["wrong"] else None,
            }
            for era, res in per_era_results.items()
        },
        "era_profiles": {
            era: {
                "n": n,
                "arc_I": [round(x, 4) for x in mean_I],
                "delta_I": round(delta, 4),
                "shape": shape,
            }
            for era, n, mean_I, delta, shape in era_profiles
        },
        "centroid_distance_top_similar": [
            {"era1": e1, "era2": e2, "distance": round(d, 4)}
            for d, e1, e2 in pairs[:15]
        ],
        "centroid_distance_top_different": [
            {"era1": e1, "era2": e2, "distance": round(d, 4)}
            for d, e1, e2 in pairs[-10:]
        ],
    }
    with open("results/arc_era_classifier.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/arc_era_classifier.json")

if __name__ == "__main__":
    main()
