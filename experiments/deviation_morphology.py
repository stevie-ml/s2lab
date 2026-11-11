"""
Deviation Morphology: How Poets Leap from Expected to Chosen

For each high-S2 token, we examine the CHARACTER-LEVEL relationship between
the actual chosen token and GPT-2's top prediction. The question:

  Is poetic surprise achieved by choosing words SIMILAR to expectations
  (near-miss: different word, similar form) or by choosing words that are
  ORTHOGONAL to predictions (category leap)?

We classify deviations into four morphological types:
  1. Phonological near-miss: chosen token shares ≥40% character bigrams with top-1
  2. Morphological variant: same root but different suffix/inflection
  3. Length-matched substitute: same token length ±1, low character overlap
  4. Radical departure: short top-1 or very low character similarity

Then: which types dominate by era, author, and poem structure?
"""

import json
import re
import string
from collections import defaultdict

CORPUS = '/home/user/s2lab/results/corpus_results.json'
OUTPUT  = '/home/user/s2lab/results/deviation_morphology.json'

# ── helpers ──────────────────────────────────────────────────────────────────

def clean_token(tok: str) -> str:
    """Strip leading space and punctuation used by GPT-2 tokenizer."""
    return tok.strip().lower().strip(string.punctuation)

def char_bigrams(s: str) -> set:
    s = s.lower()
    if len(s) < 2:
        return {s}
    return {s[i:i+2] for i in range(len(s) - 1)}

def jaccard(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    bg_a = char_bigrams(a)
    bg_b = char_bigrams(b)
    if not bg_a or not bg_b:
        return 0.0
    inter = len(bg_a & bg_b)
    union = len(bg_a | bg_b)
    return inter / union if union > 0 else 0.0

SUFFIXES = ('ing', 'ed', 'er', 'est', 'ly', 'tion', 'ness', 'ment',
            'ful', 'less', 'ity', 'ive', 'al', 'ous', 'ic', 's', 'es',
            'en', 'ist', 'ism', 'ize', 'ise', 'age', 'ure', 'ance', 'ence')

def stem(w: str) -> str:
    """Very rough stemming — strip common suffixes."""
    for suf in sorted(SUFFIXES, key=len, reverse=True):
        if w.endswith(suf) and len(w) - len(suf) >= 3:
            return w[:-len(suf)]
    return w

def is_real_word(tok: str) -> bool:
    """True if token represents a real word (not subword fragment, punct, or whitespace)."""
    c = clean_token(tok)
    if len(c) < 2:
        return False
    # Must contain at least one alphabetic character
    if not any(ch.isalpha() for ch in c):
        return False
    # Reject likely subword fragments: tokens that start with non-alpha after strip
    # (e.g. ' op', ' o', ' val' fragments)
    if len(c) <= 2:
        return False
    return True

STRUCTURAL_TOKENS = {'\n', '\r\n', '.', ',', '!', '?', ';', ':', '—', '–', '-', '...', "'", '"', '(', ')'}

def is_structural(raw: str) -> bool:
    """True if the raw token is a structural/punctuation token."""
    s = raw.strip()
    if not s:
        return True
    if s in STRUCTURAL_TOKENS:
        return True
    if all(ch in string.punctuation or ch.isspace() for ch in s):
        return True
    return False

def classify_deviation(chosen: str, top1: str) -> str:
    """Classify the morphological type of deviation between chosen and top-1 prediction."""
    # Case: structural vs word (or vice versa) = structural surprise
    chosen_struct = is_structural(chosen)
    top1_struct   = is_structural(top1)
    if chosen_struct != top1_struct:
        return 'structural_surprise'    # poet wrote word where punct expected, or vice versa

    c = clean_token(chosen)
    t = clean_token(top1)

    if not c or not t or not any(ch.isalpha() for ch in c) or not any(ch.isalpha() for ch in t):
        return 'other'

    j = jaccard(c, t)
    len_c, len_t = len(c), len(t)
    len_ratio = min(len_c, len_t) / max(len_c, len_t) if max(len_c, len_t) > 0 else 1.0

    # Same stem?
    same_stem = stem(c) == stem(t) and len(stem(c)) >= 3

    if same_stem:
        return 'morphological_variant'       # e.g. "running"/"run", "darker"/"dark"
    elif j >= 0.5:
        return 'phonological_near_miss'      # e.g. "light"/"night", "love"/"live"
    elif j >= 0.25 and len_ratio >= 0.6:
        return 'partial_overlap'             # shares some bigrams, similar length
    elif len_ratio >= 0.75:
        return 'length_matched_substitute'   # same length, different root
    else:
        return 'radical_departure'           # completely different form


def is_content(tok: str) -> bool:
    """Very rough heuristic: is the token a content word?"""
    t = clean_token(tok)
    # common function words
    FUNCTION = {
        'the', 'a', 'an', 'of', 'in', 'to', 'and', 'or', 'but', 'for',
        'on', 'at', 'by', 'with', 'from', 'is', 'are', 'was', 'were',
        'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
        'will', 'would', 'could', 'should', 'may', 'might', 'shall',
        'that', 'this', 'these', 'those', 'it', 'its', 'i', 'you',
        'he', 'she', 'we', 'they', 'my', 'your', 'his', 'her', 'our',
        'their', 'me', 'him', 'us', 'them', 'not', 'no', 'so', 'as',
        'if', 'when', 'while', 'than', 'then', 'up', 'out', 'into',
    }
    return t not in FUNCTION and len(t) > 1

# ── main analysis ─────────────────────────────────────────────────────────────

def analyze():
    with open(CORPUS) as f:
        data = json.load(f)

    # Global buckets
    type_stats  = defaultdict(lambda: {'n': 0, 's2_sum': 0.0, 's2_vals': []})

    # Era buckets
    era_types   = defaultdict(lambda: defaultdict(int))
    era_tokens  = defaultdict(int)   # total high-S2 tokens per era

    # Author buckets
    author_types = defaultdict(lambda: defaultdict(int))
    author_meta  = {}

    # For each deviation event: store detail
    events = []

    total_high_s2 = 0
    skipped_no_alt = 0

    for poem in data:
        meta    = poem['metadata']
        author  = meta.get('author', 'Unknown')
        era     = meta.get('era', 'unknown')
        lang    = meta.get('language', 'en')

        if lang != 'en':
            continue

        for tok in poem['tokens']:
            # Artifact filter
            if tok.get('p_newline', 0) >= 0.9:
                continue
            if tok['s2'] < 2.0:
                continue

            alts = tok.get('alternatives', [])
            if not alts:
                skipped_no_alt += 1
                continue

            top1 = alts[0]['token']
            chosen = tok['token']

            # Skip subword fragments and punctuation-only tokens
            if not is_real_word(chosen) and not is_real_word(top1):
                continue

            dev_type = classify_deviation(chosen, top1)

            type_stats[dev_type]['n']       += 1
            type_stats[dev_type]['s2_sum']  += tok['s2']
            type_stats[dev_type]['s2_vals'].append(tok['s2'])

            era_types[era][dev_type]        += 1
            era_tokens[era]                 += 1
            author_types[author][dev_type]  += 1
            author_meta[author]             = era
            total_high_s2 += 1

            # Store event details (sample up to 300 for inspection)
            if len(events) < 300:
                events.append({
                    'title':   meta.get('title', '?'),
                    'author':  author,
                    'era':     era,
                    'chosen':  chosen,
                    'top1':    top1,
                    'type':    dev_type,
                    's2':      round(tok['s2'], 2),
                    'entropy': round(tok['entropy'], 2),
                    'rank':    tok.get('rank', -1),
                    'jaccard': round(jaccard(clean_token(chosen), clean_token(top1)), 3),
                })

    # Compute per-type percentages
    global_pct = {}
    for t, st in type_stats.items():
        st['mean_s2'] = st['s2_sum'] / st['n'] if st['n'] else 0
        # sort and compute median
        v = sorted(st['s2_vals'])
        st['median_s2'] = v[len(v)//2] if v else 0
        st['pct'] = round(100 * st['n'] / total_high_s2, 1) if total_high_s2 else 0
        del st['s2_vals']  # too large for JSON
        global_pct[t] = st['pct']

    # Era table: for each era, fraction of each deviation type
    era_table = {}
    for era, counts in era_types.items():
        total = era_tokens[era]
        era_table[era] = {
            t: round(100 * counts.get(t, 0) / total, 1)
            for t in type_stats
        }
        era_table[era]['total_high_s2'] = total

    # Author table: top 20 by total high-S2 count
    author_rows = []
    for auth, counts in author_types.items():
        total = sum(counts.values())
        if total < 5:
            continue
        radical = counts.get('radical_departure', 0)
        phono   = counts.get('phonological_near_miss', 0)
        morph   = counts.get('morphological_variant', 0)
        sub     = counts.get('length_matched_substitute', 0)
        author_rows.append({
            'author': auth,
            'era': author_meta[auth],
            'total': total,
            'radical_pct': round(100 * radical / total, 1),
            'phonological_pct': round(100 * phono / total, 1),
            'morphological_pct': round(100 * morph / total, 1),
            'substitute_pct': round(100 * sub / total, 1),
        })
    author_rows.sort(key=lambda r: r['total'], reverse=True)

    result = {
        'meta': {
            'total_high_s2_tokens': total_high_s2,
            'skipped_no_alternatives': skipped_no_alt,
            'threshold': 'S2 >= 2.0, p_newline < 0.9, English only',
        },
        'global': dict(type_stats),
        'global_pct': global_pct,
        'era_table': era_table,
        'author_table': author_rows[:30],
        'sample_events': events,
    }

    with open(OUTPUT, 'w') as f:
        json.dump(result, f, indent=2)

    return result

# ── entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    r = analyze()
    print(f"\nTotal high-S2 tokens analyzed: {r['meta']['total_high_s2_tokens']}")
    print("\n=== Global Deviation Types ===")
    for t, st in sorted(r['global'].items(), key=lambda x: -x[1]['n']):
        print(f"  {t:30s}  n={st['n']:4d}  {st['pct']:4.1f}%  mean_s2={st['mean_s2']:.2f}")
    print("\nSaved:", OUTPUT)
