"""
Stanza-Internal Liberation Arc: Fractal Structure Hypothesis

Building on liberation_arc_within_poem.py which found:
- Poems move from Anchoring-dominant (opening) to Liberation-dominant (close)
- The effect is strongest in forms with refrain/repetition (villanelle, ballad)
- 68% of poems show Liberation building toward the end

HYPOTHESIS: The poem-level Anchoring→Liberation arc REPLICATES within each stanza.
If poetic structure is fractal, each stanza should have its own mini-arc:
- Stanza-opening positions dominated by Anchoring (model is uncertain)
- Stanza-closing positions dominated by Liberation (model has learned the stanza's idiom)

A secondary test: Does stanza position within a poem modulate the stanza arc slope?
(Early stanzas might show stronger Anchoring, late stanzas stronger Liberation)

Method:
1. Segment tokens into stanzas using newline-heavy tokens as stanza breaks
2. Within each stanza, classify tokens as Liberation/Anchoring by within-stanza position
3. Test whether the within-stanza arc direction matches the within-poem arc
4. Compare arc slopes: early stanzas vs. late stanzas
5. Test the fractal hypothesis: does stanza_arc_slope ~ poem_arc_slope?
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/stanza_internal_arc.json"

LOW_ENT_THRESHOLD = 4.0
HIGH_ENT_THRESHOLD = 7.0
MIN_STANZA_TOKENS = 5     # minimum tokens to count a stanza
MIN_POEM_STANZAS = 2      # minimum stanzas to analyze a poem


def pearson_r(xs, ys):
    n = len(xs)
    if n < 4:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx * dy == 0:
        return None
    return num / (dx * dy)


def linear_slope(xs, ys):
    n = len(xs)
    if n < 4:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    ssxx = sum((x - mx) ** 2 for x in xs)
    ssxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if ssxx == 0:
        return None, None
    slope = ssxy / ssxx
    return slope, my - slope * mx


def is_artifact(tok):
    return tok.get('p_newline', 0) > 0.9


def is_stanza_break(tok):
    """Tokens with very high p_newline (blank-line boundary) signal stanza breaks."""
    return tok.get('p_newline', 0) > 0.95


def classify_event(s2_t, ent_t, s2_median):
    if s2_t <= s2_median:
        return 'neutral'
    if ent_t < LOW_ENT_THRESHOLD:
        return 'liberation'
    elif ent_t >= HIGH_ENT_THRESHOLD:
        return 'anchoring'
    return 'neutral'


def segment_into_stanzas(tokens, global_s2_median):
    """Split clean tokens into stanzas, returning list of stanza token lists."""
    stanzas = []
    current = []
    for tok in tokens:
        if is_artifact(tok):
            if is_stanza_break(tok) and len(current) >= MIN_STANZA_TOKENS:
                stanzas.append(current)
                current = []
        else:
            current.append(tok)
    if len(current) >= MIN_STANZA_TOKENS:
        stanzas.append(current)
    return stanzas


def stanza_arc(stanza_tokens, global_s2_median):
    """
    For a single stanza, compute:
    - within-stanza decile Liberation/Anchoring profiles
    - arc slope (positive = Liberation builds toward stanza-end)
    """
    n = len(stanza_tokens)
    if n < MIN_STANZA_TOKENS:
        return None

    events = []
    for i, tok in enumerate(stanza_tokens):
        pos = i / (n - 1) if n > 1 else 0.5
        evt = classify_event(tok['s2'], tok['entropy'], global_s2_median)
        events.append((pos, evt))

    # Quintile profile (5 bins, since stanzas are short)
    bins = defaultdict(lambda: {'lib': 0, 'anc': 0, 'total': 0})
    for pos, evt in events:
        b = min(int(pos * 5), 4)
        bins[b]['total'] += 1
        if evt == 'liberation':
            bins[b]['lib'] += 1
        elif evt == 'anchoring':
            bins[b]['anc'] += 1

    lib_frac = []
    anc_frac = []
    net_frac = []
    xs = []
    for b in range(5):
        d = bins[b]
        if d['total'] >= 2:
            l = d['lib'] / d['total']
            a = d['anc'] / d['total']
            lib_frac.append(l)
            anc_frac.append(a)
            net_frac.append(l - a)
            xs.append(b / 4)

    if len(xs) < 3:
        return None

    slope, _ = linear_slope(xs, net_frac)
    r = pearson_r(xs, net_frac)

    return {
        'n_tokens': n,
        'lib_profile': lib_frac,
        'anc_profile': anc_frac,
        'net_profile': net_frac,
        'arc_slope': slope,
        'arc_r': r,
        'mean_lib': sum(lib_frac) / len(lib_frac),
        'mean_anc': sum(anc_frac) / len(anc_frac),
    }


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Global S2 median
    all_s2 = []
    for text in corpus:
        for tok in text.get('tokens', []):
            if not is_artifact(tok):
                all_s2.append(tok['s2'])
    global_s2_median = statistics.median(all_s2)
    print(f"Global S2 median: {global_s2_median:.3f} (n={len(all_s2):,} tokens)")

    # Per-poem analysis
    per_poem = []
    era_poems = defaultdict(list)
    total_stanzas = 0

    for text in corpus:
        meta = text.get('metadata', {})
        era = meta.get('era', 'unknown')
        title = meta.get('title', 'Unknown')
        author = meta.get('author', 'Unknown')
        tokens = text.get('tokens', [])

        stanzas = segment_into_stanzas(tokens, global_s2_median)
        if len(stanzas) < MIN_POEM_STANZAS:
            continue

        stanza_results = []
        for stanza_toks in stanzas:
            result = stanza_arc(stanza_toks, global_s2_median)
            if result is not None:
                stanza_results.append(result)

        if len(stanza_results) < MIN_POEM_STANZAS:
            continue

        total_stanzas += len(stanza_results)

        # Test fractal hypothesis: does stanza arc slope increase with stanza position?
        # (If poem-level arc is fractal, later stanzas should have higher arc slopes)
        stanza_positions = [i / (len(stanza_results) - 1) for i in range(len(stanza_results))]
        stanza_slopes = [s['arc_slope'] for s in stanza_results if s['arc_slope'] is not None]
        valid_pos = [p for p, s in zip(stanza_positions, [sr['arc_slope'] for sr in stanza_results])
                     if s is not None]

        pos_slope_r = pearson_r(valid_pos, stanza_slopes) if len(stanza_slopes) >= 4 else None

        # Average arc slope across all stanzas
        avg_arc_slope = sum(stanza_slopes) / len(stanza_slopes) if stanza_slopes else None
        pos_arc_slopes = sum(1 for s in stanza_slopes if s is not None and s > 0)
        pct_pos_arc = pos_arc_slopes / len(stanza_slopes) if stanza_slopes else None

        # Early vs. late stanza arc slopes
        n_stanzas = len(stanza_results)
        early_stanzas = stanza_results[:n_stanzas // 2]
        late_stanzas = stanza_results[n_stanzas // 2:]
        early_slopes = [s['arc_slope'] for s in early_stanzas if s['arc_slope'] is not None]
        late_slopes = [s['arc_slope'] for s in late_stanzas if s['arc_slope'] is not None]
        early_avg = sum(early_slopes) / len(early_slopes) if early_slopes else None
        late_avg = sum(late_slopes) / len(late_slopes) if late_slopes else None

        poem_data = {
            'title': title,
            'author': author,
            'era': era,
            'n_stanzas': len(stanza_results),
            'stanza_slopes': stanza_slopes,
            'avg_arc_slope': avg_arc_slope,
            'pct_pos_arc': pct_pos_arc,
            'pos_slope_correlation': pos_slope_r,
            'early_stanza_slope': early_avg,
            'late_stanza_slope': late_avg,
            'early_late_delta': (late_avg - early_avg) if early_avg is not None and late_avg is not None else None,
        }
        per_poem.append(poem_data)
        era_poems[era].append(poem_data)

    print(f"\nPoems analyzed: {len(per_poem):,} with {total_stanzas:,} stanzas")

    # === GLOBAL STANZA ARC ===
    all_arc_slopes = [p['avg_arc_slope'] for p in per_poem if p['avg_arc_slope'] is not None]
    pct_positive = sum(1 for s in all_arc_slopes if s > 0) / len(all_arc_slopes) if all_arc_slopes else 0
    mean_slope = sum(all_arc_slopes) / len(all_arc_slopes) if all_arc_slopes else 0

    print(f"\n=== GLOBAL STANZA-INTERNAL ARC ===")
    print(f"Mean within-stanza arc slope: {mean_slope:.4f}")
    print(f"% poems with positive slope (Anchoring→Liberation): {pct_positive*100:.1f}%")

    # Comparison to poem-level arc from previous experiment
    # (previous experiment found: poem-level mean slope ~+0.131, 68% positive)
    if pct_positive > 0.5:
        print("  → Fractal hypothesis SUPPORTED: stanzas mirror poem-level arc")
    elif pct_positive < 0.4:
        print("  → Fractal hypothesis REJECTED: stanzas show opposite arc to poem-level")
    else:
        print("  → Fractal hypothesis INCONCLUSIVE")

    # === STANZA POSITION EFFECT ===
    pos_slope_rs = [p['pos_slope_correlation'] for p in per_poem if p['pos_slope_correlation'] is not None]
    pct_pos_r = sum(1 for r in pos_slope_rs if r > 0) / len(pos_slope_rs) if pos_slope_rs else 0
    mean_r = sum(pos_slope_rs) / len(pos_slope_rs) if pos_slope_rs else 0

    print(f"\n=== STANZA POSITION EFFECT ===")
    print(f"Mean correlation (stanza position → arc slope): r = {mean_r:.4f}")
    print(f"% poems where later stanzas have higher arc slopes: {pct_pos_r*100:.1f}%")
    if mean_r > 0.1:
        print("  → Later stanzas tend to have stronger Anchoring→Liberation arcs")
    elif mean_r < -0.1:
        print("  → Earlier stanzas tend to have stronger arcs")

    # Early vs late stanza delta
    all_deltas = [p['early_late_delta'] for p in per_poem if p['early_late_delta'] is not None]
    mean_delta = sum(all_deltas) / len(all_deltas) if all_deltas else 0
    print(f"\nMean early-to-late stanza arc slope delta: {mean_delta:+.4f}")
    if mean_delta > 0.01:
        print("  → Arc slopes increase from early to late stanzas (fractal amplification)")
    elif mean_delta < -0.01:
        print("  → Arc slopes decrease from early to late stanzas (fractal attenuation)")

    # === ERA BREAKDOWN ===
    print(f"\n=== ERA-LEVEL STANZA ARC SLOPES ===")
    era_stats = []
    for era, poems in sorted(era_poems.items(), key=lambda kv: -len(kv[1])):
        slopes = [p['avg_arc_slope'] for p in poems if p['avg_arc_slope'] is not None]
        if len(slopes) < 2:
            continue
        mean_s = sum(slopes) / len(slopes)
        pct_p = sum(1 for s in slopes if s > 0) / len(slopes)
        deltas = [p['early_late_delta'] for p in poems if p['early_late_delta'] is not None]
        mean_d = sum(deltas) / len(deltas) if deltas else None
        era_stats.append({
            'era': era,
            'n': len(poems),
            'mean_slope': mean_s,
            'pct_pos': pct_p,
            'mean_delta': mean_d
        })

    era_stats.sort(key=lambda x: -x['mean_slope'])
    print(f"{'Era':<30} {'n':>4} {'Avg slope':>10} {'% pos':>7} {'Early→Late Δ':>13}")
    for e in era_stats:
        d_str = f"{e['mean_delta']:+.4f}" if e['mean_delta'] is not None else "    —"
        print(f"  {e['era']:<28} {e['n']:>4} {e['mean_slope']:>10.4f} {e['pct_pos']*100:>6.1f}% {d_str:>13}")

    # === POEMS WITH STRONGEST FRACTAL SIGNATURE ===
    print(f"\n=== TOP 10 POEMS: STRONGEST FRACTAL ARC (consistent slope) ===")
    poems_with_data = [p for p in per_poem if p['avg_arc_slope'] is not None and p['n_stanzas'] >= 3]
    top_poems = sorted(poems_with_data, key=lambda p: abs(p['avg_arc_slope']), reverse=True)[:10]
    for p in top_poems:
        direction = "→Liberation" if p['avg_arc_slope'] > 0 else "→Anchoring"
        stanza_slopes_fmt = ", ".join(f"{s:+.2f}" for s in (p['stanza_slopes'] or [])[:5])
        print(f"  {p['title'][:35]:<35} | {p['author'][:20]:<20} | slope={p['avg_arc_slope']:+.3f} {direction}")
        print(f"    stanza slopes: [{stanza_slopes_fmt}]  n={p['n_stanzas']}")

    # === POEMS WHERE STANZA POSITION PREDICTS SLOPE ===
    print(f"\n=== TOP 10 POEMS: STRONGEST POSITION-SLOPE CORRELATION ===")
    poems_pos_corr = [p for p in per_poem if p['pos_slope_correlation'] is not None and p['n_stanzas'] >= 4]
    top_pos = sorted(poems_pos_corr, key=lambda p: p['pos_slope_correlation'], reverse=True)[:10]
    for p in top_pos:
        print(f"  r={p['pos_slope_correlation']:+.3f} | {p['title'][:35]:<35} | {p['era']:<20} | n_stanzas={p['n_stanzas']}")

    # Save results
    output = {
        'global': {
            'n_poems': len(per_poem),
            'n_stanzas': total_stanzas,
            'mean_arc_slope': mean_slope,
            'pct_positive_arc': pct_positive,
            'mean_pos_slope_r': mean_r,
            'mean_early_late_delta': mean_delta,
        },
        'per_era': era_stats,
        'top_fractal_poems': [
            {k: v for k, v in p.items() if k != 'stanza_slopes'}
            for p in top_poems
        ],
        'top_position_corr_poems': [
            {k: v for k, v in p.items() if k != 'stanza_slopes'}
            for p in top_pos
        ],
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
