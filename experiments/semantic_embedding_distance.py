"""
Semantic Embedding Distance vs S2

Research question: Is poetic S2 driven by *semantic* surprise (the poet writes
a word from a different semantic field than expected) or *structural* surprise
(the poet writes a word from the same semantic field as expected, but the
specific choice is unexpected)?

Method:
  For each non-punctuation, non-newline content token in the corpus:
  1. Get S2, entropy from pre-computed corpus_results.json
  2. Get GPT-2's top-1 predicted token (alternatives[0])
  3. Compute cosine distance between GPT-2's input embeddings for:
       a) the actual token written
       b) the top-1 predicted token
  4. Assign to quadrant based on S2 and semantic distance:
     A. Low-S2,  Low-dist  → conformist (expected + semantically close)
     B. Low-S2,  High-dist → semantic match (expected + semantically far — odd)
     C. High-S2, Low-dist  → structural surprise (unexpected but same semantic field)
     D. High-S2, High-dist → semantic surprise (unexpected AND different semantic field)

The correlation between S2 and semantic distance tells us which dominates:
  r >> 0  → poetic surprise is mainly semantic divergence
  r ≈ 0   → structural and semantic surprise are independent
  r << 0  → high-S2 moments tend to be semantically close (structural, lexical precision)
"""

import sys, json, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
from collections import defaultdict

def cosine_sim(a, b):
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(np.dot(a, b))

def is_content_token(tok_str):
    """Return True if token is not purely punctuation, space, or newline."""
    clean = tok_str.strip()
    if not clean:
        return False
    if clean == '\n' or clean == '':
        return False
    # purely punctuation
    if re.match(r'^[\W_]+$', clean):
        return False
    return True

def run():
    results_path = Path(__file__).parent.parent / "results" / "corpus_results.json"
    print(f"Loading {results_path}...")
    with open(results_path) as f:
        corpus = json.load(f)
    print(f"  Loaded {len(corpus)} texts")

    print("Loading GPT-2 model for embeddings...")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    model.eval()

    # Input embedding matrix: shape (vocab_size, 768)
    emb_matrix = model.transformer.wte.weight.detach().numpy()
    print(f"  Embedding matrix shape: {emb_matrix.shape}")

    # Cache: token_string -> embedding (to avoid repeated tokenization)
    tok_emb_cache = {}
    def get_emb(tok_str):
        if tok_str not in tok_emb_cache:
            ids = tokenizer.encode(tok_str, add_special_tokens=False)
            if ids:
                # Use first subtoken's embedding
                tok_emb_cache[tok_str] = emb_matrix[ids[0]]
            else:
                tok_emb_cache[tok_str] = np.zeros(768)
        return tok_emb_cache[tok_str]

    all_records = []
    era_data = defaultdict(list)
    is_control = set(["control", "cliche_control"])

    for result in corpus:
        meta = result.get("metadata", {})
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        title = meta.get("title", "unknown")
        tokens = result.get("tokens", [])

        for tok in tokens:
            tok_str = tok.get("token", "")
            if not is_content_token(tok_str):
                continue
            # Skip stanza-break artifact
            if tok.get("p_newline", 0) >= 0.9:
                continue

            s2 = tok.get("s2", 0.0)
            entropy = tok.get("entropy", 0.0)
            alts = tok.get("alternatives", [])
            if not alts:
                continue

            top1_str = alts[0].get("token", "")
            if not top1_str:
                continue

            # If actual token == top-1, sem_dist = 0 by definition
            if tok_str == top1_str:
                sem_dist = 0.0
            else:
                actual_emb = get_emb(tok_str)
                pred_emb = get_emb(top1_str)
                sim = cosine_sim(actual_emb, pred_emb)
                sem_dist = 1.0 - sim

            rec = {
                "token": tok_str,
                "top1": top1_str,
                "s2": s2,
                "entropy": entropy,
                "sem_dist": sem_dist,
                "era": era,
                "author": author,
                "title": title,
                "is_control": era in is_control,
            }
            all_records.append(rec)
            era_data[era].append(rec)

    print(f"\nTotal content tokens: {len(all_records)}")

    s2_arr = np.array([r["s2"] for r in all_records])
    dist_arr = np.array([r["sem_dist"] for r in all_records])

    # Median sem_dist as threshold for quadrant assignment
    med_dist = float(np.median(dist_arr))
    print(f"Median semantic distance: {med_dist:.4f}")

    # Overall correlation
    corr = float(np.corrcoef(s2_arr, dist_arr)[0, 1])
    print(f"Pearson r(S2, sem_dist) = {corr:.4f}")

    # Correlation within poetry only (excluding controls)
    poetry = [r for r in all_records if not r["is_control"]]
    s2p = np.array([r["s2"] for r in poetry])
    dp = np.array([r["sem_dist"] for r in poetry])
    corr_poetry = float(np.corrcoef(s2p, dp)[0, 1])
    print(f"Pearson r(S2, sem_dist) [poetry only] = {corr_poetry:.4f}")

    controls = [r for r in all_records if r["is_control"]]
    s2c = np.array([r["s2"] for r in controls])
    dc = np.array([r["sem_dist"] for r in controls])
    corr_ctrl = float(np.corrcoef(s2c, dc)[0, 1]) if len(controls) > 2 else 0
    print(f"Pearson r(S2, sem_dist) [control only] = {corr_ctrl:.4f}")

    # Quadrants
    quads = {"A": [], "B": [], "C": [], "D": []}
    for r in all_records:
        hi_s2 = r["s2"] > 0.0
        hi_dist = r["sem_dist"] > med_dist
        q = {(False, False): "A", (False, True): "B",
             (True, False): "C", (True, True): "D"}[(hi_s2, hi_dist)]
        quads[q].append(r)

    print("\nQuadrant distribution (S2>0 = high; dist>median = high):")
    for q, label in [
        ("A", "Low-S2, Low-dist  (conformist)"),
        ("B", "Low-S2, High-dist (semantic match)"),
        ("C", "High-S2, Low-dist (structural surprise)"),
        ("D", "High-S2, High-dist (semantic surprise)"),
    ]:
        n = len(quads[q])
        pct = 100 * n / len(all_records)
        avg_s2 = float(np.mean([r["s2"] for r in quads[q]])) if quads[q] else 0
        avg_dist = float(np.mean([r["sem_dist"] for r in quads[q]])) if quads[q] else 0
        print(f"  {q} {label}: n={n:5d} ({pct:4.1f}%)  avg_s2={avg_s2:+.3f}  avg_dist={avg_dist:.4f}")

    # For high-S2 tokens: what fraction are semantic vs structural?
    hi_s2_all = [r for r in all_records if r["s2"] > 0]
    n_struct = sum(1 for r in hi_s2_all if r["sem_dist"] <= med_dist)
    n_sem = sum(1 for r in hi_s2_all if r["sem_dist"] > med_dist)
    print(f"\nAmong all high-S2 tokens (n={len(hi_s2_all)}):")
    print(f"  Structural (C): {n_struct} ({100*n_struct/len(hi_s2_all):.1f}%)")
    print(f"  Semantic   (D): {n_sem}   ({100*n_sem/len(hi_s2_all):.1f}%)")

    # Era breakdown
    print("\n--- Era breakdown: semantic vs structural surprise among high-S2 tokens ---")
    era_rows = []
    for era, recs in sorted(era_data.items(), key=lambda x: -len(x[1])):
        if len(recs) < 20:
            continue
        hi = [r for r in recs if r["s2"] > 0]
        if not hi:
            continue
        n_c = sum(1 for r in hi if r["sem_dist"] <= med_dist)
        n_d = sum(1 for r in hi if r["sem_dist"] > med_dist)
        avg_dist_hi = float(np.mean([r["sem_dist"] for r in hi]))
        avg_dist_all = float(np.mean([r["sem_dist"] for r in recs]))
        era_rows.append({
            "era": era, "n": len(recs), "n_hi": len(hi),
            "n_struct": n_c, "n_sem": n_d,
            "pct_struct": 100*n_c/(n_c+n_d) if (n_c+n_d) else 0,
            "avg_dist_hi": avg_dist_hi,
            "avg_dist_all": avg_dist_all,
        })

    # Sort by pct_struct descending (most structural-surprise eras first)
    era_rows_sorted = sorted(era_rows, key=lambda x: -x["pct_struct"])
    print(f"{'Era':<22} {'n':>5} {'hi-S2':>6} {'Struct%':>8} {'Sem%':>6} {'avg_dist(hi)':>13}")
    for row in era_rows_sorted:
        print(f"  {row['era']:<20} {row['n']:>5} {row['n_hi']:>6} {row['pct_struct']:>7.1f}% "
              f"{100-row['pct_struct']:>5.1f}% {row['avg_dist_hi']:>13.4f}")

    # Top examples
    print("\n--- Top 15 quadrant C (high-S2, LOW sem-dist = structural surprise) ---")
    top_c = sorted(quads["C"], key=lambda r: -r["s2"])[:15]
    for r in top_c:
        print(f"  S2={r['s2']:+.2f} dist={r['sem_dist']:.4f} | wrote '{r['token']}' expected '{r['top1']}' | {r['author']}: {r['title']}")

    print("\n--- Top 15 quadrant D (high-S2, HIGH sem-dist = semantic surprise) ---")
    top_d = sorted(quads["D"], key=lambda r: -r["s2"])[:15]
    for r in top_d:
        print(f"  S2={r['s2']:+.2f} dist={r['sem_dist']:.4f} | wrote '{r['token']}' expected '{r['top1']}' | {r['author']}: {r['title']}")

    # Average sem_dist for top 100 highest S2 tokens
    top_100 = sorted(all_records, key=lambda r: -r["s2"])[:100]
    avg_dist_top100 = float(np.mean([r["sem_dist"] for r in top_100]))
    print(f"\nAvg sem_dist for top-100 highest-S2 tokens: {avg_dist_top100:.4f}")
    print(f"  (compared to overall median: {med_dist:.4f})")

    # Save
    output = {
        "n_tokens": len(all_records),
        "median_sem_dist": med_dist,
        "correlation_all": corr,
        "correlation_poetry": corr_poetry,
        "correlation_control": corr_ctrl,
        "quadrant_counts": {q: len(v) for q, v in quads.items()},
        "quadrant_avg_s2": {q: float(np.mean([r["s2"] for r in v])) if v else 0 for q, v in quads.items()},
        "high_s2_structural_pct": 100 * n_struct / len(hi_s2_all) if hi_s2_all else 0,
        "high_s2_semantic_pct": 100 * n_sem / len(hi_s2_all) if hi_s2_all else 0,
        "avg_sem_dist_top100_s2": avg_dist_top100,
        "era_breakdown": era_rows,
        "top_structural": [
            {"s2": r["s2"], "sem_dist": r["sem_dist"], "token": r["token"],
             "top1": r["top1"], "author": r["author"], "title": r["title"]}
            for r in top_c
        ],
        "top_semantic": [
            {"s2": r["s2"], "sem_dist": r["sem_dist"], "token": r["token"],
             "top1": r["top1"], "author": r["author"], "title": r["title"]}
            for r in top_d
        ],
    }

    out_path = Path(__file__).parent.parent / "results" / "semantic_embedding_distance.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    return output

if __name__ == "__main__":
    run()
