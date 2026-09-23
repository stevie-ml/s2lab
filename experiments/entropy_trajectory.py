"""
Entropy Trajectory Analysis: How Does Uncertainty Change Across a Poem?

Following from entropy_decomposition.py, which showed that:
  - Minimalist/CD poets create 'entropy punctures' (certainty-defying spikes)
  - Dense/CN poets create sustained high-entropy states

This experiment asks: does entropy systematically change OVER THE COURSE of a poem?

Hypotheses:
  H1: Poems open with low entropy and build toward uncertainty (ASCENDING ramp)
  H2: Poems begin in uncertainty and resolve toward certainty (DESCENDING / closure)
  H3: Chaos Navigation poets produce ascending entropy arcs; CD poets produce flat or punctured arcs
  H4: Different eras have characteristic trajectory signatures

Approach:
  - Divide each poem into 3 equal segments (beginning, middle, end)
  - Compute mean entropy per segment (excluding stanza-break artifacts)
  - Classify trajectory: ASCENDING, DESCENDING, ARCH, VALLEY, FLAT
  - Correlate with era, S2 strategy, and closure patterns
"""

import json
import ast
from collections import defaultdict
import statistics

with open("results/corpus_results.json") as f:
    data = json.load(f)


def parse_tokens(entry):
    t = entry.get("tokens", [])
    if isinstance(t, list):
        return t
    try:
        return ast.literal_eval(t)
    except Exception:
        return []


def parse_metadata(entry):
    m = entry.get("metadata", {})
    if isinstance(m, dict):
        return m
    try:
        return ast.literal_eval(m)
    except Exception:
        return {}


def is_artifact(token_data):
    alts = token_data.get("alternatives", [])
    if not alts:
        return False
    top_alt = alts[0]
    return top_alt.get("token", "") == "\n" and top_alt.get("prob", 0) > 0.9


def classify_trajectory(begin_e, mid_e, end_e, threshold=0.5):
    """
    Classify poem entropy trajectory from three-segment means.
    threshold = minimum change in entropy units to count as "real" change
    """
    asc_first = mid_e - begin_e > threshold
    asc_second = end_e - mid_e > threshold
    desc_first = begin_e - mid_e > threshold
    desc_second = mid_e - end_e > threshold

    if asc_first and asc_second:
        return "ASCENDING"
    elif desc_first and desc_second:
        return "DESCENDING"
    elif asc_first and desc_second:
        return "ARCH"
    elif desc_first and asc_second:
        return "VALLEY"
    else:
        return "FLAT"


# ------- collect per-poem entropy trajectories -------
MIN_TOKENS = 30  # minimum clean tokens for reliable segmentation

poem_trajectories = []

for entry in data:
    meta = parse_metadata(entry)
    tokens = parse_tokens(entry)

    # Filter artifacts
    clean = [t for t in tokens if not is_artifact(t)]

    if len(clean) < MIN_TOKENS:
        continue

    era = meta.get("era", "unknown")
    author = meta.get("author", "Unknown")
    title = meta.get("title", "Untitled")
    year = meta.get("year", 0)

    # Divide into thirds
    n = len(clean)
    s1 = clean[:n // 3]
    s2 = clean[n // 3: 2 * n // 3]
    s3 = clean[2 * n // 3:]

    def seg_entropy(seg):
        vals = [t["entropy"] for t in seg if t.get("entropy") is not None]
        return statistics.mean(vals) if vals else None

    def seg_s2(seg):
        vals = [t["s2"] for t in seg if t.get("s2") is not None]
        return statistics.mean(vals) if vals else None

    e1 = seg_entropy(s1)
    e2 = seg_entropy(s2)
    e3 = seg_entropy(s3)

    if e1 is None or e2 is None or e3 is None:
        continue

    traj = classify_trajectory(e1, e2, e3)

    # Also track S2 trajectory
    s2_1 = seg_s2(s1)
    s2_2 = seg_s2(s2)
    s2_3 = seg_s2(s3)

    # Overall metrics
    all_entropy = [t["entropy"] for t in clean if t.get("entropy") is not None]
    all_s2 = [t["s2"] for t in clean if t.get("s2") is not None]

    poem_trajectories.append({
        "era": era,
        "author": author,
        "title": title,
        "year": year,
        "n_tokens": len(clean),
        "entropy_begin": round(e1, 3),
        "entropy_mid": round(e2, 3),
        "entropy_end": round(e3, 3),
        "entropy_slope": round(e3 - e1, 3),  # net entropy change
        "entropy_mean": round(statistics.mean(all_entropy), 3),
        "trajectory": traj,
        "s2_begin": round(s2_1, 3) if s2_1 else None,
        "s2_mid": round(s2_2, 3) if s2_2 else None,
        "s2_end": round(s2_3, 3) if s2_3 else None,
        "s2_mean": round(statistics.mean(all_s2), 3),
    })

print(f"Total poems analyzed: {len(poem_trajectories)}")
print()

# ------- FINDING 1: Overall trajectory distribution -------
traj_counts = defaultdict(int)
for p in poem_trajectories:
    traj_counts[p["trajectory"]] += 1

total = len(poem_trajectories)
print("=== FINDING 1: Trajectory Distribution ===")
print(f"{'Trajectory':<15} {'Count':>6} {'%':>7}")
for traj, count in sorted(traj_counts.items(), key=lambda x: -x[1]):
    print(f"{traj:<15} {count:>6} {100*count/total:>6.1f}%")
print()

# ------- FINDING 2: Trajectory vs S2 -------
print("=== FINDING 2: Trajectory vs Mean S2 ===")
traj_s2 = defaultdict(list)
traj_entropy_slope = defaultdict(list)
for p in poem_trajectories:
    traj_s2[p["trajectory"]].append(p["s2_mean"])
    traj_entropy_slope[p["trajectory"]].append(p["entropy_slope"])

print(f"{'Trajectory':<15} {'n':>5} {'Mean S2':>9} {'Mean ΔH':>9} {'SD S2':>8}")
for traj in sorted(traj_s2.keys(), key=lambda t: -statistics.mean(traj_s2[t])):
    n = len(traj_s2[traj])
    m_s2 = statistics.mean(traj_s2[traj])
    m_slope = statistics.mean(traj_entropy_slope[traj])
    sd_s2 = statistics.stdev(traj_s2[traj]) if n > 1 else 0
    print(f"{traj:<15} {n:>5} {m_s2:>9.3f} {m_slope:>9.3f} {sd_s2:>8.3f}")
print()

# ------- FINDING 3: Era trajectories -------
print("=== FINDING 3: Era Trajectory Profiles ===")
era_trajs = defaultdict(lambda: defaultdict(int))
era_slopes = defaultdict(list)

SKIP_ERAS = {"control_prose"}
for p in poem_trajectories:
    era = p["era"]
    if era in SKIP_ERAS:
        continue
    era_trajs[era][p["trajectory"]] += 1
    era_slopes[era].append(p["entropy_slope"])

# For each era, find dominant trajectory and mean slope
era_summary = []
for era, traj_dist in era_trajs.items():
    total_era = sum(traj_dist.values())
    dominant = max(traj_dist, key=lambda t: traj_dist[t])
    dom_pct = 100 * traj_dist[dominant] / total_era
    flat_pct = 100 * traj_dist.get("FLAT", 0) / total_era
    asc_pct = 100 * traj_dist.get("ASCENDING", 0) / total_era
    desc_pct = 100 * traj_dist.get("DESCENDING", 0) / total_era
    mean_slope = statistics.mean(era_slopes[era])
    era_summary.append({
        "era": era, "n": total_era, "dominant": dominant,
        "dom_pct": dom_pct, "flat_pct": flat_pct,
        "asc_pct": asc_pct, "desc_pct": desc_pct,
        "mean_slope": mean_slope
    })

# Sort by mean entropy slope (ascending → descending)
era_summary.sort(key=lambda x: -x["mean_slope"])
print(f"{'Era':<30} {'n':>4} {'ASC%':>6} {'DESC%':>7} {'FLAT%':>7} {'MeanΔH':>8}")
for e in era_summary:
    print(f"{e['era']:<30} {e['n']:>4} {e['asc_pct']:>6.1f} {e['desc_pct']:>7.1f} {e['flat_pct']:>7.1f} {e['mean_slope']:>8.3f}")
print()

# ------- FINDING 4: Author trajectory profiles (≥4 poems) -------
print("=== FINDING 4: Author Trajectory Profiles (≥4 poems) ===")
author_trajs = defaultdict(lambda: defaultdict(int))
author_slopes = defaultdict(list)
author_eras = {}

for p in poem_trajectories:
    author_trajs[p["author"]][p["trajectory"]] += 1
    author_slopes[p["author"]].append(p["entropy_slope"])
    author_eras[p["author"]] = p["era"]

author_data = []
for author, traj_dist in author_trajs.items():
    n = sum(traj_dist.values())
    if n < 4:
        continue
    mean_slope = statistics.mean(author_slopes[author])
    flat_pct = 100 * traj_dist.get("FLAT", 0) / n
    asc_pct = 100 * traj_dist.get("ASCENDING", 0) / n
    desc_pct = 100 * traj_dist.get("DESCENDING", 0) / n
    arch_pct = 100 * traj_dist.get("ARCH", 0) / n
    valley_pct = 100 * traj_dist.get("VALLEY", 0) / n
    dominant = max(traj_dist, key=lambda t: traj_dist[t])
    author_data.append({
        "author": author, "n": n, "era": author_eras[author],
        "dominant": dominant, "mean_slope": mean_slope,
        "flat_pct": flat_pct, "asc_pct": asc_pct, "desc_pct": desc_pct,
        "arch_pct": arch_pct, "valley_pct": valley_pct
    })

# Print top ascending authors (entropy rises across poem)
author_data.sort(key=lambda x: -x["mean_slope"])
print("\n  Top ASCENDING (entropy builds across poem):")
print(f"  {'Author':<30} {'n':>4} {'ASC%':>6} {'DESC%':>7} {'MeanΔH':>8} {'Era'}")
for a in author_data[:8]:
    print(f"  {a['author']:<30} {a['n']:>4} {a['asc_pct']:>6.1f} {a['desc_pct']:>7.1f} {a['mean_slope']:>8.3f}  {a['era']}")

print("\n  Top DESCENDING (entropy resolves across poem):")
author_data.sort(key=lambda x: x["mean_slope"])
for a in author_data[:8]:
    print(f"  {a['author']:<30} {a['n']:>4} {a['asc_pct']:>6.1f} {a['desc_pct']:>7.1f} {a['mean_slope']:>8.3f}  {a['era']}")

# ------- FINDING 5: Entropy slope and S2 correlation -------
print()
print("=== FINDING 5: Entropy Slope vs S2 ===")
# Bin by entropy slope direction
ascending = [p for p in poem_trajectories if p["trajectory"] == "ASCENDING"]
descending = [p for p in poem_trajectories if p["trajectory"] == "DESCENDING"]
flat = [p for p in poem_trajectories if p["trajectory"] == "FLAT"]

def group_stats(group, label):
    if not group:
        return
    slopes = [p["entropy_slope"] for p in group]
    s2s = [p["s2_mean"] for p in group]
    e_begins = [p["entropy_begin"] for p in group]
    e_ends = [p["entropy_end"] for p in group]
    print(f"\n  {label} (n={len(group)}):")
    print(f"    Mean entropy slope: {statistics.mean(slopes):+.3f}")
    print(f"    Mean entropy: begin={statistics.mean(e_begins):.2f}, end={statistics.mean(e_ends):.2f}")
    print(f"    Mean S2: {statistics.mean(s2s):+.3f}")

group_stats(ascending, "ASCENDING poems")
group_stats(descending, "DESCENDING poems")
group_stats(flat, "FLAT poems")

# ------- FINDING 6: Exemplary poems -------
print()
print("=== FINDING 6: Exemplary Trajectories ===")

# Strongest ascending poems
poem_trajectories_sorted = sorted(poem_trajectories, key=lambda p: -p["entropy_slope"])
print("\n  Strongest entropy ascent (entropy ramps UP):")
print(f"  {'Title':<40} {'Author':<25} {'H_beg':>6} {'H_end':>6} {'ΔH':>7}")
for p in poem_trajectories_sorted[:5]:
    print(f"  {p['title'][:39]:<40} {p['author'][:24]:<25} {p['entropy_begin']:>6.2f} {p['entropy_end']:>6.2f} {p['entropy_slope']:>+7.2f}")

# Strongest descending poems
poem_trajectories_sorted_desc = sorted(poem_trajectories, key=lambda p: p["entropy_slope"])
print("\n  Strongest entropy descent (entropy ramps DOWN / resolves):")
print(f"  {'Title':<40} {'Author':<25} {'H_beg':>6} {'H_end':>6} {'ΔH':>7}")
for p in poem_trajectories_sorted_desc[:5]:
    print(f"  {p['title'][:39]:<40} {p['author'][:24]:<25} {p['entropy_begin']:>6.2f} {p['entropy_end']:>6.2f} {p['entropy_slope']:>+7.2f}")

# ARCH poems (rise then fall) - classical closure
arch_poems = [p for p in poem_trajectories if p["trajectory"] == "ARCH"]
arch_poems.sort(key=lambda p: -(p["entropy_mid"] - min(p["entropy_begin"], p["entropy_end"])))
if arch_poems:
    print("\n  ARCH poems (entropy peaks in middle, closes down):")
    print(f"  {'Title':<40} {'Author':<25} {'H_beg':>6} {'H_mid':>6} {'H_end':>6}")
    for p in arch_poems[:5]:
        print(f"  {p['title'][:39]:<40} {p['author'][:24]:<25} {p['entropy_begin']:>6.2f} {p['entropy_mid']:>6.2f} {p['entropy_end']:>6.2f}")

# ------- FINDING 7: Trajectory vs closure (end entropy as proxy for resolution) -------
print()
print("=== FINDING 7: Does Poetic Closure Correlate with Falling End Entropy? ===")
# Compare end-entropy across eras
era_end_entropy = defaultdict(list)
era_begin_entropy = defaultdict(list)
for p in poem_trajectories:
    if p["era"] in SKIP_ERAS:
        continue
    era_end_entropy[p["era"]].append(p["entropy_end"])
    era_begin_entropy[p["era"]].append(p["entropy_begin"])

era_closure = []
for era in era_end_entropy:
    if len(era_end_entropy[era]) < 3:
        continue
    mean_end = statistics.mean(era_end_entropy[era])
    mean_begin = statistics.mean(era_begin_entropy[era])
    net_change = mean_end - mean_begin
    n = len(era_end_entropy[era])
    era_closure.append((era, n, mean_begin, mean_end, net_change))

era_closure.sort(key=lambda x: x[4])  # sort by net entropy change (descending -> ascending)
print(f"\n  {'Era':<30} {'n':>4} {'H_begin':>8} {'H_end':>8} {'Net ΔH':>8}")
for era, n, h_b, h_e, delta in era_closure:
    direction = "↓" if delta < 0 else "↑"
    print(f"  {era:<30} {n:>4} {h_b:>8.2f} {h_e:>8.2f} {delta:>+7.3f} {direction}")

print()
print("Done.")
