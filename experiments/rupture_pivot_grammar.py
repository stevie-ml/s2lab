"""
Rupture vs. Pivot: Grammar of the Suppressed and the Chosen

Building on entropy_cascade_context.md and rupture_pivot_poet_profiles.md:
  - Rupture event: s2 > S2_THRESH AND entropy_t < CONFIDENT_THRESH
    (poet surprises when model is confident → liberation of subsequent context)
  - Pivot event: s2 > S2_THRESH AND entropy_t >= UNCERTAIN_THRESH
    (poet surprises when model is uncertain → anchoring of subsequent context)

Research question:
  When a rupture happens, what grammatical class does the poet CHOOSE and SUPPRESS?
  When a pivot happens, what grammatical class does the poet CHOOSE and SUPPRESS?

Key hypotheses:
  H1 (Rupture suppresses content words): In confident contexts, GPT-2 expects
      specific content words (NOUN, VERB). The poet subverts with a different class.
  H2 (Pivot suppresses structure words): In uncertain contexts, GPT-2 hedges with
      function words (PREP, CONJ, DET). The poet resolves ambiguity with content.
  H3 (Rupture chooses broader grammar): The rupture poet's actual token is more
      likely to be a content word (ADJ, NOUN) than a function word.
  H4 (Pivot chooses specific content): The pivot poet may actually choose a more
      specific/concrete word (NOUN, VERB) than what was suppressed.
"""

import json
import re
from collections import defaultdict

import nltk.pathsec
nltk.pathsec.ALLOW_PROXIED_FETCH = True
import nltk

# Ensure required NLTK data is available
for pkg in ("punkt", "averaged_perceptron_tagger", "averaged_perceptron_tagger_eng"):
    nltk.download(pkg, quiet=True)

# ── Constants ────────────────────────────────────────────────────────────────
S2_THRESH = 1.5        # minimum S2 to count as a surprise event
CONFIDENT_THRESH = 4.0 # entropy < this → confident context → rupture
UNCERTAIN_THRESH = 7.0 # entropy ≥ this → uncertain context → pivot
NEWLINE_PROB_THRESH = 0.9  # artifact filter: skip tokens where stanza-break dominates

# Penn Treebank → broad category
_PENN = {
    "NN": "NOUN", "NNS": "NOUN", "NNP": "NOUN", "NNPS": "NOUN",
    "VB": "VERB", "VBD": "VERB", "VBG": "VERB", "VBN": "VERB",
    "VBP": "VERB", "VBZ": "VERB",
    "MD": "AUX",
    "JJ": "ADJ", "JJR": "ADJ", "JJS": "ADJ",
    "RB": "ADV", "RBR": "ADV", "RBS": "ADV",
    "DT": "DET",
    "IN": "PREP",
    "CC": "CONJ",
    "PRP": "PRON", "PRP$": "PRON", "WP": "PRON", "WP$": "PRON",
    ".": "PUNCT", ",": "PUNCT", ":": "PUNCT", "``": "PUNCT", "''": "PUNCT",
    "-LRB-": "PUNCT", "-RRB-": "PUNCT",
}

CONTENT = {"NOUN", "VERB", "ADJ", "ADV"}
FUNCTION = {"DET", "PREP", "CONJ", "PRON", "AUX"}


def broad_cat(penn: str) -> str:
    return _PENN.get(penn, "OTHER")


def pos_tag_token(text: str) -> str:
    """Quick POS tag for a single (sub)word token string."""
    text = text.strip()
    if not text or text == "\n":
        return "NEWLINE"
    # Punctuation-only
    if re.fullmatch(r"[^\w\s]+", text):
        return "PUNCT"
    try:
        tokens = nltk.word_tokenize(text)
        if not tokens:
            return "OTHER"
        tags = nltk.pos_tag(tokens)
        return broad_cat(tags[0][1])
    except Exception:
        return "OTHER"


def analyze_corpus(data: list[dict]) -> dict:
    """
    For each poem (English, non-control), pair consecutive tokens.
    For each pair (t, t+1) with no artifact:
      - classify as rupture, pivot, or neither
      - record POS of actual token t AND top-1 suppressed token
    """
    rupture_chosen = defaultdict(int)   # what poet wrote in rupture events
    rupture_suppressed = defaultdict(int)  # what GPT-2 predicted (suppressed)
    pivot_chosen = defaultdict(int)
    pivot_suppressed = defaultdict(int)
    baseline_chosen = defaultdict(int)  # middle zone (4 <= entropy < 7)
    baseline_suppressed = defaultdict(int)

    # Substitution matrices: [event_type][chosen_pos][suppressed_pos]
    rupture_matrix = defaultdict(lambda: defaultdict(int))
    pivot_matrix = defaultdict(lambda: defaultdict(int))
    baseline_matrix = defaultdict(lambda: defaultdict(int))

    rupture_n = 0
    pivot_n = 0
    baseline_n = 0
    total_texts = 0

    for entry in data:
        meta = entry.get("metadata", {})
        if meta.get("era") == "control":
            continue
        if meta.get("language", "en") != "en":
            continue

        tokens = entry.get("tokens", [])
        total_texts += 1

        for i in range(len(tokens) - 1):
            t = tokens[i]
            t_next = tokens[i + 1]

            # Skip artifact positions
            if t.get("p_newline", 0) >= NEWLINE_PROB_THRESH:
                continue
            if t_next.get("p_newline", 0) >= NEWLINE_PROB_THRESH:
                continue

            s2_t = t.get("s2", 0)
            ent_t = t.get("entropy", 0)

            if s2_t <= S2_THRESH:
                continue  # not a surprise event

            # Get top-1 suppressed token
            alts = t.get("alternatives", [])
            if not alts:
                continue
            top1_token = alts[0].get("token", "")

            # POS tag actual and suppressed
            chosen_pos = pos_tag_token(t["token"])
            suppressed_pos = pos_tag_token(top1_token)

            # Skip NEWLINE/OTHER to reduce noise
            if chosen_pos in ("NEWLINE", "OTHER", "SPACE"):
                continue

            if ent_t < CONFIDENT_THRESH:
                rupture_chosen[chosen_pos] += 1
                rupture_suppressed[suppressed_pos] += 1
                rupture_matrix[chosen_pos][suppressed_pos] += 1
                rupture_n += 1
            elif ent_t >= UNCERTAIN_THRESH:
                pivot_chosen[chosen_pos] += 1
                pivot_suppressed[suppressed_pos] += 1
                pivot_matrix[chosen_pos][suppressed_pos] += 1
                pivot_n += 1
            else:
                baseline_chosen[chosen_pos] += 1
                baseline_suppressed[suppressed_pos] += 1
                baseline_matrix[chosen_pos][suppressed_pos] += 1
                baseline_n += 1

    return {
        "rupture": {
            "n": rupture_n,
            "chosen": dict(rupture_chosen),
            "suppressed": dict(rupture_suppressed),
            "matrix": {k: dict(v) for k, v in rupture_matrix.items()},
        },
        "pivot": {
            "n": pivot_n,
            "chosen": dict(pivot_chosen),
            "suppressed": dict(pivot_suppressed),
            "matrix": {k: dict(v) for k, v in pivot_matrix.items()},
        },
        "baseline": {
            "n": baseline_n,
            "chosen": dict(baseline_chosen),
            "suppressed": dict(baseline_suppressed),
            "matrix": {k: dict(v) for k, v in baseline_matrix.items()},
        },
        "total_texts": total_texts,
        "thresholds": {
            "s2": S2_THRESH,
            "confident": CONFIDENT_THRESH,
            "uncertain": UNCERTAIN_THRESH,
        },
    }


def pct(d: dict, key: str) -> float:
    total = sum(d.values())
    if total == 0:
        return 0.0
    return 100.0 * d.get(key, 0) / total


def content_pct(d: dict) -> float:
    total = sum(d.values())
    if total == 0:
        return 0.0
    return 100.0 * sum(d.get(k, 0) for k in CONTENT) / total


def print_report(results: dict) -> None:
    CATS = ["NOUN", "VERB", "ADJ", "ADV", "AUX", "DET", "PREP", "CONJ", "PRON", "PUNCT"]

    for event_type in ("rupture", "pivot", "baseline"):
        r = results[event_type]
        print(f"\n{'='*60}")
        print(f"  {event_type.upper()} events  (n={r['n']:,})")
        print(f"{'='*60}")

        chosen = r["chosen"]
        suppressed = r["suppressed"]

        print(f"\n  {'POS':<8} {'%Chosen':>8} {'%Suppressed':>12}  {'Δ (Chosen-Suppressed)':>22}")
        print(f"  {'-'*56}")
        for cat in CATS:
            ch = pct(chosen, cat)
            su = pct(suppressed, cat)
            delta = ch - su
            bar = ("+" if delta > 0 else "") + f"{delta:+.1f}"
            print(f"  {cat:<8} {ch:>7.1f}% {su:>11.1f}%  {bar:>22}")

        ch_c = content_pct(chosen)
        su_c = content_pct(suppressed)
        print(f"\n  Content-word %: chosen={ch_c:.1f}%  suppressed={su_c:.1f}%  Δ={ch_c - su_c:+.1f}pp")

    # Cross-event comparison
    print("\n\n" + "="*60)
    print("  CROSS-EVENT: % Content-word in CHOSEN vs SUPPRESSED")
    print("="*60)
    print(f"  {'Event':<12} {'Chosen %Content':>16} {'Suppressed %Content':>20} {'Δ':>8}")
    print(f"  {'-'*58}")
    for ev in ("rupture", "pivot", "baseline"):
        r = results[ev]
        ch_c = content_pct(r["chosen"])
        su_c = content_pct(r["suppressed"])
        print(f"  {ev:<12} {ch_c:>15.1f}% {su_c:>19.1f}% {ch_c - su_c:>+8.1f}pp")

    # Most contrasting POS pairs between rupture and pivot (suppressed)
    print("\n\n" + "="*60)
    print("  RUPTURE vs PIVOT: Which POS gets SUPPRESSED differently?")
    print("  (Δ = rupture suppressed% − pivot suppressed%)")
    print("="*60)
    print(f"  {'POS':<8} {'Rupt Supp%':>11} {'Pivot Supp%':>12} {'Δ':>8}")
    print(f"  {'-'*44}")
    diffs = []
    rsupp = results["rupture"]["suppressed"]
    psupp = results["pivot"]["suppressed"]
    for cat in CATS:
        r_pct = pct(rsupp, cat)
        p_pct = pct(psupp, cat)
        diffs.append((cat, r_pct, p_pct, r_pct - p_pct))
    diffs.sort(key=lambda x: -abs(x[3]))
    for cat, rp, pp, d in diffs:
        print(f"  {cat:<8} {rp:>10.1f}% {pp:>11.1f}% {d:>+8.1f}pp")


def main():
    with open("results/corpus_results.json") as f:
        data = json.load(f)

    print(f"Loaded {len(data)} corpus entries")
    print("Running rupture/pivot grammar analysis...")

    results = analyze_corpus(data)

    print(f"\nTexts analyzed: {results['total_texts']}")
    print(f"Rupture events: {results['rupture']['n']:,}")
    print(f"Pivot events:   {results['pivot']['n']:,}")
    print(f"Baseline events:{results['baseline']['n']:,}")

    print_report(results)

    # Save JSON
    out_path = "results/rupture_pivot_grammar.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == "__main__":
    main()
