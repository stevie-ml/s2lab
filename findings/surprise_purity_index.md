# Surprise Purity Index: Measuring the Quality of the Straussian Gap

**Date:** 2026-10-31  
**Experiment:** `experiments/surprise_purity_index.py`  
**Corpus:** 86 poets (≥2 poems), 49,373 artifact-free tokens  

---

## Research Question

Not all high-S₂ moments are equal. The S₂ formula is:

> **S₂ = S − H**  (surprisal minus entropy)

When entropy H is *high*, the model is already confused — any unusual token will
generate positive S₂ without the model having made a strong prediction.
When entropy H is *low*, the model was *confident* about what came next —
so a high-S₂ token represents a genuine defiance of expectation.

**Surprise Purity Index (SPI)** = fraction of high-S₂ tokens (S₂ ≥ 3.0) that occur
in *low-entropy* contexts (model was confident). It measures whether a poet achieves
Straussian surprise efficiently — defying confident predictions — or mainly operates
in semantic territory where the model was confused anyway.

---

## Setup

- High-S₂ threshold: S₂ ≥ 3.0
- Artifact filter: p(newline) < 0.9
- Low-entropy (confident) threshold: H < 5.086 bits (33rd percentile of all token entropies)

---

## Corpus-Level Results

- Total artifact-free tokens: **49,373**
- High-S₂ tokens (S₂ ≥ 3.0): **7,842** (15.9%)
- High-S₂ in confident contexts: **2,017** (25.7% of high-S₂ tokens)
- **Overall SPI: 0.2572** — only 26% of high-S₂ moments occur when the model was confident

This means **74% of surface-level 'surprises' occur in already-uncertain contexts** — the model was confused regardless.
True Straussian defiance of confident expectation is rare.

---

## Results by Era

| Era | N | Mean SPI | Mean avg_S₂ |
|-----|---|----------|-------------|
| found_poetry | 8 | **0.472** | -0.192 |
| prose_poetry | 12 | **0.452** | -0.180 |
| nursery_rhyme | 1 | **0.452** | 0.104 |
| control | 3 | **0.444** | -1.487 |
| song_lyrics | 3 | **0.419** | 0.092 |
| biblical | 8 | **0.375** | -0.391 |
| double_dactyl | 5 | **0.373** | 1.213 |
| contemporary | 16 | **0.369** | 0.349 |
| imagist | 5 | **0.360** | 0.702 |
| rondeau | 1 | **0.353** | 0.391 |
| beat | 6 | **0.350** | 0.460 |
| oulipo | 7 | **0.344** | 0.211 |
| postcolonial | 6 | **0.344** | 0.492 |
| haiku | 14 | **0.343** | 1.632 |
| black_arts | 1 | **0.333** | 0.650 |
| cliche_control | 3 | **0.331** | -0.034 |
| parody_original | 3 | **0.317** | 0.651 |
| language | 6 | **0.305** | -0.206 |
| ghazal | 2 | **0.301** | 0.575 |
| ballad | 6 | **0.294** | 0.814 |
| classical_chinese | 4 | **0.292** | -0.218 |
| surrealist | 8 | **0.286** | 0.162 |
| fixed_form | 8 | **0.281** | 0.599 |
| mid_century | 4 | **0.281** | 1.198 |
| parody | 4 | **0.278** | 0.805 |
| spoken_word | 3 | **0.271** | -0.174 |
| 19th_century | 17 | **0.267** | 0.286 |
| german_symbolist | 3 | **0.258** | 0.419 |
| new_york_school | 20 | **0.249** | -0.189 |
| villanelle | 2 | **0.242** | 1.108 |
| ancient | 3 | **0.240** | 0.113 |
| harlem_renaissance | 6 | **0.237** | 0.492 |
| german_modernist | 2 | **0.236** | 1.121 |
| victorian | 29 | **0.220** | 0.382 |
| elegy | 8 | **0.217** | 0.294 |
| latin_american | 4 | **0.216** | 0.081 |
| dramatic_monologue | 7 | **0.216** | -0.092 |
| protest_political | 2 | **0.212** | 0.356 |
| concrete | 3 | **0.212** | 1.510 |
| limerick | 10 | **0.206** | -0.062 |
| confessional | 6 | **0.203** | 0.503 |
| german_expressionist | 6 | **0.203** | 0.440 |
| japanese_classical | 2 | **0.200** | -0.151 |
| triolet | 2 | **0.200** | -0.438 |
| ekphrastic | 8 | **0.199** | -0.044 |
| modernist | 27 | **0.199** | 0.778 |
| romantic | 21 | **0.195** | 0.192 |
| war_poetry | 3 | **0.191** | 0.189 |
| old_english | 5 | **0.187** | -0.073 |
| early_modern | 7 | **0.173** | 0.089 |
| 18th_century | 8 | **0.169** | -0.171 |
| pantoum | 1 | **0.167** | 0.069 |
| nonsense | 2 | **0.153** | 0.621 |
| metaphysical | 4 | **0.142** | -0.171 |
| persian | 2 | **0.138** | 0.842 |
| clerihew | 10 | **0.129** | 1.552 |
| deep_image | 1 | **0.067** | 0.251 |
| korean_modernist | 1 | **0.062** | 0.749 |

---

## Results by Poet (≥2 poems)

### Highest SPI (pure surprise specialists)

| Author | Era | N | SPI | avg_S₂ |
|--------|-----|---|-----|--------|
| Kobayashi Issa | haiku | 3 | **0.667** | 1.153 |
| Anonymous (found text) | found_poetry | 4 | **0.553** | -0.033 |
| Russell Edson | prose_poetry | 2 | **0.528** | -0.387 |
| Lawrence Ferlinghetti | beat | 2 | **0.496** | -0.080 |
| Charles Bernstein | language | 2 | **0.483** | -0.607 |
| Control | control | 3 | **0.444** | -1.487 |
| Joy Harjo | postcolonial | 3 | **0.438** | 0.557 |
| Claudia Rankine | contemporary | 2 | **0.408** | -0.002 |
| Frank O'Hara | new_york_school | 3 | **0.405** | 0.362 |
| Synthetic (scientific register test case) | contemporary | 3 | **0.399** | 1.600 |
| Georges Perec | oulipo | 2 | **0.393** | -0.310 |
| Marianne Moore | modernist | 2 | **0.385** | 0.566 |
| Adelaide Crapsey | imagist | 2 | **0.375** | 0.242 |
| Synthetic (double dactyl test case) | double_dactyl | 5 | **0.373** | 1.213 |
| Edwin Arlington Robinson | fixed_form | 2 | **0.367** | 1.458 |
| Matsuo Bashō | haiku | 4 | **0.362** | 1.506 |
| Christina Rossetti | victorian | 2 | **0.356** | -0.036 |
| Anonymous (Hebrew Bible) | biblical | 7 | **0.353** | -0.416 |
| Pablo Neruda | surrealist | 2 | **0.352** | 0.159 |
| Isaac Watts | parody_original | 2 | **0.341** | 0.491 |

### Lowest SPI (noisy surprisers)

| Author | Era | N | SPI | avg_S₂ |
|--------|-----|---|-----|--------|
| Edmund Clerihew Bentley | clerihew | 3 | **0.000** | 1.250 |
| Ben Jonson | early_modern | 2 | **0.071** | -0.369 |
| Carl Sandburg | modernist | 2 | **0.083** | 2.540 |
| Ernest Dowson | fixed_form | 2 | **0.083** | 0.788 |
| Yosa Buson | haiku | 2 | **0.083** | 0.560 |
| William Carlos Williams | modernist | 4 | **0.083** | 3.103 |
| Alexander Pope | parody | 4 | **0.095** | 0.094 |
| Anonymous (limerick tradition) | limerick | 3 | **0.111** | -0.486 |
| Anonymous (trans. Hall) | old_english | 2 | **0.116** | -0.266 |
| John Donne | metaphysical | 2 | **0.117** | -0.025 |
| Omar Khayyam (trans. FitzGerald, 1859) | persian | 2 | **0.138** | 0.842 |
| Algernon Charles Swinburne | ekphrastic | 2 | **0.138** | 0.148 |
| John Milton | victorian | 2 | **0.140** | 0.028 |
| Alfred Lord Tennyson | victorian | 3 | **0.141** | 0.273 |
| John Keats | romantic | 9 | **0.144** | 0.131 |
| Gottfried Benn | german_expressionist | 2 | **0.151** | 0.294 |
| George Herbert | metaphysical | 2 | **0.151** | 0.260 |
| Gwendolyn Brooks | mid_century | 2 | **0.167** | 2.181 |
| William Shakespeare | victorian | 3 | **0.171** | -0.618 |
| Wilfred Owen | war_poetry | 2 | **0.171** | 0.081 |

---

## The Four Quadrants of Surprise Quality

Using global means as thresholds (avg_S₂ = 0.418, SPI = 0.258):

| Quadrant | Description | Poets |
|----------|-------------|-------|
| **High S₂ + High SPI** (Pure Surprise Specialists) | Surprise the model often AND efficiently | Kobayashi Issa, Joy Harjo, Synthetic (scientific register test case), Marianne Moore, Synthetic (double dactyl test case), Edwin Arlington Robinson, Matsuo Bashō, Isaac Watts |
| **High S₂ + Low SPI** (Noisy Surprisers) | Many high-S₂ tokens but in uncertain contexts | Lewis Carroll, Robert Frost, Sylvia Plath, Rainer Maria Rilke, Edward Lear, Agha Shahid Ali, Emily Dickinson, Thomas Hardy |
| **Low S₂ + High SPI** (Strategic Minimalists) | Rare surprises, but always when model was confident | Anonymous (found text), Russell Edson, Lawrence Ferlinghetti, Charles Bernstein, Control, Claudia Rankine, Frank O'Hara, Georges Perec |
| **Low S₂ + Low SPI** (Conventional) | Rare surprises, mostly in uncertain contexts | Walt Whitman, Amy Lowell, Rudyard Kipling, William Blake, Percy Bysshe Shelley, Robert Browning, T.S. Eliot, Dante Gabriel Rossetti |

---

## Top 15 Poems by SPI

| Title | Author | Era | SPI | High-S₂ count | avg_S₂ |
|-------|--------|-----|-----|---------------|--------|
| Self-Evident Truths (Found Poem from Declarat | Thomas Jefferson (found t | found_poetry | **0.786** | 14 | 0.097 |
| On the Roof of Hell (Issa, translated) | Kobayashi Issa | haiku | **0.750** | 4 | 1.615 |
| Cooking Instructions (Found Poem from generic | Anonymous (found text) | found_poetry | **0.750** | 8 | -0.601 |
| Crossing (excerpt) | Rae Armantrout | prose_poetry | **0.733** | 15 | -0.333 |
| Yesterday (prose poem) | W.S. Merwin | prose_poetry | **0.714** | 7 | -1.026 |
| Remember | Joy Harjo | postcolonial | **0.677** | 31 | -0.281 |
| Night Sky with Exit Wounds (excerpt) | Ocean Vuong | contemporary | **0.667** | 3 | -0.084 |
| Terms and Conditions (Found Poem from generic | Anonymous (found text) | found_poetry | **0.667** | 18 | 0.354 |
| Alfred Lord Tennyson (Double Dactyl) | Synthetic (double dactyl  | double_dactyl | **0.667** | 3 | 0.639 |
| For Spacious Skies | Emmett Williams | concrete | **0.636** | 11 | 0.806 |
| Constantly Risking Absurdity | Lawrence Ferlinghetti | beat | **0.632** | 19 | -0.077 |
| One Art | Elizabeth Bishop | mid_century | **0.625** | 8 | 1.216 |
| There Was a Young Man of Japan | Anonymous | limerick | **0.625** | 8 | 0.542 |
| The Listeners | Walter de la Mare | 19th_century | **0.600** | 20 | -0.136 |
| If I Told Him: A Completed Portrait of Picass | Gertrude Stein | oulipo | **0.600** | 40 | 0.153 |

## Bottom 15 Poems by SPI

| Title | Author | Era | SPI | High-S₂ count | avg_S₂ |
|-------|--------|-----|-----|---------------|--------|
| The Sick Rose | William Blake | romantic | **0.000** | 3 | -0.951 |
| Song: To Celia | Ben Jonson | early_modern | **0.000** | 7 | -0.704 |
| Fog | Carl Sandburg | modernist | **0.000** | 7 | 3.958 |
| l(a | E.E. Cummings | concrete | **0.000** | 3 | 3.890 |
| Western Wind (anonymous lyric) | Anonymous (English, c. 15 | early_modern | **0.000** | 4 | -0.080 |
| 'Tis the Voice of the Lobster | Lewis Carroll | parody | **0.000** | 10 | -0.426 |
| There Was an Old Man of Nantucket | Anonymous (limerick tradi | limerick | **0.000** | 6 | -0.345 |
| A Limerick on Time | Anonymous (limerick tradi | limerick | **0.000** | 4 | -0.402 |
| A Flea and a Fly in a Flue | Anonymous | limerick | **0.000** | 3 | -0.736 |
| An Essay on Criticism (opening) | Alexander Pope | 18th_century | **0.000** | 25 | -0.145 |
| Sir Humphrey Davy | Edmund Clerihew Bentley | clerihew | **0.000** | 6 | 2.306 |
| The Art of Biography | Edmund Clerihew Bentley | clerihew | **0.000** | 3 | -0.440 |
| Oscar Wilde | Edmund Clerihew Bentley | clerihew | **0.000** | 4 | 1.883 |
| Lawrence Ferlinghetti (Double Dactyl) | Synthetic (double dactyl  | double_dactyl | **0.000** | 4 | 1.123 |
| This Is Just to Say | William Carlos Williams | modernist | **0.000** | 3 | 2.612 |

---

## Key Findings

1. **SPI is low overall (0.26)**: Most 'surprises' (S₂ ≥ 3) occur when the model is uncertain,
   not when it is confident. The truly Straussian — defiance of confident prediction — is rare.

2. **SPI and avg_S₂ correlation: r = -0.156**: Weak correlation — surprise quantity and purity are largely independent.
   This means some poets achieve high S₂ through quantity of surprises in uncertain contexts,
   while others specialize in rare, highly pure defiance.

3. **Era differences**: Fixed-form and constrained poetry (where the model builds stronger expectations)
   may show higher SPI, while Language Poetry (entropy flooding) would show near-zero SPI.

4. **The 'quality vs. quantity' trade-off**: Poets can maximize S₂ by (a) frequently surprising
   an uncertain model (low SPI, high quantity) or (b) rarely but decisively surprising a
   confident model (high SPI). These are distinct aesthetic strategies.

## Suggested Next Steps

- Correlate SPI with known 'difficulty' ratings or anthology frequency
- Examine per-poem SPI arc: does purity cluster at poem beginning/end?
- Cross-model: does GPT-2 medium show different SPI distributions (more confidence → higher SPI)?
- Test whether high-SPI moments correspond to recognized 'great lines' vs. high-S₂ noise
