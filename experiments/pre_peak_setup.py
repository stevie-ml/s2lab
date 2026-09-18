"""
Pre-Peak Setup: What happens in the tokens LEADING UP to an S₂ spike?

Companion to surprise_decay.py (which studies post-peak dynamics).

Central question:
    Before a poet strikes with an unexpected word, do they systematically
    prime the model into confidence? That is — is a spike preceded by a
    stretch of LOW entropy (model complacent) and LOW/negative S₂ (poet
    conforming)?  This would be the temporal fingerprint of the "confidence
    trap" mechanism previously described only at a single-token level.

Metrics (aggregated across all spikes, per era):
  - Pre-peak entropy curve      : mean H at lag k = -8..-1
  - Pre-peak surprisal curve    : mean surprisal at lag k = -8..-1
  - Pre-peak S₂ curve           : mean S₂ at lag k = -8..-1
  - "Trap depth"                : (mean entropy at lags -3..-1) minus (poem's
                                  mean entropy).  Negative means the model
                                  was systematically MORE confident just
                                  before the spike than baseline.
  - "Lull depth"                : (mean S₂ at lags -3..-1) minus (poem's
                                  mean S₂).  Negative means the poet was
                                  systematically MORE conventional just
                                  before the spike.

If either quantity is significantly negative across a movement, we have
evidence that poets set up their surprises by first performing conformity.

No new model inference — works entirely from corpus_results.json.
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

SPIKE_THRESHOLD = 3.0  # S₂ units, matches surprise_decay.py
LAGS = list(range(-8, 0))  # k = -8, -7, ..., -1  (tokens BEFORE the peak)


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def find_spikes(tokens, threshold=SPIKE_THRESHOLD):
    """Return list of (index, s2) for tokens with S2 >= threshold."""
    return [(i, t["s2"]) for i, t in enumerate(tokens) if t["s2"] >= threshold]


def pre_peak_trajectory(tokens, spike_idx, lags=LAGS):
    """For a given peak, return dict of {lag: (entropy, surprisal, s2)}.
       Only includes lags where the pre-peak token exists inside the poem
       (i.e. spike_idx + k >= 0)."""
    traj = {}
    for k in lags:
        j = spike_idx + k
        if j < 0:
            continue
        t = tokens[j]
        traj[k] = (t["entropy"], t["surprisal"], t["s2"])
    return traj


def analyze_poem(poem):
    """Return per-poem stats:
         spikes       : list of spike indices
         pre_curves   : list of trajectory dicts (one per spike)
         mean_entropy : baseline over the whole poem
         mean_s2      : baseline over the whole poem
         era          : era label
    """
    tokens = poem["tokens"]
    spikes = find_spikes(tokens)
    pre = [pre_peak_trajectory(tokens, i) for i, _ in spikes]
    if not tokens:
        return None
    mean_h  = statistics.mean(t["entropy"]   for t in tokens)
    mean_s  = statistics.mean(t["surprisal"] for t in tokens)
    mean_s2 = statistics.mean(t["s2"]        for t in tokens)
    return {
        "era":     poem["metadata"].get("era", ""),
        "author":  poem["metadata"].get("author", ""),
        "title":   poem["metadata"].get("title", ""),
        "spikes":  spikes,
        "pre":     pre,
        "mean_h":  mean_h,
        "mean_s":  mean_s,
        "mean_s2": mean_s2,
        "n":       len(tokens),
    }


def aggregate_by_era(poem_stats):
    """Aggregate pre-peak curves grouped by era."""
    by_era = defaultdict(lambda: {
        "h_lag":  defaultdict(list),  # lag → [entropies across spikes]
        "s_lag":  defaultdict(list),
        "s2_lag": defaultdict(list),
        "trap_depth":  [],   # entropy(-3..-1 mean) - poem's mean_h
        "lull_depth":  [],   # s2(-3..-1 mean)      - poem's mean_s2
        "n_spikes":    0,
        "n_poems":     0,
    })
    for ps in poem_stats:
        if ps is None or not ps["pre"]:
            continue
        e = ps["era"]
        by_era[e]["n_poems"] += 1
        for traj in ps["pre"]:
            by_era[e]["n_spikes"] += 1
            for k, (h, s, s2) in traj.items():
                by_era[e]["h_lag"][k].append(h)
                by_era[e]["s_lag"][k].append(s)
                by_era[e]["s2_lag"][k].append(s2)
            # trap/lull depth over lags -3..-1
            close_h  = [h  for k, (h, s, s2) in traj.items() if k >= -3]
            close_s2 = [s2 for k, (h, s, s2) in traj.items() if k >= -3]
            if close_h:
                by_era[e]["trap_depth"].append(
                    statistics.mean(close_h) - ps["mean_h"]
                )
            if close_s2:
                by_era[e]["lull_depth"].append(
                    statistics.mean(close_s2) - ps["mean_s2"]
                )
    return by_era


def summarize(by_era):
    """Return a summary table sortable by lull_depth."""
    rows = []
    for era, d in by_era.items():
        if d["n_spikes"] < 5:  # skip eras with too little data
            continue
        row = {
            "era":        era,
            "n_poems":    d["n_poems"],
            "n_spikes":   d["n_spikes"],
            "trap_depth": statistics.mean(d["trap_depth"]) if d["trap_depth"] else None,
            "lull_depth": statistics.mean(d["lull_depth"]) if d["lull_depth"] else None,
        }
        # entropy trajectory (lag → mean H)
        row["h_curve"]  = {k: statistics.mean(v) for k, v in sorted(d["h_lag"].items())}
        row["s2_curve"] = {k: statistics.mean(v) for k, v in sorted(d["s2_lag"].items())}
        row["s_curve"]  = {k: statistics.mean(v) for k, v in sorted(d["s_lag"].items())}
        rows.append(row)
    rows.sort(key=lambda r: (r["lull_depth"] if r["lull_depth"] is not None else 0))
    return rows


def format_curve(curve, precision=2):
    """Format a lag→value dict as 'k=-8: 5.12 | k=-7: ...' etc."""
    parts = []
    for k in sorted(curve.keys()):
        parts.append(f"k={k:+d}:{curve[k]:.{precision}f}")
    return " | ".join(parts)


def analyze_overall(poem_stats):
    """Ignore era; pool all spikes to get the grand-average pre-peak curve."""
    all_h  = defaultdict(list)
    all_s  = defaultdict(list)
    all_s2 = defaultdict(list)
    total_spikes = 0
    for ps in poem_stats:
        if ps is None:
            continue
        for traj in ps["pre"]:
            total_spikes += 1
            for k, (h, s, s2) in traj.items():
                all_h[k].append(h)
                all_s[k].append(s)
                all_s2[k].append(s2)
    curves = {
        "h":  {k: statistics.mean(v) for k, v in sorted(all_h.items())},
        "s":  {k: statistics.mean(v) for k, v in sorted(all_s.items())},
        "s2": {k: statistics.mean(v) for k, v in sorted(all_s2.items())},
    }
    return curves, total_spikes


def top_traps(poem_stats, n=15):
    """Find the individual spikes with the deepest trap-depth (i.e. the
    ones best set up by preceding low entropy)."""
    candidates = []
    for ps in poem_stats:
        if ps is None:
            continue
        for (i, s2), traj in zip(ps["spikes"], ps["pre"]):
            close_h = [h for k, (h, _, _) in traj.items() if k >= -3]
            if not close_h:
                continue
            depth = statistics.mean(close_h) - ps["mean_h"]
            candidates.append({
                "trap_depth": depth,
                "s2": s2,
                "spike_idx": i,
                "author": ps["author"],
                "title": ps["title"],
                "era": ps["era"],
            })
    candidates.sort(key=lambda c: c["trap_depth"])  # most negative first
    return candidates[:n]


def main():
    poems = load_results()
    poem_stats = [analyze_poem(p) for p in poems]
    by_era = aggregate_by_era(poem_stats)
    rows = summarize(by_era)
    curves, total_spikes = analyze_overall(poem_stats)
    traps = top_traps(poem_stats)

    out = {
        "spike_threshold": SPIKE_THRESHOLD,
        "total_spikes": total_spikes,
        "total_poems": len(poems),
        "overall_curves": curves,
        "by_era": [
            {**row, "h_curve": row["h_curve"], "s2_curve": row["s2_curve"], "s_curve": row["s_curve"]}
            for row in rows
        ],
        "top_traps": traps,
    }

    out_path = os.path.join(RESULTS_DIR, "pre_peak_setup.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, default=str)

    print(f"\nAnalyzed {total_spikes} spikes (S₂ ≥ {SPIKE_THRESHOLD}) across {len(poems)} poems\n")
    print("=" * 78)
    print("OVERALL pre-peak curves (aggregated across all spikes)")
    print("=" * 78)
    print(f"  Entropy   : {format_curve(curves['h'])}")
    print(f"  Surprisal : {format_curve(curves['s'])}")
    print(f"  S₂        : {format_curve(curves['s2'])}")

    print("\n" + "=" * 78)
    print("PER-ERA: trap_depth (entropy at lags -3..-1  vs poem baseline)")
    print("         lull_depth (S₂      at lags -3..-1  vs poem baseline)")
    print("Negative = poet primes the model with easier / more conventional writing.")
    print("=" * 78)
    print(f"{'era':<22}{'n_poems':>10}{'n_spikes':>12}{'trap':>10}{'lull':>10}")
    for r in rows:
        td = f"{r['trap_depth']:+.3f}" if r['trap_depth'] is not None else "     n/a"
        ld = f"{r['lull_depth']:+.3f}" if r['lull_depth'] is not None else "     n/a"
        print(f"{r['era']:<22}{r['n_poems']:>10}{r['n_spikes']:>12}{td:>10}{ld:>10}")

    print("\n" + "=" * 78)
    print("TOP 15 individual spikes with deepest trap-depth")
    print("(Model was much MORE confident than usual just before the poet struck.)")
    print("=" * 78)
    for t in traps:
        print(f"  trap_depth {t['trap_depth']:+.2f}  S₂={t['s2']:.2f}  "
              f"{t['author'][:20]:<22} — {t['title'][:36]:<36}  ({t['era']})")

    print(f"\nSaved detailed data to {out_path}")


if __name__ == "__main__":
    main()
