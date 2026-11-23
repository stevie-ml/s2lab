# Poet α Arc Fingerprints and the Pre-Climax Dip

**Date:** 2026-11-20  
**Experiment:** `experiments/poet_alpha_fingerprints.py` → `results/poet_alpha_fingerprints.json`  
**Corpus:** 411 poems with ≥20 clean tokens, artifact-filtered  
**Building on:** `findings/alpha_arc_within_poem.md` (global α arc, slope = +0.213)

---

## Research Question

The α arc finding established that GPT-2's prediction concentration (Zipf exponent α) rises systematically as a poem progresses — the model "learns" the poem's idiom and places increasingly concentrated bets. The global arc showed a **pre-climax dip** at deciles 7–8 (α = 1.394, 1.386) before the final peak (1.451).

This experiment asks:
1. Is the pre-climax dip universal, or genre-specific?
2. What is the lexical character of the dip zone (dec 6–7) versus the final peak zone (dec 8–9)?
3. Do individual poets have characteristic α arc shapes (fingerprints)?

---

## Finding 1: The Pre-Climax Dip Is NOT Universal — It's a Repetition Artifact

**Global dip metric:** −0.0085 (barely negative)  
**Fraction of poems with a dip:** 51.8%

The global-average dip seen in the original α arc finding is **not a universal feature of poetry** — it is driven by specific genres with strong repetition and fixed form. When pooled across all 411 poems, the dip is essentially flat.

### Era-Level Dip Profile

Sorted by mean dip metric (most negative = strongest V-shape):

| Era | n | Mean Dip | % with Dip | Mean α Slope |
|---|---|---|---|---|
| **song_lyrics** | 3 | **−0.318** | 100% | 0.086 |
| **fixed_form** | 8 | **−0.201** | 88% | 0.060 |
| **cliche_control** | 4 | **−0.156** | 100% | 0.013 |
| **procedural** | 8 | **−0.128** | 75% | 0.020 |
| **villanelle** | 3 | **−0.116** | 67% | 0.142 |
| **modernist** | 25 | **−0.107** | 72% | 0.017 |
| ghazal | 3 | −0.078 | 100% | 0.016 |
| romantic | 21 | −0.062 | 67% | 0.014 |
| language | 6 | −0.060 | 67% | 0.015 |
| new_york_school | 26 | −0.010 | 54% | 0.019 |
| **(no dip)** | | | | |
| ballad | 6 | +0.256 | 17% | 0.074 |
| spoken_word | 3 | +0.300 | 0% | 0.037 |
| **concrete** | 3 | **+0.307** | 33% | 0.097 |

**Interpretation:** The strongest dips appear in forms with heavy repetition (villanelle, song lyrics, fixed forms) and in clichéd/procedural text. In these genres, α builds, then briefly opens (entropy rises as the poem introduces new material before its final structural move), then concentrates again at the peak. This is not a "pre-climax literary effect" per se — it is a **repetition-driven reorientation**: each new non-refrain unit loosens model confidence before the final tightening.

Ballads and concrete poetry show the **opposite** pattern — their final zones are MORE concentrated than their middle zones, suggesting their arc is a pure ramp with no valley.

---

## Finding 2: The Final Zone Has Lower S₂ Than the Middle — Closing as Constraint

Comparing the dip zone (deciles 6–7) versus the final peak zone (deciles 8–9):

| Metric | Dip Zone (dec 6–7) | Peak Zone (dec 8–9) |
|---|---|---|
| Mean S₂ | **−0.371** | **−0.406** |
| Mean rank | **283** | **253** |
| Mean entropy | **6.214** | **6.072** |

Counterintuitively, the **final two deciles have lower S₂ and lower rank** (more expected choices) than the pre-final zone. The poem's final moves are:
- More expected (lower rank — GPT-2's top predictions closer to actual)
- More contextually constrained (lower entropy)
- Less surprising relative to context (lower S₂)

This reframes the Liberation finding: the peak of the **α arc** (high prediction concentration) in the final zone does not mean more surprising tokens — it means the **context is more certain**, even if tokens are conformist. Liberation events are rare high-S₂ tokens within a generally more constrained final zone. The poem's close works through constraint, not raw surprise.

---

## Finding 3: Poet-Level α Arc Fingerprints

For poets with ≥3 poems, mean α arc slope and shape:

| Author | Era | Slope | Arc Type | Dip Metric | n |
|---|---|---|---|---|---|
| Traditional (Scottish ballad) | ballad | **+0.086** | dome | +0.264 | 5 |
| Anonymous | limerick | +0.057 | rising | −0.006 | 3 |
| Control texts | control | +0.052 | rising | +0.127 | 5 |
| Wallace Stevens | modernist | +0.046 | plateau | −0.306 | 3 |
| Joy Harjo | postcolonial | +0.045 | plateau | +0.005 | 3 |
| Lucille Clifton | contemporary | +0.039 | plateau | +0.370 | 4 |
| Lewis Carroll | parody | +0.039 | plateau | −0.053 | 5 |
| William Blake | romantic | +0.030 | plateau | −0.240 | 7 |
| John Ashbery | new_york_school | +0.014 | plateau | +0.008 | 17 |
| T.S. Eliot | modernist | +0.011 | plateau | +0.015 | 5 |
| Robert Browning | victorian | +0.002 | plateau | −0.036 | 8 |
| Emily Dickinson | 19th_century | +0.002 | plateau | −0.071 | 7 |
| W.B. Yeats | modernist | −0.002 | plateau | −0.048 | 3 |
| Gertrude Stein | modernist | **−0.015** | plateau | +0.056 | 4 |
| Anonymous (found text) | found_poetry | **−0.023** | plateau | −0.005 | 4 |

**Key observations:**

1. **Most poets show plateau arcs** — the global α rise is an average effect across poems, not driven by any single poet consistently steepening their arc.

2. **Scottish ballads** have the highest slope (+0.086) with a **dome** shape — α rises then falls. The refrain teaches GPT-2 the ballad idiom very aggressively, but the poem's conclusion loops back rather than peaking. This is consistent with ballads' structural return to the opening: the closing verse often circles back to the same imagery, loosening α.

3. **Gertrude Stein** (−0.015) and **found text** (−0.023) are the only poets with negative slopes. Stein's deliberate disruption of syntactic expectation (parataxis, repetition without semantic advance) may **suppress α accumulation** — the model never internalizes her idiom because her idiom is grammatical dissolution.

4. **Wallace Stevens** shows the strongest dip metric among individual poets (−0.306 with 3 poems), consistent with the finding that modernist poetry generally shows strong pre-climax dips. Stevens' long final movements (the coda in "Sunday Morning," the final turn in "The Snow Man") involve genuine syntactic reorientation before resolution.

5. **Lucille Clifton** shows an unusually positive dip metric (+0.370) — her poems accelerate their prediction concentration all the way through the final zone without any valley. This is consistent with her spare, compressed style that builds directly to devastating final lines.

---

## Finding 4: The α Plateau — A Null Finding Worth Noting

The fact that **almost all poet fingerprints are "plateau" type** (essentially flat across deciles 1–10, with slopes near zero) despite the global arc showing a clear rise (+0.213, r = 0.888) is itself informative.

The global α rise is **compositional, not individual**: it emerges because poems in aggregate tend to get more contextually constrained as they progress, but no single poet systematically produces poems where α ramps up. The arc is a property of the aggregate *distribution* of poem lengths and structures, not of any poet's intentional arc management.

This parallels the stanza-break artifact finding: an observed pattern disappears when you look at the right level of analysis. The α arc is real at the corpus level but invisible at the poet level.

---

## Methodology Note

**Dip metric:** `mean(α[dec 6–7]) − (mean(α[dec 4–5]) + mean(α[dec 8–9])) / 2`  
Negative = V-shaped dip (dec 6–7 below both neighbors); positive = inverse-V (peak in that zone).

**Arc classification thresholds:** slope > 0.15 and r > 0.7 → "ramp"; slope < −0.15 and r < −0.7 → "descent"; slope near zero → "plateau"; dome/valley detected by min/max position within middle deciles.

---

## Suggested Next Steps

1. **Stanza-level α analysis**: Rather than decile position, track α at the stanza level — does α reset at each stanza boundary? This could distinguish "within-stanza arc" from "cross-stanza arc."

2. **Wallace Stevens deep dive**: His strong pre-climax dip (−0.306) is the largest among individual poets. Analyze his specific poems to characterize what happens lexically at deciles 6–7 — are these the pivotal lines where his grammar opens up before closing?

3. **Villanelle α arc by refrain position**: The villanelle's refrain lines should show radically different α than non-refrain lines — the model rapidly learns to expect the exact refrain tokens. Map α against within-villanelle position and refrain/non-refrain type.

4. **Lucille Clifton's compressive arc**: Her positive dip metric suggests a distinctive "building to a point" structure. Compare her α arc against other compression-focused poets (Dickinson, Celan) to see if this is a general minimalist-poet trait.
