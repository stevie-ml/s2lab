"""
Title Word Recurrence and S2

When words from a poem's title appear in the body text, do they show
different S2 values vs. the rest of the poem?

Hypothesis A (priming): Title words in the body will have LOWER S2 —
  the title creates a semantic frame, making GPT-2 less surprised by them.

Hypothesis B (strategic recurrence): Title words will have HIGHER S2 —
  poets deliberately echo titles at moments of semantic emphasis/surprise.

Hypothesis C (null): No systematic difference.

Method:
  - Tokenize poem text, match tokens against title word stems
  - Compare S2 at title-word positions vs. non-title-word positions
  - Filter out stanza-break artifact (p_newline < 0.9)
  - Analyze per poem, then aggregate
"""

import json
import re
import statistics
from collections import defaultdict


def normalize(s):
    """Lowercase and strip punctuation for matching."""
    return re.sub(r"[^a-z]", "", s.lower())


def get_title_words(title):
    """Extract meaningful words from title (skip stop words)."""
    stop_words = {
        "a", "an", "the", "of", "in", "on", "at", "to", "for",
        "with", "by", "from", "as", "is", "are", "was", "were",
        "and", "or", "but", "not", "no", "i", "my", "me", "you",
        "he", "she", "it", "we", "they", "his", "her", "its",
        "their", "that", "this", "be", "do", "did", "has", "have",
        "had", "will", "would", "could", "should", "may", "might",
        "shall", "can", "so", "if", "when", "where", "who", "which",
    }
    words = re.findall(r"[a-zA-Z]+", title)
    return {normalize(w) for w in words if normalize(w) not in stop_words and len(normalize(w)) > 2}


def run_title_recurrence(corpus_path):
    with open(corpus_path) as f:
        data = json.load(f)

    # Aggregate results
    title_s2_all = []
    non_title_s2_all = []
    poem_level = []

    # For detailed cases
    high_delta_poems = []

    for poem in data:
        meta = poem.get("metadata", {})
        title = meta.get("title", "")
        era = meta.get("era", "")
        author = meta.get("author", "")
        tokens = poem.get("tokens", [])

        if not tokens or not title:
            continue

        title_words = get_title_words(title)
        if not title_words:
            continue

        title_s2 = []
        non_title_s2 = []

        for tok in tokens:
            # Filter stanza-break artifact
            if tok.get("p_newline", 0) >= 0.9:
                continue
            s2 = tok["s2"]
            token_str = normalize(tok["token"])

            # Check if this token matches any title word
            is_title_word = any(
                token_str == tw or
                (len(tw) > 3 and token_str.startswith(tw[:4])) or
                (len(token_str) > 3 and tw.startswith(token_str[:4]))
                for tw in title_words
            )

            if is_title_word:
                title_s2.append(s2)
            else:
                non_title_s2.append(s2)

        if len(title_s2) >= 1 and len(non_title_s2) >= 5:
            avg_title = statistics.mean(title_s2)
            avg_non = statistics.mean(non_title_s2)
            delta = avg_title - avg_non

            title_s2_all.extend(title_s2)
            non_title_s2_all.extend(non_title_s2)

            poem_level.append({
                "title": title,
                "author": author,
                "era": era,
                "title_words": sorted(title_words),
                "n_title_occurrences": len(title_s2),
                "avg_title_s2": round(avg_title, 3),
                "avg_non_title_s2": round(avg_non, 3),
                "delta": round(delta, 3),
            })

            if abs(delta) > 1.0:
                high_delta_poems.append(poem_level[-1])

    return {
        "poem_level": poem_level,
        "high_delta": high_delta_poems,
        "title_s2_all": title_s2_all,
        "non_title_s2_all": non_title_s2_all,
    }


def print_report(results):
    poem_level = results["poem_level"]
    ts = results["title_s2_all"]
    ns = results["non_title_s2_all"]

    print(f"\n=== TITLE WORD RECURRENCE AND S2 ===")
    print(f"\nPoems with analyzable title recurrence: {len(poem_level)}")
    print(f"Total title-word token occurrences: {len(ts)}")
    print(f"Total non-title token occurrences: {len(ns)}")

    if ts and ns:
        avg_ts = statistics.mean(ts)
        avg_ns = statistics.mean(ns)
        print(f"\nGlobal avg S2 at TITLE positions: {avg_ts:.3f}")
        print(f"Global avg S2 at NON-TITLE positions: {avg_ns:.3f}")
        print(f"Delta (title - non-title): {avg_ts - avg_ns:.3f}")

        # Median
        med_ts = statistics.median(ts)
        med_ns = statistics.median(ns)
        print(f"\nMedian S2 at TITLE positions: {med_ts:.3f}")
        print(f"Median S2 at NON-TITLE positions: {med_ns:.3f}")

    # Direction count
    higher = sum(1 for p in poem_level if p["delta"] > 0)
    lower = sum(1 for p in poem_level if p["delta"] < 0)
    print(f"\nPoems where title words have HIGHER S2: {higher} ({100*higher/len(poem_level):.0f}%)")
    print(f"Poems where title words have LOWER S2: {lower} ({100*lower/len(poem_level):.0f}%)")

    # Top/bottom by delta
    sorted_poems = sorted(poem_level, key=lambda x: x["delta"], reverse=True)
    print("\n--- Top 10 poems: title words MOST surprising (high delta) ---")
    for p in sorted_poems[:10]:
        print(f"  {p['delta']:+.2f}  [{p['author']}] '{p['title']}' ({p['era']})")
        print(f"        title_words={p['title_words']}, n={p['n_title_occurrences']}")

    print("\n--- Top 10 poems: title words LEAST surprising (low delta) ---")
    for p in sorted_poems[-10:]:
        print(f"  {p['delta']:+.2f}  [{p['author']}] '{p['title']}' ({p['era']})")
        print(f"        title_words={p['title_words']}, n={p['n_title_occurrences']}")

    # By era
    era_data = defaultdict(list)
    for p in poem_level:
        era_data[p["era"]].append(p["delta"])

    era_avgs = {era: (statistics.mean(deltas), len(deltas))
                for era, deltas in era_data.items() if len(deltas) >= 2}

    print("\n--- Delta by era (min 2 poems) ---")
    for era, (avg, n) in sorted(era_avgs.items(), key=lambda x: -x[1][0]):
        print(f"  {era:25s}  avg delta={avg:+.3f}  n={n}")

    return sorted_poems


if __name__ == "__main__":
    results = run_title_recurrence("results/corpus_results.json")
    sorted_poems = print_report(results)

    # Save summary
    summary = {
        "n_poems": len(results["poem_level"]),
        "n_title_tokens": len(results["title_s2_all"]),
        "n_non_title_tokens": len(results["non_title_s2_all"]),
        "avg_title_s2": round(statistics.mean(results["title_s2_all"]), 4) if results["title_s2_all"] else None,
        "avg_non_title_s2": round(statistics.mean(results["non_title_s2_all"]), 4) if results["non_title_s2_all"] else None,
        "poem_level": results["poem_level"],
    }
    with open("findings/title_recurrence_s2.json", "w") as f:
        json.dump(summary, f, indent=2)
    print("\n[Saved findings/title_recurrence_s2.json]")
