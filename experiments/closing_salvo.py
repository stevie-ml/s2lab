"""
Closing Salvo: The Hot End Problem in Poetic S₂.

Counterpart to opening_salvo.py. While the opening faces a "cold start"
(GPT-2 has no prior context, entropy is ~11 bits), the ending has full
accumulated context — GPT-2 should be maximally confident.

This experiment asks:
  1. Is S₂ systematically different in the final 15 tokens vs. the rest?
  2. Does entropy DROP further as the poem approaches its end?
  3. Does a poem's closing S₂ predict its overall S₂?
  4. What is the "terminal profile"? (Does S₂ spike or resolve at the end?)
  5. Is there a "closing advantage" (closing S₂ > rest S₂) for any eras?
     Or is it always a resolution (closing S₂ < rest S₂)?
  6. How does the closing compare to the opening — symmetric or inverted?
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/closing_salvo.json"
P_NEWLINE_MAX = 0.9
CLOSING_N = 15   # last N clean tokens = "closing"
MIN_CLEAN = 30   # minimum clean tokens to include poem


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def clean_tokens(poem):
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < P_NEWLINE_MAX]


def poem_stats(toks):
    if not toks:
        return None
    s2_vals = [t["s2"] for t in toks]
    h_vals = [t["entropy"] for t in toks]
    n = len(s2_vals)
    return {
        "n": n,
        "mean_s2": sum(s2_vals) / n,
        "mean_entropy": sum(h_vals) / n,
        "spike_rate": sum(1 for v in s2_vals if v >= 3.0) / n,
        "pos_s2_ratio": sum(1 for v in s2_vals if v > 0) / n,
    }


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def main():
    corpus = load_corpus(CORPUS_PATH)

    poem_records = []
    era_closing = defaultdict(list)
    era_rest = defaultdict(list)
    era_opening = defaultdict(list)

    # Position-level aggregates (counting from END: lag 0 = last token, lag 1 = second to last, ...)
    lag_s2 = defaultdict(list)
    lag_h = defaultdict(list)

    for poem in corpus:
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue

        clean = clean_tokens(poem)
        if len(clean) < MIN_CLEAN:
            continue

        # Closing = last CLOSING_N tokens
        closing = clean[-CLOSING_N:]
        # Opening = first CLOSING_N tokens (for comparison)
        opening = clean[:CLOSING_N]
        # Middle = everything else
        middle = clean[CLOSING_N:-CLOSING_N] if len(clean) > 2 * CLOSING_N else []

        if not middle and len(clean) <= CLOSING_N:
            continue

        # "rest" for closing comparison = everything except closing
        rest = clean[:-CLOSING_N]
        if not rest:
            continue

        c_stats = poem_stats(closing)
        o_stats = poem_stats(opening)
        r_stats = poem_stats(rest)
        all_stats = poem_stats(clean)

        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")
        title = poem["metadata"].get("title", "unknown")

        # Lag positions (0 = last token, 1 = second to last, ...)
        for lag, tok in enumerate(reversed(closing)):
            lag_s2[lag].append(tok["s2"])
            lag_h[lag].append(tok["entropy"])

        rec = {
            "title": title,
            "author": author,
            "era": era,
            "overall_s2": all_stats["mean_s2"],
            "closing_s2": c_stats["mean_s2"],
            "opening_s2": o_stats["mean_s2"],
            "rest_s2": r_stats["mean_s2"],  # all but last CLOSING_N
            "closing_advantage": c_stats["mean_s2"] - r_stats["mean_s2"],
            "closing_vs_opening": c_stats["mean_s2"] - o_stats["mean_s2"],
            "closing_entropy": c_stats["mean_entropy"],
            "rest_entropy": r_stats["mean_entropy"],
            "opening_entropy": o_stats["mean_entropy"],
            "closing_spike_rate": c_stats["spike_rate"],
            "rest_spike_rate": r_stats["spike_rate"],
            "n_closing": c_stats["n"],
            "n_rest": r_stats["n"],
        }
        poem_records.append(rec)
        era_closing[era].append(c_stats["mean_s2"])
        era_rest[era].append(r_stats["mean_s2"])
        era_opening[era].append(o_stats["mean_s2"])

    n = len(poem_records)
    mean_closing = sum(r["closing_s2"] for r in poem_records) / n
    mean_rest = sum(r["rest_s2"] for r in poem_records) / n
    mean_opening = sum(r["opening_s2"] for r in poem_records) / n
    mean_closing_h = sum(r["closing_entropy"] for r in poem_records) / n
    mean_rest_h = sum(r["rest_entropy"] for r in poem_records) / n
    mean_opening_h = sum(r["opening_entropy"] for r in poem_records) / n
    mean_closing_spike = sum(r["closing_spike_rate"] for r in poem_records) / n
    mean_rest_spike = sum(r["rest_spike_rate"] for r in poem_records) / n

    # Correlations
    xs = [r["closing_s2"] for r in poem_records]
    ys = [r["overall_s2"] for r in poem_records]
    corr_closing_overall = pearson(xs, ys)

    xs_rest = [r["rest_s2"] for r in poem_records]
    corr_rest_overall = pearson(xs_rest, ys)

    xs_open = [r["opening_s2"] for r in poem_records]
    corr_opening_overall = pearson(xs_open, ys)

    # Fraction of poems where closing > rest (closure detonation)
    frac_closing_above_rest = sum(1 for r in poem_records if r["closing_s2"] > r["rest_s2"]) / n
    frac_closing_above_opening = sum(1 for r in poem_records if r["closing_s2"] > r["opening_s2"]) / n

    # Era stats
    era_stats = {}
    for era in sorted(era_closing.keys()):
        c_vals = era_closing[era]
        r_vals = era_rest[era]
        o_vals = era_opening[era]
        if len(c_vals) < 2:
            continue
        era_stats[era] = {
            "n": len(c_vals),
            "mean_closing_s2": sum(c_vals) / len(c_vals),
            "mean_rest_s2": sum(r_vals) / len(r_vals),
            "mean_opening_s2": sum(o_vals) / len(o_vals),
            "closing_advantage": sum(c_vals) / len(c_vals) - sum(r_vals) / len(r_vals),
            "opening_advantage": sum(o_vals) / len(o_vals) - sum(r_vals) / len(r_vals),
        }

    # Lag-level profile (lag 0 = last token, lag 14 = 15th from end)
    lag_profile = {}
    for lag in range(CLOSING_N + 5):
        s2v = lag_s2[lag]
        hv = lag_h[lag]
        if s2v:
            lag_profile[lag] = {
                "mean_s2": sum(s2v) / len(s2v),
                "mean_entropy": sum(hv) / len(hv),
                "n": len(s2v),
            }

    # Top/bottom poems by closing advantage
    top_closing = sorted(poem_records, key=lambda r: r["closing_advantage"], reverse=True)[:10]
    bottom_closing = sorted(poem_records, key=lambda r: r["closing_advantage"])[:10]

    output = {
        "n_poems": n,
        "closing_n_tokens": CLOSING_N,
        "corpus_level": {
            "mean_closing_s2": mean_closing,
            "mean_opening_s2": mean_opening,
            "mean_rest_s2": mean_rest,
            "closing_vs_rest_delta": mean_closing - mean_rest,
            "closing_vs_opening_delta": mean_closing - mean_opening,
            "mean_closing_entropy": mean_closing_h,
            "mean_opening_entropy": mean_opening_h,
            "mean_rest_entropy": mean_rest_h,
            "mean_closing_spike_rate": mean_closing_spike,
            "mean_rest_spike_rate": mean_rest_spike,
            "corr_closing_vs_overall_s2": corr_closing_overall,
            "corr_rest_vs_overall_s2": corr_rest_overall,
            "corr_opening_vs_overall_s2": corr_opening_overall,
            "frac_closing_above_rest": frac_closing_above_rest,
            "frac_closing_above_opening": frac_closing_above_opening,
        },
        "era_stats": era_stats,
        "lag_profile": lag_profile,
        "top_closing_advantage": top_closing,
        "bottom_closing_advantage": bottom_closing,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Poems analyzed: {n}")
    print(f"Closing S2 (last {CLOSING_N} tokens): {mean_closing:+.4f}")
    print(f"Opening S2 (first {CLOSING_N} tokens): {mean_opening:+.4f}")
    print(f"Rest S2 (everything else):            {mean_rest:+.4f}")
    print(f"Closing - Rest delta:                 {mean_closing - mean_rest:+.4f}")
    print(f"Closing - Opening delta:              {mean_closing - mean_opening:+.4f}")
    print(f"Closing entropy:                      {mean_closing_h:.4f}")
    print(f"Opening entropy:                      {mean_opening_h:.4f}")
    print(f"Rest entropy:                         {mean_rest_h:.4f}")
    print(f"Closing spike rate:                   {mean_closing_spike:.4f}")
    print(f"Rest spike rate:                      {mean_rest_spike:.4f}")
    print(f"r(closing, overall S2):               {corr_closing_overall:.4f}")
    print(f"r(rest, overall S2):                  {corr_rest_overall:.4f}")
    print(f"r(opening, overall S2):               {corr_opening_overall:.4f}")
    print(f"Frac poems: closing > rest:           {frac_closing_above_rest:.3f}")
    print(f"Frac poems: closing > opening:        {frac_closing_above_opening:.3f}")
    print()
    print("Era breakdown (sorted by closing_advantage):")
    sorted_eras = sorted(era_stats.items(), key=lambda x: -x[1]["closing_advantage"])
    for era, st in sorted_eras[:15]:
        print(f"  {era:30s}  n={st['n']:3d}  close={st['mean_closing_s2']:+.3f}  rest={st['mean_rest_s2']:+.3f}  close_adv={st['closing_advantage']:+.3f}  open_adv={st['opening_advantage']:+.3f}")
    print()
    print("Lag profile (lag 0 = last token, lag 14 = 15th from end):")
    for lag in range(min(CLOSING_N, len(lag_profile))):
        if lag in lag_profile:
            lp = lag_profile[lag]
            print(f"  lag -{lag:2d}: S2={lp['mean_s2']:+.4f}  H={lp['mean_entropy']:.4f}  n={lp['n']}")
    print()
    print("Top 5 poems with highest closing advantage (closing > rest):")
    for r in top_closing[:5]:
        print(f"  [{r['era']}] {r['title']} ({r['author']})  close={r['closing_s2']:+.3f} rest={r['rest_s2']:+.3f} adv={r['closing_advantage']:+.3f}")
    print()
    print("Bottom 5 poems (most resolved endings):")
    for r in bottom_closing[:5]:
        print(f"  [{r['era']}] {r['title']} ({r['author']})  close={r['closing_s2']:+.3f} rest={r['rest_s2']:+.3f} adv={r['closing_advantage']:+.3f}")
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
