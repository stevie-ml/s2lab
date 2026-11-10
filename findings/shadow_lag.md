# Shadow Lag: When Does the Suppressed Word Finally Arrive?

**Date:** 2026-11-10
**Experiment:** `experiments/shadow_lag.py` → `results/shadow_lag.json`
**Corpus:** 410 of 411 texts analyzed (1 empty)
**Builds on:** `shadow_vocab_fulfillment.md` (which found that 41% of suppressed words appear
later in the same poem), `stanza_break_artifact.md`

---

## Research Question

`shadow_vocab_fulfillment.md` established that 41% of GPT-2's suppressed content-word
predictions eventually appear elsewhere in the same poem. But **when** do they arrive?

This experiment tracks the **shadow lag**: the number of tokens between a suppression event
(the poet deviates from GPT-2's top prediction) and the first appearance of the suppressed
word elsewhere in the poem.

Three-tier classification:
- **Early** (lag ≤ 10 tokens): poet suppresses the word, then uses it almost immediately
- **Medium** (lag 11–50 tokens): moderate delay
- **Late** (lag > 50 tokens): suppressed word arrives much later in the poem, or never
- **Evaded** (lag = ∞): the shadow word never appears in this poem

**Core hypothesis**: Surprising poems (high avg_S₂) will have *longer* lags — the words the
model predicted arrive late or not at all. The shadow is deferred or permanently banished.

---

## Global Findings

| Metric | Value |
|--------|-------|
| Poems analyzed | 410 |
| **Mean shadow lag** (when fulfilled) | **32.6 tokens** |
| Median shadow lag | 28.1 tokens |
| **Global evasion rate** (shadow never arrives) | **85.7%** |
| Mean early-fulfillment rate | 5.1% |
| Mean late-fulfillment rate | 3.4% |
| Corr(avg\_S₂, evasion rate) | **+0.23** |
| Corr(poem length, evasion rate) | **−0.45** |
| Mean lag-diff: high-S₂ vs low-S₂ positions | **+2.3 tokens** |

**Finding 1**: Poets suppress GPT-2's predictions and the suppressed word never appears
in the poem 85.7% of the time. The vast majority of shadows are permanent.

**Finding 2**: Higher-S₂ poems evade their shadow vocabulary more (r=0.23), but poem
length is a stronger confound (r=−0.45). After controlling for length (poems > 50 tokens),
the correlation weakens to 0.15 but persists.

**Finding 3**: At high-S₂ positions within a poem, the shadow word arrives **2.3 tokens
later** than at low-S₂ positions. Surprise positions have slightly more deferred shadows.

---

## The Poetry vs. Prose Contrast (Key Finding)

| Group | lag-diff (high-S₂ − low-S₂) | Interpretation |
|---|---|---|
| **Poetry overall** | **+2.3** | Surprising choices defer their shadows |
| **Prose control** | **−5.2** | Surprising choices have EARLIER shadows |

In prose, when the author makes a statistically surprising choice, the shadow word tends to
arrive **sooner** than average — the text "corrects" itself back toward expectation quickly.

In poetry, when the poet makes a surprising choice, the shadow word arrives **later** —
the poem maintains the deviation and delays normalization.

**This is a structural distinction between prose and poetry**: prose reverts toward its own
shadow; poetry escapes it.

---

## Era Breakdown: Highest Evasion Rates

| Era | n | Evasion% | Mean lag | lag-diff |
|---|---|---|---|---|
| haiku | 14 | **99.5%** | 9.0 | — |
| pantoum | 1 | 98.7% | 71.0 | — |
| clerihew | 10 | 98.0% | 6.0 | — |
| confessional | 6 | **97.7%** | **1.9** | +3.5 |
| mid_century | 6 | 96.7% | 34.7 | **+58.8** |
| classical_chinese | 4 | 96.4% | 16.2 | +4.0 |

**Haiku and clerihew** top the evasion list, but this is partly a length artifact — very
short poems have no room for the shadow to return.

**Confessional poetry** is different: near-100% evasion, but with an extraordinary anomaly
— when a confessional poem does fulfill its shadow, the lag is only **1.9 tokens**. The shadow
word appears almost immediately adjacent to where it was suppressed. Confessional poets
(Plath, Sexton, Lowell, Berryman) almost never deliver what GPT-2 expects, but when they
relent — rarely — they do so in the very next phrase.

---

## Era Breakdown: Lowest Evasion Rates (Highest Fulfillment)

| Era | n | Evasion% | Mean lag | Explanation |
|---|---|---|---|---|
| concrete | 3 | **46.7%** | 16.4 | Maximal repetition within poems |
| villanelle | 3 | 64.8% | 41.2 | Mandatory refrain repetition |
| german_symbolist | 3 | 64.8% | 18.3 | Relatively conventional vocabulary |
| triolet | 2 | 75.1% | 20.5 | Mandatory repetition |

**Concrete poetry** has the lowest evasion (46.7%) because poems like Gomringer's "silencio"
use the same word repeatedly — the shadow vocabulary is fully delivered.

**Villanelle** (64.8% evasion) confirms the formal logic: the mandated refrain repetition
forces shadow fulfillment. When villanelles deviate (high-S₂), the lag-diff is **negative**
(−16.4 pooled across all three), meaning surprising choices in villanelles have shadows that
arrive *sooner* than expected choices. The refrain immediately follows the deviation.

---

## The lag-diff Spectrum: Who Defers Their Shadows Longest at High-S₂ Moments?

| Era | lag-diff (high − low S₂) | Interpretation |
|---|---|---|
| mid_century | **+58.8** | Maximum deferral at surprise positions |
| biblical | +23.7 | Psalm 136 refrain effect |
| ekphrastic | +16.1 | Description-driven long-range callbacks |
| early_modern | +11.1 | Long syntactic periods |
| imagist | +11.7 | Small corpus but striking |
| **control prose** | **−5.2** | Prose reverts quickly |
| fixed_form | −22.9 | Surprising moments resolve early |
| villanelle | −16.4 | Refrain resolves surprises immediately |

**Psalm 136** (lag-diff = +117.5) is the extreme outlier: its famous repeating refrain
("for his mercy endureth for ever") creates a situation where every verse begins with a
content-word deviation from the expected refrain pattern, and the refrain then arrives
~120 tokens later at the verse end. This is the most extreme "shadow deferral" in the corpus.

**Mid-century poetry** ("Traveling Through the Dark" is the sole representative here) shows
the most consistent deferral: surprising choices take substantially longer for the shadow
to arrive — perhaps reflecting the meditative, slow-movement quality of that style.

---

## Villanelle "Pre-Refrain Paradox"

The two villanelles with lag-diff data show **negative** lag-diff:
- The House on the Hill: −14.9
- Villanelle of the Unsaid: −17.8

**Interpretation**: In villanelles, the most *surprising* token positions are those just
before the mandatory refrain. At those positions, GPT-2's shadow vocabulary is immediately
fulfilled by the upcoming refrain line. So high-S₂ moments in villanelles have *earlier*
shadow resolution because the form provides a guaranteed resolution mechanism.

The villanelle is the inverse of confessional: confessional poetry suppresses almost
everything but occasionally yields, immediately. Villanelle formally delivers the shadow on
schedule, and its surprises are pre-resolved by the form's machinery.

---

## Hypothesis: Shadow Lag as a Measure of "Lexical Resistance"

We propose a **lexical resistance index** per poem:

```
LR = evasion_rate × (1 + lag_diff / mean_lag)
```

A poem with high evasion AND positive lag-diff (high-S₂ surprises are even more deferred)
has the highest lexical resistance. These are poems that most thoroughly escape GPT-2's
vocabulary world.

Top lexical resistance candidates from the data:
- Confessional poems (high evasion, rare but immediate fulfillment)
- Mid-century meditative poems (high evasion, positive lag-diff)
- Biblical anaphoric structures (Psalm 136)

Lowest lexical resistance:
- Concrete poems (fulfill their entire shadow vocabulary)
- Villanelles (form-mandated fulfillment)
- German prose control (fulfills quickly, negative lag-diff)

---

## Suggested Next Steps

1. **Compute formal lexical resistance index** across all 410 poems and correlate with
   literary reputation, era, and form.
2. **Within-poem lag trajectories**: track shadow lag at each stanza, testing whether
   lag decreases toward the end of a poem (gradual reconciliation with expectation).
3. **Quality of shadows at different lags**: are EARLY-fulfilled shadows semantically
   closer to the chosen word than LATE-fulfilled shadows?
4. **Cross-era lag-diff analysis** controlling for poem length via residualization.
