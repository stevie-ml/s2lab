"""
S₂ Higher-Order Statistics: Variance, Skewness, and Kurtosis as Genre Fingerprints

The project has studied mean S₂ extensively — this experiment goes deeper.
Within each poem, the SHAPE of the S₂ distribution (not just its center) encodes
genre logic:

  - Comedy (limerick, clerihew, parody): high variance + rightward terminal spike
    (flat setup, then the punchline)
  - Elegy: moderate variance, sustained plateau
  - Surrealism: high variance + leptokurtic (fat-tailed) — random spikes everywhere
  - Haiku: low variance (every token matters; no padding)
  - Oulipo: constraint reduces variance despite poetic intent
  - Fixed-form (sonnet etc): lower variance than free verse same era?

Statistics computed per poem (artifact-free tokens only):
  - std     : within-poem standard deviation of S₂
  - skew    : Fisher-Pearson skewness (right-skewed = positive = occasional spikes)
  - kurt    : excess kurtosis (leptokurtic = fat tail = surprise spikes)
  - q90     : 90th percentile S₂ (captures spike height)
  - term20  : mean S₂ in final 20% of tokens minus overall mean (terminal spike)
  - range   : max S₂ − min S₂
"""

import json
import math
import statistics
import os

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")

ARTIFACT_P_NEWLINE_THRESHOLD = 0.9

COMIC_ERAS = {"limerick", "clerihew", "parody", "parody_original", "nursery_rhyme"}
ELEGIAC_ERAS = {"elegy", "war_poetry"}
SURREAL_ERAS = {"surrealist"}
HAIKU_ERAS = {"haiku", "japanese_classical"}
CONSTRAINED_ERAS = {"oulipo", "fixed_form", "concrete"}
FREE_ERAS = {"beat", "confessional", "contemporary", "new_york_school", "language", "modernist"}


def skewness(vals):
    """Fisher-Pearson skewness (moment-based)."""
    n = len(vals)
    if n < 3:
        return None
    mu = statistics.mean(vals)
    s = statistics.stdev(vals)
    if s == 0:
        return 0.0
    return sum(((v - mu) / s) ** 3 for v in vals) / n


def kurtosis(vals):
    """Excess kurtosis (0 = normal; >0 = leptokurtic = fat tails = spiky)."""
    n = len(vals)
    if n < 4:
        return None
    mu = statistics.mean(vals)
    s = statistics.stdev(vals)
    if s == 0:
        return 0.0
    return sum(((v - mu) / s) ** 4 for v in vals) / n - 3.0


def percentile(vals, p):
    """Simple percentile via linear interpolation."""
    if not vals:
        return None
    sv = sorted(vals)
    n = len(sv)
    idx = (p / 100) * (n - 1)
    lo = int(idx)
    hi = min(lo + 1, n - 1)
    frac = idx - lo
    return sv[lo] + frac * (sv[hi] - sv[lo])


def poem_stats(poem, min_tokens=10):
    """Return shape stats for a single poem (artifact-free tokens)."""
    tokens = poem.get("tokens", [])
    s2_vals = []
    for tok in tokens:
        pnl = tok.get("p_newline", 0)
        if pnl >= ARTIFACT_P_NEWLINE_THRESHOLD:
            continue
        s2 = tok.get("s2")
        if s2 is None:
            continue
        s2_vals.append(s2)

    if len(s2_vals) < min_tokens:
        return None

    n = len(s2_vals)
    mu = statistics.mean(s2_vals)
    std = statistics.stdev(s2_vals) if n >= 2 else 0.0

    # Terminal spike: last 20% vs overall mean
    cutoff = max(1, int(n * 0.8))
    terminal = s2_vals[cutoff:]
    term20 = statistics.mean(terminal) - mu if terminal else 0.0

    # Opening: first 20%
    open_vals = s2_vals[: max(1, int(n * 0.2))]
    open20 = statistics.mean(open_vals) - mu if open_vals else 0.0

    sk = skewness(s2_vals)
    kurt = kurtosis(s2_vals)
    q90 = percentile(s2_vals, 90)
    q10 = percentile(s2_vals, 10)
    rng = max(s2_vals) - min(s2_vals)

    return {
        "n_tokens": n,
        "mean": mu,
        "std": std,
        "skew": sk,
        "kurt": kurt,
        "q90": q90,
        "q10": q10,
        "range": rng,
        "term20": term20,
        "open20": open20,
        "title": poem["metadata"].get("title", "?"),
        "author": poem["metadata"].get("author", "?"),
        "era": poem["metadata"].get("era", "?"),
        "year": poem["metadata"].get("year"),
    }


def aggregate(poem_stats_list):
    """Aggregate shape stats across a list of poem stats dicts."""
    if not poem_stats_list:
        return None
    keys = ["mean", "std", "skew", "kurt", "q90", "term20", "open20", "range"]
    out = {}
    for k in keys:
        vals = [p[k] for p in poem_stats_list if p.get(k) is not None]
        if vals:
            out[f"avg_{k}"] = statistics.mean(vals)
            out[f"med_{k}"] = statistics.median(vals)
        else:
            out[f"avg_{k}"] = None
            out[f"med_{k}"] = None
    out["n_poems"] = len(poem_stats_list)
    return out


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    era_poems = {}
    all_stats = []

    for poem in data:
        meta = poem.get("metadata", {})
        lang = meta.get("language", "en")
        era = meta.get("era", "?")
        if lang != "en":
            continue
        if era in ("control",):
            continue

        ps = poem_stats(poem, min_tokens=10)
        if ps is None:
            continue

        all_stats.append(ps)
        era_poems.setdefault(era, []).append(ps)

    print(f"\n{'='*80}")
    print("S₂ Higher-Order Statistics: Genre Shape Analysis")
    print(f"{'='*80}")
    print(f"Total poems: {len(all_stats)}")

    # Per-era aggregation
    era_agg = {}
    for era, plist in era_poems.items():
        era_agg[era] = aggregate(plist)
        era_agg[era]["era"] = era

    # Sort by avg_std descending (spikiest to smoothest)
    ranked = sorted(era_agg.values(), key=lambda x: (x["avg_std"] or -999), reverse=True)

    print(f"\n{'─'*100}")
    print(f"{'Era':<22} {'N':>4} {'Mean S2':>8} {'Avg Std':>8} {'Avg Skew':>9} {'Avg Kurt':>9} {'Avg Q90':>8} {'Term20':>8}")
    print(f"{'─'*100}")
    for e in ranked:
        era = e["era"]
        n = e["n_poems"]
        mu = e.get("avg_mean")
        std = e.get("avg_std")
        sk = e.get("avg_skew")
        kt = e.get("avg_kurt")
        q90 = e.get("avg_q90")
        t20 = e.get("avg_term20")
        def fmt(v, d=2):
            return f"{v:+.{d}f}" if v is not None else "    N/A"
        print(f"{era:<22} {n:>4} {fmt(mu):>8} {fmt(std):>8} {fmt(sk):>9} {fmt(kt):>9} {fmt(q90):>8} {fmt(t20):>8}")

    # Grouped analysis: Comic vs Elegiac
    print(f"\n{'='*80}")
    print("GROUPED ANALYSIS: Comic vs. Elegiac vs. Surreal vs. Haiku vs. Constrained")
    print(f"{'='*80}")

    groups = {
        "COMIC (limerick/clerihew/parody/nursery)": COMIC_ERAS,
        "ELEGIAC (elegy/war_poetry)": ELEGIAC_ERAS,
        "SURREALIST": SURREAL_ERAS,
        "HAIKU/JAPANESE": HAIKU_ERAS,
        "CONSTRAINED (oulipo/fixed/concrete)": CONSTRAINED_ERAS,
        "FREE VERSE (beat/confessional/etc)": FREE_ERAS,
    }

    group_results = {}
    for group_name, era_set in groups.items():
        plist = [p for p in all_stats if p["era"] in era_set]
        agg = aggregate(plist)
        if agg:
            agg["label"] = group_name
            group_results[group_name] = agg
            print(f"\n{group_name} (N={agg['n_poems']} poems)")
            print(f"  Avg mean S2:  {agg['avg_mean']:+.3f}  |  Avg std: {agg['avg_std']:.3f}")
            print(f"  Avg skew:     {agg['avg_skew']:+.3f}  |  Avg kurtosis: {agg['avg_kurt']:+.3f}")
            print(f"  Avg Q90:      {agg['avg_q90']:+.2f}   |  Avg range: {agg['avg_range']:.2f}")
            print(f"  Terminal20:   {agg['avg_term20']:+.3f}  |  Open20: {agg['avg_open20']:+.3f}")

    # Per-poem outliers: highest and lowest std
    print(f"\n{'='*80}")
    print("TOP 10 SPIKIEST POEMS (highest within-poem std)")
    print(f"{'='*80}")
    sorted_std = sorted(all_stats, key=lambda x: x["std"], reverse=True)
    for p in sorted_std[:10]:
        print(f"  {p['era']:<20} std={p['std']:.2f}  mean={p['mean']:+.2f}  skew={p['skew']:+.2f}  term20={p['term20']:+.2f} | {p['author']} — {p['title'][:40]}")

    print(f"\n{'='*80}")
    print("TOP 10 SMOOTHEST POEMS (lowest within-poem std)")
    print(f"{'='*80}")
    sorted_std_asc = sorted(all_stats, key=lambda x: x["std"])
    for p in sorted_std_asc[:10]:
        print(f"  {p['era']:<20} std={p['std']:.2f}  mean={p['mean']:+.2f}  skew={p['skew']:+.2f}  term20={p['term20']:+.2f} | {p['author']} — {p['title'][:40]}")

    # Terminal spike analysis: which genres "end on a spike"?
    print(f"\n{'='*80}")
    print("TERMINAL SPIKE RANKING (avg S2 in final 20% vs poem mean)")
    print("Positive = poem ends with MORE surprise than its average (punchline effect)")
    print(f"{'='*80}")
    term_ranked = sorted(era_agg.values(), key=lambda x: (x["avg_term20"] or -999), reverse=True)
    for e in term_ranked[:15]:
        era = e["era"]
        t20 = e["avg_term20"]
        n = e["n_poems"]
        if t20 is not None:
            print(f"  {era:<22}  N={n:>3}  term20={t20:+.3f}")

    print(f"\n{'='*80}")
    print("OPENING SPIKE RANKING (avg S2 in first 20% vs poem mean)")
    print("Positive = poem opens with MORE surprise than its average (in medias res)")
    print(f"{'='*80}")
    open_ranked = sorted(era_agg.values(), key=lambda x: (x["avg_open20"] or -999), reverse=True)
    for e in open_ranked[:15]:
        era = e["era"]
        o20 = e["avg_open20"]
        n = e["n_poems"]
        if o20 is not None:
            print(f"  {era:<22}  N={n:>3}  open20={o20:+.3f}")

    # Save structured results
    output = {
        "era_aggregates": era_agg,
        "group_comparisons": group_results,
        "top_spiky": [
            {k: v for k, v in p.items()} for p in sorted_std[:20]
        ],
        "top_smooth": [
            {k: v for k, v in p.items()} for p in sorted_std_asc[:20]
        ],
    }
    out_path = os.path.join(os.path.dirname(__file__), "..", "results", "s2_distribution_shape_genre.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return output


if __name__ == "__main__":
    main()
