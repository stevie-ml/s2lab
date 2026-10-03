"""
Interruption Structures and S₂: Dashes, Parentheses, and the Poetry of the Aside

Research question: When poets interrupt the syntactic flow with dashes or parentheses,
what is the information-theoretic profile of the interruption?

Dickinson's em-dashes are the canonical example, but interruption is pervasive across
poetry traditions (Milton's elaborate asides, Keats's parenthetical qualifications,
modern poets' bracket-asides). The hypothesis:

  H1: Interruption-opener tokens (dash, open-paren) arrive at HIGH entropy moments —
      the model is uncertain what comes next, and the poet uses that uncertainty to
      insert an aside.

  H2: The first token INSIDE an interruption has higher S2 than baseline (unexpected
      content given the syntactic context that was just established).

  H3: The first token AFTER a closed interruption (the "re-entry" to the main clause)
      has lower S2 than the interruption itself — the poet returns to a more predictable
      continuation.

  H4: Dickinson's dashes have a distinctive profile compared to dashes used by other poets
      (she uses them not just as asides but as structural line-ending punctuation).

Secondary question: Do dash-bounded interruptions and paren-bounded interruptions differ
informationally? (Different poets, different eras, different structural roles.)
"""

import json
import re
import statistics
from collections import defaultdict

# Load corpus
with open("results/corpus_results.json") as f:
    corpus = json.load(f)


def is_artifact(token_data):
    return token_data.get("p_newline", 0) >= 0.9


def clean_token_text(token):
    """Strip GPT-2 leading space marker."""
    return token.replace("Ġ", "").replace("Ċ", "\n").strip()


def is_dash(token_text):
    """Detect em dash or en dash (as token text, possibly with leading space)."""
    cleaned = clean_token_text(token_text)
    return cleaned in ["–", "—", "--", "-–", "–-"]


def is_open_paren(token_text):
    cleaned = clean_token_text(token_text)
    return cleaned == "("


def is_close_paren(token_text):
    cleaned = clean_token_text(token_text)
    return cleaned == ")"


# --- Main data collection ---
# For each interruption event we record:
#   - type: "dash_pair", "dash_single", "paren_pair"
#   - poet, era
#   - s2_at_opener: s2 of the dash/( token itself
#   - entropy_at_opener: entropy at the opener
#   - s2_first_inside: s2 of first non-artifact token inside
#   - mean_s2_inside: mean s2 across all tokens inside
#   - s2_at_closer: s2 of closing dash/)
#   - s2_first_after: s2 of first non-artifact token after closing
#   - poem_baseline_s2: mean s2 of this poem's non-artifact non-interruption tokens

interruptions = []
baseline_s2 = []  # all non-artifact poetry tokens
poet_baselines = defaultdict(list)  # poet → [s2 values]
era_baselines = defaultdict(list)

SKIP_ERAS = {"control", "cliche_control"}


def find_next_non_artifact(tokens, start, max_look=10):
    """Return index of next non-artifact token after start, or None."""
    for j in range(start, min(start + max_look, len(tokens))):
        if not is_artifact(tokens[j]):
            return j
    return None


def find_next_dash_or_end(tokens, start, max_look=50):
    """
    After an opening dash, find the matching closing dash.
    Returns (closing_index, interior_indices) or (None, interior_indices).
    A 'closing dash' is a dash token within max_look tokens.
    Interior = non-artifact tokens between opener and closer.
    """
    interior = []
    for j in range(start, min(start + max_look, len(tokens))):
        tok = tokens[j]
        if is_artifact(tok):
            continue
        if is_dash(tok["token"]):
            return j, interior
        interior.append(j)
    return None, interior


def find_close_paren(tokens, start, max_look=30):
    """Find matching close paren. Returns (close_idx, interior_indices)."""
    interior = []
    depth = 0
    for j in range(start, min(start + max_look, len(tokens))):
        tok = tokens[j]
        if is_artifact(tok):
            continue
        txt = clean_token_text(tok["token"])
        if txt == "(":
            depth += 1
        elif txt == ")":
            if depth == 0:
                return j, interior
            depth -= 1
        interior.append(j)
    return None, interior


for text in corpus:
    meta = text["metadata"]
    tokens = text["tokens"]
    era = meta.get("era", "unknown")
    author = meta.get("author", "Unknown")
    lang = meta.get("language", "en")

    if era in SKIP_ERAS or lang not in ["en", "english", "en_us"]:
        continue

    # Gather baseline
    for t in tokens:
        if not is_artifact(t):
            baseline_s2.append(t["s2"])
            poet_baselines[author].append(t["s2"])
            era_baselines[era].append(t["s2"])

    # Poem-level context tracking: which token indices are "inside interruptions"
    inside_interruption = set()

    # First pass: find all paren pairs
    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if is_artifact(tok):
            i += 1
            continue

        # --- Parenthetical ------------------------------------------------
        if is_open_paren(tok["token"]):
            close_idx, interior_idxs = find_close_paren(tokens, i + 1)
            if close_idx is not None and len(interior_idxs) >= 1:
                inside_interruption.update(interior_idxs)

                # Opener metrics
                opener_s2 = tok["s2"]
                opener_h = tok["entropy"]

                # First token inside
                first_inside_idx = find_next_non_artifact(tokens, i + 1, 5)
                first_inside = tokens[first_inside_idx]["s2"] if first_inside_idx and first_inside_idx < close_idx else None

                # Mean inside
                inside_s2_vals = [tokens[j]["s2"] for j in interior_idxs
                                  if not is_artifact(tokens[j])]
                mean_inside = statistics.mean(inside_s2_vals) if inside_s2_vals else None

                # Closer s2
                closer_s2 = tokens[close_idx]["s2"]

                # First token after closer
                after_idx = find_next_non_artifact(tokens, close_idx + 1, 10)
                first_after = tokens[after_idx]["s2"] if after_idx else None

                interruptions.append({
                    "type": "paren",
                    "author": author,
                    "era": era,
                    "title": meta["title"],
                    "s2_at_opener": opener_s2,
                    "entropy_at_opener": opener_h,
                    "s2_first_inside": first_inside,
                    "mean_s2_inside": mean_inside,
                    "n_inside": len(inside_s2_vals),
                    "s2_at_closer": closer_s2,
                    "s2_first_after": first_after,
                })
            i += 1
            continue

        # --- Dash pair --------------------------------------------------------
        if is_dash(tok["token"]) and not is_artifact(tok):
            # Look for a closing dash
            close_idx, interior_idxs = find_next_dash_or_end(tokens, i + 1)
            if close_idx is not None and len(interior_idxs) >= 1:
                inside_interruption.update(interior_idxs)

                opener_s2 = tok["s2"]
                opener_h = tok["entropy"]

                first_inside_idx = find_next_non_artifact(tokens, i + 1, 5)
                first_inside = tokens[first_inside_idx]["s2"] if first_inside_idx and first_inside_idx < close_idx else None

                inside_s2_vals = [tokens[j]["s2"] for j in interior_idxs
                                  if not is_artifact(tokens[j])]
                mean_inside = statistics.mean(inside_s2_vals) if inside_s2_vals else None

                closer_s2 = tokens[close_idx]["s2"]

                after_idx = find_next_non_artifact(tokens, close_idx + 1, 10)
                first_after = tokens[after_idx]["s2"] if after_idx else None

                interruptions.append({
                    "type": "dash_pair",
                    "author": author,
                    "era": era,
                    "title": meta["title"],
                    "s2_at_opener": opener_s2,
                    "entropy_at_opener": opener_h,
                    "s2_first_inside": first_inside,
                    "mean_s2_inside": mean_inside,
                    "n_inside": len(inside_s2_vals),
                    "s2_at_closer": closer_s2,
                    "s2_first_after": first_after,
                })
                # Skip to after the closer
                i = close_idx + 1
                continue

            # Single dash (line-ending or non-paired)
            after_idx = find_next_non_artifact(tokens, i + 1, 10)
            first_after = tokens[after_idx]["s2"] if after_idx else None
            inside_s2_vals = []  # no interior for single dash

            interruptions.append({
                "type": "dash_single",
                "author": author,
                "era": era,
                "title": meta["title"],
                "s2_at_opener": tok["s2"],
                "entropy_at_opener": tok["entropy"],
                "s2_first_inside": None,
                "mean_s2_inside": None,
                "n_inside": 0,
                "s2_at_closer": None,
                "s2_first_after": first_after,
            })

        i += 1


# ──────────────────────────────────────────────────────────────────────────────
# Analysis
# ──────────────────────────────────────────────────────────────────────────────

print("=" * 70)
print("INTERRUPTION STRUCTURES AND S₂")
print("=" * 70)

baseline_mean = statistics.mean(baseline_s2)
baseline_h_mean = None  # compute separately
all_h = []
for text in corpus:
    meta = text["metadata"]
    if meta.get("era") in SKIP_ERAS:
        continue
    for t in text["tokens"]:
        if not is_artifact(t):
            all_h.append(t["entropy"])
baseline_h_mean = statistics.mean(all_h) if all_h else 0.0

print(f"\nBaseline (all non-artifact poetry tokens):")
print(f"  N = {len(baseline_s2)}")
print(f"  mean S2 = {baseline_mean:.3f}")
print(f"  mean entropy = {baseline_h_mean:.3f}")

# Separate by type
by_type = defaultdict(list)
for ev in interruptions:
    by_type[ev["type"]].append(ev)

print(f"\nInterruptions found:")
for itype, evs in sorted(by_type.items()):
    print(f"  {itype}: {len(evs)} instances")

# ── Type-level summary ────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("TYPE SUMMARY: S₂ PROFILE ACROSS INTERRUPTION PHASES")
print("=" * 70)

for itype in ["dash_pair", "paren", "dash_single"]:
    evs = by_type.get(itype, [])
    if len(evs) < 3:
        continue

    opener_s2s = [e["s2_at_opener"] for e in evs]
    opener_hs = [e["entropy_at_opener"] for e in evs]
    first_insides = [e["s2_first_inside"] for e in evs if e["s2_first_inside"] is not None]
    mean_insides = [e["mean_s2_inside"] for e in evs if e["mean_s2_inside"] is not None]
    first_afters = [e["s2_first_after"] for e in evs if e["s2_first_after"] is not None]

    print(f"\n  [{itype.upper()}]  n = {len(evs)}")
    print(f"    Entropy at opener:         {statistics.mean(opener_hs):>7.3f} bits  "
          f"(vs baseline {baseline_h_mean:.3f}, Δ {statistics.mean(opener_hs) - baseline_h_mean:+.3f})")
    print(f"    S2 at opener:              {statistics.mean(opener_s2s):>7.3f}      "
          f"(vs baseline {baseline_mean:.3f}, Δ {statistics.mean(opener_s2s) - baseline_mean:+.3f})")
    if first_insides:
        delta_fi = statistics.mean(first_insides) - baseline_mean
        pct_pos = sum(1 for x in first_insides if x > 0) / len(first_insides)
        print(f"    S2 at 1st inside token:    {statistics.mean(first_insides):>7.3f}      "
              f"(Δ {delta_fi:+.3f}, {pct_pos:.0%} positive)")
    if mean_insides:
        print(f"    Mean S2 across interior:   {statistics.mean(mean_insides):>7.3f}      "
              f"(Δ {statistics.mean(mean_insides) - baseline_mean:+.3f})")
    if first_afters:
        delta_fa = statistics.mean(first_afters) - baseline_mean
        pct_pos = sum(1 for x in first_afters if x > 0) / len(first_afters)
        print(f"    S2 at re-entry (1st after):{statistics.mean(first_afters):>7.3f}      "
              f"(Δ {delta_fa:+.3f}, {pct_pos:.0%} positive)")

# ── Hypothesis tests ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("HYPOTHESIS TESTS")
print("=" * 70)

# H1: Opener arrives at high entropy
all_opener_hs = [e["entropy_at_opener"] for e in interruptions
                 if e["type"] in ("dash_pair", "paren")]
if all_opener_hs:
    mean_oh = statistics.mean(all_opener_hs)
    verdict = "CONFIRMED" if mean_oh > baseline_h_mean else "NOT CONFIRMED"
    print(f"\n  H1 (Opener arrives at HIGH entropy): {verdict}")
    print(f"       Opener H = {mean_oh:.3f} vs baseline {baseline_h_mean:.3f}  "
          f"(Δ {mean_oh - baseline_h_mean:+.3f})")

# H2: First token inside has higher S2
all_first_inside = [e["s2_first_inside"] for e in interruptions
                    if e["type"] in ("dash_pair", "paren")
                    and e["s2_first_inside"] is not None]
if all_first_inside:
    mean_fi = statistics.mean(all_first_inside)
    verdict = "CONFIRMED" if mean_fi > baseline_mean else "NOT CONFIRMED"
    print(f"\n  H2 (1st token inside has higher S2): {verdict}")
    print(f"       1st inside S2 = {mean_fi:.3f} vs baseline {baseline_mean:.3f}  "
          f"(Δ {mean_fi - baseline_mean:+.3f})")

# H3: Re-entry token lower S2 than interior
all_mean_inside = [e["mean_s2_inside"] for e in interruptions
                   if e["type"] in ("dash_pair", "paren")
                   and e["mean_s2_inside"] is not None]
all_reentry = [e["s2_first_after"] for e in interruptions
               if e["type"] in ("dash_pair", "paren")
               and e["s2_first_after"] is not None]
if all_mean_inside and all_reentry:
    # Match only paired examples (same index in list)
    paired = [(interruptions[i]["mean_s2_inside"], interruptions[i]["s2_first_after"])
              for i in range(len(interruptions))
              if interruptions[i]["type"] in ("dash_pair", "paren")
              and interruptions[i]["mean_s2_inside"] is not None
              and interruptions[i]["s2_first_after"] is not None]
    if paired:
        inside_vals = [p[0] for p in paired]
        reentry_vals = [p[1] for p in paired]
        mean_inside_avg = statistics.mean(inside_vals)
        mean_reentry_avg = statistics.mean(reentry_vals)
        verdict = "CONFIRMED" if mean_reentry_avg < mean_inside_avg else "NOT CONFIRMED"
        print(f"\n  H3 (Re-entry token < interior S2): {verdict}")
        print(f"       Interior mean S2 = {mean_inside_avg:.3f}, re-entry S2 = {mean_reentry_avg:.3f}  "
              f"(Δ {mean_reentry_avg - mean_inside_avg:+.3f})")

# ── Poet-level breakdown ──────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("POET-LEVEL BREAKDOWN (poets with ≥3 paired interruptions)")
print("=" * 70)

poet_events = defaultdict(list)
for ev in interruptions:
    if ev["type"] in ("dash_pair", "paren"):
        poet_events[ev["author"]].append(ev)

print(f"\n{'Poet':<28} {'Era':<18} {'N':>5} {'H@open':>8} {'S2@1stIn':>10} {'S2@reent':>10} {'Δreent':>8}")
print("-" * 82)

sorted_poets = sorted(poet_events.items(), key=lambda x: -len(x[1]))
for author, evs in sorted_poets:
    if len(evs) < 3:
        continue
    era = evs[0]["era"]

    hs = [e["entropy_at_opener"] for e in evs]
    fis = [e["s2_first_inside"] for e in evs if e["s2_first_inside"] is not None]
    ras = [e["s2_first_after"] for e in evs if e["s2_first_after"] is not None]

    mean_h = statistics.mean(hs)
    mean_fi = statistics.mean(fis) if fis else float("nan")
    mean_ra = statistics.mean(ras) if ras else float("nan")
    poet_base = statistics.mean(poet_baselines.get(author, [0]))
    delta_reentry = mean_ra - poet_base if ras else float("nan")

    print(f"  {author:<28} {era:<18} {len(evs):>5} {mean_h:>8.3f} {mean_fi:>10.3f} {mean_ra:>10.3f} {delta_reentry:>+8.3f}")

# ── Era breakdown ─────────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("ERA BREAKDOWN: ENTROPY AT OPENER vs. BASELINE")
print("=" * 70)

era_events = defaultdict(list)
for ev in interruptions:
    if ev["type"] in ("dash_pair", "paren"):
        era_events[ev["era"]].append(ev)

print(f"\n{'Era':<22} {'N':>5} {'H@opener':>10} {'ΔH':>8} {'S2@1stIn':>10} {'Δ1stIn':>8} {'S2@reent':>10}")
print("-" * 80)

sorted_eras = sorted(era_events.items(), key=lambda x: -len(x[1]))
for era, evs in sorted_eras:
    if len(evs) < 3:
        continue
    hs = [e["entropy_at_opener"] for e in evs]
    fis = [e["s2_first_inside"] for e in evs if e["s2_first_inside"] is not None]
    ras = [e["s2_first_after"] for e in evs if e["s2_first_after"] is not None]
    era_base = statistics.mean(era_baselines.get(era, [baseline_mean]))

    mean_h = statistics.mean(hs)
    mean_fi = statistics.mean(fis) if fis else float("nan")
    mean_ra = statistics.mean(ras) if ras else float("nan")

    print(f"  {era:<22} {len(evs):>5} {mean_h:>10.3f} {mean_h - baseline_h_mean:>+8.3f} "
          f"{mean_fi:>10.3f} {mean_fi - era_base:>+8.3f} {mean_ra:>10.3f}")

# ── Dickinson special ─────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("SPECIAL FOCUS: EMILY DICKINSON's DASHES")
print("=" * 70)

dick_evs = [e for e in interruptions if "Dickinson" in e["author"]]
other_dash = [e for e in interruptions if e["type"] in ("dash_pair", "dash_single")
              and "Dickinson" not in e["author"]]

if dick_evs:
    dick_paired = [e for e in dick_evs if e["type"] == "dash_pair"]
    dick_single = [e for e in dick_evs if e["type"] == "dash_single"]
    print(f"\n  Dickinson dash events: {len(dick_evs)} total "
          f"({len(dick_paired)} paired, {len(dick_single)} single)")

    if dick_paired:
        fi_d = [e["s2_first_inside"] for e in dick_paired if e["s2_first_inside"] is not None]
        ra_d = [e["s2_first_after"] for e in dick_paired if e["s2_first_after"] is not None]
        h_d = [e["entropy_at_opener"] for e in dick_paired]
        print(f"  Paired dashes:  H@opener = {statistics.mean(h_d):.3f},  "
              f"S2@1stInside = {statistics.mean(fi_d) if fi_d else float('nan'):.3f},  "
              f"S2@reentry = {statistics.mean(ra_d) if ra_d else float('nan'):.3f}")

    if dick_single:
        ra_ds = [e["s2_first_after"] for e in dick_single if e["s2_first_after"] is not None]
        h_ds = [e["entropy_at_opener"] for e in dick_single]
        print(f"  Single dashes:  H@opener = {statistics.mean(h_ds):.3f},  "
              f"S2@next = {statistics.mean(ra_ds) if ra_ds else float('nan'):.3f}")

if other_dash:
    other_paired = [e for e in other_dash if e["type"] == "dash_pair"]
    other_single = [e for e in other_dash if e["type"] == "dash_single"]
    print(f"\n  Non-Dickinson dashes: {len(other_dash)} total "
          f"({len(other_paired)} paired, {len(other_single)} single)")
    if other_paired:
        fi_o = [e["s2_first_inside"] for e in other_paired if e["s2_first_inside"] is not None]
        ra_o = [e["s2_first_after"] for e in other_paired if e["s2_first_after"] is not None]
        h_o = [e["entropy_at_opener"] for e in other_paired]
        print(f"  Paired dashes:  H@opener = {statistics.mean(h_o):.3f},  "
              f"S2@1stInside = {statistics.mean(fi_o) if fi_o else float('nan'):.3f},  "
              f"S2@reentry = {statistics.mean(ra_o) if ra_o else float('nan'):.3f}")

# ── Notable examples ──────────────────────────────────────────────────────────
print("\n" + "=" * 70)
print("NOTABLE EXAMPLES: HIGH-S2 FIRST-INSIDE TOKENS")
print("=" * 70)

high_first_inside = [e for e in interruptions
                     if e["type"] in ("dash_pair", "paren")
                     and e["s2_first_inside"] is not None
                     and e["s2_first_inside"] > 3.0]
high_first_inside.sort(key=lambda e: -e["s2_first_inside"])

for ev in high_first_inside[:15]:
    n = ev["n_inside"]
    s2fi = ev["s2_first_inside"]
    s2ra = ev.get("s2_first_after")
    print(f"  [{ev['type']}] {ev['author']} ({ev['era']}) — '{ev['title']}'")
    print(f"    S2 at 1st inside = {s2fi:.2f}, interior N = {n}, re-entry S2 = {s2ra if s2ra else 'N/A'}")

print("\n" + "=" * 70)
print("NOTABLE EXAMPLES: HIGH-S2 RE-ENTRY TOKENS")
print("=" * 70)

high_reentry = [e for e in interruptions
                if e["type"] in ("dash_pair", "paren")
                and e["s2_first_after"] is not None
                and e["s2_first_after"] > 3.0]
high_reentry.sort(key=lambda e: -e["s2_first_after"])

for ev in high_reentry[:10]:
    n = ev["n_inside"]
    s2ra = ev["s2_first_after"]
    mean_in = ev["mean_s2_inside"]
    print(f"  [{ev['type']}] {ev['author']} ({ev['era']}) — '{ev['title']}'")
    print(f"    Re-entry S2 = {s2ra:.2f}, interior mean S2 = {mean_in if mean_in else 'N/A'}")

print("\nDone.")
