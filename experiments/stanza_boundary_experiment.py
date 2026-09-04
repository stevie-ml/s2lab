"""
Stanza Boundary Analysis: Does the Stanza Break Amplify the Line-Break Effect?

Research question:
  The line-position experiment showed that line-initial tokens have dramatically
  higher S2 (+5.57) than medial (-0.24) or final (-0.49) tokens. But a stanza
  break is a stronger boundary than a line break — it introduces silence, white
  space, and a structural reset. Do stanza-initial tokens show even higher S2?

Hypotheses:
  H1 (Stanza Amplification): Stanza-initial tokens have higher S2 than regular
      line-initial tokens. The longer the pause, the more freedom the poet has.
  H2 (Stanza Closure): The final line of a stanza has lower S2 than non-final lines
      (poets land softly before the break, like a musical cadence).
  H3 (Stanza Arc): S2 is high at stanza opening, falls through the middle, and
      reaches its lowest just before the stanza break.
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


def analyze_with_stanza_positions(text, model, tokenizer):
    """
    Analyze a poem and tag each token with its position relative to stanzas and lines.

    Stanza structure:
      - Stanzas are separated by blank lines ('\n\n' or more)
      - Each stanza has lines; each line has tokens

    Position tags:
      'stanza_initial'  — first non-empty token of the first line of any stanza (except the first)
      'stanza_final'    — last non-empty token of the last line of a stanza (except last)
      'line_initial'    — first token of any other line
      'line_final'      — last token of any other line
      'medial'          — everything else
    """
    # Split into stanzas: consecutive non-empty lines form a stanza
    raw_lines = text.split("\n")

    stanzas = []
    current_stanza = []
    for line in raw_lines:
        if line.strip() == "":
            if current_stanza:
                stanzas.append(current_stanza)
                current_stanza = []
        else:
            current_stanza.append(line)
    if current_stanza:
        stanzas.append(current_stanza)

    if len(stanzas) < 2:
        return None, 0  # Need at least 2 stanzas

    # Rebuild text (preserve original spacing)
    # Build a line-level map: (stanza_idx, line_idx_in_stanza, is_first_in_stanza, is_last_in_stanza, is_only_stanza)
    line_info = {}  # line_number_in_full_poem -> (stanza_idx, line_in_stanza, stanza_len)
    line_num = 0
    for si, stanza in enumerate(stanzas):
        for li, line in enumerate(stanza):
            line_info[line_num] = {
                "stanza_idx": si,
                "line_in_stanza": li,
                "stanza_len": len(stanza),
                "n_stanzas": len(stanzas),
            }
            line_num += 1
        # blank lines between stanzas
        if si < len(stanzas) - 1:
            line_num += 1

    # Tokenize the full text
    input_ids = tokenizer.encode(text, return_tensors="pt")
    tokens = [tokenizer.decode([t]) for t in input_ids[0]]

    with torch.no_grad():
        outputs = model(input_ids)
        logits = outputs.logits

    # Build character offsets for each token
    char_offsets = []
    offset = 0
    for t in tokens:
        char_offsets.append(offset)
        offset += len(t)

    # Build char -> (line_in_poem, is_blank) map
    char_to_line = {}
    char_pos = 0
    poem_line_num = 0
    for raw_line in raw_lines:
        for ch_i in range(len(raw_line)):
            char_to_line[char_pos + ch_i] = poem_line_num
        char_to_line[char_pos + len(raw_line)] = poem_line_num  # the \n itself
        char_pos += len(raw_line) + 1
        poem_line_num += 1

    # Determine line-position for every token
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

        tok_char = char_offsets[i + 1] if (i + 1) < len(char_offsets) else -1
        tok_line = char_to_line.get(tok_char, -1)

        info = line_info.get(tok_line)

        # Compute line-level position: initial / final / medial on this poem line
        tok_is_final = False
        tok_is_initial = False
        if tok_line >= 0:
            same_line_tokens = [
                j for j in range(1, len(tokens))
                if char_to_line.get(char_offsets[j] if j < len(char_offsets) else -1, -1) == tok_line
                and tokens[j].strip()
            ]
            if same_line_tokens:
                if (i + 1) == same_line_tokens[-1]:
                    tok_is_final = True
                if (i + 1) == same_line_tokens[0]:
                    tok_is_initial = True

        # Assign position label
        position = "medial"
        if info is not None and tok_is_initial:
            si = info["stanza_idx"]
            li = info["line_in_stanza"]
            sl = info["stanza_len"]
            ns = info["n_stanzas"]
            if li == 0 and si > 0:
                position = "stanza_initial"  # first line of any stanza except the first
            elif li == sl - 1 and si < ns - 1:
                position = "stanza_final_line_initial"
            else:
                position = "line_initial"
        elif info is not None and tok_is_final:
            si = info["stanza_idx"]
            li = info["line_in_stanza"]
            sl = info["stanza_len"]
            ns = info["n_stanzas"]
            if li == sl - 1 and si < ns - 1:
                position = "stanza_final_line_final"
            elif li == 0 and si > 0:
                position = "stanza_initial_line_final"
            else:
                position = "line_final"

        token_data.append({
            "position": i + 1,
            "token": actual_token,
            "surprisal": round(surprisal, 4),
            "entropy": round(entropy, 4),
            "s2": round(s2, 4),
            "line_pos": position,
            "line_num": tok_line,
            "info": info,
        })

    return token_data, len(stanzas)


def run_experiment():
    print("Loading GPT-2 model...")
    model, tokenizer = get_model()
    print("Model loaded.\n")

    all_by_pos = defaultdict(list)
    poem_results = []
    n_poems = 0

    print("Analyzing poems with stanza structure...")
    for poem in POEMS:
        if poem.get("language", "en") != "en":
            continue
        if poem["era"] == "control":
            continue
        if "\n\n" not in poem["text"]:
            continue

        try:
            token_data, n_stanzas = analyze_with_stanza_positions(poem["text"], model, tokenizer)
            if token_data is None:
                continue

            n_poems += 1
            for td in token_data:
                all_by_pos[td["line_pos"]].append(td["s2"])

            # Poem-level summaries by position
            pos_avgs = {}
            for pos in ["stanza_initial", "stanza_final_line_initial", "stanza_final_line_final",
                        "stanza_initial_line_final", "line_initial", "line_final", "medial"]:
                vals = [td["s2"] for td in token_data if td["line_pos"] == pos]
                if vals:
                    pos_avgs[pos] = sum(vals) / len(vals)

            # Get exemplar: highest S2 stanza_initial token
            si_tokens = [td for td in token_data if td["line_pos"] == "stanza_initial"]
            best = max(si_tokens, key=lambda t: t["s2"]) if si_tokens else None

            poem_results.append({
                "title": poem["title"],
                "author": poem.get("author", ""),
                "era": poem.get("era", ""),
                "n_stanzas": n_stanzas,
                "pos_avgs": pos_avgs,
                "best_si": best,
            })
            print(f"  OK: {poem['author']} — {poem['title']} ({n_stanzas} stanzas)")

        except Exception as e:
            print(f"  ERR: {poem['title']}: {e}")

    print(f"\nAnalyzed {n_poems} poems with stanzas.\n")

    # ── Global statistics ─────────────────────────────────────────────────────
    def stats(lst):
        if not lst:
            return {"n": 0, "avg": None}
        n = len(lst)
        avg = sum(lst) / n
        std = (sum((x - avg) ** 2 for x in lst) / n) ** 0.5
        pos_ratio = sum(1 for x in lst if x > 0) / n
        return {"n": n, "avg": round(avg, 2), "std": round(std, 2), "pos_ratio": round(pos_ratio, 3)}

    positions_ordered = [
        ("stanza_initial", "First token, first line of stanza (stanza break before)"),
        ("stanza_initial_line_final", "Last token, first line of stanza"),
        ("line_initial", "First token, mid-stanza line"),
        ("line_final", "Last token, mid-stanza line"),
        ("stanza_final_line_initial", "First token, last line of stanza (before break)"),
        ("stanza_final_line_final", "Last token, last line of stanza"),
        ("medial", "Medial position (not initial or final)"),
    ]

    print("=" * 70)
    print("STANZA BOUNDARY ANALYSIS — GLOBAL RESULTS")
    print("=" * 70)
    print(f"\n{'Position':<40} {'N':>6} {'Avg S2':>8} {'Std':>6} {'+S2%':>6}")
    print("-" * 70)
    global_stats = {}
    for pos_key, label in positions_ordered:
        s = stats(all_by_pos[pos_key])
        global_stats[pos_key] = s
        if s["n"] > 0:
            print(f"{label:<40} {s['n']:>6} {s['avg']:>8.2f} {s['std']:>6.2f} {s['pos_ratio']:>6.1%}")
        else:
            print(f"{label:<40} {'0':>6}")

    print("\n")
    print("=" * 70)
    print("POEM-LEVEL RESULTS: Stanza-initial vs Line-initial S2")
    print("=" * 70)
    print(f"\n{'Title':<35} {'Author':<20} {'Stanzas'} {'SI avg':>8} {'LI avg':>8} {'Δ':>8}")
    print("-" * 90)
    poem_results.sort(key=lambda x: x["pos_avgs"].get("stanza_initial", 0), reverse=True)
    for pr in poem_results:
        si = pr["pos_avgs"].get("stanza_initial", None)
        li = pr["pos_avgs"].get("line_initial", None)
        if si is None:
            continue
        delta = (si - li) if li is not None else float("nan")
        si_str = f"{si:.2f}" if si is not None else " —"
        li_str = f"{li:.2f}" if li is not None else " —"
        d_str = f"{delta:+.2f}" if li is not None else " —"
        print(f"{pr['title'][:35]:<35} {pr['author'][:20]:<20} {pr['n_stanzas']:>7} {si_str:>8} {li_str:>8} {d_str:>8}")

    print("\n")
    print("=" * 70)
    print("TOP STANZA-INITIAL MOMENTS (highest S2 at stanza openings)")
    print("=" * 70)
    all_si = []
    for pr in poem_results:
        if pr.get("best_si"):
            best = pr["best_si"]
            all_si.append((best["s2"], best["token"], pr["title"], pr["author"]))
    all_si.sort(reverse=True)
    for s2, tok, title, author in all_si[:15]:
        print(f"  S2={s2:+.2f} | token={repr(tok):<20} | {author} — {title}")

    # Save results
    out = {
        "global_stats": {k: v for k, v in global_stats.items()},
        "poem_results": poem_results,
        "n_poems_analyzed": n_poems,
    }
    out_path = os.path.join(RESULTS_DIR, "stanza_boundary_results.json")
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nResults saved to {out_path}")

    return out


if __name__ == "__main__":
    run_experiment()
