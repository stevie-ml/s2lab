"""
Entropy Variance vs S₂: The Trap-and-Release Mechanism

Research question: Do high-S₂ poets achieve surprise through CONTRAST —
setting up low-entropy (confident) contexts and then deviating? Or through
sustained high entropy ("ambient uncertainty")?

This would appear as: correlation between within-poem entropy std and S₂.

Novel metric: for each poem, compute:
  - mean_H: average context entropy
  - std_H: within-poem entropy variance
  - mean_s2: average S₂
  - trap_release_score: fraction of high-S₂ tokens preceded by low-H context
  - fog_score: fraction of high-S₂ tokens preceded by high-H context
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = "/home/user/s2lab/results"
FINDINGS_DIR = "/home/user/s2lab/findings"
os.makedirs(FINDINGS_DIR, exist_ok=True)

ARTIFACT_P = 0.90  # stanza-break artifact threshold


def newline_prob(tok):
    return sum(a["prob"] for a in tok.get("alternatives", []) if a["token"].strip("\r\n") == "")


def clean_tokens(tokens):
    return [t for t in tokens if newline_prob(t) < ARTIFACT_P]


def load_results():
    path = os.path.join(RESULTS_DIR, "corpus_results.json")
    with open(path) as f:
        return json.load(f)


def analyze_poem(poem):
    tokens = clean_tokens(poem["tokens"])
    if len(tokens) < 15:
        return None

    H_vals = [t["entropy"] for t in tokens]
    s2_vals = [t["s2"] for t in tokens]

    mean_H = statistics.mean(H_vals)
    std_H = statistics.stdev(H_vals) if len(H_vals) > 1 else 0
    mean_s2 = statistics.mean(s2_vals)

    median_H = statistics.median(H_vals)
    median_s2 = statistics.median(s2_vals)

    # High S₂ tokens: s2 > 2.0 (above one std roughly)
    high_s2_tokens = [t for t in tokens if t["s2"] > 2.0]
    n_high_s2 = len(high_s2_tokens)

    # For each high-S₂ token, check the context entropy of the token BEFORE it
    # (this is the "setup" entropy — was the model confident before the surprise?)
    trap_release_count = 0  # high S₂ after LOW H (confident -> surprise)
    fog_leap_count = 0      # high S₂ after HIGH H (uncertain -> surprise)

    for i, tok in enumerate(tokens):
        if tok["s2"] > 2.0 and i > 0:
            prev_H = tokens[i-1]["entropy"]
            if prev_H < median_H:
                trap_release_count += 1
            else:
                fog_leap_count += 1

    total_surprise_events = trap_release_count + fog_leap_count
    if total_surprise_events > 0:
        trap_ratio = trap_release_count / total_surprise_events
    else:
        trap_ratio = None

    # "Entropy regularity": coefficient of variation of H (std/mean)
    # High CoV = very irregular entropy = more trap-and-release opportunities
    coeff_var_H = std_H / mean_H if mean_H > 0 else 0

    return {
        "title": poem["metadata"]["title"],
        "author": poem["metadata"]["author"],
        "era": poem["metadata"]["era"],
        "n_tokens": len(tokens),
        "mean_H": round(mean_H, 3),
        "std_H": round(std_H, 3),
        "coeff_var_H": round(coeff_var_H, 3),
        "mean_s2": round(mean_s2, 3),
        "median_H": round(median_H, 3),
        "n_high_s2": n_high_s2,
        "trap_ratio": round(trap_ratio, 3) if trap_ratio is not None else None,
        "trap_count": trap_release_count,
        "fog_count": fog_leap_count,
    }


def main():
    results = load_results()

    poem_stats = []
    for r in results:
        if r["metadata"].get("era") == "control":
            continue
        stat = analyze_poem(r)
        if stat:
            poem_stats.append(stat)

    # Also compute prose control stats
    prose_stats = []
    for r in results:
        if r["metadata"].get("era") == "control":
            stat = analyze_poem(r)
            if stat:
                prose_stats.append(stat)

    # 1. Overall correlation: does high std_H correlate with high mean_s2?
    s2_vals = [p["mean_s2"] for p in poem_stats]
    h_std_vals = [p["std_H"] for p in poem_stats]
    h_mean_vals = [p["mean_H"] for p in poem_stats]
    cv_vals = [p["coeff_var_H"] for p in poem_stats]

    # Simple Pearson r using covariance
    def pearson_r(xs, ys):
        n = len(xs)
        if n < 3:
            return None
        mx, my = statistics.mean(xs), statistics.mean(ys)
        cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
        sx = statistics.stdev(xs)
        sy = statistics.stdev(ys)
        return cov / (sx * sy) if sx > 0 and sy > 0 else None

    r_stdH_s2 = pearson_r(h_std_vals, s2_vals)
    r_meanH_s2 = pearson_r(h_mean_vals, s2_vals)
    r_cv_s2 = pearson_r(cv_vals, s2_vals)

    # 2. Classify poems by quadrant
    median_s2_all = statistics.median(s2_vals)
    median_stdH_all = statistics.median(h_std_vals)
    median_meanH_all = statistics.median(h_mean_vals)

    quadrants = defaultdict(list)
    for p in poem_stats:
        high_s2 = p["mean_s2"] > median_s2_all
        high_stdH = p["std_H"] > median_stdH_all
        if high_s2 and high_stdH:
            quadrants["Trap-Release (high S₂, variable H)"].append(p)
        elif high_s2 and not high_stdH:
            quadrants["Consistent Ambush (high S₂, stable H)"].append(p)
        elif not high_s2 and high_stdH:
            quadrants["Erratic Conformist (low S₂, variable H)"].append(p)
        else:
            quadrants["Metronomic (low S₂, stable H)"].append(p)

    # 3. Era-level breakdown
    era_data = defaultdict(list)
    for p in poem_stats:
        era_data[p["era"]].append(p)

    era_stats = {}
    for era, poems in era_data.items():
        if len(poems) < 2:
            continue
        era_stats[era] = {
            "n": len(poems),
            "mean_s2": statistics.mean(p["mean_s2"] for p in poems),
            "mean_stdH": statistics.mean(p["std_H"] for p in poems),
            "mean_coeff_var": statistics.mean(p["coeff_var_H"] for p in poems),
            "trap_ratio": statistics.mean(p["trap_ratio"] for p in poems if p["trap_ratio"] is not None),
        }

    # 4. Trap-and-release champions: highest trap_ratio with enough surprise events
    champions = [p for p in poem_stats if p["trap_ratio"] is not None and p["trap_count"] + p["fog_count"] >= 5]
    champions_sorted = sorted(champions, key=lambda p: p["trap_ratio"], reverse=True)

    # 5. Fog-leap champions: lowest trap_ratio (most fog-leap surprises)
    fog_champions = sorted(champions, key=lambda p: p["trap_ratio"])

    # --- Write output ---
    lines = []
    lines.append("# Within-Poem Entropy Variance and S₂: The Trap-and-Release Mechanism\n")
    lines.append("**Date:** 2026-11-26")
    lines.append(f"**Corpus:** {len(poem_stats)} poetry texts (artifact-free tokens, control excluded)\n")
    lines.append("**Research Question:** Do high-S₂ poems achieve surprise through *contrast* (low-entropy context → surprise) or through *sustained uncertainty* (high entropy throughout)?\n")
    lines.append("---\n")
    lines.append("## Method\n")
    lines.append("For each poem (artifact-filtered tokens, min 15 tokens):")
    lines.append("- **mean_H**: average context entropy across all tokens")
    lines.append("- **std_H**: standard deviation of entropy = within-poem entropy variance")
    lines.append("- **CoV(H)**: coefficient of variation of entropy (std_H / mean_H) = normalized irregularity")
    lines.append("- **trap_ratio**: among high-S₂ tokens (s2 > 2.0), fraction preceded by LOW-entropy token (H < median)")
    lines.append("  - trap_ratio = 1.0: ALL surprises come after confident contexts ('true Straussian ambush')")
    lines.append("  - trap_ratio = 0.0: ALL surprises come after uncertain contexts ('fog-and-leap')\n")
    lines.append("---\n")
    lines.append("## Corpus-Level Correlations\n")
    lines.append("| Metric pair | Pearson r | Interpretation |")
    lines.append("|---|---|---|")
    lines.append(f"| std(H) vs mean S₂ | **{r_stdH_s2:.3f}** | Does variable entropy predict high deviation? |")
    lines.append(f"| mean(H) vs mean S₂ | **{r_meanH_s2:.3f}** | Does uncertain context predict high deviation? |")
    lines.append(f"| CoV(H) vs mean S₂ | **{r_cv_s2:.3f}** | Does normalized entropy irregularity predict deviation? |")
    lines.append(f"\n*Note: n = {len(poem_stats)} poems. r > 0.3 is moderate, r > 0.5 is strong.*\n")

    lines.append("---\n")
    lines.append("## 2×2 Quadrant Classification\n")
    lines.append(f"Poems classified by whether mean S₂ and std(H) are above/below their corpus median.\n")
    lines.append(f"- **Median S₂**: {median_s2_all:.3f}")
    lines.append(f"- **Median std(H)**: {median_stdH_all:.3f}\n")
    lines.append("| Quadrant | n poems | Description |")
    lines.append("|---|---|---|")
    for qname, qpoems in sorted(quadrants.items(), key=lambda x: -len(x[1])):
        lines.append(f"| {qname} | {len(qpoems)} | — |")

    lines.append("\n### Top poems in each quadrant:\n")
    for qname, qpoems in sorted(quadrants.items(), key=lambda x: -len(x[1])):
        sorted_q = sorted(qpoems, key=lambda p: p["mean_s2"], reverse=True)[:3]
        lines.append(f"**{qname}** (n={len(qpoems)}):")
        for p in sorted_q:
            lines.append(f"  - {p['author']}, \"{p['title']}\" — S₂={p['mean_s2']:.2f}, std(H)={p['std_H']:.2f}")
        lines.append("")

    lines.append("---\n")
    lines.append("## Trap-and-Release Champions (highest trap_ratio, ≥5 high-S₂ events)\n")
    lines.append("| Author | Title | Era | trap_ratio | n surprises | mean S₂ | mean H |")
    lines.append("|---|---|---|---|---|---|---|")
    for p in champions_sorted[:15]:
        total = p["trap_count"] + p["fog_count"]
        lines.append(f"| {p['author']} | \"{p['title']}\" | {p['era']} | **{p['trap_ratio']:.2f}** | {total} | {p['mean_s2']:.2f} | {p['mean_H']:.2f} |")

    lines.append("\n## Fog-and-Leap Champions (lowest trap_ratio, ≥5 high-S₂ events)\n")
    lines.append("| Author | Title | Era | trap_ratio | n surprises | mean S₂ | mean H |")
    lines.append("|---|---|---|---|---|---|---|")
    for p in fog_champions[:15]:
        total = p["trap_count"] + p["fog_count"]
        lines.append(f"| {p['author']} | \"{p['title']}\" | {p['era']} | **{p['trap_ratio']:.2f}** | {total} | {p['mean_s2']:.2f} | {p['mean_H']:.2f} |")

    lines.append("\n---\n")
    lines.append("## Era-Level Entropy Variance Profile\n")
    lines.append("| Era | n | mean S₂ | mean std(H) | mean CoV(H) | trap_ratio |")
    lines.append("|---|---|---|---|---|---|")
    for era, es in sorted(era_stats.items(), key=lambda x: -x[1]["trap_ratio"]):
        lines.append(f"| {era} | {es['n']} | {es['mean_s2']:.2f} | {es['mean_stdH']:.2f} | {es['mean_coeff_var']:.2f} | **{es['trap_ratio']:.2f}** |")

    lines.append("\n---\n")
    lines.append("## Prose Control Comparison\n")
    if prose_stats:
        prose_mean_s2 = statistics.mean(p["mean_s2"] for p in prose_stats)
        prose_mean_stdH = statistics.mean(p["std_H"] for p in prose_stats)
        prose_mean_cv = statistics.mean(p["coeff_var_H"] for p in prose_stats)
        prose_trap = [p["trap_ratio"] for p in prose_stats if p["trap_ratio"] is not None]
        prose_trap_mean = statistics.mean(prose_trap) if prose_trap else None
        lines.append(f"- Prose mean S₂: {prose_mean_s2:.3f}")
        lines.append(f"- Prose mean std(H): {prose_mean_stdH:.3f}")
        lines.append(f"- Prose mean CoV(H): {prose_mean_cv:.3f}")
        if prose_trap_mean:
            lines.append(f"- Prose trap_ratio: {prose_trap_mean:.3f}")

    # Finding section
    lines.append("\n---\n")
    lines.append("## Finding\n")

    if r_stdH_s2 and abs(r_stdH_s2) > 0.3:
        direction = "positive" if r_stdH_s2 > 0 else "negative"
        lines.append(f"**Key result**: std(H) and mean S₂ show a {direction} correlation (r = {r_stdH_s2:.3f}). "
                     f"This {'confirms' if direction == 'positive' else 'contradicts'} the trap-and-release hypothesis: "
                     f"poems with {'more variable' if direction == 'positive' else 'more stable'} entropy tend to have higher S₂.")
    else:
        lines.append(f"**Key result**: std(H) and mean S₂ are weakly correlated (r = {r_stdH_s2:.3f}). "
                     f"Entropy variance does not strongly predict S₂ magnitude.")

    if r_meanH_s2 and abs(r_meanH_s2) > 0.3:
        direction = "positive" if r_meanH_s2 > 0 else "negative"
        lines.append(f"\n**Context entropy**: mean H and mean S₂ are {direction}ly correlated (r = {r_meanH_s2:.3f}), "
                     f"{'suggesting that high-H contexts tend to produce higher S₂' if direction == 'positive' else 'suggesting that LOW-H (confident) contexts produce the highest S₂'}. "
                     f"{'This supports the fog-and-leap model (uncertainty breeds deviation).' if direction == 'positive' else 'This supports the trap-and-release model (confidence breeds ambush).'}")
    else:
        lines.append(f"\n**Context entropy**: mean H and mean S₂ are weakly correlated (r = {r_meanH_s2:.3f}).")

    # Quadrant finding
    trap_q = quadrants["Trap-Release (high S₂, variable H)"]
    ambush_q = quadrants["Consistent Ambush (high S₂, stable H)"]
    fog_q = quadrants["Metronomic (low S₂, stable H)"]
    erratic_q = quadrants["Erratic Conformist (low S₂, variable H)"]

    lines.append(f"\n**Quadrant analysis**: {len(trap_q)} poems ({len(trap_q)*100//len(poem_stats)}%) are 'Trap-Release' (high S₂, variable H). "
                 f"{len(ambush_q)} ({len(ambush_q)*100//len(poem_stats)}%) are 'Consistent Ambush' (high S₂, stable H). "
                 f"This means high-S₂ poetry is split between poems that use entropy variation to set up surprise and poems that maintain consistently unpredictable contexts.")

    lines.append(f"\n**Suggested next steps**:")
    lines.append("1. Examine whether trap_ratio varies systematically with *era* (e.g., do Romantic poets trap-and-release while Language poets fog-and-leap?)")
    lines.append("2. Within the 'Consistent Ambush' quadrant, what makes the high S₂ tokens unexpected if H is stable? Are these the 'truly deviant' words?")
    lines.append("3. Test whether trap_ratio correlates with perceived poetic 'intensity' or 'impact' metrics.")

    output = "\n".join(lines)
    outpath = os.path.join(FINDINGS_DIR, "entropy_variance_trap_release.md")
    with open(outpath, "w") as f:
        f.write(output)

    # Also save JSON
    out_data = {
        "correlations": {
            "r_stdH_s2": r_stdH_s2,
            "r_meanH_s2": r_meanH_s2,
            "r_cv_s2": r_cv_s2,
        },
        "corpus_medians": {
            "s2": median_s2_all,
            "std_H": median_stdH_all,
            "mean_H": median_meanH_all,
        },
        "quadrant_counts": {k: len(v) for k, v in quadrants.items()},
        "era_stats": era_stats,
        "top_trap_poems": [p for p in champions_sorted[:20]],
        "top_fog_poems": [p for p in fog_champions[:20]],
    }
    json_path = os.path.join(RESULTS_DIR, "entropy_variance_trap_release.json")
    with open(json_path, "w") as f:
        json.dump(out_data, f, indent=2)

    print(f"Written: {outpath}")
    print(f"Written: {json_path}")
    print(f"\nCorrelations:")
    print(f"  r(std_H, S₂) = {r_stdH_s2:.3f}")
    print(f"  r(mean_H, S₂) = {r_meanH_s2:.3f}")
    print(f"  r(CoV_H, S₂) = {r_cv_s2:.3f}")
    print(f"\nQuadrant counts:")
    for qname, qpoems in sorted(quadrants.items(), key=lambda x: -len(x[1])):
        print(f"  {qname}: {len(qpoems)}")

    return out_data


if __name__ == "__main__":
    main()
