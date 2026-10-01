"""
Capitalization as S2 Artifact: The Dickinson Problem

Research question: Does mid-line capitalization (Dickinson's practice of
capitalizing nouns and key words) inflate S2 scores as an artifact?

GPT-2 is case-sensitive. A capitalized word mid-sentence receives lower
probability than its lowercase equivalent, potentially creating spurious S2
spikes that reflect typography, not semantic deviance.

Method:
1. Load corpus_results.json
2. Classify tokens: sentence-initial, line-initial, mid-line-lower, mid-line-UPPER
3. Compare S2 at capitalized vs lowercase mid-line tokens
4. Identify which poets use most mid-line capitalization
5. Re-analyze a few Dickinson poems with lowercased text to quantify the artifact
"""

import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import analyze_poem, get_model


def load_corpus():
    path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")
    with open(path) as f:
        return json.load(f)


def is_mid_line_capitalized(token_str):
    """Token is mid-line capitalized: starts with uppercase but isn't special."""
    t = token_str.strip()
    if not t:
        return False
    # Must start with uppercase letter
    if not t[0].isupper():
        return False
    # Exclude all-caps (acronyms like 'I', 'USA') - but keep single capital letter
    # Actually: include "I" as it's a frequent false positive
    # Exclude tokens that are all punctuation or whitespace
    if all(c in '.,;:!?—–-\'"()[]{}' for c in t):
        return False
    return True


def classify_tokens(poem_result):
    """
    Classify each token as:
    - 'sentence_start': follows '.', '!', '?', or is position 1
    - 'line_start': token starts with '\n' in preceding context
    - 'mid_upper': mid-line uppercase
    - 'mid_lower': mid-line lowercase
    - 'other': punctuation, numbers, etc.
    """
    tokens = poem_result["tokens"]
    text = poem_result["metadata"].get("title", "")  # we'll reconstruct from tokens

    classified = []

    # Reconstruct the text from tokens to detect line/sentence boundaries
    # Token positions: position 1 = token after BOS
    all_token_strs = [t["token"] for t in tokens]

    for i, tok in enumerate(tokens):
        token_str = tok["token"]
        t_stripped = token_str.strip()

        # Determine position context
        prev_tokens = all_token_strs[max(0, i-3):i]
        prev_text = "".join(prev_tokens)

        # Check if previous non-whitespace ends a sentence
        prev_clean = prev_text.rstrip()
        ends_sentence = prev_clean.endswith(('.', '!', '?')) if prev_clean else True

        # Check if there's a newline in the preceding token(s)
        has_newline = any('\n' in pt for pt in prev_tokens)

        # Classify
        if i == 0:
            category = 'sentence_start'
        elif ends_sentence:
            category = 'sentence_start'
        elif has_newline:
            category = 'line_start'
        elif not t_stripped:
            category = 'whitespace'
        elif not any(c.isalpha() for c in t_stripped):
            category = 'other'
        elif t_stripped[0].isupper():
            category = 'mid_upper'
        else:
            category = 'mid_lower'

        classified.append({**tok, "category": category})

    return classified


def poet_capitalization_profile(results):
    """Per-poet: fraction of mid-line tokens that are capitalized, and avg S2 by category."""
    poet_data = {}

    for r in results:
        author = r["metadata"]["author"]
        if author not in poet_data:
            poet_data[author] = {
                "mid_upper_s2": [], "mid_lower_s2": [],
                "mid_upper_count": 0, "mid_lower_count": 0,
                "total_tokens": 0,
            }

        classified = classify_tokens(r)

        for tok in classified:
            cat = tok["category"]
            if cat == "mid_upper":
                poet_data[author]["mid_upper_s2"].append(tok["s2"])
                poet_data[author]["mid_upper_count"] += 1
            elif cat == "mid_lower":
                poet_data[author]["mid_lower_s2"].append(tok["s2"])
                poet_data[author]["mid_lower_count"] += 1
            poet_data[author]["total_tokens"] += 1

    # Summarize
    profiles = []
    for author, d in poet_data.items():
        if d["total_tokens"] < 20:
            continue
        upper_n = d["mid_upper_count"]
        lower_n = d["mid_lower_count"]
        upper_s2 = sum(d["mid_upper_s2"]) / upper_n if upper_n > 0 else None
        lower_s2 = sum(d["mid_lower_s2"]) / lower_n if lower_n > 0 else None
        upper_rate = upper_n / (upper_n + lower_n) if (upper_n + lower_n) > 0 else 0

        profiles.append({
            "author": author,
            "upper_rate": round(upper_rate, 3),
            "upper_n": upper_n,
            "lower_n": lower_n,
            "avg_s2_upper": round(upper_s2, 3) if upper_s2 is not None else None,
            "avg_s2_lower": round(lower_s2, 3) if lower_s2 is not None else None,
            "s2_delta": round(upper_s2 - lower_s2, 3) if (upper_s2 is not None and lower_s2 is not None) else None,
        })

    return sorted(profiles, key=lambda x: x["upper_rate"], reverse=True)


def corpus_wide_analysis(results):
    """Global S2 stats by token category."""
    cat_s2 = {"sentence_start": [], "line_start": [], "mid_upper": [], "mid_lower": []}

    for r in results:
        classified = classify_tokens(r)
        for tok in classified:
            cat = tok["category"]
            if cat in cat_s2:
                cat_s2[cat].append(tok["s2"])

    stats = {}
    for cat, vals in cat_s2.items():
        if vals:
            n = len(vals)
            mean = sum(vals) / n
            pos_ratio = sum(1 for v in vals if v > 0) / n
            stats[cat] = {
                "n": n,
                "mean_s2": round(mean, 3),
                "pos_ratio": round(pos_ratio, 3),
            }
    return stats


def lowercasing_experiment(poems_to_test):
    """
    For selected poems, compare S2 with original vs lowercased text.
    Returns comparison data.
    """
    print("Loading model for lowercasing experiment...")
    get_model("en")

    comparisons = []
    for poem in poems_to_test:
        print(f"  Analyzing: {poem['author']} - {poem['title']}")

        # Original analysis
        orig = analyze_poem(
            text=poem["text"],
            title=poem["title"],
            author=poem["author"],
            year=poem.get("year"),
            era=poem.get("era", ""),
        )

        # Lowercased analysis
        lower_text = poem["text"].lower()
        lower = analyze_poem(
            text=lower_text,
            title=poem["title"] + " [lowercased]",
            author=poem["author"],
            year=poem.get("year"),
            era=poem.get("era", ""),
        )

        # Token-level comparison
        orig_tokens = orig["tokens"]
        lower_tokens = lower["tokens"]

        # Find tokens that changed case
        changed = []
        for ot, lt in zip(orig_tokens, lower_tokens):
            if ot["token"].strip() != lt["token"].strip():
                changed.append({
                    "position": ot["position"],
                    "original_token": ot["token"],
                    "lower_token": lt["token"],
                    "orig_s2": ot["s2"],
                    "lower_s2": lt["s2"],
                    "s2_delta": round(ot["s2"] - lt["s2"], 3),
                })

        comparisons.append({
            "title": poem["title"],
            "author": poem["author"],
            "orig_avg_s2": orig["summary"]["avg_s2"],
            "lower_avg_s2": lower["summary"]["avg_s2"],
            "avg_s2_delta": round(orig["summary"]["avg_s2"] - lower["summary"]["avg_s2"], 3),
            "n_changed_tokens": len(changed),
            "changed_tokens": changed[:20],  # top 20
            "high_delta_tokens": sorted(changed, key=lambda x: abs(x["s2_delta"]), reverse=True)[:10],
        })

    return comparisons


def get_dickinson_poems():
    """Get Emily Dickinson poems from corpus."""
    from corpus.poems import POEMS
    return [p for p in POEMS if "Dickinson" in p.get("author", "")]


def main():
    print("Loading corpus results...")
    results = load_corpus()
    print(f"  Loaded {len(results)} texts")

    # 1. Corpus-wide analysis by token category
    print("\nAnalyzing token categories corpus-wide...")
    global_stats = corpus_wide_analysis(results)

    # 2. Per-poet capitalization profiles
    print("Computing per-poet capitalization profiles...")
    profiles = poet_capitalization_profile(results)

    # 3. Lowercasing experiment on Dickinson + a control
    print("\nRunning lowercasing experiment...")
    dickinson_poems = get_dickinson_poems()
    print(f"  Found {len(dickinson_poems)} Dickinson poems in corpus")

    # Also grab a control poet who doesn't capitalize mid-line
    from corpus.poems import POEMS
    whitman_poems = [p for p in POEMS if "Whitman" in p.get("author", "")][:2]
    cummings_poems = [p for p in POEMS if "cummings" in p.get("author", "").lower() or
                      "Cummings" in p.get("author", "")][:2]

    # Run lowercasing experiment (small set for speed)
    test_poems = dickinson_poems[:3] + whitman_poems[:1] + cummings_poems[:1]
    comparisons = lowercasing_experiment(test_poems)

    # Save results
    output = {
        "global_category_stats": global_stats,
        "poet_capitalization_profiles": profiles[:30],
        "lowercasing_comparisons": comparisons,
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "capitalization_artifact.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved results to {out_path}")

    # Print summary
    print("\n=== CORPUS-WIDE TOKEN CATEGORY STATS ===")
    for cat, stat in global_stats.items():
        print(f"  {cat:<20} n={stat['n']:>6}  mean_S2={stat['mean_s2']:>7.3f}  pos%={stat['pos_ratio']:.0%}")

    print("\n=== TOP 15 POETS BY MID-LINE CAPITALIZATION RATE ===")
    print(f"  {'Author':<25} {'Upper%':>7} {'nUpper':>7} {'avgS2↑':>8} {'avgS2↓':>8} {'delta':>7}")
    for p in profiles[:15]:
        delta_str = f"{p['s2_delta']:+.3f}" if p['s2_delta'] is not None else "  N/A"
        u_s2 = f"{p['avg_s2_upper']:>7.3f}" if p['avg_s2_upper'] is not None else "   N/A"
        l_s2 = f"{p['avg_s2_lower']:>7.3f}" if p['avg_s2_lower'] is not None else "   N/A"
        print(f"  {p['author']:<25} {p['upper_rate']:>6.1%} {p['upper_n']:>7}  {u_s2}  {l_s2}  {delta_str}")

    print("\n=== LOWERCASING EXPERIMENT ===")
    for c in comparisons:
        print(f"  {c['author'][:20]:<22} {c['title'][:25]:<27}: "
              f"orig_S2={c['orig_avg_s2']:>6.3f}  lower_S2={c['lower_avg_s2']:>6.3f}  "
              f"delta={c['avg_s2_delta']:+.3f}  changed={c['n_changed_tokens']}")
        if c['high_delta_tokens']:
            print(f"    Top changed tokens:")
            for tok in c['high_delta_tokens'][:5]:
                print(f"      '{tok['original_token'].strip()}'→'{tok['lower_token'].strip()}': "
                      f"S2 {tok['orig_s2']:+.2f} → {tok['lower_s2']:+.2f} (Δ={tok['s2_delta']:+.2f})")

    return output


if __name__ == "__main__":
    main()
