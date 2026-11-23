"""
Liberation Arc: Within-Poem Shift from Liberation to Anchoring Modes

Building on entropy_after_surprise_v2.py which found:
- LOW-entropy context + high-S2 → Liberation (+1.25 bits next entropy)
- HIGH-entropy context + high-S2 → Anchoring (−1.01 bits next entropy)

Hypothesis: Poems shift from Liberation mode (early) to Anchoring mode (late).
If true, surprise at the start of a poem opens new possibility; surprise near the
end collapses toward closure. This would be a measurable "information-theoretic arc."

Method:
1. For each poem, classify each consecutive token pair as:
   - Liberation: high-S2 in low-entropy context (ent_t < 4, s2_t > median_s2)
   - Anchoring: high-S2 in high-entropy context (ent_t >= 7, s2_t > median_s2)
   - Neutral: everything else
2. Normalize token position to [0, 1] within each poem.
3. Compute mean Liberation ratio in each decile of poem position.
4. Fit linear regression to test for a systematic arc.
5. Compare arc slopes across literary eras.
6. Test the "volta" hypothesis: is there a sharp transition around position 0.5-0.75?
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/liberation_arc_within_poem.json"

LOW_ENT_THRESHOLD = 4.0   # model was confident
HIGH_ENT_THRESHOLD = 7.0  # model was uncertain


def pearson_r(xs, ys):
    n = len(xs)
    if n < 5:
        return None
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx * dy == 0:
        return None
    return num / (dx * dy)


def linear_slope(xs, ys):
    """Return slope and intercept of least-squares line."""
    n = len(xs)
    if n < 5:
        return None, None
    mx, my = sum(xs) / n, sum(ys) / n
    ssxx = sum((x - mx) ** 2 for x in xs)
    ssxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    if ssxx == 0:
        return None, None
    slope = ssxy / ssxx
    intercept = my - slope * mx
    return slope, intercept


def is_artifact(tok):
    return tok.get('p_newline', 0) > 0.9


def classify_pair(s2_t, ent_t, s2_median):
    """Return 'liberation', 'anchoring', or 'neutral'."""
    is_high_s2 = s2_t > s2_median
    if not is_high_s2:
        return 'neutral'
    if ent_t < LOW_ENT_THRESHOLD:
        return 'liberation'
    elif ent_t >= HIGH_ENT_THRESHOLD:
        return 'anchoring'
    return 'neutral'


def analyze_poem(tokens, global_s2_median):
    """Return list of (pos_norm, event_type) for each consecutive pair."""
    clean = [t for t in tokens if not is_artifact(t)]
    n = len(clean)
    if n < 10:
        return []
    pairs = []
    for i in range(n - 1):
        t0 = clean[i]
        s2_t = t0['s2']
        ent_t = t0['entropy']
        pos_norm = i / (n - 2) if n > 2 else 0.5
        event_type = classify_pair(s2_t, ent_t, global_s2_median)
        pairs.append((pos_norm, event_type, s2_t, ent_t))
    return pairs


def decile_profile(pairs, event_type):
    """Compute mean fraction of `event_type` in each decile (0-9)."""
    buckets = defaultdict(list)
    for pos, evt, s2, ent in pairs:
        decile = min(int(pos * 10), 9)
        buckets[decile].append(1 if evt == event_type else 0)
    profile = []
    for d in range(10):
        vals = buckets.get(d, [])
        profile.append(sum(vals) / len(vals) if vals else None)
    return profile


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Compute global S2 median across all clean tokens
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

    texts_used = 0
    for text in corpus:
        meta = text.get('metadata', {})
        era = meta.get('era', 'unknown')
        title = meta.get('title', 'Unknown')
        author = meta.get('author', 'Unknown')
        tokens = text.get('tokens', [])

        pairs = analyze_poem(tokens, global_s2_median)
        if len(pairs) < 20:
            continue
        texts_used += 1

        lib_profile = decile_profile(pairs, 'liberation')
        anc_profile = decile_profile(pairs, 'anchoring')

        # Liberation - Anchoring net score per decile
        net_profile = []
        for l, a in zip(lib_profile, anc_profile):
            if l is None or a is None:
                net_profile.append(None)
            else:
                net_profile.append(l - a)

        # Linear trend: does the net Liberation score decrease over the poem?
        decile_xs = [d / 9 for d in range(10)]
        valid_pairs = [(x, y) for x, y in zip(decile_xs, net_profile) if y is not None]
        if len(valid_pairs) >= 5:
            xs, ys = zip(*valid_pairs)
            slope, intercept = linear_slope(xs, ys)
            r = pearson_r(xs, ys)
        else:
            slope, intercept, r = None, None, None

        # Early vs. late liberation balance
        early_net = [v for d, v in enumerate(net_profile) if d < 5 and v is not None]
        late_net = [v for d, v in enumerate(net_profile) if d >= 5 and v is not None]
        early_mean = sum(early_net) / len(early_net) if early_net else None
        late_mean = sum(late_net) / len(late_net) if late_net else None

        poem_data = {
            'title': title,
            'author': author,
            'era': era,
            'n_pairs': len(pairs),
            'lib_profile': lib_profile,
            'anc_profile': anc_profile,
            'net_profile': net_profile,
            'arc_slope': slope,
            'arc_r': r,
            'early_net': early_mean,
            'late_net': late_mean,
            'early_late_delta': (late_mean - early_mean) if early_mean is not None and late_mean is not None else None,
        }
        per_poem.append(poem_data)
        era_poems[era].append(poem_data)

    print(f"\nTexts analyzed: {texts_used:,}")

    # === GLOBAL DECILE PROFILE ===
    global_lib_deciles = [[] for _ in range(10)]
    global_anc_deciles = [[] for _ in range(10)]
    global_net_deciles = [[] for _ in range(10)]

    for poem in per_poem:
        for d in range(10):
            if poem['lib_profile'][d] is not None:
                global_lib_deciles[d].append(poem['lib_profile'][d])
            if poem['anc_profile'][d] is not None:
                global_anc_deciles[d].append(poem['anc_profile'][d])
            if poem['net_profile'][d] is not None:
                global_net_deciles[d].append(poem['net_profile'][d])

    global_lib_profile = [sum(v) / len(v) if v else None for v in global_lib_deciles]
    global_anc_profile = [sum(v) / len(v) if v else None for v in global_anc_deciles]
    global_net_profile = [sum(v) / len(v) if v else None for v in global_net_deciles]

    print("\n=== GLOBAL WITHIN-POEM DECILE PROFILE ===")
    print(f"{'Decile':>8} {'Liberation':>12} {'Anchoring':>12} {'Net (L-A)':>12}")
    for d in range(10):
        l = global_lib_profile[d]
        a = global_anc_profile[d]
        n = global_net_profile[d]
        bar = "+" * int(max(0, (n or 0)) * 100) if n is not None and n > 0 else "-" * int(max(0, -(n or 0)) * 100)
        print(f"  {d*10:3d}-{(d+1)*10:3d}%  {l:12.4f}  {a:12.4f}  {n:12.4f}  {bar[:40]}")

    # Linear slope of global net profile
    xs = [d / 9 for d in range(10)]
    valid = [(x, y) for x, y in zip(xs, global_net_profile) if y is not None]
    if valid:
        gxs, gys = zip(*valid)
        g_slope, g_intercept = linear_slope(gxs, gys)
        g_r = pearson_r(gxs, gys)
        print(f"\nGlobal arc slope: {g_slope:.5f} (r={g_r:.3f})")
        if g_slope < -0.0001:
            print("  → Net Liberation decreases over the poem (Liberation→Anchoring arc CONFIRMED)")
        elif g_slope > 0.0001:
            print("  → Net Liberation increases over the poem (Liberation builds to end)")
        else:
            print("  → No strong arc direction")

    # === ERA-LEVEL ARC SLOPES ===
    print("\n=== ERA ARC SLOPES (Liberation→Anchoring trend) ===")
    print("Negative slope = Liberation decreases toward end (poem moves to Anchoring)")
    print(f"{'Era':>30} {'n':>5} {'Avg slope':>10} {'Avg r':>8} {'Early net':>10} {'Late net':>10}")

    era_stats = {}
    for era, poems in era_poems.items():
        slopes = [p['arc_slope'] for p in poems if p['arc_slope'] is not None]
        rs = [p['arc_r'] for p in poems if p['arc_r'] is not None]
        early = [p['early_net'] for p in poems if p['early_net'] is not None]
        late = [p['late_net'] for p in poems if p['late_net'] is not None]
        if len(slopes) < 2:
            continue
        avg_slope = sum(slopes) / len(slopes)
        avg_r = sum(rs) / len(rs) if rs else None
        avg_early = sum(early) / len(early) if early else None
        avg_late = sum(late) / len(late) if late else None
        era_stats[era] = {
            'n': len(slopes),
            'avg_slope': avg_slope,
            'avg_r': avg_r,
            'avg_early': avg_early,
            'avg_late': avg_late,
        }

    for era, stats in sorted(era_stats.items(), key=lambda x: x[1]['avg_slope']):
        n = stats['n']
        sl = stats['avg_slope']
        r = stats['avg_r']
        e = stats['avg_early']
        l = stats['avg_late']
        print(f"  {era:>30} {n:>5} {sl:>10.5f} {r if r else 0:>8.3f} {e if e else 0:>10.4f} {l if l else 0:>10.4f}")

    # === TOP POEMS: Strongest Liberation Arc ===
    print("\n=== TOP 15 POEMS WITH STRONGEST Liberation→Anchoring ARC ===")
    sorted_poems = sorted([p for p in per_poem if p['arc_slope'] is not None], key=lambda x: x['arc_slope'])
    for p in sorted_poems[:15]:
        print(f"  slope={p['arc_slope']:+.4f} r={p['arc_r'] or 0:+.3f}  {p['title'][:45]} [{p['era']}]")

    print("\n=== TOP 15 POEMS WITH Liberation THAT BUILDS TOWARD END (Anchoring→Liberation ARC) ===")
    for p in sorted_poems[-15:]:
        print(f"  slope={p['arc_slope']:+.4f} r={p['arc_r'] or 0:+.3f}  {p['title'][:45]} [{p['era']}]")

    # === VOLTA ANALYSIS ===
    # Does the net score drop sharply at decile 5 (50-60%)?
    print("\n=== VOLTA ANALYSIS: Transition at Mid-Poem ===")
    # For each poem, compute (mean deciles 0-4) - (mean deciles 5-9)
    deltas = [(p['early_late_delta'], p['title'], p['era']) for p in per_poem if p['early_late_delta'] is not None]
    negative_deltas = [d for d, t, e in deltas if d < 0]
    positive_deltas = [d for d, t, e in deltas if d > 0]
    print(f"  Poems where late net > early net (anchoring builds late): {len(negative_deltas)} / {len(deltas)}")
    print(f"  Poems where early net > late net (liberation dominant early): {len(positive_deltas)} / {len(deltas)}")
    overall_delta = sum(d for d, t, e in deltas) / len(deltas) if deltas else 0
    print(f"  Mean delta (early - late): {overall_delta:+.5f}")
    if overall_delta > 0:
        print("  → CONFIRMED: Liberation more prevalent early; Anchoring more prevalent late")
    else:
        print("  → NOT CONFIRMED: No consistent early-to-late shift")

    # Era-level volta analysis
    print("\n  Era volta direction (mean early_late_delta):")
    for era, poems in era_poems.items():
        deltas_era = [p['early_late_delta'] for p in poems if p['early_late_delta'] is not None]
        if len(deltas_era) < 3:
            continue
        mean_d = sum(deltas_era) / len(deltas_era)
        direction = "Liberation→Anchoring" if mean_d > 0 else "Anchoring→Liberation"
        print(f"    {era:>30}  delta={mean_d:+.5f}  {direction}")

    # Save results
    output = {
        'global_s2_median': global_s2_median,
        'texts_analyzed': texts_used,
        'global_lib_profile': global_lib_profile,
        'global_anc_profile': global_anc_profile,
        'global_net_profile': global_net_profile,
        'global_arc_slope': g_slope if valid else None,
        'global_arc_r': g_r if valid else None,
        'era_stats': era_stats,
        'per_poem': per_poem,
    }
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
