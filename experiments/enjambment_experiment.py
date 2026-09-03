"""
Enjambment and S₂: Do poets use surprise strategically at line breaks?

Hypothesis: Enjambed line endings (no terminal punctuation) will have higher S₂
than end-stopped lines. Poets use syntactic suspension to heighten surprise —
placing a high-S₂ word at the break where the reader must wait for resolution.

Also tests: Do the FIRST words of lines following enjambment have different S₂?
"""

import json
import os
import sys
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine import load_results

TERMINAL_PUNCT = set(".,;:?!—")


def is_end_stopped(line: str) -> bool:
    """True if the line ends with terminal punctuation (ignoring trailing whitespace/quotes)."""
    stripped = line.rstrip().rstrip("\"'")
    return bool(stripped) and stripped[-1] in TERMINAL_PUNCT


def split_poem_to_lines(text: str):
    """Split poem text into non-empty lines."""
    return [l for l in text.split("\n") if l.strip()]


def find_line_boundary_tokens(token_data, text):
    """
    Map each token to whether it's a line-ending or line-starting position,
    and classify its line as enjambed or end-stopped.

    GPT-2 tokenizer preserves newlines. We scan for tokens containing '\n'
    to find line boundaries.

    Returns list of dicts:
      { 'role': 'end' | 'start',
        'enjambed': bool,
        'token': str,
        's2': float,
        'surprisal': float,
        'entropy': float,
        'line_text': str }
    """
    lines = split_poem_to_lines(text)
    if len(lines) < 2:
        return []

    # Build a classification for each line
    line_types = []  # (line_text, is_enjambed)
    for i, line in enumerate(lines):
        enjambed = not is_end_stopped(line)
        line_types.append((line, enjambed))

    results = []

    # Walk through tokens, find newline tokens, and annotate surrounding tokens
    for i, tok in enumerate(token_data):
        token_str = tok["token"]
        if "\n" not in token_str:
            continue

        # This token marks a line boundary.
        # The token BEFORE this (if not the newline itself) is the line-ending word.
        # Find the token just before the newline character in this token.

        # The actual newline-carrying token may be just "\n" or " \n" or "word\n"
        # We need the last non-whitespace token before the newline.
        # Strategy: look backward for the last token without \n.

        # Find the line-ending token: last CONTENT (non-punctuation) token before newline.
        # For end-stopped lines, skip trailing punctuation tokens so we compare
        # the last content word, not the punctuation mark itself.
        PUNCT_ONLY = set(".,;:?!—–\"'""''")
        end_idx = i - 1
        while end_idx >= 0 and (
            token_data[end_idx]["token"].strip() == ""
            or all(c in PUNCT_ONLY for c in token_data[end_idx]["token"].strip())
        ):
            end_idx -= 1

        # Find which line this corresponds to — count newlines seen so far
        newline_count = sum(1 for t in token_data[:i+1] if "\n" in t["token"])
        line_idx = newline_count - 1  # 0-indexed line that just ended

        if line_idx < 0 or line_idx >= len(line_types):
            continue

        line_text, enjambed = line_types[line_idx]

        # Record end-of-line token
        if end_idx >= 0 and token_data[end_idx]["token"].strip():
            end_tok = token_data[end_idx]
            if "\n" not in end_tok["token"]:  # skip if it's also a newline
                results.append({
                    "role": "end",
                    "enjambed": enjambed,
                    "token": end_tok["token"],
                    "s2": end_tok["s2"],
                    "surprisal": end_tok["surprisal"],
                    "entropy": end_tok["entropy"],
                    "line_text": line_text,
                    "line_idx": line_idx,
                })

        # Record start-of-next-line token
        start_idx = i + 1
        while start_idx < len(token_data) and token_data[start_idx]["token"].strip() == "":
            start_idx += 1

        if start_idx < len(token_data) and "\n" not in token_data[start_idx]["token"]:
            start_tok = token_data[start_idx]
            results.append({
                "role": "start",
                "enjambed": enjambed,  # same classification as the line we just left
                "token": start_tok["token"],
                "s2": start_tok["s2"],
                "surprisal": start_tok["surprisal"],
                "entropy": start_tok["entropy"],
                "line_text": line_text,
                "line_idx": line_idx,
            })

    return results


def mean(vals):
    return sum(vals) / len(vals) if vals else float("nan")


def analyze():
    from corpus.poems import POEMS

    # Load pre-computed results
    results = load_results()

    # Build index from title -> result
    result_index = {}
    for r in results:
        result_index[r["metadata"]["title"]] = r

    all_line_data = []
    poem_summaries = []

    for poem in POEMS:
        title = poem["title"]
        text = poem["text"]
        lang = poem.get("language", "en")
        if lang != "en":
            continue
        if title not in result_index:
            continue

        res = result_index[title]
        token_data = res["tokens"]

        boundary_tokens = find_line_boundary_tokens(token_data, text)
        if not boundary_tokens:
            continue

        all_line_data.extend(boundary_tokens)

        # Per-poem summary
        ends = [b for b in boundary_tokens if b["role"] == "end"]
        enjambed_ends = [b for b in ends if b["enjambed"]]
        stopped_ends = [b for b in ends if not b["enjambed"]]

        poem_summaries.append({
            "title": title,
            "author": poem["author"],
            "year": poem.get("year"),
            "n_lines": len(split_poem_to_lines(text)),
            "n_enjambed": len(enjambed_ends),
            "n_stopped": len(stopped_ends),
            "enjambed_pct": len(enjambed_ends) / max(1, len(ends)),
            "avg_s2_enjambed_end": mean([b["s2"] for b in enjambed_ends]),
            "avg_s2_stopped_end": mean([b["s2"] for b in stopped_ends]),
            "delta_s2": mean([b["s2"] for b in enjambed_ends]) - mean([b["s2"] for b in stopped_ends]),
        })

    return all_line_data, poem_summaries


def format_report(all_line_data, poem_summaries):
    # Aggregate statistics
    def group_stats(data, role, enjambed):
        vals = [d["s2"] for d in data if d["role"] == role and d["enjambed"] == enjambed]
        if not vals:
            return {"n": 0, "mean_s2": float("nan"), "median_s2": float("nan")}
        sorted_vals = sorted(vals)
        n = len(sorted_vals)
        median = sorted_vals[n // 2] if n % 2 else (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2
        return {"n": n, "mean_s2": mean(vals), "median_s2": median}

    ej_end   = group_stats(all_line_data, "end", True)
    stop_end = group_stats(all_line_data, "end", False)
    ej_start = group_stats(all_line_data, "start", True)
    stop_start = group_stats(all_line_data, "start", False)

    # Top examples: highest S₂ enjambed endings
    enjambed_examples = sorted(
        [d for d in all_line_data if d["role"] == "end" and d["enjambed"]],
        key=lambda d: d["s2"], reverse=True
    )[:10]

    # Top examples: highest S₂ end-stopped endings
    stopped_examples = sorted(
        [d for d in all_line_data if d["role"] == "end" and not d["enjambed"]],
        key=lambda d: d["s2"], reverse=True
    )[:10]

    # Poems with highest enjambment rate
    high_enjambment = sorted(
        [p for p in poem_summaries if p["n_enjambed"] + p["n_stopped"] >= 3],
        key=lambda p: p["enjambed_pct"], reverse=True
    )[:8]

    # Poems where enjambed ends have highest S₂ delta
    high_delta = sorted(
        [p for p in poem_summaries if p["n_enjambed"] >= 2 and p["n_stopped"] >= 2],
        key=lambda p: p["delta_s2"], reverse=True
    )[:8]

    report = f"""# Enjambment and S₂: Strategic Surprise at Line Breaks
**Date:** 2026-09-03
**Experiment:** `experiments/enjambment_experiment.py`

## Question
Do poets use enjambment — the continuation of a sentence past a line break without terminal
punctuation — to strategically heighten S₂? Is the last word of an enjambed line more
surprising than the last word of an end-stopped line?

## Method
- Analyzed {len(set(d["line_text"] for d in all_line_data))} unique lines across {len(poem_summaries)} English poems
- Classified each line as **enjambed** (no terminal punctuation: .,;:?!—) or **end-stopped**
- Extracted S₂ of the **last word** of each line and the **first word** of the following line
- Compared distributions across {ej_end["n"] + stop_end["n"]} line-boundary tokens

## Results

### Line-ending tokens (the crucial position)

| Type | n | Mean S₂ | Median S₂ |
|------|---|---------|-----------|
| Enjambed line endings | {ej_end["n"]} | {ej_end["mean_s2"]:+.3f} | {ej_end["median_s2"]:+.3f} |
| End-stopped line endings | {stop_end["n"]} | {stop_end["mean_s2"]:+.3f} | {stop_end["median_s2"]:+.3f} |
| **Delta (enjambed − stopped)** | — | **{ej_end["mean_s2"] - stop_end["mean_s2"]:+.3f}** | **{ej_end["median_s2"] - stop_end["median_s2"]:+.3f}** |

### Line-starting tokens (first word after the break)

| Type | n | Mean S₂ | Median S₂ |
|------|---|---------|-----------|
| After enjambed line | {ej_start["n"]} | {ej_start["mean_s2"]:+.3f} | {ej_start["median_s2"]:+.3f} |
| After end-stopped line | {stop_start["n"]} | {stop_start["mean_s2"]:+.3f} | {stop_start["median_s2"]:+.3f} |
| **Delta (after enjambed − after stopped)** | — | **{ej_start["mean_s2"] - stop_start["mean_s2"]:+.3f}** | **{ej_start["median_s2"] - stop_start["median_s2"]:+.3f}** |

## Top 10 highest-S₂ enjambed line endings

| Token | S₂ | Line |
|-------|----|------|
"""
    for ex in enjambed_examples:
        token = ex["token"].strip().replace("|", "\\|")
        line = ex["line_text"].strip()[:60].replace("|", "\\|")
        report += f"| `{token}` | {ex['s2']:+.2f} | {line} |\n"

    report += f"""
## Top 10 highest-S₂ end-stopped line endings

| Token | S₂ | Line |
|-------|----|------|
"""
    for ex in stopped_examples:
        token = ex["token"].strip().replace("|", "\\|")
        line = ex["line_text"].strip()[:60].replace("|", "\\|")
        report += f"| `{token}` | {ex['s2']:+.2f} | {line} |\n"

    report += f"""
## Poems with highest enjambment rates

| Poem | Author | Year | Lines | Enjambed% | Avg S₂ (enj) | Avg S₂ (stop) | Δ |
|------|--------|------|-------|-----------|--------------|----------------|---|
"""
    for p in high_enjambment:
        report += (
            f"| {p['title'][:30]} | {p['author'][:20]} | {p['year']} "
            f"| {p['n_lines']} | {p['enjambed_pct']:.0%} "
            f"| {p['avg_s2_enjambed_end']:+.2f} "
            f"| {p['avg_s2_stopped_end']:+.2f} "
            f"| {p['delta_s2']:+.2f} |\n"
        )

    report += f"""
## Poems with highest S₂ delta (enjambed − stopped)

| Poem | Author | Δ S₂ | Enjambed% |
|------|--------|------|-----------|
"""
    for p in high_delta:
        report += (
            f"| {p['title'][:35]} | {p['author'][:20]} "
            f"| {p['delta_s2']:+.2f} | {p['enjambed_pct']:.0%} |\n"
        )

    # Determine overall finding
    delta = ej_end["mean_s2"] - stop_end["mean_s2"]
    if delta > 0.3:
        finding = "**CONFIRMED**: Enjambed line endings have substantially higher S₂ than end-stopped ones."
        direction = "Poets strategically place surprising words at enjambed breaks."
    elif delta > 0.05:
        finding = "**WEAK SUPPORT**: Enjambed line endings trend higher in S₂, but the effect is small."
        direction = "Weak evidence that enjambment and surprise co-occur."
    elif delta < -0.1:
        finding = "**REVERSED**: End-stopped lines show higher S₂ at their endings."
        direction = "The surprise comes *with* the closure — punctuation marks a moment of resolution-via-surprise."
    else:
        finding = "**NULL RESULT**: No significant S₂ difference between enjambed and end-stopped line endings."
        direction = "Enjambment operates on syntactic structure, not information-theoretic surprise per token."

    start_delta = ej_start["mean_s2"] - stop_start["mean_s2"]
    start_finding = ""
    if abs(start_delta) > 0.2:
        if start_delta > 0:
            start_finding = f"\nThe first word **after** an enjambed break is also more surprising (Δ={start_delta:+.2f}), suggesting the surprise carries across the line break — a double-peak effect."
        else:
            start_finding = f"\nInterestingly, the first word **after** an enjambed break is *less* surprising (Δ={start_delta:+.2f}), consistent with the 'leap and land' model: enjambment propels the reader toward a resolved, expected continuation."

    report += f"""
## Key Finding

{finding}

{direction}{start_finding}

### Interpretation: Two models of enjambment

**Model A — Suspension hypothesis**: Enjambment places high-S₂ words at line breaks to create
suspense. The reader is left holding an unexpected word and must wait for the next line to
resolve the meaning. This predicts higher S₂ at enjambed endings.

**Model B — Propulsion hypothesis**: Enjambment uses *syntactically incomplete* (hence
predictable) endings to pull the reader forward. Surprise is deferred to the resolution in
the next line (the start token). This predicts *lower* S₂ at enjambed endings but *higher*
S₂ at the first word of the continuation.

The actual Δ of {delta:+.3f} at endings and {start_delta:+.3f} at line starts suggests:
{"Model A dominates in this corpus." if delta > 0.1 else "Model B dominates — enjambment is a propulsive, low-surprise mechanism." if delta < -0.05 else "Neither model dominates cleanly; both forces operate."}

## Implications for the Straussian gap

When a poet enjambs a high-S₂ word, they create a dual gap:
1. **Semantic gap**: the unexpected word hangs in air without syntactic closure
2. **Information gap**: GPT-2's top prediction (the "unsaid") would have ended the line differently

The line break acts as a *second* Straussian gap, amplifying the first.

## Next steps
- Analyze specific poet-level enjambment strategies (Keats vs Dickinson vs Plath)
- Test whether enjambment interacts with meter — does enjambment of iambic pentameter
  produce stronger S₂ spikes than free verse enjambment?
- Look at *depth* of enjambment: how far into the next line does resolution take?
- Compare with prose control texts: do prose sentences broken arbitrarily show the same pattern?
"""
    return report


if __name__ == "__main__":
    print("Running enjambment experiment...")
    all_line_data, poem_summaries = analyze()
    print(f"  Analyzed {len(poem_summaries)} poems, {len(all_line_data)} boundary tokens")
    report = format_report(all_line_data, poem_summaries)
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings", "enjambment_vs_s2.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"Report saved to: {out_path}")

    # Print key stats to terminal
    for role, ej in [("end", True), ("end", False), ("start", True), ("start", False)]:
        vals = [d["s2"] for d in all_line_data if d["role"] == role and d["enjambed"] == ej]
        label = f"{'Enjambed' if ej else 'End-stopped'} {role}"
        if vals:
            print(f"  {label:<30} n={len(vals):>4}  mean_S2={sum(vals)/len(vals):+.3f}")
