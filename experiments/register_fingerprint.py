"""
Register Fingerprint: Full Corpus 2D Mapping

Maps all poems onto a 2D space:
  X-axis: Entropy Autocorrelation (lag-1) — rhythmic groove signal
  Y-axis: True Straussian Score — lexical deviation at confident positions

Hypothesis: oral and literary traditions form separable clusters in this space.
Special interest: "covert" crossovers — poems that score as the wrong register.

Builds directly on oral_literary_register.md findings.
"""

import json
import math
from collections import defaultdict

with open("results/corpus_results.json") as f:
    data = json.load(f)

# ─── Register classification (same as oral_literary_register.py) ─────────────
ORAL_ERAS = {"ballad", "spoken_word", "song_lyrics", "nursery_rhyme", "biblical"}
LITERARY_ERAS = {
    "modernist", "language", "metaphysical",
    "new_york_school", "imagist", "surrealist", "oulipo",
}
MIXED_ERAS = {
    "romantic", "victorian", "19th_century", "confessional",
    "contemporary", "harlem_renaissance", "prose_poetry", "beat",
    "fixed_form", "early_modern", "found_poetry", "haiku",
    "mid_century", "deep_image", "concrete", "black_arts",
    "latin_american", "german_symbolist", "german_modernist",
    "german_expressionist", "ancient", "korean_modernist",
}

ENTROPY_THRESHOLD = 5.0  # confident positions

def compute_fingerprint(poem_data):
    tokens = poem_data["tokens"]
    clean = [t for t in tokens if t.get("p_newline", 0) <= 0.5]
    if len(clean) < 15:
        return None

    entropies = [t["entropy"] for t in clean]
    s2s = [t["s2"] for t in clean]
    n = len(clean)

    # True Straussian Score
    low_ent = [t for t in clean if t["entropy"] < ENTROPY_THRESHOLD]
    true_straussian = (
        sum(1 for t in low_ent if t["s2"] > 0) / len(low_ent)
        if low_ent else 0.0
    )
    frac_low_entropy = len(low_ent) / n

    # Entropy autocorrelation lag-1
    mean_e = sum(entropies) / n
    var_e = sum((e - mean_e) ** 2 for e in entropies) / n
    if var_e < 1e-10:
        ac1 = 0.0
    else:
        cov1 = sum(
            (entropies[i] - mean_e) * (entropies[i + 1] - mean_e)
            for i in range(n - 1)
        ) / (n - 1)
        ac1 = cov1 / var_e

    # S2 volatility (std)
    mean_s2 = sum(s2s) / n
    s2_std = math.sqrt(sum((s - mean_s2) ** 2 for s in s2s) / n)

    # Mean entropy
    mean_entropy = mean_e

    # Entropy autocorrelation lag-2
    if n > 2:
        cov2 = sum(
            (entropies[i] - mean_e) * (entropies[i + 2] - mean_e)
            for i in range(n - 2)
        ) / (n - 2)
        ac2 = cov2 / var_e
    else:
        ac2 = 0.0

    return {
        "ac1": ac1,
        "ac2": ac2,
        "true_straussian": true_straussian,
        "frac_low_entropy": frac_low_entropy,
        "mean_entropy": mean_entropy,
        "mean_s2": mean_s2,
        "s2_std": s2_std,
        "n_tokens": n,
    }


# ─── Compute fingerprints for all poems ──────────────────────────────────────
poems = []
for poem in data:
    meta = poem["metadata"]
    era = meta.get("era", "")
    fp = compute_fingerprint(poem)
    if fp is None:
        continue

    if era in ORAL_ERAS:
        register = "ORAL"
    elif era in LITERARY_ERAS:
        register = "LITERARY"
    else:
        register = "MIXED"

    poems.append({
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "year": meta.get("year"),
        "era": era,
        "register": register,
        **fp,
    })

print(f"Total poems analyzed: {len(poems)}")
by_reg = defaultdict(list)
for p in poems:
    by_reg[p["register"]].append(p)
print(f"  ORAL: {len(by_reg['ORAL'])}, LITERARY: {len(by_reg['LITERARY'])}, MIXED: {len(by_reg['MIXED'])}")

# ─── Cluster statistics ───────────────────────────────────────────────────────
print("\n=== REGISTER CLUSTER STATISTICS ===")
print(f"{'Register':<12} {'n':>4} {'mean_AC1':>10} {'mean_TSS':>10} {'frac_LowH':>10} {'mean_ent':>10}")
print("-" * 60)
for reg in ["ORAL", "MIXED", "LITERARY"]:
    ps = by_reg[reg]
    if not ps:
        continue
    n = len(ps)
    print(f"{reg:<12} {n:>4} "
          f"{sum(p['ac1'] for p in ps)/n:>10.3f} "
          f"{sum(p['true_straussian'] for p in ps)/n:>10.3f} "
          f"{sum(p['frac_low_entropy'] for p in ps)/n:>10.3f} "
          f"{sum(p['mean_entropy'] for p in ps)/n:>10.3f}")

# ─── Define separation boundary ───────────────────────────────────────────────
# Based on oral_literary_register.md:
# Oral: AC1 > 0.15 AND TSS < 0.25 → "oral zone"
# Literary: AC1 < 0.10 AND TSS > 0.26 → "literary zone"
# (these boundaries are data-driven from previous experiment)

AC1_ORAL_THRESH = 0.15
TSS_ORAL_THRESH = 0.25

AC1_LIT_THRESH = 0.10
TSS_LIT_THRESH = 0.26

def classify_zone(ac1, tss):
    if ac1 >= AC1_ORAL_THRESH and tss < TSS_ORAL_THRESH:
        return "oral_zone"
    elif ac1 < AC1_LIT_THRESH and tss >= TSS_LIT_THRESH:
        return "literary_zone"
    elif ac1 >= AC1_ORAL_THRESH and tss >= TSS_LIT_THRESH:
        return "high_ac_high_tss"  # interesting crossover: rhythmic AND lexically deviant
    else:
        return "middle"

for p in poems:
    p["zone"] = classify_zone(p["ac1"], p["true_straussian"])

# ─── Crossover analysis ───────────────────────────────────────────────────────
print("\n=== CROSSOVER POEMS (register ≠ zone) ===")

# Oral poems in the literary zone (lexically deviant despite oral tradition)
oral_in_lit = [p for p in by_reg["ORAL"] if p["zone"] == "literary_zone"]
print(f"\nOral poems scoring as literary (AC1 low, TSS high): {len(oral_in_lit)}")
for p in sorted(oral_in_lit, key=lambda x: x["true_straussian"], reverse=True):
    print(f"  {p['title'][:45]:<45} ({p['era']}) AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

# Literary poems in the oral zone (rhythmic despite literary tradition)
lit_in_oral = [p for p in by_reg["LITERARY"] if p["zone"] == "oral_zone"]
print(f"\nLiterary poems scoring as oral (AC1 high, TSS low): {len(lit_in_oral)}")
for p in sorted(lit_in_oral, key=lambda x: x["ac1"], reverse=True):
    print(f"  {p['title'][:45]:<45} ({p['era']}) AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

# High AC1 + high TSS: The "double deviants" — rhythmic AND lexically unexpected
double_dev = [p for p in poems if p["zone"] == "high_ac_high_tss"]
print(f"\nDouble deviants (rhythmic groove AND lexical deviation): {len(double_dev)}")
for p in sorted(double_dev, key=lambda x: x["ac1"] + x["true_straussian"], reverse=True)[:15]:
    print(f"  {p['title'][:45]:<45} ({p['era']}/{p['register']}) AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

# ─── Zone distribution by register ───────────────────────────────────────────
print("\n=== ZONE DISTRIBUTION BY REGISTER ===")
zones = ["oral_zone", "literary_zone", "high_ac_high_tss", "middle"]
for reg in ["ORAL", "MIXED", "LITERARY"]:
    ps = by_reg[reg]
    if not ps:
        continue
    n = len(ps)
    print(f"\n{reg} (n={n}):")
    for z in zones:
        cnt = sum(1 for p in ps if p["zone"] == z)
        pct = 100 * cnt / n
        print(f"  {z:<20}: {cnt:>3} ({pct:.0f}%)")

# ─── Top 15 poems in each extreme zone ──────────────────────────────────────
print("\n=== TOP ORAL-ZONE POEMS (highest AC1) ===")
oral_zone_all = sorted([p for p in poems if p["zone"] == "oral_zone"],
                       key=lambda x: x["ac1"], reverse=True)
for p in oral_zone_all[:15]:
    print(f"  {p['title'][:40]:<40} {p['register']:<10} AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

print("\n=== TOP LITERARY-ZONE POEMS (highest TSS) ===")
lit_zone_all = sorted([p for p in poems if p["zone"] == "literary_zone"],
                      key=lambda x: x["true_straussian"], reverse=True)
for p in lit_zone_all[:15]:
    print(f"  {p['title'][:40]:<40} {p['register']:<10} TSS={p['true_straussian']:.3f} AC1={p['ac1']:.3f}")

# ─── Centroid distances ───────────────────────────────────────────────────────
oral_ps = by_reg["ORAL"]
lit_ps = by_reg["LITERARY"]

if oral_ps and lit_ps:
    oral_centroid = (
        sum(p["ac1"] for p in oral_ps) / len(oral_ps),
        sum(p["true_straussian"] for p in oral_ps) / len(oral_ps),
    )
    lit_centroid = (
        sum(p["ac1"] for p in lit_ps) / len(lit_ps),
        sum(p["true_straussian"] for p in lit_ps) / len(lit_ps),
    )
    centroid_dist = math.sqrt(
        (oral_centroid[0] - lit_centroid[0]) ** 2 +
        (oral_centroid[1] - lit_centroid[1]) ** 2
    )
    print(f"\n=== CLUSTER CENTROIDS ===")
    print(f"  Oral centroid:    AC1={oral_centroid[0]:.3f}, TSS={oral_centroid[1]:.3f}")
    print(f"  Literary centroid: AC1={lit_centroid[0]:.3f}, TSS={lit_centroid[1]:.3f}")
    print(f"  Euclidean distance: {centroid_dist:.3f}")

    # Distance of each poem from its own centroid vs the other
    print("\n=== MOST MISPLACED ORAL POEMS (closest to literary centroid) ===")
    def dist(p, centroid):
        return math.sqrt((p["ac1"] - centroid[0])**2 + (p["true_straussian"] - centroid[1])**2)

    oral_sorted = sorted(oral_ps, key=lambda p: dist(p, lit_centroid))
    for p in oral_sorted[:8]:
        d_own = dist(p, oral_centroid)
        d_lit = dist(p, lit_centroid)
        print(f"  {p['title'][:40]:<40} d_lit={d_lit:.3f} d_oral={d_own:.3f} AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

    print("\n=== MOST MISPLACED LITERARY POEMS (closest to oral centroid) ===")
    lit_sorted = sorted(lit_ps, key=lambda p: dist(p, oral_centroid))
    for p in lit_sorted[:8]:
        d_own = dist(p, lit_centroid)
        d_oral = dist(p, oral_centroid)
        print(f"  {p['title'][:40]:<40} d_oral={d_oral:.3f} d_lit={d_own:.3f} AC1={p['ac1']:.3f} TSS={p['true_straussian']:.3f}")

# ─── Era-level fingerprints ───────────────────────────────────────────────────
print("\n=== ERA FINGERPRINTS (sorted by AC1) ===")
era_data = defaultdict(list)
for p in poems:
    era_data[p["era"]].append(p)

era_stats = []
for era, ps in era_data.items():
    if len(ps) < 3:
        continue
    n = len(ps)
    reg = "ORAL" if era in ORAL_ERAS else ("LITERARY" if era in LITERARY_ERAS else "MIXED")
    era_stats.append({
        "era": era,
        "register": reg,
        "n": n,
        "mean_ac1": sum(p["ac1"] for p in ps) / n,
        "mean_tss": sum(p["true_straussian"] for p in ps) / n,
        "mean_entropy": sum(p["mean_entropy"] for p in ps) / n,
    })

era_stats.sort(key=lambda x: x["mean_ac1"], reverse=True)
print(f"{'Era':<22} {'Reg':<10} {'n':>4} {'AC1':>8} {'TSS':>8} {'MeanEnt':>9}")
print("-" * 65)
for e in era_stats:
    print(f"{e['era']:<22} {e['register']:<10} {e['n']:>4} {e['mean_ac1']:>8.3f} {e['mean_tss']:>8.3f} {e['mean_entropy']:>9.3f}")

# ─── Save results ─────────────────────────────────────────────────────────────
output = {
    "poems": poems,
    "era_stats": era_stats,
    "oral_centroid": list(oral_centroid) if oral_ps and lit_ps else None,
    "literary_centroid": list(lit_centroid) if oral_ps and lit_ps else None,
    "centroid_distance": centroid_dist if oral_ps and lit_ps else None,
    "thresholds": {
        "ac1_oral": AC1_ORAL_THRESH,
        "tss_oral": TSS_ORAL_THRESH,
        "ac1_lit": AC1_LIT_THRESH,
        "tss_lit": TSS_LIT_THRESH,
    },
}

with open("results/register_fingerprint.json", "w") as f:
    json.dump(output, f, indent=2)

print("\nResults saved to results/register_fingerprint.json")
