"""
Number Words and Quantifiers in Poetry: S2 Analysis
=====================================================
Do number words and quantifiers in poetry have distinctive S2 profiles?
Are specific numbers (three, seven) more surprising than vague ones (many, some)?
Does the choice of a specific cardinal number create a Straussian gap?

Hypothesis: Specific cardinal numbers should have higher S2 than vague quantifiers,
because GPT-2 cannot predict which specific number a poet will choose, while
vague quantifiers are more contextually predictable.

Also: "magical" numbers (three, seven, twelve, forty) in English poetic
tradition may show elevated S2 — poets reach for these for symbolic weight
in contexts where even a number word feels unexpected.
"""

import json
import re
from collections import defaultdict

# ── corpus ────────────────────────────────────────────────────────────────────
with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# ── word categories ───────────────────────────────────────────────────────────
# Cardinal numbers (word forms)
CARDINALS_SMALL = {
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen",
    "seventeen", "eighteen", "nineteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
}

# "Mythic" numbers with strong symbolic tradition in English literature
MYTHIC_NUMBERS = {"three", "seven", "twelve", "forty", "four", "nine", "ten",
                   "hundred", "thousand"}
PROSAIC_NUMBERS = {"two", "five", "six", "eight", "twenty", "thirty", "fifty",
                    "sixty", "seventy", "eighty", "ninety", "million"}

# Ordinals
ORDINALS = {
    "first", "second", "third", "fourth", "fifth", "sixth", "seventh",
    "eighth", "ninth", "tenth", "eleventh", "twelfth",
}

# Vague quantifiers
VAGUE_QUANT = {
    "all", "every", "each", "both", "many", "much", "more", "most",
    "few", "little", "some", "any", "several", "enough", "less", "fewer",
    "half", "once", "twice", "thrice",
}

# Exact zero/total
EXTREMAL = {"none", "nothing", "no", "never", "always", "everywhere", "nowhere"}


def classify_token(tok_lower: str) -> str | None:
    if tok_lower in MYTHIC_NUMBERS:
        return "mythic_number"
    if tok_lower in PROSAIC_NUMBERS:
        return "prosaic_number"
    if tok_lower in CARDINALS_SMALL:
        return "cardinal_other"
    if tok_lower in ORDINALS:
        return "ordinal"
    if tok_lower in VAGUE_QUANT:
        return "vague_quantifier"
    if tok_lower in EXTREMAL:
        return "extremal"
    return None


# ── collect token-level data ──────────────────────────────────────────────────
# Bucket → list of (s2, surprisal, entropy, token, context_before, era, top_alt)
bucket_data: dict[str, list] = defaultdict(list)
baseline_s2: list[float] = []

# Also per-token: for specific numbers, track which number has what S2
per_number: dict[str, list[float]] = defaultdict(list)

ARTIFACT_THRESHOLD = 0.9  # exclude stanza-break artifact positions

for entry in corpus:
    meta = entry.get("metadata", {})
    era = meta.get("era", "unknown")
    is_prose = era in ("control",)

    for tok in entry.get("tokens", []):
        p_newline = tok.get("p_newline", 0.0)
        if p_newline >= ARTIFACT_THRESHOLD:
            continue  # skip stanza-break artifact

        # Only word-start tokens (space prefix → new word)
        raw = tok.get("token", "")
        is_word_start = raw.startswith(" ")
        if not is_word_start:
            continue

        s2 = tok.get("s2", 0.0)
        surprisal = tok.get("surprisal", 0.0)
        entropy = tok.get("entropy", 0.0)
        ctx = tok.get("context_before", "")
        alts = tok.get("alternatives", [])
        top_alt = alts[0]["token"].strip() if alts else ""

        clean_tok = raw.strip().lower()
        cat = classify_token(clean_tok)

        if not is_prose:
            baseline_s2.append(s2)

        if cat is not None:
            record = (s2, surprisal, entropy, raw.strip(), ctx, era, top_alt, is_prose)
            bucket_data[cat].append(record)

            if cat in ("mythic_number", "prosaic_number", "cardinal_other"):
                per_number[clean_tok].append(s2)


# ── compute statistics ────────────────────────────────────────────────────────
def stats(vals: list[float]) -> dict:
    if not vals:
        return {"n": 0, "mean": None, "median": None, "pos_pct": None}
    n = len(vals)
    mean = sum(vals) / n
    svals = sorted(vals)
    med = svals[n // 2]
    pos = sum(1 for v in vals if v > 0) / n * 100
    return {"n": n, "mean": round(mean, 3), "median": round(med, 3), "pos_pct": round(pos, 1)}


baseline_stats = stats(baseline_s2)

results = {}
for cat, records in bucket_data.items():
    s2_vals = [r[0] for r in records if not r[7]]  # exclude prose
    s2_prose = [r[0] for r in records if r[7]]
    results[cat] = {
        "poetry": stats(s2_vals),
        "prose": stats(s2_prose),
        "sample": [(r[3], r[5], round(r[0], 2), r[6]) for r in records if not r[7]][:20],
    }

# Per-number stats (poetry only)
per_number_stats = {}
for word, vals in per_number.items():
    if len(vals) >= 3:
        per_number_stats[word] = stats(vals)

# Top high-S2 number moments
all_number_tokens = []
for cat in ("mythic_number", "prosaic_number", "cardinal_other"):
    for rec in bucket_data.get(cat, []):
        if not rec[7]:  # poetry only
            all_number_tokens.append(rec)

all_number_tokens.sort(key=lambda r: r[0], reverse=True)
top_moments = [(r[3], r[5], round(r[0], 2), r[2], r[6], r[6]) for r in all_number_tokens[:30]]

# Examples for vague quantifiers with high S2
vague_high = sorted(
    [r for r in bucket_data.get("vague_quantifier", []) if not r[7] and r[0] > 2.0],
    key=lambda r: r[0], reverse=True
)[:20]
vague_examples = [(r[3], r[5], round(r[0], 2), r[6]) for r in vague_high]


# ── Save ──────────────────────────────────────────────────────────────────────
output = {
    "baseline": baseline_stats,
    "by_category": results,
    "per_number": per_number_stats,
    "top_cardinal_moments": top_moments,
    "vague_high_s2_examples": vague_examples,
}

with open("results/number_words_s2.json", "w") as f:
    json.dump(output, f, indent=2)

print("Done. Results saved to results/number_words_s2.json")

# ── Print summary ─────────────────────────────────────────────────────────────
print(f"\n{'Category':<22} {'n':>6} {'Mean S₂':>8} {'Median S₂':>10} {'+S₂%':>6}")
print("-" * 60)
print(f"{'BASELINE (all poetry)':<22} {baseline_stats['n']:>6} {baseline_stats['mean']:>8.3f} {baseline_stats['median']:>10.3f} {baseline_stats['pos_pct']:>5.1f}%")

order = ["mythic_number", "prosaic_number", "cardinal_other", "ordinal",
         "vague_quantifier", "extremal"]
for cat in order:
    if cat not in results:
        continue
    p = results[cat]["poetry"]
    if p["n"] == 0:
        continue
    print(f"{cat:<22} {p['n']:>6} {p['mean']:>8.3f} {p['median']:>10.3f} {p['pos_pct']:>5.1f}%")

print("\n── Per-number stats (n ≥ 3, poetry) ──")
print(f"{'Number':<12} {'n':>5} {'Mean S₂':>8} {'Median':>8} {'+S₂%':>6}")
print("-" * 44)
per_sorted = sorted(per_number_stats.items(), key=lambda x: x[1]["mean"] or 0, reverse=True)
for word, st in per_sorted:
    print(f"{word:<12} {st['n']:>5} {st['mean']:>8.3f} {st['median']:>8.3f} {st['pos_pct']:>5.1f}%")

print("\n── Top high-S₂ cardinal moments ──")
top_sorted = sorted(all_number_tokens, key=lambda r: r[0], reverse=True)[:15]
for rec in top_sorted:
    tok, era, s2, entropy, top_alt = rec[3], rec[5], rec[0], rec[2], rec[6]
    ctx = rec[4][-30:].replace("\n", "↵") if rec[4] else ""
    print(f"  S₂={s2:+.2f}  '{tok}'  era={era}  ctx='…{ctx}'  top_alt='{top_alt}'")
