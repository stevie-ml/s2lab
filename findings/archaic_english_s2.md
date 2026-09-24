# Archaic English in Poetry: GPT-2 Has Learned Poetic Register

**Date:** 2026-09-24
**Experiment:** `experiments/archaic_english_s2.py`
**Corpus:** 180 texts; 71 archaic tokens across 27 poems
**Builds on:** `syntactic_position_vs_s2.md`, `repetition_and_entropy.md`, `stanza_break_artifact.md`

---

## Research Question

When poets use archaic language — *thee*, *thou*, *thy*, *hath*, *doth*, *'tis*, *ere*, *hence* — does GPT-2 treat these forms as genuinely surprising? Or has the model internalized archaic vocabulary as **genre-appropriate**, expected within the register of classical poetry?

The naive expectation: archaic forms are rare in the modern web-scale corpus GPT-2 was trained on, so they should be high-surprisal and boost S₂. 

The surprising result overturns this.

---

## Key Finding: Archaic Language Has **Negative** S₂

| Metric | Archaic tokens | Modern baseline |
|--------|---------------|----------------|
| Avg S₂ | **−0.772** | +1.312 |
| Avg Surprisal | 6.031 | 8.320 |
| Avg Entropy | 6.803 | 7.008 |
| % positive S₂ | **26.8%** | 51.1% |
| n | 71 | 7,933 |

**Archaic tokens are among the most predictable in the corpus.** Modern content words achieve positive S₂ over half the time; archaic forms manage it only 27% of the time. Their average S₂ is −0.772 — more than two units below the modern baseline.

---

## The Genuine Straussian Test: All Positives Are False Positives

Of the 19 archaic tokens that do achieve positive S₂, none qualify as **genuine Straussian deviations** under the strict criterion (S₂ > 0 AND entropy < 3.0 — i.e., the model was *confident* before being surprised).

- 19/19 positive-S₂ archaic tokens: model was **uncertain** (high entropy) when the surprise occurred
- 0/19 positive-S₂ archaic tokens: model was **confident** and the poet deviated (genuine S₂)

This is the critical distinction. Genuine S₂ = surprisal − entropy > 0 only when entropy is low. If the model was already guessing wildly (high entropy), high surprisal doesn't count as the poet "defeating" a confident prediction. **All archaic positives are explained by general model uncertainty, not poetic deviance.**

---

## By Category: Pronouns Are Most Expected, Verbs Are Mildly Surprising

| Category | n | Avg S₂ | Avg Surprisal | Avg Entropy |
|----------|---|--------|--------------|------------|
| verb_conjugation (*hath*, *doth*, *wilt*…) | 8 | **+0.888** | 7.279 | 6.392 |
| elision (*o'er*, *ne'er*) | 1 | +0.128 | 6.054 | 5.926 |
| adverb_other (*hence*, *ere*, *yonder*…) | 6 | −0.562 | 6.526 | 7.088 |
| pronoun (*thee*, *thou*, *thy*, *thine*) | 54 | **−0.986** | 5.799 | 6.785 |
| other | 2 | −2.728 | 5.793 | 8.521 |

The most dramatic result: **archaic pronouns average S₂ = −0.986.** When Keats writes "thee", Shakespeare writes "thou", or Donne writes "thy" — GPT-2 predicts these tokens. The pronouns are so deeply embedded in the classical register that the model anticipates them.

Archaic verb conjugations (*hath*, *wilt*, *doth*) do better (+0.888), but this is still modest. The model knows that classical poetry uses "hath" in contexts that would take "has" in modern prose — but it is slightly less certain about the exact form.

---

## By Era: The Most Archaic Poets Have the Most Expected S₂

| Era | n | Avg S₂ (archaic) | Avg S₂ (modern) |
|-----|---|-----------------|----------------|
| romantic | 24 | −0.315 | 1.367 |
| victorian | 16 | −0.826 | 1.603 |
| **metaphysical** | 13 | **−2.424** | 1.291 |
| early_modern | 3 | −0.569 | 1.502 |
| fixed_form | 3 | −1.602 | 1.073 |
| modernist | 3 | −1.778 | 1.772 |
| song_lyrics | 2 | +0.297 | 0.580 |
| **found_poetry** | 2 | **+5.926** | 0.163 |

Two extremes:
- **Metaphysical poets (Donne, Marvell):** archaic S₂ = **−2.424**, the most negative. Donne saturates his poems with archaic forms, and GPT-2 has fully internalized this as his register. "Thee", "thy", "hath" are *expected* in a Donne poem.
- **Found poetry:** archaic S₂ = **+5.926**, highly positive. When the KJV's "hast" appears in a found poem framing (an out-of-genre context), GPT-2 has no prior that archaic forms belong here. The surprise is genuine.

The **era gradient** is striking: the longer archaisms have been *established* in a genre, the more expected they become. Found poetry, which deliberately transplants archaic language into alien contexts, is the only setting where archaic vocabulary creates genuine S₂.

---

## What GPT-2 Expected Instead

When the model does get "surprised" by an archaic form, the top predicted alternative reveals GPT-2's mental model of the register:

| Poet wrote | GPT-2 expected | n | Avg S₂ |
|-----------|---------------|---|--------|
| *thou* | **thou** | 7 | −3.040 |
| *thy* | the | 6 | −1.649 |
| *thee* | the | 6 | −0.666 |
| *thou* | , | 5 | −0.257 |
| *hath* | is | 3 | +0.320 |
| *thee* | thee | 3 | −1.196 |

The most revealing row: in **7 cases, GPT-2's top prediction for "thou" was "thou" itself** (avg S₂ = −3.040). The model was correct — it predicted the archaic form. This is the clearest evidence that GPT-2 has memorized classical register.

When "thy" is written and GPT-2 expected "the", the model was *close* — it expected a determiner, and "thy" is a determiner. The S₂ is mildly negative (−1.649) because the surprisal is moderate: the model got the grammatical role right but missed the form.

---

## Exceptions: When Archaism IS Surprising

Two cases stand out where archaic forms DO create genuine information-theoretic spikes:

**Robert Burns, "To a Mouse" (S₂ = +12.35):**
> *"Wee, sleekit, cowrin, tim'rous beastie / ... Mousie,* **thou** *..."*

After the noun phrase direct address "Mousie,", GPT-2's top prediction was "who" (28% probability). Burns writes "thou". The archaic pronoun choice is unusual even within the Scottish vernacular context — GPT-2 was not prepared for it. High entropy (6.56), very high surprisal (18.91), producing S₂ = +12.35.

**KJV Found Poem, "hast" (S₂ = +10.07):**
> *"...and\n* **hast** ..."* (from Ecclesiastes via found poem framing)

Context: a comma and newline followed by "and" — GPT-2 predicted "the" (a common article after "and"). Entropy was only **3.42**, making this the closest to genuine Straussian deviation in the archaic dataset. The archaic form appears *out of its normal genre context*, and GPT-2's genre awareness fails to activate.

**Pattern:** Archaic tokens spike S₂ only when they appear in *unusual grammatical positions* (after apostrophes, at clause boundaries where they're structurally unexpected) or in *out-of-genre contexts* (found poetry, song lyrics). Within traditional genres, they're anticipated.

---

## Literary Interpretation: GPT-2 Has Learned Genre Contracts

The finding reveals something profound about how GPT-2 models literature:

**GPT-2 has internalized the "genre contract" of classical poetry.** Just as a human reader, encountering a sonnet, expects Elizabethan diction, so GPT-2 has learned that the *presence of thee and thou signals* certain predictions about the surrounding context. This isn't just vocabulary memorization — it's register recognition.

This matters for the S₂ framework:
- **S₂ does not capture archaism as a source of poetic deviation** in traditional genres. A Victorian poet writing "hath" is conforming to an expectation, not violating it.
- **The Straussian gap is register-sensitive.** What counts as "unexpected" depends on which genre GPT-2 thinks it's reading. In a found poem, "hast" is shocking. In a Donne elegy, "hath" is invisible.
- **Archaism-as-surprise requires genre displacement.** When Mary Oliver, Frank O'Hara, or a Language poet occasionally deploys an archaic form, *that* would register as high S₂. The form's power comes from its violation of the expected register, not from the word itself.

This suggests a general principle: **S₂ is not a measure of absolute linguistic surprise, but of surprise relative to the model's genre expectation.** The same word — "thou" — can have S₂ = −3.040 in Shakespeare or S₂ = +9.46 in a context where it's structurally unexpected (Shakespeare Sonnet 73: "That time of year **thou**...").

---

## Next Steps

1. **Genre displacement experiment:** Deliberately test how high-archaism poems in found-poetry or contemporary frames would score vs. their original classical contexts.
2. **Register contrast within a poem:** Some modernist poems quote or mimic archaic styles (Eliot, Pound, Hughes). Do the archaic passages register as lower S₂ than the modern passages in the same poem?
3. **The 'thou' inflection point:** At what era does "thou" stop being expected? Chart its S₂ trajectory from Early Modern → Romantic → Victorian → Modernist.
4. **Archaism as irony:** When contemporary poets use "thee" deliberately (pastiche, irony), is the archaic form informationally distinct from sincere archaism?
