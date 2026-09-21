"""
Corpus-Wide Impact of the Stanza-Break Artifact on S₂ Statistics

experiments/stanza_break_artifact.py showed that line-head S₂ is dominated by
positions where GPT-2 was near-certain a newline came next. This script asks
the harder question: how much of the LAB'S HEADLINE NUMBERS is artifact?

Specifically it re-derives, with artifact positions excluded:
  - avg S₂ per era (the lab's most-cited table)
  - the poetry-vs-prose gap (the project's core claim)
  - the top-S₂ poem rankings

NON-CIRCULARITY CHECK
---------------------
The exclusion rule uses only the model's predictive distribution — how much
probability mass sits on a newline continuation — and never looks at S₂ or at
which token the poet actually wrote. The concern is nonetheless that the rule
selects high-S₂ tokens by construction. It does, and that is the argument: at
a position where p(newline) ≈ 1, entropy ≈ 0, so S₂ ≈ surprisal, and ANY
non-newline token scores ~20 bits. The poet's lexical choice contributes
almost nothing to the number. Test A below quantifies this: if the artifact
positions are genuinely choice-insensitive, S₂ there should have LOW variance
relative to its mean, and should be near-identical for common and rare words.
"""

import json
import math
import os
import statistics
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "artifact_corpus_impact.json")

ARTIFACT_P = 0.90


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    # ── Test A: are artifact positions choice-insensitive? ──
    art, clean = [], []
    for entry in corpus:
        for t in entry["tokens"]:
            (art if newline_prob(t) >= ARTIFACT_P else clean).append(t)

    print("=" * 74)
    print("CORPUS-WIDE IMPACT OF THE STANZA-BREAK ARTIFACT")
    print(f"{sum(len(e['tokens']) for e in corpus)} tokens, {len(corpus)} texts")
    print("=" * 74)

    print("\n--- TEST A: ARE ARTIFACT POSITIONS INSENSITIVE TO WHAT THE POET WROTE? ---")
    for label, g in (("artifact (p_nl>=0.9)", art), ("clean", clean)):
        s2 = [t["s2"] for t in g]
        print(f"  {label:<24} n={len(g):<6} mean S2={statistics.mean(s2):>7.3f}  "
              f"sd={statistics.stdev(s2):>6.3f}  CV={statistics.stdev(s2)/abs(statistics.mean(s2)):>5.2f}  "
              f"mean entropy={statistics.mean(t['entropy'] for t in g):>6.3f}")

    # Does the poet's word matter at artifact positions? Compare S2 for tokens
    # the model ranked highly vs poorly among NON-newline options.
    print("\n  S2 at artifact positions, split by the chosen token's own probability:")
    print(f"  {'p(chosen token)':<22}{'n':>7}{'mean S2':>10}{'sd':>8}")
    for lo, hi in [(0, 1e-6), (1e-6, 1e-5), (1e-5, 1e-4), (1e-4, 1.0)]:
        g = [t for t in art if lo <= t["prob"] < hi]
        if len(g) < 5:
            continue
        s2 = [t["s2"] for t in g]
        print(f"  {f'{lo:g}-{hi:g}':<22}{len(g):>7}{statistics.mean(s2):>10.3f}"
              f"{statistics.stdev(s2):>8.3f}")

    # ── Era table, raw vs cleaned ──
    print("\n--- ERA AVG S2: AS REPORTED vs ARTIFACT-FREE ---")
    print(f"{'era':<22}{'n':>4}{'S2 raw':>9}{'S2 clean':>10}{'delta':>9}"
          f"{'%tok art':>10}{'rank raw':>10}{'rank new':>9}")

    era_tok = defaultdict(list)
    era_texts = defaultdict(set)
    for entry in corpus:
        era = entry["metadata"]["era"]
        era_texts[era].add(entry["metadata"]["title"])
        era_tok[era] += entry["tokens"]

    rows = []
    for era, toks in era_tok.items():
        cl = [t for t in toks if newline_prob(t) < ARTIFACT_P]
        if not cl:
            continue
        raw = statistics.mean(t["s2"] for t in toks)
        clean_m = statistics.mean(t["s2"] for t in cl)
        rows.append({
            "era": era,
            "n_texts": len(era_texts[era]),
            "s2_raw": raw,
            "s2_clean": clean_m,
            "pct_artifact": 1 - len(cl) / len(toks),
        })

    raw_rank = {r["era"]: i + 1 for i, r in
                enumerate(sorted(rows, key=lambda r: -r["s2_raw"]))}
    new_rank = {r["era"]: i + 1 for i, r in
                enumerate(sorted(rows, key=lambda r: -r["s2_clean"]))}
    for r in rows:
        r["rank_raw"] = raw_rank[r["era"]]
        r["rank_clean"] = new_rank[r["era"]]

    for r in sorted(rows, key=lambda r: -r["s2_raw"]):
        move = r["rank_raw"] - r["rank_clean"]
        arrow = f"{r['rank_clean']}" + ("" if move == 0 else f" ({move:+d})")
        print(f"{r['era']:<22}{r['n_texts']:>4}{r['s2_raw']:>9.3f}{r['s2_clean']:>10.3f}"
              f"{r['s2_clean'] - r['s2_raw']:>+9.3f}{r['pct_artifact']:>10.1%}"
              f"{r['rank_raw']:>10}{arrow:>9}")

    # ── The core poetry-vs-prose claim ──
    print("\n--- THE CORE CLAIM: POETRY vs PROSE, ARTIFACT-FREE ---")
    poetry_t, prose_t = [], []
    for entry in corpus:
        tgt = prose_t if entry["metadata"]["era"] == "control" else poetry_t
        tgt += entry["tokens"]

    for label, toks in (("poetry", poetry_t), ("control prose", prose_t)):
        cl = [t for t in toks if newline_prob(t) < ARTIFACT_P]
        raw = statistics.mean(t["s2"] for t in toks)
        clm = statistics.mean(t["s2"] for t in cl)
        praw = sum(1 for t in toks if t["s2"] > 0) / len(toks)
        pcl = sum(1 for t in cl if t["s2"] > 0) / len(cl)
        print(f"  {label:<15} raw S2={raw:>7.3f} (pos {praw:.0%})   "
              f"clean S2={clm:>7.3f} (pos {pcl:.0%})   "
              f"artifact tokens={1 - len(cl)/len(toks):.1%}")

    p_raw = statistics.mean(t["s2"] for t in poetry_t)
    c_raw = statistics.mean(t["s2"] for t in prose_t)
    p_cl = statistics.mean(t["s2"] for t in poetry_t if newline_prob(t) < ARTIFACT_P)
    c_cl = statistics.mean(t["s2"] for t in prose_t if newline_prob(t) < ARTIFACT_P)
    print(f"\n  poetry-prose gap  raw = {p_raw - c_raw:+.3f} bits")
    print(f"  poetry-prose gap clean = {p_cl - c_cl:+.3f} bits "
          f"({(p_cl - c_cl) / (p_raw - c_raw):.0%} of the reported gap survives)")

    # ── Poem rankings ──
    print("\n--- TOP-S2 POEMS: AS REPORTED vs ARTIFACT-FREE ---")
    poems = []
    for entry in corpus:
        toks = entry["tokens"]
        cl = [t for t in toks if newline_prob(t) < ARTIFACT_P]
        if len(cl) < 10:
            continue
        poems.append({
            "title": entry["metadata"]["title"],
            "author": entry["metadata"]["author"],
            "era": entry["metadata"]["era"],
            "s2_raw": statistics.mean(t["s2"] for t in toks),
            "s2_clean": statistics.mean(t["s2"] for t in cl),
            "pct_artifact": 1 - len(cl) / len(toks),
        })

    print("  reported top 8:")
    for p in sorted(poems, key=lambda p: -p["s2_raw"])[:8]:
        print(f"    {p['s2_raw']:>6.2f} -> {p['s2_clean']:>6.2f}  "
              f"({p['pct_artifact']:>4.0%} artifact)  {p['author'][:20]:<21} {p['title'][:34]}")
    print("  artifact-free top 8:")
    for p in sorted(poems, key=lambda p: -p["s2_clean"])[:8]:
        print(f"    {p['s2_clean']:>6.2f} (raw {p['s2_raw']:>5.2f})  "
              f"{p['author'][:20]:<21} {p['title'][:34]}")

    with open(OUT_JSON, "w") as f:
        json.dump({
            "artifact_threshold_p_newline": ARTIFACT_P,
            "n_tokens_total": len(art) + len(clean),
            "n_tokens_artifact": len(art),
            "artifact_mean_s2": round(statistics.mean(t["s2"] for t in art), 4),
            "clean_mean_s2": round(statistics.mean(t["s2"] for t in clean), 4),
            "by_era": sorted(rows, key=lambda r: -r["s2_raw"]),
            "poetry_prose": {
                "poetry_raw": round(p_raw, 4), "poetry_clean": round(p_cl, 4),
                "prose_raw": round(c_raw, 4), "prose_clean": round(c_cl, 4),
                "gap_raw": round(p_raw - c_raw, 4),
                "gap_clean": round(p_cl - c_cl, 4),
            },
            "poems": sorted(poems, key=lambda p: -p["s2_clean"]),
        }, f, indent=2)
    print(f"\nSaved: {OUT_JSON}")


if __name__ == "__main__":
    main()
