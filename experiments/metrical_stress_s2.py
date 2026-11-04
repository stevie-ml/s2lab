#!/usr/bin/env python3.13
"""
Metrical Stress and S2: Does phonological stress correlate with surprisal?

Question: Do tokens at metrically STRESSED positions have higher or lower S2
than tokens at UNSTRESSED positions in formal iambic pentameter?

Three hypotheses:
  H1 (Semantic weight): Stressed syllables have HIGHER S2 — they carry
     semantic load, which requires choosing an unexpected word.
  H2 (Metrical predictability): Stressed positions have LOWER S2 — the meter
     creates a template that makes content words predictable.
  H3 (Independence): No correlation — phonology and information theory operate
     on separate levels.

Method:
1. Load token-level S2 data from corpus_results.json for sonnets/formal verse
2. For each token, reconstruct the word and look up stress pattern via CMU dict
3. Classify tokens as: initial-stressed (trochaic), final-stressed (iambic),
   monosyllabic (stressed by context), or function word (unstressed)
4. Compare S2 distributions across stress classes
5. Also analyze metrical position within iambic pentameter lines
"""

import json
import re
import sys
from collections import defaultdict
import statistics

try:
    import pronouncing
except ImportError:
    print("pip install pronouncing required")
    sys.exit(1)

CORPUS_FILE = "/home/user/s2lab/results/corpus_results.json"

# Common English function words — typically unstressed
FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "it", "its", "that", "this",
    "was", "are", "be", "been", "has", "have", "had", "do", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "not",
    "no", "nor", "so", "yet", "both", "either", "neither", "each", "every",
    "all", "some", "any", "few", "more", "most", "other", "such", "than",
    "then", "when", "where", "which", "who", "whom", "whose", "how", "if",
    "though", "although", "because", "since", "while", "after", "before",
    "into", "onto", "upon", "about", "above", "below", "through", "during",
    "between", "among", "i", "me", "my", "we", "us", "our", "you", "your",
    "he", "him", "his", "she", "her", "they", "them", "their", "these",
    "those", "what", "there", "here", "also", "just", "only", "even", "still",
    "too", "very", "quite", "much", "many", "own", "same", "than", "till",
    "o'er", "doth", "thy", "thee", "thou", "ye", "hath", "art", "'tis",
}


def get_stress_pattern(word):
    """Get the stress pattern of a word from CMU dict.
    Returns a string like '10' (stressed-unstressed) or '01' or '1' etc.
    1=primary, 2=secondary, 0=unstressed
    Returns None if word not in CMU dict.
    """
    word_clean = re.sub(r"[^a-z'-]", "", word.lower())
    if not word_clean:
        return None
    stresses = pronouncing.stresses_for_word(word_clean)
    if stresses:
        return stresses[0]
    # Try without apostrophe
    word_clean2 = word_clean.replace("'", "")
    stresses = pronouncing.stresses_for_word(word_clean2)
    if stresses:
        return stresses[0]
    return None


def classify_stress(word, stress_pattern):
    """Classify a word's stress type."""
    word_lower = re.sub(r"[^a-z]", "", word.lower())
    if word_lower in FUNCTION_WORDS:
        return "function_word"
    if stress_pattern is None:
        return "unknown"
    n_syllables = len(stress_pattern)
    if n_syllables == 1:
        return "monosyllabic_content"
    primary_pos = stress_pattern.index("1") if "1" in stress_pattern else -1
    if primary_pos == 0:
        return "trochaic_initial_stress"  # first syllable stressed
    elif primary_pos == n_syllables - 1:
        return "iambic_final_stress"      # last syllable stressed
    else:
        return "medial_stress"             # stress in middle


def token_to_word(token_str):
    """Clean GPT-2 token to get the word."""
    # GPT-2 tokens start with Ġ (space) for word-initial, or are subword
    word = token_str.strip().lstrip("Ġ").lstrip(" ")
    # Remove punctuation (but keep apostrophes for contractions)
    word = re.sub(r"[^a-zA-Z'-]", "", word)
    return word.lower()


def analyze_stress_vs_s2(corpus_data, target_poems=None):
    """Main analysis: compare S2 values by stress classification."""

    results_by_stress = defaultdict(list)
    results_by_poem = defaultdict(lambda: defaultdict(list))

    # Also track syllable count vs S2
    monosyllabic_s2 = []
    polysyllabic_s2 = []

    # Track initial vs non-initial syllable stress
    initial_stressed_s2 = []
    final_stressed_s2 = []

    poems_analyzed = 0
    tokens_analyzed = 0

    for poem_data in corpus_data:
        meta = poem_data["metadata"]

        # Filter to target poems if specified
        if target_poems:
            if meta["title"] not in target_poems:
                continue

        poem_title = meta["title"]
        poem_author = meta["author"]

        for tok in poem_data["tokens"]:
            token_str = tok["token"]
            s2 = tok["s2"]

            word = token_to_word(token_str)
            if not word or len(word) < 2:
                continue

            stress_pat = get_stress_pattern(word)
            stress_class = classify_stress(word, stress_pat)

            results_by_stress[stress_class].append(s2)
            results_by_poem[poem_title][stress_class].append(s2)
            tokens_analyzed += 1

            if stress_pat:
                n_syl = len(stress_pat)
                if n_syl == 1:
                    monosyllabic_s2.append(s2)
                else:
                    polysyllabic_s2.append(s2)

                if "1" in stress_pat:
                    primary_pos = stress_pat.index("1")
                    if primary_pos == 0:
                        initial_stressed_s2.append(s2)
                    else:
                        final_stressed_s2.append(s2)

        poems_analyzed += 1

    return {
        "poems_analyzed": poems_analyzed,
        "tokens_analyzed": tokens_analyzed,
        "results_by_stress": {k: v for k, v in results_by_stress.items()},
        "monosyllabic_s2": monosyllabic_s2,
        "polysyllabic_s2": polysyllabic_s2,
        "initial_stressed_s2": initial_stressed_s2,
        "final_stressed_s2": final_stressed_s2,
        "results_by_poem": dict(results_by_poem),
    }


def analyze_iambic_pentameter_positions(corpus_data, sonnet_titles):
    """
    For iambic pentameter lines, analyze S2 by metrical position (1-10).
    Uses syllable counting to map tokens to metrical feet.
    """
    position_s2 = defaultdict(list)  # position (1-10) -> list of S2 values
    even_positions = []  # stressed in iambic: 2,4,6,8,10
    odd_positions = []   # unstressed in iambic: 1,3,5,7,9

    for poem_data in corpus_data:
        if poem_data["metadata"]["title"] not in sonnet_titles:
            continue

        # Get the poem text to analyze line by line
        # We need to reconstruct text from tokens
        tokens = poem_data["tokens"]

        # Reconstruct line structure by tracking token positions
        # and estimating syllable positions within lines
        line_tokens = []
        current_line = []

        for tok in tokens:
            token_str = tok["token"]
            # Newline token marks line boundary
            if "\n" in token_str or token_str.strip() == "":
                if current_line:
                    line_tokens.append(current_line)
                current_line = []
            else:
                current_line.append(tok)
        if current_line:
            line_tokens.append(current_line)

        # For each line, assign metrical positions
        for line in line_tokens:
            metrical_pos = 1
            for tok in line:
                word = token_to_word(tok["token"])
                if not word:
                    continue

                stress_pat = get_stress_pattern(word)
                n_syllables = len(stress_pat) if stress_pat else 1

                # This token starts at metrical_pos
                for syl_offset in range(n_syllables):
                    pos = metrical_pos + syl_offset
                    if 1 <= pos <= 10:
                        position_s2[pos].append(tok["s2"])
                        if pos % 2 == 0:
                            even_positions.append(tok["s2"])
                        else:
                            odd_positions.append(tok["s2"])

                metrical_pos += n_syllables
                if metrical_pos > 10:
                    break

    return {
        "position_s2": {k: v for k, v in position_s2.items()},
        "even_positions_s2": even_positions,   # iambic STRESSED positions
        "odd_positions_s2": odd_positions,     # iambic UNSTRESSED positions
    }


def summarize_group(values):
    if not values:
        return {"n": 0, "mean": None, "median": None, "std": None}
    return {
        "n": len(values),
        "mean": round(statistics.mean(values), 4),
        "median": round(statistics.median(values), 4),
        "std": round(statistics.stdev(values) if len(values) > 1 else 0, 4),
    }


def main():
    print("Loading corpus data...")
    with open(CORPUS_FILE) as f:
        corpus_data = json.load(f)

    print(f"Corpus: {len(corpus_data)} poems")

    # --- Analysis 1: Full corpus, stress class vs S2 ---
    print("\n--- Analysis 1: Stress Classification vs S2 (all English poems) ---")
    res1 = analyze_stress_vs_s2(
        [p for p in corpus_data if p["metadata"].get("language", "en") == "en"]
    )

    print(f"\nPoems analyzed: {res1['poems_analyzed']}")
    print(f"Tokens analyzed: {res1['tokens_analyzed']}")

    summary = {}
    print("\n## S2 by Stress Classification:")
    print(f"{'Category':<35} {'N':>6} {'Mean S2':>8} {'Median S2':>10} {'Std S2':>8}")
    print("-" * 75)

    order = [
        "function_word", "monosyllabic_content",
        "trochaic_initial_stress", "iambic_final_stress",
        "medial_stress", "unknown"
    ]

    for cat in order:
        vals = res1["results_by_stress"].get(cat, [])
        s = summarize_group(vals)
        summary[cat] = s
        if s["n"] > 0:
            print(f"{cat:<35} {s['n']:>6} {s['mean']:>8.3f} {s['median']:>10.3f} {s['std']:>8.3f}")

    print("\n## Mono vs Polysyllabic:")
    mono = summarize_group(res1["monosyllabic_s2"])
    poly = summarize_group(res1["polysyllabic_s2"])
    print(f"  Monosyllabic content: n={mono['n']}, mean={mono['mean']:.3f}")
    print(f"  Polysyllabic content: n={poly['n']}, mean={poly['mean']:.3f}")

    print("\n## Initial vs Final Primary Stress (polysyllabic content words):")
    init = summarize_group(res1["initial_stressed_s2"])
    final = summarize_group(res1["final_stressed_s2"])
    print(f"  Initial-stressed (trochaic): n={init['n']}, mean={init['mean']:.3f}")
    print(f"  Final-stressed (iambic): n={final['n']}, mean={final['mean']:.3f}")

    if init["mean"] and final["mean"]:
        diff = final["mean"] - init["mean"]
        print(f"  Difference (final - initial): {diff:+.3f}")
        if diff > 0.5:
            print("  → Iambic (final-stressed) words are MORE surprising (H1 supported)")
        elif diff < -0.5:
            print("  → Trochaic (initial-stressed) words are MORE surprising (H1 partial)")
        else:
            print("  → Minimal difference in stress position (H3 supported)")

    # --- Analysis 2: Formal sonnets specifically ---
    sonnet_titles = [
        "Sonnet 18 (Shall I compare thee)",
        "Sonnet 73 (That time of year)",
        "Sonnet 130 (My mistress' eyes)",
        "Death, Be Not Proud (Holy Sonnet X)",
    ]

    print(f"\n--- Analysis 2: Formal Sonnets Only (n={len(sonnet_titles)}) ---")
    res2 = analyze_stress_vs_s2(corpus_data, target_poems=sonnet_titles)

    print(f"Tokens analyzed: {res2['tokens_analyzed']}")
    print("\n## S2 by Stress Classification (sonnets only):")
    print(f"{'Category':<35} {'N':>6} {'Mean S2':>8}")
    print("-" * 55)

    sonnet_summary = {}
    for cat in order:
        vals = res2["results_by_stress"].get(cat, [])
        s = summarize_group(vals)
        sonnet_summary[cat] = s
        if s["n"] > 0:
            print(f"{cat:<35} {s['n']:>6} {s['mean']:>8.3f}")

    # --- Analysis 3: Iambic pentameter metrical positions ---
    print(f"\n--- Analysis 3: Iambic Pentameter Position vs S2 ---")
    res3 = analyze_iambic_pentameter_positions(corpus_data, sonnet_titles)

    pos_data = res3["position_s2"]
    if pos_data:
        print("\n## Average S2 by Metrical Position (1=unstressed, 2=stressed, etc.):")
        print(f"{'Position':<12} {'Expected':<12} {'N':>6} {'Mean S2':>8}")
        print("-" * 42)

        pos_means = {}
        for pos in range(1, 11):
            vals = pos_data.get(pos, [])
            s = summarize_group(vals)
            stress_label = "STRESSED" if pos % 2 == 0 else "unstressed"
            pos_means[pos] = s["mean"]
            if s["n"] > 0:
                print(f"  {pos:<10} {stress_label:<12} {s['n']:>6} {s['mean']:>8.3f}")

        even = summarize_group(res3["even_positions_s2"])
        odd = summarize_group(res3["odd_positions_s2"])
        print(f"\n  Stressed positions (2,4,6,8,10): mean S2 = {even['mean']:.3f} (n={even['n']})")
        print(f"  Unstressed positions (1,3,5,7,9): mean S2 = {odd['mean']:.3f} (n={odd['n']})")
        if even["mean"] and odd["mean"]:
            diff = even["mean"] - odd["mean"]
            print(f"  Difference (stressed - unstressed): {diff:+.3f}")

    # --- Save results ---
    output = {
        "experiment": "metrical_stress_vs_s2",
        "date": "2026-11-04",
        "full_corpus": {
            "n_poems": res1["poems_analyzed"],
            "n_tokens": res1["tokens_analyzed"],
            "stress_summary": summary,
            "monosyllabic": mono,
            "polysyllabic": poly,
            "initial_stressed": init,
            "final_stressed": final,
        },
        "sonnets_only": {
            "n_tokens": res2["tokens_analyzed"],
            "stress_summary": sonnet_summary,
        },
        "iambic_pentameter_positions": {
            "by_position": {
                str(pos): summarize_group(res3["position_s2"].get(pos, []))
                for pos in range(1, 11)
            },
            "stressed_positions": summarize_group(res3["even_positions_s2"]),
            "unstressed_positions": summarize_group(res3["odd_positions_s2"]),
        },
    }

    out_path = "/home/user/s2lab/findings/metrical_stress_s2.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return output


if __name__ == "__main__":
    result = main()
