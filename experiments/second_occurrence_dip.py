"""
Second-Occurrence Dip: Does repeated word use lower S₂?

When a word appears for the first time in a poem, does its second, third,
or Nth occurrence have lower S₂? GPT-2 reads left-to-right, so by the
time a word appears a second time, the model has "seen" it once and may
assign it higher probability — lowering its S₂.

This tests whether poets "educate" the model as the poem proceeds,
and whether structural repetition (anaphora, refrain) exploits this
expectation dynamic.
"""

import json
import re
from collections import defaultdict
import statistics

RESULTS_PATH = "results/corpus_results.json"

def normalize(token: str) -> str:
    return token.strip().lower().strip(".,!?;:\"'()-—")

def run_experiment():
    with open(RESULTS_PATH) as f:
        data = json.load(f)

    # Filter English poems only
    poems = [d for d in data if d["metadata"].get("language", "en") == "en"]
    print(f"Analyzing {len(poems)} English poems")

    # Per-occurrence-position data (1st, 2nd, 3rd+ occurrence)
    occurrence_s2 = defaultdict(list)   # occurrence_number -> [s2 values]

    # Words that appear exactly 2 times: delta S₂
    two_occurrence_deltas = []  # (word, poem_title, s2_1, s2_2, delta)

    # Words that appear 3+ times: track trajectory
    multi_trajectories = []  # (word, poem_title, [s2_by_occurrence])

    # Era-level aggregates
    era_first = defaultdict(list)
    era_second = defaultdict(list)

    # Words that RISE on second occurrence (surprise recovery)
    risers = []

    # Per-poem summary
    poem_avg_first = []
    poem_avg_second = []

    for poem in poems:
        tokens = poem["tokens"]
        era = poem["metadata"].get("era", "unknown")
        title = poem["metadata"].get("title", "?")
        author = poem["metadata"].get("author", "?")

        # Build token stream with occurrence tracking
        seen_normalized = defaultdict(int)  # normalized_word -> count
        occurrence_record = defaultdict(list)  # normalized_word -> [(position, s2)]

        for tok in tokens:
            word = tok["token"]
            s2 = tok["s2"]
            norm = normalize(word)
            if not norm or len(norm) < 2:
                continue
            # Skip tokens that are purely whitespace/newline
            if norm in {"\n", " ", "", "\\n"}:
                continue

            seen_normalized[norm] += 1
            occ_num = seen_normalized[norm]
            occurrence_record[norm].append((occ_num, s2))

            # Aggregate
            if occ_num <= 6:
                occurrence_s2[occ_num].append(s2)

            era_first[era].append(s2) if occ_num == 1 else None
            era_second[era].append(s2) if occ_num == 2 else None

        # Find two-occurrence words
        poem_first_s2 = []
        poem_second_s2 = []
        for word, records in occurrence_record.items():
            if len(records) == 2:
                s2_1 = records[0][1]
                s2_2 = records[1][1]
                delta = s2_2 - s2_1
                two_occurrence_deltas.append((word, title, author, s2_1, s2_2, delta))
                poem_first_s2.append(s2_1)
                poem_second_s2.append(s2_2)
                if delta > 2.0:  # significant rise
                    risers.append((word, title, author, s2_1, s2_2, delta))
            elif len(records) >= 3:
                s2_trajectory = [r[1] for r in records[:6]]
                multi_trajectories.append((word, title, author, s2_trajectory))
                poem_first_s2.append(s2_trajectory[0])
                if len(s2_trajectory) > 1:
                    poem_second_s2.append(s2_trajectory[1])

        if poem_first_s2:
            poem_avg_first.append(statistics.mean(poem_first_s2))
        if poem_second_s2:
            poem_avg_second.append(statistics.mean(poem_second_s2))

    print("\n=== OVERALL: S₂ BY OCCURRENCE NUMBER ===")
    print(f"{'Occurrence':<12} {'n':<8} {'mean S₂':<12} {'median S₂':<12} {'% positive':<12}")
    for occ in range(1, 7):
        vals = occurrence_s2[occ]
        if len(vals) < 5:
            continue
        mean = statistics.mean(vals)
        med = statistics.median(vals)
        pos_pct = 100 * sum(v > 0 for v in vals) / len(vals)
        print(f"{occ:<12} {len(vals):<8} {mean:<12.3f} {med:<12.3f} {pos_pct:<12.1f}%")

    print("\n=== TWO-OCCURRENCE WORDS: S₂ DELTA ===")
    if two_occurrence_deltas:
        all_deltas = [d[5] for d in two_occurrence_deltas]
        drops = [d for d in all_deltas if d < 0]
        rises = [d for d in all_deltas if d > 0]
        print(f"Total two-occurrence pairs: {len(two_occurrence_deltas)}")
        print(f"Mean delta (S₂₂ - S₂₁): {statistics.mean(all_deltas):.3f}")
        print(f"Pairs where S₂ DROPS (2nd < 1st): {len(drops)} ({100*len(drops)/len(all_deltas):.1f}%)")
        print(f"Pairs where S₂ RISES (2nd > 1st): {len(rises)} ({100*len(rises)/len(all_deltas):.1f}%)")
        print(f"Mean drop (when dropping): {statistics.mean(drops):.3f}")
        print(f"Mean rise (when rising): {statistics.mean(rises):.3f}")

    print("\n=== LARGEST S₂ RISES ON 2ND OCCURRENCE ===")
    risers_sorted = sorted(risers, key=lambda x: x[5], reverse=True)[:15]
    print(f"{'Word':<20} {'Poem':<35} {'S₂ 1st':<10} {'S₂ 2nd':<10} {'Delta':<10}")
    for word, title, author, s1, s2, delta in risers_sorted:
        print(f"{word!r:<20} {title[:33]:<35} {s1:<10.2f} {s2:<10.2f} {delta:<10.2f}")

    print("\n=== LARGEST S₂ DROPS ON 2ND OCCURRENCE ===")
    drops_sorted = sorted(two_occurrence_deltas, key=lambda x: x[5])[:15]
    print(f"{'Word':<20} {'Poem':<35} {'S₂ 1st':<10} {'S₂ 2nd':<10} {'Delta':<10}")
    for word, title, author, s1, s2, delta in drops_sorted:
        print(f"{word!r:<20} {title[:33]:<35} {s1:<10.2f} {s2:<10.2f} {delta:<10.2f}")

    print("\n=== MULTI-OCCURRENCE TRAJECTORIES (3+ uses) ===")
    # Group by length to see average trajectory
    traj_by_length = defaultdict(list)
    for word, title, author, traj in multi_trajectories:
        for i, s2 in enumerate(traj):
            traj_by_length[i+1].append(s2)

    print("Average S₂ by occurrence for words used 3+ times:")
    print(f"{'Occurrence':<12} {'n':<8} {'mean S₂':<12}")
    for occ in range(1, 7):
        vals = traj_by_length[occ]
        if len(vals) < 5:
            continue
        print(f"{occ:<12} {len(vals):<8} {statistics.mean(vals):<12.3f}")

    print("\n=== ERA ANALYSIS: FIRST vs SECOND OCCURRENCE ===")
    print(f"{'Era':<25} {'n_1st':<8} {'avg 1st':<10} {'n_2nd':<8} {'avg 2nd':<10} {'delta':<10}")
    era_data = []
    for era in sorted(era_first.keys()):
        first_vals = era_first[era]
        second_vals = era_second[era]
        if len(first_vals) < 10 or len(second_vals) < 5:
            continue
        avg1 = statistics.mean(first_vals)
        avg2 = statistics.mean(second_vals)
        era_data.append((era, len(first_vals), avg1, len(second_vals), avg2, avg2-avg1))

    era_data.sort(key=lambda x: x[5])  # sort by delta
    for row in era_data:
        print(f"{row[0]:<25} {row[1]:<8} {row[2]:<10.3f} {row[3]:<8} {row[4]:<10.3f} {row[5]:<10.3f}")

    print("\n=== EXAMPLES: WORDS THAT GAIN SURPRISE ON REPETITION ===")
    print("(Anaphoric candidates: high-S₂ rise on 2nd occurrence)")
    # Focus on words where 1st occurrence is BELOW average but 2nd is HIGH
    interesting = [(w, t, a, s1, s2, d) for w, t, a, s1, s2, d in two_occurrence_deltas
                   if d > 3.0 and s1 < 2.0]
    interesting.sort(key=lambda x: x[5], reverse=True)
    for word, title, author, s1, s2, delta in interesting[:10]:
        print(f"  '{word}' in '{title}' ({author}): S₂ = {s1:.1f} → {s2:.1f} (+{delta:.1f})")

    print("\n=== EXAMPLES: ANAPHORA — SAME WORD 3+ TIMES ===")
    # Find words repeated 3+ times with a clear pattern
    anaphora_candidates = []
    for word, title, author, traj in multi_trajectories:
        if len(traj) >= 3:
            anaphora_candidates.append((word, title, author, traj, traj[0], max(traj)))
    anaphora_candidates.sort(key=lambda x: x[5], reverse=True)
    print(f"{'Word':<20} {'Poem':<35} {'S₂ trajectory'}")
    for word, title, author, traj, first, mx in anaphora_candidates[:10]:
        traj_str = " → ".join(f"{v:.1f}" for v in traj)
        print(f"{word!r:<20} {title[:33]:<35} {traj_str}")

    # Return data for findings file
    return {
        "occurrence_s2": {str(k): {"n": len(v), "mean": statistics.mean(v) if v else 0}
                          for k, v in occurrence_s2.items() if v},
        "two_occ_n": len(two_occurrence_deltas),
        "two_occ_mean_delta": statistics.mean([d[5] for d in two_occurrence_deltas]) if two_occurrence_deltas else 0,
        "pct_drops": 100 * len([d for d in two_occurrence_deltas if d[5] < 0]) / len(two_occurrence_deltas) if two_occurrence_deltas else 0,
        "top_risers": [(w, t, s1, s2, d) for w, t, a, s1, s2, d in risers_sorted[:5]],
        "era_data": era_data,
        "multi_traj_means": {str(k): statistics.mean(v) for k, v in traj_by_length.items() if len(v) >= 5},
    }


if __name__ == "__main__":
    results = run_experiment()
