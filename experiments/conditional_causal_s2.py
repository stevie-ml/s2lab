"""
Conditional and Causal Connectives: S2 Analysis of Logical Structures in Poetry

Research question: When poets use logical connectives (if, unless, because, when, etc.),
does the S2 of what follows differ from baseline? Do these connectives create "open" or
"constrained" contexts for the words that follow them?

Different connectives encode different epistemic stances:
- Conditional (if/unless): opens possibility space — what MIGHT happen
- Temporal (when/until/while): specifies time relation — what DOES happen at time X
- Causal (because/since): closes causal chain — what EXPLAINS something
- Concessive (although/though/even): signals contrast — what is TRUE DESPITE something

The theory: if-conditionals should produce high entropy (anything is possible in the
hypothetical space), causal connectives should produce low entropy (the cause must fit the
effect), and concessive connectives should produce HIGH S2 (the poet is setting up a
surprise that works AGAINST expectation).
"""

import json
import re
from collections import defaultdict
import statistics

# Load corpus
with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# Connective categories with semantic roles
CONNECTIVE_CATEGORIES = {
    "conditional": ["if", "unless", "whether"],
    "temporal": ["when", "whenever", "until", "while", "before", "after", "once", "since"],
    "causal": ["because", "since", "therefore", "thus", "hence", "so"],
    "concessive": ["although", "though", "even", "despite", "yet", "still", "however"],
    "comparative": ["like", "as", "than"],  # included for cross-reference with simile work
}

# Flatten to lookup
ALL_CONNECTIVES = {}
for cat, words in CONNECTIVE_CATEGORIES.items():
    for w in words:
        ALL_CONNECTIVES[w.lower()] = cat

# Note: "since" appears in both temporal and causal; we'll record which category wins by context
AMBIGUOUS = {"since"}  # will count in both

def clean_token(token):
    """Normalize token text for matching."""
    return token.strip().lower().lstrip("Ġ").lstrip(" ").strip(".,;:!?\"'()")

def is_artifact(token_data):
    """Filter stanza-break artifacts."""
    return token_data.get("p_newline", 0) >= 0.9

def get_windows(tokens, position, window_size=3):
    """Get tokens at positions +1, +2, +3 after position, excluding artifacts."""
    results = []
    j = position + 1
    while j < len(tokens) and len(results) < window_size:
        if not is_artifact(tokens[j]):
            results.append((len(results) + 1, tokens[j]))  # (offset, token)
        j += 1
    return results

# Collect data
# Structure: {category: {offset: [s2_values], "entropy": [H_values]}}
connective_data = defaultdict(lambda: defaultdict(list))
connective_examples = defaultdict(list)
baseline_s2 = []
baseline_entropy = []

# Per-poem stats
poem_connective_counts = defaultdict(lambda: defaultdict(int))  # poem title → {cat: count}

for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]

    # Skip non-poetry and non-English
    if meta.get("era") == "control" or meta.get("language", "en") not in ["en", "english"]:
        continue
    if meta.get("era") in ["cliche_control"]:
        continue

    # Gather baseline (all non-artifact tokens)
    for t in tokens:
        if not is_artifact(t):
            baseline_s2.append(t["s2"])
            baseline_entropy.append(t["entropy"])

    # Find connective positions
    for i, t in enumerate(tokens):
        if is_artifact(t):
            continue

        cleaned = clean_token(t["token"])

        if cleaned not in ALL_CONNECTIVES:
            continue

        cat = ALL_CONNECTIVES[cleaned]

        # Get window of next N tokens
        window = get_windows(tokens, i, window_size=5)

        if not window:
            continue

        # Record the connective itself
        connective_data[cat]["connective_s2"].append(t["s2"])
        connective_data[cat]["connective_entropy"].append(t["entropy"])

        # Record following tokens
        for offset, tok in window:
            key_s2 = f"s2_+{offset}"
            key_h = f"entropy_+{offset}"
            connective_data[cat][key_s2].append(tok["s2"])
            connective_data[cat][key_h].append(tok["entropy"])

        # Record examples for high-S2 moments after connective
        if window and window[0][1]["s2"] > 3.0:
            connective_examples[cat].append({
                "poem": meta["title"],
                "author": meta["author"],
                "era": meta["era"],
                "connective": t["token"],
                "context": t["context_before"][-30:] if t.get("context_before") else "",
                "next_token": window[0][1]["token"],
                "next_s2": window[0][1]["s2"],
                "connective_entropy": t["entropy"],
            })

        poem_connective_counts[meta["title"]][cat] += 1

# --- Analysis ---
print("=" * 70)
print("CONDITIONAL AND CAUSAL CONNECTIVES: S2 PROFILE ANALYSIS")
print("=" * 70)

baseline_mean = statistics.mean(baseline_s2)
baseline_med = statistics.median(baseline_s2)
baseline_h_mean = statistics.mean(baseline_entropy)
print(f"\nBaseline (all non-artifact poetry tokens):")
print(f"  N = {len(baseline_s2)}")
print(f"  mean S2 = {baseline_mean:.3f}")
print(f"  median S2 = {baseline_med:.3f}")
print(f"  mean entropy = {baseline_h_mean:.3f}")

print("\n" + "=" * 70)
print("CONNECTIVE CATEGORY SUMMARY")
print("=" * 70)

results_by_cat = {}
for cat in CONNECTIVE_CATEGORIES:
    data = connective_data[cat]

    if "s2_+1" not in data or len(data["s2_+1"]) < 5:
        continue

    n = len(data["connective_s2"])
    s2_at = data["connective_s2"]
    h_at = data["connective_entropy"]
    s2_1 = data.get("s2_+1", [])
    s2_2 = data.get("s2_+2", [])
    s2_3 = data.get("s2_+3", [])
    h_1 = data.get("entropy_+1", [])

    mean_s2_at = statistics.mean(s2_at) if s2_at else float('nan')
    mean_h_at = statistics.mean(h_at) if h_at else float('nan')
    mean_s2_1 = statistics.mean(s2_1) if s2_1 else float('nan')
    mean_s2_2 = statistics.mean(s2_2) if s2_2 else float('nan')
    mean_s2_3 = statistics.mean(s2_3) if s2_3 else float('nan')
    mean_h_1 = statistics.mean(h_1) if h_1 else float('nan')

    pos_ratio_1 = sum(1 for x in s2_1 if x > 0) / len(s2_1) if s2_1 else float('nan')

    results_by_cat[cat] = {
        "n_instances": n,
        "mean_entropy_at_connective": mean_h_at,
        "mean_s2_at_connective": mean_s2_at,
        "mean_s2_+1": mean_s2_1,
        "mean_s2_+2": mean_s2_2,
        "mean_s2_+3": mean_s2_3,
        "mean_entropy_+1": mean_h_1,
        "pos_ratio_+1": pos_ratio_1,
        "s2_delta_vs_baseline_+1": mean_s2_1 - baseline_mean,
        "entropy_delta_vs_baseline_+1": mean_h_1 - baseline_h_mean,
    }

    print(f"\n  [{cat.upper()}] n={n} instances")
    print(f"    Entropy at connective:    {mean_h_at:.2f} bits  (vs baseline {baseline_h_mean:.2f})")
    print(f"    S2 at connective:         {mean_s2_at:.3f}")
    print(f"    S2 at +1 token:           {mean_s2_1:.3f}  (Δ {mean_s2_1 - baseline_mean:+.3f} vs baseline)")
    print(f"    S2 at +2 token:           {mean_s2_2:.3f}")
    print(f"    S2 at +3 token:           {mean_s2_3:.3f}")
    print(f"    Entropy at +1 token:      {mean_h_1:.2f} bits  (Δ {mean_h_1 - baseline_h_mean:+.2f})")
    print(f"    +S2 ratio at +1:          {pos_ratio_1:.1%}")

# --- Individual connective breakdown ---
print("\n" + "=" * 70)
print("INDIVIDUAL CONNECTIVE BREAKDOWN (top 10 by frequency)")
print("=" * 70)

word_stats = {}
for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]
    if meta.get("era") in ["control", "cliche_control"]:
        continue
    if meta.get("language", "en") not in ["en", "english"]:
        continue

    for i, t in enumerate(tokens):
        if is_artifact(t):
            continue
        cleaned = clean_token(t["token"])
        if cleaned not in ALL_CONNECTIVES:
            continue
        window = get_windows(tokens, i, window_size=3)
        if not window:
            continue

        if cleaned not in word_stats:
            word_stats[cleaned] = {"n": 0, "s2_after": [], "entropy_at": [], "cat": ALL_CONNECTIVES[cleaned]}
        word_stats[cleaned]["n"] += 1
        word_stats[cleaned]["entropy_at"].append(t["entropy"])
        for _, tok in window[:1]:  # just +1
            word_stats[cleaned]["s2_after"].append(tok["s2"])

# Sort by frequency
sorted_words = sorted(word_stats.items(), key=lambda x: -x[1]["n"])[:20]

print(f"\n{'Connective':<12} {'Cat':<14} {'N':>5} {'H@conn':>8} {'S2@+1':>8} {'ΔS2':>8} {'+S2%':>7}")
print("-" * 65)
for word, stats in sorted_words:
    n = stats["n"]
    if n < 3:
        continue
    mean_h = statistics.mean(stats["entropy_at"]) if stats["entropy_at"] else 0
    mean_s2 = statistics.mean(stats["s2_after"]) if stats["s2_after"] else 0
    delta = mean_s2 - baseline_mean
    pos_r = sum(1 for x in stats["s2_after"] if x > 0) / len(stats["s2_after"]) if stats["s2_after"] else 0
    cat = stats["cat"]
    print(f"  {word:<12} {cat:<14} {n:>5} {mean_h:>8.2f} {mean_s2:>8.3f} {delta:>+8.3f} {pos_r:>7.1%}")

# --- Era comparison for conditionals vs. causals ---
print("\n" + "=" * 70)
print("ERA COMPARISON: CONDITIONAL vs. CAUSAL USE")
print("=" * 70)

era_conditional = defaultdict(list)  # era → [s2 at +1 after conditional]
era_causal = defaultdict(list)
era_s2_baseline = defaultdict(list)

for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]
    era = meta.get("era", "unknown")
    if meta.get("era") in ["control", "cliche_control"]:
        continue
    if meta.get("language", "en") not in ["en", "english"]:
        continue

    for i, t in enumerate(tokens):
        if is_artifact(t):
            continue
        era_s2_baseline[era].append(t["s2"])

        cleaned = clean_token(t["token"])
        if cleaned not in ALL_CONNECTIVES:
            continue
        cat = ALL_CONNECTIVES[cleaned]
        window = get_windows(tokens, i, window_size=1)
        if not window:
            continue

        for _, tok in window:
            if cat == "conditional":
                era_conditional[era].append(tok["s2"])
            elif cat == "causal":
                era_causal[era].append(tok["s2"])

# Eras with enough data
eras_with_data = {era for era in era_conditional if len(era_conditional[era]) >= 5}
eras_with_data |= {era for era in era_causal if len(era_causal[era]) >= 5}

print(f"\n{'Era':<25} {'Cond N':>7} {'Cond S2':>9} {'Caus N':>7} {'Caus S2':>9} {'Cond-Caus':>10}")
print("-" * 72)

sorted_eras = sorted(eras_with_data, key=lambda e: -len(era_conditional.get(e, [])))
for era in sorted_eras:
    cond_data = era_conditional.get(era, [])
    caus_data = era_causal.get(era, [])
    if len(cond_data) < 3 and len(caus_data) < 3:
        continue
    cond_mean = statistics.mean(cond_data) if len(cond_data) >= 3 else float('nan')
    caus_mean = statistics.mean(caus_data) if len(caus_data) >= 3 else float('nan')
    diff = cond_mean - caus_mean if not (cond_mean != cond_mean or caus_mean != caus_mean) else float('nan')
    print(f"  {era:<25} {len(cond_data):>7} {cond_mean:>+9.3f} {len(caus_data):>7} {caus_mean:>+9.3f} {diff:>+10.3f}")

# --- High-S2 examples after connectives ---
print("\n" + "=" * 70)
print("NOTABLE HIGH-S2 MOMENTS AFTER CONNECTIVES (S2 > 3.0)")
print("=" * 70)

for cat in ["conditional", "causal", "concessive", "temporal"]:
    examples = connective_examples.get(cat, [])
    examples_sorted = sorted(examples, key=lambda x: -x["next_s2"])[:3]
    if not examples_sorted:
        continue
    print(f"\n  [{cat.upper()}]")
    for ex in examples_sorted:
        print(f"    '{ex['author']}' ({ex['era']})")
        print(f"    Context: '...{ex['context'].strip()}' → [{ex['connective']}] → '{ex['next_token']}'")
        print(f"    S2 = {ex['next_s2']:.2f}, H at connective = {ex['connective_entropy']:.2f}")

# --- Hypothesis test ---
print("\n" + "=" * 70)
print("HYPOTHESIS RESULTS")
print("=" * 70)

cond_s2 = connective_data["conditional"].get("s2_+1", [])
caus_s2 = connective_data["causal"].get("s2_+1", [])
conc_s2 = connective_data["concessive"].get("s2_+1", [])
temp_s2 = connective_data["temporal"].get("s2_+1", [])
comp_s2 = connective_data["comparative"].get("s2_+1", [])

if cond_s2:
    print(f"\n  H1 (Conditionals → high entropy → low S2): ", end="")
    cond_h = statistics.mean(connective_data["conditional"].get("entropy_+1", [0]))
    if cond_h > baseline_h_mean and statistics.mean(cond_s2) < baseline_mean:
        print(f"CONFIRMED (entropy higher {cond_h:.1f}>{baseline_h_mean:.1f}, S2 lower {statistics.mean(cond_s2):.3f}<{baseline_mean:.3f})")
    elif cond_h > baseline_h_mean:
        print(f"PARTIALLY — entropy higher but S2 not lower ({statistics.mean(cond_s2):.3f} vs {baseline_mean:.3f})")
    else:
        print(f"NOT CONFIRMED (entropy {cond_h:.1f}, S2 {statistics.mean(cond_s2):.3f})")

if caus_s2:
    print(f"  H2 (Causals → closed chain → low S2): ", end="")
    if statistics.mean(caus_s2) < baseline_mean:
        print(f"CONFIRMED (mean S2 {statistics.mean(caus_s2):.3f} < baseline {baseline_mean:.3f})")
    else:
        print(f"NOT CONFIRMED (mean S2 {statistics.mean(caus_s2):.3f} vs baseline {baseline_mean:.3f})")

if conc_s2:
    print(f"  H3 (Concessives → contrast → high S2): ", end="")
    if statistics.mean(conc_s2) > baseline_mean:
        print(f"CONFIRMED (mean S2 {statistics.mean(conc_s2):.3f} > baseline {baseline_mean:.3f})")
    else:
        print(f"NOT CONFIRMED (mean S2 {statistics.mean(conc_s2):.3f} vs baseline {baseline_mean:.3f})")

print("\nDone.")
