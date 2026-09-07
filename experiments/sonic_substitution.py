"""
Sonic Substitution Analysis

When a poet makes a high-S₂ choice, does the chosen word sound/look similar
to what GPT-2 predicted? Do poets substitute unexpected words that nonetheless
resemble the "expected" word in form?

Metrics:
  - char_sim: character-level similarity (SequenceMatcher ratio)
  - suffix_overlap: shared ending characters (captures rhyme-like similarity)
  - prefix_overlap: shared leading characters
  - "defection ratio": P(actual) / P(top_prediction)

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import math
import re
from collections import defaultdict
from difflib import SequenceMatcher


RESULT_PATH = "results/corpus_results.json"
S2_HIGH_THRESHOLD = 2.0
S2_LOW_THRESHOLD = -2.0
TOP_CHAR_SIM_THRESHOLD = 0.6  # "phonetically similar" cutoff


def normalize(tok: str) -> str:
    return tok.strip().lower()


def char_similarity(a: str, b: str) -> float:
    a, b = normalize(a), normalize(b)
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def suffix_overlap(a: str, b: str, n: int = 3) -> int:
    """Count shared trailing n characters."""
    a, b = normalize(a), normalize(b)
    count = 0
    for i in range(1, min(n + 1, min(len(a), len(b)) + 1)):
        if a[-i] == b[-i]:
            count += 1
        else:
            break
    return count


def prefix_overlap(a: str, b: str, n: int = 3) -> int:
    """Count shared leading n characters."""
    a, b = normalize(a), normalize(b)
    count = 0
    for i in range(min(n, min(len(a), len(b)))):
        if a[i] == b[i]:
            count += 1
        else:
            break
    return count


def is_alpha(tok: str) -> bool:
    return bool(re.search(r"[a-zA-Z]", tok))


def analyze():
    with open(RESULT_PATH) as f:
        corpus = json.load(f)

    # Filter to English poems only
    corpus = [p for p in corpus if p["metadata"].get("language", "en") == "en"]

    # Collect token records for analysis
    all_tokens = []
    for poem in corpus:
        meta = poem["metadata"]
        for tok in poem["tokens"]:
            if not tok["alternatives"]:
                continue
            actual = tok["token"]
            top_pred = tok["alternatives"][0]["token"]
            # Only analyze alphabetic tokens of meaningful length
            if not is_alpha(actual) or not is_alpha(top_pred):
                continue
            if len(normalize(actual)) < 2 or len(normalize(top_pred)) < 2:
                continue

            top_prob = tok["alternatives"][0]["prob"]
            actual_prob = tok["prob"]
            defection_ratio = actual_prob / top_prob if top_prob > 0 else 0.0

            cs = char_similarity(actual, top_pred)
            suf = suffix_overlap(actual, top_pred, n=3)
            pre = prefix_overlap(actual, top_pred, n=3)

            # Best similarity among all top-10 alternatives
            best_cs = max(char_similarity(actual, alt["token"]) for alt in tok["alternatives"])
            best_cs_token = max(
                tok["alternatives"],
                key=lambda a: char_similarity(actual, a["token"])
            )["token"]

            all_tokens.append({
                "poem_title": meta["title"],
                "author": meta["author"],
                "era": meta["era"],
                "year": meta.get("year"),
                "token": actual,
                "top_pred": top_pred,
                "s2": tok["s2"],
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "rank": tok["rank"],
                "defection_ratio": round(defection_ratio, 6),
                "char_sim": round(cs, 4),
                "best_char_sim": round(best_cs, 4),
                "best_cs_token": best_cs_token,
                "suffix_overlap": suf,
                "prefix_overlap": pre,
            })

    # ── Analysis ──────────────────────────────────────────────────────────────

    # Split into high-S2, low-S2, and middle groups
    high_s2 = [t for t in all_tokens if t["s2"] >= S2_HIGH_THRESHOLD]
    low_s2  = [t for t in all_tokens if t["s2"] <= S2_LOW_THRESHOLD]
    mid_s2  = [t for t in all_tokens if S2_LOW_THRESHOLD < t["s2"] < S2_HIGH_THRESHOLD]

    def avg(lst, key):
        vals = [x[key] for x in lst if x[key] is not None]
        return sum(vals) / len(vals) if vals else 0.0

    def pct_above(lst, key, threshold):
        vals = [x[key] for x in lst]
        return 100 * sum(1 for v in vals if v >= threshold) / len(vals) if vals else 0.0

    print("=" * 70)
    print("SONIC SUBSTITUTION ANALYSIS")
    print("=" * 70)
    print(f"\nTotal alphabetic token pairs analyzed: {len(all_tokens)}")
    print(f"  High S₂ (≥ {S2_HIGH_THRESHOLD}):  {len(high_s2)}")
    print(f"  Mid S₂:             {len(mid_s2)}")
    print(f"  Low S₂ (≤ {S2_LOW_THRESHOLD}): {len(low_s2)}")

    print("\n── 1. MEAN SIMILARITY BY S2 GROUP ─────────────────────────────────")
    print(f"{'Group':<12} {'n':>5} {'Char sim':>10} {'Best CS':>10} {'Sfx ovlp':>10} {'Pfx ovlp':>10} {'Def ratio':>10}")
    for label, group in [("High S₂", high_s2), ("Mid S₂", mid_s2), ("Low S₂", low_s2)]:
        print(
            f"{label:<12} {len(group):>5} "
            f"{avg(group,'char_sim'):>10.4f} "
            f"{avg(group,'best_char_sim'):>10.4f} "
            f"{avg(group,'suffix_overlap'):>10.4f} "
            f"{avg(group,'prefix_overlap'):>10.4f} "
            f"{avg(group,'defection_ratio'):>10.6f}"
        )

    print("\n── 2. % OF HIGH-S₂ CHOICES WITH CHAR SIM ≥ 0.6 (similar-sounding) ─")
    for label, group in [("High S₂", high_s2), ("Mid S₂", mid_s2), ("Low S₂", low_s2)]:
        pct = pct_above(group, "char_sim", TOP_CHAR_SIM_THRESHOLD)
        pct_best = pct_above(group, "best_char_sim", TOP_CHAR_SIM_THRESHOLD)
        print(f"  {label:<10}: {pct:5.1f}% match top pred  |  {pct_best:5.1f}% match any top-10")

    # ── 3. Top examples of "sonic substitution" (high S2 + high char_sim) ─────
    sonic_subs = sorted(
        [t for t in high_s2 if t["char_sim"] >= 0.5],
        key=lambda x: x["s2"],
        reverse=True
    )[:20]

    print("\n── 3. TOP SONIC SUBSTITUTIONS (high S₂ + char_sim ≥ 0.5) ──────────")
    print(f"{'Token':<16} {'Predicted':<16} {'S₂':>7} {'CS':>7} {'Poem':<35}")
    for t in sonic_subs:
        print(
            f"{repr(t['token']):<16} {repr(t['top_pred']):<16} "
            f"{t['s2']:>7.2f} {t['char_sim']:>7.4f} {t['poem_title'][:34]}"
        )

    # ── 4. Era breakdown: which eras show most sonic substitution? ─────────────
    print("\n── 4. ERA BREAKDOWN (high-S₂ tokens: char_sim ≥ 0.5) ────────────────")
    era_stats = defaultdict(list)
    for t in high_s2:
        era_stats[t["era"]].append(t)

    era_rows = []
    for era, tokens in era_stats.items():
        n = len(tokens)
        mean_cs = avg(tokens, "char_sim")
        pct_sonic = pct_above(tokens, "char_sim", 0.5)
        era_rows.append((era, n, mean_cs, pct_sonic))

    era_rows.sort(key=lambda x: x[3], reverse=True)
    print(f"{'Era':<22} {'n':>5} {'Mean CS':>9} {'%Sonic':>8}")
    for era, n, mean_cs, pct_sonic in era_rows:
        print(f"{era:<22} {n:>5} {mean_cs:>9.4f} {pct_sonic:>8.1f}%")

    # ── 5. Most "defected" high-S₂ moments (low defection ratio = far from top) ─
    print("\n── 5. MOST EXTREME DEFECTIONS (high S₂, lowest defection ratio) ────")
    radical = sorted(high_s2, key=lambda x: x["defection_ratio"])[:15]
    print(f"{'Token':<16} {'Predicted':<16} {'S₂':>7} {'DefRatio':>10} {'Poem':<35}")
    for t in radical:
        print(
            f"{repr(t['token']):<16} {repr(t['top_pred']):<16} "
            f"{t['s2']:>7.2f} {t['defection_ratio']:>10.6f} {t['poem_title'][:34]}"
        )

    # ── 6. Quasi-rhyme substitution: high suffix overlap + high S₂ ────────────
    quasi_rhyme = sorted(
        [t for t in high_s2 if t["suffix_overlap"] >= 2],
        key=lambda x: x["s2"],
        reverse=True
    )[:15]

    print("\n── 6. QUASI-RHYME SUBSTITUTIONS (suffix_overlap ≥ 2 + high S₂) ───")
    print(f"{'Token':<16} {'Predicted':<16} {'S₂':>7} {'SufOvlp':>9} {'Poem':<35}")
    for t in quasi_rhyme:
        print(
            f"{repr(t['token']):<16} {repr(t['top_pred']):<16} "
            f"{t['s2']:>7.2f} {t['suffix_overlap']:>9} {t['poem_title'][:34]}"
        )

    # ── 7. Correlation: S₂ vs char_sim ────────────────────────────────────────
    # Pearson r between s2 and char_sim across all alpha tokens
    xs = [t["s2"] for t in all_tokens]
    ys = [t["char_sim"] for t in all_tokens]
    n = len(xs)
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x - mx)*(y - my) for x, y in zip(xs, ys)) / n
    sdx = math.sqrt(sum((x - mx)**2 for x in xs) / n)
    sdy = math.sqrt(sum((y - my)**2 for y in ys) / n)
    r = cov / (sdx * sdy) if sdx * sdy > 0 else 0.0

    print(f"\n── 7. CORRELATION: S₂ vs char_sim (Pearson r) ──────────────────────")
    print(f"  r = {r:.4f}  (n = {n})")
    if r > 0.05:
        print("  → Positive: higher S₂ tokens tend to resemble their top prediction more")
    elif r < -0.05:
        print("  → Negative: higher S₂ tokens tend to differ from their top prediction more")
    else:
        print("  → Near zero: no strong linear relationship")

    # S₂ vs defection ratio
    xs = [t["s2"] for t in all_tokens]
    ys = [t["defection_ratio"] for t in all_tokens]
    mx, my = sum(xs)/n, sum(ys)/n
    cov = sum((x - mx)*(y - my) for x, y in zip(xs, ys)) / n
    sdx = math.sqrt(sum((x - mx)**2 for x in xs) / n)
    sdy = math.sqrt(sum((y - my)**2 for y in ys) / n)
    r2 = cov / (sdx * sdy) if sdx * sdy > 0 else 0.0
    print(f"\n  S₂ vs defection_ratio: r = {r2:.4f}")
    print("  (defection ratio = P(actual)/P(top_pred); 1 = chose most likely, 0 = maximally deviant)")

    print("\n── 8. POET SONIC SIGNATURE ─────────────────────────────────────────")
    poet_stats = defaultdict(list)
    for t in high_s2:
        poet_stats[t["author"]].append(t)

    poet_rows = []
    for poet, tokens in poet_stats.items():
        if len(tokens) < 5:
            continue
        mean_cs = avg(tokens, "char_sim")
        pct_sonic = pct_above(tokens, "char_sim", 0.5)
        mean_def = avg(tokens, "defection_ratio")
        poet_rows.append((poet, len(tokens), mean_cs, pct_sonic, mean_def))

    poet_rows.sort(key=lambda x: x[3], reverse=True)
    print(f"{'Poet':<25} {'n':>5} {'Mean CS':>9} {'%Sonic':>8} {'Mean DefR':>11}")
    for poet, n, mean_cs, pct_sonic, mean_def in poet_rows:
        print(f"{poet:<25} {n:>5} {mean_cs:>9.4f} {pct_sonic:>8.1f}% {mean_def:>11.6f}")

    return {
        "all_tokens": all_tokens,
        "high_s2": high_s2,
        "low_s2": low_s2,
        "sonic_subs": sonic_subs,
        "r_s2_cs": r,
        "r_s2_def": r2,
    }


if __name__ == "__main__":
    results = analyze()
