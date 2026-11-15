"""
Singular vs Plural Noun S2: Does Grammatical Number Drive Poetic Surprise?

In English poetry, the choice between singular ("the rose") and plural ("roses")
is often deliberate. Singular nouns are specific/concrete; plural nouns are
generic/archetypal. rank_pos_deviation.py collapses NN and NNS into a single
NOUN category, losing this distinction.

This experiment asks:
  1. Do singular nouns (NN) and plural nouns (NNS) have different S2 profiles
     in poetry vs prose?
  2. At high-S2 NN moments, does GPT-2's top prediction tend to be NNS (the model
     expected generality but the poet wrote specificity), or vice versa?
  3. Which literary eras show the strongest NN/NNS S2 asymmetry?

Hypothesis: singular nouns should have HIGHER S2 because concrete, specific nouns
are harder to predict than generic plurals; and poetry amplifies this effect.

Builds on: rank_pos_deviation.md, content_vs_function_word_s2.md, syntactic_position_vs_s2.md
"""

import json
import math
import statistics
from collections import defaultdict

import nltk
import nltk.pathsec
nltk.pathsec.ALLOW_PROXIED_FETCH = True
for resource, path in [
    ("punkt_tab", "tokenizers/punkt_tab"),
    ("averaged_perceptron_tagger_eng", "taggers/averaged_perceptron_tagger_eng"),
]:
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(resource, quiet=True)


# ── POS helpers ─────────────────────────────────────────────────────────────

def reconstruct_and_offsets(gpt2_tokens):
    chars = []
    offsets = []
    for tok in gpt2_tokens:
        text = tok["token"]
        start = len(chars)
        chars.extend(text)
        offsets.append((start, len(chars)))
    return "".join(chars), offsets


def assign_fine_noun_class(gpt2_tokens, full_text, offsets):
    """Return per-token label: 'NN', 'NNS', 'NNP', 'NNPS', or None."""
    try:
        words = nltk.word_tokenize(full_text)
        tagged = nltk.pos_tag(words)
    except Exception:
        return [None] * len(gpt2_tokens)

    noun_tags = {"NN", "NNS", "NNP", "NNPS"}
    word_spans = []
    cursor = 0
    for word, tag in tagged:
        idx = full_text.lower().find(word.lower(), cursor)
        if idx == -1:
            word_spans.append((word, tag, cursor, cursor + len(word)))
        else:
            word_spans.append((word, tag, idx, idx + len(word)))
            cursor = idx + len(word)

    per_token = []
    for tok_start, tok_end in offsets:
        best = None
        for _word, penn, w_start, w_end in word_spans:
            if penn in noun_tags and tok_end > w_start and tok_start < w_end:
                best = penn
                break
        per_token.append(best)
    return per_token


def is_noun_plural(penn_tag):
    return penn_tag in ("NNS", "NNPS")


def is_noun_singular(penn_tag):
    return penn_tag in ("NN", "NNP")


# ── Load corpus ───────────────────────────────────────────────────────────────
with open("results/corpus_results.json") as f:
    data = json.load(f)

poetry = [d for d in data
          if d["metadata"].get("era") != "control"
          and d["metadata"].get("language", "en") == "en"]
prose = [d for d in data
         if d["metadata"].get("era") == "control"
         and d["metadata"].get("language", "en") == "en"]

print(f"Poetry: {len(poetry)} texts | Prose: {len(prose)} texts")

ARTIFACT_FILTER = 0.9  # exclude tokens where p(newline) >= threshold

# ── Accumulators ─────────────────────────────────────────────────────────────
# [genre][number_class] → list of s2 values
s2_by_number = {"poetry_SG": [], "poetry_PL": [],
                "prose_SG": [],  "prose_PL": []}

era_sg = defaultdict(list)  # era → [s2 for singular nouns]
era_pl = defaultdict(list)  # era → [s2 for plural nouns]

# At high-S2 singular moments, what is the alternative's number class?
# Collect: when NN token has high S2, is top-1 prediction also NN or NNS?
alt_nn_top1_number = defaultdict(int)   # {NN, NNS, NNP, NNPS, OTHER} → count
alt_nns_top1_number = defaultdict(int)

# Example moments
high_s2_examples_sg = []  # (s2, token, era, top1)
high_s2_examples_pl = []

processed = 0
for corpus_name, texts in [("poetry", poetry), ("prose", prose)]:
    for entry in texts:
        tokens = entry["tokens"]
        era = entry["metadata"].get("era", "unknown")
        full_text, offsets = reconstruct_and_offsets(tokens)
        noun_classes = assign_fine_noun_class(tokens, full_text, offsets)

        for tok, noun_cls in zip(tokens, noun_classes):
            if tok.get("p_newline", 0) >= ARTIFACT_FILTER:
                continue
            if noun_cls is None:
                continue

            s2 = tok["s2"]
            is_sg = is_noun_singular(noun_cls)
            is_pl = is_noun_plural(noun_cls)

            if is_sg:
                s2_by_number[f"{corpus_name}_SG"].append(s2)
                if corpus_name == "poetry":
                    era_sg[era].append(s2)
                # Collect alternative class at high-S2 moments
                if s2 >= 3.0 and tok.get("alternatives"):
                    top1 = tok["alternatives"][0]["token"].strip()
                    # Classify top1 token's number by naive heuristics
                    # (we can't POS-tag alternatives, so use ending)
                    if top1.endswith("s") and not top1.endswith("ss"):
                        alt_nn_top1_number["likely_plural"] += 1
                    elif top1.isalpha():
                        alt_nn_top1_number["likely_singular"] += 1
                    else:
                        alt_nn_top1_number["other"] += 1
                    if s2 >= 5.0:
                        high_s2_examples_sg.append({
                            "s2": s2, "token": tok["token"].strip(),
                            "era": era, "top1": top1,
                            "entropy": tok["entropy"],
                        })
            elif is_pl:
                s2_by_number[f"{corpus_name}_PL"].append(s2)
                if corpus_name == "poetry":
                    era_pl[era].append(s2)
                if s2 >= 3.0 and tok.get("alternatives"):
                    top1 = tok["alternatives"][0]["token"].strip()
                    if top1.endswith("s") and not top1.endswith("ss"):
                        alt_nns_top1_number["likely_plural"] += 1
                    elif top1.isalpha():
                        alt_nns_top1_number["likely_singular"] += 1
                    else:
                        alt_nns_top1_number["other"] += 1
                    if s2 >= 5.0:
                        high_s2_examples_pl.append({
                            "s2": s2, "token": tok["token"].strip(),
                            "era": era, "top1": top1,
                            "entropy": tok["entropy"],
                        })
        processed += 1

print(f"Processed {processed} texts")

# ── Summary statistics ─────────────────────────────────────────────────────
print("\n=== CORE COMPARISON: Singular vs Plural Noun S₂ ===\n")
header = f"{'Group':<20} {'n':>6} {'mean S₂':>10} {'median S₂':>10} {'std':>8} {'pos%':>7}"
print(header)
print("-" * len(header))

for key in ["poetry_SG", "poetry_PL", "prose_SG", "prose_PL"]:
    vals = s2_by_number[key]
    if not vals:
        print(f"{key:<20} {'0':>6}")
        continue
    mn = statistics.mean(vals)
    med = statistics.median(vals)
    sd = statistics.stdev(vals) if len(vals) > 1 else 0
    pos = sum(1 for v in vals if v > 0) / len(vals) * 100
    print(f"{key:<20} {len(vals):>6} {mn:>10.3f} {med:>10.3f} {sd:>8.3f} {pos:>6.1f}%")

# ── SG-PL gap by era ──────────────────────────────────────────────────────
print("\n=== NN vs NNS S₂ GAP BY ERA (poetry only, ≥10 tokens each) ===\n")
print(f"{'Era':<25} {'n_SG':>6} {'n_PL':>6} {'SG mean':>9} {'PL mean':>9} {'Gap (SG-PL)':>12}")
print("-" * 72)

era_rows = []
for era in sorted(set(list(era_sg.keys()) + list(era_pl.keys()))):
    sg = era_sg.get(era, [])
    pl = era_pl.get(era, [])
    if len(sg) < 10 or len(pl) < 10:
        continue
    sg_mean = statistics.mean(sg)
    pl_mean = statistics.mean(pl)
    gap = sg_mean - pl_mean
    era_rows.append((era, len(sg), len(pl), sg_mean, pl_mean, gap))

era_rows.sort(key=lambda x: x[5], reverse=True)
for era, n_sg, n_pl, sg_m, pl_m, gap in era_rows:
    marker = " ← SG>PL" if gap > 0.3 else (" ← PL>SG" if gap < -0.3 else "")
    print(f"{era:<25} {n_sg:>6} {n_pl:>6} {sg_m:>9.3f} {pl_m:>9.3f} {gap:>12.3f}{marker}")

# ── Alternative class at high-S2 ─────────────────────────────────────────
print("\n=== WHAT GPT-2 PREDICTED AT HIGH-S₂ SINGULAR MOMENTS ===\n")
total_nn = sum(alt_nn_top1_number.values())
if total_nn:
    for cls, cnt in sorted(alt_nn_top1_number.items(), key=lambda x: -x[1]):
        print(f"  Top-1 prediction = {cls:<20}: {cnt:>5} ({cnt/total_nn*100:.1f}%)")

print("\n=== WHAT GPT-2 PREDICTED AT HIGH-S₂ PLURAL MOMENTS ===\n")
total_nns = sum(alt_nns_top1_number.values())
if total_nns:
    for cls, cnt in sorted(alt_nns_top1_number.items(), key=lambda x: -x[1]):
        print(f"  Top-1 prediction = {cls:<20}: {cnt:>5} ({cnt/total_nns*100:.1f}%)")

# ── Top examples ─────────────────────────────────────────────────────────
print("\n=== TOP 10 HIGH-S₂ SINGULAR NOUN MOMENTS ===\n")
high_s2_examples_sg.sort(key=lambda x: -x["s2"])
for ex in high_s2_examples_sg[:10]:
    print(f"  S₂={ex['s2']:.2f}  token='{ex['token']}'  top1='{ex['top1']}'  era={ex['era']}  H={ex['entropy']:.2f}")

print("\n=== TOP 10 HIGH-S₂ PLURAL NOUN MOMENTS ===\n")
high_s2_examples_pl.sort(key=lambda x: -x["s2"])
for ex in high_s2_examples_pl[:10]:
    print(f"  S₂={ex['s2']:.2f}  token='{ex['token']}'  top1='{ex['top1']}'  era={ex['era']}  H={ex['entropy']:.2f}")

# ── Save results ─────────────────────────────────────────────────────────
results = {
    "summary": {
        k: {
            "n": len(v),
            "mean": statistics.mean(v) if v else None,
            "median": statistics.median(v) if v else None,
            "std": statistics.stdev(v) if len(v) > 1 else None,
            "pos_ratio": sum(1 for x in v if x > 0) / len(v) if v else None,
        }
        for k, v in s2_by_number.items()
    },
    "era_sg_pl_gap": [
        {"era": e, "n_sg": n_sg, "n_pl": n_pl,
         "sg_mean": sg_m, "pl_mean": pl_m, "gap": gap}
        for e, n_sg, n_pl, sg_m, pl_m, gap in era_rows
    ],
    "alt_top1_at_high_s2_singular": dict(alt_nn_top1_number),
    "alt_top1_at_high_s2_plural": dict(alt_nns_top1_number),
    "top_examples_singular": high_s2_examples_sg[:20],
    "top_examples_plural": high_s2_examples_pl[:20],
}

with open("results/singular_plural_s2.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nResults saved to results/singular_plural_s2.json")
