# Structural vs Lexical S₂ Decomposition
**Date:** 2026-10-30
**Experiment:** `experiments/structural_lexical_decomposition.py`
**Results:** `results/structural_lexical_decomposition.json`

---

## Question

How much of a poem's measured S₂ is _form-induced_ (coming from line breaks and punctuation that GPT-2 didn't expect) vs _genuinely lexical_ (coming from surprising word choices)?

The stanza-break artifact finding showed that newline tokens inflate raw S₂ for short-line poems. This experiment extends that into a **full decomposition** across the whole corpus.

---

## Method

Every token in each poem is classified as **structural** or **lexical**:

- **Structural**: pure whitespace/newline tokens, punctuation-only tokens, or any token where `p_newline > 0.85` (GPT-2 was highly confident a line break was coming, meaning the token's position is form-dictated).
- **Lexical**: everything else — genuine word choices.

S₂ contribution is calculated per-token and averaged across each class, then per poem. Era statistics are derived from all poems in that era with ≥ 2 texts.

---

## Key Finding: Two Distinct Strategies for Poetic Surprise

Poetic forms split into two strategies for generating high S₂:

### Strategy A — **Form-Driven Surprise** (structural dominant)

These forms generate S₂ primarily through the _shape_ of the poem: short lines, unusual stanza structures, and lineation that violates GPT-2's prose expectations.

| Era | Structural S₂ contrib | Lexical S₂ contrib | Structural token % |
|---|---|---|---|
| concrete | +1.578 | −0.068 | 40.5% |
| villanelle | +1.506 | −0.398 | 36.4% |
| haiku | +1.235 | +0.397 | 36.5% |
| double_dactyl | +1.224 | −0.011 | 37.3% |
| mid_century | +1.001 | +0.197 | 35.1% |

The **lexical S₂ is near zero or negative** for these forms, meaning the _words themselves_ are not especially surprising — only the lineation is. Concrete poetry is the extreme case: structural S₂ = +1.578, lexical S₂ = −0.068. The words conform; the shape defies.

### Strategy B — **Lexically-Driven Surprise** (lexical dominant)

These forms generate S₂ through word choice, not lineation:

| Era | Structural S₂ contrib | Lexical S₂ contrib |
|---|---|---|
| clerihew | +0.681 | **+0.871** |
| beat | −0.196 | **+0.656** |
| oulipo | −0.150 | **+0.360** |
| 19th_century | +0.052 | **+0.234** |
| haiku | +1.235 | +0.397 |

**Clerihew**: biographical comic verse — the humor comes entirely from unexpected lexical choices (proper nouns, surprising predications), not from lineation.

**Beat poetry**: Ginsberg and co. use long sprawling lines (low structural S₂) but deviant diction creates lexical surprise.

**Oulipo**: Formal constraints (lipograms, N+7) force word substitutions that are lexically unusual — the form suppresses, not enables, structural novelty.

---

## Most Structurally S₂-Dominant Individual Poems

| Poem | Structural contrib | Lexical contrib |
|---|---|---|
| The Red Wheelbarrow (Williams) | +3.567 | +0.026 |
| l(a (e.e. cummings) | +3.537 | +0.353 |
| This Is Just to Say (Williams) | +3.155 | −0.543 |
| Lorine's Work (Niedecker) | +2.836 | +0.422 |
| Fog (Sandburg) | +2.794 | +1.164 |
| Cicadas (Bashō, tr.) | +2.254 | −0.661 |

Williams' imagist poems are almost entirely structural: the surprise is the _line breaks_, not the diction. "This Is Just to Say" has **negative lexical S₂** — its words are deliberately plain (plums, icebox, breakfast) — all the strangeness comes from how the note is broken into lines.

---

## Most Lexically S₂-Dominant Individual Poems

| Poem | Lexical contrib | Structural contrib |
|---|---|---|
| Eunoia: Chapter E (Bök) | +2.298 | −0.371 |
| Morning Glory (Chiyo-ni, tr.) | +2.238 | +1.918 |
| Nikola Tesla (clerihew) | +2.002 | +0.587 |
| Sir Humphrey Davy (clerihew) | +1.900 | +0.406 |
| Old Pond (Bashō, tr.) | +1.704 | +0.207 |

**Eunoia Chapter E** tops the lexical chart: Christian Bök's lipogram forces every word to contain only the vowel E, producing a lexicon entirely outside GPT-2's predictions. The structural S₂ is _negative_ — the poem's line structure is regular and expected; the strangeness is purely in the words.

---

## The Prose Poetry Null Result

Prose poetry sits at structural S₂ ≈ 0.0 and lexical S₂ ≈ −0.18. This is the expected baseline: without line breaks, structural tokens don't create surprise, and the semantic content of prose poetry is often deliberately mundane (found/documentary sources). This confirms the decomposition method is well-calibrated.

---

## Theoretical Implication: The Two Paths to the Straussian Gap

This decomposition suggests a taxonomy of how poets create the "Straussian gap" (the space between conventional language expectations and what is actually written):

1. **Topographic defamiliarization**: Use the page itself as a surprise generator — break lines where prose wouldn't, use whitespace as content. GPT-2 (trained on prose) is structurally ambushed. Williams, cummings, imagists.

2. **Lexical defamiliarization**: Use words GPT-2 has low probability for in context — unusual proper nouns, lipogrammatic vocabularies, dialect, avant-garde diction. Bök, clerihew authors, Beat poets.

Most poets use both, but form-constrained poetry (haiku, concrete, villanelle) strongly favors topology; constraint-based poetry (oulipo, clerihew) favors lexicon.

---

## Suggested Next Steps

1. **Test whether lexical S₂ predicts "literary quality" ratings** — form-induced S₂ may be a confound. A poem with high structural but low lexical S₂ might be structurally sophisticated but linguistically bland.
2. **Build a structural/lexical S₂ "fingerprint"** — each poet as a point in (structural, lexical) S₂ space. Are poets with similar aesthetics clustered?
3. **Temporal shift**: Does the structural-vs-lexical ratio shift across history? (Hypothesis: modernist poets shifted toward structural surprise; postmodern poets back toward lexical.)
4. **Compare S₂ on prose vs poetic line breaks for the same text** — what is the "cost" in structural S₂ of lineation?
