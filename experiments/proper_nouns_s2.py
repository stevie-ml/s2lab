"""
Proper Nouns as Sites of the Straussian Gap

The existing syntactic_position.py experiment collapses NNP (proper noun)
and NN (common noun) into a single NOUN category.  This experiment separates
them to test the hypothesis:

  Proper nouns — names of people, places, mythological figures,
  and other specific entities — are a primary strategy by which poets
  achieve the Straussian gap (positive S₂).

Intuition: GPT-2 is trained on prose where proper nouns appear in
predictable NP positions.  In poetry, the *choice* of which proper noun
appears is far more constrained by sound, connotation, and tradition than
by statistical likelihood — so the model is surprised by the *specific*
name even when it expects *a* noun.

Method:
  1. Load corpus_results.json (cached token-level data).
  2. Reconstruct text + offsets per poem (same as syntactic_position.py).
  3. POS-tag with NLTK; isolate NNP/NNPS (proper) vs NN/NNS (common).
  4. Compute avg S₂, surprisal, entropy per category and compare.
  5. Identify top-S₂ proper nouns across the corpus and hand-classify them.
"""

import json
import sys
import os
from collections import defaultdict

import nltk
import nltk.pathsec

nltk.pathsec.ALLOW_PROXIED_FETCH = True

# ── Reuse offset/tagging helpers from syntactic_position ──────────────────────

def reconstruct_words_and_offsets(gpt2_tokens):
    chars = []
    offsets = []
    for tok in gpt2_tokens:
        text = tok["token"]
        start = len(chars)
        for ch in text:
            chars.append(ch)
        offsets.append((start, len(chars)))
    return "".join(chars), offsets


def pos_tag_text(text):
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)
    result = []
    cursor = 0
    for word, tag in tags:
        idx = text.lower().find(word.lower(), cursor)
        if idx == -1:
            result.append((word, tag, cursor, cursor + len(word)))
            continue
        result.append((word, tag, idx, idx + len(word)))
        cursor = idx + len(word)
    return result


def assign_fine_pos(gpt2_tokens, full_text, offsets):
    """Return fine-grained Penn Treebank tag per GPT-2 token."""
    word_tags = pos_tag_text(full_text)
    result = []
    for tok_start, tok_end in offsets:
        best = "OTHER"
        for _word, penn, w_start, w_end in word_tags:
            if tok_end > w_start and tok_start < w_end:
                best = penn
                break
        result.append(best)
    return result


# ── Main analysis ─────────────────────────────────────────────────────────────

PROPER_TAGS = {"NNP", "NNPS"}
COMMON_TAGS = {"NN", "NNS"}


def run():
    results_path = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")
    with open(results_path) as f:
        data = json.load(f)

    poetry = [d for d in data
              if d["metadata"].get("era") != "control"
              and d["metadata"].get("language", "en") == "en"]

    proper_s2 = []   # list of (s2, token_text, poem_title, author)
    common_s2 = []   # list of (s2, token_text, poem_title, author)

    # Per-poem stats for comparison
    poem_proper = defaultdict(list)  # era → list of s2
    poem_common = defaultdict(list)

    for entry in poetry:
        gpt2_toks = entry["tokens"]
        meta = entry["metadata"]
        title = meta.get("title", "?")
        author = meta.get("author", "?")
        era = meta.get("era", "?")

        full_text, offsets = reconstruct_words_and_offsets(gpt2_toks)
        penn_tags = assign_fine_pos(gpt2_toks, full_text, offsets)

        for tok, penn in zip(gpt2_toks, penn_tags):
            s2 = tok["s2"]
            tok_text = tok["token"].strip()
            if penn in PROPER_TAGS:
                proper_s2.append((s2, tok_text, title, author))
                poem_proper[era].append(s2)
            elif penn in COMMON_TAGS:
                common_s2.append((s2, tok_text, title, author))
                poem_common[era].append(s2)

    return {
        "proper": proper_s2,
        "common": common_s2,
        "proper_by_era": dict(poem_proper),
        "common_by_era": dict(poem_common),
    }


def avg(lst):
    return sum(lst) / len(lst) if lst else 0.0


def pos_ratio(lst):
    return sum(1 for v in lst if v > 0) / len(lst) if lst else 0.0


def print_report(results):
    proper = results["proper"]
    common = results["common"]

    proper_vals = [x[0] for x in proper]
    common_vals = [x[0] for x in common]

    print("\n=== PROPER NOUNS vs. COMMON NOUNS: S₂ COMPARISON ===\n")
    print(f"{'Category':<16} {'n':>6}  {'avg S₂':>8}  {'+S₂%':>7}  {'max S₂':>8}")
    print("-" * 52)
    print(f"{'Proper (NNP/NNPS)':<16} {len(proper_vals):>6}  {avg(proper_vals):>+8.3f}  "
          f"{pos_ratio(proper_vals)*100:>6.1f}%  {max(proper_vals):>8.2f}")
    print(f"{'Common (NN/NNS)':<16} {len(common_vals):>6}  {avg(common_vals):>+8.3f}  "
          f"{pos_ratio(common_vals)*100:>6.1f}%  {max(common_vals):>8.2f}")

    # Top proper nouns by S2
    print("\n=== TOP 30 HIGHEST-S₂ PROPER NOUNS ===\n")
    top_proper = sorted(proper, key=lambda x: -x[0])[:30]
    print(f"{'S₂':>7}  {'Token':<20}  {'Poem / Author'}")
    print("-" * 65)
    for s2, tok, title, author in top_proper:
        label = f"{title[:28]} / {author[:16]}"
        print(f"{s2:>+7.2f}  {tok:<20}  {label}")

    # Top common nouns by S2
    print("\n=== TOP 20 HIGHEST-S₂ COMMON NOUNS ===\n")
    top_common = sorted(common, key=lambda x: -x[0])[:20]
    print(f"{'S₂':>7}  {'Token':<20}  {'Poem / Author'}")
    print("-" * 65)
    for s2, tok, title, author in top_common:
        label = f"{title[:28]} / {author[:16]}"
        print(f"{s2:>+7.2f}  {tok:<20}  {label}")

    # Most frequent proper nouns (by occurrence at positive S2)
    print("\n=== MOST FREQUENT PROPER NOUNS WITH POSITIVE S₂ ===\n")
    from collections import Counter
    freq = Counter(tok.lower() for s2, tok, _, _ in proper if s2 > 0)
    print(f"{'Name':<20}  {'n (positive S₂)':>16}")
    print("-" * 38)
    for name, cnt in freq.most_common(20):
        print(f"{name:<20}  {cnt:>16}")

    # Compare proper vs common per era
    print("\n=== PROPER vs. COMMON NOUN S₂ BY ERA ===\n")
    proper_by_era = results["proper_by_era"]
    common_by_era = results["common_by_era"]
    all_eras = sorted(set(list(proper_by_era) + list(common_by_era)))

    print(f"{'Era':<22}  {'Prop n':>6}  {'Prop AvgS₂':>10}  {'Comm n':>6}  {'Comm AvgS₂':>10}  {'Δ':>7}")
    print("-" * 70)
    for era in all_eras:
        pv = proper_by_era.get(era, [])
        cv = common_by_era.get(era, [])
        if not pv or not cv:
            continue
        delta = avg(pv) - avg(cv)
        print(f"{era:<22}  {len(pv):>6}  {avg(pv):>+10.3f}  {len(cv):>6}  {avg(cv):>+10.3f}  {delta:>+7.3f}")


if __name__ == "__main__":
    results = run()
    print_report(results)
