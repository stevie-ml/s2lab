"""
Subword Tokenization and S2: Where Does Poetic Surprise Actually Live?

GPT-2 uses byte-pair encoding (BPE). Common words = single tokens.
Rare words = multiple tokens (e.g., "extraordinary" → ["extra", "ord", "inary"]).

Hypothesis: The S2 measure mixes two fundamentally different populations:
  1. Word-START tokens (Ġ-prefix, space-leading): genuine lexical choices
  2. Word-CONTINUATION tokens (no space prefix): largely predetermined once word-start is known

If true, the "Straussian gap" lives almost entirely in word-start tokens.
Continuation tokens are low-S2 artefacts of how GPT-2 tokenizes unusual words.
"""

import json
import re
from collections import defaultdict

with open("results/corpus_results.json") as f:
    data = json.load(f)

# ─────────────────────────────────────────────
# Classify each token
# ─────────────────────────────────────────────

def classify_tokens_sequential(tokens):
    """
    Classify tokens using sequential context:
      - After '\n' the next token is a 'line_start' (GPT-2 drops space prefix after newline)
      - Tokens starting with ' ' (space prefix) are 'word_start'
      - Tokens without space prefix that follow a word_start/line_start or
        another continuation are 'continuation' (true subword)
      - '\n' and whitespace-only tokens are 'special'

    Returns a list of classes parallel to tokens.
    """
    classes = []
    after_newline = True  # poem begins at a line start

    for tok in tokens:
        txt = tok['token']

        if txt == '\n' or txt.strip() == '':
            classes.append('special')
            after_newline = True
            continue

        if txt.startswith(' '):
            classes.append('word_start')
            after_newline = False
            continue

        # No leading space.
        if after_newline:
            # First token of a new line — NOT a subword continuation
            classes.append('line_start')
            after_newline = False
        else:
            # Follows a non-newline token without a space prefix: true subword
            classes.append('continuation')

    return classes

# ─────────────────────────────────────────────
# Collect token-level data
# ─────────────────────────────────────────────

classes = defaultdict(list)   # class -> [s2, ...]
era_word_starts = defaultdict(list)
era_continuations = defaultdict(list)
author_data = defaultdict(lambda: {'starts': [], 'conts': []})

word_complexity = defaultdict(list)   # n_tokens_in_word -> [s2 of start token]
multi_word_pairs = []  # (start_s2, cont_s2) for 2-token words

poems_english = [p for p in data if p['metadata'].get('language', 'en') == 'en']

for poem in poems_english:
    era = poem['metadata'].get('era', 'unknown')
    author = poem['metadata'].get('author', 'Unknown')
    tokens = poem['tokens']
    tok_classes = classify_tokens_sequential(tokens)

    for i, (tok, cls) in enumerate(zip(tokens, tok_classes)):
        s2 = tok['s2']
        classes[cls].append(s2)

        if cls in ('word_start', 'line_start'):
            era_word_starts[era].append(s2)
            author_data[author]['starts'].append(s2)

            if cls == 'word_start':
                # How many tokens does this word span?
                n_toks = 1
                j = i + 1
                while j < len(tokens) and tok_classes[j] == 'continuation':
                    n_toks += 1
                    j += 1
                word_complexity[n_toks].append(s2)

                # Pair start + first continuation
                if i + 1 < len(tokens) and tok_classes[i+1] == 'continuation':
                    multi_word_pairs.append((s2, tokens[i+1]['s2']))

        elif cls == 'continuation':
            era_continuations[era].append(s2)
            author_data[author]['conts'].append(s2)

# ─────────────────────────────────────────────
# Aggregate stats
# ─────────────────────────────────────────────

def stats(vals):
    if not vals:
        return {}
    n = len(vals)
    mu = sum(vals) / n
    pos = sum(1 for v in vals if v > 0) / n * 100
    return {'n': n, 'mean': round(mu, 3), 'pos_pct': round(pos, 1)}

print("=== GLOBAL CLASSIFICATION STATS ===\n")
for cls in ['word_start', 'line_start', 'continuation', 'special']:
    s = stats(classes[cls])
    print(f"  {cls:20s}  n={s.get('n',0):6d}  mean_s2={s.get('mean', 0):+.3f}  pos_s2%={s.get('pos_pct', 0):.1f}%")

print()
# Combined word-start-equivalent vs continuation
ws_vals = classes['word_start'] + classes['line_start']
ct_vals = classes['continuation']
ws = stats(ws_vals)
ct = stats(ct_vals)
print(f"  {'WORD-START (all)':20s}  n={ws['n']:6d}  mean_s2={ws['mean']:+.3f}  pos_s2%={ws['pos_pct']:.1f}%")
print(f"  {'CONTINUATION':20s}  n={ct['n']:6d}  mean_s2={ct['mean']:+.3f}  pos_s2%={ct['pos_pct']:.1f}%")
print(f"\n  S2 gap (word_start − continuation): {ws['mean'] - ct['mean']:+.3f} bits")

print("\n=== WORD COMPLEXITY (n tokens per word) → start-token S2 ===\n")
for n_toks in sorted(word_complexity):
    s = stats(word_complexity[n_toks])
    bar = '█' * max(0, int((s['mean'] + 2) * 4))
    print(f"  {n_toks}-token words: mean_s2={s['mean']:+.3f}  n={s['n']:5d}  {bar}")

print("\n=== MULTI-WORD PAIRS: S2 DROP from start → first continuation ===\n")
if multi_word_pairs:
    drops = [c - s for s, c in multi_word_pairs]
    mean_drop = sum(drops) / len(drops)
    pct_drop = sum(1 for d in drops if d < 0) / len(drops) * 100
    start_means = [s for s, _ in multi_word_pairs]
    cont_means = [c for _, c in multi_word_pairs]
    print(f"  n pairs:               {len(multi_word_pairs)}")
    print(f"  mean S2 at word-start: {sum(start_means)/len(start_means):+.3f}")
    print(f"  mean S2 at 1st cont:   {sum(cont_means)/len(cont_means):+.3f}")
    print(f"  mean Δ (cont - start): {mean_drop:+.3f}")
    print(f"  % pairs where S2 drops:{pct_drop:.1f}%")

print("\n=== ERA BREAKDOWN: word-start S2 vs continuation S2 ===\n")
all_eras = sorted(set(list(era_word_starts.keys()) + list(era_continuations.keys())))
print(f"  {'Era':22s}  {'WS mean':>8}  {'Cont mean':>9}  {'Gap':>6}  n_ws  n_cont")
era_rows = []
for era in all_eras:
    ws_e = stats(era_word_starts[era])
    ct_e = stats(era_continuations[era])
    gap = ws_e.get('mean', 0) - ct_e.get('mean', 0)
    era_rows.append((era, ws_e, ct_e, gap))

era_rows.sort(key=lambda x: x[1].get('mean', 0), reverse=True)
for era, ws_e, ct_e, gap in era_rows:
    print(f"  {era:22s}  {ws_e.get('mean', 0):+8.3f}  {ct_e.get('mean', 0):+9.3f}  {gap:+6.3f}  {ws_e.get('n', 0):5d}  {ct_e.get('n', 0)}")

print("\n=== AUTHOR BREAKDOWN (≥3 word-starts): word-start mean S2 ===\n")
author_rows = []
for author, d in author_data.items():
    if len(d['starts']) < 3:
        continue
    ws_a = stats(d['starts'])
    ct_a = stats(d['conts']) if d['conts'] else {'mean': float('nan'), 'n': 0}
    author_rows.append((author, ws_a, ct_a))

author_rows.sort(key=lambda x: x[1]['mean'], reverse=True)
print(f"  {'Author':35s}  {'WS mean':>8}  {'WS n':>5}  {'Cont mean':>9}  {'Cont n':>6}")
for author, ws_a, ct_a in author_rows[:20]:
    print(f"  {author:35s}  {ws_a['mean']:+8.3f}  {ws_a['n']:5d}  {ct_a.get('mean', 0):+9.3f}  {ct_a.get('n', 0):6d}")

print("\n=== TOP HIGH-S2 CONTINUATION TOKENS (the interesting exceptions) ===")
print("  (Where GPT-2 was still surprised mid-word — rarest words)\n")
high_cont = []
for poem in poems_english:
    tokens = poem['tokens']
    tok_classes = classify_tokens_sequential(tokens)
    for i, (tok, cls) in enumerate(zip(tokens, tok_classes)):
        if cls == 'continuation' and tok['s2'] > 3.0:
            # Find the word start
            j = i - 1
            word_so_far = tok['token']
            while j >= 0 and tok_classes[j] == 'continuation':
                word_so_far = tokens[j]['token'] + word_so_far
                j -= 1
            if j >= 0:
                word_so_far = tokens[j]['token'] + word_so_far
            high_cont.append({
                'poem': poem['metadata']['title'],
                'author': poem['metadata']['author'],
                'word': word_so_far.strip(),
                'cont_token': tok['token'],
                's2': tok['s2'],
                'context': tok.get('context_before', ''),
            })

high_cont.sort(key=lambda x: x['s2'], reverse=True)
for item in high_cont[:15]:
    print(f"  s2={item['s2']:+6.2f}  word='{item['word']}'  cont='{item['cont_token']}'  — {item['author']}: \"{item['poem']}\"")
