"""
Poet S2 Fingerprint Consistency Analysis

Tests whether individual poets (those with 4+ poems) have more consistent
information-theoretic profiles across their works than would be expected by
chance (random poem-to-poet assignment).

Research question: Is the 'Straussian gap' a property of the *poet* or just
the *era/form*? A poet with a consistent fingerprint across poems is functioning
as an idiosyncratic information-theoretic agent. A poet whose S2 varies as much
as between-poet variance shows no personal signature beyond their era.

Metrics per poem:
  avg_s2          — average Straussian gap (surprisal - entropy)
  pos_s2_ratio    — fraction of tokens with positive S2
  std_s2          — standard deviation (spikiness)
  max_s2          — highest single-token S2 (peak surprise)
  s2_range        — max_s2 - min_s2 (dynamic range)
  surprisal_gap   — avg_surprisal - avg_entropy (overall S2 summary)
"""

import json
import math
import random
from collections import defaultdict

ARTIFACT_PROB_THRESHOLD = 0.9  # newline tokens above this p_newline are excluded


def load_data():
    with open("/home/user/s2lab/results/corpus_results.json") as f:
        return json.load(f)


def get_clean_stats(entry):
    """Compute poem stats using artifact-free tokens only."""
    tokens = entry.get("tokens", [])
    clean = []
    for t in tokens:
        # Exclude high-probability newline (stanza-break artifact)
        top_preds = t.get("top_predictions", [])
        p_newline = 0.0
        for pred in top_preds:
            if pred.get("token", "") in ("\n", "Ċ", " \n", "\n\n", "ĊĊ"):
                p_newline = max(p_newline, pred.get("probability", 0.0))
        if p_newline >= ARTIFACT_PROB_THRESHOLD:
            continue
        clean.append(t)

    if len(clean) < 10:
        return None  # too few clean tokens for reliable stats

    s2_vals = [t.get("s2", 0.0) for t in clean]
    surp_vals = [t.get("surprisal", 0.0) for t in clean]
    ent_vals = [t.get("entropy", 0.0) for t in clean]

    n = len(s2_vals)
    avg_s2 = sum(s2_vals) / n
    pos_s2_ratio = sum(1 for s in s2_vals if s > 0) / n
    mean_sq = sum((s - avg_s2) ** 2 for s in s2_vals) / n
    std_s2 = math.sqrt(mean_sq)
    max_s2 = max(s2_vals)
    min_s2 = min(s2_vals)
    avg_surprisal = sum(surp_vals) / n
    avg_entropy = sum(ent_vals) / n

    return {
        "avg_s2": avg_s2,
        "pos_s2_ratio": pos_s2_ratio,
        "std_s2": std_s2,
        "max_s2": max_s2,
        "s2_range": max_s2 - min_s2,
        "surprisal_gap": avg_surprisal - avg_entropy,
        "n_clean": n,
    }


def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def variance(vals):
    if len(vals) < 2:
        return 0.0
    m = mean(vals)
    return sum((x - m) ** 2 for x in vals) / (len(vals) - 1)


def std(vals):
    return math.sqrt(variance(vals))


def coeff_variation(vals):
    m = mean(vals)
    s = std(vals)
    if abs(m) < 1e-6:
        return float("inf")
    return abs(s / m)


def between_within_ratio(groups):
    """F-ratio analog: between-group variance / within-group variance for avg_s2."""
    all_vals = [v for grp in groups.values() for v in grp]
    if len(all_vals) < 2:
        return 0.0, 0.0, 0.0

    grand_mean = mean(all_vals)
    k = len(groups)
    n_total = len(all_vals)

    ss_between = sum(
        len(g) * (mean(g) - grand_mean) ** 2 for g in groups.values() if len(g) >= 2
    )
    ss_within = sum(
        (v - mean(g)) ** 2
        for g in groups.values()
        for v in g
        if len(g) >= 2
    )

    df_between = k - 1
    df_within = n_total - k

    ms_between = ss_between / max(df_between, 1)
    ms_within = ss_within / max(df_within, 1)
    f_ratio = ms_between / ms_within if ms_within > 0 else 0.0

    return f_ratio, ms_between, ms_within


def permutation_f(poet_s2_groups, n_perm=1000):
    """Permutation test: how often does a random grouping produce F >= observed?"""
    all_vals = [v for grp in poet_s2_groups.values() for v in grp]
    group_sizes = [len(g) for g in poet_s2_groups.values()]

    obs_f, _, _ = between_within_ratio(poet_s2_groups)

    exceed_count = 0
    for _ in range(n_perm):
        shuffled = list(all_vals)
        random.shuffle(shuffled)
        perm_groups = {}
        idx = 0
        for i, size in enumerate(group_sizes):
            perm_groups[i] = shuffled[idx : idx + size]
            idx += size
        perm_f, _, _ = between_within_ratio(perm_groups)
        if perm_f >= obs_f:
            exceed_count += 1

    return obs_f, exceed_count / n_perm


def run():
    data = load_data()
    random.seed(42)

    # Gather stats per poem, grouped by poet (English only, exclude controls)
    poet_poems = defaultdict(list)
    for entry in data:
        meta = entry.get("metadata", {})
        lang = meta.get("language", "en")
        if lang != "en":
            continue
        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")
        # skip synthetic/control
        if era in ("control", "cliche_control") or "Synthetic" in author or "Control" in author:
            continue

        stats = get_clean_stats(entry)
        if stats is None:
            continue

        stats["title"] = meta.get("title", "Unknown")
        stats["era"] = era
        stats["year"] = meta.get("year", None)
        poet_poems[author].append(stats)

    # Filter to poets with >= 4 poems
    qualifying = {p: poems for p, poems in poet_poems.items() if len(poems) >= 4}

    print(f"\n=== Poet Fingerprint Consistency Analysis ===")
    print(f"Qualifying poets (4+ poems): {len(qualifying)}")
    print(f"Total poems from qualifying poets: {sum(len(v) for v in qualifying.values())}")
    print()

    # Per-poet consistency metrics
    print("=== Per-Poet Consistency (sorted by intra-poet std) ===")
    print(f"{'Poet':<35} {'n':>3} {'era':<20} {'mean_S2':>8} {'std_S2':>7} {'CV_S2':>7} {'mean_pos%':>9}")

    poet_data = []
    for poet, poems in sorted(qualifying.items(), key=lambda x: std([p["avg_s2"] for p in x[1]])):
        s2_vals = [p["avg_s2"] for p in poems]
        eras = [p["era"] for p in poems]
        primary_era = max(set(eras), key=eras.count)
        n = len(s2_vals)
        m = mean(s2_vals)
        s = std(s2_vals)
        cv = coeff_variation(s2_vals)
        pos_ratio = mean([p["pos_s2_ratio"] for p in poems])
        poet_data.append({
            "poet": poet,
            "n": n,
            "era": primary_era,
            "mean_s2": m,
            "std_s2": s,
            "cv": cv,
            "pos_ratio": pos_ratio,
            "poems": poems,
        })
        print(f"{poet:<35} {n:>3} {primary_era:<20} {m:>8.3f} {s:>7.3f} {cv:>7.3f} {pos_ratio:>8.1%}")

    # F-ratio test: are poets more consistent than chance?
    print()
    print("=== Between-Poet vs Within-Poet F-ratio (avg_s2) ===")
    poet_s2_groups = {p: [x["avg_s2"] for x in poems] for p, poems in qualifying.items()}
    obs_f, p_value = permutation_f(poet_s2_groups, n_perm=2000)
    print(f"Observed F-ratio: {obs_f:.3f}")
    print(f"Permutation p-value (2000 shuffles): {p_value:.4f}")
    if p_value < 0.05:
        print("→ Individual poets show significantly consistent S2 profiles (p < 0.05)")
    else:
        print("→ No significant poet-level consistency beyond era/form")

    # Most vs least consistent poets
    print()
    print("=== Most Consistent (lowest std_S2) ===")
    for pd in poet_data[:5]:
        print(f"  {pd['poet']:<35} std={pd['std_s2']:.3f}  mean={pd['mean_s2']:.3f}")
        for poem in pd["poems"]:
            print(f"    '{poem['title'][:50]}'  S2={poem['avg_s2']:.3f}")

    print()
    print("=== Most Variable (highest std_S2) ===")
    for pd in sorted(poet_data, key=lambda x: -x["std_s2"])[:5]:
        print(f"  {pd['poet']:<35} std={pd['std_s2']:.3f}  mean={pd['mean_s2']:.3f}")
        for poem in pd["poems"]:
            print(f"    '{poem['title'][:50]}'  S2={poem['avg_s2']:.3f}")

    # Per-metric consistency: which feature is most consistent within poets?
    print()
    print("=== Which S2 Metric is Most Consistent Within Poets? ===")
    metrics = ["avg_s2", "pos_s2_ratio", "std_s2", "max_s2", "s2_range"]
    for metric in metrics:
        # Compute mean intra-poet CV for this metric
        cvs = []
        for pd in poet_data:
            vals = [p[metric] for p in pd["poems"]]
            cv = coeff_variation(vals)
            if not math.isinf(cv) and not math.isnan(cv):
                cvs.append(cv)
        if cvs:
            print(f"  {metric:<20}: mean intra-poet CV = {mean(cvs):.3f}  (lower = more consistent)")

    # The 'idiosyncrasy score': intra-poet std vs inter-era std
    print()
    print("=== Idiosyncrasy: Poet std vs Era std ===")
    era_s2 = defaultdict(list)
    for pd in poet_data:
        era_s2[pd["era"]].extend([p["avg_s2"] for p in pd["poems"]])

    for pd in poet_data:
        intra_std = pd["std_s2"]
        era_vals = era_s2[pd["era"]]
        era_s = std(era_vals) if len(era_vals) >= 2 else 1.0
        # If poet's std << era std, the poet is more consistent than their era baseline
        ratio = intra_std / era_s if era_s > 0 else float("inf")
        pd["idiosyncrasy_ratio"] = ratio

    print(f"{'Poet':<35} {'n':>3} {'era':<20} {'poet_std':>9} {'era_std':>8} {'ratio':>7}")
    for pd in sorted(poet_data, key=lambda x: x["idiosyncrasy_ratio"]):
        era_vals = era_s2[pd["era"]]
        era_s = std(era_vals) if len(era_vals) >= 2 else float("nan")
        print(
            f"{pd['poet']:<35} {pd['n']:>3} {pd['era']:<20}"
            f" {pd['std_s2']:>9.3f} {era_s:>8.3f} {pd['idiosyncrasy_ratio']:>7.3f}"
        )

    return poet_data, obs_f, p_value


if __name__ == "__main__":
    run()
