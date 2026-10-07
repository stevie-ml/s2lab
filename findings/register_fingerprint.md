# The Register Fingerprint: Mapping 211 Poems in 2D Information Space

**Date:** 2026-10-07  
**Experiment:** `experiments/register_fingerprint.py` → `results/register_fingerprint.json`  
**Corpus:** 211 poems (19 oral, 51 literary, 141 mixed)  
**Builds on:** `oral_literary_register.md` (the 2-axis hypothesis)

---

## Research Question

The `oral_literary_register.md` finding proposed a "register fingerprint" — a 2D space
separating oral and literary traditions using:

- **X-axis**: Entropy autocorrelation lag-1 (rhythmic groove)
- **Y-axis**: True Straussian Score (lexical deviation at confident positions)

This experiment maps **all 211 poems** onto this space, tests how cleanly the registers
cluster, and identifies the most interesting crossover poems.

---

## Finding 1: The 2D Space Works — Partially

| Register | n | Mean AC1 | Mean TSS | Frac Low-Entropy | Mean Entropy |
|---|---|---|---|---|---|
| ORAL | 19 | **0.210** | **0.215** | 38.7% | 5.55 |
| MIXED | 141 | 0.054 | 0.272 | 28.4% | 6.44 |
| LITERARY | 51 | 0.062 | **0.279** | 24.8% | 6.73 |

**Cluster centroids** (oral vs. literary):
- Oral centroid: AC1 = 0.210, TSS = 0.215
- Literary centroid: AC1 = 0.062, TSS = 0.279
- Euclidean distance: **0.162**

The two clusters are **separated by ~16% of the unit range** in this 2D space — meaningful but
not dramatic. The X-axis (AC1) is the primary discriminant; the Y-axis (TSS) is secondary and
**inverted** from what one might expect: oral poems have *lower* TSS, literary poems *higher*.

Oral and literary traditions occupy opposite quadrants of the space:

```
High TSS ↑  |  "Double Deviants" | LITERARY zone  |
            |  (oral + literary)  | (low AC1,      |
            |                     |  high TSS)     |
            |---------------------+----------------|
Low TSS  ↓  |  ORAL zone          | Middle ground  |
            |  (high AC1,         | (neither pure) |
            |   low TSS)          |                |
            +--------------------------------------------→
               High AC1                  Low AC1
```

---

## Finding 2: Eight Literary Poems That Behave Like Oral Poetry

Using threshold AC1 > 0.15 AND TSS < 0.25, 8 literary-classified poems fall in the "oral zone":

| Title | Era | AC1 | TSS |
|---|---|---|---|
| Buffalo Bill 's | modernist | **0.817** | 0.054 |
| Susie Asado | modernist | **0.582** | 0.222 |
| Grass | modernist | 0.321 | 0.211 |
| Leaving the Atocha Station | new_york_school | 0.266 | 0.200 |
| And Ut Pictura Poesis Is Her Name | new_york_school | 0.255 | 0.192 |
| The Congo (opening, sanitized) | modernist | 0.235 | 0.148 |
| The Emperor of Ice-Cream | modernist | 0.233 | 0.136 |
| What Is Poetry | new_york_school | 0.197 | 0.125 |

**The E.E. Cummings anomaly**: *Buffalo Bill 's* has AC1 = **0.817** — the highest in the
entire 211-poem corpus, higher than any oral tradition poem. This concrete poem's extreme
whitespace and fragmentation creates a rhythmic groove that GPT-2's entropy pattern
registers as more "oral" than a Scottish ballad.

**The pattern**: Most of these 8 poems are **early modernist** or **New York School**. What
do Cummings, Stein (*Susie Asado*), Sandburg (*Grass*), Ashbery, and Lindsay have in common?
They all use **repetition, incantation, and syntactic play** as their primary poetic device.
Stein's "Susie Asado" repeats sonic patterns obsessively; Sandburg's "Grass" has its
"shovel them under and let me work"; Cummings' visual fragmentation creates rhythmic lockstep.
These poets are classified as literary but their information-theoretic mechanism is oral.

**Implication**: The oral/literary register divide does not map cleanly onto traditional
genre classifications. Some of the 20th century's most avant-garde "literary" poets are
actually running the oral mechanism (rhythmic groove, systematic satisfaction of expectation)
rather than the literary mechanism (lexical deviation from confident predictions).

---

## Finding 3: Four Oral Poems That Behave Like Literary Poetry

| Title | Era | AC1 | TSS |
|---|---|---|---|
| Sir Patrick Spens | ballad | 0.062 | **0.412** |
| Psalm 121 (KJV) | biblical | 0.053 | **0.328** |
| Nursery Rhymes (compilation) | nursery_rhyme | 0.099 | 0.307 |
| Psalm 19:1-6 (KJV) | biblical | 0.089 | 0.262 |

**The Biblical paradox**: The KJV Psalms (Psalms 19, 23, 46, 121, Song of Solomon) were
classified as ORAL (biblical tradition), but they cluster closest to the *literary* centroid.
Three of the six most "misplaced" oral poems are from the Bible:

| Poem | d_lit | d_oral | AC1 | TSS |
|---|---|---|---|---|
| Psalm 46:1-5 (KJV) | **0.027** | 0.138 | 0.080 | 0.258 |
| Psalm 19:1-6 (KJV) | 0.032 | 0.131 | 0.089 | 0.262 |
| Psalm 23 (KJV) | 0.045 | 0.152 | 0.059 | 0.234 |

The KJV Psalms are a literary *translation* of an oral tradition. Their rhetoric — parallelism,
elevation of vocabulary, apophatic construction — was shaped by the 17th-century translators
to carry weight on the page. The oral rhythm of the Hebrew original (meter, acrostic structure,
chanting patterns) is not recoverable from the English translation, so GPT-2 sees only the
literary elevation. The Bible as we read it in English behaves informationally as literary
poetry, not oral tradition.

**Sir Patrick Spens** (TSS = 0.412, the highest of any ballad) is the other anomaly.
Its compressed narrative jumps — "half-owre, half-owre to Aberdour / It's fifty fathoms deep"
— are so abrupt that GPT-2 is repeatedly surprised at positions where it was confident.
This is a ballad that achieves literary-style lexical deviation within an oral framework.

---

## Finding 4: The Double Deviants — 16 Poems Running Both Mechanisms

"Double deviants" have both high AC1 (> 0.15) AND high TSS (> 0.26): they create a rhythmic
groove *and* consistently deviate lexically from the model's confident predictions.

| Title | Era/Register | AC1 | TSS |
|---|---|---|---|
| The House on the Hill | fixed_form/MIXED | 0.454 | 0.267 |
| Yesterday (prose poem) | prose_poetry/MIXED | 0.384 | 0.348 |
| In After Days (rondeau) | fixed_form/MIXED | 0.345 | 0.417 |
| The Fish | modernist/LITERARY | 0.366 | 0.267 |
| The Road Not Taken | modernist/LITERARY | 0.301 | 0.324 |
| Islets/Irritations | language/LITERARY | 0.281 | 0.467 |
| Peony Falling (Buson) | haiku/MIXED | 0.285 | 0.400 |
| A Wave (opening) | new_york_school/LITERARY | 0.237 | 0.400 |
| The Ballad of Dead Ladies | fixed_form/MIXED | 0.235 | 0.324 |
| The Truth the Dead Know | confessional/MIXED | 0.258 | 0.556 |
| Nobody (Wright) | haiku/MIXED | 0.377 | 0.500 |

**The fixed_form cluster**: Fixed forms (villanelle, sestina, rondeau) dominate the "double
deviant" zone. This confirms a central theoretical prediction: strict formal constraint
creates the rhythmic groove (meter and refrain raise AC1), but the best formal poets
consistently *violate* those constraints lexically (high TSS). The form sets up the
expectation; the poet breaks it.

**The Road Not Taken (Frost)**: AC1 = 0.301, TSS = 0.324. This is one of the most
mass-accessible poems in the English language, and yet it scores as a double deviant —
its ballad-like meter creates a strong groove, but Frost consistently surprises at every
confident position. The poem's mass appeal may partly derive from this mechanism: the
rhythmic groove draws readers in, while the lexical deviations create the sensation of
depth and originality.

**"The Truth the Dead Know" (Sexton)**: TSS = 0.556 with moderate AC1 = 0.258.
Anne Sexton's poem combines confessional directness (driving a rhythmic, declarative
groove) with extreme lexical deviation — she consistently defies the model's confident
predictions. This pairing may explain the feeling of confessional poetry: the direct,
plain-speech tone creates predictability at the structural level, then the actual words
chosen are anything but plain.

---

## Finding 5: Era Fingerprints — The Full Ordering

| Era | Register | n | AC1 | TSS | Mean Entropy |
|---|---|---|---|---|---|
| song_lyrics | ORAL | 3 | **0.425** | 0.160 | 4.53 |
| ballad | ORAL | 6 | **0.347** | 0.205 | 6.05 |
| fixed_form | MIXED | 8 | **0.319** | 0.253 | 6.36 |
| found_poetry | MIXED | 7 | 0.134 | 0.240 | 4.93 |
| modernist | LITERARY | 22 | 0.112 | 0.275 | 6.76 |
| victorian | MIXED | 21 | 0.064 | 0.276 | 6.76 |
| contemporary | MIXED | 9 | 0.063 | 0.295 | 6.00 |
| biblical | ORAL | 7 | 0.057 | **0.264** | 5.32 |
| haiku | MIXED | 12 | 0.053 | **0.292** | 7.08 |
| german_symbolist | MIXED | 3 | 0.046 | **0.414** | 6.87 |
| prose_poetry | MIXED | 9 | 0.037 | **0.292** | 5.70 |
| new_york_school | LITERARY | 18 | 0.037 | **0.295** | 6.69 |
| language | LITERARY | 3 | 0.029 | **0.299** | 6.80 |
| confessional | MIXED | 6 | 0.020 | **0.380** | 6.95 |
| metaphysical | LITERARY | 4 | −0.001 | 0.262 | 6.96 |
| control | MIXED | 5 | −0.020 | 0.139 | 5.59 |
| harlem_renaissance | MIXED | 5 | −0.024 | 0.279 | 6.63 |
| 19th_century | MIXED | 11 | −0.050 | **0.305** | 6.85 |

**Three notable findings**:

1. **German Symbolist poetry has the highest TSS (0.414)** — Rilke, Stefan George, and their
   contemporaries are the most relentlessly lexically deviant of any era in the corpus. Their
   elevated, mystical vocabulary consistently surprises GPT-2 at its most confident positions.

2. **Confessional poetry (TSS = 0.380)** — the second-highest TSS. The "plain speech" of
   Sexton, Lowell, and Plath is informationally anything but plain. Their plain syntax
   creates confident positions that they then fill with unexpected, intensely personal
   vocabulary.

3. **The control poems (TSS = 0.139)** — the lowest TSS, confirming the baseline. Texts
   designed to be maximally predictable are maximally predictable. The control corpus
   effectively anchors the lower bound of the fingerprint space.

4. **19th_century (AC1 = −0.050)** — the only era with **negative** entropy autocorrelation,
   meaning consecutive positions are *anti-correlated* in their entropy. A confident position
   is slightly more likely to be followed by an uncertain one and vice versa. This may reflect
   the 19th-century rhetorical tradition: alternating between concrete, noun-heavy statements
   and expansive, less-predictable elaboration.

---

## Finding 6: Zone Distribution Confirms Imperfect Separation

| Zone | ORAL (n=19) | MIXED (n=141) | LITERARY (n=51) |
|---|---|---|---|
| oral_zone | 37% | 14% | **16%** |
| literary_zone | **21%** | 40% | 43% |
| double_deviant | 5% | 8% | 8% |
| middle | 37% | 38% | 33% |

Key observation: **Literary poems fall in the oral zone (16%) almost as often as oral poems
themselves (37%)** — the separation is real but not clean. The "wrong" classification rate
for literary poems in the oral zone is substantial. Conversely, only 21% of oral poems fall
in the literary zone.

This asymmetry reveals the underlying structure: **being oral is informatively distinctive**
(a high AC1 score is a strong signal), but **being literary is not** — a low AC1 score is
necessary but not sufficient for the literary register. The literary cluster is defined by
what it lacks (rhythmic groove) rather than by a unique positive property.

---

## Interpretation: Two Mechanisms, Continuous Variation

The register fingerprint confirms the two-mechanism model proposed in `oral_literary_register.md`,
but with more nuance:

1. **Oral mechanism**: Uses rhythmic regularity (meter, formula, repetition) to create a
   "groove." The model's entropy becomes autocorrelated. Lexical deviation is LOW because
   the poem works by satisfying rhythmic expectation.

2. **Literary mechanism**: Uses lexical deviation at confident positions. The model's entropy
   is *not* autocorrelated — there is no groove, only individual-token surprise.

3. **Double deviant mechanism**: A third, rarer mode — used by fixed forms, some modernists
   (Frost), and confessional poetry. The form creates the groove; the poet then fills it with
   unexpected lexical choices. This may be informationally the most "demanding" of all three,
   as it requires managing both dimensions simultaneously.

The oral/literary divide is **continuous, not categorical**. The "register" of a poem is
not a binary flag but a position in a 2D space that can be read off its information-theoretic
profile.

---

## Suggested Next Steps

1. **Hopkins' sprung rhythm test**: Does Gerard Manley Hopkins (*God's Grandeur*, *Pied Beauty*,
   *The Windhover*) score as oral (high AC1 from strong accentual stress) or literary
   (high TSS from dense, rare vocabulary)? His corpus presence suggests MIXED — but where
   exactly does he fall in the double-deviant zone?

2. **The Stein-Cummings cluster**: Why do Gertrude Stein and E.E. Cummings (plus Lindsay's
   *The Congo*) have such anomalously high AC1? Investigate their token-level profiles:
   is the groove created by lexical repetition, by syntactic parallelism, by punctuation
   patterns, or by something else?

3. **Tracking the double-deviant mechanism historically**: Is the double-deviant zone a
   modernist invention (Frost, Bishop, early-20th-century), or does it appear in earlier
   formal poetry (Donne, Dryden, Pope)?

4. **Negative AC1 and 19th-century rhetoric**: Why does 19th-century poetry (Browning,
   Tennyson, Arnold) show anti-correlated entropy? Test whether this is a feature of the
   dramatic monologue form specifically.

5. **Full corpus scatter plot**: Build an interactive HTML visualization of all 211 poems
   in (AC1, TSS) space, colored by era, with hover labels.
