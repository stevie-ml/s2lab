"""
Opening Salvo: The Cold Start Problem in Poetic S2.

GPT-2 processes poems token by token. At position 0 (the first token),
there is NO prior context — the model generates from its global language
prior. As context accumulates, the model's predictions become more
constrained.

This experiment asks:
  1. Is S2 systematically different in the opening 15 tokens vs. the rest?
  2. Does opening entropy behave differently from later entropy?
  3. Does a poem's opening S2 predict its overall S2 (correlation)?
  4. Which eras have unusually high or low opening S2?
  5. What are the most striking examples of "high opening" vs "high rest" divergence?
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/opening_salvo.json"
P_NEWLINE_MAX = 0.9
OPENING_N = 15   # first N clean tokens = "opening"
MIN_CLEAN = 30   # minimum clean tokens to include poem


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def clean_tokens(poem):
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < P_NEWLINE_MAX]


def poem_stats(clean_toks):
    if not clean_toks:
        return None
    s2_vals = [t["s2"] for t in clean_toks]
    h_vals = [t["entropy"] for t in clean_toks]
    surp_vals = [t["surprisal"] for t in clean_toks]
    rank_vals = [t["rank"] for t in clean_toks]
    n = len(s2_vals)
    return {
        "n": n,
        "mean_s2": sum(s2_vals) / n,
        "mean_entropy": sum(h_vals) / n,
        "mean_surprisal": sum(surp_vals) / n,
        "mean_rank": sum(rank_vals) / n,
        "pos_s2_ratio": sum(1 for v in s2_vals if v > 0) / n,
        "spike_rate": sum(1 for v in s2_vals if v >= 3.0) / n,
    }


def main():
    corpus = load_corpus(CORPUS_PATH)

    poem_records = []
    era_opening = defaultdict(list)
    era_rest = defaultdict(list)

    for poem in corpus:
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue

        clean = clean_tokens(poem)
        if len(clean) < MIN_CLEAN:
            continue

        opening = clean[:OPENING_N]
        rest = clean[OPENING_N:]

        if not rest:
            continue

        o_stats = poem_stats(opening)
        r_stats = poem_stats(rest)
        all_stats = poem_stats(clean)

        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")
        title = poem["metadata"].get("title", "unknown")

        rec = {
            "title": title,
            "author": author,
            "era": era,
            "overall_s2": all_stats["mean_s2"],
            "opening_s2": o_stats["mean_s2"],
            "rest_s2": r_stats["mean_s2"],
            "delta": o_stats["mean_s2"] - r_stats["mean_s2"],
            "opening_entropy": o_stats["mean_entropy"],
            "rest_entropy": r_stats["mean_entropy"],
            "opening_spike_rate": o_stats["spike_rate"],
            "rest_spike_rate": r_stats["spike_rate"],
            "n_opening": o_stats["n"],
            "n_rest": r_stats["n"],
        }
        poem_records.append(rec)
        era_opening[era].append(o_stats["mean_s2"])
        era_rest[era].append(r_stats["mean_s2"])

    # Corpus-level stats
    n = len(poem_records)
    mean_opening = sum(r["opening_s2"] for r in poem_records) / n
    mean_rest = sum(r["rest_s2"] for r in poem_records) / n
    mean_opening_h = sum(r["opening_entropy"] for r in poem_records) / n
    mean_rest_h = sum(r["rest_entropy"] for r in poem_records) / n
    mean_opening_spike = sum(r["opening_spike_rate"] for r in poem_records) / n
    mean_rest_spike = sum(r["rest_spike_rate"] for r in poem_records) / n

    # Correlation: overall S2 vs opening S2
    def pearson(xs, ys):
        n = len(xs)
        mx = sum(xs) / n
        my = sum(ys) / n
        num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
        dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
        dy = math.sqrt(sum((y - my) ** 2 for y in ys))
        if dx == 0 or dy == 0:
            return 0.0
        return num / (dx * dy)

    xs = [r["opening_s2"] for r in poem_records]
    ys = [r["overall_s2"] for r in poem_records]
    corr_opening_overall = pearson(xs, ys)

    xs_rest = [r["rest_s2"] for r in poem_records]
    corr_rest_overall = pearson(xs_rest, ys)

    # Correlation: opening entropy vs rest entropy
    xhe = [r["opening_entropy"] for r in poem_records]
    yhe = [r["rest_entropy"] for r in poem_records]
    corr_h = pearson(xhe, yhe)

    # Era breakdown: avg opening vs rest s2
    era_stats = {}
    for era in sorted(era_opening.keys()):
        o_vals = era_opening[era]
        r_vals = era_rest[era]
        if len(o_vals) < 2:
            continue
        era_stats[era] = {
            "n": len(o_vals),
            "mean_opening_s2": sum(o_vals) / len(o_vals),
            "mean_rest_s2": sum(r_vals) / len(r_vals),
            "opening_advantage": sum(o_vals) / len(o_vals) - sum(r_vals) / len(r_vals),
        }

    # Top 10 poems by opening advantage (opening much higher than rest)
    top_opening = sorted(poem_records, key=lambda r: r["delta"], reverse=True)[:10]
    top_rest = sorted(poem_records, key=lambda r: r["delta"])[:10]

    # By position: aggregate S2 and entropy at each absolute position 0..OPENING_N+5
    position_s2 = defaultdict(list)
    position_h = defaultdict(list)

    for poem in corpus:
        if poem["metadata"].get("language", "en") != "en":
            continue
        clean = clean_tokens(poem)
        if len(clean) < MIN_CLEAN:
            continue
        for idx, tok in enumerate(clean):
            if idx < OPENING_N + 10:
                position_s2[idx].append(tok["s2"])
                position_h[idx].append(tok["entropy"])

    position_profile = {}
    for pos in range(OPENING_N + 10):
        s2v = position_s2[pos]
        hv = position_h[pos]
        if s2v:
            position_profile[pos] = {
                "mean_s2": sum(s2v) / len(s2v),
                "mean_entropy": sum(hv) / len(hv),
                "n": len(s2v),
            }

    output = {
        "n_poems": n,
        "opening_n_tokens": OPENING_N,
        "corpus_level": {
            "mean_opening_s2": mean_opening,
            "mean_rest_s2": mean_rest,
            "delta_opening_minus_rest": mean_opening - mean_rest,
            "mean_opening_entropy": mean_opening_h,
            "mean_rest_entropy": mean_rest_h,
            "mean_opening_spike_rate": mean_opening_spike,
            "mean_rest_spike_rate": mean_rest_spike,
            "corr_opening_vs_overall_s2": corr_opening_overall,
            "corr_rest_vs_overall_s2": corr_rest_overall,
            "corr_opening_vs_rest_entropy": corr_h,
        },
        "era_stats": era_stats,
        "position_profile": position_profile,
        "top_opening_advantage": top_opening,
        "top_rest_advantage": top_rest,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Poems analyzed: {n}")
    print(f"Opening S2 (first {OPENING_N} tokens): {mean_opening:.4f}")
    print(f"Rest S2:                              {mean_rest:.4f}")
    print(f"Delta (opening - rest):               {mean_opening - mean_rest:.4f}")
    print(f"Opening entropy:                      {mean_opening_h:.4f}")
    print(f"Rest entropy:                         {mean_rest_h:.4f}")
    print(f"Opening spike rate:                   {mean_opening_spike:.4f}")
    print(f"Rest spike rate:                      {mean_rest_spike:.4f}")
    print(f"r(opening S2, overall S2):            {corr_opening_overall:.4f}")
    print(f"r(rest S2, overall S2):               {corr_rest_overall:.4f}")
    print()
    print("Era breakdown (opening_advantage = opening_s2 - rest_s2):")
    sorted_eras = sorted(era_stats.items(), key=lambda x: -x[1]["opening_advantage"])
    for era, st in sorted_eras[:15]:
        print(f"  {era:30s} n={st['n']:3d}  open={st['mean_opening_s2']:+.3f}  rest={st['mean_rest_s2']:+.3f}  adv={st['opening_advantage']:+.3f}")
    print()
    print("Top 5 poems where opening >> rest:")
    for r in top_opening[:5]:
        print(f"  [{r['era']}] {r['title']} ({r['author']}) open={r['opening_s2']:+.3f} rest={r['rest_s2']:+.3f} delta={r['delta']:+.3f}")
    print()
    print("Top 5 poems where rest >> opening:")
    for r in top_rest[:5]:
        print(f"  [{r['era']}] {r['title']} ({r['author']}) open={r['opening_s2']:+.3f} rest={r['rest_s2']:+.3f} delta={r['delta']:+.3f}")
    print()
    print("Position-level profile (first 15 clean tokens):")
    for pos in range(min(OPENING_N, max(position_profile.keys()) + 1)):
        if pos in position_profile:
            pp = position_profile[pos]
            print(f"  pos {pos:2d}: S2={pp['mean_s2']:+.4f}  H={pp['mean_entropy']:.4f}  n={pp['n']}")
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
