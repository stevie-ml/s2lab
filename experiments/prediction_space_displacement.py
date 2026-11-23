"""
Prediction Space Displacement: Does a High-S2 Token Redirect the Poem's Trajectory?

Previous work measured what FOLLOWS a surprise (aftermath_entropy, post_surprise_signature)
and what PRECEDES it (pre_peak_setup). This experiment asks a different question:

Does a high-S2 token *fundamentally redirect* GPT-2's prediction landscape, or is it a
local detour that leaves the poem's overall trajectory intact?

Method: For each high-S2 token at position i, compute the Jaccard similarity between
the sets of top-10 predicted alternatives at:
  - position i-1 (the token just BEFORE the surprise)
  - position i+1 (the token just AFTER the surprise)

Jaccard(A, B) = |A ∩ B| / |A ∪ B|

Low Jaccard = the prediction space changed dramatically around the surprise.
High Jaccard = the prediction space was largely unchanged — the surprise was a local detour.

We call this the "Prediction Space Displacement" (PSD) around a surprise.

Hypotheses:
1. Larger S2 spikes should produce lower PSD (more displacement).
2. Poets known for syntactic disruption (Language poetry, OuLiPo) should produce lower PSD.
3. Formally constrained poems (sonnets, villanelles) should produce higher PSD — surprises
   that don't disrupt the trajectory, because syntax forces the poem back on track.
4. PSD at the VOLTA of a sonnet should be lower than PSD elsewhere in the sonnet.

Output: results/prediction_space_displacement.json
"""

import json
import math
from collections import defaultdict

CORPUS = "results/corpus_results.json"
OUTPUT = "results/prediction_space_displacement.json"

S2_THRESHOLD = 2.0        # define "high-S2" for this analysis
MIN_WINDOW = 1            # need at least 1 token before and after
NEWLINE_PROB_THRESHOLD = 0.9  # exclude stanza-break artifacts


def jaccard(set_a: set, set_b: set) -> float:
    if not set_a and not set_b:
        return 1.0
    intersection = set_a & set_b
    union = set_a | set_b
    return len(intersection) / len(union) if union else 0.0


def top10_token_set(token_data: dict) -> set:
    alts = token_data.get("alternatives", [])
    return {alt["token"].strip().lower() for alt in alts[:10]}


def compute_poem_psd(tokens: list) -> list:
    """
    For each high-S2 token in the poem, compute PSD = Jaccard(alts[i-1], alts[i+1]).
    Returns list of dicts with position, token, s2, psd, and other metrics.
    """
    n = len(tokens)
    results = []

    for i, tok in enumerate(tokens):
        # skip artifact positions
        if tok.get("p_newline", 0) >= NEWLINE_PROB_THRESHOLD:
            continue

        s2 = tok.get("s2", 0.0)
        if s2 < S2_THRESHOLD:
            continue

        # need at least one neighbor on each side, non-artifact
        # find nearest non-artifact neighbor before i
        prev_idx = None
        for j in range(i - 1, max(i - 5, -1), -1):
            if j >= 0 and tokens[j].get("p_newline", 0) < NEWLINE_PROB_THRESHOLD:
                prev_idx = j
                break

        next_idx = None
        for j in range(i + 1, min(i + 5, n)):
            if tokens[j].get("p_newline", 0) < NEWLINE_PROB_THRESHOLD:
                next_idx = j
                break

        if prev_idx is None or next_idx is None:
            continue

        alts_prev = top10_token_set(tokens[prev_idx])
        alts_next = top10_token_set(tokens[next_idx])
        psd = jaccard(alts_prev, alts_next)

        # also compute: does the actual token appear in alts[i+1]?
        actual = tok.get("token", "").strip().lower()
        actual_in_next = actual in alts_next

        # entropy of prediction at current position (from stored entropy)
        entropy = tok.get("entropy", 0.0)
        surprisal = tok.get("surprisal", 0.0)
        rank = tok.get("rank", 0)

        results.append({
            "position": tok["position"],
            "token": tok["token"],
            "s2": s2,
            "surprisal": surprisal,
            "entropy": entropy,
            "rank": rank,
            "psd": psd,
            "actual_in_next_alts": actual_in_next,
        })

    return results


def bin_s2(s2: float) -> str:
    if s2 < 3:
        return "2–3"
    elif s2 < 5:
        return "3–5"
    elif s2 < 8:
        return "5–8"
    elif s2 < 12:
        return "8–12"
    else:
        return "12+"


def main():
    with open(CORPUS) as f:
        data = json.load(f)

    # Aggregate by era
    era_records = defaultdict(list)
    # Aggregate by poet
    poet_records = defaultdict(list)
    # Aggregate by S2 bin
    s2bin_records = defaultdict(list)
    # All displacement events
    all_events = []
    # Poem-level aggregates
    poem_aggregates = []

    for poem in data:
        meta = poem.get("metadata", {})
        era = meta.get("era", "unknown")
        poet = meta.get("author", "unknown")
        title = meta.get("title", "?")
        tokens = poem.get("tokens", [])

        psd_events = compute_poem_psd(tokens)
        if not psd_events:
            continue

        for ev in psd_events:
            ev["era"] = era
            ev["poet"] = poet
            ev["title"] = title
            all_events.append(ev)

            era_records[era].append(ev["psd"])
            poet_records[poet].append(ev["psd"])
            s2bin_records[bin_s2(ev["s2"])].append(ev["psd"])

        psds = [e["psd"] for e in psd_events]
        mean_psd = sum(psds) / len(psds)
        poem_aggregates.append({
            "title": title,
            "author": poet,
            "era": era,
            "n_events": len(psd_events),
            "mean_psd": round(mean_psd, 4),
            "min_psd": round(min(psds), 4),
        })

    # Summarize by S2 bin
    s2bin_summary = {}
    for b in ["2–3", "3–5", "5–8", "8–12", "12+"]:
        vals = s2bin_records.get(b, [])
        if vals:
            s2bin_summary[b] = {
                "n": len(vals),
                "mean_psd": round(sum(vals) / len(vals), 4),
            }

    # Summarize by era (min 10 events)
    era_summary = {}
    for era, vals in era_records.items():
        if len(vals) >= 5:
            era_summary[era] = {
                "n": len(vals),
                "mean_psd": round(sum(vals) / len(vals), 4),
            }

    # Summarize by poet (min 5 events)
    poet_summary = {}
    for poet, vals in poet_records.items():
        if len(vals) >= 5:
            poet_summary[poet] = {
                "n": len(vals),
                "mean_psd": round(sum(vals) / len(vals), 4),
            }

    # Find the most and least disruptive surprise events
    all_events.sort(key=lambda e: e["psd"])
    top_displaced = all_events[:20]   # lowest PSD = most displaced
    low_displaced = all_events[-20:]  # highest PSD = least displaced (local detours)

    # Global stats
    all_psds = [e["psd"] for e in all_events]
    global_mean = sum(all_psds) / len(all_psds) if all_psds else 0

    # Correlation: s2 vs psd
    # Pearson manually
    n = len(all_psds)
    s2s = [e["s2"] for e in all_events]
    if n > 1:
        mean_s2 = sum(s2s) / n
        mean_psd = global_mean
        cov = sum((s - mean_s2) * (p - mean_psd) for s, p in zip(s2s, all_psds)) / n
        std_s2 = (sum((s - mean_s2) ** 2 for s in s2s) / n) ** 0.5
        std_psd = (sum((p - mean_psd) ** 2 for p in all_psds) / n) ** 0.5
        pearson_r = cov / (std_s2 * std_psd) if std_s2 * std_psd > 0 else 0
    else:
        pearson_r = 0

    output = {
        "total_events": len(all_events),
        "global_mean_psd": round(global_mean, 4),
        "pearson_r_s2_vs_psd": round(pearson_r, 4),
        "s2bin_summary": s2bin_summary,
        "era_summary": {
            k: v for k, v in sorted(era_summary.items(), key=lambda x: x[1]["mean_psd"])
        },
        "poet_summary": {
            k: v for k, v in sorted(poet_summary.items(), key=lambda x: x[1]["mean_psd"])
        },
        "top_displaced_events": [
            {k: v for k, v in e.items() if k not in ("actual_in_next_alts",)}
            for e in top_displaced
        ],
        "low_displaced_events": [
            {k: v for k, v in e.items() if k not in ("actual_in_next_alts",)}
            for e in low_displaced
        ],
        "poem_aggregates": sorted(poem_aggregates, key=lambda x: x["mean_psd"])[:30],
    }

    with open(OUTPUT, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Done. {len(all_events)} displacement events analyzed.")
    print(f"Global mean PSD: {global_mean:.4f}")
    print(f"Pearson r (S2 vs PSD): {pearson_r:.4f}")
    print(f"Saved to {OUTPUT}")


if __name__ == "__main__":
    main()
