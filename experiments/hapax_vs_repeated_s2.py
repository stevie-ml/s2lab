"""
Hapax Legomena vs. Repeated Words: Does Lexical Uniqueness Drive S2?

Research question: Within a single poem, do words used only once (hapax legomena)
have higher S2 than words the poet uses multiple times? And what does this tell us
about the dual nature of the Straussian gap?
"""
import json, statistics, re
from collections import Counter

with open("results/corpus_results.json") as f:
    data = json.load(f)

hapax_all = []
repeated_all = []
poem_results = []
era_data = {}

for poem in data:
    if poem["metadata"].get("language", "en") != "en":
        continue
    tokens = poem["tokens"]
    if len(tokens) < 20:
        continue

    era = poem["metadata"].get("era", "unknown")
    word_counts = Counter()
    for tok in tokens:
        word = re.sub(r"[^a-z]", "", tok["token"].strip().lower())
        if len(word) >= 3:
            word_counts[word] += 1

    poem_hapax, poem_repeated = [], []
    for tok in tokens:
        word = re.sub(r"[^a-z]", "", tok["token"].strip().lower())
        if len(word) < 3:
            continue
        s2 = tok["s2"]
        if word_counts[word] == 1:
            poem_hapax.append(s2)
            hapax_all.append(s2)
        else:
            poem_repeated.append(s2)
            repeated_all.append(s2)

    if not poem_hapax or not poem_repeated:
        continue

    poem_results.append({
        "title": poem["metadata"]["title"],
        "author": poem["metadata"]["author"],
        "era": era,
        "hapax_mean": statistics.mean(poem_hapax),
        "repeated_mean": statistics.mean(poem_repeated),
        "diff": statistics.mean(poem_hapax) - statistics.mean(poem_repeated),
        "n_hapax": len(poem_hapax),
        "n_repeated": len(poem_repeated),
    })

    if era not in era_data:
        era_data[era] = {"hapax": [], "repeated": []}
    era_data[era]["hapax"].extend(poem_hapax)
    era_data[era]["repeated"].extend(poem_repeated)

gap = statistics.mean(hapax_all) - statistics.mean(repeated_all)
hapax_higher = sum(1 for p in poem_results if p["hapax_mean"] > p["repeated_mean"])

print(f"=== HAPAX vs REPEATED WORDS: S2 ANALYSIS ===\n")
print(f"Hapax tokens    : {len(hapax_all):5d}  mean S2 = {statistics.mean(hapax_all):+.3f}  ± {statistics.stdev(hapax_all):.3f}")
print(f"Repeated tokens : {len(repeated_all):5d}  mean S2 = {statistics.mean(repeated_all):+.3f}  ± {statistics.stdev(repeated_all):.3f}")
print(f"Gap             : {gap:+.3f}")
print(f"Poems with hapax > repeated: {hapax_higher}/{len(poem_results)} ({hapax_higher/len(poem_results)*100:.0f}%)\n")

print("=== BY ERA (hapax gap = hapax_mean - repeated_mean) ===")
for era, d in sorted(era_data.items(), key=lambda x: -(statistics.mean(x[1]["hapax"]) - statistics.mean(x[1]["repeated"]))):
    if len(d["hapax"]) < 10:
        continue
    era_gap = statistics.mean(d["hapax"]) - statistics.mean(d["repeated"])
    print(f"  {era:25s}: gap={era_gap:+.3f}  hapax={statistics.mean(d['hapax']):+.3f}  repeated={statistics.mean(d['repeated']):+.3f}  (n={len(d['hapax'])}/{len(d['repeated'])})")

print("\n=== LARGEST POSITIVE GAP (hapax >> repeated) ===")
for p in sorted(poem_results, key=lambda x: -x["diff"])[:8]:
    print(f"  {p['title'][:40]:40s}  hapax={p['hapax_mean']:+.2f}  rep={p['repeated_mean']:+.2f}  Δ={p['diff']:+.2f}")

print("\n=== REVERSED PATTERN (repeated >> hapax) ===")
for p in sorted(poem_results, key=lambda x: x["diff"])[:5]:
    print(f"  {p['title'][:40]:40s}  hapax={p['hapax_mean']:+.2f}  rep={p['repeated_mean']:+.2f}  Δ={p['diff']:+.2f}")
    # Show what the high-S2 repeated words are
    for poem in data:
        if poem["metadata"]["title"] == p["title"]:
            tokens = poem["tokens"]
            wc = Counter()
            for tok in tokens:
                w = re.sub(r"[^a-z]", "", tok["token"].strip().lower())
                if len(w) >= 3:
                    wc[w] += 1
            repeated_words = {w for w, c in wc.items() if c >= 2}
            top_rep = [(tok["s2"], tok["token"], tok.get("context_before", "")[-25:])
                       for tok in tokens
                       if re.sub(r"[^a-z]", "", tok["token"].strip().lower()) in repeated_words]
            for s2, tok, ctx in sorted(top_rep, key=lambda x: -x[0])[:3]:
                print(f"    S2={s2:+.2f}  [{tok}]  context: {repr(ctx)}")
