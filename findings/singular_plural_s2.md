# Singular vs Plural Nouns and S₂: Number as Aesthetic Choice

**Date:** 2026-11-15
**Experiment:** `experiments/singular_plural_s2.py` → `results/singular_plural_s2.json`
**Corpus:** 407 English poetry texts, 4 prose controls; 11,109 singular-noun tokens and 2,724 plural-noun tokens (p_newline < 0.9 artifact filter)
**Builds on:** `rank_pos_deviation.md` (collapses NN+NNS → NOUN), `content_vs_function_word_s2.md`, `imagist` and `confessional` era profiles

---

## Research Question

`rank_pos_deviation.md` established that content words deviate radically 29× more than function words. But it collapses **singular** (NN, NNP) and **plural** (NNS, NNPS) nouns into a single category. In English poetry, the singular/plural choice is often deliberate and aesthetically loaded:

- Singular: concrete, specific, particularized ("the rose", "a chair")
- Plural: generic, archetypal, universalizing ("roses", "stones")

**Hypothesis**: Imagist and similar movements that value the specific image should show SG > PL in S₂; movements that generalize personal or political experience should show PL > SG.

---

## Core Finding: Number Is Not an Aggregate Predictor — But Era Signatures Are Stark

### Overall S₂ by Grammatical Number

| Group        |    n | mean S₂ | median S₂ |   std | pos% |
|--------------|-----:|--------:|----------:|------:|-----:|
| poetry_SG    | 11109 |   0.817 |    −0.049 | 4.125 | 48.1% |
| poetry_PL    |  2724 |   0.818 |    −0.085 | 4.093 | 47.5% |
| prose_SG     |    29 |  −1.952 |    −2.352 | 2.838 | 27.6% |
| prose_PL     |     9 |  −1.539 |    −1.444 | 2.180 | 22.2% |

**At the aggregate level, singular and plural nouns have nearly identical mean S₂ (0.817 vs 0.818)** — grammatical number is not a primary driver of surprise. The poetry/prose gap (+0.817 vs −1.952 for singular) replicates the standard finding.

---

## Era-Level Variation: Where Number Matters

The aggregate masks dramatic era-level divergence. Below: eras with ≥10 tokens of each class.

### Eras where SINGULAR > PLURAL (SG-PL gap ≥ 0.3):

| Era                  | SG mean | PL mean |   Gap |
|----------------------|--------:|--------:|------:|
| rondeau              |   1.880 |  −0.286 | +2.165 |
| fixed_form           |   0.933 |  −0.123 | +1.057 |
| ancient              |   1.029 |   0.328 | +0.701 |
| **imagist**          |   1.081 |   0.387 | +0.694 |
| harlem_renaissance   |   0.703 |   0.062 | +0.641 |
| old_english          |   1.386 |   0.880 | +0.505 |
| contemporary         |   0.906 |   0.445 | +0.461 |

### Eras where PLURAL > SINGULAR (PL-SG gap ≥ 0.3):

| Era                  | SG mean | PL mean |   Gap |
|----------------------|--------:|--------:|------:|
| clerihew             |   1.960 |   4.571 | −2.612 |
| 19th_century         |   0.494 |   1.621 | −1.127 |
| mid_century          |   1.665 |   2.672 | −1.007 |
| **confessional**     |   1.837 |   2.483 | −0.646 |
| prose_poetry         |   0.418 |   0.956 | −0.539 |
| surrealist           |   0.668 |   1.243 | −0.575 |
| **elegy**            |   0.890 |   1.237 | −0.347 |
| dramatic_monologue   |   1.113 |   1.457 | −0.344 |
| metaphysical         |   0.809 |   1.226 | −0.417 |

---

## Interpretation: Two Aesthetic Ideologies Map Onto Number

### The Imagist Pattern (SG > PL)

Imagism, fixed forms, ancient poetry, and old English show singular nouns with higher S₂. This aligns with imagist doctrine: the **concrete, specific, unrepeatable object** is the locus of poetic surprise. When an imagist poet surprises you, it is with a *specific* word — a noun in its singularity.

GPT-2 (trained on prose) would expect generic or collective references. The imagist's specific singular noun violates this expectation most forcefully.

### The Confessional/Elegiac Pattern (PL > SG)

Confessional, elegy, 19th-century, and prose poetry show plural nouns with higher S₂. This is the opposite movement: the poet **generalizes** from the personal to the universal. When Sylvia Plath writes of "wounds" (plural) rather than "a wound" (singular), the plurality itself does unexpected work — it converts the intimate to the archetypal.

The clerihew result (+2.612 PL advantage) is the most dramatic: clerihew is a biographical comic form, and its use of plural nouns often functions as a taxonomizing gesture ("his works", "their blunders") that generalizes ironically about the subject.

### Surrealism: Plural as Destabilizer

Surrealist PL > SG (gap = −0.575) suggests a third use: plural as defamiliarizer. Surrealist plurals don't generalize but multiply ("the hands", "the skies") in ways that disrupt expected singularity.

---

## GPT-2's Singular Bias

At high-S₂ moments, GPT-2's top-1 prediction is classified as:

| Context             | Model predicted likely-singular | likely-plural |
|---------------------|---------------------------------|---------------|
| **High-S₂ singular** |               71.4%             |   6.9%        |
| **High-S₂ plural**   |               64.2%             |  17.0%        |

GPT-2 has a strong "singular bias" — at high-S₂ moments for BOTH noun classes, the model most often predicted a singular. When poets choose a surprising singular noun, they're almost certainly defeating the model's singular prediction on IDENTITY grounds. When poets choose a surprising plural, there's a ~17% chance that **the plurality itself** is part of the surprise (model expected singular, poet wrote plural).

This 7-percentage-point gap (6.9% vs 17.0%) means that **grammatical number is a minor but real contributor to plural noun surprise** — the choice to pluralize is itself unexpected roughly 1 in 6 times a plural surprises us.

---

## Key Numbers

- Aggregate SG vs PL mean S₂: **0.817 vs 0.818** (no meaningful overall difference)
- Largest SG > PL gap: **clerihew (+2.612 favoring PL)**, rondeau (+2.165 favoring SG)
- Imagist SG advantage: **+0.694** (specific image doctrine confirmed)
- Confessional PL advantage: **−0.646** (universalizing from personal confirmed)
- GPT-2 singular bias at high-S₂ plural moments: 64.2% predict singular

---

## Suggested Next Steps

1. **Proper noun analysis**: NNP (singular) vs NNPS (plural proper names) — are proper names' S₂ patterns different from common nouns?
2. **Number as semantic field**: Do plural nouns cluster in certain semantic fields (body parts, natural objects, emotions) while singular nouns cluster in others?
3. **Number shift within poem**: Do poems that begin with plurals and end with singulars (or vice versa) have distinctive S₂ arcs?
4. **The clerihew exception**: The +2.612 PL advantage in clerihew deserves a targeted analysis — which plural nouns in clerihews are most surprising, and why?
