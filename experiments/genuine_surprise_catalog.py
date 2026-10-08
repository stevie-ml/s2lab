"""
Genuine Surprise Catalog: Artifact-Free High-S2 Moments

Now that the stanza-break artifact is understood (the top-50 high-S2 moments
are 98% newline-expectation positions), this experiment asks:

    WHAT ARE THE GENUINE SURPRISE MOMENTS?

Method:
  1. Filter ALL tokens with p(newline) >= 0.9 (artifact positions)
  2. Also filter pure whitespace tokens
  3. From remaining "clean" tokens, find the top-200 highest-S2 moments
  4. For each: record author, era, context, chosen token, top-1 alternative
  5. Classify into categories:
     - LEXICAL: poet chose an unexpected content word
     - SYNTACTIC: poet used expected word class but in unexpected slot
     - PROPER_NOUN: named something specific (person, place, title)
     - PUNCTUATION_INNOVATION: unusual punctuation mid-sentence
     - REGISTER_SHIFT: sudden shift in register (archaic/slang/technical)
     - MORPHOLOGICAL: unusual word form, compound, or neologism
  6. Compute per-era and per-poet distributions
"""

import json
import os
import sys
import statistics
import re
from collections import defaultdict, Counter

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

ROOT = os.path.dirname(os.path.dirname(__file__))
RESULTS_FILE = os.path.join(ROOT, "results", "corpus_results.json")
OUT_JSON = os.path.join(ROOT, "results", "genuine_surprise_catalog.json")

ARTIFACT_P = 0.90   # p(newline) threshold for artifact removal
MIN_S2 = 3.0        # threshold for "high S2"
TOP_N = 200         # how many top moments to catalog in detail


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def is_artifact(tok):
    return newline_prob(tok) >= ARTIFACT_P


def is_whitespace(tok):
    return tok["token"].strip() == ""


def classify_token(token_str, alt_token_str, context_before):
    """Classify a high-S2 substitution by the CHOSEN token type."""
    t = token_str.strip()
    alt = alt_token_str.strip()

    # Morphological: hyphens, unusual compounds, diacritics, all-caps mid-word
    if ("-" in t and len(t) > 3) or ("'" in t and t not in ("'s", "'t", "'ll", "'re", "'ve", "'d", "'m")):
        return "MORPHOLOGICAL"
    if any(c in t for c in "—–"):
        return "PUNCTUATION_INNOVATION"
    if t and t[0].isupper() and len(t) > 1:
        # Check if it's likely a proper noun (capitalized non-sentence-initial)
        ctx = context_before.rstrip()
        if ctx and ctx[-1] not in ".!?:":
            return "PROPER_NOUN"

    # Punctuation innovation: unusual punctuation choices
    if all(c in '.,;:!?()[]{}—–…' for c in t) and t:
        return "PUNCTUATION_INNOVATION"

    # Function words as alternatives (model expected grammar, poet chose content)
    function_words = {"the", "a", "an", "of", "in", "to", "and", "or", "but",
                      "is", "was", "are", "were", "be", "been", "being",
                      "I", "he", "she", "it", "they", "we", "you",
                      "not", "no", "so", "for", "on", "at", "by", "as", "from",
                      "that", "this", "which", "who", "what", "how"}
    if alt.lower() in function_words:
        return "LEXICAL"  # model expected grammar, poet gave content

    # Register shift: archaic or unusual register markers
    archaic = {"thou", "thee", "thy", "thine", "hast", "hath", "doth", "dost",
               "wherefore", "whence", "hither", "thither", "yea", "nay",
               "betwixt", "ere", "naught", "methinks", "perchance"}
    if t.lower() in archaic:
        return "REGISTER_SHIFT"

    # Default: lexical substitution
    return "LEXICAL"


def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    # Step 1: collect all clean high-S2 tokens
    all_clean = []
    total_clean = 0
    total_artifact = 0
    total_whitespace = 0

    for entry in corpus:
        meta = entry["metadata"]
        toks = entry["tokens"]
        if not toks:
            continue

        for i, tok in enumerate(toks):
            if is_whitespace(tok):
                total_whitespace += 1
                continue
            if is_artifact(tok):
                total_artifact += 1
                continue
            total_clean += 1
            all_clean.append({
                "author": meta["author"],
                "title": meta["title"],
                "era": meta.get("era", ""),
                "s2": tok["s2"],
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "rank": tok["rank"],
                "token": tok["token"],
                "top1_alt": tok["alternatives"][0]["token"] if tok["alternatives"] else "",
                "top1_prob": tok["alternatives"][0]["prob"] if tok["alternatives"] else 0.0,
                "context_before": tok.get("context_before", ""),
                "p_newline": newline_prob(tok),
                "rel_pos": (i + 1) / len(toks),
            })

    print("=" * 76)
    print("GENUINE SURPRISE CATALOG: ARTIFACT-FREE HIGH-S2 ANALYSIS")
    print(f"Corpus: {len(corpus)} texts")
    print(f"  Whitespace tokens excluded : {total_whitespace:,}")
    print(f"  Artifact tokens excluded   : {total_artifact:,}")
    print(f"  Clean tokens remaining     : {total_clean:,}")
    print("=" * 76)

    # Step 2: overall S2 stats on clean tokens
    all_s2 = [t["s2"] for t in all_clean]
    print(f"\n--- CLEAN TOKEN S2 DISTRIBUTION ---")
    print(f"  Mean S2        : {statistics.mean(all_s2):.3f}")
    print(f"  Median S2      : {statistics.median(all_s2):.3f}")
    print(f"  Stdev          : {statistics.stdev(all_s2):.3f}")
    print(f"  % positive S2  : {sum(1 for s in all_s2 if s > 0) / len(all_s2):.1%}")
    print(f"  % S2 > 3       : {sum(1 for s in all_s2 if s > MIN_S2) / len(all_s2):.1%}")
    print(f"  % S2 > 5       : {sum(1 for s in all_s2 if s > 5) / len(all_s2):.1%}")

    # Step 3: top-200 highest clean S2 moments
    high_s2 = sorted(all_clean, key=lambda t: -t["s2"])[:TOP_N]

    print(f"\n--- TOP {TOP_N} ARTIFACT-FREE HIGH-S2 MOMENTS ---")
    print(f"Min S2 in top-{TOP_N}: {high_s2[-1]['s2']:.2f}")
    print(f"Max S2 in top-{TOP_N}: {high_s2[0]['s2']:.2f}")
    print()

    # Step 4: classify
    category_counts = Counter()
    for tok in high_s2:
        cat = classify_token(tok["token"], tok["top1_alt"], tok["context_before"])
        tok["category"] = cat
        category_counts[cat] += 1

    print(f"{'Category':<28}{'Count':>6}{'%':>6}  {'Mean S2':>9}")
    for cat, count in category_counts.most_common():
        cat_s2 = [t["s2"] for t in high_s2 if t.get("category") == cat]
        pct = count / TOP_N * 100
        print(f"{cat:<28}{count:>6}{pct:>5.1f}%  {statistics.mean(cat_s2):>9.2f}")

    # Step 5: what does GPT-2 expect at genuine surprise moments?
    print(f"\n--- WHAT GPT-2 EXPECTED AT TOP-{TOP_N} GENUINE SURPRISES ---")
    alt_counter = Counter(t["top1_alt"].strip() for t in high_s2)
    print("Top-15 suppressed alternatives:")
    for alt, cnt in alt_counter.most_common(15):
        repr_alt = repr(alt)
        pct = cnt / TOP_N * 100
        print(f"  {repr_alt:<20} {cnt:>3}× ({pct:.1f}%)")

    # Step 6: Show most striking examples
    print(f"\n--- MOST STRIKING GENUINE SURPRISES (S2 > 5, no artifact) ---")
    examples = [t for t in high_s2 if t["s2"] > 5][:30]
    for tok in examples:
        ctx = tok["context_before"][-35:] if tok["context_before"] else ""
        print(f"\n  [{tok['era']}] {tok['author']}, \"{tok['title']}\"")
        print(f"  Context: '...{ctx}' → chose '{tok['token'].strip()}'")
        print(f"  GPT-2 expected: '{tok['top1_alt'].strip()}' (p={tok['top1_prob']:.3f})")
        print(f"  S2={tok['s2']:.2f}  entropy={tok['entropy']:.2f}  rank={tok['rank']}")

    # Step 7: era breakdown of genuine high-S2 moments (clean tokens)
    print(f"\n--- ERA BREAKDOWN: ARTIFACT-FREE S2 ---")
    by_era = defaultdict(list)
    for tok in all_clean:
        by_era[tok["era"]].append(tok["s2"])

    era_rows = [
        (era, s2_list) for era, s2_list in by_era.items()
        if len(s2_list) >= 30
    ]
    era_rows.sort(key=lambda r: -statistics.mean(r[1]))

    print(f"{'Era':<24}{'n':>6}{'Mean S2':>10}{'%+S2':>8}{'%S2>3':>8}")
    for era, s2_list in era_rows:
        pct_pos = sum(1 for s in s2_list if s > 0) / len(s2_list)
        pct_high = sum(1 for s in s2_list if s > MIN_S2) / len(s2_list)
        print(f"{era:<24}{len(s2_list):>6}{statistics.mean(s2_list):>10.3f}"
              f"{pct_pos:>7.1%}{pct_high:>8.1%}")

    # Step 8: era share of top-200 high-S2 moments
    print(f"\n--- ERA SHARE OF TOP-{TOP_N} GENUINE SURPRISE MOMENTS ---")
    era_in_top = Counter(t["era"] for t in high_s2)
    # Normalize by era token count
    era_token_counts = {era: len(s2_list) for era, s2_list in by_era.items()}
    rows = []
    for era, cnt in era_in_top.most_common():
        total = era_token_counts.get(era, 1)
        rate = cnt / total * 100
        rows.append((era, cnt, total, rate))
    rows.sort(key=lambda r: -r[3])

    print(f"{'Era':<24}{'Top-200':>8}{'Tokens':>8}{'Rate%':>8}")
    for era, cnt, total, rate in rows:
        print(f"{era:<24}{cnt:>8}{total:>8}{rate:>8.2f}%")

    # Step 9: Stein vs Hopkins comparison (specific test cases)
    print(f"\n--- STEIN vs. HOPKINS vs. other VICTORIANS (artifact-free) ---")
    test_authors = {
        "Gerard Manley Hopkins": "Hopkins (sprung rhythm)",
        "Gertrude Stein": "Stein (semantic disruption)",
    }
    # Group all victorians for comparison
    victorian_s2 = [t["s2"] for t in all_clean if t["era"] == "victorian"
                    and "Hopkins" not in t["author"]]
    modernist_s2 = [t["s2"] for t in all_clean if t["era"] == "modernist"
                    and "Stein" not in t["author"]]

    print(f"\n{'Group':<34}{'n':>6}{'Mean S2':>10}{'%+S2':>8}{'%S2>3':>8}")

    for author, label in test_authors.items():
        s2_list = [t["s2"] for t in all_clean if author in t["author"]]
        if s2_list:
            pct_pos = sum(1 for s in s2_list if s > 0) / len(s2_list)
            pct_high = sum(1 for s in s2_list if s > MIN_S2) / len(s2_list)
            print(f"{label:<34}{len(s2_list):>6}{statistics.mean(s2_list):>10.3f}"
                  f"{pct_pos:>7.1%}{pct_high:>8.1%}")

    for label, s2_list in [("Victorian (excl. Hopkins)", victorian_s2),
                            ("Modernist (excl. Stein)", modernist_s2)]:
        if s2_list:
            pct_pos = sum(1 for s in s2_list if s > 0) / len(s2_list)
            pct_high = sum(1 for s in s2_list if s > MIN_S2) / len(s2_list)
            print(f"{label:<34}{len(s2_list):>6}{statistics.mean(s2_list):>10.3f}"
                  f"{pct_pos:>7.1%}{pct_high:>8.1%}")

    # Save
    out = {
        "corpus_size": len(corpus),
        "total_clean_tokens": total_clean,
        "total_artifact_tokens": total_artifact,
        "mean_s2_clean": round(statistics.mean(all_s2), 4),
        "pct_positive_s2": round(sum(1 for s in all_s2 if s > 0) / len(all_s2), 4),
        "pct_s2_above_3": round(sum(1 for s in all_s2 if s > MIN_S2) / len(all_s2), 4),
        "top_n": TOP_N,
        "category_distribution": dict(category_counts),
        "era_stats": [
            {
                "era": era,
                "n_clean_tokens": len(s2_list),
                "mean_s2": round(statistics.mean(s2_list), 4),
                "pct_positive": round(sum(1 for s in s2_list if s > 0) / len(s2_list), 4),
                "pct_above_3": round(sum(1 for s in s2_list if s > MIN_S2) / len(s2_list), 4),
            }
            for era, s2_list in era_rows
        ],
        "top_200_examples": [
            {
                "author": t["author"],
                "title": t["title"],
                "era": t["era"],
                "s2": t["s2"],
                "token": t["token"],
                "top1_alt": t["top1_alt"],
                "context_before": t["context_before"][-60:],
                "category": t.get("category", ""),
                "rank": t["rank"],
            }
            for t in high_s2
        ],
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved: {OUT_JSON}")


if __name__ == "__main__":
    main()
