"""
Postcolonial / Diaspora Poetics and S₂

Research question: Do poets working between oral traditions, vernacular
dialect, and standard literary English show systematically different S₂
signatures from mainstream Anglo-American poetry?

Hypothesis: Code-switching, oral patterning, and cross-cultural lexicons
diverge from GPT-2's primarily Anglo-American training distribution →
higher artifact-free S₂ than comparable contemporary poetry.

Key poets added: Joy Harjo, Derek Walcott, Agha Shahid Ali, Kamau Brathwaite
Comparison: contemporary, confessional, beat, new_york_school, victorian, romantic
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")

with open(RESULTS) as f:
    data = json.load(f)

ARTIFACT_THRESHOLD = 0.9  # p_newline threshold for stanza-break filtering


def poem_stats(poem, clean=True):
    tokens = poem["tokens"]
    if clean:
        tokens = [t for t in tokens if t.get("p_newline", 0) < ARTIFACT_THRESHOLD]
    if not tokens:
        return None
    s2_vals = [t["s2"] for t in tokens]
    return {
        "title": poem["metadata"]["title"],
        "author": poem["metadata"]["author"],
        "era": poem["metadata"]["era"],
        "year": poem["metadata"].get("year"),
        "n_tokens": len(tokens),
        "mean_s2": sum(s2_vals) / len(s2_vals),
        "max_s2": max(s2_vals),
        "pos_ratio": sum(1 for s in s2_vals if s > 0) / len(s2_vals),
        "std_s2": (sum((s - sum(s2_vals)/len(s2_vals))**2 for s in s2_vals) / len(s2_vals))**0.5,
    }


# Collect stats by era
era_groups = {}
for poem in data:
    era = poem["metadata"]["era"]
    lang = poem["metadata"].get("language", "en")
    if lang != "en":
        continue
    stats = poem_stats(poem)
    if stats is None:
        continue
    era_groups.setdefault(era, []).append(stats)


def era_summary(era_name):
    poems = era_groups.get(era_name, [])
    if not poems:
        return None
    mean_s2 = sum(p["mean_s2"] for p in poems) / len(poems)
    max_s2 = max(p["max_s2"] for p in poems)
    pos_ratio = sum(p["pos_ratio"] for p in poems) / len(poems)
    return {
        "era": era_name,
        "n": len(poems),
        "mean_s2": round(mean_s2, 3),
        "max_s2": round(max_s2, 3),
        "pos_ratio": round(pos_ratio, 3),
        "poems": poems,
    }


# Focal group
postcolonial = era_summary("postcolonial")

# Comparison eras
comparison_eras = [
    "contemporary", "confessional", "beat", "new_york_school",
    "victorian", "romantic", "modernist", "black_arts",
    "harlem_renaissance", "protest_political", "language",
]
comparisons = [era_summary(e) for e in comparison_eras if era_summary(e)]

print("\n=== POSTCOLONIAL / DIASPORA S₂ ANALYSIS ===\n")
print("FOCAL GROUP — postcolonial poets:")
if postcolonial:
    for p in postcolonial["poems"]:
        print(f"  {p['author']:<30} {p['title']:<40} S₂={p['mean_s2']:+.3f}  max={p['max_s2']:.2f}  +S₂={p['pos_ratio']:.0%}")
    print(f"\n  ERA MEAN: {postcolonial['mean_s2']:+.3f}  max={postcolonial['max_s2']:.2f}  n={postcolonial['n']}")

print("\n\nCOMPARISON ERAS (artifact-free mean S₂):")
all_groups = [postcolonial] + comparisons
all_groups_sorted = sorted([g for g in all_groups if g], key=lambda x: x["mean_s2"], reverse=True)
print(f"{'Era':<25} {'n':>4}  {'Mean S₂':>9}  {'Max S₂':>8}  {'+S₂%':>6}")
print("-" * 62)
for g in all_groups_sorted:
    marker = " ◄ FOCAL" if g["era"] == "postcolonial" else ""
    print(f"{g['era']:<25} {g['n']:>4}  {g['mean_s2']:>+9.3f}  {g['max_s2']:>8.2f}  {g['pos_ratio']:>5.0%}{marker}")

# Per-poet analysis: locate highest-S2 tokens and categorize what GPT-2 expected
print("\n\n=== TOP S₂ MOMENTS IN POSTCOLONIAL POEMS (artifact-free) ===\n")
postcolonial_raw = [p for p in data if p["metadata"]["era"] == "postcolonial"]

for poem in postcolonial_raw:
    tokens = [t for t in poem["tokens"] if t.get("p_newline", 0) < ARTIFACT_THRESHOLD]
    if not tokens:
        continue
    top = sorted(tokens, key=lambda t: t["s2"], reverse=True)[:5]
    print(f"\n{poem['metadata']['author']} — \"{poem['metadata']['title']}\"")
    for t in top:
        alts = t.get("alternatives", [])[:3]
        alt_str = ", ".join(f"'{a['token'].strip()}'({a['prob']:.1%})" for a in alts)
        ctx = t.get("context_before", "")[-30:].replace("\n", "↵")
        print(f"  S₂={t['s2']:+.2f}  token='{t['token'].strip()}'  |  GPT-2 expected: {alt_str}")
        print(f"         context: ...{ctx}")

# Cross-analysis: what textual features drive high S2 in postcolonial poems?
print("\n\n=== LINGUISTIC FEATURE ANALYSIS ===\n")

def categorize_token(tok_str, alternatives):
    """Rough categorization of what makes a token surprising."""
    tok = tok_str.strip().lower()
    top_alt = alternatives[0]["token"].strip() if alternatives else ""
    # Check if model expected newline
    if top_alt == "" or top_alt == "\n":
        return "newline_expected"
    # Check if token looks like a proper noun / cultural-specific word
    if tok_str.strip() and tok_str.strip()[0].isupper() and len(tok_str.strip()) > 2:
        return "proper_noun"
    # Check if it's a function word
    function_words = {"the", "a", "an", "of", "in", "and", "or", "but", "to", "for",
                      "with", "is", "was", "are", "were", "be", "been", "have", "had",
                      "that", "this", "it", "he", "she", "they", "we", "I", "you"}
    if tok.replace("'", "").replace(",", "") in function_words:
        return "function_word"
    # Check number of subword tokens (proxy for rarity)
    # (length heuristic: long tokens tend to be multi-subword words)
    if len(tok) >= 8:
        return "long_rare_word"
    # Cultural/sensory vocabulary — rough heuristic
    cultural_markers = {
        "guadeloupe", "kashmir", "jhelum", "himalayas", "calypso",
        "sargasso", "caribbean", "brathwaite", "harjo", "walcott",
        "ultramarine", "bergamot", "vermouth",
        "horses", "sky", "earth", "rain", "savannah", "sand",
    }
    if tok in cultural_markers:
        return "cultural_lexicon"
    return "content_word"


category_counts = {}
for poem in postcolonial_raw:
    tokens = [t for t in poem["tokens"] if t.get("p_newline", 0) < ARTIFACT_THRESHOLD]
    high_s2 = [t for t in tokens if t["s2"] > 2.0]
    for t in high_s2:
        cat = categorize_token(t["token"], t.get("alternatives", []))
        category_counts[cat] = category_counts.get(cat, 0) + 1

total = sum(category_counts.values())
if total > 0:
    print("Category breakdown of high-S₂ tokens (S₂ > 2.0) in postcolonial poems:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<25} {count:>4}  ({count/total:.0%})")

# Specific feature: oral/repetition markers
print("\n\n=== ORAL PATTERNING: ANAPHORA AND S₂ ===\n")
print("Examining Harjo 'She Had Some Horses' — anaphoric catalog:")

horses_poem = next((p for p in postcolonial_raw if "Horses" in p["metadata"]["title"]), None)
if horses_poem:
    tokens = [t for t in horses_poem["tokens"] if t.get("p_newline", 0) < ARTIFACT_THRESHOLD]
    print(f"  Total clean tokens: {len(tokens)}")
    print(f"  Mean S₂ (clean): {sum(t['s2'] for t in tokens)/len(tokens):+.3f}")
    # Find the "horses" repetitions
    horse_tokens = [(i, t) for i, t in enumerate(tokens) if "horse" in t["token"].lower()]
    if horse_tokens:
        print(f"\n  Occurrences of 'horses' token (S₂ per occurrence):")
        for i, (pos, t) in enumerate(horse_tokens[:12]):
            print(f"    Occurrence {i+1}: pos={pos}  S₂={t['s2']:+.2f}  surprisal={t['surprisal']:.2f}  entropy={t['entropy']:.2f}")

# Save results for findings
results_out = {
    "postcolonial": postcolonial,
    "comparisons": {g["era"]: {"n": g["n"], "mean_s2": g["mean_s2"], "pos_ratio": g["pos_ratio"]}
                    for g in comparisons if g},
    "category_counts": category_counts,
}
out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings", "postcolonial_s2.json")
with open(out_path, "w") as f:
    json.dump(results_out, f, indent=2)
print(f"\n\nResults saved to {out_path}")
