"""
Rhyme-Slot Phonetic Targeting

Research question: Do line-final (rhyme-slot) tokens achieve 'phonetic-fidelity
surprise' — high S2 + high phonetic similarity to the top prediction — more
often than mid-line tokens?

Hypothesis: In rhymed verse, the poet is constrained to choose a line-final word
that sounds like a previous line-final word. This means the rhyme sound is
'expected' in a local sense (the reader/model anticipates the phonetic pattern),
but the specific word chosen may violate semantic expectations. Result: rhyme-slot
tokens should show higher phonetic similarity to GPT-2's top prediction at
equivalent S2 levels, compared to non-rhyme tokens.

Method:
1. Load corpus_results.json
2. For each poem, identify line-final tokens (last token before a newline)
3. Compute phonetic similarity to top-1 prediction for every non-punctuation token
4. Compare line-final vs mid-line distribution of:
   - S2 levels
   - Phonetic similarity to top prediction
   - 'Phonetic-fidelity surprise' (high S2 + high phonetic sim)
5. Separate rhymed poems from free-verse poems using end-rhyme detection heuristic
6. Compare rhymed-line-final vs free-verse-line-final tokens
"""

import json
import re
from collections import defaultdict
import math

def load_corpus(path="results/corpus_results.json"):
    with open(path) as f:
        return json.load(f)

def edit_distance(s1, s2):
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
    t1 = tok1.strip().lower()
    t2 = tok2.strip().lower()
    if not t1 or not t2:
        return 0.0
    if t1 == t2:
        return 1.0
    max_len = max(len(t1), len(t2))
    dist = edit_distance(t1, t2)
    return 1.0 - dist / max_len

def is_alphabetic_word(token):
    """Filter to real alphabetic words only."""
    clean = token.strip()
    return bool(re.match(r"^[a-zA-Z']+$", clean)) and len(clean) >= 2

def detect_rhyme_scheme(line_final_words):
    """
    Detect if a poem has end-rhyme by checking if at least 30% of
    line-final word pairs share the last 3 characters.
    Returns (has_rhyme, rhyme_density).
    """
    words = [w.strip().lower() for w in line_final_words if re.match(r"^[a-zA-Z]+$", w.strip())]
    if len(words) < 4:
        return False, 0.0

    rhyme_pairs = 0
    total_pairs = 0
    for i in range(len(words)):
        for j in range(i+1, len(words)):
            total_pairs += 1
            if len(words[i]) >= 3 and len(words[j]) >= 3:
                if words[i][-3:] == words[j][-3:]:
                    rhyme_pairs += 1

    if total_pairs == 0:
        return False, 0.0
    density = rhyme_pairs / total_pairs
    return density >= 0.08, density  # ~8%+ rhyme pair density = rhymed poem

def analyze_rhyme_slot_phonetics(corpus):
    """
    Main analysis: compare line-final vs mid-line phonetic similarity profiles.
    """

    # Accumulators
    linefinal_tokens = []    # (s2, phon_sim, era, poem_title, has_rhyme)
    midline_tokens = []      # (s2, phon_sim, era, poem_title, has_rhyme)

    poems_analyzed = 0
    poems_rhymed = 0

    for poem in corpus:
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        era = poem.get("metadata", {}).get("era", "unknown")
        title = poem.get("metadata", {}).get("title", "")

        # Identify line-final positions:
        # A token is line-final if the NEXT token is a newline character
        # (token == '\n' or token starts with '\n')
        linefinal_positions = set()
        for i in range(len(tokens) - 1):
            next_tok = tokens[i+1]["token"]
            if next_tok.strip() == "" and "\n" in next_tok:
                linefinal_positions.add(i)
            elif next_tok == "\n":
                linefinal_positions.add(i)

        # Also collect line-final words (for rhyme detection)
        line_final_words = []
        for pos in sorted(linefinal_positions):
            tok = tokens[pos]["token"]
            if is_alphabetic_word(tok):
                line_final_words.append(tok)

        has_rhyme, rhyme_density = detect_rhyme_scheme(line_final_words)
        if has_rhyme:
            poems_rhymed += 1
        poems_analyzed += 1

        # Analyze each token
        for i, tok_data in enumerate(tokens):
            tok = tok_data["token"]
            s2 = tok_data["s2"]
            p_nl = tok_data.get("p_newline", 0.0)
            alts = tok_data.get("alternatives", [])

            # Skip stanza-break artifact positions
            if p_nl > 0.9:
                continue

            # Skip non-alphabetic tokens
            if not is_alphabetic_word(tok):
                continue

            # Skip if no alternatives
            if not alts:
                continue

            # Get top prediction
            top_pred = alts[0]["token"]
            phon_sim = phonetic_similarity(tok, top_pred)

            is_lf = (i in linefinal_positions)

            entry = {
                "s2": s2,
                "phon_sim": phon_sim,
                "era": era,
                "title": title,
                "has_rhyme": has_rhyme,
                "token": tok,
                "top_pred": top_pred,
            }

            if is_lf:
                linefinal_tokens.append(entry)
            else:
                midline_tokens.append(entry)

    return linefinal_tokens, midline_tokens, poems_analyzed, poems_rhymed

def bin_by_s2(tokens, bins):
    """Bin tokens by S2 and return mean phonetic similarity per bin."""
    result = {}
    for label, (lo, hi) in bins.items():
        subset = [t for t in tokens if lo <= t["s2"] < hi]
        if not subset:
            result[label] = {"n": 0, "mean_phon_sim": None, "pct_close": None}
            continue
        mean_ps = sum(t["phon_sim"] for t in subset) / len(subset)
        pct_close = sum(1 for t in subset if t["phon_sim"] > 0.5) / len(subset) * 100
        pct_fidelity = sum(1 for t in subset if t["phon_sim"] > 0.4) / len(subset) * 100
        result[label] = {
            "n": len(subset),
            "mean_phon_sim": round(mean_ps, 4),
            "pct_close": round(pct_close, 1),
            "pct_phon_fidelity": round(pct_fidelity, 1),
        }
    return result

def compute_phonetic_fidelity_surprise(tokens, s2_threshold=4.0, phon_threshold=0.4):
    """
    Compute rate of 'phonetic-fidelity surprise' tokens:
    high S2 (>= threshold) AND phonetically close (>= phon_threshold).
    """
    high_s2 = [t for t in tokens if t["s2"] >= s2_threshold]
    if not high_s2:
        return 0.0, 0, 0
    pfs = [t for t in high_s2 if t["phon_sim"] >= phon_threshold]
    return len(pfs) / len(high_s2) * 100, len(pfs), len(high_s2)

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)

def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"  {len(corpus)} poems loaded.")

    print("Analyzing line-final vs mid-line phonetics...")
    linefinal, midline, n_poems, n_rhymed = analyze_rhyme_slot_phonetics(corpus)

    print(f"  Poems analyzed: {n_poems}")
    print(f"  Poems with detected rhyme: {n_rhymed} ({100*n_rhymed/n_poems:.1f}%)")
    print(f"  Line-final tokens: {len(linefinal)}")
    print(f"  Mid-line tokens: {len(midline)}")

    S2_BINS = {
        "very_low (< −4)":   (-999, -4),
        "low (−4 to −1)":    (-4, -1),
        "neutral (−1 to 1)": (-1, 1),
        "moderate (1 to 4)": (1, 4),
        "high (4 to 8)":     (4, 8),
        "very_high (> 8)":   (8, 999),
    }

    lf_bins = bin_by_s2(linefinal, S2_BINS)
    ml_bins = bin_by_s2(midline, S2_BINS)

    print("\n=== Phonetic Similarity by S2 Class: LINE-FINAL vs MID-LINE ===")
    print(f"{'S2 Class':<25} {'LF N':>6} {'LF PhonSim':>10} {'LF %Close':>10} {'ML N':>6} {'ML PhonSim':>10} {'ML %Close':>10} {'Gap':>8}")
    print("-"*90)
    for label in S2_BINS:
        lf = lf_bins[label]
        ml = ml_bins[label]
        if lf["mean_phon_sim"] is not None and ml["mean_phon_sim"] is not None:
            gap = lf["mean_phon_sim"] - ml["mean_phon_sim"]
            print(f"{label:<25} {lf['n']:>6} {lf['mean_phon_sim']:>10.3f} {lf['pct_close']:>9.1f}% {ml['n']:>6} {ml['mean_phon_sim']:>10.3f} {ml['pct_close']:>9.1f}% {gap:>+8.3f}")
        else:
            print(f"{label:<25} {lf.get('n',0):>6}  {'N/A':>10} {'N/A':>10} {ml.get('n',0):>6}  {'N/A':>10} {'N/A':>10} {'N/A':>8}")

    # Phonetic-fidelity surprise rate
    lf_pfs_rate, lf_pfs_n, lf_high = compute_phonetic_fidelity_surprise(linefinal)
    ml_pfs_rate, ml_pfs_n, ml_high = compute_phonetic_fidelity_surprise(midline)

    print(f"\n=== Phonetic-Fidelity Surprise Rate (S2 ≥ 4 AND PhonSim ≥ 0.4) ===")
    print(f"  Line-final: {lf_pfs_rate:.2f}% ({lf_pfs_n}/{lf_high})")
    print(f"  Mid-line:   {ml_pfs_rate:.2f}% ({ml_pfs_n}/{ml_high})")
    print(f"  Ratio:      {lf_pfs_rate/ml_pfs_rate:.2f}x" if ml_pfs_rate > 0 else "  Ratio: N/A")

    # Rhymed vs free-verse comparison (line-final tokens only)
    rhymed_lf = [t for t in linefinal if t["has_rhyme"]]
    freev_lf = [t for t in linefinal if not t["has_rhyme"]]

    if rhymed_lf and freev_lf:
        r_bins = bin_by_s2(rhymed_lf, S2_BINS)
        f_bins = bin_by_s2(freev_lf, S2_BINS)

        print(f"\n=== LINE-FINAL: Rhymed vs Free-Verse Phonetics ===")
        print(f"  Rhymed line-final tokens: {len(rhymed_lf)}")
        print(f"  Free-verse line-final tokens: {len(freev_lf)}")
        print(f"\n{'S2 Class':<25} {'Rhymed N':>8} {'Rhymed Sim':>10} {'FreeV N':>8} {'FreeV Sim':>10} {'Gap':>8}")
        print("-"*75)
        for label in S2_BINS:
            r = r_bins[label]
            fv = f_bins[label]
            if r["mean_phon_sim"] is not None and fv["mean_phon_sim"] is not None:
                gap = r["mean_phon_sim"] - fv["mean_phon_sim"]
                print(f"{label:<25} {r['n']:>8} {r['mean_phon_sim']:>10.3f} {fv['n']:>8} {fv['mean_phon_sim']:>10.3f} {gap:>+8.3f}")

        # PFS rates
        r_pfs, r_pfs_n, r_h = compute_phonetic_fidelity_surprise(rhymed_lf)
        fv_pfs, fv_pfs_n, fv_h = compute_phonetic_fidelity_surprise(freev_lf)
        print(f"\n  Phonetic-Fidelity Surprise rate (S2≥4, PhonSim≥0.4):")
        print(f"    Rhymed line-final:     {r_pfs:.2f}% ({r_pfs_n}/{r_h})")
        print(f"    Free-verse line-final: {fv_pfs:.2f}% ({fv_pfs_n}/{fv_h})")

    # Top examples of phonetic-fidelity surprise at line endings
    pfs_tokens = [t for t in linefinal if t["s2"] >= 4.0 and t["phon_sim"] >= 0.4]
    pfs_tokens.sort(key=lambda t: -t["s2"])

    print(f"\n=== Top Phonetic-Fidelity Surprise Tokens at Line Endings ===")
    print(f"{'Poet word':<15} {'GPT-2 pred':<15} {'S2':>8} {'PhonSim':>8} {'Era':<20} {'Title'}")
    print("-"*90)
    seen = set()
    count = 0
    for t in pfs_tokens:
        key = (t["token"], t["top_pred"])
        if key not in seen:
            seen.add(key)
            title_short = t["title"][:30] if t["title"] else "?"
            print(f"{t['token']:<15} {t['top_pred']:<15} {t['s2']:>8.2f} {t['phon_sim']:>8.3f} {t['era']:<20} {title_short}")
            count += 1
            if count >= 20:
                break

    # Era breakdown: phonetic similarity at HIGH S2 line-final positions
    era_lf_high = defaultdict(list)
    for t in linefinal:
        if t["s2"] >= 4.0:
            era_lf_high[t["era"]].append(t["phon_sim"])

    era_stats = []
    for era, sims in era_lf_high.items():
        if len(sims) >= 5:
            era_stats.append((era, len(sims), sum(sims)/len(sims)))
    era_stats.sort(key=lambda x: -x[2])

    print(f"\n=== Era: Mean Phonetic Similarity at High-S2 LINE-FINAL Positions ===")
    print(f"{'Era':<25} {'N':>5} {'Mean PhonSim':>14}")
    print("-"*50)
    for era, n, ps in era_stats:
        print(f"{era:<25} {n:>5} {ps:>14.3f}")

    # Save results
    results = {
        "n_poems": n_poems,
        "n_rhymed": n_rhymed,
        "n_linefinal": len(linefinal),
        "n_midline": len(midline),
        "linefinal_phon_by_s2_bin": lf_bins,
        "midline_phon_by_s2_bin": ml_bins,
        "pfs_linefinal_rate": round(lf_pfs_rate, 3),
        "pfs_midline_rate": round(ml_pfs_rate, 3),
        "pfs_ratio": round(lf_pfs_rate / ml_pfs_rate, 3) if ml_pfs_rate > 0 else None,
        "rhymed_lf_pfs_rate": round(r_pfs, 3) if rhymed_lf and freev_lf else None,
        "freev_lf_pfs_rate": round(fv_pfs, 3) if rhymed_lf and freev_lf else None,
        "era_linefinal_highS2_phonetics": {e: {"n": n, "mean_phon_sim": round(ps, 4)}
                                            for e, n, ps in era_stats},
        "top_pfs_examples": [
            {"token": t["token"], "top_pred": t["top_pred"], "s2": t["s2"],
             "phon_sim": t["phon_sim"], "era": t["era"], "title": t["title"]}
            for t in pfs_tokens[:30]
        ],
    }

    out_path = "results/rhyme_slot_phonetics.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return results

if __name__ == "__main__":
    main()
