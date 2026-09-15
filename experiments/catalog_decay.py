"""
Catalog Decay: S₂ Patterns in Poetic Enumeration

Research question: When a poet creates a catalog or list (repeated parallel
structures, anaphora chains), does GPT-2's S₂ systematically decrease across
successive items — as the model learns the pattern — or does the poet maintain
surprise by inserting unexpected items?

Two competing hypotheses:
  - ADAPTATION: S₂ decays as repetition establishes expectation (model learns pattern)
  - SUBVERSION: poets insert "dark horses" mid-list that spike S₂ against the template

Method:
  1. Split tokens into lines using '\n' tokens.
  2. Identify anaphoric chains: 3+ consecutive lines opening with the same token.
  3. For each chain position, compute:
     - anchor_s2: S₂ of the repeated word itself (how surprising is repeating it?)
     - content_s2: mean S₂ of the remaining tokens on that line
  4. Test for monotonic decay vs. mid-chain peaks (subversive insertions).

Works entirely from corpus_results.json (no new model inference needed).
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

SKIP_ANCHORS = {'the', 'a', 'an', 'in', 'of', 'for', 'to', 'on', 'with', 'at', 'by',
                'that', 'this', 'there', 'which', 'do', 'did', 'will', 'would', 'should',
                'is', 'was', 'are', 'were', 'it', 'its', 'if', 'as', 'so', 'then',
                'from', 'into', 'through', 'over', 'under', 'after', 'before',
                'not', 'but', 'or', 'nor'}


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def mean_safe(lst):
    lst = [x for x in lst if x == x and x is not None]
    return statistics.mean(lst) if lst else float("nan")


def tokens_to_lines(tokens):
    """
    Split token sequence into lines using '\n' tokens.
    Each line is a list of (token_dict, position_in_line).
    Returns list of lines (lists of token dicts), excluding newline tokens.
    """
    lines = []
    current_line = []
    for tok in tokens:
        if tok['token'] == '\n':
            if current_line:
                lines.append(current_line)
            current_line = []
        else:
            current_line.append(tok)
    if current_line:
        lines.append(current_line)
    return lines


def identify_anaphora_chains(lines):
    """
    Find runs of 3+ consecutive lines where first token (normalized) is identical.
    Returns list of chains: [{anchor, positions (line indices), lines}]
    """
    if not lines:
        return []

    # Get the normalized first token of each line
    line_anchors = []
    for line in lines:
        if not line:
            line_anchors.append(None)
            continue
        first = line[0]['token'].strip().lower().rstrip(',.!?:;')
        if len(first) < 1 or first in SKIP_ANCHORS:
            line_anchors.append(None)
        else:
            line_anchors.append(first)

    chains = []
    i = 0
    while i < len(line_anchors):
        if line_anchors[i] is None:
            i += 1
            continue
        anchor = line_anchors[i]
        chain_indices = [i]
        j = i + 1
        while j < len(line_anchors) and line_anchors[j] == anchor:
            chain_indices.append(j)
            j += 1
        if len(chain_indices) >= 3:
            chains.append({
                'anchor': anchor,
                'line_indices': chain_indices,
                'n': len(chain_indices),
            })
        i = max(i + 1, j)
    return chains


def analyze_catalog_poem(poem):
    """
    Find anaphora chains and compute S₂ statistics by position in chain.
    """
    meta = poem.get('metadata', {})
    tokens = poem.get('tokens', [])
    if not tokens:
        return []

    lines = tokens_to_lines(tokens)
    if not lines:
        return []

    chains = identify_anaphora_chains(lines)
    if not chains:
        return []

    results = []
    for chain in chains:
        position_data = []
        for pos, line_idx in enumerate(chain['line_indices']):
            line = lines[line_idx]
            if not line:
                continue

            # anchor token: the repeated line-opener
            anchor_s2 = line[0]['s2']
            anchor_tok = line[0]['token']

            # content tokens: rest of the line (what varies across items)
            content_tokens = line[1:] if len(line) > 1 else []
            content_s2_vals = [t['s2'] for t in content_tokens]
            content_mean_s2 = mean_safe(content_s2_vals)
            content_max_s2 = max(content_s2_vals) if content_s2_vals else float('nan')

            # Full reconstruction of line text
            line_text = ''.join(t['token'] for t in line).strip()

            position_data.append({
                'position': pos + 1,
                'anchor_token': anchor_tok,
                'anchor_s2': anchor_s2,
                'content_mean_s2': content_mean_s2,
                'content_max_s2': content_max_s2,
                'n_content_tokens': len(content_tokens),
                'line_text': line_text[:70],
            })

        if len(position_data) < 3:
            continue

        # Compute slope of content_s2 across chain positions
        valid = [(pd['position'], pd['content_mean_s2'])
                 for pd in position_data
                 if pd['content_mean_s2'] == pd['content_mean_s2']]
        if len(valid) < 3:
            continue

        xs = [x for x, _ in valid]
        ys = [y for _, y in valid]
        xm = sum(xs) / len(xs)
        ym = sum(ys) / len(ys)
        num = sum((xs[i] - xm) * (ys[i] - ym) for i in range(len(xs)))
        den = sum((xs[i] - xm) ** 2 for i in range(len(xs)))
        slope = num / den if den > 0 else 0.0

        # Track anchor S₂ slope (how fast does repeating the word become predicted?)
        anchor_s2_vals = [pd['anchor_s2'] for pd in position_data]
        xs2 = list(range(len(anchor_s2_vals)))
        xm2 = sum(xs2) / len(xs2)
        ym2 = sum(anchor_s2_vals) / len(anchor_s2_vals)
        num2 = sum((xs2[i] - xm2) * (anchor_s2_vals[i] - ym2) for i in range(len(xs2)))
        den2 = sum((xs2[i] - xm2) ** 2 for i in range(len(xs2)))
        anchor_slope = num2 / den2 if den2 > 0 else 0.0

        # Identify mid-chain peaks (local maxima in content S₂)
        peaks = []
        for i in range(1, len(position_data) - 1):
            s2_i = position_data[i]['content_mean_s2']
            s2_prev = position_data[i-1]['content_mean_s2']
            s2_next = position_data[i+1]['content_mean_s2']
            if all(x == x for x in [s2_i, s2_prev, s2_next]):
                if s2_i > s2_prev and s2_i > s2_next:
                    peaks.append(i + 1)  # 1-indexed position

        results.append({
            'author': meta.get('author', '?'),
            'title': meta.get('title', '?'),
            'era': meta.get('era', '?'),
            'anchor': chain['anchor'],
            'chain_length': chain['n'],
            'content_slope': slope,
            'anchor_slope': anchor_slope,
            'first_content_s2': ys[0] if ys else float('nan'),
            'last_content_s2': ys[-1] if ys else float('nan'),
            'delta_s2': (ys[-1] - ys[0]) if ys else float('nan'),
            'anchor_s2_seq': anchor_s2_vals,
            'peaks': peaks,
            'position_data': position_data,
        })

    return results


def main():
    data = load_results()
    all_chains = []
    for poem in data:
        chains = analyze_catalog_poem(poem)
        all_chains.extend(chains)

    if not all_chains:
        print("No anaphora chains found.")
        return {}

    print(f"Found {len(all_chains)} anaphora chains across {len(data)} corpus texts\n")

    # Sort by chain length
    all_chains.sort(key=lambda c: c['chain_length'], reverse=True)

    print("=== ALL ANAPHORA CHAINS (sorted by length) ===")
    print(f"{'Author':<28} {'Title':<32} {'Anchor':<10} {'N':>3} {'ContentSlope':>13} {'Δ S₂':>8} {'Peaks':>6}")
    for c in all_chains:
        peaks_str = str(c['peaks']) if c['peaks'] else '-'
        print(f"{c['author'][:27]:<28} {c['title'][:31]:<32} '{c['anchor']}':{'':<2} "
              f"{c['chain_length']:>3} {c['content_slope']:>13.3f} {c['delta_s2']:>8.3f} {peaks_str:>6}")

    # Global summary
    adapting = [c for c in all_chains if c['content_slope'] < -0.05]
    subverting = [c for c in all_chains if c['content_slope'] > 0.05]
    flat = [c for c in all_chains if abs(c['content_slope']) <= 0.05]

    n = len(all_chains)
    print(f"\n=== ADAPTATION vs SUBVERSION (content S₂) ===")
    print(f"  Adapting   (content S₂ decays): {len(adapting):>3} chains  ({100*len(adapting)/n:.0f}%)")
    print(f"  Subverting (content S₂ grows):  {len(subverting):>3} chains  ({100*len(subverting)/n:.0f}%)")
    print(f"  Flat        (no clear trend):   {len(flat):>3} chains  ({100*len(flat)/n:.0f}%)")

    all_anchor_slopes = [c['anchor_slope'] for c in all_chains]
    print(f"\n=== ANCHOR S₂ (how fast does the repeated word become expected?) ===")
    print(f"  Mean anchor slope:  {mean_safe(all_anchor_slopes):.3f}")
    print(f"  (Negative = anchor word becomes rapidly predictable after first use)")

    # By era
    era_chains = defaultdict(list)
    for c in all_chains:
        era_chains[c['era']].append(c)

    print("\n=== MEAN CONTENT S₂ SLOPE BY ERA ===")
    era_rows = sorted(
        [(era, chains) for era, chains in era_chains.items()],
        key=lambda x: mean_safe([c['content_slope'] for c in x[1]])
    )
    for era, chains in era_rows:
        slopes = [c['content_slope'] for c in chains]
        avg_slope = mean_safe(slopes)
        tag = 'ADAPTING' if avg_slope < -0.05 else 'SUBVERTING' if avg_slope > 0.05 else 'flat'
        print(f"  {era:<25} n={len(chains):>2}  avg_slope={avg_slope:>8.3f}  {tag}")

    # Detailed position breakdown for chains of 5+
    print("\n=== DETAILED POSITION ANALYSIS (chains of 5+ lines) ===")
    long_chains = [c for c in all_chains if c['chain_length'] >= 5]
    for c in long_chains:
        print(f"\n{c['author']} — {c['title']}")
        print(f"  Anchor: '{c['anchor']}'  ({c['chain_length']} lines)  "
              f"content_slope={c['content_slope']:.3f}  anchor_slope={c['anchor_slope']:.3f}")
        print(f"  {'Pos':>4}  {'Anchor S₂':>9}  {'Content S₂':>11}  Line")
        for pd in c['position_data']:
            peak_flag = " ← PEAK" if pd['position'] in c['peaks'] else ""
            print(f"  {pd['position']:>4}  {pd['anchor_s2']:>9.3f}  {pd['content_mean_s2']:>11.3f}  {pd['line_text'][:55]}{peak_flag}")

    # Szymborska deep dive
    szym = [c for c in all_chains if 'szymborska' in c['author'].lower()]
    if szym:
        print("\n=== SZYMBORSKA 'POSSIBILITIES' DEEP DIVE ===")
        for c in szym:
            print(f"\n  Anchor: '{c['anchor']}'  ({c['chain_length']} lines)")
            print(f"  First item content S₂: {c['first_content_s2']:.3f}")
            print(f"  Last item content S₂:  {c['last_content_s2']:.3f}")
            print(f"  Content slope: {c['content_slope']:.3f}  Anchor slope: {c['anchor_slope']:.3f}")
            print(f"  Internal peaks at positions: {c['peaks'] if c['peaks'] else 'none'}")
            print(f"\n  {'Pos':>4}  {'Anchor S₂':>9}  {'Content S₂':>11}  Line")
            for pd in c['position_data']:
                flag = " ← PEAK" if pd['position'] in c['peaks'] else ""
                print(f"  {pd['position']:>4}  {pd['anchor_s2']:>9.3f}  {pd['content_mean_s2']:>11.3f}  {pd['line_text'][:55]}{flag}")

    return {
        'all_chains': all_chains,
        'n_chains': n,
        'n_adapting': len(adapting),
        'n_subverting': len(subverting),
        'n_flat': len(flat),
    }


if __name__ == "__main__":
    main()
