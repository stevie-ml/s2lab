"""
Readability vs S2: Does traditional text difficulty align with information-theoretic surprise?

We compute Flesch-Kincaid Grade Level, Automated Readability Index (ARI), and
Coleman-Liau Index for each English poem, then correlate with avg S2.

Hypothesis: Traditional readability (based on word/sentence length) may be INVERSELY
correlated with S2, since:
- Long words give GPT-2 more context = more prediction certainty = lower entropy
- But GPT-2 may still be surprised by rare long words (high surprisal, high S2)
- Short, simple poems with monosyllables could have HIGH entropy (unpredictable) = high S2

This experiment tests whether information-theoretic difficulty ≠ traditional difficulty.
"""

import json
import re
import math
import sys

def count_syllables(word):
    """Approximate syllable count using vowel-group heuristic."""
    word = word.lower().strip(".,!?;:\"'")
    if not word:
        return 0
    # Count vowel groups
    count = len(re.findall(r'[aeiou]+', word))
    # Subtract silent e at word end
    if word.endswith('e') and len(word) > 2 and word[-2] not in 'aeiou':
        count -= 1
    return max(1, count)

def count_sentences(text):
    """Count sentences by terminal punctuation."""
    sentences = re.split(r'[.!?]+', text)
    return max(1, len([s for s in sentences if s.strip()]))

def compute_readability(text):
    """Compute multiple readability scores for a text."""
    # Tokenize
    words = re.findall(r"[a-zA-Z']+", text)
    if not words:
        return None

    n_words = len(words)
    n_sentences = count_sentences(text)
    n_chars = sum(len(w) for w in words)
    n_syllables = sum(count_syllables(w) for w in words)

    if n_words < 5 or n_sentences < 1:
        return None

    words_per_sentence = n_words / n_sentences
    syllables_per_word = n_syllables / n_words
    chars_per_word = n_chars / n_words

    # Flesch Reading Ease (higher = easier)
    fre = 206.835 - 1.015 * words_per_sentence - 84.6 * syllables_per_word

    # Flesch-Kincaid Grade Level (higher = harder)
    fkgl = 0.39 * words_per_sentence + 11.8 * syllables_per_word - 15.59

    # Automated Readability Index (higher = harder)
    ari = 4.71 * chars_per_word + 0.5 * words_per_sentence - 21.43

    # Coleman-Liau Index (higher = harder)
    l = chars_per_word * 100  # avg chars per 100 words
    s = (n_sentences / n_words) * 100  # avg sentences per 100 words
    cli = 0.0588 * l - 0.296 * s - 15.8

    return {
        "n_words": n_words,
        "n_sentences": n_sentences,
        "n_syllables": n_syllables,
        "words_per_sentence": words_per_sentence,
        "syllables_per_word": syllables_per_word,
        "chars_per_word": chars_per_word,
        "flesch_reading_ease": fre,
        "flesch_kincaid_grade": fkgl,
        "automated_readability_index": ari,
        "coleman_liau_index": cli,
    }

def pearson_r(xs, ys):
    """Compute Pearson correlation coefficient."""
    n = len(xs)
    if n < 3:
        return None
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return None
    return num / (dx * dy)

def main():
    # Load corpus results
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    # Load poem texts
    sys.path.insert(0, ".")
    from corpus.poems import POEMS
    poem_texts = {(p["title"], p.get("author", "")): p["text"] for p in POEMS}

    results = []
    skipped = 0

    for poem in corpus:
        meta = poem["metadata"]
        # Skip non-English poems
        if meta.get("language", "en") != "en":
            continue
        # Skip control prose
        if meta.get("era") == "control":
            continue

        # Find text
        key = (meta["title"], meta.get("author", ""))
        text = poem_texts.get(key)
        if text is None:
            # Try title-only match
            for (t, a), txt in poem_texts.items():
                if t == meta["title"]:
                    text = txt
                    break
        if text is None:
            skipped += 1
            continue

        # Compute readability
        readability = compute_readability(text)
        if readability is None:
            skipped += 1
            continue

        # Get S2 metrics (artifact-free: exclude p_newline >= 0.9)
        clean_tokens = [t for t in poem["tokens"] if t.get("p_newline", 0) < 0.9]
        if len(clean_tokens) < 10:
            skipped += 1
            continue

        avg_s2 = sum(t["s2"] for t in clean_tokens) / len(clean_tokens)
        avg_entropy = sum(t["entropy"] for t in clean_tokens) / len(clean_tokens)
        avg_surprisal = sum(t["surprisal"] for t in clean_tokens) / len(clean_tokens)
        pos_s2_ratio = sum(1 for t in clean_tokens if t["s2"] > 0) / len(clean_tokens)

        results.append({
            "title": meta["title"],
            "author": meta.get("author", ""),
            "era": meta.get("era", ""),
            "year": meta.get("year", 0),
            "avg_s2": avg_s2,
            "avg_entropy": avg_entropy,
            "avg_surprisal": avg_surprisal,
            "pos_s2_ratio": pos_s2_ratio,
            **readability
        })

    print(f"Analyzed: {len(results)} poems, skipped: {skipped}")

    # Compute correlations
    measures = [
        ("flesch_reading_ease", "Flesch Reading Ease (higher=easier)"),
        ("flesch_kincaid_grade", "Flesch-Kincaid Grade Level (higher=harder)"),
        ("automated_readability_index", "Automated Readability Index (higher=harder)"),
        ("coleman_liau_index", "Coleman-Liau Index (higher=harder)"),
        ("words_per_sentence", "Words Per Sentence"),
        ("syllables_per_word", "Syllables Per Word"),
    ]

    s2_vals = [r["avg_s2"] for r in results]
    h_vals = [r["avg_entropy"] for r in results]

    print("\n=== Correlations with Avg S2 (artifact-free) ===")
    print(f"{'Measure':<45} {'r(S2)':<10} {'r(entropy)'}")
    print("-" * 70)
    correlations = {}
    for key, label in measures:
        vals = [r[key] for r in results]
        r_s2 = pearson_r(vals, s2_vals)
        r_h = pearson_r(vals, h_vals)
        correlations[key] = r_s2
        print(f"{label:<45} {r_s2:+.3f}     {r_h:+.3f}")

    # Sort by readability (FK grade)
    results.sort(key=lambda x: x["flesch_kincaid_grade"])

    # Quintile analysis
    n = len(results)
    q = n // 5
    print("\n=== S2 by Flesch-Kincaid Grade Quintile ===")
    print(f"{'Quintile':<20} {'FK Grade':<12} {'Avg S2':<10} {'Pos S2%':<10} {'Avg Entropy'}")
    print("-" * 65)
    for i in range(5):
        group = results[i*q:(i+1)*q] if i < 4 else results[i*q:]
        fk_avg = sum(r["flesch_kincaid_grade"] for r in group) / len(group)
        s2_avg = sum(r["avg_s2"] for r in group) / len(group)
        h_avg = sum(r["avg_entropy"] for r in group) / len(group)
        pos_ratio = sum(r["pos_s2_ratio"] for r in group) / len(group)
        label = ["Very Easy (Q1)", "Easy (Q2)", "Medium (Q3)", "Hard (Q4)", "Very Hard (Q5)"][i]
        print(f"{label:<20} {fk_avg:<12.1f} {s2_avg:<10.3f} {pos_ratio*100:<10.1f} {h_avg:.3f}")

    # Extreme examples
    print("\n=== Top 10 Easiest Poems (by FK Grade) ===")
    for r in results[:10]:
        print(f"  FK={r['flesch_kincaid_grade']:.1f} S2={r['avg_s2']:+.3f} | {r['author']}: {r['title']}")

    print("\n=== Top 10 Hardest Poems (by FK Grade) ===")
    for r in results[-10:]:
        print(f"  FK={r['flesch_kincaid_grade']:.1f} S2={r['avg_s2']:+.3f} | {r['author']}: {r['title']}")

    # By era
    era_data = {}
    for r in results:
        era = r["era"]
        if era not in era_data:
            era_data[era] = []
        era_data[era].append(r)

    print("\n=== Average FK Grade and S2 by Era (n>=3) ===")
    era_summary = []
    for era, items in era_data.items():
        if len(items) < 3:
            continue
        fk = sum(r["flesch_kincaid_grade"] for r in items) / len(items)
        s2 = sum(r["avg_s2"] for r in items) / len(items)
        era_summary.append((era, len(items), fk, s2))
    era_summary.sort(key=lambda x: x[2])
    print(f"{'Era':<25} {'n':<5} {'Avg FK Grade':<15} {'Avg S2'}")
    print("-" * 55)
    for era, n, fk, s2 in era_summary:
        print(f"{era:<25} {n:<5} {fk:<15.1f} {s2:+.3f}")

    # Interesting quadrants: easy+high S2 vs hard+low S2
    fk_median = sorted(r["flesch_kincaid_grade"] for r in results)[len(results)//2]
    s2_median = sorted(r["avg_s2"] for r in results)[len(results)//2]

    print(f"\n=== Quadrant Analysis (FK median={fk_median:.1f}, S2 median={s2_median:.3f}) ===")
    quadrants = {
        "Easy + High S2 (readable but surprising)": [],
        "Hard + High S2 (difficult and surprising)": [],
        "Easy + Low S2 (readable and expected)": [],
        "Hard + Low S2 (difficult but predictable)": [],
    }
    for r in results:
        easy = r["flesch_kincaid_grade"] < fk_median
        high_s2 = r["avg_s2"] > s2_median
        if easy and high_s2:
            quadrants["Easy + High S2 (readable but surprising)"].append(r)
        elif not easy and high_s2:
            quadrants["Hard + High S2 (difficult and surprising)"].append(r)
        elif easy and not high_s2:
            quadrants["Easy + Low S2 (readable and expected)"].append(r)
        else:
            quadrants["Hard + Low S2 (difficult but predictable)"].append(r)

    for label, items in quadrants.items():
        print(f"\n{label} (n={len(items)}):")
        # Show top 5 by era diversity
        shown = sorted(items, key=lambda x: abs(x["avg_s2"]), reverse=True)[:5]
        for r in shown:
            print(f"  FK={r['flesch_kincaid_grade']:.1f} S2={r['avg_s2']:+.3f} | {r['author']}: {r['title']}")

    # Save results
    output = {
        "n_analyzed": len(results),
        "correlations": correlations,
        "poems": results
    }
    with open("results/readability_vs_s2.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/readability_vs_s2.json")

if __name__ == "__main__":
    main()
