"""
Cross-model comparison: GPT-2 small vs GPT-2 medium.

Research question: Does a more capable model (GPT-2 medium) 'understand' poetry better
— i.e., does it predict poetic choices with higher probability, lowering S2?
Or do poets remain equally 'Straussian' against a smarter model?

S2 = surprisal - entropy.
A lower S2 with the larger model means the model has 'caught up' to the poet.
A similar S2 means the poet's choices are irreducibly surprising — they resist
even a better language model.
"""

import sys
import os
import torch
import torch.nn.functional as F
import math
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from corpus.poems import POEMS

MODELS = {
    "gpt2-small": "gpt2",
    "gpt2-medium": "gpt2-medium",
}

# Use a subset of poems that represent the corpus well
SELECTED = [
    "Because I could not stop for Death",
    "The Love Song of J. Alfred Prufrock (opening)",
    "The Red Wheelbarrow",
    "Howl (opening)",
    "The Road Not Taken",
    "Ode to a Nightingale (stanza 1)",
    "Diving into the Wreck (excerpt)",
    "Thirteen Ways of Looking at a Blackbird (I-III)",
]


def load_model(model_name):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    print(f"  Loading {model_name}...", flush=True)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    model.eval()
    return model, tokenizer


def analyze_text(text, model, tokenizer):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    tokens = [tokenizer.decode([t]) for t in input_ids[0]]

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits

    results = []
    for i in range(len(tokens) - 1):
        token_logits = logits[0, i, :]
        probs = F.softmax(token_logits, dim=-1)
        log_probs = F.log_softmax(token_logits, dim=-1)

        actual_id = input_ids[0, i + 1].item()
        surprisal = -log_probs[actual_id].item() / math.log(2)
        entropy = -(probs * log_probs).sum().item() / math.log(2)
        s2 = surprisal - entropy
        prob = probs[actual_id].item()

        topk_probs, topk_ids = torch.topk(probs, 5)
        top5 = [tokenizer.decode([tid.item()]) for tid in topk_ids]

        results.append({
            "token": tokens[i + 1],
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "prob": round(prob, 6),
            "top5": top5,
        })
    return results


def poem_stats(token_data):
    n = len(token_data)
    avg_s = sum(t["surprisal"] for t in token_data) / n
    avg_e = sum(t["entropy"] for t in token_data) / n
    avg_s2 = sum(t["s2"] for t in token_data) / n
    pos_ratio = sum(1 for t in token_data if t["s2"] > 0) / n
    top_s2 = sorted(token_data, key=lambda t: t["s2"], reverse=True)[:3]
    return {
        "avg_surprisal": round(avg_s, 3),
        "avg_entropy": round(avg_e, 3),
        "avg_s2": round(avg_s2, 3),
        "pos_s2_ratio": round(pos_ratio, 3),
        "top_s2_tokens": [(t["token"].strip(), round(t["s2"], 2), t["top5"][0]) for t in top_s2],
    }


def run():
    selected_poems = [p for p in POEMS if p["title"] in SELECTED]
    if not selected_poems:
        print("No matching poems found in corpus. Using first 8 poems instead.")
        selected_poems = POEMS[:8]

    loaded_models = {}
    for label, model_name in MODELS.items():
        print(f"\nLoading {label} ({model_name})...")
        loaded_models[label] = load_model(model_name)

    all_results = {}
    print("\nAnalyzing poems...")
    for poem in selected_poems:
        title = poem["title"]
        text = poem["text"]
        print(f"  {title}")
        all_results[title] = {
            "author": poem.get("author", ""),
            "era": poem.get("era", ""),
            "models": {}
        }
        for label, (model, tokenizer) in loaded_models.items():
            token_data = analyze_text(text, model, tokenizer)
            all_results[title]["models"][label] = poem_stats(token_data)

    return all_results


def print_comparison_table(results):
    print("\n" + "=" * 90)
    print("CROSS-MODEL COMPARISON: GPT-2 Small vs Medium")
    print("=" * 90)

    print(f"\n{'Poem':<42} {'Model':<14} {'Surprisal':>10} {'Entropy':>9} {'S2':>7} {'+S2%':>6}")
    print("-" * 90)

    s2_deltas = []
    surprisal_deltas = []
    entropy_deltas = []

    for title, data in results.items():
        short = title[:38] + ".." if len(title) > 40 else title
        for model_label, stats in data["models"].items():
            print(f"  {short:<40} {model_label:<14} {stats['avg_surprisal']:>10.3f} "
                  f"{stats['avg_entropy']:>9.3f} {stats['avg_s2']:>7.3f} "
                  f"{stats['pos_s2_ratio']*100:>5.1f}%")

        small = data["models"].get("gpt2-small")
        medium = data["models"].get("gpt2-medium")
        if small and medium:
            delta_s2 = medium["avg_s2"] - small["avg_s2"]
            delta_surp = medium["avg_surprisal"] - small["avg_surprisal"]
            delta_ent = medium["avg_entropy"] - small["avg_entropy"]
            s2_deltas.append(delta_s2)
            surprisal_deltas.append(delta_surp)
            entropy_deltas.append(delta_ent)
            print(f"  {'  -> Δ (medium - small)':<54} ΔS₂={delta_s2:+.3f}  "
                  f"Δsurp={delta_surp:+.3f}  Δent={delta_ent:+.3f}")
        print()

    if s2_deltas:
        print("=" * 90)
        print("AGGREGATE: Medium vs Small")
        print(f"  Avg ΔS₂:            {sum(s2_deltas)/len(s2_deltas):+.4f}")
        print(f"  Avg Δsurprisal:     {sum(surprisal_deltas)/len(surprisal_deltas):+.4f}")
        print(f"  Avg Δentropy:       {sum(entropy_deltas)/len(entropy_deltas):+.4f}")
        n_lower = sum(1 for d in s2_deltas if d < 0)
        print(f"  Poems where medium has LOWER S2: {n_lower}/{len(s2_deltas)}")
        print(f"  Poems where medium has HIGHER S2: {len(s2_deltas)-n_lower}/{len(s2_deltas)}")

    print("\nTOP HIGH-S2 TOKENS PER POEM (gpt2-medium, with model's top prediction):")
    print("-" * 90)
    for title, data in results.items():
        short = title[:60]
        medium_stats = data["models"].get("gpt2-medium", {})
        top_tokens = medium_stats.get("top_s2_tokens", [])
        if top_tokens:
            print(f"  {short}:")
            for tok, s2_val, top_pred in top_tokens:
                print(f"    '{tok}' (S2={s2_val:+.2f}) — model expected: '{top_pred}'")
        print()

    return s2_deltas, surprisal_deltas, entropy_deltas


if __name__ == "__main__":
    results = run()
    s2_deltas, surprisal_deltas, entropy_deltas = print_comparison_table(results)

    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "cross_model_comparison.json")
    with open(out_path, "w") as f:
        json.dump({
            "results": results,
            "aggregate": {
                "avg_delta_s2": sum(s2_deltas) / len(s2_deltas) if s2_deltas else 0,
                "avg_delta_surprisal": sum(surprisal_deltas) / len(surprisal_deltas) if surprisal_deltas else 0,
                "avg_delta_entropy": sum(entropy_deltas) / len(entropy_deltas) if entropy_deltas else 0,
                "n_poems": len(s2_deltas),
            }
        }, f, indent=2)
    print(f"\nResults saved to {out_path}")
