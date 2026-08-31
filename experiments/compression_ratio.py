"""
Compression Ratio vs S₂ Analysis

Hypothesis: gzip compression ratio of poem text is a distinct but related
information-theoretic signal from GPT-2-derived S₂.

gzip compressibility ≈ string-level redundancy (character n-gram repetition).
S₂ = token surprisal − context entropy (model-level semantic surprise).

We expect:
  - High-S₂ poems: unpredictable at the *token/semantic* level
  - Low compression ratio: unpredictable at the *character/surface* level
  - These can dissociate: anaphoric poems may be highly compressible
    (surface repetition) yet yield high S₂ at repeated structures
    (model prediction collapses, but choice persists as surprising)
"""

import gzip
import json
import statistics
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"


def compression_ratio(text: str) -> float:
    """Returns compressed/uncompressed byte ratio. Lower = more compressible."""
    raw = text.encode("utf-8")
    compressed = gzip.compress(raw, compresslevel=9)
    return len(compressed) / len(raw)


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs)
    sy = statistics.stdev(ys)
    if sx == 0 or sy == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / ((n - 1) * sx * sy)


def main():
    data = load_data()

    rows = []
    for entry in data:
        meta = entry["metadata"]
        summ = entry["summary"]
        # Reconstruct text from tokens for compression
        tokens = entry.get("tokens", [])
        text = "".join(t["token"] for t in tokens)
        if not text.strip():
            continue

        cr = compression_ratio(text)
        rows.append({
            "title": meta["title"],
            "author": meta["author"],
            "year": meta.get("year"),
            "era": meta.get("era", "unknown"),
            "is_control": meta.get("era") == "control",
            "n_tokens": meta["n_tokens"],
            "avg_s2": summ["avg_s2"],
            "avg_surprisal": summ["avg_surprisal"],
            "avg_entropy": summ["avg_entropy"],
            "pos_s2_ratio": summ["pos_s2_ratio"],
            "compression_ratio": cr,
            "text_length": len(text),
        })

    # ── Global stats ────────────────────────────────────────────────────
    poetry = [r for r in rows if not r["is_control"]]
    prose  = [r for r in rows if r["is_control"]]

    print("=" * 70)
    print("COMPRESSION RATIO VS S₂ ANALYSIS")
    print("=" * 70)

    print(f"\nCorpus: {len(rows)} texts ({len(poetry)} poetry, {len(prose)} control prose)")
    print()

    # ── 1. Basic compression stats by group ─────────────────────────────
    print("## 1. Compression Ratio by Group")
    print()
    print(f"{'Group':<12} {'n':>4} {'Mean CR':>10} {'Mean S₂':>10} {'Corr(CR,S₂)':>14}")
    print("-" * 54)

    for label, group in [("Poetry", poetry), ("Prose", prose)]:
        crs = [r["compression_ratio"] for r in group]
        s2s = [r["avg_s2"] for r in group]
        r = pearson_r(crs, s2s)
        print(f"{label:<12} {len(group):>4} {statistics.mean(crs):>10.4f} "
              f"{statistics.mean(s2s):>10.4f} {r:>14.4f}")

    print()

    # ── 2. Correlation table (full corpus) ──────────────────────────────
    all_crs = [r["compression_ratio"] for r in rows]
    all_s2  = [r["avg_s2"] for r in rows]
    all_surp = [r["avg_surprisal"] for r in rows]
    all_ent  = [r["avg_entropy"] for r in rows]
    all_pos  = [r["pos_s2_ratio"] for r in rows]

    print("## 2. Pearson Correlations with Compression Ratio (all texts)")
    print()
    print(f"  {'Variable':<20} {'r':>8}")
    print(f"  {'-'*30}")
    for label, vals in [
        ("avg_s2", all_s2),
        ("avg_surprisal", all_surp),
        ("avg_entropy", all_ent),
        ("pos_s2_ratio", all_pos),
    ]:
        r = pearson_r(all_crs, vals)
        print(f"  {label:<20} {r:>8.4f}")
    print()

    # ── 3. Per-era compression ratio ────────────────────────────────────
    print("## 3. Compression Ratio and S₂ by Era (poetry only)")
    print()
    from collections import defaultdict
    era_buckets = defaultdict(list)
    for r in poetry:
        era_buckets[r["era"]].append(r)

    print(f"{'Era':<24} {'n':>4} {'Mean CR':>10} {'Mean S₂':>10} {'CR rank'}")
    print("-" * 60)

    era_stats = []
    for era, group in era_buckets.items():
        crs = [r["compression_ratio"] for r in group]
        s2s = [r["avg_s2"] for r in group]
        era_stats.append((era, len(group), statistics.mean(crs), statistics.mean(s2s)))

    era_stats.sort(key=lambda x: x[2])  # sort by compression ratio ascending
    for rank, (era, n, cr, s2) in enumerate(era_stats, 1):
        print(f"{era:<24} {n:>4} {cr:>10.4f} {s2:>10.4f} {rank}")
    print()

    # ── 4. Top 10 most & least compressible poems ────────────────────────
    print("## 4. Most Compressible (lowest CR) — surface repetition")
    print()
    sorted_by_cr = sorted(poetry, key=lambda r: r["compression_ratio"])
    for r in sorted_by_cr[:10]:
        print(f"  CR={r['compression_ratio']:.4f}  S₂={r['avg_s2']:+.3f}  "
              f"{r['author']}, \"{r['title']}\" ({r['year']})")
    print()

    print("## 5. Least Compressible (highest CR) — surface unpredictability")
    print()
    for r in sorted_by_cr[-10:]:
        print(f"  CR={r['compression_ratio']:.4f}  S₂={r['avg_s2']:+.3f}  "
              f"{r['author']}, \"{r['title']}\" ({r['year']})")
    print()

    # ── 5. Dissociations: high-CR + low-S₂ and low-CR + high-S₂ ────────
    print("## 6. Interesting Dissociations")
    print()
    median_cr = statistics.median(all_crs)
    median_s2 = statistics.median(all_s2)

    q = {"hi_cr_lo_s2": [], "lo_cr_hi_s2": [], "hi_cr_hi_s2": [], "lo_cr_lo_s2": []}
    for r in rows:
        cr_hi = r["compression_ratio"] > median_cr
        s2_hi = r["avg_s2"] > median_s2
        if cr_hi and not s2_hi:
            q["hi_cr_lo_s2"].append(r)
        elif not cr_hi and s2_hi:
            q["lo_cr_hi_s2"].append(r)
        elif cr_hi and s2_hi:
            q["hi_cr_hi_s2"].append(r)
        else:
            q["lo_cr_lo_s2"].append(r)

    labels = {
        "hi_cr_hi_s2": "Hard at both levels (high CR, high S₂)",
        "lo_cr_lo_s2": "Easy at both levels (low CR, low S₂)",
        "hi_cr_lo_s2": "Surface-hard, semantically-easy (high CR, low S₂)",
        "lo_cr_hi_s2": "Surface-easy, semantically-hard (low CR, high S₂)",
    }
    for key, label in labels.items():
        group = q[key]
        if group:
            print(f"  {label} — n={len(group)}")
            for r in sorted(group, key=lambda x: abs(x["compression_ratio"] - x["avg_s2"]))[:3]:
                print(f"    CR={r['compression_ratio']:.4f} S₂={r['avg_s2']:+.3f}  "
                      f"\"{r['title'][:50]}\" [{r['era']}]")
        print()

    # ── 6. Return structured results ─────────────────────────────────────
    return {
        "rows": rows,
        "poetry_mean_cr": statistics.mean(r["compression_ratio"] for r in poetry),
        "prose_mean_cr": statistics.mean(r["compression_ratio"] for r in prose),
        "r_cr_s2_all": pearson_r(all_crs, all_s2),
        "r_cr_s2_poetry": pearson_r(
            [r["compression_ratio"] for r in poetry],
            [r["avg_s2"] for r in poetry]
        ),
        "era_stats": era_stats,
        "quadrants": {k: len(v) for k, v in q.items()},
    }


if __name__ == "__main__":
    results = main()
