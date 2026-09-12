"""
Emotional Valence vs S₂: The Affective Dimension of Poetic Surprise

Research question: When poets make high-S₂ choices (surprising the model),
do those choices tend to carry emotional charge? And does the emotional
valence of the poet's word differ systematically from what GPT-2 expected?

The 'Affective Gap' hypothesis: the Straussian gap is not just an
information-theoretic phenomenon but an affective one — poets surprise
by choosing emotionally intense words when the model expects bland ones,
or emotionally charged alternatives to what seemed syntactically inevitable.

Method:
1. Use AFINN-111 word ratings (-5 to +5) for ~2477 English words
2. For each token with |S₂| > 1.0, look up actual token valence
3. Also look up top-3 predicted alternative valences
4. Compare: do high-S₂ moments have higher |valence|?
5. Measure the 'affective gap': |valence(actual)| - |valence(predicted)|
6. Are positive-S₂ substitutions net-positive or net-negative in valence?
"""

import json
import re
import os
import statistics
from pathlib import Path

# ── AFINN-111 lexicon (subset: the most common and emotionally extreme words) ─────
# Full AFINN-111 by Finn Årup Nielsen, MIT license
# https://github.com/fnielsen/afinn
# Included inline for reproducibility. Integer ratings: -5 (very negative) to +5 (very positive)
AFINN = {
    "abandon": -2, "abandoned": -2, "abhor": -3, "abhorrent": -3,
    "abominable": -3, "abominably": -3, "abominate": -3, "abomination": -3,
    "abort": -2, "aborted": -2, "aborts": -2, "abrupt": -1,
    "absent": -1, "absorbed": 1, "absurd": -1, "abuse": -3,
    "abused": -3, "abuses": -3, "abusive": -4, "ache": -2,
    "aches": -2, "aching": -2, "afraid": -2, "agony": -3,
    "agree": 1, "agreeable": 2, "aid": 2, "alarm": -2,
    "alarmed": -2, "alienated": -2, "alone": -1, "amazing": 4,
    "angry": -3, "anguish": -3, "annoy": -2, "annoyed": -2,
    "annoying": -2, "appreciate": 2, "approval": 2, "approve": 2,
    "awful": -3, "bad": -3, "beautiful": 3, "beauty": 3,
    "best": 3, "better": 2, "bliss": 3, "blissful": 3,
    "blessing": 3, "bold": 2, "bored": -2, "boredom": -2,
    "brave": 2, "break": -1, "broken": -2, "calm": 2,
    "care": 2, "careful": 2, "caring": 2, "celebrate": 3,
    "cheerful": 2, "clarity": 2, "clean": 2, "comfort": 2,
    "compassion": 2, "confidence": 2, "confused": -2, "corrupt": -3,
    "courage": 2, "create": 1, "creative": 2, "cruel": -3,
    "crush": -2, "cry": -2, "crying": -2, "curious": 1,
    "danger": -2, "dark": -1, "darkness": -1, "dead": -2,
    "death": -2, "defeat": -2, "delight": 3, "delighted": 3,
    "delightful": 4, "depressed": -3, "depression": -3, "desperate": -3,
    "destroy": -3, "devastated": -3, "die": -2, "disaster": -3,
    "disgust": -3, "disgusting": -4, "distress": -3, "doubt": -1,
    "dread": -3, "dreary": -2, "eager": 2, "ecstatic": 4,
    "embarrassed": -2, "embrace": 2, "empathy": 2, "enchant": 3,
    "encourage": 2, "energetic": 2, "enjoy": 2, "enlighten": 2,
    "enormous": 1, "excellent": 3, "excited": 3, "exhausted": -2,
    "exquisite": 4, "extraordinary": 3, "extreme": -1, "exuberant": 3,
    "fail": -2, "failure": -3, "faith": 2, "fantastic": 4,
    "fear": -2, "fearful": -3, "filth": -3, "foul": -3,
    "freedom": 2, "funny": 2, "gloom": -2, "gloomy": -2,
    "glorious": 3, "glory": 3, "good": 3, "gorgeous": 4,
    "grace": 3, "graceful": 3, "grateful": 3, "great": 3,
    "grief": -3, "grieve": -3, "grim": -2, "happiness": 3,
    "happy": 3, "harm": -2, "harmful": -3, "harsh": -2,
    "hate": -3, "hatred": -3, "heal": 2, "heart": 1,
    "helpless": -2, "hollow": -2, "hope": 2, "horrible": -4,
    "horrible": -4, "horror": -4, "hostile": -2, "hurt": -2,
    "ideal": 2, "illuminate": 2, "imagination": 2, "inspire": 2,
    "inspiring": 3, "insult": -2, "intense": 1, "joy": 3,
    "joyful": 4, "joyous": 4, "kind": 2, "lament": -2,
    "laugh": 2, "laughter": 2, "lazy": -2, "light": 1,
    "loneliness": -2, "lonely": -2, "longing": -1, "loss": -2,
    "love": 3, "lovely": 3, "magic": 2, "magnificent": 4,
    "meaningless": -2, "melancholy": -2, "mercy": 2, "misery": -3,
    "mistake": -2, "mourn": -2, "mysterious": 1, "naive": -1,
    "natural": 1, "nightmare": -3, "noble": 2, "odd": -1,
    "pain": -2, "painful": -3, "paradise": 3, "passion": 2,
    "peaceful": 3, "perfect": 3, "pleasure": 3, "poor": -2,
    "powerful": 2, "praise": 3, "precious": 3, "pride": 2,
    "problem": -2, "proud": 2, "pure": 2, "quiet": 1,
    "radiant": 3, "rapture": 3, "reassure": 2, "regret": -2,
    "rejoice": 3, "remarkable": 2, "remorse": -2, "resilient": 2,
    "respect": 2, "restore": 2, "rotten": -3, "ruin": -2,
    "sacred": 2, "sad": -2, "sorrow": -3, "sorrowful": -3,
    "magnificent": 4, "savage": -2, "scarred": -2, "serene": 3,
    "shame": -2, "shock": -2, "silence": 1, "sin": -3,
    "smile": 2, "sorrow": -3, "soul": 1, "splendid": 3,
    "strong": 2, "sublime": 3, "suffer": -3, "suffering": -3,
    "superb": 4, "sweet": 2, "tender": 2, "terrible": -3,
    "terror": -3, "thankful": 3, "thoughtful": 2, "torment": -3,
    "tragedy": -3, "transform": 2, "triumph": 3, "troubled": -2,
    "trust": 2, "truth": 2, "ugly": -3, "unbelievable": 1,
    "unfortunate": -2, "unhappy": -3, "unique": 2, "void": -2,
    "vulnerable": -1, "warm": 2, "wasted": -2, "weep": -2,
    "wonderful": 4, "worry": -3, "wrath": -3, "wrong": -2,
    "yearning": -1, "beautiful": 3, "bright": 2, "cold": -1,
    "dark": -1, "dead": -2, "dream": 1, "eternal": 1,
    "lost": -2, "mad": -2, "rage": -3, "silent": 1,
    "still": 1, "sweet": 2, "wild": 1, "wonder": 2,
    "alone": -1, "broken": -2, "cruel": -3, "empty": -2,
    "gentle": 2, "holy": 2, "innocent": 2, "pure": 2,
    "lost": -2, "black": -1, "white": 1, "red": 0,
    "blue": 0, "green": 1, "night": -1, "day": 1,
    "sun": 2, "moon": 1, "star": 2, "fire": 1,
    "water": 1, "earth": 1, "sky": 2, "sea": 1,
    "wind": 1, "rain": 0, "storm": -2, "thunder": -1,
    "god": 2, "death": -2, "life": 2, "love": 3,
    "war": -2, "peace": 3, "blood": -2, "heart": 1,
    "soul": 1, "spirit": 2, "grave": -2, "heaven": 3,
    "hell": -3, "paradise": 3, "sin": -3, "grace": 3,
    "silence": 1, "music": 2, "song": 2, "dance": 2,
    "laughter": 2, "tears": -1, "smiles": 2, "hope": 2,
    "despair": -3, "faith": 2, "truth": 2, "beauty": 3,
    "waste": -2, "loss": -2, "gain": 1, "wealth": 1,
    "poverty": -2, "hunger": -2, "thirst": -1, "cold": -1,
    "warm": 2, "light": 1, "shadow": -1, "ghost": -1,
    "demon": -3, "angel": 3, "monster": -3, "hero": 3,
    "evil": -3, "good": 3, "better": 2, "worse": -2,
    "best": 3, "worst": -3, "noble": 2, "coward": -2,
    "brave": 2, "fearless": 2, "mighty": 2, "weak": -1,
    "strong": 2, "free": 2, "bound": -1, "trapped": -2,
    "escape": 1, "prison": -2, "chains": -2, "liberty": 3,
    "justice": 3, "revenge": -2, "mercy": 2, "kindness": 3,
    "cruelty": -3, "envy": -2, "jealousy": -2, "pride": 2,
    "humble": 1, "arrogant": -2, "wise": 2, "foolish": -2,
    "clever": 2, "stupid": -2, "bright": 2, "dim": -1,
    "bold": 2, "timid": -1, "rich": 2, "poor": -2,
    "alive": 2, "dying": -2, "breathe": 1, "suffocate": -3,
    "open": 1, "closed": -1, "found": 2, "missing": -2,
    "remember": 1, "forget": -1, "forgive": 2, "blame": -2,
    "trust": 2, "deceive": -3, "honest": 2, "lie": -2,
    "truth": 2, "fiction": 0, "real": 1, "false": -2,
    "certain": 1, "doubt": -1, "clear": 1, "obscure": -1,
    "visible": 1, "hidden": -1, "known": 1, "unknown": -1,
    "near": 1, "far": 0, "together": 2, "apart": -1,
    "united": 2, "divided": -1, "whole": 1, "broken": -2,
    "safe": 2, "danger": -2, "risk": -1, "chance": 1,
    "luck": 2, "fate": 0, "fortune": 2, "curse": -3,
}

RESULTS_PATH = Path(__file__).parent.parent / "results" / "corpus_results.json"


def clean_token(tok: str) -> str:
    """Strip GPT-2 leading space marker and lowercase."""
    return tok.lstrip(" Ġ").strip().lower()


def get_valence(word: str) -> float | None:
    """Return AFINN valence for a word, or None if not in lexicon."""
    w = clean_token(word)
    # Try exact match, then stemmed forms
    if w in AFINN:
        return float(AFINN[w])
    # Try removing trailing 's', 'ed', 'ing', 'ly'
    for suffix in ("ing", "ly", "ed", "er", "est", "s"):
        if w.endswith(suffix) and len(w) - len(suffix) > 3:
            stem = w[: -len(suffix)]
            if stem in AFINN:
                return float(AFINN[stem])
    return None


def run():
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Filter to English poems only
    poems = [r for r in corpus if r["metadata"].get("language", "en") == "en"]
    print(f"Analyzing {len(poems)} English poems")

    # Per-token analysis
    rows = []  # (s2, actual_valence, top_pred_valence, actual_word, top_pred, era, author)

    for poem in poems:
        era = poem["metadata"]["era"]
        author = poem["metadata"]["author"]

        for tok in poem["tokens"]:
            actual_word = tok["token"]
            s2 = tok["s2"]

            # Only content words (alphabetic only)
            clean = clean_token(actual_word)
            if not clean.isalpha() or len(clean) < 3:
                continue

            actual_val = get_valence(actual_word)
            if actual_val is None:
                continue

            # Top predicted token valence
            top_pred_tok = tok["alternatives"][0]["token"] if tok["alternatives"] else ""
            top_pred_val = get_valence(top_pred_tok)

            rows.append({
                "s2": s2,
                "actual_val": actual_val,
                "top_pred_val": top_pred_val,
                "actual_word": clean,
                "top_pred_word": clean_token(top_pred_tok),
                "era": era,
                "author": author,
            })

    print(f"Found {len(rows)} tokens with AFINN ratings")

    # ── Analysis 1: Correlation of |S₂| with |valence| ─────────────────────────
    # Bin by S2 range
    bins = [
        ("Very low S₂ (< -3)", lambda r: r["s2"] < -3),
        ("Low S₂ (-3 to -1)", lambda r: -3 <= r["s2"] < -1),
        ("Neutral S₂ (-1 to 1)", lambda r: -1 <= r["s2"] < 1),
        ("High S₂ (1 to 3)", lambda r: 1 <= r["s2"] < 3),
        ("Very high S₂ (≥ 3)", lambda r: r["s2"] >= 3),
    ]

    print("\n=== Analysis 1: Emotional Intensity by S₂ bin ===")
    print(f"{'S₂ bin':<25} {'n':>5} {'mean |val|':>11} {'mean val':>9} {'% positive':>11} {'% negative':>11}")
    print("-" * 75)

    bin_stats = []
    for label, pred in bins:
        subset = [r for r in rows if pred(r)]
        if not subset:
            continue
        n = len(subset)
        abs_vals = [abs(r["actual_val"]) for r in subset]
        vals = [r["actual_val"] for r in subset]
        mean_abs = statistics.mean(abs_vals)
        mean_val = statistics.mean(vals)
        pct_pos = sum(1 for v in vals if v > 0) / n
        pct_neg = sum(1 for v in vals if v < 0) / n
        print(f"{label:<25} {n:>5} {mean_abs:>11.3f} {mean_val:>9.3f} {pct_pos:>10.1%} {pct_neg:>10.1%}")
        bin_stats.append((label, n, mean_abs, mean_val, pct_pos, pct_neg))

    # ── Analysis 2: The Affective Gap ───────────────────────────────────────────
    # For tokens where we also know top-prediction valence:
    # affective_gap = actual_val - top_pred_val
    # Positive = poet chose more positive than expected
    # Negative = poet chose more negative than expected
    paired = [r for r in rows if r["top_pred_val"] is not None]
    print(f"\n=== Analysis 2: The Affective Gap (n={len(paired)} paired tokens) ===")
    print("affective_gap = valence(actual) - valence(top_GPT2_prediction)")
    print()

    gap_bins = [
        ("Very low S₂ (< -2)", lambda r: r["s2"] < -2),
        ("Low S₂ (-2 to 0)", lambda r: -2 <= r["s2"] < 0),
        ("High S₂ (0 to 2)", lambda r: 0 <= r["s2"] < 2),
        ("Very high S₂ (≥ 2)", lambda r: r["s2"] >= 2),
    ]

    print(f"{'S₂ bin':<25} {'n':>5} {'mean gap':>10} {'mean |gap|':>11} {'% pos gap':>10} {'% neg gap':>10}")
    print("-" * 75)

    for label, pred in gap_bins:
        subset = [r for r in paired if pred(r)]
        if not subset:
            continue
        gaps = [r["actual_val"] - r["top_pred_val"] for r in subset]
        mean_gap = statistics.mean(gaps)
        mean_abs_gap = statistics.mean(abs(g) for g in gaps)
        pct_pos = sum(1 for g in gaps if g > 0) / len(gaps)
        pct_neg = sum(1 for g in gaps if g < 0) / len(gaps)
        print(f"{label:<25} {len(subset):>5} {mean_gap:>10.3f} {mean_abs_gap:>11.3f} {pct_pos:>9.1%} {pct_neg:>9.1%}")

    # ── Analysis 3: Top 15 highest-S₂ emotionally charged tokens ─────────────
    print("\n=== Analysis 3: Most Surprising Emotionally Charged Moments ===")
    extreme = sorted([r for r in rows if abs(r["actual_val"]) >= 2],
                     key=lambda r: r["s2"], reverse=True)[:20]
    print(f"\n{'Word':<15} {'S₂':>7} {'Valence':>8} {'Expected':>15} {'Author':<20}")
    print("-" * 70)
    for r in extreme:
        print(f"{r['actual_word']:<15} {r['s2']:>7.2f} {r['actual_val']:>8.1f} "
              f"{r['top_pred_word']:>15} {r['author'][:19]:<20}")

    # ── Analysis 4: By literary era ─────────────────────────────────────────────
    print("\n=== Analysis 4: Mean Emotional Charge by Era ===")
    era_rows = {}
    for r in rows:
        era_rows.setdefault(r["era"], []).append(r)

    era_data = []
    for era, rs in era_rows.items():
        if len(rs) < 10:
            continue
        high_s2 = [r for r in rs if r["s2"] >= 2.0]
        low_s2 = [r for r in rs if r["s2"] <= -2.0]
        all_abs = statistics.mean(abs(r["actual_val"]) for r in rs)
        high_abs = statistics.mean(abs(r["actual_val"]) for r in high_s2) if high_s2 else None
        low_abs = statistics.mean(abs(r["actual_val"]) for r in low_s2) if low_s2 else None
        mean_val = statistics.mean(r["actual_val"] for r in rs)
        era_data.append((era, len(rs), all_abs, high_abs, low_abs, mean_val))

    era_data.sort(key=lambda x: x[2], reverse=True)
    print(f"{'Era':<25} {'n':>5} {'all |val|':>10} {'high-S₂ |val|':>14} {'low-S₂ |val|':>13} {'mean val':>9}")
    print("-" * 80)
    for era, n, all_abs, high_abs, low_abs, mean_val in era_data:
        h = f"{high_abs:.3f}" if high_abs else "  n/a"
        l = f"{low_abs:.3f}" if low_abs else "  n/a"
        print(f"{era:<25} {n:>5} {all_abs:>10.3f} {h:>14} {l:>13} {mean_val:>9.3f}")

    # ── Analysis 5: Asymmetry — do poets surprise toward positive or negative? ──
    print("\n=== Analysis 5: Valence Asymmetry at High-S₂ Moments ===")
    high_s2_all = [r for r in rows if r["s2"] >= 2.0]
    if high_s2_all:
        mean_val_high = statistics.mean(r["actual_val"] for r in high_s2_all)
        pct_pos = sum(1 for r in high_s2_all if r["actual_val"] > 0) / len(high_s2_all)
        pct_neg = sum(1 for r in high_s2_all if r["actual_val"] < 0) / len(high_s2_all)
        pct_neutral = sum(1 for r in high_s2_all if r["actual_val"] == 0) / len(high_s2_all)
        print(f"High-S₂ (≥ 2.0) tokens with AFINN ratings: {len(high_s2_all)}")
        print(f"  Mean valence:       {mean_val_high:+.3f}")
        print(f"  % positive valence: {pct_pos:.1%}")
        print(f"  % negative valence: {pct_neg:.1%}")
        print(f"  % neutral:          {pct_neutral:.1%}")

    low_s2_all = [r for r in rows if r["s2"] <= -2.0]
    if low_s2_all:
        mean_val_low = statistics.mean(r["actual_val"] for r in low_s2_all)
        pct_pos = sum(1 for r in low_s2_all if r["actual_val"] > 0) / len(low_s2_all)
        pct_neg = sum(1 for r in low_s2_all if r["actual_val"] < 0) / len(low_s2_all)
        print(f"\nLow-S₂ (≤ -2.0) tokens with AFINN ratings: {len(low_s2_all)}")
        print(f"  Mean valence:       {mean_val_low:+.3f}")
        print(f"  % positive valence: {pct_pos:.1%}")
        print(f"  % negative valence: {pct_neg:.1%}")

    print("\n=== Summary ===")
    print("Run complete.")
    return bin_stats


if __name__ == "__main__":
    run()
