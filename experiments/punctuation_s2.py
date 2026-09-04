"""
Punctuation and S2: How punctuation tokens affect information-theoretic profiles.

Questions:
1. What are the S2 values of punctuation tokens themselves?
2. Do tokens immediately following punctuation have higher S2? (fresh context = more freedom)
3. Do punctuation-heavy poets have different S2 profiles than punctuation-light poets?
4. Is Dickinson's famous dash informationally distinctive?
"""

import json
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


PUNCTUATION_TOKENS = {
    ".",  ",",  ";",  ":",  "!",  "?",
    "–",  "—",  "-",  "...",
    "'",  '"',  "(",  ")",
    "\n", "\r\n",
}

DASH_VARIANTS = {"–", "—", "-", " –", " —", "–\n", "—\n"}


def is_punctuation(tok: str) -> bool:
    stripped = tok.strip()
    return stripped in PUNCTUATION_TOKENS or stripped.startswith("–") or stripped.startswith("—")


def is_dash(tok: str) -> bool:
    stripped = tok.strip()
    return stripped in {"–", "—", "-"} or stripped.startswith("–") or stripped.startswith("—")


def punctuation_density(tokens: list) -> float:
    """Fraction of tokens that are punctuation."""
    if not tokens:
        return 0.0
    return sum(1 for t in tokens if is_punctuation(t["token"])) / len(tokens)


def analyze_poem_punctuation(poem_result: dict) -> dict:
    tokens = poem_result.get("tokens", [])
    if not tokens:
        return {}

    meta = poem_result.get("metadata", {})
    title = meta.get("title", "")
    author = meta.get("author", "")
    year = meta.get("year", None)

    # Separate punctuation vs. non-punctuation tokens
    punct_tokens = [t for t in tokens if is_punctuation(t["token"])]
    non_punct_tokens = [t for t in tokens if not is_punctuation(t["token"])]
    dash_tokens = [t for t in tokens if is_dash(t["token"])]

    # Tokens that follow punctuation (position = position_of_punct + 1)
    punct_positions = {t["position"] for t in punct_tokens}
    post_punct_tokens = [t for t in tokens if (t["position"] - 1) in punct_positions]

    # Tokens that follow dashes specifically
    dash_positions = {t["position"] for t in dash_tokens}
    post_dash_tokens = [t for t in tokens if (t["position"] - 1) in dash_positions]

    def avg_s2(tlist):
        if not tlist:
            return None
        return round(sum(t["s2"] for t in tlist) / len(tlist), 4)

    def pos_ratio(tlist):
        if not tlist:
            return None
        return round(sum(1 for t in tlist if t["s2"] > 0) / len(tlist), 4)

    pd = punctuation_density(tokens)
    # Count dashes specifically
    n_dashes = len(dash_tokens)
    n_tokens = len(tokens)

    return {
        "title": title,
        "author": author,
        "year": year,
        "n_tokens": n_tokens,
        "punct_density": round(pd, 4),
        "n_dashes": n_dashes,
        "dash_density": round(n_dashes / n_tokens, 4) if n_tokens else 0,
        "avg_s2_all": avg_s2(tokens),
        "avg_s2_punct": avg_s2(punct_tokens),
        "avg_s2_non_punct": avg_s2(non_punct_tokens),
        "avg_s2_post_punct": avg_s2(post_punct_tokens),
        "avg_s2_post_dash": avg_s2(post_dash_tokens),
        "pos_ratio_all": pos_ratio(tokens),
        "pos_ratio_punct": pos_ratio(punct_tokens),
        "pos_ratio_non_punct": pos_ratio(non_punct_tokens),
        "pos_ratio_post_punct": pos_ratio(post_punct_tokens),
        "n_punct": len(punct_tokens),
        "n_post_punct": len(post_punct_tokens),
        "n_post_dash": len(post_dash_tokens),
    }


def run(results_path: str = None) -> list:
    if results_path is None:
        base = os.path.dirname(os.path.dirname(__file__))
        results_path = os.path.join(base, "results", "corpus_results.json")

    with open(results_path) as f:
        corpus = json.load(f)

    analyzed = []
    for poem in corpus:
        row = analyze_poem_punctuation(poem)
        if row:
            analyzed.append(row)

    return analyzed


def report(rows: list):
    print(f"\n{'='*70}")
    print("PUNCTUATION AND S₂ ANALYSIS")
    print(f"{'='*70}")
    print(f"Poems analyzed: {len(rows)}")

    # Sort by punctuation density
    rows_with_pd = [r for r in rows if r["punct_density"] is not None]
    by_pd = sorted(rows_with_pd, key=lambda r: r["punct_density"], reverse=True)

    print("\n── Top 10 most punctuation-dense poems ──")
    print(f"{'Author':<25} {'Title':<40} {'P-Dens':>6} {'Avg S₂':>7} {'Post-P S₂':>10}")
    for r in by_pd[:10]:
        print(
            f"{r['author']:<25} {r['title'][:38]:<40} "
            f"{r['punct_density']:>6.3f} {r['avg_s2_all']:>7.4f} "
            f"{(r['avg_s2_post_punct'] or 0):>10.4f}"
        )

    print("\n── Bottom 10 (least punctuation) ──")
    for r in by_pd[-10:]:
        print(
            f"{r['author']:<25} {r['title'][:38]:<40} "
            f"{r['punct_density']:>6.3f} {r['avg_s2_all']:>7.4f} "
            f"{(r['avg_s2_post_punct'] or 0):>10.4f}"
        )

    # S2 of punctuation tokens vs. non-punctuation
    punct_s2_vals = [r["avg_s2_punct"] for r in rows if r["avg_s2_punct"] is not None]
    non_punct_s2_vals = [r["avg_s2_non_punct"] for r in rows if r["avg_s2_non_punct"] is not None]
    post_punct_s2_vals = [r["avg_s2_post_punct"] for r in rows if r["avg_s2_post_punct"] is not None]
    all_s2_vals = [r["avg_s2_all"] for r in rows if r["avg_s2_all"] is not None]

    print("\n── Global averages across corpus ──")
    print(f"  Avg S₂ (all tokens):        {sum(all_s2_vals)/len(all_s2_vals):.4f}")
    print(f"  Avg S₂ (punct tokens):      {sum(punct_s2_vals)/len(punct_s2_vals):.4f}")
    print(f"  Avg S₂ (non-punct tokens):  {sum(non_punct_s2_vals)/len(non_punct_s2_vals):.4f}")
    print(f"  Avg S₂ (post-punct tokens): {sum(post_punct_s2_vals)/len(post_punct_s2_vals):.4f}")

    # High vs low punctuation density: split at median
    pd_vals = sorted(r["punct_density"] for r in rows)
    median_pd = pd_vals[len(pd_vals) // 2]
    high_pd = [r for r in rows if r["punct_density"] >= median_pd]
    low_pd = [r for r in rows if r["punct_density"] < median_pd]

    def avg(lst, key):
        vals = [r[key] for r in lst if r[key] is not None]
        return sum(vals) / len(vals) if vals else None

    print(f"\n── High-punctuation vs low-punctuation poems (median split at {median_pd:.3f}) ──")
    print(f"  High-punct (n={len(high_pd)}): avg S₂ = {avg(high_pd, 'avg_s2_all'):.4f}")
    print(f"  Low-punct  (n={len(low_pd)}): avg S₂ = {avg(low_pd, 'avg_s2_all'):.4f}")

    # Dickinson vs. Whitman specifically
    dickinson = [r for r in rows if "Dickinson" in r["author"]]
    whitman = [r for r in rows if "Whitman" in r["author"]]
    hopkins = [r for r in rows if "Hopkins" in r["author"]]

    print("\n── Dickinson vs Whitman vs Hopkins ──")
    for label, group in [("Dickinson", dickinson), ("Whitman", whitman), ("Hopkins", hopkins)]:
        if group:
            print(
                f"  {label:<12} n={len(group):2d}  "
                f"punct_density={avg(group,'punct_density'):.3f}  "
                f"dash_density={avg(group,'dash_density'):.3f}  "
                f"avg_s2={avg(group,'avg_s2_all'):.4f}  "
                f"post_punct_s2={avg(group,'avg_s2_post_punct'):.4f}"
            )

    # Dash analysis
    dash_rows = [r for r in rows if r["n_dashes"] > 0]
    print(f"\n── Dash-using poems (n={len(dash_rows)}) ──")
    print(f"  Avg post-dash S₂: {avg(dash_rows, 'avg_s2_post_dash'):.4f}")
    print(f"  vs. global post-punct S₂: {sum(post_punct_s2_vals)/len(post_punct_s2_vals):.4f}")

    # Correlation: punct density vs avg_s2
    # Simple Pearson r
    xs = [r["punct_density"] for r in rows]
    ys = [r["avg_s2_all"] for r in rows]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = (sum((x - mx) ** 2 for x in xs)) ** 0.5
    dy = (sum((y - my) ** 2 for y in ys)) ** 0.5
    r = num / (dx * dy) if dx * dy else 0
    print(f"\n── Correlation: punct_density vs avg_s2: r = {r:.4f} ──")

    return {
        "n_poems": len(rows),
        "global_avg_s2_all": round(sum(all_s2_vals) / len(all_s2_vals), 4),
        "global_avg_s2_punct": round(sum(punct_s2_vals) / len(punct_s2_vals), 4),
        "global_avg_s2_non_punct": round(sum(non_punct_s2_vals) / len(non_punct_s2_vals), 4),
        "global_avg_s2_post_punct": round(sum(post_punct_s2_vals) / len(post_punct_s2_vals), 4),
        "median_punct_density": round(median_pd, 4),
        "high_pd_avg_s2": round(avg(high_pd, "avg_s2_all"), 4),
        "low_pd_avg_s2": round(avg(low_pd, "avg_s2_all"), 4),
        "punct_density_s2_corr": round(r, 4),
        "rows": rows,
    }


if __name__ == "__main__":
    rows = run()
    stats = report(rows)
