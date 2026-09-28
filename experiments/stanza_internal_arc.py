"""
Stanza-Internal Arc: Is "Deviate Early, Resolve Late" Fractal?

Prior work (within_poem_type_arc.py) established that whole poems show
a strong "deviate early, resolve late" arc: Type I% (Definite Straussian Gap)
is highest in the first third of poems and declines toward the end.

This experiment asks: does the same arc hold *within individual stanzas*?

If each stanza also front-loads Type I and back-loads Type III, the
pattern is *self-similar across scales* — a fractal property of poetic
information management.

If stanzas do not show the arc (or show the reverse), it would suggest the
whole-poem arc emerges from macro-structure (the poem's argument/narrative)
rather than from any local principle of line-group composition.

Method:
  - Uses corpus_results.json (pre-computed S2/entropy/rank)
  - Re-tokenizes each poem (tokenizer only, no model) to map positions → stanzas
  - For each stanza with ≥15 artifact-free tokens, splits into thirds
  - Classifies tokens (Type I/II/III/IV) using corpus-wide entropy median
  - Aggregates stanza arcs vs. whole-poem arcs
"""

import json
import statistics
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from corpus.poems import POEMS

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")
RANK_THRESHOLD = 10
MIN_STANZA_TOKENS = 15  # minimum artifact-free tokens per stanza to analyze


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    top = alts[0]
    return top["token"] in ("\n", "\r\n", "\r") and top["prob"] >= 0.9


def classify_token(tok, entropy_median):
    if is_artifact(tok):
        return None
    h = tok["entropy"]
    rank = tok.get("rank", 9999)
    low_entropy = h < entropy_median
    expected = rank <= RANK_THRESHOLD
    if low_entropy and not expected:
        return "I"
    elif not low_entropy and not expected:
        return "II"
    elif low_entropy and expected:
        return "III"
    else:
        return "IV"


def build_position_to_stanza(poem_text, tokenizer):
    """
    Tokenize poem_text, map each token (1-indexed position) to its stanza index.
    Returns dict: position (1-based) -> stanza_index (0-based), or None if not in a stanza.
    """
    # Parse stanzas (groups of non-empty lines separated by blank lines)
    raw_lines = poem_text.split("\n")
    stanza_char_ranges = []  # list of (start_char, end_char) for each stanza
    current_stanza_start = None
    current_stanza_end = None
    char_pos = 0

    for line in raw_lines:
        line_start = char_pos
        line_end = char_pos + len(line)
        char_pos += len(line) + 1  # +1 for \n

        if line.strip() == "":
            if current_stanza_start is not None:
                stanza_char_ranges.append((current_stanza_start, current_stanza_end))
                current_stanza_start = None
                current_stanza_end = None
        else:
            if current_stanza_start is None:
                current_stanza_start = line_start
            current_stanza_end = line_end

    if current_stanza_start is not None:
        stanza_char_ranges.append((current_stanza_start, current_stanza_end))

    if len(stanza_char_ranges) < 2:
        return None, stanza_char_ranges  # Need at least 2 stanzas

    # Tokenize to get character offsets
    ids = tokenizer.encode(poem_text)
    tokens = [tokenizer.decode([i]) for i in ids]

    # Build character offset for each token
    char_offsets = []
    offset = 0
    for t in tokens:
        char_offsets.append(offset)
        offset += len(t)

    # Map each position (1-indexed) to stanza index
    pos_to_stanza = {}
    for tok_idx in range(1, len(tokens)):
        tok_char = char_offsets[tok_idx]
        stanza_idx = None
        for si, (s_start, s_end) in enumerate(stanza_char_ranges):
            if s_start <= tok_char <= s_end:
                stanza_idx = si
                break
        pos_to_stanza[tok_idx] = stanza_idx  # None if in blank line between stanzas

    return pos_to_stanza, stanza_char_ranges


def type_stats(type_list):
    counts = defaultdict(int)
    for t in type_list:
        counts[t] += 1
    total = sum(counts.values())
    if total == 0:
        return None
    return {
        "n": total,
        "I":   round(counts["I"] / total * 100, 1),
        "III": round(counts["III"] / total * 100, 1),
        "contrast": round((counts["I"] - counts["III"]) / total, 4),
    }


def run():
    # Load tokenizer (no model needed)
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained("gpt2")
    except Exception as e:
        print(f"Error loading tokenizer: {e}")
        sys.exit(1)

    print("Tokenizer loaded.")

    with open(RESULTS_PATH) as f:
        corpus_data = json.load(f)

    # Build corpus entropy median
    all_entropies = []
    for poem in corpus_data:
        for tok in poem["tokens"]:
            if not is_artifact(tok) and tok["entropy"] > 0:
                all_entropies.append(tok["entropy"])
    entropy_median = statistics.median(all_entropies)
    print(f"Corpus entropy median: {entropy_median:.3f} bits")
    print(f"Total poems in corpus: {len(corpus_data)}")

    # Build lookup from title to poem text
    title_to_text = {p["title"]: p["text"] for p in POEMS}

    stanza_arcs = []      # per-stanza arc data
    poem_arc_summary = [] # per-poem summary
    n_analyzed_poems = 0
    n_analyzed_stanzas = 0
    n_skipped_poems = 0

    for poem_data in corpus_data:
        meta = poem_data["metadata"]
        title = meta["title"]
        era = meta.get("era", "unknown")
        language = meta.get("language", "en")

        if language != "en":
            continue
        if era == "control":
            continue

        poem_text = title_to_text.get(title)
        if poem_text is None:
            continue
        if "\n\n" not in poem_text:
            continue  # No stanza breaks

        # Map positions to stanzas
        pos_to_stanza, stanza_ranges = build_position_to_stanza(poem_text, tokenizer)
        if pos_to_stanza is None:
            continue  # < 2 stanzas
        n_stanzas = len(stanza_ranges)

        # Group tokens by stanza
        stanza_tokens = defaultdict(list)  # stanza_idx -> [(position, type)]
        for tok in poem_data["tokens"]:
            pos = tok["position"]
            stanza_idx = pos_to_stanza.get(pos)
            if stanza_idx is None:
                continue
            qtype = classify_token(tok, entropy_median)
            if qtype is None:
                continue
            stanza_tokens[stanza_idx].append((pos, qtype))

        # Analyze each stanza's internal arc
        poem_stanza_arcs = []
        for si in range(n_stanzas):
            toks = stanza_tokens[si]
            if len(toks) < MIN_STANZA_TOKENS:
                continue

            n = len(toks)
            t1 = [t for _, t in toks[:n // 3]]
            t3 = [t for _, t in toks[2 * n // 3:]]

            s1 = type_stats(t1)
            s3 = type_stats(t3)
            if not s1 or not s3:
                continue

            arc_I = round(s3["I"] - s1["I"], 2)
            arc_III = round(s3["III"] - s1["III"], 2)

            stanza_arcs.append({
                "poem": title,
                "author": meta.get("author", ""),
                "era": era,
                "stanza_idx": si,
                "n_stanzas": n_stanzas,
                "stanza_position": "first" if si == 0 else ("last" if si == n_stanzas - 1 else "middle"),
                "n": n,
                "first_I": s1["I"],
                "last_I": s3["I"],
                "first_III": s1["III"],
                "last_III": s3["III"],
                "arc_I": arc_I,
                "arc_III": arc_III,
                "arc_contrast": round((s3["contrast"] - s1["contrast"]), 4),
            })
            poem_stanza_arcs.append(arc_I)
            n_analyzed_stanzas += 1

        if poem_stanza_arcs:
            n_analyzed_poems += 1
            poem_arc_summary.append({
                "title": title,
                "author": meta.get("author", ""),
                "era": era,
                "n_stanzas": n_stanzas,
                "n_usable_stanzas": len(poem_stanza_arcs),
                "avg_stanza_arc_I": round(statistics.mean(poem_stanza_arcs), 2),
            })
        else:
            n_skipped_poems += 1

    print(f"\nAnalyzed: {n_analyzed_poems} poems, {n_analyzed_stanzas} stanzas")
    print(f"Skipped (no usable stanzas): {n_skipped_poems}\n")

    # ── FINDING 1: Global stanza arc direction ────────────────────────────────
    all_arc_I = [s["arc_I"] for s in stanza_arcs]
    all_arc_III = [s["arc_III"] for s in stanza_arcs]
    n_negative_arc = sum(1 for x in all_arc_I if x < 0)
    n_positive_arc = sum(1 for x in all_arc_I if x > 0)
    mean_arc_I = statistics.mean(all_arc_I)
    mean_arc_III = statistics.mean(all_arc_III)

    print("=" * 65)
    print("FINDING 1: Global Stanza Arc Direction")
    print("=" * 65)
    print(f"  Stanzas where arc_I < 0 (deviate early): {n_negative_arc} / {len(all_arc_I)} = {100*n_negative_arc/len(all_arc_I):.1f}%")
    print(f"  Stanzas where arc_I > 0 (buildup-release): {n_positive_arc} / {len(all_arc_I)} = {100*n_positive_arc/len(all_arc_I):.1f}%")
    print(f"  Mean arc_I (across stanzas): {mean_arc_I:+.2f}")
    print(f"  Mean arc_III (across stanzas): {mean_arc_III:+.2f}")

    # ── FINDING 2: Stanza position within poem ────────────────────────────────
    print("\n" + "=" * 65)
    print("FINDING 2: Arc by Stanza Position in Poem")
    print("=" * 65)
    print(f"{'Stanza position':<16} {'N':>5} {'%deviate_early':>15} {'mean arc_I':>12} {'mean arc_III':>13}")
    print("-" * 65)
    for pos_label in ["first", "middle", "last"]:
        subset = [s for s in stanza_arcs if s["stanza_position"] == pos_label]
        if not subset:
            continue
        arcs = [s["arc_I"] for s in subset]
        neg_pct = 100 * sum(1 for x in arcs if x < 0) / len(arcs)
        print(f"{pos_label:<16} {len(subset):>5} {neg_pct:>14.1f}% {statistics.mean(arcs):>+12.2f} "
              f"{statistics.mean(s['arc_III'] for s in subset):>+13.2f}")

    # ── FINDING 3: Per-era stanza arc ─────────────────────────────────────────
    print("\n" + "=" * 65)
    print("FINDING 3: Per-Era Stanza Arc (mean arc_I, stanzas)")
    print("=" * 65)
    era_data = defaultdict(list)
    for s in stanza_arcs:
        era_data[s["era"]].append(s["arc_I"])
    era_rows = []
    for era, arcs in era_data.items():
        if len(arcs) < 3:
            continue
        neg_pct = 100 * sum(1 for x in arcs if x < 0) / len(arcs)
        era_rows.append({
            "era": era,
            "n": len(arcs),
            "mean_arc": round(statistics.mean(arcs), 2),
            "neg_pct": round(neg_pct, 1),
        })
    era_rows.sort(key=lambda r: r["mean_arc"])
    print(f"{'Era':<22} {'N':>5} {'mean arc_I':>12} {'% deviate_early':>16}")
    print("-" * 60)
    for r in era_rows:
        print(f"  {r['era']:<20} {r['n']:>5} {r['mean_arc']:>+12.2f} {r['neg_pct']:>15.1f}%")

    # ── FINDING 4: First stanza vs. rest of poem ──────────────────────────────
    print("\n" + "=" * 65)
    print("FINDING 4: First Stanza vs. Later Stanzas (within same poem)")
    print("=" * 65)
    first_arcs = [s["arc_I"] for s in stanza_arcs if s["stanza_position"] == "first"]
    later_arcs = [s["arc_I"] for s in stanza_arcs if s["stanza_position"] != "first"]
    print(f"  First stanza avg arc_I:  {statistics.mean(first_arcs):+.2f}  (n={len(first_arcs)})")
    print(f"  Later stanzas avg arc_I: {statistics.mean(later_arcs):+.2f}  (n={len(later_arcs)})")

    # ── FINDING 5: Compare stanza-level arc to poem-level arc ─────────────────
    print("\n" + "=" * 65)
    print("FINDING 5: Stanza Arc vs. Poem-Level Arc (same poems)")
    print("=" * 65)
    # For poems where we know the poem-level arc from within_poem_type_arc results, compare
    # Here we compute the poem-level arc from the same data for consistency
    poem_level_arcs = []
    for poem_data in corpus_data:
        meta = poem_data["metadata"]
        if meta.get("language", "en") != "en":
            continue
        if meta.get("era", "") == "control":
            continue
        classified = []
        for tok in poem_data["tokens"]:
            qtype = classify_token(tok, entropy_median)
            if qtype is not None:
                classified.append(qtype)
        if len(classified) < 30:
            continue
        n = len(classified)
        t1 = classified[:n // 3]
        t3 = classified[2 * n // 3:]
        s1 = type_stats(t1)
        s3 = type_stats(t3)
        if s1 and s3:
            poem_level_arcs.append(s3["I"] - s1["I"])

    if poem_level_arcs:
        poem_neg = 100 * sum(1 for x in poem_level_arcs if x < 0) / len(poem_level_arcs)
        stanza_neg = 100 * n_negative_arc / len(all_arc_I)
        print(f"  Poem-level: {poem_neg:.1f}% show deviate-early arc (n={len(poem_level_arcs)} poems)")
        print(f"  Stanza-level: {stanza_neg:.1f}% show deviate-early arc (n={len(all_arc_I)} stanzas)")

    # ── Top examples ──────────────────────────────────────────────────────────
    print("\n" + "=" * 65)
    print("TOP 10 STANZAS: Strongest 'deviate early' (most negative arc_I)")
    print("=" * 65)
    sorted_stanzas = sorted(stanza_arcs, key=lambda s: s["arc_I"])
    for s in sorted_stanzas[:10]:
        print(f"  arc_I={s['arc_I']:+.1f}  stanza {s['stanza_idx']+1}/{s['n_stanzas']}  "
              f"{s['author']}: '{s['poem'][:40]}' ({s['era']})")

    print("\n" + "=" * 65)
    print("TOP 10 STANZAS: Strongest 'buildup-release' (most positive arc_I)")
    print("=" * 65)
    for s in sorted(stanza_arcs, key=lambda s: -s["arc_I"])[:10]:
        print(f"  arc_I={s['arc_I']:+.1f}  stanza {s['stanza_idx']+1}/{s['n_stanzas']}  "
              f"{s['author']}: '{s['poem'][:40]}' ({s['era']})")

    # Save results
    out = {
        "entropy_median": entropy_median,
        "n_poems_analyzed": n_analyzed_poems,
        "n_stanzas_analyzed": n_analyzed_stanzas,
        "global": {
            "pct_deviate_early": round(100 * n_negative_arc / len(all_arc_I), 1),
            "mean_arc_I": round(mean_arc_I, 2),
            "mean_arc_III": round(mean_arc_III, 2),
        },
        "by_stanza_position": {
            pos_label: {
                "n": len([s for s in stanza_arcs if s["stanza_position"] == pos_label]),
                "mean_arc_I": round(statistics.mean(
                    [s["arc_I"] for s in stanza_arcs if s["stanza_position"] == pos_label]
                ), 2) if any(s["stanza_position"] == pos_label for s in stanza_arcs) else None,
                "pct_deviate_early": round(100 * sum(
                    1 for s in stanza_arcs if s["stanza_position"] == pos_label and s["arc_I"] < 0
                ) / max(1, len([s for s in stanza_arcs if s["stanza_position"] == pos_label])), 1)
            }
            for pos_label in ["first", "middle", "last"]
        },
        "era_rows": era_rows,
        "poem_level_pct_deviate_early": round(poem_neg, 1) if poem_level_arcs else None,
        "stanza_arcs_sample": sorted_stanzas[:20],
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "stanza_internal_arc.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return out


if __name__ == "__main__":
    results = run()
