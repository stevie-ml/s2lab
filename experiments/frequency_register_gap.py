"""
Frequency vs Context: What Kind of Surprise Creates the Straussian Gap?

Research question: At high-S2 moments, are poets choosing:
  a) RARE words (long/unusual tokens that are intrinsically infrequent)
  b) COMMON words in UNUSUAL positions (short/common tokens where model was confident)

Method:
  - Use token length as a proxy for word frequency (Zipf's law: shorter = more common)
  - Compare actual token length vs. top-alternative token length at each position
  - Classify high-S2 events by which strategy dominates

Hypothesis: The Straussian gap is primarily created through strategy (b) —
common words in unexpected positions — because this is the most "poetic" form
of surprise: choosing something simple and concrete when the model expected
something elaborated.
"""

import json
import numpy as np
from collections import Counter, defaultdict

with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# Collect all clean tokens (removing stanza-break artifacts)
all_tokens = []
for poem in corpus:
    meta = poem["metadata"]
    for tok in poem["tokens"]:
        p_newline = tok.get("p_newline", 0)
        if p_newline > 0.9:
            continue  # skip stanza-break artifacts

        token_str = tok["token"]
        s2 = tok["s2"]
        rank = tok["rank"]  # rank in conditional distribution
        entropy = tok.get("entropy", 0) or 0
        surprisal = tok.get("surprisal", 0) or 0

        # Top expected alternative
        alts = tok.get("alternatives", [])
        top_alt = alts[0]["token"] if alts else None
        top_alt_prob = alts[0]["prob"] if alts else 0

        # Token length (proxy for word frequency)
        # Strip leading space (GPT-2 tokenization artifact)
        clean_tok = token_str.strip()
        clean_alt = top_alt.strip() if top_alt else ""

        tok_len = len(clean_tok)
        alt_len = len(clean_alt) if clean_alt else 0

        # Classify the "register gap"
        # positive = poet chose longer (rarer) word than expected
        # negative = poet chose shorter (commoner) word than expected
        length_diff = tok_len - alt_len

        all_tokens.append({
            "s2": s2,
            "rank": rank,
            "entropy": entropy,
            "surprisal": surprisal,
            "token": token_str,
            "clean_tok": clean_tok,
            "tok_len": tok_len,
            "alt_len": alt_len,
            "length_diff": length_diff,
            "top_alt": top_alt,
            "era": meta["era"],
            "author": meta["author"],
            "is_function_word": clean_tok.lower() in {
                "the", "a", "an", "of", "in", "on", "at", "to", "for",
                "and", "or", "but", "is", "are", "was", "were", "be",
                "it", "its", "this", "that", "with", "from", "by",
                "as", "i", "he", "she", "we", "they", "his", "her",
                "our", "their", "my", "your", "me", "him", "us", "them",
                "not", "no", "so", "if", "then", "when", "which", "who",
                "what", "how", "do", "did", "has", "have", "had",
            },
        })

print(f"Total clean tokens: {len(all_tokens)}")
print(f"Overall mean S2: {np.mean([t['s2'] for t in all_tokens]):.3f}")

# ─── SECTION 1: Token Length by S2 bin ────────────────────────────────────────
print("\n" + "="*60)
print("TOKEN LENGTH BY S2 BIN (proxy for word rarity)")
print("="*60)

bins = [
    ("Very Low S2 (< -2)", [t for t in all_tokens if t["s2"] < -2]),
    ("Low S2 (-2 to 0)", [t for t in all_tokens if -2 <= t["s2"] < 0]),
    ("Near-zero S2 (0 to 1)", [t for t in all_tokens if 0 <= t["s2"] < 1]),
    ("High S2 (1 to 3)", [t for t in all_tokens if 1 <= t["s2"] < 3]),
    ("Very High S2 (> 3)", [t for t in all_tokens if t["s2"] >= 3]),
]

print(f"\n{'Bin':<28} {'n':>6} {'mean_len':>10} {'%short':>8} {'%long':>8} {'mean_rank':>10}")
print("-"*70)
for label, group in bins:
    if not group:
        continue
    lens = [t["tok_len"] for t in group]
    ranks = [t["rank"] for t in group]
    n = len(group)
    pct_short = sum(1 for l in lens if l <= 2) / n * 100  # ≤2 chars: very common
    pct_long = sum(1 for l in lens if l >= 7) / n * 100   # ≥7 chars: unusual
    print(f"{label:<28} {n:>6} {np.mean(lens):>10.2f} {pct_short:>7.1f}% {pct_long:>7.1f}% {np.mean(ranks):>10.1f}")

# ─── SECTION 2: The Register Gap ──────────────────────────────────────────────
print("\n" + "="*60)
print("REGISTER GAP: actual token length vs. expected token length")
print("='rare word' if actual longer than expected; 'common word surprise' if shorter")
print("="*60)

high_s2_tokens = [t for t in all_tokens if t["s2"] > 1.5]
n_high = len(high_s2_tokens)

longer = [t for t in high_s2_tokens if t["length_diff"] > 1]   # chose rarer word
same = [t for t in high_s2_tokens if abs(t["length_diff"]) <= 1]  # same length class
shorter = [t for t in high_s2_tokens if t["length_diff"] < -1]  # chose commoner word

print(f"\nHigh-S2 tokens (S2 > 1.5): n={n_high}")
print(f"  Chose LONGER (rarer) word than expected: {len(longer)} ({len(longer)/n_high*100:.1f}%)")
print(f"  Same length class as expected:           {len(same)} ({len(same)/n_high*100:.1f}%)")
print(f"  Chose SHORTER (commoner) word:           {len(shorter)} ({len(shorter)/n_high*100:.1f}%)")

print(f"\nMean length difference at high-S2 events: {np.mean([t['length_diff'] for t in high_s2_tokens]):.2f} chars")
all_diff = np.mean([t['length_diff'] for t in all_tokens])
high_diff = np.mean([t['length_diff'] for t in high_s2_tokens])
print(f"Overall mean length difference: {all_diff:.2f} chars")
print(f"High-S2 mean length difference: {high_diff:.2f} chars (higher = rarer word chosen)")

# ─── SECTION 3: Function Words at High-S2 ─────────────────────────────────────
print("\n" + "="*60)
print("FUNCTION WORDS AT HIGH-S2 MOMENTS")
print("(common grammar words appearing in unexpected positions)")
print("="*60)

all_fw_rate = sum(1 for t in all_tokens if t["is_function_word"]) / len(all_tokens)
high_fw_rate = sum(1 for t in high_s2_tokens if t["is_function_word"]) / n_high

print(f"\nFunction word rate overall:    {all_fw_rate*100:.1f}%")
print(f"Function word rate at high-S2: {high_fw_rate*100:.1f}%")
print(f"Enrichment: {high_fw_rate/all_fw_rate:.2f}x")

# ─── SECTION 4: Top 20 Most Common High-S2 Tokens ────────────────────────────
print("\n" + "="*60)
print("TOP 20 TOKENS AT HIGH-S2 POSITIONS (S2 > 1.5, artifact-free)")
print("="*60)

token_counts = Counter(t["clean_tok"].lower() for t in high_s2_tokens if len(t["clean_tok"]) > 0)
print("\nRank | Token | Count | Length | Note")
print("-"*50)
for rank_i, (tok, cnt) in enumerate(token_counts.most_common(20), 1):
    note = "FUNCTION" if tok in {"the","a","an","of","in","on","at","to","and","or","but","i","he","she","we","is","was","it"} else ""
    print(f"{rank_i:>4} | {tok:<12} | {cnt:>5} | {len(tok):>6} | {note}")

# ─── SECTION 5: Top 20 Most Common EXPECTED tokens at high-S2 positions ───────
print("\n" + "="*60)
print("WHAT GPT-2 EXPECTED AT HIGH-S2 POSITIONS")
print("(the 'unsaid' — the choice the model favored)")
print("="*60)

alt_counts = Counter(t["top_alt"].strip().lower() for t in high_s2_tokens if t["top_alt"])
print("\nRank | Expected Token | Count | Length")
print("-"*45)
for rank_i, (tok, cnt) in enumerate(alt_counts.most_common(20), 1):
    print(f"{rank_i:>4} | {tok:<18} | {cnt:>5} | {len(tok):>6}")

# ─── SECTION 6: The "Short-Word Poets" - who uses common words at high-S2? ───
print("\n" + "="*60)
print("POET PROFILES: Common-word vs Rare-word strategists")
print("(at high-S2 moments, how long are their chosen tokens?)")
print("="*60)

poet_data = defaultdict(list)
for t in high_s2_tokens:
    poet_data[t["author"]].append(t["tok_len"])

poet_stats = {
    author: {
        "n": len(lens),
        "mean_len": np.mean(lens),
        "pct_short": sum(1 for l in lens if l <= 3) / len(lens) * 100,
    }
    for author, lens in poet_data.items()
    if len(lens) >= 10  # minimum sample
}

# Sort by mean token length at high-S2 moments
sorted_poets = sorted(poet_stats.items(), key=lambda x: x[1]["mean_len"])

print("\nPoets who use SHORTEST words at surprise moments (common-word strategists):")
print(f"{'Author':<30} {'n':>5} {'mean_len':>10} {'%≤3 chars':>10}")
print("-"*57)
for author, stats in sorted_poets[:10]:
    print(f"{author:<30} {stats['n']:>5} {stats['mean_len']:>10.2f} {stats['pct_short']:>9.1f}%")

print("\nPoets who use LONGEST words at surprise moments (rare-word strategists):")
print(f"{'Author':<30} {'n':>5} {'mean_len':>10} {'%≤3 chars':>10}")
print("-"*57)
for author, stats in sorted_poets[-10:]:
    print(f"{author:<30} {stats['n']:>5} {stats['mean_len']:>10.2f} {stats['pct_short']:>9.1f}%")

# ─── SECTION 7: Era-level analysis ───────────────────────────────────────────
print("\n" + "="*60)
print("ERA ANALYSIS: Common-word vs Rare-word surprise by era")
print("="*60)

era_data = defaultdict(list)
for t in high_s2_tokens:
    era_data[t["era"]].append(t["tok_len"])

era_stats = {
    era: {
        "n": len(lens),
        "mean_len": np.mean(lens),
        "pct_short": sum(1 for l in lens if l <= 3) / len(lens) * 100,
    }
    for era, lens in era_data.items()
    if len(lens) >= 20
}

sorted_eras = sorted(era_stats.items(), key=lambda x: x[1]["mean_len"])

print(f"\n{'Era':<25} {'n':>5} {'mean_len':>10} {'%≤3 chars':>10}")
print("-"*52)
for era, stats in sorted_eras:
    print(f"{era:<25} {stats['n']:>5} {stats['mean_len']:>10.2f} {stats['pct_short']:>9.1f}%")

# Save results
results = {
    "total_clean_tokens": len(all_tokens),
    "high_s2_tokens": n_high,
    "high_s2_strategy": {
        "longer_rarer": len(longer),
        "same_length": len(same),
        "shorter_commoner": len(shorter),
        "pct_longer": len(longer)/n_high*100,
        "pct_shorter": len(shorter)/n_high*100,
    },
    "function_word_rates": {
        "overall": all_fw_rate,
        "high_s2": high_fw_rate,
        "enrichment": high_fw_rate / all_fw_rate,
    },
    "mean_length_at_high_s2": float(np.mean([t["tok_len"] for t in high_s2_tokens])),
    "mean_length_overall": float(np.mean([t["tok_len"] for t in all_tokens])),
    "top_high_s2_tokens": dict(token_counts.most_common(30)),
    "top_expected_at_high_s2": dict(alt_counts.most_common(30)),
    "poet_profiles": {
        author: stats for author, stats in sorted_poets
    },
    "era_profiles": {
        era: stats for era, stats in sorted_eras
    },
}

import os
os.makedirs("results", exist_ok=True)
with open("results/frequency_register_gap.json", "w") as f:
    json.dump(results, f, indent=2)

print("\n\nSaved to results/frequency_register_gap.json")
