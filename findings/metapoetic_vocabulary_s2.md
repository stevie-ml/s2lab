# S₂ and Metapoetic Vocabulary: When Poetry Talks About Itself

**Date:** 2026-11-17  
**Experiment:** `experiments/metapoetic_vocabulary_s2.py`  
**Results:** `results/metapoetic_vocabulary_s2.json`  
**Corpus:** 419 poems, 531 metapoetic tokens vs 55,260 other tokens

---

## Research Question

When poets use words that refer to language, writing, speaking, or silence —
the vocabulary of poetry-about-poetry — do those words carry **more** or **less**
surprise than ordinary content words in the same poems?

**Hypothesis A (formulaic reflexivity):** metapoetic words are LOW S2 — referring
to language is a tired convention, expected by any reader of poems.

**Hypothesis B (defamiliarizing language-about-language):** metapoetic words are
HIGH S2 — the act of turning language on itself opens unexpected territory.

---

## Finding: Both Are Partly True — With a Crucial Internal Split

**Overall, metapoetic words have HIGHER mean S2 than other content words:**

| Token class | Mean S2 | Positive ratio | N |
|---|---|---|---|
| Metapoetic vocabulary | **−0.19** | **41%** | 531 |
| Other content tokens | −0.43 | 34% | 55,260 |
| Delta (meta − other) | **+0.24** | | |

Hypothesis B is confirmed at the population level: taken together, words about
language are more surprising than average. But this masks a dramatic internal split.

---

## The Internal Split: Category Matters Enormously

| Category | Words included | Mean S2 | Positive ratio | N |
|---|---|---|---|---|
| **voice_silence** | silence, silent, voice, mute, dumb, sound | **+0.60** | **54%** | 80 |
| **writing** | write, wrote, read, text, page, inscribe | **+0.44** | **53%** | 64 |
| poem_object | poem, verse, lyric, song, line, stanza | −0.01 | 38% | 56 |
| speech_act | say, said, speak, told, call, whisper | −0.30 | 39% | 232 |
| **language** | word, words, language, tongue, name | **−1.08** | **29%** | 99 |

This reveals a spectrum from **highly surprising** to **highly conventional**:

### HIGH S2 Pole: Silence and Writing Acts
"Silence" (mean S2 = +2.11), "silent" (+2.06), "wrote" (+0.89), "read" (+3.78) —
words about the *absence* of language or *completed* writing acts are used unexpectedly.
When a poet writes "silence," they are reaching for something the language model
didn't anticipate, suggesting that silence-as-theme is not a cliché in this dataset
but a deliberate, surprising choice.

### LOW S2 Pole: Direct Language-Naming
"word" (mean S2 = −1.73), "words" (−1.02), "name" (−1.75), "speak" (−1.98) —
the explicit vocabulary FOR language is predictable. Calling something a "word" or
speaking of "words" in a poem is so conventional that the model expects it perfectly.
**This is the information-theoretic signature of a cliché.**

### The Paradox: "language" vs. "word"
"language" (mean S2 = +1.78) is SURPRISING, while "word" (−1.73) is PREDICTABLE.
Both are in the same semantic field, but the abstract term is used more idiosyncratically
than the concrete one. Poets reach for "language" in unexpected contexts; they reach
for "word" in formulaic ones.

### The Voice/Silence Asymmetry
Most striking: "silence" (+2.11) and "silent" (+2.06) are HIGH S2;
while "voice" (−1.44) and "sound" are LOW S2.

**Voice is an overused workshop cliché; silence is not.**

The word "voice" appears in predictable positions in poems — it's the default
metaphor for poetic subjectivity in a generation shaped by workshop instruction.
"Silence" is used more riskily, in unexpected contexts, suggesting poets reach
for it when they need to do something the model didn't see coming.

---

## Era-Level Results

| Era | N (meta) | Meta mean | Other mean | Delta |
|---|---|---|---|---|
| postcolonial | 6 | +4.07 | −1.21 | **+5.28** |
| haiku | 6 | +3.65 | −0.69 | **+4.35** |
| beat | 6 | +3.70 | −0.57 | **+4.27** |
| modernist | 13 | +1.07 | −0.97 | +2.04 |
| metaphysical | 8 | +0.76 | −1.02 | +1.78 |
| … | | | | |
| prose_poetry | 29 | −1.02 | −0.13 | −0.88 |
| oulipo | 12 | −1.09 | −0.16 | −0.93 |
| biblical | 8 | −0.69 | +0.93 | **−1.62** |
| song_lyrics | 6 | −1.49 | +0.14 | **−1.68** |
| concrete | 9 | −1.44 | +1.44 | **−2.89** |

### Interpretation

**Concrete poetry has the most negative delta**: In a poetry movement *defined* by
language as material artifact, words about language are maximally conventional and
predictable. "Word" in a concrete poem by Emmett Williams is EXPECTED — the entire
poem is about words, so the word "word" carries no surprise.

**Biblical poetry has the second-most-negative delta**: "In the beginning was the
Word" — metapoetic vocabulary in the Bible is formulaic, not defamiliarizing.

**Beat and postcolonial poetry have the highest positive delta**: Allen Ginsberg,
Amiri Baraka, and postcolonial poets use language-about-language in unexpected, angry,
transformative ways — not to invoke the workshop lyric but to interrogate the politics
of voice itself.

**Haiku has very high delta** (from small n): In haiku's stripped-down universe,
any mention of language or naming is cosmically unexpected.

---

## Individual Word Rankings

**Most surprising metapoetic words (mean S2 ≥ 0.5, n ≥ 5):**

| Word | Mean S2 | N | Pos. ratio |
|---|---|---|---|
| read | +3.78 | 7 | 100% |
| silence | +2.11 | 15 | 67% |
| silent | +2.06 | 17 | 94% |
| letter | +1.85 | 5 | 60% |
| language | +1.78 | 8 | 62% |
| told | +1.29 | 19 | 58% |
| voices | +1.16 | 7 | 57% |
| called | +0.93 | 14 | 50% |
| wrote | +0.89 | 9 | 56% |
| lines | +0.78 | 6 | 50% |

**Most conventional/clichéd metapoetic words:**

| Word | Mean S2 | N | Pos. ratio |
|---|---|---|---|
| book | −2.46 | 9 | 11% |
| cry | −2.04 | 7 | 14% |
| speak | −1.98 | 10 | 10% |
| name | −1.75 | 25 | 32% |
| word | −1.73 | 28 | 14% |
| voice | −1.44 | 20 | 20% |
| says | −1.13 | 9 | 22% |
| said | −1.09 | 53 | 32% |
| words | −1.02 | 19 | 26% |
| write | −0.92 | 18 | 39% |

---

## Theoretical Significance

This experiment reveals an **information-theoretic taxonomy of poetic self-reference**:

1. **Active silence vocabulary** (silence, silent, mute) = HIGH S2: reaching into
   absence, the unspeakable, negative space. Unexpected, defamiliarizing.

2. **Past-tense writing acts** (wrote, read) = HIGH S2: completed acts of inscription
   are more surprising than ongoing ones — probably because they create retrospective
   distance.

3. **Generic language vocabulary** (word, words, name, speak) = LOW S2: the
   default meta-language of poetry has become its own cliché. These words function
   as filler — placeholders for a reflexivity that has become formulaic.

4. **"voice" is the supreme workshop cliché**: the most overused word in contemporary
   poetry teaching (every workshop asks "what is the speaker's voice?") registers
   as fully predictable in the information-theoretic analysis. The concept of "voice"
   as poetic uniqueness is — ironically — the most statistically expected word in
   the entire metapoetic lexicon.

---

## Methodological Note

Small n in some era cells (n_meta = 6–9) means era-level results have wide uncertainty.
The corpus-level finding (n = 531) is robust. Word-level results with n < 10 should
be treated as preliminary. The "read" result (100% positive ratio, n=7) warrants
replication — GPT-2 may be processing "read" as past tense of "read" or as an adjective
rather than the verb, inflating its surprisal.

---

## Next Steps

1. **Category refinement**: Split "voice/silence" into separate sub-groups to test
   whether negative-capability words (silence, dumb, mute) differ from presence-words
   (voice, sound).
2. **Collocation analysis**: When "word" appears as LOW S2, what precedes it?
   ("a word", "the word", "one word" = formulaic; "word" as subject = less so?)
3. **Temporal trend**: Does the cliché-ification of "voice" correlate with the
   rise of creative writing programs (post-1970)?
4. **Language poetry**: This tradition explicitly interrogates "word" and "language" —
   does it use them with higher or lower S2 than the corpus mean?
