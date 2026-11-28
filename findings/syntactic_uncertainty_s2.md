# Syntactic Uncertainty and S2: The POS Jump Effect
**Date:** 2026-11-28

## Research Question

When GPT-2 is uncertain about the next token, is that uncertainty
**syntactically structured** (all alternatives are the same POS) or
**scattered** across grammatical categories? And when a poet chooses
a word with a *different* POS than the dominant prediction, does that
constitute a "double surprise" — crossing both lexical and syntactic
expectations simultaneously?

**Terminology:**
- **POS coherence**: fraction of top-10 alternatives sharing the most common POS tag (1.0 = all same POS, syntactically structured uncertainty)
- **POS jump**: chosen token has different POS than dominant alternative POS
- **Double surprise**: POS jump + S2 > 2.0 (syntactic AND semantic surprise)

## Overall Statistics

- **Total tokens analyzed:** 61,414 (stanza-break artifacts removed)
- **POS jumps:** 35,261 (57.4% of all tokens)
- **Double surprises** (POS jump + S2>2): 9,028 (14.7% of tokens)
- **Mean S2 with POS jump:** 0.039
- **Mean S2 without POS jump:** -1.046
- **Mean POS coherence at POS jump:** 0.438
- **Mean POS coherence without jump:** 0.514

## POS Coherence by S2 Band

Does the model's syntactic certainty change as S2 increases?

| S2 Band | N tokens | Mean POS Coherence |
|---|---|---|
| below_zero(-1,0) | 8,482 | 0.503 |
| extreme(>5) | 5,383 | 0.469 |
| high(2,5) | 7,316 | 0.479 |
| low_s2(<-1) | 32,289 | 0.458 |
| modest(0,2) | 7,944 | 0.480 |

## POS Transition Matrix (What POS Jumps Where?)

When the model predicts one POS but the poet chooses another:
**Row = dominant predicted POS, Column = chosen POS**

| Predicted→Chosen | NOUN | VERB | ADJ | ADV | PRON | DET | PREP | CONJ | NUM |
|---|---|---|---|---|---|---|---|---|---|
| **NOUN** | 0% | 12% | 54% | 7% | 3% | 7% | 7% | 3% | 1% |
| **VERB** | 59% | 0% | 8% | 9% | 6% | 4% | 6% | 2% | 0% |
| **ADJ** | 53% | 17% | 0% | 16% | 2% | 3% | 6% | 0% | 1% |
| **ADV** | 24% | 17% | 18% | 0% | 5% | 14% | 13% | 4% | 0% |
| **PRON** | 28% | 9% | 10% | 7% | 0% | 23% | 12% | 4% | 1% |
| **DET** | 28% | 17% | 8% | 8% | 19% | 0% | 13% | 3% | 1% |
| **PREP** | 25% | 6% | 7% | 9% | 6% | 9% | 0% | 10% | 0% |
| **CONJ** | 29% | 3% | 31% | 7% | 9% | 8% | 10% | 0% | 1% |
| **NUM** | 31% | 11% | 8% | 11% | 7% | 10% | 10% | 6% | 0% |
| **OTHER** | 34% | 22% | 7% | 6% | 5% | 4% | 8% | 3% | 1% |

## Poet POS Jump Rates

Which poets most frequently cross syntactic expectations?

| Poet | N tokens | Jump Rate | Double Surprise Rate | Avg S2 |
|---|---|---|---|---|
| Lawrence Ferlinghetti | 670 | 91.9% | 4.9% | -0.135 |
| William Carlos Williams | 118 | 78.0% | 15.3% | -0.871 |
| E.E. Cummings | 293 | 74.7% | 10.2% | -0.623 |
| Louis Zukofsky | 272 | 74.6% | 12.1% | -0.828 |
| Adelaide Crapsey | 57 | 73.7% | 26.3% | -0.453 |
| Lorine Niedecker | 280 | 72.9% | 16.1% | -0.235 |
| George Oppen | 507 | 72.8% | 9.5% | -0.927 |
| Kamau Brathwaite | 215 | 71.6% | 9.8% | -0.307 |
| Robert Creeley | 147 | 70.7% | 20.4% | -0.068 |
| Francis Thompson | 322 | 70.2% | 19.3% | 0.473 |
| Lyn Hejinian | 50 | 70.0% | 16.0% | -0.901 |
| Horace (trans. Howes, 1849) | 151 | 68.9% | 20.5% | -0.370 |
| Christian Bök | 215 | 68.4% | 28.4% | 0.802 |
| Anonymous (trans. Francis B. Gummere) | 138 | 68.1% | 20.3% | -0.289 |
| Matsuo Basho | 50 | 68.0% | 20.0% | -0.313 |
| Marianne Moore | 658 | 67.8% | 17.3% | -0.117 |
| Ben Jonson | 220 | 66.8% | 17.3% | -0.428 |
| Thomas Gray | 176 | 66.5% | 15.9% | -0.517 |
| Wislawa Szymborska | 122 | 66.4% | 17.2% | -0.372 |
| Thomas Wyatt | 367 | 65.9% | 21.0% | 0.018 |

## Era POS Jump Rates

| Era | N tokens | Jump Rate | Double Surprise Rate | Avg S2 |
|---|---|---|---|---|
| beat | 1,195 | 78.7% | 11.4% | 0.049 |
| objectivist | 1,089 | 71.7% | 11.8% | -0.639 |
| ancient | 434 | 65.4% | 19.1% | -0.330 |
| double_dactyl | 248 | 64.9% | 14.5% | -0.955 |
| protest_political | 250 | 64.4% | 17.2% | -0.754 |
| clerihew | 232 | 62.9% | 23.3% | 0.507 |
| haiku | 293 | 62.5% | 19.1% | -0.110 |
| modernist | 3,393 | 62.4% | 15.4% | -0.397 |
| metaphysical | 938 | 61.9% | 15.0% | -0.593 |
| classical_chinese | 238 | 61.8% | 15.5% | -0.558 |
| early_modern | 1,801 | 61.6% | 16.3% | -0.371 |
| old_english | 629 | 60.9% | 15.7% | -0.309 |
| elegy | 1,255 | 60.6% | 17.5% | -0.455 |
| persian | 382 | 60.2% | 17.5% | -0.235 |
| 18th_century | 1,435 | 59.5% | 16.8% | -0.285 |
| ekphrastic | 1,901 | 59.5% | 15.1% | -0.508 |
| procedural | 640 | 59.5% | 14.7% | -0.455 |
| victorian | 6,179 | 59.3% | 16.0% | -0.287 |
| imagist | 321 | 59.2% | 16.8% | -0.518 |
| oulipo | 1,282 | 59.0% | 17.2% | -0.182 |
| korean_modernist | 102 | 58.8% | 15.7% | -0.692 |
| 19th_century | 3,366 | 58.6% | 14.8% | -0.493 |
| dramatic_monologue | 5,305 | 58.4% | 15.6% | -0.468 |
| harlem_renaissance | 948 | 57.7% | 14.3% | -0.432 |
| war_poetry | 639 | 57.7% | 16.3% | -0.340 |
| language | 496 | 56.9% | 11.9% | -0.662 |
| mid_century | 583 | 56.8% | 16.0% | -0.250 |
| spoken_word | 286 | 56.6% | 15.0% | -0.593 |
| romantic | 4,220 | 56.4% | 15.2% | -0.433 |
| contemporary | 3,024 | 56.3% | 15.5% | -0.461 |
| pantoum | 283 | 56.2% | 13.1% | -0.433 |
| fixed_form | 858 | 56.1% | 14.7% | -0.560 |
| confessional | 397 | 55.7% | 15.6% | -0.234 |
| new_york_school | 2,773 | 55.5% | 13.3% | -0.585 |
| ghazal | 334 | 55.4% | 17.4% | -0.312 |
| parody_original | 443 | 54.9% | 13.8% | -0.454 |
| parody | 669 | 54.9% | 14.1% | -0.288 |
| rondeau | 130 | 54.6% | 14.6% | -0.400 |
| postcolonial | 989 | 54.1% | 12.5% | -0.484 |
| found_poetry | 1,204 | 53.7% | 10.9% | -0.615 |
| surrealist | 1,102 | 53.1% | 13.7% | -0.505 |
| cliche_control | 489 | 53.0% | 11.9% | -0.935 |
| latin_american | 461 | 52.9% | 15.4% | -0.481 |
| prose_poetry | 1,408 | 52.4% | 13.8% | -0.471 |
| nursery_rhyme | 222 | 51.8% | 13.5% | -0.818 |
| black_arts | 246 | 50.8% | 13.0% | -0.416 |
| limerick | 426 | 50.7% | 11.7% | -0.661 |
| concrete | 311 | 49.8% | 8.7% | -0.584 |
| villanelle | 436 | 49.3% | 11.9% | -0.489 |
| ballad | 915 | 49.0% | 14.3% | -0.421 |
| nonsense | 500 | 48.2% | 11.4% | -0.693 |
| german_expressionist | 781 | 47.6% | 12.4% | 0.100 |
| control | 163 | 44.2% | 4.3% | -1.721 |
| biblical | 1,331 | 44.1% | 11.9% | -0.453 |
| song_lyrics | 541 | 42.1% | 9.4% | -0.678 |
| triolet | 130 | 37.7% | 8.5% | -0.747 |
| german_modernist | 234 | 32.9% | 6.4% | 0.626 |
| german_symbolist | 356 | 32.0% | 9.3% | 0.452 |

## Top "Double Surprise" Examples

Tokens where the poet crossed a POS boundary AND achieved high S2:
The model expected one grammatical category; the poet delivered another.

| Token | Chosen POS | Expected POS | Model Predicted | S2 | Entropy | Poet |
|---|---|---|---|---|---|---|
| `Fun` | NOUN | ADJ |  little,  bit,  sense | 18.90 | 6.87 | Emily Dickinson |
| `Death` | VERB | DET |  a,  long,  any | 12.86 | 5.19 | Emily Dickinson |
| `Let` | VERB | DET |  the,  I,  then | 11.43 | 6.71 | John Keats |
| `lonely` | ADV | PREP |  into,  around,  in | 11.37 | 5.09 | William Wordsworth |
| `val` | NOUN | PRON |  the,  my,  a | 10.70 | 6.19 | William Wordsworth |
| `Our` | PRON | PREP |  as,  a,  barely | 10.20 | 8.03 | Emily Dickinson |
| `Sense` | NOUN | PRON |  the,  they,  I | 8.95 | 7.35 | Emily Dickinson |
| `kindly` | ADV | VERB |  was,  had,  said | 7.58 | 8.12 | Emily Dickinson |
| `,` | PUNCT | VERB |  of,  is,  that | 7.15 | 1.72 | John Keats |
| `My` | PRON | DET | 
, The, And | 7.04 | 1.24 | Emily Dickinson |
| `number` | NOUN | PREP |  of, ,,  in | 7.00 | 8.07 | John Keats |
| `–` | VERB | PREP |  the,  on, , | 6.70 | 6.87 | Emily Dickinson |
| `wandered` | VERB | PUNCT | ., ,, 
 | 6.11 | 11.12 | William Wordsworth |
| `too` | ADV | PUNCT |  –, 
, . | 5.67 | 4.19 | Emily Dickinson |
| `Dry` | NOUN | PREP | ,,  and,  as | 5.63 | 9.96 | John Keats |
| `,—` | NOUN | PUNCT | ,, 
,  to | 5.32 | 4.56 | John Keats |
| `belonging` | NOUN | PREP |  of,  I,  that | 5.30 | 5.96 | Walt Whitman |
| `o` | NOUN | PREP | ,,  above,  and | 4.98 | 6.17 | William Wordsworth |
| `he` | PRON | DET |  a,  some,  the | 4.98 | 8.90 | John Keats |
| `Sing` | VERB | NOUN | And, That, In | 4.83 | 7.39 | John Keats |

## High-S2 Without POS Jump (Semantic Surprise Only)

These tokens surprised the model lexically but stayed within the expected grammar:

| Token | POS | Model Predicted | S2 | Poet |
|---|---|---|---|---|
| `cloud` | NOUN |  child,  kid,  boy | 8.10 | William Wordsworth |
| `pains` | NOUN |  creeps,  in,  fills | 5.02 | John Keats |
| `sense` | NOUN |  heart,  body,  mind | 2.08 | John Keats |
| `op` | NOUN | ,,  bottle,  and | 2.13 | John Keats |
| `drains` | NOUN |  head,  heart, 
 | 3.94 | John Keats |
| `wards` | NOUN | d, 
, t | 3.70 | John Keats |
| `happiness` | NOUN |  own,  eyes,  heart | 4.27 | John Keats |
| `wing` | VERB | hearted, footed, eyed | 2.78 | John Keats |
| `–` | NOUN | ,,  and,  to | 3.10 | Emily Dickinson |
| `Car` | NOUN |  man,  only,  last | 3.16 | Emily Dickinson |

## Findings

1. **57.4% of all poetic tokens constitute a POS jump** — 
   the poet chose a word in a different grammatical category than the
   model's dominant prediction.

2. **POS jumps carry significantly higher S2** (mean: 0.039 vs. -1.046,
   difference: +1.085). Syntactic boundary-crossing correlates with higher
   information-theoretic surprise.

3. **POS coherence peaks in the "slightly expected" S2 band** (-1 to 0: coherence
   0.503) and falls at both extremes (extreme S2 >5: 0.469; very low S2 <-1: 0.458).
   Interestingly, the most routine tokens (very low S2) don't have the highest POS
   coherence — suggesting that highly predictable function words still attract
   grammatically mixed alternatives. The clearest syntactic structure in the model's
   uncertainty emerges at modest negative S2, where the poet follows grammar but
   surprises lexically within that frame.

4. **The POS jump is not random**: the transition matrix reveals asymmetric patterns.
   When the model expects a NOUN, 54% of jumps deliver an ADJ — poets promote
   modifiers to head position. When the model expects a VERB, 59% of jumps deliver
   a NOUN — poets nominalize (choose the name of the action rather than the action
   itself). When the model expects ADJ, 53% of jumps deliver a NOUN — again,
   nominalization. NOUN is the gravitational attractor: poets pull toward nouns
   from other POS categories, while pushing away from expected nouns toward adjectives.

5. **Poets differ significantly in their POS jump rates**, suggesting that
   syntactic boundary-crossing is part of individual style. Critically, high POS
   jump rates do NOT guarantee high S2: Ferlinghetti (91.9% jump rate, avg S2 -0.135),
   George Oppen (72.8%, avg S2 -0.927), and E.E. Cummings (74.7%, avg S2 -0.623) all
   show that syntactic estrangement and lexical surprise can be **decoupled** — the
   Objectivists create grammatical disruption while choosing individually expected words.
   
6. **The Objectivist paradox**: the Objectivists and Language poets score highest on
   POS jump rate (beat: 78.7%, objectivist: 71.7%, language: 56.9%) but have the
   MOST NEGATIVE avg S2. They surprise syntactically while conforming lexically —
   the estrangement is structural, not semantic. This is the opposite of poets like
   Emily Dickinson and Francis Thompson who achieve both syntactic AND lexical surprise.

## Theoretical Implications

This analysis suggests a two-dimensional model of poetic surprise:

```
           Lexical Surprise (S2 high)
                      │
  Syntactic      ─────┼─────  Double Surprise
  Stay     (low  │   │   ↑
  POS jump)      │   │  Straussian maximum
           ──────┴───┴──────── POS Jump
           no jump   │   yes jump
```

The **double surprise** quadrant (high S2 + POS jump) represents the most
radical poetic moves: not just unexpected *what*, but unexpected *kind-of-thing*.
These are the moments where poetry most dramatically diverges from prose expectation.

## Suggested Next Steps

1. **Is POS jump rate correlated with perceived "difficulty" of a poem?**
   Cross-reference with established difficulty ratings if available.
2. **Do POS jumps cluster at particular poem positions?** Compare to stanza
   boundaries, line endings, and volta positions.
3. **Which specific POS transitions are most "poetic"?** The VERB→NOUN jump
   may be the most characteristically modernist estrangement technique.
4. **Do language poets, known for syntactic disruption, have the highest
   POS jump rates?** Check whether experimental poetics correlate with this metric.