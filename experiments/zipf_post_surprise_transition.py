"""
Zipf Regime Transitions After Surprise

After a poet makes an unexpected choice (high S2 token), does the model's
probability distribution at the NEXT position become:
  (a) MORE concentrated  (hyper-Zipf: model re-anchored, now confident)
  (b) LESS concentrated  (sub-Zipf: model disoriented, now uncertain)

This reveals the structural aftermath of surprise:
- "Anchoring" surprise: choosing X narrows what can follow → model concentrates
- "Liberating" surprise: choosing X opens multiple paths → model diffuses

We analyze:
1. Mean Zipf alpha at position i+1 conditioned on S2 at position i
2. Transition matrix: Zipf class at i → Zipf class at i+1
3. Era-level breakdown: which traditions produce anchoring vs liberating surprises
4. S2 magnitude gradient: does bigger surprise produce bigger concentration change?
"""

import json
import math
import statistics
from collections import defaultdict

# --- Zipf utilities (same as zipf_prediction_coefficient.py) ---

def fit_zipf_exponent(probs):
    if len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    if len(normed) < 2:
        return None
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

def classify_zipf(alpha):
    if alpha is None:
        return None
    if alpha >= 2.5:
        return "hyper_zipf"
    elif alpha >= 1.5:
        return "super_zipf"
    elif alpha >= 0.8:
        return "near_zipf"
    elif alpha >= 0.3:
        return "sub_zipf"
    else:
        return "anti_zipf"

ZIPF_ORDER = ["hyper_zipf", "super_zipf", "near_zipf", "sub_zipf", "anti_zipf"]
S2_HIGH_THRESHOLD = 2.0  # positive S2 ≥ 2 = high surprise
P_NEWLINE_MAX = 0.9       # artifact filter

# --- Load corpus ---
print("Loading corpus_results.json...")
with open("results/corpus_results.json") as f:
    corpus = json.load(f)

print(f"  {len(corpus)} texts loaded")

# --- Per-token computation ---
# For each pair of consecutive non-artifact tokens, record:
#   (S2 at i, Zipf alpha at i, Zipf alpha at i+1, era)

records = []  # (s2_i, alpha_i, alpha_next, era)

n_total = 0
n_filtered = 0

for poem in corpus:
    if poem["metadata"].get("language", "en") not in ("en", "english"):
        continue
    if poem["metadata"].get("era") in ("prose_control", "prose"):
        continue

    era = poem["metadata"].get("era", "unknown")
    tokens = poem["tokens"]

    # Build list of valid (non-artifact) tokens with their alpha
    valid = []
    for tok in tokens:
        n_total += 1
        if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
            n_filtered += 1
            continue
        alts = tok.get("alternatives", [])
        probs = [a["prob"] for a in alts]
        alpha = fit_zipf_exponent(probs)
        s2 = tok.get("s2", None)
        if s2 is None or alpha is None:
            continue
        valid.append({"s2": s2, "alpha": alpha, "era": era, "token": tok["token"]})

    # Build consecutive pairs
    for i in range(len(valid) - 1):
        cur = valid[i]
        nxt = valid[i + 1]
        records.append({
            "s2": cur["s2"],
            "alpha_cur": cur["alpha"],
            "alpha_next": nxt["alpha"],
            "era": cur["era"],
        })

print(f"  {n_total} raw tokens, {n_filtered} artifact-filtered")
print(f"  {len(records)} consecutive pairs analyzed")

# --- Analysis 1: Conditional Zipf alpha at i+1 by S2 category at i ---

def s2_bucket(s2):
    if s2 < -3:
        return "very_neg (<-3)"
    elif s2 < 0:
        return "neg (-3–0)"
    elif s2 < 2:
        return "low_pos (0–2)"
    elif s2 < 5:
        return "high_pos (2–5)"
    else:
        return "extreme (≥5)"

BUCKET_ORDER = ["very_neg (<-3)", "neg (-3–0)", "low_pos (0–2)", "high_pos (2–5)", "extreme (≥5)"]

by_bucket = defaultdict(list)
for r in records:
    by_bucket[s2_bucket(r["s2"])].append(r["alpha_next"])

print("\n=== Analysis 1: Mean Zipf Alpha at i+1 by S2 Bucket at i ===")
bucket_summary = {}
for b in BUCKET_ORDER:
    vals = by_bucket[b]
    if not vals:
        continue
    mn = statistics.mean(vals)
    std = statistics.stdev(vals) if len(vals) > 1 else 0
    pct_hyper = sum(1 for v in vals if v >= 2.5) / len(vals) * 100
    pct_sub = sum(1 for v in vals if v < 0.8) / len(vals) * 100
    bucket_summary[b] = {
        "n": len(vals),
        "mean_alpha_next": round(mn, 3),
        "std": round(std, 3),
        "pct_hyper_next": round(pct_hyper, 1),
        "pct_sub_next": round(pct_sub, 1),
    }
    print(f"  {b}: n={len(vals)}, mean_alpha_next={mn:.3f}, pct_hyper={pct_hyper:.1f}%, pct_sub={pct_sub:.1f}%")

# --- Analysis 2: Zipf transition matrix ---

print("\n=== Analysis 2: Zipf Regime Transition Matrix ===")
transitions = defaultdict(lambda: defaultdict(int))
for r in records:
    cls_cur = classify_zipf(r["alpha_cur"])
    cls_next = classify_zipf(r["alpha_next"])
    if cls_cur and cls_next:
        transitions[cls_cur][cls_next] += 1

# Normalize rows
transition_matrix = {}
for cls_cur in ZIPF_ORDER:
    row = transitions[cls_cur]
    total = sum(row.values())
    if total == 0:
        continue
    transition_matrix[cls_cur] = {
        cls_next: round(row[cls_next] / total * 100, 1)
        for cls_next in ZIPF_ORDER
    }
    print(f"  {cls_cur}: " + " | ".join(
        f"{c}: {transition_matrix[cls_cur].get(c, 0.0):.1f}%"
        for c in ZIPF_ORDER
    ))

# --- Analysis 3: Delta alpha after surprise (high S2 vs low S2) ---

print("\n=== Analysis 3: Delta Alpha = alpha(i+1) - alpha(i) ===")
delta_by_bucket = defaultdict(list)
for r in records:
    delta = r["alpha_next"] - r["alpha_cur"]
    delta_by_bucket[s2_bucket(r["s2"])].append(delta)

delta_summary = {}
for b in BUCKET_ORDER:
    vals = delta_by_bucket[b]
    if not vals:
        continue
    mn = statistics.mean(vals)
    pct_up = sum(1 for v in vals if v > 0.5) / len(vals) * 100
    pct_down = sum(1 for v in vals if v < -0.5) / len(vals) * 100
    delta_summary[b] = {
        "n": len(vals),
        "mean_delta": round(mn, 3),
        "pct_concentrate": round(pct_up, 1),
        "pct_diffuse": round(pct_down, 1),
    }
    print(f"  {b}: n={len(vals)}, mean_delta={mn:.3f}, "
          f"concentrate={pct_up:.1f}%, diffuse={pct_down:.1f}%")

# --- Analysis 4: Era-level breakdown ---

print("\n=== Analysis 4: Era-Level Anchoring vs Liberation ===")
era_data = defaultdict(lambda: {"n": 0, "delta": [], "s2_high": 0})
for r in records:
    if r["s2"] >= S2_HIGH_THRESHOLD:
        era_data[r["era"]]["delta"].append(r["alpha_next"] - r["alpha_cur"])
        era_data[r["era"]]["n"] += 1
        era_data[r["era"]]["s2_high"] += 1

era_summary = {}
for era, d in era_data.items():
    if d["n"] < 20:
        continue
    mn_delta = statistics.mean(d["delta"])
    pct_anchor = sum(1 for v in d["delta"] if v > 0.5) / len(d["delta"]) * 100
    pct_lib = sum(1 for v in d["delta"] if v < -0.5) / len(d["delta"]) * 100
    era_summary[era] = {
        "n": d["n"],
        "mean_delta_alpha": round(mn_delta, 3),
        "pct_anchoring": round(pct_anchor, 1),
        "pct_liberating": round(pct_lib, 1),
    }

# Sort by mean_delta_alpha
sorted_eras = sorted(era_summary.items(), key=lambda x: -x[1]["mean_delta_alpha"])
print(f"  {'Era':<25} {'n':>6} {'delta_α':>8} {'anchor%':>8} {'liberate%':>10}")
for era, s in sorted_eras:
    print(f"  {era:<25} {s['n']:>6} {s['mean_delta_alpha']:>8.3f} "
          f"{s['pct_anchoring']:>8.1f} {s['pct_liberating']:>10.1f}")

# --- Save results ---
results = {
    "n_pairs": len(records),
    "s2_threshold": S2_HIGH_THRESHOLD,
    "bucket_summary": bucket_summary,
    "transition_matrix": transition_matrix,
    "delta_summary": delta_summary,
    "era_summary": era_summary,
}

with open("results/zipf_post_surprise_transition.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/zipf_post_surprise_transition.json")
