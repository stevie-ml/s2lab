"""
Biblical Parallelism and S2: Does the Second Hemistich Pay an Informational Discount?

In classical Hebrew poetry, every verse is composed of two (sometimes three) parallel
halves — the hemistich. The second hemistich restates, contrasts, or completes the first
(synonymic, antithetic, and synthetic parallelism respectively). After the first hemistich,
GPT-2 has a strong contextual prior about what the second will say. The hypothesis:

  H1 — The second hemistich has lower mean S2 than the first (informational discount:
       the parallelistic expectation makes the second half more predictable).

  H2 — The second hemistich has HIGHER S2 than the first (violation premium: the poet
       deliberately chooses different words for the same meaning, which the model doesn't
       expect — it would just repeat the first hemistich).

We also compare biblical texts against the broader poetry corpus and prose controls,
and examine the concrete poetry additions (extreme repetition) as a limit case.
"""

import json
import os
import re

RESULTS = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")

with open(RESULTS) as f:
    data = json.load(f)

# ── 1. Collect all texts ──────────────────────────────────────────────────────
def era(d):
    return d.get("metadata", {}).get("era") or d.get("era", "")

def get_title(d):
    return d.get("metadata", {}).get("title") or d.get("title", "")

biblical_poems = [d for d in data if era(d) == "biblical"]
concrete_poems = [d for d in data if era(d) == "concrete"]
control_poems  = [d for d in data if era(d) == "control"]
all_poetry     = [d for d in data if era(d) not in ("control", "biblical", "concrete")]

def artifact_free(tokens):
    """Remove stanza-break artifact tokens (top predicted = newline, prob > 0.9)."""
    clean = []
    for t in tokens:
        alts = t.get("alternatives", [])
        if alts:
            top_tok, top_p = alts[0]["token"], alts[0]["prob"]
            if top_tok.strip("\n\r") == "" and top_p > 0.9:
                continue
        clean.append(t)
    return clean

def mean_s2(tokens):
    vals = [t["s2"] for t in tokens if t.get("s2") is not None]
    return sum(vals) / len(vals) if vals else None

def pos_pct(tokens):
    vals = [t["s2"] for t in tokens if t.get("s2") is not None]
    return sum(1 for v in vals if v > 0) / len(vals) if vals else 0

# ── 2. Overall comparison: biblical vs. poetry vs. concrete vs. prose ─────────
groups = {
    "biblical (n=7)":  biblical_poems,
    "concrete (n=3)":  concrete_poems,
    "poetry corpus":   all_poetry,
    "prose control":   control_poems,
}

print("=" * 70)
print("GROUP-LEVEL S2 COMPARISON")
print("=" * 70)
print(f"{'Group':<22} {'n':>4} {'Avg S2':>8} {'Pos%':>6} {'Max S2':>8}")
print("-" * 50)
for label, group in groups.items():
    all_tokens = []
    for poem in group:
        toks = artifact_free(poem.get("tokens", []))
        all_tokens.extend(toks)
    if all_tokens:
        vals = [t["s2"] for t in all_tokens if t.get("s2") is not None]
        avg = sum(vals) / len(vals)
        pos = sum(1 for v in vals if v > 0) / len(vals) * 100
        mx  = max(vals)
        print(f"{label:<22} {len(group):>4} {avg:>8.3f} {pos:>5.1f}% {mx:>8.2f}")
    else:
        print(f"{label:<22} {len(group):>4}      N/A    N/A      N/A")

# ── 3. Per-biblical-poem breakdown ───────────────────────────────────────────
print()
print("=" * 70)
print("BIBLICAL TEXTS — PER-POEM ANALYSIS")
print("=" * 70)
print(f"{'Title':<40} {'Avg S2':>8} {'Pos%':>6} {'Max S2':>8}")
print("-" * 65)
for poem in biblical_poems:
    toks = artifact_free(poem.get("tokens", []))
    ms = mean_s2(toks)
    pp = pos_pct(toks) * 100
    vals = [t["s2"] for t in toks if t.get("s2") is not None]
    mx = max(vals) if vals else 0
    ttl = get_title(poem)[:40]
    print(f"{ttl:<40} {ms:>8.3f} {pp:>5.1f}% {mx:>8.2f}")

# ── 4. Hemistich Analysis — first vs. second half of each verse ──────────────
# Verse boundaries = ';' or ':' (KJV verse-internal), '.' or '\n' (verse end)
# We split each verse at ';' or ':' to isolate first vs. second hemistich.

def split_at_semicolons(tokens):
    """
    Return list of (hemistich_index, token) pairs.
    hemistich_index 0 = odd (first), 1 = even (second).
    """
    result = []
    idx = 0  # 0-based hemistich counter per verse-line
    in_line = 0  # hemistich counter within current verse line
    for t in tokens:
        surface = t.get("token", "")
        result.append((in_line % 2, t))
        # semicolon or colon is the hemistich boundary in KJV parallelism
        if ";" in surface or ((":" in surface) and surface.strip() == ":"):
            in_line += 1
        # newline resets to 0 (new verse)
        if "\n" in surface:
            in_line = 0
    return result

print()
print("=" * 70)
print("HEMISTICH ANALYSIS — First vs. Second Half of Parallel Verses")
print("=" * 70)
print("(Splitting on semicolons / colons as verse-internal boundaries)")
print()

first_all, second_all = [], []
poem_rows = []
for poem in biblical_poems:
    toks = artifact_free(poem.get("tokens", []))
    labeled = split_at_semicolons(toks)
    first  = [t for (h, t) in labeled if h == 0]
    second = [t for (h, t) in labeled if h == 1]
    ms1 = mean_s2(first)
    ms2 = mean_s2(second)
    delta = (ms2 - ms1) if (ms1 is not None and ms2 is not None) else None
    poem_rows.append((get_title(poem)[:38], ms1, ms2, delta,
                      len(first), len(second)))
    first_all.extend(first)
    second_all.extend(second)

print(f"{'Title':<38} {'H1 S2':>7} {'H2 S2':>7} {'Δ':>7} {'n1':>5} {'n2':>5}")
print("-" * 68)
for (ptitle, ms1, ms2, delta, n1, n2) in poem_rows:
    d_str = f"{delta:+.3f}" if delta is not None else "  N/A"
    print(f"{ptitle:<38} {ms1:>7.3f} {ms2:>7.3f} {d_str:>7} {n1:>5} {n2:>5}")

# Aggregate
ms1_agg = mean_s2(first_all)
ms2_agg = mean_s2(second_all)
delta_agg = ms2_agg - ms1_agg if (ms1_agg is not None and ms2_agg is not None) else None
print("-" * 68)
if ms1_agg is not None and ms2_agg is not None and delta_agg is not None:
    print(f"{'AGGREGATE':<38} {ms1_agg:>7.3f} {ms2_agg:>7.3f} {delta_agg:>+7.3f} "
          f"{len(first_all):>5} {len(second_all):>5}")
else:
    print(f"{'AGGREGATE':<38}     N/A     N/A     N/A {len(first_all):>5} {len(second_all):>5}")

# ── 5. Concrete poetry analysis ───────────────────────────────────────────────
print()
print("=" * 70)
print("CONCRETE POETRY — Extreme Repetition Limit Case")
print("=" * 70)
print(f"{'Title':<35} {'Avg S2':>8} {'Pos%':>6} {'n':>5} {'Max S2':>8}")
print("-" * 60)
for poem in concrete_poems:
    toks = artifact_free(poem.get("tokens", []))
    ms = mean_s2(toks)
    pp = pos_pct(toks) * 100
    n  = len([t for t in toks if t.get("s2") is not None])
    vals = [t["s2"] for t in toks if t.get("s2") is not None]
    mx = max(vals) if vals else 0
    print(f"{get_title(poem)[:35]:<35} {ms:>8.3f} {pp:>5.1f}% {n:>5} {mx:>8.2f}")

# ── 6. Top high-S2 moments in biblical texts ─────────────────────────────────
print()
print("=" * 70)
print("TOP 15 HIGH-S2 MOMENTS IN BIBLICAL TEXTS")
print("=" * 70)
print(f"{'S2':>6}  {'Token':>12}  {'Top Predicted':>14}  {'P(pred)':>8}  Poem")
print("-" * 80)

spikes = []
for poem in biblical_poems:
    toks = artifact_free(poem.get("tokens", []))
    for t in toks:
        s2 = t.get("s2")
        if s2 is None:
            continue
        alts = t.get("alternatives", [])
        top_pred = alts[0]["token"] if alts else "?"
        top_p    = alts[0]["prob"] if alts else 0.0
        spikes.append((s2, t.get("token", "?"), top_pred, top_p, get_title(poem)[:30]))

spikes.sort(reverse=True)
for s2, tok, pred, prob, title in spikes[:15]:
    tok_display  = repr(tok)[:12]
    pred_display = repr(pred)[:14]
    print(f"{s2:>6.2f}  {tok_display:>12}  {pred_display:>14}  {prob:>8.4f}  {title}")

# ── 7. Synonymic parallelism examples — side by side ─────────────────────────
# Show token-level S2 for Psalm 23 to illustrate the hemistich rhythm
print()
print("=" * 70)
print("PSALM 23 — TOKEN-LEVEL S2 (First 40 clean tokens)")
print("=" * 70)
ps23 = next((d for d in biblical_poems if "Psalm 23" in get_title(d)), None)
if ps23:
    toks = artifact_free(ps23.get("tokens", []))
    for t in toks[:40]:
        bar_len = max(0, int((t.get("s2", 0) + 5) * 2))
        bar     = "#" * min(bar_len, 30)
        print(f"  {t.get('token',''):>14}  S2={t.get('s2',0):>6.2f}  {bar}")
