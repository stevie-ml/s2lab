"""
Vocabulary Priming Experiment
Research question: As GPT-2 reads through a poem, does it increasingly predict words
from the poem's own growing vocabulary (in-context priming)?

For each token at position P, we compute:
  in_context_ratio = (# of top-10 alternatives already seen in poem so far) / 10

Then analyze how this changes across:
  - Normalized poem position (do predictions increasingly reflect poem vocabulary?)
  - Poem avg_S2 quintile (do high-S2 poems resist priming?)
  - Era (which genres show strongest/weakest priming?)
  - Correlation with local S2

2026-10-29
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/vocab_priming.json"

def normalize(token_str):
    """Normalize token for vocabulary matching (lowercase, strip leading space)."""
    return token_str.strip().lower()

def run_experiment():
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    # Filter to English poetry with enough tokens
    poems = [
        p for p in data
        if p["metadata"].get("language", "en") == "en"
        and p["metadata"].get("era") not in ("control",)
        and len(p["tokens"]) >= 20
    ]
    print(f"Analyzing {len(poems)} poems...")

    poem_results = []
    position_buckets = defaultdict(list)  # normalized position -> list of in_context_ratios
    era_data = defaultdict(list)
    s2_quintile_data = defaultdict(list)
    local_s2_vs_ratio = []  # (s2, in_context_ratio) pairs

    for poem in poems:
        tokens = [t for t in poem["tokens"] if t.get("p_newline", 1.0) < 0.9]
        if len(tokens) < 10:
            continue

        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        avg_s2 = poem["summary"]["avg_s2"]

        running_vocab = set()
        poem_in_context_ratios = []
        poem_positions = []

        for i, tok in enumerate(tokens):
            alt_tokens = [normalize(a["token"]) for a in tok.get("alternatives", [])]
            if not alt_tokens:
                running_vocab.add(normalize(tok["token"]))
                continue

            # Count how many alternatives are in the running vocabulary
            in_context_count = sum(1 for a in alt_tokens if a in running_vocab)
            ratio = in_context_count / len(alt_tokens)

            poem_in_context_ratios.append(ratio)
            poem_positions.append(i / max(len(tokens) - 1, 1))  # normalized 0-1

            local_s2 = tok.get("s2", 0.0)
            local_s2_vs_ratio.append((local_s2, ratio))

            # Update running vocabulary with the actual chosen token
            running_vocab.add(normalize(tok["token"]))

        if not poem_in_context_ratios:
            continue

        # Compute position-bucketed averages for this poem
        buckets = [[], [], [], [], []]  # 5 equal segments
        for pos, ratio in zip(poem_positions, poem_in_context_ratios):
            bucket_idx = min(int(pos * 5), 4)
            buckets[bucket_idx].append(ratio)

        bucket_avgs = [statistics.mean(b) if b else None for b in buckets]

        # Priming slope: does ratio increase across the poem?
        if len(poem_in_context_ratios) >= 6:
            first_third = poem_in_context_ratios[:len(poem_in_context_ratios)//3]
            last_third = poem_in_context_ratios[-len(poem_in_context_ratios)//3:]
            priming_slope = statistics.mean(last_third) - statistics.mean(first_third)
        else:
            priming_slope = None

        result = {
            "title": meta.get("title"),
            "author": meta.get("author"),
            "era": era,
            "avg_s2": avg_s2,
            "n_tokens": len(tokens),
            "mean_in_context_ratio": statistics.mean(poem_in_context_ratios),
            "early_ratio": statistics.mean(poem_in_context_ratios[:len(poem_in_context_ratios)//3]) if len(poem_in_context_ratios) >= 3 else None,
            "late_ratio": statistics.mean(poem_in_context_ratios[-len(poem_in_context_ratios)//3:]) if len(poem_in_context_ratios) >= 3 else None,
            "priming_slope": priming_slope,
            "bucket_avgs": bucket_avgs,
        }
        poem_results.append(result)

        era_data[era].append({
            "avg_s2": avg_s2,
            "mean_ratio": statistics.mean(poem_in_context_ratios),
            "priming_slope": priming_slope,
        })

        # Position bucket data
        for pos, ratio in zip(poem_positions, poem_in_context_ratios):
            bucket = int(pos * 10)  # 10 deciles
            position_buckets[bucket].append(ratio)

    # Global position profile
    position_profile = {}
    for bucket in sorted(position_buckets.keys()):
        vals = position_buckets[bucket]
        position_profile[str(bucket)] = {
            "n": len(vals),
            "mean_ratio": round(statistics.mean(vals), 4),
            "stdev": round(statistics.stdev(vals) if len(vals) > 1 else 0, 4),
        }

    # S2 quintile analysis
    sorted_by_s2 = sorted(poem_results, key=lambda x: x["avg_s2"])
    n = len(sorted_by_s2)
    quintiles = {}
    for q in range(5):
        start = q * n // 5
        end = (q + 1) * n // 5
        group = sorted_by_s2[start:end]
        quintiles[f"Q{q+1}"] = {
            "avg_s2_range": [round(group[0]["avg_s2"], 3), round(group[-1]["avg_s2"], 3)],
            "n": len(group),
            "mean_in_context_ratio": round(statistics.mean(g["mean_in_context_ratio"] for g in group), 4),
            "mean_priming_slope": round(statistics.mean(g["priming_slope"] for g in group if g["priming_slope"] is not None), 4),
            "label": ["Q1 (least surprising)", "Q2", "Q3", "Q4", "Q5 (most surprising)"][q],
        }

    # Era summary
    era_summary = {}
    for era, records in era_data.items():
        if len(records) < 2:
            continue
        era_summary[era] = {
            "n": len(records),
            "mean_ratio": round(statistics.mean(r["mean_ratio"] for r in records), 4),
            "mean_priming_slope": round(statistics.mean(r["priming_slope"] for r in records if r["priming_slope"] is not None), 4),
            "mean_s2": round(statistics.mean(r["avg_s2"] for r in records), 3),
        }

    # Correlation between local S2 and in-context ratio
    # Use 10-bucket binning on S2
    s2_bins = defaultdict(list)
    for s2, ratio in local_s2_vs_ratio:
        # Cap extremes
        s2_capped = max(-10, min(10, s2))
        bin_key = int((s2_capped + 10) / 2)  # 0-9 bins for -10 to +10
        s2_bins[bin_key].append(ratio)

    s2_bin_summary = {}
    for bin_key in sorted(s2_bins.keys()):
        vals = s2_bins[bin_key]
        s2_center = bin_key * 2 - 10 + 1
        s2_bin_summary[str(s2_center)] = {
            "n": len(vals),
            "mean_ratio": round(statistics.mean(vals), 4),
            "s2_range": f"[{s2_center-1}, {s2_center+1}]",
        }

    output = {
        "n_poems": len(poem_results),
        "position_profile": position_profile,
        "s2_quintile_analysis": quintiles,
        "era_summary": era_summary,
        "s2_vs_in_context_ratio": s2_bin_summary,
        "top_poems_by_priming": sorted(
            [p for p in poem_results if p["priming_slope"] is not None],
            key=lambda x: x["priming_slope"], reverse=True
        )[:10],
        "bottom_poems_by_priming": sorted(
            [p for p in poem_results if p["priming_slope"] is not None],
            key=lambda x: x["priming_slope"]
        )[:10],
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Results saved to {OUTPUT_FILE}")
    return output

if __name__ == "__main__":
    results = run_experiment()
    print("\n=== Position Profile (deciles) ===")
    for pos, stats in results["position_profile"].items():
        print(f"  Decile {pos}: mean_ratio={stats['mean_ratio']:.4f} (n={stats['n']})")

    print("\n=== S2 Quintile Analysis ===")
    for q, data in results["s2_quintile_analysis"].items():
        print(f"  {data['label']}: ratio={data['mean_in_context_ratio']:.4f}, slope={data['mean_priming_slope']:.4f}")

    print("\n=== Top Eras by In-Context Ratio ===")
    sorted_eras = sorted(results["era_summary"].items(), key=lambda x: x[1]["mean_ratio"], reverse=True)
    for era, stats in sorted_eras[:10]:
        print(f"  {era}: ratio={stats['mean_ratio']:.4f}, slope={stats['mean_priming_slope']:.4f} (n={stats['n']})")
