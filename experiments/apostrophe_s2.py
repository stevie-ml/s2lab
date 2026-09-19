"""
Apostrophe and S₂: When Poets Address the Absent

Research question: Apostrophe — directly addressing an absent person, a dead person,
or a personified abstraction ("O Death", "O wild West Wind", "O Rose") — is one of
poetry's oldest rhetorical figures. When a poet suddenly shifts to direct address of
the ineffable, how does the information-theoretic profile change?

We distinguish three tiers of apostrophic signal:
  T1 (STRONG):  vocative "O"/"Oh" at line-start or after punctuation
  T2 (MEDIUM):  archaic 2nd-person pronouns: thou, thee, thy, thine
  T3 (WEAK):    non-archaic direct address: "you" in a clearly apostrophic frame

Hypotheses:
  H1. The vocative "O" / "Oh" is itself a high-S₂ token (unexpected in context).
  H2. The noun or adjective immediately following "O" carries elevated S₂
      (what entity the poet chooses to address is maximally deviant).
  H3. "thou/thee/thy" pronouns have higher S₂ than regular 2nd-person "you"
      (archaism itself is a surprising choice against the GPT-2 baseline).
  H4. Poems that use apostrophe have higher overall average S₂ than poems that don't.
  H5. GPT-2's top alternative for the vocative "O" reveals what conventional
      language would have written instead (taxonomy of the unsaid at apostrophe points).

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_FILE = "results/corpus_results.json"

# ── Token normaliser ───────────────────────────────────────────────────────────
def norm(token: str) -> str:
    return token.strip().lower()

def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")

def stdev(xs):
    return statistics.stdev(xs) if len(xs) >= 2 else float("nan")

# ── Apostrophe marker sets ─────────────────────────────────────────────────────

# T1: Vocative "O" / "Oh" / "Hail" — strong apostrophe markers
T1_MARKERS = {"o", "oh", "hail", "hark"}

# T2: Archaic 2nd-person pronouns
T2_MARKERS = {"thou", "thee", "thy", "thine", "thyself"}

# T3: Modern direct address in clearly apostrophic context (approximate via
#     "you" tokens that follow vocative markers within 5 tokens)
T3_MARKERS = {"you", "your", "yourself"}


def classify_token(tok: str) -> str:
    n = norm(tok)
    if n in T1_MARKERS:
        return "T1_vocative"
    if n in T2_MARKERS:
        return "T2_archaic"
    return None


def load_data():
    with open(RESULTS_FILE) as f:
        return json.load(f)


def is_apostrophic_poem(poem_data) -> bool:
    tokens = poem_data["tokens"]
    for t in tokens:
        n = norm(t["token"])
        if n in T1_MARKERS or n in T2_MARKERS:
            return True
    return False


def collect_marker_windows(poem_data, window_after=3):
    """
    For each apostrophe marker token, collect:
      - the marker's own S₂
      - the S₂ of the `window_after` tokens following it
      - GPT-2's top alternative at the marker position
    """
    tokens = poem_data["tokens"]
    results = []

    for i, t in enumerate(tokens):
        tier = classify_token(t["token"])
        if tier is None:
            continue

        after_s2 = []
        for j in range(1, window_after + 1):
            if i + j < len(tokens):
                after_s2.append(tokens[i + j]["s2"])

        top_alt = t["alternatives"][0]["token"] if t.get("alternatives") else None
        results.append({
            "tier": tier,
            "token": t["token"],
            "s2": t["s2"],
            "surprisal": t["surprisal"],
            "entropy": t["entropy"],
            "after_s2": after_s2,
            "first_after_s2": after_s2[0] if after_s2 else float("nan"),
            "first_after_token": tokens[i + 1]["token"] if i + 1 < len(tokens) else None,
            "top_alt": top_alt,
            "context_before": t.get("context_before", ""),
            "poem_title": poem_data["metadata"]["title"],
            "poem_author": poem_data["metadata"]["author"],
        })

    return results


def collect_all_you_tokens(poem_data):
    """Collect S₂ for all 'you/your/yourself' tokens for baseline comparison."""
    tokens = poem_data["tokens"]
    return [t["s2"] for t in tokens if norm(t["token"]) in T3_MARKERS]


def collect_all_pronoun_s2(poem_data):
    """Collect S₂ for standard 3rd-person and 1st-person pronouns as baseline."""
    BASELINE_PRONOUNS = {"i", "he", "she", "we", "they", "it", "me", "him", "her", "us", "them"}
    tokens = poem_data["tokens"]
    return [t["s2"] for t in tokens if norm(t["token"]) in BASELINE_PRONOUNS]


def run():
    data = load_data()

    # ── Separate apostrophic vs non-apostrophic poems ─────────────────────────
    apo_poems = [d for d in data if is_apostrophic_poem(d)]
    non_apo_poems = [d for d in data if not is_apostrophic_poem(d)]

    print(f"\n{'=' * 70}")
    print("APOSTROPHE AND S₂ IN POETRY")
    print(f"{'=' * 70}")
    print(f"\nCorpus: {len(data)} texts total")
    print(f"  Apostrophic (T1 or T2 markers): {len(apo_poems)}")
    print(f"  Non-apostrophic:                {len(non_apo_poems)}")

    # ── H4: Overall S₂ difference ─────────────────────────────────────────────
    apo_all_s2 = [t["s2"] for d in apo_poems for t in d["tokens"]]
    non_apo_all_s2 = [t["s2"] for d in non_apo_poems for t in d["tokens"]]

    print(f"\n── H4: Poem-level S₂ comparison ──────────────────────────────────────")
    print(f"  Apostrophic poems — avg S₂: {mean(apo_all_s2):.3f}  (n_tokens={len(apo_all_s2)})")
    print(f"  Non-apostrophic  — avg S₂: {mean(non_apo_all_s2):.3f}  (n_tokens={len(non_apo_all_s2)})")
    print(f"  Lift: {mean(apo_all_s2) - mean(non_apo_all_s2):+.3f}")

    # Per-poem averages
    apo_poem_avgs = [mean([t["s2"] for t in d["tokens"]]) for d in apo_poems]
    non_apo_poem_avgs = [mean([t["s2"] for t in d["tokens"]]) for d in non_apo_poems]
    print(f"\n  Per-poem averages:")
    print(f"    Apostrophic: {mean(apo_poem_avgs):.3f} ± {stdev(apo_poem_avgs):.3f}")
    print(f"    Non-apo:     {mean(non_apo_poem_avgs):.3f} ± {stdev(non_apo_poem_avgs):.3f}")

    # ── Collect all marker windows ─────────────────────────────────────────────
    all_markers = []
    for d in data:
        all_markers.extend(collect_marker_windows(d, window_after=3))

    t1_markers = [m for m in all_markers if m["tier"] == "T1_vocative"]
    t2_markers = [m for m in all_markers if m["tier"] == "T2_archaic"]

    # ── H1: Vocative "O" / "Oh" S₂ ────────────────────────────────────────────
    print(f"\n── H1: Vocative marker S₂ ─────────────────────────────────────────────")
    print(f"  T1 marker occurrences: {len(t1_markers)}")

    if t1_markers:
        t1_by_word = defaultdict(list)
        for m in t1_markers:
            t1_by_word[norm(m["token"])].append(m["s2"])

        print(f"\n  S₂ by vocative word:")
        print(f"  {'Word':<10} {'n':>5} {'Avg S₂':>8} {'Std':>7}")
        print(f"  {'-'*10} {'-'*5} {'-'*8} {'-'*7}")
        for word, vals in sorted(t1_by_word.items(), key=lambda x: -mean(x[1])):
            print(f"  {word:<10} {len(vals):>5} {mean(vals):>8.3f} {stdev(vals):>7.3f}")

    # ── H3: Archaic 2nd-person vs. regular pronoun baseline ───────────────────
    print(f"\n── H3: Archaic pronoun S₂ vs. baseline ───────────────────────────────")
    print(f"  T2 archaic pronoun occurrences: {len(t2_markers)}")

    t2_s2 = [m["s2"] for m in t2_markers]
    you_s2 = [s for d in data for s in collect_all_you_tokens(d)]
    baseline_s2 = [s for d in data for s in collect_all_pronoun_s2(d)]

    if t2_by_word := defaultdict(list):
        for m in t2_markers:
            t2_by_word[norm(m["token"])].append(m["s2"])

    print(f"\n  S₂ by archaic pronoun:")
    print(f"  {'Word':<10} {'n':>5} {'Avg S₂':>8}")
    print(f"  {'-'*10} {'-'*5} {'-'*8}")
    for word, vals in sorted(t2_by_word.items(), key=lambda x: -mean(x[1])):
        print(f"  {word:<10} {len(vals):>5} {mean(vals):>8.3f}")

    print(f"\n  Comparison:")
    print(f"    Archaic (thou/thee/thy/thine): avg S₂ = {mean(t2_s2):.3f}  (n={len(t2_s2)})")
    print(f"    Modern 'you/your':             avg S₂ = {mean(you_s2):.3f}  (n={len(you_s2)})")
    print(f"    Baseline pronouns (I/he/she):  avg S₂ = {mean(baseline_s2):.3f}  (n={len(baseline_s2)})")
    print(f"    Archaic lift over modern 'you': {mean(t2_s2) - mean(you_s2):+.3f}")

    # ── H2: First token after vocative marker ─────────────────────────────────
    print(f"\n── H2: First token after vocative 'O' / 'Oh' ────────────────────────")
    t1_after = [(m["first_after_token"], m["first_after_s2"]) for m in t1_markers
                if m["first_after_token"] is not None]

    if t1_after:
        after_s2_vals = [s for _, s in t1_after]
        print(f"  Avg S₂ of token after vocative: {mean(after_s2_vals):.3f}  (n={len(after_s2_vals)})")

        # Highest-S₂ "O/Oh X" moments
        print(f"\n  Top 10 highest-S₂ post-vocative tokens:")
        sorted_after = sorted(t1_markers, key=lambda x: x["first_after_s2"], reverse=True)[:10]
        for m in sorted_after:
            if m["first_after_token"]:
                print(f"    '{m['token'].strip()}  {m['first_after_token'].strip()}'  "
                      f"S₂={m['first_after_s2']:.2f}  "
                      f"({m['poem_author']}: {m['poem_title']})")

    # ── H5: Taxonomy of the unsaid at apostrophe moments ──────────────────────
    print(f"\n── H5: What GPT-2 expected at T1 vocative positions ──────────────────")
    alt_categories = defaultdict(int)
    alt_examples = defaultdict(list)
    PUNCT = set(".,;:!?\"'—-–…")
    FUNC_WORDS = {"the", "a", "an", "of", "in", "to", "and", "that", "it", "for",
                  "is", "was", "be", "with", "as", "at", "by", "from", "not",
                  "but", "or", "so", "if", "my", "your", "his", "her", "their"}

    for m in t1_markers:
        alt = m["top_alt"]
        if alt is None:
            continue
        n_alt = norm(alt)
        if all(c in PUNCT for c in n_alt.strip()):
            cat = "punctuation"
        elif n_alt.strip() == "" or n_alt == "\n":
            cat = "newline"
        elif n_alt in FUNC_WORDS:
            cat = "function_word"
        elif n_alt.startswith(" "):
            cat = "content_word"
        else:
            cat = "other"
        alt_categories[cat] += 1
        if len(alt_examples[cat]) < 3:
            alt_examples[cat].append(
                f"'{m['token'].strip()}' (expected '{alt.strip()}') — {m['poem_author']}"
            )

    total_t1 = len(t1_markers)
    print(f"\n  GPT-2's top alternative at {total_t1} vocative positions:")
    for cat, cnt in sorted(alt_categories.items(), key=lambda x: -x[1]):
        pct = 100 * cnt / total_t1 if total_t1 else 0
        print(f"    {cat:<20}: {cnt:>3}  ({pct:.0f}%)")
        for ex in alt_examples[cat][:2]:
            print(f"      e.g. {ex}")

    # ── Poem-level apostrophe breakdown ───────────────────────────────────────
    print(f"\n── Apostrophic poems ranked by marker density ─────────────────────────")
    poem_stats = []
    for d in apo_poems:
        markers = collect_marker_windows(d)
        n_markers = len(markers)
        n_tokens = len(d["tokens"])
        density = n_markers / n_tokens if n_tokens else 0
        poem_avg_s2 = mean([t["s2"] for t in d["tokens"]])
        poem_stats.append({
            "title": d["metadata"]["title"],
            "author": d["metadata"]["author"],
            "n_markers": n_markers,
            "density": density,
            "avg_s2": poem_avg_s2,
        })

    poem_stats.sort(key=lambda x: -x["density"])
    print(f"\n  {'Title':<42} {'Author':<22} {'Markers':>8} {'Density':>8} {'Avg S₂':>7}")
    print(f"  {'-'*42} {'-'*22} {'-'*8} {'-'*8} {'-'*7}")
    for ps in poem_stats:
        print(f"  {ps['title'][:41]:<42} {ps['author'][:21]:<22} "
              f"{ps['n_markers']:>8} {ps['density']:>8.3f} {ps['avg_s2']:>7.3f}")

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")

    h1_result = "SUPPORTED" if t1_markers and mean([m["s2"] for m in t1_markers]) > 0 else "NOT SUPPORTED"
    h2_result = "SUPPORTED" if t1_after and mean([s for _, s in t1_after]) > mean(apo_all_s2) else "NOT SUPPORTED"
    h3_result = "SUPPORTED" if mean(t2_s2) > mean(you_s2) else "NOT SUPPORTED"
    h4_lift = mean(apo_all_s2) - mean(non_apo_all_s2)
    h4_result = "SUPPORTED" if h4_lift > 0 else "NOT SUPPORTED"

    print(f"\n  H1 (vocative 'O' is high-S₂): {h1_result}")
    if t1_markers:
        print(f"     avg S₂ of 'O'/'Oh': {mean([m['s2'] for m in t1_markers]):.3f}")
    print(f"\n  H2 (post-vocative token spikes): {h2_result}")
    if t1_after:
        print(f"     avg S₂ after 'O': {mean([s for _, s in t1_after]):.3f}  vs poem avg: {mean(apo_all_s2):.3f}")
    print(f"\n  H3 (thou/thee/thy > 'you'): {h3_result}")
    print(f"     archaic avg S₂: {mean(t2_s2):.3f}  vs  'you' avg: {mean(you_s2):.3f}")
    print(f"\n  H4 (apostrophic poems higher S₂): {h4_result}")
    print(f"     lift = {h4_lift:+.3f}")


if __name__ == "__main__":
    run()
