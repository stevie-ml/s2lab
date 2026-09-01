"""
Metaphor Detection via S2 Spikes
=================================
Hypothesis: Metaphors work by placing an unexpected (high-surprisal) word where the
model had confident (low-entropy) expectations — i.e., they produce high S2.

Method:
  1. Manually annotate metaphor 'vehicles' (the figurative term) in a set of poems.
  2. Extract S2 values for those specific tokens from corpus_results.json.
  3. Compare against non-metaphoric tokens in the same poems.
  4. Measure whether high-S2 moments capture known metaphors at a rate better than chance.

We annotate TWO types:
  - METAPHOR_VEHICLES: the figurative word itself (should be high-S2, model was surprised)
  - LITERAL_COUNTERPARTS: neighboring content words (baseline; model less surprised)
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")


# ── Annotated metaphor vehicles ────────────────────────────────────────────────
# Format: (poem_title_substring, token_substring, annotation)
# We search for the first occurrence of each token in the poem's token stream.
METAPHORS = [
    # Wordsworth: "I wandered lonely as a cloud" — the whole poem is the simile
    # Vehicle: cloud (mind/person likened to a cloud)
    ("Wandered Lonely", "cloud", "simile-vehicle: person/mood as cloud"),
    ("Wandered Lonely", "daffodils", "simile-vehicle: extended comparison"),

    # Dickinson: "I felt a Funeral, in my Brain" — Funeral is the metaphor for mental breakdown
    ("Funeral, in my Brain", "Funeral", "metaphor-vehicle: mental collapse as funeral"),
    ("Funeral, in my Brain", "Drum", "metaphor-vehicle: relentless thought as drum"),
    ("Funeral, in my Brain", "Service", "metaphor-vehicle: mental state as church service"),

    # Dickinson: "Because I could not stop for Death" — Death as a gentleman
    ("could not stop for Death", "kindly", "personification: Death described as kind"),
    ("could not stop for Death", "Carriage", "metaphor-vehicle: death journey as carriage ride"),
    ("could not stop for Death", "Civility", "personification: Death as civil gentleman"),

    # Hughes: "Harlem" — extended metaphor of deferred dream
    ("Harlem", "raisin", "simile-vehicle: deferred dream as raisin"),
    ("Harlem", "sore", "simile-vehicle: dream as festering sore"),
    ("Harlem", "meat", "simile-vehicle: dream as rotten meat"),
    ("Harlem", "syrupy", "simile-vehicle: dream as syrupy sweet"),
    ("Harlem", "explode", "metaphor: final rupture image"),

    # Williams: "The Red Wheelbarrow" — the poem IS a metaphor (depends on)
    # The word 'glazed' is figurative — it turns the wheelbarrow into a still life
    ("Red Wheelbarrow", "glazed", "metaphor: wet wheelbarrow as glazed ceramic"),
    ("Red Wheelbarrow", "white", "contrast-image: chickens as purity/plainness"),

    # Keats: "Ode to a Nightingale" — drowsiness as hemlock
    ("Ode to a Nightingale", "hemlock", "simile-vehicle: drowsiness as poison"),
    ("Ode to a Nightingale", "Dryad", "metaphor-vehicle: nightingale as forest sprite"),
    ("Ode to a Nightingale", "Lethe", "allusion-vehicle: forgetting as mythic river"),

    # Whitman: "Song of Myself" — self as cosmos
    ("Song of Myself", "atom", "metaphor-vehicle: self as atomic matter"),
    ("Song of Myself", "creeds", "metonym: organized religion/thought"),

    # Plath: "Lady Lazarus" — rebirth via Holocaust imagery
    ("Lady Lazarus", "Holocaust", "extended-metaphor: personal resurrection as mass death"),
    ("Lady Lazarus", "miracle", "irony: treating spectacle as miracle"),
    ("Lady Lazarus", "trash", "self-deprecation metaphor"),
    ("Lady Lazarus", "peanut", "bathos: sacred/profane juxtaposition"),

    # Plath: "Ariel" — horse as vehicle for dissolution of self
    ("Ariel", "Godiva", "allusion-vehicle: rider as Godiva"),
    ("Ariel", "arrow", "metaphor-vehicle: riding as arrow flight"),
    ("Ariel", "dew", "metaphor: dissolving as morning dew"),

    # Stevens: "The Emperor of Ice-Cream" — ice cream as life/death
    ("Emperor of Ice-Cream", "emperor", "metaphor-vehicle: pleasure as sovereign"),
    ("Emperor of Ice-Cream", "wenches", "register-contrast: ceremonial context"),

    # Hardy: "The Convergence of the Twain"
    ("Convergence of the Twain", "Immanent Will", "personification: fate as force"),
    ("Convergence of the Twain", "sinister", "metaphor: iceberg given moral quality"),
]


def find_token_s2(token_data, target_substring):
    """Find the first token containing target_substring and return its S2."""
    # Try exact match first (case-insensitive strip)
    for t in token_data:
        stripped = t["token"].strip().lower()
        if stripped == target_substring.lower():
            return t
    # Fallback: substring match
    for t in token_data:
        if target_substring.lower() in t["token"].lower():
            return t
    return None


def run():
    print("Loading corpus results...")
    with open(RESULTS_PATH) as f:
        results = json.load(f)

    print(f"Corpus: {len(results)} texts\n")

    # Index results by title
    by_title = {r["metadata"]["title"]: r for r in results}

    # ── Per-annotation analysis ──────────────────────────────────────────────
    rows = []
    found_poems = set()
    missing_poems = []

    for (title_sub, token_sub, annotation) in METAPHORS:
        # Find matching poem
        match = None
        for title, r in by_title.items():
            if title_sub.lower() in title.lower():
                match = r
                break
        if match is None:
            missing_poems.append(title_sub)
            continue
        found_poems.add(match["metadata"]["title"])

        token_hit = find_token_s2(match["tokens"], token_sub)
        if token_hit is None:
            rows.append({
                "poem": match["metadata"]["title"],
                "author": match["metadata"]["author"],
                "annotation": annotation,
                "target": token_sub,
                "token": None,
                "s2": None,
                "surprisal": None,
                "entropy": None,
                "rank": None,
            })
            continue

        rows.append({
            "poem": match["metadata"]["title"],
            "author": match["metadata"]["author"],
            "annotation": annotation,
            "target": token_sub,
            "token": token_hit["token"],
            "s2": token_hit["s2"],
            "surprisal": token_hit["surprisal"],
            "entropy": token_hit["entropy"],
            "rank": token_hit["rank"],
        })

    # ── Baseline: non-metaphor content words from same poems ─────────────────
    # For each poem that appears in our metaphor set, compute the median S2 of
    # all its content tokens (non-punctuation, non-newline, len > 2).
    baseline_by_poem = {}
    for r in results:
        title = r["metadata"]["title"]
        content_s2 = [
            t["s2"] for t in r["tokens"]
            if len(t["token"].strip()) > 2 and t["token"].strip().isalpha()
        ]
        if content_s2:
            baseline_by_poem[title] = sorted(content_s2)[len(content_s2) // 2]  # median

    # ── Results table ─────────────────────────────────────────────────────────
    print(f"{'Poem':<40} {'Target':<12} {'S₂':>7} {'Surp':>7} {'Ent':>7} {'Rank':>6}  Annotation")
    print("-" * 115)

    hit_s2 = []
    above_median = 0
    n_valid = 0

    for row in rows:
        if row["s2"] is None:
            tag = "(not found)"
        else:
            n_valid += 1
            hit_s2.append(row["s2"])
            poem_median = baseline_by_poem.get(row["poem"], 0)
            above = row["s2"] > poem_median
            if above:
                above_median += 1
            tag = "▲ above median" if above else "▼ below median"

        print(
            f"{row['poem'][:39]:<40} "
            f"{row['target'][:11]:<12} "
            f"{str(round(row['s2'], 2)) if row['s2'] is not None else 'N/A':>7} "
            f"{str(round(row['surprisal'], 2)) if row['surprisal'] is not None else 'N/A':>7} "
            f"{str(round(row['entropy'], 2)) if row['entropy'] is not None else 'N/A':>7} "
            f"{str(row['rank']) if row['rank'] is not None else 'N/A':>6}  {row['annotation'][:50]}"
        )

    print()

    # ── Summary stats ─────────────────────────────────────────────────────────
    if hit_s2:
        avg_metaphor_s2 = sum(hit_s2) / len(hit_s2)
        high_s2 = [v for v in hit_s2 if v > 0]
        pos_ratio = len(high_s2) / len(hit_s2)

        # Overall corpus baseline: avg S2 of all content words across all poems
        all_content_s2 = []
        for r in results:
            if r["metadata"]["era"] == "control":
                continue
            all_content_s2.extend(
                t["s2"] for t in r["tokens"]
                if len(t["token"].strip()) > 2 and t["token"].strip().isalpha()
            )
        corpus_avg = sum(all_content_s2) / len(all_content_s2) if all_content_s2 else 0

        print("=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"  Metaphor vehicles found:     {n_valid}/{len(rows)}")
        print(f"  Avg S₂ (metaphor vehicles):  {avg_metaphor_s2:.3f}")
        print(f"  Avg S₂ (all poetry content): {corpus_avg:.3f}")
        print(f"  Gap (metaphor - baseline):   {avg_metaphor_s2 - corpus_avg:+.3f}")
        print(f"  Metaphors with +S₂:          {pos_ratio:.0%}  ({len(high_s2)}/{n_valid})")
        print(f"  Above poem's median S₂:      {above_median}/{n_valid} ({above_median/n_valid:.0%})")
        print()

        # Top 10 metaphors by S2
        valid_rows = [r for r in rows if r["s2"] is not None]
        top10 = sorted(valid_rows, key=lambda r: r["s2"], reverse=True)[:10]
        print("Top 10 metaphor vehicles by S₂:")
        for i, r in enumerate(top10, 1):
            print(f"  {i:2}. S₂={r['s2']:>7.2f}  '{r['token'].strip():<12}' ({r['author']}) — {r['annotation'][:60]}")
        print()

        # Bottom 5
        bottom5 = sorted(valid_rows, key=lambda r: r["s2"])[:5]
        print("Lowest-S₂ metaphor vehicles (where model was confident AND right):")
        for r in bottom5:
            print(f"      S₂={r['s2']:>7.2f}  '{r['token'].strip():<12}' ({r['author']}) — {r['annotation'][:60]}")
        print()

        return {
            "n_valid": n_valid,
            "n_total": len(rows),
            "avg_metaphor_s2": avg_metaphor_s2,
            "corpus_content_avg_s2": corpus_avg,
            "gap": avg_metaphor_s2 - corpus_avg,
            "pos_ratio": pos_ratio,
            "above_median_ratio": above_median / n_valid,
            "rows": rows,
            "top10": top10,
        }
    return None


if __name__ == "__main__":
    run()
