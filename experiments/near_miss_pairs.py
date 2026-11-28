"""
Near-Miss Pairs: What Poets Choose When GPT-2 Is Close But Not Right

When a poet's actual word is in GPT-2's top-10 predictions but isn't the #1 pick,
the shadow of the top prediction hangs visibly in the air. This creates a rhetorical
"almost"—the reader's completing mind supplies the rank-1 word, but the poet supplies
rank-2 or rank-3 instead.

This experiment catalogs these (actual, shadow) near-miss pairs and asks:
- Are near-miss choices related to their shadow (same POS? morphological family?)?
- Which eras use the near-miss zone most heavily?
- What is the typical probability gap between shadow (rank-1) and actual (rank-2)?
- Do near-miss pairs form predictable semantic patterns (antonym, synonym, same frame)?
"""

import json
import math
import statistics
import re
from collections import defaultdict, Counter

with open('results/corpus_results.json') as f:
    data = json.load(f)

# Artifact filter
def is_artifact(tok):
    return tok.get('p_newline', 0) >= 0.9

# Near-miss: actual token is in top-10 alternatives at rank 2-10
# (rank=1 is perfect match, rank>10 means not in the visible prediction menu)
near_miss_records = []
rank_zone_by_era = defaultdict(lambda: defaultdict(int))
all_clean_tokens_by_era = defaultdict(int)

for poem in data:
    meta = poem['metadata']
    era = meta.get('era', 'unknown')
    author = meta.get('author', 'Unknown')
    title = meta.get('title', 'Unknown')
    tokens = poem.get('tokens', [])
    n_tokens = len(tokens)

    for i, tok in enumerate(tokens):
        if is_artifact(tok):
            continue

        rank = tok.get('rank')
        s2 = tok.get('s2', 0)
        entropy = tok.get('entropy', 0)
        surprisal = tok.get('surprisal', 0)
        actual_token = str(tok.get('token', ''))
        alternatives = tok.get('alternatives', [])
        pos_pct = i / n_tokens if n_tokens > 0 else 0

        all_clean_tokens_by_era[era] += 1

        # Classify rank zone
        if rank == 1:
            zone = 'rank1_exact'
        elif rank is not None and 2 <= rank <= 5:
            zone = 'rank2_5_nearmiss'
        elif rank is not None and 6 <= rank <= 10:
            zone = 'rank6_10_menu'
        elif rank is not None and 11 <= rank <= 50:
            zone = 'rank11_50_fringe'
        elif rank is not None and rank > 50:
            zone = 'rank51plus_radical'
        else:
            zone = 'unknown'

        rank_zone_by_era[era][zone] += 1

        # For near-miss tokens in rank 2-5: extract the shadow (rank-1 prediction)
        if rank is not None and 2 <= rank <= 5 and alternatives:
            # alternatives is list of {token, prob} sorted by probability (rank-1 first)
            shadow_token = str(alternatives[0]['token']) if alternatives else None
            shadow_prob = alternatives[0]['prob'] if alternatives else 0
            actual_prob = tok.get('prob', 0)

            # Probability gap: how much more likely was the shadow?
            prob_gap = shadow_prob - actual_prob
            prob_ratio = shadow_prob / actual_prob if actual_prob > 0 else float('inf')

            # Character-level relationship analysis
            a_clean = actual_token.strip().lower()
            s_clean = shadow_token.strip().lower() if shadow_token else ''

            # Shared prefix length
            prefix_len = 0
            for ca, cs in zip(a_clean, s_clean):
                if ca == cs:
                    prefix_len += 1
                else:
                    break

            # Length difference
            len_diff = len(a_clean) - len(s_clean)

            # Is shadow a prefix/suffix of actual or vice versa?
            is_morphological = (
                a_clean.startswith(s_clean) or
                s_clean.startswith(a_clean) or
                (len(a_clean) > 3 and len(s_clean) > 3 and
                 (a_clean[:-2] == s_clean[:-2] or a_clean[:-3] == s_clean[:-3]))
            )

            # Shared character proportion
            max_len = max(len(a_clean), len(s_clean), 1)
            char_overlap = prefix_len / max_len

            near_miss_records.append({
                'actual': actual_token,
                'shadow': shadow_token,
                'rank': rank,
                's2': s2,
                'entropy': entropy,
                'surprisal': surprisal,
                'shadow_prob': shadow_prob,
                'actual_prob': actual_prob,
                'prob_gap': prob_gap,
                'prob_ratio': prob_ratio,
                'prefix_len': prefix_len,
                'len_diff': len_diff,
                'is_morphological': is_morphological,
                'char_overlap': char_overlap,
                'era': era,
                'author': author,
                'title': title,
                'pos_pct': pos_pct,
            })

print(f"Total near-miss records (rank 2-5): {len(near_miss_records)}")

# --- ANALYSIS 1: Overall distribution ---
print("\n=== 1. Rank Zone Distribution (clean tokens) ===")
all_zones = Counter()
for era_data in rank_zone_by_era.values():
    for zone, count in era_data.items():
        all_zones[zone] += count

total_clean = sum(all_zones.values())
zone_order = ['rank1_exact', 'rank2_5_nearmiss', 'rank6_10_menu', 'rank11_50_fringe', 'rank51plus_radical']
for zone in zone_order:
    n = all_zones[zone]
    print(f"  {zone}: {n} ({100*n/total_clean:.1f}%)")

# --- ANALYSIS 2: Near-miss statistics ---
print("\n=== 2. Near-Miss Pair Statistics ===")
nm = near_miss_records
if nm:
    prob_gaps = [r['prob_gap'] for r in nm]
    prob_ratios = [r['prob_ratio'] for r in nm if r['prob_ratio'] != float('inf')]
    char_overlaps = [r['char_overlap'] for r in nm]
    morph_count = sum(1 for r in nm if r['is_morphological'])
    s2_vals = [r['s2'] for r in nm]

    print(f"  N near-miss tokens: {len(nm)}")
    print(f"  Avg S₂: {statistics.mean(s2_vals):.3f} (median: {statistics.median(s2_vals):.3f})")
    print(f"  Avg shadow→actual prob gap: {statistics.mean(prob_gaps):.4f}")
    print(f"  Avg shadow/actual prob ratio: {statistics.mean(prob_ratios):.2f}x")
    print(f"  Avg character overlap (actual vs shadow): {statistics.mean(char_overlaps):.3f}")
    print(f"  Morphologically related pairs: {morph_count} ({100*morph_count/len(nm):.1f}%)")

# --- ANALYSIS 3: Most common near-miss pairs ---
print("\n=== 3. Most Common Near-Miss Pairs (actual ← shadow) ===")
pair_counter = Counter()
for r in nm:
    actual_clean = r['actual'].strip().lower()
    shadow_clean = r['shadow'].strip().lower() if r['shadow'] else '?'
    pair_counter[(actual_clean, shadow_clean)] += 1

print("  Top 25 near-miss pairs (actual ← shadow, count):")
for (actual, shadow), cnt in pair_counter.most_common(25):
    print(f"    '{actual}' (chose) ← '{shadow}' (GPT-2 wanted): {cnt}x")

# --- ANALYSIS 4: By era — near-miss rate ---
print("\n=== 4. Near-Miss Rate by Era (% of clean tokens in rank 2-5) ===")
era_stats = []
for era, zones in rank_zone_by_era.items():
    total = sum(zones.values())
    if total < 50:
        continue
    nm_count = zones.get('rank2_5_nearmiss', 0)
    r1_count = zones.get('rank1_exact', 0)
    radical_count = zones.get('rank51plus_radical', 0)
    nm_rate = nm_count / total
    r1_rate = r1_count / total
    radical_rate = radical_count / total
    era_stats.append((era, total, nm_rate, r1_rate, radical_rate))

era_stats.sort(key=lambda x: -x[2])  # sort by near-miss rate
print(f"  {'Era':<30} {'n':>6} {'NM rate':>8} {'R1 rate':>8} {'Radical':>8}")
for era, total, nm_r, r1_r, rad_r in era_stats:
    print(f"  {era:<30} {total:>6} {100*nm_r:>7.1f}% {100*r1_r:>7.1f}% {100*rad_r:>7.1f}%")

# --- ANALYSIS 5: Semantic category of near-miss pairs ---
print("\n=== 5. Character Overlap Distribution of Near-Miss Pairs ===")
# Classify overlap into rough semantic categories
def tok_str(val):
    return str(val).strip().lower() if val is not None else ''

exact_copy = sum(1 for r in nm if tok_str(r['actual']) == tok_str(r['shadow']))
high_overlap = sum(1 for r in nm if r['char_overlap'] >= 0.7 and tok_str(r['actual']) != tok_str(r['shadow']))
low_overlap = sum(1 for r in nm if r['char_overlap'] < 0.3)
mid_overlap = len(nm) - exact_copy - high_overlap - low_overlap

print(f"  Exact same string (capitalization/whitespace only): {exact_copy} ({100*exact_copy/len(nm):.1f}%)")
print(f"  High char overlap (≥70%): {high_overlap} ({100*high_overlap/len(nm):.1f}%)")
print(f"  Mid char overlap (30-70%): {mid_overlap} ({100*mid_overlap/len(nm):.1f}%)")
print(f"  Low char overlap (<30%, likely different words): {low_overlap} ({100*low_overlap/len(nm):.1f}%)")

# High-overlap examples (morphological near-miss)
print("\n  High-overlap near-miss examples:")
high_examples = [(r['actual'], r['shadow'], r['char_overlap'], r['era'])
                 for r in nm if r['char_overlap'] >= 0.7 and tok_str(r['actual']) != tok_str(r['shadow'])]
high_examples.sort(key=lambda x: -x[2])
for actual, shadow, overlap, era in high_examples[:20]:
    print(f"    '{str(actual).strip()}' ← '{str(shadow).strip() if shadow else '?'}' (overlap={overlap:.2f}, era={era})")

# Low-overlap examples (semantic divergence)
print("\n  Low-overlap near-miss examples (semantic jumps):")
low_examples = [(r['actual'], r['shadow'], r['s2'], r['era'])
                for r in nm if r['char_overlap'] < 0.3]
low_examples.sort(key=lambda x: -x[2])
for actual, shadow, s2, era in low_examples[:20]:
    print(f"    '{str(actual).strip()}' ← '{str(shadow).strip() if shadow else '?'}' (S₂={s2:.2f}, era={era})")

# --- ANALYSIS 6: Position in poem for near-miss ---
print("\n=== 6. Near-Miss Position in Poem ===")
nm_pos = [r['pos_pct'] for r in nm]
nm_q1 = sum(1 for p in nm_pos if p < 0.25)
nm_q2 = sum(1 for p in nm_pos if 0.25 <= p < 0.5)
nm_q3 = sum(1 for p in nm_pos if 0.5 <= p < 0.75)
nm_q4 = sum(1 for p in nm_pos if p >= 0.75)
n_total = len(nm_pos)
print(f"  First quarter (0-25%): {nm_q1} ({100*nm_q1/n_total:.1f}%)")
print(f"  Second quarter (25-50%): {nm_q2} ({100*nm_q2/n_total:.1f}%)")
print(f"  Third quarter (50-75%): {nm_q3} ({100*nm_q3/n_total:.1f}%)")
print(f"  Fourth quarter (75-100%): {nm_q4} ({100*nm_q4/n_total:.1f}%)")

# Save results
results = {
    'zone_distribution': {z: {'n': all_zones[z], 'pct': 100*all_zones[z]/total_clean} for z in zone_order},
    'near_miss_stats': {
        'n': len(nm),
        'avg_s2': statistics.mean([r['s2'] for r in nm]) if nm else 0,
        'median_s2': statistics.median([r['s2'] for r in nm]) if nm else 0,
        'avg_prob_gap': statistics.mean([r['prob_gap'] for r in nm]) if nm else 0,
        'avg_char_overlap': statistics.mean([r['char_overlap'] for r in nm]) if nm else 0,
        'morph_pct': 100*morph_count/len(nm) if nm else 0,
    },
    'top_pairs': [{'actual': a, 'shadow': s, 'count': c} for (a, s), c in pair_counter.most_common(50)],
    'era_near_miss_rates': [
        {'era': era, 'n': total, 'nm_rate': nm, 'r1_rate': r1, 'radical_rate': rad}
        for era, total, nm, r1, rad in sorted(era_stats, key=lambda x: -x[2])
    ],
    'overlap_distribution': {
        'exact': exact_copy, 'high': high_overlap, 'mid': mid_overlap, 'low': low_overlap
    },
    'position': {
        'q1': nm_q1, 'q2': nm_q2, 'q3': nm_q3, 'q4': nm_q4
    }
}

with open('results/near_miss_pairs.json', 'w') as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/near_miss_pairs.json")
