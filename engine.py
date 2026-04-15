"""
S₂ Lab — Information-theoretic analysis engine.

Computes token-level surprisal, entropy, and S₂ for texts using GPT-2.
Saves structured results to JSON for downstream analysis.

Language settings
-----------------
  "en" (default)  — gpt2
  "de"            — dbmdz/german-gpt2

Set via the `language` parameter on analyze_poem() / analyze_corpus(),
or pass --language de when running as a script.
"""

import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
import math
import json
import os
from datetime import datetime

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)

# ── Language config ────────────────────────────────────────────────────────────
# Each entry: model name + demo example shown when running as a script.
LANGUAGE_CONFIG = {
    "en": {
        "model":          "gpt2",
        "example_text":   "The only emperor is the emperor of ice-cream.",
        "example_title":  "The Emperor of Ice-Cream",
        "example_author": "Wallace Stevens",
        "example_year":   1922,
    },
    "de": {
        "model":          "dbmdz/german-gpt2",
        "example_text":   "Komm in den totgesagten park und schau:",
        "example_title":  "Komm in den totgesagten park",
        "example_author": "Stefan George",
        "example_year":   1891,
    },
}

# Model cache — one (model, tokenizer) pair per language, loaded on first use.
_models: dict = {}


def get_model(language: str = "en"):
    """Return (model, tokenizer) for the given language, loading if needed."""
    if language not in _models:
        cfg = LANGUAGE_CONFIG.get(language)
        if cfg is None:
            raise ValueError(
                f"Unknown language '{language}'. Choose from: {list(LANGUAGE_CONFIG)}"
            )
        model_name = cfg["model"]
        print(f"Loading {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        model.eval()
        _models[language] = (model, tokenizer)
    return _models[language]


def analyze_poem(text, title="", author="", year=None, era="", language="en", top_k=10):
    """
    Analyze a text and return structured token-level metrics.

    Parameters
    ----------
    language : str
        "en" (default, uses gpt2) or "de" (uses dbmdz/german-gpt2).

    Returns dict with:
      - metadata (title, author, language, model, etc.)
      - summary stats (avg surprisal, entropy, s2)
      - token-level data (each token with metrics + top-k alternatives)
      - high_s2 moments (top 10 by S₂, with "unsaid" alternatives)
    """
    model, tokenizer = get_model(language)
    model_name = LANGUAGE_CONFIG[language]["model"]

    input_ids = tokenizer.encode(text, return_tensors="pt")
    tokens = [tokenizer.decode([t]) for t in input_ids[0]]

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits

    token_data = []

    for i in range(len(tokens) - 1):
        token_logits = logits[0, i, :]
        probs = F.softmax(token_logits, dim=-1)
        log_probs = F.log_softmax(token_logits, dim=-1)

        actual_id = input_ids[0, i + 1].item()
        actual_token = tokens[i + 1]

        surprisal = -log_probs[actual_id].item() / math.log(2)
        entropy = -(probs * log_probs).sum().item() / math.log(2)
        s2 = surprisal - entropy
        prob = probs[actual_id].item()

        # Top-k alternatives (the "unsaid")
        topk_probs, topk_ids = torch.topk(probs, top_k)
        alternatives = [
            {"token": tokenizer.decode([tid.item()]), "prob": tp.item()}
            for tid, tp in zip(topk_ids, topk_probs)
        ]

        # Rank of actual token
        sorted_probs, sorted_ids = torch.sort(probs, descending=True)
        rank = (sorted_ids == actual_id).nonzero(as_tuple=True)[0].item() + 1

        token_data.append({
            "position": i + 1,
            "token": actual_token,
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "prob": round(prob, 6),
            "rank": rank,
            "alternatives": alternatives,
        })

    # Summary stats
    n = len(token_data)
    avg_surprisal = sum(t["surprisal"] for t in token_data) / n
    avg_entropy = sum(t["entropy"] for t in token_data) / n
    avg_s2 = sum(t["s2"] for t in token_data) / n
    max_s2 = max(t["s2"] for t in token_data)
    min_s2 = min(t["s2"] for t in token_data)
    std_s2 = (sum((t["s2"] - avg_s2) ** 2 for t in token_data) / n) ** 0.5

    # Positive S₂ ratio: what fraction of tokens are "more surprising than expected"
    pos_s2_ratio = sum(1 for t in token_data if t["s2"] > 0) / n

    # High S₂ moments (top 10)
    high_s2 = sorted(token_data, key=lambda t: t["s2"], reverse=True)[:10]

    # Build context for high-S₂ moments
    for moment in high_s2:
        pos = moment["position"]
        ctx_start = max(0, pos - 4)
        ctx_tokens = [token_data[j]["token"] for j in range(ctx_start, min(pos - 1, n))]
        moment["context_before"] = "".join(ctx_tokens)

    result = {
        "metadata": {
            "title": title,
            "author": author,
            "year": year,
            "era": era,
            "language": language,
            "analyzed_at": datetime.now().isoformat(),
            "model": model_name,
            "n_tokens": n,
        },
        "summary": {
            "avg_surprisal": round(avg_surprisal, 4),
            "avg_entropy": round(avg_entropy, 4),
            "avg_s2": round(avg_s2, 4),
            "max_s2": round(max_s2, 4),
            "min_s2": round(min_s2, 4),
            "std_s2": round(std_s2, 4),
            "pos_s2_ratio": round(pos_s2_ratio, 4),
        },
        "tokens": token_data,
        "high_s2_moments": high_s2,
    }

    return result


def analyze_corpus(poems):
    """Analyze a list of poem dicts, return list of results.

    Each poem dict may include a 'language' key ("en" or "de").
    Defaults to "en" if absent.
    """
    results = []
    for i, poem in enumerate(poems):
        lang = poem.get("language", "en")
        print(f"  [{i+1}/{len(poems)}] [{lang}] {poem['author']} — {poem['title']}")
        result = analyze_poem(
            text=poem["text"],
            title=poem["title"],
            author=poem["author"],
            year=poem.get("year"),
            era=poem.get("era", ""),
            language=lang,
        )
        results.append(result)
    return results


def save_results(results, filename="corpus_results.json"):
    """Save results to JSON file."""
    path = os.path.join(RESULTS_DIR, filename)
    with open(path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"Saved {len(results)} results to {path}")
    return path


def load_results(filename="corpus_results.json"):
    """Load results from JSON file."""
    path = os.path.join(RESULTS_DIR, filename)
    with open(path) as f:
        return json.load(f)


def comparative_summary(results):
    """Print a comparative table of all analyzed texts."""
    print(f"\n{'='*100}")
    print(f"  COMPARATIVE SUMMARY — {len(results)} texts")
    print(f"{'='*100}")
    print(f"\n{'Author':<22} {'Title':<35} {'Surp':>6} {'Ent':>6} {'S₂':>7} {'S₂σ':>6} {'+S₂%':>6} {'maxS₂':>7}")
    print("-" * 100)

    for r in sorted(results, key=lambda r: r["summary"]["avg_s2"], reverse=True):
        m = r["metadata"]
        s = r["summary"]
        print(f"{m['author'][:21]:<22} {m['title'][:34]:<35} {s['avg_surprisal']:>6.2f} {s['avg_entropy']:>6.2f} {s['avg_s2']:>7.2f} {s['std_s2']:>6.2f} {s['pos_s2_ratio']:>5.0%} {s['max_s2']:>7.2f}")

    # Era averages
    era_data = {}
    for r in results:
        era = r["metadata"]["era"]
        if era not in era_data:
            era_data[era] = []
        era_data[era].append(r["summary"])

    print(f"\n{'─'*100}")
    print(f"  BY ERA")
    print(f"{'─'*100}")
    print(f"\n{'Era':<25} {'n':>3} {'Avg Surp':>9} {'Avg Ent':>9} {'Avg S₂':>9} {'Avg +S₂%':>9}")
    print("-" * 70)

    for era in sorted(
        era_data,
        key=lambda e: sum(s["avg_s2"] for s in era_data[e]) / len(era_data[e]),
        reverse=True,
    ):
        summaries = era_data[era]
        n = len(summaries)
        avg_surp = sum(s["avg_surprisal"] for s in summaries) / n
        avg_ent = sum(s["avg_entropy"] for s in summaries) / n
        avg_s2 = sum(s["avg_s2"] for s in summaries) / n
        avg_pos = sum(s["pos_s2_ratio"] for s in summaries) / n
        print(f"{era:<25} {n:>3} {avg_surp:>9.2f} {avg_ent:>9.2f} {avg_s2:>9.2f} {avg_pos:>8.0%}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="S₂ Lab engine demo")
    parser.add_argument(
        "--language", choices=list(LANGUAGE_CONFIG), default="en",
        help="Language setting: en (default, gpt2) or de (dbmdz/german-gpt2)",
    )
    args = parser.parse_args()

    cfg = LANGUAGE_CONFIG[args.language]
    print(f"Language: {args.language}  |  Model: {cfg['model']}\n")
    print(f"Example: \"{cfg['example_text']}\"")
    print(f"  — {cfg['example_author']}, {cfg['example_title']} ({cfg['example_year']})\n")

    result = analyze_poem(
        text=cfg["example_text"],
        title=cfg["example_title"],
        author=cfg["example_author"],
        year=cfg["example_year"],
        language=args.language,
    )

    s = result["summary"]
    print(
        f"avg_surprisal={s['avg_surprisal']:.3f}  avg_entropy={s['avg_entropy']:.3f}  "
        f"avg_s2={s['avg_s2']:.3f}  pos_s2_ratio={s['pos_s2_ratio']:.0%}"
    )
    print("\nToken-level breakdown:")
    for t in result["tokens"]:
        marker = " <<<" if t["s2"] > 2 else ""
        print(
            f"  {t['token']:<15} surp={t['surprisal']:>6.2f}  "
            f"ent={t['entropy']:>6.2f}  S₂={t['s2']:>7.2f}  rank={t['rank']}{marker}"
        )
