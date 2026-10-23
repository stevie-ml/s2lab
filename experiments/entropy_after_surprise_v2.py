"""
Entropy After Surprise v2: Partial correlation and conditional analysis.

The v1 finding that S2(t) negatively correlates with Entropy(t+1) is partially
a mathematical consequence: S2 = surprisal - entropy, so very_negative S2 tokens
occur in high-entropy contexts, and entropy persists.

v2 tests: CONTROLLING FOR entropy at t, does S2(t) still affect entropy(t+1)?
This partial correlation is the truly independent empirical finding.

Also: comparing LOW-entropy contexts (model was confident) vs HIGH-entropy contexts
— do poets' creative choices have different cascade effects depending on context certainty?
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/entropy_after_surprise_v2.json"

def pearson_r(xs, ys):
    n = len(xs)
    if n < 5:
        return None
    mx, my = sum(xs)/n, sum(ys)/n
    num = sum((x-mx)*(y-my) for x,y in zip(xs, ys))
    dx = math.sqrt(sum((x-mx)**2 for x in xs))
    dy = math.sqrt(sum((y-my)**2 for y in ys))
    if dx * dy == 0:
        return None
    return num / (dx * dy)

def partial_r(a_vals, b_vals, c_vals):
    """Partial correlation r(A, B | C): correlation of A and B controlling for C."""
    n = len(a_vals)
    if n < 10:
        return None
    # Regress A on C, get residuals
    r_ac = pearson_r(a_vals, c_vals)
    r_bc = pearson_r(b_vals, c_vals)
    if r_ac is None or r_bc is None:
        return None
    # Partial correlation formula: (r_ab - r_ac * r_bc) / sqrt((1 - r_ac^2)(1 - r_bc^2))
    r_ab = pearson_r(a_vals, b_vals)
    if r_ab is None:
        return None
    denom = math.sqrt((1 - r_ac**2) * (1 - r_bc**2))
    if denom == 0:
        return None
    return (r_ab - r_ac * r_bc) / denom

def is_artifact(tok):
    return tok.get('p_newline', 0) > 0.9

def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    all_s2_t = []
    all_ent_t = []
    all_ent_t1 = []
    all_s2_t1 = []

    # Conditional accumulators by entropy context
    low_ent_pairs = []   # entropy(t) < 4  (model was confident)
    mid_ent_pairs = []   # 4 <= entropy(t) < 7
    high_ent_pairs = []  # entropy(t) >= 7  (model was uncertain)

    # Era-level partial correlations
    era_data = defaultdict(list)

    texts_used = 0
    for text in corpus:
        meta = text.get('metadata', {})
        era = meta.get('era', 'unknown')
        tokens = text.get('tokens', [])
        clean = [t for t in tokens if not is_artifact(t)]
        if len(clean) < 10:
            continue
        texts_used += 1

        for i in range(len(clean) - 1):
            t0, t1 = clean[i], clean[i+1]
            s2_t  = t0['s2']
            ent_t  = t0['entropy']
            s2_t1 = t1['s2']
            ent_t1 = t1['entropy']

            all_s2_t.append(s2_t)
            all_ent_t.append(ent_t)
            all_ent_t1.append(ent_t1)
            all_s2_t1.append(s2_t1)

            era_data[era].append((s2_t, ent_t, ent_t1, s2_t1))

            if ent_t < 4:
                low_ent_pairs.append((s2_t, ent_t, ent_t1, s2_t1))
            elif ent_t < 7:
                mid_ent_pairs.append((s2_t, ent_t, ent_t1, s2_t1))
            else:
                high_ent_pairs.append((s2_t, ent_t, ent_t1, s2_t1))

    print(f"Used {texts_used} texts, {len(all_s2_t)} pairs")
    print(f"Context buckets: low={len(low_ent_pairs)}, mid={len(mid_ent_pairs)}, high={len(high_ent_pairs)}")

    # Overall partial correlation: r(S2_t, Entropy_t+1 | Entropy_t)
    pr = partial_r(all_s2_t, all_ent_t1, all_ent_t)
    print(f"\nPartial r(S2_t, Entropy_t+1 | Entropy_t) = {pr:.4f}" if pr else "Partial r = N/A")

    # Conditional analysis: in LOW-entropy contexts (model confident),
    # does high S2 predict higher or lower entropy next?
    def analyze_conditional(pairs, label):
        s2s  = [p[0] for p in pairs]
        ents = [p[1] for p in pairs]
        ent1s= [p[2] for p in pairs]
        s2n  = [p[3] for p in pairs]
        r_raw = pearson_r(s2s, ent1s)
        pr_cond = partial_r(s2s, ent1s, ents)
        # Split into positive/negative S2 within this context
        pos_ent1 = [p[2] for p in pairs if p[0] >= 2.0]
        neg_ent1 = [p[2] for p in pairs if p[0] < 0.0]
        pos_mean = sum(pos_ent1)/len(pos_ent1) if pos_ent1 else None
        neg_mean = sum(neg_ent1)/len(neg_ent1) if neg_ent1 else None
        print(f"\n{label} (n={len(pairs)}, mean_ent_t={sum(ents)/len(ents):.2f}):")
        print(f"  raw r(S2_t, Entropy_t+1) = {r_raw:.4f}" if r_raw else "  raw r = N/A")
        print(f"  partial r(S2_t, Ent_t+1 | Ent_t) = {pr_cond:.4f}" if pr_cond else "  partial r = N/A")
        if pos_mean and neg_mean:
            print(f"  Mean Entropy_t+1 after positive-S2 tokens: {pos_mean:.4f} (n={len(pos_ent1)})")
            print(f"  Mean Entropy_t+1 after negative-S2 tokens: {neg_mean:.4f} (n={len(neg_ent1)})")
            print(f"  Delta (pos-neg): {pos_mean - neg_mean:+.4f}")
        return {
            'n': len(pairs),
            'mean_ent_t': round(sum(ents)/len(ents), 4),
            'r_raw': round(r_raw, 4) if r_raw else None,
            'partial_r': round(pr_cond, 4) if pr_cond else None,
            'mean_ent1_after_pos_s2': round(pos_mean, 4) if pos_mean else None,
            'mean_ent1_after_neg_s2': round(neg_mean, 4) if neg_mean else None,
            'n_pos_s2': len(pos_ent1),
            'n_neg_s2': len(neg_ent1),
        }

    cond_results = {
        'low_entropy_context': analyze_conditional(low_ent_pairs, "LOW entropy context (model confident, entropy_t < 4)"),
        'mid_entropy_context': analyze_conditional(mid_ent_pairs, "MID entropy context (4 <= entropy_t < 7)"),
        'high_entropy_context': analyze_conditional(high_ent_pairs, "HIGH entropy context (model uncertain, entropy_t >= 7)"),
    }

    # Era-level partial correlations
    era_partial = {}
    for era, pairs in era_data.items():
        if len(pairs) < 30:
            continue
        s2s  = [p[0] for p in pairs]
        ents = [p[1] for p in pairs]
        ent1s= [p[2] for p in pairs]
        pr_e = partial_r(s2s, ent1s, ents)
        era_partial[era] = {
            'n': len(pairs),
            'partial_r': round(pr_e, 4) if pr_e else None
        }

    # Sort eras by partial r
    print("\n\nEra partial r(S2_t, Ent_t+1 | Ent_t):")
    for era, v in sorted(era_partial.items(), key=lambda x: x[1].get('partial_r') or 0, reverse=True):
        print(f"  {era:<30} r={v['partial_r']}  (n={v['n']})")

    # Key summary: in low-entropy (high-confidence) contexts specifically,
    # does positive S2 cascade into higher or lower entropy?
    # This is the empirically cleanest test.
    lep = cond_results['low_entropy_context']
    if lep.get('mean_ent1_after_pos_s2') and lep.get('mean_ent1_after_neg_s2'):
        delta = lep['mean_ent1_after_pos_s2'] - lep['mean_ent1_after_neg_s2']
        if delta > 0:
            verdict = "LIBERATION: surprising choices in confident contexts expand what can follow"
        else:
            verdict = "ANCHORING: surprising choices in confident contexts narrow what can follow"
        print(f"\n\nVerdict in low-entropy contexts: {verdict}")
        print(f"  Delta entropy_t+1 = {delta:+.4f}")

    output = {
        'n_texts': texts_used,
        'n_pairs': len(all_s2_t),
        'overall': {
            'r_s2_ent_next': round(pearson_r(all_s2_t, all_ent_t1), 4) if pearson_r(all_s2_t, all_ent_t1) else None,
            'partial_r_s2_ent_next_given_ent_t': round(pr, 4) if pr else None,
        },
        'conditional': cond_results,
        'era_partial_correlations': era_partial,
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")

if __name__ == '__main__':
    main()
