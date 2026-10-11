"""
Q2 vs Q1 Strategy Taxonomy: Two Paths to Poetic Surprise

Research question: The S2 coordinate system (s2_coordinate_system.md) identified two
modes of surprise:
  - Q2 (High surprisal + Low entropy): "Confident mismatch" — model was sure; poet defied it.
  - Q1 (High surprisal + High entropy): "Ambiguous surprise" — model was uncertain; poet chose one
    of many possible paths, but still unusually.

The coordinate system noted W.S. Merwin (highest Q2/Q1 ratio) exploits moments when the model
is most confident. This experiment formally tests the hypothesis:

  Q2 strategy = colloquial syntax with surprising CONTENT words
                (model expects punctuation/common continuations; poet chooses unexpected noun/verb)
  Q1 strategy = archaic/complex syntax where even FUNCTION WORDS become uncertain
                (model sees many equally plausible directions; poet navigates ambiguity)

Method:
1. For each token above the S2 threshold, classify as Q1 or Q2 using corpus median thresholds
2. Characterize the TOKEN itself:
   - Is it short (≤3 chars, likely function word) or long (content word)?
   - What was the TOP-1 model prediction? (punctuation vs word vs newline)
   - What is the token's "surface rank" — how common a word is it?
3. Classify the MODEL'S PREDICTION at Q2 vs Q1 positions:
   - At Q2 (low entropy): what narrow set did the model expect?
   - At Q1 (high entropy): what diverse set was available?
4. Compare poet-level Q2/Q1 ratios to test the two-strategy hypothesis
5. Test whether Q2 vs Q1 dominance correlates with other known properties

Thresholds: corpus medians (surprisal > 4.77, entropy > 6.34), same as coordinate system.
S2 threshold for "high surprise": S2 > 2.0 (meaningful deviation)
"""

import json
import re
from collections import defaultdict, Counter
from statistics import mean, stdev, median

RESULTS_PATH = "results/corpus_results.json"
SURP_MEDIAN = 4.77  # corpus median surprisal (artifact-free)
ENT_MEDIAN = 6.34   # corpus median entropy (artifact-free)
S2_THRESHOLD = 2.0  # minimum S2 to count as "interesting surprise"

PUNCTUATION_TOKENS = {",", ".", "!", "?", ";", ":", "'", '"', "-", "—", "(", ")", "/", "\\"}
NEWLINE_OR_SPACE = re.compile(r"^[\n\r\s]+$")

# Common English function words (proxy for syntactic/grammatical words)
FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "nor", "for", "yet", "so",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "up",
    "about", "into", "through", "during", "before", "after", "above",
    "below", "between", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "that", "which",
    "who", "whom", "whose", "what", "this", "these", "those", "it", "its",
    "he", "she", "they", "we", "you", "i", "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their", "not", "no", "nor", "if", "as",
    "when", "where", "how", "than", "then", "there", "here", "all", "each",
    "both", "either", "neither", "such", "same", "own", "other",
}


def newline_prob(tok):
    return sum(a["prob"] for a in tok.get("alternatives", []) if NEWLINE_OR_SPACE.match(a["token"]))


def is_artifact(tok):
    return newline_prob(tok) >= 0.90


def classify_quadrant(tok):
    """Q1/Q2/Q3/Q4 based on surprisal and entropy relative to medians."""
    s = tok["surprisal"]
    e = tok["entropy"]
    high_s = s > SURP_MEDIAN
    high_e = e > ENT_MEDIAN
    if high_s and high_e:
        return "Q1"  # ambiguous surprise
    elif high_s and not high_e:
        return "Q2"  # confident mismatch
    elif not high_s and not high_e:
        return "Q3"  # confident match
    else:
        return "Q4"  # lucky guess


def token_type(text):
    """Classify token text as function_word, content_word, punctuation, or other."""
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
    """Classify the top-1 model prediction."""
    if not alternatives:
        return "unknown"
    top = alternatives[0]["token"]
    stripped = top.strip()
    if not stripped or NEWLINE_OR_SPACE.match(top):
        return "whitespace/newline"
    if stripped in PUNCTUATION_TOKENS or (len(stripped) == 1 and not stripped.isalpha()):
        return "punctuation"
    lower = stripped.lower().lstrip("'\"")
    if lower in FUNCTION_WORDS:
        return "function_word"
    return "content_word"


def entropy_of_alts(alternatives):
    """Compute entropy of the distribution over listed alternatives."""
    total = sum(a["prob"] for a in alternatives)
    if total == 0:
        return 0
    ent = 0.0
    for a in alternatives:
        p = a["prob"] / total
        if p > 0:
            import math
            ent -= p * math.log2(p)
    return ent


def run():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Filter to English poetry (no controls)
    poems = [p for p in corpus
             if p["metadata"].get("language", "en") == "en"
             and p["metadata"].get("era") != "control"]
    print(f"Analyzing {len(poems)} English poetry texts...")

    # ── Global quadrant token analysis ────────────────────────────────────
    q_token_types = defaultdict(Counter)   # quadrant -> token_type -> count
    q_alt_types = defaultdict(Counter)     # quadrant -> top-alt-type -> count
    q_s2 = defaultdict(list)               # quadrant -> s2 values
    q_token_len = defaultdict(list)        # quadrant -> token length (stripped)
    q_entropy_alts = defaultdict(list)     # quadrant -> entropy of alternatives

    high_q2 = []  # top Q2 surprises
    high_q1 = []  # top Q1 surprises

    for poem in poems:
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            if tok["s2"] < S2_THRESHOLD:
                continue
            q = classify_quadrant(tok)
            tt = token_type(tok["token"])
            at = top_alt_type(tok.get("alternatives", []))
            s2 = tok["s2"]
            length = len(tok["token"].strip())
            ent_alts = entropy_of_alts(tok.get("alternatives", []))

            q_token_types[q][tt] += 1
            q_alt_types[q][at] += 1
            q_s2[q].append(s2)
            q_token_len[q].append(length)
            q_entropy_alts[q].append(ent_alts)

            if q == "Q2" and s2 > 10:
                high_q2.append({
                    "token": tok["token"].strip(),
                    "s2": s2,
                    "surprisal": tok["surprisal"],
                    "entropy": tok["entropy"],
                    "top_alt": tok["alternatives"][0]["token"].strip() if tok.get("alternatives") else "?",
                    "top_alt_prob": tok["alternatives"][0]["prob"] if tok.get("alternatives") else 0,
                    "poem": poem["metadata"]["title"],
                    "author": poem["metadata"]["author"],
                })
            if q == "Q1" and s2 > 10:
                high_q1.append({
                    "token": tok["token"].strip(),
                    "s2": s2,
                    "surprisal": tok["surprisal"],
                    "entropy": tok["entropy"],
                    "top_alt": tok["alternatives"][0]["token"].strip() if tok.get("alternatives") else "?",
                    "top_alt_prob": tok["alternatives"][0]["prob"] if tok.get("alternatives") else 0,
                    "poem": poem["metadata"]["title"],
                    "author": poem["metadata"]["author"],
                })

    # Sort high examples
    high_q2.sort(key=lambda x: -x["s2"])
    high_q1.sort(key=lambda x: -x["s2"])

    print("\n=== Global: Token Type Distribution by Quadrant (high-S2 tokens only) ===\n")
    all_q = ["Q1", "Q2"]
    for q in all_q:
        n_total = sum(q_token_types[q].values())
        if not n_total:
            continue
        print(f"  {q} (n={n_total}, mean S2={mean(q_s2[q]):+.2f}, mean token_len={mean(q_token_len[q]):.1f}):")
        for tt, cnt in sorted(q_token_types[q].items(), key=lambda x: -x[1]):
            pct = cnt / n_total * 100
            print(f"    {tt:20s} {cnt:5d} ({pct:.1f}%)")
        print()

    print("=== Global: Top-1 Alternative Type by Quadrant ===\n")
    for q in all_q:
        n_total = sum(q_alt_types[q].values())
        if not n_total:
            continue
        print(f"  {q} (n={n_total}):")
        for at, cnt in sorted(q_alt_types[q].items(), key=lambda x: -x[1]):
            pct = cnt / n_total * 100
            print(f"    {at:25s} {cnt:5d} ({pct:.1f}%)")
        print()

    print("=== Q2 vs Q1: Key Metrics Comparison ===\n")
    for q in all_q:
        if not q_s2[q]:
            continue
        print(f"  {q}:")
        print(f"    Count (S2 > {S2_THRESHOLD}):     {len(q_s2[q])}")
        print(f"    Mean S2:               {mean(q_s2[q]):+.2f}")
        print(f"    Mean token length:     {mean(q_token_len[q]):.1f} chars")
        print(f"    Mean alt entropy:      {mean(q_entropy_alts[q]):.2f} bits")
        content_n = q_token_types[q].get("content", 0)
        func_n = q_token_types[q].get("function", 0)
        total = sum(q_token_types[q].values())
        print(f"    Content word rate:     {content_n/total*100:.1f}%")
        print(f"    Function word rate:    {func_n/total*100:.1f}%")
        top_alt_punc = q_alt_types[q].get("punctuation", 0) + q_alt_types[q].get("whitespace/newline", 0)
        print(f"    Top-alt was punc/ws:   {top_alt_punc/sum(q_alt_types[q].values())*100:.1f}%")
        print()

    print("=== Top Q2 Confident-Mismatch Examples ===\n")
    for ex in high_q2[:12]:
        print(f"  '{ex['token']}' (S2={ex['s2']:.1f}, surp={ex['surprisal']:.1f}, ent={ex['entropy']:.1f})")
        print(f"    Model expected: '{ex['top_alt']}' (p={ex['top_alt_prob']:.3f})")
        print(f"    Poem: {ex['author']} — {ex['poem'][:50]}")

    print("\n=== Top Q1 Ambiguous-Surprise Examples ===\n")
    for ex in high_q1[:12]:
        print(f"  '{ex['token']}' (S2={ex['s2']:.1f}, surp={ex['surprisal']:.1f}, ent={ex['entropy']:.1f})")
        print(f"    Model expected: '{ex['top_alt']}' (p={ex['top_alt_prob']:.3f})")
        print(f"    Poem: {ex['author']} — {ex['poem'][:50]}")

    # ── Poet-level Q2/Q1 ratios ────────────────────────────────────────────
    print("\n\n=== Poet-Level Q2/Q1 Ratios (min 5 surprise tokens each) ===\n")
    poet_q = defaultdict(lambda: {"Q1": 0, "Q2": 0, "tokens": 0, "content_q2": 0,
                                   "func_q2": 0, "content_q1": 0, "func_q1": 0})

    for poem in poems:
        author = poem["metadata"]["author"]
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            if tok["s2"] < S2_THRESHOLD:
                continue
            q = classify_quadrant(tok)
            tt = token_type(tok["token"])
            poet_q[author]["tokens"] += 1
            if q in ("Q1", "Q2"):
                poet_q[author][q] += 1
                if tt == "content":
                    poet_q[author][f"content_{q.lower()}"] += 1
                elif tt == "function":
                    poet_q[author][f"func_{q.lower()}"] += 1

    # Filter to poets with enough data
    qualified = {a: d for a, d in poet_q.items()
                 if d["Q1"] >= 5 and d["Q2"] >= 5}

    rows = []
    for author, d in qualified.items():
        ratio = d["Q2"] / d["Q1"]
        content_q2_rate = d["content_q2"] / d["Q2"] if d["Q2"] else 0
        content_q1_rate = d["content_q1"] / d["Q1"] if d["Q1"] else 0
        func_q1_rate = d["func_q1"] / d["Q1"] if d["Q1"] else 0
        rows.append({
            "author": author, "q2": d["Q2"], "q1": d["Q1"],
            "ratio": ratio,
            "content_q2_rate": content_q2_rate,
            "content_q1_rate": content_q1_rate,
            "func_q1_rate": func_q1_rate,
        })

    rows.sort(key=lambda x: -x["ratio"])

    print(f"{'Author':<40} {'Q2':>5} {'Q1':>5} {'Q2/Q1':>6} {'Cntnt-Q2':>9} {'Cntnt-Q1':>9} {'Func-Q1':>8}")
    print("-" * 90)
    for r in rows:
        print(f"  {r['author']:<38} {r['q2']:>5} {r['q1']:>5} {r['ratio']:>6.2f} "
              f"{r['content_q2_rate']:>8.0%} {r['content_q1_rate']:>8.0%} {r['func_q1_rate']:>7.0%}")

    # Strategy classification
    median_ratio = median([r["ratio"] for r in rows])
    q2_strategists = [r for r in rows if r["ratio"] > median_ratio * 1.5]
    q1_strategists = [r for r in rows if r["ratio"] < median_ratio * 0.67]

    print(f"\nMedian Q2/Q1 ratio: {median_ratio:.2f}")
    print(f"\nStrong Q2 strategists (ratio > {median_ratio*1.5:.2f}):")
    for r in sorted(q2_strategists, key=lambda x: -x["ratio"]):
        print(f"  {r['author']}: Q2/Q1={r['ratio']:.2f}, content-Q2={r['content_q2_rate']:.0%}, func-Q1={r['func_q1_rate']:.0%}")
    print(f"\nStrong Q1 strategists (ratio < {median_ratio*0.67:.2f}):")
    for r in sorted(q1_strategists, key=lambda x: x["ratio"]):
        print(f"  {r['author']}: Q2/Q1={r['ratio']:.2f}, content-Q2={r['content_q2_rate']:.0%}, func-Q1={r['func_q1_rate']:.0%}")

    # Test the hypothesis: Q2 strategists have higher content-word rate in Q2 moments
    q2_strat_content = [r["content_q2_rate"] for r in q2_strategists]
    q1_strat_content = [r["content_q1_rate"] for r in q1_strategists]
    print(f"\nHypothesis test:")
    if q2_strat_content:
        print(f"  Q2 strategists mean content-word rate at Q2 moments: {mean(q2_strat_content):.0%}")
    if q1_strat_content:
        print(f"  Q1 strategists mean content-word rate at Q1 moments: {mean(q1_strat_content):.0%}")

    # ── Era-level analysis ─────────────────────────────────────────────────
    print("\n\n=== Era-Level Q2/Q1 Ratios ===\n")
    era_q = defaultdict(lambda: {"Q1": 0, "Q2": 0})
    for poem in poems:
        era = poem["metadata"]["era"]
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            if tok["s2"] < S2_THRESHOLD:
                continue
            q = classify_quadrant(tok)
            if q in ("Q1", "Q2"):
                era_q[era][q] += 1

    era_rows = []
    for era, d in era_q.items():
        if d["Q1"] >= 10 and d["Q2"] >= 5:
            era_rows.append({
                "era": era,
                "q2": d["Q2"],
                "q1": d["Q1"],
                "ratio": d["Q2"] / d["Q1"],
                "total": d["Q1"] + d["Q2"],
            })
    era_rows.sort(key=lambda x: -x["ratio"])
    print(f"{'Era':<30} {'Q2':>5} {'Q1':>5} {'Q2/Q1':>7} {'total':>7}")
    print("-" * 60)
    for r in era_rows:
        print(f"  {r['era']:<28} {r['q2']:>5} {r['q1']:>5} {r['ratio']:>7.2f} {r['total']:>7}")

    print("\nDone.")
    return {
        "q_token_types": {k: dict(v) for k, v in q_token_types.items()},
        "q_alt_types": {k: dict(v) for k, v in q_alt_types.items()},
        "poet_rows": rows,
        "era_rows": era_rows,
        "high_q2": high_q2[:20],
        "high_q1": high_q1[:20],
    }


if __name__ == "__main__":
    results = run()
