"""
Line-Number S₂ Profile: How prior-line context shapes expectation at each new line.

The opening_salvo.py looked at absolute token position (0, 1, 2...) and found that
GPT-2 faces maximum entropy at position 0 (no context). This experiment looks at a
different structural dimension: the LINE NUMBER within the poem.

Questions:
  1. Does the first token of line 2 differ from the first token of line 1? (Line 1
     has just established the poem's "world" — does this help or hurt surprise at line 2?)
  2. Does each successive line's first token become progressively less surprising as
     context accumulates?
  3. At what line number does the "Straussian window" close — i.e., where does the
     first-token S₂ stabilize?
  4. Does the S₂ trajectory by line number differ across poetic eras?

Key distinction from opening_salvo.py: that experiment tracked ABSOLUTE TOKEN POSITION
(position 0, 1, 2 from the start of the poem). This experiment tracks LINE NUMBER —
regardless of how many tokens each line contains, we compare the first token of
line 1 vs. line 2 vs. line 3, etc. A 3-word line and a 10-word line both contribute
one data point per line to this analysis.

Hypothesis:
  - Line 1 first token: high entropy (near cold-start), moderate positive S₂
  - Line 2 first token: HIGHEST S₂ — model has crystallized a prediction from line 1
    and the poet most violates it here
  - Lines 3-5: S₂ declining as context builds
  - Lines 6+: S₂ asymptotes to the poem's baseline
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/line_number_profile.json"
P_NEWLINE_MAX = 0.9     # artifact filter threshold
MIN_CLEAN_LINES = 4     # minimum lines with clean first-tokens to include poem
MAX_LINE_N = 15         # track individual lines up to this number; 15+ grouped


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def mean(vals):
    return sum(vals) / len(vals) if vals else float("nan")


def parse_lines_first_tokens(poem):
    """
    Return a list of (line_number, token_dict) for the FIRST non-newline token
    of each line. Line numbers are 1-indexed.

    A line is the sequence of tokens between consecutive '\n' tokens.
    Blank lines (a '\n' immediately followed by another '\n') indicate stanza breaks;
    these are skipped (not counted as a content line).

    Returns: list of (line_no, tok) where tok is the first content token of that line.
             Only includes lines where the first token is NOT an artifact (p_newline < 0.9).
    """
    tokens = poem["tokens"]
    lines = []         # list of [tok, tok, ...] for each non-blank line
    current_line = []

    for tok in tokens:
        if tok["token"] == "\n" or tok["token"] == "\r\n":
            if current_line:
                lines.append(current_line)
                current_line = []
            # If the next line is blank (another \n immediately), it'll just produce
            # an empty current_line which we'll skip.
        else:
            current_line.append(tok)

    # Handle last line (no trailing newline)
    if current_line:
        lines.append(current_line)

    # For each line, extract the first non-artifact token
    result = []
    for line_no, line in enumerate(lines, start=1):
        first_tok = None
        for tok in line:
            if tok.get("p_newline", 0) < P_NEWLINE_MAX:
                first_tok = tok
                break
        if first_tok is not None:
            result.append((line_no, first_tok))

    return result


def bucket_line_no(n):
    """Map line number to display bucket."""
    if n <= MAX_LINE_N:
        return n
    elif n <= 20:
        return "16-20"
    else:
        return "21+"


def main():
    corpus = load_corpus(CORPUS_PATH)
    en_poems = [p for p in corpus if p["metadata"].get("language", "en") == "en"
                and p["metadata"].get("era") not in ("control",)]

    # Per-line-number buckets: s2, entropy, surprisal lists
    by_line: dict = defaultdict(lambda: {"s2": [], "entropy": [], "surprisal": []})
    # Era breakdown for lines 1 and 2
    by_era_line: dict = defaultdict(lambda: defaultdict(list))
    # Per-poem line trajectories (for correlation analysis)
    poem_trajectories = []

    poems_used = 0
    poems_skipped = 0

    for poem in en_poems:
        line_first_tokens = parse_lines_first_tokens(poem)
        if len(line_first_tokens) < MIN_CLEAN_LINES:
            poems_skipped += 1
            continue
        poems_used += 1
        era = poem["metadata"].get("era", "unknown")

        traj = []
        for line_no, tok in line_first_tokens:
            b = bucket_line_no(line_no)
            by_line[b]["s2"].append(tok["s2"])
            by_line[b]["entropy"].append(tok["entropy"])
            by_line[b]["surprisal"].append(tok["surprisal"])
            if line_no <= 5:
                by_era_line[era][line_no].append(tok["s2"])
            traj.append({"line_no": line_no, "s2": tok["s2"], "entropy": tok["entropy"]})

        poem_trajectories.append({
            "title": poem["metadata"]["title"],
            "author": poem["metadata"]["author"],
            "era": era,
            "trajectory": traj,
        })

    print(f"Poems used: {poems_used}, skipped (too few lines): {poems_skipped}")

    # Build summary by bucket
    bucket_summary = {}
    all_buckets = sorted(
        by_line.keys(),
        key=lambda x: x if isinstance(x, int) else 100
    )

    print("\n=== Line-Number S₂ Profile (first token of each line) ===")
    print(f"{'Line':>7}  {'N':>5}  {'Mean S₂':>9}  {'Mean H':>8}  {'Spike%':>7}  {'Pos%':>7}")
    print("-" * 55)

    for b in all_buckets:
        s2v = by_line[b]["s2"]
        hv  = by_line[b]["entropy"]
        n = len(s2v)
        m_s2 = mean(s2v)
        m_h  = mean(hv)
        spike = sum(1 for v in s2v if v >= 3.0) / n * 100
        pos   = sum(1 for v in s2v if v > 0) / n * 100
        print(f"{str(b):>7}  {n:>5}  {m_s2:>+9.3f}  {m_h:>8.3f}  {spike:>6.1f}%  {pos:>6.1f}%")
        bucket_summary[str(b)] = {
            "n": n, "mean_s2": round(m_s2, 4), "mean_entropy": round(m_h, 4),
            "spike_rate": round(spike / 100, 4), "pos_s2_ratio": round(pos / 100, 4),
        }

    # Era breakdown for line 1 vs line 2
    print("\n=== Era breakdown: S₂ at line-1 first-token vs. line-2 first-token ===")
    print(f"{'Era':>25}  {'L1 n':>5}  {'L1 S₂':>8}  {'L2 n':>5}  {'L2 S₂':>8}  {'L2-L1':>7}")
    print("-" * 70)
    era_rows = []
    for era, by_line_era in by_era_line.items():
        l1 = by_line_era.get(1, [])
        l2 = by_line_era.get(2, [])
        if len(l1) >= 3 and len(l2) >= 3:
            m1 = mean(l1)
            m2 = mean(l2)
            diff = m2 - m1
            era_rows.append((era, len(l1), m1, len(l2), m2, diff))

    era_rows.sort(key=lambda x: -x[5])  # sort by L2-L1 difference descending
    for era, n1, m1, n2, m2, diff in era_rows:
        print(f"{era:>25}  {n1:>5}  {m1:>+8.3f}  {n2:>5}  {m2:>+8.3f}  {diff:>+7.3f}")

    # Save results
    output = {
        "by_line_bucket": bucket_summary,
        "era_line_breakdown": {
            era: {str(ln): {"mean_s2": round(mean(vals), 4), "n": len(vals)}
                  for ln, vals in by_line_era.items()}
            for era, by_line_era in by_era_line.items()
        },
        "poem_trajectories": poem_trajectories[:50],  # sample
        "metadata": {
            "poems_used": poems_used,
            "poems_skipped": poems_skipped,
            "p_newline_max": P_NEWLINE_MAX,
            "min_clean_lines": MIN_CLEAN_LINES,
        }
    }
    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
