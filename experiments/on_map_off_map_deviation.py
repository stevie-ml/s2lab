"""
On-Map vs. Off-Map Deviation: Two Geometries of Poetic Surprise

When a poet writes a high-S2 token (more surprising than entropy warrants),
there are two fundamentally different situations:

  ON-MAP deviation (rank ≤ 10):
    The chosen token appears in GPT-2's top-10 predictions.
    The model "considered" this word — it just assigned it lower probability
    than something else. The poet selected from the model's imaginative horizon
    but picked a less-expected option.
    Example: model predicts "cold" most likely, poet writes "blue" (rank 4).

  OFF-MAP deviation (rank > 10):
    The chosen token does NOT appear in GPT-2's top-10 predictions.
    The model essentially did not "imagine" this word at all given the context.
    The poet's choice is completely outside the model's probability mass.
    Example: model predicts "cold/dark/still/...", poet writes "giddy" (rank 847).

These two types represent different creative strategies:
  - On-map: "choosing the road less traveled" — working within a known space
    but selecting the less-obvious option. A conversational deviation.
  - Off-map: "leaving the map entirely" — vocabulary, register, or imagery
    that the model's training never connected to this context. A radical departure.

Research questions:
1. What fraction of high-S2 moments are on-map vs. off-map by era/genre?
2. Which poets favor on-map vs. off-map strategies?
3. Are on-map and off-map tokens characterized by different linguistic features
   (word length, part of speech, register)?
4. Do off-map tokens have systematically different S2 distributions than on-map?
"""

import json
import re
from collections import defaultdict

RESULTS = "results/corpus_results.json"
STANZA_ARTIFACT_THRESHOLD = 0.9
S2_THRESHOLD = 1.0  # minimum S2 to count as "high-S2"
MAP_BOUNDARY = 10   # rank ≤ this = on-map; rank > this = off-map


def is_artifact(tok):
    return tok.get("p_newline", 0) >= STANZA_ARTIFACT_THRESHOLD


def normalize(t):
    return t.strip().lower()


def word_length(token_str):
    """Estimate word length in characters (strip leading space)."""
    return len(token_str.strip())


def load_data():
    with open(RESULTS) as f:
        return json.load(f)


def classify_token(tok):
    """Return 'on_map', 'off_map', or None (not high-S2)."""
    if is_artifact(tok):
        return None
    if tok["s2"] < S2_THRESHOLD:
        return None
    rank = tok.get("rank", 999)
    if rank <= MAP_BOUNDARY:
        return "on_map"
    else:
        return "off_map"


def analyze(data):
    results = {
        "by_era": defaultdict(lambda: {"on_map": [], "off_map": [], "total": 0}),
        "by_author": defaultdict(lambda: {"on_map": [], "off_map": [], "total": 0}),
        "on_map_tokens": [],
        "off_map_tokens": [],
        "poem_summaries": [],
    }

    for poem in data:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        title = meta.get("title", "untitled")

        tokens = poem.get("tokens", [])
        clean_tokens = [t for t in tokens if not is_artifact(t)]

        if len(clean_tokens) < 5:
            continue

        on_map_count = 0
        off_map_count = 0
        on_map_s2 = []
        off_map_s2 = []

        for tok in clean_tokens:
            cat = classify_token(tok)
            if cat == "on_map":
                on_map_count += 1
                on_map_s2.append(tok["s2"])
                results["on_map_tokens"].append({
                    "token": tok["token"],
                    "s2": tok["s2"],
                    "rank": tok["rank"],
                    "entropy": tok["entropy"],
                    "era": era,
                    "author": author,
                    "context": tok.get("context_before", "")[-60:],
                    "top_alt": tok["alternatives"][0]["token"] if tok.get("alternatives") else "",
                })
            elif cat == "off_map":
                off_map_count += 1
                off_map_s2.append(tok["s2"])
                results["off_map_tokens"].append({
                    "token": tok["token"],
                    "s2": tok["s2"],
                    "rank": tok["rank"],
                    "entropy": tok["entropy"],
                    "era": era,
                    "author": author,
                    "context": tok.get("context_before", "")[-60:],
                    "top_alt": tok["alternatives"][0]["token"] if tok.get("alternatives") else "",
                })

        total_high = on_map_count + off_map_count
        if total_high == 0:
            continue

        on_map_ratio = on_map_count / total_high
        avg_on_map_s2 = sum(on_map_s2) / len(on_map_s2) if on_map_s2 else 0
        avg_off_map_s2 = sum(off_map_s2) / len(off_map_s2) if off_map_s2 else 0

        results["poem_summaries"].append({
            "title": title,
            "author": author,
            "era": era,
            "n_clean": len(clean_tokens),
            "on_map_count": on_map_count,
            "off_map_count": off_map_count,
            "on_map_ratio": on_map_ratio,
            "avg_on_map_s2": avg_on_map_s2,
            "avg_off_map_s2": avg_off_map_s2,
        })

        results["by_era"][era]["total"] += len(clean_tokens)
        results["by_era"][era]["on_map"].extend(on_map_s2)
        results["by_era"][era]["off_map"].extend(off_map_s2)

        results["by_author"][author]["total"] += len(clean_tokens)
        results["by_author"][author]["on_map"].extend(on_map_s2)
        results["by_author"][author]["off_map"].extend(off_map_s2)

    return results


def compute_era_stats(by_era):
    rows = []
    for era, d in by_era.items():
        n_on = len(d["on_map"])
        n_off = len(d["off_map"])
        total = n_on + n_off
        if total < 5:
            continue
        on_map_ratio = n_on / total if total else 0
        avg_on = sum(d["on_map"]) / n_on if n_on else 0
        avg_off = sum(d["off_map"]) / n_off if n_off else 0
        rows.append({
            "era": era,
            "n_on": n_on,
            "n_off": n_off,
            "total_high_s2": total,
            "on_map_ratio": on_map_ratio,
            "avg_on_map_s2": avg_on,
            "avg_off_map_s2": avg_off,
            "s2_gap": avg_off - avg_on,
        })
    return sorted(rows, key=lambda x: -x["on_map_ratio"])


def compute_author_stats(by_author):
    rows = []
    for author, d in by_author.items():
        n_on = len(d["on_map"])
        n_off = len(d["off_map"])
        total = n_on + n_off
        if total < 8:
            continue
        on_map_ratio = n_on / total if total else 0
        avg_on = sum(d["on_map"]) / n_on if n_on else 0
        avg_off = sum(d["off_map"]) / n_off if n_off else 0
        rows.append({
            "author": author,
            "n_on": n_on,
            "n_off": n_off,
            "total_high_s2": total,
            "on_map_ratio": on_map_ratio,
            "avg_on_map_s2": avg_on,
            "avg_off_map_s2": avg_off,
        })
    return sorted(rows, key=lambda x: -x["on_map_ratio"])


def compute_token_stats(tokens):
    """Aggregate statistics about a group of tokens."""
    if not tokens:
        return {}
    s2_vals = [t["s2"] for t in tokens]
    avg_s2 = sum(s2_vals) / len(s2_vals)
    avg_len = sum(word_length(t["token"]) for t in tokens) / len(tokens)
    # How often is the token longer than the top alternative?
    longer_than_alt = sum(
        1 for t in tokens
        if word_length(t["token"]) > word_length(t.get("top_alt", ""))
    )
    return {
        "count": len(tokens),
        "avg_s2": round(avg_s2, 3),
        "avg_word_len": round(avg_len, 2),
        "longer_than_alt_pct": round(100 * longer_than_alt / len(tokens), 1),
        "entropy_avg": round(sum(t["entropy"] for t in tokens) / len(tokens), 3),
    }


def top_examples(tokens, n=10):
    return sorted(tokens, key=lambda x: -x["s2"])[:n]


def main():
    data = load_data()
    results = analyze(data)

    era_stats = compute_era_stats(results["by_era"])
    author_stats = compute_author_stats(results["by_author"])
    on_map_stats = compute_token_stats(results["on_map_tokens"])
    off_map_stats = compute_token_stats(results["off_map_tokens"])

    # Overall ratio
    n_on = len(results["on_map_tokens"])
    n_off = len(results["off_map_tokens"])
    total = n_on + n_off
    print(f"=== ON-MAP vs. OFF-MAP DEVIATION ===")
    print(f"Total high-S₂ tokens (S₂ ≥ {S2_THRESHOLD}): {total}")
    print(f"  On-map  (rank ≤ {MAP_BOUNDARY}): {n_on} ({100*n_on/total:.1f}%)")
    print(f"  Off-map (rank > {MAP_BOUNDARY}): {n_off} ({100*n_off/total:.1f}%)")
    print()
    print("ON-MAP token stats:", on_map_stats)
    print("OFF-MAP token stats:", off_map_stats)
    print()

    print("=== ERA BREAKDOWN ===")
    for row in era_stats[:20]:
        bar = "█" * int(row["on_map_ratio"] * 20)
        print(f"  {row['era']:<25} on-map: {100*row['on_map_ratio']:4.0f}%  {bar}  (n={row['total_high_s2']})")
    print()

    print("=== AUTHOR BREAKDOWN (most on-map first) ===")
    for row in author_stats[:15]:
        print(f"  {row['author']:<30} on-map: {100*row['on_map_ratio']:4.0f}%  (n={row['total_high_s2']}, avg_on_S₂={row['avg_on_map_s2']:.2f}, avg_off_S₂={row['avg_off_map_s2']:.2f})")
    print()

    print("=== AUTHOR BREAKDOWN (most off-map first) ===")
    for row in sorted(author_stats, key=lambda x: x["on_map_ratio"])[:15]:
        print(f"  {row['author']:<30} on-map: {100*row['on_map_ratio']:4.0f}%  (n={row['total_high_s2']})")
    print()

    print("=== TOP ON-MAP EXAMPLES (high S₂, rank ≤ 10) ===")
    for ex in top_examples(results["on_map_tokens"], 10):
        print(f"  {repr(ex['token']):<20} S₂={ex['s2']:.2f} rank={ex['rank']:>3} | expected: {repr(ex['top_alt']):<15} | {ex['era']:<15} | ...{ex['context']}")
    print()

    print("=== TOP OFF-MAP EXAMPLES (high S₂, rank > 10) ===")
    for ex in top_examples(results["off_map_tokens"], 10):
        print(f"  {repr(ex['token']):<20} S₂={ex['s2']:.2f} rank={ex['rank']:>5} | expected: {repr(ex['top_alt']):<15} | {ex['era']:<15} | ...{ex['context']}")

    # Return structured results for saving
    return {
        "overall": {
            "n_on_map": n_on,
            "n_off_map": n_off,
            "on_map_pct": round(100 * n_on / total, 1),
            "off_map_pct": round(100 * n_off / total, 1),
        },
        "on_map_stats": on_map_stats,
        "off_map_stats": off_map_stats,
        "by_era": era_stats,
        "by_author": author_stats,
        "top_on_map_examples": top_examples(results["on_map_tokens"], 20),
        "top_off_map_examples": top_examples(results["off_map_tokens"], 20),
        "poem_summaries": sorted(results["poem_summaries"], key=lambda x: -x["on_map_ratio"])[:40],
    }


if __name__ == "__main__":
    import json as _json
    result = main()
    with open("results/on_map_off_map.json", "w") as f:
        _json.dump(result, f, indent=2)
    print("\nResults saved to results/on_map_off_map.json")
