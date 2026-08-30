"""
Repetition and Entropy: Does the 'Straussian Gap' collapse at repeated phrases?

Hypothesis: In poems with anaphora/refrain, S₂ should be high at the FIRST
occurrence of a repeated phrase (surprising choice) but lower at subsequent
occurrences (model learns the pattern from context → lower entropy → lower S₂).

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import re
from collections import defaultdict

STOP_TOKENS = {'\n', ',', '.', '!', '?', ';', ':', '-', '–', '—',
               ' the', ' a', ' an', ' and', ' of', ' in', ' to', ' is',
               ' was', ' are', ' were', ' be', ' been', ' have', ' has',
               ' it', ' its', ' this', ' that', ' as', ' at', ' by',
               ' for', ' on', ' with', ' or', ' but', ' not', ' so',
               ' my', ' your', ' his', ' her', ' their', ' our',
               "'s", "'ve", "'re", "'t", " I"}

with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# ── 1. GLOBAL: first vs. repeat occurrence across ALL poems ──────────────────
first_s2 = []
repeat_s2 = []
repeat_examples = []  # (author, title, token, first_s2, repeat_s2, position)

for poem in corpus:
    meta = poem["metadata"]
    if meta.get("era") == "control":
        continue
    tokens = poem["tokens"]
    seen = {}  # token → (first_position, first_s2)
    for t in tokens:
        tok = t["token"].strip().lower()
        if len(tok) < 2 or tok in {w.strip().lower() for w in STOP_TOKENS}:
            continue
        pos = t["position"]
        s2 = t["s2"]
        if tok not in seen:
            seen[tok] = (pos, s2)
            first_s2.append(s2)
        else:
            repeat_s2.append(s2)
            fp, fs = seen[tok]
            repeat_examples.append({
                "author": meta["author"],
                "title": meta["title"],
                "token": t["token"],
                "first_pos": fp,
                "first_s2": fs,
                "repeat_pos": pos,
                "repeat_s2": s2,
                "delta": s2 - fs,
            })

n_first = len(first_s2)
n_repeat = len(repeat_s2)
avg_first = sum(first_s2) / n_first
avg_repeat = sum(repeat_s2) / n_repeat

print("=== GLOBAL: First vs. Repeat Occurrences ===")
print(f"First occurrences:  n={n_first:4d}  avg S₂={avg_first:+.3f}")
print(f"Repeat occurrences: n={n_repeat:4d}  avg S₂={avg_repeat:+.3f}")
print(f"Δ (repeat - first): {avg_repeat - avg_first:+.3f}")

# t-test approximation
import math
std_first = math.sqrt(sum((x - avg_first)**2 for x in first_s2) / n_first)
std_repeat = math.sqrt(sum((x - avg_repeat)**2 for x in repeat_s2) / n_repeat)
se = math.sqrt(std_first**2/n_first + std_repeat**2/n_repeat)
t = (avg_first - avg_repeat) / se if se > 0 else 0
print(f"  SD first={std_first:.3f}  SD repeat={std_repeat:.3f}")
print(f"  t ≈ {t:.2f} (positive = first > repeat as predicted)")


# ── 2. PER-POEM: poems with strong anaphora/refrain ──────────────────────────
ANAPHORA_POEMS = [
    "The Negro Speaks of Rivers",
    "Howl",
    "We Real Cool",
    "Whereas",
    "Free Union",
    "Lady Lazarus",
    "Catalog of Unabashed Gratitude",
    "Daddy",
]

print("\n\n=== PER-POEM REPETITION ANALYSIS ===")
poem_stats = []
for poem in corpus:
    meta = poem["metadata"]
    if meta.get("era") == "control":
        continue
    title = meta["title"]
    if not any(a in title for a in ANAPHORA_POEMS):
        continue

    tokens = poem["tokens"]
    seen = {}
    p_first, p_repeat = [], []
    for t in tokens:
        tok = t["token"].strip().lower()
        if len(tok) < 2 or tok in {w.strip().lower() for w in STOP_TOKENS}:
            continue
        s2 = t["s2"]
        if tok not in seen:
            seen[tok] = s2
            p_first.append(s2)
        else:
            p_repeat.append(s2)

    if not p_first or not p_repeat:
        continue
    af = sum(p_first)/len(p_first)
    ar = sum(p_repeat)/len(p_repeat)
    poem_stats.append((title, meta["author"], af, ar, ar - af, len(p_first), len(p_repeat)))
    print(f"\n{meta['author']}: {title}")
    print(f"  First occurrences (n={len(p_first)}):  avg S₂ = {af:+.3f}")
    print(f"  Repeat occurrences (n={len(p_repeat)}): avg S₂ = {ar:+.3f}")
    print(f"  Δ = {ar-af:+.3f} {'✓ drops as predicted' if ar < af else '✗ unexpected rise'}")


# ── 3. CASE STUDY: The Negro Speaks of Rivers ───────────────────────────────
print("\n\n=== CASE STUDY: The Negro Speaks of Rivers ===")
for poem in corpus:
    if "Negro Speaks" in poem["metadata"]["title"]:
        tokens = poem["tokens"]
        seen = {}
        for t in tokens:
            tok = t["token"].strip().lower()
            if len(tok) < 2:
                continue
            pos = t["position"]
            s2 = t["s2"]
            if tok not in seen:
                seen[tok] = []
            seen[tok].append((pos, s2, t["token"]))

        # Find tokens that appear 2+ times with large delta
        candidates = [(tok, occs) for tok, occs in seen.items() if len(occs) >= 2]
        candidates.sort(key=lambda x: x[1][0][1] - x[1][-1][1], reverse=True)
        print(f"{'Token':<15} {'1st S₂':>8}  {'2nd S₂':>8}  {'Δ':>8}")
        for tok, occs in candidates[:15]:
            first_s = occs[0][1]
            last_s = occs[-1][1]
            print(f"{repr(occs[0][2]):<15} {first_s:>8.2f}  {last_s:>8.2f}  {last_s-first_s:>+8.2f}")
        break


# ── 4. CASE STUDY: We Real Cool (pure anaphora) ─────────────────────────────
print("\n\n=== CASE STUDY: We Real Cool — 'We' anaphora ===")
for poem in corpus:
    if "We Real Cool" in poem["metadata"]["title"]:
        tokens = poem["tokens"]
        we_tokens = [(t["position"], t["s2"]) for t in tokens
                     if t["token"].strip() == "We"]
        print(f"{'Occurrence':<12} {'Position':>8}  {'S₂':>8}")
        for i, (pos, s2) in enumerate(we_tokens):
            print(f"  #{i+1:<9} {pos:>8}  {s2:>+8.2f}")
        break


# ── 5. TOP MOST-DRAMATIC DROPS ───────────────────────────────────────────────
print("\n\n=== TOP 15 MOST DRAMATIC ENTROPY COLLAPSES (first→repeat) ===")
repeat_examples.sort(key=lambda x: x["delta"])
print(f"{'Author':<25} {'Token':<15} {'1st S₂':>8}  {'2nd S₂':>8}  {'Δ':>8}")
for ex in repeat_examples[:15]:
    print(f"{ex['author']:<25} {repr(ex['token']):<15} "
          f"{ex['first_s2']:>8.2f}  {ex['repeat_s2']:>8.2f}  {ex['delta']:>+8.2f}")

# ── 6. SUMMARY TABLE FOR REPORT ─────────────────────────────────────────────
print("\n\n=== SUMMARY TABLE FOR FINDINGS ===")
print(f"| Poem | Author | n_first | n_repeat | Avg S₂ (1st) | Avg S₂ (repeat) | Δ |")
print(f"|---|---|---|---|---|---|---|")
for title, author, af, ar, delta, nf, nr in sorted(poem_stats, key=lambda x: x[4]):
    print(f"| {title[:35]} | {author[:20]} | {nf} | {nr} | {af:+.3f} | {ar:+.3f} | {delta:+.3f} |")
