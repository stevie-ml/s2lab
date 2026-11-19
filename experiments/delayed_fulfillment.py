"""
Delayed Fulfillment Hypothesis
===============================
When a poet suppresses GPT-2's top prediction (high S2), does that
suppressed word appear later in the same poem?

If so: the poet has not abandoned the expectation but *deferred* it —
creating a semantic debt that gets paid off later. This would be evidence
that poets consciously manage reader expectation over long arcs.

We distinguish:
  - Quick fulfillment: suppressed word appears within 20 tokens
  - Delayed fulfillment: suppressed word appears 20–100 tokens later
  - Long-arc fulfillment: appears >100 tokens later
  - No fulfillment: word never appears

We filter out function words / punctuation to focus on content words.
"""

import json
import re
from collections import defaultdict
import os

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

# Common function words / structural tokens to skip (not interesting)
SKIP_TOKENS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "as", "is", "was", "are", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "that",
    "this", "it", "he", "she", "they", "we", "i", "you", "my", "his",
    "her", "their", "our", "your", "its", "not", "no", "so", "if",
    ",", ".", ";", ":", "!", "?", '"', "'", "(", ")", "-", "--",
    "\n", " ", "", "—", "…",
}

S2_THRESHOLD = 2.0  # Tokens where S2 > this are "moments of suppression"
CONTENT_WORD_MIN_LENGTH = 3  # Skip very short tokens


def normalize_token(tok):
    """Strip leading space, lowercase."""
    return tok.strip().lower()


def is_content_token(tok):
    """True if token is a meaningful content word (not function/punct)."""
    n = normalize_token(tok)
    if n in SKIP_TOKENS:
        return False
    if len(n) < CONTENT_WORD_MIN_LENGTH:
        return False
    if re.match(r'^[^a-z]+$', n):  # No letters at all
        return False
    return True


def analyze_poem_delayed_fulfillment(poem):
    """
    For each high-S2 position in a poem, check whether the top-1 suppressed
    prediction (GPT-2's most likely alternative) appears later in the poem.
    Returns a list of events.
    """
    tokens = poem.get("tokens", [])
    meta = poem.get("metadata", {})
    title = meta.get("title", "?")
    author = meta.get("author", "?")
    era = meta.get("era", "?")

    # Build list of actual token texts (lowercase, normalized)
    actual_tokens = [normalize_token(t["token"]) for t in tokens]
    n = len(tokens)

    events = []

    for i, tok_data in enumerate(tokens):
        s2 = tok_data.get("s2", 0)
        if s2 < S2_THRESHOLD:
            continue

        alternatives = tok_data.get("alternatives", [])
        if not alternatives:
            continue

        top1 = alternatives[0]["token"]
        top1_norm = normalize_token(top1)
        top1_prob = alternatives[0]["prob"]

        # Skip newlines and non-content top predictions
        if not is_content_token(top1):
            continue

        # Also skip if top1 probability is dominated by newline (p_newline > 0.8)
        p_newline = tok_data.get("p_newline", 0)
        if p_newline > 0.8:
            continue

        # Look for top1 in tokens AFTER position i
        fulfillment_pos = None
        for j in range(i + 1, n):
            if actual_tokens[j] == top1_norm:
                fulfillment_pos = j
                break

        distance = fulfillment_pos - i if fulfillment_pos is not None else None

        if distance is not None:
            if distance <= 20:
                category = "quick"
            elif distance <= 100:
                category = "delayed"
            else:
                category = "long_arc"
        else:
            category = "unfulfilled"

        events.append({
            "title": title,
            "author": author,
            "era": era,
            "position": i,
            "token_chosen": tok_data["token"],
            "top1_suppressed": top1,
            "top1_prob": top1_prob,
            "s2": s2,
            "fulfillment_distance": distance,
            "fulfillment_category": category,
        })

    return events


def run():
    print("Loading corpus...")
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        poems = json.load(f)

    all_events = []
    for poem in poems:
        era = poem.get("metadata", {}).get("era", "")
        if era == "control":
            continue
        events = analyze_poem_delayed_fulfillment(poem)
        all_events.extend(events)

    print(f"Found {len(all_events)} suppression events (S2 > {S2_THRESHOLD}, content words)")

    # --- Overall fulfillment rates ---
    total = len(all_events)
    cats = defaultdict(int)
    for e in all_events:
        cats[e["fulfillment_category"]] += 1

    print("\nOverall fulfillment rates:")
    for cat in ["quick", "delayed", "long_arc", "unfulfilled"]:
        pct = 100 * cats[cat] / total if total else 0
        print(f"  {cat}: {cats[cat]} ({pct:.1f}%)")

    # --- Fulfillment rate by era ---
    era_stats = defaultdict(lambda: {"total": 0, "fulfilled": 0,
                                     "quick": 0, "delayed": 0,
                                     "long_arc": 0, "unfulfilled": 0})
    for e in all_events:
        era = e["era"]
        era_stats[era]["total"] += 1
        era_stats[era][e["fulfillment_category"]] += 1
        if e["fulfillment_category"] != "unfulfilled":
            era_stats[era]["fulfilled"] += 1

    # Sort by fulfillment rate
    era_rows = []
    for era, s in era_stats.items():
        if s["total"] < 3:
            continue
        rate = s["fulfilled"] / s["total"]
        era_rows.append((era, s["total"], rate, s["quick"], s["delayed"],
                         s["long_arc"], s["unfulfilled"]))
    era_rows.sort(key=lambda x: -x[2])

    # --- Fulfillment rate by author ---
    author_stats = defaultdict(lambda: {"total": 0, "fulfilled": 0,
                                        "quick": 0, "delayed": 0,
                                        "long_arc": 0, "unfulfilled": 0})
    for e in all_events:
        author = e["author"]
        author_stats[author]["total"] += 1
        author_stats[author][e["fulfillment_category"]] += 1
        if e["fulfillment_category"] != "unfulfilled":
            author_stats[author]["fulfilled"] += 1

    author_rows = []
    for author, s in author_stats.items():
        if s["total"] < 3:
            continue
        rate = s["fulfilled"] / s["total"]
        author_rows.append((author, s["total"], rate, s["quick"], s["delayed"],
                            s["long_arc"], s["unfulfilled"]))
    author_rows.sort(key=lambda x: -x[2])

    # --- Most striking delayed-fulfillment examples ---
    delayed_examples = [e for e in all_events
                        if e["fulfillment_category"] in ("delayed", "long_arc")]
    delayed_examples.sort(key=lambda x: -x["s2"])
    top_examples = delayed_examples[:15]

    # --- Save results ---
    output = {
        "total_events": total,
        "category_counts": dict(cats),
        "era_stats": {r[0]: {"total": r[1], "fulfillment_rate": r[2],
                              "quick": r[3], "delayed": r[4],
                              "long_arc": r[5], "unfulfilled": r[6]}
                      for r in era_rows},
        "top_examples": top_examples,
    }
    out_path = os.path.join(RESULTS_DIR, "delayed_fulfillment.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return output, era_rows, author_rows, top_examples


if __name__ == "__main__":
    output, era_rows, author_rows, top_examples = run()
