"""
Double Dactyl Form Spectrum: The Most Constrained English Poem

Research question: Does the double dactyl — the most formally constrained short
poem in English — have even lower mean S₂ than the limerick? And do its specific
structural positions (nonsense line 1, person's name line 2, single polysyllabic
word line 7) produce distinctive S₂ spikes?

The form constraint spectrum, from most to least constrained:
  double_dactyl → limerick → clerihew → fixed_form → free verse → prose

Expected:
  - Double dactyls: lowest mean S₂ of any poetry (below limerick)
  - Exception: nonsense line-1 tokens (Higgledy-piggledy) should spike HIGH
  - The single polysyllabic word (line 7) may spike depending on word rarity
  - Clerihews (no meter) should be HIGHER than limericks despite similar length/humor

Date: 2026-10-20
"""

import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")

with open(RESULTS_FILE) as f:
    data = json.load(f)

# Stanza-break artifact filter: skip tokens with p(newline) >= 0.9
def artifact_free(tokens):
    return [t for t in tokens if t.get("p_newline", 0) < 0.9]

def stats(tokens):
    if not tokens:
        return {"mean": None, "n": 0, "pos_ratio": 0}
    s2 = [t["s2"] for t in tokens]
    pos = [x for x in s2 if x > 0]
    return {
        "mean": sum(s2) / len(s2),
        "n": len(s2),
        "pos_ratio": len(pos) / len(s2) if s2 else 0,
        "max": max(s2) if s2 else None,
    }

# ─── 1. Era-level comparison ─────────────────────────────────────────────────

target_eras = ["double_dactyl", "clerihew", "limerick", "fixed_form",
               "metaphysical", "romantic", "prose_poetry", "found_poetry", "control"]

era_data = {era: [] for era in target_eras}
era_poems = {era: [] for era in target_eras}

for entry in data:
    era = entry["metadata"].get("era", "")
    if era in era_data:
        tokens = artifact_free(entry["tokens"])
        if tokens:
            era_data[era].extend(tokens)
            era_poems[era].append({
                "title": entry["metadata"]["title"],
                "author": entry["metadata"]["author"],
                "tokens": tokens,
                "raw_tokens": entry["tokens"],
            })

print("=" * 65)
print("FORM CONSTRAINT SPECTRUM: Mean Artifact-Free S₂")
print("=" * 65)
print(f"{'Era':<20} {'n poems':>8} {'n tokens':>9} {'Mean S₂':>8} {'Pos%':>6}")
print("-" * 65)
for era in target_eras:
    poems = era_poems[era]
    tokens = era_data[era]
    if not tokens:
        print(f"  {era:<18} {'—':>8} {'—':>9} {'—':>8} {'—':>6}")
        continue
    s = stats(tokens)
    print(f"  {era:<18} {len(poems):>8} {s['n']:>9} {s['mean']:>8.3f} {100*s['pos_ratio']:>5.1f}%")

# ─── 2. Per-poem stats for double dactyls and clerihews ─────────────────────

print("\n" + "=" * 65)
print("DOUBLE DACTYL — Per-poem S₂")
print("=" * 65)
for p in era_poems["double_dactyl"]:
    s = stats(p["tokens"])
    raw_s = stats(p["raw_tokens"])
    print(f"  {p['title'][:45]:<45} AF:{s['mean']:>7.3f}  raw:{raw_s['mean']:>7.3f}")

print("\nCLERIHEW — Per-poem S₂")
print("=" * 65)
for p in era_poems["clerihew"]:
    s = stats(p["tokens"])
    raw_s = stats(p["raw_tokens"])
    print(f"  {p['title'][:45]:<45} AF:{s['mean']:>7.3f}  raw:{raw_s['mean']:>7.3f}")

print("\nLIMERICK — Per-poem S₂ (top/bottom)")
print("=" * 65)
lims = sorted(era_poems["limerick"], key=lambda p: stats(p["tokens"])["mean"], reverse=True)
for p in lims:
    s = stats(p["tokens"])
    raw_s = stats(p["raw_tokens"])
    print(f"  {p['title'][:45]:<45} AF:{s['mean']:>7.3f}  raw:{raw_s['mean']:>7.3f}")

# ─── 3. Line-by-line analysis of double dactyls ─────────────────────────────

print("\n" + "=" * 65)
print("DOUBLE DACTYL — Line-by-line S₂ (pooled across all 5 poems)")
print("=" * 65)

# For each double dactyl, reconstruct the 8-line structure from token positions.
# We identify line breaks by looking at the raw text of each poem.

line_s2 = {i: [] for i in range(1, 9)}  # lines 1-8
line_tokens = {i: [] for i in range(1, 9)}

from corpus.poems import POEMS
dd_poems_corpus = [p for p in POEMS if p["era"] == "double_dactyl"]

for entry in data:
    if entry["metadata"].get("era") != "double_dactyl":
        continue
    title = entry["metadata"]["title"]
    # Find the matching poem text
    poem = next((p for p in dd_poems_corpus if p["title"] == title), None)
    if poem is None:
        continue
    text = poem["text"].strip()
    lines_text = [l for l in text.split("\n") if l.strip()]
    if len(lines_text) != 8:
        print(f"  WARNING: {title} has {len(lines_text)} non-empty lines, expected 8")
        continue

    # Map each token to its line by character offset
    raw_text = poem["text"]
    tokens = entry["tokens"]

    # Rebuild character positions for each token
    cursor = 0
    token_line_map = []
    for tok in tokens:
        token_text = tok.get("token", "")
        # Find this token's position in the raw text
        pos = raw_text.find(token_text, cursor)
        if pos == -1:
            token_line_map.append(None)
            continue
        cursor = pos + len(token_text)
        # Count newlines before this position to determine line number
        preceding = raw_text[:pos]
        newline_count = preceding.count("\n")
        # Ignore blank lines (the stanza break between lines 4 and 5)
        non_blank_lines_before = sum(1 for l in preceding.split("\n") if l.strip())
        line_num = non_blank_lines_before + 1  # 1-indexed
        if 1 <= line_num <= 8:
            token_line_map.append(line_num)
        else:
            token_line_map.append(None)

    for tok, ln in zip(tokens, token_line_map):
        if ln is None:
            continue
        if tok.get("p_newline", 0) >= 0.9:
            continue  # artifact filter
        s2_val = tok["s2"]
        line_s2[ln].append(s2_val)

# Print line-by-line stats
roles = {
    1: "nonsense phrase",
    2: "person's name",
    3: "content",
    4: "rhyme A (catalectic)",
    5: "content",
    6: "content",
    7: "SINGLE LONG WORD",
    8: "rhyme A (catalectic)",
}
print(f"{'Line':>5} {'Role':<25} {'n':>5} {'Mean S₂':>8} {'Pos%':>6}")
print("-" * 55)
for ln in range(1, 9):
    vals = line_s2[ln]
    if not vals:
        print(f"  {ln:>3}  {roles[ln]:<25}  {'—':>5}  {'—':>8}  {'—':>6}")
        continue
    mean = sum(vals) / len(vals)
    pos_pct = 100 * sum(1 for v in vals if v > 0) / len(vals)
    print(f"  {ln:>3}  {roles[ln]:<25} {len(vals):>5} {mean:>8.3f} {pos_pct:>5.1f}%")

# ─── 4. The nonsense line in detail ─────────────────────────────────────────

print("\n" + "=" * 65)
print("NONSENSE LINE DETAIL (Higgledy-piggledy tokens)")
print("=" * 65)
for entry in data:
    if entry["metadata"].get("era") != "double_dactyl":
        continue
    title = entry["metadata"]["title"]
    tokens = entry["tokens"]
    # Look for tokens that are part of "Higgledy" or "piggledy"
    hig_tokens = [t for t in tokens if "iggle" in t.get("token", "").lower()
                  or "Higgle" in t.get("token", "")]
    first_top = tokens[:8] if len(tokens) >= 8 else tokens
    s2_vals = [t["s2"] for t in first_top if t.get("p_newline", 0) < 0.9]
    if s2_vals:
        print(f"  {title[:50]}: line-1 mean S₂={sum(s2_vals)/len(s2_vals):.3f}")
        for t in first_top:
            if t.get("p_newline", 0) >= 0.9:
                continue
            top1 = t.get("alternatives", [{}])[0].get("token", "?") if t.get("alternatives") else "?"
            print(f"    tok={t['token']!r:15} s2={t['s2']:7.2f}  top1={top1!r}")

# ─── 5. The single-long-word line in detail ─────────────────────────────────

print("\n" + "=" * 65)
print("SINGLE LONG WORD (line 7) — Per-poem analysis")
print("=" * 65)
LONG_WORDS = {
    "Emily Dickinson (Double Dactyl)": "Unconventionally",
    "Gerard Manley Hopkins (Double Dactyl)": "Theologically",
    "Alfred Lord Tennyson (Double Dactyl)": "Philosophically",
    "William Carlos Williams (Double Dactyl)": "Experientially",
    "Lawrence Ferlinghetti (Double Dactyl)": "Uncompromisingly",
}
for entry in data:
    if entry["metadata"].get("era") != "double_dactyl":
        continue
    title = entry["metadata"]["title"]
    long_word = LONG_WORDS.get(title, "")
    tokens = entry["tokens"]
    # Find tokens near the long word
    long_toks = [t for t in tokens if long_word[:4].lower() in t.get("token", "").lower()
                 and t.get("p_newline", 0) < 0.9]
    print(f"\n  {title}")
    print(f"  Target word: {long_word!r}")
    if long_toks:
        for t in long_toks[:4]:
            top1 = t.get("alternatives", [{}])[0].get("token", "?") if t.get("alternatives") else "?"
            print(f"    tok={t['token']!r:20} s2={t['s2']:7.2f}  top1={top1!r}")
    else:
        print(f"    (tokens not identified by prefix search)")
        # Fallback: find by position (line 7 is penultimate content line)
        line7_s2 = line_s2.get(7, [])
        if line7_s2:
            print(f"    line-7 mean S₂: {sum(line7_s2)/len(line7_s2):.3f} (n={len(line7_s2)})")
