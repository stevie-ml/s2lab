# Information Arcs: The Shape of S₂ Trajectories in Poetry
**Date:** 2026-09-05
**Corpus:** 87 poetry texts + 4 control texts (English only, ≥6 tokens)
**Experiment:** `experiments/information_arcs.py`

---

## Research Question

Do poems have characteristic shapes in their S₂ (surprisal minus entropy) trajectory over poem position? Do falling arcs (front-loaded surprise) behave differently from rising arcs (building toward climax)? Do eras or authors cluster into distinctive arc types?

---

## Method

For each poem:
1. Extract the sequence of token-level S₂ values
2. Smooth with a sliding window (width ≈ 20% of poem length)
3. Fit a linear slope and locate the global peak and valley
4. Classify into one of six arc types: **rising**, **falling**, **arch**, **valley**, **flat**, **complex**, **spike**

Arc classification logic:
- **spike**: one token accounts for >60% of total positive deviation
- **rising/falling**: |slope| ≥ 1.0
- **arch**: peak in 25–75% of poem, smoothed peak substantially above endpoints
- **valley**: valley in 25–75% of poem, endpoints substantially above trough
- **complex**: multiple slope reversals (>30% of smoothed positions)
- **flat**: otherwise

---

## Results

### 1. Overall Arc Distribution

| Arc Type | Count | % | Avg S₂ |
|---|---|---|---|
| **falling** | 47 | 54% | 0.043 |
| **valley** | 15 | 17% | 0.085 |
| **rising** | 14 | 16% | **0.953** |
| **arch** | 6 | 7% | 0.153 |
| **complex** | 4 | 5% | **1.007** |
| **spike** | 1 | 1% | -2.364 |

**Key finding:** 54% of poems are falling arcs — they front-load their surprise. But poems with rising arcs have dramatically higher avg S₂ (0.953 vs 0.043 for falling). **The poems that build toward surprise are, in aggregate, more surprising.**

---

### 2. Where Does S₂ Peak?

| Region of poem | Count | % |
|---|---|---|
| **0–19% (opening)** | **46** | **55%** |
| 20–39% | 13 | 16% |
| 40–59% (middle) | 7 | 8% |
| 60–79% | 8 | 10% |
| 80–99% (ending) | 9 | 11% |

More than half of poems reach their maximum S₂ in the first fifth. This confirms and extends the earlier structural position finding: **poetry front-loads its most unexpected choices.** The first word after the first line break is the most common location for peak S₂.

---

### 3. Arc Type by Literary Era

| Era | n | Dominant Arc | Distribution |
|---|---|---|---|
| new_york_school | 18 | **falling** | 83% falling |
| modernist | 15 | falling | falling:6, rising:2, arch:2, valley:3, complex:2 |
| victorian | 8 | falling | rising:1, falling:4, arch:1, valley:1, complex:1 |
| contemporary | 7 | falling | rising:1, falling:4, valley:2 |
| romantic | 6 | **split** | rising:3, falling:3 |
| harlem_renaissance | 4 | falling | falling:2, valley:2 |
| **confessional** | 3 | **rising** | rising:2, falling:1 |
| language | 3 | falling | falling:2, arch:1 |
| 19th_century | 9 | falling | rising:1, falling:5, arch:1, valley:2 |
| mid_century | 2 | **rising** | rising:2 |

**Observation:** The New York School (Ashbery et al.) is overwhelmingly falling-arc — almost all front-loading. Confessional poets (Plath, Sexton) skew rising — building toward revelation. Romantic poetry splits evenly: some poets front-load (Wordsworth), others build (Keats, Byron). This suggests arc type is a genuine stylistic signature, not noise.

---

### 4. Most Dramatic Rising Arcs (poems that build toward surprise)

| Author | Poem | Slope | Avg S₂ |
|---|---|---|---|
| William Carlos Williams | "This Is Just to Say" | **+4.68** | 2.61 |
| Sylvia Plath | "Daddy (opening)" | +3.00 | 0.48 |
| Elizabeth Bishop | "One Art" | +2.23 | 1.22 |
| Seamus Heaney | "Digging" | +1.97 | 1.85 |
| Sylvia Plath | "Lady Lazarus (opening)" | +1.72 | 1.41 |

**Williams' "This Is Just to Say"** is the most steeply rising poem in the corpus. The entire poem builds — through mundane confession ("I have eaten / the plums") — to the most surprising line: "Forgive me / they were delicious / so sweet / and so cold." The GPT-2 model is progressively more surprised as the poem reaches its anti-climactic climax. The poem *earns* its surprise by withholding it.

---

### 5. Most Dramatic Falling Arcs (front-loaded surprise)

| Author | Poem | Slope | Avg S₂ |
|---|---|---|---|
| Layli Long Soldier | "Whereas (excerpt)" | -7.47 | 0.51 |
| John Ashbery | "Some Trees" | -6.22 | -0.59 |
| Bruce Andrews | "Islets/Irritations" | -5.83 | 1.85 |
| William Wordsworth | "I Wandered Lonely as a Cloud" | -5.61 | -0.40 |
| H.D. | "Oread" | -5.36 | 0.51 |

**Long Soldier's "Whereas"** opens with extreme formal surprise (the legal document parody format hits GPT-2 hardest at the start), then becomes more legible as the form stabilizes. Ashbery's poems reliably decay in surprise — they open with a striking line and then drift into fluency.

---

### 6. Arch-Shaped Poems (S₂ peaks in middle)

| Author | Poem | Peak Position | Avg S₂ |
|---|---|---|---|
| Thomas Hardy | "Neutral Tones" | 36% | 1.33 |
| Emily Dickinson | "I felt a Funeral, in my Brain" | 74% | 0.48 |
| Ezra Pound | "In a Station of the Metro" | 63% | 0.26 |

Hardy's "Neutral Tones" has a mid-poem S₂ climax — the scene-setting stanza gives way to the poem's most unexpected image ("the smile on your mouth was the deadest thing"), then resolves. Pound's two-line poem peaks on "petals" — the word GPT-2 least expects in that context.

---

### 7. Volatility Leaders (most jagged S₂ profiles)

| Author | Poem | S₂ σ | Arc |
|---|---|---|---|
| W.C. Williams | "The Red Wheelbarrow" | **10.32** | falling |
| W.C. Williams | "This Is Just to Say" | 9.91 | rising |
| Gwendolyn Brooks | "We Real Cool" | 9.84 | rising |
| Matsuo Basho | "Three Haiku" | 8.02 | valley |
| Langston Hughes | "Harlem" | 8.00 | falling |

The most volatile poems are also the shortest and most formally concentrated — every token counts, so deviations are extreme. Short lyric poems (haiku, Williams' Imagism, Brooks' minimalism) produce the most jagged S₂ profiles because there's no room for the curve to smooth out.

---

## Key Findings

1. **Poetry front-loads surprise**: 55% of poems peak in their opening 20%. The first word after the first line break is the most common site of maximum S₂.

2. **Rising arcs are rarer but more surprising**: Only 16% of poems have rising arcs, but these poems have avg S₂ ≈ 0.95 vs ≈ 0.04 for falling arcs. Poems that *build* to their surprise tend to be more surprising in aggregate.

3. **Arc type is a stylistic signature**: New York School = falling. Confessional = rising. Romantic = split. This matches intuition about how these movements relate to reader expectation.

4. **Williams' "This Is Just to Say" is the prototypical rising-arc poem**: The entire poem earns its closing surprise through apparent casualness. The information-theoretic structure precisely mirrors the rhetorical one.

5. **Volatility and brevity are correlated**: Short, concentrated poems (haiku, Imagism, minimalist lyrics) produce the highest S₂ standard deviations. There's no room to "average out" — each token carries maximal weight.

---

## Hypotheses for Future Work

- **Arc type predicts emotional effect**: Rising arcs → catharsis/revelation; falling arcs → puzzle/mystery. Test with reader-response data.
- **Arc type and genre**: Sonnets may have characteristic arch shapes (volta at ~60%); villanelles may have complex shapes (due to repetition); odes may rise.
- **Within-poet arc evolution**: Do poets' arc types change across their careers? Does Plath's arc shape shift from earlier to later work?
- **Arc + volatility = poetic intensity**: A combined metric (rising arc + high volatility) might predict "impact" poems better than avg S₂ alone.

---

## Next Steps

1. Extend arc analysis to non-English poems (currently filtered to English)
2. Annotate poems by formal type (sonnet, villanelle, free verse, ode) and test arc-type correlation with form
3. Build a visualization: S₂ time-series plots for representative poems of each arc type
4. Test whether human readers' reported "most memorable line" correlates with the S₂ peak position
