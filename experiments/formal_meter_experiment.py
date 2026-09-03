"""
Formal Meter vs. S₂ Experiment
=================================
Tests whether metric/rhyme constraint shapes the S₂ distribution.

H1 (Constraint Compression): Metrically constrained poems have lower avg S₂
       because meter and rhyme pre-determine a large fraction of tokens.
H2 (Variance Reduction): Constrained poems have lower σ(S₂) — their surprises
       are more evenly spread rather than clustered in Straussian spikes.
H3 (End-Word Penalty): In rhymed poems, line-final tokens have significantly
       lower S₂ than in free-verse poems (extending the line-position finding).
H4 (Compensation): Despite lower avg S₂, constrained poems have comparable or
       higher MAX S₂ — poets "save up" surprise for key moments.
"""

import sys, os, json, re, statistics
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ─── Form classification ───────────────────────────────────────────────────
# Hand-coded: strict = regular meter + rhyme scheme
#             loose  = some metrical convention but not strict (e.g. Keats odes)
#             free   = no regular meter or rhyme
#             prose  = prose poem

FORM_MAP = {
    # STRICT METRICAL / RHYMED
    "The Raven (opening stanzas)":              "strict",
    "The Tyger":                                 "strict",
    "London":                                    "strict",
    "Remember":                                  "strict",   # Petrarchan sonnet
    "We Real Cool":                              "strict",
    "Ozymandias":                                "strict",   # loose sonnet form
    "I heard a Fly buzz — when I died":          "strict",   # hymn/common meter
    "The Oxen":                                  "strict",   # ballad quatrains
    "The Listeners":                             "strict",   # ballad-like
    "I Wandered Lonely as a Cloud":              "strict",
    "Harlem":                                    "strict",
    "We Wear the Mask":                          "strict",
    "Because I could not stop for Death":        "strict",
    "I felt a Funeral, in my Brain":             "strict",
    "A Route of Evanescence":                    "strict",
    "My Last Duchess (opening)":                 "strict",   # dramatic monologue, blank verse
    "Ulysses (opening)":                         "strict",   # blank verse (strict iambic pentameter)
    "Dover Beach":                               "strict",   # irregular but rhymed

    # LOOSELY METRICAL (ode-like, free rhyme, modernist form)
    "Ode to a Nightingale (stanza 1)":           "loose",
    "The Windhover":                             "loose",    # Hopkins sprung rhythm
    "The Convergence of the Twain (excerpt)":    "loose",
    "Anecdote of the Jar":                       "loose",
    "The Emperor of Ice-Cream":                  "loose",
    "Sunday Morning (stanza 1)":                 "loose",
    "Driving Toward the Lac Qui Parle River":    "loose",
    "The Love Song of J. Alfred Prufrock (opening)": "loose",
    "The Waste Land (opening)":                  "loose",
    "Fragment 31 (translated)":                  "loose",    # Sappho – sapphic meter in original
    "The Truth the Dead Know (opening)":         "loose",
    "Three Haiku (Basho, translated)":           "loose",
    "Daddy (opening)":                           "loose",
    "Lady Lazarus (opening)":                    "loose",
    "One Art":                                   "loose",    # villanelle (strict refrains but prose-y)
    "Incantation":                               "loose",
    "Variations on A (excerpt)":                 "loose",

    # FREE VERSE
    "Song of Myself (section 1)":                "free",
    "A Noiseless Patient Spider":                "free",
    "The Negro Speaks of Rivers":                "free",
    "Howl (opening)":                            "free",
    "A Supermarket in California":               "free",
    "Why I Am Not a Painter":                    "free",
    "The Day Lady Died":                         "free",
    "Self-Portrait in a Convex Mirror (opening)": "free",
    "Some Trees":                                "free",
    "What Is Poetry":                            "free",
    "Paradoxes and Oxymorons":                   "free",
    "And Ut Pictura Poesis Is Her Name":         "free",
    "Self-Portrait in a Convex Mirror (middle passage)": "free",
    "Self-Portrait in a Convex Mirror (closing)": "free",
    "The One Thing That Can Save America":       "free",
    "A Wave (opening)":                          "free",
    "Rivers and Mountains":                      "free",
    "Leaving the Atocha Station":                "free",
    "A Blessing in Disguise":                    "free",
    "Wet Casements":                             "free",
    "The Painter":                               "free",
    "Soonest Mended":                            "free",
    "The Instruction Manual":                    "free",
    "In a Station of the Metro":                 "free",
    "The Red Wheelbarrow":                       "free",
    "Oread":                                     "free",
    "Poetry (opening)":                          "free",
    "Buffalo Bill 's":                           "free",
    "Citizen (excerpt)":                         "free",
    "Night Sky with Exit Wounds (excerpt)":      "free",
    "Catalog of Unabashed Gratitude (excerpt)":  "free",
    "Whereas (excerpt)":                         "free",

    # PROSE POEM
    "The Stranger (prose poem, translated)":     "prose",
    "My Life (excerpt)":                         "prose",
    "Ketjak (excerpt)":                          "prose",
    "Islets/Irritations (excerpt)":              "prose",

    # EXPERIMENTAL / CONCRETE
    "Susie Asado":                               "experimental",
    "The Congo (opening, sanitized excerpt)":    "experimental",
    "Free Union (excerpt)":                      "experimental",
    "Howl (opening)":                            "free",

    # CONTROLS
    "Simple narrative prose":                    "control",
    "News article prose":                        "control",
    "Academic prose":                            "control",
    "Technical prose":                           "control",
}


def load_results(lang="en"):
    path = "results/corpus_results.json"
    with open(path) as f:
        data = json.load(f)
    return [p for p in data if p["metadata"].get("language", "en") == lang]


def get_line_final_tokens(poem_entry):
    """
    Return s2 values only for line-final tokens.
    Heuristic: a token is 'line-final' if the original text has a newline
    immediately after the characters that produced it — or it's the last
    token before a blank line.  We use a simplified approach:
    reconstruct positions from context_before length increments.
    """
    from corpus.poems import POEMS  # noqa: E402
    title = poem_entry["metadata"]["title"]
    author = poem_entry["metadata"]["author"]
    text = next(
        (p["text"] for p in POEMS if p["title"] == title and p["author"] == author),
        None
    )
    if text is None:
        return []

    # Get the set of character offsets where newlines occur
    newline_positions = {i for i, c in enumerate(text) if c == "\n"}

    tokens = poem_entry["tokens"]
    line_final_s2 = []
    for i, tok in enumerate(tokens):
        ctx_len = len(tok.get("context_before", ""))
        tok_str = tok["token"]
        # Estimate end-position of this token in the original text
        end_pos = ctx_len + len(tok_str)
        # Check if right after this token there's a newline (within a few chars)
        for offset in range(0, 4):
            if (end_pos + offset) in newline_positions:
                line_final_s2.append(tok["s2"])
                break
    return line_final_s2


def run():
    results = load_results("en")

    # Group by form
    by_form = defaultdict(list)
    unclassified = []
    for poem in results:
        title = poem["metadata"]["title"]
        form = FORM_MAP.get(title)
        if form:
            by_form[form].append(poem)
        else:
            unclassified.append(title)

    if unclassified:
        print(f"[WARN] Unclassified titles ({len(unclassified)}):")
        for t in sorted(unclassified):
            print(f"  - {t}")

    print("\n" + "="*70)
    print("FORMAL METER vs. S₂ — CORPUS-LEVEL STATISTICS")
    print("="*70)

    FORM_ORDER = ["strict", "loose", "free", "prose", "experimental", "control"]
    form_stats = {}

    for form in FORM_ORDER:
        poems = by_form.get(form, [])
        if not poems:
            continue
        all_s2 = [tok["s2"] for p in poems for tok in p["tokens"]]
        avg_s2  = statistics.mean(all_s2)
        std_s2  = statistics.stdev(all_s2) if len(all_s2) > 1 else 0
        pos_s2  = sum(1 for s in all_s2 if s > 0) / len(all_s2)
        max_s2  = max(all_s2)
        avg_max = statistics.mean(p["summary"]["max_s2"] for p in poems)
        n_poems = len(poems)
        n_tok   = len(all_s2)

        form_stats[form] = {
            "poems": n_poems, "tokens": n_tok,
            "avg_s2": avg_s2, "std_s2": std_s2,
            "pos_s2_ratio": pos_s2, "global_max": max_s2, "avg_max": avg_max,
        }

        print(f"\n{form.upper()} (n={n_poems} poems, {n_tok} tokens)")
        print(f"  avg S₂      = {avg_s2:+.3f}")
        print(f"  σ(S₂)       = {std_s2:.3f}")
        print(f"  +S₂ ratio   = {pos_s2:.1%}")
        print(f"  global max  = {max_s2:.2f}")
        print(f"  avg poem max= {avg_max:.2f}")

    # ── H1: Constraint Compression ─────────────────────────────────────────
    print("\n" + "="*70)
    print("H1 TEST — Constraint Compression (avg S₂)")
    print("="*70)
    for form in FORM_ORDER:
        if form in form_stats:
            print(f"  {form:<14} avg S₂ = {form_stats[form]['avg_s2']:+.3f}")

    # ── H2: Variance Reduction ─────────────────────────────────────────────
    print("\n" + "="*70)
    print("H2 TEST — Variance Reduction (σ of S₂)")
    print("="*70)
    for form in FORM_ORDER:
        if form in form_stats:
            print(f"  {form:<14} σ(S₂) = {form_stats[form]['std_s2']:.3f}")

    # ── H3: End-Word Penalty ───────────────────────────────────────────────
    print("\n" + "="*70)
    print("H3 TEST — End-Word S₂ Penalty by form")
    print("="*70)
    for form in FORM_ORDER:
        poems = by_form.get(form, [])
        final_s2_vals = []
        for p in poems:
            final_s2_vals.extend(get_line_final_tokens(p))
        if final_s2_vals:
            mean_final = statistics.mean(final_s2_vals)
            global_avg = form_stats.get(form, {}).get("avg_s2", 0)
            delta = mean_final - global_avg
            print(f"  {form:<14}  end-word avg S₂ = {mean_final:+.3f}  "
                  f"(Δ vs global avg = {delta:+.3f},  n={len(final_s2_vals)})")

    # ── H4: Compensation ───────────────────────────────────────────────────
    print("\n" + "="*70)
    print("H4 TEST — Compensation: avg poem-level MAX S₂")
    print("="*70)
    for form in FORM_ORDER:
        if form in form_stats:
            print(f"  {form:<14} avg max S₂ = {form_stats[form]['avg_max']:.2f}")

    # ── PER-POEM TABLE ─────────────────────────────────────────────────────
    print("\n" + "="*70)
    print("PER-POEM DETAIL (strict + free only)")
    print("="*70)
    print(f"{'Title':<50} {'Form':<12} {'Avg S₂':>8} {'σ(S₂)':>8} {'+S₂%':>7}")
    print("-"*90)
    for form in ["strict", "free"]:
        for p in sorted(by_form.get(form, []), key=lambda x: x["summary"]["avg_s2"]):
            title  = p["metadata"]["title"][:48]
            avg    = p["summary"]["avg_s2"]
            std    = p["summary"]["std_s2"]
            pos    = p["summary"]["pos_s2_ratio"]
            print(f"{title:<50} {form:<12} {avg:+8.3f} {std:8.3f} {pos:7.1%}")

    return form_stats


if __name__ == "__main__":
    run()
