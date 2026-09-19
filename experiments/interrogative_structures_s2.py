"""
Interrogative Structures in Poetry: The S₂ Profile of Questions

Research question: When poets ask questions, how does the information-theoretic
profile change? Poetic questions range from genuine inquiry (Keats: "What can I do
to drive away / Remembrance from mine eyes?") to rhetorical assertion (Blake: "Did
he who made the Lamb make thee?") to existential suspension (Eliot: "Do I dare
disturb the universe?"). Do these interrogative structures show distinctive S₂ patterns?

Hypotheses:
  H1. Wh-question words (what, who, where, when, why, how) have higher entropy
      than their non-question-word homonyms — GPT-2 is uncertain what follows.
  H2. The token immediately after a wh-question word has elevated S₂ — the poet
      makes an unexpected choice in the semantic field opened by the question.
  H3. Questions cluster at poem endings (rhetorical closure) vs poem openings
      (dramatic entrance). The positional pattern differs by era.
  H4. The "?" token itself has very high entropy but low S₂ — it is expected
      at sentence end, but the question mark raises maximum uncertainty about
      what follows next.
  H5. Poems with more questions per token have higher overall S₂ — questions
      are an uncertainty-generating device.

Works from precomputed corpus_results.json — no GPU needed.
"""

import json
import re
from collections import defaultdict
import statistics

# ── Constants ────────────────────────────────────────────────────────────────

WH_WORDS = {'what', 'who', 'whom', 'whose', 'which', 'where', 'when', 'why', 'how'}

# Tokens that often introduce yes/no questions
AUX_QUESTION_STARTERS = {
    'is', 'are', 'was', 'were', 'do', 'does', 'did', 'have', 'has', 'had',
    'will', 'would', 'shall', 'should', 'can', 'could', 'may', 'might', 'must',
    'am', 'be'
}


def normalize(token: str) -> str:
    return token.strip().lower().lstrip('Ġ').lstrip('Ġ').lstrip(' ')


def mean(xs):
    return sum(xs) / len(xs) if xs else float('nan')


def std(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def is_nan(x):
    try:
        return x != x
    except Exception:
        return False


# ── Load corpus ───────────────────────────────────────────────────────────────

with open('results/corpus_results.json') as f:
    corpus = json.load(f)


# ── Analysis functions ────────────────────────────────────────────────────────

def find_question_spans(tokens):
    """
    Identify question sentences by finding "?" tokens and working backward
    to the previous sentence boundary.
    Returns list of dicts with question span data.
    """
    sentences = []
    current_start = 0

    for i, tok in enumerate(tokens):
        raw = tok['token']
        norm = normalize(raw)

        if '?' in raw or norm in {'.', '!', '?', '...', '--'}:
            if '?' in raw:
                sentences.append({
                    'type': 'question',
                    'start': current_start,
                    'end': i,
                    'tokens': tokens[current_start:i + 1]
                })
            else:
                sentences.append({
                    'type': 'statement',
                    'start': current_start,
                    'end': i,
                    'tokens': tokens[current_start:i + 1]
                })
            current_start = i + 1

    # Remainder (no final punctuation)
    if current_start < len(tokens):
        sentences.append({
            'type': 'statement',
            'start': current_start,
            'end': len(tokens) - 1,
            'tokens': tokens[current_start:]
        })

    return sentences


def classify_question(sentence_tokens):
    """
    Classify a question as 'wh' (open) or 'yn' (yes/no/closed) or 'other'.
    """
    # Look at the first few non-whitespace tokens
    for tok in sentence_tokens[:5]:
        norm = normalize(tok['token'])
        if norm in WH_WORDS:
            return 'wh', norm
    for tok in sentence_tokens[:3]:
        norm = normalize(tok['token'])
        if norm in AUX_QUESTION_STARTERS:
            return 'yn', norm
    return 'other', None


def get_wh_word_records(tokens):
    """
    For each wh-word in question context, get S2 context.
    Also captures wh-words NOT in question context to compare.
    """
    records = []
    for i, tok in enumerate(tokens):
        norm = normalize(tok['token'])
        if norm in WH_WORDS:
            # Is this in a question? Look ahead for "?"
            is_question = False
            for j in range(i, min(i + 20, len(tokens))):
                if '?' in tokens[j]['token']:
                    is_question = True
                    break
                if any(p in tokens[j]['token'] for p in ['.', '!', '\n\n']):
                    break

            record = {
                'wh_word': norm,
                'wh_token': tok['token'].strip(),
                'wh_s2': tok['s2'],
                'wh_surprisal': tok['surprisal'],
                'wh_entropy': tok['entropy'],
                'wh_pos': i,
                'in_question': is_question,
                'post1': None,
                'post2': None,
                'pre1': None,
            }

            if i + 1 < len(tokens):
                record['post1'] = {
                    'token': tokens[i + 1]['token'].strip(),
                    's2': tokens[i + 1]['s2'],
                    'surprisal': tokens[i + 1]['surprisal'],
                    'entropy': tokens[i + 1]['entropy'],
                }
            if i + 2 < len(tokens):
                record['post2'] = {
                    'token': tokens[i + 2]['token'].strip(),
                    's2': tokens[i + 2]['s2'],
                    'surprisal': tokens[i + 2]['surprisal'],
                    'entropy': tokens[i + 2]['entropy'],
                }
            if i > 0:
                record['pre1'] = {
                    'token': tokens[i - 1]['token'].strip(),
                    's2': tokens[i - 1]['s2'],
                }

            records.append(record)
    return records


def get_question_mark_records(tokens):
    """Get S2 data for '?' tokens."""
    records = []
    for i, tok in enumerate(tokens):
        if '?' in tok['token'] and len(tok['token'].strip()) <= 2:
            records.append({
                's2': tok['s2'],
                'surprisal': tok['surprisal'],
                'entropy': tok['entropy'],
                'pos': i,
                'total_tokens': len(tokens),
                'rel_pos': i / len(tokens) if tokens else 0,
            })
    return records


# ── Main analysis ─────────────────────────────────────────────────────────────

poem_question_stats = []
all_wh_records = []
all_qmark_records = []
question_sentence_s2 = []
statement_sentence_s2 = []
era_question_density = defaultdict(list)
author_question_stats = defaultdict(lambda: {
    'total_tokens': 0, 'question_tokens': 0, 'wh_count': 0,
    'question_s2': [], 'baseline_s2': []
})

question_examples = []  # For qualitative analysis

for poem in corpus:
    meta = poem['metadata']
    tokens = poem['tokens']

    if meta.get('language', 'en') != 'en':
        continue
    if meta.get('era') == 'control':
        continue
    if not tokens:
        continue

    author = meta['author']
    era = meta['era']
    title = meta['title']

    baseline_s2 = [t['s2'] for t in tokens]
    mean_baseline = mean(baseline_s2)

    # Find question sentences
    sentences = find_question_spans(tokens)
    questions = [s for s in sentences if s['type'] == 'question']
    non_questions = [s for s in sentences if s['type'] != 'question']

    # S2 by sentence type
    q_s2_all = []
    nq_s2_all = []
    for s in questions:
        s_s2 = [t['s2'] for t in s['tokens']]
        q_s2_all.extend(s_s2)
        question_sentence_s2.extend(s_s2)
    for s in non_questions:
        s_s2 = [t['s2'] for t in s['tokens']]
        nq_s2_all.extend(s_s2)
        statement_sentence_s2.extend(s_s2)

    # Classify questions
    q_types = defaultdict(int)
    for q in questions:
        qtype, _ = classify_question(q['tokens'])
        q_types[qtype] += 1

        # Find examples
        q_text = ''.join(t['token'] for t in q['tokens']).strip()
        if q_text and len(q_text) > 5:
            q_s2_vals = [t['s2'] for t in q['tokens']]
            question_examples.append({
                'text': q_text[:200],
                'author': author,
                'title': title,
                'era': era,
                'mean_s2': mean(q_s2_vals),
                'type': qtype,
                'rel_pos': q['start'] / len(tokens),
            })

    # Question density for this poem
    n_questions = len(questions)
    question_density = n_questions / len(tokens) * 100 if tokens else 0

    # Wh-word records
    wh_records = get_wh_word_records(tokens)
    for r in wh_records:
        r['poem_title'] = title
        r['author'] = author
        r['era'] = era
        r['poem_mean_s2'] = mean_baseline
    all_wh_records.extend(wh_records)

    # Question mark records
    qmark_records = get_question_mark_records(tokens)
    for r in qmark_records:
        r['author'] = author
        r['era'] = era
    all_qmark_records.extend(qmark_records)

    # Per-poem stats
    poem_question_stats.append({
        'title': title,
        'author': author,
        'era': era,
        'n_tokens': len(tokens),
        'n_questions': n_questions,
        'question_density': question_density,
        'n_wh': sum(1 for r in wh_records if r['in_question']),
        'n_yn': q_types.get('yn', 0),
        'mean_baseline_s2': mean_baseline,
        'mean_question_s2': mean(q_s2_all),
        'mean_nonquestion_s2': mean(nq_s2_all),
        'q_s2_lift': mean(q_s2_all) - mean(nq_s2_all) if q_s2_all and nq_s2_all else float('nan'),
    })

    # Era and author stats
    if n_questions > 0:
        era_question_density[era].append(question_density)

    author_question_stats[author]['total_tokens'] += len(tokens)
    author_question_stats[author]['baseline_s2'].extend(baseline_s2)
    if q_s2_all:
        author_question_stats[author]['question_s2'].extend(q_s2_all)
    author_question_stats[author]['wh_count'] += sum(1 for r in wh_records if r['in_question'])


# ── Print report ───────────────────────────────────────────────────────────────

print("\n" + "=" * 65)
print("INTERROGATIVE STRUCTURES IN POETRY — S₂ ANALYSIS REPORT")
print("=" * 65)

total_poems = len(poem_question_stats)
poems_with_questions = sum(1 for p in poem_question_stats if p['n_questions'] > 0)
total_questions = sum(p['n_questions'] for p in poem_question_stats)
total_wh = sum(1 for r in all_wh_records if r['in_question'])
total_wh_nonquestion = sum(1 for r in all_wh_records if not r['in_question'])

print(f"\n  Poems analyzed (English, non-control): {total_poems}")
print(f"  Poems containing at least 1 question: {poems_with_questions} ({100*poems_with_questions//total_poems}%)")
print(f"  Total question sentences found: {total_questions}")
print(f"  Wh-words in question context: {total_wh}")
print(f"  Wh-words in non-question context (relative clauses etc.): {total_wh_nonquestion}")

# ── H1: Entropy at wh-words ───────────────────────────────────────────────────
print("\n\n── H1: Entropy at Wh-words in vs. out of questions ──────────────────")

wh_in_q_entropy = [r['wh_entropy'] for r in all_wh_records if r['in_question']]
wh_out_q_entropy = [r['wh_entropy'] for r in all_wh_records if not r['in_question']]
wh_in_q_s2 = [r['wh_s2'] for r in all_wh_records if r['in_question']]
wh_out_q_s2 = [r['wh_s2'] for r in all_wh_records if not r['in_question']]

print(f"\n  Wh-word entropy IN questions:      {mean(wh_in_q_entropy):.3f} (n={len(wh_in_q_entropy)})")
print(f"  Wh-word entropy NOT in questions:  {mean(wh_out_q_entropy):.3f} (n={len(wh_out_q_entropy)})")
print(f"  Wh-word S₂ IN questions:           {mean(wh_in_q_s2):.3f}")
print(f"  Wh-word S₂ NOT in questions:       {mean(wh_out_q_s2):.3f}")

# ── H2: Post-wh-word S₂ ──────────────────────────────────────────────────────
print("\n\n── H2: Post-wh-word S₂ (what follows the question word?) ────────────")

post1_in_q = [r['post1']['s2'] for r in all_wh_records if r['in_question'] and r['post1']]
post1_out_q = [r['post1']['s2'] for r in all_wh_records if not r['in_question'] and r['post1']]

print(f"\n  S₂ of token after wh-word (in question):     {mean(post1_in_q):.3f} (n={len(post1_in_q)})")
print(f"  S₂ of token after wh-word (non-question):    {mean(post1_out_q):.3f} (n={len(post1_out_q)})")

# Breakdown by wh-word type
print("\n  S₂ by question word (in question context):")
by_wh = defaultdict(list)
for r in all_wh_records:
    if r['in_question']:
        by_wh[r['wh_word']].append(r['wh_s2'])

for wh, vals in sorted(by_wh.items(), key=lambda x: -mean(x[1])):
    if len(vals) >= 2:
        print(f"    {wh:8s}: avg S₂ = {mean(vals):+.3f}  (n={len(vals)}, std={std(vals):.3f})")

# ── H3: Positional distribution of questions ─────────────────────────────────
print("\n\n── H3: Where do questions appear in poems? ───────────────────────────")

early_qs = [e for e in question_examples if e['rel_pos'] < 0.25]
mid_qs = [e for e in question_examples if 0.25 <= e['rel_pos'] < 0.75]
late_qs = [e for e in question_examples if e['rel_pos'] >= 0.75]

print(f"\n  Questions in opening quarter (rel_pos < 0.25):  {len(early_qs)} ({100*len(early_qs)//max(len(question_examples),1)}%)")
print(f"  Questions in middle half (0.25 ≤ rel_pos < 0.75): {len(mid_qs)} ({100*len(mid_qs)//max(len(question_examples),1)}%)")
print(f"  Questions in closing quarter (rel_pos ≥ 0.75): {len(late_qs)} ({100*len(late_qs)//max(len(question_examples),1)}%)")
print(f"\n  Mean S₂ — opening questions:  {mean([e['mean_s2'] for e in early_qs]):.3f}")
print(f"  Mean S₂ — middle questions:   {mean([e['mean_s2'] for e in mid_qs]):.3f}")
print(f"  Mean S₂ — closing questions:  {mean([e['mean_s2'] for e in late_qs]):.3f}")

# ── H4: Question mark entropy ─────────────────────────────────────────────────
print("\n\n── H4: The '?' token — entropy and S₂ ───────────────────────────────")

qmark_entropy = [r['entropy'] for r in all_qmark_records]
qmark_s2 = [r['s2'] for r in all_qmark_records]

print(f"\n  Number of '?' tokens found: {len(all_qmark_records)}")
print(f"  Avg entropy at '?':         {mean(qmark_entropy):.3f}")
print(f"  Avg S₂ at '?':              {mean(qmark_s2):.3f}")
print(f"  Avg surprisal at '?':       {mean([r['surprisal'] for r in all_qmark_records]):.3f}")

# ── H5: Question-heavy poems and overall S₂ ──────────────────────────────────
print("\n\n── H5: Question density vs. overall poem S₂ ─────────────────────────")

q_s2_global = mean(question_sentence_s2)
nq_s2_global = mean(statement_sentence_s2)

print(f"\n  Global avg S₂ in QUESTION sentences:     {q_s2_global:.4f}")
print(f"  Global avg S₂ in NON-QUESTION sentences: {nq_s2_global:.4f}")
print(f"  Lift from questions:                      {q_s2_global - nq_s2_global:+.4f}")

# ── Era breakdown: question usage ─────────────────────────────────────────────
print("\n\n── Era Breakdown: Question Density in Poetry ─────────────────────────")

era_q_lift = defaultdict(list)
for p in poem_question_stats:
    if not is_nan(p['q_s2_lift']):
        era_q_lift[p['era']].append(p['q_s2_lift'])

era_rows = []
for era, densities in sorted(era_question_density.items(), key=lambda x: -mean(x[1])):
    lifts = era_q_lift.get(era, [])
    era_rows.append((era, mean(densities), mean(lifts) if lifts else float('nan'), len(densities)))

print(f"\n  {'Era':25s} {'Avg Q-density':>14s} {'S₂ lift in Qs':>14s} {'n poems':>8s}")
print(f"  {'-'*25} {'-'*14} {'-'*14} {'-'*8}")
for era, density, lift, n in sorted(era_rows, key=lambda x: -x[1]):
    lift_str = f"{lift:+.3f}" if not is_nan(lift) else "  n/a"
    print(f"  {era:25s} {density:14.2f} {lift_str:>14s} {n:>8d}")

# ── Top question-using poets ──────────────────────────────────────────────────
print("\n\n── Top Question-Using Poets ──────────────────────────────────────────")

author_rows = []
for author, stats in author_question_stats.items():
    if stats['wh_count'] > 0 and stats['total_tokens'] > 50:
        wh_density = stats['wh_count'] / stats['total_tokens'] * 100
        q_s2 = mean(stats['question_s2']) if stats['question_s2'] else float('nan')
        base_s2 = mean(stats['baseline_s2']) if stats['baseline_s2'] else float('nan')
        author_rows.append((author, wh_density, stats['wh_count'], q_s2, base_s2))

print(f"\n  {'Author':30s} {'Wh/100tok':>10s} {'Wh count':>10s} {'Q S₂':>8s} {'Base S₂':>8s}")
print(f"  {'-'*30} {'-'*10} {'-'*10} {'-'*8} {'-'*8}")
for author, density, wh_count, q_s2, base in sorted(author_rows, key=lambda x: -x[1])[:15]:
    q_s2_str = f"{q_s2:.3f}" if not is_nan(q_s2) else "  n/a"
    print(f"  {author:30s} {density:10.2f} {wh_count:10d} {q_s2_str:>8s} {base:.3f}")

# ── Highest-S₂ questions ──────────────────────────────────────────────────────
print("\n\n── Highest-S₂ Question Sentences ────────────────────────────────────")

top_qs = sorted([e for e in question_examples if not is_nan(e['mean_s2'])],
                key=lambda x: -x['mean_s2'])[:10]

for i, q in enumerate(top_qs, 1):
    print(f"\n  {i}. [{q['author']} — \"{q['title']}\"] (S₂={q['mean_s2']:.3f}, pos={q['rel_pos']:.2f})")
    print(f"     \"{q['text'][:120]}\"")

# ── Lowest-S₂ questions (most expected questions) ────────────────────────────
print("\n\n── Lowest-S₂ Question Sentences (Most Expected) ─────────────────────")

low_qs = sorted([e for e in question_examples if not is_nan(e['mean_s2']) and len(e['text']) > 10],
                key=lambda x: x['mean_s2'])[:5]
for i, q in enumerate(low_qs, 1):
    print(f"\n  {i}. [{q['author']} — \"{q['title']}\"] (S₂={q['mean_s2']:.3f})")
    print(f"     \"{q['text'][:120]}\"")

print("\n\n" + "=" * 65)
print("END OF REPORT")
print("=" * 65 + "\n")
