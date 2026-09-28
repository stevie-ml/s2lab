"""
Alternative Landscape: WHY are line-final tokens predictable?

Research question: We know line-final tokens have lower S2 (-0.49 vs +5.57 for
line-initial). But is this because:
  A) GPT-2 is already CONTEXT-CONSTRAINED at line endings — only a narrow set of
     alternatives are possible, so the poet picks from a small pool?
  B) Poets make an ACTIVE CHOICE — GPT-2 offers diverse alternatives but poets
     reliably choose conventional, expected endings anyway?

Method: For each token position, analyze the TOP-10 ALTERNATIVES in the corpus
results (already stored). Compute:
  1. "Concentration": entropy of the alternatives' probability distribution
     (how sure is GPT-2 about its top prediction?)
  2. "Coverage": cumulative probability of top-10 alternatives
     (how much of the probability mass is in the top 10?)
  3. "Spread": standard deviation of alternative probs
  4. "Chosen rank": where does the actual token rank among all alternatives?

Then compare these metrics at line-initial vs. medial vs. line-final positions.

If A is true: concentration should be HIGH at line-final (tight constraint)
If B is true: concentration should be LOW at line-final (poet ignores diverse options)
"""

import sys
import os
import json
import math
import statistics
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FINDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings")


def detect_line_position(tokens):
    """
    Tag each token with line position based on presence of newline tokens.
    Returns list of position labels: 'initial', 'medial', 'final'
    """
    positions = []
    n = len(tokens)

    # Find indices of newline tokens
    newline_indices = {i for i, t in enumerate(tokens) if '\n' in t['token']}

    for i, tok in enumerate(tokens):
        token_str = tok['token']

        if '\n' in token_str:
            # Newline itself — treat as final of the preceding line
            positions.append('final')
            continue

        # Is previous token a newline (or this is the first token)?
        prev_is_newline = (i == 0) or ('\n' in tokens[i-1]['token'])

        # Is next token a newline (or this is the last token)?
        next_is_newline = (i == n-1) or ('\n' in tokens[i+1]['token'])

        if prev_is_newline:
            positions.append('initial')
        elif next_is_newline:
            positions.append('final')
        else:
            positions.append('medial')

    return positions


def analyze_alternative_landscape(token):
    """
    Given a token dict with 'alternatives' list, compute:
    - concentration: entropy of alternatives probs (lower = more concentrated)
    - coverage: sum of alternative probs (how much mass in top-10?)
    - top1_prob: probability of GPT-2's top prediction
    - prob_gap: difference between top-1 and top-2 probs
    - chosen_in_top10: whether actual token is in the top-10 alternatives
    - chosen_rank: rank of actual token (1=top prediction, None if not in top-10)
    """
    alts = token.get('alternatives', [])
    if not alts:
        return None

    probs = [a['prob'] for a in alts]
    total_prob = sum(probs)

    # Entropy of alternative distribution (using raw probs, not normalized)
    alt_entropy = 0.0
    for p in probs:
        if p > 0:
            alt_entropy -= p * math.log2(p)

    # Concentration = negative entropy (higher = more concentrated on top prediction)
    top1_prob = probs[0] if probs else 0.0
    top2_prob = probs[1] if len(probs) > 1 else 0.0
    prob_gap = top1_prob - top2_prob

    # Is the actual token in the top-10 alternatives?
    actual_token = token['token'].strip().lower()
    alt_tokens = [a['token'].strip().lower() for a in alts]

    chosen_in_top10 = actual_token in alt_tokens
    chosen_rank = None
    if chosen_in_top10:
        try:
            chosen_rank = alt_tokens.index(actual_token) + 1  # 1-indexed
        except ValueError:
            pass

    return {
        'alt_entropy': alt_entropy,
        'coverage': total_prob,
        'top1_prob': top1_prob,
        'prob_gap': prob_gap,
        'chosen_in_top10': chosen_in_top10,
        'chosen_rank': chosen_rank,
        's2': token['s2'],
        'token_entropy': token['entropy'],
    }


def main():
    # Load existing corpus results
    results_path = os.path.join(RESULTS_DIR, "corpus_results.json")
    with open(results_path) as f:
        corpus = json.load(f)

    # Filter to English poetry only (exclude control/non-English)
    poetry = [
        p for p in corpus
        if p['metadata'].get('language', 'en') == 'en'
        and p['metadata'].get('era', '') not in ('control', 'cliche_control')
    ]

    print(f"Analyzing {len(poetry)} English poetry texts...")

    # Aggregate by position
    position_data = defaultdict(lambda: {
        'alt_entropy': [], 'coverage': [], 'top1_prob': [], 'prob_gap': [],
        'chosen_in_top10': [], 'chosen_rank': [], 's2': [], 'token_entropy': []
    })

    era_data = defaultdict(lambda: defaultdict(lambda: {'s2': [], 'alt_entropy': [], 'chosen_in_top10': []}))

    total_tokens = 0
    poems_processed = 0

    for poem in poetry:
        tokens = poem.get('tokens', [])
        if len(tokens) < 5:
            continue

        era = poem['metadata'].get('era', 'unknown')
        positions = detect_line_position(tokens)

        for tok, pos in zip(tokens, positions):
            metrics = analyze_alternative_landscape(tok)
            if metrics is None:
                continue

            total_tokens += 1

            for key in position_data[pos]:
                val = metrics.get(key)
                if val is not None:
                    position_data[pos][key].append(val)

            # Track era-level data
            era_data[era][pos]['s2'].append(tok['s2'])
            era_data[era][pos]['alt_entropy'].append(metrics['alt_entropy'])
            era_data[era][pos]['chosen_in_top10'].append(int(metrics['chosen_in_top10']))

        poems_processed += 1

    print(f"Processed {poems_processed} poems, {total_tokens} tokens")

    # Summary stats
    def mean(lst):
        return sum(lst) / len(lst) if lst else 0.0

    def pct(lst):
        return 100 * sum(lst) / len(lst) if lst else 0.0

    print("\n=== ALTERNATIVE LANDSCAPE BY LINE POSITION ===\n")

    results = {}
    for pos in ['initial', 'medial', 'final']:
        d = position_data[pos]
        n = len(d['s2'])

        results[pos] = {
            'n': n,
            'avg_s2': mean(d['s2']),
            'avg_alt_entropy': mean(d['alt_entropy']),
            'avg_top1_prob': mean(d['top1_prob']),
            'avg_prob_gap': mean(d['prob_gap']),
            'avg_coverage': mean(d['coverage']),
            'chosen_in_top10_pct': pct(d['chosen_in_top10']),
            'avg_token_entropy': mean(d['token_entropy']),
        }

        # For tokens in top-10, what's avg rank?
        ranks = [r for r in d['chosen_rank'] if r is not None]
        results[pos]['avg_chosen_rank'] = mean(ranks) if ranks else None
        results[pos]['n_in_top10'] = len(ranks)

        r = results[pos]
        print(f"Position: {pos.upper()} (n={n:,})")
        print(f"  Avg S₂:             {r['avg_s2']:+.3f}")
        print(f"  Avg context H:      {r['avg_token_entropy']:.3f} bits")
        print(f"  Avg alt entropy:    {r['avg_alt_entropy']:.4f}  (concentration of predictions)")
        print(f"  Avg top-1 prob:     {r['avg_top1_prob']:.4f}  (how sure GPT-2 is)")
        print(f"  Avg prob gap (1-2): {r['avg_prob_gap']:.4f}  (margin of top prediction)")
        print(f"  Avg coverage:       {r['avg_coverage']:.4f}  (cum prob of top-10)")
        print(f"  Chosen in top-10:   {r['chosen_in_top10_pct']:.1f}%")
        if r['avg_chosen_rank']:
            print(f"  Avg rank (if in top-10): {r['avg_chosen_rank']:.2f}")
        print()

    # The key test: Does GPT-2 offer NARROWER alternatives at line endings?
    init = results['initial']
    fin = results['final']
    med = results['medial']

    print("=== THE KEY COMPARISON ===")
    print(f"Δ alt entropy (final - initial): {fin['avg_alt_entropy'] - init['avg_alt_entropy']:+.4f}")
    print(f"  (positive = final is LESS concentrated; negative = MORE concentrated)")
    print(f"Δ top-1 prob (final - initial):  {fin['avg_top1_prob'] - init['avg_top1_prob']:+.4f}")
    print(f"  (positive = GPT-2 more certain at line endings)")
    print(f"Δ coverage (final - initial):    {fin['avg_coverage'] - init['avg_coverage']:+.4f}")
    print(f"Δ chosen_in_top10 (final - initial): {fin['chosen_in_top10_pct'] - init['chosen_in_top10_pct']:+.1f}pp")
    print()

    # Era breakdown
    print("=== CHOSEN-IN-TOP10 RATE BY ERA AND POSITION ===")
    print(f"{'Era':<25} {'initial':>10} {'medial':>10} {'final':>10} {'Δ(fin-init)':>12}")

    era_rows = []
    for era, pos_dict in sorted(era_data.items()):
        row = {'era': era}
        for pos in ['initial', 'medial', 'final']:
            vals = pos_dict[pos]['chosen_in_top10']
            row[pos] = 100 * sum(vals) / len(vals) if vals else None
        if row['initial'] and row['final']:
            row['delta'] = row['final'] - row['initial']
            era_rows.append(row)

    era_rows.sort(key=lambda x: x['delta'])
    for row in era_rows:
        delta_str = f"{row['delta']:+.1f}" if row['delta'] is not None else "N/A"
        print(f"{row['era']:<25} {row['initial']:>9.1f}% {row['medial']:>9.1f}% {row['final']:>9.1f}% {delta_str:>12}")

    # S2 and alt_entropy correlation
    print("\n=== DOES HIGH ALT-ENTROPY (DISPERSED PREDICTIONS) PREDICT HIGH S₂? ===")
    # Use medial tokens (cleanest signal)
    med_d = position_data['medial']
    n_med = len(med_d['s2'])

    if n_med > 100:
        # Bucket by alt_entropy quartiles
        combined = list(zip(med_d['alt_entropy'], med_d['s2']))
        combined.sort(key=lambda x: x[0])
        q = n_med // 4

        quartile_labels = ['Q1 (most concentrated)', 'Q2', 'Q3', 'Q4 (most dispersed)']
        for i, label in enumerate(quartile_labels):
            chunk = combined[i*q:(i+1)*q]
            alt_ents = [x[0] for x in chunk]
            s2s = [x[1] for x in chunk]
            print(f"  {label}: avg alt_entropy={mean(alt_ents):.4f}, avg S₂={mean(s2s):+.3f}")

    # Save results
    output = {
        'position_results': results,
        'era_breakdown': {
            era: {pos: {
                'chosen_in_top10_pct': 100 * sum(v['chosen_in_top10']) / len(v['chosen_in_top10']) if v['chosen_in_top10'] else None,
                'avg_s2': mean(v['s2']),
                'avg_alt_entropy': mean(v['alt_entropy']),
                'n': len(v['s2'])
            } for pos, v in pos_dict.items()}
            for era, pos_dict in era_data.items()
        }
    }

    out_path = os.path.join(RESULTS_DIR, "alternative_landscape.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results, era_rows


if __name__ == "__main__":
    main()
