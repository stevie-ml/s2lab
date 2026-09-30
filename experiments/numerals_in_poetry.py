"""
Numerals in Poetry: When Poets Count

Research question: Do numeral tokens (digit strings and number words) carry
distinctive S2 signatures? When a poet writes "two" or "1984", what did GPT-2
expect instead? Does specificity of quantity correlate with higher surprise?

Hypothesis: Numerals are semantically precise in a way that resists prediction —
GPT-2, trained on prose, learns that number words are rare in poetic positions.
When a poet counts ("Two roads diverged", "Four score and seven years"), they
are doing something language does not expect.

Counter-hypothesis: Many numeral uses are formulaic ("one day", "twice", "first
light") and therefore low-S2.

Sub-questions:
1. Are digit tokens (1, 2, 100) more surprising than number words (one, two)?
2. Do specific numbers (exact quantities) vs. approximate (many, few, some) differ?
3. What does GPT-2 expect when the poet writes a numeral?
4. Which poems / poets use numerals most strategically (highest numeral S2)?
"""

import json
import re
from collections import defaultdict

DATA_PATH = "results/corpus_results.json"

# Cardinal number words
CARDINALS = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
    "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen",
    "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty", "sixty",
    "seventy", "eighty", "ninety", "hundred", "thousand", "million", "billion",
    "zero", "nought", "naught",
}

# Ordinal number words
ORDINALS = {
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth",
    "ninth", "tenth", "eleventh", "twelfth", "once", "twice", "thrice",
}

# Approximate / vague quantity words (control group)
APPROXIMATE = {
    "many", "few", "some", "several", "numerous", "countless", "myriad",
    "much", "little", "most", "least", "half", "quarter",
}

DIGIT_RE = re.compile(r'^\s*\d[\d,\.]*$')

def classify_token(tok_str):
    """Classify a token into numeral categories."""
    t = tok_str.strip().lower()
    if DIGIT_RE.match(tok_str):
        return "digit"
    if t in CARDINALS:
        return "cardinal"
    if t in ORDINALS:
        return "ordinal"
    if t in APPROXIMATE:
        return "approximate"
    return None


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Collect all tokens with their categories
    all_tokens = []
    numeral_tokens = []
    approx_tokens = []

    # Track per-poem numeral density
    poem_numeral_stats = []

    for poem in data:
        meta = poem["metadata"]
        tokens = poem.get("tokens", [])

        # Exclude stanza-break artifacts (p_newline > 0.9)
        clean_tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]

        poem_numerals = []

        for tok in clean_tokens:
            tok_str = tok["token"]
            cat = classify_token(tok_str)

            record = {
                "token": tok_str.strip(),
                "s2": tok["s2"],
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "rank": tok["rank"],
                "alternatives": tok.get("alternatives", []),
                "context_before": tok.get("context_before", ""),
                "author": meta.get("author", "Unknown"),
                "title": meta.get("title", "Unknown"),
                "era": meta.get("era", "unknown"),
                "category": cat,
            }

            all_tokens.append(record)

            if cat in ("digit", "cardinal", "ordinal"):
                numeral_tokens.append(record)
                poem_numerals.append(record)
            elif cat == "approximate":
                approx_tokens.append(record)

        if poem_numerals:
            poem_numeral_stats.append({
                "author": meta.get("author", "Unknown"),
                "title": meta.get("title", "Unknown"),
                "era": meta.get("era", "unknown"),
                "n_numerals": len(poem_numerals),
                "n_tokens": len(clean_tokens),
                "avg_numeral_s2": sum(r["s2"] for r in poem_numerals) / len(poem_numerals),
                "max_numeral_s2": max(r["s2"] for r in poem_numerals),
                "numerals": poem_numerals,
            })

    # ── Summary statistics ────────────────────────────────────────────────────
    def stats(recs):
        if not recs:
            return {"n": 0, "mean_s2": None, "median_s2": None, "pos_pct": None, "max_s2": None}
        s2s = sorted(r["s2"] for r in recs)
        n = len(s2s)
        pos = sum(1 for s in s2s if s > 0)
        return {
            "n": n,
            "mean_s2": sum(s2s) / n,
            "median_s2": s2s[n // 2],
            "pos_pct": pos / n * 100,
            "max_s2": max(s2s),
        }

    # Baseline: all non-numeral, non-approximate alphabetic tokens
    baseline_tokens = [
        t for t in all_tokens
        if t["category"] is None
        and re.match(r'^[a-zA-Z]+$', t["token"])
        and len(t["token"]) > 2
    ]

    digit_recs = [t for t in numeral_tokens if t["category"] == "digit"]
    cardinal_recs = [t for t in numeral_tokens if t["category"] == "cardinal"]
    ordinal_recs = [t for t in numeral_tokens if t["category"] == "ordinal"]

    categories = {
        "Digit (e.g. 1, 42, 1984)": digit_recs,
        "Cardinal word (one, two, hundred)": cardinal_recs,
        "Ordinal word (first, second, twice)": ordinal_recs,
        "Approximate (many, few, some)": approx_tokens,
        "Baseline (other alphabetic content words)": baseline_tokens,
    }

    print("=" * 70)
    print("NUMERALS IN POETRY: S₂ ANALYSIS")
    print("=" * 70)
    print()
    print("─── 1. Overall S₂ by numeral category ────────────────────────────────")
    print(f"{'Category':<40} {'n':>5}  {'mean S₂':>8}  {'median S₂':>10}  {'pos%':>6}  {'max S₂':>8}")
    print("-" * 82)
    for cat, recs in categories.items():
        s = stats(recs)
        if s["n"] == 0:
            print(f"{cat:<40} {'0':>5}  {'n/a':>8}")
        else:
            print(f"{cat:<40} {s['n']:>5}  {s['mean_s2']:>8.3f}  {s['median_s2']:>10.3f}  {s['pos_pct']:>6.1f}%  {s['max_s2']:>8.2f}")

    # ── What did GPT-2 expect? ─────────────────────────────────────────────────
    print()
    print("─── 2. What GPT-2 expected when poets wrote numerals ─────────────────")
    print("  (Top alternative predictions at high-S₂ numeral moments)")
    print()

    high_s2_numerals = sorted(numeral_tokens, key=lambda r: -r["s2"])[:25]
    for r in high_s2_numerals:
        top_alt = r["alternatives"][0]["token"].strip() if r["alternatives"] else "?"
        top_prob = r["alternatives"][0]["prob"] if r["alternatives"] else 0
        ctx = r["context_before"][-40:] if len(r["context_before"]) > 40 else r["context_before"]
        print(f"  [{r['s2']:+.2f}]  '{r['token']}' (GPT-2 expected '{top_alt}' p={top_prob:.3f})")
        print(f"         context: '...{ctx}'  —  {r['author']}, \"{r['title']}\"")
        print()

    # ── Poems that use numerals most effectively ──────────────────────────────
    print("─── 3. Poems with highest average numeral S₂ ────────────────────────")
    poem_numeral_stats.sort(key=lambda p: -p["avg_numeral_s2"])
    print(f"{'Poem':<45} {'Auth':<20} {'n':>3}  {'avg S₂':>7}  {'max S₂':>8}")
    print("-" * 90)
    for p in poem_numeral_stats[:15]:
        title_short = p["title"][:43]
        auth_short = p["author"][:18]
        print(f"{title_short:<45} {auth_short:<20} {p['n_numerals']:>3}  {p['avg_numeral_s2']:>7.3f}  {p['max_numeral_s2']:>8.2f}")

    # ── Digit vs. word: individual instances ──────────────────────────────────
    print()
    print("─── 4. All digit tokens (exact numerals) ─────────────────────────────")
    digit_recs_sorted = sorted(digit_recs, key=lambda r: -r["s2"])
    for r in digit_recs_sorted[:20]:
        print(f"  '{r['token']:>6}'  S₂={r['s2']:+.2f}  ctx: '...{r['context_before'][-30:]}'  {r['author']}")

    # ── The "counting" moment: cardinal words with their context ───────────────
    print()
    print("─── 5. High-S₂ cardinal words in context ─────────────────────────────")
    high_card = sorted(cardinal_recs, key=lambda r: -r["s2"])[:15]
    for r in high_card:
        top_alt = r["alternatives"][0]["token"].strip() if r["alternatives"] else "?"
        ctx = r["context_before"][-50:] if len(r["context_before"]) > 50 else r["context_before"]
        print(f"  S₂={r['s2']:+.2f}  '{r['token']}'  (vs GPT-2's '{top_alt}')")
        print(f"    ctx: '...{ctx}' — {r['author']}, \"{r['title']}\"")
        print()

    # ── Era breakdown ──────────────────────────────────────────────────────────
    print("─── 6. Numeral S₂ by era ─────────────────────────────────────────────")
    by_era = defaultdict(list)
    for r in numeral_tokens:
        by_era[r["era"]].append(r["s2"])

    era_stats = []
    for era, s2s in by_era.items():
        n = len(s2s)
        mean = sum(s2s) / n
        era_stats.append((era, n, mean))
    era_stats.sort(key=lambda x: -x[2])

    print(f"{'Era':<30} {'n':>4}  {'mean S₂':>8}")
    print("-" * 48)
    for era, n, mean in era_stats:
        print(f"{era:<30} {n:>4}  {mean:>8.3f}")

    # ── Save results ───────────────────────────────────────────────────────────
    results = {
        "by_category": {},
        "high_s2_numerals": [
            {
                "token": r["token"],
                "s2": r["s2"],
                "category": r["category"],
                "top_expected": r["alternatives"][0]["token"].strip() if r["alternatives"] else "",
                "top_expected_prob": r["alternatives"][0]["prob"] if r["alternatives"] else 0,
                "context_before": r["context_before"][-60:],
                "author": r["author"],
                "title": r["title"],
            }
            for r in high_s2_numerals
        ],
        "top_numeral_poems": [
            {
                "title": p["title"],
                "author": p["author"],
                "era": p["era"],
                "n_numerals": p["n_numerals"],
                "avg_numeral_s2": round(p["avg_numeral_s2"], 4),
                "max_numeral_s2": round(p["max_numeral_s2"], 4),
            }
            for p in poem_numeral_stats[:20]
        ],
    }
    for cat, recs in categories.items():
        s = stats(recs)
        results["by_category"][cat] = s

    import os
    os.makedirs("findings", exist_ok=True)
    with open("findings/numerals_s2_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print()
    print("Results saved to findings/numerals_s2_results.json")


if __name__ == "__main__":
    main()
