"""
Experiment: Hypotaxis vs. Parataxis — does sentence structure affect S2?

Hypothesis:
  - Subordinating conjunctions (because, although, if, when, that, since, while,
    who, which, though, unless, until) reduce GPT-2's entropy (more constrained
    context), so tokens following them can have higher S2 if the poet deviates.
  - Coordinating conjunctions (and, but, or, nor, yet, so, for) leave entropy
    high, producing moderate S2 throughout.
  - A poem's overall "hypotaxis ratio" (subordinating / total conjunctions) may
    correlate with its avg S2 profile.

Method:
  1. Load corpus_results.json (already computed — no GPT-2 inference needed)
  2. For each token, check whether the immediately preceding content token is
     a subordinating or coordinating conjunction.
  3. Compute avg entropy & S2 by conjunction class.
  4. Also compute per-poem hypotaxis ratios and correlate with avg S2.
  5. Show the "most contested" moments: high-S2 tokens after a subordinator
     (places where the model was constrained but the poet still surprised it).
"""

import json
import os
import re
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "findings", "hypotaxis_parataxis_s2.md")

# Subordinating conjunctions (contextually constraining — force a specific syntactic slot)
SUBORDINATORS = {
    "because", "although", "though", "even", "if", "unless", "when", "whenever",
    "while", "since", "until", "after", "before", "as", "whether", "that", "who",
    "which", "whose", "where", "wherever", "once", "whereas", "in", "so"
}

# Coordinating conjunctions (additive/listing — keep prediction open)
COORDINATORS = {"and", "but", "or", "nor", "yet", "for", "both", "either", "neither"}

# Artifact mask: skip tokens where p_newline > 0.9 (stanza-break artifact)
P_NEWLINE_THRESHOLD = 0.9

def normalize(tok: str) -> str:
    return tok.strip().lower().strip(".,;:!?\"'-()")


def load_results():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def classify_prev_token(tokens: list[dict], i: int):
    """Return 'sub', 'coord', or None based on the token at position i."""
    if i < 0:
        return None
    tok_text = normalize(tokens[i]["token"])
    if tok_text in SUBORDINATORS:
        return "sub"
    if tok_text in COORDINATORS:
        return "coord"
    return None


def is_artifact(token: dict) -> bool:
    return token.get("p_newline", 0.0) > P_NEWLINE_THRESHOLD


def analyze():
    data = load_results()

    # Stats: {context_type: [s2, entropy, surprisal]}
    by_context: dict[str, list] = defaultdict(list)

    # Per-poem: hypotaxis ratio and avg clean S2
    poem_stats = []

    # High-S2 moments after subordinators
    contested = []  # (s2, poem_title, author, context_str, token, conjunction)

    for poem in data:
        meta = poem.get("metadata", {})
        tokens = poem.get("tokens", [])
        if not tokens:
            continue

        sub_count = 0
        coord_count = 0
        clean_s2_values = []

        for i, tok in enumerate(tokens):
            if is_artifact(tok):
                continue

            s2 = tok["s2"]
            ent = tok["entropy"]
            surp = tok["surprisal"]
            clean_s2_values.append(s2)

            ctx = classify_prev_token(tokens, i - 1)
            by_context[ctx or "other"].append({
                "s2": s2, "entropy": ent, "surprisal": surp
            })

            # Count conjunction use
            prev_tok = normalize(tokens[i - 1]["token"]) if i > 0 else ""
            if prev_tok in SUBORDINATORS:
                sub_count += 1
            elif prev_tok in COORDINATORS:
                coord_count += 1

            # Collect high-S2 after subordinators
            if ctx == "sub" and s2 > 3.0:
                conj = normalize(tokens[i - 1]["token"]) if i > 0 else "?"
                ctx_start = max(0, i - 4)
                ctx_str = "".join(t["token"] for t in tokens[ctx_start:i])
                contested.append({
                    "s2": round(s2, 2),
                    "entropy": round(ent, 2),
                    "token": tok["token"],
                    "context": ctx_str,
                    "conjunction": conj,
                    "title": meta.get("title", "?"),
                    "author": meta.get("author", "?"),
                    "era": meta.get("era", "?"),
                })

        total_conj = sub_count + coord_count
        hypo_ratio = sub_count / total_conj if total_conj > 0 else None
        avg_clean_s2 = sum(clean_s2_values) / len(clean_s2_values) if clean_s2_values else None

        if hypo_ratio is not None and avg_clean_s2 is not None and total_conj >= 5:
            poem_stats.append({
                "title": meta.get("title", "?"),
                "author": meta.get("author", "?"),
                "era": meta.get("era", "?"),
                "hypo_ratio": round(hypo_ratio, 3),
                "avg_s2": round(avg_clean_s2, 4),
                "sub_count": sub_count,
                "coord_count": coord_count,
            })

    return by_context, poem_stats, contested


def mean(lst):
    return sum(lst) / len(lst) if lst else 0.0


def write_findings(by_context, poem_stats, contested):
    # Compute summary stats per context type
    context_summary = {}
    for ctx, items in by_context.items():
        s2_vals = [x["s2"] for x in items]
        ent_vals = [x["entropy"] for x in items]
        context_summary[ctx] = {
            "n": len(s2_vals),
            "avg_s2": round(mean(s2_vals), 4),
            "avg_entropy": round(mean(ent_vals), 4),
            "pos_s2_pct": round(100 * sum(1 for v in s2_vals if v > 0) / len(s2_vals), 1) if s2_vals else 0,
        }

    # Sort poem_stats by hypotaxis ratio
    poem_stats_sorted = sorted(poem_stats, key=lambda x: x["hypo_ratio"], reverse=True)

    # Top 5 most hypotactic and paratactic poems
    top_hypo = poem_stats_sorted[:5]
    top_para = sorted(poem_stats, key=lambda x: x["hypo_ratio"])[:5]

    # Correlation: hypo_ratio vs avg_s2
    xs = [p["hypo_ratio"] for p in poem_stats]
    ys = [p["avg_s2"] for p in poem_stats]
    n = len(xs)
    mx, my = mean(xs), mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n if n else 0
    sx = (sum((x - mx) ** 2 for x in xs) / n) ** 0.5
    sy = (sum((y - my) ** 2 for y in ys) / n) ** 0.5
    r = cov / (sx * sy) if sx > 0 and sy > 0 else 0

    # Top contested moments
    top_contested = sorted(contested, key=lambda x: x["s2"], reverse=True)[:15]

    lines = [
        "# Hypotaxis vs. Parataxis: Does Clause Structure Shape S₂?",
        "",
        "**Date:** 2026-10-14",
        "**Question:** Do poems organized through subordination (hypotaxis) differ",
        "informationally from poems organized through coordination (parataxis)?",
        "",
        "---",
        "",
        "## Background",
        "",
        "**Hypotaxis** = embedding clauses inside one another (subordinating conjunctions:",
        "*because, although, if, when, that, since, while, who, which ...*)",
        "",
        "**Parataxis** = placing clauses side-by-side without subordination (coordinating",
        "conjunctions: *and, but, or, yet, for ...*)",
        "",
        "Hypothesis: Subordinating conjunctions **constrain** GPT-2's next-token distribution",
        "(lower entropy), meaning any deviation by the poet at that point is especially",
        "costly and produces high S₂. Coordinating conjunctions leave the distribution",
        "broader, so deviation is cheaper.",
        "",
        "---",
        "",
        "## Result 1: Entropy and S₂ by Conjunction Context",
        "",
        "Tokens are classified by the word immediately preceding them in the poem.",
        "Artifact positions (p_newline > 0.9) excluded.",
        "",
        "| Context | n | Avg Entropy (bits) | Avg S₂ | +S₂% |",
        "|---|---|---|---|---|",
    ]

    for ctx_label, ctx_key in [
        ("After subordinator (because, if, when...)", "sub"),
        ("After coordinator (and, but, or...)", "coord"),
        ("All other positions", "other"),
    ]:
        s = context_summary.get(ctx_key, {})
        lines.append(
            f"| {ctx_label} | {s.get('n',0):,} | {s.get('avg_entropy',0):.2f} | "
            f"**{s.get('avg_s2',0):.4f}** | {s.get('pos_s2_pct',0):.1f}% |"
        )

    lines += [
        "",
        "### Interpretation",
        "",
    ]

    sub_s = context_summary.get("sub", {})
    coord_s = context_summary.get("coord", {})
    other_s = context_summary.get("other", {})

    sub_ent = sub_s.get("avg_entropy", 0)
    coord_ent = coord_s.get("avg_entropy", 0)
    other_ent = other_s.get("avg_entropy", 0)

    if sub_ent < coord_ent:
        lines.append(
            f"**Subordinating conjunctions DO reduce entropy** ({sub_ent:.2f} bits) compared to "
            f"coordinating ({coord_ent:.2f} bits) and other contexts ({other_ent:.2f} bits). "
            f"The model is more constrained in what it expects after *if*, *because*, *when*."
        )
    else:
        lines.append(
            f"Subordinating conjunctions did not reduce entropy below coordinating ones "
            f"({sub_ent:.2f} vs {coord_ent:.2f} bits). "
            f"This may reflect GPT-2's training — prose subordination is common enough "
            f"to remain predictable."
        )

    sub_s2 = sub_s.get("avg_s2", 0)
    coord_s2 = coord_s.get("avg_s2", 0)
    if sub_s2 > coord_s2:
        lines.append(
            f"\nDespite (or because of) the constraint, **tokens after subordinators have higher avg S₂** "
            f"({sub_s2:.4f}) than after coordinators ({coord_s2:.4f}). "
            f"Poets use subordination to set up high-surprise payoffs."
        )
    else:
        lines.append(
            f"\nTokens after coordinators have avg S₂ = {coord_s2:.4f} vs "
            f"after subordinators = {sub_s2:.4f}. "
            f"Paratactic positions produce higher deviation on average."
        )

    lines += [
        "",
        "---",
        "",
        "## Result 2: Poem-Level Hypotaxis Ratio vs. Avg S₂",
        "",
        f"Pearson r (hypotaxis ratio vs avg S₂, artifact-free): **{r:.3f}** (n={n} poems)",
        "",
        "### Most hypotactic poems (highest subordinator ratio):",
        "",
        "| Poem | Author | Era | Hypo ratio | Avg S₂ |",
        "|---|---|---|---|---|",
    ]
    for p in top_hypo:
        lines.append(
            f"| {p['title']} | {p['author']} | {p['era']} | "
            f"{p['hypo_ratio']:.3f} | {p['avg_s2']:.4f} |"
        )

    lines += [
        "",
        "### Most paratactic poems (lowest subordinator ratio):",
        "",
        "| Poem | Author | Era | Hypo ratio | Avg S₂ |",
        "|---|---|---|---|---|",
    ]
    for p in top_para:
        lines.append(
            f"| {p['title']} | {p['author']} | {p['era']} | "
            f"{p['hypo_ratio']:.3f} | {p['avg_s2']:.4f} |"
        )

    if abs(r) > 0.15:
        direction = "positive" if r > 0 else "negative"
        lines += [
            "",
            f"A {direction} correlation (r={r:.3f}) suggests that {'more hypotactic' if r > 0 else 'more paratactic'} poems "
            f"tend to have {'higher' if r > 0 else 'lower'} avg S₂.",
        ]
    else:
        lines += [
            "",
            f"Correlation is weak (r={r:.3f}): overall hypotaxis ratio is not a strong predictor of avg S₂.",
            "Structure type alone does not determine information signature.",
        ]

    lines += [
        "",
        "---",
        "",
        "## Result 3: High-S₂ Moments After Subordinators",
        "",
        "These are the 'most contested' positions: the model was constrained by a",
        "subordinator but the poet still chose something unexpected.",
        "",
        "| S₂ | Token | After | Context | Poem |",
        "|---|---|---|---|---|",
    ]
    for m in top_contested[:12]:
        ctx_clean = m["context"].replace("\n", "↵").replace("|", "/")
        tok_clean = m["token"].strip().replace("|", "/")
        lines.append(
            f"| {m['s2']:.2f} | `{tok_clean}` | *{m['conjunction']}* | "
            f"…{ctx_clean}… | {m['author']}: {m['title'][:40]} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Summary Finding",
        "",
    ]

    # Write a conclusion based on actual results
    ent_diff = coord_ent - sub_ent
    s2_diff = sub_s2 - coord_s2

    if abs(ent_diff) > 0.2:
        ent_conclusion = (
            f"Subordinating conjunctions reduce GPT-2 entropy by {ent_diff:.2f} bits "
            f"compared to coordinators — the syntactic slot after a subordinator is more "
            f"constrained."
        )
    else:
        ent_conclusion = (
            f"Entropy after subordinators ({sub_ent:.2f} bits) and coordinators "
            f"({coord_ent:.2f} bits) is nearly the same — both types constrain context similarly."
        )

    if abs(s2_diff) > 0.05:
        s2_conclusion = (
            f"Despite this, {'subordinating' if s2_diff > 0 else 'coordinating'} conjunction "
            f"positions have higher avg S₂ (diff = {abs(s2_diff):.4f}). "
            f"{'Poets exploit subordinator-constrained slots for high-surprise payoffs.' if s2_diff > 0 else 'Paratactic/additive structures create more room for unexpected choices.'}"
        )
    else:
        s2_conclusion = (
            f"S₂ after subordinators ({sub_s2:.4f}) and coordinators ({coord_s2:.4f}) "
            f"are nearly the same, suggesting conjunction type does not systematically "
            f"shape the Straussian gap at the local level."
        )

    lines += [
        ent_conclusion,
        "",
        s2_conclusion,
        "",
        f"The poem-level correlation between hypotaxis ratio and avg S₂ is r={r:.3f} "
        f"({'moderate' if abs(r) > 0.2 else 'weak'}), suggesting that "
        f"{'sentence structure has a meaningful relationship with information profile.' if abs(r) > 0.2 else 'other factors (era, form, individual poet style) dominate over clause structure.'}",
        "",
        "---",
        "",
        "## Suggested Next Steps",
        "",
        "1. **Deeper context**: Look not just at the immediately preceding token but",
        "   at multi-token sequences (e.g., 'if the', 'because I', 'although it') —",
        "   multi-word subordinate frames may constrain more strongly than single conjunctions.",
        "2. **Era breakdown**: Do modernist/imagist poets (known for parataxis) vs.",
        "   Victorian poets (known for hypotaxis) show the expected pattern?",
        "3. **Rhetorical question S₂**: Questions with 'who', 'what', 'where' as subordinators",
        "   deserve a separate look — they may function informationally as open slots.",
        "4. **The 'if...then' construction**: Conditional structures are arguably the most",
        "   constraining syntactic frame. Profile the S₂ trajectory across a conditional clause.",
    ]

    with open(FINDINGS_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Findings written to: {FINDINGS_PATH}")
    return context_summary, r, len(poem_stats), top_contested[:5]


def main():
    print("Loading corpus results...")
    by_context, poem_stats, contested = analyze()

    print(f"  Poems with sufficient conjunctions: {len(poem_stats)}")
    for ctx_key, label in [("sub","subordinator"), ("coord","coordinator"), ("other","other")]:
        items = by_context[ctx_key]
        print(f"  Tokens after {label}: {len(items):,}")

    summary, r, n_poems, top5 = write_findings(by_context, poem_stats, contested)

    print(f"\nCorrelation (hypotaxis ratio vs avg S₂): r = {r:.3f} (n={n_poems} poems)")
    sub = summary.get("sub", {})
    coord = summary.get("coord", {})
    print(f"Avg S₂ after subordinators: {sub.get('avg_s2'):.4f}  entropy: {sub.get('avg_entropy'):.2f}")
    print(f"Avg S₂ after coordinators:  {coord.get('avg_s2'):.4f}  entropy: {coord.get('avg_entropy'):.2f}")

    print("\nTop contested moments (high S₂ after subordinator):")
    for m in top5:
        print(f"  S₂={m['s2']:.1f}  after '{m['conjunction']}'  token='{m['token'].strip()}'  "
              f"— {m['author']}: {m['title'][:40]}")


if __name__ == "__main__":
    main()
