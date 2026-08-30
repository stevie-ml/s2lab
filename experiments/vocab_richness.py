"""
Vocabulary Richness vs S2 Profiles
Investigates whether type-token ratio (TTR) and lexical diversity
correlate with information-theoretic signatures in poetry.
"""

import json
import re
from collections import Counter
from math import sqrt


def load_data():
    with open("results/corpus_results.json") as f:
        return json.load(f)


def tokenize_words(text):
    """Extract word tokens (lowercase, stripped of punctuation) from poem text."""
    words = re.findall(r"\b[a-z']+\b", text.lower())
    return [w for w in words if w]


def compute_ttr(words):
    """Type-token ratio: unique types / total tokens."""
    if not words:
        return 0.0
    return len(set(words)) / len(words)


def compute_repeat_ratio(words):
    """Fraction of tokens that are repeated (appear more than once)."""
    if not words:
        return 0.0
    counts = Counter(words)
    repeated = sum(1 for w in words if counts[w] > 1)
    return repeated / len(words)


def compute_hapax_ratio(words):
    """Hapax legomena ratio: words appearing exactly once / total tokens."""
    if not words:
        return 0.0
    counts = Counter(words)
    hapax = sum(1 for w, c in counts.items() if c == 1)
    return hapax / len(words)


def pearson_r(xs, ys):
    """Compute Pearson correlation coefficient."""
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denom = sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / denom if denom else 0.0


def run():
    data = load_data()

    # Filter to English poetry only (exclude control prose)
    poems = [
        d for d in data
        if d["metadata"].get("era") != "control"
        and d["metadata"].get("language", "en") == "en"
    ]

    rows = []
    for poem in poems:
        meta = poem["metadata"]
        summary = poem["summary"]

        # We need the original text — reconstruct approximate text from tokens
        token_texts = [t["token"] for t in poem["tokens"]]
        raw = "".join(token_texts)

        words = tokenize_words(raw)
        if len(words) < 5:
            continue

        ttr = compute_ttr(words)
        repeat_ratio = compute_repeat_ratio(words)
        hapax_ratio = compute_hapax_ratio(words)
        n_words = len(words)
        n_types = len(set(words))

        rows.append({
            "title": meta["title"],
            "author": meta["author"],
            "era": meta["era"],
            "year": meta.get("year", 0),
            "n_tokens": meta["n_tokens"],
            "n_words": n_words,
            "n_types": n_types,
            "ttr": round(ttr, 4),
            "repeat_ratio": round(repeat_ratio, 4),
            "hapax_ratio": round(hapax_ratio, 4),
            "avg_s2": round(summary["avg_s2"], 4),
            "avg_surprisal": round(summary["avg_surprisal"], 4),
            "avg_entropy": round(summary["avg_entropy"], 4),
            "pos_s2_ratio": round(summary["pos_s2_ratio"], 4),
            "std_s2": round(summary["std_s2"], 4),
        })

    return rows


def print_report(rows):
    # Sort by TTR descending
    rows_by_ttr = sorted(rows, key=lambda r: r["ttr"], reverse=True)

    print("=" * 72)
    print("VOCABULARY RICHNESS vs S2 PROFILES")
    print("=" * 72)
    print(f"\n{'Author':<22} {'Title':<28} {'TTR':>5} {'AvgS2':>6} {'Hpx%':>5} {'nWrd':>5}")
    print("-" * 72)
    for r in rows_by_ttr:
        title_short = r["title"][:27]
        author_short = r["author"][:21]
        print(f"{author_short:<22} {title_short:<28} {r['ttr']:>5.3f} {r['avg_s2']:>+6.2f} {r['hapax_ratio']:>5.2f} {r['n_words']:>5}")

    # Correlations
    ttrs = [r["ttr"] for r in rows]
    avg_s2s = [r["avg_s2"] for r in rows]
    avg_surps = [r["avg_surprisal"] for r in rows]
    avg_ents = [r["avg_entropy"] for r in rows]
    pos_s2_ratios = [r["pos_s2_ratio"] for r in rows]
    repeat_ratios = [r["repeat_ratio"] for r in rows]

    print("\n" + "=" * 72)
    print("CORRELATION: TTR vs Information Metrics (r = Pearson)")
    print("-" * 72)
    print(f"  TTR vs avg_s2:         r = {pearson_r(ttrs, avg_s2s):+.4f}")
    print(f"  TTR vs avg_surprisal:  r = {pearson_r(ttrs, avg_surps):+.4f}")
    print(f"  TTR vs avg_entropy:    r = {pearson_r(ttrs, avg_ents):+.4f}")
    print(f"  TTR vs pos_s2_ratio:   r = {pearson_r(ttrs, pos_s2_ratios):+.4f}")
    print(f"  repeat_ratio vs avg_s2: r = {pearson_r(repeat_ratios, avg_s2s):+.4f}")

    # Quartile analysis
    sorted_by_ttr = sorted(rows, key=lambda r: r["ttr"])
    n = len(sorted_by_ttr)
    q1 = sorted_by_ttr[:n // 4]
    q4 = sorted_by_ttr[3 * n // 4:]

    def mean(vals):
        return sum(vals) / len(vals) if vals else 0

    print("\n" + "=" * 72)
    print("QUARTILE ANALYSIS: Low-TTR (repetitive) vs High-TTR (lexically rich)")
    print("-" * 72)
    for label, group in [("Bottom 25% TTR (repetitive)", q1), ("Top 25% TTR (lexically rich)", q4)]:
        avg_ttr = mean([r["ttr"] for r in group])
        avg_s2 = mean([r["avg_s2"] for r in group])
        avg_surp = mean([r["avg_surprisal"] for r in group])
        avg_ent = mean([r["avg_entropy"] for r in group])
        avg_pos = mean([r["pos_s2_ratio"] for r in group])
        print(f"\n{label} (n={len(group)}, avg_TTR={avg_ttr:.3f}):")
        print(f"  avg_S2={avg_s2:+.3f}  avg_surprisal={avg_surp:.3f}  avg_entropy={avg_ent:.3f}  pos_S2_ratio={avg_pos:.3f}")

    # Spotlight: most repetitive poems
    print("\n" + "=" * 72)
    print("SPOTLIGHT: 5 Most Repetitive Poems (lowest TTR)")
    print("-" * 72)
    for r in sorted(rows, key=lambda r: r["ttr"])[:5]:
        print(f"  TTR={r['ttr']:.3f}  AvgS2={r['avg_s2']:+.3f}  repeat={r['repeat_ratio']:.2f}  {r['author']}: \"{r['title']}\"")

    print("\n" + "=" * 72)
    print("SPOTLIGHT: 5 Most Lexically Rich Poems (highest TTR)")
    print("-" * 72)
    for r in sorted(rows, key=lambda r: r["ttr"], reverse=True)[:5]:
        print(f"  TTR={r['ttr']:.3f}  AvgS2={r['avg_s2']:+.3f}  hapax={r['hapax_ratio']:.2f}  {r['author']}: \"{r['title']}\"")

    return rows


if __name__ == "__main__":
    rows = run()
    print_report(rows)
