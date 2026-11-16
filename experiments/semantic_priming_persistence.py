"""
Semantic Priming Persistence Experiment
Date: 2026-11-16

Question: After a high-S2 token (a semantic surprise), does GPT-2's prediction
distribution for the NEXT position shift toward the semantic field of the
surprise token? In other words, does GPT-2 "incorporate" a poet's deviation
and prime subsequent predictions toward the new semantic territory, or does
it quickly revert to base-rate patterns?

Method:
- For each high-S2 token W_t (surprise), determine its semantic field F_t
- Look at the top-10 alternatives for the NEXT position (t+1)
- Measure what fraction of those alternatives belong to F_t
- Compare to baseline: same measure at non-surprise positions

If P(next alternatives in F_t | W_t is surprise) > P(next alternatives in F_t | baseline),
then GPT-2 is "primed" by surprises toward the surprise's semantic field.

This tests whether the model *integrates* poetic deviations into its forward predictions
or whether it essentially ignores them.
"""

import json
import re
import sys
from collections import defaultdict

# Semantic field vocabulary (token-level, lowercase, no leading space)
SEMANTIC_FIELDS = {
    "BODY": {
        "heart", "hand", "hands", "eye", "eyes", "head", "mouth", "blood",
        "breath", "face", "arm", "arms", "leg", "legs", "skin", "bone", "bones",
        "lips", "ear", "ears", "chest", "throat", "tongue", "finger", "fingers",
        "back", "foot", "feet", "body", "flesh", "hair", "brow", "neck", "knee",
        "knees", "palm", "palms", "shoulder", "shoulders"
    },
    "NATURE": {
        "tree", "trees", "water", "sky", "sun", "moon", "stone", "stones",
        "earth", "wind", "rain", "leaf", "leaves", "flower", "flowers", "bird",
        "birds", "grass", "cloud", "clouds", "sea", "river", "lake", "field",
        "fields", "rock", "rocks", "wave", "waves", "snow", "ice", "fire",
        "air", "land", "mountain", "forest", "wood", "woods", "sand", "soil",
        "dust", "star", "stars", "night", "dawn", "dusk", "spring", "summer",
        "winter", "autumn", "shadow", "shadows", "stream", "tide"
    },
    "TIME": {
        "now", "then", "before", "after", "long", "ago", "still", "day",
        "days", "night", "nights", "year", "years", "time", "morning", "evening",
        "once", "always", "never", "ever", "yet", "soon", "already", "century",
        "moment", "hour", "hours", "minute", "past", "future", "age", "ages",
        "eternal", "forever", "today", "yesterday", "tomorrow"
    },
    "MOTION": {
        "go", "went", "come", "came", "walk", "walked", "run", "ran", "fall",
        "fell", "fallen", "rise", "rose", "risen", "move", "moved", "turn",
        "turned", "fly", "flew", "flow", "flowed", "drift", "drifted",
        "follow", "followed", "pass", "passed", "return", "returned",
        "climb", "climbed", "descend", "descended", "break", "broke", "broken",
        "carry", "carried", "bring", "brought", "leave", "left", "reach",
        "reaching", "reaching", "reaching", "reaching"
    },
    "EMOTION": {
        "love", "loved", "grief", "fear", "joy", "hope", "pain", "sorrow",
        "anger", "desire", "longing", "wonder", "hate", "hatred", "loss",
        "loneliness", "lonely", "sad", "sadness", "happiness", "happy",
        "beautiful", "beauty", "glad", "weep", "wept", "cry", "cried",
        "laugh", "laughed", "mourn", "mourned", "regret", "proud", "pride",
        "shame", "shame", "dream", "dreamed", "dreamt", "sweet", "bitter",
        "tender", "gentle", "fierce", "wild", "broken"
    },
    "ABSTRACTION": {
        "truth", "death", "life", "god", "soul", "mind", "thought",
        "beauty", "silence", "power", "voice", "word", "words", "meaning",
        "nothing", "everything", "something", "world", "universe", "heaven",
        "hell", "fate", "doom", "grace", "sin", "light", "dark", "darkness",
        "spirit", "ghost", "dream", "dreams", "memory", "memories", "being",
        "existence", "faith", "hope", "love", "peace", "war", "time", "space",
        "void", "chaos", "order", "nature", "human", "divine", "eternal"
    },
    "COLOR": {
        "white", "black", "red", "blue", "green", "gold", "golden", "silver",
        "pale", "bright", "grey", "gray", "brown", "yellow", "orange", "purple",
        "violet", "crimson", "scarlet", "azure", "emerald", "amber", "ivory",
        "ebony", "obsidian", "ruby", "sapphire", "rose", "pink", "dark", "light"
    },
    "SOUND": {
        "voice", "cry", "cried", "sound", "music", "sing", "sang", "song",
        "songs", "noise", "whisper", "whispered", "silence", "thunder",
        "bell", "bells", "echo", "echoed", "shout", "shouted", "moan",
        "moaned", "hum", "hummed", "ring", "rang", "rung", "call", "called",
        "speak", "spoke", "spoken", "say", "said", "tell", "told", "hear",
        "heard", "listen", "listened", "tune", "tone", "note", "chord"
    }
}

# Build a reverse lookup: token -> field
TOKEN_TO_FIELD = {}
for field, tokens in SEMANTIC_FIELDS.items():
    for tok in tokens:
        # Note: a token could belong to multiple fields; take first match
        if tok not in TOKEN_TO_FIELD:
            TOKEN_TO_FIELD[tok] = field


def normalize_token(tok: str) -> str:
    """Strip GPT-2 Ġ prefix and lowercase."""
    return tok.strip().lstrip("Ġ").lstrip(" ").lower()


def get_field(token_str: str) -> str | None:
    norm = normalize_token(token_str)
    return TOKEN_TO_FIELD.get(norm)


def run_experiment(corpus_path: str):
    with open(corpus_path) as f:
        data = json.load(f)

    # Collect all tokens with their context
    # For each position t, we have:
    #   t.s2, t.p_newline -> to identify high-S2 non-artifact positions
    #   t.token -> the actual chosen token
    #   t+1.alternatives -> GPT-2's top-10 predictions for the next position

    # Stanza-break artifact filter: exclude positions where p_newline >= 0.9
    ARTIFACT_THRESHOLD = 0.9
    HIGH_S2_THRESHOLD = 2.0

    # We'll compute:
    # 1. For high-S2 moments where W_t has a known field F_t:
    #    - fraction of t+1 alternatives in F_t  ("primed" measure)
    # 2. Baseline: same measure at all other clean positions

    primed_field_fractions = defaultdict(list)   # field -> list of fractions at high-S2
    baseline_field_fractions = defaultdict(list)  # field -> list of fractions at baseline

    # Also track: does the ACTUAL next token belong to same field? (not just alternatives)
    primed_actual_match = defaultdict(list)    # field -> [0/1]
    baseline_actual_match = defaultdict(list)  # field -> [0/1]

    # Track priming by era
    era_primed = defaultdict(list)
    era_baseline = defaultdict(list)

    # Track general stats
    total_high_s2 = 0
    high_s2_with_field = 0
    total_baseline = 0
    baseline_with_field = 0

    for poem in data:
        tokens = poem.get("tokens", [])
        era = poem.get("metadata", {}).get("era", "unknown")

        for i in range(len(tokens) - 1):
            t = tokens[i]
            t_next = tokens[i + 1]

            p_nl = t.get("p_newline", 0.0)
            s2 = t.get("s2", 0.0)

            # Skip stanza-break artifacts
            if p_nl >= ARTIFACT_THRESHOLD:
                continue

            # Determine field of current token
            field_t = get_field(t.get("token", ""))

            # Get alternatives at position t+1
            alts = t_next.get("alternatives", [])
            if not alts:
                continue

            # Measure fraction of t+1 alternatives in field_t (if field_t is known)
            if field_t:
                field_alts = sum(
                    1 for a in alts
                    if get_field(a.get("token", "")) == field_t
                )
                frac = field_alts / len(alts)

                # Check if the actual t+1 token is in same field
                actual_next_field = get_field(t_next.get("token", ""))
                actual_match = 1 if (actual_next_field == field_t) else 0

            # Classify as high-S2 or baseline
            is_high_s2 = (s2 >= HIGH_S2_THRESHOLD)

            if is_high_s2:
                total_high_s2 += 1
                if field_t:
                    high_s2_with_field += 1
                    primed_field_fractions[field_t].append(frac)
                    primed_actual_match[field_t].append(actual_match)
                    era_primed[era].append(frac)
            else:
                total_baseline += 1
                if field_t:
                    baseline_with_field += 1
                    baseline_field_fractions[field_t].append(frac)
                    baseline_actual_match[field_t].append(actual_match)
                    era_baseline[era].append(frac)

    # Compute summary statistics
    results = {
        "summary": {
            "total_high_s2_positions": total_high_s2,
            "high_s2_with_known_field": high_s2_with_field,
            "total_baseline_positions": total_baseline,
            "baseline_with_known_field": baseline_with_field
        },
        "field_priming": {},
        "era_priming": {},
        "overall": {}
    }

    # Per-field stats
    all_fields = set(list(primed_field_fractions.keys()) + list(baseline_field_fractions.keys()))
    for field in sorted(all_fields):
        p_fracs = primed_field_fractions.get(field, [])
        b_fracs = baseline_field_fractions.get(field, [])
        p_actual = primed_actual_match.get(field, [])
        b_actual = baseline_actual_match.get(field, [])

        results["field_priming"][field] = {
            "primed_n": len(p_fracs),
            "primed_alt_frac": sum(p_fracs) / len(p_fracs) if p_fracs else 0,
            "baseline_n": len(b_fracs),
            "baseline_alt_frac": sum(b_fracs) / len(b_fracs) if b_fracs else 0,
            "delta_alt_frac": (
                (sum(p_fracs) / len(p_fracs)) - (sum(b_fracs) / len(b_fracs))
                if p_fracs and b_fracs else None
            ),
            "primed_actual_match_rate": sum(p_actual) / len(p_actual) if p_actual else 0,
            "baseline_actual_match_rate": sum(b_actual) / len(b_actual) if b_actual else 0,
        }

    # Overall priming signal
    all_primed = [f for fracs in primed_field_fractions.values() for f in fracs]
    all_baseline = [f for fracs in baseline_field_fractions.values() for f in fracs]
    results["overall"] = {
        "mean_primed_alt_frac": sum(all_primed) / len(all_primed) if all_primed else 0,
        "mean_baseline_alt_frac": sum(all_baseline) / len(all_baseline) if all_baseline else 0,
        "overall_delta": (
            (sum(all_primed) / len(all_primed)) - (sum(all_baseline) / len(all_baseline))
            if all_primed and all_baseline else None
        ),
    }

    # Per-era priming
    for era in sorted(era_primed.keys()):
        p = era_primed[era]
        b = era_baseline.get(era, [])
        results["era_priming"][era] = {
            "primed_n": len(p),
            "primed_mean": sum(p) / len(p) if p else 0,
            "baseline_n": len(b),
            "baseline_mean": sum(b) / len(b) if b else 0,
            "delta": (
                (sum(p) / len(p)) - (sum(b) / len(b))
                if p and b else None
            )
        }

    return results


if __name__ == "__main__":
    corpus_path = "results/corpus_results.json"
    print("Running semantic priming persistence experiment...", flush=True)
    results = run_experiment(corpus_path)

    out_path = "results/semantic_priming_persistence.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"Results written to {out_path}")

    # Print summary to stdout
    print("\n--- Overall Summary ---")
    print(f"High-S2 positions: {results['summary']['total_high_s2_positions']}")
    print(f"High-S2 with known field: {results['summary']['high_s2_with_known_field']}")
    print(f"Baseline positions: {results['summary']['total_baseline_positions']}")
    print(f"\nOverall priming effect:")
    ov = results["overall"]
    print(f"  Mean alt-fraction in same field (high-S2):   {ov['mean_primed_alt_frac']:.4f}")
    print(f"  Mean alt-fraction in same field (baseline):  {ov['mean_baseline_alt_frac']:.4f}")
    print(f"  Delta (primed - baseline):                   {ov['overall_delta']:+.4f}")
    print("\n--- Per-Field Results ---")
    print(f"{'Field':<15} {'Prime N':>8} {'Prime%':>8} {'Base N':>8} {'Base%':>8} {'Delta':>8}")
    for field, stats in sorted(results["field_priming"].items()):
        delta = stats["delta_alt_frac"]
        delta_str = f"{delta:+.4f}" if delta is not None else "N/A"
        print(f"{field:<15} {stats['primed_n']:>8} {stats['primed_alt_frac']:>8.4f} "
              f"{stats['baseline_n']:>8} {stats['baseline_alt_frac']:>8.4f} {delta_str:>8}")
