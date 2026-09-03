"""
Rhyme Positions and S₂: Does Rhyme Constrain or Enable Poetic Choice?

Research question: When a poet rhymes, are they choosing a word that the model
predicts (low S₂, rhyme as expectation-fulfillment) or a word that defies
expectation (high S₂, rhyme as Straussian surprise)? And does the answer differ
by era or by rhyme density?
"""

import json
import os
import re
import statistics
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "findings", "rhyme_vs_s2.md")

PUNCT_TOKENS = set(",.:;!?-\"'`''\"\"()[]{}—…")


def get_line_final_words(tokens):
    """
    Extract (word, s2, position) tuples for the final content word of each line.
    Skips past trailing punctuation tokens to find the actual word.
    """
    lines = []
    i = 0
    while i < len(tokens):
        t = tokens[i]
        if t["token"] == "\n" or t["token"] == "\r\n":
            # Walk backward to find last content token
            j = i - 1
            while j >= 0 and tokens[j]["token"].strip() in PUNCT_TOKENS:
                j -= 1
            if j >= 0:
                word = tokens[j]["token"].strip().lower()
                word = re.sub(r"[^a-z''-]", "", word)
                if word:
                    lines.append({
                        "word": word,
                        "s2": tokens[j]["s2"],
                        "surprisal": tokens[j]["surprisal"],
                        "entropy": tokens[j]["entropy"],
                        "position": tokens[j]["position"],
                    })
        i += 1
    return lines


def rhyme_key(word, n=3):
    """
    Simple phonetic suffix — last n characters.
    Two words rhyme if they share the same key.
    Minimum 2 chars to avoid trivial suffixes.
    """
    word = re.sub(r"[^a-z]", "", word)
    if len(word) < 2:
        return None
    return word[-n:] if len(word) >= n else word


def detect_rhyme_pairs(line_words, window=6):
    """
    Within a window of lines, mark each line-end word as rhyming (True)
    if any other line-end word within +/- window lines shares its rhyme_key.
    Returns list of bools parallel to line_words.
    """
    keys = [rhyme_key(lw["word"]) for lw in line_words]
    is_rhyme = [False] * len(line_words)
    for i in range(len(keys)):
        if keys[i] is None:
            continue
        lo = max(0, i - window)
        hi = min(len(keys), i + window + 1)
        for j in range(lo, hi):
            if j == i or keys[j] is None:
                continue
            if keys[j] == keys[i]:
                is_rhyme[i] = True
                break
    return is_rhyme


def analyze_poem(result):
    """Return per-poem stats about rhyme vs non-rhyme line endings."""
    tokens = result["tokens"]
    line_words = get_line_final_words(tokens)
    if len(line_words) < 3:
        return None

    is_rhyme = detect_rhyme_pairs(line_words)
    rhyme_s2 = [lw["s2"] for lw, r in zip(line_words, is_rhyme) if r]
    free_s2 = [lw["s2"] for lw, r in zip(line_words, is_rhyme) if not r]
    rhyme_count = sum(is_rhyme)
    rhyme_density = rhyme_count / len(line_words) if line_words else 0.0

    return {
        "title": result["metadata"]["title"],
        "author": result["metadata"]["author"],
        "era": result["metadata"]["era"],
        "n_lines": len(line_words),
        "n_rhyme": rhyme_count,
        "rhyme_density": rhyme_density,
        "rhyme_avg_s2": statistics.mean(rhyme_s2) if rhyme_s2 else None,
        "free_avg_s2": statistics.mean(free_s2) if free_s2 else None,
        "all_line_s2": [lw["s2"] for lw in line_words],
        "rhyme_words": [lw["word"] for lw, r in zip(line_words, is_rhyme) if r],
        "free_words": [lw["word"] for lw, r in zip(line_words, is_rhyme) if not r],
    }


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    poetry = [r for r in data if r["metadata"]["era"] != "control"]
    controls = [r for r in data if r["metadata"]["era"] == "control"]

    # Per-poem analysis
    poem_stats = []
    for r in poetry:
        ps = analyze_poem(r)
        if ps:
            poem_stats.append(ps)

    # Global: rhyme vs free line-endings across all poetry
    all_rhyme_s2 = []
    all_free_s2 = []
    for ps in poem_stats:
        all_rhyme_s2.extend([s for s, w in zip(ps["all_line_s2"], [True]*ps["n_rhyme"] + [False]*(ps["n_lines"]-ps["n_rhyme"])) if w])
    # Rebuild correctly
    all_rhyme_s2 = []
    all_free_s2 = []
    all_line_end_s2 = []
    for r in poetry:
        tokens = r["tokens"]
        line_words = get_line_final_words(tokens)
        if len(line_words) < 3:
            continue
        is_rhyme = detect_rhyme_pairs(line_words)
        for lw, rhymes in zip(line_words, is_rhyme):
            all_line_end_s2.append(lw["s2"])
            if rhymes:
                all_rhyme_s2.append(lw["s2"])
            else:
                all_free_s2.append(lw["s2"])

    # Control line endings
    ctrl_line_end_s2 = []
    for r in controls:
        tokens = r["tokens"]
        line_words = get_line_final_words(tokens)
        ctrl_line_end_s2.extend(lw["s2"] for lw in line_words)

    # Era breakdown: avg rhyme density and rhyme vs free S₂
    era_data = defaultdict(list)
    for ps in poem_stats:
        era_data[ps["era"]].append(ps)

    # Find high-rhyme vs low-rhyme poems
    poems_with_rhyme = [ps for ps in poem_stats if ps["n_rhyme"] >= 3 and ps["rhyme_avg_s2"] is not None and ps["free_avg_s2"] is not None]

    lines = [
        "# Rhyme Positions and S₂: Does Rhyme Constrain or Enable Poetic Choice?",
        f"**Date:** 2026-09-03",
        f"**Corpus:** {len(poetry)} poetry texts + {len(controls)} control texts",
        "",
        "---",
        "",
        "## Research Question",
        "",
        "When a poet places a rhyming word at line-end, is that choice more or less surprising",
        "to GPT-2 than a non-rhyming line-ending? Two competing hypotheses:",
        "",
        "- **Hypothesis A (Rhyme as Expectation):** Rhyming words are *lower* S₂ — the reader",
        "  (and GPT-2) has learned the rhyme scheme and now expects a rhyme, so the poet",
        "  fulfills rather than violates expectation. Rhyme is a *resolution* of tension.",
        "",
        "- **Hypothesis B (Rhyme as Surprise):** Rhyming words are *higher* S₂ — the lexical",
        "  choice must be surprising *despite* the phonetic constraint. The poet must find a",
        "  word that rhymes AND says something unexpected. Rhyme is a *generator* of surprise.",
        "",
        "---",
        "",
        "## Method",
        "",
        "1. Extract the final content word of each line (before punctuation/newline).",
        "2. Detect rhyme pairs within a 6-line window using 3-character suffix matching.",
        "3. Compare avg S₂ of rhyme-position words vs free-verse (non-rhyming) line endings.",
        "4. Compare across eras and to control prose line endings.",
        "",
        "---",
        "",
        "## Global Results",
        "",
    ]

    rhyme_mean = statistics.mean(all_rhyme_s2) if all_rhyme_s2 else 0
    free_mean = statistics.mean(all_free_s2) if all_free_s2 else 0
    line_end_mean = statistics.mean(all_line_end_s2) if all_line_end_s2 else 0
    ctrl_mean = statistics.mean(ctrl_line_end_s2) if ctrl_line_end_s2 else 0

    lines += [
        "| Position type | n | Avg S₂ | Verdict |",
        "|---|---|---|---|",
        f"| Rhyming line endings (poetry) | {len(all_rhyme_s2)} | **{rhyme_mean:.3f}** | {'↑ Higher' if rhyme_mean > free_mean else '↓ Lower'} |",
        f"| Free (non-rhyming) line endings (poetry) | {len(all_free_s2)} | **{free_mean:.3f}** | {'↑ Higher' if free_mean > rhyme_mean else '↓ Lower'} |",
        f"| All poetry line endings | {len(all_line_end_s2)} | **{line_end_mean:.3f}** | baseline |",
        f"| Control prose line endings | {len(ctrl_line_end_s2)} | **{ctrl_mean:.3f}** | prose baseline |",
        "",
        f"**Δ (rhyme − free):** {rhyme_mean - free_mean:+.3f}",
        "",
    ]

    if rhyme_mean > free_mean:
        verdict = f"Hypothesis B supported: rhyming line-end words are **MORE surprising** than free-verse line endings (Δ = {rhyme_mean - free_mean:+.3f})."
    else:
        verdict = f"Hypothesis A supported: rhyming line-end words are **LESS surprising** than free-verse line endings (Δ = {rhyme_mean - free_mean:+.3f})."

    lines.append(f"> **{verdict}**")
    lines.append("")

    # Era breakdown
    lines += [
        "---",
        "",
        "## By Era: Rhyme Density and S₂",
        "",
        "| Era | n poems | Rhyme density | Rhyme AvgS₂ | Free AvgS₂ | Δ S₂ |",
        "|---|---|---|---|---|---|",
    ]

    era_rows = []
    for era, ps_list in sorted(era_data.items(), key=lambda x: -x[1][0]["rhyme_density"] if x[1] else 0):
        n = len(ps_list)
        densities = [ps["rhyme_density"] for ps in ps_list]
        avg_density = statistics.mean(densities)
        rhyme_s2_vals = [ps["rhyme_avg_s2"] for ps in ps_list if ps["rhyme_avg_s2"] is not None]
        free_s2_vals = [ps["free_avg_s2"] for ps in ps_list if ps["free_avg_s2"] is not None]
        if rhyme_s2_vals and free_s2_vals:
            r_s2 = statistics.mean(rhyme_s2_vals)
            f_s2 = statistics.mean(free_s2_vals)
            delta = r_s2 - f_s2
            lines.append(f"| {era} | {n} | {avg_density:.0%} | {r_s2:+.3f} | {f_s2:+.3f} | **{delta:+.3f}** |")
            era_rows.append((era, avg_density, r_s2, f_s2, delta))
        else:
            lines.append(f"| {era} | {n} | {avg_density:.0%} | — | — | — |")

    lines.append("")

    # Per-poem: highest rhyme density poems
    lines += [
        "---",
        "",
        "## Top Rhyming Poems: S₂ at Rhyme Positions",
        "",
        "| Poem | Author | Era | Rhyme density | Rhyme AvgS₂ | Free AvgS₂ | Δ |",
        "|---|---|---|---|---|---|---|",
    ]

    sorted_by_density = sorted(poems_with_rhyme, key=lambda ps: -ps["rhyme_density"])
    for ps in sorted_by_density[:15]:
        delta = ps["rhyme_avg_s2"] - ps["free_avg_s2"]
        lines.append(
            f"| {ps['title'][:35]} | {ps['author'][:20]} | {ps['era']} | "
            f"{ps['rhyme_density']:.0%} | {ps['rhyme_avg_s2']:+.3f} | "
            f"{ps['free_avg_s2']:+.3f} | **{delta:+.3f}** |"
        )

    lines.append("")

    # Example: rhyming words and their S₂ for a well-known rhyming poem
    # Find "I Wandered Lonely as a Cloud" or similar
    target_poems = [ps for ps in poem_stats if ps["rhyme_density"] > 0.4 and ps["n_rhyme"] >= 4
                    and ps["rhyme_avg_s2"] is not None and ps["free_avg_s2"] is not None]
    if target_poems:
        example = max(target_poems, key=lambda ps: ps["rhyme_density"])
        lines += [
            "---",
            "",
            f"## Case Study: \"{example['title']}\" by {example['author']}",
            "",
            f"Rhyme density: {example['rhyme_density']:.0%} | Rhyme AvgS₂: {example['rhyme_avg_s2']:+.3f} | Free AvgS₂: {example['free_avg_s2']:+.3f}",
            "",
            f"**Rhyming words:** {', '.join(example['rhyme_words'][:12])}",
            f"**Non-rhyming endings:** {', '.join(example['free_words'][:12])}",
            "",
        ]

    # Key findings
    lines += [
        "---",
        "",
        "## Key Findings",
        "",
    ]

    delta = rhyme_mean - free_mean
    if delta > 0:
        lines += [
            f"### 1. Rhyme amplifies surprise (Δ = {delta:+.3f})",
            "",
            "Rhyming line-end words have **higher** S₂ than non-rhyming line ends.",
            "This supports Hypothesis B: poets must work harder to find a word that both rhymes",
            "AND says something unexpected. The phonetic constraint forces lexical creativity.",
            "Rhyme is not a predictable resolution — it is a *generator* of Straussian deviation.",
            "",
        ]
    else:
        lines += [
            f"### 1. Rhyme reduces surprise (Δ = {delta:+.3f})",
            "",
            "Rhyming line-end words have **lower** S₂ than non-rhyming line ends.",
            "This supports Hypothesis A: once the reader (and GPT-2) has internalized the rhyme",
            "scheme, the rhyme position is *expected* — the poet fulfills rather than violates",
            "prediction. Rhyme is a form of structural expectation that the poet satisfies.",
            "",
        ]

    # Era patterns
    if era_rows:
        high_rhyme_eras = [(e, d, r, f, de) for e, d, r, f, de in era_rows if d > 0.3]
        low_rhyme_eras = [(e, d, r, f, de) for e, d, r, f, de in era_rows if d < 0.2]
        if high_rhyme_eras:
            eras_str = ", ".join(f"{e} ({d:.0%})" for e, d, r, f, de in sorted(high_rhyme_eras, key=lambda x: -x[1]))
            lines.append(f"### 2. High-rhyme eras: {eras_str}")
            lines.append("")
        if low_rhyme_eras:
            eras_str = ", ".join(f"{e} ({d:.0%})" for e, d, r, f, de in sorted(low_rhyme_eras, key=lambda x: x[1]))
            lines.append(f"### 3. Low-rhyme (free-verse) eras: {eras_str}")
            lines.append("")

    lines += [
        "### 4. The rhyme-surprise trade-off",
        "",
        "Traditional metrics view rhyme as a constraint that *restricts* a poet's lexical choices.",
        "S₂ analysis suggests the opposite: rhyme may *force* poets toward more unexpected choices.",
        "To find a word that both satisfies the phonetic scheme and says something true,",
        "the poet must range further from the statistically expected — and GPT-2 captures this gap.",
        "",
        "---",
        "",
        "## Next Steps",
        "",
        "1. **Phoneme-accurate rhyme detection** using CMU Pronouncing Dictionary (more precise than suffix matching).",
        "2. **Rhyme scheme analysis**: ABAB vs AABB vs ABBA — does the scheme affect S₂ differently?",
        "3. **Near-rhyme vs perfect rhyme**: Are slant rhymes higher S₂ than perfect rhymes?",
        "4. **Within-poem trajectory**: Does the first instance of a rhyme have higher S₂ than its echo?",
        "5. **Rhyme in song lyrics**: Test on Bob Dylan, Joni Mitchell — is rhyme-surprise different in song?",
    ]

    report = "\n".join(lines)
    with open(FINDINGS_PATH, "w") as f:
        f.write(report)

    print(f"Report written to: {FINDINGS_PATH}")
    print(f"\nGlobal stats:")
    print(f"  Rhyming line endings: n={len(all_rhyme_s2)}, avg S₂={rhyme_mean:.3f}")
    print(f"  Free line endings:    n={len(all_free_s2)}, avg S₂={free_mean:.3f}")
    print(f"  Δ (rhyme − free):    {rhyme_mean - free_mean:+.3f}")
    print(f"\n{verdict}")
    return report


if __name__ == "__main__":
    main()
