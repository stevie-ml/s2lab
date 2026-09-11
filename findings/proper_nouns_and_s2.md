# Proper Nouns and the Straussian Gap: Names as Sites of Poetic Surprise

**Date:** 2026-09-11
**Experiment:** `experiments/proper_nouns_s2.py`
**Corpus:** 106 English poetry texts (control prose excluded)
**Builds on:** `syntactic_position_vs_s2.md` (which collapsed NNP/NNPS into a single NOUN category)

---

## Research Question

The prior syntactic-position experiment showed that NOUN tokens in poetry have higher average S₂ than in prose. But "nouns" is a heterogeneous category. This experiment separates:

- **Proper nouns (NNP/NNPS):** names of people, places, mythological figures, and — critically in poetry — **abstractly capitalized concepts** (e.g., Dickinson's "Death," "Immortality"; Blake's "Tyger").
- **Common nouns (NN/NNS):** ordinary concrete and abstract nouns.

**Central hypothesis:** Proper nouns are a primary mechanism by which poets achieve the Straussian gap. Naming a specific person, place, or entity is a strategy of unexpected specificity — GPT-2 expects *some* noun in a given position but cannot predict *which* name the poet chooses.

---

## Results

### Global Comparison

| Category | n | avg S₂ | +S₂ ratio | max S₂ |
|---|---|---|---|---|
| **Proper (NNP/NNPS)** | 593 | **+3.821** | 56.5% | +36.38 |
| Common (NN/NNS) | 1,781 | +0.959 | 50.5% | +35.40 |

**Δ (proper − common) = +2.862 bits.** Proper nouns have nearly 4× the average S₂ of common nouns.

### By Literary Era (Proper − Common Noun S₂ Gap)

| Era | Prop n | Prop AvgS₂ | Comm n | Comm AvgS₂ | **Δ** |
|---|---|---|---|---|---|
| confessional | 22 | +8.739 | 29 | +0.792 | **+7.947** |
| mid_century | 9 | +8.749 | 20 | +1.868 | **+6.881** |
| deep_image | 2 | +8.122 | 15 | +1.304 | **+6.817** |
| contemporary | 9 | +6.523 | 102 | +0.779 | **+5.744** |
| victorian | 62 | +4.925 | 232 | +1.371 | **+3.554** |
| ballad | 89 | +4.255 | 213 | +0.585 | **+3.669** |
| romantic | 68 | +3.699 | 190 | +0.542 | **+3.157** |
| 19th_century | 119 | +2.751 | 130 | +0.332 | **+2.419** |
| modernist | 92 | +2.875 | 293 | +1.291 | **+1.584** |
| new_york_school | 69 | +3.677 | 230 | +1.008 | **+2.669** |
| harlem_renaissance | 22 | +3.019 | 86 | +0.638 | **+2.381** |
| surrealist | 8 | +0.644 | 22 | +0.795 | **−0.150** |

---

## Methodological Layer: Three Types of NNP in Poetry

NLTK's POS tagger assigns NNP (proper noun) to any capitalized word it cannot classify otherwise. In poetry, this creates three distinct sub-categories:

**Layer 1 — True proper names:** Personal names ("Edward," "June"), place names ("London," "Manhattan"), mythological figures ("Anansi," "Sisyphus"). These are proper nouns in every sense.

**Layer 2 — Poetically personified abstractions:** Dickinson's "Death," "Immortality," "Nature"; Blake's "Tiger" → "Tyger"; Milton's "Sin," "Death." The poet deliberately capitalizes an abstract concept to treat it as a unique entity. NLTK correctly identifies these as NNP. This IS a literary strategy — personification is a form of specificity.

**Layer 3 — Line-initial capitalization artifact:** Traditional verse capitalizes the first word of every line ("Cold," "Of," "To," "The" at the top of a Convergence of the Twain stanza). NLTK tags these as NNP even when the word is a preposition or article. This inflates the NNP S₂ numbers, since line-initial position already has high S₂ (see `line_position_analysis.md`: avg +5.57 for initial tokens).

**Implication:** The +3.821 avg S₂ for "proper nouns" is partly a line-position artifact. However, the *by-era* results (which are relative: proper vs. common within the same poem) partially control for this, since both categories share the same line-position distribution. The era Δ values are more interpretable.

---

## Key Finding: Confessional and Mid-Century Poets Lead

The largest proper-vs-common gaps appear in **confessional** (+7.947) and **mid-century** (+6.881) poetry — genres associated with Sylvia Plath, Anne Sexton, Robert Lowell, and Elizabeth Bishop.

This is theoretically coherent: confessional poetry is defined by its use of *specific* proper names — real people, real places, real events. When Plath writes about "Dachau, Auschwitz, Belsen" or names her father specifically, these names are maximally unexpected given any statistical model of poetic language. The Straussian gap is at its widest when the poet names the unnameable.

**Ballad tradition** shows the third-largest Δ (+3.669). Traditional ballads use character names as anchors: "Edward, Edward," "Barbara Allen," "Patrick Spens." The name carries the entire narrative weight of the form. GPT-2 cannot predict which specific name the balladeer deploys.

**Surrealist** poetry (Breton, Lorca translations) shows essentially no gap (−0.150). Surrealist language dissolves the distinction between the named and the unnamed — objects are treated as abstractions, and the proper noun loses its specificity.

---

## High-S₂ Proper Names in the Corpus (Selected)

From the top-S₂ proper noun tokens, filtering for genuine names:

| Token | S₂ | Poem | Note |
|---|---|---|---|
| Edward | +28.31 | "Edward, Edward" | Ballad protagonist named at stanza turn |
| Jew | +25.56 | "Lady Lazarus" (Plath) | Self-identification; extreme specificity |
| God | +4× positive | Multiple | Recurrent personification across eras |
| Death | +2× positive | Dickinson | Abstract personified as proper noun |
| June | +3× positive | Multiple | Temporal specificity → proper-noun treatment |

---

## Hypothesis for Future Work

**The "specificity ratchet":** Poets increase the Straussian gap by trading generic nouns for proper nouns — "a man" → "Edward" → "my father." Each substitution becomes statistically less predictable (higher S₂) while becoming semantically more charged. 

An experiment testing this directly would: (1) identify every NNP in the corpus, (2) hand-classify as generic noun that was capitalized vs. genuine proper name vs. abstract personification, (3) compute S₂ separately for each subclass to isolate the line-position artifact from the true specificity effect.

**Cross-check with negation:** The `negation_and_s2.md` findings showed that negation is another high-S₂ strategy. Are there poems that combine proper nouns WITH negation ("Not you, but Edward")? These might be the sites of maximal Straussian gap.

---

## Suggested Next Steps

1. **Disambiguate NNP subtypes** with a simple heuristic: filter out tokens that appear in line-initial position (already have high S₂ for structural reasons). Recompute proper-noun S₂ for mid-line NNPs only.
2. **Build a name database:** Extract all NNP tokens that appear ≥2 times in the corpus, hand-classify by type (person/place/abstract-personified), compute S₂ by type.
3. **Proper noun density:** Does poems with MORE proper nouns have higher overall average S₂? Plot proper-noun-per-line-count vs poem-level S₂.
4. **Translation effect:** Do translated poems (German → English in corpus) show different NNP behavior? Translation often replaces proper nouns with glosses.
