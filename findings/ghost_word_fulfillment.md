# Ghost Word Fulfillment: The Poem's Debt to Rejected Predictions

**Date:** 2026-10-09
**Experiment:** `experiments/ghost_word_fulfillment.py`
**Corpus:** 204 English poems (control excluded), 3,481 high-S2 moments (S2 ≥ 2.0)
**Builds on:** `straussian_gap_taxonomy.md`, `suppressed_lexicon.md`, `surprise_decay_curves.md`

---

## Research Question

When GPT-2 predicts word X but the poet chooses a different word Y (creating a high-S2
"Straussian gap"), does X — the *ghost word* — appear later in the poem? And if it does,
at what S2 level does it arrive?

**Hypothesis:** Poets create a semantic "debt" by rejecting the expected word. When the debt
is later paid (ghost word appears), it arrives in a highly expected context — the prediction
is finally fulfilled. Poems that never pay the debt sustain tension through permanent withholding.

---

## Core Finding: Ghost Words Arrive Resigned

### Fulfillment Rate
| | Count | % |
|---|---|---|
| High-S2 moments analyzed | 3,481 | — |
| Ghost word appears later in poem | 1,282 | **36.8%** |
| Ghost word never appears | 2,199 | **63.2%** |

### S2 at Fulfillment

When a ghost word does appear later, it arrives at dramatically *lower* S2 than the poem's
average:

| Metric | Value |
|---|---|
| Mean S2 at fulfillment | **−2.449** |
| Median S2 at fulfillment | **−3.009** |
| Mean poem-wide avg S2 (unfulfilled ghost moments) | +0.245 |
| **Resolution gap** (fulfillment S2 − poem avg) | **−2.652** |
| % of fulfilled ghost words arriving below poem average | **87.8%** |

The ghost word, when it finally appears, is not just below the poem's average — it is
dramatically below it. The median resolution gap is −3.1 bits. This is not random: words
that arrive at −3 S2 are words the model expected intensely. The poet placed the rejected
prediction in exactly the context where it was most inevitable.

**Interpretation:** The act of rejecting a prediction at a high-S2 moment creates a
*semantic reservation* in the poem. The word remains "pending." When it is eventually
used, it tends to appear in the most conventional, expected position possible — as if the
poet is paying off the debt quietly, at a moment of low surprise.

---

## Ghost Words: Fulfillment Rates by Token Type

The most illuminating split is between **function words** (which appear everywhere) and
**content words** (which can genuinely be withheld):

| Ghost Word | Times Rejected | Times Fulfilled | Fulfill % |
|---|---|---|---|
| **the** | 526 | 420 | **79.8%** |
| **and** | 208 | 158 | **76.0%** |
| **of** | 165 | 110 | **66.7%** |
| **to** | 105 | 65 | **61.9%** |
| **is** | 98 | 52 | **53.1%** |
| **in** | 58 | 33 | **56.9%** |
| **was** | 57 | 22 | **38.6%** |
| **he** | 40 | 19 | **47.5%** |
| **not** | 38 | 13 | **34.2%** |
| **you** | 34 | 19 | **55.9%** |
| **man** | 23 | 2 | **8.7%** |
| **world** | 17 | 0 | **0.0%** |

**The content word contrast is stark:**
- Function words ("the", "and", "of") are fulfilled at 67–80% — they almost inevitably
  appear in any poem, so rejecting them is only a momentary deferral.
- Content words like "man" (8.7%) and "world" (0%) are almost never fulfilled.
  These are GPT-2's "stock" poetic words — the clichéd vocabulary it reaches for at
  meaningful moments — and poets systematically suppress them permanently.

**"world" is rejected 17 times across the corpus and never once appears later.**
This is the most striking single statistic: GPT-2's most generic poetic word is used
as a prediction but never paid as a debt.

---

## Ghost Word Fulfillment by Era

| Era | N | Fulfill% | Fulfill S2 | Poem Avg | Gap |
|---|---|---|---|---|---|
| concrete | 6 | **66.7%** | −1.412 | 0.806 | −2.218 |
| deep_image | 14 | **57.1%** | −2.152 | 0.251 | −2.403 |
| found_poetry | 121 | **49.6%** | −2.047 | −0.284 | −1.763 |
| 19th_century | 253 | 43.1% | −2.615 | 0.251 | −2.866 |
| nursery_rhyme | 28 | 42.9% | −3.164 | 0.104 | −3.268 |
| ancient | 54 | 42.6% | −3.455 | 0.052 | −3.507 |
| victorian | 518 | 41.7% | −2.322 | 0.443 | −2.765 |
| romantic | 313 | 36.4% | −3.507 | 0.107 | −3.614 |
| modernist | 352 | 36.6% | −2.508 | 0.532 | −3.040 |
| confessional | 64 | **18.8%** | −1.743 | 0.624 | −2.366 |
| language | 21 | **14.3%** | −4.009 | 0.562 | −4.571 |
| surrealist | 8 | **12.5%** | −0.664 | −0.328 | −0.337 |
| haiku | 17 | **5.9%** | −2.390 | 2.043 | −4.433 |
| oulipo | 6 | **0.0%** | n/a | −0.121 | n/a |

### Era Pattern: Fulfillment Rate Tracks "Closure" Aesthetics

**High fulfillment eras** (concrete, deep image, found poetry, 19th century) tend toward
conventional closure and predictable vocabulary — the poem settles its debts. The high
rate for *concrete* and *deep image* may reflect their shorter, more concentrated texts
where every word circulates within a small vocabulary set.

**Low fulfillment eras** (haiku, Oulipo, surrealist, language poetry) resist closure and
conventional prediction. Haiku's 5.9% rate is extreme: in 17 syllables, a ghost word
rarely gets a second chance. Oulipo's 0% across all ghost words signals the genre's
radical rejection of conventional prediction entirely — the system suppresses GPT-2's
expectations and never delivers them.

**Language poetry** (14.3%) has an interesting property: when ghost words DO appear, they
arrive at S2 = −4.009 — the deepest average resolution of any era. Language poets rarely
pay their debts, but when they do, it is with conspicuous inevitability.

---

## Most Striking Individual Cases

### Maximum Resolution (Ghost Word Arrives at Lowest S2)

| Poem | Ghost | At S2 | Fulfillment S2 | Gap |
|---|---|---|---|---|
| Marianne Moore, "The Fish" | "the" | +2.55 | −6.72 | −8.08 |
| Hopkins, "The Windhover" | "the" | +7.55 | −7.40 | −7.74 |
| Keats, "To Autumn" | "the" | +5.41 | −7.67 | −7.34 |
| Layli Long Soldier, "Whereas" | "hand" | +4.56 | −6.83 | −7.34 |

The "hand" case is notable: at a high-S2 moment (S2=4.56), GPT-2 expected "hand" but
Long Soldier wrote "uncle." Later in the poem, "hand" appears at S2=−6.83 — extremely
expected, in a context where it was highly probable. The rejected body part becomes a
resolved one: the poem literally fulfills its suppressed gesture.

### Maximum Detonation (Ghost Word Arrives at Highest S2)

| Poem | Ghost | At S2 | Fulfillment S2 | Gap |
|---|---|---|---|---|
| Ferlinghetti, "In Goya's greatest scenes" | "in" | +3.79 | **+18.45** | **+18.53** |
| Moore, "The Fish" | "of" | +8.86 | +13.51 | +12.16 |
| Dickinson, "I heard a Fly buzz" | "around" | +6.55 | +9.94 | +9.02 |

These are cases where the ghost word is eventually used — but at a moment even MORE
surprising than where it was first rejected. Ferlinghetti's "in" at S2=18.45 represents
a paradox: the preposition GPT-2 most wanted is used where it is least expected. Dickinson's
"around" is rejected in favor of a dash, then appears in a maximally surprising context —
contributing to the poem's famous disorientation.

---

## Theoretical Interpretation

### The Semantic Debt Model

This experiment supports a **semantic debt** interpretation of poetic surprise. When a poet
writes a high-S2 token, they are not merely being idiosyncratic — they are implicitly promising
something to the model's prediction field. The rejected word hovers as an unfulfilled expectation.

**Two resolution strategies:**
1. **Payment** (36.8%): The ghost word appears later, in a maximally expected context. The
   debt is paid quietly. This is especially common for function words and in poetry with strong
   closure aesthetics (Victorian, romantic, concrete).
2. **Withholding** (63.2%): The ghost word never appears. The debt is permanent. This is
   the Oulipo and haiku strategy: each high-S2 moment creates a small irresolvable tension
   that accumulates across the poem.

### The Cliché Suppression Finding

The "world" and "man" statistics deserve special attention. GPT-2 reaches for "world" and "man"
at high-stakes moments (when confident predictions break down, it defaults to these abstractions).
Poets suppress these words entirely: "world" appears as a rejected ghost in 17 poems and is
**never subsequently used in any of them.**

This is not neutral — it is a systematic anti-cliché strategy. When the model predicts a stock
poetic abstraction, the poet not only refuses it at that moment, but refuses it for the rest of
the poem. The suppression is permanent, not deferred.

---

## Next Steps

1. **Control for word frequency**: Analyze ghost word fulfillment separately for function words
   vs. content words, controlling for base-rate frequency in the corpus.
2. **Lag analysis**: How many tokens later does a ghost word typically appear when fulfilled?
   Is there a preferred "distance" from rejection to fulfillment?
3. **Semantic field of unfulfilled ghosts**: What semantic categories of ghost words are most
   often permanently withheld? (We know "world" and "man"; are there others?)
4. **Cross-poet comparison**: Do individual poets have characteristic ghost-word strategies?
   Dickinson's ghost words may systematically remain unfulfilled; Whitman's may be resolved.
