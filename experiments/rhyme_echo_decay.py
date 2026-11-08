"""
Rhyme Echo Decay

Research question: Within a poem, does the S2 of a rhyme-slot word decrease
on its SECOND (echo) occurrence compared to its FIRST (lead) occurrence?

Background: When GPT-2 reads a poem that has already established a rhyme scheme,
the model's context window includes the earlier rhyme-slot words. If GPT-2 begins
to anticipate phonetically similar words at subsequent line endings, the echo-word
should be LESS surprising (lower S2) than the lead-word.

This is the 'rhyme habituation' hypothesis: the model partially learns the phonetic
pattern as it reads, reducing the surprisal of the second rhyme occurrence.

If true, rhyme echo decay implies that the full S2 'cost' of rhyme is paid at the
lead position, while the echo position gets a 'rhyme discount' — the reader (and
the model) has been primed to expect a rhyme sound.

Method:
1. Load corpus_results.json
2. For each poem, identify line-final tokens (last alphabetic word before newline)
3. Within a sliding 12-line window, find pairs of line endings that share the
   last 3 characters (rhyme suffix match)
4. For each rhyme pair, record S2 of lead and echo positions
5. Compute lead_s2 - echo_s2 (positive = decay, negative = inverse)
6. Stratify by: era, poem-level S2, rhyme density, distance between lead/echo

Hypothesis: lead_s2 > echo_s2 on average (decay is positive)
"""

import json
import re
from collections import defaultdict
import math

CORPUS_PATH = "results/corpus_results.json"
RESULTS_PATH = "results/rhyme_echo_decay.json"
WINDOW_LINES = 10   # lines within which to look for rhyme pairs
MIN_SUFFIX = 3      # minimum suffix length for rhyme match

def load_corpus():
    with open(CORPUS_PATH) as f:
        return json.load(f)

def is_alphabetic_word(token):
    clean = token.strip()
    return bool(re.match(r"^[a-zA-Z']+$", clean)) and len(clean) >= 2

def get_line_finals(tokens):
    """
    Return list of (position_index, token_str, s2, p_newline) for line-final tokens.
    A token is line-final if the next token contains a newline.
    """
    result = []
    for i in range(len(tokens) - 1):
        tok = tokens[i]
        next_tok = tokens[i + 1]
        is_before_newline = ("\n" in next_tok["token"])
        if is_before_newline and is_alphabetic_word(tok["token"]):
            # Skip stanza-break artifact positions (high p_newline means model expected newline)
            if tok.get("p_newline", 0.0) < 0.9:
                result.append({
                    "pos": i,
                    "token": tok["token"].strip().lower(),
                    "s2": tok["s2"],
                    "p_newline": tok.get("p_newline", 0.0),
                })
    return result

def rhymes(word1, word2, suffix_len=MIN_SUFFIX):
    """True if two words share the last suffix_len characters (case-insensitive)."""
    w1 = word1.strip().lower()
    w2 = word2.strip().lower()
    if w1 == w2:
        return False   # Identical words don't count as rhyme pair
    if len(w1) < suffix_len or len(w2) < suffix_len:
        return False
    return w1[-suffix_len:] == w2[-suffix_len:]

def find_rhyme_pairs(line_finals, window=WINDOW_LINES):
    """
    Find (lead, echo) pairs within a sliding window.
    Returns list of dicts with lead/echo info.
    """
    pairs = []
    n = len(line_finals)
    for i in range(n):
        for j in range(i + 1, min(i + window + 1, n)):
            if rhymes(line_finals[i]["token"], line_finals[j]["token"]):
                distance = j - i   # lines between lead and echo
                pairs.append({
                    "lead_token":  line_finals[i]["token"],
                    "echo_token":  line_finals[j]["token"],
                    "lead_s2":     line_finals[i]["s2"],
                    "echo_s2":     line_finals[j]["s2"],
                    "decay":       line_finals[i]["s2"] - line_finals[j]["s2"],
                    "distance":    distance,
                    "lead_pos":    line_finals[i]["pos"],
                    "echo_pos":    line_finals[j]["pos"],
                })
    return pairs

def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)

def main():
    print("Loading corpus...")
    corpus = load_corpus()
    print(f"  {len(corpus)} poems loaded.")

    all_pairs = []
    era_pairs = defaultdict(list)
    poem_stats = []

    for poem in corpus:
        tokens = poem.get("tokens", [])
        if len(tokens) < 10:
            continue

        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        title = meta.get("title", "")
        author = meta.get("author", "")
        avg_s2 = poem.get("summary", {}).get("avg_s2", 0.0)

        line_finals = get_line_finals(tokens)
        if len(line_finals) < 4:
            continue

        pairs = find_rhyme_pairs(line_finals)
        if not pairs:
            continue

        for p in pairs:
            p["era"] = era
            p["title"] = title
            p["author"] = author

        all_pairs.extend(pairs)
        era_pairs[era].extend(pairs)

        poem_stats.append({
            "title": title,
            "author": author,
            "era": era,
            "avg_s2": avg_s2,
            "n_line_finals": len(line_finals),
            "n_pairs": len(pairs),
            "mean_decay": sum(p["decay"] for p in pairs) / len(pairs),
            "pct_positive_decay": sum(1 for p in pairs if p["decay"] > 0) / len(pairs) * 100,
        })

    print(f"\n  Total rhyme pairs found: {len(all_pairs)}")
    print(f"  Poems with rhyme pairs:  {len(poem_stats)}")

    if not all_pairs:
        print("No rhyme pairs found.")
        return {}

    # --- Global summary ---
    n = len(all_pairs)
    mean_lead = sum(p["lead_s2"] for p in all_pairs) / n
    mean_echo = sum(p["echo_s2"] for p in all_pairs) / n
    mean_decay = sum(p["decay"] for p in all_pairs) / n
    pct_pos_decay = sum(1 for p in all_pairs if p["decay"] > 0) / n * 100

    print(f"\n=== GLOBAL RHYME ECHO DECAY ===")
    print(f"  Lead position mean S2:   {mean_lead:+.4f}")
    print(f"  Echo position mean S2:   {mean_echo:+.4f}")
    print(f"  Mean decay (lead-echo):  {mean_decay:+.4f}")
    print(f"  % pairs with decay > 0:  {pct_pos_decay:.1f}%")

    # --- By distance ---
    print(f"\n=== DECAY BY LINE DISTANCE (lead to echo) ===")
    print(f"{'Distance':>10} {'N':>6} {'Lead S2':>10} {'Echo S2':>10} {'Decay':>10} {'%Pos':>8}")
    print("-" * 60)
    for dist in sorted(set(p["distance"] for p in all_pairs)):
        subset = [p for p in all_pairs if p["distance"] == dist]
        if len(subset) < 5:
            continue
        ml = sum(p["lead_s2"] for p in subset) / len(subset)
        me = sum(p["echo_s2"] for p in subset) / len(subset)
        md = sum(p["decay"] for p in subset) / len(subset)
        pp = sum(1 for p in subset if p["decay"] > 0) / len(subset) * 100
        print(f"{dist:>10} {len(subset):>6} {ml:>+10.3f} {me:>+10.3f} {md:>+10.3f} {pp:>7.1f}%")

    # --- By era ---
    print(f"\n=== DECAY BY ERA ===")
    print(f"{'Era':<30} {'N pairs':>8} {'Lead S2':>10} {'Echo S2':>10} {'Decay':>10} {'%Pos':>8}")
    print("-" * 76)
    era_summary = []
    for era, pairs in era_pairs.items():
        if len(pairs) < 5:
            continue
        ml = sum(p["lead_s2"] for p in pairs) / len(pairs)
        me = sum(p["echo_s2"] for p in pairs) / len(pairs)
        md = sum(p["decay"] for p in pairs) / len(pairs)
        pp = sum(1 for p in pairs if p["decay"] > 0) / len(pairs) * 100
        era_summary.append((era, len(pairs), ml, me, md, pp))

    era_summary.sort(key=lambda x: -x[4])  # sort by mean decay
    for era, np, ml, me, md, pp in era_summary:
        print(f"{era:<30} {np:>8} {ml:>+10.3f} {me:>+10.3f} {md:>+10.3f} {pp:>7.1f}%")

    # --- By lead S2 level ---
    print(f"\n=== DECAY CONDITIONED ON LEAD S2 LEVEL ===")
    print(f"{'Lead S2 tier':<20} {'N':>6} {'Echo S2':>10} {'Decay':>10}")
    print("-" * 50)
    tiers = [
        ("very_low (<-4)",  -99, -4),
        ("low (-4 to -1)", -4, -1),
        ("neutral (-1 to 1)", -1, 1),
        ("moderate (1-4)", 1, 4),
        ("high (4-8)", 4, 8),
        ("very_high (>8)", 8, 99),
    ]
    for label, lo, hi in tiers:
        subset = [p for p in all_pairs if lo <= p["lead_s2"] < hi]
        if len(subset) < 5:
            continue
        me = sum(p["echo_s2"] for p in subset) / len(subset)
        md = sum(p["decay"] for p in subset) / len(subset)
        print(f"{label:<20} {len(subset):>6} {me:>+10.3f} {md:>+10.3f}")

    # --- Correlation: distance vs decay ---
    if len(all_pairs) > 20:
        dists = [p["distance"] for p in all_pairs]
        decays = [p["decay"] for p in all_pairs]
        r = pearson_r(dists, decays)
        print(f"\n  Correlation (distance vs decay): r = {r:.4f}")

    # --- Top examples of strongest echo decay (high lead, low echo) ---
    strong_decay = [p for p in all_pairs if p["lead_s2"] > 2.0 and p["decay"] > 2.0]
    strong_decay.sort(key=lambda x: -x["decay"])

    print(f"\n=== TOP RHYME PAIRS WITH STRONG ECHO DECAY ===")
    print(f"(Lead S2 > 2.0, Decay > 2.0 — model surprised by lead, primed for echo)")
    print(f"{'Lead word':<15} {'Echo word':<15} {'Lead S2':>8} {'Echo S2':>8} {'Decay':>8} {'Dist':>5} {'Author'}")
    print("-" * 85)
    seen = set()
    count = 0
    for p in strong_decay:
        key = (p["lead_token"], p["echo_token"])
        if key not in seen:
            seen.add(key)
            author_short = p["author"][:20]
            print(f"{p['lead_token']:<15} {p['echo_token']:<15} {p['lead_s2']:>+8.2f} {p['echo_s2']:>+8.2f} {p['decay']:>+8.2f} {p['distance']:>5}  {author_short}")
            count += 1
            if count >= 20:
                break

    # --- Inverse decay examples (echo MORE surprising than lead) ---
    inverse_decay = [p for p in all_pairs if p["lead_s2"] > 0 and p["decay"] < -2.0]
    inverse_decay.sort(key=lambda x: x["decay"])

    print(f"\n=== TOP INVERSE DECAY (echo MORE surprising than lead) ===")
    print(f"(Lead S2 > 0, Decay < -2.0 — anticipation followed by greater surprise)")
    print(f"{'Lead word':<15} {'Echo word':<15} {'Lead S2':>8} {'Echo S2':>8} {'Decay':>8} {'Dist':>5} {'Author'}")
    print("-" * 85)
    seen2 = set()
    count2 = 0
    for p in inverse_decay:
        key = (p["lead_token"], p["echo_token"])
        if key not in seen2:
            seen2.add(key)
            author_short = p["author"][:20]
            print(f"{p['lead_token']:<15} {p['echo_token']:<15} {p['lead_s2']:>+8.2f} {p['echo_s2']:>+8.2f} {p['decay']:>+8.2f} {p['distance']:>5}  {author_short}")
            count2 += 1
            if count2 >= 15:
                break

    # --- Per-poem stats for top poets ---
    poem_stats.sort(key=lambda x: -x["mean_decay"])

    print(f"\n=== POEMS WITH STRONGEST RHYME ECHO DECAY ===")
    print(f"{'Title':<40} {'Author':<20} {'Pairs':>6} {'Decay':>8} {'%Pos':>7}")
    print("-" * 90)
    for stat in poem_stats[:15]:
        title_s = stat["title"][:38]
        author_s = stat["author"][:18]
        print(f"{title_s:<40} {author_s:<20} {stat['n_pairs']:>6} {stat['mean_decay']:>+8.3f} {stat['pct_positive_decay']:>6.1f}%")

    # --- Null hypothesis check: shuffled control ---
    # Shuffle echo positions within each poem to get a null distribution
    import random
    random.seed(42)
    shuffled_decays = []
    for poem_pair_list in [list(v) for v in era_pairs.values()]:
        leads = [p["lead_s2"] for p in poem_pair_list]
        echoes = [p["echo_s2"] for p in poem_pair_list]
        random.shuffle(echoes)
        shuffled_decays.extend(l - e for l, e in zip(leads, echoes))

    if shuffled_decays:
        null_mean = sum(shuffled_decays) / len(shuffled_decays)
        print(f"\n=== NULL HYPOTHESIS CHECK ===")
        print(f"  Observed mean decay: {mean_decay:+.4f}")
        print(f"  Null (shuffled) decay: {null_mean:+.4f}")
        print(f"  Difference: {mean_decay - null_mean:+.4f}")
        if mean_decay > null_mean:
            print(f"  → Observed decay EXCEEDS null — rhyme position is predictive of S2 reduction")
        else:
            print(f"  → Observed decay at or below null — no systematic rhyme habituation effect")

    # Save results
    results = {
        "n_poems_with_pairs": len(poem_stats),
        "n_total_pairs": len(all_pairs),
        "global_mean_lead_s2": round(mean_lead, 4),
        "global_mean_echo_s2": round(mean_echo, 4),
        "global_mean_decay": round(mean_decay, 4),
        "pct_positive_decay": round(pct_pos_decay, 2),
        "null_mean_decay": round(null_mean, 4) if shuffled_decays else None,
        "distance_vs_decay_r": round(pearson_r(
            [p["distance"] for p in all_pairs],
            [p["decay"] for p in all_pairs]
        ), 4),
        "era_summary": [
            {"era": era, "n_pairs": np, "mean_lead": round(ml,4), "mean_echo": round(me,4),
             "mean_decay": round(md,4), "pct_positive_decay": round(pp,2)}
            for era, np, ml, me, md, pp in era_summary
        ],
        "lead_s2_tier_decay": {},
        "top_decay_examples": [
            {"lead": p["lead_token"], "echo": p["echo_token"],
             "lead_s2": p["lead_s2"], "echo_s2": p["echo_s2"],
             "decay": p["decay"], "distance": p["distance"],
             "author": p["author"], "title": p["title"]}
            for p in strong_decay[:20]
        ],
        "top_inverse_examples": [
            {"lead": p["lead_token"], "echo": p["echo_token"],
             "lead_s2": p["lead_s2"], "echo_s2": p["echo_s2"],
             "decay": p["decay"], "distance": p["distance"],
             "author": p["author"], "title": p["title"]}
            for p in inverse_decay[:15]
        ],
    }

    # Populate tier decay
    for label, lo, hi in tiers:
        subset = [p for p in all_pairs if lo <= p["lead_s2"] < hi]
        if subset:
            results["lead_s2_tier_decay"][label] = {
                "n": len(subset),
                "mean_echo_s2": round(sum(p["echo_s2"] for p in subset) / len(subset), 4),
                "mean_decay": round(sum(p["decay"] for p in subset) / len(subset), 4),
            }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")
    return results

if __name__ == "__main__":
    main()
