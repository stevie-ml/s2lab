"""
Era-Level Counter-Lexicon: What does each literary era suppress most?

For each literary era, identify the words GPT-2 most frequently expected
but poets in that era systematically rejected. This reveals what default
language each movement writes *against*.

Extends suppressed_lexicon.py (global) to per-era breakdown.
"""

import json
import os
from collections import defaultdict, Counter

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")


def load_corpus():
    path = os.path.join(RESULTS_DIR, "corpus_results.json")
    with open(path) as f:
        return json.load(f)


def is_artifact(token):
    return token.get("p_newline", 0.0) >= 0.9


def is_function_word(tok):
    fw = {
        "the", "a", "an", "of", "in", "to", "and", "is", "are", "was",
        "were", "be", "been", "being", "have", "has", "had", "do", "does",
        "did", "will", "would", "could", "should", "may", "might", "shall",
        "at", "on", "by", "with", "as", "for", "that", "this", "it", "its",
        "i", "my", "me", "we", "our", "you", "your", "he", "she", "they",
        "him", "her", "them", "not", "no", "or", "but", "if", "so", "from",
        "up", "out", "all", "one", "there", "their", "what", "which", "who",
        "more", "when", "then", "than", "into", "about", "like", "some", "can",
    }
    return tok.strip().lower() in fw


def get_era_suppressions(corpus, min_era_poems=3, min_word_predictions=10):
    """
    For each era, collect:
    - era_predicted[era][word] = # times GPT-2 predicted this word
    - era_accepted[era][word] = # times poet actually wrote it when predicted
    """
    era_predicted = defaultdict(Counter)
    era_accepted = defaultdict(Counter)
    era_poem_counts = Counter()

    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        lang = meta.get("language", "en")
        if lang != "en":
            continue
        era_poem_counts[era] += 1

        for token in poem["tokens"]:
            if is_artifact(token):
                continue
            actual = token["token"].strip()
            if not actual:
                continue

            alts = token.get("alternatives", [])
            if not alts:
                continue

            top1 = alts[0]["token"].strip()
            if not top1:
                continue

            era_predicted[era][top1] += 1
            if actual.lower() == top1.lower():
                era_accepted[era][top1] += 1

    return era_predicted, era_accepted, era_poem_counts


def build_era_counter_lexicon(era_predicted, era_accepted, era_poem_counts,
                               min_era_poems=3, min_predictions=10, top_n=15):
    """
    For each qualifying era, compute:
    - top-N most suppressed words (predicted frequently, accepted rarely)
    - suppression rate = 1 - acceptance_rate
    - break down by function vs. content word
    """
    results = {}

    for era, pred_counts in era_predicted.items():
        n_poems = era_poem_counts[era]
        if n_poems < min_era_poems:
            continue

        acc_counts = era_accepted.get(era, Counter())
        total_tokens_predicted = sum(pred_counts.values())

        # Compute per-word suppression stats
        word_stats = []
        for word, n_pred in pred_counts.items():
            if n_pred < min_predictions:
                continue
            n_acc = acc_counts.get(word, 0)
            accept_rate = n_acc / n_pred
            suppress_rate = 1.0 - accept_rate
            word_stats.append({
                "word": word,
                "predicted": n_pred,
                "accepted": n_acc,
                "accept_rate": round(accept_rate, 3),
                "suppress_rate": round(suppress_rate, 3),
                "is_function": is_function_word(word),
            })

        # Sort by: high predictions AND high suppression (suppress_rate * log(n_pred))
        # This avoids privileging words predicted only 10 times
        import math
        word_stats.sort(
            key=lambda x: x["suppress_rate"] * math.log(x["predicted"] + 1),
            reverse=True
        )

        content_suppressed = [w for w in word_stats if not w["is_function"]][:top_n]
        all_suppressed = word_stats[:top_n]

        # Function word suppression rate (as a block)
        fw_pred = sum(w["predicted"] for w in word_stats if w["is_function"])
        fw_acc = sum(w["accepted"] for w in word_stats if w["is_function"])
        fw_suppress = (1 - fw_acc / fw_pred) if fw_pred > 0 else None

        cw_pred = sum(w["predicted"] for w in word_stats if not w["is_function"])
        cw_acc = sum(w["accepted"] for w in word_stats if not w["is_function"])
        cw_suppress = (1 - cw_acc / cw_pred) if cw_pred > 0 else None

        results[era] = {
            "n_poems": n_poems,
            "total_predictions": total_tokens_predicted,
            "top_suppressed_overall": all_suppressed,
            "top_suppressed_content": content_suppressed,
            "fw_suppression_rate": round(fw_suppress, 3) if fw_suppress else None,
            "cw_suppression_rate": round(cw_suppress, 3) if cw_suppress else None,
        }

    return results


def compute_era_divergence(era_results, target_eras=None):
    """
    Measure how distinctive each era's counter-lexicon is
    vs. the global average. High divergence = the era suppresses
    very different words than the overall pattern.
    """
    if target_eras:
        era_results = {k: v for k, v in era_results.items() if k in target_eras}

    # Build global counter
    global_suppress_words = set()
    for era_data in era_results.values():
        for w in era_data["top_suppressed_content"][:10]:
            global_suppress_words.add(w["word"])

    divergence = {}
    for era, data in era_results.items():
        era_top10 = {w["word"] for w in data["top_suppressed_content"][:10]}
        overlap = len(era_top10 & global_suppress_words)
        divergence[era] = {
            "overlap_with_global_top10": overlap,
            "unique_suppressions": len(era_top10 - global_suppress_words),
        }
    return divergence


def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"  {len(corpus)} texts loaded")

    print("Computing era-level suppressions...")
    era_predicted, era_accepted, era_poem_counts = get_era_suppressions(corpus)

    print(f"  {len(era_predicted)} eras found")

    print("Building counter-lexicons per era...")
    era_results = build_era_counter_lexicon(
        era_predicted, era_accepted, era_poem_counts,
        min_era_poems=3, min_predictions=8, top_n=15
    )
    print(f"  {len(era_results)} qualifying eras")

    # Save results
    out_path = os.path.join(RESULTS_DIR, "era_counter_lexicon.json")
    with open(out_path, "w") as f:
        json.dump(era_results, f, indent=2)
    print(f"  Saved to {out_path}")

    # Print summary table
    print("\n=== ERA COUNTER-LEXICON SUMMARY ===\n")
    print(f"{'Era':<22} {'Poems':>6} {'FW Supp':>8} {'CW Supp':>8}  Top Content-Word Suppressions")
    print("-" * 95)

    era_order = sorted(era_results.items(), key=lambda x: x[1]["n_poems"], reverse=True)

    for era, data in era_order:
        fw = data["fw_suppression_rate"]
        cw = data["cw_suppression_rate"]
        top5 = [w["word"] for w in data["top_suppressed_content"][:5]]
        fw_str = f"{fw:.1%}" if fw else " n/a"
        cw_str = f"{cw:.1%}" if cw else " n/a"
        print(f"{era:<22} {data['n_poems']:>6} {fw_str:>8} {cw_str:>8}  {', '.join(top5)}")

    # Print deep dive for a few interesting eras
    focus_eras = ["romantic", "modernist", "new_york_school", "confessional",
                  "victorian", "surrealist", "language", "beat", "old_english"]
    print("\n\n=== DEEP DIVES ===\n")
    for era in focus_eras:
        if era not in era_results:
            continue
        data = era_results[era]
        print(f"\n--- {era.upper()} (n={data['n_poems']}) ---")
        print(f"  FW suppression: {data['fw_suppression_rate']:.1%}  |  CW suppression: {data['cw_suppression_rate']:.1%}")
        print("  Top suppressed content words:")
        for w in data["top_suppressed_content"][:10]:
            print(f"    {w['word']:<20} predicted={w['predicted']:>4}  accepted={w['accepted']:>4}  suppressed={w['suppress_rate']:.0%}")

    return era_results


if __name__ == "__main__":
    main()
