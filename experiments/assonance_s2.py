"""
Assonance and S₂: Does Vowel-Sound Repetition Correlate with Semantic Surprise?

Hypothesis: When a poet uses assonance — repeating a vowel sound across nearby
words — do those tokens show systematically different S₂ than non-assonant tokens?

Competing theories:
  1. LOWER S₂ (Phonetic Grooming): Assonance is a surfacing strategy — poets
     choose vowel-compatible words to smooth over semantic surprises. The shared
     vowel sound "fits" a tonal or textural context, reducing statistical surprise.
  2. HIGHER S₂ (Sonic Risk-Taking): Assonance is used to "carry" semantically
     daring choices — the shared sound makes an unexpected word feel inevitable,
     a Trojan-horse strategy. The sonic fit licenses the semantic leap.
  3. NULL: Assonance is purely sonic and orthogonal to GPT-2's statistical model,
     which doesn't have phonetic representations.

Method:
  - For each content-word token, extract its dominant vowel sound (the primary
    vowel pattern: single-vowel, diphthong, or vowel cluster)
  - Check if any of the 4 preceding content-word tokens share that vowel pattern
  - Compare S₂ at assonant vs non-assonant positions
  - Stratify by vowel type (low/back: a,o vs high/front: i,e,u)
  - Look at whether assonance clusters with HIGH or LOW entropy contexts
  - Check era and author variation

Note: Vowel extraction from orthographic form is an approximation of phonetics.
'ea' in "bread" vs "bead" differs, but many patterns are consistent enough to
be statistically meaningful in aggregate.
"""

import json
import re
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "in", "on", "at",
    "to", "for", "with", "is", "was", "are", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "that", "this",
    "it", "he", "she", "they", "we", "i", "you", "my", "your",
    "his", "her", "our", "their", "its", "not", "no", "by", "from",
    "as", "if", "so", "up", "out", "then", "there", "when", "where",
    "who", "what", "which", "how", "all", "into", "through", "just",
    "even", "still", "also", "each", "them", "these", "those",
}

# Vowel pattern extraction — classify words by their primary vowel nucleus
# This is a simplified phonetic approximation based on orthography.
# We extract the first "vowel cluster" (sequence of vowels) in the word.

VOWEL_CHARS = set("aeiouAEIOU")

# Back/low vowels: a, o (tend to open, dark sound)
# Front/high vowels: i, e (tend to bright, forward sound)
# High-back: u (lips rounded)

VOWEL_CLASS = {
    "a": "low",
    "o": "back",
    "u": "high_back",
    "e": "front",
    "i": "front_high",
    # Clusters
    "ai": "front", "ay": "front", "ae": "front",
    "au": "back", "aw": "back",
    "ea": "front", "ee": "front_high",
    "ei": "front", "ey": "front",
    "eu": "front",
    "ia": "front_high",
    "ie": "front_high",
    "io": "back",
    "oa": "back", "oe": "back",
    "oi": "back", "oy": "back",
    "oo": "high_back",
    "ou": "back", "ow": "back",
    "ui": "high_back",
    "ue": "high_back",
}


def clean_token(tok: str) -> str:
    return tok.lstrip("Ġ Ċ\n\r\t ").lower()


def extract_vowel_nucleus(word: str) -> str | None:
    """Extract the first vowel cluster from a word as its primary nucleus."""
    word = word.lower()
    # Remove non-alpha chars
    word = re.sub(r"[^a-z]", "", word)
    if not word:
        return None
    # Find the first vowel cluster (1 or 2 consecutive vowels)
    i = 0
    while i < len(word):
        if word[i] in VOWEL_CHARS:
            # Collect vowel cluster (up to 2 chars for digraphs)
            cluster = word[i]
            if i + 1 < len(word) and word[i+1] in VOWEL_CHARS:
                cluster += word[i+1]
            return cluster
        i += 1
    return None  # No vowel found (unusual)


def vowel_class(nucleus: str | None) -> str | None:
    """Map a vowel nucleus to a broad phonetic class."""
    if nucleus is None:
        return None
    return VOWEL_CLASS.get(nucleus, VOWEL_CLASS.get(nucleus[0], "other"))


def is_content_word(tok: str) -> bool:
    cleaned = clean_token(tok)
    if not any(c.isalpha() for c in cleaned):
        return False
    if cleaned in STOPWORDS:
        return False
    return True


NEWLINE_THRESHOLD = 0.9


def get_clean_tokens(tokens):
    return [
        t for t in tokens
        if t.get("p_newline", 0) < NEWLINE_THRESHOLD
        and t.get("token", "") not in ["<|endoftext|>"]
    ]


def run():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Per-token data: (s2, entropy, is_assonant, vowel_class, era, author)
    all_tokens = []
    era_data = defaultdict(lambda: {"assonant": [], "non_assonant": []})
    author_data = defaultdict(lambda: {"assonant": [], "non_assonant": []})
    vowel_class_data = defaultdict(lambda: {"assonant": [], "non_assonant": []})

    # Entropy context: assonant tokens in high vs low entropy contexts
    high_entropy_assonant_s2 = []
    high_entropy_non_assonant_s2 = []
    low_entropy_assonant_s2 = []
    low_entropy_non_assonant_s2 = []

    poems_processed = 0
    total_assonant = 0
    total_non_assonant = 0

    for item in corpus:
        meta = item.get("metadata", {})
        if meta.get("era") == "control":
            continue

        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        tokens = get_clean_tokens(item.get("tokens", []))

        if len(tokens) < 15:
            continue

        poems_processed += 1

        # Build a sliding window of content-word vowel nuclei
        # For each token position, look at the previous WINDOW_SIZE content words
        WINDOW = 4

        # Pre-extract: list of (position, vowel_nucleus) for content words only
        content_positions = []
        for idx, t in enumerate(tokens):
            tok_str = t.get("token", "")
            if is_content_word(tok_str):
                nucleus = extract_vowel_nucleus(clean_token(tok_str))
                if nucleus:
                    content_positions.append((idx, nucleus))

        # For each content word, check if its vowel nucleus appears in the
        # previous WINDOW content words
        for ci, (idx, nucleus) in enumerate(content_positions):
            t = tokens[idx]
            if "s2" not in t or "entropy" not in t:
                continue

            s2 = t["s2"]
            entropy = t["entropy"]

            # Look back at previous WINDOW content words
            prev_nuclei = [n for _, n in content_positions[max(0, ci - WINDOW):ci]]

            # Assonance: same vowel nucleus appears in previous window
            is_assonant = nucleus in prev_nuclei

            # Also check by vowel class (broader matching)
            nucleus_class = vowel_class(nucleus)
            is_class_assonant = any(
                vowel_class(n) == nucleus_class for n in prev_nuclei
            ) if nucleus_class else False

            # Categorize
            key = "assonant" if is_assonant else "non_assonant"
            era_data[era][key].append(s2)
            author_data[author][key].append(s2)
            if nucleus_class:
                vowel_class_data[nucleus_class][key].append(s2)

            all_tokens.append({
                "s2": s2,
                "entropy": entropy,
                "is_assonant": is_assonant,
                "is_class_assonant": is_class_assonant,
                "nucleus": nucleus,
                "nucleus_class": nucleus_class,
                "era": era,
                "author": author,
            })

            if is_assonant:
                total_assonant += 1
            else:
                total_non_assonant += 1

            # Entropy stratification (median entropy ≈ split point)
            # We'll compute this after the fact using overall median

    # Compute overall medians
    all_s2 = [t["s2"] for t in all_tokens]
    all_entropy = [t["entropy"] for t in all_tokens]
    if not all_s2:
        print("No data!")
        return {}

    median_entropy = statistics.median(all_entropy)
    median_s2 = statistics.median(all_s2)

    # Corpus-level comparison
    assonant_s2 = [t["s2"] for t in all_tokens if t["is_assonant"]]
    non_assonant_s2 = [t["s2"] for t in all_tokens if not t["is_assonant"]]

    class_assonant_s2 = [t["s2"] for t in all_tokens if t["is_class_assonant"]]
    non_class_assonant_s2 = [t["s2"] for t in all_tokens if not t["is_class_assonant"]]

    # Entropy-stratified
    for t in all_tokens:
        H = t["entropy"]
        if t["is_assonant"]:
            if H > median_entropy:
                high_entropy_assonant_s2.append(t["s2"])
            else:
                low_entropy_assonant_s2.append(t["s2"])
        else:
            if H > median_entropy:
                high_entropy_non_assonant_s2.append(t["s2"])
            else:
                low_entropy_non_assonant_s2.append(t["s2"])

    def stats(lst):
        if len(lst) < 2:
            return {"n": len(lst), "mean": None, "std": None, "pos_pct": None}
        m = statistics.mean(lst)
        s = statistics.stdev(lst)
        pos = sum(1 for x in lst if x > 0) / len(lst) * 100
        return {"n": len(lst), "mean": round(m, 4), "std": round(s, 4), "pos_pct": round(pos, 1)}

    # Era breakdown: sort by assonant - non_assonant difference
    era_rows = []
    for era, d in era_data.items():
        a = d["assonant"]
        na = d["non_assonant"]
        if len(a) < 20 or len(na) < 20:
            continue
        ma = statistics.mean(a)
        mna = statistics.mean(na)
        era_rows.append({
            "era": era,
            "assonant_mean": round(ma, 4),
            "non_assonant_mean": round(mna, 4),
            "diff": round(ma - mna, 4),
            "n_assonant": len(a),
            "n_non_assonant": len(na),
        })
    era_rows.sort(key=lambda x: x["diff"])

    # Vowel class breakdown
    vclass_rows = []
    for vc, d in vowel_class_data.items():
        a = d["assonant"]
        na = d["non_assonant"]
        if len(a) < 20 or len(na) < 20:
            continue
        ma = statistics.mean(a)
        mna = statistics.mean(na)
        vclass_rows.append({
            "vowel_class": vc,
            "assonant_mean": round(ma, 4),
            "non_assonant_mean": round(mna, 4),
            "diff": round(ma - mna, 4),
            "n_assonant": len(a),
        })
    vclass_rows.sort(key=lambda x: x["diff"])

    results = {
        "corpus_summary": {
            "poems_processed": poems_processed,
            "total_assonant_tokens": total_assonant,
            "total_non_assonant_tokens": total_non_assonant,
            "assonance_rate": round(total_assonant / (total_assonant + total_non_assonant) * 100, 2) if (total_assonant + total_non_assonant) > 0 else 0,
            "median_entropy": round(median_entropy, 4),
            "median_s2": round(median_s2, 4),
        },
        "corpus_level": {
            "assonant": stats(assonant_s2),
            "non_assonant": stats(non_assonant_s2),
            "diff_assonant_minus_non": round(statistics.mean(assonant_s2) - statistics.mean(non_assonant_s2), 4) if assonant_s2 and non_assonant_s2 else None,
            "class_assonant": stats(class_assonant_s2),
            "class_non_assonant": stats(non_class_assonant_s2),
        },
        "entropy_stratified": {
            "high_entropy": {
                "assonant": stats(high_entropy_assonant_s2),
                "non_assonant": stats(high_entropy_non_assonant_s2),
                "diff": round(statistics.mean(high_entropy_assonant_s2) - statistics.mean(high_entropy_non_assonant_s2), 4) if high_entropy_assonant_s2 and high_entropy_non_assonant_s2 else None,
            },
            "low_entropy": {
                "assonant": stats(low_entropy_assonant_s2),
                "non_assonant": stats(low_entropy_non_assonant_s2),
                "diff": round(statistics.mean(low_entropy_assonant_s2) - statistics.mean(low_entropy_non_assonant_s2), 4) if low_entropy_assonant_s2 and low_entropy_non_assonant_s2 else None,
            },
        },
        "era_breakdown": era_rows,
        "vowel_class_breakdown": vclass_rows,
    }

    return results


if __name__ == "__main__":
    import sys, os
    from pathlib import Path
    os.chdir(Path(__file__).parent.parent)
    results = run()

    output_path = Path("results/assonance_s2.json")
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results saved to {output_path}")
    print(f"\nCorpus: {results['corpus_summary']['poems_processed']} poems, "
          f"{results['corpus_summary']['total_assonant_tokens']} assonant tokens "
          f"({results['corpus_summary']['assonance_rate']}%)")
    print(f"\nCorpus-level S2:")
    cl = results["corpus_level"]
    print(f"  Assonant tokens:     mean S2 = {cl['assonant']['mean']} (n={cl['assonant']['n']})")
    print(f"  Non-assonant:        mean S2 = {cl['non_assonant']['mean']} (n={cl['non_assonant']['n']})")
    print(f"  Difference:          {cl['diff_assonant_minus_non']}")
    print(f"\n  Class-assonant:      mean S2 = {cl['class_assonant']['mean']}")
    print(f"  Non-class-assonant:  mean S2 = {cl['class_non_assonant']['mean']}")
    print(f"\nEntropy-stratified:")
    es = results["entropy_stratified"]
    print(f"  High-H assonant:     {es['high_entropy']['assonant']['mean']}  "
          f"| High-H non-assonant: {es['high_entropy']['non_assonant']['mean']}  "
          f"| diff: {es['high_entropy']['diff']}")
    print(f"  Low-H assonant:      {es['low_entropy']['assonant']['mean']}  "
          f"| Low-H non-assonant:  {es['low_entropy']['non_assonant']['mean']}  "
          f"| diff: {es['low_entropy']['diff']}")

    print(f"\nEra breakdown (sorted by assonant-nonassonant diff):")
    for row in results["era_breakdown"]:
        marker = " *** HIGHER ASSONANT" if row["diff"] > 0.1 else (" *** LOWER ASSONANT" if row["diff"] < -0.1 else "")
        print(f"  {row['era']:30s} assonant={row['assonant_mean']:+.3f} non={row['non_assonant_mean']:+.3f} diff={row['diff']:+.3f}{marker}")

    print(f"\nVowel class breakdown:")
    for row in results["vowel_class_breakdown"]:
        print(f"  {row['vowel_class']:15s} assonant={row['assonant_mean']:+.3f} non={row['non_assonant_mean']:+.3f} diff={row['diff']:+.3f} n_assonant={row['n_assonant']}")
