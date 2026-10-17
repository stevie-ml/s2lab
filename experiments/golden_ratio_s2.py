"""
Golden Ratio and Peak S2 Position

Hypothesis: In poems, the token of maximum S2 (peak surprise) tends to fall
near the golden ratio position φ ≈ 0.618 through the poem — the same
"divine proportion" observed in visual art, music, and narrative structure.

Method:
1. Load corpus_results.json
2. For each poem (≥20 clean tokens), find the position of max S2 token
   (excluding stanza-break artifacts: p_newline < 0.9)
3. Compute the relative position (0.0 = start, 1.0 = end)
4. Compute the distribution of peak S2 positions across all poems
5. Compare to φ ≈ 0.618 and to null expectation (uniform 0–1)
6. Test whether any secondary peaks exist at 1−φ ≈ 0.382 or φ² ≈ 0.382

Secondary question: Does the SECOND-highest S2 peak tend to fall at the
complementary position (1 - peak_1_position)?
"""

import json
import math
import statistics
from collections import defaultdict

GOLDEN_RATIO = (1 + math.sqrt(5)) / 2 - 1  # φ − 1 ≈ 0.618
GOLDEN_COMPLEMENT = 1 - GOLDEN_RATIO         # 1 − φ ≈ 0.382

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def clean_tokens(poem):
    """Remove stanza-break artifacts (p_newline ≥ 0.9)."""
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < 0.9]

def get_peak_positions(tokens, n_peaks=3):
    """
    Return relative positions (0..1) of the top-N S2 peaks.
    Returns None if not enough tokens.
    """
    if len(tokens) < 20:
        return None
    n = len(tokens)
    # Sort by S2 descending, get positions
    sorted_by_s2 = sorted(enumerate(tokens), key=lambda x: x[1]["s2"], reverse=True)
    peaks = []
    for rank, (idx, tok) in enumerate(sorted_by_s2[:n_peaks]):
        rel_pos = idx / (n - 1) if n > 1 else 0.5
        peaks.append({
            "rank": rank + 1,
            "position": idx,
            "rel_pos": rel_pos,
            "s2": tok["s2"],
            "token": tok["token"],
        })
    return peaks

def histogram(values, bins=10):
    """Simple histogram for relative positions."""
    counts = [0] * bins
    for v in values:
        b = min(int(v * bins), bins - 1)
        counts[b] += 1
    return counts

def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")

def stdev(xs):
    if len(xs) < 2:
        return float("nan")
    return statistics.stdev(xs)

def t_stat_vs_null(values, null_mean=0.5):
    """One-sample t-statistic vs. a null mean."""
    n = len(values)
    if n < 2:
        return float("nan")
    m = mean(values)
    s = stdev(values)
    return (m - null_mean) / (s / math.sqrt(n))

def golden_proximity(pos, phi=GOLDEN_RATIO, complement=GOLDEN_COMPLEMENT, window=0.1):
    """Is this position within `window` of φ or 1−φ?"""
    return abs(pos - phi) < window or abs(pos - complement) < window

def main():
    data = load_corpus()

    era_peaks = defaultdict(list)
    all_peak1 = []
    all_peak2 = []
    all_peak3 = []
    near_golden = 0
    total_poems = 0

    per_poem_results = []

    for poem in data:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue
        tokens = clean_tokens(poem)
        peaks = get_peak_positions(tokens, n_peaks=3)
        if peaks is None:
            continue

        era = meta.get("era", "unknown")
        p1 = peaks[0]["rel_pos"]

        era_peaks[era].append(p1)
        all_peak1.append(p1)

        if len(peaks) >= 2:
            all_peak2.append(peaks[1]["rel_pos"])
        if len(peaks) >= 3:
            all_peak3.append(peaks[2]["rel_pos"])

        if golden_proximity(p1):
            near_golden += 1
        total_poems += 1

        per_poem_results.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": era,
            "n_tokens": len(tokens),
            "peak1_pos": round(p1, 3),
            "peak1_s2": round(peaks[0]["s2"], 2),
            "peak1_token": peaks[0]["token"],
            "peak2_pos": round(peaks[1]["rel_pos"], 3) if len(peaks) >= 2 else None,
            "peak3_pos": round(peaks[2]["rel_pos"], 3) if len(peaks) >= 3 else None,
            "near_golden": golden_proximity(p1),
        })

    # ── Summary statistics ─────────────────────────────────────────────────────

    print(f"\n=== Golden Ratio Peak Position Analysis ===")
    print(f"Total poems analyzed: {total_poems}")
    print(f"\nφ (golden ratio)     ≈ {GOLDEN_RATIO:.3f}")
    print(f"1−φ (complement)     ≈ {GOLDEN_COMPLEMENT:.3f}")

    m1 = mean(all_peak1)
    s1 = stdev(all_peak1)
    t1 = t_stat_vs_null(all_peak1, null_mean=0.5)

    print(f"\n--- Peak #1 (highest S2 token) ---")
    print(f"  Mean position:  {m1:.3f}  (φ={GOLDEN_RATIO:.3f}, null=0.500)")
    print(f"  Std deviation:  {s1:.3f}")
    print(f"  t vs. null:     {t1:.2f}")
    print(f"  Distance from φ: {abs(m1 - GOLDEN_RATIO):.3f}")
    print(f"  Within ±0.1 of φ or 1−φ: {near_golden}/{total_poems} = {near_golden/total_poems*100:.1f}%")
    print(f"  Expected by chance (uniform):  ~20%")

    # ── Histogram ─────────────────────────────────────────────────────────────
    hist = histogram(all_peak1, bins=10)
    print(f"\n--- Position distribution (peak #1) ---")
    bin_labels = ["0.0-0.1","0.1-0.2","0.2-0.3","0.3-0.4","0.4-0.5",
                  "0.5-0.6","0.6-0.7","0.7-0.8","0.8-0.9","0.9-1.0"]
    max_count = max(hist)
    for label, count in zip(bin_labels, hist):
        bar = "█" * int(count / max_count * 30)
        is_phi = "← φ≈0.618" if "0.6-0.7" in label else ("← 1-φ≈0.382" if "0.3-0.4" in label else "")
        print(f"  {label}: {bar:30s} {count:3d}  {is_phi}")

    # ── Second and third peaks ─────────────────────────────────────────────────
    if all_peak2:
        m2 = mean(all_peak2)
        t2 = t_stat_vs_null(all_peak2, null_mean=0.5)
        print(f"\n--- Peak #2 (second-highest S2 token) ---")
        print(f"  Mean position:  {m2:.3f}  (distance from 1-φ: {abs(m2-GOLDEN_COMPLEMENT):.3f})")
        print(f"  t vs. null:     {t2:.2f}")

    if all_peak3:
        m3 = mean(all_peak3)
        t3 = t_stat_vs_null(all_peak3, null_mean=0.5)
        print(f"\n--- Peak #3 (third-highest S2 token) ---")
        print(f"  Mean position:  {m3:.3f}")
        print(f"  t vs. null:     {t3:.2f}")

    # ── Complementarity: do peak 1 and peak 2 mirror each other? ─────────────
    if len(per_poem_results) > 0:
        mirrored = [abs(r["peak1_pos"] + r["peak2_pos"] - 1.0)
                    for r in per_poem_results if r["peak2_pos"] is not None]
        mean_mirror = mean(mirrored)
        print(f"\n--- Peak 1 + Peak 2 complementarity ---")
        print(f"  Mean |peak1_pos + peak2_pos − 1| = {mean_mirror:.3f}")
        print(f"  (0 = perfectly complementary / mirrored; 0.33 = random)")

    # ── Era breakdown ─────────────────────────────────────────────────────────
    print(f"\n--- Era breakdown (mean peak1 position, n≥3) ---")
    era_rows = []
    for era, positions in sorted(era_peaks.items(), key=lambda x: mean(x[1])):
        if len(positions) < 3:
            continue
        m = mean(positions)
        s = stdev(positions)
        era_rows.append((era, len(positions), m, s))

    for era, n, m, s in sorted(era_rows, key=lambda x: x[2]):
        near_phi = "← near 1-φ" if abs(m - GOLDEN_COMPLEMENT) < 0.05 else (
                   "← near φ" if abs(m - GOLDEN_RATIO) < 0.05 else "")
        print(f"  {era:25s} n={n:3d}  mean={m:.3f}  std={s:.3f}  {near_phi}")

    # ── Extreme examples ──────────────────────────────────────────────────────
    near_phi_poems = [(r, abs(r["peak1_pos"] - GOLDEN_RATIO))
                      for r in per_poem_results]
    near_phi_poems.sort(key=lambda x: x[1])

    print(f"\n--- Top 10 poems closest to φ peak position ---")
    for r, dist in near_phi_poems[:10]:
        print(f"  {r['title'][:40]:40s} | {r['author'][:20]:20s} | pos={r['peak1_pos']:.3f} | Δφ={dist:.3f} | token='{r['peak1_token'].strip()}'")

    far_phi_poems = sorted(near_phi_poems, key=lambda x: -x[1])
    print(f"\n--- Top 5 poems FARTHEST from φ peak position ---")
    for r, dist in far_phi_poems[:5]:
        print(f"  {r['title'][:40]:40s} | pos={r['peak1_pos']:.3f} | Δφ={dist:.3f}")

    return {
        "total_poems": total_poems,
        "peak1_mean": m1,
        "peak1_std": s1,
        "peak1_t_vs_null": t1,
        "near_golden_pct": near_golden / total_poems * 100,
        "histogram": dict(zip(bin_labels, hist)),
        "peak2_mean": mean(all_peak2) if all_peak2 else None,
        "peak3_mean": mean(all_peak3) if all_peak3 else None,
        "mean_complementarity": mean(mirrored) if mirrored else None,
    }

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    results = main()

    import json
    with open("results/golden_ratio_s2.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/golden_ratio_s2.json")
