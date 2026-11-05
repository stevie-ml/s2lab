"""
Poetic Peaks: Anatomy of the Single Highest-S2 Moment per Poem

For each poem in the corpus, find the SINGLE highest-S2 token (artifact-filtered)
and characterize it. This builds a cross-corpus "hall of peaks" — the most extreme
Straussian gap moment in each poem.

Research questions:
  1. What POS category typically occupies the peak position? Are noun peaks more
     common than verb peaks? Do certain eras peak on different word classes?
  2. How high is the typical peak, and does peak height predict overall S2 avg?
  3. What is the suppressed alternative at the peak? (function vs content vs structural)
  4. At what position in the poem does the peak typically occur?
     First third, middle, last third? Do different eras have different peak timing?
  5. Is the peak token rare (high frequency rank) or a common word used in an
     unexpected context?

Filtering:
  - Exclude tokens where p_newline > 0.9 (capitalization artifact)
  - Exclude subword continuation tokens (no leading space + alphabetic)
  - Require at least 5 artifact-free tokens per poem
"""

import json
import os
import re
from collections import defaultdict, Counter
import statistics

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")
FINDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "findings")

# ── Function word list (from ambush_vs_fog_classification) ────────────────────
FUNCTION_WORDS = {
    "the", "a", "an", "this", "that", "these", "those", "my", "your", "his", "her",
    "its", "our", "their", "all", "both", "each", "every", "few", "many", "much",
    "some", "any", "no", "such", "what", "which", "whose",
    "in", "on", "at", "to", "for", "of", "with", "by", "from", "up", "about",
    "into", "through", "during", "before", "after", "above", "below", "between",
    "under", "along", "around", "against", "out", "off", "over", "within", "without",
    "across", "behind", "beyond", "despite", "down", "past", "since", "toward",
    "upon", "via", "throughout", "among", "beside", "except", "like", "near", "per",
    "and", "but", "or", "nor", "yet", "so", "although", "because", "while",
    "whereas", "whether", "if", "unless", "until", "when", "where",
    "though", "as", "than",
    "i", "me", "myself", "you", "yourself", "he", "him", "himself",
    "she", "herself", "it", "itself", "we", "us", "ourselves",
    "they", "them", "themselves", "who", "whom",
    "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "shall", "should", "may", "might",
    "must", "can", "could", "ought",
    "not", "very", "quite", "rather", "too", "also", "just", "even", "only",
    "still", "already", "never", "ever", "always", "often", "sometimes", "here",
    "there", "now", "then", "today", "yesterday", "tomorrow", "well",
    "more", "most", "less", "least", "much",
    "no", "yes", "oh", "o", "ah",
}

PUNCT = set('.,!?;:\'"()-—–…\'"`')


def classify_token_type(tok: str) -> str:
    """Classify a token as function/content/punct/structural."""
    stripped = tok.strip()
    if not stripped:
        return "structural"
    if stripped in {"\n", "\\n"} or stripped == "":
        return "structural"
    if all(c in '.,!?;:\'"()-—–…\'"`' for c in stripped):
        return "punct"
    # subword check
    if tok and tok[0] != " " and any(c.isalpha() for c in tok):
        return "subword"
    lower = stripped.lower()
    if lower in FUNCTION_WORDS:
        return "function"
    return "content"


def is_artifact(tok_data: dict) -> bool:
    """True if this token is a capitalization/newline artifact."""
    return tok_data.get("p_newline", 0) > 0.9


def is_subword(tok: str) -> bool:
    """True if tok is a GPT-2 subword continuation."""
    if not tok:
        return False
    if tok[0] == " ":
        return False
    if all(not c.isalpha() for c in tok):
        return False
    return True


def guess_pos(tok: str) -> str:
    """Very coarse POS guess from surface form only."""
    t = tok.strip().lower()
    if not t or not any(c.isalpha() for c in t):
        return "PUNCT"
    if t in FUNCTION_WORDS:
        return "FUNC"
    # Heuristics
    if t.endswith("ing"):
        return "VERB/GERUND"
    if t.endswith("ed"):
        return "VERB/ADJ"
    if t.endswith("ly"):
        return "ADV"
    if t.endswith("ness") or t.endswith("tion") or t.endswith("ment"):
        return "NOUN"
    if t.endswith("ful") or t.endswith("less") or t.endswith("ous") or t.endswith("ive"):
        return "ADJ"
    if t[0].isupper() and len(t) > 1:
        return "PROPER/NOUN"
    return "CONTENT"  # default


# ── Load corpus ───────────────────────────────────────────────────────────────

corpus_path = os.path.join(RESULTS_DIR, "corpus_results.json")
with open(corpus_path) as f:
    corpus = json.load(f)

print(f"Corpus: {len(corpus)} poems")

peaks = []  # one entry per poem

for poem in corpus:
    meta = poem["metadata"]
    tokens = poem.get("tokens", [])

    # Filter artifacts and subwords
    clean = [t for t in tokens
             if not is_artifact(t) and not is_subword(t.get("token", ""))]

    if len(clean) < 5:
        continue

    # Find peak S2 token
    peak = max(clean, key=lambda t: t.get("s2", -999))
    s2_val = peak.get("s2", 0)

    # Only consider genuine positive peaks
    if s2_val < 1.0:
        continue

    tok_str = peak.get("token", "")
    pos = guess_pos(tok_str)
    tok_type = classify_token_type(tok_str)

    # Position in poem (0=start, 1=end)
    n_clean = len(clean)
    peak_idx = next((i for i, t in enumerate(clean) if t is peak), 0)
    rel_pos = peak_idx / max(n_clean - 1, 1)

    # Classify relative position
    if rel_pos < 0.33:
        pos_zone = "first_third"
    elif rel_pos < 0.67:
        pos_zone = "middle_third"
    else:
        pos_zone = "last_third"

    # Suppressed alternative classification
    alts = peak.get("alternatives", [])
    suppressed_type = "unknown"
    suppressed_word = ""
    if alts:
        top_alt = alts[0]["token"]
        suppressed_word = top_alt.strip()
        suppressed_type = classify_token_type(top_alt)

    # Rank of chosen token (how rare was it?)
    rank = peak.get("rank", 0)

    peaks.append({
        "title": meta.get("title", ""),
        "author": meta.get("author", ""),
        "year": meta.get("year", 0),
        "era": meta.get("era", ""),
        "peak_token": tok_str.strip(),
        "peak_s2": round(s2_val, 3),
        "peak_surprisal": round(peak.get("surprisal", 0), 3),
        "peak_entropy": round(peak.get("entropy", 0), 3),
        "peak_rank": rank,
        "tok_type": tok_type,
        "pos_guess": pos,
        "pos_zone": pos_zone,
        "rel_pos": round(rel_pos, 3),
        "suppressed_type": suppressed_type,
        "suppressed_word": suppressed_word,
        "avg_s2": round(poem["summary"]["avg_s2"], 3),
        "n_clean": n_clean,
    })

print(f"Valid poems with peak S2 >= 1.0: {len(peaks)}")

# ── Analysis 1: POS distribution of peaks ────────────────────────────────────

pos_counts = Counter(p["pos_guess"] for p in peaks)
tok_type_counts = Counter(p["tok_type"] for p in peaks)
zone_counts = Counter(p["pos_zone"] for p in peaks)
suppressed_counts = Counter(p["suppressed_type"] for p in peaks)

print("\n--- POS at Peak ---")
for pos, n in pos_counts.most_common():
    print(f"  {pos}: {n} ({100*n/len(peaks):.1f}%)")

print("\n--- Token type at Peak ---")
for tt, n in tok_type_counts.most_common():
    print(f"  {tt}: {n} ({100*n/len(peaks):.1f}%)")

print("\n--- Position zone of Peak ---")
for z, n in zone_counts.most_common():
    print(f"  {z}: {n} ({100*n/len(peaks):.1f}%)")

print("\n--- Suppressed alternative type ---")
for st, n in suppressed_counts.most_common():
    print(f"  {st}: {n} ({100*n/len(peaks):.1f}%)")

# ── Analysis 2: Peak height distribution ─────────────────────────────────────

s2_vals = [p["peak_s2"] for p in peaks]
print(f"\n--- Peak S2 distribution ---")
print(f"  Mean: {statistics.mean(s2_vals):.2f}")
print(f"  Median: {statistics.median(s2_vals):.2f}")
print(f"  Stdev: {statistics.stdev(s2_vals):.2f}")
print(f"  Max: {max(s2_vals):.2f}")
print(f"  >10: {sum(1 for v in s2_vals if v > 10)} poems")
print(f"  >15: {sum(1 for v in s2_vals if v > 15)} poems")
print(f"  >20: {sum(1 for v in s2_vals if v > 20)} poems")

# Correlation between peak S2 and avg S2
peaks_sorted_by_s2 = sorted(peaks, key=lambda p: p["peak_s2"], reverse=True)
print("\n--- Top 15 absolute peaks across corpus ---")
for p in peaks_sorted_by_s2[:15]:
    print(f"  S2={p['peak_s2']:5.1f} | '{p['peak_token']}' (suppressed: '{p['suppressed_word']}') | {p['author']}, {p['title'][:40]}")

# ── Analysis 3: Era-level peak profiles ──────────────────────────────────────

era_data = defaultdict(list)
for p in peaks:
    era_data[p["era"]].append(p)

print("\n--- Era peak profiles (eras with >=3 poems) ---")
era_rows = []
for era, ps in era_data.items():
    if len(ps) < 3:
        continue
    avg_peak = statistics.mean(p["peak_s2"] for p in ps)
    avg_rel_pos = statistics.mean(p["rel_pos"] for p in ps)
    content_pct = 100 * sum(1 for p in ps if p["tok_type"] == "content") / len(ps)
    last_third_pct = 100 * sum(1 for p in ps if p["pos_zone"] == "last_third") / len(ps)
    era_rows.append((era, len(ps), avg_peak, avg_rel_pos, content_pct, last_third_pct))

era_rows.sort(key=lambda r: r[2], reverse=True)
for row in era_rows:
    print(f"  {row[0]:<20} n={row[1]:3d} | avg_peak={row[2]:5.1f} | rel_pos={row[3]:.2f} | content%={row[4]:.0f}% | last_third%={row[5]:.0f}%")

# ── Analysis 4: Does peak position correlate with poem length? ───────────────

short_poems = [p for p in peaks if p["n_clean"] < 30]
medium_poems = [p for p in peaks if 30 <= p["n_clean"] < 100]
long_poems = [p for p in peaks if p["n_clean"] >= 100]

print("\n--- Peak position by poem length ---")
for label, group in [("Short (<30 tokens)", short_poems), ("Medium (30-100)", medium_poems), ("Long (100+)", long_poems)]:
    if group:
        avg_pos = statistics.mean(p["rel_pos"] for p in group)
        avg_s2 = statistics.mean(p["peak_s2"] for p in group)
        print(f"  {label}: n={len(group)}, avg_rel_pos={avg_pos:.2f}, avg_peak_s2={avg_s2:.2f}")

# ── Analysis 5: Suppressed word at the peak — what did GPT-2 most want? ──────

# Most common suppressed words when poet peaked content
content_peaks = [p for p in peaks if p["tok_type"] == "content"]
suppressed_at_content_peak = Counter(
    p["suppressed_word"].lower() for p in content_peaks
    if p["suppressed_word"] and len(p["suppressed_word"]) > 1
)

print("\n--- Top suppressed words at content peaks ---")
for word, n in suppressed_at_content_peak.most_common(20):
    print(f"  '{word}': {n}")

# ── Analysis 6: Rank at peak — how rare is the peak token? ──────────────────

rank_vals = [p["peak_rank"] for p in peaks if p["peak_rank"] > 0]
if rank_vals:
    low_rank = sum(1 for r in rank_vals if r <= 100)
    mid_rank = sum(1 for r in rank_vals if 100 < r <= 1000)
    high_rank = sum(1 for r in rank_vals if r > 1000)
    print(f"\n--- Vocabulary rank at peak token ---")
    print(f"  Top-100 (common words): {low_rank} ({100*low_rank/len(rank_vals):.1f}%)")
    print(f"  101-1000 (medium freq): {mid_rank} ({100*mid_rank/len(rank_vals):.1f}%)")
    print(f"  >1000 (rare words):     {high_rank} ({100*high_rank/len(rank_vals):.1f}%)")
    print(f"  Median rank: {statistics.median(rank_vals):.0f}")

# ── Save results ──────────────────────────────────────────────────────────────

out_path = os.path.join(RESULTS_DIR, "poetic_peaks.json")
with open(out_path, "w") as f:
    json.dump({
        "n_poems": len(peaks),
        "peaks": peaks,
        "pos_distribution": dict(pos_counts),
        "tok_type_distribution": dict(tok_type_counts),
        "zone_distribution": dict(zone_counts),
        "suppressed_type_distribution": dict(suppressed_counts),
        "peak_s2_stats": {
            "mean": round(statistics.mean(s2_vals), 3),
            "median": round(statistics.median(s2_vals), 3),
            "stdev": round(statistics.stdev(s2_vals), 3),
            "max": round(max(s2_vals), 3),
        },
        "era_rows": [
            {"era": r[0], "n": r[1], "avg_peak": round(r[2], 2),
             "avg_rel_pos": round(r[3], 2), "content_pct": round(r[4], 1),
             "last_third_pct": round(r[5], 1)}
            for r in era_rows
        ],
        "top_15_peaks": [
            {"rank": i+1, "s2": p["peak_s2"], "token": p["peak_token"],
             "suppressed": p["suppressed_word"], "author": p["author"],
             "title": p["title"], "era": p["era"]}
            for i, p in enumerate(peaks_sorted_by_s2[:15])
        ],
    }, f, indent=2)
print(f"\nSaved to {out_path}")
