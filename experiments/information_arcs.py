"""
Information Arcs: Shape of S₂ trajectories within poems.

Do poems have characteristic "information arc" shapes? Do these shapes
correlate with era, form, or author?

Arc types classified:
  - rising:   S₂ increases toward end (building tension)
  - falling:  S₂ decreases toward end (front-loaded surprise)
  - arch:     S₂ peaks in middle (climax structure)
  - valley:   S₂ dips in middle (framing structure)
  - spike:    One extreme outlier dominates; otherwise flat
  - flat:     No clear shape (near-zero slope across)
  - complex:  Multiple reversals (volatile profile)
"""

import json
import math
from collections import defaultdict


def load_corpus(path="results/corpus_results.json"):
    with open(path) as f:
        return json.load(f)


def smooth(values, window=5):
    """Simple moving average smoothing."""
    if len(values) < window:
        return values
    out = []
    half = window // 2
    for i in range(len(values)):
        lo = max(0, i - half)
        hi = min(len(values), i + half + 1)
        out.append(sum(values[lo:hi]) / (hi - lo))
    return out


def linear_slope(values):
    """Return slope of best-fit line (normalized x in [0,1])."""
    n = len(values)
    if n < 3:
        return 0.0
    xs = [i / (n - 1) for i in range(n)]
    xm = sum(xs) / n
    ym = sum(values) / n
    num = sum((xs[i] - xm) * (values[i] - ym) for i in range(n))
    den = sum((xs[i] - xm) ** 2 for i in range(n))
    return num / den if den > 0 else 0.0


def classify_arc(s2_values):
    """
    Returns (arc_type, peak_pos_pct, valley_pos_pct, slope, volatility).
    """
    if len(s2_values) < 6:
        return "too_short", None, None, 0.0, 0.0

    smoothed = smooth(s2_values, window=max(3, len(s2_values) // 5))
    n = len(smoothed)

    slope = linear_slope(smoothed)
    peak_idx = smoothed.index(max(smoothed))
    valley_idx = smoothed.index(min(smoothed))
    peak_pos = peak_idx / (n - 1)
    valley_pos = valley_idx / (n - 1)

    # Volatility: std of raw s2
    mean = sum(s2_values) / len(s2_values)
    volatility = math.sqrt(sum((v - mean) ** 2 for v in s2_values) / len(s2_values))

    # Spike detection: is one token responsible for >50% of total positive deviation?
    positives = [v for v in s2_values if v > 0]
    if positives:
        max_val = max(s2_values)
        total_pos = sum(positives)
        spike_ratio = max_val / total_pos if total_pos > 0 else 0
    else:
        spike_ratio = 0

    # Classify
    abs_slope = abs(slope)

    if spike_ratio > 0.6 and len(positives) < len(s2_values) * 0.15:
        arc = "spike"
    elif abs_slope < 1.0:
        # Flat-ish — check for arch or valley
        if 0.25 < peak_pos < 0.75 and (smoothed[peak_idx] - smoothed[0] > 0.5):
            arc = "arch"
        elif 0.25 < valley_pos < 0.75 and (smoothed[0] - smoothed[valley_idx] > 0.5):
            arc = "valley"
        else:
            # count direction changes in smoothed
            changes = sum(
                1
                for i in range(1, n - 1)
                if (smoothed[i] - smoothed[i - 1]) * (smoothed[i + 1] - smoothed[i]) < 0
            )
            if changes > n * 0.3:
                arc = "complex"
            else:
                arc = "flat"
    elif slope > 1.0:
        arc = "rising"
    else:
        arc = "falling"

    return arc, round(peak_pos * 100), round(valley_pos * 100), round(slope, 3), round(volatility, 3)


def run_arc_analysis(data):
    """Analyze arc shapes across the corpus."""
    results = []
    arc_counts = defaultdict(int)
    era_arcs = defaultdict(lambda: defaultdict(int))
    author_arcs = defaultdict(lambda: defaultdict(int))
    arc_s2 = defaultdict(list)

    for poem in data:
        meta = poem["metadata"]
        tokens = poem.get("tokens", [])
        if not tokens or meta.get("language", "en") != "en":
            continue

        # Skip if too short
        if len(tokens) < 6:
            continue

        s2_vals = [t["s2"] for t in tokens]
        avg_s2 = sum(s2_vals) / len(s2_vals)

        arc, peak_pct, valley_pct, slope, volatility = classify_arc(s2_vals)

        results.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta["era"],
            "n_tokens": len(tokens),
            "avg_s2": round(avg_s2, 3),
            "arc": arc,
            "peak_pct": peak_pct,
            "valley_pct": valley_pct,
            "slope": slope,
            "volatility": volatility,
        })

        arc_counts[arc] += 1
        era_arcs[meta["era"]][arc] += 1
        author_arcs[meta["author"]][arc] += 1
        arc_s2[arc].append(avg_s2)

    return results, arc_counts, era_arcs, author_arcs, arc_s2


def fmt_table(rows, headers, widths=None):
    """Simple ASCII table formatter."""
    if widths is None:
        widths = [max(len(str(r[i])) for r in [headers] + rows) + 2 for i in range(len(headers))]
    header_row = "|".join(str(h).ljust(w) for h, w in zip(headers, widths))
    sep = "|".join("-" * w for w in widths)
    lines = [f"| {header_row} |", f"|{sep}|"]
    for row in rows:
        lines.append("| " + "|".join(str(v).ljust(w) for v, w in zip(row, widths)) + " |")
    return "\n".join(lines)


def run():
    data = load_corpus()
    results, arc_counts, era_arcs, author_arcs, arc_s2 = run_arc_analysis(data)

    n_poems = len(results)
    poetry = [r for r in results if r["era"] != "control"]
    prose = [r for r in results if r["era"] == "control"]

    print("\n=== Information Arc Analysis ===\n")

    # 1. Overall arc distribution
    print("### Overall Arc Distribution (poetry only)\n")
    arc_rows = []
    for arc, count in sorted(arc_counts.items(), key=lambda x: -x[1]):
        if arc == "too_short":
            continue
        pct = round(100 * count / n_poems)
        avg = round(sum(arc_s2[arc]) / len(arc_s2[arc]), 3) if arc_s2[arc] else 0
        arc_rows.append([arc, count, f"{pct}%", avg])
    print(fmt_table(arc_rows, ["Arc Type", "Count", "%", "Avg S₂"], [14, 8, 6, 10]))

    # 2. Peak position distribution — where does the S₂ peak cluster?
    peak_positions = [r["peak_pct"] for r in poetry if r["peak_pct"] is not None]
    bins = [0] * 5  # 0-19, 20-39, 40-59, 60-79, 80-99
    for p in peak_positions:
        bins[min(p // 20, 4)] += 1

    print("\n### Peak S₂ Position Distribution (poetry)\n")
    bin_rows = [
        ["0-19% (opening)", bins[0], f"{round(100*bins[0]/len(peak_positions))}%"],
        ["20-39%", bins[1], f"{round(100*bins[1]/len(peak_positions))}%"],
        ["40-59% (middle)", bins[2], f"{round(100*bins[2]/len(peak_positions))}%"],
        ["60-79%", bins[3], f"{round(100*bins[3]/len(peak_positions))}%"],
        ["80-99% (ending)", bins[4], f"{round(100*bins[4]/len(peak_positions))}%"],
    ]
    print(fmt_table(bin_rows, ["Region", "Count", "%"], [20, 8, 6]))

    # 3. Era breakdown
    print("\n### Arc Types by Era\n")
    arc_types = ["rising", "falling", "arch", "valley", "flat", "complex", "spike"]
    era_list = sorted(era_arcs.keys())
    for era in era_list:
        total = sum(era_arcs[era].values())
        parts = [era_arcs[era].get(a, 0) for a in arc_types]
        dominant = arc_types[parts.index(max(parts))]
        print(f"  **{era}** (n={total}): dominant={dominant} | " +
              ", ".join(f"{a}:{era_arcs[era].get(a,0)}" for a in arc_types if era_arcs[era].get(a, 0) > 0))

    # 4. Extreme examples — most dramatic arcs
    print("\n### Most Dramatic Rising Arcs (slope > 2.0)\n")
    rising = sorted([r for r in poetry if r["arc"] == "rising"], key=lambda x: -x["slope"])[:5]
    for r in rising:
        print(f"  {r['author']} — '{r['title']}' (slope={r['slope']}, avg_s2={r['avg_s2']})")

    print("\n### Most Dramatic Falling Arcs (slope < -2.0)\n")
    falling = sorted([r for r in poetry if r["arc"] == "falling"], key=lambda x: x["slope"])[:5]
    for r in falling:
        print(f"  {r['author']} — '{r['title']}' (slope={r['slope']}, avg_s2={r['avg_s2']})")

    print("\n### Arch-shaped poems (S₂ peaks in middle)\n")
    arches = sorted([r for r in poetry if r["arc"] == "arch"], key=lambda x: -x["avg_s2"])[:8]
    for r in arches:
        print(f"  {r['author']} — '{r['title']}' (peak at {r['peak_pct']}%, avg_s2={r['avg_s2']})")

    # 5. Volatility leaders
    print("\n### Most Volatile S₂ Profiles\n")
    volatile = sorted(poetry, key=lambda x: -x["volatility"])[:8]
    for r in volatile:
        print(f"  {r['author']} — '{r['title']}' (σ={r['volatility']}, arc={r['arc']})")

    # 6. Arc vs avg S₂ summary
    print("\n### Arc Type → Avg S₂ Relationship\n")
    arc_avg_rows = []
    for arc in arc_types:
        vals = arc_s2.get(arc, [])
        if vals:
            avg = round(sum(vals) / len(vals), 3)
            arc_avg_rows.append([arc, len(vals), avg])
    arc_avg_rows.sort(key=lambda x: -x[2])
    print(fmt_table(arc_avg_rows, ["Arc", "n", "Avg S₂"], [12, 6, 10]))

    return results, arc_counts, era_arcs, arc_s2


if __name__ == "__main__":
    run()
