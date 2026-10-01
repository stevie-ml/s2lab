"""
S2 Transition Entropy: How Open Is the Road After Surprise?

Building on s2_markov_transitions.md, which found that poetry shows
a flat transition distribution from HIGH_SURPRISE states while prose
collapses back to CONFORM. This experiment QUANTIFIES that difference
by computing the Shannon entropy of each row of the Markov transition
matrix — the "transition entropy" — per zone, era, and poetry/prose.

Key questions:
  1. Is transition entropy from HIGH_SURPRISE higher in poetry than prose?
  2. Does transition entropy vary by era? (ballads vs free verse vs haiku)
  3. Which eras have the LOWEST transition entropy from surprise
     (structured predictability) vs highest (open field)?
  4. What do HIGH→HIGH chains look like? (examples of sustained surprise)

Builds on: s2_markov_transitions.md, aftermath_entropy.md,
           surprise_decay_curves.md, spike_symmetry_analysis.md
"""

import json
import math
from collections import defaultdict

CORPUS_PATH = "results/corpus_results.json"
ARTIFACT_THRESHOLD = 0.9  # exclude tokens where p(newline) >= this
MIN_PAIRS = 5             # minimum transition pairs to include a zone/era

# S2 zones (same as s2_markov_transitions.py)
ZONES = [
    ("deep_conform",  float("-inf"), -3.0),
    ("conform",       -3.0,          -0.5),
    ("neutral",       -0.5,           0.5),
    ("surprise",       0.5,           3.0),
    ("high_surprise",  3.0,  float("inf")),
]
ZONE_NAMES = [z[0] for z in ZONES]

def s2_to_zone(s2):
    for name, lo, hi in ZONES:
        if lo <= s2 < hi:
            return name
    return ZONE_NAMES[-1]

def transition_entropy(row_counts):
    """Shannon entropy of the row distribution."""
    total = sum(row_counts.values())
    if total == 0:
        return None
    h = 0.0
    for count in row_counts.values():
        if count > 0:
            p = count / total
            h -= p * math.log2(p)
    return h

def load_clean_tokens(data, include_control=False):
    poems = []
    for poem in data:
        meta = poem.get("metadata", {})
        lang = meta.get("language", "en")
        era = meta.get("era", "")
        if lang != "en":
            continue
        if not include_control and era in ("cliche_control", "control"):
            poems_ctrl = []
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

def load_control(data):
    ctrl = []
    for poem in data:
        meta = poem.get("metadata", {})
        if meta.get("era", "") not in ("control", "cliche_control"):
            continue
        tokens = [
            t for t in poem.get("tokens", [])
            if t.get("p_newline", 0) < ARTIFACT_THRESHOLD
        ]
        if len(tokens) < 10:
            continue
        ctrl.append({"title": meta.get("title","?"), "era": meta.get("era",""), "tokens": tokens})
    return ctrl

def build_transition_matrix(poems):
    """Build {from_zone: {to_zone: count}} from all consecutive clean token pairs."""
    matrix = {z: defaultdict(int) for z in ZONE_NAMES}
    for poem in poems:
        toks = poem["tokens"]
        for i in range(len(toks) - 1):
            z1 = s2_to_zone(toks[i]["s2"])
            z2 = s2_to_zone(toks[i+1]["s2"])
            matrix[z1][z2] += 1
    return matrix

def matrix_transition_entropies(matrix):
    """Return {zone: entropy} for each row of the matrix."""
    return {zone: transition_entropy(dict(matrix[zone])) for zone in ZONE_NAMES}

def collect_high_high_chains(poems, chain_min=2, s2_threshold=3.0):
    """Find sequences of ≥ chain_min consecutive high-S2 tokens."""
    chains = []
    for poem in poems:
        toks = poem["tokens"]
        i = 0
        while i < len(toks):
            if toks[i]["s2"] >= s2_threshold:
                j = i
                while j < len(toks) and toks[j]["s2"] >= s2_threshold:
                    j += 1
                if j - i >= chain_min:
                    chains.append({
                        "poem": poem["title"],
                        "author": poem["author"],
                        "era": poem["era"],
                        "length": j - i,
                        "tokens": [toks[k]["token"] for k in range(i, j)],
                        "s2_values": [round(toks[k]["s2"], 2) for k in range(i, j)],
                        "avg_s2": round(sum(toks[k]["s2"] for k in range(i,j))/(j-i), 2),
                    })
                i = j
            else:
                i += 1
    return sorted(chains, key=lambda c: -c["avg_s2"])

def main():
    with open(CORPUS_PATH) as f:
        data = json.load(f)

    poetry = load_clean_tokens(data)
    ctrl = load_control(data)

    # ── 1. Overall poetry vs prose transition entropy ──────────────────────
    poetry_matrix = build_transition_matrix(poetry)
    ctrl_matrix = build_transition_matrix(ctrl)

    poetry_te = matrix_transition_entropies(poetry_matrix)
    ctrl_te = matrix_transition_entropies(ctrl_matrix)

    print("=" * 70)
    print("TRANSITION ENTROPY: HOW OPEN IS THE ROAD AFTER SURPRISE?")
    print("=" * 70)
    print()
    print("Shannon entropy of the transition distribution from each S2 zone.")
    print("Max possible entropy = log2(5) = 2.32 bits (perfectly flat)")
    print()
    print(f"{'Zone':<20} {'Poetry H (bits)':>17} {'Prose H (bits)':>15} {'Δ (poetry−prose)':>18}")
    print("-" * 72)
    for zone in ZONE_NAMES:
        ph = poetry_te.get(zone)
        ch = ctrl_te.get(zone)
        delta = (ph - ch) if ph is not None and ch is not None else None
        ph_str = f"{ph:.3f}" if ph else "n/a"
        ch_str = f"{ch:.3f}" if ch else "n/a"
        d_str  = f"{delta:+.3f}" if delta is not None else "n/a"
        print(f"  {zone:<18} {ph_str:>17} {ch_str:>15} {d_str:>18}")
    print()

    # ── 2. Transition entropy by era (HIGH_SURPRISE row only) ──────────────
    ERA_MIN = 20  # minimum transitions from HIGH_SURPRISE to include era
    era_poems = defaultdict(list)
    for poem in poetry:
        era_poems[poem["era"]].append(poem)

    print("TRANSITION ENTROPY FROM HIGH_SURPRISE BY ERA")
    print("-" * 60)
    print("(Only eras with ≥20 transitions from high-surprise zone)")
    print()
    era_results = []
    for era, plist in era_poems.items():
        m = build_transition_matrix(plist)
        total = sum(m["high_surprise"].values())
        if total < ERA_MIN:
            continue
        h = transition_entropy(dict(m["high_surprise"]))
        # Also compute the proportion returning to high_surprise
        p_hh = m["high_surprise"].get("high_surprise", 0) / total if total > 0 else 0
        p_conf = (m["high_surprise"].get("conform", 0) + m["high_surprise"].get("deep_conform", 0)) / total
        era_results.append({
            "era": era,
            "n_transitions": total,
            "H_high": h,
            "p_HH": p_hh,
            "p_conform": p_conf,
        })

    era_results.sort(key=lambda x: -x["H_high"])
    print(f"  {'Era':<25} {'n':>6} {'H (bits)':>10} {'P(→HH)':>10} {'P(→conf)':>11}")
    print(f"  {'-'*25} {'-'*6} {'-'*10} {'-'*10} {'-'*11}")
    for r in era_results:
        print(f"  {r['era']:<25} {r['n_transitions']:>6} {r['H_high']:>10.3f} "
              f"{r['p_HH']:>10.1%} {r['p_conform']:>11.1%}")

    # Prose comparison
    ctrl_total = sum(ctrl_matrix["high_surprise"].values())
    if ctrl_total > 0:
        h_ctrl = transition_entropy(dict(ctrl_matrix["high_surprise"]))
        p_hh_ctrl = ctrl_matrix["high_surprise"].get("high_surprise", 0) / ctrl_total
        p_conf_ctrl = (ctrl_matrix["high_surprise"].get("conform", 0) +
                       ctrl_matrix["high_surprise"].get("deep_conform", 0)) / ctrl_total
        print(f"  {'[prose control]':<25} {ctrl_total:>6} {h_ctrl:>10.3f} "
              f"{p_hh_ctrl:>10.1%} {p_conf_ctrl:>11.1%}")
    print()

    # ── 3. Transition entropy matrix for formal vs free verse ──────────────
    FORMAL_ERAS = {"ballad", "fixed_form", "haiku", "nursery_rhyme",
                   "biblical", "metaphysical", "early_modern", "victorian",
                   "romantic", "19th_century", "18th_century"}
    FREE_ERAS   = {"modernist", "confessional", "contemporary", "beat",
                   "new_york_school", "language", "prose_poetry", "deep_image",
                   "concrete", "oulipo", "found_poetry", "surrealist"}

    formal = [p for p in poetry if p["era"] in FORMAL_ERAS]
    free   = [p for p in poetry if p["era"] in FREE_ERAS]

    formal_m = build_transition_matrix(formal)
    free_m   = build_transition_matrix(free)

    formal_te = matrix_transition_entropies(formal_m)
    free_te   = matrix_transition_entropies(free_m)

    print("TRANSITION ENTROPY: FORMAL vs FREE VERSE")
    print("-" * 60)
    print(f"{'Zone':<20} {'Formal H':>10} {'Free H':>10} {'Δ (free−formal)':>17}")
    print("-" * 60)
    for zone in ZONE_NAMES:
        fh = formal_te.get(zone)
        frh = free_te.get(zone)
        delta = (frh - fh) if fh is not None and frh is not None else None
        fh_s  = f"{fh:.3f}"  if fh  else "n/a"
        frh_s = f"{frh:.3f}" if frh else "n/a"
        d_s   = f"{delta:+.3f}" if delta is not None else "n/a"
        print(f"  {zone:<18} {fh_s:>10} {frh_s:>10} {d_s:>17}")
    print()

    # ── 4. HIGH→HIGH chains: what do they look like? ──────────────────────
    print("HIGH→HIGH CHAINS: SUSTAINED SURPRISE (≥2 consecutive tokens, S2 ≥ 3)")
    print("-" * 70)
    chains = collect_high_high_chains(poetry, chain_min=2, s2_threshold=3.0)
    print(f"Total HIGH→HIGH chains found: {len(chains)}")
    print()

    # Count chains by era
    era_chain_count = defaultdict(int)
    for c in chains:
        era_chain_count[c["era"]] += 1
    print("Chains by era:")
    for era, count in sorted(era_chain_count.items(), key=lambda x: -x[1])[:10]:
        print(f"  {era}: {count}")
    print()

    # Longest / highest-S2 chains
    print("Top 15 highest-S2 chains (artifact-free):")
    print(f"  {'Poem':<35} {'Era':<18} {'Len':>4} {'Avg S2':>8}  Tokens")
    print(f"  {'-'*35} {'-'*18} {'-'*4} {'-'*8}  ------")
    for c in chains[:15]:
        tok_str = repr("".join(c["tokens"]))[:30]
        print(f"  {c['poem'][:35]:<35} {c['era']:<18} {c['length']:>4} {c['avg_s2']:>8.2f}  {tok_str}")
    print()

    # ── 5. Chain length distribution ──────────────────────────────────────
    from collections import Counter
    len_dist = Counter(c["length"] for c in chains)
    print("Chain length distribution:")
    for length in sorted(len_dist):
        print(f"  length {length}: {len_dist[length]} chains")
    print()

    print("=" * 70)
    print("DONE")

    return {
        "poetry_transition_entropy": {z: poetry_te.get(z) for z in ZONE_NAMES},
        "prose_transition_entropy": {z: ctrl_te.get(z) for z in ZONE_NAMES},
        "era_high_surprise_transition_entropy": era_results,
        "n_chains": len(chains),
        "chain_len_dist": dict(len_dist),
    }

if __name__ == "__main__":
    results = main()
    with open("results/s2_transition_entropy.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved to results/s2_transition_entropy.json")
