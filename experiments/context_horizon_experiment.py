"""
Context Horizon Experiment: Is Poetic Surprise Local or Global?

For each token, compare surprisal computed with different context window lengths:
  window=1:  P(w | w_{-1})          — bigram local surprise
  window=5:  P(w | w_{-5}...w_{-1}) — short-range phrase context
  window=20: P(w | w_{-20}...w_{-1})— clause/sentence context
  window=50: P(w | w_{-50}...w_{-1})— stanza/paragraph context
  window=MAX: P(w | all previous)   — full poem context (normal S2)

Key metrics:
  - "context_gain": how much extra surprise/predictability the full context adds
    vs the bigram baseline (full_surprisal - bigram_surprisal)
  - If context_gain < 0: full context HELPS prediction (poem telegraphs the word)
  - If context_gain > 0: full context HURTS prediction (poem builds toward violation)

The hypothesis: poets use two strategies:
  A) "Telegraph and deliver": build context that makes a word seem inevitable,
     then deliver it (context_gain < 0, low/negative S2)
  B) "Frame and violate": build context that makes a word seem IMPOSSIBLE,
     then choose it anyway (context_gain > 0, high S2)
"""

import sys
import os
import json
import math
import numpy as np
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from corpus.poems import POEMS

WINDOWS = [1, 5, 20, 50]  # context lengths to test, plus MAX (full)
SAMPLE_N = 40  # poems to analyze (full run is slow)
STANZA_BREAK_THRESHOLD = 0.9  # skip tokens where P(newline) > 0.9

def load_model():
    print("Loading GPT-2...")
    tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
    model = GPT2LMHeadModel.from_pretrained("gpt2")
    model.eval()
    return model, tokenizer

def get_surprisal_and_entropy(model, tokenizer, input_ids, position):
    """Get surprisal and entropy for the token at `position`, given context before it."""
    if position == 0:
        return None, None
    context = input_ids[:position]
    target = input_ids[position]

    with torch.no_grad():
        out = model(torch.tensor([context]))
        logits = out.logits[0, -1, :]
        log_probs = torch.log_softmax(logits, dim=-1)
        probs = torch.softmax(logits, dim=-1)

    surprisal = -log_probs[target].item() / math.log(2)
    entropy = -torch.sum(probs * torch.log2(probs + 1e-10)).item()
    return surprisal, entropy

def is_stanza_break_token(model, tokenizer, input_ids, position):
    """Return True if newline is the modal prediction at this position."""
    if position == 0:
        return False
    context = input_ids[:position]
    newline_id = tokenizer.encode("\n")[0]
    with torch.no_grad():
        out = model(torch.tensor([context]))
        probs = torch.softmax(out.logits[0, -1, :], dim=-1)
    return probs[newline_id].item() > STANZA_BREAK_THRESHOLD

def analyze_poem_horizons(model, tokenizer, text):
    """
    For each token in the poem, compute surprisal at different context lengths.
    Returns a list of dicts with per-token metrics.
    """
    tokens = tokenizer.encode(text)
    results = []

    for pos in range(1, len(tokens)):
        # Skip if this looks like a stanza-break artifact
        if is_stanza_break_token(model, tokenizer, tokens, pos):
            continue

        token_str = tokenizer.decode([tokens[pos]])

        # Compute surprisal at each context window length
        window_results = {}
        for window in WINDOWS:
            start = max(0, pos - window)
            sub_ids = tokens[start:pos+1]
            sub_pos = len(sub_ids) - 1  # position within truncated context
            surp, ent = get_surprisal_and_entropy(model, tokenizer, sub_ids, sub_pos)
            window_results[f"w{window}"] = {"surprisal": surp, "entropy": ent}

        # Full context
        full_surp, full_ent = get_surprisal_and_entropy(model, tokenizer, tokens, pos)
        window_results["wMAX"] = {"surprisal": full_surp, "entropy": full_ent}

        if full_surp is None:
            continue

        # Context gain: how much extra (or less) surprising is this token with full context vs bigram
        bigram_surp = window_results["w1"]["surprisal"]
        if bigram_surp is None:
            continue

        context_gain = full_surp - bigram_surp  # positive = full context HURTS; negative = HELPS
        full_s2 = full_surp - full_ent
        bigram_s2 = bigram_surp - window_results["w1"]["entropy"]

        results.append({
            "pos": pos,
            "token": token_str,
            "full_surprisal": full_surp,
            "full_entropy": full_ent,
            "full_s2": full_s2,
            "bigram_surprisal": bigram_surp,
            "bigram_entropy": window_results["w1"]["entropy"],
            "bigram_s2": bigram_s2,
            "context_gain": context_gain,
            # surprisal at each window
            "surp_w5": window_results["w5"]["surprisal"],
            "surp_w20": window_results["w20"]["surprisal"],
            "surp_w50": window_results["w50"]["surprisal"],
        })

    return results

def classify_token(full_s2, context_gain, s2_thresh=2.0, gain_thresh=0.5):
    """Classify a token into one of four strategic types."""
    high_s2 = full_s2 > s2_thresh
    context_hurts = context_gain > gain_thresh

    if high_s2 and context_hurts:
        return "FRAME_AND_VIOLATE"    # context built up to make this more surprising
    elif high_s2 and not context_hurts:
        return "LOCAL_SHOCK"          # locally surprising, context didn't make it worse
    elif not high_s2 and context_hurts:
        return "CONTEXTUAL_DRIFT"     # context disrupted expectation but still conformist
    else:
        return "TELEGRAPHED"          # context helped predict this token

def main():
    model, tokenizer = load_model()

    # Filter to English poems with sufficient length
    en_poems = [p for p in POEMS if p.get("language", "en") == "en" and len(p["text"].split()) >= 30]
    sample = en_poems[:SAMPLE_N]

    print(f"Analyzing {len(sample)} poems for context horizon effects...")

    all_tokens = []
    poem_stats = []

    for i, poem in enumerate(sample):
        print(f"  [{i+1}/{len(sample)}] {poem['author']} — {poem['title'][:40]}")
        tokens = analyze_poem_horizons(model, tokenizer, poem["text"])

        if len(tokens) < 10:
            continue

        # Compute poem-level stats
        full_s2s = [t["full_s2"] for t in tokens]
        context_gains = [t["context_gain"] for t in tokens]

        # Classify tokens
        type_counts = {"FRAME_AND_VIOLATE": 0, "LOCAL_SHOCK": 0, "CONTEXTUAL_DRIFT": 0, "TELEGRAPHED": 0}
        for t in tokens:
            cls = classify_token(t["full_s2"], t["context_gain"])
            type_counts[cls] += 1
            t["type"] = cls
            t["poem_title"] = poem["title"]
            t["author"] = poem["author"]
            t["era"] = poem.get("era", "unknown")

        n = len(tokens)
        poem_stats.append({
            "title": poem["title"],
            "author": poem["author"],
            "era": poem.get("era", "unknown"),
            "n_tokens": n,
            "mean_full_s2": np.mean(full_s2s),
            "mean_context_gain": np.mean(context_gains),
            "pct_frame_violate": type_counts["FRAME_AND_VIOLATE"] / n * 100,
            "pct_local_shock": type_counts["LOCAL_SHOCK"] / n * 100,
            "pct_telegraphed": type_counts["TELEGRAPHED"] / n * 100,
            # Correlation: does higher full_s2 tend to come with higher context_gain?
            "s2_gain_correlation": float(np.corrcoef(full_s2s, context_gains)[0,1]) if len(full_s2s) > 5 else 0,
        })
        all_tokens.extend(tokens)

    # Aggregate analysis
    all_full_s2 = [t["full_s2"] for t in all_tokens]
    all_gains = [t["context_gain"] for t in all_tokens]
    all_bigram_s2 = [t["bigram_s2"] for t in all_tokens]

    # How much does full context CHANGE surprisal vs bigram?
    mean_gain = np.mean(all_gains)
    # High-S2 tokens: is context_gain positive or negative?
    high_s2_mask = [t["full_s2"] > 2.0 for t in all_tokens]
    high_s2_gains = [t["context_gain"] for t, m in zip(all_tokens, high_s2_mask) if m]

    # Token-type taxonomy
    types = [t["type"] for t in all_tokens]
    type_dist = {t: types.count(t) / len(types) * 100 for t in ["FRAME_AND_VIOLATE", "LOCAL_SHOCK", "CONTEXTUAL_DRIFT", "TELEGRAPHED"]}

    # Era-level breakdown
    era_data = {}
    for t in all_tokens:
        era = t["era"]
        if era not in era_data:
            era_data[era] = {"gains": [], "s2s": []}
        era_data[era]["gains"].append(t["context_gain"])
        era_data[era]["s2s"].append(t["full_s2"])

    era_stats = {}
    for era, d in era_data.items():
        if len(d["gains"]) >= 10:
            era_stats[era] = {
                "n": len(d["gains"]),
                "mean_gain": np.mean(d["gains"]),
                "mean_s2": np.mean(d["s2s"]),
                "corr": float(np.corrcoef(d["gains"], d["s2s"])[0,1]),
            }

    # Context saturation: how much does S2 change as window grows?
    # Use window comparison to find where S2 "saturates"
    paired = [(t["full_s2"], t["bigram_s2"], t.get("surp_w5"), t.get("surp_w20"), t.get("surp_w50"))
              for t in all_tokens if t.get("surp_w5") and t.get("surp_w20")]
    if paired:
        full_s2s_p = [x[0] for x in paired]
        bigram_s2s_p = [x[1] for x in paired]
        # Correlation between full and bigram S2: if high, local context = global context
        local_global_corr = float(np.corrcoef(full_s2s_p, bigram_s2s_p)[0,1])
    else:
        local_global_corr = 0.0

    results = {
        "n_poems": len(poem_stats),
        "n_tokens": len(all_tokens),
        "mean_context_gain": float(mean_gain),
        "local_global_s2_correlation": local_global_corr,
        "high_s2_mean_gain": float(np.mean(high_s2_gains)) if high_s2_gains else 0,
        "high_s2_n": len(high_s2_gains),
        "type_distribution_pct": type_dist,
        "era_stats": era_stats,
        "poem_stats": poem_stats,
        "top_frame_violate_tokens": sorted(
            [t for t in all_tokens if t["type"] == "FRAME_AND_VIOLATE"],
            key=lambda t: t["full_s2"], reverse=True
        )[:20],
        "top_local_shock_tokens": sorted(
            [t for t in all_tokens if t["type"] == "LOCAL_SHOCK"],
            key=lambda t: t["full_s2"], reverse=True
        )[:20],
    }

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "results", "context_horizon_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n=== Context Horizon Results ===")
    print(f"Poems: {results['n_poems']}, Tokens: {results['n_tokens']}")
    print(f"Mean context_gain (full vs bigram): {mean_gain:+.3f} bits")
    print(f"  (negative = full context predicts better; positive = full context predicts worse)")
    print(f"Local vs global S2 correlation: {local_global_corr:.3f}")
    print(f"High-S2 tokens (S2>2): n={len(high_s2_gains)}, mean gain={np.mean(high_s2_gains) if high_s2_gains else 0:+.3f}")
    print(f"\nToken type distribution:")
    for k, v in sorted(type_dist.items(), key=lambda x: -x[1]):
        print(f"  {k:25s}: {v:5.1f}%")
    print(f"\nSaved to {out_path}")
    return results

if __name__ == "__main__":
    main()
