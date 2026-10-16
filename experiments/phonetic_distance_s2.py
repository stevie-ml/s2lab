"""
Phonetic Distance from the Top Prediction

Research question: When poets deviate from GPT-2's top prediction,
do they choose words that SOUND similar (phonetic substitution) or
words that sound completely different?

Hypothesis: High-S2 moments may involve words that are phonetically
close to the top prediction but semantically different — a 'phonetic
Straussian gap' where sound is preserved while meaning diverges.

Method:
- For each token, compute edit-distance-based phonetic proximity
  between the poet's choice and GPT-2's #1 prediction
- Bin by S2 level and compare phonetic proximity distributions
- Look at specific examples of phonetically-close high-S2 substitutions
- Compare across poetry eras and prose control
"""

import json
import re
from collections import defaultdict

def load_corpus(path="results/corpus_results.json"):
    with open(path) as f:
        return json.load(f)

def edit_distance(s1, s2):
    """Levenshtein edit distance."""
    s1 = s1.strip().lower()
    s2 = s2.strip().lower()
    m, n = len(s1), len(s2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if s1[i-1] == s2[j-1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j-1])
            prev = temp
    return dp[n]

def phonetic_similarity(tok1, tok2):
    """
    Normalized phonetic similarity score: 1 = identical, 0 = completely different.
    Based on character-level edit distance, normalized by max length.
    """
    t1 = tok1.strip().lower()
    t2 = tok2.strip().lower()
    if not t1 or not t2:
        return 0.0
    if t1 == t2:
        return 1.0
    max_len = max(len(t1), len(t2))
    dist = edit_distance(t1, t2)
    return 1.0 - dist / max_len

def starts_same(tok1, tok2):
    t1 = tok1.strip().lower().lstrip('Ġ▁ ')
    t2 = tok2.strip().lower().lstrip('Ġ▁ ')
    return len(t1) > 0 and len(t2) > 0 and t1[0] == t2[0]

def is_alpha_token(tok):
    """Filter to alphabetic tokens only (skip punctuation, numbers, special)."""
    clean = tok.strip().lstrip('Ġ▁ ')
    return clean.isalpha() and len(clean) > 1

def classify_s2(s2_val):
    if s2_val < -4:
        return "very_low"
    elif s2_val < -1:
        return "low"
    elif s2_val < 1:
        return "neutral"
    elif s2_val < 4:
        return "moderate"
    elif s2_val < 8:
        return "high"
    else:
        return "very_high"

def main():
    corpus = load_corpus()

    # Collect metrics per token
    bins = defaultdict(list)   # s2_class -> list of phonetic_sim scores
    era_bins = defaultdict(lambda: defaultdict(list))  # era -> s2_class -> [sim]

    # High-S2 phonetically close examples
    close_high_s2 = []
    far_high_s2 = []

    # All phonetic sim vs s2 pairs
    all_pairs = []

    for poem in corpus:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        tokens = poem.get("tokens", [])

        for tok_data in tokens:
            token = tok_data.get("token", "")
            s2 = tok_data.get("s2", 0.0)
            entropy = tok_data.get("entropy", 0.0)
            surprisal = tok_data.get("surprisal", 0.0)
            alternatives = tok_data.get("alternatives", [])
            p_newline = tok_data.get("p_newline", 0.0)

            # Skip stanza-break artifact positions
            if p_newline > 0.9:
                continue

            # Skip non-alphabetic tokens
            if not is_alpha_token(token):
                continue

            if not alternatives:
                continue

            top_pred = alternatives[0].get("token", "")
            if not is_alpha_token(top_pred):
                continue

            sim = phonetic_similarity(token, top_pred)
            same_start = starts_same(token, top_pred)
            s2_class = classify_s2(s2)

            bins[s2_class].append(sim)
            era_bins[era][s2_class].append(sim)
            all_pairs.append((s2, sim, token, top_pred, era))

            # Collect interesting examples
            if s2 > 6 and sim > 0.6:
                close_high_s2.append({
                    "token": token, "top_pred": top_pred,
                    "s2": round(s2, 2), "sim": round(sim, 2),
                    "era": era, "entropy": round(entropy, 2)
                })
            elif s2 > 6 and sim < 0.2:
                far_high_s2.append({
                    "token": token, "top_pred": top_pred,
                    "s2": round(s2, 2), "sim": round(sim, 2),
                    "era": era, "entropy": round(entropy, 2)
                })

    # Compute statistics per bin
    print("\n=== PHONETIC PROXIMITY BY S2 CLASS ===")
    print(f"{'S2 Class':<12} {'N':>6} {'Mean Sim':>10} {'> 0.5 (%)':>12} {'Same Start (%)':>15}")
    print("-" * 60)

    order = ["very_low", "low", "neutral", "moderate", "high", "very_high"]
    results = {}
    for cls in order:
        sims = bins[cls]
        if not sims:
            continue
        mean_sim = sum(sims) / len(sims)
        frac_close = sum(1 for s in sims if s > 0.5) / len(sims)

        # Recompute same_start for this bin
        same_starts = sum(
            1 for (s2, sim, tok, pred, era) in all_pairs
            if classify_s2(s2) == cls and starts_same(tok, pred)
        )
        n = len(sims)
        same_start_frac = same_starts / n if n > 0 else 0

        results[cls] = {
            "n": n,
            "mean_sim": round(mean_sim, 4),
            "frac_close": round(frac_close, 4),
            "frac_same_start": round(same_start_frac, 4)
        }
        print(f"{cls:<12} {n:>6} {mean_sim:>10.4f} {frac_close*100:>11.1f}% {same_start_frac*100:>14.1f}%")

    # S2 vs phonetic sim correlation
    if all_pairs:
        s2_vals = [p[0] for p in all_pairs]
        sim_vals = [p[1] for p in all_pairs]
        n = len(s2_vals)
        mean_s2 = sum(s2_vals) / n
        mean_sim = sum(sim_vals) / n
        cov = sum((s - mean_s2) * (sim - mean_sim) for s, sim in zip(s2_vals, sim_vals)) / n
        std_s2 = (sum((s - mean_s2)**2 for s in s2_vals) / n) ** 0.5
        std_sim = (sum((s - mean_sim)**2 for s in sim_vals) / n) ** 0.5
        corr = cov / (std_s2 * std_sim) if std_s2 > 0 and std_sim > 0 else 0
        print(f"\nPearson correlation (S2 vs phonetic sim): {corr:.4f} (n={n})")

    # Era comparison at high S2
    print("\n=== PHONETIC SIMILARITY AT HIGH S2 BY ERA (≥6 S2 tokens) ===")
    era_stats = []
    for era, era_data in era_bins.items():
        high = era_data.get("high", []) + era_data.get("very_high", [])
        if len(high) < 5:
            continue
        mean_h = sum(high) / len(high)
        era_stats.append((era, len(high), mean_h))
    era_stats.sort(key=lambda x: -x[2])
    print(f"{'Era':<25} {'N (high S2)':>12} {'Mean Sim':>10}")
    for era, n, mean_h in era_stats[:20]:
        print(f"{era:<25} {n:>12} {mean_h:>10.4f}")

    # Show examples: phonetically-close high-S2 substitutions
    print(f"\n=== TOP PHONETICALLY-CLOSE HIGH-S2 SUBSTITUTIONS (top 15) ===")
    close_high_s2.sort(key=lambda x: -x["s2"])
    print(f"{'Poet chose':<15} {'GPT-2 predicted':<20} {'S2':>6} {'Sim':>6} {'Era':<20}")
    for ex in close_high_s2[:15]:
        print(f"{ex['token']:<15} {ex['top_pred']:<20} {ex['s2']:>6.2f} {ex['sim']:>6.2f} {ex['era']:<20}")

    print(f"\n=== TOP PHONETICALLY-FAR HIGH-S2 SUBSTITUTIONS (top 15) ===")
    far_high_s2.sort(key=lambda x: -x["s2"])
    print(f"{'Poet chose':<15} {'GPT-2 predicted':<20} {'S2':>6} {'Sim':>6} {'Era':<20}")
    for ex in far_high_s2[:15]:
        print(f"{ex['token']:<15} {ex['top_pred']:<20} {ex['s2']:>6.2f} {ex['sim']:>6.2f} {ex['era']:<20}")

    # Save results
    output = {
        "s2_bins": results,
        "correlation_s2_phonetic_sim": round(corr, 4) if all_pairs else None,
        "n_total_tokens": len(all_pairs),
        "close_high_s2_examples": close_high_s2[:30],
        "far_high_s2_examples": far_high_s2[:30],
    }
    with open("results/phonetic_distance_s2.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nResults saved to results/phonetic_distance_s2.json")
    return output

if __name__ == "__main__":
    main()
