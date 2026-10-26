"""
Polarity Reversal as Rupture vs. Pivot: Are Oxymoronic Substitutions Liberation or Anchoring Events?
=====================================================================================================

The oxymoron_polarity_s2 experiment established that polarity reversal tokens
(where the poet chooses opposite emotional valence from what GPT-2 predicted)
are +2.56 bits higher S₂ than concordant tokens. This experiment asks:

  Do polarity reversals function as RUPTURES (shattering confident expectations,
  expanding entropy) or as PIVOTS (resolving uncertain contexts, contracting entropy)?

The Rupture/Pivot framework (from rupture_pivot_poet_profiles.md):
  - Rupture: high-S₂ token in confident context (entropy_pre < 4 bits)
             → model was sure, the surprise liberates / expands possibility space
  - Pivot: high-S₂ token in uncertain context (entropy_pre >= 7 bits)
           → model was confused, the surprise anchors / collapses possibility space

Method:
  1. Load corpus_results.json
  2. Re-detect polarity reversal events using the same valence lexicon
  3. For each reversal event at position i:
       - Classify as rupture/pivot/middle based on entropy_pre
       - Compute delta_entropy = entropy_post - entropy_pre (i.e., tokens[i+1].entropy - tokens[i].entropy)
       - Positive delta = entropy expanded (liberation); Negative delta = entropy contracted (anchoring)
  4. Compare reversal events vs. non-reversal high-S₂ events on:
       - Rupture/pivot classification rates
       - Mean delta_entropy
       - Era-level breakdown
  5. Identify canonical polarity-reversal ruptures and pivots

Hypothesis:
  H1 (Semantic reversal = liberation): Polarity reversals should cluster in confident
     contexts (ruptures), since they work by shattering a clear expectation.
  H2 (Semantic reversal = anchoring): Polarity reversals might prefer uncertain contexts
     (pivots), since the unexpected valence resolves ambiguity into a clear (dark or light) frame.
  H0 (No preference): Polarity reversals are indifferent to the confidence level of the
     context — they just exploit surprise wherever it occurs.
"""

import json
import re
import os
from collections import defaultdict
from statistics import mean, stdev

# ---------------------------------------------------------------------------
# Valence lexicon (same as oxymoron_polarity_s2.py)
# ---------------------------------------------------------------------------

POSITIVE_WORDS = {
    "love","lovely","light","bright","beauty","beautiful","sweet","joy","joyful",
    "peace","peaceful","hope","hopeful","grace","graceful","true","truth","good",
    "great","warm","warmth","life","living","dream","rise","spring","sun","shine",
    "shining","gold","golden","free","freedom","sing","song","music","pure","holy",
    "heaven","divine","gentle","tender","smile","laugh","laughter","happy","happiness",
    "delight","delightful","glory","glorious","noble","fair","rich","plenty","bloom",
    "blossom","soft","kind","kindness","clear","calm","serene","sacred","bliss",
    "blessed","praise","celebrate","triumph","win","victory","strong","strength",
    "safe","brilliant","wonder","wonderful","glad","gift","care","heal",
    "fresh","alive","grow","flourish","radiant","splendid","magnificent",
    "eternal","immortal","paradise","ecstasy","euphoria","rapture","elation",
    "content","fortunate","merry","vivid","vibrant","lively","jubilant",
    "sublime","perfect","harmony","harmonious","unity","trust","faith",
    "loyal","loyalty","courage","courageous","heroic",
}

NEGATIVE_WORDS = {
    "death","dead","die","dying","dark","darkness","shadow","cold","night","end",
    "fall","fallen","fear","grief","grieve","sad","sorrow","pain","suffer","loss",
    "lost","broken","break","destroy","destruction","hate","hatred","war","fight",
    "battle","wound","blood","tears","cry","weep","mourning","grave","tomb",
    "silence","silent","alone","lonely","empty","hollow","void","nothing","nothingness",
    "despair","desperate","decay","rot","ruin","ruined","ash","ashes","bitter",
    "bitterness","anger","rage","cruel","cruelty","evil","wicked","wrong","sin",
    "guilt","shame","regret","remorse","anguish","agony","misery","wretched",
    "horror","dread","terror","panic","anxiety","doom","fatal",
    "violent","violence","burden","heavy","weight","stone","grey","gray","black",
    "curse","cursed","poison","poisoned","blind","deaf","mute","scar","scars",
    "storm","flood","drown","drowning","slavery","slave","prison","cage","trap",
    "bound","chains","chained","forgotten","absence","absent","barren","bleak",
    "desolate","forsaken","abandon","abandoned","hunger","starve","thirst",
    "exhausted","weary","fading","wither","withered","crumbling","vanish",
    "vanished","collapse","failure","fail","sink","sinking","crash",
}

ARTIFACT_THRESHOLD = 0.9
HIGH_S2 = 1.5
RUPTURE_THRESH = 4.0
PIVOT_THRESH = 7.0


def get_valence(token_text: str) -> str | None:
    word = re.sub(r"[^a-zA-Z]", "", token_text.strip().lower())
    if word in POSITIVE_WORDS:
        return "pos"
    if word in NEGATIVE_WORDS:
        return "neg"
    return None


def predicted_valence(alternatives: list[dict]) -> str | None:
    """Majority valence among top-10 alternatives."""
    pos = 0.0
    neg = 0.0
    for alt in alternatives[:10]:
        v = get_valence(alt["token"])
        p = alt.get("prob", 0.0)
        if v == "pos":
            pos += p
        elif v == "neg":
            neg += p
    if pos == 0 and neg == 0:
        return None
    return "pos" if pos >= neg else "neg"


def is_artifact(tok):
    return tok.get("p_newline", 0.0) >= ARTIFACT_THRESHOLD


def classify_event(entropy_pre: float) -> str:
    if entropy_pre < RUPTURE_THRESH:
        return "rupture"
    elif entropy_pre >= PIVOT_THRESH:
        return "pivot"
    return "middle"


def main():
    with open("results/corpus_results.json") as f:
        corpus = json.load(f)

    # -----------------------------------------------------------------------
    # Collect events
    # -----------------------------------------------------------------------

    reversal_events = []    # polarity reversal tokens
    concordant_events = []  # same-valence tokens (baseline)
    # both filtered to high-S2 for fair comparison

    era_reversal_counts = defaultdict(int)
    era_total_valenced = defaultdict(int)

    poem_reversal_rates = []

    for poem in corpus:
        meta = poem["metadata"]
        era = meta.get("era", "unknown")
        tokens = poem["tokens"]
        n = len(tokens)

        poem_reversals = 0
        poem_valenced = 0

        for i, tok in enumerate(tokens):
            if is_artifact(tok):
                continue

            actual_v = get_valence(tok["token"])
            if actual_v is None:
                continue

            pred_v = predicted_valence(tok.get("alternatives", []))
            if pred_v is None:
                continue

            poem_valenced += 1
            era_total_valenced[era] += 1

            is_reversal = (actual_v != pred_v)
            s2 = tok["s2"]
            entropy_pre = tok["entropy"]

            # delta_entropy: need next clean token
            delta_ent = None
            if i + 1 < n:
                nxt = tokens[i + 1]
                if not is_artifact(nxt):
                    delta_ent = nxt["entropy"] - entropy_pre

            event = {
                "s2": s2,
                "entropy_pre": entropy_pre,
                "delta_entropy": delta_ent,
                "event_type": classify_event(entropy_pre),
                "is_reversal": is_reversal,
                "direction": f"{pred_v}→{actual_v}" if is_reversal else "concordant",
                "token": tok["token"].strip(),
                "era": era,
                "poem": meta.get("title", ""),
                "author": meta.get("author", ""),
                "pos": i,
            }

            if is_reversal:
                poem_reversals += 1
                era_reversal_counts[era] += 1
                reversal_events.append(event)
            else:
                concordant_events.append(event)

        if poem_valenced > 0:
            poem_reversal_rates.append({
                "era": era,
                "rate": poem_reversals / poem_valenced,
                "n_valenced": poem_valenced,
                "title": meta.get("title", ""),
                "author": meta.get("author", ""),
            })

    # -----------------------------------------------------------------------
    # Analysis
    # -----------------------------------------------------------------------

    def stats(events, label):
        if not events:
            return {}
        s2v = [e["s2"] for e in events]
        delta = [e["delta_entropy"] for e in events if e["delta_entropy"] is not None]
        ruptures = sum(1 for e in events if e["event_type"] == "rupture")
        pivots = sum(1 for e in events if e["event_type"] == "pivot")
        middles = sum(1 for e in events if e["event_type"] == "middle")
        return {
            "label": label,
            "n": len(events),
            "mean_s2": round(mean(s2v), 3),
            "mean_delta_entropy": round(mean(delta), 3) if delta else None,
            "pct_delta_pos": round(100 * sum(1 for d in delta if d > 0) / len(delta), 1) if delta else None,
            "n_rupture": ruptures,
            "n_pivot": pivots,
            "n_middle": middles,
            "pct_rupture": round(100 * ruptures / len(events), 1),
            "pct_pivot": round(100 * pivots / len(events), 1),
        }

    reversal_stats = stats(reversal_events, "polarity_reversal")
    concordant_stats = stats(concordant_events, "concordant")

    # High-S₂ only subsets
    rev_high = [e for e in reversal_events if e["s2"] >= HIGH_S2]
    conc_high = [e for e in concordant_events if e["s2"] >= HIGH_S2]
    rev_high_stats = stats(rev_high, "reversal_high_s2")
    conc_high_stats = stats(conc_high, "concordant_high_s2")

    # Direction breakdown
    dir_counts = defaultdict(list)
    for e in reversal_events:
        dir_counts[e["direction"]].append(e)
    dir_stats = {d: stats(evts, d) for d, evts in dir_counts.items()}

    # Era breakdown
    era_reversal_s = defaultdict(list)
    for e in reversal_events:
        era_reversal_s[e["era"]].append(e)
    era_stats = []
    for era in sorted(era_reversal_s.keys()):
        evts = era_reversal_s[era]
        total_v = era_total_valenced[era]
        s = stats(evts, era)
        s["reversal_rate_pct"] = round(100 * len(evts) / total_v, 1) if total_v else 0
        s["total_valenced"] = total_v
        era_stats.append(s)
    era_stats.sort(key=lambda x: x["mean_delta_entropy"] if x["mean_delta_entropy"] else 0, reverse=True)

    # Canonical examples: top reversal ruptures (high S2, low entropy_pre, positive delta_entropy)
    rupture_reversals = sorted(
        [e for e in reversal_events if e["event_type"] == "rupture" and e["delta_entropy"] is not None],
        key=lambda e: e["s2"], reverse=True
    )[:15]

    # Canonical examples: top reversal pivots (high S2, high entropy_pre, negative delta_entropy)
    pivot_reversals = sorted(
        [e for e in reversal_events if e["event_type"] == "pivot" and e["delta_entropy"] is not None],
        key=lambda e: e["s2"], reverse=True
    )[:15]

    # -----------------------------------------------------------------------
    # Save results
    # -----------------------------------------------------------------------
    results = {
        "reversal_stats": reversal_stats,
        "concordant_stats": concordant_stats,
        "reversal_high_s2_stats": rev_high_stats,
        "concordant_high_s2_stats": conc_high_stats,
        "direction_stats": dir_stats,
        "era_stats": era_stats,
        "canonical_rupture_reversals": rupture_reversals,
        "canonical_pivot_reversals": pivot_reversals,
    }

    os.makedirs("results", exist_ok=True)
    with open("results/polarity_reversal_rupture_pivot.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Done. Results saved to results/polarity_reversal_rupture_pivot.json")

    # Quick summary
    print(f"\n=== POLARITY REVERSAL EVENTS ===")
    print(f"Total polarity reversals: {reversal_stats['n']}")
    print(f"  % rupture: {reversal_stats['pct_rupture']}%")
    print(f"  % pivot: {reversal_stats['pct_pivot']}%")
    print(f"  mean S2: {reversal_stats['mean_s2']}")
    print(f"  mean delta_entropy: {reversal_stats['mean_delta_entropy']}")
    print(f"\n=== CONCORDANT EVENTS ===")
    print(f"Total concordant: {concordant_stats['n']}")
    print(f"  % rupture: {concordant_stats['pct_rupture']}%")
    print(f"  % pivot: {concordant_stats['pct_pivot']}%")
    print(f"  mean S2: {concordant_stats['mean_s2']}")
    print(f"  mean delta_entropy: {concordant_stats['mean_delta_entropy']}")

    print("\n=== DIRECTION BREAKDOWN ===")
    for d, s in dir_stats.items():
        print(f"  {d}: n={s['n']}, mean_S2={s['mean_s2']}, mean_delta_H={s['mean_delta_entropy']}, "
              f"rupture={s['pct_rupture']}%, pivot={s['pct_pivot']}%")

    print("\n=== ERA STATS (by mean delta_entropy) ===")
    for s in era_stats[:10]:
        print(f"  {s['label']:25s} n={s['n']:4d} rev_rate={s['reversal_rate_pct']:5.1f}% "
              f"mean_S2={s['mean_s2']:6.3f} delta_H={s['mean_delta_entropy']:6.3f} "
              f"rupt={s['pct_rupture']:5.1f}% pivot={s['pct_pivot']:5.1f}%")

    print("\n=== TOP RUPTURE REVERSALS ===")
    for e in rupture_reversals[:5]:
        print(f"  [{e['direction']}] '{e['token']}' S2={e['s2']:.2f} H_pre={e['entropy_pre']:.2f} "
              f"delta_H={e['delta_entropy']:.2f} | {e['author']}: {e['poem'][:40]}")

    print("\n=== TOP PIVOT REVERSALS ===")
    for e in pivot_reversals[:5]:
        print(f"  [{e['direction']}] '{e['token']}' S2={e['s2']:.2f} H_pre={e['entropy_pre']:.2f} "
              f"delta_H={e['delta_entropy']:.2f} | {e['author']}: {e['poem'][:40]}")


if __name__ == "__main__":
    main()
