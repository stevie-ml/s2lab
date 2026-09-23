"""
Entropy Decomposition: The Two Strategies of Poetic Surprise

S2 = surprisal - entropy (per Simon DeDeo's framework)
This experiment decomposes high-S2 moments into two strategies:
  1. CERTAIN DEFIANCE: low entropy + high surprisal
     (model was confident, poet defied certainty)
  2. CHAOS NAVIGATION: high entropy + high surprisal
     (model was uncertain, poet still found the unexpected)

By examining WHERE in the (entropy, surprisal) plane poetry operates
relative to prose, we can characterize different poetic aesthetics.
"""

import json
import ast
from collections import defaultdict
import statistics

# Load corpus
with open("results/corpus_results.json") as f:
    data = json.load(f)

# Parse tokens
def parse_tokens(entry):
    t = entry.get("tokens", [])
    if isinstance(t, list):
        return t
    try:
        return ast.literal_eval(t)
    except Exception:
        return []

def parse_metadata(entry):
    m = entry.get("metadata", {})
    if isinstance(m, dict):
        return m
    try:
        return ast.literal_eval(m)
    except Exception:
        return {}

# Exclude stanza-break artifact positions (where top prediction is \n with prob > 0.9)
def is_artifact(token_data):
    alts = token_data.get("alternatives", [])
    if not alts:
        return False
    top_alt = alts[0]
    return top_alt.get("token", "") == "\n" and top_alt.get("prob", 0) > 0.9

# Classify each token into quadrants based on entropy and surprisal
# Using median entropy as the threshold for "low" vs "high" entropy
def classify_quadrant(entropy, surprisal, entropy_threshold, surprisal_threshold):
    """
    Q1 (CERTAIN DEFIANCE): low entropy, high surprisal -> S2 positive and strong
    Q2 (CHAOS NAVIGATION): high entropy, high surprisal -> S2 positive despite uncertainty
    Q3 (RIDING THE WAVE): high entropy, low surprisal -> model unsure, poet conforming
    Q4 (CONFORMITY): low entropy, low surprisal -> model sure, poet agrees
    """
    if entropy < entropy_threshold and surprisal > surprisal_threshold:
        return "CERTAIN_DEFIANCE"
    elif entropy >= entropy_threshold and surprisal > surprisal_threshold:
        return "CHAOS_NAVIGATION"
    elif entropy >= entropy_threshold and surprisal <= surprisal_threshold:
        return "RIDING_WAVE"
    else:
        return "CONFORMITY"

# Collect all non-artifact token data
all_tokens = []
poetry_tokens = []
prose_tokens = []
author_tokens = defaultdict(list)
era_tokens = defaultdict(list)

for entry in data:
    meta = parse_metadata(entry)
    tokens = parse_tokens(entry)
    if not tokens:
        continue

    era = meta.get("era", "unknown")
    author = meta.get("author", "unknown")
    is_control = era == "control"

    for t in tokens:
        if is_artifact(t):
            continue
        surprisal = t.get("surprisal", 0)
        entropy = t.get("entropy", 0)
        s2 = t.get("s2", 0)

        record = {
            "surprisal": surprisal,
            "entropy": entropy,
            "s2": s2,
            "token": t.get("token", ""),
            "author": author,
            "era": era,
            "is_control": is_control,
        }
        all_tokens.append(record)
        if is_control:
            prose_tokens.append(record)
        else:
            poetry_tokens.append(record)
        author_tokens[author].append(record)
        era_tokens[era].append(record)

# Compute thresholds from all tokens
all_entropy = [t["entropy"] for t in all_tokens]
all_surprisal = [t["surprisal"] for t in all_tokens]
entropy_threshold = statistics.median(all_entropy)
surprisal_threshold = statistics.median(all_surprisal)

print(f"Global entropy median: {entropy_threshold:.3f}")
print(f"Global surprisal median: {surprisal_threshold:.3f}")
print(f"Total non-artifact tokens: {len(all_tokens)}")
print(f"Poetry tokens: {len(poetry_tokens)}")
print(f"Prose tokens: {len(prose_tokens)}")

# Add quadrant classification
for t in all_tokens:
    t["quadrant"] = classify_quadrant(
        t["entropy"], t["surprisal"], entropy_threshold, surprisal_threshold
    )

# Global quadrant distribution: poetry vs prose
def quadrant_dist(tokens):
    counts = defaultdict(int)
    for t in tokens:
        counts[t["quadrant"]] += 1
    total = len(tokens)
    return {k: round(100 * v / total, 1) for k, v in counts.items()}

print("\n=== GLOBAL QUADRANT DISTRIBUTION ===")
print("\nPoetry:")
poetry_dist = quadrant_dist(poetry_tokens)
for q, pct in sorted(poetry_dist.items()):
    print(f"  {q}: {pct}%")

print("\nProse (control):")
prose_dist = quadrant_dist(prose_tokens)
for q, pct in sorted(prose_dist.items()):
    print(f"  {q}: {pct}%")

# The key metric: the ratio of CERTAIN_DEFIANCE to CONFORMITY
def defiance_ratio(tokens):
    counts = defaultdict(int)
    for t in tokens:
        counts[t["quadrant"]] += 1
    cd = counts.get("CERTAIN_DEFIANCE", 0)
    conf = counts.get("CONFORMITY", 0)
    if conf == 0:
        return float("inf")
    return round(cd / conf, 3)

print("\n=== CERTAIN DEFIANCE RATIO (CD/CONFORMITY) ===")
print(f"Poetry: {defiance_ratio(poetry_tokens)}")
print(f"Prose: {defiance_ratio(prose_tokens)}")

# Per-era analysis
print("\n=== ERA ANALYSIS: DEFIANCE STRATEGY ===")
era_stats = []
for era, tokens in era_tokens.items():
    if len(tokens) < 50:
        continue
    counts = defaultdict(int)
    for t in tokens:
        counts[t["quadrant"]] += 1
    total = len(tokens)
    cd_pct = round(100 * counts["CERTAIN_DEFIANCE"] / total, 1)
    cn_pct = round(100 * counts["CHAOS_NAVIGATION"] / total, 1)
    conf_pct = round(100 * counts["CONFORMITY"] / total, 1)
    rw_pct = round(100 * counts["RIDING_WAVE"] / total, 1)
    avg_entropy = round(statistics.mean([t["entropy"] for t in tokens]), 2)
    avg_surprisal = round(statistics.mean([t["surprisal"] for t in tokens]), 2)
    dr = defiance_ratio(tokens)

    # Dominant strategy
    strategy_pcts = {
        "CERTAIN_DEFIANCE": cd_pct,
        "CHAOS_NAVIGATION": cn_pct,
        "CONFORMITY": conf_pct,
        "RIDING_WAVE": rw_pct,
    }
    dominant = max(strategy_pcts, key=strategy_pcts.get)

    era_stats.append({
        "era": era,
        "n": total,
        "cd_pct": cd_pct,
        "cn_pct": cn_pct,
        "rw_pct": rw_pct,
        "conf_pct": conf_pct,
        "avg_entropy": avg_entropy,
        "avg_surprisal": avg_surprisal,
        "dr": dr,
        "dominant": dominant,
    })

# Sort by defiance ratio
era_stats.sort(key=lambda x: x["dr"], reverse=True)

print(f"\n{'Era':<22} {'n':>5} {'CD%':>6} {'CN%':>6} {'RW%':>6} {'Conf%':>6} {'H(avg)':>7} {'P(avg)':>7} {'DR':>6} | Dominant")
print("-" * 100)
for s in era_stats:
    print(
        f"{s['era']:<22} {s['n']:>5} {s['cd_pct']:>6} {s['cn_pct']:>6} "
        f"{s['rw_pct']:>6} {s['conf_pct']:>6} {s['avg_entropy']:>7} "
        f"{s['avg_surprisal']:>7} {s['dr']:>6} | {s['dominant']}"
    )

# Per-author analysis (top authors by token count)
print("\n=== AUTHOR ANALYSIS: DEFIANCE STRATEGY ===")
author_stats = []
for author, tokens in author_tokens.items():
    if len(tokens) < 100:
        continue
    counts = defaultdict(int)
    for t in tokens:
        counts[t["quadrant"]] += 1
    total = len(tokens)
    cd_pct = round(100 * counts["CERTAIN_DEFIANCE"] / total, 1)
    cn_pct = round(100 * counts["CHAOS_NAVIGATION"] / total, 1)
    conf_pct = round(100 * counts["CONFORMITY"] / total, 1)
    avg_entropy = round(statistics.mean([t["entropy"] for t in tokens]), 2)
    avg_surprisal = round(statistics.mean([t["surprisal"] for t in tokens]), 2)
    dr = defiance_ratio(tokens)

    author_stats.append({
        "author": author[:30],
        "n": total,
        "cd_pct": cd_pct,
        "cn_pct": cn_pct,
        "conf_pct": conf_pct,
        "avg_entropy": avg_entropy,
        "avg_surprisal": avg_surprisal,
        "dr": dr,
    })

author_stats.sort(key=lambda x: x["dr"], reverse=True)
print(f"\n{'Author':<32} {'n':>5} {'CD%':>6} {'CN%':>6} {'Conf%':>6} {'H(avg)':>7} {'P(avg)':>7} {'DR':>6}")
print("-" * 85)
for s in author_stats:
    print(
        f"{s['author']:<32} {s['n']:>5} {s['cd_pct']:>6} {s['cn_pct']:>6} "
        f"{s['conf_pct']:>6} {s['avg_entropy']:>7} {s['avg_surprisal']:>7} {s['dr']:>6}"
    )

# Examples of CERTAIN_DEFIANCE: model was certain, poet defied it
print("\n=== TOP CERTAIN-DEFIANCE MOMENTS (low entropy, high surprisal) ===")
# Find tokens where entropy < 25th percentile AND surprisal > 75th percentile
import statistics as st
all_entropy_sorted = sorted(all_entropy)
all_surprisal_sorted = sorted(all_surprisal)
e_25 = all_entropy_sorted[len(all_entropy_sorted) // 4]
s_75 = all_surprisal_sorted[3 * len(all_surprisal_sorted) // 4]

cd_examples = [
    t for t in poetry_tokens
    if t["entropy"] < e_25 and t["surprisal"] > s_75 and not t.get("is_control")
]
cd_examples.sort(key=lambda x: x["s2"], reverse=True)
print(f"(entropy < {e_25:.2f} AND surprisal > {s_75:.2f})")
for ex in cd_examples[:20]:
    print(
        f"  [{ex['author'][:25]}] token={repr(ex['token']):<15} "
        f"H={ex['entropy']:.2f} P={ex['surprisal']:.2f} S2={ex['s2']:.2f}"
    )

# Examples of CHAOS_NAVIGATION: both entropy AND surprisal high
print("\n=== TOP CHAOS-NAVIGATION MOMENTS (high entropy, high surprisal) ===")
e_75 = all_entropy_sorted[3 * len(all_entropy_sorted) // 4]
cn_examples = [
    t for t in poetry_tokens
    if t["entropy"] >= e_75 and t["surprisal"] > s_75 and not t.get("is_control")
]
cn_examples.sort(key=lambda x: x["s2"], reverse=True)
print(f"(entropy > {e_75:.2f} AND surprisal > {s_75:.2f})")
for ex in cn_examples[:20]:
    print(
        f"  [{ex['author'][:25]}] token={repr(ex['token']):<15} "
        f"H={ex['entropy']:.2f} P={ex['surprisal']:.2f} S2={ex['s2']:.2f}"
    )

# Summarize: which quadrant has the highest mean S2?
print("\n=== MEAN S2 BY QUADRANT ===")
for q in ["CERTAIN_DEFIANCE", "CHAOS_NAVIGATION", "RIDING_WAVE", "CONFORMITY"]:
    q_tokens = [t for t in poetry_tokens if t["quadrant"] == q]
    if q_tokens:
        mean_s2 = statistics.mean([t["s2"] for t in q_tokens])
        mean_h = statistics.mean([t["entropy"] for t in q_tokens])
        mean_p = statistics.mean([t["surprisal"] for t in q_tokens])
        print(f"  {q}: mean_S2={mean_s2:.3f}, mean_H={mean_h:.3f}, mean_surprisal={mean_p:.3f}, n={len(q_tokens)}")

# What fraction of each author's high-S2 moments (S2 > 3) are CERTAIN vs CHAOS?
print("\n=== HIGH-S2 MOMENT ORIGIN: CERTAIN DEFIANCE vs CHAOS NAVIGATION ===")
high_s2_author = defaultdict(lambda: defaultdict(int))
for t in poetry_tokens:
    if t["s2"] >= 3.0 and not t.get("is_control"):
        high_s2_author[t["author"]][t["quadrant"]] += 1

author_hs2_stats = []
for author, counts in high_s2_author.items():
    total = sum(counts.values())
    if total < 5:
        continue
    cd = counts.get("CERTAIN_DEFIANCE", 0)
    cn = counts.get("CHAOS_NAVIGATION", 0)
    author_hs2_stats.append({
        "author": author[:30],
        "total_hs2": total,
        "cd": cd,
        "cn": cn,
        "cd_pct": round(100 * cd / total, 1),
        "cn_pct": round(100 * cn / total, 1),
    })

author_hs2_stats.sort(key=lambda x: x["cd_pct"], reverse=True)
print(f"\n{'Author':<32} {'High-S2':>8} {'CD%':>6} {'CN%':>6} | Strategy")
print("-" * 70)
for s in author_hs2_stats:
    dominant = "CERTAIN" if s["cd_pct"] > s["cn_pct"] else "CHAOS"
    print(f"{s['author']:<32} {s['total_hs2']:>8} {s['cd_pct']:>6} {s['cn_pct']:>6} | {dominant}")

print("\n=== DONE ===")
