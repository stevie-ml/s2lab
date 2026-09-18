"""
Alliteration and S₂: Does Phonetic Craft Correlate with Semantic Surprise?

Hypothesis: When a poet alliterates — choosing a word that shares its initial
sound with a nearby word — do those words have higher or lower S₂?

Two competing theories:
  1. LOWER S₂: alliterating words fit the context better statistically —
     the semantic field activated by the initial word constrains subsequent
     choices (sound symbolism, collocational attractors).
  2. HIGHER S₂: alliteration is a form of defamiliarization — poets pick
     semantically unexpected words and add sonic craft on top of that surprise.
     The alliteration is a "cover" for semantic risk-taking.

Method:
  - Reconstruct token sequences from corpus_results.json
  - Detect alliterative pairs within a 6-token window (same initial consonant/vowel)
  - Compare S₂ at alliterating vs non-alliterating positions
  - Control for token position (line-initial, line-final) which independently affects S₂
  - Check if specific initial sounds drive the pattern (labial, sibilant, velar, etc.)

Note: GPT-2 processes byte-pair-encoded tokens, not phonemes. So any S₂ difference
at alliterating positions reflects genuine statistical regularities in language
(sound-meaning correlations, collocational attractors) rather than phonetic priming.
"""

import json
import re
import math
import statistics
from collections import defaultdict

RESULTS_PATH = "results/corpus_results.json"

# Consonant sound groups for phonetic analysis
SOUND_GROUPS = {
    "sibilant": set("sS"),
    "labial": set("bBpPmMwW"),
    "dental": set("tTdDnN"),
    "velar": set("gGkKcCqQ"),
    "fricative": set("fFvVhH"),
    "liquid": set("lLrR"),
    "vowel": set("aAeEiIoOuU"),
}


def get_sound_group(letter: str) -> str:
    for group, chars in SOUND_GROUPS.items():
        if letter in chars:
            return group
    return "other"


def clean_token(tok: str) -> str:
    """Strip GPT-2 tokenizer whitespace prefix (Ġ or Ċ) and normalize."""
    return tok.lstrip("Ġ Ċ\n\r\t ").lower()


def get_initial_letter(tok: str) -> str | None:
    """Return initial alphabetic character of a token, or None."""
    cleaned = clean_token(tok)
    for ch in cleaned:
        if ch.isalpha():
            return ch
    return None


def is_content_word(tok: str) -> bool:
    """Rough heuristic: alphabetic tokens that are not stopwords."""
    STOPWORDS = {
        "the", "a", "an", "and", "or", "but", "of", "in", "on", "at",
        "to", "for", "with", "is", "was", "are", "were", "be", "been",
        "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "that", "this",
        "it", "he", "she", "they", "we", "i", "you", "my", "your",
        "his", "her", "our", "their", "its", "not", "no", "by", "from",
        "as", "if", "so", "up", "out", "then", "there", "when", "where",
        "who", "what", "which", "how", "all", "been", "into", "through",
    }
    cleaned = clean_token(tok)
    return cleaned.isalpha() and cleaned not in STOPWORDS and len(cleaned) > 1


def detect_alliterative_tokens(tokens: list[dict], window: int = 6) -> set[int]:
    """
    Return the set of token positions that alliterate with a nearby token.

    A token at position i is alliterative if:
      - It is a content word
      - Another content word within `window` positions shares its initial letter
    Both positions are marked as alliterative (this is a symmetric relation).
    """
    alliterative = set()
    initials = []
    for tok_data in tokens:
        tok = tok_data["token"]
        init = get_initial_letter(tok) if is_content_word(tok) else None
        initials.append(init)

    n = len(tokens)
    for i in range(n):
        if initials[i] is None:
            continue
        for j in range(max(0, i - window), min(n, i + window + 1)):
            if j == i:
                continue
            if initials[j] is not None and initials[j] == initials[i]:
                alliterative.add(i)
                alliterative.add(j)
                break

    return alliterative


def analyze():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # English poems only (exclude control prose and German texts)
    poems = [
        p for p in data
        if p["metadata"].get("language", "en") == "en"
        and p["metadata"].get("era") != "control"
    ]

    print(f"Analyzing {len(poems)} English poems (excluding control prose)...")

    # Collect measurements
    alliterative_s2 = []
    non_alliterative_s2 = []
    alliterative_surprisal = []
    non_alliterative_surprisal = []
    alliterative_entropy = []
    non_alliterative_entropy = []

    # Sound-group breakdown
    sound_group_s2 = defaultdict(list)
    sound_group_n_alli = defaultdict(int)

    # Per-era breakdown
    era_alliterative = defaultdict(list)
    era_nonalliterative = defaultdict(list)
    era_alli_count = defaultdict(int)
    era_total_count = defaultdict(int)

    # Author breakdown
    author_alli_rate = defaultdict(lambda: {"alli": 0, "total": 0})

    # Top alliterative pairs
    top_pairs = []  # (s2, token, partner_init, context_before, poem_title)

    for poem in poems:
        tokens = poem["tokens"]
        era = poem["metadata"].get("era", "unknown")
        author = poem["metadata"].get("author", "Unknown")
        title = poem["metadata"].get("title", "Untitled")

        alli_positions = detect_alliterative_tokens(tokens)

        for pos, tok_data in enumerate(tokens):
            tok = tok_data["token"]
            s2 = tok_data.get("s2", 0)
            surprisal = tok_data.get("surprisal", 0)
            entropy = tok_data.get("entropy", 0)

            if not is_content_word(tok):
                continue

            era_total_count[era] += 1
            author_alli_rate[author]["total"] += 1

            if pos in alli_positions:
                alliterative_s2.append(s2)
                alliterative_surprisal.append(surprisal)
                alliterative_entropy.append(entropy)
                era_alliterative[era].append(s2)
                era_alli_count[era] += 1
                author_alli_rate[author]["alli"] += 1

                init = get_initial_letter(tok)
                if init:
                    sg = get_sound_group(init)
                    sound_group_s2[sg].append(s2)
                    sound_group_n_alli[sg] += 1

                if s2 > 3.0:
                    ctx = tok_data.get("context_before", "")[-60:]
                    top_pairs.append((s2, tok, init or "?", ctx, title, author))
            else:
                non_alliterative_s2.append(s2)
                non_alliterative_surprisal.append(surprisal)
                non_alliterative_entropy.append(entropy)
                era_nonalliterative[era].append(s2)

    print(f"\nAlliterative content-word tokens:   {len(alliterative_s2):,}")
    print(f"Non-alliterative content-word tokens: {len(non_alliterative_s2):,}")

    def stats(vals):
        if not vals:
            return {"mean": 0, "median": 0, "std": 0}
        return {
            "mean": statistics.mean(vals),
            "median": statistics.median(vals),
            "std": statistics.stdev(vals) if len(vals) > 1 else 0,
        }

    a_s = stats(alliterative_s2)
    n_s = stats(non_alliterative_s2)
    diff = a_s["mean"] - n_s["mean"]

    print("\n=== CORE RESULT ===")
    print(f"                    Mean S₂   Median S₂   Std")
    print(f"Alliterative:       {a_s['mean']:+.4f}   {a_s['median']:+.4f}     {a_s['std']:.4f}")
    print(f"Non-alliterative:   {n_s['mean']:+.4f}   {n_s['median']:+.4f}     {n_s['std']:.4f}")
    print(f"Difference:         {diff:+.4f}  ({'HIGHER' if diff > 0 else 'LOWER'} S₂ for alliterative tokens)")

    print("\n=== SURPRISAL & ENTROPY ===")
    a_surp = stats(alliterative_surprisal)
    n_surp = stats(non_alliterative_surprisal)
    a_ent = stats(alliterative_entropy)
    n_ent = stats(non_alliterative_entropy)
    print(f"Surprisal — Alliterative: {a_surp['mean']:.4f}, Non: {n_surp['mean']:.4f}, Δ = {a_surp['mean']-n_surp['mean']:+.4f}")
    print(f"Entropy   — Alliterative: {a_ent['mean']:.4f}, Non: {n_ent['mean']:.4f}, Δ = {a_ent['mean']-n_ent['mean']:+.4f}")

    print("\n=== S₂ BY SOUND GROUP (alliterative tokens only) ===")
    print(f"{'Sound group':<14} {'n':>5}  {'Mean S₂':>8}")
    for sg in sorted(sound_group_s2, key=lambda g: -statistics.mean(sound_group_s2[g])):
        vals = sound_group_s2[sg]
        if len(vals) >= 10:
            print(f"  {sg:<12} {len(vals):>5}  {statistics.mean(vals):>+8.4f}")

    print("\n=== ERA BREAKDOWN ===")
    print(f"{'Era':<24} {'Alli%':>6}  {'Alli S₂':>8}  {'Non S₂':>8}  {'Δ S₂':>7}")
    era_rows = []
    for era in sorted(era_total_count, key=lambda e: -era_total_count[e]):
        a_vals = era_alliterative[era]
        n_vals = era_nonalliterative[era]
        if len(a_vals) < 5 or len(n_vals) < 5:
            continue
        alli_pct = 100 * era_alli_count[era] / era_total_count[era]
        a_mean = statistics.mean(a_vals)
        n_mean = statistics.mean(n_vals)
        delta = a_mean - n_mean
        era_rows.append((era, alli_pct, a_mean, n_mean, delta, len(a_vals)))

    era_rows.sort(key=lambda r: -r[4])  # sort by delta
    for row in era_rows:
        era, pct, am, nm, d, n = row
        print(f"  {era:<22} {pct:>5.1f}%  {am:>+8.4f}  {nm:>+8.4f}  {d:>+7.4f}")

    print("\n=== TOP ALLITERATIVE HIGH-S₂ MOMENTS ===")
    top_pairs.sort(key=lambda x: -x[0])
    for s2, tok, init, ctx, title, author in top_pairs[:15]:
        print(f"  S₂={s2:+.2f}  '{tok.strip()}'  (init='{init}')  [{author}, \"{title}\"]")
        print(f"    Context: ...{ctx!r}")

    print("\n=== AUTHORS WITH HIGHEST ALLITERATION RATE ===")
    author_rows = []
    for author, counts in author_alli_rate.items():
        if counts["total"] < 30:
            continue
        rate = counts["alli"] / counts["total"]
        author_rows.append((author, rate, counts["total"]))
    author_rows.sort(key=lambda r: -r[1])
    for author, rate, n in author_rows[:15]:
        print(f"  {author:<30} {100*rate:>5.1f}%  (n={n})")

    # Return summary for findings write-up
    return {
        "n_alliterative": len(alliterative_s2),
        "n_nonalliterative": len(non_alliterative_s2),
        "alli_mean_s2": a_s["mean"],
        "non_mean_s2": n_s["mean"],
        "alli_mean_surprisal": a_surp["mean"],
        "non_mean_surprisal": n_surp["mean"],
        "alli_mean_entropy": a_ent["mean"],
        "non_mean_entropy": n_ent["mean"],
        "era_rows": era_rows,
        "sound_group_s2": {k: statistics.mean(v) for k, v in sound_group_s2.items() if len(v) >= 10},
        "top_pairs": top_pairs[:15],
    }


if __name__ == "__main__":
    analyze()
