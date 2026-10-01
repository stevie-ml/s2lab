"""
Experiment: The Negative Capability Index

Keats coined 'negative capability' to describe the capacity to be in 'uncertainties,
Mysteries, doubts, without any irritable reaching after fact & reason.'
Information-theoretically, we can operationalize this:

When GPT-2 is UNCERTAIN (high entropy), the poet faces a choice:
  - Accept a conventional option (S2 < 0: the poet chose something GPT-2 expected)
  - Force an unexpected choice (S2 > 0: the poet resisted the ambiguity)

The NEGATIVE CAPABILITY INDEX is the fraction of HIGH-ENTROPY positions where
the poet accepts the conventional choice (S2 ≤ 0), weighted by entropy level.

Hypothesis: Poets known for holding ambiguity (Keats, Dickinson, Coleridge)
will show higher NC indices than poets known for assertive resolution
(Milton, Pope, Whitman).

Secondary question: Does negative capability correlate with era (Romantic vs
Modernist vs Contemporary) or with poem form?

Date: 2026-10-01
"""

import json
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
FINDINGS_PATH = "findings/negative_capability_index.md"

# Load data
with open(RESULTS_PATH) as f:
    data = json.load(f)

# Compute corpus-wide entropy quartiles (artifact-filtered)
all_entropy = []
for poem in data:
    for tok in poem["tokens"]:
        if tok.get("p_newline", 0) < 0.9:
            all_entropy.append(tok["entropy"])

all_entropy.sort()
n = len(all_entropy)
q1 = all_entropy[n // 4]
median_e = all_entropy[n // 2]
q3 = all_entropy[3 * n // 4]
high_entropy_threshold = q3  # top quartile = "high entropy"

print(f"Corpus entropy quartiles: Q1={q1:.2f}, Q2={median_e:.2f}, Q3={q3:.2f}")
print(f"High-entropy threshold: {high_entropy_threshold:.2f}")
print(f"Total artifact-filtered tokens: {n}")

# ─── Per-poet analysis ───────────────────────────────────────────────────────
# For each poet: compute NC index, separate stats at high/mid/low entropy

poet_stats = defaultdict(lambda: {
    "n_he_tokens": 0,     # high entropy
    "n_he_conform": 0,    # high entropy + S2 <= 0
    "n_he_resist": 0,     # high entropy + S2 > 0
    "he_s2_values": [],
    "n_le_tokens": 0,     # low entropy (< median)
    "n_le_conform": 0,
    "n_le_resist": 0,
    "le_s2_values": [],
    "n_poems": 0,
    "titles": [],
    "era": None,
    "total_tokens": 0,
    "all_s2": [],
})

era_stats = defaultdict(lambda: {
    "n_he_tokens": 0,
    "n_he_conform": 0,
    "he_s2_values": [],
    "n_le_tokens": 0,
    "n_le_conform": 0,
    "le_s2_values": [],
    "n_poems": 0,
    "poets": set(),
})

for poem in data:
    meta = poem.get("metadata", {})
    author = meta.get("author", "Unknown")
    era = meta.get("era", "unknown")
    lang = meta.get("language", "en")

    # Only English poems for poet-level analysis
    if lang != "en":
        continue
    # Exclude control/cliche texts
    if era in ("control", "cliche_control"):
        continue

    poet_stats[author]["n_poems"] += 1
    poet_stats[author]["titles"].append(meta.get("title", "?"))
    poet_stats[author]["era"] = era
    era_stats[era]["n_poems"] += 1
    era_stats[era]["poets"].add(author)

    for tok in poem["tokens"]:
        # Artifact filter
        if tok.get("p_newline", 0) >= 0.9:
            continue

        e = tok["entropy"]
        s2 = tok["s2"]
        poet_stats[author]["total_tokens"] += 1
        poet_stats[author]["all_s2"].append(s2)

        if e >= high_entropy_threshold:
            poet_stats[author]["n_he_tokens"] += 1
            poet_stats[author]["he_s2_values"].append(s2)
            era_stats[era]["n_he_tokens"] += 1
            era_stats[era]["he_s2_values"].append(s2)
            if s2 <= 0:
                poet_stats[author]["n_he_conform"] += 1
                era_stats[era]["n_he_conform"] += 1
            else:
                poet_stats[author]["n_he_resist"] += 1
        elif e < median_e:
            poet_stats[author]["n_le_tokens"] += 1
            poet_stats[author]["le_s2_values"].append(s2)
            era_stats[era]["n_le_tokens"] += 1
            era_stats[era]["le_s2_values"].append(s2)
            if s2 <= 0:
                poet_stats[author]["n_le_conform"] += 1
                era_stats[era]["n_le_conform"] += 1

# ─── Compute NC index ──────────────────────────────────────────────────────
# NC index = fraction of high-entropy tokens where poet conforms (S2 ≤ 0)
# (Higher = more "negative capability" = accepting ambiguity conventionally)

def nc_index(stats):
    n = stats["n_he_tokens"]
    if n < 10:
        return None
    return stats["n_he_conform"] / n

def le_conform_rate(stats):
    n = stats["n_le_tokens"]
    if n < 10:
        return None
    return stats["n_le_conform"] / n

def mean_safe(lst):
    return round(statistics.mean(lst), 3) if lst else None

# ─── Sort poets by NC index ───────────────────────────────────────────────
poet_nc = []
for poet, st in poet_stats.items():
    nc = nc_index(st)
    if nc is None:
        continue
    avg_he_s2 = mean_safe(st["he_s2_values"])
    avg_le_s2 = mean_safe(st["le_s2_values"])
    avg_s2 = mean_safe(st["all_s2"])
    le_rate = le_conform_rate(st)
    poet_nc.append({
        "poet": poet,
        "era": st["era"],
        "n_poems": st["n_poems"],
        "n_he": st["n_he_tokens"],
        "nc_index": nc,
        "le_conform_rate": le_rate,
        "avg_he_s2": avg_he_s2,
        "avg_le_s2": avg_le_s2,
        "avg_s2": avg_s2,
        "resistance_ratio": st["n_he_resist"] / st["n_he_tokens"],
    })

poet_nc.sort(key=lambda x: -x["nc_index"])

# ─── Era NC index ─────────────────────────────────────────────────────────
era_nc = []
for era, st in era_stats.items():
    nc = nc_index(st)
    if nc is None:
        continue
    era_nc.append({
        "era": era,
        "n_poems": st["n_poems"],
        "n_poets": len(st["poets"]),
        "n_he": st["n_he_tokens"],
        "nc_index": nc,
        "avg_he_s2": mean_safe(st["he_s2_values"]),
        "avg_le_s2": mean_safe(st["le_s2_values"]),
    })

era_nc.sort(key=lambda x: -x["nc_index"])

# ─── The "Delta NC" — gap between high-entropy and low-entropy conform rates ─
# Poets with high delta NC are ESPECIALLY conformist at high-entropy moments
# (over and above their baseline conformism at low-entropy moments)
# This is the purest measure of Keatsian "acceptance of ambiguity"

print("\nTop-20 poets by NC index (high-entropy conformism):")
for p in poet_nc[:20]:
    delta = (p["nc_index"] - (p["le_conform_rate"] or 0))
    print(f"  {p['poet']} ({p['era']}) NC={p['nc_index']:.3f} "
          f"ΔNC={delta:+.3f} avgS2_HE={p['avg_he_s2']:.2f}")

print("\nBottom-10 poets (lowest NC = most resistant to ambiguity):")
for p in poet_nc[-10:]:
    print(f"  {p['poet']} ({p['era']}) NC={p['nc_index']:.3f}")

print("\nEra NC indices:")
for e in era_nc:
    print(f"  {e['era']}: NC={e['nc_index']:.3f} n_poems={e['n_poems']}")

# ─── Compute delta_nc for each poet ────────────────────────────────────────
for p in poet_nc:
    p["delta_nc"] = p["nc_index"] - (p["le_conform_rate"] or 0)

poet_nc_sorted_delta = sorted(poet_nc, key=lambda x: -x["delta_nc"])

# ─── Corpus-wide baseline ─────────────────────────────────────────────────
all_he_s2 = []
all_le_s2 = []
n_he_conform_total = 0
n_he_total = 0
n_le_conform_total = 0
n_le_total = 0

for poem in data:
    meta = poem.get("metadata", {})
    era = meta.get("era", "unknown")
    lang = meta.get("language", "en")
    if lang != "en" or era in ("control", "cliche_control"):
        continue
    for tok in poem["tokens"]:
        if tok.get("p_newline", 0) >= 0.9:
            continue
        e = tok["entropy"]
        s2 = tok["s2"]
        if e >= high_entropy_threshold:
            all_he_s2.append(s2)
            n_he_total += 1
            if s2 <= 0:
                n_he_conform_total += 1
        elif e < median_e:
            all_le_s2.append(s2)
            n_le_total += 1
            if s2 <= 0:
                n_le_conform_total += 1

corpus_nc = n_he_conform_total / n_he_total
corpus_le = n_le_conform_total / n_le_total
print(f"\nCorpus-wide: NC_index={corpus_nc:.3f}, LE_conform={corpus_le:.3f}, ΔNC={corpus_nc-corpus_le:+.3f}")
print(f"Avg S2 at HIGH-entropy positions: {statistics.mean(all_he_s2):.3f}")
print(f"Avg S2 at LOW-entropy positions: {statistics.mean(all_le_s2):.3f}")

# ─── Write findings ────────────────────────────────────────────────────────
md_lines = [
    "# The Negative Capability Index: Poetry and the Acceptance of Ambiguity",
    "",
    "**Date:** 2026-10-01",
    "**Experiment:** `experiments/negative_capability_index.py`",
    "**Corpus:** English poetry texts from `results/corpus_results.json`, stanza-break artifact filtered",
    "**Builds on:** `straussian_gap_taxonomy.md`, `s2_transition_entropy.md`, `surprise_taxonomy_2x2.md`",
    "",
    "---",
    "",
    "## Research Question",
    "",
    'Keats coined "negative capability" to describe "the capacity to be in uncertainties, Mysteries, doubts, without any irritable reaching after fact & reason."',
    "Can information theory operationalize this concept?",
    "",
    "When GPT-2 is **uncertain** (high entropy), the poet faces two paths:",
    "1. **Accept ambiguity** (S₂ ≤ 0): Choose a word GPT-2 expects — let the ambiguity stand, unforcefully resolved",
    "2. **Resist ambiguity** (S₂ > 0): Choose a word GPT-2 does NOT expect — impose a specific, unexpected resolution",
    "",
    "**The Negative Capability Index (NC)** = fraction of high-entropy positions where the poet accepts a conventional choice.",
    "Higher NC → more 'Keatsian' acceptance of uncertainty.",
    "Lower NC → more assertive resistance to the model's ambiguity.",
    "",
    "---",
    "",
    "## Method",
    "",
    "- Filtered all tokens (stanza-break artifact removed: p_newline < 0.9)",
    f"- Computed corpus-wide entropy quartiles: Q1={q1:.2f}, Q2={median_e:.2f}, Q3={q3:.2f} bits",
    f"- **High-entropy threshold**: top quartile (H ≥ {high_entropy_threshold:.2f} bits)",
    f"- Low-entropy zone: H < {median_e:.2f} bits",
    "- NC Index = fraction of high-entropy tokens where S₂ ≤ 0",
    "- ΔNC = NC_index − LE_conform_rate (net 'high-entropy acceptance above baseline')",
    "- Restricted to English poetry; excluded control/cliché texts",
    "",
    "---",
    "",
    "## Finding 1: Corpus-Wide Baseline",
    "",
    f"| Zone | N tokens | Conform rate (S₂ ≤ 0) | Avg S₂ |",
    "|---|---|---|---|",
    f"| High entropy (H ≥ {high_entropy_threshold:.1f}) | {n_he_total:,} | **{corpus_nc:.1%}** | {statistics.mean(all_he_s2):.3f} |",
    f"| Low entropy (H < {median_e:.1f}) | {n_le_total:,} | **{corpus_le:.1%}** | {statistics.mean(all_le_s2):.3f} |",
    "",
    f"Corpus-wide ΔNC (high vs low entropy conformism): **{corpus_nc - corpus_le:+.3f}**",
    "",
    f"At high-entropy positions, poets conform {corpus_nc:.1%} of the time.",
    f"At low-entropy positions, they conform {corpus_le:.1%} of the time.",
    "",
]

if corpus_nc > corpus_le:
    md_lines.append(
        "**Poets are actually MORE conventional at uncertain positions** — when the model doesn't know what comes next, "
        "poets tend to choose expected words. This is the corpus-wide 'negative capability' signal."
    )
else:
    md_lines.append(
        "**Poets are LESS conventional at uncertain positions** — when the model doesn't know what comes next, "
        "poets tend to push further into the unexpected. Uncertainty invites resistance, not acceptance."
    )

md_lines += [
    "",
    "---",
    "",
    "## Finding 2: Era Profiles — Which Literary Movements Accept Ambiguity?",
    "",
    "| Era | n poems | n poets | NC Index | Avg S₂ at HE | Avg S₂ at LE |",
    "|---|---|---|---|---|---|",
]
for e in era_nc:
    md_lines.append(
        f"| {e['era']} | {e['n_poems']} | {e['n_poets']} | "
        f"**{e['nc_index']:.3f}** | {e['avg_he_s2']:.3f} | {e['avg_le_s2']:.3f} |"
    )

# Identify era patterns
highest_nc_era = era_nc[0]
lowest_nc_era = era_nc[-1]

md_lines += [
    "",
    f"**Most 'negatively capable' era** (accepts uncertainty most): **{highest_nc_era['era']}** (NC={highest_nc_era['nc_index']:.3f})",
    f"**Least 'negatively capable' era** (resists uncertainty most): **{lowest_nc_era['era']}** (NC={lowest_nc_era['nc_index']:.3f})",
    "",
    "---",
    "",
    "## Finding 3: Poet-Level NC Index — The Full Ranking",
    "",
    "NC Index: fraction of high-entropy positions where S₂ ≤ 0 (poet accepts conventional choice).",
    "ΔNC: NC minus the poet's baseline low-entropy conform rate (net uncertainty-acceptance).",
    "",
    "| Poet | Era | n poems | NC Index | ΔNC | Avg HE S₂ |",
    "|---|---|---|---|---|---|",
]

for p in poet_nc_sorted_delta:
    delta_str = f"{p['delta_nc']:+.3f}"
    md_lines.append(
        f"| {p['poet']} | {p['era']} | {p['n_poems']} | "
        f"{p['nc_index']:.3f} | **{delta_str}** | {p['avg_he_s2']:.3f} |"
    )

# Identify notable examples
top_nc_poets = [p for p in poet_nc_sorted_delta if p['n_he'] >= 20][:5]
bottom_nc_poets = sorted([p for p in poet_nc_sorted_delta if p['n_he'] >= 20], key=lambda x: x["delta_nc"])[:5]

md_lines += [
    "",
    "---",
    "",
    "## Finding 4: The Ambiguity Gap — High vs. Low Entropy S₂ Contrast",
    "",
    "How much does S₂ CHANGE between high-entropy and low-entropy positions?",
    "A large positive gap means the poet writes unexpectedly at uncertain moments.",
    "A near-zero or negative gap means the poet's behavior is similar regardless of context uncertainty.",
    "",
    "| Poet | Era | Avg S₂ (HE) | Avg S₂ (LE) | S₂ Gap (HE−LE) |",
    "|---|---|---|---|---|",
]

poet_by_s2_gap = sorted(
    [p for p in poet_nc if p["avg_he_s2"] is not None and p["avg_le_s2"] is not None and p["n_he"] >= 15],
    key=lambda x: x["avg_he_s2"] - x["avg_le_s2"],
    reverse=True
)

for p in poet_by_s2_gap[:25]:
    gap = p["avg_he_s2"] - p["avg_le_s2"]
    md_lines.append(
        f"| {p['poet']} | {p['era']} | {p['avg_he_s2']:.3f} | {p['avg_le_s2']:.3f} | **{gap:+.3f}** |"
    )

md_lines += [
    "",
    "---",
    "",
    "## Interpretation: Two Strategies for Uncertainty",
    "",
    "The poet who faces high entropy (the model is uncertain about what comes next) can:",
    "",
    "### Strategy A — 'Acceptance' (High NC Index)",
    "Choose something GPT-2 would have predicted. This is NOT laziness — it's knowing that when language opens up into multiple valid paths, the most resonant choice is often the one that:",
    "- Honors the semantic field already established",
    "- Respects the sound pattern the line has built",
    "- Lets the image speak without forced cleverness",
    "",
    "### Strategy B — 'Resistance' (Low NC Index, High S₂ at HE)",
    "Choose something GPT-2 would NOT have predicted, even though many valid choices exist.",
    "This is the poet forcing specificity into openness — imposing particularity where language was genuinely uncertain.",
    "",
    "Neither strategy is inherently better. Keats prized Strategy A for lyric resolution.",
    "Modernists (Pound's 'Make it new') arguably practice Strategy B: resist the expected at every turn.",
    "",
    "---",
    "",
    "## Suggested Next Steps",
    "",
    "1. **Stanza-level NC trajectories**: does a poet's NC index change over the course of a single poem?",
    "2. **Form and NC**: do sonnets (with formal constraint) force Strategy A or B more than free verse?",
    "3. **NC and critical reception**: do poets with higher NC index receive different critical vocabulary (ambiguous, mysterious, suggestive) vs. lower NC (vivid, concrete, direct)?",
    "4. **Multi-model test**: does GPT-2-medium show the same NC ranking, or is 'uncertainty' model-dependent?",
    "",
]

with open(FINDINGS_PATH, "w") as f:
    f.write("\n".join(md_lines))

print(f"\nFindings written to {FINDINGS_PATH}")

# Save key stats as JSON for future experiments
import json as json_mod
results_out = {
    "corpus_nc_index": corpus_nc,
    "corpus_le_conform": corpus_le,
    "delta_nc_corpus": corpus_nc - corpus_le,
    "high_entropy_threshold": high_entropy_threshold,
    "median_entropy": median_e,
    "poet_nc_table": poet_nc_sorted_delta,
    "era_nc_table": era_nc,
}
with open("results/negative_capability_results.json", "w") as f:
    json_mod.dump(results_out, f, indent=2)
print("Results saved to results/negative_capability_results.json")
