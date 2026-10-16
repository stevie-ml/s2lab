# Phonetic Distance from the Top Prediction

**Date:** 2026-10-16  
**Experiment:** `experiments/phonetic_distance_s2.py`  
**Data:** `results/phonetic_distance_s2.json`  
**Corpus:** 284 poems, 19,077 alphabetic tokens (stanza-break artifact filtered)

---

## Research Question

When poets deviate from GPT-2's top prediction, do they choose words that *sound* similar (phonetic substitution — preserving the signifier, changing the signified) or words that are phonetically unrelated?

**Hypothesis tested:** High-S2 moments might involve sound-alike substitutions — the poet picks a near-homophone of the expected word, maintaining acoustic texture while diverging semantically.

---

## Method

For each non-punctuation, alphabetic token in the corpus:
1. Retrieve GPT-2's #1 ranked alternative token
2. Compute normalized edit-distance phonetic similarity between the poet's token and the top prediction (1 = identical, 0 = completely different)
3. Bin by S2 level and compare phonetic similarity distributions

---

## Key Finding: Dual Departure — Phonetic AND Semantic

**Pearson correlation: r = −0.465 (n = 19,077)**

Poetic surprise (high S2) almost always involves both semantic AND phonetic departure from the top prediction. The hypothesis that poets use "sound-alike" substitution to create informational surprise is **falsified** for the general case.

### Phonetic Proximity by S2 Class

| S2 Class | Range | N | Mean Similarity | % Phonetically Close (>0.5) | % Same First Letter |
|---|---|---|---|---|---|
| very_low | < −4 | 2,355 | **0.801** | **77.5%** | **79.2%** |
| low | −4 to −1 | 7,013 | 0.489 | 42.3% | 47.1% |
| neutral | −1 to 1 | 4,098 | 0.379 | 30.0% | 36.2% |
| moderate | 1 to 4 | 3,096 | 0.139 | 3.0% | 9.9% |
| high | 4 to 8 | 1,864 | 0.125 | 1.6% | 8.2% |
| very_high | > 8 | 651 | 0.115 | 1.7% | 7.4% |

### The Phase Transition at S2 ≈ 1

There is a dramatic phase transition between the *neutral* and *moderate* S2 bins:
- Below S2 = 1: phonetic similarity **0.38–0.80** (poet and model speak the same acoustic language)
- Above S2 = 1: phonetic similarity **0.11–0.14** (poet has genuinely departed from the sound-world the model expects)

This suggests that the S2 threshold of ~1 bit marks not just a semantic but an **acoustic discontinuity** in poetic choice.

---

## The Rare Exception: Rhyming Substitution

The ~1.7% of high-S2 tokens that *are* phonetically close are genuinely interesting. These are cases where poetic surprise is achieved through **phonetic fidelity with semantic rupture** — the auditory expectation is met but the meaning diverges:

| Poet's Token | GPT-2's Prediction | S2 | Phonetic Sim | Interpretation |
|---|---|---|---|---|
| `could` | `would` | 10.83 | 0.80 | Modal substitution: same length, same ending, different modality |
| `day` | `way` | 9.47 | 0.67 | Rhyme-slot substitution: /-eɪ/ maintained |
| `them` | `the` | 8.06 | 0.75 | Pronoun expanded from expected article |
| `He` | `the` | 8.27 | 0.67 | Capitalized agent from expected article |
| `men` | `me` | 6.17 | 0.67 | Plural expansion at pronoun slot |

These are not accidents. "Could/would" is a classic poetic substitution that preserves the auxiliary modal slot phonetically while shifting semantic modality. "Day/way" preserves the rhyme sound at a metrically prominent position.

These constitute a coherent **rhetorical category**: *phonetic rhyme-within-expectation*, where the poet's sound choice is acoustically *right* but semantically *surprising*.

---

## Era Analysis: Who Achieves Phonetic-Fidelity Surprise?

Mean phonetic similarity at high-S2 moments (S2 ≥ 4) by era:

| Era | N (high S2 tokens) | Mean Phonetic Sim |
|---|---|---|
| early_modern | 40 | **0.203** |
| german_symbolist | 31 | **0.198** |
| protest_political | 16 | 0.181 |
| german_modernist | 27 | 0.159 |
| biblical | 71 | 0.157 |
| song_lyrics | 36 | 0.157 |
| harlem_renaissance | 37 | 0.149 |
| contemporary | 67 | 0.125 |
| postcolonial | 70 | 0.122 |

**Early modern** (Shakespeare-era) poetry achieves the *highest* phonetically-similar surprise: even at high S2, early modern poets are relatively more likely to choose a word that sounds like GPT-2's prediction. This is consistent with the metrical-acoustic tradition of early modern verse, where sound texture is paramount.

**Contemporary** and **postcolonial** poetry shows the lowest phonetic similarity at high-S2 — these poets' surprising choices are the most acoustically radical. This aligns with the shift away from metrical/acoustic constraint in modern free verse.

---

## Interpretation: The Acoustic Straussian Gap

The Straussian gap (what is *chosen* vs what was *expected*) is not just semantic — it is acoustic. When a poet deviates significantly from GPT-2's prediction, they almost always choose a word that *sounds different* from the top prediction. 

This challenges the intuition that poetic defamiliarization often works via near-homophones or rhyme substitution. While that mechanism exists (the ~1.7% exception), it is not the dominant mode of poetic surprise.

The dominant mode is **dual departure**: the poet leaves both the semantic and acoustic field of the expected word simultaneously. This is consistent with defamiliarization theory (Shklovsky) — genuine poetic surprise requires the reader to register both *that* something unexpected was said *and* that it doesn't even sound like what was expected.

The phase transition at S2 ≈ 1 is particularly clean: it suggests that the S2 = 1 threshold marks the point where a poet "crosses over" into genuinely alien acoustic territory, not just semantic territory.

---

## Suggested Next Steps

1. **Semantic distance parallel**: Run the same analysis with semantic similarity (using word embeddings) — compare whether semantic gap and phonetic gap are correlated at high-S2 moments.
2. **Rhyme-slot targeting**: Specifically analyze rhyme-position tokens (line-final) to see if phonetic-fidelity surprise is significantly more common there.
3. **The "sound world" of each era**: Cluster eras by their (mean_S2, mean_phonetic_sim_at_high_S2) — do eras group into acoustic-priority vs semantic-priority?
4. **Per-poet analysis**: Does phonetic fidelity at surprise correlate with a poet's formal commitments (meter, rhyme scheme)?
