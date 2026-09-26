"""
S2 Markov Transitions: Is Poetic Surprise a Markov Chain?

Research question: Given the S2 level at token t, what is the conditional
distribution of S2 at token t+1? Do high-S2 moments self-reinforce (persistence)
or self-correct (reversion)? Does the transition structure differ by era?

This extends:
- s2_zone_topology.md (which asks if high-S2 clusters)
- spike_symmetry.md (which asks if spikes are temporally balanced)
by giving the full Markov transition probability matrix.
"""

import json
import os
import sys
from collections import defaultdict
import statistics

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

ARTIFACT_P = 0.90


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def clean_tokens(tokens):
    return [t for t in tokens if newline_prob(t) < ARTIFACT_P]


def s2_bucket(s2):
    """Discretize S2 into 5 levels."""
    if s2 < -3.0:
        return "DEEP_CONFORM"
    elif s2 < -0.5:
        return "CONFORM"
    elif s2 < 0.5:
        return "NEUTRAL"
    elif s2 < 3.0:
        return "SURPRISE"
    else:
        return "HIGH_SURPRISE"


BUCKETS = ["DEEP_CONFORM", "CONFORM", "NEUTRAL", "SURPRISE", "HIGH_SURPRISE"]
BUCKET_LABELS = {
    "DEEP_CONFORM": "Deep Conform (<-3)",
    "CONFORM": "Conform (-3 to -0.5)",
    "NEUTRAL": "Neutral (-0.5 to 0.5)",
    "SURPRISE": "Surprise (0.5 to 3)",
    "HIGH_SURPRISE": "High Surprise (>3)",
}


def compute_transitions(token_list):
    """Return list of (bucket_t, bucket_t1) pairs from consecutive tokens."""
    pairs = []
    toks = clean_tokens(token_list)
    for i in range(len(toks) - 1):
        b0 = s2_bucket(toks[i]["s2"])
        b1 = s2_bucket(toks[i + 1]["s2"])
        pairs.append((b0, b1))
    return pairs


def build_transition_matrix(pairs):
    """Build row-normalized transition matrix. Returns dict[from_bucket][to_bucket] = probability."""
    counts = defaultdict(lambda: defaultdict(int))
    for b0, b1 in pairs:
        counts[b0][b1] += 1

    matrix = {}
    for b0 in BUCKETS:
        row_total = sum(counts[b0].values())
        if row_total == 0:
            matrix[b0] = {b1: 0.0 for b1 in BUCKETS}
        else:
            matrix[b0] = {b1: counts[b0][b1] / row_total for b1 in BUCKETS}
    return matrix, counts


def autocorrelation(token_list):
    """Pearson autocorrelation of S2 sequence at lag 1."""
    toks = clean_tokens(token_list)
    if len(toks) < 4:
        return None
    s2_vals = [t["s2"] for t in toks]
    n = len(s2_vals)
    mean = sum(s2_vals) / n
    variance = sum((x - mean) ** 2 for x in s2_vals) / n
    if variance == 0:
        return None
    covar = sum((s2_vals[i] - mean) * (s2_vals[i + 1] - mean) for i in range(n - 1)) / (n - 1)
    return covar / variance


def main():
    data = json.load(open(os.path.join(RESULTS_DIR, "corpus_results.json")))

    # Split by poetry vs prose
    all_pairs_poetry = []
    all_pairs_prose = []
    era_pairs = defaultdict(list)
    autocorrs_by_era = defaultdict(list)

    for item in data:
        meta = item["metadata"]
        era = meta.get("era", "unknown")
        tokens = item["tokens"]
        pairs = compute_transitions(tokens)
        ac = autocorrelation(tokens)

        if era == "control":
            all_pairs_prose.extend(pairs)
        else:
            all_pairs_poetry.extend(pairs)
            era_pairs[era].extend(pairs)
            if ac is not None:
                autocorrs_by_era[era].append(ac)

    matrix_poetry, counts_poetry = build_transition_matrix(all_pairs_poetry)
    matrix_prose, counts_prose = build_transition_matrix(all_pairs_prose)

    # Global autocorrelation
    all_autocorrs_poetry = []
    all_autocorrs_prose = []
    for item in data:
        era = item["metadata"].get("era", "unknown")
        ac = autocorrelation(item["tokens"])
        if ac is None:
            continue
        if era == "control":
            all_autocorrs_prose.append(ac)
        else:
            all_autocorrs_poetry.append(ac)

    # Era-level autocorrelation
    era_ac_means = {}
    for era, acs in autocorrs_by_era.items():
        if acs:
            era_ac_means[era] = (statistics.mean(acs), len(acs))

    return {
        "matrix_poetry": matrix_poetry,
        "matrix_prose": matrix_prose,
        "counts_poetry": dict(counts_poetry),
        "counts_prose": dict(counts_prose),
        "n_pairs_poetry": len(all_pairs_poetry),
        "n_pairs_prose": len(all_pairs_prose),
        "autocorr_poetry_mean": statistics.mean(all_autocorrs_poetry) if all_autocorrs_poetry else None,
        "autocorr_prose_mean": statistics.mean(all_autocorrs_prose) if all_autocorrs_prose else None,
        "era_autocorrs": era_ac_means,
    }


if __name__ == "__main__":
    results = main()

    print("=== S2 MARKOV TRANSITION ANALYSIS ===\n")

    print(f"Poetry pairs: {results['n_pairs_poetry']:,}")
    print(f"Prose pairs:  {results['n_pairs_prose']:,}")
    print()

    print(f"Global S2 autocorrelation (poetry): {results['autocorr_poetry_mean']:.4f}")
    print(f"Global S2 autocorrelation (prose):  {results['autocorr_prose_mean']:.4f}")
    print()

    print("=== POETRY TRANSITION MATRIX (row = state at t, col = state at t+1) ===")
    col_sep = "From/To"
    header = f"{col_sep:<18}" + "".join(f"{b:<14}" for b in BUCKETS)
    print(header)
    mp = results["matrix_poetry"]
    for b0 in BUCKETS:
        row = f"{b0:<18}" + "".join(f"{mp[b0].get(b1, 0):.3f}         " for b1 in BUCKETS)
        print(row)
    print()

    print("=== PROSE TRANSITION MATRIX ===")
    mpr = results["matrix_prose"]
    for b0 in BUCKETS:
        row = f"{b0:<18}" + "".join(f"{mpr[b0].get(b1, 0):.3f}         " for b1 in BUCKETS)
        print(row)
    print()

    print("=== SELF-TRANSITION PROBABILITIES (persistence) ===")
    print(f"{'Bucket':<18} {'Poetry P(same)':<18} {'Prose P(same)':<18} {'Diff'}")
    for b in BUCKETS:
        pp = mp[b].get(b, 0)
        pr = mpr[b].get(b, 0)
        print(f"{b:<18} {pp:.3f}              {pr:.3f}              {pp - pr:+.3f}")
    print()

    print("=== HIGH_SURPRISE ROW (what follows a surprise?) ===")
    print("Poetry:")
    for b1 in BUCKETS:
        print(f"  HIGH_SURPRISE → {b1}: {mp['HIGH_SURPRISE'].get(b1, 0):.3f}")
    print("Prose:")
    for b1 in BUCKETS:
        print(f"  HIGH_SURPRISE → {b1}: {mpr['HIGH_SURPRISE'].get(b1, 0):.3f}")
    print()

    print("=== ERA AUTOCORRELATIONS (sorted) ===")
    sorted_eras = sorted(results["era_autocorrs"].items(), key=lambda x: x[1][0])
    for era, (mean_ac, n) in sorted_eras:
        bar = "+" * int(abs(mean_ac) * 20) if mean_ac > 0 else "-" * int(abs(mean_ac) * 20)
        sign = "+" if mean_ac >= 0 else ""
        print(f"  {era:<25} {sign}{mean_ac:.4f}  (n={n}) {bar}")
