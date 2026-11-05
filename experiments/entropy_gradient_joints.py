"""
Entropy Gradient Joints: Token-Level Entropy Transitions as Poetic Structure

Each token changes GPT-2's entropy for the NEXT position.
delta_H = H(t+1) - H(t): did this token OPEN or CLOSE semantic possibilities?

Large positive delta_H: "opener" token — expands what could come next
Large negative delta_H: "closer" token — constrains what must come next

Questions:
1. What is the statistical profile of delta_H across the corpus?
2. Do "opener" tokens (large +delta_H) tend to precede high-S2 events?
3. Do different genres have different opener/closer ratios?
4. What grammatical categories produce the largest entropy jumps?
5. Is there a "structural rhythm" of open-close cycles within poems?
"""

import json
import math
import statistics
from collections import defaultdict

def load_corpus():
    with open("results/corpus_results.json") as f:
        return json.load(f)

def get_clean_tokens(poem):
    """Filter out stanza-break artifacts."""
    return [t for t in poem["tokens"] if t.get("p_newline", 0) < 0.9]

def compute_entropy_gradients(tokens):
    """Compute delta_H between consecutive tokens."""
    gradients = []
    for i in range(len(tokens) - 1):
        h_curr = tokens[i]["entropy"]
        h_next = tokens[i + 1]["entropy"]
        delta = h_next - h_curr
        gradients.append({
            "position": tokens[i]["position"],
            "token": tokens[i]["token"],
            "s2_curr": tokens[i]["s2"],
            "s2_next": tokens[i + 1]["s2"],
            "h_curr": h_curr,
            "h_next": h_next,
            "delta_H": delta,
        })
    return gradients

def classify_token_role(token_text):
    """Rough classification of token type."""
    t = token_text.strip().lower()
    function_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "of",
                      "for", "with", "by", "from", "as", "is", "are", "was", "were",
                      "be", "been", "being", "have", "has", "had", "do", "does", "did",
                      "will", "would", "could", "should", "may", "might", "must", "shall",
                      "i", "you", "he", "she", "it", "we", "they", "me", "him", "her",
                      "us", "them", "my", "your", "his", "its", "our", "their",
                      "this", "that", "these", "those", "not", "no", "nor", "so",
                      "yet", "if", "then", "than", "when", "where", "while", "that",
                      "which", "who", "what", "how"}
    punct = set(".,;:!?-—()[]{}\"'`")

    if not t:
        return "EMPTY"
    if all(c in punct for c in t):
        return "PUNCT"
    if t in function_words:
        return "FUNCTION"
    if t[0].isupper() and len(t) > 1:
        return "PROPER_OR_LINE_START"
    return "CONTENT"

def main():
    corpus = load_corpus()
    results = {
        "global_stats": {},
        "opener_closer_ratio_by_era": {},
        "entropy_jump_predicts_s2": {},
        "top_opener_tokens": {},
        "top_closer_tokens": {},
        "open_close_cycle_length": {},
        "pre_spike_entropy_gradient": {},
        "token_role_gradient": {},
    }

    all_deltas = []
    era_data = defaultdict(lambda: {"openers": 0, "closers": 0, "flat": 0, "delta_sum": 0.0, "n": 0})
    jump_buckets = defaultdict(list)  # delta_H range -> list of s2_next values
    token_gradients = defaultdict(list)  # token_text -> list of delta_H
    role_gradients = defaultdict(list)

    # For pre-spike analysis: tokens immediately before high-S2 events
    pre_spike_deltas = []
    non_spike_deltas = []

    # For cycle analysis: within each poem, track alternation of opener/closer
    cycle_lengths = []

    OPENER_THRESHOLD = 1.0   # entropy units
    CLOSER_THRESHOLD = -1.0

    for poem in corpus:
        era = poem["metadata"].get("era", "unknown")
        tokens = get_clean_tokens(poem)
        if len(tokens) < 10:
            continue

        grads = compute_entropy_gradients(tokens)

        # Track open/close run lengths within this poem
        current_run = None
        run_len = 0
        poem_runs = []

        for g in grads:
            d = g["delta_H"]
            all_deltas.append(d)
            era_data[era]["n"] += 1
            era_data[era]["delta_sum"] += d

            # Classify
            if d >= OPENER_THRESHOLD:
                era_data[era]["openers"] += 1
                role = "opener"
            elif d <= CLOSER_THRESHOLD:
                era_data[era]["closers"] += 1
                role = "closer"
            else:
                era_data[era]["flat"] += 1
                role = "flat"

            # Token-level gradient mapping
            tok = g["token"].strip().lower()
            if tok:
                token_gradients[tok].append(d)
                role_gradients[classify_token_role(g["token"])].append(d)

            # Bucket by delta_H to predict s2_next
            if d >= 2.0:
                jump_buckets["large_open (+2+)"].append(g["s2_next"])
            elif d >= 1.0:
                jump_buckets["open (+1 to +2)"].append(g["s2_next"])
            elif d >= 0.0:
                jump_buckets["slight_open (0 to +1)"].append(g["s2_next"])
            elif d >= -1.0:
                jump_buckets["slight_close (-1 to 0)"].append(g["s2_next"])
            elif d >= -2.0:
                jump_buckets["close (-2 to -1)"].append(g["s2_next"])
            else:
                jump_buckets["large_close (-2-)"].append(g["s2_next"])

            # Pre-spike analysis: collect delta_H for the token BEFORE high-S2 events
            if g["s2_next"] >= 3.0:
                pre_spike_deltas.append(d)
            else:
                non_spike_deltas.append(d)

            # Cycle tracking
            if role != "flat":
                if role != current_run:
                    if current_run is not None and run_len > 0:
                        poem_runs.append(run_len)
                    current_run = role
                    run_len = 1
                else:
                    run_len += 1

        if poem_runs:
            cycle_lengths.extend(poem_runs)

    # Compute global stats
    results["global_stats"] = {
        "n_transitions": len(all_deltas),
        "mean_delta_H": statistics.mean(all_deltas),
        "median_delta_H": statistics.median(all_deltas),
        "stdev_delta_H": statistics.stdev(all_deltas),
        "pct_openers": 100 * sum(1 for d in all_deltas if d >= OPENER_THRESHOLD) / len(all_deltas),
        "pct_closers": 100 * sum(1 for d in all_deltas if d <= CLOSER_THRESHOLD) / len(all_deltas),
        "pct_flat": 100 * sum(1 for d in all_deltas if CLOSER_THRESHOLD < d < OPENER_THRESHOLD) / len(all_deltas),
    }

    # Era-level opener/closer ratios (require at least 50 transitions)
    era_summary = {}
    for era, ed in sorted(era_data.items(), key=lambda x: -x[1]["n"]):
        n = ed["n"]
        if n < 50:
            continue
        total_non_flat = ed["openers"] + ed["closers"]
        if total_non_flat == 0:
            oc_ratio = None
        else:
            oc_ratio = ed["openers"] / total_non_flat
        era_summary[era] = {
            "n": n,
            "pct_opener": 100 * ed["openers"] / n,
            "pct_closer": 100 * ed["closers"] / n,
            "mean_delta_H": ed["delta_sum"] / n,
            "opener_closer_ratio": oc_ratio,
        }
    results["opener_closer_ratio_by_era"] = era_summary

    # Entropy jump predicts S2 of next token
    jump_summary = {}
    for bucket, s2_list in sorted(jump_buckets.items()):
        if len(s2_list) < 20:
            continue
        jump_summary[bucket] = {
            "n": len(s2_list),
            "mean_s2_next": statistics.mean(s2_list),
            "pct_high_s2_next": 100 * sum(1 for s in s2_list if s >= 3.0) / len(s2_list),
        }
    results["entropy_jump_predicts_s2"] = jump_summary

    # Pre-spike vs non-spike delta_H comparison
    if pre_spike_deltas and non_spike_deltas:
        results["pre_spike_entropy_gradient"] = {
            "n_pre_spike": len(pre_spike_deltas),
            "n_non_spike": len(non_spike_deltas),
            "mean_delta_H_pre_spike": statistics.mean(pre_spike_deltas),
            "mean_delta_H_non_spike": statistics.mean(non_spike_deltas),
            "pct_opener_pre_spike": 100 * sum(1 for d in pre_spike_deltas if d >= OPENER_THRESHOLD) / len(pre_spike_deltas),
            "pct_opener_non_spike": 100 * sum(1 for d in non_spike_deltas if d >= OPENER_THRESHOLD) / len(non_spike_deltas),
            "pct_closer_pre_spike": 100 * sum(1 for d in pre_spike_deltas if d <= CLOSER_THRESHOLD) / len(pre_spike_deltas),
            "pct_closer_non_spike": 100 * sum(1 for d in non_spike_deltas if d <= CLOSER_THRESHOLD) / len(non_spike_deltas),
        }

    # Top opener and closer tokens (require >= 10 occurrences, exclude very common short tokens)
    MIN_OCC = 10
    min_len = 3
    top_openers = []
    top_closers = []
    for tok, dlist in token_gradients.items():
        if len(dlist) < MIN_OCC or len(tok) < min_len:
            continue
        mean_d = statistics.mean(dlist)
        if mean_d >= 0.5:
            top_openers.append((tok, mean_d, len(dlist)))
        elif mean_d <= -0.5:
            top_closers.append((tok, mean_d, len(dlist)))
    top_openers.sort(key=lambda x: -x[1])
    top_closers.sort(key=lambda x: x[1])
    results["top_opener_tokens"] = [
        {"token": t, "mean_delta_H": d, "n": n} for t, d, n in top_openers[:25]
    ]
    results["top_closer_tokens"] = [
        {"token": t, "mean_delta_H": d, "n": n} for t, d, n in top_closers[:25]
    ]

    # Token role gradient
    for role, dlist in role_gradients.items():
        if dlist:
            results["token_role_gradient"][role] = {
                "n": len(dlist),
                "mean_delta_H": statistics.mean(dlist),
                "pct_opener": 100 * sum(1 for d in dlist if d >= OPENER_THRESHOLD) / len(dlist),
                "pct_closer": 100 * sum(1 for d in dlist if d <= CLOSER_THRESHOLD) / len(dlist),
            }

    # Open/close cycle statistics
    if cycle_lengths:
        results["open_close_cycle_length"] = {
            "n_runs": len(cycle_lengths),
            "mean_run_length": statistics.mean(cycle_lengths),
            "median_run_length": statistics.median(cycle_lengths),
            "pct_runs_1": 100 * sum(1 for x in cycle_lengths if x == 1) / len(cycle_lengths),
            "pct_runs_2_3": 100 * sum(1 for x in cycle_lengths if 2 <= x <= 3) / len(cycle_lengths),
            "pct_runs_4plus": 100 * sum(1 for x in cycle_lengths if x >= 4) / len(cycle_lengths),
        }

    # Save results
    with open("results/entropy_gradient_joints.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Saved results/entropy_gradient_joints.json")
    return results

if __name__ == "__main__":
    r = main()
    # Print key results
    gs = r["global_stats"]
    print(f"\nGlobal: mean delta_H={gs['mean_delta_H']:.3f}, "
          f"openers={gs['pct_openers']:.1f}%, closers={gs['pct_closers']:.1f}%, "
          f"flat={gs['pct_flat']:.1f}%")
    print("\nEntropy jump -> S2 of next token:")
    for bucket, stats in r["entropy_jump_predicts_s2"].items():
        print(f"  {bucket:30s}: mean_s2_next={stats['mean_s2_next']:.3f}, "
              f"high_s2_pct={stats['pct_high_s2_next']:.1f}% (n={stats['n']})")
    if r["pre_spike_entropy_gradient"]:
        ps = r["pre_spike_entropy_gradient"]
        print(f"\nPre-spike delta_H: {ps['mean_delta_H_pre_spike']:.3f} "
              f"vs non-spike: {ps['mean_delta_H_non_spike']:.3f}")
        print(f"  opener% pre-spike: {ps['pct_opener_pre_spike']:.1f}% "
              f"vs non-spike: {ps['pct_opener_non_spike']:.1f}%")
