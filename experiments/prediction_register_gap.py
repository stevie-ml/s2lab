"""
Prediction Register Gap: Function vs. Content Word Expectations

When GPT-2 predicts a function word but the poet writes a content word
(or vice versa), what are the information-theoretic signatures?

This experiment builds a 3x3 matrix of:
  rows: register of GPT-2's TOP prediction (punct, function, content)
  cols: register of the poet's ACTUAL token (punct, function, content)
  cells: mean S2 for each combination

This reveals the 'grammar of poetic surprise' — how poets intervene
in grammatical slots vs. semantic slots vs. punctuation slots.

The hypothesis is that the LARGEST S2 values come from cross-register
violations: choosing a content word when a function word was expected
('semantic invasion of grammatical slot').
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
P_NEWLINE_MAX = 0.9
S2_THRESHOLD = 2.0   # only analyze tokens with |S2| > this

# ------------------------------------------------------------------
# Function word lexicon: common English function words.
# Stripped of leading space (GPT-2 tokenizer adds spaces).
# ------------------------------------------------------------------
FUNCTION_WORDS = {
    # articles
    "a", "an", "the",
    # prepositions
    "of", "in", "to", "for", "with", "on", "at", "from", "by", "about",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "out", "off", "over", "under", "again", "further", "then",
    "once", "against", "along", "among", "around", "but", "per", "via",
    "upon", "within", "without", "behind", "beside", "beneath", "beyond",
    "across", "throughout", "towards", "toward", "inside", "outside", "except",
    # coordinating conjunctions
    "and", "but", "or", "nor", "yet", "so",
    # subordinating conjunctions
    "if", "unless", "until", "while", "although", "though", "since",
    "because", "when", "where", "whereas", "whether", "after", "before",
    "even",
    # pronouns
    "i", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "mine", "yours", "hers", "ours", "theirs",
    "myself", "yourself", "himself", "herself", "itself",
    "ourselves", "themselves",
    "who", "whom", "whose", "which", "that", "what",
    "this", "these", "those",
    # auxiliary and modal verbs
    "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had",
    "do", "does", "did",
    "will", "would", "shall", "should",
    "may", "might", "must", "can", "could",
    # negation, quantifiers, determiners
    "not", "no", "never", "none",
    "all", "each", "every", "either", "neither", "both",
    "some", "any", "few", "many", "much", "more", "most",
    "other", "another", "such", "same",
    # wh-words
    "where", "when", "why", "how",
    # misc
    "there", "here", "than", "'s", "n't",
}

# Punctuation characters (stripped token = exactly one of these)
PUNCT_CHARS = set(".,;:!?—–-()[]{}\"'`/\\|@#$%^&*")


def classify_token(tok_str: str) -> str:
    """Return 'punct', 'function', or 'content' for a token string."""
    stripped = tok_str.strip().lower()
    if not stripped:
        return "function"  # whitespace/empty = functional
    # Pure punctuation: every character is punctuation
    if all(c in PUNCT_CHARS for c in stripped):
        return "punct"
    # Multi-char punctuation ligatures
    if stripped in {"...", "--", "---", "``", "''"}:
        return "punct"
    # Contractions: classify by stem ('re, 've, 'll, 'd, 'm)
    if stripped in {"'re", "'ve", "'ll", "'d", "'m", "'t"}:
        return "function"
    if stripped in FUNCTION_WORDS:
        return "function"
    return "content"


def pearson_r(xs, ys):
    n = len(xs)
    if n < 2:
        return float("nan")
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs) / n)
    sy = math.sqrt(sum((y - my) ** 2 for y in ys) / n)
    return cov / (sx * sy) if sx > 0 and sy > 0 else float("nan")


def main():
    with open(CORPUS_PATH) as f:
        corpus = json.load(f)

    CATS = ["punct", "function", "content"]

    # s2_by_cell[pred_cat][chosen_cat] → list of s2 values
    s2_by_cell = {p: {c: [] for c in CATS} for p in CATS}

    # era-level: era → {pred_cat → {chosen_cat → [s2]}}
    era_cells = defaultdict(lambda: {p: {c: [] for c in CATS} for p in CATS})

    # author-level
    author_cells = defaultdict(lambda: {p: {c: [] for c in CATS} for p in CATS})

    # Exemplars: top examples per cell
    exemplars = {p: {c: [] for c in CATS} for p in CATS}

    total_tokens = 0
    qualifying_tokens = 0

    for poem in corpus:
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue
        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "unknown")
        tokens = poem["tokens"]

        for tok in tokens:
            if tok.get("p_newline", 0) >= P_NEWLINE_MAX:
                continue
            total_tokens += 1
            s2 = tok["s2"]
            if abs(s2) < S2_THRESHOLD:
                continue
            qualifying_tokens += 1

            actual = tok.get("token", "")
            alts = tok.get("alternatives", [])
            if not alts:
                continue
            predicted = alts[0]["token"]

            pred_cat = classify_token(predicted)
            chosen_cat = classify_token(actual)

            s2_by_cell[pred_cat][chosen_cat].append(s2)
            era_cells[era][pred_cat][chosen_cat].append(s2)
            author_cells[author][pred_cat][chosen_cat].append(s2)

            # Collect exemplars for cross-register cells
            if pred_cat != chosen_cat:
                cell = exemplars[pred_cat][chosen_cat]
                entry = {
                    "s2": s2,
                    "token": actual,
                    "predicted": predicted,
                    "author": author,
                    "era": era,
                }
                cell.append(entry)
                cell.sort(key=lambda x: -x["s2"])
                if len(cell) > 10:
                    cell.pop()

    print(f"English tokens analyzed: {total_tokens}")
    print(f"Qualifying tokens (|S2| ≥ {S2_THRESHOLD}): {qualifying_tokens}\n")

    # ── 3x3 S2 matrix ───────────────────────────────────────────────────────
    print("=" * 70)
    print("3×3 MEAN S₂ MATRIX")
    print("  rows = GPT-2 top prediction register")
    print("  cols = poet's actual token register")
    print("=" * 70)
    header = f"{'Predicted →':22}" + "".join(f"  {c:>12}" for c in CATS) + "  {'N total':>8}"
    print(header)
    print("-" * 70)

    matrix_data = {}
    for pred in CATS:
        row_total = sum(len(s2_by_cell[pred][c]) for c in CATS)
        cells_str = ""
        matrix_data[pred] = {}
        for chosen in CATS:
            vals = s2_by_cell[pred][chosen]
            if vals:
                m = sum(vals) / len(vals)
                matrix_data[pred][chosen] = {"mean_s2": m, "n": len(vals)}
                cells_str += f"  {m:>+12.3f}"
            else:
                matrix_data[pred][chosen] = {"mean_s2": float("nan"), "n": 0}
                cells_str += f"  {'—':>12}"
        print(f"{'Predicts ' + pred:22}{cells_str}  {row_total:>8}")
    print()

    # ── Count matrix ────────────────────────────────────────────────────────
    print("=" * 70)
    print("3×3 COUNT MATRIX (N tokens per cell)")
    print("=" * 70)
    print(header)
    print("-" * 70)
    for pred in CATS:
        row_total = sum(len(s2_by_cell[pred][c]) for c in CATS)
        cells_str = "".join(
            f"  {len(s2_by_cell[pred][c]):>12}" for c in CATS
        )
        print(f"{'Predicts ' + pred:22}{cells_str}  {row_total:>8}")
    print()

    # ── Cross-register rate ──────────────────────────────────────────────────
    diagonal = sum(len(s2_by_cell[c][c]) for c in CATS)
    off_diag = qualifying_tokens - diagonal
    print(f"Cross-register violations: {off_diag:,} / {qualifying_tokens:,} = {100*off_diag/qualifying_tokens:.1f}%")
    print(f"Register conformity:       {diagonal:,} / {qualifying_tokens:,} = {100*diagonal/qualifying_tokens:.1f}%\n")

    # ── Top cross-register exemplars ─────────────────────────────────────────
    print("=" * 70)
    print("TOP EXEMPLARS: CROSS-REGISTER VIOLATIONS (highest S₂)")
    print("=" * 70)
    for pred in CATS:
        for chosen in CATS:
            if pred == chosen:
                continue
            exs = exemplars[pred][chosen]
            if not exs:
                continue
            print(f"\n  Predicted {pred.upper()} → chose {chosen.upper()}  (top 5 by S₂):")
            print(f"  {'Token':20} {'Predicted':18} {'S2':>8}  {'Author':25} {'Era':20}")
            print("  " + "-" * 95)
            for e in exs[:5]:
                tok_r = repr(e["token"])[:18]
                pred_r = repr(e["predicted"])[:16]
                print(f"  {tok_r:20} {pred_r:18} {e['s2']:>8.2f}  {e['author'][:24]:25} {e['era'][:19]:20}")
    print()

    # ── Era breakdown: cross-register fraction ───────────────────────────────
    print("=" * 70)
    print("ERA BREAKDOWN: % cross-register tokens + mean cross-register S₂")
    print("=" * 70)
    era_rows = []
    for era, cells in era_cells.items():
        total = sum(len(cells[p][c]) for p in CATS for c in CATS)
        cross = sum(len(cells[p][c]) for p in CATS for c in CATS if p != c)
        cross_s2_vals = [s for p in CATS for c in CATS if p != c
                         for s in cells[p][c]]
        if total < 5:
            continue
        pct = 100 * cross / total if total else 0
        mean_cs = sum(cross_s2_vals) / len(cross_s2_vals) if cross_s2_vals else float("nan")

        # specific cell: predict function, chose content (semantic invasion)
        invasion = cells["function"]["content"]
        inv_pct = 100 * len(invasion) / total if total else 0

        era_rows.append((era, total, pct, mean_cs, inv_pct))

    era_rows.sort(key=lambda x: -x[2])  # sort by cross-register pct
    print(f"{'Era':30} {'N':>6} {'%Cross':>7} {'MeanS₂':>8} {'%FuncInv':>10}")
    print("-" * 65)
    for era, n, pct, ms, inv in era_rows:
        print(f"{era:30} {n:>6} {pct:>7.1f}% {ms:>8.3f} {inv:>9.1f}%")
    print()

    # ── Key cross-register cells compared ────────────────────────────────────
    print("=" * 70)
    print("CROSS-REGISTER COMPARISON: MEAN S₂ BY VIOLATION TYPE")
    print("=" * 70)
    comparisons = [
        ("func→content (semantic invasion)", s2_by_cell["function"]["content"]),
        ("func→punct   (abbreviation)", s2_by_cell["function"]["punct"]),
        ("content→func (grammatical retreat)", s2_by_cell["content"]["function"]),
        ("content→punct (content cut short)", s2_by_cell["content"]["punct"]),
        ("punct→content (punctual surprise)", s2_by_cell["punct"]["content"]),
        ("punct→func   (punct continuity)", s2_by_cell["punct"]["function"]),
        # diagonal
        ("func→func    (grammatical conformity)", s2_by_cell["function"]["function"]),
        ("content→content (semantic divergence)", s2_by_cell["content"]["content"]),
        ("punct→punct  (punctuation match)", s2_by_cell["punct"]["punct"]),
    ]
    print(f"{'Type':45} {'N':>7} {'MeanS₂':>8} {'PctPos':>8}")
    print("-" * 72)
    for label, vals in comparisons:
        if not vals:
            continue
        m = sum(vals) / len(vals)
        pct_pos = 100 * sum(1 for v in vals if v > 0) / len(vals)
        print(f"{label:45} {len(vals):>7} {m:>8.3f} {pct_pos:>7.1f}%")
    print()

    # ── Author signature: func-invasion rate ────────────────────────────────
    print("=" * 70)
    print("AUTHOR SIGNATURE: TOP 15 BY SEMANTIC INVASION RATE (func→content)")
    print("=" * 70)
    author_rows = []
    for author, cells in author_cells.items():
        total = sum(len(cells[p][c]) for p in CATS for c in CATS)
        if total < 10:
            continue
        invasion_n = len(cells["function"]["content"])
        retreat_n = len(cells["content"]["function"])
        inv_pct = 100 * invasion_n / total
        ret_pct = 100 * retreat_n / total
        inv_s2 = (sum(cells["function"]["content"]) / invasion_n
                  if invasion_n else float("nan"))
        author_rows.append((author, total, inv_pct, ret_pct, inv_s2))

    author_rows.sort(key=lambda x: -x[2])
    print(f"{'Author':30} {'N':>6} {'%Invasion':>10} {'%Retreat':>9} {'InvMeanS₂':>12}")
    print("-" * 72)
    for author, n, inv_pct, ret_pct, inv_s2 in author_rows[:15]:
        inv_s2_str = f"{inv_s2:>12.3f}" if not math.isnan(inv_s2) else "       N/A"
        print(f"{author[:29]:30} {n:>6} {inv_pct:>10.1f}% {ret_pct:>8.1f}% {inv_s2_str}")
    print()

    results = {
        "total_tokens": total_tokens,
        "qualifying_tokens": qualifying_tokens,
        "matrix": {
            pred: {
                chosen: matrix_data[pred][chosen]
                for chosen in CATS
            }
            for pred in CATS
        },
        "era_data": {
            era: {
                "n": n,
                "cross_register_pct": pct,
                "mean_cross_s2": ms,
                "func_invasion_pct": inv,
            }
            for era, n, pct, ms, inv in era_rows
        },
        "cross_register_total_pct": 100 * off_diag / qualifying_tokens,
    }

    out_path = "results/prediction_register_gap.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Saved to {out_path}")
    return results


if __name__ == "__main__":
    main()
