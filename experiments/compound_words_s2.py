"""
S2 at the Hyphen: Information-Theoretic Analysis of Compound Words in Poetry

Hypothesis: The second element of hyphenated compound words (wine-dark, rose-fingered,
iron-grey, star-crossed) should show higher S2 than comparable standalone words,
because:
(1) After "wine-", the model has an unusual context that raises surprisal for
    whatever follows
(2) Poets who coin compounds are making lexical choices the model never trained on

We compare:
- Tokens immediately after "-" (second elements of compounds)
- Tokens after non-hyphen context (baseline)

Split by: poetry vs prose, era, and word class (Adj, Noun, Verb)
"""

import json
import sys
import re
from collections import defaultdict
import statistics

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def is_artifact(token_data):
    """Stanza-break artifact filter"""
    return token_data.get("p_newline", 0) >= 0.9

def classify_token_class(token_text):
    """Rough POS classification by suffix/form"""
    t = token_text.strip().lower()
    # Common adjective suffixes
    adj_suffixes = ("ful", "less", "ish", "ous", "ive", "al", "ic", "ed", "en", "y")
    # Common noun suffixes
    noun_suffixes = ("ness", "tion", "ity", "ment", "er", "or", "ist", "ism", "age")
    # Common verb suffixes
    verb_suffixes = ("ing", "ize", "ise", "ate", "ify")

    for s in adj_suffixes:
        if t.endswith(s) and len(t) > len(s) + 2:
            return "ADJ"
    for s in verb_suffixes:
        if t.endswith(s) and len(t) > len(s) + 2:
            return "VERB"
    for s in noun_suffixes:
        if t.endswith(s) and len(t) > len(s) + 2:
            return "NOUN"
    return "OTHER"

def analyze_compound_elements(poem_data):
    """
    Find positions where the previous token was "-" (compound second element).
    Also find positions where previous token was a word (not hyphen) for baseline.
    Returns lists of (s2, era, era_type, word_class) tuples.
    """
    tokens = poem_data.get("tokens", [])
    meta = poem_data.get("metadata", {})
    era = meta.get("era", "unknown")
    is_control = era == "control"
    category = "prose" if is_control else "poetry"

    compound_events = []   # second element of compound
    baseline_events = []   # adjacent word pair (not hyphen)

    for i, tok in enumerate(tokens):
        if is_artifact(tok):
            continue
        s2 = tok.get("s2", 0)
        token_text = tok.get("token", "")

        if i == 0:
            continue

        prev_tok = tokens[i - 1]
        prev_text = prev_tok.get("token", "")

        # Check if previous token is a hyphen
        if prev_text.strip() == "-":
            word_class = classify_token_class(token_text)
            compound_events.append({
                "s2": s2,
                "surprisal": tok.get("surprisal", 0),
                "entropy": tok.get("entropy", 0),
                "token": token_text,
                "era": era,
                "category": category,
                "word_class": word_class,
            })
        elif (
            prev_text.strip() not in ["-", ".", ",", ";", ":", "!", "?", "(", ")", '"', "'", "\n"]
            and prev_text.strip()  # not empty
            and token_text.strip() not in ["-", ".", ",", ";", ":", "!", "?"]
            and not is_artifact(prev_tok)
        ):
            # Baseline: adjacent content word pair
            word_class = classify_token_class(token_text)
            baseline_events.append({
                "s2": s2,
                "surprisal": tok.get("surprisal", 0),
                "entropy": tok.get("entropy", 0),
                "token": token_text,
                "era": era,
                "category": category,
                "word_class": word_class,
            })

    return compound_events, baseline_events

def find_notable_compounds(poem_data, top_n=5):
    """Find the highest-S2 compound moments in a poem"""
    tokens = poem_data.get("tokens", [])
    meta = poem_data.get("metadata", {})
    title = meta.get("title", "untitled")
    author = meta.get("author", "?")

    compounds = []
    for i, tok in enumerate(tokens):
        if is_artifact(tok) or i == 0:
            continue
        prev = tokens[i - 1]
        if prev.get("token", "").strip() == "-":
            # Get the full compound: token before hyphen + hyphen + current token
            first_part = tokens[i - 2].get("token", "") if i >= 2 else ""
            full_compound = (first_part + "-" + tok.get("token", "")).strip()
            compounds.append({
                "compound": full_compound,
                "s2": tok.get("s2", 0),
                "title": title,
                "author": author,
                "suppressed_top1": (
                    tok.get("alternatives", [{}])[0].get("token", "?")
                    if tok.get("alternatives") else "?"
                ),
            })

    compounds.sort(key=lambda x: -x["s2"])
    return compounds[:top_n]

def main():
    print("Loading corpus...", file=sys.stderr)
    data = load_corpus()

    all_compound = []
    all_baseline = []
    notable = []

    era_compound = defaultdict(list)
    era_baseline = defaultdict(list)

    for poem in data:
        ce, be = analyze_compound_elements(poem)
        all_compound.extend(ce)
        all_baseline.extend(be)
        for e in ce:
            era_compound[e["era"]].append(e["s2"])
        for e in be:
            era_baseline[e["era"]].append(e["s2"])
        notable.extend(find_notable_compounds(poem, top_n=3))

    # Global stats
    compound_s2 = [e["s2"] for e in all_compound]
    baseline_s2 = [e["s2"] for e in all_baseline]

    def stats(vals):
        if not vals:
            return {"n": 0, "mean": 0, "std": 0, "median": 0, "pos_pct": 0}
        return {
            "n": len(vals),
            "mean": round(statistics.mean(vals), 4),
            "std": round(statistics.stdev(vals) if len(vals) > 1 else 0, 4),
            "median": round(statistics.median(vals), 4),
            "pos_pct": round(sum(1 for v in vals if v > 0) / len(vals) * 100, 1),
        }

    print("=== GLOBAL COMPARISON ===")
    cs = stats(compound_s2)
    bs = stats(baseline_s2)
    print(f"Compound second-elements: n={cs['n']}, mean S2={cs['mean']}, std={cs['std']}, pos%={cs['pos_pct']}")
    print(f"Baseline adjacent words:  n={bs['n']}, mean S2={bs['mean']}, std={bs['std']}, pos%={bs['pos_pct']}")
    delta = round(cs["mean"] - bs["mean"], 4)
    print(f"Delta (compound - baseline): {delta:+.4f} bits")

    # By poetry vs prose
    print("\n=== BY CATEGORY ===")
    for cat in ["poetry", "prose"]:
        c_vals = [e["s2"] for e in all_compound if e["category"] == cat]
        b_vals = [e["s2"] for e in all_baseline if e["category"] == cat]
        cs2 = stats(c_vals)
        bs2 = stats(b_vals)
        d = round(cs2["mean"] - bs2["mean"], 4)
        print(f"{cat}: compound mean={cs2['mean']} (n={cs2['n']}), baseline={bs2['mean']} (n={bs2['n']}), delta={d:+.4f}")

    # By word class
    print("\n=== COMPOUND SECOND-ELEMENTS BY WORD CLASS ===")
    for wc in ["ADJ", "NOUN", "VERB", "OTHER"]:
        vals = [e["s2"] for e in all_compound if e["word_class"] == wc]
        s = stats(vals)
        if s["n"] > 10:
            print(f"{wc}: n={s['n']}, mean={s['mean']}, std={s['std']}, pos%={s['pos_pct']}")

    # By era (compound mean vs baseline mean, for eras with enough compound events)
    print("\n=== BY ERA (compound mean S2 vs era baseline) ===")
    era_stats = []
    for era in era_compound:
        c_vals = era_compound[era]
        b_vals = era_baseline.get(era, [])
        if len(c_vals) < 5:
            continue
        cs3 = stats(c_vals)
        bs3 = stats(b_vals)
        d = round(cs3["mean"] - bs3["mean"], 4)
        era_stats.append((era, cs3["n"], cs3["mean"], bs3["mean"], d))
    era_stats.sort(key=lambda x: -x[4])  # sort by delta
    for era, n, cm, bm, d in era_stats:
        print(f"  {era:25s}: n={n:4d}, compound={cm:+.3f}, baseline={bm:+.3f}, delta={d:+.3f}")

    # Top notable compound moments
    print("\n=== TOP 20 HIGHEST-S2 COMPOUND MOMENTS ===")
    notable.sort(key=lambda x: -x["s2"])
    for item in notable[:20]:
        print(f"  S2={item['s2']:+.2f} | {item['compound']:30s} | suppressed: {item['suppressed_top1']:15s} | {item['title'][:30]} ({item['author'][:20]})")

    # High-S2 compound tokens
    high_compound = [e for e in all_compound if e["s2"] > 2.0]
    low_compound = [e for e in all_compound if e["s2"] < -2.0]
    print(f"\nHigh-S2 compound events (>2.0): {len(high_compound)} ({round(len(high_compound)/len(all_compound)*100,1)}%)")
    print(f"Low-S2 compound events (<-2.0): {len(low_compound)} ({round(len(low_compound)/len(all_compound)*100,1)}%)")

    # Save results
    results = {
        "global_compound": stats(compound_s2),
        "global_baseline": stats(baseline_s2),
        "delta_compound_minus_baseline": delta,
        "by_category": {
            cat: {
                "compound": stats([e["s2"] for e in all_compound if e["category"] == cat]),
                "baseline": stats([e["s2"] for e in all_baseline if e["category"] == cat]),
            }
            for cat in ["poetry", "prose"]
        },
        "by_word_class": {
            wc: stats([e["s2"] for e in all_compound if e["word_class"] == wc])
            for wc in ["ADJ", "NOUN", "VERB", "OTHER"]
        },
        "by_era": {
            era: {
                "compound": stats(era_compound[era]),
                "baseline": stats(era_baseline.get(era, [])),
            }
            for era in era_compound
            if len(era_compound[era]) >= 5
        },
        "top_compound_moments": notable[:20],
        "high_s2_fraction": round(len(high_compound) / len(all_compound), 4) if all_compound else 0,
        "low_s2_fraction": round(len(low_compound) / len(all_compound), 4) if all_compound else 0,
    }
    with open("results/compound_words_s2.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/compound_words_s2.json", file=sys.stderr)

if __name__ == "__main__":
    main()
