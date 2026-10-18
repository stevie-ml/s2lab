"""
The Language Poetry Paradox

Research question: Why does Language Poetry — theoretically the most
experimental / disruptive movement — have LOWER artifact-free S2 than
Beat poetry (and many traditional poetic eras)?

Hypothesis: Language Poetry disrupts SYNTAX but uses relatively common
words. GPT-2 tracks token-by-token predictability. When syntax is fragmented
the model enters high-entropy states — it has no confident expectation —
so even ordinary tokens yield near-zero S2 (surprisal ≈ entropy).
Beat poetry by contrast uses long cumulative structures that allow GPT-2
to form real expectations, which are then violated at the lexical level.

The key S2 decomposition:
  S2 = S - H
  where S = surprisal (-log p(chosen token))
        H = entropy of the full distribution

High H, moderate S → negative S2  (model confused, poet plays it safe)
Low H, high S      → positive S2  (model confident, poet defies it)

This experiment tests whether Language Poetry is characterized by
ENTROPY-FLOODING: making the model uniformly uncertain (high H) while
making relatively safe lexical choices.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from engine import load_results
import statistics

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "corpus_results.json")


def artifact_free(tokens):
    """Return tokens with p_newline < 0.9 (exclude stanza-break artifacts)."""
    return [t for t in tokens if t.get("p_newline", 0) < 0.9]


def poem_stats(result):
    """Compute detailed stats for one poem."""
    tokens = result["tokens"]
    clean = artifact_free(tokens)
    if not clean:
        clean = tokens  # fallback

    surprisals = [t["surprisal"] for t in clean]
    entropies  = [t["entropy"]   for t in clean]
    s2s        = [t["s2"]        for t in clean]

    avg_S  = statistics.mean(surprisals)
    avg_H  = statistics.mean(entropies)
    avg_S2 = statistics.mean(s2s)
    std_S2 = statistics.stdev(s2s) if len(s2s) > 1 else 0.0

    # Fraction of tokens where H > 9 (model in high-entropy / confused state)
    frac_high_entropy = sum(1 for h in entropies if h > 9) / len(entropies)

    # Fraction of tokens where poet's rank = 1 (most probable choice)
    frac_rank1 = sum(1 for t in clean if t.get("rank", 99) == 1) / len(clean)

    # Mean rank of chosen token
    avg_rank = statistics.mean(t.get("rank", 50000) for t in clean)

    return {
        "title":  result["metadata"]["title"],
        "author": result["metadata"]["author"],
        "era":    result["metadata"]["era"],
        "n_tokens": len(clean),
        "avg_S":  round(avg_S, 3),
        "avg_H":  round(avg_H, 3),
        "avg_S2": round(avg_S2, 3),
        "std_S2": round(std_S2, 3),
        "frac_high_entropy": round(frac_high_entropy, 3),
        "frac_rank1": round(frac_rank1, 3),
        "avg_rank": round(avg_rank, 1),
    }


def era_aggregate(poem_stats_list):
    """Aggregate stats for a list of poems."""
    if not poem_stats_list:
        return {}
    n = len(poem_stats_list)
    keys = ["avg_S", "avg_H", "avg_S2", "std_S2",
            "frac_high_entropy", "frac_rank1", "avg_rank"]
    agg = {}
    for k in keys:
        vals = [p[k] for p in poem_stats_list]
        agg[k] = round(statistics.mean(vals), 3)
    agg["n_poems"] = n
    agg["total_tokens"] = sum(p["n_tokens"] for p in poem_stats_list)
    return agg


def run():
    results = load_results()

    # Focus eras for the paradox
    TARGET_ERAS = {
        "language":       "Language Poetry",
        "beat":           "Beat",
        "new_york_school":"New York School",
        "surrealist":     "Surrealist",
        "confessional":   "Confessional",
        "modernist":      "Modernist",
        "romantic":       "Romantic",
        "control":        "Control prose",
    }

    era_poems = {era: [] for era in TARGET_ERAS}
    for r in results:
        era = r["metadata"].get("era", "")
        if era in TARGET_ERAS:
            era_poems[era].append(poem_stats(r))

    print("=" * 90)
    print("  THE LANGUAGE POETRY PARADOX")
    print("  Decomposing S2 = S (surprisal) - H (entropy) by era")
    print("=" * 90)
    print()
    print(f"{'Era':<22} {'n':>3} {'avg S':>7} {'avg H':>7} {'avg S2':>7}"
          f" {'σ(S2)':>6} {'Hi-H%':>6} {'Rank1%':>7} {'avg Rank':>9}")
    print("-" * 90)

    agg_rows = []
    for era, label in TARGET_ERAS.items():
        poems = era_poems[era]
        if not poems:
            continue
        agg = era_aggregate(poems)
        row = {
            "label": label,
            "era": era,
            **agg
        }
        agg_rows.append(row)
        print(f"{label:<22} {agg['n_poems']:>3}"
              f" {agg['avg_S']:>7.3f} {agg['avg_H']:>7.3f} {agg['avg_S2']:>7.3f}"
              f" {agg['std_S2']:>6.3f} {agg['frac_high_entropy']*100:>5.1f}%"
              f" {agg['frac_rank1']*100:>6.1f}% {agg['avg_rank']:>9.1f}")

    print()
    print("Per-poem breakdown for Language Poetry vs Beat:")
    print()

    for era in ["language", "beat"]:
        label = TARGET_ERAS[era]
        print(f"  {label}:")
        for p in sorted(era_poems[era], key=lambda x: x["avg_S2"]):
            print(f"    {p['author'][:25]:<26} S={p['avg_S']:.3f}  H={p['avg_H']:.3f}"
                  f"  S2={p['avg_S2']:+.3f}  Hi-H%={p['frac_high_entropy']*100:.0f}%"
                  f"  Rank1%={p['frac_rank1']*100:.0f}%  AvgRank={p['avg_rank']:.0f}")
        print()

    # The core test: does Language Poetry have higher H than Beat?
    lang_agg = era_aggregate(era_poems["language"])
    beat_agg = era_aggregate(era_poems["beat"])

    print("CORE TEST: Language Poetry vs Beat — The Entropy-Flooding Hypothesis")
    print("-" * 60)
    print(f"  Language Poetry  avg H = {lang_agg['avg_H']:.3f}  avg S = {lang_agg['avg_S']:.3f}  avg S2 = {lang_agg['avg_S2']:.3f}")
    print(f"  Beat Poetry      avg H = {beat_agg['avg_H']:.3f}  avg S = {beat_agg['avg_S']:.3f}  avg S2 = {beat_agg['avg_S2']:.3f}")
    print()
    delta_H  = lang_agg['avg_H']  - beat_agg['avg_H']
    delta_S  = lang_agg['avg_S']  - beat_agg['avg_S']
    delta_S2 = lang_agg['avg_S2'] - beat_agg['avg_S2']
    print(f"  ΔH  (Lang - Beat) = {delta_H:+.3f}")
    print(f"  ΔS  (Lang - Beat) = {delta_S:+.3f}")
    print(f"  ΔS2 (Lang - Beat) = {delta_S2:+.3f}")
    print()

    if delta_H > 0.2 and delta_S2 < 0:
        print("  → ENTROPY-FLOODING CONFIRMED: Language Poetry pushes H higher")
        print("    while S barely rises → S2 collapses toward zero / negative.")
    elif delta_H < 0:
        print("  → ENTROPY-FLOODING REJECTED: Beat Poetry actually has higher H.")
        print("    S2 gap explained by S differences, not H differences.")
    else:
        print("  → MIXED RESULT: H differences smaller than expected.")
        print("    Check per-poem breakdown for within-era variation.")

    # Save for write-up
    output = {
        "date": "2026-10-18",
        "era_aggregates": agg_rows,
        "language_poems": era_poems["language"],
        "beat_poems": era_poems["beat"],
        "delta_H": round(delta_H, 3),
        "delta_S": round(delta_S, 3),
        "delta_S2": round(delta_S2, 3),
    }
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "language_poetry_paradox.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return output


if __name__ == "__main__":
    run()
