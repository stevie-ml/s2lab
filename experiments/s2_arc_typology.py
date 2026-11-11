"""
S2 Arc Typology: Classifying Poems by Their Information Curve Shape

The quarter-arc experiment established that the dominant pattern is monotone decline
(Q1 highest S2 → Q4 lowest), but 52.2% of poems show a mid-poem trough and 21.3%
have Q1 as minimum. This experiment formalizes these observations into a typology.

For each poem with >=40 clean tokens, classify its Q1→Q4 S2 arc into one of:
  - DECLINE: Monotone decline (Q1 > Q2 > Q3 > Q4, or close to it)
  - ASCENT:  Monotone ascent (Q4 > Q3 > Q2 > Q1)
  - U_SHAPE: Dip in middle (Q2 or Q3 is minimum, Q1 and Q4 both higher)
  - ARCH:    Peak in middle (Q2 or Q3 is maximum, Q1 and Q4 both lower)
  - FLAT:    Low variance across quarters (all quarters within 1 bit of each other)
  - ERRATIC: No clear pattern

Then correlate arc type with:
  - Literary era
  - Poem length
  - Form (formal/free verse)
  - Specific author signatures

Builds on: findings/quarter_arc_mid_dip.md, findings/within_poem_type_arc.md
"""

import json
import os
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
corpus_path = os.path.join(RESULTS_DIR, "corpus_results.json")


def classify_arc(q_vals):
    """Classify a Q1→Q4 arc pattern given [q1, q2, q3, q4] S2 averages."""
    q1, q2, q3, q4 = q_vals
    vals = q_vals
    rng = max(vals) - min(vals)

    # FLAT: very small variation
    if rng < 1.0:
        return "FLAT"

    # Find min and max positions
    min_q = vals.index(min(vals))  # 0-based index
    max_q = vals.index(max(vals))

    # DECLINE: highest early, lowest late (monotone or nearly)
    if max_q == 0 and min_q == 3:
        return "DECLINE"
    if max_q == 0 and min_q >= 2 and q1 > q2 and q3 >= q4:
        return "DECLINE"
    if q1 > q2 >= q3 >= q4:
        return "DECLINE"
    # Relaxed decline: Q1 is highest and Q4 is lower
    if max_q == 0 and min_q >= 2:
        return "DECLINE"

    # ASCENT: highest late, lowest early
    if min_q == 0 and max_q == 3:
        return "ASCENT"
    if min_q == 0 and max_q >= 2 and q4 > q3 and q2 <= q1:
        return "ASCENT"
    if q4 > q3 >= q2 >= q1:
        return "ASCENT"
    # Relaxed ascent: Q4 is highest and Q1 is lower
    if max_q == 3 and min_q <= 1:
        return "ASCENT"

    # U_SHAPE: minimum in middle (Q2 or Q3), endpoints both higher
    if min_q in [1, 2] and q1 > min(q2, q3) and q4 > min(q2, q3):
        return "U_SHAPE"

    # ARCH (inverted U): maximum in middle, endpoints both lower
    if max_q in [1, 2] and q1 < max(q2, q3) and q4 < max(q2, q3):
        return "ARCH"

    return "ERRATIC"


def compute_quartile_s2(tokens):
    """Compute mean S2 per quarter for clean tokens."""
    clean = [t for t in tokens if t.get("p_newline", 0.0) < 0.9]
    n = len(clean)
    if n < 40:
        return None

    q_size = n // 4
    quarters = [
        clean[:q_size],
        clean[q_size:2*q_size],
        clean[2*q_size:3*q_size],
        clean[3*q_size:]
    ]

    return [sum(t["s2"] for t in q) / len(q) for q in quarters]


def main():
    print("Loading corpus...")
    with open(corpus_path) as f:
        corpus = json.load(f)

    results = []
    arc_by_era = defaultdict(lambda: defaultdict(int))
    arc_by_author = defaultdict(lambda: defaultdict(int))
    era_counts = defaultdict(int)
    author_counts = defaultdict(int)

    for poem in corpus:
        tokens = poem.get("tokens", [])
        q_vals = compute_quartile_s2(tokens)
        if q_vals is None:
            continue

        arc = classify_arc(q_vals)
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        title = meta.get("title", "")

        results.append({
            "title": title,
            "author": author,
            "era": era,
            "arc": arc,
            "q1": round(q_vals[0], 3),
            "q2": round(q_vals[1], 3),
            "q3": round(q_vals[2], 3),
            "q4": round(q_vals[3], 3),
            "range": round(max(q_vals) - min(q_vals), 3),
            "n_clean": len([t for t in tokens if t.get("p_newline", 0.0) < 0.9]),
        })

        arc_by_era[era][arc] += 1
        era_counts[era] += 1
        arc_by_author[author][arc] += 1
        author_counts[author] += 1

    # Overall distribution
    arc_counts = defaultdict(int)
    for r in results:
        arc_counts[r["arc"]] += 1
    total = len(results)

    print(f"\nTotal poems analyzed: {total}")
    print("\nArc type distribution:")
    for arc, count in sorted(arc_counts.items(), key=lambda x: -x[1]):
        print(f"  {arc}: {count} ({count/total*100:.1f}%)")

    # Era breakdown — which eras favor which arc?
    print("\n\nArc type by era (eras with n>=5):")
    print(f"{'Era':<25} {'n':>4} {'DEC%':>6} {'ASC%':>6} {'U%':>6} {'ARCH%':>6} {'FLAT%':>6} {'ERR%':>6}")
    for era, total_era in sorted(era_counts.items(), key=lambda x: -x[1]):
        if total_era < 5:
            continue
        arcs = arc_by_era[era]
        def pct(arc):
            return f"{arcs.get(arc, 0)/total_era*100:.0f}%"
        print(f"{era:<25} {total_era:>4} {pct('DECLINE'):>6} {pct('ASCENT'):>6} {pct('U_SHAPE'):>6} {pct('ARCH'):>6} {pct('FLAT'):>6} {pct('ERRATIC'):>6}")

    # Find most extreme ASCENT poems (Q4 >> Q1) — the anti-culmination
    ascents = sorted([r for r in results if r["arc"] == "ASCENT"],
                     key=lambda x: x["q4"] - x["q1"], reverse=True)
    print("\n\nTop ASCENT poems (Q4 >> Q1, anti-culmination):")
    for r in ascents[:10]:
        delta = r["q4"] - r["q1"]
        print(f"  {r['author']:30} '{r['title'][:40]}'  Q1={r['q1']:+.2f} Q4={r['q4']:+.2f}  Δ={delta:+.2f}")

    # Find most extreme DECLINE poems (Q1 >> Q4)
    declines = sorted([r for r in results if r["arc"] == "DECLINE"],
                      key=lambda x: x["q1"] - x["q4"], reverse=True)
    print("\nTop DECLINE poems (Q1 >> Q4, front-loaded):")
    for r in declines[:10]:
        delta = r["q1"] - r["q4"]
        print(f"  {r['author']:30} '{r['title'][:40]}'  Q1={r['q1']:+.2f} Q4={r['q4']:+.2f}  Δ={delta:+.2f}")

    # Find exemplary U-SHAPE poems
    u_shapes = sorted([r for r in results if r["arc"] == "U_SHAPE"],
                      key=lambda x: min(x["q2"], x["q3"]) - (x["q1"] + x["q4"]) / 2,
                      reverse=False)  # most extreme U (deepest valley)
    print("\nTop U_SHAPE poems (deepest mid-poem valley):")
    for r in u_shapes[:8]:
        valley = min(r["q2"], r["q3"])
        avg_ends = (r["q1"] + r["q4"]) / 2
        print(f"  {r['author']:30} '{r['title'][:40]}'  valley={valley:+.2f} ends={avg_ends:+.2f}")

    # Find exemplary ARCH poems
    arches = sorted([r for r in results if r["arc"] == "ARCH"],
                    key=lambda x: max(x["q2"], x["q3"]) - (x["q1"] + x["q4"]) / 2,
                    reverse=True)  # highest arch
    print("\nTop ARCH poems (highest mid-poem peak):")
    for r in arches[:8]:
        peak = max(r["q2"], r["q3"])
        avg_ends = (r["q1"] + r["q4"]) / 2
        print(f"  {r['author']:30} '{r['title'][:40]}'  peak={peak:+.2f} ends={avg_ends:+.2f}")

    # Author signatures — which arc type is each author's most common?
    print("\nAuthor arc signatures (authors with n>=4):")
    for author, total_auth in sorted(author_counts.items(), key=lambda x: -x[1]):
        if total_auth < 4:
            continue
        arcs = arc_by_author[author]
        dominant = max(arcs, key=arcs.get)
        dominant_pct = arcs[dominant] / total_auth * 100
        print(f"  {author:<35} n={total_auth:>3}  dominant={dominant:<10} ({dominant_pct:.0f}%)")

    # Save results
    output = {
        "total_analyzed": total,
        "arc_distribution": {k: v for k, v in arc_counts.items()},
        "poems": sorted(results, key=lambda x: x["arc"]),
        "era_arc_counts": {era: dict(arcs) for era, arcs in arc_by_era.items()},
        "author_arc_counts": {auth: dict(arcs) for auth, arcs in arc_by_author.items()},
    }
    output_path = os.path.join(RESULTS_DIR, "s2_arc_typology.json")
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {output_path}")
    return output


if __name__ == "__main__":
    main()
