"""
Volta Experiment: Does S₂ spike at the structural turn in sonnets?

The volta (Italian: "turn") is the rhetorical pivot that defines sonnet structure.
In Petrarchan sonnets, it falls between the octave (lines 1-8) and sestet (lines 9-14).
In Shakespearean sonnets, the primary turn is at the final couplet (lines 13-14),
though a secondary shift often precedes it.

If the information-theoretic framework captures genuine poetic structure,
we expect S₂ to be elevated at the volta:
  - The model, conditioned on the octave's argument, predicts continuation.
  - The poet pivots, introducing new material the model did not expect.
  - This mismatch should register as high S₂.

Hypotheses:
  H1: Line 9 mean S₂ > octave mean S₂ in Petrarchan sonnets.
  H2: Lines 13-14 mean S₂ > quatrain mean S₂ in Shakespearean sonnets.
  H3: Irregular/hybrid sonnets (Ozymandias) show volta-like spikes but
      not aligned with the canonical line positions.
"""

import sys
import os
import json
import math
import torch
import torch.nn.functional as F
from transformers import AutoModelForCausalLM, AutoTokenizer
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from corpus.poems import POEMS

RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "results")


def get_model():
    print("Loading GPT-2...")
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    return model, tokenizer


def analyze_poem_by_line(text, model, tokenizer):
    """
    Compute S₂ for each token and track which line each token belongs to.

    Returns a list of (line_number, token_str, s2) tuples.
    Line numbers are 1-indexed.
    """
    lines = text.strip().split("\n")
    # Build per-line character spans in the full text
    char_to_line = {}
    pos = 0
    for line_num, line in enumerate(lines, start=1):
        for _ in line:
            char_to_line[pos] = line_num
            pos += 1
        # newline character — assign to the line just finished
        char_to_line[pos] = line_num
        pos += 1

    input_ids = tokenizer.encode(text, return_tensors="pt")

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits  # (1, seq_len, vocab_size)

    probs_all = torch.softmax(logits[0], dim=-1)  # (seq_len, vocab_size)

    results = []
    char_cursor = 0

    for i in range(1, input_ids.shape[1]):
        token_id = input_ids[0, i].item()
        token_str = tokenizer.decode([token_id])

        # Surprisal of the chosen token
        p_chosen = probs_all[i - 1, token_id].item()
        surprisal = -math.log2(p_chosen + 1e-10)

        # Shannon entropy of the predictive distribution at position i-1
        p_dist = probs_all[i - 1]
        entropy = -torch.sum(p_dist * torch.log2(p_dist + 1e-10)).item()

        s2 = surprisal - entropy

        # Map token's character position to a line number
        # Use the char position of the first character of this token
        # (approximated by advancing a cursor through the decoded tokens)
        line_num = char_to_line.get(char_cursor, None)
        if line_num is None:
            # Clamp to last line
            line_num = len(lines)

        results.append({
            "line": line_num,
            "token": token_str,
            "s2": s2,
            "surprisal": surprisal,
            "entropy": entropy,
        })

        # Advance cursor by length of this token in the original text
        char_cursor += len(token_str)

    return results, lines


def per_line_s2(token_results):
    """Return dict: line_num -> list of s2 values."""
    by_line = defaultdict(list)
    for t in token_results:
        if t["line"] is not None:
            by_line[t["line"]].append(t["s2"])
    return by_line


def mean(vals):
    return sum(vals) / len(vals) if vals else float("nan")


def main():
    sonnets = [p for p in POEMS if "sonnet_type" in p]
    # Also include existing sonnets from the corpus (Rossetti, McKay, Cullen)
    # that are full 14-line sonnets — add them manually
    extra_sonnets = [
        p for p in POEMS
        if p["title"] in ("Remember", "If We Must Die", "Yet Do I Marvel")
    ]
    # Annotate existing sonnets with type
    type_map = {
        "Remember": "petrarchan",
        "If We Must Die": "petrarchan",
        "Yet Do I Marvel": "shakespearean",
    }
    for p in extra_sonnets:
        p = dict(p)
        p["sonnet_type"] = type_map[p["title"]]

    all_sonnets = sonnets + extra_sonnets
    print(f"\nFound {len(all_sonnets)} sonnets for analysis.\n")

    model, tokenizer = get_model()

    results = []
    for poem in all_sonnets:
        title = poem["title"]
        sonnet_type = poem.get("sonnet_type", "unknown")
        text = poem["text"]
        lines = text.strip().split("\n")
        n_lines = len(lines)

        print(f"  Analyzing: {title!r} ({sonnet_type}, {n_lines} lines) ...")

        token_data, text_lines = analyze_poem_by_line(text, model, tokenizer)
        by_line = per_line_s2(token_data)

        # Compute per-line mean S₂
        line_means = {ln: mean(vals) for ln, vals in by_line.items()}

        # Compute structural zone means
        if sonnet_type == "petrarchan":
            octave_lines = list(range(1, 9))
            sestet_lines = list(range(9, 15))
            volta_lines = [9]
            body_lines = list(range(1, 9))
        elif sonnet_type == "shakespearean":
            octave_lines = list(range(1, 13))
            sestet_lines = list(range(13, 15))
            volta_lines = [13, 14]
            body_lines = list(range(1, 13))
        else:  # irregular
            octave_lines = list(range(1, 9))
            sestet_lines = list(range(9, 15))
            volta_lines = [9, 10]
            body_lines = list(range(1, 9))

        def zone_mean(line_list):
            vals = []
            for ln in line_list:
                vals.extend(by_line.get(ln, []))
            return mean(vals)

        octave_s2 = zone_mean(octave_lines)
        sestet_s2 = zone_mean(sestet_lines)
        volta_s2 = zone_mean(volta_lines)
        body_s2 = zone_mean([l for l in body_lines if l not in volta_lines])
        overall_s2 = mean([t["s2"] for t in token_data])

        # Volta elevation: how much higher is the volta vs the rest?
        volta_lift = volta_s2 - body_s2

        results.append({
            "title": title,
            "author": poem["author"],
            "year": poem["year"],
            "sonnet_type": sonnet_type,
            "n_lines": n_lines,
            "overall_s2": round(overall_s2, 4),
            "octave_s2": round(octave_s2, 4),
            "sestet_s2": round(sestet_s2, 4),
            "volta_s2": round(volta_s2, 4),
            "body_s2": round(body_s2, 4),
            "volta_lift": round(volta_lift, 4),
            "line_means": {str(k): round(v, 4) for k, v in sorted(line_means.items())},
            "token_data": token_data,
        })

        print(f"    Overall={overall_s2:.3f}  Octave={octave_s2:.3f}  "
              f"Sestet={sestet_s2:.3f}  Volta={volta_s2:.3f}  Lift={volta_lift:+.3f}")

    return results


def print_report(results):
    print("\n" + "=" * 70)
    print("VOLTA EXPERIMENT RESULTS")
    print("=" * 70)

    petrarchan = [r for r in results if r["sonnet_type"] == "petrarchan"]
    shakespearean = [r for r in results if r["sonnet_type"] == "shakespearean"]
    irregular = [r for r in results if r["sonnet_type"] == "irregular"]

    for label, group in [("Petrarchan", petrarchan),
                          ("Shakespearean", shakespearean),
                          ("Irregular", irregular)]:
        if not group:
            continue
        print(f"\n── {label} sonnets (volta at {'line 9' if label == 'Petrarchan' else 'lines 13-14' if label == 'Shakespearean' else 'lines 9-10'}) ──")
        print(f"{'Title':<45} {'Body S₂':>8} {'Volta S₂':>9} {'Lift':>7}")
        print("-" * 72)
        lifts = []
        for r in group:
            print(f"{r['title'][:44]:<45} {r['body_s2']:>8.3f} {r['volta_s2']:>9.3f} {r['volta_lift']:>+7.3f}")
            lifts.append(r["volta_lift"])
        avg_lift = mean(lifts)
        direction = "HIGHER" if avg_lift > 0 else "lower"
        print(f"\n  Mean volta lift: {avg_lift:+.3f}  → volta S₂ is {direction} than body S₂")

    print("\n── Line-by-line S₂ profiles (selected sonnets) ──")
    for r in results[:4]:  # Show first 4 in detail
        print(f"\n  {r['title']} ({r['sonnet_type']})")
        print(f"  {'Line':<6} {'Mean S₂':>9}  {'Zone':<12}")
        for ln_str, s2 in sorted(r["line_means"].items(), key=lambda x: int(x[0])):
            ln = int(ln_str)
            n_lines = r["n_lines"]
            if r["sonnet_type"] == "petrarchan":
                zone = "VOLTA" if ln == 9 else ("octave" if ln < 9 else "sestet")
            elif r["sonnet_type"] == "shakespearean":
                zone = "VOLTA" if ln >= 13 else "quatrains"
            else:
                zone = "VOLTA" if ln in (9, 10) else ("octave" if ln < 9 else "sestet")
            marker = " ◄" if "VOLTA" in zone else ""
            print(f"  {ln:<6} {s2:>9.3f}  {zone:<12}{marker}")


if __name__ == "__main__":
    results = main()
    print_report(results)

    # Save summary (without bulky token_data)
    summary = []
    for r in results:
        s = {k: v for k, v in r.items() if k != "token_data"}
        summary.append(s)

    out_path = os.path.join(RESULTS_DIR, "volta_experiment.json")
    with open(out_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResults saved to {out_path}")
