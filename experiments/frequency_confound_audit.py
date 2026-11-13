"""
The Frequency Confound Audit: How much of S2 is just word rarity?

Motivation
----------
`findings/polysemy_s2.md` (2026-11-13) found that polysemy correlates *inversely*
with S2 -- and traced the cause to a confound: polysemous words are overwhelmingly
high-frequency words that GPT-2 always expects. The apparent "polysemy effect" was
largely a frequency effect wearing a costume.

That raises a question for the whole lab. S2 = surprisal - entropy, and surprisal is
driven hard by how rare a word is. If much of the S2 signal is unigram word rarity,
then any finding of the form "linguistic feature X has elevated S2" may be reporting
nothing more than "feature X co-occurs with rarer words."

This experiment builds a frequency baseline from an EXTERNAL reference (wordfreq's
Zipf scale, derived from a broad multi-source English corpus, independent of this
project's poetry corpus), measures how much of S2 it explains, then re-tests the
lab's headline findings against frequency-residualised S2.

Method notes
------------
* Only COMPLETE WORDS are analysed. GPT-2 uses BPE, so many tokens are subword
  fragments ("ain" inside "mountain"). Scoring a fragment against a word-frequency
  table is meaningless. A token qualifies only if it is word-initial (leading space)
  and is not continued by an alphabetic token.
* This filter also drops newline tokens, so the known stanza-break artifact
  (findings/stanza_break_artifact.md) cannot contaminate these numbers.
* Only English-language texts are analysed. The corpus holds 8 German poems, and
  scoring German words against an English frequency table would misread them as
  ultra-rare English, manufacturing exactly the confound this audit is measuring.
* Residualisation is non-parametric: S2_resid = S2 - mean(S2 | Zipf bin), using
  0.25-wide Zipf bins fit on the pooled analysed set. It removes the average
  frequency effect without assuming linearity.
"""

import json
import math
import re
import statistics
from collections import defaultdict

from wordfreq import zipf_frequency

RESULTS_FILE = "results/corpus_results.json"
OUTPUT_FILE = "results/frequency_confound_audit.json"

BIN_WIDTH = 0.25
SPIKE_THRESHOLD = 3.0

FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "at", "by", "for", "with",
    "about", "into", "through", "during", "to", "from", "up", "down", "in", "out",
    "on", "off", "over", "under", "again", "then", "once", "here", "there", "when",
    "where", "why", "how", "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "no", "nor", "not", "only", "own", "same", "so",
    "than", "too", "very", "s", "t", "can", "will", "just", "should", "now",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
    "yours", "he", "him", "his", "she", "her", "hers", "it", "its", "they", "them",
    "their", "theirs", "what", "which", "who", "whom", "this", "that", "these",
    "those", "am", "is", "are", "was", "were", "be", "been", "being", "have",
    "has", "had", "having", "do", "does", "did", "doing", "would", "could",
    "shall", "may", "might", "must", "thy", "thou", "thee", "ye", "o", "oh",
    "upon", "as", "while", "because", "until", "unto", "shall", "let",
}


def pearson(xs, ys):
    n = len(xs)
    if n < 3:
        return 0.0
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    dx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    dy = math.sqrt(sum((y - my) ** 2 for y in ys))
    if dx == 0 or dy == 0:
        return 0.0
    return num / (dx * dy)


def describe(values):
    """Summary stats for a list of S2 values."""
    if not values:
        return None
    return {
        "n": len(values),
        "mean": round(statistics.mean(values), 4),
        "median": round(statistics.median(values), 4),
        "spike_rate": round(
            sum(1 for v in values if v >= SPIKE_THRESHOLD) / len(values), 4
        ),
    }


def extract_words(corpus):
    """Yield one record per complete-word token with external frequency data."""
    records = []
    for poem in corpus:
        meta = poem["metadata"]
        if meta.get("language", "en") != "en":
            continue
        era = meta.get("era", "unknown")
        tokens = poem["tokens"]
        for i, tok in enumerate(tokens):
            raw = tok["token"]
            if not raw.startswith(" "):
                continue
            core = raw.strip().lower()
            if not re.fullmatch(r"[a-z']+", core):
                continue
            nxt = tokens[i + 1]["token"] if i + 1 < len(tokens) else " "
            if nxt and nxt[0].isalpha():
                continue  # word continues into next BPE token
            zipf = zipf_frequency(core, "en")
            if zipf <= 0:
                continue
            records.append(
                {
                    "word": core,
                    "zipf": zipf,
                    "s2": tok["s2"],
                    "surprisal": tok["surprisal"],
                    "entropy": tok["entropy"],
                    "era": era,
                    "author": meta.get("author", "unknown"),
                    "title": meta.get("title", ""),
                    "is_poetry": era != "control",
                    "length": len(core),
                }
            )
    return records


def residualise(records):
    """Attach frequency-residual S2 via non-parametric bin-mean subtraction."""
    bins = defaultdict(list)
    for r in records:
        bins[round(r["zipf"] / BIN_WIDTH)].append(r["s2"])

    bin_means = {b: statistics.mean(v) for b, v in bins.items()}
    global_mean = statistics.mean(r["s2"] for r in records)

    for r in records:
        b = round(r["zipf"] / BIN_WIDTH)
        # Thin bins fall back to the global mean to avoid fitting noise.
        baseline = bin_means[b] if len(bins[b]) >= 30 else global_mean
        r["s2_resid"] = r["s2"] - baseline

    curve = [
        {
            "zipf_bin": round(b * BIN_WIDTH, 2),
            "n": len(bins[b]),
            "mean_s2": round(bin_means[b], 4),
        }
        for b in sorted(bins)
        if len(bins[b]) >= 30
    ]
    return curve


def bootstrap_gap(poetry, prose, field, iters=2000, seed=7):
    """Bootstrap CI for the poetry-minus-prose difference in `field`."""
    import random

    rng = random.Random(seed)
    a = [r[field] for r in poetry]
    b = [r[field] for r in prose]
    if not a or not b:
        return None
    gaps = []
    for _ in range(iters):
        sa = sum(a[rng.randrange(len(a))] for _ in range(len(a))) / len(a)
        sb = sum(b[rng.randrange(len(b))] for _ in range(len(b))) / len(b)
        gaps.append(sa - sb)
    gaps.sort()
    return {
        "mean": round(sum(gaps) / len(gaps), 4),
        "ci95_low": round(gaps[int(0.025 * iters)], 4),
        "ci95_high": round(gaps[int(0.975 * iters)], 4),
        "frac_above_zero": round(sum(1 for g in gaps if g > 0) / len(gaps), 4),
    }


def per_text_comparison(records):
    """Text-level means -- the honest unit of analysis for poetry vs prose."""
    texts = defaultdict(list)
    for r in records:
        texts[(r["title"], r["is_poetry"])].append(r)

    poem_means, prose_means = [], []
    for (title, is_poetry), rs in texts.items():
        if len(rs) < 20:
            continue
        m = statistics.mean(r["s2_resid"] for r in rs)
        (poem_means if is_poetry else prose_means).append((title, round(m, 4)))

    pm = [m for _, m in poem_means]
    qm = [m for _, m in prose_means]
    if not pm or not qm:
        return None

    worse = sum(1 for m in pm if m <= max(qm))
    return {
        "n_poems": len(pm),
        "n_prose": len(qm),
        "poem_mean_resid": round(statistics.mean(pm), 4),
        "prose_mean_resid": round(statistics.mean(qm), 4),
        "poem_sd": round(statistics.pstdev(pm), 4),
        "prose_texts": sorted(prose_means, key=lambda x: x[1]),
        "poems_below_worst_prose": worse,
        "pct_poems_below_worst_prose": round(100 * worse / len(pm), 1),
    }


def group_comparison(records, keyfunc, min_n=30):
    """Mean raw vs residual S2 for each group produced by keyfunc."""
    groups = defaultdict(list)
    for r in records:
        groups[keyfunc(r)].append(r)

    out = {}
    for name, rs in groups.items():
        if len(rs) < min_n:
            continue
        out[name] = {
            "n": len(rs),
            "mean_zipf": round(statistics.mean(r["zipf"] for r in rs), 3),
            "raw_s2": round(statistics.mean(r["s2"] for r in rs), 4),
            "resid_s2": round(statistics.mean(r["s2_resid"] for r in rs), 4),
            "spike_rate": round(
                sum(1 for r in rs if r["s2"] >= SPIKE_THRESHOLD) / len(rs), 4
            ),
        }
    return out


def length_buckets(records):
    def bucket(r):
        n = r["length"]
        if n <= 2:
            return "1-2"
        if n <= 4:
            return "3-4"
        if n <= 6:
            return "5-6"
        if n <= 9:
            return "7-9"
        return "10+"

    return group_comparison(records, bucket)


def polysemy_retest(records):
    """Re-run the polysemy finding against residual S2, if WordNet is available."""
    try:
        import nltk
        from nltk.corpus import wordnet as wn

        nltk.download("wordnet", quiet=True)
        nltk.download("omw-1.4", quiet=True)
        wn.synsets("test")
    except Exception as exc:  # noqa: BLE001 - optional dependency
        return {"available": False, "reason": str(exc)[:200]}

    cache = {}

    def bucket(r):
        w = r["word"]
        if w not in cache:
            cache[w] = len(wn.synsets(w))
        c = cache[w]
        if c == 0:
            return "not-in-wordnet"
        if c == 1:
            return "1 (monosemous)"
        if c <= 3:
            return "2-3 (low)"
        if c <= 7:
            return "4-7 (medium)"
        if c <= 15:
            return "8-15 (high)"
        return "16+ (very high)"

    return {"available": True, "buckets": group_comparison(records, bucket)}


def main():
    with open(RESULTS_FILE) as f:
        corpus = json.load(f)

    english = [p for p in corpus if p["metadata"].get("language", "en") == "en"]
    total_tokens = sum(len(p["tokens"]) for p in english)
    records = extract_words(corpus)
    print(f"Analysed {len(records)} complete words out of {total_tokens} tokens")

    curve = residualise(records)

    zipfs = [r["zipf"] for r in records]
    r_s2 = pearson(zipfs, [r["s2"] for r in records])
    r_surp = pearson(zipfs, [r["surprisal"] for r in records])
    r_ent = pearson(zipfs, [r["entropy"] for r in records])
    r_resid = pearson(zipfs, [r["s2_resid"] for r in records])

    poetry = [r for r in records if r["is_poetry"]]
    prose = [r for r in records if not r["is_poetry"]]

    results = {
        "meta": {
            "corpus_texts": len(corpus),
            "english_texts": len(english),
            "total_tokens": total_tokens,
            "analysed_words": len(records),
            "coverage_pct": round(100 * len(records) / total_tokens, 1),
            "frequency_source": "wordfreq Zipf scale (external, corpus-independent)",
            "bin_width": BIN_WIDTH,
            "spike_threshold": SPIKE_THRESHOLD,
        },
        "correlations": {
            "zipf_vs_s2": round(r_s2, 4),
            "zipf_vs_s2_r2": round(r_s2 ** 2, 4),
            "zipf_vs_surprisal": round(r_surp, 4),
            "zipf_vs_surprisal_r2": round(r_surp ** 2, 4),
            "zipf_vs_entropy": round(r_ent, 4),
            "zipf_vs_entropy_r2": round(r_ent ** 2, 4),
            "zipf_vs_residual_s2": round(r_resid, 4),
        },
        "frequency_curve": curve,
        "poetry_vs_prose": {
            "poetry": {
                **describe([r["s2"] for r in poetry]),
                "mean_zipf": round(statistics.mean(r["zipf"] for r in poetry), 3),
                "resid_s2": round(statistics.mean(r["s2_resid"] for r in poetry), 4),
            },
            "prose_control": {
                **describe([r["s2"] for r in prose]),
                "mean_zipf": round(statistics.mean(r["zipf"] for r in prose), 3),
                "resid_s2": round(statistics.mean(r["s2_resid"] for r in prose), 4),
            },
        },
        "bootstrap_raw_gap": bootstrap_gap(poetry, prose, "s2"),
        "bootstrap_resid_gap": bootstrap_gap(poetry, prose, "s2_resid"),
        "per_text": per_text_comparison(records),
        "by_era": group_comparison(records, lambda r: r["era"], min_n=100),
        "by_length": length_buckets(records),
        "by_word_class": group_comparison(
            records,
            lambda r: "function" if r["word"] in FUNCTION_WORDS else "content",
        ),
        "by_author": group_comparison(records, lambda r: r["author"], min_n=150),
        "polysemy_retest": polysemy_retest(records),
    }

    pv = results["poetry_vs_prose"]
    results["poetry_vs_prose"]["raw_gap"] = round(
        pv["poetry"]["mean"] - pv["prose_control"]["mean"], 4
    )
    results["poetry_vs_prose"]["resid_gap"] = round(
        pv["poetry"]["resid_s2"] - pv["prose_control"]["resid_s2"], 4
    )

    with open(OUTPUT_FILE, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nZipf vs S2:        r={r_s2:+.4f}  R2={r_s2**2:.4f}")
    print(f"Zipf vs surprisal: r={r_surp:+.4f}  R2={r_surp**2:.4f}")
    print(f"Zipf vs entropy:   r={r_ent:+.4f}  R2={r_ent**2:.4f}")
    print(f"\nPoetry raw S2 {pv['poetry']['mean']:+.3f} (zipf {pv['poetry']['mean_zipf']}) "
          f"| resid {pv['poetry']['resid_s2']:+.3f}")
    print(f"Prose  raw S2 {pv['prose_control']['mean']:+.3f} (zipf {pv['prose_control']['mean_zipf']}) "
          f"| resid {pv['prose_control']['resid_s2']:+.3f}")
    print(f"Gap: raw {results['poetry_vs_prose']['raw_gap']:+.3f} "
          f"-> residual {results['poetry_vs_prose']['resid_gap']:+.3f}")
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
