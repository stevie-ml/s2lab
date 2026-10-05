"""
S2 Volatility as Style Signature
=================================
Research question: Do poets differ not just in mean S2 but in how *volatile*
their surprises are? We classify poets on a 2D style space:
  - mean S2   (x-axis): systematic bias toward / away from expectation
  - std_s2    (y-axis): consistency of that deviation

Quadrants:
  Q1 high mean, high std:  "Strategic Saboteurs" — occasional explosions of surprise
  Q2 high mean, low std:   "Systematic Innovators" — consistently above expectation
  Q3 low mean, high std:   "Volatile Conformists"  — mostly conventional, wild outliers
  Q4 low mean, low std:    "Predictable Traditionalists" — stable, expected language

Additional: skewness of S2 distribution per poem (heavy right tail = rare but extreme spikes)
"""

import json
import os
import sys
import math
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'results', 'corpus_results.json')


def skewness(values):
    """Fisher–Pearson skewness."""
    n = len(values)
    if n < 3:
        return float('nan')
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    if variance == 0:
        return 0.0
    std = math.sqrt(variance)
    return (sum((v - mean) ** 3 for v in values) / n) / (std ** 3)


def kurtosis(values):
    """Excess kurtosis (Fisher definition, normal=0)."""
    n = len(values)
    if n < 4:
        return float('nan')
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / n
    if variance == 0:
        return 0.0
    kurt = (sum((v - mean) ** 4 for v in values) / n) / (variance ** 2)
    return kurt - 3.0  # excess kurtosis


def p90_s2(values):
    """90th percentile S2 (captures the spikes without being pulled by outliers)."""
    if not values:
        return float('nan')
    sorted_v = sorted(values)
    idx = int(0.9 * len(sorted_v))
    return sorted_v[min(idx, len(sorted_v) - 1)]


def load_results():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def run():
    data = load_results()

    # Per-poem statistics
    poem_stats = []
    for entry in data:
        meta = entry['metadata']
        tokens = entry.get('tokens', [])
        if not tokens:
            continue

        # Filter stanza-break artifacts (p_newline > 0.9)
        clean_s2 = [t['s2'] for t in tokens if t.get('p_newline', 0) < 0.9]
        raw_s2 = [t['s2'] for t in tokens]

        if len(clean_s2) < 5:
            continue

        mean = sum(clean_s2) / len(clean_s2)
        variance = sum((v - mean) ** 2 for v in clean_s2) / len(clean_s2)
        std = math.sqrt(variance)

        poem_stats.append({
            'title': meta['title'],
            'author': meta['author'],
            'era': meta.get('era', 'unknown'),
            'year': meta.get('year', 0),
            'n_tokens': len(clean_s2),
            'mean_s2': mean,
            'std_s2': std,
            'skewness': skewness(clean_s2),
            'kurtosis': kurtosis(clean_s2),
            'p90_s2': p90_s2(clean_s2),
            'pos_ratio': sum(1 for v in clean_s2 if v > 0) / len(clean_s2),
        })

    # ── Per-poet aggregates ──────────────────────────────────────────────
    poet_data = defaultdict(list)
    for p in poem_stats:
        poet_data[p['author']].append(p)

    poet_summary = []
    for author, poems in poet_data.items():
        if len(poems) < 2:
            continue
        means = [p['mean_s2'] for p in poems]
        stds = [p['std_s2'] for p in poems]
        skews = [p['skewness'] for p in poems if not math.isnan(p['skewness'])]
        p90s = [p['p90_s2'] for p in poems]
        poet_summary.append({
            'author': author,
            'era': poems[0]['era'],
            'n_poems': len(poems),
            'avg_mean_s2': sum(means) / len(means),
            'avg_std_s2': sum(stds) / len(stds),
            'avg_skewness': sum(skews) / len(skews) if skews else float('nan'),
            'avg_p90_s2': sum(p90s) / len(p90s),
            'mean_s2_range': max(means) - min(means),  # how much the poet varies across poems
        })

    poet_summary.sort(key=lambda x: x['avg_mean_s2'], reverse=True)

    # ── Per-era volatility ───────────────────────────────────────────────
    era_data = defaultdict(list)
    for p in poem_stats:
        era_data[p['era']].append(p)

    era_summary = []
    for era, poems in era_data.items():
        if len(poems) < 2:
            continue
        stds = [p['std_s2'] for p in poems]
        means = [p['mean_s2'] for p in poems]
        skews = [p['skewness'] for p in poems if not math.isnan(p['skewness'])]
        era_summary.append({
            'era': era,
            'n': len(poems),
            'avg_mean_s2': sum(means) / len(means),
            'avg_std_s2': sum(stds) / len(stds),
            'avg_skewness': sum(skews) / len(skews) if skews else float('nan'),
            'cv': (sum(stds) / len(stds)) / abs(sum(means) / len(means)) if sum(means) != 0 else float('nan'),
        })
    era_summary.sort(key=lambda x: x['avg_std_s2'], reverse=True)

    # ── Most extreme single poems ────────────────────────────────────────
    most_volatile = sorted(poem_stats, key=lambda x: x['std_s2'], reverse=True)[:10]
    least_volatile = sorted(poem_stats, key=lambda x: x['std_s2'])[:10]
    high_skew = sorted([p for p in poem_stats if not math.isnan(p['skewness'])],
                       key=lambda x: x['skewness'], reverse=True)[:10]

    # ── Quadrant classification ──────────────────────────────────────────
    # Compute corpus-wide median mean_s2 and median std_s2
    all_means = sorted(p['mean_s2'] for p in poem_stats)
    all_stds = sorted(p['std_s2'] for p in poem_stats)
    med_mean = all_means[len(all_means) // 2]
    med_std = all_stds[len(all_stds) // 2]

    quadrants = {'strategic_saboteur': [], 'systematic_innovator': [],
                 'volatile_conformist': [], 'predictable_traditionalist': []}
    for p in poem_stats:
        high_mean = p['mean_s2'] >= med_mean
        high_std = p['std_s2'] >= med_std
        if high_mean and high_std:
            quadrants['strategic_saboteur'].append(p)
        elif high_mean and not high_std:
            quadrants['systematic_innovator'].append(p)
        elif not high_mean and high_std:
            quadrants['volatile_conformist'].append(p)
        else:
            quadrants['predictable_traditionalist'].append(p)

    results = {
        'med_mean_s2': med_mean,
        'med_std_s2': med_std,
        'poet_summary': poet_summary,
        'era_summary': era_summary,
        'high_std_poems': most_volatile,
        'low_std_poems': least_volatile,
        'high_skew_poems': high_skew,
        'quadrants': {k: len(v) for k, v in quadrants.items()},
        'quadrant_era_breakdown': {
            k: list({p['era'] for p in v})[:5]
            for k, v in quadrants.items()
        },
        'quadrant_examples': {
            k: [{'title': p['title'], 'author': p['author']} for p in v[:5]]
            for k, v in quadrants.items()
        },
    }

    out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 's2_volatility.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)

    return results


if __name__ == '__main__':
    r = run()
    print(f"Median mean_s2: {r['med_mean_s2']:.3f}")
    print(f"Median std_s2:  {r['med_std_s2']:.3f}")
    print("\nQuadrant counts:")
    for k, v in r['quadrants'].items():
        print(f"  {k}: {v}")
    print("\nTop poets by avg mean_s2 (>=2 poems):")
    for p in r['poet_summary'][:10]:
        print(f"  {p['author']}: mean={p['avg_mean_s2']:.3f} std={p['avg_std_s2']:.3f} skew={p['avg_skewness']:.2f} n={p['n_poems']}")
    print("\nEras by avg std_s2:")
    for e in r['era_summary'][:10]:
        print(f"  {e['era']}: mean={e['avg_mean_s2']:.3f} std={e['avg_std_s2']:.3f} skew={e['avg_skewness']:.2f} n={e['n']}")
    print("\nHighest std_s2 poems (most volatile):")
    for p in r['high_std_poems'][:8]:
        print(f"  {p['std_s2']:.3f}  {p['title']} ({p['author']})")
    print("\nLowest std_s2 poems (most consistent):")
    for p in r['low_std_poems'][:8]:
        print(f"  {p['std_s2']:.3f}  {p['title']} ({p['author']})")
    print("\nHighest skewness poems:")
    for p in r['high_skew_poems'][:8]:
        print(f"  {p['skewness']:.3f}  {p['title']} ({p['author']})")
