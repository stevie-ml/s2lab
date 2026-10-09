"""
Alternatives Architecture: The Shape of the Prediction Cloud

At each token position, GPT-2 assigns probabilities to all possible next tokens.
The top-10 alternatives in corpus_results.json let us characterize the *shape*
of this prediction cloud:

- top_ratio: how dominant is the top prediction over the second? (p[0]/p[1])
- coverage_10: how much of the total probability mass do top-10 alternatives cover?
- spread: how quickly do probabilities decay? (p[9]/p[0])

This creates a 4-type taxonomy of poetic surprise:
  AMBUSH:    high top_ratio + high S2  → poet defied a confident, specific prediction
  FOG:       low top_ratio + high S2   → poet surprised in a diffuse uncertainty
  COMPLIANCE: any distribution + low S2 → poet conformed to expectation
  NEAR-MISS: poet chose within top-10 but not top-1
"""
import json
import math
from collections import defaultdict

ARTIFACT_FILTER = 0.9
HIGH_S2_THRESH = 2.0
NEAR_MISS_THRESH = 0.5  # poet's choice in top-10 if rank <= 10

def classify_distribution(alts):
    """Classify the shape of top-10 alternatives distribution."""
    if len(alts) < 2:
        return None
    p0 = alts[0]['prob']
    p1 = alts[1]['prob']
    p9 = alts[-1]['prob'] if len(alts) >= 10 else alts[-1]['prob']
    coverage = sum(a['prob'] for a in alts)
    top_ratio = p0 / p1 if p1 > 0 else float('inf')
    spread = p9 / p0 if p0 > 0 else 0.0
    return {
        'top_ratio': top_ratio,
        'spread': spread,
        'coverage_10': coverage,
        'p0': p0,
        'p1': p1,
    }

def categorize_surprise(s2, top_ratio, rank, is_artifact):
    """Assign surprise category."""
    if is_artifact:
        return 'artifact'
    if rank is not None and rank <= 10:
        return 'near_miss'
    if s2 >= HIGH_S2_THRESH:
        if top_ratio >= 2.0:
            return 'ambush'
        else:
            return 'fog'
    elif s2 <= -1.0:
        return 'compliance'
    else:
        return 'neutral'

def main():
    with open('results/corpus_results.json') as f:
        data = json.load(f)

    # Per-poem results
    poem_stats = []
    # Global category stats
    category_s2 = defaultdict(list)
    category_examples = defaultdict(list)

    # Top_ratio distribution at high-S2 moments
    high_s2_top_ratios = []

    # Poet profiles: {author: {category: count}}
    poet_profiles = defaultdict(lambda: defaultdict(int))
    poet_s2 = defaultdict(list)

    # Distribution shape vs S2
    shape_buckets = {
        'winner_take_all': [],   # top_ratio > 5
        'dominant':        [],   # 2 < top_ratio <= 5
        'competitive':     [],   # 1 < top_ratio <= 2
        'flat':            [],   # top_ratio <= 1
    }

    for poem in data:
        meta = poem['metadata']
        title = meta['title']
        author = meta.get('author', 'Unknown')
        era = meta.get('era', 'unknown')
        tokens = poem['tokens']

        ambush_count = fog_count = compliance_count = near_miss_count = 0
        poem_top_ratios_high = []

        for tok in tokens:
            if tok.get('p_newline', 0) >= ARTIFACT_FILTER:
                continue

            s2 = tok['s2']
            rank = tok.get('rank')
            alts = tok.get('alternatives', [])

            if len(alts) < 2:
                continue

            dist = classify_distribution(alts)
            if dist is None:
                continue

            top_ratio = dist['top_ratio']
            is_artifact = tok.get('p_newline', 0) >= ARTIFACT_FILTER
            cat = categorize_surprise(s2, top_ratio, rank, is_artifact)

            # Accumulate stats
            category_s2[cat].append(s2)
            poet_profiles[author][cat] += 1
            poet_s2[author].append(s2)

            if cat in ('ambush', 'fog'):
                high_s2_top_ratios.append(top_ratio)

            if cat == 'ambush':
                ambush_count += 1
                category_examples['ambush'].append({
                    'poem': title, 'author': author, 'era': era,
                    'token': tok['token'], 's2': s2,
                    'top_alt': alts[0]['token'], 'top_alt_prob': alts[0]['prob'],
                    'poet_prob': tok['prob'], 'top_ratio': top_ratio,
                    'rank': rank,
                })
            elif cat == 'fog':
                fog_count += 1
                category_examples['fog'].append({
                    'poem': title, 'author': author, 'era': era,
                    'token': tok['token'], 's2': s2,
                    'top_alt': alts[0]['token'], 'top_alt_prob': alts[0]['prob'],
                    'poet_prob': tok['prob'], 'top_ratio': top_ratio,
                    'rank': rank,
                })

            # Distribution shape bucket
            if top_ratio > 5:
                shape_buckets['winner_take_all'].append(s2)
            elif top_ratio > 2:
                shape_buckets['dominant'].append(s2)
            elif top_ratio > 1:
                shape_buckets['competitive'].append(s2)
            else:
                shape_buckets['flat'].append(s2)

        poem_stats.append({
            'title': title, 'author': author, 'era': era,
            'ambush': ambush_count, 'fog': fog_count,
            'compliance': compliance_count, 'near_miss': near_miss_count,
            'n_tokens': len([t for t in tokens if t.get('p_newline', 0) < ARTIFACT_FILTER]),
        })

    # Sort examples by s2 desc for reporting
    for cat in category_examples:
        category_examples[cat].sort(key=lambda x: -x['s2'])

    # Poet profile analysis
    poet_summary = []
    for author, profile in poet_profiles.items():
        total = sum(profile.values())
        if total < 20:
            continue
        ambush_rate = profile['ambush'] / total
        fog_rate = profile['fog'] / total
        near_miss_rate = profile['near_miss'] / total
        mean_s2 = sum(poet_s2[author]) / len(poet_s2[author])
        poet_summary.append({
            'author': author, 'total': total,
            'ambush_rate': ambush_rate, 'fog_rate': fog_rate,
            'near_miss_rate': near_miss_rate, 'mean_s2': mean_s2,
            'ratio': ambush_rate / fog_rate if fog_rate > 0 else float('inf'),
        })
    poet_summary.sort(key=lambda x: -x['ambush_rate'])

    # Era analysis
    era_stats = defaultdict(lambda: {'ambush': [], 'fog': [], 'compliance': [], 's2': []})
    for poem in data:
        meta = poem['metadata']
        era = meta.get('era', 'unknown')
        tokens = poem['tokens']
        for tok in tokens:
            if tok.get('p_newline', 0) >= ARTIFACT_FILTER:
                continue
            alts = tok.get('alternatives', [])
            if len(alts) < 2:
                continue
            s2 = tok['s2']
            rank = tok.get('rank')
            dist = classify_distribution(alts)
            cat = categorize_surprise(s2, dist['top_ratio'], rank, False)
            era_stats[era]['s2'].append(s2)
            if cat in ('ambush', 'fog', 'compliance'):
                era_stats[era][cat].append(s2)

    era_summary = []
    for era, stats in era_stats.items():
        total = len(stats['s2'])
        if total < 50:
            continue
        era_summary.append({
            'era': era, 'n': total,
            'ambush_rate': len(stats['ambush']) / total,
            'fog_rate': len(stats['fog']) / total,
            'ambush_mean_s2': sum(stats['ambush']) / len(stats['ambush']) if stats['ambush'] else 0,
            'fog_mean_s2': sum(stats['fog']) / len(stats['fog']) if stats['fog'] else 0,
            'overall_mean_s2': sum(stats['s2']) / total,
        })
    era_summary.sort(key=lambda x: -x['ambush_rate'])

    # Shape buckets summary
    shape_summary = {}
    for shape, s2s in shape_buckets.items():
        if s2s:
            shape_summary[shape] = {
                'n': len(s2s),
                'mean_s2': sum(s2s) / len(s2s),
                'pos_rate': sum(1 for x in s2s if x > 0) / len(s2s),
                'spike_rate': sum(1 for x in s2s if x >= 2.0) / len(s2s),
            }

    # Overall category stats
    cat_summary = {}
    for cat, s2s in category_s2.items():
        if cat == 'artifact':
            continue
        cat_summary[cat] = {
            'n': len(s2s),
            'mean_s2': sum(s2s) / len(s2s),
            'pos_rate': sum(1 for x in s2s if x > 0) / len(s2s),
        }

    results = {
        'category_summary': cat_summary,
        'shape_bucket_summary': shape_summary,
        'top_ambush_examples': category_examples['ambush'][:30],
        'top_fog_examples': category_examples['fog'][:30],
        'poet_profiles': poet_summary[:30],
        'era_summary': era_summary,
    }

    with open('results/alternatives_architecture.json', 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    print("=== ALTERNATIVES ARCHITECTURE RESULTS ===\n")

    print("## Category Summary")
    for cat, stats in cat_summary.items():
        print(f"  {cat:15s}: n={stats['n']:5d}  mean_s2={stats['mean_s2']:+.3f}  pos_rate={stats['pos_rate']:.1%}")

    print("\n## Distribution Shape vs S2")
    for shape, stats in shape_summary.items():
        print(f"  {shape:20s}: n={stats['n']:5d}  mean_s2={stats['mean_s2']:+.3f}  spike_rate={stats['spike_rate']:.1%}")

    print("\n## Top Ambush Moments (high top_ratio, high S2)")
    for ex in category_examples['ambush'][:10]:
        suppression = ex['top_alt_prob'] / ex['poet_prob'] if ex['poet_prob'] > 0 else 0
        print(f"  [{ex['author']}] '{ex['token']}' (S2={ex['s2']:.2f}) "
              f"suppressed '{ex['top_alt']}' ({suppression:.0f}x more likely, top_ratio={ex['top_ratio']:.2f})")

    print("\n## Top Poet Ambush Rates (prefer confident-prediction-defiance)")
    for p in poet_summary[:15]:
        print(f"  {p['author'][:30]:30s}: ambush={p['ambush_rate']:.1%}  fog={p['fog_rate']:.1%}  "
              f"ratio={p['ratio']:.2f}  mean_s2={p['mean_s2']:+.3f}")

    print("\n## Era Analysis (top by ambush rate)")
    for e in era_summary[:12]:
        print(f"  {e['era']:25s}: ambush={e['ambush_rate']:.1%}  fog={e['fog_rate']:.1%}  n={e['n']}")

    print("\nResults saved to results/alternatives_architecture.json")

if __name__ == '__main__':
    main()
