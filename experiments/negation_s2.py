"""
Negation and the Double Bind: S2 profiles at negation sites in poetry.

Hypothesis:
  - Negation words (not, no, never, nor, neither, without, etc.) force a
    "double construction": the reader must build the affirmed version and
    then cancel it.
  - The negation token itself may have lower S2 (it's often structurally
    predictable — poetry often needs to negate) or higher S2 if unexpected.
  - The token FOLLOWING negation should have systematically different S2
    than the same token in non-negated context (the post-negation space is
    semantically constrained in a different way).
  - Poems that use more negation might have different global S2 profiles.

Analysis:
  1. Identify negation tokens (token text matching negation vocab).
  2. Compare S2 of negation tokens vs. overall non-negation distribution.
  3. Compare S2 of post-negation tokens vs. all other tokens (same-class).
  4. Measure per-poem negation density and correlate with overall S2.
  5. Look at strongest negation "swerves": what did GPT-2 expect before
     the negation, and what did the poet deny?
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/negation_s2.json"
P_NEWLINE_MAX = 0.9

# Core negation words (stripped/lowercased token text)
NEGATION_WORDS = {
    "not", "no", "never", "nor", "neither", "without",
    "n't", "nt", "nothing", "nowhere", "nobody", "none",
    "hardly", "scarcely", "barely",
}

# Also catch "un-" and "-less" prefixes/suffixes
def is_negation_prefix(tok_text):
    t = tok_text.strip().lower()
    return t.startswith("un") and len(t) > 3

def is_negation_suffix(tok_text):
    t = tok_text.strip().lower()
    return t.endswith("less") and len(t) > 5


def load_corpus(path):
    with open(path) as f:
        return json.load(f)


def clean_tokens(poem):
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < P_NEWLINE_MAX]


def token_text_clean(t):
    return t["token"].strip().lower()


def is_negation(tok):
    t = token_text_clean(tok)
    return (t in NEGATION_WORDS or
            is_negation_prefix(tok["token"]) or
            is_negation_suffix(tok["token"]))


def pearson(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx)**2 for x in xs))
    dy = math.sqrt(sum((y - my)**2 for y in ys))
    return num / (dx * dy) if dx * dy > 0 else float("nan")


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")


def stdev(xs):
    if len(xs) < 2:
        return float("nan")
    m = mean(xs)
    return math.sqrt(sum((x - m)**2 for x in xs) / (len(xs) - 1))


def main():
    corpus = load_corpus(CORPUS_PATH)

    neg_s2 = []          # S2 of negation tokens
    neg_ent = []         # entropy of negation tokens
    post_neg_s2 = []     # S2 of token immediately after negation
    non_neg_s2 = []      # S2 of all non-negation, non-post-negation tokens
    all_token_s2 = []    # S2 of all clean tokens

    per_poem = []        # per-poem stats

    # Examples of biggest negation S2 swerves
    top_neg = []         # (s2, token, prev_alts, poem_title, neg_word)
    top_post_neg = []    # (s2, token, neg_word, poem_title)

    for poem in corpus:
        meta = poem["metadata"]
        toks = clean_tokens(poem)
        if len(toks) < 10:
            continue

        poem_neg_s2 = []
        poem_post_neg_s2 = []
        poem_non_neg_s2 = []

        neg_count = 0
        i = 0
        while i < len(toks):
            t = toks[i]
            all_token_s2.append(t["s2"])
            if is_negation(t):
                neg_count += 1
                neg_s2.append(t["s2"])
                neg_ent.append(t["entropy"])
                poem_neg_s2.append(t["s2"])
                top_neg.append({
                    "s2": t["s2"],
                    "neg_token": t["token"],
                    "entropy": t["entropy"],
                    "surprisal": t["surprisal"],
                    "top_alts": [a["token"] for a in t.get("alternatives", [])[:5]],
                    "title": meta.get("title", "unknown"),
                    "poet": meta.get("poet", "unknown"),
                })
                # Post-negation token
                if i + 1 < len(toks):
                    post = toks[i + 1]
                    post_neg_s2.append(post["s2"])
                    poem_post_neg_s2.append(post["s2"])
                    top_post_neg.append({
                        "s2": post["s2"],
                        "post_token": post["token"],
                        "neg_token": t["token"],
                        "post_entropy": post["entropy"],
                        "post_surprisal": post["surprisal"],
                        "post_alts": [a["token"] for a in post.get("alternatives", [])[:5]],
                        "title": meta.get("title", "unknown"),
                        "poet": meta.get("poet", "unknown"),
                    })
                i += 1
            else:
                non_neg_s2.append(t["s2"])
                poem_non_neg_s2.append(t["s2"])
                i += 1

        n_clean = len(toks)
        neg_density = neg_count / n_clean if n_clean > 0 else 0
        per_poem.append({
            "title": meta.get("title", "unknown"),
            "poet": meta.get("poet", "unknown"),
            "era": meta.get("era", "unknown"),
            "n_clean": n_clean,
            "neg_count": neg_count,
            "neg_density": neg_density,
            "mean_s2_overall": mean(all_token_s2[-n_clean:]),
            "mean_neg_s2": mean(poem_neg_s2),
            "mean_post_neg_s2": mean(poem_post_neg_s2),
            "mean_non_neg_s2": mean(poem_non_neg_s2),
        })

    # Sort examples
    top_neg.sort(key=lambda x: abs(x["s2"]), reverse=True)
    top_post_neg.sort(key=lambda x: x["s2"], reverse=True)

    # Negation density vs overall S2 correlation
    valid = [(p["neg_density"], p["mean_s2_overall"])
             for p in per_poem if not math.isnan(p["mean_s2_overall"]) and p["neg_count"] > 0]
    neg_densities = [x[0] for x in valid]
    overall_s2s = [x[1] for x in valid]
    r_density_s2 = pearson(neg_densities, overall_s2s)

    # By era
    era_stats = defaultdict(lambda: {"neg_s2": [], "post_neg_s2": [], "non_neg_s2": [], "densities": []})
    for p in per_poem:
        e = p["era"]
        if not math.isnan(p.get("mean_neg_s2", float("nan"))):
            era_stats[e]["neg_s2"].append(p["mean_neg_s2"])
        if not math.isnan(p.get("mean_post_neg_s2", float("nan"))):
            era_stats[e]["post_neg_s2"].append(p["mean_post_neg_s2"])
        era_stats[e]["densities"].append(p["neg_density"])

    era_summary = {}
    for era, d in era_stats.items():
        era_summary[era] = {
            "mean_neg_s2": mean(d["neg_s2"]),
            "mean_post_neg_s2": mean(d["post_neg_s2"]),
            "mean_neg_density": mean(d["densities"]),
            "n_poems": len(d["densities"]),
        }

    # Highest-density negation poems
    high_neg_poems = sorted(per_poem, key=lambda x: x["neg_density"], reverse=True)[:10]

    results = {
        "n_poems": len(per_poem),
        "n_neg_tokens": len(neg_s2),
        "n_post_neg_tokens": len(post_neg_s2),
        "corpus_stats": {
            "mean_neg_s2": mean(neg_s2),
            "stdev_neg_s2": stdev(neg_s2),
            "mean_post_neg_s2": mean(post_neg_s2),
            "stdev_post_neg_s2": stdev(post_neg_s2),
            "mean_non_neg_s2": mean(non_neg_s2),
            "stdev_non_neg_s2": stdev(non_neg_s2),
            "mean_all_s2": mean(all_token_s2),
            "mean_neg_entropy": mean(neg_ent),
            "neg_pos_rate": sum(1 for x in neg_s2 if x > 0) / len(neg_s2) if neg_s2 else 0,
            "post_neg_pos_rate": sum(1 for x in post_neg_s2 if x > 0) / len(post_neg_s2) if post_neg_s2 else 0,
            "non_neg_pos_rate": sum(1 for x in non_neg_s2 if x > 0) / len(non_neg_s2) if non_neg_s2 else 0,
        },
        "r_neg_density_vs_overall_s2": r_density_s2,
        "era_summary": era_summary,
        "top_neg_swerves": top_neg[:20],
        "top_post_neg_swerves": top_post_neg[:20],
        "high_density_poems": high_neg_poems,
        "per_poem": per_poem,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Done. {len(per_poem)} poems, {len(neg_s2)} negation tokens, {len(post_neg_s2)} post-neg tokens.")
    print(f"Mean S2: negation={mean(neg_s2):.3f}, post-neg={mean(post_neg_s2):.3f}, non-neg={mean(non_neg_s2):.3f}")
    print(f"Correlation neg_density ~ overall_s2: r={r_density_s2:.3f}")


if __name__ == "__main__":
    main()
