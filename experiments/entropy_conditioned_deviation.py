"""
Entropy-Conditioned Deviation Analysis
=======================================
Research question: When does the Straussian gap matter most?

S2 = surprisal - entropy. But not all S2 is equal:
- High S2 in a HIGH-entropy context: poet deviated when model was already uncertain
  → less "Straussian" since any word would be somewhat surprising
- High S2 in a LOW-entropy context: poet defied a confident prediction
  → maximum "Straussian" — the model was sure, and the poet said something else

We call deviation in low-entropy contexts "True Straussian" moments.

This analysis:
1. Bins tokens by entropy quartile
2. Computes deviation rates and avg S2 per bin
3. Computes a "True Straussian Score" per poet/era (% of low-entropy tokens
   where S2 > 0 — i.e., poet beat the model's confident prediction)
4. Compares poets and eras on this refined metric
"""

import json
import math
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                             "results", "corpus_results.json")


def load_corpus():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def get_clean_tokens(poem):
    """Return tokens excluding stanza-break artifact positions (p_newline >= 0.9)."""
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < 0.9]


def entropy_bins():
    """Return bin labels and thresholds (bits)."""
    return [
        ("very_low  (< 2 bits)",  2.0),
        ("low       (2–5 bits)",  5.0),
        ("medium    (5–8 bits)",  8.0),
        ("high      (> 8 bits)", float("inf")),
    ]


def classify_entropy(entropy_val):
    for label, threshold in entropy_bins():
        if entropy_val < threshold:
            return label
    return entropy_bins()[-1][0]


def analyze():
    corpus = load_corpus()

    # Filter to non-control English poems
    poems = [p for p in corpus
             if p["metadata"].get("era") != "control"
             and p["metadata"].get("language", "en") == "en"]

    control = [p for p in corpus
               if p["metadata"].get("era") == "control"]

    print(f"Analyzing {len(poems)} poems, {len(control)} control texts\n")

    # === Global entropy-bin statistics ===
    bins = {label: {"n": 0, "n_pos_s2": 0, "s2_sum": 0.0, "s2_vals": []}
            for label, _ in entropy_bins()}

    for poem in poems + control:
        is_control = poem["metadata"].get("genre") in ("control", "prose_control")
        tokens = get_clean_tokens(poem)
        for t in tokens:
            ent = t.get("entropy", 0)
            s2 = t.get("s2", 0)
            label = classify_entropy(ent)
            d = bins[label]
            d["n"] += 1
            d["s2_sum"] += s2
            d["s2_vals"].append(s2)
            if s2 > 0:
                d["n_pos_s2"] += 1

    # === Per-poem metrics ===
    poem_metrics = []
    LOW_ENT_THRESHOLD = 5.0   # "model was confident" if entropy < 5 bits

    for poem in poems:
        tokens = get_clean_tokens(poem)
        if len(tokens) < 10:
            continue

        # Standard avg S2
        s2_vals = [t["s2"] for t in tokens]
        avg_s2 = sum(s2_vals) / len(s2_vals)

        # Low-entropy tokens
        low_ent = [t for t in tokens if t.get("entropy", 0) < LOW_ENT_THRESHOLD]
        high_ent = [t for t in tokens if t.get("entropy", 0) >= LOW_ENT_THRESHOLD]

        if len(low_ent) < 3:
            continue

        # True Straussian: % of low-entropy tokens where poet defied confident prediction
        true_straussian = sum(1 for t in low_ent if t["s2"] > 0) / len(low_ent)

        # Uncertainty exploitation: % of high-ent tokens where poet deviated
        uncertainty_exploit = (sum(1 for t in high_ent if t["s2"] > 0) / len(high_ent)
                               if high_ent else 0.0)

        # Avg S2 conditioned on entropy
        low_avg_s2 = sum(t["s2"] for t in low_ent) / len(low_ent)
        high_avg_s2 = (sum(t["s2"] for t in high_ent) / len(high_ent)
                       if high_ent else 0.0)

        poem_metrics.append({
            "title": poem["metadata"]["title"],
            "author": poem["metadata"]["author"],
            "era": poem["metadata"].get("era", "unknown"),
            "avg_s2": avg_s2,
            "true_straussian": true_straussian,
            "uncertainty_exploit": uncertainty_exploit,
            "low_avg_s2": low_avg_s2,
            "high_avg_s2": high_avg_s2,
            "n_low_ent": len(low_ent),
            "n_high_ent": len(high_ent),
            "n_tokens": len(tokens),
        })

    # === Author aggregates ===
    author_data = defaultdict(list)
    for m in poem_metrics:
        author_data[m["author"]].append(m)

    author_stats = []
    for author, mlist in author_data.items():
        if len(mlist) < 1:
            continue
        ts_vals = [m["true_straussian"] for m in mlist]
        ue_vals = [m["uncertainty_exploit"] for m in mlist]
        s2_vals = [m["avg_s2"] for m in mlist]
        author_stats.append({
            "author": author,
            "n_poems": len(mlist),
            "avg_true_straussian": sum(ts_vals) / len(ts_vals),
            "avg_uncertainty_exploit": sum(ue_vals) / len(ue_vals),
            "avg_s2": sum(s2_vals) / len(s2_vals),
            "ts_gap": (sum(ts_vals) / len(ts_vals)) - (sum(ue_vals) / len(ue_vals)),
        })

    author_stats.sort(key=lambda x: x["avg_true_straussian"], reverse=True)

    # === Era aggregates ===
    era_data = defaultdict(list)
    for m in poem_metrics:
        era_data[m["era"]].append(m)

    era_stats = []
    for era, mlist in era_data.items():
        if len(mlist) < 2:
            continue
        ts_vals = [m["true_straussian"] for m in mlist]
        ue_vals = [m["uncertainty_exploit"] for m in mlist]
        era_stats.append({
            "era": era,
            "n": len(mlist),
            "avg_true_straussian": sum(ts_vals) / len(ts_vals),
            "avg_uncertainty_exploit": sum(ue_vals) / len(ue_vals),
            "ts_gap": (sum(ts_vals) / len(ts_vals)) - (sum(ue_vals) / len(ue_vals)),
        })

    era_stats.sort(key=lambda x: x["avg_true_straussian"], reverse=True)

    # === Control comparison ===
    control_metrics = []
    for poem in control:
        tokens = get_clean_tokens(poem)
        if len(tokens) < 5:
            continue
        low_ent = [t for t in tokens if t.get("entropy", 0) < LOW_ENT_THRESHOLD]
        if not low_ent:
            continue
        control_metrics.append(sum(1 for t in low_ent if t["s2"] > 0) / len(low_ent))
    control_ts = sum(control_metrics) / len(control_metrics) if control_metrics else 0

    # === Top true-Straussian poems ===
    poem_metrics.sort(key=lambda x: x["true_straussian"], reverse=True)

    return {
        "poem_metrics": poem_metrics,
        "author_stats": author_stats,
        "era_stats": era_stats,
        "control_ts": control_ts,
        "low_ent_threshold": LOW_ENT_THRESHOLD,
    }


def format_report(results):
    pm = results["poem_metrics"]
    author_stats = results["author_stats"]
    era_stats = results["era_stats"]
    control_ts = results["control_ts"]
    threshold = results["low_ent_threshold"]

    lines = []
    lines.append("# Entropy-Conditioned Deviation: The 'True Straussian' Score")
    lines.append("")
    lines.append(f"**Date:** 2026-10-06")
    lines.append(f"**Low-entropy threshold:** {threshold} bits (model 'confident' below this)")
    lines.append("")
    lines.append("## Research Question")
    lines.append("")
    lines.append("Not all S₂ is equal. A positive S₂ in a *high-entropy* context means the poet chose")
    lines.append("something less likely when the model was already uncertain — not very Straussian,")
    lines.append("since any word would be moderately surprising. A positive S₂ in a *low-entropy*")
    lines.append("context means the poet defied a confident prediction — the model was sure of what")
    lines.append("came next, and the poet said something else entirely.")
    lines.append("")
    lines.append("**True Straussian Score** = fraction of low-entropy tokens where S₂ > 0.")
    lines.append("This measures *precision deviation*: the ability to defy confident expectations.")
    lines.append("")
    lines.append(f"**Control prose True Straussian baseline:** {control_ts:.1%}")
    lines.append("")

    lines.append("## Top 15 Poems by True Straussian Score")
    lines.append("")
    lines.append("| Poem | Author | Era | True Straussian | Uncertainty Exploit | Avg S₂ | n_low_ent |")
    lines.append("|---|---|---|---|---|---|---|")
    for m in pm[:15]:
        lines.append(
            f"| {m['title'][:45]} | {m['author'][:30]} | {m['era']} "
            f"| **{m['true_straussian']:.1%}** | {m['uncertainty_exploit']:.1%} "
            f"| {m['avg_s2']:+.2f} | {m['n_low_ent']} |"
        )

    lines.append("")
    lines.append("## Bottom 10 Poems (lowest True Straussian)")
    lines.append("")
    lines.append("| Poem | Author | Era | True Straussian | Avg S₂ |")
    lines.append("|---|---|---|---|---|")
    for m in sorted(pm, key=lambda x: x["true_straussian"])[:10]:
        lines.append(
            f"| {m['title'][:45]} | {m['author'][:30]} | {m['era']} "
            f"| **{m['true_straussian']:.1%}** | {m['avg_s2']:+.2f} |"
        )

    lines.append("")
    lines.append("## Author Rankings by True Straussian Score")
    lines.append("")
    lines.append("| Author | n | True Straussian | Uncertainty Exploit | TS Gap | Avg S₂ |")
    lines.append("|---|---|---|---|---|---|")
    for a in author_stats[:30]:
        lines.append(
            f"| {a['author'][:35]} | {a['n_poems']} "
            f"| **{a['avg_true_straussian']:.1%}** | {a['avg_uncertainty_exploit']:.1%} "
            f"| {a['ts_gap']:+.1%} | {a['avg_s2']:+.2f} |"
        )

    lines.append("")
    lines.append("## Era Rankings by True Straussian Score")
    lines.append("")
    lines.append("| Era | n | True Straussian | Uncertainty Exploit | TS Gap |")
    lines.append("|---|---|---|---|---|")
    for e in era_stats:
        lines.append(
            f"| {e['era']} | {e['n']} "
            f"| **{e['avg_true_straussian']:.1%}** | {e['avg_uncertainty_exploit']:.1%} "
            f"| {e['ts_gap']:+.1%} |"
        )

    lines.append("")
    lines.append("## Key Findings")
    lines.append("")

    # Compute summary stats
    all_ts = [m["true_straussian"] for m in pm]
    all_ue = [m["uncertainty_exploit"] for m in pm]
    median_ts = sorted(all_ts)[len(all_ts)//2]
    median_ue = sorted(all_ue)[len(all_ue)//2]

    lines.append(f"1. **Poetry median True Straussian score: {median_ts:.1%}** vs prose baseline: {control_ts:.1%}")
    lines.append(f"   The gap ({median_ts - control_ts:+.1%}) represents the 'confidence-adjusted' Straussian gap.")
    lines.append("")
    lines.append(f"2. **Poetry median Uncertainty Exploitation: {median_ue:.1%}** (deviating when model uncertain).")
    lines.append(f"   True Straussian - Uncertainty Exploit gap: {median_ts - median_ue:+.1%}")
    lines.append(f"   Positive gap means poets preferentially defy *confident* predictions more than uncertain ones.")
    lines.append("")

    # Top author insights
    top3 = author_stats[:3]
    lines.append(f"3. **Highest True Straussian authors:** "
                 + ", ".join(f"{a['author']} ({a['avg_true_straussian']:.1%})" for a in top3))
    lines.append(f"   These poets most consistently deviate *when the model is sure* of what comes next.")
    lines.append("")

    # TS gap insight
    top_ts_gap = sorted(author_stats, key=lambda x: x["ts_gap"], reverse=True)[:3]
    lines.append(f"4. **Largest TS Gap (precision > uncertainty deviation):** "
                 + ", ".join(f"{a['author']} ({a['ts_gap']:+.1%})" for a in top_ts_gap))
    lines.append(f"   These authors disproportionately defy confident predictions vs. uncertain contexts.")
    lines.append("")

    lines.append("## Interpretation")
    lines.append("")
    lines.append("The True Straussian Score refines the S₂ framework. Standard S₂ averages all deviation,")
    lines.append("including 'cheap' deviation in high-entropy contexts where the model has no strong prior.")
    lines.append("The True Straussian score isolates *precision deviation* — the poet's ability to say")
    lines.append("something unexpected precisely when language has its strongest expectations.")
    lines.append("")
    lines.append("This connects to a craft insight: great poetic surprise often works *against* the grain")
    lines.append("of confident syntactic and semantic expectation, not merely in ambiguous contexts.")
    lines.append("The TS score distinguishes poets who surprise us *despite* predictability")
    lines.append("from those who operate in the more permissive space of lexical ambiguity.")
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("- Compute TS score for individual lines to find the most 'precisely Straussian' lines")
    lines.append("- Test if TS score correlates with reader-rated memorability or critical esteem")
    lines.append("- Compare TS score across poem types: are sonnets (highly regular) more 'precisely Straussian'?")
    lines.append("- Examine what the model predicted at low-entropy Straussian moments (the 'suppressed' word)")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running entropy-conditioned deviation analysis...")
    results = analyze()
    report = format_report(results)
    output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                               "findings", "entropy_conditioned_deviation.md")
    with open(output_path, "w") as f:
        f.write(report)
    print(f"Report saved to: {output_path}")
    print("\n--- PREVIEW ---")
    print(report[:3000])
