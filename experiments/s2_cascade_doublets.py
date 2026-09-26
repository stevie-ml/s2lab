"""
S2 Cascade Doublets: Do Adjacent Surprise Tokens Interact?

When two high-S2 tokens appear in close proximity, does the second
suffer "surprise fatigue" — reduced S2 because the first already
raised entropy and signaled that anything goes?

Builds on: aftermath_entropy.md (entropy rises after extreme S2),
           surprise_decay.md (S2 collapses within 1 token),
           s2_markov_transitions.md (lag-1 autocorrelation -0.016)

New angle: looks at SECOND spikes within a window of N tokens, asking
whether proximity to a prior spike systematically reduces S2.
"""

import json
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
SPIKE_THRESHOLD = 3.0
WINDOW_SIZES = [2, 3, 5, 10]
ARTIFACT_THRESHOLD = 0.9  # exclude tokens with p(newline) >= this


def load_clean_tokens(data):
    """Return per-poem lists of clean (non-newline-artifact) token dicts."""
    poems = []
    for poem in data:
        meta = poem.get("metadata", {})
        lang = meta.get("language", "en")
        era = meta.get("era", "")
        if lang != "en":
            continue
        if era in ("cliche_control", "control"):
            continue
        tokens = [
            t for t in poem.get("tokens", [])
            if t.get("p_newline", 0) < ARTIFACT_THRESHOLD
        ]
        if len(tokens) < 10:
            continue
        poems.append({
            "title": meta.get("title", "?"),
            "author": meta.get("author", "?"),
            "era": era,
            "tokens": tokens,
        })
    return poems


def classify_spikes(tokens, window):
    """
    For each spike (S2 >= SPIKE_THRESHOLD), classify as:
      - isolated: no other spike within `window` positions
      - first_of_doublet: followed by another spike within `window`
      - second_of_doublet: preceded by another spike within `window`
      - interior: surrounded by spikes on both sides
    Returns list of (s2, classification, distance_to_prior, distance_to_next).
    """
    spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
    spike_set = set(spike_positions)
    results = []
    for idx, pos in enumerate(spike_positions):
        s2 = tokens[pos]["s2"]
        # distance to prior spike
        prior_dist = pos - spike_positions[idx - 1] if idx > 0 else 999
        # distance to next spike
        next_dist = spike_positions[idx + 1] - pos if idx < len(spike_positions) - 1 else 999
        has_prior_close = prior_dist <= window
        has_next_close = next_dist <= window
        if has_prior_close and has_next_close:
            label = "interior"
        elif has_prior_close:
            label = "second_of_doublet"
        elif has_next_close:
            label = "first_of_doublet"
        else:
            label = "isolated"
        results.append({
            "s2": s2,
            "label": label,
            "prior_dist": prior_dist,
            "next_dist": next_dist,
            "pos": pos,
            "entropy_at_spike": tokens[pos]["entropy"],
            "surprisal_at_spike": tokens[pos]["surprisal"],
        })
    return results


def analyze_s2_by_distance(poems):
    """
    For each second spike, record S2 as a function of distance from prior spike.
    """
    by_distance = defaultdict(list)
    for poem in poems:
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        for idx in range(1, len(spike_positions)):
            pos = spike_positions[idx]
            prev_pos = spike_positions[idx - 1]
            dist = pos - prev_pos
            s2 = tokens[pos]["s2"]
            entropy = tokens[pos]["entropy"]
            by_distance[dist].append({"s2": s2, "entropy": entropy})
    return by_distance


def analyze_entropy_at_second_spike(poems):
    """
    Compare entropy at isolated spikes vs. second spikes.
    High entropy = model already uncertain = less genuine surprise.
    """
    isolated_entropy = []
    second_entropy = []
    isolated_s2 = []
    second_s2 = []
    for poem in poems:
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        spike_set = set(spike_positions)
        for idx, pos in enumerate(spike_positions):
            prior_dist = pos - spike_positions[idx - 1] if idx > 0 else 999
            entropy = tokens[pos]["entropy"]
            s2 = tokens[pos]["s2"]
            if prior_dist <= 5:
                second_entropy.append(entropy)
                second_s2.append(s2)
            elif prior_dist > 10:
                isolated_entropy.append(entropy)
                isolated_s2.append(s2)
    return {
        "isolated": {"entropy": isolated_entropy, "s2": isolated_s2},
        "second": {"entropy": second_entropy, "s2": second_s2},
    }


def era_doublet_profiles(poems, window=5):
    """Per-era: what fraction of spikes are doublet vs. isolated, and mean S2."""
    by_era = defaultdict(lambda: {"isolated": [], "doublet": []})
    for poem in poems:
        era = poem["era"]
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        for idx, pos in enumerate(spike_positions):
            prior_dist = pos - spike_positions[idx - 1] if idx > 0 else 999
            s2 = tokens[pos]["s2"]
            if prior_dist <= window:
                by_era[era]["doublet"].append(s2)
            else:
                by_era[era]["isolated"].append(s2)
    return dict(by_era)


def poet_doublet_profiles(poems, window=5):
    """Per-poet: what fraction of spikes are doublet vs. isolated, and mean S2."""
    by_poet = defaultdict(lambda: {"isolated": [], "doublet": []})
    for poem in poems:
        author = poem["author"]
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        for idx, pos in enumerate(spike_positions):
            prior_dist = pos - spike_positions[idx - 1] if idx > 0 else 999
            s2 = tokens[pos]["s2"]
            if prior_dist <= window:
                by_poet[author]["doublet"].append(s2)
            else:
                by_poet[author]["isolated"].append(s2)
    return dict(by_poet)


def mean(lst):
    return sum(lst) / len(lst) if lst else float('nan')


def main():
    with open(CORPUS_PATH) as f:
        data = json.load(f)

    poems = load_clean_tokens(data)
    print(f"Loaded {len(poems)} clean English poems")

    # --- 1. Cascade effect at multiple window sizes ---
    print("\n=== FINDING 1: Cascade Effect at Multiple Window Sizes ===")
    print(f"{'Window':>8} {'Isolated_n':>12} {'Isolated_S2':>14} {'Second_n':>12} {'Second_S2':>12} {'Delta_S2':>10}")
    for window in WINDOW_SIZES:
        isolated_s2 = []
        second_s2 = []
        for poem in poems:
            for rec in classify_spikes(poem["tokens"], window):
                if rec["label"] == "isolated":
                    isolated_s2.append(rec["s2"])
                elif rec["label"] == "second_of_doublet":
                    second_s2.append(rec["s2"])
        m_iso = mean(isolated_s2)
        m_sec = mean(second_s2)
        print(f"{window:>8} {len(isolated_s2):>12} {m_iso:>14.3f} {len(second_s2):>12} {m_sec:>12.3f} {m_sec - m_iso:>10.3f}")

    # --- 2. S2 as a function of distance from prior spike ---
    print("\n=== FINDING 2: S2 by Distance from Prior Spike ===")
    by_dist = analyze_s2_by_distance(poems)
    print(f"{'Distance':>10} {'n':>6} {'mean_S2':>10} {'mean_H':>10}")
    for dist in sorted(by_dist.keys()):
        if dist > 15:
            continue
        recs = by_dist[dist]
        s2_vals = [r["s2"] for r in recs]
        h_vals = [r["entropy"] for r in recs]
        print(f"{dist:>10} {len(recs):>6} {mean(s2_vals):>10.3f} {mean(h_vals):>10.3f}")

    # --- 3. Entropy comparison: isolated vs. second spikes ---
    print("\n=== FINDING 3: Entropy at Isolated vs. Second Spikes (window=5) ===")
    comp = analyze_entropy_at_second_spike(poems)
    iso = comp["isolated"]
    sec = comp["second"]
    print(f"Group       {'n':>6} {'mean_S2':>10} {'mean_H':>10}")
    print(f"Isolated    {len(iso['s2']):>6} {mean(iso['s2']):>10.3f} {mean(iso['entropy']):>10.3f}")
    print(f"Second(≤5)  {len(sec['s2']):>6} {mean(sec['s2']):>10.3f} {mean(sec['entropy']):>10.3f}")
    delta_s2 = mean(sec["s2"]) - mean(iso["s2"])
    delta_h = mean(sec["entropy"]) - mean(iso["entropy"])
    print(f"  Delta S2 = {delta_s2:.3f},  Delta H = {delta_h:.3f}")

    # --- 4. What fraction of each spike's S2 is 'entropy-absorbed'? ---
    print("\n=== FINDING 4: Surprisal vs. S2 at Second Spikes ===")
    iso_surp = mean([data["tokens"][i]["surprisal"]
                     for poem in poems
                     for data_poem in [poem]
                     for i, t in enumerate(data_poem["tokens"])
                     if t["s2"] >= SPIKE_THRESHOLD
                     if not any(
                         abs(j - i) <= 5 and j != i and data_poem["tokens"][j]["s2"] >= SPIKE_THRESHOLD
                         for j in range(max(0, i-5), i)
                     )
                    ] if False else [])
    # simpler approach
    iso_surprisals, iso_entropies = [], []
    sec_surprisals, sec_entropies = [], []
    for poem in poems:
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        for idx, pos in enumerate(spike_positions):
            prior_dist = pos - spike_positions[idx - 1] if idx > 0 else 999
            s = tokens[pos]["surprisal"]
            h = tokens[pos]["entropy"]
            if prior_dist > 10:
                iso_surprisals.append(s)
                iso_entropies.append(h)
            elif prior_dist <= 5:
                sec_surprisals.append(s)
                sec_entropies.append(h)
    print(f"{'Group':>12} {'n':>6} {'mean_surp':>12} {'mean_ent':>12} {'mean_s2':>10}")
    print(f"{'Isolated':>12} {len(iso_surprisals):>6} {mean(iso_surprisals):>12.3f} {mean(iso_entropies):>12.3f} {mean([s-h for s,h in zip(iso_surprisals,iso_entropies)]):>10.3f}")
    print(f"{'Second(≤5)':>12} {len(sec_surprisals):>6} {mean(sec_surprisals):>12.3f} {mean(sec_entropies):>12.3f} {mean([s-h for s,h in zip(sec_surprisals,sec_entropies)]):>10.3f}")

    # --- 5. Era profiles ---
    print("\n=== FINDING 5: Era-Level Doublet Profiles (window=5) ===")
    era_data = era_doublet_profiles(poems, window=5)
    rows = []
    for era, d in era_data.items():
        n_iso = len(d["isolated"])
        n_dbl = len(d["doublet"])
        if n_iso + n_dbl < 5:
            continue
        dbl_rate = n_dbl / (n_iso + n_dbl)
        rows.append((era, n_iso, n_dbl, dbl_rate, mean(d["isolated"]), mean(d["doublet"])))
    rows.sort(key=lambda x: -x[3])
    print(f"{'Era':>25} {'iso_n':>6} {'dbl_n':>6} {'dbl%':>8} {'iso_S2':>8} {'dbl_S2':>8} {'ratio':>8}")
    for era, n_iso, n_dbl, dbl_rate, s2_iso, s2_dbl in rows:
        ratio = s2_dbl / s2_iso if s2_iso > 0 else float('nan')
        print(f"{era:>25} {n_iso:>6} {n_dbl:>6} {dbl_rate*100:>7.1f}% {s2_iso:>8.2f} {s2_dbl:>8.2f} {ratio:>8.2f}")

    # --- 6. Poet profiles ---
    print("\n=== FINDING 6: Poet-Level Doublet Profiles (window=5, min 10 total spikes) ===")
    poet_data = poet_doublet_profiles(poems, window=5)
    rows = []
    for author, d in poet_data.items():
        n_iso = len(d["isolated"])
        n_dbl = len(d["doublet"])
        if n_iso + n_dbl < 10:
            continue
        dbl_rate = n_dbl / (n_iso + n_dbl)
        rows.append((author, n_iso, n_dbl, dbl_rate, mean(d["isolated"]), mean(d["doublet"])))
    rows.sort(key=lambda x: -x[3])
    print(f"{'Poet':>35} {'iso_n':>6} {'dbl_n':>6} {'dbl%':>8} {'iso_S2':>8} {'dbl_S2':>8}")
    for author, n_iso, n_dbl, dbl_rate, s2_iso, s2_dbl in rows[:20]:
        print(f"{author:>35} {n_iso:>6} {n_dbl:>6} {dbl_rate*100:>7.1f}% {s2_iso:>8.2f} {s2_dbl:>8.2f}")

    # --- 7. Examples of high-S2 doublets ---
    print("\n=== FINDING 7: Most Remarkable Doublet Pairs ===")
    doublet_examples = []
    for poem in poems:
        tokens = poem["tokens"]
        spike_positions = [i for i, t in enumerate(tokens) if t["s2"] >= SPIKE_THRESHOLD]
        for idx in range(1, len(spike_positions)):
            pos2 = spike_positions[idx]
            pos1 = spike_positions[idx - 1]
            dist = pos2 - pos1
            if dist <= 5:
                s2_pair = tokens[pos1]["s2"] + tokens[pos2]["s2"]
                doublet_examples.append({
                    "author": poem["author"],
                    "title": poem["title"],
                    "pos1": pos1, "pos2": pos2, "dist": dist,
                    "tok1": tokens[pos1]["token"],
                    "tok2": tokens[pos2]["token"],
                    "s2_1": tokens[pos1]["s2"],
                    "s2_2": tokens[pos2]["s2"],
                    "s2_pair": s2_pair,
                    "ctx1": tokens[pos1].get("context_before", "")[-30:],
                    "expected1": tokens[pos1]["alternatives"][0]["token"] if tokens[pos1]["alternatives"] else "?",
                    "expected2": tokens[pos2]["alternatives"][0]["token"] if tokens[pos2]["alternatives"] else "?",
                })
    doublet_examples.sort(key=lambda x: -x["s2_pair"])
    print(f"Total doublet pairs (dist≤5): {len(doublet_examples)}")
    print()
    print(f"{'Rank':>4} {'Author':>25} {'S2_1':>6} {'S2_2':>6} {'Dist':>5} {'Token1':>12} {'(exp)':>10} {'Token2':>12} {'(exp)':>10}")
    for i, ex in enumerate(doublet_examples[:15], 1):
        print(f"{i:>4} {ex['author'][:25]:>25} {ex['s2_1']:>6.1f} {ex['s2_2']:>6.1f} {ex['dist']:>5} {ex['tok1'][:12]:>12} ({ex['expected1'][:8]:>8}) {ex['tok2'][:12]:>12} ({ex['expected2'][:8]:>8})")
        print(f"       Title: {ex['title'][:60]}")

    # Save results as JSON
    results = {
        "cascade_by_window": {},
        "s2_by_distance": {},
        "entropy_comparison": {
            "isolated_mean_s2": mean(iso_surprisals) - mean(iso_entropies),
            "second_mean_s2": mean(sec_surprisals) - mean(sec_entropies),
            "isolated_mean_entropy": mean(iso_entropies),
            "second_mean_entropy": mean(sec_entropies),
            "isolated_n": len(iso_surprisals),
            "second_n": len(sec_surprisals),
        },
        "top_doublet_examples": doublet_examples[:20],
    }
    for window in WINDOW_SIZES:
        isolated_s2, second_s2 = [], []
        for poem in poems:
            for rec in classify_spikes(poem["tokens"], window):
                if rec["label"] == "isolated":
                    isolated_s2.append(rec["s2"])
                elif rec["label"] == "second_of_doublet":
                    second_s2.append(rec["s2"])
        results["cascade_by_window"][str(window)] = {
            "isolated_n": len(isolated_s2),
            "isolated_mean_s2": mean(isolated_s2),
            "second_n": len(second_s2),
            "second_mean_s2": mean(second_s2),
            "delta_s2": mean(second_s2) - mean(isolated_s2),
        }
    for dist, recs in by_dist.items():
        if dist <= 15:
            results["s2_by_distance"][str(dist)] = {
                "n": len(recs),
                "mean_s2": mean([r["s2"] for r in recs]),
                "mean_entropy": mean([r["entropy"] for r in recs]),
            }
    with open("results/s2_cascade_doublets.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nResults saved to results/s2_cascade_doublets.json")


if __name__ == "__main__":
    main()
