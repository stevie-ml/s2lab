# Within-Poem Entropy Variance and S₂: The Trap-and-Release Mechanism

**Date:** 2026-11-26
**Corpus:** 446 poetry texts (artifact-free tokens, control excluded)

**Research Question:** Do high-S₂ poems achieve surprise through *contrast* (low-entropy context → surprise) or through *sustained uncertainty* (high entropy throughout)?

---

## Method

For each poem (artifact-filtered tokens, min 15 tokens):
- **mean_H**: average context entropy across all tokens
- **std_H**: standard deviation of entropy = within-poem entropy variance
- **CoV(H)**: coefficient of variation of entropy (std_H / mean_H) = normalized irregularity
- **trap_ratio**: among high-S₂ tokens (s2 > 2.0), fraction preceded by LOW-entropy token (H < median)
  - trap_ratio = 1.0: ALL surprises come after confident contexts ('true Straussian ambush')
  - trap_ratio = 0.0: ALL surprises come after uncertain contexts ('fog-and-leap')

---

## Corpus-Level Correlations

| Metric pair | Pearson r | Interpretation |
|---|---|---|
| std(H) vs mean S₂ | **-0.070** | Does variable entropy predict high deviation? |
| mean(H) vs mean S₂ | **0.103** | Does uncertain context predict high deviation? |
| CoV(H) vs mean S₂ | **-0.087** | Does normalized entropy irregularity predict deviation? |

*Note: n = 446 poems. r > 0.3 is moderate, r > 0.5 is strong.*

---

## 2×2 Quadrant Classification

Poems classified by whether mean S₂ and std(H) are above/below their corpus median.

- **Median S₂**: -0.415
- **Median std(H)**: 2.547

| Quadrant | n poems | Description |
|---|---|---|
| Consistent Ambush (high S₂, stable H) | 118 | — |
| Erratic Conformist (low S₂, variable H) | 117 | — |
| Metronomic (low S₂, stable H) | 106 | — |
| Trap-Release (high S₂, variable H) | 105 | — |

### Top poems in each quadrant:

**Consistent Ambush (high S₂, stable H)** (n=118):
  - Richard Wright, "Nobody (Wright)" — S₂=1.33, std(H)=2.31
  - Rainer Maria Rilke, "Die erste Elegie (Eröffnung)" — S₂=1.25, std(H)=2.18
  - Synthetic (clerihew test case), "William Topaz McGonagall" — S₂=1.16, std(H)=2.35

**Erratic Conformist (low S₂, variable H)** (n=117):
  - Lorine Niedecker, "My Life by Water" — S₂=-0.42, std(H)=3.61
  - John Keats, "On Seeing the Elgin Marbles" — S₂=-0.42, std(H)=2.75
  - Synthetic (procedural test case), "Field Notes for Living (Synthetic procedural test case V)" — S₂=-0.42, std(H)=2.78

**Metronomic (low S₂, stable H)** (n=106):
  - Robert Browning, "Andrea del Sarto" — S₂=-0.42, std(H)=2.41
  - Wilfred Owen, "Dulce et Decorum Est" — S₂=-0.42, std(H)=2.52
  - Robert Desnos, "I Have Dreamed of You So Much" — S₂=-0.43, std(H)=2.43

**Trap-Release (high S₂, variable H)** (n=105):
  - Synthetic (clerihew test case), "Nikola Tesla" — S₂=1.89, std(H)=2.87
  - Christian Bök, "Eunoia: Chapter E (excerpt)" — S₂=1.77, std(H)=2.74
  - Matsuo Bashō, "Old Pond (Bashō, translated)" — S₂=1.18, std(H)=2.75

---

## Trap-and-Release Champions (highest trap_ratio, ≥5 high-S₂ events)

| Author | Title | Era | trap_ratio | n surprises | mean S₂ | mean H |
|---|---|---|---|---|---|---|
| Wang Wei | "Deer Park (literal trans.)" | classical_chinese | **1.00** | 6 | -0.99 | 7.30 |
| Austin Dobson | "In After Days (rondeau)" | fixed_form | **0.80** | 15 | -0.70 | 7.32 |
| Percy Bysshe Shelley | "Ode to the West Wind (stanza 1)" | romantic | **0.75** | 36 | -0.37 | 7.03 |
| Synthetic (clerihew test case) | "Nikola Tesla" | clerihew | **0.75** | 8 | 1.89 | 7.15 |
| Edmund Clerihew Bentley | "Oscar Wilde" | clerihew | **0.71** | 7 | 0.57 | 7.70 |
| Synthetic (clerihew test case) | "Isaac Newton" | clerihew | **0.71** | 7 | 1.11 | 7.76 |
| Allen Ginsberg | "Howl (opening)" | beat | **0.71** | 17 | 0.95 | 6.94 |
| John Ashbery | "Self-Portrait in a Convex Mirror (middle passage)" | new_york_school | **0.69** | 16 | -0.46 | 6.99 |
| Barbara Guest | "Parachutes, My Love, Could Carry Us Higher" | new_york_school | **0.68** | 31 | -0.46 | 6.05 |
| T.S. Eliot | "The Waste Land (opening)" | modernist | **0.67** | 12 | -0.26 | 7.03 |
| W.S. Merwin | "Yesterday (prose poem)" | prose_poetry | **0.67** | 9 | -1.03 | 5.46 |
| Anonymous (limerick tradition) | "There Was an Old Man of Nantucket" | limerick | **0.67** | 6 | -1.22 | 6.31 |
| Synthetic (clerihew test case) | "James Joyce" | clerihew | **0.67** | 6 | 0.10 | 7.03 |
| A.E. Housman | "To an Athlete Dying Young" | elegy | **0.66** | 29 | 0.06 | 6.77 |
| Georges Perec | "The Lipogram: A Sentence Without the Letter E" | oulipo | **0.65** | 23 | -0.60 | 5.76 |

## Fog-and-Leap Champions (lowest trap_ratio, ≥5 high-S₂ events)

| Author | Title | Era | trap_ratio | n surprises | mean S₂ | mean H |
|---|---|---|---|---|---|---|
| Pierre Reverdy | "Departure" | surrealist | **0.00** | 6 | -1.58 | 6.78 |
| Synthetic (double dactyl test case) | "Emily Dickinson (Double Dactyl)" | double_dactyl | **0.12** | 8 | -1.17 | 6.90 |
| Austin Dobson | "A Kiss" | triolet | **0.14** | 7 | -0.63 | 4.27 |
| Lawrence Ferlinghetti | "In Goya's greatest scenes" | beat | **0.17** | 29 | -0.14 | 2.47 |
| Richard Wright | "Nobody (Wright)" | haiku | **0.20** | 5 | 1.33 | 7.16 |
| Anonymous | "There Was a Young Man of Japan" | limerick | **0.20** | 10 | 0.15 | 5.36 |
| Matsuo Basho | "Three Haiku (Basho, translated)" | haiku | **0.21** | 14 | -0.31 | 6.76 |
| Traditional (American sea chanty) | "Oh Shenandoah" | song_lyrics | **0.22** | 23 | -0.34 | 3.01 |
| Anonymous (KJV translation) | "Psalm 136 (KJV)" | biblical | **0.23** | 53 | -0.23 | 2.83 |
| Wislawa Szymborska | "Possibilities" | contemporary | **0.23** | 26 | -0.37 | 5.46 |
| Anonymous (found text) | "Weather Observations (Found Poem from meteorological prose)" | found_poetry | **0.23** | 17 | -0.74 | 5.33 |
| Rainer Maria Rilke | "Die erste Elegie (Eröffnung)" | german_modernist | **0.25** | 28 | 1.25 | 6.03 |
| Lawrence Ferlinghetti | "Constantly Risking Absurdity" | beat | **0.25** | 20 | -0.13 | 1.87 |
| Kamau Brathwaite | "Calypso" | postcolonial | **0.26** | 39 | -0.31 | 4.77 |
| Traditional (Scottish ballad) | "Lord Randal" | ballad | **0.26** | 23 | -0.71 | 3.97 |

---

## Era-Level Entropy Variance Profile

| Era | n | mean S₂ | mean std(H) | mean CoV(H) | trap_ratio |
|---|---|---|---|---|---|
| classical_chinese | 4 | -0.59 | 2.36 | 0.36 | **0.62** |
| clerihew | 10 | 0.55 | 2.59 | 0.36 | **0.61** |
| protest_political | 2 | -0.73 | 2.48 | 0.37 | **0.56** |
| elegy | 8 | -0.43 | 2.57 | 0.37 | **0.56** |
| war_poetry | 3 | -0.31 | 2.53 | 0.37 | **0.56** |
| black_arts | 2 | -0.40 | 2.32 | 0.45 | **0.53** |
| german_expressionist | 6 | 0.10 | 2.47 | 0.38 | **0.53** |
| latin_american | 4 | -0.52 | 2.43 | 0.41 | **0.52** |
| dramatic_monologue | 12 | -0.44 | 2.45 | 0.37 | **0.52** |
| haiku | 12 | -0.12 | 2.82 | 0.40 | **0.52** |
| parody | 4 | -0.40 | 2.53 | 0.38 | **0.52** |
| cliche_control | 4 | -0.93 | 2.54 | 0.47 | **0.52** |
| confessional | 6 | -0.30 | 2.51 | 0.37 | **0.51** |
| 18th_century | 8 | -0.25 | 2.61 | 0.40 | **0.51** |
| 19th_century | 19 | -0.27 | 2.58 | 0.39 | **0.51** |
| early_modern | 11 | -0.37 | 2.23 | 0.33 | **0.50** |
| ekphrastic | 8 | -0.39 | 2.42 | 0.35 | **0.50** |
| metaphysical | 7 | -0.54 | 2.31 | 0.34 | **0.50** |
| prose_poetry | 12 | -0.47 | 2.31 | 0.42 | **0.50** |
| language | 6 | -0.52 | 2.45 | 0.39 | **0.49** |
| romantic | 23 | -0.49 | 2.71 | 0.41 | **0.49** |
| fixed_form | 8 | -0.58 | 2.88 | 0.47 | **0.49** |
| german_symbolist | 3 | 0.39 | 2.19 | 0.33 | **0.49** |
| persian | 2 | -0.24 | 2.73 | 0.40 | **0.48** |
| oulipo | 13 | -0.25 | 2.60 | 0.43 | **0.48** |
| procedural | 8 | -0.54 | 2.70 | 0.46 | **0.48** |
| new_york_school | 26 | -0.60 | 2.43 | 0.39 | **0.48** |
| victorian | 34 | -0.26 | 2.62 | 0.40 | **0.48** |
| ancient | 4 | -0.31 | 2.45 | 0.37 | **0.47** |
| modernist | 30 | -0.46 | 2.66 | 0.41 | **0.46** |
| old_english | 5 | -0.29 | 2.42 | 0.37 | **0.46** |
| contemporary | 21 | -0.39 | 2.54 | 0.44 | **0.45** |
| ghazal | 3 | -0.30 | 2.45 | 0.41 | **0.45** |
| imagist | 5 | -0.45 | 2.41 | 0.36 | **0.44** |
| found_poetry | 9 | -0.61 | 2.40 | 0.53 | **0.44** |
| beat | 8 | 0.19 | 2.61 | 0.63 | **0.44** |
| biblical | 8 | -0.51 | 2.41 | 0.52 | **0.44** |
| harlem_renaissance | 8 | -0.49 | 2.70 | 0.43 | **0.44** |
| mid_century | 6 | -0.29 | 2.56 | 0.41 | **0.44** |
| ballad | 6 | -0.39 | 2.80 | 0.51 | **0.43** |
| nonsense | 2 | -0.68 | 3.13 | 0.51 | **0.43** |
| surrealist | 8 | -0.61 | 2.60 | 0.43 | **0.42** |
| parody_original | 3 | -0.55 | 2.57 | 0.45 | **0.42** |
| objectivist | 6 | -0.59 | 2.93 | 0.55 | **0.42** |
| japanese_classical | 2 | -0.70 | 2.34 | 0.39 | **0.42** |
| pantoum | 2 | -0.44 | 2.70 | 0.54 | **0.42** |
| concrete | 5 | -0.65 | 2.68 | 0.69 | **0.41** |
| postcolonial | 6 | -0.49 | 2.77 | 0.52 | **0.40** |
| limerick | 10 | -0.69 | 2.35 | 0.38 | **0.40** |
| spoken_word | 3 | -0.58 | 2.31 | 0.42 | **0.39** |
| song_lyrics | 3 | -0.64 | 2.92 | 0.70 | **0.37** |
| villanelle | 3 | -0.57 | 3.33 | 0.64 | **0.36** |
| german_modernist | 2 | 0.77 | 2.36 | 0.39 | **0.35** |
| double_dactyl | 5 | -0.95 | 2.73 | 0.38 | **0.32** |
| triolet | 2 | -0.74 | 2.97 | 0.75 | **0.30** |
| social_media_poetry | 2 | -1.07 | 2.99 | 0.44 | **0.25** |

---

## Prose Control Comparison

- Prose mean S₂: -1.736
- Prose mean std(H): 2.567
- Prose mean CoV(H): 0.462
- Prose trap_ratio: 0.647

---

## Finding

**Key result**: std(H) and mean S₂ are weakly correlated (r = -0.070). Entropy variance does not strongly predict S₂ magnitude.

**Context entropy**: mean H and mean S₂ are weakly correlated (r = 0.103).

**Quadrant analysis**: 105 poems (23%) are 'Trap-Release' (high S₂, variable H). 118 (26%) are 'Consistent Ambush' (high S₂, stable H). This means high-S₂ poetry is split between poems that use entropy variation to set up surprise and poems that maintain consistently unpredictable contexts.

**Suggested next steps**:
1. Examine whether trap_ratio varies systematically with *era* (e.g., do Romantic poets trap-and-release while Language poets fog-and-leap?)
2. Within the 'Consistent Ambush' quadrant, what makes the high S₂ tokens unexpected if H is stable? Are these the 'truly deviant' words?
3. Test whether trap_ratio correlates with perceived poetic 'intensity' or 'impact' metrics.

---

## New Poems Added (2026-11-26): Entropy Variance Test Cases

4 new poems were added to the corpus to test the entropy variance hypothesis directly:

| Title | Author | Era | avg S₂ | avg H | std S₂ | Top spike (token / S₂ / H) |
|---|---|---|---|---|---|---|
| The Bells (stanza 1) | Edgar Allan Poe | 19th_century | **-0.859** | 6.314 | 4.132 | "Silver" / 23.93 / H=0.04 |
| Up-Hill | Christina Rossetti | victorian | 0.442 | 5.238 | 5.105 | "May" / 29.14 / H=0.01 |
| The Creation (excerpt) | James Weldon Johnson | harlem_renaissance | 0.802 | 4.619 | 6.353 | "Dark" / 30.33 / H=0.01 |
| Fragment 31 (Wharton 1885) | Sappho | ancient | 0.366 | 5.760 | 5.165 | "Then" / 21.82 / H=0.01 |

### Key observation
Poe's "The Bells" — the most repetitively structured poem — has the **lowest avg S₂ (-0.859)** of the group.
Its top spike ("Silver") has H=0.04, nearly zero: the model was utterly confident about what would come
(a continuation of the established pattern), and "Silver bells!" violated that confidence completely.

This is the trap-and-release mechanism visible at the token level: the poem's extreme repetition CREATES
confident contexts, and the deviations from pattern produce extreme localized S₂ — but the averaging across
so many predictable tokens yields a below-baseline poem mean.

For Johnson and Sappho, the top spikes (H≈0.01) are all stanza-break artifacts (model expected newline, got a capitalized word).
But Poe's "Silver" at H=0.04 may be a genuinely within-line trap: it appears after "Silver" is established as a refrain element.

**Hypothesis for future work**: In highly repetitive poems, the trap-and-release operates at TWO levels:
1. Layout-level (stanza breaks, as artifact) — same as all poems
2. Schema-level (within the established repetition pattern, specific words violate the expected continuation)

Schema-level traps are more interesting literarily and would need artifact-free analysis focusing on
non-stanza-break high-S₂ tokens within repetitive structures.