"""
Semantic Field of Poetic Surprise

When poets deviate from GPT-2's predictions (high S2), what SEMANTIC FIELDS
do their chosen words belong to? Are there semantic domains that poets
systematically prefer when they choose to be surprising?

This experiment filters out the stanza-break artifact (tokens where GPT-2's
top alternative is a newline) and asks: of the remaining genuine deviations,
what kinds of words do poets reach for?

Method:
  1. Load corpus_results.json
  2. Filter high-S2 tokens (S2 >= 1.5) where top alternative is NOT a newline
  3. Categorize chosen tokens by semantic field
  4. Compare rates vs. baseline (all poetry tokens)
  5. Identify which semantic fields poets are most likely to choose when surprising
"""

import json
from collections import Counter, defaultdict

RESULT_PATH = "results/corpus_results.json"
S2_THRESHOLD = 1.5   # moderate threshold to get enough clean examples
MIN_LEN = 2

# ── Semantic field lexicons ───────────────────────────────────────────────────

SEMANTIC_FIELDS = {
    "BODY": {
        "hand", "hands", "eye", "eyes", "mouth", "blood", "heart", "bone", "bones",
        "skin", "face", "body", "breast", "finger", "fingers", "foot", "feet",
        "head", "hair", "lip", "lips", "tongue", "ear", "ears", "throat",
        "arm", "arms", "leg", "legs", "back", "neck", "chest", "shoulder",
        "knee", "knees", "jaw", "brow", "wrist", "palm", "fist", "heel",
        "spine", "skull", "nerve", "nerves", "flesh", "vein", "veins",
        "breath", "breathing", "pulse", "muscle", "muscles", "belly",
    },
    "NATURE": {
        "stone", "stones", "leaf", "leaves", "tree", "trees", "bird", "birds",
        "water", "earth", "wind", "sky", "grass", "flower", "flowers",
        "river", "ocean", "sea", "lake", "hill", "mountain", "forest",
        "snow", "rain", "cloud", "clouds", "sand", "dust", "mud", "rock",
        "branch", "root", "roots", "seed", "seeds", "stream", "shore",
        "wave", "waves", "field", "fields", "valley", "shore", "coast",
        "soil", "soil", "feather", "feathers", "petal", "petals", "moss",
        "bark", "thorn", "thorns", "web", "wing", "wings", "nest",
    },
    "DEATH_DARK": {
        "death", "dead", "dying", "die", "dies", "died", "grave", "graves",
        "dark", "darkness", "shadow", "shadows", "night", "ash", "ashes",
        "ruin", "ruins", "void", "absence", "loss", "lost", "gone",
        "end", "ending", "ended", "silence", "silent", "cold", "hollow",
        "fallen", "fall", "failing", "faded", "fading", "ghost", "ghosts",
        "burial", "corpse", "bones", "skull", "tomb", "mourning",
        "grief", "sorrow", "wound", "wounds", "pain", "suffer",
        "empty", "emptiness", "alone", "loneliness", "lonely",
    },
    "LIGHT_SACRED": {
        "light", "bright", "sun", "sunlight", "fire", "gold", "golden",
        "white", "pure", "purity", "God", "heaven", "divine", "holy",
        "sacred", "grace", "angel", "angels", "spirit", "soul", "eternal",
        "glory", "shine", "shining", "shines", "glowing", "glow",
        "star", "stars", "moon", "moonlight", "radiance", "radiant",
        "flame", "flames", "burning", "burn", "blaze",
    },
    "EMOTION": {
        "love", "fear", "joy", "hope", "desire", "longing", "yearning",
        "anger", "rage", "terror", "wonder", "awe", "shame", "pride",
        "envy", "jealousy", "pity", "mercy", "compassion", "tenderness",
        "hatred", "hate", "anguish", "despair", "ecstasy", "bliss",
        "sadness", "happiness", "gladness", "anxiety", "dread",
        "passion", "emotion", "feeling", "heart", "felt", "feeling",
    },
    "ABSTRACT_TIME": {
        "time", "memory", "dream", "truth", "meaning", "idea", "thought",
        "past", "future", "moment", "eternity", "history", "story",
        "mind", "soul", "spirit", "self", "nothing", "something",
        "everything", "always", "never", "once", "still", "ever",
        "world", "life", "existence", "being", "becoming",
        "power", "force", "will", "fate", "chance", "purpose",
        "beauty", "art", "music", "poetry", "language", "word", "words",
    },
    "COLOR": {
        "red", "blue", "green", "black", "white", "yellow", "orange",
        "purple", "pink", "brown", "gray", "grey", "silver", "golden",
        "crimson", "scarlet", "azure", "indigo", "violet", "amber",
        "ivory", "ebony", "pale", "dark", "bright", "vivid", "emerald",
        "rose", "russet", "sable", "tawny",
    },
    "SOUND_MUSIC": {
        "sound", "sounds", "voice", "voices", "song", "songs", "sing",
        "singing", "sung", "noise", "silence", "quiet", "whisper",
        "shout", "cry", "cries", "call", "calls", "echo", "echoes",
        "music", "melody", "rhythm", "beat", "note", "notes", "chord",
        "bell", "bells", "drum", "drums", "hum", "murmur", "roar",
    },
    "MOTION": {
        "fall", "falls", "falling", "fell", "rise", "rises", "rising",
        "rose", "run", "runs", "running", "ran", "walk", "walking",
        "walked", "fly", "flies", "flying", "flew", "turn", "turning",
        "turned", "move", "moving", "moved", "drift", "drifting",
        "flow", "flowing", "flows", "fled", "flee", "chase", "follow",
        "climb", "climbing", "sink", "sinking", "sank",
    },
    "NUMBER_QUANTITY": {
        "one", "two", "three", "four", "five", "ten", "hundred", "thousand",
        "all", "every", "each", "many", "few", "some", "any", "half",
        "whole", "more", "less", "most", "least", "much", "little",
        "single", "double", "once", "twice",
    },
}

def normalize(tok: str) -> str:
    return tok.strip().lower()

def classify_semantic(tok: str) -> list:
    """Return list of all matching semantic fields (a token can belong to multiple)."""
    n = normalize(tok)
    matches = []
    for field, words in SEMANTIC_FIELDS.items():
        if n in words:
            matches.append(field)
    return matches

def is_stanza_break(top_alt: str) -> bool:
    """Return True if the top alternative is a newline / stanza-break token."""
    n = normalize(top_alt)
    return n.startswith("\n") or n == "" or n == "\n"

# ── Load corpus ───────────────────────────────────────────────────────────────

with open(RESULT_PATH) as f:
    corpus = json.load(f)

print(f"Loaded {len(corpus)} texts\n")

# ── Collect all tokens (baseline) and high-S2 tokens (clean) ─────────────────

baseline_tokens = []    # all content tokens in poetry
high_s2_tokens = []     # clean high-S2 (not stanza-break artifact)
stanza_artifact_tokens = []  # high-S2 tokens flagged as stanza-break artifact

poetry_texts = [p for p in corpus if p["metadata"].get("era", "") != "control"]
control_texts = [p for p in corpus if p["metadata"].get("era", "") == "control"]

for poem in poetry_texts:
    meta = poem["metadata"]
    for tok in poem.get("tokens", []):
        token_text = tok.get("token", "")
        s2 = tok.get("s2", 0.0)
        alts = tok.get("alternatives", [])
        n = normalize(token_text)

        # Only look at alphabetic tokens of length >= MIN_LEN
        if len(n) < MIN_LEN or not any(c.isalpha() for c in n):
            continue

        baseline_tokens.append(token_text)

        if s2 >= S2_THRESHOLD and alts:
            top_alt = alts[0]["token"]
            if is_stanza_break(top_alt):
                stanza_artifact_tokens.append({
                    "token": token_text, "s2": s2, "top_alt": top_alt,
                    "author": meta["author"], "era": meta.get("era", ""),
                })
            else:
                high_s2_tokens.append({
                    "token": token_text, "s2": s2, "top_alt": top_alt,
                    "top_alt_prob": alts[0].get("prob", 0),
                    "author": meta["author"], "era": meta.get("era", ""),
                    "title": meta["title"],
                    "context_before": tok.get("context_before", ""),
                })

print(f"Baseline (all poetry content tokens): {len(baseline_tokens)}")
print(f"High-S2 clean (S2≥{S2_THRESHOLD}, not stanza-break): {len(high_s2_tokens)}")
print(f"High-S2 stanza artifact (filtered out): {len(stanza_artifact_tokens)}")
artifact_pct = 100 * len(stanza_artifact_tokens) / max(len(stanza_artifact_tokens) + len(high_s2_tokens), 1)
print(f"Artifact fraction: {artifact_pct:.1f}%\n")

# ── 1. Semantic field rates in baseline vs. high-S2 ──────────────────────────

print("=" * 65)
print("1. SEMANTIC FIELD RATES: Baseline vs. High-S2 (clean)")
print("=" * 65)

baseline_field_counts = Counter()
for tok in baseline_tokens:
    for field in classify_semantic(tok):
        baseline_field_counts[field] += 1

high_s2_field_counts = Counter()
for rec in high_s2_tokens:
    for field in classify_semantic(rec["token"]):
        high_s2_field_counts[field] += 1

total_base = len(baseline_tokens)
total_high = len(high_s2_tokens)

print(f"\n{'Semantic Field':<22} {'Baseline%':>10} {'HighS2%':>10} {'Lift':>8}")
print("-" * 55)
field_lifts = []
for field in sorted(SEMANTIC_FIELDS.keys()):
    base_pct = 100 * baseline_field_counts[field] / max(total_base, 1)
    high_pct = 100 * high_s2_field_counts[field] / max(total_high, 1)
    lift = high_pct / max(base_pct, 0.001)
    field_lifts.append((field, base_pct, high_pct, lift))

field_lifts.sort(key=lambda x: -x[3])
for field, base_pct, high_pct, lift in field_lifts:
    marker = " ◄ OVER" if lift > 1.5 else (" ▼ UNDER" if lift < 0.7 else "")
    print(f"{field:<22} {base_pct:>9.2f}% {high_pct:>9.2f}% {lift:>7.2f}x{marker}")

# ── 2. What did GPT-2 expect at high-S2 moments? ────────────────────────────

print("\n" + "=" * 65)
print("2. WHAT DID GPT-2 EXPECT? (top suppressed tokens, clean)")
print("=" * 65)

suppressed_counter = Counter()
for rec in high_s2_tokens:
    suppressed_counter[rec["top_alt"].strip()] += 1

print("\nMost-suppressed alternatives (what model wanted but poet chose against):")
print(f"{'Token':>14} {'Count':>8}")
print("-" * 25)
for tok, cnt in suppressed_counter.most_common(20):
    fields = ", ".join(classify_semantic(tok)) or "—"
    print(f"{tok!r:>14} {cnt:>8}    [{fields}]")

# ── 3. Examples: each semantic field's most surprising tokens ─────────────────

print("\n" + "=" * 65)
print("3. MOST SURPRISING TOKENS BY SEMANTIC FIELD")
print("=" * 65)

for field, _, _, lift in field_lifts:
    examples = [r for r in high_s2_tokens if field in classify_semantic(r["token"])]
    examples.sort(key=lambda r: -r["s2"])
    if not examples:
        print(f"\n── {field} (no examples) ──")
        continue
    print(f"\n── {field} (lift={lift:.2f}x, n={len(examples)}) ──")
    for ex in examples[:4]:
        ctx = ex["context_before"][-25:] if ex["context_before"] else "(start)"
        print(
            f"  [{ex['author'][:16]:16}] …{ctx!r}→ chose {ex['token']!r:12} "
            f"(expected {ex['top_alt']!r:10}, S2={ex['s2']:.2f})"
        )

# ── 4. ERA-level semantic field profiles ─────────────────────────────────────

print("\n" + "=" * 65)
print("4. ERA-LEVEL SEMANTIC FIELD PROFILES")
print("=" * 65)

era_high_s2 = defaultdict(list)
for rec in high_s2_tokens:
    era_high_s2[rec["era"]].append(rec)

era_field_matrix = {}
for era, records in era_high_s2.items():
    if len(records) < 10:
        continue
    field_cnt = Counter()
    for r in records:
        for f in classify_semantic(r["token"]):
            field_cnt[f] += 1
    total = len(records)
    era_field_matrix[era] = {f: 100 * c / total for f, c in field_cnt.items()}

# Print as table: eras as rows, top fields as columns
top_fields = [f for f, _, _, _ in field_lifts[:6]]
header = f"{'Era':<22}" + "".join(f"{f[:7]:>10}" for f in top_fields)
print(f"\n{header}")
print("-" * (22 + 10 * len(top_fields)))
for era in sorted(era_field_matrix.keys(), key=lambda e: -sum(era_field_matrix[e].values())):
    row = f"{era:<22}"
    for f in top_fields:
        val = era_field_matrix[era].get(f, 0.0)
        row += f"{val:>9.1f}%"
    print(row)

# ── 5. Poet-level semantic surprise preferences ──────────────────────────────

print("\n" + "=" * 65)
print("5. POET SEMANTIC SURPRISE PREFERENCES (≥20 clean high-S2 tokens)")
print("=" * 65)

poet_high_s2 = defaultdict(list)
for rec in high_s2_tokens:
    poet_high_s2[rec["author"]].append(rec)

print(f"\n{'Author':<24} {'n':>5} {'TopField1':<18} {'TopField2':<18}")
print("-" * 70)
rows = []
for author, records in poet_high_s2.items():
    if len(records) < 20:
        continue
    field_cnt = Counter()
    for r in records:
        for f in classify_semantic(r["token"]):
            field_cnt[f] += 1
    top = field_cnt.most_common(2)
    f1 = f"{top[0][0]}({top[0][1]})" if len(top) > 0 else "—"
    f2 = f"{top[1][0]}({top[1][1]})" if len(top) > 1 else "—"
    avg_s2 = sum(r["s2"] for r in records) / len(records)
    rows.append((author, len(records), avg_s2, f1, f2))

rows.sort(key=lambda x: -x[2])
for author, n, avg_s2, f1, f2 in rows:
    print(f"{author:<24} {n:>5}   {f1:<18} {f2:<18}  (avg S2={avg_s2:.2f})")

print("\n\nDone.")
