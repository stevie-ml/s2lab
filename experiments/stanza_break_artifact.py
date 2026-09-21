"""
The Stanza-Break Artifact: A Confound in Line-Head S₂

DISCOVERY CONTEXT
-----------------
While testing whether villanelle refrains create a periodic S₂ signal
(experiments/spectral_refrain.py), the refrain's *second* occurrence appeared
to carry an enormous S₂ jump (+15.7 bits at the line head). Inspection of the
token stream showed the effect is not about refrains at all.

In Wilde's villanelle, the huge line-head spikes land on:
    token  6  'In'    S2=12.01  entropy=0.150  model expected '\\n' p=0.991
    token 31  'Where' S2=15.75  entropy=0.087  model expected '\\n' p=0.995
Neither line is a refrain.

MECHANISM
---------
Poems are stored with blank lines between stanzas, i.e. '\\n\\n'. GPT-2 emits
these as two separate '\\n' tokens. Once the model has seen a few stanzas, it
learns the poem's stanza period and becomes near-certain that the token after
a line-ending '\\n' is a SECOND '\\n' (the blank line). Entropy collapses toward
zero. When the poem instead continues with a word — which happens at every
line head that is NOT a stanza break — surprisal is enormous and

    S2 = surprisal - entropy

explodes. The spike measures the model's confidence in the *layout*, not the
poet's lexical choice.

WHY IT CONFOUNDS REPETITION STUDIES
-----------------------------------
A refrain's 2nd occurrence is necessarily LATER in the poem than its 1st. By
then the stanza rhythm is better established, so p('\\n') is higher and the
artifact is larger. Any "surprise grows on repetition" result is therefore
partly, or wholly, an artifact of position.

TESTS
-----
T1 Do line-head spikes track STANZA-BREAK CONFIDENCE rather than repetition?
   Split line-head tokens by the model's p('\\n') and compare S₂.
T2 Does line-head S₂ rise with position in poem for ALL lines, not just
   refrains? If so, the "refrain return" effect dissolves into position.
T3 Are stanza'd poems (blank lines present) affected more than unstanza'd
   poems (no blank lines)? The artifact requires a stanza pattern to learn.
T4 With artifact tokens excluded, does any refrain effect survive?
"""

import json
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "stanza_break_artifact.json")

# A line-head token is "artifact-contaminated" when the model was this sure
# that a newline (i.e. a blank line / stanza break) came next instead.
ARTIFACT_P = 0.90


def newline_prob(tok):
    """Model's probability mass on a newline continuation at this position."""
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def line_heads(tokens):
    """
    Yield (index, is_after_blank_line) for every token that begins a line,
    excluding position 0 (the BOS position has its own known artifact).
    """
    for i in range(1, len(tokens)):
        prev = tokens[i - 1]["token"]
        cur = tokens[i]["token"]
        if "\n" in prev and "\n" not in cur:
            after_blank = i >= 2 and "\n" in tokens[i - 2]["token"]
            yield i, after_blank


def poem_lines(tokens):
    """(normalised_text, start_idx, end_idx) for lines of >=2 words."""
    out, cur, start = [], [], 0
    for i, t in enumerate(tokens):
        if "\n" in t["token"]:
            if cur:
                out.append(("".join(cur).strip().lower(), start, i))
            cur, start = [], i + 1
        else:
            cur.append(t["token"])
    if cur:
        out.append(("".join(cur).strip().lower(), start, len(tokens)))
    return [ln for ln in out if len(ln[0].split()) >= 2]


def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    heads = []              # every line-head token in the corpus
    for entry in corpus:
        meta = entry["metadata"]
        toks = entry["tokens"]
        n = len(toks)
        if n < 20:
            continue
        has_stanzas = any(
            "\n" in toks[i]["token"] and "\n" in toks[i + 1]["token"]
            for i in range(n - 1)
        )
        # which lines repeat?
        rep_starts = {}
        by_text = defaultdict(list)
        for txt, s, _ in poem_lines(toks):
            by_text[txt].append(s)
        for positions in by_text.values():
            if len(positions) >= 2:
                for occ, s in enumerate(sorted(positions), start=1):
                    rep_starts[s] = occ

        for i, after_blank in line_heads(toks):
            t = toks[i]
            heads.append({
                "era": meta["era"],
                "title": meta["title"],
                "author": meta["author"],
                "s2": t["s2"],
                "surprisal": t["surprisal"],
                "entropy": t["entropy"],
                "p_newline": newline_prob(t),
                "rel_pos": i / n,
                "after_blank": after_blank,
                "has_stanzas": has_stanzas,
                "occ": rep_starts.get(i, 0),   # 0 = not a repeated line
            })

    print("=" * 76)
    print("THE STANZA-BREAK ARTIFACT IN LINE-HEAD S2")
    print(f"{len(heads)} line-head tokens across {len(corpus)} texts")
    print("=" * 76)

    # ── T1: does line-head S2 track the model's newline confidence? ──
    print("\n--- T1: LINE-HEAD S2 BY MODEL'S P(newline) AT THAT POSITION ---")
    print(f"{'p(newline) bucket':<22}{'n':>7}{'surprisal':>11}{'entropy':>10}{'S2':>9}")
    buckets = [(0.0, 0.1), (0.1, 0.3), (0.3, 0.6), (0.6, 0.9), (0.9, 0.99), (0.99, 1.01)]
    for lo, hi in buckets:
        g = [h for h in heads if lo <= h["p_newline"] < hi]
        if not g:
            continue
        label = f"{lo:.2f}-{hi if hi <= 1 else 1.0:.2f}"
        print(f"{label:<22}{len(g):>7}"
              f"{statistics.mean(h['surprisal'] for h in g):>11.3f}"
              f"{statistics.mean(h['entropy'] for h in g):>10.3f}"
              f"{statistics.mean(h['s2'] for h in g):>9.3f}")

    contaminated = [h for h in heads if h["p_newline"] >= ARTIFACT_P]
    clean = [h for h in heads if h["p_newline"] < ARTIFACT_P]
    print(f"\n  contaminated (p>={ARTIFACT_P}): n={len(contaminated):<6} "
          f"({len(contaminated)/len(heads):.1%} of line heads)  "
          f"mean S2={statistics.mean(h['s2'] for h in contaminated):.3f}")
    print(f"  clean                    : n={len(clean):<6} "
          f"({len(clean)/len(heads):.1%})  "
          f"mean S2={statistics.mean(h['s2'] for h in clean):.3f}")

    # ── T2: does line-head S2 rise with position for ALL lines? ──
    print("\n--- T2: LINE-HEAD S2 BY POSITION IN POEM (all lines, not just refrains) ---")
    print(f"{'position':<14}{'n':>7}{'p(nl)':>9}{'S2 all':>10}{'S2 clean':>11}")
    for lo, hi in [(0, .2), (.2, .4), (.4, .6), (.6, .8), (.8, 1.01)]:
        g = [h for h in heads if lo <= h["rel_pos"] < hi]
        gc = [h for h in g if h["p_newline"] < ARTIFACT_P]
        if not g:
            continue
        print(f"{f'{lo:.0%}-{hi:.0%}':<14}{len(g):>7}"
              f"{statistics.mean(h['p_newline'] for h in g):>9.3f}"
              f"{statistics.mean(h['s2'] for h in g):>10.3f}"
              f"{statistics.mean(h['s2'] for h in gc):>11.3f}")

    # ── T3: stanza'd vs unstanza'd poems ──
    print("\n--- T3: POEMS WITH BLANK-LINE STANZA BREAKS vs WITHOUT ---")
    print(f"{'group':<26}{'n heads':>9}{'p(nl)':>9}{'S2':>9}{'%contam':>10}")
    for label, flag in (("has stanza breaks", True), ("no stanza breaks", False)):
        g = [h for h in heads if h["has_stanzas"] is flag]
        if not g:
            continue
        c = sum(1 for h in g if h["p_newline"] >= ARTIFACT_P)
        print(f"{label:<26}{len(g):>9}"
              f"{statistics.mean(h['p_newline'] for h in g):>9.3f}"
              f"{statistics.mean(h['s2'] for h in g):>9.3f}{c/len(g):>10.1%}")

    # ── T4: refrain effect before and after removing the artifact ──
    print("\n--- T4: REPEATED-LINE HEADS BY OCCURRENCE, RAW vs ARTIFACT-FREE ---")
    print(f"{'occurrence':<14}{'n raw':>7}{'S2 raw':>10}{'n clean':>9}{'S2 clean':>11}")
    for occ in (1, 2, 3):
        g = [h for h in heads if h["occ"] == occ]
        gc = [h for h in g if h["p_newline"] < ARTIFACT_P]
        if not g:
            continue
        clean_s2 = f"{statistics.mean(h['s2'] for h in gc):.3f}" if gc else "—"
        print(f"{'#' + str(occ):<14}{len(g):>7}"
              f"{statistics.mean(h['s2'] for h in g):>10.3f}"
              f"{len(gc):>9}{clean_s2:>11}")

    nonrep = [h for h in heads if h["occ"] == 0]
    nonrep_c = [h for h in nonrep if h["p_newline"] < ARTIFACT_P]
    print(f"{'non-repeated':<14}{len(nonrep):>7}"
          f"{statistics.mean(h['s2'] for h in nonrep):>10.3f}"
          f"{len(nonrep_c):>9}{statistics.mean(h['s2'] for h in nonrep_c):>11.3f}")

    # ── Corpus-level impact ──
    print("\n--- IMPACT: HOW MUCH OF REPORTED LINE-HEAD S2 IS ARTIFACT? ---")
    all_s2 = statistics.mean(h["s2"] for h in heads)
    clean_s2 = statistics.mean(h["s2"] for h in clean)
    print(f"  reported line-head S2 (all)      : {all_s2:.3f}")
    print(f"  artifact-free line-head S2       : {clean_s2:.3f}")
    print(f"  inflation attributable to artifact: {all_s2 - clean_s2:+.3f} bits "
          f"({(all_s2 - clean_s2) / all_s2:.0%} of the reported value)")

    print("\n--- ERAS MOST AFFECTED (by % of line heads contaminated) ---")
    by_era = defaultdict(list)
    for h in heads:
        by_era[h["era"]].append(h)
    era_rows = []
    for era, g in by_era.items():
        if len(g) < 20:
            continue
        c = [h for h in g if h["p_newline"] >= ARTIFACT_P]
        cl = [h for h in g if h["p_newline"] < ARTIFACT_P]
        era_rows.append((era, len(g), len(c) / len(g),
                         statistics.mean(h["s2"] for h in g),
                         statistics.mean(h["s2"] for h in cl) if cl else float("nan")))
    era_rows.sort(key=lambda r: -r[2])
    print(f"{'era':<22}{'n':>6}{'%contam':>10}{'S2 raw':>10}{'S2 clean':>11}{'delta':>9}")
    for era, n, pct, raw, cl in era_rows:
        print(f"{era:<22}{n:>6}{pct:>10.1%}{raw:>10.3f}{cl:>11.3f}{raw - cl:>+9.3f}")

    with open(OUT_JSON, "w") as f:
        json.dump({
            "artifact_threshold_p_newline": ARTIFACT_P,
            "n_line_heads": len(heads),
            "n_contaminated": len(contaminated),
            "line_head_s2_raw": round(all_s2, 4),
            "line_head_s2_clean": round(clean_s2, 4),
            "by_era": [
                {"era": e, "n": n, "pct_contaminated": round(p, 4),
                 "s2_raw": round(r, 4), "s2_clean": round(c, 4)}
                for e, n, p, r, c in era_rows
            ],
        }, f, indent=2)
    print(f"\nSaved: {OUT_JSON}")


if __name__ == "__main__":
    main()
