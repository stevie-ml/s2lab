"""
Arc Vocabulary Signature: What Do Poets Write at Their Climactic Moments?

Builds on:
- findings/s2_arc_typology.md (established 5 arc types: DECLINE, ASCENT, U_SHAPE, ARCH, FLAT)
- findings/counter_trend_escalation.md (escalation is rare; settlement is universal law)

Research Question:
Are the VOCABULARIES of high-S2 moments different depending on where in the poem they occur?

Hypothesis:
- DECLINE poems (front-loaded): opening surprises are scene-setting, grand, abstract
- ASCENT poems (back-loaded): closing surprises are specific, concrete, embodied
- ARCH poems (mid-peak): middle surprises are transitional, processual
- U_SHAPE poems (mid-trough): recovers with surprising vocabulary near the end

By comparing the high-S2 vocabulary per arc type, per quarter, we can answer:
Is there a "grammar of placement" — are certain words structurally confined to surprise roles
at the beginning vs end of poems?
"""

import json
import statistics
from pathlib import Path
from collections import defaultdict

results_path = Path("results/corpus_results.json")
arc_path = Path("results/s2_arc_typology.json")

with open(results_path) as f:
    corpus = json.load(f)
with open(arc_path) as f:
    arc_data = json.load(f)

# Build arc lookup: (title.lower(), author.lower()) -> arc_type
arc_lookup = {}
for p in arc_data["poems"]:
    key = (p["title"].strip().lower(), p["author"].strip().lower())
    arc_lookup[key] = p["arc"]

NEWLINE_THRESHOLD = 0.9
S2_THRESHOLD = 2.0  # only "real" surprises

def get_clean_tokens(tokens):
    return [t for t in tokens
            if t.get("p_newline", 0) < NEWLINE_THRESHOLD
            and t.get("token", "").strip() not in ["", "<|endoftext|>"]]

# For each arc type, collect: per-quarter high-S2 token lists
# Quarter = {Q1, Q2, Q3, Q4} split by token position

arc_quarter_tokens = defaultdict(lambda: defaultdict(list))  # arc -> quarter -> [(token, s2)]
arc_all_tokens = defaultdict(list)  # arc -> [(token, s2, quarter)]

poems_by_arc = defaultdict(list)
n_matched = 0
n_total = 0

for item in corpus:
    meta = item.get("metadata", {})
    if meta.get("era") == "control":
        continue
    n_total += 1
    title = meta.get("title", "").strip()
    author = meta.get("author", "").strip()
    key = (title.lower(), author.lower())
    arc = arc_lookup.get(key)
    if arc is None:
        continue
    n_matched += 1

    tokens = get_clean_tokens(item.get("tokens", []))
    n = len(tokens)
    if n < 20:
        continue

    q_size = n // 4
    for i, t in enumerate(tokens):
        # assign to quarter 1-4
        if i < q_size:
            q = "Q1"
        elif i < 2 * q_size:
            q = "Q2"
        elif i < 3 * q_size:
            q = "Q3"
        else:
            q = "Q4"

        s2 = t.get("s2", 0)
        tok = t.get("token", "").strip().lower()
        if not tok or tok in {".", ",", "!", "?", ";", ":", "'", '"', "-", "(", ")", "\n"}:
            continue

        if s2 > S2_THRESHOLD:
            arc_quarter_tokens[arc][q].append((tok, s2))
            arc_all_tokens[arc].append((tok, s2, q))

        poems_by_arc[arc].append(meta.get("title"))

print(f"Total poems: {n_total}")
print(f"Matched to arc type: {n_matched}")
print(f"Arc type distribution: {dict((k, len(set(v))) for k, v in poems_by_arc.items())}")
print()

# For each arc type, find the PEAK QUARTER (the climactic quarter for that arc type)
arc_peak_quarter = {
    "DECLINE": "Q1",   # front-loaded: peak is at start
    "ASCENT":  "Q4",   # back-loaded: peak is at end
    "ARCH":    "Q2",   # mid-peak: peak in second quarter (or Q3)
    "U_SHAPE": "Q4",   # mid-trough: recovery at end
    "FLAT":    None,   # no structural peak
}

print("=" * 70)
print("PART 1: Vocabulary at the Arc's Peak Quarter")
print("=" * 70)
print()

arc_peak_vocab = {}  # arc -> sorted token list at peak quarter

for arc in ["DECLINE", "ASCENT", "ARCH", "U_SHAPE"]:
    peak_q = arc_peak_quarter[arc]
    tokens_at_peak = arc_quarter_tokens[arc][peak_q]
    if not tokens_at_peak:
        continue

    # frequency × mean S2 score
    freq = defaultdict(list)
    for tok, s2 in tokens_at_peak:
        freq[tok].append(s2)

    ranked = sorted(freq.items(), key=lambda x: len(x[1]), reverse=True)
    arc_peak_vocab[arc] = ranked

    print(f"\n--- {arc} poems | Peak Quarter: {peak_q} | n high-S2 tokens: {len(tokens_at_peak)} ---")
    print(f"{'Token':<20} {'Count':>6} {'Avg S₂':>8} {'Max S₂':>8}")
    print("-" * 48)
    for tok, s2_list in ranked[:20]:
        print(f"{tok:<20} {len(s2_list):>6} {statistics.mean(s2_list):>8.2f} {max(s2_list):>8.2f}")

print()
print("=" * 70)
print("PART 2: Tokens EXCLUSIVE or DOMINANT in One Arc Type at Its Peak Quarter")
print("=" * 70)
print()

# For each token appearing in peak quarters, what fraction of its appearances
# come from each arc type? Tokens with high exclusivity to one arc are most diagnostic.

# Build global frequency across all arcs at their respective peak quarters
global_token_arc_counts = defaultdict(lambda: defaultdict(int))
for arc in ["DECLINE", "ASCENT", "ARCH", "U_SHAPE"]:
    peak_q = arc_peak_quarter[arc]
    for tok, s2 in arc_quarter_tokens[arc][peak_q]:
        global_token_arc_counts[tok][arc] += 1

# For tokens that appear at least 3 times in some arc, compute dominance score
print("Tokens most exclusive to ASCENT peaks (back-loaded climax):")
ascent_exclusive = []
for tok, arc_counts in global_token_arc_counts.items():
    total = sum(arc_counts.values())
    if total < 3:
        continue
    ascent_pct = arc_counts.get("ASCENT", 0) / total
    if arc_counts.get("ASCENT", 0) >= 2:
        ascent_exclusive.append((tok, ascent_pct, total, arc_counts.get("ASCENT", 0)))

ascent_exclusive.sort(key=lambda x: x[1], reverse=True)
print(f"{'Token':<20} {'ASCENT%':>8} {'ASCENT n':>9} {'Total n':>8}")
print("-" * 50)
for tok, pct, total, ascent_n in ascent_exclusive[:20]:
    print(f"{tok:<20} {pct*100:>7.1f}% {ascent_n:>9} {total:>8}")

print()
print("Tokens most exclusive to DECLINE peaks (front-loaded surprise):")
decline_exclusive = []
for tok, arc_counts in global_token_arc_counts.items():
    total = sum(arc_counts.values())
    if total < 3:
        continue
    decline_pct = arc_counts.get("DECLINE", 0) / total
    if arc_counts.get("DECLINE", 0) >= 2:
        decline_exclusive.append((tok, decline_pct, total, arc_counts.get("DECLINE", 0)))

decline_exclusive.sort(key=lambda x: x[1], reverse=True)
print(f"{'Token':<20} {'DECLINE%':>9} {'DECLINE n':>10} {'Total n':>8}")
print("-" * 50)
for tok, pct, total, dec_n in decline_exclusive[:20]:
    print(f"{tok:<20} {pct*100:>8.1f}% {dec_n:>10} {total:>8}")

print()
print("=" * 70)
print("PART 3: Mean S2 at Each Quarter by Arc Type (the information landscape)")
print("=" * 70)
print()

# Average S2 at EACH quarter for EACH arc type
# This shows: does Q4 of ASCENT poems have higher S2 than Q4 of DECLINE poems?
arc_q_all_s2 = defaultdict(lambda: defaultdict(list))  # arc -> quarter -> [s2 values]

for item in corpus:
    meta = item.get("metadata", {})
    if meta.get("era") == "control":
        continue
    title = meta.get("title", "").strip()
    author = meta.get("author", "").strip()
    key = (title.lower(), author.lower())
    arc = arc_lookup.get(key)
    if arc is None:
        continue
    tokens = get_clean_tokens(item.get("tokens", []))
    n = len(tokens)
    if n < 20:
        continue
    q_size = n // 4
    for i, t in enumerate(tokens):
        if i < q_size:
            q = "Q1"
        elif i < 2 * q_size:
            q = "Q2"
        elif i < 3 * q_size:
            q = "Q3"
        else:
            q = "Q4"
        arc_q_all_s2[arc][q].append(t.get("s2", 0))

print(f"{'Arc Type':<12} {'Q1 (mean S₂)':>14} {'Q2':>8} {'Q3':>8} {'Q4':>8} {'Peak Quarter':>14}")
print("-" * 70)
for arc in ["DECLINE", "ASCENT", "ARCH", "U_SHAPE", "FLAT"]:
    q_means = {}
    for q in ["Q1", "Q2", "Q3", "Q4"]:
        vals = arc_q_all_s2[arc][q]
        q_means[q] = statistics.mean(vals) if vals else float("nan")
    peak = max(q_means, key=lambda q: q_means[q])
    row = f"{arc:<12} {q_means['Q1']:>14.3f} {q_means['Q2']:>8.3f} {q_means['Q3']:>8.3f} {q_means['Q4']:>8.3f} {peak:>14}"
    print(row)

print()
print("=" * 70)
print("PART 4: Semantic Character of Arc-Specific Surprise Words")
print("=" * 70)
print()

# Classify tokens into rough semantic categories for ASCENT Q4 vs DECLINE Q1
def categorize(token):
    tok = token.lower()
    # Sensory/concrete
    sensory = {"red", "blue", "green", "white", "black", "gold", "dark", "bright", "light",
               "cold", "warm", "hot", "soft", "hard", "heavy", "sweet", "sharp", "smooth",
               "stone", "rain", "snow", "fire", "water", "earth", "air", "sky", "sun",
               "blood", "bone", "eye", "hand", "face", "mouth", "heart", "body", "skin",
               "silence", "sound", "voice", "cry", "whisper", "shadow", "dream"}
    # Abstract/conceptual
    abstract = {"love", "death", "time", "life", "truth", "beauty", "hope", "fear",
                "soul", "spirit", "god", "fate", "thought", "mind", "feeling",
                "world", "nothing", "everything", "forever", "eternal"}
    # Verbs/action
    action = {"fall", "rise", "move", "run", "turn", "break", "make", "see",
              "know", "feel", "come", "go", "bring", "find", "hold", "take", "give",
              "wait", "stand", "walk", "fly", "float", "sing", "speak", "say"}
    # Structural/formal
    structural = {"the", "a", "an", "of", "in", "on", "at", "by", "for", "and",
                  "but", "or", "not", "no", "it", "is", "was", "been", "are", "were"}

    if tok in sensory:
        return "SENSORY"
    elif tok in abstract:
        return "ABSTRACT"
    elif tok in action:
        return "ACTION"
    elif tok in structural:
        return "STRUCTURAL"
    else:
        return "OTHER"

print("Semantic category breakdown at peak quarters:")
print(f"{'Arc':>10} {'Peak Q':>8} {'SENSORY':>9} {'ABSTRACT':>10} {'ACTION':>8} {'OTHER':>7}")
print("-" * 58)

for arc in ["DECLINE", "ASCENT", "ARCH", "U_SHAPE"]:
    peak_q = arc_peak_quarter[arc]
    tokens_at_peak = arc_quarter_tokens[arc][peak_q]
    if not tokens_at_peak:
        continue
    cats = defaultdict(int)
    for tok, s2 in tokens_at_peak:
        cats[categorize(tok)] += 1
    total = sum(cats.values())
    if total == 0:
        continue
    sensory_pct = 100 * cats["SENSORY"] / total
    abstract_pct = 100 * cats["ABSTRACT"] / total
    action_pct = 100 * cats["ACTION"] / total
    other_pct = 100 * cats["OTHER"] / total
    print(f"{arc:>10} {peak_q:>8} {sensory_pct:>8.1f}% {abstract_pct:>9.1f}% {action_pct:>7.1f}% {other_pct:>6.1f}%")

# --- Save results ---
output = {
    "n_poems_matched": n_matched,
    "n_poems_total": n_total,
    "arc_peak_quarters": arc_peak_quarter,
    "arc_peak_vocab": {
        arc: [{"token": tok, "count": len(s2s), "mean_s2": round(statistics.mean(s2s), 3), "max_s2": round(max(s2s), 3)}
              for tok, s2s in ranked[:30]]
        for arc, ranked in arc_peak_vocab.items()
    },
    "arc_q_means": {
        arc: {q: round(statistics.mean(arc_q_all_s2[arc][q]), 3) if arc_q_all_s2[arc][q] else None
              for q in ["Q1", "Q2", "Q3", "Q4"]}
        for arc in ["DECLINE", "ASCENT", "ARCH", "U_SHAPE", "FLAT"]
    },
    "ascent_exclusive_tokens": [
        {"token": tok, "ascent_pct": round(pct * 100, 1), "ascent_n": ascent_n, "total_n": total}
        for tok, pct, total, ascent_n in ascent_exclusive[:30]
    ],
    "decline_exclusive_tokens": [
        {"token": tok, "decline_pct": round(pct * 100, 1), "decline_n": dec_n, "total_n": total}
        for tok, pct, total, dec_n in decline_exclusive[:30]
    ],
}

with open("results/arc_vocabulary_signature.json", "w") as f:
    json.dump(output, f, indent=2)
print("\nSaved to results/arc_vocabulary_signature.json")
