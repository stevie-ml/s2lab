"""
Sentence-boundary position analysis.

Research question: Do nouns, verbs, and other content words have systematically different
S2 values depending on whether they occur at sentence-initial, sentence-final, or
sentence-medial positions? And does this interact with line-breaks (enjambment)?

Method:
- Use punctuation tokens to detect sentence boundaries (no NLTK needed)
- Sentence-enders: tokens whose stripped form ends in '.', '!', '?'
  (also ';' for major clause breaks, treated separately)
- Sentence-initial: first content token after a sentence-ender
- Sentence-final: last content token before a sentence-ender
- Sentence-medial: everything else
- Apply p_newline < 0.9 filter to avoid stanza-break artifact
- Compare poetry vs prose; break down by era

Additional analysis:
- Enjambment detection: a sentence is "enjambed" if its initial token is NOT
  line-initial (i.e., the sentence continues across a line boundary)
  → Proxy: sentence-initial token does NOT immediately follow a newline token
"""
import json
import statistics

SENTENCE_ENDERS = set(['.', '!', '?'])
CLAUSE_ENDERS = set([';', ':'])

def stripped(tok):
    return tok.strip()

def is_sentence_end(tok):
    s = stripped(tok)
    return s in SENTENCE_ENDERS or (len(s) > 1 and s[-1] in SENTENCE_ENDERS)

def is_clause_end(tok):
    s = stripped(tok)
    return s in CLAUSE_ENDERS

def is_newline(tok):
    return stripped(tok) == '' or tok == '\n'

def is_punct(tok):
    s = stripped(tok)
    return s in set(['.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '-', '--',
                     '...', '——', '—', '/', '\\', '[', ']', '{', '}', '"', '"', ''', '''])

def analyze_poem(tokens, is_prose=False):
    """
    Categorize each token by sentence position.
    Returns list of (category, s2, p_newline, is_prose) tuples.
    """
    results = []
    n = len(tokens)

    # Build sentence-position labels
    # First pass: label each token's position
    prev_was_sentence_end = False
    prev_was_newline = False
    prev_was_clause_end = False

    for i, t in enumerate(tokens):
        tok = t['token']
        s2 = t['s2']
        p_nl = t['p_newline']

        # Determine position category
        if is_sentence_end(tok) or is_clause_end(tok) or is_newline(tok) or is_punct(tok):
            # Update state flags
            if is_sentence_end(tok):
                prev_was_sentence_end = True
                prev_was_clause_end = False
            elif is_clause_end(tok):
                prev_was_clause_end = True
            if is_newline(tok):
                prev_was_newline = True
            # Skip punctuation tokens themselves for position analysis
            continue

        # This is a content/function token
        if prev_was_sentence_end:
            pos = 'sentence_initial'
        elif prev_was_clause_end:
            pos = 'clause_initial'
        else:
            # Check if next non-punct token is sentence-ender
            # Look ahead
            is_sent_final = False
            is_clause_final = False
            for j in range(i + 1, min(i + 5, n)):
                next_tok = tokens[j]['token']
                if is_newline(next_tok):
                    continue
                if is_sentence_end(next_tok):
                    is_sent_final = True
                    break
                elif is_clause_end(next_tok):
                    is_clause_final = True
                    break
                elif not is_punct(next_tok):
                    break

            if is_sent_final:
                pos = 'sentence_final'
            elif is_clause_final:
                pos = 'clause_final'
            else:
                pos = 'sentence_medial'

        # Record result with enjambment info
        # A sentence-initial token that follows a newline is "line-initial"
        # A sentence-initial token that does NOT follow a newline is "enjambed" (sentence continues across line break)
        enjamb = None
        if pos == 'sentence_initial':
            enjamb = 'enjambed' if not prev_was_newline else 'end_stopped'

        results.append({
            'position': pos,
            's2': s2,
            'p_newline': p_nl,
            'enjamb': enjamb,
            'is_prose': is_prose,
            'token': tok,
        })

        # Reset state
        prev_was_sentence_end = False
        prev_was_clause_end = False
        if is_newline(tok):
            prev_was_newline = True
        else:
            prev_was_newline = False

    return results


def compute_stats(values):
    if not values:
        return {'n': 0, 'mean': None, 'median': None, 'std': None}
    n = len(values)
    mean = sum(values) / n
    med = statistics.median(values)
    std = statistics.stdev(values) if n > 1 else 0
    return {'n': n, 'mean': round(mean, 4), 'median': round(med, 4), 'std': round(std, 4)}


def main():
    with open('results/corpus_results.json') as f:
        data = json.load(f)

    all_results = []
    era_results = {}

    for item in data:
        meta = item['metadata']
        is_prose = meta.get('era') == 'control'
        era = meta.get('era', 'unknown')
        lang = meta.get('language', 'en')

        # Only English for consistency
        if lang != 'en':
            continue

        poem_results = analyze_poem(item['tokens'], is_prose=is_prose)
        for r in poem_results:
            r['era'] = era
        all_results.extend(poem_results)

        if era not in era_results:
            era_results[era] = []
        era_results[era].extend(poem_results)

    # --- Global analysis: by position, with and without p_newline filter ---

    positions = ['sentence_initial', 'sentence_final', 'sentence_medial', 'clause_initial', 'clause_final']

    global_stats = {}
    for pos in positions:
        # Raw
        raw_vals = [r['s2'] for r in all_results if r['position'] == pos]
        # Clean (p_newline < 0.9)
        clean_vals = [r['s2'] for r in all_results if r['position'] == pos and r['p_newline'] < 0.9]
        # Poetry only (clean)
        poetry_clean = [r['s2'] for r in all_results if r['position'] == pos and r['p_newline'] < 0.9 and not r['is_prose']]
        # Prose only (clean)
        prose_clean = [r['s2'] for r in all_results if r['position'] == pos and r['p_newline'] < 0.9 and r['is_prose']]

        global_stats[pos] = {
            'raw': compute_stats(raw_vals),
            'clean': compute_stats(clean_vals),
            'poetry_clean': compute_stats(poetry_clean),
            'prose_clean': compute_stats(prose_clean),
        }

    # --- Enjambment analysis ---

    enjamb_results = {}
    for ej in ['enjambed', 'end_stopped']:
        vals = [r['s2'] for r in all_results if r['enjamb'] == ej and r['p_newline'] < 0.9 and not r['is_prose']]
        enjamb_results[ej] = compute_stats(vals)

    # --- Era breakdown (clean) ---

    era_stats = {}
    for era, results in era_results.items():
        pos_stats = {}
        for pos in ['sentence_initial', 'sentence_final', 'sentence_medial']:
            vals = [r['s2'] for r in results if r['position'] == pos and r['p_newline'] < 0.9]
            pos_stats[pos] = compute_stats(vals)
        era_stats[era] = pos_stats

    # --- Top-word analysis: what do sentence-initial positions look like? ---
    # Most common first tokens after sentence breaks
    si_tokens = {}
    for r in all_results:
        if r['position'] == 'sentence_initial' and r['p_newline'] < 0.9 and not r['is_prose']:
            tok = r['token'].strip().lower()
            if tok not in si_tokens:
                si_tokens[tok] = {'count': 0, 's2_sum': 0, 's2_vals': []}
            si_tokens[tok]['count'] += 1
            si_tokens[tok]['s2_sum'] += r['s2']
            si_tokens[tok]['s2_vals'].append(r['s2'])

    # Sort by count
    top_si_tokens = sorted(si_tokens.items(), key=lambda x: -x[1]['count'])[:25]
    top_si_with_stats = [(tok, d['count'], round(d['s2_sum']/d['count'], 3)) for tok, d in top_si_tokens]

    # High-S2 sentence-initial tokens
    high_s2_si = [(r['token'].strip(), r['s2'], r['era']) for r in all_results
                   if r['position'] == 'sentence_initial' and r['p_newline'] < 0.9
                   and not r['is_prose'] and r['s2'] > 5.0]
    high_s2_si.sort(key=lambda x: -x[1])

    output = {
        'global_stats': global_stats,
        'enjambment': enjamb_results,
        'era_stats': era_stats,
        'top_sentence_initial_tokens': top_si_with_stats[:25],
        'high_s2_sentence_initial': high_s2_si[:20],
    }

    with open('results/sentence_boundary_s2.json', 'w') as f:
        json.dump(output, f, indent=2)

    print("Done. Results saved to results/sentence_boundary_s2.json")

    # Print summary
    print("\n=== SENTENCE POSITION S2 (artifact-free) ===\n")
    print(f"{'Position':<20} {'Poetry n':>10} {'Poetry mean S2':>15} {'Prose mean S2':>14} {'Δ':>8}")
    print("-" * 70)
    for pos in positions:
        ps = global_stats[pos]['poetry_clean']
        pr = global_stats[pos]['prose_clean']
        pn = ps['n']
        pm = ps['mean'] if ps['mean'] is not None else 'N/A'
        prm = pr['mean'] if pr['mean'] is not None else 'N/A'
        delta = round(pm - prm, 4) if isinstance(pm, float) and isinstance(prm, float) else 'N/A'
        print(f"  {pos:<20} {pn:>10} {pm!s:>15} {prm!s:>14} {delta!s:>8}")

    print("\n=== ENJAMBMENT ANALYSIS (poetry, clean) ===\n")
    for ej, stats in enjamb_results.items():
        print(f"  {ej}: n={stats['n']}, mean S2={stats['mean']}")

    print("\n=== TOP SENTENCE-INITIAL TOKENS (poetry) ===\n")
    for tok, count, avg_s2 in top_si_with_stats[:15]:
        print(f"  '{tok}': count={count}, avg_s2={avg_s2}")


if __name__ == '__main__':
    main()
