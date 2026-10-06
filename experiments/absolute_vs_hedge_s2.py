"""
The Rhetoric of Totality vs. Qualification: Absolute vs. Hedged Language in Poetry

Research question: Do grand absolute claims ("always", "never", "everything", "nothing",
"forever", "eternal") cost more or less surprise than epistemic hedges ("perhaps",
"maybe", "seems", "might", "almost")?

Poets are famous for totalizing gestures: "I contain multitudes", "Nothing gold can stay",
"Forever and a day." But hedges appear too: "seems", "perhaps", "as if." This experiment
tests whether each class is informationally "cheap" or "expensive" relative to the poem
as a whole.

Hypothesis A (Grand claims are cheap): The poetic register foregrounds absolute terms;
GPT-2 expects them. Low S2 — the poet buys grandeur at a discount.

Hypothesis B (Grand claims are expensive): Even in poetry, "always" and "never" are
rare in actual context — they spike S2 because the model expects more specific words.

Hypothesis C (Hedges are surprising): Because poetry typically projects confidence,
a hedge word is statistically unexpected — the poet choosing "perhaps" surprises the
model that expected a bolder word.

Method:
- For each English poem, scan all tokens for matches to our term lists
- Record S2, entropy, surprisal, rank, and what the model predicted instead
- Compare distributions across the two classes vs. poem baseline
- Break down by era and author
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_PATH = "results/corpus_results.json"

# ── Term lists ─────────────────────────────────────────────────────────────────
# Stripped/lowercased — we match the token stripped of leading spaces.
ABSOLUTE_TERMS = {
    "always", "never", "all", "nothing", "everything", "everybody", "everyone",
    "everywhere", "nowhere", "forever", "eternal", "eternity", "infinite",
    "infinity", "absolute", "completely", "utterly", "entirely", "wholly",
    "perfectly", "certainly", "certainly", "inevitably", "necessarily",
    "every", "none", "no", "whole", "total", "pure", "perfect", "ultimate",
    "forever", "evermore", "forevermore", "always", "constant", "unchanging",
    "immortal", "immortality", "endless", "boundless", "infinite",
}

HEDGE_TERMS = {
    "perhaps", "maybe", "possibly", "probably", "seemingly", "apparently",
    "almost", "nearly", "somewhat", "rather", "quite", "fairly", "partly",
    "partially", "barely", "hardly", "scarcely", "rarely", "seldom",
    "might", "could", "would", "should", "seems", "seem", "seemed",
    "appears", "appear", "appeared", "suggests", "suggest", "implies",
    "imply", "like",  # simile marker
    "as", "though", "although",  # conditional comparisons
    "perhaps", "maybe",
}

# Simile markers — "like" and "as" are context-dependent; we flag them separately
SIMILE_MARKERS = {"like", "as", "though"}

# Words that OVERLAP — remove from both
OVERLAP = ABSOLUTE_TERMS & HEDGE_TERMS
ABSOLUTE_TERMS -= OVERLAP
HEDGE_TERMS -= OVERLAP

# "no" is absolute but also a common function word — track separately
STRONG_ABSOLUTE = {"always", "never", "nothing", "everything", "everyone", "everywhere",
                   "nowhere", "forever", "eternal", "eternity", "infinite", "infinity",
                   "immortal", "immortality", "evermore", "forevermore", "endless",
                   "boundless"}
STRONG_HEDGE = {"perhaps", "maybe", "possibly", "probably", "almost", "nearly",
                "seemed", "seems", "appear", "appears", "appeared"}


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    top = alts[0]
    return top["token"] in ("\n", "\r\n", "\r") and top["prob"] >= 0.9


def normalize(token_str):
    """Strip leading space, lowercase."""
    return token_str.strip().lower()


def classify_token(norm):
    """Return 'absolute', 'hedge', 'simile', or None."""
    if norm in STRONG_ABSOLUTE or norm in ABSOLUTE_TERMS:
        return "absolute"
    if norm in STRONG_HEDGE or norm in HEDGE_TERMS:
        return "hedge"
    return None


def top_predicted(tok):
    alts = tok.get("alternatives", [])
    if alts:
        return normalize(alts[0]["token"])
    return None


def run():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Filter to English poems only, excluding control prose
    poems = [d for d in data
             if d["metadata"].get("language", "en") == "en"
             and d["metadata"].get("era") not in ("control",)]

    # ── Collect token records ─────────────────────────────────────────────────
    records = defaultdict(list)  # class → list of token dicts with extras
    baseline_s2 = []             # all non-artifact tokens
    era_data = defaultdict(lambda: defaultdict(list))  # era → class → s2 list
    author_data = defaultdict(lambda: defaultdict(list))  # author → class → s2

    for poem in poems:
        author = poem["metadata"]["author"]
        era    = poem["metadata"]["era"]

        # Compute poem-level baseline (non-artifact)
        poem_s2_clean = [t["s2"] for t in poem["tokens"] if not is_artifact(t)]
        poem_baseline  = statistics.mean(poem_s2_clean) if poem_s2_clean else 0.0

        for tok in poem["tokens"]:
            if is_artifact(tok):
                continue
            s2   = tok["s2"]
            norm = normalize(tok["token"])
            cls  = classify_token(norm)

            baseline_s2.append(s2)

            if cls is not None:
                rec = {
                    "s2":            s2,
                    "surprisal":     tok["surprisal"],
                    "entropy":       tok["entropy"],
                    "rank":          tok.get("rank", 9999),
                    "token":         norm,
                    "top_predicted": top_predicted(tok),
                    "poem_baseline": poem_baseline,
                    "deviation":     s2 - poem_baseline,
                    "author":        author,
                    "era":           era,
                    "title":         poem["metadata"]["title"],
                }
                records[cls].append(rec)
                era_data[era][cls].append(s2)
                author_data[author][cls].append(s2)

    # ── Statistics helpers ────────────────────────────────────────────────────
    def stats(vals):
        if not vals:
            return {}
        return {
            "n":       len(vals),
            "mean":    round(statistics.mean(vals), 3),
            "median":  round(statistics.median(vals), 3),
            "stdev":   round(statistics.stdev(vals), 3) if len(vals) > 1 else 0.0,
            "pct_pos": round(sum(1 for v in vals if v > 0) / len(vals) * 100, 1),
        }

    # ── Global stats ─────────────────────────────────────────────────────────
    global_abs  = [r["s2"] for r in records["absolute"]]
    global_hedge = [r["s2"] for r in records["hedge"]]
    baseline_stats = stats(baseline_s2)

    # ── Top predicted alternatives for each class ─────────────────────────────
    def top_predictions(cls, n=15):
        counter = defaultdict(int)
        for r in records[cls]:
            tp = r["top_predicted"]
            if tp:
                counter[tp] += 1
        return sorted(counter.items(), key=lambda x: -x[1])[:n]

    # ── Per-term breakdown ────────────────────────────────────────────────────
    term_stats = {}
    for cls in ("absolute", "hedge"):
        term_groups = defaultdict(list)
        for r in records[cls]:
            term_groups[r["token"]].append(r["s2"])
        term_stats[cls] = {
            tok: stats(vals)
            for tok, vals in sorted(term_groups.items(), key=lambda x: -len(x[1]))
            if len(vals) >= 3
        }

    # ── Era breakdown ─────────────────────────────────────────────────────────
    era_comparison = {}
    for era in sorted(era_data.keys()):
        abs_vals  = era_data[era]["absolute"]
        hedge_vals = era_data[era]["hedge"]
        if len(abs_vals) >= 3 or len(hedge_vals) >= 3:
            era_comparison[era] = {
                "absolute": stats(abs_vals) if abs_vals else {},
                "hedge":    stats(hedge_vals) if hedge_vals else {},
            }

    # ── Author breakdown (min 5 tokens each class) ──────────────────────────
    author_comparison = {}
    for author in sorted(author_data.keys()):
        abs_vals  = author_data[author]["absolute"]
        hedge_vals = author_data[author]["hedge"]
        if len(abs_vals) + len(hedge_vals) >= 10:
            author_comparison[author] = {
                "absolute": stats(abs_vals) if abs_vals else {},
                "hedge":    stats(hedge_vals) if hedge_vals else {},
                "abs_count":   len(abs_vals),
                "hedge_count": len(hedge_vals),
                "abs_ratio":   round(len(abs_vals) / (len(abs_vals) + len(hedge_vals)), 3),
            }

    # ── Strongest deviations from poem baseline ───────────────────────────────
    def top_deviations(cls, n=10):
        recs = sorted(records[cls], key=lambda r: -abs(r["deviation"]))[:n]
        return [
            {
                "token":     r["token"],
                "s2":        round(r["s2"], 2),
                "deviation": round(r["deviation"], 2),
                "poem":      r["title"],
                "author":    r["author"],
                "top_pred":  r["top_predicted"],
            }
            for r in recs
        ]

    # ── Assemble output ───────────────────────────────────────────────────────
    result = {
        "baseline":    baseline_stats,
        "absolute":    stats(global_abs),
        "hedge":       stats(global_hedge),
        "term_stats":  term_stats,
        "era_comparison": era_comparison,
        "author_comparison": author_comparison,
        "top_absolute_predictions": top_predictions("absolute"),
        "top_hedge_predictions":    top_predictions("hedge"),
        "top_deviations_absolute":  top_deviations("absolute"),
        "top_deviations_hedge":     top_deviations("hedge"),
        "n_poems": len(poems),
    }

    return result


if __name__ == "__main__":
    result = run()
    import json
    print(json.dumps(result, indent=2))
