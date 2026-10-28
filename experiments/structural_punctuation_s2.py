"""
Structural punctuation as S2 markers: em-dash, colon, semicolon.

The em-dash (Dickinson), colon (Hopkins, Plath), and semicolon are structural
choices that "pause" or redirect the poem's syntactic flow. The frequency_register_gap
study noted that "em-dash and colon as high-S2 tokens deserve their own analysis."

Hypothesis: These structural marks should have significantly higher S2 than
conventional punctuation (comma, period) because they BREAK the model's expectation
of grammatical continuation.

Sub-hypotheses:
1. Em-dash > colon > semicolon > comma in avg S2 (ordered by "disruptiveness")
2. Dickinson's em-dashes are more informationally disruptive than other poets' em-dashes
3. Structural punctuation in LINE-FINAL positions (enjambment reinforcement) has
   higher S2 than in mid-line positions
4. The token AFTER a structural mark has higher entropy (model is now uncertain)
"""

import json
import re
from collections import defaultdict
import numpy as np
from datetime import datetime

with open("results/corpus_results.json") as f:
    data = json.load(f)


def classify_punctuation(token: str) -> str | None:
    t = token.strip()
    if not t:
        return None
    if "——" in token or "—" in token or "--" in token:
        return "em_dash"
    if t == ":":
        return "colon"
    if t == ";":
        return "semicolon"
    if t == ",":
        return "comma"
    if t in (".", "!", "?"):
        return "sentence_end"
    return None


def is_line_final(tokens, idx) -> bool:
    """Check if this token is at or near a line-final position
    (the next token is a newline or this is before a newline)."""
    if idx + 1 >= len(tokens):
        return True
    nxt = tokens[idx + 1].get("token", "")
    return "\n" in nxt or nxt.strip() == ""


results = {
    "em_dash": [],
    "colon": [],
    "semicolon": [],
    "comma": [],
    "sentence_end": [],
}

poet_em_dash = defaultdict(list)
poet_colon = defaultdict(list)

# Per-poet, per-era tracking
era_data = defaultdict(lambda: defaultdict(list))

after_structural_entropy = []  # H(token after em_dash/colon/semicolon)
after_comma_entropy = []        # H(token after comma)

line_position_data = {"em_dash": {"mid": [], "final": []},
                      "colon": {"mid": [], "final": []},
                      "semicolon": {"mid": [], "final": []}}

examples = defaultdict(list)  # ptype -> list of (s2, token, context, author, title)

for poem in data:
    meta = poem.get("metadata", {})
    author = meta.get("author", "Unknown")
    title = meta.get("title", "Unknown")
    era = meta.get("era", "unknown")
    tokens = poem.get("tokens", [])
    lang = meta.get("language", "en")
    if lang != "en":
        continue

    for i, t in enumerate(tokens):
        raw_tok = t.get("token", "")
        s2 = t.get("s2", 0.0)
        h = t.get("entropy", None)
        p_newline = t.get("p_newline", 0.0)

        # Skip stanza-break artifact
        if p_newline >= 0.9:
            continue

        ptype = classify_punctuation(raw_tok)
        if ptype is None:
            continue

        results[ptype].append(s2)
        era_data[era][ptype].append(s2)

        if ptype == "em_dash":
            poet_em_dash[author].append(s2)
        elif ptype == "colon":
            poet_colon[author].append(s2)

        # Line position
        if ptype in line_position_data:
            pos = "final" if is_line_final(tokens, i) else "mid"
            line_position_data[ptype][pos].append(s2)

        # After-mark entropy
        if i + 1 < len(tokens):
            next_t = tokens[i + 1]
            next_h = next_t.get("entropy", None)
            if next_h is not None:
                if ptype in ("em_dash", "colon", "semicolon"):
                    after_structural_entropy.append(next_h)
                elif ptype == "comma":
                    after_comma_entropy.append(next_h)

        # Collect examples for high-S2 structural marks
        if ptype in ("em_dash", "colon", "semicolon") and s2 > 2.0:
            ctx_before = "".join(
                tok.get("token", "") for tok in tokens[max(0, i-5):i]
            )
            examples[ptype].append((s2, raw_tok, ctx_before, author, title))


# Summary stats
print("=" * 60)
print("STRUCTURAL PUNCTUATION S2 ANALYSIS")
print("=" * 60)

order = ["em_dash", "colon", "semicolon", "comma", "sentence_end"]
print(f"\n{'Type':<15} {'N':>5} {'Mean S2':>10} {'Median':>10} {'Pos%':>8} {'Max S2':>10}")
print("-" * 60)
for ptype in order:
    vals = results[ptype]
    if not vals:
        continue
    arr = np.array(vals)
    print(f"{ptype:<15} {len(arr):>5} {arr.mean():>10.3f} "
          f"{np.median(arr):>10.3f} "
          f"{(arr > 0).mean() * 100:>7.1f}% "
          f"{arr.max():>10.3f}")

# Hypothesis ranking
print("\n--- H1: Disruptiveness Ordering ---")
ranks = sorted(order, key=lambda p: np.mean(results[p]) if results[p] else -999, reverse=True)
for i, p in enumerate(ranks):
    if results[p]:
        print(f"  {i+1}. {p}: {np.mean(results[p]):.3f}")

# Per-poet em-dash analysis
print("\n--- H2: Top Em-Dash Poets by Avg S2 ---")
poet_em_stats = [
    (p, np.mean(v), len(v))
    for p, v in poet_em_dash.items() if len(v) >= 3
]
poet_em_stats.sort(key=lambda x: x[1], reverse=True)
for poet, avg, n in poet_em_stats[:12]:
    print(f"  {poet:<35} n={n:>3}  avg_s2={avg:.3f}")

# Per-poet colon analysis
print("\n--- Top Colon Poets by Avg S2 ---")
poet_col_stats = [
    (p, np.mean(v), len(v))
    for p, v in poet_colon.items() if len(v) >= 3
]
poet_col_stats.sort(key=lambda x: x[1], reverse=True)
for poet, avg, n in poet_col_stats[:10]:
    print(f"  {poet:<35} n={n:>3}  avg_s2={avg:.3f}")

# H3: Line position
print("\n--- H3: Line-Final vs Mid-Line Structural Punctuation ---")
for ptype in ("em_dash", "colon", "semicolon"):
    mid = line_position_data[ptype]["mid"]
    fin = line_position_data[ptype]["final"]
    if mid and fin:
        mid_arr = np.array(mid)
        fin_arr = np.array(fin)
        print(f"  {ptype}: mid={mid_arr.mean():.3f} (n={len(mid)}), "
              f"final={fin_arr.mean():.3f} (n={len(fin)})  "
              f"Δ={fin_arr.mean()-mid_arr.mean():+.3f}")

# H4: Post-mark entropy
print("\n--- H4: Entropy After Structural vs. Comma ---")
if after_structural_entropy and after_comma_entropy:
    se = np.array(after_structural_entropy)
    ce = np.array(after_comma_entropy)
    print(f"  After em-dash/colon/semicolon: mean H = {se.mean():.3f} (n={len(se)})")
    print(f"  After comma:                   mean H = {ce.mean():.3f} (n={len(ce)})")
    print(f"  Δ = {se.mean() - ce.mean():+.3f} (positive = more uncertain after structural mark)")

# Era analysis
print("\n--- Era Analysis: Em-Dash Usage S2 ---")
era_em_stats = [
    (era, np.mean(era_data[era]["em_dash"]), len(era_data[era]["em_dash"]))
    for era in era_data
    if len(era_data[era]["em_dash"]) >= 3
]
era_em_stats.sort(key=lambda x: x[1], reverse=True)
for era, avg, n in era_em_stats[:12]:
    print(f"  {era:<25} n={n:>3}  avg_s2={avg:.3f}")

# Top examples
print("\n--- Top 10 High-S2 Em-Dash Moments ---")
all_em_examples = sorted(examples.get("em_dash", []), key=lambda x: x[0], reverse=True)
for s2, tok, ctx, author, title in all_em_examples[:10]:
    print(f"  S2={s2:.2f} | …{ctx.strip()!r}⟨{tok}⟩ | {author} — {title}")

print("\n--- Top 10 High-S2 Colon Moments ---")
all_col_examples = sorted(examples.get("colon", []), key=lambda x: x[0], reverse=True)
for s2, tok, ctx, author, title in all_col_examples[:10]:
    print(f"  S2={s2:.2f} | …{ctx.strip()!r}⟨{tok}⟩ | {author} — {title}")

# Save results
output = {
    "generated": datetime.now().isoformat(),
    "summary": {
        ptype: {
            "n": len(results[ptype]),
            "mean_s2": float(np.mean(results[ptype])) if results[ptype] else None,
            "median_s2": float(np.median(results[ptype])) if results[ptype] else None,
            "pos_s2_pct": float((np.array(results[ptype]) > 0).mean() * 100) if results[ptype] else None,
            "max_s2": float(np.max(results[ptype])) if results[ptype] else None,
        }
        for ptype in order
    },
    "poet_em_dash": {
        p: {"mean_s2": float(np.mean(v)), "n": len(v)}
        for p, v in poet_em_dash.items() if len(v) >= 3
    },
    "line_position": {
        ptype: {
            pos: {
                "n": len(line_position_data[ptype][pos]),
                "mean_s2": float(np.mean(line_position_data[ptype][pos])) if line_position_data[ptype][pos] else None
            }
            for pos in ("mid", "final")
        }
        for ptype in ("em_dash", "colon", "semicolon")
    },
    "after_mark_entropy": {
        "after_structural": float(np.mean(after_structural_entropy)) if after_structural_entropy else None,
        "after_comma": float(np.mean(after_comma_entropy)) if after_comma_entropy else None,
    },
    "top_em_dash_examples": [
        {"s2": s2, "token": tok, "context_before": ctx, "author": author, "title": title}
        for s2, tok, ctx, author, title in all_em_examples[:20]
    ],
    "top_colon_examples": [
        {"s2": s2, "token": tok, "context_before": ctx, "author": author, "title": title}
        for s2, tok, ctx, author, title in all_col_examples[:20]
    ],
}

with open("results/structural_punctuation_s2.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to results/structural_punctuation_s2.json")
