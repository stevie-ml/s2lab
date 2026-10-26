"""
Alternative Semantic Taxonomy at Peak S₂ Moments

When a poet makes a maximally surprising choice (top S₂ tokens), what was
GPT-2 expecting instead? By classifying the 'alternatives' (the model's
top-10 predictions at those moments), we can build a taxonomy of the
*semantic domain of the unsaid* — what conventional language would have
provided vs. what the poet chose.

Hypothesis: At peak S₂ moments, the alternatives cluster into coherent
semantic domains (e.g., GPT-2 expected another body-part noun, or another
temporal marker, or another color). The poet's actual choice belongs to a
*different* semantic domain. This cross-domain switch is what produces the
"Straussian gap."

Method:
1. Collect top-N highest S₂ tokens per poem (filtered: p_newline < 0.9)
2. For each, classify actual token + alternatives into broad semantic
   categories using a keyword-based taxonomy
3. Measure "domain gap": do alternatives cluster in a different domain than
   the actual token?
4. Find cases of pure same-domain surprise (unusual word in expected domain)
   vs. cross-domain surprise (poet jumps to a different field entirely)
"""

import json
import os
from collections import defaultdict, Counter

RESULTS_PATH = os.path.join(os.path.dirname(__file__), "..", "results", "corpus_results.json")

# Broad semantic category taxonomy (keyword matching)
# Each category: (name, set of keywords/stems)
DOMAINS = {
    "body": {"body", "hand", "heart", "eye", "face", "head", "foot", "feet", "arm", "leg",
             "mouth", "lip", "ear", "nose", "skin", "bone", "blood", "breath", "chest",
             "finger", "hair", "neck", "throat", "back", "tongue", "soul", "flesh",
             "shoulder", "knee", "brow", "cheek", "spine"},
    "nature": {"tree", "leaf", "flower", "grass", "stone", "river", "sea", "sky", "cloud",
                "wind", "rain", "sun", "moon", "star", "field", "hill", "rock", "water",
                "earth", "ground", "mountain", "forest", "wood", "bird", "light", "fire",
                "wave", "shore", "garden", "branch", "root", "seed", "snow", "ice",
                "lake", "stream", "bird", "wing", "rose", "oak"},
    "temporal": {"time", "night", "day", "morning", "evening", "year", "hour", "moment",
                  "age", "dawn", "dusk", "noon", "century", "season", "spring", "summer",
                  "autumn", "fall", "winter", "past", "future", "now", "then", "when",
                  "forever", "never", "always", "once", "again", "still", "until",
                  "before", "after", "long", "old", "young"},
    "emotion": {"love", "fear", "grief", "joy", "pain", "sorrow", "hope", "desire",
                  "hate", "anger", "beauty", "shame", "pride", "wonder", "terror",
                  "peace", "rage", "dream", "longing", "despair", "bliss", "suffering",
                  "ecstasy", "anguish", "melancholy", "passion", "feeling"},
    "death_void": {"death", "dead", "die", "grave", "tomb", "ghost", "shadow", "dark",
                    "darkness", "void", "night", "nothing", "silence", "cold", "empty",
                    "gone", "lost", "end", "final", "last", "dust", "ash", "ruin",
                    "hollow", "pale", "dim", "fading"},
    "light_vision": {"light", "bright", "shine", "glow", "gleam", "flash", "fire",
                      "gold", "silver", "white", "black", "grey", "blue", "red", "green",
                      "color", "colour", "see", "look", "gaze", "sight", "vision", "eye",
                      "watch", "glimpse", "blind", "clear", "dark"},
    "motion": {"come", "go", "walk", "run", "rise", "fall", "fly", "move", "pass",
                "turn", "return", "leave", "enter", "flow", "drift", "wander", "follow",
                "lead", "reach", "carry", "bear", "bring", "draw", "push", "pull",
                "climb", "fall", "drop", "leap"},
    "speech_thought": {"say", "speak", "tell", "sing", "call", "cry", "know", "think",
                        "feel", "hear", "sound", "voice", "word", "name", "song", "poem",
                        "story", "speak", "silence", "whisper", "echo", "answer",
                        "question", "truth", "lie", "dream", "imagine", "remember"},
    "social_human": {"man", "woman", "child", "people", "god", "world", "life", "home",
                      "house", "father", "mother", "king", "lord", "friend", "enemy",
                      "nation", "country", "city", "land", "place", "way", "door",
                      "room", "street", "family", "heart"},
    "function_grammar": {"the", "a", "an", "of", "in", "to", "and", "or", "but", "not",
                           "is", "was", "are", "were", "be", "have", "had", "has", "will",
                           "would", "could", "should", "may", "might", "shall", "my", "your",
                           "his", "her", "our", "their", "this", "that", "which", "who",
                           "what", "when", "where", "how", "all", "no", "more", "so",
                           "as", "at", "by", "for", "from", "with", "on", "up", "out",
                           "if", "than", "into", "over", "after", "through"},
}


def classify_token(token_text: str) -> str:
    """Return the semantic domain of a token (case-insensitive, strip punctuation)."""
    word = token_text.strip().lower().strip("'\".,;:!?-—")
    # Try exact match first
    for domain, keywords in DOMAINS.items():
        if word in keywords:
            return domain
    # Try stem match (first 4+ chars)
    if len(word) >= 4:
        for domain, keywords in DOMAINS.items():
            for kw in keywords:
                if len(kw) >= 4 and word.startswith(kw[:4]):
                    return domain
    return "other"


def load_corpus():
    with open(RESULTS_PATH) as f:
        return json.load(f)


def run():
    data = load_corpus()
    print(f"Loaded {len(data)} texts")

    # Collect peak S2 moments (top 5 per poem, p_newline filtered)
    peak_moments = []
    for poem in data:
        meta_block = poem.get("metadata", {})
        tokens = poem.get("tokens") or poem.get("token_data") or []
        meta = {
            "title": meta_block.get("title", poem.get("title", "")),
            "author": meta_block.get("author", poem.get("author", "")),
            "era": meta_block.get("era", poem.get("era", "")),
        }
        clean_tokens = [t for t in tokens if t.get("p_newline", 0) < 0.9]
        if not clean_tokens:
            continue
        top5 = sorted(clean_tokens, key=lambda t: t["s2"], reverse=True)[:5]
        for tok in top5:
            if tok["s2"] < 2.0:  # Only genuinely high S2
                continue
            actual_domain = classify_token(tok["token"])
            alternatives = tok.get("alternatives", [])
            alt_domains = [classify_token(a["token"]) for a in alternatives]
            alt_domain_counts = Counter(alt_domains)
            dominant_alt_domain = alt_domain_counts.most_common(1)[0][0] if alt_domain_counts else "other"
            peak_moments.append({
                **meta,
                "token": tok["token"],
                "s2": tok["s2"],
                "actual_domain": actual_domain,
                "alt_domains": alt_domains,
                "dominant_alt_domain": dominant_alt_domain,
                "cross_domain": actual_domain != dominant_alt_domain and actual_domain != "other",
                "alternatives_top3": [a["token"] for a in alternatives[:3]],
                "context": tok.get("context_before", tok.get("context", "")),
            })

    print(f"Collected {len(peak_moments)} peak S₂ moments (S₂ > 2.0)\n")

    # === Analysis 1: What domains do alternatives cluster in? ===
    print("=== DOMAIN DISTRIBUTION OF ALTERNATIVES (what GPT-2 expected) ===")
    all_alt_domains = []
    for m in peak_moments:
        all_alt_domains.extend(m["alt_domains"])
    alt_domain_counts = Counter(all_alt_domains)
    total_alts = sum(alt_domain_counts.values())
    for domain, count in alt_domain_counts.most_common():
        pct = 100 * count / total_alts
        print(f"  {domain:<20} {count:>5} ({pct:.1f}%)")

    # === Analysis 2: What domains do the actual (surprising) tokens belong to? ===
    print("\n=== DOMAIN OF ACTUAL TOKENS (what poet chose) ===")
    actual_domains = Counter(m["actual_domain"] for m in peak_moments)
    total_actual = sum(actual_domains.values())
    for domain, count in actual_domains.most_common():
        pct = 100 * count / total_actual
        print(f"  {domain:<20} {count:>5} ({pct:.1f}%)")

    # === Analysis 3: Cross-domain surprises ===
    cross_domain = [m for m in peak_moments if m["cross_domain"]]
    same_domain = [m for m in peak_moments if not m["cross_domain"] and m["actual_domain"] != "other"]
    print(f"\n=== CROSS-DOMAIN vs. SAME-DOMAIN SURPRISES ===")
    print(f"  Cross-domain surprise (poet jumped to different field): {len(cross_domain)} ({100*len(cross_domain)/len(peak_moments):.1f}%)")
    print(f"  Same-domain surprise (unusual word in expected domain): {len(same_domain)} ({100*len(same_domain)/len(peak_moments):.1f}%)")

    # === Analysis 4: Most common domain transitions ===
    print("\n=== TOP DOMAIN TRANSITIONS (expected → actual) ===")
    transitions = Counter()
    for m in peak_moments:
        if m["dominant_alt_domain"] != "other" and m["actual_domain"] != "other":
            transitions[(m["dominant_alt_domain"], m["actual_domain"])] += 1
    for (from_d, to_d), count in transitions.most_common(15):
        arrow = f"{from_d} → {to_d}"
        print(f"  {arrow:<40} {count:>4}")

    # === Analysis 5: Most striking cross-domain examples ===
    print("\n=== TOP CROSS-DOMAIN PEAK MOMENTS (examples) ===")
    examples = sorted([m for m in cross_domain], key=lambda m: m["s2"], reverse=True)[:20]
    for m in examples:
        author = m["author"].split()[-1] if m["author"] else "?"
        alts = ", ".join(m["alternatives_top3"])
        print(f"  S₂={m['s2']:>6.2f} | '{m['token'].strip()}' ({m['actual_domain']}) | "
              f"expected: {m['dominant_alt_domain']} [{alts}] | {author}")

    # === Analysis 6: Per-era cross-domain rate ===
    print("\n=== CROSS-DOMAIN RATE BY ERA ===")
    era_stats = defaultdict(lambda: {"total": 0, "cross": 0, "avg_s2": 0.0})
    for m in peak_moments:
        era = m["era"] or "unknown"
        era_stats[era]["total"] += 1
        era_stats[era]["avg_s2"] += m["s2"]
        if m["cross_domain"]:
            era_stats[era]["cross"] += 1
    era_rows = []
    for era, stats in era_stats.items():
        if stats["total"] >= 3:
            rate = 100 * stats["cross"] / stats["total"]
            avg_s2 = stats["avg_s2"] / stats["total"]
            era_rows.append((era, stats["total"], rate, avg_s2))
    era_rows.sort(key=lambda r: r[2], reverse=True)
    print(f"  {'Era':<25} {'n':>5} {'Cross%':>8} {'Avg S₂':>8}")
    for era, n, rate, avg_s2 in era_rows:
        print(f"  {era:<25} {n:>5} {rate:>7.1f}% {avg_s2:>8.2f}")

    # === Analysis 7: Per-author cross-domain rate ===
    print("\n=== CROSS-DOMAIN RATE BY AUTHOR (top 15) ===")
    author_stats = defaultdict(lambda: {"total": 0, "cross": 0, "avg_s2": 0.0})
    for m in peak_moments:
        author = m["author"] or "unknown"
        author_stats[author]["total"] += 1
        author_stats[author]["avg_s2"] += m["s2"]
        if m["cross_domain"]:
            author_stats[author]["cross"] += 1
    author_rows = []
    for author, stats in author_stats.items():
        if stats["total"] >= 3:
            rate = 100 * stats["cross"] / stats["total"]
            avg_s2 = stats["avg_s2"] / stats["total"]
            author_rows.append((author, stats["total"], rate, avg_s2))
    author_rows.sort(key=lambda r: r[2], reverse=True)
    print(f"  {'Author':<30} {'n':>5} {'Cross%':>8} {'Avg S₂':>8}")
    for author, n, rate, avg_s2 in author_rows[:15]:
        print(f"  {author:<30} {n:>5} {rate:>7.1f}% {avg_s2:>8.2f}")

    return peak_moments


if __name__ == "__main__":
    run()
