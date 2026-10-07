"""
Oral vs. Literary Register: Rhythmic Conformity vs. Lexical Deviation

Research question: Do oral-tradition poems (ballads, spoken word, song lyrics, nursery
rhymes) achieve their emotional effects through rhythmic predictability rather than
lexical deviation? Does the information-theoretic profile distinguish these registers?

Builds on: entropy_conditioned_deviation.md (True Straussian Score)
"""

import json
import sys
import math
from collections import defaultdict

# Load corpus results
with open("results/corpus_results.json") as f:
    data = json.load(f)

# ─── Register classification ─────────────────────────────────────────────────
# ORAL: traditions that prioritize spoken/performed delivery
# LITERARY: traditions that prioritize written/page reading

ORAL_ERAS = {
    "ballad", "spoken_word", "song_lyrics", "nursery_rhyme",
    "biblical",  # psalms, Psalms: chanted/sung oral tradition
}

LITERARY_ERAS = {
    "modernist", "language", "metaphysical",
    "new_york_school", "imagist",
    "surrealist", "oulipo",
}

# Contextual middle ground (excluded from primary comparison but analyzed separately)
MIXED_ERAS = {
    "romantic", "victorian", "19th_century", "confessional",
    "contemporary", "harlem_renaissance", "prose_poetry", "beat",
    "fixed_form", "early_modern", "found_poetry", "haiku",
    "mid_century", "deep_image", "concrete", "black_arts",
    "latin_american", "german_symbolist", "german_modernist",
    "german_expressionist", "ancient", "korean_modernist",
}

ENTROPY_THRESHOLD = 5.0  # "confident" model below this

def compute_register_profile(poem_data):
    """Compute information-theoretic register profile for a poem."""
    tokens = poem_data["tokens"]

    # Filter out stanza-break artifact (p_newline > 0.5)
    clean_tokens = [t for t in tokens if t.get("p_newline", 0) <= 0.5]

    if len(clean_tokens) < 10:
        return None

    entropies = [t["entropy"] for t in clean_tokens]
    s2s = [t["s2"] for t in clean_tokens]

    n = len(clean_tokens)

    # 1. Basic S2 stats
    mean_s2 = sum(s2s) / n
    pos_s2_ratio = sum(1 for s in s2s if s > 0) / n

    # 2. True Straussian Score (fraction of low-entropy tokens with S2 > 0)
    low_ent_tokens = [t for t in clean_tokens if t["entropy"] < ENTROPY_THRESHOLD]
    if low_ent_tokens:
        true_straussian = sum(1 for t in low_ent_tokens if t["s2"] > 0) / len(low_ent_tokens)
    else:
        true_straussian = 0.0
    n_low_entropy = len(low_ent_tokens)
    frac_low_entropy = n_low_entropy / n

    # 3. Entropy volatility (std of entropy values)
    mean_ent = sum(entropies) / n
    entropy_volatility = math.sqrt(sum((e - mean_ent)**2 for e in entropies) / n)

    # 4. Entropy autocorrelation at lag 1, 2, 3
    def autocorr(vals, lag):
        n_ = len(vals)
        if n_ <= lag:
            return 0.0
        m = sum(vals) / n_
        var = sum((v - m)**2 for v in vals)
        if var == 0:
            return 0.0
        cov = sum((vals[i] - m) * (vals[i-lag] - m) for i in range(lag, n_))
        return cov / var

    ent_autocorr1 = autocorr(entropies, 1)
    ent_autocorr2 = autocorr(entropies, 2)
    ent_autocorr3 = autocorr(entropies, 3)

    # 5. "Rhythmic regularity" proxy: fraction of tokens in HIGH-confidence zone
    frac_very_low_ent = sum(1 for e in entropies if e < 3.0) / n  # model very confident

    # 6. S2 volatility (how spiky is the S2 profile)
    mean_s2_ = sum(s2s) / n
    s2_std = math.sqrt(sum((s - mean_s2_)**2 for s in s2s) / n)

    # 7. "Oral paradox" ratio: deviation rate in low vs high entropy contexts
    high_ent_tokens = [t for t in clean_tokens if t["entropy"] >= ENTROPY_THRESHOLD]
    if high_ent_tokens:
        uncertainty_exploit = sum(1 for t in high_ent_tokens if t["s2"] > 0) / len(high_ent_tokens)
    else:
        uncertainty_exploit = 0.0

    # TS Gap: True Straussian vs Uncertainty Exploitation
    ts_gap = true_straussian - uncertainty_exploit

    # 8. Recovery rate: after a high-S2 spike, how quickly does entropy return to baseline?
    # Compute average entropy in positions 1,2,3,4 after any S2 > 3.0 spike
    spikes = [i for i, t in enumerate(clean_tokens) if t["s2"] > 3.0]
    recovery_1 = []
    recovery_3 = []
    for idx in spikes:
        if idx + 1 < n:
            recovery_1.append(entropies[idx + 1])
        if idx + 3 < n:
            recovery_3.append(entropies[idx + 3])

    entropy_recovery_1 = sum(recovery_1)/len(recovery_1) if recovery_1 else mean_ent
    entropy_recovery_3 = sum(recovery_3)/len(recovery_3) if recovery_3 else mean_ent
    recovery_speed = entropy_recovery_1 - entropy_recovery_3  # positive = faster recovery

    return {
        "title": poem_data["metadata"]["title"],
        "author": poem_data["metadata"]["author"],
        "era": poem_data["metadata"]["era"],
        "n_tokens": n,
        "n_low_entropy": n_low_entropy,
        # Core metrics
        "mean_s2": mean_s2,
        "pos_s2_ratio": pos_s2_ratio,
        "true_straussian": true_straussian,
        "uncertainty_exploit": uncertainty_exploit,
        "ts_gap": ts_gap,
        # Entropy structure
        "mean_entropy": mean_ent,
        "entropy_volatility": entropy_volatility,
        "frac_low_entropy": frac_low_entropy,
        "frac_very_low_entropy": frac_very_low_ent,
        "ent_autocorr1": ent_autocorr1,
        "ent_autocorr2": ent_autocorr2,
        "ent_autocorr3": ent_autocorr3,
        # S2 structure
        "s2_std": s2_std,
        # Recovery
        "entropy_recovery_speed": recovery_speed,
        "n_spikes": len(spikes),
    }


# ─── Compute profiles for all poems ─────────────────────────────────────────
all_profiles = []
for poem_data in data:
    era = poem_data["metadata"]["era"]
    if era in {"control", "cliche_control"}:
        continue
    profile = compute_register_profile(poem_data)
    if profile:
        all_profiles.append(profile)

# ─── Group by register ────────────────────────────────────────────────────────
oral_profiles = [p for p in all_profiles if p["era"] in ORAL_ERAS]
literary_profiles = [p for p in all_profiles if p["era"] in LITERARY_ERAS]
mixed_profiles = [p for p in all_profiles if p["era"] in MIXED_ERAS]

def avg(lst, key):
    vals = [p[key] for p in lst if p[key] is not None]
    return sum(vals) / len(vals) if vals else 0.0

def fmt(v, digits=3):
    return round(v, digits)

# ─── Summary statistics ────────────────────────────────────────────────────────
METRICS = [
    ("mean_s2", "Mean S2"),
    ("pos_s2_ratio", "Pos-S2 ratio"),
    ("true_straussian", "True Straussian"),
    ("uncertainty_exploit", "Uncertainty Exploit"),
    ("ts_gap", "TS Gap"),
    ("mean_entropy", "Mean Entropy"),
    ("entropy_volatility", "Entropy Volatility"),
    ("frac_low_entropy", "Frac Low-Entropy"),
    ("frac_very_low_entropy", "Frac Very-Low-Entropy"),
    ("ent_autocorr1", "Entropy Autocorr (lag-1)"),
    ("s2_std", "S2 Std Dev"),
    ("entropy_recovery_speed", "Spike Recovery Speed"),
]

print("\n=== ORAL vs LITERARY REGISTER ANALYSIS ===")
print(f"Oral poems (n={len(oral_profiles)}): {', '.join(ORAL_ERAS)}")
print(f"Literary poems (n={len(literary_profiles)}): {', '.join(LITERARY_ERAS)}")

print("\n--- Core Metrics by Register ---")
print(f"{'Metric':<30} {'ORAL':>10} {'MIXED':>10} {'LITERARY':>10} {'L-O diff':>10}")
for key, label in METRICS:
    o = avg(oral_profiles, key)
    m = avg(mixed_profiles, key)
    l = avg(literary_profiles, key)
    print(f"  {label:<28} {fmt(o):>10} {fmt(m):>10} {fmt(l):>10} {fmt(l-o):>10}")

# ─── Era-level breakdown ──────────────────────────────────────────────────────
era_stats = defaultdict(list)
for p in all_profiles:
    era_stats[p["era"]].append(p)

print("\n\n--- Era Rankings by True Straussian Score ---")
era_rows = []
for era, plist in era_stats.items():
    if len(plist) < 2:
        continue
    register = "ORAL" if era in ORAL_ERAS else ("LITERARY" if era in LITERARY_ERAS else "MIXED")
    era_rows.append({
        "era": era,
        "n": len(plist),
        "register": register,
        "true_straussian": avg(plist, "true_straussian"),
        "mean_s2": avg(plist, "mean_s2"),
        "entropy_volatility": avg(plist, "entropy_volatility"),
        "frac_low_entropy": avg(plist, "frac_low_entropy"),
        "ts_gap": avg(plist, "ts_gap"),
        "ent_autocorr1": avg(plist, "ent_autocorr1"),
    })

era_rows.sort(key=lambda x: x["true_straussian"], reverse=True)
print(f"\n{'Era':<20} {'Reg':>8} {'N':>3} {'TrueStr':>9} {'MeanS2':>8} {'EntVol':>8} {'LowEnt%':>8} {'TSGap':>8} {'EntAC1':>8}")
for r in era_rows:
    print(f"  {r['era']:<18} {r['register']:>8} {r['n']:>3} {fmt(r['true_straussian']):>9} "
          f"{fmt(r['mean_s2']):>8} {fmt(r['entropy_volatility']):>8} "
          f"{fmt(r['frac_low_entropy']):>8} {fmt(r['ts_gap']):>8} {fmt(r['ent_autocorr1']):>8}")

# ─── Individual poem rankings within oral ────────────────────────────────────
print("\n\n--- Oral Tradition Poems Ranked by True Straussian Score ---")
oral_sorted = sorted(oral_profiles, key=lambda x: x["true_straussian"], reverse=True)
print(f"{'Poem':<45} {'Era':<12} {'TrueStr':>9} {'MeanS2':>8} {'EntVol':>8} {'TSGap':>8}")
for p in oral_sorted:
    title = p["title"][:43]
    print(f"  {title:<45} {p['era']:<12} {fmt(p['true_straussian']):>9} "
          f"{fmt(p['mean_s2']):>8} {fmt(p['entropy_volatility']):>8} {fmt(p['ts_gap']):>8}")

# ─── The "Oral Paradox" analysis ──────────────────────────────────────────────
print("\n\n--- The Oral Paradox: Entropy Structure ---")
print("Do oral poems have different entropy autocorrelation? (Rhythmic regularity → predictable entropy rhythm)")
print(f"\n{'Register':<12} {'N':>4} {'EntAC1':>8} {'EntAC2':>8} {'EntAC3':>8} {'FracLowH':>10} {'SpikeRecov':>12}")
for label, plist in [("ORAL", oral_profiles), ("MIXED", mixed_profiles), ("LITERARY", literary_profiles)]:
    print(f"  {label:<12} {len(plist):>4} "
          f"{fmt(avg(plist,'ent_autocorr1')):>8} "
          f"{fmt(avg(plist,'ent_autocorr2')):>8} "
          f"{fmt(avg(plist,'ent_autocorr3')):>8} "
          f"{fmt(avg(plist,'frac_low_entropy')):>10} "
          f"{fmt(avg(plist,'entropy_recovery_speed')):>12}")

# ─── Save results ─────────────────────────────────────────────────────────────
out = {
    "oral_summary": {k: fmt(avg(oral_profiles, k)) for k, _ in METRICS},
    "literary_summary": {k: fmt(avg(literary_profiles, k)) for k, _ in METRICS},
    "mixed_summary": {k: fmt(avg(mixed_profiles, k)) for k, _ in METRICS},
    "era_breakdown": era_rows,
    "oral_poems": oral_profiles,
    "literary_poems": literary_profiles,
}

with open("results/oral_literary_register.json", "w") as f:
    json.dump(out, f, indent=2)

print("\n\nResults saved to results/oral_literary_register.json")
