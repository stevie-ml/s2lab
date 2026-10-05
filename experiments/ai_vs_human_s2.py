"""
AI-Generated vs Human Poetry: S₂ Signature of Algorithmic Text

Research question: Can information-theoretic S₂ distinguish human poetry
from GPT-2's own generated text? When GPT-2 evaluates its own outputs,
does it find them conformist (low S₂) compared to human poetry?

Three conditions:
  1. GPT-2 greedy (temp ≈ 0): Should have near-zero S₂ by construction
  2. GPT-2 sampled (temp = 1.0): Random variation, possibly high S₂ but unstructured
  3. GPT-2 high temp (temp = 1.5): Chaotic, possibly high surprisal + entropy
  4. Human poetry (from corpus): Strategic S₂ — spikes at meaningful moments

Additionally tests whether S₂ variance (not just mean) differs between conditions.
"""

import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from engine import analyze_poem, get_model
import numpy as np
import random

random.seed(42)
torch.manual_seed(42)

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                             "results", "ai_vs_human_s2.json")

# ── Poem-like prompts (first line given, GPT-2 completes) ─────────────────────
PROMPTS = [
    "The light falls through the window onto",
    "I have waited long enough for the",
    "Something there is that doesn't love a",
    "In the middle of the road of my life",
    "Tell me, what is it you plan to do",
]

# Temperatures to test
TEMPERATURES = {
    "greedy": 0.01,    # near-deterministic
    "sampled": 1.0,    # standard sampling
    "high_temp": 1.5,  # chaotic sampling
}

MAX_NEW_TOKENS = 60
N_SAMPLES_PER_CONDITION = 3


def generate_text(model, tokenizer, prompt, temperature=1.0, max_new_tokens=60, seed=42):
    """Generate text continuation from a prompt."""
    torch.manual_seed(seed)
    inputs = tokenizer.encode(prompt, return_tensors="pt")

    with torch.no_grad():
        if temperature < 0.05:
            # Greedy
            outputs = model.generate(
                inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,
                pad_token_id=tokenizer.eos_token_id,
            )
        else:
            outputs = model.generate(
                inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=0.95,
                pad_token_id=tokenizer.eos_token_id,
            )

    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return full_text


def split_into_lines(text, approx_line_length=40):
    """Split generated text into rough poetic lines."""
    words = text.split()
    lines = []
    current_line = []
    current_len = 0

    for word in words:
        current_line.append(word)
        current_len += len(word) + 1
        if current_len >= approx_line_length:
            lines.append(" ".join(current_line))
            current_line = []
            current_len = 0

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)


def analyze_s2_stats(result):
    """Extract S₂ statistics from engine result."""
    tokens = result.get("tokens", [])
    clean_tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]

    if not clean_tokens:
        return None

    s2_vals = [t["s2"] for t in clean_tokens]
    entropy_vals = [t["entropy"] for t in clean_tokens]
    surprisal_vals = [t["surprisal"] for t in clean_tokens]

    return {
        "n_tokens": len(clean_tokens),
        "mean_s2": float(np.mean(s2_vals)),
        "std_s2": float(np.std(s2_vals)),
        "max_s2": float(np.max(s2_vals)),
        "pos_s2_ratio": float(np.mean([s > 0 for s in s2_vals])),
        "gini_s2": gini(np.array([abs(s) for s in s2_vals])),
        "mean_entropy": float(np.mean(entropy_vals)),
        "mean_surprisal": float(np.mean(surprisal_vals)),
        "spike_density": float(np.mean([s > 2.0 for s in s2_vals])),
        # Autocorrelation at lag 1 (sticky vs. random spikes)
        "autocorr_lag1": float(autocorr(s2_vals, 1)) if len(s2_vals) > 5 else 0.0,
    }


def gini(arr):
    """Gini coefficient of absolute S₂ values."""
    if len(arr) == 0:
        return 0.0
    arr = np.sort(arr)
    n = len(arr)
    if arr.sum() == 0:
        return 0.0
    return float((2 * np.sum(arr * np.arange(1, n+1)) - (n + 1) * arr.sum()) / (n * arr.sum()))


def autocorr(series, lag=1):
    """Pearson autocorrelation at given lag."""
    if len(series) <= lag + 1:
        return 0.0
    s = np.array(series)
    x = s[:-lag]
    y = s[lag:]
    if x.std() == 0 or y.std() == 0:
        return 0.0
    return float(np.corrcoef(x, y)[0, 1])


def run():
    print("Loading GPT-2 model...")
    model_obj, tokenizer, nl_ids = get_model("en")
    model = model_obj

    results = {
        "ai_generated": {},
        "summary": {}
    }

    all_stats = {}

    # ── Generate and analyze AI texts ─────────────────────────────────────────
    for cond_name, temperature in TEMPERATURES.items():
        print(f"\n=== Condition: {cond_name} (temp={temperature}) ===")
        cond_stats = []
        generated_texts = []

        for i, prompt in enumerate(PROMPTS[:N_SAMPLES_PER_CONDITION]):
            text = generate_text(model, tokenizer, prompt, temperature=temperature, seed=i*10+42)
            # Split into line-like structure
            text_lined = split_into_lines(text)
            generated_texts.append({"prompt": prompt, "text": text_lined, "raw_text": text})

            title = f"GPT-2 [{cond_name}] #{i+1}"
            result = analyze_poem(
                text=text_lined,
                title=title,
                author=f"GPT-2 ({cond_name})",
                year=2026,
                era=f"ai_{cond_name}",
                language="en",
                top_k=10,
            )

            stats = analyze_s2_stats(result)
            if stats:
                cond_stats.append(stats)
                print(f"  [{i+1}] mean_s2={stats['mean_s2']:.3f}, std={stats['std_s2']:.3f}, "
                      f"pos_ratio={stats['pos_s2_ratio']:.2f}, spike_density={stats['spike_density']:.3f}")

        all_stats[cond_name] = cond_stats
        results["ai_generated"][cond_name] = {
            "samples": generated_texts,
            "stats": cond_stats,
        }

    # ── Compare with human poetry from corpus results ──────────────────────────
    print("\n=== Loading human poetry comparison ===")
    corpus_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                               "results", "corpus_results.json")

    with open(corpus_path) as f:
        corpus = json.load(f)

    human_stats_by_era = {}
    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        if era in ("control",):  # skip prose control for now
            continue

        tokens = poem.get("tokens", [])
        clean_tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]
        if len(clean_tokens) < 10:
            continue

        s2_vals = [t["s2"] for t in clean_tokens]
        entropy_vals = [t["entropy"] for t in clean_tokens]
        surprisal_vals = [t["surprisal"] for t in clean_tokens]

        stats = {
            "n_tokens": len(clean_tokens),
            "mean_s2": float(np.mean(s2_vals)),
            "std_s2": float(np.std(s2_vals)),
            "max_s2": float(np.max(s2_vals)),
            "pos_s2_ratio": float(np.mean([s > 0 for s in s2_vals])),
            "gini_s2": gini(np.array([abs(s) for s in s2_vals])),
            "mean_entropy": float(np.mean(entropy_vals)),
            "mean_surprisal": float(np.mean(surprisal_vals)),
            "spike_density": float(np.mean([s > 2.0 for s in s2_vals])),
            "autocorr_lag1": float(autocorr(s2_vals, 1)) if len(s2_vals) > 5 else 0.0,
        }

        if era not in human_stats_by_era:
            human_stats_by_era[era] = []
        human_stats_by_era[era].append(stats)

    # Aggregate by era
    human_era_summary = {}
    for era, stats_list in human_stats_by_era.items():
        human_era_summary[era] = {
            metric: float(np.mean([s[metric] for s in stats_list]))
            for metric in stats_list[0].keys()
            if metric != "n_tokens"
        }
        human_era_summary[era]["n_poems"] = len(stats_list)

    results["human_era_summary"] = human_era_summary

    # ── Compute key comparisons ────────────────────────────────────────────────
    def avg_metric(stats_list, metric):
        return float(np.mean([s[metric] for s in stats_list if metric in s]))

    all_human_stats = [s for stats_list in human_stats_by_era.values() for s in stats_list]

    summary = {}
    for cond_name, cond_stats in all_stats.items():
        if not cond_stats:
            continue
        summary[f"ai_{cond_name}"] = {
            metric: avg_metric(cond_stats, metric)
            for metric in ["mean_s2", "std_s2", "pos_s2_ratio", "gini_s2",
                          "spike_density", "mean_entropy", "autocorr_lag1"]
        }

    summary["human_poetry"] = {
        metric: avg_metric(all_human_stats, metric)
        for metric in ["mean_s2", "std_s2", "pos_s2_ratio", "gini_s2",
                      "spike_density", "mean_entropy", "autocorr_lag1"]
    }

    results["summary"] = summary

    # ── Print results table ────────────────────────────────────────────────────
    print("\n=== Summary Table ===")
    metrics = ["mean_s2", "std_s2", "pos_s2_ratio", "gini_s2", "spike_density",
               "mean_entropy", "autocorr_lag1"]
    header = f"{'Condition':<20} " + " ".join(f"{m[:12]:>13}" for m in metrics)
    print(header)
    print("-" * len(header))

    for cond, stats in sorted(summary.items()):
        row = f"{cond:<20} " + " ".join(f"{stats.get(m, 0):>13.4f}" for m in metrics)
        print(row)

    # Save
    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {RESULTS_PATH}")
    return results


if __name__ == "__main__":
    run()
