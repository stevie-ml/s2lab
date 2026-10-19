"""
Sentence-level surprise position: do poets back-load their surprises?

Within a sentence, is the peak S2 token in the first half or second half?
Do poets systematically end-weight their surprises, compared to prose?

Hypothesis: Poetry back-loads surprise (peak S2 falls in second half of sentence)
more often than prose, reflecting the grammatical-end effect — the noun/adjective
at the end of an English clause lands harder.
"""

import json
import os
import re
from statistics import mean, median, stdev

RESULTS_FILE = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")

SENTENCE_END_RE = re.compile(r'[.?!;]$')
NEWLINE_CLEAN_THRESH = 0.9  # exclude stanza-break artifacts


def split_sentences(tokens):
    """
    Split a token list into sentences using terminal punctuation.
    Returns list of lists; each inner list is one sentence's tokens.
    Excludes newline-artifact tokens (p_newline >= threshold).
    """
    # First filter: remove high-p_newline artifact tokens
    clean = [t for t in tokens if t.get('p_newline', 0) < NEWLINE_CLEAN_THRESH]

    sentences = []
    current = []
    for tok in clean:
        current.append(tok)
        text = tok['token'].strip()
        if SENTENCE_END_RE.search(text):
            if len(current) >= 4:
                sentences.append(current)
            current = []

    if len(current) >= 4:
        sentences.append(current)

    return sentences


def sentence_peak_position(sentence_tokens):
    """
    Return the relative position (0..1) of the peak-S2 token in the sentence.
    0 = first token, 1 = last token.
    """
    s2_vals = [t['s2'] for t in sentence_tokens]
    peak_idx = s2_vals.index(max(s2_vals))
    return peak_idx / (len(sentence_tokens) - 1)


def is_back_loaded(sentence_tokens):
    """Peak S2 in the second half of the sentence."""
    return sentence_peak_position(sentence_tokens) >= 0.5


def avg_sentence_s2(sentence_tokens):
    return mean(t['s2'] for t in sentence_tokens)


def main():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    era_stats = {}   # era -> {sentences, back_count, positions, avg_s2}
    control_positions = []
    poetry_positions = []
    back_by_era = {}

    for poem in data:
        meta = poem['metadata']
        era = meta.get('era', 'unknown')
        tokens = poem['tokens']

        sentences = split_sentences(tokens)
        if not sentences:
            continue

        is_control = (era == 'control')

        for sent in sentences:
            pos = sentence_peak_position(sent)
            if is_control:
                control_positions.append(pos)
            else:
                poetry_positions.append(pos)

            if era not in era_stats:
                era_stats[era] = {'n_sentences': 0, 'back_count': 0,
                                  'positions': [], 'avg_s2_values': []}
            era_stats[era]['n_sentences'] += 1
            era_stats[era]['positions'].append(pos)
            era_stats[era]['avg_s2_values'].append(avg_sentence_s2(sent))
            if pos >= 0.5:
                era_stats[era]['back_count'] += 1

    # Summary
    def pct_back(positions):
        return 100 * sum(1 for p in positions if p >= 0.5) / len(positions) if positions else 0

    print("\n=== SENTENCE SURPRISE POSITION ANALYSIS ===\n")
    print(f"Total poetry sentences: {len(poetry_positions)}")
    print(f"Total prose sentences: {len(control_positions)}")
    if poetry_positions:
        print(f"Poetry: peak S2 in 2nd half = {pct_back(poetry_positions):.1f}%")
        print(f"Poetry: mean peak position = {mean(poetry_positions):.3f} (0=front, 1=back)")
    if control_positions:
        print(f"Prose:  peak S2 in 2nd half = {pct_back(control_positions):.1f}%")
        print(f"Prose:  mean peak position = {mean(control_positions):.3f}")
    print()

    # Sort eras by back-loading rate
    era_rows = []
    for era, stats in era_stats.items():
        n = stats['n_sentences']
        if n < 5:
            continue
        back_pct = 100 * stats['back_count'] / n
        mean_pos = mean(stats['positions'])
        mean_s2 = mean(stats['avg_s2_values'])
        era_rows.append((era, n, back_pct, mean_pos, mean_s2))

    era_rows.sort(key=lambda x: -x[2])  # sort by back-loading %

    print("Era breakdown (sorted by % back-loaded, min 5 sentences):")
    print(f"{'Era':<25} {'N':>5} {'%Back':>7} {'MeanPos':>8} {'AvgS2':>7}")
    print("-" * 55)
    for era, n, back_pct, mean_pos, mean_s2 in era_rows:
        print(f"{era:<25} {n:>5} {back_pct:>6.1f}% {mean_pos:>8.3f} {mean_s2:>7.3f}")

    # Build results dict for JSON export
    results = {
        'summary': {
            'poetry_n': len(poetry_positions),
            'prose_n': len(control_positions),
            'poetry_back_pct': round(pct_back(poetry_positions), 2) if poetry_positions else 0,
            'prose_back_pct': round(pct_back(control_positions), 2) if control_positions else 0,
            'poetry_mean_pos': round(mean(poetry_positions), 4) if poetry_positions else 0,
            'prose_mean_pos': round(mean(control_positions), 4) if control_positions else 0,
        },
        'by_era': {
            era: {
                'n_sentences': n,
                'back_pct': round(back_pct, 2),
                'mean_peak_pos': round(mean_pos, 4),
                'avg_s2': round(mean_s2, 4),
            }
            for era, n, back_pct, mean_pos, mean_s2 in era_rows
        }
    }

    out_path = os.path.join(os.path.dirname(__file__), "..", "results",
                            "sentence_surprise_position.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {out_path}")
    return results


if __name__ == "__main__":
    main()
