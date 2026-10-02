"""
Imperative Mood and S2: Commands as Informational Disruptions

Research question: When poets issue direct commands — "Go, lovely rose",
"Do not go gentle", "Look on my works, ye Mighty" — what is the
information-theoretic profile? Imperative verbs suppress the grammatical
subject, creating a structural departure from GPT-2's training distribution
(dominated by declarative prose with explicit subjects).

Three hypotheses:
  H1: Imperative verbs ARE high-S2 — the suppressed subject makes them
      unexpected at clause-initial positions (GPT-2 expects "I go", not "Go")
  H2: The tokens FOLLOWING an imperative are high-entropy — commands open
      a wide possibility space for objects/complements
  H3: Apostrophic imperatives (addressing nature/death/abstractions, often
      featuring vocative O/Oh or archaic address) show HIGHER S2 than
      imperatives directed at humans

Method:
  - Detect imperative-likely instances: line-initial verb in base form
    (after newline or strong punctuation), drawn from curated verb list
  - Compare S2 at the imperative token vs. the same verb in non-imperative
    (mid-sentence) positions
  - Analyze the +1 to +3 entropy envelope after imperatives vs. baseline
  - Check for apostrophic context (O/Oh/thee/thou near the imperative)
"""

import json
import statistics
from collections import defaultdict

with open("results/corpus_results.json") as f:
    corpus = json.load(f)

# ── Imperative verb list ───────────────────────────────────────────────────────
# Verbs that appear frequently as imperatives in English poetry
# Base form only; we'll match case-insensitively
IMPERATIVE_VERBS = {
    # Motion / leaving / coming
    "go", "come", "fly", "rise", "fall", "run", "walk", "turn", "pass", "stay",
    "stand", "sit", "lie", "move", "return", "depart", "leave", "follow",
    # Attention / perception
    "look", "see", "hear", "watch", "listen", "behold", "mark", "note",
    "observe", "gaze", "glance",
    # Cognition / memory
    "think", "remember", "forget", "know", "consider", "understand", "learn",
    "imagine", "dream", "feel",
    # Speech / expression
    "say", "tell", "speak", "sing", "call", "cry", "name", "write",
    # Action
    "take", "give", "bring", "keep", "make", "let", "hold", "put", "seek",
    "find", "read", "love", "live", "die", "grow", "sleep", "wake",
    "open", "close", "fill", "pour", "build", "break", "weep", "laugh",
    # Invitatory
    "gather", "rise", "arise", "hark", "haste", "hasten", "pause",
}

# Apostrophe context markers
APOSTROPHE_MARKERS = {"o", "oh", "thee", "thou", "thy", "thine", "ye"}

def clean_token(t):
    """Strip GPT-2 space prefix and punctuation for matching."""
    return t.strip().lower().lstrip("Ġ").lstrip(" ").strip(".,;:!?\"'()-—")

def raw_surface(t):
    return t.strip().lstrip("Ġ").lstrip(" ")

def is_artifact(td):
    return td.get("p_newline", 0) >= 0.9

# ── Data collection ────────────────────────────────────────────────────────────
# For each token in the corpus that is:
#   (a) an imperative candidate: in IMPERATIVE_VERBS AND at line-initial position
#   (b) a declarative candidate: same verb but NOT line-initial
# We collect S2 windows.

imperative_instances = []   # {verb, s2, entropy, window, poem, author, era, year, apostrophic}
declarative_instances = []  # {verb, s2, entropy, window, poem, author, era, year}
baseline_s2 = []
baseline_entropy = []

for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]

    if meta.get("era") in ["control", "cliche_control"]:
        continue
    if meta.get("language", "en") not in ["en", "english", None]:
        continue

    # Build clean sequence (no artifacts)
    clean_seq = []
    for i, t in enumerate(tokens):
        if not is_artifact(t):
            clean_seq.append((i, t))
            baseline_s2.append(t["s2"])
            baseline_entropy.append(t["entropy"])

    poem_info = {
        "poem": meta.get("title", "?"),
        "author": meta.get("author", "?"),
        "era": meta.get("era", "?"),
        "year": meta.get("year", 0),
    }

    for seq_pos, (orig_idx, t) in enumerate(clean_seq):
        ctext = clean_token(t["token"])
        if ctext not in IMPERATIVE_VERBS:
            continue

        # Determine if this looks like an imperative position:
        # "line-initial" = immediately after a newline token (p_newline >= 0.9)
        # or at position 0, or immediately after strong punctuation (. ! ; :)
        is_line_initial = False

        # Check if the ORIGINAL token just before this one (including artifacts) is a newline
        if orig_idx > 0:
            prev_orig = tokens[orig_idx - 1]
            if prev_orig.get("p_newline", 0) >= 0.9:
                is_line_initial = True
            # Also: previous token ends in . ! ; : or is opening punctuation
            prev_surf = raw_surface(prev_orig.get("token", "")).rstrip()
            if prev_surf and prev_surf[-1] in ".!;:,":
                # comma is debatable but allow it (e.g. "roses are red, go away")
                is_line_initial = True
        else:
            is_line_initial = True  # Very first token of poem

        # Check apostrophic context: within ±3 tokens look for apostrophe markers
        apostrophic = False
        for offset in range(-3, 4):
            idx2 = seq_pos + offset
            if 0 <= idx2 < len(clean_seq):
                if clean_token(clean_seq[idx2][1]["token"]) in APOSTROPHE_MARKERS:
                    apostrophic = True
                    break

        # Extract S2 window: positions -2..+3
        window = []
        for offset in range(-2, 4):
            idx2 = seq_pos + offset
            if 0 <= idx2 < len(clean_seq):
                tok = clean_seq[idx2][1]
                window.append({
                    "offset": offset,
                    "token": raw_surface(tok["token"]),
                    "s2": tok["s2"],
                    "entropy": tok["entropy"],
                    "surprisal": tok.get("surprisal", None),
                })
            else:
                window.append({"offset": offset, "token": None, "s2": None, "entropy": None})

        record = {
            "verb": ctext,
            "s2": t["s2"],
            "entropy": t["entropy"],
            "surprisal": t.get("surprisal"),
            "window": window,
            "apostrophic": apostrophic,
            **poem_info,
        }

        if is_line_initial:
            imperative_instances.append(record)
        else:
            declarative_instances.append(record)

# ── Analysis ──────────────────────────────────────────────────────────────────
base_mean_s2 = statistics.mean(baseline_s2)
base_mean_h  = statistics.mean(baseline_entropy)
base_pos_pct = sum(1 for s in baseline_s2 if s > 0) / len(baseline_s2) * 100

print(f"Corpus baseline: N={len(baseline_s2):,} | mean S2={base_mean_s2:.3f} | mean H={base_mean_h:.3f} | +S2%={base_pos_pct:.1f}%")
print(f"Imperative instances: {len(imperative_instances)}")
print(f"Declarative instances (same verbs, mid-sentence): {len(declarative_instances)}")
print()

# ── H1: Imperative vs. Declarative S2 ─────────────────────────────────────────
print("=== H1: IMPERATIVE vs. DECLARATIVE VERB POSITION ===")
imp_s2 = [x["s2"] for x in imperative_instances]
dec_s2 = [x["s2"] for x in declarative_instances]

if imp_s2 and dec_s2:
    imp_mean = statistics.mean(imp_s2)
    dec_mean = statistics.mean(dec_s2)
    imp_pos  = sum(1 for s in imp_s2 if s > 0) / len(imp_s2) * 100
    dec_pos  = sum(1 for s in dec_s2 if s > 0) / len(dec_s2) * 100
    imp_h    = statistics.mean([x["entropy"] for x in imperative_instances])
    dec_h    = statistics.mean([x["entropy"] for x in declarative_instances])

    print(f"{'':30} {'N':>6} {'mean S2':>9} {'ΔS2':>8} {'+S2%':>7} {'mean H':>8}")
    print(f"{'Imperative (line-initial verb)':30} {len(imp_s2):>6} {imp_mean:>9.3f} {imp_mean - base_mean_s2:>+8.3f} {imp_pos:>7.1f} {imp_h:>8.3f}")
    print(f"{'Declarative (same verbs, mid-sent)':30} {len(dec_s2):>6} {dec_mean:>9.3f} {dec_mean - base_mean_s2:>+8.3f} {dec_pos:>7.1f} {dec_h:>8.3f}")
    print(f"{'Baseline (all poetry tokens)':30} {len(baseline_s2):>6} {base_mean_s2:>9.3f} {'':>8} {base_pos_pct:>7.1f} {base_mean_h:>8.3f}")
print()

# ── H2: Entropy envelope after imperatives ────────────────────────────────────
print("=== H2: S2 AND ENTROPY ENVELOPE AFTER IMPERATIVES ===")
offsets = [-2, -1, 0, 1, 2, 3]
offset_labels = ["-2", "-1", "IMP", "+1", "+2", "+3"]

# Imperative window
print("\nImperative windows (mean S2 per offset):")
print(f"{'Offset':>8}", end="")
for lbl in offset_labels:
    print(f"  {lbl:>8}", end="")
print()

for label, instances in [("Imperative", imperative_instances), ("Declarative", declarative_instances)]:
    print(f"{label:>8}", end="")
    for off in offsets:
        vals = [r["window"][off + 2]["s2"] for r in instances
                if r["window"][off + 2]["s2"] is not None]
        if vals:
            print(f"  {statistics.mean(vals):>+8.3f}", end="")
        else:
            print(f"  {'N/A':>8}", end="")
    print()

print("\nEntropy envelope:")
for label, instances in [("Imperative", imperative_instances), ("Declarative", declarative_instances)]:
    print(f"{label:>8}", end="")
    for off in offsets:
        vals = [r["window"][off + 2]["entropy"] for r in instances
                if r["window"][off + 2]["entropy"] is not None]
        if vals:
            print(f"  {statistics.mean(vals):>8.3f}", end="")
        else:
            print(f"  {'N/A':>8}", end="")
    print()
print()

# ── H3: Apostrophic vs. non-apostrophic imperatives ──────────────────────────
print("=== H3: APOSTROPHIC vs. NON-APOSTROPHIC IMPERATIVES ===")
apost = [x for x in imperative_instances if x["apostrophic"]]
non_apost = [x for x in imperative_instances if not x["apostrophic"]]

if apost and non_apost:
    a_s2  = statistics.mean([x["s2"] for x in apost])
    na_s2 = statistics.mean([x["s2"] for x in non_apost])
    a_h   = statistics.mean([x["entropy"] for x in apost])
    na_h  = statistics.mean([x["entropy"] for x in non_apost])
    a_pos = sum(1 for x in apost if x["s2"] > 0) / len(apost) * 100
    na_pos = sum(1 for x in non_apost if x["s2"] > 0) / len(non_apost) * 100

    print(f"{'':25} {'N':>5} {'mean S2':>9} {'ΔS2':>8} {'+S2%':>7} {'mean H':>8}")
    print(f"{'Apostrophic imperative':25} {len(apost):>5} {a_s2:>9.3f} {a_s2 - base_mean_s2:>+8.3f} {a_pos:>7.1f} {a_h:>8.3f}")
    print(f"{'Non-apostrophic imperative':25} {len(non_apost):>5} {na_s2:>9.3f} {na_s2 - base_mean_s2:>+8.3f} {na_pos:>7.1f} {na_h:>8.3f}")
print()

# ── Top imperative verbs by S2 ────────────────────────────────────────────────
print("=== TOP IMPERATIVE VERBS BY MEAN S2 (N >= 3) ===")
verb_imp = defaultdict(list)
for x in imperative_instances:
    verb_imp[x["verb"]].append(x["s2"])

verb_stats = [(v, statistics.mean(s), len(s)) for v, s in verb_imp.items() if len(s) >= 3]
verb_stats.sort(key=lambda x: -x[1])

print(f"{'Verb':>12} {'N':>5} {'mean S2':>9}")
for verb, ms2, n in verb_stats[:15]:
    print(f"{verb:>12} {n:>5} {ms2:>9.3f}")
print()

# ── Lowest imperative verbs (most conformist imperatives) ─────────────────────
print("=== BOTTOM IMPERATIVE VERBS BY MEAN S2 (N >= 3) ===")
verb_stats_sorted_asc = sorted(verb_stats, key=lambda x: x[1])
for verb, ms2, n in verb_stats_sorted_asc[:10]:
    print(f"{verb:>12} {n:>5} {ms2:>9.3f}")
print()

# ── Era breakdown ──────────────────────────────────────────────────────────────
print("=== ERA BREAKDOWN: IMPERATIVE S2 ===")
era_imp = defaultdict(list)
era_dec = defaultdict(list)
for x in imperative_instances:
    era_imp[x["era"]].append(x["s2"])
for x in declarative_instances:
    era_dec[x["era"]].append(x["s2"])

all_eras = sorted(set(list(era_imp.keys()) + list(era_dec.keys())))
print(f"{'Era':>22} {'Imp N':>6} {'Imp S2':>8} {'Dec N':>6} {'Dec S2':>8} {'Gap':>8}")
for era in all_eras:
    i_list = era_imp.get(era, [])
    d_list = era_dec.get(era, [])
    if not i_list:
        continue
    i_mean = statistics.mean(i_list)
    d_mean = statistics.mean(d_list) if d_list else float("nan")
    gap = i_mean - d_mean if d_list else float("nan")
    print(f"{era:>22} {len(i_list):>6} {i_mean:>8.3f} {len(d_list):>6} {d_mean:>8.3f} {gap:>8.3f}")
print()

# ── Showcase examples ──────────────────────────────────────────────────────────
print("=== TOP 10 HIGHEST-S2 IMPERATIVE INSTANCES ===")
imperative_instances_sorted = sorted(imperative_instances, key=lambda x: -x["s2"])
for rec in imperative_instances_sorted[:10]:
    window_str = " ".join(
        ("[" + w["token"] + "]" if w["offset"] == 0 else w["token"])
        for w in rec["window"] if w["token"]
    )
    print(f"  S2={rec['s2']:+.2f} | {window_str[:60]:60} | {rec['author']}")
print()

print("=== TOP 10 LOWEST-S2 IMPERATIVE INSTANCES (most expected) ===")
for rec in imperative_instances_sorted[-10:]:
    window_str = " ".join(
        ("[" + w["token"] + "]" if w["offset"] == 0 else w["token"])
        for w in rec["window"] if w["token"]
    )
    print(f"  S2={rec['s2']:+.2f} | {window_str[:60]:60} | {rec['author']}")
print()

# ── What does GPT-2 want instead of the imperative? ──────────────────────────
print("=== TOP SUPPRESSED ALTERNATIVES AT IMPERATIVE POSITIONS ===")
# Collect the top alternative (what GPT-2 most wanted) for high-S2 imperatives
alt_counts = defaultdict(int)
for rec in imperative_instances:
    if rec["s2"] > 0:  # only surprising ones
        # Find the window entry at offset 0
        for w in rec["window"]:
            if w["offset"] == 0:
                # We don't have alternatives in the window directly --
                # need to look up from original corpus
                break

# Instead look up alternatives directly from original tokens
alt_counts_direct = defaultdict(lambda: {"count": 0, "total_prob": 0.0})
for text in corpus:
    meta = text["metadata"]
    if meta.get("era") in ["control", "cliche_control"]:
        continue
    if meta.get("language", "en") not in ["en", "english", None]:
        continue

    tokens = text["tokens"]
    for orig_idx, t in enumerate(tokens):
        if is_artifact(t):
            continue
        ctext = clean_token(t["token"])
        if ctext not in IMPERATIVE_VERBS:
            continue
        if t["s2"] <= 0:
            continue

        # Check if line-initial
        is_line_initial_check = False
        if orig_idx > 0:
            prev_orig = tokens[orig_idx - 1]
            if prev_orig.get("p_newline", 0) >= 0.9:
                is_line_initial_check = True
            prev_surf = raw_surface(prev_orig.get("token", "")).rstrip()
            if prev_surf and prev_surf[-1] in ".!;:":
                is_line_initial_check = True
        else:
            is_line_initial_check = True

        if is_line_initial_check:
            for alt in t.get("alternatives", [])[:3]:
                atxt = raw_surface(alt["token"]).lower().strip(".,;:?!")
                alt_counts_direct[atxt]["count"] += 1
                alt_counts_direct[atxt]["total_prob"] += alt["prob"]

alt_ranked = sorted(alt_counts_direct.items(), key=lambda x: -x[1]["count"])
print("What GPT-2 most wanted at line-initial imperative positions:")
print(f"{'Token':>15} {'Count':>7} {'Avg prob':>10}")
for tok, stats in alt_ranked[:15]:
    avg_p = stats["total_prob"] / stats["count"]
    print(f"{tok:>15} {stats['count']:>7} {avg_p:>10.3f}")
print()

print("Done.")
