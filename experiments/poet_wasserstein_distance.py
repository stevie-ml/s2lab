"""
Pairwise S2 Distribution Similarity Between Poets
Using Wasserstein distance to measure informational closeness between poets.

Research question: which poets are informationally most alike / most different?
Does poetic family resemblance show up in the distribution of S2 values?

Builds on: poet_fingerprint_consistency.md, s2_volatility_signature.md
New angle: pairwise distance matrix (not just per-poet summary stats)
"""

import json
import numpy as np
from scipy.stats import wasserstein_distance
from collections import defaultdict
import os

RESULTS_PATH = os.path.join(os.path.dirname(__file__), '..', 'results', 'corpus_results.json')
FINDINGS_PATH = os.path.join(os.path.dirname(__file__), '..', 'findings', 'poet_wasserstein_distance.md')

# Load corpus
with open(RESULTS_PATH) as f:
    corpus = json.load(f)

# Collect clean S2 values per poet (exclude newline-artifact tokens)
poet_s2 = defaultdict(list)
poet_poems = defaultdict(set)
poet_era = {}

for poem in corpus:
    author = poem['metadata'].get('author', 'Unknown')
    era = poem['metadata'].get('era', 'unknown')
    title = poem['metadata'].get('title', '')
    poet_era[author] = era
    poet_poems[author].add(title)

    for tok in poem['tokens']:
        # Exclude stanza-break artifact tokens
        if tok.get('p_newline', 0) >= 0.9:
            continue
        s2 = tok['s2']
        if not (np.isnan(s2) or np.isinf(s2)):
            poet_s2[author].append(s2)

# Filter to poets with at least 50 clean tokens (enough distribution data)
MIN_TOKENS = 50
qualified = {p: np.array(v) for p, v in poet_s2.items() if len(v) >= MIN_TOKENS}

print(f"Qualified poets (≥{MIN_TOKENS} clean tokens): {len(qualified)}")

# Summary stats per poet
poet_stats = {}
for poet, vals in qualified.items():
    poet_stats[poet] = {
        'n_tokens': len(vals),
        'n_poems': len(poet_poems[poet]),
        'mean': float(np.mean(vals)),
        'median': float(np.median(vals)),
        'std': float(np.std(vals)),
        'skewness': float(np.mean(((vals - np.mean(vals)) / (np.std(vals) + 1e-9))**3)),
        'era': poet_era.get(poet, 'unknown'),
    }

# Compute pairwise Wasserstein distances
poets = sorted(qualified.keys())
n = len(poets)
dist_matrix = np.zeros((n, n))

print(f"\nComputing {n*(n-1)//2} pairwise distances...")
for i in range(n):
    for j in range(i+1, n):
        d = wasserstein_distance(qualified[poets[i]], qualified[poets[j]])
        dist_matrix[i, j] = d
        dist_matrix[j, i] = d

# Find most similar pairs (lowest Wasserstein distance, excluding self)
pairs = []
for i in range(n):
    for j in range(i+1, n):
        pairs.append((dist_matrix[i, j], poets[i], poets[j]))
pairs.sort()

print("\n=== Most Similar Poet Pairs (lowest Wasserstein distance) ===")
for d, p1, p2 in pairs[:15]:
    print(f"  {d:.3f}  {p1} <-> {p2}")

print("\n=== Most Different Poet Pairs (highest Wasserstein distance) ===")
for d, p1, p2 in pairs[-10:]:
    print(f"  {d:.3f}  {p1} <-> {p2}")

# For each poet, find their nearest and farthest neighbor
print("\n=== Each poet's nearest neighbor ===")
nearest = {}
for i, poet in enumerate(poets):
    row = dist_matrix[i].copy()
    row[i] = np.inf
    j = np.argmin(row)
    nearest[poet] = (poets[j], row[j])

# Sort by mean S2 to show the spectrum
sorted_poets = sorted(poet_stats.keys(), key=lambda p: poet_stats[p]['mean'], reverse=True)
for poet in sorted_poets[:25]:
    nbr, d = nearest.get(poet, ('?', float('inf')))
    stats = poet_stats[poet]
    print(f"  {poet[:35]:35s} mean={stats['mean']:+.3f} skew={stats['skewness']:+.2f} -> nearest: {nbr[:30]:30s} (d={d:.3f})")

# Check if era correlates with distance: compute mean intra-era vs inter-era distance
era_poets = defaultdict(list)
for i, poet in enumerate(poets):
    era = poet_stats[poet]['era']
    era_poets[era].append(i)

intra = []
inter = []
for era, idxs in era_poets.items():
    if len(idxs) < 2:
        continue
    for ii in range(len(idxs)):
        for jj in range(ii+1, len(idxs)):
            intra.append(dist_matrix[idxs[ii], idxs[jj]])

# Sample inter-era distances
for i in range(n):
    for j in range(i+1, n):
        if poet_stats[poets[i]]['era'] != poet_stats[poets[j]]['era']:
            inter.append(dist_matrix[i, j])

print(f"\n=== Era clustering ===")
print(f"Mean intra-era Wasserstein distance: {np.mean(intra):.3f} ± {np.std(intra):.3f} (n={len(intra)})")
print(f"Mean inter-era Wasserstein distance: {np.mean(inter):.3f} ± {np.std(inter):.3f} (n={len(inter)})")
if len(intra) > 0:
    print(f"Ratio intra/inter: {np.mean(intra)/np.mean(inter):.3f}")

# Identify era groups with notable clustering
print("\n=== Intra-era distances by era (eras with 2+ qualified poets) ===")
era_intra = defaultdict(list)
for era, idxs in era_poets.items():
    if len(idxs) < 2:
        continue
    for ii in range(len(idxs)):
        for jj in range(ii+1, len(idxs)):
            era_intra[era].append(dist_matrix[idxs[ii], idxs[jj]])

for era, dists in sorted(era_intra.items(), key=lambda x: np.mean(x[1])):
    members = [poets[i] for i in era_poets[era]]
    print(f"  {era:25s}  mean_d={np.mean(dists):.3f}  n_poets={len(members)}  poets={', '.join(m[:15] for m in members[:5])}")

# Save results
results = {
    'poets': poets,
    'poet_stats': poet_stats,
    'distance_matrix': dist_matrix.tolist(),
    'most_similar_pairs': [(d, p1, p2) for d, p1, p2 in pairs[:20]],
    'most_different_pairs': [(d, p1, p2) for d, p1, p2 in pairs[-10:]],
    'intra_era_mean': float(np.mean(intra)) if intra else None,
    'inter_era_mean': float(np.mean(inter)) if inter else None,
    'era_intra_distances': {e: {'mean': float(np.mean(d)), 'n': len(d)} for e, d in era_intra.items()},
}

import json
out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'poet_wasserstein_distance.json')
with open(out_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to {out_path}")
