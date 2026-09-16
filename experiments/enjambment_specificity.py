"""
Enjambment Specificity: What does the poet write when GPT-2 predicted a newline?

This experiment characterizes the *type* of token that appears at confidence traps
where GPT-2's top prediction was a newline ("\n"). When a poet continues a line
against the model's line-break expectation, what kind of word do they use?

Builds on: confidence_trap_analysis.md, enjambment_vs_s2.md
"""

import json
import re
from collections import defaultdict

CONJUNCTIONS = {
    'and', 'but', 'or', 'nor', 'yet', 'for', 'so', 'both',
    'either', 'neither', 'not', 'although', 'though', 'while',
    'whereas', 'since', 'because', 'if', 'unless', 'until',
    'when', 'where', 'which', 'who', 'that', 'as', 'than',
}

PREPOSITIONS = {
    'in', 'on', 'at', 'with', 'from', 'by', 'through', 'into',
    'over', 'under', 'above', 'below', 'between', 'among', 'along',
    'across', 'around', 'behind', 'before', 'after', 'against',
    'within', 'without', 'beyond', 'beside', 'beneath', 'toward',
    'towards', 'upon', 'of', 'to', 'off', 'out', 'up', 'down',
    'during', 'throughout', 'despite', 'about', 'like', 'near',
}

DETERMINERS = {
    'the', 'a', 'an', 'this', 'that', 'these', 'those', 'my', 'your',
    'his', 'her', 'its', 'our', 'their', 'no', 'each', 'every',
    'some', 'any', 'all', 'both', 'half', 'such', 'what', 'whatever',
}

PRONOUNS = {
    'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
    'her', 'us', 'them', 'who', 'whom', 'what', 'which', 'myself',
    'yourself', 'himself', 'herself', 'itself', 'ourselves', 'themselves',
}

COMMON_VERBS = {
    'is', 'are', 'was', 'were', 'be', 'been', 'being', 'am',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'shall', 'should', 'may', 'might', 'must', 'can', 'could',
    'seem', 'seems', 'seemed', 'become', 'becomes', 'became',
    'know', 'knew', 'say', 'said', 'see', 'saw', 'come', 'came',
    'go', 'went', 'make', 'made', 'take', 'took', 'think', 'thought',
    'feel', 'felt', 'find', 'found', 'give', 'gave', 'bring',
    'rise', 'fall', 'hold', 'stand', 'sit', 'lie', 'run', 'turn',
    'move', 'keep', 'let', 'leave', 'begin', 'start', 'end',
    'hear', 'look', 'speak', 'speak', 'speaks', 'fall', 'falls',
}

def classify_token(tok):
    """Classify a token by its grammatical/functional type."""
    t = tok.strip().lower().lstrip("'")

    if not t or t in {'.', ',', ';', ':', '!', '?', '-', '—', '...', '"', "'"}:
        return 'punctuation'

    # Detect em-dash or hyphen continuations
    if t in {'-', '—', '–'}:
        return 'dash_continuation'

    if t in PRONOUNS:
        return 'pronoun'
    if t in CONJUNCTIONS:
        return 'conjunction'
    if t in PREPOSITIONS:
        return 'preposition'
    if t in DETERMINERS:
        return 'determiner'
    if t in COMMON_VERBS:
        return 'auxiliary/verb'

    # Likely content word if not in any function set
    # Heuristic: starts with capital after stripping → proper noun
    if tok.strip() and tok.strip()[0].isupper():
        return 'proper_noun'

    return 'content_word'


def analyze_enjambment_specificity(data, newline_prob_threshold=0.20):
    """
    Find all tokens where newline was a top predicted token (prob > threshold),
    but the poet wrote something else (not a newline). Classify the chosen token.

    Also find positions where a newline was the top-1 prediction (stricter analysis).
    """
    traps_all = []   # newline in top-10 with prob > threshold
    traps_top1 = []  # newline was the #1 prediction

    for poem in data:
        meta = poem['metadata']
        if meta.get('language', 'en') != 'en':
            continue
        if meta.get('era') == 'control':
            continue

        tokens = poem['tokens']
        for tok in tokens:
            if tok['token'].strip() == '' or tok['token'] == '\n':
                continue  # skip actual newlines

            alts = tok.get('alternatives', [])
            if not alts:
                continue

            # Find newline in alternatives
            newline_prob = 0.0
            newline_rank = None
            for rank, alt in enumerate(alts):
                if alt['token'] == '\n':
                    newline_prob = alt['prob']
                    newline_rank = rank + 1  # 1-indexed
                    break

            if newline_prob < newline_prob_threshold:
                continue

            # This is an enjambment trap
            token_type = classify_token(tok['token'])
            record = {
                'title': meta['title'],
                'author': meta['author'],
                'era': meta['era'],
                'token': tok['token'],
                'token_type': token_type,
                's2': tok['s2'],
                'surprisal': tok['surprisal'],
                'entropy': tok['entropy'],
                'newline_prob': newline_prob,
                'newline_rank': newline_rank,
                'context': tok.get('context_before', ''),
            }
            traps_all.append(record)

            if newline_rank == 1:
                traps_top1.append(record)

    return traps_all, traps_top1


def summarize_by_type(traps):
    """Group traps by token_type and compute statistics."""
    by_type = defaultdict(list)
    for t in traps:
        by_type[t['token_type']].append(t)

    summaries = []
    for ttype, items in by_type.items():
        s2_vals = [i['s2'] for i in items]
        newline_probs = [i['newline_prob'] for i in items]
        avg_s2 = sum(s2_vals) / len(s2_vals)
        avg_conf = sum(newline_probs) / len(newline_probs)

        # Find examples
        top_s2 = sorted(items, key=lambda x: -x['s2'])[:3]
        examples = [(i['token'].strip(), i['s2'], i['author'], i['title'])
                    for i in top_s2]

        summaries.append({
            'type': ttype,
            'count': len(items),
            'avg_s2': avg_s2,
            'avg_newline_confidence': avg_conf,
            'examples': examples,
        })

    return sorted(summaries, key=lambda x: -x['count'])


def era_breakdown(traps):
    """Show trap type distribution per era."""
    by_era = defaultdict(lambda: defaultdict(int))
    for t in traps:
        by_era[t['era']][t['token_type']] += 1

    result = {}
    for era, types in by_era.items():
        total = sum(types.values())
        result[era] = {
            'total': total,
            'types': {k: (v, round(100*v/total, 1)) for k, v in
                      sorted(types.items(), key=lambda x: -x[1])}
        }
    return result


def highest_confidence_traps(traps, n=20):
    """Most extreme cases: highest newline_prob at time of enjambment."""
    return sorted(traps, key=lambda x: -x['newline_prob'])[:n]


if __name__ == '__main__':
    with open('/home/user/s2lab/results/corpus_results.json') as f:
        data = json.load(f)

    print("Analyzing enjambment specificity...")

    traps_all, traps_top1 = analyze_enjambment_specificity(data, newline_prob_threshold=0.15)

    print(f"\nTotal enjambment traps (newline prob > 15%): {len(traps_all)}")
    print(f"Top-1 enjambment traps (newline was #1 prediction): {len(traps_top1)}")

    # Summary by type
    print("\n=== DISTRIBUTION BY CONTINUATION TYPE (all traps, newline prob > 15%) ===")
    summaries = summarize_by_type(traps_all)
    total = len(traps_all)
    print(f"{'Type':<20} {'N':>5} {'%':>6} {'Avg S2':>8} {'Avg NL conf':>12}")
    print("-" * 60)
    for s in summaries:
        pct = 100 * s['count'] / total
        print(f"{s['type']:<20} {s['count']:>5} {pct:>5.1f}% {s['avg_s2']:>8.3f} {s['avg_newline_confidence']:>11.3f}")

    print("\n=== TOP-1 PREDICTION WAS NEWLINE ===")
    summaries_top1 = summarize_by_type(traps_top1)
    total_top1 = len(traps_top1)
    print(f"{'Type':<20} {'N':>5} {'%':>6} {'Avg S2':>8}")
    print("-" * 50)
    for s in summaries_top1:
        pct = 100 * s['count'] / total_top1
        print(f"{s['type']:<20} {s['count']:>5} {pct:>5.1f}% {s['avg_s2']:>8.3f}")

    print("\n=== MOST EXTREME ENJAMBMENT TRAPS (highest newline confidence defeated) ===")
    extremes = highest_confidence_traps(traps_top1, n=15)
    for i, t in enumerate(extremes):
        print(f"{i+1:2}. {t['author']}: '{t['context'].strip()[-30:]}' → '{t['token'].strip()}'")
        print(f"    NL prob={t['newline_prob']:.3f}, S2={t['s2']:.2f}, type={t['token_type']}")

    print("\n=== HIGH-S2 EXAMPLES BY TYPE ===")
    for s in sorted(summaries_top1, key=lambda x: -x['avg_s2'])[:6]:
        print(f"\n{s['type']} (avg S2 = {s['avg_s2']:.3f}):")
        for tok, s2, auth, title in s['examples'][:2]:
            print(f"  '{tok}' (S2={s2:.2f}) — {auth}: {title}")

    print("\n=== S2 COMPARISON: ENJAMBMENT TRAPS VS CONTROL ===")
    # Compare avg S2 of enjambment traps to overall corpus avg
    all_s2 = []
    en_s2 = []
    for poem in data:
        if poem['metadata'].get('language', 'en') != 'en':
            continue
        for tok in poem['tokens']:
            all_s2.append(tok['s2'])
    en_trap_s2 = [t['s2'] for t in traps_top1]
    all_avg = sum(all_s2) / len(all_s2) if all_s2 else 0
    trap_avg = sum(en_trap_s2) / len(en_trap_s2) if en_trap_s2 else 0
    print(f"Average S2 across all English tokens: {all_avg:.4f}")
    print(f"Average S2 at enjambment trap tokens: {trap_avg:.4f}")
    print(f"Enjambment premium (trap - baseline): {trap_avg - all_avg:.4f}")

    # Save results
    results = {
        'total_traps_15pct': len(traps_all),
        'total_traps_top1': len(traps_top1),
        'by_type_all': summaries,
        'by_type_top1': summaries_top1,
        'extreme_examples': extremes[:10],
        'corpus_avg_s2': all_avg,
        'trap_avg_s2': trap_avg,
    }
    with open('/home/user/s2lab/results/enjambment_specificity.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/enjambment_specificity.json")
