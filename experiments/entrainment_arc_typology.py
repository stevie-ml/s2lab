"""
Entrainment Arc Typology: Does GPT-2 'learn' poem style as it reads?

Research question: As a poem progresses, does GPT-2's prediction field (entropy)
narrow — indicating the model is 'entraining' to the poem's style? And when the
model entrains, does the poet also become more conformist (entropy and S2 both
drop) or do they maintain their deviance ('defiant crystallization')?

This distinguishes two key arc types:
  Type A: Entrainment Convergence (H↓, S2↓) — model and poet both settle
  Type B: Defiant Crystallization (H↓, S2↑) — model learns, poet keeps defying
  Type C: Escalating Tension (H↑, S2↑) — both become more uncertain/surprising
  Type D: Settling into Chaos (H↑, S2↓) — context becomes unpredictable, poet follows

Also analyzes: where in a poem does the maximum S2 spike occur?
"""

import json, math, statistics
from collections import defaultdict

with open('results/corpus_results.json') as f:
    data = json.load(f)

# === STEP 1: Global quartile analysis ===
quartile_stats = defaultdict(lambda: {'entropy': [], 's2': [], 'top1_prob': []})

for poem in data:
    tokens = [t for t in poem['tokens'] if t.get('p_newline', 0) < 0.9]
    n = len(tokens)
    if n < 10:
        continue
    for i, t in enumerate(tokens):
        q = min(int((i / n) * 4), 3)
        quartile_stats[q]['entropy'].append(t['entropy'])
        quartile_stats[q]['s2'].append(t['s2'])
        if t.get('alternatives'):
            quartile_stats[q]['top1_prob'].append(t['alternatives'][0]['prob'])

print("=== Global Quartile Analysis ===")
qnames = ['Q1 (0-25%)', 'Q2 (25-50%)', 'Q3 (50-75%)', 'Q4 (75-100%)']
for q in range(4):
    d = quartile_stats[q]
    n = len(d['entropy'])
    me = statistics.mean(d['entropy'])
    ms = statistics.mean(d['s2'])
    mp = statistics.mean(d['top1_prob']) if d['top1_prob'] else 0
    pos_ratio = sum(1 for x in d['s2'] if x > 0) / n
    print(f"{qnames[q]}: H={me:.3f}, S2={ms:.3f}, top1_prob={mp:.4f}, %pos_S2={pos_ratio:.1%}")

# === STEP 2: Per-poem arc classification ===
poem_arcs = []
for poem in data:
    tokens = [t for t in poem['tokens'] if t.get('p_newline', 0) < 0.9]
    n = len(tokens)
    if n < 20:
        continue
    cutoff = n // 4
    q1_H  = statistics.mean([t['entropy']   for t in tokens[:cutoff]])
    q4_H  = statistics.mean([t['entropy']   for t in tokens[3*cutoff:]])
    q1_S2 = statistics.mean([t['s2']        for t in tokens[:cutoff]])
    q4_S2 = statistics.mean([t['s2']        for t in tokens[3*cutoff:]])
    poem_arcs.append({
        'title':   poem['metadata'].get('title', '?'),
        'author':  poem['metadata'].get('author', '?'),
        'era':     poem['metadata'].get('era', '?'),
        'q1_H': q1_H, 'q4_H': q4_H, 'H_drop': q1_H - q4_H,
        'q1_S2': q1_S2, 'q4_S2': q4_S2, 'S2_drop': q1_S2 - q4_S2,
        'n': n,
    })

H_drops = [p['H_drop'] for p in poem_arcs]
S2_drops = [p['S2_drop'] for p in poem_arcs]
print(f"\nPoems analyzed: {len(poem_arcs)}")
print(f"Entropy drop Q1→Q4: mean={statistics.mean(H_drops):.3f}, "
      f"% poems dropping: {sum(d>0 for d in H_drops)/len(H_drops):.1%}")
print(f"S2 drop Q1→Q4: mean={statistics.mean(S2_drops):.3f}, "
      f"% poems dropping: {sum(d>0 for d in S2_drops)/len(S2_drops):.1%}")

typeA = [p for p in poem_arcs if p['H_drop'] > 0.3 and p['S2_drop'] > 0.3]
typeB = [p for p in poem_arcs if p['H_drop'] > 0.3 and p['S2_drop'] < -0.1]
typeC = [p for p in poem_arcs if p['H_drop'] < -0.3 and p['S2_drop'] < -0.3]
typeD = [p for p in poem_arcs if p['H_drop'] < -0.3 and p['S2_drop'] > 0.3]
print(f"\nType A (H↓, S2↓): {len(typeA)} ({len(typeA)/len(poem_arcs):.1%})")
print(f"Type B (H↓, S2↑): {len(typeB)} ({len(typeB)/len(poem_arcs):.1%})")
print(f"Type C (H↑, S2↑): {len(typeC)} ({len(typeC)/len(poem_arcs):.1%})")
print(f"Type D (H↑, S2↓): {len(typeD)} ({len(typeD)/len(poem_arcs):.1%})")

# === STEP 3: Max-S2-spike position ===
spike_positions = []
for poem in data:
    tokens = [t for t in poem['tokens'] if t.get('p_newline', 0) < 0.9]
    n = len(tokens)
    if n < 20:
        continue
    s2s = [t['s2'] for t in tokens]
    max_pos = s2s.index(max(s2s))
    spike_positions.append(max_pos / n)

print(f"\n=== Max S2 Spike Position ===")
print(f"Mean: {statistics.mean(spike_positions):.3f}, Median: {statistics.median(spike_positions):.3f}")
q_pcts = [
    sum(1 for r in spike_positions if r < 0.25),
    sum(1 for r in spike_positions if 0.25 <= r < 0.5),
    sum(1 for r in spike_positions if 0.5 <= r < 0.75),
    sum(1 for r in spike_positions if r >= 0.75),
]
for i, name in enumerate(qnames):
    print(f"  {name}: {q_pcts[i]/len(spike_positions):.1%}")

# === STEP 4: Era entrainment ranking ===
era_data = defaultdict(list)
for p in poem_arcs:
    era_data[p['era']].append(p['H_drop'])
print("\n=== Era Entrainment Ranking (mean entropy drop Q1→Q4) ===")
era_ranks = sorted(
    [(e, statistics.mean(d), len(d)) for e, d in era_data.items() if len(d) >= 3],
    key=lambda x: -x[1]
)
for era, mean_drop, n in era_ranks[:12]:
    print(f"  {era:<25} H_drop={mean_drop:.3f}  (n={n})")

# Save results
results = {
    'global_quartiles': {str(q): {
        'mean_entropy': statistics.mean(quartile_stats[q]['entropy']),
        'mean_s2': statistics.mean(quartile_stats[q]['s2']),
        'pct_positive_s2': sum(x > 0 for x in quartile_stats[q]['s2']) / len(quartile_stats[q]['s2']),
    } for q in range(4)},
    'entrainment': {
        'mean_H_drop': statistics.mean(H_drops),
        'pct_poems_H_drops': sum(d > 0 for d in H_drops) / len(H_drops),
        'mean_S2_drop': statistics.mean(S2_drops),
        'pct_poems_S2_drops': sum(d > 0 for d in S2_drops) / len(S2_drops),
    },
    'arc_types': {
        'typeA_n': len(typeA), 'typeA_pct': len(typeA)/len(poem_arcs),
        'typeB_n': len(typeB), 'typeB_pct': len(typeB)/len(poem_arcs),
        'typeC_n': len(typeC), 'typeC_pct': len(typeC)/len(poem_arcs),
        'typeD_n': len(typeD), 'typeD_pct': len(typeD)/len(poem_arcs),
    },
    'spike_position': {
        'mean': statistics.mean(spike_positions),
        'median': statistics.median(spike_positions),
        'q1_pct': q_pcts[0]/len(spike_positions),
        'q2_pct': q_pcts[1]/len(spike_positions),
        'q3_pct': q_pcts[2]/len(spike_positions),
        'q4_pct': q_pcts[3]/len(spike_positions),
    },
    'era_entrainment': {e: {'mean_H_drop': m, 'n': n} for e, m, n in era_ranks},
    'typeB_examples': [
        {'title': p['title'], 'author': p['author'], 'era': p['era'],
         'H_drop': round(p['H_drop'], 3), 'S2_change': round(-p['S2_drop'], 3)}
        for p in sorted(typeB, key=lambda p: p['S2_drop'])[:10]
    ],
    'typeC_examples': [
        {'title': p['title'], 'author': p['author'], 'era': p['era'],
         'H_rise': round(-p['H_drop'], 3), 'S2_rise': round(-p['S2_drop'], 3)}
        for p in sorted(typeC, key=lambda p: p['H_drop'])[:10]
    ],
}
import json as _json
with open('results/entrainment_arc_typology.json', 'w') as f:
    _json.dump(results, f, indent=2)
print("\nResults saved to results/entrainment_arc_typology.json")
