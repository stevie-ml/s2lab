"""
straussian_extremes.py
Taxonomy of extreme Straussian gaps (S2 >= 5.0, cleaned).
Categorizes WHAT gets suppressed vs. chosen at maximum-surprise moments.
"""

import json
from collections import defaultdict, Counter
import statistics

with open('results/corpus_results.json') as f:
    data = json.load(f)

# ── Filtering helpers ─────────────────────────────────────────────────────────

FUNCTION_WORDS = {
    'the', 'a', 'an', 'of', 'in', 'to', 'and', 'but', 'or', 'for', 'nor',
    'on', 'at', 'by', 'up', 'as', 'is', 'it', 'its', 'was', 'are', 'be',
    'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
    'would', 'shall', 'should', 'may', 'might', 'must', 'can', 'could',
    'that', 'this', 'these', 'those', 'he', 'she', 'they', 'we', 'you',
    'his', 'her', 'their', 'our', 'your', 'my', 'him', 'them', 'us',
    'with', 'from', 'into', 'out', 'then', 'than', 'not', 'so', 'yet',
    'if', 'when', 'where', 'which', 'who', 'whom', 'whose', 'what', 'how',
    'more', 'most', 'such', 'each', 'all', 'both', 'just', 'now', 'very',
    'even', 'still', 'also', 'only', 'about', 'after', 'before', 'through',
    'over', 'under', 'again', 'then', 'there', 'here', 'too', 'much', 'any',
    'some', 'no', 'one', 'two', 'three', 'first', 'last', 'am',
}

PUNCT_SET = {',', '.', ';', ':', '?', '!', '—', '-', "'", '"', '(', ')', '--'}

def classify_suppressed(top_pred):
    """Classify what GPT-2 expected."""
    t = top_pred.strip().lower()
    if top_pred.strip() in PUNCT_SET or top_pred.strip() in {',', '.', ';', ':', '—'}:
        return 'PUNCTUATION'
    if t in FUNCTION_WORDS:
        return 'FUNCTION_WORD'
    if top_pred.startswith("'") or top_pred.startswith(' \''):
        return 'CONTRACTION'
    if top_pred.strip() == top_pred.strip().capitalize() and len(top_pred.strip()) > 2:
        return 'CONTENT_WORD'  # starts lowercase = common noun/verb
    return 'CONTENT_WORD'

def classify_chosen(token_str):
    """Rough semantic category of chosen token."""
    t = token_str.strip().lower()
    # Abstract concepts
    abstract = {'death', 'life', 'time', 'love', 'beauty', 'truth', 'soul', 'god',
                'heaven', 'light', 'dark', 'silence', 'peace', 'war', 'pain',
                'grief', 'joy', 'hope', 'fear', 'despair', 'mercy', 'justice',
                'glory', 'doom', 'fate', 'dream', 'thought', 'memory', 'mind',
                'spirit', 'heart', 'nature', 'music', 'art', 'poetry', 'words',
                'songs', 'poems', 'prose', 'anguish', 'consequences', 'suffering',
                'freedom', 'power', 'knowledge', 'wisdom', 'duty', 'honor'}
    # Concrete/sensory
    concrete_sensory = {'blood', 'mud', 'rain', 'snow', 'sun', 'moon', 'star',
                        'fire', 'water', 'earth', 'stone', 'wood', 'iron', 'gold',
                        'glass', 'grass', 'leaf', 'flower', 'bird', 'fish',
                        'cloud', 'wind', 'wave', 'shore', 'hill', 'river', 'sea',
                        'road', 'door', 'wall', 'room', 'house', 'field', 'tree',
                        'bone', 'flesh', 'skin', 'eye', 'hand', 'mouth', 'voice'}
    # Colloquial/vernacular
    colloquial = {'gravy', 'grub', 'gal', 'guy', 'kid', 'stuff', 'thing', 'thump',
                  'rack', 'yell', 'shout', 'chat', 'chat', 'mess', 'fuss'}
    # Action/surprise verbs
    action_verbs = {'shook', 'squats', 'prank', 'fleeing', 'stacked', 'chaired',
                    'mounting', 'observing', 'entangled', 'witnessed'}
    if t in abstract:
        return 'ABSTRACT'
    if t in concrete_sensory:
        return 'CONCRETE_SENSORY'
    if t in colloquial:
        return 'COLLOQUIAL'
    if t in action_verbs:
        return 'ACTION_VERB'
    if token_str.strip() and token_str.strip()[0].isupper():
        return 'PROPER_NOUN'
    return 'OTHER_CONTENT'

def is_valid_token(token_str, top_pred, entropy):
    """Filter artifacts and subword tokens."""
    if not token_str.startswith(' '):
        return False
    t = token_str.strip()
    if not t or len(t) < 2:
        return False
    known_short_words = {'I', 'O', 'A', 'oh', 'ah', 'lo', 'no', 'so', 'go',
                         'do', 'be', 'up', 'in', 'on', 'or', 'at', 'by', 'as'}
    if len(t) <= 2 and t not in known_short_words:
        return False
    if top_pred.strip() in ('', '\n'):
        return False
    if entropy < 1.0:
        return False
    if not all(c.isalpha() or c in "'-" for c in t):
        return False
    return True

# ── Collect all high-S2 moments ───────────────────────────────────────────────

moments = []
for poem in data:
    meta = poem['metadata']
    tokens = poem.get('tokens', [])
    for tok in tokens:
        if tok.get('p_newline', 0) >= 0.9:
            continue
        entropy = tok.get('entropy', 10)
        token_str = tok.get('token', '')
        alts = tok.get('alternatives', [])
        top_pred = alts[0]['token'] if alts else ''
        if not is_valid_token(token_str, top_pred, entropy):
            continue
        s2 = tok.get('s2', 0)
        if s2 < 5.0:
            continue

        suppressed_cat = classify_suppressed(top_pred)
        chosen_cat = classify_chosen(token_str.strip())

        moments.append({
            's2': s2,
            'token': token_str.strip(),
            'top_pred': top_pred.strip(),
            'suppressed_cat': suppressed_cat,
            'chosen_cat': chosen_cat,
            'rank': tok.get('rank', 0),
            'entropy': entropy,
            'surprisal': tok.get('surprisal', 0),
            'context': tok.get('context_before', '').strip()[-50:],
            'poet': meta.get('author', '?'),
            'title': meta.get('title', '?'),
            'era': meta.get('era', '?'),
            'year': meta.get('year', '?'),
        })

moments.sort(key=lambda x: -x['s2'])

# ── Analysis 1: What does GPT-2 expect at extreme moments? ───────────────────

suppressed_counts = Counter(m['suppressed_cat'] for m in moments)
# Baseline: all tokens in corpus (not just high-S2)
baseline_suppressed = Counter()
total_baseline = 0
for poem in data:
    for tok in poem.get('tokens', []):
        if tok.get('p_newline', 0) >= 0.9:
            continue
        alts = tok.get('alternatives', [])
        if not alts:
            continue
        top_pred = alts[0]['token'].strip().lower()
        if top_pred in PUNCT_SET:
            baseline_suppressed['PUNCTUATION'] += 1
        elif top_pred in FUNCTION_WORDS:
            baseline_suppressed['FUNCTION_WORD'] += 1
        elif top_pred.startswith("'"):
            baseline_suppressed['CONTRACTION'] += 1
        else:
            baseline_suppressed['CONTENT_WORD'] += 1
        total_baseline += 1

# ── Analysis 2: Transition matrix — what suppressed → what chosen ─────────────

transition_counts = defaultdict(Counter)
for m in moments:
    transition_counts[m['suppressed_cat']][m['chosen_cat']] += 1

# ── Analysis 3: Which poets/eras produce the most extreme gaps ──────────────

era_moments = defaultdict(list)
poet_moments = defaultdict(list)
for m in moments:
    era_moments[m['era']].append(m['s2'])
    poet_moments[m['poet']].append(m['s2'])

# ── Analysis 4: S2 by suppressed category ────────────────────────────────────

s2_by_suppressed = defaultdict(list)
for m in moments:
    s2_by_suppressed[m['suppressed_cat']].append(m['s2'])

# ── Save results ─────────────────────────────────────────────────────────────

results = {
    'n_moments': len(moments),
    'suppressed_counts': dict(suppressed_counts),
    'baseline_suppressed': dict(baseline_suppressed),
    'transition_matrix': {k: dict(v) for k, v in transition_counts.items()},
    'era_stats': {
        era: {
            'n': len(vals),
            'mean_s2': round(statistics.mean(vals), 3),
            'max_s2': round(max(vals), 3),
        }
        for era, vals in era_moments.items() if len(vals) >= 2
    },
    'poet_stats': {
        poet: {
            'n': len(vals),
            'mean_s2': round(statistics.mean(vals), 3),
            'max_s2': round(max(vals), 3),
        }
        for poet, vals in poet_moments.items() if len(vals) >= 3
    },
    's2_by_suppressed': {
        cat: {
            'n': len(vals),
            'mean': round(statistics.mean(vals), 3),
            'median': round(statistics.median(vals), 3),
            'max': round(max(vals), 3),
        }
        for cat, vals in s2_by_suppressed.items() if vals
    },
    'top_50_moments': [
        {
            's2': round(m['s2'], 2),
            'token': m['token'],
            'top_pred': m['top_pred'],
            'suppressed_cat': m['suppressed_cat'],
            'chosen_cat': m['chosen_cat'],
            'rank': m['rank'],
            'entropy': round(m['entropy'], 2),
            'context': m['context'],
            'poet': m['poet'],
            'era': m['era'],
            'title': m['title'],
        }
        for m in moments[:50]
    ],
}

with open('results/straussian_extremes.json', 'w') as f:
    json.dump(results, f, indent=2)

# ── Print report ─────────────────────────────────────────────────────────────

print(f"Total extreme S2 moments (>= 5.0, cleaned): {len(moments)}")
print()

print("1. WHAT GPT-2 EXPECTED at extreme moments (vs baseline)")
print("-" * 60)
total = sum(suppressed_counts.values())
total_base = sum(baseline_suppressed.values())
for cat in ['PUNCTUATION', 'FUNCTION_WORD', 'CONTENT_WORD', 'CONTRACTION']:
    high_pct = suppressed_counts.get(cat, 0) / total * 100
    base_pct = baseline_suppressed.get(cat, 0) / total_base * 100
    lift = high_pct / base_pct if base_pct > 0 else 0
    print(f"  {cat:20s}: {high_pct:.1f}% at high-S2  vs {base_pct:.1f}% baseline  (lift={lift:.2f}x)")
print()

print("2. S2 MAGNITUDE BY WHAT WAS SUPPRESSED")
print("-" * 60)
s2_suppressed_stats = {
    cat: {
        'n': len(vals),
        'mean': round(statistics.mean(vals), 3),
        'median': round(statistics.median(vals), 3),
        'max': round(max(vals), 3),
    }
    for cat, vals in s2_by_suppressed.items()
}
for cat, stats in sorted(s2_suppressed_stats.items(), key=lambda x: -x[1]['mean']):
    print(f"  {cat:20s}: n={stats['n']:4d}  mean={stats['mean']:5.1f}  median={stats['median']:5.1f}  max={stats['max']:5.1f}")
print()

print("3. TRANSITION MATRIX: suppressed → chosen")
print("-" * 60)
all_chosen_cats = sorted({m['chosen_cat'] for m in moments})
header = f"{'suppressed':20s}" + "".join(f"{c[:12]:>14s}" for c in all_chosen_cats)
print(header)
for sup_cat in ['PUNCTUATION', 'FUNCTION_WORD', 'CONTENT_WORD', 'CONTRACTION']:
    row = f"{sup_cat:20s}"
    total_row = sum(transition_counts[sup_cat].values())
    for chosen_cat in all_chosen_cats:
        n = transition_counts[sup_cat].get(chosen_cat, 0)
        pct = n / total_row * 100 if total_row > 0 else 0
        row += f"{pct:>13.1f}%"
    print(row)
print()

print("4. ERAS WITH MOST EXTREME GAPS (mean S2 at high-S2 moments)")
print("-" * 60)
era_sorted = sorted(era_moments.items(),
                    key=lambda x: statistics.mean(x[1]) if len(x[1]) >= 2 else 0,
                    reverse=True)
for era, vals in era_sorted[:15]:
    if len(vals) < 2:
        continue
    print(f"  {era:25s}: n={len(vals):4d}  mean={statistics.mean(vals):5.1f}  max={max(vals):5.1f}")
print()

print("5. POETS WITH MOST EXTREME GAPS")
print("-" * 60)
poet_sorted = sorted(poet_moments.items(),
                     key=lambda x: statistics.mean(x[1]) if len(x[1]) >= 3 else 0,
                     reverse=True)
for poet, vals in poet_sorted[:15]:
    if len(vals) < 3:
        continue
    print(f"  {poet[:35]:35s}: n={len(vals):4d}  mean={statistics.mean(vals):5.1f}  max={max(vals):5.1f}")
print()

print("6. TOP 20 EXTREME STRAUSSIAN MOMENTS")
print("-" * 80)
for i, m in enumerate(moments[:20]):
    print(f"\n{i+1:3d}. S2={m['s2']:5.1f}  [{m['token']!r:20s}] suppresses [{m['top_pred']!r}]")
    print(f"      Context: ...{m['context']!r}")
    print(f"      Type: {m['suppressed_cat']} → {m['chosen_cat']}")
    print(f"      {m['poet']} | {m['era']}")

print("\nResults saved to results/straussian_extremes.json")
