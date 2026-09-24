"""
Lexical Fork Analysis: How do poets navigate genuine model uncertainty?

At 'fork' positions — where GPT-2's probability is split among multiple competing
tokens (no single dominant prediction) — does poetry exploit the offered choices or
create surprise by taking none of them?

This tests whether poetic deviation is primarily about:
  (a) Surprising the confident model (confidence_trap type: certainty defeated)
  (b) Escaping the undecided model (fork type: all offered paths refused)
  (c) Choosing among offered paths (fork navigation: taking one of the model's options)

A 'fork' is defined as a position where top-1 alternative probability < 2.5× top-2 alternative
probability AND top-1 probability < 0.50 (model genuinely undecided between options).

'Escape' means the actual token was NOT in the top-10 alternatives at a fork.
'Navigation' means the actual token WAS in the top-10 alternatives at a fork.
'Confident trap' means entropy was low (< 3 bits) and the actual token was not in top-10.
"""

import json
import sys
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

def load_corpus():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def is_fork(alts):
    """True if top-2 alternatives are within 2.5:1 ratio AND top-1 < 0.50 probability."""
    if len(alts) < 2:
        return False
    p1 = alts[0]['prob']
    p2 = alts[1]['prob']
    if p2 == 0:
        return False
    return (p1 < 0.50) and (p1 / p2 < 2.5)

def classify_position(token_data):
    """
    Returns a classification string for this token position:
      'fork_escape'   - fork position, actual token not in top-10
      'fork_navigate' - fork position, actual token was in top-10
      'trap'          - high confidence (entropy < 3), actual token not in top-10
      'neutral'       - everything else
    """
    alts = token_data.get('alternatives', [])
    entropy = token_data.get('entropy', 999)
    rank = token_data.get('rank', 9999)
    s2 = token_data.get('s2', 0)

    in_top10 = rank <= 10
    fork = is_fork(alts)

    if fork and not in_top10:
        return 'fork_escape'
    elif fork and in_top10:
        return 'fork_navigate'
    elif entropy < 3.0 and not in_top10:
        return 'trap'
    else:
        return 'neutral'

def fork_options_summary(alts):
    """Get the top-3 alternative tokens as a string."""
    tops = [a['token'].strip() for a in alts[:3]]
    return ' / '.join(f'"{t}"' for t in tops)

def run():
    corpus = load_corpus()

    # Global tallies
    class_counts = defaultdict(int)
    class_s2 = defaultdict(list)
    era_stats = defaultdict(lambda: defaultdict(list))

    # Track interesting fork escapes
    fork_escapes = []

    # Track fork navigation: which top-N slot is chosen?
    fork_nav_ranks = []

    for poem in corpus:
        meta = poem.get('metadata', {})
        era = meta.get('era', 'unknown')
        title = meta.get('title', '?')
        author = meta.get('author', '?')
        lang = meta.get('language', 'en')

        if lang != 'en':
            continue

        for tok in poem.get('tokens', []):
            cls = classify_position(tok)
            s2 = tok.get('s2', 0)
            rank = tok.get('rank', 9999)

            class_counts[cls] += 1
            class_s2[cls].append(s2)
            era_stats[era][cls].append(s2)

            if cls == 'fork_navigate':
                fork_nav_ranks.append(rank)

            # Collect best fork_escape moments
            if cls == 'fork_escape' and s2 > 5.0:
                alts = tok.get('alternatives', [])
                fork_escapes.append({
                    'title': title,
                    'author': author,
                    'era': era,
                    'token': tok['token'],
                    's2': s2,
                    'entropy': tok.get('entropy', 0),
                    'rank': rank,
                    'offered': fork_options_summary(alts),
                    'top1_prob': alts[0]['prob'] if alts else 0,
                    'top2_prob': alts[1]['prob'] if len(alts) > 1 else 0,
                })

    # Sort escapes by S2
    fork_escapes.sort(key=lambda x: x['s2'], reverse=True)

    # Navigation rank distribution
    nav_rank_dist = defaultdict(int)
    for r in fork_nav_ranks:
        nav_rank_dist[r] += 1

    # --- Output ---
    print("=" * 60)
    print("LEXICAL FORK ANALYSIS")
    print("=" * 60)
    print()

    # 1. Overall token classification
    total = sum(class_counts.values())
    print("## 1. Token Classification (English poems only)")
    print()
    print(f"{'Class':<20} {'Count':>7} {'%':>6} {'Avg S2':>8} {'%+S2':>7}")
    print("-" * 52)
    for cls in ['fork_escape', 'fork_navigate', 'trap', 'neutral']:
        n = class_counts[cls]
        pct = 100 * n / total if total else 0
        s2_vals = class_s2[cls]
        avg_s2 = sum(s2_vals) / len(s2_vals) if s2_vals else 0
        pct_pos = 100 * sum(1 for v in s2_vals if v > 0) / len(s2_vals) if s2_vals else 0
        print(f"{cls:<20} {n:>7,} {pct:>6.1f}% {avg_s2:>8.3f} {pct_pos:>6.1f}%")
    print(f"{'TOTAL':<20} {total:>7,}")
    print()

    # 2. Fork navigation: which rank slot do poets choose?
    print("## 2. At Fork Positions: Which Rank Does the Poet Choose?")
    print("(When the poet DOES pick one of the top-10 options at a fork)")
    print()
    nav_total = sum(nav_rank_dist.values())
    print(f"{'Rank':<8} {'Count':>7} {'%':>7}")
    print("-" * 25)
    for r in sorted(nav_rank_dist.keys()):
        n = nav_rank_dist[r]
        pct = 100 * n / nav_total if nav_total else 0
        print(f"{r:<8} {n:>7,} {pct:>7.1f}%")
    print()

    # Cumulative: how often is rank 1 or 2 chosen?
    r1 = nav_rank_dist.get(1, 0)
    r2 = nav_rank_dist.get(2, 0)
    r1_2_pct = 100 * (r1 + r2) / nav_total if nav_total else 0
    print(f"Top-1 or Top-2 chosen: {r1_2_pct:.1f}% of fork navigations")
    print()

    # 3. Era comparison: fork escape rate
    print("## 3. Era Comparison: Fork Escape Rate")
    print("(% of fork positions where poet rejects ALL top-10 options)")
    print()
    era_rows = []
    for era, stats in era_stats.items():
        n_escape = len(stats.get('fork_escape', []))
        n_navigate = len(stats.get('fork_navigate', []))
        n_fork_total = n_escape + n_navigate
        if n_fork_total < 5:
            continue
        escape_rate = 100 * n_escape / n_fork_total
        avg_escape_s2 = sum(stats.get('fork_escape', [0])) / max(len(stats.get('fork_escape', [1])), 1)
        era_rows.append((era, n_fork_total, n_escape, escape_rate, avg_escape_s2))

    era_rows.sort(key=lambda x: x[3], reverse=True)
    print(f"{'Era':<25} {'Fork pos':>9} {'Escapes':>8} {'Esc.%':>7} {'Avg S2 esc.':>11}")
    print("-" * 65)
    for era, n_fork, n_esc, esc_rate, avg_s2 in era_rows:
        print(f"{era:<25} {n_fork:>9,} {n_esc:>8,} {esc_rate:>7.1f}% {avg_s2:>11.3f}")
    print()

    # 4. Top fork escape moments
    print("## 4. Most Striking Fork Escapes (S2 > 5.0)")
    print("(High S2 at fork = poet refused ALL offered paths, chose something far outside the menu)")
    print()
    print(f"{'Poem':<35} {'Token':<15} {'S2':>6} {'Offered paths':<40}")
    print("-" * 100)
    for item in fork_escapes[:25]:
        poem_label = f"{item['title'][:20]} ({item['author'].split()[-1]})"
        print(f"{poem_label:<35} {item['token']:<15} {item['s2']:>6.2f} {item['offered']}")
    print()

    # 5. Fork escape vs confidence trap comparison
    print("## 5. Fork Escape vs Confidence Trap: S2 Comparison")
    print()
    print("Both fork escapes and confidence traps are 'surprises', but different kinds:")
    print("  - Confidence trap: model was certain (H < 3 bits), poet ignored it")
    print("  - Fork escape: model was genuinely split, poet rejected ALL offered options")
    print()
    fe_s2 = class_s2['fork_escape']
    ct_s2 = class_s2['trap']
    fn_s2 = class_s2['fork_navigate']

    for label, vals in [('Fork escape', fe_s2), ('Fork navigate', fn_s2), ('Confidence trap', ct_s2)]:
        if vals:
            avg = sum(vals) / len(vals)
            median = sorted(vals)[len(vals)//2]
            pct_pos = 100 * sum(1 for v in vals if v > 0) / len(vals)
            max_v = max(vals)
            print(f"  {label:<20} n={len(vals):>5,}  avg={avg:>7.3f}  median={median:>7.3f}  %+S2={pct_pos:>5.1f}%  max={max_v:>6.2f}")
    print()

    # 6. Save data for findings
    results = {
        'class_counts': dict(class_counts),
        'class_avg_s2': {cls: sum(v)/len(v) if v else 0 for cls, v in class_s2.items()},
        'class_pct_pos': {cls: 100*sum(1 for x in v if x>0)/len(v) if v else 0
                          for cls, v in class_s2.items()},
        'fork_nav_rank_dist': dict(nav_rank_dist),
        'era_fork_escape_rates': {
            era: {'n_fork': n_fork, 'n_escape': n_esc, 'escape_rate': esc_rate, 'avg_s2': avg_s2}
            for era, n_fork, n_esc, esc_rate, avg_s2 in era_rows
        },
        'top_fork_escapes': fork_escapes[:20],
    }
    with open('results/lexical_fork_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to results/lexical_fork_analysis.json")

if __name__ == '__main__':
    run()
