"""
Surprise Asymmetry: Pre-peak wind-up vs. post-peak collapse.

Prior work:
  - pre_peak_setup.md: S2 drops 0.6 units over lags -3 to -1 (wind-up)
  - surprise_decay_curves.md: S2 collapses to near-zero at lag +1 (decay)

This experiment overlays both curves to quantify the *asymmetry*:
  - How slowly does the poet descend into a spike? (setup duration)
  - How quickly does it recover? (decay speed)
  - Is the temporal structure symmetric or skewed?

For each spike (S2 ≥ 3.0, artifact-free), we aggregate:
  - Pre-peak: lags -8 to -1
  - Post-peak: lags +1 to +8
Then compute asymmetry metrics per era and per poet.
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
SPIKE_THRESHOLD = 3.0
P_NEWLINE_MAX = 0.9  # artifact filter
WINDOW = 8  # lags to look pre/post


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def compute_poem_baseline(tokens, p_newline_max=P_NEWLINE_MAX):
    clean = [t for t in tokens if t.get("p_newline", 0) < p_newline_max]
    if not clean:
        return 0.0
    return sum(t["s2"] for t in clean) / len(clean)


def extract_spikes(poem):
    """Return list of spike dicts with pre/post windows."""
    tokens = poem["tokens"]
    era = poem["metadata"].get("era", "unknown")
    author = poem["metadata"].get("author", "unknown")
    baseline = compute_poem_baseline(tokens)
    lang = poem["metadata"].get("language", "en")
    if lang != "en":
        return []

    spikes = []
    for i, t in enumerate(tokens):
        if t.get("p_newline", 0) >= P_NEWLINE_MAX:
            continue
        if t["s2"] < SPIKE_THRESHOLD:
            continue

        pre_window = []
        for lag in range(1, WINDOW + 1):
            j = i - lag
            if j < 0:
                break
            tok = tokens[j]
            if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
                # stop at artifact boundary
                break
            pre_window.append((-lag, tok["s2"], tok["entropy"]))

        post_window = []
        for lag in range(1, WINDOW + 1):
            j = i + lag
            if j >= len(tokens):
                break
            tok = tokens[j]
            if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
                break
            post_window.append((lag, tok["s2"], tok["entropy"]))

        spikes.append({
            "era": era,
            "author": author,
            "spike_s2": t["s2"],
            "spike_entropy": t["entropy"],
            "baseline": baseline,
            "pre": pre_window,   # list of (-lag, s2, entropy)
            "post": post_window,  # list of (+lag, s2, entropy)
        })

    return spikes


def aggregate_curve(spikes, side, max_lag=WINDOW):
    """Aggregate mean s2 per lag position for pre or post."""
    lag_s2 = defaultdict(list)
    lag_entropy = defaultdict(list)
    for sp in spikes:
        for (lag, s2, entropy) in sp[side]:
            abs_lag = abs(lag)
            if abs_lag <= max_lag:
                lag_s2[abs_lag].append(s2)
                lag_entropy[abs_lag].append(entropy)
    result = {}
    for lag in range(1, max_lag + 1):
        vals = lag_s2.get(lag, [])
        ent_vals = lag_entropy.get(lag, [])
        if vals:
            result[lag] = {
                "mean_s2": sum(vals) / len(vals),
                "mean_entropy": sum(ent_vals) / len(ent_vals) if ent_vals else 0,
                "n": len(vals),
            }
    return result


def compute_setup_depth(pre_curve, baseline, lags=(1, 2, 3)):
    """How much lower is mean s2 in the final `lags` positions before spike vs baseline?"""
    vals = [pre_curve[lag]["mean_s2"] for lag in lags if lag in pre_curve]
    if not vals:
        return 0.0
    return (sum(vals) / len(vals)) - baseline


def compute_decay_depth(post_curve, baseline, lags=(1, 2, 3)):
    """How much lower is mean s2 in the first `lags` positions after spike vs baseline?"""
    vals = [post_curve[lag]["mean_s2"] for lag in lags if lag in post_curve]
    if not vals:
        return 0.0
    return (sum(vals) / len(vals)) - baseline


def area_under_curve(curve, max_lag=8):
    """Sum of mean_s2 deviations from 0 over the window (rough AUC proxy)."""
    total = 0.0
    for lag in range(1, max_lag + 1):
        if lag in curve:
            total += curve[lag]["mean_s2"]
    return total


def main():
    data = load_corpus(CORPUS_PATH)

    # Collect all spikes
    all_spikes = []
    for poem in data:
        all_spikes.extend(extract_spikes(poem))

    print(f"Total spikes found: {len(all_spikes)}")
    print(f"Poems in corpus: {len(data)}")
    print()

    # --- GLOBAL CURVES ---
    pre_curve = aggregate_curve(all_spikes, "pre")
    post_curve = aggregate_curve(all_spikes, "post")
    avg_baseline = sum(s["baseline"] for s in all_spikes) / len(all_spikes) if all_spikes else 0.0

    print("=== GLOBAL PRE/POST CURVES ===")
    print(f"Average poem baseline S2: {avg_baseline:.3f}")
    print(f"{'Lag':>5}  {'Pre S2':>9}  {'Post S2':>9}  {'Δ(post-pre)':>12}")
    for lag in range(1, WINDOW + 1):
        pre_s2 = pre_curve.get(lag, {}).get("mean_s2", float("nan"))
        post_s2 = post_curve.get(lag, {}).get("mean_s2", float("nan"))
        if not math.isnan(pre_s2) and not math.isnan(post_s2):
            delta = post_s2 - pre_s2
            print(f"{lag:>5}  {pre_s2:>9.3f}  {post_s2:>9.3f}  {delta:>12.3f}")

    print()
    pre_auc = area_under_curve(pre_curve)
    post_auc = area_under_curve(post_curve)
    print(f"Pre-peak AUC (sum lags 1-8):  {pre_auc:.3f}")
    print(f"Post-peak AUC (sum lags 1-8): {post_auc:.3f}")
    if pre_auc != 0:
        ratio = post_auc / pre_auc
        print(f"AUC asymmetry ratio (post/pre): {ratio:.3f}")
        if ratio < 0.5:
            print("→ Strong asymmetry: collapse much faster than wind-up")
        elif ratio < 0.8:
            print("→ Moderate asymmetry: collapse somewhat faster than wind-up")
        elif ratio < 1.2:
            print("→ Near-symmetric setup and decay")
        else:
            print("→ Inverse asymmetry: recovery slower than setup")

    print()

    # --- BY ERA ---
    era_spikes = defaultdict(list)
    for sp in all_spikes:
        era_spikes[sp["era"]].append(sp)

    print("=== ASYMMETRY BY ERA ===")
    print(f"{'Era':25}  {'N_spikes':>9}  {'Pre_AUC':>8}  {'Post_AUC':>9}  {'Ratio':>6}  {'Setup_depth(1-3)':>17}  {'Decay_depth(1-3)':>17}")
    print("-" * 110)

    era_results = []
    for era, spikes in era_spikes.items():
        if len(spikes) < 10:
            continue
        pre = aggregate_curve(spikes, "pre")
        post = aggregate_curve(spikes, "post")
        avg_bl = sum(s["baseline"] for s in spikes) / len(spikes)

        p_auc = area_under_curve(pre)
        po_auc = area_under_curve(post)
        ratio = po_auc / p_auc if p_auc != 0 else float("nan")

        setup = compute_setup_depth(pre, avg_bl, lags=(1, 2, 3))
        decay = compute_decay_depth(post, avg_bl, lags=(1, 2, 3))

        era_results.append((era, len(spikes), p_auc, po_auc, ratio, setup, decay))

    era_results.sort(key=lambda x: x[4] if not math.isnan(x[4]) else 999)

    for (era, n, p_auc, po_auc, ratio, setup, decay) in era_results:
        ratio_str = f"{ratio:.2f}" if not math.isnan(ratio) else " NaN"
        print(f"{era:25}  {n:>9}  {p_auc:>8.2f}  {po_auc:>9.2f}  {ratio_str:>6}  {setup:>17.3f}  {decay:>17.3f}")

    print()

    # --- BY POET (min 20 spikes) ---
    author_spikes = defaultdict(list)
    for sp in all_spikes:
        author_spikes[sp["author"]].append(sp)

    print("=== ASYMMETRY BY POET (≥20 spikes) ===")
    print(f"{'Poet':35}  {'N':>5}  {'Pre_AUC':>8}  {'Post_AUC':>9}  {'Ratio':>6}  {'Setup_lull':>11}  {'Decay_drop':>11}")
    print("-" * 100)

    poet_results = []
    for author, spikes in author_spikes.items():
        if len(spikes) < 20:
            continue
        pre = aggregate_curve(spikes, "pre")
        post = aggregate_curve(spikes, "post")
        avg_bl = sum(s["baseline"] for s in spikes) / len(spikes)

        p_auc = area_under_curve(pre)
        po_auc = area_under_curve(post)
        ratio = po_auc / p_auc if p_auc != 0 else float("nan")
        setup = compute_setup_depth(pre, avg_bl, lags=(1, 2, 3))
        decay = compute_decay_depth(post, avg_bl, lags=(1, 2, 3))

        poet_results.append((author, len(spikes), p_auc, po_auc, ratio, setup, decay))

    poet_results.sort(key=lambda x: x[4] if not math.isnan(x[4]) else 999)

    for (author, n, p_auc, po_auc, ratio, setup, decay) in poet_results:
        ratio_str = f"{ratio:.2f}" if not math.isnan(ratio) else " NaN"
        print(f"{author:35}  {n:>5}  {p_auc:>8.2f}  {po_auc:>9.2f}  {ratio_str:>6}  {setup:>11.3f}  {decay:>11.3f}")

    print()

    # --- DETAILED GLOBAL CURVES with entropy ---
    print("=== FULL CURVES (S2 and entropy) ===")
    print(f"{'Lag':>5}  {'Dir':>5}  {'Mean_S2':>9}  {'Mean_H':>9}  {'N':>6}")
    for lag in range(WINDOW, 0, -1):
        if lag in pre_curve:
            d = pre_curve[lag]
            print(f"{-lag:>5}  {'pre':>5}  {d['mean_s2']:>9.3f}  {d['mean_entropy']:>9.3f}  {d['n']:>6}")
    print(f"{'  0':>5}  {'PEAK':>5}  {'[spike]':>9}  {'':>9}")
    for lag in range(1, WINDOW + 1):
        if lag in post_curve:
            d = post_curve[lag]
            print(f"{lag:>5}  {'post':>5}  {d['mean_s2']:>9.3f}  {d['mean_entropy']:>9.3f}  {d['n']:>6}")

    # Return summary dict for JSON output
    result = {
        "n_spikes": len(all_spikes),
        "avg_baseline": avg_baseline,
        "pre_auc": pre_auc,
        "post_auc": post_auc,
        "auc_ratio": post_auc / pre_auc if pre_auc != 0 else None,
        "pre_curve": {str(k): v for k, v in pre_curve.items()},
        "post_curve": {str(k): v for k, v in post_curve.items()},
        "era_results": [
            {
                "era": era, "n_spikes": n,
                "pre_auc": p_auc, "post_auc": po_auc,
                "ratio": ratio if not math.isnan(ratio) else None,
                "setup_depth": setup, "decay_depth": decay
            }
            for (era, n, p_auc, po_auc, ratio, setup, decay) in era_results
        ],
    }
    return result


if __name__ == "__main__":
    import json
    result = main()
    out_path = "results/surprise_asymmetry.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to {out_path}")
