"""
Surprise Lexicon Map: Corpus Frequency vs. Mean S2

For every word type in the corpus, computes:
  - How often it appears (corpus frequency)
  - Its mean S2 across all occurrences
  - Its S2 consistency (std)

This creates a 2D "lexicon map" that identifies:
  - STANDARD words: common, low S2 — the expected vocabulary of poetry
  - TRADEMARK words: common, high S2 — words that always surprise GPT-2
  - RARE CONFORMISTS: rare, low S2 — unusual words used in expected ways
  - RARE FIRECRACKERS: rare, high S2 — rare words that always detonate

The key question: is there intrinsic "surprise value" baked into specific words
independent of context? Or is all surprise contextual?
"""

import json
import math
import re
from collections import defaultdict

# Load corpus
with open("results/corpus_results.json") as f:
    data = json.load(f)

# --- collect per-word S2 stats ---
word_s2 = defaultdict(list)
word_era = defaultdict(set)
word_meta = defaultdict(list)  # (s2, era, title, poet) per occurrence

ARTIFACT_THRESH = 0.60  # p_newline threshold for stanza-break filtering

total_tokens = 0
skipped_artifact = 0
skipped_punct = 0

for poem in data:
    meta = poem.get("metadata", {})
    era = meta.get("era", "unknown")
    title = meta.get("title", "")
    author = meta.get("author", "")

    for tok in poem.get("tokens", []):
        # Skip stanza-break artifacts
        p_nl = tok.get("p_newline", 0.0)
        if p_nl >= ARTIFACT_THRESH:
            skipped_artifact += 1
            continue

        token_str = tok.get("token", "")
        s2 = tok.get("s2", 0.0)

        # Normalise: strip leading space (GPT-2 BPE), lowercase
        word = token_str.strip().lower()

        # Skip pure punctuation, numbers, very short tokens, newlines
        if not word:
            skipped_punct += 1
            continue
        if word == "\n" or word == "\r":
            skipped_artifact += 1
            continue
        if re.fullmatch(r"[\W\d]+", word):
            skipped_punct += 1
            continue
        if len(word) < 3:
            skipped_punct += 1
            continue

        total_tokens += 1
        word_s2[word].append(s2)
        word_era[word].add(era)
        word_meta[word].append((s2, era, title, author))

print(f"Total qualifying tokens: {total_tokens:,}")
print(f"Skipped (artifact): {skipped_artifact:,}")
print(f"Skipped (punct/short): {skipped_punct:,}")
print(f"Unique word types: {len(word_s2):,}")

# --- compute per-word statistics ---
MIN_N = 8  # minimum occurrences for reliable mean

word_stats = {}
for word, s2_list in word_s2.items():
    n = len(s2_list)
    if n < MIN_N:
        continue
    mean_s2 = sum(s2_list) / n
    variance = sum((x - mean_s2) ** 2 for x in s2_list) / n
    std_s2 = math.sqrt(variance)
    # 95% CI half-width
    ci = 1.96 * std_s2 / math.sqrt(n)
    word_stats[word] = {
        "word": word,
        "n": n,
        "mean_s2": round(mean_s2, 3),
        "std_s2": round(std_s2, 3),
        "ci95": round(ci, 3),
        "min_s2": round(min(s2_list), 3),
        "max_s2": round(max(s2_list), 3),
        "pct_positive": round(sum(1 for x in s2_list if x > 0) / n, 3),
        "n_eras": len(word_era[word]),
    }

print(f"\nWords with N≥{MIN_N}: {len(word_stats):,}")

# Sort by mean S2
by_s2 = sorted(word_stats.values(), key=lambda x: x["mean_s2"], reverse=True)
by_freq = sorted(word_stats.values(), key=lambda x: x["n"], reverse=True)
by_consistency = sorted(word_stats.values(), key=lambda x: x["std_s2"])  # low std = consistent

# --- Top/bottom S2 words ---
print("\n=== TOP 30 HIGHEST MEAN-S2 WORDS (intrinsically surprising) ===")
print(f"{'Word':20s} {'N':>5} {'Mean S2':>8} {'Std':>6} {'%Pos':>6} {'Eras':>5}")
print("-" * 60)
for w in by_s2[:30]:
    print(f"{w['word']:20s} {w['n']:>5} {w['mean_s2']:>8.3f} {w['std_s2']:>6.3f} "
          f"{w['pct_positive']:>5.0%} {w['n_eras']:>5}")

print("\n=== TOP 30 LOWEST MEAN-S2 WORDS (intrinsically conformist) ===")
print(f"{'Word':20s} {'N':>5} {'Mean S2':>8} {'Std':>6} {'%Pos':>6} {'Eras':>5}")
print("-" * 60)
for w in reversed(by_s2[-30:]):
    print(f"{w['word']:20s} {w['n']:>5} {w['mean_s2']:>8.3f} {w['std_s2']:>6.3f} "
          f"{w['pct_positive']:>5.0%} {w['n_eras']:>5}")

print("\n=== TOP 30 MOST FREQUENT WORDS (most common in corpus) ===")
print(f"{'Word':20s} {'N':>5} {'Mean S2':>8} {'Std':>6} {'%Pos':>6}")
print("-" * 55)
for w in by_freq[:30]:
    print(f"{w['word']:20s} {w['n']:>5} {w['mean_s2']:>8.3f} {w['std_s2']:>6.3f} "
          f"{w['pct_positive']:>5.0%}")

# --- Quadrant analysis ---
# Threshold: high freq = top 25% by n; high S2 = mean_s2 > 0
freq_vals = sorted(w["n"] for w in word_stats.values())
freq_thresh = freq_vals[int(len(freq_vals) * 0.75)]  # top 25% = "common"

quadrants = {"TRADEMARK": [], "STANDARD": [], "FIRECRACKER": [], "RARE_CONFORMIST": []}
for w in word_stats.values():
    high_freq = w["n"] >= freq_thresh
    high_s2 = w["mean_s2"] > 0
    if high_freq and high_s2:
        quadrants["TRADEMARK"].append(w)
    elif high_freq and not high_s2:
        quadrants["STANDARD"].append(w)
    elif not high_freq and high_s2:
        quadrants["FIRECRACKER"].append(w)
    else:
        quadrants["RARE_CONFORMIST"].append(w)

print(f"\n=== QUADRANT ANALYSIS (freq threshold: N≥{freq_thresh}) ===")
for qname, words in quadrants.items():
    label = {
        "TRADEMARK": "Common + High S2 (always surprise)",
        "STANDARD": "Common + Low S2 (expected vocabulary)",
        "FIRECRACKER": "Rare + High S2 (rare detonators)",
        "RARE_CONFORMIST": "Rare + Low S2 (rare but expected)",
    }[qname]
    print(f"\n{qname} ({label}): {len(words)} words")
    top = sorted(words, key=lambda x: abs(x["mean_s2"]), reverse=True)[:15]
    for w in top:
        print(f"  {w['word']:18s} N={w['n']:>4}  S2={w['mean_s2']:>+7.3f}  std={w['std_s2']:.3f}")

# --- Most CONSISTENT words (low std = same surprise level every time) ---
print("\n=== MOST S2-CONSISTENT WORDS (low std = reliable surprise level) ===")
# Among words with N >= 15 for reliability
consistent = sorted(
    [w for w in word_stats.values() if w["n"] >= 15],
    key=lambda x: x["std_s2"]
)
print(f"\nAlways LOW S2 (consistently conformist, std < 2.5):")
print(f"{'Word':20s} {'N':>5} {'Mean S2':>8} {'Std':>6}")
low_s2_consistent = [w for w in consistent if w["mean_s2"] < 0][:20]
for w in low_s2_consistent:
    print(f"{w['word']:20s} {w['n']:>5} {w['mean_s2']:>8.3f} {w['std_s2']:>6.3f}")

print(f"\nAlways HIGH S2 (consistently surprising, std < 3.0):")
high_s2_consistent = sorted(
    [w for w in consistent if w["mean_s2"] > 0],
    key=lambda x: x["std_s2"]
)[:20]
for w in high_s2_consistent:
    print(f"{w['word']:20s} {w['n']:>5} {w['mean_s2']:>8.3f} {w['std_s2']:>6.3f}")

# --- Save results ---
output = {
    "method": "Surprise Lexicon Map",
    "date": "2026-11-03",
    "total_tokens": total_tokens,
    "unique_word_types": len(word_s2),
    "words_above_threshold": len(word_stats),
    "min_occurrences": MIN_N,
    "freq_threshold_for_common": freq_thresh,
    "top_30_high_s2": [w for w in by_s2[:30]],
    "top_30_low_s2": [w for w in reversed(by_s2[-30:])],
    "top_30_most_frequent": [w for w in by_freq[:30]],
    "quadrant_counts": {k: len(v) for k, v in quadrants.items()},
    "quadrant_top15": {k: sorted(v, key=lambda x: abs(x["mean_s2"]), reverse=True)[:15]
                       for k, v in quadrants.items()},
    "full_lexicon": sorted(word_stats.values(), key=lambda x: x["mean_s2"], reverse=True),
}

with open("results/surprise_lexicon_map.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nResults saved to results/surprise_lexicon_map.json")
