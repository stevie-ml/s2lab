# Career S₂ Trajectory: How Individual Poets' Information Signatures Evolve

**Date:** 2026-10-05  
**Experiment:** `experiments/career_trajectory.py`  
**Corpus:** 209 texts; 14 poets qualifying (≥3 English poems, career span ≥5 years)  
**Builds on:** `temporal_evolution_s2.md`, `poet_s2_fingerprints.md`, `poet_suppression_profiles.md`

---

## Research Question

`temporal_evolution_s2.md` mapped S₂ across literary history by grouping poets into eras. But does a poet's own information signature shift *within* their career? Do poets become more or less willing to surprise readers as they mature?

This is a fundamentally different question: intra-career trajectory vs inter-generational drift.

---

## Method

For each author with ≥3 English-language poems spanning ≥5 years in the corpus:

1. Compute per-poem artifact-free (p_newline < 0.9) S₂ metrics: avg_s2, pos_s2_ratio, high_s2_ratio (>2 bits), std_s2
2. Normalize year within career to 0→1 (earliest poem = 0, latest = 1)
3. Fit OLS slope for each metric vs normalized time
4. Compute Pearson r for confidence

**Corpus note:** Langston Hughes' "Harlem" and "A Dream Deferred" are duplicate entries for the same poem; the r=−1.00 for Hughes reflects this inflation and should be interpreted cautiously.

---

## Main Results: Per-Author avg_S₂ Trajectory

| Author | Poems | Span | Slope | r | Early avg_S₂ → Late avg_S₂ |
|--------|-------|------|-------|---|---------------------------|
| Walt Whitman | 4 | 13y | **−0.992** | −0.73 | +0.77 → +0.03 ↓ |
| Matsuo Bashō | 4 | 9y | **−0.691** | −0.37 | +0.11 → −0.95 ↓ |
| E.E. Cummings | 3 | 38y | **−0.595** | −0.40 | −0.87 → −1.51 ↓ |
| Langston Hughes† | 3 | 30y | −0.535 | −1.00† | −0.35 → −0.88 ↓ |
| Emily Dickinson | 4 | 35y | +0.521 | +0.47 | −0.89 → +0.14 ↑ |
| John Ashbery | 16 | 28y | +0.370 | +0.27 | −1.21 → −1.39 ↑ (weak) |
| T.S. Eliot | 3 | 10y | +0.355 | +0.99 | −0.48 → −0.11 ↑ |
| Lucille Clifton | 3 | 20y | +0.334 | +0.97 | −0.81 → −0.49 ↑ |
| Anonymous (Hebrew Bible) | 7 | 413y | +0.245 | +0.66 | −0.62 → −0.20 ↑ |
| Thomas Hardy | 3 | 17y | +0.071 | +0.19 | +0.17 → +0.10 ≈ |
| Wallace Stevens | 3 | 7y | −0.026 | −0.02 | −0.80 → −0.92 ≈ |

†Hughes' r=−1.00 is an artifact of the corpus containing two identically-worded entries for "Harlem (A Dream Deferred)."

**Aggregate: 9/14 poets show rising S₂ over their careers; 5 show falling.**  
Mean slope: +0.0017 (effectively zero). There is **no universal trend** — poets split roughly 2:1 toward increasing surprisal, but the variance is high (SD = 0.50).

---

## Key Finding 1: Walt Whitman's Convergence to Expectation

Whitman shows the **sharpest falling trajectory** (slope = −0.992, r = −0.73):

| Year | avg_S₂ | pos% | Title |
|------|--------|------|-------|
| 1855 | **+0.775** | 51% | Song of Myself (section 1) |
| 1865 | +0.039 | 38% | When I Heard the Learn'd Astronomer |
| 1865 | −0.686 | 34% | O Captain! My Captain! |
| 1868 | +0.029 | 44% | A Noiseless Patient Spider |

"Song of Myself" (1855) is his most semantically wild — nearly 3/4 of a bit above all later work. By 1865–1868, his avg_S₂ has converged to near zero. "O Captain!" — his most consciously conventional, popular elegy — is his *most conformist* poem by S₂.

**Literary resonance:** This matches the known critical narrative. The 1855 *Leaves of Grass* was genuinely unprecedented in its cataloging, free rhythms, and semantic leaps. Later Whitman writing occasional verse ("O Captain!") adopted a more formal, audience-accessible style.

---

## Key Finding 2: Cummings' Typographic Paradox

E.E. Cummings' trajectory runs counter to expectation:

| Year | avg_S₂ | pos% | std_S₂ | Title |
|------|--------|------|--------|-------|
| 1920 | −0.870 | 16% | 4.001 | Buffalo Bill 's |
| 1940 | −0.016 | 42% | 4.446 | anyone lived in a pretty how town |
| 1958 | **−1.507** | 20% | 4.661 | l(a |

His most radical typographic experiment — "l(a" (1958), which fragments "la / leaf falls / loneliness" into single letters and syllables — has the **lowest avg_S₂** of his three poems. Despite being visually extreme, the fragmentary structure gives GPT-2 short, high-entropy windows where the specific letter or syllable matters less: the model is maximally uncertain AND the poet's choices happen in a low-information field.

**Interpretation:** Typographic disruption ≠ semantic surprise. S₂ is fundamentally a *semantic* measure (confirming `semantic_vs_structural_surprise.md`). When Cummings breaks language into atoms, he creates local uncertainty without large Straussian gaps, because there's nothing coherent enough to "expect."

By contrast, "anyone lived in a pretty how town" (1940) has avg_S₂ near zero and 42% positive-S₂ — his poem with the most conventionally readable syntax (despite scrambled meaning) is the one where deviation is measured against clear expectations.

---

## Key Finding 3: T.S. Eliot's Rising Trajectory (Strong r)

| Year | avg_S₂ | pos% | Title |
|------|--------|------|-------|
| 1915 | −0.48 | 38% | The Love Song of J. Alfred Prufrock |
| 1922 | −0.24 | 43% | The Waste Land (opening) |
| 1925 | −0.11 | 44% | The Hollow Men |

Slope = +0.355, r = **+0.99** — a near-perfect linear rise. This is remarkable for only three poems but aligns with the literary understanding: Prufrock, despite its famous strangeness, uses complete sentences and coherent syntax; The Waste Land is more fragmented; The Hollow Men is more repetitive and incantatory, with its famous "This is the way the world ends" refrain — the incantatory mode creates expectation + deviation cycles that register as higher S₂.

---

## Key Finding 4: Ashbery's Weak but Notable Late-Career Decline in Peaks

Ashbery shows a weak upward slope in avg_S₂ (r = 0.27) but a more meaningful **decline in high_s2_ratio** (r = −0.33):

| Period | high_s2_ratio | avg_S₂ |
|--------|---------------|--------|
| 1956–1962 (early) | 22–29% | −0.38 to −1.26 |
| 1975 (Self-Portrait) | 20–27% | −0.26 to −0.46 |
| 1984 (A Wave) | **9%** | −1.39 |

"A Wave" (1984) — widely considered a late-career masterwork — has the lowest proportion of high-S₂ tokens of any Ashbery poem. The poem's prose-like meditative style creates fewer sharp surprises, replaced by sustained, even flow of information. This is consistent with the "long poem as sustained entropy" hypothesis.

---

## Aggregate Pattern

| Direction | n | Notes |
|-----------|---|-------|
| Rising S₂ | 9 | Dickinson, Eliot, Clifton, Ashbery (weak), Biblical tradition... |
| Falling S₂ | 5 | Whitman, Bashō, Cummings, Hughes, Stevens |

No clear null hypothesis is violated: both directions are well-represented. The variation WITHIN any one poet's career (SD of individual slopes = 0.50) swamps the tiny mean (+0.0017).

**Key implication:** S₂ trajectory is *poet-specific*, not developmental-universal. There is no "maturing toward surprise" or "maturing toward convention" as a general tendency. The direction of change likely reflects each poet's specific formal evolution.

---

## Limitations

1. Small n for most authors (3–4 poems). Slopes are indicative, not inferentially robust.
2. Corpus selection is non-random; the poems chosen may not represent a poet's full range.
3. The "found text" trajectory (1900→2010) is not a real career — different sources, same label.
4. Duplicate entry for Hughes contaminates that slope.

---

## Suggested Next Steps

1. **Expand Ashbery corpus** — he's the one case with enough poems (16) to run a proper regression. Track his metrics decade by decade.
2. **Test with poets who wrote in quantifiably different "phases"** — e.g., early/late Yeats, where the shift from Celtic Twilight to modernism is documented.
3. **Micro-analysis of Whitman 1855 vs 1865**: What specific token choices drove his loss of 0.8 bits of avg_S₂? Is it the shift from catalogs (which were semantically wild) to lyric voice?
4. **The "typographic paradox" for other visual poets**: Does concrete poetry generally show low S₂ despite radical visual form?
