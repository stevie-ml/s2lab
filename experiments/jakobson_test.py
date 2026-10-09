"""
The Jakobson Test: Selection vs. Combination Surprise in Poetry

Roman Jakobson (1956) argued that language has two axes:
  - SELECTION (metaphoric axis): choosing one word over paradigmatically similar alternatives
  - COMBINATION (metonymic axis): linking words in a syntagmatic sequence

In information-theoretic terms:
  - Q2 (confident mismatch): model was SURE about what should come next (low entropy = stable
    syntactic/combinatorial context), but poet chose something unexpected.
    → Selection surprise: the paradigmatic slot was clear, the choice was not.
    → Maps to Jakobson's METAPHORIC axis.

  - Q1 (ambiguous surprise): model was UNCERTAIN about what comes next (high entropy = unstable
    combinatorial context), AND the poet still surprised it.
    → Combination surprise: the sequence was already in flux, suggesting unusual combinations.
    → Maps to Jakobson's METONYMIC axis.

Hypothesis: Poets renowned for metaphoric richness (Keats, Hopkins, Dickinson) will have
high Q2/Q1 ratios. Poets renowned for unusual combination / juxtaposition
(Gertrude Stein, Language poets, Whitman catalogs) will have low Q2/Q1 ratios.

Additional test: In Q2 positions, do poets substitute CONTENT words for FUNCTION words
(structural substitution) or CONTENT for CONTENT (lexical substitution)?
- Content-for-function substitution: the model expected 'the/a/and/,' but poet wrote a noun/verb.
  This is the purest "defying the syntax" move.
- Content-for-content substitution: model expected a content word, poet chose a different one.
  This is "defying the lexical expectation".

We can classify GPT-2's top prediction and the actual poet token as:
  FUNCTION: determiners, prepositions, conjunctions, pronouns, auxiliaries, punctuation, newlines
  CONTENT: nouns, verbs (non-auxiliary), adjectives, adverbs (non-discourse)
"""

import json
import sys
import os
import re
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")

# ── Function word vocabulary ──────────────────────────────────────────────────
# These stripped and lowercased forms count as function words.
FUNCTION_WORDS = {
    # Articles
    'the', 'a', 'an',
    # Prepositions
    'in', 'on', 'at', 'by', 'for', 'with', 'about', 'against', 'between',
    'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
    'up', 'down', 'into', 'onto', 'upon', 'of', 'off', 'over', 'under',
    'out', 'along', 'around', 'near', 'across', 'behind', 'beside',
    'beyond', 'inside', 'outside', 'within', 'without', 'toward', 'towards',
    'until', 'unless',
    # Conjunctions
    'and', 'but', 'or', 'nor', 'yet', 'so', 'for', 'than', 'as', 'if',
    'when', 'while', 'because', 'since', 'although', 'though', 'that',
    'which', 'who', 'whom', 'whose', 'where', 'whether', 'after', 'before',
    # Pronouns
    'i', 'me', 'my', 'myself', 'we', 'us', 'our', 'ourselves',
    'you', 'your', 'yourself', 'yourselves',
    'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself',
    'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
    'this', 'that', 'these', 'those', 'what', 'which', 'who', 'whom',
    'each', 'every', 'all', 'both', 'few', 'more', 'most', 'other',
    'some', 'such', 'no', 'not', 'only', 'same',
    # Auxiliaries
    'is', 'am', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did',
    'will', 'would', 'shall', 'should', 'may', 'might', 'must',
    'can', 'could', 'ought', 'need', 'dare',
    # Common discourse
    'there', 'here', 'then', 'now', 'still', 'just', 'also', 'too',
    'even', 'never', 'always', 'often', 'much', 'many', 'more', 'less',
    'very', 'so', 'quite', 'rather',
}

PUNCT_TOKENS = {',', '.', ';', ':', '!', '?', '"', "'", '(', ')', '[', ']',
                '-', '--', '—', '...', '..', '``', "''", '/', '\\',
                '\n', '\t', ' '}

def clean_token(token):
    """Strip leading space and lowercase."""
    return token.lstrip().lower()

def classify_token(token):
    """Classify a GPT-2 token as FUNCTION, PUNCT/NEWLINE, or CONTENT."""
    stripped = token.strip()
    if stripped in PUNCT_TOKENS or stripped == '' or token == '\n':
        return 'punct_newline'
    clean = clean_token(token)
    if clean in FUNCTION_WORDS:
        return 'function'
    # Heuristic: if the token is very short (1-2 chars) and not alphabetic, likely punct
    if len(clean) <= 2 and not clean.isalpha():
        return 'punct_newline'
    return 'content'

def get_top_prediction_class(alternatives):
    """Get the class of GPT-2's top predicted token."""
    if not alternatives:
        return 'unknown'
    return classify_token(alternatives[0]['token'])

def is_artifact(tok):
    return tok.get('p_newline', 0) >= 0.9

def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def get_quadrant(surprisal, entropy, surp_median, ent_median):
    if surprisal > surp_median and entropy <= ent_median:
        return 'Q2'   # Confident mismatch (metaphoric)
    elif surprisal > surp_median and entropy > ent_median:
        return 'Q1'   # Ambiguous surprise (metonymic)
    elif surprisal <= surp_median and entropy <= ent_median:
        return 'Q3'
    else:
        return 'Q4'

def run():
    data = load_data()
    print("=== The Jakobson Test: Selection vs. Combination Surprise ===\n")

    # ── Compute corpus medians ────────────────────────────────────────────────
    all_surp, all_ent = [], []
    for poem in data:
        for tok in poem['tokens']:
            if is_artifact(tok):
                continue
            all_surp.append(tok['surprisal'])
            all_ent.append(tok['entropy'])

    all_surp.sort(); all_ent.sort()
    surp_median = all_surp[len(all_surp) // 2]
    ent_median  = all_ent[len(all_ent) // 2]
    print(f"Surprisal median: {surp_median:.2f} bits | Entropy median: {ent_median:.2f} bits\n")

    # ── Per-poet Q2/Q1 analysis ───────────────────────────────────────────────
    poet_data = defaultdict(lambda: {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'total': 0,
                                     'q2_subst': {'cf': 0, 'cc': 0, 'ff': 0, 'fc': 0},
                                     'q1_subst': {'cf': 0, 'cc': 0, 'ff': 0, 'fc': 0}})
    era_data = defaultdict(lambda: {'Q1': 0, 'Q2': 0, 'Q3': 0, 'Q4': 0, 'total': 0})

    for poem in data:
        author = poem['metadata'].get('author', 'Unknown')
        era    = poem['metadata'].get('era', 'unknown')
        for tok in poem['tokens']:
            if is_artifact(tok):
                continue
            q = get_quadrant(tok['surprisal'], tok['entropy'], surp_median, ent_median)
            poet_data[author][q] += 1
            poet_data[author]['total'] += 1
            era_data[era][q] += 1
            era_data[era]['total'] += 1

            # For Q2 and Q1, classify the substitution type
            actual_class = classify_token(tok['token'])
            pred_class   = get_top_prediction_class(tok.get('alternatives', []))
            if q in ('Q1', 'Q2'):
                key = f"{pred_class[0]}{actual_class[0]}"  # e.g. 'fc' = function predicted, content chosen
                if key in poet_data[author][f'q{q[1]}_subst']:
                    poet_data[author][f'q{q[1]}_subst'][key] += 1

    # ── Compute Q2/Q1 ratios ──────────────────────────────────────────────────
    print("=== Poet Q2/Q1 Ratios (Selection/Combination Surprise Index) ===\n")
    print("High Q2/Q1 = metaphoric/selection strategy (confident mismatch dominant)")
    print("Low  Q2/Q1 = metonymic/combination strategy (ambiguous surprise dominant)\n")

    poet_rows = []
    for poet, d in poet_data.items():
        total = d['total']
        if total < 40:
            continue
        q1, q2 = d['Q1'], d['Q2']
        ratio = q2 / q1 if q1 > 0 else float('inf')
        # Content-for-function rate in Q2: the purest "defying the syntax" move
        cf_rate = d['q2_subst'].get('cf', 0) / max(q2, 1)
        cc_rate = d['q2_subst'].get('cc', 0) / max(q2, 1)
        poet_rows.append({
            'poet': poet, 'total': total,
            'q1': q1, 'q2': q2,
            'q1_pct': 100 * q1 / total, 'q2_pct': 100 * q2 / total,
            'ratio': ratio,
            'cf_rate': cf_rate,  # content-for-function (syntax-defying)
            'cc_rate': cc_rate,  # content-for-content (lexical substitution)
        })

    poet_rows.sort(key=lambda x: x['ratio'], reverse=True)

    print(f"{'Poet':<40} {'n':>5} {'Q2%':>6} {'Q1%':>6} {'Q2/Q1':>7} {'C/F rate':>9} {'C/C rate':>9}")
    print("-" * 90)
    for r in poet_rows:
        q21_str = f"{r['ratio']:.2f}" if r['ratio'] < 10 else f"{r['ratio']:.1f}"
        print(f"{r['poet']:<40} {r['total']:>5} {r['q2_pct']:>6.1f} {r['q1_pct']:>6.1f} "
              f"{q21_str:>7} {r['cf_rate']:>9.1%} {r['cc_rate']:>9.1%}")

    # ── Top metaphoric strategists vs. top metonymic strategists ─────────────
    print("\n=== Top METAPHORIC strategists (highest Q2/Q1, dominant SELECTION surprise) ===\n")
    for r in poet_rows[:10]:
        print(f"  {r['poet']}: Q2/Q1 = {r['ratio']:.2f}  "
              f"(Q2={r['q2_pct']:.1f}%, Q1={r['q1_pct']:.1f}%,  "
              f"syntax-defy={r['cf_rate']:.1%}, lex-subst={r['cc_rate']:.1%})")

    print("\n=== Top METONYMIC strategists (lowest Q2/Q1, dominant COMBINATION surprise) ===\n")
    for r in reversed(poet_rows[-10:]):
        print(f"  {r['poet']}: Q2/Q1 = {r['ratio']:.2f}  "
              f"(Q2={r['q2_pct']:.1f}%, Q1={r['q1_pct']:.1f}%)")

    # ── Substitution type breakdown: what GPT-2 expected vs what poet chose ──
    print("\n=== Substitution Types in Q2 (Confident Mismatch) ===\n")
    print("C/F = content word chosen when function/punct predicted  (defies syntax)")
    print("C/C = content word chosen when content word predicted    (lexical swap)")
    print("F/F = function word chosen when function predicted       (unexpected function)")
    print("F/C = function word chosen when content predicted        (de-lexicalization)\n")

    # Corpus-wide aggregation
    corpus_q2_subst = defaultdict(int)
    corpus_q1_subst = defaultdict(int)
    for d in poet_data.values():
        for k, v in d['q2_subst'].items():
            corpus_q2_subst[k] += v
        for k, v in d['q1_subst'].items():
            corpus_q1_subst[k] += v

    q2_total = sum(corpus_q2_subst.values())
    q1_total = sum(corpus_q1_subst.values())

    print("Q2 (Confident Mismatch) substitution breakdown:")
    for k in ['cf', 'cc', 'ff', 'fc']:
        lbl = {'cf': 'content for function/punct', 'cc': 'content for content',
               'ff': 'function for function', 'fc': 'function for content'}[k]
        n = corpus_q2_subst.get(k, 0)
        print(f"  {lbl}: {n:>6}  ({100*n/max(q2_total,1):.1f}%)")

    print("\nQ1 (Ambiguous Surprise) substitution breakdown:")
    for k in ['cf', 'cc', 'ff', 'fc']:
        lbl = {'cf': 'content for function/punct', 'cc': 'content for content',
               'ff': 'function for function', 'fc': 'function for content'}[k]
        n = corpus_q1_subst.get(k, 0)
        print(f"  {lbl}: {n:>6}  ({100*n/max(q1_total,1):.1f}%)")

    # ── Era-level Jakobson analysis ───────────────────────────────────────────
    print("\n=== Era Q2/Q1 Ratio (Jakobson Index) ===\n")
    era_rows = []
    for era, d in era_data.items():
        if d['total'] < 20:
            continue
        q1, q2 = d['Q1'], d['Q2']
        ratio = q2 / q1 if q1 > 0 else float('inf')
        era_rows.append({'era': era, 'n': d['total'],
                         'q1_pct': 100*q1/d['total'], 'q2_pct': 100*q2/d['total'],
                         'ratio': ratio})
    era_rows.sort(key=lambda x: x['ratio'], reverse=True)
    print(f"{'Era':<30} {'n':>6} {'Q2%':>6} {'Q1%':>6} {'Q2/Q1':>7}")
    print("-" * 60)
    for r in era_rows:
        print(f"{r['era']:<30} {r['n']:>6} {r['q2_pct']:>6.1f} {r['q1_pct']:>6.1f} "
              f"{r['ratio']:>7.2f}")

    # ── Example Q2 tokens by substitution type ───────────────────────────────
    print("\n=== Best examples of each Q2 substitution type ===\n")

    examples = {'cf': [], 'cc': [], 'ff': []}
    ARTIFACT_THRESHOLD = 0.9
    for poem in data:
        author = poem['metadata'].get('author', 'Unknown')
        title  = poem['metadata'].get('title', '')
        for tok in poem['tokens']:
            if is_artifact(tok):
                continue
            q = get_quadrant(tok['surprisal'], tok['entropy'], surp_median, ent_median)
            if q != 'Q2':
                continue
            actual_class = classify_token(tok['token'])
            pred_class   = get_top_prediction_class(tok.get('alternatives', []))
            key = f"{pred_class[0]}{actual_class[0]}"
            if key in examples:
                top_pred = tok['alternatives'][0]['token'] if tok.get('alternatives') else '?'
                examples[key].append({
                    'token': tok['token'], 'top_pred': top_pred,
                    's2': tok['s2'], 'surp': tok['surprisal'], 'ent': tok['entropy'],
                    'author': author, 'title': title,
                    'context': tok.get('context_before', '')[-40:]
                })

    for key, label in [('cf', 'Content for Function (syntax-defy)'),
                       ('cc', 'Content for Content (lexical swap)'),
                       ('ff', 'Function for Function (functional shift)')]:
        srt = sorted(examples[key], key=lambda x: x['s2'], reverse=True)[:5]
        print(f"--- {label} ---")
        for e in srt:
            ctx = e['context'].replace('\n', '↵')
            print(f"  \"{ctx}\" → [{e['token'].strip()}] (GPT-2 expected: {e['top_pred'].strip()!r})")
            print(f"    S₂={e['s2']:.2f}  surp={e['surp']:.2f}  ent={e['ent']:.2f}")
            print(f"    — {e['author']}, \"{e['title']}\"")
        print()

    # ── Return results dict for saving ───────────────────────────────────────
    return {
        'surp_median': surp_median,
        'ent_median': ent_median,
        'poet_ratios': [
            {'poet': r['poet'], 'q2_q1_ratio': round(r['ratio'], 3),
             'q2_pct': round(r['q2_pct'], 2), 'q1_pct': round(r['q1_pct'], 2),
             'n': r['total'],
             'cf_rate': round(r['cf_rate'], 3), 'cc_rate': round(r['cc_rate'], 3)}
            for r in poet_rows
        ],
        'corpus_q2_subst': dict(corpus_q2_subst),
        'corpus_q1_subst': dict(corpus_q1_subst),
        'era_ratios': [
            {'era': r['era'], 'q2_q1_ratio': round(r['ratio'], 3),
             'q2_pct': round(r['q2_pct'], 2), 'q1_pct': round(r['q1_pct'], 2),
             'n': r['n']}
            for r in era_rows
        ],
    }


if __name__ == "__main__":
    result = run()
    import json
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "jakobson_test.json")
    with open(out_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to {out_path}")
