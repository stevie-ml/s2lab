"""
Poet S₂ Fingerprints: Do individual poets have distinctive information-theoretic signatures?

We extract the full token-level S₂ distribution for each poet and characterize it
along several axes: central tendency, volatility, skewness, tail behavior, and
the ratio of "surprising" to "predictable" tokens.

The key question: are poet fingerprints stable across poems by the same author,
and do they separate meaningfully from other poets?
"""

import json
import numpy as np
from collections import defaultdict
from scipy import stats
from scipy.spatial.distance import cdist

def load_corpus(path="results/corpus_results.json"):
    with open(path) as f:
        return json.load(f)

def poet_features(s2_vals):
    arr = np.array(s2_vals)
    return {
        "n_tokens": len(arr),
        "mean_s2": float(np.mean(arr)),
        "median_s2": float(np.median(arr)),
        "std_s2": float(np.std(arr)),
        "skewness": float(stats.skew(arr)),
        "kurtosis": float(stats.kurtosis(arr)),  # excess kurtosis
        "pos_ratio": float(np.mean(arr > 0)),
        "spike_ratio": float(np.mean(arr > 5)),
        "deep_neg_ratio": float(np.mean(arr < -5)),
        "mean_median_gap": float(np.mean(arr) - np.median(arr)),  # indicates right-skew spikes
        "q75": float(np.percentile(arr, 75)),
        "q95": float(np.percentile(arr, 95)),
        "q99": float(np.percentile(arr, 99)),
    }

def poem_features(tokens):
    s2_vals = [t["s2"] for t in tokens if t.get("s2") is not None]
    return poet_features(s2_vals) if len(s2_vals) >= 10 else None

def within_poet_consistency(poems_data):
    """How consistent is a poet across their poems? Returns mean pairwise Pearson r on features."""
    feature_keys = ["mean_s2", "std_s2", "skewness", "kurtosis", "pos_ratio", "spike_ratio"]
    vecs = []
    for p in poems_data:
        f = p["features"]
        vecs.append([f[k] for k in feature_keys])
    if len(vecs) < 2:
        return None
    vecs = np.array(vecs)
    rs = []
    for i in range(len(vecs)):
        for j in range(i+1, len(vecs)):
            r, _ = stats.pearsonr(vecs[i], vecs[j])
            rs.append(r)
    return float(np.mean(rs))

def run():
    data = load_corpus()

    # Collect per-poem and per-poet S2 values
    poet_tokens = defaultdict(list)
    poet_poems = defaultdict(list)

    for item in data:
        meta = item["metadata"]
        author = meta["author"]
        lang = meta.get("language", "en")
        if lang != "en":
            continue
        tokens = item.get("tokens", [])
        s2_vals = [t["s2"] for t in tokens if t.get("s2") is not None]
        if len(s2_vals) < 15:
            continue
        f = poet_features(s2_vals)
        poet_tokens[author].extend(s2_vals)
        poet_poems[author].append({
            "title": meta["title"],
            "n_tokens": len(s2_vals),
            "features": f,
        })

    # Compute aggregate poet fingerprints
    poet_fingerprints = {}
    for author, vals in poet_tokens.items():
        if len(vals) < 20:
            continue
        f = poet_features(vals)
        f["n_poems"] = len(poet_poems[author])
        f["within_consistency"] = within_poet_consistency(poet_poems[author])
        poet_fingerprints[author] = f

    # Feature matrix for clustering / similarity
    feature_keys = ["mean_s2", "std_s2", "skewness", "kurtosis", "pos_ratio", "spike_ratio", "mean_median_gap"]
    poets_ordered = sorted(poet_fingerprints.keys(), key=lambda p: -poet_fingerprints[p]["mean_s2"])

    feature_matrix = np.array([[poet_fingerprints[p][k] for k in feature_keys] for p in poets_ordered])
    # Normalize
    feature_matrix_norm = (feature_matrix - feature_matrix.mean(0)) / (feature_matrix.std(0) + 1e-8)

    # Pairwise distances between poets
    dists = cdist(feature_matrix_norm, feature_matrix_norm, metric="euclidean")

    # Find most similar pairs
    similar_pairs = []
    for i in range(len(poets_ordered)):
        for j in range(i+1, len(poets_ordered)):
            similar_pairs.append((dists[i, j], poets_ordered[i], poets_ordered[j]))
    similar_pairs.sort()

    # Archetypal classification
    def classify(f):
        m = f["mean_s2"]
        k = f["kurtosis"]
        sk = f["skewness"]
        sp = f["spike_ratio"]
        if m > 1.0 and sp > 0.15:
            return "HIGH-DEVIATION SPIKER"
        elif m > 0.5:
            return "CONSISTENTLY SURPRISING"
        elif k > 8 and m < 0:
            return "SPIKE-HEAVY CONFORMIST"
        elif m < -0.8:
            return "LANGUAGE CONFORMIST"
        else:
            return "MODERATE DEVIANT"

    results = {
        "poet_fingerprints": {
            p: dict(feat=poet_fingerprints[p], archetype=classify(poet_fingerprints[p]))
            for p in poets_ordered
        },
        "most_similar_pairs": [(d, a, b) for d, a, b in similar_pairs[:10]],
        "most_dissimilar_pairs": [(d, a, b) for d, a, b in similar_pairs[-10:]],
        "feature_keys": feature_keys,
        "poets_ordered": poets_ordered,
    }

    return results, feature_matrix_norm, dists, poets_ordered, poet_fingerprints

if __name__ == "__main__":
    results, feat_mat, dists, poets, fingerprints = run()

    print("\n=== POET S₂ FINGERPRINTS ===\n")
    print(f"{'Poet':<30} {'Arch':<28} {'Mean':>6} {'Std':>5} {'Skew':>5} {'Kurt':>6} {'Pos%':>5} {'Spk%':>5} {'Consst':>7}")
    print("-" * 110)
    for p in poets:
        f = fingerprints[p]
        arch = results["poet_fingerprints"][p]["archetype"]
        cons = f.get("within_consistency")
        cons_str = f"{cons:.2f}" if cons is not None else "  -  "
        print(f"{p:<30} {arch:<28} {f['mean_s2']:>6.3f} {f['std_s2']:>5.2f} {f['skewness']:>5.2f} {f['kurtosis']:>6.2f} {f['pos_ratio']:>5.2f} {f['spike_ratio']:>5.2f} {cons_str:>7}")

    print("\n=== MOST SIMILAR POET PAIRS (close fingerprints) ===")
    for d, a, b in results["most_similar_pairs"][:8]:
        print(f"  dist={d:.3f}  {a}  ≈  {b}")

    print("\n=== MOST DISSIMILAR POET PAIRS ===")
    for d, a, b in results["most_dissimilar_pairs"][-8:]:
        print(f"  dist={d:.3f}  {a}  ≠  {b}")
