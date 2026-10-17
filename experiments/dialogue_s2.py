"""
Dialogue in Poetry: S₂ inside vs outside quoted speech.

Research question: When a poet puts words in a character's mouth (quoted speech),
does the GPT-2 S₂ profile of those tokens differ from the surrounding narrative frame?

Hypotheses:
  H1 (Ballad): Formulaic question-answer dialogue in ballads should be lower S₂ inside
               quotes (conventional responses, predictable frames).
  H2 (Lyric/dramatic): Quoted speech in lyric/dramatic contexts captures surprising
                        utterances; S₂ should be HIGHER inside quotes.
  H3 (Attribution): The "he said / she cried" attribution phrases just outside quotes
                    should be LOWEST S₂ (most formulaic).
"""

import json
import re
import statistics
import os
from collections import defaultdict

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
ARTIFACT_P = 0.90


def load_results(filename="corpus_results.json"):
    path = os.path.join(RESULTS_DIR, filename)
    with open(path) as f:
        return json.load(f)


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def is_clean(tok):
    return newline_prob(tok) < ARTIFACT_P


def reconstruct_and_label(tokens):
    """
    Reconstruct the token string and label each token as
    'quoted', 'unquoted', or 'attribution' (within 6 tokens of a quote boundary).

    Returns list of (token_dict, label) pairs.
    """
    # Reconstruct character sequence with per-token boundaries
    # Each entry: (start_char, end_char, token_dict)
    spans = []
    pos = 0
    for tok in tokens:
        s = tok["token"]
        spans.append((pos, pos + len(s), tok))
        pos += len(s)
    full_text = "".join(tok["token"] for tok in tokens)

    # Find all quote characters and their positions
    # Only double quotes (curly and straight) — NOT apostrophes/single quotes,
    # which would misidentify contractions like "o'er", "don't" as quoted speech.
    OPEN_QUOTES = {'"', '“'}
    CLOSE_QUOTES = {'"', '”'}

    # Build a char-level in_quote array
    in_quote = [False] * len(full_text)
    quote_depth = 0
    for i, ch in enumerate(full_text):
        if ch in OPEN_QUOTES:
            quote_depth += 1
        elif ch in CLOSE_QUOTES and quote_depth > 0:
            quote_depth -= 1
        in_quote[i] = quote_depth > 0

    # For each token determine: what fraction of its characters are in quotes?
    labeled = []
    for (start, end, tok) in spans:
        if start >= end:
            labeled.append((tok, "unquoted"))
            continue
        chars_in = sum(1 for i in range(start, min(end, len(full_text))) if in_quote[i])
        frac = chars_in / (end - start)
        if frac > 0.5:
            labeled.append((tok, "quoted"))
        else:
            labeled.append((tok, "unquoted"))

    # Mark attribution tokens: unquoted tokens within 6 positions of a quote boundary
    # Find positions where label flips
    labels = [lbl for (_, lbl) in labeled]
    attribution_positions = set()
    for i in range(len(labels)):
        if labels[i] == "quoted":
            # mark 1-6 positions before
            for j in range(max(0, i - 6), i):
                if labels[j] == "unquoted":
                    attribution_positions.add(j)
            # mark 1-6 positions after
            for j in range(i + 1, min(len(labels), i + 7)):
                if labels[j] == "unquoted":
                    attribution_positions.add(j)

    final = []
    for i, (tok, lbl) in enumerate(labeled):
        if lbl == "unquoted" and i in attribution_positions:
            final.append((tok, "attribution"))
        else:
            final.append((tok, lbl))

    return final


def main():
    results = load_results()

    # Only English poems, exclude control prose
    en_results = [r for r in results
                  if r["metadata"].get("language", "en") == "en"
                  and r["metadata"].get("era", "") not in ("control",)]

    # Find poems with quoted speech
    poem_stats = []
    global_buckets = {"quoted": [], "unquoted": [], "attribution": []}

    era_buckets = defaultdict(lambda: {"quoted": [], "unquoted": []})

    for r in en_results:
        labeled = reconstruct_and_label(r["tokens"])

        # Check if poem has any quoted tokens
        quote_count = sum(1 for _, lbl in labeled if lbl == "quoted")
        if quote_count < 5:
            continue  # skip poems with negligible quoted content

        # Collect S2 per label (clean tokens only)
        buckets = {"quoted": [], "unquoted": [], "attribution": []}
        for tok, lbl in labeled:
            if not is_clean(tok):
                continue
            buckets[lbl].append(tok["s2"])

        n_q = len(buckets["quoted"])
        n_u = len(buckets["unquoted"])
        if n_q < 3 or n_u < 3:
            continue

        avg_q = statistics.mean(buckets["quoted"])
        avg_u = statistics.mean(buckets["unquoted"])
        avg_a = statistics.mean(buckets["attribution"]) if buckets["attribution"] else None

        poem_stats.append({
            "title": r["metadata"]["title"],
            "author": r["metadata"]["author"],
            "era": r["metadata"]["era"],
            "avg_s2_quoted": avg_q,
            "avg_s2_unquoted": avg_u,
            "avg_s2_attribution": avg_a,
            "delta": avg_q - avg_u,
            "n_quoted": n_q,
            "n_unquoted": n_u,
            "quote_pct": 100 * n_q / (n_q + n_u),
        })

        era = r["metadata"]["era"]
        era_buckets[era]["quoted"].extend(buckets["quoted"])
        era_buckets[era]["unquoted"].extend(buckets["unquoted"])

        for lbl in ("quoted", "unquoted", "attribution"):
            global_buckets[lbl].extend(buckets[lbl])

    # Sort by delta
    poem_stats.sort(key=lambda x: x["delta"])

    # Era summary
    era_summary = []
    for era, b in era_buckets.items():
        if len(b["quoted"]) >= 5 and len(b["unquoted"]) >= 5:
            avg_q = statistics.mean(b["quoted"])
            avg_u = statistics.mean(b["unquoted"])
            era_summary.append({
                "era": era,
                "avg_s2_quoted": avg_q,
                "avg_s2_unquoted": avg_u,
                "delta": avg_q - avg_u,
                "n_quoted": len(b["quoted"]),
                "n_unquoted": len(b["unquoted"]),
            })
    era_summary.sort(key=lambda x: x["delta"])

    # Save JSON
    out = {
        "poem_stats": poem_stats,
        "era_summary": era_summary,
        "global": {
            "avg_s2_quoted": statistics.mean(global_buckets["quoted"]) if global_buckets["quoted"] else None,
            "avg_s2_unquoted": statistics.mean(global_buckets["unquoted"]) if global_buckets["unquoted"] else None,
            "avg_s2_attribution": statistics.mean(global_buckets["attribution"]) if global_buckets["attribution"] else None,
            "n_quoted": len(global_buckets["quoted"]),
            "n_unquoted": len(global_buckets["unquoted"]),
            "n_attribution": len(global_buckets["attribution"]),
        }
    }
    out_path = os.path.join(RESULTS_DIR, "dialogue_s2.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Results saved to {out_path}")
    print(f"\nPoems analyzed (quoted content ≥ 5 tokens): {len(poem_stats)}")
    print(f"\nGlobal comparison:")
    print(f"  Quoted S2:      {out['global']['avg_s2_quoted']:.3f} (n={out['global']['n_quoted']})")
    print(f"  Unquoted S2:    {out['global']['avg_s2_unquoted']:.3f} (n={out['global']['n_unquoted']})")
    print(f"  Attribution S2: {out['global']['avg_s2_attribution']:.3f} (n={out['global']['n_attribution']})")
    print(f"\nPer-poem delta (quoted - unquoted), sorted:")
    for ps in poem_stats:
        print(f"  {ps['delta']:+.3f}  {ps['title']} [{ps['era']}]")

    print(f"\nEra summary:")
    for es in era_summary:
        print(f"  {es['era']:25s} delta={es['delta']:+.3f}  q={es['avg_s2_quoted']:.3f} u={es['avg_s2_unquoted']:.3f}")


if __name__ == "__main__":
    main()
