"""
Intensifiers and Degree Markers in Poetry: S2 Analysis

Research question: Do intensifiers (very, so, quite, utterly, etc.)
tend to precede high-S2 tokens? Do they signal that the poet is about
to do something unexpected, or do they precede predictable words?

Hypothesis: In skilled poetry, intensifiers often precede surprising
word choices — the intensifier is a "confidence builder" before the
deviation. In prose, intensifiers may precede more predictable words.

Also: do intensifiers themselves carry high or low S2?
"""

import json
import re
import sys
from collections import defaultdict
from statistics import mean, stdev

RESULTS_PATH = "results/corpus_results.json"

# Degree adverbs and intensifiers
INTENSIFIERS = {
    # Boosters (amplifiers)
    " very", " so", " quite", " rather", " extremely", " utterly",
    " absolutely", " entirely", " completely", " totally", " wholly",
    " deeply", " greatly", " highly", " strongly", " purely", " truly",
    " terribly", " awfully", " dreadfully", " frightfully", " horribly",
    " wonderfully", " beautifully", " remarkably", " incredibly", " terribly",
    " supremely", " infinitely", " endlessly", " eternally", " perfectly",
    " simply", " merely", " merely", " only", " just", " barely",
    " scarcely", " hardly", " nearly", " almost",
    # Downtoners
    " somewhat", " rather", " fairly", " pretty", " mildly", " slightly",
    " partly", " partially",
}

# Presupposition triggers (separate category)
PRESUPPOSITION_TRIGGERS = {
    " again", " still", " yet", " already", " also", " too", " even",
    " anymore", " back", " anymore", " once", " once more", " another",
}


def strip_newline(token_str: str) -> str:
    return token_str.replace("\n", "\\n")


def classify_intensifier(token_str: str) -> str:
    t = token_str.lower()
    if t in INTENSIFIERS:
        return "intensifier"
    if t in PRESUPPOSITION_TRIGGERS:
        return "presupposition"
    return None


def analyze(data):
    # Track: for each intensifier token, what is S2 of the NEXT token?
    intensifier_next_s2 = []
    presupposition_next_s2 = []

    # S2 of intensifiers themselves
    intensifier_self_s2 = []
    presupposition_self_s2 = []

    # Baseline: S2 of all non-newline, non-special tokens
    all_token_s2 = []

    # By era
    era_intensifier_density = defaultdict(list)  # intensifiers per 100 tokens
    era_next_s2 = defaultdict(list)

    # Best examples: intensifier → high-S2 next token
    examples = []

    for poem in data:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        tokens = poem["tokens"]
        n = len(tokens)

        intensifier_count = 0

        for i, tok in enumerate(tokens):
            t = tok["token"]
            s2 = tok["s2"]
            p_nl = tok.get("p_newline", 0)

            # Skip newline artifacts
            if t.strip() == "" or p_nl > 0.7:
                continue

            all_token_s2.append(s2)

            kind = classify_intensifier(t)

            if kind == "intensifier":
                intensifier_self_s2.append(s2)
                intensifier_count += 1

                # Look at next non-newline token
                if i + 1 < n:
                    next_tok = tokens[i + 1]
                    next_s2 = next_tok["s2"]
                    next_p_nl = next_tok.get("p_newline", 0)

                    if next_p_nl <= 0.7:
                        intensifier_next_s2.append(next_s2)
                        era_next_s2[era].append(next_s2)

                        # Collect good examples
                        examples.append({
                            "poem": meta["title"],
                            "author": meta["author"],
                            "era": era,
                            "intensifier": t,
                            "next_token": next_tok["token"],
                            "next_s2": next_s2,
                            "context": tok.get("context_before", ""),
                        })

            elif kind == "presupposition":
                presupposition_self_s2.append(s2)

                if i + 1 < n:
                    next_tok = tokens[i + 1]
                    next_s2 = next_tok["s2"]
                    next_p_nl = next_tok.get("p_newline", 0)

                    if next_p_nl <= 0.7:
                        presupposition_next_s2.append(next_s2)

        # Per-poem intensity density
        n_clean = sum(1 for t in tokens
                      if t["token"].strip() and t.get("p_newline", 0) <= 0.7)
        if n_clean > 0:
            density = intensifier_count / n_clean * 100
            era_intensifier_density[era].append(density)

    return {
        "all_token_s2": all_token_s2,
        "intensifier_self_s2": intensifier_self_s2,
        "presupposition_self_s2": presupposition_self_s2,
        "intensifier_next_s2": intensifier_next_s2,
        "presupposition_next_s2": presupposition_next_s2,
        "era_intensifier_density": era_intensifier_density,
        "era_next_s2": era_next_s2,
        "examples": examples,
    }


def main():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    print(f"Analyzing {len(data)} texts...")
    results = analyze(data)

    baseline_mean = mean(results["all_token_s2"])
    baseline_std = stdev(results["all_token_s2"])

    print("\n=== INTENSIFIERS (self S2) ===")
    if results["intensifier_self_s2"]:
        im = mean(results["intensifier_self_s2"])
        print(f"  n={len(results['intensifier_self_s2'])}, mean S2={im:.3f} (baseline={baseline_mean:.3f})")
        print(f"  z-score vs baseline: {(im - baseline_mean)/baseline_std:.2f}")

    print("\n=== NEXT TOKEN AFTER INTENSIFIER ===")
    if results["intensifier_next_s2"]:
        nm = mean(results["intensifier_next_s2"])
        print(f"  n={len(results['intensifier_next_s2'])}, mean S2={nm:.3f} (baseline={baseline_mean:.3f})")
        print(f"  z-score vs baseline: {(nm - baseline_mean)/baseline_std:.2f}")

    print("\n=== PRESUPPOSITION TRIGGERS (self S2) ===")
    if results["presupposition_self_s2"]:
        pm = mean(results["presupposition_self_s2"])
        print(f"  n={len(results['presupposition_self_s2'])}, mean S2={pm:.3f} (baseline={baseline_mean:.3f})")

    print("\n=== NEXT TOKEN AFTER PRESUPPOSITION ===")
    if results["presupposition_next_s2"]:
        pnm = mean(results["presupposition_next_s2"])
        print(f"  n={len(results['presupposition_next_s2'])}, mean S2={pnm:.3f} (baseline={baseline_mean:.3f})")

    print("\n=== ERA: Intensifier density (per 100 tokens) ===")
    era_dens = [(era, mean(vals), len(vals))
                for era, vals in results["era_intensifier_density"].items()
                if vals]
    era_dens.sort(key=lambda x: -x[1])
    for era, dens, n in era_dens[:15]:
        print(f"  {era:25s}: {dens:.2f}  (n_poems={n})")

    print("\n=== TOP 15 INTENSIFIER → HIGH-S2 NEXT TOKEN EXAMPLES ===")
    top = sorted(results["examples"], key=lambda x: -x["next_s2"])[:15]
    for ex in top:
        print(f"  [{ex['era']}] {ex['author']}: ...{ex['intensifier'].strip()} → '{ex['next_token'].strip()}' (S2={ex['next_s2']:.2f})")

    # Save JSON
    output = {
        "baseline_mean_s2": baseline_mean,
        "baseline_std_s2": baseline_std,
        "intensifier_self_mean_s2": mean(results["intensifier_self_s2"]) if results["intensifier_self_s2"] else None,
        "intensifier_next_mean_s2": mean(results["intensifier_next_s2"]) if results["intensifier_next_s2"] else None,
        "presupposition_self_mean_s2": mean(results["presupposition_self_s2"]) if results["presupposition_self_s2"] else None,
        "presupposition_next_mean_s2": mean(results["presupposition_next_s2"]) if results["presupposition_next_s2"] else None,
        "n_intensifier_tokens": len(results["intensifier_self_s2"]),
        "n_presupposition_tokens": len(results["presupposition_self_s2"]),
        "era_density": {era: {"mean_density": mean(vals), "n_poems": len(vals)}
                        for era, vals in results["era_intensifier_density"].items() if vals},
        "top_examples": top,
    }

    with open("results/intensifier_s2.json", "w") as f:
        json.dump(output, f, indent=2)
    print("\nSaved results/intensifier_s2.json")
    return output


if __name__ == "__main__":
    main()
