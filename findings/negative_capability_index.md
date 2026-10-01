# The Negative Capability Index: Poetry and the Acceptance of Ambiguity

**Date:** 2026-10-01
**Experiment:** `experiments/negative_capability_index.py`
**Corpus:** English poetry texts from `results/corpus_results.json`, stanza-break artifact filtered
**Builds on:** `straussian_gap_taxonomy.md`, `s2_transition_entropy.md`, `surprise_taxonomy_2x2.md`

---

## Research Question

Keats coined "negative capability" to describe "the capacity to be in uncertainties, Mysteries, doubts, without any irritable reaching after fact & reason."
Can information theory operationalize this concept?

When GPT-2 is **uncertain** (high entropy), the poet faces two paths:
1. **Accept ambiguity** (S₂ ≤ 0): Choose a word GPT-2 expects — let the ambiguity stand, unforcefully resolved
2. **Resist ambiguity** (S₂ > 0): Choose a word GPT-2 does NOT expect — impose a specific, unexpected resolution

**The Negative Capability Index (NC)** = fraction of high-entropy positions where the poet accepts a conventional choice.
Higher NC → more 'Keatsian' acceptance of uncertainty.
Lower NC → more assertive resistance to the model's ambiguity.

---

## Method

- Filtered all tokens (stanza-break artifact removed: p_newline < 0.9)
- Computed corpus-wide entropy quartiles: Q1=4.34, Q2=6.43, Q3=8.22 bits
- **High-entropy threshold**: top quartile (H ≥ 8.22 bits)
- Low-entropy zone: H < 6.43 bits
- NC Index = fraction of high-entropy tokens where S₂ ≤ 0
- ΔNC = NC_index − LE_conform_rate (net 'high-entropy acceptance above baseline')
- Restricted to English poetry; excluded control/cliché texts

---

## Finding 1: Corpus-Wide Baseline

| Zone | N tokens | Conform rate (S₂ ≤ 0) | Avg S₂ |
|---|---|---|---|
| High entropy (H ≥ 8.2) | 4,984 | **57.4%** | -0.502 |
| Low entropy (H < 6.4) | 9,900 | **72.4%** | -0.338 |

Corpus-wide ΔNC (high vs low entropy conformism): **-0.150**

At high-entropy positions, poets conform 57.4% of the time.
At low-entropy positions, they conform 72.4% of the time.

**Poets are LESS conventional at uncertain positions** — when the model doesn't know what comes next, poets tend to push further into the unexpected. Uncertainty invites resistance, not acceptance.

---

## Finding 2: Era Profiles — Which Literary Movements Accept Ambiguity?

| Era | n poems | n poets | NC Index | Avg S₂ at HE | Avg S₂ at LE |
|---|---|---|---|---|---|
| oulipo | 1 | 1 | **0.706** | -0.951 | -0.454 |
| song_lyrics | 3 | 3 | **0.685** | -1.237 | -0.446 |
| nursery_rhyme | 1 | 1 | **0.649** | -1.152 | -0.447 |
| concrete | 3 | 3 | **0.643** | -0.332 | -0.442 |
| ballad | 6 | 2 | **0.635** | -0.880 | -0.108 |
| fixed_form | 8 | 8 | **0.634** | -0.954 | -0.491 |
| prose_poetry | 9 | 9 | **0.632** | -1.048 | -0.392 |
| language | 3 | 3 | **0.619** | -0.755 | 0.488 |
| confessional | 6 | 4 | **0.613** | -0.671 | -0.120 |
| found_poetry | 7 | 5 | **0.612** | -0.620 | -0.440 |
| mid_century | 3 | 3 | **0.603** | -0.804 | -0.325 |
| haiku | 14 | 7 | **0.596** | -0.373 | 0.116 |
| romantic | 14 | 6 | **0.593** | -0.685 | -0.259 |
| biblical | 7 | 1 | **0.591** | -0.807 | -0.444 |
| ancient | 1 | 1 | **0.583** | -0.724 | 0.283 |
| metaphysical | 4 | 3 | **0.574** | -0.501 | -1.061 |
| new_york_school | 18 | 2 | **0.574** | -0.491 | -0.440 |
| 18th_century | 1 | 1 | **0.561** | -0.066 | -0.497 |
| spoken_word | 2 | 1 | **0.556** | -0.004 | -0.605 |
| victorian | 21 | 13 | **0.552** | -0.228 | -0.270 |
| modernist | 21 | 13 | **0.549** | -0.428 | -0.308 |
| harlem_renaissance | 5 | 3 | **0.548** | -0.369 | -0.225 |
| 19th_century | 10 | 5 | **0.548** | -0.507 | -0.396 |
| early_modern | 4 | 3 | **0.534** | -0.407 | -0.057 |
| deep_image | 1 | 1 | **0.533** | 0.572 | -0.462 |
| contemporary | 9 | 9 | **0.512** | -0.242 | -0.327 |
| surrealist | 1 | 1 | **0.450** | 0.363 | -0.777 |
| beat | 2 | 1 | **0.372** | 1.483 | 0.490 |

**Most 'negatively capable' era** (accepts uncertainty most): **oulipo** (NC=0.706)
**Least 'negatively capable' era** (resists uncertainty most): **beat** (NC=0.372)

---

## Finding 3: Poet-Level NC Index — The Full Ranking

NC Index: fraction of high-entropy positions where S₂ ≤ 0 (poet accepts conventional choice).
ΔNC: NC minus the poet's baseline low-entropy conform rate (net uncertainty-acceptance).

| Poet | Era | n poems | NC Index | ΔNC | Avg HE S₂ |
|---|---|---|---|---|---|
| Marianne Moore | modernist | 1 | 0.667 | **+0.167** | -1.793 |
| Anne Sexton | confessional | 2 | 0.724 | **+0.119** | -1.812 |
| Sylvia Plath | confessional | 2 | 0.723 | **+0.098** | -1.103 |
| Anonymous (KJV, found text) | found_poetry | 1 | 0.778 | **+0.090** | -1.783 |
| William Wordsworth | romantic | 1 | 0.750 | **+0.083** | -1.529 |
| Layli Long Soldier | contemporary | 1 | 0.619 | **+0.081** | -1.186 |
| Philip Larkin | contemporary | 1 | 0.625 | **+0.069** | -0.710 |
| Lyn Hejinian | language | 1 | 0.800 | **+0.061** | -2.674 |
| Matsuo Bashō | haiku | 4 | 0.704 | **+0.052** | -0.748 |
| Carolyn Forché | prose_poetry | 1 | 0.667 | **+0.035** | -1.287 |
| Killarney Clary | prose_poetry | 1 | 0.739 | **+0.016** | -1.527 |
| Traditional (American folk) | song_lyrics | 1 | 0.818 | **+0.012** | -1.895 |
| Austin Dobson | fixed_form | 1 | 0.677 | **-0.003** | -1.051 |
| Georges Perec | oulipo | 1 | 0.706 | **-0.014** | -0.951 |
| Elizabeth Bishop | mid_century | 1 | 0.636 | **-0.030** | -1.437 |
| Felicia Hemans | victorian | 1 | 0.634 | **-0.036** | -1.079 |
| Edna St. Vincent Millay | mid_century | 1 | 0.667 | **-0.036** | -1.077 |
| Kobayashi Issa | haiku | 3 | 0.640 | **-0.044** | -1.540 |
| William Shakespeare | victorian | 3 | 0.674 | **-0.050** | -0.747 |
| Ben Jonson | early_modern | 1 | 0.667 | **-0.057** | -1.328 |
| Walter de la Mare | 19th_century | 1 | 0.615 | **-0.060** | -0.781 |
| John Donne | metaphysical | 1 | 0.700 | **-0.064** | -0.922 |
| Samuel Taylor Coleridge | romantic | 1 | 0.598 | **-0.065** | -0.461 |
| Sappho | ancient | 1 | 0.583 | **-0.066** | -0.724 |
| Thomas Wyatt | early_modern | 2 | 0.530 | **-0.070** | -0.368 |
| Traditional (English) | nursery_rhyme | 1 | 0.649 | **-0.071** | -1.152 |
| Langston Hughes | harlem_renaissance | 3 | 0.645 | **-0.073** | -1.051 |
| Christina Rossetti | victorian | 1 | 0.615 | **-0.074** | -0.224 |
| Hart Crane | modernist | 1 | 0.473 | **-0.075** | 0.998 |
| David Antin | prose_poetry | 1 | 0.750 | **-0.077** | -1.664 |
| Frank O'Hara | new_york_school | 2 | 0.571 | **-0.077** | 0.261 |
| Rae Armantrout | prose_poetry | 1 | 0.588 | **-0.082** | -0.668 |
| Dante Gabriel Rossetti | fixed_form | 1 | 0.611 | **-0.086** | -0.837 |
| Masaoka Shiki | haiku | 2 | 0.600 | **-0.088** | -0.435 |
| Rudyard Kipling | victorian | 2 | 0.667 | **-0.090** | -1.575 |
| Emily Dickinson | 19th_century | 4 | 0.584 | **-0.101** | -0.431 |
| Traditional (American sea chanty) | song_lyrics | 1 | 0.727 | **-0.106** | -1.831 |
| Yosa Buson | haiku | 2 | 0.533 | **-0.110** | -0.271 |
| Carl Sandburg | modernist | 2 | 0.600 | **-0.112** | -0.937 |
| Robert Burns | romantic | 2 | 0.616 | **-0.113** | -0.872 |
| T.S. Eliot | modernist | 3 | 0.529 | **-0.113** | -0.389 |
| Thomas Hardy | victorian | 3 | 0.480 | **-0.116** | 0.103 |
| Matthew Arnold | victorian | 2 | 0.585 | **-0.117** | -0.406 |
| John Keats | romantic | 3 | 0.545 | **-0.123** | -0.678 |
| Anonymous (Hebrew Bible) | biblical | 7 | 0.591 | **-0.125** | -0.807 |
| John Ashbery | new_york_school | 16 | 0.574 | **-0.130** | -0.524 |
| Robert Bly | deep_image | 1 | 0.533 | **-0.133** | 0.572 |
| Claude McKay | harlem_renaissance | 1 | 0.488 | **-0.137** | -0.148 |
| Traditional (Scottish ballad) | ballad | 5 | 0.652 | **-0.143** | -1.065 |
| Edmund Spenser | early_modern | 1 | 0.440 | **-0.143** | 0.210 |
| Traditional (English/Scottish ballad) | ballad | 1 | 0.553 | **-0.144** | 0.002 |
| Charles Baudelaire | prose_poetry | 1 | 0.538 | **-0.152** | -0.092 |
| William Ernest Henley | victorian | 2 | 0.597 | **-0.153** | -0.601 |
| William Blake | romantic | 4 | 0.618 | **-0.158** | -0.742 |
| Percy Bysshe Shelley | romantic | 3 | 0.571 | **-0.160** | -0.569 |
| Wallace Stevens | modernist | 3 | 0.588 | **-0.164** | -0.625 |
| Ross Gay | contemporary | 1 | 0.583 | **-0.167** | -0.711 |
| Ernest Dowson | fixed_form | 1 | 0.773 | **-0.172** | -1.313 |
| Edgar Allan Poe | fixed_form | 2 | 0.574 | **-0.172** | -0.794 |
| Edwin Arlington Robinson | fixed_form | 1 | 0.562 | **-0.184** | 0.006 |
| Charles Darwin (found text) | found_poetry | 1 | 0.609 | **-0.186** | -0.200 |
| James Wright | prose_poetry | 1 | 0.400 | **-0.186** | -0.282 |
| Robert Lowell | confessional | 1 | 0.516 | **-0.187** | -0.144 |
| Lucille Clifton | spoken_word | 3 | 0.553 | **-0.189** | -0.039 |
| Robert Frost | modernist | 1 | 0.500 | **-0.191** | -0.246 |
| Alfred, Lord Tennyson | victorian | 3 | 0.554 | **-0.196** | -0.314 |
| Christopher Smart | 18th_century | 1 | 0.561 | **-0.198** | -0.066 |
| Gerard Manley Hopkins | victorian | 3 | 0.505 | **-0.204** | 0.095 |
| Vachel Lindsay | modernist | 1 | 0.686 | **-0.206** | -1.411 |
| Paul Laurence Dunbar | victorian | 1 | 0.500 | **-0.207** | 0.509 |
| Walt Whitman | 19th_century | 3 | 0.485 | **-0.209** | -0.176 |
| H.D. (Hilda Doolittle) | modernist | 1 | 0.438 | **-0.210** | 0.398 |
| Isaac Newton (found text) | found_poetry | 1 | 0.500 | **-0.212** | 0.544 |
| William Carlos Williams | modernist | 2 | 0.533 | **-0.217** | -0.957 |
| Ron Silliman | language | 1 | 0.565 | **-0.220** | -0.137 |
| Anonymous (found text) | found_poetry | 3 | 0.524 | **-0.225** | -0.622 |
| John Milton | victorian | 1 | 0.500 | **-0.231** | 0.211 |
| Robert Browning | victorian | 1 | 0.438 | **-0.238** | 0.669 |
| Brewster Higley | song_lyrics | 1 | 0.517 | **-0.247** | -0.264 |
| W.B. Yeats | modernist | 2 | 0.505 | **-0.248** | -0.144 |
| George Herbert | metaphysical | 2 | 0.509 | **-0.250** | -0.482 |
| E.E. Cummings | concrete | 3 | 0.600 | **-0.257** | -0.685 |
| Seamus Heaney | contemporary | 1 | 0.378 | **-0.271** | 0.693 |
| Allen Ginsberg | beat | 2 | 0.372 | **-0.277** | 1.483 |
| Gertrude Stein | modernist | 1 | 0.556 | **-0.278** | -0.984 |
| Mary Oliver | contemporary | 1 | 0.500 | **-0.279** | 0.216 |
| Countee Cullen | harlem_renaissance | 1 | 0.492 | **-0.296** | 0.158 |
| Wislawa Szymborska | contemporary | 1 | 0.517 | **-0.302** | -0.570 |
| Andrew Marvell | metaphysical | 1 | 0.455 | **-0.303** | 0.233 |
| Matsuo Basho | haiku | 1 | 0.500 | **-0.310** | 0.483 |
| Claudia Rankine | prose_poetry | 2 | 0.346 | **-0.330** | 0.210 |
| Alfred Lord Tennyson | victorian | 1 | 0.474 | **-0.332** | 0.320 |
| Oscar Wilde | fixed_form | 1 | 0.438 | **-0.358** | -0.025 |
| André Breton | surrealist | 1 | 0.450 | **-0.365** | 0.363 |
| John Berryman | confessional | 1 | 0.294 | **-0.380** | 1.511 |
| Gwendolyn Brooks | mid_century | 1 | 0.385 | **-0.449** | 0.549 |

---

## Finding 4: The Ambiguity Gap — High vs. Low Entropy S₂ Contrast

How much does S₂ CHANGE between high-entropy and low-entropy positions?
A large positive gap means the poet writes unexpectedly at uncertain moments.
A near-zero or negative gap means the poet's behavior is similar regardless of context uncertainty.

| Poet | Era | Avg S₂ (HE) | Avg S₂ (LE) | S₂ Gap (HE−LE) |
|---|---|---|---|---|
| Matsuo Basho | haiku | 0.483 | -1.332 | **+1.815** |
| Alfred Lord Tennyson | victorian | 0.320 | -1.393 | **+1.713** |
| John Berryman | confessional | 1.511 | -0.159 | **+1.670** |
| Andrew Marvell | metaphysical | 0.233 | -1.317 | **+1.550** |
| Paul Laurence Dunbar | victorian | 0.509 | -0.964 | **+1.473** |
| Isaac Newton (found text) | found_poetry | 0.544 | -0.802 | **+1.346** |
| André Breton | surrealist | 0.363 | -0.777 | **+1.140** |
| Robert Browning | victorian | 0.669 | -0.465 | **+1.134** |
| Mary Oliver | contemporary | 0.216 | -0.878 | **+1.094** |
| Robert Bly | deep_image | 0.572 | -0.462 | **+1.034** |
| Allen Ginsberg | beat | 1.483 | 0.490 | **+0.993** |
| Countee Cullen | harlem_renaissance | 0.158 | -0.614 | **+0.772** |
| Ernest Dowson | fixed_form | -1.313 | -2.075 | **+0.762** |
| W.B. Yeats | modernist | -0.144 | -0.879 | **+0.735** |
| Charles Darwin (found text) | found_poetry | -0.200 | -0.816 | **+0.616** |
| George Herbert | metaphysical | -0.482 | -1.058 | **+0.576** |
| Ron Silliman | language | -0.137 | -0.697 | **+0.560** |
| Seamus Heaney | contemporary | 0.693 | 0.160 | **+0.533** |
| Lucille Clifton | spoken_word | -0.039 | -0.562 | **+0.523** |
| Edwin Arlington Robinson | fixed_form | 0.006 | -0.456 | **+0.462** |
| Christopher Smart | 18th_century | -0.066 | -0.497 | **+0.431** |
| Gertrude Stein | modernist | -0.984 | -1.381 | **+0.397** |
| John Milton | victorian | 0.211 | -0.162 | **+0.373** |
| Edmund Spenser | early_modern | 0.210 | -0.151 | **+0.361** |
| Robert Lowell | confessional | -0.144 | -0.463 | **+0.319** |

---

## Interpretation: Two Strategies for Uncertainty

The poet who faces high entropy (the model is uncertain about what comes next) can:

### Strategy A — 'Acceptance' (High NC Index)
Choose something GPT-2 would have predicted. This is NOT laziness — it's knowing that when language opens up into multiple valid paths, the most resonant choice is often the one that:
- Honors the semantic field already established
- Respects the sound pattern the line has built
- Lets the image speak without forced cleverness

### Strategy B — 'Resistance' (Low NC Index, High S₂ at HE)
Choose something GPT-2 would NOT have predicted, even though many valid choices exist.
This is the poet forcing specificity into openness — imposing particularity where language was genuinely uncertain.

Neither strategy is inherently better. Keats prized Strategy A for lyric resolution.
Modernists (Pound's 'Make it new') arguably practice Strategy B: resist the expected at every turn.

---

## Suggested Next Steps

1. **Stanza-level NC trajectories**: does a poet's NC index change over the course of a single poem?
2. **Form and NC**: do sonnets (with formal constraint) force Strategy A or B more than free verse?
3. **NC and critical reception**: do poets with higher NC index receive different critical vocabulary (ambiguous, mysterious, suggestive) vs. lower NC (vivid, concrete, direct)?
4. **Multi-model test**: does GPT-2-medium show the same NC ranking, or is 'uncertainty' model-dependent?
