"""
Semantic Arc Within a Poem: Does Semantic Distance Follow a Temporal Pattern?

Research question: The within_poem_type_arc.md established that S2 is front-loaded in
poetry (high Type I% early, declining toward the end). Does the inter-token semantic
distance show the same or an opposite pattern?

Two competing hypotheses:
  H1 (Semantic convergence): As a poem develops its theme, adjacent tokens become
     more semantically related (semantic distance decreases). The poem "finds its
     subject" and successive tokens stay closer in embedding space.

  H2 (Semantic crescendo): Poetry builds toward a semantic climax — the most daring
     semantic juxtapositions happen at the poem's volta or ending. Distance increases.

If H1 holds: early poetry = semantically adventurous, late poetry = semantically
  tight. This MIRRORS the S2 arc (high S2 early → conforms late).

If H2 holds: late poetry = semantically daring, while simultaneously S2 decreases.
  This would show that SEMANTIC surprise and PREDICTION surprise diverge over
  a poem's arc — the poem becomes more semantically bold even as GPT-2 learns
  to predict it.

Method:
  - For each poem with ≥30 content tokens, split into thirds
  - Compute mean inter-token cosine distance within each third
  - Compare: arc_dist = (last third dist − first third dist)
              arc_s2  = (last third mean_S2 − first third mean_S2)
  - Test for correlation between arc_dist and arc_s2
  - Aggregate by era

Output: results/semantic_arc_within_poem.json + findings/semantic_arc_within_poem.md
"""

import sys, json, re, statistics
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(__file__).parent.parent))

import torch
import numpy as np
from transformers import GPT2LMHeadModel, GPT2TokenizerFast

RESULTS_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"
OUT_JSON = Path(__file__).parent.parent / "results" / "semantic_arc_within_poem.json"
FINDINGS_PATH = Path(__file__).parent.parent / "findings" / "semantic_arc_within_poem.md"
MIN_CONTENT_TOKENS = 30


def cosine_dist(a, b):
    a = a / (np.linalg.norm(a) + 1e-9)
    b = b / (np.linalg.norm(b) + 1e-9)
    return float(1 - np.dot(a, b))


def is_content(tok_str):
    clean = tok_str.strip()
    if not clean or clean == "\n":
        return False
    if re.match(r"^[\W_]+$", clean):
        return False
    return True


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    return alts[0]["token"] in ("\n", "\r\n", "\r") and alts[0]["prob"] >= 0.9


def run():
    print("Loading corpus...")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)
    print(f"  {len(corpus)} texts")

    print("Loading GPT-2 embeddings...")
    tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    wte = model.transformer.wte.weight.detach().numpy()  # [50257, 768]
    print(f"  Embedding matrix: {wte.shape}")

    def embed(tok_str):
        ids = tokenizer.encode(tok_str)
        if not ids:
            return None
        return wte[ids[0]]

    poem_arcs = []
    skipped = 0

    for text in corpus:
        meta = text.get("metadata", {})
        title = meta.get("title", "?")
        author = meta.get("author", "?")
        era = meta.get("era", "unknown")

        tokens = text.get("tokens", [])
        # Remove stanza-break artifacts
        clean = [t for t in tokens if not is_artifact(t)]
        # Keep only content tokens
        content = [t for t in clean if is_content(t["token"])]

        if len(content) < MIN_CONTENT_TOKENS:
            skipped += 1
            continue

        # Compute embeddings
        embs = [embed(t["token"]) for t in content]

        # Compute inter-token distances (paired: i vs i-1)
        pairs = []
        for i in range(1, len(content)):
            if embs[i] is not None and embs[i - 1] is not None:
                d = cosine_dist(embs[i], embs[i - 1])
                s2 = content[i]["s2"]
                pairs.append((i, d, s2))

        if len(pairs) < MIN_CONTENT_TOKENS - 1:
            skipped += 1
            continue

        # Split into thirds by index within pairs list
        n = len(pairs)
        t1 = pairs[: n // 3]
        t2 = pairs[n // 3 : 2 * n // 3]
        t3 = pairs[2 * n // 3 :]

        def thirds_stats(subset):
            if not subset:
                return None
            dists = [d for _, d, _ in subset]
            s2s = [s for _, _, s in subset]
            return {
                "mean_dist": float(np.mean(dists)),
                "mean_s2": float(np.mean(s2s)),
                "n": len(subset),
            }

        s1 = thirds_stats(t1)
        s2_thirds = thirds_stats(t2)
        s3 = thirds_stats(t3)
        if not (s1 and s2_thirds and s3):
            skipped += 1
            continue

        arc_dist = s3["mean_dist"] - s1["mean_dist"]
        arc_s2 = s3["mean_s2"] - s1["mean_s2"]

        poem_arcs.append({
            "title": title,
            "author": author,
            "era": era,
            "is_prose": era == "control",
            "n_pairs": n,
            "first": s1,
            "middle": s2_thirds,
            "last": s3,
            "arc_dist": round(arc_dist, 4),
            "arc_s2": round(arc_s2, 4),
        })

    print(f"\nPoems analyzed: {len(poem_arcs)}, skipped: {skipped}")

    # --------------------------------------------------------------------------
    # Global arc analysis
    # --------------------------------------------------------------------------
    poetry = [p for p in poem_arcs if not p["is_prose"]]
    prose = [p for p in poem_arcs if p["is_prose"]]

    print("\n--- Global Arc (all poetry, thirds) ---")
    for key, label in [("first", "1st third"), ("middle", "2nd third"), ("last", "3rd third")]:
        dists = [p[key]["mean_dist"] for p in poetry]
        s2s = [p[key]["mean_s2"] for p in poetry]
        print(f"  {label}: mean_dist={np.mean(dists):.4f}  mean_S2={np.mean(s2s):.4f}")

    arc_dists = [p["arc_dist"] for p in poetry]
    arc_s2s = [p["arc_s2"] for p in poetry]
    pct_dist_increase = sum(1 for x in arc_dists if x > 0) / len(arc_dists)
    pct_s2_increase = sum(1 for x in arc_s2s if x > 0) / len(arc_s2s)
    mean_arc_dist = float(np.mean(arc_dists))
    mean_arc_s2 = float(np.mean(arc_s2s))
    r_arc = float(np.corrcoef(arc_dists, arc_s2s)[0, 1])

    print(f"\n  Mean arc_dist (last−first): {mean_arc_dist:+.4f}")
    print(f"  Mean arc_S2 (last−first): {mean_arc_s2:+.4f}")
    print(f"  % poems with dist INCREASE (first→last): {100*pct_dist_increase:.1f}%")
    print(f"  % poems with S2 INCREASE (first→last): {100*pct_s2_increase:.1f}%")
    print(f"  r(arc_dist, arc_S2): {r_arc:+.3f}")

    # --------------------------------------------------------------------------
    # Era-level analysis
    # --------------------------------------------------------------------------
    era_data = defaultdict(list)
    for p in poetry:
        era_data[p["era"]].append(p)

    era_rows = []
    for era, poems in era_data.items():
        if len(poems) < 2:
            continue
        mean_d1 = np.mean([p["first"]["mean_dist"] for p in poems])
        mean_d3 = np.mean([p["last"]["mean_dist"] for p in poems])
        mean_s2_1 = np.mean([p["first"]["mean_s2"] for p in poems])
        mean_s2_3 = np.mean([p["last"]["mean_s2"] for p in poems])
        arc_d = float(mean_d3 - mean_d1)
        arc_s = float(mean_s2_3 - mean_s2_1)
        era_rows.append({
            "era": era,
            "n": len(poems),
            "dist_first": round(float(mean_d1), 4),
            "dist_last": round(float(mean_d3), 4),
            "arc_dist": round(arc_d, 4),
            "arc_s2": round(arc_s, 4),
            "pct_dist_increase": round(100 * sum(1 for p in poems if p["arc_dist"] > 0) / len(poems), 1),
        })

    era_rows.sort(key=lambda r: r["arc_dist"])  # most convergent first

    print("\n--- Per-Era Arc (sorted by arc_dist, most convergent first) ---")
    print(f"{'Era':<22}  {'N':>3}  {'d1':>6}  {'d3':>6}  {'Δdist':>7}  {'ΔS2':>7}  {'%↑dist':>7}")
    for r in era_rows:
        print(f"  {r['era']:<20}  {r['n']:>3}  {r['dist_first']:.4f}  "
              f"{r['dist_last']:.4f}  {r['arc_dist']:+.4f}  "
              f"{r['arc_s2']:+.4f}  {r['pct_dist_increase']:>5.1f}%")

    # --------------------------------------------------------------------------
    # Top poems: strongest convergence vs crescendo
    # --------------------------------------------------------------------------
    poetry_sorted_dist = sorted(poetry, key=lambda p: p["arc_dist"])
    convergent = poetry_sorted_dist[:10]   # most decreasing distance
    crescendo = poetry_sorted_dist[-10:]   # most increasing distance
    crescendo.reverse()

    print("\n--- Top 10 Semantic CONVERGENCE poems (distance decreases most) ---")
    for p in convergent:
        print(f"  {p['arc_dist']:+.4f}  [d1={p['first']['mean_dist']:.3f}→d3={p['last']['mean_dist']:.3f}]  "
              f"{p['author']}: '{p['title']}'  ({p['era']}, n={p['n_pairs']})")

    print("\n--- Top 10 Semantic CRESCENDO poems (distance increases most) ---")
    for p in crescendo:
        print(f"  {p['arc_dist']:+.4f}  [d1={p['first']['mean_dist']:.3f}→d3={p['last']['mean_dist']:.3f}]  "
              f"{p['author']}: '{p['title']}'  ({p['era']}, n={p['n_pairs']})")

    # --------------------------------------------------------------------------
    # Interesting quadrants: (arc_dist, arc_s2)
    # --------------------------------------------------------------------------
    print("\n--- Quadrant analysis (arc_dist vs arc_s2) ---")
    quad_counts = {"converge+conform": 0, "converge+deviate": 0,
                   "crescendo+conform": 0, "crescendo+deviate": 0}
    for p in poetry:
        dist_up = p["arc_dist"] > 0
        s2_up = p["arc_s2"] > 0
        if not dist_up and not s2_up:
            quad_counts["converge+conform"] += 1
        elif not dist_up and s2_up:
            quad_counts["converge+deviate"] += 1
        elif dist_up and not s2_up:
            quad_counts["crescendo+conform"] += 1
        else:
            quad_counts["crescendo+deviate"] += 1

    for q, n in quad_counts.items():
        print(f"  {q}: {n} ({100*n/len(poetry):.1f}%)")

    # --------------------------------------------------------------------------
    # Save output
    # --------------------------------------------------------------------------
    output = {
        "n_poems": len(poem_arcs),
        "n_poetry": len(poetry),
        "n_prose": len(prose),
        "corpus_thirds": {
            key: {
                "mean_dist": round(float(np.mean([p[key]["mean_dist"] for p in poetry])), 4),
                "mean_s2": round(float(np.mean([p[key]["mean_s2"] for p in poetry])), 4),
            }
            for key in ("first", "middle", "last")
        },
        "mean_arc_dist": round(mean_arc_dist, 4),
        "mean_arc_s2": round(mean_arc_s2, 4),
        "pct_dist_increase": round(100 * pct_dist_increase, 1),
        "pct_s2_increase": round(100 * pct_s2_increase, 1),
        "r_arc_dist_arc_s2": round(r_arc, 4),
        "era_rows": era_rows,
        "top_convergent": [
            {"title": p["title"], "author": p["author"], "era": p["era"],
             "arc_dist": p["arc_dist"], "arc_s2": p["arc_s2"],
             "d1": p["first"]["mean_dist"], "d3": p["last"]["mean_dist"]}
            for p in convergent
        ],
        "top_crescendo": [
            {"title": p["title"], "author": p["author"], "era": p["era"],
             "arc_dist": p["arc_dist"], "arc_s2": p["arc_s2"],
             "d1": p["first"]["mean_dist"], "d3": p["last"]["mean_dist"]}
            for p in crescendo
        ],
        "quadrants": {k: {"n": v, "pct": round(100 * v / len(poetry), 1)}
                      for k, v in quad_counts.items()},
    }
    OUT_JSON.write_text(json.dumps(output, indent=2))
    print(f"\nSaved → {OUT_JSON}")
    return output


if __name__ == "__main__":
    result = run()
