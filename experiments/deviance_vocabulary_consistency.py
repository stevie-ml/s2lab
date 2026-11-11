"""
Deviance Vocabulary Consistency: Do poets have a stable 'surprise lexicon' across poems?

For each poet with >= 3 poems, we ask:
  - Is the set of high-S2 tokens consistent across poems by the same poet?
  - Do poets have a stable "signature vocabulary of deviance"?
  - Is the suppressed vocabulary (GPT-2's top predictions at high-S2 positions) also stable?

Method:
  1. For each poem: collect the set of unique high-S2 token types (clean, S2 > THRESHOLD)
  2. For each poet with >= 3 poems: compute all pairwise Jaccard similarities
     (intersection / union of high-S2 vocabularies between poem pairs)
  3. Compare within-poet Jaccard vs between-poet Jaccard
  4. Find poets with the most / least consistent deviance vocabulary
  5. Catalog the "signature" deviance words for major poets

Builds on: poet_fingerprints.md, poet_suppression_profiles.md, suppressed_lexicon.md
"""

import json
import re
from collections import defaultdict
from itertools import combinations

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/deviance_vocabulary_consistency.json"
S2_THRESHOLD = 2.0
P_NEWLINE_ARTIFACT = 0.9  # exclude stanza-break artifact positions
MIN_POEMS_PER_POET = 3
MIN_TOKENS_PER_POEM = 5  # minimum high-S2 tokens for Jaccard to be meaningful

def clean_token(tok):
    """Normalize token: lowercase, strip leading space and subword markers."""
    t = tok.strip().lstrip()
    t = re.sub(r'^[^a-zA-Z0-9]+', '', t)
    t = t.lower()
    return t

def is_alphabetic(tok):
    cleaned = clean_token(tok)
    return bool(re.match(r'^[a-zA-Z]{2,}$', cleaned))

def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    if not set_a or not set_b:
        return 0.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union > 0 else 0.0

def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def extract_poem_deviance_vocab(poem, threshold=S2_THRESHOLD):
    """Return set of unique word types at high-S2 positions (artifact-cleaned)."""
    high_s2_words = set()
    suppressed_words = set()  # top GPT-2 prediction at each high-S2 position

    for tok in poem.get('tokens', []):
        # Skip stanza-break artifacts
        if tok.get('p_newline', 0) >= P_NEWLINE_ARTIFACT:
            continue

        s2 = tok.get('s2', 0)
        if s2 >= threshold:
            word = clean_token(tok['token'])
            if is_alphabetic(word):
                high_s2_words.add(word)

            # Track what GPT-2 expected (suppressed word)
            alternatives = tok.get('alternatives', [])
            for alt in alternatives[:1]:  # top-1 prediction
                alt_word = clean_token(alt['token'])
                if is_alphabetic(alt_word):
                    suppressed_words.add(alt_word)

    return high_s2_words, suppressed_words

def analyze_poet_consistency(poet_poems):
    """
    Given a list of (poem_title, high_s2_vocab, suppressed_vocab) tuples,
    compute pairwise Jaccard similarities and other metrics.
    """
    if len(poet_poems) < 2:
        return None

    # Filter to poems with enough high-S2 tokens
    valid = [(t, v, s) for t, v, s in poet_poems if len(v) >= MIN_TOKENS_PER_POEM]

    if len(valid) < 2:
        return None

    titles = [t for t, v, s in valid]
    vocabs = [v for t, v, s in valid]
    suppressed = [s for t, v, s in valid]

    # Pairwise Jaccard for actual deviance vocab
    jaccards = []
    for i, j in combinations(range(len(vocabs)), 2):
        jaccards.append(jaccard(vocabs[i], vocabs[j]))

    # Pairwise Jaccard for suppressed (shadow) vocab
    supp_jaccards = []
    for i, j in combinations(range(len(suppressed)), 2):
        supp_jaccards.append(jaccard(suppressed[i], suppressed[j]))

    # Union of all high-S2 tokens across poems
    all_words = set()
    for v in vocabs:
        all_words |= v

    # Core vocabulary: words appearing in >= 50% of poems
    n = len(vocabs)
    word_counts = defaultdict(int)
    for v in vocabs:
        for w in v:
            word_counts[w] += 1
    core_vocab = {w for w, c in word_counts.items() if c >= max(2, n * 0.5)}

    # Signature words (appear in >= 2 poems)
    signature_words = [(w, c) for w, c in sorted(word_counts.items(), key=lambda x: -x[1]) if c >= 2]

    return {
        'n_poems': len(valid),
        'mean_vocab_size': sum(len(v) for v in vocabs) / len(vocabs),
        'mean_jaccard': sum(jaccards) / len(jaccards) if jaccards else 0.0,
        'max_jaccard': max(jaccards) if jaccards else 0.0,
        'mean_suppressed_jaccard': sum(supp_jaccards) / len(supp_jaccards) if supp_jaccards else 0.0,
        'total_unique_words': len(all_words),
        'core_vocab': sorted(core_vocab),
        'signature_words': signature_words[:20],
        'poems': titles,
        'per_poem_vocab_sizes': [len(v) for v in vocabs],
    }

def main():
    data = load_data()

    # Group poems by poet
    poet_poems_raw = defaultdict(list)  # author -> list of (title, vocab, suppressed)

    for poem in data:
        meta = poem.get('metadata', {})
        author = meta.get('author', 'Unknown')
        title = meta.get('title', 'Untitled')
        era = meta.get('era', '')

        vocab, suppressed = extract_poem_deviance_vocab(poem)
        poet_poems_raw[author].append((title, vocab, suppressed, era))

    # Compute consistency for poets with enough poems
    results = {}
    for author, poems in poet_poems_raw.items():
        if len(poems) < MIN_POEMS_PER_POET:
            continue

        analysis = analyze_poet_consistency([(t, v, s) for t, v, s, _e in poems])
        if analysis is None:
            continue

        analysis['era'] = poems[0][3] if poems else ''
        results[author] = analysis

    # Cross-poet Jaccard (between-poet baseline)
    # Sample random pairs from different poets
    all_poet_vocabs = []
    for author, poems in poet_poems_raw.items():
        combined = set()
        for t, v, s, _e in poems:
            combined |= v
        if len(combined) >= MIN_TOKENS_PER_POEM:
            all_poet_vocabs.append((author, combined))

    # Random between-poet Jaccard
    import random
    random.seed(42)
    between_jaccards = []
    pairs = list(combinations(range(len(all_poet_vocabs)), 2))
    sample_pairs = random.sample(pairs, min(500, len(pairs)))
    for i, j in sample_pairs:
        between_jaccards.append(jaccard(all_poet_vocabs[i][1], all_poet_vocabs[j][1]))

    mean_between = sum(between_jaccards) / len(between_jaccards) if between_jaccards else 0

    # Sort poets by within-poet consistency
    sorted_poets = sorted(results.items(), key=lambda x: -x[1]['mean_jaccard'])

    # Compile summary
    all_within_jaccards = [v['mean_jaccard'] for v in results.values()]
    mean_within = sum(all_within_jaccards) / len(all_within_jaccards) if all_within_jaccards else 0

    all_suppressed_jaccards = [v['mean_suppressed_jaccard'] for v in results.values()]
    mean_suppressed = sum(all_suppressed_jaccards) / len(all_suppressed_jaccards) if all_suppressed_jaccards else 0

    output = {
        'summary': {
            'n_poets_analyzed': len(results),
            'threshold': S2_THRESHOLD,
            'mean_within_poet_jaccard': round(mean_within, 4),
            'mean_between_poet_jaccard': round(mean_between, 4),
            'mean_suppressed_vocab_jaccard': round(mean_suppressed, 4),
            'consistency_lift': round(mean_within / mean_between, 3) if mean_between > 0 else None,
        },
        'most_consistent': [
            {
                'author': author,
                'mean_jaccard': round(v['mean_jaccard'], 4),
                'suppressed_jaccard': round(v['mean_suppressed_jaccard'], 4),
                'n_poems': v['n_poems'],
                'core_vocab': v['core_vocab'][:10],
                'signature_words': [(w, c) for w, c in v['signature_words'][:10]],
            }
            for author, v in sorted_poets[:15]
        ],
        'least_consistent': [
            {
                'author': author,
                'mean_jaccard': round(v['mean_jaccard'], 4),
                'n_poems': v['n_poems'],
                'mean_vocab_size': round(v['mean_vocab_size'], 1),
            }
            for author, v in sorted_poets[-10:]
        ],
        'full_results': {
            author: {
                'mean_jaccard': round(v['mean_jaccard'], 4),
                'suppressed_jaccard': round(v['mean_suppressed_jaccard'], 4),
                'n_poems': v['n_poems'],
                'mean_vocab_size': round(v['mean_vocab_size'], 1),
                'total_unique_words': v['total_unique_words'],
                'core_vocab': v['core_vocab'],
                'signature_words': v['signature_words'],
            }
            for author, v in results.items()
        }
    }

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)

    # Print summary
    print(f"Poets analyzed: {len(results)}")
    print(f"Mean within-poet Jaccard: {mean_within:.4f}")
    print(f"Mean between-poet Jaccard: {mean_between:.4f}")
    print(f"Consistency lift: {mean_within / mean_between:.3f}x" if mean_between > 0 else "N/A")
    print(f"Mean suppressed vocab Jaccard: {mean_suppressed:.4f}")
    print()
    print("Most consistent deviance vocabularies:")
    for author, v in sorted_poets[:10]:
        sig = [w for w, c in v['signature_words'][:5]]
        print(f"  {author}: J={v['mean_jaccard']:.3f} (n={v['n_poems']}), core: {sig}")
    print()
    print("Least consistent:")
    for author, v in sorted_poets[-5:]:
        print(f"  {author}: J={v['mean_jaccard']:.3f} (n={v['n_poems']})")

    return output

if __name__ == '__main__':
    main()
