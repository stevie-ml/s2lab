"""
Haiku Kireji Analysis: S₂ at the Cut

Haiku are excluded from the spike_symmetry.py analysis because their spikes are too
dense to satisfy the ±8-token isolation criterion. But haiku have a known, structural
juxtaposition: the kireji (cutting word), realized in English translation as em dash (—),
colon (:), or punctuation at end of phrase 1 or 2.

Research Questions:
1. Is S₂ elevated at the first token of each image (phrase 1, 2, 3)?
2. Does the kireji token itself carry elevated S₂?
3. Does the "juxtaposition effect" (semantic distance between images) manifest as
   elevated S₂ at the post-kireji token (+1 after cut)?
4. How does haiku's "pre-kireji vs post-kireji" S₂ balance compare to the global
   Conservation Principle found in spike_symmetry.py?

Methodology:
- For each individual haiku (not grouped 3-haiku poems), identify the kireji position.
- "Kireji token" = the —, :, or ! that ends phrase 1 or phrase 2.
- "Phrase 1" = tokens before first kireji or newline.
- "Phrase 3" = tokens after final kireji / end of phrase 2.
- Compare mean S₂ across phrase 1 vs phrase 3.
- Compare S₂ at kireji token vs surrounding tokens.
"""

import json
import numpy as np
from collections import defaultdict

KIREJI_TOKENS = {'—', ':', '!', ';'}

def load_data():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def is_kireji(token_str):
    """Check if a token string is or contains a kireji marker."""
    return any(k in token_str for k in KIREJI_TOKENS)

def find_kireji_positions(tokens):
    """
    Find the kireji position(s) in a haiku's token list.
    Returns list of (position_index, token_str) for kireji tokens.
    We prioritize em dash (—) over colon/semicolon, and look for
    structural markers (not punctuation mid-phrase).
    """
    kireji_positions = []
    for i, tok in enumerate(tokens):
        t = tok['token']
        if '—' in t:
            kireji_positions.append((i, t, 'emdash'))
        elif ':' in t and t.strip() == ':':
            kireji_positions.append((i, t, 'colon'))
        elif ';' in t and t.strip() == ';':
            kireji_positions.append((i, t, 'semicolon'))
        elif '!' in t and t.strip() == '!':
            kireji_positions.append((i, t, 'exclamation'))
    return kireji_positions

def get_phrase_s2(tokens, start, end):
    """Mean S₂ for tokens in [start, end) range, excluding newlines."""
    vals = [tokens[i]['s2'] for i in range(start, end)
            if i < len(tokens) and '\n' not in tokens[i]['token']]
    return np.mean(vals) if vals else None

def analyze_haiku(poem_data):
    """
    Analyze a single haiku's S₂ structure around the kireji.
    Returns a dict with kireji info and phrase S₂ values.
    """
    meta = poem_data['metadata']
    tokens = poem_data['tokens']
    n = len(tokens)

    if n < 5:
        return None

    # Find newline positions (structural breaks)
    newline_positions = [i for i, t in enumerate(tokens) if '\n' in t['token']]

    # Find kireji positions
    kireji_positions = find_kireji_positions(tokens)

    # Identify the main cut position:
    # Prefer em dash/colon/semicolon over newline-only
    main_cut_idx = None
    cut_type = None
    if kireji_positions:
        # Take the first structural kireji
        main_cut_idx, cut_tok, cut_type = kireji_positions[0]
    elif newline_positions:
        # Fall back to first newline
        main_cut_idx = newline_positions[0]
        cut_type = 'newline'

    if main_cut_idx is None:
        return None

    # Phrase 1 = before cut (non-newline tokens)
    phrase1_s2 = get_phrase_s2(tokens, 0, main_cut_idx)

    # Phrase 3 = after the last newline or after the second kireji
    if len(newline_positions) >= 2:
        phrase3_start = newline_positions[-2] + 1
    elif len(newline_positions) >= 1:
        phrase3_start = newline_positions[0] + 1
    else:
        phrase3_start = main_cut_idx + 1

    phrase3_s2 = get_phrase_s2(tokens, phrase3_start, n)

    # S₂ at kireji token itself
    kireji_s2 = tokens[main_cut_idx]['s2']

    # S₂ at tokens immediately after kireji (+1, +2, +3, skipping newlines)
    post_cut_s2 = []
    j = main_cut_idx + 1
    while j < n and len(post_cut_s2) < 4:
        if '\n' not in tokens[j]['token']:
            post_cut_s2.append(tokens[j]['s2'])
        j += 1

    # S₂ at tokens immediately before kireji (-1, -2, -3, skipping newlines)
    pre_cut_s2 = []
    j = main_cut_idx - 1
    while j >= 0 and len(pre_cut_s2) < 4:
        if '\n' not in tokens[j]['token']:
            pre_cut_s2.append(tokens[j]['s2'])
        j -= 1

    # Overall poem stats
    all_s2 = [t['s2'] for t in tokens if '\n' not in t['token']]
    poem_baseline = np.mean(all_s2) if all_s2 else 0

    # Check if this is an individual haiku (not a grouped "Three Haiku" entry)
    is_individual = 'Three' not in meta['title']

    return {
        'title': meta['title'],
        'author': meta['author'],
        'year': meta.get('year', 0),
        'cut_type': cut_type,
        'cut_position': main_cut_idx,
        'n_tokens': n,
        'poem_baseline': poem_baseline,
        'kireji_s2': kireji_s2,
        'phrase1_s2': phrase1_s2,
        'phrase3_s2': phrase3_s2,
        'post_cut_mean': np.mean(post_cut_s2) if post_cut_s2 else None,
        'post_cut_+1': post_cut_s2[0] if post_cut_s2 else None,
        'pre_cut_mean': np.mean(pre_cut_s2) if pre_cut_s2 else None,
        'is_individual': is_individual,
    }

def main():
    data = load_data()

    # Get all haiku
    haiku_poems = [d for d in data if 'haiku' in str(d['metadata']).lower()]
    print(f"Total haiku in corpus: {len(haiku_poems)}")

    results = []
    for poem_data in haiku_poems:
        r = analyze_haiku(poem_data)
        if r:
            results.append(r)

    print(f"\nAnalyzed: {len(results)} haiku")

    # ── Print per-poem breakdown ──
    print("\n" + "="*70)
    print("PER-HAIKU KIREJI ANALYSIS")
    print("="*70)
    header = f"{'Title':<40} {'Cut':10} {'Baseline':8} {'Kireji S₂':9} {'Phrase1':7} {'Phrase3':7} {'Post+1':7}"
    print(header)
    print("-"*70)
    for r in sorted(results, key=lambda x: x['year'] or 0):
        p1 = f"{r['phrase1_s2']:+.2f}" if r['phrase1_s2'] is not None else "  N/A "
        p3 = f"{r['phrase3_s2']:+.2f}" if r['phrase3_s2'] is not None else "  N/A "
        p_plus1 = f"{r['post_cut_+1']:+.2f}" if r['post_cut_+1'] is not None else "  N/A "
        print(f"{r['title'][:38]:<40} {r['cut_type']:<10} {r['poem_baseline']:+.2f}   "
              f"{r['kireji_s2']:+.2f}    {p1}  {p3}  {p_plus1}")

    # ── Aggregate statistics ──
    print("\n" + "="*70)
    print("AGGREGATE STATISTICS")
    print("="*70)

    # Only use individual haiku (not grouped three-haiku poems)
    individual = [r for r in results if r['is_individual']]
    all_r = results

    for label, group in [("All haiku (incl. grouped)", all_r), ("Individual haiku only", individual)]:
        phrase1_vals = [r['phrase1_s2'] for r in group if r['phrase1_s2'] is not None]
        phrase3_vals = [r['phrase3_s2'] for r in group if r['phrase3_s2'] is not None]
        kireji_vals = [r['kireji_s2'] for r in group]
        post1_vals = [r['post_cut_+1'] for r in group if r['post_cut_+1'] is not None]
        baseline_vals = [r['poem_baseline'] for r in group]

        print(f"\n  {label} (n={len(group)}):")
        print(f"    Poem baseline (mean S₂ excl. newlines): {np.mean(baseline_vals):+.3f}")
        print(f"    Phrase 1 (pre-kireji image) mean S₂:    {np.mean(phrase1_vals):+.3f}")
        print(f"    Phrase 3 (post-kireji image) mean S₂:   {np.mean(phrase3_vals):+.3f}")
        print(f"    Kireji token itself mean S₂:            {np.mean(kireji_vals):+.3f}")
        print(f"    Post-kireji +1 token mean S₂:           {np.mean(post1_vals):+.3f}")

        # Test: is phrase3 more or less predictable than phrase1?
        if phrase1_vals and phrase3_vals and len(phrase1_vals) == len(phrase3_vals):
            diffs = [p3 - p1 for p1, p3 in zip(phrase1_vals, phrase3_vals)]
            print(f"    Phrase3 - Phrase1 (juxtaposition gap): {np.mean(diffs):+.3f}")

    # ── Cut type breakdown ──
    print("\n" + "="*70)
    print("BY CUT TYPE")
    print("="*70)
    cut_groups = defaultdict(list)
    for r in results:
        cut_groups[r['cut_type']].append(r)

    for cut_type, group in sorted(cut_groups.items()):
        kireji_vals = [r['kireji_s2'] for r in group]
        post1_vals = [r['post_cut_+1'] for r in group if r['post_cut_+1'] is not None]
        baseline_vals = [r['poem_baseline'] for r in group]
        print(f"\n  Cut type: '{cut_type}' (n={len(group)}):")
        print(f"    Kireji S₂: {np.mean(kireji_vals):+.3f}  (vs baseline {np.mean(baseline_vals):+.3f})")
        print(f"    Post +1 S₂: {np.mean(post1_vals):+.3f}")

    # ── Conservation principle test ──
    print("\n" + "="*70)
    print("CONSERVATION PRINCIPLE TEST")
    print("="*70)
    print("(From spike_symmetry.py: pre-area ≈ post-area at global level)")
    print()

    for r in results:
        if r['pre_cut_mean'] is not None and r['post_cut_mean'] is not None:
            asymmetry = r['post_cut_mean'] - r['pre_cut_mean']
            direction = "setup-dominant" if asymmetry < 0 else "reverb-dominant"
            print(f"  {r['title'][:45]:<47}: asym={asymmetry:+.3f} ({direction})")

    pre_means = [r['pre_cut_mean'] for r in results if r['pre_cut_mean'] is not None]
    post_means = [r['post_cut_mean'] for r in results if r['post_cut_mean'] is not None]
    if pre_means and post_means:
        print(f"\n  Global kireji pre-mean:  {np.mean(pre_means):+.3f}")
        print(f"  Global kireji post-mean: {np.mean(post_means):+.3f}")
        print(f"  Global asymmetry:        {np.mean(post_means) - np.mean(pre_means):+.3f}")

    # Return for saving
    return results

if __name__ == "__main__":
    results = main()
