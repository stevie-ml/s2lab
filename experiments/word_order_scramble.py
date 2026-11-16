"""
Word Order Scramble: Does S₂ capture syntax or just vocabulary?

Hypothesis: S₂ measures *sequential* deviation — the poet chooses words
that are surprising given what came before. If we scramble word order
(while preserving all tokens), the vocabulary is identical but the
sequential prediction context is destroyed.

Method:
  - For 50 poems, compute canonical S₂ (standard analysis)
  - Scramble: shuffle words within each line (preserving line structure)
  - Compare avg_s2, std_s2, pos_s2_ratio before and after scrambling
  - Also try full scramble (across the whole poem) and "anti-poem"
    (reverse word order within each line)

Expected results:
  H1 (syntactic): S₂ drops significantly — syntax matters for prediction context
  H2 (lexical): S₂ stays similar — vocabulary alone drives surprise
  H3 (chaos): S₂ increases — random order is maximally unpredictable

Finding 'The Intentionality Gap': the difference between original and
scrambled S₂ tells us how much of poetic deviance is *sequential* (choosing
the right word at the right moment) vs *lexical* (using unusual vocabulary
at all). This complements the found-poetry intentionality finding.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import json
import random
import re
from engine import analyze_poem, get_model

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
CORPUS_PATH = os.path.join(RESULTS_DIR, "corpus_results.json")

N_POEMS = 50
RANDOM_SEED = 42


def scramble_within_lines(text, mode="shuffle"):
    """
    Scramble word order within each line, preserving line breaks.

    mode:
      'shuffle'  - random shuffle of words in each line
      'reverse'  - reverse word order in each line
      'full'     - shuffle ALL words in the whole poem (no line structure)
    """
    if mode == "full":
        words = text.split()
        random.shuffle(words)
        return " ".join(words)

    lines = text.split("\n")
    result = []
    for line in lines:
        words = line.split()
        if len(words) <= 1:
            result.append(line)
            continue
        if mode == "shuffle":
            random.shuffle(words)
        elif mode == "reverse":
            words = list(reversed(words))
        result.append(" ".join(words))
    return "\n".join(result)


def compute_avg_s2_clean(poem_result):
    """Compute avg S₂ excluding stanza-break artifacts (p_newline < 0.9)."""
    tokens = [t for t in poem_result.get("tokens", [])
              if t.get("p_newline", 0) < 0.9]
    if not tokens:
        return None
    return sum(t["s2"] for t in tokens) / len(tokens)


def compute_summary(poem_result):
    tokens = [t for t in poem_result.get("tokens", [])
              if t.get("p_newline", 0) < 0.9]
    if not tokens:
        return None
    n = len(tokens)
    s2_vals = [t["s2"] for t in tokens]
    avg = sum(s2_vals) / n
    std = (sum((v - avg) ** 2 for v in s2_vals) / n) ** 0.5
    pos_ratio = sum(1 for v in s2_vals if v > 0) / n
    return {
        "n": n,
        "avg_s2": round(avg, 4),
        "std_s2": round(std, 4),
        "pos_ratio": round(pos_ratio, 4),
        "max_s2": round(max(s2_vals), 4),
    }


def main():
    random.seed(RANDOM_SEED)

    print("Loading corpus results...")
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    # Select poems: diverse sample, min 30 clean tokens, English only, skip control
    candidates = [
        r for r in corpus
        if r["metadata"].get("language", "en") == "en"
        and r["metadata"].get("era", "") not in ("control", "cliche_control")
        and r["metadata"].get("n_tokens", 0) >= 50
        and len(r.get("tokens", [])) >= 30
    ]

    # Stratified sample: pick from different eras
    era_map = {}
    for r in candidates:
        era = r["metadata"].get("era", "unknown")
        era_map.setdefault(era, []).append(r)

    selected = []
    eras = list(era_map.keys())
    random.shuffle(eras)
    for era in eras:
        poems = era_map[era]
        random.shuffle(poems)
        selected.extend(poems[:2])
        if len(selected) >= N_POEMS:
            break
    selected = selected[:N_POEMS]

    print(f"Analyzing {len(selected)} poems × 3 conditions (original / shuffle / reverse)...")

    # Pre-load model
    model, tokenizer, nl_tensor = get_model("en")

    results = []
    for i, poem_result in enumerate(selected):
        meta = poem_result["metadata"]
        title = meta.get("title", f"poem_{i}")
        era = meta.get("era", "unknown")
        text = None

        # Reconstruct the poem text from tokens (approximate; rejoins token strings)
        # Better: use the original corpus — load from corpus.poems
        # We'll use engine.analyze_poem with the reconstructed text
        # Actually: get text from the tokens (strip leading space from GPT-2 tokens)
        raw_tokens = poem_result.get("tokens", [])
        if not raw_tokens:
            continue

        # Reconstruct text from token strings
        # GPT-2 uses Ġ for space-prefixed tokens; decode gives actual text
        # Use original text if available, else reconstruct
        # Get text from corpus.poems directly
        pass

    # Load actual poem texts from corpus
    from corpus.poems import POEMS
    poem_lookup = {p["title"]: p["text"] for p in POEMS}

    results = []
    for i, poem_result in enumerate(selected):
        meta = poem_result["metadata"]
        title = meta.get("title", "")
        era = meta.get("era", "unknown")

        text = poem_lookup.get(title)
        if not text:
            continue

        orig_summary = compute_summary(poem_result)
        if orig_summary is None:
            continue

        # Scrambled versions
        shuffle_text = scramble_within_lines(text, "shuffle")
        reverse_text = scramble_within_lines(text, "reverse")
        full_shuffle_text = scramble_within_lines(text, "full")

        try:
            shuffle_result = analyze_poem(shuffle_text, title=title + " [SHUFFLE]", era=era)
            reverse_result = analyze_poem(reverse_text, title=title + " [REVERSE]", era=era)
            full_result = analyze_poem(full_shuffle_text, title=title + " [FULL]", era=era)
        except Exception as e:
            print(f"  Error on '{title}': {e}")
            continue

        shuffle_sum = compute_summary(shuffle_result)
        reverse_sum = compute_summary(reverse_result)
        full_sum = compute_summary(full_result)

        entry = {
            "title": title,
            "era": era,
            "original": orig_summary,
            "shuffle": shuffle_sum,
            "reverse": reverse_sum,
            "full_shuffle": full_sum,
        }

        if shuffle_sum:
            entry["delta_shuffle"] = round(shuffle_sum["avg_s2"] - orig_summary["avg_s2"], 4)
        if reverse_sum:
            entry["delta_reverse"] = round(reverse_sum["avg_s2"] - orig_summary["avg_s2"], 4)
        if full_sum:
            entry["delta_full"] = round(full_sum["avg_s2"] - orig_summary["avg_s2"], 4)

        results.append(entry)
        pct = (i + 1) / len(selected) * 100
        print(
            f"  [{i+1:2d}/{len(selected)}] {title[:45]:45s} "
            f"orig={orig_summary['avg_s2']:+.3f} "
            f"shuffle={shuffle_sum['avg_s2'] if shuffle_sum else 'err':+.3f} "
            f"Δ={entry.get('delta_shuffle', 'err'):+.3f}"
        )

    # Aggregate stats
    deltas_shuffle = [r["delta_shuffle"] for r in results if "delta_shuffle" in r]
    deltas_reverse = [r["delta_reverse"] for r in results if "delta_reverse" in r]
    deltas_full = [r["delta_full"] for r in results if "delta_full" in r]

    def _stats(vals):
        if not vals:
            return {}
        n = len(vals)
        mean = sum(vals) / n
        return {
            "n": n,
            "mean": round(mean, 4),
            "std": round((sum((v - mean) ** 2 for v in vals) / n) ** 0.5, 4),
            "min": round(min(vals), 4),
            "max": round(max(vals), 4),
            "pct_positive": round(sum(1 for v in vals if v > 0) / n, 4),
        }

    summary = {
        "delta_shuffle": _stats(deltas_shuffle),
        "delta_reverse": _stats(deltas_reverse),
        "delta_full": _stats(deltas_full),
    }

    print("\n=== AGGREGATE RESULTS ===")
    for cond, stats in summary.items():
        print(f"  {cond}: mean Δ={stats.get('mean', '?'):+.4f}  "
              f"std={stats.get('std', '?'):.4f}  "
              f"pct_positive={stats.get('pct_positive', '?'):.1%}")

    # Save
    output = {
        "experiment": "word_order_scramble",
        "n_poems": len(results),
        "aggregate": summary,
        "per_poem": results,
    }

    out_path = os.path.join(RESULTS_DIR, "word_order_scramble.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nResults saved to {out_path}")
    return output


if __name__ == "__main__":
    main()
