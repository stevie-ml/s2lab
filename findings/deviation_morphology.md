# Deviation Morphology: How Poets Leap from Expected to Chosen

**Date:** 2026-11-11  
**Experiment:** `experiments/deviation_morphology.py` → `results/deviation_morphology.json`  
**Corpus:** 411 texts; 9,605 clean high-S₂ tokens (S₂ ≥ 2.0, p_newline < 0.9, English only)  
**Builds on:** `rank_topology.md`, `straussian_gap_taxonomy.md`, `phonaesthetics_s2.md`

---

## Research Question

When a poet writes a high-S₂ token — something GPT-2 did not predict — *how morphologically
and phonologically related is the chosen word to the top prediction?*

We know from `rank_topology.md` that most poetic surprises are "radical departures" in rank
(rank 100+). But rank measures statistical position, not formal similarity. A poet could
choose rank 500 yet still pick a word that *sounds like* what was expected (e.g., "night"
when "light" was predicted), or they could pick something phonologically orthogonal.

**Four deviation categories** (applied to all high-S₂ tokens):
1. **Morphological variant**: same root, different inflection (e.g., *running* vs *run*)
2. **Phonological near-miss**: ≥50% shared character bigrams (e.g., *light* vs *night*)
3. **Partial overlap**: 25–49% shared bigrams and similar length
4. **Length-matched substitute**: same word-length ±25%, low character overlap
5. **Radical departure**: short top-1 or low similarity — no morphological relationship
6. **Structural surprise**: poet writes word where punctuation expected, or vice versa

---

## Global Distribution

| Deviation Type | n | % of events | Mean S₂ |
|---|---|---|---|
| **Radical departure** | 4,904 | **51.1%** | 5.34 |
| **Length-matched substitute** | 2,434 | **25.3%** | 5.02 |
| **Structural surprise** | 2,062 | **21.5%** | **5.83** |
| Partial overlap | 112 | 1.2% | 4.95 |
| Phonological near-miss | 65 | **0.7%** | 4.30 |
| Morphological variant | 16 | **0.2%** | 5.54 |

**Three headline findings emerge immediately:**

### Finding 1 — Poetic deviation is almost never phonological

Phonological near-misses (words that *sound like* what was expected) make up only **0.7%** of
all high-S₂ events. Morphological variants (same root, different form) are even rarer at **0.2%**.

This falsifies an intuitive hypothesis: that poets exploit acoustic similarity to generate
"low-cost" surprises that feel familiar. When a poet departs from the model's expectation,
the departure is almost always RADICAL — the chosen word shares no acoustic or morphological
kinship with what was predicted.

### Finding 2 — Structural surprises have the highest information-theoretic impact

**Structural surprises** (writing a content word where punctuation was predicted, or vice versa)
represent 21.5% of deviations but carry the **highest mean S₂ (5.83)** — higher even than
radical departures (5.34). Structural position violations are maximally surprising because
GPT-2 is extremely confident about punctuation/newline positions (p_newline or p_comma often
> 0.5), so any word choice is a defiance of near-certainty.

### Finding 3 — Length-matched substitutes reveal syntactic strategy (25.3%)

A quarter of deviations involve words of similar length to the prediction — syntactic swaps
where the poet preserves the "shape" of the sentence (syllable count, word-length) while
inserting unexpected content. This is consistent with metrical constraint: poets working in
formal or quasi-formal verse need to find metrically appropriate words, and the available
options often have similar lengths even when semantically radical.

---

## Era Analysis: Acoustic vs. Experimental Traditions

| Era | n | radical% | structural% | length-match% | phonological% |
|---|---|---|---|---|---|
| biblical | 201 | 52.7 | 23.4 | 21.4 | **2.5** |
| 18th_century | 292 | 51.0 | 20.5 | 23.3 | **2.1** |
| ballad | 141 | 54.6 | 28.4 | 14.9 | **1.4** |
| victorian | 1065 | 48.7 | 21.8 | 28.2 | 0.8 |
| romantic | 695 | 49.8 | 18.4 | 29.9 | 0.9 |
| elegy | 254 | 45.3 | 22.4 | 29.9 | 0.8 |
| **language** | 82 | 53.7 | **29.3** | 14.6 | **0.0** |
| **oulipo** | 215 | **56.7** | 17.2 | 23.3 | **0.0** |
| **surrealist** | 195 | 55.4 | 15.4 | 28.7 | **0.0** |
| new_york_school | 463 | 55.9 | 18.4 | 22.9 | 0.6 |
| modernist | 567 | 48.1 | 21.9 | 27.5 | 0.4 |
| contemporary | 509 | 54.4 | 20.0 | 23.0 | 0.4 |

**Acoustic/oral traditions** (biblical, 18th century, ballad) show 1.4–2.5% phonological
near-misses — 2–4× the rate of experimental traditions.

**Experimental traditions** (Language poetry, Oulipo, Surrealism) show **0.0%** phonological
near-misses. These traditions have completely evacuated acoustic similarity from their
surprise lexicon.

The pattern for **radical departure** runs the opposite direction: Oulipo (56.7%), Surrealist
(55.4%), new_york_school (55.9%) all show higher radical departure rates than elegy (45.3%)
or Victorian (48.7%).

**Language poetry** shows the highest **structural surprise** rate (29.3%) — consistent with
Language Poetry's project of violating syntactic expectations by inserting content in
"grammatical position" slots.

---

## Author Analysis: Sound-Based Poets vs. Semantic Leapers

**Authors with highest phonological near-miss rate** (poets who choose acoustically similar surprises):

| Author | Era | phono% | n |
|---|---|---|---|
| Anonymous (Hebrew Bible) | biblical | 2.7 | 150 |
| Christopher Smart | 18th_century | 2.3 | 88 |
| Traditional (Scottish ballad) | ballad | 1.8 | 112 |
| Edgar Allan Poe | fixed_form | 1.7 | 117 |
| Percy Bysshe Shelley | elegy | 1.5 | 134 |
| Gerard Manley Hopkins | victorian | 1.3 | 236 |
| Alexander Pope | 18th_century | 1.3 | 153 |

Every poet in this list is known for distinctive sound patterning:
- Biblical Hebrew: parallelism, assonance, vocalization
- Smart (*Jubilate Agno*): incantatory acoustic repetition
- Poe: systematic sound effects (raven/raving, nevermore)
- Hopkins: sprung rhythm, inscape, consonantal echo
- Pope: heroic couplets with Augustan sonic balance

**Authors with LOWEST radical departure rate** (most "formal" deviation style):

| Author | Era | radical% | n |
|---|---|---|---|
| Gerard Manley Hopkins | victorian | 44.5 | 236 |
| Percy Bysshe Shelley | elegy | 44.8 | 134 |
| Tennyson | elegy / ekphrastic | 47.3–47.9 | 322 |
| Algernon Swinburne | victorian | 48.0 | 98 |
| Emily Dickinson | 19th_century | 48.1 | 133 |
| Christina Rossetti | victorian | 48.4 | 93 |

**Authors with HIGHEST radical departure** (most "nuclear" deviation style):

| Author | Era | radical% | n |
|---|---|---|---|
| Gertrude Stein | oulipo | 61.8 | 102 |
| William Blake | romantic | 58.2 | 146 |
| William Shakespeare | victorian | 58.1 | 74 |
| Traditional (Scottish ballad) | ballad | 57.1 | 112 |
| Thomas Hardy | victorian | 55.1 | 214 |
| John Ashbery | new_york_school | 54.7 | 254 |

Gertrude Stein's 61.8% radical departure is the highest in the corpus — consistent with her
project of making language strange by complete semantic dislocation rather than acoustic play.

---

## The Length-Matched Substitute Cluster

Authors with the highest **length-matched substitute** rates:

| Author | Era | length-match% | n |
|---|---|---|---|
| Christopher Smart | 18th_century | 36.4 | 88 |
| Anonymous (Hebrew Bible) | biblical | 33.3 | 150 |
| Lewis Carroll | nonsense | 32.1 | 156 |
| Walt Whitman | 19th_century | 28.3 | 360 |
| Alfred Lord Tennyson | elegy | 28.1 | 96 |

The pattern here is striking: parallelistic traditions (Biblical psalms, Smart's Jubilate Agno,
Whitman's catalogs) produce the highest rates of length-matched substitutes. In parallel
structures ("For X is…, For Y is…"), each substitution preserves syntactic position and
approximate word-length while cycling through semantic variants. This is "shape-preserving
deviation" — the formal scaffold constrains word-length even as content deviates radically.

Lewis Carroll's high rate reflects *Jabberwocky*'s nonsense words, which substitute
semantically but preserve morphological/syllabic shape (*brillig*, *slithy*, *toves*).

---

## Summary Table: Deviation Style by Tradition

| Tradition | Primary strategy | Secondary | Characteristic |
|---|---|---|---|
| Acoustic/oral (biblical, ballad, 18th c.) | Radical departure | Length-match | + phonological near-miss |
| Victorian formal | Radical departure | Length-match | Low structural surprise |
| Parallelistic (Whitman, Smart) | Radical departure | Length-match | Shape-preserving |
| Modernist | Radical departure | Length-match | Low phonological |
| Language/Oulipo/Surrealist | **Highest radical** | Structural | Zero phonological |
| Confessional | Radical departure | Structural | High structural% |

---

## Interpretation

The overarching finding is a **bimodal phonological strategy in poetry**:

- **Acoustic traditions** deploy small but non-zero rates of phonological near-miss. These
  are traditions where the SOUND of the word matters — where choosing "night" instead of
  "light" is a valid and meaningful surprise because the near-miss itself is part of the
  acoustic texture. The surprise is in the NEAR-ESCAPE from prediction.

- **Experimental/visual traditions** deploy ZERO phonological near-miss. When Language
  poetry or Oulipo or Surrealism deviates, it leaps entirely out of the acoustic field of
  prediction. The word chosen has no sound-kinship to what was expected.

This maps cleanly onto a known distinction in poetics: **poetry-of-the-ear** (oral tradition,
ballad, Romantic lyric, Victorian sound poetry) vs. **poetry-of-the-eye** (Language poetry,
concrete poetry, Oulipo, visual/conceptual work). The information-theoretic signature of this
distinction is now measurable: ear-poetry exploits acoustic proximity; eye-poetry exploits
semantic orthogonality.

---

## Suggested Next Steps

1. **Phonological cluster analysis**: For the 65 phonological near-miss tokens, build a
   taxonomy of acoustic substitution types (rhyme, consonance, assonance, reversal).
2. **Length-match and meter**: Test whether length-matched substitutes are specifically
   metrically-equivalent (same number of syllables), which would explain their concentration
   in formal poetry.
3. **Structural surprise by line position**: Does structural surprise concentrate at line
   beginnings (enjambment) or line endings (closure)?
4. **Cross-poet near-miss catalog**: Compile the full 65 phonological near-misses and annotate
   them manually — are they all acoustic substitutions, or some coincidental bigram overlaps?
