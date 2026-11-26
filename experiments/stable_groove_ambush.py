"""
Stable Groove → Ambush: Does a stable prediction window BEFORE a high-S2 spike
increase the spike's height or frequency?

The alternative_space_volatility.md finding established that:
- Extreme S2 events (both high and low) tend to follow MORE stable prediction spaces
- The poem-level correlation between stability and S2 is positive (r=0.214)
- The U-shaped relationship means volatility creates middling conformity

This experiment directly tests the mechanistic claim:
"High-impact S2 events (the Straussian gap) are more possible when the model has
converged on strong expectations."

For each high-S2 "ambush" token, we look backward N steps and ask:
- Was the prediction space more stable in the N positions before the ambush?
- Does the LENGTH of a stable run before the spike predict spike height?
- Are some eras/poets better at "setting up" their ambushes with stable grooves?

Also: Does a conformist run (low S2) before a spike predict spike height?
("Tension-release" model of poetic information)
"""

import json
import statistics
from collections import defaultdict

CORPUS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/stable_groove_ambush.json"
ARTIFACT_THRESHOLD = 0.90
MIN_TOKENS = 20
WINDOW_SIZES = [1, 2, 3, 4, 5, 8, 10]

# S2 thresholds
AMBUSH_THRESHOLD = 3.0      # "high S2" token = ambush
CONTROL_LOW = -1.0          # control band: neutral
CONTROL_HIGH = 1.0
CONFORMIST_THRESHOLD = -1.0  # low S2 = conformist


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 1.0
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    return intersection / union if union else 0.0


def pearson_r(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx, my = statistics.mean(xs), statistics.mean(ys)
    sx = statistics.stdev(xs)
    sy = statistics.stdev(ys)
    if sx == 0 or sy == 0:
        return 0.0
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / (n * sx * sy)


def run():
    with open(CORPUS_FILE) as f:
        corpus = json.load(f)

    # Collect per-poem token sequences with pre-computed Jaccard
    poem_sequences = []  # list of (tokens, jaccard_values, era, author, title)

    for poem in corpus:
        era = poem["metadata"]["era"]
        author = poem["metadata"]["author"]
        title = poem["metadata"]["title"]

        tokens = [
            t for t in poem["tokens"]
            if t["p_newline"] < ARTIFACT_THRESHOLD
            and t["token"].strip() not in ("", "\n", "\r")
        ]
        if len(tokens) < MIN_TOKENS:
            continue

        alt_sets = [
            frozenset(a["token"].strip().lower() for a in t["alternatives"])
            for t in tokens
        ]

        # Jaccard between consecutive positions: jacc[i] = J(alt[i-1], alt[i])
        # so jacc[i] is "how stable was the prediction space when we arrived at token i"
        jacc = [None]  # no predecessor for position 0
        for i in range(1, len(tokens)):
            jacc.append(jaccard(alt_sets[i - 1], alt_sets[i]))

        poem_sequences.append((tokens, jacc, era, author, title))

    print(f"Loaded {len(poem_sequences)} poems")

    # -----------------------------------------------------------
    # 1. For each token with enough predecessors, record:
    #    - its S2
    #    - the mean Jaccard in the W preceding positions (for each W in WINDOW_SIZES)
    #    - the consecutive conformist run length before it
    #    - era, author
    # -----------------------------------------------------------
    token_data = []

    for tokens, jacc, era, author, title in poem_sequences:
        n = len(tokens)
        for i in range(max(WINDOW_SIZES), n):
            tok = tokens[i]
            s2 = tok["s2"]

            # Jaccard windows: look at positions (i-W) to (i-1)
            pre_jacc_by_window = {}
            for W in WINDOW_SIZES:
                window_jacc = [jacc[j] for j in range(i - W + 1, i + 1) if jacc[j] is not None]
                pre_jacc_by_window[W] = statistics.mean(window_jacc) if window_jacc else None

            # Consecutive conformist run before position i
            # (how many tokens back are all conformist, i.e. S2 < CONFORMIST_THRESHOLD)
            run_len = 0
            for k in range(i - 1, -1, -1):
                if tokens[k]["s2"] < CONFORMIST_THRESHOLD:
                    run_len += 1
                else:
                    break

            # Consecutive stable groove run (Jaccard > 0.1 means "stable")
            stable_run = 0
            for k in range(i, 0, -1):
                if jacc[k] is not None and jacc[k] > 0.1:
                    stable_run += 1
                else:
                    break

            token_data.append({
                "s2": s2,
                "era": era,
                "author": author,
                "pre_jacc": pre_jacc_by_window,
                "conformist_run": run_len,
                "stable_run": stable_run,
                "token": tok["token"],
            })

    print(f"Collected {len(token_data)} token records with full windows")

    # -----------------------------------------------------------
    # 2. Split into ambush / control / conformist groups
    # -----------------------------------------------------------
    ambush = [r for r in token_data if r["s2"] >= AMBUSH_THRESHOLD]
    control = [r for r in token_data if CONTROL_LOW <= r["s2"] <= CONTROL_HIGH]
    conformist = [r for r in token_data if r["s2"] <= CONFORMIST_THRESHOLD]

    print(f"Ambush (S2≥{AMBUSH_THRESHOLD}): {len(ambush)}")
    print(f"Control ({CONTROL_LOW}≤S2≤{CONTROL_HIGH}): {len(control)}")
    print(f"Conformist (S2≤{CONFORMIST_THRESHOLD}): {len(conformist)}")

    # -----------------------------------------------------------
    # 3. Compare pre-spike Jaccard: ambush vs control vs conformist
    # -----------------------------------------------------------
    group_comparison = {}
    for W in WINDOW_SIZES:
        a_jacc = [r["pre_jacc"][W] for r in ambush if r["pre_jacc"][W] is not None]
        c_jacc = [r["pre_jacc"][W] for r in control if r["pre_jacc"][W] is not None]
        k_jacc = [r["pre_jacc"][W] for r in conformist if r["pre_jacc"][W] is not None]

        group_comparison[W] = {
            "window": W,
            "ambush_mean_jacc": round(statistics.mean(a_jacc), 5) if a_jacc else None,
            "control_mean_jacc": round(statistics.mean(c_jacc), 5) if c_jacc else None,
            "conformist_mean_jacc": round(statistics.mean(k_jacc), 5) if k_jacc else None,
            "n_ambush": len(a_jacc),
            "n_control": len(c_jacc),
            "n_conformist": len(k_jacc),
        }

    # -----------------------------------------------------------
    # 4. Within ambush group: correlation of pre-spike Jaccard with S2 height
    # -----------------------------------------------------------
    jacc_vs_s2_r = {}
    for W in WINDOW_SIZES:
        pairs = [(r["pre_jacc"][W], r["s2"]) for r in ambush if r["pre_jacc"][W] is not None]
        if len(pairs) > 10:
            xs = [p[0] for p in pairs]
            ys = [p[1] for p in pairs]
            jacc_vs_s2_r[W] = round(pearson_r(xs, ys), 4)

    # -----------------------------------------------------------
    # 5. Conformist run length vs S2 at ambush
    # -----------------------------------------------------------
    # Group ambush tokens by pre-run length
    run_bins = [(0, 0), (1, 1), (2, 3), (4, 7), (8, 100)]
    run_bin_stats = []
    for lo, hi in run_bins:
        group = [r for r in ambush if lo <= r["conformist_run"] <= hi]
        if not group:
            continue
        s2_vals = [r["s2"] for r in group]
        jacc_vals_w3 = [r["pre_jacc"][3] for r in group if r["pre_jacc"][3] is not None]
        run_bin_stats.append({
            "run_length": f"{lo}–{hi}",
            "n": len(group),
            "mean_s2": round(statistics.mean(s2_vals), 3),
            "max_s2": round(max(s2_vals), 3),
            "mean_pre_jacc_w3": round(statistics.mean(jacc_vals_w3), 5) if jacc_vals_w3 else None,
        })

    # Also overall correlation: conformist_run vs s2
    pairs = [(r["conformist_run"], r["s2"]) for r in ambush]
    xs = [p[0] for p in pairs]
    ys = [p[1] for p in pairs]
    conformist_run_vs_s2_r = round(pearson_r(xs, ys), 4)

    # -----------------------------------------------------------
    # 6. Era-level: which eras best set up ambushes with stable grooves?
    # -----------------------------------------------------------
    era_ambush = defaultdict(list)
    for r in ambush:
        era_ambush[r["era"]].append(r)

    era_setup_stats = {}
    for era, recs in era_ambush.items():
        if len(recs) < 10:
            continue
        jacc_w3 = [r["pre_jacc"][3] for r in recs if r["pre_jacc"][3] is not None]
        s2_vals = [r["s2"] for r in recs]
        run_vals = [r["conformist_run"] for r in recs]
        era_setup_stats[era] = {
            "n_ambush_tokens": len(recs),
            "mean_s2": round(statistics.mean(s2_vals), 3),
            "mean_pre_jacc_w3": round(statistics.mean(jacc_w3), 5) if jacc_w3 else None,
            "mean_conformist_run": round(statistics.mean(run_vals), 2),
        }

    # -----------------------------------------------------------
    # 7. Stable-run distribution before ambush vs control
    # -----------------------------------------------------------
    ambush_stable_runs = [r["stable_run"] for r in ambush]
    control_stable_runs = [r["stable_run"] for r in control]

    stable_run_comparison = {
        "ambush_mean": round(statistics.mean(ambush_stable_runs), 3) if ambush_stable_runs else None,
        "control_mean": round(statistics.mean(control_stable_runs), 3) if control_stable_runs else None,
        "ambush_pct_zero": round(sum(1 for x in ambush_stable_runs if x == 0) / len(ambush_stable_runs), 4),
        "control_pct_zero": round(sum(1 for x in control_stable_runs if x == 0) / len(control_stable_runs), 4),
        "ambush_pct_3plus": round(sum(1 for x in ambush_stable_runs if x >= 3) / len(ambush_stable_runs), 4),
        "control_pct_3plus": round(sum(1 for x in control_stable_runs if x >= 3) / len(control_stable_runs), 4),
    }

    # -----------------------------------------------------------
    # 8. Perfect ambush examples: high S2, high pre-spike Jaccard
    # -----------------------------------------------------------
    well_set_ambushes = sorted(
        [r for r in ambush if r["pre_jacc"][5] is not None],
        key=lambda r: r["pre_jacc"][5] * r["s2"],
        reverse=True,
    )[:20]

    perfect_ambushes = [
        {
            "token": r["token"],
            "s2": round(r["s2"], 2),
            "pre_jacc_w5": round(r["pre_jacc"][5], 4),
            "conformist_run": r["conformist_run"],
            "era": r["era"],
            "author": r["author"],
        }
        for r in well_set_ambushes
    ]

    # -----------------------------------------------------------
    # 9. S2 bins across all tokens: does pre-Jaccard step up with S2?
    # -----------------------------------------------------------
    s2_bands = [
        ("Conformist (<-3)", float("-inf"), -3),
        ("Low (-3 to -1)", -3, -1),
        ("Neutral (-1 to 1)", -1, 1),
        ("High (1 to 3)", 1, 3),
        ("Very High (3-5)", 3, 5),
        ("Extreme (5+)", 5, float("inf")),
    ]
    s2_band_analysis = []
    for name, lo, hi in s2_bands:
        group = [r for r in token_data if lo < r["s2"] <= hi]
        if not group:
            continue
        jacc_w3 = [r["pre_jacc"][3] for r in group if r["pre_jacc"][3] is not None]
        jacc_w5 = [r["pre_jacc"][5] for r in group if r["pre_jacc"][5] is not None]
        s2_band_analysis.append({
            "band": name,
            "n": len(group),
            "mean_pre_jacc_w3": round(statistics.mean(jacc_w3), 5) if jacc_w3 else None,
            "mean_pre_jacc_w5": round(statistics.mean(jacc_w5), 5) if jacc_w5 else None,
            "mean_conformist_run": round(statistics.mean(r["conformist_run"] for r in group), 3),
        })

    output = {
        "summary": {
            "n_poems": len(poem_sequences),
            "n_tokens_analyzed": len(token_data),
            "n_ambush": len(ambush),
            "n_control": len(control),
            "n_conformist": len(conformist),
            "ambush_threshold": AMBUSH_THRESHOLD,
            "window_sizes": WINDOW_SIZES,
        },
        "group_comparison_by_window": list(group_comparison.values()),
        "within_ambush_jacc_vs_s2_r": jacc_vs_s2_r,
        "conformist_run_vs_s2_r_in_ambush": conformist_run_vs_s2_r,
        "run_length_bin_stats": run_bin_stats,
        "stable_run_comparison": stable_run_comparison,
        "s2_band_analysis": s2_band_analysis,
        "era_setup_stats": era_setup_stats,
        "perfect_ambush_examples": perfect_ambushes,
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to {OUTPUT_FILE}")
    return output


if __name__ == "__main__":
    result = run()

    print("\n=== PRE-SPIKE JACCARD BY GROUP (window=3) ===")
    for w_data in result["group_comparison_by_window"]:
        if w_data["window"] == 3:
            print(f"  Ambush (S2≥3):      pre-Jaccard = {w_data['ambush_mean_jacc']:.5f}")
            print(f"  Control (-1 to 1):  pre-Jaccard = {w_data['control_mean_jacc']:.5f}")
            print(f"  Conformist (S2≤-1): pre-Jaccard = {w_data['conformist_mean_jacc']:.5f}")

    print("\n=== WITHIN-AMBUSH: pre-Jaccard vs S2 height ===")
    for W, r in sorted(result["within_ambush_jacc_vs_s2_r"].items()):
        print(f"  Window {W}: r = {r}")

    print(f"\n=== CONFORMIST RUN vs S2 (in ambush group): r = {result['conformist_run_vs_s2_r_in_ambush']} ===")

    print("\n=== PRE-CONFORMIST RUN LENGTH → AMBUSH S2 ===")
    for b in result["run_length_bin_stats"]:
        print(f"  Run {b['run_length']:5s}: mean S2={b['mean_s2']:.3f}, max S2={b['max_s2']:.3f} (n={b['n']})")

    print("\n=== STABLE RUN BEFORE TOKEN ===")
    sr = result["stable_run_comparison"]
    print(f"  Ambush: mean stable-run={sr['ambush_mean']}, pct_3+={sr['ambush_pct_3plus']:.1%}")
    print(f"  Control: mean stable-run={sr['control_mean']}, pct_3+={sr['control_pct_3plus']:.1%}")

    print("\n=== TOP 5 PERFECT AMBUSHES ===")
    for ex in result["perfect_ambush_examples"][:5]:
        print(f"  '{ex['token']}': S2={ex['s2']}, pre_jacc_w5={ex['pre_jacc_w5']}, "
              f"run={ex['conformist_run']}, {ex['author']}")
