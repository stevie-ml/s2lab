# Poetic Peaks: Anatomy of the Highest-S₂ Moment per Poem

**Date:** 2026-11-05  
**Experiment:** `experiments/poetic_peaks.py` → `results/poetic_peaks.json`  
**Corpus:** 403 English-language poems, all with peak S₂ ≥ 1.0 (artifact-filtered)  
**Research question:** What is the anatomy of the single highest-S₂ moment in each poem? What type of word, at what position, suppressing what alternative?

---

## Background

Previous work has characterized high-S₂ tokens statistically — their distribution, era profiles, POS budgets. This experiment asks a different question: **in each poem, what is the absolute peak Straussian gap?** The maximum-S₂ token is the single moment when the poet deviated most drastically from language's expectations. What is it, and what did it displace?

---

## Finding 1: The Peak Is Almost Always a Content Word

Across 403 poems, the peak S₂ token is classified as:

| Token type | N | % |
|---|---|---|
| **Content word** | 349 | **86.6%** |
| Structural (punct/newline) | 20 | 5.0% |
| Function word | 19 | 4.7% |
| Punctuation | 15 | 3.7% |

**86.6% of peak moments are content words.** The highest-surprise moment in almost every poem is when the poet placed a noun, verb, or adjective where the model least expected one. The peak is almost never structural or grammatical.

---

## Finding 2: The Peak Mostly Falls in the FIRST THIRD of the Poem

| Position zone | N | % |
|---|---|---|
| **First third** | 186 | **46.2%** |
| Middle third | 113 | 28.0% |
| Last third | 104 | 25.8% |

This is striking: **nearly half of poems have their maximum surprise in the first third**. This contradicts the intuition that poems build toward a climactic surprise at the end. Instead, many poets strike hardest at the outset — the "opening salvo" strategy — establishing their register of surprise early and sustaining it.

This pattern holds across poem lengths:

| Length | N | Avg relative position | Avg peak S₂ |
|---|---|---|---|
| Short (<30 tokens) | 38 | 0.30 | 8.59 |
| Medium (30–100 tokens) | 163 | 0.45 | 11.45 |
| Long (100+ tokens) | 202 | 0.43 | 13.52 |

Short poems peak earliest (position 0.30 on average) and have the lowest absolute peak — compression forces the peak earlier and constrains its height. Long poems have later and higher peaks.

---

## Finding 3: The Suppressed Alternative Is Usually a Function Word

At the moment of maximum surprise, what did GPT-2 most want?

| Suppressed type | N | % |
|---|---|---|
| **Function word** | 198 | **49.1%** |
| Content word | 74 | 18.4% |
| Punctuation | 63 | 15.6% |
| Subword | 36 | 8.9% |
| Structural | 32 | 7.9% |

At **49.1% of peak moments**, the model's top prediction was a function word. The most common specific suppressed words at content peaks:

| Suppressed word | Count |
|---|---|
| "the" | 39 |
| "of" | 14 |
| "to" | 13 |
| "and" | 9 |
| "is" | 7 |
| "you" | 6 |

**"The" is the most commonly suppressed word at peak moments.** The definite article — the most basic grammatical connector — is what language expected, and what the poet refused. This is the purest form of ambush: the model anticipated a grammatical scaffold word, and the poet delivered a content word with high semantic weight instead.

---

## Finding 4: Peak Tokens Are Rare Words

The vocabulary rank of the peak token tells us whether it was a common word in a surprising context, or a genuinely rare word:

| Rank bucket | N | % |
|---|---|---|
| Top-100 (common words) | 42 | 10.4% |
| 101–1000 (medium) | 85 | 21.1% |
| **>1000 (rare words)** | 276 | **68.5%** |
| **Median rank** | — | **2,653** |

**68.5% of peak tokens are low-frequency words** (vocabulary rank >1000 out of GPT-2's ~50K vocab). The median peak token has rank 2,653. Poetic peaks are mostly achieved through rare vocabulary — unusual words that GPT-2 assigned very low probability — not common words used in surprising positions.

---

## Finding 5: The Hall of Peaks — Top 15 Absolute Peak Moments

The highest-S₂ moments across the entire corpus:

| Rank | S₂ | Token | Suppressed | Author | Poem |
|---|---|---|---|---|---|
| 1 | 36.7 | 'gro' | (newline) | Ferlinghetti | In Goya's greatest scenes |
| 2 | 28.3 | 'climbs' | (newline) | Ferlinghetti | Constantly Risking Absurdity |
| 3 | 27.7 | 'pour' | 'm | Bukowski | Bluebird |
| 4 | 25.7 | 'hum' | (newline) | Kamau Brathwaite | Calypso |
| 5 | 25.6 | 'glass' | (newline) | Marianne Moore | The Fish |
| 6 | 23.4 | 'ferner' | 't | Stefan George | Komm in den totgesagten park |
| 7 | 22.1 | 'prank' | 'the' | Christopher Smart | For I Will Consider My Cat Jeoffry |
| 8 | 22.1 | ''' (apostrophe) | 'ering' | Wilfred Owen | Dulce et Decorum Est |
| 9 | 22.1 | 'Pra' | (newline) | Gerard Manley Hopkins | Pied Beauty |
| 10 | 22.0 | 'shook' | 'the' | Gerard Manley Hopkins | God's Grandeur |
| 11 | 22.0 | 'prank' | 'the' | Christopher Smart | For I Will Consider My Cat Jeoffry |
| 12 | 21.0 | 'env' | 'o' | Robert Browning | The Bishop Orders His Tomb |
| 13 | 20.7 | 'Pra' | (newline) | Gerard Manley Hopkins | Pied Beauty |
| 14 | 20.6 | 'printer' | 'ne' | Whitman | Song of Myself (section 15) |
| 15 | 20.6 | 'badly' | 'glass' | Elizabeth Bishop | One Art |

**Key observations:**
- Beat poets (Ferlinghetti, Bukowski) claim two of the top three. Beat's improvisational lineation creates frequent and extreme Straussian gaps.
- Hopkins appears three times in the top 15. His invented compound words and sprung rhythm produce extreme subword-tokenization surprises.
- Smart's "prank" appears twice (duplicated poem with slight variation). Jeoffry's catalogue generates maximum ambush when Smart chooses unusual nouns over expected articles.
- Bishop's "badly" (rank 15, S₂=20.6) is a true semantic peak: at the climax of "One Art," where the model predicted "glass" (continuing a rhyme pattern), Bishop wrote "badly" — the word that breaks the villanelle's formal control.

---

## Finding 6: Era Peak Profiles — Beat and Dramatic Monologue Peak Highest

| Era | N | Avg peak S₂ | Avg rel. pos | Content% | Last-third% |
|---|---|---|---|---|---|
| **beat** | 8 | **18.9** | 0.52 | 100% | 38% |
| german_symbolist | 3 | 17.8 | 0.46 | 67% | 33% |
| dramatic_monologue | 7 | 17.1 | 0.41 | 100% | 29% |
| 18th_century | 8 | 16.3 | **0.29** | 100% | 12% |
| spoken_word | 3 | 15.5 | 0.57 | 67% | 33% |
| postcolonial | 6 | 15.0 | 0.59 | 100% | 50% |
| … | … | … | … | … | … |
| haiku | 14 | 8.0 | 0.36 | 71% | 21% |
| **control** | 5 | **3.8** | **0.81** | 80% | 80% |

**Key contrasts:**
- **Beat (18.9) vs. Control (3.8)**: the gap between the highest-S₂ tradition and the prose baseline is 5×. Beat poetry generates peaks nearly five times as extreme as ordinary prose.
- **18th century peaks earliest (rel. pos 0.29)**: classical-period poets load their maximum surprise into the opening lines — perhaps because the heroic couplet's closed form makes early surprise the safest deviation.
- **Control prose peaks last (rel. pos 0.81)**: prose's highest-surprise moment arrives near the end — a consequence of topic drift over long texts, not deliberate poetic strategy.
- **Haiku (8.0) vs. Beat (18.9)**: the two extreme short-form traditions use radically different peak strategies. Haiku constrains surprise to small perturbations; Beat maximizes it.

---

## Synthesis

**The anatomy of a poetic peak:**
1. It is a content word (87% of cases)
2. It arrives in the first half of the poem (median rel. pos ≈ 0.42)
3. It displaced a function word — most often "the" (49% of cases)
4. It is a rare vocabulary item (median rank: 2,653)
5. Its S₂ value is ~12 on average, but can reach 37 for extremes

**The 'Opening Bomb' effect**: First-third peaks dominate (46.2%). This suggests that many canonical poems open with their most extreme Straussian gap — establishing the poem's register of surprise immediately. The conventional view that poems "build to a climax" does not match the information-theoretic signature; more poems front-load their maximum surprise.

**The 'the' displacement hypothesis**: The single most common suppressed prediction at peak moments is the definite article "the." Poets achieve their highest surprise by placing a content word exactly where the most neutral, invisible grammatical word would go. The maximum Straussian gap is the moment when the poet refuses the article.

---

## Suggested Next Steps

1. **Opening bomb analysis**: Compare poems where the peak falls in the first vs. last third — do they differ in other literary features (form, length, era, avg S₂)?
2. **"The" displacement taxonomy**: Collect all cases where the suppressed prediction is "the" and characterize the content word chosen instead — are there semantic patterns?
3. **Bishop's "badly"**: This is a singular moment — the word that breaks the formal contract of the villanelle. Analyze One Art token-by-token for how the S₂ profile traces the form's mounting control, then its deliberate break.
4. **Smart's "prank"**: The two Christopher Smart peaks (ranks 7 and 11) point to the catalogue poem as a generator of extreme ambush events. Run a focused study on the catalogue genre.
5. **Peak timing by form**: Does the sonnet volta correlate with the peak position? Do ballads peak at the narrative turn?
