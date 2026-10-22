"""
Spike Height Gradient Analysis: Does spike magnitude predict post-valley depth?

Follows from surprise_asymmetry.md suggestion:
  "Spike height vs. asymmetry: does the magnitude of the spike predict the
   depth of the post-valley? (higher spikes → deeper valley?)"

Hypothesis: A larger S2 spike acts as a stronger semantic anchor, constraining
GPT-2's subsequent predictions more severely, producing a deeper post-spike
conformity valley.

Secondary question: Do extreme spikes (S2 > 20) show qualitatively different
temporal behavior from moderate spikes (S2 3-5)?
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
P_NEWLINE_MAX = 0.9
WINDOW = 8

TIERS = [
    ("low",     3.0,  6.0),
    ("medium",  6.0, 12.0),
    ("high",   12.0, 20.0),
    ("extreme",20.0, float("inf")),
]


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def extract_spikes(corpus):
    spikes = []
    for poem in corpus:
        tokens = poem["tokens"]
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue
        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")

        clean_tokens = [t for t in tokens if t.get("p_newline", 0) < P_NEWLINE_MAX]
        if not clean_tokens:
            continue
        baseline = sum(t["s2"] for t in clean_tokens) / len(clean_tokens)

        for i, t in enumerate(tokens):
            if t.get("p_newline", 0) >= P_NEWLINE_MAX:
                continue
            if t["s2"] < 3.0:
                continue

            pre = []
            for lag in range(1, WINDOW + 1):
                j = i - lag
                if j < 0:
                    break
                tok = tokens[j]
                if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
                    break
                pre.append((lag, tok["s2"], tok["entropy"]))

            post = []
            for lag in range(1, WINDOW + 1):
                j = i + lag
                if j >= len(tokens):
                    break
                tok = tokens[j]
                if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
                    break
                post.append((lag, tok["s2"], tok["entropy"]))

            spikes.append({
                "era": era,
                "author": author,
                "spike_s2": t["s2"],
                "spike_entropy": t["entropy"],
                "token": t.get("token", ""),
                "baseline": baseline,
                "pre": pre,
                "post": post,
            })
    return spikes


def auc(window):
    return sum(s2 for (_, s2, _) in window)


def mean_at_lag(spikes_list, side, lag):
    vals = [s[side][lag - 1][1] for s in spikes_list
            if len(s[side]) >= lag]
    return (sum(vals) / len(vals), len(vals)) if vals else (float("nan"), 0)


def tier_label(s2):
    for label, lo, hi in TIERS:
        if lo <= s2 < hi:
            return label
    return "extreme"


def main():
    corpus = load_corpus(CORPUS_PATH)
    all_spikes = extract_spikes(corpus)
    print(f"Total spikes: {len(all_spikes)}\n")

    # Group by tier
    tiered = defaultdict(list)
    for sp in all_spikes:
        tiered[tier_label(sp["spike_s2"])].append(sp)

    results = {}

    print("=" * 70)
    print("TIER OVERVIEW")
    print("=" * 70)
    print(f"{'Tier':10} {'Range':15} {'N':>6} {'Mean spike S2':>14} {'Baseline':>9}")
    print("-" * 60)
    for label, lo, hi in TIERS:
        spikes = tiered[label]
        if not spikes:
            continue
        n = len(spikes)
        mean_spike = sum(s["spike_s2"] for s in spikes) / n
        mean_base = sum(s["baseline"] for s in spikes) / n
        hi_str = f"{hi:.0f}" if hi != float("inf") else "∞"
        print(f"{label:10} [{lo:4.0f}–{hi_str:>3}) {n:>6} {mean_spike:>14.2f} {mean_base:>9.3f}")

    print()

    # Post-valley depth by tier
    print("=" * 70)
    print("POST-VALLEY DEPTH BY TIER (mean S2 at each lag after spike)")
    print("=" * 70)

    header = f"{'Lag':>5}  " + "  ".join(f"{label:>10}" for label, _, _ in TIERS)
    print(header)
    print("-" * (7 + 12 * len(TIERS)))

    lag_data = {}
    for lag in range(1, WINDOW + 1):
        row = {}
        for label, _, _ in TIERS:
            m, n = mean_at_lag(tiered[label], "post", lag)
            row[label] = (m, n)
        lag_data[lag] = row
        cells = "  ".join(
            f"{row[label][0]:>10.3f}" if not math.isnan(row[label][0]) else f"{'N/A':>10}"
            for label, _, _ in TIERS
        )
        print(f"{lag:>5}  {cells}")

    print()
    print("POST AUC (sum lags 1-8):")
    for label, _, _ in TIERS:
        spikes = tiered[label]
        if not spikes:
            continue
        post_aucs = [auc(sp["post"]) for sp in spikes if sp["post"]]
        mean_post_auc = sum(post_aucs) / len(post_aucs) if post_aucs else float("nan")
        pre_aucs = [auc(sp["pre"]) for sp in spikes if sp["pre"]]
        mean_pre_auc = sum(pre_aucs) / len(pre_aucs) if pre_aucs else float("nan")
        ratio = mean_post_auc / mean_pre_auc if mean_pre_auc else float("nan")
        print(f"  {label:10} pre AUC={mean_pre_auc:7.3f}  post AUC={mean_post_auc:7.3f}  ratio={ratio:.3f}")
        results[label] = {
            "n": len(spikes),
            "mean_spike_s2": sum(s["spike_s2"] for s in spikes) / len(spikes),
            "mean_pre_auc": mean_pre_auc,
            "mean_post_auc": mean_post_auc,
            "auc_ratio": ratio,
        }

    print()

    # Pre-valley (setup) by tier
    print("=" * 70)
    print("PRE-SETUP DEPTH BY TIER (mean S2 at each lag before spike)")
    print("=" * 70)
    print(header)
    print("-" * (7 + 12 * len(TIERS)))
    for lag in range(1, WINDOW + 1):
        cells = []
        for label, _, _ in TIERS:
            m, n = mean_at_lag(tiered[label], "pre", lag)
            cells.append(f"{m:>10.3f}" if not math.isnan(m) else f"{'N/A':>10}")
        print(f"{lag:>5}  {'  '.join(cells)}")

    print()

    # Correlation: spike height vs post-valley depth
    print("=" * 70)
    print("CORRELATION: spike_s2 vs post_auc (token-level)")
    print("=" * 70)
    spike_s2_vals = [sp["spike_s2"] for sp in all_spikes if sp["post"]]
    post_auc_vals = [auc(sp["post"]) for sp in all_spikes if sp["post"]]
    if spike_s2_vals:
        n = len(spike_s2_vals)
        mean_x = sum(spike_s2_vals) / n
        mean_y = sum(post_auc_vals) / n
        cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(spike_s2_vals, post_auc_vals)) / n
        std_x = math.sqrt(sum((x - mean_x) ** 2 for x in spike_s2_vals) / n)
        std_y = math.sqrt(sum((y - mean_y) ** 2 for y in post_auc_vals) / n)
        if std_x > 0 and std_y > 0:
            r = cov / (std_x * std_y)
            print(f"Pearson r(spike_s2, post_auc) = {r:.4f}  (n={n})")
        else:
            r = float("nan")
            print("Cannot compute r (zero variance)")
    print()

    # Most extreme spikes
    print("=" * 70)
    print("TOP 20 MOST EXTREME SPIKES")
    print("=" * 70)
    top = sorted(all_spikes, key=lambda s: s["spike_s2"], reverse=True)[:20]
    print(f"{'Token':20} {'S2':>8} {'Post AUC':>9} {'Author':25} {'Era':20}")
    print("-" * 90)
    for sp in top:
        token_str = repr(sp["token"])[:18]
        post_a = auc(sp["post"]) if sp["post"] else float("nan")
        print(f"{token_str:20} {sp['spike_s2']:>8.2f} {post_a:>9.3f} {sp['author'][:24]:25} {sp['era'][:19]:20}")

    print()

    # Valley depth vs spike height: binned averages for 10-bin analysis
    print("=" * 70)
    print("BINNED REGRESSION: spike height deciles vs mean post-valley lag+1")
    print("=" * 70)
    valid = [(sp["spike_s2"], sp["post"][0][1]) for sp in all_spikes if sp["post"]]
    valid.sort(key=lambda x: x[0])
    if valid:
        bin_size = max(1, len(valid) // 10)
        bins = [valid[i:i + bin_size] for i in range(0, len(valid), bin_size)]
        print(f"{'Bin':>4}  {'Spike S2 range':>22}  {'Mean spike S2':>14}  {'Mean lag+1 S2':>14}  {'N':>5}")
        print("-" * 70)
        bin_results = []
        for b_idx, b in enumerate(bins):
            s2_vals = [x[0] for x in b]
            post1_vals = [x[1] for x in b]
            mean_s2 = sum(s2_vals) / len(s2_vals)
            mean_post1 = sum(post1_vals) / len(post1_vals)
            lo, hi = s2_vals[0], s2_vals[-1]
            print(f"{b_idx + 1:>4}  [{lo:6.1f} – {hi:6.1f}]  {mean_s2:>14.2f}  {mean_post1:>14.3f}  {len(b):>5}")
            bin_results.append({"bin": b_idx + 1, "mean_spike_s2": mean_s2,
                                 "mean_post1_s2": mean_post1, "n": len(b)})

    return {
        "n_spikes": len(all_spikes),
        "tier_results": results,
        "lag1_correlation_r": r if not math.isnan(r) else None,
        "bin_regression": bin_results,
    }


if __name__ == "__main__":
    result = main()
    out_path = "results/spike_height_gradient.json"
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nSaved to {out_path}")
