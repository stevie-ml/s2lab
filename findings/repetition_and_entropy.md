# Repetition and Entropy: The Straussian Gap Collapses at Refrain
**Date:** 2026-08-30  
**Experiment:** `experiments/repetition_entropy.py`

## Question
Do poems that use repetition (anaphora, refrain) have different S₂ profiles at repeated structures? Specifically: does the Straussian gap — the excess surprise a poet produces — *collapse* when a word or phrase recurs, as GPT-2 "learns" the pattern from prior context and lowers its entropy?

## Hypothesis
At the **first** occurrence of a repeated phrase, the model has not encountered it yet → high entropy, potentially high surprisal → real chance of positive S₂ (genuine Straussian deviation).  
At **subsequent** occurrences, the model can predict the pattern from context → lower entropy → even if surprisal also drops, the S₂ should fall more sharply, potentially going negative (the poet's "unusual" choice is now expected).

---

## Method
- Loaded all 51 English poems from `corpus_results.json` (pre-computed GPT-2 token data)
- For each content token (length ≥ 2 characters, not a stop/function word), recorded whether it was its **first** or **repeat** occurrence in that poem
- Computed average S₂ for first vs. repeat occurrences globally and per poem
- Case studies: poems with known strong anaphora (Howl, We Real Cool, Whereas, The Negro Speaks of Rivers, Free Union, Daddy)
- Approximated t-statistic for the global comparison

---

## Results

### Global Finding (n=51 poems, excluding control prose)

| Group | n tokens | Avg S₂ |
|---|---|---|
| First occurrences | 1,606 | **+1.903** |
| Repeat occurrences | 207 | **−0.867** |
| Δ (repeat − first) | — | **−2.771** |

**t ≈ 7.49** — extremely strong signal. Repeated content words carry dramatically lower S₂ than their first occurrences.

> Interpretation: **The Straussian gap is a property of novelty, not repetition.** When a poet repeats a word, GPT-2 has already encoded that choice as possible in this context, lowering its entropy. The poet's deviation from expectation disappears — the word becomes *expected*.

---

### Per-Poem Summary (anaphora/refrain poems only)

| Poem | Author | n_first | n_repeat | Avg S₂ (1st) | Avg S₂ (repeat) | Δ |
|---|---|---|---|---|---|---|
| We Real Cool | Gwendolyn Brooks | 17 | 6 | +9.790 | −3.101 | **−12.892** |
| The Negro Speaks of Rivers | Langston Hughes | 53 | 5 | +1.651 | −2.677 | **−4.328** |
| Free Union (excerpt) | André Breton | 26 | 8 | +2.211 | −1.732 | **−3.943** |
| Whereas (excerpt) | Layli Long Soldier | 11 | 9 | +3.198 | −0.549 | **−3.748** |
| Catalog of Unabashed Gratitude | Ross Gay | 20 | 1 | +0.860 | −1.042 | **−1.902** |
| Daddy (opening) | Sylvia Plath | 42 | 7 | +3.235 | +1.581 | **−1.654** |

**All 6 anaphoric poems show the predicted pattern (Δ < 0).** The effect is strongest in *We Real Cool*, which relies most heavily on pure structural anaphora.

---

### Case Study: "The Negro Speaks of Rivers" — Token-Level Collapse

The most striking individual repetition in the corpus: the word "rivers" drops **−16.97 S₂ points** from first to second occurrence (S₂: +10.91 → −6.06).

| Token | 1st S₂ | 2nd S₂ | Δ |
|---|---|---|---|
| 'rivers' | +10.91 | −2.71 | **−13.62** |
| 'known' | +1.39 | −3.27 | **−4.66** |
| 'and' | −0.21 | −4.67 | **−4.46** |
| 'My' | −1.05 | −4.03 | **−2.99** |

Hughes writes: *"I've known rivers: / I've known rivers ancient as the world..."* — the second "I've known rivers" was already surprising the first time (establishing a sonic identity), but by repetition it becomes the poem's structural signature. GPT-2 rewards the repetition with lower entropy, causing S₂ to collapse. **The phrase migrates from the Straussian register to the expected.**

---

### Case Study: "We Real Cool" — 'We' Anaphora Decay

Brooks uses "We" to open every couplet. Here is GPT-2's S₂ for each occurrence of "We":

| Occurrence | Position | S₂ |
|---|---|---|
| #1 | 4 | −3.50 |
| #2 | 9 | **−4.66** (minimum) |
| #3 | 17 | −3.79 |
| #4 | 22 | −3.52 |
| #5 | 28 | −2.83 |
| #6 | 34 | −1.62 |
| #7 | 41 | −2.19 |

Surprisingly, S₂ for "We" is **always negative** — the model expects "We" at every point. The S₂ is lowest at the second occurrence (deepest expectation), but then *partially recovers* at occurrences 5-7, possibly because the model's attention window spreads thin across so many prior "We" tokens.

**Implication:** Brooks' genius in "We Real Cool" isn't the "We" itself (always predicted) — it's what follows each "We". The predictable anaphora creates a *container* of low S₂ that makes the unpredictable content words ("Die", "Strike", "Lurk") carry maximum Straussian charge by contrast.

---

### Top 5 Most Dramatic Entropy Collapses

| Author | Token | 1st S₂ | Repeat S₂ | Δ |
|---|---|---|---|---|
| Langston Hughes | ' like' | +27.72 | −2.23 | **−29.95** |
| André Breton | 'Wh' (Whose) | +19.75 | −4.29 | **−24.05** |
| John Ashbery | ' he' | +15.75 | −5.56 | **−21.31** |
| Langston Hughes | ' rivers' | +10.91 | −6.06 | **−16.97** |
| John Ashbery | ' look' | +15.10 | −0.70 | **−15.80** |

---

## Key Findings

1. **The Straussian gap is a first-use property.** Repeated content words lose ~2.77 S₂ bits on average — a robust, statistically significant effect (t ≈ 7.49).

2. **Anaphora converts surprise into structure.** Once a poet establishes a repeating frame (Howl's "who", Hughes's "rivers", Brooks's "We"), subsequent uses register as expected rather than deviant. The poem trains GPT-2's in-context expectations in real time.

3. **The contrast effect:** Poems like *We Real Cool* use predictable anaphora as a structural frame that *amplifies* the S₂ of the content words that break the pattern. Low-S₂ scaffolding makes high-S₂ moments more prominent — an information-theoretic version of poetic defamiliarization.

4. **Partial recovery at high repetition counts:** The "We" data from *We Real Cool* suggests that S₂ partially recovers after 4-5 repetitions, possibly due to GPT-2's attention window dilution. This predicts that very long anaphoric structures (like Ginsberg's "who" list) should show U-shaped S₂ curves at the anaphoric token.

---

## Suggested Next Steps

- **Map the full Ginsberg "who" curve:** Plot S₂ for every "who" token across all of Howl. Does it show the predicted U-shape?
- **Cross-poem anaphora comparison:** Group poems by their anaphoric word type (pronoun vs. conjunction vs. noun) — do different word classes show different collapse rates?
- **Compression ratio connection:** Does gzip compression ratio correlate with the first/repeat S₂ differential? High-repetition poems should compress well AND show large S₂ drops.
- **Add poems to corpus:** Dylan Thomas's "Do Not Go Gentle" (refrain), Whitman's "Leaves of Grass" catalogues, Neruda's "Odes" (strong anaphora).
