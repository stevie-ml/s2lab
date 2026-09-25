"""
Aftermath Entropy: What happens to GPT-2's uncertainty AFTER a high-S₂ token?

When a poet makes an unexpected choice (high S₂), does the surprising token:
  (A) CRYSTALLIZE the context — drop the next token's entropy?
       The surprise is a pivot word that narrows what must follow.
  (B) DISSOLVE the context — raise the next token's entropy?
       The surprise opens new possibility, leaving the model more lost.
  (C) No effect — entropy at t+1 is the same as at control positions.

We measure: delta_H = entropy(t+1) − entropy(t)
at high-S₂ positions vs. control positions.
"""

import json
import statistics
from collections import defaultdict

CORPUS_FILE = "results/corpus_results.json"
SPIKE_THRESHOLD = 3.0   # S₂ threshold for "surprise"
HIGH_SPIKE_THRESHOLD = 6.0
MIN_TOKENS = 20         # Minimum poem length to analyze

data = json.load(open(CORPUS_FILE))

# ── helpers ──────────────────────────────────────────────────────────────────

def aftermath_entropy(poem, spike_threshold):
    """
    For each interior token position in a poem, compute:
      - is_spike: S₂ ≥ threshold
      - delta_H: entropy(t+1) - entropy(t)  (entropy change after this token)
      - s2: current S₂
      - entropy_before: entropy(t)
    Returns list of dicts.
    """
    tokens = poem.get("tokens", [])
    rows = []
    for i in range(len(tokens) - 1):  # need t+1
        t = tokens[i]
        t1 = tokens[i + 1]
        s2 = t.get("s2", 0)
        h_now = t.get("entropy", None)
        h_next = t1.get("entropy", None)
        if h_now is None or h_next is None:
            continue
        rows.append({
            "s2": s2,
            "is_spike": s2 >= spike_threshold,
            "is_high_spike": s2 >= HIGH_SPIKE_THRESHOLD,
            "is_neg": s2 < -spike_threshold,
            "delta_H": h_next - h_now,
            "entropy_before": h_now,
            "entropy_after": h_next,
            "token": t.get("token", ""),
            "token_next": t1.get("token", ""),
            "era": poem["metadata"].get("era", "unknown"),
            "title": poem["metadata"].get("title", ""),
            "author": poem["metadata"].get("author", ""),
        })
    return rows

# ── collect all positions ────────────────────────────────────────────────────

all_rows = []
for poem in data:
    lang = poem["metadata"].get("language", "en")
    if lang != "en":
        continue
    era = poem["metadata"].get("era", "")
    if era == "control":
        continue
    tokens = poem.get("tokens", [])
    if len(tokens) < MIN_TOKENS:
        continue
    all_rows.extend(aftermath_entropy(poem, SPIKE_THRESHOLD))

print(f"\n{'='*60}")
print("AFTERMATH ENTROPY ANALYSIS")
print(f"Total interior positions: {len(all_rows)}")

# ── global comparison: spikes vs control ─────────────────────────────────────

spike_deltas    = [r["delta_H"] for r in all_rows if r["is_spike"]]
hi_spike_deltas = [r["delta_H"] for r in all_rows if r["is_high_spike"]]
neg_deltas      = [r["delta_H"] for r in all_rows if r["is_neg"]]
neutral_deltas  = [r["delta_H"] for r in all_rows if not r["is_spike"] and not r["is_neg"] and abs(r["s2"]) < 1.5]

def stats(deltas):
    if not deltas:
        return dict(n=0, mean=0, median=0, pct_pos=0)
    return dict(
        n=len(deltas),
        mean=round(statistics.mean(deltas), 4),
        median=round(statistics.median(deltas), 4),
        pct_pos=round(100 * sum(1 for d in deltas if d > 0) / len(deltas), 1),
    )

print("\n## Global aftermath entropy (delta_H = H_next - H_now)")
print(f"{'Group':<22} {'n':>7} {'mean delta_H':>13} {'median':>8} {'% H rises':>10}")
print("-" * 65)

groups = [
    ("Spike S₂≥3", spike_deltas),
    ("High spike S₂≥6", hi_spike_deltas),
    ("Negative S₂≤-3", neg_deltas),
    ("Neutral |S₂|<1.5", neutral_deltas),
]
for label, d in groups:
    s = stats(d)
    print(f"{label:<22} {s['n']:>7} {s['mean']:>13.4f} {s['median']:>8.4f} {s['pct_pos']:>9.1f}%")

# ── crystallizers vs dissolvers at spike positions ──────────────────────────

spike_rows = [r for r in all_rows if r["is_spike"]]
crystallizers = [r for r in spike_rows if r["delta_H"] < -0.5]
dissolvers    = [r for r in spike_rows if r["delta_H"] > +0.5]
neutral_spikes = [r for r in spike_rows if abs(r["delta_H"]) <= 0.5]

print(f"\n## Classification at spike positions (S₂ ≥ {SPIKE_THRESHOLD})")
total_sp = len(spike_rows)
print(f"Total spikes analyzed: {total_sp}")
print(f"  Crystallizers (ΔH < −0.5): {len(crystallizers)} ({100*len(crystallizers)/total_sp:.1f}%)")
print(f"  Neutral      (|ΔH| ≤ 0.5): {len(neutral_spikes)} ({100*len(neutral_spikes)/total_sp:.1f}%)")
print(f"  Dissolvers   (ΔH > +0.5):  {len(dissolvers)}  ({100*len(dissolvers)/total_sp:.1f}%)")

print(f"\n  Mean ΔH | crystallizers: {statistics.mean(r['delta_H'] for r in crystallizers):.3f}")
print(f"  Mean ΔH | dissolvers:    {statistics.mean(r['delta_H'] for r in dissolvers):.3f}")
cryst_s2 = statistics.mean(r['s2'] for r in crystallizers)
diss_s2  = statistics.mean(r['s2'] for r in dissolvers)
print(f"\n  Mean S₂ | crystallizers: {cryst_s2:.3f}")
print(f"  Mean S₂ | dissolvers:    {diss_s2:.3f}")

# ── what tokens crystallize vs dissolve? ────────────────────────────────────

from collections import Counter

print("\n## Top 20 crystallizing tokens (spike, ΔH < −0.5)")
cryst_tok = Counter(r["token"].strip().lower() for r in crystallizers if len(r["token"].strip()) > 1)
for tok, cnt in cryst_tok.most_common(20):
    mean_dh = statistics.mean(r["delta_H"] for r in crystallizers if r["token"].strip().lower() == tok)
    print(f"  {tok:<15} n={cnt:>4}  mean ΔH={mean_dh:.3f}")

print("\n## Top 20 dissolving tokens (spike, ΔH > +0.5)")
diss_tok = Counter(r["token"].strip().lower() for r in dissolvers if len(r["token"].strip()) > 1)
for tok, cnt in diss_tok.most_common(20):
    mean_dh = statistics.mean(r["delta_H"] for r in dissolvers if r["token"].strip().lower() == tok)
    print(f"  {tok:<15} n={cnt:>4}  mean ΔH={mean_dh:.3f}")

# ── era breakdown ────────────────────────────────────────────────────────────

print("\n## Aftermath entropy by era")
print(f"{'Era':<22} {'n_spikes':>9} {'mean_dH':>9} {'% cryst':>9} {'% diss':>8}")
print("-" * 60)

era_rows = defaultdict(list)
for r in spike_rows:
    era_rows[r["era"]].append(r)

era_stats = []
for era, rows in era_rows.items():
    if len(rows) < 5:
        continue
    mean_dH = statistics.mean(r["delta_H"] for r in rows)
    pct_cryst = 100 * sum(1 for r in rows if r["delta_H"] < -0.5) / len(rows)
    pct_diss  = 100 * sum(1 for r in rows if r["delta_H"] > +0.5) / len(rows)
    era_stats.append((era, len(rows), mean_dH, pct_cryst, pct_diss))

era_stats.sort(key=lambda x: x[2])  # sort by mean_dH (most crystallizing first)
for era, n, mdh, pc, pd in era_stats:
    print(f"{era:<22} {n:>9} {mdh:>9.4f} {pc:>8.1f}% {pd:>7.1f}%")

# ── does bigger surprise = stronger crystallization? ─────────────────────────

print("\n## S₂ quartiles and aftermath entropy")
s2_vals = sorted(r["s2"] for r in spike_rows)
n = len(s2_vals)
q25, q50, q75 = s2_vals[n//4], s2_vals[n//2], s2_vals[3*n//4]
buckets = {
    f"S₂ 3.0–{q25:.1f}": [r for r in spike_rows if 3.0 <= r["s2"] < q25],
    f"S₂ {q25:.1f}–{q50:.1f}": [r for r in spike_rows if q25 <= r["s2"] < q50],
    f"S₂ {q50:.1f}–{q75:.1f}": [r for r in spike_rows if q50 <= r["s2"] < q75],
    f"S₂ >{q75:.1f}": [r for r in spike_rows if r["s2"] >= q75],
}
print(f"{'Bucket':<25} {'n':>6} {'mean ΔH':>10} {'% cryst':>9} {'% diss':>8}")
print("-" * 60)
for label, rows in buckets.items():
    if not rows:
        continue
    mdH = statistics.mean(r["delta_H"] for r in rows)
    pc  = 100 * sum(1 for r in rows if r["delta_H"] < -0.5) / len(rows)
    pd  = 100 * sum(1 for r in rows if r["delta_H"] > +0.5) / len(rows)
    print(f"{label:<25} {len(rows):>6} {mdH:>10.4f} {pc:>8.1f}% {pd:>7.1f}%")

# ── what follows crystallizers vs dissolvers? ─────────────────────────────

print("\n## Tokens that follow crystallizers vs dissolvers")
print("(What comes after the surprise?)")

cryst_next = Counter(r["token_next"].strip().lower() for r in crystallizers if len(r["token_next"].strip()) > 1)
diss_next  = Counter(r["token_next"].strip().lower() for r in dissolvers  if len(r["token_next"].strip()) > 1)

print("\nTop 15 tokens following crystallizing surprises:")
for tok, cnt in cryst_next.most_common(15):
    print(f"  {tok:<15} {cnt:>4}")

print("\nTop 15 tokens following dissolving surprises:")
for tok, cnt in diss_next.most_common(15):
    print(f"  {tok:<15} {cnt:>4}")

print("\nDone.")
