"""
Rank Profile: Where in GPT-2's distribution do poets aim?
==========================================================
S2 tells us HOW surprising a choice was given its context.
But RANK tells us WHERE in GPT-2's probability distribution
the poet reached: rank 50 = "near miss," rank 5000 = "wild shot."

These are distinct: a rank-100 word in high-entropy context (many possible
words) may have low S2, while the same rank-100 in low-entropy context
could yield very high S2. Rank measures the poet's target depth in the
tail of GPT-2's distribution; S2 measures the surprise given context.

Research questions:
1. Do poets/eras have characteristic "rank profiles" (consistent target depth)?
2. Do certain forms (haiku, sonnet, free verse) show different rank distributions?
3. What is the relationship between rank tier and S2 magnitude?
4. Can we identify "near-miss deviators" vs "wild deviators" in the corpus?
"""

import json
import os
from collections import defaultdict
import statistics

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

# Rank tiers
RANK_TIERS = [
    ("top1",    1,     1),    # GPT-2's exact choice
    ("near",    2,    50),    # Near misses
    ("mid",    51,   500),    # Mid-range deviations
    ("far",   501,  5000),    # Far deviations
    ("wild", 5001, 999999),   # Wild shots
]

def tier(rank):
    for name, lo, hi in RANK_TIERS:
        if lo <= rank <= hi:
            return name
    return "wild"

def load_data():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)

def analyze():
    data = load_data()

    # Per-era and per-author aggregation
    era_data = defaultdict(list)      # era -> list of (rank, s2, era)
    author_data = defaultdict(list)   # author -> list of (rank, s2)
    all_tokens = []

    for poem in data:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")

        for tok in poem["tokens"]:
            if tok.get("p_newline", 0) >= 0.9:
                continue  # Skip stanza-break artifacts
            rank = tok.get("rank", 0)
            s2 = tok.get("s2", 0)
            if rank <= 0:
                continue

            era_data[era].append((rank, s2))
            author_data[author].append((rank, s2))
            all_tokens.append((rank, s2, era, author))

    # --- Global rank tier distribution ---
    global_tiers = defaultdict(int)
    global_s2_by_tier = defaultdict(list)
    for rank, s2, _, _ in all_tokens:
        t = tier(rank)
        global_tiers[t] += 1
        global_s2_by_tier[t].append(s2)

    total = len(all_tokens)
    global_tier_stats = {}
    for t_name, _, _ in RANK_TIERS:
        n = global_tiers[t_name]
        s2_vals = global_s2_by_tier[t_name]
        global_tier_stats[t_name] = {
            "n": n,
            "pct": round(100 * n / total, 1),
            "mean_s2": round(statistics.mean(s2_vals), 3) if s2_vals else 0,
            "median_s2": round(statistics.median(s2_vals), 3) if s2_vals else 0,
        }

    # --- Per-era rank profiles ---
    era_profiles = {}
    for era, tokens in era_data.items():
        if len(tokens) < 50:
            continue
        tiers = defaultdict(list)
        for rank, s2 in tokens:
            tiers[tier(rank)].append(s2)
        n_total = len(tokens)
        profile = {
            "n": n_total,
            "median_rank": round(statistics.median([r for r, _ in tokens])),
            "wild_ratio": round(100 * len(tiers["wild"]) / n_total, 1),
            "near_ratio": round(100 * len(tiers["near"]) / n_total, 1),
            "mean_s2": round(statistics.mean([s for _, s in tokens]), 3),
        }
        era_profiles[era] = profile

    # Sort by wild_ratio descending
    era_profiles_sorted = sorted(era_profiles.items(), key=lambda x: x[1]["wild_ratio"], reverse=True)

    # --- Per-author rank profiles (≥200 tokens) ---
    author_profiles = {}
    for author, tokens in author_data.items():
        if len(tokens) < 200:
            continue
        tiers = defaultdict(list)
        for rank, s2 in tokens:
            tiers[tier(rank)].append(s2)
        n_total = len(tokens)
        profile = {
            "n": n_total,
            "median_rank": round(statistics.median([r for r, _ in tokens])),
            "wild_ratio": round(100 * len(tiers["wild"]) / n_total, 1),
            "near_ratio": round(100 * len(tiers["near"]) / n_total, 1),
            "mid_ratio": round(100 * len(tiers["mid"]) / n_total, 1),
            "far_ratio": round(100 * len(tiers["far"]) / n_total, 1),
            "mean_s2": round(statistics.mean([s for _, s in tokens]), 3),
        }
        author_profiles[author] = profile

    author_profiles_sorted = sorted(author_profiles.items(), key=lambda x: x[1]["wild_ratio"], reverse=True)

    # --- Rank-tier × S2 relationship ---
    # For positive S2 tokens only (actual surprises), what's the tier distribution?
    pos_s2_tier_dist = defaultdict(list)
    for rank, s2, _, _ in all_tokens:
        if s2 > 0:
            pos_s2_tier_dist[tier(rank)].append(s2)

    pos_total = sum(len(v) for v in pos_s2_tier_dist.values())
    pos_tier_stats = {}
    for t_name, _, _ in RANK_TIERS:
        vals = pos_s2_tier_dist[t_name]
        pos_tier_stats[t_name] = {
            "n": len(vals),
            "pct_of_pos_s2": round(100 * len(vals) / pos_total, 1) if pos_total else 0,
            "mean_s2": round(statistics.mean(vals), 3) if vals else 0,
        }

    # --- S2 quartiles × rank ---
    # Bucket tokens by S2 quartile; look at rank distribution within each
    s2_vals_all = [s for _, s, _, _ in all_tokens]
    q25 = sorted(s2_vals_all)[len(s2_vals_all)//4]
    q50 = sorted(s2_vals_all)[len(s2_vals_all)//2]
    q75 = sorted(s2_vals_all)[3*len(s2_vals_all)//4]

    s2_q_ranks = defaultdict(list)
    for rank, s2, _, _ in all_tokens:
        if s2 <= q25: q_name = "Q1_low"
        elif s2 <= q50: q_name = "Q2"
        elif s2 <= q75: q_name = "Q3"
        else: q_name = "Q4_high"
        s2_q_ranks[q_name].append(rank)

    s2_rank_stats = {}
    for q in ["Q1_low", "Q2", "Q3", "Q4_high"]:
        vals = s2_q_ranks[q]
        s2_rank_stats[q] = {
            "n": len(vals),
            "median_rank": round(statistics.median(vals)),
            "pct_wild": round(100 * sum(1 for r in vals if r > 5000) / len(vals), 1),
            "pct_near": round(100 * sum(1 for r in vals if r <= 50) / len(vals), 1),
        }

    results = {
        "total_tokens": total,
        "global_tier_stats": global_tier_stats,
        "era_profiles": dict(era_profiles_sorted),
        "author_profiles": dict(author_profiles_sorted),
        "pos_s2_tier_distribution": pos_tier_stats,
        "s2_quartile_rank_stats": s2_rank_stats,
        "s2_quartile_thresholds": {"q25": round(q25, 3), "q50": round(q50, 3), "q75": round(q75, 3)},
    }

    out_path = os.path.join(RESULTS_DIR, "rank_profile_by_poet.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Analyzed {total} tokens across {len(era_profiles)} eras, {len(author_profiles)} authors")
    print(f"Results saved to {out_path}")
    return results

if __name__ == "__main__":
    analyze()
