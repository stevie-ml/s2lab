"""
Ghost Word Fulfillment: Does the Rejected Prediction Appear Later in the Poem?

When GPT-2 predicts token X but the poet chooses token Y (high S2 moment),
does X appear later in the poem? And if so, does it arrive with lower S2
than average — as if the prediction is finally "fulfilled"?

Hypothesis: Poets use semantic tension — frustrating expectations early, then
partially satisfying them late. The "ghost word" (the suppressed prediction)
haunts the poem until it either appears (fulfillment) or never does (permanent
withholding).

Two sub-questions:
1. FREQUENCY: How often does the top-1 rejected prediction appear later in the poem?
2. S2 AT FULFILLMENT: When it does appear, what is its S2 relative to poem average?
   (If poets deliberately "resolve" ghost words, they should arrive at below-average S2)
"""

import json
import sys
sys.path.insert(0, '/home/user/s2lab')

from collections import defaultdict
import statistics

# Load corpus
data = json.load(open('/home/user/s2lab/results/corpus_results.json'))

# Filter to English poems with enough tokens
poems = [
    p for p in data
    if p['metadata'].get('language', 'en') == 'en'
    and p['metadata'].get('era') not in ('control',)
    and len(p['tokens']) >= 20
]

print(f"Analyzing {len(poems)} poems\n")

# ── Experiment ─────────────────────────────────────────────────────────────────

results_by_poem = []
fulfillment_s2_vals = []      # S2 at the moment of ghost-word fulfillment
unfulfilled_s2_vals = []      # Avg S2 at equivalent positions when ghost NOT fulfilled
ghost_word_fulfilled_count = 0
ghost_word_total = 0
era_stats = defaultdict(lambda: {'fulfilled': 0, 'total': 0,
                                  'fulfillment_s2': [], 'avg_s2': []})

ARTIFACT_THRESHOLD = 0.9      # Skip stanza-break artifact tokens

for poem in poems:
    tokens = poem['tokens']
    n = len(tokens)
    era = poem['metadata'].get('era', 'unknown')
    avg_s2 = poem['summary']['avg_s2']

    # Build a list of content tokens (non-artifact) for this poem
    content_tokens = [t for t in tokens if t.get('p_newline', 0) < ARTIFACT_THRESHOLD]
    if not content_tokens:
        continue

    # For each content token with S2 > 2.0 (meaningful deviation),
    # check what GPT-2's top-1 prediction was and whether it appears later
    poem_ghost_words = []

    for idx, tok in enumerate(content_tokens):
        if tok['s2'] < 2.0:
            continue
        if not tok.get('alternatives'):
            continue

        ghost = tok['alternatives'][0]['token'].strip().lower()
        if not ghost or len(ghost) < 2 or ghost in ('\n', '', ' '):
            continue

        # Look for the ghost word in later content tokens (same poem)
        later_tokens = content_tokens[idx + 1:]

        # Does the ghost word appear later? (exact match, case-insensitive)
        fulfilled = False
        fulfillment_s2 = None
        for later_tok in later_tokens:
            if later_tok['token'].strip().lower() == ghost:
                fulfilled = True
                fulfillment_s2 = later_tok['s2']
                break

        poem_ghost_words.append({
            'ghost': ghost,
            'at_s2': tok['s2'],
            'at_token': tok['token'],
            'fulfilled': fulfilled,
            'fulfillment_s2': fulfillment_s2,
        })

        ghost_word_total += 1
        era_stats[era]['total'] += 1
        era_stats[era]['avg_s2'].append(avg_s2)

        if fulfilled:
            ghost_word_fulfilled_count += 1
            era_stats[era]['fulfilled'] += 1
            fulfillment_s2_vals.append(fulfillment_s2)
            era_stats[era]['fulfillment_s2'].append(fulfillment_s2)
        else:
            unfulfilled_s2_vals.append(avg_s2)

    if poem_ghost_words:
        results_by_poem.append({
            'title': poem['metadata']['title'],
            'author': poem['metadata']['author'],
            'era': era,
            'avg_s2': avg_s2,
            'ghost_words': poem_ghost_words,
        })

# ── Summary Statistics ─────────────────────────────────────────────────────────

print(f"{'='*60}")
print(f"GHOST WORD FULFILLMENT ANALYSIS")
print(f"{'='*60}\n")

print(f"Total high-S2 moments analyzed: {ghost_word_total}")
print(f"Ghost words fulfilled (appear later): {ghost_word_fulfilled_count} "
      f"({100*ghost_word_fulfilled_count/ghost_word_total:.1f}%)")
print(f"Ghost words never fulfilled: {ghost_word_total - ghost_word_fulfilled_count} "
      f"({100*(ghost_word_total - ghost_word_fulfilled_count)/ghost_word_total:.1f}%)\n")

if fulfillment_s2_vals:
    print(f"S2 at fulfillment (when ghost word appears later):")
    print(f"  Mean S2:   {statistics.mean(fulfillment_s2_vals):.3f}")
    print(f"  Median S2: {statistics.median(fulfillment_s2_vals):.3f}")
    print(f"  Stdev S2:  {statistics.stdev(fulfillment_s2_vals):.3f}")

if unfulfilled_s2_vals:
    print(f"\nPoem avg S2 for unfulfilled ghost words:")
    print(f"  Mean poem avg S2:   {statistics.mean(unfulfilled_s2_vals):.3f}")

print()

# ── Gap: Fulfillment S2 vs. Poem Average ──────────────────────────────────────

gaps = []
for poem in results_by_poem:
    for gw in poem['ghost_words']:
        if gw['fulfilled']:
            gap = gw['fulfillment_s2'] - poem['avg_s2']
            gaps.append(gap)

if gaps:
    print(f"S2 at fulfillment MINUS poem's avg S2 (the 'resolution gap'):")
    print(f"  Mean gap:   {statistics.mean(gaps):.3f}")
    print(f"  Median gap: {statistics.median(gaps):.3f}")
    neg = sum(1 for g in gaps if g < 0)
    print(f"  % below poem average (resolved): {100*neg/len(gaps):.1f}%")
    print()

# ── By Era ─────────────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"GHOST WORD FULFILLMENT BY ERA")
print(f"{'='*60}\n")

print(f"{'Era':<22} {'N':>5} {'Fulfill%':>9} {'Fulfill S2':>11} {'Poem Avg':>9} {'Gap':>7}")
print(f"{'-'*22} {'-'*5} {'-'*9} {'-'*11} {'-'*9} {'-'*7}")

era_rows = []
for era, stats in era_stats.items():
    if stats['total'] < 5:
        continue
    pct = 100 * stats['fulfilled'] / stats['total']
    f_s2 = statistics.mean(stats['fulfillment_s2']) if stats['fulfillment_s2'] else float('nan')
    p_avg = statistics.mean(stats['avg_s2']) if stats['avg_s2'] else float('nan')
    gap = f_s2 - p_avg if stats['fulfillment_s2'] else float('nan')
    era_rows.append((era, stats['total'], pct, f_s2, p_avg, gap))

era_rows.sort(key=lambda x: x[2], reverse=True)  # sort by fulfillment %
for row in era_rows:
    era, n, pct, f_s2, p_avg, gap = row
    f_s2_str = f"{f_s2:.3f}" if f_s2 == f_s2 else "n/a"
    gap_str = f"{gap:+.3f}" if gap == gap else "n/a"
    print(f"{era:<22} {n:>5} {pct:>8.1f}% {f_s2_str:>11} {p_avg:>9.3f} {gap_str:>7}")

# ── Most Striking Examples ─────────────────────────────────────────────────────

print(f"\n{'='*60}")
print(f"MOST STRIKING GHOST WORD FULFILLMENTS (high initial S2, then resolved)")
print(f"{'='*60}\n")

all_cases = []
for poem in results_by_poem:
    for gw in poem['ghost_words']:
        if gw['fulfilled']:
            gap = gw['fulfillment_s2'] - poem['avg_s2']
            all_cases.append({
                'poem': poem['title'],
                'author': poem['author'],
                'ghost': gw['ghost'],
                'at_token': gw['at_token'],
                'at_s2': gw['at_s2'],
                'fulfillment_s2': gw['fulfillment_s2'],
                'poem_avg_s2': poem['avg_s2'],
                'gap': gap,
            })

# Top 10 resolved (largest negative gap = most "satisfied" fulfillment)
top_resolved = sorted(all_cases, key=lambda x: x['gap'])[:12]
print("Top resolved (ghost word arrives at lowest S2 relative to poem average):\n")
for i, c in enumerate(top_resolved, 1):
    print(f"{i:2}. '{c['ghost']}' rejected at S2={c['at_s2']:.2f} (chose '{c['at_token'].strip()}')")
    print(f"    → appeared later at S2={c['fulfillment_s2']:.2f} (poem avg={c['poem_avg_s2']:.2f}, gap={c['gap']:+.2f})")
    print(f"    — {c['author']}, \"{c['poem']}\"")
    print()

# Top 10 detonated (ghost word arrives at very HIGH S2 — paradox, irony)
print("\nTop detonated (ghost word arrives with high S2 — unexpected even when fulfilled):\n")
top_detonated = sorted(all_cases, key=lambda x: x['gap'], reverse=True)[:8]
for i, c in enumerate(top_detonated, 1):
    print(f"{i:2}. '{c['ghost']}' rejected at S2={c['at_s2']:.2f} (chose '{c['at_token'].strip()}')")
    print(f"    → appeared later at S2={c['fulfillment_s2']:.2f} (poem avg={c['poem_avg_s2']:.2f}, gap={c['gap']:+.2f})")
    print(f"    — {c['author']}, \"{c['poem']}\"")
    print()

# ── Ghost Word Frequency Table ─────────────────────────────────────────────────

from collections import Counter
ghost_counts = Counter()
fulfilled_counts = Counter()
for poem in results_by_poem:
    for gw in poem['ghost_words']:
        g = gw['ghost']
        ghost_counts[g] += 1
        if gw['fulfilled']:
            fulfilled_counts[g] += 1

print(f"\n{'='*60}")
print(f"MOST COMMON GHOST WORDS (rejected top-1 predictions at high-S2 moments)")
print(f"{'='*60}\n")
print(f"{'Ghost Word':<20} {'Rejected':>8} {'Fulfilled':>10} {'Fulfill%':>10}")
print(f"{'-'*20} {'-'*8} {'-'*10} {'-'*10}")
for word, cnt in ghost_counts.most_common(20):
    f_cnt = fulfilled_counts.get(word, 0)
    pct = 100 * f_cnt / cnt
    print(f"{word:<20} {cnt:>8} {f_cnt:>10} {pct:>9.1f}%")

print("\nDone.")
