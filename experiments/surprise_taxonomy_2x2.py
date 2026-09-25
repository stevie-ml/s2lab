"""
The 2×2 Surprise Taxonomy: Classifying Poetic Deviation by Context and Choice

Two independent axes create four types of S2 token:
  Axis 1: Context Entropy  — low (model confident) vs. high (model uncertain)
  Axis 2: Token Rank       — low (expected choice) vs. high (unexpected choice)

Resulting quadrant names:
  I   Low H, High Rank  → "Definite Straussian Gap"  — real poetic surprise
  II  High H, High Rank → "Uncertain Leap"            — surprise amid confusion
  III Low H, Low Rank   → "Confirmed Prediction"      — conventional / cliché
  IV  High H, Low Rank  → "Lucky Hit"                 — expected amid uncertainty

Hypothesis: poetry shows more Type I tokens than prose and cliché control.
Sub-hypothesis: individual poets have distinct Type I / Type III ratios (poetic fingerprint).
"""

import json
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

# Thresholds — split at corpus median for entropy, and use rank ≤ 10 as "expected"
RANK_THRESHOLD = 10   # top-10 = "expected"; rank > 10 = "unexpected"
# Entropy threshold determined dynamically (corpus median)


def load_tokens(results_path):
    """Return flat list of (poem_meta, token_dict) pairs."""
    with open(results_path) as f:
        data = json.load(f)
    records = []
    for poem in data:
        meta = poem["metadata"]
        for tok in poem["tokens"]:
            records.append((meta, tok))
    return records


def is_artifact(tok):
    """Return True if this token is at a stanza-break artifact position.

    Criterion: the model's top-ranked alternative is a newline token with
    probability ≥ 0.9.  At these positions, entropy collapses to ~0 bits
    because GPT-2 is nearly certain a newline follows, so any non-newline
    token trivially achieves huge S₂.  These tokens are not measuring poetic
    choice.  See findings/stanza_break_artifact.md.
    """
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    top = alts[0]
    return top["token"] in ("\n", "\r\n", "\r") and top["prob"] >= 0.9


def classify_token(tok, entropy_median):
    """Return quadrant I / II / III / IV (or None for artifact tokens)."""
    if is_artifact(tok):
        return None
    h = tok["entropy"]
    rank = tok.get("rank", 9999)
    low_entropy = h < entropy_median
    expected = rank <= RANK_THRESHOLD
    if low_entropy and not expected:
        return "I"    # Definite Straussian Gap
    elif not low_entropy and not expected:
        return "II"   # Uncertain Leap
    elif low_entropy and expected:
        return "III"  # Confirmed Prediction
    else:
        return "IV"   # Lucky Hit


def run():
    records = load_tokens(RESULTS_PATH)

    # Compute entropy median across all tokens (excluding newline-dominant tokens)
    entropies = [t["entropy"] for _, t in records if t["entropy"] > 0]
    entropy_median = statistics.median(entropies)
    print(f"Entropy median (corpus): {entropy_median:.3f}")

    # Classify all tokens (skip artifact positions)
    artifact_count = sum(1 for _, t in records if is_artifact(t))
    print(f"Artifact tokens filtered: {artifact_count} ({100*artifact_count/len(records):.1f}%)")

    corpus_counts = defaultdict(int)
    type_s2 = defaultdict(list)
    type_examples = defaultdict(list)   # (s2, token, context, author, title)

    for meta, tok in records:
        qtype = classify_token(tok, entropy_median)
        if qtype is None:
            continue
        corpus_counts[qtype] += 1
        type_s2[qtype].append(tok["s2"])
        if len(type_examples[qtype]) < 30:
            type_examples[qtype].append({
                "s2": tok["s2"],
                "token": tok["token"],
                "context": tok.get("context_before", ""),
                "author": meta["author"],
                "title": meta["title"],
                "rank": tok.get("rank"),
                "entropy": tok["entropy"],
                "surprisal": tok["surprisal"],
            })

    total = sum(corpus_counts.values())
    print(f"\nTotal tokens classified: {total}")
    print(f"\n{'Type':<8} {'Count':>7} {'%':>6} {'Avg S2':>8} {'Median S2':>10}")
    print("-" * 44)
    for qt in ["I", "II", "III", "IV"]:
        n = corpus_counts[qt]
        pct = 100 * n / total
        avg = statistics.mean(type_s2[qt])
        med = statistics.median(type_s2[qt])
        print(f"  {qt:<6} {n:>7} {pct:>5.1f}% {avg:>8.3f} {med:>10.3f}")

    # Per-era analysis
    print("\n--- Per-era Type I ratio (artifact-free) ---")
    era_types = defaultdict(lambda: defaultdict(int))
    for meta, tok in records:
        era = meta.get("era", "unknown")
        qtype = classify_token(tok, entropy_median)
        if qtype is None:
            continue
        era_types[era][qtype] += 1

    era_rows = []
    for era, counts in era_types.items():
        total_era = sum(counts.values())
        ratio_I = counts["I"] / total_era if total_era else 0
        ratio_III = counts["III"] / total_era if total_era else 0
        contrast = ratio_I - ratio_III
        era_rows.append((era, total_era, ratio_I, ratio_III, contrast))
    era_rows.sort(key=lambda x: -x[2])  # sort by Type I ratio

    print(f"\n{'Era':<22} {'N':>5} {'Type I%':>8} {'TypeIII%':>9} {'I-III':>7}")
    print("-" * 55)
    for era, n, ri, riii, diff in era_rows:
        print(f"  {era:<20} {n:>5} {100*ri:>7.1f}% {100*riii:>8.1f}% {diff:>+7.3f}")

    # Per-author analysis (authors with ≥ 50 tokens)
    print("\n--- Per-author Type I ratio (min 50 tokens, artifact-free) ---")
    author_types = defaultdict(lambda: defaultdict(int))
    for meta, tok in records:
        author = meta["author"]
        qtype = classify_token(tok, entropy_median)
        if qtype is None:
            continue
        author_types[author][qtype] += 1

    author_rows = []
    for author, counts in author_types.items():
        total_auth = sum(counts.values())
        if total_auth < 50:
            continue
        ratio_I = counts["I"] / total_auth
        ratio_III = counts["III"] / total_auth
        contrast = ratio_I - ratio_III
        author_rows.append((author, total_auth, ratio_I, ratio_III, contrast))
    author_rows.sort(key=lambda x: -x[2])

    print(f"\n{'Author':<30} {'N':>5} {'TypeI%':>7} {'TypeIII%':>9} {'I-III':>7}")
    print("-" * 58)
    for author, n, ri, riii, diff in author_rows:
        print(f"  {author:<28} {n:>5} {100*ri:>6.1f}% {100*riii:>8.1f}% {diff:>+7.3f}")

    # Top Type-I examples (Definite Straussian Gaps)
    print("\n--- Top 15 Type I (Definite Straussian Gap) tokens, artifact-free ---")
    type_I_all = [
        (meta, tok) for meta, tok in records
        if classify_token(tok, entropy_median) == "I"
    ]
    type_I_all.sort(key=lambda x: -x[1]["s2"])
    for meta, tok in type_I_all[:15]:
        ctx = tok.get("context_before", "")[-25:].replace("\n", "↵")
        alt1 = tok["alternatives"][0]["token"] if tok["alternatives"] else "?"
        print(f"  S2={tok['s2']:6.2f} H={tok['entropy']:.2f} rank={tok.get('rank','?'):>5}"
              f"  [{ctx}] → '{tok['token']}' (expected: '{alt1}')"
              f"  — {meta['author']}")

    # Prose vs. poetry comparison
    print("\n--- Prose vs. Poetry Type I comparison (artifact-free) ---")
    prose_types = defaultdict(int)
    poetry_types = defaultdict(int)
    for meta, tok in records:
        era = meta.get("era", "unknown")
        qtype = classify_token(tok, entropy_median)
        if qtype is None:
            continue
        if era == "control":
            prose_types[qtype] += 1
        else:
            poetry_types[qtype] += 1

    for label, counts in [("Prose (control)", prose_types), ("Poetry", poetry_types)]:
        total_l = sum(counts.values())
        ri = counts["I"] / total_l if total_l else 0
        riii = counts["III"] / total_l if total_l else 0
        print(f"  {label:<22}  Type I: {100*ri:.1f}%   Type III: {100*riii:.1f}%   I−III: {ri-riii:+.3f}")

    return {
        "entropy_median": entropy_median,
        "corpus_counts": dict(corpus_counts),
        "era_rows": era_rows,
    }


if __name__ == "__main__":
    run()
