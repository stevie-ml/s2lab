"""
The Positive Counter-Lexicon: What Words Does Poetry Write MORE Than GPT-2 Expects?

Complement to suppressed_lexicon.py. While that experiment found words GPT-2 frequently
predicts but poetry rarely writes, this asks the inverse:

  Which words appear in poetry MORE often than GPT-2 ranked them?

A word with consistently low rank (GPT-2 barely considered it) but high actual occurrence
in the corpus is a distinctively POETIC word — one that marks the register of poetry
as distinct from "average" language.

This produces an empirical "positive counter-lexicon": the vocabulary that actual poets
prefer but statistical language models underweight.
"""

import json
from collections import defaultdict

RESULTS = "results/corpus_results.json"
STANZA_ARTIFACT_THRESHOLD = 0.9


def is_artifact(tok):
    return tok.get("p_newline", 0) >= STANZA_ARTIFACT_THRESHOLD


def normalize(t):
    return t.strip()


def run():
    with open(RESULTS) as f:
        data = json.load(f)

    poetry = [p for p in data if p["metadata"].get("era") not in ("control", "cliche_control")]

    # For each word that appears in the corpus:
    # - word_count[w]: how many times w was written (as actual token, normalized)
    # - word_rank_sum[w]: sum of GPT-2 ranks when this word was written
    # - word_s2_sum[w]: sum of S2 values
    # - word_in_top10[w]: how many times this word appeared in GPT-2's top-10 alternatives
    # - word_top1_count[w]: how many times this word was GPT-2's top-1 prediction
    # - word_high_rank_count[w]: how many times the poet wrote it when rank > 50

    word_count = defaultdict(int)
    word_rank_sum = defaultdict(int)
    word_s2_sum = defaultdict(float)
    word_in_top10 = defaultdict(int)
    word_top1_count = defaultdict(int)
    word_high_rank = defaultdict(int)   # rank > 50 = well outside model's menu
    word_ranks = defaultdict(list)

    era_word = defaultdict(lambda: defaultdict(int))

    total_tokens = 0

    for poem in poetry:
        era = poem["metadata"].get("era", "unknown")
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            total_tokens += 1

            actual = normalize(tok["token"])
            rank = tok.get("rank", None)
            s2 = tok.get("s2", 0)
            alts = tok.get("alternatives", [])

            if actual.isspace() or actual == "":
                continue

            word_count[actual] += 1
            era_word[era][actual] += 1

            if rank is not None:
                word_rank_sum[actual] += rank
                word_ranks[actual].append(rank)
                if rank > 50:
                    word_high_rank[actual] += 1

            word_s2_sum[actual] += s2

            # Check if word appears in GPT-2's top-10 alternatives for this position
            alt_tokens = [normalize(a["token"]) for a in alts]
            if actual in alt_tokens:
                word_in_top10[actual] += 1
            if alts and normalize(alts[0]["token"]) == actual:
                word_top1_count[actual] += 1

    # Positive counter-lexicon: words that:
    # 1. Appear at least N times in the corpus
    # 2. Have a high average rank (GPT-2 rarely put them in top-10)
    # 3. Were rarely GPT-2's top-1 prediction
    # (Ratio of word_count to word_top1_count = "poetic excess")

    min_count = 10

    # Average rank per word
    word_avg_rank = {w: word_rank_sum[w] / word_count[w]
                    for w in word_count if word_count[w] >= min_count}

    # Sort by average rank (highest = most consistently unexpected by GPT-2)
    top_unexpected = sorted(word_avg_rank.items(), key=lambda x: -x[1])

    print(f"Clean tokens: {total_tokens:,}")
    print(f"Unique words (≥{min_count} occurrences): {len(word_avg_rank):,}")

    print(f"\n=== The Positive Counter-Lexicon: Most Consistently Unexpected Words (≥{min_count} occurrences) ===")
    print(f"{'Word':<20} {'Count':>7} {'Avg Rank':>10} {'Avg S2':>9} {'Top1%':>8} {'High-rank%':>12}")
    for word, avg_rank in top_unexpected[:40]:
        n = word_count[word]
        avg_s2 = word_s2_sum[word] / n
        top1_rate = 100.0 * word_top1_count[word] / n
        high_rank_rate = 100.0 * word_high_rank[word] / n
        print(f"{repr(word):<20} {n:>7} {avg_rank:>10.1f} {avg_s2:>9.3f} {top1_rate:>7.1f}% {high_rank_rate:>11.1f}%")

    print(f"\n=== Most Expected Words Actually Written (lowest avg rank) ===")
    bottom_unexpected = sorted(word_avg_rank.items(), key=lambda x: x[1])
    print(f"{'Word':<20} {'Count':>7} {'Avg Rank':>10} {'Avg S2':>9} {'Top1%':>8}")
    for word, avg_rank in bottom_unexpected[:25]:
        n = word_count[word]
        avg_s2 = word_s2_sum[word] / n
        top1_rate = 100.0 * word_top1_count[word] / n
        print(f"{repr(word):<20} {n:>7} {avg_rank:>10.1f} {avg_s2:>9.3f} {top1_rate:>7.1f}%")

    # Era breakdown: which era produces the most "positive counter-lexicon" words?
    # Proxy: for each era, average rank of all its tokens
    print("\n=== Era-Level Average Rank (higher = more systematically unexpected) ===")
    era_avg_rank = {}
    era_total_rank = defaultdict(int)
    era_total_count = defaultdict(int)
    for poem in poetry:
        era = poem["metadata"].get("era", "unknown")
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            rank = tok.get("rank")
            if rank is not None:
                era_total_rank[era] += rank
                era_total_count[era] += 1

    for era in sorted(era_total_rank.keys(), key=lambda e: -era_total_rank[e] / era_total_count[e] if era_total_count[e] else 0):
        n = era_total_count[era]
        avg_r = era_total_rank[era] / n if n else 0
        print(f"  {era:<30} n={n:>5}  avg_rank={avg_r:>7.1f}")

    # Most unexpected words by specific era
    print("\n=== Top-10 Most Unexpected Words by Era (avg rank of all tokens ≥5 per era) ===")
    interesting_eras = ["beat", "language", "modernist", "romantic", "new_york_school",
                        "confessional", "haiku", "victorian", "found_poetry", "prose_poetry"]
    for era in interesting_eras:
        # get word counts in this era
        era_words = [(w, n) for w, n in era_word[era].items() if n >= 3]
        if not era_words:
            continue
        # sort by average rank of that word overall (proxy for "unexpected in general")
        era_words_ranked = [(w, n, word_avg_rank.get(w, 0)) for w, n in era_words
                            if w in word_avg_rank]
        top_for_era = sorted(era_words_ranked, key=lambda x: -x[2])[:6]
        word_str = ", ".join(f"{repr(w)} (rk={avg_r:.0f})" for w, n, avg_r in top_for_era)
        print(f"  {era:<20}: {word_str}")

    return {
        "top_unexpected": [(w, word_count[w], avg_rank, word_s2_sum[w] / word_count[w])
                           for w, avg_rank in top_unexpected[:30]],
    }


if __name__ == "__main__":
    results = run()
    with open("results/positive_counter_lexicon.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to results/positive_counter_lexicon.json")
