"""
Deixis and S2: How do 'pointing words' work informationally in poetry?

Deixis = words that ground meaning in the context of utterance:
  - Spatial:    here, there, nearby, beyond
  - Temporal:   now, then, today, tonight, yesterday, tomorrow, once, always, never
  - Demonstrative: this, that, these, those

These words assert presence or proximity — poetry's 'lyric NOW' and 'lyric HERE'.
Hypothesis: temporal deictics (now/today/tonight) have higher S2 than prose counterparts,
because poets deploy them at moments of heightened significance. Demonstratives (this/that)
may be more predictable — they often introduce familiar/established referents.

Secondary question: what immediately FOLLOWS a deictic in poetry? Does the deictic
open a high-entropy window (many possible referents) and then the poet's choice is
more surprising (high S2)?
"""

import json
from collections import defaultdict

with open("results/corpus_results.json") as f:
    data = json.load(f)

# --- Deictic lexicon ---
SPATIAL = {"here", "there", "nearby", "yonder", "beyond", "hence", "hither", "thither"}
TEMPORAL = {
    "now", "then", "today", "tonight", "yesterday", "tomorrow",
    "once", "always", "never", "ever", "already", "still", "yet", "soon", "soon",
    "before", "after", "again",
}
DEMONSTRATIVE = {"this", "that", "these", "those"}
ALL_DEICTIC = SPATIAL | TEMPORAL | DEMONSTRATIVE

# --- Helper ---
def classify(tok_str):
    t = tok_str.strip().lower()
    if t in SPATIAL:
        return "spatial"
    if t in TEMPORAL:
        return "temporal"
    if t in DEMONSTRATIVE:
        return "demonstrative"
    return None


# -------------------------------------------------------------------
# 1. Token-level: collect deictic and non-deictic stats
# -------------------------------------------------------------------
deictic_records = []   # {category, s2, surprisal, entropy, poem_title, poem_era, token}
control_records = []   # non-deictic, non-punct, alphabetic tokens
post_deictic = []      # token FOLLOWING a deictic

english_poems = [p for p in data if p["metadata"].get("language", "en") == "en"
                                  and p["metadata"].get("era") != "control"]

for poem in english_poems:
    tokens = poem["tokens"]
    meta = poem["metadata"]
    for i, tok in enumerate(tokens):
        raw = tok["token"]
        t = raw.strip().lower()
        cat = classify(raw)
        if cat:
            deictic_records.append({
                "category": cat,
                "token": t,
                "s2": tok["s2"],
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "title": meta["title"],
                "author": meta.get("author", "?"),
                "era": meta.get("era", "?"),
            })
            # record the following token's S2
            if i + 1 < len(tokens):
                nxt = tokens[i + 1]
                post_deictic.append({
                    "deictic": t,
                    "category": cat,
                    "next_token": nxt["token"].strip(),
                    "next_s2": nxt["s2"],
                    "next_entropy": nxt["entropy"],
                    "deictic_s2": tok["s2"],
                    "era": meta.get("era", "?"),
                })
        elif t.isalpha() and len(t) >= 3:
            control_records.append(tok["s2"])


# -------------------------------------------------------------------
# 2. Per-category stats
# -------------------------------------------------------------------
def stats(vals):
    if not vals:
        return {"n": 0, "mean": 0.0, "median": 0.0, "pos_pct": 0.0, "max": 0.0}
    vals = sorted(vals)
    n = len(vals)
    return {
        "n": n,
        "mean": round(sum(vals) / n, 3),
        "median": round(vals[n // 2], 3),
        "pos_pct": round(100 * sum(1 for v in vals if v > 0) / n, 1),
        "max": round(max(vals), 2),
    }

def group_stats(records, key="category"):
    groups = defaultdict(list)
    for r in records:
        groups[r[key]].append(r["s2"])
    return {k: stats(v) for k, v in groups.items()}

cat_stats = group_stats(deictic_records)
ctrl_stats = stats(control_records)

print("=== DEICTIC TOKEN S₂ BY CATEGORY ===")
print(f"{'Category':<16} {'n':>5} {'mean S2':>8} {'median':>8} {'pos%':>6} {'max':>7}")
print("-" * 55)
for cat in ["temporal", "spatial", "demonstrative"]:
    s = cat_stats.get(cat, {"n": 0, "mean": 0, "median": 0, "pos_pct": 0, "max": 0})
    print(f"{cat:<16} {s['n']:>5} {s['mean']:>8.3f} {s['median']:>8.3f} {s['pos_pct']:>5.1f}% {s['max']:>7.2f}")
print(f"{'control (all)':16} {ctrl_stats['n']:>5} {ctrl_stats['mean']:>8.3f} {ctrl_stats['median']:>8.3f} {ctrl_stats['pos_pct']:>5.1f}% {ctrl_stats['max']:>7.2f}")


# -------------------------------------------------------------------
# 3. Per-token stats (within category)
# -------------------------------------------------------------------
print("\n=== TOP DEICTIC TOKENS BY MEAN S₂ ===")
token_groups = defaultdict(list)
for r in deictic_records:
    token_groups[(r["token"], r["category"])].append(r["s2"])

token_stats = [(tok, cat, stats(vals)) for (tok, cat), vals in token_groups.items() if len(vals) >= 3]
token_stats.sort(key=lambda x: -x[2]["mean"])
print(f"{'Token':<12} {'Cat':<14} {'n':>4} {'mean S2':>8} {'pos%':>6}")
for tok, cat, s in token_stats[:20]:
    print(f"{tok:<12} {cat:<14} {s['n']:>4} {s['mean']:>8.3f} {s['pos_pct']:>5.1f}%")


# -------------------------------------------------------------------
# 4. Post-deictic S2: what comes after a deictic?
# -------------------------------------------------------------------
print("\n=== POST-DEICTIC S₂ (token following deictic) ===")
post_groups = defaultdict(list)
for r in post_deictic:
    post_groups[r["category"]].append(r["next_s2"])

print(f"{'Category':<16} {'n':>5} {'post mean S2':>13} {'post median':>12}")
for cat in ["temporal", "spatial", "demonstrative"]:
    vals = post_groups.get(cat, [])
    s = stats(vals)
    print(f"{cat:<16} {s['n']:>5} {s['mean']:>13.3f} {s['median']:>12.3f}")

# compare: post-deictic vs. random position entropy
post_entropy = defaultdict(list)
for r in post_deictic:
    post_entropy[r["category"]].append(r["next_entropy"])
print("\nPost-deictic entropy (model openness after deictic):")
for cat in ["temporal", "spatial", "demonstrative"]:
    vals = post_entropy.get(cat, [])
    if vals:
        print(f"  {cat}: mean entropy = {sum(vals)/len(vals):.3f} nats over {len(vals)} tokens")


# -------------------------------------------------------------------
# 5. Most striking individual deictic moments
# -------------------------------------------------------------------
print("\n=== TOP 10 HIGHEST-S₂ DEICTIC MOMENTS ===")
sorted_deixis = sorted(deictic_records, key=lambda r: -r["s2"])
for r in sorted_deixis[:10]:
    print(f"  S₂={r['s2']:+.2f}  '{r['token']}'  — {r['author']}, '{r['title']}'  [{r['category']}]")


# -------------------------------------------------------------------
# 6. Poem-level: deictic density vs. mean S₂
# -------------------------------------------------------------------
print("\n=== POEM-LEVEL: DEICTIC DENSITY vs. S₂ ===")
poem_data_out = []
for poem in english_poems:
    tokens = poem["tokens"]
    meta = poem["metadata"]
    n = len(tokens)
    if n < 10:
        continue
    deictic_count = sum(1 for tok in tokens if classify(tok["token"]))
    density = deictic_count / n
    mean_s2 = sum(tok["s2"] for tok in tokens) / n
    poem_data_out.append({
        "title": meta["title"],
        "author": meta.get("author", "?"),
        "era": meta.get("era", "?"),
        "n_tokens": n,
        "deictic_count": deictic_count,
        "density": density,
        "mean_s2": mean_s2,
    })

# Group by density tercile
poem_data_out.sort(key=lambda x: x["density"])
tercile = len(poem_data_out) // 3
low = poem_data_out[:tercile]
mid = poem_data_out[tercile:2*tercile]
high = poem_data_out[2*tercile:]

def group_mean_s2(group):
    return sum(p["mean_s2"] for p in group) / len(group) if group else 0

print(f"{'Tercile':<12} {'n':>4} {'avg density':>12} {'avg poem S₂':>12}")
print(f"{'Low deixis':<12} {len(low):>4} {sum(p['density'] for p in low)/len(low):>12.3f} {group_mean_s2(low):>12.3f}")
print(f"{'Mid deixis':<12} {len(mid):>4} {sum(p['density'] for p in mid)/len(mid):>12.3f} {group_mean_s2(mid):>12.3f}")
print(f"{'High deixis':<12} {len(high):>4} {sum(p['density'] for p in high)/len(high):>12.3f} {group_mean_s2(high):>12.3f}")

print("\n--- Highest deictic density poems ---")
top_deictic_poems = sorted(poem_data_out, key=lambda x: -x["density"])[:10]
for p in top_deictic_poems:
    print(f"  {p['density']:.3f}  '{p['title']}'  ({p['author']})  mean_s2={p['mean_s2']:+.3f}  era={p['era']}")

print("\n--- Lowest deictic density poems ---")
for p in poem_data_out[:10]:
    print(f"  {p['density']:.3f}  '{p['title']}'  ({p['author']})  mean_s2={p['mean_s2']:+.3f}  era={p['era']}")


# -------------------------------------------------------------------
# 7. Era-level deictic density
# -------------------------------------------------------------------
print("\n=== ERA-LEVEL DEICTIC DENSITY ===")
era_density = defaultdict(list)
era_s2 = defaultdict(list)
for p in poem_data_out:
    era_density[p["era"]].append(p["density"])
    era_s2[p["era"]].append(p["mean_s2"])

era_summary = []
for era in era_density:
    dens = era_density[era]
    s2s = era_s2[era]
    era_summary.append((era, len(dens), sum(dens)/len(dens), sum(s2s)/len(s2s)))

era_summary.sort(key=lambda x: -x[2])
print(f"{'Era':<22} {'n':>3} {'avg density':>12} {'avg poem S₂':>12}")
for era, n, d, s in era_summary:
    print(f"{era:<22} {n:>3} {d:>12.3f} {s:>12.3f}")
