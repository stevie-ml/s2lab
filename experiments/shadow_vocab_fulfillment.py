"""
Shadow Vocabulary Fulfillment
==============================
At each token position, GPT-2 predicts a top-1 "most-wanted" token.
The poet may suppress it. Does the suppressed token appear elsewhere in
the same poem? If so, the poem "fulfills" its shadow — the vocabulary the
model expected is eventually delivered, just not where the model wanted it.

This tests: do poems live inside GPT-2's vocabulary world, just rearranging
its expectations, OR do they depart entirely from the shadow text?

Metrics per poem:
  - shadow_vocab: set of unique top-1 alternatives (content words only)
  - actual_vocab: set of unique actual tokens (content words only)
  - fulfillment_rate: |shadow_vocab ∩ actual_vocab| / |shadow_vocab|
  - evasion_rate: 1 - fulfillment_rate
  - shadow_density: |shadow_vocab| / poem_length  (how rich the shadow)
  - at_high_s2: fulfillment rate restricted to high-S2 positions

The key question: do high-S2 poems have LOWER fulfillment (they build an
alien vocabulary GPT-2 never predicted) or HIGHER fulfillment (they use
the shadow words, just in unexpected positions)?
"""

import json
import re
import numpy as np
from collections import defaultdict, Counter

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/shadow_vocab_fulfillment.json"

# Stop words / function words to skip — we care about content word fulfillment
FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "was", "are", "were", "be", "been",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "it", "its", "i", "my", "me",
    "you", "your", "he", "she", "they", "we", "us", "him", "her", "them",
    "that", "this", "these", "those", "not", "no", "as", "if", "then",
    "than", "so", "yet", "also", "just", "even", "still", "only", "about",
    "into", "up", "out", "down", "off", "over", "under", "through",
    ".", ",", "!", "?", ";", ":", "'", '"', "-", "--", "...",
    "\n", " ",
}

P_NEWLINE_THRESHOLD = 0.9  # skip stanza-break artifacts
S2_HIGH_THRESHOLD = 2.0


def normalize_token(tok: str) -> str:
    """Strip leading space and lowercase."""
    return tok.strip().lower()


def is_content(tok: str) -> bool:
    """True if tok is a meaningful content word (not function/punct)."""
    t = normalize_token(tok)
    if not t or not t[0].isalpha():
        return False
    if len(t) < 3:
        return False
    return t not in FUNCTION_WORDS


def analyze_poem(poem: dict) -> dict | None:
    tokens = poem.get("tokens", [])
    if not tokens:
        return None

    meta_raw = poem.get("metadata", {})
    if isinstance(meta_raw, str):
        # Sometimes stored as string repr of dict
        try:
            import ast
            meta = ast.literal_eval(meta_raw)
        except Exception:
            meta = {}
    else:
        meta = meta_raw

    title = meta.get("title", "unknown")
    author = meta.get("author", "unknown")
    era = meta.get("era", "unknown")

    # Build set of actual content-word tokens in the poem
    actual_content = set()
    for tok in tokens:
        t = normalize_token(tok.get("token", ""))
        if is_content(t):
            actual_content.add(t)

    # Build shadow vocab: top-1 alternatives at each non-artifact position
    shadow_all = []        # all top-1 content alts
    shadow_high_s2 = []    # top-1 content alts at high-S2 positions

    for tok in tokens:
        if tok.get("p_newline", 0) >= P_NEWLINE_THRESHOLD:
            continue
        alts = tok.get("alternatives", [])
        if not alts:
            continue
        top1 = normalize_token(alts[0]["token"])
        if not is_content(top1):
            continue

        shadow_all.append(top1)
        if tok.get("s2", 0) >= S2_HIGH_THRESHOLD:
            shadow_high_s2.append(top1)

    if not shadow_all:
        return None

    shadow_vocab = set(shadow_all)
    shadow_high_vocab = set(shadow_high_s2)

    # Fulfillment: how many shadow words actually appear in the poem?
    fulfilled = shadow_vocab & actual_content
    fulfilled_high = shadow_high_vocab & actual_content

    fulfillment_rate = len(fulfilled) / len(shadow_vocab)
    fulfillment_high = (len(fulfilled_high) / len(shadow_high_vocab)
                        if shadow_high_vocab else None)

    # Shadow density: shadow vocab size relative to poem length
    shadow_density = len(shadow_vocab) / max(len(tokens), 1)

    # Overlap asymmetry: how much of ACTUAL vocab is in the shadow?
    shadow_in_actual = len(fulfilled) / max(len(actual_content), 1)

    # Top suppressed words (not in poem)
    evaded_counts = Counter(shadow_all)
    top_evaded = [(w, evaded_counts[w]) for w in shadow_vocab - actual_content]
    top_evaded.sort(key=lambda x: -x[1])

    # S2 stats
    s2_vals = [t["s2"] for t in tokens
               if t.get("p_newline", 0) < P_NEWLINE_THRESHOLD]
    avg_s2 = float(np.mean(s2_vals)) if s2_vals else 0.0

    return {
        "title": title,
        "author": author,
        "era": era,
        "poem_length": len(tokens),
        "actual_vocab_size": len(actual_content),
        "shadow_vocab_size": len(shadow_vocab),
        "shadow_density": round(shadow_density, 4),
        "fulfilled_count": len(fulfilled),
        "fulfillment_rate": round(fulfillment_rate, 4),
        "shadow_in_actual_rate": round(shadow_in_actual, 4),
        "shadow_high_vocab_size": len(shadow_high_vocab),
        "fulfillment_rate_high_s2": (round(fulfillment_high, 4)
                                     if fulfillment_high is not None else None),
        "top_evaded_words": top_evaded[:8],
        "avg_s2": round(avg_s2, 4),
    }


def main():
    print("Loading corpus…")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    print(f"Analyzing {len(corpus)} poems…")
    results = []
    for poem in corpus:
        r = analyze_poem(poem)
        if r:
            results.append(r)

    print(f"Valid poems: {len(results)}")

    # ── Global stats ──────────────────────────────────────────────────────
    fr = [r["fulfillment_rate"] for r in results]
    fr_high = [r["fulfillment_rate_high_s2"] for r in results
               if r["fulfillment_rate_high_s2"] is not None]
    sd = [r["shadow_density"] for r in results]
    s2v = [r["avg_s2"] for r in results]

    global_stats = {
        "n_poems": len(results),
        "mean_fulfillment_rate": round(float(np.mean(fr)), 4),
        "median_fulfillment_rate": round(float(np.median(fr)), 4),
        "std_fulfillment_rate": round(float(np.std(fr)), 4),
        "mean_fulfillment_high_s2": round(float(np.mean(fr_high)), 4),
        "median_fulfillment_high_s2": round(float(np.median(fr_high)), 4),
        "mean_shadow_density": round(float(np.mean(sd)), 4),
        "correlation_fulfillment_avg_s2": round(float(np.corrcoef(fr, s2v)[0, 1]), 4),
    }

    # ── Era breakdown ─────────────────────────────────────────────────────
    era_groups = defaultdict(list)
    for r in results:
        era_groups[r["era"]].append(r)

    era_stats = {}
    for era, poems in era_groups.items():
        if len(poems) < 2:
            continue
        efr = [p["fulfillment_rate"] for p in poems]
        efr_h = [p["fulfillment_rate_high_s2"] for p in poems
                 if p["fulfillment_rate_high_s2"] is not None]
        es2 = [p["avg_s2"] for p in poems]
        era_stats[era] = {
            "n": len(poems),
            "mean_fulfillment": round(float(np.mean(efr)), 4),
            "mean_fulfillment_high_s2": (round(float(np.mean(efr_h)), 4)
                                         if efr_h else None),
            "mean_avg_s2": round(float(np.mean(es2)), 4),
        }

    # Sort eras by fulfillment rate
    era_sorted = sorted(era_stats.items(), key=lambda x: -x[1]["mean_fulfillment"])

    # ── Author breakdown ──────────────────────────────────────────────────
    author_groups = defaultdict(list)
    for r in results:
        author_groups[r["author"]].append(r)

    author_stats = {}
    for author, poems in author_groups.items():
        if len(poems) < 3:
            continue
        afr = [p["fulfillment_rate"] for p in poems]
        afr_h = [p["fulfillment_rate_high_s2"] for p in poems
                 if p["fulfillment_rate_high_s2"] is not None]
        as2 = [p["avg_s2"] for p in poems]
        author_stats[author] = {
            "n": len(poems),
            "mean_fulfillment": round(float(np.mean(afr)), 4),
            "mean_fulfillment_high_s2": (round(float(np.mean(afr_h)), 4)
                                         if afr_h else None),
            "mean_avg_s2": round(float(np.mean(as2)), 4),
        }

    author_sorted = sorted(author_stats.items(),
                           key=lambda x: -x[1]["mean_fulfillment"])

    # ── Length effect ─────────────────────────────────────────────────────
    # Bin poems by length quartile
    lengths = [r["poem_length"] for r in results]
    q25, q50, q75 = np.percentile(lengths, [25, 50, 75])

    def length_bin(n):
        if n <= q25: return "short"
        elif n <= q50: return "medium-short"
        elif n <= q75: return "medium-long"
        else: return "long"

    length_groups = defaultdict(list)
    for r in results:
        length_groups[length_bin(r["poem_length"])].append(r["fulfillment_rate"])

    length_stats = {
        k: {
            "n": len(v),
            "mean_fulfillment": round(float(np.mean(v)), 4),
            "length_range": f"≤{int(q25)}" if k=="short" else
                            f"{int(q25)+1}–{int(q50)}" if k=="medium-short" else
                            f"{int(q50)+1}–{int(q75)}" if k=="medium-long" else
                            f">{int(q75)}"
        }
        for k, v in length_groups.items()
    }

    # ── Compile top evaded words globally ─────────────────────────────────
    all_evaded = Counter()
    for r in results:
        for w, c in r["top_evaded_words"]:
            all_evaded[w] += c

    output = {
        "global_stats": global_stats,
        "era_breakdown": dict(era_sorted),
        "author_breakdown": dict(author_sorted[:30]),
        "length_effect": length_stats,
        "top_globally_evaded_words": all_evaded.most_common(20),
        "poems": sorted(results,
                        key=lambda x: -x["fulfillment_rate"])[:100],
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults written to {OUTPUT_PATH}")
    print(f"\n=== GLOBAL STATS ===")
    for k, v in global_stats.items():
        print(f"  {k}: {v}")

    print(f"\n=== TOP ERAS BY FULFILLMENT RATE ===")
    for era, stats in era_sorted[:10]:
        print(f"  {era:25s} n={stats['n']:3d}  fulfillment={stats['mean_fulfillment']:.3f}  "
              f"high_s2_fulfillment={stats.get('mean_fulfillment_high_s2', 'N/A')}  "
              f"avg_s2={stats['mean_avg_s2']:.3f}")

    print(f"\n=== BOTTOM ERAS BY FULFILLMENT RATE ===")
    for era, stats in era_sorted[-10:]:
        print(f"  {era:25s} n={stats['n']:3d}  fulfillment={stats['mean_fulfillment']:.3f}  "
              f"avg_s2={stats['mean_avg_s2']:.3f}")

    print(f"\n=== TOP AUTHORS BY FULFILLMENT RATE ===")
    for author, stats in author_sorted[:10]:
        print(f"  {author:30s} n={stats['n']:3d}  fulfillment={stats['mean_fulfillment']:.3f}  "
              f"avg_s2={stats['mean_avg_s2']:.3f}")

    print(f"\n=== TOP GLOBALLY EVADED WORDS ===")
    for w, c in all_evaded.most_common(15):
        print(f"  '{w}': suppressed {c} times across corpus")

    print(f"\n=== FULFILLMENT BY POEM LENGTH ===")
    for k, v in sorted(length_stats.items(), key=lambda x: x[1]["mean_fulfillment"]):
        print(f"  {k:15s} ({v['length_range']:>8} tokens)  n={v['n']:3d}  "
              f"fulfillment={v['mean_fulfillment']:.3f}")


if __name__ == "__main__":
    main()
