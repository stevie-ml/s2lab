"""
Syntactic Prediction Diversity vs S2.

For each token position (artifact-free), measure how syntactically diverse
GPT-2's top-10 alternatives are. Then ask: do high-S2 tokens come from
syntactically narrow (all alternatives in same category) or syntactically
wide (alternatives span many categories) prediction contexts?

New angle: previous work studied POS of chosen tokens; this studies POS of
the prediction distribution itself — the shape of the possibility space.
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/prediction_diversity_s2.json"

# Simple POS classifier for single tokens
FUNCTION_WORDS = {
    'the', 'a', 'an', 'of', 'in', 'on', 'at', 'to', 'for', 'with',
    'by', 'from', 'up', 'about', 'as', 'into', 'through', 'during',
    'before', 'after', 'above', 'below', 'between', 'and', 'but', 'or',
    'nor', 'yet', 'so', 'both', 'either', 'neither', 'not', 'is', 'are',
    'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do',
    'does', 'did', 'will', 'would', 'shall', 'should', 'may', 'might',
    'must', 'can', 'could', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our',
    'their', 'this', 'that', 'these', 'those', 'which', 'who', 'what',
    'when', 'where', 'how', 'if', 'then', 'than', 'because', 'while',
    'although', 'though', 'since', 'until', 'unless', 'however', 'also',
    'such', 'no', 'each', 'all', 'any', 'more', 'most', 'other', 'some',
    'just', 'now', 'only', 'even', 'still', 'here', 'there', 'much', 'many',
    'like', 'very', 'too', 'over', 'back', 'long', 'down', 'way', 'could',
    'come', 'look', 'know', 'take', 'go', 'see', 'make', 'get', 'give',
    'say', 'think', 'seem', 'feel', 'tell', 'try', 'leave', 'keep', 'let',
    'work', 'move', 'live', 'stand', 'turn', 'begin', 'show', 'hear', 'play',
    'run', 'hold', 'bring', 'happen', 'write', 'provide', 'sit', 'talk'
}

PUNCT_CHARS = set('.,;:!?\'"-()[]{}—…')


def classify_token(tok):
    """Classify a token string into a broad syntactic category."""
    t = tok.strip().lower()

    if not t:
        return 'empty'

    # Newline / whitespace
    if t == '\n' or t.isspace():
        return 'newline'

    # Pure punctuation
    if all(c in PUNCT_CHARS for c in t):
        return 'punct'

    # Numeral
    if re.match(r'^-?\d+(\.\d+)?$', t):
        return 'num'

    # Function word
    if t in FUNCTION_WORDS:
        return 'func'

    # Likely adjective: -ful, -less, -ous, -ive, -al, -ic, -ary, -ent, -ant
    if re.search(r'(ful|less|ous|ive|al|ic|ary|ent|ant|able|ible|ish)$', t):
        return 'adj_like'

    # Likely verb: -ing, -ed, -ize, -ify, -ate
    if re.search(r'(ing|ized|ised|ified|ated)$', t) and len(t) > 4:
        return 'verb_like'

    # Likely adverb: -ly
    if t.endswith('ly') and len(t) > 4:
        return 'adv_like'

    # Default: treat as noun/content word
    return 'noun_like'


def diversity_score(alt_tokens):
    """Count distinct syntactic categories among alternatives."""
    cats = set()
    for tok in alt_tokens:
        cats.add(classify_token(tok))
    # Exclude newline/empty from diversity
    cats.discard('newline')
    cats.discard('empty')
    return len(cats)


def compute_diversity_for_poem(poem):
    """Return list of (s2, diversity, era, is_high_s2) for artifact-free tokens."""
    era = poem['metadata']['era']
    rows = []
    for t in poem['tokens']:
        if t.get('p_newline', 1.0) >= 0.9:
            continue
        s2 = t['s2']
        alts = t.get('alternatives', [])
        alt_tokens = [a['token'] for a in alts[:10]]
        div = diversity_score(alt_tokens)
        rows.append({'s2': s2, 'diversity': div, 'era': era,
                     'token': t['token'].strip()})
    return rows


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    all_rows = []
    for poem in data:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        all_rows.extend(compute_diversity_for_poem(poem))

    if not all_rows:
        print("No data!")
        return

    # Bin by S2 level
    bins = {
        'very_low (<-3)': [],
        'low (-3 to -1)': [],
        'neutral (-1 to 1)': [],
        'high (1 to 3)': [],
        'very_high (>3)': [],
    }
    for r in all_rows:
        s = r['s2']
        if s < -3:
            bins['very_low (<-3)'].append(r['diversity'])
        elif s < -1:
            bins['low (-3 to -1)'].append(r['diversity'])
        elif s < 1:
            bins['neutral (-1 to 1)'].append(r['diversity'])
        elif s < 3:
            bins['high (1 to 3)'].append(r['diversity'])
        else:
            bins['very_high (>3)'].append(r['diversity'])

    print("\n=== DIVERSITY BY S2 BIN ===")
    print(f"{'S2 Bin':<22} {'n':>6} {'mean div':>10} {'median':>8} {'1-cat%':>8} {'4+cat%':>8}")
    print("-" * 70)
    bin_summary = {}
    for label, divs in bins.items():
        if not divs:
            continue
        mn = statistics.mean(divs)
        med = statistics.median(divs)
        one_cat = sum(1 for d in divs if d == 1) / len(divs) * 100
        four_plus = sum(1 for d in divs if d >= 4) / len(divs) * 100
        print(f"{label:<22} {len(divs):>6} {mn:>10.3f} {med:>8.1f} {one_cat:>8.1f}% {four_plus:>8.1f}%")
        bin_summary[label] = {
            'n': len(divs), 'mean_div': round(mn, 3), 'median_div': med,
            'pct_1cat': round(one_cat, 1), 'pct_4plus': round(four_plus, 1)
        }

    # Era-level: average diversity among high-S2 tokens vs all tokens
    era_data = defaultdict(lambda: {'high_divs': [], 'all_divs': []})
    for r in all_rows:
        era_data[r['era']]['all_divs'].append(r['diversity'])
        if r['s2'] >= 3.0:
            era_data[r['era']]['high_divs'].append(r['diversity'])

    print("\n=== ERA: HIGH-S2 DIVERSITY vs BASELINE ===")
    print(f"{'Era':<25} {'n poems':>7} {'base div':>9} {'high div':>9} {'Δ':>6}")
    print("-" * 60)
    era_summary = {}
    for era, d in sorted(era_data.items()):
        if len(d['all_divs']) < 50:
            continue
        base = statistics.mean(d['all_divs'])
        if d['high_divs']:
            high = statistics.mean(d['high_divs'])
            delta = high - base
        else:
            high = None
            delta = None
        era_summary[era] = {
            'n': len(d['all_divs']),
            'n_high': len(d['high_divs']),
            'base_div': round(base, 3),
            'high_div': round(high, 3) if high else None,
            'delta': round(delta, 3) if delta else None,
        }
        delta_str = f"{delta:+.3f}" if delta is not None else "N/A"
        high_str = f"{high:.3f}" if high else "N/A"
        print(f"{era:<25} {len(d['all_divs']):>7} {base:>9.3f} {high_str:>9} {delta_str:>6}")

    # Diversity distribution overall
    all_divs = [r['diversity'] for r in all_rows]
    print(f"\n=== OVERALL DIVERSITY DISTRIBUTION ===")
    print(f"Total artifact-free tokens: {len(all_divs)}")
    for d_val in range(1, 7):
        cnt = sum(1 for d in all_divs if d == d_val)
        pct = cnt / len(all_divs) * 100
        print(f"  Diversity {d_val}: {cnt:>6} ({pct:.1f}%)")

    # Save results
    output = {
        'total_tokens': len(all_rows),
        'bin_summary': bin_summary,
        'era_summary': era_summary,
        'overall_distribution': {
            str(d): sum(1 for x in all_divs if x == d)
            for d in range(1, 7)
        }
    }
    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == '__main__':
    main()
