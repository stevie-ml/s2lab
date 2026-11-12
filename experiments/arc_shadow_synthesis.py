"""
Arc Type × Shadow Fulfillment Synthesis
=========================================
Synthesizes two recent findings:
  1. S2 Arc Typology (findings/s2_arc_typology.md): poems classified by their
     information curve shape (DECLINE, ASCENT, U_SHAPE, ARCH, FLAT).
  2. Shadow Vocabulary Fulfillment (findings/shadow_vocab_fulfillment.md): whether
     GPT-2's suppressed top-1 predictions eventually appear in the poem.

The key novel question: Does arc type PREDICT whether a poem's peak suppression
moment gets "redeemed"?

Hypotheses:
  DECLINE (peak in Q1): suppressed word has the full poem to appear in → high fulfillment
  ASCENT  (peak in Q4): suppressed at the end, little poem remains → low fulfillment
  U_SHAPE (peak in Q1 and Q4): split prediction
  ARCH    (peak in Q2/Q3): some remaining poem after peak → medium-high fulfillment
  FLAT    (no clear peak): baseline fulfillment

Additional question: At the PEAK suppression moment (highest artifact-free S2),
does the semantic category of the suppressed word (function vs content) differ by arc type?

Metrics per poem:
  - arc_type: from s2_arc_typology.json
  - peak_s2: highest artifact-free S2 in the poem
  - peak_position: normalized position (0=start, 1=end) of that peak
  - peak_suppressed: GPT-2's top-1 prediction at peak position
  - peak_suppressed_category: function/content/punctuation/contraction
  - post_peak_fulfillment: does the suppressed word appear AFTER the peak?
  - whole_poem_fulfillment: does it appear anywhere in the poem?
  - remaining_poem_fraction: fraction of tokens remaining after the peak

Builds on:
  findings/s2_arc_typology.md
  findings/shadow_vocab_fulfillment.md
  findings/straussian_extremes_taxonomy.md
"""

import json
import re
from collections import defaultdict

ARC_TYPOLOGY_PATH  = "results/s2_arc_typology.json"
CORPUS_PATH        = "results/corpus_results.json"
OUTPUT_PATH        = "results/arc_shadow_synthesis.json"

P_NEWLINE_THRESHOLD = 0.9

FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "it", "its", "i", "my", "me",
    "you", "your", "he", "she", "they", "we", "us", "him", "her", "them",
    "that", "this", "these", "those", "not", "no", "as", "if", "then",
    "than", "so", "yet", "also", "just", "even", "still", "only", "about",
    "into", "up", "out", "down", "off", "over", "under", "through",
}

PUNCTUATION = {".", ",", "!", "?", ";", ":", "'", '"', "-", "--", "...", "\n", " "}

CONTRACTIONS = {"'s", "'t", "'ll", "'ve", "'d", "'re", "'m", "n't"}


def normalize(tok: str) -> str:
    return tok.strip().lower()


def categorize_token(tok: str) -> str:
    t = normalize(tok)
    if not t:
        return "empty"
    if t in CONTRACTIONS or tok in CONTRACTIONS:
        return "contraction"
    if t in PUNCTUATION or not any(c.isalpha() for c in t):
        return "punctuation"
    if t in FUNCTION_WORDS:
        return "function_word"
    return "content_word"


def is_content(tok: str) -> bool:
    return categorize_token(tok) == "content_word"


def clean_tokens(tokens):
    """Filter out stanza-break artifact positions."""
    return [t for t in tokens if t.get("p_newline", 0) < P_NEWLINE_THRESHOLD]


def get_top_alternative(token_data):
    alts = token_data.get("alternatives", [])
    if alts:
        return alts[0]["token"]
    return None


def main():
    with open(ARC_TYPOLOGY_PATH) as f:
        arc_data = json.load(f)
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Build lookup: (title, author) -> arc type
    arc_lookup = {}
    for p in arc_data["poems"]:
        key = (p["title"], p["author"])
        arc_lookup[key] = p["arc"]

    results = []
    arc_stats = defaultdict(lambda: {
        "n": 0,
        "post_peak_fulfillments": 0,
        "whole_poem_fulfillments": 0,
        "peak_positions": [],
        "peak_s2s": [],
        "remaining_fractions": [],
        "suppressed_categories": defaultdict(int),
        "suppressed_is_content": 0,
    })

    for poem in corpus:
        meta   = poem["metadata"]
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        key = (meta["title"], meta["author"])
        arc = arc_lookup.get(key)
        if arc is None:
            continue  # poem not in arc typology (too short)

        clean = clean_tokens(tokens)
        if not clean:
            continue

        # Find peak artifact-free S2 position (index in ORIGINAL tokens list)
        best_s2 = -999
        best_idx = None
        for i, t in enumerate(tokens):
            if t.get("p_newline", 0) >= P_NEWLINE_THRESHOLD:
                continue
            if t["s2"] > best_s2:
                best_s2 = t["s2"]
                best_idx = i

        if best_idx is None:
            continue

        total_tokens = len(tokens)
        peak_pos_norm = best_idx / max(total_tokens - 1, 1)
        suppressed = get_top_alternative(tokens[best_idx])

        if suppressed is None:
            continue

        suppressed_cat = categorize_token(suppressed)
        suppressed_norm = normalize(suppressed)

        # Check fulfillment: does suppressed word appear AFTER the peak?
        tokens_after = tokens[best_idx + 1 :]
        words_after = {normalize(t["token"]) for t in tokens_after}
        post_peak_fulfilled = suppressed_norm in words_after

        # Check fulfillment: does it appear ANYWHERE in the poem?
        all_words = {normalize(t["token"]) for t in tokens}
        whole_poem_fulfilled = suppressed_norm in all_words

        remaining_fraction = len(tokens_after) / max(total_tokens, 1)

        # Only count content-word suppressions for semantic analysis
        # (function word suppressions are less informative)
        result = {
            "title": meta["title"],
            "author": meta["author"],
            "era": meta.get("era", "unknown"),
            "arc": arc,
            "peak_s2": round(best_s2, 3),
            "peak_position_norm": round(peak_pos_norm, 3),
            "suppressed": suppressed,
            "suppressed_category": suppressed_cat,
            "post_peak_fulfilled": post_peak_fulfilled,
            "whole_poem_fulfilled": whole_poem_fulfilled,
            "remaining_fraction": round(remaining_fraction, 3),
        }
        results.append(result)

        st = arc_stats[arc]
        st["n"] += 1
        if post_peak_fulfilled:
            st["post_peak_fulfillments"] += 1
        if whole_poem_fulfilled:
            st["whole_poem_fulfillments"] += 1
        st["peak_positions"].append(peak_pos_norm)
        st["peak_s2s"].append(best_s2)
        st["remaining_fractions"].append(remaining_fraction)
        st["suppressed_categories"][suppressed_cat] += 1
        if suppressed_cat == "content_word":
            st["suppressed_is_content"] += 1

    # Compute summary statistics per arc type
    summary = {}
    for arc, st in arc_stats.items():
        n = st["n"]
        if n == 0:
            continue
        summary[arc] = {
            "n": n,
            "post_peak_fulfillment_rate": round(st["post_peak_fulfillments"] / n, 3),
            "whole_poem_fulfillment_rate": round(st["whole_poem_fulfillments"] / n, 3),
            "mean_peak_position": round(sum(st["peak_positions"]) / n, 3),
            "mean_peak_s2": round(sum(st["peak_s2s"]) / n, 3),
            "mean_remaining_fraction": round(sum(st["remaining_fractions"]) / n, 3),
            "suppressed_categories": dict(st["suppressed_categories"]),
            "suppressed_content_pct": round(
                100 * st["suppressed_is_content"] / n, 1
            ),
        }

    # Compute overall stats for comparison
    n_total = len(results)
    overall_post = sum(1 for r in results if r["post_peak_fulfilled"]) / max(n_total, 1)
    overall_whole = sum(1 for r in results if r["whole_poem_fulfilled"]) / max(n_total, 1)

    output = {
        "total_poems": n_total,
        "overall_post_peak_fulfillment": round(overall_post, 3),
        "overall_whole_poem_fulfillment": round(overall_whole, 3),
        "arc_summary": summary,
        "poems": results,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Analyzed {n_total} poems with arc classifications.")
    print(f"Overall post-peak fulfillment: {overall_post:.1%}")
    print(f"Overall whole-poem fulfillment: {overall_whole:.1%}")
    print()
    print(f"{'Arc':<10} {'n':>4} {'PostPeak%':>10} {'WholePm%':>10} {'MeanPeakPos':>12} {'MeanRem%':>10}")
    for arc, s in sorted(summary.items(), key=lambda x: -x[1]["post_peak_fulfillment_rate"]):
        print(f"{arc:<10} {s['n']:>4} {s['post_peak_fulfillment_rate']:>10.1%} "
              f"{s['whole_poem_fulfillment_rate']:>10.1%} "
              f"{s['mean_peak_position']:>12.3f} "
              f"{s['mean_remaining_fraction']:>10.1%}")

    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
