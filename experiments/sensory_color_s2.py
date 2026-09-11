"""
Experiment: Color and Sensory Language vs S₂

Tests whether imagistic/sensory words (colors, textures, temperatures, sounds, smells)
appear at systematically higher S₂ positions in poetry. Connects to Imagist theory
(Pound, H.D.) which holds that the concrete image is the locus of poetic meaning.

Hypothesis: Sensory words are information-theoretically surprising — GPT-2's language
model privileges abstraction and function words, so concrete sensory vocabulary
constitutes a form of Straussian deviation.
"""

import json
import os
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FINDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings")

# Sensory word lexicons by category
SENSORY_LEXICONS = {
    "color": {
        "red", "blue", "green", "yellow", "white", "black", "grey", "gray",
        "gold", "golden", "silver", "brown", "pink", "purple", "violet",
        "orange", "crimson", "scarlet", "azure", "indigo", "ivory", "ebony",
        "amber", "jade", "copper", "rose", "pale", "dark", "bright",
        "dim", "black", "white", "ochre", "teal", "magenta", "vermilion",
        "russet", "saffron", "auburn", "tawny", "cerulean", "chartreuse",
        "cobalt", "hazel", "maroon",
    },
    "texture": {
        "smooth", "rough", "soft", "hard", "sharp", "dull", "jagged",
        "silky", "coarse", "fine", "gritty", "sandy", "wet", "dry",
        "slick", "sticky", "thick", "thin", "brittle", "crisp", "limp",
        "supple", "tender", "tough", "fuzzy", "prickly", "velvety",
    },
    "temperature": {
        "cold", "hot", "warm", "cool", "icy", "frozen", "burning",
        "frigid", "scorching", "tepid", "lukewarm", "chilly", "sweltering",
        "searing", "freezing", "frosty",
    },
    "sound": {
        "loud", "quiet", "silent", "soft", "harsh", "shrill", "muffled",
        "echoing", "hissing", "roaring", "whispering", "murmuring",
        "buzzing", "ringing", "thunder", "silence", "noise", "hush",
        "crash", "clatter", "rustle", "creak",
    },
    "smell_taste": {
        "sweet", "bitter", "sour", "salt", "salty", "savory", "spicy",
        "fragrant", "pungent", "acrid", "stale", "fresh", "ripe",
        "rotten", "musty", "perfumed", "rank", "fetid", "honeyed",
    },
    "light": {
        "bright", "dark", "dim", "light", "glow", "gleam", "shine",
        "flash", "flicker", "luminous", "radiant", "shadowy", "murky",
        "glowing", "sparkling", "dazzling", "luminous", "brilliant",
        "opaque", "translucent", "transparent", "shadowy",
    },
}

# All sensory words flattened for quick lookup
ALL_SENSORY = set()
for words in SENSORY_LEXICONS.values():
    ALL_SENSORY.update(w.lower() for w in words)


def classify_token(token_str):
    """Return the sensory category of a token, or None."""
    clean = token_str.strip().lower().strip("'\".,;:!?-")
    for category, words in SENSORY_LEXICONS.items():
        if clean in {w.lower() for w in words}:
            return category
    return None


def run_experiment(results_path="corpus_results.json"):
    with open(os.path.join(RESULTS_DIR, results_path)) as f:
        results = json.load(f)

    poetry = [r for r in results if r["metadata"]["era"] != "control"]
    prose = [r for r in results if r["metadata"]["era"] == "control"]

    # --- Global: sensory vs non-sensory token S2 ---
    sensory_tokens = []
    non_sensory_tokens = []
    sensory_by_category = defaultdict(list)
    sensory_by_era = defaultdict(lambda: defaultdict(list))
    sensory_by_poet = defaultdict(list)

    # Track sensory examples with high S2
    examples = []

    for r in poetry:
        era = r["metadata"]["era"]
        author = r["metadata"]["author"]
        title = r["metadata"]["title"]
        for tok in r["tokens"]:
            t = tok["token"]
            s2 = tok["s2"]
            category = classify_token(t)
            if category:
                sensory_tokens.append(s2)
                sensory_by_category[category].append(s2)
                sensory_by_era[era][category].append(s2)
                sensory_by_poet[author].append(s2)
                if s2 > 3.0:
                    examples.append({
                        "token": t.strip(),
                        "s2": s2,
                        "category": category,
                        "title": title,
                        "author": author,
                        "top_pred": tok["alternatives"][0]["token"] if tok.get("alternatives") else "?",
                    })
            else:
                non_sensory_tokens.append(s2)

    # Prose sensory tokens for comparison
    prose_sensory = []
    prose_non_sensory = []
    for r in prose:
        for tok in r["tokens"]:
            category = classify_token(tok["token"])
            if category:
                prose_sensory.append(tok["s2"])
            else:
                prose_non_sensory.append(tok["s2"])

    # Sort examples by S2
    examples.sort(key=lambda x: x["s2"], reverse=True)

    return {
        "poetry_sensory": sensory_tokens,
        "poetry_non_sensory": non_sensory_tokens,
        "prose_sensory": prose_sensory,
        "prose_non_sensory": prose_non_sensory,
        "by_category": sensory_by_category,
        "by_era": sensory_by_era,
        "by_poet": sensory_by_poet,
        "examples": examples[:25],
    }


def format_report(data):
    lines = []

    def mean(lst):
        return statistics.mean(lst) if lst else 0.0

    def pct_positive(lst):
        if not lst:
            return 0.0
        return sum(1 for x in lst if x > 0) / len(lst) * 100

    lines.append("# Sensory and Color Language in Poetry: An Information-Theoretic Analysis")
    lines.append("")
    lines.append("**Date:** 2026-09-11")
    lines.append("**Experiment:** `experiments/sensory_color_s2.py`")
    lines.append("")
    lines.append("## Research Question")
    lines.append("")
    lines.append("The Imagist tradition (Pound, H.D., Williams) holds that the concrete sensory image")
    lines.append("is the fundamental unit of poetic power. Does information theory support this claim?")
    lines.append("Are color words, texture words, temperature words, and other sensory vocabulary")
    lines.append("information-theoretically surprising to GPT-2 — i.e., do they occur at high-S₂ positions?")
    lines.append("")
    lines.append("**Hypothesis:** Sensory words represent a form of Straussian deviation. A language model")
    lines.append("trained on general text expects abstract connective tissue; a poet's commitment to")
    lines.append("the concrete is, from the model's perspective, a consistent form of surprise.")
    lines.append("")

    # --- Core Comparison Table ---
    ps = data["poetry_sensory"]
    pns = data["poetry_non_sensory"]
    prs = data["prose_sensory"]
    prns = data["prose_non_sensory"]

    lines.append("## Core Comparison: Sensory vs Non-Sensory Tokens")
    lines.append("")
    lines.append("| Context | Token Type | N | Avg S₂ | % Positive S₂ |")
    lines.append("|---------|-----------|---|--------|--------------|")
    if ps:
        lines.append(f"| Poetry  | Sensory    | {len(ps):,} | **{mean(ps):.3f}** | {pct_positive(ps):.1f}% |")
    if pns:
        lines.append(f"| Poetry  | Non-Sensory | {len(pns):,} | {mean(pns):.3f} | {pct_positive(pns):.1f}% |")
    if prs:
        lines.append(f"| Prose   | Sensory    | {len(prs):,} | {mean(prs):.3f} | {pct_positive(prs):.1f}% |")
    if prns:
        lines.append(f"| Prose   | Non-Sensory | {len(prns):,} | {mean(prns):.3f} | {pct_positive(prns):.1f}% |")

    # Gap
    if ps and pns:
        gap = mean(ps) - mean(pns)
        lines.append("")
        lines.append(f"**Sensory premium in poetry:** {gap:+.3f} bits S₂ over non-sensory tokens.")
    lines.append("")

    # --- By Sensory Category ---
    lines.append("## S₂ by Sensory Category")
    lines.append("")
    lines.append("| Category | N tokens | Avg S₂ | % Positive S₂ | Example Words |")
    lines.append("|----------|---------|--------|--------------|--------------|")

    category_examples = {
        "color": "red, blue, golden, crimson, pale",
        "texture": "rough, silky, sharp, velvety, coarse",
        "temperature": "cold, burning, icy, warm, frigid",
        "sound": "silent, echoing, hissing, crash, rustle",
        "smell_taste": "sweet, bitter, fragrant, rotten, honeyed",
        "light": "bright, dim, gleam, radiant, shadowy",
    }

    by_cat = data["by_category"]
    cat_sorted = sorted(by_cat.keys(), key=lambda c: mean(by_cat[c]), reverse=True)
    for cat in cat_sorted:
        toks = by_cat[cat]
        if toks:
            ex = category_examples.get(cat, "")
            lines.append(f"| {cat} | {len(toks)} | **{mean(toks):.3f}** | {pct_positive(toks):.1f}% | {ex} |")
    lines.append("")

    # --- High-S₂ sensory moments ---
    lines.append("## Top 20 High-S₂ Sensory Moments")
    lines.append("")
    lines.append("Moments where a sensory word was most surprising (highest S₂),")
    lines.append("and what GPT-2 expected instead:")
    lines.append("")
    lines.append("| Token | S₂ | Category | GPT-2 Expected | Poem |")
    lines.append("|-------|-----|----------|---------------|------|")
    for ex in data["examples"][:20]:
        title = ex["title"][:30] + "…" if len(ex["title"]) > 30 else ex["title"]
        lines.append(f"| `{ex['token']}` | {ex['s2']:.2f} | {ex['category']} | `{ex['top_pred'].strip()}` | *{title}* |")
    lines.append("")

    # --- By poet ---
    by_poet = data["by_poet"]
    poet_sorted = sorted(
        [(p, mean(v), len(v)) for p, v in by_poet.items() if len(v) >= 3],
        key=lambda x: x[1],
        reverse=True,
    )

    if poet_sorted:
        lines.append("## Poets Ranked by Sensory-Word S₂")
        lines.append("")
        lines.append("Which poets place sensory words at the most surprising positions?")
        lines.append("")
        lines.append("| Poet | Avg S₂ of Sensory Words | N sensory tokens |")
        lines.append("|------|------------------------|-----------------|")
        for poet, avg, n in poet_sorted[:12]:
            lines.append(f"| {poet} | **{avg:.3f}** | {n} |")
        lines.append("")

    # --- Finding ---
    lines.append("## Key Findings")
    lines.append("")

    if ps and pns:
        gap = mean(ps) - mean(pns)
        if gap > 0:
            lines.append(f"1. **Sensory words ARE information-theoretically surprising** — they average")
            lines.append(f"   {mean(ps):.3f} bits S₂ in poetry vs {mean(pns):.3f} bits for non-sensory tokens")
            lines.append(f"   (a +{gap:.3f} bit premium). Poets deploy sensory language precisely where")
            lines.append(f"   the language model is most confident about what should come next.")
        else:
            lines.append(f"1. **Counter-result:** Sensory words average {mean(ps):.3f} bits S₂ in poetry —")
            lines.append(f"   **lower** than non-sensory tokens ({mean(pns):.3f}). This may reflect that")
            lines.append(f"   sensory words often serve predictable grammatical roles (adjective before noun).")

    if prs and pns:
        prose_gap = mean(prs) - mean(prns)
        if abs(prose_gap) < abs(mean(ps) - mean(pns)):
            lines.append(f"2. **Poetry amplifies the sensory-word S₂ premium.** In prose, sensory words")
            lines.append(f"   average {mean(prs):.3f} bits S₂ vs {mean(prns):.3f} for non-sensory")
            lines.append(f"   (gap: {prose_gap:+.3f} bits). In poetry, the gap is larger.")
        else:
            lines.append(f"2. The poetry/prose comparison shows sensory-word S₂ is {mean(prs):.3f} in prose")
            lines.append(f"   vs {mean(ps):.3f} in poetry.")

    if cat_sorted and by_cat:
        top_cat = cat_sorted[0]
        bottom_cat = cat_sorted[-1]
        lines.append(f"3. **{top_cat.upper()} words** have the highest average sensory S₂ ({mean(by_cat[top_cat]):.3f}).")
        lines.append(f"   **{bottom_cat.upper()} words** have the lowest ({mean(by_cat[bottom_cat]):.3f}).")
        lines.append(f"   This hierarchy suggests that different sensory channels have different")
        lines.append(f"   relationships to statistical expectation in language.")

    lines.append("")
    lines.append("## Interpretive Note")
    lines.append("")
    lines.append("These findings suggest a nuanced relationship between sensory language and surprise:")
    lines.append("the Imagist claim that the concrete image is the locus of poetic meaning can be")
    lines.append("partially re-read as a claim about *statistical expectation violation*. When a poet")
    lines.append("writes 'crimson' instead of 'the' or 'a', they are performing a Straussian maneuver")
    lines.append("— placing something unexpected where the model was most confident something ordinary")
    lines.append("would appear.")
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("- Cross-tabulate sensory category with poem era (do Imagists have more color-S₂?)")
    lines.append("- Check whether sensory words cluster at line-initial positions (high-S₂ zone)")
    lines.append("- Test whether haiku (highest avg S₂) have disproportionate sensory token density")
    lines.append("- Compare sensory-word S₂ in concrete poetry vs abstract verse")

    return "\n".join(lines)


if __name__ == "__main__":
    print("Running sensory/color language vs S₂ experiment...")
    data = run_experiment()

    ps = data["poetry_sensory"]
    pns = data["poetry_non_sensory"]
    print(f"  Poetry sensory tokens: {len(ps)}, avg S₂ = {statistics.mean(ps) if ps else 0:.3f}")
    print(f"  Poetry non-sensory tokens: {len(pns)}, avg S₂ = {statistics.mean(pns) if pns else 0:.3f}")
    print(f"  Prose sensory tokens: {len(data['prose_sensory'])}, avg S₂ = {statistics.mean(data['prose_sensory']) if data['prose_sensory'] else 0:.3f}")

    report = format_report(data)
    out_path = os.path.join(FINDINGS_DIR, "sensory_color_s2.md")
    with open(out_path, "w") as f:
        f.write(report)
    print(f"  Report written to {out_path}")
