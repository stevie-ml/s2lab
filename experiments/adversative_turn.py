"""
The Adversative Turn: S₂ Dynamics After Contrastive Conjunctions in Poetry

Research question: When poets deploy adversative conjunctions ("but", "yet", "though",
"although"), they signal a semantic reversal — the current line of argument gives way
to its opposite. How does this rhetorical figure manifest in GPT-2's information-theoretic
profile?

Hypotheses:
  H1. Adversative conjunctions have high entropy (GPT-2 is uncertain what reversal comes)
  H2. Tokens immediately following adversatives have elevated S₂ (poets exploit the
      high-entropy window to make unexpected choices)
  H3. The "reversal window" (3–5 tokens after the adversative) has higher S₂ than the
      "run-up window" (3–5 tokens before it)
  H4. "but" and "yet" at line-initial positions (classic Shakespearean pivot markers)
      show stronger effects than medial adversatives

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import re
from collections import defaultdict
import statistics

# ── Adversative categories ────────────────────────────────────────────────────

COORD_ADVERSATIVE = {
    'but', 'yet', 'still'
}

SUBORD_ADVERSATIVE = {
    'though', 'although', 'whereas', 'while', 'whilst'
}

CONJ_ADV = {
    'however', 'nevertheless', 'nonetheless', 'notwithstanding',
    'conversely', 'instead', 'rather'
}

ALL_ADVERSATIVE = COORD_ADVERSATIVE | SUBORD_ADVERSATIVE | CONJ_ADV

# Context window
WINDOW_SIZE = 5


def normalize(token: str) -> str:
    return token.strip().lower()


def mean(xs):
    return sum(xs) / len(xs) if xs else float('nan')


def median(xs):
    if not xs:
        return float('nan')
    return statistics.median(xs)


def std(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def classify_adversative(norm_tok):
    if norm_tok in COORD_ADVERSATIVE:
        return 'coordinating'
    if norm_tok in SUBORD_ADVERSATIVE:
        return 'subordinating'
    if norm_tok in CONJ_ADV:
        return 'conjunctive'
    return None


with open('results/corpus_results.json') as f:
    corpus = json.load(f)


# ── Main analysis ─────────────────────────────────────────────────────────────

adversative_records = []
all_tokens_s2 = []          # baseline S2 (all non-adversative tokens)
baseline_entropy = []       # baseline entropy
baseline_surprisal = []

for poem in corpus:
    meta = poem['metadata']
    tokens = poem['tokens']

    if meta.get('language', 'en') != 'en':
        continue
    if meta.get('era') == 'control':
        continue

    poem_s2 = [t['s2'] for t in tokens]

    for i, tok in enumerate(tokens):
        norm = normalize(tok['token'])

        # Track baseline
        cat = classify_adversative(norm)
        if cat is None:
            all_tokens_s2.append(tok['s2'])
            baseline_entropy.append(tok['entropy'])
            baseline_surprisal.append(tok['surprisal'])
        else:
            # Build window records
            pre_window = tokens[max(0, i - WINDOW_SIZE): i]
            post_window = tokens[i + 1: i + 1 + WINDOW_SIZE]

            # Detect line-initial position (context_before ends with \n or is very short)
            ctx_before = tok.get('context_before', '')
            lines_before = ctx_before.split('\n')
            is_line_initial = (
                len(lines_before[-1].strip()) == 0 or
                len(lines_before[-1].strip()) <= 3   # only whitespace/short lead
            )

            record = {
                'token': tok['token'].strip(),
                'norm': norm,
                'category': cat,
                's2': tok['s2'],
                'surprisal': tok['surprisal'],
                'entropy': tok['entropy'],
                'position': tok.get('position', i),
                'is_line_initial': is_line_initial,

                # Window values
                'pre_s2': [t['s2'] for t in pre_window],
                'pre_entropy': [t['entropy'] for t in pre_window],
                'post_s2': [t['s2'] for t in post_window],
                'post_entropy': [t['entropy'] for t in post_window],
                'post_tokens_detail': [
                    {
                        'token': t['token'].strip(),
                        's2': t['s2'],
                        'entropy': t['entropy'],
                        'surprisal': t['surprisal'],
                        'top_pred': (t.get('alternatives') or [{}])[0].get('token', '?'),
                        'top_prob': (t.get('alternatives') or [{}])[0].get('prob', 0),
                    }
                    for t in post_window
                ],
                'alternatives_at_adv': tok.get('alternatives', [])[:5],

                # Context string
                'context_before': ctx_before[-80:],

                # Metadata
                'author': meta['author'],
                'title': meta['title'],
                'era': meta.get('era', '?'),
                'poem_avg_s2': mean(poem_s2),
            }
            adversative_records.append(record)


# ── REPORT ────────────────────────────────────────────────────────────────────

total_poems = len(corpus)
n_adv = len(adversative_records)
global_mean_s2 = mean(all_tokens_s2)
global_mean_entropy = mean(baseline_entropy)

print('=' * 70)
print('THE ADVERSATIVE TURN: S₂ AFTER CONTRASTIVE CONJUNCTIONS IN POETRY')
print('=' * 70)
print(f'\nCorpus: {total_poems} texts | Adversative tokens found: {n_adv}')
print(f'Baseline (non-adversative) mean S₂: {global_mean_s2:+.3f}')
print(f'Baseline mean entropy: {global_mean_entropy:.3f} bits')


# ── 1. BY ADVERSATIVE CATEGORY ───────────────────────────────────────────────

print('\n\n## 1. Adversative Tokens: S₂ and Entropy by Category\n')
print(f'{"Category":<18} {"n":>4} {"S₂(self)":>9} {"H(self)":>8} {"post-S₂":>9} {"pre-S₂":>9} {"lift":>7}')
print('-' * 65)

by_cat = defaultdict(list)
for r in adversative_records:
    by_cat[r['category']].append(r)

for cat in ['coordinating', 'subordinating', 'conjunctive']:
    recs = by_cat[cat]
    if not recs:
        continue
    self_s2 = [r['s2'] for r in recs]
    self_h = [r['entropy'] for r in recs]
    post_s2 = [mean(r['post_s2']) for r in recs if r['post_s2']]
    pre_s2 = [mean(r['pre_s2']) for r in recs if r['pre_s2']]
    lift = mean(post_s2) - mean(pre_s2) if post_s2 and pre_s2 else float('nan')
    print(f'{cat:<18} {len(recs):>4} {mean(self_s2):>+9.3f} {mean(self_h):>8.3f} '
          f'{mean(post_s2):>+9.3f} {mean(pre_s2):>+9.3f} {lift:>+7.3f}')

# Overall
all_self_s2 = [r['s2'] for r in adversative_records]
all_post_s2 = [mean(r['post_s2']) for r in adversative_records if r['post_s2']]
all_pre_s2  = [mean(r['pre_s2']) for r in adversative_records if r['pre_s2']]
print(f'{"TOTAL":<18} {n_adv:>4} {mean(all_self_s2):>+9.3f} '
      f'{mean([r["entropy"] for r in adversative_records]):>8.3f} '
      f'{mean(all_post_s2):>+9.3f} {mean(all_pre_s2):>+9.3f} '
      f'{mean(all_post_s2)-mean(all_pre_s2):>+7.3f}')
print(f'{"baseline":<18} {"--":>4} {global_mean_s2:>+9.3f} {global_mean_entropy:>8.3f}')


# ── 2. BY SPECIFIC CONJUNCTION ───────────────────────────────────────────────

print('\n\n## 2. Per-Conjunction Breakdown\n')
print(f'{"Word":<12} {"n":>4} {"S₂(self)":>9} {"H(self)":>8} {"post-1 S₂":>10} {"post-2 S₂":>10} {"post-3 S₂":>10}')
print('-' * 70)

by_word = defaultdict(list)
for r in adversative_records:
    by_word[r['norm']].append(r)

word_rows = []
for word, recs in by_word.items():
    if len(recs) < 3:
        continue
    self_s2 = mean([r['s2'] for r in recs])
    self_h  = mean([r['entropy'] for r in recs])

    # Post-1, post-2, post-3 tokens
    p1 = [r['post_tokens_detail'][0]['s2'] for r in recs if len(r['post_tokens_detail']) > 0]
    p2 = [r['post_tokens_detail'][1]['s2'] for r in recs if len(r['post_tokens_detail']) > 1]
    p3 = [r['post_tokens_detail'][2]['s2'] for r in recs if len(r['post_tokens_detail']) > 2]
    word_rows.append((word, len(recs), self_s2, self_h, mean(p1), mean(p2), mean(p3)))

word_rows.sort(key=lambda x: -x[1])
for row in word_rows:
    word, n, ss2, sh, mp1, mp2, mp3 = row
    print(f'"{word}"<{12-2} {n:>4} {ss2:>+9.3f} {sh:>8.3f} {mp1:>+10.3f} {mp2:>+10.3f} {mp3:>+10.3f}')


# ── 3. LINE-INITIAL vs MEDIAL ────────────────────────────────────────────────

print('\n\n## 3. Line-Initial vs. Medial Adversatives\n')
print(f'{"Position":<16} {"n":>4} {"S₂(adv)":>9} {"H(adv)":>8} {"post-window S₂":>15} {"lift":>7}')
print('-' * 65)

for position_label, pred in [('Line-initial', True), ('Medial', False)]:
    recs = [r for r in adversative_records if r['is_line_initial'] == pred]
    if not recs:
        continue
    self_s2 = mean([r['s2'] for r in recs])
    self_h  = mean([r['entropy'] for r in recs])
    post_s2 = [mean(r['post_s2']) for r in recs if r['post_s2']]
    pre_s2  = [mean(r['pre_s2']) for r in recs if r['pre_s2']]
    lift = mean(post_s2) - mean(pre_s2) if post_s2 and pre_s2 else float('nan')
    print(f'{position_label:<16} {len(recs):>4} {self_s2:>+9.3f} {self_h:>8.3f} '
          f'{mean(post_s2):>+15.3f} {lift:>+7.3f}')


# ── 4. DISTRIBUTION: S₂ in reversal window vs baseline ──────────────────────

print('\n\n## 4. S₂ Distribution: Reversal Window vs. Run-Up Window\n')

# Collect all post-adversative S2 values (positions +1 to +5)
post_all = []
pre_all  = []
for r in adversative_records:
    post_all.extend(r['post_s2'])
    pre_all.extend(r['pre_s2'])

def pct_pos(xs):
    return 100 * sum(1 for x in xs if x > 0) / len(xs) if xs else 0

print(f'{"Window":<22} {"n":>6} {"mean S₂":>9} {"median":>8} {"std":>7} {"pos%":>6}')
print('-' * 58)
print(f'{"Post-adversative (+1–5)":<22} {len(post_all):>6} {mean(post_all):>+9.3f} '
      f'{median(post_all):>+8.3f} {std(post_all):>7.3f} {pct_pos(post_all):>5.1f}%')
print(f'{"Pre-adversative (−5–−1)":<22} {len(pre_all):>6} {mean(pre_all):>+9.3f} '
      f'{median(pre_all):>+8.3f} {std(pre_all):>7.3f} {pct_pos(pre_all):>5.1f}%')
print(f'{"Global baseline":<22} {len(all_tokens_s2):>6} {global_mean_s2:>+9.3f} '
      f'{median(all_tokens_s2):>+8.3f} {std(all_tokens_s2):>7.3f} '
      f'{pct_pos(all_tokens_s2):>5.1f}%')


# ── 5. HIGHEST-S₂ POST-ADVERSATIVE MOMENTS ──────────────────────────────────

print('\n\n## 5. The Most Surprising Post-Adversative Words\n')
print('(Top 20 by S₂ of the first token after the adversative)\n')
print(f'{"S₂":>7} | {"Adv":>6} | {"Surprise word":<16} | {"Top pred":>12} | {"P(pred)":>8} | Source')
print('-' * 90)

post_tok_examples = []
for r in adversative_records:
    if not r['post_tokens_detail']:
        continue
    pt = r['post_tokens_detail'][0]
    post_tok_examples.append({
        's2': pt['s2'],
        'adv': r['norm'],
        'word': pt['token'],
        'top_pred': pt['top_pred'],
        'top_prob': pt['top_prob'],
        'author': r['author'],
        'title': r['title'],
        'context': r['context_before'],
    })

post_tok_examples.sort(key=lambda x: -x['s2'])
for ex in post_tok_examples[:20]:
    ctx = ex['context'].replace('\n', '↵').strip()[-45:]
    print(f'{ex["s2"]:>+7.2f} | {ex["adv"]:>6} | {ex["word"]:<16} | '
          f'{ex["top_pred"]:>12} | {ex["top_prob"]:>8.4f} | '
          f'{ex["author"]} — …{ctx}')


# ── 6. ERA × ADVERSATIVE DENSITY ─────────────────────────────────────────────

print('\n\n## 6. Adversative Density and Post-Turn S₂ by Era\n')
print(f'{"Era":<22} {"n poems":>8} {"adv/poem":>9} {"post-adv S₂":>12} {"baseline S₂":>12}')
print('-' * 68)

era_adv = defaultdict(list)  # era → adversative records
era_poems = defaultdict(list)

for r in adversative_records:
    era_adv[r['era']].append(r)

for poem in corpus:
    meta = poem['metadata']
    if meta.get('language', 'en') != 'en':
        continue
    if meta.get('era') == 'control':
        continue
    era_poems[meta.get('era', '?')].append(poem['summary']['avg_s2'])

era_rows = []
for era, recs in era_adv.items():
    n_poems = len(era_poems[era])
    if n_poems < 2:
        continue
    adv_per_poem = len(recs) / n_poems
    post_s2_vals = [mean(r['post_s2']) for r in recs if r['post_s2']]
    base_s2 = mean(era_poems[era])
    era_rows.append((era, n_poems, adv_per_poem, mean(post_s2_vals), base_s2))

era_rows.sort(key=lambda x: -x[2])  # sort by adversative density
for row in era_rows:
    era, np, apk, post_s2, base = row
    print(f'{era:<22} {np:>8} {apk:>9.2f} {post_s2:>+12.3f} {base:>+12.3f}')


# ── 7. WHAT DOES GPT-2 EXPECT AFTER "BUT"? ──────────────────────────────────

print('\n\n## 7. Alternatives Analysis: What Does GPT-2 Expect After Adversatives?\n')

for conj in ['but', 'yet', 'though']:
    recs = [r for r in adversative_records if r['norm'] == conj and r['alternatives_at_adv']]
    if len(recs) < 3:
        continue
    # Collect what models predict would come after this conjunction
    # (i.e., the alternatives at position of the conjunction itself)
    alt_counter = defaultdict(float)
    for r in recs:
        for alt in r['alternatives_at_adv'][:5]:
            alt_counter[alt.get('token', '?').strip()] += alt.get('prob', 0)

    top_alts = sorted(alt_counter.items(), key=lambda x: -x[1])[:8]
    print(f'After "{conj}" — GPT-2 most expected to see the conjunction itself be ({len(recs)} occurrences):')
    # Actually let's show what GPT-2 expected INSTEAD of this adversative
    print(f'  (GPT-2 expected these words instead of "{conj}"):')
    for tok, prob in top_alts:
        print(f'    "{tok}" — avg prob {prob/len(recs):.4f}')
    print()


# ── 8. POET-LEVEL ADVERSATIVE FINGERPRINTS ───────────────────────────────────

print('\n\n## 8. Poet-Level Adversative Fingerprints\n')
print(f'{"Author":<25} {"adv count":>10} {"post-adv S₂":>12} {"corpus S₂":>11}')
print('-' * 62)

poet_recs = defaultdict(list)
for r in adversative_records:
    poet_recs[r['author']].append(r)

poet_corpus_s2 = defaultdict(list)
for poem in corpus:
    meta = poem['metadata']
    if meta.get('language', 'en') == 'en' and meta.get('era') != 'control':
        poet_corpus_s2[meta['author']].append(poem['summary']['avg_s2'])

poet_rows = []
for author, recs in poet_recs.items():
    if len(recs) < 4:
        continue
    post_s2 = [mean(r['post_s2']) for r in recs if r['post_s2']]
    base_s2 = mean(poet_corpus_s2.get(author, [0]))
    poet_rows.append((author, len(recs), mean(post_s2), base_s2))

poet_rows.sort(key=lambda x: -x[2])
for row in poet_rows:
    author, count, post_s2, base = row
    print(f'{author:<25} {count:>10} {post_s2:>+12.3f} {base:>+11.3f}')


print('\n\n[Done]')
