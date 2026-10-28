"""
Onomatopoeia and S2: Do Sound-Imitating Words Have a Distinct Information Signature?

Onomatopoeic words (buzz, hiss, crack, murmur) are supposedly "natural" language
because they sound like what they mean. But GPT-2 only knows text, not sound.
The question: at positions where a poet deploys onomatopoeia, is the choice
predictable or surprising? And what was GPT-2 expecting instead?

Hypothesis A (iconicity advantage): Onomatopoeic words fit their contexts well
because their phonetic texture makes them semantically resonant — even in text,
readers (and LLMs trained on text about sound) have absorbed these conventions.
Prediction: lower-than-average S2.

Hypothesis B (oddity of the specific): Onomatopoeic words are rare and often
concrete when the context could be abstract. The poet reaches for the precise
sensory word when convention would allow something vaguer.
Prediction: higher-than-average S2.
"""

import json
import re
from collections import defaultdict

# ─── Onomatopoeia Lexicon ──────────────────────────────────────────────────────

ONOMATOPOEIA = {
    # Core sound-imitating words
    "acoustic": [
        "buzz", "buzzing", "buzzed", "buzzes",
        "hiss", "hissing", "hissed", "hisses",
        "crack", "cracking", "crackle", "crackling", "crackled",
        "snap", "snapping", "snapped",
        "thud", "thudding", "thudded",
        "boom", "booming", "boomed",
        "bang", "banging", "banged",
        "crash", "crashing", "crashed",
        "splash", "splashing", "splashed",
        "drip", "dripping", "dripped", "drips",
        "murmur", "murmuring", "murmured", "murmurs",
        "rustle", "rustling", "rustled",
        "sizzle", "sizzling", "sizzled",
        "roar", "roaring", "roared",
        "growl", "growling", "growled",
        "chirp", "chirping", "chirped",
        "twitter", "twittering", "twittered",
        "howl", "howling", "howled",
        "screech", "screeching", "screeched",
        "shriek", "shrieking", "shrieked",
        "hum", "humming", "hummed",
        "purr", "purring", "purred",
        "clatter", "clattering", "clattered",
        "rattle", "rattling", "rattled",
        "jingle", "jingling", "jingled",
        "clang", "clanging", "clanged",
        "clunk", "clunking", "clunked",
        "thump", "thumping", "thumped",
        "swoosh", "whoosh",
        "zip", "zipping",
        "pop", "popping", "popped",
        "clink", "clinking", "clinked",
        "creak", "creaking", "creaked",
        "squeak", "squeaking", "squeaked",
        "groan", "groaning", "groaned",
        "moan", "moaning", "moaned",
        "sigh", "sighing", "sighed",
        "sob", "sobbing", "sobbed",
        "whirr", "whirring", "whir",
        "gurgle", "gurgling", "gurgled",
        "babble", "babbling", "babbled",
        "trickle", "trickling", "trickled",
        "ripple", "rippling", "rippled",
        "flutter", "fluttering", "fluttered",
        "whisper", "whispering", "whispered",
        "rumble", "rumbling", "rumbled",
        "thunder", "thundering", "thundered",
        "clap", "clapping", "clapped",
        "tap", "tapping", "tapped",
        "tick", "ticking", "ticked",
        "coo", "cooing", "cooed",
        "caw", "cawing", "cawed",
        "bark", "barking", "barked",
        "yelp", "yelping", "yelped",
        "screams", "scream", "screaming", "screamed",
        "wail", "wailing", "wailed",
        "whimper", "whimpering", "whimpered",
        "clatter", "splutter", "sputter",
        "fizz", "fizzing", "fizzed",
        "snarl", "snarling", "snarled",
    ],
}

# Flatten to a set for fast lookup (lowercase, strip leading space)
ONOMAT_SET = set()
for words in ONOMATOPOEIA.values():
    for w in words:
        ONOMAT_SET.add(w.lower())


def normalize(tok):
    """Strip leading/trailing whitespace and lowercase."""
    return tok.strip().lower()


def main():
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    onomat_tokens = []
    control_tokens = []  # all non-onomatopoeic, non-newline tokens
    onomat_by_word = defaultdict(list)

    total_poems = 0
    poems_with_hit = 0

    for poem in corpus:
        lang = poem["metadata"].get("language", "en")
        if lang != "en":
            continue
        total_poems += 1
        found_in_poem = False
        for tok in poem["tokens"]:
            if tok.get("p_newline", 0) > 0.9:
                continue  # skip stanza-break artifacts
            word = normalize(tok["token"])
            s2 = tok["s2"]
            surprisal = tok["surprisal"]
            entropy = tok["entropy"]
            rank = tok["rank"]
            alts = [a["token"].strip().lower() for a in tok.get("alternatives", [])]
            rec = {
                "token": tok["token"],
                "word": word,
                "s2": s2,
                "surprisal": surprisal,
                "entropy": entropy,
                "rank": rank,
                "alternatives": alts,
                "title": poem["metadata"]["title"],
                "author": poem["metadata"]["author"],
                "era": poem["metadata"]["era"],
            }
            if word in ONOMAT_SET:
                onomat_tokens.append(rec)
                onomat_by_word[word].append(rec)
                found_in_poem = True
            else:
                control_tokens.append(rec)
        if found_in_poem:
            poems_with_hit += 1

    print(f"Total English poems: {total_poems}")
    print(f"Poems with ≥1 onomatopoeic token: {poems_with_hit}")
    print(f"Total onomatopoeic tokens: {len(onomat_tokens)}")
    print(f"Total control tokens: {len(control_tokens)}")

    if not onomat_tokens:
        print("No onomatopoeic tokens found — check lexicon.")
        return {}

    # ─── Aggregate stats ─────────────────────────────────────────────────────

    def stats(lst, key):
        vals = [r[key] for r in lst]
        n = len(vals)
        if n == 0:
            return {"n": 0, "mean": None, "median": None}
        vals.sort()
        return {
            "n": n,
            "mean": round(sum(vals) / n, 4),
            "median": round(vals[n // 2], 4),
            "pct_positive": round(100 * sum(1 for v in vals if v > 0) / n, 1),
        }

    onomat_s2 = stats(onomat_tokens, "s2")
    control_s2 = stats(control_tokens, "s2")
    onomat_rank = stats(onomat_tokens, "rank")
    control_rank = stats(control_tokens, "rank")

    print(f"\n--- S₂ Comparison ---")
    print(f"Onomatopoeia:  mean={onomat_s2['mean']:.3f}  median={onomat_s2['median']:.3f}  +S2={onomat_s2['pct_positive']}%")
    print(f"Control:       mean={control_s2['mean']:.3f}  median={control_s2['median']:.3f}  +S2={control_s2['pct_positive']}%")
    print(f"\n--- Rank Comparison (lower=more expected) ---")
    print(f"Onomatopoeia:  mean rank={onomat_rank['mean']:.1f}  median rank={onomat_rank['median']:.1f}")
    print(f"Control:       mean rank={control_rank['mean']:.1f}  median rank={control_rank['median']:.1f}")

    # ─── Per-word breakdown ───────────────────────────────────────────────────

    print("\n--- Per-Word Breakdown (≥3 occurrences) ---")
    word_stats = []
    for word, recs in sorted(onomat_by_word.items()):
        if len(recs) < 3:
            continue
        s2_vals = [r["s2"] for r in recs]
        mean_s2 = sum(s2_vals) / len(s2_vals)
        rank_vals = [r["rank"] for r in recs]
        mean_rank = sum(rank_vals) / len(rank_vals)
        word_stats.append({
            "word": word,
            "n": len(recs),
            "mean_s2": round(mean_s2, 3),
            "mean_rank": round(mean_rank, 1),
        })

    word_stats.sort(key=lambda x: x["mean_s2"], reverse=True)
    print(f"{'Word':<18} {'N':>4} {'Mean S2':>9} {'Mean Rank':>11}")
    print("-" * 50)
    for ws in word_stats[:25]:
        print(f"{ws['word']:<18} {ws['n']:>4} {ws['mean_s2']:>9.3f} {ws['mean_rank']:>11.1f}")

    # ─── What was GPT-2 predicting instead? ──────────────────────────────────

    print("\n--- GPT-2's Top Alternatives at Onomatopoeic Positions ---")
    alt_counts = defaultdict(int)
    for rec in onomat_tokens:
        for alt in rec["alternatives"][:5]:  # top 5 predictions
            alt_counts[alt] += 1

    top_alts = sorted(alt_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    print("What GPT-2 expected instead of the onomatopoeic word:")
    for alt, cnt in top_alts:
        print(f"  '{alt}' — {cnt}x")

    # ─── Are onomatopoeia predicted by other onomatopoeia? ───────────────────
    print("\n--- Is Onomatopoeia Predicted by Onomatopoeia? ---")
    onomat_predicts_onomat = 0
    onomat_total = 0
    for rec in onomat_tokens:
        onomat_total += 1
        for alt in rec["alternatives"][:10]:
            if alt in ONOMAT_SET:
                onomat_predicts_onomat += 1
                break
    pct = 100 * onomat_predicts_onomat / onomat_total if onomat_total else 0
    print(f"Onomatopoeic positions where GPT-2 also predicted another onomatopoeic word: {pct:.1f}%")
    print(f"(i.e., GPT-2 had semantic awareness of the sound-word category at these positions)")

    # ─── Era breakdown ────────────────────────────────────────────────────────
    print("\n--- S₂ by Era (onomatopoeic tokens only) ---")
    era_data = defaultdict(list)
    for rec in onomat_tokens:
        era_data[rec["era"]].append(rec["s2"])

    era_stats = []
    for era, vals in era_data.items():
        if len(vals) >= 3:
            era_stats.append({
                "era": era,
                "n": len(vals),
                "mean_s2": round(sum(vals) / len(vals), 3),
            })
    era_stats.sort(key=lambda x: x["mean_s2"], reverse=True)
    print(f"{'Era':<22} {'N':>4} {'Mean S2':>9}")
    print("-" * 40)
    for es in era_stats:
        print(f"{es['era']:<22} {es['n']:>4} {es['mean_s2']:>9.3f}")

    # ─── High-surprise examples ───────────────────────────────────────────────
    print("\n--- Most Surprising Onomatopoeic Moments (S₂ ≥ 5) ---")
    high = [r for r in onomat_tokens if r["s2"] >= 5]
    high.sort(key=lambda x: x["s2"], reverse=True)
    for r in high[:15]:
        top_pred = r["alternatives"][0] if r["alternatives"] else "?"
        print(f"  '{r['token'].strip()}' (S₂={r['s2']:.2f}, rank={r['rank']}) vs '{top_pred}'"
              f" — {r['author']} ({r['era']})")

    # ─── Low-surprise examples (onomatopoeia that was expected) ──────────────
    print("\n--- Least Surprising Onomatopoeic Moments (S₂ ≤ 0) ---")
    low = [r for r in onomat_tokens if r["s2"] <= 0]
    low.sort(key=lambda x: x["s2"])
    for r in low[:10]:
        top_pred = r["alternatives"][0] if r["alternatives"] else "?"
        print(f"  '{r['token'].strip()}' (S₂={r['s2']:.2f}, rank={r['rank']}) vs '{top_pred}'"
              f" — {r['author']} ({r['era']})")

    # ─── Save results ─────────────────────────────────────────────────────────
    results = {
        "total_poems": total_poems,
        "poems_with_hit": poems_with_hit,
        "onomat_count": len(onomat_tokens),
        "control_count": len(control_tokens),
        "onomat_s2": onomat_s2,
        "control_s2": control_s2,
        "onomat_rank": onomat_rank,
        "control_rank": control_rank,
        "per_word": word_stats,
        "era_breakdown": era_stats,
        "top_alternatives": top_alts[:20],
        "onomat_predicts_onomat_pct": round(pct, 1),
        "high_s2_examples": [
            {"token": r["token"].strip(), "s2": r["s2"], "rank": r["rank"],
             "top_pred": r["alternatives"][0] if r["alternatives"] else "",
             "author": r["author"], "era": r["era"]}
            for r in high[:20]
        ],
        "low_s2_examples": [
            {"token": r["token"].strip(), "s2": r["s2"], "rank": r["rank"],
             "top_pred": r["alternatives"][0] if r["alternatives"] else "",
             "author": r["author"], "era": r["era"]}
            for r in low[:10]
        ],
    }

    with open("results/onomatopoeia_s2.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\n→ Results saved to results/onomatopoeia_s2.json")
    return results


if __name__ == "__main__":
    main()
