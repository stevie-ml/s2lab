"""
Epistemic Hedges and Uncertainty Markers in Poetry: S2 Analysis

Research question: When poets use epistemic hedge words — "perhaps", "maybe",
"almost", "seem", "appear", "somehow" — do these signal proximity to high-S2
content? Is the poet acknowledging their own uncertainty, or using hedges
strategically to soften otherwise jarring surprises?

Extends modal_verbs_s2.md by moving from grammatical modality (might/could/would)
to lexical uncertainty markers (adverbs and appearance verbs that hedge claims
about truth/reality).

Categories:
  - pure_hedge_adverbs: perhaps, maybe, possibly, probably, presumably, apparently
  - degree_hedges: almost, nearly, hardly, barely, scarcely, quite, rather, somewhat
  - appearance_verbs: seem, seems, seemed, appear, appears, appeared, look, looks
  - evidential_adverbs: somehow, somewhere, somehow, whatever, whoever
  - contrastive_hedges: yet, still, though (already covered in logical_connectives)
  - simulative_phrases: as if, as though (token-level approximation)

Three-window analysis: S2 at positions -2, -1, HEDGE, +1, +2, +3
(Does surprise peak BEFORE the hedge, AT the hedge, or AFTER?)
"""

import json
import re
from collections import defaultdict
import statistics

with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# ── Hedge categories ──────────────────────────────────────────────────────────
HEDGE_CATEGORIES = {
    "pure_hedge_adverbs": [
        "perhaps", "maybe", "possibly", "probably", "presumably", "apparently",
        "perhaps,", "maybe,", "possibly,",
    ],
    "degree_hedges": [
        "almost", "nearly", "hardly", "barely", "scarcely", "quite", "rather",
        "somewhat", "partly", "largely", "mostly",
    ],
    "appearance_verbs": [
        "seem", "seems", "seemed", "seeming",
        "appear", "appears", "appeared", "appearing",
    ],
    "manner_hedges": [
        "somehow", "somewhere", "somehow,",
        "faintly", "vaguely", "dimly", "half",
    ],
    "as_if_marker": [
        "if",  # will filter to "as if" / "as though" by checking prior token == "as"
    ],
}

ALL_HEDGES = {}
for cat, words in HEDGE_CATEGORIES.items():
    for w in words:
        ALL_HEDGES[w.lower()] = cat

def clean_token(t):
    return t.strip().lower().lstrip("Ġ").lstrip(" ").strip(".,;:!?\"'()")

def raw_token(t):
    return t.strip().lstrip("Ġ").lstrip(" ")

def is_artifact(td):
    return td.get("p_newline", 0) >= 0.9

# ── Collect data ──────────────────────────────────────────────────────────────
# For each hedge instance, record S2 window: positions -2, -1, 0, +1, +2, +3
# Also record: entropy at hedge, top suppressed word, era, poet
hedge_windows = defaultdict(list)  # {category: [{window: [...], meta: {...}}]}
baseline_s2 = []
baseline_entropy = []

poet_hedge_rates = defaultdict(lambda: {"hedges": 0, "tokens": 0})

for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]

    if meta.get("era") in ["control", "cliche_control"]:
        continue
    if meta.get("language", "en") not in ["en", "english", None]:
        continue

    non_artifact_tokens = [t for t in tokens if not is_artifact(t)]
    for t in non_artifact_tokens:
        baseline_s2.append(t["s2"])
        baseline_entropy.append(t["entropy"])

    poet = meta.get("author", "Unknown")

    # Track non-artifact token list with original indices for window extraction
    clean_seq = []
    for i, t in enumerate(tokens):
        if not is_artifact(t):
            clean_seq.append((i, t))  # (original_index, token_data)

    for seq_pos, (orig_idx, t) in enumerate(clean_seq):
        poet_hedge_rates[poet]["tokens"] += 1

        ctext = clean_token(t["token"])
        if ctext not in ALL_HEDGES:
            continue

        cat = ALL_HEDGES[ctext]

        # Special case: "as if" / "as though" — require prev token to be "as"
        if cat == "as_if_marker":
            if seq_pos == 0:
                continue
            prev_clean = clean_token(clean_seq[seq_pos - 1][1]["token"])
            if prev_clean != "as":
                continue
            cat = "as_if_phrase"

        poet_hedge_rates[poet]["hedges"] += 1

        # Extract window: up to 3 tokens before, the hedge, 3 tokens after
        window = []
        for offset in range(-3, 4):
            idx = seq_pos + offset
            if 0 <= idx < len(clean_seq):
                tok = clean_seq[idx][1]
                window.append({
                    "offset": offset,
                    "token": raw_token(tok["token"]),
                    "s2": tok["s2"],
                    "entropy": tok["entropy"],
                    "surprisal": tok.get("surprisal", None),
                    "alternatives": tok.get("top_alternatives", []),
                })
            else:
                window.append({"offset": offset, "token": None, "s2": None, "entropy": None})

        hedge_windows[cat].append({
            "word": ctext,
            "window": window,
            "poem": meta.get("title", "?"),
            "author": meta.get("author", "?"),
            "era": meta.get("era", "?"),
            "year": meta.get("year", 0),
        })

# ── Analysis ──────────────────────────────────────────────────────────────────
base_mean_s2 = statistics.mean(baseline_s2)
base_mean_h = statistics.mean(baseline_entropy)
base_pct_pos = sum(1 for s in baseline_s2 if s > 0) / len(baseline_s2) * 100

print(f"Corpus baseline: N={len(baseline_s2):,} | mean S2={base_mean_s2:.3f} | mean H={base_mean_h:.3f} | +S2={base_pct_pos:.1f}%")
print()

# Per category summary across offset window
all_categories = list(hedge_windows.keys()) + ["as_if_phrase"]
all_categories = [c for c in all_categories if c in hedge_windows]

print("=== CATEGORY SUMMARY: S2 AT EACH POSITION ===")
print(f"{'Category':<25} {'N':>5} {'S2@-2':>7} {'S2@-1':>7} {'S2@0':>7} {'S2@+1':>7} {'S2@+2':>7} {'H@0':>7} {'+S2@0%':>8}")
print("-" * 90)

category_stats = {}
for cat in all_categories:
    instances = hedge_windows[cat]
    N = len(instances)
    if N < 3:
        continue

    by_offset = defaultdict(list)
    for inst in instances:
        for w in inst["window"]:
            if w["s2"] is not None:
                by_offset[w["offset"]].append(w["s2"])

    def mean_at(off):
        vals = by_offset.get(off, [])
        return statistics.mean(vals) if vals else float("nan")

    s2_vals_at_0 = by_offset.get(0, [])
    pct_pos_at_0 = sum(1 for s in s2_vals_at_0 if s > 0) / len(s2_vals_at_0) * 100 if s2_vals_at_0 else 0

    h_at_0 = [w["entropy"] for inst in instances for w in inst["window"] if w["offset"] == 0 and w["entropy"] is not None]
    mean_h_at_0 = statistics.mean(h_at_0) if h_at_0 else float("nan")

    stats = {
        "N": N,
        "s2_m2": mean_at(-2),
        "s2_m1": mean_at(-1),
        "s2_0": mean_at(0),
        "s2_p1": mean_at(1),
        "s2_p2": mean_at(2),
        "h_0": mean_h_at_0,
        "pct_pos_0": pct_pos_at_0,
        "instances": instances,
        "by_offset": by_offset,
    }
    category_stats[cat] = stats
    print(f"{cat:<25} {N:>5} {mean_at(-2):>7.3f} {mean_at(-1):>7.3f} {mean_at(0):>7.3f} {mean_at(1):>7.3f} {mean_at(2):>7.3f} {mean_h_at_0:>7.3f} {pct_pos_at_0:>8.1f}%")

print()
print(f"{'BASELINE':<25} {'':>5} {'':>7} {'':>7} {base_mean_s2:>7.3f} {'':>7} {'':>7} {base_mean_h:>7.3f} {base_pct_pos:>8.1f}%")
print()

# ── Individual word breakdown ──────────────────────────────────────────────────
print("=== INDIVIDUAL HEDGE WORDS ===")
word_data = defaultdict(list)
for cat, instances in hedge_windows.items():
    for inst in instances:
        word_data[(inst["word"], cat)].append(inst)

word_stats = []
for (word, cat), instances in word_data.items():
    N = len(instances)
    if N < 2:
        continue
    s2_at_0 = [w["s2"] for inst in instances for w in inst["window"] if w["offset"] == 0 and w["s2"] is not None]
    s2_at_p1 = [w["s2"] for inst in instances for w in inst["window"] if w["offset"] == 1 and w["s2"] is not None]
    h_at_0 = [w["entropy"] for inst in instances for w in inst["window"] if w["offset"] == 0 and w["entropy"] is not None]
    s2_at_m1 = [w["s2"] for inst in instances for w in inst["window"] if w["offset"] == -1 and w["s2"] is not None]

    def smean(lst): return statistics.mean(lst) if lst else float("nan")

    word_stats.append({
        "word": word,
        "cat": cat,
        "N": N,
        "s2_m1": smean(s2_at_m1),
        "s2_0": smean(s2_at_0),
        "s2_p1": smean(s2_at_p1),
        "delta": smean(s2_at_p1) - base_mean_s2,
        "h_0": smean(h_at_0),
        "pct_pos_0": sum(1 for s in s2_at_0 if s > 0) / len(s2_at_0) * 100 if s2_at_0 else 0,
    })

word_stats.sort(key=lambda x: x["s2_0"], reverse=True)
print(f"{'Word':<15} {'Cat':<22} {'N':>4} {'S2@-1':>7} {'S2@0':>7} {'S2@+1':>7} {'ΔS2@+1':>8} {'H@0':>7}")
print("-" * 85)
for w in word_stats:
    print(f"{w['word']:<15} {w['cat']:<22} {w['N']:>4} {w['s2_m1']:>7.3f} {w['s2_0']:>7.3f} {w['s2_p1']:>7.3f} {w['delta']:>8.3f} {w['h_0']:>7.3f}")

print()

# ── Most striking individual examples ─────────────────────────────────────────
print("=== TOP S2 INSTANCES AT HEDGE POSITION (S2@0 highest) ===")
all_instances = []
for cat, instances in hedge_windows.items():
    for inst in instances:
        for w in inst["window"]:
            if w["offset"] == 0 and w["s2"] is not None:
                all_instances.append({
                    "cat": cat,
                    "word": inst["word"],
                    "s2": w["s2"],
                    "entropy": w["entropy"],
                    "poem": inst["poem"],
                    "author": inst["author"],
                    "era": inst["era"],
                    "context": " ".join(
                        x["token"] for x in inst["window"] if x["token"] is not None
                    ),
                    "alts": w["alternatives"][:3] if w["alternatives"] else [],
                })

all_instances.sort(key=lambda x: x["s2"], reverse=True)
print(f"{'Author':<22} {'Word':<12} {'S2':>7} {'H':>7}  Context")
print("-" * 95)
for ex in all_instances[:25]:
    alts_str = "|".join(a[0].strip().lstrip("Ġ") for a in ex["alts"][:2]) if ex["alts"] else ""
    print(f"{ex['author']:<22} {ex['word']:<12} {ex['s2']:>7.2f} {ex['entropy']:>7.2f}  ...{ex['context']}... [{alts_str}]")

print()

# ── S2 before vs after hedge ──────────────────────────────────────────────────
print("=== DIRECTIONAL ANALYSIS: IS S2 HIGHER BEFORE OR AFTER THE HEDGE? ===")
for cat, stats in category_stats.items():
    N = stats["N"]
    before_s2 = statistics.mean(stats["by_offset"].get(-1, [0]))
    at_hedge = stats["s2_0"]
    after_s2 = statistics.mean(stats["by_offset"].get(1, [0]))
    delta = after_s2 - before_s2
    pattern = "AFTER > BEFORE" if after_s2 > before_s2 else "BEFORE > AFTER"
    print(f"  {cat:<25} N={N:>4} | before={before_s2:>6.3f} → hedge={at_hedge:>6.3f} → after={after_s2:>6.3f} | Δ={delta:>+6.3f} | {pattern}")

print()

# ── Top suppressed alternatives at hedge position ──────────────────────────────
print("=== WHAT THE MODEL PREDICTED INSTEAD OF THE HEDGE WORD ===")
for cat in all_categories:
    instances = hedge_windows[cat]
    if len(instances) < 3:
        continue
    alt_counts = defaultdict(int)
    for inst in instances:
        for w in inst["window"]:
            if w["offset"] == 0 and w["alternatives"]:
                for alt_tok, alt_prob in w["alternatives"][:5]:
                    alt_clean = alt_tok.strip().lstrip("Ġ").lstrip(" ").lower()
                    if alt_clean:
                        alt_counts[alt_clean] += 1
    top = sorted(alt_counts.items(), key=lambda x: -x[1])[:8]
    top_str = " | ".join(f"{w}({c})" for w, c in top)
    print(f"  {cat:<25}: {top_str}")

print()

# ── Poet-level hedge rate ──────────────────────────────────────────────────────
print("=== POET HEDGE USAGE RATES ===")
poet_rates = []
for poet, data in poet_hedge_rates.items():
    if data["tokens"] >= 100:
        rate = data["hedges"] / data["tokens"] * 1000  # per thousand tokens
        poet_rates.append((poet, rate, data["hedges"], data["tokens"]))

poet_rates.sort(key=lambda x: -x[1])
print(f"{'Poet':<28} {'Hedges/1k':>10} {'Hedges':>8} {'Tokens':>8}")
for poet, rate, hedges, tokens in poet_rates[:20]:
    print(f"  {poet:<26} {rate:>10.2f} {hedges:>8} {tokens:>8}")

print()

# ── Era-level breakdown ─────────────────────────────────────────────────────
print("=== ERA COMPARISON: HEDGE RATE AND S2 AT HEDGE ===")
era_data = defaultdict(lambda: {"hedges": 0, "total_s2": [], "total_tokens": 0})
for cat, instances in hedge_windows.items():
    for inst in instances:
        era = inst["era"]
        era_data[era]["hedges"] += 1
        for w in inst["window"]:
            if w["offset"] == 0 and w["s2"] is not None:
                era_data[era]["total_s2"].append(w["s2"])

# Token counts by era from baseline
era_token_counts = defaultdict(int)
for text in corpus:
    meta = text["metadata"]
    if meta.get("era") in ["control", "cliche_control"]:
        continue
    for t in text["tokens"]:
        if not is_artifact(t):
            era_token_counts[meta.get("era", "??")] += 1

for era in sorted(era_data):
    d = era_data[era]
    n = era_token_counts.get(era, 0)
    rate = d["hedges"] / n * 1000 if n > 0 else 0
    mean_s2 = statistics.mean(d["total_s2"]) if d["total_s2"] else float("nan")
    print(f"  {era:<25} hedges/1k={rate:.2f} | N={d['hedges']:>4} | S2@hedge={mean_s2:.3f}")

print()
print("DONE")
