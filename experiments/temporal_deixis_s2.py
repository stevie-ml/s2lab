"""
Temporal Deixis and S2: Do Poets Use Time Words as Surprise Vehicles?

Temporal adverbs (now, then, always, never, once, still, etc.) are deictic
words that anchor a poem in time. This experiment asks:
1. Do temporal adverbs have higher or lower S2 in poetry vs prose?
2. Which temporal adverbs are most "Straussian" (deviate confident predictions)?
3. When a temporal adverb appears, what did GPT-2 expect instead?
4. Do different eras use temporal adverbs differently informationally?

Hypothesis: Temporal adverbs are "compressed surprise" in poetry — poets use
"always" or "never" in contexts where prose would use specific time references,
creating a kind of temporal sublime (infinite time vs concrete time).
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")
ARTIFACT_P = 0.90

# Temporal adverb categories
TEMPORAL_LEXICON = {
    "absolute_eternal": [
        " always", " never", " forever", " eternal", " eternally",
        " evermore", " everlasting", " perpetually", " immortal",
    ],
    "indefinite_past": [
        " once", " ago", " before", " formerly", " previously",
        " yesterday", " long", " ancient", " old",
    ],
    "indefinite_present": [
        " now", " still", " yet", " already", " today",
        " currently", " presently",
    ],
    "indefinite_future": [
        " soon", " then", " after", " later", " eventually",
        " someday", " tomorrow",
    ],
    "frequency": [
        " sometimes", " often", " rarely", " seldom", " occasionally",
        " always", " never", " again", " frequently",
    ],
    "sudden_change": [
        " suddenly", " suddenly", " once", " instantly", " abruptly",
        " finally", " at",
    ],
}

# Flat set of all temporal tokens (normalized to lowercase with leading space)
ALL_TEMPORAL = set()
TEMPORAL_CATEGORIES = {}
for cat, words in TEMPORAL_LEXICON.items():
    for w in words:
        ALL_TEMPORAL.add(w.lower())
        # First category wins if overlap
        if w.lower() not in TEMPORAL_CATEGORIES:
            TEMPORAL_CATEGORIES[w.lower()] = cat

# Core single-word temporals for detailed analysis
CORE_TEMPORALS = {
    " now", " then", " always", " never", " once", " still",
    " yet", " already", " soon", " before", " after", " again",
    " forever", " sometimes", " often", " rarely", " suddenly",
    " ago", " today", " tomorrow", " yesterday", " long",
}


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def clean_tokens(tokens):
    return [t for t in tokens if newline_prob(t) < ARTIFACT_P]


def get_top_alternative(tok):
    """Return the top-1 alternative token (excluding newline)."""
    for alt in sorted(tok["alternatives"], key=lambda x: -x["prob"]):
        if alt["token"].strip("\r\n") != "":
            return alt["token"]
    return ""


def analyze():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Data stores
    # By text type (poetry vs control)
    type_data = defaultdict(list)  # type -> list of (s2, surprisal, entropy) for temporal tokens
    type_all = defaultdict(list)   # type -> list of s2 for ALL tokens (baseline)

    # By specific temporal word
    word_data = defaultdict(list)  # word -> list of dicts

    # By era
    era_data = defaultdict(lambda: {"temporal_s2": [], "baseline_s2": []})

    # Temporal vs non-temporal within poetry
    poetry_temporal = []
    poetry_nontemporal = []

    # Suppressed alternatives for temporal tokens
    suppressed = defaultdict(list)  # actual_temporal_word -> list of top-1 alternatives

    # Type I analysis: "pure Straussian" temporal tokens
    # (high s2, low entropy = model was confident and wrong)
    pure_straussian = []

    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        lang = meta.get("language", "en")
        is_control = era == "control"
        is_poetry = not is_control

        tokens = clean_tokens(poem["tokens"])
        if not tokens:
            continue

        for tok in tokens:
            token_lower = tok["token"].lower()
            s2 = tok["s2"]
            surprisal = tok["surprisal"]
            entropy = tok["entropy"]
            is_temporal = token_lower in ALL_TEMPORAL

            # Baseline: all tokens by type
            label = "prose_control" if is_control else "poetry"
            type_all[label].append(s2)

            # Era baseline
            era_data[era]["baseline_s2"].append(s2)

            if is_temporal:
                type_data[label].append({
                    "s2": s2, "surprisal": surprisal, "entropy": entropy,
                    "token": token_lower, "rank": tok["rank"], "era": era,
                    "author": meta.get("author", "?"), "title": meta.get("title", "?"),
                })
                era_data[era]["temporal_s2"].append(s2)
                word_data[token_lower].append({
                    "s2": s2, "entropy": entropy, "era": era,
                    "top1_alt": get_top_alternative(tok),
                    "rank": tok["rank"],
                })
                suppressed[token_lower].append(get_top_alternative(tok))

                if is_poetry:
                    poetry_temporal.append(s2)

                    # Type I (pure Straussian): S2 >= 3 AND entropy < 5 (confident context)
                    if s2 >= 3.0 and entropy < 5.0:
                        pure_straussian.append({
                            "token": token_lower, "s2": s2, "entropy": entropy,
                            "top1_alt": get_top_alternative(tok),
                            "author": meta.get("author", "?"),
                            "title": meta.get("title", "?"),
                            "era": era,
                        })
            elif is_poetry:
                poetry_nontemporal.append(s2)

    return {
        "type_data": type_data,
        "type_all": type_all,
        "word_data": word_data,
        "era_data": era_data,
        "poetry_temporal": poetry_temporal,
        "poetry_nontemporal": poetry_nontemporal,
        "suppressed": suppressed,
        "pure_straussian": pure_straussian,
    }


def fmt(lst):
    if not lst:
        return "N/A"
    return f"{statistics.mean(lst):.3f}"


def run_experiment():
    results = analyze()
    type_data = results["type_data"]
    type_all = results["type_all"]
    word_data = results["word_data"]
    era_data = results["era_data"]
    poetry_temporal = results["poetry_temporal"]
    poetry_nontemporal = results["poetry_nontemporal"]
    suppressed = results["suppressed"]
    pure_straussian = results["pure_straussian"]

    output = []
    output.append("# Temporal Deixis and S₂: Time Words as Poetic Surprise Vehicles\n")
    output.append("**Date:** 2026-11-18\n")
    output.append("**Experiment:** `experiments/temporal_deixis_s2.py`\n")
    output.append(f"**Corpus:** {sum(1 for p in [type_data['poetry'], type_data['prose_control']] for _ in p)} temporal tokens across {len(word_data)} distinct temporal adverbs\n")
    output.append("\n---\n\n")

    output.append("## Research Question\n\n")
    output.append("Temporal adverbs — *now, then, always, never, once, still* — are among ")
    output.append("poetry's most charged words. They compress infinite time into single tokens. ")
    output.append("Do they carry a distinctive information-theoretic signature? ")
    output.append("When a poet writes \"always\" or \"never,\" was GPT-2 expecting something else?\n\n")

    # 1. Baseline comparison: temporal vs non-temporal in poetry
    n_temp = len(poetry_temporal)
    n_nontemp = len(poetry_nontemporal)
    avg_temp = fmt(poetry_temporal)
    avg_nontemp = fmt(poetry_nontemporal)

    output.append("## 1. Temporal Adverbs vs. Rest of Poetry\n\n")
    output.append(f"| Metric | Temporal adverbs (n={n_temp}) | Non-temporal tokens (n={n_nontemp}) |\n")
    output.append("|---|---|---|\n")
    output.append(f"| Avg S₂ | **{avg_temp}** | {avg_nontemp} |\n")
    if poetry_temporal and poetry_nontemporal:
        pos_temp = sum(1 for s in poetry_temporal if s > 0) / len(poetry_temporal)
        pos_nontemp = sum(1 for s in poetry_nontemporal if s > 0) / len(poetry_nontemporal)
        output.append(f"| % positive S₂ | **{pos_temp:.1%}** | {pos_nontemp:.1%} |\n")
        if len(poetry_temporal) > 1:
            std_temp = statistics.stdev(poetry_temporal)
        else:
            std_temp = 0
        if len(poetry_nontemporal) > 1:
            std_nontemp = statistics.stdev(poetry_nontemporal)
        else:
            std_nontemp = 0
        output.append(f"| Std S₂ | {std_temp:.3f} | {std_nontemp:.3f} |\n")
    output.append("\n")

    # 2. Poetry vs prose for temporal adverbs
    output.append("## 2. Temporal Adverbs in Poetry vs. Prose Control\n\n")
    if type_data["poetry"] and type_data["prose_control"]:
        p_s2 = [d["s2"] for d in type_data["poetry"]]
        c_s2 = [d["s2"] for d in type_data["prose_control"]]
        output.append(f"| | Poetry (n={len(p_s2)}) | Prose Control (n={len(c_s2)}) |\n")
        output.append("|---|---|---|\n")
        output.append(f"| Avg S₂ at temporal adverbs | **{fmt(p_s2)}** | {fmt(c_s2)} |\n")
        all_p = type_all["poetry"]
        all_c = type_all["prose_control"]
        output.append(f"| Avg S₂ overall | {fmt(all_p)} | {fmt(all_c)} |\n")
        if all_p and p_s2:
            lift_p = statistics.mean(p_s2) - statistics.mean(all_p)
            output.append(f"| Temporal lift above baseline | **{lift_p:+.3f}** | ")
        if all_c and c_s2:
            lift_c = statistics.mean(c_s2) - statistics.mean(all_c)
            output.append(f"{lift_c:+.3f} |\n")
        else:
            output.append("N/A |\n")
    output.append("\n")

    # 3. Per-word analysis
    output.append("## 3. Per-Word S₂ Rankings (Poetry, ≥5 occurrences)\n\n")
    output.append("| Temporal Word | n | Avg S₂ | % Positive | Avg Entropy | Top-1 Alt (most common) |\n")
    output.append("|---|---|---|---|---|---|\n")

    word_rows = []
    for word, data in word_data.items():
        poetry_data = [d for d in data if d["era"] != "control"]
        if len(poetry_data) < 5:
            continue
        s2s = [d["s2"] for d in poetry_data]
        entropies = [d["entropy"] for d in poetry_data]
        avg_s2 = statistics.mean(s2s)
        pos_pct = sum(1 for s in s2s if s > 0) / len(s2s)
        avg_ent = statistics.mean(entropies)

        # Most common top-1 alternative
        alts = suppressed.get(word, [])
        alt_counts = defaultdict(int)
        for a in alts:
            alt_counts[a] += 1
        top_alt = max(alt_counts, key=alt_counts.get) if alt_counts else "?"

        word_rows.append((word.strip(), len(poetry_data), avg_s2, pos_pct, avg_ent, top_alt, s2s))

    # Sort by avg S2 descending
    word_rows.sort(key=lambda x: -x[2])
    for word, n, avg_s2, pos_pct, avg_ent, top_alt, _ in word_rows[:30]:
        output.append(f"| `{word}` | {n} | **{avg_s2:.3f}** | {pos_pct:.1%} | {avg_ent:.2f} | `{top_alt}` |\n")
    output.append("\n")

    # 4. Temporal categories
    output.append("## 4. Temporal Category Analysis\n\n")
    cat_data = defaultdict(list)
    for poem_type in ["poetry"]:
        for d in type_data[poem_type]:
            cat = TEMPORAL_CATEGORIES.get(d["token"], "other")
            cat_data[cat].append(d["s2"])

    output.append("| Category | n | Avg S₂ |\n")
    output.append("|---|---|---|\n")
    for cat, s2s in sorted(cat_data.items(), key=lambda x: -statistics.mean(x[1]) if x[1] else 0):
        if s2s:
            output.append(f"| {cat} | {len(s2s)} | {fmt(s2s)} |\n")
    output.append("\n")

    # 5. Pure Straussian temporal tokens (high S2, low entropy)
    output.append("## 5. Pure Straussian Temporal Moments (S₂ ≥ 3.0, H < 5.0)\n\n")
    output.append(f"Found **{len(pure_straussian)}** moments where a temporal adverb shocked a confident model.\n\n")
    if pure_straussian:
        pure_straussian.sort(key=lambda x: -x["s2"])
        output.append("| Token | S₂ | Entropy | GPT-2 Expected | Author | Title | Era |\n")
        output.append("|---|---|---|---|---|---|---|\n")
        for ps in pure_straussian[:20]:
            output.append(f"| `{ps['token'].strip()}` | {ps['s2']:.2f} | {ps['entropy']:.2f} | `{ps['top1_alt'].strip()}` | {ps['author']} | {ps['title'][:30]} | {ps['era']} |\n")
    output.append("\n")

    # 6. Era comparison (eras with >= 10 temporal tokens)
    output.append("## 6. Era Comparison: Temporal S₂ vs. Baseline\n\n")
    output.append("| Era | Temporal n | Temporal Avg S₂ | Baseline Avg S₂ | Lift |\n")
    output.append("|---|---|---|---|---|\n")
    era_rows = []
    for era, d in era_data.items():
        if era == "control" or len(d["temporal_s2"]) < 5:
            continue
        t_avg = statistics.mean(d["temporal_s2"])
        b_avg = statistics.mean(d["baseline_s2"]) if d["baseline_s2"] else 0
        lift = t_avg - b_avg
        era_rows.append((era, len(d["temporal_s2"]), t_avg, b_avg, lift))
    era_rows.sort(key=lambda x: -x[4])  # sort by lift
    for era, n, t_avg, b_avg, lift in era_rows[:20]:
        output.append(f"| {era} | {n} | {t_avg:.3f} | {b_avg:.3f} | **{lift:+.3f}** |\n")
    output.append("\n")

    # 7. The "eternal" vs "contingent" time split
    output.append("## 7. Eternal vs. Contingent Temporality\n\n")
    output.append("Hypothesis: *Eternal* words (always, never, forever) carry different S₂ than\n")
    output.append("*contingent* words (now, then, once, soon) because they collapse the time axis\n")
    output.append("in a way GPT-2 doesn't expect.\n\n")

    eternal_words = {" always", " never", " forever", " eternal", " eternally", " evermore"}
    contingent_words = {" now", " then", " once", " soon", " before", " after", " again",
                        " yesterday", " today", " tomorrow", " already", " yet", " still"}

    eternal_s2 = []
    contingent_s2 = []

    for d in type_data["poetry"]:
        if d["token"] in eternal_words:
            eternal_s2.append(d["s2"])
        elif d["token"] in contingent_words:
            contingent_s2.append(d["s2"])

    output.append(f"| Type | n | Avg S₂ | % Positive |\n")
    output.append("|---|---|---|---|\n")
    if eternal_s2:
        pos_e = sum(1 for s in eternal_s2 if s > 0) / len(eternal_s2)
        output.append(f"| Eternal (always/never/forever...) | {len(eternal_s2)} | **{fmt(eternal_s2)}** | {pos_e:.1%} |\n")
    if contingent_s2:
        pos_c = sum(1 for s in contingent_s2 if s > 0) / len(contingent_s2)
        output.append(f"| Contingent (now/then/once/still...) | {len(contingent_s2)} | {fmt(contingent_s2)} | {pos_c:.1%} |\n")
    output.append("\n")

    # 8. Findings summary
    output.append("## Findings\n\n")

    # Determine key finding from data
    if poetry_temporal and poetry_nontemporal:
        delta = statistics.mean(poetry_temporal) - statistics.mean(poetry_nontemporal)
        direction = "HIGHER" if delta > 0 else "LOWER"
        output.append(f"1. **Temporal adverbs have {direction} S₂ than the average poetry token** ")
        output.append(f"(Δ = {delta:+.3f} bits). ")
        if delta > 0:
            output.append("Temporal words are charged moments of Straussian deviation — they signal the poet's departure from the statistically expected.\n\n")
        else:
            output.append("Temporal words tend to be grammatically predictable — they follow patterns the model anticipates.\n\n")

    if word_rows:
        top_word = word_rows[0][0]
        bottom_word = word_rows[-1][0]
        output.append(f"2. **Most surprising temporal word:** `{top_word}` (avg S₂ = {word_rows[0][2]:.3f}). ")
        output.append(f"**Least surprising:** `{bottom_word}` (avg S₂ = {word_rows[-1][2]:.3f}).\n\n")

    if eternal_s2 and contingent_s2:
        e_avg = statistics.mean(eternal_s2)
        c_avg = statistics.mean(contingent_s2)
        if abs(e_avg - c_avg) > 0.2:
            winner = "eternal" if e_avg > c_avg else "contingent"
            output.append(f"3. **{winner.capitalize()} temporality is more Straussian** ")
            output.append(f"(eternal avg = {e_avg:.3f}, contingent avg = {c_avg:.3f}). ")
            if e_avg > c_avg:
                output.append("Words like *always* and *never* catch GPT-2 off-guard more than specific time references — the absolute disrupts the conditional.\n\n")
            else:
                output.append("Specific time words (now, then, once) are more surprising than absolutes — the particular disrupts the general.\n\n")
        else:
            output.append("3. **Eternal and contingent temporality have similar S₂ profiles** — the absolute/contingent distinction does not predict surprise.\n\n")

    if pure_straussian:
        output.append(f"4. Found **{len(pure_straussian)}** 'pure Straussian' temporal moments (S₂ ≥ 3, H < 5) — ")
        output.append("where the model was highly confident but the poet wrote a time word anyway. ")
        # What was most common top-1 alternative at these positions?
        alt_counts = defaultdict(int)
        for ps in pure_straussian:
            alt_counts[ps["top1_alt"].strip()] += 1
        if alt_counts:
            top_suppressed = sorted(alt_counts.items(), key=lambda x: -x[1])[:3]
            top_str = ", ".join(f"`{a[0]}`×{a[1]}" for a in top_suppressed)
            output.append(f"Most common suppressed alternatives: {top_str}. ")
            output.append("These are the grammatically 'expected' words displaced by temporal ones.\n\n")

    output.append("## Suggested Next Steps\n\n")
    output.append("- **Temporal polarity**: Compare how poets use `never` vs `always` and their local S₂ context.\n")
    output.append("- **Tense-time consistency**: Do verbs immediately adjacent to temporal adverbs violate tense expectations?\n")
    output.append("- **Temporal clustering**: Are temporal adverbs clustered in certain parts of poems?\n")
    output.append("- **Cross-era vocabulary**: Which eras favor eternal vs contingent temporality?\n")

    return "".join(output)


if __name__ == "__main__":
    output = run_experiment()
    outpath = os.path.join(FINDINGS_DIR, "temporal_deixis_s2.md")
    with open(outpath, "w") as f:
        f.write(output)
    print(f"Saved to {outpath}")
    # Also save JSON
    results = analyze()
    # Save key numbers as JSON
    import json as json_mod
    summary = {
        "n_poetry_temporal": len(results["poetry_temporal"]),
        "n_poetry_nontemporal": len(results["poetry_nontemporal"]),
        "avg_s2_temporal_poetry": statistics.mean(results["poetry_temporal"]) if results["poetry_temporal"] else None,
        "avg_s2_nontemporal_poetry": statistics.mean(results["poetry_nontemporal"]) if results["poetry_nontemporal"] else None,
        "n_pure_straussian": len(results["pure_straussian"]),
    }
    with open(os.path.join(os.path.dirname(outpath), "temporal_deixis_s2.json"), "w") as f:
        json_mod.dump(summary, f, indent=2)
    print("Done.")
