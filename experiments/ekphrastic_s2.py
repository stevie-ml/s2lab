"""
Ekphrastic Poetry and the Verbal-Visual Interface

Research question: Do poems about visual art (ekphrasis) have distinctive S2 profiles?
Hypothesis: S2 spikes at "translation moments" — where language attempts to capture
visual specifics — because GPT-2's sequential language model is unprepared for the
intrusion of visual/artistic vocabulary into otherwise conventional lyric flow.

Sub-hypotheses:
  H1: Ekphrastic poems have higher mean S2 than the broader Victorian/Romantic average
  H2: Tokens describing visual features (color, shape, form, material) have higher S2
  H3: Proper nouns naming artworks/artists have especially high S2 (unpredictable names)
  H4: Questions about what is depicted ("What men or gods are these?") show S2 spikes

Comparison: ekphrastic era vs. romantic + victorian + 19th_century eras
"""

import json, re, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine import analyze_corpus, load_results
from corpus.poems import POEMS

# ── Load or compute S2 for full corpus ──────────────────────────────────────
results_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "results", "corpus_results.json")
print("Loading corpus results...")
try:
    all_results = load_results(results_path)
    # Check if ekphrastic poems are already in results
    ekphrastic_titles = {p["title"] for p in POEMS if p.get("era") == "ekphrastic"}
    computed_titles = {r["metadata"]["title"] for r in all_results}
    missing = ekphrastic_titles - computed_titles
    if missing:
        print(f"  {len(missing)} ekphrastic poems not in cached results — computing...")
        new_poems = [p for p in POEMS if p["title"] in missing]
        new_results = analyze_corpus(new_poems)
        all_results.extend(new_results)
    else:
        print(f"  All ekphrastic poems already cached.")
except Exception as e:
    print(f"  Computing full corpus: {e}")
    all_results = analyze_corpus(POEMS)

print(f"  Total analyzed: {len(all_results)} poems")

# ── Organize by era ──────────────────────────────────────────────────────────
def artifact_free_s2(tokens):
    """Return S2 values excluding stanza-break artifact tokens (p(newline) >= 0.9)."""
    return [t["s2"] for t in tokens
            if t.get("s2") is not None
            and not (t["token"].strip() == "" and t.get("surprisal", 0) < 0.15)]

def poem_stats(result):
    """Compute summary stats for a poem."""
    tokens = result.get("tokens", [])
    clean = artifact_free_s2(tokens)
    if not clean:
        return None
    meta = result.get("metadata", result)  # handle both nested and flat structure
    pos = [v for v in clean if v > 0]
    return {
        "title":   meta.get("title", "?"),
        "author":  meta.get("author", "?"),
        "era":     meta.get("era", "?"),
        "mean_s2": sum(clean) / len(clean),
        "pos_ratio": len(pos) / len(clean),
        "max_s2":  max(clean),
        "n_tokens": len(clean),
        "top_tokens": sorted(
            [(t["token"], t["s2"]) for t in tokens
             if t.get("s2") is not None and t["s2"] > 1.0],
            key=lambda x: -x[1]
        )[:8]
    }

# Group results
ekphrastic = []
comparison = []  # romantic + 19th_century + victorian
control_eras = {"romantic", "19th_century", "victorian", "early_modern"}

for r in all_results:
    meta = r.get("metadata", r)
    era = meta.get("era", "")
    s = poem_stats(r)
    if s is None:
        continue
    if era == "ekphrastic":
        ekphrastic.append(s)
    elif era in control_eras:
        comparison.append(s)

print(f"\nEkphrastic poems: {len(ekphrastic)}")
print(f"Comparison poems (romantic/19th/victorian/early_modern): {len(comparison)}")

# ── Per-poem breakdown ────────────────────────────────────────────────────────
print("\n" + "="*70)
print("EKPHRASTIC POEMS — S2 PROFILES")
print("="*70)

ekphrastic.sort(key=lambda x: -x["mean_s2"])
for s in ekphrastic:
    print(f"\n  {s['title'][:50]} ({s['author']}, era=ekphrastic)")
    print(f"    mean S2={s['mean_s2']:+.3f}  pos_ratio={s['pos_ratio']:.2f}  max_S2={s['max_s2']:.2f}  n={s['n_tokens']}")
    if s["top_tokens"]:
        print(f"    Top surprise tokens:")
        for tok, val in s["top_tokens"][:5]:
            print(f"      {repr(tok):20s} S2={val:+.2f}")

# ── Comparison stats ──────────────────────────────────────────────────────────
def era_summary(poems_stats):
    if not poems_stats:
        return None
    means = [s["mean_s2"] for s in poems_stats]
    pos_ratios = [s["pos_ratio"] for s in poems_stats]
    return {
        "n": len(poems_stats),
        "mean_s2": sum(means) / len(means),
        "median_s2": sorted(means)[len(means)//2],
        "pos_ratio": sum(pos_ratios) / len(pos_ratios),
        "max_s2": max(s["max_s2"] for s in poems_stats)
    }

ekph_summary = era_summary(ekphrastic)
comp_summary = era_summary(comparison)

print("\n" + "="*70)
print("GROUP COMPARISON")
print("="*70)
print(f"\n{'Group':35s} {'n':>4s} {'mean S2':>9s} {'median S2':>9s} {'pos_ratio':>10s} {'max S2':>9s}")
print("-"*70)
if ekph_summary:
    print(f"{'Ekphrastic':35s} {ekph_summary['n']:>4d} {ekph_summary['mean_s2']:>+9.3f} "
          f"{ekph_summary['median_s2']:>+9.3f} {ekph_summary['pos_ratio']:>10.2f} "
          f"{ekph_summary['max_s2']:>9.2f}")
if comp_summary:
    print(f"{'Romantic/Victorian/19th-cent':35s} {comp_summary['n']:>4d} {comp_summary['mean_s2']:>+9.3f} "
          f"{comp_summary['median_s2']:>+9.3f} {comp_summary['pos_ratio']:>10.2f} "
          f"{comp_summary['max_s2']:>9.2f}")

# ── Token-level: visual vocabulary analysis ───────────────────────────────────
# Look for "visual vocabulary" tokens in ekphrastic poems
VISUAL_KEYWORDS = {
    # colors
    "white", "red", "green", "gold", "golden", "silver", "grey", "gray",
    "pale", "dark", "bright", "dim", "shadow", "shad",
    # form/shape
    "shape", "form", "curve", "arch", "marble", "stone", "carved",
    "brede", "wrought", "drest", "brow",
    # art materials
    "paint", "canvas", "brush", "chisel", "viol", "web", "weave", "wove",
    # visual action words
    "gaze", "look", "see", "behold", "stare", "mirror", "reflect",
    "portrait", "picture", "image", "depict",
    # art-specific nouns
    "urn", "timbrel", "pipe", "maiden", "altar", "priest", "sacrifice",
    "statue", "frieze", "palette", "scene",
}

def is_visual_token(tok_str):
    w = tok_str.strip().lower().lstrip("Ġ").lstrip(" ")
    return any(w == kw or w.startswith(kw) for kw in VISUAL_KEYWORDS)

visual_s2_values = []
nonvisual_s2_values = []

for r in all_results:
    meta = r.get("metadata", r)
    if meta.get("era") != "ekphrastic":
        continue
    for t in r.get("tokens", []):
        if t.get("s2") is None:
            continue
        # skip newline artifacts
        if t["token"].strip() == "" and t.get("surprisal", 0) < 0.15:
            continue
        if is_visual_token(t["token"]):
            visual_s2_values.append(t["s2"])
        else:
            nonvisual_s2_values.append(t["s2"])

print("\n" + "="*70)
print("VISUAL vs NON-VISUAL TOKENS IN EKPHRASTIC POEMS")
print("="*70)
if visual_s2_values:
    print(f"\n  Visual vocabulary tokens: n={len(visual_s2_values)}")
    print(f"    mean S2 = {sum(visual_s2_values)/len(visual_s2_values):+.3f}")
    print(f"    pos_ratio = {sum(1 for v in visual_s2_values if v > 0)/len(visual_s2_values):.2f}")
if nonvisual_s2_values:
    print(f"\n  Non-visual tokens: n={len(nonvisual_s2_values)}")
    print(f"    mean S2 = {sum(nonvisual_s2_values)/len(nonvisual_s2_values):+.3f}")
    print(f"    pos_ratio = {sum(1 for v in nonvisual_s2_values if v > 0)/len(nonvisual_s2_values):.2f}")

# ── Interrogative / apostrophe moments ───────────────────────────────────────
# Find tokens immediately after "?" or "What" / "Thou" in ekphrastic poems
print("\n" + "="*70)
print("S2 AT APOSTROPHE AND INTERROGATIVE MOMENTS")
print("="*70)

interrogative_s2 = []
apostrophe_s2 = []

for r in all_results:
    meta = r.get("metadata", r)
    if meta.get("era") != "ekphrastic":
        continue
    tokens = r.get("tokens", [])
    for i, t in enumerate(tokens):
        tok = t["token"].strip()
        s2 = t.get("s2")
        if s2 is None:
            continue
        # tokens that ARE the question word
        if tok in ("What", "Who", "Why", "Where", "Thou", "thee", "thy"):
            interrogative_s2.append((t["token"], s2))
        # tokens right after "?"
        if i > 0 and "?" in tokens[i-1]["token"]:
            interrogative_s2.append((t["token"], s2))

if interrogative_s2:
    vals = [v for _, v in interrogative_s2]
    print(f"\n  Interrogative/apostrophe tokens: n={len(vals)}")
    print(f"    mean S2 = {sum(vals)/len(vals):+.3f}")
    print(f"    pos_ratio = {sum(1 for v in vals if v > 0)/len(vals):.2f}")
    top = sorted(interrogative_s2, key=lambda x: -x[1])[:5]
    print(f"    Top examples:")
    for tok, val in top:
        print(f"      {repr(tok):20s} S2={val:+.2f}")

# ── Save results ─────────────────────────────────────────────────────────────
output = {
    "ekphrastic_poems": ekphrastic,
    "ekphrastic_summary": ekph_summary,
    "comparison_summary": comp_summary,
    "visual_token_mean_s2": (sum(visual_s2_values)/len(visual_s2_values)
                              if visual_s2_values else None),
    "nonvisual_token_mean_s2": (sum(nonvisual_s2_values)/len(nonvisual_s2_values)
                                 if nonvisual_s2_values else None),
    "visual_n": len(visual_s2_values),
    "nonvisual_n": len(nonvisual_s2_values),
    "interrogative_mean_s2": (sum(v for _, v in interrogative_s2)/len(interrogative_s2)
                               if interrogative_s2 else None),
}

out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "results", "ekphrastic_s2.json")
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to {out_path}")
