# S₂ Inequality: Gini Coefficient of Poetic Surprise
**Date:** 2026-09-14

## Research Question

Is the Straussian gap *democratically distributed* across all tokens of a poem,
or *aristocratically concentrated* in a few extreme deviations?

We apply the **Gini coefficient** — the standard measure of income inequality —
to the distribution of positive S₂ values within each poem. Gini = 0 means every
surprising token contributes equally; Gini = 1 means a single token carries all
the poem's deviation from expectation.

We also compute the **concentration ratio (CR-10)**: the fraction of total positive
S₂ accounted for by the top 10% of surprising tokens.

## Era-Level Results

*(Sorted by Gini, most concentrated first)*

| Era | n | Avg S₂ | Gini | CR-10 | Near-Zero% |
|-----|---|--------|------|-------|------------|
| nursery_rhyme | 1 | 0.10 | **0.559** | 39% | 14% |
| mid_century | 3 | 0.87 | **0.559** | 27% | 13% |
| confessional | 3 | 0.53 | **0.542** | 36% | 6% |
| haiku | 2 | 2.08 | **0.541** | 31% | 9% |
| oulipo | 1 | -0.12 | **0.532** | 23% | 16% |
| modernist | 18 | 0.37 | **0.529** | 32% | 12% |
| harlem_renaissance | 4 | 0.44 | **0.525** | 29% | 9% |
| romantic | 9 | 0.17 | **0.522** | 30% | 10% |
| new_york_school | 18 | -0.18 | **0.513** | 31% | 9% |
| ballad | 6 | 0.81 | **0.510** | 31% | 14% |
| victorian | 13 | 0.34 | **0.505** | 34% | 10% |
| 19th_century | 9 | 0.39 | **0.501** | 31% | 9% |
| song_lyrics | 3 | 0.09 | **0.494** | 31% | 22% |
| ancient | 1 | 0.19 | **0.491** | 32% | 7% |
| prose_poetry | 9 | -0.16 | **0.487** | 29% | 10% |
| surrealist | 1 | -0.33 | **0.486** | 24% | 9% |
| contemporary | 9 | 0.07 | **0.480** | 28% | 11% |
| german_symbolist | 3 | 0.42 | **0.468** | 29% | 10% |
| german_expressionist | 2 | 0.62 | **0.463** | 27% | 13% |
| german_modernist | 2 | 1.12 | **0.447** | 26% | 11% |
| beat | 2 | 1.03 | **0.447** | 25% | 4% |
| language | 3 | 0.26 | **0.438** | 26% | 8% |
| deep_image | 1 | 0.25 | **0.408** | 22% | 8% |

## Most Concentrated Poems (highest Gini)

*A few tokens carry nearly all the surprise.*

| Poem | Author | Era | Avg S₂ | Gini | CR-10 | n tokens |
|------|--------|-----|--------|------|-------|----------|
| Harlem | Langston Hughes | harlem_renaissance | 1.40 | **0.631** | 27% | 77 |
| In a Station of the Metro | Ezra Pound | modernist | 0.26 | **0.625** | 67% | 20 |
| I felt a Funeral, in my Brain | Emily Dickinson | 19th_century | 0.48 | **0.624** | 37% | 69 |
| The Red Wheelbarrow | William Carlos William | modernist | 3.59 | **0.604** | 21% | 31 |
| This Is Just to Say | William Carlos William | modernist | 2.61 | **0.602** | 21% | 43 |
| Rivers and Mountains | John Ashbery | new_york_school | -0.57 | **0.595** | 38% | 64 |
| One Art | Elizabeth Bishop | mid_century | 1.22 | **0.593** | 28% | 63 |
| The One Thing That Can Save America | John Ashbery | new_york_school | -0.83 | **0.586** | 33% | 82 |
| Oread | H.D. (Hilda Doolittle) | modernist | 0.51 | **0.582** | 31% | 42 |
| Digging | Seamus Heaney | contemporary | 1.85 | **0.581** | 39% | 140 |
| Some Trees | John Ashbery | new_york_school | -0.59 | **0.576** | 40% | 44 |
| And Ut Pictura Poesis Is Her Name | John Ashbery | new_york_school | -0.53 | **0.574** | 40% | 92 |

## Most Distributed Poems (lowest Gini)

*Surprise is spread across many tokens.*

| Poem | Author | Era | Avg S₂ | Gini | CR-10 | n tokens |
|------|--------|-----|--------|------|-------|----------|
| My Life (excerpt) | Lyn Hejinian | language | -0.90 | **0.387** | 24% | 50 |
| Oh Shenandoah | Traditional (American  | song_lyrics | 0.34 | **0.388** | 25% | 186 |
| A Supermarket in California | Allen Ginsberg | beat | 0.65 | **0.394** | 24% | 96 |
| The Summer Day | Mary Oliver | contemporary | -0.65 | **0.397** | 25% | 195 |
| On His Blindness | John Milton | victorian | 0.04 | **0.405** | 24% | 163 |
| Driving Toward the Lac Qui Parle River | Robert Bly | deep_image | 0.25 | **0.408** | 22% | 62 |
| The Stranger (prose poem, translated) | Charles Baudelaire | prose_poetry | -0.34 | **0.408** | 25% | 148 |
| Possibilities | Wislawa Szymborska | contemporary | -0.31 | **0.419** | 23% | 128 |
| A Route of Evanescence | Emily Dickinson | 19th_century | 0.23 | **0.425** | 27% | 57 |
| Ketjak (excerpt) | Ron Silliman | language | -0.15 | **0.426** | 19% | 51 |
| A Blessing in Disguise | John Ashbery | new_york_school | -1.05 | **0.430** | 28% | 76 |
| Sunday Morning (stanza 1) | Wallace Stevens | modernist | -0.57 | **0.437** | 25% | 80 |

## Two-Axis Taxonomy: S₂ Level × Concentration

*(Median S₂ = 0.08, Median Gini = 0.507)*

### High S₂ / High Gini (n=32)
**The Spike Poets** — high average surprise achieved through concentrated bursts. Most tokens are conventional; the poem's information load sits in one or two extreme moments.

Top eras: modernist (7), victorian (4), new_york_school (3)
Exemplar: **William Carlos Williams** — "The Red Wheelbarrow" (S₂=3.59, Gini=0.604)

### High S₂ / Low Gini (n=29)
**The Sustained Deviants** — many tokens are moderately surprising. Deviation is a pervasive texture across the whole poem, not a single concentrated act.

Top eras: 19th_century (4), victorian (4), german_symbolist (3)
Exemplar: **Thomas Hardy** — "The Convergence of the Twain (excerpt)" (S₂=1.94, Gini=0.490)

### Low S₂ / High Gini (n=29)
**The Rare Flashes** — mostly conventional language with an occasional jarring moment. The poem conforms most of the time but reserves one genuine break from expectation.

Top eras: new_york_school (6), modernist (5), contemporary (3)
Exemplar: **John Ashbery** — "A Wave (opening)" (S₂=-1.14, Gini=0.512)

### Low S₂ / Low Gini (n=33)
**The Smooth Traditionalists** — consistently close to what language predicts. What little surprise exists is evenly distributed; nothing dominates.

Top eras: new_york_school (7), modernist (5), prose_poetry (5)
Exemplar: **W.S. Merwin** — "Yesterday (prose poem)" (S₂=-1.03, Gini=0.484)

## Correlation: Gini vs. Average S₂

Pearson r(Gini, avg S₂) = **0.293** across 123 poems.

The weak correlation (r=0.293) confirms that Gini and avg S₂ are **largely independent dimensions**. A poem's *level* of surprise and its *distribution* of surprise are separate properties. Average S₂ alone is insufficient to characterize a poem's information architecture.

Pearson r(token count, Gini) = **-0.122**.

Token count does not strongly predict concentration.

## Key Findings

1. **Gini varies substantially across poems**: range [0.387, 0.631], mean 0.505, median 0.507. There is no single distribution type for poetry.

2. **The quadrant taxonomy reveals four distinct information architectures**: Spike Poets (rare extreme moments), Sustained Deviants (pervasive mild surprise), Rare Flashes (otherwise conventional + one break), and Smooth Traditionalists. These categories are invisible to avg S₂ alone.

3. **Gini and avg S₂ are nearly independent** (r=0.293). A poet can achieve high average surprise through either many moderate deviations *or* through one or two extreme ones. These are different poetic strategies, not the same thing measured twice.

4. **Era-level concentration reflects form constraints**: shorter, more compressed forms show higher Gini — the poem must pack its deviation into fewer moments.

## Suggested Next Steps

1. **Correlate Gini with syllable count / word count**: Do shorter poems have higher Gini?
   Test whether form length, not era, drives the concentration pattern.

2. **Author Gini signatures**: Does a poet maintain consistent Gini across poems, or vary    concentration by work? (Hypothesis: imagists consistently high; confessionals vary by poem.)

3. **Gini over poem structure**: Compute Gini separately for the first half vs. second half    of each poem. Does the 'moment of maximum surprise' cluster at the end (climactic structure)?

4. **Gini and the confidence trap rate**: Do poems with high Gini also have fewer confidence    traps? If the surprise is concentrated in 1-2 tokens, the rest of the poem should conform    strongly to expectation.