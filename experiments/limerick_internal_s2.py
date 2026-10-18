"""
Limerick Internal S2 Structure

AABBA rhyme scheme: lines 1-2 (setup), 3-4 (twist/reveal), 5 (punchline).
Hypothesis: The twist lines (3-4) have higher S2 than setup (1-2) and punchline (5),
because the poet must surprise within maximum formal constraint.

Artifact-free: excludes tokens where p_newline > 0.9 (stanza-break artifact).
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

RESULTS_FILE = os.path.join(os.path.dirname(__file__), '..', 'results', 'corpus_results.json')


def split_into_lines(tokens):
    """Group tokens by line number (separated by newline tokens)."""
    lines = []
    current_line = []
    for t in tokens:
        if '\n' in t['token'] and len(t['token'].strip()) == 0:
            if current_line:
                lines.append(current_line)
            current_line = []
        else:
            current_line.append(t)
    if current_line:
        lines.append(current_line)
    return lines


def is_artifact(token):
    return token.get('p_newline', 0) > 0.9


def line_stats(line_tokens, artifact_free=True):
    toks = [t for t in line_tokens if not (artifact_free and is_artifact(t))]
    if not toks:
        return None
    s2_vals = [t['s2'] for t in toks]
    return {
        'n': len(s2_vals),
        'mean_s2': sum(s2_vals) / len(s2_vals),
        'pos_ratio': sum(1 for v in s2_vals if v > 0) / len(s2_vals),
        'mean_entropy': sum(t['entropy'] for t in toks) / len(toks),
        'mean_surprisal': sum(t['surprisal'] for t in toks) / len(toks),
    }


def analyze_limericks(data):
    results = []
    for poem in data:
        if poem.get('metadata', {}).get('era') != 'limerick':
            continue
        meta = poem['metadata']
        tokens = poem['tokens']

        # Reconstruct lines from token stream
        lines = split_into_lines(tokens)

        # A limerick has exactly 5 lines; skip if different
        if len(lines) != 5:
            # Try to handle trailing empty lines
            non_empty = [l for l in lines if l]
            if len(non_empty) != 5:
                continue
            lines = non_empty

        setup = lines[0] + lines[1]
        twist = lines[2] + lines[3]
        punchline = lines[4]

        results.append({
            'title': meta['title'],
            'author': meta['author'],
            'n_lines': len(lines),
            'setup': line_stats(setup),
            'twist': line_stats(twist),
            'punchline': line_stats(punchline),
            'line_by_line': [line_stats(l) for l in lines],
        })
    return results


def pool_stats(group_data_list):
    """Pool S2 values across poems for a group."""
    all_s2 = []
    all_entropy = []
    pos_count = 0
    total = 0
    for group in group_data_list:
        if group is None:
            continue
        n = group['n']
        all_s2.extend([group['mean_s2']] * n)  # weighted mean proxy
        all_entropy.extend([group['mean_entropy']] * n)
        pos_count += group['pos_ratio'] * n
        total += n
    if not all_s2:
        return None
    return {
        'n_tokens': total,
        'mean_s2': sum(all_s2) / len(all_s2),
        'pos_ratio': pos_count / total if total else 0,
        'mean_entropy': sum(all_entropy) / len(all_entropy),
    }


def main():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    results = analyze_limericks(data)

    if not results:
        print("No limericks found in corpus.")
        return

    print(f"\n=== LIMERICK INTERNAL S2 STRUCTURE ===")
    print(f"Poems analyzed: {len(results)}\n")

    # Per-poem table
    print("Per-poem breakdown (artifact-free S2):\n")
    print(f"{'Title':<42} {'Setup(1-2)':<12} {'Twist(3-4)':<12} {'Punchline(5)':<12} {'Twist>Setup?'}")
    print("-" * 85)
    for r in results:
        s = r['setup']['mean_s2'] if r['setup'] else float('nan')
        tw = r['twist']['mean_s2'] if r['twist'] else float('nan')
        pl = r['punchline']['mean_s2'] if r['punchline'] else float('nan')
        flag = "YES" if tw > s else "no"
        print(f"{r['title']:<42} {s:>+8.3f}    {tw:>+8.3f}    {pl:>+8.3f}     {flag}")

    print()

    # Pooled stats by position
    setup_pool = pool_stats([r['setup'] for r in results])
    twist_pool = pool_stats([r['twist'] for r in results])
    punch_pool = pool_stats([r['punchline'] for r in results])

    print("Pooled stats across all limericks:\n")
    print(f"{'Group':<15} {'Mean S2':>10} {'Pos%':>8} {'Mean H':>10} {'N tokens':>10}")
    print("-" * 55)
    for label, pool in [('Setup (L1-2)', setup_pool), ('Twist (L3-4)', twist_pool), ('Punchline (L5)', punch_pool)]:
        if pool:
            print(f"{label:<15} {pool['mean_s2']:>+10.3f} {pool['pos_ratio']*100:>7.1f}% {pool['mean_entropy']:>10.3f} {pool['n_tokens']:>10}")

    # Line-by-line average
    print("\nLine-by-line average S2 (pooled across poems):\n")
    print(f"{'Line':<10} {'Avg S2':>10} {'Pos%':>8}")
    print("-" * 30)
    for line_idx in range(5):
        line_group = [r['line_by_line'][line_idx] for r in results
                      if r['line_by_line'] and len(r['line_by_line']) > line_idx
                      and r['line_by_line'][line_idx] is not None]
        if line_group:
            avg = sum(g['mean_s2'] for g in line_group) / len(line_group)
            pos = sum(g['pos_ratio'] for g in line_group) / len(line_group)
            rhyme = 'A' if line_idx in (0, 1, 4) else 'B'
            role = ['setup', 'setup', 'twist', 'twist', 'punch'][line_idx]
            print(f"Line {line_idx+1} ({rhyme},{role:<6}) {avg:>+10.3f} {pos*100:>7.1f}%")

    # Return structured results for writing
    return {
        'n_poems': len(results),
        'poems': results,
        'pooled': {
            'setup': setup_pool,
            'twist': twist_pool,
            'punchline': punch_pool,
        }
    }


if __name__ == '__main__':
    result = main()
    if result:
        out_path = os.path.join(os.path.dirname(__file__), '..', 'results', 'limerick_internal_s2.json')
        with open(out_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\nResults saved to {out_path}")
