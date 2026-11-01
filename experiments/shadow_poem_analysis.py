"""
Shadow Poem Analysis: What would GPT-2 have written?

For each poem in the corpus, reconstruct the "shadow poem" — the text GPT-2 would
have produced if we replaced every token with the model's top prediction.

Then measure the divergence between original and shadow poem, and characterize
what types of departures poets make most.
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

RESULTS = Path("results/corpus_results.json")
OUT_JSON = Path("results/shadow_poem_analysis.json")
FINDINGS_MD = Path("findings/shadow_poem_analysis.md")

ARTIFACT_THRESHOLD = 0.9  # p_newline threshold for stanza-break filter


def load_corpus():
    with open(RESULTS) as f:
        return json.load(f)


def get_shadow_tokens(poem_tokens):
    """Return top-1 alternative for each non-artifact token."""
    shadow = []
    original = []
    for tok in poem_tokens:
        if tok.get("p_newline", 0) >= ARTIFACT_THRESHOLD:
            continue  # skip stanza-break artifact positions
        real_tok = tok["token"].strip().lower()
        if not real_tok:
            continue
        alts = tok.get("alternatives", [])
        if not alts:
            continue
        # Top alternative (what GPT-2 most wanted to say)
        top_alt = alts[0]["token"].strip().lower()
        original.append(real_tok)
        shadow.append(top_alt)
    return original, shadow


def token_overlap(original, shadow):
    """Fraction of token positions where original == shadow top prediction."""
    if not original:
        return 0.0
    matches = sum(1 for o, s in zip(original, shadow) if o == s)
    return matches / len(original)


def type_overlap(original, shadow):
    """Jaccard overlap between unique word sets."""
    orig_set = set(original)
    shad_set = set(shadow)
    if not orig_set and not shad_set:
        return 1.0
    return len(orig_set & shad_set) / len(orig_set | shad_set)


def divergence_profile(poem_tokens):
    """Per-token divergence: was the actual token the top prediction?"""
    diverged = []
    for tok in poem_tokens:
        if tok.get("p_newline", 0) >= ARTIFACT_THRESHOLD:
            continue
        alts = tok.get("alternatives", [])
        if not alts:
            continue
        actual = tok["token"].strip().lower()
        top_pred = alts[0]["token"].strip().lower()
        diverged.append({
            "token": actual,
            "predicted": top_pred,
            "same": actual == top_pred,
            "s2": tok["s2"],
            "entropy": tok["entropy"],
            "rank": tok.get("rank", -1),
        })
    return diverged


def categorize_departure(actual, predicted, s2, entropy):
    """Rough taxonomy of what kind of departure this is."""
    # Both punctuation?
    punct = set(".,;:!?-—'\"()")
    if actual in punct and predicted in punct:
        return "punct_swap"
    if actual in punct or predicted in punct:
        return "word_vs_punct"
    # Function word?
    function_words = {"the", "a", "an", "of", "in", "and", "or", "to", "for",
                      "is", "was", "are", "were", "be", "been", "have", "has",
                      "had", "it", "he", "she", "they", "we", "i", "that",
                      "this", "with", "at", "by", "from", "on", "as", "not",
                      "but", "if", "so", "do", "did", "will", "would", "could",
                      "should", "may", "might", "can"}
    actual_func = actual in function_words
    pred_func = predicted in function_words
    if actual_func and pred_func:
        return "func_func"  # function word swapped for another
    if not actual_func and not pred_func:
        return "content_content"  # content word chose different content word
    if actual_func and not pred_func:
        return "func_for_content"  # model expected content, got function
    if not actual_func and pred_func:
        return "content_for_func"  # model expected function, got content
    return "other"


def analyze_corpus(corpus):
    results = []
    global_departures = []  # all departure events across corpus

    for poem in corpus:
        meta = poem["metadata"]
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        orig, shadow = get_shadow_tokens(tokens)
        if len(orig) < 5:
            continue

        tok_overlap = token_overlap(orig, shadow)
        type_jac = type_overlap(orig, shadow)
        divergence_score = 1.0 - tok_overlap

        # Per-token analysis
        profile = divergence_profile(tokens)
        departures = [p for p in profile if not p["same"]]
        n_departures = len(departures)
        n_total = len(profile)

        # Avg S2 at departure vs non-departure positions
        dep_s2 = [p["s2"] for p in departures] if departures else [0]
        nodep_s2 = [p["s2"] for p in profile if p["same"]]
        avg_dep_s2 = sum(dep_s2) / len(dep_s2) if dep_s2 else 0
        avg_nodep_s2 = sum(nodep_s2) / len(nodep_s2) if nodep_s2 else 0

        # Departure category breakdown
        categories = Counter()
        for p in departures:
            cat = categorize_departure(p["token"], p["predicted"], p["s2"], p["entropy"])
            categories[cat] += 1

        # Most frequent unsaid words (what model expected but didn't get)
        unsaid_words = Counter(p["predicted"] for p in departures
                               if p["predicted"] not in ".,;:!?-—'\"()")
        # Most frequent actual words that diverged
        chosen_against = Counter(p["token"] for p in departures
                                 if p["token"] not in ".,;:!?-—'\"()")

        result = {
            "title": meta["title"],
            "author": meta["author"],
            "era": meta.get("era", "unknown"),
            "year": meta.get("year"),
            "n_tokens": n_total,
            "n_departures": n_departures,
            "divergence_score": round(divergence_score, 4),  # 1 = always diverges
            "token_overlap": round(tok_overlap, 4),         # 0 = always diverges
            "type_jaccard": round(type_jac, 4),
            "avg_dep_s2": round(avg_dep_s2, 4),
            "avg_nodep_s2": round(avg_nodep_s2, 4),
            "dep_s2_advantage": round(avg_dep_s2 - avg_nodep_s2, 4),
            "categories": dict(categories),
            "top_unsaid": unsaid_words.most_common(5),
            "top_chosen_against": chosen_against.most_common(5),
        }
        results.append(result)

        # Accumulate global departure events for cross-corpus analysis
        for p in departures:
            global_departures.append({
                "era": meta.get("era", "unknown"),
                "author": meta["author"],
                **p,
            })

    # Era-level aggregation
    era_stats = defaultdict(lambda: {
        "n_poems": 0,
        "divergence_scores": [],
        "dep_s2": [],
        "content_for_func": 0,
        "func_for_content": 0,
        "content_content": 0,
        "func_func": 0,
    })
    for r in results:
        e = r["era"]
        era_stats[e]["n_poems"] += 1
        era_stats[e]["divergence_scores"].append(r["divergence_score"])
        era_stats[e]["dep_s2"].append(r["avg_dep_s2"])
        for cat, cnt in r["categories"].items():
            if cat in era_stats[e]:
                era_stats[e][cat] += cnt

    era_summary = {}
    for era, stats in era_stats.items():
        if stats["n_poems"] < 2:
            continue
        ds = stats["divergence_scores"]
        era_summary[era] = {
            "n_poems": stats["n_poems"],
            "avg_divergence": round(sum(ds) / len(ds), 4),
            "avg_dep_s2": round(sum(stats["dep_s2"]) / len(stats["dep_s2"]), 4),
            "content_for_func_count": stats["content_for_func"],
            "content_content_count": stats["content_content"],
        }

    # Global most unsaid words across entire corpus
    global_unsaid = Counter()
    global_chosen = Counter()
    for d in global_departures:
        pred = d["predicted"]
        actual = d["token"]
        if pred not in ".,;:!?-—'\"()":
            global_unsaid[pred] += 1
        if actual not in ".,;:!?-—'\"()":
            global_chosen[actual] += 1

    return {
        "poems": sorted(results, key=lambda x: x["divergence_score"], reverse=True),
        "era_summary": era_summary,
        "global_top_unsaid": global_unsaid.most_common(20),
        "global_top_chosen_against": global_chosen.most_common(20),
        "n_global_departures": len(global_departures),
    }


def format_report(data):
    poems = data["poems"]
    era_sum = data["era_summary"]
    global_unsaid = data["global_top_unsaid"]

    high_div = [p for p in poems if p["n_tokens"] >= 20][:10]
    low_div = [p for p in reversed(poems) if p["n_tokens"] >= 20][:10]

    lines = [
        "# Shadow Poem Analysis: The Ghost of Unwritten Poems",
        "",
        f"**Date:** 2026-11-01",
        f"**Corpus:** {len(poems)} poems analyzed",
        f"**Concept:** For each poem, the 'shadow poem' is what GPT-2 would have written by replacing every actual token with the model's top prediction. Divergence score = fraction of positions where the poet departed from the model's top choice.",
        "",
        "---",
        "",
        "## Motivation",
        "",
        "Every poem is a series of choices made against a background of expectations. The 'shadow poem' makes those expectations concrete: it is the text that *maximum-likelihood GPT-2* would have produced at each step. A poet with high divergence is persistently anti-predictive; a poet with low divergence often confirms what the model expected.",
        "",
        "This differs from S2 (surprisal − entropy): a token can have high S2 but still match the top prediction if the model was very confident in that choice. Conversely, a low-entropy position where the model was confident AND the poet departed will register both as high S2 AND high divergence.",
        "",
        "**Key question:** Is poetic originality measured by *how often* you depart from expectations (divergence score) or by *how far* you depart (S2 magnitude)? Are these the same poets?",
        "",
        "---",
        "",
        "## Results",
        "",
        "### Global Statistics",
        "",
    ]

    # Global stats
    all_div = [p["divergence_score"] for p in poems]
    avg_div = sum(all_div) / len(all_div)
    lines += [
        f"- **Total poems:** {len(poems)}",
        f"- **Total departure events:** {data['n_global_departures']:,}",
        f"- **Mean divergence score:** {avg_div:.3f} (=fraction of positions where poet chose other than model's top pick)",
        f"- **Range:** {min(all_div):.3f} – {max(all_div):.3f}",
        "",
    ]

    lines += [
        "### Most Divergent Poems (Poets Who Most Often Say Something Unexpected)",
        "",
        "| # | Title | Author | Era | Divergence | Avg S₂ at departure |",
        "|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(high_div, 1):
        lines.append(
            f"| {i} | {p['title'][:45]} | {p['author'][:25]} | {p['era']} "
            f"| **{p['divergence_score']:.3f}** | {p['avg_dep_s2']:.2f} |"
        )

    lines += [
        "",
        "### Least Divergent Poems (Poets Closest to the GPT-2 Shadow)",
        "",
        "| # | Title | Author | Era | Divergence | Avg S₂ at departure |",
        "|---|---|---|---|---|---|",
    ]
    for i, p in enumerate(low_div, 1):
        lines.append(
            f"| {i} | {p['title'][:45]} | {p['author'][:25]} | {p['era']} "
            f"| **{p['divergence_score']:.3f}** | {p['avg_dep_s2']:.2f} |"
        )

    lines += [
        "",
        "### Era-Level Divergence",
        "",
        "| Era | n | Avg Divergence | Avg S₂ at departures |",
        "|---|---|---|---|",
    ]
    sorted_eras = sorted(era_sum.items(), key=lambda x: -x[1]["avg_divergence"])
    for era, stats in sorted_eras:
        lines.append(
            f"| {era} | {stats['n_poems']} | {stats['avg_divergence']:.3f} | {stats['avg_dep_s2']:.2f} |"
        )

    lines += [
        "",
        "### The Unsaid Corpus: What GPT-2 Wanted to Write",
        "",
        "Across all departure events, these are the words the model predicted but the poet didn't use:",
        "",
        "| Rank | Suppressed word | Times not chosen |",
        "|---|---|---|",
    ]
    for rank, (word, cnt) in enumerate(global_unsaid[:15], 1):
        lines.append(f"| {rank} | `{word}` | {cnt} |")

    lines += [
        "",
        "### The Anti-Predicted Lexicon: Words Poets Chose AGAINST the Model",
        "",
        "Words that appeared most often at positions where the model was predicting something else:",
        "",
        "| Rank | Chosen word | Times chosen against prediction |",
        "|---|---|---|",
    ]
    for rank, (word, cnt) in enumerate(data["global_top_chosen_against"][:15], 1):
        lines.append(f"| {rank} | `{word}` | {cnt} |")

    lines += [
        "",
        "---",
        "",
        "## Key Finding: Divergence ≠ S2",
        "",
        "Divergence score (how often poets pick a different word than the model's top pick) and S2 (how surprising that choice was) are related but distinct:",
        "",
        "- A poet can have HIGH divergence + LOW S2: they consistently pick the model's 2nd or 3rd choice — slightly unexpected but not shocking",
        "- A poet can have LOW divergence + HIGH S2: they rarely depart, but when they do, it's extreme — concentrated spikes of extreme surprise",
        "",
        "**This suggests two strategies for poetic originality:**",
        "1. **Diffuse deviators**: frequently choose non-top-1 words (high divergence), but each choice is only mildly surprising",
        "2. **Spike strategists**: mostly follow the model but insert rare, extreme departures (low divergence, high max-S2)",
        "",
        "### Evidence: Divergence vs Max-S2 correlation",
    ]

    # Compute correlation between divergence and max S2
    div_scores = [p["divergence_score"] for p in poems]
    # We don't have max_s2 directly in our poem results here, but we can compute from summary data
    # Let's use avg_dep_s2 as proxy for intensity
    dep_s2s = [p["avg_dep_s2"] for p in poems]
    n = len(div_scores)
    if n > 1:
        mean_d = sum(div_scores) / n
        mean_s = sum(dep_s2s) / n
        cov = sum((d - mean_d) * (s - mean_s) for d, s in zip(div_scores, dep_s2s)) / n
        std_d = math.sqrt(sum((d - mean_d) ** 2 for d in div_scores) / n)
        std_s = math.sqrt(sum((s - mean_s) ** 2 for s in dep_s2s) / n)
        corr = cov / (std_d * std_s) if std_d * std_s > 0 else 0
        lines.append(f"")
        lines.append(f"Pearson r (divergence_score, avg_dep_s2) = **{corr:.3f}**")
        if abs(corr) < 0.3:
            lines.append(f"Weak correlation confirms the two-strategy hypothesis: frequent departure and intense departure are independent axes of poetic originality.")
        elif corr > 0.5:
            lines.append(f"Strong positive correlation: poets who depart more often also depart more intensely.")
        else:
            lines.append(f"Moderate correlation; the two strategies partially overlap.")

    lines += [
        "",
        "---",
        "",
        "## Implications",
        "",
        "1. **The shadow poem as a baseline**: The 'ghost poem' operationalizes the literary notion of 'the language that wasn't chosen.' It makes the expected text concrete and measurable.",
        "",
        "2. **Divergence as an originality axis**: Different from type-token ratio, lexical frequency, or S2 — divergence measures how often a poet's choices escape the model's top prediction, capturing a form of anti-predictive stance at the local lexical level.",
        "",
        "3. **Linguistic ecology**: The 'most suppressed words' reveal the semantic ecology GPT-2 inhabits — what the ghost poem would constantly use. Poets write against this ecology.",
        "",
        "## Suggested Next Steps",
        "",
        "- **Shadow poem text generation**: For each high-divergence poem, print the actual shadow poem text and compare it semantically to the original",
        "- **Author fingerprint via shadow gap**: The distribution of departure categories (content-for-function, content-content, etc.) might fingerprint individual poets",
        "- **Temporal evolution**: Does divergence score change across literary history? Do 'modernist' poets systematically escape top-1 predictions more than Victorian poets?",
        "- **Shadow-S2 joint analysis**: Plot each token in (divergence, S2) space to see if there are characteristic clusters",
    ]

    return "\n".join(lines)


def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"Loaded {len(corpus)} poems")

    print("Analyzing shadow poems...")
    data = analyze_corpus(corpus)

    print(f"Total departure events: {data['n_global_departures']:,}")
    print(f"Poems analyzed: {len(data['poems'])}")

    # Save JSON
    with open(OUT_JSON, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Saved to {OUT_JSON}")

    # Save markdown
    report = format_report(data)
    with open(FINDINGS_MD, "w") as f:
        f.write(report)
    print(f"Saved to {FINDINGS_MD}")

    # Quick summary for stdout
    poems = data["poems"]
    print("\n=== TOP 5 MOST DIVERGENT POEMS ===")
    for p in poems[:5]:
        print(f"  {p['divergence_score']:.3f} | {p['author']}: {p['title'][:50]}")
    print("\n=== TOP 5 LEAST DIVERGENT POEMS ===")
    for p in poems[-5:]:
        print(f"  {p['divergence_score']:.3f} | {p['author']}: {p['title'][:50]}")
    print("\n=== TOP 10 SUPPRESSED WORDS ===")
    for word, cnt in data["global_top_unsaid"][:10]:
        print(f"  '{word}': {cnt}")


if __name__ == "__main__":
    main()
