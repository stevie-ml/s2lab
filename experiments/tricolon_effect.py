"""
Tricolon Effect: Does the Third List Item Have Higher S2?
=========================================================
Classical rhetoric holds that the tricolon (series of three) reaches
its maximum power at the third element. Climax (ascending force) and
the "rule of three" (Omne trium perfectum) both predict that the THIRD
item in a list carries the most weight.

Information-theoretic question: Does GPT-2 confirm this? Specifically,
given "A, B, and C":
  - Is S2(C) > S2(B) > S2(A)?  (climax law)
  - Or is S2(A) > S2(B) > S2(C)?  (front-loading / anticlimax)
  - Or S2(C) > max(S2(A), S2(B))?  (surprise-at-end)
  - Or S2(A) > max(S2(B), S2(C))?  (surprise-at-start / anti-Aristotelian)

We also test ENTROPY H: does GPT-2 become more or less certain as it
approaches the final list item? If the model learns the list pattern
early (from position 1 and 2), H at position 3 should be LOWER —
meaning a high S2(C) would be a genuine defiance of confident prediction.

Method:
  1. Load corpus_results.json
  2. Regex-search each poem's full text for "X, Y, and Z" noun-phrase patterns
  3. Align matched phrases back to token-level data to extract S2 and H
  4. Aggregate across all poets and eras
  5. Statistical test: paired sign test on S2(1) vs S2(3)

This gives an information-theoretic test of the classical "rule of three."
"""

import json
import re
import sys
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUT_PATH = "results/tricolon_effect.json"
P_NEWLINE_THRESHOLD = 0.9

def load_corpus():
    with open(CORPUS_PATH) as f:
        return json.load(f)


def reconstruct_text_with_positions(tokens):
    """Return (full_text, char_to_token_idx) mapping."""
    text = ""
    char_to_idx = []
    for i, tok in enumerate(tokens):
        t = tok['token']
        for _ in t:
            char_to_idx.append(i)
        text += t
    return text, char_to_idx


def find_first_content_token_in_span(tokens, start_char, end_char, char_to_idx):
    """
    Given a character span in the full text, find the first non-whitespace,
    non-artifact token's index in the token list.
    """
    seen = set()
    for ci in range(start_char, min(end_char, len(char_to_idx))):
        ti = char_to_idx[ci]
        if ti in seen:
            continue
        seen.add(ti)
        tok = tokens[ti]
        if tok['token'].strip() and tok.get('p_newline', 0) < P_NEWLINE_THRESHOLD:
            return ti
    return None


def extract_tricolon_hits(poem):
    """
    Find "A, B, and C" patterns in the poem and return list of
    (pos1, pos2, pos3) token indices representing the first content
    token of each list element.
    """
    tokens = poem['tokens']
    text, char_to_idx = reconstruct_text_with_positions(tokens)

    # Pattern: capture three groups separated by commas and "and"/"or"
    # Allows multi-word items in each slot, bounded by newlines
    # Group1: [^,\n]+ (first element)
    # ,\s*
    # Group2: [^,\n]+ (second element)
    # ,\s*(and|or)\s+
    # Group3: [^,\n.]+ (third element)
    pattern = re.compile(
        r'([A-Za-z][^,\n]{1,50}),\s*'   # A
        r'([A-Za-z][^,\n]{1,50}),\s*'   # B
        r'(?:and|or)\s+'                  # "and"/"or"
        r'([A-Za-z][^,\n.!?]{1,50})',    # C
        re.IGNORECASE
    )

    hits = []
    for m in pattern.finditer(text):
        a_start = m.start(1)
        b_start = m.start(2)
        c_start = m.start(3)
        a_end   = m.end(1)
        b_end   = m.end(2)
        c_end   = m.end(3)

        ti_a = find_first_content_token_in_span(tokens, a_start, a_end, char_to_idx)
        ti_b = find_first_content_token_in_span(tokens, b_start, b_end, char_to_idx)
        ti_c = find_first_content_token_in_span(tokens, c_start, c_end, char_to_idx)

        if ti_a is None or ti_b is None or ti_c is None:
            continue
        if ti_a == ti_b or ti_b == ti_c:
            continue

        tok_a = tokens[ti_a]
        tok_b = tokens[ti_b]
        tok_c = tokens[ti_c]

        hits.append({
            'phrase': m.group(0)[:100],
            'a_text': tok_a['token'].strip(),
            'b_text': tok_b['token'].strip(),
            'c_text': tok_c['token'].strip(),
            's2_a': tok_a['s2'],
            's2_b': tok_b['s2'],
            's2_c': tok_c['s2'],
            'h_a': tok_a['entropy'],
            'h_b': tok_b['entropy'],
            'h_c': tok_c['entropy'],
            'rank_a': tok_a.get('rank', None),
            'rank_b': tok_b.get('rank', None),
            'rank_c': tok_c.get('rank', None),
        })

    return hits


def mean(xs):
    return sum(xs) / len(xs) if xs else float('nan')

def median(xs):
    if not xs:
        return float('nan')
    s = sorted(xs)
    n = len(s)
    return (s[n//2] if n % 2 else (s[n//2-1] + s[n//2]) / 2)


def main():
    corpus = load_corpus()
    all_hits = []
    poem_hit_counts = []

    for poem in corpus:
        lang = poem['metadata'].get('language', 'en')
        if lang != 'en':
            continue
        hits = extract_tricolon_hits(poem)
        if hits:
            poem_hit_counts.append({
                'title': poem['metadata']['title'],
                'author': poem['metadata']['author'],
                'era': poem['metadata'].get('era', 'unknown'),
                'n_tricola': len(hits),
            })
        for h in hits:
            h['title'] = poem['metadata']['title']
            h['author'] = poem['metadata']['author']
            h['era'] = poem['metadata'].get('era', 'unknown')
        all_hits.extend(hits)

    print(f"Total tricolon hits: {len(all_hits)}")
    print(f"Poems with ≥1 tricolon: {len(poem_hit_counts)}")

    if not all_hits:
        print("No tricolon hits found — exiting.")
        return

    # ── Overall S2 by position ───────────────────────────────────────
    s2_a = [h['s2_a'] for h in all_hits]
    s2_b = [h['s2_b'] for h in all_hits]
    s2_c = [h['s2_c'] for h in all_hits]
    h_a  = [h['h_a'] for h in all_hits]
    h_b  = [h['h_b'] for h in all_hits]
    h_c  = [h['h_c'] for h in all_hits]

    print(f"\nOverall S2 by list position:")
    print(f"  A (1st): mean={mean(s2_a):.3f}  median={median(s2_a):.3f}")
    print(f"  B (2nd): mean={mean(s2_b):.3f}  median={median(s2_b):.3f}")
    print(f"  C (3rd): mean={mean(s2_c):.3f}  median={median(s2_c):.3f}")

    print(f"\nOverall Entropy H by position:")
    print(f"  A (1st): mean={mean(h_a):.3f}")
    print(f"  B (2nd): mean={mean(h_b):.3f}")
    print(f"  C (3rd): mean={mean(h_c):.3f}")

    # ── Sign tests ───────────────────────────────────────────────────
    n = len(all_hits)
    c_gt_a = sum(1 for h in all_hits if h['s2_c'] > h['s2_a'])
    c_gt_b = sum(1 for h in all_hits if h['s2_c'] > h['s2_b'])
    a_gt_c = sum(1 for h in all_hits if h['s2_a'] > h['s2_c'])
    b_gt_c = sum(1 for h in all_hits if h['s2_b'] > h['s2_c'])
    c_max  = sum(1 for h in all_hits if h['s2_c'] > h['s2_a'] and h['s2_c'] > h['s2_b'])
    a_max  = sum(1 for h in all_hits if h['s2_a'] > h['s2_b'] and h['s2_a'] > h['s2_c'])
    b_max  = sum(1 for h in all_hits if h['s2_b'] > h['s2_a'] and h['s2_b'] > h['s2_c'])

    print(f"\nSign tests (n={n}):")
    print(f"  S2(C) > S2(A): {c_gt_a}/{n} = {100*c_gt_a/n:.1f}%")
    print(f"  S2(C) > S2(B): {c_gt_b}/{n} = {100*c_gt_b/n:.1f}%")
    print(f"  S2(A) > S2(C): {a_gt_c}/{n} = {100*a_gt_c/n:.1f}%")
    print(f"  S2(B) > S2(C): {b_gt_c}/{n} = {100*b_gt_c/n:.1f}%")
    print(f"\nWhich position is MAX S2?")
    print(f"  A is max: {a_max}/{n} = {100*a_max/n:.1f}%")
    print(f"  B is max: {b_max}/{n} = {100*b_max/n:.1f}%")
    print(f"  C is max: {c_max}/{n} = {100*c_max/n:.1f}%")

    # ── Entropy at position 3 ────────────────────────────────────────
    # Is model MORE or LESS certain at position 3 vs 1?
    h_c_lt_a = sum(1 for h in all_hits if h['h_c'] < h['h_a'])
    print(f"\nEntropy at C < Entropy at A: {h_c_lt_a}/{n} = {100*h_c_lt_a/n:.1f}%")
    print(f"  (If > 50%: model is MORE confident at position 3 → high S2 at C = genuine defiance)")

    # ── Top tricola by S2(C) ─────────────────────────────────────────
    top_c = sorted(all_hits, key=lambda h: h['s2_c'], reverse=True)[:20]
    print(f"\nTop 20 tricola by S2(C) — highest 'third item' surprise:")
    for h in top_c:
        print(f"  [{h['author']}] S2(C)={h['s2_c']:.2f} | phrase: {h['phrase'][:80]}")

    # ── By ERA ───────────────────────────────────────────────────────
    era_hits = defaultdict(list)
    for h in all_hits:
        era_hits[h['era']].append(h)

    print(f"\nBy Era (min 5 tricola):")
    era_rows = []
    for era, hits in era_hits.items():
        if len(hits) < 5:
            continue
        sa = mean([h['s2_a'] for h in hits])
        sb = mean([h['s2_b'] for h in hits])
        sc = mean([h['s2_c'] for h in hits])
        c_max_rate = sum(1 for h in hits if h['s2_c'] > h['s2_a'] and h['s2_c'] > h['s2_b']) / len(hits)
        era_rows.append((era, len(hits), sa, sb, sc, c_max_rate))

    era_rows.sort(key=lambda r: r[4], reverse=True)
    print(f"  {'Era':<20} {'n':>4} {'S2(A)':>7} {'S2(B)':>7} {'S2(C)':>7} {'C-max%':>7}")
    for row in era_rows:
        print(f"  {row[0]:<20} {row[1]:>4} {row[2]:>7.3f} {row[3]:>7.3f} {row[4]:>7.3f} {row[5]*100:>6.0f}%")

    # ── Poems with most tricola ───────────────────────────────────────
    poem_hit_counts.sort(key=lambda r: -r['n_tricola'])
    print(f"\nPoems with most tricola (top 10):")
    for p in poem_hit_counts[:10]:
        print(f"  {p['n_tricola']:>3} | {p['author']} — {p['title'][:50]} ({p['era']})")

    # ── Save results ─────────────────────────────────────────────────
    result = {
        'n_hits': len(all_hits),
        'n_poems': len(poem_hit_counts),
        'overall': {
            'mean_s2_a': mean(s2_a),
            'mean_s2_b': mean(s2_b),
            'mean_s2_c': mean(s2_c),
            'median_s2_a': median(s2_a),
            'median_s2_b': median(s2_b),
            'median_s2_c': median(s2_c),
            'mean_h_a': mean(h_a),
            'mean_h_b': mean(h_b),
            'mean_h_c': mean(h_c),
        },
        'sign_tests': {
            'n': n,
            'c_gt_a_pct': 100 * c_gt_a / n,
            'c_gt_b_pct': 100 * c_gt_b / n,
            'a_max_pct': 100 * a_max / n,
            'b_max_pct': 100 * b_max / n,
            'c_max_pct': 100 * c_max / n,
            'h_c_lt_a_pct': 100 * h_c_lt_a / n,
        },
        'by_era': {
            era: {
                'n': len(hits),
                'mean_s2_a': mean([h['s2_a'] for h in hits]),
                'mean_s2_b': mean([h['s2_b'] for h in hits]),
                'mean_s2_c': mean([h['s2_c'] for h in hits]),
                'c_max_pct': 100 * sum(1 for h in hits if h['s2_c'] > h['s2_a'] and h['s2_c'] > h['s2_b']) / len(hits),
            }
            for era, hits in era_hits.items() if len(hits) >= 5
        },
        'top_tricola': [
            {k: v for k, v in h.items()} for h in top_c
        ],
        'poem_hit_counts': poem_hit_counts[:30],
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to {OUT_PATH}")


if __name__ == '__main__':
    main()
