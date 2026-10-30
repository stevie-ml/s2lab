"""
Hyperbaton and S₂: Does syntactic inversion elevate surprisal?

Hyperbaton (deliberate word-order inversion) is a classical rhetorical device
common in formal and older poetry. This experiment tests whether displaced words
— moved from their canonical position — show higher S₂ than the same word in
its expected syntactic slot.

Method:
  1. Controlled pairs of sentences: canonical vs. inverted order.
  2. Compute S₂ at the displaced token in each version.
  3. Measure the "inversion premium" = S₂(inverted position) - S₂(canonical position).
  4. Scan the corpus for lines that likely contain inversions (adjective after noun,
     verb before subject at line start) and measure their S₂ profiles.
"""

import sys
import os
import json
import math
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine import analyze_poem

# ── Controlled sentence pairs ──────────────────────────────────────────────────
# Format: (label, canonical_sentence, inverted_sentence, displaced_word)
# 'displaced_word' is the token we compare across conditions.
#
# Note: GPT-2 cannot compute surprisal for token-0 (no prior context).
# Pairs where inversion places the target word at position 0 use a brief
# context prefix (after "||") so it has left context in both conditions.

PAIRS = [
    # Adjective-noun inversion (postpositive adjective)
    ("adj-noun: raven black",
     "The night was still when I saw the black raven fly.",
     "The night was still when I saw the raven black fly.",
     "black"),

    # Object fronting — add "He said:" prefix so "Beauty" has context
    ("obj-front: beauty I have none",
     "He confessed: I have no beauty here.",
     "He confessed: beauty I have none here.",
     "beauty"),

    # Adverbial fronting — prefix gives "softly" context
    ("adv-front: softly she spoke",
     "In the hall she spoke softly at night.",
     "In the hall softly she spoke at night.",
     "softly"),

    # Verb-subject inversion after adverbial
    ("verb-subj: down fell the knight",
     "In the tournament the knight fell down.",
     "In the tournament down fell the knight.",
     "fell"),

    # Predicate fronting
    ("pred-front: great is the king",
     "Among all rulers the king is great.",
     "Among all rulers great is the king.",
     "great"),

    # Participial inversion (Milton-style) — prefix gives "said" context
    ("part-inv: said the poet",
     "At the feast the poet said, I saw the light.",
     "At the feast said the poet, I saw the light.",
     "said"),

    # Genitive inversion
    ("gen-inv: of winter the cold",
     "When the cold of winter settles in.",
     "When of winter the cold settles in.",
     "cold"),

    # Direct object fronting — prefix
    ("dobj-front: love alone I sought",
     "All my days I sought love alone.",
     "All my days love alone I sought.",
     "love"),

    # Keatsian adjective clusters
    ("keats-style: wild surmise",
     "He looked with a wild surmise upon the sea.",
     "He looked with a surmise wild upon the sea.",
     "wild"),

    # Miltonic inversion: object before subject
    ("milt-verb-last: him long endured",
     "The wife endured him long with patience.",
     "The wife him long endured with patience.",
     "endured"),

    # Adjective-noun inversion with color
    ("adj-post: the rose red",
     "He gave her the red rose at dawn.",
     "He gave her the rose red at dawn.",
     "red"),

    # Verb-final (SOV order in English inversion)
    ("sov: the words she spoke",
     "In the silence she spoke the words.",
     "In the silence the words she spoke.",
     "spoke"),
]


def find_token_s2(result, target_word):
    """Find the S₂ of the first token that contains target_word (case-insensitive)."""
    target_lower = target_word.lower().strip()
    for tok in result["tokens"]:
        if target_lower in tok["token"].lower():
            return tok["s2"], tok["surprisal"], tok["entropy"], tok["position"]
    return None, None, None, None


def find_token_rank(result, target_word):
    """Find the rank of the first token containing target_word."""
    target_lower = target_word.lower().strip()
    for tok in result["tokens"]:
        if target_lower in tok["token"].lower():
            return tok["rank"]
    return None


def run_pair(label, canonical, inverted, displaced_word):
    print(f"\n  Pair: {label}")
    print(f"    Canonical : {canonical}")
    print(f"    Inverted  : {inverted}")

    r_can = analyze_poem(canonical, title=f"canonical:{label}")
    r_inv = analyze_poem(inverted, title=f"inverted:{label}")

    s2_can, surp_can, ent_can, pos_can = find_token_s2(r_can, displaced_word)
    s2_inv, surp_inv, ent_inv, pos_inv = find_token_s2(r_inv, displaced_word)

    rank_can = find_token_rank(r_can, displaced_word)
    rank_inv = find_token_rank(r_inv, displaced_word)

    result = {
        "label": label,
        "canonical": canonical,
        "inverted": inverted,
        "displaced_word": displaced_word,
        "canonical_s2": s2_can,
        "inverted_s2": s2_inv,
        "inversion_premium": round(s2_inv - s2_can, 4) if s2_can is not None and s2_inv is not None else None,
        "canonical_surprisal": surp_can,
        "inverted_surprisal": surp_inv,
        "canonical_entropy": ent_can,
        "inverted_entropy": ent_inv,
        "canonical_rank": rank_can,
        "inverted_rank": rank_inv,
        "canonical_position": pos_can,
        "inverted_position": pos_inv,
    }

    premium = result["inversion_premium"]
    if s2_can is None or s2_inv is None:
        print(f"    WARNING: token '{displaced_word}' not found in one/both versions")
    else:
        print(f"    S₂ canonical={s2_can:.3f} | inverted={s2_inv:.3f} | premium={premium:+.3f}")
        print(f"    Rank canonical={rank_can} | inverted={rank_inv}")

    return result


def corpus_inversion_scan():
    """
    Scan corpus_results.json for lines with likely inversions.
    Heuristics: lines where an adjective follows a noun (postpositive)
    or where a verb appears before a pronoun subject at line start.
    """
    corpus_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               "results", "corpus_results.json")
    if not os.path.exists(corpus_path):
        print("  [corpus scan] corpus_results.json not found, skipping.")
        return []

    with open(corpus_path) as f:
        corpus = json.load(f)

    # Collect high-S₂ tokens at the VERY START of lines (position 1 or 2)
    # These are most likely to be the displaced element in a Miltonic inversion
    early_high_s2 = []

    for poem in corpus:
        title = poem.get("metadata", {}).get("title", "?")
        author = poem.get("metadata", {}).get("author", "?")
        tokens = poem.get("tokens", [])

        # Find tokens that are at position 1 or 2 (line starts) with high S₂
        for tok in tokens:
            if tok["s2"] > 3.0 and tok["position"] <= 3:
                early_high_s2.append({
                    "poem": title,
                    "author": author,
                    "token": tok["token"],
                    "s2": tok["s2"],
                    "surprisal": tok["surprisal"],
                    "entropy": tok["entropy"],
                    "rank": tok["rank"],
                    "alternatives": tok.get("alternatives", [])[:3],
                })

    # Also find tokens where the top alternative is "the" or "a" (article expected,
    # non-article chosen — strong indicator of subject/noun displacement)
    article_surprises = []
    for poem in corpus:
        title = poem.get("metadata", {}).get("title", "?")
        author = poem.get("metadata", {}).get("author", "?")
        tokens = poem.get("tokens", [])

        for tok in tokens:
            alts = tok.get("alternatives", [])
            if not alts:
                continue
            top_alt = alts[0]["token"].strip().lower()
            actual = tok["token"].strip().lower()
            # Top prediction was article/pronoun, poet chose adjective/verb/noun
            if top_alt in ("the", "a", "an", "i", "he", "she", "it") and \
               actual not in ("the", "a", "an", "i", "he", "she", "it", ",", ".", ";", ":", "!") and \
               tok["s2"] > 2.0:
                article_surprises.append({
                    "poem": title,
                    "author": author,
                    "token": tok["token"],
                    "top_predicted": alts[0]["token"],
                    "s2": tok["s2"],
                    "rank": tok["rank"],
                    "position": tok["position"],
                })

    return {
        "early_line_high_s2": sorted(early_high_s2, key=lambda x: x["s2"], reverse=True)[:20],
        "article_surprises": sorted(article_surprises, key=lambda x: x["s2"], reverse=True)[:20],
    }


def main():
    print("=" * 70)
    print("Hyperbaton and S₂: Syntactic Inversion Experiment")
    print("=" * 70)

    # Run controlled pairs
    pair_results = []
    for label, canonical, inverted, displaced in PAIRS:
        r = run_pair(label, canonical, inverted, displaced)
        pair_results.append(r)

    # Summary statistics
    premiums = [r["inversion_premium"] for r in pair_results if r["inversion_premium"] is not None]
    avg_premium = sum(premiums) / len(premiums) if premiums else 0
    pos_count = sum(1 for p in premiums if p > 0)

    print("\n" + "=" * 70)
    print("SUMMARY: Inversion Premium Statistics")
    print(f"  Pairs tested         : {len(pair_results)}")
    print(f"  Avg inversion premium: {avg_premium:+.3f} bits")
    print(f"  Positive premium     : {pos_count}/{len(premiums)} pairs")
    print(f"  Premiums by pair:")
    for r in pair_results:
        p = r["inversion_premium"]
        marker = "▲" if p and p > 0 else "▼"
        print(f"    {marker} {r['label']:35s} {p:+.3f}" if p is not None else f"    ? {r['label']}")

    # Corpus scan
    print("\nScanning corpus for likely inversion patterns...")
    corpus_scan = corpus_inversion_scan()

    print(f"\nEarly-line high-S₂ tokens (position ≤ 3, S₂ > 3.0):")
    for item in corpus_scan["early_line_high_s2"][:10]:
        print(f"  '{item['token']}' (S₂={item['s2']:.2f}) in '{item['poem']}' by {item['author']}")

    print(f"\nArticle-predicted, non-article chosen (likely displacement):")
    for item in corpus_scan["article_surprises"][:10]:
        print(f"  '{item['token']}' [predicted: '{item['top_predicted']}'] "
              f"S₂={item['s2']:.2f} in '{item['poem']}' by {item['author']}")

    # Save results
    output = {
        "experiment": "hyperbaton_s2",
        "description": "Syntactic inversion (hyperbaton) and its effect on S₂",
        "pair_results": pair_results,
        "summary": {
            "n_pairs": len(pair_results),
            "avg_inversion_premium": round(avg_premium, 4),
            "positive_premium_count": pos_count,
            "total_pairs": len(premiums),
            "all_premiums": premiums,
        },
        "corpus_scan": corpus_scan,
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "hyperbaton_s2.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return output


if __name__ == "__main__":
    main()
