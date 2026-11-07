# Grammar Defiance Index: How Poetry Systematically Rejects Syntactic Prediction

**Date:** 2026-11-07  
**Analysis:** Corpus-level analysis of `results/corpus_results.json` (403 texts, 18,869 artifact-free tokens)  
**New corpus additions:** 8 poems added to test the hypothesis (Vaughan, Traherne, Crashaw, Thompson, Drayton, Bradstreet, Campion, Samuel Daniel) — will be analyzed on next corpus run  
**Research Question:** When GPT-2's top-10 alternatives are dominated by function words (grammar), does the poet systematically override this prediction? Does the override rate vary by poetic form and era?

---

## Background

Previous research established that the Straussian gap (S₂ = surprisal − entropy) captures moments where poets choose something unexpected when the model is confident. The "suppressed lexicon" shows that GPT-2 most commonly predicts function words, determiners, and conjunctions. This experiment asks: **Is poetic deviation from function-word prediction systematic and form-dependent?**

**Method**: For every artifact-free token with S₂ ≥ 1.5, classify the dominant token class in GPT-2's top-10 alternatives. When ≥ 7 of the 10 alternatives are function words, record whether the poet:
- **Breaks**: writes a non-function word (content word or punctuation)
- **Conforms**: writes a function word

The **Grammar Defiance Index (GDI)** = percentage of function-dominant predictions that the poet overrides.

---

## Finding 1: Grammar Defiance Is Universal — But Not Equal

**Corpus-wide GDI: 79.7%** — across all 403 poems, when GPT-2 predicts a function word with near-certainty (7+ of top-10 are function words), poets override this 4 out of 5 times.

| Era | GDI | Mean S₂ at breaks |
|---|---|---|
| **haiku** | **92.9%** | 6.65 |
| **double_dactyl** | **90.9%** | 4.69 |
| **clerihew** | **90.0%** | 6.07 |
| romantic | 89.9% | 5.43 |
| ballad | 89.2% | 5.38 |
| harlem_renaissance | 89.4% | 5.09 |
| german_expressionist | 88.2% | 5.02 |
| metaphysical | 86.8% | 5.13 |
| confessional | 86.7% | 5.52 |
| rondeau | 86.7% | 5.16 |
| ancient | 85.7% | 4.52 |
| ekphrastic | 85.0% | 4.90 |
| mid_century | 84.6% | 4.49 |
| dramatic_monologue | 83.1% | 5.03 |
| victorian | 81.4% | 5.33 |
| war_poetry | 81.4% | 4.68 |
| *…corpus average…* | *79.7%* | *5.33* |
| found_poetry | 67.3% | 5.44 |
| prose_poetry | 67.4% | 5.41 |
| **biblical** | **65.8%** | 5.01 |
| **song_lyrics** | **63.2%** | 5.51 |
| **black_arts** | **63.2%** | 4.17 |

**Key finding:** Haiku has the highest Grammar Defiance Index (92.9%). This is not surprising given haiku's extreme semantic compression — the form leaves almost no room for grammatical function words, maximizing content-per-token. The surprise is the **pattern at the bottom**: biblical (65.8%), song lyrics (63.2%), and Black Arts poetry (63.2%) show the most grammatical conformity.

---

## Finding 2: The Asymmetry of Defiance — What Poets Substitute

When rejecting function-word predictions, what do poets actually write?

| Chosen class | Count | % of all function-overrides |
|---|---|---|
| **content word** | 2,461 | **87.5%** |
| **punctuation** | 352 | **12.5%** |

The substitution asymmetry is remarkably clean: **87.5% of function-word overrides insert content words**. Punctuation substitutions (12.5%) represent poets cutting short a syntactic structure rather than extending it.

This confirms the Straussian Gap's core mechanism: **poetry is a systematic substitution of semantic content for grammatical structure**. When the model says "here comes grammar," the poet says "here comes meaning."

---

## Finding 3: Beat Poetry Has the Most Extreme Grammar-Override Moments

| Era | GDI | Mean S₂ at breaks | Max S₂ |
|---|---|---|---|
| **beat** | 81.0% | **7.28** | 16.6 |
| classical_chinese | 71.4% | **6.86** | — |
| concrete | 66.7% | **6.92** | — |
| haiku | 92.9% | 6.65 | — |
| *corpus average* | 79.7% | 5.33 | — |

Beat poetry has a GDI of 81% (slightly above average), but the **mean S₂ at function-override moments is 7.28** — the highest of any era with sufficient samples. This means that when Beat poets override grammar, they leap further. The model is surprised more deeply, not just more often.

---

## Finding 4: The Top Grammar-Override Moments Are Semantic Explosions

The 15 highest-S₂ function-word overrides in the corpus:

| S₂ | Author | Era | Context | Expected | Wrote |
|---|---|---|---|---|---|
| 22.7 | Anonymous (trans. Gordon) | old_english | `...that he` | ` may` (p=0.39) | `riot` |
| 19.8 | Charles Bukowski | spoken_word | `...inhale` | `\n` (p=0.85) | `cigarette` |
| 19.4 | Szymborska | contemporary | `...admirable number` | ` of` (p=0.86) | ` pi` |
| 19.4 | Swinburne | victorian | `...or ear` | `\n` (p=0.83) | `Wan` |
| 18.9 | William Stafford | mid_century | `...flute end of` | ` a` (p=0.38) | ` consequences` |
| 17.4 | Trad. Scottish ballad | ballad | `...Tay,` | `\n` (p=0.76) | `Bon` |
| 17.2 | John Keats | romantic | `''` | ` he` (p=0.43) | ` Music` |
| 16.8 | Kenneth Koch | new_york_school | `...think\nof` | ` you` (p=0.47) | ` mot` |
| 16.7 | Szymborska | contemporary | `...myself` | ` to` (p=0.67) | ` liking` |
| 16.6 | Gregory Corso | beat | `...So if` | ` you` (p=0.33) | ` neb` |
| 15.6 | Allen Ginsberg | beat | `...madness, starving` | ` to` (p=0.26) | ` hysterical` |

**Notable patterns:**
- The old English translation's `riot` after `that he` (S₂ = 22.7) shows how translation amplifies syntactic defiance — the original kenning structure has no equivalent English grammar.
- Bukowski's `cigarette` after `inhale` (S₂ = 19.8) is a classic Beat content-extension: the model expected the line to end after `inhale`, but Bukowski specifies.
- Szymborska's ` pi` (S₂ = 19.4) is the most striking: the model predicts ` of` after "admirable number" — a perfectly reasonable, grammatically expected continuation — and Szymborska inserts the mathematical symbol for infinity.
- Ginsberg's `hysterical` after `madness, starving` (S₂ = 15.6) is the seed of Howl's infamous opening: "I saw the best minds of my generation destroyed by madness, starving / hysterical / naked" — the three adjectives form a cascade where each is more unexpected than grammar expects.

---

## Finding 5: The Low-Defiance Cluster Reveals Genre Conventions

**Biblical poetry (65.8%)** and **song lyrics (63.2%)** have the lowest GDI. These genres share a characteristic: **formulaic language**. Biblical verse uses fixed invocations and parallelism; song lyrics must set to melody, which requires syllabic predictability. Both conventions partially restore the function words that lyric poetry typically strips away.

**Black Arts poetry (63.2%)** is the most surprising outlier. The Black Arts movement (Amiri Baraka, Sonia Sanchez, Nikki Giovanni) used vernacular speech rhythms and declarative syntax — both features that may preserve more grammatical structure even in highly charged political verse. This warrants further investigation.

---

## Corpus Additions for Next Analysis

Eight new poems were added to test the hypothesis that **ornate baroque sacred verse** (Vaughan, Traherne, Crashaw, Thompson) shows higher GDI than **direct, plain-style early modern verse** (Drayton, Bradstreet, Campion, Daniel):

| Poet | Work | Era | Predicted GDI |
|---|---|---|---|
| Henry Vaughan | "The World" | metaphysical | High (unusual imagery, inverted syntax) |
| Thomas Traherne | "Wonder" | metaphysical | High (accumulative, mystical) |
| Richard Crashaw | "A Hymn of the Nativity" | metaphysical | Very high (baroque, ornate conceits) |
| Francis Thompson | "The Hound of Heaven" (opening) | victorian | High (dense imagery, compressed syntax) |
| Michael Drayton | "Since there's no help" | early_modern | Moderate (clear syntax, emotional directness) |
| Anne Bradstreet | "To My Dear and Loving Husband" | early_modern | Moderate (Puritan plain style) |
| Thomas Campion | "My Sweetest Lesbia" | early_modern | Moderate (compressed, musical) |
| Samuel Daniel | "Care-charmer Sleep" | early_modern | Moderate (Petrarchan formalism) |

---

## Corpus Additions: Results

The 8 new poems were analyzed. The hypothesis that **ornate baroque sacred verse would have higher GDI** than **plain-style early modern verse** was **not confirmed** in the expected direction — but yielded a more interesting finding:

| Poet | Work | Predicted Style | avg_S₂ | GDI |
|---|---|---|---|---|
| Thomas Campion | "My Sweetest Lesbia" | lute song (musical) | **+1.10** | 92% |
| Francis Thompson | "The Hound of Heaven" | ornate Victorian | **+0.67** | 76% |
| Richard Crashaw | "A Hymn of the Nativity" | baroque Catholic | **+0.47** | 90% |
| Thomas Traherne | "Wonder" | metaphysical mystical | -0.13 | 83% |
| Anne Bradstreet | "To My Dear and Loving Husband" | Puritan plain | -0.11 | 82% |
| Henry Vaughan | "The World" | metaphysical mystical | -0.20 | 92% |
| Michael Drayton | "Since there's no help" | Petrarchan direct | -0.37 | 93% |
| Samuel Daniel | "Care-charmer Sleep" | Petrarchan formal | **-0.61** | **100%** |

**Key finding**: Samuel Daniel has **100% GDI** (he overrides every single function-dominant prediction) but the **lowest avg_S₂ (-0.61)**. This is the GDI-S₂ paradox: **Daniel always refuses grammar's demand, but his content words are exactly what the model expects once it adjusts for the class override.** He is a maximally defiant syntactician but a conformist semantic poet.

**Campion (+1.10)** achieves the highest avg_S₂ — higher than any of the ornate baroque poets — with a compact, musical style rather than ornamental density. His brief lute song structure forces maximum semantic weight into every token.

**Thompson (76%)** has the lowest GDI despite being predicted high, because his dense imagery creates so many content-word-dominant prediction windows (reducing the function-dominant windows where GDI is measured).

This reveals a **GDI-S₂ decoupling**: GDI measures *whether* a poet breaks grammar; avg_S₂ measures *how far* they go when they break anything. These are independent axes of poetic deviation.

---

## Theoretical Significance

The Grammar Defiance Index quantifies a core property of poetic language: **systematic anti-syntactic behavior**. Where prose follows grammar's probability distribution, poetry inverts it. The 79.7% corpus-wide GDI means that when the model is most confident about grammar, the poet is most likely to refuse that confidence.

This is the information-theoretic signature of verse as a *form of linguistic resistance*: not randomness (which would yield ~50%), but **structured defiance** — the selective insertion of semantic content precisely at the moments grammar is most demanding.

The form hierarchy (haiku > fixed form > lyric > song lyrics > biblical) suggests that **formal constraint paradoxically increases semantic defiance**: tighter syllabic forms must pack more meaning into fewer tokens, systematically overriding grammatical expectations to do so.

---

## Next Steps

1. **Run corpus analysis on the 8 new poems** to compare baroque vs. plain-style early modern GDI
2. **Test within-poem GDI arc**: does defiance increase or decrease as a poem progresses? (Does the reader's attuned expectation become easier to defy?)
3. **GDI as poet fingerprint**: is GDI consistent within a poet's work and distinctive across poets?
4. **Is high GDI correlated with critical reception or canonicity?** (Do more "difficult" canonical poems have higher GDI?)
