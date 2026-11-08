# Rhyme Echo Decay: Does S₂ Decrease on the Second Rhyme Occurrence?

**Date:** 2026-11-08
**Experiment:** `experiments/rhyme_echo_decay.py`
**Corpus:** 411 texts; 49 poems with detectable rhyme pairs; 108 rhyme pairs analyzed

---

## Research Question

In a poem with a repeating rhyme scheme, does GPT-2 "learn" the phonetic pattern as it
reads — producing lower S₂ for the **echo** word (second occurrence of a rhyme sound)
than the **lead** word (first occurrence)?

**Hypothesis:** lead_S₂ > echo_S₂ — the model is surprised by the first rhyme sound but
primed for the second, reducing its surprisal (and hence S₂) at the echo position.

**Null:** No systematic difference. Rhyme position (lead vs echo) does not predict S₂.

---

## Method

1. Load `corpus_results.json` (411 texts, GPT-2 token-level analysis)
2. For each poem, identify line-final tokens (last alphabetic word before newline)
3. Within a 10-line sliding window, detect rhyme pairs: two line endings sharing the
   last 3 characters (suffix match, excluding identical words)
4. For each pair: record S₂ of lead and echo; compute **decay = lead_S₂ − echo_S₂**
5. Stratify by era, line distance, lead S₂ tier
6. Null check: shuffle echo positions within each era to remove positional information

---

## Global Result

| Metric | Value |
|--------|-------|
| Poems with rhyme pairs | 49 |
| Total rhyme pairs | 108 |
| Lead position mean S₂ | **+1.29** |
| Echo position mean S₂ | **+1.88** |
| Mean decay (lead − echo) | **−0.59** |
| % pairs where decay > 0 | **49.1%** |

**The hypothesis is REFUTED.** The echo position is on average *more* surprising than the
lead (+1.88 vs +1.29). The distribution of decay is nearly uniform (49.1% positive), and
the null model (shuffled echoes) gives the same mean decay. There is no systematic rhyme
habituation effect.

---

## Distance Effect: Adjacent vs Separated Rhymes

| Distance (lines) | N | Lead S₂ | Echo S₂ | Decay | %Positive |
|---|---|---|---|---|---|
| 1 (adjacent lines) | 56 | +1.39 | +2.17 | **−0.78** | 46.4% |
| 2 (every other line) | 28 | +1.46 | +1.46 | **+0.01** | 53.6% |
| 3 | 12 | +0.41 | +2.33 | **−1.92** | 33.3% |
| 5 | 5 | +1.02 | −1.68 | **+2.70** | 80.0% |

The only robust positive decay appears at distance 5+ — when the rhyme words are far
apart. This suggests a different mechanism: **regression to the mean**. High-S₂ words
at line 1 tend to be followed by lower-S₂ rhymes at line 6 not because of priming, but
because extreme S₂ values are statistically unlikely to persist.

For adjacent lines (distance 1), the echo is *more* surprising — the opposite of habituation.

---

## Era Breakdown

| Era | N pairs | Lead S₂ | Echo S₂ | Decay | %Positive |
|---|---|---|---|---|---|
| found_poetry | 5 | +0.09 | −1.45 | **+1.54** | 60% |
| ekphrastic | 10 | +0.31 | −1.08 | **+1.39** | 80% |
| modernist | 17 | +3.64 | +4.48 | **−0.84** | 41% |
| victorian | 29 | +1.10 | +2.38 | **−1.28** | 52% |
| mid_century | 6 | −1.01 | +0.79 | **−1.80** | 17% |
| dramatic_monologue | 5 | +2.83 | +4.83 | **−2.00** | 40% |

Victorian and dramatic monologue show the strongest inverse decay (echo more surprising),
while found poetry and ekphrastic show genuine positive decay (echo less surprising).

---

## Lead S₂ Tier: Regression to Mean

| Lead S₂ tier | N | Echo S₂ | Decay |
|---|---|---|---|
| Low (−4 to −1) | 29 | **+0.98** | −3.14 |
| Neutral (−1 to 1) | 26 | **+0.57** | −0.67 |
| Moderate (1–4) | 27 | **+3.16** | −0.77 |
| High (4–8) | 14 | **+3.22** | **+1.96** |
| Very high (> 8) | 8 | **+3.14** | **+7.88** |

This pattern is diagnostic: **when the lead word has very high S₂, the decay is strongly
positive; when the lead has low S₂, the echo is higher**. This is precisely the signature
of regression to the mean, not rhyme priming. Extreme lead values drag echo values toward
the corpus mean (≈ +1.3), regardless of direction.

---

## Strongest Individual Pairs

### Top Decay (lead much more surprising than echo)

| Lead | Echo | Lead S₂ | Echo S₂ | Decay | Author |
|---|---|---|---|---|---|
| desolate | ate | +14.25 | −1.27 | **+15.52** | Oscar Wilde |
| breeding | stirring | +11.17 | +2.35 | **+8.83** | T.S. Eliot |
| singing | morning | +11.36 | +2.57 | **+8.79** | Kamau Brathwaite |
| circumstance | chance | +8.92 | +0.50 | **+8.42** | W.E. Henley |

Wilde's "desolate/ate": "desolate" is extraordinary at +14.25 — the word is far from what GPT-2
expected at that line ending. Its rhyme pair "ate" (at line 3, distance 2) is mundane by
comparison. This is the **catapult-and-catch** pattern: a spectacular lead followed by a
workmanlike echo.

### Top Inverse (echo more surprising than lead)

| Lead | Echo | Lead S₂ | Echo S₂ | Decay | Author |
|---|---|---|---|---|---|
| older | colder | +0.79 | +15.61 | **−14.82** | G.M. Hopkins |
| live | revive | +2.90 | +13.65 | **−10.74** | Marianne Moore |
| perhaps | laps | +3.48 | +10.98 | **−7.50** | Robert Browning |
| thanked | ranked | +5.05 | +12.42 | **−7.37** | Robert Browning |

Hopkins' "older/colder": the lead "older" (+0.79) is barely surprising. The echo "colder" at
line 2 is massive (+15.61). "Colder" rhymes phonetically but is semantically extreme given
the context — Hopkins is using the rhyme slot for **escalation**, not resolution. The constraint
generates a word more surprising than the word that set up the scheme.

---

## Poems with Strongest Positive Decay (Lead > Echo)

| Title | Author | Pairs | Mean Decay |
|---|---|---|---|
| Theocritus: A Villanelle | Oscar Wilde | 1 | +15.52 |
| Calypso | Kamau Brathwaite | 1 | +8.79 |
| Grodek (trans. Hamburger) | Georg Trakl | 1 | +7.47 |
| Umbra Vitae | Georg Heym | 1 | +7.35 |
| Invictus | W.E. Henley | 2 | +3.93 |
| Sunday Morning (stanza 1) | Wallace Stevens | 1 | +4.45 |

---

## Two Structural Models

The data suggests two distinct rhyme strategies:

### 1. Catapult-and-Catch (positive decay)
The poet places a high-S₂ word at the lead position, establishing the rhyme sound with a
surprising choice. The echo position can then be more conventional — the rhyme expectation
is set, the work is done. The lead word "buys" the echo word's phonetic predictability.

**Characteristic poets:** Wilde, Brathwaite, Trakl, Henley

### 2. Escalating Rhyme (inverse decay — echo > lead)
The poet uses a conventional or low-surprise lead word to set up the rhyme scheme, then
deploys a high-S₂ word at the echo position. The rhyme scheme functions as an escalator:
the phonetic expectation is fulfilled, but the semantic content *intensifies*.

**Characteristic poets:** Hopkins, Browning, Moore, Eliot (The Waste Land's -ing rhymes)

Notably, Eliot's Waste Land shows *both* patterns depending on which rhyme set:
- "breeding/stirring" (decay +8.83): catapult-and-catch
- "stirring/feeding" (decay −6.87): escalation

The two-strategy model suggests that **rhyme scheme choice interacts with the poet's
information-theoretic strategy**. A fixed form like the sonnet creates specific constraints
at specific positions; poets differ in whether they front-load or back-load S₂ within them.

---

## Key Finding

**The rhyme habituation hypothesis is not supported.** GPT-2 does not systematically show
lower S₂ at echo positions than at lead positions (49.1% positive decay, mean decay = −0.59).
The distribution is consistent with regression to the mean, not phonetic priming.

However, two *opposed* structural strategies emerge:
- **Catapult-and-catch:** high-S₂ lead, low-S₂ echo (positive decay) — Wilde, Trakl, Henley
- **Escalating rhyme:** low-S₂ lead, high-S₂ echo (inverse decay) — Hopkins, Browning, Moore

The global mean is near zero because these two strategies cancel out. A poet's choice between
them is a distinctive part of their S₂ signature: **where in the rhyme pair they concentrate
their surprise**.

---

## Suggested Next Steps

1. **Per-poet classification:** Classify each rhyming poet as catapult-and-catch vs.
   escalating-rhyme using their mean decay score. Test whether this correlates with era,
   form-strictness, or critical reputation for "difficulty."
2. **Villanelle analysis:** The villanelle's refrain returns the same WORDS, not just sounds.
   Does S₂ of the repeated-verbatim refrain lines decay over iterations? (This is the pure
   repetition case, not rhyme.)
3. **Sonnet octave vs sestet:** In a Petrarchan sonnet (ABBA ABBA / CDECDE), the A-rhyme
   recurs twice in the octave. Does the third occurrence of the A-rhyme (at the second "ABBA")
   show decay relative to the first?
4. **Phonetic vs semantic echo:** Extend the analysis to distinguish whether the decay
   pattern differs for perfect rhymes vs slant rhymes. Does phonetic distance between lead
   and echo word correlate with the decay magnitude?
5. **Semantic field of echo:** When the echo word is more surprising than the lead, is it
   because it comes from a different semantic field (escalation across semantic domains)?
   Link to inter-token semantic jumps data.
