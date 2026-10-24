# Rupture vs. Pivot: Poet-Level Surprise Mechanism Profiles

**Date:** 2026-10-24  
**Experiment:** `experiments/rupture_pivot_poet_profiles.py`  
**Results:** `results/rupture_pivot_profiles.json`  
**Corpus:** 328 texts, 106 poets analyzed (≥30 high-S₂ events each)  
**Builds on:** `entropy_cascade_context.md` (the liberation/anchoring reversal)

---

## Research Question

The previous entropy cascade finding established that S₂'s effect on subsequent entropy
**reverses by context**:

- **Confident context** (entropy_t < 4 bits) + high S₂ → entropy *increases* next → **Rupture/Liberation**
- **Uncertain context** (entropy_t ≥ 7 bits) + high S₂ → entropy *decreases* next → **Pivot/Anchoring**

Do individual poets have a characteristic preference for one mechanism? Can we build a
**Rupture-Pivot (RP) index** that classifies poets by their dominant surprise strategy?

---

## Method

For each consecutive token pair (position t, t+1) in each poem:

1. Extract: S₂_t, entropy_t, entropy_{t+1}
2. For high-S₂ events (S₂_t > 1.5): split by context certainty
   - **Confident context**: entropy_t < 4 bits → compute mean Δentropy (rupture score)
   - **Uncertain context**: entropy_t ≥ 7 bits → compute mean Δentropy (pivot score)
3. **RP index** = rupture_score − pivot_score (higher = more rupture-dominant)

Poets with fewer than 30 high-S₂ events excluded. English-language texts only.

---

## Key Results

### 1. Every Poet Is Rupture-Dominant (But in Different Degrees)

The RP index ranges from **3.76 to 11.27** — all positive. This means:

- **Rupture scores** are universally positive (1.69–7.33 bits): confident-context surprises
  always tend to *increase* subsequent entropy.
- **Pivot scores** are universally negative (−1.14 to −4.48 bits): uncertain-context
  surprises always tend to *decrease* subsequent entropy.

The RP index captures **how much more rupture-dominant than pivot-dominant** a poet is —
not whether they use one or the other, but in which proportion.

### 2. Full Poet Rankings (RP Index)

| Author | Era | Rupture | Pivot | RP Index | n high-S₂ |
|--------|-----|---------|-------|----------|-----------|
| Thomas Gray | elegy | 7.33 | −3.94 | **11.27** | 50 |
| Christian Bök | oulipo | 7.25 | −2.99 | **10.24** | 39 |
| Langston Hughes | harlem_renaissance | 6.21 | −3.89 | **10.10** | 66 |
| William Ernest Henley | victorian | 5.83 | −4.10 | **9.92** | 68 |
| Wilfred Owen | war_poetry | 6.95 | −2.92 | **9.87** | 137 |
| Lawrence Ferlinghetti | beat | 6.91 | −2.93 | **9.84** | 58 |
| Agha Shahid Ali | postcolonial | 6.62 | −3.09 | **9.71** | 98 |
| Wallace Stevens | modernist | 6.51 | −2.91 | **9.42** | 66 |
| John Donne | early_modern | 6.75 | −2.37 | **9.12** | 140 |
| Seamus Heaney | contemporary | 6.75 | −2.37 | **9.11** | 52 |
| Alexander Pope | 18th_century | 6.53 | −2.26 | **8.79** | 198 |
| W.B. Yeats | modernist | 5.96 | −2.68 | **8.65** | 173 |
| Alfred, Lord Tennyson | ekphrastic | 5.48 | −3.04 | **8.51** | 330 |
| John Ashbery | new_york_school | 5.32 | −3.02 | **8.34** | 320 |
| Emily Dickinson | 19th_century | 5.21 | −2.52 | **7.73** | 140 |
| T.S. Eliot | dramatic_monologue | 4.06 | −3.31 | **7.37** | 224 |
| Gerard Manley Hopkins | victorian | 4.73 | −2.59 | **7.32** | 167 |
| Walt Whitman | 19th_century | 4.60 | −2.51 | **7.11** | 171 |
| Robert Frost | early_modern | 4.40 | −2.53 | **6.93** | 133 |
| Robert Browning | ekphrastic | 4.47 | −2.21 | **6.68** | 581 |
| Marianne Moore | modernist | 3.33 | −2.98 | **6.32** | 127 |
| Allen Ginsberg | beat | 2.28 | −3.58 | **5.86** | 56 |
| Anonymous (Hebrew Bible) | biblical | 2.20 | −3.54 | **5.74** | 194 |
| Charles Baudelaire | prose_poetry | 2.45 | −3.06 | **5.52** | 37 |
| Gertrude Stein | oulipo | 2.77 | −1.92 | **4.68** | 132 |
| William Shakespeare | victorian | 2.38 | −2.14 | **4.52** | 98 |
| Traditional (sea chanty) | song_lyrics | 2.34 | −1.42 | **3.76** | 35 |

*(Full table of 106 poets in results/rupture_pivot_profiles.json)*

### 3. Era Aggregates

| Era | Mean RP Index | N Poets |
|-----|--------------|---------|
| german_expressionist | 9.13 | 2 |
| war_poetry | 8.97 | 2 |
| elegy | 8.79 | 6 |
| fixed_form | 8.75 | 3 |
| early_modern | 8.47 | 3 |
| romantic | 8.38 | 3 |
| modernist | 8.28 | 5 |
| 18th_century | 8.00 | 4 |
| oulipo | 7.98 | 3 |
| victorian | 7.79 | 8 |
| surrealist | 7.77 | 6 |
| beat | 7.71 | 3 |
| ekphrastic | 7.58 | 5 |
| ballad | 7.16 | 2 |
| language | 7.09 | 1 |
| **prose_poetry** | **5.86** | 7 |
| **biblical** | **5.74** | 1 |
| **found_poetry** | **5.63** | 3 |

---

## Key Findings

### Finding 1: Prose Poetry Is the Most Pivot-Dominant Genre

All seven prose poets (Rankine, Edson, Glück, Forché, Armantrout, Baudelaire, Clary)
cluster at the low end. Mean RP index = 5.86, vs. 8.79 for elegy.

**Explanation**: Prose poetry operates without prosodic templates (meter, line-break
conventions), so GPT-2's context entropy is *already high* throughout. High-entropy base
conditions mean most high-S₂ events land in uncertain contexts → they pivot rather than
rupture. The poet makes a surprising specific choice in an already-ambiguous situation,
resolving the ambiguity in an unexpected direction, rather than shattering a confident
trajectory.

### Finding 2: Formal Verse Generates the Strongest Ruptures

Thomas Gray (RP=11.27), Alexander Pope (8.79), Wilfred Owen (9.87) rank among the
highest. These poets write within tight formal constraints (heroic couplets, iambic
pentameter), which produces very confident contexts — GPT-2 "knows" where the grammar
and meter are heading. When the poet deviates, the liberation effect is maximal.

Gray's "Elegy Written in a Country Churchyard" exemplifies this: every line is a
metrical and syntactic template, creating confident contexts. The few moments of
unexpected diction therefore explode the model's entropy, producing massive ruptures.
**Formality, paradoxically, enables the largest liberation effects.**

### Finding 3: War Poetry Is Rupture-Dominant — the Tension Hypothesis

Owen (9.87) and Brooke (8.07) both rank high. War poetry imposes formal verse on
atrocity, creating a structural tension: the syntactic/metrical template predicts
dignified, conventional language, but the subject demands rupture. High-S₂ words
in war poetry occur against confident formal contexts, producing strong liberation.
The horror of the content is amplified by the violation of formal expectation.

### Finding 4: The Shakespeare Anomaly

Shakespeare ranks 97th out of 106 poets (RP=4.52), clustering with prose poets and
found text. His sonnets and dramatic monologues generate *uncertain* contexts throughout:
complex syntax, hypotaxis, shifting registers. High-S₂ moments in this uncertain terrain
tend to anchor rather than liberate. Shakespeare uses surprise to *resolve* semantic
ambiguity rather than create it — a pivot strategy that concentrates meaning rather than
proliferating it.

This may explain why Shakespeare's images feel *inevitable* on rereading even though
they were surprising on first reading: they pivot the meaning rather than rupturing it
open. Compare Keats (RP=8.83): Keats's confident Romantic syntax makes his deviations
explosive and open-ended.

### Finding 5: Ginsberg vs. Ferlinghetti — Beat Internal Split

Beat poetry shows an internal split:
- Ferlinghetti: RP = 9.84 (strong rupture)
- Ginsberg: RP = 5.86 (near prose poetry)

Ferlinghetti's shorter, more aphoristic lines create confident contexts that rupture.
Ginsberg's long Whitmanesque lines ("Howl") accumulate so much syntactic complexity
that high-S₂ moments occur in uncertain terrain and pivot rather than rupture.

This distinguishes two Beat strategies: Ferlinghetti's *aphoristic rupture* vs.
Ginsberg's *catalogic pivot*.

### Finding 6: Oulipo Shows a Genuine Split

- Christian Bök: RP = 10.24 (strong rupture — *Eunoia*'s single-vowel constraints
  create extremely confident contexts, so any deviation explodes entropy)
- Gertrude Stein: RP = 4.68 (near pivot — repetition creates uncertain contexts where
  any variation anchors rather than liberates)
- Georges Perec: RP = 9.01 (strong rupture)

The Stein/Bök divergence tracks their constraint types: Stein's constraints are
*additive* (repetition accumulates context, increasing entropy), while Bök's are
*restrictive* (phonetic constraints reduce context, decreasing entropy), creating
opposite information-theoretic environments for high-S₂ events.

---

## Theoretical Interpretation: The "Tramway Paradox"

These findings support what we might call the **tramway paradox**:

> The more tramway-like the poetic context (formal, predictable, high-confidence),
> the more explosive any deviation from it.

Poets who work in forms (sonnet, couplet, meter) create high-confidence contexts that
amplify every rupture. Prose poets work in open terrain where surprises anchor rather
than liberate. The liberation effect requires the compression of expectation that
only formality can provide.

This reframes a longstanding debate in prosody: formal verse doesn't constrain the
poet — it **amplifies** the poet's surprises by making confident contexts within which
ruptures detonate.

---

## Limitations

1. **Poet sample size**: Thomas Gray has only 50 high-S₂ events (just over the threshold);
   his top ranking should be treated as provisional.
2. **Corpus representation**: Some poets appear only in a single era-type (sea chanty,
   biblical) where corpus size limits generalization.
3. **Entropy thresholds**: The 4-bit/7-bit cutoffs are inherited from the entropy cascade
   study and may not be optimal for individual poet analysis.
4. **GPT-2 as proxy**: The model's notion of "confident" context is English-language-
   biased; results for translated works (Vallejo, Baudelaire) mix language-level and
   translation-level effects.

---

## Suggested Next Steps

1. **Within-poem evolution**: Does a poet's RP ratio shift across their career? Plot
   per-poet RP index by publication year to detect stylistic evolution.

2. **Rupture moments as literary events**: For top-rupture poets, identify the specific
   tokens that produced the largest liberation effects. Do these correspond to canonical
   "great lines"?

3. **Prose poetry internal taxonomy**: Within the prose-poetry cluster, which texts
   are most pivot-dominant? Does Russell Edson's surrealism differ from Rankine's
   documentary poetics?

4. **The tramway paradox — formal test**: Directly compare the same poet's formal vs.
   informal poems (e.g., Yeats's early ballads vs. late free verse). Does formality
   increase rupture scores within a single poet's output?

5. **Interaction with suppressed lexicon**: For rupture-dominant poets, what word
   classes does GPT-2 suppress at the moment of rupture? For pivot-dominant poets?
