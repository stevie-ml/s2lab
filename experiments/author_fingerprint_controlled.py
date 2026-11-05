"""
Author Fingerprint After Sentence-Length Control

After removing the structural dampening effect of sentence length (finding:
longer sentences have lower S2 because GPT-2 gains predictive certainty),
which poets show genuine *lexical* creativity vs. those who achieve high raw
S2 mainly through short, fragmentary syntax?

Builds on:
  findings/sentence_length_s2.md  (Pearson r = -0.233 between sent_len and S2)
  findings/second_person_address_s2.md
"""

import json
import re
import sys
import os
import numpy as np
from collections import defaultdict
from datetime import datetime

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
RESULTS_DIR  = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")


def split_into_sentences(tokens_data):
    """Split a token list into sentences using terminal punctuation + newline heuristics."""
    sentences = []
    current = []
    for tok in tokens_data:
        current.append(tok)
        t = tok["token"].rstrip()
        # Sentence boundary: ends with . ! ? or high p_newline probability
        if t.endswith((".", "!", "?")) or tok.get("p_newline", 0) > 0.5:
            if current:
                sentences.append(current)
            current = []
    if current:
        sentences.append(current)
    return sentences


def build_sent_len_correction(all_records):
    """
    For each sentence-length bucket, compute mean S2.
    Returns a dict: sent_len -> mean_s2.
    Uses bucket sizes matching the previous experiment.
    """
    # Bin boundaries (upper-inclusive)
    bins = [1, 2, 4, 7, 12, 20, 33, 54, 999]
    bin_values = defaultdict(list)
    for rec in all_records:
        sl = rec["sent_len"]
        for b in bins:
            if sl <= b:
                bin_values[b].append(rec["s2"])
                break
    correction = {}
    for b, vals in bin_values.items():
        correction[b] = np.mean(vals)
    return correction, bins


def get_correction(sent_len, correction, bins):
    for b in bins:
        if sent_len <= b:
            return correction.get(b, 0.0)
    return correction.get(bins[-1], 0.0)


def main():
    print("Loading corpus results...")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)
    print(f"  {len(corpus)} poems")

    # ── Step 1: Assign sentence lengths to all tokens ──────────────────────────
    all_records = []  # one entry per non-artifact token

    for poem in corpus:
        meta   = poem["metadata"]
        tokens = poem["tokens"]
        author = meta.get("author", "Unknown")
        era    = meta.get("era", "unknown")
        title  = meta.get("title", "")
        year   = meta.get("year", 0) or 0

        sentences = split_into_sentences(tokens)
        for sent in sentences:
            sl = len(sent)
            for tok in sent:
                # Skip stanza-break artifact (line-initial capital after newline)
                if tok.get("p_newline", 0) > 0.5:
                    continue
                all_records.append({
                    "author": author,
                    "era":    era,
                    "title":  title,
                    "year":   year,
                    "sent_len": sl,
                    "s2":     tok["s2"],
                    "token":  tok["token"],
                })

    print(f"  {len(all_records)} non-artifact tokens across all poems")

    # ── Step 2: Build sentence-length correction model ─────────────────────────
    correction, bins = build_sent_len_correction(all_records)
    global_mean = np.mean([r["s2"] for r in all_records])

    print("\nSentence-length correction table:")
    print(f"  {'Bin ≤':>8}  {'Mean S2':>8}  {'Correction':>10}  {'n':>6}")
    for b in bins:
        vals = [r["s2"] for r in all_records if any(
            r["sent_len"] <= bb and bb == b for bb in bins
        )]
        # Recompute properly
        pass

    # Cleaner recompute
    bin_groups = defaultdict(list)
    for rec in all_records:
        sl = rec["sent_len"]
        for b in bins:
            if sl <= b:
                bin_groups[b].append(rec["s2"])
                break

    correction = {b: np.mean(v) for b, v in bin_groups.items()}
    global_mean = np.mean([r["s2"] for r in all_records])

    print(f"\n  Global mean S2: {global_mean:.3f}")
    print(f"  {'Bin ≤':>8}  {'n':>6}  {'Mean S2':>8}  {'Correction':>10}")
    for b in bins:
        if b in bin_groups:
            n = len(bin_groups[b])
            m = correction[b]
            print(f"  {b:>8}  {n:>6}  {m:+.3f}    {m - global_mean:+.3f}")

    # ── Step 3: Compute residual S2 for every token ─────────────────────────────
    for rec in all_records:
        sl = rec["sent_len"]
        sl_mean = get_correction(sl, correction, bins)
        # Residual: how much higher/lower than expected for this sentence length?
        rec["s2_residual"] = rec["s2"] - sl_mean + global_mean

    # ── Step 4: Aggregate by author ────────────────────────────────────────────
    author_buckets = defaultdict(lambda: {"s2_raw": [], "s2_res": [], "titles": set(),
                                          "sent_lens": [], "era": "unknown", "year": 0})
    for rec in all_records:
        a = rec["author"]
        author_buckets[a]["s2_raw"].append(rec["s2"])
        author_buckets[a]["s2_res"].append(rec["s2_residual"])
        author_buckets[a]["titles"].add(rec["title"])
        author_buckets[a]["sent_lens"].append(rec["sent_len"])
        author_buckets[a]["era"] = rec["era"]
        author_buckets[a]["year"] = max(author_buckets[a]["year"], rec["year"])

    # Only include authors with ≥ 100 tokens (enough for reliable mean)
    MIN_TOKENS = 100
    summary = {}
    for author, d in author_buckets.items():
        if len(d["s2_raw"]) < MIN_TOKENS:
            continue
        raw   = np.array(d["s2_raw"])
        res   = np.array(d["s2_res"])
        avg_sl = np.mean(d["sent_lens"])
        summary[author] = {
            "n_tokens":          len(raw),
            "n_poems":           len(d["titles"]),
            "avg_sent_len":      float(avg_sl),
            "avg_s2_raw":        float(np.mean(raw)),
            "avg_s2_residual":   float(np.mean(res)),
            "std_s2_raw":        float(np.std(raw)),
            "std_s2_residual":   float(np.std(res)),
            "era":               d["era"],
            "year":              d["year"],
        }

    # ── Step 5: Rank comparisons ────────────────────────────────────────────────
    ranked_raw = sorted(summary.items(), key=lambda x: x[1]["avg_s2_raw"], reverse=True)
    ranked_res = sorted(summary.items(), key=lambda x: x[1]["avg_s2_residual"], reverse=True)

    # Build rank-change lookup
    raw_rank = {a: i+1 for i, (a, _) in enumerate(ranked_raw)}
    res_rank = {a: i+1 for i, (a, _) in enumerate(ranked_res)}
    rank_change = {a: raw_rank[a] - res_rank[a] for a in summary}

    n_authors = len(summary)
    print(f"\n{n_authors} authors with ≥{MIN_TOKENS} tokens")

    print("\n── TOP 25 BY RAW S₂ ────────────────────────────────────────────────────────")
    print(f"  {'Rank':>4}  {'Author':<28}  {'Raw S2':>7}  {'Res S2':>7}  {'Avg SentLen':>11}  {'ΔRank':>6}")
    for i, (author, d) in enumerate(ranked_raw[:25]):
        chg = rank_change[author]
        print(f"  {i+1:>4}  {author:<28}  {d['avg_s2_raw']:+.3f}  {d['avg_s2_residual']:+.3f}  "
              f"{d['avg_sent_len']:>11.1f}  {chg:+5d}")

    print("\n── TOP 25 BY RESIDUAL S₂ (sentence-length controlled) ──────────────────────")
    print(f"  {'Rank':>4}  {'Author':<28}  {'Res S2':>7}  {'Raw S2':>7}  {'Avg SentLen':>11}  {'ΔRank':>6}")
    for i, (author, d) in enumerate(ranked_res[:25]):
        chg = rank_change[author]
        print(f"  {i+1:>4}  {author:<28}  {d['avg_s2_residual']:+.3f}  {d['avg_s2_raw']:+.3f}  "
              f"{d['avg_sent_len']:>11.1f}  {chg:+5d}")

    # Biggest risers and fallers
    movers = sorted(rank_change.items(), key=lambda x: x[1], reverse=True)
    biggest_rise  = movers[:8]
    biggest_fall  = movers[-8:][::-1]

    print("\n── BIGGEST RANK RISES after sentence-length control ───────────────────────")
    print(f"  {'Author':<28}  {'Raw Rank':>8}  {'Res Rank':>8}  {'Rise':>5}  "
          f"{'Avg SL':>6}  {'Raw S2':>7}  {'Res S2':>7}")
    for author, chg in biggest_rise:
        d = summary[author]
        print(f"  {author:<28}  {raw_rank[author]:>8}  {res_rank[author]:>8}  {chg:>+5}  "
              f"{d['avg_sent_len']:>6.1f}  {d['avg_s2_raw']:+.3f}  {d['avg_s2_residual']:+.3f}")

    print("\n── BIGGEST RANK FALLS after sentence-length control ───────────────────────")
    print(f"  {'Author':<28}  {'Raw Rank':>8}  {'Res Rank':>8}  {'Fall':>5}  "
          f"{'Avg SL':>6}  {'Raw S2':>7}  {'Res S2':>7}")
    for author, chg in biggest_fall:
        d = summary[author]
        print(f"  {author:<28}  {raw_rank[author]:>8}  {res_rank[author]:>8}  {chg:>+5}  "
              f"{d['avg_sent_len']:>6.1f}  {d['avg_s2_raw']:+.3f}  {d['avg_s2_residual']:+.3f}")

    # ── Step 6: Era-level analysis ─────────────────────────────────────────────
    era_buckets = defaultdict(lambda: {"s2_raw": [], "s2_res": [], "sent_lens": []})
    for rec in all_records:
        e = rec["era"]
        era_buckets[e]["s2_raw"].append(rec["s2"])
        era_buckets[e]["s2_res"].append(rec["s2_residual"])
        era_buckets[e]["sent_lens"].append(rec["sent_len"])

    era_summary = {}
    for era, d in era_buckets.items():
        if len(d["s2_raw"]) < 50:
            continue
        era_summary[era] = {
            "n":              len(d["s2_raw"]),
            "avg_s2_raw":     float(np.mean(d["s2_raw"])),
            "avg_s2_residual": float(np.mean(d["s2_res"])),
            "avg_sent_len":   float(np.mean(d["sent_lens"])),
        }

    ranked_era_raw = sorted(era_summary.items(), key=lambda x: x[1]["avg_s2_raw"], reverse=True)
    ranked_era_res = sorted(era_summary.items(), key=lambda x: x[1]["avg_s2_residual"], reverse=True)
    era_raw_rank = {e: i+1 for i, (e, _) in enumerate(ranked_era_raw)}
    era_res_rank = {e: i+1 for i, (e, _) in enumerate(ranked_era_res)}

    print("\n── ERA RANKINGS: Raw vs Residual S₂ ────────────────────────────────────────")
    print(f"  {'Era':<30}  {'Raw S2':>7}  {'Res S2':>7}  {'Avg SL':>6}  {'ΔRank':>6}  {'n':>5}")
    for era, d in ranked_era_res:
        chg = era_raw_rank[era] - era_res_rank[era]
        print(f"  {era:<30}  {d['avg_s2_raw']:+.3f}  {d['avg_s2_residual']:+.3f}  "
              f"{d['avg_sent_len']:>6.1f}  {chg:>+6}  {d['n']:>5}")

    # ── Step 7: "Genuine surprise" candidates ──────────────────────────────────
    # Find poets whose residual S2 is significantly higher than raw, AND residual is high
    print("\n── 'GENUINE LEXICAL CREATIVITY' LEADERS (high residual, long sentences) ──")
    genuine = [(a, d) for a, d in summary.items()
               if d["avg_s2_residual"] > 0.3 and d["avg_sent_len"] > 8]
    genuine.sort(key=lambda x: x[1]["avg_s2_residual"], reverse=True)
    print(f"  {'Author':<28}  {'Res S2':>7}  {'Raw S2':>7}  {'Avg SL':>7}  {'nPms':>5}")
    for author, d in genuine[:15]:
        print(f"  {author:<28}  {d['avg_s2_residual']:+.3f}  {d['avg_s2_raw']:+.3f}  "
              f"{d['avg_sent_len']:>7.1f}  {d['n_poems']:>5}")

    # ── Save results ───────────────────────────────────────────────────────────
    output = {
        "date":          datetime.now().isoformat(),
        "n_poems":       len(corpus),
        "n_tokens":      len(all_records),
        "global_mean_s2": global_mean,
        "sent_len_correction": {str(k): v for k, v in correction.items()},
        "author_summary": summary,
        "era_summary":    era_summary,
        "top_raw":        [(a, d["avg_s2_raw"], d["avg_s2_residual"]) for a, d in ranked_raw[:30]],
        "top_residual":   [(a, d["avg_s2_residual"], d["avg_s2_raw"]) for a, d in ranked_res[:30]],
        "biggest_rises":  [(a, rank_change[a]) for a, _ in biggest_rise],
        "biggest_falls":  [(a, rank_change[a]) for a, _ in biggest_fall],
    }

    out_path = os.path.join(RESULTS_DIR, "author_fingerprint_controlled.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    return output


if __name__ == "__main__":
    main()
