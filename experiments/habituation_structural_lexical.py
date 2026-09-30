"""
Experiment: Separating Structural vs. Lexical Habituation

The two-factor model from second_occurrence_dip.md proposes:
  S2(word, n) ≈ S2_structural(position) + S2_lexical(word) - habituation(n)

If structural position drives habituation, then words that appear at the SAME
structural position on both occurrences should show LESS habituation than words
that appear at DIFFERENT positions.

Method:
- For each word appearing exactly twice in a poem, classify both positions as:
  LINE_START (previous token is newline), LINE_END (next token is newline), or MEDIAL
- Compare S2 change by same-position vs. different-position pairs
- Also test: for words at line-start BOTH times, does habituation vanish?
"""

import json
import re
import statistics
from collections import defaultdict, Counter

def get_position_type(tokens, idx):
    """Classify token position as LINE_START, LINE_END, or MEDIAL."""
    is_line_start = idx > 0 and tokens[idx - 1]['token'] == '\n'
    is_line_end = idx + 1 < len(tokens) and tokens[idx + 1]['token'] == '\n'
    if is_line_start:
        return 'LINE_START'
    elif is_line_end:
        return 'LINE_END'
    else:
        return 'MEDIAL'

def normalize_token(tok):
    """Lowercase and strip whitespace for word-level matching."""
    return tok.strip().lower()

def is_content_word(tok):
    """Simple heuristic: content words are alpha, len > 2, not in stoplist."""
    stopwords = {
        'the', 'and', 'of', 'to', 'in', 'is', 'it', 'as', 'at', 'be', 'by',
        'or', 'an', 'on', 'for', 'with', 'not', 'but', 'so', 'if', 'do',
        'he', 'she', 'we', 'i', 'my', 'his', 'her', 'our', 'their', 'its',
        'that', 'this', 'was', 'are', 'has', 'had', 'have', 'were', 'been',
        'from', 'all', 'me', 'him', 'them', 'you', 'your', 'who', 'what',
        'when', 'where', 'which', 'how', 'may', 'can', 'will', 'would',
        'could', 'should', 'shall', 'did', 'does', 'more', 'into'
    }
    cleaned = tok.strip().lower().strip("'\".,!?;:-")
    return len(cleaned) > 2 and cleaned.isalpha() and cleaned not in stopwords

def main():
    with open('results/corpus_results.json') as f:
        data = json.load(f)

    # Filter to English poetry (exclude prose controls)
    poems = [p for p in data if p['metadata'].get('era', '') not in ('control',)]
    print(f"Analyzing {len(poems)} poems...")

    # Collect all pairs: (S2_first, S2_second, pos_first, pos_second, word, era, p_newline)
    pairs = []
    # Also track n>2 occurrences for curve fitting
    multi_occur = defaultdict(list)  # (poem_idx, word) -> list of (s2, position_type)

    for poem_idx, poem in enumerate(poems):
        tokens = poem['tokens']
        era = poem['metadata'].get('era', 'unknown')

        # Filter artifact tokens
        clean_tokens = []
        for tok in tokens:
            if tok.get('p_newline', 0) < 0.9:
                clean_tokens.append(tok)

        # Track word occurrences
        word_occurrences = defaultdict(list)  # word -> list of (token_dict, position_type)

        for idx, tok in enumerate(tokens):
            if tok.get('p_newline', 0) >= 0.9:
                continue
            word = normalize_token(tok['token'])
            if not word or not any(c.isalpha() for c in word):
                continue
            pos_type = get_position_type(tokens, idx)
            word_occurrences[word].append((tok, pos_type))

        # Collect pairs (2 occurrences) and multi-occurrences
        for word, occurs in word_occurrences.items():
            if len(occurs) == 2:
                tok1, pos1 = occurs[0]
                tok2, pos2 = occurs[1]
                pairs.append({
                    'word': word,
                    'era': era,
                    's2_1': tok1['s2'],
                    's2_2': tok2['s2'],
                    'pos_1': pos1,
                    'pos_2': pos2,
                    'is_content': is_content_word(word),
                    'delta': tok2['s2'] - tok1['s2'],
                })
            if len(occurs) >= 3:
                for n, (tok, pos_type) in enumerate(occurs):
                    key = (poem_idx, word)
                    multi_occur[key].append({'n': n+1, 's2': tok['s2'], 'pos': pos_type, 'era': era})

    print(f"\nTotal 2-occurrence pairs: {len(pairs)}")

    # --- Analysis 1: Same vs. Different Structural Position ---
    def categorize_pair(p):
        p1, p2 = p['pos_1'], p['pos_2']
        if p1 == p2:
            return f"SAME_{p1}"
        else:
            return f"{p1}_to_{p2}"

    cats = Counter(categorize_pair(p) for p in pairs)
    print("\n--- Pair count by position category ---")
    for cat, n in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {n}")

    # Aggregate by position category
    cat_data = defaultdict(list)
    for p in pairs:
        cat = categorize_pair(p)
        cat_data[cat].append(p['delta'])

    print("\n--- Mean S2 change by position transition ---")
    print(f"{'Category':<30} {'N':>5} {'Mean Δ':>8} {'Median Δ':>9} {'% falls':>8}")
    for cat in sorted(cat_data, key=lambda c: statistics.mean(cat_data[c])):
        vals = cat_data[cat]
        if len(vals) < 5:
            continue
        mean_d = statistics.mean(vals)
        median_d = statistics.median(vals)
        pct_fall = 100 * sum(1 for v in vals if v < 0) / len(vals)
        print(f"  {cat:<28} {len(vals):>5} {mean_d:>+8.2f} {median_d:>+9.2f} {pct_fall:>7.1f}%")

    # --- Analysis 2: The key test ---
    # Compare same-LINE_START pairs vs. same-MEDIAL pairs
    print("\n--- KEY TEST: Same structural position pairs ---")
    same_start = [p for p in pairs if p['pos_1'] == 'LINE_START' and p['pos_2'] == 'LINE_START']
    same_end = [p for p in pairs if p['pos_1'] == 'LINE_END' and p['pos_2'] == 'LINE_END']
    same_medial = [p for p in pairs if p['pos_1'] == 'MEDIAL' and p['pos_2'] == 'MEDIAL']
    diff_all = [p for p in pairs if p['pos_1'] != p['pos_2']]

    for label, group in [
        ("Same LINE_START", same_start),
        ("Same LINE_END", same_end),
        ("Same MEDIAL", same_medial),
        ("Different positions (all)", diff_all),
    ]:
        if len(group) < 5:
            continue
        deltas = [p['delta'] for p in group]
        s2_1 = [p['s2_1'] for p in group]
        s2_2 = [p['s2_2'] for p in group]
        mean_d = statistics.mean(deltas)
        pct_fall = 100 * sum(1 for v in deltas if v < 0) / len(deltas)
        print(f"\n  {label} (n={len(group)}):")
        print(f"    Mean S2 1st:  {statistics.mean(s2_1):+.3f}")
        print(f"    Mean S2 2nd:  {statistics.mean(s2_2):+.3f}")
        print(f"    Mean Δ:       {mean_d:+.3f}")
        print(f"    % fall:       {pct_fall:.1f}%")

    # --- Analysis 3: Content words vs. function words ---
    print("\n--- Content vs. function word habituation ---")
    content_same_start = [p for p in same_start if p['is_content']]
    func_same_start = [p for p in same_start if not p['is_content']]
    content_diff = [p for p in diff_all if p['is_content']]

    for label, group in [
        ("Content word, same LINE_START", content_same_start),
        ("Function word, same LINE_START", func_same_start),
        ("Content word, different positions", content_diff),
    ]:
        if len(group) < 3:
            continue
        deltas = [p['delta'] for p in group]
        mean_d = statistics.mean(deltas)
        pct_fall = 100 * sum(1 for v in deltas if v < 0) / len(deltas)
        print(f"  {label} (n={len(group)}): mean Δ = {mean_d:+.2f}, {pct_fall:.0f}% fall")

    # --- Analysis 4: Multi-occurrence decay curve (N=1..6) ---
    print("\n--- Multi-occurrence decay curve (N≥3) ---")
    by_n = defaultdict(list)
    for key, occurrences in multi_occur.items():
        # Only include words appearing at line-start EVERY time (pure structural)
        if all(o['pos'] == 'LINE_START' for o in occurrences):
            for o in occurrences:
                by_n[o['n']].append(o['s2'])
        # And separately: non-line-start every time
        elif all(o['pos'] == 'MEDIAL' for o in occurrences):
            for o in occurrences:
                by_n[-(o['n'])].append(o['s2'])  # negative key for medial

    print(f"\n{'Occ N':<8} {'Group':<22} {'n':>5} {'Mean S2':>8} {'% pos':>6}")
    for n_key in sorted(set(list(by_n.keys()))):
        vals = by_n[n_key]
        if len(vals) < 3:
            continue
        group = 'Always LINE_START' if n_key > 0 else 'Always MEDIAL'
        n_display = abs(n_key)
        mean_s2 = statistics.mean(vals)
        pct_pos = 100 * sum(1 for v in vals if v > 0) / len(vals)
        print(f"  N={n_display:<5}  {group:<22} {len(vals):>5} {mean_s2:>+8.2f} {pct_pos:>5.1f}%")

    # --- Analysis 5: Era-level habituation at same-position pairs ---
    print("\n--- Era-level same-position habituation (LINE_START to LINE_START) ---")
    era_same = defaultdict(list)
    for p in same_start:
        era_same[p['era']].append(p['delta'])

    era_rows = []
    for era, deltas in era_same.items():
        if len(deltas) < 3:
            continue
        era_rows.append((era, len(deltas), statistics.mean(deltas),
                         100 * sum(1 for v in deltas if v < 0) / len(deltas)))
    era_rows.sort(key=lambda x: x[2])
    print(f"\n{'Era':<22} {'N':>4} {'Mean Δ':>8} {'% falls':>8}")
    for era, n, mean_d, pct_fall in era_rows:
        print(f"  {era:<22} {n:>4} {mean_d:>+8.2f} {pct_fall:>7.1f}%")

    # --- Summary ---
    print("\n=== SUMMARY ===")
    if same_start and diff_all:
        d_same = statistics.mean([p['delta'] for p in same_start])
        d_diff = statistics.mean([p['delta'] for p in diff_all])
        print(f"  Same LINE_START habituation: {d_same:+.3f} bits")
        print(f"  Different positions change:  {d_diff:+.3f} bits")
        ratio = d_same / d_diff if d_diff != 0 else float('inf')
        print(f"  Ratio (same/diff):           {ratio:.2f}")
        print()
        if abs(d_same) < abs(d_diff) * 0.7:
            print("  FINDING: Same-position habituation is substantially weaker → structural position explains most habituation")
        elif abs(d_same) > abs(d_diff) * 0.7:
            print("  FINDING: Same-position pairs still show strong habituation → lexical/semantic habituation is real")


if __name__ == '__main__':
    main()
