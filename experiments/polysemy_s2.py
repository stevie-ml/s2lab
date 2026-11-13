"""
Polysemy and S2: Does Word Ambiguity Drive Information Spikes?

Hypothesis: Multiply-defined words (high WordNet synset count) have higher S2 in poetry
because semantic ambiguity forces GPT-2 to spread probability across interpretations,
creating structural opportunity for surprise.

We use WordNet synset count as a standard polysemy proxy, controlling for frequency.
"""

import json
import re
import statistics
from collections import defaultdict

# Try NLTK WordNet
try:
    import nltk
    from nltk.corpus import wordnet as wn
    nltk.download('wordnet', quiet=True)
    nltk.download('omw-1.4', quiet=True)
    HAS_WORDNET = True
except ImportError:
    HAS_WORDNET = False
    print("WARNING: NLTK not available, using fallback polysemy data")

RESULTS_FILE = "results/corpus_results.json"
OUTPUT_FILE  = "results/polysemy_s2.json"

def clean_token(tok):
    """Strip GPT-2 leading space and lowercase."""
    return tok.strip().lower()

def get_synset_count(word, pos=None):
    """Return the number of WordNet synsets for a word (across all POS if pos=None)."""
    if not HAS_WORDNET:
        return None
    synsets = wn.synsets(word)
    return len(synsets)

def get_synset_count_by_pos(word):
    """Return synset counts broken down by POS."""
    if not HAS_WORDNET:
        return {}
    counts = {}
    for pos_tag, pos_name in [(wn.NOUN, 'noun'), (wn.VERB, 'verb'),
                               (wn.ADJ, 'adj'), (wn.ADV, 'adv')]:
        c = len(wn.synsets(word, pos=pos_tag))
        if c:
            counts[pos_name] = c
    return counts

def is_content_word(tok):
    """Very light filter: exclude punctuation, numbers, typical function words."""
    t = clean_token(tok)
    # Remove tokens that are only punctuation or digits
    if re.match(r'^[\W\d]+$', t):
        return False
    # Exclude the very highest-frequency function words
    FUNCTION_WORDS = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'shall', 'can', 'must', 'it', 'its',
        'this', 'that', 'these', 'those', 'my', 'your', 'his', 'her', 'our',
        'their', 'i', 'you', 'he', 'she', 'we', 'they', 'me', 'him', 'us',
        'them', 'as', 'if', 'not', 'no', 'nor', 'so', 'yet', 'both', 'either',
        'each', 'all', 'any', 'more', 'most', 'such', 'than', 'then', 'when',
        'where', 'while', 'how', 'who', 'which', 'what', 'whom', 'whose',
    }
    return t not in FUNCTION_WORDS

def bucket_polysemy(n_synsets):
    """Group synset count into named buckets."""
    if n_synsets == 0:
        return 'hapax/OOV'  # not in WordNet
    elif n_synsets == 1:
        return 'monosemous (1)'
    elif n_synsets <= 3:
        return 'low (2-3)'
    elif n_synsets <= 7:
        return 'medium (4-7)'
    elif n_synsets <= 15:
        return 'high (8-15)'
    else:
        return 'very_high (16+)'

BUCKET_ORDER = ['hapax/OOV', 'monosemous (1)', 'low (2-3)', 'medium (4-7)', 'high (8-15)', 'very_high (16+)']

def bucket_frequency(log_prob):
    """Bucket token frequency by log-probability."""
    if log_prob is None:
        return 'unknown'
    # prob is stored directly; convert to log scale
    import math
    if log_prob <= 0:
        return 'unknown'
    lp = math.log2(log_prob)
    if lp < -20:
        return 'very_rare (<2^-20)'
    elif lp < -15:
        return 'rare (2^-20 to 2^-15)'
    elif lp < -10:
        return 'uncommon (2^-15 to 2^-10)'
    elif lp < -5:
        return 'common (2^-10 to 2^-5)'
    else:
        return 'very_common (>2^-5)'

def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} poems")

    # Collect word-level data
    word_data = {}  # word -> {'s2_values': [...], 'synsets': int, 'era_s2': {era: [...]}}
    token_records = []  # flat list of records

    n_processed = 0
    n_wordnet_hits = 0

    for poem in corpus:
        meta = poem.get('metadata', {})
        era = meta.get('era', 'unknown')
        language = meta.get('language', 'en')

        # Skip non-English poems
        if language not in ('en', 'english', None, ''):
            continue

        for tok_data in poem.get('tokens', []):
            tok = tok_data.get('token', '')
            s2 = tok_data.get('s2')
            prob = tok_data.get('prob')
            p_newline = tok_data.get('p_newline', 0)

            # Filter artifacts
            if p_newline > 0.9:
                continue
            if s2 is None:
                continue

            word = clean_token(tok)
            if not word or not is_content_word(tok):
                continue

            n_processed += 1

            # Get polysemy
            n_synsets = get_synset_count(word)
            if n_synsets is None:
                continue  # no WordNet

            if n_synsets > 0:
                n_wordnet_hits += 1

            # Accumulate by word
            if word not in word_data:
                word_data[word] = {
                    'n_synsets': n_synsets,
                    's2_values': [],
                    'era_s2': defaultdict(list),
                    'pos_synsets': get_synset_count_by_pos(word),
                }
            word_data[word]['s2_values'].append(s2)
            word_data[word]['era_s2'][era].append(s2)

            token_records.append({
                'word': word,
                'n_synsets': n_synsets,
                's2': s2,
                'prob': prob,
                'era': era,
                'bucket': bucket_polysemy(n_synsets),
            })

    print(f"Processed {n_processed} content tokens, {n_wordnet_hits} with WordNet hits")
    print(f"Unique words: {len(word_data)}")

    # 1. S2 by polysemy bucket
    bucket_s2 = defaultdict(list)
    for rec in token_records:
        bucket_s2[rec['bucket']].append(rec['s2'])

    print("\n=== S2 by Polysemy Bucket ===")
    bucket_summary = {}
    for b in BUCKET_ORDER:
        vals = bucket_s2[b]
        if not vals:
            continue
        m = statistics.mean(vals)
        med = statistics.median(vals)
        std = statistics.stdev(vals) if len(vals) > 1 else 0
        spike_rate = sum(1 for v in vals if v >= 3.0) / len(vals)
        print(f"  {b:<22}: n={len(vals):6d}  mean={m:+.3f}  median={med:+.3f}  spike%={spike_rate:.1%}")
        bucket_summary[b] = {
            'n': len(vals), 'mean_s2': round(m, 4),
            'median_s2': round(med, 4), 'std_s2': round(std, 4),
            'spike_rate': round(spike_rate, 4)
        }

    # 2. Correlation: synset count vs S2
    # Use Pearson r on the token-level data (excluding OOV, capped at 30 synsets)
    pairs = [(rec['n_synsets'], rec['s2'])
             for rec in token_records if rec['n_synsets'] > 0 and rec['n_synsets'] <= 30]
    if len(pairs) > 10:
        import math
        xs = [p[0] for p in pairs]
        ys = [p[1] for p in pairs]
        n = len(xs)
        mx, my = statistics.mean(xs), statistics.mean(ys)
        sx, sy = statistics.stdev(xs), statistics.stdev(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n - 1)
        r = cov / (sx * sy) if sx * sy > 0 else 0
        print(f"\nPearson r(polysemy, S2): {r:.4f}  (n={n})")
    else:
        r = None
        print("\nToo few pairs for correlation")

    # 3. Word-level: mean S2 by mean synset count
    # Group by exact synset count
    synset_to_s2 = defaultdict(list)
    for word, wd in word_data.items():
        ns = wd['n_synsets']
        if ns > 0:
            mean_s2 = statistics.mean(wd['s2_values'])
            synset_to_s2[ns].append(mean_s2)

    synset_profile = {}
    print("\n=== Word-Level: Mean S2 by Synset Count (1–20) ===")
    for ns in range(1, 21):
        vals = synset_to_s2[ns]
        if len(vals) >= 5:
            m = statistics.mean(vals)
            synset_profile[ns] = {'n_words': len(vals), 'mean_s2': round(m, 4)}
            print(f"  synsets={ns:2d}: {len(vals):5d} words, mean_s2={m:+.3f}")

    # 4. Top polysemous words: highest S2
    high_poly = [(w, d) for w, d in word_data.items() if d['n_synsets'] >= 10 and len(d['s2_values']) >= 5]
    high_poly.sort(key=lambda x: -statistics.mean(x[1]['s2_values']))

    print("\n=== Top High-Polysemy Words by Mean S2 ===")
    top_high = []
    for w, d in high_poly[:20]:
        m = statistics.mean(d['s2_values'])
        print(f"  {w:<20} synsets={d['n_synsets']:3d}  mean_s2={m:+.3f}  n={len(d['s2_values'])}")
        top_high.append({'word': w, 'n_synsets': d['n_synsets'],
                         'mean_s2': round(m, 4), 'n_appearances': len(d['s2_values'])})

    # 5. Bottom: most polysemous but lowest S2
    high_poly.sort(key=lambda x: statistics.mean(x[1]['s2_values']))
    top_low = []
    print("\n=== High-Polysemy Words with LOWEST S2 (expected even though ambiguous) ===")
    for w, d in high_poly[:15]:
        m = statistics.mean(d['s2_values'])
        print(f"  {w:<20} synsets={d['n_synsets']:3d}  mean_s2={m:+.3f}  n={len(d['s2_values'])}")
        top_low.append({'word': w, 'n_synsets': d['n_synsets'],
                        'mean_s2': round(m, 4), 'n_appearances': len(d['s2_values'])})

    # 6. Monosemous high-S2 words: words with exactly 1 synset but very high S2
    mono_high = [(w, d) for w, d in word_data.items()
                 if d['n_synsets'] == 1 and len(d['s2_values']) >= 3
                 and statistics.mean(d['s2_values']) > 2.0]
    mono_high.sort(key=lambda x: -statistics.mean(x[1]['s2_values']))
    print("\n=== Monosemous High-S2 Words (pure surprise without ambiguity) ===")
    top_mono = []
    for w, d in mono_high[:20]:
        m = statistics.mean(d['s2_values'])
        print(f"  {w:<20} synsets=1  mean_s2={m:+.3f}  n={len(d['s2_values'])}")
        top_mono.append({'word': w, 'mean_s2': round(m, 4), 'n_appearances': len(d['s2_values'])})

    # 7. Era breakdown: does polysemy-S2 correlation differ by era?
    era_poly_s2 = defaultdict(lambda: defaultdict(list))
    for rec in token_records:
        if rec['n_synsets'] > 0:
            bucket = 'high_poly' if rec['n_synsets'] >= 8 else 'low_poly'
            era_poly_s2[rec['era']][bucket].append(rec['s2'])

    era_comparison = {}
    print("\n=== Era Comparison: High vs Low Polysemy S2 Gap ===")
    for era in sorted(era_poly_s2.keys()):
        hi = era_poly_s2[era]['high_poly']
        lo = era_poly_s2[era]['low_poly']
        if len(hi) >= 20 and len(lo) >= 20:
            gap = statistics.mean(hi) - statistics.mean(lo)
            era_comparison[era] = {
                'high_poly_mean_s2': round(statistics.mean(hi), 4),
                'low_poly_mean_s2': round(statistics.mean(lo), 4),
                'gap': round(gap, 4),
                'n_high': len(hi), 'n_low': len(lo)
            }
            print(f"  {era:<25} gap={gap:+.3f}  hi={statistics.mean(hi):+.3f}(n={len(hi)})  lo={statistics.mean(lo):+.3f}(n={len(lo)})")

    # Save results
    output = {
        'summary': {
            'n_poems': len(corpus),
            'n_tokens_processed': n_processed,
            'n_wordnet_hits': n_wordnet_hits,
            'n_unique_words': len(word_data),
            'pearson_r_polysemy_s2': round(r, 4) if r is not None else None,
        },
        'bucket_summary': bucket_summary,
        'synset_profile': synset_profile,
        'top_high_polysemy_high_s2': top_high,
        'top_high_polysemy_low_s2': top_low,
        'top_monosemous_high_s2': top_mono,
        'era_comparison': era_comparison,
    }

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {OUTPUT_FILE}")

if __name__ == '__main__':
    main()
