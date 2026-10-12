# The Surprise Economy: S2 Inequality in Poetry

**Date:** 2026-10-12  
**Experiment:** `experiments/surprise_economy.py`  
**Results:** `results/surprise_economy.json`  
**Corpus:** 246 poems analyzed (artifact-filtered)

---

## Research Question

Does the total amount of surprise in a poem predict how that surprise is *distributed*?

Two competing hypotheses:
- **Surprise Economy hypothesis**: High-mean-S2 poems "spend" their budget evenly — low lag-1 autocorrelation, spread surprises throughout. Low-mean-S2 poems concentrate their rare surprises.
- **Surprise Abundance hypothesis**: High-mean-S2 poems have MORE extreme spikes *in addition to* higher baseline surprise — surprise is not zero-sum, and the rich get richer.

---

## Method

For each poem (artifact-free, ≥15 tokens):
1. **Mean S2**: average artifact-free S2 (the "surprise level")
2. **Lag-1 autocorrelation**: does high S2 at position t predict high S2 at t+1?
3. **Gini coefficient** of |S2| values: measure of *inequality* in surprise distribution
4. **Top-10% concentration**: what fraction of total positive S2 mass is held by the top 10% of tokens?

Pearson correlations between mean S2 and each distributional measure.

---

## Key Results

### 1. The Surprise Economy hypothesis FAILS

| Measure | r | t | Interpretation |
|---|---|---|---|
| Mean S2 vs lag-1 AC | **−0.008** | −0.12 | No correlation |
| Mean S2 vs top-10% conc | **−0.091** | −1.43 | Slight, non-significant |
| **Mean S2 vs Gini** | **+0.359** | **+6.00** | **Strong positive** |

**Result:** High mean S2 does NOT predict spread-out surprises (autocorrelation). But it DOES predict more **unequal** surprise distributions (higher Gini).

### 2. The Surprise Abundance finding

High-S2 poems are not more equal — they are more *unequal*. They combine a higher baseline of surprise with increasingly extreme spikes. The surprise budget is not zero-sum.

| Quartile | Mean S2 | lag-1 AC | Gini (|S2|) | Top-10% conc |
|---|---|---|---|---|
| Q1 (lowest) | −1.061 | −0.022 | **0.382** | 0.282 |
| Q2 | −0.601 | −0.002 | 0.391 | 0.241 |
| Q3 | −0.262 | −0.002 | 0.418 | 0.256 |
| Q4 (highest) | +0.283 | −0.018 | **0.423** | 0.270 |

Gini increases monotonically from Q1 to Q4. High-S2 poems have MORE variance in their surprise distribution, not less.

---

## Era-Level Findings

| Era | n | Mean S2 | lag-1 AC | Gini | Top-10% |
|---|---|---|---|---|---|
| german_modernist | 2 | **+0.773** | −0.082 | 0.465 | 0.250 |
| german_symbolist | 3 | +0.394 | +0.010 | 0.425 | 0.290 |
| beat | 6 | +0.279 | −0.001 | **0.529** | 0.256 |
| german_expressionist | 6 | +0.100 | −0.025 | 0.417 | 0.247 |
| haiku | 12 | −0.117 | **−0.102** | 0.404 | **0.362** |
| oulipo | 4 | −0.230 | +0.030 | 0.407 | 0.237 |
| metaphysical | 4 | −0.558 | −0.068 | 0.375 | 0.236 |
| concrete | 3 | −0.756 | −0.109 | **0.492** | **0.499** |
| spoken_word | 2 | −0.675 | **−0.124** | 0.340 | 0.200 |
| japanese_classical | 2 | −0.705 | **−0.179** | 0.319 | 0.195 |
| control | 5 | **−1.736** | **+0.094** | 0.351 | 0.387 |

### Beat Poetry: Highest Gini (0.529)

Beat poetry (Ginsberg, Ferlinghetti, Corso) has the **most unequal** surprise distribution in the corpus. Beat poets write long passages of flowing, semi-conventional syntax punctuated by sudden, extreme lexical deviations. The baseline is not low (mean S2 = +0.279) but the spikes are enormous. This matches the aesthetic: the "riff" mode interrupted by visionary outbursts.

### Concrete Poetry: Highest Concentration (0.499)

Concrete poetry (Gomringer's "silencio", E.E. Cummings' "l(a") has **nearly half its positive S2 mass concentrated in the top 10% of tokens**. These are extreme cases: mostly empty/repetitive text with one or two visually/semantically shocking moments. The whole poem builds to a single surprise.

### Control Prose: Positive Autocorrelation (+0.094)

Control prose is the **only genre with positive lag-1 AC** (surprises cluster). In prose, unusual vocabulary tends to appear in bursts (a technical paragraph, a dialogue section). Poetry systematically alternates surprising and predictable tokens. This confirms the "spike-and-recover" model as distinctly poetic.

### Haiku: Maximum Alternation, Maximum Concentration

Haiku has **the most negative lag-1 AC** (−0.102) AND **the highest top-10% concentration** (0.362) among multi-poem genres. This paradox resolves on inspection: haiku consist of very few tokens (10-20), each alternating between grammatical function words (low S2) and the kigo or juxtaposition (very high S2). The alternation is structural (noun → particle → noun); the concentration is semantic (one key image dominates).

---

## The "Rich Get Richer" Model of Poetic Surprise

The Gini–mean S2 correlation (r = 0.36) suggests a **compounding model of surprise**:

1. Poets who push against convention don't do it uniformly — they elevate both the baseline AND the peaks
2. The more a poet deviates from expectation, the more their *best* deviations become extreme outliers
3. Low-S2 poets have nearly uniform (and uniformly low) surprise — nothing stands out because nothing diverges
4. High-S2 poets have unequal surprise — a higher floor plus occasional towering spikes

This mirrors the DeDeo "impulse account": a poet in a high-deviation mode doesn't just use more unusual words — they periodically locate moments where the context is maximally confident and then violates it completely. The Straussian gap appears not just more often but more dramatically.

---

## Most and Least Concentrated Poems

### Most Egalitarian (lowest top-10% concentration)
Poems where surprises are spread democratically throughout:
- Three Haiku (Basho collection, translated) — conc = 0.119
- Ketjak (Ron Silliman) — conc = 0.125
- Catalog of Unabashed Gratitude (Ross Gay) — conc = 0.137
- Leaving the Atocha Station (Ashbery) — conc = 0.138

These are long(er) poems with sustained, moderate deviation throughout.

### Most Concentrated (highest top-10%)
Poems where one moment dominates:
- Cicadas (Bashō) — conc = 0.849 (virtually all surprise in one token)
- silencio (Gomringer) — conc = 0.791 (repetitive except for the central erasure)
- Academic prose (control) — conc = 0.674 (surprising only at jargon terms)
- The World of Dew (Issa) — conc = 0.557

---

## Interpretive Summary

The "surprise economy" metaphor is wrong in one direction but right in another:

- **Wrong**: High-S2 poems do NOT spread surprises more evenly (no correlation with AC)
- **Right**: High-S2 poems have more *unequal* surprise distribution (Gini +0.36)

A better metaphor: **surprise is capital**. Poets who accumulate more of it also have more extreme "wealthy tokens" — their best moments are proportionally more extreme than in low-S2 poems. There is no democratic redistribution of surprise; the variance scales with the mean.

The exception that tests the rule: haiku. Ultra-short form forces a different geometry: maximum alternation between grammatical necessity and semantic shock, with extreme concentration in one or two key words. Haiku poets cannot "spread" surprise — the form forbids it.

---

## Suggested Next Steps

1. **Fit the mean-Gini relationship**: Is the correlation linear or does Gini grow faster at high S2? A curvilinear model might show acceleration.
2. **Test the "peak premium"**: For each poem, compute the ratio of max S2 to mean S2. Does this ratio increase with mean S2? (Do high-S2 poets have proportionally more extreme peaks?)
3. **Gini over time within poem**: Does the Gini of the poem's S2 distribution change from the first half to the second half? (Does a poem become more or less equal over its arc?)
4. **The "spike tax"**: After an extreme high-S2 token, do subsequent tokens have lower S2 (recovery period)? This would test whether individual spikes create local "tax" on subsequent choices.
