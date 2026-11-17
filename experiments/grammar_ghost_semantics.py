"""
Grammar Ghost Semantics: When poets suppress expected grammar words,
what content words replace them, and what do those replacements reveal
about poetic strategy?

Builds on category_jump_analysis.md which found that GRAMMAR→CONTENT
jumps dominate (39.6%) genuine high-S2 moments.
"""

import json
import re
from collections import Counter, defaultdict

RESULTS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/grammar_ghost_semantics.json"
S2_THRESHOLD = 5.0

GRAMMAR_TOKENS = {
    # Articles
    "the", "a", "an", "The", "A", "An",
    # Prepositions
    "in", "on", "at", "by", "for", "with", "of", "to", "from",
    "into", "onto", "upon", "over", "under", "between", "through",
    "about", "around", "against", "In", "On", "At", "By", "For",
    "With", "Of", "To", "From", "Into", "Upon", "Over", "Under",
    # Conjunctions
    "and", "or", "but", "nor", "yet", "so", "because", "although",
    "while", "when", "if", "that", "which", "who", "whom",
    "And", "Or", "But", "Nor", "Yet", "So", "Because", "Although",
    "While", "When", "If", "That", "Which", "Who",
    # Auxiliaries/copula
    "is", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did",
    "will", "would", "shall", "should", "may", "might",
    "can", "could", "must",
    # Pronouns
    "I", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "myself", "himself", "herself", "itself",
    "this", "these", "those",
    # Other function words
    "not", "no", "as", "than", "also", "just", "only", "even",
    "still", "now", "then", "here", "there", "where",
    "Not", "No", "As", "Than", "Also", "Just", "Only", "Even",
    "Still", "Now", "Then", "Here", "There", "Where",
}

ARTICLE_TOKENS = {"the", "a", "an", "The", "A", "An"}
PREP_TOKENS = {
    "in", "on", "at", "by", "for", "with", "of", "to", "from",
    "into", "onto", "upon", "over", "under", "between", "through",
    "about", "around", "against", "In", "On", "At", "By", "For",
    "With", "Of", "To", "From", "Into", "Upon", "Over", "Under",
}
CONJ_TOKENS = {
    "and", "or", "but", "nor", "yet", "so", "because", "although",
    "while", "when", "if", "And", "Or", "But", "Nor", "Yet", "So",
    "Because", "Although", "While", "When", "If",
}
AUX_TOKENS = {
    "is", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did",
    "will", "would", "shall", "should", "may", "might", "can", "could", "must",
}
PRONOUN_TOKENS = {
    "I", "you", "he", "she", "it", "we", "they",
    "me", "him", "her", "us", "them",
    "my", "your", "his", "its", "our", "their",
    "myself", "himself", "herself", "itself",
    "this", "these", "those",
}
OTHER_FUNCTION = {
    "not", "no", "as", "than", "also", "just", "only", "even",
    "still", "now", "then", "here", "there", "where", "that", "which", "who",
    "Not", "No", "As", "Than", "Also", "Just", "Only", "Even",
    "Still", "Now", "Then", "Here", "There", "Where",
}

def categorize_grammar(token: str) -> str:
    t = token.strip()
    if t in ARTICLE_TOKENS:
        return "article"
    if t in PREP_TOKENS:
        return "preposition"
    if t in CONJ_TOKENS:
        return "conjunction"
    if t in AUX_TOKENS:
        return "auxiliary/copula"
    if t in PRONOUN_TOKENS:
        return "pronoun"
    if t in OTHER_FUNCTION:
        return "other_function"
    return "unknown"

def is_grammar(token: str) -> bool:
    return token.strip() in GRAMMAR_TOKENS

def is_content(token: str) -> bool:
    t = token.strip()
    if not t or not re.search(r'[a-zA-Z]', t):
        return False
    return not is_grammar(t) and not re.match(r'^[,.:;!?"\'\-\(\)\[\]]+$', t)

def is_punctuation(token: str) -> bool:
    t = token.strip()
    return bool(re.match(r'^[,.:;!?"\'\-\(\)\[\]…]+$', t))

# Word length heuristic for categorizing content word type
CONCRETE_NOUNS = {
    "stone", "moon", "sun", "sea", "tree", "sky", "earth", "water", "fire",
    "blood", "bone", "hand", "eye", "heart", "night", "day", "light",
    "shadow", "snow", "rain", "wind", "field", "road", "door", "wall",
    "leaf", "flower", "grass", "river", "mountain", "cloud", "star",
    "bird", "fish", "horse", "dog", "cat", "child", "mother", "father",
    "man", "woman", "god", "death", "life", "love", "dream", "time",
    "house", "room", "garden", "city", "forest", "lake", "wave", "tide",
}

ABSTRACT_NOUNS = {
    "truth", "beauty", "hope", "faith", "fear", "joy", "grief", "pain",
    "soul", "mind", "thought", "memory", "silence", "darkness", "glory",
    "grace", "peace", "war", "fate", "power", "freedom", "desire",
    "being", "nothing", "everything", "infinity", "eternity",
}

def classify_content_type(token: str) -> str:
    t = token.strip().lower()
    # Heuristic POS via morphology + word lists
    if t in CONCRETE_NOUNS:
        return "concrete_noun"
    if t in ABSTRACT_NOUNS:
        return "abstract_noun"
    if t.endswith(("ing", "ed", "s")) and len(t) > 4:
        return "verb/participle"
    if t.endswith(("ly",)):
        return "adverb"
    if t.endswith(("ful", "less", "ous", "ive", "al", "ic")):
        return "adjective"
    return "other_content"


def main():
    print("Loading corpus results...")
    with open(RESULTS_FILE) as f:
        data = json.load(f)

    # Pairs: (expected_grammar, actual_content, grammar_subcategory, content_type, era, s2)
    ghost_pairs = []

    # Count by grammar category and specific suppressed word
    grammar_suppressed_counts = Counter()
    grammar_category_counts = Counter()
    top_ghost_to_content = defaultdict(Counter)  # grammar_word -> Counter of replacements
    grammar_category_to_content_type = defaultdict(Counter)
    era_grammar_ghost_counts = defaultdict(lambda: {"total_tokens": 0, "grammar_ghost": 0})

    total_tokens = 0
    total_high_s2 = 0
    grammar_ghost_count = 0

    for poem in data:
        era = poem["metadata"].get("era", "unknown")
        tokens = poem.get("tokens", [])

        for tok in tokens:
            p_newline = tok.get("p_newline", 0)
            if p_newline >= 0.9:
                continue  # skip artifact tokens

            total_tokens += 1
            era_grammar_ghost_counts[era]["total_tokens"] += 1

            s2 = tok.get("s2", 0)
            if s2 < S2_THRESHOLD:
                continue

            total_high_s2 += 1

            actual = tok.get("token", "")
            alternatives = tok.get("alternatives", [])
            if not alternatives:
                continue

            top_alt = alternatives[0]["token"]

            # Check GRAMMAR→CONTENT
            if is_grammar(top_alt) and is_content(actual):
                grammar_ghost_count += 1

                grammar_cat = categorize_grammar(top_alt)
                content_type = classify_content_type(actual)

                ghost_pairs.append({
                    "era": era,
                    "s2": round(s2, 2),
                    "suppressed": top_alt.strip(),
                    "chosen": actual.strip(),
                    "grammar_category": grammar_cat,
                    "content_type": content_type,
                })

                grammar_suppressed_counts[top_alt.strip()] += 1
                grammar_category_counts[grammar_cat] += 1
                top_ghost_to_content[top_alt.strip()][actual.strip()] += 1
                grammar_category_to_content_type[grammar_cat][content_type] += 1
                era_grammar_ghost_counts[era]["grammar_ghost"] += 1

    # Build output
    top_suppressed = grammar_suppressed_counts.most_common(30)
    top_per_grammar = {
        gw: list(replacements.most_common(10))
        for gw, replacements in top_ghost_to_content.items()
        if grammar_suppressed_counts[gw] >= 5
    }

    # Era rates
    era_rates = []
    for era, counts in sorted(era_grammar_ghost_counts.items(),
                              key=lambda x: x[1]["total_tokens"], reverse=True):
        total = counts["total_tokens"]
        ghosts = counts["grammar_ghost"]
        era_rates.append({
            "era": era,
            "total_tokens": total,
            "grammar_ghost_count": ghosts,
            "rate_per_1000": round(ghosts / total * 1000, 2) if total > 0 else 0,
        })

    result = {
        "summary": {
            "total_tokens": total_tokens,
            "total_high_s2": total_high_s2,
            "grammar_ghost_count": grammar_ghost_count,
            "pct_of_high_s2": round(grammar_ghost_count / total_high_s2 * 100, 1) if total_high_s2 else 0,
        },
        "grammar_category_breakdown": dict(grammar_category_counts.most_common()),
        "top_suppressed_grammar_words": top_suppressed,
        "grammar_category_to_content_type": {
            cat: dict(counts.most_common())
            for cat, counts in grammar_category_to_content_type.items()
        },
        "top_replacement_content_by_grammar": top_per_grammar,
        "era_rates": era_rates,
        "sample_pairs": sorted(ghost_pairs, key=lambda x: -x["s2"])[:50],
    }

    with open(OUTPUT_FILE, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n=== Grammar Ghost Semantics ===")
    print(f"Total tokens (artifact-free): {total_tokens:,}")
    print(f"High-S2 tokens (s2 > {S2_THRESHOLD}): {total_high_s2:,}")
    print(f"Grammar ghost events: {grammar_ghost_count:,} "
          f"({grammar_ghost_count/total_high_s2*100:.1f}% of high-S2)")
    print(f"\nTop 15 suppressed grammar words:")
    for word, count in top_suppressed[:15]:
        pct = count / grammar_ghost_count * 100
        top_replacements = list(top_ghost_to_content[word].most_common(5))
        repl_str = ", ".join(f"'{r}'({c})" for r, c in top_replacements)
        print(f"  {word!r:12} {count:4}  ({pct:.1f}%)  → {repl_str}")

    print(f"\nBy grammar subcategory:")
    for cat, count in grammar_category_counts.most_common():
        pct = count / grammar_ghost_count * 100
        content_breakdown = grammar_category_to_content_type[cat].most_common(3)
        content_str = ", ".join(f"{t}:{c}" for t, c in content_breakdown)
        print(f"  {cat:20} {count:4} ({pct:.1f}%)  content types: {content_str}")

    print(f"\nTop 5 eras by grammar ghost rate (per 1000 tokens):")
    sorted_eras = sorted(era_rates, key=lambda x: -x["rate_per_1000"])
    for er in sorted_eras[:10]:
        if er["total_tokens"] >= 500:
            print(f"  {er['era']:25} {er['rate_per_1000']:6.2f}/1k  ({er['grammar_ghost_count']} ghosts)")

    print(f"\nResults saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
