"""
Forgetting Curve for Lexical Habituation: Does Distance Between Occurrences
Predict S₂ Recovery?

The second_occurrence_dip.md established a massive habituation effect: words
lose ~2.31 S₂ units between their first and second appearance. But that study
did not ask: does the token *distance* between occurrences moderate how much
S₂ drops? Longer gaps might allow GPT-2's local context to "forget" the word,
producing partial S₂ recovery.

This experiment tests whether there is a forgetting curve in lexical surprise.
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_PATH = "results/corpus_results.json"


def normalize(token: str) -> str:
    return token.strip().lower().strip(".,!?;:\"'()-—")


def run_experiment():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    poems = [d for d in data if d["metadata"].get("language", "en") == "en"]
    print(f"Analyzing {len(poems)} English poems")

    # For each pair of consecutive occurrences of the same word, record:
    # (s2_first, s2_second, delta_s2, token_distance, occ_number, era)
    pair_records = []

    # For multi-occurrence words: track full trajectory with distances
    multi_occ_records = []

    # Distance buckets for aggregation
    BUCKETS = [(0, 10), (11, 25), (26, 50), (51, 100), (101, 300), (301, 9999)]

    for poem in poems:
        tokens = poem["tokens"]
        era = poem["metadata"].get("era", "unknown")
        title = poem["metadata"].get("title", "?")

        word_positions = defaultdict(list)  # norm_word -> [(position, s2, p_newline)]

        for tok in tokens:
            norm = normalize(tok["token"])
            if len(norm) < 3:  # skip short tokens / punctuation
                continue
            if not re.search(r"[a-zA-Z]", norm):  # skip non-alpha
                continue
            word_positions[norm].append((tok["position"], tok["s2"], tok.get("p_newline", 0.0)))

        for word, occurrences in word_positions.items():
            if len(occurrences) < 2:
                continue

            # Record consecutive-pair metrics
            for i in range(1, len(occurrences)):
                pos_prev, s2_prev, nl_prev = occurrences[i - 1]
                pos_curr, s2_curr, nl_curr = occurrences[i]
                dist = pos_curr - pos_prev  # token distance between occurrences
                delta = s2_curr - s2_prev
                pair_records.append({
                    "word": word,
                    "title": title,
                    "era": era,
                    "occ_number": i + 1,  # 2nd, 3rd, etc.
                    "s2_prev": s2_prev,
                    "s2_curr": s2_curr,
                    "delta": delta,
                    "distance": dist,
                    "line_start_prev": nl_prev >= 0.5,
                    "line_start_curr": nl_curr >= 0.5,
                })

            # Track full trajectory for words appearing 3+ times
            if len(occurrences) >= 3:
                traj = {
                    "word": word,
                    "title": title,
                    "era": era,
                    "s2_sequence": [s2 for _, s2, _ in occurrences],
                    "distances": [occurrences[i+1][0] - occurrences[i][0]
                                  for i in range(len(occurrences) - 1)],
                }
                multi_occ_records.append(traj)

    print(f"Total consecutive-pair records: {len(pair_records)}")
    print(f"Multi-occurrence trajectories (3+): {len(multi_occ_records)}")

    # ── ANALYSIS 1: Forgetting Curve by Distance Bucket ──────────────────────
    print("\n=== Forgetting Curve by Token Distance ===")
    bucket_data = defaultdict(list)
    for rec in pair_records:
        d = rec["distance"]
        for lo, hi in BUCKETS:
            if lo <= d <= hi:
                bucket_data[(lo, hi)].append(rec["delta"])
                break

    print(f"\n{'Distance':>12} | {'N':>5} | {'Mean Δ':>8} | {'Median Δ':>9} | {'% Rise':>7} | {'% Drop':>7}")
    print("-" * 65)
    forgetting_data = []
    for lo, hi in BUCKETS:
        deltas = bucket_data[(lo, hi)]
        if not deltas:
            continue
        mean_d = statistics.mean(deltas)
        med_d = statistics.median(deltas)
        pct_rise = sum(1 for d in deltas if d > 0) / len(deltas) * 100
        pct_drop = sum(1 for d in deltas if d < 0) / len(deltas) * 100
        label = f"{lo}-{hi}" if hi < 9999 else f"{lo}+"
        print(f"{label:>12} | {len(deltas):>5} | {mean_d:>8.3f} | {med_d:>9.3f} | {pct_rise:>6.1f}% | {pct_drop:>6.1f}%")
        forgetting_data.append({
            "distance_range": label,
            "lo": lo,
            "hi": hi if hi < 9999 else None,
            "n": len(deltas),
            "mean_delta": round(mean_d, 4),
            "median_delta": round(med_d, 4),
            "pct_rise": round(pct_rise, 2),
            "pct_drop": round(pct_drop, 2),
        })

    # ── ANALYSIS 2: Second-only occurrences by distance ──────────────────────
    print("\n=== Second Occurrences Only (occ_number=2) by Distance ===")
    second_only = [r for r in pair_records if r["occ_number"] == 2]
    bucket_data2 = defaultdict(list)
    for rec in second_only:
        d = rec["distance"]
        for lo, hi in BUCKETS:
            if lo <= d <= hi:
                bucket_data2[(lo, hi)].append(rec["delta"])
                break

    print(f"\n{'Distance':>12} | {'N':>5} | {'Mean Δ':>8} | {'Median Δ':>9} | {'% Rise':>7}")
    print("-" * 55)
    second_occ_data = []
    for lo, hi in BUCKETS:
        deltas = bucket_data2[(lo, hi)]
        if not deltas:
            continue
        mean_d = statistics.mean(deltas)
        med_d = statistics.median(deltas)
        pct_rise = sum(1 for d in deltas if d > 0) / len(deltas) * 100
        label = f"{lo}-{hi}" if hi < 9999 else f"{lo}+"
        print(f"{label:>12} | {len(deltas):>5} | {mean_d:>8.3f} | {med_d:>9.3f} | {pct_rise:>6.1f}%")
        second_occ_data.append({
            "distance_range": label,
            "lo": lo,
            "hi": hi if hi < 9999 else None,
            "n": len(deltas),
            "mean_delta": round(mean_d, 4),
            "median_delta": round(med_d, 4),
            "pct_rise": round(pct_rise, 2),
        })

    # ── ANALYSIS 3: N-th occurrence curve (regardless of distance) ───────────
    print("\n=== Mean S₂ by Occurrence Number (regardless of distance) ===")
    occ_s2 = defaultdict(list)
    for rec in pair_records:
        occ_s2[rec["occ_number"]].append(rec["s2_curr"])
    # Also first occurrences: get them from pair_records where occ_number==2
    first_s2 = [r["s2_prev"] for r in pair_records if r["occ_number"] == 2]
    occ_s2[1] = first_s2

    print(f"\n{'Occ #':>6} | {'N':>5} | {'Mean S₂':>8} | {'Median S₂':>10} | {'% +S₂':>7}")
    print("-" * 50)
    occ_curve_data = []
    for n in sorted(occ_s2.keys()):
        vals = occ_s2[n]
        if len(vals) < 5:
            continue
        mean_s2 = statistics.mean(vals)
        med_s2 = statistics.median(vals)
        pct_pos = sum(1 for v in vals if v > 0) / len(vals) * 100
        print(f"{n:>6} | {len(vals):>5} | {mean_s2:>8.3f} | {med_s2:>10.3f} | {pct_pos:>6.1f}%")
        occ_curve_data.append({
            "occurrence_number": n,
            "n": len(vals),
            "mean_s2": round(mean_s2, 4),
            "median_s2": round(med_s2, 4),
            "pct_positive": round(pct_pos, 2),
        })

    # ── ANALYSIS 4: Extreme recovery cases (high delta, large distance) ───────
    print("\n=== Top 10 Largest Recoveries (high Δ, large distance) ===")
    recoveries = sorted(pair_records, key=lambda r: r["delta"], reverse=True)[:15]
    for r in recoveries[:10]:
        print(f"  '{r['word']}' ({r['title']}) | occ {r['occ_number']} | "
              f"dist={r['distance']} | S₂: {r['s2_prev']:.2f} → {r['s2_curr']:.2f} (Δ={r['delta']:+.2f})")

    # ── ANALYSIS 5: Multi-occurrence trajectories with oscillation ────────────
    print("\n=== Multi-Occurrence Words: Do Distances Predict Recovery? ===")
    # For 3+ occurrence words, test: does the distance predict S2 at next occurrence?
    dist_s2_pairs = []  # (distance, s2_next, s2_base) for all consecutive pairs in 3+ occ words
    for traj in multi_occ_records:
        s2_seq = traj["s2_sequence"]
        dists = traj["distances"]
        for i, (dist, s2_next) in enumerate(zip(dists, s2_seq[1:])):
            dist_s2_pairs.append((dist, s2_next, s2_seq[i]))

    if dist_s2_pairs:
        # Correlation between distance and delta (s2_next - s2_base)
        deltas_all = [s2_next - s2_base for _, s2_next, s2_base in dist_s2_pairs]
        dists_all = [dist for dist, _, _ in dist_s2_pairs]

        # Pearson correlation manually
        n_pts = len(deltas_all)
        mean_x = sum(dists_all) / n_pts
        mean_y = sum(deltas_all) / n_pts
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(dists_all, deltas_all)) / n_pts
        std_x = (sum((x - mean_x) ** 2 for x in dists_all) / n_pts) ** 0.5
        std_y = (sum((y - mean_y) ** 2 for y in deltas_all) / n_pts) ** 0.5
        if std_x > 0 and std_y > 0:
            corr = cov / (std_x * std_y)
            print(f"\nCorrelation (distance vs Δ S₂): r = {corr:.4f} (n={n_pts})")
            print("(Positive r → larger gap → smaller drop / more recovery)")
        else:
            corr = None
            print("Cannot compute correlation (zero variance)")
    else:
        corr = None

    # ── SAVE RESULTS ──────────────────────────────────────────────────────────
    results = {
        "forgetting_curve_all_occ": forgetting_data,
        "forgetting_curve_second_only": second_occ_data,
        "occurrence_number_curve": occ_curve_data,
        "distance_delta_correlation": corr,
        "total_pair_records": len(pair_records),
        "multi_occ_trajectories": len(multi_occ_records),
        "top_recoveries": [
            {
                "word": r["word"],
                "title": r["title"],
                "era": r["era"],
                "occ_number": r["occ_number"],
                "distance": r["distance"],
                "s2_prev": round(r["s2_prev"], 3),
                "s2_curr": round(r["s2_curr"], 3),
                "delta": round(r["delta"], 3),
            }
            for r in sorted(pair_records, key=lambda r: r["delta"], reverse=True)[:20]
        ],
        "top_drops": [
            {
                "word": r["word"],
                "title": r["title"],
                "era": r["era"],
                "occ_number": r["occ_number"],
                "distance": r["distance"],
                "s2_prev": round(r["s2_prev"], 3),
                "s2_curr": round(r["s2_curr"], 3),
                "delta": round(r["delta"], 3),
            }
            for r in sorted(pair_records, key=lambda r: r["delta"])[:20]
        ],
    }

    out_path = "results/forgetting_curve_s2.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved results to {out_path}")
    return results


if __name__ == "__main__":
    run_experiment()
