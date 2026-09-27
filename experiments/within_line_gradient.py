"""
Within-Line Gradient: Where Does Conformity "Kick In"?

Research question: The alternative_landscape_conformity.md analysis showed that
line-final tokens are highly conformist (82.6% chosen from top-10 alternatives)
while line-initial tokens are strongly non-conformist (41.4%). But is the
conformity gradient smooth — a linear increase across the line — or does it
"kick in" abruptly at some position from the end?

Two competing hypotheses:
  A) Smooth gradient: conformity rises continuously from position 0 to end
  B) Threshold effect: conformity is flat for most of the line, then jumps
     sharply in the last 2-3 positions (when rhyme/meter pressure is felt)

Metrics tracked per position (from-start and from-end):
  - avg S2
  - avg entropy H
  - % tokens chosen from top-10 (conformity rate)
  - avg rank of chosen token
  - avg alt_entropy (dispersion of GPT-2's predictions)

Also: breakdown by era to see if threshold position varies with tradition.
"""

import sys
import os
import json
import math
import statistics
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FINDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings")

OUTPUT_JSON = os.path.join(RESULTS_DIR, "within_line_gradient.json")
OUTPUT_MD = os.path.join(FINDINGS_DIR, "within_line_gradient.md")


def alt_entropy(alternatives):
    """Shannon entropy of alternative probability distribution."""
    probs = [a['prob'] for a in alternatives if a['prob'] > 0]
    if not probs:
        return 0.0
    total = sum(probs)
    if total <= 0:
        return 0.0
    normed = [p / total for p in probs]
    return -sum(p * math.log2(p) for p in normed if p > 0)


def chosen_rank_in_alternatives(token_str, alternatives):
    """Return 1-based rank of token_str in alternatives, or None if not found."""
    for i, alt in enumerate(alternatives):
        if alt['token'] == token_str:
            return i + 1
    return None


def parse_lines(tokens):
    """
    Segment tokens into lines, tracking position-from-start and position-from-end
    for each non-newline token.
    Returns list of dicts with extra fields: from_start, from_end
    """
    # First pass: collect line boundaries
    lines = []
    current_line = []

    for tok in tokens:
        if '\n' in tok['token']:
            if current_line:
                lines.append(current_line)
                current_line = []
        else:
            current_line.append(tok)

    if current_line:
        lines.append(current_line)

    # Second pass: annotate each token with positional info
    result = []
    for line in lines:
        n = len(line)
        for i, tok in enumerate(line):
            result.append({
                **tok,
                'from_start': i,
                'from_end': n - 1 - i,
                'line_length': n,
            })

    return result


def is_artifact(tok):
    """Filter out tokens that are likely tokenization artifacts."""
    token_str = tok['token']
    if tok.get('p_newline', 0) > 0.4:
        return True
    if token_str.strip() == '':
        return True
    return False


def conformity_metrics(bucket):
    """Compute conformity metrics for a list of token dicts."""
    if not bucket:
        return None
    s2_vals = [t['s2'] for t in bucket]
    h_vals = [t['entropy'] for t in bucket]
    ae_vals = [alt_entropy(t['alternatives']) for t in bucket if t['alternatives']]
    ranks = [t['rank'] for t in bucket if t['rank'] is not None]
    in_top10 = sum(1 for t in bucket if t['rank'] is not None and t['rank'] <= 10)
    n_ranked = sum(1 for t in bucket if t['rank'] is not None)

    return {
        'n': len(bucket),
        'n_ranked': n_ranked,
        'avg_s2': statistics.mean(s2_vals),
        'avg_h': statistics.mean(h_vals),
        'avg_alt_entropy': statistics.mean(ae_vals) if ae_vals else None,
        'avg_rank': statistics.mean(ranks) if ranks else None,
        'pct_top10': 100 * in_top10 / n_ranked if n_ranked > 0 else None,
    }


def main():
    with open(os.path.join(RESULTS_DIR, 'corpus_results.json')) as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} poems")

    # Collect annotated tokens across corpus
    all_tokens_by_from_start = defaultdict(list)
    all_tokens_by_from_end = defaultdict(list)
    era_tokens_by_from_end = defaultdict(lambda: defaultdict(list))

    # Also track "relative position" (0.0 = start, 1.0 = end) in buckets of 0.1
    relative_buckets = defaultdict(list)

    total_poems = 0
    skipped = 0

    for poem in corpus:
        meta = poem.get('metadata', {})
        era = meta.get('era', 'unknown')
        tokens = poem.get('tokens', [])

        if len(tokens) < 10:
            skipped += 1
            continue

        annotated = parse_lines(tokens)

        for tok in annotated:
            if is_artifact(tok):
                continue
            if not tok['alternatives']:
                continue

            # Limit to lines with at least 2 and at most 15 tokens
            # (avoids single-word lines and very long prose-like lines)
            ll = tok['line_length']
            if ll < 2 or ll > 15:
                continue

            fs = tok['from_start']
            fe = tok['from_end']

            # Relative position in line: 0.0 = start, 1.0 = end
            rel = fs / (ll - 1) if ll > 1 else 0.5
            rel_bucket = round(rel * 10) / 10  # 0.0, 0.1, ..., 1.0

            all_tokens_by_from_start[fs].append(tok)
            all_tokens_by_from_end[fe].append(tok)
            era_tokens_by_from_end[era][fe].append(tok)
            relative_buckets[rel_bucket].append(tok)

        total_poems += 1

    print(f"Analyzed {total_poems} poems, skipped {skipped}")

    # Compute metrics for from-start positions 0–8+
    from_start_results = {}
    for pos in sorted(all_tokens_by_from_start.keys()):
        if pos > 8:
            continue
        m = conformity_metrics(all_tokens_by_from_start[pos])
        if m and m['n'] >= 30:
            from_start_results[pos] = m

    # Compute metrics for from-end positions 0–8+
    from_end_results = {}
    for pos in sorted(all_tokens_by_from_end.keys()):
        if pos > 8:
            continue
        m = conformity_metrics(all_tokens_by_from_end[pos])
        if m and m['n'] >= 30:
            from_end_results[pos] = m

    # Relative position results
    relative_results = {}
    for rb in sorted(relative_buckets.keys()):
        m = conformity_metrics(relative_buckets[rb])
        if m and m['n'] >= 30:
            relative_results[str(rb)] = m

    # Era breakdown: from-end positions 0, 1, 2 (end, second-to-end, third-to-end)
    era_results = {}
    for era, pos_dict in era_tokens_by_from_end.items():
        era_results[era] = {}
        for pos in [0, 1, 2, 3]:
            toks = pos_dict.get(pos, [])
            m = conformity_metrics(toks)
            if m and m['n'] >= 10:
                era_results[era][pos] = m

    # Detect threshold: find the from-end position where conformity jumps most
    from_end_pct = {pos: from_end_results[pos]['pct_top10']
                    for pos in sorted(from_end_results.keys())
                    if from_end_results[pos]['pct_top10'] is not None}

    # Look for biggest jump in consecutive positions (from low end = far from end)
    positions_desc = sorted(from_end_pct.keys(), reverse=True)  # 8,7,6,...,0
    jumps = {}
    for i in range(len(positions_desc) - 1):
        pos_far = positions_desc[i]
        pos_near = positions_desc[i + 1]
        jump = from_end_pct[pos_near] - from_end_pct[pos_far]
        jumps[f"{pos_far}->{pos_near}"] = jump

    output = {
        'from_start': from_start_results,
        'from_end': from_end_results,
        'relative': relative_results,
        'era_from_end': era_results,
        'conformity_jumps': jumps,
    }

    with open(OUTPUT_JSON, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"Results saved to {OUTPUT_JSON}")
    return output


def write_findings(output):
    from_start = output['from_start']
    from_end = output['from_end']
    relative = output['relative']
    era_results = output['era_from_end']
    jumps = output['conformity_jumps']

    lines = []
    lines.append("# Within-Line Gradient: Where Does Conformity Kick In?\n")
    lines.append("**Date:** 2026-09-27  ")
    lines.append("**Experiment:** `experiments/within_line_gradient.py`  ")
    lines.append("**Builds on:** `alternative_landscape_conformity.md`\n")
    lines.append("---\n")
    lines.append("## Research Question\n")
    lines.append(
        "The alternative landscape analysis showed that line-final tokens are highly "
        "conformist (82.6% from top-10 alternatives) while line-initial tokens are "
        "strongly non-conformist (41.4%). This experiment asks: **is this gradient smooth "
        "or does conformity kick in abruptly near line endings?**\n\n"
        "Two hypotheses:\n"
        "- **Smooth gradient**: conformity rises linearly from position 0 to end\n"
        "- **Threshold effect**: conformity is flat for most of the line, then jumps "
        "sharply at the last 2–3 positions when rhyme/meter pressure is felt\n"
    )
    lines.append("---\n")
    lines.append("## From-Start Positions (position 0 = line-initial)\n")
    lines.append("| From-start | n | Avg S₂ | Avg H | % top-10 | Avg rank |")
    lines.append("|---|---|---|---|---|---|")
    for pos in sorted(from_start.keys()):
        m = from_start[pos]
        lines.append(
            f"| {pos} | {m['n']:,} | {m['avg_s2']:.3f} | {m['avg_h']:.3f} | "
            f"{m['pct_top10']:.1f}% | {m['avg_rank']:.2f} |"
        )
    lines.append("")

    lines.append("## From-End Positions (position 0 = line-final)\n")
    lines.append("| From-end | n | Avg S₂ | Avg H | % top-10 | Avg rank |")
    lines.append("|---|---|---|---|---|---|")
    for pos in sorted(from_end.keys()):
        m = from_end[pos]
        lines.append(
            f"| {pos} | {m['n']:,} | {m['avg_s2']:.3f} | {m['avg_h']:.3f} | "
            f"{m['pct_top10']:.1f}% | {m['avg_rank']:.2f} |"
        )
    lines.append("")

    lines.append("## Relative Position (0.0 = line-start, 1.0 = line-end)\n")
    lines.append("| Rel pos | n | Avg S₂ | % top-10 |")
    lines.append("|---|---|---|---|")
    for rb in sorted(relative.keys(), key=float):
        m = relative[rb]
        lines.append(f"| {rb} | {m['n']:,} | {m['avg_s2']:.3f} | {m['pct_top10']:.1f}% |")
    lines.append("")

    lines.append("## Conformity Jumps (step-by-step from far to near line-end)\n")
    lines.append("Positive = conformity increases as we get closer to the end.\n")
    lines.append("| Step | Δ% top-10 |")
    lines.append("|---|---|")
    for step, delta in sorted(jumps.items(), key=lambda x: int(x[0].split('->')[1])):
        lines.append(f"| {step} (from_end {step}) | {delta:+.1f}pp |")
    lines.append("")

    lines.append("## Era Breakdown: % Top-10 by From-End Position\n")
    lines.append("| Era | FE=3 | FE=2 | FE=1 | FE=0 (final) | Δ(0−3) |")
    lines.append("|---|---|---|---|---|---|")
    era_rows = []
    for era, pos_dict in era_results.items():
        fe3 = pos_dict.get(3, {}).get('pct_top10')
        fe2 = pos_dict.get(2, {}).get('pct_top10')
        fe1 = pos_dict.get(1, {}).get('pct_top10')
        fe0 = pos_dict.get(0, {}).get('pct_top10')
        if fe0 is not None and fe3 is not None:
            delta = fe0 - fe3
            era_rows.append((era, fe3, fe2, fe1, fe0, delta))

    era_rows.sort(key=lambda x: -x[5])
    for era, fe3, fe2, fe1, fe0, delta in era_rows:
        fe2_s = f"{fe2:.1f}%" if fe2 is not None else "—"
        fe1_s = f"{fe1:.1f}%" if fe1 is not None else "—"
        lines.append(
            f"| {era} | {fe3:.1f}% | {fe2_s} | {fe1_s} | {fe0:.1f}% | {delta:+.1f}pp |"
        )
    lines.append("")

    # Analysis section
    lines.append("## Analysis\n")

    # Find threshold position
    from_end_top10 = {pos: from_end[pos]['pct_top10']
                      for pos in sorted(from_end.keys())
                      if from_end[pos]['pct_top10'] is not None}

    if from_end_top10:
        max_jump_key = max(jumps, key=lambda k: jumps[k])
        max_jump_val = jumps[max_jump_key]

        # Find total range
        all_vals = list(from_end_top10.values())
        total_range = max(all_vals) - min(all_vals)

        # Check if gradient is smooth or threshold
        # Smooth: all jumps are roughly equal
        # Threshold: one jump dominates
        jump_vals = list(jumps.values())
        if jump_vals:
            max_j = max(abs(v) for v in jump_vals)
            mean_j = statistics.mean(abs(v) for v in jump_vals)
            threshold_ratio = max_j / mean_j if mean_j > 0 else 1

            verdict = "threshold effect" if threshold_ratio > 2.0 else "smooth gradient"
            lines.append(
                f"**Verdict: {verdict.upper()}** "
                f"(max jump = {max_j:.1f}pp, mean jump = {mean_j:.1f}pp, ratio = {threshold_ratio:.1f}x)\n"
            )
            lines.append(
                f"The largest single conformity increase occurs at step **{max_jump_key}** "
                f"({max_jump_val:+.1f}pp). "
                f"The total conformity range across the line is {total_range:.1f}pp.\n"
            )

    lines.append("---\n")
    lines.append("## Suggested Next Steps\n")
    lines.append(
        "1. **Rhymed vs. free verse split**: Does the threshold position differ between "
        "rhymed poems (where end-pressure is phonetic) and free verse (where it may be "
        "purely syntactic)?\n"
        "2. **Line-length interaction**: Does the threshold position scale with line length "
        "or stay fixed (e.g., always at from_end=1 regardless of line length)?\n"
        "3. **Token type at threshold**: What kinds of tokens occupy the threshold position? "
        "Are they adjectives (pre-nominal) or prepositions (pre-object)?\n"
    )

    with open(OUTPUT_MD, 'w') as f:
        f.write('\n'.join(lines))
    print(f"Findings written to {OUTPUT_MD}")


if __name__ == '__main__':
    output = main()
    write_findings(output)
    print("\n=== KEY RESULTS ===")
    print("\nFrom-End conformity (% top-10):")
    for pos in sorted(output['from_end'].keys()):
        m = output['from_end'][pos]
        if m['pct_top10']:
            print(f"  from_end={pos}: {m['pct_top10']:.1f}% (n={m['n']})")
    print("\nConformity jumps (far->near end):")
    for step, delta in sorted(output['conformity_jumps'].items(), key=lambda x: int(x[0].split('->')[1])):
        print(f"  {step}: {delta:+.1f}pp")
