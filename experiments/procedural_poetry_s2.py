"""
Procedural poetry S2 analysis: does imperative grammar create a sawtooth S2 pattern?

Hypothesis: In procedural/instructional poems:
  1. Imperative verbs (command the reader) have high S2 — the model is uncertain
     which specific action will be named.
  2. Object nouns immediately after those verbs have *lower* S2 — constrained by
     the verb that precedes them.
  3. This alternation creates a distinctive "sawtooth" S2 rhythm absent in lyric poetry.

Method:
  - Load corpus_results.json
  - Identify the new "procedural" era poems
  - For each procedural poem, classify tokens as: VERB (imperative), OBJECT (noun
    immediately after a bare verb), ADJ, or OTHER
  - Use simple surface heuristics (position in sentence, capitalization/lowercasing)
  - Compare S2 at VERB positions vs. OBJECT positions vs. lyric corpus baseline

Comparison groups:
  - Procedural poems (new era)
  - Lyric poems (romantic, victorian, modernist)
  - Prose poetry (for a prose-verb baseline)
"""

import json
import re
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH  = "results/procedural_poetry_s2.json"

# ── helpers ───────────────────────────────────────────────────────────────────

IMPERATIVE_SIGNALS = {
    "take", "unfold", "cut", "season", "stir", "pour", "let", "serve",
    "begin", "gather", "sort", "discard", "wash", "press", "label", "store",
    "refuse", "accept", "forget", "remember", "observe", "note", "record",
    "catalogue", "measure", "compare", "write", "cross", "mark", "prune",
    "drive", "believe", "grant", "open", "subtract", "erase", "exhale",
    "skip", "start", "stop", "count", "choose", "place", "fold", "lift",
    "carry", "set", "make", "find", "keep", "show", "see", "look",
    "read", "turn", "walk", "stand", "wait", "go", "come", "hold",
    "give", "bring", "try", "use", "put", "get", "say", "think",
    "know", "run", "leave", "call", "remain",
}

def clean_token(tok):
    """Strip GPT-2 Ġ prefix and lowercase."""
    return tok.lstrip("Ġ").lower().strip(".,!?;:'\"()")

def is_newline_token(tok):
    return tok.strip() == "" or tok in {"\n", "\r\n", "Ċ", "ĊĊ"}

def clean_tokens(tokens, threshold=0.9):
    """Return tokens with stanza-break artifacts removed (p_newline >= threshold)."""
    return [t for t in tokens if t.get("p_newline", 0) < threshold]

def classify_token(tok_str, prev_tok_str=None):
    """
    Classify a token as: imperative_verb | post_verb | other.
    'post_verb' = token immediately after an imperative verb (likely the object).
    """
    clean = clean_token(tok_str)
    if clean in IMPERATIVE_SIGNALS:
        return "imperative_verb"
    if prev_tok_str is not None:
        prev = clean_token(prev_tok_str)
        if prev in IMPERATIVE_SIGNALS:
            return "post_verb"
    return "other"


def load_results(path):
    with open(path) as f:
        return json.load(f)


def stats(values):
    if not values:
        return {"n": 0, "mean": None, "median": None, "std": None}
    return {
        "n": len(values),
        "mean": round(statistics.mean(values), 4),
        "median": round(statistics.median(values), 4),
        "std": round(statistics.stdev(values) if len(values) > 1 else 0.0, 4),
    }


# ── main analysis ─────────────────────────────────────────────────────────────

def main():
    all_results = load_results(RESULTS_PATH)
    print(f"Loaded {len(all_results)} poems.")

    # Groups
    procedural = [r for r in all_results if r["metadata"].get("era") == "procedural"]
    lyric_eras = {"romantic", "victorian", "modernist", "confessional", "19th_century"}
    lyric = [r for r in all_results if r["metadata"].get("era") in lyric_eras]
    prose_poetry = [r for r in all_results if r["metadata"].get("era") == "prose_poetry"]

    print(f"  Procedural poems: {len(procedural)}")
    print(f"  Lyric poems:      {len(lyric)}")
    print(f"  Prose poetry:     {len(prose_poetry)}")

    # ── Token-level classification for procedural poems ────────────────────────
    proc_verb_s2 = []
    proc_postverb_s2 = []
    proc_other_s2 = []
    proc_poem_details = []

    for poem in procedural:
        tokens = clean_tokens(poem.get("tokens", []))
        verb_s2 = []
        postverb_s2 = []
        other_s2 = []

        prev_clean = None
        for i, tok in enumerate(tokens):
            if is_newline_token(tok["token"]):
                prev_clean = None
                continue
            cat = classify_token(tok["token"], prev_clean)
            s2 = tok["s2"]
            if cat == "imperative_verb":
                verb_s2.append(s2)
            elif cat == "post_verb":
                postverb_s2.append(s2)
            else:
                other_s2.append(s2)
            prev_clean = tok["token"]

        proc_verb_s2.extend(verb_s2)
        proc_postverb_s2.extend(postverb_s2)
        proc_other_s2.extend(other_s2)

        proc_poem_details.append({
            "title": poem["metadata"]["title"],
            "author": poem["metadata"]["author"],
            "avg_s2": round(statistics.mean(t["s2"] for t in tokens) if tokens else 0, 4),
            "verb_s2": stats(verb_s2),
            "postverb_s2": stats(postverb_s2),
            "n_imperative_verbs": len(verb_s2),
        })

    # ── Lyric baseline ─────────────────────────────────────────────────────────
    lyric_verb_s2 = []
    lyric_postverb_s2 = []
    lyric_other_s2 = []

    for poem in lyric:
        tokens = clean_tokens(poem.get("tokens", []))
        prev_clean = None
        for tok in tokens:
            if is_newline_token(tok["token"]):
                prev_clean = None
                continue
            cat = classify_token(tok["token"], prev_clean)
            s2 = tok["s2"]
            if cat == "imperative_verb":
                lyric_verb_s2.append(s2)
            elif cat == "post_verb":
                lyric_postverb_s2.append(s2)
            else:
                lyric_other_s2.append(s2)
            prev_clean = tok["token"]

    # ── Prose poetry baseline ──────────────────────────────────────────────────
    prose_verb_s2 = []
    prose_postverb_s2 = []
    prose_other_s2 = []

    for poem in prose_poetry:
        tokens = clean_tokens(poem.get("tokens", []))
        prev_clean = None
        for tok in tokens:
            if is_newline_token(tok["token"]):
                prev_clean = None
                continue
            cat = classify_token(tok["token"], prev_clean)
            s2 = tok["s2"]
            if cat == "imperative_verb":
                prose_verb_s2.append(s2)
            elif cat == "post_verb":
                prose_postverb_s2.append(s2)
            else:
                prose_other_s2.append(s2)
            prev_clean = tok["token"]

    # ── S2 oscillation / sawtooth analysis ────────────────────────────────────
    # For each procedural poem, compute the S2 delta (verb → post-verb) per pair
    sawtooth_deltas = []
    for poem in procedural:
        tokens = clean_tokens(poem.get("tokens", []))
        prev_clean = None
        prev_s2 = None
        prev_cat = None
        for tok in tokens:
            if is_newline_token(tok["token"]):
                prev_clean = None
                prev_s2 = None
                prev_cat = None
                continue
            cat = classify_token(tok["token"], prev_clean)
            if cat == "post_verb" and prev_cat == "imperative_verb" and prev_s2 is not None:
                delta = tok["s2"] - prev_s2
                sawtooth_deltas.append(delta)
            prev_clean = tok["token"]
            prev_s2 = tok["s2"]
            prev_cat = cat

    # ── Compile output ─────────────────────────────────────────────────────────
    result = {
        "procedural": {
            "n_poems": len(procedural),
            "imperative_verb_s2": stats(proc_verb_s2),
            "post_verb_s2": stats(proc_postverb_s2),
            "other_s2": stats(proc_other_s2),
            "sawtooth_deltas": stats(sawtooth_deltas),
            "poem_details": proc_poem_details,
        },
        "lyric_baseline": {
            "n_poems": len(lyric),
            "imperative_verb_s2": stats(lyric_verb_s2),
            "post_verb_s2": stats(lyric_postverb_s2),
            "other_s2": stats(lyric_other_s2),
        },
        "prose_poetry_baseline": {
            "n_poems": len(prose_poetry),
            "imperative_verb_s2": stats(prose_verb_s2),
            "post_verb_s2": stats(prose_postverb_s2),
            "other_s2": stats(prose_other_s2),
        },
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    # ── Print summary ──────────────────────────────────────────────────────────
    print("\n=== PROCEDURAL POETRY S2 ANALYSIS ===\n")
    print("── Procedural poems ──")
    print(f"  Imperative verb positions: n={len(proc_verb_s2)}, mean S2={stats(proc_verb_s2)['mean']}")
    print(f"  Post-verb positions:       n={len(proc_postverb_s2)}, mean S2={stats(proc_postverb_s2)['mean']}")
    print(f"  Other positions:           n={len(proc_other_s2)}, mean S2={stats(proc_other_s2)['mean']}")
    print(f"  Sawtooth deltas (post-verb − verb): n={len(sawtooth_deltas)}, mean={stats(sawtooth_deltas)['mean']}")

    print("\n── Lyric baseline ──")
    print(f"  Imperative verb positions: n={len(lyric_verb_s2)}, mean S2={stats(lyric_verb_s2)['mean']}")
    print(f"  Post-verb positions:       n={len(lyric_postverb_s2)}, mean S2={stats(lyric_postverb_s2)['mean']}")
    print(f"  Other positions:           n={len(lyric_other_s2)}, mean S2={stats(lyric_other_s2)['mean']}")

    print("\n── Prose poetry baseline ──")
    print(f"  Imperative verb positions: n={len(prose_verb_s2)}, mean S2={stats(prose_verb_s2)['mean']}")
    print(f"  Post-verb positions:       n={len(prose_postverb_s2)}, mean S2={stats(prose_postverb_s2)['mean']}")
    print(f"  Other positions:           n={len(prose_other_s2)}, mean S2={stats(prose_other_s2)['mean']}")

    print("\n── Per-poem detail (procedural) ──")
    for pd in proc_poem_details:
        print(f"  {pd['title'][:50]}")
        print(f"    avg S2={pd['avg_s2']}, imperative verbs={pd['n_imperative_verbs']}")
        print(f"    verb mean={pd['verb_s2']['mean']}, post-verb mean={pd['postverb_s2']['mean']}")

    print(f"\nResults saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    import os
    os.chdir("/home/user/s2lab")
    main()
