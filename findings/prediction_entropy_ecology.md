# Prediction Entropy Ecology: The Full Shape of GPT-2's Uncertainty at High-S2 Moments

**Date:** 2026-10-10  
**Experiment:** `experiments/prediction_entropy_ecology.py` → `results/prediction_entropy_ecology.json`  
**Corpus:** 240 texts, 24,824 artifact-free tokens (p_newline < 0.9, control excluded)  
**New poems added:** Stein "If I Told Him," Perec lipogram excerpt, Bök "Eunoia" Ch. A, Bernstein ×2, Niedecker "Poet's Work" (6 poems → oulipo: 1→4, language: 3→5, imagist: 2→3)  
**Builds on:** `alternatives_architecture.md` (Ambush/Fog binary), `prediction_field_homogeneity.md`, `entropy_conditioned_deviation.md`

---

## Research Question

Yesterday's work introduced a binary classification of GPT-2's prediction field:
**Ambush** (top prediction dominates, top_ratio > 2) vs. **Fog** (diffuse field, top_ratio ≤ 2).
This experiment replaces that binary with a continuous measure: the **Shannon entropy of the
top-10 alternatives distribution** (H_top10), normalized so they sum to 1.

H_top10 = −∑ (p_i / Z) · log₂(p_i / Z)  where Z = sum of top-10 probs

Range: 0 (only one prediction has all the mass) to log₂(10) ≈ 3.32 (perfectly flat top-10).

Three core questions:
1. Does H_top10 have a linear or non-linear relationship with S2?
2. Do different poetic schools have characteristic prediction entropy landscapes?
3. Does this measure clarify what OuLiPo constraints do to GPT-2's expectations?

---

## Finding 1: A U-Shaped Relationship — Concentrated Predictions Are "High Stakes"

| H_top10 bin | Description | n | Mean S2 | High S2% (≥3) |
|---|---|---|---|---|
| 0.0 – 1.0 | Very concentrated | 2,968 | **+0.040** | **9.7%** |
| 1.0 – 1.5 | Concentrated | 1,441 | −0.510 | 16.2% |
| 1.5 – 2.0 | Moderate | 2,156 | −0.496 | 18.2% |
| 2.0 – 2.5 | Medium diffuse | 4,279 | **−0.603** | 16.4% |
| 2.5 – 3.0 | Diffuse | 8,207 | −0.480 | 17.0% |
| 3.0 – 3.3 | Maximum entropy | 5,736 | −0.324 | 15.5% |

**The U-shape is the central finding.** When H_top10 is lowest (0–1.0, very concentrated
predictions), **mean S2 is the highest of any bin (+0.040)**, yet only 9.7% of tokens
achieve S2 ≥ 3 — the lowest high-S2 rate in the table. The middle bins (H_top10 2.0–2.5)
have the lowest mean S2 (−0.603) and roughly average high-S2 rates.

Interpretation: Very concentrated prediction fields are **all-or-nothing**. When the model
places most of its top-10 mass on one or two tokens:
- **Conforming poets** produce deeply negative S2 (expected choice, very low surprisal)
- **Deviating poets** produce enormous S2 — the model was almost certain and got it completely wrong

The 9.7% who deviate at H_top10 < 1.0 pull the mean S2 to near-zero despite 90.3% conformity.
These concentrated-field deviations are the highest-payoff moments in the corpus.

---

## Finding 2: Rank Confirms the H_top10 Structure

| Rank band | n | Mean H_top10 | Mean S2 |
|---|---|---|---|
| rank = 1 (top-1 match) | 8,123 | **1.611** | −2.779 |
| rank 2–5 | 5,300 | 2.505 | −2.071 |
| rank 6–10 | 1,885 | 2.678 | −0.768 |
| rank 11–50 | 3,490 | 2.712 | +0.424 |
| rank 51–500 | 3,786 | 2.747 | +2.597 |
| rank > 500 | 2,240 | **2.782** | +6.072 |

When a poet matches the top prediction (rank 1), H_top10 is 1.611 — well below average.
The model typically concentrates its prediction when it gets the right answer. As the poet
deviates further (rank rises), H_top10 rises too — the model was less certain in the first
place at those positions.

**But the H_top10 range is narrow** (1.611 to 2.782) while S2 swings from −2.779 to +6.072.
The structure of the prediction field (H_top10) is a secondary factor; the distance of
the actual token from that field (rank, surprisal) drives S2 primarily.

---

## Finding 3: The Grammar Gap Confirmed — Function-to-Content Switch Has Highest H_top10

| Transition type | n | Mean H_top10 | Mean S2 | Pos S2% |
|---|---|---|---|---|
| function → content | 4,602 | **2.696** | +2.740 | 72.2% |
| content → function | 992 | 2.596 | −0.022 | 42.1% |
| content → content | 5,923 | 2.317 | −0.164 | 36.0% |
| other | 13,307 | 2.165 | −1.631 | 18.2% |

When the model expects a function word but the poet installs content, not only is S2 highest
(+2.740), but H_top10 is also highest (2.696) — the model was already somewhat uncertain
within its expected class. These are "fog" deviations: the model had no clear single
prediction, and the poet found content where grammar was expected.

When the model expects content and the poet writes content (content→content), H_top10 is
lower (2.317) and S2 is near-zero (−0.164) — content-to-content exchanges happen in more
predictable slots.

---

## Finding 4: OuLiPo and Concrete Poetry — Ambushing the Most Certain Moments

Era-level mean H_top10 at **high-S2 tokens only** (S2 ≥ 3), ordered by H_top10:

| Era | n | Mean H_top10 | Mean S2 | Ambush% |
|---|---|---|---|---|
| deep_image | 15 | **2.676** | 5.356 | 33.3% |
| metaphysical | 78 | 2.610 | 5.682 | 51.3% |
| early_modern | 93 | 2.609 | 5.830 | 41.9% |
| spoken_word | 31 | 2.549 | 5.663 | 38.7% |
| confessional | 77 | 2.538 | 6.000 | 40.3% |
| romantic | 331 | 2.457 | 6.158 | 49.8% |
| language | 64 | 2.298 | 6.022 | **64.1%** |
| modernist | 421 | 2.332 | 6.421 | 53.9% |
| ballad | 140 | 2.295 | 6.949 | 55.0% |
| beat | 131 | 2.174 | **8.577** | 54.2% |
| song_lyrics | 67 | 2.119 | 5.959 | 61.2% |
| **oulipo** | 92 | **2.096** | 6.112 | **62.0%** |
| **concrete** | 15 | **1.650** | 7.474 | **66.7%** |

**OuLiPo and concrete poetry cluster at the BOTTOM of the H_top10 ranking.**

- **Concrete**: Mean H_top10 = 1.650 (lowest of all eras), Ambush% = 66.7%
- **OuLiPo**: Mean H_top10 = 2.096 (second lowest), Ambush% = 62.0%

When these formal/constraint poems achieve high S2, they do so by **breaking the model's
most confident predictions** — the "ambush" strategy. The formal constraint (vowel limitation
in Bök, lipogram in Perec, repetition structure in Stein) FORCES the poet to place tokens
where ordinary language would be highly predictable, and then the constraint mandates an
unexpected choice at exactly those high-certainty moments.

Contrast with **deep image** (H_top10 = 2.676, Ambush% = 33.3%) and **metaphysical** poetry
(H_top10 = 2.610, Ambush% = 51.3%): these traditions surprise in already-uncertain contexts.
They are "fog explorers" — they wade into the model's least certain zones and find images
the model never considered.

**The constraint-vs-exploration axis**: This is a fundamental distinction in how poets
manage information:
- **Constraint poets (OuLiPo, concrete)**: Create surprise at certainty — ambush strategy
- **Image poets (deep image, metaphysical)**: Create surprise at uncertainty — fog strategy
- **Language poetry** (H_top10 = 2.298, Ambush% = 64.1%): Aligned with constraint strategy,
  breaking certain slots with non-referential language

---

## Finding 5: New OuLiPo Poems Confirm the Pattern

S2 profiles for the 4 newly-analyzed OuLiPo poems:

| Poem | Era | Avg S2 (clean) | High S2% |
|---|---|---|---|
| Bök — "Eunoia: Chapter A" | oulipo | −0.002 | **21.4%** |
| Stein — "If I Told Him" | oulipo | +0.056 | 19.8% |
| Perec — "Lipogram (no E)" | oulipo | −0.597 | 14.9% |
| Existing: Perec "Variations on A" | oulipo | −0.443 | 16.0% |

**Bök's all-A vowel constraint** produces the highest high-S2 rate of the 4 OuLiPo poems
(21.4%), confirming that strong lexical constraints force more frequent unexpected choices.

**Stein's "If I Told Him"** has near-zero average S2 (+0.056) — the repetitive structure
("Would he like it if Napoleon") creates a private predictability engine: GPT-2 learns
the poem's internal grammar as it reads, and the repetitions cycle between expected
(low S2) and unexpected (high S2) as Stein varies and returns.

**Perec's lipogram** (no E in English translation) has the lowest high-S2% (14.9%) and
most negative average S2 (−0.597). The "no E" constraint in English forces unusual words,
but many of those unusual words are still morphologically predictable in context (plurals,
past tenses), so the constraint doesn't necessarily break GPT-2's top predictions.

For comparison, **Lorine Niedecker's spare imagist poem "Poet's Work"** has:
- Avg S2 = +0.085, High S2% = 24.1%

Despite being 9 lines and only 23 tokens, it achieves the highest high-S2 rate of any
of the new poems. The extreme compression of "condense / No layoff / from this / condensery"
creates exactly the kind of lexical ambush this study finds in constraint poetry — but
without formal constraints, through pure imagist economy.

---

## Finding 6: Ambush vs. Fog × H_top10 — Mutual Confirmation

| Type | n | Mean H_top10 | Mean S2 | H_top10 > 2.5 |
|---|---|---|---|---|
| Ambush (top_ratio > 2) | 2,002 | **1.996** | 6.473 | 33.1% |
| Fog (top_ratio ≤ 2) | 1,908 | **2.848** | 5.856 | **85.5%** |

The H_top10 measure aligns cleanly with the binary Ambush/Fog classification:
- Ambush tokens have mean H_top10 = 1.996 (concentrated field)
- Fog tokens have mean H_top10 = 2.848 (diffuse field)
- 85.5% of Fog tokens have H_top10 > 2.5, vs. only 33.1% of Ambush tokens

This confirms the Ambush/Fog classification as a reliable proxy for prediction field
concentration, while H_top10 provides a continuous measure for gradient analyses.

---

## Core Finding: Two Axes of Surprise

This analysis establishes two independent axes that together characterize any high-S2 moment:

| | **Low H_top10** (concentrated field) | **High H_top10** (diffuse field) |
|---|---|---|
| **High S2** | **Concentrated Ambush**: Rare, extreme. OuLiPo, concrete, ballad. | **Distributed Fog**: More frequent, moderate force. Deep image, confessional, metaphysical. |
| **Low S2** | **Concentrated Conformity**: The norm. Top-1 match with model's certain prediction. | **Distributed Conformity**: "Lucky hit" — chose from diffuse field without surprising. |

**OuLiPo and concrete operate in the top-left cell**: rare, extreme ambushes at the model's
most confident moments. Deep image operates top-right: numerous moderate surprises in
uncertain territory.

The H_top10 measure adds a dimension that rank and S2 alone cannot provide: the **character
of the expectation being violated** — whether the poet struck at certainty or waded through
uncertainty to find something new.

---

## Suggested Next Steps

1. **Phonological analysis**: Do low-H_top10 (ambush) positions show phonological similarity
   between predicted and actual tokens? The model was sure of one word — did the poet
   choose something that sounds like it?

2. **Within-poem ambush/fog arc**: Does a poem's ratio of ambush-to-fog moments shift
   over its course? The "deviate early, resolve late" finding suggests ambush moments
   (breaking certain slots) might be more concentrated at poem openings.

3. **Constraint poetry expansion**: Add more OuLiPo poems (N+7 texts, Mathews) and
   run the H_top10 analysis to test whether N+7 (semantic substitution) and lipogram
   (phonological substitution) have different prediction field profiles.

4. **The "certainty budget"**: Compute the total mass of positions with H_top10 < 1.5
   (very concentrated predictions) per poem. Do poems vary systematically in how many
   "ambush-eligible" positions they contain? This would measure a poem's "certainty
   infrastructure" — the predictable scaffolding that constraint poets exploit.
