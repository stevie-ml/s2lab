"""
Modal Verbs and the Conditional Register in Poetry

Research question: Do modal auxiliaries (would, could, might, should, may, shall,
must, can, ought, will) create distinctive S₂ patterns? And what follows them?

Hypothesis — The 'Counterfactual Window':
Modal verbs suspend commitment to fact. "She would sing" opens a hypothetical
space where the actualization — what comes AFTER the modal — is the poet's
crucial creative decision. If the Straussian gap measures deviation from
expectation, post-modal positions may be the freest, most creative slots
in the poem: the model knows only that SOMETHING will actualize the modality,
but not what. Post-modal tokens should show high entropy (many possibilities)
and high S₂ (surprising actualizations).

Three modal sub-classes:
  DEONTIC    — must, should, ought  (obligation, necessity)
  EPISTEMIC  — might, may           (possibility, probability)
  VOLITIONAL — would, could, shall  (hypothetical, counterfactual, will)
  CAPABILITY — can, could           (ability; note: 'could' appears in both)

A secondary question: are modals themselves surprising at their position
(high S₂ modal tokens) or expected (low S₂)? The former would mean the
poet's *entry* into the conditional register is itself a Straussian move.
"""

import json
from collections import defaultdict

with open("results/corpus_results.json") as f:
    data = json.load(f)

# ── Modal lexicon with sub-classification ────────────────────────────────────
DEONTIC    = {"must", "should", "ought"}
EPISTEMIC  = {"might", "may"}
VOLITIONAL = {"would", "could", "shall", "will"}
CAPABILITY = {"can"}
ALL_MODALS = DEONTIC | EPISTEMIC | VOLITIONAL | CAPABILITY | {"could"}  # 'could' bridges

def modal_class(tok_str):
    t = tok_str.strip().lower().rstrip("'t")  # strip "'t" for wouldn't → would
    t = tok_str.strip().lower()
    # Handle contractions: wouldn't → would + n't
    base = t.replace("n't", "").replace("'t", "")
    if base in DEONTIC:   return "deontic"
    if base in EPISTEMIC: return "epistemic"
    if base in VOLITIONAL: return "volitional"
    if base in CAPABILITY: return "capability"
    if base == "could":   return "volitional"  # could = past/conditional of 'can'
    return None

# Precise match: strip and lowercase the full token
def classify_token(raw):
    t = raw.strip().lower()
    # Direct match
    if t in ALL_MODALS:
        if t in DEONTIC:    return "deontic"
        if t in EPISTEMIC:  return "epistemic"
        if t in VOLITIONAL: return "volitional"
        if t in CAPABILITY: return "capability"
    # Contraction form: wouldn't, couldn't, etc.
    for modal in ALL_MODALS:
        if t.startswith(modal) and t.endswith("n't"):
            if modal in DEONTIC:    return "deontic"
            if modal in EPISTEMIC:  return "epistemic"
            if modal in VOLITIONAL: return "volitional"
            if modal in CAPABILITY: return "capability"
    return None

# ── Corpus filtering ─────────────────────────────────────────────────────────
english_poems  = [p for p in data
                  if p["metadata"].get("language", "en") == "en"
                  and p["metadata"].get("era") != "control"]
english_prose  = [p for p in data
                  if p["metadata"].get("language", "en") == "en"
                  and p["metadata"].get("era") == "control"]

# ── Data collection ──────────────────────────────────────────────────────────
modal_records   = []   # one per modal token occurrence
post_modal      = []   # token immediately following a modal
control_s2      = []   # all non-modal, alphabetic tokens (baseline)
poem_profiles   = []   # per-poem aggregate

for corpus_label, corpus in [("poetry", english_poems), ("prose", english_prose)]:
    for poem in corpus:
        tokens = poem["tokens"]
        meta   = poem["metadata"]
        n      = len(tokens)
        if n < 5:
            continue

        modal_s2_vals = []
        non_modal_s2  = []

        for i, tok in enumerate(tokens):
            raw = tok["token"]
            cls = classify_token(raw)

            if cls:
                rec = {
                    "modal": raw.strip().lower(),
                    "class": cls,
                    "s2":    tok["s2"],
                    "surprisal": tok["surprisal"],
                    "entropy":   tok["entropy"],
                    "title":  meta["title"],
                    "author": meta.get("author", "?"),
                    "era":    meta.get("era", "?"),
                    "corpus": corpus_label,
                }
                modal_records.append(rec)
                modal_s2_vals.append(tok["s2"])

                # Post-modal token
                if i + 1 < len(tokens):
                    nxt = tokens[i + 1]
                    post_modal.append({
                        "modal":       raw.strip().lower(),
                        "class":       cls,
                        "post_token":  nxt["token"].strip(),
                        "post_s2":     nxt["s2"],
                        "post_entropy": tok["entropy"],   # entropy AT modal = openness
                        "modal_s2":    tok["s2"],
                        "era":         meta.get("era", "?"),
                        "corpus":      corpus_label,
                    })
            else:
                t = raw.strip().lower()
                if t.isalpha() and len(t) >= 3:
                    non_modal_s2.append(tok["s2"])
                    if corpus_label == "poetry":
                        control_s2.append(tok["s2"])

        # Poem profile
        mean_s2 = sum(t["s2"] for t in tokens) / n if n else 0
        modal_count = len(modal_s2_vals)
        modal_density = modal_count / n if n else 0
        poem_profiles.append({
            "title":         meta["title"],
            "author":        meta.get("author", "?"),
            "era":           meta.get("era", "?"),
            "corpus":        corpus_label,
            "n_tokens":      n,
            "modal_count":   modal_count,
            "modal_density": modal_density,
            "mean_modal_s2": (sum(modal_s2_vals) / len(modal_s2_vals)) if modal_s2_vals else None,
            "mean_poem_s2":  mean_s2,
        })


# ── Statistics helpers ────────────────────────────────────────────────────────
def stats(vals):
    if not vals:
        return {"n": 0, "mean": 0.0, "median": 0.0, "pos_pct": 0.0, "max": 0.0}
    vals = sorted(vals)
    n = len(vals)
    return {
        "n":       n,
        "mean":    round(sum(vals) / n, 3),
        "median":  round(vals[n // 2], 3),
        "pos_pct": round(100 * sum(1 for v in vals if v > 0) / n, 1),
        "max":     round(max(vals), 2),
    }

def group_stats(records, key):
    groups = defaultdict(list)
    for r in records:
        groups[r[key]].append(r["s2"])
    return {k: stats(v) for k, v in groups.items()}


# ═══════════════════════════════════════════════════════════════════════════════
# 1. Modal token S₂ by class, compared to corpus baseline
# ═══════════════════════════════════════════════════════════════════════════════
print("=== 1. MODAL TOKEN S₂ BY CLASS (poetry) ===")
poetry_modals = [r for r in modal_records if r["corpus"] == "poetry"]
by_class = defaultdict(list)
for r in poetry_modals:
    by_class[r["class"]].append(r["s2"])

ctrl = stats(control_s2)
print(f"{'Class':<14} {'n':>5} {'mean S₂':>8} {'median':>8} {'pos%':>6} {'max':>7}")
print("-" * 52)
for cls in ["deontic", "epistemic", "volitional", "capability"]:
    s = stats(by_class.get(cls, []))
    print(f"{cls:<14} {s['n']:>5} {s['mean']:>8.3f} {s['median']:>8.3f} {s['pos_pct']:>5.1f}% {s['max']:>7.2f}")
print(f"{'baseline':14} {ctrl['n']:>5} {ctrl['mean']:>8.3f} {ctrl['median']:>8.3f} {ctrl['pos_pct']:>5.1f}% {ctrl['max']:>7.2f}")


# ═══════════════════════════════════════════════════════════════════════════════
# 2. Poetry vs prose: are modals more or less surprising in each context?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 2. MODAL S₂: POETRY vs. PROSE ===")
for corpus_label in ["poetry", "prose"]:
    records = [r for r in modal_records if r["corpus"] == corpus_label]
    s = stats([r["s2"] for r in records])
    print(f"  {corpus_label}: n={s['n']}, mean S₂={s['mean']:.3f}, pos%={s['pos_pct']:.1f}%")


# ═══════════════════════════════════════════════════════════════════════════════
# 3. Post-modal S₂: the 'counterfactual window'
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 3. POST-MODAL S₂ (token following modal) — poetry only ===")
poetry_post = [r for r in post_modal if r["corpus"] == "poetry"]

by_class_post = defaultdict(list)
by_class_entropy = defaultdict(list)
for r in poetry_post:
    by_class_post[r["class"]].append(r["post_s2"])
    by_class_entropy[r["class"]].append(r["post_entropy"])

print(f"{'Class':<14} {'n':>5} {'post mean S₂':>13} {'post pos%':>9} {'modal entropy':>14}")
print("-" * 60)
for cls in ["deontic", "epistemic", "volitional", "capability"]:
    s_post = stats(by_class_post.get(cls, []))
    ent_vals = by_class_entropy.get(cls, [])
    mean_ent = round(sum(ent_vals) / len(ent_vals), 3) if ent_vals else 0
    print(f"{cls:<14} {s_post['n']:>5} {s_post['mean']:>13.3f} {s_post['pos_pct']:>8.1f}% {mean_ent:>14.3f}")

# Baseline: post-random tokens
all_poetry_s2 = [t["s2"] for p in english_poems for t in p["tokens"]]
baseline_post = stats(all_poetry_s2)
print(f"{'baseline':14} {'—':>5} {baseline_post['mean']:>13.3f} {baseline_post['pos_pct']:>8.1f}% {'—':>14}")


# ═══════════════════════════════════════════════════════════════════════════════
# 4. Individual modal word analysis (which specific modals are most surprising?)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 4. INDIVIDUAL MODAL WORDS: MEAN S₂ ===")
by_word = defaultdict(list)
for r in poetry_modals:
    by_word[r["modal"]].append(r["s2"])

word_stats = [(word, stats(vals)) for word, vals in by_word.items() if len(vals) >= 2]
word_stats.sort(key=lambda x: -x[1]["mean"])
print(f"{'Modal':<12} {'n':>4} {'mean S₂':>8} {'pos%':>6}")
for word, s in word_stats:
    print(f"{word:<12} {s['n']:>4} {s['mean']:>8.3f} {s['pos_pct']:>5.1f}%")


# ═══════════════════════════════════════════════════════════════════════════════
# 5. Top post-modal surprises (most surprising actualizations)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 5. TOP 15 HIGHEST-S₂ POST-MODAL MOMENTS ===")
sorted_post = sorted(poetry_post, key=lambda r: -r["post_s2"])
for r in sorted_post[:15]:
    print(f"  S₂={r['post_s2']:+.2f}  '{r['modal']} {r['post_token']}'  — era={r['era']}")


# ═══════════════════════════════════════════════════════════════════════════════
# 6. Modal density vs poem-level S₂
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 6. MODAL DENSITY vs. POEM-LEVEL MEAN S₂ ===")
poetry_profiles = [p for p in poem_profiles if p["corpus"] == "poetry" and p["modal_count"] > 0]

# Tercile split
poetry_profiles.sort(key=lambda x: x["modal_density"])
n3 = len(poetry_profiles) // 3
low_density   = poetry_profiles[:n3]
mid_density   = poetry_profiles[n3:2*n3]
high_density  = poetry_profiles[2*n3:]

for label, group in [("low",  low_density),
                     ("mid",  mid_density),
                     ("high", high_density)]:
    s2_vals = [p["mean_poem_s2"] for p in group]
    dens    = [p["modal_density"] for p in group]
    print(f"  {label} modal density: mean density={sum(dens)/len(dens):.3f}, "
          f"mean poem S₂={sum(s2_vals)/len(s2_vals):.3f}  (n={len(group)})")

print("\nTop 5 poems by modal density (poetry):")
poetry_profiles.sort(key=lambda x: -x["modal_density"])
for p in poetry_profiles[:5]:
    print(f"  density={p['modal_density']:.3f}  n_modal={p['modal_count']}  "
          f"mean_s2={p['mean_poem_s2']:.3f}  '{p['title']}' ({p['era']})")


# ═══════════════════════════════════════════════════════════════════════════════
# 7. Epistemic vs Volitional in high-S₂ moments
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 7. CLASS DISTRIBUTION IN HIGH-S₂ vs. LOW-S₂ MODAL WINDOWS ===")
# Define high-S₂ post-modal as post_s2 > 2.0
high_post = [r for r in poetry_post if r["post_s2"] > 2.0]
low_post  = [r for r in poetry_post if r["post_s2"] < -1.0]

def class_distribution(records):
    counts = defaultdict(int)
    for r in records:
        counts[r["class"]] += 1
    total = sum(counts.values())
    return {k: round(100*v/total, 1) for k, v in counts.items()} if total else {}

print(f"High-S₂ post-modal (post_s2 > 2.0): n={len(high_post)}")
dist = class_distribution(high_post)
for cls, pct in sorted(dist.items(), key=lambda x: -x[1]):
    print(f"  {cls}: {pct:.1f}%")

print(f"\nLow-S₂ post-modal (post_s2 < -1.0): n={len(low_post)}")
dist2 = class_distribution(low_post)
for cls, pct in sorted(dist2.items(), key=lambda x: -x[1]):
    print(f"  {cls}: {pct:.1f}%")


# ═══════════════════════════════════════════════════════════════════════════════
# 8. Era analysis: which eras use modals most / least surprisingly?
# ═══════════════════════════════════════════════════════════════════════════════
print("\n=== 8. ERA-LEVEL MODAL S₂ ===")
era_modal_s2 = defaultdict(list)
for r in poetry_modals:
    era_modal_s2[r["era"]].append(r["s2"])

era_stats = [(era, stats(vals)) for era, vals in era_modal_s2.items() if len(vals) >= 3]
era_stats.sort(key=lambda x: -x[1]["mean"])
print(f"{'Era':<24} {'n':>4} {'mean S₂':>8}")
for era, s in era_stats:
    print(f"{era:<24} {s['n']:>4} {s['mean']:>8.3f}")
