"""
Structural Position Immunity
==============================
Follow-up to second_occurrence_dip.md.

That study found: S2 drops massively from 1st to 2nd occurrence of a word
(mean swing of -2.31 units). It proposed that STRUCTURAL POSITION (line-start)
can override this habituation — but didn't test it directly.

This experiment tests: when BOTH occurrences of a word are at line-start
positions, does the second-occurrence dip disappear or shrink?

Hypothesis: The second-occurrence dip reflects lexical habituation (GPT-2
"remembers" seeing this word). But when the second occurrence is at a
line-start, GPT-2 strongly expects a newline, and the word takes its full
structural bonus. If line-start position provides enough "structural surprise"
to mask lexical familiarity, the dip should vanish for line-start → line-start
pairs.

Four comparison groups for word pairs (appear exactly twice):
  LL: 1st at line-start, 2nd at line-start
  LM: 1st at line-start, 2nd at mid-line
  ML: 1st at mid-line, 2nd at line-start
  MM: 1st at mid-line, 2nd at mid-line

If structural position overrides habituation:
  - MM: largest dip (no structural support)
  - LM: intermediate (1st has structural bonus, 2nd does not)
  - ML: intermediate (2nd has structural bonus despite habituation)
  - LL: smallest dip (both occurrences have structural support)
"""

import json
import re
import statistics
from collections import defaultdict


P_NEWLINE_THRESHOLD = 0.9   # artifact filter: skip if p_newline >= this
LINE_START_THRESHOLD = 0.5  # previous token's p_newline >= this → current is line-start


def normalize_token(tok: str) -> str:
    """Lowercase, strip leading space, strip punctuation."""
    t = tok.strip().lower()
    t = re.sub(r"[^a-z]", "", t)
    return t


def is_content_word(norm_tok: str) -> bool:
    """True if the token is a meaningful content word."""
    if len(norm_tok) < 3:
        return False
    stop = {
        "the", "and", "but", "not", "for", "you", "that", "this", "are",
        "was", "were", "has", "had", "have", "been", "being", "would",
        "could", "should", "will", "can", "may", "might", "shall", "did",
        "does", "from", "with", "into", "onto", "upon", "then", "than",
        "when", "where", "who", "which", "what", "how", "also", "just",
        "even", "yet", "still", "only", "ever", "never", "here", "there",
        "its", "our", "their", "his", "her", "him", "them", "these",
        "those", "some", "any", "all", "each", "both", "more", "most",
        "much", "many", "own", "she", "out", "off", "over",
    }
    return norm_tok not in stop


def classify_line_start(prev_p_newline: float) -> bool:
    """True if the current position is at a line start."""
    return prev_p_newline >= LINE_START_THRESHOLD


def analyze_poem(poem: dict) -> list[dict]:
    """
    For each word appearing exactly twice in the poem, return one record:
    {word, s2_1, s2_2, pos_1, pos_2, group (LL/LM/ML/MM), era, author, title}
    """
    tokens = poem.get("tokens", [])
    if not tokens:
        return []

    meta = poem.get("metadata", {})
    title = meta.get("title", "")
    author = meta.get("author", "")
    era = meta.get("era", "")

    # Build list of clean tokens with position and line-start flag
    clean_tokens = []
    for i, tok in enumerate(tokens):
        # Skip stanza-break artifacts
        if tok.get("p_newline", 0) >= P_NEWLINE_THRESHOLD:
            continue
        norm = normalize_token(tok.get("token", ""))
        if not is_content_word(norm):
            continue

        # Determine line-start: look at previous token (including artifacts)
        prev_p_nl = 0.0
        if i > 0:
            prev_p_nl = tokens[i - 1].get("p_newline", 0.0)

        clean_tokens.append({
            "norm": norm,
            "s2": tok["s2"],
            "pos": tok["position"],
            "is_line_start": classify_line_start(prev_p_nl),
            "prev_p_newline": prev_p_nl,
        })

    # Find words with exactly 2 occurrences
    word_positions = defaultdict(list)
    for ct in clean_tokens:
        word_positions[ct["norm"]].append(ct)

    records = []
    for word, occs in word_positions.items():
        if len(occs) != 2:
            continue
        occ1, occ2 = occs[0], occs[1]

        ls1 = occ1["is_line_start"]
        ls2 = occ2["is_line_start"]

        if ls1 and ls2:
            group = "LL"
        elif ls1 and not ls2:
            group = "LM"
        elif not ls1 and ls2:
            group = "ML"
        else:
            group = "MM"

        records.append({
            "word": word,
            "s2_1": occ1["s2"],
            "s2_2": occ2["s2"],
            "delta": occ2["s2"] - occ1["s2"],
            "group": group,
            "ls1": ls1,
            "ls2": ls2,
            "pos_1": occ1["pos"],
            "pos_2": occ2["pos"],
            "era": era,
            "author": author,
            "title": title,
        })
    return records


def run(corpus_path: str) -> dict:
    with open(corpus_path) as f:
        data = json.load(f)

    all_records = []
    for poem in data:
        all_records.extend(analyze_poem(poem))

    if not all_records:
        return {"error": "no records found"}

    # Group by LL/LM/ML/MM
    groups = defaultdict(list)
    for r in all_records:
        groups[r["group"]].append(r)

    summary = {}
    for grp in ["LL", "LM", "ML", "MM"]:
        recs = groups[grp]
        if not recs:
            summary[grp] = {"n": 0}
            continue
        deltas = [r["delta"] for r in recs]
        s2_1_vals = [r["s2_1"] for r in recs]
        s2_2_vals = [r["s2_2"] for r in recs]

        summary[grp] = {
            "n": len(recs),
            "mean_delta": round(statistics.mean(deltas), 4),
            "median_delta": round(statistics.median(deltas), 4),
            "mean_s2_1": round(statistics.mean(s2_1_vals), 4),
            "mean_s2_2": round(statistics.mean(s2_2_vals), 4),
            "pct_dip": round(100 * sum(1 for d in deltas if d < 0) / len(deltas), 1),
            "pct_rise": round(100 * sum(1 for d in deltas if d > 0) / len(deltas), 1),
        }

    # Era breakdown
    era_groups = defaultdict(lambda: defaultdict(list))
    for r in all_records:
        era_groups[r["era"]][r["group"]].append(r["delta"])

    era_summary = {}
    for era, era_grp in era_groups.items():
        # Only include eras with at least 10 LL and 10 MM records
        if len(era_grp.get("LL", [])) >= 5 and len(era_grp.get("MM", [])) >= 5:
            era_summary[era] = {
                grp: {
                    "n": len(deltas),
                    "mean_delta": round(statistics.mean(deltas), 4),
                }
                for grp, deltas in era_grp.items()
            }

    # Top examples: biggest absolute delta changes by group
    examples = {}
    for grp in ["LL", "MM"]:
        recs = sorted(groups[grp], key=lambda x: abs(x["delta"]), reverse=True)[:10]
        examples[grp] = [{
            "word": r["word"],
            "s2_1": round(r["s2_1"], 2),
            "s2_2": round(r["s2_2"], 2),
            "delta": round(r["delta"], 2),
            "title": r["title"],
            "author": r["author"],
        } for r in recs]

    # Also: examples of LL pairs where S2 stays high or RISES
    ll_rises = sorted(groups["LL"], key=lambda x: -x["delta"])[:15]
    mm_drops = sorted(groups["MM"], key=lambda x: x["delta"])[:15]

    return {
        "group_summary": summary,
        "era_summary": era_summary,
        "examples": examples,
        "ll_rises": [{
            "word": r["word"],
            "s2_1": round(r["s2_1"], 2),
            "s2_2": round(r["s2_2"], 2),
            "delta": round(r["delta"], 2),
            "title": r["title"],
            "author": r["author"],
        } for r in ll_rises],
        "mm_drops": [{
            "word": r["word"],
            "s2_1": round(r["s2_1"], 2),
            "s2_2": round(r["s2_2"], 2),
            "delta": round(r["delta"], 2),
            "title": r["title"],
            "author": r["author"],
        } for r in mm_drops],
        "total_pairs": len(all_records),
    }


def print_report(result: dict):
    print("=" * 60)
    print("STRUCTURAL POSITION IMMUNITY EXPERIMENT")
    print("=" * 60)
    print(f"\nTotal two-occurrence word pairs: {result['total_pairs']}")

    gs = result["group_summary"]
    print("\n--- GROUP SUMMARY ---")
    print(f"{'Group':<6} {'N':>6} {'S2_1':>7} {'S2_2':>7} {'Δ':>8} {'%dip':>7} {'%rise':>7}")
    print("-" * 50)
    for grp in ["LL", "LM", "ML", "MM"]:
        if gs[grp].get("n", 0) == 0:
            continue
        g = gs[grp]
        print(f"{grp:<6} {g['n']:>6} {g['mean_s2_1']:>7.3f} {g['mean_s2_2']:>7.3f} "
              f"{g['mean_delta']:>8.3f} {g['pct_dip']:>6.1f}% {g['pct_rise']:>6.1f}%")

    print("\n--- LL: LINE-START → LINE-START (top rises) ---")
    for r in result["ll_rises"][:10]:
        print(f"  '{r['word']}': {r['s2_1']:+.1f} → {r['s2_2']:+.1f} (Δ={r['delta']:+.1f})  "
              f"[{r['author']}: {r['title'][:40]}]")

    print("\n--- MM: MID-LINE → MID-LINE (worst drops) ---")
    for r in result["mm_drops"][:10]:
        print(f"  '{r['word']}': {r['s2_1']:+.1f} → {r['s2_2']:+.1f} (Δ={r['delta']:+.1f})  "
              f"[{r['author']}: {r['title'][:40]}]")

    if result["era_summary"]:
        print("\n--- ERA BREAKDOWN (LL vs MM delta, min 5 pairs each) ---")
        for era, grp_data in sorted(result["era_summary"].items()):
            ll_d = grp_data.get("LL", {}).get("mean_delta", None)
            mm_d = grp_data.get("MM", {}).get("mean_delta", None)
            if ll_d is not None and mm_d is not None:
                immunity = mm_d - ll_d
                print(f"  {era:<25s} LL δ={ll_d:+.3f}  MM δ={mm_d:+.3f}  "
                      f"immunity={immunity:+.3f}")


if __name__ == "__main__":
    import sys

    corpus = "results/corpus_results.json"
    out_path = "results/structural_position_immunity.json"

    print("Loading corpus…")
    result = run(corpus)

    print_report(result)

    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(f"\n[Saved {out_path}]")
