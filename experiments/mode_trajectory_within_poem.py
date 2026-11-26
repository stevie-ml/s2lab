"""
Mode Trajectory Within Poem: Does the four-quadrant entropy/S2 mode change
across a poem's arc?

Builds on: entropy_inflation_per_poet.md (four-quadrant model)
           alternative_space_volatility.md (prediction space stabilizes over poem arc)

The four quadrants use corpus-wide baselines:
  BOTH_MODES       : entropy > mean AND S2 > mean  (raises uncertainty AND exceeds it)
  CHAOS_NAVIGATION : entropy > mean AND S2 < mean  (raises uncertainty but surrenders to it)
  CERTAIN_DEFIANCE : entropy < mean AND S2 > mean  (operates in tight contexts, deviates sharply)
  SMOOTH_CONFORMITY: entropy < mean AND S2 < mean  (prose-like)

For each poem we split into two halves and three thirds, compute per-segment
quadrant placement, and characterize the trajectory.
"""

import json
import os
import sys
from collections import defaultdict, Counter
import statistics

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")

# ── Corpus baselines from entropy_inflation_per_poet.md ──────────────────────
CORPUS_MEAN_ENTROPY = 6.415  # bits
CORPUS_MEAN_S2      = -0.262  # bits

QUAD_NAMES = {
    (True, True):   "BOTH_MODES",
    (True, False):  "CHAOS_NAVIGATION",
    (False, True):  "CERTAIN_DEFIANCE",
    (False, False): "SMOOTH_CONFORMITY",
}


def classify_quad(mean_entropy, mean_s2):
    high_e = mean_entropy > CORPUS_MEAN_ENTROPY
    high_s = mean_s2 > CORPUS_MEAN_S2
    return QUAD_NAMES[(high_e, high_s)]


def segment_tokens(tokens, n_segs):
    """Split list of tokens into n_segs roughly equal segments."""
    n = len(tokens)
    size = n / n_segs
    segs = []
    for i in range(n_segs):
        start = int(round(i * size))
        end = int(round((i + 1) * size))
        segs.append(tokens[start:end])
    return segs


def compute_seg_stats(tokens):
    """Compute mean entropy, mean S2 for a list of token dicts."""
    entropies = [t["entropy"] for t in tokens]
    s2s = [t["s2"] for t in tokens]
    return statistics.mean(entropies), statistics.mean(s2s)


def is_artifact(token):
    return token.get("p_newline", 0) >= 0.9 or token.get("token", "").strip() == ""


def main():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        data = json.load(f)

    MIN_TOKENS = 40
    results = []

    for poem in data:
        meta = poem["metadata"]
        tokens = poem["tokens"]
        clean = [t for t in tokens if not is_artifact(t)]

        if len(clean) < MIN_TOKENS:
            continue

        # ── Global poem stats ─────────────────────────────────────────────────
        all_e = [t["entropy"] for t in clean]
        all_s = [t["s2"] for t in clean]
        mean_e = statistics.mean(all_e)
        mean_s = statistics.mean(all_s)
        quad_overall = classify_quad(mean_e, mean_s)

        # ── Half split ────────────────────────────────────────────────────────
        half1, half2 = segment_tokens(clean, 2)
        h1e, h1s = compute_seg_stats(half1)
        h2e, h2s = compute_seg_stats(half2)
        q1 = classify_quad(h1e, h1s)
        q2 = classify_quad(h2e, h2s)
        traj_halves = f"{q1}→{q2}"
        changes_halves = int(q1 != q2)

        # ── Third split ───────────────────────────────────────────────────────
        t1, t2, t3 = segment_tokens(clean, 3)
        t1e, t1s = compute_seg_stats(t1)
        t2e, t2s = compute_seg_stats(t2)
        t3e, t3s = compute_seg_stats(t3)
        qt1 = classify_quad(t1e, t1s)
        qt2 = classify_quad(t2e, t2s)
        qt3 = classify_quad(t3e, t3s)
        traj_thirds = f"{qt1}→{qt2}→{qt3}"
        changes_thirds = int(qt1 != qt2) + int(qt2 != qt3)

        # ── Entropy and S2 drift (second half minus first half) ───────────────
        entropy_drift = h2e - h1e   # positive = entropy rises toward end
        s2_drift      = h2s - h1s   # positive = more surprising toward end

        results.append({
            "title":         meta.get("title", ""),
            "author":        meta.get("author", ""),
            "era":           meta.get("era", ""),
            "year":          meta.get("year"),
            "n_clean":       len(clean),
            "mean_entropy":  round(mean_e, 4),
            "mean_s2":       round(mean_s, 4),
            "quad_overall":  quad_overall,
            # halves
            "h1_entropy":    round(h1e, 4),
            "h1_s2":         round(h1s, 4),
            "h2_entropy":    round(h2e, 4),
            "h2_s2":         round(h2s, 4),
            "quad_h1":       q1,
            "quad_h2":       q2,
            "traj_halves":   traj_halves,
            "changes_halves": changes_halves,
            # thirds
            "quad_t1":       qt1,
            "quad_t2":       qt2,
            "quad_t3":       qt3,
            "traj_thirds":   traj_thirds,
            "changes_thirds": changes_thirds,
            # drift
            "entropy_drift": round(entropy_drift, 4),
            "s2_drift":      round(s2_drift, 4),
        })

    # ── Summary statistics ────────────────────────────────────────────────────
    n = len(results)
    stable_count = sum(1 for r in results if r["changes_halves"] == 0)
    changing_count = n - stable_count

    # Trajectory frequency (halves)
    traj_counts = Counter(r["traj_halves"] for r in results)
    traj_thirds_counts = Counter(r["traj_thirds"] for r in results)

    # Average drift by overall quadrant
    drift_by_quad = defaultdict(list)
    for r in results:
        drift_by_quad[r["quad_overall"]].append({
            "entropy_drift": r["entropy_drift"],
            "s2_drift":      r["s2_drift"],
        })

    drift_summary = {}
    for q, vals in drift_by_quad.items():
        drift_summary[q] = {
            "n": len(vals),
            "mean_entropy_drift": round(statistics.mean(v["entropy_drift"] for v in vals), 4),
            "mean_s2_drift":      round(statistics.mean(v["s2_drift"] for v in vals), 4),
        }

    # Per-era trajectory profile
    era_trajs = defaultdict(list)
    for r in results:
        era_trajs[r["era"]].append(r)

    era_summary = {}
    for era, poems in era_trajs.items():
        if len(poems) < 3:
            continue
        stable_frac = sum(1 for p in poems if p["changes_halves"] == 0) / len(poems)
        common_traj = Counter(p["traj_halves"] for p in poems).most_common(1)[0]
        era_summary[era] = {
            "n": len(poems),
            "stable_frac": round(stable_frac, 3),
            "most_common_traj": common_traj[0],
            "most_common_traj_n": common_traj[1],
            "mean_entropy_drift": round(statistics.mean(p["entropy_drift"] for p in poems), 4),
            "mean_s2_drift":      round(statistics.mean(p["s2_drift"] for p in poems), 4),
        }

    # Trajectory class examples
    traj_examples = defaultdict(list)
    for r in results:
        traj_examples[r["traj_halves"]].append(r)

    output = {
        "n_poems": n,
        "corpus_baselines": {"mean_entropy": CORPUS_MEAN_ENTROPY, "mean_s2": CORPUS_MEAN_S2},
        "stability": {
            "stable_halves": stable_count,
            "changing_halves": changing_count,
            "stable_pct": round(100 * stable_count / n, 1),
        },
        "trajectory_frequency_halves": dict(traj_counts.most_common()),
        "trajectory_frequency_thirds": dict(traj_thirds_counts.most_common(20)),
        "drift_by_overall_quad": drift_summary,
        "era_summary": dict(sorted(era_summary.items(), key=lambda x: x[1]["n"], reverse=True)),
        "poems": results,
    }

    out_path = os.path.join(RESULTS_DIR, "mode_trajectory_within_poem.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Saved {n} poems → {out_path}")

    # Quick print summary
    print(f"\nStability: {stable_count}/{n} poems ({100*stable_count/n:.1f}%) stay in same quadrant (halves)")
    print("\nTop 10 half-trajectories:")
    for traj, cnt in traj_counts.most_common(10):
        pct = 100 * cnt / n
        print(f"  {traj}: {cnt} ({pct:.1f}%)")
    print("\nDrift by overall quadrant:")
    for q, d in sorted(drift_summary.items(), key=lambda x: -x[1]["n"]):
        print(f"  {q} (n={d['n']}): entropy_drift={d['mean_entropy_drift']:+.3f}  s2_drift={d['mean_s2_drift']:+.3f}")


if __name__ == "__main__":
    main()
