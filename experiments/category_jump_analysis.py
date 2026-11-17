"""
Category Jump Analysis: What do poets refuse to write?

At genuine (artifact-filtered) high-S2 positions, GPT-2 had a confident prediction
that the poet suppressed. This experiment classifies both the expectation and the
actual choice into semantic/grammatical categories, then studies the "category jump"
-- the class of deviation the poet made.

Research question: When poets achieve genuine high-S2 moments, are they mostly
escaping grammar (function→content), substituting unexpected content (content→content),
or something else? Does this vary by poet, era, or S2 level?
"""

import json
import re
from collections import defaultdict, Counter

# Token classification lists
GRAMMAR_WORDS = {
    # Articles
    'the', 'a', 'an',
    # Pronouns
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
    'my', 'your', 'his', 'its', 'our', 'their', 'mine', 'yours', 'hers', 'ours', 'theirs',
    'myself', 'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',
    'this', 'that', 'these', 'those', 'who', 'whom', 'whose', 'which', 'what',
    # Prepositions
    'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'from', 'up', 'about', 'into',
    'through', 'during', 'before', 'after', 'above', 'below', 'between', 'under', 'over',
    'out', 'off', 'against', 'without', 'within', 'along', 'across', 'behind', 'beyond',
    'down', 'near', 'around', 'among', 'per', 'since', 'until', 'upon', 'toward', 'towards',
    # Conjunctions
    'and', 'or', 'but', 'yet', 'so', 'nor', 'although', 'while', 'though', 'since',
    'because', 'if', 'when', 'as', 'than', 'that', 'whether', 'until', 'unless',
    'however', 'therefore', 'thus', 'then', 'hence',
    # Auxiliary/copula verbs
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am',
    'have', 'has', 'had', 'having', 'do', 'does', 'did',
    'will', 'would', 'could', 'should', 'may', 'might', 'must', 'shall', 'can',
    # Other function words
    'not', 'no', 'never', 'also', 'just', 'very', 'more', 'most', 'much', 'many',
    'all', 'both', 'each', 'every', 'any', 'some', 'few', 'other', 'another',
    'only', 'even', 'still', 'already', 'now', 'here', 'there', 'where', 'how',
    'quite', 'rather', 'such', 'same', 'own', 'like', 'get', 'got',
    # Genitive/contractions
    "'s", "n't", "'re", "'ve", "'ll", "'d", "'m",
}

PUNCT_CHARS = set('.,;:!?-—()[]{}"\'/\\|`~@#$%^&*+=<>')


def classify_token(tok: str) -> str:
    """Classify a token into: NEWLINE, PUNCTUATION, GRAMMAR, CONTENT."""
    if tok.strip() == '':
        return 'WHITESPACE'
    clean = tok.strip().lower()
    if '\n' in tok:
        return 'NEWLINE'
    if all(c in PUNCT_CHARS for c in clean) and len(clean) > 0:
        return 'PUNCTUATION'
    # Remove leading space for lookup
    lookup = clean.lstrip()
    if lookup in GRAMMAR_WORDS:
        return 'GRAMMAR'
    # Mixed punct+word e.g. "word," -- classify by word part
    word_part = re.sub(r'[^\w]', '', lookup)
    if word_part and word_part in GRAMMAR_WORDS:
        return 'GRAMMAR'
    return 'CONTENT'


def analyze(corpus_path: str) -> dict:
    data = json.load(open(corpus_path))

    ARTIFACT_THRESHOLD = 0.90  # p(newline) >= this => artifact
    HIGH_S2_THRESHOLD = 5.0    # bits; genuine high-S2

    # Collect all genuine tokens
    all_tokens = []
    for entry in data:
        meta = entry['metadata']
        for tok in entry['tokens']:
            if tok.get('p_newline', 0) >= ARTIFACT_THRESHOLD:
                continue  # filter artifact
            all_tokens.append({
                's2': tok['s2'],
                'token': tok['token'],
                'entropy': tok['entropy'],
                'surprisal': tok['surprisal'],
                'top_alt': tok['alternatives'][0]['token'] if tok.get('alternatives') else '',
                'top_alt_prob': tok['alternatives'][0]['prob'] if tok.get('alternatives') else 0,
                'context': tok.get('context_before', ''),
                'era': meta.get('era', 'unknown'),
                'author': meta.get('author', 'unknown'),
                'title': meta.get('title', 'unknown'),
                'year': meta.get('year', 0),
            })

    # Compute S2 percentiles for threshold
    s2_vals = [t['s2'] for t in all_tokens]
    s2_vals.sort()
    n = len(s2_vals)
    pct_90 = s2_vals[int(0.90 * n)]
    pct_95 = s2_vals[int(0.95 * n)]
    pct_99 = s2_vals[int(0.99 * n)]

    # Classify all tokens
    for t in all_tokens:
        t['actual_cat'] = classify_token(t['token'])
        t['expected_cat'] = classify_token(t['top_alt'])
        t['jump'] = f"{t['expected_cat']}→{t['actual_cat']}"

    # Analysis 1: Distribution at high-S2 positions (s2 > HIGH_S2_THRESHOLD)
    high_s2_tokens = [t for t in all_tokens if t['s2'] > HIGH_S2_THRESHOLD]

    # Jump distribution at high-S2
    jump_counts = Counter(t['jump'] for t in high_s2_tokens)
    expected_cat_counts = Counter(t['expected_cat'] for t in high_s2_tokens)
    actual_cat_counts = Counter(t['actual_cat'] for t in high_s2_tokens)

    # Analysis 2: Examples of each jump type
    jump_examples = defaultdict(list)
    for t in sorted(high_s2_tokens, key=lambda x: -x['s2'])[:500]:
        jt = t['jump']
        if len(jump_examples[jt]) < 5:
            jump_examples[jt].append(t)

    # Analysis 3: By poet
    poet_jumps = defaultdict(lambda: defaultdict(int))
    for t in high_s2_tokens:
        poet_jumps[t['author']][t['jump']] += 1

    # Analysis 4: Jump distribution by S2 bin
    bins = [
        (HIGH_S2_THRESHOLD, pct_90, 'moderate (5–90th pct)'),
        (pct_90, pct_95, '90th–95th pct'),
        (pct_95, pct_99, '95th–99th pct'),
        (pct_99, float('inf'), 'top 1%'),
    ]
    bin_data = {}
    for lo, hi, label in bins:
        bin_toks = [t for t in all_tokens if lo < t['s2'] <= hi]
        if bin_toks:
            bin_data[label] = {
                'n': len(bin_toks),
                'jumps': Counter(t['jump'] for t in bin_toks),
                'mean_s2': sum(t['s2'] for t in bin_toks) / len(bin_toks),
            }

    # Analysis 5: Era breakdown of dominant jump type
    era_jumps = defaultdict(lambda: defaultdict(int))
    for t in high_s2_tokens:
        era_jumps[t['era']][t['jump']] += 1

    # Analysis 6: Content→Content -- what did they choose vs expect?
    cc_examples = [t for t in high_s2_tokens if t['jump'] == 'CONTENT→CONTENT']
    cc_examples.sort(key=lambda x: -x['s2'])

    return {
        'n_tokens_total': len(all_tokens),
        'n_high_s2': len(high_s2_tokens),
        'threshold_s2': HIGH_S2_THRESHOLD,
        'percentiles': {'p90': pct_90, 'p95': pct_95, 'p99': pct_99},
        'jump_counts': dict(jump_counts.most_common()),
        'expected_cat_counts': dict(expected_cat_counts.most_common()),
        'actual_cat_counts': dict(actual_cat_counts.most_common()),
        'bin_data': {k: {'n': v['n'], 'mean_s2': v['mean_s2'],
                        'jumps': dict(v['jumps'].most_common())}
                     for k, v in bin_data.items()},
        'era_jumps': {era: dict(Counter(jc).most_common(5))
                      for era, jc in era_jumps.items()},
        'jump_examples': {k: v for k, v in jump_examples.items()},
        'cc_top_examples': cc_examples[:20],
        'poet_jumps': {p: dict(Counter(jc).most_common(5))
                       for p, jc in sorted(poet_jumps.items(),
                                           key=lambda x: -sum(x[1].values()))[:30]},
    }


if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    result = analyze('results/corpus_results.json')

    out_path = 'results/category_jump_analysis.json'
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved {out_path}")
    print(f"Total clean tokens: {result['n_tokens_total']}")
    print(f"High-S2 tokens (s2 > {result['threshold_s2']}): {result['n_high_s2']}")
    print("Jump distribution:")
    total = sum(result['jump_counts'].values())
    for jump, cnt in sorted(result['jump_counts'].items(), key=lambda x: -x[1]):
        print(f"  {jump}: {cnt} ({100*cnt/total:.1f}%)")
