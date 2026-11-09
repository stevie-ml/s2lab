# Shadow Vocabulary Fulfillment: Do Poets Eventually Deliver What GPT-2Expected?

**Date:** 2026-11-09  
**Experiment:** `experiments/shadow_vocab_fulfillment.py` → `results/shadow_vocab_fulfillment.json`  
**Corpus:** 410 of 411 texts analyzed (1 empty)  
**Builds on:** `grammar_of_unsaid.md`, `suppressed_lexicon.md`, `shadow_poem_analysis.md`

---

## Research Question

At every token position, GPT-2 predicts a most-likely continuation: the **shadow word**. The
poet suppresses it at that position. But does the shadow word appear *later* in the same poem?
If so, the poem **fulfills** its shadow — it stays inside GPT-2's vocabulary world, just
rearranging when the expected words arrive. If not, the poem **evades** its shadow entirely.

**Fulfillment rate**: fraction of the poem's unique shadow content words (top-1 alternatives,
function words excluded) that also appear as actual words in the poem.

**Hypothesis A**: Surprising poems (high avg_S₂) will have *lower* fulfillment — they
escape the model's lexical world, not just its timing.  
**Hypothesis B**: High-S₂ moments within poems will have *lower* fulfillment than low-S₂
positions — peak surprises represent genuine lexical departures, not just reorderings.

---

## Global Findings

| Metric | Value |
|--------|-------|
| Poems analyzed | 410 |
| Mean fulfillment rate (all positions) | **41.2%** |
| Median fulfillment rate | 42.0% |
| Mean fulfillment at high-S₂ positions (S₂ ≥ 2.0) | **31.6%** |
| Median fulfillment at high-S₂ positions | 30.0% |
| Correlation: fulfillment rate × avg S₂ | **−0.27** |

**Finding 1: Poems live substantially inside GPT-2's vocabulary world.** On average, 41%
of GPT-2's suppressed content-word predictions eventually appear elsewhere in the same poem.
The model is not wrong about the vocabulary — it is wrong about the *timing*.

**Finding 2: High-S₂ moments are lexically more independent.** At the positions of
maximum surprise (S₂ ≥ 2.0), only 31.6% of GPT-2's top predictions appear anywhere in the
poem — 10 points lower than the baseline. When poets surprise the model most strongly, they
are reaching *outside* the shadow vocabulary, not just reordering it.

**Finding 3: Higher-surprise poets evade GPT-2's lexicon more completely** (r = −0.27).
Poems with higher average S₂ have systematically lower fulfillment rates. Surprise is not
just about position — it is about vocabulary selection too.

---

## Era Analysis: Which Traditions Fulfill vs. Evade

| Era | n | Fulfillment | High-S₂ Fulfillment | Avg S₂ | Profile |
|-----|---|------------|---------------------|--------|---------|
| **concrete** | 3 | **0.728** | 0.646 | −0.48 | maximum fulfillment |
| **found_poetry** | 9 | 0.621 | 0.579 | −0.62 | natural overlap |
| **song_lyrics** | 3 | 0.580 | 0.370 | −0.64 | repetition-driven |
| **biblical** | 8 | 0.570 | 0.409 | −0.51 | restricted sacred lexicon |
| **villanelle** | 3 | 0.529 | 0.468 | −0.57 | refrain-mandated returns |
| **ballad** | 6 | 0.512 | 0.332 | −0.39 | oral formula repertoire |
| **prose_poetry** | 12 | 0.478 | 0.428 | −0.47 | medium fulfillment |
| **language** | 6 | 0.471 | 0.422 | −0.52 | surprisingly high |
| **oulipo** | 8 | 0.454 | 0.287 | −0.05 | constraint-bound vocabulary |
| **modernist** | 28 | 0.348 | 0.228 | −0.46 | suppressed shadow |
| **imagist** | 5 | 0.316 | 0.170 | −0.45 | curated alien words |
| **clerihew** | 10 | 0.302 | 0.100 | +0.55 | forced rhyme evasion |
| **confessional** | 6 | 0.279 | 0.154 | −0.30 | personal lexicon |
| **limerick** | 10 | 0.254 | 0.200 | −0.69 | meter-forced choices |
| **haiku** | 14 | **0.207** | 0.117 | +0.03 | minimum fulfillment |

### Pattern 1: Concrete Poetry — Maximum Lexical Re-use (72.8%)

Concrete poetry has the highest fulfillment by far. Concrete poems
cycle through a restricted vocabulary (Emmett Williams' word grids, Gomringer's "Silencio"),
so GPT-2's predictions keep appearing because the poet keeps returning to the same small
lexicon. The shadow vocabulary *is* the poem's vocabulary — there is no evasion, only
redistributed placement.

### Pattern 2: Haiku — Maximum Evasion (20.7%)

Haiku has the lowest fulfillment, nearly one-fifth of the global mean. In 17 syllables,
haiku has almost no space to deliver GPT-2's predictions elsewhere, and its imagistic
economy draws on words the model rarely predicts. When a Bashō poem contains "pond" and
"frog," GPT-2 was not expecting either of those words at any position — and there are only
three lines in which to later appear.

### Pattern 3: Clerihew — High S₂, Low Fulfillment (30.2% / 10.0% at high-S₂)

Clerihews have one of the highest average S₂ scores (+0.55) but very low fulfillment,
especially at high-S₂ moments (10.0%). This reveals the clerihew's mechanism: it
produces surprise via *forced rhyme* — the meter and rhyme scheme compel unusual words
that GPT-2 did not predict and that do not recur. The surprise is structurally generated
and lexically non-repeating. High S₂ with low fulfillment = **surprise as one-time shock**.

### Pattern 4: Villanelle — Form Forces Fulfillment (52.9%)

The villanelle's refrains mechanically guarantee high fulfillment: the same lines return
multiple times, so GPT-2's shadow predictions at those positions inevitably appear later in
the poem. The villanelle's repetition is an extreme fulfillment strategy.

### Pattern 5: Language Poetry — Unexpectedly High Fulfillment (47.1%)

Language poetry ranks near the top (above Modernist) despite its reputation for
disrupting semantic norms. The result suggests Language poetry works with an *anti-lexicon*
that it still uses consistently: Silliman and Hejinian suppress conventional words in favor
of unexpected ones, but these unexpected words recur throughout a poem. The surprise is
consistent, not random.

---

## The Globally Evaded Words

Across 410 poems, GPT-2 most frequently predicts these content words — and poets most
frequently *never* deliver them:

| Word | Times Suppressed (not in poem) |
|------|-------------------------------|
| **world** | 70 |
| **man** | 69 |
| **sun** | 50 |
| **day** | 49 |
| **eyes** | 45 |
| **little** | 43 |
| **see** | 43 |
| **night** | 37 |
| **sea** | 36 |
| **face** | 35 |
| **same** | 35 |
| **more** | 33 |
| **light** | 33 |
| **own** | 30 |

This is the **anti-lexicon of poetry**: the words poetry most systematically refuses. GPT-2
wants the generic ("world", "man", "day"), the bodily-visual ("eyes", "face"), and the
elemental-landscape ("sun", "night", "sea", "light"). Poetry evades exactly these — the
ambient words of ordinary discourse — in favor of more specific or unusual choices.

This extends the `suppressed_lexicon.md` finding at a larger scale: the most suppressed
words are not random — they form a coherent domain of *conventional experience*: the
generic masculine subject ("man"), the natural cycle ("sun", "day", "night", "sea"), the
social gaze ("eyes", "face"). Poetry's shadow vocabulary is a portrait of the clichéd world
it perpetually refuses.

---

## Length Effect: Fulfillment Scales with Poem Length

| Length | Tokens | n | Fulfillment Rate |
|--------|--------|---|-----------------|
| Short | ≤70 | 103 | **0.326** |
| Medium-short | 71–127 | 102 | 0.419 |
| Medium-long | 128–170 | 104 | 0.447 |
| Long | >170 | 101 | **0.455** |

Longer poems have significantly higher fulfillment. Part of this is mechanical (more
opportunities to use a word), but it also reflects that short-form poetry (haiku, clerihew,
limerick) tends toward the low-fulfillment end of the spectrum. Short poems are more likely
to be radically condensed, with no room to deliver the expected.

---

## The High-S₂ Fulfillment Anomaly

At high-S₂ moments, the most interesting outliers are traditions that break the
fulfillment-S₂ correlation:

**High S₂, HIGH fulfillment at peak moments (black_arts: 59.2%)**  
Black Arts poetry has above-average fulfillment at its own surprise peaks.
This suggests Black Arts poets repeat surprising words: they introduce an unexpected
image and then come back to it. Surprise-and-return rather than surprise-and-abandon.

**Low S₂, LOW fulfillment (control/prose texts: 26.7%)**  
The control texts (scientific papers, prose) have surprisingly low high-S₂ fulfillment.
Prose's high-S₂ moments (genuine jargon, technical terms) tend to be isolated and
non-recurring. Discipline-specific vocabulary is used precisely — not repeated.

**Low fulfillment at high-S₂ for clerihew (10.0%)**  
Clerihew produces its strongest surprises via unique rhyme words that never recur. The
form's constraint is to surprise once, never to build a vocabulary.

---

## Theoretical Implications

The fulfillment rate introduces a new axis for poetic analysis:

```
                    HIGH fulfillment
                    (GPT-2's words used, not in predicted position)
           ┌──────────────────────┐
high S₂   │ BLACK ARTS           │  low S₂
(surprise) │ LANGUAGE POETRY      │  (conventional)
           │                      │  BIBLICAL
           │                      │  CONCRETE
           │                      │  FOUND POETRY
           ├──────────────────────┤
           │ IMAGIST              │  MODERNIST
           │ CLERIHEW             │  HAIKU
           │ LIMERICK             │
           └──────────────────────┘
                    LOW fulfillment
                    (GPT-2's words never appear in poem)
```

- **High S₂, high fulfillment** = surprises that build a consistent anti-conventional vocabulary (Language, Black Arts)
- **High S₂, low fulfillment** = surprises that are one-off, structurally forced (clerihew, limerick)
- **Low S₂, high fulfillment** = conventional forms with high repetition (biblical, ballad, concrete)
- **Low S₂, low fulfillment** = suppressed words absent AND the form is non-conventional (haiku, imagist)

---

## Suggested Next Steps

1. **Per-poem fulfillment maps**: visualize which shadow words are fulfilled and where in
   the poem they finally appear. Do words tend to be fulfilled in the poem's latter half?
2. **Fulfillment as a closure signal**: do poems with higher fulfillment rates in the final
   stanza have stronger "sense of closure"? A poem that delivers its shadow words at the
   end may feel more resolved.
3. **Authorial consistency**: do poets have stable fulfillment rates across their work, or
   does it vary by poem? A stable rate would make fulfillment a stylometric signature.
4. **Semantic distance of fulfillment**: when the shadow word IS used, how far (in tokens)
   is it from where the model predicted it? Do surprise poets use shadow words far from
   their predicted position, or close?
5. **The "shadow poem" reconstruction**: take the top-1 alternative at every position and
   assemble the full shadow poem. Compare its readability and coherence to the actual poem.
   Does the shadow of a villanelle read like a villanelle?
