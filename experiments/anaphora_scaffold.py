"""
Anaphora as Information Scaffold
=================================
Hypothesis: In anaphoric poetry (repeated line-openings), GPT-2 'learns'
the repeated phrase within the poem. Successive repetitions of the scaffold
should show DECREASING entropy (model grows more confident) while the
varied content after the scaffold maintains HIGH S2 (the semantic surprise
is preserved in the variation).

This tests whether anaphora is an 'information deal': the poet trades
certainty on the scaffold to build tension for the variation.
"""

import json
import sys
import re
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"

def load_corpus():
    with open(CORPUS_PATH) as f:
        return json.load(f)

def find_tokens_matching(tokens, target_text):
    """Find all tokens whose text (stripped) matches target_text."""
    matches = []
    for tok in tokens:
        if tok['token'].strip() == target_text.strip():
            matches.append(tok)
    return matches

def find_anaphoric_sequences(tokens, scaffold_texts):
    """
    Given a list of scaffold token-texts (e.g. ['I', 'prefer']),
    find all positions where the scaffold appears in the token list.
    Returns list of occurrences, each as:
      {scaffold_tokens, variation_tokens (next 3 after scaffold)}
    """
    scaffold_len = len(scaffold_texts)
    occurrences = []
    i = 0
    while i < len(tokens) - scaffold_len:
        window = [tokens[i+j]['token'].strip() for j in range(scaffold_len)]
        if window == scaffold_texts:
            scaffold_slice = tokens[i:i+scaffold_len]
            variation_slice = tokens[i+scaffold_len:i+scaffold_len+3]
            occurrences.append({
                'position': tokens[i]['position'],
                'scaffold': scaffold_slice,
                'variation': variation_slice,
                'occurrence_num': len(occurrences) + 1
            })
        i += 1
    return occurrences

def analyze_poem(item, scaffold_texts, poem_label):
    tokens = item['tokens']
    # Filter stanza-break artifact (p_newline < 0.9)
    clean = [t for t in tokens if t.get('p_newline', 0) < 0.9]

    occurrences = find_anaphoric_sequences(tokens, scaffold_texts)
    if len(occurrences) < 3:
        return None

    print(f"\n{'='*60}")
    print(f"POEM: {poem_label}")
    print(f"Scaffold: {' '.join(scaffold_texts)!r}")
    print(f"Occurrences found: {len(occurrences)}")

    results = []
    for occ in occurrences:
        scaffold_entropy = [t['entropy'] for t in occ['scaffold'] if t.get('p_newline',0) < 0.9]
        scaffold_s2 = [t['s2'] for t in occ['scaffold'] if t.get('p_newline',0) < 0.9]
        variation_s2 = [t['s2'] for t in occ['variation'] if t.get('p_newline',0) < 0.9]
        variation_entropy = [t['entropy'] for t in occ['variation'] if t.get('p_newline',0) < 0.9]

        avg_scaffold_entropy = sum(scaffold_entropy)/len(scaffold_entropy) if scaffold_entropy else None
        avg_scaffold_s2 = sum(scaffold_s2)/len(scaffold_s2) if scaffold_s2 else None
        avg_variation_s2 = sum(variation_s2)/len(variation_s2) if variation_s2 else None
        avg_variation_entropy = sum(variation_entropy)/len(variation_entropy) if variation_entropy else None

        var_tokens_text = ' '.join([t['token'] for t in occ['variation']])

        print(f"\n  Occurrence #{occ['occurrence_num']} at pos {occ['position']}:")
        print(f"    Scaffold entropy: {avg_scaffold_entropy:.3f}" if avg_scaffold_entropy is not None else "    Scaffold entropy: N/A")
        print(f"    Scaffold S2:      {avg_scaffold_s2:.3f}" if avg_scaffold_s2 is not None else "    Scaffold S2: N/A")
        print(f"    Variation tokens: {var_tokens_text!r}")
        print(f"    Variation S2:     {avg_variation_s2:.3f}" if avg_variation_s2 is not None else "    Variation S2: N/A")
        print(f"    Variation entropy:{avg_variation_entropy:.3f}" if avg_variation_entropy is not None else "    Variation entropy: N/A")

        results.append({
            'occurrence_num': occ['occurrence_num'],
            'scaffold_entropy': avg_scaffold_entropy,
            'scaffold_s2': avg_scaffold_s2,
            'variation_s2': avg_variation_s2,
            'variation_entropy': avg_variation_entropy,
            'variation_text': var_tokens_text.strip(),
        })

    return results

def compute_trend(values):
    """Simple linear trend: positive means increasing, negative decreasing."""
    n = len([v for v in values if v is not None])
    if n < 2:
        return 0
    vals = [v for v in values if v is not None]
    mid = n // 2
    first_half = sum(vals[:mid]) / mid
    second_half = sum(vals[mid:]) / (n - mid)
    return second_half - first_half

def main():
    data = load_corpus()

    # Poems and their anaphoric scaffolds
    targets = [
        {
            'title_fragment': 'Possibilities',
            'scaffold': ['I', 'prefer'],
            'label': 'Szymborska - "Possibilities" (I prefer...)'
        },
        {
            'title_fragment': 'Incantation',
            'scaffold': ['blessed', 'are'],
            'label': 'Clifton - "Incantation" (blessed are...)'
        },
        {
            'title_fragment': 'Homage to My Hips',
            'scaffold': ['these', 'hips'],
            'label': 'Clifton - "Homage to My Hips" (these hips...)'
        },
        {
            'title_fragment': 'Oh Shenandoah',
            'scaffold': ['Oh', 'Shenandoah'],
            'label': 'Traditional - "Oh Shenandoah" (Oh Shenandoah...)'
        },
        {
            'title_fragment': 'Harlem',
            'scaffold': ['like', 'a'],
            'label': 'Hughes - "Harlem" (like a...)'
        },
        {
            'title_fragment': 'Recessional',
            'scaffold': ['Lest', 'we'],
            'label': 'Kipling - "Recessional" (Lest we...)'
        },
    ]

    all_results = {}

    for target in targets:
        item = next((d for d in data if target['title_fragment'] in d.get('metadata',{}).get('title','')), None)
        if item is None:
            print(f"NOT FOUND: {target['title_fragment']}")
            continue

        res = analyze_poem(item, target['scaffold'], target['label'])
        if res:
            all_results[target['label']] = res

    print("\n\n" + "="*70)
    print("SUMMARY: Scaffold Entropy Trend Across Occurrences")
    print("="*70)
    print(f"{'Poem':<50} {'Scaffold H trend':>17} {'Variation S2 avg':>17}")
    print("-"*86)

    for label, results in all_results.items():
        entropy_vals = [r['scaffold_entropy'] for r in results]
        var_s2_vals = [r['variation_s2'] for r in results if r['variation_s2'] is not None]

        trend = compute_trend(entropy_vals)
        avg_var_s2 = sum(var_s2_vals)/len(var_s2_vals) if var_s2_vals else 0

        direction = "↓ decreasing" if trend < -0.2 else ("↑ increasing" if trend > 0.2 else "→ flat")
        print(f"  {label[:48]:<48} {direction:>17} {avg_var_s2:>+15.3f}")

    # Hypothesis test: does scaffold entropy decrease?
    print("\n\nHYPOTHESIS TEST")
    print("-"*50)

    first_occ_entropy = []
    last_occ_entropy = []
    first_var_s2 = []
    last_var_s2 = []

    for label, results in all_results.items():
        if len(results) >= 3:
            first_occ_entropy.append(results[0]['scaffold_entropy'])
            last_occ_entropy.append(results[-1]['scaffold_entropy'])
            if results[0]['variation_s2'] is not None:
                first_var_s2.append(results[0]['variation_s2'])
            if results[-1]['variation_s2'] is not None:
                last_var_s2.append(results[-1]['variation_s2'])

    if first_occ_entropy and last_occ_entropy:
        avg_first_h = sum(x for x in first_occ_entropy if x) / len([x for x in first_occ_entropy if x])
        avg_last_h = sum(x for x in last_occ_entropy if x) / len([x for x in last_occ_entropy if x])
        print(f"Avg scaffold entropy, 1st occurrence:  {avg_first_h:.3f} bits")
        print(f"Avg scaffold entropy, last occurrence: {avg_last_h:.3f} bits")
        print(f"Change: {avg_last_h - avg_first_h:+.3f} bits")
        if avg_last_h < avg_first_h:
            print("CONFIRMED: Scaffold entropy DECREASES over repetitions.")
        else:
            print("DISCONFIRMED: Scaffold entropy does NOT decrease.")

    if first_var_s2 and last_var_s2:
        avg_first_vs = sum(first_var_s2) / len(first_var_s2)
        avg_last_vs = sum(last_var_s2) / len(last_var_s2)
        print(f"\nAvg variation S2, 1st occurrence:  {avg_first_vs:.3f} bits")
        print(f"Avg variation S2, last occurrence: {avg_last_vs:.3f} bits")
        print(f"Change: {avg_last_vs - avg_first_vs:+.3f} bits")

    # Save results for finding
    with open('results/anaphora_scaffold.json', 'w') as f:
        json.dump({
            'description': 'Anaphora scaffold analysis: entropy and S2 by occurrence number',
            'poems_analyzed': list(all_results.keys()),
            'results': all_results,
            'summary': {
                'avg_first_scaffold_entropy': avg_first_h if first_occ_entropy else None,
                'avg_last_scaffold_entropy': avg_last_h if last_occ_entropy else None,
            }
        }, f, indent=2)
    print("\nResults saved to results/anaphora_scaffold.json")

if __name__ == '__main__':
    main()
