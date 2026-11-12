"""
Liberating vs Channeling Surprise
==================================
After a high-S2 token, does GPT-2 become MORE uncertain (high entropy follows)
or LESS uncertain (low entropy follows)?

- "Liberating surprise": unexpected token opens new semantic possibilities (entropy rises)
- "Channeling surprise": unexpected token forces a narrow path (entropy drops)

This is distinct from s2_autocorrelation (S2→S2) — we look at S2→entropy transitions.
"""
import json
import numpy as np
from collections import defaultdict
import os

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/surprise_liberation.json"
S2_THRESHOLD = 2.0  # "high S2" threshold
LOW_S2_THRESHOLD = 0.0  # "low S2" for baseline

def filter_artifact(tok):
    """Filter stanza-break artifacts AND subword continuation tokens.
    Continuation tokens (no leading space, not start of poem) would artificially
    channel because they're partially determined by the preceding subword fragment.
    """
    if tok.get("p_newline", 0) >= 0.9:
        return False
    t = tok["token"]
    # Exclude newline-only tokens
    if t.strip() == "" or t == "\n":
        return False
    # Exclude continuation tokens (subword fragments: no space, not punctuation-led)
    # In GPT-2 tokenization, full words start with Ġ (space) or are punctuation
    # In decoded form, full words start with " " (space)
    # Continuation tokens start with a letter directly
    if not t.startswith(" ") and t[0].isalpha() and t[0].islower():
        return False
    return True

def analyze_poem(poem):
    tokens = [t for t in poem.get("tokens", []) if filter_artifact(t)]
    if len(tokens) < 4:
        return None

    liberating = []  # entropy delta after high-S2 token
    channeling = []  # same
    baseline = []    # entropy delta after low-S2 token
    liberating_examples = []

    for i, tok in enumerate(tokens[:-1]):
        s2 = tok["s2"]
        curr_entropy = tok["entropy"]
        next_entropy = tokens[i + 1]["entropy"]
        delta = next_entropy - curr_entropy  # positive = more uncertain after

        if s2 >= S2_THRESHOLD:
            liberating.append(delta)
            if len(liberating_examples) < 3 and abs(delta) > 0.5:
                liberating_examples.append({
                    "token": tok["token"],
                    "s2": round(s2, 2),
                    "curr_entropy": round(curr_entropy, 3),
                    "next_entropy": round(next_entropy, 3),
                    "delta": round(delta, 3),
                    "type": "liberating" if delta > 0 else "channeling",
                    "context": tok.get("context_before", "")[-80:]
                })
        elif s2 <= LOW_S2_THRESHOLD:
            baseline.append(delta)

    if not liberating:
        return None

    return {
        "title": poem["metadata"]["title"],
        "author": poem["metadata"]["author"],
        "era": poem["metadata"].get("era", "unknown"),
        "n_high_s2": len(liberating),
        "mean_delta_high_s2": round(float(np.mean(liberating)), 4),
        "mean_delta_baseline": round(float(np.mean(baseline)), 4) if baseline else None,
        "pct_liberating": round(100 * sum(1 for d in liberating if d > 0) / len(liberating), 1),
        "pct_channeling": round(100 * sum(1 for d in liberating if d <= 0) / len(liberating), 1),
        "examples": liberating_examples
    }


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    results = []
    for poem in data:
        r = analyze_poem(poem)
        if r:
            results.append(r)

    print(f"Analyzed {len(results)} poems with high-S2 tokens")

    # === Global summary ===
    all_high_deltas = [r["mean_delta_high_s2"] for r in results]
    all_base_deltas = [r["mean_delta_baseline"] for r in results if r["mean_delta_baseline"] is not None]
    all_pct_lib = [r["pct_liberating"] for r in results]

    print(f"\n=== GLOBAL ===")
    print(f"Mean entropy delta after high-S2: {np.mean(all_high_deltas):.4f}")
    print(f"Mean entropy delta after low-S2 (baseline): {np.mean(all_base_deltas):.4f}")
    print(f"Pct liberating (entropy rises): {np.mean(all_pct_lib):.1f}%")
    print(f"Pct channeling (entropy drops): {100 - np.mean(all_pct_lib):.1f}%")

    # === By era ===
    era_stats = defaultdict(list)
    for r in results:
        era_stats[r["era"]].append(r)

    print(f"\n=== BY ERA (sorted by % liberating) ===")
    era_summary = []
    for era, poems in era_stats.items():
        deltas = [p["mean_delta_high_s2"] for p in poems]
        pcts = [p["pct_liberating"] for p in poems]
        era_summary.append({
            "era": era,
            "n": len(poems),
            "mean_delta": round(float(np.mean(deltas)), 4),
            "pct_liberating": round(float(np.mean(pcts)), 1),
        })

    era_summary.sort(key=lambda x: -x["pct_liberating"])
    for e in era_summary:
        print(f"  {e['era']:25s} n={e['n']:3d}  Δentropy={e['mean_delta']:+.4f}  lib={e['pct_liberating']:4.1f}%")

    # === By author (min 3 poems) ===
    author_stats = defaultdict(list)
    for r in results:
        author_stats[r["author"]].append(r)

    print(f"\n=== TOP AUTHORS by % liberating (min 3 poems) ===")
    author_summary = []
    for author, poems in author_stats.items():
        if len(poems) < 3:
            continue
        pcts = [p["pct_liberating"] for p in poems]
        deltas = [p["mean_delta_high_s2"] for p in poems]
        author_summary.append({
            "author": author,
            "n": len(poems),
            "mean_delta": round(float(np.mean(deltas)), 4),
            "pct_liberating": round(float(np.mean(pcts)), 1),
        })

    author_summary.sort(key=lambda x: -x["pct_liberating"])
    print("Most liberating:")
    for a in author_summary[:10]:
        print(f"  {a['author']:30s} n={a['n']}  lib={a['pct_liberating']:.1f}%  Δ={a['mean_delta']:+.4f}")
    print("Most channeling:")
    for a in author_summary[-10:]:
        print(f"  {a['author']:30s} n={a['n']}  lib={a['pct_liberating']:.1f}%  Δ={a['mean_delta']:+.4f}")

    # Collect examples
    lib_examples = []
    chan_examples = []
    for r in results:
        for ex in r.get("examples", []):
            ex["author"] = r["author"]
            ex["title"] = r["title"]
            if ex["type"] == "liberating":
                lib_examples.append(ex)
            else:
                chan_examples.append(ex)

    lib_examples.sort(key=lambda x: -x["delta"])
    chan_examples.sort(key=lambda x: x["delta"])

    print(f"\n=== TOP LIBERATING EXAMPLES ===")
    for ex in lib_examples[:8]:
        print(f"  '{ex['token']}' (s2={ex['s2']}, Δentropy=+{ex['delta']:.3f}) — {ex['author']}")
        if ex['context']:
            print(f"    context: ...{ex['context']}")

    print(f"\n=== TOP CHANNELING EXAMPLES ===")
    for ex in chan_examples[:8]:
        print(f"  '{ex['token']}' (s2={ex['s2']}, Δentropy={ex['delta']:.3f}) — {ex['author']}")
        if ex['context']:
            print(f"    context: ...{ex['context']}")

    output = {
        "global": {
            "n_poems": len(results),
            "mean_delta_high_s2": round(float(np.mean(all_high_deltas)), 4),
            "mean_delta_baseline": round(float(np.mean(all_base_deltas)), 4),
            "pct_liberating_overall": round(float(np.mean(all_pct_lib)), 1),
        },
        "by_era": era_summary,
        "by_author": author_summary,
        "liberating_examples": lib_examples[:20],
        "channeling_examples": chan_examples[:20],
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
