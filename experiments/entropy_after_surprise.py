"""
Entropy After Surprise: Does a high-S2 choice expand or collapse the space of what can follow?

When a poet deviates from GPT-2's predictions (high S2), does the model become:
  (A) MORE uncertain about the next token (liberation: the unexpected word opens new paths)
  (B) LESS uncertain about the next token (anchoring: the unexpected word creates new strong context)

We test this by computing, for each consecutive token pair (t, t+1):
  - S2 at position t (how surprising was the choice?)
  - entropy at position t+1 (how uncertain is GPT-2 about what follows?)

A positive correlation (high S2 → high entropy_next) = Liberation hypothesis
A negative correlation (high S2 → low entropy_next) = Anchoring hypothesis
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/entropy_after_surprise.json"

S2_BINS = [
    ("very_negative", float('-inf'), -3.0),
    ("negative",      -3.0,          0.0),
    ("low_positive",   0.0,           2.0),
    ("mid_positive",   2.0,           5.0),
    ("high_positive",  5.0,          10.0),
    ("extreme",       10.0,          float('inf')),
]

def bin_s2(s2_val):
    for name, lo, hi in S2_BINS:
        if lo <= s2_val < hi:
            return name
    return "extreme"

def is_artifact(tok):
    """Filter stanza-break newline artifact tokens."""
    return tok.get('p_newline', 0) > 0.9

def pearson_r(xs, ys):
    if len(xs) < 3:
        return None
    n = len(xs)
    mx, my = sum(xs)/n, sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    if dx * dy == 0:
        return None
    return num / (dx * dy)

def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} texts")

    # Per-bin accumulators: (entropy_next) values
    bin_entropy_next = defaultdict(list)
    # Per-bin: (s2_next) values
    bin_s2_next = defaultdict(list)
    # Raw pairs for correlation
    all_s2_t = []
    all_entropy_t1 = []
    all_s2_t1 = []

    # Per-poem: (first_half_s2, second_half_s2) for conservation test
    poem_halves = []

    # Entropy at position t vs entropy at t+1: "entropy persistence"
    entropy_same = []   # pairs where both tokens are non-artifact
    bin_entropy_now = defaultdict(list)  # for entropy(t) → s2(t) check

    texts_used = 0

    for text in corpus:
        meta = text.get('metadata', {})
        era = meta.get('era', 'unknown')
        tokens = text.get('tokens', [])

        # Filter out artifacts and very short texts
        clean = [t for t in tokens if not is_artifact(t)]
        if len(clean) < 10:
            continue

        texts_used += 1

        # First/second half for conservation
        mid = len(clean) // 2
        first_half_s2 = [t['s2'] for t in clean[:mid]]
        second_half_s2 = [t['s2'] for t in clean[mid:]]
        if first_half_s2 and second_half_s2:
            poem_halves.append((
                sum(first_half_s2)/len(first_half_s2),
                sum(second_half_s2)/len(second_half_s2),
                meta.get('title',''),
                era
            ))

        # Consecutive pair analysis
        for i in range(len(clean) - 1):
            t0 = clean[i]
            t1 = clean[i+1]

            s2_t  = t0['s2']
            ent_t  = t0['entropy']
            s2_t1 = t1['s2']
            ent_t1 = t1['entropy']

            b = bin_s2(s2_t)
            bin_entropy_next[b].append(ent_t1)
            bin_s2_next[b].append(s2_t1)
            bin_entropy_now[b].append(ent_t)

            all_s2_t.append(s2_t)
            all_entropy_t1.append(ent_t1)
            all_s2_t1.append(s2_t1)
            entropy_same.append((ent_t, ent_t1))

    print(f"Used {texts_used} texts, {len(all_s2_t)} consecutive pairs")

    # Compute bin statistics
    results_by_bin = {}
    for name, lo, hi in S2_BINS:
        entropies = bin_entropy_next[name]
        s2nexts = bin_s2_next[name]
        ent_nows = bin_entropy_now[name]
        if not entropies:
            continue
        results_by_bin[name] = {
            'n': len(entropies),
            's2_range': [lo, hi],
            'mean_entropy_next': round(sum(entropies)/len(entropies), 4),
            'median_entropy_next': round(statistics.median(entropies), 4),
            'mean_s2_next': round(sum(s2nexts)/len(s2nexts), 4),
            'mean_entropy_now': round(sum(ent_nows)/len(ent_nows), 4),
        }

    # Overall correlations
    r_s2_entropy = pearson_r(all_s2_t, all_entropy_t1)
    r_s2_s2next = pearson_r(all_s2_t, all_s2_t1)
    r_ent_entnext = pearson_r(
        [p[0] for p in entropy_same],
        [p[1] for p in entropy_same]
    )

    # Conservation test: do first-half and second-half S2 negatively correlate?
    half_r = pearson_r(
        [p[0] for p in poem_halves],
        [p[1] for p in poem_halves]
    )

    # Find poems with largest S2 asymmetry (front-loaded vs back-loaded)
    poem_halves_sorted = sorted(poem_halves, key=lambda x: x[1]-x[0])
    back_loaded = poem_halves_sorted[-10:]
    front_loaded = poem_halves_sorted[:10]

    # Era-level analysis: do different eras show different entropy cascade patterns?
    era_pairs = defaultdict(list)
    for text in corpus:
        meta = text.get('metadata', {})
        era = meta.get('era', 'unknown')
        tokens = text.get('tokens', [])
        clean = [t for t in tokens if not is_artifact(t)]
        for i in range(len(clean)-1):
            t0, t1 = clean[i], clean[i+1]
            era_pairs[era].append((t0['s2'], t1['entropy'], t1['s2']))

    era_results = {}
    for era, pairs in era_pairs.items():
        if len(pairs) < 30:
            continue
        s2s = [p[0] for p in pairs]
        ents = [p[1] for p in pairs]
        s2nexts = [p[2] for p in pairs]
        r = pearson_r(s2s, ents)
        era_results[era] = {
            'n': len(pairs),
            'r_s2_entropy_next': round(r, 4) if r else None,
            'mean_s2': round(sum(s2s)/len(s2s), 4),
            'mean_entropy_next': round(sum(ents)/len(ents), 4),
        }

    output = {
        'n_texts': texts_used,
        'n_pairs': len(all_s2_t),
        'bins': results_by_bin,
        'correlations': {
            'r_s2_entropy_next': round(r_s2_entropy, 4) if r_s2_entropy else None,
            'r_s2_s2_next': round(r_s2_s2next, 4) if r_s2_s2next else None,
            'r_entropy_entropy_next': round(r_ent_entnext, 4) if r_ent_entnext else None,
        },
        'conservation': {
            'r_first_second_half': round(half_r, 4) if half_r else None,
            'n_poems': len(poem_halves),
            'back_loaded_examples': [
                {'title': p[2], 'era': p[3],
                 'first_half_s2': round(p[0],3), 'second_half_s2': round(p[1],3),
                 'asymmetry': round(p[1]-p[0],3)}
                for p in back_loaded
            ],
            'front_loaded_examples': [
                {'title': p[2], 'era': p[3],
                 'first_half_s2': round(p[0],3), 'second_half_s2': round(p[1],3),
                 'asymmetry': round(p[1]-p[0],3)}
                for p in front_loaded
            ],
        },
        'era_results': era_results,
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"Saved to {OUTPUT_PATH}")

    # Print key findings
    print("\n=== ENTROPY AFTER SURPRISE ===")
    print(f"\nCorrelations:")
    print(f"  S2(t) vs Entropy(t+1):  r = {r_s2_entropy:.4f}" if r_s2_entropy else "  r = N/A")
    print(f"  S2(t) vs S2(t+1):       r = {r_s2_s2next:.4f}" if r_s2_s2next else "  r = N/A")
    print(f"  Entropy(t) vs Entropy(t+1): r = {r_ent_entnext:.4f}" if r_ent_entnext else "  r = N/A")
    print(f"\nBin Analysis (S2 at t → mean Entropy at t+1):")
    print(f"{'Bin':<18} {'N':>6} {'MeanEnt(t+1)':>14} {'MeanS2(t+1)':>13}")
    for name, lo, hi in S2_BINS:
        if name in results_by_bin:
            r = results_by_bin[name]
            print(f"  {name:<16} {r['n']:>6} {r['mean_entropy_next']:>14.4f} {r['mean_s2_next']:>13.4f}")
    print(f"\nFirst vs Second Half S2 correlation: r = {half_r:.4f}" if half_r else "")

if __name__ == '__main__':
    main()
