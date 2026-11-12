"""
Surprise Cohesion: Are a Poem's High-S2 Tokens Semantically Unified?

For each poem, we ask: do the tokens that GPT-2 found most surprising
cluster together semantically, or are they scattered across unrelated
semantic domains?

If a poem's surprises are semantically COHESIVE, the poet is using
deviation to build a unified semantic thread (like a conceit or thematic
obsession). If surprises are SCATTERED, each spike is a local effect
with no global semantic program.

Method:
- Load GPT-2 token embeddings (wte matrix)
- For each poem with ≥3 clean high-S2 tokens (S2 ≥ 2.0, p_newline < 0.9),
  compute mean pairwise cosine similarity among the surprise tokens
- Compare to a baseline: mean pairwise cosine similarity among random
  same-sized subsets of the poem's ordinary tokens (S2 < 0.5)
- "Excess cohesion" = surprise cohesion - baseline cohesion

A positive score means surprise tokens are MORE semantically related
to each other than ordinary tokens; negative means MORE scattered.
"""

import json
import random
import numpy as np
from pathlib import Path
from collections import defaultdict

# ── Configuration ──────────────────────────────────────────────────────────────
S2_THRESHOLD = 2.0        # high-S2 cutoff
ORDINARY_THRESHOLD = 0.5  # "ordinary" token cutoff
MIN_SURPRISE_TOKENS = 3   # minimum high-S2 tokens to include poem
NEWLINE_PROB_CUTOFF = 0.9 # stanza-break artifact filter
N_BOOTSTRAP_SAMPLES = 10  # random samples for baseline estimation
RESULTS_PATH = Path("results/surprise_cohesion.json")
CORPUS_PATH  = Path("results/corpus_results.json")

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)

def mean_pairwise_cosine(vecs):
    """Mean cosine similarity of all distinct pairs in a list of vectors."""
    if len(vecs) < 2:
        return 0.0
    total, count = 0.0, 0
    vecs = [np.array(v) for v in vecs]
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            total += cosine_similarity(vecs[i], vecs[j])
            count += 1
    return total / count if count > 0 else 0.0

def load_embeddings():
    """Load GPT-2 token embedding matrix (wte)."""
    import torch
    from transformers import GPT2Model, GPT2Tokenizer
    print("Loading GPT-2 embeddings …")
    model = GPT2Model.from_pretrained("gpt2")
    model.eval()
    wte = model.wte.weight.detach().numpy()  # (50257, 768)
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    return wte, tokenizer

def is_content_word(token_str, pos_tag=None):
    """Rough filter: exclude pure punctuation and very common function words."""
    stripped = token_str.strip().lower().lstrip("Ġ").strip()
    if not stripped or not any(c.isalpha() for c in stripped):
        return False
    function_words = {
        "the","a","an","and","or","but","in","on","at","to","for",
        "of","with","by","from","as","it","its","is","was","are",
        "were","be","been","being","have","has","had","do","does",
        "did","will","would","could","should","may","might","shall",
        "that","this","these","those","i","you","he","she","we","they",
        "me","him","her","us","them","my","your","his","our","their",
        "what","which","who","whom","when","where","why","how","if",
        "not","no","nor","so","yet","both","either","neither","each",
        "all","any","few","more","most","other","some","such","own",
        "same","than","then","too","very","just","also","up","out",
        "about","into","through","during","before","after","above",
        "below","between","among","while","although","because","since",
    }
    return stripped not in function_words

def token_str_to_id(tok_str, tokenizer):
    """Convert a token string (from corpus) to its GPT-2 token ID.
    Returns None if the string encodes to multiple IDs or is empty."""
    ids = tokenizer.encode(tok_str, add_special_tokens=False)
    if len(ids) == 1:
        return ids[0]
    # Try with the leading Ġ prefix that GPT-2 uses for space-prefixed tokens
    return None

def analyze_poem(poem_data, wte, tokenizer, tok_cache):
    """
    Returns a dict with:
      surprise_cohesion   - mean pairwise cosine similarity of high-S2 tokens
      baseline_cohesion   - mean pairwise cosine similarity of ordinary tokens
      excess_cohesion     - surprise_cohesion - baseline_cohesion
      n_surprise          - number of high-S2 tokens used
      n_ordinary          - number of ordinary tokens available
      surprise_tokens     - list of token strings at high-S2 positions
    """
    tokens = poem_data.get("tokens", [])
    if not tokens:
        return None

    surprise_items, ordinary_items = [], []

    for t in tokens:
        s2     = t.get("s2", 0)
        p_nl   = t.get("p_newline", 0)
        tok_str = t.get("token", "")

        # stanza-break artifact filter
        if p_nl >= NEWLINE_PROB_CUTOFF:
            continue
        if not is_content_word(tok_str):
            continue

        # Get token ID via cache
        if tok_str not in tok_cache:
            ids = tokenizer.encode(tok_str, add_special_tokens=False)
            tok_cache[tok_str] = ids[0] if len(ids) == 1 else None
        tok_id = tok_cache[tok_str]
        if tok_id is None or tok_id >= len(wte):
            continue

        if s2 >= S2_THRESHOLD:
            surprise_items.append((tok_id, tok_str))
        elif s2 < ORDINARY_THRESHOLD:
            ordinary_items.append((tok_id, tok_str))

    if len(surprise_items) < MIN_SURPRISE_TOKENS:
        return None

    surprise_ids   = [x[0] for x in surprise_items]
    surprise_strs  = [x[1].strip() for x in surprise_items]
    ordinary_ids   = [x[0] for x in ordinary_items]

    # Embeddings for surprise tokens
    surprise_vecs = [wte[tid] for tid in surprise_ids]
    surprise_coh  = mean_pairwise_cosine(surprise_vecs)

    # Baseline: sample equal-size subsets from ordinary tokens (bootstrap)
    n = min(len(surprise_ids), len(ordinary_ids))
    baseline_scores = []
    if n >= 2 and ordinary_ids:
        for _ in range(N_BOOTSTRAP_SAMPLES):
            sample = random.sample(ordinary_ids, min(n, len(ordinary_ids)))
            vecs   = [wte[tid] for tid in sample]
            baseline_scores.append(mean_pairwise_cosine(vecs))
    baseline_coh = float(np.mean(baseline_scores)) if baseline_scores else 0.0

    return {
        "surprise_cohesion": round(surprise_coh, 4),
        "baseline_cohesion": round(baseline_coh, 4),
        "excess_cohesion":   round(surprise_coh - baseline_coh, 4),
        "n_surprise":        len(surprise_ids),
        "n_ordinary":        len(ordinary_ids),
        "surprise_tokens":   surprise_strs,
    }

def main():
    random.seed(42)

    print(f"Loading corpus from {CORPUS_PATH} …")
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    wte, tokenizer = load_embeddings()

    results = []
    skipped = 0
    tok_cache = {}

    for poem in corpus:
        meta   = poem.get("metadata", {})
        summ   = poem.get("summary", {})
        title  = meta.get("title", "unknown")
        author = meta.get("author", "unknown")
        era    = meta.get("era", "unknown")
        avg_s2 = summ.get("avg_s2", None)

        analysis = analyze_poem(poem, wte, tokenizer, tok_cache)
        if analysis is None:
            skipped += 1
            continue

        analysis.update({
            "title":  title,
            "author": author,
            "era":    era,
            "avg_s2": avg_s2,
        })
        results.append(analysis)

    print(f"Analyzed: {len(results)} poems  |  skipped (< {MIN_SURPRISE_TOKENS} clean high-S2): {skipped}")

    # ── Global Statistics ──────────────────────────────────────────────────────
    excess   = [r["excess_cohesion"]   for r in results]
    surprise = [r["surprise_cohesion"] for r in results]
    baseline = [r["baseline_cohesion"] for r in results]

    print(f"\n=== Global Statistics (n={len(results)}) ===")
    print(f"  Mean surprise cohesion : {np.mean(surprise):.4f}")
    print(f"  Mean baseline cohesion : {np.mean(baseline):.4f}")
    print(f"  Mean excess cohesion   : {np.mean(excess):.4f}")
    print(f"  Std excess cohesion    : {np.std(excess):.4f}")
    print(f"  % poems with positive excess cohesion: {100*sum(1 for e in excess if e > 0)/len(excess):.1f}%")

    # ── Era Analysis ───────────────────────────────────────────────────────────
    era_groups = defaultdict(list)
    for r in results:
        era_groups[r["era"]].append(r)

    print("\n=== Era Analysis (eras with ≥4 poems) ===")
    era_stats = []
    for era, poems in era_groups.items():
        if len(poems) < 4:
            continue
        exc = [p["excess_cohesion"] for p in poems]
        sc  = [p["surprise_cohesion"] for p in poems]
        era_stats.append({
            "era": era,
            "n":   len(poems),
            "mean_excess":   round(float(np.mean(exc)), 4),
            "mean_surprise": round(float(np.mean(sc)), 4),
            "std_excess":    round(float(np.std(exc)), 4),
            "pct_positive":  round(100 * sum(1 for e in exc if e > 0) / len(exc), 1),
        })
    era_stats.sort(key=lambda x: -x["mean_excess"])
    for e in era_stats:
        print(f"  {e['era']:25s}  n={e['n']:3d}  mean_excess={e['mean_excess']:+.4f}  "
              f"mean_surprise={e['mean_surprise']:.4f}  pct+={e['pct_positive']:.0f}%")

    # ── Top & Bottom Poems ─────────────────────────────────────────────────────
    results_sorted = sorted(results, key=lambda x: -x["excess_cohesion"])

    print("\n=== Most Cohesively Surprising Poems (top 10) ===")
    for r in results_sorted[:10]:
        toks = " | ".join(r["surprise_tokens"][:6])
        print(f"  [{r['excess_cohesion']:+.3f}] {r['author'][:25]} – {r['title'][:35]}  "
              f"era={r['era']}  tokens: {toks}")

    print("\n=== Most Scattered Surprising Poems (bottom 10) ===")
    for r in results_sorted[-10:]:
        toks = " | ".join(r["surprise_tokens"][:6])
        print(f"  [{r['excess_cohesion']:+.3f}] {r['author'][:25]} – {r['title'][:35]}  "
              f"era={r['era']}  tokens: {toks}")

    # ── Correlation with avg_s2 ────────────────────────────────────────────────
    paired = [(r["excess_cohesion"], r["avg_s2"]) for r in results if r["avg_s2"] is not None]
    if len(paired) >= 10:
        ex_arr = np.array([p[0] for p in paired])
        s2_arr = np.array([p[1] for p in paired])
        corr = float(np.corrcoef(ex_arr, s2_arr)[0, 1])
        print(f"\n=== Correlation: excess_cohesion × avg_s2 = {corr:.4f} ===")

    # ── Save ───────────────────────────────────────────────────────────────────
    output = {
        "metadata": {
            "n_poems_analyzed": len(results),
            "n_skipped":        skipped,
            "s2_threshold":     S2_THRESHOLD,
            "ordinary_threshold": ORDINARY_THRESHOLD,
            "min_surprise_tokens": MIN_SURPRISE_TOKENS,
        },
        "global_stats": {
            "mean_surprise_cohesion": round(float(np.mean(surprise)), 4),
            "mean_baseline_cohesion": round(float(np.mean(baseline)), 4),
            "mean_excess_cohesion":   round(float(np.mean(excess)), 4),
            "std_excess_cohesion":    round(float(np.std(excess)), 4),
            "pct_positive":           round(100 * sum(1 for e in excess if e > 0) / len(excess), 1),
        },
        "era_stats":   era_stats,
        "poems":       results_sorted,
    }
    with open(RESULTS_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {RESULTS_PATH}")

if __name__ == "__main__":
    main()
