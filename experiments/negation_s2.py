"""
Negation and S2: When Poets Say "Not"

Research question: How do negation tokens and the words that follow them
behave informationally? When a poet says "not X", they invoke X while denying it.
Does the negated term show elevated S2 (unexpected given the negation context)?

Method: Identify negation tokens in the corpus, analyze S2 for the negation
token and its immediate successor.
"""

import json
import re
from collections import defaultdict

NEGATION_TOKENS = {
    'not', 'no', 'never', 'nothing', 'none', 'neither', 'nor',
    'nobody', 'nowhere', 'never', 'without', 'beyond', 'un', 'dis',
    'cannot', "can't", "won't", "don't", "doesn't", "didn't", "isn't",
    "aren't", "wasn't", "weren't", "haven't", "hasn't", "hadn't",
    "shouldn't", "wouldn't", "couldn't", "mightn't",
}

# Stricter set for clear syntactic negation
CORE_NEG = {'not', 'no', 'never', 'nothing', 'none', 'neither', 'nor',
             'nobody', 'nowhere', 'without'}


def normalize(token: str) -> str:
    return token.strip().lower().lstrip('Ġ').lstrip(' ')


def load_results(path='results/corpus_results.json'):
    with open(path) as f:
        return json.load(f)


def find_negation_windows(tokens, window=2):
    """
    For each negation token, return a record with:
      - the negation token and its S2
      - the S2 of the next 1-2 tokens
      - metadata for grouping
    """
    records = []
    for i, tok in enumerate(tokens):
        norm = normalize(tok['token'])
        if norm in CORE_NEG:
            record = {
                'neg_token': tok['token'].strip(),
                'neg_s2': tok['s2'],
                'neg_surprisal': tok['surprisal'],
                'neg_entropy': tok['entropy'],
                'neg_pos': tok['position'],
                'post_tokens': [],
                'alternatives_at_neg': tok.get('alternatives', [])[:5],
                'context': tok.get('context_before', ''),
            }
            for j in range(1, window + 1):
                if i + j < len(tokens):
                    next_tok = tokens[i + j]
                    record['post_tokens'].append({
                        'token': next_tok['token'].strip(),
                        's2': next_tok['s2'],
                        'surprisal': next_tok['surprisal'],
                        'entropy': next_tok['entropy'],
                        'alternatives': next_tok.get('alternatives', [])[:5],
                    })
            records.append(record)
    return records


def analyze(results):
    all_s2 = []
    neg_records = []
    poet_stats = defaultdict(lambda: {'neg_count': 0, 'post_neg_s2': [], 'baseline_s2': []})

    for poem in results:
        meta = poem['metadata']
        tokens = poem['tokens']
        author = meta['author']

        # Baseline: all tokens in this poem
        poem_s2 = [t['s2'] for t in tokens]
        all_s2.extend(poem_s2)
        poet_stats[author]['baseline_s2'].extend(poem_s2)

        # Negation windows
        negs = find_negation_windows(tokens)
        for neg in negs:
            neg['poem_title'] = meta['title']
            neg['author'] = author
            neg['era'] = meta['era']
            neg['poem_baseline_s2'] = sum(poem_s2) / len(poem_s2) if poem_s2 else 0
            neg_records.append(neg)

            poet_stats[author]['neg_count'] += 1
            if neg['post_tokens']:
                post_s2 = neg['post_tokens'][0]['s2']
                poet_stats[author]['post_neg_s2'].append(post_s2)

    global_mean_s2 = sum(all_s2) / len(all_s2) if all_s2 else 0
    return neg_records, poet_stats, global_mean_s2, all_s2


def print_report(neg_records, poet_stats, global_mean, all_s2):
    print(f"\n{'='*60}")
    print("NEGATION AND S2 — ANALYSIS REPORT")
    print(f"{'='*60}")
    print(f"  Total poems analyzed: {len(set(r['poem_title'] for r in neg_records))}")
    print(f"  Total negation tokens found: {len(neg_records)}")
    print(f"  Global mean S2 (all tokens): {global_mean:.4f}")

    # S2 of negation tokens themselves
    neg_s2_vals = [r['neg_s2'] for r in neg_records]
    mean_neg_s2 = sum(neg_s2_vals) / len(neg_s2_vals) if neg_s2_vals else 0

    # S2 of the token immediately after negation
    post1_s2_vals = [r['post_tokens'][0]['s2'] for r in neg_records if r['post_tokens']]
    mean_post1_s2 = sum(post1_s2_vals) / len(post1_s2_vals) if post1_s2_vals else 0

    print(f"\n--- S2 VALUES ---")
    print(f"  Mean S2 (negation tokens):     {mean_neg_s2:.4f}  (vs global {global_mean:.4f})")
    print(f"  Mean S2 (token after negation): {mean_post1_s2:.4f}  (vs global {global_mean:.4f})")

    # Break down by negation type
    print(f"\n--- BY NEGATION WORD ---")
    neg_by_word = defaultdict(list)
    post_by_word = defaultdict(list)
    for r in neg_records:
        w = r['neg_token'].lower()
        neg_by_word[w].append(r['neg_s2'])
        if r['post_tokens']:
            post_by_word[w].append(r['post_tokens'][0]['s2'])

    rows = []
    for w in sorted(neg_by_word, key=lambda x: -len(neg_by_word[x])):
        n = len(neg_by_word[w])
        ms2 = sum(neg_by_word[w]) / n
        post_n = len(post_by_word[w])
        mpost = sum(post_by_word[w]) / post_n if post_n else float('nan')
        rows.append((w, n, ms2, mpost))

    print(f"  {'Word':<14} {'Count':>6} {'Own S2':>8} {'Post S2':>8}")
    print(f"  {'-'*40}")
    for w, n, ms2, mpost in rows[:15]:
        print(f"  {w:<14} {n:>6} {ms2:>8.3f} {mpost:>8.3f}")

    # Top "negation premium" cases: where post-negation S2 far exceeds baseline
    print(f"\n--- TOP 10 CASES: HIGHEST POST-NEGATION S2 ---")
    records_with_post = [r for r in neg_records if r['post_tokens']]
    records_with_post.sort(key=lambda r: r['post_tokens'][0]['s2'], reverse=True)
    print(f"  {'Negation':<12} {'Follows':<20} {'Post S2':>8} {'Poem'}")
    print(f"  {'-'*70}")
    for r in records_with_post[:10]:
        post = r['post_tokens'][0]
        title = r['poem_title'][:30]
        print(f"  {r['neg_token']:<12} {post['token']:<20} {post['s2']:>8.3f}  {title} ({r['author'].split()[-1]})")

    # Cases where GPT-2's top prediction after negation was something different
    print(f"\n--- NEGATION OVERRIDES: WHAT GPT-2 PREDICTED VS WHAT THE POET CHOSE ---")
    print(f"  (at the token following the negation)")
    override_rows = []
    for r in records_with_post:
        post = r['post_tokens'][0]
        alts = post.get('alternatives', [])
        if alts:
            gpt2_top = alts[0]['token'].strip()
            poet_chose = post['token'].strip()
            if poet_chose.lower() != gpt2_top.lower():
                override_rows.append({
                    'neg': r['neg_token'],
                    'gpt2_predicted': gpt2_top,
                    'poet_wrote': poet_chose,
                    'post_s2': post['s2'],
                    'poem': r['poem_title'],
                    'author': r['author'],
                    'context': r['context'],
                })
    override_rows.sort(key=lambda x: x['post_s2'], reverse=True)
    print(f"  {'Context':<20} {'Neg':<8} GPT-2 predicted → Poet wrote  (S2)")
    print(f"  {'-'*70}")
    for row in override_rows[:10]:
        ctx = (row['context'][-15:] if row['context'] else '').strip()
        print(f"  '...{ctx:<17}' {row['neg']:<8} '{row['gpt2_predicted']}' → '{row['poet_wrote']}'  ({row['post_s2']:.2f})")

    # Poet negation frequency and post-negation S2
    print(f"\n--- POET PROFILES: NEGATION FREQUENCY & POST-NEGATION S2 ---")
    poet_rows = []
    for author, stats in poet_stats.items():
        if stats['neg_count'] >= 2:
            base_mean = sum(stats['baseline_s2']) / len(stats['baseline_s2']) if stats['baseline_s2'] else 0
            post_mean = sum(stats['post_neg_s2']) / len(stats['post_neg_s2']) if stats['post_neg_s2'] else float('nan')
            neg_rate = stats['neg_count'] / max(len(stats['baseline_s2']), 1) * 100
            poet_rows.append((author, stats['neg_count'], neg_rate, base_mean, post_mean))
    poet_rows.sort(key=lambda x: -x[2])
    print(f"  {'Author':<25} {'Negs':>5} {'Rate%':>7} {'Base S2':>8} {'PostNeg S2':>10}")
    print(f"  {'-'*60}")
    for author, n, rate, base, post in poet_rows[:15]:
        print(f"  {author:<25} {n:>5} {rate:>7.2f} {base:>8.3f} {post:>10.3f}")

    return {
        'global_mean': global_mean,
        'mean_neg_s2': mean_neg_s2,
        'mean_post1_s2': mean_post1_s2,
        'total_negation_tokens': len(neg_records),
        'top_high_post_neg': records_with_post[:10],
        'top_overrides': override_rows[:10],
        'by_word_rows': rows,
        'poet_rows': poet_rows,
    }


if __name__ == '__main__':
    results = load_results()
    neg_records, poet_stats, global_mean, all_s2 = analyze(results)
    stats = print_report(neg_records, poet_stats, global_mean, all_s2)
    print(f"\n{'='*60}")
    print("Done.")
