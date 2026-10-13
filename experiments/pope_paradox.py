"""
The Pope Paradox: Why Do Heroic Couplets Produce Q1 Rather Than Q2 Surprise?

Background:
  The Q2/Q1 taxonomy (2026-10-11) found Alexander Pope to be the most extreme Q1
  strategist (Q2/Q1 ratio = 0.13) despite writing in closed heroic couplets — a form
  that should produce Q2 "syntax trap" moments (model expects line-end, gets continuation).
  This paradox was flagged as requiring investigation.

This experiment:
  1. Analyzes all Pope poems in the corpus in detail at the quadrant level
  2. Compares Pope with other Q1-dominant poets (Milton, Donne, Keats, Dryden, Johnson)
     vs Q2-dominant poets (Merwin, Edson, Forché, O'Hara)
  3. At Q1 moments, examines:
     a. Was it a function word or content word that surprised GPT-2?
     b. What was H_top10 (entropy of alternatives field)?
     c. What category of word did the model predict vs. what appeared?
  4. Tests the "archaic diction" hypothesis:
     Pope's Latinate, elevated 18th-century vocabulary creates HIGH prediction entropy
     (GPT-2 can't form confident predictions) — creating Q1 dominance NOT because of
     structural complexity (Milton/Donne) but because of LEXICAL alienness.

Results saved to: results/pope_paradox.json
"""

import json
import re
import math
from collections import defaultdict, Counter
from statistics import mean, stdev, median

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH  = "results/pope_paradox.json"

# Thresholds from Q2/Q1 taxonomy
SURP_MEDIAN  = 4.77
ENT_MEDIAN   = 6.34
S2_THRESHOLD = 2.0

PUNCTUATION_TOKENS = {",", ".", "!", "?", ";", ":", "'", '"', "-", "—", "(", ")", "/", "\\"}
NEWLINE_OR_SPACE   = re.compile(r"^[\n\r\s]+$")

FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "nor", "for", "yet", "so",
    "in", "on", "at", "to", "of", "with", "by", "from", "up", "about",
    "into", "through", "during", "before", "after", "above", "below",
    "between", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "that", "which",
    "who", "whom", "whose", "what", "this", "these", "those", "it", "its",
    "he", "she", "they", "we", "you", "i", "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their", "not", "no", "nor", "if", "as",
    "when", "where", "how", "than", "then", "there", "here", "all", "each",
    "both", "either", "neither", "such", "same", "own", "other",
}


def is_artifact(tok):
    nl_prob = sum(a["prob"] for a in tok.get("alternatives", [])
                  if NEWLINE_OR_SPACE.match(a["token"]))
    return nl_prob >= 0.90


def classify_quadrant(tok):
    s = tok["surprisal"]
    e = tok["entropy"]
    if s > SURP_MEDIAN and e > ENT_MEDIAN:
        return "Q1"
    elif s > SURP_MEDIAN and e <= ENT_MEDIAN:
        return "Q2"
    elif s <= SURP_MEDIAN and e <= ENT_MEDIAN:
        return "Q3"
    else:
        return "Q4"


def token_type(text):
    stripped = text.strip()
    if not stripped:
        return "whitespace"
    if stripped in PUNCTUATION_TOKENS or (len(stripped) == 1 and not stripped.isalpha()):
        return "punctuation"
    lower = stripped.lower().lstrip("'\"")
    if lower in FUNCTION_WORDS:
        return "function"
    return "content"


def top_alt_type(alternatives):
    if not alternatives:
        return "unknown"
    top = alternatives[0]["token"]
    stripped = top.strip()
    if not stripped or NEWLINE_OR_SPACE.match(top):
        return "newline/space"
    if stripped in PUNCTUATION_TOKENS or (len(stripped) == 1 and not stripped.isalpha()):
        return "punctuation"
    lower = stripped.lower().lstrip("'\"")
    if lower in FUNCTION_WORDS:
        return "function"
    return "content"


def h_top10(alternatives):
    """Shannon entropy of top-10 alternatives (normalized to sum to 1)."""
    if not alternatives:
        return 0.0
    probs = [a["prob"] for a in alternatives[:10]]
    Z = sum(probs)
    if Z <= 0:
        return 0.0
    return -sum((p / Z) * math.log2(p / Z) for p in probs if p > 0)


def analyze_poet(poems_data):
    """Compute Q1/Q2 breakdown and token-level diagnostics for a set of poems."""
    q1_tokens = []
    q2_tokens = []
    all_high_s2 = []

    for poem in poems_data:
        for tok in poem.get("tokens", []):
            if is_artifact(tok):
                continue
            s2_val = tok.get("s2", tok["surprisal"] - tok["entropy"])
            if s2_val < S2_THRESHOLD:
                continue
            quad = classify_quadrant(tok)
            tt = token_type(tok["token"])
            alt_type = top_alt_type(tok.get("alternatives", []))
            h10 = h_top10(tok.get("alternatives", []))
            record = {
                "token": tok["token"],
                "s2": round(s2_val, 3),
                "surprisal": round(tok["surprisal"], 3),
                "entropy": round(tok["entropy"], 3),
                "quadrant": quad,
                "token_type": tt,
                "top1_predicted_type": alt_type,
                "top1_predicted": tok["alternatives"][0]["token"] if tok.get("alternatives") else "",
                "top1_prob": round(tok["alternatives"][0]["prob"], 4) if tok.get("alternatives") else 0,
                "h_top10": round(h10, 4),
            }
            all_high_s2.append(record)
            if quad == "Q1":
                q1_tokens.append(record)
            elif quad == "Q2":
                q2_tokens.append(record)

    if not all_high_s2:
        return None

    q1_n = len(q1_tokens)
    q2_n = len(q2_tokens)
    ratio = q2_n / q1_n if q1_n > 0 else float("inf")

    def summarize_group(group):
        if not group:
            return {}
        return {
            "n": len(group),
            "mean_s2": round(mean(t["s2"] for t in group), 3),
            "mean_h10": round(mean(t["h_top10"] for t in group), 4),
            "mean_top1_prob": round(mean(t["top1_prob"] for t in group), 4),
            "token_type_dist": dict(Counter(t["token_type"] for t in group)),
            "top1_predicted_type_dist": dict(Counter(t["top1_predicted_type"] for t in group)),
            "top_actual_tokens": [t["token"].strip() for t in sorted(group, key=lambda x: -x["s2"])[:10]],
            "top_predicted_tokens": [t["top1_predicted"].strip()
                                      for t in sorted(group, key=lambda x: -x["s2"])[:10]],
        }

    return {
        "q1_n": q1_n,
        "q2_n": q2_n,
        "q2_q1_ratio": round(ratio, 3),
        "total_high_s2": len(all_high_s2),
        "q1": summarize_group(q1_tokens),
        "q2": summarize_group(q2_tokens),
        "q1_vs_q2_h10_gap": round(
            (mean(t["h_top10"] for t in q1_tokens) - mean(t["h_top10"] for t in q2_tokens))
            if q1_tokens and q2_tokens else 0, 4
        ),
    }


def main():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Group poems by author — keep only English-language poems
    by_author = defaultdict(list)
    for poem in corpus:
        meta = poem.get("metadata", poem)
        lang = meta.get("language", "en")
        if lang != "en":
            continue
        author = meta.get("author", "Unknown")
        by_author[author].append(poem)

    # Poets of interest: Q1-dominant (archaic/formal) vs Q2-dominant (colloquial)
    # Based on Q2/Q1 taxonomy findings
    FOCAL_POETS = {
        # Q1-dominant — expected to avoid syntax traps
        "Alexander Pope":        "Q1-dominant (neoclassical heroic couplets)",
        "John Milton":           "Q1-dominant (Latinate epic syntax)",
        "John Donne":            "Q1-dominant (metaphysical conceits)",
        "John Keats":            "Q1-dominant (ode syntax, archaism)",
        "George Herbert":        "Q1-dominant (devotional syntax)",
        "Gerard Manley Hopkins": "Q1-dominant (sprung rhythm, compound forms)",
        "W.B. Yeats":            "Q1-dominant (late archaic)",
        "John Dryden":           "Q1-dominant (neoclassical satire)",
        "Samuel Johnson":        "Q1-dominant (neoclassical didactic)",
        # Q2-dominant — expected to exploit syntax traps
        "W.S. Merwin":           "Q2-dominant (punctuation-free, syntax traps)",
        "Russell Edson":         "Q2-dominant (prose fabulist, sudden pivots)",
        "Frank O'Hara":          "Q2-dominant (casual syntax, surprising objects)",
        "Carolyn Forché":        "Q2-dominant (documentary prose)",
        "William Carlos Williams": "Q2-dominant (imagist, bare syntax)",
    }

    results = {}
    for author, description in FOCAL_POETS.items():
        poems = by_author.get(author, [])
        if not poems:
            # Try partial match
            for a in by_author:
                if author.split()[-1].lower() in a.lower() and author.split()[0].lower() in a.lower():
                    poems = by_author[a]
                    break
        if not poems:
            results[author] = {"description": description, "error": "not in corpus"}
            continue

        analysis = analyze_poet(poems)
        if analysis is None:
            results[author] = {"description": description, "error": "insufficient high-S2 tokens"}
            continue

        results[author] = {
            "description": description,
            "n_poems": len(poems),
            **analysis,
        }
        print(f"{author}: Q2/Q1={analysis['q2_q1_ratio']:.2f}  "
              f"Q1_h10={analysis['q1'].get('mean_h10','?'):.3f}  "
              f"Q2_h10={analysis['q2'].get('mean_h10','?'):.3f}  "
              f"h10_gap={analysis['q1_vs_q2_h10_gap']:.3f}")

    # Additional analysis: neoclassical era as a whole vs modernist
    era_results = {}
    ERA_GROUPS = {
        "18th_century": "Neoclassical (Pope, Dryden, Johnson, Smart, Wheatley)",
        "metaphysical": "Metaphysical (Donne, Herbert, Marvell)",
        "early_modern": "Early Modern (Wyatt, Spenser, Jonson)",
        "romantic":     "Romantic (Wordsworth, Keats, Byron, Shelley)",
        "modernist":    "Modernist (Eliot, Williams, Stevens, etc.)",
        "new_york_school": "New York School (O'Hara, etc.)",
        "beat":         "Beat (Ginsberg, etc.)",
        "victorian":    "Victorian (Tennyson, Browning, etc.)",
    }
    for era, description in ERA_GROUPS.items():
        era_poems = [p for p in corpus if p.get("metadata", p).get("era") == era]
        if not era_poems:
            continue
        analysis = analyze_poet(era_poems)
        if analysis is None:
            continue
        era_results[era] = {
            "description": description,
            "n_poems": len(era_poems),
            **analysis,
        }

    output = {
        "by_poet": results,
        "by_era": era_results,
        "metadata": {
            "s2_threshold": S2_THRESHOLD,
            "surp_median": SURP_MEDIAN,
            "ent_median": ENT_MEDIAN,
            "date": "2026-10-13",
            "note": "Pope paradox investigation: Q2/Q1 ratio + H_top10 at Q1 vs Q2 moments",
        }
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUTPUT_PATH}")
    return output


if __name__ == "__main__":
    main()
