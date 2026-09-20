"""
Semantic Distance in the Straussian Gap

At each high-S2 moment, how far is the poet's actual token from GPT-2's
top prediction in the model's own embedding space? Does high surprisal
(S2 > 0) mean a semantically radical substitution, or can poets achieve
high S2 through formally surprising but semantically adjacent choices?

Methodology:
- Load GPT-2's token embedding matrix (wte weights, shape [vocab, 768])
- For each high-S2 token (s2 > 1.0), get the actual token id and the
  top-1 predicted token id from the stored alternatives
- Compute cosine similarity between their embedding vectors
- Semantic distance = 1 - cosine_similarity
- Correlate S2 magnitude with semantic distance
- Compare across eras and poets

Hypothesis: High-S2 substitutions should cluster into two types:
  A) Semantically DISTANT: the poet chose something genuinely "other" in
     meaning space — a strong Straussian gap, suppressing the expected
     meaning entirely
  B) Semantically CLOSE: the poet chose a formally unlikely token that is
     nonetheless near in embedding space — same semantic field, different
     distributional behavior (e.g., a rare synonym, an inversion)

Finding either pattern would reveal something fundamental about the
mechanics of poetic deviation.
"""

import json
import os
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from collections import defaultdict
import statistics
import math

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "..", "results")


def load_results():
    with open(os.path.join(RESULTS_DIR, "corpus_results.json")) as f:
        return json.load(f)


def get_embedding_matrix():
    """Load GPT-2 and return its token embedding matrix (shape: vocab_size x 768)."""
    print("Loading GPT-2 for embedding analysis...")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    # wte = word token embeddings
    emb = model.transformer.wte.weight.detach()  # [50257, 768]
    return tokenizer, emb


def cosine_sim(v1, v2):
    return float(F.cosine_similarity(v1.unsqueeze(0), v2.unsqueeze(0)).item())


def token_to_id(tokenizer, token_str):
    """Convert a decoded token string back to its ID (first match)."""
    ids = tokenizer.encode(token_str, add_special_tokens=False)
    if ids:
        return ids[0]
    return None


def analyze_semantic_distances(results, tokenizer, emb):
    """
    For all high-S2 moments (s2 > 1.0), compute semantic distance
    between actual token and top-1 predicted token in embedding space.
    """
    all_gaps = []

    for r in results:
        era = r["metadata"]["era"]
        author = r["metadata"]["author"]
        title = r["metadata"]["title"]

        for moment in r["tokens"]:
            if moment["s2"] < 1.0:
                continue
            if not moment["alternatives"]:
                continue

            actual_token = moment["token"]
            top_pred = moment["alternatives"][0]["token"]

            actual_id = token_to_id(tokenizer, actual_token)
            pred_id = token_to_id(tokenizer, top_pred)

            if actual_id is None or pred_id is None:
                continue
            if actual_id == pred_id:
                continue  # same token — skip (shouldn't happen at high S2)

            sim = cosine_sim(emb[actual_id], emb[pred_id])
            dist = 1.0 - sim

            # Also compute distance to top-5 predictions
            top5_sims = []
            for alt in moment["alternatives"][:5]:
                alt_id = token_to_id(tokenizer, alt["token"])
                if alt_id is not None and alt_id != actual_id:
                    top5_sims.append(cosine_sim(emb[actual_id], emb[alt_id]))

            all_gaps.append({
                "era": era,
                "author": author,
                "title": title,
                "token": actual_token,
                "top_pred": top_pred,
                "s2": moment["s2"],
                "surprisal": moment["surprisal"],
                "entropy": moment["entropy"],
                "rank": moment["rank"],
                "cosine_sim": sim,
                "semantic_dist": dist,
                "top5_max_sim": max(top5_sims) if top5_sims else None,
                "context": moment.get("context_before", ""),
            })

    return all_gaps


def bin_by_s2(gaps, bins=5):
    """Divide gaps into S2 bins and report avg semantic distance per bin."""
    if not gaps:
        return []
    s2_vals = [g["s2"] for g in gaps]
    lo, hi = min(s2_vals), max(s2_vals)
    step = (hi - lo) / bins
    result = []
    for i in range(bins):
        lo_b = lo + i * step
        hi_b = lo + (i + 1) * step
        bucket = [g for g in gaps if lo_b <= g["s2"] < hi_b]
        if not bucket:
            continue
        result.append({
            "s2_range": f"{lo_b:.1f}–{hi_b:.1f}",
            "n": len(bucket),
            "avg_dist": statistics.mean(g["semantic_dist"] for g in bucket),
            "avg_sim": statistics.mean(g["cosine_sim"] for g in bucket),
        })
    return result


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return 0.0
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = math.sqrt(sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys))
    return num / den if den else 0.0


def run():
    results = load_results()
    tokenizer, emb = get_embedding_matrix()

    print("Computing semantic distances...")
    gaps = analyze_semantic_distances(results, tokenizer, emb)
    print(f"Analyzed {len(gaps)} high-S2 moments (s2 > 1.0)")

    # Overall S2 vs semantic distance correlation
    s2_vals = [g["s2"] for g in gaps]
    dist_vals = [g["semantic_dist"] for g in gaps]
    r_s2_dist = pearson_r(s2_vals, dist_vals)

    # S2 bins
    bins = bin_by_s2(gaps, bins=8)

    # By era: avg semantic distance of high-S2 moments
    era_gaps = defaultdict(list)
    for g in gaps:
        era_gaps[g["era"]].append(g)

    era_stats = {}
    for era, eg in era_gaps.items():
        era_stats[era] = {
            "n": len(eg),
            "avg_s2": statistics.mean(x["s2"] for x in eg),
            "avg_dist": statistics.mean(x["semantic_dist"] for x in eg),
            "avg_sim": statistics.mean(x["cosine_sim"] for x in eg),
            "pct_close": sum(1 for x in eg if x["semantic_dist"] < 0.15) / len(eg),
            "pct_far": sum(1 for x in eg if x["semantic_dist"] > 0.5) / len(eg),
        }

    # By author (min 20 high-S2 moments)
    author_gaps = defaultdict(list)
    for g in gaps:
        if g["era"] != "control":
            author_gaps[g["author"]].append(g)

    author_stats = {}
    for author, ag in author_gaps.items():
        if len(ag) >= 20:
            author_stats[author] = {
                "n": len(ag),
                "avg_s2": statistics.mean(x["s2"] for x in ag),
                "avg_dist": statistics.mean(x["semantic_dist"] for x in ag),
                "pct_close": sum(1 for x in ag if x["semantic_dist"] < 0.15) / len(ag),
            }

    # Extreme examples: highest S2 but closest in embedding space (unexpected)
    close_high_s2 = sorted(
        [g for g in gaps if g["era"] != "control" and g["s2"] > 3.0 and g["semantic_dist"] < 0.2],
        key=lambda g: g["s2"], reverse=True
    )[:15]

    # Extreme examples: highest S2 AND farthest in embedding space
    far_high_s2 = sorted(
        [g for g in gaps if g["era"] != "control" and g["s2"] > 3.0 and g["semantic_dist"] > 0.5],
        key=lambda g: g["s2"], reverse=True
    )[:15]

    # Overall distribution: what fraction of high-S2 moments are close vs far?
    n_total = len([g for g in gaps if g["era"] != "control"])
    n_close = len([g for g in gaps if g["era"] != "control" and g["semantic_dist"] < 0.15])
    n_mid = len([g for g in gaps if g["era"] != "control" and 0.15 <= g["semantic_dist"] < 0.4])
    n_far = len([g for g in gaps if g["era"] != "control" and g["semantic_dist"] >= 0.4])

    avg_dist_overall = statistics.mean(g["semantic_dist"] for g in gaps if g["era"] != "control")
    median_dist = sorted([g["semantic_dist"] for g in gaps if g["era"] != "control"])[n_total // 2]

    return {
        "n_total": len(gaps),
        "r_s2_dist": r_s2_dist,
        "bins": bins,
        "era_stats": era_stats,
        "author_stats": author_stats,
        "close_high_s2": close_high_s2,
        "far_high_s2": far_high_s2,
        "n_close": n_close,
        "n_mid": n_mid,
        "n_far": n_far,
        "n_total_poetry": n_total,
        "avg_dist": avg_dist_overall,
        "median_dist": median_dist,
    }


if __name__ == "__main__":
    data = run()
    print(f"\n=== SEMANTIC DISTANCE IN THE STRAUSSIAN GAP ===")
    print(f"Total high-S2 moments analyzed: {data['n_total']}")
    print(f"Pearson r (S2 vs semantic distance): {data['r_s2_dist']:.3f}")
    print(f"\nOverall distribution (poetry only, n={data['n_total_poetry']}):")
    print(f"  Close (<0.15 dist):  {data['n_close']} ({data['n_close']/data['n_total_poetry']:.1%})")
    print(f"  Mid (0.15-0.4 dist): {data['n_mid']} ({data['n_mid']/data['n_total_poetry']:.1%})")
    print(f"  Far (>0.4 dist):     {data['n_far']} ({data['n_far']/data['n_total_poetry']:.1%})")
    print(f"  Avg dist: {data['avg_dist']:.3f}, Median: {data['median_dist']:.3f}")
    print(f"\nS2 vs distance bins:")
    for b in data["bins"]:
        print(f"  S2 {b['s2_range']}: n={b['n']}, avg_dist={b['avg_dist']:.3f}")
    import json
    with open(os.path.join(RESULTS_DIR, "semantic_distance_results.json"), "w") as f:
        json.dump(data, f, indent=2, default=str)
    print("\nResults saved to results/semantic_distance_results.json")
