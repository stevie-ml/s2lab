"""
Spectral Analysis of the S₂ Series: Does Structural Repetition Have a Frequency?

Prior work in this lab measured the S₂ series in the *time domain*:
  - s2_spikiness.py     → variance (how big are the swings)
  - s2_momentum.py      → autocorrelation at lags 1, 2, 5 (local alternation)
  - surprise_decay.py   → what happens 1-10 tokens after a spike

All three are blind to *long-period* structure. Lag-1 autocorrelation cannot
tell you that a poem returns to the same state every 40 tokens. The natural
tool for that is the frequency domain.

This experiment takes the discrete Fourier transform of each poem's S₂ series
and asks three questions:

  Q1 SPECTRAL FLATNESS. Is the S₂ series white noise (flat spectrum, power
     spread evenly across all frequencies) or is it structured (power
     concentrated at a few frequencies)? Measured by spectral flatness =
     geometric mean of the power spectrum / arithmetic mean. 1.0 = pure
     white noise; →0 = one dominant periodicity.

  Q2 THE REFRAIN FREQUENCY. Fixed forms (villanelle, ballade, rondeau,
     sestina) impose a refrain that returns at a *known* interval. If the
     model genuinely re-predicts the refrain on each return, S₂ should carry
     measurable power at that refrain period. We compute each poem's
     dominant period and compare it to the observed line-repeat period.

  Q3 DOES REPETITION SHOW UP AT ALL? The alternative hypothesis is null:
     a returning refrain becomes *more* predictable each time (the model has
     seen it), so S₂ collapses toward a flat low value rather than oscillating.
     Under that account, refrain forms would be spectrally FLATTER than free
     verse, not peakier.

Hypotheses:
  H1: fixed_form poems have lower spectral flatness than free verse
      (structural repetition → concentrated spectral power)
  H2: the dominant period of a villanelle aligns with its refrain interval
  H3: prose control has the flattest spectrum of all (no imposed structure)
"""

import json
import math
import os
import statistics
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "spectral_refrain.json")

MIN_TOKENS = 40  # need enough samples for a meaningful spectrum

# Positions where GPT-2 put >= this much mass on a newline continuation are
# stanza-break artifacts, not poetic choices (see findings/stanza_break_artifact.md).
# Their S2 is fixed by layout, and they inject impulses that whiten the spectrum.
ARTIFACT_P = 0.90


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def deartifacted_s2(tokens):
    """
    S2 series with artifact positions replaced by the poem's clean median.
    Replacement (rather than deletion) keeps the series evenly sampled, which
    the DFT requires, while removing the layout impulses.
    """
    clean = [t["s2"] for t in tokens if newline_prob(t) < ARTIFACT_P]
    if not clean:
        return None
    med = statistics.median(clean)
    return [med if newline_prob(t) >= ARTIFACT_P else t["s2"] for t in tokens]


# ─── DFT ────────────────────────────────────────────────────────────────────

def power_spectrum(series):
    """
    Real DFT power spectrum of a mean-removed series, via direct computation.
    Returns list of (period_in_tokens, power) for frequency bins 1..N/2.
    Bin 0 (DC) is dropped: we removed the mean, and the poem's average S2 is
    already reported everywhere else in this lab.
    """
    n = len(series)
    mean = statistics.mean(series)
    x = [v - mean for v in series]

    out = []
    for k in range(1, n // 2 + 1):
        re = im = 0.0
        w = 2.0 * math.pi * k / n
        for t, val in enumerate(x):
            re += val * math.cos(w * t)
            im -= val * math.sin(w * t)
        power = (re * re + im * im) / n
        out.append((n / k, power))  # period = n/k tokens per cycle
    return out


def spectral_flatness(powers):
    """
    Geometric mean / arithmetic mean of the power spectrum (Wiener entropy).
    1.0 → white noise (all frequencies equal). →0 → one frequency dominates.
    """
    pos = [p for p in powers if p > 1e-12]
    if len(pos) < 2:
        return float("nan")
    log_mean = sum(math.log(p) for p in pos) / len(pos)
    geo = math.exp(log_mean)
    arith = sum(pos) / len(pos)
    return geo / arith if arith > 0 else float("nan")


def spectral_entropy(powers):
    """
    Shannon entropy of the normalised power spectrum, in bits, normalised to
    [0,1] by dividing by log2(n_bins). 1.0 = maximally spread (white noise).
    """
    tot = sum(powers)
    if tot <= 0 or len(powers) < 2:
        return float("nan")
    p = [v / tot for v in powers if v > 0]
    h = -sum(v * math.log2(v) for v in p)
    return h / math.log2(len(powers))


def dominant_period(spec):
    """Period (in tokens) of the highest-power frequency bin."""
    if not spec:
        return float("nan")
    return max(spec, key=lambda pair: pair[1])[0]


def peak_prominence(spec):
    """Max bin power / median bin power — how much the top peak stands out."""
    powers = [p for _, p in spec]
    if len(powers) < 3:
        return float("nan")
    med = statistics.median(powers)
    return max(powers) / med if med > 0 else float("nan")


# ─── REFRAIN DETECTION ──────────────────────────────────────────────────────

def split_lines(tokens):
    """
    Reconstruct lines from the token stream.
    Returns list of (normalised_text, start_index, end_index_exclusive).
    """
    lines = []
    cur, start = [], 0
    for i, t in enumerate(tokens):
        if "\n" in t["token"]:
            if cur:
                lines.append(("".join(cur).strip().lower(), start, i))
            cur, start = [], i + 1
        else:
            cur.append(t["token"])
    if cur:
        lines.append(("".join(cur).strip().lower(), start, len(tokens)))
    return [ln for ln in lines if len(ln[0].split()) >= 2]


def refrain_period_tokens(tokens):
    """
    Detect structural repetition empirically: find lines that repeat verbatim
    and return the mean token-distance between consecutive occurrences. This
    is the poem's observed refrain interval, derived from the data rather
    than assumed from the form label.
    """
    by_text = defaultdict(list)
    for txt, start, _ in split_lines(tokens):
        by_text[txt].append(start)

    gaps = []
    for positions in by_text.values():
        if len(positions) >= 2:
            positions.sort()
            gaps += [positions[i + 1] - positions[i] for i in range(len(positions) - 1)]

    return (statistics.mean(gaps) if gaps else None), len(gaps)


def refrain_occurrence_s2(tokens):
    """
    THE MECHANISM TEST.

    For every line that appears more than once, record the mean S2 of that
    line on its 1st, 2nd, 3rd... occurrence.

    If a returning refrain is re-learned by the model, S2 should fall sharply
    on occurrence 2 and stay low. That would mean structural repetition
    *destroys* information rather than creating a periodic signal — and would
    explain a flat spectrum in the very forms built on repetition.

    Returns dict: occurrence_number -> list of per-line mean S2 values.
    """
    by_text = defaultdict(list)
    for txt, start, end in split_lines(tokens):
        by_text[txt].append((start, end))

    out = defaultdict(list)
    for positions in by_text.values():
        if len(positions) < 2:
            continue
        positions.sort()
        for occ, (start, end) in enumerate(positions, start=1):
            idx = range(start, end)
            if start >= end:
                continue
            out[occ].append({
                "s2": statistics.mean(tokens[i]["s2"] for i in idx),
                "surprisal": statistics.mean(tokens[i]["surprisal"] for i in idx),
                "entropy": statistics.mean(tokens[i]["entropy"] for i in idx),
                # first token of the line: the moment the refrain RE-ENTERS
                "head_s2": tokens[start]["s2"],
                "head_surprisal": tokens[start]["surprisal"],
                "head_entropy": tokens[start]["entropy"],
            })
    return out


# ─── MAIN ───────────────────────────────────────────────────────────────────

def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    rows = []
    occ_global = defaultdict(list)     # occurrence # -> mean S2 per repeated line
    occ_fixed = defaultdict(list)      # same, restricted to fixed_form poems

    for entry in corpus:
        meta = entry["metadata"]
        tokens = entry["tokens"]
        s2 = [t["s2"] for t in tokens]
        if len(s2) < MIN_TOKENS:
            continue

        for occ, vals in refrain_occurrence_s2(tokens).items():
            occ_global[occ] += vals
            if meta["era"] == "fixed_form":
                occ_fixed[occ] += vals

        spec = power_spectrum(s2)
        powers = [p for _, p in spec]
        rp, n_repeats = refrain_period_tokens(tokens)
        dom = dominant_period(spec)

        clean_series = deartifacted_s2(tokens)
        if clean_series:
            cspec = power_spectrum(clean_series)
            cflat = spectral_flatness([p for _, p in cspec])
            cdom = dominant_period(cspec)
        else:
            cflat = cdom = float("nan")

        rows.append({
            "flatness_clean": round(cflat, 4),
            "dom_period_clean": round(cdom, 2),
            "title": meta["title"],
            "author": meta["author"],
            "era": meta["era"],
            "year": meta.get("year"),
            "n_tokens": len(s2),
            "avg_s2": round(statistics.mean(s2), 4),
            "std_s2": round(statistics.stdev(s2), 4),
            "flatness": round(spectral_flatness(powers), 4),
            "spec_entropy": round(spectral_entropy(powers), 4),
            "dom_period": round(dom, 2),
            "peak_prom": round(peak_prominence(spec), 3),
            "refrain_period": round(rp, 2) if rp else None,
            "n_repeated_lines": n_repeats,
            "period_ratio": round(dom / rp, 3) if rp else None,
        })

    rows.sort(key=lambda r: r["flatness"])

    # ─ By era ─
    by_era = defaultdict(list)
    for r in rows:
        by_era[r["era"]].append(r)

    era_stats = []
    for era, rs in by_era.items():
        if len(rs) < 2:
            continue
        era_stats.append({
            "era": era,
            "n": len(rs),
            "flatness_clean": statistics.mean(r["flatness_clean"] for r in rs),
            "flatness": statistics.mean(r["flatness"] for r in rs),
            "spec_entropy": statistics.mean(r["spec_entropy"] for r in rs),
            "peak_prom": statistics.mean(r["peak_prom"] for r in rs),
            "avg_s2": statistics.mean(r["avg_s2"] for r in rs),
            "std_s2": statistics.mean(r["std_s2"] for r in rs),
            "n_tokens": statistics.mean(r["n_tokens"] for r in rs),
        })
    era_stats.sort(key=lambda e: e["flatness"])

    # ─ Repeaters vs non-repeaters ─
    repeaters = [r for r in rows if r["n_repeated_lines"] >= 2]
    singles = [r for r in rows if r["n_repeated_lines"] == 0]

    print("=" * 78)
    print("SPECTRAL ANALYSIS OF THE S2 SERIES")
    print(f"{len(rows)} texts with >= {MIN_TOKENS} tokens")
    print("=" * 78)

    print("\n--- SPECTRAL FLATNESS BY ERA (low = periodic, high = white noise) ---")
    print(f"{'era':<22}{'n':>4}{'flat_raw':>10}{'flat_clean':>12}{'spec_H':>9}"
          f"{'peak_prom':>11}{'avg_s2':>9}{'len':>7}")
    for e in sorted(era_stats, key=lambda e: e["flatness_clean"]):
        print(f"{e['era']:<22}{e['n']:>4}{e['flatness']:>10.4f}{e['flatness_clean']:>12.4f}"
              f"{e['spec_entropy']:>9.4f}{e['peak_prom']:>11.2f}{e['avg_s2']:>9.3f}"
              f"{e['n_tokens']:>7.0f}")

    print("\n--- POEMS WITH REPEATED LINES vs WITHOUT ---")
    for label, group in (("repeated lines (>=2 returns)", repeaters),
                         ("no repeated lines", singles)):
        if not group:
            continue
        print(f"{label:<32} n={len(group):<4} "
              f"flat_raw={statistics.mean(r['flatness'] for r in group):.4f}  "
              f"flat_clean={statistics.mean(r['flatness_clean'] for r in group):.4f}  "
              f"peak_prom={statistics.mean(r['peak_prom'] for r in group):.2f}  "
              f"std_s2={statistics.mean(r['std_s2'] for r in group):.3f}")

    print("\n--- FIXED-FORM POEMS: DOMINANT PERIOD vs OBSERVED REFRAIN PERIOD ---")
    print(f"{'title':<44}{'len':>5}{'dom_per':>9}{'refr_per':>10}{'ratio':>8}{'flat':>8}")
    for r in sorted((r for r in rows if r["era"] == "fixed_form"),
                    key=lambda r: r["flatness"]):
        rp = f"{r['refrain_period']:.1f}" if r["refrain_period"] else "—"
        ratio = f"{r['period_ratio']:.2f}" if r["period_ratio"] else "—"
        print(f"{r['title'][:43]:<44}{r['n_tokens']:>5}{r['dom_period']:>9.1f}"
              f"{rp:>10}{ratio:>8}{r['flatness']:>8.4f}")

    print("\n--- 12 MOST PERIODIC TEXTS (lowest spectral flatness) ---")
    print(f"{'title':<40}{'author':<22}{'era':<16}{'flat':>8}{'dom_per':>9}")
    for r in rows[:12]:
        print(f"{r['title'][:39]:<40}{r['author'][:21]:<22}{r['era'][:15]:<16}"
              f"{r['flatness']:>8.4f}{r['dom_period']:>9.1f}")

    print("\n--- 12 MOST NOISE-LIKE TEXTS (highest spectral flatness) ---")
    for r in rows[-12:]:
        print(f"{r['title'][:39]:<40}{r['author'][:21]:<22}{r['era'][:15]:<16}"
              f"{r['flatness']:>8.4f}{r['dom_period']:>9.1f}")

    print("\n--- MECHANISM: A REPEATED LINE, DECOMPOSED, BY OCCURRENCE NUMBER ---")
    print("whole line:")
    print(f"{'group':<18}{'n':>5}{'surprisal':>11}{'entropy':>10}{'S2':>9}{'dS2':>9}")

    def occ_table(label, store):
        base = statistics.mean(d["s2"] for d in store[1]) if store.get(1) else None
        for occ in sorted(store):
            ds = store[occ]
            if len(ds) < 2:
                continue
            s2m = statistics.mean(d["s2"] for d in ds)
            delta = f"{s2m - base:+.3f}" if base is not None else "—"
            print(f"{label + ' #' + str(occ):<18}{len(ds):>5}"
                  f"{statistics.mean(d['surprisal'] for d in ds):>11.3f}"
                  f"{statistics.mean(d['entropy'] for d in ds):>10.3f}"
                  f"{s2m:>9.3f}{delta:>9}")

    occ_table("all poems", occ_global)
    if occ_fixed:
        occ_table("fixed_form", occ_fixed)

    print("\nline-head token only (the moment the refrain re-enters):")
    print(f"{'group':<18}{'n':>5}{'surprisal':>11}{'entropy':>10}{'S2':>9}{'dS2':>9}")

    def head_table(label, store):
        base = statistics.mean(d["head_s2"] for d in store[1]) if store.get(1) else None
        for occ in sorted(store):
            ds = store[occ]
            if len(ds) < 2:
                continue
            s2m = statistics.mean(d["head_s2"] for d in ds)
            delta = f"{s2m - base:+.3f}" if base is not None else "—"
            print(f"{label + ' #' + str(occ):<18}{len(ds):>5}"
                  f"{statistics.mean(d['head_surprisal'] for d in ds):>11.3f}"
                  f"{statistics.mean(d['head_entropy'] for d in ds):>10.3f}"
                  f"{s2m:>9.3f}{delta:>9}")

    head_table("all poems", occ_global)
    if occ_fixed:
        head_table("fixed_form", occ_fixed)

    # ─ Does length confound flatness? ─
    print("\n--- FLATNESS vs POEM LENGTH (confound check) ---")
    buckets = [(40, 60), (60, 90), (90, 140), (140, 220), (220, 10000)]
    for lo, hi in buckets:
        g = [r for r in rows if lo <= r["n_tokens"] < hi]
        if len(g) < 3:
            continue
        print(f"  {lo:>4}-{hi if hi < 10000 else '+':<5} n={len(g):<4} "
              f"flatness={statistics.mean(r['flatness'] for r in g):.4f}  "
              f"spec_H={statistics.mean(r['spec_entropy'] for r in g):.4f}")

    with open(OUT_JSON, "w") as f:
        json.dump({
            "min_tokens": MIN_TOKENS,
            "n_texts": len(rows),
            "by_era": era_stats,
            "refrain_occurrence": {
                label: {
                    str(k): {
                        "n": len(v),
                        "surprisal": round(statistics.mean(d["surprisal"] for d in v), 4),
                        "entropy": round(statistics.mean(d["entropy"] for d in v), 4),
                        "s2": round(statistics.mean(d["s2"] for d in v), 4),
                        "head_surprisal": round(statistics.mean(d["head_surprisal"] for d in v), 4),
                        "head_entropy": round(statistics.mean(d["head_entropy"] for d in v), 4),
                        "head_s2": round(statistics.mean(d["head_s2"] for d in v), 4),
                    }
                    for k, v in sorted(store.items()) if v
                }
                for label, store in (("all", occ_global), ("fixed_form", occ_fixed))
            },
            "texts": rows,
        }, f, indent=2)
    print(f"\nSaved: {OUT_JSON}")


if __name__ == "__main__":
    main()
