"""
Copula Predication and S2: Do poets make more surprising identity claims?

Hypothesis: tokens immediately following a copula ("is", "are", "was", "were")
have higher S2 in poetry than prose, because poets use unusual predications
("love is a door," "night was a wound") to encode metaphor. The Straussian gap
at predications quantifies the semantic boldness of poetic identity claims.
"""

import json
import re
from collections import defaultdict
import statistics

DATA_FILE = "results/corpus_results.json"

# Copula surface forms (as they appear after tokenization: leading space matters)
COPULA_FORMS = {
    " is", " are", " was", " were", " be", " been",
    "'s",   # contracted "is" (e.g., "love's a door")
    " am",  # first person
}

# Stanza-break artifact filter (same as used in other experiments)
P_NEWLINE_THRESHOLD = 0.9


def is_copula(token_text: str) -> bool:
    return token_text in COPULA_FORMS


def is_artifact(token: dict) -> bool:
    return token.get("p_newline", 0) >= P_NEWLINE_THRESHOLD


def analyze_copula_predications(data):
    """
    For each poem, find copula tokens and record S2 of the following token.
    Returns lists of (s2, era, title, author, copula_token, predicate_token, context)
    """
    results = []

    for poem in data:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue

        tokens = poem["tokens"]
        era = meta["era"]
        title = meta["title"]
        author = meta["author"]
        is_control = era in ("control",)

        for i, tok in enumerate(tokens):
            if i + 1 >= len(tokens):
                continue
            if is_artifact(tok) or is_artifact(tokens[i + 1]):
                continue
            if is_copula(tok["token"]):
                pred_tok = tokens[i + 1]
                # Skip punctuation and whitespace tokens as predicates
                pred_text = pred_tok["token"].strip()
                if not pred_text or pred_text in (".", ",", "!", "?", ":", ";", "-", "--", "'", '"'):
                    continue
                results.append({
                    "s2": pred_tok["s2"],
                    "surprisal": pred_tok["surprisal"],
                    "entropy": pred_tok["entropy"],
                    "era": era,
                    "title": title,
                    "author": author,
                    "copula": tok["token"],
                    "predicate": pred_tok["token"],
                    "rank": pred_tok.get("rank", None),
                    "alternatives": pred_tok.get("alternatives", [])[:3],
                    "is_control": is_control,
                    "context": tok.get("context_before", "")[-30:],
                    "p_newline": pred_tok.get("p_newline", 0),
                })

    return results


def compute_baseline(data):
    """Average S2 across all non-artifact tokens in poetry vs prose."""
    poetry_s2 = []
    prose_s2 = []
    for poem in data:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue
        is_ctrl = meta["era"] == "control"
        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            if is_ctrl:
                prose_s2.append(tok["s2"])
            else:
                poetry_s2.append(tok["s2"])
    return (
        statistics.mean(poetry_s2), statistics.stdev(poetry_s2),
        statistics.mean(prose_s2), statistics.stdev(prose_s2),
        len(poetry_s2), len(prose_s2),
    )


def main():
    with open(DATA_FILE) as f:
        data = json.load(f)

    events = analyze_copula_predications(data)

    poetry_events = [e for e in events if not e["is_control"]]
    prose_events = [e for e in events if e["is_control"]]

    poetry_s2 = [e["s2"] for e in poetry_events]
    prose_s2 = [e["s2"] for e in prose_events]

    print(f"Total copula-predication events: {len(events)}")
    print(f"  Poetry: {len(poetry_events)}")
    print(f"  Prose control: {len(prose_events)}")
    print()

    pm, ps = statistics.mean(poetry_s2), statistics.stdev(poetry_s2) if len(poetry_s2) > 1 else (0, 0)
    prm, prs = (statistics.mean(prose_s2), statistics.stdev(prose_s2)) if prose_s2 else (None, None)

    print(f"Avg S2 at predicates — Poetry: {pm:.3f} ± {ps:.3f}")
    if prm is not None:
        print(f"Avg S2 at predicates — Prose:  {prm:.3f} ± {prs:.3f}")
    print()

    # Baseline comparison
    bpm, bps, bprm, bprs, bn_po, bn_pr = compute_baseline(data)
    print(f"Baseline avg S2 (all tokens) — Poetry: {bpm:.3f} ± {bps:.3f}  (n={bn_po})")
    print(f"Baseline avg S2 (all tokens) — Prose:  {bprm:.3f} ± {bprs:.3f}  (n={bn_pr})")
    print()
    print(f"Copula-predicate lift over baseline — Poetry: {pm - bpm:+.3f}")
    if prm is not None:
        print(f"Copula-predicate lift over baseline — Prose:  {prm - bprm:+.3f}")
    print()

    # By era
    era_data = defaultdict(list)
    for e in poetry_events:
        era_data[e["era"]].append(e["s2"])

    era_stats = sorted(
        [(era, statistics.mean(vals), len(vals)) for era, vals in era_data.items() if len(vals) >= 3],
        key=lambda x: -x[1]
    )
    print("S2 at copula-predicates by era (≥3 events):")
    print(f"{'Era':<25} {'n':>5} {'Avg S2':>10}")
    print("-" * 45)
    for era, mean_s2, n in era_stats:
        print(f"{era:<25} {n:>5} {mean_s2:>10.3f}")
    print()

    # By copula form
    copula_data = defaultdict(list)
    for e in poetry_events:
        copula_data[e["copula"].strip()].append(e["s2"])

    print("S2 at predicates by copula form:")
    print(f"{'Copula':<10} {'n':>5} {'Avg S2':>10}")
    print("-" * 30)
    for cop, vals in sorted(copula_data.items(), key=lambda x: -statistics.mean(x[1]) if x[1] else 0):
        if vals:
            print(f"{cop:<10} {len(vals):>5} {statistics.mean(vals):>10.3f}")
    print()

    # Top 20 most surprising predications
    print("Top 20 most surprising predicates (highest S2 in poetry):")
    print(f"{'S2':>7} {'Rank':>6}  {'Author':<20} {'Copula':<6} {'Predicate':<20} {'vs Expected':<15}")
    print("-" * 80)
    top_events = sorted(poetry_events, key=lambda x: -x["s2"])[:20]
    for e in top_events:
        top_pred = e["alternatives"][0]["token"].strip() if e["alternatives"] else "?"
        print(f"{e['s2']:>7.2f} {str(e['rank'] or '?'):>6}  {e['author'][:20]:<20} "
              f"{e['copula'].strip():<6} {e['predicate'].strip()[:20]:<20} vs '{top_pred}'")
    print()

    # Predicate token type analysis: articles, nouns, adjectives
    # GPT-2 doesn't have POS tags, but we can categorize by whether the predicate
    # starts with "a/an/the" (nominal predication) vs adjective (descriptive predication)
    nominal_pred = [e for e in poetry_events if e["predicate"].strip().lower() in ("a", "an", "the", "this", "that", "my", "your", "his", "her", "its", "our", "their", "no")]
    adj_pred = [e for e in poetry_events if e["predicate"].strip().lower() not in ("a", "an", "the", "this", "that", "my", "your", "his", "her", "its", "our", "their", "no")]

    if nominal_pred and adj_pred:
        nom_s2 = [e["s2"] for e in nominal_pred]
        adj_s2 = [e["s2"] for e in adj_pred]
        print(f"Nominal predication (X is a/the Y): n={len(nominal_pred)}, avg S2={statistics.mean(nom_s2):.3f}")
        print(f"Adjectival/other predication (X is ADJ): n={len(adj_pred)}, avg S2={statistics.mean(adj_s2):.3f}")
        print()

    # Fraction of predications above baseline S2
    pct_positive = sum(1 for s in poetry_s2 if s > 0) / len(poetry_s2) * 100 if poetry_s2 else 0
    pct_positive_prose = sum(1 for s in prose_s2 if s > 0) / len(prose_s2) * 100 if prose_s2 else 0
    print(f"% of poetic predicates with S2 > 0: {pct_positive:.1f}%")
    if prose_s2:
        print(f"% of prose predicates with S2 > 0:  {pct_positive_prose:.1f}%")

    return {
        "poetry_mean_s2": pm,
        "poetry_std_s2": ps,
        "prose_mean_s2": prm,
        "prose_std_s2": prs,
        "poetry_n": len(poetry_events),
        "prose_n": len(prose_events),
        "poetry_baseline": bpm,
        "prose_baseline": bprm,
        "poetry_lift": pm - bpm,
        "prose_lift": (prm - bprm) if prm is not None else None,
        "era_stats": era_stats,
        "top_events": top_events,
        "pct_positive_poetry": pct_positive,
        "pct_positive_prose": pct_positive_prose,
    }


if __name__ == "__main__":
    results = main()
    import json as _json
    with open("results/copula_predication.json", "w") as f:
        _json.dump(results, f, indent=2, default=str)
    print("\nSaved to results/copula_predication.json")
