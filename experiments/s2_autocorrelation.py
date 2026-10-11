"""
S2 Autocorrelation Analysis
============================
Computes the autocorrelation of S2 at lags 1–10 for each poem,
then aggregates by era. Tests whether surprises cluster (positive AC)
or alternate with predictable tokens (negative AC).

New angle: captures the *temporal dynamics* of surprise, not just its
mean or variance. Complements s2_markov_transitions (discrete bins)
and s2_transition_entropy (entropy of transitions) with continuous-value
lag statistics.
"""

import json
import math
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
ARTIFACT_THRESHOLD = 0.9   # filter tokens where p(newline) >= this

LAGS = [1, 2, 3, 5, 10]


def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def pearson_correlation(xs, ys):
    """Compute Pearson r between two equal-length lists."""
    n = len(xs)
    if n < 3:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
    den_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
    den_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
    if den_x < 1e-9 or den_y < 1e-9:
        return None
    return num / (den_x * den_y)


def autocorrelation_at_lag(s2_sequence, lag):
    """Compute autocorrelation of s2_sequence at given lag."""
    if len(s2_sequence) <= lag + 2:
        return None
    xs = s2_sequence[:-lag]
    ys = s2_sequence[lag:]
    return pearson_correlation(xs, ys)


def get_clean_s2(poem):
    """Return artifact-filtered S2 sequence for a poem."""
    return [
        t["s2"]
        for t in poem["tokens"]
        if t.get("p_newline", 0) < ARTIFACT_THRESHOLD
    ]


def run():
    data = load_data()

    # Per-poem autocorrelation
    era_acs = defaultdict(lambda: {lag: [] for lag in LAGS})
    global_acs = {lag: [] for lag in LAGS}
    era_poem_counts = defaultdict(int)

    poem_results = []
    for poem in data:
        era = poem["metadata"]["era"]
        if era == "control":
            continue
        s2_seq = get_clean_s2(poem)
        if len(s2_seq) < 15:
            continue

        poem_acs = {}
        for lag in LAGS:
            ac = autocorrelation_at_lag(s2_seq, lag)
            if ac is not None:
                era_acs[era][lag].append(ac)
                global_acs[lag].append(ac)
                poem_acs[lag] = ac

        poem_results.append({
            "title": poem["metadata"]["title"],
            "author": poem["metadata"]["author"],
            "era": era,
            "n_tokens": len(s2_seq),
            "acs": poem_acs,
            "lag1": poem_acs.get(1),
        })
        era_poem_counts[era] += 1

    # Aggregate by era: mean autocorrelation at each lag
    era_summaries = {}
    for era, lag_dict in era_acs.items():
        era_summaries[era] = {
            "n": era_poem_counts[era],
            "mean_acs": {
                lag: (sum(vals) / len(vals) if vals else None)
                for lag, vals in lag_dict.items()
            }
        }

    # Global autocorrelation
    global_means = {
        lag: (sum(vals) / len(vals) if vals else None)
        for lag, vals in global_acs.items()
    }

    # Sort eras by lag-1 autocorrelation
    ranked_eras = sorted(
        era_summaries.items(),
        key=lambda x: x[1]["mean_acs"].get(1) or 0,
        reverse=True
    )

    # Find poems with most positive/negative lag-1 AC
    lag1_poems = [p for p in poem_results if p["lag1"] is not None]
    top_cluster = sorted(lag1_poems, key=lambda p: p["lag1"], reverse=True)[:10]
    top_alternate = sorted(lag1_poems, key=lambda p: p["lag1"])[:10]

    return {
        "ranked_eras": ranked_eras,
        "global_means": global_means,
        "top_clustering_poems": top_cluster,
        "top_alternating_poems": top_alternate,
        "n_poems": len(poem_results),
    }


def format_report(results):
    ranked = results["ranked_eras"]
    global_means = results["global_means"]
    top_cluster = results["top_clustering_poems"]
    top_alt = results["top_alternating_poems"]

    lines = [
        "# S2 Autocorrelation Analysis",
        "",
        "**Question:** After a surprising token, is the next token also surprising? Do surprises cluster (positive autocorrelation) or alternate with predictable tokens (negative autocorrelation)?",
        "",
        "**Method:** Compute Pearson autocorrelation of the artifact-filtered S2 sequence at lags 1, 2, 3, 5, 10 for each poem. Aggregate by era.",
        "",
        f"**Corpus:** {results['n_poems']} poems analyzed.",
        "",
        "## Global Autocorrelation Profile",
        "",
        "| Lag | Mean AC (all poetry) | Interpretation |",
        "|-----|---------------------|----------------|",
    ]

    interp = {
        1: "immediate: does S2 predict next token's S2?",
        2: "2-token memory",
        3: "3-token memory",
        5: "5-token memory",
        10: "10-token memory",
    }
    for lag in LAGS:
        ac = global_means.get(lag)
        ac_str = f"{ac:.4f}" if ac is not None else "—"
        sign = "+" if ac and ac > 0 else ""
        lines.append(f"| {lag} | {sign}{ac_str} | {interp.get(lag, '')} |")

    lines += [
        "",
        "**Finding:** " + (
            "Poetry has **positive** lag-1 autocorrelation — surprises cluster in runs, "
            "suggesting the poet sustains unexpected modes for several tokens."
            if (global_means.get(1) or 0) > 0.01
            else "Poetry has **negative** lag-1 autocorrelation — surprises alternate with "
            "predictable tokens, like a 'call-and-response' pattern."
            if (global_means.get(1) or 0) < -0.01
            else "Poetry has near-zero lag-1 autocorrelation — surprises are essentially uncorrelated token-to-token."
        ),
        "",
        "## Era Rankings by Lag-1 Autocorrelation",
        "",
        "Sorted by mean lag-1 AC (most clustered surprises → most alternating).",
        "",
        "| Era | n poems | Lag-1 | Lag-2 | Lag-3 | Lag-5 | Lag-10 |",
        "|-----|---------|-------|-------|-------|-------|--------|",
    ]

    for era, summary in ranked:
        n = summary["n"]
        acs = summary["mean_acs"]
        def fmt(v):
            if v is None:
                return "—"
            return f"{v:+.3f}"
        lines.append(
            f"| {era} | {n} | {fmt(acs.get(1))} | {fmt(acs.get(2))} | "
            f"{fmt(acs.get(3))} | {fmt(acs.get(5))} | {fmt(acs.get(10))} |"
        )

    lines += [
        "",
        "## Poems with Most *Clustered* Surprises (Highest Lag-1 AC)",
        "",
        "These poems sustain surprise across consecutive tokens:",
        "",
        "| Poem | Author | Era | Lag-1 AC | N tokens |",
        "|------|--------|-----|----------|----------|",
    ]
    for p in top_cluster:
        lines.append(
            f"| {p['title'][:40]} | {p['author'][:25]} | {p['era']} | "
            f"{p['lag1']:+.3f} | {p['n_tokens']} |"
        )

    lines += [
        "",
        "## Poems with Most *Alternating* Surprises (Lowest Lag-1 AC)",
        "",
        "These poems create a 'surprise-then-settle' rhythm:",
        "",
        "| Poem | Author | Era | Lag-1 AC | N tokens |",
        "|------|--------|-----|----------|----------|",
    ]
    for p in top_alt:
        lines.append(
            f"| {p['title'][:40]} | {p['author'][:25]} | {p['era']} | "
            f"{p['lag1']:+.3f} | {p['n_tokens']} |"
        )

    # Interpretation
    lines += [
        "",
        "## Interpretation",
        "",
        "The autocorrelation structure reveals two distinct poetic strategies:",
        "",
        "- **Sustained deviation** (high positive lag-1 AC): the poet enters an 'unexpected mode' for several tokens in a row. Associated with long noun phrases, appositive chains, and technical vocabulary runs.",
        "- **Spike-and-recover** (negative lag-1 AC): a single surprising word followed by a conventional one, then another spike. This 'call-and-response' structure may feel more rhythmically controlled.",
        "",
        "The decay of autocorrelation across lags (lag-1 vs lag-10) characterizes the **memory length** of each poem's surprise structure: how many tokens does a surprise 'echo' forward?",
        "",
        "## Suggested Next Steps",
        "",
        "1. **Align with phonological meter**: do stressed syllables coincide with AC peaks?",
        "2. **Compare within-poem AC by stanza**: does lag-1 AC increase or decrease in later stanzas?",
        "3. **Test the 'surprise economy' hypothesis**: do poems with high mean S2 have lower lag-1 AC (they 'spread out' surprises) while low-mean-S2 poems cluster their rare surprises?",
        "4. **Cross-language check**: do German modernists (highest clean S2) also have highest lag-1 AC?",
    ]

    return "\n".join(lines)


if __name__ == "__main__":
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    print("Running S2 autocorrelation analysis...")
    results = run()
    report = format_report(results)
    print(report[:3000])

    output_path = "findings/s2_autocorrelation.md"
    with open(output_path, "w") as f:
        f.write(report)
    print(f"\nSaved to {output_path}")

    # Also save JSON
    import json as _json
    json_path = "findings/s2_autocorrelation.json"
    with open(json_path, "w") as f:
        _json.dump({
            "global_means": {str(k): v for k, v in results["global_means"].items()},
            "era_rankings": [
                {
                    "era": era,
                    "n": summary["n"],
                    "acs": {str(k): v for k, v in summary["mean_acs"].items()},
                }
                for era, summary in results["ranked_eras"]
            ],
            "top_clustering_poems": results["top_clustering_poems"],
            "top_alternating_poems": results["top_alternating_poems"],
        }, f, indent=2)
    print(f"JSON saved to {json_path}")
