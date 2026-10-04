"""
Inter-Token Semantic Jumps vs S2

Research question: When poets create semantic discontinuity between adjacent tokens
(a "horizontal" semantic cut), is this the same phenomenon as S2 (a "vertical"
prediction surprise)? Or do they capture different aspects of poetic deviation?

The haiku kireji study found that the post-cut token carries S2 ~ +19, suggesting
the jump and the prediction failure are aligned. But in non-haiku poetry, do poets
also use semantic jumps, and do those jumps create S2?

Method:
  For each poem, examine consecutive content-token pairs:
  1. Compute cosine distance between adjacent token GPT-2 embeddings
     → "inter-token distance" = how semantically far token[i] is from token[i-1]
  2. Classify each token by (S2 zone, inter-token distance zone)
  3. Find:
     a) r(S2, inter-token-distance) — are they correlated?
     b) "Pure semantic jumps" — high inter-token distance, low S2 (poet crossed
        fields smoothly — GPT-2 saw it coming)
     c) "Pure S2 surprises" — low inter-token distance but high S2 (prediction
        failure without semantic discontinuity — structural surprise)
     d) "Aligned surprises" — both high (the classic Straussian gap)
  4. Compare genres and poets for each category

Output: results/inter_token_semantic_jumps.json + findings/inter_token_semantic_jumps.md
"""

import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from collections import defaultdict

RESULTS_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"
OUT_JSON = Path(__file__).parent.parent / "results" / "inter_token_semantic_jumps.json"

def cosine_dist(a, b):
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(1 - np.dot(a, b))

def is_content(tok_str):
    clean = tok_str.strip()
    if not clean or clean == '\n':
        return False
    if re.match(r'^[\W_]+$', clean):
        return False
    return True

def run():
    print("Loading corpus...")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)
    print(f"  {len(corpus)} texts")

    print("Loading GPT-2...")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    wte = model.transformer.wte.weight.detach().numpy()  # [50257, 768]
    print(f"  Embedding matrix: {wte.shape}")

    def embed(tok_str):
        ids = tokenizer.encode(tok_str)
        if not ids:
            return None
        # use the first token's embedding (most tokens map to 1 subword)
        return wte[ids[0]]

    # -------------------------------------------------------------------------
    # Per-poem analysis
    # -------------------------------------------------------------------------
    poem_stats = []
    all_s2 = []
    all_dist = []
    all_meta = []  # (era, title, author)

    for text in corpus:
        meta = text.get("metadata", {})
        title = meta.get("title", "?")
        author = meta.get("author", "?")
        era = meta.get("era", "unknown")
        is_prose = era in ("control",)

        tokens = text.get("tokens", [])
        # filter stanza-break artifact (p_newline >= 0.9)
        clean = [t for t in tokens if t.get("p_newline", 0) < 0.9]
        # filter to content tokens only
        content = [t for t in clean if is_content(t["token"])]

        if len(content) < 10:
            continue

        # compute embeddings for each content token
        embs = []
        for t in content:
            e = embed(t["token"])
            embs.append(e)

        # inter-token distances (starts at index 1)
        dists = []
        for i in range(1, len(content)):
            if embs[i] is not None and embs[i-1] is not None:
                d = cosine_dist(embs[i], embs[i-1])
                dists.append(d)
            else:
                dists.append(None)

        # collect paired (s2, dist) for correlation analysis
        paired_s2 = []
        paired_dist = []
        for i in range(1, len(content)):
            if dists[i-1] is not None:
                s2 = content[i]["s2"]
                d = dists[i-1]
                paired_s2.append(s2)
                paired_dist.append(d)
                all_s2.append(s2)
                all_dist.append(d)
                all_meta.append((era, title, author, content[i]["token"], s2, d))

        if len(paired_s2) < 5:
            continue

        # poem-level stats
        arr_s2 = np.array(paired_s2)
        arr_dist = np.array(paired_dist)

        # Pearson r
        r = np.corrcoef(arr_s2, arr_dist)[0, 1] if len(arr_s2) > 2 else float('nan')

        # thresholds: use corpus-level (computed later, approximate for now)
        s2_thresh = 0.5     # above = "high S2"
        dist_thresh = 0.50  # above = "high jump" (empirically set)

        # quadrant counts
        hi_s2 = arr_s2 > s2_thresh
        hi_dist = arr_dist > dist_thresh

        n = len(arr_s2)
        q_aa = int(np.sum(~hi_s2 & ~hi_dist))  # low S2, low dist — conformist
        q_ab = int(np.sum(~hi_s2 & hi_dist))   # low S2, high dist — pure semantic jump
        q_ba = int(np.sum(hi_s2 & ~hi_dist))   # high S2, low dist — structural surprise
        q_bb = int(np.sum(hi_s2 & hi_dist))    # high S2, high dist — aligned surprise

        # top semantic jumps
        jump_pairs = sorted(
            [(dists[i-1], content[i]["s2"], content[i-1]["token"], content[i]["token"])
             for i in range(1, len(content)) if dists[i-1] is not None],
            reverse=True
        )[:3]

        poem_stats.append({
            "title": title,
            "author": author,
            "era": era,
            "is_prose": is_prose,
            "n": n,
            "mean_s2": float(np.mean(arr_s2)),
            "mean_dist": float(np.mean(arr_dist)),
            "std_dist": float(np.std(arr_dist)),
            "r_s2_dist": float(r) if not np.isnan(r) else None,
            "q_conform": q_aa,
            "q_pure_jump": q_ab,
            "q_structural": q_ba,
            "q_aligned": q_bb,
            "pct_aligned": float(q_bb / n) if n > 0 else 0,
            "top_jumps": [
                {"dist": float(d), "s2": float(s2), "prev": prev, "curr": curr}
                for d, s2, prev, curr in jump_pairs
            ],
        })

    # -------------------------------------------------------------------------
    # Global analysis
    # -------------------------------------------------------------------------
    arr_all_s2 = np.array(all_s2)
    arr_all_dist = np.array(all_dist)
    global_r = float(np.corrcoef(arr_all_s2, arr_all_dist)[0, 1])

    # use actual medians as thresholds
    s2_med = float(np.median(arr_all_s2))
    dist_med = float(np.median(arr_all_dist))

    hi_s2 = arr_all_s2 > s2_med
    hi_dist = arr_all_dist > dist_med
    N = len(arr_all_s2)
    global_q = {
        "conform": int(np.sum(~hi_s2 & ~hi_dist)),
        "pure_jump": int(np.sum(~hi_s2 & hi_dist)),
        "structural": int(np.sum(hi_s2 & ~hi_dist)),
        "aligned": int(np.sum(hi_s2 & hi_dist)),
    }

    # by era
    era_data = defaultdict(lambda: {"s2": [], "dist": [], "n_poems": 0, "is_prose": False})
    for era, title, author, tok, s2, d in all_meta:
        era_data[era]["s2"].append(s2)
        era_data[era]["dist"].append(d)
        era_data[era]["is_prose"] = era in ("control",)

    # count poems per era
    era_poem_count = defaultdict(set)
    for ps in poem_stats:
        era_poem_count[ps["era"]].add(ps["title"])

    era_stats = {}
    for era, ed in era_data.items():
        if len(ed["s2"]) < 5:
            continue
        arr_s = np.array(ed["s2"])
        arr_d = np.array(ed["dist"])
        r = np.corrcoef(arr_s, arr_d)[0, 1] if len(arr_s) > 2 else float('nan')
        era_stats[era] = {
            "n_tokens": len(arr_s),
            "n_poems": len(era_poem_count[era]),
            "mean_s2": float(np.mean(arr_s)),
            "mean_dist": float(np.mean(arr_d)),
            "r_s2_dist": float(r) if not np.isnan(r) else None,
            "is_prose": ed["is_prose"],
        }

    # top "pure jumps" — high inter-token dist, low S2
    pure_jumps = sorted(
        [(d, s2, era, tok)
         for (era, title, author, tok, s2, d) in all_meta
         if d > 0.70 and s2 < 0.0],
        reverse=True
    )[:10]

    # top "aligned surprises" — high both
    aligned = sorted(
        [(s2 + d, s2, d, era, tok)
         for (era, title, author, tok, s2, d) in all_meta
         if d > 0.65 and s2 > 3.0],
        reverse=True
    )[:10]

    # Distribution of inter-token distances
    dist_percentiles = {str(p): float(np.percentile(arr_all_dist, p))
                        for p in [10, 25, 50, 75, 90, 95]}

    output = {
        "n_texts": len(corpus),
        "n_poems_analyzed": len(poem_stats),
        "n_token_pairs": N,
        "global_r_s2_dist": global_r,
        "s2_median": float(s2_med),
        "dist_median": float(dist_med),
        "dist_percentiles": dist_percentiles,
        "global_quadrants": global_q,
        "era_stats": era_stats,
        "poem_stats": sorted(poem_stats, key=lambda x: x["mean_dist"], reverse=True)[:30],
        "top_pure_jumps": [{"dist": float(d), "s2": float(s2), "era": era, "token": tok}
                           for d, s2, era, tok in pure_jumps],
        "top_aligned_surprises": [{"score": float(sc), "s2": float(s2), "dist": float(d),
                                   "era": era, "token": tok}
                                  for sc, s2, d, era, tok in aligned],
    }

    OUT_JSON.write_text(json.dumps(output, indent=2))
    print(f"\nSaved → {OUT_JSON}")
    print(f"  N token pairs: {N}")
    print(f"  Global r(S2, inter-token dist): {global_r:.3f}")
    print(f"  Median inter-token dist: {dist_med:.3f}")
    print(f"\nQuadrant breakdown (by median thresholds):")
    for k, v in global_q.items():
        print(f"  {k}: {v} ({100*v/N:.1f}%)")

    print("\nEra mean inter-token distances (top 10):")
    sorted_eras = sorted(era_stats.items(), key=lambda x: x[1]["mean_dist"], reverse=True)[:10]
    for era, es in sorted_eras:
        marker = "(prose)" if es["is_prose"] else ""
        print(f"  {era}: mean_dist={es['mean_dist']:.3f}, r={es['r_s2_dist']:.3f} {marker}")

if __name__ == "__main__":
    run()
