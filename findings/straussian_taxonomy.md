# Straussian Gap Taxonomy: A Classification of Poet Deviations

**Date:** 2026-11-03  
**Experiment:** `experiments/straussian_taxonomy.py`  
**Research Question:** For each high-S₂ moment (S₂ ≥ 3.0), what does GPT-2 expect vs. what does the poet write? Can we build a taxonomy of Straussian deviations?

---

## Method

Applied to all 403 poems in the corpus. For every token with S₂ ≥ 3.0 bits (~99th percentile), we recorded:
- The poet's actual choice (chosen token)
- GPT-2's top alternative (the "suppressed" token)
- A deviation-type label based on the syntactic class of both tokens

**Total high-S₂ moments analyzed:** 8,925

---

## 1. Taxonomy Distribution

| Deviation Type | Count | % | Mean S₂ | Max S₂ |
|---|---|---|---|---|
| FUNCTION_TO_CONTENT | 2,799 | 31.4% | 6.39 | 22.73 |
| CONTENT_SUBSTITUTION | 2,524 | 28.3% | 6.91 | 41.53 |
| OTHER | 1,842 | 20.6% | **12.97** | 34.59 |
| PUNCTUATION_SKIP | 1,079 | 12.1% | 6.23 | 20.40 |
| PROPER_NOUN_BREAK | 581 | 6.5% | **16.17** | 39.00 |
| MODAL_DODGE | 100 | 1.1% | 6.38 | 27.73 |

**Key finding:** PROPER_NOUN_BREAK is rare (6.5%) but carries the highest mean S₂ (16.17 bits) — proper nouns injected where content words were expected are among the most extreme semantic violations. The OTHER category (mean S₂ = 12.97) captures cases where GPT-2 expected a newline with near-certainty (probability > 0.99) and the poet continued — these produce the largest individual spikes.

---

## 2. What Did GPT-2 Most Want? (The Suppressed Lexicon)

| Expected Token | Times Suppressed |
|---|---|
| `''` (newline) | **2,012** |
| `'the'` | 768 |
| `','` | 740 |
| `'of'` | 236 |
| `'and'` | 208 |
| `'.'` | 195 |
| `'I'` | 192 |
| `'a'` | 158 |
| `'is'` | 137 |
| `'to'` | 135 |

**The newline dominates** — 22.5% of all high-S₂ moments are caused by the poet *not ending a line* when the model was confident a line would end. The model has deeply internalized line-ending as the default continuation in poetry. This is a structural, not semantic, source of surprise.

After removing newline-related deviations, the model's most suppressed lexical items are function words: *the, of, and, I, a, is, to* — the connective tissue of English prose that poetry systematically bypasses.

---

## 3. Exemplary High-S₂ Moments by Category

**FUNCTION_TO_CONTENT** (model expected function word, poet chose content):
- Anonymous (trans.): `…that he` → chose `riot` (expected `may`, prob=0.393, S₂=22.73)
- Christopher Smart: `…he rolls upon` → chose `prank` (expected `the`, prob=0.455, S₂=22.13)
- Gerard Manley Hopkins: `…like shining from` → chose `shook` (expected `the`, prob=0.387, S₂=22.04)

**CONTENT_SUBSTITUTION** (model expected content word, poet chose different content):
- Robert Creeley: `…of holes\n` → chose `aching` (expected `\n`, prob=1.000, S₂=41.53)
- Kobayashi Issa: `…keep house\n` → chose `cas` (expected `\n`, prob=0.999, S₂=39.62)
- Marianne Moore: `…sun,\n` → chose `split` (expected `\n`, prob=0.999, S₂=39.17)

**PROPER_NOUN_BREAK** (unexpected proper noun injection):
- Synthetic (double dactyl): `…ically—\n` → chose `Death` (expected `\n`, prob=1.000, S₂=39.00)
- Lewis Carroll: `…box—\n` → chose `Allow` (expected `\n`, prob=1.000, S₂=38.37)
- William Stafford: `…less.\n` → chose `Ready` (expected `\n`, prob=1.000, S₂=37.72)

---

## 4. Token Class Transition Matrix

At high-S₂ moments, when GPT-2 expected class X, the poet chose class Y:

| Expected → | FUNCTION | CONTENT | PUNCTUATION | MODAL | PROPER_NOUN |
|---|---|---|---|---|---|
| **FUNCTION** | 476 | **2,358** | 0 | 4 | 441 |
| **CONTENT** | 1,323 | **2,375** | 2 | 19 | 581 |
| **PUNCTUATION** | 197 | **784** | 5 | 9 | 84 |
| **MODAL** | 11 | **83** | 0 | 2 | 4 |
| **PROPER_NOUN** | 18 | **67** | 0 | 0 | 82 |

**Pattern:** Regardless of what the model expected, poets predominantly choose CONTENT or PROPER_NOUN tokens at high-S₂ moments. Poetry's basic surprise mechanism is lexical concretization — bringing in the specific, named, and tangible where grammar expected the abstract or structural.

---

## 5. Poet Straussian Profiles (Top 10 by Avg S₂)

| Author | Poems | Avg S₂ | High-S₂ % | Top Deviation |
|---|---|---|---|---|
| Chiyo-ni | 1 | 4.156 | 31.2% | CONTENT_SUBSTITUTION |
| Lorine Niedecker | 1 | 3.258 | 34.3% | CONTENT_SUBSTITUTION |
| William Carlos Williams | 4 | 3.023 | 27.0% | CONTENT_SUBSTITUTION |
| Robert Creeley | 2 | 3.002 | 29.9% | CONTENT_SUBSTITUTION |
| Sonia Sanchez | 1 | 2.347 | 21.5% | OTHER |
| Gwendolyn Brooks | 2 | 2.181 | 22.2% | PROPER_NOUN_BREAK |
| Matsuo Bashō | 1 | 2.142 | 29.3% | CONTENT_SUBSTITUTION |
| Richard Wright | 1 | 2.028 | 37.5% | CONTENT_SUBSTITUTION |
| Hart Crane | 1 | 1.872 | 30.6% | FUNCTION_TO_CONTENT |
| Seamus Heaney | 1 | 1.854 | 25.0% | FUNCTION_TO_CONTENT |

**Finding:** Imagist and objectivist poets (WCW, Niedecker, Creeley) dominate the top of the Straussian ranking — their minimalism creates extreme lexical focus, each token bearing maximum deviation load. Haiku poets cluster near the top via CONTENT_SUBSTITUTION. At the bottom: Whitman, Language poets, Shakespeare — prolific/syntactically conformist or prose-like flow.

---

## 6. Era-Level Straussian Gap

| Era | Tokens | Avg S₂ | High-S₂ % |
|---|---|---|---|
| haiku | 324 | **1.714** | 27.5% |
| clerihew | 243 | 1.491 | 28.8% |
| black_arts | 280 | 1.383 | 20.0% |
| double_dactyl | 269 | 1.200 | 19.0% |
| german_modernist | 240 | 0.955 | 24.6% |
| modernist | 3,195 | 0.561 | 20.4% |
| … | … | … | … |
| language | 502 | -0.414 | 16.1% |
| control (prose) | 164 | **-1.636** | 4.3% |

**The haiku / clerihew paradox:** These short, highly constrained forms sit at opposite ends of the aesthetic spectrum (one is a Japanese meditative tradition, the other a comic verse form) yet both have the highest Straussian scores. The likely explanation: extreme brevity forces every token to work harder — no padding, no function words to buffer the model. Constraint paradoxically produces deviation.

---

## Key Findings

1. **The newline is GPT-2's poetic default**: 22.5% of all high-S₂ moments are the poet refusing to end a line when the model was near-certain the line was over. The model has learned "poems end lines after certain patterns" — and poets exploit this expectation by continuing.

2. **PROPER_NOUN_BREAK is the highest-intensity deviation type** (mean S₂ = 16.17) despite being rare (6.5%). Proper nouns injected mid-grammar violate semantic and syntactic expectations simultaneously.

3. **Poetry's fundamental surprise move is lexical concretization**: regardless of what the model expected, poets predominantly choose CONTENT or PROPER_NOUN tokens at high-S₂ moments. The poet brings the specific where grammar expected the general.

4. **Imagist / objectivist tradition maximizes Straussian deviation** — minimalism is not just aesthetic but information-theoretically extreme. Each word carries maximal deviation load when there are no others to diffuse it.

5. **Language poetry underperforms** (avg S₂ = -0.414) despite its experimental reputation — its syntactic disruption creates low-entropy, unpredictable sequences that GPT-2 actually finds *less* surprising per token than Victorian verse.

---

## Suggested Next Steps

- Refine the "OTHER" category (these are the most extreme deviations — mostly newline-continuation events) — separate newline-skip from genuine semantic others
- Build a finer semantic taxonomy for CONTENT_SUBSTITUTION using word embeddings (semantic proximity of chosen vs. expected)
- Test whether PROPER_NOUN_BREAK correlates with the poem's thematic specificity (named places, named people)
- Investigate the "Creeley effect" — why do tight, minimal lyric structures produce such large S₂ values?
