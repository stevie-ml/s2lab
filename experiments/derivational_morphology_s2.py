"""
Derivational Morphology and S₂
--------------------------------
Research question: Do different word-forming (derivational) suffix classes
show systematically different S₂ profiles in poetry?

Hypothesis: Nominalized forms (-tion, -ness, -ity, -ment) signal abstract
register which GPT-2 finds more predictable in context, while verb-derived
forms (-ing nouns, -al adjectives) may be more surprising. Prefixation
(un-, re-, dis-, over-, mis-, pre-) might signal negation / reversal and
be more surprising.

Method:
  - Load existing corpus_results.json (no model re-run needed).
  - Classify each token by dominant suffix / prefix.
  - Filter stanza-break artifact positions (p_newline >= 0.9).
  - Compare mean S₂, mean entropy, and +S₂ rate per morphological class.
  - Also look at: by era, top tokens per class.
"""

import json
import re
import math
import sys
import os
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "findings", "derivational_morphology_s2.md")

# ── Morphological classifiers ─────────────────────────────────────────────────

NOUN_SUFFIXES = [
    ("tion", "nominalizer -tion"),   # consolation, mutation
    ("sion", "nominalizer -sion"),   # tension, passion
    ("ness", "quality -ness"),       # darkness, stillness
    ("ity",  "quality -ity"),        # infinity, purity
    ("ment", "result -ment"),        # movement, astonishment
    ("ance", "state -ance"),         # radiance, silence
    ("ence", "state -ence"),         # silence, presence
    ("hood", "collective -hood"),    # childhood, falsehood
    ("ship", "condition -ship"),     # friendship, worship
    ("dom",  "realm -dom"),          # freedom, boredom
    ("ism",  "doctrine -ism"),       # romanticism, symbolism
    ("ist",  "agent -ist"),          # symbolist, modernist
]

VERB_SUFFIXES = [
    ("ize",  "verbalizer -ize"),     # crystallize, memorize
    ("ise",  "verbalizer -ise"),
    ("ify",  "verbalizer -ify"),     # mortify, beautify
    ("ate",  "verbalizer -ate"),     # articulate, meditate
    ("en",   "verbalizer -en"),      # darken, brighten (short, tricky)
]

ADJ_SUFFIXES = [
    ("ful",  "adjective -ful"),      # beautiful, sorrowful
    ("less", "adjective -less"),     # boundless, speechless
    ("ous",  "adjective -ous"),      # glorious, luminous
    ("ive",  "adjective -ive"),      # pensive, elusive
    ("al",   "adjective -al"),       # eternal, natural
    ("ic",   "adjective -ic"),       # lyric, metallic
    ("ish",  "adjective -ish"),      # reddish, darkish
    ("like", "adjective -like"),     # dreamlike, marble-like
]

ADV_SUFFIXES = [
    ("ly",   "adverb -ly"),          # slowly, deeply
]

GERUND_PATTERN = re.compile(r'\b\w+ing\b', re.IGNORECASE)

PREFIXES = [
    ("un",  "negation un-"),         # undone, unearthly
    ("re",  "iteration re-"),        # return, remember
    ("dis", "reversal dis-"),        # dissolve, disclose
    ("over","excess over-"),         # overflow, overwhelm
    ("mis", "error mis-"),           # misspent, mistaken
    ("pre", "before pre-"),          # prepare, precede
    ("out", "surpass out-"),         # outrun, outlast
    ("in",  "into/negation in-"),    # innate, inward
    ("sub", "under sub-"),           # submerge, sublime
    ("trans","across trans-"),       # transform, transcend
]


def classify_token(tok: str):
    """Return (category_key, label) for the token, or ('base', 'base form') if unclassified."""
    t = tok.strip().lower().lstrip("Ġ").lstrip("▁")  # strip BPE/sentencepiece markers
    # remove punctuation
    t = re.sub(r"[^a-z]", "", t)
    if len(t) < 4:
        return ("base", "base form (short)")

    # Check suffixes (longest first within each group to avoid false short matches)
    for suffix, label in sorted(NOUN_SUFFIXES, key=lambda x: -len(x[0])):
        if t.endswith(suffix) and len(t) > len(suffix) + 1:
            return (f"noun_{suffix}", label)
    for suffix, label in sorted(ADV_SUFFIXES, key=lambda x: -len(x[0])):
        if t.endswith(suffix) and len(t) > len(suffix) + 2:
            return (f"adv_{suffix}", label)
    for suffix, label in sorted(ADJ_SUFFIXES, key=lambda x: -len(x[0])):
        if t.endswith(suffix) and len(t) > len(suffix) + 1:
            return (f"adj_{suffix}", label)
    for suffix, label in sorted(VERB_SUFFIXES, key=lambda x: -len(x[0])):
        if t.endswith(suffix) and len(t) > len(suffix) + 1:
            return (f"verb_{suffix}", label)
    # Check -ing separately (could be gerund noun or present participle)
    if t.endswith("ing") and len(t) > 5:
        return ("verb_ing", "gerund/participle -ing")

    # Check prefixes (only for longer words)
    if len(t) >= 6:
        for prefix, label in sorted(PREFIXES, key=lambda x: -len(x[0])):
            if t.startswith(prefix) and len(t) > len(prefix) + 2:
                return (f"prefix_{prefix}", label)

    return ("base", "base form")


def group_label(cat_key: str):
    """Coarser grouping for summary table."""
    if cat_key.startswith("noun_"):
        return "NOUN suffix"
    if cat_key.startswith("adv_"):
        return "ADV suffix"
    if cat_key.startswith("adj_"):
        return "ADJ suffix"
    if cat_key.startswith("verb_"):
        return "VERB suffix / gerund"
    if cat_key.startswith("prefix_"):
        return "prefix"
    return "base form"


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # collect per-class stats
    # class_stats[cat_key] = {label, s2_values, entropy_values, tokens_list}
    class_stats = defaultdict(lambda: {
        "label": "",
        "s2_values": [],
        "entropy_values": [],
        "surprisal_values": [],
        "examples": [],   # (token, s2, era, title)
        "group": ""
    })

    # Also by era
    era_class = defaultdict(lambda: defaultdict(list))  # era -> group -> [s2]

    total_tokens = 0
    artifact_filtered = 0

    for poem in data:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        title = meta.get("title", "?")
        tokens = poem.get("tokens", [])

        for tok in tokens:
            p_nl = tok.get("p_newline", 0.0)
            if p_nl >= 0.9:
                artifact_filtered += 1
                continue
            total_tokens += 1

            token_str = tok.get("token", "")
            s2 = tok.get("s2", 0.0)
            entropy = tok.get("entropy", 0.0)
            surprisal = tok.get("surprisal", 0.0)

            cat_key, label = classify_token(token_str)
            group = group_label(cat_key)

            cs = class_stats[cat_key]
            cs["label"] = label
            cs["group"] = group
            cs["s2_values"].append(s2)
            cs["entropy_values"].append(entropy)
            cs["surprisal_values"].append(surprisal)
            if s2 > 5.0 and len(cs["examples"]) < 5:
                cs["examples"].append((token_str.strip(), round(s2, 2), era, title))

            era_class[era][group].append(s2)

    # ── Aggregate results ─────────────────────────────────────────────────────

    def stats(vals):
        if not vals:
            return {"n": 0, "mean": 0, "pos_rate": 0, "max": 0, "std": 0}
        n = len(vals)
        mean = sum(vals) / n
        pos = sum(1 for v in vals if v > 0) / n
        mx = max(vals)
        std = math.sqrt(sum((v - mean) ** 2 for v in vals) / n)
        return {"n": n, "mean": round(mean, 3), "pos_rate": round(pos, 3), "max": round(mx, 2), "std": round(std, 3)}

    # Coarse group summary
    group_data = defaultdict(lambda: {"s2": [], "entropy": [], "surprisal": []})
    for cat_key, cs in class_stats.items():
        group_data[cs["group"]]["s2"].extend(cs["s2_values"])
        group_data[cs["group"]]["entropy"].extend(cs["entropy_values"])
        group_data[cs["group"]]["surprisal"].extend(cs["surprisal_values"])

    group_stats = {g: stats(gd["s2"]) for g, gd in group_data.items()}

    # Fine-grained suffix summary (only suffix classes with >50 tokens)
    suffix_rows = []
    for cat_key, cs in sorted(class_stats.items()):
        st = stats(cs["s2_values"])
        if st["n"] < 50:
            continue
        suffix_rows.append({
            "cat": cat_key,
            "label": cs["label"],
            "group": cs["group"],
            **st,
            "examples": cs["examples"]
        })
    suffix_rows.sort(key=lambda x: x["mean"], reverse=True)

    # ── Print report ──────────────────────────────────────────────────────────

    lines = []
    lines.append("# Derivational Morphology and S₂")
    lines.append("")
    lines.append(f"**Date:** 2026-11-14")
    lines.append(f"**Corpus:** {len(data)} poems | **Tokens analyzed:** {total_tokens:,} (artifact positions removed: {artifact_filtered:,})")
    lines.append("")
    lines.append("## Research Question")
    lines.append("")
    lines.append("Do words carrying derivational suffixes (e.g. *-ness*, *-tion*, *-ly*) or prefixes")
    lines.append("(e.g. *un-*, *re-*, *dis-*) show systematically different information-theoretic")
    lines.append("signatures in poetry? Do abstract nominalizations feel predictable or surprising?")
    lines.append("")
    lines.append("**Hypothesis A**: Nominal suffixes (-tion/-ness/-ity) signal abstract register and are")
    lines.append("*more predictable* (lower S₂) because abstract diction is contextually constrained.")
    lines.append("")
    lines.append("**Hypothesis B**: Negating/reversing prefixes (un-/dis-/mis-) are *more surprising*")
    lines.append("because they reverse the expected polarity.")
    lines.append("")
    lines.append("**Hypothesis C**: Adverbial -ly forms are the *most conformist* — they tend to modify")
    lines.append("predictable adjectives/verbs and rarely carry the semantic weight of a poem.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Results: Coarse Morphological Groups")
    lines.append("")
    lines.append("| Morphological Class | n tokens | Mean S₂ | +S₂ Rate | Max S₂ | Std |")
    lines.append("|---|---|---|---|---|---|")
    for group in ["NOUN suffix", "ADJ suffix", "VERB suffix / gerund", "ADV suffix", "prefix", "base form"]:
        st = group_stats.get(group, {"n": 0, "mean": 0, "pos_rate": 0, "max": 0, "std": 0})
        lines.append(f"| {group} | {st['n']:,} | **{st['mean']:.3f}** | {st['pos_rate']:.1%} | {st['max']:.1f} | {st['std']:.3f} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Results: Fine-Grained Suffix Analysis (n ≥ 50 tokens)")
    lines.append("")
    lines.append("| Suffix class | n | Mean S₂ | +S₂ Rate | Max S₂ | Group |")
    lines.append("|---|---|---|---|---|---|")
    for row in suffix_rows:
        lines.append(f"| `{row['label']}` | {row['n']:,} | **{row['mean']:.3f}** | {row['pos_rate']:.1%} | {row['max']:.1f} | {row['group']} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## High-S₂ Examples by Suffix Class")
    lines.append("")
    for row in suffix_rows[:15]:  # top 15 classes
        if row["examples"]:
            lines.append(f"### `{row['label']}`")
            for tok, s2, era, title in row["examples"]:
                lines.append(f"- **{tok}** (S₂={s2}) in *{title}* [{era}]")
            lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Era × Morphological Group")
    lines.append("")
    lines.append("Top 5 eras by NOUN suffix S₂ mean (how much do different eras use surprising abstract diction?):")
    lines.append("")

    era_noun_means = {}
    for era, groups in era_class.items():
        vals = groups.get("NOUN suffix", [])
        if len(vals) >= 20:
            era_noun_means[era] = sum(vals) / len(vals)
    top_noun_eras = sorted(era_noun_means.items(), key=lambda x: -x[1])[:10]
    lines.append("| Era | Mean S₂ (NOUN suffix) | n |")
    lines.append("|---|---|---|")
    for era, mean in top_noun_eras:
        n = len(era_class[era].get("NOUN suffix", []))
        lines.append(f"| {era} | {mean:.3f} | {n} |")
    lines.append("")

    lines.append("Top 5 eras by PREFIX S₂ mean (do some eras use more surprising prefixed forms?):")
    lines.append("")
    era_prefix_means = {}
    for era, groups in era_class.items():
        vals = groups.get("prefix", [])
        if len(vals) >= 10:
            era_prefix_means[era] = sum(vals) / len(vals)
    top_prefix_eras = sorted(era_prefix_means.items(), key=lambda x: -x[1])[:10]
    lines.append("| Era | Mean S₂ (prefix) | n |")
    lines.append("|---|---|---|")
    for era, mean in top_prefix_eras:
        n = len(era_class[era].get("prefix", []))
        lines.append(f"| {era} | {mean:.3f} | {n} |")
    lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("## Finding")
    lines.append("")

    # Determine actual finding
    noun_mean = group_stats.get("NOUN suffix", {}).get("mean", 0)
    adv_mean  = group_stats.get("ADV suffix", {}).get("mean", 0)
    verb_mean = group_stats.get("VERB suffix / gerund", {}).get("mean", 0)
    adj_mean  = group_stats.get("ADJ suffix", {}).get("mean", 0)
    prefix_mean = group_stats.get("prefix", {}).get("mean", 0)
    base_mean = group_stats.get("base form", {}).get("mean", 0)

    # rank groups
    ranked = sorted([
        ("NOUN suffix", noun_mean),
        ("ADV suffix", adv_mean),
        ("VERB suffix / gerund", verb_mean),
        ("ADJ suffix", adj_mean),
        ("prefix", prefix_mean),
        ("base form", base_mean),
    ], key=lambda x: -x[1])

    lines.append(f"**Ranking of morphological groups by mean S₂ (artifact-free):**")
    for rank, (group, mean) in enumerate(ranked, 1):
        lines.append(f"{rank}. **{group}**: {mean:.3f}")
    lines.append("")

    if noun_mean < base_mean:
        lines.append("**Hypothesis A SUPPORTED**: Nominal suffixes (-tion/-ness/-ity) are *more predictable*")
        lines.append(f"than base forms (mean S₂ {noun_mean:.3f} vs {base_mean:.3f}).")
        lines.append("Abstract nominalizations occupy contextually constrained slots — the model anticipates them.")
    else:
        lines.append("**Hypothesis A CHALLENGED**: Nominal suffixes are *not* more predictable than base forms.")
        lines.append(f"NOUN suffix mean S₂ ({noun_mean:.3f}) ≥ base ({base_mean:.3f}).")

    lines.append("")
    if prefix_mean > base_mean:
        lines.append("**Hypothesis B SUPPORTED**: Prefixed forms have higher S₂ than base forms")
        lines.append(f"({prefix_mean:.3f} vs {base_mean:.3f}), consistent with negation/reversal creating surprise.")
    else:
        lines.append("**Hypothesis B CHALLENGED**: Prefixed forms are not more surprising than base forms.")

    lines.append("")
    if adv_mean < base_mean:
        lines.append("**Hypothesis C SUPPORTED**: Adverbial -ly forms are more conformist than base forms")
        lines.append(f"(mean S₂ {adv_mean:.3f} vs {base_mean:.3f}).")
    else:
        lines.append("**Hypothesis C CHALLENGED**: Adverbial -ly forms are not more conformist than base forms.")

    lines.append("")
    lines.append("### Interpretation")
    lines.append("")
    lines.append("Derivational morphology encodes *register choices* that GPT-2 has learned.")
    lines.append("If nominal-suffix words are more predictable, it suggests that abstract")
    lines.append("diction forms a coherent register that the model tracks — the -ness/-tion")
    lines.append("vocabulary tends to cluster together and is contextually anticipated.")
    lines.append("Prefixed forms, by contrast, may carry more semantic surprise because")
    lines.append("the prefix negates or modifies an expected base, creating a gap between")
    lines.append("what was expected and what arrived.")
    lines.append("")
    lines.append("### Next Steps")
    lines.append("")
    lines.append("- Compare nominalization rates across eras: do Victorian/Romantic poets")
    lines.append("  nominalize more heavily, explaining their lower artifact-free S₂?")
    lines.append("- Specifically test whether Latinate (Romance) suffixes vs Germanic suffixes")
    lines.append("  differ (extends `latinate_germanic_diction_s2.md`).")
    lines.append("- Look at compound words with these suffixes in haiku and concrete poetry")
    lines.append("  vs. their much lower S₂ means — could derivational density explain their rank?")

    output = "\n".join(lines)
    with open(FINDINGS_PATH, "w") as f:
        f.write(output)

    print(output)
    print(f"\n[Saved to {FINDINGS_PATH}]")

    # Also save JSON data
    json_path = FINDINGS_PATH.replace(".md", ".json")
    with open(json_path, "w") as f:
        json.dump({
            "group_stats": {g: stats(gd["s2"]) for g, gd in group_data.items()},
            "suffix_rows": [{k: v for k, v in row.items() if k != "examples"} for row in suffix_rows],
            "top_noun_eras": top_noun_eras,
            "top_prefix_eras": top_prefix_eras,
        }, f, indent=2)
    print(f"[JSON saved to {json_path}]")


if __name__ == "__main__":
    main()
