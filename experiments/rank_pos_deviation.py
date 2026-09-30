"""
Rank Distance × Part-of-Speech: What Grammatical Category Do Poets Exploit for
Near-Miss vs. Radical Departures?

The rank_distance_analysis.md found two deviation strategies:
  - Near-miss (rank 11-50): constrained deviation, preferred when GPT-2 is confident
  - Radical (rank > 500): liberated deviation, preferred when GPT-2 is uncertain

This experiment asks: do these strategies cluster in different grammatical categories?
Hypothesis: Content words (NOUN, ADJ) may favor radical departures (semantic richness
allows going anywhere), while function words (PREP, DET, PRON) stay near-miss (their
alternatives are structurally constrained).

Builds on: rank_distance_analysis.md, syntactic_position_vs_s2.md
"""

import json
import math
import statistics
from collections import defaultdict

import nltk
import nltk.pathsec
nltk.pathsec.ALLOW_PROXIED_FETCH = True
try:
    nltk.data.find("tokenizers/punkt_tab")
except LookupError:
    nltk.download("punkt_tab", quiet=True)
try:
    nltk.data.find("taggers/averaged_perceptron_tagger_eng")
except LookupError:
    nltk.download("averaged_perceptron_tagger_eng", quiet=True)


# ── Penn Treebank → broad POS category ──────────────────────────────────────
_PENN_TO_CAT = {
    "NN": "NOUN", "NNS": "NOUN", "NNP": "NOUN", "NNPS": "NOUN",
    "VB": "VERB", "VBD": "VERB", "VBG": "VERB",
    "VBN": "VERB", "VBP": "VERB", "VBZ": "VERB",
    "MD": "AUX",
    "JJ": "ADJ", "JJR": "ADJ", "JJS": "ADJ",
    "RB": "ADV", "RBR": "ADV", "RBS": "ADV",
    "DT": "DET",
    "IN": "PREP",
    "CC": "CONJ",
    "PRP": "PRON", "PRP$": "PRON", "WP": "PRON", "WP$": "PRON",
    ".": "PUNCT", ",": "PUNCT", ":": "PUNCT", "``": "PUNCT",
    "''": "PUNCT", "-LRB-": "PUNCT", "-RRB-": "PUNCT",
}


def broad_cat(penn_tag: str) -> str:
    return _PENN_TO_CAT.get(penn_tag, "OTHER")


def reconstruct_and_offsets(gpt2_tokens):
    chars = []
    offsets = []
    for tok in gpt2_tokens:
        text = tok["token"]
        start = len(chars)
        chars.extend(text)
        offsets.append((start, len(chars)))
    return "".join(chars), offsets


def assign_pos(gpt2_tokens, full_text, offsets):
    try:
        words = nltk.word_tokenize(full_text)
        tagged = nltk.pos_tag(words)
    except Exception:
        return ["OTHER"] * len(gpt2_tokens)

    word_spans = []
    cursor = 0
    for word, tag in tagged:
        idx = full_text.lower().find(word.lower(), cursor)
        if idx == -1:
            word_spans.append((word, tag, cursor, cursor + len(word)))
        else:
            word_spans.append((word, tag, idx, idx + len(word)))
            cursor = idx + len(word)

    pos_per_token = []
    for tok_start, tok_end in offsets:
        best = "OTHER"
        for _word, penn, w_start, w_end in word_spans:
            if tok_end > w_start and tok_start < w_end:
                best = broad_cat(penn)
                break
        pos_per_token.append(best)
    return pos_per_token


def rank_bucket(rank):
    if rank == 1:
        return "rank_1"
    elif rank <= 5:
        return "top_2_5"
    elif rank <= 10:
        return "top_6_10"
    elif rank <= 20:
        return "near_miss_11_20"
    elif rank <= 50:
        return "near_miss_21_50"
    elif rank <= 100:
        return "moderate_51_100"
    elif rank <= 500:
        return "wide_101_500"
    elif rank <= 1000:
        return "far_501_1000"
    else:
        return "radical_1000plus"


# High-level strategy groupings
def deviation_strategy(rank):
    if rank <= 10:
        return "conformist"
    elif rank <= 50:
        return "near_miss"
    elif rank <= 100:
        return "moderate"
    elif rank <= 500:
        return "wide"
    else:
        return "radical"


# ── Load data ────────────────────────────────────────────────────────────────
with open("results/corpus_results.json") as f:
    data = json.load(f)

# Focus on English poetry (exclude control prose)
poetry = [d for d in data
          if d["metadata"].get("era") != "control"
          and d["metadata"].get("language", "en") == "en"]

prose = [d for d in data
         if d["metadata"].get("era") == "control"
         and d["metadata"].get("language", "en") == "en"]

print(f"Poetry texts: {len(poetry)}, Prose texts: {len(prose)}")

# ── Core accumulation ────────────────────────────────────────────────────────
# For each (strategy, POS) cell: collect counts, S2 values
strategy_pos_s2 = defaultdict(lambda: defaultdict(list))   # [strategy][pos] → [s2...]
strategy_pos_rank = defaultdict(lambda: defaultdict(list))  # [strategy][pos] → [rank...]

# Track per-era too
era_pos_strategy = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))  # [era][pos][strategy]

processed = 0
skipped = 0

for entry in poetry:
    tokens = entry["tokens"]
    era = entry["metadata"].get("era", "unknown")

    try:
        full_text, offsets = reconstruct_and_offsets(tokens)
        pos_labels = assign_pos(tokens, full_text, offsets)
    except Exception:
        skipped += 1
        continue

    for tok, pos in zip(tokens, pos_labels):
        rank = tok.get("rank")
        if rank is None:
            continue
        p_newline = tok.get("p_newline", 0)
        if p_newline >= 0.9:  # skip stanza-break artifact
            continue

        s2 = tok.get("s2", 0)
        strat = deviation_strategy(rank)

        strategy_pos_s2[strat][pos].append(s2)
        strategy_pos_rank[strat][pos].append(rank)
        era_pos_strategy[era][pos][strat] += 1

    processed += 1

print(f"Processed: {processed} poems, Skipped: {skipped}")
print()

# ── Table 1: Overall POS × Strategy distribution ─────────────────────────────
STRATEGIES = ["conformist", "near_miss", "moderate", "wide", "radical"]
POSS = ["NOUN", "VERB", "ADJ", "ADV", "PREP", "DET", "PRON", "CONJ", "PUNCT", "AUX", "OTHER"]

# Count total tokens per (strategy, POS)
strat_pos_count = defaultdict(lambda: defaultdict(int))
for strat, pos_dict in strategy_pos_s2.items():
    for pos, vals in pos_dict.items():
        strat_pos_count[strat][pos] = len(vals)

# Total per POS (to compute row percentages)
pos_total = defaultdict(int)
for strat in STRATEGIES:
    for pos in POSS:
        pos_total[pos] += strat_pos_count[strat][pos]

print("=" * 80)
print("TABLE 1: Deviation Strategy Distribution by POS Category (% of POS tokens)")
print("=" * 80)
header = f"{'POS':<8} {'Total':>7} | {'Conform':>8} {'NearMiss':>9} {'Moderate':>9} {'Wide':>7} {'Radical':>8}"
print(header)
print("-" * 70)
for pos in POSS:
    total = pos_total[pos]
    if total < 20:
        continue
    row = f"{pos:<8} {total:>7} |"
    for strat in STRATEGIES:
        pct = 100 * strat_pos_count[strat][pos] / total if total > 0 else 0
        row += f" {pct:>8.1f}%"
    print(row)
print()

# ── Table 2: Radical% per POS (ranking) ──────────────────────────────────────
print("=" * 80)
print("TABLE 2: Radical Deviation Rate per POS (sorted high→low)")
print("=" * 80)
radical_rates = []
for pos in POSS:
    total = pos_total[pos]
    if total < 50:
        continue
    rad = strat_pos_count["radical"][pos]
    rad_pct = 100 * rad / total
    avg_s2_radical = statistics.mean(strategy_pos_s2["radical"][pos]) if strategy_pos_s2["radical"][pos] else float("nan")
    avg_s2_conform = statistics.mean(strategy_pos_s2["conformist"][pos]) if strategy_pos_s2["conformist"][pos] else float("nan")
    median_rank = statistics.median(strategy_pos_rank["radical"][pos]) if strategy_pos_rank["radical"][pos] else float("nan")
    radical_rates.append((pos, total, rad_pct, avg_s2_radical, avg_s2_conform, median_rank))

radical_rates.sort(key=lambda x: -x[2])
print(f"{'POS':<8} {'Total':>7} {'Radical%':>9} {'AvgS2(rad)':>11} {'AvgS2(con)':>11} {'Med.rank(rad)':>14}")
print("-" * 70)
for pos, total, rad_pct, avg_s2_rad, avg_s2_con, med_rank in radical_rates:
    print(f"{pos:<8} {total:>7} {rad_pct:>8.1f}% {avg_s2_rad:>11.3f} {avg_s2_con:>11.3f} {med_rank:>14.0f}")
print()

# ── Table 3: Near-miss strategy rate per POS ─────────────────────────────────
print("=" * 80)
print("TABLE 3: Near-Miss Deviation Rate per POS (sorted high→low)")
print("=" * 80)
nearmiss_rates = []
for pos in POSS:
    total = pos_total[pos]
    if total < 50:
        continue
    nm = strat_pos_count["near_miss"][pos]
    nm_pct = 100 * nm / total
    nearmiss_rates.append((pos, total, nm_pct))

nearmiss_rates.sort(key=lambda x: -x[2])
print(f"{'POS':<8} {'Total':>7} {'NearMiss%':>10}")
print("-" * 40)
for pos, total, nm_pct in nearmiss_rates:
    print(f"{pos:<8} {total:>7} {nm_pct:>9.1f}%")
print()

# ── Table 4: Content vs Function word comparison ──────────────────────────────
print("=" * 80)
print("TABLE 4: Content Words vs. Function Words — Deviation Strategy Profiles")
print("=" * 80)
content_poss = ["NOUN", "VERB", "ADJ", "ADV"]
function_poss = ["PREP", "DET", "PRON", "CONJ", "AUX"]

def aggregate_group(pos_list):
    totals = {s: 0 for s in STRATEGIES}
    for pos in pos_list:
        for strat in STRATEGIES:
            totals[strat] += strat_pos_count[strat][pos]
    grand_total = sum(totals.values())
    return grand_total, {s: 100 * n / grand_total for s, n in totals.items()} if grand_total else {}

content_total, content_pcts = aggregate_group(content_poss)
function_total, function_pcts = aggregate_group(function_poss)

for label, total, pcts in [("Content words", content_total, content_pcts),
                             ("Function words", function_total, function_pcts)]:
    row = f"{label:<16} n={total:,} | "
    for s in STRATEGIES:
        row += f"{s[:8]}:{pcts.get(s,0):.1f}% "
    print(row)
print()

# ── Table 5: Top examples — notable radical departures by POS ────────────────
print("=" * 80)
print("TABLE 5: Sample Radical Departures (rank > 500) by POS Category")
print("=" * 80)

radical_examples = defaultdict(list)  # pos → [(rank, s2, token, context_poem)]

for entry in poetry:
    tokens = entry["tokens"]
    title = entry["metadata"].get("title", "?")
    author = entry["metadata"].get("author", "?")
    era = entry["metadata"].get("era", "?")

    try:
        full_text, offsets = reconstruct_and_offsets(tokens)
        pos_labels = assign_pos(tokens, full_text, offsets)
    except Exception:
        continue

    for tok, pos in zip(tokens, pos_labels):
        rank = tok.get("rank")
        if rank is None or rank <= 500:
            continue
        if tok.get("p_newline", 0) >= 0.9:
            continue
        s2 = tok.get("s2", 0)
        if pos in ["NOUN", "VERB", "ADJ", "ADV", "PREP"]:
            radical_examples[pos].append((rank, s2, tok.get("token", ""), author, title))

# Show top-5 most extreme per content POS
for pos in ["NOUN", "VERB", "ADJ", "ADV", "PREP"]:
    examples = sorted(radical_examples[pos], key=lambda x: -x[1])[:5]
    if not examples:
        continue
    print(f"\n  {pos} — top 5 highest S₂ radical departures:")
    for rank, s2, token, author, title in examples:
        print(f"    token={repr(token):<20} rank={rank:>5}  S₂={s2:>6.2f}  {author} — {title}")

print()

# ── Table 6: Radical rate by era × POS ───────────────────────────────────────
print("=" * 80)
print("TABLE 6: NOUN Radical% and VERB Radical% by Era")
print("=" * 80)

era_noun_verb = []
for era, pos_dict in era_pos_strategy.items():
    if era == "unknown":
        continue
    noun_totals = {s: pos_dict.get("NOUN", {}).get(s, 0) for s in STRATEGIES}
    verb_totals = {s: pos_dict.get("VERB", {}).get(s, 0) for s in STRATEGIES}
    noun_total = sum(noun_totals.values())
    verb_total = sum(verb_totals.values())
    if noun_total < 30 or verb_total < 30:
        continue
    noun_rad = 100 * noun_totals["radical"] / noun_total
    verb_rad = 100 * verb_totals["radical"] / verb_total
    noun_nm = 100 * noun_totals["near_miss"] / noun_total
    verb_nm = 100 * verb_totals["near_miss"] / verb_total
    era_noun_verb.append((era, noun_total, noun_rad, noun_nm, verb_total, verb_rad, verb_nm))

era_noun_verb.sort(key=lambda x: -x[2])  # sort by noun radical%
print(f"{'Era':<20} {'N(noun)':>8} {'N_rad%':>7} {'N_nm%':>7} | {'N(verb)':>8} {'V_rad%':>7} {'V_nm%':>7}")
print("-" * 75)
for era, nn, nr, nnm, nv, vr, vnm in era_noun_verb:
    print(f"{era:<20} {nn:>8} {nr:>6.1f}% {nnm:>6.1f}% | {nv:>8} {vr:>6.1f}% {vnm:>6.1f}%")
print()

# ── Summary ───────────────────────────────────────────────────────────────────
print("=" * 80)
print("SUMMARY")
print("=" * 80)
# Find POS with highest vs. lowest radical rate
if radical_rates:
    highest_rad = radical_rates[0]
    lowest_rad = radical_rates[-1]
    print(f"Highest radical departure rate: {highest_rad[0]} ({highest_rad[2]:.1f}%)")
    print(f"Lowest radical departure rate:  {lowest_rad[0]} ({lowest_rad[2]:.1f}%)")

# Content vs function word radical rates
if content_pcts and function_pcts:
    print(f"Content words radical%: {content_pcts.get('radical', 0):.1f}%")
    print(f"Function words radical%: {function_pcts.get('radical', 0):.1f}%")
    ratio = content_pcts.get('radical', 0) / function_pcts.get('radical', 1)
    print(f"Ratio content:function radical = {ratio:.2f}x")
