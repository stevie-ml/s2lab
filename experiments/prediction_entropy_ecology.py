"""
Prediction Entropy Ecology: The Full Shape of GPT-2's Uncertainty at High-S2 Moments

Prior work classified GPT-2's prediction landscape as binary: Ambush (top prediction dominates)
vs. Fog (diffuse field). This experiment extends that to a continuous measure: the Shannon
entropy of the top-10 alternatives distribution, which we call "prediction entropy."

Key questions:
1. How does prediction entropy at a token position relate to the resulting S2?
2. Are there characteristic "prediction entropy landscapes" for different poets / eras?
3. Does prediction entropy interact with the TYPE of surprise (function→content, content→content)?
4. Do high-S2 tokens in constraint poems (OuLiPo) come from a different prediction entropy
   landscape than high-S2 tokens in free verse?

The prediction entropy of the top-10 alternatives is:
  H_top10 = -sum(p_i/Z * log2(p_i/Z) for i in top10)
where Z = sum of top-10 probabilities (normalizing so they sum to 1).

This is a local measure of how "pointed" vs. "diffuse" the model's uncertainty is,
computed from the top-10 probability mass only.
"""

import json
import math
from collections import defaultdict

CORPUS = "results/corpus_results.json"

def top10_entropy(alternatives: list) -> float:
    """Shannon entropy of the top-10 prediction distribution (normalized)."""
    if not alternatives:
        return 0.0
    probs = [a["prob"] for a in alternatives]
    Z = sum(probs)
    if Z == 0:
        return 0.0
    ent = 0.0
    for p in probs:
        pn = p / Z
        if pn > 0:
            ent -= pn * math.log2(pn)
    return ent


def classify_token_type(token: str, top_alt: str) -> str:
    """Rough classification of poet's actual choice vs. model's top prediction."""
    tok = token.strip().lower().strip(".,!?;:'\"")
    alt = top_alt.strip().lower().strip(".,!?;:'\"")

    FUNCTION = {
        "the","a","an","and","or","but","of","in","on","at","to","for","with","as",
        "by","from","that","this","is","are","was","were","be","been","being","have",
        "has","had","do","does","did","will","would","could","should","may","might",
        "can","shall","must","not","no","it","its","they","them","we","us","our",
        "my","your","his","her","who","which","what","all","each","any","some","i",
        "he","she","you","me","him","so","then","when","where","if","though","while",
        "about","into","through","before","after","above","below","up","down","out",
        "over","under","here","there","also","than","these","those","their",
    }
    PUNCT = set(".,;:!?-–—\"'()[]{}…/\\")

    def is_func(t): return t in FUNCTION or len(t) <= 1
    def is_punct(t): return t in PUNCT or all(c in ".,;:!?-–—\"'()[]{}…/\\" for c in t)

    poet_func = is_func(tok)
    poet_punct = is_punct(tok)
    alt_func = is_func(alt)
    alt_punct = is_punct(alt)

    if alt_func and not poet_func and not poet_punct:
        return "function→content"
    elif not alt_func and not alt_punct and poet_func:
        return "content→function"
    elif alt_punct and not poet_punct and not poet_func:
        return "punct→content"
    elif not alt_func and not alt_punct and not poet_func and not poet_punct:
        return "content→content"
    else:
        return "other"


def main():
    with open(CORPUS) as f:
        corpus = json.load(f)

    # ── Collect token-level data ──────────────────────────────────────────────
    records = []
    poet_data = defaultdict(list)
    era_data = defaultdict(list)

    for poem in corpus:
        meta = poem["metadata"]
        lang = meta.get("language", "en")
        if lang != "en":
            continue
        era = meta.get("era", "unknown")
        author = meta.get("author", "unknown")
        if era in ("control", "cliche_control"):
            continue

        for tok in poem["tokens"]:
            # exclude stanza-break artifact tokens
            if tok.get("p_newline", 0) >= 0.9:
                continue
            alts = tok.get("alternatives", [])
            if not alts:
                continue

            h10 = top10_entropy(alts)
            s2 = tok["s2"]
            surprisal = tok["surprisal"]
            entropy = tok["entropy"]
            rank = tok["rank"]
            top_alt = alts[0]["token"] if alts else ""
            actual = tok["token"]
            trans_type = classify_token_type(actual, top_alt)

            rec = {
                "h10": h10,
                "s2": s2,
                "surprisal": surprisal,
                "entropy": entropy,
                "rank": rank,
                "trans_type": trans_type,
                "author": author,
                "era": era,
                "is_high_s2": s2 >= 3.0,
                "is_ambush": alts[0]["prob"] / alts[1]["prob"] > 2.0 if len(alts) >= 2 else False,
            }
            records.append(rec)
            poet_data[author].append(rec)
            era_data[era].append(rec)

    print(f"Total artifact-free tokens: {len(records)}")

    # ── 1. Prediction entropy vs S2 quintiles ────────────────────────────────
    sorted_by_s2 = sorted(records, key=lambda r: r["s2"])
    n = len(sorted_by_s2)
    q_size = n // 5
    print("\n=== Prediction Entropy H_top10 vs S2 Quintile ===")
    print(f"{'Quintile':<20} {'S2 range':<20} {'n':>6} {'Mean H_top10':>14} {'Mean S2':>10}")
    for qi in range(5):
        chunk = sorted_by_s2[qi*q_size : (qi+1)*q_size]
        s2_vals = [r["s2"] for r in chunk]
        h_vals = [r["h10"] for r in chunk]
        print(f"Q{qi+1} ({['lowest','lower','middle','upper','highest'][qi]:<7})"
              f"  [{min(s2_vals):5.1f}, {max(s2_vals):5.1f}]"
              f"  {len(chunk):>6}"
              f"  {sum(h_vals)/len(h_vals):>14.3f}"
              f"  {sum(s2_vals)/len(s2_vals):>10.3f}")

    # ── 2. Prediction entropy correlates with rank ────────────────────────────
    rank_bands = [(1,1,"rank=1 (top-1 match)"), (2,5,"rank 2-5"), (6,10,"rank 6-10"),
                  (11,50,"rank 11-50"), (51,500,"rank 51-500"), (501,99999,"rank >500")]
    print("\n=== Prediction Entropy by Rank Band ===")
    print(f"{'Band':<28} {'n':>6} {'Mean H_top10':>14} {'Mean S2':>10}")
    for lo, hi, label in rank_bands:
        chunk = [r for r in records if lo <= r["rank"] <= hi]
        if not chunk:
            continue
        h = sum(r["h10"] for r in chunk)/len(chunk)
        s = sum(r["s2"] for r in chunk)/len(chunk)
        print(f"  {label:<26}  {len(chunk):>6}  {h:>14.3f}  {s:>10.3f}")

    # ── 3. Prediction entropy by substitution type ────────────────────────────
    print("\n=== Prediction Entropy by Transition Type (all tokens) ===")
    by_type = defaultdict(list)
    for r in records:
        by_type[r["trans_type"]].append(r)
    print(f"{'Type':<24} {'n':>6} {'Mean H_top10':>14} {'Mean S2':>10} {'Pos S2%':>9}")
    for ttype, recs in sorted(by_type.items(), key=lambda x: -len(x[1])):
        h = sum(r["h10"] for r in recs)/len(recs)
        s = sum(r["s2"] for r in recs)/len(recs)
        pos = sum(1 for r in recs if r["s2"]>0)/len(recs)*100
        print(f"  {ttype:<22}  {len(recs):>6}  {h:>14.3f}  {s:>10.3f}  {pos:>8.1f}%")

    # ── 4. High-S2 tokens: Ambush vs Fog × H_top10 ───────────────────────────
    high_s2 = [r for r in records if r["is_high_s2"]]
    ambush = [r for r in high_s2 if r["is_ambush"]]
    fog = [r for r in high_s2 if not r["is_ambush"]]
    print(f"\n=== High-S2 Tokens (S2 ≥ 3): Prediction Entropy × Ambush/Fog ===")
    for label, recs in [("Ambush (top_ratio > 2)", ambush), ("Fog (top_ratio ≤ 2)", fog)]:
        if not recs:
            continue
        h = sum(r["h10"] for r in recs)/len(recs)
        s = sum(r["s2"] for r in recs)/len(recs)
        print(f"  {label:<35}  n={len(recs):>5}  Mean H_top10={h:.3f}  Mean S2={s:.3f}")

    # H_top10 distribution for ambush vs fog
    ambush_hi = sum(1 for r in ambush if r["h10"] > 2.5)/len(ambush)*100 if ambush else 0
    fog_hi = sum(1 for r in fog if r["h10"] > 2.5)/len(fog)*100 if fog else 0
    print(f"  H_top10 > 2.5 (diffuse field): Ambush {ambush_hi:.1f}%, Fog {fog_hi:.1f}%")

    # ── 5. Era-level prediction entropy landscape ─────────────────────────────
    print("\n=== Era-Level Prediction Entropy (high-S2 tokens only, S2 ≥ 3) ===")
    print(f"{'Era':<24} {'n':>6} {'Mean H_top10':>14} {'Mean S2':>10} {'Ambush%':>9}")
    era_rows = []
    for era, recs in era_data.items():
        hi = [r for r in recs if r["is_high_s2"]]
        if len(hi) < 10:
            continue
        h = sum(r["h10"] for r in hi)/len(hi)
        s = sum(r["s2"] for r in hi)/len(hi)
        amb = sum(1 for r in hi if r["is_ambush"])/len(hi)*100
        era_rows.append((era, len(hi), h, s, amb))
    for row in sorted(era_rows, key=lambda x: -x[2]):
        print(f"  {row[0]:<22}  {row[1]:>6}  {row[2]:>14.3f}  {row[3]:>10.3f}  {row[4]:>8.1f}%")

    # ── 6. Poet-level: H_top10 fingerprint ───────────────────────────────────
    print("\n=== Poet Prediction Entropy Fingerprint (≥20 high-S2 tokens) ===")
    print(f"{'Author':<30} {'n':>6} {'Mean H_top10':>14} {'Mean S2':>10} {'Ambush%':>9}")
    poet_rows = []
    for author, recs in poet_data.items():
        hi = [r for r in recs if r["is_high_s2"]]
        if len(hi) < 20:
            continue
        h = sum(r["h10"] for r in hi)/len(hi)
        s = sum(r["s2"] for r in hi)/len(hi)
        amb = sum(1 for r in hi if r["is_ambush"])/len(hi)*100
        poet_rows.append((author, len(hi), h, s, amb))
    for row in sorted(poet_rows, key=lambda x: -x[2]):
        print(f"  {row[0]:<28}  {row[1]:>6}  {row[2]:>14.3f}  {row[3]:>10.3f}  {row[4]:>8.1f}%")

    # ── 7. Continuous H_top10 bins vs mean S2 ────────────────────────────────
    print("\n=== S2 by H_top10 Prediction Entropy Bin ===")
    bins = [(0,1.0,"0.0–1.0 (very concentrated)"),(1.0,1.5,"1.0–1.5"),(1.5,2.0,"1.5–2.0"),
            (2.0,2.5,"2.0–2.5"),(2.5,3.0,"2.5–3.0"),(3.0,3.3,"3.0–3.3 (maximum entropy)")]
    print(f"{'H_top10 bin':<32} {'n':>7} {'Mean S2':>10} {'High S2%':>10}")
    for lo, hi, label in bins:
        chunk = [r for r in records if lo <= r["h10"] < hi]
        if not chunk:
            continue
        s = sum(r["s2"] for r in chunk)/len(chunk)
        pos = sum(1 for r in chunk if r["is_high_s2"])/len(chunk)*100
        print(f"  {label:<30}  {len(chunk):>7}  {s:>10.3f}  {pos:>9.1f}%")

    # ── Save results ──────────────────────────────────────────────────────────
    results = {
        "total_tokens": len(records),
        "high_s2_tokens": len(high_s2),
        "ambush_n": len(ambush),
        "fog_n": len(fog),
        "ambush_mean_h10": sum(r["h10"] for r in ambush)/max(1,len(ambush)),
        "fog_mean_h10": sum(r["h10"] for r in fog)/max(1,len(fog)),
        "era_rows": [{"era":r[0],"n":r[1],"mean_h10":r[2],"mean_s2":r[3],"ambush_pct":r[4]}
                     for r in era_rows],
        "poet_rows": [{"author":r[0],"n":r[1],"mean_h10":r[2],"mean_s2":r[3],"ambush_pct":r[4]}
                      for r in poet_rows],
    }
    with open("results/prediction_entropy_ecology.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nSaved to results/prediction_entropy_ecology.json")


if __name__ == "__main__":
    main()
