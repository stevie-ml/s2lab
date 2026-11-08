"""
Speech Act S2: Performative vs. Constative Verbs in Poetry

Research question: Do performative verbs (Austin's illocutionaries — swear,
promise, declare, bless, curse, vow, proclaim) carry higher S2 than constative
verbs (see, feel, know, think, believe)?

Hypothesis: Performative verbs are "world-changing" speech acts — they don't
describe reality but enact it. In poetry, these verbs appear at moments of
maximum commitment. GPT-2, trained on descriptive prose, doesn't anticipate
"I swear" or "I curse thee" at positions where it expects "I see" or "I feel."

Sub-questions:
1. Do performative verbs have higher S2 than constative verbs?
2. What does GPT-2 expect at performative positions?
3. Which poets use performatives most strategically?
4. Do specific speech act categories (blessing/cursing vs. promising vs.
   declaring) differ in S2?
5. Is there a first-person constraint? ("I swear" vs. bare "swear")
"""

import json
import re
from collections import defaultdict
import statistics

DATA_PATH = "results/corpus_results.json"

# Austin/Searle taxonomy of speech act verbs
# Commissives: speaker commits to future action
COMMISSIVES = {
    "promise", "vow", "swear", "pledge", "guarantee", "commit", "dedicate",
    "devote", "undertake", "covenant", "bind", "offer", "volunteer",
}

# Expressives: express psychological state sincerely
EXPRESSIVES = {
    "thank", "apologize", "congratulate", "condole", "mourn", "lament",
    "grieve", "regret", "celebrate", "bless", "curse", "damn", "forgive",
    "pardon", "deplore", "bewail", "bemoan", "rejoice", "welcome", "praise",
    "worship", "adore", "revere", "cherish", "loathe", "detest", "abhor",
}

# Declarations: change institutional reality
DECLARATIONS = {
    "declare", "proclaim", "announce", "pronounce", "ordain", "appoint",
    "crown", "baptize", "christen", "name", "dub", "designate", "sentence",
    "condemn", "absolve", "acquit", "excommunicate", "consecrate", "dedicate",
}

# Directives: attempt to get hearer to do something
DIRECTIVES = {
    "command", "order", "demand", "request", "beg", "implore", "beseech",
    "plead", "pray", "entreat", "adjure", "conjure", "invoke", "summon",
    "call", "bid", "charge", "urge", "exhort", "warn", "forbid",
}

# Constative / assertive verbs (control group) - describe internal states
CONSTATIVES_MENTAL = {
    "see", "hear", "feel", "know", "think", "believe", "wonder", "imagine",
    "remember", "forget", "dream", "sense", "perceive", "understand",
    "realize", "recognize", "notice", "observe", "find", "discover",
}

# Constative / assertive verbs - describe actions
CONSTATIVES_ACTION = {
    "walk", "run", "stand", "sit", "lie", "sleep", "wake", "move", "turn",
    "look", "watch", "wait", "go", "come", "rise", "fall", "open", "close",
    "hold", "take", "give", "make", "keep", "put", "set", "let",
}

ALL_PERFORMATIVE = COMMISSIVES | EXPRESSIVES | DECLARATIONS | DIRECTIVES
ALL_CONSTATIVE = CONSTATIVES_MENTAL | CONSTATIVES_ACTION


def classify_token(tok_str):
    """Classify a verb token into speech act categories."""
    t = tok_str.strip().lower().rstrip("s")  # crude lemmatization
    t_base = tok_str.strip().lower()

    for base in [t_base, t]:
        if base in COMMISSIVES:
            return "commissive"
        if base in EXPRESSIVES:
            return "expressive"
        if base in DECLARATIONS:
            return "declaration"
        if base in DIRECTIVES:
            return "directive"
        if base in CONSTATIVES_MENTAL:
            return "constative_mental"
        if base in CONSTATIVES_ACTION:
            return "constative_action"
    return None


def main():
    with open(DATA_PATH) as f:
        data = json.load(f)

    # Collect tokens by speech act category
    categories = defaultdict(list)
    # Track first-person context (token preceded by "I" or "i")
    first_person_tokens = defaultdict(list)

    # Track top examples per category
    top_examples = defaultdict(list)

    for poem in data:
        meta = poem["metadata"]
        tokens = poem.get("tokens", [])

        # Exclude stanza-break artifacts
        clean_tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]

        for i, tok in enumerate(clean_tokens):
            tok_str = tok["token"]
            cat = classify_token(tok_str)
            if cat is None:
                continue

            s2 = tok["s2"]
            record = {
                "token": tok_str.strip(),
                "s2": s2,
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
                "rank": tok["rank"],
                "alternatives": tok.get("alternatives", []),
                "context_before": tok.get("context_before", ""),
                "author": meta.get("author", "Unknown"),
                "title": meta.get("title", "Unknown"),
                "era": meta.get("era", "unknown"),
            }
            categories[cat].append(record)

            # Check for first-person usage
            ctx = tok.get("context_before", "")
            last_tokens = ctx.split()[-3:] if ctx else []
            is_first_person = any(w.lower() in {"i", "i'll", "i've", "i'd", "i'm"}
                                  for w in last_tokens)
            if is_first_person:
                first_person_tokens[cat].append(record)

    # --- Print summary table ---
    print("\n## Speech Act S2 Summary\n")
    print(f"{'Category':<24} {'N':>6} {'Mean S2':>9} {'Median S2':>10} {'Pos%':>6} {'Max S2':>8}")
    print("-" * 70)

    # Group for comparison
    group_order = [
        ("commissive", "Commissive (vow/promise)"),
        ("expressive", "Expressive (bless/curse)"),
        ("declaration", "Declaration (proclaim)"),
        ("directive", "Directive (implore/bid)"),
        ("constative_mental", "Constative: mental"),
        ("constative_action", "Constative: action"),
    ]

    summary = {}
    for cat, label in group_order:
        recs = categories[cat]
        if len(recs) < 5:
            print(f"  {label:<22} {'<5 tokens, skipping':>40}")
            continue
        vals = [r["s2"] for r in recs]
        pos_pct = 100 * sum(1 for v in vals if v > 0) / len(vals)
        mean_s2 = statistics.mean(vals)
        median_s2 = statistics.median(vals)
        max_s2 = max(vals)
        summary[cat] = {
            "n": len(recs),
            "mean": mean_s2,
            "median": median_s2,
            "pos_pct": pos_pct,
            "max": max_s2,
            "records": recs,
        }
        print(f"  {label:<22} {len(recs):>6} {mean_s2:>9.3f} {median_s2:>10.3f} "
              f"{pos_pct:>5.1f}% {max_s2:>8.2f}")

    # --- First-person constraint ---
    print("\n## First-Person Constraint\n")
    print("Speech acts are canonical when the speaker is 'I':\n")
    print(f"{'Category':<24} {'All':>6} {'1st-person':>12} {'1st-prs mean S2':>16}")
    print("-" * 65)
    for cat, label in group_order:
        recs = categories[cat]
        fp_recs = first_person_tokens[cat]
        if len(recs) < 5:
            continue
        all_mean = statistics.mean(r["s2"] for r in recs)
        fp_mean = statistics.mean(r["s2"] for r in fp_recs) if fp_recs else float("nan")
        print(f"  {label:<22} {len(recs):>6} {len(fp_recs):>12} {fp_mean:>16.3f}")

    # --- Top examples per performative category ---
    print("\n## Top High-S2 Examples by Category\n")
    for cat, label in [
        ("commissive", "COMMISSIVE"),
        ("expressive", "EXPRESSIVE"),
        ("declaration", "DECLARATION"),
        ("directive", "DIRECTIVE"),
    ]:
        recs = categories.get(cat, [])
        if not recs:
            continue
        top = sorted(recs, key=lambda x: -x["s2"])[:5]
        print(f"### {label}\n")
        for r in top:
            alts = r["alternatives"][:3] if r["alternatives"] else []
            alt_str = " / ".join(f'"{a["token"].strip()}"' for a in alts)
            ctx_snippet = r["context_before"][-50:].strip() if r["context_before"] else ""
            print(f"  '{r['token']}' (S2={r['s2']:.2f}) — {r['author']}, {r['title']}")
            print(f"    Context: ...{ctx_snippet}")
            print(f"    GPT-2 expected: {alt_str}")
            print()

    # --- What does GPT-2 suppress? ---
    print("\n## GPT-2's Suppressed Alternatives at Performative Positions\n")
    all_perf_records = []
    for cat in ["commissive", "expressive", "declaration", "directive"]:
        all_perf_records.extend(categories.get(cat, []))

    alt_counter = defaultdict(int)
    for r in all_perf_records:
        for alt in (r["alternatives"][:3] if r["alternatives"] else []):
            alt_counter[alt["token"].strip()] += 1

    print("Top tokens GPT-2 expected at performative verb positions:\n")
    top_alts = sorted(alt_counter.items(), key=lambda x: -x[1])[:20]
    for tok, count in top_alts:
        print(f"  '{tok}': {count} times")
    print()

    # --- Save results ---
    results = {
        "summary": {
            cat: {k: v for k, v in vals.items() if k != "records"}
            for cat, vals in summary.items()
        },
        "top_examples": {},
        "suppressed_alternatives": [{"token": t, "count": c} for t, c in top_alts[:20]],
        "first_person_counts": {
            cat: len(first_person_tokens[cat]) for cat in categories
        },
    }
    for cat in ["commissive", "expressive", "declaration", "directive"]:
        recs = categories.get(cat, [])
        top = sorted(recs, key=lambda x: -x["s2"])[:10]
        results["top_examples"][cat] = top

    out_path = "findings/speech_act_s2.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n[Saved to {out_path}]")


if __name__ == "__main__":
    main()
