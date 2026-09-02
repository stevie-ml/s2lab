"""
Line-Position Analysis: Do poets systematically place high-S2 tokens at line endings?

Research question: In poetry, the line break is a fundamental formal unit.
Does the position of a token within a line (beginning / middle / end) predict its S2 value?

Hypotheses:
  H1: Line-final tokens have LOWER S2 (rhyme and meter constrain end-words, making
      them more predictable — the "rhyme penalty").
  H2: Line-initial tokens have HIGHER S2 (the fresh start of a line allows more
      deviation from grammatical expectation — especially in enjambment).
  H3: Line-final tokens in rhymed poetry differ from those in free verse (rhyme
      imposes a constraint on the "pool" of possible words, affecting entropy vs surprisal).
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
    tokenizer = AutoTokenizer.from_pretrained("gpt2")
    model = AutoModelForCausalLM.from_pretrained("gpt2")
    model.eval()
    return model, tokenizer


def analyze_with_line_positions(text, model, tokenizer, top_k=5):
    """
    Analyze a poem and tag each token with its line position.
    Returns list of token dicts with added 'line_pos' field:
      'initial'  — first token of a line
      'final'    — last token of a line
      'medial'   — everything else
    Also tracks line number and which tokens are line-final whitespace.
    """
    # Split text into lines to track structure
    lines = text.split("\n")

    # Tokenize the full text to get consistent IDs
    input_ids = tokenizer.encode(text, return_tensors="pt")
    tokens = [tokenizer.decode([t]) for t in input_ids[0]]

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits

    # Build a mapping: for each raw token index (1..N), determine line position
    # Strategy: reconstruct character offsets and match to line boundaries
    char_offsets = []
    offset = 0
    for t in tokens:
        char_offsets.append(offset)
        offset += len(t)

    # Find char positions of line boundaries (newline characters)
    newline_positions = set()
    line_start_positions = {0}  # first line starts at char 0
    char_offset = 0
    for line in lines:
        char_offset += len(line)
        if char_offset < len(text):
            newline_positions.add(char_offset)
            line_start_positions.add(char_offset + 1)
        char_offset += 1  # for the \n itself

    # For each token, determine if it contains a newline, starts a line, or ends a line
    # We'll do this by checking which line each token's character position belongs to
    char_to_line = {}
    char_pos = 0
    for line_num, line in enumerate(lines):
        for ch in range(len(line)):
            char_to_line[char_pos + ch] = line_num
        # The newline char itself — assign to the line it ends
        char_to_line[char_pos + len(line)] = line_num
        char_pos += len(line) + 1  # +1 for \n

    token_data = []

    for i in range(len(tokens) - 1):
        token_logits = logits[0, i, :]
        probs = F.softmax(token_logits, dim=-1)
        log_probs = F.log_softmax(token_logits, dim=-1)

        actual_id = input_ids[0, i + 1].item()
        actual_token = tokens[i + 1]

        surprisal = -log_probs[actual_id].item() / math.log(2)
        entropy = -(probs * log_probs).sum().item() / math.log(2)
        s2 = surprisal - entropy

        # Top-k alternatives
        topk_probs, topk_ids = torch.topk(probs, top_k)
        alternatives = [tokenizer.decode([tid.item()]) for tid in topk_ids]

        # Determine line position for the ACTUAL token (i+1)
        tok_char_offset = char_offsets[i + 1] if (i + 1) < len(char_offsets) else -1
        tok_line = char_to_line.get(tok_char_offset, -1)

        # Is this token the last non-whitespace on its line?
        # Find all tokens on the same line
        tok_is_final = False
        tok_is_initial = False
        if tok_line >= 0:
            # Tokens on same line
            same_line_token_indices = [
                j for j in range(1, len(tokens))
                if char_to_line.get(char_offsets[j] if j < len(char_offsets) else -1, -1) == tok_line
                and tokens[j].strip()  # ignore pure-whitespace tokens
            ]
            if same_line_token_indices:
                if (i + 1) == same_line_token_indices[-1]:
                    tok_is_final = True
                if (i + 1) == same_line_token_indices[0]:
                    tok_is_initial = True

        if tok_is_final:
            line_pos = "final"
        elif tok_is_initial:
            line_pos = "initial"
        else:
            line_pos = "medial"

        token_data.append({
            "position": i + 1,
            "token": actual_token,
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "line_pos": line_pos,
            "line_num": tok_line,
            "alternatives": alternatives,
        })

    return token_data


def run_experiment():
    print("Loading GPT-2 model...")
    model, tokenizer = get_model()
    print("Model loaded.\n")

    # Filter to English poems only (exclude control prose for now)
    # We want to compare poetry with distinct lines
    poetry_eras = [
        "romantic", "19th_century", "modernist", "confessional",
        "beat", "new_york_school", "language", "contemporary",
        "victorian", "harlem_renaissance", "deep_image", "mid_century",
        "surrealist", "imagist", "haiku", "oulipo"
    ]

    all_results = defaultdict(list)  # line_pos -> list of s2 values
    poem_results = []

    print("Analyzing poems for line-position effects...")
    analyzed = 0
    for poem in POEMS:
        if poem.get("language", "en") != "en":
            continue
        if poem["era"] == "control":
            continue
        if "\n" not in poem["text"]:
            continue

        try:
            token_data = analyze_with_line_positions(poem["text"], model, tokenizer)

            # Aggregate by line position
            pos_stats = defaultdict(list)
            for tok in token_data:
                if tok["token"].strip():  # skip pure whitespace
                    pos_stats[tok["line_pos"]].append(tok["s2"])

            poem_stats = {
                "title": poem["title"],
                "author": poem["author"],
                "era": poem["era"],
                "year": poem.get("year"),
            }
            for pos in ["initial", "medial", "final"]:
                vals = pos_stats.get(pos, [])
                if vals:
                    poem_stats[f"{pos}_avg_s2"] = round(sum(vals) / len(vals), 4)
                    poem_stats[f"{pos}_n"] = len(vals)
                    all_results[pos].extend(vals)
                else:
                    poem_stats[f"{pos}_avg_s2"] = None
                    poem_stats[f"{pos}_n"] = 0

            poem_results.append(poem_stats)
            analyzed += 1
            if analyzed % 10 == 0:
                print(f"  Analyzed {analyzed} poems...")

        except Exception as e:
            print(f"  Skipping {poem['title']}: {e}")
            continue

    print(f"\nAnalyzed {analyzed} poems total.\n")

    # Aggregate stats across all poems
    print("=" * 70)
    print("LINE-POSITION ANALYSIS: S₂ BY POSITION IN LINE")
    print("=" * 70)
    print()

    global_stats = {}
    for pos in ["initial", "medial", "final"]:
        vals = all_results[pos]
        if vals:
            avg = sum(vals) / len(vals)
            var = sum((v - avg) ** 2 for v in vals) / len(vals)
            std = var ** 0.5
            pos_ratio = sum(1 for v in vals if v > 0) / len(vals)
            global_stats[pos] = {
                "avg_s2": round(avg, 4),
                "std_s2": round(std, 4),
                "n": len(vals),
                "pos_ratio": round(pos_ratio, 4),
            }

    print(f"{'Position':<12} {'N tokens':>10} {'Avg S₂':>10} {'Std S₂':>10} {'+S₂ ratio':>12}")
    print("-" * 56)
    for pos in ["initial", "medial", "final"]:
        s = global_stats.get(pos, {})
        print(f"{pos:<12} {s.get('n', 0):>10} {s.get('avg_s2', 'N/A'):>10} "
              f"{s.get('std_s2', 'N/A'):>10} {s.get('pos_ratio', 'N/A'):>12.3f}")

    # Per-poem: which poems show strongest final-position elevation or depression?
    print()
    print("TOP POEMS: Final-position S₂ ELEVATION above medial baseline")
    print("-" * 70)
    poems_with_gap = [
        (p, p.get("final_avg_s2", 0) - p.get("medial_avg_s2", 0))
        for p in poem_results
        if p.get("final_avg_s2") is not None and p.get("medial_avg_s2") is not None
    ]
    poems_with_gap.sort(key=lambda x: x[1], reverse=True)

    print(f"{'Title':<45} {'Author':<20} {'Final-Med Δ':>12}")
    print("-" * 80)
    for p, gap in poems_with_gap[:10]:
        print(f"{p['title'][:44]:<45} {p['author'][:19]:<20} {gap:>12.4f}")

    print()
    print("TOP POEMS: Final-position S₂ DEPRESSION below medial baseline")
    print("-" * 70)
    for p, gap in reversed(poems_with_gap[-10:]):
        print(f"{p['title'][:44]:<45} {p['author'][:19]:<20} {gap:>12.4f}")

    # Per-era analysis
    print()
    print("LINE-POSITION EFFECTS BY ERA")
    print("-" * 70)
    era_data = defaultdict(lambda: defaultdict(list))
    for p in poem_results:
        for pos in ["initial", "medial", "final"]:
            val = p.get(f"{pos}_avg_s2")
            if val is not None:
                era_data[p["era"]][pos].append(val)

    print(f"{'Era':<22} {'n poems':>8} {'Initial S₂':>12} {'Medial S₂':>12} {'Final S₂':>12} {'Δ(F-M)':>10}")
    print("-" * 80)
    era_rows = []
    for era, pos_data in era_data.items():
        n_poems = len(pos_data.get("initial", pos_data.get("medial", pos_data.get("final", []))))
        init_avg = sum(pos_data["initial"]) / len(pos_data["initial"]) if pos_data["initial"] else None
        med_avg = sum(pos_data["medial"]) / len(pos_data["medial"]) if pos_data["medial"] else None
        fin_avg = sum(pos_data["final"]) / len(pos_data["final"]) if pos_data["final"] else None
        delta = round(fin_avg - med_avg, 4) if fin_avg is not None and med_avg is not None else None
        era_rows.append((era, n_poems, init_avg, med_avg, fin_avg, delta))

    era_rows.sort(key=lambda x: (x[5] or 0), reverse=True)
    for era, n, init, med, fin, delta in era_rows:
        init_s = f"{init:.3f}" if init is not None else "N/A"
        med_s = f"{med:.3f}" if med is not None else "N/A"
        fin_s = f"{fin:.3f}" if fin is not None else "N/A"
        delta_s = f"{delta:+.3f}" if delta is not None else "N/A"
        print(f"{era:<22} {n:>8} {init_s:>12} {med_s:>12} {fin_s:>12} {delta_s:>10}")

    # Save results
    results = {
        "experiment": "line_position_analysis",
        "date": "2026-09-02",
        "global_stats": global_stats,
        "poem_results": poem_results,
        "n_poems_analyzed": analyzed,
    }
    out_path = os.path.join(RESULTS_DIR, "line_position_results.json")
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return results


if __name__ == "__main__":
    run_experiment()
