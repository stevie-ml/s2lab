"""
The Cliché Test: Does S2 Track Poetic Originality?

Hypothesis: S2 measures how much a text deviates from GPT-2's statistical
expectations. Clichéd, formulaic poetry uses stock phrases that GPT-2 was
trained on millions of times — so it should predict them accurately, yielding
low S2 (possibly near or below zero). Original, inventive poetry should yield
higher S2.

Prediction: cliche_control << prose_control < generic_poetry < ecstatic_verse

If confirmed, S2 is not just a statistical anomaly detector — it's a
quantitative originality signal.
"""

import json
import sys
import os
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")
OUTPUT_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "cliche_test.json")


def flatten(r):
    """Flatten the nested corpus_results format into a flat dict."""
    meta = r.get("metadata", r)
    summ = r.get("summary", r)
    tokens = r.get("tokens", [])
    return {
        "title": meta.get("title", r.get("title", "")),
        "author": meta.get("author", r.get("author", "")),
        "era": meta.get("era", r.get("era", "")),
        "avg_s2": summ.get("avg_s2", r.get("avg_s2", 0)),
        "max_s2": summ.get("max_s2", r.get("max_s2", 0)),
        "std_s2": summ.get("std_s2", r.get("std_s2", 0)),
        "pos_s2_ratio": summ.get("pos_s2_ratio", r.get("pos_s2_ratio", 0)),
        "tokens": tokens,
    }


def load_existing():
    with open(RESULTS_FILE) as f:
        raw = json.load(f)
    return [flatten(r) for r in raw]


def compute_new(poems):
    """Analyze poems not yet in corpus_results.json."""
    from engine import analyze_poem
    results = []
    for p in poems:
        print(f"  Analyzing: {p['title']}...", flush=True)
        raw = analyze_poem(p["text"], p["title"], p["author"], p.get("year"), p.get("era", ""))
        r = flatten(raw)
        results.append(r)
        print(f"    avg_s2={r['avg_s2']:.3f}  pos_s2_ratio={r['pos_s2_ratio']:.2%}")
    return results


def group_stats(items):
    if not items:
        return None
    avg = statistics.mean(items)
    std = statistics.stdev(items) if len(items) > 1 else 0.0
    return {"n": len(items), "mean": round(avg, 4), "std": round(std, 4),
            "min": round(min(items), 4), "max": round(max(items), 4)}


def run():
    print("Loading existing corpus results...")
    existing = load_existing()

    # Group existing results by era
    by_era = {}
    for r in existing:
        era = r.get("era", "unknown")
        by_era.setdefault(era, []).append(r)

    # Identify new poems (in poems.py but not in corpus_results)
    from corpus.poems import POEMS
    existing_titles = {r["title"] for r in existing}
    new_poems = [p for p in POEMS if p["title"] not in existing_titles]

    print(f"\nFound {len(new_poems)} new poems not yet analyzed:")
    for p in new_poems:
        print(f"  [{p['era']}] {p['title']}")

    print("\nComputing S2 for new poems...")
    new_results = compute_new(new_poems)

    # Merge new results into by_era
    for r in new_results:
        era = r.get("era", "unknown")
        by_era.setdefault(era, []).append(r)

    # Build summary table
    focus_eras = [
        ("cliche_control",   "Synthetic Cliché"),
        ("control",          "Prose Control"),
        ("nursery_rhyme",    "Nursery Rhyme"),
        ("song_lyrics",      "Song Lyrics"),
        ("found_poetry",     "Found Poetry"),
        ("spoken_word",      "Spoken Word"),
        ("prose_poetry",     "Prose Poetry"),
        ("ballad",           "Ballad"),
        ("contemporary",     "Contemporary"),
        ("new_york_school",  "New York School"),
        ("romantic",         "Romantic"),
        ("victorian",        "Victorian"),
        ("modernist",        "Modernist"),
        ("confessional",     "Confessional"),
        ("haiku",            "Haiku"),
        ("beat",             "Beat"),
        ("18th_century",     "18th Century"),
    ]

    print("\n\n=== S2 BY GROUP (ordered low→high) ===\n")
    print(f"{'Group':<22}  {'n':>3}  {'Avg S2':>8}  {'±σ':>6}  {'Min':>7}  {'Max':>7}  {'%+S2':>6}")
    print("-" * 72)

    summary = []
    for era_key, era_label in focus_eras:
        if era_key not in by_era:
            continue
        poems_in_era = by_era[era_key]
        s2_vals = [r["avg_s2"] for r in poems_in_era]
        pos_ratios = [r["pos_s2_ratio"] for r in poems_in_era]
        stats = group_stats(s2_vals)
        if stats is None:
            continue
        avg_pos = statistics.mean(pos_ratios)
        print(f"{era_label:<22}  {stats['n']:>3}  {stats['mean']:>8.3f}  "
              f"{stats['std']:>6.3f}  {stats['min']:>7.3f}  {stats['max']:>7.3f}  "
              f"{avg_pos:>6.1%}")
        summary.append({
            "era": era_key, "label": era_label, **stats,
            "avg_pos_s2_ratio": round(avg_pos, 4)
        })

    # Detailed cliché poems
    print("\n\n=== INDIVIDUAL CLICHÉ POEMS ===\n")
    cliche_results = [r for r in new_results if r.get("era") == "cliche_control"]
    for r in cliche_results:
        print(f"  {r['title']}")
        print(f"    avg_s2={r['avg_s2']:.3f}  pos_s2_ratio={r['pos_s2_ratio']:.2%}  "
              f"max_s2={r['max_s2']:.2f}  std_s2={r['std_s2']:.3f}")
        # Top-3 highest S2 tokens (what even a cliché poem surprises on)
        top_tokens = sorted(r["tokens"], key=lambda t: t["s2"], reverse=True)[:5]
        print(f"    Highest-S2 tokens:")
        for tok in top_tokens:
            unsaid = tok["alternatives"][0]["token"] if tok["alternatives"] else "?"
            print(f"      '{tok['token'].strip()}' (s2={tok['s2']:.2f}, expected '{unsaid.strip()}')")

    # Detailed ecstatic / canonical new poems
    print("\n\n=== NEW CANONICAL POEMS ===\n")
    canonical_results = [r for r in new_results if r.get("era") != "cliche_control"]
    for r in canonical_results:
        print(f"  [{r.get('era')}] {r['title']} — {r.get('author','')}")
        print(f"    avg_s2={r['avg_s2']:.3f}  pos_s2_ratio={r['pos_s2_ratio']:.2%}  "
              f"max_s2={r['max_s2']:.2f}")

    # Key comparison: cliché vs prose vs poetry
    cliche_s2 = [r["avg_s2"] for r in (by_era.get("cliche_control") or [])]
    prose_s2   = [r["avg_s2"] for r in (by_era.get("control") or [])]
    poetry_s2  = []
    for era_key, _ in focus_eras:
        if era_key not in ("cliche_control", "control"):
            poetry_s2.extend(r["avg_s2"] for r in (by_era.get(era_key) or []))

    print("\n\n=== KEY COMPARISON ===\n")
    print(f"  Synthetic Cliché   avg S2: {statistics.mean(cliche_s2):.3f}  (n={len(cliche_s2)})")
    print(f"  Prose Control      avg S2: {statistics.mean(prose_s2):.3f}  (n={len(prose_s2)})")
    print(f"  Poetry (all eras)  avg S2: {statistics.mean(poetry_s2):.3f}  (n={len(poetry_s2)})")

    cliche_below_prose = sum(1 for c in cliche_s2 for p in prose_s2 if c < p)
    print(f"\n  Cliché poems below prose-control avg: "
          f"{sum(1 for c in cliche_s2 if c < statistics.mean(prose_s2))}/{len(cliche_s2)}")

    # Save results
    output = {
        "experiment": "cliche_test",
        "date": "2026-09-21",
        "hypothesis": "S2 tracks originality: cliché < prose < poetry",
        "summary": summary,
        "new_poems": [
            {
                "title": r["title"],
                "author": r.get("author", ""),
                "era": r.get("era", ""),
                "avg_s2": r["avg_s2"],
                "pos_s2_ratio": r["pos_s2_ratio"],
                "max_s2": r["max_s2"],
                "std_s2": r["std_s2"],
            }
            for r in new_results
        ],
        "key_comparison": {
            "cliche_avg_s2": round(statistics.mean(cliche_s2), 4),
            "prose_avg_s2":  round(statistics.mean(prose_s2), 4),
            "poetry_avg_s2": round(statistics.mean(poetry_s2), 4),
        },
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {OUTPUT_FILE}")

    return output


if __name__ == "__main__":
    run()
