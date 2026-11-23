"""
Vocabulary Bubble Formation: How Fast Does GPT-2 Learn a Poem's Own Words?

As a poem progresses, GPT-2 may start predicting previously-used words
in the poem — forming a "lexical bubble." We measure:

  recapture_rate(position) = fraction of top-10 GPT-2 alternatives at that
                              position that are words already used in the poem.

A high recapture rate means GPT-2 has "learned" the poem's vocabulary and
now predicts it back. A low recapture rate means the poem constantly brings
in new words that GPT-2 never anticipated from the poem's context.

This is distinct from (but related to) alpha (prediction concentration):
- α measures HOW STEEP the distribution is
- recapture measures WHAT vocabulary GPT-2 is predicting

Hypothesis:
- Poems with refrain/anaphora will show high recapture early (GPT-2 quickly
  learns the repeated words)
- Whitman-style catalogs will show LOW recapture (the catalog never repeats)
- Villanelles and other fixed forms will show strong recapture as the refrain
  words become GPT-2's most-predicted options

New metric coined: "bubble formation index" = slope of recapture rate over
the poem's normalized position (0→1). Positive = GPT-2 increasingly predicts
the poem's own vocabulary; near-zero = poem maintains lexical novelty throughout.
"""

import json
import re
import math
import statistics
from collections import defaultdict


def normalize_token(token: str) -> str:
    """Strip leading space and lowercase for vocabulary comparison."""
    return token.strip().lower()


def compute_poem_bubble(tokens: list, min_vocab_at_position: int = 5) -> dict:
    """
    For a poem's token list, compute the vocabulary recapture rate
    at each position and other derived metrics.

    Returns a dict with:
      - decile_recapture: list of 10 avg recapture values (by poem decile)
      - decile_alpha: list of 10 avg alpha values
      - bubble_slope: linear slope of recapture over position
      - max_recapture: maximum recapture rate reached
      - final_recapture: recapture rate in last decile
      - vocab_size_trajectory: set sizes at each decile
    """
    # Filter artifact tokens
    clean = [t for t in tokens if t.get('p_newline', 1.0) < 0.9 and t.get('alternatives')]
    if len(clean) < 10:
        return None

    n = len(clean)
    seen_vocab = set()  # normalized tokens seen so far

    decile_recaptures = defaultdict(list)
    decile_alphas = defaultdict(list)
    decile_vocab_sizes = defaultdict(list)

    per_token_recapture = []

    for i, tok in enumerate(clean):
        # Current position as normalized fraction
        pos_frac = i / n
        decile = min(int(pos_frac * 10), 9)

        # Add this token to seen vocab BEFORE computing recapture
        # (we want to measure: when model is AT position i, how much of its
        # top-10 predictions are words ALREADY SEEN before position i)
        norm_actual = normalize_token(tok['token'])

        # Compute recapture for this position using vocab seen BEFORE this token
        alts = tok.get('alternatives', [])
        alt_tokens_norm = [normalize_token(a['token']) for a in alts]
        probs = [a['prob'] for a in alts]

        if seen_vocab and len(alt_tokens_norm) >= 2:
            recapture = sum(1 for t in alt_tokens_norm if t in seen_vocab) / len(alt_tokens_norm)
        else:
            recapture = 0.0

        # Compute alpha from probs
        alpha = fit_zipf(probs)

        decile_recaptures[decile].append(recapture)
        if alpha is not None:
            decile_alphas[decile].append(alpha)
        decile_vocab_sizes[decile].append(len(seen_vocab))
        per_token_recapture.append((pos_frac, recapture))

        # NOW add token to seen vocab
        seen_vocab.add(norm_actual)

    # Aggregate by decile
    dr = [statistics.mean(decile_recaptures.get(d, [0])) for d in range(10)]
    da = [statistics.mean(decile_alphas.get(d, [1.0])) if decile_alphas.get(d) else None for d in range(10)]
    dvs = [statistics.mean(decile_vocab_sizes.get(d, [0])) for d in range(10)]

    # Compute bubble slope (linear regression of recapture vs position)
    xs = [p for p, _ in per_token_recapture]
    ys = [r for _, r in per_token_recapture]
    slope = linreg_slope(xs, ys)

    return {
        'decile_recapture': dr,
        'decile_alpha': da,
        'bubble_slope': slope,
        'max_recapture': max(dr),
        'final_recapture': dr[9],
        'opening_recapture': dr[0],
        'vocab_size_trajectory': dvs,
        'n_tokens': n,
    }


def fit_zipf(probs: list) -> float | None:
    """Fit Zipf exponent to list of probabilities (rank-ordered)."""
    if len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    if len(normed) < 2:
        return None

    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_probs = [math.log(p) for p in normed]

    mean_lr = sum(log_ranks) / n
    mean_lp = sum(log_probs) / n

    numer = sum((log_ranks[i] - mean_lr) * (log_probs[i] - mean_lp) for i in range(n))
    denom = sum((log_ranks[i] - mean_lr) ** 2 for i in range(n))

    if denom == 0:
        return None
    return -numer / denom


def linreg_slope(xs, ys):
    """Simple linear regression slope."""
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    numer = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    denom = sum((xs[i] - mx) ** 2 for i in range(n))
    return numer / denom if denom != 0 else 0.0


def main():
    with open('results/corpus_results.json') as f:
        corpus = json.load(f)

    results = []
    era_data = defaultdict(list)
    poet_data = defaultdict(list)

    for poem in corpus:
        meta = poem.get('metadata', {})
        tokens = poem.get('tokens', [])

        if not tokens:
            continue

        bubble = compute_poem_bubble(tokens)
        if bubble is None:
            continue

        era = meta.get('era', 'unknown')
        author = meta.get('author', 'Unknown')
        title = meta.get('title', 'Untitled')
        is_control = era in ('control',)

        entry = {
            'title': title,
            'author': author,
            'era': era,
            'is_control': is_control,
            **bubble
        }
        results.append(entry)

        if not is_control:
            era_data[era].append(bubble)
            poet_data[author].append(bubble)

    # Sort by bubble slope (highest = fastest bubble formation)
    results.sort(key=lambda x: x['bubble_slope'], reverse=True)

    # Era summary
    era_summary = []
    for era, bubbles in era_data.items():
        if len(bubbles) < 2:
            continue
        slopes = [b['bubble_slope'] for b in bubbles]
        final_r = [b['final_recapture'] for b in bubbles]
        opening_r = [b['opening_recapture'] for b in bubbles]
        era_summary.append({
            'era': era,
            'n': len(bubbles),
            'avg_slope': statistics.mean(slopes),
            'avg_final_recapture': statistics.mean(final_r),
            'avg_opening_recapture': statistics.mean(opening_r),
            'recapture_gain': statistics.mean(final_r) - statistics.mean(opening_r),
        })
    era_summary.sort(key=lambda x: x['avg_slope'], reverse=True)

    # Corpus-wide decile averages (poetry only)
    poetry_results = [r for r in results if not r['is_control']]
    decile_avg_recapture = []
    decile_avg_alpha = []
    for d in range(10):
        recaps = [r['decile_recapture'][d] for r in poetry_results]
        alphas = [r['decile_alpha'][d] for r in poetry_results if r['decile_alpha'][d] is not None]
        decile_avg_recapture.append(statistics.mean(recaps) if recaps else 0.0)
        decile_avg_alpha.append(statistics.mean(alphas) if alphas else 0.0)

    # Control comparison
    control_results = [r for r in results if r['is_control']]
    control_decile_recapture = []
    for d in range(10):
        recaps = [r['decile_recapture'][d] for r in control_results]
        control_decile_recapture.append(statistics.mean(recaps) if recaps else 0.0)

    output = {
        'summary': {
            'n_poems_analyzed': len(results),
            'poetry_avg_slope': statistics.mean([r['bubble_slope'] for r in poetry_results]),
            'control_avg_slope': statistics.mean([r['bubble_slope'] for r in control_results]) if control_results else None,
        },
        'corpus_wide_decile_trajectory': {
            'decile_labels': [f'D{d+1}' for d in range(10)],
            'poetry_recapture': [round(x, 4) for x in decile_avg_recapture],
            'control_recapture': [round(x, 4) for x in control_decile_recapture],
            'poetry_alpha': [round(x, 4) if x else None for x in decile_avg_alpha],
        },
        'era_summary': era_summary,
        'top_bubble_poems': [
            {k: (round(v, 4) if isinstance(v, float) else v)
             for k, v in r.items()
             if k not in ('decile_recapture', 'decile_alpha', 'vocab_size_trajectory')}
            for r in results[:15]
        ],
        'lowest_bubble_poems': [
            {k: (round(v, 4) if isinstance(v, float) else v)
             for k, v in r.items()
             if k not in ('decile_recapture', 'decile_alpha', 'vocab_size_trajectory')}
            for r in results[-15:]
        ],
        'all_poems': results,
    }

    with open('results/vocabulary_bubble.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Analyzed {len(results)} poems")
    print(f"Poetry avg bubble slope: {output['summary']['poetry_avg_slope']:.4f}")
    if output['summary']['control_avg_slope'] is not None:
        print(f"Control avg bubble slope: {output['summary']['control_avg_slope']:.4f}")

    print("\nCorpus-wide recapture trajectory (by decile):")
    traj = output['corpus_wide_decile_trajectory']
    for d in range(10):
        pr = traj['poetry_recapture'][d]
        cr = traj['control_recapture'][d] if d < len(traj['control_recapture']) else 0
        pa = traj['poetry_alpha'][d]
        print(f"  D{d+1}: poetry={pr:.3f}  control={cr:.3f}  alpha={pa:.3f}")

    print("\nTop 10 fastest bubble-forming poems:")
    for r in results[:10]:
        print(f"  slope={r['bubble_slope']:.4f}  final_r={r['final_recapture']:.3f}  "
              f"{r['author']}: '{r['title']}'")

    print("\nTop 10 slowest bubble-forming (most novelty-maintaining) poems:")
    for r in results[-10:]:
        print(f"  slope={r['bubble_slope']:.4f}  final_r={r['final_recapture']:.3f}  "
              f"{r['author']}: '{r['title']}'")

    print("\nEra averages (top/bottom 10 by slope):")
    for era in era_summary[:10]:
        print(f"  {era['era']:25s} n={era['n']:3d}  slope={era['avg_slope']:.4f}  "
              f"gain={era['recapture_gain']:.3f}  final={era['avg_final_recapture']:.3f}")
    print("  ...")
    for era in era_summary[-5:]:
        print(f"  {era['era']:25s} n={era['n']:3d}  slope={era['avg_slope']:.4f}  "
              f"gain={era['recapture_gain']:.3f}  final={era['avg_final_recapture']:.3f}")


if __name__ == '__main__':
    main()
