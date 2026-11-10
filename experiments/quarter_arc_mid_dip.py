"""
Quarter-Arc: The Mid-Poem Trough and Arc-as-Fingerprint

The within_poem_type_arc.py experiment found that poems divide into thirds with
Type I% decreasing from first to last — the "deviate early, resolve late" pattern
dominated 76% of poems. The last finding suggested that dividing into QUARTERS
would reveal whether there is a "mid-poem trough" where Type I reaches its absolute
minimum in the 2nd or 3rd quarter (not at the end).

Hypothesis A (Mid-Poem Trough): Type I% follows a U-shape or monotonic decline,
with its minimum in the 2nd or 3rd quarter, not the 4th.

Hypothesis B (Arc Fingerprint): Each poet's consistent quarter arc — their typical
pattern of deviation across a poem's span — constitutes a recognizable "fingerprint"
that is distinct across poets.

Method:
  - Divide each poem into 4 equal quarters by token position (artifact-free only)
  - Compute Type I%, Type III%, entropy for each quarter
  - Aggregate by corpus, era, and poet
  - Find the "dip position" for each poem and check where it most often falls
  - Compute per-poet arc consistency (σ of arc pattern across their poems)
"""

import json
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
RANK_THRESHOLD = 10
MIN_TOKENS = 40  # need enough tokens for 4 quarters of at least 10 each


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    top = alts[0]
    return top["token"] in ("\n", "\r\n", "\r") and top["prob"] >= 0.9


def classify_token(tok, entropy_median):
    if is_artifact(tok):
        return None
    h = tok["entropy"]
    rank = tok.get("rank", 9999)
    low_entropy = h < entropy_median
    expected = rank <= RANK_THRESHOLD
    if low_entropy and not expected:
        return "I"
    elif not low_entropy and not expected:
        return "II"
    elif low_entropy and expected:
        return "III"
    else:
        return "IV"


def type_stats(type_list):
    counts = defaultdict(int)
    for t in type_list:
        counts[t] += 1
    total = sum(counts.values())
    if total == 0:
        return None
    return {
        "n": total,
        "I":   round(counts["I"]   / total * 100, 1),
        "II":  round(counts["II"]  / total * 100, 1),
        "III": round(counts["III"] / total * 100, 1),
        "IV":  round(counts["IV"]  / total * 100, 1),
        "contrast": round((counts["I"] - counts["III"]) / total, 4),
    }


def run():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Compute corpus entropy median
    all_entropies = []
    for poem in data:
        for tok in poem["tokens"]:
            if not is_artifact(tok) and tok["entropy"] > 0:
                all_entropies.append(tok["entropy"])
    entropy_median = statistics.median(all_entropies)
    print(f"Corpus entropy median: {entropy_median:.3f} bits")
    print(f"Total poems in corpus: {len(data)}")

    # Classify tokens and split into 4 quarters
    poem_arcs = []
    skipped = 0
    for poem in data:
        meta = poem["metadata"]
        classified = []
        for tok in poem["tokens"]:
            qtype = classify_token(tok, entropy_median)
            if qtype is not None:
                classified.append(qtype)

        if len(classified) < MIN_TOKENS:
            skipped += 1
            continue

        n = len(classified)
        q1 = classified[:n // 4]
        q2 = classified[n // 4: n // 2]
        q3 = classified[n // 2: 3 * n // 4]
        q4 = classified[3 * n // 4:]

        s1 = type_stats(q1)
        s2 = type_stats(q2)
        s3 = type_stats(q3)
        s4 = type_stats(q4)

        if s1 and s2 and s3 and s4:
            I_values = [s1["I"], s2["I"], s3["I"], s4["I"]]
            # Position (1-indexed) where Type I is minimum
            min_pos = I_values.index(min(I_values)) + 1
            # Is there a U-shape? (min in q2 or q3)
            is_dip = min_pos in (2, 3)
            # Monotonic decline?
            is_mono_decline = I_values[0] >= I_values[1] >= I_values[2] >= I_values[3]

            poem_arcs.append({
                "title":  meta["title"],
                "author": meta.get("author", "Unknown"),
                "era":    meta.get("era", "unknown"),
                "year":   meta.get("year"),
                "n":      n,
                "q1": s1, "q2": s2, "q3": s3, "q4": s4,
                "I_values": I_values,
                "min_I_pos": min_pos,
                "is_dip": is_dip,
                "is_mono_decline": is_mono_decline,
                "delta_I_q1_q4": round(s4["I"] - s1["I"], 2),
                "delta_III_q1_q4": round(s4["III"] - s1["III"], 2),
            })

    print(f"Poems analyzed: {len(poem_arcs)}, skipped (< {MIN_TOKENS} tokens): {skipped}")

    # ── 1. Corpus-Level Quarter Arc ──────────────────────────────────────────
    print("\n=== CORPUS-LEVEL QUARTER ARC ===")
    for qkey, qlabel in [("q1","Q1 (0–25%)"), ("q2","Q2 (25–50%)"), ("q3","Q3 (50–75%)"), ("q4","Q4 (75–100%)")]:
        all_I   = [p[qkey]["I"]   for p in poem_arcs]
        all_III = [p[qkey]["III"] for p in poem_arcs]
        all_con = [p[qkey]["contrast"] for p in poem_arcs]
        print(f"  {qlabel}: Type I={statistics.mean(all_I):.1f}%  "
              f"Type III={statistics.mean(all_III):.1f}%  "
              f"contrast={statistics.mean(all_con):+.3f}")

    # ── 2. Where Does the Minimum Type I Fall? ───────────────────────────────
    print("\n=== WHERE IS TYPE I MINIMUM? (position of minimum Type I% across 4 quarters) ===")
    min_counts = defaultdict(int)
    for p in poem_arcs:
        min_counts[p["min_I_pos"]] += 1
    total = len(poem_arcs)
    for pos in [1, 2, 3, 4]:
        cnt = min_counts[pos]
        label = ["", "Q1 (opening)", "Q2 (early-mid)", "Q3 (late-mid)", "Q4 (closing)"][pos]
        print(f"  {label}: {cnt} poems ({cnt/total*100:.1f}%)")

    # Is Q2+Q3 dominant? (mid-poem dip)
    mid_dip_count = sum(1 for p in poem_arcs if p["is_dip"])
    mono_decline_count = sum(1 for p in poem_arcs if p["is_mono_decline"])
    print(f"\n  Mid-poem dip (min at Q2 or Q3): {mid_dip_count} poems ({mid_dip_count/total*100:.1f}%)")
    print(f"  Monotonic decline (Q1>Q2>Q3>Q4): {mono_decline_count} poems ({mono_decline_count/total*100:.1f}%)")
    print(f"  Min at Q4 (end is lowest): {min_counts[4]} poems ({min_counts[4]/total*100:.1f}%)")
    print(f"  Min at Q1 (start is lowest): {min_counts[1]} poems ({min_counts[1]/total*100:.1f}%)")

    # ── 3. Per-Era Quarter Arc ────────────────────────────────────────────────
    print("\n=== PER-ERA QUARTER ARC (avg Type I% by quarter, sorted by Q1 desc) ===")
    era_arcs = defaultdict(list)
    for p in poem_arcs:
        era_arcs[p["era"]].append(p)

    era_rows = []
    for era, poems in era_arcs.items():
        if len(poems) < 2:
            continue
        q1_I = statistics.mean(p["q1"]["I"] for p in poems)
        q2_I = statistics.mean(p["q2"]["I"] for p in poems)
        q3_I = statistics.mean(p["q3"]["I"] for p in poems)
        q4_I = statistics.mean(p["q4"]["I"] for p in poems)
        # Find where the minimum falls
        vals = [q1_I, q2_I, q3_I, q4_I]
        min_q = vals.index(min(vals)) + 1
        era_rows.append({
            "era": era, "n": len(poems),
            "q1_I": round(q1_I, 1), "q2_I": round(q2_I, 1),
            "q3_I": round(q3_I, 1), "q4_I": round(q4_I, 1),
            "delta": round(q4_I - q1_I, 1), "min_q": min_q,
        })

    era_rows.sort(key=lambda r: -r["q1_I"])
    print(f"{'Era':<22} {'N':>4}  {'Q1':>6}  {'Q2':>6}  {'Q3':>6}  {'Q4':>6}  {'Δ(Q4-Q1)':>9}  {'Min at':>7}")
    for r in era_rows:
        print(f"  {r['era']:<20} {r['n']:>4}  {r['q1_I']:>5.1f}%  {r['q2_I']:>5.1f}%  "
              f"{r['q3_I']:>5.1f}%  {r['q4_I']:>5.1f}%  {r['delta']:>+8.1f}  Q{r['min_q']:>1}")

    # ── 4. Per-Poet Arc Fingerprint ───────────────────────────────────────────
    print("\n=== PER-POET ARC FINGERPRINT (poets with ≥3 poems) ===")
    poet_arcs = defaultdict(list)
    for p in poem_arcs:
        poet_arcs[p["author"]].append(p)

    poet_rows = []
    for author, poems in poet_arcs.items():
        if len(poems) < 3:
            continue
        q1_I = statistics.mean(p["q1"]["I"] for p in poems)
        q2_I = statistics.mean(p["q2"]["I"] for p in poems)
        q3_I = statistics.mean(p["q3"]["I"] for p in poems)
        q4_I = statistics.mean(p["q4"]["I"] for p in poems)

        vals = [q1_I, q2_I, q3_I, q4_I]
        min_q = vals.index(min(vals)) + 1
        # Consistency: how much do individual poems agree with the arc pattern?
        # Measure: std dev of delta_I (q4-q1) across poems
        deltas = [p["delta_I_q1_q4"] for p in poems]
        delta_std = statistics.stdev(deltas) if len(deltas) > 1 else 0
        delta_mean = statistics.mean(deltas)

        poet_rows.append({
            "author": author, "n": len(poems),
            "q1_I": round(q1_I, 1), "q2_I": round(q2_I, 1),
            "q3_I": round(q3_I, 1), "q4_I": round(q4_I, 1),
            "delta_mean": round(delta_mean, 1), "delta_std": round(delta_std, 1),
            "min_q": min_q,
        })

    poet_rows.sort(key=lambda r: r["delta_mean"])  # most negative = strongest "deviate early"
    print(f"{'Author':<30} {'N':>3}  {'Q1':>5}  {'Q2':>5}  {'Q3':>5}  {'Q4':>5}  {'Δ mean':>7}  {'Δ σ':>5}  Min")
    for r in poet_rows:
        print(f"  {r['author']:<28} {r['n']:>3}  {r['q1_I']:>4.1f}%  {r['q2_I']:>4.1f}%  "
              f"{r['q3_I']:>4.1f}%  {r['q4_I']:>4.1f}%  {r['delta_mean']:>+6.1f}  "
              f"{r['delta_std']:>4.1f}  Q{r['min_q']}")

    # ── 5. Most Consistent "Deviate Early" Poets (low σ, negative Δ) ─────────
    consistent_early = [r for r in poet_rows if r["delta_mean"] < -3 and r["delta_std"] < 8]
    if consistent_early:
        print(f"\n  Most consistent 'deviate early' poets (Δ < -3, σ < 8):")
        for r in sorted(consistent_early, key=lambda x: x["delta_mean"])[:8]:
            print(f"    {r['author']:<30} Δ={r['delta_mean']:>+5.1f}  σ={r['delta_std']:>4.1f}  n={r['n']}")

    # ── 6. Individual poem arc extremes ──────────────────────────────────────
    print("\n=== TOP POEMS: LARGEST TYPE I DROP (Q1 → Q4) ===")
    for p in sorted(poem_arcs, key=lambda x: x["delta_I_q1_q4"])[:10]:
        print(f"  {p['delta_I_q1_q4']:>+6.1f}  "
              f"[{p['I_values'][0]:.1f}→{p['I_values'][1]:.1f}→{p['I_values'][2]:.1f}→{p['I_values'][3]:.1f}]  "
              f"  {p['author']}: '{p['title']}'")

    print("\n=== TOP POEMS: LARGEST TYPE I RISE (Q1 → Q4, volta pattern) ===")
    for p in sorted(poem_arcs, key=lambda x: -x["delta_I_q1_q4"])[:10]:
        print(f"  {p['delta_I_q1_q4']:>+6.1f}  "
              f"[{p['I_values'][0]:.1f}→{p['I_values'][1]:.1f}→{p['I_values'][2]:.1f}→{p['I_values'][3]:.1f}]  "
              f"  {p['author']}: '{p['title']}'")

    # ── 7. Mid-poem dip examples ──────────────────────────────────────────────
    print("\n=== EXAMPLES: MID-POEM DIP (Type I minimum at Q2 or Q3) ===")
    dip_poems = [p for p in poem_arcs if p["is_dip"]]
    # Sort by how deep the dip goes (how much lower the min is vs Q1 and Q4)
    for p in sorted(dip_poems, key=lambda x: -abs(min(x["I_values"]) - x["I_values"][0]))[:10]:
        print(f"  min@Q{p['min_I_pos']}  [{p['I_values'][0]:.1f}→{p['I_values'][1]:.1f}→"
              f"{p['I_values'][2]:.1f}→{p['I_values'][3]:.1f}]  "
              f"{p['author']}: '{p['title']}'  ({p['era']})")


if __name__ == "__main__":
    run()
