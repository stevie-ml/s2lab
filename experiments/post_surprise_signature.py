"""
Post-surprise token signature: what immediately follows a high-S2 token?

aftermath_entropy.md measured the entropy CHANGE after a surprise.
This experiment measures what TOKEN TYPE actually appears after each
high-S2 moment. The goal: understand the mechanical structure of
"channeling" surprise — does surprise precede punctuation, function words,
or further content words?

No model re-run needed: uses existing corpus_results.json.
"""

import json
import re
from collections import defaultdict, Counter

RESULTS_PATH = "results/corpus_results.json"
OUTPUT_PATH = "results/post_surprise_signature.json"

# ---- token classifiers -------------------------------------------------------

PUNCTUATION_TOKENS = {
    ",", ".", "!", "?", ";", ":", "—", "–", "-", "...", "'", '"',
    "(", ")", "[", "]", "{", "}", "/", "\\", "'", '"', '"',
    "Ġ,", "Ġ.", "Ġ!", "Ġ?", "Ġ;", "Ġ:", "Ġ—", "Ġ–",
}

FUNCTION_WORDS = {
    # articles
    "the", "a", "an",
    # conjunctions
    "and", "or", "but", "nor", "for", "yet", "so", "both", "either", "neither",
    "although", "because", "since", "while", "if", "unless", "until", "when",
    "where", "as", "than", "that", "which", "who", "whom", "whose",
    # prepositions
    "in", "on", "at", "by", "for", "with", "about", "against", "between",
    "through", "during", "before", "after", "above", "below", "from", "up",
    "down", "out", "off", "over", "under", "into", "onto", "upon", "within",
    "without", "along", "across", "behind", "beyond", "near", "toward",
    "towards", "despite", "except", "per", "via", "among", "around",
    # pronouns
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
    "you", "your", "yours", "yourself", "yourselves",
    "he", "him", "his", "himself", "she", "her", "hers", "herself",
    "it", "its", "itself", "they", "them", "their", "theirs", "themselves",
    "this", "that", "these", "those", "what", "whatever", "which", "whichever",
    "who", "whoever", "whom", "whomever", "whose",
    # auxiliaries
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "will", "would", "shall", "should", "may", "might", "must", "can", "could",
    "ought", "need", "dare", "used",
    # other function words
    "not", "no", "nor", "also", "just", "even", "still", "already",
    "yet", "again", "too", "very", "quite", "rather", "much", "more",
    "most", "less", "least", "few", "many", "much", "all", "both",
    "each", "every", "any", "some", "such", "own", "same", "other",
    "than", "then", "there", "here",
}

NEWLINE_TOKENS = {"\n", "Ċ"}


def clean_token(tok: str) -> str:
    """Strip GPT-2 Ġ space prefix and lowercase."""
    return tok.lstrip("Ġ").lower()


def classify_token(tok: str) -> str:
    """Return one of: NEWLINE, PUNCTUATION, FUNCTION_WORD, CONTENT_WORD."""
    # check raw token for newline
    if tok in NEWLINE_TOKENS or tok.strip() == "" or "\n" in tok:
        return "NEWLINE"
    cleaned = clean_token(tok)
    if cleaned in PUNCTUATION_TOKENS or tok in PUNCTUATION_TOKENS:
        return "PUNCTUATION"
    if cleaned in FUNCTION_WORDS:
        return "FUNCTION_WORD"
    return "CONTENT_WORD"


def get_rank_bucket(s2: float) -> str:
    if s2 < 5.0:
        return "moderate (2–5)"
    elif s2 < 9.5:
        return "high (5–9.5)"
    else:
        return "extreme (≥9.5)"


def analyze():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Overall stats
    post_surprise_classes = defaultdict(int)
    baseline_classes = defaultdict(int)

    # By S2 bucket
    bucket_stats = defaultdict(lambda: defaultdict(int))

    # Top post-surprise tokens
    post_surprise_tokens = Counter()
    baseline_tokens = Counter()

    # Second token (t+2) after surprise
    post2_classes = defaultdict(int)

    # Consecutive high-S2 rate
    consecutive_surprise = 0
    total_surprise = 0

    # Era breakdown
    era_post_classes = defaultdict(lambda: defaultdict(int))

    for poem in corpus:
        tokens = poem.get("tokens", [])
        era = poem.get("metadata", {}).get("era", "unknown")
        n = len(tokens)

        for i, tok in enumerate(tokens):
            s2 = tok.get("s2", 0.0)
            p_nl = tok.get("p_newline", 1.0)
            is_high = s2 >= 2.0 and p_nl < 0.9

            if i + 1 < n:
                next_tok = tokens[i + 1]
                next_class = classify_token(next_tok["token"])

                if is_high:
                    post_surprise_classes[next_class] += 1
                    post_surprise_tokens[clean_token(next_tok["token"])] += 1
                    bucket = get_rank_bucket(s2)
                    bucket_stats[bucket][next_class] += 1
                    era_post_classes[era][next_class] += 1
                    total_surprise += 1

                    # check consecutive
                    next_s2 = next_tok.get("s2", 0.0)
                    next_p_nl = next_tok.get("p_newline", 1.0)
                    if next_s2 >= 2.0 and next_p_nl < 0.9:
                        consecutive_surprise += 1
                else:
                    baseline_classes[next_class] += 1
                    baseline_tokens[clean_token(next_tok["token"])] += 1

            if is_high and i + 2 < n:
                tok2 = tokens[i + 2]
                post2_classes[classify_token(tok2["token"])] += 1

    # Compute fractions
    def to_pct(d):
        total = sum(d.values())
        if total == 0:
            return {}
        return {k: round(100 * v / total, 1) for k, v in sorted(d.items(), key=lambda x: -x[1])}

    result = {
        "total_high_s2": total_surprise,
        "consecutive_surprise_rate": round(100 * consecutive_surprise / max(total_surprise, 1), 1),
        "post_surprise_distribution": to_pct(post_surprise_classes),
        "baseline_distribution": to_pct(baseline_classes),
        "post_surprise_top_tokens": dict(post_surprise_tokens.most_common(30)),
        "baseline_top_tokens": dict(baseline_tokens.most_common(30)),
        "by_s2_bucket": {
            bucket: to_pct(counts)
            for bucket, counts in bucket_stats.items()
        },
        "post2_distribution": to_pct(post2_classes),
        "by_era": {
            era: to_pct(counts)
            for era, counts in era_post_classes.items()
            if sum(counts.values()) >= 20
        },
        "raw_counts": {
            "post_surprise": dict(post_surprise_classes),
            "baseline": dict(baseline_classes),
        },
    }

    # Compute lifts
    lifts = {}
    total_ps = sum(post_surprise_classes.values())
    total_bl = sum(baseline_classes.values())
    for cls in set(post_surprise_classes) | set(baseline_classes):
        ps_rate = post_surprise_classes.get(cls, 0) / max(total_ps, 1)
        bl_rate = baseline_classes.get(cls, 0) / max(total_bl, 1)
        lift = ps_rate / bl_rate if bl_rate > 0 else float("inf")
        lifts[cls] = round(lift, 3)
    result["lifts"] = lifts

    with open(OUTPUT_PATH, "w") as f:
        json.dump(result, f, indent=2)

    print("Done. Written to", OUTPUT_PATH)
    print("\nPost-surprise distribution:", to_pct(post_surprise_classes))
    print("Baseline distribution:", to_pct(baseline_classes))
    print("\nLifts (surprise vs baseline):")
    for cls, lift in sorted(lifts.items(), key=lambda x: -x[1]):
        print(f"  {cls}: {lift:.3f}×")
    print("\nTop 15 post-surprise tokens:")
    for tok, count in post_surprise_tokens.most_common(15):
        pct = 100 * count / total_surprise
        print(f"  '{tok}': {count} ({pct:.1f}%)")
    print(f"\nConsecutive surprise rate: {result['consecutive_surprise_rate']}%")


if __name__ == "__main__":
    analyze()
