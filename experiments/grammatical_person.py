"""
Grammatical Person and S₂: Does GPT-2's prose bias make lyric address surprising?

Hypothesis: GPT-2 is trained largely on 3rd-person prose (narration, news, web text).
Poetry's distinctive use of 1st-person "I" (lyric confession) and 2nd-person "you"
(direct address / apostrophe) should be systematically more surprising — higher S₂ —
because the model's prior skews toward 3rd-person continuations.

We test:
  1. Poem-level: Classify poems by dominant pronoun person. Do 1st/2nd-person poems
     have higher avg S₂ than 3rd-person or impersonal poems?
  2. Token-level: At positions where pronouns appear, what is their avg S₂?
     Do 1st/2nd-person pronouns have higher S₂ than 3rd-person pronouns?
  3. Alternatives analysis: When a poem uses "you", what does GPT-2 predict instead?
     When it uses "I", what are the alternatives?
  4. Person-switch moments: When the poem switches from one person to another,
     does S₂ spike?

Works purely from precomputed corpus_results.json — no GPU needed.
"""

import json
import re
from collections import defaultdict

# Pronoun sets (token-level: GPT-2 tokenizes with a leading space for most words)
FIRST_PERSON = {
    " i", " me", " my", " mine", " myself", " we", " us", " our", " ours", " ourselves",
    "i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves",
}
SECOND_PERSON = {
    " you", " your", " yours", " yourself", " yourselves",
    " thee", " thy", " thine", " thou", " thyself",
    "you", "your", "yours", "yourself", "yourselves",
    "thee", "thy", "thine", "thou", "thyself",
}
THIRD_PERSON = {
    " he", " him", " his", " himself",
    " she", " her", " hers", " herself",
    " they", " them", " their", " theirs", " themselves",
    " it", " its", " itself",
    "he", "him", "his", "himself",
    "she", "her", "hers", "herself",
    "they", "them", "their", "theirs", "themselves",
    "it", "its", "itself",
}


def classify_person(tokens):
    """Count pronoun occurrences; return dominant person and counts."""
    c1, c2, c3 = 0, 0, 0
    for t in tokens:
        tok_lower = t["token"].lower()
        if tok_lower in FIRST_PERSON:
            c1 += 1
        elif tok_lower in SECOND_PERSON:
            c2 += 1
        elif tok_lower in THIRD_PERSON:
            c3 += 1
    total = c1 + c2 + c3
    if total == 0:
        dominant = "impersonal"
    elif c1 >= c2 and c1 >= c3:
        dominant = "1st"
    elif c2 >= c1 and c2 >= c3:
        dominant = "2nd"
    else:
        dominant = "3rd"
    return dominant, c1, c2, c3


def person_of_token(tok_lower):
    if tok_lower in FIRST_PERSON:
        return "1st"
    if tok_lower in SECOND_PERSON:
        return "2nd"
    if tok_lower in THIRD_PERSON:
        return "3rd"
    return None


with open("results/corpus_results.json") as f:
    corpus = json.load(f)


# ── 1. POEM-LEVEL: classify by dominant person ───────────────────────────────

person_groups = defaultdict(list)   # person → list of poem summaries
person_poems  = defaultdict(list)   # person → list of (author, title, avg_s2)

for poem in corpus:
    meta   = poem["metadata"]
    tokens = poem["tokens"]
    is_en  = meta.get("language", "en") == "en"
    # Include control for baseline comparison
    if not is_en:
        continue

    dom, c1, c2, c3 = classify_person(tokens)
    avg_s2 = poem["summary"]["avg_s2"]
    std_s2 = poem["summary"].get("std_s2", 0)
    pos_ratio = poem["summary"]["pos_s2_ratio"]

    person_groups[dom].append({
        "avg_s2": avg_s2,
        "std_s2": std_s2,
        "pos_s2_ratio": pos_ratio,
        "era": meta.get("era", "unknown"),
        "c1": c1, "c2": c2, "c3": c3,
    })
    person_groups[dom + "_c1"].append(c1)
    person_groups[dom + "_c2"].append(c2)
    person_groups[dom + "_c3"].append(c3)
    person_poems[dom].append((meta["author"], meta["title"], avg_s2, meta.get("era", "?")))


def mean(xs):
    return sum(xs) / len(xs) if xs else float("nan")

def std(xs):
    if len(xs) < 2:
        return 0.0
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


print("=" * 65)
print("GRAMMATICAL PERSON AND S₂ IN POETRY")
print("=" * 65)

print("\n## 1. Poem-level S₂ by Dominant Grammatical Person\n")
print(f"{'Person':<12} {'n':>4} {'avg S₂':>8} {'std S₂':>8} {'pos%':>6}")
print("-" * 42)

order = ["1st", "2nd", "3rd", "impersonal"]
results_by_person = {}
for person in order:
    grp = person_groups[person]
    if not grp:
        continue
    avg_s2s = [g["avg_s2"] for g in grp]
    std_s2s = [g["std_s2"] for g in grp]
    pos_rs  = [g["pos_s2_ratio"] for g in grp]
    n = len(grp)
    m_avg = mean(avg_s2s)
    m_pos = mean(pos_rs)
    results_by_person[person] = {
        "n": n, "avg_s2": m_avg, "pos_ratio": m_pos,
        "raw_avg_s2": avg_s2s,
    }
    label = {"1st": "1st (I/we)", "2nd": "2nd (you/thee)",
             "3rd": "3rd (he/she)", "impersonal": "impersonal"}[person]
    print(f"{label:<12} {n:>4} {m_avg:>+8.3f} {mean(std_s2s):>8.3f} {m_pos*100:>5.1f}%")


# ── 2. TOKEN-LEVEL: pronoun S₂ values ────────────────────────────────────────

pronoun_s2 = defaultdict(list)           # "1st"/"2nd"/"3rd" → [s2 values]
pronoun_examples = defaultdict(list)     # person → [(token, s2, top_pred, author, title)]

for poem in corpus:
    meta   = poem["metadata"]
    tokens = poem["tokens"]
    if meta.get("language", "en") != "en":
        continue
    if meta.get("era") == "control":
        continue
    for t in tokens:
        tok_lower = t["token"].lower()
        person = person_of_token(tok_lower)
        if person is None:
            continue
        s2 = t["s2"]
        pronoun_s2[person].append(s2)
        top_pred = t["alternatives"][0]["token"] if t.get("alternatives") else "?"
        if abs(s2) > 2.0:
            pronoun_examples[person].append({
                "token": t["token"],
                "s2": s2,
                "surprisal": t["surprisal"],
                "entropy": t["entropy"],
                "top_pred": top_pred,
                "top_prob": t["alternatives"][0]["prob"] if t.get("alternatives") else 0,
                "author": meta["author"],
                "title": meta["title"],
                "context": t.get("context_before", "")[-60:],
            })

print("\n\n## 2. Token-level S₂ for Pronoun Choices\n")
print(f"{'Person':<6} {'n tokens':>9} {'avg S₂':>8} {'median':>8} {'pos%':>6}")
print("-" * 42)

import statistics

for person in ["1st", "2nd", "3rd"]:
    vals = pronoun_s2[person]
    if not vals:
        continue
    n = len(vals)
    m = mean(vals)
    med = statistics.median(vals)
    pos_pct = 100 * sum(1 for v in vals if v > 0) / n
    print(f"{person:<6} {n:>9,} {m:>+8.3f} {med:>+8.3f} {pos_pct:>5.1f}%")


# ── 3. ALTERNATIVES when poem uses 1st/2nd-person pronouns ──────────────────

print("\n\n## 3. What Does GPT-2 Expect When Poets Write 'I' or 'You'?\n")

for person in ["1st", "2nd"]:
    examples = sorted(pronoun_examples[person], key=lambda x: x["s2"], reverse=True)[:8]
    label = {"1st": "'I/we/me' (1st person)", "2nd": "'you/thee/thy' (2nd person)"}[person]
    print(f"\n### High-S₂ {label} tokens:\n")
    print(f"{'S₂':>6} | {'Token':<8} | {'GPT-2 predicted':<16} | {'P(pred)':>8} | Context")
    print("-" * 80)
    for ex in examples:
        ctx = ex["context"].replace("\n", "↵").strip()[-40:]
        print(f"{ex['s2']:>+6.2f} | {ex['token']:<8} | {ex['top_pred']:<16} | {ex['top_prob']:>8.4f} | …{ctx}")


# ── 4. PERSON-SWITCH DETECTION ────────────────────────────────────────────────

print("\n\n## 4. Person-Switch Moments (S₂ at switches between grammatical person)\n")

switch_s2_values  = []
noswitch_s2_values = []
switch_examples   = []

WINDOW = 3  # tokens around switch to capture context

for poem in corpus:
    meta   = poem["metadata"]
    tokens = poem["tokens"]
    if meta.get("language", "en") != "en":
        continue
    if meta.get("era") == "control":
        continue

    # Build person sequence
    person_seq = []
    for t in tokens:
        tok_lower = t["token"].lower()
        p = person_of_token(tok_lower)
        person_seq.append(p)

    # Identify switches: positions where a pronoun changes person
    last_person = None
    for i, (t, p) in enumerate(zip(tokens, person_seq)):
        if p is None:
            continue
        if last_person is not None and p != last_person:
            # Switch detected at position i
            s2 = t["s2"]
            switch_s2_values.append(s2)
            if abs(s2) > 1.5:
                ctx_tokens = tokens[max(0, i-3):i+2]
                ctx_str = "".join(tok["token"] for tok in ctx_tokens)
                switch_examples.append({
                    "from": last_person,
                    "to": p,
                    "s2": s2,
                    "token": t["token"],
                    "context": ctx_str,
                    "author": meta["author"],
                    "title": meta["title"],
                })
        elif p is not None:
            noswitch_s2_values.append(t["s2"])
        if p is not None:
            last_person = p

print(f"Switch pronoun tokens: {len(switch_s2_values):,}")
print(f"Non-switch pronoun tokens: {len(noswitch_s2_values):,}")
if switch_s2_values and noswitch_s2_values:
    print(f"Avg S₂ at switch: {mean(switch_s2_values):+.3f}")
    print(f"Avg S₂ at non-switch: {mean(noswitch_s2_values):+.3f}")
    print(f"Difference: {mean(switch_s2_values) - mean(noswitch_s2_values):+.3f}")

print("\n### Notable person-switch examples (|S₂| > 1.5):\n")
switch_examples_sorted = sorted(switch_examples, key=lambda x: x["s2"], reverse=True)[:10]
for ex in switch_examples_sorted:
    ctx = ex["context"].replace("\n", "↵")
    print(f"  [{ex['from']} -> {ex['to']}] S2={ex['s2']:+.2f} | '{ctx}' -- {ex['author']}")


# ── 5. ERA × PERSON BREAKDOWN ────────────────────────────────────────────────

print("\n\n## 5. Grammatical Person Distribution Across Eras\n")
print(f"{'Era':<20} {'n':>4} | {'%1st':>5} {'%2nd':>5} {'%3rd':>5} | {'dom. person'}")
print("-" * 60)

era_person = defaultdict(lambda: defaultdict(list))  # era → person → [avg_s2]
era_counts  = defaultdict(lambda: {"1st": 0, "2nd": 0, "3rd": 0, "impersonal": 0, "total": 0})

for poem in corpus:
    meta   = poem["metadata"]
    tokens = poem["tokens"]
    if meta.get("language", "en") != "en":
        continue
    era = meta.get("era", "unknown")
    dom, c1, c2, c3 = classify_person(tokens)
    era_counts[era]["total"] += 1
    era_counts[era][dom]     += 1
    era_person[era][dom].append(poem["summary"]["avg_s2"])

for era in sorted(era_counts.keys(), key=lambda e: -era_counts[e]["total"]):
    ec = era_counts[era]
    tot = ec["total"]
    if tot < 2:
        continue
    p1 = 100 * ec["1st"] / tot
    p2 = 100 * ec["2nd"] / tot
    p3 = 100 * ec["3rd"] / tot
    dom = max(["1st", "2nd", "3rd", "impersonal"], key=lambda p: ec[p])
    print(f"{era:<20} {tot:>4} | {p1:>4.0f}% {p2:>4.0f}% {p3:>4.0f}% | {dom}")


# ── 6. SUMMARY TABLE ─────────────────────────────────────────────────────────

print("\n\n## 6. Summary: Person vs S₂ Ranking\n")
ranking = sorted(results_by_person.items(), key=lambda kv: -kv[1]["avg_s2"])
for i, (person, stats) in enumerate(ranking, 1):
    label = {"1st": "1st-person (I/we)", "2nd": "2nd-person (you/thee)",
             "3rd": "3rd-person (he/she/they)", "impersonal": "impersonal"}[person]
    print(f"  #{i}. {label:30s}  avg S₂ = {stats['avg_s2']:+.3f}  (n={stats['n']})")

print("\n[Done]")
