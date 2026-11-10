"""
Shadow Lag Analysis
====================
Extends shadow_vocab_fulfillment.py by adding TIMING information:
When a poem fulfills its shadow word, HOW MANY TOKENS later does it appear?

For each suppressed content-word prediction (top-1 alternative at each token),
if the word eventually appears in the poem:
  - shadow_lag = first_appearance_position - suppression_position

Metrics:
  - Lag distribution per era / poet
  - Early (lag < 10), medium (10–50), late (50+) fulfillment rates
  - Lag at high-S2 positions vs. low-S2 positions
  - Does high-S2 mean DELAYED gratification, or does it mean the shadow
    word never comes at all?

Hypothesis: Surprising poems (high avg_S2) will have *longer* lags —
the shadow word arrives later (or never). "Quick" poems fulfill their
shadows almost immediately; "slow" poems defer or evade entirely.
"""

import json
import re
import math
import statistics
from collections import defaultdict


def mean(xs):
    return sum(xs) / len(xs) if xs else None


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return None
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/shadow_lag.json"

FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "it", "its", "i", "my", "me",
    "you", "your", "he", "she", "they", "we", "us", "him", "her", "them",
    "that", "this", "these", "those", "not", "no", "as", "if", "then",
    "than", "so", "yet", "also", "just", "even", "still", "only", "about",
    "into", "up", "out", "down", "off", "over", "under", "through",
    ".", ",", "!", "?", ";", ":", "'", '"', "-", "--", "...",
    "\n", " ",
}

P_NEWLINE_THRESHOLD = 0.9
S2_HIGH_THRESHOLD = 2.0

LAG_EARLY = 10    # within 10 tokens = "immediate" fulfillment
LAG_MEDIUM = 50   # 10–50 tokens = "medium" fulfillment
# 50+ = "late" fulfillment


def normalize(tok: str) -> str:
    return tok.strip().lower()


def is_content(tok: str) -> bool:
    t = normalize(tok)
    if not t or not t[0].isalpha():
        return False
    return t not in FUNCTION_WORDS and len(t) > 2


def analyze_poem(poem: dict):
    tokens = poem.get("tokens", [])
    meta = poem.get("metadata", {})
    if not tokens:
        return None

    n = len(tokens)
    # Build actual token positions: normalized word -> list of positions
    actual_positions = defaultdict(list)
    for i, tok in enumerate(tokens):
        word = normalize(tok["token"])
        actual_positions[word].append(i)

    # For each position, record the shadow word (top-1 content alternative)
    # and compute lag if it appears later
    lag_records = []  # (s2, lag_or_None, is_high_s2)
    early_count = medium_count = late_count = evaded_count = 0
    all_lags = []

    for i, tok in enumerate(tokens):
        # Skip stanza-break artifacts
        if tok.get("p_newline", 0) >= P_NEWLINE_THRESHOLD:
            continue

        alts = tok.get("alternatives", [])
        if not alts:
            continue

        # Find top-1 content word alternative
        shadow_word = None
        for alt in alts[:5]:  # check top-5 for first content word
            w = normalize(alt["token"])
            if is_content(w):
                shadow_word = w
                break

        if not shadow_word:
            continue

        # Is the shadow word used by the poet at all?
        positions = actual_positions.get(shadow_word, [])
        # Find first occurrence AFTER current position
        later_positions = [p for p in positions if p > i]

        s2 = tok.get("s2", 0.0)
        is_high = s2 >= S2_HIGH_THRESHOLD

        if later_positions:
            lag = later_positions[0] - i
            all_lags.append(lag)
            if lag <= LAG_EARLY:
                early_count += 1
            elif lag <= LAG_MEDIUM:
                medium_count += 1
            else:
                late_count += 1
            lag_records.append({"position": i, "s2": s2, "shadow": shadow_word,
                                 "lag": lag, "is_high_s2": is_high})
        else:
            evaded_count += 1
            lag_records.append({"position": i, "s2": s2, "shadow": shadow_word,
                                 "lag": None, "is_high_s2": is_high})

    total = early_count + medium_count + late_count + evaded_count
    if total == 0:
        return None

    # Separate lag stats for high-S2 vs low-S2 positions
    high_lags = [r["lag"] for r in lag_records if r["is_high_s2"] and r["lag"] is not None]
    low_lags  = [r["lag"] for r in lag_records if not r["is_high_s2"] and r["lag"] is not None]

    return {
        "title": meta.get("title", "?"),
        "author": meta.get("author", "?"),
        "era": meta.get("era", "?"),
        "year": meta.get("year"),
        "avg_s2": poem["summary"]["avg_s2"],
        "n_tokens": n,
        "total_suppressions": total,
        "early_count": early_count,
        "medium_count": medium_count,
        "late_count": late_count,
        "evaded_count": evaded_count,
        "fulfillment_rate": (early_count + medium_count + late_count) / total,
        "early_rate": early_count / total,
        "medium_rate": medium_count / total,
        "late_rate": late_count / total,
        "evasion_rate": evaded_count / total,
        "mean_lag": mean(all_lags) if all_lags else None,
        "median_lag": statistics.median(all_lags) if all_lags else None,
        "mean_lag_high_s2": mean(high_lags) if high_lags else None,
        "mean_lag_low_s2": mean(low_lags) if low_lags else None,
        "lag_diff_high_minus_low": (
            mean(high_lags) - mean(low_lags)
            if high_lags and low_lags else None
        ),
    }


def era_stats(poems):
    """Aggregate poem-level stats into era-level stats."""
    by_era = defaultdict(list)
    for p in poems:
        by_era[p["era"]].append(p)

    result = {}
    for era, plist in by_era.items():
        mean_lag = [p["mean_lag"] for p in plist if p["mean_lag"] is not None]
        evasion  = [p["evasion_rate"] for p in plist]
        early    = [p["early_rate"] for p in plist]
        late     = [p["late_rate"] for p in plist]
        avg_s2   = [p["avg_s2"] for p in plist]
        lag_diff = [p["lag_diff_high_minus_low"] for p in plist
                    if p["lag_diff_high_minus_low"] is not None]
        result[era] = {
            "n": len(plist),
            "mean_lag": mean(mean_lag) if mean_lag else None,
            "mean_evasion_rate": mean(evasion),
            "mean_early_rate": mean(early),
            "mean_late_rate": mean(late),
            "mean_avg_s2": mean(avg_s2),
            "mean_lag_diff_high_vs_low": mean(lag_diff) if lag_diff else None,
        }
    return result


def main():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    poems = []
    for poem in corpus:
        result = analyze_poem(poem)
        if result:
            poems.append(result)

    # Correlation: avg_s2 vs mean_lag
    s2_vals  = [p["avg_s2"] for p in poems if p["mean_lag"] is not None]
    lag_vals = [p["mean_lag"] for p in poems if p["mean_lag"] is not None]
    corr_s2_lag = pearson(s2_vals, lag_vals)

    s2_ev = [p["avg_s2"] for p in poems]
    ev_ev = [p["evasion_rate"] for p in poems]
    corr_s2_evasion = pearson(s2_ev, ev_ev)

    # High-S2 lag vs low-S2 lag (global)
    all_lag_diff = [p["lag_diff_high_minus_low"] for p in poems
                    if p["lag_diff_high_minus_low"] is not None]

    lag_global = [p["mean_lag"] for p in poems if p["mean_lag"] is not None]
    global_stats = {
        "poems_analyzed": len(poems),
        "mean_lag_global": mean(lag_global) if lag_global else None,
        "median_lag_global": statistics.median(lag_global) if lag_global else None,
        "mean_evasion_rate": mean([p["evasion_rate"] for p in poems]),
        "mean_early_rate": mean([p["early_rate"] for p in poems]),
        "mean_late_rate": mean([p["late_rate"] for p in poems]),
        "corr_s2_lag": corr_s2_lag,
        "corr_s2_evasion": corr_s2_evasion,
        "mean_lag_diff_high_vs_low": (mean(all_lag_diff) if all_lag_diff else None),
    }

    era_breakdown = era_stats(poems)

    # Top-10 poems with longest mean lag (slow fulfillment)
    top_slow = sorted([p for p in poems if p["mean_lag"] is not None],
                      key=lambda x: x["mean_lag"], reverse=True)[:10]
    # Top-10 poems with highest evasion (least fulfillment)
    top_evasion = sorted(poems, key=lambda x: x["evasion_rate"], reverse=True)[:10]
    # Top-10 poems with highest lag-diff (high-S2 moments are much slower)
    top_lag_diff = sorted([p for p in poems if p["lag_diff_high_minus_low"] is not None],
                          key=lambda x: x["lag_diff_high_minus_low"], reverse=True)[:10]

    output = {
        "global_stats": global_stats,
        "era_breakdown": era_breakdown,
        "top_slow_poems": top_slow,
        "top_evasion_poems": top_evasion,
        "top_lag_diff_poems": top_lag_diff,
        "poems": poems,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Analyzed {len(poems)} poems")
    print(f"Global mean lag: {global_stats['mean_lag_global']:.1f} tokens")
    print(f"Mean evasion rate: {global_stats['mean_evasion_rate']:.3f}")
    print(f"Corr(avg_S2, mean_lag): {corr_s2_lag:.3f}" if corr_s2_lag else "Corr: N/A")
    print(f"Corr(avg_S2, evasion): {corr_s2_evasion:.3f}" if corr_s2_evasion else "Corr: N/A")
    print(f"Mean lag diff (high-S2 vs low-S2): {global_stats['mean_lag_diff_high_vs_low']:.1f}"
          if global_stats["mean_lag_diff_high_vs_low"] else "Lag diff: N/A")


if __name__ == "__main__":
    main()
