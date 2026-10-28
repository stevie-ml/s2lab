"""
Whitman Section 15 Catalogue: S2 in Syntactic Parallel Without Lexical Anaphora

Hypothesis: Whitman's catalogue in Song of Myself section 15 uses syntactic
parallelism (The [occupation], [activity]) without lexical anaphora. Does GPT-2
adapt to the syntactic template even without a repeated anchor word?

Builds on catalog_decay_s2.md (lexical anaphora chains), but tests whether
*grammatical* pattern-learning creates the same entropy decay.
"""

import json
import re
import statistics

# Load corpus data
with open('results/corpus_results.json', 'r') as f:
    corpus = json.load(f)

# Find Whitman section 15
whitman15 = None
for poem in corpus:
    if 'section 15' in poem.get('metadata', {}).get('title', '').lower():
        whitman15 = poem
        break

if not whitman15:
    print("ERROR: Could not find Whitman section 15 in corpus")
    exit(1)

tokens = whitman15['tokens']
print(f"Song of Myself section 15: {len(tokens)} tokens")
print()

# The poem consists of ~87 occupational "items" each following a pattern.
# Each line starts with an article ("The") or a proper name, then an occupation,
# then the person's activity. We split by newlines.

# Reconstruct lines from token stream
lines = []
current_line = []
for t in tokens:
    current_line.append(t)
    if t['token'] == '\n':
        if current_line:
            lines.append(current_line)
            current_line = []
if current_line:
    lines.append(current_line)

print(f"Total lines (including newline tokens): {len(lines)}")

# Filter out very short lines (punctuation-only) and reconstruct text per line
def line_text(line_tokens):
    return ''.join(t['token'] for t in line_tokens).strip()

def line_s2_stats(line_tokens):
    """Get S2 statistics for content tokens (exclude newlines and the 'The' article)."""
    content = [t for t in line_tokens if t['token'] not in ['\n', 'The', 'the', ',', '.', ';', '!', '?', '"', '"']]
    if not content:
        return None
    s2_vals = [t['s2'] for t in content]
    entropy_vals = [t['entropy'] for t in content]
    return {
        'mean_s2': statistics.mean(s2_vals),
        'mean_entropy': statistics.mean(entropy_vals),
        'max_s2': max(s2_vals),
        'n': len(content),
        'first_noun_s2': content[0]['s2'] if content else None,  # usually the occupation noun
        'tokens': content
    }

# Catalog lines: lines starting with 'The' (the characteristic pattern)
catalog_lines = []
for i, line in enumerate(lines):
    text = line_text(line)
    # Keep lines that start with 'The' and have substance
    if text.startswith('The') and len(text) > 5:
        stats = line_s2_stats(line)
        if stats and stats['n'] >= 2:
            catalog_lines.append({
                'line_num': i + 1,
                'text': text,
                'stats': stats,
                'catalog_pos': len(catalog_lines) + 1
            })

print(f"Catalogue items ('The...' lines): {len(catalog_lines)}")
print()

# Show first 10 and last 10 catalogue items
print("=== FIRST 10 CATALOGUE ITEMS ===")
for item in catalog_lines[:10]:
    s = item['stats']
    print(f"  [{item['catalog_pos']:2d}] {item['text'][:65]}")
    print(f"       mean_s2={s['mean_s2']:+.2f}  mean_entropy={s['mean_entropy']:.2f}  max_s2={s['max_s2']:+.2f}  first_noun_s2={s['first_noun_s2']:+.2f}")

print()
print("=== LAST 10 CATALOGUE ITEMS ===")
for item in catalog_lines[-10:]:
    s = item['stats']
    print(f"  [{item['catalog_pos']:2d}] {item['text'][:65]}")
    print(f"       mean_s2={s['mean_s2']:+.2f}  mean_entropy={s['mean_entropy']:.2f}  max_s2={s['max_s2']:+.2f}  first_noun_s2={s['first_noun_s2']:+.2f}")

print()

# Key analysis: does entropy decay across catalogue positions?
# Split into thirds
n = len(catalog_lines)
thirds = [catalog_lines[:n//3], catalog_lines[n//3:2*n//3], catalog_lines[2*n//3:]]
print("=== ENTROPY ACROSS THIRDS OF CATALOGUE ===")
labels = ['First third', 'Middle third', 'Final third']
for label, group in zip(labels, thirds):
    entropies = [item['stats']['mean_entropy'] for item in group]
    s2s = [item['stats']['mean_s2'] for item in group]
    first_noun_s2s = [item['stats']['first_noun_s2'] for item in group if item['stats']['first_noun_s2'] is not None]
    print(f"  {label} (items {group[0]['catalog_pos']}-{group[-1]['catalog_pos']}):")
    print(f"    mean entropy: {statistics.mean(entropies):.3f}")
    print(f"    mean S2:      {statistics.mean(s2s):+.3f}")
    print(f"    mean first-noun S2: {statistics.mean(first_noun_s2s):+.3f}")
    print(f"    stdev S2:     {statistics.stdev(s2s):.3f}")

print()

# Find the most and least surprising occupation nouns
print("=== TOP 10 HIGHEST S2 OCCUPATION NOUNS (first content token of each item) ===")
by_noun_s2 = sorted(catalog_lines, key=lambda x: x['stats']['first_noun_s2'] or -999, reverse=True)
for item in by_noun_s2[:10]:
    s = item['stats']
    print(f"  [{item['catalog_pos']:2d}] first_noun_s2={s['first_noun_s2']:+.2f}  {item['text'][:65]}")

print()
print("=== TOP 10 LOWEST S2 OCCUPATION NOUNS ===")
for item in by_noun_s2[-10:]:
    s = item['stats']
    print(f"  [{item['catalog_pos']:2d}] first_noun_s2={s['first_noun_s2']:+.2f}  {item['text'][:65]}")

print()

# Entropy trend: linear regression across catalogue position
positions = [item['catalog_pos'] for item in catalog_lines]
entropies = [item['stats']['mean_entropy'] for item in catalog_lines]
s2s = [item['stats']['mean_s2'] for item in catalog_lines]
first_noun_s2s = [item['stats']['first_noun_s2'] for item in catalog_lines if item['stats']['first_noun_s2'] is not None]

# Compute Pearson correlation: position vs entropy
def pearson(xs, ys):
    n = len(xs)
    mx = statistics.mean(xs)
    my = statistics.mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx)**2 for x in xs) * sum((y - my)**2 for y in ys)) ** 0.5
    return num / den if den != 0 else 0

r_ent = pearson(positions, entropies)
r_s2 = pearson(positions, s2s)
print("=== POSITION-ENTROPY CORRELATION ===")
print(f"  r(position, entropy): {r_ent:.4f}")
print(f"  r(position, mean_s2): {r_s2:.4f}")
print()
print("  Interpretation:")
if r_ent < -0.2:
    print("  CONFIRMED: Entropy DECAYS as catalogue progresses (GPT-2 learning the template)")
elif r_ent > 0.2:
    print("  SURPRISING: Entropy RISES as catalogue progresses (template becomes less predictive)")
else:
    print(f"  No strong trend (r={r_ent:.3f}): catalogue entropy is roughly flat")

print()

# Compare 'The' token S2 across positions — does the definite article become more predictable?
the_tokens = []
for item in catalog_lines:
    # Find 'The' token in the line
    for t in item['stats']['tokens']:
        pass  # we filtered 'The' out — let's re-grab from raw
for line in lines:
    for t in line:
        if t['token'] == 'The':
            the_tokens.append(t)

print(f"=== 'THE' ARTICLE TOKENS: {len(the_tokens)} occurrences ===")
if the_tokens:
    the_s2s = [t['s2'] for t in the_tokens]
    the_entropies = [t['entropy'] for t in the_tokens]
    print(f"  Mean S2 of 'The':     {statistics.mean(the_s2s):+.3f}")
    print(f"  Stdev S2 of 'The':   {statistics.stdev(the_s2s):.3f}")
    print(f"  Mean entropy at 'The': {statistics.mean(the_entropies):.3f}")
    print()
    # Are early 'The's more surprising than late ones?
    n_the = len(the_tokens)
    early = the_tokens[:n_the//2]
    late = the_tokens[n_the//2:]
    print(f"  Early 'The' (pos 1-{n_the//2}): mean_s2={statistics.mean(t['s2'] for t in early):+.3f}  mean_entropy={statistics.mean(t['entropy'] for t in early):.3f}")
    print(f"  Late 'The' (pos {n_the//2+1}-{n_the}): mean_s2={statistics.mean(t['s2'] for t in late):+.3f}  mean_entropy={statistics.mean(t['entropy'] for t in late):.3f}")

print()

# Compute ALL item stats for JSON output
results = {
    'poem': 'Song of Myself section 15',
    'total_tokens': len(tokens),
    'catalog_item_count': len(catalog_lines),
    'position_entropy_correlation': r_ent,
    'position_s2_correlation': r_s2,
    'thirds_analysis': {
        labels[0]: {
            'mean_entropy': statistics.mean([item['stats']['mean_entropy'] for item in thirds[0]]),
            'mean_s2': statistics.mean([item['stats']['mean_s2'] for item in thirds[0]]),
        },
        labels[1]: {
            'mean_entropy': statistics.mean([item['stats']['mean_entropy'] for item in thirds[1]]),
            'mean_s2': statistics.mean([item['stats']['mean_s2'] for item in thirds[1]]),
        },
        labels[2]: {
            'mean_entropy': statistics.mean([item['stats']['mean_entropy'] for item in thirds[2]]),
            'mean_s2': statistics.mean([item['stats']['mean_s2'] for item in thirds[2]]),
        },
    },
    'top_surprise_items': [
        {'pos': item['catalog_pos'], 'text': item['text'], 'first_noun_s2': item['stats']['first_noun_s2']}
        for item in by_noun_s2[:5]
    ],
    'least_surprise_items': [
        {'pos': item['catalog_pos'], 'text': item['text'], 'first_noun_s2': item['stats']['first_noun_s2']}
        for item in by_noun_s2[-5:]
    ],
    'all_catalog_items': [
        {
            'pos': item['catalog_pos'],
            'text': item['text'],
            'mean_s2': round(item['stats']['mean_s2'], 3),
            'mean_entropy': round(item['stats']['mean_entropy'], 3),
            'first_noun_s2': round(item['stats']['first_noun_s2'], 3) if item['stats']['first_noun_s2'] else None,
        }
        for item in catalog_lines
    ]
}

with open('results/whitman_catalogue_s2.json', 'w') as f:
    json.dump(results, f, indent=2)
print("Results saved to results/whitman_catalogue_s2.json")
