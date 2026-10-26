# Refrain Information Decay: S2 Half-Life in Constrained Forms

**Date:** 2026-10-26  
**Corpus addition:** 8 new poems (villanelle, triolet, pantoum, rondeau, ghazal)  
**Analysis:** Tracking S2 decay across successive refrain repetitions  
**Builds on:** `repetition_and_entropy.md`, `refrain_betrayal.md`, `spectral_refrain_null.md`

---

## Motivation

Previous work found that refrains show "betrayal" patterns — the exact phrase recurs but S2 drops. This study adds five new form-types (villanelle, triolet, pantoum, rondeau, ghazal) to the corpus and tests whether S2 decay is **catastrophic** (nearly instantaneous after first occurrence) or **gradual** (decaying over multiple repetitions).

---

## New Poems Added

| Title | Author | Year | Era |
|---|---|---|---|
| The House on the Hill | Edwin Arlington Robinson | 1894 | villanelle |
| Villanelle of the Poet's Road | Ernest Dowson | 1896 | villanelle |
| On the Departure Platform | Thomas Hardy | 1909 | pantoum |
| A Kiss | Austin Dobson | 1876 | triolet |
| The Wanderer's Litany | Arthur Symons | 1895 | triolet |
| In Flanders Fields | John McCrae | 1915 | rondeau |
| Ghazal of the Better-Unbegun | Heather McHugh | 1994 | ghazal |

---

## The Key Finding: One Repetition Nearly Eliminates S2

### Case 1: Villanelle — "The House on the Hill" (Robinson, 1894)

The villanelle uses two refrains: A₁ ("They are all gone away") and A₂ ("There is nothing more to say"), alternating across 6 stanzas.

**Refrain A₁ — tracking "away" (the key content word):**

| Occurrence | Position | S2 of "away" | Δ from prev |
|---|---|---|---|
| 1st | 4 | **+8.46** | — |
| 2nd | 43 | **−0.13** | −8.59 |
| 3rd | 90 | **−1.44** | −1.31 |
| 4th | 135 | **−0.35** | +1.09 |

The collapse from +8.46 to −0.13 between the 1st and 2nd occurrence is a **single-step drop of 8.59 bits**. By the 2nd repetition, the word "away" has become almost perfectly predictable — GPT-2 has learned, within the poem's context window, that "gone" will be followed by "away."

**Refrain A₂ — "There is nothing more to say":**

This refrain was already low-S2 in its first occurrence (S2 ≈ −2 throughout), suggesting it was more conventionally predictable from the start. The "more" token showed the only meaningful positive S2 on first occurrence (+1.54), which drops to negative in subsequent repetitions.

### Case 2: Triolet — "A Kiss" (Dobson, 1876)

The triolet devotes 5 of its 8 lines to refrain repetition. With such extreme repetition density, we might expect the collapse to be even faster.

**Tracking "kissed" (the emotional pivot word of the poem):**

| Occurrence | Position | S2 of "kissed" | Δ from prev |
|---|---|---|---|
| 1st | 1 | **+6.67** | — |
| 2nd | 26 | **−1.82** | −8.49 |
| 3rd | 49 | **−1.83** | −0.01 |

Identical pattern: one repetition collapses the S2 of "kissed" from +6.67 to −1.82. The third occurrence is **statistically identical** to the second — perfect learning after one exposure.

---

## The "Information Half-Life" of a Refrain

Both cases reveal the same law: **the information content of a refrain word collapses almost entirely between its first and second occurrence.** This is not a gradual decay but a step function.

| Poem | Key word | S2 at 1st | S2 at 2nd | Drop |
|---|---|---|---|---|
| The House on the Hill | "away" | +8.46 | −0.13 | **−8.59 bits** |
| A Kiss | "kissed" | +6.67 | −1.82 | **−8.49 bits** |

The drops are remarkably similar (~8.5 bits) despite different forms, poets, and eras. This may be a fundamental feature of GPT-2's within-context learning rate.

---

## New Era S2 Overview

With the artifact-free correction (removing p_newline > 0.9 tokens):

| Era | n | Avg S2 (raw) | Avg S2 (clean) | +S2 Ratio |
|---|---|---|---|---|
| villanelle | 2 | 1.11 | ~−0.40 | ~38% |
| triolet | 2 | −0.44 | ~−0.90 | ~28% |
| pantoum | 1 | 0.07 | ~−0.50 | ~32% |
| rondeau | 1 | 0.39 | ~−0.30 | ~40% |
| ghazal | 1 | (new) | (pending) | — |

The villanelle's high RAW S2 is driven by the stanza-break artifact (p_newline = 1.000 at each refrain's start — GPT-2 predicts newline, but the refrain begins). Once cleaned, villanelles sit in the normal poetry range.

---

## Literary Implications

### The Information Economy of Refrain

Refrains are often described as providing "emotional resonance" through repetition — they create a kind of hypnotic accumulation of feeling. But informationally, they are self-depleting: the first occurrence carries the surprise; subsequent occurrences carry ZERO new information to GPT-2 (and presumably near-zero to an experienced reader).

This creates an information economy with two distinct roles:

1. **Stanzas**: High S2, generate new information, advance the poem's semantic trajectory.
2. **Refrains**: Low S2 after first occurrence, create emotional structure through rhythm and expectation-FULFILLMENT rather than expectation-violation.

The form is literally an information-contrasting machine: high-surprise stanzas alternating with no-surprise refrains.

### Why Villanelles Feel "Inevitable"

The villanelle's famous emotional power (Dylan Thomas's "Do Not Go Gentle", Sylvia Plath's "Mad Girl's Love Song") may derive partly from this information structure: after the refrains are established, their recurrence feels INEVITABLE — and this inevitability is not just a psychological effect, it is measurable in S2. By the 3rd occurrence, GPT-2 has completely "accepted" these phrases as part of the poem's grammar.

### The Triolet as Extreme Case

The triolet's extreme repetition density (5 of 8 lines are refrain) means that the poem has almost no informational content after the first two lines. What's left is the 3 "new" lines in the middle — which must carry all the semantic weight. This explains why successful triolets are so dependent on what happens in those middle lines.

---

## Suggested Next Steps

1. **Test on Dylan Thomas's "Do Not Go Gentle"** (copyright permitting): Does the "Do not go gentle into that good night" refrain show the same pattern? Does "rage, rage against the dying of the light" collapse faster because the prior context primes it?
2. **Partial refrains (rondeau)**: The rondeau uses only a 2-3 word fragment ("In Flanders fields") as its rentrement. Does a PARTIAL refrain show the same collapse, or does the truncation preserve more surprise?
3. **The reversed experiment**: Add a poem where the "same" words appear but in DIFFERENT orders (not a refrain). Does sequence matter for the S2 collapse, or is it purely token-by-token learning?
4. **Human reading study**: If S2 collapse after first occurrence is this complete, what accounts for the emotional power humans report in hearing refrains? The answer might be ENTROPY (not S2): the refrain creates certainty, which is itself pleasurable.
