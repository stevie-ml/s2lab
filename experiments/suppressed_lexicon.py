"""
Suppressed Lexicon: What Words Does GPT-2 Most Want to Write (but Poetry Refuses)?

For every token in the corpus, GPT-2's top-1 prediction is stored in the
`alternatives` field. This experiment asks:

  1. Which words does GPT-2 most frequently nominate as its top prediction?
  2. For each frequently predicted word, how often does the poet actually write it
     (acceptance rate)?
  3. The words with high prediction frequency but low acceptance are the
     "counter-lexicon" — the words poetry most systematically suppresses.

This produces an empirical, data-driven map of the Straussian gap at the lexical
level: not just categories (function vs content, as in straussian_taxonomy.md)
but the specific words that conventional language most wants, and poetry most often refuses.
"""

import json
import re
from collections import defaultdict

RESULTS = "results/corpus_results.json"
STANZA_ARTIFACT_THRESHOLD = 0.9


def is_artifact(tok):
    return tok.get("p_newline", 0) >= STANZA_ARTIFACT_THRESHOLD


def normalize(t):
    """Strip leading/trailing whitespace for grouping."""
    return t.strip()


def run():
    with open(RESULTS) as f:
        data = json.load(f)

    # Collect poetry texts only (exclude control/cliche_control)
    poetry = [p for p in data if p["metadata"].get("era") not in ("control", "cliche_control")]

    # ─── Pass 1: for each token with alternatives, record ───────────────────────
    # predicted_word → count of times it was GPT-2's top-1 prediction
    # predicted_word → count of times it was actually written by the poet (accepted)
    # predicted_word → list of S2 values when this word was the prediction (accepted)
    # predicted_word → list of S2 values when this word was predicted but NOT written
    #
    # Also track which words APPEAR in the corpus and their average S2.

    predicted_count = defaultdict(int)  # GPT-2 top-1 nomination count
    accepted_count = defaultdict(int)   # times poet wrote the top-1 prediction
    rejected_s2 = defaultdict(list)     # S2 at rejection of this predicted word
    written_count = defaultdict(int)    # times this word appeared as actual token
    written_s2 = defaultdict(list)      # S2 of this word when written

    # For era-level breakdown
    era_predicted = defaultdict(lambda: defaultdict(int))
    era_accepted = defaultdict(lambda: defaultdict(int))

    total_tokens = 0
    artifact_tokens = 0

    for poem in poetry:
        era = poem["metadata"].get("era", "unknown")
        for tok in poem["tokens"]:
            if is_artifact(tok):
                artifact_tokens += 1
                continue
            total_tokens += 1

            actual = tok["token"]
            s2 = tok.get("s2", 0)
            alts = tok.get("alternatives", [])

            norm_actual = normalize(actual)
            written_count[norm_actual] += 1
            written_s2[norm_actual].append(s2)

            if alts:
                top1 = normalize(alts[0]["token"])
                predicted_count[top1] += 1
                era_predicted[era][top1] += 1

                if normalize(actual) == top1:
                    accepted_count[top1] += 1
                    era_accepted[era][top1] += 1
                else:
                    rejected_s2[top1].append(s2)

    print(f"Clean tokens: {total_tokens:,} (artifact excluded: {artifact_tokens:,})")
    print(f"Unique words predicted as top-1: {len(predicted_count):,}")
    print(f"Unique words written: {len(written_count):,}")

    # ─── Analysis 1: Most Frequently Predicted Words ────────────────────────────
    top_predicted = sorted(predicted_count.items(), key=lambda x: -x[1])[:50]
    print("\n=== Top 30 Most-Predicted (GPT-2 Top-1) Words in Poetry ===")
    print(f"{'Word':<20} {'Predicted':>10} {'Accepted':>10} {'Acceptance%':>12} {'Avg_rej_S2':>12}")
    for word, pred_n in top_predicted[:30]:
        acc_n = accepted_count[word]
        rate = 100.0 * acc_n / pred_n if pred_n else 0
        rej_s2_vals = rejected_s2[word]
        avg_rej_s2 = sum(rej_s2_vals) / len(rej_s2_vals) if rej_s2_vals else 0
        print(f"{repr(word):<20} {pred_n:>10} {acc_n:>10} {rate:>11.1f}% {avg_rej_s2:>12.3f}")

    # ─── Analysis 2: The Counter-Lexicon ────────────────────────────────────────
    # Words predicted 20+ times but with lowest acceptance rate
    min_pred = 20
    filtered = [(w, n) for w, n in predicted_count.items() if n >= min_pred]

    counter_lexicon = sorted(filtered, key=lambda x: accepted_count[x[0]] / x[1])
    print(f"\n=== Counter-Lexicon: Most Suppressed Words (predicted ≥ {min_pred}x, lowest acceptance) ===")
    print(f"{'Word':<20} {'Predicted':>10} {'Accepted':>10} {'Acceptance%':>12} {'Avg_rej_S2':>12}")
    for word, pred_n in counter_lexicon[:25]:
        acc_n = accepted_count[word]
        rate = 100.0 * acc_n / pred_n if pred_n else 0
        rej_s2_vals = rejected_s2[word]
        avg_rej_s2 = sum(rej_s2_vals) / len(rej_s2_vals) if rej_s2_vals else 0
        print(f"{repr(word):<20} {pred_n:>10} {acc_n:>10} {rate:>11.1f}% {avg_rej_s2:>12.3f}")

    # ─── Analysis 3: What replaces the suppressed words? ─────────────────────────
    # For top-N suppressed words, what did the poet write instead?
    print("\n=== What Does Poetry Write Instead of the Most-Suppressed Word? ===")

    suppressed_top = counter_lexicon[:10]
    for word, pred_n in suppressed_top:
        acc_n = accepted_count[word]
        rate = 100.0 * acc_n / pred_n
        # Find actual tokens when this word was predicted but not written
        replacements = defaultdict(int)
        for poem in poetry:
            era = poem["metadata"].get("era", "unknown")
            for tok in poem["tokens"]:
                if is_artifact(tok):
                    continue
                alts = tok.get("alternatives", [])
                if alts and normalize(alts[0]["token"]) == word:
                    actual_norm = normalize(tok["token"])
                    if actual_norm != word:
                        replacements[actual_norm] += 1
        top_replacements = sorted(replacements.items(), key=lambda x: -x[1])[:8]
        rep_str = ", ".join(f"{repr(r)} ({n})" for r, n in top_replacements)
        print(f"  {repr(word)} ({rate:.0f}% acc) → {rep_str}")

    # ─── Analysis 4: High-acceptance vs low-acceptance words ────────────────────
    # Words that poetry rarely suppresses (acceptance > 80%) vs often suppresses
    common_threshold = 15
    high_acc = [(w, n) for w, n in predicted_count.items()
                if n >= common_threshold and accepted_count[w] / n >= 0.8]
    low_acc = [(w, n) for w, n in predicted_count.items()
               if n >= common_threshold and accepted_count[w] / n < 0.2]

    print(f"\n=== High-Acceptance Words (predicted ≥{common_threshold}x, ≥80% accepted) ===")
    high_acc_sorted = sorted(high_acc, key=lambda x: -accepted_count[x[0]] / x[1])
    for w, n in high_acc_sorted[:20]:
        rate = 100.0 * accepted_count[w] / n
        avg_s2 = sum(written_s2[normalize(w)]) / len(written_s2[normalize(w)]) if written_s2[normalize(w)] else 0
        print(f"  {repr(w):<18} pred={n:>4}  acc={rate:>5.1f}%  avg_s2={avg_s2:>6.3f}")

    print(f"\n=== Low-Acceptance Words (predicted ≥{common_threshold}x, <20% accepted) ===")
    low_acc_sorted = sorted(low_acc, key=lambda x: accepted_count[x[0]] / x[1])
    for w, n in low_acc_sorted[:20]:
        rate = 100.0 * accepted_count[w] / n
        rej_s2_vals = rejected_s2[w]
        avg_rej = sum(rej_s2_vals) / len(rej_s2_vals) if rej_s2_vals else 0
        print(f"  {repr(w):<18} pred={n:>4}  acc={rate:>5.1f}%  avg_rej_s2={avg_rej:>6.3f}")

    # ─── Analysis 5: Era-level suppression of specific words ─────────────────────
    # For the most suppressed words, which era suppresses them most?
    key_suppressed = [w for w, n in counter_lexicon[:5]]
    print("\n=== Era-Level Suppression of Top-5 Counter-Lexicon Words ===")
    print(f"{'Era':<25} " + " ".join(f"{repr(w)[:8]:<12}" for w in key_suppressed))
    eras_present = sorted(era_predicted.keys())
    for era in eras_present:
        row = []
        for w in key_suppressed:
            pred = era_predicted[era][w]
            acc = era_accepted[era][w]
            if pred > 0:
                rate = 100.0 * acc / pred
                row.append(f"{rate:>5.1f}%({pred})")
            else:
                row.append("  n/a    ")
        print(f"{era:<25} " + " ".join(f"{r:<12}" for r in row))

    # ─── Summary statistics ──────────────────────────────────────────────────────
    # Overall acceptance rate for categories
    function_words = {"the", "a", "an", "of", "in", "to", "and", "or", "but", "for",
                      "with", "at", "by", "from", "as", "on", "not", "so", "if",
                      "it", "he", "she", "they", "we", "I", "that", "this", "which"}
    punct_words = {",", ".", ";", ":", "!", "?", "'s", "'t", "—", "-", "(", ")"}

    def category_acceptance(words_set):
        total_pred = sum(predicted_count[w] for w in words_set if w in predicted_count)
        total_acc = sum(accepted_count[w] for w in words_set if w in predicted_count)
        return 100.0 * total_acc / total_pred if total_pred else 0

    print("\n=== Acceptance Rate by Word Category ===")
    print(f"  Function words: {category_acceptance(function_words):.1f}%")
    print(f"  Punctuation: {category_acceptance(punct_words):.1f}%")

    # Return data for markdown
    return {
        "total_tokens": total_tokens,
        "total_predicted": sum(predicted_count.values()),
        "top_predicted": [(w, predicted_count[w], accepted_count[w],
                          100.0 * accepted_count[w] / predicted_count[w])
                         for w, n in top_predicted[:25]],
        "counter_lexicon": [(w, predicted_count[w], accepted_count[w],
                             100.0 * accepted_count[w] / predicted_count[w],
                             sum(rejected_s2[w]) / len(rejected_s2[w]) if rejected_s2[w] else 0)
                           for w, n in counter_lexicon[:25]],
        "function_acc": category_acceptance(function_words),
        "punct_acc": category_acceptance(punct_words),
    }


if __name__ == "__main__":
    results = run()
    with open("results/suppressed_lexicon.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to results/suppressed_lexicon.json")
