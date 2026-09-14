# S2 Distribution Shape as a Poetic Signature

**Date:** 2026-09-14  
**Research Question:** Beyond mean S2, do the *shape* of S2 distributions reveal distinct aesthetic strategies? Can we classify poets as "Snipers" (rare extreme surprises) vs. "Spreaders" (many moderate surprises)?

---

## Motivation

All prior analyses used mean or median S2 to compare poets and genres. But the same mean can arise from very different distributions:

- **Sniper**: low spike rate (≤15%), but when the poet fires, S2 is extreme (kurtosis ≫ 0)  
- **Spreader**: high spike rate (≥30%), moderate intensity, near-normal kurtosis  

These correspond to distinct aesthetic philosophies: *concentrated defamiliarization* vs. *sustained estrangement*.

---

## Methodology

For each poem (n = 125), computed:
- **Mean S2**, **Std S2** — central tendency and spread
- **Skewness** — directionality (all poems are right-skewed; the question is by how much)
- **Excess kurtosis** — tailedness; high kurtosis = rare extreme events dominate the distribution
- **Spike rate** — fraction of tokens with S2 > 2 nats
- **Spike concentration** — fraction of total positive S2 carried by the top 10% of tokens (by S2 value)
- **Dynamic range** — 95th minus 5th percentile of S2

---

## Key Finding 1: Spike Rate, Not Spike Intensity, Drives Mean S2

| Correlation | r |
|---|---|
| Mean S2 ↔ Spike Rate | **+0.789** |
| Mean S2 ↔ Kurtosis | -0.075 |
| Mean S2 ↔ Concentration | -0.350 |
| Kurtosis ↔ Spike Rate | -0.199 |
| Kurtosis ↔ Concentration | +0.383 |

The dominant driver of a poem's average surprisingness is **how often** the poet chooses surprising words (spike rate), not how extreme those surprises are (kurtosis). Mean S2 and spike rate correlate at r = 0.789 — the strongest relationship in the dataset.

**Implication**: "Sniper" poets are not necessarily more surprising overall. The Spreader strategy — consistent moderate deviation — is informationally more efficient. It's cheaper (in terms of linguistic extremity) to be continuously unusual than to alternate between boring and shocking.

---

## Key Finding 2: Author Profiles by Kurtosis

| Author | n | Mean S2 | Kurtosis | Spike Rate | Concentration |
|---|---|---|---|---|---|
| Traditional (Scottish ballad) | 5 | +0.756 | **6.38** | 0.229 | 0.692 |
| William Blake | 2 | +0.920 | **6.30** | 0.237 | 0.740 |
| William Shakespeare | 3 | -0.618 | **6.25** | 0.172 | 0.690 |
| John Ashbery | 16 | -0.284 | **6.10** | 0.212 | 0.644 |
| E.E. Cummings | 2 | +0.420 | **5.54** | 0.232 | 0.713 |
| Thomas Hardy | 3 | +1.509 | 5.52 | 0.328 | 0.596 |
| Rainer Maria Rilke | 2 | +1.121 | 1.54 | 0.326 | 0.475 |
| Georg Trakl | 2 | +0.625 | 1.08 | 0.282 | 0.505 |
| Allen Ginsberg | 2 | +1.031 | 1.79 | 0.328 | 0.477 |
| Walt Whitman | 2 | +0.760 | 2.43 | 0.300 | 0.543 |
| Control (prose) | 5 | -1.663 | 0.37 | 0.082 | 0.784 |

**Ballads and Blake are the most leptokurtic poets.** Their spare, repetitive structures create a predictable backdrop against which sudden narrative turns (a murder reveal in a ballad; "fearful symmetry" in Blake) strike with maximum force.

**Ashbery has the highest kurtosis among 20th century poets** — remarkable given his negative mean S2. He most often follows expectation, but when he departs, he departs *violently*. This matches his aesthetic: surfaces of ordinary language punctured by eruptions of radical dislocation.

**Rilke, Trakl, Ginsberg, and Whitman are Spreaders** — their long, expansive lines generate consistent surprise over time, rather than concentrating it in moments.

---

## Key Finding 3: The Snipers and Spreaders

### Pure Snipers (kurtosis > 8, spike rate < 20%)

| Poem | Author | Kurtosis | Spike Rate | Concentration |
|---|---|---|---|---|
| "From 'Who Whispered Near Me'" | Killarney Clary | 23.0 | 0.15 | 0.71 |
| "And Ut Pictura Poesis Is Her Name" | John Ashbery | 16.6 | 0.16 | 0.71 |
| "Frankie and Johnny" | Traditional (American folk) | 16.6 | 0.13 | 0.83 |
| "Lord Randal" | Traditional (Scottish ballad) | 11.5 | 0.16 | 0.81 |
| "The Congo" | Vachel Lindsay | 9.5 | 0.15 | 0.83 |
| "Edward, Edward" | Traditional (Scottish ballad) | 9.1 | 0.17 | — |

Folk ballads dominate the Sniper category. Their formulaic dialogue and refrain structure keeps entropy high (the model becomes unsure of what comes next) while the narrative information is tightly concentrated in the revelation moments (who killed my father? who will care for my children?).

### Pure Spreaders (kurtosis < 1, spike rate > 25%)

| Poem | Author | Kurtosis | Spike Rate |
|---|---|---|---|
| "A Supermarket in California" | Allen Ginsberg | 0.11 | 0.32 |
| "Die erste Elegie" | Rainer Maria Rilke | 0.49 | 0.37 |
| "Driving Toward the Lac Qui Parle River" | Robert Bly | 0.40 | 0.31 |
| "A Noiseless Patient Spider" | Walt Whitman | 0.73 | 0.27 |
| "Grodek" | Georg Trakl | 1.01 | 0.30 |

These are cataloguing, expansive poems. Ginsberg's California supermarket is a long walk through unexpected images, each moderately surprising; Rilke's elegy sustains elevated strangeness through long syntactic arcs.

---

## Key Finding 4: Ashbery's Bimodal Persona

Ashbery (n=16) has *both* the highest mean kurtosis among 20th century poets (6.10) *and* multiple poems in the Spreader category ("Soonest Mended," "The Painter"). He operates across the entire spectrum — the same poet produces concentrated-shock and sustained-estrangement poems. His overall kurtosis is high because his distribution across poems is itself wide.

---

## Key Finding 5: Prose Is Platykurtic

Control prose has kurtosis of 0.37 — near-normal. Even when prose makes a surprising word choice, it doesn't diverge as wildly as poetry. The "fat tails" of extreme S2 values are a poetic, not a linguistic, phenomenon.

---

## Data Table: Style Classification Summary

| Style | Count | Description |
|---|---|---|
| Balanced | 64 | Moderate kurtosis, mixed spike rate |
| Conformist | 30 | Mean S2 < 0; follows statistical expectation |
| Concentrated | 25 | Top 10% of tokens carry >60% of positive S2 |
| Sniper | 6 | High kurtosis (>3) + low spike rate (<15%) |

---

## Implications

1. **Kurtosis as a formalism marker**: Highly formal or repetitive structures (ballads, villanelles) may systematically produce high kurtosis, because the repetitive frame amplifies the deviation of non-repeated elements.

2. **The Spreader advantage**: Since spike rate predicts mean S2 far better than kurtosis does (r = 0.789 vs. r = -0.075), poets who sustain surprise across the entire poem achieve higher overall information density than those who save it all for one moment. This may explain why prose poems and free verse (Ginsberg, Whitman, Rilke) often score high on S2 despite lacking rhyme/meter to generate conventional "surprise."

3. **Ashbery as chameleon**: His range across the Sniper-Spreader axis is itself a form. Perhaps this taxonomic flexibility is part of what makes him the corpus's most studied New York School poet.

---

## Next Steps

- Investigate whether kurtosis correlates with poem length (shorter poems may be forced into Sniper mode)  
- Test whether formal meter (iambic pentameter) constrains the kurtosis-spike rate tradeoff  
- Examine whether a poet's kurtosis is consistent across their work, or varies by subject matter  
- Look at per-stanza kurtosis to see whether poems have "Sniper stanzas" followed by "Spreader stanzas"
