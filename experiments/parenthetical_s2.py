"""
Parenthetical asides and S₂: When poets whisper.
When a poet uses parentheses, they create a secondary frame — an aside, a qualification,
an ironic interjection. This experiment asks: does text inside parenthetical expressions
have different S₂ than the surrounding poem?
"""

import json
import re
from collections import defaultdict

def load_data():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def find_parenthetical_tokens(poem):
    """
    Given a poem's token list, return sets of positions inside parentheses.
    Returns:
      - open_paren_positions: positions of '(' tokens
      - close_paren_positions: positions of ')' tokens
      - inside_positions: positions of tokens strictly inside parentheses
      - outside_positions: all other alpha token positions
    """
    tokens = poem["tokens"]
    open_paren_positions = set()
    close_paren_positions = set()
    inside_positions = set()
    outside_positions = set()

    # First pass: find all paren tokens
    depth = 0
    paren_stack = []

    for i, tok in enumerate(tokens):
        t = tok["token"].strip()
        if t == "(":
            open_paren_positions.add(i)
            depth += 1
            paren_stack.append(i)
        elif t == ")" and depth > 0:
            close_paren_positions.add(i)
            depth -= 1
            if paren_stack:
                paren_stack.pop()

    # Second pass: mark inside positions
    depth = 0
    for i, tok in enumerate(tokens):
        t = tok["token"].strip()
        if i in open_paren_positions:
            depth += 1
        elif i in close_paren_positions:
            depth -= 1
        elif depth > 0:
            inside_positions.add(i)
        else:
            # Only count alpha tokens for outside baseline
            if any(c.isalpha() for c in tok["token"]):
                outside_positions.add(i)

    return open_paren_positions, close_paren_positions, inside_positions, outside_positions

def compute_stats(values):
    if not values:
        return None
    n = len(values)
    mean = sum(values) / n
    pos = sum(1 for v in values if v > 0) / n
    sorted_v = sorted(values)
    median = sorted_v[n // 2]
    max_v = max(values)
    return {"n": n, "mean": round(mean, 3), "median": round(median, 3), "pos_pct": round(pos * 100, 1), "max": round(max_v, 3)}

def main():
    data = load_data()

    # Collect poems that have parenthetical content
    poems_with_parens = []
    all_inside_s2 = []
    all_outside_s2 = []
    all_open_paren_s2 = []
    all_close_paren_s2 = []

    # By era
    era_data = defaultdict(lambda: {"inside": [], "outside": []})
    # By author
    author_data = defaultdict(lambda: {"inside": [], "outside": [], "poems": []})

    # Collect parenthetical content examples
    examples = []

    for poem in data:
        if poem["metadata"].get("language", "en") != "en":
            continue

        tokens = poem["tokens"]
        open_p, close_p, inside_p, outside_p = find_parenthetical_tokens(poem)

        if not inside_p and not open_p:
            continue

        # Collect S2 values
        poem_inside = [tokens[i]["s2"] for i in inside_p if not tokens[i].get("p_newline", 0) > 0.9]
        poem_outside = [tokens[i]["s2"] for i in outside_p if not tokens[i].get("p_newline", 0) > 0.9]

        # Collect the paren tokens themselves
        for i in open_p:
            all_open_paren_s2.append(tokens[i]["s2"])
        for i in close_p:
            all_close_paren_s2.append(tokens[i]["s2"])

        all_inside_s2.extend(poem_inside)
        all_outside_s2.extend(poem_outside)

        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")

        era_data[era]["inside"].extend(poem_inside)
        era_data[era]["outside"].extend(poem_outside)
        author_data[author]["inside"].extend(poem_inside)
        author_data[author]["outside"].extend(poem_outside)
        author_data[author]["poems"].append(poem["metadata"]["title"])

        if poem_inside:
            # Collect example: highest S2 token inside a parenthetical
            best_inside = None
            best_s2 = -999
            for i in inside_p:
                tok = tokens[i]
                if tok["s2"] > best_s2 and any(c.isalpha() for c in tok["token"]):
                    best_s2 = tok["s2"]
                    best_inside = i

            # Also record what's just before and after the paren
            context_parts = []
            for i in sorted(inside_p)[:15]:
                context_parts.append(tokens[i]["token"])
            context_text = "".join(context_parts)

            # Find surrounding context (unused, removed)

            examples.append({
                "title": poem["metadata"]["title"],
                "author": poem["metadata"]["author"],
                "era": era,
                "n_inside": len(poem_inside),
                "inside_mean_s2": round(sum(poem_inside)/len(poem_inside), 3) if poem_inside else None,
                "outside_mean_s2": round(sum(poem_outside)/len(poem_outside), 3) if poem_outside else None,
                "gap": round(sum(poem_inside)/len(poem_inside) - sum(poem_outside)/len(poem_outside), 3) if poem_inside and poem_outside else None,
                "context": context_text[:60],
                "best_inside_token": tokens[best_inside]["token"] if best_inside else "",
                "best_inside_s2": round(best_s2, 3),
            })

        poems_with_parens.append(poem["metadata"]["title"])

    print(f"\n=== PARENTHETICAL ASIDES AND S₂ ===\n")
    print(f"Total poems with parenthetical content: {len(poems_with_parens)}")
    print(f"Total inside-paren tokens: {len(all_inside_s2)}")
    print(f"Total outside-paren tokens (baseline): {len(all_outside_s2)}")

    print(f"\n--- GLOBAL COMPARISON ---")
    inside_stats = compute_stats(all_inside_s2)
    outside_stats = compute_stats(all_outside_s2)
    paren_open_stats = compute_stats(all_open_paren_s2)
    paren_close_stats = compute_stats(all_close_paren_s2)

    print(f"\nLocation           | N      | Mean S₂ | Median S₂ | Pos% | Max S₂")
    print(f"-------------------|--------|---------|-----------|------|-------")
    print(f"Inside ( )         | {inside_stats['n']:>6} | {inside_stats['mean']:>7} | {inside_stats['median']:>9} | {inside_stats['pos_pct']:>4}% | {inside_stats['max']:>7}")
    print(f"Outside ( )        | {outside_stats['n']:>6} | {outside_stats['mean']:>7} | {outside_stats['median']:>9} | {outside_stats['pos_pct']:>4}% | {outside_stats['max']:>7}")
    print(f"'(' token itself   | {paren_open_stats['n']:>6} | {paren_open_stats['mean']:>7} | {paren_open_stats['median']:>9} | {paren_open_stats['pos_pct']:>4}% | {paren_open_stats['max']:>7}")
    print(f"')' token itself   | {paren_close_stats['n']:>6} | {paren_close_stats['mean']:>7} | {paren_close_stats['median']:>9} | {paren_close_stats['pos_pct']:>4}% | {paren_close_stats['max']:>7}")

    gap = inside_stats["mean"] - outside_stats["mean"]
    print(f"\nS₂ gap (inside − outside): {gap:+.3f}")

    print(f"\n--- ERA BREAKDOWN (eras with ≥10 inside tokens) ---")
    era_rows = []
    for era, d in era_data.items():
        if len(d["inside"]) >= 10:
            ins = compute_stats(d["inside"])
            out = compute_stats(d["outside"]) if d["outside"] else None
            if ins and out:
                era_rows.append({
                    "era": era,
                    "n_inside": ins["n"],
                    "inside_mean": ins["mean"],
                    "outside_mean": out["mean"],
                    "gap": round(ins["mean"] - out["mean"], 3),
                })
    era_rows.sort(key=lambda x: x["gap"], reverse=True)

    print(f"\nEra                    | n_in | Inside Mean | Outside Mean | Gap")
    print(f"-----------------------|------|-------------|--------------|-----")
    for row in era_rows:
        print(f"{row['era']:<23} | {row['n_inside']:>4} | {row['inside_mean']:>11} | {row['outside_mean']:>12} | {row['gap']:>+.3f}")

    print(f"\n--- AUTHOR BREAKDOWN (authors with ≥10 inside tokens) ---")
    author_rows = []
    for author, d in author_data.items():
        if len(d["inside"]) >= 10:
            ins = compute_stats(d["inside"])
            out = compute_stats(d["outside"]) if d["outside"] else None
            if ins and out:
                author_rows.append({
                    "author": author,
                    "n_inside": ins["n"],
                    "inside_mean": ins["mean"],
                    "outside_mean": out["mean"],
                    "gap": round(ins["mean"] - out["mean"], 3),
                })
    author_rows.sort(key=lambda x: x["gap"], reverse=True)

    print(f"\nAuthor                 | n_in | Inside Mean | Outside Mean | Gap")
    print(f"-----------------------|------|-------------|--------------|-----")
    for row in author_rows[:20]:
        print(f"{row['author'][:23]:<23} | {row['n_inside']:>4} | {row['inside_mean']:>11} | {row['outside_mean']:>12} | {row['gap']:>+.3f}")

    print(f"\n--- TOP EXAMPLES: HIGHEST INSIDE MEAN S₂ vs LOWEST ---")
    examples_with_gap = [e for e in examples if e["gap"] is not None]
    examples_with_gap.sort(key=lambda x: x["gap"], reverse=True)

    print("\nTop 10 poems where parenthetical S₂ >> outside:")
    print(f"{'Title':<35} | {'Author':<20} | Inside | Outside | Gap")
    for e in examples_with_gap[:10]:
        print(f"{e['title'][:35]:<35} | {e['author'][:20]:<20} | {e['inside_mean_s2']:>6} | {e['outside_mean_s2']:>7} | {e['gap']:>+.3f}")

    print("\nBottom 10 poems where parenthetical S₂ << outside:")
    for e in examples_with_gap[-10:]:
        print(f"{e['title'][:35]:<35} | {e['author'][:20]:<20} | {e['inside_mean_s2']:>6} | {e['outside_mean_s2']:>7} | {e['gap']:>+.3f}")

    print(f"\n--- PARENTHETICAL CONTENT EXAMPLES ---")
    # Show some high-S2 parenthetical examples
    high_examples = [e for e in examples_with_gap if e.get("best_inside_s2", 0) > 5]
    high_examples.sort(key=lambda x: x.get("best_inside_s2", 0), reverse=True)
    print("\nHighest-S₂ tokens found inside parentheses:")
    print(f"{'Token':<20} | S₂ | Context | Poem")
    for e in high_examples[:15]:
        print(f"{e['best_inside_token']:<20} | {e['best_inside_s2']:>5} | {e['context'][:25]:<25} | {e['title'][:30]}")

    # Save results
    result = {
        "global": {
            "inside": inside_stats,
            "outside": outside_stats,
            "open_paren": paren_open_stats,
            "close_paren": paren_close_stats,
            "gap": round(gap, 3),
        },
        "era_breakdown": era_rows,
        "author_breakdown": author_rows[:30],
        "top_examples": examples_with_gap[:20],
        "bottom_examples": examples_with_gap[-20:],
        "poems_with_parens": poems_with_parens,
        "n_poems_with_parens": len(poems_with_parens),
    }
    with open("results/parenthetical_s2.json", "w") as f:
        json.dump(result, f, indent=2)
    print(f"\nResults saved to results/parenthetical_s2.json")

if __name__ == "__main__":
    main()
