"""
Context-Specification by Token Class: Does the TYPE of surprise affect what
comes next?

Hypothesis: after a genuine high-S2 token, the entropy at k=+1 should differ
depending on the CLASS of the surprising token:

  - Proper nouns (entities): "name" a specific thing → model can now track
    that entity → entropy FALLS (context has been specified)
  - Verbs (actions): open up many potential objects/complements → entropy
    stays high or rises
  - Adjectives/adverbs: modify an upcoming noun → entropy depends on whether
    the modified noun is now constrained
  - Function words: short words that close off phrases → entropy can go either way
  - Punctuation surprises: may signal structural disruption → distinctive pattern

This follows spike_symmetry_profile.md suggestion #2: "Context-specification
by token class: do proper nouns specifically show a larger post-spike entropy
drop than other high-S2 token classes?"

Method:
  1. Load corpus_results.json
  2. For each genuine high-S2 spike (s2 >= 3.0, p_newline < 0.9):
     a. Extract the token text and its entropy
     b. Classify the token into a class using heuristics
     c. Record entropy at k-1 and k+1 (excluding artifact tokens)
  3. Compare entropy delta (k+1 - k-1) across token classes
  4. Also compare across eras
"""

import json
import math
import re
import string
from collections import defaultdict

SPIKE_THRESH   = 3.0
ARTIFACT_THRESH = 0.9
RESULTS_PATH   = "results/corpus_results.json"

# ── Common English function words ──────────────────────────────────────────────
FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "nor", "so", "yet",
    "is", "are", "was", "were", "be", "been", "being", "am",
    "have", "has", "had", "do", "does", "did",
    "in", "on", "at", "to", "for", "with", "by", "from", "of",
    "that", "which", "who", "whom", "whose",
    "it", "its", "this", "these", "those",
    "he", "she", "they", "we", "i", "you", "me", "him", "her", "us", "them",
    "not", "no", "nor",
    "if", "as", "when", "while", "although", "though", "because", "since",
}

# Words that clearly indicate verb or adjective usage
COMMON_VERB_PREFIXES = {"un", "re", "pre", "over", "under", "dis", "mis"}


def classify_token(token_str: str, prev_token_str: str | None) -> str:
    """
    Classify a GPT-2 token into a broad category.

    GPT-2 encodes leading whitespace: ' dog' is a word-initial 'dog'.
    Strategy:
      - Strip leading space to get the clean surface form
      - Use capitalization, punctuation, and common word lists
    """
    clean = token_str.lstrip()

    if not clean:
        return "WHITESPACE"

    # Punctuation-only tokens
    if all(c in string.punctuation for c in clean):
        return "PUNCTUATION"

    # Numeric tokens
    if re.match(r"^[\d.,%-]+$", clean):
        return "NUMERIC"

    # All-caps (shouting, acronyms, emphatic)
    if clean.isupper() and len(clean) > 1 and clean.isalpha():
        return "ALL_CAPS"

    # Lowercase function words
    if clean.lower() in FUNCTION_WORDS:
        return "FUNCTION"

    # Short alphabetic tokens (likely function words or particles, ≤ 3 chars)
    if clean.isalpha() and len(clean) <= 3 and clean[0].islower():
        return "SHORT_ALPHA"

    # Capitalized mid-sentence (likely proper noun)
    # If the token has a leading space (word-initial) AND starts with uppercase,
    # and the previous token is not purely whitespace/newline/sentence-final punctuation,
    # it's a strong proper noun signal.
    if clean[0].isupper():
        prev_clean = (prev_token_str or "").lstrip()
        prev_is_sentence_end = (
            prev_clean in {".", "!", "?", ""}
            or prev_token_str in {"", "\n", " \n"}
            or (prev_token_str or "").strip() in {".", "!", "?"}
        )
        if not prev_is_sentence_end:
            return "PROPER_NOUN"
        else:
            return "SENTENCE_START"

    # Lowercase longer alpha: content word
    if clean.isalpha():
        return "CONTENT_LOWER"

    # Mixed alphanumeric
    return "OTHER"


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")

def median(xs):
    if not xs:
        return float("nan")
    s = sorted(xs)
    n = len(s)
    return s[n // 2] if n % 2 == 1 else (s[n // 2 - 1] + s[n // 2]) / 2


def analyze():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Per-class: list of (entropy_k_minus1, entropy_k_plus1, entropy_delta, s2, era)
    class_data: dict[str, list[dict]] = defaultdict(list)
    era_class_data: dict[str, dict[str, list[float]]] = defaultdict(lambda: defaultdict(list))

    # Also track top-alternative class at spike positions
    top_alt_class_data: dict[str, list[float]] = defaultdict(list)  # class → entropy deltas

    total_spikes = 0
    skipped_no_neighbor = 0

    for poem in data:
        tokens  = poem["tokens"]
        era     = poem["metadata"]["era"]
        tok_map = {t["position"]: t for t in tokens}
        max_pos = max(t["position"] for t in tokens) if tokens else 0

        for i, t in enumerate(tokens):
            if t["s2"] < SPIKE_THRESH:
                continue
            if t.get("p_newline", 0) >= ARTIFACT_THRESH:
                continue

            pos = t["position"]

            # Find nearest non-artifact tokens before and after
            # k-1: search backward
            k_minus1 = None
            for offset in range(1, 6):
                prev = tok_map.get(pos - offset)
                if prev is not None and prev.get("p_newline", 0) < ARTIFACT_THRESH:
                    k_minus1 = prev
                    break

            # k+1: search forward
            k_plus1 = None
            for offset in range(1, 6):
                nxt = tok_map.get(pos + offset)
                if nxt is not None and nxt.get("p_newline", 0) < ARTIFACT_THRESH:
                    k_plus1 = nxt
                    break

            if k_minus1 is None or k_plus1 is None:
                skipped_no_neighbor += 1
                continue

            total_spikes += 1

            prev_tok_str = (tok_map.get(pos - 1) or {}).get("token", "")
            cls = classify_token(t["token"], prev_tok_str)

            h_pre  = k_minus1["entropy"]
            h_post = k_plus1["entropy"]
            delta  = h_post - h_pre   # negative = entropy dropped after spike

            class_data[cls].append({
                "delta": delta,
                "h_pre": h_pre,
                "h_post": h_post,
                "s2": t["s2"],
                "era": era,
                "token": t["token"],
            })
            era_class_data[era][cls].append(delta)

            # What was GPT-2's top alternative?
            alts = t.get("alternatives", [])
            if alts:
                top_alt_token = alts[0]["token"]
                top_alt_cls = classify_token(top_alt_token, prev_tok_str)
                top_alt_class_data[top_alt_cls].append(delta)

    # ── Report ────────────────────────────────────────────────────────────────
    print(f"\n{'='*70}")
    print("CONTEXT-SPECIFICATION BY TOKEN CLASS")
    print(f"Total genuine spikes: {total_spikes}")
    print(f"Skipped (no clean neighbor): {skipped_no_neighbor}")
    print(f"{'='*70}\n")

    # Overall by token class
    print("## Entropy Delta (k+1 − k−1) by Spike Token Class")
    print("Negative = entropy DROPS after spike (context specified)")
    print("Positive = entropy RISES after spike (new uncertainty opened)")
    print()
    print(f"{'Class':<18} {'n':>5} {'Avg delta':>10} {'Median':>10} {'Avg h_pre':>10} {'Avg h_post':>10}")
    print("-" * 65)

    rows = []
    for cls, items in class_data.items():
        deltas = [x["delta"] for x in items]
        h_pres  = [x["h_pre"] for x in items]
        h_posts = [x["h_post"] for x in items]
        rows.append((cls, len(items), mean(deltas), median(deltas),
                     mean(h_pres), mean(h_posts)))

    rows.sort(key=lambda r: r[2])  # sort by avg delta (most negative first)
    for cls, n, avg_d, med_d, avg_pre, avg_post in rows:
        print(f"{cls:<18} {n:>5} {avg_d:>10.3f} {med_d:>10.3f} {avg_pre:>10.3f} {avg_post:>10.3f}")

    # Aggregate meaningful categories
    print()
    print("## Simplified 3-Class Summary")
    # Proper nouns vs content words vs function/punct
    groups = {
        "PROPER_NOUN": [],
        "CONTENT (CONTENT_LOWER + SENTENCE_START)": [],
        "FUNCTION/SHORT": [],
        "PUNCTUATION": [],
    }
    for cls, items in class_data.items():
        deltas = [x["delta"] for x in items]
        if cls == "PROPER_NOUN":
            groups["PROPER_NOUN"].extend(deltas)
        elif cls in ("CONTENT_LOWER",):
            groups["CONTENT (CONTENT_LOWER + SENTENCE_START)"].extend(deltas)
        elif cls in ("FUNCTION", "SHORT_ALPHA"):
            groups["FUNCTION/SHORT"].extend(deltas)
        elif cls == "PUNCTUATION":
            groups["PUNCTUATION"].extend(deltas)

    print(f"{'Group':<44} {'n':>5} {'Avg delta':>10} {'Std':>10}")
    print("-" * 75)
    import statistics
    for grp, deltas in sorted(groups.items(), key=lambda x: mean(x[1])):
        if not deltas:
            continue
        std = statistics.stdev(deltas) if len(deltas) > 1 else 0.0
        print(f"{grp:<44} {len(deltas):>5} {mean(deltas):>10.3f} {std:>10.3f}")

    # Per-era, which classes dominate?
    print()
    print("## Era-Level: % of Spikes by Token Class (Top 4 Eras)")

    era_totals = {
        era: sum(len(v) for v in cls_dict.values())
        for era, cls_dict in era_class_data.items()
    }
    top_eras = sorted(era_totals, key=era_totals.get, reverse=True)[:4]

    for era in top_eras:
        cls_dict = era_class_data[era]
        total = era_totals[era]
        print(f"\n  Era: {era} (n_spikes={total})")
        print(f"  {'Class':<20} {'n':>4} {'%':>6} {'Avg delta':>10}")
        cls_rows = []
        for cls, ds in cls_dict.items():
            cls_rows.append((cls, len(ds), 100*len(ds)/total, mean(ds)))
        cls_rows.sort(key=lambda r: -r[1])
        for cls, n, pct, avg_d in cls_rows[:6]:
            print(f"  {cls:<20} {n:>4} {pct:>6.1f}% {avg_d:>10.3f}")

    # Top examples of PROPER_NOUN spikes with large entropy drops
    print()
    print("## Top PROPER_NOUN Spikes: Largest Entropy Drop (k+1 - k-1)")
    proper_items = sorted(class_data["PROPER_NOUN"], key=lambda x: x["delta"])[:20]
    print(f"{'Token':<20} {'Era':<20} {'S2':>6} {'H_pre':>7} {'H_post':>7} {'Delta':>7}")
    print("-" * 75)
    for item in proper_items:
        print(f"{item['token']:<20} {item['era']:<20} {item['s2']:>6.2f} {item['h_pre']:>7.2f} {item['h_post']:>7.2f} {item['delta']:>7.2f}")

    # Top examples of CONTENT_LOWER spikes with large entropy drops
    print()
    print("## Top CONTENT_LOWER Spikes: Largest Entropy Drop")
    content_items = sorted(class_data.get("CONTENT_LOWER", []), key=lambda x: x["delta"])[:10]
    print(f"{'Token':<20} {'Era':<20} {'S2':>6} {'H_pre':>7} {'H_post':>7} {'Delta':>7}")
    print("-" * 75)
    for item in content_items:
        print(f"{item['token']:<20} {item['era']:<20} {item['s2']:>6.2f} {item['h_pre']:>7.2f} {item['h_post']:>7.2f} {item['delta']:>7.2f}")

    # Top-alternative class: does it matter what GPT-2 predicted?
    print()
    print("## When GPT-2's Top Alternative Was... (entropy delta of actual choice)")
    print("Does what the model EXPECTED affect how much the deviation 'opens up' the future?")
    print(f"{'Top alt class':<22} {'n':>5} {'Avg delta':>10}")
    print("-" * 45)
    alt_rows = [(cls, ds) for cls, ds in top_alt_class_data.items() if ds]
    alt_rows.sort(key=lambda r: mean(r[1]))
    for cls, ds in alt_rows:
        print(f"{cls:<22} {len(ds):>5} {mean(ds):>10.3f}")

    # Summary for findings writeup
    print()
    print("## Summary Statistics for Findings Writeup")
    all_deltas = [x["delta"] for items in class_data.values() for x in items]
    pn_deltas = [x["delta"] for x in class_data.get("PROPER_NOUN", [])]
    cl_deltas = [x["delta"] for x in class_data.get("CONTENT_LOWER", [])]
    fn_deltas = [x["delta"] for x in class_data.get("FUNCTION", [])]
    punct_deltas = [x["delta"] for x in class_data.get("PUNCTUATION", [])]
    print(f"Global avg delta:        {mean(all_deltas):.3f}")
    print(f"Proper noun avg delta:   {mean(pn_deltas):.3f} (n={len(pn_deltas)})")
    print(f"Content lower avg delta: {mean(cl_deltas):.3f} (n={len(cl_deltas)})")
    print(f"Function word avg delta: {mean(fn_deltas):.3f} (n={len(fn_deltas)})")
    print(f"Punctuation avg delta:   {mean(punct_deltas):.3f} (n={len(punct_deltas)})")

    return {
        "class_summary": {
            cls: {
                "n": len(items),
                "avg_delta": mean([x["delta"] for x in items]),
                "avg_h_pre": mean([x["h_pre"] for x in items]),
                "avg_h_post": mean([x["h_post"] for x in items]),
            }
            for cls, items in class_data.items()
        }
    }


if __name__ == "__main__":
    import sys
    import os
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    analyze()
