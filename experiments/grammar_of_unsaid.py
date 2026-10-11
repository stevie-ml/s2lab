"""
Grammar of the Unsaid: POS substitution patterns in the Straussian gap.

When a poet deviates from GPT-2's prediction, what grammatical category
does GPT-2 expect vs. what the poet actually wrote?

This builds a "grammar substitution matrix" showing systematic POS-level
deviations in poetry.
"""
import json
import re
from collections import defaultdict
import statistics

import spacy

nlp = spacy.load("en_core_web_sm")

# --- Load corpus results ---
with open("/home/user/s2lab/results/corpus_results.json") as f:
    results = json.load(f)

if isinstance(results, dict):
    results = results.get("results", list(results.values()))

# --- Helper: get POS tag for a single word/token ---
def pos_tag(word):
    """Return coarse POS for a word (NOUN, VERB, ADJ, ADV, DET, PREP, etc.)"""
    word = word.strip()
    if not word or word in ("\n", ""):
        return "NEWLINE"
    # remove leading special chars
    clean = re.sub(r"^[^a-zA-Z0-9]+", "", word)
    if not clean:
        return "PUNCT"
    doc = nlp(clean[:30])  # only first 30 chars for speed
    if not doc:
        return "OTHER"
    token = doc[0]
    pos = token.pos_
    if pos in ("", "X", "SYM"):
        return "OTHER"
    return pos

# Build POS tags for alternates and actuals
# We focus on HIGH-S2 positions (S2 > 2.0 to avoid artifact positions)
# and also exclude clear stanza-break artifacts (p_newline > 0.9)

print("Building POS substitution matrix...")

# Substitution matrix: actual_pos -> expected_pos -> count
sub_matrix = defaultdict(lambda: defaultdict(int))
# Also: for each actual POS, avg S2 when substituting from each expected POS
pos_s2 = defaultdict(list)

# Per-era breakdowns
era_subs = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))

all_sub_examples = []  # (s2, actual_token, expected_token, actual_pos, expected_pos, poem)

total_tokens = 0
analyzed = 0

for poem in results:
    meta = poem["metadata"]
    era = meta.get("era", "unknown")
    title = meta.get("title", "")
    author = meta.get("author", "")
    lang = meta.get("language", "en")

    if lang != "en":
        continue

    tokens = poem.get("tokens", [])
    for tok in tokens:
        total_tokens += 1
        s2 = tok.get("s2", 0)
        p_newline = tok.get("p_newline", 0)

        # Skip stanza-break artifacts
        if p_newline > 0.9:
            continue

        actual = tok.get("token", "")
        alternatives = tok.get("alternatives", [])
        if not alternatives:
            continue

        # Top predicted token
        top_pred = alternatives[0].get("token", "")

        actual_pos = pos_tag(actual)
        expected_pos = pos_tag(top_pred)

        sub_matrix[actual_pos][expected_pos] += 1

        if abs(s2) > 0.5:  # meaningful deviation
            pos_s2[(actual_pos, expected_pos)].append(s2)
            era_subs[era][actual_pos][expected_pos] += 1

            if s2 > 3.0:  # high-S2 substitutions
                all_sub_examples.append({
                    "s2": s2,
                    "actual": actual,
                    "expected": top_pred,
                    "actual_pos": actual_pos,
                    "expected_pos": expected_pos,
                    "poem": title,
                    "author": author,
                    "era": era,
                })

        analyzed += 1

print(f"Analyzed {analyzed} tokens across {total_tokens} total")

# --- Summary statistics ---
pos_labels = ["NOUN", "VERB", "ADJ", "ADV", "DET", "ADP", "PRON", "CCONJ", "PUNCT", "NEWLINE", "OTHER", "NUM"]

print("\n=== POS Substitution Matrix (actual → expected) ===")
print("Format: what the poet wrote (rows) → what GPT-2 predicted (columns)")
print()

# Get all observed POS
all_pos = sorted(set(list(sub_matrix.keys()) + [p for v in sub_matrix.values() for p in v.keys()]))
key_pos = [p for p in ["NOUN", "VERB", "ADJ", "ADV", "DET", "ADP", "PRON", "PUNCT", "NEWLINE", "OTHER"] if p in all_pos]

header = f"{'Actual→Expected':<16}" + "".join(f"{p:<10}" for p in key_pos)
print(header)
for ap in key_pos:
    row = f"{ap:<16}"
    total_row = sum(sub_matrix[ap].values())
    for ep in key_pos:
        cnt = sub_matrix[ap].get(ep, 0)
        pct = cnt / total_row * 100 if total_row > 0 else 0
        row += f"{pct:>6.1f}%   "
    print(row)

# --- Most surprising substitution patterns ---
print("\n=== POS pairs with highest avg S2 (poet chose X when GPT-2 expected Y) ===")
pair_stats = []
for (ap, ep), s2_vals in pos_s2.items():
    if len(s2_vals) >= 5:  # min sample
        pair_stats.append((ap, ep, statistics.mean(s2_vals), len(s2_vals)))
pair_stats.sort(key=lambda x: -x[2])
for ap, ep, avg, n in pair_stats[:20]:
    print(f"  Poet wrote {ap:<8} when GPT-2 expected {ep:<8} → avg S2={avg:+.2f}, n={n}")

# --- By era: dominant substitution type ---
print("\n=== Per-era dominant POS substitution strategy ===")
era_dominant = {}
for era, subs in era_subs.items():
    total = sum(sum(v.values()) for v in subs.values())
    if total < 20:
        continue
    # Find most common non-identity substitution
    best = None
    best_n = 0
    for ap, by_ep in subs.items():
        for ep, cnt in by_ep.items():
            if ap != ep and cnt > best_n:
                best_n = cnt
                best = (ap, ep, cnt)
    if best:
        era_dominant[era] = (best[0], best[1], best[2] / total * 100)

for era, (ap, ep, pct) in sorted(era_dominant.items(), key=lambda x: -x[1][2]):
    print(f"  {era:<25} → wrote {ap:<8} when expected {ep:<8} ({pct:.1f}%)")

# --- High-S2 examples with POS mismatch ---
print(f"\n=== Top high-S2 grammatical substitutions (poet changed the POS) ===")
mismatch = [e for e in all_sub_examples if e["actual_pos"] != e["expected_pos"]]
mismatch.sort(key=lambda x: -x["s2"])
for e in mismatch[:20]:
    print(f"  S2={e['s2']:+.1f} | '{e['actual']}' ({e['actual_pos']}) where '{e['expected']}' ({e['expected_pos']}) expected")
    print(f"         [{e['author']}, '{e['poem']}', era={e['era']}]")

# --- Identity vs. Non-identity substitutions by era ---
print("\n=== POS identity rate by era (how often poet keeps the expected POS) ===")
era_identity = {}
for era, subs in era_subs.items():
    total = sum(sum(v.values()) for v in subs.values())
    identity = sum(subs[p].get(p, 0) for p in subs)
    if total >= 20:
        era_identity[era] = (identity / total * 100, total)

for era, (pct, n) in sorted(era_identity.items(), key=lambda x: x[1][0]):
    print(f"  {era:<25} POS-identity={pct:.1f}%, n={n}")

# Save results
output = {
    "sub_matrix": {ap: dict(by_ep) for ap, by_ep in sub_matrix.items()},
    "pos_s2_avg": {f"{ap}→{ep}": statistics.mean(vals) for (ap, ep), vals in pos_s2.items() if len(vals) >= 3},
    "era_identity": {era: pct for era, (pct, n) in era_identity.items()},
    "high_s2_mismatches": sorted(mismatch, key=lambda x: -x["s2"])[:50],
}
with open("/home/user/s2lab/results/grammar_of_unsaid.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nResults saved to results/grammar_of_unsaid.json")
