"""
S2 Spectral Periodicity: Does Poetic Meter Create Rhythmic Surprise?
=====================================================================
Hypothesis: Metrical poetry creates periodic patterns in S2 because:
  1. GPT-2 is sensitive to syntactic/positional regularity
  2. Meter constrains word placement (stressed syllables → content words → higher S2)
  3. Therefore S2 should oscillate at the frequency of the metrical foot / line

Method: Apply FFT to the S2 time series of each poem.
Dominant period (in GPT-2 tokens) is compared across metrical traditions.

Expected period if meter shows up:
  - Iambic pentameter: ~10 syllables/line × ~1.2 tokens/syllable ≈ 12 tokens
  - Ballad stanza: ~7-8 syllables/line ≈ 8-9 tokens
  - Haiku: 5-7-5 syllables, ~7-8 tokens/line
  - Free verse: no dominant period
"""

import json
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
MIN_TOKENS = 40  # minimum clean tokens for reliable FFT

def fft_dominant_period(s2_values):
    """
    Compute dominant period from FFT of S2 time series.
    Returns (period_in_tokens, periodicity_strength, full_spectrum).
    periodicity_strength = max_power / mean_power (ratio; 1.0 = white noise).
    """
    n = len(s2_values)
    if n < MIN_TOKENS:
        return None, None, None

    # Subtract mean (detrend)
    mean = sum(s2_values) / n
    centered = [x - mean for x in s2_values]

    # Compute DFT manually (avoid numpy dependency)
    # Only need frequencies 2..n//2 (periods n/2 .. 2 tokens)
    powers = []
    for k in range(1, n // 2 + 1):
        re = sum(centered[t] * math.cos(2 * math.pi * k * t / n) for t in range(n))
        im = sum(centered[t] * math.sin(2 * math.pi * k * t / n) for t in range(n))
        power = (re**2 + im**2) / n
        period = n / k  # period in tokens
        powers.append((period, power, k))

    if not powers:
        return None, None, None

    # Filter to meaningful period range: 3-30 tokens (sub-line to multi-line)
    filtered = [(period, power, k) for period, power, k in powers if 3 <= period <= 30]
    if not filtered:
        return None, None, None

    mean_power = statistics.mean(p for _, p, _ in filtered)
    if mean_power == 0:
        return None, None, None

    # Dominant period in filtered range
    best = max(filtered, key=lambda x: x[1])
    dominant_period = best[0]
    dominant_power = best[1]
    strength = dominant_power / mean_power

    return dominant_period, strength, filtered


def clean_s2(tokens):
    """Extract S2 values, removing stanza-break artifact tokens."""
    return [
        t['s2'] for t in tokens
        if t.get('p_newline', 0) < 0.9 and abs(t.get('s2', 0)) < 50
    ]


def analyze_poem(poem):
    tokens = poem.get('tokens', [])
    meta = poem.get('metadata', {})
    s2_clean = clean_s2(tokens)

    if len(s2_clean) < MIN_TOKENS:
        return None

    dominant_period, strength, spectrum = fft_dominant_period(s2_clean)
    if dominant_period is None:
        return None

    return {
        'title': meta.get('title', '?'),
        'author': meta.get('author', '?'),
        'era': meta.get('era', '?'),
        'n_tokens': len(s2_clean),
        'dominant_period': dominant_period,
        'strength': strength,
        'avg_s2': statistics.mean(s2_clean),
        'spectrum': spectrum,
    }


def run():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    results = []
    for poem in corpus:
        r = analyze_poem(poem)
        if r:
            results.append(r)

    # Group by era
    era_data = defaultdict(list)
    for r in results:
        era_data[r['era']].append(r)

    # Summary per era: avg dominant_period, avg strength, n
    era_summary = []
    for era, poems in era_data.items():
        if len(poems) < 2:
            continue
        avg_period = statistics.mean(p['dominant_period'] for p in poems)
        avg_strength = statistics.mean(p['strength'] for p in poems)
        era_summary.append({
            'era': era,
            'n': len(poems),
            'avg_period': avg_period,
            'avg_strength': avg_strength,
        })

    # Sort by avg_strength descending (most periodic first)
    era_summary.sort(key=lambda x: -x['avg_strength'])

    # Top poems by periodicity strength
    top_poems = sorted(results, key=lambda x: -x['strength'])[:15]

    # Compare metrical vs free verse (manual grouping)
    metrical_eras = {'ballad', 'fixed_form', 'romantic', 'victorian', 'metaphysical',
                     'early_modern', '19th_century', 'nursery_rhyme', 'harlem_renaissance'}
    free_verse_eras = {'contemporary', 'new_york_school', 'beat', 'language',
                       'prose_poetry', 'found_poetry', 'modernist', 'confessional'}

    metrical_strengths = [r['strength'] for r in results if r['era'] in metrical_eras]
    free_verse_strengths = [r['strength'] for r in results if r['era'] in free_verse_eras]
    metrical_periods = [r['dominant_period'] for r in results if r['era'] in metrical_eras]
    free_verse_periods = [r['dominant_period'] for r in results if r['era'] in free_verse_eras]

    metrical_avg_strength = statistics.mean(metrical_strengths) if metrical_strengths else 0
    free_verse_avg_strength = statistics.mean(free_verse_strengths) if free_verse_strengths else 0
    metrical_avg_period = statistics.mean(metrical_periods) if metrical_periods else 0
    free_verse_avg_period = statistics.mean(free_verse_periods) if free_verse_periods else 0

    # Period histogram: count poems with dominant period in bins
    bins = [(3,5), (5,7), (7,9), (9,12), (12,15), (15,20), (20,30)]
    metrical_hist = defaultdict(int)
    free_verse_hist = defaultdict(int)
    for r in results:
        p = r['dominant_period']
        for lo, hi in bins:
            if lo <= p < hi:
                bin_label = f"{lo}-{hi}"
                if r['era'] in metrical_eras:
                    metrical_hist[bin_label] += 1
                elif r['era'] in free_verse_eras:
                    free_verse_hist[bin_label] += 1
                break

    return {
        'era_summary': era_summary,
        'top_poems': top_poems,
        'metrical_avg_strength': metrical_avg_strength,
        'free_verse_avg_strength': free_verse_avg_strength,
        'metrical_avg_period': metrical_avg_period,
        'free_verse_avg_period': free_verse_avg_period,
        'n_metrical': len(metrical_strengths),
        'n_free_verse': len(free_verse_strengths),
        'metrical_hist': dict(metrical_hist),
        'free_verse_hist': dict(free_verse_hist),
        'n_analyzed': len(results),
    }


if __name__ == '__main__':
    import time
    print("Running spectral periodicity analysis...")
    t0 = time.time()
    result = run()
    elapsed = time.time() - t0
    print(f"Done in {elapsed:.1f}s. Analyzed {result['n_analyzed']} poems.")
    print(f"\nMetrical avg strength: {result['metrical_avg_strength']:.2f} (n={result['n_metrical']})")
    print(f"Free verse avg strength: {result['free_verse_avg_strength']:.2f} (n={result['n_free_verse']})")
    print(f"\nMetrical avg dominant period: {result['metrical_avg_period']:.1f} tokens")
    print(f"Free verse avg dominant period: {result['free_verse_avg_period']:.1f} tokens")
    print("\nTop 10 most periodic poems:")
    for p in result['top_poems'][:10]:
        print(f"  {p['author']} - {p['title'][:40]:40s} | period={p['dominant_period']:.1f} | strength={p['strength']:.1f} | era={p['era']}")
    print("\nEra summary (sorted by periodicity strength):")
    for e in result['era_summary']:
        print(f"  {e['era']:25s} n={e['n']:3d}  period={e['avg_period']:5.1f}  strength={e['avg_strength']:.2f}")
    print("\nPeriod histogram:")
    bins = ["3-5","5-7","7-9","9-12","12-15","15-20","20-30"]
    for b in bins:
        m = result['metrical_hist'].get(b, 0)
        f = result['free_verse_hist'].get(b, 0)
        print(f"  {b:6s} tokens: metrical={m:3d}  free_verse={f:3d}")
