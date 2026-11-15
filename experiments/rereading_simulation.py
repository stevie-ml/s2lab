"""
Rereading Simulation: How does S2 change on second reading?

Hypothesis: When a poem is "read again" (the model has seen its text before),
surprisal drops but entropy drops too — and S2 (the gap between them) might
actually increase, stay the same, or collapse. This tells us whether a poem's
information signature is robust or contingent on novelty.

Method:
  - "First reading": standard S2 analysis (cold context)
  - "Second reading": prepend the full poem as context, then analyze it again
    (GPT-2 now "knows" what's coming)
  - Compare avg_s2, std_s2, pos_s2_ratio, surprisal, entropy across both passes

For the second reading, GPT-2 has seen all the words in sequence; on re-encounter
each token's surprisal should drop to near zero (it predicts exactly), while
entropy might also drop (it's confident). S2 = surprisal - entropy may become
very negative (overconfident model).

The interesting finding: which poems/eras maintain their S2 on rereading?
Poems where deviation is STRUCTURAL (forced by meter, form, semantic choices)
vs poems where it's sequential (surprise depends on what came before).
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import math
import torch
import torch.nn.functional as F
from transformers import AutoTokenizer, AutoModelForCausalLM
from engine import get_model

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
CORPUS_PATH = os.path.join(RESULTS_DIR, "corpus_results.json")

MAX_TOKENS = 450  # max poem length to include (leaves room for double context in 1024 window)
TOP_K = 5
N_POEMS = 40  # analyze this many poems (diverse sample)


def analyze_with_context(text, context_text, model, tokenizer, nl_tensor, top_k=5):
    """
    Analyze a text given a preceding context string.

    Returns the same structure as engine.analyze_poem() but only for the
    tokens in `text`, using `context_text` as prefix.
    """
    full_text = context_text + text
    full_ids = tokenizer.encode(full_text, return_tensors="pt")
    context_ids = tokenizer.encode(context_text, return_tensors="pt")
    context_len = context_ids.shape[1]

    # Safety check: total length must fit in model context
    if full_ids.shape[1] > 1020:
        return None

    tokens_text = [tokenizer.decode([t]) for t in tokenizer.encode(text)]

    with torch.no_grad():
        outputs = model(full_ids)
        logits = outputs.logits

    token_data = []
    n_text_tokens = len(tokens_text) - 1  # number of predictions we can make

    for i in range(n_text_tokens):
        # Position in full sequence: context_len + i
        pos_in_full = context_len + i

        if pos_in_full >= full_ids.shape[1] - 1:
            break

        token_logits = logits[0, pos_in_full, :]
        probs = F.softmax(token_logits, dim=-1)
        log_probs = F.log_softmax(token_logits, dim=-1)

        actual_id = full_ids[0, pos_in_full + 1].item()
        actual_token = tokenizer.decode([actual_id])

        surprisal = -log_probs[actual_id].item() / math.log(2)
        entropy = -(probs * log_probs).sum().item() / math.log(2)
        s2 = surprisal - entropy
        prob = probs[actual_id].item()

        p_newline = probs[nl_tensor].sum().item() if nl_tensor is not None else 0.0

        token_data.append({
            "position": i + 1,
            "token": actual_token,
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "prob": round(prob, 6),
            "p_newline": round(p_newline, 6),
        })

    if not token_data:
        return None

    n = len(token_data)
    avg_surprisal = sum(t["surprisal"] for t in token_data) / n
    avg_entropy = sum(t["entropy"] for t in token_data) / n
    avg_s2 = sum(t["s2"] for t in token_data) / n
    std_s2 = (sum((t["s2"] - avg_s2) ** 2 for t in token_data) / n) ** 0.5
    pos_s2_ratio = sum(1 for t in token_data if t["s2"] > 0) / n

    return {
        "avg_surprisal": round(avg_surprisal, 4),
        "avg_entropy": round(avg_entropy, 4),
        "avg_s2": round(avg_s2, 4),
        "std_s2": round(std_s2, 4),
        "pos_s2_ratio": round(pos_s2_ratio, 4),
        "n_tokens": n,
    }


def run():
    print("Loading corpus results...")
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    print(f"Loaded {len(corpus)} results")

    # Filter: English only, fit in context, diverse eras
    candidates = []
    for r in corpus:
        lang = r.get("metadata", {}).get("language", "en")
        if lang != "en":
            continue
        n_tokens = r.get("metadata", {}).get("n_tokens", 9999)
        if n_tokens <= MAX_TOKENS and n_tokens >= 30:
            candidates.append(r)

    print(f"Candidates fitting context window: {len(candidates)}")

    # Sample diverse eras
    era_groups = {}
    for c in candidates:
        era = c["metadata"].get("era", "unknown")
        era_groups.setdefault(era, []).append(c)

    # Pick up to 2 poems per era, aiming for N_POEMS total
    selected = []
    per_era = max(1, N_POEMS // len(era_groups))
    for era, poems in sorted(era_groups.items()):
        for p in poems[:per_era]:
            selected.append(p)
        if len(selected) >= N_POEMS:
            break

    # Fill remaining slots from any era
    if len(selected) < N_POEMS:
        remaining = [c for c in candidates if c not in selected]
        selected.extend(remaining[:N_POEMS - len(selected)])

    selected = selected[:N_POEMS]
    print(f"Selected {len(selected)} poems for analysis")

    # Load model
    print("Loading GPT-2...")
    model, tokenizer, nl_tensor = get_model("en")

    results = []
    for idx, poem_result in enumerate(selected):
        meta = poem_result["metadata"]
        title = meta.get("title", "Unknown")
        author = meta.get("author", "Unknown")
        era = meta.get("era", "unknown")

        # We need the original text. We reconstruct it from tokens.
        # Actually, let's get the original poem from the corpus.
        # We'll use the token sequence to reconstruct.
        tokens = poem_result.get("tokens", [])
        if not tokens:
            continue

        # Reconstruct text from token data - use the first token + all subsequent tokens
        text_tokens = [tokens[0]["token"]] + [t["token"] for t in tokens]
        poem_text = "".join(text_tokens)

        # First reading stats (from existing results)
        first_read = poem_result.get("summary", {})
        avg_s2_first = first_read.get("avg_s2", None)
        avg_surp_first = first_read.get("avg_surprisal", None)
        avg_ent_first = first_read.get("avg_entropy", None)
        std_s2_first = first_read.get("std_s2", None)
        pos_ratio_first = first_read.get("pos_s2_ratio", None)

        # Second reading: prepend the poem as context
        second = analyze_with_context(poem_text, poem_text, model, tokenizer, nl_tensor, TOP_K)

        if second is None:
            print(f"  [{idx+1}/{len(selected)}] SKIP (too long): {title[:50]}")
            continue

        s2_drop = round((second["avg_s2"] - avg_s2_first) if avg_s2_first is not None else 0, 4)
        surp_drop = round((second["avg_surprisal"] - avg_surp_first) if avg_surp_first is not None else 0, 4)
        ent_drop = round((second["avg_entropy"] - avg_ent_first) if avg_ent_first is not None else 0, 4)

        result = {
            "title": title,
            "author": author,
            "era": era,
            "n_tokens": meta.get("n_tokens", 0),
            "first_read": {
                "avg_s2": avg_s2_first,
                "avg_surprisal": avg_surp_first,
                "avg_entropy": avg_ent_first,
                "std_s2": std_s2_first,
                "pos_s2_ratio": pos_ratio_first,
            },
            "second_read": second,
            "delta": {
                "s2": s2_drop,
                "surprisal": surp_drop,
                "entropy": ent_drop,
                "s2_pct_change": round(s2_drop / abs(avg_s2_first) * 100, 1) if avg_s2_first else None,
            }
        }
        results.append(result)

        print(f"  [{idx+1}/{len(selected)}] {title[:50]} | "
              f"S2: {avg_s2_first:.3f}→{second['avg_s2']:.3f} (Δ{s2_drop:+.3f}) | "
              f"Surp: {avg_surp_first:.2f}→{second['avg_surprisal']:.2f} | "
              f"Ent: {avg_ent_first:.2f}→{second['avg_entropy']:.2f}")

    # Aggregate by era
    era_stats = {}
    for r in results:
        era = r["era"]
        era_stats.setdefault(era, []).append(r)

    print(f"\n=== ERA SUMMARY ===")
    for era, poems in sorted(era_stats.items(), key=lambda x: -len(x[1])):
        avg_delta_s2 = sum(p["delta"]["s2"] for p in poems) / len(poems)
        avg_delta_surp = sum(p["delta"]["surprisal"] for p in poems) / len(poems)
        avg_delta_ent = sum(p["delta"]["entropy"] for p in poems) / len(poems)
        print(f"  {era} (n={len(poems)}): ΔS2={avg_delta_s2:+.3f}, ΔSurp={avg_delta_surp:+.3f}, ΔEnt={avg_delta_ent:+.3f}")

    output = {
        "experiment": "rereading_simulation",
        "description": "Compare S2 on first vs second reading (poem prepended as context)",
        "n_poems": len(results),
        "results": results,
    }

    out_path = os.path.join(RESULTS_DIR, "rereading_simulation.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    return output


if __name__ == "__main__":
    run()
