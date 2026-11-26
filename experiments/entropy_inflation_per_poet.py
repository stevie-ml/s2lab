"""
Entropy Inflation Per Poet: Chaos Navigation vs. Certain Defiance

The genuine_surprise_catalog.md finding revealed two distinct modes of poetic deviation:
  - "Chaos Navigation" (Gertrude Stein): poet raises entropy everywhere, making every token
    hard to predict, but S2 stays low because the model is already uncertain
  - "Certain Defiance" (Hopkins): poet operates in tight contexts where the model is confident,
    then deviates sharply — producing high S2

This experiment quantifies WHICH POETS USE WHICH STRATEGY by measuring:
  1. Mean context entropy per poet (how uncertain is GPT-2 when reading this poet?)
  2. Mean S2 per poet (how often does the poet exceed what uncertainty warrants?)
  3. Entropy Inflation Ratio = poet_entropy / corpus_mean_entropy
  4. Classification into quadrants:
     - HIGH entropy + HIGH S2: "Both modes" (rare)
     - HIGH entropy + LOW S2:  "Chaos Navigation" (Stein mode)
     - LOW entropy + HIGH S2:  "Certain Defiance" (Hopkins mode)
     - LOW entropy + LOW S2:   "Smooth Conformity" (prose-like)
"""

import json
import os
import statistics
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "entropy_inflation_per_poet.json")

ARTIFACT_P = 0.90  # p(newline) threshold to exclude stanza-break artifacts
MIN_TOKENS = 50    # minimum tokens for reliable stats


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def is_artifact(tok):
    # Use precomputed p_newline if available (much faster)
    if "p_newline" in tok:
        return tok["p_newline"] >= ARTIFACT_P
    return newline_prob(tok) >= ARTIFACT_P


def is_whitespace(tok):
    return tok["token"].strip() == ""


def get_entropy(tok):
    """Entropy of GPT-2's predictive distribution at this position."""
    import math
    entropy = 0.0
    for alt in tok["alternatives"]:
        p = alt["prob"]
        if p > 0:
            entropy -= p * math.log2(p)
    # Add residual entropy from non-top-k probability mass
    # (not available, so use top-k only as approximation)
    return entropy


def get_surprisal(tok):
    """Surprisal of the actual chosen token."""
    import math
    actual_token = tok["token"]
    for alt in tok["alternatives"]:
        if alt["token"] == actual_token:
            p = alt["prob"]
            if p > 0:
                return -math.log2(p)
            break
    # If not in top-k, use the minimum probability in alternatives as upper bound
    min_prob = min(a["prob"] for a in tok["alternatives"])
    if min_prob > 0:
        return -math.log2(min_prob) + 1.0  # conservative estimate
    return 20.0  # fallback for zero probability


def compute_s2(tok):
    return tok.get("s2", get_surprisal(tok) - get_entropy(tok))


def main():
    print("Loading corpus results...")
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    # Gather per-poet stats (artifact-free)
    poet_entropies = defaultdict(list)
    poet_s2s = defaultdict(list)
    poet_meta = {}  # author -> {era, n_poems}

    corpus_entropies = []  # all tokens for baseline

    for poem in data:
        meta = poem.get("metadata", {})
        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")

        if author not in poet_meta:
            poet_meta[author] = {"era": era, "n_poems": 0}
        poet_meta[author]["n_poems"] += 1

        for tok in poem.get("tokens", []):
            if is_artifact(tok) or is_whitespace(tok):
                continue

            # Use precomputed entropy and s2 from the JSON if available
            entropy = tok.get("entropy", get_entropy(tok))
            s2 = tok.get("s2", compute_s2(tok))

            corpus_entropies.append(entropy)
            poet_entropies[author].append(entropy)
            poet_s2s[author].append(s2)

    corpus_mean_entropy = statistics.mean(corpus_entropies)
    corpus_mean_s2 = statistics.mean(
        s2 for s2s in poet_s2s.values() for s2 in s2s
    )
    corpus_sd_entropy = statistics.stdev(corpus_entropies)

    print(f"Corpus mean entropy: {corpus_mean_entropy:.3f} bits")
    print(f"Corpus mean S2:      {corpus_mean_s2:.3f} bits")
    print(f"Total clean tokens:  {len(corpus_entropies)}")

    # Per-poet statistics
    results = []
    for author, entropies in poet_entropies.items():
        s2s = poet_s2s[author]
        if len(entropies) < MIN_TOKENS:
            continue

        mean_e = statistics.mean(entropies)
        mean_s2 = statistics.mean(s2s)
        sd_s2 = statistics.stdev(s2s) if len(s2s) > 1 else 0.0
        entropy_inflation = mean_e / corpus_mean_entropy

        # Quadrant classification
        e_above = mean_e > corpus_mean_entropy
        s2_above = mean_s2 > corpus_mean_s2

        if e_above and s2_above:
            mode = "BOTH_MODES"
        elif e_above and not s2_above:
            mode = "CHAOS_NAVIGATION"
        elif not e_above and s2_above:
            mode = "CERTAIN_DEFIANCE"
        else:
            mode = "SMOOTH_CONFORMITY"

        # Fraction of tokens with high S2 in low-entropy contexts
        precise_deviations = sum(
            1 for e, s in zip(entropies, s2s)
            if e < corpus_mean_entropy and s > 0
        )
        low_entropy_tokens = sum(1 for e in entropies if e < corpus_mean_entropy)
        precision_rate = precise_deviations / low_entropy_tokens if low_entropy_tokens > 0 else 0

        results.append({
            "author": author,
            "era": poet_meta[author]["era"],
            "n_poems": poet_meta[author]["n_poems"],
            "n_tokens": len(entropies),
            "mean_entropy": round(mean_e, 4),
            "mean_s2": round(mean_s2, 4),
            "sd_s2": round(sd_s2, 4),
            "entropy_inflation": round(entropy_inflation, 4),
            "precision_rate": round(precision_rate, 4),
            "mode": mode,
        })

    # Sort by entropy inflation
    results.sort(key=lambda r: r["entropy_inflation"], reverse=True)

    output = {
        "corpus_mean_entropy": round(corpus_mean_entropy, 4),
        "corpus_mean_s2": round(corpus_mean_s2, 4),
        "corpus_sd_entropy": round(corpus_sd_entropy, 4),
        "total_clean_tokens": len(corpus_entropies),
        "poets": results,
    }

    with open(OUT_JSON, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {OUT_JSON}")
    print(f"\n{'Author':<40} {'Mode':<20} {'Entropy':>8} {'Infl':>6} {'S2':>8} {'Precision':>10}")
    print("-" * 100)
    for r in results[:30]:
        print(f"{r['author']:<40} {r['mode']:<20} {r['mean_entropy']:>8.3f} {r['entropy_inflation']:>6.3f} {r['mean_s2']:>8.3f} {r['precision_rate']:>10.3f}")

    # Also print by mode
    print("\n--- CERTAIN DEFIANCE (low entropy + high S2) ---")
    defiance = [r for r in results if r["mode"] == "CERTAIN_DEFIANCE"]
    defiance.sort(key=lambda r: r["mean_s2"], reverse=True)
    for r in defiance[:10]:
        print(f"  {r['author']:<40} entropy={r['mean_entropy']:.3f}  S2={r['mean_s2']:.3f}  precision={r['precision_rate']:.3f}")

    print("\n--- CHAOS NAVIGATION (high entropy + low S2) ---")
    chaos = [r for r in results if r["mode"] == "CHAOS_NAVIGATION"]
    chaos.sort(key=lambda r: r["entropy_inflation"], reverse=True)
    for r in chaos[:10]:
        print(f"  {r['author']:<40} entropy={r['mean_entropy']:.3f}  infl={r['entropy_inflation']:.3f}  S2={r['mean_s2']:.3f}")

    print("\n--- SMOOTH CONFORMITY (low entropy + low S2) ---")
    smooth = [r for r in results if r["mode"] == "SMOOTH_CONFORMITY"]
    smooth.sort(key=lambda r: r["mean_s2"])
    for r in smooth[:10]:
        print(f"  {r['author']:<40} entropy={r['mean_entropy']:.3f}  S2={r['mean_s2']:.3f}")

    print("\n--- BOTH MODES (high entropy + high S2) ---")
    both = [r for r in results if r["mode"] == "BOTH_MODES"]
    both.sort(key=lambda r: r["mean_s2"], reverse=True)
    for r in both[:10]:
        print(f"  {r['author']:<40} entropy={r['mean_entropy']:.3f}  S2={r['mean_s2']:.3f}")

    return output


if __name__ == "__main__":
    main()
