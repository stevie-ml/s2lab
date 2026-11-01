"""
Sentence Length and S₂ Correlation
====================================
Date: 2026-11-01

Motivation: The Ashbery Paradox (findings/new_york_school_s2.md) found that
Ashbery's "architectural difficulty" (syntactic complexity, long sentences)
does NOT produce high token-level S₂. His difficulty is built from ordinary
bricks. This experiment tests the hypothesis more systematically:

HYPOTHESIS: Longer sentences produce LOWER per-token S₂, because as a sentence
grows, the conditioning context becomes more specific, narrowing GPT-2's
probability distribution and making each successive token more predictable.

This would mean: syntactic complexity and lexical surprise are inversely related
-- the poet's choice to use architecture (long sentences) as the vehicle for
difficulty is, in information-theoretic terms, a surprise-DAMPENING move.

We also test: is there a 'sweet spot' sentence length that maximizes S₂? Or is
the relationship monotone?

Method:
1. Load corpus_results.json
2. For each poem, re-parse the original text into sentences (split by .!?)
3. Map each token to its sentence
4. Compute per-sentence avg S₂ and sentence length
5. Run correlation analysis
6. Break down by era and poet
"""

import json
import re
import numpy as np
from pathlib import Path
from collections import defaultdict

RESULTS_FILE = Path(__file__).parent.parent / "results" / "corpus_results.json"
FINDINGS_DIR = Path(__file__).parent.parent / "findings"


def split_sentences(text):
    """Split text into sentences by . ! ? ; — treat each as a unit."""
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?;]+', text)
    return [s.strip() for s in sentences if len(s.strip()) > 3]


def count_words(sentence):
    return len(sentence.split())


def get_sentence_for_position(text, token_offset_chars):
    """Get which sentence (by index) a character position falls in."""
    sentences = split_sentences(text)
    pos = 0
    for i, sent in enumerate(sentences):
        # find position in text
        start = text.find(sent, pos)
        if start == -1:
            continue
        end = start + len(sent)
        if start <= token_offset_chars < end:
            return i, len(sentences[i].split())
        pos = start
    return None, None


def analyze():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    # Remove stanza-break artifact tokens
    def is_artifact(token_text):
        return token_text.strip() == '' or token_text == '\n' or token_text == 'Ċ'

    # Collect sentence-level data
    # For each poem: map sentences to avg S2 and sentence word count
    poem_sentence_data = []  # list of (poem_id, sentence_idx, sent_word_count, tokens_in_sent)

    # Also collect raw token data with estimated sentence membership
    # Strategy: reconstruct sentences from token texts, track position
    all_obs = []  # (poem_title, era, author, sent_len_words, token_s2)

    for poem in data:
        meta = poem['metadata']
        tokens = poem['tokens']

        if not tokens:
            continue

        # Rebuild text from tokens to track sentence boundaries
        token_texts = [t['token'] for t in tokens]

        # Simple sentence segmentation on token stream:
        # A new sentence starts after: '.', '!', '?', '\n\n' (paragraph), or ';'
        # We'll track sentence length in tokens (not words) for this experiment

        current_sentence_tokens = []
        sentence_s2_values = []
        sentences_in_poem = []

        for t in tokens:
            token_text = t['token']
            s2 = t.get('s2', 0) or 0
            is_art = is_artifact(token_text)

            # Sentence terminators
            is_sentence_end = any(c in token_text for c in ['.', '!', '?'])
            is_para_break = '\n\n' in token_text or (token_text.strip() == '' and '\n' in token_text)

            if not is_art:
                current_sentence_tokens.append(s2)

            if (is_sentence_end or is_para_break) and current_sentence_tokens:
                sentence_s2_values.append(np.mean(current_sentence_tokens))
                sentences_in_poem.append(len(current_sentence_tokens))
                current_sentence_tokens = []

        # Flush remaining
        if current_sentence_tokens:
            sentence_s2_values.append(np.mean(current_sentence_tokens))
            sentences_in_poem.append(len(current_sentence_tokens))

        # Record per-sentence observations
        for sent_len, sent_s2 in zip(sentences_in_poem, sentence_s2_values):
            all_obs.append({
                'title': meta.get('title', '?'),
                'author': meta.get('author', '?'),
                'era': meta.get('era', '?'),
                'sent_len': sent_len,
                'sent_s2': sent_s2,
            })

    # Global correlation
    lens = np.array([o['sent_len'] for o in all_obs])
    s2s = np.array([o['sent_s2'] for o in all_obs])

    # Filter: only sentences with 2-80 tokens (avoid outliers)
    mask = (lens >= 2) & (lens <= 80)
    lens_f = lens[mask]
    s2s_f = s2s[mask]

    from scipy import stats
    r, p = stats.pearsonr(lens_f, s2s_f)
    rho, p_rho = stats.spearmanr(lens_f, s2s_f)

    print(f"Global correlation (n={len(lens_f)} sentences, 2-80 tokens):")
    print(f"  Pearson r = {r:.4f} (p={p:.4g})")
    print(f"  Spearman ρ = {rho:.4f} (p={p_rho:.4g})")

    # Bin analysis — sweet spot?
    bins = [1, 2, 3, 5, 8, 13, 21, 34, 55, 80]
    print(f"\nS₂ by sentence length bin:")
    print(f"{'Bin (tokens)':20s} {'n':>6} {'avg S₂':>10} {'std':>8}")
    bin_data = []
    for i in range(len(bins)-1):
        lo, hi = bins[i], bins[i+1]
        m = (lens >= lo) & (lens < hi)
        if m.sum() > 5:
            avg = s2s[m].mean()
            std = s2s[m].std()
            print(f"  {lo:2d}–{hi-1:2d} tokens         {m.sum():6d} {avg:10.4f} {std:8.4f}")
            bin_data.append({'lo': lo, 'hi': hi, 'n': int(m.sum()), 'avg_s2': float(avg), 'std': float(std)})

    # Era breakdown — avg sentence length vs avg S2
    print(f"\nEra-level: avg sentence length vs avg S₂")
    era_data = defaultdict(list)
    for o in all_obs:
        era_data[o['era']].append(o)

    era_rows = []
    for era, obs in sorted(era_data.items(), key=lambda x: -len(x[1])):
        if len(obs) < 10:
            continue
        era_lens = np.array([o['sent_len'] for o in obs])
        era_s2 = np.array([o['sent_s2'] for o in obs])
        m = (era_lens >= 2) & (era_lens <= 80)
        if m.sum() < 10:
            continue
        row = {
            'era': era,
            'n_sentences': int(m.sum()),
            'avg_sent_len': float(era_lens[m].mean()),
            'avg_s2': float(era_s2[m].mean()),
        }
        era_rows.append(row)
        print(f"  {era:25s} n={m.sum():4d} avgLen={era_lens[m].mean():5.1f} avgS2={era_s2[m].mean():+.3f}")

    # Poet-level for NYS poets (Ashbery focus)
    print(f"\nNYS poets: sentence length vs S₂")
    nys_poets = ['John Ashbery', 'Frank O\'Hara', 'Kenneth Koch', 'Barbara Guest',
                 'James Schuyler', 'Anne Waldman', 'Ted Berrigan']
    for poet in nys_poets:
        obs = [o for o in all_obs if o['author'] == poet]
        if not obs:
            continue
        poet_lens = np.array([o['sent_len'] for o in obs])
        poet_s2 = np.array([o['sent_s2'] for o in obs])
        print(f"  {poet:20s} n={len(obs):4d} avgLen={poet_lens.mean():5.1f} avgS2={poet_s2.mean():+.3f}")

    # Save JSON output
    output = {
        'global_correlation': {
            'pearson_r': float(r),
            'pearson_p': float(p),
            'spearman_rho': float(rho),
            'spearman_p': float(p_rho),
            'n_sentences': int(len(lens_f)),
        },
        'bins': bin_data,
        'eras': era_rows,
    }
    out_path = FINDINGS_DIR / 'sentence_length_s2.json'
    with open(out_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved: {out_path}")
    return output


if __name__ == '__main__':
    try:
        from scipy import stats
    except ImportError:
        import subprocess
        subprocess.run(['pip', 'install', 'scipy', '-q'])
        from scipy import stats
    analyze()
