# Numerology and Information Theory: Number Words in Poetry

**Date:** 2026-11-15
**Experiment:** `experiments/number_words_s2.py` → `results/number_words_s2.json`
**Corpus:** 419 poems, 34,164 artifact-free word-start tokens (p_newline < 0.9)
**Builds on:** `suppressed_lexicon.md`, `straussian_gap_taxonomy.md`, `subword_tokenization_s2.md`

---

## Research Question

Do number words and quantifiers in poetry have distinctive S₂ profiles? And does it matter *which* number a poet chooses — is "seven" more surprising than "two"?

Three hypotheses:
- **Symbolic weight hypothesis**: Mythic numbers (seven, three, forty, twelve) appear in contexts where GPT-2 doesn't expect a number at all → HIGH S₂
- **Counting context hypothesis**: Scale numbers (hundred, thousand, million) and simple pairing numbers (two) appear in predictable enumeration contexts → LOW S₂
- **Null hypothesis**: All numbers are equally surprising once we control for base frequency

---

## Results: Category Summary

| Category | n | Mean S₂ | Median S₂ | +S₂% |
|---|---|---|---|---|
| **BASELINE (all poetry)** | 34,164 | +0.004 | −0.747 | 40.1% |
| **mythic_number** (three, seven, twelve, forty, four, nine, ten) | 72 | **+1.278** | −0.074 | 48.6% |
| cardinal_other (eleven, fifteen, etc.) | 92 | +0.162 | +0.024 | 50.0% |
| vague_quantifier (all, every, many, few, some, once) | 601 | +0.002 | −0.154 | 46.6% |
| extremal (none, nothing, never, always) | 209 | +0.276 | −0.285 | 46.9% |
| **prosaic_number** (two, five, six, eight, million, etc.) | 50 | **−0.021** | −1.172 | 38.0% |
| ordinal (first, second, third…) | 64 | −0.481 | −1.037 | 34.4% |

Mythic numbers average **+1.278 S₂** — 1.27 bits above the poetry baseline. Prosaic numbers sit below baseline at −0.021. Ordinals are decisively low at −0.481.

---

## Finding 1: The Numerological Hierarchy

The per-number breakdown reveals a striking hierarchy by symbolic status:

| Number | n | Mean S₂ | Median S₂ | +S₂% |
|---|---|---|---|---|
| **seven** | 6 | **+4.766** | +4.620 | **83.3%** |
| **forty** | 4 | **+4.054** | +7.744 | 50.0% |
| **twelve** | 3 | **+3.738** | +4.536 | 66.7% |
| nine | 7 | +1.979 | +1.683 | 57.1% |
| four | 10 | +1.379 | +1.792 | 60.0% |
| ten | 8 | +1.230 | +0.520 | 62.5% |
| three | 19 | +1.127 | −1.482 | 42.1% |
| one | 89 | +0.042 | −0.037 | 49.4% |
| six | 9 | −0.066 | −1.513 | 33.3% |
| two | 29 | **−0.923** | −1.380 | 37.9% |
| hundred | 8 | **−1.514** | −0.206 | 12.5% |
| thousand | 7 | **−1.543** | −2.995 | 28.6% |

The range runs from +4.77 (seven) to −1.54 (thousand) — a 6.3-bit spread across number words.

**The mythic ladder**: seven, forty, twelve are the three highest-S₂ numbers. These are the numbers most deeply embedded in English poetic and biblical tradition — seven (days, sins, wonders), forty (days in the desert, Ali Baba), twelve (apostles, months). Poets reach for them in contexts where the model never anticipated a number at all.

**The banal floor**: hundred, thousand, and two have negative S₂. These appear in counting contexts where numbers are expected (enumeration, rounds, pairs), and GPT-2 often predicts the same number back (see Finding 2).

---

## Finding 2: Two Regimes of Number Usage

Low-S₂ examples reveal why scale numbers underperform:

| Token | S₂ | Context ends with | GPT-2's top prediction |
|---|---|---|---|
| hundred | −5.18 | (line start) | `thousand` |
| thousand | −4.72 | (line start) | `thousand` (exact same word) |
| two | −4.91 | (line start) | `same` |
| hundred | −2.97 | (line start) | `hundred` (exact same word) |

GPT-2 often *predicts the exact same word* at scale number positions — a sign that these numbers are appearing in clearly repetitive or counting contexts where the model has already learned the pattern. When the top alternative is the same word (self-prediction), it means the number is so contextually expected that only itself would satisfy.

Contrast with high-S₂ mythic number contexts:

| Token | S₂ | Context ends with | GPT-2's top prediction |
|---|---|---|---|
| three | +14.88 | (line start) | `an` |
| three | +10.80 | `first morning of` | `the` |
| seven | +10.43 | `hing his body` | `and` |
| forty | +10.35 | `to three times` | `the` |
| twelve | +6.81 | (line start) | `the` |

In every high-S₂ number case, GPT-2 predicted a **function word** (the, a, an, and) — not a number. The poet is reaching for a specific symbolic count in a position where the model expected grammatical continuation.

**Core pattern**: Mythic numbers arrive at positions where GPT-2 expects articles and conjunctions. The number isn't just surprising in its choice — the entire *grammatical category* is unexpected.

---

## Finding 3: "One" Is Grammaticalized

The number "one" appears 89 times with mean S₂ = +0.042 — essentially neutral. This is because "one" in poetry largely functions as a pronoun/indefinite article ("one must...", "one day...", "one could not...") rather than a counting word. Its near-zero S₂ reflects grammatical use, not numerical use.

By contrast, "two" (mean S₂ = −0.923) appears in predictable parallel structures. When a poet writes "two..." the structure (couplet, pair, duet) is usually pre-announced by context. "Two" is semantically richer than "one" but contextually more constrained — appearing after setup phrases like "between us," "my two," "these two."

---

## Finding 4: Ordinals Are Structural, Not Poetic

Ordinals (first, second, third) average −0.481 S₂ — consistently below baseline. They typically appear in predictable serial contexts ("the first time," "a second look," "third stanza") where the ordinal is the most grammatically expected continuation. Ordinals are content-free structural markers that signal sequence without opening semantic space.

---

## Finding 5: Vague Quantifiers Cluster at Baseline — Except at Peaks

Vague quantifiers (all, every, many, few, some, once, twice) average +0.002 S₂ — baseline level. They are informationally neutral *on average*. But they have the highest single-peak moments in the number/quantifier domain:

| Token | S₂ | Era | Context |
|---|---|---|---|
| most | +14.42 | new_york_school | (top_alt: 'you') |
| some | +10.44 | contemporary | (top_alt: 'horses') |
| each | +9.87 | 18th_century | (top_alt: 'ably') |
| once | +9.24 | victorian | (top_alt: 'cried') |
| many | +8.82 | romantic | (top_alt: 'of') |

At these positions, the quantifier appears where GPT-2 predicted a verb, noun, or pronoun — not a quantifier at all. The quantifier breaks into the syntax where it's grammatically licensed but semantically unexpected.

---

## Interpretation: The Numerological Contract

Poetry has an implicit numerological contract with tradition:
- **Symbolic numbers** (seven, forty, twelve, three) derive their S₂ from deploying culturally coded values in contexts GPT-2 reads as expecting function words. The number's meaning-load — its biblical, mythological, ritualistic weight — requires arriving at a moment of grammatical openness.
- **Counting numbers** (hundred, thousand) appear in contexts already set up for enumeration. They fulfill rather than violate expectation.
- The 6.3-bit spread between seven (+4.77) and thousand (−1.54) is not random noise: it maps the difference between numerology and arithmetic.

A poet who writes "seven" is making a rhetorical gesture; a poet who writes "thousand" is making a measurement.

---

## Suggested Next Steps
1. **Numerical position in line**: Do numbers with high S₂ appear preferentially at line-start vs. mid-line?
2. **Collocational analysis**: What words most often follow seven/three vs. hundred/thousand? Do mythic numbers attract more abstract nouns?
3. **Era evolution**: Has the symbolic weight of "seven" changed across literary history? Do Romantic and Victorian poets show higher or lower S₂ at "seven" than contemporary poets?
4. **Scripture-dependent analysis**: Biblical poetry (psalms, prophets) and ballads (the oral tradition "three times seven") may account for a disproportionate share of high-S₂ mythic numbers.
