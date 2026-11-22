"""
α-Primed Ambush: When GPT-2 Concentrates Its Predictions, Do Poets Strike?

The Zipf coefficient experiment (zipf_prediction_coefficient.md) showed that
different eras operate in different α regimes: beat poetry has high α (concentrated
predictions), symbolist poetry has low α (diffuse predictions).

The α arc experiment (alpha_arc_within_poem.md) showed that α rises as a poem
progresses — GPT-2 becomes more concentrated in its predictions the deeper it reads.

This experiment introduces a NEW metric: the **α-Primed Ambush Score**.

For each token position i:
  ambush_score[i] = max(0, α[i-1]) × max(0, s2[i])

This measures moments where:
  - The preceding context made the model CONFIDENT (high α at i-1)
  - The poet wrote something the model did NOT predict (high s2 at i)

The α-primed ambush is a stricter form of Straussian deviance: not just any
surprise, but surprise that defeats a concentrated, specific expectation.

Research questions:
1. What fraction of high-S2 tokens are also α-primed ambushes?
2. Do different poets/eras specialize in ambush vs. fog surprise?
3. What do the specific "perfect α-ambush" tokens look like?
4. Is there a characteristic temporal pattern — do α-ambushes cluster at certain
   positions within poems (volta, final couplet, line endings)?
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/alpha_primed_ambush.json"

# ───────── Zipf helper ──────────────────────────────────────────────────────

def fit_zipf_alpha(alts):
    """Fit Zipf exponent α to the top-10 alternative probabilities."""
    probs = [a["prob"] for a in alts if a.get("prob", 0) > 0]
    if len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs]
    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_probs = [math.log(p) for p in normed]
    mean_lr = sum(log_ranks) / n
    mean_lp = sum(log_probs) / n
    numer = sum((log_ranks[i] - mean_lr) * (log_probs[i] - mean_lp) for i in range(n))
    denom = sum((log_ranks[i] - mean_lr) ** 2 for i in range(n))
    if denom == 0:
        return None
    return -numer / denom

# ───────── Main analysis ────────────────────────────────────────────────────

def main():
    print("Loading corpus…")
    corpus = json.load(open(CORPUS_PATH))
    print(f"  {len(corpus)} texts loaded")

    # Per-token data for all poems
    all_ambush_scores = []          # all α-ambush scores across corpus
    global_top_ambushes = []        # for taxonomizing perfect ambushes

    # Aggregation by poet / era
    poet_data = defaultdict(lambda: {
        "ambush_scores": [], "s2_vals": [], "alpha_vals": [], "n_primed": 0
    })
    era_data = defaultdict(lambda: {
        "ambush_scores": [], "s2_vals": [], "alpha_vals": [], "n_primed": 0
    })

    # Position analysis (position within poem, normalized 0–1)
    n_buckets = 10
    position_buckets = defaultdict(list)

    n_skipped = 0

    for poem in corpus:
        meta = poem.get("metadata", {})
        lang = meta.get("language", "en")
        if lang != "en":
            continue  # English only for clean comparison

        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")

        tokens = poem.get("tokens", [])
        if len(tokens) < 4:
            n_skipped += 1
            continue

        # Build clean token sequence (filter stanza-break artifacts)
        clean = [
            t for t in tokens
            if t.get("p_newline", 0) < 0.9
            and t.get("alternatives") is not None
            and len(t["alternatives"]) >= 2
        ]
        if len(clean) < 4:
            n_skipped += 1
            continue

        # Compute α for each clean token
        alphas = []
        for t in clean:
            a = fit_zipf_alpha(t["alternatives"])
            alphas.append(a)

        s2s = [t["s2"] for t in clean]

        # Compute α-primed ambush scores (using previous token's α)
        poem_ambush = []
        for i in range(1, len(clean)):
            prev_alpha = alphas[i - 1]
            curr_s2 = s2s[i]
            if prev_alpha is None:
                poem_ambush.append(None)
                continue
            # Ambush score: only positive if BOTH α is high AND s2 is positive
            score = max(0.0, prev_alpha) * max(0.0, curr_s2)
            poem_ambush.append(score)

            # Is this an α-primed moment? (α > 1.5 AND s2 > 2.0)
            is_primed = prev_alpha > 1.5 and curr_s2 > 2.0

            poet_data[author]["ambush_scores"].append(score)
            poet_data[author]["s2_vals"].append(curr_s2)
            poet_data[author]["alpha_vals"].append(prev_alpha)
            if is_primed:
                poet_data[author]["n_primed"] += 1

            era_data[era]["ambush_scores"].append(score)
            era_data[era]["s2_vals"].append(curr_s2)
            era_data[era]["alpha_vals"].append(prev_alpha)
            if is_primed:
                era_data[era]["n_primed"] += 1

            # Position bucket
            norm_pos = (i - 1) / max(1, len(clean) - 2)
            bucket = min(n_buckets - 1, int(norm_pos * n_buckets))
            position_buckets[bucket].append(score)

            # Track top ambushes globally
            global_top_ambushes.append({
                "score": score,
                "s2": curr_s2,
                "alpha": prev_alpha,
                "token": clean[i]["token"],
                "top_pred": clean[i]["alternatives"][0]["token"] if clean[i]["alternatives"] else "?",
                "context": clean[i].get("context_before", "")[-40:],
                "author": author,
                "era": era,
                "title": meta.get("title", "Unknown"),
            })

        all_ambush_scores.extend([s for s in poem_ambush if s is not None])

    print(f"  Skipped {n_skipped} short/non-English texts")
    print(f"  Total token positions analyzed: {len(all_ambush_scores)}")

    # ── Global stats ──────────────────────────────────────────────────────
    valid_scores = [s for s in all_ambush_scores if s is not None]
    global_stats = {
        "n_positions": len(valid_scores),
        "mean_ambush": statistics.mean(valid_scores) if valid_scores else 0,
        "median_ambush": statistics.median(valid_scores) if valid_scores else 0,
        "pct_primed_ambush": sum(1 for s in valid_scores if s > 3.0) / max(1, len(valid_scores)),
        "pct_primed_ambush_strict": sum(1 for s in valid_scores if s > 6.0) / max(1, len(valid_scores)),
    }

    # ── Era profiles ──────────────────────────────────────────────────────
    era_profiles = {}
    for era, d in era_data.items():
        sc = d["ambush_scores"]
        s2 = d["s2_vals"]
        al = d["alpha_vals"]
        n = len(sc)
        if n < 20:
            continue
        era_profiles[era] = {
            "n": n,
            "mean_ambush": statistics.mean(sc),
            "mean_s2": statistics.mean(s2),
            "mean_alpha": statistics.mean(al),
            "pct_primed": d["n_primed"] / n,
            "ambush_ratio": statistics.mean(sc) / max(0.001, statistics.mean([abs(v) for v in s2])),
        }

    # Sort eras by mean_ambush
    era_ranked = sorted(era_profiles.items(), key=lambda x: x[1]["mean_ambush"], reverse=True)

    # ── Poet profiles ─────────────────────────────────────────────────────
    poet_profiles = {}
    for poet, d in poet_data.items():
        sc = d["ambush_scores"]
        s2 = d["s2_vals"]
        al = d["alpha_vals"]
        n = len(sc)
        if n < 30:
            continue
        poet_profiles[poet] = {
            "n": n,
            "mean_ambush": statistics.mean(sc),
            "mean_s2": statistics.mean(s2),
            "mean_alpha": statistics.mean(al),
            "pct_primed": d["n_primed"] / n,
        }

    poet_ranked = sorted(poet_profiles.items(), key=lambda x: x[1]["mean_ambush"], reverse=True)

    # ── Position analysis ─────────────────────────────────────────────────
    position_profile = {}
    for b in range(n_buckets):
        sc = position_buckets[b]
        if sc:
            position_profile[b] = {
                "mean_ambush": statistics.mean(sc),
                "n": len(sc),
            }

    # ── Perfect ambushes (top 50 by score) ───────────────────────────────
    top_ambushes = sorted(global_top_ambushes, key=lambda x: x["score"], reverse=True)[:60]

    # ── Fraction of S2 that is α-primed ──────────────────────────────────
    # Compare: tokens with S2 > 2.0 that have high α vs. not
    high_s2_tokens = [t for t in global_top_ambushes if t["s2"] > 2.0]
    alpha_primed_high_s2 = sum(1 for t in high_s2_tokens if t["alpha"] > 1.5)
    alpha_fog_high_s2 = len(high_s2_tokens) - alpha_primed_high_s2
    fraction_ambush_vs_fog = {
        "total_high_s2": len(high_s2_tokens),
        "alpha_primed_count": alpha_primed_high_s2,
        "alpha_fog_count": alpha_fog_high_s2,
        "pct_ambush": alpha_primed_high_s2 / max(1, len(high_s2_tokens)),
        "pct_fog": alpha_fog_high_s2 / max(1, len(high_s2_tokens)),
    }

    # Assemble output
    result = {
        "global_stats": global_stats,
        "ambush_vs_fog_decomposition": fraction_ambush_vs_fog,
        "era_profiles": {k: v for k, v in era_ranked},
        "poet_profiles": {k: v for k, v in poet_ranked[:25]},
        "position_profile": position_profile,
        "top_ambushes": top_ambushes,
    }

    json.dump(result, open(OUTPUT_PATH, "w"), indent=2)
    print(f"\nResults saved to {OUTPUT_PATH}")

    # Quick summary
    print("\n── Global Stats ─────────────────────────────")
    for k, v in global_stats.items():
        print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")

    print("\n── Top 15 Eras by α-Ambush Score ────────────")
    print(f"{'Era':<25} {'n':>6} {'mean_ambush':>12} {'mean_s2':>9} {'mean_α':>8} {'pct_primed':>11}")
    for era, p in era_ranked[:15]:
        print(f"{era:<25} {p['n']:>6} {p['mean_ambush']:>12.4f} {p['mean_s2']:>9.4f} {p['mean_alpha']:>8.4f} {p['pct_primed']:>10.1%}")

    print("\n── Top 15 Poets by α-Ambush Score ───────────")
    print(f"{'Poet':<30} {'n':>6} {'mean_ambush':>12} {'mean_s2':>9} {'pct_primed':>11}")
    for poet, p in poet_ranked[:15]:
        print(f"{poet:<30} {p['n']:>6} {p['mean_ambush']:>12.4f} {p['mean_s2']:>9.4f} {p['pct_primed']:>10.1%}")

    print("\n── Top 10 Perfect α-Ambushes ─────────────────")
    for t in top_ambushes[:10]:
        print(f"  score={t['score']:.2f}  s2={t['s2']:.2f}  α={t['alpha']:.2f}")
        print(f"  token: '{t['token']}'  top_pred: '{t['top_pred']}'")
        print(f"  context: ...{t['context'].strip()}")
        print(f"  → {t['author']} / {t['title']}")
        print()

    print("\n── Ambush vs. Fog Decomposition (all S2 > 2.0 tokens) ──")
    d = fraction_ambush_vs_fog
    print(f"  Total high-S2 tokens: {d['total_high_s2']}")
    print(f"  α-primed (α>1.5 before): {d['alpha_primed_count']} ({d['pct_ambush']:.1%})")
    print(f"  α-fog    (α≤1.5 before): {d['alpha_fog_count']} ({d['pct_fog']:.1%})")

    print("\n── Position Profile (normalized within-poem) ─")
    for b in range(n_buckets):
        p = position_profile.get(b, {})
        print(f"  D{b+1} ({b*10}–{(b+1)*10}%): mean_ambush={p.get('mean_ambush',0):.4f} n={p.get('n',0)}")


if __name__ == "__main__":
    main()
