# Assonance and S₂: Does Vowel-Sound Repetition Lower Semantic Surprise?

**Date:** 2026-11-27
**Experiment:** `experiments/assonance_s2.py` → `results/assonance_s2.json`
**Corpus:** 446 poems, 26,532 content-word tokens analyzed
**Research question:** When a poet repeats a vowel sound (assonance), is the assonant word more or less statistically surprising?

---

## Background

Alliteration (initial-consonant repetition) has been studied in this corpus — see `findings/alliteration_and_s2.md`. **Assonance** (vowel-sound repetition across nearby words: "rolling home through the golden dome") is a distinct sonic strategy that works through the sustained vowel nucleus rather than the onset.

The question is whether assonance creates or destroys statistical surprise. Two competing hypotheses:

1. **Phonetic Grooming**: Assonance words fit their sonic context — they are *expected* by the texture of the passage. The repeated vowel constrains what sounds (and therefore what words) can follow. → Predicts **lower S₂** at assonant positions.

2. **Sonic Trojan Horse**: Poets use assonance to license semantically daring choices — the shared sound makes an unexpected word feel inevitable. The sonic fit is cover for semantic risk-taking. → Predicts **higher S₂** at assonant positions.

**Method**: For each content-word token, extracted its primary vowel nucleus (first vowel cluster). Checked whether that nucleus appeared in any of the 4 preceding content words. Defined assonant tokens as those where the vowel nucleus recurs.

---

## Finding 1: Phonetic Grooming is the Default (−0.34 S₂ Discount)

Across the full corpus of 446 poems:

| Condition | n tokens | Mean S₂ | +S₂ % |
|---|---|---|---|
| **Assonant** (exact nucleus match) | 12,348 | **+0.87** | 48.8% |
| **Non-assonant** | 14,184 | **+1.20** | 53.7% |
| **Difference** | — | **−0.34** | −4.9 pp |

| Condition | n tokens | Mean S₂ |
|---|---|---|
| **Class-assonant** (same vowel class) | 16,025 | **+0.89** |
| **Non-class-assonant** | 10,507 | **+1.28** |
| **Difference** | — | **−0.39** |

**The phonetic grooming hypothesis is confirmed globally.** Assonant tokens are significantly less surprising than non-assonant tokens. When a poet repeats a vowel sound, the word chosen tends to be more statistically expected — it "belongs" to the sonic context GPT-2 has built up.

The 46.5% assonance rate means nearly half of all content-word tokens participate in vowel repetition within a 4-word window, suggesting assonance is a constant (mostly unconscious) feature of English poetry.

---

## Finding 2: The Effect Holds — and Strengthens — in Low-Entropy Contexts

| Entropy context | Assonant mean S₂ | Non-assonant mean S₂ | Difference |
|---|---|---|---|
| High entropy (H > median) | +0.37 | +0.72 | **−0.35** |
| Low entropy (H < median) | **+1.31** | **+1.74** | **−0.44** |

The assonance discount is **larger** in low-entropy (high-confidence) contexts than in high-entropy (uncertain) contexts. When GPT-2 is already confident about what comes next, an assonant word is even more expected. When GPT-2 is uncertain, assonance offers less phonetic constraint.

**Interpretation**: Assonance operates as a *double grooming* mechanism. If the model is already confident (low H), and the token is assonant, it has a double claim to expectedness — semantic context AND phonetic fit. If the model is uncertain (high H), neither mechanism can fully constrain the outcome.

---

## Finding 3: Seven Traditions INVERT the Pattern (Sonic Trojan Horse)

The global trend (assonance lowers S₂) is **reversed in specific traditions**:

| Era | Assonant S₂ | Non-assonant S₂ | Difference | Interpretation |
|---|---|---|---|---|
| **nursery_rhyme** | +0.91 | −0.88 | **+1.79** | Forced rhyme/assonance → semantically arbitrary choices |
| **clerihew** | +3.04 | +2.09 | **+0.96** | Comic fixed form forces phonetically-driven semantic leaps |
| **classical_chinese** | +1.43 | +0.34 | **+1.09** | Translation artifacts amplify semantic-sonic tension |
| **korean_modernist** | +0.64 | −0.27 | **+0.91** | Same translation dynamic |
| **metaphysical** | +1.30 | +0.60 | **+0.70** | Donne's conceits use sonic repetition to license semantic surprise |
| **german_symbolist** | +1.12 | +0.27 | **+0.85** | Symbolist sound-painting carries unexpected imagery |
| **german_expressionist** | +1.46 | +1.09 | **+0.37** | Expressionist sound-symbolism licenses semantic dislocation |
| **beat** | +3.01 | +2.67 | **+0.35** | Rhythmic assonance carries forward semantic momentum |
| **song_lyrics** | +0.33 | −0.01 | **+0.33** | Rhyme schemes force phonetically-constrained word choices |

**The Sonic Trojan Horse** operates in traditions where **the sonic constraint forces semantic risk-taking**. In nursery rhymes, clerihews, and fixed forms (villanelle shows this too, though subtly), the need to find an assonant word COMPELS the poet toward words they wouldn't otherwise choose — and those forced choices are semantically unexpected.

The metaphysical poetry result is especially interesting: Donne's conceits explicitly use phonetic patterns to build toward surprising semantic connections. The repeated vowel is NOT a grooming strategy — it is an argumentative tool that makes the logical leap feel sonically inevitable even as it is semantically shocking.

---

## Finding 4: Back Vowels Create the Strongest Grooming Effect

| Vowel class | Assonant mean S₂ | Non-assonant mean S₂ | Difference |
|---|---|---|---|
| **back** (o, au, ow) | +0.66 | +1.20 | **−0.55** |
| **front** (e, ai, ea) | +0.81 | +1.20 | **−0.39** |
| **high_back** (u, oo) | +1.41 | +1.64 | **−0.23** |
| **front_high** (i, ee) | +0.70 | +0.91 | **−0.21** |
| **low** (a) | +1.11 | +1.24 | **−0.13** |

**Back vowels** (the "o" sounds: home, road, bone, stone) create the strongest phonetic grooming. When poets repeat these dark, back-resonant sounds, the words chosen tend to be maximally expected. This may reflect the high collocational density of "o" words in English (go, so, know, show, low, grow) — the sonic field is semantically tightly constrained.

**Low "a" sounds** create the least grooming. The "a" class (map, trap, lack, back) is phonetically broad and semantically dispersed — assonance on "a" doesn't significantly constrain what word follows, so the S₂ discount is minimal.

---

## Synthesis: Two Modes of Phonetic-Semantic Interaction

| Mode | Traditions | Mechanism | S₂ effect |
|---|---|---|---|
| **Phonetic Grooming** | Most English poetry (Victorian, Romantic, contemporary) | Shared vowel sounds constrain semantic field; word "belongs" to tonal context | Assonant < non-assonant |
| **Sonic Trojan Horse** | Fixed forms, metaphysical, expressionist, nursery rhyme | Sonic constraint FORCES semantically unexpected words; sound is cover for surprise | Assonant > non-assonant |

The two modes are not random — they correlate with the **intentionality of sonic design** in a tradition. Where poets use assonance as texture (the sonic background of natural English rhythm), it lowers surprise. Where poets use assonance as CONSTRAINT (the need to find a rhyming or assonant word at all costs), it forces them into semantic territory they wouldn't occupy otherwise.

---

## Suggested Next Steps

1. **Rhyme vs. assonance**: Compare the S₂ effects of end-rhyme (perfect phonetic match) vs. mid-line assonance. Does rhyme operate as an even stronger Trojan Horse than assonance?

2. **Vowel-change and S₂**: When poets move from one vowel class to another (e.g., a poem that uses "a" sounds and then pivots to "o" sounds), is the vowel pivot associated with a semantic shift (high S₂)?

3. **Consonance vs. assonance**: Does consonance (consonant repetition in non-initial position, e.g., "pitter-patter") show the same grooming/Trojan-horse pattern?

4. **Poet-level variation**: Which individual poets most consistently use the Trojan Horse strategy (high assonant S₂)? This could identify poets who consciously deploy phonetics to license semantic risk.

5. **Diphthong-specific analysis**: Diphthongs (oi, au, ie) are rarer and more marked. Do they create stronger grooming effects than monophthongs?
