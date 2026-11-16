# Deferred Semantic Priming: How Poetic Surprises Reshape GPT-2's Predictions

**Date:** 2026-11-16  
**Experiment:** `experiments/semantic_priming_persistence.py`  
**Data:** `results/semantic_priming_persistence.json`  
**Corpus:** 422 poems | 11,716 high-S2 positions (S2 ≥ 2.0, stanza-artifact filtered) | 44,329 baseline positions

---

## Research Question

After a high-S2 token (a semantic surprise), does GPT-2's prediction distribution for
subsequent tokens shift toward the semantic field of the surprise token? In other words,
does the model *incorporate* a poet's deviation and prime its forward predictions toward
the new semantic territory?

**Hypothesis A** (integration): GPT-2 updates toward the surprise's semantic field —
"summer" leads to predictions of "autumn", "spring", etc.

**Hypothesis B** (resistance): GPT-2 reverts to base-rate predictions, treating the
surprise as a local anomaly.

**Hypothesis C** (deferred integration): priming happens, but with a delay — the
immediate next position is grammatical scaffolding, but 2-3 positions later the
semantic field propagates.

---

## Method

For each high-S2 token W_t at position t, we:
1. Classify W_t into one of 8 semantic fields (BODY, NATURE, TIME, MOTION, EMOTION,
   ABSTRACTION, COLOR, SOUND) via vocabulary lookup
2. For the alternatives GPT-2 predicted at positions t+1, t+2, and t+3, count what
   fraction belong to the same semantic field as W_t
3. Compare to baseline: the same measurement at all non-high-S2 positions

The 8 semantic fields together account for ~10% of all tokens; the priming analysis
covers the 1,186 high-S2 positions where the actual token had a classifiable field.

---

## Primary Finding: Priming Is Deferred, Not Immediate

| Step | Primed Alt% | Baseline Alt% | Delta | N (primed) |
|------|-------------|---------------|-------|------------|
| **t+1** (immediate) | 1.323% | 1.360% | **−0.037%** | 1,141 |
| **t+2** (deferred) | 4.238% | 3.633% | **+0.604%** | 1,128 |
| **t+3** (deferred) | 3.966% | 3.239% | **+0.727%** | 1,117 |

**The immediate next position (t+1) shows slight negative priming** — the model is
*less* likely to predict same-field vocabulary right after a surprise. By t+2 and t+3,
the priming effect reverses: the surprise's semantic field now appears in alternatives
at **+0.6–0.7% above baseline**.

This "deferred priming" aligns with the finding in `post_surprise_signature.md` that
high-S2 tokens are followed immediately by punctuation (comma, dash) or function words
at an elevated rate. The t+1 slot is typically grammatical scaffolding; the semantic
"wake" of the surprise materializes 2–3 positions later.

---

## Finding 2: Field Asymmetry — Time Primes, Color Anti-Primes

### Immediate priming (t+1):

| Semantic Field | Primed Alt% | Baseline Alt% | Delta | Ratio |
|----------------|-------------|---------------|-------|-------|
| **TIME** | 3.418% | 3.027% | **+0.391%** | 1.13× |
| **NATURE** | 1.737% | 1.570% | +0.167% | 1.11× |
| **BODY** | 0.185% | 0.148% | +0.037% | 1.25× |
| ABSTRACTION | 0.336% | 0.495% | −0.159% | 0.68× |
| **SOUND** | 0.196% | 0.453% | −0.257% | 0.43× |
| **EMOTION** | 0.940% | 1.608% | **−0.668%** | 0.59× |
| **COLOR** | 1.348% | 2.308% | **−0.959%** | 0.58× |
| MOTION | 0.079% | 0.171% | −0.092% | 0.46× |

### Deferred priming (t+2):

| Semantic Field | Primed Alt% | Baseline Alt% | Delta |
|----------------|-------------|---------------|-------|
| **BODY** | 5.000% | 2.778% | **+2.222%** |
| **TIME** | 4.851% | 2.896% | **+1.955%** |
| **NATURE** | 6.860% | 5.015% | **+1.845%** |
| EMOTION | 4.828% | 5.519% | −0.692% |
| **COLOR** | 4.382% | 6.373% | **−1.991%** |
| SOUND | 2.745% | 3.561% | −0.816% |

**Two distinct clusters emerge:**

**"Priming" fields** (TIME, NATURE, BODY): Surprising use of these words leads GPT-2
to expect more vocabulary from the same field, particularly at t+2. These are the
"sticky" semantic domains — once a poet introduces the body or time as a surprising
frame, the model expects continued engagement with those domains.

**"Anti-priming" fields** (COLOR, EMOTION, SOUND): Surprising use of these words
*suppresses* subsequent same-field prediction. After a surprising color word, GPT-2
is less likely to predict further color vocabulary; after a surprising emotion word,
less likely to predict emotion words. These are semantic "one-shot" domains — their
surprise value is exhausted by a single high-S2 instance.

---

## Finding 3: Complete Surprises Prime More Than Near-Misses

| Rank category | Alt% at t+1 | N |
|---------------|-------------|---|
| Near-miss (rank < 100) | 0.931% | 290 |
| Far-miss (rank > 1000) | 1.417% | 247 |

Counter-intuitively, tokens that GPT-2 ranked *very* far down (rank > 1000) produce
slightly stronger priming than near-misses (rank < 100). A word that GPT-2 would
never have predicted shifts the model's subsequent predictions more than a word the
model almost expected.

**Interpretation:** Near-miss surprises (rank 2–100) are semantically similar to what
the model expected and don't create strong new semantic territory. Far-miss surprises
introduce genuinely new material that reshapes the prediction landscape. This suggests
that the most "Straussian" poets — who consistently write rank-1000+ tokens — are
doing more work in re-orienting the model's forward expectations.

---

## Finding 4: Strong Priming Examples

Examining positions where > 30% of t+1 alternatives were in the same field as the surprise:

| Surprise token | S2 | Next token | Top alternatives at t+1 | Priming frac | Poet |
|----------------|----|------------|--------------------------|--------------|------|
| `summer` (NATURE) | 3.8 | `autumn` | fall, summer, autumn, winter | **60%** | E.E. Cummings |
| `after` (TIME) | 3.4 | `days` | days, hours, years | **60%** | Austin Dobson |
| `long` (TIME) | 3.1 | `hours` | hours, days, years | **50%** | Robert Browning |
| `autumn` (NATURE) | 7.6 | `sun` | morning, evening, afternoon, day, night | 40% | Richard Wright |
| `bright` (COLOR) | 8.9 | `moon` | red, blue, and, light, lights | 40% | Li Bai |

The E.E. Cummings case is striking: a surprising "summer" (GPT-2 didn't expect this
seasonal vocabulary here) causes GPT-2's very next predictions to include the full
roster of seasonal terms (fall, summer, autumn, winter). The poet "opened a semantic
door" that the model immediately walked through. The actual next word is "autumn" —
the model and poet converge on seasonal continuation.

---

## Synthesis: The "Two-Step" Mechanism of Semantic Surprise

Combining these findings with `post_surprise_signature.md` and
`surprise_liberation_vs_channeling.md`, the following sequence emerges:

**Step 1 (t+1):** A high-S2 token is immediately followed by punctuation or a function
word (the "channeling" effect). GPT-2 at t+1 is predicting grammatical structure, not
semantic content — hence the negative or null priming at t+1.

**Step 2 (t+2-3):** With the grammatical scaffolding in place, GPT-2's context window
now includes the surprising token and its immediate grammatical anchor. The model begins
predicting semantic content again, and this content is shifted toward the surprise's
semantic field. This is the "deferred priming" window.

The semantic fields that escape this two-step mechanism (COLOR, EMOTION, SOUND) may do
so because their surprising instances are often single vivid images — not the opening
of an extended semantic passage. A surprising color word ("crimson") is a brushstroke,
not a door.

---

## Suggested Next Steps

1. **Longitudinal tracking**: Measure priming out to t+5, t+10 to see how long the
   deferred priming effect persists before reverting to baseline.

2. **Within-poem vs across-poem**: Does deferred priming persist across stanza breaks?
   (the stanza boundary is itself a "reset" for the model's context)

3. **Poet-level priming profiles**: Do certain poets generate consistently higher
   deferred priming (Whitman, with his catalogue structures) while others generate
   negative priming throughout (Language poetry, designed to resist semantic entrainment)?

4. **Bidirectional priming**: Does the ACTUAL word at t+2 belong to the same field as
   the surprising t-word more often than baseline? (Here we measured the alternatives;
   the actual token is the stronger test.)
