"""
Straussian Gap Taxonomy: What does the poet suppress, and what do they choose?

For each high-S2 moment, we characterize:
  - What GPT-2 expected (its top prediction)
  - What the poet actually wrote
  - The "type" of deviation

Taxonomy categories:
  - FUNCTION_TO_CONTENT: Model expected a function word; poet chose a content word
  - PUNCTUATION_SKIP: Model expected punctuation/newline; poet continued
  - VERB_SWERVE: Model expected a verb; poet chose noun/adj/other
  - NOUN_SWERVE: Model expected a noun; poet chose verb/adj/other
  - SEMANTIC_INVERSION: Poet chose near-opposite meaning of top prediction
  - CONCRETE_SURGE: Model expected abstract/generic; poet chose vivid/concrete specific
  - PROPER_NOUN_BREAK: Poet chose a proper noun / named entity where model expected common word
  - MODAL_DODGE: Model expected modal/auxiliary; poet bypassed
  - CONTINUATION: Catch-all for other high-S2 moments

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
from collections import defaultdict, Counter

RESULT_PATH = "results/corpus_results.json"

# ── Token classification helpers ─────────────────────────────────────────────

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
    "down", "out", "over", "under", "again", "also", "here", "there", "also",
    "i", "he", "she", "you", "me", "him", "her",
}

PUNCTUATION_TOKENS = {
    ".", ",", "!", "?", ";", ":", "-", "–", "—", "(", ")", '"', "'",
    "\n", "...", "``", "''",
}

MODAL_AUXILIARIES = {
    "will", "would", "could", "should", "may", "might", "can", "shall", "must",
    "'ll", "'d", "'ve", "'m", "'re", "'s",
}

def normalize(tok: str) -> str:
    """Strip leading space and lowercase."""
    return tok.strip().lower()

def classify_token(tok: str) -> str:
    """Classify a token into coarse categories."""
    n = normalize(tok)
    if n in PUNCTUATION_TOKENS or n.startswith("\n"):
        return "PUNCTUATION"
    if n in FUNCTION_WORDS:
        return "FUNCTION"
    if n in MODAL_AUXILIARIES:
        return "MODAL"
    # Heuristics for proper nouns: capitalized non-first token, not common word
    stripped = tok.strip()
    if stripped and stripped[0].isupper() and n not in FUNCTION_WORDS:
        return "PROPER_NOUN"
    return "CONTENT"


def deviation_type(top_alt_tok: str, chosen_tok: str) -> str:
    """Map (expected, actual) token pair to a taxonomy label."""
    exp_class = classify_token(top_alt_tok)
    act_class = classify_token(chosen_tok)

    if exp_class == "PUNCTUATION":
        return "PUNCTUATION_SKIP"
    if exp_class == "FUNCTION" and act_class in ("CONTENT", "PROPER_NOUN"):
        return "FUNCTION_TO_CONTENT"
    if exp_class == "MODAL":
        return "MODAL_DODGE"
    if act_class == "PROPER_NOUN" and exp_class == "CONTENT":
        return "PROPER_NOUN_BREAK"

    # Semantic inversion check: look for antonym-ish patterns in the label
    # Simple heuristic: top-5 alts contain antonymy signals
    # (We'll do this at a higher level; here just return general swerve)
    if exp_class in ("FUNCTION", "CONTENT", "PROPER_NOUN") and act_class in ("CONTENT", "PROPER_NOUN"):
        return "CONTENT_SUBSTITUTION"
    return "OTHER"


# ── Load corpus ───────────────────────────────────────────────────────────────

with open(RESULT_PATH) as f:
    corpus = json.load(f)

print(f"Loaded {len(corpus)} poems\n")

# ── Collect all high-S2 moments ───────────────────────────────────────────────

S2_THRESHOLD = 3.0  # bits — roughly 99th percentile
MIN_TOKEN_LEN = 2   # skip single-char tokens

high_s2_records = []

for poem in corpus:
    meta = poem["metadata"]
    for tok in poem.get("tokens", []):
        token_text = tok.get("token", "")
        s2 = tok.get("s2", 0)
        alts = tok.get("alternatives", [])
        if (
            s2 >= S2_THRESHOLD
            and len(token_text.strip()) >= MIN_TOKEN_LEN
            and alts
        ):
            top_alt = alts[0]["token"]
            top_alt_prob = alts[0]["prob"]
            dev = deviation_type(top_alt, token_text)
            high_s2_records.append({
                "title": meta["title"],
                "author": meta["author"],
                "year": meta.get("year", 0),
                "era": meta.get("era", "unknown"),
                "position": tok["position"],
                "token": token_text,
                "s2": s2,
                "surprisal": tok.get("surprisal", 0),
                "entropy": tok.get("entropy", 0),
                "rank": tok.get("rank", 0),
                "top_alt": top_alt,
                "top_alt_prob": top_alt_prob,
                "top_alt_class": classify_token(top_alt),
                "chosen_class": classify_token(token_text),
                "deviation": dev,
                "context_before": tok.get("context_before", ""),
            })

high_s2_records.sort(key=lambda r: r["s2"], reverse=True)
print(f"High-S2 tokens (S2 ≥ {S2_THRESHOLD}): {len(high_s2_records)}\n")

# ── 1. Taxonomy distribution ──────────────────────────────────────────────────

print("=" * 60)
print("1. TAXONOMY OF STRAUSSIAN DEVIATIONS")
print("=" * 60)

dev_counter = Counter(r["deviation"] for r in high_s2_records)
dev_s2_totals = defaultdict(list)
for r in high_s2_records:
    dev_s2_totals[r["deviation"]].append(r["s2"])

print(f"\n{'Deviation Type':<25} {'Count':>6} {'%':>6} {'Mean S2':>8} {'Max S2':>8}")
print("-" * 60)
total = len(high_s2_records)
for dev, count in dev_counter.most_common():
    s2_vals = dev_s2_totals[dev]
    pct = 100 * count / total
    mean_s2 = sum(s2_vals) / len(s2_vals)
    max_s2 = max(s2_vals)
    print(f"{dev:<25} {count:>6} {pct:>6.1f}% {mean_s2:>8.2f} {max_s2:>8.2f}")

# ── 2. Top model-suppressed tokens ───────────────────────────────────────────

print("\n" + "=" * 60)
print("2. WHAT DID GPT-2 EXPECT? (Top suppressed alternatives)")
print("=" * 60)

suppressed_counter = Counter()
for r in high_s2_records:
    suppressed_counter[r["top_alt"].strip()] += 1

print("\nMost-suppressed alternatives (what the model wanted but didn't get):")
print(f"\n{'Token':>12} {'Suppressed N':>14}")
print("-" * 30)
for tok, cnt in suppressed_counter.most_common(20):
    print(f"{tok!r:>12} {cnt:>14}")

# ── 3. Top examples in each category ─────────────────────────────────────────

print("\n" + "=" * 60)
print("3. EXEMPLARY HIGH-S2 MOMENTS BY CATEGORY")
print("=" * 60)

for dev_type in ["PUNCTUATION_SKIP", "FUNCTION_TO_CONTENT", "CONTENT_SUBSTITUTION",
                 "MODAL_DODGE", "PROPER_NOUN_BREAK", "OTHER"]:
    examples = [r for r in high_s2_records if r["deviation"] == dev_type][:3]
    if not examples:
        continue
    print(f"\n── {dev_type} ──")
    for ex in examples:
        ctx = ex["context_before"][-30:] if ex["context_before"] else "(start)"
        print(
            f"  [{ex['author'][:18]:18}] …{ctx!r}| chose {ex['token']!r:12} "
            f"(expected {ex['top_alt']!r:10}, top_prob={ex['top_alt_prob']:.3f}, S2={ex['s2']:.2f})"
        )

# ── 4. Expected vs. chosen class cross-table ──────────────────────────────────

print("\n" + "=" * 60)
print("4. EXPECTED CLASS → CHOSEN CLASS (transition matrix)")
print("=" * 60)

classes = ["FUNCTION", "CONTENT", "PUNCTUATION", "MODAL", "PROPER_NOUN"]
matrix = defaultdict(Counter)
for r in high_s2_records:
    matrix[r["top_alt_class"]][r["chosen_class"]] += 1

header = f"{'Expected →':>18}" + "".join(f"{c[:9]:>12}" for c in classes)
print(f"\n{header}")
print("-" * (18 + 12 * len(classes)))
for exp_class in classes:
    row_total = sum(matrix[exp_class].values())
    if row_total == 0:
        continue
    row = f"{exp_class:>18}"
    for chosen_class in classes:
        n = matrix[exp_class][chosen_class]
        row += f"{n:>12}"
    row += f"  (n={row_total})"
    print(row)

# ── 5. Poet-level Straussian style ───────────────────────────────────────────

print("\n" + "=" * 60)
print("5. POET STRAUSSIAN PROFILES")
print("=" * 60)

poet_stats = defaultdict(lambda: {"high_s2": 0, "deviations": Counter(), "s2_vals": [], "total_tokens": 0})
for poem in corpus:
    meta = poem["metadata"]
    author = meta["author"]
    for tok in poem.get("tokens", []):
        poet_stats[author]["total_tokens"] += 1
        s2 = tok.get("s2", 0)
        poet_stats[author]["s2_vals"].append(s2)
        if s2 >= S2_THRESHOLD:
            poet_stats[author]["high_s2"] += 1

for r in high_s2_records:
    poet_stats[r["author"]]["deviations"][r["deviation"]] += 1

print(f"\n{'Author':>24} {'Poems':>5} {'AvgS2':>7} {'High%':>7} {'Top Deviation':<25}")
print("-" * 75)

poet_poem_count = Counter()
for poem in corpus:
    poet_poem_count[poem["metadata"]["author"]] += 1

rows = []
for author, stats in poet_stats.items():
    if not stats["s2_vals"]:
        continue
    avg_s2 = sum(stats["s2_vals"]) / len(stats["s2_vals"])
    high_pct = 100 * stats["high_s2"] / max(stats["total_tokens"], 1)
    top_dev = stats["deviations"].most_common(1)
    top_dev_label = top_dev[0][0] if top_dev else "—"
    rows.append((author, poet_poem_count[author], avg_s2, high_pct, top_dev_label))

rows.sort(key=lambda x: x[2], reverse=True)
for author, n_poems, avg_s2, high_pct, top_dev in rows:
    print(f"{author:>24} {n_poems:>5} {avg_s2:>7.3f} {high_pct:>6.1f}% {top_dev:<25}")

# ── 6. Era-level analysis ─────────────────────────────────────────────────────

print("\n" + "=" * 60)
print("6. ERA-LEVEL STRAUSSIAN GAP")
print("=" * 60)

era_stats = defaultdict(lambda: {"s2_vals": [], "tokens": 0, "high_s2": 0})
for poem in corpus:
    era = poem["metadata"].get("era", "unknown")
    for tok in poem.get("tokens", []):
        era_stats[era]["tokens"] += 1
        s2 = tok.get("s2", 0)
        era_stats[era]["s2_vals"].append(s2)
        if s2 >= S2_THRESHOLD:
            era_stats[era]["high_s2"] += 1

print(f"\n{'Era':>15} {'Tokens':>8} {'Avg S2':>8} {'High%':>8}")
print("-" * 45)
for era, stats in sorted(era_stats.items(), key=lambda x: -sum(x[1]["s2_vals"])/max(len(x[1]["s2_vals"]),1)):
    if not stats["s2_vals"]:
        continue
    avg = sum(stats["s2_vals"]) / len(stats["s2_vals"])
    high_pct = 100 * stats["high_s2"] / max(stats["tokens"], 1)
    print(f"{era:>15} {stats['tokens']:>8} {avg:>8.3f} {high_pct:>7.1f}%")

# ── 7. Semantic polarity scan ─────────────────────────────────────────────────

print("\n" + "=" * 60)
print("7. SEMANTIC POLARITY: Poet's word vs. model's expectation")
print("=" * 60)

# Simple check: look for cases where the top-5 alternatives all belong to
# a coherent semantic cluster (movement, emotion, abstraction) and the poet
# chose something orthogonal

MOVEMENT_WORDS = {"into","through","over","around","along","toward","towards",
                  "across","beyond","forward","away","down","up","out"}
ABSTRACT_WORDS = {"truth","beauty","death","love","life","time","nature","God",
                  "soul","spirit","heart","mind","light","dark","shadow","hope",
                  "fear","peace","dream","memory","silence","voice","world","power"}
CONCRETE_WORDS = {"stone","leaf","grass","door","hand","eye","water","wind",
                  "tree","bird","sky","sun","moon","star","rain","snow","wood",
                  "fire","dust","earth","blood","bone","bread","cup","iron","gold"}

movement_poet_chose_concrete = []
abstract_poet_chose_concrete = []

for r in high_s2_records:
    alts_normalized = {normalize(a["token"]) for a in r.get("alternatives", [])[:5] if "token" in a}
    chosen_n = normalize(r["token"])

    # Case A: model expected movement, poet chose concrete noun
    if alts_normalized & MOVEMENT_WORDS and chosen_n in CONCRETE_WORDS:
        movement_poet_chose_concrete.append(r)

    # Case B: model expected abstract, poet chose concrete
    if alts_normalized & ABSTRACT_WORDS and chosen_n in CONCRETE_WORDS:
        abstract_poet_chose_concrete.append(r)

print(f"\nMovement → Concrete shift: {len(movement_poet_chose_concrete)} instances")
for r in movement_poet_chose_concrete[:5]:
    ctx = r["context_before"][-25:] if r["context_before"] else ""
    print(f"  [{r['author'][:16]:16}] …{ctx!r} | chose {r['token']!r} (expected alts include movement words, S2={r['s2']:.2f})")

print(f"\nAbstract → Concrete shift: {len(abstract_poet_chose_concrete)} instances")
for r in abstract_poet_chose_concrete[:5]:
    ctx = r["context_before"][-25:] if r["context_before"] else ""
    print(f"  [{r['author'][:16]:16}] …{ctx!r} | chose {r['token']!r} (expected alts abstract, S2={r['s2']:.2f})")

print("\n\nDone.")
