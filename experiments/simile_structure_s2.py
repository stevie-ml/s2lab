"""
Simile Structure and the Entropy Valley: S₂ before, at, and after explicit simile markers.

Hypothesis: Simile markers ("like", "as") function as "surprise licenses" — they
signal to the reader (and to GPT-2) that an unexpected comparison is coming.
This should produce a characteristic pattern:
  1. Pre-simile: normal S₂
  2. At "like"/"as" (marker): LOW S₂ (model expects the comparison syntax)
  3. Post-marker (vehicle): HIGH entropy, paradoxically LOW S₂ (model is uncertain,
     any comparison object is plausible — poet's choice lands in a wide field)
  4. The "unsaid" at vehicle positions reveals what GPT-2 imagined as "conventional" comparison

Builds on: metaphor_detection_s2.md (which noted that simile vehicles have lower S₂
than implicit metaphor vehicles), straussian_gap_taxonomy.md.

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
from collections import defaultdict

RESULT_PATH = "results/corpus_results.json"

with open(RESULT_PATH) as f:
    corpus = json.load(f)

# ── Simile marker detection ───────────────────────────────────────────────────
# GPT-2 tokenizes with leading spaces: " like", " as"
# We use lowercase normalization.

SIMILE_MARKERS = {" like", "like", " as", "as"}
# We only want simile "like/as", not verbal "like" (I like this) or "as" conjunction.
# Heuristic: exclude if followed by a verb form or if preceded by "I", "they", etc.
VERB_SIGNALS = {
    " to", " it", " them", " him", " her", " you", " me", " us",
    " the", " what", " which", " this", " that", " much", " many",
    " well", " usual", " long", " far", " soon", " good",
}

def normalize(tok):
    return tok.strip().lower()

def is_simile_marker(token, next_token=None, prev_token=None):
    """Heuristic filter to distinguish simile 'like/as' from other uses."""
    n = normalize(token)
    if n not in ("like", "as"):
        return False
    if next_token:
        nn = normalize(next_token)
        # "as well", "as much", "as long" etc. → not simile
        if nn in ("well", "much", "many", "long", "far", "soon", "good",
                  "usual", "usual", "follows", "if", "though", "long"):
            return False
    if prev_token:
        pn = normalize(prev_token)
        # "I like", "they like", "he likes" → verbal
        if pn in ("i", "they", "he", "she", "we", "you", "it"):
            return False
    return True

# ── Main analysis ─────────────────────────────────────────────────────────────

windows = []  # Each: dict with s2 values at positions relative to marker

marker_data = []  # Detailed per-marker data
vehicle_alts = []  # GPT-2's alternatives at vehicle positions

# Global baselines
all_s2 = []
content_s2 = []  # content words (alpha, len >= 3)

for poem in corpus:
    meta = poem["metadata"]
    if meta.get("language", "en") != "en":
        continue
    if meta.get("era") == "control":
        continue

    tokens = poem.get("tokens", [])
    n = len(tokens)
    all_s2.extend(t["s2"] for t in tokens)
    content_s2.extend(
        t["s2"] for t in tokens
        if t["token"].strip().isalpha() and len(t["token"].strip()) >= 3
    )

    for i, tok in enumerate(tokens):
        tn = normalize(tok["token"])
        if tn not in ("like", "as"):
            continue

        prev_tok = tokens[i-1]["token"] if i > 0 else None
        next_tok = tokens[i+1]["token"] if i < n-1 else None

        if not is_simile_marker(tok["token"], next_tok, prev_tok):
            continue

        # Collect window: [−3, −2, −1, 0=marker, +1, +2, +3]
        window = {}
        for offset in range(-3, 4):
            idx = i + offset
            if 0 <= idx < n:
                window[offset] = {
                    "token": tokens[idx]["token"],
                    "s2": tokens[idx]["s2"],
                    "surprisal": tokens[idx]["surprisal"],
                    "entropy": tokens[idx]["entropy"],
                }

        if 0 not in window or 1 not in window:
            continue

        windows.append(window)

        # Vehicle = position +1 (first token after marker)
        vehicle = window.get(1)
        if vehicle:
            vehicle_alts.append({
                "poem": meta["title"],
                "author": meta["author"],
                "marker": tok["token"].strip(),
                "vehicle_token": vehicle["token"],
                "vehicle_s2": vehicle["s2"],
                "vehicle_entropy": vehicle["entropy"],
                "marker_s2": window[0]["s2"],
                "marker_entropy": window[0]["entropy"],
                "pre_s2": window.get(-1, {}).get("s2"),
                "alternatives": tokens[i+1].get("alternatives", [])[:5],
            })

        marker_data.append({
            "poem": meta["title"],
            "author": meta["author"],
            "marker": tok["token"].strip(),
            "window": window,
        })

# ── Aggregate results ─────────────────────────────────────────────────────────

def mean(vals):
    vals = [v for v in vals if v is not None]
    return sum(vals) / len(vals) if vals else float("nan")

def std(vals):
    vals = [v for v in vals if v is not None]
    if len(vals) < 2:
        return float("nan")
    m = mean(vals)
    return (sum((v - m) ** 2 for v in vals) / len(vals)) ** 0.5

n_windows = len(windows)
n_markers = len(marker_data)

# Aggregate by offset
offset_s2 = defaultdict(list)
offset_entropy = defaultdict(list)
offset_surprisal = defaultdict(list)

for w in windows:
    for offset, data in w.items():
        offset_s2[offset].append(data["s2"])
        offset_entropy[offset].append(data["entropy"])
        offset_surprisal[offset].append(data["surprisal"])

baseline_s2 = mean(all_s2)
baseline_content_s2 = mean(content_s2)

# Marker vs vehicle comparison
marker_s2_vals = [v["marker_s2"] for v in vehicle_alts]
vehicle_s2_vals = [v["vehicle_s2"] for v in vehicle_alts]
vehicle_entropy_vals = [v["vehicle_entropy"] for v in vehicle_alts]
marker_entropy_vals = [v["marker_entropy"] for v in vehicle_alts]

# Pre-simile (position -1) vs marker vs vehicle
pre_s2_vals = [v["pre_s2"] for v in vehicle_alts if v["pre_s2"] is not None]

# ── Vehicle alternatives: what did GPT-2 predict? ─────────────────────────────

# Collect all alternative tokens at vehicle positions (pos +1 from marker)
alt_counter = defaultdict(float)
for va in vehicle_alts:
    for alt in va["alternatives"]:
        alt_counter[alt["token"].strip().lower()] += alt["prob"]

top_alts = sorted(alt_counter.items(), key=lambda x: x[1], reverse=True)[:20]

# Like vs As breakdown
like_windows = [v for v in vehicle_alts if v["marker"] == "like"]
as_windows = [v for v in vehicle_alts if v["marker"] == "as"]

# High vs low S₂ vehicles
high_vehicle_s2 = sorted(vehicle_alts, key=lambda v: v["vehicle_s2"], reverse=True)[:10]
low_vehicle_s2 = sorted(vehicle_alts, key=lambda v: v["vehicle_s2"])[:10]

# ── Print results ─────────────────────────────────────────────────────────────

print(f"\n{'='*60}")
print("SIMILE STRUCTURE AND THE ENTROPY VALLEY")
print(f"{'='*60}")
print(f"Poems analyzed: {sum(1 for p in corpus if p['metadata'].get('language','en')=='en' and p['metadata'].get('era')!='control')}")
print(f"Simile markers found: {n_markers}")
print(f"  'like': {sum(1 for v in vehicle_alts if v['marker']=='like')}")
print(f"  'as':   {sum(1 for v in vehicle_alts if v['marker']=='as')}")
print()
print(f"Baseline S₂ (all tokens):        {baseline_s2:.4f}")
print(f"Baseline S₂ (content words ≥3):  {baseline_content_s2:.4f}")
print()

print("─── S₂ profile around simile markers ───")
print(f"{'Offset':>10} {'Token position':>20} {'Mean S₂':>10} {'Mean H':>10} {'n':>6}")
labels = {-3: "t-3 (pre)", -2: "t-2 (pre)", -1: "t-1 (pre)",
           0: "t0 (marker)", 1: "t+1 (vehicle)", 2: "t+2", 3: "t+3"}
for offset in range(-3, 4):
    vals = offset_s2[offset]
    hvs = offset_entropy[offset]
    print(f"{offset:>10}  {labels[offset]:>19}  {mean(vals):>10.4f}  {mean(hvs):>10.4f}  {len(vals):>6}")

print()
print("─── Marker vs. vehicle comparison ───")
print(f"{'Metric':<30} {'like':>10} {'as':>10} {'combined':>10}")
print(f"{'Mean S₂ at marker':<30} {mean([v['marker_s2'] for v in like_windows]):>10.4f} "
      f"{mean([v['marker_s2'] for v in as_windows]):>10.4f} "
      f"{mean(marker_s2_vals):>10.4f}")
print(f"{'Mean S₂ at vehicle (t+1)':<30} {mean([v['vehicle_s2'] for v in like_windows]):>10.4f} "
      f"{mean([v['vehicle_s2'] for v in as_windows]):>10.4f} "
      f"{mean(vehicle_s2_vals):>10.4f}")
print(f"{'Mean H at marker':<30} {mean([v['marker_entropy'] for v in like_windows]):>10.4f} "
      f"{mean([v['marker_entropy'] for v in as_windows]):>10.4f} "
      f"{mean(marker_entropy_vals):>10.4f}")
print(f"{'Mean H at vehicle (t+1)':<30} {mean([v['vehicle_entropy'] for v in like_windows]):>10.4f} "
      f"{mean([v['vehicle_entropy'] for v in as_windows]):>10.4f} "
      f"{mean(vehicle_entropy_vals):>10.4f}")
print(f"{'Mean S₂ pre-marker (t-1)':<30} {'':>10} {'':>10} {mean(pre_s2_vals):>10.4f}")

print()
print("─── Δ S₂ relative to corpus baseline ───")
print(f"  At marker (t0):       {mean(marker_s2_vals) - baseline_s2:+.4f}")
print(f"  At vehicle (t+1):     {mean(vehicle_s2_vals) - baseline_s2:+.4f}")
print(f"  Pre-marker (t-1):     {mean(pre_s2_vals) - baseline_s2:+.4f}")

print()
print("─── GPT-2's top predicted tokens at vehicle positions ───")
print("(What GPT-2 imagined as 'conventional' comparison objects)")
for tok, prob in top_alts[:15]:
    print(f"  {tok!r:>15}  {prob:.3f}")

print()
print("─── Highest S₂ vehicles (most surprising comparisons) ───")
for v in high_vehicle_s2:
    pre = f"...{v['marker']} {v['vehicle_token'].strip()}"
    print(f"  S₂={v['vehicle_s2']:+.2f}  {pre:<30}  — {v['author']}, \"{v['poem']}\"")

print()
print("─── Lowest S₂ vehicles (most expected comparisons) ───")
for v in low_vehicle_s2:
    pre = f"...{v['marker']} {v['vehicle_token'].strip()}"
    print(f"  S₂={v['vehicle_s2']:+.2f}  {pre:<30}  — {v['author']}, \"{v['poem']}\"")
