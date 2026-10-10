"""
Parody and Pastiche: S₂ Analysis of Literary Subversion

Research question:
  Does parody achieve its effect by evoking familiar language (LOW S₂)
  and then subverting it at key moments (HIGH S₂ spikes)?

Method:
  1. Load corpus results for parody poems and their originals (parody_original era)
  2. Compare S₂ distributions between parody vs. original
  3. For Carroll parodies, align original/parody at shared phrase beginnings
     and find exact divergence points — do S₂ values spike there?
  4. Compare parody S₂ profile shape (bimodal?) vs. original (unimodal?)
  5. Contrast mock-epic (Pope) — high register on trivial subject — vs.
     straight parody (Carroll)

Hypothesis:
  - Parody poems will show HIGHER variance / spikier S₂ than originals
  - The subversion tokens will have markedly HIGHER S₂ than surrounding context
  - The "evocation" phase (shared words) will show LOW S₂ (GPT-2 recognizes the familiar)
  - Mock-epic (Pope) may show overall lower avg S₂ than Carroll's direct parody
    (epic diction is common in training data; pure nonsense is not)
"""

import json
import os
import sys
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

ARTIFACT_P = 0.90


def load_results():
    path = os.path.join(RESULTS_DIR, "corpus_results.json")
    with open(path) as f:
        return json.load(f)


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def clean_tokens(tokens):
    return [t for t in tokens if newline_prob(t) < ARTIFACT_P]


def s2_stats(tokens):
    vals = [t["s2"] for t in tokens]
    if not vals:
        return {}
    return {
        "n": len(vals),
        "mean": statistics.mean(vals),
        "stdev": statistics.stdev(vals) if len(vals) > 1 else 0.0,
        "max": max(vals),
        "min": min(vals),
        "pos_ratio": sum(1 for v in vals if v > 0) / len(vals),
        "high_ratio": sum(1 for v in vals if v > 3) / len(vals),
        "variance": statistics.variance(vals) if len(vals) > 1 else 0.0,
    }


def run_parody_analysis(results):
    # ── 1. Separate poems by era ───────────────────────────────────────────────
    parody_poems = [r for r in results if r["metadata"]["era"] == "parody"]
    original_poems = [r for r in results if r["metadata"]["era"] == "parody_original"]
    control_poems = [r for r in results if r["metadata"]["era"] == "control"]
    poetry_general = [r for r in results
                      if r["metadata"]["era"] not in ("parody", "parody_original", "control")]

    lines = []

    # ── 2. Overall S₂ comparison ───────────────────────────────────────────────
    lines.append("## Overall S₂ Comparison: Parody vs. Original vs. General Poetry vs. Prose\n")
    lines.append("| Group | n poems | n tokens | Mean S₂ | StDev S₂ | Variance | +S₂ Ratio | High-S₂ Ratio (>3) |")
    lines.append("|---|---|---|---|---|---|---|---|")

    groups = [
        ("Parody", parody_poems),
        ("Parody Original", original_poems),
        ("General Poetry", poetry_general),
        ("Prose Control", control_poems),
    ]

    group_stats = {}
    for label, poems in groups:
        all_tokens = [t for r in poems for t in clean_tokens(r["tokens"])]
        st = s2_stats(all_tokens)
        group_stats[label] = st
        if st:
            lines.append(
                f"| {label} | {len(poems)} | {st['n']} | "
                f"{st['mean']:.3f} | {st['stdev']:.3f} | {st['variance']:.3f} | "
                f"{st['pos_ratio']:.1%} | {st['high_ratio']:.1%} |"
            )

    lines.append("")

    # ── 3. Per-poem breakdown ──────────────────────────────────────────────────
    lines.append("## Per-Poem S₂ Profile (Parody + Originals)\n")
    lines.append("| Title | Author | Era | n tokens | Mean S₂ | StDev | Variance | +S₂ | High-S₂ |")
    lines.append("|---|---|---|---|---|---|---|---|---|")

    all_parody_related = parody_poems + original_poems
    all_parody_related.sort(key=lambda r: r["metadata"]["title"])

    for r in all_parody_related:
        toks = clean_tokens(r["tokens"])
        st = s2_stats(toks)
        if st:
            lines.append(
                f"| {r['metadata']['title'][:45]} | {r['metadata']['author'][:25]} | "
                f"{r['metadata']['era']} | {st['n']} | "
                f"{st['mean']:.3f} | {st['stdev']:.3f} | {st['variance']:.3f} | "
                f"{st['pos_ratio']:.1%} | {st['high_ratio']:.1%} |"
            )

    lines.append("")

    # ── 4. Carroll pairs: divergence point analysis ────────────────────────────
    lines.append("## Carroll Parody Divergence Analysis\n")
    lines.append("Each Carroll parody follows its original closely at the start, then diverges.\n")
    lines.append("We find where the parody 'breaks' from the original and measure S₂ around that point.\n")

    # Pair titles
    pairs = [
        ("How Doth the Little Busy Bee", "How Doth the Little Crocodile"),
        ("The Old Man's Comforts and How He Gained Them", "You Are Old, Father William"),
        ("'Tis the Voice of the Sluggard", "'Tis the Voice of the Lobster"),
    ]

    def find_poem(results, title):
        for r in results:
            if r["metadata"]["title"] == title:
                return r
        return None

    for orig_title, parody_title in pairs:
        orig = find_poem(results, orig_title)
        parody = find_poem(results, parody_title)
        if not (orig and parody):
            lines.append(f"\n### {parody_title}\n⚠️ Missing from results — run engine first.\n")
            continue

        lines.append(f"\n### Pair: '{orig_title}' → '{parody_title}'\n")

        orig_toks = orig["tokens"]
        par_toks = parody["tokens"]

        # Find first shared token (shared start)
        orig_words = [t["token"].lower().strip() for t in orig_toks]
        par_words = [t["token"].lower().strip() for t in par_toks]

        # Find first divergence — longest common prefix at word level
        diverge_idx = 0
        for i, (ow, pw) in enumerate(zip(orig_words, par_words)):
            if ow != pw:
                diverge_idx = i
                break
        else:
            diverge_idx = min(len(orig_words), len(par_words))

        lines.append(f"**Shared tokens before first divergence:** {diverge_idx}\n")

        if diverge_idx > 0 and diverge_idx < len(par_toks):
            shared_par = clean_tokens(par_toks[:diverge_idx])
            post_div = clean_tokens(par_toks[diverge_idx:diverge_idx + 20])

            shared_s2 = statistics.mean(t["s2"] for t in shared_par) if shared_par else float("nan")
            post_s2 = statistics.mean(t["s2"] for t in post_div) if post_div else float("nan")
            div_token = par_toks[diverge_idx]["token"] if diverge_idx < len(par_toks) else "?"
            div_s2 = par_toks[diverge_idx]["s2"] if diverge_idx < len(par_toks) else float("nan")

            orig_div_token = orig_toks[diverge_idx]["token"] if diverge_idx < len(orig_toks) else "?"
            orig_div_s2 = orig_toks[diverge_idx]["s2"] if diverge_idx < len(orig_toks) else float("nan")

            lines.append(f"| Metric | Original | Parody |")
            lines.append(f"|---|---|---|")
            lines.append(f"| Mean S₂ (shared prefix, clean) | "
                         f"{statistics.mean(t['s2'] for t in clean_tokens(orig_toks[:diverge_idx])) if clean_tokens(orig_toks[:diverge_idx]) else 'n/a':.3f} | "
                         f"{shared_s2:.3f} |")
            lines.append(f"| Divergence token | `{orig_div_token.strip()}` (S₂={orig_div_s2:.2f}) | "
                         f"`{div_token.strip()}` (S₂={div_s2:.2f}) |")
            lines.append(f"| Mean S₂ (20 tokens post-divergence) | - | {post_s2:.3f} |\n")

        # Show top 5 highest-S₂ moments in the parody
        par_clean = sorted(clean_tokens(par_toks), key=lambda t: t["s2"], reverse=True)[:5]
        lines.append("**Top 5 highest-S₂ tokens in parody:**\n")
        lines.append("| Token | S₂ | Context |")
        lines.append("|---|---|---|")
        for t in par_clean:
            ctx = t.get("context", "")[-40:].replace("\n", "↵")
            lines.append(f"| `{t['token'].strip()}` | {t['s2']:.2f} | `...{ctx}` |")
        lines.append("")

    # ── 5. Variance comparison: spikiness as a parody signature ───────────────
    lines.append("## Variance as Parody Signature\n")
    lines.append("If parody works by alternating 'evocation' (low S₂) and 'subversion' (high S₂),\n")
    lines.append("parody poems should have HIGHER variance in S₂ than their originals.\n\n")

    for label, poems in [("Parody", parody_poems), ("Parody Original", original_poems)]:
        poem_variances = []
        for r in poems:
            toks = clean_tokens(r["tokens"])
            if len(toks) > 3:
                poem_variances.append(statistics.variance(t["s2"] for t in toks))
        if poem_variances:
            lines.append(f"**{label}** — mean within-poem S₂ variance: {statistics.mean(poem_variances):.3f} "
                         f"(n={len(poem_variances)} poems)\n")

    lines.append("")

    # ── 6. Pope mock-epic vs. Carroll absurdist parody ────────────────────────
    pope = find_poem(results, "The Rape of the Lock (Canto I, opening)")
    if pope:
        pope_toks = clean_tokens(pope["tokens"])
        st = s2_stats(pope_toks)
        lines.append("## Pope's Mock-Epic vs. Carroll's Absurdist Parody\n")
        lines.append("Pope's mock-epic uses *genuine* epic diction (familiar to GPT-2 from Homer, Virgil, Milton)\n")
        lines.append("on a trivial subject. The S₂ should be LOW in the diction phase and possibly spike\n")
        lines.append("at incongruous domestic details (lapdogs, lapdogs, beauty spot).\n\n")
        lines.append(f"**Pope 'Rape of the Lock'** — Mean S₂: {st['mean']:.3f}, StDev: {st['stdev']:.3f}, "
                     f"Variance: {st['variance']:.3f}, +S₂: {st['pos_ratio']:.1%}\n")
        lines.append("\nTop 5 highest-S₂ tokens (the incongruous moments):\n")
        lines.append("| Token | S₂ | Context |")
        lines.append("|---|---|---|")
        for t in sorted(pope_toks, key=lambda x: x["s2"], reverse=True)[:5]:
            ctx = t.get("context", "")[-40:].replace("\n", "↵")
            lines.append(f"| `{t['token'].strip()}` | {t['s2']:.2f} | `...{ctx}` |")

    lines.append("")

    # ── 7. Summary stats for saving ───────────────────────────────────────────
    summary = {
        "parody_mean_s2": group_stats.get("Parody", {}).get("mean"),
        "original_mean_s2": group_stats.get("Parody Original", {}).get("mean"),
        "parody_variance": group_stats.get("Parody", {}).get("variance"),
        "original_variance": group_stats.get("Parody Original", {}).get("variance"),
        "parody_high_ratio": group_stats.get("Parody", {}).get("high_ratio"),
        "original_high_ratio": group_stats.get("Parody Original", {}).get("high_ratio"),
    }

    return lines, summary


def main():
    print("Loading corpus results...")
    results = load_results()

    print(f"Loaded {len(results)} texts.")
    parody_count = sum(1 for r in results if r["metadata"]["era"] in ("parody", "parody_original"))
    print(f"Parody/original poems: {parody_count}")

    if parody_count == 0:
        print("ERROR: No parody poems found in corpus_results.json.")
        print("Run engine.py first to process the updated corpus.")
        sys.exit(1)

    print("Running parody S₂ analysis...")
    lines, summary = run_parody_analysis(results)

    # Write output
    output_path = os.path.join(FINDINGS_DIR, "parody_s2.md")
    with open(output_path, "w") as f:
        f.write("# Parody, Pastiche, and Literary Subversion: S₂ Analysis\n")
        f.write("**Date:** 2026-10-10\n")
        f.write("**Experiment:** `experiments/parody_s2.py`\n\n")
        f.write("## Question\n")
        f.write("Does parody achieve its comic and critical effect through an information-theoretic mechanism?\n")
        f.write("Specifically: does parody *evoke* familiar language (GPT-2 is confident → LOW entropy → LOW S₂)\n")
        f.write("and then *subvert* it at key moments (HIGH S₂ spikes where the poet deviates from expectation)?\n\n")
        f.write("**Corpus:** Lewis Carroll parodies of Watts and Southey; Pope's mock-epic *Rape of the Lock*;\n")
        f.write("paired with their source texts as a `parody_original` control.\n\n")
        f.write("---\n\n")
        f.write("\n".join(lines))
        f.write("\n\n---\n\n")
        f.write("## Summary\n\n")
        if summary.get("parody_mean_s2") is not None:
            f.write(f"- **Parody mean S₂:** {summary['parody_mean_s2']:.3f}\n")
            f.write(f"- **Original mean S₂:** {summary['original_mean_s2']:.3f}\n")
            f.write(f"- **Parody variance:** {summary['parody_variance']:.3f}\n")
            f.write(f"- **Original variance:** {summary['original_variance']:.3f}\n")
            f.write(f"- **Parody high-S₂ ratio:** {summary['parody_high_ratio']:.1%}\n")
            f.write(f"- **Original high-S₂ ratio:** {summary['original_high_ratio']:.1%}\n\n")

        # Write interpretation
        if summary.get("parody_variance") and summary.get("original_variance"):
            if summary["parody_variance"] > summary["original_variance"]:
                f.write("**Finding:** Parody poems show HIGHER S₂ variance than their source texts, "
                        "consistent with the hypothesis that parody oscillates between\n"
                        "evocation (low S₂) and subversion (high S₂) more sharply than ordinary verse.\n")
            else:
                f.write("**Finding:** Parody poems do NOT show higher S₂ variance than originals. "
                        "The evocation-subversion mechanism may not operate at the token level,\n"
                        "or GPT-2's training on Carroll/Pope has normalized these texts.\n")

        f.write("\n## Suggested Next Steps\n\n")
        f.write("1. Extend corpus with more parody pairs (Virgil/Virgil parodies, "
                "Eliot self-parody, etc.)\n")
        f.write("2. Align parody/original at the sentence level (not just prefix) "
                "to better isolate divergence points\n")
        f.write("3. Compute semantic distance (word2vec/sentence embeddings) at divergence tokens — "
                "do HIGH S₂ tokens also occupy distant semantic space?\n")
        f.write("4. Test whether COMIC parody (Carroll) vs. CRITICAL parody (mock-epic) "
                "show different S₂ profiles\n")

    print(f"Wrote {output_path}")

    # Save JSON summary
    json_path = os.path.join(RESULTS_DIR, "parody_s2.json") if False else os.path.join(
        os.path.dirname(__file__), "..", "findings", "parody_s2.json")
    with open(json_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"Wrote {json_path}")

    return summary


if __name__ == "__main__":
    main()
