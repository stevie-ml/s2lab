"""
Stanza Form and S₂ Budget

Do different stanza forms (couplet, tercet, quatrain, sestet, octave)
show systematically different S₂ profiles?

Hypotheses:
1. Smaller stanzas must concentrate S₂ more tightly — fewer tokens,
   higher peak-to-mean ratio.
2. Longer stanzas allow a "setup → surprise → resolution" arc within
   the stanza itself; shorter ones cannot.
3. The last-line S₂ boost (closing emphasis) is strongest in couplets,
   where the final line has maximum relative weight.

Method:
- Re-uses corpus_results.json (token-level S₂, entropy, rank)
- Segments each poem text into stanzas (blank-line-delimited groups)
- Classifies each stanza by its line count: 2 (couplet), 3 (tercet),
  4 (quatrain), 5 (cinquain), 6 (sestet), 7+ (longer/complex)
- For each stanza, computes:
    * mean_s2 (artifact-cleaned)
    * max_s2 (peak)
    * s2_range (max - mean)
    * pos_s2_ratio (% tokens with S₂ > 0)
    * peak_to_mean: max_s2 / max(mean_s2, 0.01)
    * line_1_s2: mean S₂ of first line tokens
    * last_line_s2: mean S₂ of last line tokens
    * last_line_boost: last_line_s2 - line_1_s2
- Aggregates by stanza form, then by era × stanza form
"""

import json
import statistics
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from corpus.poems import POEMS

RESULTS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "results", "corpus_results.json"
)
OUTPUT_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "findings", "stanza_form_s2_budget.json"
)

MIN_TOKENS_PER_STANZA = 8  # exclude tiny stanzas from stats
MIN_STANZAS_PER_FORM = 10  # only report forms with enough data


def is_artifact(tok):
    alts = tok.get("alternatives", [])
    if not alts:
        return False
    return alts[0]["token"] in ("\n", "\r\n", "\r") and alts[0]["prob"] >= 0.9


def clean_tokens(tokens):
    return [t for t in tokens if not is_artifact(t)]


def mean(lst):
    return statistics.mean(lst) if lst else None


def segment_poem_into_stanzas(text):
    """Split poem text into stanzas (blank-line-separated groups of non-empty lines).
    Returns list of lists of lines (each inner list is one stanza's lines).
    """
    stanzas = []
    current = []
    for line in text.split("\n"):
        stripped = line.strip()
        if stripped:
            current.append(stripped)
        else:
            if current:
                stanzas.append(current)
                current = []
    if current:
        stanzas.append(current)
    return stanzas


def classify_form(n_lines):
    if n_lines == 2:
        return "couplet (2)"
    elif n_lines == 3:
        return "tercet (3)"
    elif n_lines == 4:
        return "quatrain (4)"
    elif n_lines == 5:
        return "cinquain (5)"
    elif n_lines == 6:
        return "sestet (6)"
    elif 7 <= n_lines <= 9:
        return "octave/septet (7-9)"
    else:
        return "longer (10+)"


def map_tokens_to_stanza_lines(poem_text, token_positions):
    """
    For each token (by its 1-based position), determine which stanza/line it
    belongs to. Returns list of (stanza_idx, line_idx_within_stanza) tuples,
    parallel to token_positions.

    Uses character-level mapping: walk poem_text char by char, tracking
    stanza/line indices, then for each token's position find the stanza/line.
    """
    # Build a char_index -> (stanza_idx, line_in_stanza) map
    char_to_sl = {}
    stanza_idx = 0
    line_in_stanza = 0
    in_stanza = False
    prev_was_blank = True  # start as if we came from blank

    lines = poem_text.split("\n")
    char_pos = 0
    stanza_i = -1

    for line in lines:
        is_blank = line.strip() == ""
        if not is_blank:
            if prev_was_blank:
                stanza_i += 1
                line_in_stanza_i = 0
            else:
                line_in_stanza_i += 1  # noqa: will be re-set per stanza below
        # Mark each char in this line
        if not is_blank:
            for ci in range(len(line)):
                char_to_sl[char_pos + ci] = (stanza_i, line_in_stanza_i)
        prev_was_blank = is_blank
        char_pos += len(line) + 1  # +1 for the \n

    # Actually we need to track line_in_stanza correctly per stanza
    # Redo with cleaner logic:
    char_to_sl = {}
    stanza_line_map = []  # (stanza_idx, line_in_stanza) per line
    cur_stanza = -1
    cur_line_in_stanza = -1
    prev_blank = True
    for line in lines:
        blank = line.strip() == ""
        if blank:
            prev_blank = True
        else:
            if prev_blank:
                cur_stanza += 1
                cur_line_in_stanza = 0
            else:
                cur_line_in_stanza += 1
            stanza_line_map.append((cur_stanza, cur_line_in_stanza))
            prev_blank = False

    # Now map char positions to (stanza_idx, line_in_stanza)
    char_pos = 0
    si = 0  # index into stanza_line_map (only non-blank lines)
    for line in lines:
        blank = line.strip() == ""
        if not blank:
            sl = stanza_line_map[si]
            si += 1
            for ci in range(len(line)):
                char_to_sl[char_pos + ci] = sl
        char_pos += len(line) + 1

    return char_to_sl


def main():
    print("Loading corpus results...")
    with open(RESULTS_PATH) as f:
        corpus = json.load(f)

    # Compute global entropy median for type classification
    all_entropies = [
        tok["entropy"]
        for poem in corpus
        for tok in poem.get("tokens", [])
        if not is_artifact(tok)
    ]
    entropy_median = statistics.median(all_entropies)
    print(f"Global entropy median: {entropy_median:.3f} ({len(all_entropies)} tokens)")

    # Build lookup: title → corpus entry
    corpus_by_title = {p["metadata"]["title"]: p for p in corpus}

    # Per-stanza records
    stanza_records = []  # dict per stanza

    # Map from poem title to poem text
    poem_texts = {p["title"]: p["text"] for p in POEMS}

    for poem_data in corpus:
        title = poem_data["metadata"].get("title", "")
        era = poem_data["metadata"].get("era", "unknown")
        text = poem_texts.get(title, "")
        if not text:
            continue

        tokens = poem_data.get("tokens", [])
        if not tokens:
            continue

        # Build char_to_sl mapping
        char_to_sl = map_tokens_to_stanza_lines(text, None)

        # Tokenize poem: tokens have "position" (1-based index in token sequence)
        # but also store the substring they correspond to in the text.
        # We'll use character-offset approach via the token text.
        # Tokens have keys: token, position, s2, entropy, rank, alternatives

        # Walk the original text token by token using their decoded text
        # to assign char offsets. Engine stores token["token"] as decoded string.

        # We need to walk the poem text and greedily match each decoded token.
        char_cursor = 0
        token_to_char = []  # (start_char, end_char) for each token
        for tok in tokens:
            tok_str = tok.get("token", "")
            # Find this token text starting at char_cursor
            # Allow small skip for whitespace that may precede the token
            found = False
            for skip in range(5):
                idx = text.find(tok_str, char_cursor + skip)
                if idx == char_cursor + skip:
                    token_to_char.append((idx, idx + len(tok_str)))
                    char_cursor = idx + len(tok_str)
                    found = True
                    break
            if not found:
                token_to_char.append((-1, -1))

        # Identify stanzas from text
        stanzas_lines = segment_poem_into_stanzas(text)
        n_stanzas = len(stanzas_lines)
        if n_stanzas == 0:
            continue

        # For each stanza, collect its tokens
        # Build (stanza_idx, line_in_stanza) for each token
        stanza_line_per_token = []
        for i, tok in enumerate(tokens):
            start_char, end_char = token_to_char[i]
            if start_char == -1:
                stanza_line_per_token.append((-1, -1))
                continue
            # Find which char this token's midpoint falls in
            mid = (start_char + end_char) // 2
            sl = char_to_sl.get(mid, None)
            if sl is None:
                # Try nearby chars
                for delta in range(1, 5):
                    sl = char_to_sl.get(mid - delta) or char_to_sl.get(mid + delta)
                    if sl:
                        break
            stanza_line_per_token.append(sl if sl else (-1, -1))

        # Group tokens by (stanza_idx, line_in_stanza)
        stanza_groups = defaultdict(list)  # stanza_idx -> list of (line_idx, tok)
        for i, tok in enumerate(tokens):
            sl = stanza_line_per_token[i]
            if sl and sl[0] >= 0:
                stanza_groups[sl[0]].append((sl[1], tok))

        # For each stanza, compute stats
        for stanza_idx, tok_sl_list in stanza_groups.items():
            if stanza_idx >= n_stanzas:
                continue
            n_lines = len(stanzas_lines[stanza_idx])
            form = classify_form(n_lines)

            # Separate by line
            by_line = defaultdict(list)
            for line_idx, tok in tok_sl_list:
                by_line[line_idx].append(tok)

            # Clean each line's tokens
            all_clean = []
            by_line_clean = {}
            for li, toks in by_line.items():
                clean = clean_tokens(toks)
                by_line_clean[li] = clean
                all_clean.extend(clean)

            if len(all_clean) < MIN_TOKENS_PER_STANZA:
                continue

            s2_vals = [t["s2"] for t in all_clean]
            mean_s2 = mean(s2_vals)
            max_s2 = max(s2_vals)
            pos_ratio = sum(1 for v in s2_vals if v > 0) / len(s2_vals)

            # First and last line S2
            line_indices = sorted(by_line_clean.keys())
            first_line_toks = by_line_clean.get(line_indices[0], [])
            last_line_toks = by_line_clean.get(line_indices[-1], [])
            first_line_s2 = mean([t["s2"] for t in first_line_toks]) if first_line_toks else None
            last_line_s2 = mean([t["s2"] for t in last_line_toks]) if last_line_toks else None
            last_line_boost = (last_line_s2 - first_line_s2) if (
                first_line_s2 is not None and last_line_s2 is not None
            ) else None

            # Entropy stats
            ent_vals = [t["entropy"] for t in all_clean]
            mean_ent = mean(ent_vals)

            stanza_records.append({
                "title": title,
                "era": era,
                "stanza_idx": stanza_idx,
                "n_lines": n_lines,
                "form": form,
                "n_tokens": len(all_clean),
                "mean_s2": mean_s2,
                "max_s2": max_s2,
                "pos_s2_ratio": pos_ratio,
                "peak_to_mean": max_s2 / max(mean_s2, 0.01) if mean_s2 > 0 else None,
                "first_line_s2": first_line_s2,
                "last_line_s2": last_line_s2,
                "last_line_boost": last_line_boost,
                "mean_entropy": mean_ent,
            })

    print(f"Total stanzas analyzed: {len(stanza_records)}")

    # Aggregate by form
    by_form = defaultdict(list)
    for rec in stanza_records:
        by_form[rec["form"]].append(rec)

    form_summary = {}
    for form, recs in sorted(by_form.items(), key=lambda x: -len(x[1])):
        if len(recs) < MIN_STANZAS_PER_FORM:
            continue
        mean_s2_list = [r["mean_s2"] for r in recs if r["mean_s2"] is not None]
        max_s2_list = [r["max_s2"] for r in recs if r["max_s2"] is not None]
        pos_list = [r["pos_s2_ratio"] for r in recs if r["pos_s2_ratio"] is not None]
        ptm_list = [r["peak_to_mean"] for r in recs if r["peak_to_mean"] is not None]
        boost_list = [r["last_line_boost"] for r in recs if r["last_line_boost"] is not None]
        ent_list = [r["mean_entropy"] for r in recs if r["mean_entropy"] is not None]

        form_summary[form] = {
            "n_stanzas": len(recs),
            "n_poems": len(set(r["title"] for r in recs)),
            "mean_s2": round(mean(mean_s2_list), 4) if mean_s2_list else None,
            "mean_max_s2": round(mean(max_s2_list), 4) if max_s2_list else None,
            "mean_pos_s2_ratio": round(mean(pos_list), 4) if pos_list else None,
            "mean_peak_to_mean": round(mean(ptm_list), 4) if ptm_list else None,
            "mean_last_line_boost": round(mean(boost_list), 4) if boost_list else None,
            "mean_entropy": round(mean(ent_list), 4) if ent_list else None,
        }

    # Aggregate by era for the most common forms
    top_forms = [f for f, v in form_summary.items()]
    by_era_form = defaultdict(lambda: defaultdict(list))
    for rec in stanza_records:
        if rec["form"] in top_forms:
            by_era_form[rec["era"]][rec["form"]].append(rec)

    era_form_summary = {}
    for era, forms in by_era_form.items():
        era_form_summary[era] = {}
        for form, recs in forms.items():
            if len(recs) < 3:
                continue
            mean_s2_list = [r["mean_s2"] for r in recs if r["mean_s2"] is not None]
            boost_list = [r["last_line_boost"] for r in recs if r["last_line_boost"] is not None]
            era_form_summary[era][form] = {
                "n": len(recs),
                "mean_s2": round(mean(mean_s2_list), 4) if mean_s2_list else None,
                "mean_last_line_boost": round(mean(boost_list), 4) if boost_list else None,
            }

    # Rank forms by mean_s2
    ranked = sorted(
        [(f, v) for f, v in form_summary.items() if v["mean_s2"] is not None],
        key=lambda x: -x[1]["mean_s2"]
    )

    output = {
        "n_stanzas_total": len(stanza_records),
        "entropy_median": round(entropy_median, 4),
        "form_summary": form_summary,
        "form_ranked_by_mean_s2": [(f, v["mean_s2"]) for f, v in ranked],
        "form_ranked_by_last_line_boost": sorted(
            [(f, form_summary[f]["mean_last_line_boost"])
             for f in form_summary
             if form_summary[f]["mean_last_line_boost"] is not None],
            key=lambda x: -(x[1] if x[1] is not None else -999)
        ),
        "era_form_summary": era_form_summary,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to {OUTPUT_PATH}")
    print("\n=== Form Summary (ranked by mean S₂) ===")
    for form, s2 in output["form_ranked_by_mean_s2"]:
        d = form_summary[form]
        boost = d["mean_last_line_boost"]
        boost_str = f"{boost:+.3f}" if boost is not None else "N/A"
        print(f"  {form:<25} n={d['n_stanzas']:>4}  mean_s2={s2:+.3f}  "
              f"max_s2={d['mean_max_s2']:.2f}  "
              f"pos%={d['mean_pos_s2_ratio']:.1%}  "
              f"last_line_boost={boost_str}")

    print("\n=== Last Line Boost (ranked) ===")
    for form, boost in output["form_ranked_by_last_line_boost"]:
        if boost is not None:
            print(f"  {form:<25}  last_line_boost={boost:+.3f}")

    return output


if __name__ == "__main__":
    main()
