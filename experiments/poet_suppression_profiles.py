"""
Poet Suppression Profiles: What does each poet's 'negative vocabulary' look like?

Building on the Straussian Gap Taxonomy and Semantic Field of Surprise findings,
this experiment asks: at high-S2 moments, what does GPT-2 *expect* that each poet
systematically refuses to write? This creates a poet-specific 'suppression profile' —
the words each poet most often *does not* say when language expects them to.

We exclude the stanza-break artifact (positions where top alternative is '\n') to
focus on genuine lexical/semantic deviations, not line-break patterns.

Works purely from corpus_results.json — no GPU needed.
"""

import json
from collections import defaultdict, Counter

RESULT_PATH = "results/corpus_results.json"
S2_THRESHOLD = 1.5
MIN_POEMS = 2       # poet must have at least this many poems
MIN_MOMENTS = 8     # poet must have at least this many clean high-S2 moments


def clean_token(tok: str) -> str:
    return tok.strip().lower()


def is_stanza_break_artifact(alternatives: list) -> bool:
    if not alternatives:
        return False
    top_alt = alternatives[0]["token"]
    return top_alt.strip() == "" or top_alt == "\n"


def get_suppressed_token(alternatives: list) -> str | None:
    """Return the top-1 suppressed token (cleaned), skipping newlines."""
    for alt in alternatives:
        tok = alt["token"].strip()
        if tok and tok != "\n":
            return tok
    return None


def token_category(tok: str) -> str:
    t = tok.lower().strip()
    PUNCTUATION = {".", ",", "!", "?", ";", ":", "-", "–", "—", "(", ")", '"', "'", "...", "``", "''", "`"}
    FUNCTION_WORDS = {
        "the", "a", "an", "and", "or", "but", "of", "in", "on", "at", "to",
        "for", "with", "as", "by", "from", "that", "this", "these", "those",
        "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
        "do", "does", "did", "will", "would", "could", "should", "may", "might",
        "can", "shall", "must", "not", "no", "nor", "so", "yet", "both", "either",
        "it", "its", "their", "they", "them", "we", "us", "our", "my", "your",
        "his", "her", "who", "which", "what", "all", "each", "any", "some",
        "than", "then", "when", "where", "if", "though", "while", "about",
        "into", "through", "during", "before", "after", "above", "below", "up",
        "down", "out", "over", "under", "again", "also", "here", "there",
        "i", "he", "she", "you", "me", "him",
    }
    GENERIC_HUMAN = {"man", "men", "woman", "women", "people", "person", "human", "humans", "one"}
    if t in PUNCTUATION:
        return "punctuation"
    if t in GENERIC_HUMAN:
        return "generic_human"
    if t in FUNCTION_WORDS:
        return "function_word"
    if not t:
        return "other"
    if t[0].isupper() and len(t) > 1:
        return "proper_noun_or_caps"
    return "content_word"


def main():
    with open(RESULT_PATH) as f:
        data = json.load(f)

    # Gather per-poet data
    poet_moments: dict[str, list[dict]] = defaultdict(list)  # poet -> list of high-S2 moments
    poet_poems: dict[str, list[str]] = defaultdict(list)     # poet -> list of poem titles

    for item in data:
        meta = item.get("metadata", {})
        author = meta.get("author") or "Unknown"
        title = meta.get("title", "Untitled")
        lang = meta.get("language", "en")
        if lang != "en":
            continue  # focus on English

        poet_poems[author].append(title)
        tokens = item.get("tokens", [])

        for tok_data in tokens:
            s2 = tok_data.get("s2", 0)
            if s2 < S2_THRESHOLD:
                continue
            alts = tok_data.get("alternatives", [])
            if is_stanza_break_artifact(alts):
                continue

            suppressed = get_suppressed_token(alts)
            if suppressed is None:
                continue

            poet_moments[author].append({
                "token": tok_data["token"].strip(),
                "s2": s2,
                "suppressed": suppressed,
                "suppressed_cat": token_category(suppressed),
                "chosen_cat": token_category(tok_data["token"]),
                "title": title,
                "rank": tok_data.get("rank", 999),
            })

    # Filter to poets with enough data
    qualified_poets = {
        p: moments for p, moments in poet_moments.items()
        if len(poet_poems[p]) >= MIN_POEMS and len(moments) >= MIN_MOMENTS
    }

    print(f"Corpus: {len(data)} texts, {len(poet_moments)} poets")
    print(f"Qualified poets (≥{MIN_POEMS} poems, ≥{MIN_MOMENTS} clean high-S2 moments): {len(qualified_poets)}")
    print()

    # Build suppression profiles
    profiles = {}
    for poet, moments in sorted(qualified_poets.items()):
        n = len(moments)
        suppressed_counter = Counter(m["suppressed"] for m in moments)
        suppressed_cat_counter = Counter(m["suppressed_cat"] for m in moments)
        chosen_cat_counter = Counter(m["chosen_cat"] for m in moments)
        avg_s2 = sum(m["s2"] for m in moments) / n
        # How often does the poet eventually use the suppressed word?
        all_chosen = Counter(m["token"].lower() for m in moments)

        profiles[poet] = {
            "n_poems": len(poet_poems[poet]),
            "n_moments": n,
            "avg_s2": avg_s2,
            "top_suppressed": suppressed_counter.most_common(10),
            "suppressed_cat_dist": dict(suppressed_cat_counter),
            "chosen_cat_dist": dict(chosen_cat_counter),
        }

    # Print full report
    print("=" * 70)
    print("POET SUPPRESSION PROFILES — Top Suppressed Words per Poet")
    print("(High-S2 positions, stanza-break artifact removed)")
    print("=" * 70)
    print()

    # Sort by number of moments for richer profiles first
    for poet, prof in sorted(profiles.items(), key=lambda x: -x[1]["n_moments"]):
        n = prof["n_moments"]
        print(f"## {poet} ({prof['n_poems']} poems, {n} clean high-S2 moments, avg S₂={prof['avg_s2']:.2f})")
        print()
        print("  Most suppressed words (what GPT-2 expected):")
        for word, count in prof["top_suppressed"][:8]:
            pct = 100 * count / n
            cat = token_category(word)
            print(f"    '{word}' × {count} ({pct:.1f}%) [{cat}]")
        print()
        cat_d = prof["suppressed_cat_dist"]
        total = sum(cat_d.values())
        cat_str = ", ".join(
            f"{k}: {100*v/total:.0f}%"
            for k, v in sorted(cat_d.items(), key=lambda x: -x[1])
        )
        print(f"  Suppression category distribution: {cat_str}")
        chosen_d = prof["chosen_cat_dist"]
        total_c = sum(chosen_d.values())
        chosen_str = ", ".join(
            f"{k}: {100*v/total_c:.0f}%"
            for k, v in sorted(chosen_d.items(), key=lambda x: -x[1])
        )
        print(f"  What they chose instead: {chosen_str}")
        print()

    # Cross-poet comparison table
    print()
    print("=" * 70)
    print("CROSS-POET COMPARISON: Suppression Category Profiles")
    print("=" * 70)
    print()
    print(f"{'Poet':<28} {'n':>4} {'fn%':>5} {'punc%':>6} {'cw%':>5} {'gen.h%':>7} {'avgS2':>7}")
    print("-" * 65)
    for poet, prof in sorted(profiles.items(), key=lambda x: -x[1]["n_moments"]):
        n = prof["n_moments"]
        cat_d = prof["suppressed_cat_dist"]
        fn_pct = 100 * cat_d.get("function_word", 0) / n
        punc_pct = 100 * cat_d.get("punctuation", 0) / n
        cw_pct = 100 * cat_d.get("content_word", 0) / n
        gh_pct = 100 * cat_d.get("generic_human", 0) / n
        print(f"{poet:<28} {n:>4} {fn_pct:>5.1f} {punc_pct:>6.1f} {cw_pct:>5.1f} {gh_pct:>7.1f} {prof['avg_s2']:>7.2f}")

    # Global statistics
    print()
    print("=" * 70)
    print("GLOBAL SUPPRESSION STATISTICS (all qualified poets pooled)")
    print("=" * 70)
    all_suppressed = []
    for moments in qualified_poets.values():
        for m in moments:
            all_suppressed.append(m["suppressed"])
    global_counter = Counter(all_suppressed)
    print(f"\nTotal clean high-S2 moments: {len(all_suppressed)}")
    print("\nTop 20 most suppressed words (across all poets):")
    for word, count in global_counter.most_common(20):
        pct = 100 * count / len(all_suppressed)
        cat = token_category(word)
        print(f"  '{word}' × {count} ({pct:.1f}%) [{cat}]")

    # Generic human analysis
    print()
    print("=" * 70)
    print("THE 'MAN' PROBLEM: What did poets write when GPT-2 expected a generic human?")
    print("=" * 70)
    generic_human_moments = [
        m for moments in qualified_poets.values() for m in moments
        if m["suppressed_cat"] == "generic_human"
    ]
    if generic_human_moments:
        n_gh = len(generic_human_moments)
        print(f"\n{n_gh} moments where GPT-2 expected a generic human agent but poet deviated.")
        suppressed_gh = Counter(m["suppressed"] for m in generic_human_moments)
        print("\nMost common suppressed generic-human tokens:")
        for word, count in suppressed_gh.most_common(8):
            pct = 100 * count / n_gh
            print(f"  GPT-2 expected '{word}' × {count} ({pct:.1f}%)")
        print()
        chosen_gh = Counter(m["token"].lower() for m in generic_human_moments)
        print("Poets wrote instead:")
        for word, count in chosen_gh.most_common(15):
            pct = 100 * count / n_gh
            print(f"  '{word}' × {count} ({pct:.1f}%)")
        print()
        print("Sample moments:")
        shown = 0
        for m in sorted(generic_human_moments, key=lambda x: -x["s2"])[:8]:
            print(f"  [{m['title']}] GPT-2→'{m['suppressed']}', poet→'{m['token']}' (S₂={m['s2']:.2f})")
            shown += 1

    return profiles, global_counter, generic_human_moments


if __name__ == "__main__":
    profiles, global_counter, generic_human_moments = main()
