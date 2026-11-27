"""
Counter-Trend Escalation Analysis

Extends findings/mode_trajectory_within_poem.md which established that ~63-73%
of poems show falling entropy and S2 toward the end ("settlement").

This experiment focuses on the exceptional poems that ESCALATE — where BOTH
entropy AND S2 rise from first to second half. What characterizes them?

Research questions:
1. What fraction of poems truly escalate on BOTH dimensions?
2. Which eras produce the most counter-trend escalation?
3. What is happening at the token level in the escalating second halves?
4. Is escalation correlated with poem length, form, or theme?
5. Can we build an "escalation index" that predicts the trajectory?
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
import statistics

results_path = Path("results/corpus_results.json")
with open(results_path) as f:
    corpus = json.load(f)

NEWLINE_THRESHOLD = 0.9

def get_clean_tokens(tokens):
    """Filter to artifact-free tokens (non-newline-dominant positions)."""
    return [t for t in tokens if t.get("p_newline", 0) < NEWLINE_THRESHOLD
            and t.get("token", "") not in ["<|endoftext|>"]]

def compute_half_stats(tokens, half="first"):
    """Compute mean H and mean S2 for a half of the token list."""
    if not tokens:
        return None, None
    n = len(tokens)
    mid = n // 2
    if half == "first":
        subset = tokens[:mid]
    else:
        subset = tokens[mid:]
    if not subset:
        return None, None
    H_vals = [t["entropy"] for t in subset if "entropy" in t]
    s2_vals = [t["s2"] for t in subset if "s2" in t]
    if not H_vals or not s2_vals:
        return None, None
    return statistics.mean(H_vals), statistics.mean(s2_vals)

# --- First pass: classify all poems ---
poems = []
for item in corpus:
    meta = item.get("metadata", {})
    if meta.get("era") == "control":
        continue
    tokens = get_clean_tokens(item.get("tokens", []))
    if len(tokens) < 30:  # skip very short poems
        continue

    H_first, s2_first = compute_half_stats(tokens, "first")
    H_second, s2_second = compute_half_stats(tokens, "second")

    if any(v is None for v in [H_first, s2_first, H_second, s2_second]):
        continue

    delta_H = H_second - H_first
    delta_s2 = s2_second - s2_first

    poems.append({
        "title": meta.get("title", "?"),
        "author": meta.get("author", "?"),
        "era": meta.get("era", "?"),
        "n_tokens": len(tokens),
        "H_first": H_first,
        "H_second": H_second,
        "s2_first": s2_first,
        "s2_second": s2_second,
        "delta_H": delta_H,
        "delta_s2": delta_s2,
        "mean_s2": statistics.mean(t["s2"] for t in tokens if "s2" in t),
        "mean_H": statistics.mean(t["entropy"] for t in tokens if "entropy" in t),
        "tokens": tokens,
    })

print(f"Total poems analyzed: {len(poems)}")

# --- Classify poems ---
n_H_rise = sum(1 for p in poems if p["delta_H"] > 0)
n_s2_rise = sum(1 for p in poems if p["delta_s2"] > 0)
counter_trend = [p for p in poems if p["delta_H"] > 0 and p["delta_s2"] > 0]
settlement = [p for p in poems if p["delta_H"] < 0 and p["delta_s2"] < 0]

print(f"\n--- Overall Trajectory Classification ---")
print(f"H rises in second half:  {n_H_rise}/{len(poems)} ({100*n_H_rise/len(poems):.1f}%)")
print(f"S2 rises in second half: {n_s2_rise}/{len(poems)} ({100*n_s2_rise/len(poems):.1f}%)")
print(f"Counter-trend (BOTH rise): {len(counter_trend)} ({100*len(counter_trend)/len(poems):.1f}%)")
print(f"Settlement (BOTH fall):    {len(settlement)} ({100*len(settlement)/len(poems):.1f}%)")

# --- Era breakdown ---
print(f"\n--- Counter-Trend Fraction by Era (min 4 poems) ---")
era_data = defaultdict(list)
for p in poems:
    era_data[p["era"]].append(p)

era_counter = {}
for era, ps in era_data.items():
    if len(ps) < 4 or era == "?":
        continue
    ct = sum(1 for p in ps if p["delta_H"] > 0 and p["delta_s2"] > 0)
    era_counter[era] = {
        "n": len(ps),
        "counter_trend": ct,
        "pct": 100 * ct / len(ps),
        "mean_delta_s2": statistics.mean(p["delta_s2"] for p in ps),
        "mean_delta_H": statistics.mean(p["delta_H"] for p in ps),
    }

sorted_eras = sorted(era_counter.items(), key=lambda x: x[1]["pct"], reverse=True)
print(f"{'Era':<25} {'n':>4} {'CounterTrend%':>14} {'mean ΔH':>9} {'mean ΔS₂':>9}")
print("-" * 65)
for era, d in sorted_eras:
    print(f"{era:<25} {d['n']:>4} {d['pct']:>13.1f}% {d['mean_delta_H']:>9.3f} {d['mean_delta_s2']:>9.3f}")

# --- Top escalating poems ---
print(f"\n--- Top 20 Most Escalating Poems (by combined delta H + delta S2) ---")
counter_trend_sorted = sorted(counter_trend, key=lambda p: p["delta_H"] + p["delta_s2"], reverse=True)
print(f"{'ΔH':>7} {'ΔS₂':>7} {'Author':<22} {'Title':<35} {'Era':<20}")
print("-" * 95)
for p in counter_trend_sorted[:20]:
    title_short = p["title"][:33] if len(p["title"]) > 33 else p["title"]
    author_short = p["author"][:20] if len(p["author"]) > 20 else p["author"]
    print(f"{p['delta_H']:>7.3f} {p['delta_s2']:>7.3f} {author_short:<22} {title_short:<35} {p['era']:<20}")

# --- Token-level analysis of escalating second halves ---
print(f"\n--- What Drives Escalation? Top High-S2 Tokens in Escalating Second Halves ---")
escalation_tokens = []
for p in counter_trend:
    tokens = p["tokens"]
    n = len(tokens)
    mid = n // 2
    second_half = tokens[mid:]
    for t in second_half:
        if t.get("s2", 0) > 2.0 and t.get("token", "").strip() not in ["", "\n"]:
            escalation_tokens.append({
                "token": t.get("token", ""),
                "s2": t["s2"],
                "entropy": t.get("entropy", 0),
                "author": p["author"],
                "title": p["title"],
            })

# Count most common tokens causing escalation
token_freq = defaultdict(list)
for t in escalation_tokens:
    tok = t["token"].strip().lower()
    if tok:
        token_freq[tok].append(t["s2"])

# Sort by frequency
print(f"{'Token':<20} {'Count':>6} {'Avg S₂':>8} {'Max S₂':>8}")
print("-" * 46)
top_tokens = sorted(token_freq.items(), key=lambda x: len(x[1]), reverse=True)[:25]
for tok, s2_list in top_tokens:
    print(f"{tok:<20} {len(s2_list):>6} {statistics.mean(s2_list):>8.2f} {max(s2_list):>8.2f}")

# --- Length relationship ---
print(f"\n--- Poem Length and Counter-Trend Tendency ---")
lengths = [p["n_tokens"] for p in poems]
median_len = statistics.median(lengths)
short = [p for p in poems if p["n_tokens"] <= median_len]
long_p = [p for p in poems if p["n_tokens"] > median_len]
ct_short = sum(1 for p in short if p["delta_H"] > 0 and p["delta_s2"] > 0) / len(short)
ct_long = sum(1 for p in long_p if p["delta_H"] > 0 and p["delta_s2"] > 0) / len(long_p)
print(f"Median poem length: {median_len:.0f} tokens")
print(f"Short poems counter-trend rate: {ct_short*100:.1f}% (n={len(short)})")
print(f"Long poems counter-trend rate:  {ct_long*100:.1f}% (n={len(long_p)})")

# --- Settlement (most conformist) poems ---
print(f"\n--- Top 10 Most 'Settlement' Poems (sharpest fall in both H and S2) ---")
settlement_sorted = sorted(settlement, key=lambda p: p["delta_H"] + p["delta_s2"])
print(f"{'ΔH':>7} {'ΔS₂':>7} {'Author':<22} {'Title':<35} {'Era':<20}")
print("-" * 95)
for p in settlement_sorted[:10]:
    title_short = p["title"][:33] if len(p["title"]) > 33 else p["title"]
    author_short = p["author"][:20] if len(p["author"]) > 20 else p["author"]
    print(f"{p['delta_H']:>7.3f} {p['delta_s2']:>7.3f} {author_short:<22} {title_short:<35} {p['era']:<20}")

# --- Escalation index ---
print(f"\n--- Escalation Index: Combined ΔH + ΔS₂ Distribution ---")
indices = [p["delta_H"] + p["delta_s2"] for p in poems]
print(f"Mean escalation index: {statistics.mean(indices):.3f}")
print(f"Std: {statistics.stdev(indices):.3f}")
print(f"Q25: {sorted(indices)[len(indices)//4]:.3f}")
print(f"Median: {statistics.median(indices):.3f}")
print(f"Q75: {sorted(indices)[3*len(indices)//4]:.3f}")
print(f"Max (most escalating): {max(indices):.3f}")
print(f"Min (most settling): {min(indices):.3f}")

# --- Save results ---
output = {
    "n_poems": len(poems),
    "n_counter_trend": len(counter_trend),
    "n_settlement": len(settlement),
    "pct_counter_trend": round(100 * len(counter_trend) / len(poems), 1),
    "pct_settlement": round(100 * len(settlement) / len(poems), 1),
    "pct_H_rise": round(100 * n_H_rise / len(poems), 1),
    "pct_s2_rise": round(100 * n_s2_rise / len(poems), 1),
    "era_breakdown": {
        era: {k: v for k, v in d.items()} for era, d in era_counter.items()
    },
    "top_counter_trend_poems": [
        {
            "title": p["title"],
            "author": p["author"],
            "era": p["era"],
            "delta_H": round(p["delta_H"], 3),
            "delta_s2": round(p["delta_s2"], 3),
            "n_tokens": p["n_tokens"],
        }
        for p in counter_trend_sorted[:30]
    ],
    "top_settlement_poems": [
        {
            "title": p["title"],
            "author": p["author"],
            "era": p["era"],
            "delta_H": round(p["delta_H"], 3),
            "delta_s2": round(p["delta_s2"], 3),
            "n_tokens": p["n_tokens"],
        }
        for p in settlement_sorted[:30]
    ],
    "escalation_index_stats": {
        "mean": round(statistics.mean(indices), 3),
        "std": round(statistics.stdev(indices), 3),
        "max": round(max(indices), 3),
        "min": round(min(indices), 3),
    },
    "era_counter_trend_sorted": [
        {"era": era, **d}
        for era, d in sorted(era_counter.items(), key=lambda x: x[1]["pct"], reverse=True)
    ],
}

with open("results/counter_trend_escalation.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to results/counter_trend_escalation.json")
