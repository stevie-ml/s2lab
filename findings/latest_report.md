# S₂ Lab Research Report
**Generated:** 2026-10-30 13:01:50
**Corpus:** 381 texts analyzed with GPT-2
**Model:** gpt2 (117M parameters)

---

## Experiment: S₂ by Literary Era

Do different literary movements produce systematically different information-theoretic signatures?

> ⚠️ **Stanza-break artifact:** Columns show raw S₂ and artifact-free S₂ (p(newline) < 0.9 tokens only). See `findings/stanza_break_artifact.md`. Rankings in the clean column are more reliable.

| Era | n | Avg S₂ (raw) | Avg S₂ (clean) | +S₂ Ratio | Max S₂ |
|---|---|---|---|---|---|
| haiku | 14 | 1.63 | **-0.11** | 42% | 39.62 |
| clerihew | 10 | 1.55 | **0.51** | 46% | 28.21 |
| concrete | 3 | 1.51 | **-0.50** | 25% | 30.95 |
| double_dactyl | 5 | 1.21 | **-0.95** | 36% | 39.00 |
| mid_century | 4 | 1.20 | **-0.60** | 37% | 36.38 |
| german_modernist | 2 | 1.12 | **0.63** | 46% | 17.49 |
| villanelle | 2 | 1.11 | **-0.80** | 28% | 30.18 |
| persian | 2 | 0.84 | **-0.23** | 40% | 30.32 |
| ballad | 6 | 0.81 | **-0.42** | 32% | 32.75 |
| parody | 4 | 0.80 | **-0.29** | 39% | 38.37 |
| modernist | 27 | 0.78 | **-0.35** | 39% | 39.17 |
| korean_modernist | 1 | 0.75 | **-0.69** | 31% | 30.95 |
| imagist | 5 | 0.70 | **-0.52** | 42% | 28.35 |
| parody_original | 3 | 0.65 | **-0.45** | 36% | 29.30 |
| black_arts | 1 | 0.65 | **-0.50** | 36% | 27.57 |
| nonsense | 2 | 0.62 | **-0.69** | 32% | 32.61 |
| fixed_form | 8 | 0.60 | **-0.56** | 34% | 30.18 |
| ghazal | 2 | 0.58 | **-0.46** | 34% | 35.04 |
| confessional | 6 | 0.50 | **-0.23** | 41% | 35.23 |
| postcolonial | 6 | 0.49 | **-0.48** | 32% | 36.66 |
| harlem_renaissance | 6 | 0.49 | **-0.38** | 38% | 31.07 |
| beat | 6 | 0.46 | **0.07** | 32% | 36.66 |
| german_expressionist | 6 | 0.44 | **0.10** | 41% | 28.16 |
| german_symbolist | 3 | 0.42 | **0.45** | 45% | 23.40 |
| rondeau | 1 | 0.39 | **-0.40** | 37% | 25.08 |
| victorian | 29 | 0.38 | **-0.32** | 38% | 34.00 |
| protest_political | 2 | 0.36 | **-0.75** | 36% | 34.25 |
| contemporary | 16 | 0.35 | **-0.40** | 36% | 33.21 |
| elegy | 8 | 0.29 | **-0.45** | 36% | 34.93 |
| 19th_century | 17 | 0.29 | **-0.46** | 39% | 35.25 |
| deep_image | 1 | 0.25 | **0.07** | 45% | 12.62 |
| oulipo | 7 | 0.21 | **-0.05** | 37% | 31.24 |
| romantic | 21 | 0.19 | **-0.44** | 36% | 33.80 |
| war_poetry | 3 | 0.19 | **-0.34** | 41% | 33.05 |
| surrealist | 8 | 0.16 | **-0.50** | 34% | 37.05 |
| ancient | 3 | 0.11 | **-0.20** | 41% | 24.76 |
| nursery_rhyme | 1 | 0.10 | **-0.82** | 32% | 26.92 |
| song_lyrics | 3 | 0.09 | **-0.68** | 25% | 29.34 |
| early_modern | 7 | 0.09 | **-0.39** | 39% | 31.07 |
| latin_american | 4 | 0.08 | **-0.48** | 33% | 36.73 |
| pantoum | 1 | 0.07 | **-0.50** | 37% | 20.85 |
| cliche_control | 3 | -0.03 | **-0.87** | 28% | 28.76 |
| ekphrastic | 8 | -0.04 | **-0.51** | 38% | 33.65 |
| limerick | 10 | -0.06 | **-0.66** | 32% | 22.11 |
| old_english | 5 | -0.07 | **-0.31** | 40% | 34.24 |
| dramatic_monologue | 7 | -0.09 | **-0.36** | 36% | 24.44 |
| japanese_classical | 2 | -0.15 | **-0.71** | 38% | 17.39 |
| 18th_century | 8 | -0.17 | **-0.29** | 35% | 22.18 |
| metaphysical | 4 | -0.17 | **-0.65** | 38% | 27.32 |
| spoken_word | 3 | -0.17 | **-0.59** | 32% | 27.73 |
| prose_poetry | 12 | -0.18 | **-0.47** | 34% | 34.59 |
| new_york_school | 20 | -0.19 | **-0.56** | 36% | 29.70 |
| found_poetry | 8 | -0.19 | **-0.62** | 29% | 28.70 |
| language | 6 | -0.21 | **-0.66** | 33% | 35.40 |
| classical_chinese | 4 | -0.22 | **-0.56** | 35% | 20.15 |
| biblical | 8 | -0.39 | **-0.45** | 31% | 21.23 |
| triolet | 2 | -0.44 | **-0.75** | 25% | 16.00 |
| control | 5 | -1.66 | **-1.72** | 20% | 12.11 |

### Finding
After removing stanza-break artifact positions, **german_modernist** has the highest artifact-free avg S₂ (0.63), while **double_dactyl** is lowest among poetry (-0.95). Prose control: -1.72.
Only 6 of 57 poetry eras have positive artifact-free avg S₂ — **most era averages are negative once cleaned** (the artifact inflated them).
The core claim survives: **poetry is less statistically conformist than prose** (gap = 1.31 bits artifact-free), but the absolute positive-S₂ framing does not hold.

---

## Experiment: Taxonomy of the Unsaid

What does GPT-2 expect when poets deviate? Can we categorize the 'unsaid'?

### What GPT-2 expected at the top 50 highest-S₂ moments:

| Category | Count | % |
|---|---|---|
| newline expected | 49 | 98% |
| content word expected | 1 | 2% |
| punctuation expected | 0 | 0% |
| function word expected | 0 | 0% |
| pronoun expected | 0 | 0% |
| verb expected | 0 | 0% |

### Most striking substitutions (S₂ > 5):

- **Kobayashi Issa**, "Three Haiku (Issa, translated)":
  - Context: `... keep house
` → poet wrote **"cas"**
  - GPT-2 expected: "" (99.9%)
  - S₂ = 39.62

- **Marianne Moore**, "The Fish":
  - Context: `...sun,
` → poet wrote **"split"**
  - GPT-2 expected: "" (99.9%)
  - S₂ = 39.17

- **Synthetic (double dactyl test case)**, "Alfred Lord Tennyson (Double Dactyl)":
  - Context: `...ically—
` → poet wrote **"Death"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 39.00

- **William Carlos Williams**, "This Is Just to Say":
  - Context: `... were probably
` → poet wrote **"saving"**
  - GPT-2 expected: "" (99.9%)
  - S₂ = 38.55

- **William Carlos Williams**, "This Is Just to Say":
  - Context: `... were probably
` → poet wrote **"saving"**
  - GPT-2 expected: "" (99.9%)
  - S₂ = 38.55

- **Lewis Carroll**, "You Are Old, Father William":
  - Context: `... box—
` → poet wrote **"Allow"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 38.37

- **Lewis Carroll**, "You Are Old, Father William":
  - Context: `... enough,
` → poet wrote **"Said"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 37.22

- **Arthur Rimbaud**, "The Sleeper in the Valley":
  - Context: `...apping:
` → poet wrote **"Nature"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 37.05

- **Pablo Neruda (trans. W.S. Merwin)**, "Tonight I Can Write (excerpt)":
  - Context: `... sings.
` → poet wrote **"Tonight"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 36.73

- **Kamau Brathwaite**, "Calypso":
  - Context: `...argasso
` → poet wrote **"rolled"**
  - GPT-2 expected: "" (99.9%)
  - S₂ = 36.66

- **Lawrence Ferlinghetti**, "In Goya's greatest scenes":
  - Context: `...   ` → poet wrote **"gro"**
  - GPT-2 expected: "" (99.7%)
  - S₂ = 36.66

- **Gwendolyn Brooks**, "We Real Cool":
  - Context: `.... We
` → poet wrote **"Die"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 36.38

- **Gwendolyn Brooks**, "We Real Cool":
  - Context: `.... We
` → poet wrote **"Die"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 36.38

- **Paul Éluard**, "The Curve of Your Eyes":
  - Context: `...ense,
` → poet wrote **"wings"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 35.56

- **Synthetic (double dactyl test case)**, "William Carlos Williams (Double Dactyl)":
  - Context: `... particular—
` → poet wrote **"Exper"**
  - GPT-2 expected: "" (100.0%)
  - S₂ = 35.43

### Finding
The 'unsaid' falls into distinct categories. When poets deviate most sharply from expectation, the model's top prediction reveals what *conventional* language would do in that position. This makes the poet's choice legible as a *decision* — not random noise, but a deliberate suppression of the expected in favor of something the poet needed to say.

---

## Experiment: Structural Position of High S₂

Do high-S₂ moments cluster at beginnings, endings, or enjambments?

| Position in poem | Avg S₂ | Median S₂ | n tokens |
|---|---|---|---|
| first_10% | 0.87 | -0.63 | 5021 |
| 10-25% | 0.17 | -1.11 | 7798 |
| 25-50% | 0.11 | -1.04 | 13025 |
| 50-75% | 0.10 | -1.02 | 12928 |
| 75-90% | 0.34 | -0.89 | 7753 |
| last_10% | 0.16 | -1.02 | 5355 |

### Line break analysis:
- Avg S₂ at newline tokens: **-1.64** (n=4912)
- Avg S₂ at tokens immediately after newline (raw): **6.58** (n=4912)
- Avg S₂ at tokens immediately after newline (**artifact-free**): **0.10** (n=3065)
- Avg S₂ at all other tokens: **0.43** (n=46968)

> ⚠️ The raw post-newline figure is dominated by the stanza-break artifact (see `findings/stanza_break_artifact.md`). The artifact-free value is near-zero. **The enjambment finding does not survive artifact removal.**

### Finding
Artifact-free post-newline S₂ = 0.10 vs other tokens = 0.43. Line-head tokens are at or below baseline once artifact positions are removed. The Straussian gap is distributed throughout the poem, not concentrated at line breaks.

---

## Experiment: Author Information Signatures

Does each poet have a distinctive information-theoretic fingerprint?

| Author | n poems | Avg S₂ | S₂ σ | +S₂% | Avg Max S₂ | Style |
|---|---|---|---|---|---|---|
| William Carlos Williams | 4 | 3.10 | 10.12 | 45% | 34.86 | high spikes, volatile |
| Carl Sandburg | 2 | 2.54 | 7.95 | 45% | 27.90 | high spikes, volatile |
| Gwendolyn Brooks | 2 | 2.18 | 9.84 | 38% | 36.38 | high spikes, volatile |
| Masaoka Shiki | 2 | 1.96 | 6.87 | 45% | 25.09 | high spikes, volatile |
| Synthetic (clerihew test case) | 7 | 1.68 | 6.45 | 49% | 24.60 | high spikes, volatile |
| Synthetic (scientific register test case) | 3 | 1.60 | 7.19 | 42% | 31.46 | high spikes, volatile |
| E.E. Cummings | 3 | 1.58 | 7.82 | 31% | 27.58 | high spikes, volatile |
| Matsuo Bashō | 4 | 1.51 | 6.58 | 38% | 19.33 | high spikes, volatile |
| Edwin Arlington Robinson | 2 | 1.46 | 6.61 | 36% | 26.94 | high spikes, volatile |
| Edmund Clerihew Bentley | 3 | 1.25 | 5.94 | 40% | 20.08 | consistently deviant |
| Synthetic (double dactyl test case) | 5 | 1.21 | 8.35 | 36% | 34.19 | high spikes, volatile |
| Kobayashi Issa | 3 | 1.15 | 7.51 | 39% | 27.52 | high spikes, volatile |
| Rainer Maria Rilke | 2 | 1.12 | 4.24 | 46% | 17.09 | consistently deviant |
| Langston Hughes | 3 | 1.09 | 7.15 | 36% | 27.66 | high spikes, volatile |
| Christian Bök | 2 | 1.05 | 5.13 | 48% | 15.55 | consistently deviant |
| Thomas Hardy | 6 | 1.04 | 5.92 | 44% | 28.64 | consistently deviant |
| Allen Ginsberg | 2 | 1.03 | 5.23 | 47% | 19.80 | consistently deviant |
| Sylvia Plath | 2 | 0.95 | 6.92 | 38% | 25.82 | high spikes, volatile |
| Agha Shahid Ali | 2 | 0.89 | 6.44 | 40% | 29.66 | high spikes, volatile |
| Omar Khayyam (trans. FitzGerald, 1859) | 2 | 0.84 | 6.13 | 40% | 30.17 | high spikes, volatile |
| Ernest Dowson | 2 | 0.79 | 7.47 | 24% | 30.18 | high spikes, volatile |
| Traditional (Scottish ballad) | 5 | 0.76 | 6.09 | 31% | 29.02 | high spikes, volatile |
| William Ernest Henley | 2 | 0.75 | 6.36 | 33% | 27.27 | high spikes, volatile |
| Lewis Carroll | 5 | 0.68 | 6.35 | 35% | 30.55 | high spikes, volatile |
| Emily Dickinson | 7 | 0.68 | 5.55 | 40% | 24.00 | consistently deviant |
| Georg Trakl | 2 | 0.62 | 3.97 | 45% | 14.57 | consistently deviant |
| Heather McHugh | 2 | 0.58 | 6.24 | 34% | 32.85 | high spikes, volatile |
| Marianne Moore | 2 | 0.57 | 5.56 | 39% | 28.36 | consistently deviant |
| Yosa Buson | 2 | 0.56 | 5.42 | 43% | 16.78 | consistently deviant |
| Joy Harjo | 3 | 0.56 | 5.72 | 28% | 29.51 | consistently deviant |
| Isaac Watts | 2 | 0.49 | 5.97 | 37% | 27.01 | selective spikes |
| Thomas Wyatt | 2 | 0.48 | 4.59 | 44% | 21.84 | mild deviation |
| Gerard Manley Hopkins | 6 | 0.46 | 5.47 | 39% | 26.67 | selective spikes |
| Robert Frost | 2 | 0.45 | 4.96 | 38% | 26.00 | mild deviation |
| Gregory Corso | 2 | 0.43 | 4.84 | 39% | 23.35 | mild deviation |
| Edward Lear | 3 | 0.43 | 5.05 | 36% | 19.90 | selective spikes |
| Stefan George | 3 | 0.42 | 3.77 | 45% | 17.80 | mild deviation |
| Georg Heym | 2 | 0.40 | 4.46 | 44% | 16.34 | mild deviation |
| Robert Burns | 2 | 0.39 | 5.98 | 35% | 24.00 | selective spikes |
| Frank O'Hara | 3 | 0.36 | 4.75 | 37% | 21.83 | mild deviation |
| Gottfried Benn | 2 | 0.29 | 4.95 | 35% | 25.66 | mild deviation |
| Alfred Lord Tennyson | 3 | 0.27 | 5.19 | 37% | 24.68 | selective spikes |
| Dante Gabriel Rossetti | 2 | 0.27 | 4.96 | 41% | 23.02 | mild deviation |
| George Herbert | 2 | 0.26 | 5.01 | 39% | 21.56 | selective spikes |
| Adelaide Crapsey | 2 | 0.24 | 5.31 | 44% | 20.89 | selective spikes |
| Alfred, Lord Tennyson | 5 | 0.19 | 5.20 | 33% | 28.62 | selective spikes |
| Pablo Neruda | 2 | 0.16 | 4.55 | 35% | 19.17 | mild deviation |
| Edgar Allan Poe | 2 | 0.15 | 6.05 | 32% | 32.50 | selective spikes |
| Algernon Charles Swinburne | 2 | 0.15 | 4.48 | 40% | 25.45 | mild deviation |
| William Blake | 7 | 0.13 | 5.26 | 32% | 23.97 | selective spikes |
| John Keats | 9 | 0.13 | 4.84 | 38% | 24.11 | mild deviation |
| Wallace Stevens | 3 | 0.13 | 4.98 | 36% | 21.37 | mild deviation |
| Percy Bysshe Shelley | 4 | 0.11 | 4.57 | 38% | 22.51 | mild deviation |
| Rudyard Kipling | 2 | 0.10 | 5.42 | 33% | 26.30 | selective spikes |
| Alexander Pope | 4 | 0.09 | 4.31 | 39% | 20.58 | mild deviation |
| Wilfred Owen | 2 | 0.08 | 4.64 | 38% | 24.66 | mild deviation |
| Matthew Arnold | 2 | 0.05 | 4.16 | 39% | 17.07 | mild deviation |
| John Milton | 2 | 0.03 | 4.33 | 39% | 22.55 | mild deviation |
| T.S. Eliot | 5 | 0.02 | 4.42 | 39% | 21.03 | mild deviation |
| Austin Dobson | 2 | 0.01 | 4.77 | 30% | 18.61 | mild deviation |
| Claudia Rankine | 2 | -0.00 | 4.25 | 36% | 18.16 | smooth/conventional |
| Walt Whitman | 9 | -0.02 | 4.49 | 37% | 21.14 | smooth/conventional |
| John Donne | 2 | -0.03 | 4.85 | 35% | 24.90 | smooth/conventional |
| Anonymous (found text) | 4 | -0.03 | 4.39 | 29% | 25.26 | smooth/conventional |
| Synthetic (research test case) | 3 | -0.03 | 5.07 | 28% | 24.70 | volatile but conforming |
| Christina Rossetti | 2 | -0.04 | 3.74 | 35% | 20.49 | smooth/conventional |
| W.B. Yeats | 3 | -0.04 | 4.55 | 38% | 24.46 | smooth/conventional |
| Robert Browning | 7 | -0.04 | 4.10 | 38% | 22.43 | smooth/conventional |
| Lawrence Ferlinghetti | 2 | -0.08 | 3.94 | 11% | 32.46 | smooth/conventional |
| Amy Lowell | 2 | -0.12 | 4.57 | 36% | 20.88 | smooth/conventional |
| Countee Cullen | 2 | -0.13 | 4.02 | 41% | 17.61 | smooth/conventional |
| Anonymous | 3 | -0.13 | 4.55 | 34% | 20.21 | smooth/conventional |
| Anne Sexton | 2 | -0.14 | 4.92 | 39% | 21.88 | smooth/conventional |
| Anonymous (trans. Hall) | 2 | -0.27 | 3.98 | 37% | 15.65 | smooth/conventional |
| John Ashbery | 16 | -0.28 | 4.47 | 36% | 20.23 | smooth/conventional |
| Gertrude Stein | 4 | -0.29 | 3.99 | 33% | 14.94 | smooth/conventional |
| Georges Perec | 2 | -0.31 | 3.59 | 34% | 13.39 | smooth/conventional |
| Christopher Smart | 2 | -0.35 | 3.37 | 30% | 22.07 | smooth/conventional |
| Lucille Clifton | 3 | -0.36 | 3.91 | 31% | 20.07 | smooth/conventional |
| Ben Jonson | 2 | -0.37 | 3.84 | 36% | 18.29 | smooth/conventional |
| Russell Edson | 2 | -0.39 | 3.20 | 30% | 12.25 | smooth/conventional |
| Anonymous (Hebrew Bible) | 7 | -0.42 | 3.60 | 32% | 16.15 | smooth/conventional |
| Anonymous (limerick tradition) | 3 | -0.49 | 4.51 | 25% | 19.40 | smooth/conventional |
| Charles Bernstein | 2 | -0.61 | 3.73 | 30% | 17.25 | smooth/conventional |
| William Shakespeare | 3 | -0.62 | 3.51 | 30% | 19.15 | smooth/conventional |

### Finding
Authors have distinct S₂ signatures. Some poets (like Plath, Ginsberg) produce high-spike, volatile profiles — concentrated moments of extreme deviation. Others (like Ashbery) produce more evenly distributed deviation. This suggests different *strategies* for managing reader expectation.

---

## Experiment: S₂ and Poetic Impact

Do 'great' poems have distinctive S₂ profiles?

> ⚠️ **Stanza-break artifact:** Raw S₂ numbers are inflated by layout positions. See `findings/stanza_break_artifact.md` for details.

- Poetry avg S₂ (raw): **0.36** (σ=0.87, n=376)
- Control prose avg S₂ (raw): **-1.66** (σ=0.67, n=5)
- Gap (raw): **2.02**

- Poetry avg S₂ (artifact-free): **-0.401**
- Control prose avg S₂ (artifact-free): **-1.721**
- Gap (artifact-free): **1.320** (65% of raw gap survives)

- Poetry: 36% of tokens have positive S₂ (raw)
- Control prose: 20% of tokens have positive S₂ (raw)

### Highest S₂ poems (artifact-free):
1. **Chiyo-ni** — "Morning Glory (Chiyo-ni, translated)" (S₂ clean=2.08, raw=4.16)
1. **Synthetic (clerihew test case)** — "Nikola Tesla" (S₂ clean=1.89, raw=2.59)
1. **Christian Bök** — "Eunoia: Chapter E (excerpt)" (S₂ clean=1.77, raw=1.93)
1. **Richard Wright** — "Nobody (Wright)" (S₂ clean=1.33, raw=2.03)
1. **Rainer Maria Rilke** — "Die erste Elegie (Eröffnung)" (S₂ clean=1.25, raw=1.67)

### Lowest S₂ poems (artifact-free):
1. **Synthetic (double dactyl test case)** — "Alfred Lord Tennyson (Double Dactyl)" (S₂ clean=-1.38, raw=0.64)
1. **John Ashbery** — "A Wave (opening)" (S₂ clean=-1.39, raw=-1.14)
1. **E.E. Cummings** — "l(a" (S₂ clean=-1.51, raw=3.89)
1. **Pierre Reverdy** — "Departure" (S₂ clean=-1.58, raw=0.19)
1. **Kobayashi Issa** — "The World of Dew (Issa, translated)" (S₂ clean=-2.14, raw=-0.18)

### Finding
The poetry–prose gap is real and survives artifact removal. Poetry is measurably less statistically conformist than prose — **poetry is the art of saying what wasn't expected.** However, artifact-free avg S₂ is *negative* for most poetry eras and poems individually (the few extreme S₂ spikes lift the mean slightly, but the median token is below baseline). The absolute positive-S₂ framing from earlier reports was an artifact of layout positions where GPT-2 expected a stanza break and got a word instead.

---

## Experiment: Syntactic Position and S₂

Do nouns, verbs, adjectives, and function words have systematically different S₂ values in poetry vs prose?

*Syntactic position experiment skipped: No module named 'nltk'*

---
