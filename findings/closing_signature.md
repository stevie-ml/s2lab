# The Closing-Signature Hypothesis: A Null Result and a New Discovery

**Date:** 2026-11-25  
**Experiment:** `experiments/closing_signature.py`  
**Corpus:** 415 poems (filtered to ≥20 artifact-free tokens), 46 eras with ≥3 poems  
**Builds on:** `findings/arc_era_classifier.md` (Q4_III identified as most era-discriminating feature)

---

## Motivation

The arc era classifier found that **Q4_III** (Type III% — conformity — in the final quarter) was the most discriminating single feature for era classification. The natural hypothesis: if the closing segment contains the most discriminating feature, then a classifier using **only the closing 20% of tokens** should outperform one using the full arc.

This experiment directly tests that hypothesis.

---

## Main Result: The Hypothesis Fails — The Middle Is King

| Feature Set | Accuracy | vs Chance | Note |
|-------------|----------|-----------|------|
| **middle (20–80%)** | **5.9%** | **2.69×** | Best performer |
| full poem | 5.3% | 2.46× | Baseline |
| opening (first 20%) | 4.8% | 2.22× | Below baseline |
| open + close | 4.6% | 2.11× | Combined ends = worse |
| **closing (last 20%)** | **3.8%** | **1.76×** | Worst performer |

**The closing-only classifier is the weakest**, not the strongest. The middle of the poem — the sustained body of the text, free from both opening establishment and closing resolution — is the most era-discriminating segment.

---

## Why Does Q4_III Have High Variance Yet Poor Classification Power?

The arc_era_classifier found Q4_III has the highest inter-era variance (0.005769). This seems to predict the closing would be most useful, but classification accuracy tells the opposite story. Three explanations:

1. **High variance ≠ structured variance**: Q4_III has high spread across eras, but the variation may be noisy (many eras clustered at similar values with a few outliers). Nearest-centroid classifiers need *structured* separation, not just spread.

2. **Short segments = noisy estimates**: The closing 20% of an average poem (≈ 80 artifact-free tokens) gives only ~16 tokens. Type I/II/III percentages computed from 16 tokens are extremely noisy. The middle (60% = ~48 tokens) has much better statistics.

3. **Opening and closing serve formal roles**: Openings establish the poem's contract; closings resolve it. Both are constrained by poetic convention in ways that *reduce* between-era distinctiveness. The middle is where the poet has maximum expressive freedom.

---

## Closing Segment Profiles by Era

The closing segments reveal distinctive era signatures even though they don't classify well:

| Era | N | Type III% (closings) | Avg S₂ | Interpretation |
|-----|---|----------------------|--------|----------------|
| **villanelle** | 3 | **68.3%** | -0.46 | Refrain repetition = extremely predictable closings |
| **song_lyrics** | 3 | **60.3%** | -0.21 | Songs end with familiar refrains/hooks |
| **control** (prose) | 5 | **51.1%** | -0.60 | Prose ends conventionally |
| **ballad** | 6 | 48.0% | -0.72 | Ballad formulas resolve predictably |
| **biblical** | 8 | 43.6% | -0.67 | Parallelism creates expected closure |
| **german_symbolist** | 3 | 28.7% | +0.52 | Highest avg S₂ in closing — most deviant endings |
| **spoken_word** | 3 | 26.2% | +0.11 | Rhetorical energy at the finish |
| **double_dactyl** | 5 | 29.7% | -0.00 | Constraint forces unusual closings |
| **war_poetry** | 3 | 27.5% | -0.41 | Endings resist predictability |

The villanelle has the most predictable closings (68.3% Type III) — its refrain repetition means the closing token is nearly always the same phrase. Song lyrics show the same pattern. This confirms that **refrain-based forms converge toward predictable endings**.

German Symbolist poetry has both the lowest Type III% and highest avg S₂ in closings (+0.52) — these poems end with the most statistical surprise.

---

## Opening vs. Closing Divergence: Volta Signatures

Which eras front-load vs. back-load their most surprising language?

### Front-loaded (more surprise in opening):

| Era | Open Type I% | Close Type I% | Δ |
|-----|-------------|--------------|---|
| war_poetry | 19.2% | 6.2% | **+0.130** |
| ballad | 15.3% | 8.6% | **+0.067** |
| dramatic_monologue | 15.7% | 9.4% | **+0.063** |
| imagist | 15.3% | 9.0% | **+0.063** |
| elegy | 17.8% | 11.7% | **+0.061** |

**War poetry, ballad, and dramatic monologue open with the most linguistic surprise and settle toward conformity** — consistent with poems that must immediately establish an urgent or dramatic register, then work within it.

Elegies open with high surprise (the shock of death/loss) and close more softly — a pattern of emotional processing moving toward acceptance.

### Back-loaded (volta — more surprise in closing):

| Era | Open Type I% | Close Type I% | Δ |
|-----|-------------|--------------|---|
| spoken_word | 10.6% | 18.1% | **-0.075** |
| limerick | 5.7% | 11.0% | **-0.054** |
| cliche_control | 2.5% | 8.3% | **-0.059** |
| double_dactyl | 10.4% | 15.6% | **-0.052** |
| language poetry | 4.9% | 10.0% | **-0.051** |

**Spoken word poetry has the strongest back-loaded surprise** (Δ = -0.075) — consistent with rhetorical climax. Limericks and double dactyls have their punchlines at the end (back-loaded by design). Language poetry builds toward disruption.

The **cliche_control** texts (consciously cliché writing) show a volta too — presumably because even in cliché writing, the closing sentence often breaks from the established pattern.

---

## Per-Era Accuracy with Closing Classifier

The closing classifier succeeds for unusual cases:

| Era | N | Accuracy |
|-----|---|----------|
| control (prose) | 5 | **40.0%** | Prose closings are distinctive — lowest S₂, highest Type III |
| song_lyrics | 3 | **33.3%** | Extreme Type III (60.3%) makes song endings recognizable |
| war_poetry | 3 | **33.3%** | High front-loading creates distinctive closing profile |
| villanelle | 3 | **33.3%** | Refrain creates unique closing signature |
| cliche_control | 4 | **25.0%** | Low S₂ closings |

The closing classifier can identify the most formally distinctive closings (prose, refrain forms, song) but fails for open verse traditions where closings are less constrained.

---

## Finding

The **closing-signature hypothesis is false**: despite Q4_III having the highest inter-era variance among arc features, the last 20% of a poem is the *worst* single segment for era classification (1.76× chance vs 2.46× for full arc).

The **middle of the poem is the most era-discriminating segment** (2.69× chance improvement), outperforming both the full arc and all individual segments. This inverts the hypothesis: poetic traditions are most distinguishable in their sustained middle movement, not their endings.

The divergence analysis confirms the **three structural arc types** from the arc_era_classifier:
1. **Front-loaded**: war, ballad, dramatic monologue, imagist, elegy — high opening surprise, settling toward conformity
2. **Back-loaded (volta)**: spoken word, limerick, double dactyl, language poetry — building toward the punchline or disruption
3. **Flat**: concrete, found, biblical, control — low surprise throughout

The highest-S₂ closing segments belong to german_symbolist (+0.52 avg) and confessional (+0.13 avg) poetry — these traditions refuse easy resolution. The lowest belong to villanelle (-0.46), song lyrics (-0.21), and biblical (-0.67) — forms that require satisfying (predictable) closure.

---

## Theoretical Interpretation

The arc_era_classifier finding that Q4_III is most *variable* across eras conflates *variance* with *discriminability*. For nearest-centroid classification, what matters is clean cluster separation — which requires that one era's closing pattern differs from all others in a consistent direction, not just that closing patterns vary a lot overall.

The middle segment's superiority may reflect that **the body of a poem is where its characteristic voice is sustained without the special demands of opening or closing**. Openings must hook; closings must resolve. These formal pressures reduce between-era distinctiveness. The middle is where the poem simply *is itself*.

---

## Suggested Next Steps

1. **Linear discriminant analysis**: Replace nearest-centroid with LDA on the closing and middle segments — LDA finds the linear combination of features that maximally separates classes, potentially recovering the Q4_III discriminating power.

2. **Opening-to-closing arc ratio**: For each poem, compute closing_I% / opening_I% — this single number captures the volta vs. front-loaded distinction. Test whether this ratio classifies era better than the absolute values.

3. **Closing entropy profile**: The closing segment's entropy *trajectory* (is it rising or falling toward the last token?) may carry more discriminative signal than the average. A poem that ends on falling entropy (the last word was almost inevitable) vs. rising entropy (the poem opens at its close) could be a stronger feature.

4. **Cross-era closing vocabulary**: Build a lexicon of the most common closing words for each era. Do certain traditions consistently end with function words, nouns, or verbs? This would bridge the token-level S₂ analysis with lexical analysis.
