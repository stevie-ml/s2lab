"""
Oulipo vs. Surrealism: Two roads to surprise.

Oulipo generates unexpected language through formal mathematical constraint
(lipogram, N+7, permutations). Surrealism generates it through automatic
writing and dream logic. Both subvert expectations — but differently.

Hypothesis: Both should show elevated S2, but with different distributional
shapes:
- Oulipo: More UNIFORM high-S2 (constraint applies globally and mechanically)
- Surrealism: More SPIKY (unexpected bursts among more normative passages)
- Oulipo: Lower entropy at surprise moments (model was highly confident,
  constraint forced a different choice)
- Surrealism: Higher entropy at surprise moments (model was genuinely confused,
  not just overridden)
"""

import json
import sys
import math
import statistics

sys.path.insert(0, '.')


def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)


def gini_coefficient(values):
    """Measures inequality in S2 distribution. Higher = spikier."""
    if not values:
        return 0
    n = len(values)
    sorted_vals = sorted(values)
    total = sum(sorted_vals)
    if total == 0:
        return 0
    cumsum = 0
    for i, v in enumerate(sorted_vals):
        cumsum += v
    # Gini = 1 - 2 * (area under Lorenz curve)
    lorenz_sum = sum((i + 1) * v for i, v in enumerate(sorted_vals))
    return 1 - (2 * lorenz_sum) / (n * total) + 1 / n


def kurtosis(values):
    """Excess kurtosis. Higher = heavier tails / spikier distribution."""
    if len(values) < 4:
        return 0
    n = len(values)
    mean = statistics.mean(values)
    std = statistics.stdev(values)
    if std == 0:
        return 0
    kurt = sum(((v - mean) / std) ** 4 for v in values) / n - 3
    return kurt


def analyze_poem(poem_data, artifact_filter=True):
    """Extract S2 metrics from a poem's token data.
    poem_data: dict with 'metadata', 'summary', 'tokens' keys
    """
    tokens = poem_data.get("tokens", [])

    # Filter stanza-break artifacts: tokens where p(newline) >= 0.9
    if artifact_filter:
        tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]

    if not tokens:
        return None

    s2_vals = [t.get("s2", 0) for t in tokens]
    entropy_vals = [t.get("entropy", 0) for t in tokens]
    prob_vals = [t.get("prob", 0) for t in tokens]
    surprisal_vals = [t.get("surprisal", 0) for t in tokens]

    positive_s2 = [v for v in s2_vals if v > 0]
    negative_s2 = [v for v in s2_vals if v < 0]

    # Tokens in top-S2 moments
    threshold = statistics.mean(s2_vals) + statistics.stdev(s2_vals) if len(s2_vals) > 1 else 0
    spike_tokens = [t for t in tokens if t.get("s2", 0) > threshold]

    # Entropy at spike positions
    spike_entropy = [t.get("entropy", 0) for t in spike_tokens] if spike_tokens else [0]

    return {
        "n_tokens": len(tokens),
        "mean_s2": statistics.mean(s2_vals),
        "std_s2": statistics.stdev(s2_vals) if len(s2_vals) > 1 else 0,
        "mean_entropy": statistics.mean(entropy_vals),
        "positive_s2_ratio": len(positive_s2) / len(s2_vals),
        "max_s2": max(s2_vals),
        "gini": gini_coefficient([max(v, 0) for v in s2_vals]),
        "kurtosis": kurtosis(s2_vals),
        "spike_entropy": statistics.mean(spike_entropy),
        "mean_surprisal": statistics.mean(surprisal_vals),
        "n_spikes": len(spike_tokens),
        # The "confident wrong" rate: high-S2 token where entropy was low
        # (model was confident but poet chose differently)
        "confident_wrong_ratio": sum(
            1 for t in spike_tokens
            if t.get("entropy", 0) < 3.0  # low entropy = model was confident
        ) / max(len(spike_tokens), 1),
    }


def group_analysis(poems_data, group_poems, label):
    """Analyze a group of poems and return aggregate statistics."""
    results = []
    for poem_meta in group_poems:
        title = poem_meta.get("title", "")
        # Match against corpus results
        for key, data in poems_data.items():
            if title in key or poem_meta.get("author", "") in key:
                metrics = analyze_poem(data)
                if metrics:
                    metrics["title"] = title
                    metrics["author"] = poem_meta.get("author", "?")
                    results.append(metrics)
                break

    if not results:
        return None

    def avg(key):
        vals = [r[key] for r in results if key in r]
        return statistics.mean(vals) if vals else 0

    def stdev(key):
        vals = [r[key] for r in results if key in r]
        return statistics.stdev(vals) if len(vals) > 1 else 0

    return {
        "label": label,
        "n_poems": len(results),
        "poems": results,
        "mean_s2": avg("mean_s2"),
        "std_s2_within": avg("std_s2"),
        "mean_entropy": avg("mean_entropy"),
        "positive_ratio": avg("positive_s2_ratio"),
        "max_s2": avg("max_s2"),
        "gini": avg("gini"),
        "kurtosis": avg("kurtosis"),
        "spike_entropy": avg("spike_entropy"),
        "confident_wrong": avg("confident_wrong_ratio"),
        "between_poem_std": stdev("mean_s2"),
    }


def main():
    corpus = load_corpus()  # list of dicts with 'metadata', 'summary', 'tokens'

    # Group by era from metadata
    era_groups = {}
    for item in corpus:
        era = item.get("metadata", {}).get("era", "unknown")
        era_groups.setdefault(era, []).append(item)

    target_eras = ["oulipo", "surrealist", "language", "found_poetry", "modernist", "romantic"]
    results_by_group = {}

    for era in target_eras:
        if era not in era_groups:
            continue
        matched = []
        for item in era_groups[era]:
            meta = item.get("metadata", {})
            metrics = analyze_poem(item)
            if metrics:
                metrics["title"] = meta.get("title", "?")
                metrics["author"] = meta.get("author", "?")
                matched.append(metrics)

        if matched:
            def avg(key, m=matched):
                vals = [r[key] for r in m]
                return statistics.mean(vals) if vals else 0

            def std(key, m=matched):
                vals = [r[key] for r in m]
                return statistics.stdev(vals) if len(vals) > 1 else 0

            results_by_group[era] = {
                "label": era,
                "n": len(matched),
                "poems": matched,
                "mean_s2": avg("mean_s2"),
                "std_s2_within": avg("std_s2"),
                "mean_entropy": avg("mean_entropy"),
                "positive_ratio": avg("positive_s2_ratio"),
                "max_s2": avg("max_s2"),
                "gini": avg("gini"),
                "kurtosis": avg("kurtosis"),
                "spike_entropy": avg("spike_entropy"),
                "confident_wrong": avg("confident_wrong_ratio"),
                "between_poem_std": std("mean_s2"),
            }

    # Print results
    print("\n=== OULIPO vs. SURREALISM: Comparative S2 Analysis ===\n")

    print(f"{'Group':<20} {'N':>3} {'Mean S2':>8} {'StdDev(S2)':>10} {'PosRatio':>9} {'Kurtosis':>9} {'Gini':>6} {'SpikeH':>7} {'ConfWrong':>9}")
    print("-" * 90)

    order = ["oulipo", "surrealist", "language", "found_poetry", "modernist", "romantic"]
    for era in order:
        if era not in results_by_group:
            continue
        g = results_by_group[era]
        print(f"{era:<20} {g['n']:>3} {g['mean_s2']:>8.3f} {g['std_s2_within']:>10.3f} "
              f"{g['positive_ratio']:>9.3f} {g['kurtosis']:>9.3f} {g['gini']:>6.3f} "
              f"{g['spike_entropy']:>7.3f} {g['confident_wrong']:>9.3f}")

    print("\n=== Per-poem breakdown: OULIPO ===")
    if "oulipo" in results_by_group:
        for p in results_by_group["oulipo"]["poems"]:
            print(f"  {p['title'][:50]:<50} S2={p['mean_s2']:+.3f} kurtosis={p['kurtosis']:.3f} gini={p['gini']:.3f}")

    print("\n=== Per-poem breakdown: SURREALIST ===")
    if "surrealist" in results_by_group:
        for p in results_by_group["surrealist"]["poems"]:
            print(f"  {p['title'][:50]:<50} S2={p['mean_s2']:+.3f} kurtosis={p['kurtosis']:.3f} gini={p['gini']:.3f}")

    # Key contrasts
    print("\n=== KEY CONTRASTS ===")
    if "oulipo" in results_by_group and "surrealist" in results_by_group:
        o = results_by_group["oulipo"]
        s = results_by_group["surrealist"]
        print(f"Kurtosis (spikiness) — Oulipo: {o['kurtosis']:.3f}, Surrealist: {s['kurtosis']:.3f}")
        print(f"  -> {'Oulipo' if o['kurtosis'] > s['kurtosis'] else 'Surrealism'} is spikier")
        print(f"Gini (inequality) — Oulipo: {o['gini']:.3f}, Surrealist: {s['gini']:.3f}")
        print(f"  -> {'Oulipo' if o['gini'] > s['gini'] else 'Surrealism'} has more unequal S2 distribution")
        print(f"Entropy at spikes — Oulipo: {o['spike_entropy']:.3f} bits, Surrealist: {s['spike_entropy']:.3f} bits")
        print(f"  -> {'Oulipo' if o['spike_entropy'] < s['spike_entropy'] else 'Surrealism'} surprises model when it was more confident")
        print(f"'Confident wrong' — Oulipo: {o['confident_wrong']:.3f}, Surrealist: {s['confident_wrong']:.3f}")
        print(f"  -> {'Oulipo' if o['confident_wrong'] > s['confident_wrong'] else 'Surrealism'} more often overrides confident model")
        print(f"Within-poem S2 std — Oulipo: {o['std_s2_within']:.3f}, Surrealist: {s['std_s2_within']:.3f}")
        print(f"  -> {'Oulipo' if o['std_s2_within'] < s['std_s2_within'] else 'Surrealism'} has more uniform S2 within poems")

    # Save results
    with open("results/oulipo_vs_surrealist.json", "w") as f:
        # Convert for JSON serialization
        output = {}
        for era, data in results_by_group.items():
            d = dict(data)
            d.pop("poems", None)  # remove per-poem detail for brevity
            output[era] = d
        json.dump(output, f, indent=2)

    print("\nResults saved to results/oulipo_vs_surrealist.json")
    return results_by_group


if __name__ == "__main__":
    main()
