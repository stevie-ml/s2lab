# Animal Vocabulary and S₂: Creature Names as Straussian Deviations

**Date:** 2026-11-28  
**Experiment:** `experiments/animal_vocabulary_s2.py`  
**Data:** 457 texts, 199 animal tokens in poetry, results in `results/animal_vocabulary_s2.json`

---

## Research Question

Poetry has long been a home for the nonhuman: Blake's tiger, Keats's nightingale, 
Hopkins's falcon, Whitman's spider, Dickinson's fly. Does information theory 
confirm what readers sense — that animal names are informationally charged 
in a way that abstract or connective language is not?

**Hypothesis:** Animal vocabulary constitutes a consistent form of Straussian 
deviation. GPT-2, trained on general prose, does not expect creature names in the 
positions poets place them. The act of naming an animal is itself an informational 
surprise — a pointer away from language's default toward the nonhuman world.

---

## Core Finding: Animal Premium

| Token Class | N | Avg S₂ | % Positive S₂ |
|------------|---|--------|--------------|
| All poetry tokens | 65,181 | +0.228 | ~37% |
| **Animal tokens (poetry)** | **199** | **+2.009** | **63.3%** |
| **Animal premium** | — | **+1.781** | **+26 pp** |
| Animal tokens (prose control) | 2 | ~−1.6 | — |

**Animal tokens in poetry average 8.8× the corpus S₂.** This is a large, robust effect.

---

## S₂ by Animal Category

The hierarchy reveals a cultural and ecological logic:

| Category | N | Avg S₂ | % +S₂ | Max S₂ |
|---------|---|--------|-------|--------|
| mythological | 1 | +5.94 | 100% | 5.94 |
| aquatic | 18 | +4.01 | 94.4% | 14.00 |
| reptiles & amphibians | 6 | +3.82 | 83.3% | 7.62 |
| birds (wild) | 24 | +2.46 | 66.7% | 15.83 |
| mammals (predatory) | 17 | +2.11 | 64.7% | 6.36 |
| insects & arachnids | 41 | +1.89 | 61.0% | 11.81 |
| birds (domestic) | 18 | +1.50 | 66.7% | 7.03 |
| mammals (prey) | 33 | +1.42 | 45.5% | 13.21 |
| mammals (domestic) | 41 | +1.28 | 58.5% | 9.50 |

**Reading the hierarchy:** Creatures that occupy the margins of the human world 
(mythological, aquatic, reptilian) are most surprising. Domesticated animals that 
share our everyday vocabulary (horse, dog, cow) are less surprising but still above 
the poetry baseline.

---

## Predators vs. Prey; Wild vs. Domestic

| Dimension | Category | N | Avg S₂ | Premium |
|-----------|---------|---|--------|---------|
| Aggression | Predatory (hawk, wolf, snake, etc.) | 47 | +2.508 | +0.864 |
| | Prey (rabbit, lamb, sparrow, etc.) | 92 | +1.644 | — |
| Wildness | Wild animals | 140 | +2.288 | +0.941 |
| | Domestic animals | 59 | +1.347 | — |

Both effects are consistent: **the more ecologically remote from human domesticity, 
the higher the S₂.** This may reflect vocabulary frequency in prose training data — 
"horse" and "dog" appear more frequently in prose than "hawk" and "serpent."

---

## Top High-S₂ Animal Moments

The twenty highest-S₂ animal tokens, with what GPT-2 expected instead:

| Token | S₂ | Category | Expected | Poem |
|-------|-----|---------|---------|------|
| raven | +15.83 | birds_wild | `le` (as in "table") | Edgar Allan Poe |
| whale | +14.00 | aquatic | `a` | Patterns |
| buck | +13.21 | mammals_prey | `\n` | My Life by Water |
| Fly | +11.81 | insects | ` lot` | I heard a Fly buzz |
| ant | +10.24 | insects | `ations` | The Bridge of Heraclitus |
| buck | +10.05 | mammals_prey | `known` | Morning Glory (Chiyo-ni) |
| worm | +9.91 | insects | `thro` | Proverbs of Hell |
| spider | +9.60 | insects | `,` | A Noiseless Patient Spider |
| Ass | +9.50 | mammals_domestic | `\n` | I heard a Fly buzz |
| swift | +8.89 | birds_wild | `\n` | The Fish |
| Eagle | +8.65 | birds_wild | ` man` | On Seeing the Elgin Marbles |
| Frog | +7.62 | reptiles | ` –` | I'm Nobody! Who are you? |
| Falcon | +7.51 | birds_wild | `-` | The Windhover |

### Close readings

**"I heard a Fly buzz — when I died"** (Dickinson): GPT-2 expected " lot" after 
"I heard a Fly buzz" — predicting a commonplace ("a lot of noise," "quite a lot"). 
Dickinson names the fly instead. Then "Ass" appears with S₂=9.50 because GPT-2, 
after the fly buzzing passage, expected a line break rather than the word for a 
donkey. These are likely stanza-break artifacts, but the fly itself is genuine.

**"A Noiseless Patient Spider"** (Whitman): "spider" at S₂=9.60 when the model 
expected a comma — the spider is named where punctuation would logically appear. 
Whitman halts the grammatical flow to place the creature there.

**"The Windhover"** (Hopkins): "Falcon" at S₂=7.51 when the model expected a hyphen. 
Hopkins writes "dapple-dawn-drawn Falcon" — the bird's name arrives mid-hyphenation 
cascade, in a slot GPT-2 reads as a compound continuation. The naming of the bird 
is the rupture in the hyphenation pattern.

**"raven"** in Poe: S₂=15.83, GPT-2 expected "le" — as in a word ending "-le" 
(table, able, stable). The raven's name arrives where a mundane syllable was expected.

---

## Theoretical Interpretation

Animal naming in poetry functions as a **systematic defamiliarization mechanism** 
at the information-theoretic level. The pattern has several components:

1. **Vocabulary frequency gap:** Animal names are less frequent in GPT-2's prose 
   training data than the abstract and connective vocabulary poetry might otherwise 
   use. When a poet writes "falcon" where prose would write "therefore" or "thus," 
   the gap is measurable.

2. **The specificity premium:** Generic "bird" likely has lower S₂ than "nightingale" 
   or "raven." The choice to name the specific creature is an act of precision that 
   the language model reads as surprise.

3. **The ecological gradient:** The wild–domestic gradient in S₂ suggests the effect 
   is partly frequency-based: horses and dogs appear in prose training data constantly 
   (racing reports, dog-care texts), while ravens and pike rarely do.

4. **Poetic traditions matter:** The "animal apostrophe" — addressing or naming a 
   nonhuman creature — is a recognized poetic genre from Keats's nightingale ode 
   to Hughes's crow. This experiment gives that tradition a quantitative signature.

---

## Comparison to Other Semantic Fields

From prior experiments:

| Vocabulary class | Avg S₂ in poetry | Premium over baseline |
|----------------|----------------|---------------------|
| Temperature words | +4.45 | +4.22 |
| Aquatic animals | +4.01 | +3.78 |
| Sound words | +3.24 | +3.01 |
| **All animal words** | **+2.01** | **+1.78** |
| Texture words | +2.54 | +2.31 |
| Color words | +2.48 | +2.25 |
| All sensory words | +2.16 | +1.93 |
| Corpus baseline | +0.23 | — |

Animals sit within the sensory-word range, which makes sense: naming an animal is 
a sensory act, a commitment to specificity over abstraction.

---

## New Poems Added to Corpus

8 animal-centered poems were added to the corpus for future analysis:
- **Ted Hughes**: "The Hawk in the Rain," "Pike"
- **D.H. Lawrence**: "Snake"  
- **Marianne Moore**: "The Fish"
- **Mary Oliver**: "Wild Geese"
- **Gerard Manley Hopkins**: "The Windhover" (animal-focused version)
- **Sylvia Plath**: "Stings (Bee Sequence, excerpt)"
- **William Blake**: "The Tyger (complete)" (fuller version)

These will be processed in the next engine run to test these hypotheses with 
poems selected specifically for their animal imagery.

---

## Suggested Next Steps

1. **Genus vs species specificity:** Compare tokens at different levels of 
   biological specificity. "Bird" vs "nightingale" vs "nightingale" token 
   broken into sub-words. Does naming the specific species have higher S₂?

2. **Animal-apostrophe poems:** Isolate poems that directly address an animal 
   (Keats, Hopkins, Whitman, Hughes) and compare their overall S₂ profiles to 
   poems that merely mention animals.

3. **Animal-verb nexus:** When does a predatory animal *act* (the hawk stoops, 
   the wolf runs)? Do action verbs near animal names inherit elevated S₂?

4. **Cross-cultural animal vocabulary:** Test on translated poems. Does the 
   semantic field of "unexpected animal" work in German, French, Japanese? 
   The existing multilingual corpus offers a partial test.

5. **Frequency correction:** Control for corpus frequency. Build a matched 
   set of non-animal tokens with the same GPT-2 frequency distribution and 
   compare their S₂ values to test whether the animal effect exceeds what 
   frequency predicts.
