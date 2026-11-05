"""
Rank Topology: Where Does Poetic Surprise Live?

For each token in the corpus, GPT-2 assigns a rank to the actual chosen word.
Rank 1 = model's top prediction, rank 10000 = very unexpected choice.

Question: At what rank does S2 peak? Is the optimal surprise strategy to pick
words just outside the top-5 (near misses), or radical rank-1000+ departures?

Also: do different poets favor different rank strategies?
"""

import json
import sys
from collections import defaultdict

def load_corpus():
    with open('/home/user/s2lab/results/corpus_results.json', 'r') as f:
        return json.load(f)

def rank_band(rank):
    if rank == 1: return "rank_1"
    elif rank <= 2: return "rank_2"
    elif rank <= 5: return "rank_3-5"
    elif rank <= 10: return "rank_6-10"
    elif rank <= 20: return "rank_11-20"
    elif rank <= 50: return "rank_21-50"
    elif rank <= 100: return "rank_51-100"
    elif rank <= 500: return "rank_101-500"
    elif rank <= 1000: return "rank_501-1000"
    else: return "rank_1001+"

RANK_BANDS = ["rank_1", "rank_2", "rank_3-5", "rank_6-10", "rank_11-20",
              "rank_21-50", "rank_51-100", "rank_101-500", "rank_501-1000",
              "rank_1001+"]

def analyze():
    data = load_corpus()

    # Global: S2 by rank band
    band_tokens = defaultdict(list)  # band -> list of (s2, entropy, surprisal)

    # Per-poet: rank distribution
    poet_bands = defaultdict(lambda: defaultdict(int))  # poet -> band -> count
    poet_tokens = defaultdict(list)  # poet -> list of (rank, s2)
    poet_meta = {}  # poet -> (era, n_tokens)

    # Per-era
    era_bands = defaultdict(lambda: defaultdict(list))  # era -> band -> s2 values

    total_tokens = 0
    artifact_excluded = 0

    for poem in data:
        meta = poem['metadata']
        author = meta.get('author', 'Unknown')
        era = meta.get('era', 'unknown')
        language = meta.get('language', 'en')

        # Only English poems
        if language != 'en':
            continue

        # Only actual poetry (not control prose)
        if era in ['control', 'prose', 'cliche']:
            continue

        for tok in poem['tokens']:
            total_tokens += 1

            # Exclude stanza-break artifacts
            if tok.get('p_newline', 0) >= 0.9:
                artifact_excluded += 1
                continue

            rank = tok.get('rank')
            s2 = tok.get('s2')
            entropy = tok.get('entropy')
            surprisal = tok.get('surprisal')

            if rank is None or s2 is None or entropy is None:
                continue

            # Exclude punctuation and newlines
            token_str = tok.get('token', '')
            if token_str.strip() in ['', '\n', ',', '.', '!', '?', ';', ':', '"', "'", '(', ')', '-', '—', '–', '``', "''", '...']:
                continue

            band = rank_band(rank)
            band_tokens[band].append({
                's2': s2,
                'entropy': entropy,
                'surprisal': surprisal,
                'rank': rank,
            })

            poet_bands[author][band] += 1
            poet_tokens[author].append((rank, s2, entropy))
            era_bands[era][band].append(s2)

            if author not in poet_meta:
                poet_meta[author] = {'era': era, 'n': 0}
            poet_meta[author]['n'] += 1

    print(f"Total tokens: {total_tokens}, excluded artifacts: {artifact_excluded}")
    print(f"Analyzing {sum(len(v) for v in band_tokens.values())} clean tokens\n")

    # === Finding 1: S2 by rank band ===
    print("=" * 70)
    print("FINDING 1: S2 by rank band")
    print("=" * 70)
    print(f"{'Band':<15} {'n':>7} {'mean_S2':>9} {'mean_H':>9} {'mean_surp':>10} {'+S2%':>7} {'mean_rank':>10}")
    print("-" * 70)

    band_stats = {}
    for band in RANK_BANDS:
        toks = band_tokens[band]
        if len(toks) < 5:
            continue
        s2_vals = [t['s2'] for t in toks]
        entropy_vals = [t['entropy'] for t in toks]
        surp_vals = [t['surprisal'] for t in toks]
        rank_vals = [t['rank'] for t in toks]

        mean_s2 = sum(s2_vals) / len(s2_vals)
        mean_entropy = sum(entropy_vals) / len(entropy_vals)
        mean_surp = sum(surp_vals) / len(surp_vals)
        pos_pct = 100 * sum(1 for s in s2_vals if s > 0) / len(s2_vals)
        mean_rank = sum(rank_vals) / len(rank_vals)

        band_stats[band] = {
            'n': len(toks),
            'mean_s2': mean_s2,
            'mean_entropy': mean_entropy,
            'mean_surp': mean_surp,
            'pos_pct': pos_pct,
            'mean_rank': mean_rank,
        }
        print(f"{band:<15} {len(toks):>7,d} {mean_s2:>+9.3f} {mean_entropy:>9.3f} {mean_surp:>10.3f} {pos_pct:>7.1f} {mean_rank:>10.1f}")

    # === Finding 2: High-S2 tokens by rank band ===
    print("\n" + "=" * 70)
    print("FINDING 2: Where do genuine S2>3 spikes come from?")
    print("=" * 70)
    spike_counts = defaultdict(int)
    total_spikes = 0
    for band in RANK_BANDS:
        for t in band_tokens[band]:
            if t['s2'] > 3.0:
                spike_counts[band] += 1
                total_spikes += 1

    print(f"{'Band':<15} {'spikes':>8} {'% of all':>10} {'cumulative%':>13}")
    print("-" * 50)
    cum = 0
    for band in RANK_BANDS:
        n = spike_counts.get(band, 0)
        pct = 100 * n / total_spikes if total_spikes > 0 else 0
        cum += pct
        print(f"{band:<15} {n:>8,d} {pct:>10.1f}% {cum:>12.1f}%")
    print(f"\nTotal S2>3 spikes: {total_spikes:,d}")

    # === Finding 3: "Sweet spot" analysis — high-S2 at low entropy ===
    print("\n" + "=" * 70)
    print("FINDING 3: S2 by rank band, split by context entropy")
    print("  Low entropy = H < 5 bits (confident model)")
    print("  High entropy = H >= 5 bits (uncertain model)")
    print("=" * 70)

    low_H_bands = defaultdict(list)
    high_H_bands = defaultdict(list)
    for band in RANK_BANDS:
        for t in band_tokens[band]:
            if t['entropy'] < 5.0:
                low_H_bands[band].append(t['s2'])
            else:
                high_H_bands[band].append(t['s2'])

    print(f"{'Band':<15} {'low_H n':>8} {'low_H S2':>10} {'high_H n':>10} {'high_H S2':>11}")
    print("-" * 60)
    for band in RANK_BANDS:
        lo = low_H_bands[band]
        hi = high_H_bands[band]
        lo_mean = sum(lo) / len(lo) if lo else float('nan')
        hi_mean = sum(hi) / len(hi) if hi else float('nan')
        print(f"{band:<15} {len(lo):>8,d} {lo_mean:>+10.3f} {len(hi):>10,d} {hi_mean:>+11.3f}")

    # === Finding 4: Poet rank strategy profiles ===
    print("\n" + "=" * 70)
    print("FINDING 4: Poet rank strategy profiles")
    print("  (poets with >= 100 clean non-punctuation tokens)")
    print("=" * 70)

    # Classify poets by their typical rank usage
    poet_profiles = []
    for author, bands in poet_bands.items():
        total = sum(bands.values())
        if total < 100:
            continue

        # Compute mean rank from token list
        ranks = [r for r, s, h in poet_tokens[author]]
        mean_rank = sum(ranks) / len(ranks)

        # S2 stats
        s2_vals = [s for r, s, h in poet_tokens[author]]
        mean_s2 = sum(s2_vals) / len(s2_vals)

        # Strategy: near-miss% (rank 2-20) vs. radical% (rank 1001+)
        near_miss = sum(bands.get(b, 0) for b in ['rank_2', 'rank_3-5', 'rank_6-10', 'rank_11-20'])
        radical = bands.get('rank_1001+', 0)
        conventional = bands.get('rank_1', 0)

        near_miss_pct = 100 * near_miss / total
        radical_pct = 100 * radical / total
        conventional_pct = 100 * conventional / total

        era = poet_meta[author]['era']

        poet_profiles.append({
            'author': author,
            'era': era,
            'n': total,
            'mean_rank': mean_rank,
            'mean_s2': mean_s2,
            'conventional_pct': conventional_pct,
            'near_miss_pct': near_miss_pct,
            'radical_pct': radical_pct,
        })

    # Sort by mean_rank
    poet_profiles.sort(key=lambda x: x['mean_rank'])

    print(f"\n{'Author':<25} {'Era':<20} {'n':>5} {'MeanRank':>9} {'MeanS2':>8} {'Conv%':>7} {'Near%':>7} {'Radical%':>9}")
    print("-" * 92)
    for p in poet_profiles[:30]:
        print(f"{p['author'][:24]:<25} {p['era'][:19]:<20} {p['n']:>5} {p['mean_rank']:>9.0f} "
              f"{p['mean_s2']:>+8.3f} {p['conventional_pct']:>7.1f} {p['near_miss_pct']:>7.1f} {p['radical_pct']:>9.1f}")

    # === Finding 5: Era rank profiles ===
    print("\n" + "=" * 70)
    print("FINDING 5: Mean rank and S2 by era")
    print("=" * 70)

    era_stats = {}
    for era, bands_data in era_bands.items():
        all_s2 = []
        for b, vals in bands_data.items():
            all_s2.extend(vals)
        if len(all_s2) < 20:
            continue

        # Compute mean S2 and rank composition
        mean_s2 = sum(all_s2) / len(all_s2)
        era_stats[era] = {
            'n': len(all_s2),
            'mean_s2': mean_s2,
        }

    sorted_eras = sorted(era_stats.items(), key=lambda x: x[1]['mean_s2'], reverse=True)
    print(f"{'Era':<25} {'n':>6} {'mean_S2':>9}")
    print("-" * 45)
    for era, stats in sorted_eras[:20]:
        print(f"{era:<25} {stats['n']:>6,d} {stats['mean_s2']:>+9.3f}")

    # === Save results ===
    results = {
        'band_stats': band_stats,
        'spike_counts': dict(spike_counts),
        'total_spikes': total_spikes,
        'poet_profiles': poet_profiles,
        'era_stats': era_stats,
    }

    with open('/home/user/s2lab/results/rank_topology.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to results/rank_topology.json")
    return results

if __name__ == '__main__':
    analyze()
