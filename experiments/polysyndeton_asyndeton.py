"""
Polysyndeton vs. Asyndeton: S2 signatures of conjunction density

Polysyndeton = many conjunctions ("and this and that and those")
Asyndeton    = no conjunctions in list structures ("earth, air, fire, water")

Hypotheses:
1. Conjunction tokens ("and", "or", "but") have low S2 (they're expected by GPT-2)
2. Tokens following conjunctions have different S2 than baseline
3. Asyndeton creates higher S2 at comma-separated items (GPT-2 expects "and")
4. High-polysyndeton poems differ in avg S2 from low-polysyndeton poems
"""

import json
import re
from collections import defaultdict

with open("results/corpus_results.json") as f:
    corpus = json.load(f)

CONJUNCTIONS = {" and", " or", " but", " nor", " yet", " so"}
CONJ_TOKENS  = {"and", "or", "but", "nor", "yet", "so"}   # without leading space

def is_conjunction(tok):
    t = tok.lower()
    return t in CONJUNCTIONS or t.strip() in CONJ_TOKENS

def is_clean(tok_entry):
    return tok_entry.get("p_newline", 0) < 0.9

# ── 1. Conjunction S2 vs baseline ─────────────────────────────────────────────
conj_s2   = []
other_s2  = []
post_conj_s2 = []   # token immediately after a conjunction

for poem in corpus:
    tokens = poem["tokens"]
    for i, t in enumerate(tokens):
        if not is_clean(t):
            continue
        if is_conjunction(t["token"]):
            conj_s2.append(t["s2"])
            if i + 1 < len(tokens) and is_clean(tokens[i+1]):
                post_conj_s2.append(tokens[i+1]["s2"])
        else:
            other_s2.append(t["s2"])

def mean(lst): return sum(lst)/len(lst) if lst else 0.0
def median(lst):
    s = sorted(lst)
    n = len(s)
    return s[n//2] if n else 0.0

print("=== 1. Conjunction tokens vs baseline ===")
print(f"  Conjunctions   (n={len(conj_s2):5d})  mean S2 = {mean(conj_s2):.3f}  median = {median(conj_s2):.3f}")
print(f"  Post-conj tok  (n={len(post_conj_s2):5d})  mean S2 = {mean(post_conj_s2):.3f}  median = {median(post_conj_s2):.3f}")
print(f"  Baseline other (n={len(other_s2):5d})  mean S2 = {mean(other_s2):.3f}  median = {median(other_s2):.3f}")
print()

# ── 2. Asyndeton: tokens after comma with NO preceding conjunction ─────────────
# Pattern: ..., TOKEN  where TOKEN is not "and/or/but..." and doesn't follow conj

def detect_asyndeton_tokens(tokens):
    """Return S2 of items in comma-separated runs without conjunction."""
    results = []
    for i, t in enumerate(tokens):
        if t["token"].strip() in (",", ";") and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if not is_clean(nxt):
                continue
            # check that previous clean word is not a conjunction
            prev_tok = None
            for j in range(i-1, max(i-4, -1), -1):
                if is_clean(tokens[j]) and tokens[j]["token"].strip() not in (",", ";", ":"):
                    prev_tok = tokens[j]
                    break
            if prev_tok and not is_conjunction(prev_tok["token"]):
                results.append(nxt["s2"])
    return results

def detect_post_and_tokens(tokens):
    """Return S2 of items that follow 'and' in a list context."""
    results = []
    for i, t in enumerate(tokens):
        if is_conjunction(t["token"]) and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if is_clean(nxt):
                # check that there's a comma somewhere in past 4 tokens (list context)
                found_comma = any(
                    tokens[j]["token"].strip() in (",", ";")
                    for j in range(max(0, i-4), i)
                )
                if found_comma:
                    results.append(nxt["s2"])
    return results

asyndeton_s2 = []
polysyndeton_s2 = []

for poem in corpus:
    asyndeton_s2.extend(detect_asyndeton_tokens(poem["tokens"]))
    polysyndeton_s2.extend(detect_post_and_tokens(poem["tokens"]))

print("=== 2. List context: asyndeton vs. polysyndeton items ===")
print(f"  Asyndeton items (n={len(asyndeton_s2):4d})  mean S2 = {mean(asyndeton_s2):.3f}  median = {median(asyndeton_s2):.3f}")
print(f"  Polysyndeton items (n={len(polysyndeton_s2):4d}) mean S2 = {mean(polysyndeton_s2):.3f}  median = {median(polysyndeton_s2):.3f}")
print()

# ── 3. Per-poem conjunction density vs avg S2 ─────────────────────────────────
poem_stats = []
for poem in corpus:
    tokens = poem["tokens"]
    clean  = [t for t in tokens if is_clean(t)]
    if len(clean) < 5:
        continue
    n_conj = sum(1 for t in clean if is_conjunction(t["token"]))
    conj_density = n_conj / len(clean)
    avg_s2 = mean([t["s2"] for t in clean])
    poem_stats.append({
        "title":   poem["metadata"]["title"],
        "author":  poem["metadata"]["author"],
        "era":     poem["metadata"]["era"],
        "conj_density": conj_density,
        "avg_s2":  avg_s2,
        "n_tokens": len(clean),
        "n_conj":  n_conj,
    })

poem_stats.sort(key=lambda x: x["conj_density"])

print("=== 3. Per-poem conjunction density vs avg S₂ ===")
print()
print("--- 10 LOWEST conjunction-density poems (asyndetic style) ---")
print(f"{'Title':<40} {'Author':<20} {'Era':<15} {'Conj%':>6} {'AvgS2':>7}")
for p in poem_stats[:10]:
    print(f"{p['title'][:39]:<40} {p['author'][:19]:<20} {p['era'][:14]:<15} {p['conj_density']*100:6.1f}% {p['avg_s2']:7.3f}")

print()
print("--- 10 HIGHEST conjunction-density poems (polysyndetic style) ---")
print(f"{'Title':<40} {'Author':<20} {'Era':<15} {'Conj%':>6} {'AvgS2':>7}")
for p in reversed(poem_stats[-10:]):
    print(f"{p['title'][:39]:<40} {p['author'][:19]:<20} {p['era'][:14]:<15} {p['conj_density']*100:6.1f}% {p['avg_s2']:7.3f}")

# ── 4. Quartile analysis ───────────────────────────────────────────────────────
n = len(poem_stats)
q1 = poem_stats[:n//4]
q4 = poem_stats[3*n//4:]

avg_s2_q1 = mean([p["avg_s2"] for p in q1])
avg_s2_q4 = mean([p["avg_s2"] for p in q4])

print()
print("=== 4. Quartile analysis: conjunction density vs avg S₂ ===")
print(f"  Lowest-density quartile  (n={len(q1)})  avg S₂ = {avg_s2_q1:.3f}")
print(f"  Highest-density quartile (n={len(q4)})  avg S₂ = {avg_s2_q4:.3f}")
print(f"  Δ = {avg_s2_q4 - avg_s2_q1:.3f}")
print()

# ── 5. Era breakdown: conjunction density ─────────────────────────────────────
era_stats = defaultdict(list)
for p in poem_stats:
    era_stats[p["era"]].append(p["conj_density"])

era_avg = {era: (mean(vals), len(vals)) for era, vals in era_stats.items() if len(vals) >= 2}
era_sorted = sorted(era_avg.items(), key=lambda x: -x[1][0])

print("=== 5. Era conjunction density ===")
print(f"{'Era':<25} {'Avg Conj%':>10} {'n':>4}")
for era, (avg, n) in era_sorted:
    print(f"{era:<25} {avg*100:10.1f}% {n:4d}")

# ── 6. Most striking substitutions: what GPT-2 expected at comma positions ─────
print()
print("=== 6. What GPT-2 expected at asyndeton comma positions (top 15 by S2) ===")
asyn_moments = []
for poem in corpus:
    tokens = poem["tokens"]
    for i, t in enumerate(tokens):
        if t["token"].strip() in (",", ";") and i + 1 < len(tokens):
            nxt = tokens[i + 1]
            if not is_clean(nxt):
                continue
            prev_tok = None
            for j in range(i-1, max(i-4, -1), -1):
                if is_clean(tokens[j]) and tokens[j]["token"].strip() not in (",", ";", ":"):
                    prev_tok = tokens[j]
                    break
            if prev_tok and not is_conjunction(prev_tok["token"]) and nxt["s2"] > 1:
                ctx = " ".join(t["token"] for t in tokens[max(0,i-4):i+2])
                top_alt = nxt["alternatives"][0]["token"] if nxt["alternatives"] else "?"
                asyn_moments.append({
                    "title": poem["metadata"]["title"],
                    "author": poem["metadata"]["author"],
                    "s2": nxt["s2"],
                    "token": nxt["token"],
                    "expected": top_alt,
                    "context": ctx,
                })

asyn_moments.sort(key=lambda x: -x["s2"])
for m in asyn_moments[:15]:
    print(f"  S2={m['s2']:6.2f}  '{m['token']}' (expected: '{m['expected']}')  — {m['author']}: {m['title'][:35]}")
    print(f"           context: ...{m['context']}...")

print()
print("Done.")
