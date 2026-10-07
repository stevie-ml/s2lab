"""
S2 Coordinate System: Mapping the Surprisal-Entropy Space

S2 = surprisal - entropy. Every token lives in 2D (surprisal, entropy) space.
The S2=0 line divides positive from negative. Within this space, four quadrants:

  Q1: High surp + High ent  = "Ambiguous surprise"   — model was uncertain, STILL wrong
  Q2: High surp + Low ent   = "Confident mismatch"   — model was confident, poet defied it
  Q3: Low surp  + Low ent   = "Confident match"      — model was confident, poet matched
  Q4: Low surp  + High ent  = "Lucky guess"          — model was uncertain, happened right

Q2 (confident mismatch) is the PUREST Straussian moment — the poet chose differently
when the model was most sure what should come next. These are the true anti-consensus moves.
"""

import json
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

RESULTS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json")

def classify_quadrant(surprisal, entropy):
    """Map a token to a quadrant label."""
    high_surp = surprisal > 5.0   # above median for poetry
    low_ent = entropy < 3.0       # below median entropy
    if high_surp and low_ent:
        return "Q2_confident_mismatch"
    elif high_surp and not low_ent:
        return "Q1_ambiguous_surprise"
    elif not high_surp and low_ent:
        return "Q3_confident_match"
    else:
        return "Q4_lucky_guess"

def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def is_artifact(tok):
    """Filter out stanza-break artifact positions."""
    return tok.get('p_newline', 0) >= 0.9

def run():
    data = load_data()

    # ── 1. Corpus-level quadrant distribution ────────────────────────────────
    print("=== S2 Coordinate System Analysis ===\n")

    quadrant_counts = {"Q1_ambiguous_surprise": 0, "Q2_confident_mismatch": 0,
                       "Q3_confident_match": 0, "Q4_lucky_guess": 0}
    quadrant_s2 = {k: [] for k in quadrant_counts}

    all_surp = []
    all_ent = []
    for poem in data:
        for tok in poem['tokens']:
            if is_artifact(tok):
                continue
            all_surp.append(tok['surprisal'])
            all_ent.append(tok['entropy'])

    # Use medians as thresholds
    all_surp.sort()
    all_ent.sort()
    surp_median = all_surp[len(all_surp)//2]
    ent_median = all_ent[len(all_ent)//2]
    print(f"Surprisal median: {surp_median:.2f} bits")
    print(f"Entropy median: {ent_median:.2f} bits")
    print()

    def classify(surprisal, entropy):
        high_surp = surprisal > surp_median
        low_ent = entropy < ent_median
        if high_surp and low_ent:
            return "Q2_confident_mismatch"
        elif high_surp and not low_ent:
            return "Q1_ambiguous_surprise"
        elif not high_surp and low_ent:
            return "Q3_confident_match"
        else:
            return "Q4_lucky_guess"

    # Collect per-poet Q2 ratios
    poet_stats = {}
    era_stats = {}

    q2_tokens = []  # (s2, token, context, poet, title)

    for poem in data:
        era = poem['metadata'].get('era', 'unknown')
        author = poem['metadata'].get('author', 'unknown')
        title = poem['metadata'].get('title', 'unknown')

        clean_toks = [t for t in poem['tokens'] if not is_artifact(t)]
        if not clean_toks:
            continue

        poem_quads = {"Q1_ambiguous_surprise": 0, "Q2_confident_mismatch": 0,
                      "Q3_confident_match": 0, "Q4_lucky_guess": 0}

        for tok in clean_toks:
            q = classify(tok['surprisal'], tok['entropy'])
            poem_quads[q] += 1
            quadrant_counts[q] += 1
            quadrant_s2[q].append(tok['s2'])

            if q == "Q2_confident_mismatch":
                q2_tokens.append({
                    's2': tok['s2'],
                    'surprisal': tok['surprisal'],
                    'entropy': tok['entropy'],
                    'token': tok['token'],
                    'context': tok.get('context_before', '')[-40:],
                    'alternatives': [a['token'] for a in tok.get('alternatives', [])[:3]],
                    'poet': author,
                    'title': title,
                })

        n = sum(poem_quads.values())
        if n == 0:
            continue
        q2_ratio = poem_quads["Q2_confident_mismatch"] / n
        q1_ratio = poem_quads["Q1_ambiguous_surprise"] / n

        if author not in poet_stats:
            poet_stats[author] = {"q2_count": 0, "q1_count": 0, "total": 0, "q2_ratios": []}
        poet_stats[author]["q2_count"] += poem_quads["Q2_confident_mismatch"]
        poet_stats[author]["q1_count"] += poem_quads["Q1_ambiguous_surprise"]
        poet_stats[author]["total"] += n
        poet_stats[author]["q2_ratios"].append(q2_ratio)

        if era not in era_stats:
            era_stats[era] = {"q2_count": 0, "q1_count": 0, "total": 0, "n_poems": 0}
        era_stats[era]["q2_count"] += poem_quads["Q2_confident_mismatch"]
        era_stats[era]["q1_count"] += poem_quads["Q1_ambiguous_surprise"]
        era_stats[era]["total"] += n
        era_stats[era]["n_poems"] += 1

    # ── 2. Corpus-level quadrant distribution ─────────────────────────────
    total = sum(quadrant_counts.values())
    print("=== Corpus-level Quadrant Distribution (artifact-free) ===")
    print(f"{'Quadrant':<35} {'Count':>8} {'%':>6} {'Avg S2':>9}")
    print("-" * 62)
    for q, label in [
        ("Q1_ambiguous_surprise",  "Q1: High surp + High ent (ambiguous surprise)"),
        ("Q2_confident_mismatch",  "Q2: High surp + Low ent  (confident mismatch)"),
        ("Q3_confident_match",     "Q3: Low surp  + Low ent  (confident match)"),
        ("Q4_lucky_guess",         "Q4: Low surp  + High ent (lucky guess)"),
    ]:
        cnt = quadrant_counts[q]
        pct = cnt / total * 100
        avg_s2 = sum(quadrant_s2[q]) / len(quadrant_s2[q]) if quadrant_s2[q] else 0
        print(f"  {label:<33} {cnt:>8,} {pct:>5.1f}% {avg_s2:>+9.3f}")
    print()

    # ── 3. Poets ranked by Q2 ratio (confident mismatch rate) ─────────────
    print("=== Poets Ranked by Confident-Mismatch Rate (Q2%) ===")
    print(f"{'Poet':<30} {'n':>5} {'Q2%':>6} {'Q1%':>6} {'Q2/Q1':>7}")
    print("-" * 54)
    poet_rows = []
    for poet, stats in poet_stats.items():
        if stats['total'] < 30:
            continue
        q2_pct = stats['q2_count'] / stats['total'] * 100
        q1_pct = stats['q1_count'] / stats['total'] * 100
        ratio = q2_pct / q1_pct if q1_pct > 0 else 0
        poet_rows.append((poet, stats['total'], q2_pct, q1_pct, ratio))
    poet_rows.sort(key=lambda x: -x[2])
    for poet, n, q2, q1, ratio in poet_rows[:20]:
        print(f"  {poet:<28} {n:>5} {q2:>5.1f}% {q1:>5.1f}% {ratio:>7.2f}")
    print()

    # ── 4. Eras ranked by Q2 ratio ─────────────────────────────────────────
    print("=== Eras Ranked by Confident-Mismatch Rate (Q2%) ===")
    print(f"{'Era':<25} {'poems':>6} {'n':>7} {'Q2%':>6} {'Q1%':>6}")
    print("-" * 54)
    era_rows = []
    for era, stats in era_stats.items():
        if stats['total'] < 20:
            continue
        q2_pct = stats['q2_count'] / stats['total'] * 100
        q1_pct = stats['q1_count'] / stats['total'] * 100
        era_rows.append((era, stats['n_poems'], stats['total'], q2_pct, q1_pct))
    era_rows.sort(key=lambda x: -x[3])
    for era, n_poems, n_tok, q2, q1 in era_rows:
        print(f"  {era:<23} {n_poems:>6} {n_tok:>7,} {q2:>5.1f}% {q1:>5.1f}%")
    print()

    # ── 5. Top Q2 tokens (purest Straussian moments) ──────────────────────
    print("=== Top 30 Confident-Mismatch Tokens (Purest Anti-Consensus Moves) ===")
    print(f"{'Token':<15} {'S2':>7} {'surp':>7} {'ent':>6} {'Expected':<20} {'Poet / Title'}")
    print("-" * 90)
    q2_tokens.sort(key=lambda x: -x['s2'])
    for t in q2_tokens[:30]:
        alts = ", ".join(t['alternatives'][:2])
        poet_title = f"{t['poet'][:15]} / {t['title'][:20]}"
        print(f"  {t['token'][:13]:<13} {t['s2']:>+7.2f} {t['surprisal']:>7.2f} {t['entropy']:>6.2f} {alts:<20} {poet_title}")
    print()

    # ── 6. Q2/Q1 ratio: does the poet "make precise bets"? ────────────────
    # Q2 = high-surprisal with LOW entropy → the model was locked in, poet defied
    # Q1 = high-surprisal with HIGH entropy → the model was already uncertain
    # Q2/Q1 > 1 means poet preferentially defies confident predictions
    print("=== Poets Who Preferentially Defy CONFIDENT Predictions (Q2/Q1 > 1.0) ===")
    precise_defiers = [(p, r, q2, q1, n) for p, n, q2, q1, r in poet_rows if r > 1.0 and n >= 50]
    precise_defiers.sort(key=lambda x: -x[1])
    for poet, ratio, q2, q1, n in precise_defiers:
        print(f"  {poet:<30} Q2/Q1={ratio:.2f}  Q2={q2:.1f}%  Q1={q1:.1f}%  (n={n})")

    print()
    print("=== Poets Who Mostly Defy UNCERTAIN Predictions (Q1/Q2 > 1.0) ===")
    uncertain_defiers = [(p, q1/q2 if q2>0 else 0, q2, q1, n) for p, n, q2, q1, r in poet_rows if q2>0 and q1/q2 > 1.0 and n >= 50]
    uncertain_defiers.sort(key=lambda x: -x[1])
    for poet, ratio, q2, q1, n in uncertain_defiers[:10]:
        print(f"  {poet:<30} Q1/Q2={ratio:.2f}  Q1={q1:.1f}%  Q2={q2:.1f}%  (n={n})")

    return {
        "surp_median": surp_median,
        "ent_median": ent_median,
        "quadrant_counts": quadrant_counts,
        "poet_rows": poet_rows,
        "era_rows": era_rows,
        "top_q2_tokens": q2_tokens[:30],
    }

if __name__ == "__main__":
    results = run()
    print("\nDone.")
