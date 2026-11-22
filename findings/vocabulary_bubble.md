# Vocabulary Bubble Formation: How Fast Does GPT-2 Learn a Poem's Own Words?

**Date:** 2026-11-22
**Experiment:** `experiments/vocabulary_bubble.py`
**Results:** `results/vocabulary_bubble.json`
**Corpus:** 436 texts (431 poetry + 5 control)
**New metric:** *Vocabulary recapture rate* and *bubble slope*

---

## Research Question

As a poem progresses, GPT-2 may start predicting words that already appeared earlier
in the poem — forming a "lexical bubble." The question: does the poem train GPT-2 on
its own vocabulary? And do different forms, eras, and poets differ in how fast they
create this bubble?

**Vocabulary recapture rate** at position *i* = fraction of GPT-2's top-10 predictions
that are words already used earlier in the poem.

**Bubble slope** = linear rate of change in recapture rate from start to end of poem.
Higher slope → faster bubble formation.

---

## Finding 1: The Lexical Bubble Grows Monotonically

Averaged across all 431 poetry texts (artifact-filtered tokens, p_newline < 0.9):

| Decile | Poetry Recapture | Control Recapture | Poetry α (Zipf) |
|--------|-----------------|-------------------|-----------------|
| D1 (first 10%) | 6.7% | 0.0% | 1.153 |
| D2 | 19.4% | 5.7% | 1.286 |
| D3 | 26.7% | 4.5% | 1.306 |
| D4 | 30.9% | 12.2% | 1.335 |
| D5 | 34.4% | 18.7% | 1.380 |
| D6 | 37.1% | 21.2% | 1.392 |
| D7 | 39.1% | 14.5% | 1.388 |
| D8 | 41.2% | 21.3% | 1.376 |
| D9 | 43.5% | 29.0% | 1.387 |
| D10 (last 10%) | **44.7%** | 26.0% | **1.454** |

By the final decile, **nearly half of GPT-2's top-10 predictions are words
that already appeared in the poem.** This rise is monotonic and consistent.

The parallel rise in Zipf-α confirms the finding from `perfect_ambush_analysis.md`:
the bubble creates both vocabulary recycling AND prediction concentration — two
aspects of the same entrainment process.

**Poetry forms bubbles faster than prose control** (avg slope: 0.373 vs 0.298).
The poem's compressed vocabulary (fewer total words) creates stronger feedback loops
than the more expansive vocabulary of prose.

---

## Finding 2: The Bubble Trap — High-Bubble Poems Have More Negative Late-S2

Splitting poems into high-bubble (top quartile, slope ≥ 0.44) vs
low-bubble (bottom quartile, slope ≤ 0.30):

| Group | Early S2 (D1–D3) | Late S2 (D8–D10) | Δ |
|-------|-----------------|-----------------|---|
| High-bubble poems | **−0.097** | −0.634 | −0.537 |
| Low-bubble poems  | −0.217 | **−0.488** | −0.271 |

**Key pattern:**
- High-bubble poems start *more surprising* (higher early S2)
- But end *less surprising* (more negative late S2)
- The bubble "traps" the model in conformity — once GPT-2 has learned the
  poem's vocabulary, it becomes very good at predicting the poem's words,
  and the poet increasingly writes those expected words

Low-bubble poems show less dramatic fall-off: they maintain more consistent
surprise throughout because their vocabulary keeps changing.

**Interpretation:** Poems with tight, repeated vocabulary (Dickinson, Clifton,
metaphysical conceit poems) create strong bubbles and show a larger S2 arc:
high initial surprise followed by increasing entrainment. Poems with expansive,
ever-new vocabulary (Ferlinghetti, beat poets, Whitman catalogs) resist the
bubble and maintain more uniform surprise.

Correlation between bubble slope and overall S2: r = −0.104 (weak, negative).
Bubble formation is *not* simply a measure of S2 level — it's an independent
dimension of how poems manage linguistic expectation over time.

---

## Finding 3: Fastest and Slowest Bubble-Forming Poems

**Top 10 fastest bubble-forming poems** (slope ≥ 0.57):

| Bubble Slope | Final Recapture | Author | Title |
|---|---|---|---|
| **0.621** | 60.0% | Lucille Clifton | "Won't You Celebrate With Me" |
| **0.618** | 63.1% | Emily Dickinson | "I heard a Fly buzz — when I died" |
| **0.605** | 66.9% | Thomas Wyatt | "Whoso List to Hunt" |
| **0.600** | 47.5% | John Ashbery | "The One Thing That Can Save America" |
| **0.578** | 62.7% | T.S. Eliot | "The Hollow Men (opening)" |
| **0.570** | 58.2% | Robert Burns | "To a Mouse (closing stanzas)" |
| **0.568** | 53.3% | Thomas Traherne | "Wonder" |
| **0.567** | 60.0% | Russell Edson | "The Fall" |

Pattern: short lyrics with limited vocabulary and intense focus — Dickinson's
spare diction, Clifton's repeated proclamations, Wyatt's courtly refrain.

**Top 10 slowest bubble-forming (maximum novelty) poems** (slope ≤ 0.15):

| Bubble Slope | Final Recapture | Author | Title |
|---|---|---|---|
| **0.156** | 5.0% | Lorine Niedecker | "Lorine's Work" |
| **0.139** | 15.0% | William Carlos Williams | "The Red Wheelbarrow" |
| **0.123** | 20.0% | Richard Wright | "Nobody" |
| **0.100** | 45.8% | Lawrence Ferlinghetti | "In Goya's greatest scenes" |
| **0.096** | 20.0% | Yosa Buson | "Temple Bells (Buson, translated)" |
| **0.093** | 31.1% | E.E. Cummings | "Buffalo Bill 's" |
| **0.092** | 32.4% | Kamau Brathwaite | "Calypso" |
| **0.015** | 37.1% | Lawrence Ferlinghetti | "Constantly Risking Absurdity" |

**Ferlinghetti appears twice in the lowest-bubble group.** His "Constantly Risking
Absurdity" has a nearly flat bubble (slope = 0.015) — the lowest in the corpus.
This aligns perfectly with his dominance of the "perfect ambush" rankings
(findings/perfect_ambush_analysis.md): his spatial typography and ever-fresh
imagery consistently defeat even a fully-entrained model. He is the anti-bubble poet.

---

## Finding 4: Era Rankings by Bubble Slope

| Era | n | Avg Slope | Final Recapture | Recapture Gain |
|-----|---|-----------|-----------------|----------------|
| metaphysical | 7 | **0.460** | 53.7% | 46.4% |
| early_modern | 11 | **0.459** | 54.0% | 44.5% |
| german_expressionist | 6 | 0.457 | 51.6% | 47.2% |
| war_poetry | 3 | 0.457 | 53.6% | 45.9% |
| ekphrastic | 8 | 0.457 | 61.2% | 49.6% |
| biblical | 8 | 0.450 | 52.8% | 43.6% |
| new_york_school | 26 | 0.440 | 45.5% | 41.8% |
| *…* | | | | |
| haiku | 14 | 0.258 | 32.6% | 32.6% |
| song_lyrics | 3 | 0.257 | 46.5% | 37.5% |
| japanese_classical | 2 | 0.257 | 32.5% | 32.5% |
| beat | 8 | **0.255** | 37.6% | 23.2% |
| clerihew | 10 | **0.217** | 22.0% | 21.7% |

**Metaphysical and early_modern poetry form the strongest bubbles** — these are
poems built on extended conceits (Donne's compass metaphor, Marvell's garden),
where a single semantic field dominates the poem's entire vocabulary. The conceit
literally trains GPT-2 to predict within the poem's private lexicon.

**Clerihew has the lowest slope** — consistent with its micro-length format; with
only 4 lines, there is barely enough poem to form a bubble. The metric here is
essentially measuring context accumulation, and clerihews have almost none.

**Beat poetry has the second-lowest slope** — Beat poets (Ginsberg, Ferlinghetti,
Corso) deliberately maintain lexical freshness, introducing new images and
references throughout rather than developing a single sustained conceit.
This aligns with their perfect-ambush density (findings/perfect_ambush_analysis.md).

---

## Synthesis: Two Modes of Managing the Bubble

1. **Bubble-riding (high slope)**: Build a tight vocabulary field early, then work
   within it — using expected words while still making locally surprising choices.
   The bubble provides constraint and form. Metaphysical poets, early modern sonneteers,
   Dickinson.

2. **Bubble-escaping (low slope)**: Maintain constant lexical novelty, defeating
   GPT-2's attempt to learn the poem's vocabulary. High perfect-ambush potential,
   sustained throughout. Beat poets, imageists, haiku masters.

The correlation between bubble slope and S2 (r = −0.104) is weak, meaning both
strategies can achieve high poetic surprise — they just achieve it differently.
Bubble riders front-load their S2 and then settle into form; bubble escapers
maintain it throughout.

---

## Suggested Next Steps

1. **Bubble confirmation rate**: Of the tokens where recapture is high,
   what fraction does the poet *actually use* (confirmed expected words)?
   This would distinguish "bubble riding" from "bubble resistance" within
   the same high-slope poem.

2. **Conceit detection**: Are metaphysical poems' bubbles organized around
   specific semantic fields (body/soul, compass/journey)? Can we identify the
   conceit's vocabulary from the top GPT-2 predictions in the bubble?

3. **Bubble and reader comprehension**: Do high-bubble poems feel more
   "complete" to readers because their vocabulary is more internally coherent?
   Testable via reader ratings if available.
