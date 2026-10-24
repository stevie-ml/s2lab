"""
Clerihew vs Limerick: Two Constrained Forms with Opposite S2 Profiles

Both are strict formal constraints, yet they occupy opposite ends of the S2 spectrum:
  - clerihew: +0.35 artifact-free S2 (among the HIGHEST of any era)
  - limerick: -0.66 artifact-free S2 (among the LOWEST of any era)

This experiment investigates WHY.

Hypotheses:
  1. Proper nouns drive high S2 in clerihews (biographical subject + their details)
  2. Strong meter in limericks suppresses S2 (anapestic rhythm makes tokens predictable)
  3. Edward Lear's limericks (more idiosyncratic) have higher S2 than traditional ones
  4. Rhyme slot position accounts for high-S2 moments in both forms
"""

import json
import re
from pathlib import Path
import statistics

RESULTS_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"

def load_corpus():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def artifact_free(tokens):
    """Filter out stanza-break artifact positions."""
    return [t for t in tokens if t.get('p_newline', 1.0) < 0.9]

def token_is_proper_noun(token_str, alternatives):
    """
    Heuristic: token starts with capital letter and model didn't predict it with capital.
    Also catches parts of proper nouns (subword tokens that are part of a name).
    """
    tok = token_str.strip()
    if not tok:
        return False
    # Capital-initial token
    if tok[0].isupper():
        # Check if model's top predictions were lowercase (meaning it didn't expect a name)
        top_alts = [a['token'].strip() for a in alternatives[:3]]
        top_caps = sum(1 for a in top_alts if a and a[0].isupper())
        return top_caps < 2  # model mostly didn't predict capitals
    return False

def pos_category(pos_in_poem, total_tokens):
    """Rough position categories."""
    frac = pos_in_poem / max(total_tokens - 1, 1)
    if frac < 0.25:
        return 'opening'
    elif frac < 0.5:
        return 'early_middle'
    elif frac < 0.75:
        return 'late_middle'
    else:
        return 'closing'

def analyze_form(poems, form_name):
    """Detailed analysis of S2 patterns in a poetic form."""
    all_clean = []
    proper_noun_s2 = []
    other_s2 = []
    high_s2_examples = []
    positional_s2 = {'opening': [], 'early_middle': [], 'late_middle': [], 'closing': []}

    for poem in poems:
        tokens = poem['tokens']
        clean = artifact_free(tokens)
        n = len(clean)
        s2_values = [t['s2'] for t in clean]
        all_clean.extend(s2_values)

        for i, t in enumerate(clean):
            pos_cat = pos_category(i, n)
            positional_s2[pos_cat].append(t['s2'])

            if token_is_proper_noun(t['token'], t.get('alternatives', [])):
                proper_noun_s2.append(t['s2'])
            else:
                other_s2.append(t['s2'])

            if t['s2'] > 5.0:
                high_s2_examples.append({
                    'poem': poem['metadata']['title'],
                    'token': t['token'],
                    's2': t['s2'],
                    'entropy': t['entropy'],
                    'context': t.get('context_before', '')[-30:],
                    'predicted': [a['token'] for a in t.get('alternatives', [])[:3]],
                    'is_proper': token_is_proper_noun(t['token'], t.get('alternatives', []))
                })

    result = {
        'form': form_name,
        'n_poems': len(poems),
        'n_clean_tokens': len(all_clean),
        'mean_s2': statistics.mean(all_clean) if all_clean else 0,
        'median_s2': statistics.median(all_clean) if all_clean else 0,
        'stdev_s2': statistics.stdev(all_clean) if len(all_clean) > 1 else 0,
        'pos_s2_ratio': sum(1 for x in all_clean if x > 0) / len(all_clean) if all_clean else 0,
        'mean_proper_noun_s2': statistics.mean(proper_noun_s2) if proper_noun_s2 else None,
        'mean_other_s2': statistics.mean(other_s2) if other_s2 else None,
        'n_proper_noun_tokens': len(proper_noun_s2),
        'proper_noun_pct': 100 * len(proper_noun_s2) / len(all_clean) if all_clean else 0,
        'positional_means': {k: statistics.mean(v) if v else None for k, v in positional_s2.items()},
        'high_s2_examples': sorted(high_s2_examples, key=lambda x: -x['s2'])[:10]
    }
    return result

def analyze_limerick_subtypes(limericks):
    """Compare Edward Lear's limericks vs anonymous/traditional."""
    lear = [p for p in limericks if 'Lear' in p['metadata'].get('author', '')]
    other = [p for p in limericks if 'Lear' not in p['metadata'].get('author', '')]

    def mean_clean_s2(poems):
        vals = []
        for p in poems:
            vals.extend([t['s2'] for t in artifact_free(p['tokens'])])
        return statistics.mean(vals) if vals else None

    return {
        'lear': {
            'n': len(lear),
            'mean_s2': mean_clean_s2(lear),
            'poems': [p['metadata']['title'] for p in lear]
        },
        'other': {
            'n': len(other),
            'mean_s2': mean_clean_s2(other),
            'poems': [p['metadata']['title'] for p in other]
        }
    }

def main():
    data = load_corpus()
    clerihews = [p for p in data if p['metadata']['era'] == 'clerihew']
    limericks = [p for p in data if p['metadata']['era'] == 'limerick']

    print(f"Clerihews: n={len(clerihews)}")
    print(f"Limericks: n={len(limericks)}")
    print()

    c_result = analyze_form(clerihews, 'clerihew')
    l_result = analyze_form(limericks, 'limerick')

    print("=== ARTIFACT-FREE S2 COMPARISON ===")
    print(f"{'Metric':<30} {'Clerihew':>12} {'Limerick':>12}")
    print(f"{'Mean S2':<30} {c_result['mean_s2']:>12.3f} {l_result['mean_s2']:>12.3f}")
    print(f"{'Median S2':<30} {c_result['median_s2']:>12.3f} {l_result['median_s2']:>12.3f}")
    print(f"{'Std S2':<30} {c_result['stdev_s2']:>12.3f} {l_result['stdev_s2']:>12.3f}")
    print(f"{'Pos S2 ratio':<30} {c_result['pos_s2_ratio']:>12.1%} {l_result['pos_s2_ratio']:>12.1%}")
    print()

    print("=== PROPER NOUN EFFECT ===")
    print(f"{'Metric':<35} {'Clerihew':>12} {'Limerick':>12}")
    print(f"{'Proper noun % of tokens':<35} {c_result['proper_noun_pct']:>11.1f}% {l_result['proper_noun_pct']:>11.1f}%")
    c_pn = c_result['mean_proper_noun_s2']
    l_pn = l_result['mean_proper_noun_s2']
    c_ot = c_result['mean_other_s2']
    l_ot = l_result['mean_other_s2']
    print(f"{'Mean S2 (proper nouns)':<35} {c_pn:>12.3f}" if c_pn else f"{'Mean S2 (proper nouns)':<35} {'N/A':>12}" + f" {l_pn:>12.3f}" if l_pn else "  N/A")
    if c_pn:
        print(f"  Clerihew proper nouns: {c_pn:.3f}")
    if l_pn:
        print(f"  Limerick proper nouns: {l_pn:.3f}")
    if c_ot:
        print(f"  Clerihew other tokens: {c_ot:.3f}")
    if l_ot:
        print(f"  Limerick other tokens: {l_ot:.3f}")
    print()

    print("=== POSITIONAL S2 PROFILES ===")
    positions = ['opening', 'early_middle', 'late_middle', 'closing']
    print(f"{'Position':<20} {'Clerihew':>12} {'Limerick':>12}")
    for pos in positions:
        cv = c_result['positional_means'].get(pos)
        lv = l_result['positional_means'].get(pos)
        cs = f"{cv:.3f}" if cv is not None else "N/A"
        ls = f"{lv:.3f}" if lv is not None else "N/A"
        print(f"{pos:<20} {cs:>12} {ls:>12}")
    print()

    print("=== TOP CLERIHEW HIGH-S2 MOMENTS ===")
    for ex in c_result['high_s2_examples'][:8]:
        pn_flag = " [PROPER NOUN]" if ex['is_proper'] else ""
        print(f"  [{ex['s2']:+.2f}] \"{ex['token']}\"{pn_flag}")
        print(f"    ctx: \"{ex['context']}\" → model predicted: {ex['predicted']}")
        print(f"    poem: {ex['poem']}")
    print()

    print("=== TOP LIMERICK HIGH-S2 MOMENTS ===")
    for ex in l_result['high_s2_examples'][:8]:
        pn_flag = " [PROPER NOUN]" if ex['is_proper'] else ""
        print(f"  [{ex['s2']:+.2f}] \"{ex['token']}\"{pn_flag}")
        print(f"    ctx: \"{ex['context']}\" → model predicted: {ex['predicted']}")
        print(f"    poem: {ex['poem']}")
    print()

    print("=== LEAR vs TRADITIONAL LIMERICKS ===")
    subtypes = analyze_limerick_subtypes(limericks)
    print(f"Edward Lear (n={subtypes['lear']['n']}): mean artifact-free S2 = {subtypes['lear']['mean_s2']:.3f}")
    print(f"Other/traditional (n={subtypes['other']['n']}): mean artifact-free S2 = {subtypes['other']['mean_s2']:.3f}")
    print("Lear poems:", subtypes['lear']['poems'])
    print("Other poems:", subtypes['other']['poems'])

    # Save results
    output = {
        'clerihew': c_result,
        'limerick': l_result,
        'limerick_subtypes': subtypes
    }
    out_path = Path(__file__).parent.parent / "results" / "clerihew_vs_limerick.json"
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")

if __name__ == '__main__':
    main()
