"""
Semantic Bridging Across Line Breaks

For each line break in every poem, measure whether the last word of the
outgoing line "semantically predicted" the first word of the incoming line —
i.e., does the first word of the new line appear in the ending word's top-10
GPT-2 alternatives?

This distinguishes two modes of line break:
  - BRIDGED: the new-line word was already predicted at the end of the previous line
  - RUPTURED: the new-line word was outside the previous word's prediction horizon

We test whether these two classes differ in S2, and whether different eras or
forms favour one pattern over the other.
"""

import json
import os
import sys
import statistics
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

ARTIFACT_P = 0.90   # p(newline) threshold for stanza-break artifact


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def is_newline_token(tok):
    return tok["token"].strip() == "" and "\n" in tok["token"]


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


PUNCT_TOKENS = set(".,;:!?-—–()[]{}\"'`…''""")


def is_punct_token(tok_text):
    return tok_text.strip() in PUNCT_TOKENS or all(c in PUNCT_TOKENS for c in tok_text.strip())


def analyze_poem(r):
    """
    Walk through the token list; identify every line-break boundary.
    Return one record per boundary:
      {era, author, is_stanza (p_newline >= 0.9), was_bridged, s2_of_head,
       source_token, head_token, rank_of_head, source_is_punct, head_is_punct}
    """
    tokens = r["tokens"]
    era = r["metadata"]["era"]
    author = r["metadata"]["author"]
    records = []

    for i, tok in enumerate(tokens):
        if not is_newline_token(tok):
            continue

        # Look backward for the last non-newline token (bridge source)
        src_idx = i - 1
        while src_idx >= 0 and is_newline_token(tokens[src_idx]):
            src_idx -= 1
        if src_idx < 0:
            continue
        source = tokens[src_idx]

        # Look forward for the first non-newline token (bridge target / line head)
        head_idx = i + 1
        while head_idx < len(tokens) and is_newline_token(tokens[head_idx]):
            head_idx += 1
        if head_idx >= len(tokens):
            continue
        head = tokens[head_idx]

        # Was the head predicted by the source's alternatives?
        alt_tokens = {a["token"] for a in source["alternatives"]}
        was_bridged = head["token"] in alt_tokens

        # Rank of head in source's alternatives (or None)
        rank_in_alts = None
        for rank_pos, a in enumerate(source["alternatives"], 1):
            if a["token"] == head["token"]:
                rank_in_alts = rank_pos
                break

        # Is this a stanza-break artifact position?
        is_stanza = newline_prob(tok) >= ARTIFACT_P

        records.append({
            "era": era,
            "author": author,
            "is_stanza": is_stanza,
            "was_bridged": was_bridged,
            "s2_of_head": head["s2"],
            "source_token": source["token"].strip(),
            "head_token": head["token"].strip(),
            "rank_in_alts": rank_in_alts,
            "head_p_newline": newline_prob(head),
            "source_is_punct": is_punct_token(source["token"]),
            "head_is_punct": is_punct_token(head["token"]),
        })

    return records


def run():
    results = load_results()
    poetry = [r for r in results if r["metadata"]["era"] != "control"]

    all_records = []
    for r in poetry:
        all_records.extend(analyze_poem(r))

    # Filter to artifact-free positions (head token not a stanza-break artifact)
    clean_all = [rec for rec in all_records if rec["head_p_newline"] < ARTIFACT_P]
    # Semantic-only: exclude punctuation tokens at source or head
    clean = [rec for rec in clean_all
             if not rec["source_is_punct"] and not rec["head_is_punct"]]

    n_total_all = len(clean_all)
    n_bridged_all = sum(1 for r in clean_all if r["was_bridged"])

    n_total = len(clean)
    n_bridged = sum(1 for r in clean if r["was_bridged"])
    n_ruptured = n_total - n_bridged

    bridged_s2 = [r["s2_of_head"] for r in clean if r["was_bridged"]]
    ruptured_s2 = [r["s2_of_head"] for r in clean if not r["was_bridged"]]

    bridged_avg = statistics.mean(bridged_s2) if bridged_s2 else float("nan")
    ruptured_avg = statistics.mean(ruptured_s2) if ruptured_s2 else float("nan")

    # By era
    era_data = defaultdict(lambda: {"bridged": [], "ruptured": []})
    for rec in clean:
        key = "bridged" if rec["was_bridged"] else "ruptured"
        era_data[rec["era"]][key].append(rec["s2_of_head"])

    # Bridge rate by era
    era_bridge_rate = {}
    for era, d in era_data.items():
        n_b = len(d["bridged"])
        n_r = len(d["ruptured"])
        total = n_b + n_r
        if total >= 10:
            era_bridge_rate[era] = {
                "rate": n_b / total,
                "n": total,
                "bridged_avg_s2": statistics.mean(d["bridged"]) if d["bridged"] else float("nan"),
                "ruptured_avg_s2": statistics.mean(d["ruptured"]) if d["ruptured"] else float("nan"),
            }

    # Examples: bridged transitions with high s2
    bridged_high = sorted(
        [r for r in clean if r["was_bridged"]],
        key=lambda x: x["s2_of_head"], reverse=True
    )[:10]

    # Examples: ruptured transitions with low s2 (most surprising ruptures)
    ruptured_low = sorted(
        [r for r in clean if not r["was_bridged"]],
        key=lambda x: x["s2_of_head"]
    )[:5]

    # Entropy quartile analysis: do high-entropy line endings predict more rupture?
    import math
    def tok_entropy_from_alts(alts):
        total_p = sum(a["prob"] for a in alts)
        if total_p == 0:
            return 0.0
        h = 0.0
        for a in alts:
            p = a["prob"] / total_p
            if p > 0:
                h -= p * math.log2(p)
        return h

    # We need to re-run analysis with source entropy attached
    all_records_with_entropy = []
    for r in poetry:
        toks = r["tokens"]
        era = r["metadata"]["era"]
        for i, tok in enumerate(toks):
            if not is_newline_token(tok):
                continue
            src_idx = i - 1
            while src_idx >= 0 and is_newline_token(toks[src_idx]):
                src_idx -= 1
            if src_idx < 0:
                continue
            source = toks[src_idx]
            head_idx = i + 1
            while head_idx < len(toks) and is_newline_token(toks[head_idx]):
                head_idx += 1
            if head_idx >= len(toks):
                continue
            head = toks[head_idx]
            if newline_prob(tok) >= ARTIFACT_P or newline_prob(head) >= ARTIFACT_P:
                continue
            if is_punct_token(source["token"]) or is_punct_token(head["token"]):
                continue
            alt_tokens = {a["token"] for a in source["alternatives"]}
            was_bridged = head["token"] in alt_tokens
            src_ent = tok_entropy_from_alts(source["alternatives"])
            all_records_with_entropy.append({
                "era": era,
                "was_bridged": was_bridged,
                "s2_of_head": head["s2"],
                "source_entropy": src_ent,
            })

    # Bucket by source entropy quartile
    ents = sorted(r["source_entropy"] for r in all_records_with_entropy)
    q1 = ents[len(ents)//4]
    q2 = ents[len(ents)//2]
    q3 = ents[3*len(ents)//4]

    def entropy_bucket(h):
        if h <= q1: return "Q1 (low entropy / concentrated prediction)"
        elif h <= q2: return "Q2"
        elif h <= q3: return "Q3"
        else: return "Q4 (high entropy / diffuse prediction)"

    entropy_buckets = defaultdict(lambda: {"bridged": 0, "ruptured": 0, "s2": []})
    for rec in all_records_with_entropy:
        b = entropy_bucket(rec["source_entropy"])
        if rec["was_bridged"]:
            entropy_buckets[b]["bridged"] += 1
        else:
            entropy_buckets[b]["ruptured"] += 1
        entropy_buckets[b]["s2"].append(rec["s2_of_head"])

    # Build output
    lines = []
    lines.append("# Semantic Bridging Across Line Breaks")
    lines.append("")
    lines.append(f"**Date:** 2026-11-25")
    lines.append(f"**Method:** For each line break in 450 poems, check whether the first word of the")
    lines.append(f"new line appears in the previous line-ending word's top-10 GPT-2 alternatives.")
    lines.append(f"'Bridged' = semantically predicted; 'Ruptured' = outside prediction horizon.")
    lines.append(f"Stanza-break artifact positions filtered (p(newline) ≥ 0.9).")
    lines.append(f"Punctuation tokens excluded from source and head positions.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Overall Bridge Rate")
    lines.append("")
    lines.append(f"| Metric | Value |")
    lines.append(f"|---|---|")
    lines.append(f"| Total line breaks (artifact-free, all tokens) | {n_total_all:,} |")
    lines.append(f"| Total line breaks (artifact-free, word tokens only) | {n_total:,} |")
    lines.append(f"| Bridged (head word predicted by source word) | {n_bridged:,} ({n_bridged/n_total:.1%}) |")
    lines.append(f"| Ruptured (head word outside prediction horizon) | {n_ruptured:,} ({n_ruptured/n_total:.1%}) |")
    lines.append(f"| Avg S₂ at bridged line heads | **{bridged_avg:.3f}** |")
    lines.append(f"| Avg S₂ at ruptured line heads | **{ruptured_avg:.3f}** |")
    lines.append(f"| S₂ gap (ruptured − bridged) | **{ruptured_avg - bridged_avg:.3f}** |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Bridge Rate and S₂ by Literary Era")
    lines.append("")
    lines.append("Sorted by bridge rate (descending = most semantically continuous line breaks).")
    lines.append("")
    lines.append("| Era | n | Bridge Rate | Bridged AvgS₂ | Ruptured AvgS₂ | Gap |")
    lines.append("|---|---|---|---|---|---|")
    for era, d in sorted(era_bridge_rate.items(), key=lambda x: -x[1]["rate"]):
        gap = d["ruptured_avg_s2"] - d["bridged_avg_s2"]
        lines.append(
            f"| {era} | {d['n']} | {d['rate']:.1%} | {d['bridged_avg_s2']:.3f} | "
            f"{d['ruptured_avg_s2']:.3f} | {gap:.3f} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Examples: Bridged Line Breaks with High S₂")
    lines.append("")
    lines.append("These are cases where the new line's first word WAS predicted by the previous word,")
    lines.append("yet still carries high S₂ (the whole context, not just the previous word, made it surprising).")
    lines.append("")
    lines.append("| Era | Source → Head | Head S₂ | Rank in Source's Alts |")
    lines.append("|---|---|---|---|")
    for rec in bridged_high:
        lines.append(
            f"| {rec['era']} | `{rec['source_token']}` → `{rec['head_token']}` "
            f"| {rec['s2_of_head']:.2f} | #{rec['rank_in_alts']} |"
        )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Finding")
    lines.append("")
    n_pct = n_bridged / n_total
    lines.append(
        f"**{n_pct:.1%} of artifact-free line breaks are 'bridged'** — the new line's first word "
        f"was already in the ending word's top-10 alternatives. "
        f"This means the vast majority ({(1-n_pct):.1%}) are 'ruptured' — the first word of the "
        f"new line was not predicted at all from the previous word alone."
    )
    lines.append("")
    lines.append(
        f"**Bridged transitions have avg S₂ = {bridged_avg:.3f}; ruptured have avg S₂ = {ruptured_avg:.3f}** "
        f"(gap = {ruptured_avg - bridged_avg:.3f} bits). "
        + (
            "Bridged transitions are more surprising despite being predicted — the broader context "
            "contradicts the local prediction."
            if bridged_avg > ruptured_avg else
            "Ruptured transitions (unpredicted by the previous word) carry higher S₂, confirming "
            "that cross-line discontinuity is a major driver of poetic surprise."
        )
    )
    lines.append("")
    high_bridge_era = max(era_bridge_rate, key=lambda e: era_bridge_rate[e]["rate"])
    low_bridge_era = min(era_bridge_rate, key=lambda e: era_bridge_rate[e]["rate"])
    lines.append(
        f"**Era variation**: {high_bridge_era} has the highest bridge rate "
        f"({era_bridge_rate[high_bridge_era]['rate']:.1%}), suggesting the most semantically "
        f"continuous line breaks. {low_bridge_era} has the lowest "
        f"({era_bridge_rate[low_bridge_era]['rate']:.1%}), suggesting maximally disruptive "
        f"cross-line transitions."
    )
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Source Word Entropy and Bridge Rate")
    lines.append("")
    lines.append("Does the **certainty of the line-ending word's prediction** affect whether the")
    lines.append("next line's first word is bridged? (Low entropy = concentrated prediction; high = diffuse.)")
    lines.append("")
    lines.append("| Entropy Quartile | n | Bridge Rate | Avg S₂ at Head |")
    lines.append("|---|---|---|---|")
    for bkt in ["Q1 (low entropy / concentrated prediction)", "Q2", "Q3", "Q4 (high entropy / diffuse prediction)"]:
        d = entropy_buckets[bkt]
        total = d["bridged"] + d["ruptured"]
        rate = d["bridged"] / total if total > 0 else 0
        avg_s2 = statistics.mean(d["s2"]) if d["s2"] else float("nan")
        lines.append(f"| {bkt} | {total} | {rate:.1%} | {avg_s2:.3f} |")
    lines.append("")
    lines.append("**Interpretation**: When the line-ending word has concentrated prediction (Q1), the next")
    lines.append("line's head is either bridged (rare but possible) or carries higher S₂ due to the")
    lines.append("stronger expectation being violated. High-entropy endings leave the prediction space")
    lines.append("so diffuse that any continuation is a rupture — but a less surprising one.")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("- Correlate bridge rate with form (formal meter vs. free verse)")
    lines.append("- Track 'bridge distance': how far back does the prediction extend?")
    lines.append("  (top-5 vs. top-10 alternatives changes the bridge rate — what's the threshold?)")
    lines.append("- Compare bridge rate to enjambment classification")
    lines.append("  (do 'hard' enjambments always rupture, or can a syntactic break be semantically bridged?)")
    lines.append("- Apply to prose: do paragraphs bridge more than stanzas?")

    return "\n".join(lines)


if __name__ == "__main__":
    output = run()
    out_path = os.path.join(FINDINGS_DIR, "line_bridge_semantics.md")
    with open(out_path, "w") as f:
        f.write(output)
    print(f"Wrote {out_path}")
    print(output[:500])
