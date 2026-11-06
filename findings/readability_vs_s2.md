# Readability vs. S₂: Two Orthogonal Dimensions of Textual Difficulty

**Date:** 2026-11-06  
**Experiment:** `experiments/readability_vs_s2.py` → `results/readability_vs_s2.json`  
**Corpus:** 391 English poems (control prose excluded, non-English excluded)  
**Builds on:** `word_length_vs_s2.md`, `hapax_legomena_s2.md`, `vocab_richness_vs_s2.md`

---

## Research Question

Traditional readability formulas (Flesch-Kincaid, ARI, Coleman-Liau) measure how hard a text
is to process based on **sentence length** and **word length/syllable count**. The S₂
framework measures **information-theoretic surprise** — how much the poet's word choice
deviated from GPT-2's predictions.

Do these two measures of textual difficulty agree? A positive correlation would suggest they
both measure "complexity." A near-zero correlation would suggest they tap orthogonal
properties of text.

---

## Main Finding: Readability and S₂ Are Nearly Uncorrelated

| Readability Measure | r with Avg S₂ | r with Avg Entropy |
|---|---|---|
| **Flesch Reading Ease** (higher = easier) | −0.070 | +0.022 |
| **Flesch-Kincaid Grade Level** (higher = harder) | −0.001 | −0.007 |
| **Automated Readability Index** (higher = harder) | −0.005 | +0.011 |
| **Coleman-Liau Index** (char-based, higher = harder) | **+0.219** | +0.078 |
| **Words Per Sentence** | −0.046 | +0.003 |
| **Syllables Per Word** | **+0.273** | −0.061 |

**FK Grade Level and ARI have virtually zero correlation with S₂ (r ≈ 0.000 to −0.005).**
Words-per-sentence is also near-zero (r = −0.046). This is a sharp negative result: the
primary dimension of traditional readability — sentence length — has no information-theoretic
significance.

**The one exception is syllables per word (r = +0.273)**: poems with polysyllabic vocabulary
are systematically more surprising. This aligns with `hapax_legomena_s2.md` (rarer words =
higher S₂) since longer words are typically less frequent. The Coleman-Liau Index, which
uses character counts rather than syllable counts, captures this same signal (r = +0.219).

**Conclusion:** Traditional readability and information-theoretic surprise are **orthogonal
dimensions**. A poem can be:
- Linguistically simple but informationally dense (easy syntax, surprising word choices)
- Linguistically complex but informationally flat (hard sentences, predictable word choices)

---

## S₂ by FK Grade Quintile

The quintile analysis confirms no monotonic relationship:

| Quintile | Avg FK Grade | Avg S₂ | Pos S₂% | Avg Entropy |
|---|---|---|---|---|
| Very Easy (Q1) | 2.0 | −0.521 | 32.5% | 6.07 |
| Easy (Q2) | 4.5 | −0.429 | 33.5% | 6.24 |
| **Medium (Q3)** | 6.8 | **−0.260** | **36.8%** | 6.46 |
| Hard (Q4) | 9.7 | −0.387 | 35.1% | 6.56 |
| Very Hard (Q5) | 23.2 | −0.381 | 33.9% | 6.25 |

The highest S₂ sits in the medium range (FK=6–7), not at the extremes. Very easy poems (FK<3)
and very hard poems (FK>15) both have lower average S₂ than medium poems. This "dome" shape
(weak, noisy) suggests there's an optimal complexity window for poetic surprise — but the
effect is small.

---

## Era-Level Analysis

Sorted by average FK Grade (easiest to hardest):

| Era | n | Avg FK Grade | Avg S₂ |
|---|---|---|---|
| german_expressionist | 4 | 2.8 | −0.162 |
| **haiku** | 14 | **3.4** | **+0.033** |
| cliche_control | 4 | 3.7 | −0.930 |
| villanelle | 3 | 4.1 | −0.569 |
| language | 6 | 4.3 | −0.518 |
| metaphysical | 4 | 4.6 | −0.558 |
| ballad | 6 | 4.8 | −0.388 |
| limerick | 10 | 5.4 | −0.693 |
| clerihew | 10 | 6.8 | **+0.552** |
| prose_poetry | 12 | 6.8 | −0.470 |
| modernist | 28 | 9.4 | −0.458 |
| surrealist | 8 | 11.1 | −0.609 |
| new_york_school | 26 | 11.1 | −0.597 |
| **beat** | 8 | **13.8** | **+0.192** |
| romantic | 21 | 13.4 | −0.496 |
| 19th_century | 18 | 26.4 | −0.230 |

**Key contrasts:**
- **Haiku**: FK=3.4 (very simple), S₂=+0.033 (positive despite simplicity) — word simplicity
  doesn't prevent surprise
- **Clerihew**: FK=6.8 (medium), S₂=+0.552 (highest positive S₂ of any era) — the proper
  name/biographical structure generates surprise independent of sentence complexity
- **Limerick**: FK=5.4 (simple), S₂=−0.693 (very negative) — formal constraint suppresses
  surprise despite easy language
- **Language poetry**: FK=4.3 (simple), S₂=−0.518 (negative) — grammatical disruption
  without surprise from GPT-2's perspective

---

## The Four Quadrants: Readability × S₂

Dividing poems at the medians (FK=6.6, S₂=−0.408):

### Easy + High S₂: "Readable but Surprising" (n=88, 22%)

Simple language, informationally dense. The optimal poetic register.

| FK Grade | S₂ | Poem |
|---|---|---|
| 6.0 | +2.077 | Chiyo-ni: Morning Glory |
| 5.7 | +1.772 | Christian Bök: Eunoia: Chapter E |
| 2.5 | +1.327 | Richard Wright: Nobody |
| 2.4 | +1.184 | Matsuo Bashō: Old Pond |

These poems use short sentences and common words yet choose those words in ways GPT-2
finds consistently surprising. This is the "haiku strategy": syntactic simplicity enables
semantic surprise by ensuring the model's predictions are precise and missable.

### Hard + High S₂: "Difficult and Surprising" (n=107, 27%)

Complex syntax AND surprising word choices — the most demanding poems.

| FK Grade | S₂ | Poem |
|---|---|---|
| 9.4 | +1.891 | Clerihew: Nikola Tesla |
| 10.0 | +0.968 | Hart Crane: The Harbor Dawn |
| 9.1 | +1.113 | Clerihew: Sir Humphrey Davy |

### Easy + Low S₂: "Readable and Expected" (n=107, 27%)

Simple language, predictable choices. Highest conformism.

| FK Grade | S₂ | Poem |
|---|---|---|
| 1.3 | −2.144 | Issa: The World of Dew |
| 1.3 | −1.507 | E.E. Cummings: l(a |
| 3.0 | −1.388 | Ashbery: A Wave (opening) |
| 3.6 | −1.323 | Dowson: Villanelle of the Poet's Road |
| 4.9 | −1.229 | Blake: The Sick Rose |

Surprisingly, E.E. Cummings' `l(a` — which is typographically radical — has very low S₂.
The tokens it contains ("la," "le," "af," etc.) are individually surprising, but the
*artifact-free* analysis strips stanza breaks, and the remaining semantic content is minimal.

### Hard + Low S₂: "Difficult but Predictable" (n=89, 23%)

Complex syntax, conformist word choices. The 19th-century mode.

| FK Grade | S₂ | Poem |
|---|---|---|
| 19.9 | −1.581 | Pierre Reverdy: Departure |
| 10.9 | −1.370 | W.C. Williams: This Is Just to Say |
| 21.5 | −1.306 | Vachel Lindsay: The Congo (excerpt) |

Long Whitman catalogues (FK=60.9) have moderate S₂ (−0.651) despite enormous FK scores —
the sentence length is extreme, but the words themselves are individually ordinary, confirming
the near-zero correlation.

---

## What This Means

**Traditional readability and information-theoretic difficulty are orthogonal** because they
measure different axes of the difficulty space:

| Dimension | Measured by | Mechanism |
|---|---|---|
| **Structural difficulty** | FK Grade, ARI | Sentence length × word length |
| **Lexical difficulty** | Syllables/word, Coleman-Liau | Word complexity / rarity |
| **Information-theoretic surprise** | S₂ | Deviation from language model's expectation |

The near-zero correlation of S₂ with sentence-length measures suggests that GPT-2's
prediction accuracy depends primarily on **what word was chosen**, not on **how the sentence
is structured**. A simple "and" in a surprising context (high-entropy Straussian choice) has
higher S₂ than a complex "multidimensional" in a predictable context.

**For literary pedagogy**: a "difficult" poem in the classroom sense (Donne, Milton, Crane)
may actually be highly predictable to GPT-2 — the difficulty is in unpacking meaning, not
in novelty of word choice. By contrast, an "easy" poem (haiku, concrete poetry) can be
information-theoretically dense in ways not captured by traditional metrics.

---

## Suggested Next Steps

1. **Multi-language readability**: Does the orthogonality hold for German-language poems in
   the corpus? German compound nouns might make syllable-count correlations even stronger.
2. **Syllable budget analysis**: Map syllables-per-word against rank deviation — do
   polysyllabic words go further from GPT-2's top predictions than monosyllables?
3. **Readability trajectory within poems**: Does FK grade (computed stanza-by-stanza) evolve
   differently from S₂ within a poem? Do opening stanzas have different readability vs.
   closing stanzas, and does this align or diverge from the S₂ arc?
4. **Reader experience modeling**: Combine readability with S₂ to predict which poems readers
   describe as "hard to understand" vs. "surprising" — testing whether these are phenomenologically
   distinct reading experiences.
