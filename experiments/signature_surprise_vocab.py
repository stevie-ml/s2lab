"""
Signature Surprise Vocabulary: Do poets reuse the same high-S₂ tokens
across different poems, or is their originality always fresh vocabulary?

For each poet with ≥2 poems, we extract the "surprise vocabulary" —
tokens where S₂ > SURPRISE_THRESHOLD — and measure how much vocabulary
overlaps across poems (Jaccard similarity).

Hypothesis A (Stable Signature): Famous poets have a persistent "surprise
vocabulary" they deploy repeatedly — same unexpected words across different works.

Hypothesis B (Perpetual Novelty): True originality means always surprising
with NEW vocabulary — low cross-poem overlap at high-S₂ positions.
"""

import json
import os
import re
import random
from collections import defaultdict
from itertools import combinations

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")
FINDINGS_DIR = os.path.join(os.path.dirname(__file__), "..", "findings")

SURPRISE_THRESHOLD = 2.0   # S₂ > 2.0 = clear positive Straussian gap
ARTIFACT_P = 0.90           # exclude stanza-break tokens


def normalize_token(tok):
    """Lowercase and strip leading punctuation/whitespace."""
    t = tok.lower().strip()
    t = re.sub(r"^[^a-z0-9]+", "", t)
    t = re.sub(r"[^a-z0-9]+$", "", t)
    return t


def get_surprise_vocab(poem, threshold=SURPRISE_THRESHOLD):
    """Return set of normalized high-S₂ tokens for a poem."""
    vocab = set()
    for tok in poem["tokens"]:
        p_nl = sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")
        if p_nl >= ARTIFACT_P:
            continue
        if tok["s2"] > threshold:
            w = normalize_token(tok["token"])
            if len(w) >= 2:  # skip single-char tokens
                vocab.add(w)
    return vocab


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def run():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        data = json.load(f)

    # English only, exclude control/cliche
    poems = [r for r in data
             if r["metadata"].get("language", "en") == "en"
             and r["metadata"]["era"] not in ("control", "cliche_control")]

    # Group by author
    by_author = defaultdict(list)
    for poem in poems:
        author = poem["metadata"].get("author", "Unknown")
        by_author[author].append(poem)

    # Authors with ≥2 poems
    multi = {a: ps for a, ps in by_author.items() if len(ps) >= 2}
    print(f"Authors with ≥2 poems: {len(multi)}")
    print(f"Total poems in multi-poem authors: {sum(len(ps) for ps in multi.values())}")

    # Compute per-poem surprise vocabulary
    poem_vocabs = {}  # (author, title) → set
    for author, ps in multi.items():
        for poem in ps:
            key = (author, poem["metadata"]["title"])
            poem_vocabs[key] = get_surprise_vocab(poem)

    # For each author: compute pairwise Jaccard similarities
    author_stats = {}
    for author, ps in multi.items():
        keys = [(author, p["metadata"]["title"]) for p in ps]
        vocabs = [poem_vocabs[k] for k in keys]
        sizes = [len(v) for v in vocabs]

        # Pairwise Jaccard
        pairs = list(combinations(range(len(vocabs)), 2))
        jaccards = [jaccard(vocabs[i], vocabs[j]) for i, j in pairs]
        mean_j = sum(jaccards) / len(jaccards) if jaccards else 0.0

        # Signature vocabulary = tokens appearing in ≥2 poems' surprise vocab
        all_tokens = defaultdict(int)
        for v in vocabs:
            for tok in v:
                all_tokens[tok] += 1
        signature = {tok: cnt for tok, cnt in all_tokens.items() if cnt >= 2}
        total_unique = len(set(t for v in vocabs for t in v))

        # Avg vocabulary size per poem
        avg_vocab_size = sum(sizes) / len(sizes)

        author_stats[author] = {
            "n_poems": len(ps),
            "mean_jaccard": mean_j,
            "signature_vocab": signature,
            "signature_size": len(signature),
            "total_unique_surprise": total_unique,
            "signature_ratio": len(signature) / total_unique if total_unique > 0 else 0.0,
            "avg_surprise_vocab_size": avg_vocab_size,
        }

    # Baseline: random cross-author pairs
    all_poem_keys = list(poem_vocabs.keys())
    random.seed(42)
    baseline_jaccards = []
    for _ in range(1000):
        a_key, b_key = random.sample(all_poem_keys, 2)
        if a_key[0] != b_key[0]:
            baseline_jaccards.append(jaccard(poem_vocabs[a_key], poem_vocabs[b_key]))
    baseline_mean = sum(baseline_jaccards) / len(baseline_jaccards) if baseline_jaccards else 0.0

    # Sort by mean_jaccard descending (most stable signature first)
    sorted_authors = sorted(author_stats.items(),
                            key=lambda x: x[1]["mean_jaccard"], reverse=True)

    # Build results dict
    results = {
        "baseline_cross_author_jaccard": round(baseline_mean, 4),
        "n_multi_poem_authors": len(multi),
        "authors": {
            author: {
                "n_poems": stats["n_poems"],
                "mean_jaccard": round(stats["mean_jaccard"], 4),
                "signature_size": stats["signature_size"],
                "total_unique_surprise": stats["total_unique_surprise"],
                "signature_ratio": round(stats["signature_ratio"], 4),
                "avg_surprise_vocab_size": round(stats["avg_surprise_vocab_size"], 1),
                "signature_words": sorted(stats["signature_vocab"],
                                          key=stats["signature_vocab"].__getitem__,
                                          reverse=True)[:20],
            }
            for author, stats in sorted_authors
        },
        "threshold_used": SURPRISE_THRESHOLD,
    }

    out_path = os.path.join(RESULTS_DIR, "signature_surprise_vocab.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved → {out_path}")

    # Print key results for the report
    print(f"\nBaseline cross-author Jaccard: {baseline_mean:.4f}")
    print("\nTop-10 poets by cross-poem surprise vocabulary consistency:")
    for author, stats in sorted_authors[:10]:
        print(f"  {author}: J={stats['mean_jaccard']:.4f}, "
              f"sig={stats['signature_size']}/{stats['total_unique_surprise']} "
              f"({stats['signature_ratio']*100:.0f}%), "
              f"n={stats['n_poems']}")

    print("\nBottom-10 poets (freshest surprise vocabulary each time):")
    for author, stats in sorted_authors[-10:]:
        print(f"  {author}: J={stats['mean_jaccard']:.4f}, "
              f"n={stats['n_poems']}")

    return results


if __name__ == "__main__":
    run()
