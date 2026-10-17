"""
Body-Part Lexicon and S₂ in Poetry

Research question: When a poem names a body part, is it using it conventionally
(low S₂, the expected word) or as a vehicle for surprise (high S₂)?

The 'anatomical turn' hypothesis: Body parts are among the most common concrete
nouns in poetry — heart, eye, hand, face, blood, bone, skin, lip, etc.
But their S₂ status should vary by:
  1. Cliché saturation (heart >> eye >> elbow in poetic frequency)
  2. Literal vs. metaphorical use (blood can be literal or intensely figurative)
  3. Literary era (Romantic poets use 'heart' differently than Language poets)
  4. Poetic vs. suppressed alternatives (what did GPT-2 expect INSTEAD of 'blood'?)

Method:
1. Compile a body-part lexicon with frequency tiers (core, extended, rare)
2. For each poem, extract all body-part tokens and their S₂ values
3. Analyze: which body parts are most/least surprising in context?
4. Compare body-part S₂ across literary eras
5. Look at the 'suppressed' alternatives — what does GPT-2 expect at body-part positions?
6. Test: do body parts appear at structurally significant positions (line-final, stressed)?
"""

import json
import re
import os
import statistics
import ast
from pathlib import Path
from collections import defaultdict, Counter

# ── Body-part lexicon ──────────────────────────────────────────────────────────
# Tier 1: Core poetic body parts (extremely common in poetry)
CORE_BODY_PARTS = {
    'heart', 'eye', 'eyes', 'hand', 'hands', 'face', 'lip', 'lips',
    'head', 'blood', 'bone', 'bones', 'skin', 'arm', 'arms', 'foot',
    'feet', 'mouth', 'breast', 'breasts', 'body', 'soul', 'mind',
    'voice', 'ear', 'ears', 'hair', 'finger', 'fingers', 'neck',
    'knee', 'knees', 'tongue', 'chest', 'back', 'brow', 'cheek',
    'cheeks', 'throat', 'shoulder', 'shoulders', 'leg', 'legs', 'flesh',
    'nose', 'teeth', 'tooth', 'thumb', 'wrist', 'ankle', 'heel',
    'spine', 'rib', 'ribs', 'vein', 'veins', 'nerve', 'nerves',
}

# Tier 2: Less common but still poetically significant
EXTENDED_BODY_PARTS = {
    'skull', 'forehead', 'jaw', 'jaw', 'chin', 'palm', 'palms',
    'elbow', 'temple', 'temples', 'loin', 'loins', 'hip', 'hips',
    'belly', 'womb', 'lung', 'lungs', 'liver', 'sinew', 'sinews',
    'marrow', 'muscle', 'muscles', 'tendon', 'artery', 'arteries',
    'eyelid', 'eyelids', 'nostril', 'nostrils', 'knuckle', 'knuckles',
    'calf', 'calves', 'thigh', 'thighs', 'torso', 'navel',
    'eyebrow', 'eyebrows', 'eyelash', 'eyelashes', 'pupil', 'pupils',
    'iris', 'cornea', 'retina',
}

ALL_BODY_PARTS = CORE_BODY_PARTS | EXTENDED_BODY_PARTS

# Body parts often used metaphorically
METAPHOR_PRONE = {'heart', 'soul', 'mind', 'blood', 'bone', 'bones', 'flesh',
                   'spine', 'backbone', 'marrow', 'vein', 'veins', 'nerve', 'nerves',
                   'breast', 'voice', 'eye', 'eyes', 'ear', 'ears', 'tongue', 'teeth'}

# ── Load corpus ────────────────────────────────────────────────────────────────
script_dir = Path(__file__).parent
corpus_path = script_dir.parent / 'results' / 'corpus_results.json'

with open(corpus_path) as f:
    corpus = json.load(f)

# Parse metadata safely
def parse_meta(m):
    if isinstance(m, dict):
        return m
    try:
        return ast.literal_eval(m)
    except Exception:
        return {}

def parse_tokens(t):
    if isinstance(t, list):
        return t
    try:
        return json.loads(t)
    except Exception:
        return []

# ── Extract body-part tokens from all poems ────────────────────────────────────
body_part_records = []  # Each: {token, s2, entropy, surprisal, poem, era, position, alternatives}
poem_stats = []

for poem in corpus:
    meta = parse_meta(poem['metadata'])
    era = meta.get('era', 'unknown')
    title = meta.get('title', '')
    author = meta.get('author', '')
    language = meta.get('language', 'english')

    # Only English-language poems (language field can be 'en' or 'english')
    if language not in ('en', 'english'):
        continue

    tokens = parse_tokens(poem['tokens'])
    n_tokens = len(tokens)
    if n_tokens == 0:
        continue

    poem_body_parts = []

    for tok in tokens:
        raw_token = tok.get('token', '')
        # Normalize: strip leading space, lowercase
        word = raw_token.strip().lower()
        # Also check with possessive: heart's -> heart
        word_base = re.sub(r"'s?$", '', word)

        s2 = tok.get('s2', 0.0)
        surprisal = tok.get('surprisal', 0.0)
        entropy = tok.get('entropy', 0.0)
        p_newline = tok.get('p_newline', 0.0)
        rank = tok.get('rank', 9999)
        alternatives = tok.get('alternatives', [])
        position = tok.get('position', 0)

        # Skip newline artifact
        if p_newline > 0.9:
            continue

        # Check if it's a body part
        for bp_form in [word, word_base]:
            if bp_form in ALL_BODY_PARTS:
                is_core = bp_form in CORE_BODY_PARTS
                is_metaphor_prone = bp_form in METAPHOR_PRONE

                # Get top predicted alternative
                top_alt = alternatives[0]['token'].strip().lower() if alternatives else ''
                # Whether the body part was predicted at all (in top-10 alts)
                alt_tokens = [a['token'].strip().lower() for a in alternatives]
                was_predicted = bp_form in alt_tokens
                top_alt_prob = alternatives[0]['prob'] if alternatives else 0.0

                record = {
                    'word': bp_form,
                    'raw_token': raw_token,
                    's2': s2,
                    'surprisal': surprisal,
                    'entropy': entropy,
                    'rank': rank,
                    'p_newline': p_newline,
                    'position_frac': position / n_tokens,  # 0=start, 1=end
                    'era': era,
                    'title': title,
                    'author': author,
                    'is_core': is_core,
                    'is_metaphor_prone': is_metaphor_prone,
                    'top_alt': top_alt,
                    'top_alt_prob': top_alt_prob,
                    'was_predicted': was_predicted,
                }
                body_part_records.append(record)
                poem_body_parts.append(record)
                break

    if poem_body_parts:
        poem_stats.append({
            'title': title,
            'author': author,
            'era': era,
            'n_body_part_tokens': len(poem_body_parts),
            'avg_s2': statistics.mean(r['s2'] for r in poem_body_parts),
            'body_part_density': len(poem_body_parts) / n_tokens,
        })

print(f"Total body-part token occurrences: {len(body_part_records)}")
print(f"Poems with body-part tokens: {len(poem_stats)}")

# ── Analysis 1: Overall S₂ statistics by body part ────────────────────────────
bp_s2 = defaultdict(list)
bp_alternatives = defaultdict(list)  # what was suppressed at body-part positions

for rec in body_part_records:
    bp_s2[rec['word']].append(rec['s2'])
    if rec['top_alt']:
        bp_alternatives[rec['word']].append(rec['top_alt'])

# Rank by mean S₂ (min 3 occurrences)
bp_means = {}
for word, s2_list in bp_s2.items():
    if len(s2_list) >= 3:
        bp_means[word] = {
            'n': len(s2_list),
            'mean': statistics.mean(s2_list),
            'median': statistics.median(s2_list),
            'std': statistics.stdev(s2_list) if len(s2_list) > 1 else 0,
            'pos_pct': sum(1 for s in s2_list if s > 0) / len(s2_list),
        }

sorted_bp = sorted(bp_means.items(), key=lambda x: x[1]['mean'], reverse=True)

print("\n=== BODY PARTS BY MEAN S₂ (artifact-free, n≥3) ===")
print(f"{'Word':<14} {'n':>4} {'Mean S₂':>8} {'Median S₂':>10} {'Pos%':>6} {'Top suppressed'}")
print("-" * 70)
for word, stats_d in sorted_bp[:20]:
    top_alts = Counter(bp_alternatives.get(word, [])).most_common(2)
    top_alt_str = ', '.join(f"'{t}'" for t, _ in top_alts)
    print(f"{word:<14} {stats_d['n']:>4} {stats_d['mean']:>+8.3f} {stats_d['median']:>+10.3f} "
          f"{stats_d['pos_pct']:>5.0%}  {top_alt_str}")

print("\n(lowest S₂ body parts):")
for word, stats_d in sorted_bp[-10:]:
    top_alts = Counter(bp_alternatives.get(word, [])).most_common(2)
    top_alt_str = ', '.join(f"'{t}'" for t, _ in top_alts)
    print(f"{word:<14} {stats_d['n']:>4} {stats_d['mean']:>+8.3f} {stats_d['median']:>+10.3f} "
          f"{stats_d['pos_pct']:>5.0%}  {top_alt_str}")

# ── Analysis 2: Era comparison for core body parts ────────────────────────────
print("\n=== ERA COMPARISON: avg S₂ of body-part tokens ===")
era_bp_s2 = defaultdict(list)
for rec in body_part_records:
    era_bp_s2[rec['era']].append(rec['s2'])

era_means = []
for era, s2_list in era_bp_s2.items():
    if len(s2_list) >= 5:
        era_means.append((era, statistics.mean(s2_list), len(s2_list)))

era_means.sort(key=lambda x: x[1], reverse=True)
print(f"{'Era':<25} {'n':>5} {'Mean S₂':>8}")
print("-" * 42)
for era, mean_s2, n in era_means:
    print(f"{era:<25} {n:>5} {mean_s2:>+8.3f}")

# ── Analysis 3: Heart specifically — most clichéd body part ───────────────────
print("\n=== HEART: S₂ by literary era ===")
heart_records = [r for r in body_part_records if r['word'] == 'heart']
heart_by_era = defaultdict(list)
for r in heart_records:
    heart_by_era[r['era']].append(r['s2'])

heart_era_means = []
for era, s2_list in heart_by_era.items():
    if len(s2_list) >= 2:
        heart_era_means.append((era, statistics.mean(s2_list), len(s2_list)))

heart_era_means.sort(key=lambda x: x[1], reverse=True)
print(f"{'Era':<25} {'n':>4} {'Mean S₂':>8}")
print("-" * 40)
for era, mean_s2, n in heart_era_means:
    print(f"{era:<25} {n:>4} {mean_s2:>+8.3f}")

# ── Analysis 4: Top suppressed alternatives at body-part positions ─────────────
print("\n=== SUPPRESSED ALTERNATIVES at body-part positions ===")
print("(What GPT-2 predicted INSTEAD of the body part)")
all_alts_at_bp = []
for rec in body_part_records:
    all_alts_at_bp.append(rec['top_alt'])

top_suppressed = Counter(all_alts_at_bp).most_common(20)
print("Top predicted alternatives when a body part appeared:")
for word, count in top_suppressed:
    print(f"  '{word}': {count} times")

# ── Analysis 5: High-S₂ body part moments ─────────────────────────────────────
print("\n=== MOST SURPRISING body-part usages (S₂ > 4.0) ===")
high_s2_bp = sorted([r for r in body_part_records if r['s2'] > 4.0],
                    key=lambda x: x['s2'], reverse=True)
for r in high_s2_bp[:15]:
    print(f"  [{r['s2']:+.2f}] '{r['word']}' — {r['title']} ({r['author']}, {r['era']}) | suppressed: '{r['top_alt']}'")

# ── Analysis 6: Metaphor-prone vs. literal body parts ─────────────────────────
print("\n=== METAPHOR-PRONE vs. LITERAL body parts ===")
metaphor_s2 = [r['s2'] for r in body_part_records if r['is_metaphor_prone']]
literal_s2 = [r['s2'] for r in body_part_records if not r['is_metaphor_prone']]
if metaphor_s2 and literal_s2:
    print(f"Metaphor-prone (heart/soul/blood/bone...): n={len(metaphor_s2)}, mean={statistics.mean(metaphor_s2):+.3f}")
    print(f"Literal/physical (elbow/knee/ankle...): n={len(literal_s2)}, mean={statistics.mean(literal_s2):+.3f}")

# ── Save results ───────────────────────────────────────────────────────────────
output = {
    'total_body_part_tokens': len(body_part_records),
    'poems_with_body_parts': len(poem_stats),
    'body_part_stats': {word: stats_d for word, stats_d in sorted_bp},
    'era_body_part_s2': {era: {'mean': mean_s2, 'n': n} for era, mean_s2, n in era_means},
    'heart_by_era': {era: {'mean': mean_s2, 'n': n} for era, mean_s2, n in heart_era_means},
    'top_suppressed_at_body_parts': [{'word': w, 'count': c} for w, c in top_suppressed],
    'high_s2_body_parts': [
        {'word': r['word'], 's2': r['s2'], 'title': r['title'],
         'author': r['author'], 'era': r['era'], 'top_alt': r['top_alt']}
        for r in high_s2_bp[:30]
    ],
    'metaphor_prone_mean_s2': statistics.mean(metaphor_s2) if metaphor_s2 else None,
    'literal_mean_s2': statistics.mean(literal_s2) if literal_s2 else None,
}

out_path = script_dir.parent / 'results' / 'body_part_lexicon_s2.json'
with open(out_path, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to: {out_path}")
