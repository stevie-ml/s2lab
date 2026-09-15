"""
Line Length vs S₂ Analysis

Hypothesis: Shorter lines concentrate more information per token. If a poet
compresses into fewer tokens, each token must carry more semantic weight —
manifesting as higher S₂. Conversely, long Whitmanesque catalogs may spread
S₂ thinly across many tokens.

We test this by segmenting each poem into lines (split on \n), computing
per-line token count and avg S₂, then looking for correlation at multiple
levels: within poems, across poems, and across eras.
"""

import json
import statistics
from collections import defaultdict
from pathlib import Path

DATA_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs) if len(xs) > 1 else 0
    sy = statistics.stdev(ys) if len(ys) > 1 else 0
    if sx == 0 or sy == 0:
        return float("nan")
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / ((n - 1) * sx * sy)


def segment_into_lines(tokens):
    """Group tokens by line (split at newline tokens)."""
    lines = []
    current = []
    for t in tokens:
        if t["token"] == "\n" or t["token"] == "\r\n":
            if current:
                lines.append(current)
                current = []
        else:
            current.append(t)
    if current:
        lines.append(current)
    return lines


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def main():
    data = load_data()

    print("=" * 70)
    print("LINE LENGTH VS S₂ ANALYSIS")
    print("=" * 70)

    # --- 1. Per-poem line stats ---
    poem_rows = []
    all_line_lengths = []
    all_line_s2 = []

    # Separate poetry vs control
    poetry_line_lengths = []
    poetry_line_s2 = []
    prose_line_lengths = []
    prose_line_s2 = []

    for entry in data:
        meta = entry["metadata"]
        tokens = entry.get("tokens", [])
        if not tokens:
            continue

        lines = segment_into_lines(tokens)
        if len(lines) < 2:
            continue

        is_control = meta.get("era") == "control"

        per_line = []
        for line in lines:
            if len(line) < 2:  # skip single-token lines
                continue
            avg_s2 = statistics.mean(t["s2"] for t in line)
            n_tokens = len(line)
            per_line.append((n_tokens, avg_s2))

        if len(per_line) < 3:
            continue

        lengths = [x[0] for x in per_line]
        s2s = [x[1] for x in per_line]

        poem_rows.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta.get("era", "unknown"),
            "is_control": is_control,
            "n_lines": len(per_line),
            "avg_line_len": statistics.mean(lengths),
            "median_line_len": statistics.median(lengths),
            "avg_s2": statistics.mean(s2s),
            "within_r": pearson_r(lengths, s2s),
            "per_line": per_line,
        })

        for length, s2 in per_line:
            all_line_lengths.append(length)
            all_line_s2.append(s2)
            if is_control:
                prose_line_lengths.append(length)
                prose_line_s2.append(s2)
            else:
                poetry_line_lengths.append(length)
                poetry_line_s2.append(s2)

    poetry_rows = [r for r in poem_rows if not r["is_control"]]
    prose_rows = [r for r in poem_rows if r["is_control"]]

    # --- 2. Global correlation ---
    print("\n## 1. Global Line-Length vs S₂ Correlation")
    print()
    r_all = pearson_r(all_line_lengths, all_line_s2)
    r_poetry = pearson_r(poetry_line_lengths, poetry_line_s2)
    r_prose = pearson_r(prose_line_lengths, prose_line_s2)
    print(f"  All texts:  r(line_len, S₂) = {r_all:+.4f}  (n={len(all_line_lengths)} lines)")
    print(f"  Poetry:     r(line_len, S₂) = {r_poetry:+.4f}  (n={len(poetry_line_lengths)} lines)")
    print(f"  Prose ctrl: r(line_len, S₂) = {r_prose:+.4f}  (n={len(prose_line_lengths)} lines)")

    # --- 3. Line length buckets ---
    print("\n## 2. S₂ by Line Length Bucket (poetry lines only)")
    print()
    buckets = defaultdict(list)
    for length, s2 in zip(poetry_line_lengths, poetry_line_s2):
        if length <= 3:
            bucket = "1-3 tokens (very short)"
        elif length <= 6:
            bucket = "4-6 tokens (short)"
        elif length <= 10:
            bucket = "7-10 tokens (medium)"
        elif length <= 15:
            bucket = "11-15 tokens (long)"
        else:
            bucket = "16+ tokens (very long)"
        buckets[bucket].append(s2)

    bucket_order = [
        "1-3 tokens (very short)",
        "4-6 tokens (short)",
        "7-10 tokens (medium)",
        "11-15 tokens (long)",
        "16+ tokens (very long)",
    ]

    print(f"  {'Bucket':<28} {'n':>6} {'Avg S₂':>8} {'Median S₂':>10}")
    print("  " + "-" * 56)
    for bucket in bucket_order:
        s2s = buckets[bucket]
        if not s2s:
            continue
        print(f"  {bucket:<28} {len(s2s):>6} {statistics.mean(s2s):>+8.4f} "
              f"{statistics.median(s2s):>+10.4f}")

    # --- 4. Within-poem correlation distribution ---
    print("\n## 3. Within-Poem Correlation r(line_len, S₂) Distribution")
    print()
    within_rs = [r["within_r"] for r in poetry_rows if not (r["within_r"] != r["within_r"])]
    valid_rs = [r for r in within_rs if r == r]  # drop NaN
    if valid_rs:
        pos = sum(1 for r in valid_rs if r > 0)
        neg = sum(1 for r in valid_rs if r < 0)
        print(f"  n poems analyzed: {len(valid_rs)}")
        print(f"  Mean within-poem r: {statistics.mean(valid_rs):+.4f}")
        print(f"  Poems with r > 0 (longer lines → higher S₂): {pos} ({100*pos//len(valid_rs)}%)")
        print(f"  Poems with r < 0 (shorter lines → higher S₂): {neg} ({100*neg//len(valid_rs)}%)")

    # --- 5. Poems with strongest negative r (short=high S2) ---
    print("\n## 4. Poems Where Short Lines Drive Highest S₂ (most negative within-r)")
    print()
    sorted_neg = sorted(poetry_rows, key=lambda r: r["within_r"])
    for row in sorted_neg[:10]:
        print(f"  r={row['within_r']:+.3f}  avg_line={row['avg_line_len']:.1f}tok  "
              f"n_lines={row['n_lines']}  {row['author']}, \"{row['title']}\"")

    # --- 6. Poems with strongest positive r (long=high S2) ---
    print("\n## 5. Poems Where Long Lines Drive Highest S₂ (most positive within-r)")
    print()
    sorted_pos = sorted(poetry_rows, key=lambda r: -r["within_r"])
    for row in sorted_pos[:10]:
        print(f"  r={row['within_r']:+.3f}  avg_line={row['avg_line_len']:.1f}tok  "
              f"n_lines={row['n_lines']}  {row['author']}, \"{row['title']}\"")

    # --- 7. Era analysis ---
    print("\n## 6. Average Line Length by Era")
    print()
    era_data = defaultdict(list)
    for row in poetry_rows:
        era_data[row["era"]].append(row)

    era_stats = []
    for era, rows in era_data.items():
        avg_len = statistics.mean(r["avg_line_len"] for r in rows)
        avg_s2 = statistics.mean(r["avg_s2"] for r in rows)
        era_stats.append((era, len(rows), avg_len, avg_s2))
    era_stats.sort(key=lambda x: x[2])  # sort by line length

    print(f"  {'Era':<24} {'n':>4} {'Avg line len':>14} {'Avg S₂':>8}")
    print("  " + "-" * 54)
    for era, n, avg_len, avg_s2 in era_stats:
        print(f"  {era:<24} {n:>4} {avg_len:>14.2f} {avg_s2:>+8.4f}")

    r_era = pearson_r([x[2] for x in era_stats], [x[3] for x in era_stats])
    print(f"\n  Cross-era r(avg_line_len, avg_S₂) = {r_era:+.4f}")

    # --- 8. Summary ---
    print("\n## 7. Key Examples: Same Poet, Different Line Lengths")
    print()
    author_poems = defaultdict(list)
    for row in poetry_rows:
        author_poems[row["author"]].append(row)

    for author, rows in author_poems.items():
        if len(rows) >= 2:
            rows_sorted = sorted(rows, key=lambda r: r["avg_line_len"])
            shortest = rows_sorted[0]
            longest = rows_sorted[-1]
            if abs(shortest["avg_line_len"] - longest["avg_line_len"]) > 3:
                print(f"  {author}:")
                print(f"    Short: \"{shortest['title']}\" — {shortest['avg_line_len']:.1f} tok/line, "
                      f"S₂={shortest['avg_s2']:+.3f}")
                print(f"    Long:  \"{longest['title']}\" — {longest['avg_line_len']:.1f} tok/line, "
                      f"S₂={longest['avg_s2']:+.3f}")
                print()

    return {
        "r_all": r_all,
        "r_poetry": r_poetry,
        "r_prose": r_prose,
        "mean_within_r": statistics.mean(valid_rs) if valid_rs else float("nan"),
        "n_lines_poetry": len(poetry_line_lengths),
        "n_poems": len(poetry_rows),
    }


if __name__ == "__main__":
    results = main()
