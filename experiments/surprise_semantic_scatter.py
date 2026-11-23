"""
Surprise Semantic Scatter: Do Poets Surprise Us in One Domain or Many?

For each poem, collect all high-S2 tokens (genuine deviations, not stanza-break
artifacts). Project them into GPT-2 embedding space. Measure the mean pairwise
cosine distance among these tokens — their "semantic scatter."

Low scatter = poet deviates consistently within one semantic territory (focused surprise).
High scatter = poet deviates across many unrelated domains (scattered surprise).

Hypotheses:
- Lyric traditions (confessional, romantic) → lower scatter (thematic coherence)
- Surrealist, language poetry → higher scatter (radical unpredictability)
- Haiku → unclear (very few tokens per poem)

Builds on:
- semantic_distance_gap.md (actual vs predicted token distance)
- prediction_cluster_geometry.md (cluster escape)
- s2_arc_typology.md (poem-level arc shapes)
"""

import json
import sys
import numpy as np
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
S2_THRESHOLD = 2.0        # only genuine high-S2 moments
MIN_SPIKES = 3            # need at least 3 to compute pairwise distances
P_NEWLINE_MAX = 0.9       # stanza-break artifact filter

def cosine_distance(a, b):
    a = np.array(a, dtype=np.float32)
    b = np.array(b, dtype=np.float32)
    dot = np.dot(a, b)
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 1.0
    return float(1.0 - dot / (na * nb))

def mean_pairwise_distance(vecs):
    """Mean cosine distance among all pairs."""
    if len(vecs) < 2:
        return None
    n = len(vecs)
    total = 0.0
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            total += cosine_distance(vecs[i], vecs[j])
            count += 1
    return total / count if count > 0 else None

def load_model_embeddings():
    """Load GPT-2 token embeddings (wte matrix)."""
    try:
        from transformers import GPT2Model
        import torch
        model = GPT2Model.from_pretrained("gpt2")
        model.eval()
        # In newer transformers, wte is directly on the model
        wte_layer = model.wte if hasattr(model, 'wte') else model.transformer.wte
        wte = wte_layer.weight.detach().numpy()  # (50257, 768)
        return wte
    except Exception as e:
        print(f"Failed to load GPT-2 embeddings: {e}", file=sys.stderr)
        return None

def get_token_id(tokenizer, token_str):
    """Get token id for a string."""
    ids = tokenizer.encode(token_str, add_special_tokens=False)
    return ids[0] if ids else None

def main():
    print("Loading corpus...", file=sys.stderr)
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)
    print(f"  {len(corpus)} texts loaded", file=sys.stderr)

    print("Loading GPT-2 tokenizer and embeddings...", file=sys.stderr)
    from transformers import GPT2Tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    wte = load_model_embeddings()
    if wte is None:
        print("Cannot proceed without embeddings.", file=sys.stderr)
        sys.exit(1)
    print(f"  Embedding matrix: {wte.shape}", file=sys.stderr)

    results_by_poem = []
    results_by_era = defaultdict(list)
    results_by_author = defaultdict(list)

    poems_processed = 0
    poems_skipped_few = 0

    for poem in corpus:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        title = meta.get("title", "unknown")

        tokens = poem.get("tokens", [])

        # Collect genuine high-S2 tokens (filtered for stanza-break artifact)
        spike_tokens = [
            t for t in tokens
            if t.get("s2", 0) >= S2_THRESHOLD
            and t.get("p_newline", 0) < P_NEWLINE_MAX
        ]

        if len(spike_tokens) < MIN_SPIKES:
            poems_skipped_few += 1
            continue

        # Get embeddings for each spike token
        spike_vecs = []
        spike_texts = []
        for tok in spike_tokens:
            token_str = tok["token"]
            tid = get_token_id(tokenizer, token_str)
            if tid is not None and 0 <= tid < wte.shape[0]:
                spike_vecs.append(wte[tid])
                spike_texts.append(token_str.strip())

        if len(spike_vecs) < MIN_SPIKES:
            poems_skipped_few += 1
            continue

        scatter = mean_pairwise_distance(spike_vecs)
        if scatter is None:
            continue

        # Also compute: mean S2 of spikes, count
        mean_s2 = np.mean([t["s2"] for t in spike_tokens])
        n_spikes = len(spike_tokens)
        poem_len = len(tokens)
        spike_rate = n_spikes / poem_len if poem_len > 0 else 0

        poem_result = {
            "title": title,
            "author": author,
            "era": era,
            "scatter": scatter,
            "n_spikes": n_spikes,
            "mean_s2": mean_s2,
            "spike_rate": spike_rate,
            "poem_len": poem_len,
            "sample_spikes": spike_texts[:10],
        }
        results_by_poem.append(poem_result)
        results_by_era[era].append(scatter)
        results_by_author[author].append(scatter)
        poems_processed += 1

    print(f"  Processed {poems_processed} poems, skipped {poems_skipped_few} (< {MIN_SPIKES} spikes)", file=sys.stderr)

    # Aggregate by era
    era_stats = {}
    for era, scatters in results_by_era.items():
        if len(scatters) >= 2:
            era_stats[era] = {
                "n": len(scatters),
                "mean_scatter": float(np.mean(scatters)),
                "std_scatter": float(np.std(scatters)),
                "median_scatter": float(np.median(scatters)),
            }

    # Aggregate by author (require >= 3 poems)
    author_stats = {}
    for author, scatters in results_by_author.items():
        if len(scatters) >= 3:
            author_stats[author] = {
                "n": len(scatters),
                "mean_scatter": float(np.mean(scatters)),
                "std_scatter": float(np.std(scatters)),
                "median_scatter": float(np.median(scatters)),
            }

    # Correlation: scatter vs mean_s2
    all_scatter = [r["scatter"] for r in results_by_poem]
    all_mean_s2 = [r["mean_s2"] for r in results_by_poem]
    all_spike_rate = [r["spike_rate"] for r in results_by_poem]
    all_n_spikes = [r["n_spikes"] for r in results_by_poem]

    if len(all_scatter) >= 10:
        r_s2 = float(np.corrcoef(all_scatter, all_mean_s2)[0, 1])
        r_rate = float(np.corrcoef(all_scatter, all_spike_rate)[0, 1])
        r_len = float(np.corrcoef(all_scatter, [r["poem_len"] for r in results_by_poem])[0, 1])
    else:
        r_s2 = r_rate = r_len = None

    # Top/bottom poems by scatter
    sorted_poems = sorted(results_by_poem, key=lambda x: x["scatter"])
    lowest_scatter = sorted_poems[:5]
    highest_scatter = sorted_poems[-5:]

    output = {
        "metadata": {
            "n_poems": poems_processed,
            "s2_threshold": S2_THRESHOLD,
            "min_spikes": MIN_SPIKES,
            "p_newline_max": P_NEWLINE_MAX,
        },
        "corpus_stats": {
            "mean_scatter": float(np.mean(all_scatter)) if all_scatter else None,
            "std_scatter": float(np.std(all_scatter)) if all_scatter else None,
            "r_scatter_vs_mean_s2": r_s2,
            "r_scatter_vs_spike_rate": r_rate,
            "r_scatter_vs_poem_len": r_len,
        },
        "era_stats": era_stats,
        "author_stats": author_stats,
        "lowest_scatter_poems": lowest_scatter,
        "highest_scatter_poems": highest_scatter,
        "all_poem_results": results_by_poem,
    }

    out_path = "results/surprise_semantic_scatter.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"Results saved to {out_path}", file=sys.stderr)

    # Print summary
    print(f"\n=== SURPRISE SEMANTIC SCATTER ===")
    print(f"Poems analyzed: {poems_processed}")
    if all_scatter:
        print(f"Mean scatter (pairwise cosine dist among spike tokens): {np.mean(all_scatter):.4f}")
        print(f"Std: {np.std(all_scatter):.4f}")
        print(f"\nCorrelations:")
        print(f"  r(scatter, mean_S2)   = {r_s2:.3f}")
        print(f"  r(scatter, spike_rate) = {r_rate:.3f}")
        print(f"  r(scatter, poem_len)   = {r_len:.3f}")

    print(f"\nTop 15 eras by LOWEST scatter (focused surprise):")
    sorted_eras = sorted(era_stats.items(), key=lambda x: x[1]["mean_scatter"])
    for era, stats in sorted_eras[:15]:
        print(f"  {era:<30} n={stats['n']:3d}  mean={stats['mean_scatter']:.4f}  std={stats['std_scatter']:.4f}")

    print(f"\nTop 15 eras by HIGHEST scatter (diffuse surprise):")
    for era, stats in sorted_eras[-15:][::-1]:
        print(f"  {era:<30} n={stats['n']:3d}  mean={stats['mean_scatter']:.4f}  std={stats['std_scatter']:.4f}")

    print(f"\nLowest scatter poems (most focused surprise):")
    for p in lowest_scatter:
        print(f"  [{p['era']}] {p['author']}, \"{p['title']}\" — scatter={p['scatter']:.4f}, n_spikes={p['n_spikes']}")
        print(f"    Sample spikes: {p['sample_spikes'][:5]}")

    print(f"\nHighest scatter poems (most diffuse surprise):")
    for p in highest_scatter[::-1]:
        print(f"  [{p['era']}] {p['author']}, \"{p['title']}\" — scatter={p['scatter']:.4f}, n_spikes={p['n_spikes']}")
        print(f"    Sample spikes: {p['sample_spikes'][:5]}")

if __name__ == "__main__":
    main()
