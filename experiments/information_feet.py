"""
Information Feet: Do S2 Sequences Form Iambic, Trochaic, or Anapestic Patterns?
==================================================================================
In classical prosody, metrical "feet" organize syllable stress into patterns:
  - Iamb:    da-DUM  (unstressed → stressed)
  - Trochee: DUM-da  (stressed → unstressed)
  - Anapest: da-da-DUM (2 unstressed → stressed)
  - Dactyl:  DUM-da-da (stressed → 2 unstressed)
  - Spondee: DUM-DUM (both stressed)
  - Pyrrhic: da-da   (both unstressed)

If we map S2 to "information stress" (High S2 = stressed, Low S2 = unstressed),
do poets organize their information structure into analogous feet?

Hypothesis 1 (Iambic Default): English poetry, being predominantly iambic,
should show more LH bigrams than HL bigrams even in information-space.

Hypothesis 2 (Era Differentiation): Metrical eras (Victorian, Romantic) should show
stronger iambic information patterns than free verse eras (New York School, Language).

Hypothesis 3 (Anapestic Ballad): Ballads with strong anapestic meter should show
more LLH trigrams than other traditions.

Method:
  1. For each artifact-free token, classify as H (S2 > 0.5) or L (S2 ≤ 0.5)
  2. Count all bigrams (LH, HL, LL, HH) and trigrams (LLH, LHL, HLL, HLH, LHH, HHL, LLL, HHH)
  3. Compute "iambic dominance" = P(LH) / P(HL) — ratio of rising to falling patterns
  4. Compare across eras and poets

Threshold note: S2 = 0.5 is chosen to split roughly the top 40% as "stressed" (H).
Alternative thresholds are also tested.
"""

import json
import statistics
from collections import defaultdict, Counter

RESULTS_PATH = "results/corpus_results.json"
S2_THRESHOLD = 0.5   # above = H (information-stressed), below = L
MIN_TOKENS = 20       # minimum clean tokens per poem

def load_data():
    with open(RESULTS_PATH) as f:
        return json.load(f)

def get_clean_s2_sequence(poem):
    """Return list of S2 values for artifact-free tokens."""
    clean = []
    for tok in poem["tokens"]:
        if tok.get("p_newline", 1.0) < 0.9:
            clean.append(tok["s2"])
    return clean

def s2_to_stress(s2_values, threshold=S2_THRESHOLD):
    """Convert S2 sequence to binary stress pattern: H or L."""
    return ["H" if v > threshold else "L" for v in s2_values]

def count_feet(stress_pattern):
    """Count bigram and trigram foot types."""
    bigrams = Counter()
    trigrams = Counter()
    for i in range(len(stress_pattern) - 1):
        bigrams[stress_pattern[i] + stress_pattern[i+1]] += 1
    for i in range(len(stress_pattern) - 2):
        trigrams[stress_pattern[i] + stress_pattern[i+1] + stress_pattern[i+2]] += 1
    return bigrams, trigrams

def iambic_dominance(bigrams):
    """LH / HL ratio — ratio of rising to falling information patterns."""
    lh = bigrams.get("LH", 0)
    hl = bigrams.get("HL", 0)
    if hl == 0:
        return None
    return lh / hl

def anapestic_ratio(trigrams):
    """LLH / (HLL + LLH) — anapest vs dactyl proportion."""
    llh = trigrams.get("LLH", 0)
    hll = trigrams.get("HLL", 0)
    total = llh + hll
    if total == 0:
        return None
    return llh / total

def compute_poem_metrics(poem, threshold=S2_THRESHOLD):
    """Compute foot metrics for a single poem."""
    s2_seq = get_clean_s2_sequence(poem)
    if len(s2_seq) < MIN_TOKENS:
        return None

    stress = s2_to_stress(s2_seq, threshold)
    bigrams, trigrams = count_feet(stress)

    total_bigrams = sum(bigrams.values())
    total_trigrams = sum(trigrams.values())

    if total_bigrams == 0:
        return None

    # Proportions
    p_lh = bigrams.get("LH", 0) / total_bigrams
    p_hl = bigrams.get("HL", 0) / total_bigrams
    p_ll = bigrams.get("LL", 0) / total_bigrams
    p_hh = bigrams.get("HH", 0) / total_bigrams

    iamb_dom = iambic_dominance(bigrams)
    h_rate = sum(1 for s in stress if s == "H") / len(stress)

    # Trigram proportions
    anapest_r = None
    if total_trigrams > 0:
        p_llh = trigrams.get("LLH", 0) / total_trigrams
        p_hll = trigrams.get("HLL", 0) / total_trigrams
        p_lhl = trigrams.get("LHL", 0) / total_trigrams
        p_hlh = trigrams.get("HLH", 0) / total_trigrams
        anapest_r = anapestic_ratio(trigrams)
    else:
        p_llh = p_hll = p_lhl = p_hlh = 0.0

    return {
        "era": poem["metadata"]["era"],
        "author": poem["metadata"]["author"],
        "title": poem["metadata"]["title"],
        "n_tokens": len(s2_seq),
        "h_rate": h_rate,
        "p_lh": p_lh,
        "p_hl": p_hl,
        "p_ll": p_ll,
        "p_hh": p_hh,
        "iamb_dominance": iamb_dom,
        "p_llh": p_llh,
        "p_hll": p_hll,
        "p_lhl": p_lhl,
        "p_hlh": p_hlh,
        "anapest_ratio": anapest_r,
    }

def group_stats(items, key):
    """Compute mean ± stdev for a list of dicts by key."""
    vals = [x[key] for x in items if x.get(key) is not None]
    if not vals:
        return None, None, 0
    mean = statistics.mean(vals)
    stdev = statistics.stdev(vals) if len(vals) > 1 else 0.0
    return mean, stdev, len(vals)

def main():
    data = load_data()

    poems_metrics = []
    for poem in data:
        m = compute_poem_metrics(poem)
        if m:
            poems_metrics.append(m)

    print(f"Poems analyzed: {len(poems_metrics)} of {len(data)}\n")

    # --- Global statistics ---
    print("=" * 60)
    print("GLOBAL INFORMATION FOOT DISTRIBUTION")
    print("=" * 60)

    all_p_lh = [m["p_lh"] for m in poems_metrics]
    all_p_hl = [m["p_hl"] for m in poems_metrics]
    all_p_ll = [m["p_ll"] for m in poems_metrics]
    all_p_hh = [m["p_hh"] for m in poems_metrics]
    all_iamb = [m["iamb_dominance"] for m in poems_metrics if m["iamb_dominance"] is not None]

    print(f"\nMean bigram proportions (threshold S2 > {S2_THRESHOLD}):")
    print(f"  LH (iamb-like):    {statistics.mean(all_p_lh):.4f}  ({statistics.mean(all_p_lh)*100:.1f}%)")
    print(f"  HL (trochee-like): {statistics.mean(all_p_hl):.4f}  ({statistics.mean(all_p_hl)*100:.1f}%)")
    print(f"  LL (pyrrhic-like): {statistics.mean(all_p_ll):.4f}  ({statistics.mean(all_p_ll)*100:.1f}%)")
    print(f"  HH (spondee-like): {statistics.mean(all_p_hh):.4f}  ({statistics.mean(all_p_hh)*100:.1f}%)")
    print(f"\n  Mean H rate (% stressed tokens): {statistics.mean([m['h_rate'] for m in poems_metrics])*100:.1f}%")
    print(f"\n  Iambic dominance (LH/HL ratio): {statistics.mean(all_iamb):.4f}")
    print(f"  > 1.0 means more iambic than trochaic; < 1.0 means more trochaic")

    # Null model: if H_rate = r, random bigrams give P(LH) = r*(1-r), P(HL) = r*(1-r)
    # So the null iambic dominance is 1.0 (symmetric). Any deviation from 1.0 is structural.
    iamb_gt1 = sum(1 for x in all_iamb if x > 1.0)
    print(f"\n  Poems with iambic dominance > 1.0: {iamb_gt1}/{len(all_iamb)} ({iamb_gt1/len(all_iamb)*100:.1f}%)")

    # Trigrams
    print(f"\nMean trigram proportions:")
    print(f"  LLH (anapest-like):  {statistics.mean([m['p_llh'] for m in poems_metrics]):.4f}")
    print(f"  HLL (dactyl-like):   {statistics.mean([m['p_hll'] for m in poems_metrics]):.4f}")
    print(f"  LHL (amphibrach):    {statistics.mean([m['p_lhl'] for m in poems_metrics]):.4f}")
    print(f"  HLH (cretic):        {statistics.mean([m['p_hlh'] for m in poems_metrics]):.4f}")

    # --- Iambic dominance: rank poets ---
    print("\n" + "=" * 60)
    print("ERA BREAKDOWN — IAMBIC DOMINANCE (LH/HL ratio)")
    print("=" * 60)

    era_groups = defaultdict(list)
    for m in poems_metrics:
        era_groups[m["era"]].append(m)

    era_iamb = []
    for era, items in era_groups.items():
        mean, stdev, n = group_stats(items, "iamb_dominance")
        if n >= 2:
            era_iamb.append((era, mean, stdev, n))
    era_iamb.sort(key=lambda x: x[1], reverse=True)

    print(f"\n{'Era':<22} {'n':>4} {'Iamb Dom':>10} {'±SD':>8} {'%iambic':>9}")
    print("-" * 58)
    for era, mean, sd, n in era_iamb:
        pct_iambic = sum(1 for m in era_groups[era] if m["iamb_dominance"] and m["iamb_dominance"] > 1.0) / n * 100
        print(f"{era:<22} {n:>4} {mean:>10.3f} {sd:>8.3f} {pct_iambic:>8.0f}%")

    # --- Anapest ratio by era ---
    print("\n" + "=" * 60)
    print("ERA BREAKDOWN — TRIGRAM PATTERNS (anapest vs dactyl)")
    print("=" * 60)

    print(f"\n{'Era':<22} {'n':>4} {'P(LLH)':>8} {'P(HLL)':>8} {'P(LHL)':>8} {'P(HLH)':>8}")
    print("-" * 62)
    for era, items in sorted(era_groups.items(),
                              key=lambda kv: statistics.mean([m['p_llh'] for m in kv[1]]),
                              reverse=True):
        if len(items) < 2:
            continue
        p_llh = statistics.mean([m['p_llh'] for m in items])
        p_hll = statistics.mean([m['p_hll'] for m in items])
        p_lhl = statistics.mean([m['p_lhl'] for m in items])
        p_hlh = statistics.mean([m['p_hlh'] for m in items])
        print(f"{era:<22} {len(items):>4} {p_llh:>8.4f} {p_hll:>8.4f} {p_lhl:>8.4f} {p_hlh:>8.4f}")

    # --- Top and bottom poems by iambic dominance ---
    print("\n" + "=" * 60)
    print("MOST IAMBIC INFORMATION STRUCTURES (top 10 poems by LH/HL ratio)")
    print("=" * 60)

    sorted_poems = sorted([m for m in poems_metrics if m["iamb_dominance"] is not None],
                          key=lambda x: x["iamb_dominance"], reverse=True)

    print(f"\n{'Author':<25} {'Title':<35} {'IambDom':>8} {'Era'}")
    print("-" * 80)
    for m in sorted_poems[:10]:
        title = m["title"][:34]
        author = m["author"][:24]
        print(f"{author:<25} {title:<35} {m['iamb_dominance']:>8.3f} {m['era']}")

    print(f"\n\nMOST TROCHAIC INFORMATION STRUCTURES (bottom 10 by LH/HL ratio):")
    print(f"\n{'Author':<25} {'Title':<35} {'IambDom':>8} {'Era'}")
    print("-" * 80)
    for m in sorted_poems[-10:]:
        title = m["title"][:34]
        author = m["author"][:24]
        print(f"{author:<25} {title:<35} {m['iamb_dominance']:>8.3f} {m['era']}")

    # --- Robustness check: multiple thresholds ---
    print("\n" + "=" * 60)
    print("ROBUSTNESS: IAMBIC DOMINANCE ACROSS THRESHOLDS")
    print("=" * 60)
    print("\nDoes the LH > HL finding hold at different S2 thresholds?")
    print(f"\n{'Threshold':>12} {'Mean LH':>10} {'Mean HL':>10} {'Iamb Dom':>10} {'% > 1.0':>10}")
    print("-" * 58)
    for thr in [-1.0, -0.5, 0.0, 0.5, 1.0, 2.0]:
        thr_metrics = [compute_poem_metrics(poem, thr) for poem in data]
        thr_metrics = [m for m in thr_metrics if m]
        iamb_vals = [m["iamb_dominance"] for m in thr_metrics if m["iamb_dominance"] is not None]
        p_lh_vals = [m["p_lh"] for m in thr_metrics]
        p_hl_vals = [m["p_hl"] for m in thr_metrics]
        if iamb_vals:
            pct_gt1 = sum(1 for x in iamb_vals if x > 1.0) / len(iamb_vals) * 100
            print(f"  S2 > {thr:>5.1f}  {statistics.mean(p_lh_vals):>10.4f} {statistics.mean(p_hl_vals):>10.4f} {statistics.mean(iamb_vals):>10.3f} {pct_gt1:>9.1f}%")

    # --- Metrical vs free verse: direct comparison ---
    print("\n" + "=" * 60)
    print("METRICAL vs FREE VERSE: INFORMATION FOOT COMPARISON")
    print("=" * 60)

    METRICAL_ERAS = {"ballad", "fixed_form", "romantic", "victorian", "metaphysical",
                     "early_modern", "nursery_rhyme", "19th_century", "18th_century"}
    FREE_VERSE_ERAS = {"contemporary", "new_york_school", "modernist", "language",
                       "beat", "confessional", "prose_poetry"}

    metrical = [m for m in poems_metrics if m["era"] in METRICAL_ERAS]
    free_verse = [m for m in poems_metrics if m["era"] in FREE_VERSE_ERAS]

    def group_summary(items, label):
        iamb = [m["iamb_dominance"] for m in items if m["iamb_dominance"] is not None]
        p_lh = [m["p_lh"] for m in items]
        p_hl = [m["p_hl"] for m in items]
        p_hh = [m["p_hh"] for m in items]
        p_llh = [m["p_llh"] for m in items]
        p_hlh = [m["p_hlh"] for m in items]
        print(f"\n  {label} (n={len(items)}):")
        print(f"    LH (iamb):    {statistics.mean(p_lh):.4f}")
        print(f"    HL (trochee): {statistics.mean(p_hl):.4f}")
        print(f"    HH (spondee): {statistics.mean(p_hh):.4f}")
        print(f"    LLH (anapest):{statistics.mean(p_llh):.4f}")
        print(f"    HLH (cretic): {statistics.mean(p_hlh):.4f}")
        if iamb:
            print(f"    Iamb dom: {statistics.mean(iamb):.3f}")

    group_summary(metrical, "METRICAL ERAS")
    group_summary(free_verse, "FREE VERSE ERAS")

    # --- Ballads specifically (anapestic tradition) ---
    ballads = [m for m in poems_metrics if m["era"] == "ballad"]
    if ballads:
        group_summary(ballads, "BALLAD (anapestic tradition)")

    # --- Haiku (very structured, 5-7-5) ---
    haiku = [m for m in poems_metrics if m["era"] == "haiku"]
    if haiku:
        group_summary(haiku, "HAIKU (5-7-5 structure)")

if __name__ == "__main__":
    main()
