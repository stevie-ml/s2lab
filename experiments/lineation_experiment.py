"""
Lineation Experiment: S2 with vs. without line breaks.

Tests whether lineation (the poetic line break) is a primary driver of S2 or
whether word-choice surprise persists when poems are rendered as prose.

Method:
- Select a stratified sample of poems from the corpus
- Run each poem twice: (a) original text with newlines, (b) stripped (newlines → space)
- Compare token-level S2 distributions
- Identify which tokens change most — i.e., which positions are lineation-sensitive

Hypothesis:
  H1 (layout artifact): S2 drops substantially when newlines are removed, confirming
      that line-break positions dominate the poetry–prose gap.
  H2 (word-choice): S2 remains high even without line breaks, confirming that
      poets' lexical choices are genuinely more surprising than expected.
"""

import sys, os, json, re, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from corpus.poems import POEMS

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),
                            "results", "lineation_experiment.json")

# ── Sample selection ───────────────────────────────────────────────────────────
# Include eras spanning the S2 range; exclude ultra-short poems (< 20 tokens)
TARGET_ERAS = [
    "modernist", "victorian", "romantic", "haiku", "beat",
    "confessional", "new_york_school", "ballad", "control",
    "imagist", "fixed_form", "contemporary", "prose_poetry",
]
SAMPLE_PER_ERA = 2
MAX_TOKENS = 300   # keep inference fast

random.seed(42)

def select_sample():
    by_era = {}
    for p in POEMS:
        era = p.get("era", "unknown")
        if era in TARGET_ERAS:
            by_era.setdefault(era, []).append(p)
    sample = []
    for era in TARGET_ERAS:
        pool = by_era.get(era, [])
        pool = [p for p in pool if len(p["text"].split()) > 15]
        chosen = random.sample(pool, min(SAMPLE_PER_ERA, len(pool)))
        sample.extend(chosen)
    return sample

# ── Model loading ──────────────────────────────────────────────────────────────
def load_model():
    print("Loading GPT-2...")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    return model, tokenizer

def analyze_text(text, model, tokenizer, max_tokens=MAX_TOKENS):
    """Return list of {token, surprisal, entropy, s2, p_newline}."""
    input_ids = tokenizer.encode(text, return_tensors="pt")
    if input_ids.shape[1] > max_tokens + 1:
        input_ids = input_ids[:, :max_tokens + 1]
    tokens = [tokenizer.decode([t]) for t in input_ids[0]]

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits

    vocab_size = len(tokenizer)
    nl_ids = [i for i in range(vocab_size) if tokenizer.decode([i]).strip("\r\n") == ""]
    nl_tensor = torch.tensor(nl_ids, dtype=torch.long) if nl_ids else None

    results = []
    for i in range(len(tokens) - 1):
        tok_logits = logits[0, i, :]
        probs = F.softmax(tok_logits, dim=-1)
        log_probs = F.log_softmax(tok_logits, dim=-1)
        actual_id = input_ids[0, i + 1].item()
        surprisal = -log_probs[actual_id].item() / math.log(2)
        entropy = -(probs * log_probs).sum().item() / math.log(2)
        s2 = surprisal - entropy
        p_nl = probs[nl_tensor].sum().item() if nl_tensor is not None else 0.0
        results.append({
            "token": tokens[i + 1],
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "p_newline": round(p_nl, 6),
            "is_newline": tokens[i + 1].strip() == "",
        })
    return results

def strip_lineation(text):
    """Replace newlines with spaces, collapsing multiple spaces."""
    return re.sub(r'\s+', ' ', text.replace('\n', ' ')).strip()

def summary_stats(token_data, artifact_free=False):
    """Compute mean S2 and other stats; optionally filter out high p_newline tokens."""
    if artifact_free:
        tokens = [t for t in token_data if t["p_newline"] < 0.9 and not t["is_newline"]]
    else:
        tokens = token_data
    if not tokens:
        return {"avg_s2": None, "n": 0, "pct_positive": 0, "std_s2": 0}
    n = len(tokens)
    avg = sum(t["s2"] for t in tokens) / n
    std = (sum((t["s2"] - avg) ** 2 for t in tokens) / n) ** 0.5
    pos = sum(1 for t in tokens if t["s2"] > 0) / n
    return {"avg_s2": round(avg, 4), "n": n, "pct_positive": round(pos, 4), "std_s2": round(std, 4)}

# ── Main ───────────────────────────────────────────────────────────────────────
def main():
    sample = select_sample()
    print(f"Selected {len(sample)} poems across {len(TARGET_ERAS)} eras")

    model, tokenizer = load_model()

    poem_results = []
    for i, poem in enumerate(sample):
        title = poem.get("title", "?")
        author = poem.get("author", "?")
        era = poem.get("era", "?")
        text = poem["text"]
        prose = strip_lineation(text)

        print(f"  [{i+1}/{len(sample)}] {author}: {title[:40]}")

        lineated = analyze_text(text, model, tokenizer)
        stripped = analyze_text(prose, model, tokenizer)

        poem_results.append({
            "title": title,
            "author": author,
            "era": era,
            "lineated": {
                "raw": summary_stats(lineated),
                "artifact_free": summary_stats(lineated, artifact_free=True),
                "newline_count": sum(1 for t in lineated if t["is_newline"]),
            },
            "stripped": {
                "raw": summary_stats(stripped),
                "artifact_free": summary_stats(stripped, artifact_free=True),
            },
            "delta_s2_raw": round(
                (summary_stats(lineated)["avg_s2"] or 0) -
                (summary_stats(stripped)["avg_s2"] or 0), 4
            ),
            "delta_s2_clean": round(
                (summary_stats(lineated, artifact_free=True)["avg_s2"] or 0) -
                (summary_stats(stripped, artifact_free=True)["avg_s2"] or 0), 4
            ),
        })

    # Aggregate by condition (lineated vs. stripped)
    all_lineated_raw = [r["lineated"]["raw"]["avg_s2"] for r in poem_results if r["lineated"]["raw"]["avg_s2"] is not None]
    all_stripped_raw = [r["stripped"]["raw"]["avg_s2"] for r in poem_results if r["stripped"]["raw"]["avg_s2"] is not None]
    all_lineated_clean = [r["lineated"]["artifact_free"]["avg_s2"] for r in poem_results if r["lineated"]["artifact_free"]["avg_s2"] is not None]
    all_stripped_clean = [r["stripped"]["artifact_free"]["avg_s2"] for r in poem_results if r["stripped"]["artifact_free"]["avg_s2"] is not None]

    def mean(lst):
        return round(sum(lst) / len(lst), 4) if lst else None

    aggregate = {
        "lineated_raw_mean": mean(all_lineated_raw),
        "stripped_raw_mean": mean(all_stripped_raw),
        "lineated_clean_mean": mean(all_lineated_clean),
        "stripped_clean_mean": mean(all_stripped_clean),
        "raw_gap": round((mean(all_lineated_raw) or 0) - (mean(all_stripped_raw) or 0), 4),
        "clean_gap": round((mean(all_lineated_clean) or 0) - (mean(all_stripped_clean) or 0), 4),
        "n_poems": len(poem_results),
    }

    output = {
        "aggregate": aggregate,
        "poems": poem_results,
    }

    with open(RESULTS_FILE, "w") as f:
        json.dump(output, f, indent=2)

    print("\n=== LINEATION EXPERIMENT RESULTS ===")
    print(f"N poems: {aggregate['n_poems']}")
    print(f"\nRaw S2:   lineated={aggregate['lineated_raw_mean']:+.3f}  stripped={aggregate['stripped_raw_mean']:+.3f}  gap={aggregate['raw_gap']:+.3f}")
    print(f"Clean S2: lineated={aggregate['lineated_clean_mean']:+.3f}  stripped={aggregate['stripped_clean_mean']:+.3f}  gap={aggregate['clean_gap']:+.3f}")
    print(f"\nPer-poem deltas (lineated - stripped, clean):")
    for r in sorted(poem_results, key=lambda x: x["delta_s2_clean"], reverse=True):
        print(f"  {r['delta_s2_clean']:+.3f}  {r['author'][:25]}: {r['title'][:35]}")
    print(f"\nSaved: {RESULTS_FILE}")
    return output

if __name__ == "__main__":
    main()
