"""
Structural vs Lexical S2 Decomposition

Decomposes each poem's S2 signal into:
  - Structural S2: contributions from line-break/punctuation tokens
  - Lexical S2: contributions from genuine word choices

Tokens are classified:
  - Structural: pure newlines (\n), punctuation-only tokens, or p_newline > 0.85
    (model was highly confident a newline was coming, so the token is "form-driven")
  - Lexical: all other tokens

This extends the stanza-break artifact finding into a full decomposition.
"""

import json
import os
import re
from collections import defaultdict

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
FINDINGS_PATH = os.path.join(os.path.dirname(__file__), "..", "findings")
RESULTS_OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "structural_lexical_decomposition.json")

PUNCT_RE = re.compile(r'^[\W_]+$')
NEWLINE_PROB_THRESHOLD = 0.85


def classify_token(tok: dict) -> str:
    """Return 'structural' or 'lexical' for a token dict."""
    text = tok["token"]
    stripped = text.strip()
    if stripped == '' or stripped == '\n' or stripped == '\r\n':
        return "structural"
    if tok.get("p_newline", 0) > NEWLINE_PROB_THRESHOLD:
        return "structural"
    if PUNCT_RE.match(stripped):
        return "structural"
    return "lexical"


def decompose_poem(poem: dict) -> dict:
    tokens = poem.get("tokens", [])
    if not tokens:
        return None

    meta = poem["metadata"]
    struct_s2, lex_s2 = [], []
    struct_surprisal, lex_surprisal = [], []
    struct_entropy, lex_entropy = [], []

    for tok in tokens:
        kind = classify_token(tok)
        s2 = tok["s2"]
        surp = tok["surprisal"]
        ent = tok["entropy"]
        if kind == "structural":
            struct_s2.append(s2)
            struct_surprisal.append(surp)
            struct_entropy.append(ent)
        else:
            lex_s2.append(s2)
            lex_surprisal.append(surp)
            lex_entropy.append(ent)

    total = len(tokens)
    struct_n = len(struct_s2)
    lex_n = len(lex_s2)

    if total == 0:
        return None

    avg = lambda lst: sum(lst) / len(lst) if lst else 0.0

    struct_contrib = sum(struct_s2) / total  # per-token contribution to avg S2
    lex_contrib = sum(lex_s2) / total

    return {
        "title": meta["title"],
        "author": meta["author"],
        "year": meta.get("year"),
        "era": meta.get("era", "unknown"),
        "n_tokens": total,
        "structural_frac": struct_n / total,
        "lexical_frac": lex_n / total,
        "overall_avg_s2": avg(struct_s2 + lex_s2),
        "structural_avg_s2": avg(struct_s2),
        "lexical_avg_s2": avg(lex_s2),
        "structural_contrib": struct_contrib,
        "lexical_contrib": lex_contrib,
        "decomp_ratio": lex_contrib / struct_contrib if struct_contrib != 0 else float('inf'),
        "structural_pos_ratio": sum(1 for x in struct_s2 if x > 0) / struct_n if struct_n else 0,
        "lexical_pos_ratio": sum(1 for x in lex_s2 if x > 0) / lex_n if lex_n else 0,
    }


def main():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    results = []
    for poem in corpus:
        if poem.get("metadata", {}).get("language", "en") != "en":
            continue
        r = decompose_poem(poem)
        if r:
            results.append(r)

    # Group by era
    era_data = defaultdict(list)
    for r in results:
        era_data[r["era"]].append(r)

    era_stats = []
    for era, poems in sorted(era_data.items(), key=lambda x: -len(x[1])):
        if len(poems) < 2:
            continue
        avg = lambda key: sum(p[key] for p in poems) / len(poems)
        era_stats.append({
            "era": era,
            "n": len(poems),
            "overall_avg_s2": avg("overall_avg_s2"),
            "structural_avg_s2": avg("structural_avg_s2"),
            "lexical_avg_s2": avg("lexical_avg_s2"),
            "structural_contrib": avg("structural_contrib"),
            "lexical_contrib": avg("lexical_contrib"),
            "structural_frac": avg("structural_frac"),
            "struct_minus_lex_contrib": avg("structural_contrib") - avg("lexical_contrib"),
        })

    # Sort by how much structural S2 DOMINATES lexical S2
    era_stats_by_struct = sorted(era_stats, key=lambda x: -x["structural_contrib"])

    # Top lexical-dominant poems
    lex_dominant = sorted(results, key=lambda x: -x["lexical_contrib"])[:15]
    struct_dominant = sorted(results, key=lambda x: -x["structural_contrib"])[:15]

    output = {
        "era_stats": era_stats_by_struct,
        "most_lexical_poems": lex_dominant,
        "most_structural_poems": struct_dominant,
        "n_poems": len(results),
    }

    with open(RESULTS_OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Analyzed {len(results)} poems")
    print("\n=== ERA S2 DECOMPOSITION (sorted by structural contribution) ===")
    print(f"{'Era':<22} {'n':>4}  {'Struct S2':>10}  {'Lexical S2':>10}  {'Struct frac':>12}")
    print("-" * 68)
    for e in era_stats_by_struct:
        print(f"{e['era']:<22} {e['n']:>4}  {e['structural_contrib']:>+10.3f}  {e['lexical_contrib']:>+10.3f}  {e['structural_frac']:>11.1%}")

    print("\n=== MOST LEXICALLY S2-DOMINANT POEMS ===")
    for p in lex_dominant[:8]:
        print(f"  {p['title'][:40]:<40} lex={p['lexical_contrib']:+.3f}  str={p['structural_contrib']:+.3f}")

    print("\n=== MOST STRUCTURALLY S2-DOMINANT POEMS ===")
    for p in struct_dominant[:8]:
        print(f"  {p['title'][:40]:<40} str={p['structural_contrib']:+.3f}  lex={p['lexical_contrib']:+.3f}")

    return output


if __name__ == "__main__":
    main()
