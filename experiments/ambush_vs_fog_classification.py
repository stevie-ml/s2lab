"""
Ambush vs. Fog Classification: Function Word vs. Content Word Suppression

Tests the hypothesis from alternatives_architecture.md:
  - AMBUSH: high-S2 moment where the suppressed top-1 prediction is a function word
    (poet broke a grammatical/structural expectation)
  - FOG: high-S2 moment where the suppressed top-1 prediction is a content word
    (poet exceeded a semantic expectation)

Builds on: alternatives_architecture.md, suppressed_lexicon.md
"""

import json
import re
from collections import defaultdict

# Canonical English function words (closed class)
FUNCTION_WORDS = {
    # Articles / determiners
    "the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her",
    "its", "our", "their", "all", "both", "each", "every", "few", "many", "much",
    "some", "any", "no", "such", "what", "which", "whose",
    # Prepositions
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "up", "about",
    "into", "through", "during", "before", "after", "above", "below", "between",
    "under", "along", "around", "against", "out", "off", "over", "within", "without",
    "across", "behind", "beyond", "despite", "down", "past", "since", "toward",
    "upon", "via", "throughout", "among", "beside", "except", "like", "near", "per",
    # Conjunctions
    "and", "but", "or", "nor", "for", "yet", "so", "although", "because", "since",
    "while", "whereas", "whether", "if", "unless", "until", "when", "where",
    "after", "before", "though", "as", "than",
    # Pronouns
    "i", "me", "my", "myself", "you", "your", "yourself", "he", "him", "himself",
    "she", "her", "herself", "it", "itself", "we", "us", "our", "ourselves",
    "they", "them", "their", "themselves", "who", "whom", "whose", "which",
    "that", "what", "whatever", "whoever", "whomever",
    # Auxiliary verbs
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "shall", "should", "may", "might",
    "must", "can", "could", "ought",
    # Adverbs (closed-class / high-frequency)
    "not", "very", "quite", "rather", "too", "also", "just", "even", "only",
    "still", "already", "never", "ever", "always", "often", "sometimes", "here",
    "there", "now", "then", "today", "yesterday", "tomorrow", "well", "so",
    "more", "most", "less", "least", "much", "more",
    # Other high-frequency function elements
    "no", "yes", "oh", "o", "ah",
}

PUNCT_TOKENS = set('.,!?;:\'"()-—–…\'"`')


def is_subword_token(tok: str) -> bool:
    """Return True if tok is a GPT-2 subword continuation (no leading space, not start-of-word)."""
    # GPT-2 marks word-initial tokens with a leading space (or Ġ internally).
    # A token without leading space that is alphabetic is a subword continuation.
    # Exceptions: single punctuation, digits, and tokens that are standalone symbols.
    if not tok:
        return False
    # If it starts with a space, it's a word-start token (not a subword)
    if tok[0] == " ":
        return False
    # Purely punctuation/digits are not subwords
    if all(not c.isalpha() for c in tok):
        return False
    # Otherwise, alphabetic token without leading space = subword continuation
    return True


def classify_token(tok: str) -> str:
    """Return 'function', 'punctuation', 'newline', 'subword', or 'content'."""
    stripped = tok.strip().lower()
    if stripped == "" or stripped == "\n" or stripped == "\\n":
        return "newline"
    if all(c in '.,!?;:\'"()-—–…\'"`' for c in stripped) or stripped in {",", ".", "!", "?", ";", ":", "'", '"'}:
        return "punctuation"
    if is_subword_token(tok):
        return "subword"
    # Strip leading spaces (GPT-2 tokens often have leading space)
    word = stripped.lstrip()
    if word in FUNCTION_WORDS:
        return "function"
    return "content"


def main():
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    S2_THRESHOLD = 2.0  # High-S2 threshold
    ARTIFACT_FILTER = 0.9  # Exclude stanza-break artifacts

    # Collect by poem
    results = []
    era_stats = defaultdict(lambda: {"ambush": 0, "fog": 0, "punct_suppressed": 0, "other": 0, "total": 0})
    poet_stats = defaultdict(lambda: {"ambush": 0, "fog": 0, "punct_suppressed": 0, "other": 0, "total": 0})

    # Detailed records for top examples
    ambush_examples = []
    fog_examples = []

    for poem in corpus:
        meta = poem["metadata"]
        title = meta["title"]
        author = meta["author"]
        era = meta["era"]
        lang = meta.get("language", "en")
        # Exclude non-English and control prose from primary analysis
        if lang != "en":
            continue

        poem_ambush = 0
        poem_fog = 0
        poem_other = 0
        poem_line_pos = []  # (within-line position, category, s2)

        line_pos = 0  # position within current line

        for tok in poem["tokens"]:
            # Artifact filter
            if tok.get("p_newline", 0) >= ARTIFACT_FILTER:
                line_pos = 0
                continue

            token_text = tok["token"]
            if token_text == "\n":
                line_pos = 0
                continue
            line_pos += 1

            s2 = tok["s2"]
            if s2 < S2_THRESHOLD:
                continue

            # Check alternatives
            if not tok.get("alternatives"):
                continue
            suppressed_top = tok["alternatives"][0]["token"]
            suppressed_prob = tok["alternatives"][0]["prob"]
            cat = classify_token(suppressed_top)

            record = {
                "title": title,
                "author": author,
                "era": era,
                "position": tok["position"],
                "line_pos": line_pos,
                "token": token_text,
                "s2": s2,
                "suppressed": suppressed_top,
                "suppressed_prob": suppressed_prob,
                "suppressed_cat": cat,
                "surprisal": tok["surprisal"],
                "entropy": tok["entropy"],
            }

            if cat == "function":
                poem_ambush += 1
                era_stats[era]["ambush"] += 1
                poet_stats[author]["ambush"] += 1
                ambush_examples.append(record)
            elif cat == "content":
                poem_fog += 1
                era_stats[era]["fog"] += 1
                poet_stats[author]["fog"] += 1
                fog_examples.append(record)
            elif cat in ("punctuation", "newline", "subword"):
                era_stats[era]["punct_suppressed"] += 1
                poet_stats[author]["punct_suppressed"] += 1
                poem_other += 1
            else:
                era_stats[era]["other"] += 1
                poet_stats[author]["other"] += 1
                poem_other += 1

            era_stats[era]["total"] += 1
            poet_stats[author]["total"] += 1

        total = poem_ambush + poem_fog + poem_other
        if total > 0:
            results.append({
                "title": title,
                "author": author,
                "era": era,
                "n_highS2": total,
                "ambush": poem_ambush,
                "fog": poem_fog,
                "other": poem_other,
                "ambush_ratio": poem_ambush / total,
                "fog_ratio": poem_fog / total,
                "avg_s2": poem["summary"]["avg_s2"],
            })

    # Top ambush examples (sort by S2 desc)
    ambush_examples.sort(key=lambda x: -x["s2"])
    fog_examples.sort(key=lambda x: -x["s2"])

    # Era table
    era_table = []
    for era, stats in era_stats.items():
        total = stats["total"]
        if total < 5:
            continue
        ambush_pct = 100 * stats["ambush"] / total
        fog_pct = 100 * stats["fog"] / total
        era_table.append({
            "era": era,
            "total": total,
            "ambush_pct": ambush_pct,
            "fog_pct": fog_pct,
            "ratio": ambush_pct / fog_pct if fog_pct > 0 else float("inf"),
        })
    era_table.sort(key=lambda x: -x["ambush_pct"])

    # Poet table (poets with >= 10 high-S2 events)
    poet_table = []
    for author, stats in poet_stats.items():
        total = stats["total"]
        if total < 10:
            continue
        ambush_pct = 100 * stats["ambush"] / total
        fog_pct = 100 * stats["fog"] / total
        poet_table.append({
            "author": author,
            "total": total,
            "ambush_pct": ambush_pct,
            "fog_pct": fog_pct,
            "ratio": ambush_pct / fog_pct if fog_pct > 0 else float("inf"),
        })
    poet_table.sort(key=lambda x: -x["ambush_pct"])

    # Overall summary
    total_all = sum(e["total"] for e in era_stats.values())
    total_ambush = sum(e["ambush"] for e in era_stats.values())
    total_fog = sum(e["fog"] for e in era_stats.values())
    total_punct = sum(e["punct_suppressed"] for e in era_stats.values())

    output = {
        "global": {
            "total_highS2": total_all,
            "ambush_n": total_ambush,
            "fog_n": total_fog,
            "punct_suppressed_n": total_punct,
            "ambush_pct": 100 * total_ambush / total_all if total_all else 0,
            "fog_pct": 100 * total_fog / total_all if total_all else 0,
            "punct_pct": 100 * total_punct / total_all if total_all else 0,
        },
        "era_table": era_table,
        "poet_table": poet_table[:30],
        "top_ambush_examples": ambush_examples[:25],
        "top_fog_examples": fog_examples[:25],
        "poem_results": sorted(results, key=lambda x: -x["ambush_ratio"])[:50],
    }

    with open("results/ambush_vs_fog_classification.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"Total high-S2 events analyzed: {total_all}")
    print(f"Ambush (function word suppressed): {total_ambush} ({100*total_ambush/total_all:.1f}%)")
    print(f"Fog (content word suppressed): {total_fog} ({100*total_fog/total_all:.1f}%)")
    print(f"Punctuation/newline suppressed: {total_punct} ({100*total_punct/total_all:.1f}%)")
    print(f"\nTop ambush eras: {[e['era'] for e in era_table[:5]]}")
    print(f"Top fog eras: {[e['era'] for e in sorted(era_table, key=lambda x: -x['fog_pct'])[:5]]}")
    print(f"\nTop ambush poets: {[p['author'] for p in poet_table[:5]]}")
    print(f"Top fog poets: {[p['author'] for p in sorted(poet_table, key=lambda x: -x['fog_pct'])[:5]]}")

    return output


if __name__ == "__main__":
    main()
