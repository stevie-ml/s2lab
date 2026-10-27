"""
Anaphora Entropy Decay: Curve Shape Analysis
============================================
Follow-up to anaphora_scaffold.py (2026-10-27).

That experiment found that in Szymborska's "Possibilities" (12 reps of "I prefer"),
scaffold entropy dropped 73% from first to last occurrence. But what SHAPE does
the decay follow? Is it:
  - Exponential decay: H(n) = H0 * exp(-kn)  [fast early, slow late]
  - Power law: H(n) = H0 * n^(-alpha)         [consistent ratio per doubling]
  - Logarithmic: H(n) = H0 - k*log(n)         [slow decay throughout]
  - Hyperbolic: H(n) = H0 / (1 + k*n)         [fast early plateau]

We test this by adding three new long-anaphora poems:
  - Psalm 136 KJV: 26 repetitions of "for his mercy endureth for ever"
  - Song of Myself Section 15: 22+ lines starting with "The..."
  - She Had Some Horses: ~15 "She had horses" instances

We also revisit Szymborska "Possibilities" (12 reps) from existing data.

Method:
  - Extract entropy at each scaffold occurrence (filtered p_newline < 0.9)
  - Fit 4 curve models using least-squares
  - Rank by R^2
  - Report: what learning law best describes within-poem GPT-2 context learning?
"""

import json
import math
import sys
import re
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"

def load_corpus():
    with open(CORPUS_PATH) as f:
        return json.load(f)

def find_scaffold_occurrences(tokens, scaffold_texts, min_occurrences=4, p_newline_threshold=0.9):
    """Find all positions where scaffold_texts appear as a token sequence."""
    scaffold_len = len(scaffold_texts)
    occurrences = []
    i = 0
    while i < len(tokens) - scaffold_len:
        window = [tokens[i+j]['token'].strip() for j in range(scaffold_len)]
        if window == scaffold_texts:
            scaffold_slice = tokens[i:i+scaffold_len]
            # Filter by newline artifact
            clean_scaffold = [t for t in scaffold_slice if t.get('p_newline', 0) < p_newline_threshold]
            if clean_scaffold:
                avg_h = sum(t['entropy'] for t in clean_scaffold) / len(clean_scaffold)
                # The key token to track: the LAST token of the scaffold (most diagnostic)
                # For "I prefer": track "prefer" entropy specifically
                last_tok = clean_scaffold[-1]
                occurrences.append({
                    'occurrence_num': len(occurrences) + 1,
                    'position': tokens[i]['position'],
                    'avg_scaffold_entropy': avg_h,
                    'last_token_entropy': last_tok['entropy'],
                    'last_token_text': last_tok['token'].strip(),
                    'full_scaffold': ' '.join(t['token'] for t in scaffold_slice),
                })
        i += 1
    return occurrences if len(occurrences) >= min_occurrences else []


def fit_decay_models(occurrences):
    """
    Fit 4 decay models to (n, H) data using grid search for parameters.
    Returns dict of {model_name: (params, r2, predicted_values)}.
    """
    ns = [o['occurrence_num'] for o in occurrences]
    hs = [o['avg_scaffold_entropy'] for o in occurrences]
    H0 = hs[0]
    H_mean = sum(hs) / len(hs)
    ss_tot = sum((h - H_mean)**2 for h in hs)

    results = {}

    # 1. Exponential decay: H(n) = A * exp(-k * n) + C
    best_r2 = -999
    best_params = None
    best_pred = None
    for k in [x/100 for x in range(1, 200)]:
        for C_frac in [x/20 for x in range(0, 20)]:
            C = H0 * C_frac
            A = H0 - C
            pred = [A * math.exp(-k * n) + C for n in ns]
            ss_res = sum((h - p)**2 for h, p in zip(hs, pred))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            if r2 > best_r2:
                best_r2 = r2
                best_params = {'A': A, 'k': k, 'C': C}
                best_pred = pred
    results['exponential'] = (best_params, best_r2, best_pred)

    # 2. Power law: H(n) = H0 * n^(-alpha) + C
    best_r2 = -999
    for alpha in [x/20 for x in range(1, 60)]:
        for C_frac in [x/20 for x in range(0, 20)]:
            C = H0 * C_frac
            A = H0 - C
            pred = [A * (n ** (-alpha)) + C for n in ns]
            ss_res = sum((h - p)**2 for h, p in zip(hs, pred))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            if r2 > best_r2:
                best_r2 = r2
                best_params = {'A': A, 'alpha': alpha, 'C': C}
                best_pred = pred
    results['power_law'] = (best_params, best_r2, best_pred)

    # 3. Logarithmic: H(n) = H0 - k * log(n)
    best_r2 = -999
    for k in [x/100 for x in range(1, 500)]:
        pred = [max(0.1, H0 - k * math.log(n)) for n in ns]
        ss_res = sum((h - p)**2 for h, p in zip(hs, pred))
        r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
        if r2 > best_r2:
            best_r2 = r2
            best_params = {'H0': H0, 'k': k}
            best_pred = pred
    results['logarithmic'] = (best_params, best_r2, best_pred)

    # 4. Hyperbolic: H(n) = H0 / (1 + k*n) + C  (plateau model)
    best_r2 = -999
    for k in [x/100 for x in range(1, 300)]:
        for C_frac in [x/20 for x in range(0, 20)]:
            C = H0 * C_frac
            A = H0 - C
            pred = [A / (1 + k * n) + C for n in ns]
            ss_res = sum((h - p)**2 for h, p in zip(hs, pred))
            r2 = 1 - ss_res/ss_tot if ss_tot > 0 else 0
            if r2 > best_r2:
                best_r2 = r2
                best_params = {'A': A, 'k': k, 'C': C}
                best_pred = pred
    results['hyperbolic'] = (best_params, best_r2, best_pred)

    return results


def compute_decay_stats(occurrences):
    hs = [o['avg_scaffold_entropy'] for o in occurrences]
    first_half = hs[:len(hs)//2]
    second_half = hs[len(hs)//2:]
    first_avg = sum(first_half)/len(first_half)
    second_avg = sum(second_half)/len(second_half)
    total_drop = hs[0] - hs[-1]
    pct_drop = 100 * total_drop / hs[0] if hs[0] > 0 else 0
    # Slope: how many bits dropped per occurrence on average
    slope = total_drop / (len(hs) - 1) if len(hs) > 1 else 0
    # Early vs late slope
    early_slope = (hs[0] - hs[len(hs)//2]) / (len(hs)//2) if len(hs) > 1 else 0
    late_slope = (hs[len(hs)//2] - hs[-1]) / (len(hs) - len(hs)//2) if len(hs) > 1 else 0
    acceleration = early_slope / late_slope if late_slope > 0 else float('inf')
    return {
        'n_occurrences': len(hs),
        'H_first': hs[0],
        'H_last': hs[-1],
        'total_drop': total_drop,
        'pct_drop': pct_drop,
        'avg_slope': slope,
        'early_slope': early_slope,
        'late_slope': late_slope,
        'acceleration': acceleration,  # >1 means learning is faster early than late
    }


def analyze_poem(data, title_fragment, scaffold_texts, label):
    item = next((d for d in data if title_fragment in d.get('metadata', {}).get('title', '')), None)
    if item is None:
        print(f"NOT FOUND: {title_fragment}")
        return None

    tokens = item['tokens']
    occurrences = find_scaffold_occurrences(tokens, scaffold_texts)

    if not occurrences:
        # Try case-insensitive matching
        scaffold_lower = [s.lower() for s in scaffold_texts]
        occurrences_ci = []
        scaffold_len = len(scaffold_texts)
        for i in range(len(tokens) - scaffold_len):
            window = [tokens[i+j]['token'].strip().lower() for j in range(scaffold_len)]
            if window == scaffold_lower:
                scaffold_slice = tokens[i:i+scaffold_len]
                clean_scaffold = [t for t in scaffold_slice if t.get('p_newline', 0) < 0.9]
                if clean_scaffold:
                    avg_h = sum(t['entropy'] for t in clean_scaffold) / len(clean_scaffold)
                    occurrences_ci.append({
                        'occurrence_num': len(occurrences_ci) + 1,
                        'position': tokens[i]['position'],
                        'avg_scaffold_entropy': avg_h,
                        'last_token_entropy': clean_scaffold[-1]['entropy'],
                        'last_token_text': clean_scaffold[-1]['token'].strip(),
                    })
        occurrences = occurrences_ci

    if len(occurrences) < 4:
        print(f"\n{label}: only {len(occurrences)} occurrences found (need ≥4), skipping")
        return None

    print(f"\n{'='*65}")
    print(f"POEM: {label}")
    print(f"Scaffold: {scaffold_texts!r}  |  Occurrences: {len(occurrences)}")
    print(f"\n  n  | Avg H  | Last-tok H | Last-tok")
    print(f"  ---|--------|------------|----------")
    for o in occurrences:
        print(f"  {o['occurrence_num']:2d} | {o['avg_scaffold_entropy']:5.3f}  | "
              f"{o['last_token_entropy']:10.3f} | {o.get('last_token_text', '?')!r}")

    stats = compute_decay_stats(occurrences)
    models = fit_decay_models(occurrences)

    print(f"\n  DECAY STATS:")
    print(f"    H(first) = {stats['H_first']:.3f},  H(last) = {stats['H_last']:.3f}")
    print(f"    Total drop: {stats['total_drop']:.3f} bits ({stats['pct_drop']:.1f}%)")
    print(f"    Avg slope:  {stats['avg_slope']:.4f} bits/occurrence")
    print(f"    Early slope: {stats['early_slope']:.4f}  Late slope: {stats['late_slope']:.4f}")
    print(f"    Acceleration ratio: {stats['acceleration']:.2f}x  (>1 = front-loaded learning)")

    print(f"\n  CURVE FIT (R²):")
    for model_name, (params, r2, _) in sorted(models.items(), key=lambda x: -x[1][1]):
        print(f"    {model_name:15s}: R² = {r2:.4f}   params = {params}")

    best_model = max(models.items(), key=lambda x: x[1][1])
    print(f"\n  BEST FIT: {best_model[0]} (R² = {best_model[1][1]:.4f})")

    return {
        'label': label,
        'scaffold': scaffold_texts,
        'occurrences': occurrences,
        'stats': stats,
        'best_model': best_model[0],
        'best_r2': best_model[1][1],
        'all_model_r2': {k: v[1] for k, v in models.items()},
        'models': {k: {'params': v[0], 'r2': v[1]} for k, v in models.items()},
    }


def main():
    data = load_corpus()

    targets = [
        {
            'title_fragment': 'Possibilities',
            'scaffold': ['I', 'prefer'],
            'label': 'Szymborska "Possibilities" (I prefer...)',
        },
        {
            'title_fragment': 'Psalm 136',
            'scaffold': ['for', 'his', 'mercy'],
            'label': 'Psalm 136 KJV (for his mercy...)',
        },
        {
            'title_fragment': 'Song of Myself (section 15',
            'scaffold': ['The'],
            'label': 'Whitman "Song of Myself" Sec. 15 (The...)',
        },
        {
            'title_fragment': 'She Had Some Horses',
            'scaffold': ['She', 'had', 'horses'],
            'label': 'Harjo "She Had Some Horses" (She had horses...)',
        },
        {
            'title_fragment': 'Recessional',
            'scaffold': ['Lest', 'we'],
            'label': 'Kipling "Recessional" (Lest we...)',
        },
        {
            'title_fragment': 'Still I Rise',
            'scaffold': ['I', "'ll"],
            'label': 'Angelou "Still I Rise" (I\'ll...)',
        },
    ]

    all_results = {}
    for target in targets:
        res = analyze_poem(data, target['title_fragment'], target['scaffold'], target['label'])
        if res:
            all_results[target['label']] = res

    # Cross-poem summary
    print(f"\n\n{'='*65}")
    print("CROSS-POEM SUMMARY: ENTROPY DECAY CURVES")
    print(f"{'='*65}")
    print(f"{'Poem':<45} | {'N':>3} | {'H_1':>5} | {'H_N':>5} | {'Drop%':>6} | {'Accel':>6} | {'Best Model'}")
    print(f"{'-'*45}-+-{'-'*3}-+-{'-'*5}-+-{'-'*5}-+-{'-'*6}-+-{'-'*6}-+-----------")
    for label, res in all_results.items():
        s = res['stats']
        print(f"{label[:45]:<45} | {s['n_occurrences']:>3} | {s['H_first']:>5.2f} | "
              f"{s['H_last']:>5.2f} | {s['pct_drop']:>5.1f}% | {s['acceleration']:>6.2f}x | {res['best_model']}")

    # Model ranking across all poems
    print(f"\n\nMODEL RANKINGS (average R² across poems):")
    model_names = ['exponential', 'power_law', 'logarithmic', 'hyperbolic']
    model_r2s = defaultdict(list)
    for res in all_results.values():
        for m in model_names:
            if m in res['all_model_r2']:
                model_r2s[m].append(res['all_model_r2'][m])
    for m in sorted(model_names, key=lambda m: -sum(model_r2s[m])/len(model_r2s[m]) if model_r2s[m] else 0):
        avg_r2 = sum(model_r2s[m])/len(model_r2s[m]) if model_r2s[m] else 0
        print(f"  {m:15s}: avg R² = {avg_r2:.4f}")

    # Save results
    outfile = "findings/anaphora_decay_curve.json"
    with open(outfile, 'w') as f:
        json.dump({k: {kk: vv for kk, vv in v.items() if kk != 'occurrences'}
                   for k, v in all_results.items()}, f, indent=2, default=str)
    print(f"\nResults saved to {outfile}")
    return all_results


if __name__ == '__main__':
    main()
