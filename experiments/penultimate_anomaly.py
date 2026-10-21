"""
The Penultimate Anomaly: Why Is the Second-to-Last Token Uniquely Elevated?

From closing_salvo.md:
  lag 0 (last):       S2 = -1.330, entropy = 4.22
  lag -1 (penultimate): S2 = +0.019, entropy = 6.195  ← strikingly high
  lag -2:             S2 = -1.013, entropy = 6.023

The penultimate token stands out as NEAR ZERO S2 in the middle of a deeply
negative closing window. Everything around it conforms; the penultimate does
not (or does so far less). This experiment characterizes WHAT makes the
penultimate position distinct.

Research questions:
  1. Is the penultimate anomaly consistent across eras/genres?
  2. What token types (by surface form category) appear at lag -1?
  3. What is the Straussian gap at lag -1? What does GPT-2 expect vs. what arrives?
  4. Is the elevated lag -1 due to higher entropy (model uncertainty) or
     higher surprisal (poet choice)?
  5. Does the penultimate S2 predict anything about the poem?
  6. Do poems with high penultimate S2 also have defiant closings?
     (Linking to closing_salvo.md's "42.6% defiant closers" finding.)

Hypothesis: the penultimate position is where poets make their last
non-trivial decision. The final token is typically "locked in" by the
preceding structure (meter, rhyme, syntax), but the penultimate still has
a degree of freedom. Poets use this last free slot to make a small,
final deviation.
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/penultimate_anomaly.json"
P_NEWLINE_MAX = 0.9
MIN_CLEAN = 30


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def clean_tokens(poem):
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < P_NEWLINE_MAX]


def top_prediction(tok):
    alts = tok.get("alternatives", [])
    if alts:
        return alts[0]["token"]
    return ""


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


def classify_token(text):
    """Rough surface-form categorization for common token patterns."""
    t = text.strip().lower()
    if not t:
        return "empty"
    # punctuation / symbols
    if all(c in ".,;:!?'\"-—–()[]{}/" for c in t):
        return "punct"
    # numbers
    if t.isdigit():
        return "numeral"
    # possessives / contractions
    if "'" in t:
        return "contraction"
    # capitalized mid-text → proper noun candidate
    if text[0].isupper() and len(text) > 1:
        return "capitalized"
    # function words
    FUNCTION = {
        "the", "a", "an", "of", "in", "on", "at", "to", "by", "with",
        "from", "for", "and", "or", "but", "nor", "yet", "so",
        "i", "you", "he", "she", "it", "we", "they", "my", "your",
        "his", "her", "its", "our", "their", "me", "him", "us", "them",
        "is", "are", "was", "were", "be", "been", "being", "am",
        "have", "has", "had", "do", "does", "did",
        "not", "no", "never", "nor",
        "that", "this", "these", "those",
        "as", "if", "when", "while", "though", "although",
        "after", "before", "since", "until", "than",
    }
    if t in FUNCTION:
        return "function"
    return "content"


def main():
    corpus = load_corpus(CORPUS_PATH)

    # Per-poem records
    poem_records = []
    # Token-level records for lag -1 (penultimate) and lag 0 (last)
    pen_tokens = []   # penultimate tokens
    last_tokens = []  # last tokens
    lag2_tokens = []  # lag -2 tokens

    era_records = defaultdict(list)  # era -> list of penultimate S2

    # Aggregate lag profile (extending closing_salvo.md, lags 0-20)
    lag_s2 = defaultdict(list)
    lag_h = defaultdict(list)
    lag_surprisal = defaultdict(list)

    for poem in corpus:
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue

        clean = clean_tokens(poem)
        if len(clean) < MIN_CLEAN:
            continue

        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")
        title = poem["metadata"].get("title", "unknown")

        all_s2 = [t["s2"] for t in clean]
        overall_mean = sum(all_s2) / len(all_s2)

        # Record per-lag data
        for lag_i in range(min(21, len(clean))):
            tok = clean[-(lag_i + 1)]
            lag_s2[lag_i].append(tok["s2"])
            lag_h[lag_i].append(tok["entropy"])
            # surprisal = s2 + entropy
            lag_surprisal[lag_i].append(tok["s2"] + tok["entropy"])

        if len(clean) >= 2:
            pen = clean[-2]   # penultimate
            last = clean[-1]  # last

            pen_cat = classify_token(pen.get("token", ""))
            last_cat = classify_token(last.get("token", ""))

            pen_record = {
                "token": pen.get("token", ""),
                "s2": pen["s2"],
                "entropy": pen["entropy"],
                "surprisal": pen["s2"] + pen["entropy"],
                "top_pred": top_prediction(pen),
                "top_pred_prob": pen.get("alternatives", [{}])[0].get("prob") if pen.get("alternatives") else None,
                "category": pen_cat,
                "era": era,
                "author": author,
                "title": title,
                "overall_s2": overall_mean,
            }
            pen_tokens.append(pen_record)

            last_record = {
                "token": last.get("token", ""),
                "s2": last["s2"],
                "entropy": last["entropy"],
                "surprisal": last["s2"] + last["entropy"],
                "top_pred": top_prediction(last),
                "top_pred_prob": last.get("alternatives", [{}])[0].get("prob") if last.get("alternatives") else None,
                "category": last_cat,
                "era": era,
            }
            last_tokens.append(last_record)

            # poem-level record
            poem_records.append({
                "title": title,
                "author": author,
                "era": era,
                "overall_s2": overall_mean,
                "pen_s2": pen["s2"],
                "pen_h": pen["entropy"],
                "last_s2": last["s2"],
                "last_h": last["entropy"],
                "pen_minus_last": pen["s2"] - last["s2"],
                "pen_above_overall": pen["s2"] - overall_mean,
                "pen_token": pen.get("token", ""),
                "last_token": last.get("token", ""),
                "pen_top_pred": top_prediction(pen),
                "last_top_pred": top_prediction(last),
                "pen_category": pen_cat,
                "last_category": last_cat,
            })
            era_records[era].append(pen["s2"])

        if len(clean) >= 3:
            l2 = clean[-3]
            lag2_tokens.append({
                "token": l2.get("token", ""),
                "s2": l2["s2"],
                "entropy": l2["entropy"],
                "era": era,
            })

    n = len(poem_records)

    # --- Global lag profile ---
    lag_profile = {}
    for lag_i in range(21):
        if lag_s2[lag_i]:
            s2v = lag_s2[lag_i]
            hv = lag_h[lag_i]
            sprv = lag_surprisal[lag_i]
            lag_profile[lag_i] = {
                "mean_s2": sum(s2v) / len(s2v),
                "mean_entropy": sum(hv) / len(hv),
                "mean_surprisal": sum(sprv) / len(sprv),
                "n": len(s2v),
                "pos_rate": sum(1 for v in s2v if v > 0) / len(s2v),
                "spike_rate": sum(1 for v in s2v if v >= 3.0) / len(s2v),
            }

    # --- Category breakdown for penultimate vs. last ---
    def cat_stats(records):
        cats = defaultdict(list)
        for r in records:
            cats[r["category"]].append(r["s2"])
        return {
            cat: {
                "n": len(vals),
                "mean_s2": sum(vals) / len(vals),
                "pct": len(vals) / len(records) * 100,
            }
            for cat, vals in sorted(cats.items(), key=lambda x: -len(x[1]))
        }

    pen_cat_stats = cat_stats(pen_tokens)
    last_cat_stats = cat_stats(last_tokens)

    # --- Top penultimate Straussian moments ---
    top_pen = sorted(poem_records, key=lambda r: r["pen_s2"], reverse=True)[:15]
    # Poems where penultimate >> last (final "setup → resolution")
    top_gap = sorted(poem_records, key=lambda r: r["pen_minus_last"], reverse=True)[:15]
    # Poems where last > penultimate (inverted: surprise at final word)
    inverted = sorted(poem_records, key=lambda r: r["pen_minus_last"])[:15]

    # --- Era stats ---
    era_stats = {}
    for era, vals in era_records.items():
        if len(vals) < 2:
            continue
        era_stats[era] = {
            "n": len(vals),
            "mean_pen_s2": sum(vals) / len(vals),
        }

    # --- Correlation: penultimate S2 vs. overall S2 ---
    pen_s2_list = [r["pen_s2"] for r in poem_records]
    overall_list = [r["overall_s2"] for r in poem_records]
    last_s2_list = [r["last_s2"] for r in poem_records]
    corr_pen_overall = pearson(pen_s2_list, overall_list)
    corr_last_overall = pearson(last_s2_list, overall_list)

    # --- Decompose the lag-1 S2: is it entropy or surprisal driven? ---
    lag0 = lag_profile.get(0, {})
    lag1 = lag_profile.get(1, {})
    lag2 = lag_profile.get(2, {})

    # --- Token frequency at penultimate position ---
    pen_token_freq = defaultdict(int)
    for r in pen_tokens:
        tok = r["token"].strip().lower()
        pen_token_freq[tok] += 1
    top_pen_tokens = sorted(pen_token_freq.items(), key=lambda x: -x[1])[:30]

    last_token_freq = defaultdict(int)
    for r in last_tokens:
        tok = r["token"].strip().lower()
        last_token_freq[tok] += 1
    top_last_tokens = sorted(last_token_freq.items(), key=lambda x: -x[1])[:30]

    # --- What does GPT-2 expect at lag -1, and what arrives? ---
    # Collect the "unsaid" at penultimate position: top_pred vs actual token
    straussian_pen_examples = [
        {
            "title": r["title"],
            "author": r["author"],
            "era": r["era"],
            "actual_pen": r["pen_token"],
            "expected_pen": r["pen_top_pred"],
            "actual_last": r["last_token"],
            "expected_last": r["last_top_pred"],
            "pen_s2": r["pen_s2"],
            "last_s2": r["last_s2"],
        }
        for r in top_pen[:20]
    ]

    output = {
        "n_poems": n,
        "global_lag_profile": lag_profile,
        "lag_decomposition_focus": {
            "lag_0_last": lag0,
            "lag_1_penultimate": lag1,
            "lag_2_antepenultimate": lag2,
            "note": "lag -1 S2 elevation: how much is entropy vs surprisal?",
            "lag1_entropy_vs_lag0": (lag1.get("mean_entropy", 0) - lag0.get("mean_entropy", 0)),
            "lag1_surprisal_vs_lag0": (lag1.get("mean_surprisal", 0) - lag0.get("mean_surprisal", 0)),
            "lag1_s2_vs_lag0": (lag1.get("mean_s2", 0) - lag0.get("mean_s2", 0)),
        },
        "category_breakdown": {
            "penultimate": pen_cat_stats,
            "last": last_cat_stats,
        },
        "era_pen_s2": era_stats,
        "correlations": {
            "pen_s2_vs_overall": corr_pen_overall,
            "last_s2_vs_overall": corr_last_overall,
        },
        "top_pen_tokens": top_pen_tokens,
        "top_last_tokens": top_last_tokens,
        "top_penultimate_s2_poems": top_pen,
        "top_pen_minus_last_poems": top_gap,
        "inverted_poems": inverted,
        "straussian_gap_examples": straussian_pen_examples,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Poems analyzed: {n}")
    print()
    print("=== GLOBAL LAG PROFILE (last 21 tokens, lag 0 = last) ===")
    print(f"{'lag':>5}  {'mean S2':>9}  {'entropy':>9}  {'surprisal':>10}  {'pos_rate':>9}  {'spike_rate':>10}  n")
    for lag_i in range(21):
        if lag_i in lag_profile:
            lp = lag_profile[lag_i]
            marker = " ← PENULTIMATE" if lag_i == 1 else (" ← LAST" if lag_i == 0 else "")
            print(f"{-lag_i:>5}  {lp['mean_s2']:>+9.4f}  {lp['mean_entropy']:>9.4f}  {lp['mean_surprisal']:>10.4f}  {lp['pos_rate']:>9.3f}  {lp['spike_rate']:>10.3f}  {lp['n']}{marker}")
    print()
    print("=== LAG -1 (PENULTIMATE) DECOMPOSITION ===")
    print(f"  lag 0  (last):        S2={lag0.get('mean_s2', 0):+.4f}  H={lag0.get('mean_entropy', 0):.4f}  surprisal={lag0.get('mean_surprisal', 0):.4f}")
    print(f"  lag -1 (penultimate): S2={lag1.get('mean_s2', 0):+.4f}  H={lag1.get('mean_entropy', 0):.4f}  surprisal={lag1.get('mean_surprisal', 0):.4f}")
    print(f"  lag -2 (antepen):     S2={lag2.get('mean_s2', 0):+.4f}  H={lag2.get('mean_entropy', 0):.4f}  surprisal={lag2.get('mean_surprisal', 0):.4f}")
    print(f"  lag1 vs lag0 — S2 diff={lag1.get('mean_s2', 0) - lag0.get('mean_s2', 0):+.4f}  H diff={lag1.get('mean_entropy', 0) - lag0.get('mean_entropy', 0):+.4f}  surprisal diff={lag1.get('mean_surprisal', 0) - lag0.get('mean_surprisal', 0):+.4f}")
    print()
    print("=== CATEGORY BREAKDOWN ===")
    print("Penultimate token categories:")
    for cat, st in pen_cat_stats.items():
        print(f"  {cat:15s}  n={st['n']:4d}  {st['pct']:5.1f}%  mean_S2={st['mean_s2']:+.4f}")
    print("Last token categories:")
    for cat, st in last_cat_stats.items():
        print(f"  {cat:15s}  n={st['n']:4d}  {st['pct']:5.1f}%  mean_S2={st['mean_s2']:+.4f}")
    print()
    print(f"r(pen S2, overall S2) = {corr_pen_overall:.4f}")
    print(f"r(last S2, overall S2) = {corr_last_overall:.4f}")
    print()
    print("=== TOP 15 MOST FREQUENT PENULTIMATE TOKENS ===")
    for tok, cnt in top_pen_tokens[:15]:
        print(f"  {repr(tok):25s}  {cnt:4d}")
    print()
    print("=== TOP 15 MOST FREQUENT LAST TOKENS ===")
    for tok, cnt in top_last_tokens[:15]:
        print(f"  {repr(tok):25s}  {cnt:4d}")
    print()
    print("=== TOP 10 POEMS: HIGHEST PENULTIMATE S2 ===")
    for r in top_pen[:10]:
        print(f"  [{r['era']}] {r['title']} ({r['author']})")
        print(f"      pen='{r['pen_token']}'  expected='{r['pen_top_pred']}'  S2={r['pen_s2']:+.3f}")
        print(f"      last='{r['last_token']}'  expected='{r['last_top_pred']}'  S2={r['last_s2']:+.3f}")
    print()
    print("=== TOP 10: STRONGEST 'SETUP→RESOLUTION' (pen_S2 >> last_S2) ===")
    for r in top_gap[:10]:
        print(f"  [{r['era']}] {r['title']} ({r['author']})")
        print(f"      pen='{r['pen_token']}'(S2={r['pen_s2']:+.3f})  last='{r['last_token']}'(S2={r['last_s2']:+.3f})  gap={r['pen_minus_last']:+.3f}")
    print()
    print("=== TOP 10: INVERTED (last_S2 > pen_S2) — FINAL WORD IS THE SURPRISE ===")
    for r in inverted[:10]:
        print(f"  [{r['era']}] {r['title']} ({r['author']})")
        print(f"      pen='{r['pen_token']}'(S2={r['pen_s2']:+.3f})  last='{r['last_token']}'(S2={r['last_s2']:+.3f})  gap={r['pen_minus_last']:+.3f}")
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
