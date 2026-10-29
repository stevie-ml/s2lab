"""
Echo of the Unsaid: Do GPT-2's Predicted Alternatives Appear Elsewhere in the Poem?

When GPT-2 expects word X at position P but the poet writes Y instead (high S2),
does X appear elsewhere in the poem? This measures whether the poet is:
  - "Delaying" X (high S2 locally, but X appears later = operating within language's semantic field)
  - "Suppressing" X (high S2 locally, and X never appears = operating outside the field)

If high-S2 poems suppress alternatives entirely, they inhabit a semantic space
language never predicted. If they merely delay them, the poem and the model share
a vocabulary even when diverging moment-to-moment.
"""

import json
import os
import sys
from collections import defaultdict
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")
OUTPUT_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "echo_of_unsaid.json")
ARTIFACT_P = 0.90

# --- Load corpus ---
with open(RESULTS_PATH) as f:
    corpus = json.load(f)

print(f"Loaded {len(corpus)} texts")

def normalize(tok):
    """Lowercase, strip whitespace."""
    return tok.strip().lower()

def analyze_poem(entry):
    """
    For each non-artifact token in the poem, compute what fraction of its
    top-5 alternatives appear (anywhere) in the poem's full token list.

    Returns per-token records and poem-level summary stats.
    """
    tokens = entry.get('tokens', [])
    if not tokens:
        return None

    meta = entry.get('metadata', {})
    era = meta.get('era', 'unknown')
    lang = meta.get('language', 'en')
    title = meta.get('title', '')
    author = meta.get('author', '')
    summary = entry.get('summary', {})
    avg_s2 = summary.get('avg_s2', 0)

    # Build the poem's full vocabulary (all tokens, lowercased)
    poem_vocab = set(normalize(t['token']) for t in tokens)

    records = []
    for tok in tokens:
        # Skip stanza-break artifacts
        if tok.get('p_newline', 0) >= ARTIFACT_P:
            continue
        s2 = tok.get('s2', 0)
        alts = tok.get('alternatives', [])
        if not alts:
            continue

        # Top-5 content alternatives (exclude punctuation and newlines)
        top5 = []
        for a in alts[:10]:
            t = normalize(a['token'])
            if t and t not in {',', '.', '!', '?', ';', ':', '-', '--', '...', '\n', '(', ')'}:
                top5.append(t)
            if len(top5) >= 5:
                break

        if not top5:
            continue

        # How many of the top-5 alternatives appear anywhere in the poem?
        echo_count = sum(1 for alt in top5 if alt in poem_vocab)
        echo_rate = echo_count / len(top5)

        records.append({
            'token': tok['token'].strip(),
            's2': s2,
            'entropy': tok.get('entropy', 0),
            'echo_rate': echo_rate,
            'echo_count': echo_count,
            'n_alts': len(top5),
            'top_alt': top5[0] if top5 else '',
            'top_alt_in_poem': top5[0] in poem_vocab if top5 else False,
        })

    if not records:
        return None

    # Poem-level stats
    echo_rates = [r['echo_rate'] for r in records]
    s2_vals = [r['s2'] for r in records]
    high_s2_records = [r for r in records if r['s2'] > 2.0]
    low_s2_records = [r for r in records if r['s2'] < -1.0]

    return {
        'title': title,
        'author': author,
        'era': era,
        'language': lang,
        'avg_s2': avg_s2,
        'n_tokens': len(records),
        'poem_vocab_size': len(poem_vocab),
        'mean_echo_rate': statistics.mean(echo_rates),
        'high_s2_echo_rate': statistics.mean([r['echo_rate'] for r in high_s2_records]) if high_s2_records else None,
        'low_s2_echo_rate': statistics.mean([r['echo_rate'] for r in low_s2_records]) if low_s2_records else None,
        'top1_echo_rate': statistics.mean([1.0 if r['top_alt_in_poem'] else 0.0 for r in records]),
        'n_high_s2': len(high_s2_records),
        'n_low_s2': len(low_s2_records),
        'per_token': records,
    }

# --- Analyze all poems ---
poem_results = []
for entry in corpus:
    lang = entry.get('metadata', {}).get('language', 'en')
    if lang != 'en':
        continue  # GPT-2 trained on English; alternatives only meaningful for English
    result = analyze_poem(entry)
    if result:
        poem_results.append(result)

print(f"Analyzed {len(poem_results)} English texts")

# --- Era-level aggregation ---
era_stats = defaultdict(list)
for pr in poem_results:
    era_stats[pr['era']].append(pr)

print("\n=== Echo Rate by Era (mean fraction of top-5 alternatives appearing elsewhere in poem) ===")
print(f"{'Era':<25} {'n':>4}  {'Avg S2':>7}  {'Echo(all)':>9}  {'Echo(hi-S2)':>11}  {'Echo(lo-S2)':>11}  {'Top1-echo':>9}")
print("-" * 90)

era_rows = []
for era, poems in sorted(era_stats.items(), key=lambda x: -statistics.mean(p['mean_echo_rate'] for p in x[1])):
    if len(poems) < 2:
        continue
    avg_s2 = statistics.mean(p['avg_s2'] for p in poems)
    echo_all = statistics.mean(p['mean_echo_rate'] for p in poems)
    hi_s2_echo_vals = [p['high_s2_echo_rate'] for p in poems if p['high_s2_echo_rate'] is not None]
    lo_s2_echo_vals = [p['low_s2_echo_rate'] for p in poems if p['low_s2_echo_rate'] is not None]
    top1_echo = statistics.mean(p['top1_echo_rate'] for p in poems)

    hi_echo = statistics.mean(hi_s2_echo_vals) if hi_s2_echo_vals else float('nan')
    lo_echo = statistics.mean(lo_s2_echo_vals) if lo_s2_echo_vals else float('nan')

    print(f"{era:<25} {len(poems):>4}  {avg_s2:>+7.3f}  {echo_all:>9.3f}  {hi_echo:>11.3f}  {lo_echo:>11.3f}  {top1_echo:>9.3f}")
    era_rows.append({'era': era, 'n': len(poems), 'avg_s2': avg_s2,
                     'echo_all': echo_all, 'hi_s2_echo': hi_echo,
                     'lo_s2_echo': lo_echo, 'top1_echo': top1_echo})

# --- Global S2 quintile breakdown ---
print("\n=== Echo Rate by S2 Quintile (global, all tokens) ===")
all_token_records = []
for pr in poem_results:
    for tok in pr['per_token']:
        all_token_records.append(tok)

all_token_records.sort(key=lambda x: x['s2'])
n = len(all_token_records)
quintile_size = n // 5

print(f"Total token records: {n}")
for q in range(5):
    start = q * quintile_size
    end = (q + 1) * quintile_size if q < 4 else n
    group = all_token_records[start:end]
    s2_range = (group[0]['s2'], group[-1]['s2'])
    echo = statistics.mean(r['echo_rate'] for r in group)
    top1 = statistics.mean(1.0 if r['top_alt_in_poem'] else 0.0 for r in group)
    print(f"  Q{q+1} S2=[{s2_range[0]:+.2f}, {s2_range[1]:+.2f}]: echo_rate={echo:.3f}, top1_echo={top1:.3f}")

# --- Poem-level correlation: avg_s2 vs mean_echo_rate ---
print("\n=== Poem-level: Avg S2 vs. Mean Echo Rate ===")
# Sort poems by avg S2
sorted_poems = sorted(poem_results, key=lambda p: p['avg_s2'])
print("Quintile by poem avg_s2:")
pq_size = len(sorted_poems) // 5
for q in range(5):
    start = q * pq_size
    end = (q + 1) * pq_size if q < 4 else len(sorted_poems)
    group = sorted_poems[start:end]
    mean_s2 = statistics.mean(p['avg_s2'] for p in group)
    echo = statistics.mean(p['mean_echo_rate'] for p in group)
    hi_s2_vals = [p['high_s2_echo_rate'] for p in group if p['high_s2_echo_rate'] is not None]
    hi_echo = statistics.mean(hi_s2_vals) if hi_s2_vals else float('nan')
    print(f"  Q{q+1}: avg_s2={mean_s2:+.3f}, echo={echo:.3f}, high_s2_echo={hi_echo:.3f}")

# --- Top "suppression" poems: high avg_s2 but low echo rate ---
print("\n=== Top 'Pure Suppressors': High S2, Low Alternative Echo ===")
eligible = [p for p in poem_results if p['avg_s2'] > 0.1 and p['n_tokens'] > 20]
suppressors = sorted(eligible, key=lambda p: p['mean_echo_rate'])[:15]
for p in suppressors:
    print(f"  echo={p['mean_echo_rate']:.3f} | avg_s2={p['avg_s2']:+.3f} | {p['author']}: {p['title'][:40]}")

print("\n=== Top 'Delayed Fulfillers': High S2, High Alternative Echo ===")
fulfillers = sorted(eligible, key=lambda p: -p['mean_echo_rate'])[:15]
for p in fulfillers:
    print(f"  echo={p['mean_echo_rate']:.3f} | avg_s2={p['avg_s2']:+.3f} | {p['author']}: {p['title'][:40]}")

# --- Save results ---
output = {
    'era_stats': era_rows,
    'global_quintiles': [
        {
            'quintile': q + 1,
            's2_min': all_token_records[q * quintile_size]['s2'],
            's2_max': all_token_records[min((q + 1) * quintile_size - 1, n - 1)]['s2'],
            'echo_rate': statistics.mean(r['echo_rate'] for r in all_token_records[q * quintile_size:(q + 1) * quintile_size if q < 4 else n]),
            'top1_echo': statistics.mean(1.0 if r['top_alt_in_poem'] else 0.0 for r in all_token_records[q * quintile_size:(q + 1) * quintile_size if q < 4 else n]),
        }
        for q in range(5)
    ],
    'poem_results': [
        {k: v for k, v in p.items() if k != 'per_token'}
        for p in poem_results
    ]
}

with open(OUTPUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to {OUTPUT_PATH}")
