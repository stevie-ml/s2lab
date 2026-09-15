"""
Confidence Trap Analysis: S2 at Low-Entropy Positions

When GPT-2 is highly confident (low entropy) but the poet deviates anyway,
these "confidence trap" moments represent the most deliberate, intentional
acts of literary choice. This experiment distinguishes:

1. Deliberate deviation (low entropy, high rank, high S2)
2. Exploratory choice (high entropy, high rank, S2 ≈ 0)
3. Expected choice (low rank, S2 ≤ 0)

We characterize which poets and eras have the most confidence traps,
and what the poet wrote vs. what GPT-2 expected at those moments.
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"

# Thresholds
LOW_ENTROPY_THRESHOLD = 2.0       # GPT-2 is confident (bits)
HIGH_RANK_THRESHOLD = 10          # Poet chose outside top-10 expected
HIGH_S2_THRESHOLD = 2.0           # Meaningfully positive S2


def classify_token(entropy, rank, s2):
    """Classify a token choice into one of three categories."""
    if entropy < LOW_ENTROPY_THRESHOLD and rank > HIGH_RANK_THRESHOLD and s2 > HIGH_S2_THRESHOLD:
        return "confidence_trap"
    elif rank > HIGH_RANK_THRESHOLD and abs(s2) < 1.0:
        return "exploratory"
    elif rank <= 3:
        return "expected"
    else:
        return "other"


def label_expected_word(alternatives):
    """Classify GPT-2's top expected token."""
    if not alternatives:
        return "unknown"
    top_tok = alternatives[0]["token"]
    if top_tok.strip() in ("", "\n"):
        return "newline"
    if top_tok.strip() in (",", ".", ";", ":", "!", "?", "-", "—"):
        return "punctuation"
    FUNCTION = {"the", "a", "an", "of", "in", "to", "and", "or", "but",
                "for", "with", "at", "by", "from", "is", "was", "are",
                "were", "that", "which", "who", "he", "she", "it", "they",
                "i", "you", "we", "not", "no", "have", "had", "be", "been"}
    if top_tok.strip().lower() in FUNCTION:
        return "function_word"
    return "content_word"


def analyze_poem(poem):
    meta = poem["metadata"]
    tokens = poem.get("tokens", [])
    if not tokens:
        return None

    traps = []
    exploratory = []
    expected_count = 0
    total = len(tokens)

    for tok in tokens:
        entropy = tok.get("entropy", 10.0)
        rank = tok.get("rank", 1)
        s2 = tok.get("s2", 0.0)
        alternatives = tok.get("alternatives", [])

        cat = classify_token(entropy, rank, s2)

        if cat == "confidence_trap":
            expected_label = label_expected_word(alternatives)
            top_expected = alternatives[0]["token"] if alternatives else "?"
            top_expected_prob = alternatives[0]["prob"] if alternatives else 0.0
            traps.append({
                "position": tok["position"],
                "token": tok["token"],
                "entropy": entropy,
                "rank": rank,
                "s2": s2,
                "surprisal": tok.get("surprisal", 0.0),
                "top_expected": top_expected,
                "top_expected_prob": top_expected_prob,
                "expected_label": expected_label,
                "context": tok.get("context_before", ""),
            })
        elif cat == "exploratory":
            exploratory.append(tok)
        elif cat == "expected":
            expected_count += 1

    return {
        "title": meta.get("title", "Unknown"),
        "author": meta.get("author", "Unknown"),
        "era": meta.get("era", "Unknown"),
        "total_tokens": total,
        "n_traps": len(traps),
        "trap_rate": len(traps) / total if total else 0.0,
        "n_exploratory": len(exploratory),
        "expected_count": expected_count,
        "traps": traps,
        "avg_trap_s2": sum(t["s2"] for t in traps) / len(traps) if traps else 0.0,
        "avg_trap_entropy": sum(t["entropy"] for t in traps) / len(traps) if traps else 0.0,
        "avg_trap_rank": sum(t["rank"] for t in traps) / len(traps) if traps else 0.0,
    }


def run():
    with open(CORPUS_PATH) as f:
        data = json.load(f)

    results = []
    for poem in data:
        if poem["metadata"].get("language", "en") != "en":
            continue
        r = analyze_poem(poem)
        if r:
            results.append(r)

    # Sort by trap rate
    results.sort(key=lambda x: x["trap_rate"], reverse=True)

    print("=" * 70)
    print("CONFIDENCE TRAP ANALYSIS")
    print(f"(Low-entropy threshold: H < {LOW_ENTROPY_THRESHOLD} bits)")
    print(f"(High-rank threshold: rank > {HIGH_RANK_THRESHOLD})")
    print("=" * 70)

    # Global stats
    total_traps = sum(r["n_traps"] for r in results)
    total_tokens = sum(r["total_tokens"] for r in results)
    print(f"\nCorpus: {len(results)} English poems, {total_tokens} tokens")
    print(f"Total confidence traps: {total_traps} ({100*total_traps/total_tokens:.2f}% of all tokens)\n")

    # By era
    era_stats = defaultdict(lambda: {"traps": 0, "tokens": 0, "poems": 0})
    for r in results:
        era = r["era"]
        era_stats[era]["traps"] += r["n_traps"]
        era_stats[era]["tokens"] += r["total_tokens"]
        era_stats[era]["poems"] += 1

    era_rows = [(era, v["poems"], v["traps"], v["tokens"],
                 100 * v["traps"] / v["tokens"] if v["tokens"] else 0)
                for era, v in era_stats.items()]
    era_rows.sort(key=lambda x: x[4], reverse=True)

    print("--- Confidence Trap Rate by Era ---")
    print(f"{'Era':<22} {'Poems':>6} {'Traps':>7} {'Tokens':>8} {'Rate%':>7}")
    print("-" * 55)
    for era, n_poems, traps, tokens, rate in era_rows:
        print(f"{era:<22} {n_poems:>6} {traps:>7} {tokens:>8} {rate:>7.2f}%")

    # Top poems by trap rate (min 30 tokens)
    top_poems = [r for r in results if r["total_tokens"] >= 30][:15]
    print("\n--- Top 15 Poems by Confidence Trap Rate ---")
    print(f"{'Title':<35} {'Author':<20} {'Rate%':>6} {'Traps':>6}")
    print("-" * 70)
    for r in top_poems:
        print(f"{r['title'][:34]:<35} {r['author'][:19]:<20} {100*r['trap_rate']:>6.2f}% {r['n_traps']:>6}")

    # What GPT-2 expected at confidence traps
    all_traps = []
    for r in results:
        for t in r["traps"]:
            all_traps.append({**t, "author": r["author"], "title": r["title"], "era": r["era"]})

    all_traps.sort(key=lambda x: x["s2"], reverse=True)

    # Category distribution of what GPT-2 expected
    expected_cats = defaultdict(int)
    for t in all_traps:
        expected_cats[t["expected_label"]] += 1

    print(f"\n--- What GPT-2 Expected at Confidence Trap Moments (n={len(all_traps)}) ---")
    for cat, count in sorted(expected_cats.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20}: {count:>4} ({100*count/len(all_traps):.1f}%)")

    # Top 20 highest-S2 confidence traps
    print("\n--- Top 20 Highest-S2 Confidence Traps ---")
    print(f"{'Author':<22} {'Wrote':<15} {'GPT-2 expected':<20} {'H(bits)':>8} {'S2':>6}")
    print("-" * 75)
    for t in all_traps[:20]:
        wrote = repr(t["token"].strip()[:12])
        expected = repr(t["top_expected"].strip()[:16])
        print(f"{t['author'][:21]:<22} {wrote:<15} {expected:<20} {t['entropy']:>8.3f} {t['s2']:>6.2f}")

    # Low-trap poets: those who mostly follow expectations
    low_trap = sorted([r for r in results if r["total_tokens"] >= 30],
                      key=lambda x: x["trap_rate"])[:10]
    print("\n--- 10 Lowest Trap-Rate Poets (most 'expected') ---")
    print(f"{'Title':<35} {'Author':<20} {'Rate%':>6}")
    print("-" * 65)
    for r in low_trap:
        print(f"{r['title'][:34]:<35} {r['author'][:19]:<20} {100*r['trap_rate']:>6.2f}%")

    # Average entropy at confidence trap moments vs. whole corpus
    all_entropies = []
    trap_entropies = []
    for poem in data:
        for tok in poem.get("tokens", []):
            if poem["metadata"].get("language", "en") != "en":
                continue
            all_entropies.append(tok.get("entropy", 0))
            if tok.get("rank", 1) > HIGH_RANK_THRESHOLD and tok.get("entropy", 10) < LOW_ENTROPY_THRESHOLD:
                trap_entropies.append(tok.get("entropy", 0))

    avg_global_h = sum(all_entropies) / len(all_entropies) if all_entropies else 0
    avg_trap_h = sum(trap_entropies) / len(trap_entropies) if trap_entropies else 0
    print(f"\nAverage entropy (all tokens): {avg_global_h:.3f} bits")
    print(f"Average entropy (confidence traps): {avg_trap_h:.3f} bits")
    print(f"→ At confidence traps, GPT-2 was {avg_global_h/avg_trap_h:.1f}x more confident than average")

    return results, all_traps


if __name__ == "__main__":
    run()
