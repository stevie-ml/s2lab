"""
Stanza-Break α Inheritance: Does GPT-2's Prediction Concentration Reset or Persist?

Background:
- alpha_arc_within_poem.py: α (Zipf exponent of top-10 prediction distribution) rises over
  a poem's arc — the model's predictions become more concentrated as it internalizes the poem.
- stanza_internal_arc.py: This arc replicates fractally within each stanza (mini-arc per stanza).

New Question:
At a stanza break, does α DROP (suggesting the model resets its familiarity with the poem's
idiom) or INHERIT (persist at pre-break levels)? This directly tests whether stanza breaks
are genuine information-theoretic discontinuities.

Hypothesis A (Reset): Each stanza is a fresh context; α drops at breaks back toward
  the opening level of the previous stanza. Poetry's stanza structure creates genuine
  episodic interruptions in expectation-formation.

Hypothesis B (Inheritance): The model's accumulated familiarity with the poem's idiom
  carries across stanza breaks. α at the start of stanza N+1 stays near the level of
  the end of stanza N. The model "remembers" the poem's grammar across the gap.

Hypothesis C (Partial Inheritance): There is some drop, but less than a full reset.
  Stanza breaks are interruptions but not complete discontinuities.

We define:
  - pre_break_α: mean α in the last 5 clean tokens of stanza N
  - post_break_α: mean α in the first 5 clean tokens of stanza N+1
  - inheritance_ratio = post_break_α / pre_break_α
  - within_stanza_ratio: same ratio at non-boundary positions (baseline)

Special case: pantoums
  Lines 2 and 4 of stanza N become lines 1 and 3 of stanza N+1 (repetition).
  If the model recognizes repeated lines, pantoums should show HIGHEST inheritance.

Special case: ghazals
  Each couplet is semantically independent (radif word at end creates syntactic but
  not semantic continuity). Ghazals should show LOWEST inheritance (most reset-like).
"""

import json
import math
import statistics
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/stanza_break_alpha_inheritance.json"

WINDOW = 5          # tokens on each side of a stanza break to compare
MIN_STANZA_TOKENS = 5   # minimum clean tokens per stanza to include it
MIN_STANZAS = 2     # poem must have at least 2 stanzas


def fit_zipf_exponent(probs):
    """Fit Zipf exponent α via log-log regression on rank vs. probability."""
    if len(probs) < 2:
        return None
    total = sum(probs)
    if total == 0:
        return None
    normed = [p / total for p in probs if p > 0]
    if len(normed) < 2:
        return None
    n = len(normed)
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_probs = [math.log(p) for p in normed]
    mean_lr = sum(log_ranks) / n
    mean_lp = sum(log_probs) / n
    numer = sum((log_ranks[i] - mean_lr) * (log_probs[i] - mean_lp) for i in range(n))
    denom = sum((log_ranks[i] - mean_lr) ** 2 for i in range(n))
    if denom == 0:
        return None
    return -numer / denom


def segment_into_stanzas(tokens):
    """
    Split token list into stanzas using high-p_newline tokens as stanza boundaries.
    Returns list of stanzas, each a list of clean (non-artifact) tokens.
    """
    stanzas = []
    current = []
    for tok in tokens:
        p_nl = tok.get("p_newline", 0)
        if p_nl > 0.9:
            # artifact token (line boundary marker)
            if p_nl > 0.95:
                # strong stanza break signal
                if current:
                    stanzas.append(current)
                    current = []
        else:
            current.append(tok)
    if current:
        stanzas.append(current)
    # Remove empty stanzas
    return [s for s in stanzas if len(s) >= MIN_STANZA_TOKENS]


def get_window_alpha(tokens, start, size):
    """Return mean α for `size` tokens starting at `start`, or None if insufficient."""
    alphas = []
    for tok in tokens[start:start + size]:
        alts = tok.get("alternatives", [])
        probs = [a["prob"] for a in alts]
        a = fit_zipf_exponent(probs)
        if a is not None:
            alphas.append(a)
    if len(alphas) < 2:
        return None
    return statistics.mean(alphas)


def within_stanza_ratio(stanza):
    """
    Compute mean α ratio between consecutive non-boundary windows within a stanza.
    This gives the baseline: how much does α change across same-sized windows in
    the middle of a stanza (no stanza break).
    """
    n = len(stanza)
    if n < 2 * WINDOW + 2:
        return None
    ratios = []
    # Sample 3 positions within the stanza
    mid = n // 2
    for start in [WINDOW, mid - WINDOW // 2]:
        a1 = get_window_alpha(stanza, start, WINDOW)
        a2 = get_window_alpha(stanza, start + WINDOW, WINDOW)
        if a1 and a2 and a1 > 0:
            ratios.append(a2 / a1)
    return statistics.mean(ratios) if ratios else None


def process_poem(poem):
    tokens = poem.get("tokens", [])
    meta = poem.get("metadata", {})

    stanzas = segment_into_stanzas(tokens)
    if len(stanzas) < MIN_STANZAS:
        return None

    break_events = []
    within_ratios = []

    for i in range(len(stanzas) - 1):
        stanza_a = stanzas[i]
        stanza_b = stanzas[i + 1]

        if len(stanza_a) < WINDOW or len(stanza_b) < WINDOW:
            continue

        # Pre-break window: last WINDOW tokens of stanza N
        pre_alpha = get_window_alpha(stanza_a, len(stanza_a) - WINDOW, WINDOW)
        # Post-break window: first WINDOW tokens of stanza N+1
        post_alpha = get_window_alpha(stanza_b, 0, WINDOW)

        if pre_alpha is None or post_alpha is None or pre_alpha == 0:
            continue

        inheritance_ratio = post_alpha / pre_alpha

        # Also record per-stanza start α (to track the "baseline" for each stanza)
        stanza_b_start = get_window_alpha(stanza_b, 0, WINDOW)
        stanza_b_end = get_window_alpha(stanza_b, len(stanza_b) - WINDOW, WINDOW)

        break_events.append({
            "break_number": i + 1,  # 1 = break between stanzas 1 and 2
            "pre_alpha": round(pre_alpha, 4),
            "post_alpha": round(post_alpha, 4),
            "inheritance_ratio": round(inheritance_ratio, 4),
            "stanza_b_tokens": len(stanza_b),
            "stanza_a_tokens": len(stanza_a),
        })

        # Within-stanza baseline from stanza B
        ws_ratio = within_stanza_ratio(stanza_b)
        if ws_ratio is not None:
            within_ratios.append(ws_ratio)

    if not break_events:
        return None

    # Poem-level first-stanza start α (the absolute baseline)
    first_stanza_alpha = get_window_alpha(stanzas[0], 0, WINDOW)
    # Last-stanza pre-final α
    last_stanza_alpha = get_window_alpha(stanzas[-1], 0, WINDOW)

    mean_inheritance = statistics.mean(e["inheritance_ratio"] for e in break_events)
    mean_within = statistics.mean(within_ratios) if within_ratios else None

    return {
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "era": meta.get("era", "unknown"),
        "year": meta.get("year"),
        "n_stanzas": len(stanzas),
        "n_breaks": len(break_events),
        "break_events": break_events,
        "mean_inheritance_ratio": round(mean_inheritance, 4),
        "mean_within_stanza_ratio": round(mean_within, 4) if mean_within else None,
        "first_stanza_alpha": round(first_stanza_alpha, 4) if first_stanza_alpha else None,
        "last_stanza_alpha": round(last_stanza_alpha, 4) if last_stanza_alpha else None,
    }


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    poems = [p for p in corpus if p.get("metadata", {}).get("era") != "prose_control"]

    results = []
    for poem in poems:
        r = process_poem(poem)
        if r is not None:
            results.append(r)

    print(f"Analyzed {len(results)} poems with stanzas out of {len(poems)} total")

    # Global statistics
    all_inheritance = [r["mean_inheritance_ratio"] for r in results]
    all_within = [r["mean_within_stanza_ratio"] for r in results
                  if r["mean_within_stanza_ratio"] is not None]

    global_mean_inheritance = statistics.mean(all_inheritance)
    global_mean_within = statistics.mean(all_within) if all_within else None
    global_median_inheritance = statistics.median(all_inheritance)

    # Count reset vs inherit
    reset_count = sum(1 for x in all_inheritance if x < 0.95)
    neutral_count = sum(1 for x in all_inheritance if 0.95 <= x <= 1.05)
    inherit_count = sum(1 for x in all_inheritance if x > 1.05)

    print(f"\nGlobal mean inheritance ratio: {global_mean_inheritance:.4f}")
    print(f"Global median inheritance ratio: {global_median_inheritance:.4f}")
    print(f"Within-stanza baseline ratio: {global_mean_within:.4f}" if global_mean_within else "")
    print(f"Reset (<0.95): {reset_count}, Neutral (0.95-1.05): {neutral_count}, Inherit (>1.05): {inherit_count}")

    # Era-level analysis
    era_groups = defaultdict(list)
    for r in results:
        era_groups[r["era"]].append(r)

    era_stats = {}
    for era, poems_in_era in era_groups.items():
        ratios = [p["mean_inheritance_ratio"] for p in poems_in_era]
        within_ratios = [p["mean_within_stanza_ratio"] for p in poems_in_era
                         if p["mean_within_stanza_ratio"] is not None]
        pre_alphas = [e["pre_alpha"]
                      for p in poems_in_era for e in p["break_events"]]
        post_alphas = [e["post_alpha"]
                       for p in poems_in_era for e in p["break_events"]]
        era_stats[era] = {
            "n_poems": len(poems_in_era),
            "n_breaks": sum(p["n_breaks"] for p in poems_in_era),
            "mean_inheritance": round(statistics.mean(ratios), 4),
            "mean_within_ratio": round(statistics.mean(within_ratios), 4) if within_ratios else None,
            "mean_pre_alpha": round(statistics.mean(pre_alphas), 4) if pre_alphas else None,
            "mean_post_alpha": round(statistics.mean(post_alphas), 4) if post_alphas else None,
            "pct_reset": round(100 * sum(1 for x in ratios if x < 0.95) / len(ratios), 1),
            "pct_inherit": round(100 * sum(1 for x in ratios if x > 1.05) / len(ratios), 1),
        }

    # By break number within poem (break 1→2, 2→3, etc.)
    by_break_number = defaultdict(list)
    for r in results:
        for ev in r["break_events"]:
            by_break_number[ev["break_number"]].append(ev["inheritance_ratio"])

    break_number_stats = {}
    for bn, ratios in sorted(by_break_number.items()):
        if len(ratios) >= 5:
            break_number_stats[str(bn)] = {
                "n": len(ratios),
                "mean_inheritance": round(statistics.mean(ratios), 4),
                "median_inheritance": round(statistics.median(ratios), 4),
            }

    # Author-level analysis (min 2 poems with stanzas)
    author_groups = defaultdict(list)
    for r in results:
        author_groups[r["author"]].append(r)

    author_stats = {}
    for author, poems_by_author in author_groups.items():
        if len(poems_by_author) < 2:
            continue
        ratios = [p["mean_inheritance_ratio"] for p in poems_by_author]
        author_stats[author] = {
            "n_poems": len(poems_by_author),
            "mean_inheritance": round(statistics.mean(ratios), 4),
        }

    output = {
        "n_poems_analyzed": len(results),
        "global_stats": {
            "mean_inheritance_ratio": round(global_mean_inheritance, 4),
            "median_inheritance_ratio": round(global_median_inheritance, 4),
            "mean_within_stanza_ratio": round(global_mean_within, 4) if global_mean_within else None,
            "pct_reset": round(100 * reset_count / len(all_inheritance), 1),
            "pct_neutral": round(100 * neutral_count / len(all_inheritance), 1),
            "pct_inherit": round(100 * inherit_count / len(all_inheritance), 1),
        },
        "era_stats": era_stats,
        "by_break_number": break_number_stats,
        "author_stats": author_stats,
        "poem_results": results,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved to {OUTPUT_PATH}")

    # Print top eras by inheritance
    print("\n--- Era Inheritance Rankings (min 3 poems) ---")
    sorted_eras = sorted(
        [(e, s) for e, s in era_stats.items() if s["n_poems"] >= 3],
        key=lambda x: x[1]["mean_inheritance"],
        reverse=True,
    )
    for era, s in sorted_eras:
        print(f"  {era:20s} n={s['n_poems']:3d}  inherit={s['mean_inheritance']:.3f}  "
              f"pre_α={s['mean_pre_alpha']:.3f}  post_α={s['mean_post_alpha']:.3f}  "
              f"reset%={s['pct_reset']:.0f}%")


if __name__ == "__main__":
    main()
