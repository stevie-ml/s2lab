"""
Closure Tokens: What ends a poem, and what does GPT-2 expect there?

Building on information_arcs_closure findings (front-load hypothesis confirmed),
this experiment focuses specifically on the final 10 tokens of each poem.

Research questions:
1. What grammatical/semantic types typically end poems?
2. Do poem-final tokens have higher or lower S2 than expected for their position?
3. Which poems end with the most surprising single final word?
4. Does the "final word S2" correlate with poetic era or reputation?
5. Is there a "last word effect" — are final tokens systematically more or less
   surprising than the second-to-last?
"""

import json
import sys
sys.path.insert(0, '/home/user/s2lab')

import re
from collections import defaultdict, Counter
import statistics

data = json.load(open('/home/user/s2lab/results/corpus_results.json'))

WINDOW = 10  # tokens from end/start to examine

# Token type classifier
PUNCTUATION = set(".,;:!?—–-'\"()[]{}...")
FUNCTION_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
    'for', 'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were',
    'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'must', 'shall', 'that', 'this',
    'it', 'its', 'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she',
    'they', 'their', 'them', 'not', 'no', 'so', 'if', 'then', 'than',
    'when', 'where', 'who', 'what', 'which', 'there', 'here', 'all', 'one',
}

def classify_token(tok):
    t = tok.strip().lower().strip(".,;:!?—–-'\"")
    if not t:
        return 'newline/space'
    if t in PUNCTUATION:
        return 'punctuation'
    if t in FUNCTION_WORDS:
        return 'function_word'
    if t[0].isupper():
        return 'proper_noun_or_capitalized'
    if t.isdigit():
        return 'number'
    return 'content_word'

# Gather per-poem stats
poems_stats = []
for entry in data:
    meta = entry['metadata']
    tokens = entry['tokens']
    if not tokens:
        continue

    n = len(tokens)
    if n < 5:
        continue

    # Split into opening, closing
    opening = tokens[:min(WINDOW, n // 3)]
    closing = tokens[max(0, n - WINDOW):]
    middle = tokens[len(opening):max(0, n - WINDOW)]

    avg_s2 = lambda toks: statistics.mean(t['s2'] for t in toks) if toks else 0

    final_token = tokens[-1]
    penultimate_token = tokens[-2] if n >= 2 else None

    # Classify final token
    ftype = classify_token(final_token['token'])

    # Get top alternative for final token
    alts = final_token.get('alternatives', [])
    top_pred = alts[0]['token'] if alts else ''

    poems_stats.append({
        'title': meta.get('title', 'Unknown'),
        'author': meta.get('author', 'Unknown'),
        'era': meta.get('era', 'unknown'),
        'n_tokens': n,
        'avg_s2_opening': avg_s2(opening),
        'avg_s2_closing': avg_s2(closing),
        'avg_s2_middle': avg_s2(middle) if middle else 0,
        'avg_s2_all': avg_s2(tokens),
        'final_token': final_token['token'],
        'final_s2': final_token['s2'],
        'final_surprisal': final_token['surprisal'],
        'final_entropy': final_token['entropy'],
        'final_type': ftype,
        'final_top_pred': top_pred,
        'penult_s2': penultimate_token['s2'] if penultimate_token else None,
        'closing_avg': avg_s2(closing),
        'arc_delta': avg_s2(closing) - avg_s2(opening),
    })

print("=" * 70)
print("CLOSURE TOKEN ANALYSIS")
print("=" * 70)
print(f"\nPoems analyzed: {len(poems_stats)}")

# --- 1. Final token type distribution ---
print("\n\n1. WHAT TYPES OF TOKENS END POEMS?")
print("-" * 50)
type_counts = Counter(p['final_type'] for p in poems_stats)
type_s2 = defaultdict(list)
for p in poems_stats:
    type_s2[p['final_type']].append(p['final_s2'])

print(f"{'Type':<35} {'Count':>6} {'Avg final S2':>14} {'Median S2':>10}")
for ftype, count in type_counts.most_common():
    s2vals = type_s2[ftype]
    avg = statistics.mean(s2vals)
    med = statistics.median(s2vals)
    print(f"{ftype:<35} {count:>6} {avg:>14.3f} {med:>10.3f}")

# --- 2. Final word S2 vs rest-of-poem ---
print("\n\n2. FINAL TOKEN S2 vs POEM AVERAGE")
print("-" * 50)
# Exclude prose control
poetry = [p for p in poems_stats if p['era'] != 'control']
final_higher = sum(1 for p in poetry if p['final_s2'] > p['avg_s2_all'])
print(f"Poems where final S2 > poem average: {final_higher}/{len(poetry)} ({100*final_higher/len(poetry):.1f}%)")
avg_final_s2 = statistics.mean(p['final_s2'] for p in poetry)
avg_all_s2 = statistics.mean(p['avg_s2_all'] for p in poetry)
print(f"Average final-token S2: {avg_final_s2:.3f}")
print(f"Average poem-wide S2:   {avg_all_s2:.3f}")
print(f"Delta (final - avg): {avg_final_s2 - avg_all_s2:+.3f}")

# --- 3. Last-word effect: final vs penultimate ---
has_both = [p for p in poetry if p['penult_s2'] is not None]
final_beats_penult = sum(1 for p in has_both if p['final_s2'] > p['penult_s2'])
avg_final = statistics.mean(p['final_s2'] for p in has_both)
avg_penult = statistics.mean(p['penult_s2'] for p in has_both)
print(f"\nFinal token S2 > penultimate token S2: {final_beats_penult}/{len(has_both)} ({100*final_beats_penult/len(has_both):.1f}%)")
print(f"Average final token S2:       {avg_final:.3f}")
print(f"Average penultimate token S2: {avg_penult:.3f}")
print(f"Delta: {avg_final - avg_penult:+.3f}")

# --- 4. Highest final-token S2 poems ---
print("\n\n3. MOST SURPRISING FINAL TOKENS")
print("-" * 70)
print(f"{'Title':<38} {'Author':<22} {'Final token':<14} {'Predicted':<14} {'S2':>7}")
print("-" * 70)
sorted_by_final = sorted(poetry, key=lambda p: -p['final_s2'])
for p in sorted_by_final[:15]:
    title = p['title'][:36]
    author = p['author'][:20]
    final = repr(p['final_token'])[:12]
    pred = repr(p['final_top_pred'])[:12]
    print(f"{title:<38} {author:<22} {final:<14} {pred:<14} {p['final_s2']:>7.2f}")

# --- 5. Lowest final-token S2 (most resolved endings) ---
print("\n\n4. MOST RESOLVED ENDINGS (lowest final S2)")
print("-" * 70)
print(f"{'Title':<38} {'Author':<22} {'Final token':<14} {'Predicted':<14} {'S2':>7}")
print("-" * 70)
for p in sorted_by_final[-15:]:
    title = p['title'][:36]
    author = p['author'][:20]
    final = repr(p['final_token'])[:12]
    pred = repr(p['final_top_pred'])[:12]
    print(f"{title:<38} {author:<22} {final:<14} {pred:<14} {p['final_s2']:>7.2f}")

# --- 6. By era ---
print("\n\n5. FINAL TOKEN S2 BY ERA")
print("-" * 60)
era_stats = defaultdict(list)
for p in poetry:
    era_stats[p['era']].append(p['final_s2'])

print(f"{'Era':<25} {'N':>4} {'Avg final S2':>14} {'% final > avg':>14}")
for era, vals in sorted(era_stats.items(), key=lambda x: -statistics.mean(x[1])):
    era_poems = [p for p in poetry if p['era'] == era]
    pct_above_avg = 100 * sum(1 for p in era_poems if p['final_s2'] > p['avg_s2_all']) / len(era_poems)
    print(f"{era:<25} {len(vals):>4} {statistics.mean(vals):>14.3f} {pct_above_avg:>13.1f}%")

# --- 7. "Last word motif" — what words appear as final tokens ---
print("\n\n6. RECURRING FINAL WORD CATEGORIES")
print("-" * 50)
final_words_clean = [p['final_token'].strip().lower().strip(".,;:!?—–\"'") for p in poetry]
word_freq = Counter(final_words_clean)
print("Most common final words (cleaned):")
for word, count in word_freq.most_common(20):
    if count > 1:
        avg = statistics.mean(p['final_s2'] for p in poetry
                               if p['final_token'].strip().lower().strip(".,;:!?—–\"'") == word)
        print(f"  '{word}': {count} poems, avg final S2 = {avg:.2f}")

# --- 8. Final-closure pattern: does high final S2 poem have high opening S2? ---
print("\n\n7. FINAL S2 vs OPENING S2 CORRELATION")
print("-" * 50)
xs = [p['avg_s2_opening'] for p in poetry]
ys = [p['final_s2'] for p in poetry]
n = len(xs)
mx, my = sum(xs) / n, sum(ys) / n
cov = sum((xs[i] - mx) * (ys[i] - my) for i in range(n)) / n
sx = (sum((xi - mx) ** 2 for xi in xs) / n) ** 0.5
sy = (sum((yi - my) ** 2 for yi in ys) / n) ** 0.5
r = cov / (sx * sy) if sx * sy > 0 else 0
print(f"Pearson r (opening avg S2 vs final token S2): {r:.3f}")
print("(Negative = high-opening poems have low-S2 endings = resolution)")
print("(Positive = high-opening poems also end with surprise = crescendo pattern)")

# --- 9. Extreme examples of final token context ---
print("\n\n8. STRAUSSIAN FINAL MOMENTS — TOP 10 CASES IN DETAIL")
print("-" * 70)
for p in sorted_by_final[:10]:
    entry = next(e for e in data if e['metadata'].get('title') == p['title'])
    tokens_all = entry['tokens']
    last = tokens_all[-1]
    ctx_start = max(0, len(tokens_all) - 6)
    ctx = ''.join(t['token'] for t in tokens_all[ctx_start:-1])
    alts = last.get('alternatives', [])
    top3 = ', '.join(f"'{a['token']}' ({a['prob']:.2%})" for a in alts[:3])
    print(f"\n{p['author']}, '{p['title']}':")
    print(f"  ...{ctx!r} → [{last['token']!r}]")
    print(f"  GPT-2 expected: {top3}")
    print(f"  S2 = {last['s2']:.2f} | Surprisal = {last['surprisal']:.2f} | Entropy = {last['entropy']:.2f}")

print("\n\nANALYSIS COMPLETE")
