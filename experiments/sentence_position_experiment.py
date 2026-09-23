"""
Sentence-Position vs. Line-Position S2 Analysis

Extends the line_position_analysis by cross-tabulating:
  - sentence position (initial / medial / final)
  - line position (initial / medial / final)

Key question: is the strong line-initial S2 spike from line_position_analysis.md
driven by sentence boundaries that co-occur with line breaks (end-stopped lines),
or is it caused by the line break itself (pure enjambment)?

If the enjambed line-initial tokens (sentence-medial but line-initial) show a spike
equal to end-stopped line-initial tokens, the LINE BREAK is the mechanism.
If enjambed line-initial tokens show a weaker spike, sentence boundaries drive it.
"""

import json
import re
from collections import defaultdict
from statistics import mean, stdev

RESULTS_FILE = "results/corpus_results.json"
SENTENCE_END_PATTERN = re.compile(r"[.!?]")


def classify_tokens(tokens):
    """
    Returns each token annotated with:
      line_pos: 'initial' | 'medial' | 'final'
      sent_pos: 'initial' | 'medial' | 'final'
    """
    n = len(tokens)
    annotated = []

    # Build string of token texts for context
    texts = [t["token"] for t in tokens]

    # Detect line boundaries: a token is line-initial if the previous token
    # contains a newline, or it's the first token.
    # A token is line-final if it contains a newline itself, or is the last token.
    def has_newline(text):
        return "\n" in text

    # Detect sentence boundaries:
    # A token is sentence-final if it ends with . ! ? (stripping whitespace)
    # A token is sentence-initial if the previous token was sentence-final,
    # or it's the first non-newline token.
    def is_sent_ending(text):
        stripped = text.strip()
        return bool(stripped and SENTENCE_END_PATTERN.search(stripped[-1]))

    # First pass: mark line positions
    line_pos = []
    for i, t in enumerate(tokens):
        text = t["token"]
        # Skip pure newline tokens from position assignment
        if text.strip("\n\r") == "":
            line_pos.append("whitespace")
            continue
        prev_has_nl = i > 0 and has_newline(texts[i - 1])
        is_first = i == 0
        is_last = i == n - 1
        # Check if next non-whitespace token is a newline
        next_is_nl = False
        for j in range(i + 1, n):
            if texts[j].strip("\n\r") == "":
                next_is_nl = True
                break
            if "\n" in texts[j]:
                next_is_nl = True
                break
            break  # next real token doesn't contain newline

        if prev_has_nl or is_first:
            line_pos.append("initial")
        elif is_last or next_is_nl or "\n" in text:
            line_pos.append("final")
        else:
            line_pos.append("medial")

    # Second pass: mark sentence positions
    sent_pos = []
    at_sentence_start = True
    for i, t in enumerate(tokens):
        text = t["token"]
        if text.strip("\n\r") == "":
            sent_pos.append("whitespace")
            continue

        if at_sentence_start:
            sent_pos.append("initial")
            at_sentence_start = False
        else:
            # Check if this token ends a sentence
            if is_sent_ending(text):
                sent_pos.append("final")
                at_sentence_start = True
            else:
                sent_pos.append("medial")

    # Combine annotations
    for i, t in enumerate(tokens):
        if line_pos[i] == "whitespace":
            continue
        annotated.append({
            "s2": t["s2"],
            "line_pos": line_pos[i],
            "sent_pos": sent_pos[i],
            "token": t["token"],
        })

    return annotated


def run():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    # Filter English poems only
    poems = [p for p in corpus if p["metadata"].get("language", "en") == "en"]
    print(f"Analyzing {len(poems)} English poems...")

    # Collect cross-tabulated S2 values
    buckets = defaultdict(list)  # key: (line_pos, sent_pos)

    for poem in poems:
        annotated = classify_tokens(poem["tokens"])
        for tok in annotated:
            key = (tok["line_pos"], tok["sent_pos"])
            buckets[key].append(tok["s2"])

    # Report
    print("\n=== Sentence-Position × Line-Position Cross-Table ===\n")
    print(f"{'Category':<40} {'N':>6} {'Mean S2':>9} {'Std':>7} {'%+S2':>7}")
    print("-" * 75)

    order = [
        ("initial", "initial"),   # line-initial & sentence-initial (end-stopped prev line)
        ("initial", "medial"),    # line-initial & sentence-medial (pure enjambment)
        ("medial", "initial"),    # sentence starts mid-line (rare)
        ("medial", "medial"),     # baseline: mid-sentence, mid-line
        ("medial", "final"),      # sentence ends mid-line
        ("final", "initial"),     # sentence starts at line end (very rare)
        ("final", "medial"),      # line-final but mid-sentence
        ("final", "final"),       # line-final & sentence-final (end-stopped)
    ]

    results = {}
    for line_p, sent_p in order:
        key = (line_p, sent_p)
        vals = buckets.get(key, [])
        if len(vals) < 5:
            label = f"line={line_p}, sent={sent_p}"
            print(f"  {label:<38} {'<5':>6}")
            continue
        m = mean(vals)
        s = stdev(vals) if len(vals) > 1 else 0
        pct = sum(1 for v in vals if v > 0) / len(vals) * 100
        label = f"line={line_p}, sent={sent_p}"
        print(f"  {label:<38} {len(vals):>6} {m:>+9.3f} {s:>7.3f} {pct:>6.1f}%")
        results[key] = {"n": len(vals), "mean": m, "std": s, "pos_pct": pct}

    # Key comparisons
    print("\n=== Key Comparisons ===")
    li_ss = results.get(("initial", "initial"), {})
    li_sm = results.get(("initial", "medial"), {})
    lm_sm = results.get(("medial", "medial"), {})

    if li_ss and li_sm and lm_sm:
        baseline = lm_sm["mean"]
        print(f"\nBaseline (line-medial, sent-medial): {baseline:+.3f} S2")
        print(f"Line-initial + sent-initial:         {li_ss['mean']:+.3f} S2  (Δ {li_ss['mean']-baseline:+.2f})")
        print(f"Line-initial + sent-medial (enjamb): {li_sm['mean']:+.3f} S2  (Δ {li_sm['mean']-baseline:+.2f})")
        print()
        print("Interpretation:")
        if abs(li_sm["mean"] - li_ss["mean"]) < 1.0:
            print("  LINE BREAK DRIVES THE SPIKE — enjambed line-initial ≈ end-stopped line-initial")
        elif li_sm["mean"] > li_ss["mean"]:
            print("  ENJAMBMENT INTENSIFIES SURPRISE — enjambed line-initial > end-stopped")
        else:
            print("  SENTENCE BOUNDARY MODERATES — end-stopped line-initial > enjambed")

    # Also show overall line-position marginals (replicating the original study)
    print("\n=== Line-Position Marginals (replication check) ===")
    for lp in ["initial", "medial", "final"]:
        vals = []
        for sp in ["initial", "medial", "final"]:
            vals.extend(buckets.get((lp, sp), []))
        if vals:
            print(f"  line={lp:<8} N={len(vals):>5}  mean={mean(vals):+.3f}")

    # Sentence-position marginals
    print("\n=== Sentence-Position Marginals ===")
    for sp in ["initial", "medial", "final"]:
        vals = []
        for lp in ["initial", "medial", "final"]:
            vals.extend(buckets.get((lp, sp), []))
        if vals:
            print(f"  sent={sp:<8} N={len(vals):>5}  mean={mean(vals):+.3f}")

    return results, buckets


if __name__ == "__main__":
    run()
