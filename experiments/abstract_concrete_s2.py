"""
Abstract vs. Concrete Vocabulary and S₂

Tests the Imagist hypothesis: do concrete words ("things") carry
different information-theoretic signatures than abstract words ("ideas")?
Directly relates to Williams' "no ideas but in things."
"""

import json
import re
from collections import defaultdict

ABSTRACT = {
    "love", "death", "beauty", "truth", "time", "soul", "god", "fear",
    "hope", "life", "mind", "heart", "faith", "grace", "glory", "spirit",
    "dream", "peace", "pain", "joy", "nature", "freedom", "power", "desire",
    "sorrow", "grief", "memory", "thought", "idea", "virtue", "evil",
    "darkness", "silence", "eternity", "heaven", "fate", "doom", "sin",
    "mercy", "beauty", "truth", "wisdom", "knowledge", "emotion", "feeling",
    "being", "existence", "meaning", "nothing", "everything", "infinite",
    "eternal", "sacred", "divine", "holy", "noble", "sublime"
}

CONCRETE = {
    "stone", "hand", "river", "tree", "blood", "snow", "fire", "water",
    "door", "eye", "mouth", "foot", "leaf", "bird", "grass", "sun", "moon",
    "wind", "rain", "earth", "wood", "bone", "flesh", "bread", "salt",
    "glass", "cloud", "shadow", "mirror", "flower", "seed", "root", "branch",
    "wing", "feather", "rose", "field", "hill", "sea", "lake", "star",
    "ship", "house", "road", "wall", "iron", "gold", "silver", "dust",
    "ash", "smoke", "fog", "ice", "frost", "tide", "wave", "shore",
    "sand", "rock", "mud", "hay", "wheat", "apple", "grape", "fruit",
    "horse", "dog", "cat", "lamb", "crow", "owl", "hawk", "fish",
    "knife", "sword", "cup", "bowl", "bottle", "rope", "chain", "wheel"
}


def clean_token(tok):
    """Strip GPT-2 tokenizer space prefix and lowercase."""
    return tok.lstrip("Ġ Ċ").lstrip(" ").lower()


def run():
    with open("/home/user/s2lab/results/corpus_results.json") as f:
        data = json.load(f)

    abstract_hits = []   # (s2, poem_title, token, author, era)
    concrete_hits = []
    other_hits = []      # baseline — all other content words

    abstract_by_word = defaultdict(list)
    concrete_by_word = defaultdict(list)

    # Collect by poet/era
    by_era = defaultdict(lambda: {"abstract": [], "concrete": []})
    by_poet = defaultdict(lambda: {"abstract": [], "concrete": []})

    for entry in data:
        meta = entry.get("metadata", {})
        title = meta.get("title", "unknown")
        author = meta.get("author", "unknown")
        era = meta.get("era", "unknown")
        lang = meta.get("language", "en")

        if lang != "en":
            continue  # only English

        for tok_obj in entry.get("tokens", []):
            raw = tok_obj.get("token", "")
            s2 = tok_obj.get("s2", 0.0)
            clean = clean_token(raw)

            if clean in ABSTRACT:
                abstract_hits.append((s2, title, raw, author, era))
                abstract_by_word[clean].append(s2)
                by_era[era]["abstract"].append(s2)
                by_poet[author]["abstract"].append(s2)
            elif clean in CONCRETE:
                concrete_hits.append((s2, title, raw, author, era))
                concrete_by_word[clean].append(s2)
                by_era[era]["concrete"].append(s2)
                by_poet[author]["concrete"].append(s2)
            elif re.match(r"^[a-z][a-z]{2,}$", clean):
                # multi-char alphabetic token not in either set = other content words
                other_hits.append(s2)

    def stats(lst):
        if not lst:
            return {"n": 0, "mean": 0, "median": 0, "pos_pct": 0, "max": 0, "min": 0}
        import statistics
        return {
            "n": len(lst),
            "mean": round(sum(lst) / len(lst), 4),
            "median": round(statistics.median(lst), 4),
            "pos_pct": round(100 * sum(1 for x in lst if x > 0) / len(lst), 1),
            "max": round(max(lst), 4),
            "min": round(min(lst), 4),
        }

    abs_s2 = [x[0] for x in abstract_hits]
    con_s2 = [x[0] for x in concrete_hits]

    print("=" * 60)
    print("ABSTRACT vs. CONCRETE VOCABULARY — S₂ Summary")
    print("=" * 60)
    print(f"\n{'Category':<20} {'n':>6} {'mean S₂':>10} {'median':>8} {'pos%':>8} {'max':>8}")
    print("-" * 62)
    for label, lst in [("ABSTRACT", abs_s2), ("CONCRETE", con_s2), ("OTHER (baseline)", other_hits)]:
        s = stats(lst)
        print(f"{label:<20} {s['n']:>6} {s['mean']:>10.4f} {s['median']:>8.4f} {s['pos_pct']:>7.1f}% {s['max']:>8.4f}")

    print("\n\nTop 15 ABSTRACT words by avg S₂:")
    print(f"{'Word':<16} {'n':>5} {'avg S₂':>9}")
    abs_word_stats = [(w, stats(vs)) for w, vs in abstract_by_word.items()]
    abs_word_stats.sort(key=lambda x: x[1]["mean"], reverse=True)
    for w, s in abs_word_stats[:15]:
        print(f"  {w:<14} {s['n']:>5} {s['mean']:>9.4f}")

    print("\n\nTop 15 CONCRETE words by avg S₂:")
    print(f"{'Word':<16} {'n':>5} {'avg S₂':>9}")
    con_word_stats = [(w, stats(vs)) for w, vs in concrete_by_word.items()]
    con_word_stats.sort(key=lambda x: x[1]["mean"], reverse=True)
    for w, s in con_word_stats[:15]:
        print(f"  {w:<14} {s['n']:>5} {s['mean']:>9.4f}")

    print("\n\nBottom 10 ABSTRACT words (lowest avg S₂):")
    for w, s in sorted(abs_word_stats, key=lambda x: x[1]["mean"])[:10]:
        print(f"  {w:<14} {s['n']:>5} {s['mean']:>9.4f}")

    print("\n\nBottom 10 CONCRETE words (lowest avg S₂):")
    for w, s in sorted(con_word_stats, key=lambda x: x[1]["mean"])[:10]:
        print(f"  {w:<14} {s['n']:>5} {s['mean']:>9.4f}")

    # High-S2 examples for each category
    print("\n\nTop 10 highest-S₂ ABSTRACT moments:")
    for s2, title, tok, author, era in sorted(abstract_hits, reverse=True)[:10]:
        print(f"  S₂={s2:>7.2f}  {tok!r:<12}  {author}  [{title[:35]}]")

    print("\n\nTop 10 highest-S₂ CONCRETE moments:")
    for s2, title, tok, author, era in sorted(concrete_hits, reverse=True)[:10]:
        print(f"  S₂={s2:>7.2f}  {tok!r:<12}  {author}  [{title[:35]}]")

    # Era-level breakdown
    print("\n\nS₂ by era — abstract vs. concrete split:")
    print(f"{'Era':<25} {'abs n':>6} {'abs avg':>9} {'con n':>6} {'con avg':>9} {'gap':>7}")
    print("-" * 64)
    era_rows = []
    for era, d in by_era.items():
        a, c = d["abstract"], d["concrete"]
        if len(a) >= 3 and len(c) >= 3:
            a_avg = sum(a) / len(a)
            c_avg = sum(c) / len(c)
            era_rows.append((era, len(a), a_avg, len(c), c_avg, c_avg - a_avg))
    era_rows.sort(key=lambda x: x[5], reverse=True)
    for row in era_rows:
        print(f"  {row[0]:<23} {row[1]:>6} {row[2]:>9.3f} {row[3]:>6} {row[4]:>9.3f} {row[5]:>+7.3f}")

    # Per-poet (poets with enough data in both categories)
    print("\n\nPer-poet — abstract vs. concrete gap (concrete avg − abstract avg):")
    print(f"{'Poet':<30} {'abs n':>6} {'abs avg':>9} {'con n':>6} {'con avg':>9} {'gap':>7}")
    print("-" * 70)
    poet_rows = []
    for poet, d in by_poet.items():
        a, c = d["abstract"], d["concrete"]
        if len(a) >= 3 and len(c) >= 3:
            a_avg = sum(a) / len(a)
            c_avg = sum(c) / len(c)
            poet_rows.append((poet, len(a), a_avg, len(c), c_avg, c_avg - a_avg))
    poet_rows.sort(key=lambda x: x[5], reverse=True)
    for row in poet_rows[:20]:
        print(f"  {row[0]:<28} {row[1]:>6} {row[2]:>9.3f} {row[3]:>6} {row[4]:>9.3f} {row[5]:>+7.3f}")

    return {
        "abstract_stats": stats(abs_s2),
        "concrete_stats": stats(con_s2),
        "other_stats": stats(other_hits),
        "abstract_word_stats": {w: s for w, s in abs_word_stats},
        "concrete_word_stats": {w: s for w, s in con_word_stats},
        "era_rows": era_rows,
        "poet_rows": poet_rows,
    }


if __name__ == "__main__":
    results = run()
