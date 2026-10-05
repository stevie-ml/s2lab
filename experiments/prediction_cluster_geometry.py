"""
Prediction Cluster Geometry at High-S2 Moments

Research question: When a poet achieves maximum surprise (high S2), what is the
*geometry* of the semantic space they departed from?

Specifically: at each high-S2 position, the model was confident (low entropy)
but wrong. GPT-2's top-K predictions form a cluster in embedding space. We ask:

  1. How *tight* is that cluster? (intra-cluster variance)
  2. How far did the poet escape? (actual token distance from cluster centroid)
  3. What is the *direction* of escape — toward abstraction, concreteness, etc.?

We define two key metrics:
  - cluster_spread: mean pairwise cosine distance between top-K predictions
    High spread = model was unsure in many directions
    Low spread = model was confident within a tight semantic region
  - centroid_escape: cosine distance between actual token and centroid of top-K

Key hypothesis: **Tight-cluster escapes** (low spread, high centroid_escape)
are the most "Straussian" moments — the poet escapes a clearly-expected semantic
zone. These should be more frequent in poetry than prose.

We also compute a "surprise efficiency" metric:
  escape_efficiency = centroid_escape / (1 + cluster_spread)
  Higher when the poet escapes a tight cluster (most artistically significant).

Compare across eras, authors, and S2 level.
"""

import sys, json, re, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from collections import defaultdict

def cosine_dist(a, b):
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return 1.0 - float(np.dot(a, b))

def cosine_sim(a, b):
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))

def is_content_token(tok_str):
    clean = tok_str.strip()
    if not clean or clean == '\n':
        return False
    if re.match(r'^[\W_]+$', clean):
        return False
    return True

def run():
    results_path = Path(__file__).parent.parent / "results" / "corpus_results.json"
    print(f"Loading corpus from {results_path}...")
    with open(results_path) as f:
        corpus = json.load(f)
    print(f"  {len(corpus)} texts")

    print("Loading GPT-2 embeddings...")
    from transformers import GPT2LMHeadModel, GPT2TokenizerFast
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    model.eval()
    emb_matrix = model.transformer.wte.weight.detach().numpy()  # (50257, 768)
    print(f"  Embedding matrix: {emb_matrix.shape}")

    def get_emb(tok_str):
        ids = tokenizer.encode(tok_str, add_special_tokens=False)
        if ids:
            return emb_matrix[ids[0]]
        return np.zeros(768)

    # Per-text records
    text_records = []
    # All token records (for global analysis)
    all_tokens = []

    for text in corpus:
        meta = text["metadata"]
        tokens = text.get("tokens", [])
        if not tokens:
            continue

        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        title = meta.get("title", "unknown")
        is_prose = era in ("control",)

        token_records = []
        for tok in tokens:
            tok_str = tok.get("token", "")
            s2 = tok.get("s2", 0.0)
            entropy = tok.get("entropy", 0.0)
            surprisal = tok.get("surprisal", 0.0)
            p_newline = tok.get("p_newline", 0.0)
            alts = tok.get("alternatives", [])

            # Skip stanza-break artifact tokens
            if p_newline >= 0.9:
                continue
            # Skip non-content tokens
            if not is_content_token(tok_str):
                continue
            # Need at least 5 alternatives
            if len(alts) < 5:
                continue

            # Get top-K (up to 10) alternative embeddings
            K = min(10, len(alts))
            alt_embs = []
            alt_tokens = []
            for a in alts[:K]:
                at = a.get("token", "")
                e = get_emb(at)
                alt_embs.append(e)
                alt_tokens.append(at)

            alt_embs = np.array(alt_embs)  # (K, 768)

            # Cluster centroid
            centroid = alt_embs.mean(axis=0)  # (768,)

            # Cluster spread: mean pairwise cosine distance
            pairwise_dists = []
            for i in range(K):
                for j in range(i+1, K):
                    pairwise_dists.append(cosine_dist(alt_embs[i], alt_embs[j]))
            cluster_spread = float(np.mean(pairwise_dists)) if pairwise_dists else 0.0

            # Actual token distance from centroid
            actual_emb = get_emb(tok_str)
            centroid_escape = cosine_dist(actual_emb, centroid)

            # Distance from top-1 prediction
            top1_dist = cosine_dist(actual_emb, alt_embs[0])

            # "Escape efficiency": normalized by cluster spread
            # High when poet escapes a tight cluster (high surprise utility)
            escape_efficiency = centroid_escape / (1.0 + cluster_spread)

            rec = {
                "era": era,
                "author": author,
                "title": title,
                "is_prose": is_prose,
                "token": tok_str,
                "s2": s2,
                "entropy": entropy,
                "surprisal": surprisal,
                "cluster_spread": cluster_spread,
                "centroid_escape": centroid_escape,
                "top1_dist": top1_dist,
                "escape_efficiency": escape_efficiency,
                "top1_token": alt_tokens[0] if alt_tokens else "",
            }
            token_records.append(rec)
            all_tokens.append(rec)

        if token_records:
            text_records.append({
                "era": era,
                "author": author,
                "title": title,
                "is_prose": is_prose,
                "n_tokens": len(token_records),
                "avg_s2": float(np.mean([r["s2"] for r in token_records])),
                "avg_cluster_spread": float(np.mean([r["cluster_spread"] for r in token_records])),
                "avg_centroid_escape": float(np.mean([r["centroid_escape"] for r in token_records])),
                "avg_escape_efficiency": float(np.mean([r["escape_efficiency"] for r in token_records])),
                # For high-S2 tokens specifically (s2 > 2)
                "high_s2_tokens": [r for r in token_records if r["s2"] > 2.0],
            })

        print(f"  Processed: {title[:40]} ({era}) — {len(token_records)} tokens")

    # ── Global analysis ──────────────────────────────────────────────────────
    print(f"\nTotal content tokens analyzed: {len(all_tokens)}")

    # Correlation: S2 vs centroid_escape
    s2_vals = np.array([r["s2"] for r in all_tokens])
    escape_vals = np.array([r["centroid_escape"] for r in all_tokens])
    spread_vals = np.array([r["cluster_spread"] for r in all_tokens])
    eff_vals = np.array([r["escape_efficiency"] for r in all_tokens])

    r_s2_escape = float(np.corrcoef(s2_vals, escape_vals)[0, 1])
    r_s2_spread = float(np.corrcoef(s2_vals, spread_vals)[0, 1])
    r_spread_escape = float(np.corrcoef(spread_vals, escape_vals)[0, 1])

    print(f"\nCorrelations:")
    print(f"  r(S2, centroid_escape) = {r_s2_escape:.3f}")
    print(f"  r(S2, cluster_spread)  = {r_s2_spread:.3f}")
    print(f"  r(spread, escape)      = {r_spread_escape:.3f}")

    # ── Bucket analysis by S2 quintile ────────────────────────────────────
    quintiles = np.percentile(s2_vals, [0, 20, 40, 60, 80, 100])
    print(f"\nS2 quintile buckets:")
    print(f"{'S2 range':<18} {'n':>6} {'spread':>10} {'escape':>10} {'efficiency':>12}")
    print("-" * 60)
    for i in range(5):
        lo, hi = quintiles[i], quintiles[i+1]
        mask = (s2_vals >= lo) & (s2_vals <= hi)
        bucket = [all_tokens[j] for j in range(len(all_tokens)) if mask[j]]
        if bucket:
            sp = np.mean([r["cluster_spread"] for r in bucket])
            es = np.mean([r["centroid_escape"] for r in bucket])
            ef = np.mean([r["escape_efficiency"] for r in bucket])
            print(f"  [{lo:6.2f}, {hi:6.2f}]  {len(bucket):>6}  {sp:>10.4f}  {es:>10.4f}  {ef:>12.4f}")

    # ── Poetry vs prose ──────────────────────────────────────────────────
    poetry_toks = [r for r in all_tokens if not r["is_prose"]]
    prose_toks = [r for r in all_tokens if r["is_prose"]]
    print(f"\nPoetry vs Prose (all content tokens):")
    print(f"  Poetry  n={len(poetry_toks)}: spread={np.mean([r['cluster_spread'] for r in poetry_toks]):.4f}, "
          f"escape={np.mean([r['centroid_escape'] for r in poetry_toks]):.4f}, "
          f"efficiency={np.mean([r['escape_efficiency'] for r in poetry_toks]):.4f}")
    print(f"  Prose   n={len(prose_toks)}: spread={np.mean([r['cluster_spread'] for r in prose_toks]):.4f}, "
          f"escape={np.mean([r['centroid_escape'] for r in prose_toks]):.4f}, "
          f"efficiency={np.mean([r['escape_efficiency'] for r in prose_toks]):.4f}")

    # Among high-S2 tokens (s2 > 2)
    poetry_high = [r for r in poetry_toks if r["s2"] > 2.0]
    prose_high = [r for r in prose_toks if r["s2"] > 2.0]
    if poetry_high and prose_high:
        print(f"\n  High-S2 (>2) only:")
        print(f"  Poetry  n={len(poetry_high)}: spread={np.mean([r['cluster_spread'] for r in poetry_high]):.4f}, "
              f"escape={np.mean([r['centroid_escape'] for r in poetry_high]):.4f}, "
              f"efficiency={np.mean([r['escape_efficiency'] for r in poetry_high]):.4f}")
        print(f"  Prose   n={len(prose_high)}: spread={np.mean([r['cluster_spread'] for r in prose_high]):.4f}, "
              f"escape={np.mean([r['centroid_escape'] for r in prose_high]):.4f}, "
              f"efficiency={np.mean([r['escape_efficiency'] for r in prose_high]):.4f}")

    # ── Tight-cluster escapes ────────────────────────────────────────────
    # Tight escape: cluster_spread < median AND centroid_escape > median AND s2 > 2
    spread_median = float(np.median(spread_vals))
    escape_median = float(np.median(escape_vals))
    tight_escapes = [r for r in all_tokens if
                     r["cluster_spread"] < spread_median and
                     r["centroid_escape"] > escape_median and
                     r["s2"] > 2.0]
    diffuse_escapes = [r for r in all_tokens if
                       r["cluster_spread"] > spread_median and
                       r["centroid_escape"] > escape_median and
                       r["s2"] > 2.0]

    print(f"\n'Tight cluster' escapes (spread<med, escape>med, S2>2): {len(tight_escapes)}")
    print(f"'Diffuse cluster' escapes (spread>med, escape>med, S2>2): {len(diffuse_escapes)}")

    if tight_escapes:
        pct_poetry_tight = sum(1 for r in tight_escapes if not r["is_prose"]) / len(tight_escapes)
        pct_poetry_diffuse = sum(1 for r in diffuse_escapes if not r["is_prose"]) / len(diffuse_escapes) if diffuse_escapes else 0
        print(f"  Tight escapes — % poetry: {pct_poetry_tight:.1%}")
        print(f"  Diffuse escapes — % poetry: {pct_poetry_diffuse:.1%}")

    # ── Top tight-cluster escapes (most "Straussian") ──────────────────
    tight_escapes_sorted = sorted(tight_escapes, key=lambda r: r["escape_efficiency"], reverse=True)
    print(f"\nTop 15 'Straussian' tight-cluster escapes (by efficiency):")
    print(f"{'Token':<15} {'Expected':<15} {'S2':>7} {'Spread':>7} {'Escape':>7} {'Effic.':>7} {'Author/Title':<40}")
    print("-"*95)
    for r in tight_escapes_sorted[:15]:
        print(f"  {r['token']:<13} {r['top1_token']:<13} {r['s2']:>7.2f} "
              f"{r['cluster_spread']:>7.4f} {r['centroid_escape']:>7.4f} "
              f"{r['escape_efficiency']:>7.4f}  {r['author'][:20]}/{r['title'][:17]}")

    # ── Era comparison ────────────────────────────────────────────────────
    era_data = defaultdict(list)
    for r in all_tokens:
        if not r["is_prose"]:
            era_data[r["era"]].append(r)

    era_rows = []
    for era, recs in era_data.items():
        if len(recs) < 50:
            continue
        high_recs = [r for r in recs if r["s2"] > 2.0]
        era_rows.append({
            "era": era,
            "n": len(recs),
            "n_high": len(high_recs),
            "avg_spread": float(np.mean([r["cluster_spread"] for r in recs])),
            "avg_escape": float(np.mean([r["centroid_escape"] for r in recs])),
            "avg_efficiency": float(np.mean([r["escape_efficiency"] for r in recs])),
            "high_spread": float(np.mean([r["cluster_spread"] for r in high_recs])) if high_recs else 0,
            "high_escape": float(np.mean([r["centroid_escape"] for r in high_recs])) if high_recs else 0,
            "high_efficiency": float(np.mean([r["escape_efficiency"] for r in high_recs])) if high_recs else 0,
        })

    era_rows.sort(key=lambda x: x["high_efficiency"], reverse=True)
    print(f"\nEra comparison (n_tokens >= 50), sorted by high-S2 escape efficiency:")
    print(f"{'Era':<22} {'n':>5} {'n_hi':>5} {'spread':>8} {'escape':>8} {'effic.':>8}")
    print("-"*60)
    for row in era_rows:
        print(f"  {row['era']:<20} {row['n']:>5} {row['n_high']:>5}  "
              f"{row['high_spread']:>8.4f}  {row['high_escape']:>8.4f}  {row['high_efficiency']:>8.4f}")

    # ── Author comparison ─────────────────────────────────────────────────
    author_data = defaultdict(list)
    for r in all_tokens:
        if not r["is_prose"]:
            author_data[r["author"]].append(r)

    author_rows = []
    for author, recs in author_data.items():
        if len(recs) < 80:
            continue
        high_recs = [r for r in recs if r["s2"] > 2.0]
        if not high_recs:
            continue
        author_rows.append({
            "author": author,
            "n": len(recs),
            "n_high": len(high_recs),
            "high_efficiency": float(np.mean([r["escape_efficiency"] for r in high_recs])),
            "high_spread": float(np.mean([r["cluster_spread"] for r in high_recs])),
            "high_escape": float(np.mean([r["centroid_escape"] for r in high_recs])),
        })

    author_rows.sort(key=lambda x: x["high_efficiency"], reverse=True)
    print(f"\nAuthor comparison (n_tokens >= 80), sorted by high-S2 escape efficiency:")
    print(f"{'Author':<25} {'n':>5} {'n_hi':>5} {'spread':>8} {'escape':>8} {'effic.':>8}")
    print("-"*65)
    for row in author_rows[:15]:
        print(f"  {row['author']:<23} {row['n']:>5} {row['n_high']:>5}  "
              f"{row['high_spread']:>8.4f}  {row['high_escape']:>8.4f}  {row['high_efficiency']:>8.4f}")

    # ── Save results ──────────────────────────────────────────────────────
    output = {
        "n_tokens": len(all_tokens),
        "correlations": {
            "r_s2_centroid_escape": r_s2_escape,
            "r_s2_cluster_spread": r_s2_spread,
            "r_spread_escape": r_spread_escape,
        },
        "spread_median": spread_median,
        "escape_median": escape_median,
        "n_tight_escapes": len(tight_escapes),
        "n_diffuse_escapes": len(diffuse_escapes),
        "era_rows": era_rows,
        "author_rows": author_rows,
        "top_straussian": [
            {k: v for k, v in r.items() if k != "is_prose"}
            for r in tight_escapes_sorted[:30]
        ],
    }
    out_path = Path(__file__).parent.parent / "results" / "prediction_cluster_geometry.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")

if __name__ == "__main__":
    run()
