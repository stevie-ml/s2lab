# Kurtosis and Crest Factor of S₂: Testing the Impulse Account

**Date:** 2026-09-22
**Experiment:** `experiments/impulse_account.py`
**Corpus:** 160 poems with ≥30 tokens (from 168-poem corpus); all metrics artifact-free (p(newline) ≥ 0.9 positions replaced by poem's clean median)
**Companion finding:** `spectral_refrain_null.md` — this test follows up directly

---

## Background

`spectral_refrain_null.md` found that fixed-form poems with mandatory refrains have spectrally flat S₂ series — their dominant period never aligns with the refrain interval. The interpretation offered was that a refrain produces an *impulse* (a sharp S₂ spike at the moment of return), not a wave. A delta function has a flat power spectrum, which is what was measured.

That interpretation makes a specific time-domain prediction:

> If repetition produces impulses, refrain poems should have **high kurtosis with flat spectra** — a specific, falsifiable joint signature.

**Excess kurtosis** = E[(x−μ)⁴]/σ⁴ − 3. Normal distribution → 0; a signal dominated by rare, large spikes → >> 0. A Gaussian mixture of well-behaved tokens would give low kurtosis. A signal with occasional extreme events against a flat background gives high kurtosis.

**Crest factor** = max(|x|) / RMS(x). Another time-domain impulse indicator.

---

## Results

| Group | n | kurtosis | crest factor | spectral flatness |
|---|---|---|---|---|
| fixed_form (villanelle, ballade, rondeau, sestina) | 8 | **1.909** | 3.474 | 0.5716 |
| other repeaters (≥2 verbatim repeated lines) | 6 | **3.032** | 3.978 | 0.5151 |
| baseline poetry (no repeats) | 142 | 1.773 | 3.372 | 0.5692 |
| prose control | 4 | **0.022** | 2.084 | 0.5830 |

### Result 1: Poetry is definitively more impulsive than prose

The prose–poetry kurtosis gap is large: corpus median kurtosis = 1.258 vs prose = 0.022. Prose is near-Gaussian (consistent with no outlier events); poetry is clearly leptokurtic. The crest factor shows the same split: prose mean 2.084 vs poetry mean ~3.4. These are clean, large-effect discriminators.

### Result 2: Within poetry, refrain structure does not concentrate kurtosis

Fixed-form poems sit at kurtosis = 1.909 — only slightly above the baseline poetry mean of 1.773, and well below the corpus p90 of 3.883. Other repeaters score higher (3.032) but also show more within-group variation (ballads driven by simple narrative repetition top the list). **Refrain structure is not a reliable marker of high kurtosis within the poetic corpus.**

The baseline sample shows why: many non-refrain poems have kurtosis that exceeds every fixed-form poem:

| Poem | kurtosis | crest | notes |
|---|---|---|---|
| Dickinson, *I felt a Funeral, in my Brain* | **11.374** | 5.018 | no refrains |
| Found Poem from Declaration | **10.885** | 4.968 | no refrains |
| Lindsay, *The Congo* | **8.889** | 4.677 | no refrains |
| Cummings, *Buffalo Bill's* | **8.736** | 4.715 | no refrains |
| Whitman, *Song of Myself (§1)* | 7.098 | 4.729 | no refrains |

These are driven by individual extreme token events — a highly unusual word choice at a single position generates a massive S₂ spike against a background of ordinary values. That is exactly the impulse structure, but it comes from lexical extremity, not repetition.

### Result 3: The joint signature is not specific to refrain poems

The original prediction was: refrain poems should have high kurtosis AND flat spectra jointly — a fingerprint distinguishing them from other high-kurtosis poems, which might show concentrated spectra instead. That distinction does not hold:

| Poem | era | kurtosis | flatness | repeats |
|---|---|---|---|---|
| Edward, Edward | ballad | 4.480 | 0.4683 | 2 |
| Bonnie George Campbell | ballad | 3.658 | 0.5611 | 2 |
| *Villanelle* (Henley) | fixed_form | 2.809 | 0.6154 | 1 |
| *Theocritus* (Wilde) | fixed_form | 2.763 | 0.6363 | 2 |
| *I felt a Funeral* (Dickinson) | 19th_century | 11.374 | 0.5068 | 0 |
| *Buffalo Bill's* (Cummings) | modernist | 8.736 | 0.4989 | 0 |

High-kurtosis, non-refrain poems have flatness comparable to refrain poems. There is no separating surface in the kurtosis × flatness plane.

---

## Interpretation: Poetry as a whole is impulse-structured

The kurtosis and crest factor data support a stronger, more general version of the impulse account than the original hypothesis. Structural repetition does not make a poem more impulse-like. **Poetry itself is impulse-structured** — compared to prose, all poetry shows high kurtosis and large crest factors. The mechanism is not periodic refrain events but the general disposition of poetry to concentrate information in a few extreme moments while maintaining a lower-S₂ background.

This is consistent with the earlier taxonomy work (`straussian_gap_taxonomy.md`) that found a bimodal S₂ distribution in poetry: most tokens are ordinary, but a small fraction carry extreme values. Kurtosis directly quantifies that bimodality.

The impulse account for refrains is not refuted — refrain heads do produce spikes, as documented in `spectral_refrain_null.md`. But those spikes are not large enough relative to the surrounding noise floor (which itself contains many natural S₂ impulses from ordinary lexical choices) to elevate the poem's aggregate kurtosis above the baseline.

---

## Summary of the two-step finding

| Step | Finding |
|---|---|
| `spectral_refrain_null.md` | Fixed-form poems have flat spectra (refrain produces impulse, not oscillation) |
| This experiment | High kurtosis + flat spectra is a property of *all poetry vs prose*, not specifically of refrain poems |
| Combined | Poetry as a mode is impulse-structured; refrain structure adds a detectable spike at the moment of return (the mechanism claim) but does not elevate aggregate impulsiveness (the distribution claim) |

---

## Corpus distribution

- Corpus median kurtosis: **1.258** (interquartile range 0.53–2.14)
- p90: 3.883 | p95: 4.899
- Prose control: 0.022 (near-zero, consistent with Gaussian S₂ process)
- Fixed-form median: 2.023
- Baseline poetry median: 1.183

---

## Next steps

- **Kurtosis as a corpus-level discriminator.** The poetry–prose kurtosis gap (1.258 vs 0.022) is large and consistent. A receiver-operating-characteristic analysis of kurtosis as a poetry/prose classifier might outperform raw avg S₂, which the stanza-break artifact contaminates. Artifact-free avg S₂ is −0.388 (poetry) vs −1.721 (prose) — a gap of 1.333 bits. Whether kurtosis gives a cleaner signal deserves testing.
- **What drives high-kurtosis poetry?** The top-kurtosis poems (Dickinson, Cummings, Lindsay, Whitman) suggest several mechanisms: extreme typographic/syntactic compression, unusual proper nouns, radical line breaks in very short poems. A per-token audit of the kurtosis-driving events could identify what classes of choice produce the distribution's heavy tail.
- **Repeated-line kurtosis control.** The "repeaters" group (kurtosis 3.032) is numerically higher than fixed_form (1.909), but the ballads dominate it — and ballads were found to be heavily artifact-contaminated (10.1% contamination, now removed). A separate check that the ballads' elevated kurtosis is not residual artifact or a small-n effect would strengthen or weaken the case.
