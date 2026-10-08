"""
Prediction Field Homogeneity vs. S₂

When GPT-2's top-10 predicted tokens all belong to the same lexical class
(function word, punctuation, content word), does the poet's choice carry
more information than when the prediction field is "split" across classes?

Tests the hypothesis: the Straussian gap is deepest when the poet breaks
a *coherent* prediction field — where language statistics converge on a
single lexical category, and the poet refuses it entirely.
"""

import json
import sys
import os
from collections import defaultdict
import statistics

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")
ARTIFACT_P = 0.90

FUNCTION_WORDS = {
    "the", "a", "an", "of", "in", "to", "and", "or", "but", "is", "are",
    "was", "were", "be", "been", "being", "have", "has", "had", "will",
    "would", "could", "should", "may", "might", "can", "shall", "do",
    "does", "did", "that", "this", "these", "those", "it", "its", "i",
    "my", "me", "we", "our", "you", "your", "he", "she", "they", "his",
    "her", "their", "him", "them", "on", "at", "by", "for", "from",
    "with", "as", "if", "not", "no", "so", "up", "out", "all", "about",
    "into", "through", "when", "which", "who", "what", "how", "there",
    "than", "then", "now", "also", "more", "one", "just", "over",
    "under", "after", "before", "between", "while", "though", "although",
    "because", "since", "until", "where", "like", "even", "still",
    "yet", "only", "both", "each", "every", "any", "such", "own",
    "same", "much", "many", "some", "few", "its", "whose", "whom",
    "nor", "neither", "either", "whether", "once", "again",
}

PUNCT_CHARS = set(".,;:!?\"'()[]{}—-–...``''\"\"/*\\")


def classify_token(token_str):
    """Classify a GPT-2 subword token as function, punctuation, or content."""
    s = token_str.strip()
    if not s:
        return "whitespace"
    # Newlines and whitespace
    if all(c in "\n\r\t " for c in token_str):
        return "whitespace"
    # Strip leading space (GPT-2 uses Ġ prefix represented as ' ')
    word = s.lstrip()
    # Check punctuation-dominated
    if all(c in ".,;:!?\"'()[]{}—-–…*\\/`" or c == '"' or c == '"' or c == "'" or c == "'" for c in word):
        return "punctuation"
    # Check function word (whole token matches)
    lower = word.lower()
    if lower in FUNCTION_WORDS:
        return "function"
    return "content"


def newline_prob(tok):
    return sum(a["prob"] for a in tok["alternatives"] if a["token"].strip("\r\n") == "")


def compute_field_homogeneity(alternatives):
    """Compute prediction field stats: dominant class, homogeneity score, mass in class."""
    classes = [classify_token(a["token"]) for a in alternatives]
    probs   = [a["prob"] for a in alternatives]

    class_mass = defaultdict(float)
    class_count = defaultdict(int)
    for cls, prob in zip(classes, probs):
        class_mass[cls] += prob
        class_count[cls] += 1

    total_prob = sum(probs)
    if total_prob == 0:
        return "unknown", 0.0, 0.0, 0

    # Dominant class by probability mass
    dominant_class = max(class_mass, key=lambda c: class_mass[c])
    dominant_mass = class_mass[dominant_class] / total_prob
    dominant_count_frac = class_count[dominant_class] / len(alternatives)
    n_classes = len([c for c in class_mass if class_mass[c] > 0.05 * total_prob])

    return dominant_class, dominant_mass, dominant_count_frac, n_classes


def run_experiment():
    with open(RESULTS_PATH) as f:
        results = json.load(f)

    # Buckets: (dominant_class, is_poet_same_class, is_high_s2) → [s2 values]
    data = []

    for poem in results:
        if poem["metadata"].get("is_control"):
            continue
        tokens = poem["tokens"]
        for tok in tokens:
            # Skip stanza-break artifacts
            if newline_prob(tok) >= ARTIFACT_P:
                continue
            if len(tok.get("alternatives", [])) < 5:
                continue

            s2 = tok["s2"]
            alts = tok["alternatives"]

            dom_class, dom_mass, dom_count_frac, n_classes = compute_field_homogeneity(alts)
            poet_class = classify_token(tok["token"])

            # Homogeneity level
            if dom_mass >= 0.70:
                homogeneity = "high"
            elif dom_mass >= 0.45:
                homogeneity = "medium"
            else:
                homogeneity = "low"

            poet_matches_field = (poet_class == dom_class)

            data.append({
                "s2": s2,
                "dom_class": dom_class,
                "dom_mass": dom_mass,
                "dom_count_frac": dom_count_frac,
                "n_classes": n_classes,
                "homogeneity": homogeneity,
                "poet_class": poet_class,
                "poet_matches_field": poet_matches_field,
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
            })

    # --- Analysis 1: Mean S₂ by prediction field type ---
    print(f"\nTotal artifact-free tokens analyzed: {len(data)}")
    print("\n=== Mean S₂ by Dominant Prediction Field Class ===")
    by_dom = defaultdict(list)
    for d in data:
        by_dom[d["dom_class"]].append(d["s2"])
    for cls in sorted(by_dom, key=lambda c: -statistics.mean(by_dom[c])):
        vals = by_dom[cls]
        print(f"  {cls:12s}: n={len(vals):5d}  mean S₂={statistics.mean(vals):+.3f}  "
              f"median={statistics.median(vals):+.3f}  pos%={sum(1 for v in vals if v>0)/len(vals):.1%}")

    # --- Analysis 2: Mean S₂ by (field type × poet matches/breaks field) ---
    print("\n=== Mean S₂ by (Field Type × Poet Matches/Breaks) ===")
    by_combo = defaultdict(list)
    for d in data:
        key = (d["dom_class"], "match" if d["poet_matches_field"] else "break")
        by_combo[key].append(d["s2"])

    for cls in ["function", "punctuation", "content", "whitespace"]:
        for match in ["match", "break"]:
            key = (cls, match)
            vals = by_combo.get(key, [])
            if not vals:
                continue
            print(f"  {cls:12s} | {match:5s}: n={len(vals):5d}  mean S₂={statistics.mean(vals):+.3f}  "
                  f"median={statistics.median(vals):+.3f}  pos%={sum(1 for v in vals if v>0)/len(vals):.1%}")

    # --- Analysis 3: S₂ by homogeneity × field type ---
    print("\n=== Mean S₂ by Prediction Field Homogeneity (function field only) ===")
    func_high = [d for d in data if d["dom_class"] == "function" and d["homogeneity"] == "high"]
    func_med  = [d for d in data if d["dom_class"] == "function" and d["homogeneity"] == "medium"]
    func_low  = [d for d in data if d["dom_class"] == "function" and d["homogeneity"] == "low"]

    for label, subset in [("high (>70% mass)", func_high), ("medium (45-70%)", func_med), ("low (<45%)", func_low)]:
        if not subset:
            continue
        vals = [d["s2"] for d in subset]
        match_pct = sum(1 for d in subset if d["poet_matches_field"]) / len(subset)
        print(f"  Function field {label:25s}: n={len(subset):5d}  mean S₂={statistics.mean(vals):+.3f}  "
              f"field_match%={match_pct:.1%}")

    # --- Analysis 4: When GPT-2 has a content word consensus, what do poets choose? ---
    print("\n=== Content-Word Consensus Predictions: Poet Behavior ===")
    content_high = [d for d in data if d["dom_class"] == "content" and d["homogeneity"] == "high"]
    print(f"  Tokens where GPT-2 strongly expected a content word: {len(content_high)}")
    if content_high:
        poet_classes = defaultdict(list)
        for d in content_high:
            poet_classes[d["poet_class"]].append(d["s2"])
        for cls in sorted(poet_classes, key=lambda c: -len(poet_classes[c])):
            vals = poet_classes[cls]
            print(f"    Poet chose {cls:12s}: n={len(vals):4d}  mean S₂={statistics.mean(vals):+.3f}")

    # --- Analysis 5: N-classes in prediction field vs. S₂ ---
    print("\n=== S₂ by Number of Lexical Classes in Top-10 Predictions ===")
    by_nclass = defaultdict(list)
    for d in data:
        by_nclass[d["n_classes"]].append(d["s2"])
    for n in sorted(by_nclass):
        vals = by_nclass[n]
        print(f"  {n} class(es) in top-10: n={len(vals):5d}  mean S₂={statistics.mean(vals):+.3f}  "
              f"pos%={sum(1 for v in vals if v>0)/len(vals):.1%}")

    # --- Analysis 6: The "consensus break" premium ---
    print("\n=== The Consensus-Break S₂ Premium ===")
    # High homogeneity function field, poet breaks (high S₂) vs. low homogeneity (low S₂ baseline)
    consensus_break = [d["s2"] for d in data
                       if d["dom_class"] == "function"
                       and d["homogeneity"] == "high"
                       and not d["poet_matches_field"]]
    within_consensus = [d["s2"] for d in data
                        if d["dom_class"] == "function"
                        and d["homogeneity"] == "high"
                        and d["poet_matches_field"]]
    mixed_field = [d["s2"] for d in data if d["homogeneity"] == "low"]

    print(f"  Break strong function consensus:  n={len(consensus_break):5d}  mean S₂={statistics.mean(consensus_break) if consensus_break else 0:+.3f}")
    print(f"  Match strong function consensus:  n={len(within_consensus):5d}  mean S₂={statistics.mean(within_consensus) if within_consensus else 0:+.3f}")
    print(f"  Mixed prediction field (low hom): n={len(mixed_field):5d}  mean S₂={statistics.mean(mixed_field) if mixed_field else 0:+.3f}")

    if consensus_break and within_consensus:
        premium = statistics.mean(consensus_break) - statistics.mean(within_consensus)
        print(f"  Consensus-break S₂ premium: {premium:+.3f} bits")

    return data


if __name__ == "__main__":
    data = run_experiment()
