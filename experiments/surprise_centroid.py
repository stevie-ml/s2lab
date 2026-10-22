"""
Surprise Centroid: Where in a poem does surprise concentrate?

For each poem, computes a 'surprise centroid' — the weighted-average
normalized position of positive-S2 tokens. A centroid near 0 = front-loaded
surprise; near 0.5 = balanced; near 1 = back-loaded.

Examines:
  1. Global distribution of centroids across corpus
  2. Centroid vs. poem length class
  3. Centroid vs. era
  4. Whether centroid predicts average S2

No PyTorch needed — reads from results/corpus_results.json.
"""

import json
import statistics
import math
from collections import defaultdict

RESULTS_DIR = "results"
FINDINGS_DIR = "findings"


def compute_centroid(tokens, artifact_threshold=0.9):
    """
    Weighted average normalized position of positive S2 tokens.
    Returns (centroid, n_positive, total_artifact_free) or None if insufficient data.
    """
    artifact_free = [t for t in tokens if t.get("p_newline", 0) < artifact_threshold]
    if len(artifact_free) < 10:
        return None

    positive = [(i / (len(artifact_free) - 1), t["s2"])
                for i, t in enumerate(artifact_free) if t["s2"] > 0]

    if len(positive) < 3:
        return None

    total_weight = sum(s2 for _, s2 in positive)
    if total_weight == 0:
        return None

    centroid = sum(pos * s2 for pos, s2 in positive) / total_weight
    return centroid, len(positive), len(artifact_free)


def length_class(n_tokens):
    if n_tokens < 50:
        return "very_short (<50)"
    elif n_tokens < 120:
        return "short (50–119)"
    elif n_tokens < 250:
        return "medium (120–249)"
    elif n_tokens < 500:
        return "long (250–499)"
    else:
        return "very_long (500+)"


def main():
    with open(f"{RESULTS_DIR}/corpus_results.json") as f:
        data = json.load(f)

    records = []
    for poem in data:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue

        tokens = poem["tokens"]
        result = compute_centroid(tokens)
        if result is None:
            continue

        centroid, n_pos, n_clean = result
        avg_s2 = statistics.mean(t["s2"] for t in tokens
                                  if t.get("p_newline", 0) < 0.9)

        records.append({
            "title": meta.get("title", "?"),
            "author": meta.get("author", "?"),
            "era": meta.get("era", "unknown"),
            "centroid": centroid,
            "n_clean": n_clean,
            "length_class": length_class(n_clean),
            "avg_s2": avg_s2,
            "n_pos": n_pos,
            "frac_pos": n_pos / n_clean,
        })

    records.sort(key=lambda r: r["centroid"])

    # --- Global stats ---
    all_centroids = [r["centroid"] for r in records]
    mean_c = statistics.mean(all_centroids)
    median_c = statistics.median(all_centroids)
    stdev_c = statistics.stdev(all_centroids)

    # --- By length class ---
    by_len = defaultdict(list)
    for r in records:
        by_len[r["length_class"]].append(r["centroid"])

    # --- By era (min 3 poems) ---
    by_era = defaultdict(list)
    for r in records:
        by_era[r["era"]].append(r)
    era_stats = {}
    for era, recs in by_era.items():
        if len(recs) < 3:
            continue
        cents = [r["centroid"] for r in recs]
        era_stats[era] = {
            "n": len(recs),
            "mean": statistics.mean(cents),
            "stdev": statistics.stdev(cents) if len(cents) > 1 else 0,
            "front": sum(1 for c in cents if c < 0.40) / len(cents),
            "back": sum(1 for c in cents if c > 0.60) / len(cents),
        }

    # --- Centroid–S2 correlation ---
    pairs = [(r["centroid"], r["avg_s2"]) for r in records]
    mean_x = statistics.mean(p[0] for p in pairs)
    mean_y = statistics.mean(p[1] for p in pairs)
    cov = statistics.mean((p[0] - mean_x) * (p[1] - mean_y) for p in pairs)
    sx = statistics.stdev(p[0] for p in pairs)
    sy = statistics.stdev(p[1] for p in pairs)
    corr = cov / (sx * sy) if sx * sy > 0 else 0

    # Front-loaded (centroid < 0.40) vs back-loaded (> 0.60)
    front = [r for r in records if r["centroid"] < 0.40]
    back = [r for r in records if r["centroid"] > 0.60]

    results = {
        "n": len(records),
        "mean_centroid": mean_c,
        "median_centroid": median_c,
        "stdev_centroid": stdev_c,
        "corr_centroid_s2": corr,
        "front_loaded": [(r["title"], r["author"], round(r["centroid"], 3)) for r in front[:10]],
        "back_loaded": [(r["title"], r["author"], round(r["centroid"], 3)) for r in back[-10:][::-1]],
        "by_length_class": {k: {
            "n": len(v),
            "mean": round(statistics.mean(v), 4),
            "stdev": round(statistics.stdev(v) if len(v) > 1 else 0, 4),
        } for k, v in sorted(by_len.items())},
        "by_era": {era: {k: round(v, 4) if isinstance(v, float) else v
                         for k, v in stats.items()}
                   for era, stats in sorted(era_stats.items(),
                                            key=lambda x: x[1]["mean"])},
    }

    out_path = f"{RESULTS_DIR}/surprise_centroid.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Analyzed {len(records)} poems")
    print(f"Mean centroid: {mean_c:.3f} (stdev {stdev_c:.3f})")
    print(f"Median centroid: {median_c:.3f}")
    print(f"Corr(centroid, avg_S2): {corr:.3f}")
    print(f"Front-loaded (<0.4): {len(front)}, Back-loaded (>0.6): {len(back)}")
    print()
    print("By length class:")
    for k, v in sorted(by_len.items()):
        m = statistics.mean(v)
        print(f"  {k}: n={len(v)}, mean centroid={m:.3f}")
    print()
    print("Top front-loaded poems:")
    for t, a, c in results["front_loaded"][:5]:
        print(f"  {c:.3f}  {t} ({a})")
    print("Top back-loaded poems:")
    for t, a, c in results["back_loaded"][:5]:
        print(f"  {c:.3f}  {t} ({a})")
    print(f"\nSaved to {out_path}")


if __name__ == "__main__":
    main()
