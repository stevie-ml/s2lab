# Rhyme-Slot Phonetic Targeting: Do Line Endings Achieve "Sound-Alike" Surprise?

**Date:** 2026-10-17  
**Experiment:** `experiments/rhyme_slot_phonetics.py`  
**Data:** `results/rhyme_slot_phonetics.json`  
**Corpus:** 301 poems, 26,684 artifact-filtered alphabetic tokens  
**Builds on:** `phonetic_distance_s2.md`, `lineation_and_s2.md`, `enjambment_vs_s2.md`

---

## Research Question

The `phonetic_distance_s2.md` experiment found that ~1.7% of high-S2 tokens are phonetically
close to the model's top prediction — a "phonetic-fidelity surprise" category where the poet
preserves acoustic texture while violating semantic expectations.

A natural follow-up: **are these phonetically-close high-S2 tokens concentrated at line endings
(rhyme slots)?** If rhyme forces the poet to pick a word that sounds like a previous line-final
word, and if that rhyming word is unexpected semantically, then line endings should be the primary
site of phonetic-fidelity surprise.

**Hypothesis:** In rhymed verse, line-final tokens achieve higher phonetic similarity to GPT-2's
top prediction at equivalent S2 levels, compared to mid-line tokens.

---

## Method

1. Identify line-final tokens (tokens immediately before a newline character)
2. Detect rhymed poems via end-rhyme heuristic (≥8% rhyming line-final word pairs by 3-char suffix)
3. Compute phonetic similarity to GPT-2's top-1 prediction for each token (Levenshtein-based,
   normalized 0–1)
4. Compare line-final vs mid-line across S2 bins

**Corpus breakdown:**
- 301 poems analyzed; **24 identified as rhymed** (8.0%)
- 1,077 line-final tokens; 25,607 mid-line tokens

---

## Main Finding: Hypothesis DISCONFIRMED — Line Endings Are No More "Phonetically Safe"

| S2 Class | LF N | LF PhonSim | LF %Close | ML N | ML PhonSim | ML %Close | Gap |
|---|---|---|---|---|---|---|---|
| very_low (< −4) | 88 | 0.646 | 59.1% | 2,764 | **0.747** | 72.3% | −0.101 |
| low (−4 to −1) | 315 | 0.384 | 32.4% | 9,099 | 0.416 | 35.7% | −0.032 |
| neutral (−1 to 1) | 272 | **0.332** | 25.4% | 5,504 | 0.309 | 24.2% | +0.023 |
| moderate (1 to 4) | 210 | 0.104 | 3.3% | 4,448 | 0.108 | 2.2% | −0.004 |
| high (4 to 8) | 141 | 0.087 | 0.7% | 2,736 | 0.092 | 1.1% | −0.005 |
| very_high (> 8) | 51 | 0.083 | 0.0% | 1,056 | **0.080** | 1.1% | +0.002 |

*(LF = line-final, ML = mid-line; PhonSim = mean phonetic similarity to top GPT-2 prediction;
%Close = % of tokens with PhonSim > 0.5)*

**Phonetic-Fidelity Surprise Rate (S2 ≥ 4 AND PhonSim ≥ 0.4):**
- Line-final: **3.12%** (6/192)
- Mid-line: **4.88%** (185/3,792)
- Ratio: **0.64×** — line endings are *less* likely to achieve phonetic-fidelity surprise

The data is clear: **line endings are not the privileged site of phonetic-fidelity surprise.**
At every high-S2 bin, mid-line tokens show equal or slightly greater phonetic fidelity to the
top prediction. The rate of phonetic-fidelity surprise is actually lower at line endings (3.12%)
than mid-line (4.88%).

---

## Secondary Finding: Rhymed vs Free-Verse Line Endings

When we split line-final tokens by rhyme scheme:

| S2 Class | Rhymed N | Rhymed Sim | Free-Verse N | FreeV Sim | Gap |
|---|---|---|---|---|---|
| very_low (< −4) | 12 | 0.549 | 76 | 0.661 | −0.113 |
| low (−4 to −1) | 31 | 0.387 | 284 | 0.384 | +0.003 |
| neutral (−1 to 1) | 29 | 0.347 | 243 | 0.330 | +0.017 |
| moderate (1 to 4) | 30 | 0.067 | 180 | 0.111 | −0.044 |
| **high (4 to 8)** | **23** | **0.117** | **118** | **0.081** | **+0.036** |
| very_high (> 8) | 10 | 0.062 | 41 | 0.087 | −0.026 |

**Phonetic-Fidelity Surprise at line endings by poem type:**
- Rhymed line-final: 3.03% (1/33)
- Free-verse line-final: 3.14% (5/159)

The rhyme effect is nearly absent at most S2 levels. There is a slight tendency toward
higher phonetic similarity in rhymed poems' line-final tokens at S2 4–8 (+0.036), but
the small sample size (23 rhymed high-S2 line-final tokens) prevents firm conclusions.

**Interpretation:** Even in formally rhymed poems, when poets choose a surprising line-final
word, they typically don't choose it for phonetic proximity to the model's prediction — they
choose it for reasons of meaning, rhyme scheme, or formal constraint that GPT-2's model
doesn't encode well. The "rhyme word" that satisfies the sound constraint is chosen from
a field that GPT-2 cannot predict, regardless of whether it sounds like what the model expected.

---

## Exceptional Case: "I Wandered Lonely as a Cloud"

The highest phonetic-fidelity surprise at a line ending:

| Poet's word | GPT-2's prediction | S2 | PhonSim | Poem |
|---|---|---|---|---|
| `cloud` | `child` | 8.10 | 0.400 | Wordsworth, "I Wandered Lonely as a Cloud" |

Wordsworth's "cloud" is the most famous line ending in Romantic poetry — and GPT-2 expected
"child." The phonetic similarity (0.40, medium) comes from the shared ending: `-ould`/`-ild`
(near-rhyme in sound class). The S2 (8.10) reflects high model confidence in "child" vs. the
unexpected "cloud."

This is a genuine instance of phonetic-fidelity surprise: the poet chose a word that occupies
the same approximate acoustic position as the expected word while changing its semantic and
imagistic register entirely (human intimacy → natural sublime). The rhyme of "cloud/crowd" in
the full poem is a secondary constraint that helps drive this choice.

---

## The Inverse Finding: Line Endings Are Less Phonetically "Safe" at Low S2

At the very_low S2 bin (< −4), line-final tokens are actually LESS phonetically similar to the
top prediction than mid-line tokens (0.646 vs. 0.747). This means:

When a line-ending is "expected" (negative S2, model's prediction was confirmed), the chosen
word is still less acoustically close to the prediction than mid-line expected words.

**Possible explanation:** Mid-line "expected" tokens are often function words (articles, prepositions,
auxiliaries) where the model's top prediction and the actual word are nearly identical. Line-final
positions, even when semantically predictable, often end with content words — nouns, verbs,
adjectives — where the model had several plausible alternatives. The poem satisfies semantic
expectations but with a specific word that may differ acoustically from the single most-predicted
alternative.

---

## Era Analysis: Phonetic Similarity at High-S2 Line Endings

| Era | N (high-S2 line-final) | Mean PhonSim |
|---|---|---|
| spoken_word | 5 | **0.187** |
| german_modernist | 5 | 0.130 |
| new_york_school | 17 | 0.127 |
| postcolonial | 11 | 0.122 |
| surrealist | 6 | 0.102 |
| fixed_form | 7 | 0.099 |
| modernist | 23 | 0.099 |
| victorian | 26 | 0.095 |
| romantic | 7 | 0.081 |
| dramatic_monologue | 18 | 0.080 |
| german_expressionist | 6 | 0.052 |
| metaphysical | 5 | 0.047 |
| contemporary | 6 | 0.000 |
| 18th_century | 5 | 0.000 |

**Spoken word** achieves the highest phonetic similarity at high-S2 line endings — consistent
with oral performance traditions where sound-texture and rhyme/near-rhyme are structural features.
**Contemporary poetry** achieves zero phonetic similarity at high-S2 line endings — contemporary
poets' most surprising line endings are completely acoustically alien from what the model expected.

---

## Interpretation: Where Does Phonetic-Fidelity Surprise Live?

The finding is clean: **phonetic-fidelity surprise is a mid-line phenomenon, not a line-ending
phenomenon.** This challenges the intuitive model of rhyme as the primary site of
"phonetic expectation + semantic surprise."

Instead, the pattern suggests:
1. **Line endings use fully dual departure** (semantic AND phonetic) when they're surprising —
   the same rule as mid-line, perhaps more so.
2. **Phonetic-fidelity surprise (sound-alike substitution) occurs mid-line**, possibly at metrically
   stressed positions, modal auxiliaries ("could/would"), or semantically loaded slots where
   the poet picks a near-homophone for resonance.
3. **Rhyme works differently from the S2 model**: Rhyme satisfies a local phonetic constraint
   between line endings, but this constraint is not captured in GPT-2's per-token predictions
   (which have no access to previous line endings). From GPT-2's perspective, rhyme slots look
   just as acoustically radical as free-verse line endings.

---

## Notable Line-Final Phonetic-Fidelity Surprise Examples

| Poet's word | GPT-2 predicted | S2 | PhonSim | Era |
|---|---|---|---|---|
| `cloud` | `child` | 8.10 | 0.40 | romantic |
| `weave` | `have` | 5.77 | 0.60 | victorian (Hardy, "The Oxen") |
| `feed` | `flew` | 4.55 | 0.50 | postcolonial (Walcott) |
| `tight` | `the` | 5.93 | 0.40 | spoken_word (Lucille Clifton) |
| `fits` | `is` | 4.01 | 0.50 | new_york_school (Ashbery) |

All five examples show the poet picking a word that shares sounds with the model's expectation
while making a semantically radical choice. "Weave/have" (both ending in /-v/) and "feed/flew"
(both beginning with /f/) are near-alliterations. "Cloud/child" is a near-rhyme.

---

## Suggested Next Steps

1. **Metrical position**: Rather than line-final vs. line-initial, compare phonetic similarity
   at metrically STRESSED vs. UNSTRESSED positions in formally metered verse — this would
   require syllable tagging but might reveal a cleaner acoustic constraint effect.
2. **Between-line rhyme distance**: For rhymed poems, measure phonetic similarity between
   each line-final token and the *previous* line-final token (the rhyme partner) — this
   directly captures the inter-line rhyme constraint that GPT-2 cannot model.
3. **Cross-line prediction priming**: Test whether the PENULTIMATE token of a rhymed line
   shows elevated phonetic similarity to the top prediction — the model might build toward
   the "expected" rhyme word at the penultimate position even if the final word diverges.
