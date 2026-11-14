# Derivational Morphology and S₂

**Date:** 2026-11-14
**Corpus:** 419 poems | **Tokens analyzed:** 54,613 (artifact positions removed: 2,971)

## Research Question

Do words carrying derivational suffixes (e.g. *-ness*, *-tion*, *-ly*) or prefixes
(e.g. *un-*, *re-*, *dis-*) show systematically different information-theoretic
signatures in poetry? Do abstract nominalizations feel predictable or surprising?

**Hypothesis A**: Nominal suffixes (-tion/-ness/-ity) signal abstract register and are
*more predictable* (lower S₂) because abstract diction is contextually constrained.

**Hypothesis B**: Negating/reversing prefixes (un-/dis-/mis-) are *more surprising*
because they reverse the expected polarity.

**Hypothesis C**: Adverbial -ly forms are the *most conformist* — they tend to modify
predictable adjectives/verbs and rarely carry the semantic weight of a poem.

---

## Results: Coarse Morphological Groups

| Morphological Class | n tokens | Mean S₂ | +S₂ Rate | Max S₂ | Std |
|---|---|---|---|---|---|
| NOUN suffix | 317 | **2.001** | 63.7% | 17.4 | 4.346 |
| ADJ suffix | 314 | **2.688** | 65.0% | 17.3 | 4.675 |
| VERB suffix / gerund | 1,343 | **1.898** | 60.8% | 20.7 | 4.259 |
| ADV suffix | 216 | **3.038** | 74.1% | 20.6 | 4.170 |
| prefix | 359 | **2.415** | 68.2% | 16.4 | 4.031 |
| base form | 52,064 | **-0.536** | 32.3% | 36.7 | 3.556 |

---

## Results: Fine-Grained Suffix Analysis (n ≥ 50 tokens)

| Suffix class | n | Mean S₂ | +S₂ Rate | Max S₂ | Group |
|---|---|---|---|---|---|
| `into/negation in-` | 59 | **3.756** | 81.4% | 16.4 | prefix |
| `adverb -ly` | 216 | **3.038** | 74.1% | 20.6 | ADV suffix |
| `adjective -al` | 120 | **2.715** | 67.5% | 15.6 | ADJ suffix |
| `gerund/participle -ing` | 727 | **2.615** | 68.1% | 20.7 | VERB suffix / gerund |
| `quality -ness` | 53 | **1.987** | 64.2% | 12.8 | NOUN suffix |
| `iteration re-` | 165 | **1.967** | 66.7% | 11.0 | prefix |
| `nominalizer -tion` | 74 | **1.859** | 63.5% | 15.7 | NOUN suffix |
| `adjective -ous` | 56 | **1.597** | 55.4% | 14.0 | ADJ suffix |
| `verbalizer -en` | 546 | **0.828** | 50.0% | 15.8 | VERB suffix / gerund |
| `base form (short)` | 52,064 | **-0.536** | 32.3% | 36.7 | base form |

---

## High-S₂ Examples by Suffix Class

### `into/negation in-`
- **instead** (S₂=6.73) in *The Summer Day* [contemporary]
- **indoors** (S₂=10.16) in *The Fall* [prose_poetry]
- **indoors** (S₂=16.4) in *The Fall* [prose_poetry]
- **incess** (S₂=9.69) in *Natural Selection (Found Poem from Darwin, 1859)* [found_poetry]
- **involve** (S₂=8.93) in *Terms and Conditions (Found Poem from generic legal prose)* [found_poetry]

### `adverb -ly`
- **lonely** (S₂=11.37) in *I Wandered Lonely as a Cloud* [romantic]
- **kindly** (S₂=7.58) in *Because I could not stop for Death* [19th_century]
- **badly** (S₂=20.59) in *One Art* [mid_century]
- **merely** (S₂=7.3) in *The Painter* [new_york_school]
- **Certainly** (S₂=7.11) in *And Ut Pictura Poesis Is Her Name* [new_york_school]

### `adjective -al`
- **hysterical** (S₂=15.61) in *Howl (opening)* [beat]
- **manual** (S₂=6.3) in *The Instruction Manual* [new_york_school]
- **central** (S₂=7.22) in *The One Thing That Can Save America* [new_york_school]
- **financial** (S₂=6.01) in *Ketjak (excerpt)* [language]
- **international** (S₂=10.91) in *Islets/Irritations (excerpt)* [language]

### `gerund/participle -ing`
- **belonging** (S₂=5.3) in *Song of Myself (section 1)* [19th_century]
- **observing** (S₂=20.4) in *Song of Myself (section 1)* [19th_century]
- **breeding** (S₂=11.17) in *The Waste Land (opening)* [modernist]
- **feeding** (S₂=9.22) in *The Waste Land (opening)* [modernist]
- **starving** (S₂=5.61) in *Howl (opening)* [beat]

### `quality -ness`
- **loneliness** (S₂=5.37) in *Black Stone Lying on a White Stone* [surrealist]
- **weakness** (S₂=5.47) in *London* [romantic]
- **goodness** (S₂=5.48) in *They Flee from Me* [early_modern]
- **goodness** (S₂=10.49) in *Psalm 23 (KJV)* [biblical]
- **darkness** (S₂=6.25) in *Der Gott der Stadt (The God of the City, trans.)* [german_expressionist]

### `iteration re-`
- **retreat** (S₂=5.26) in *The Love Song of J. Alfred Prufrock (opening)* [modernist]
- **restaurants** (S₂=8.34) in *The Love Song of J. Alfred Prufrock (opening)* [modernist]
- **relevant** (S₂=7.47) in *A Wave (opening)* [new_york_school]
- **retina** (S₂=6.2) in *Scientific Method (Found Poem from Newton's Opticks, 1704)* [found_poetry]
- **Resources** (S₂=6.45) in *Dream Song 14 (opening)* [confessional]

### `nominalizer -tion`
- **instruction** (S₂=5.52) in *The Instruction Manual* [new_york_school]
- **interrogation** (S₂=7.18) in *Aubade (opening)* [contemporary]
- **redemption** (S₂=14.49) in *On Being Brought from Africa to America* [18th_century]
- **eviction** (S₂=15.74) in *S+7: Genesis (N+7 variant)* [oulipo]
- **ambition** (S₂=5.59) in *An Essay on Man (Epistle I, opening)* [18th_century]

### `adjective -ous`
- **tedious** (S₂=13.98) in *Neutral Tones* [victorian]
- **various** (S₂=5.51) in *Dover Beach (closing stanzas)* [victorian]
- **spacious** (S₂=5.17) in *For Spacious Skies* [concrete]
- **spacious** (S₂=7.7) in *For Spacious Skies* [concrete]
- **anxious** (S₂=9.01) in *The Vanity of Human Wishes (opening)* [18th_century]

### `verbalizer -en`
- **kitchen** (S₂=9.98) in *The Emperor of Ice-Cream* [modernist]
- **linen** (S₂=9.05) in *Lady Lazarus (opening)* [confessional]
- **when** (S₂=5.03) in *My Life (excerpt)* [language]
- **even** (S₂=10.93) in *Citizen (excerpt)* [contemporary]
- **golden** (S₂=5.24) in *The Negro Speaks of Rivers* [harlem_renaissance]

### `base form (short)`
- **wandered** (S₂=6.11) in *I Wandered Lonely as a Cloud* [romantic]
- **cloud** (S₂=8.1) in *I Wandered Lonely as a Cloud* [romantic]
- **val** (S₂=10.7) in *I Wandered Lonely as a Cloud* [romantic]
- **pains** (S₂=5.02) in *Ode to a Nightingale (stanza 1)* [romantic]
- **,** (S₂=7.15) in *Ode to a Nightingale (stanza 1)* [romantic]

---

## Era × Morphological Group

Top 5 eras by NOUN suffix S₂ mean (how much do different eras use surprising abstract diction?):

| Era | Mean S₂ (NOUN suffix) | n |
|---|---|---|
| modernist | 2.314 | 21 |
| contemporary | 2.143 | 31 |
| new_york_school | 1.012 | 29 |
| 19th_century | 0.949 | 24 |
| found_poetry | -1.166 | 29 |

Top 5 eras by PREFIX S₂ mean (do some eras use more surprising prefixed forms?):

| Era | Mean S₂ (prefix) | n |
|---|---|---|
| modernist | 4.684 | 17 |
| dramatic_monologue | 4.063 | 15 |
| early_modern | 3.798 | 14 |
| prose_poetry | 3.604 | 15 |
| romantic | 3.562 | 12 |
| new_york_school | 3.413 | 19 |
| victorian | 3.269 | 26 |
| biblical | 2.978 | 13 |
| 19th_century | 2.582 | 10 |
| procedural | 2.279 | 11 |

---

## Finding

**Ranking of morphological groups by mean S₂ (artifact-free):**
1. **ADV suffix**: 3.038
2. **ADJ suffix**: 2.688
3. **prefix**: 2.415
4. **NOUN suffix**: 2.001
5. **VERB suffix / gerund**: 1.898
6. **base form**: -0.536

**Hypothesis A CHALLENGED**: Nominal suffixes are *not* more predictable than base forms.
NOUN suffix mean S₂ (2.001) ≥ base (-0.536).

**Hypothesis B SUPPORTED**: Prefixed forms have higher S₂ than base forms
(2.415 vs -0.536), consistent with negation/reversal creating surprise.

**Hypothesis C OVERTURNED — KEY FINDING**: **Adverbial -ly forms are the MOST
surprising morphological class** (mean S₂ 3.038, +S₂ rate 74.1%). Examples:
- "badly" in Bishop's *One Art* (S₂ = 20.59): understated devastation
- "lonely" in Wordsworth (S₂ = 11.37): unexpected attributive adverb  
- "kindly" in Dickinson (S₂ = 7.58): ironic courtesy of Death

In prose, adverbs modify predictable verbs and adjectives. In **poetry**, the
-ly adverb becomes an instrument of understatement, irony, and tonal rupture.
GPT-2 does not anticipate the flat adverb in a heightened context — this is
precisely where poets exploit the Straussian gap.

> **⚠️ Methodological note**: the "base form" category captures *all* words
> shorter than 4 characters or without recognized affixes — including the full
> inventory of function words (articles, prepositions, conjunctions, pronouns)
> which are highly predictable. The gap between suffix classes and "base form"
> therefore partly reflects the content-word vs. function-word divide.
> The *relative ranking among suffix/prefix classes* is the more informative
> comparison.

### Interpretation

**The adverb -ly as a Straussian weapon**: the most striking result is that
adverbial forms — typically the least prestigious word class in prose style —
appear at high-S₂ positions in poetry far more reliably than any other
morphological class. The 74.1% positive-S₂ rate means three in four -ly
adverbs appear where the model is MORE confident than the word warrants.

This suggests a poetic strategy of **register collision**: poets drop flat
adverbs into contexts of emotional or semantic intensity, and the mismatch
between the model's expectation and the poet's mundane modifier creates the
gap. Bishop's "badly" at the climax of *One Art* is the canonical example;
the data show it is systematic.

**Nominal suffixes at the bottom**: -tion and -ness words rank above average
but below other suffix classes. Abstract diction is unexpected in an absolute
sense but *less* unexpected than adverbs or adjectives, because the model
partly anticipates the register shift when elevated vocabulary is building.

### Next Steps

- Compare nominalization rates across eras: do Victorian/Romantic poets
  nominalize more heavily, explaining their lower artifact-free S₂?
- Specifically test whether Latinate (Romance) suffixes vs Germanic suffixes
  differ (extends `latinate_germanic_diction_s2.md`).
- Look at compound words with these suffixes in haiku and concrete poetry
  vs. their much lower S₂ means — could derivational density explain their rank?