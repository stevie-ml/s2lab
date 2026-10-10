"""
Q2 Lexicon Analysis: What Do Poets Choose When GPT-2 Is Most Certain?

The 'Q2 quadrant' (high surprisal + low entropy) represents the purest Straussian
moments — the model was confident AND wrong. This experiment catalogs the lexical
and semantic patterns of Q2 choices: what types of words poets place at positions
of maximum model certainty.

Key questions:
1. What types of tokens (function words, content words, punctuation, proper nouns)
   dominate Q2 vs. Q1 (ambiguous surprise)?
2. What does the model EXPECT (top-1 alternative) at Q2 positions?
3. What semantic moves characterize Q2? ("function→content" swaps, etc.)
4. Which words appear in Q2 most often across the corpus (the Q2 lexicon)?
5. Do poets differ in their Q2 word preferences?
"""

import json
import re
from collections import defaultdict, Counter
import statistics

# ── Load corpus ────────────────────────────────────────────────────────────────
with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# ── Token classification helpers ──────────────────────────────────────────────

FUNCTION_WORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "is", "are", "was",
    "were", "be", "been", "have", "has", "had", "do", "does", "did", "will",
    "would", "could", "should", "may", "might", "shall", "can", "not", "no",
    "on", "at", "by", "for", "with", "from", "into", "about", "than", "that",
    "this", "these", "those", "it", "its", "he", "she", "they", "we", "i",
    "his", "her", "their", "our", "my", "your", "if", "as", "so", "there",
    "when", "who", "which", "what", "all", "each", "any", "some", "more",
    "up", "out", "then", "now", "just", "also", "how", "after", "before",
    "through", "over", "under", "between", "against", "while", "where", "whom"
}

COMMON_PUNCTUATION = {",", ".", ";", ":", "!", "?", "-", "—", "–", "'", '"',
                      "(", ")", "[", "]", "/", "\\", "&", "@", "#", "%"}


def classify_token(token_str: str) -> str:
    """Classify a raw token string into broad categories."""
    t = token_str.strip()
    if not t:
        return "empty"
    # Newline/whitespace only
    if all(c in "\n\r\t " for c in t):
        return "whitespace"
    # Punctuation only
    if all(c in ".,;:!?-—–'\"()[]/\\&@#%" for c in t):
        return "punctuation"
    # Number
    if re.match(r"^[\d,.]+$", t):
        return "numeral"
    # Remove leading space for word checks
    word = t.lstrip()
    if not word:
        return "whitespace"
    word_lower = word.lower()
    if word_lower in FUNCTION_WORDS:
        return "function_word"
    # Proper noun heuristic: starts with capital (not at position 0 of line)
    if word[0].isupper() and len(word) > 1:
        return "capitalized_word"
    # Content word (lowercase letter start)
    if word[0].isalpha():
        return "content_word"
    return "other"


def get_token_word(token_str: str) -> str:
    """Get normalized word form."""
    return token_str.strip().lower()


# ── Collect all tokens, compute corpus medians ────────────────────────────────

all_tokens = []
for poem in corpus:
    meta = poem["metadata"]
    for tok in poem["tokens"]:
        if tok.get("p_newline", 0) >= 0.9:
            continue  # artifact filter
        all_tokens.append({
            **tok,
            "poet": meta.get("author", "unknown"),
            "title": meta.get("title", ""),
            "era": meta.get("era", ""),
        })

print(f"Artifact-free tokens: {len(all_tokens):,}")

surp_vals = [t["surprisal"] for t in all_tokens]
ent_vals = [t["entropy"] for t in all_tokens]
surp_median = statistics.median(surp_vals)
ent_median = statistics.median(ent_vals)

print(f"Surprisal median: {surp_median:.3f}")
print(f"Entropy median:   {ent_median:.3f}")


def assign_quadrant(tok):
    hi_surp = tok["surprisal"] > surp_median
    lo_ent = tok["entropy"] < ent_median
    if hi_surp and lo_ent:
        return "Q2"  # Confident mismatch — purest Straussian
    elif hi_surp and not lo_ent:
        return "Q1"  # Ambiguous surprise
    elif not hi_surp and lo_ent:
        return "Q3"  # Confident match
    else:
        return "Q4"  # Lucky guess


# ── Assign quadrants ──────────────────────────────────────────────────────────

for tok in all_tokens:
    tok["quadrant"] = assign_quadrant(tok)

q2_tokens = [t for t in all_tokens if t["quadrant"] == "Q2"]
q1_tokens = [t for t in all_tokens if t["quadrant"] == "Q1"]
q3_tokens = [t for t in all_tokens if t["quadrant"] == "Q3"]
q4_tokens = [t for t in all_tokens if t["quadrant"] == "Q4"]

print(f"\nQ1 (ambig. surprise):     {len(q1_tokens):,}")
print(f"Q2 (confident mismatch):  {len(q2_tokens):,}")
print(f"Q3 (confident match):     {len(q3_tokens):,}")
print(f"Q4 (lucky guess):         {len(q4_tokens):,}")


# ── 1. Token type distribution by quadrant ───────────────────────────────────

print("\n=== Token Type Distribution by Quadrant ===")
for label, tokens in [("Q1", q1_tokens), ("Q2", q2_tokens),
                      ("Q3", q3_tokens), ("Q4", q4_tokens)]:
    counts = Counter(classify_token(t["token"]) for t in tokens)
    total = len(tokens)
    print(f"\n  {label} (n={total:,}):")
    for cat, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"    {cat:<22} {cnt:>6,}  ({cnt/total*100:>4.1f}%)")


# ── 2. Q2 vs Q1 enrichment ratio ─────────────────────────────────────────────

print("\n=== Token Type Enrichment: Q2 vs Q1 ===")
print(f"{'Type':<22} {'Q2%':>7} {'Q1%':>7} {'ratio':>7}")
q2_counts = Counter(classify_token(t["token"]) for t in q2_tokens)
q1_counts = Counter(classify_token(t["token"]) for t in q1_tokens)
all_cats = set(list(q2_counts.keys()) + list(q1_counts.keys()))
rows = []
for cat in all_cats:
    q2_pct = q2_counts.get(cat, 0) / len(q2_tokens) * 100
    q1_pct = q1_counts.get(cat, 0) / len(q1_tokens) * 100
    ratio = q2_pct / q1_pct if q1_pct > 0 else float("inf")
    rows.append((cat, q2_pct, q1_pct, ratio))
rows.sort(key=lambda x: -x[3])
for cat, q2p, q1p, r in rows:
    print(f"  {cat:<22} {q2p:>6.1f}%  {q1p:>6.1f}%  {r:>6.2f}x")


# ── 3. What did the model expect at Q2 positions? ───────────────────────────

print("\n=== What GPT-2 Expected at Q2 Positions (Top-1 Alternatives) ===")
expected_types = Counter()
actual_types = Counter()
swap_patterns = Counter()  # (expected_type, actual_type)

for tok in q2_tokens:
    alts = tok.get("alternatives", [])
    if not alts:
        continue
    expected_token = alts[0]["token"]
    expected_type = classify_token(expected_token)
    actual_type = classify_token(tok["token"])
    expected_types[expected_type] += 1
    actual_types[actual_type] += 1
    swap_patterns[(expected_type, actual_type)] += 1

print("\n  Expected (GPT-2's top prediction):")
for cat, cnt in expected_types.most_common():
    print(f"    {cat:<22} {cnt:>6,}  ({cnt/len(q2_tokens)*100:>4.1f}%)")

print("\n  Actual (poet's choice):")
for cat, cnt in actual_types.most_common():
    print(f"    {cat:<22} {cnt:>6,}  ({cnt/len(q2_tokens)*100:>4.1f}%)")

print("\n  Swap patterns (expected → actual), top 15:")
print(f"  {'Expected → Actual':<40} {'Count':>7} {'%':>6}")
for (exp, act), cnt in swap_patterns.most_common(15):
    print(f"  {exp:>22} → {act:<22} {cnt:>6,}  ({cnt/len(q2_tokens)*100:>4.1f}%)")


# ── 4. Q2 lexicon: most common Q2 words ────────────────────────────────────

print("\n=== Q2 Lexicon: Words Appearing Most Often in Confident Mismatch ===")
# Compare Q2 frequency to overall frequency (enrichment)
q2_word_freq = Counter(get_token_word(t["token"]) for t in q2_tokens
                       if classify_token(t["token"]) in ("content_word", "capitalized_word"))
all_word_freq = Counter(get_token_word(t["token"]) for t in all_tokens
                        if classify_token(t["token"]) in ("content_word", "capitalized_word"))

# Q2 enrichment ratio (Q2_pct / overall_pct), min count filter
total_q2_content = sum(q2_word_freq.values())
total_all_content = sum(all_word_freq.values())

enrichment_rows = []
for word, q2_cnt in q2_word_freq.items():
    if q2_cnt < 3:
        continue
    all_cnt = all_word_freq.get(word, 1)
    q2_pct = q2_cnt / total_q2_content
    all_pct = all_cnt / total_all_content
    enrichment = q2_pct / all_pct
    avg_s2 = statistics.mean(t["s2"] for t in q2_tokens
                             if get_token_word(t["token"]) == word)
    enrichment_rows.append((word, q2_cnt, all_cnt, enrichment, avg_s2))

enrichment_rows.sort(key=lambda x: -x[3])

print(f"\n  Top 30 Words Most Enriched in Q2 (vs corpus average):")
print(f"  {'Word':<18} {'Q2n':>5} {'Total':>7} {'Enrich':>8} {'AvgS2':>7}")
for word, q2n, alln, enrich, avgs2 in enrichment_rows[:30]:
    print(f"  {word:<18} {q2n:>5} {alln:>7} {enrich:>7.2f}x {avgs2:>+7.2f}")

print(f"\n  Top 30 Words by Raw Q2 Frequency:")
print(f"  {'Word':<18} {'Q2n':>5} {'Total':>7} {'Q2%':>7} {'AvgS2':>7}")
for word, q2n, _, enrich, avgs2 in sorted(enrichment_rows, key=lambda x: -x[1])[:30]:
    alln = all_word_freq.get(word, 1)
    q2_pct = q2n / total_q2_content * 100
    print(f"  {word:<18} {q2n:>5} {alln:>7} {q2_pct:>6.2f}%  {avgs2:>+7.2f}")


# ── 5. Most extreme Q2 examples (canonical "anti-consensus" moves) ──────────

print("\n=== Top 25 Canonical Anti-Consensus Moments (Q2, highest S2) ===")
print(f"  {'Token':<16} {'S2':>7} {'Surp':>7} {'Ent':>5} {'Expected (top-1)':>20}  Poet / Context")
print("  " + "-" * 95)
q2_sorted = sorted(q2_tokens, key=lambda x: -x["s2"])
for tok in q2_sorted[:25]:
    alts = tok.get("alternatives", [])
    expected = alts[0]["token"] if alts else "?"
    poet = tok.get("poet", "")[:18]
    context = tok.get("context_before", "")[-25:].replace("\n", "↵").strip()
    print(f"  {tok['token'][:14]:<16} {tok['s2']:>+7.2f} {tok['surprisal']:>7.2f} "
          f"{tok['entropy']:>5.2f} {expected:>20}  {poet} | ...{context}")


# ── 6. Q2 function-word → content-word swaps (most illuminating sub-pattern) ─

print("\n=== Function→Content Swaps in Q2 (Model Expected Grammar, Poet Chose Image) ===")
fw_to_content = [
    t for t in q2_tokens
    if t.get("alternatives") and
    classify_token(t["alternatives"][0]["token"]) == "function_word" and
    classify_token(t["token"]) in ("content_word", "capitalized_word")
]
fw_to_content.sort(key=lambda x: -x["s2"])
print(f"  Total function→content swaps: {len(fw_to_content)} ({len(fw_to_content)/len(q2_tokens)*100:.1f}% of Q2)")
print(f"\n  Top 20:")
print(f"  {'Chosen':<16} {'S2':>7} {'Expected':>12}  Context | Poet")
print("  " + "-" * 80)
for tok in fw_to_content[:20]:
    alts = tok.get("alternatives", [])
    expected = alts[0]["token"] if alts else "?"
    poet = tok.get("poet", "")[:18]
    context = tok.get("context_before", "")[-25:].replace("\n", "↵").strip()
    print(f"  {tok['token'][:14]:<16} {tok['s2']:>+7.2f} {expected:>12}  ...{context} | {poet}")


# ── 7. Per-poet Q2 vocabulary profiles ───────────────────────────────────────

print("\n=== Per-Poet Q2 Vocabulary (Top Words per Poet, n≥40 artifact-free tokens) ===")

poet_tokens = defaultdict(list)
for tok in all_tokens:
    poet_tokens[tok["poet"]].append(tok)

poet_q2_vocab = {}
for poet, tokens in poet_tokens.items():
    if len(tokens) < 40:
        continue
    q2 = [t for t in tokens if t["quadrant"] == "Q2"]
    if len(q2) < 3:
        continue
    words = Counter(get_token_word(t["token"]) for t in q2
                    if classify_token(t["token"]) in ("content_word", "capitalized_word"))
    top_words = words.most_common(6)
    q2_pct = len(q2) / len(tokens) * 100
    poet_q2_vocab[poet] = {
        "q2_pct": q2_pct,
        "n_tokens": len(tokens),
        "n_q2": len(q2),
        "top_words": top_words,
    }

# Sort by Q2 percent
sorted_poets = sorted(poet_q2_vocab.items(), key=lambda x: -x[1]["q2_pct"])
print(f"\n  {'Poet':<28} {'Q2%':>5} {'n':>6}  Top Q2 words")
print("  " + "-" * 90)
for poet, info in sorted_poets[:25]:
    top = ", ".join(f"{w}({c})" for w, c in info["top_words"][:4])
    print(f"  {poet:<28} {info['q2_pct']:>4.1f}% {info['n_tokens']:>6}  {top}")


print("\nDone.")
