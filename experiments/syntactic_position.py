"""
Syntactic Position vs S2
Investigates whether nouns, verbs, adjectives, and function words have
systematically different S2 values in poetry vs prose.

Method:
  1. Reconstruct word-level text from GPT-2 subword tokens.
  2. POS-tag words with NLTK's averaged perceptron tagger.
  3. Map each GPT-2 token back to its word and inherit that word's POS tag.
  4. Aggregate avg_s2 / avg_surprisal / avg_entropy by POS category.
  5. Compare poetry vs control prose.
"""

import json
import re
from collections import defaultdict

import nltk
import nltk.pathsec

# Allow proxy-based NLTK data access (CI/cloud environments).
nltk.pathsec.ALLOW_PROXIED_FETCH = True


# Penn Treebank → broad category mapping.
_PENN_TO_CAT = {
    # Nouns
    "NN": "NOUN", "NNS": "NOUN", "NNP": "NOUN", "NNPS": "NOUN",
    # Verbs (main)
    "VB": "VERB", "VBD": "VERB", "VBG": "VERB",
    "VBN": "VERB", "VBP": "VERB", "VBZ": "VERB",
    # Auxiliary / modal
    "MD": "AUX",
    # Adjectives
    "JJ": "ADJ", "JJR": "ADJ", "JJS": "ADJ",
    # Adverbs
    "RB": "ADV", "RBR": "ADV", "RBS": "ADV",
    # Determiners / articles
    "DT": "DET",
    # Prepositions / subordinating conjunctions
    "IN": "PREP",
    # Coordinating conjunctions
    "CC": "CONJ",
    # Pronouns
    "PRP": "PRON", "PRP$": "PRON", "WP": "PRON", "WP$": "PRON",
    # Punctuation / symbols / other
    ".": "PUNCT", ",": "PUNCT", ":": "PUNCT", "``": "PUNCT", "''": "PUNCT",
    "-LRB-": "PUNCT", "-RRB-": "PUNCT",
}


def broad_cat(penn_tag: str) -> str:
    """Map Penn Treebank tag to a broad category label."""
    return _PENN_TO_CAT.get(penn_tag, "OTHER")


def reconstruct_words_and_offsets(gpt2_tokens: list[dict]) -> tuple[str, list[tuple[int, int]]]:
    """
    Join GPT-2 subword tokens into a plain string and record the character
    span [start, end) of each token within that string.

    GPT-2 uses '▁' (U+2581) — represented as a leading space in the decoded
    token — to mark word boundaries.  Every token whose text starts with ' '
    begins a new word.
    """
    chars = []
    offsets = []  # (start_char, end_char) per token
    for tok in gpt2_tokens:
        text = tok["token"]
        start = len(chars)
        for ch in text:
            chars.append(ch)
        offsets.append((start, len(chars)))
    return "".join(chars), offsets


def pos_tag_text(text: str) -> list[tuple[str, str, int, int]]:
    """
    Tokenize `text` with NLTK word_tokenize and POS-tag it.
    Returns list of (word, penn_tag, start_char, end_char).

    We locate each NLTK token in `text` with a left-anchored search so we
    can map character offsets back to GPT-2 tokens.
    """
    tokens = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokens)

    result = []
    cursor = 0
    for word, tag in tags:
        # Find word in remaining text (case-insensitive search for robustness).
        idx = text.lower().find(word.lower(), cursor)
        if idx == -1:
            # Fallback: keep cursor unchanged, attribute unknown position.
            result.append((word, tag, cursor, cursor + len(word)))
            continue
        result.append((word, tag, idx, idx + len(word)))
        cursor = idx + len(word)
    return result


def assign_pos_to_tokens(gpt2_tokens: list[dict], full_text: str, token_offsets: list[tuple[int, int]]) -> list[str]:
    """
    For each GPT-2 token, find which NLTK word it overlaps with and return
    the corresponding broad POS category.  Tokens that don't overlap any
    word (e.g. pure whitespace) are tagged 'SPACE'.
    """
    word_tags = pos_tag_text(full_text)  # (word, penn, start, end)

    pos_per_token = []
    for tok_start, tok_end in token_offsets:
        best = "OTHER"
        for _word, penn, w_start, w_end in word_tags:
            # Overlap: token and word share at least one character.
            if tok_end > w_start and tok_start < w_end:
                best = broad_cat(penn)
                break
        pos_per_token.append(best)
    return pos_per_token


def run():
    with open("results/corpus_results.json") as f:
        data = json.load(f)

    # Separate poetry from control prose.
    poetry = [d for d in data if d["metadata"].get("era") != "control"
              and d["metadata"].get("language", "en") == "en"]
    prose = [d for d in data if d["metadata"].get("era") == "control"
             and d["metadata"].get("language", "en") == "en"]

    def accumulate(corpus_subset):
        """Collect per-POS stats across a set of texts."""
        cat_s2 = defaultdict(list)
        cat_surp = defaultdict(list)
        cat_ent = defaultdict(list)

        for entry in corpus_subset:
            gpt2_toks = entry["tokens"]
            full_text, offsets = reconstruct_words_and_offsets(gpt2_toks)
            pos_labels = assign_pos_to_tokens(gpt2_toks, full_text, offsets)

            for tok, pos in zip(gpt2_toks, pos_labels):
                cat_s2[pos].append(tok["s2"])
                cat_surp[pos].append(tok["surprisal"])
                cat_ent[pos].append(tok["entropy"])

        summary = {}
        for cat in sorted(cat_s2):
            vals_s2 = cat_s2[cat]
            vals_surp = cat_surp[cat]
            vals_ent = cat_ent[cat]
            n = len(vals_s2)
            summary[cat] = {
                "n": n,
                "avg_s2": round(sum(vals_s2) / n, 4),
                "avg_surprisal": round(sum(vals_surp) / n, 4),
                "avg_entropy": round(sum(vals_ent) / n, 4),
                "pos_s2_ratio": round(sum(1 for v in vals_s2 if v > 0) / n, 4),
            }
        return summary

    poetry_stats = accumulate(poetry)
    prose_stats = accumulate(prose)

    return {
        "poetry": poetry_stats,
        "prose": prose_stats,
        "n_poetry_texts": len(poetry),
        "n_prose_texts": len(prose),
    }


def print_report(results):
    poetry = results["poetry"]
    prose = results["prose"]

    CATS = ["NOUN", "VERB", "AUX", "ADJ", "ADV", "DET", "PREP", "CONJ", "PRON", "PUNCT", "OTHER"]
    present = [c for c in CATS if c in poetry or c in prose]

    print("=" * 80)
    print("SYNTACTIC POSITION vs S2: Poetry vs Prose")
    print(f"  Poetry: {results['n_poetry_texts']} texts   Prose: {results['n_prose_texts']} texts")
    print("=" * 80)

    hdr = f"{'POS':<8} {'Poetry n':>9} {'Poet AvgS2':>10} {'Poet Surp':>9} {'Poet Ent':>8} {'ProsAvgS2':>10} {'Pros Surp':>9} {'Delta S2':>9}"
    print(hdr)
    print("-" * 80)
    for cat in present:
        ps = poetry.get(cat, {})
        pr = prose.get(cat, {})
        n = ps.get("n", 0)
        p_s2 = ps.get("avg_s2", float("nan"))
        p_su = ps.get("avg_surprisal", float("nan"))
        p_en = ps.get("avg_entropy", float("nan"))
        r_s2 = pr.get("avg_s2", float("nan"))
        r_su = pr.get("avg_surprisal", float("nan"))
        delta = p_s2 - r_s2 if (p_s2 == p_s2 and r_s2 == r_s2) else float("nan")
        print(f"{cat:<8} {n:>9,} {p_s2:>+10.3f} {p_su:>9.3f} {p_en:>8.3f} {r_s2:>+10.3f} {r_su:>9.3f} {delta:>+9.3f}")

    print()
    print("  Delta S2 = Poetry avg_S2 − Prose avg_S2 (positive = poetry more surprising for that POS)")
    print()

    # Rank POS by Delta S2 (poetry minus prose)
    deltas = []
    for cat in present:
        ps = poetry.get(cat, {})
        pr = prose.get(cat, {})
        p_s2 = ps.get("avg_s2", None)
        r_s2 = pr.get("avg_s2", None)
        n = ps.get("n", 0)
        if p_s2 is not None and r_s2 is not None and n > 50:
            deltas.append((cat, p_s2 - r_s2, p_s2, r_s2, n))
    deltas.sort(key=lambda x: -x[1])

    print("POS categories ranked by poetry-vs-prose S2 gap (n > 50 tokens):")
    for cat, d, ps2, rs2, n in deltas:
        bar = "+" * int(abs(d) * 3) if d > 0 else "-" * int(abs(d) * 3)
        print(f"  {cat:<8}  Δ={d:+.3f}  ({bar})")

    return results


if __name__ == "__main__":
    results = run()
    print_report(results)
