"""
Semantic Surprise Transition Matrix
====================================
At high-S2 moments, GPT-2 expects one category of word; the poet chooses another.
This experiment builds a semantic transition matrix: what did the model expect →
what did the poet write?

Categories: spatial/motion, temporal, emotional, concrete, abstract, function

Hypothesis: Different poetic movements have characteristic semantic "pivot" types.
Romantics turn motion into emotion; Modernists turn function words into concrete images.
"""

import json
import re
from collections import defaultdict, Counter
from pathlib import Path

# Simple keyword-based semantic tagger
SPATIAL_MOTION = {
    'in', 'out', 'through', 'around', 'into', 'to', 'from', 'over', 'under',
    'by', 'at', 'up', 'down', 'across', 'along', 'beside', 'between', 'beyond',
    'near', 'above', 'below', 'toward', 'away', 'back', 'forward', 'forth',
    'came', 'come', 'go', 'went', 'walk', 'walked', 'run', 'ran', 'fly', 'flew',
    'move', 'moved', 'fall', 'fell', 'rise', 'rose', 'pass', 'passed', 'through',
    'return', 'returned', 'reach', 'reached', 'turn', 'turned', 'leave', 'left',
    'enter', 'entered', 'climb', 'climbed', 'stand', 'stood', 'sit', 'sat',
    'rise', 'rose', 'sink', 'sank', 'float', 'floated', 'drift', 'drifted',
}

TEMPORAL = {
    'then', 'now', 'before', 'after', 'when', 'while', 'still', 'yet', 'already',
    'once', 'soon', 'later', 'long', 'past', 'forever', 'never', 'always',
    'again', 'ago', 'until', 'since', 'during', 'today', 'tomorrow', 'yesterday',
    'morning', 'evening', 'night', 'day', 'year', 'time', 'moment', 'hour',
    'second', 'minute', 'century', 'age', 'era', 'eternal', 'ancient', 'new',
    'old', 'young', 'recent', 'early', 'late', 'brief', 'last', 'first',
}

EMOTIONAL_PSYCHOLOGICAL = {
    'love', 'hate', 'fear', 'joy', 'grief', 'sorrow', 'hope', 'despair',
    'lonely', 'alone', 'sad', 'happy', 'glad', 'sorry', 'afraid', 'lost',
    'tender', 'gentle', 'fierce', 'bitter', 'sweet', 'dark', 'bright',
    'pain', 'ache', 'longing', 'desire', 'passion', 'anger', 'rage', 'peace',
    'soul', 'heart', 'mind', 'spirit', 'dream', 'thought', 'memory', 'wish',
    'feel', 'felt', 'know', 'knew', 'believe', 'thought', 'wonder', 'remember',
    'forget', 'cry', 'weep', 'laugh', 'smile', 'mourn', 'grieve', 'long',
    'yearn', 'ache', 'break', 'shatter', 'mend', 'heal', 'suffer', 'endure',
    'beautiful', 'terrible', 'wonderful', 'awful', 'strange', 'wild', 'quiet',
}

CONCRETE_NOUNS = {
    'tree', 'flower', 'leaf', 'stone', 'rock', 'river', 'lake', 'sea', 'ocean',
    'mountain', 'hill', 'field', 'wood', 'forest', 'cloud', 'rain', 'sun', 'moon',
    'star', 'sky', 'wind', 'snow', 'ice', 'fire', 'water', 'earth', 'grass',
    'bird', 'fish', 'horse', 'dog', 'cat', 'hand', 'eye', 'face', 'mouth',
    'door', 'house', 'room', 'wall', 'window', 'road', 'path', 'bridge',
    'book', 'word', 'name', 'voice', 'light', 'shadow', 'color', 'gold', 'silver',
    'blood', 'bone', 'flesh', 'skin', 'hair', 'wing', 'root', 'branch', 'seed',
    'rose', 'rose', 'oak', 'ash', 'willow', 'wave', 'shore', 'sand', 'dust',
    'sword', 'shield', 'crown', 'ring', 'cup', 'wine', 'bread', 'salt', 'glass',
    'table', 'chair', 'bed', 'street', 'city', 'tower', 'gate', 'garden', 'grave',
}

FUNCTION_GRAMMAR = {
    'the', 'a', 'an', 'and', 'or', 'but', 'nor', 'yet', 'so', 'of', 'with',
    'it', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
    'had', 'do', 'does', 'did', 'will', 'would', 'shall', 'should', 'may',
    'might', 'must', 'can', 'could', 'not', 'no', 'nor', 'that', 'this',
    'these', 'those', 'he', 'she', 'they', 'we', 'you', 'I', 'him', 'her',
    'them', 'his', 'hers', 'their', 'my', 'your', 'its', 'our', 'who', 'what',
    'which', 'whom', 'whose', 'as', 'if', 'though', 'although', 'because',
    'for', 'on', 'in', 'at', 'by', 'with', 'about', 'against', 'between',
    'into', 'through', 'during', 'before', 'after', 'above', 'below',
    ':', ',', '.', ';', '!', '?', "'", '"', '-', '--', '(', ')',
    'said', 'says', 'tell', 'told', 'ask', 'asked', "'s", "'t", "'d",
}

ABSTRACT_NOUNS = {
    'truth', 'beauty', 'justice', 'freedom', 'death', 'life', 'nature',
    'fate', 'fortune', 'glory', 'honor', 'shame', 'guilt', 'grace', 'mercy',
    'power', 'force', 'will', 'law', 'order', 'chaos', 'void', 'nothing',
    'everything', 'being', 'existence', 'thought', 'idea', 'form', 'essence',
    'meaning', 'silence', 'darkness', 'emptiness', 'infinite', 'eternal',
    'god', 'heaven', 'hell', 'world', 'universe', 'light', 'dark',
    'art', 'music', 'poetry', 'language', 'sign', 'symbol', 'image',
    'culture', 'society', 'history', 'tradition', 'myth', 'legend',
}


def categorize_token(tok: str) -> str:
    """Return semantic category for a token string."""
    t = tok.strip().lower().lstrip(" '")
    if t in FUNCTION_GRAMMAR:
        return 'function/grammar'
    if t in SPATIAL_MOTION:
        return 'spatial/motion'
    if t in TEMPORAL:
        return 'temporal'
    if t in EMOTIONAL_PSYCHOLOGICAL:
        return 'emotional/psychological'
    if t in CONCRETE_NOUNS:
        return 'concrete noun'
    if t in ABSTRACT_NOUNS:
        return 'abstract noun'
    # heuristic fallbacks
    if t.endswith(('ly',)):
        return 'adverbial'
    if t.endswith(('ing', 'ed', 'en')) and len(t) > 4:
        return 'verbal'
    if re.match(r'^[A-Z]', tok.strip()):
        return 'proper noun'
    if re.match(r'^[\W\d]+$', t):
        return 'punctuation/numeral'
    return 'other'


def load_corpus():
    with open('results/corpus_results.json') as f:
        return json.load(f)


def analyze():
    corpus = load_corpus()

    # Collect high-S2 events (s2 > 2, p_newline < 0.5 to filter stanza artifacts)
    all_events = []
    era_events = defaultdict(list)

    for poem in corpus:
        era = poem['metadata']['era']
        author = poem['metadata']['author']
        for tok in poem['tokens']:
            if tok['s2'] < 2.0:
                continue
            if tok.get('p_newline', 0) > 0.5:
                continue  # filter stanza-break artifact
            if not tok.get('alternatives'):
                continue

            actual = tok['token']
            top_pred = tok['alternatives'][0]['token']

            actual_cat = categorize_token(actual)
            pred_cat = categorize_token(top_pred)

            if actual_cat == pred_cat:
                transition = 'same'
            else:
                transition = f"{pred_cat} → {actual_cat}"

            event = {
                'era': era,
                'author': author,
                's2': tok['s2'],
                'actual': actual.strip(),
                'top_pred': top_pred.strip(),
                'actual_cat': actual_cat,
                'pred_cat': pred_cat,
                'transition': transition,
                'rank': tok.get('rank', 0),
                'entropy': tok['entropy'],
                'surprisal': tok['surprisal'],
            }
            all_events.append(event)
            era_events[era].append(event)

    print(f"Total high-S2 events (s2>2, non-artifact): {len(all_events)}")

    # Global transition matrix
    transition_counts = Counter(e['transition'] for e in all_events)

    print("\n## Global Semantic Transition Matrix (expected → chosen)")
    print("(Top 20 most frequent transitions)\n")
    for trans, count in transition_counts.most_common(20):
        pct = 100 * count / len(all_events)
        print(f"  {trans:<50s} {count:>5}  ({pct:.1f}%)")

    # Build matrix: pred_cat -> actual_cat counts (excluding 'same')
    matrix = defaultdict(lambda: defaultdict(int))
    for e in all_events:
        if e['transition'] != 'same':
            matrix[e['pred_cat']][e['actual_cat']] += 1

    print("\n## Full Matrix (expected → actual, non-same transitions only)")
    cats = ['function/grammar', 'spatial/motion', 'temporal', 'emotional/psychological',
            'concrete noun', 'abstract noun', 'adverbial', 'verbal', 'proper noun',
            'punctuation/numeral', 'other']

    # get most active row categories
    row_totals = {c: sum(matrix[c].values()) for c in cats}
    active_cats = sorted(row_totals, key=lambda x: -row_totals[x])[:7]

    print(f"\n{'Expected↓ / Chosen→':<26}", end='')
    for c in active_cats[:6]:
        label = c.split('/')[0][:8]
        print(f"{label:>12}", end='')
    print()

    for rc in active_cats:
        total = row_totals[rc]
        if total == 0:
            continue
        print(f"{rc[:25]:<26}", end='')
        for cc in active_cats[:6]:
            cnt = matrix[rc][cc]
            pct = 100 * cnt / total if total else 0
            print(f"{pct:>11.0f}%", end='')
        print(f"  (n={total})")

    # Era-level profiles: what % of non-same transitions go to which target?
    print("\n## Era Semantic Pivot Profiles (% of high-S2 transitions by target category)")
    print("(Eras with ≥25 events)\n")

    era_cats = defaultdict(lambda: Counter())
    era_total = Counter()
    for e in all_events:
        era = e['era']
        era_cats[era][e['actual_cat']] += 1
        era_total[era] += 1

    focus_cats = ['emotional/psychological', 'concrete noun', 'abstract noun',
                  'spatial/motion', 'other', 'adverbial']

    header = f"{'Era':<20}"
    for c in focus_cats:
        header += f"{c[:8]:>10}"
    header += f"{'n':>6}"
    print(header)
    print("-" * len(header))

    for era, total in sorted(era_total.items(), key=lambda x: -x[1]):
        if total < 25:
            continue
        row = f"{era[:19]:<20}"
        for c in focus_cats:
            pct = 100 * era_cats[era][c] / total
            row += f"{pct:>9.0f}%"
        row += f"{total:>6}"
        print(row)

    # Author profiles: characteristic substitution patterns
    print("\n## Author Semantic Pivot Profiles (top authors by event count)")
    print("(Authors with ≥30 events)\n")

    author_cats = defaultdict(lambda: Counter())
    author_total = Counter()
    for e in all_events:
        a = e['author']
        author_cats[a][e['actual_cat']] += 1
        author_total[a] += 1

    print(header.replace('Era', 'Author'))
    print("-" * len(header))
    for author, total in sorted(author_total.items(), key=lambda x: -x[1]):
        if total < 30:
            continue
        row = f"{author[:19]:<20}"
        for c in focus_cats:
            pct = 100 * author_cats[author][c] / total
            row += f"{pct:>9.0f}%"
        row += f"{total:>6}"
        print(row)

    # Most striking transitions: highest-S2 substitutions
    print("\n## Top 25 Highest-S2 Semantic Pivots (excluding stanza-artifact)\n")
    top = sorted(all_events, key=lambda x: -x['s2'])[:25]
    for e in top:
        print(f"  S2={e['s2']:6.2f}  {e['author'][:20]:<22}  "
              f"expected '{e['top_pred'][:12]:<14}' ({e['pred_cat'][:12]}) → "
              f"chose '{e['actual'][:12]:<14}' ({e['actual_cat'][:12]})")

    # Save results for findings
    results = {
        'n_events': len(all_events),
        'transition_counts': dict(transition_counts.most_common(30)),
        'era_profiles': {
            era: {cat: int(era_cats[era][cat]) for cat in focus_cats}
            for era in era_total if era_total[era] >= 25
        },
        'author_profiles': {
            author: {cat: int(author_cats[author][cat]) for cat in focus_cats}
            for author, total in author_total.items() if total >= 30
        },
        'top_pivots': [
            {'s2': e['s2'], 'author': e['author'], 'actual': e['actual'],
             'actual_cat': e['actual_cat'], 'pred': e['top_pred'],
             'pred_cat': e['pred_cat'], 'era': e['era']}
            for e in top
        ]
    }

    out_path = Path('results/semantic_surprise_transitions.json')
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == '__main__':
    analyze()
