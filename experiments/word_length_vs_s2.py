"""
Word Length vs. S2: Does Poetic Surprise Favor Short Words (Contextual Defiance)
or Long Words (Vocabulary Rarity)?

Key question: When a poet surprises, are they deploying rare long words (vocabulary
rarity mechanism) or inserting short common words in unexpected positions (contextual
defiance mechanism)?

This matters theoretically: if surprise lives in long words, poetic S2 is mainly
a measure of vocabulary richness. If surprise lives in short words placed contextually
wrong, it's a measure of syntactic/semantic subversion — a more interesting finding.
"""

import json
import re
import statistics

def clean_token(tok):
    """Strip GPT-2 tokenization artifacts (leading space, Ġ, etc.)"""
    t = tok.strip()
    if t.startswith('Ġ'):
        t = t[1:]
    return t.strip()

def char_len(tok):
    """Length of token in alphabetic characters (ignore punctuation/whitespace)."""
    t = clean_token(tok)
    alpha = re.sub(r'[^a-zA-Z]', '', t)
    return len(alpha)

def classify_length(n):
    """Bin token by alphabetic character count."""
    if n == 0:
        return 'punct/ws'
    elif n <= 2:
        return '1-2 chars'
    elif n <= 4:
        return '3-4 chars'
    elif n <= 6:
        return '5-6 chars'
    elif n <= 9:
        return '7-9 chars'
    else:
        return '10+ chars'

LENGTH_ORDER = ['1-2 chars', '3-4 chars', '5-6 chars', '7-9 chars', '10+ chars', 'punct/ws']

def analyze_word_length_vs_s2(data, era_filter=None, min_tokens=20):
    """
    Main analysis: for each length bucket, collect S2 values.
    Returns dict of bucket -> list of S2 values.
    """
    buckets = {b: [] for b in LENGTH_ORDER}

    for poem in data:
        era = poem['metadata'].get('era', '')
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        if era == 'control':
            continue
        if era_filter and era != era_filter:
            continue

        for tok in poem.get('tokens', []):
            token_str = tok.get('token', '')
            s2 = tok.get('s2', 0)
            n = char_len(token_str)
            bucket = classify_length(n)
            buckets[bucket].append(s2)

    return buckets

def high_s2_length_profile(data, threshold=3.0):
    """
    At high-S2 positions, what does the length distribution look like?
    Compare to the overall length distribution.
    """
    all_lengths = []
    high_s2_lengths = []

    for poem in data:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        if poem['metadata'].get('era') == 'control':
            continue

        for tok in poem.get('tokens', []):
            token_str = tok.get('token', '')
            s2 = tok.get('s2', 0)
            n = char_len(token_str)
            if n > 0:  # skip pure punctuation
                all_lengths.append(n)
                if s2 >= threshold:
                    high_s2_lengths.append(n)

    return all_lengths, high_s2_lengths

def alternative_length_analysis(data, threshold=3.0):
    """
    For high-S2 tokens: compare the length of CHOSEN token vs. length of TOP PREDICTED token.

    If chosen word is SHORTER than predicted: contextual defiance (short word, unexpected place)
    If chosen word is LONGER than predicted: vocabulary rarity (longer/rarer word chosen)
    If lengths are similar: same-register substitution
    """
    shorter_chosen = []  # chosen shorter than predicted: contextual defiance
    longer_chosen = []   # chosen longer than predicted: vocabulary rarity
    same_length = []     # comparable length

    for poem in data:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        if poem['metadata'].get('era') == 'control':
            continue

        for tok in poem.get('tokens', []):
            s2 = tok.get('s2', 0)
            if s2 < threshold:
                continue

            token_str = tok.get('token', '')
            alts = tok.get('alternatives', [])
            if not alts:
                continue

            chosen_len = char_len(token_str)
            top_pred = alts[0].get('token', '')
            pred_len = char_len(top_pred)

            if chosen_len == 0 or pred_len == 0:
                continue

            diff = chosen_len - pred_len
            entry = {
                'chosen': clean_token(token_str),
                'predicted': clean_token(top_pred),
                'chosen_len': chosen_len,
                'pred_len': pred_len,
                'diff': diff,
                's2': s2,
                'author': poem['metadata'].get('author', 'unknown'),
                'era': poem['metadata'].get('era', 'unknown')
            }

            if diff <= -2:
                shorter_chosen.append(entry)
            elif diff >= 2:
                longer_chosen.append(entry)
            else:
                same_length.append(entry)

    return shorter_chosen, longer_chosen, same_length

def era_length_profiles(data, threshold=3.0):
    """
    For each era: what's the median word length at high-S2 positions?
    And at baseline positions?
    """
    era_high_lengths = {}
    era_all_lengths = {}

    for poem in data:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        era = poem['metadata'].get('era', 'unknown')
        if era == 'control':
            continue

        for tok in poem.get('tokens', []):
            token_str = tok.get('token', '')
            s2 = tok.get('s2', 0)
            n = char_len(token_str)
            if n == 0:
                continue

            if era not in era_all_lengths:
                era_all_lengths[era] = []
                era_high_lengths[era] = []

            era_all_lengths[era].append(n)
            if s2 >= threshold:
                era_high_lengths[era].append(n)

    return era_high_lengths, era_all_lengths

def poet_length_at_surprise(data, threshold=3.0, min_high_s2=5):
    """
    Per-poet: average word length at high-S2 positions vs. overall.
    Reveals each poet's "surprise vocabulary weight."
    """
    poet_stats = {}

    for poem in data:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        era = poem['metadata'].get('era', 'unknown')
        if era == 'control':
            continue
        author = poem['metadata'].get('author', 'Unknown')

        for tok in poem.get('tokens', []):
            token_str = tok.get('token', '')
            s2 = tok.get('s2', 0)
            n = char_len(token_str)
            if n == 0:
                continue

            if author not in poet_stats:
                poet_stats[author] = {'all': [], 'high': []}

            poet_stats[author]['all'].append(n)
            if s2 >= threshold:
                poet_stats[author]['high'].append(n)

    results = []
    for author, stats in poet_stats.items():
        if len(stats['high']) < min_high_s2:
            continue
        avg_all = statistics.mean(stats['all'])
        avg_high = statistics.mean(stats['high'])
        results.append({
            'author': author,
            'avg_len_all': round(avg_all, 2),
            'avg_len_high_s2': round(avg_high, 2),
            'diff': round(avg_high - avg_all, 2),
            'n_high': len(stats['high']),
            'n_all': len(stats['all'])
        })

    return sorted(results, key=lambda x: x['diff'])

def main():
    with open('results/corpus_results.json') as f:
        data = json.load(f)

    print("=" * 70)
    print("WORD LENGTH vs. S₂: CONTEXTUAL DEFIANCE vs. VOCABULARY RARITY")
    print("=" * 70)

    # 1. Overall length-bucket analysis
    print("\n## 1. S₂ by Word Length Bucket (all English poetry, excl. control)\n")
    buckets = analyze_word_length_vs_s2(data)

    total_tokens = sum(len(v) for k,v in buckets.items() if k != 'punct/ws')
    print(f"Total tokens analyzed: {total_tokens:,}")
    print()
    print(f"{'Bucket':<14} {'N':>7} {'Mean S₂':>9} {'Median S₂':>11} {'%Positive':>11} {'StdDev':>8}")
    print("-" * 65)

    for bucket in LENGTH_ORDER:
        vals = buckets[bucket]
        if bucket == 'punct/ws' or not vals:
            continue
        mean_s2 = statistics.mean(vals)
        med_s2 = statistics.median(vals)
        pct_pos = sum(1 for v in vals if v > 0) / len(vals) * 100
        std = statistics.stdev(vals) if len(vals) > 1 else 0
        print(f"{bucket:<14} {len(vals):>7,} {mean_s2:>+9.3f} {med_s2:>+11.3f} {pct_pos:>10.1f}% {std:>8.3f}")

    # 2. High-S2 length profile
    print("\n## 2. Length Distribution: High-S₂ Tokens vs. All Tokens\n")
    all_lengths, high_s2_lengths = high_s2_length_profile(data, threshold=3.0)

    if all_lengths and high_s2_lengths:
        avg_all = statistics.mean(all_lengths)
        avg_high = statistics.mean(high_s2_lengths)
        med_all = statistics.median(all_lengths)
        med_high = statistics.median(high_s2_lengths)
        print(f"All tokens: mean len = {avg_all:.2f}, median = {med_all:.0f}")
        print(f"High-S₂ tokens (S₂≥3.0): mean len = {avg_high:.2f}, median = {med_high:.0f}")
        print(f"Length INCREASE at high-S₂: {avg_high - avg_all:+.2f} chars ({(avg_high/avg_all - 1)*100:+.1f}%)")
        print()

        # Distribution breakdown
        from collections import Counter
        all_dist = Counter(classify_length(n) for n in all_lengths)
        high_dist = Counter(classify_length(n) for n in high_s2_lengths)
        all_total = len(all_lengths)
        high_total = len(high_s2_lengths)

        print(f"{'Bucket':<14} {'All %':>7} {'High-S₂ %':>10} {'Ratio':>7}")
        print("-" * 42)
        for bucket in LENGTH_ORDER[:-1]:
            a_pct = all_dist.get(bucket, 0) / all_total * 100
            h_pct = high_dist.get(bucket, 0) / high_total * 100
            ratio = h_pct / a_pct if a_pct > 0 else 0
            print(f"{bucket:<14} {a_pct:>6.1f}% {h_pct:>9.1f}% {ratio:>7.2f}x")

    # 3. Chosen vs. predicted length
    print("\n## 3. Chosen vs. Predicted Token Length at High-S₂ Moments\n")
    shorter, longer, same = alternative_length_analysis(data, threshold=3.0)
    total_compared = len(shorter) + len(longer) + len(same)

    print(f"Total high-S₂ tokens with alternatives: {total_compared}")
    print()
    print(f"Shorter chosen (contextual defiance):  {len(shorter):>5} ({len(shorter)/total_compared*100:.1f}%)")
    print(f"Similar length (same-register swap):   {len(same):>5} ({len(same)/total_compared*100:.1f}%)")
    print(f"Longer chosen (vocabulary rarity):     {len(longer):>5} ({len(longer)/total_compared*100:.1f}%)")

    # Mean S2 for each category
    if shorter:
        print(f"\nMean S₂ — shorter chosen: {statistics.mean(s['s2'] for s in shorter):.2f}")
    if same:
        print(f"Mean S₂ — similar length:  {statistics.mean(s['s2'] for s in same):.2f}")
    if longer:
        print(f"Mean S₂ — longer chosen:   {statistics.mean(s['s2'] for s in longer):.2f}")

    # Examples
    print("\nTop 5 'shorter chosen' examples (contextual defiance):")
    for ex in sorted(shorter, key=lambda x: -x['s2'])[:5]:
        print(f"  '{ex['predicted']}' (len={ex['pred_len']}) → '{ex['chosen']}' (len={ex['chosen_len']}) | S₂={ex['s2']:.1f} | {ex['author']}")

    print("\nTop 5 'longer chosen' examples (vocabulary rarity):")
    for ex in sorted(longer, key=lambda x: -x['s2'])[:5]:
        print(f"  '{ex['predicted']}' (len={ex['pred_len']}) → '{ex['chosen']}' (len={ex['chosen_len']}) | S₂={ex['s2']:.1f} | {ex['author']}")

    # 4. Era profiles
    print("\n## 4. Era-Level Length at High-S₂ Positions\n")
    era_high, era_all = era_length_profiles(data, threshold=3.0)

    era_results = []
    for era in era_high:
        if len(era_high[era]) < 5:
            continue
        avg_h = statistics.mean(era_high[era])
        avg_a = statistics.mean(era_all[era])
        era_results.append((era, avg_h, avg_a, avg_h - avg_a, len(era_high[era])))

    era_results.sort(key=lambda x: x[1])
    print(f"{'Era':<22} {'HighS₂ AvgLen':>14} {'All AvgLen':>11} {'Diff':>7} {'N':>5}")
    print("-" * 62)
    for era, h, a, diff, n in era_results:
        print(f"{era:<22} {h:>14.2f} {a:>11.2f} {diff:>+7.2f} {n:>5}")

    # 5. Poet-level
    print("\n## 5. Poets Ranked by Word Length at High-S₂ Positions\n")
    poet_results = poet_length_at_surprise(data, threshold=3.0, min_high_s2=5)

    print(f"{'Author':<30} {'All AvgLen':>10} {'High AvgLen':>12} {'Diff':>7} {'N_high':>7}")
    print("-" * 68)
    for r in poet_results:
        print(f"{r['author']:<30} {r['avg_len_all']:>10.2f} {r['avg_len_high_s2']:>12.2f} {r['diff']:>+7.2f} {r['n_high']:>7}")

    return {
        'buckets': {k: {'n': len(v), 'mean_s2': statistics.mean(v) if v else 0} for k,v in buckets.items()},
        'avg_len_all': statistics.mean(all_lengths),
        'avg_len_high_s2': statistics.mean(high_s2_lengths),
        'shorter_pct': len(shorter) / total_compared * 100 if total_compared else 0,
        'longer_pct': len(longer) / total_compared * 100 if total_compared else 0,
        'same_pct': len(same) / total_compared * 100 if total_compared else 0,
        'shorter_mean_s2': statistics.mean(s['s2'] for s in shorter) if shorter else 0,
        'longer_mean_s2': statistics.mean(s['s2'] for s in longer) if longer else 0,
        'same_mean_s2': statistics.mean(s['s2'] for s in same) if same else 0,
        'top_shorter_examples': sorted(shorter, key=lambda x: -x['s2'])[:10],
        'top_longer_examples': sorted(longer, key=lambda x: -x['s2'])[:10],
        'poet_results': poet_results,
        'era_results': [(e, h, a, d, n) for e, h, a, d, n in era_results]
    }

if __name__ == '__main__':
    results = main()
