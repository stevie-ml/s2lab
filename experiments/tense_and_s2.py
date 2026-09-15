"""
Tense and S₂: The Grammar of Time in Poetic Surprise

Research question: Does verb tense — and especially tense transitions — correlate
with S₂ patterns in poetry? When a poem shifts from past to present (or vice versa),
does GPT-2 register surprise, producing a measurable S₂ spike?

The 'Temporal Straussian Gap' hypothesis:
  Poetry's famous "lyric present" — the sudden shift into present tense even when
  narrating past events — creates syntactic surprise. GPT-2, trained on prose that
  maintains tense consistency, expects tense continuity. When a poet violates this
  expectation, that violation registers as high S₂. The lyric present may be
  computationally detectable as a grammar-level surprise.

Sub-hypotheses:
  H1: Modal verbs (would/could/might) occupy a distinctive S₂ range — the model
      is often confident about predicting modals in hedging contexts, so when the
      poet uses one, it's low-S₂; but modals in unexpected positions are high-S₂.
  H2: Past-tense tokens have lower mean S₂ than present-tense in narrative-heavy poems
      (past is more expected from the model's prose training).
  H3: Tense-mismatch moments — where GPT-2 predicts past but gets present (or vice
      versa) — are high-S₂ events: the temporal Straussian gap.

Method:
  1. Classify each token as past/present/future/modal using lexicon + morphology
  2. For each tense token, check whether GPT-2's top-3 alternatives are same-tense
  3. Compute S₂ at tense-match vs tense-mismatch positions
  4. Compare mean S₂ across tense categories and eras
  5. Identify the highest-S₂ tense-switching moments across the corpus
"""

import json
import re
import statistics
from pathlib import Path
from collections import defaultdict

RESULTS_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"

# ── Tense lexicons ─────────────────────────────────────────────────────────────

PAST_IRREGULAR = {
    'was', 'were', 'had', 'did', 'went', 'saw', 'came', 'felt', 'knew',
    'thought', 'told', 'found', 'left', 'stood', 'kept', 'heard', 'brought',
    'looked', 'turned', 'began', 'seemed', 'fell', 'walked', 'held', 'rose',
    'ran', 'sat', 'took', 'made', 'said', 'asked', 'lost', 'broke', 'spoke',
    'bore', 'woke', 'grew', 'blew', 'flew', 'sang', 'rang', 'hung', 'caught',
    'bought', 'fought', 'sought', 'taught', 'built', 'sent', 'spent', 'meant',
    'led', 'met', 'put', 'cut', 'wept', 'slept', 'crept', 'leapt', 'dreamt',
    'swept', 'knelt', 'dwelt', 'smelt', 'spelt', 'lay', 'saw', 'beat', 'bet',
    'bid', 'bit', 'bled', 'bred', 'fed', 'fled', 'pled', 'shed', 'sped',
    'sold', 'told', 'held', 'dealt', 'felt', 'knelt', 'meant', 'sent',
    'lent', 'bent', 'leant', 'burnt', 'learnt', 'dreamt', 'spelt',
    'dwelt', 'smelt', 'crept', 'slept', 'wept', 'kept',
    'lit', 'hit', 'set', 'let', 'hurt', 'quit', 'rid', 'spread',
    'thrust', 'cast', 'burst', 'cost', 'shut',
}

PRESENT_FORMS = {
    'is', 'are', 'am', 'has', 'have', 'do', 'does', 'know', 'see', 'come',
    'go', 'say', 'think', 'look', 'seem', 'feel', 'hear', 'become', 'keep',
    'stand', 'fall', 'sit', 'rise', 'begin', 'hold', 'walk', 'turn', 'find',
    'make', 'break', 'speak', 'write', 'live', 'lie', 'die', 'fly', 'run',
    'sing', 'ring', 'bring', 'think', 'leave', 'give', 'take', 'show',
    'gets', 'goes', 'says', 'knows', 'sees', 'feels', 'hears', 'means',
    'looks', 'turns', 'finds', 'makes', 'keeps', 'holds', 'stands',
    'remains', 'becomes', 'appears', 'seems', 'sounds', 'smells', 'tastes',
}

FUTURE_MARKERS = {'will', 'shall'}

MODAL_MARKERS = {'would', 'could', 'might', 'should', 'must', 'may', 'ought'}


def clean_token(tok: str) -> str:
    return tok.strip().lower().rstrip('.,;:!?"\')—-')


def classify_tense(token: str) -> str | None:
    """Return tense category or None if not a tense marker."""
    t = clean_token(token)
    if not t or not t.isalpha():
        return None

    if t in MODAL_MARKERS:
        return 'modal'
    if t in FUTURE_MARKERS:
        return 'future'
    if t in PAST_IRREGULAR:
        return 'past'
    if t in PRESENT_FORMS:
        return 'present'

    # Regular past tense: ends in -ed, not a known present/modal
    if t.endswith('ed') and len(t) > 4:
        return 'past'

    # Present participle / gerund: -ing forms (can be past or present, skip)
    # Third-person -s: hard to distinguish from plural nouns — skip

    return None


def get_alternative_tense(alts: list) -> str | None:
    """Check if any of the top-3 GPT-2 alternatives has a tense classification."""
    for alt in alts[:3]:
        t = classify_tense(alt['token'])
        if t:
            return t
    return None


def run_analysis():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Global accumulators
    tense_s2: dict[str, list] = defaultdict(list)       # tense → [s2]
    mismatch_s2: list = []                               # s2 at tense mismatches
    match_s2: list = []                                  # s2 at tense matches
    tense_examples: dict[str, list] = defaultdict(list) # tense → top examples
    mismatch_examples: list = []

    era_tense_s2: dict[str, dict[str, list]] = defaultdict(lambda: defaultdict(list))

    # Per-poem: detect tense transitions (sequence of tense labels)
    transition_s2: list = []     # s2 at transitions
    sustained_s2: list = []      # s2 in sustained tense (not a transition)

    total_poems = 0
    tense_poems = 0

    for poem in data:
        meta = poem['metadata']
        era = meta.get('era', 'unknown')
        tokens = poem['tokens']

        # Build tense sequence for this poem
        tense_seq = []  # (position, tense, s2, token)
        for tok in tokens:
            t = classify_tense(tok['token'])
            if t:
                tense_seq.append((tok['position'], t, tok['s2'], tok['token'].strip()))
                tense_s2[t].append(tok['s2'])
                era_tense_s2[era][t].append(tok['s2'])

                # Check tense mismatch: actual tense vs predicted tense
                alt_tense = get_alternative_tense(tok.get('alternatives', []))
                if alt_tense is not None:
                    if alt_tense == t:
                        match_s2.append(tok['s2'])
                    else:
                        mismatch_s2.append(tok['s2'])
                        mismatch_examples.append({
                            'poem': meta.get('title', '?'),
                            'author': meta.get('author', '?'),
                            'year': meta.get('year', 0),
                            'token': tok['token'].strip(),
                            'actual_tense': t,
                            'predicted_tense': alt_tense,
                            's2': tok['s2'],
                            'top_alt': tok['alternatives'][0]['token'].strip() if tok.get('alternatives') else '?',
                            'context': tok.get('context_before', '')[-40:],
                        })

        total_poems += 1
        if tense_seq:
            tense_poems += 1

        # Detect transitions in the tense sequence
        prev_tense = None
        for i, (pos, tense, s2, tok) in enumerate(tense_seq):
            if prev_tense is not None and tense != prev_tense:
                # This is a transition point
                transition_s2.append(s2)
                tense_examples[f'{prev_tense}→{tense}'].append({
                    'poem': meta.get('title', '?'),
                    'author': meta.get('author', '?'),
                    'year': meta.get('year', 0),
                    'token': tok,
                    's2': s2,
                    'transition': f'{prev_tense}→{tense}',
                })
            else:
                sustained_s2.append(s2)
            prev_tense = tense

    # Sort mismatch examples by S₂ descending
    mismatch_examples.sort(key=lambda x: x['s2'], reverse=True)

    # Build results
    results = {
        'total_poems': total_poems,
        'poems_with_tense_tokens': tense_poems,
        'tense_counts': {t: len(v) for t, v in tense_s2.items()},
        'tense_mean_s2': {
            t: round(statistics.mean(v), 4)
            for t, v in tense_s2.items() if v
        },
        'tense_median_s2': {
            t: round(statistics.median(v), 4)
            for t, v in tense_s2.items() if v
        },
        'tense_std_s2': {
            t: round(statistics.stdev(v), 4)
            for t, v in tense_s2.items() if len(v) > 1
        },
        'match_count': len(match_s2),
        'mismatch_count': len(mismatch_s2),
        'match_mean_s2': round(statistics.mean(match_s2), 4) if match_s2 else None,
        'mismatch_mean_s2': round(statistics.mean(mismatch_s2), 4) if mismatch_s2 else None,
        'transition_count': len(transition_s2),
        'sustained_count': len(sustained_s2),
        'transition_mean_s2': round(statistics.mean(transition_s2), 4) if transition_s2 else None,
        'sustained_mean_s2': round(statistics.mean(sustained_s2), 4) if sustained_s2 else None,
        'transition_types': {
            k: {
                'count': len(v),
                'mean_s2': round(statistics.mean([x['s2'] for x in v]), 4),
            }
            for k, v in sorted(tense_examples.items(), key=lambda x: -len(x[1]))
        },
        'era_tense_mean_s2': {
            era: {
                t: round(statistics.mean(vs), 4)
                for t, vs in tenses.items() if vs
            }
            for era, tenses in era_tense_s2.items()
        },
        'top_mismatch_examples': mismatch_examples[:20],
        'top_transition_examples': {
            k: sorted(v, key=lambda x: -x['s2'])[:3]
            for k, v in tense_examples.items()
        },
    }

    return results


if __name__ == '__main__':
    print("Analyzing tense and S₂...")
    results = run_analysis()

    print(f"\nCorpus: {results['total_poems']} poems, "
          f"{results['poems_with_tense_tokens']} with tense tokens")

    print("\n── Tense category S₂ ──────────────────────────")
    for tense in ['past', 'present', 'future', 'modal']:
        if tense in results['tense_mean_s2']:
            print(f"  {tense:10s}: n={results['tense_counts'][tense]:4d}, "
                  f"mean S₂={results['tense_mean_s2'][tense]:+.3f}, "
                  f"median={results['tense_median_s2'][tense]:+.3f}")

    print("\n── Tense match vs mismatch ─────────────────────")
    print(f"  Match   (model predicted same tense): n={results['match_count']:4d}, "
          f"mean S₂={results['match_mean_s2']:+.3f}")
    print(f"  Mismatch (model predicted diff tense): n={results['mismatch_count']:4d}, "
          f"mean S₂={results['mismatch_mean_s2']:+.3f}")

    print("\n── Transition vs sustained S₂ ──────────────────")
    print(f"  Transition points: n={results['transition_count']:4d}, "
          f"mean S₂={results['transition_mean_s2']:+.3f}")
    print(f"  Sustained (same tense): n={results['sustained_count']:4d}, "
          f"mean S₂={results['sustained_mean_s2']:+.3f}")

    print("\n── Transition type breakdown ───────────────────")
    for trans, info in sorted(results['transition_types'].items(),
                               key=lambda x: -x[1]['mean_s2']):
        print(f"  {trans:20s}: n={info['count']:3d}, mean S₂={info['mean_s2']:+.3f}")

    print("\n── Top tense-mismatch examples (highest S₂) ───")
    for ex in results['top_mismatch_examples'][:10]:
        print(f"  [{ex['year']}] {ex['author'][:20]:20s} | "
              f"'{ex['token']}' (actual:{ex['actual_tense']}, "
              f"pred:{ex['predicted_tense']}, S₂={ex['s2']:+.2f})")
        print(f"    context: ...{ex['context']}...")
        print(f"    GPT-2 top alt: '{ex['top_alt']}'")

    print("\n── Era analysis ────────────────────────────────")
    for era, tenses in sorted(results['era_tense_mean_s2'].items()):
        parts = ', '.join(f"{t}={v:+.3f}" for t, v in tenses.items())
        print(f"  {era:20s}: {parts}")

    out_path = Path(__file__).parent.parent / "results" / "tense_s2_results.json"
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
