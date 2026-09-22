"""
Kurtosis and Crest Factor of S₂ Series: Testing the Impulse Account

The spectral null result (spectral_refrain_null.md) showed that fixed-form refrain
poems do not concentrate spectral power at their refrain frequency. The proposed
interpretation: a refrain produces S₂ *impulses* — sharp spikes at the moment of
return — not smooth oscillations.

A delta function (pure impulse) has a flat power spectrum. If repetition in poetry
works like a drumbeat, it should produce:

  1. HIGH KURTOSIS  — the distribution is peaky / heavy-tailed (impulse → extreme
     values occur rarely but are very large; normal distribution = 0 excess kurtosis)
  2. HIGH CREST FACTOR — a few large peaks dominate the RMS, quantifying how "spiky"
     the signal is
  3. FLAT SPECTRUM — which the prior result already found for refrain poems

The first two metrics are TIME-DOMAIN complements of the frequency-domain flatness
already measured. The joint prediction is specific: refrain poems should show all
three together. High kurtosis with CONCENTRATED spectra would be different (that would
suggest wave-like periodic structure). Flat spectra alone could just be noise.

Groups compared:
  A. fixed_form era poems (villanelles, ballade, rondeau, sestina) — n=8
  B. Poems with ≥2 verbatim repeated lines (verbatim detection) — varies
  C. All other poetry — baseline

All metrics computed artifact-free: positions where p(newline) ≥ 0.9 are replaced by
the poem's clean median before computing statistics. This follows the methodology
established in stanza_break_artifact.md.
"""

import json
import math
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "impulse_account.json")

ARTIFACT_P = 0.90
MIN_TOKENS = 30  # skip very short poems


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def deartifacted(tokens):
    """Replace artifact positions with poem's clean median; return list of floats."""
    clean = [t["s2"] for t in tokens if newline_prob(t) < ARTIFACT_P]
    if not clean:
        return [t["s2"] for t in tokens]
    med = statistics.median(clean)
    return [med if newline_prob(t) >= ARTIFACT_P else t["s2"] for t in tokens]


def kurtosis(series):
    """Excess kurtosis = E[(x-μ)^4]/σ^4 − 3. Normal distribution → 0."""
    n = len(series)
    if n < 4:
        return float("nan")
    mu = sum(series) / n
    sigma2 = sum((x - mu) ** 2 for x in series) / n
    if sigma2 < 1e-12:
        return float("nan")
    sigma4 = sigma2 ** 2
    m4 = sum((x - mu) ** 4 for x in series) / n
    return m4 / sigma4 - 3.0


def crest_factor(series):
    """max(|x|) / RMS(x) — large values indicate impulsive behaviour."""
    if not series:
        return float("nan")
    rms = math.sqrt(sum(x * x for x in series) / len(series))
    if rms < 1e-12:
        return float("nan")
    return max(abs(x) for x in series) / rms


def spectral_flatness(series):
    """Geometric mean / arithmetic mean of the power spectrum (via direct DFT).
    Returns NaN if series is too short or degenerate."""
    n = len(series)
    if n < 8:
        return float("nan")
    mu = sum(series) / n
    x = [v - mu for v in series]
    powers = []
    for k in range(1, n // 2 + 1):
        re = im = 0.0
        w = 2.0 * math.pi * k / n
        for t, val in enumerate(x):
            re += val * math.cos(w * t)
            im -= val * math.sin(w * t)
        p = (re * re + im * im) / n
        if p > 1e-15:
            powers.append(p)
    if len(powers) < 2:
        return float("nan")
    log_sum = sum(math.log(p) for p in powers)
    arith = sum(powers) / len(powers)
    geo = math.exp(log_sum / len(powers))
    return geo / arith


def verbatim_repeats(tokens):
    """Count poems' worth of repeated lines.
    Returns the number of lines that appear ≥2 times verbatim."""
    text = "".join(t["token"] for t in tokens)
    lines = [ln.strip() for ln in text.split("\n") if len(ln.strip()) > 8]
    from collections import Counter
    counts = Counter(lines)
    return sum(1 for v in counts.values() if v >= 2)


def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    rows = []
    for entry in corpus:
        tokens = entry["tokens"]
        if len(tokens) < MIN_TOKENS:
            continue
        meta = entry["metadata"]
        series = deartifacted(tokens)
        n_art = sum(1 for t in tokens if newline_prob(t) >= ARTIFACT_P)
        pct_art = n_art / len(tokens)
        n_repeats = verbatim_repeats(tokens)
        rows.append({
            "title":       meta["title"],
            "author":      meta["author"],
            "era":         meta["era"],
            "n_tokens":    len(tokens),
            "pct_artifact": pct_art,
            "kurtosis":    kurtosis(series),
            "crest_factor": crest_factor(series),
            "flatness":    spectral_flatness(series),
            "n_repeats":   n_repeats,
        })

    def safe_mean(lst):
        finite = [v for v in lst if v == v]  # filter nan
        return statistics.mean(finite) if finite else float("nan")

    # ── Group classification ──
    fixed = [r for r in rows if r["era"] == "fixed_form"]
    repeaters = [r for r in rows if r["n_repeats"] >= 2 and r["era"] != "fixed_form"]
    baseline_poetry = [r for r in rows
                       if r["n_repeats"] < 2
                       and r["era"] not in ("fixed_form", "control")]
    prose = [r for r in rows if r["era"] == "control"]

    print("=" * 74)
    print("IMPULSE ACCOUNT TEST: KURTOSIS AND CREST FACTOR OF S₂ SERIES")
    print("=" * 74)
    print()

    groups = [
        ("fixed_form (A)", fixed),
        ("repeaters (B)", repeaters),
        ("baseline poetry (C)", baseline_poetry),
        ("prose control (D)", prose),
    ]

    print(f"{'Group':<25}{'n':>4}{'kurtosis':>11}{'crest':>10}{'flatness':>11}")
    print("-" * 65)
    for label, grp in groups:
        if not grp:
            continue
        print(f"{label:<25}{len(grp):>4}"
              f"{safe_mean([r['kurtosis'] for r in grp]):>11.3f}"
              f"{safe_mean([r['crest_factor'] for r in grp]):>10.3f}"
              f"{safe_mean([r['flatness'] for r in grp]):>11.4f}")

    print()
    print("── Joint signature check (refrain = impulse → high kurtosis + flat spectrum) ──")
    print()
    print(f"{'Poem':<40}{'era':<14}{'kurtosis':>10}{'crest':>10}{'flatness':>10}{'reps':>5}")
    print("-" * 95)
    for r in sorted(fixed + repeaters, key=lambda r: -r["kurtosis"]):
        print(f"{r['title'][:39]:<40}{r['era'][:13]:<14}"
              f"{r['kurtosis']:>10.3f}{r['crest_factor']:>10.3f}"
              f"{r['flatness']:>10.4f}{r['n_repeats']:>5}")

    print()
    print("── Baseline sample (highest kurtosis from non-refrain poetry) ──")
    print()
    top_base = sorted(baseline_poetry, key=lambda r: -r["kurtosis"])[:10]
    for r in top_base:
        print(f"{r['title'][:39]:<40}{r['era'][:13]:<14}"
              f"{r['kurtosis']:>10.3f}{r['crest_factor']:>10.3f}"
              f"{r['flatness']:>10.4f}")

    print()
    print("── Kurtosis distribution summary ──")
    all_k = [(r["kurtosis"], r["era"]) for r in rows if r["kurtosis"] == r["kurtosis"]]
    all_k.sort()
    n = len(all_k)
    median_k = all_k[n // 2][0]
    p90_k = all_k[int(n * 0.9)][0]
    p95_k = all_k[int(n * 0.95)][0]
    print(f"  Corpus: n={n}, median={median_k:.3f}, p90={p90_k:.3f}, p95={p95_k:.3f}")
    print(f"  Fixed-form median kurtosis: {statistics.median([r['kurtosis'] for r in fixed if r['kurtosis'] == r['kurtosis']]):.3f}")
    if repeaters:
        rk = [r["kurtosis"] for r in repeaters if r["kurtosis"] == r["kurtosis"]]
        if rk:
            print(f"  Repeaters  median kurtosis: {statistics.median(rk):.3f}")
    bk = [r["kurtosis"] for r in baseline_poetry if r["kurtosis"] == r["kurtosis"]]
    if bk:
        print(f"  Baseline   median kurtosis: {statistics.median(bk):.3f}")

    # ── Save results ──
    with open(OUT_JSON, "w") as f:
        json.dump({
            "n_poems": len(rows),
            "groups": {
                label: {
                    "n": len(grp),
                    "kurtosis_mean": round(safe_mean([r["kurtosis"] for r in grp]), 4),
                    "crest_mean":    round(safe_mean([r["crest_factor"] for r in grp]), 4),
                    "flatness_mean": round(safe_mean([r["flatness"] for r in grp]), 4),
                } for label, grp in groups if grp
            },
            "per_poem": sorted(rows, key=lambda r: -r["kurtosis"]),
        }, f, indent=2)
    print(f"\nSaved: {OUT_JSON}")


if __name__ == "__main__":
    main()
