"""
Within-Line S2 Peak Position Analysis

Where within a poetic line does the maximum S2 value occur?
Front-loaded (near the beginning), medial (near the middle),
or end-loaded (near the end)?

Hypothesis:
  - Formal verse (end-rhyme): peak should AVOID the line-final position
    because rhyme position = high predictability = low S2.
    Expect mid-line or early peaks.
  - Free verse (Whitman, beat): no strong bias, possibly front-loaded
    because free verse often front-weights the powerful substantive word.
  - Haiku: mid-to-end (cutting word / season word effect).
  - Language / Oulipo: flat / random distribution.

Method:
  - Reconstruct lines by splitting at newline tokens.
  - For each line with >= 4 content tokens (excluding newlines and
    stanza-break artifacts: p_newline > 0.9):
      * Find normalized position of max-S2 token (0 = start, 1 = end).
      * Compute S2 slope (linear regression) to see if surprise rises
        or falls toward line end.
  - Aggregate by era.

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
ARTIFACT_THRESHOLD = 0.9  # p_newline threshold for stanza-break token


def is_artifact(tok):
    return (tok.get("p_newline", 0) > ARTIFACT_THRESHOLD
            or "\n" in tok["token"])


def slope(vals):
    """Linear regression slope of a list of values vs. their index."""
    n = len(vals)
    if n < 3:
        return 0.0
    x_mean = (n - 1) / 2.0
    y_mean = statistics.mean(vals)
    num = sum((i - x_mean) * (vals[i] - y_mean) for i in range(n))
    den = sum((i - x_mean) ** 2 for i in range(n))
    return num / den if den else 0.0


def analyze_intraline_peaks(data):
    era_peaks = defaultdict(list)   # era -> [normalized_peak_pos, ...]
    era_slopes = defaultdict(list)  # era -> [s2_slope, ...]
    poem_rows = []

    for poem in data:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        if era == "control":
            continue

        tokens = poem.get("tokens", [])
        current_line = []
        poem_peaks = []
        poem_slopes = []

        def process_line(line_toks):
            content = [t for t in line_toks if not is_artifact(t)]
            if len(content) < 4:
                return
            s2_vals = [t["s2"] for t in content]
            max_s2 = max(s2_vals)
            max_idx = s2_vals.index(max_s2)
            n = len(s2_vals)
            norm_pos = max_idx / (n - 1) if n > 1 else 0.5
            sl = slope(s2_vals)
            era_peaks[era].append(norm_pos)
            era_slopes[era].append(sl)
            poem_peaks.append(norm_pos)
            poem_slopes.append(sl)

        for tok in tokens:
            if "\n" in tok["token"]:
                process_line(current_line)
                current_line = []
            else:
                current_line.append(tok)
        process_line(current_line)  # final line without trailing newline

        if poem_peaks:
            poem_rows.append({
                "title": meta.get("title", "?")[:40],
                "author": meta.get("author", "?"),
                "era": era,
                "n_lines": len(poem_peaks),
                "mean_peak": statistics.mean(poem_peaks),
                "mean_slope": statistics.mean(poem_slopes),
            })

    return era_peaks, era_slopes, poem_rows


def tertile(peaks):
    front = sum(1 for p in peaks if p < 0.333) / len(peaks)
    mid   = sum(1 for p in peaks if 0.333 <= p <= 0.667) / len(peaks)
    end   = sum(1 for p in peaks if p > 0.667) / len(peaks)
    return front, mid, end


def print_report(era_peaks, era_slopes, poem_rows):
    total_lines = sum(len(v) for v in era_peaks.values())
    print("=" * 76)
    print("WITHIN-LINE S2 PEAK POSITION ANALYSIS")
    print("=" * 76)
    print(f"\nTotal lines analyzed: {total_lines}  |  Eras: {len(era_peaks)}\n")

    # Era table — sort by mean peak position
    summary = []
    for era, peaks in era_peaks.items():
        if len(peaks) < 8:
            continue
        front, mid, end = tertile(peaks)
        summary.append({
            "era": era,
            "n": len(peaks),
            "mean": statistics.mean(peaks),
            "front": front,
            "mid": mid,
            "end": end,
            "slope": statistics.mean(era_slopes[era]),
        })
    summary.sort(key=lambda x: x["mean"])

    header = (f"{'Era':<26} {'N':<7} {'MeanPos':<10} "
              f"{'Front%':<8} {'Mid%':<8} {'End%':<8} {'Slope'}")
    print(header)
    print("-" * 76)
    for e in summary:
        flag = " ◀" if e["mean"] < 0.42 else (" ▶" if e["mean"] > 0.58 else "")
        print(f"{e['era']:<26} {e['n']:<7} {e['mean']:.3f}{'':<5} "
              f"{e['front']*100:5.0f}%   {e['mid']*100:5.0f}%   {e['end']*100:5.0f}%   "
              f"{e['slope']:+.3f}{flag}")

    all_peaks = [p for v in era_peaks.values() for p in v]
    all_slopes = [s for v in era_slopes.values() for s in v]
    print(f"\nGlobal mean peak position : {statistics.mean(all_peaks):.4f}  "
          f"(uniform baseline = 0.5000)")
    print(f"Global mean S2 slope      : {statistics.mean(all_slopes):+.4f}  "
          f"(neg = S2 falls toward line end)")

    # Front-loaded poems
    print("\n── 10 MOST FRONT-LOADED POEMS (peak near line start) ──────────────")
    for p in sorted((r for r in poem_rows if r["n_lines"] >= 4),
                    key=lambda x: x["mean_peak"])[:10]:
        print(f"  {p['mean_peak']:.3f}  {p['title']:<40} {p['author']}")

    # End-loaded poems
    print("\n── 10 MOST END-LOADED POEMS (peak near line end) ──────────────────")
    for p in sorted((r for r in poem_rows if r["n_lines"] >= 4),
                    key=lambda x: -x["mean_peak"])[:10]:
        print(f"  {p['mean_peak']:.3f}  {p['title']:<40} {p['author']}")

    # Strongest falling slope (S2 drops toward line end → end-predictable)
    print("\n── 10 STEEPEST FALLING S2 SLOPE (end-predictable) ─────────────────")
    for p in sorted((r for r in poem_rows if r["n_lines"] >= 4),
                    key=lambda x: x["mean_slope"])[:10]:
        print(f"  {p['mean_slope']:+.3f}  {p['title']:<40} {p['author']}")

    # Strongest rising slope
    print("\n── 10 STEEPEST RISING S2 SLOPE (end-surprising) ───────────────────")
    for p in sorted((r for r in poem_rows if r["n_lines"] >= 4),
                    key=lambda x: -x["mean_slope"])[:10]:
        print(f"  {p['mean_slope']:+.3f}  {p['title']:<40} {p['author']}")


if __name__ == "__main__":
    print("Loading corpus...")
    data = json.load(open(RESULTS_PATH))
    print(f"Loaded {len(data)} texts.\n")

    era_peaks, era_slopes, poem_rows = analyze_intraline_peaks(data)
    print_report(era_peaks, era_slopes, poem_rows)
    print("\nDone.")
