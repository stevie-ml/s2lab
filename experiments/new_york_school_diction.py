"""
New York School Diction Analysis
Experiment: Do Ashbery and O'Hara have systematically different S2 profiles?
Hypothesis: O'Hara's casual, conversational diction → lower S2; Ashbery's
oblique syntax → higher S2 volatility.

Also compares NYS as a whole to reference eras.
"""
import json
import re
from collections import defaultdict

with open("results/corpus_results.json") as f:
    data = json.load(f)

# ── helpers ────────────────────────────────────────────────────────────────
def era_stats(items):
    s2s = [t["s2"] for it in items for t in it.get("tokens", [])
           if not t.get("is_newline")]
    if not s2s:
        return {}
    avg = sum(s2s) / len(s2s)
    variance = sum((x - avg) ** 2 for x in s2s) / len(s2s)
    std = variance ** 0.5
    pos_ratio = sum(1 for x in s2s if x > 0) / len(s2s)
    return {
        "n_poems": len(items),
        "n_tokens": len(s2s),
        "avg_s2": round(avg, 4),
        "std_s2": round(std, 4),
        "pos_ratio": round(pos_ratio, 3),
        "max_s2": round(max(s2s), 2),
        "median_s2": round(sorted(s2s)[len(s2s) // 2], 4),
    }

def top_s2_tokens(items, n=15, threshold=3.0):
    tokens = []
    for it in items:
        title = it["metadata"]["title"]
        author = it["metadata"].get("author", "?")
        for t in it.get("tokens", []):
            if not t.get("is_newline") and t["s2"] > threshold:
                alts = t.get("alternatives", [])
                top_pred = alts[0]["token"].strip() if alts else ""
                tokens.append({
                    "token": t["token"].strip(),
                    "s2": t["s2"],
                    "surprisal": t["surprisal"],
                    "entropy": t["entropy"],
                    "top_pred": top_pred,
                    "title": title,
                    "author": author,
                })
    tokens.sort(key=lambda x: -x["s2"])
    return tokens[:n]

def suppression_taxonomy(items, threshold=3.0):
    """POS-style taxonomy of what GPT-2 predicted vs what the poet chose."""
    pronouns = {"I", "you", "he", "she", "it", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "its", "our", "their"}
    articles = {"a", "an", "the"}
    prepositions = {"in", "on", "at", "to", "for", "of", "from", "with", "by", "as", "into", "through", "about", "over", "under", "between", "among"}
    conjunctions = {"and", "but", "or", "nor", "so", "yet", "for", "although", "because", "since", "while", "if", "when", "that", "which"}

    def classify(w):
        w = w.strip().lower().rstrip('.,!?;:')
        if not w:
            return "other"
        if w in pronouns: return "pronoun"
        if w in articles: return "article"
        if w in prepositions: return "preposition"
        if w in conjunctions: return "conjunction"
        if w[0].isupper(): return "proper_noun"
        if w.isdigit(): return "number"
        return "content_word"

    chosen_cats = defaultdict(int)
    suppressed_cats = defaultdict(int)
    for it in items:
        for t in it.get("tokens", []):
            if not t.get("is_newline") and t["s2"] > threshold:
                chosen_cats[classify(t["token"])] += 1
                alts = t.get("alternatives", [])
                top = alts[0]["token"] if alts else ""
                suppressed_cats[classify(top)] += 1
    return chosen_cats, suppressed_cats

# ── group poems ────────────────────────────────────────────────────────────
groups = defaultdict(list)
for item in data:
    era = item["metadata"].get("era")
    author = item["metadata"].get("author", "")
    groups[("era", era)].append(item)
    if era == "new_york_school":
        groups[("author", author)].append(item)

# ── reference eras ─────────────────────────────────────────────────────────
reference_eras = ["romantic", "modernist", "confessional", "beat", "language",
                  "victorian", "imagist", "surrealist"]

print("=" * 60)
print("NEW YORK SCHOOL S2 ANALYSIS")
print("=" * 60)

# 1. Era comparison
print("\n## 1. Era-Level Comparison (NYS vs Reference)\n")
nys_stats = era_stats(groups[("era", "new_york_school")])
rows = [("new_york_school", nys_stats)]
for era in reference_eras:
    s = era_stats(groups[("era", era)])
    if s:
        rows.append((era, s))

rows.sort(key=lambda x: -x[1]["avg_s2"])
print(f"{'Era':<22} {'n':>4} {'avg_S2':>8} {'std_S2':>8} {'+S2%':>7} {'median':>8}")
print("-" * 60)
for era, s in rows:
    marker = " ◄" if era == "new_york_school" else ""
    print(f"{era:<22} {s['n_poems']:>4} {s['avg_s2']:>8.3f} {s['std_s2']:>8.3f} "
          f"{s['pos_ratio']*100:>6.1f}% {s['median_s2']:>8.3f}{marker}")

# 2. Within-NYS: Ashbery vs O'Hara
print("\n## 2. Ashbery vs O'Hara vs Koch\n")
for author in ["John Ashbery", "Frank O'Hara", "Kenneth Koch"]:
    items = groups[("author", author)]
    if items:
        s = era_stats(items)
        print(f"{author}: n={s['n_poems']} avg_S2={s['avg_s2']} std={s['std_s2']} +S2%={s['pos_ratio']*100:.1f}%")

# 3. Top high-S2 tokens per author
print("\n## 3. Top High-S2 Tokens by Author\n")
for author in ["John Ashbery", "Frank O'Hara"]:
    items = groups[("author", author)]
    if items:
        top = top_s2_tokens(items, n=10, threshold=5.0)
        print(f"\n{author}:")
        for t in top:
            print(f"  '{t['token']}' S2={t['s2']:.2f} (predicted: '{t['top_pred']}') — {t['title'][:40]}")

# 4. Suppression taxonomy: what does NYS suppress?
print("\n## 4. Suppression Taxonomy (high-S2 positions, NYS vs Romantic)\n")
for label, era in [("New York School", "new_york_school"), ("Romantic", "romantic")]:
    items = groups[("era", era)]
    chosen, suppressed = suppression_taxonomy(items, threshold=2.0)
    total_chosen = sum(chosen.values())
    total_suppressed = sum(suppressed.values())
    print(f"\n{label} — what was chosen at high-S2 positions:")
    for cat, n in sorted(chosen.items(), key=lambda x: -x[1]):
        print(f"  {cat:<15}: {n:3d} ({100*n/total_chosen:.1f}%)")
    print(f"{label} — what was suppressed (top GPT-2 prediction):")
    for cat, n in sorted(suppressed.items(), key=lambda x: -x[1]):
        print(f"  {cat:<15}: {n:3d} ({100*n/total_suppressed:.1f}%)")

# 5. Per-poem S2 stats for NYS
print("\n## 5. Per-Poem S2 Summary (NYS)\n")
nys_items = groups[("era", "new_york_school")]
poem_stats = []
for item in nys_items:
    s2s = [t["s2"] for t in item.get("tokens", []) if not t.get("is_newline")]
    if s2s:
        avg = sum(s2s) / len(s2s)
        std = (sum((x - avg)**2 for x in s2s) / len(s2s)) ** 0.5
        pos = sum(1 for x in s2s if x > 0) / len(s2s)
        poem_stats.append({
            "title": item["metadata"]["title"][:35],
            "author": item["metadata"].get("author", "?").split()[-1],
            "avg_s2": avg,
            "std_s2": std,
            "pos_ratio": pos,
            "n": len(s2s),
        })
poem_stats.sort(key=lambda x: -x["avg_s2"])
print(f"{'Title':<36} {'Author':<10} {'avg_S2':>7} {'std':>7} {'+S2%':>6}")
print("-" * 70)
for p in poem_stats:
    print(f"{p['title']:<36} {p['author']:<10} {p['avg_s2']:>7.3f} {p['std_s2']:>7.3f} {p['pos_ratio']*100:>5.1f}%")

# 6. Save to JSON for findings
output = {
    "era_comparison": {era: stats for era, stats in rows},
    "author_comparison": {},
    "per_poem": poem_stats,
}
for author in ["John Ashbery", "Frank O'Hara", "Kenneth Koch"]:
    items = groups[("author", author)]
    if items:
        output["author_comparison"][author] = era_stats(items)

with open("results/new_york_school_diction.json", "w") as f:
    json.dump(output, f, indent=2)

print("\n\nSaved to results/new_york_school_diction.json")
