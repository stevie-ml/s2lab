"""
Poet Strategy Fingerprint: Is information-theoretic strategy a stable poet property?

entropy_variance_trap_release.md found that poems cluster into 4 quadrants:
  - Consistent Ambush (high S2, stable H)
  - Trap-Release (high S2, variable H)
  - Erratic Conformist (low S2, variable H)
  - Metronomic (low S2, stable H)

Question: Is a poet's quadrant a stable property across their body of work,
or does it vary poem-by-poem? Can we build a "strategy fingerprint" per poet?
"""

import json
import statistics
import math
from collections import defaultdict

ARTIFACT_THRESHOLD = 0.9

def get_clean_tokens(poem):
    return [t for t in poem['tokens'] if t.get('p_newline', 0) < ARTIFACT_THRESHOLD]

def poem_strategy_metrics(poem):
    tokens = get_clean_tokens(poem)
    if len(tokens) < 15:
        return None

    s2_vals = [t['s2'] for t in tokens]
    h_vals = [t['entropy'] for t in tokens]

    mean_s2 = statistics.mean(s2_vals)
    std_h = statistics.stdev(h_vals) if len(h_vals) > 1 else 0.0
    median_h = statistics.median(h_vals)

    # Trap ratio: of high-S2 tokens, what fraction follow a low-entropy token?
    high_s2_tokens = [tokens[i] for i in range(1, len(tokens)) if tokens[i]['s2'] > 2.0]
    trap_count = sum(
        1 for i in range(1, len(tokens))
        if tokens[i]['s2'] > 2.0 and tokens[i-1]['entropy'] < median_h
    )
    trap_ratio = trap_count / len(high_s2_tokens) if high_s2_tokens else float('nan')

    return {
        'mean_s2': mean_s2,
        'std_h': std_h,
        'trap_ratio': trap_ratio,
        'n_tokens': len(tokens),
        'n_high_s2': len(high_s2_tokens),
    }

def quadrant(mean_s2, std_h, s2_median, h_median):
    if mean_s2 >= s2_median and std_h < h_median:
        return 'Consistent_Ambush'
    elif mean_s2 >= s2_median and std_h >= h_median:
        return 'Trap_Release'
    elif mean_s2 < s2_median and std_h >= h_median:
        return 'Erratic_Conformist'
    else:
        return 'Metronomic'

def main():
    with open('results/corpus_results.json') as f:
        all_results = json.load(f)

    # Only English poems, exclude control
    poems = [r for r in all_results
             if r['metadata'].get('era') != 'control'
             and r['metadata'].get('language', 'en') == 'en']

    # Compute per-poem metrics
    poem_metrics = []
    for poem in poems:
        m = poem_strategy_metrics(poem)
        if m is None:
            continue
        m['title'] = poem['metadata']['title']
        m['author'] = poem['metadata']['author']
        m['era'] = poem['metadata']['era']
        m['year'] = poem['metadata'].get('year', 0)
        poem_metrics.append(m)

    all_s2 = [m['mean_s2'] for m in poem_metrics]
    all_h = [m['std_h'] for m in poem_metrics]
    s2_median = statistics.median(all_s2)
    h_median = statistics.median(all_h)

    for m in poem_metrics:
        m['quadrant'] = quadrant(m['mean_s2'], m['std_h'], s2_median, h_median)

    # Group by author
    by_author = defaultdict(list)
    for m in poem_metrics:
        by_author[m['author']].append(m)

    # Only analyze poets with >= 3 poems
    multi_poem_poets = {a: ms for a, ms in by_author.items() if len(ms) >= 3}

    print(f"Total poems analyzed: {len(poem_metrics)}")
    print(f"Poets with ≥3 poems: {len(multi_poem_poets)}")
    print(f"Global S2 median: {s2_median:.3f}")
    print(f"Global std_H median: {h_median:.3f}")
    print()

    # Compute per-poet strategy consistency
    poet_profiles = []
    for author, ms in sorted(multi_poem_poets.items(), key=lambda x: -len(x[1])):
        s2s = [m['mean_s2'] for m in ms]
        hs = [m['std_h'] for m in ms]
        traps = [m['trap_ratio'] for m in ms if not math.isnan(m['trap_ratio'])]
        quads = [m['quadrant'] for m in ms]

        dominant_q = max(set(quads), key=quads.count)
        consistency = quads.count(dominant_q) / len(quads)

        mean_s2 = statistics.mean(s2s)
        mean_h = statistics.mean(hs)
        s2_cv = statistics.stdev(s2s) / abs(mean_s2) if len(s2s) > 1 and mean_s2 != 0 else float('inf')

        poet_profiles.append({
            'author': author,
            'n_poems': len(ms),
            'era': ms[0]['era'],
            'dominant_quadrant': dominant_q,
            'consistency': consistency,
            'mean_s2': mean_s2,
            'mean_std_h': statistics.mean(hs),
            'mean_trap_ratio': statistics.mean(traps) if traps else float('nan'),
            's2_range': max(s2s) - min(s2s),
            'poems': [(m['title'], m['quadrant'], round(m['mean_s2'], 3), round(m['std_h'], 3)) for m in ms],
        })

    # Sort by consistency (most consistent first)
    poet_profiles.sort(key=lambda x: -x['consistency'])

    print("=" * 70)
    print("POET STRATEGY FINGERPRINTS (sorted by consistency)")
    print("=" * 70)
    for p in poet_profiles:
        print(f"\n{p['author']} (n={p['n_poems']}, era={p['era']})")
        print(f"  Dominant quadrant: {p['dominant_quadrant']} ({p['consistency']:.0%} consistent)")
        print(f"  Mean S2={p['mean_s2']:.3f}, Mean std_H={p['mean_std_h']:.3f}, "
              f"Trap_ratio={p['mean_trap_ratio']:.2f}"
              if not math.isnan(p['mean_trap_ratio']) else
              f"  Mean S2={p['mean_s2']:.3f}, Mean std_H={p['mean_std_h']:.3f}")
        for title, q, s2, h in p['poems']:
            marker = "*" if q == p['dominant_quadrant'] else " "
            print(f"  {marker} [{q:22s}] S2={s2:+.3f} stdH={h:.3f}  \"{title[:50]}\"")

    # Summary statistics
    consistencies = [p['consistency'] for p in poet_profiles]
    print("\n" + "=" * 70)
    print("CONSISTENCY DISTRIBUTION")
    print("=" * 70)
    thresholds = [1.0, 0.75, 0.5]
    for t in thresholds:
        count = sum(1 for c in consistencies if c >= t)
        print(f"  Consistency ≥ {t:.0%}: {count}/{len(consistencies)} poets ({count/len(consistencies):.0%})")

    # Quadrant distribution per era
    print("\n" + "=" * 70)
    print("DOMINANT QUADRANT BY ERA")
    print("=" * 70)
    era_quads = defaultdict(list)
    for m in poem_metrics:
        era_quads[m['era']].append(m['quadrant'])

    era_summary = []
    for era, qs in sorted(era_quads.items(), key=lambda x: -len(x[1])):
        if len(qs) < 3:
            continue
        q_counts = {q: qs.count(q) for q in set(qs)}
        dominant = max(q_counts, key=q_counts.get)
        dom_pct = q_counts[dominant] / len(qs)
        era_summary.append((era, len(qs), dominant, dom_pct, q_counts))

    print(f"{'Era':<25} {'n':>4}  {'Dominant Quadrant':<25} {'%':>5}  Distribution")
    for era, n, dom, pct, counts in sorted(era_summary, key=lambda x: -x[3]):
        dist = " | ".join(f"{q[:2]}={counts.get(q,0)}" for q in
                         ['Consistent_Ambush','Trap_Release','Erratic_Conformist','Metronomic'])
        print(f"{era:<25} {n:>4}  {dom:<25} {pct:>4.0%}   {dist}")

    # Save results
    output = {
        'global_medians': {'s2': s2_median, 'std_h': h_median},
        'n_poems_analyzed': len(poem_metrics),
        'n_multi_poem_poets': len(multi_poem_poets),
        'poet_profiles': [{
            'author': p['author'],
            'n_poems': p['n_poems'],
            'era': p['era'],
            'dominant_quadrant': p['dominant_quadrant'],
            'consistency': round(p['consistency'], 3),
            'mean_s2': round(p['mean_s2'], 3),
            'mean_std_h': round(p['mean_std_h'], 3),
            'mean_trap_ratio': round(p['mean_trap_ratio'], 3) if not math.isnan(p['mean_trap_ratio']) else None,
            's2_range': round(p['s2_range'], 3),
        } for p in poet_profiles],
        'era_dominance': {era: {'n': n, 'dominant': dom, 'pct': round(pct, 3), 'counts': counts}
                          for era, n, dom, pct, counts in era_summary},
    }
    with open('results/poet_strategy_fingerprint.json', 'w') as f:
        json.dump(output, f, indent=2)
    print("\nSaved to results/poet_strategy_fingerprint.json")

if __name__ == '__main__':
    main()
