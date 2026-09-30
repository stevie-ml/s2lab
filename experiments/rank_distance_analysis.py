"""
Rank Distance Analysis: How Far From GPT-2's Top Prediction Do Poets Go?

When poets surprise us, are they choosing rank 11-50 ("near-miss deviations")
or rank 500+ ("radical departures")? This experiment maps the full rank distribution
of poetic choices and asks whether "near-miss" vs "radical" strategies differ by era,
by entropy level, and by position in the poem.

Builds on: lexical_fork_analysis.md, confidence_trap_analysis.md
"""

import json
import math
import statistics
from collections import defaultdict

with open('results/corpus_results.json') as f:
    data = json.load(f)

# Collect all tokens with metadata
all_tokens = []
for poem in data:
    meta = poem['metadata']
    era = meta.get('era', 'unknown')
    author = meta.get('author', 'Unknown')
    title = meta.get('title', 'Unknown')
    tokens = poem.get('tokens', [])
    n_tokens = len(tokens)

    for i, tok in enumerate(tokens):
        rank = tok.get('rank')
        if rank is None:
            continue
        s2 = tok.get('s2', 0)
        entropy = tok.get('entropy', 0)
        surprisal = tok.get('surprisal', 0)
        p_newline = tok.get('p_newline', 0)
        token_str = tok.get('token', '')
        position = tok.get('position', i + 1)

        # Position within poem (0=first, 1=last)
        relative_pos = position / n_tokens if n_tokens > 0 else 0.5

        all_tokens.append({
            'era': era,
            'author': author,
            'title': title,
            'rank': rank,
            's2': s2,
            'entropy': entropy,
            'surprisal': surprisal,
            'p_newline': p_newline,
            'token': token_str,
            'relative_pos': relative_pos,
            'position': position,
        })

# Remove stanza-break artifact tokens
clean_tokens = [t for t in all_tokens if t['p_newline'] < 0.9]

print(f"Total tokens: {len(all_tokens)}")
print(f"Clean tokens (stanza-break artifact removed): {len(clean_tokens)}")
print()

# ─────────────────────────────────────────────
# 1. OVERALL RANK DISTRIBUTION
# ─────────────────────────────────────────────

def rank_bucket(rank):
    if rank == 1:
        return "1 (exact match)"
    elif rank <= 5:
        return "2-5 (top predicted)"
    elif rank <= 10:
        return "6-10 (in model menu)"
    elif rank <= 20:
        return "11-20 (near miss)"
    elif rank <= 50:
        return "21-50 (moderate miss)"
    elif rank <= 100:
        return "51-100 (moderate)"
    elif rank <= 500:
        return "101-500 (wide miss)"
    elif rank <= 1000:
        return "501-1000 (far miss)"
    elif rank <= 5000:
        return "1001-5000 (radical)"
    else:
        return "5000+ (extreme)"

bucket_order = [
    "1 (exact match)", "2-5 (top predicted)", "6-10 (in model menu)",
    "11-20 (near miss)", "21-50 (moderate miss)", "51-100 (moderate)",
    "101-500 (wide miss)", "501-1000 (far miss)", "1001-5000 (radical)",
    "5000+ (extreme)"
]

print("=" * 60)
print("1. OVERALL RANK DISTRIBUTION (clean tokens, all eras)")
print("=" * 60)

buckets = defaultdict(list)
for t in clean_tokens:
    b = rank_bucket(t['rank'])
    buckets[b].append(t)

total_clean = len(clean_tokens)
print(f"\n{'Rank bucket':<30} {'Count':>8} {'%':>7} {'Avg S2':>9} {'%+S2':>7}")
print("-" * 65)
for b in bucket_order:
    toks = buckets[b]
    if not toks:
        continue
    count = len(toks)
    pct = count / total_clean * 100
    avg_s2 = statistics.mean(t['s2'] for t in toks)
    pos_s2_pct = sum(1 for t in toks if t['s2'] > 0) / count * 100
    print(f"{b:<30} {count:>8,} {pct:>7.1f}% {avg_s2:>9.3f} {pos_s2_pct:>7.1f}%")

print()

# ─────────────────────────────────────────────
# 2. RANK DISTRIBUTION BY S2 ZONE
# ─────────────────────────────────────────────

print("=" * 60)
print("2. RANK DISTRIBUTION BY S2 ZONE")
print("=" * 60)

low_s2 = [t for t in clean_tokens if t['s2'] < -1.0]
mid_s2 = [t for t in clean_tokens if -1.0 <= t['s2'] <= 1.0]
high_s2 = [t for t in clean_tokens if t['s2'] > 1.0]
very_high_s2 = [t for t in clean_tokens if t['s2'] > 5.0]

def rank_distribution_summary(tokens, label):
    if not tokens:
        return
    ranks = [t['rank'] for t in tokens]
    median_r = statistics.median(ranks)
    mean_r = statistics.mean(ranks)
    pct_near_miss = sum(1 for r in ranks if 11 <= r <= 50) / len(ranks) * 100
    pct_radical = sum(1 for r in ranks if r > 500) / len(ranks) * 100
    pct_extreme = sum(1 for r in ranks if r > 5000) / len(ranks) * 100
    print(f"  {label}: n={len(tokens):,}, median_rank={median_r:.0f}, "
          f"near-miss(11-50)={pct_near_miss:.1f}%, "
          f"radical(>500)={pct_radical:.1f}%, "
          f"extreme(>5000)={pct_extreme:.1f}%")

print()
rank_distribution_summary(low_s2, "LOW S2 (<-1.0)")
rank_distribution_summary(mid_s2, "MID S2 (-1.0 to 1.0)")
rank_distribution_summary(high_s2, "HIGH S2 (>1.0)")
rank_distribution_summary(very_high_s2, "VERY HIGH S2 (>5.0)")
print()

# ─────────────────────────────────────────────
# 3. NEAR-MISS vs RADICAL DEVIATION — by era
# ─────────────────────────────────────────────

print("=" * 60)
print("3. ERA COMPARISON: 'NEAR-MISS' vs 'RADICAL' DEVIATION STRATEGY")
print("   (Among tokens with rank > 10, i.e., not predicted by GPT-2)")
print("=" * 60)

# Only look at "deviation" tokens (rank > 10)
deviation_tokens = [t for t in clean_tokens if t['rank'] > 10]

era_data = defaultdict(list)
for t in deviation_tokens:
    era_data[t['era']].append(t)

# Compute near-miss rate and radical rate per era
era_stats = {}
for era, toks in era_data.items():
    if len(toks) < 50:
        continue
    ranks = [t['rank'] for t in toks]
    near_miss = sum(1 for r in ranks if 11 <= r <= 50) / len(ranks)
    radical = sum(1 for r in ranks if r > 500) / len(ranks)
    extreme = sum(1 for r in ranks if r > 5000) / len(ranks)
    median_rank = statistics.median(ranks)
    mean_rank = statistics.mean(ranks)
    avg_s2 = statistics.mean(t['s2'] for t in toks)
    era_stats[era] = {
        'n': len(toks),
        'near_miss': near_miss,
        'radical': radical,
        'extreme': extreme,
        'median_rank': median_rank,
        'mean_rank': mean_rank,
        'avg_s2': avg_s2,
    }

print(f"\n{'Era':<22} {'N':>6} {'Median rank':>12} {'Near-miss%':>11} {'Radical%':>10} {'Extreme%':>10} {'Avg S2':>8}")
print("-" * 85)
# Sort by median rank (ascending = more predictable, descending = more radical)
for era, stats in sorted(era_stats.items(), key=lambda x: x[1]['median_rank']):
    print(f"{era:<22} {stats['n']:>6,} {stats['median_rank']:>12.0f} "
          f"{stats['near_miss']*100:>10.1f}% {stats['radical']*100:>9.1f}% "
          f"{stats['extreme']*100:>9.1f}% {stats['avg_s2']:>8.3f}")
print()

# ─────────────────────────────────────────────
# 4. RANK vs ENTROPY LEVEL
# ─────────────────────────────────────────────

print("=" * 60)
print("4. RANK DISTRIBUTION BY ENTROPY LEVEL")
print("   (How far do poets deviate when GPT-2 is confident vs uncertain?)")
print("=" * 60)

# Quartile entropy breakdown
entropies = sorted(t['entropy'] for t in clean_tokens)
q25 = entropies[int(len(entropies) * 0.25)]
q75 = entropies[int(len(entropies) * 0.75)]

low_ent = [t for t in clean_tokens if t['entropy'] < q25 and t['rank'] > 10]
high_ent = [t for t in clean_tokens if t['entropy'] > q75 and t['rank'] > 10]

print(f"\n  Entropy Q25={q25:.2f} bits, Q75={q75:.2f} bits")
print()
rank_distribution_summary(low_ent, "LOW entropy (confident model, rank>10)")
rank_distribution_summary(high_ent, "HIGH entropy (uncertain model, rank>10)")
print()

# ─────────────────────────────────────────────
# 5. TEMPORAL RANK EVOLUTION WITHIN POEMS
# ─────────────────────────────────────────────

print("=" * 60)
print("5. TEMPORAL RANK EVOLUTION WITHIN POEMS")
print("   (Do poets make more radical choices early or late?)")
print("=" * 60)

deviation_toks = [t for t in clean_tokens if t['rank'] > 10]

thirds = {'early (0-33%)': [], 'middle (33-66%)': [], 'late (66-100%)': []}
for t in deviation_toks:
    pos = t['relative_pos']
    if pos < 0.33:
        thirds['early (0-33%)'].append(t)
    elif pos < 0.66:
        thirds['middle (33-66%)'].append(t)
    else:
        thirds['late (66-100%)'].append(t)

print()
for label, toks in thirds.items():
    rank_distribution_summary(toks, label)
print()

# ─────────────────────────────────────────────
# 6. HIGHEST-RANK DEVIATIONS: The Most Radical Moments
# ─────────────────────────────────────────────

print("=" * 60)
print("6. THE MOST RADICAL DEPARTURES (rank > 10000, clean)")
print("=" * 60)

extreme_tokens = sorted(
    [t for t in clean_tokens if t['rank'] > 10000],
    key=lambda t: -t['rank']
)[:20]

print(f"\n{'Token':<20} {'Author':<22} {'Rank':>7} {'S2':>7} {'Entropy':>9} {'Context'}")
print("-" * 85)
for t in extreme_tokens:
    author_short = t['author'].split()[-1] if t['author'] else 'Unknown'
    ctx = t.get('context_before', '')[-20:].replace('\n', '↵')
    token_disp = repr(t['token'])[:18]
    print(f"{token_disp:<20} {author_short:<22} {t['rank']:>7,} {t['s2']:>7.2f} {t['entropy']:>9.2f}  …{ctx}")
print()

# ─────────────────────────────────────────────
# 7. "NEAR-MISS" POETS vs "RADICAL DEPARTURE" POETS
# ─────────────────────────────────────────────

print("=" * 60)
print("7. POET SIGNATURES: NEAR-MISS vs RADICAL STRATEGY")
print("=" * 60)

author_data = defaultdict(list)
for t in deviation_tokens:
    author_data[t['author']].append(t)

author_stats = {}
for author, toks in author_data.items():
    if len(toks) < 30:
        continue
    ranks = [t['rank'] for t in toks]
    near_miss_rate = sum(1 for r in ranks if 11 <= r <= 50) / len(ranks)
    radical_rate = sum(1 for r in ranks if r > 500) / len(ranks)
    median_rank = statistics.median(ranks)
    avg_s2 = statistics.mean(t['s2'] for t in toks)
    author_stats[author] = {
        'n': len(toks),
        'near_miss_rate': near_miss_rate,
        'radical_rate': radical_rate,
        'median_rank': median_rank,
        'avg_s2': avg_s2,
    }

# Sort by near-miss rate (highest = "near-miss poets")
print(f"\n{'Author':<28} {'N':>5} {'Median rank':>12} {'Near-miss%':>11} {'Radical%':>10} {'Avg S2':>8}")
print("-" * 80)
for author, stats in sorted(author_stats.items(), key=lambda x: x[1]['median_rank']):
    if len(author_stats) > 20 and stats['n'] < 50:
        continue
    print(f"{author:<28} {stats['n']:>5} {stats['median_rank']:>12.0f} "
          f"{stats['near_miss_rate']*100:>10.1f}% {stats['radical_rate']*100:>9.1f}% "
          f"{stats['avg_s2']:>8.3f}")
print()

# ─────────────────────────────────────────────
# 8. RANK QUARTILE X ERA HEATMAP
# ─────────────────────────────────────────────

print("=" * 60)
print("8. RANK QUARTILE DISTRIBUTION BY ERA (deviation tokens only)")
print("=" * 60)

# Compute rank quartiles globally
all_dev_ranks = sorted(t['rank'] for t in deviation_tokens)
q1_rank = all_dev_ranks[len(all_dev_ranks)//4]
q2_rank = all_dev_ranks[len(all_dev_ranks)//2]
q3_rank = all_dev_ranks[3*len(all_dev_ranks)//4]

print(f"\n  Global rank quartiles: Q1={q1_rank}, Q2={q2_rank}, Q3={q3_rank}")
print()

key_eras = ['romantic', 'victorian', 'modernist', 'confessional', 'new_york_school',
            'language', 'beat', 'found_poetry', 'prose_poetry', 'haiku',
            'ballad', 'control']

print(f"{'Era':<22} {'N':>5} {'Q1%(≤'+str(q1_rank)+')':>10} {'Q2%(≤'+str(q2_rank)+')':>10} {'Q3%(≤'+str(q3_rank)+')':>10} {'Q4%(>'+str(q3_rank)+')':>10}")
print("-" * 70)
for era in key_eras:
    toks = era_data.get(era, [])
    if len(toks) < 30:
        continue
    ranks = [t['rank'] for t in toks]
    q1_pct = sum(1 for r in ranks if r <= q1_rank) / len(ranks) * 100
    q2_pct = sum(1 for r in ranks if q1_rank < r <= q2_rank) / len(ranks) * 100
    q3_pct = sum(1 for r in ranks if q2_rank < r <= q3_rank) / len(ranks) * 100
    q4_pct = sum(1 for r in ranks if r > q3_rank) / len(ranks) * 100
    print(f"{era:<22} {len(ranks):>5} {q1_pct:>9.1f}% {q2_pct:>9.1f}% {q3_pct:>9.1f}% {q4_pct:>9.1f}%")

print()
print("Done.")
