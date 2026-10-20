# The Form Constraint Spectrum: Double Dactyl and the Bottom of Poetic S₂

**Date:** 2026-10-20  
**Experiment:** `experiments/double_dactyl_spectrum.py`  
**New poems added:** 5 double dactyls + 3 clerihews (316 poems total)  
**Builds on:** `limerick_internal_s2.md`, `new_era_profiles_20261012.md`, `formal_meter_vs_s2.md`

---

## Research Question

The double dactyl (Anthony Hecht and John Hollander, 1966) is arguably the most formally
constrained short poem in English:

1. **Line 1**: Nonsense reduplication phrase ("Higgledy-piggledy")
2. **Line 2**: Person's name (6 syllables, dactylic dimeter)
3. **Lines 3, 5, 6**: Content in dactylic dimeter (DUM-da-da DUM-da-da, 6 syl each)
4. **Lines 4, 8**: Catalectic dimeter (DUM-da-da DUM, 4 syl); must rhyme with each other
5. **Line 7**: A **single polysyllabic word** (6 syllables)

Can a form this constrained extend the constraint spectrum below the limerick?

---

## Finding 1: The Spectrum Confirmed and Extended

| Form | n poems | AF mean S₂ | Pos% |
|------|---------|-----------|------|
| **double_dactyl** | **5** | **−0.955** | **31.0%** |
| limerick | 10 | −0.661 | 30.0% |
| fixed_form | 8 | −0.560 | 31.7% |
| metaphysical | 4 | −0.648 | 35.6% |
| found_poetry | 7 | −0.614 | 26.8% |
| romantic | 16 | −0.438 | 34.7% |
| prose_poetry | 12 | −0.471 | 32.2% |
| **clerihew** | **5** | **+0.353** | **40.3%** |
| control prose | 5 | −1.721 | 20.2% |

**Double dactyls have the lowest mean artifact-free S₂ of any non-prose form** (−0.955),
extending the constraint spectrum below the limerick (−0.661). The complete constraint
gradient is now:

```
control prose     −1.72
double dactyl     −0.96  ← new, extremal
cliché control    −0.87
limerick          −0.66
fixed form        −0.56
other poetry      −0.2 to −0.5
beat/german       +0.1 to +0.6
prose control     −1.72
```

The triple constraint of the double dactyl — dactylic dimeter meter, required proper
name in line 2, mandatory single-word line 7 — reduces the Straussian gap beyond
what the AABBA limerick achieves. GPT-2 "learns" the form's pattern and assigns
increasingly confident predictions at each position.

---

## Finding 2: The Clerihew Paradox — Meter Removed, S₂ Explodes

The most striking result is the clerihew: **+0.353 mean AF S₂**, higher than romantic,
Victorian, prose poetry, and found poetry. Despite being a short humorous biographical
form superficially similar to the limerick, it achieves S₂ levels comparable to modernist
verse.

| Clerihew | AF S₂ | Raw S₂ | Driver |
|----------|-------|--------|--------|
| Sir Humphrey Davy | +1.113 | +2.306 | "Abominated gravy," rare Latin ("odium") |
| William Topaz McGonagall | +1.158 | +1.988 | Unexpected proper nouns, awkward juxtapositions |
| Oscar Wilde | +0.570 | +1.883 | "Epigrams to fill the gallery" — unexpected verb phrase |
| Charlotte Mew | +0.074 | +1.070 | Known title quote, moderate surprise |
| The Art of Biography | −1.035 | −0.440 | Pure logical parallelism — GPT-2 predicts each step |

The clerihew's enormous variance (+1.16 to −1.04) reveals the **content law**:
without metrical constraint, short humorous poems spike S₂ when they use technical
vocabulary, unusual proper nouns, or unexpected verb phrases — and collapse when
they use logical parallelism or conventional phrasing.

**Meter is the force that suppresses S₂ in limericks**, not humor, length, or
the biographical subject matter. Remove the meter, and S₂ is free to spike wherever
the poet's lexical choices take it.

---

## Finding 3: The Double Dactyl's Internal Line Structure

Mapping tokens to the 8-line structure (pooled across all 5 poems):

| Line | Role | n tokens | AF Mean S₂ | Pos% |
|------|------|----------|-----------|------|
| 1 | Nonsense phrase | (filtered) | see below | — |
| **2** | **Person's name** | **50** | **−1.636** | **20.0%** |
| 3 | Content | 30 | −1.376 | 26.7% |
| **4** | **Rhyme A (catalectic)** | **37** | **+0.007** | **40.5%** |
| 5 | Content | 35 | −1.415 | 25.7% |
| 6 | Content | 32 | −0.191 | 40.6% |
| 7 | Single long word | 26 | −0.716 | 34.6% |
| 8 | Rhyme A (catalectic) | 19 | −0.881 | 36.8% |

**The most conformist position is the person's name (line 2, mean = −1.636).**
After "Higgledy-piggledy," GPT-2 strongly predicts common words (or the comma/newline),
and the proper name is at most modestly surprising. Famous people are especially
well-predicted because GPT-2 has biographical knowledge about them — "Emily Dickinson"
after the nonsense opening is something GPT-2 can model.

**The most deviant positions are lines 4 and 6** (mean ≈ 0.00 and −0.19), where:
- Line 4 is the catalectic close of the first stanza — a position where the rhyme word
  needs to end on a stressed syllable but *also* make semantic sense
- Line 6 contains the setup for the single-word line 7, and often contains more
  unexpected content phrases

**Line 7 (the single polysyllabic word)** is moderately deviant (−0.716). The long
technical words ("Unconventionally," "Theologically," "Philosophically," "Experientially,"
"Uncompromisingly") are recognizable to GPT-2 as plausible long adverbs — they're not
highly surprising in isolation, but they're harder to predict in the specific poem context.

---

## Finding 4: The Nonsense Phrase Does Not Spike

"Higgledy-piggledy," the form's canonical nonsense opener, produces mean AF S₂ ≈ −1.44
for its subword tokens:

| Token | S₂ | GPT-2 expected |
|-------|-----|----------------|
| 'igg' | +2.18 | '.' (period, punctuation) |
| 'led' | −1.23 | 'ling' |
| 'y' | +1.95 | ' at' |
| '-' | −4.22 | ',' |
| 'p' | −2.27 | 'eyed' |
| 'igg' | −3.34 | 'ink' |
| 'led' | −2.40 | 'led' |
| 'y' | −2.21 | 'y' |

The nonsense phrase does NOT create a massive S₂ spike. GPT-2's BPE tokenizer
splits "Higgledy-piggledy" into short common subword tokens, each somewhat
predictable from prior context. GPT-2 has no model for "nonsense" — it cannot
distinguish "Higgledy" from an unusual proper noun or brand name. The compound
word is processed as a sequence of phonetic subunits, each moderately plausible.

This null result is theoretically important: **S₂ cannot detect semantic nonsense**.
It can detect statistical deviation from learned patterns, but if the surface form
of the nonsense word (its subword sequence) happens to be statistically plausible,
S₂ remains low despite the semantic emptiness.

---

## Per-Poem Variation in Double Dactyls

| Poem | AF S₂ | Raw S₂ | Note |
|------|-------|--------|------|
| Alfred Lord Tennyson (DD) | −1.381 | +0.639 | Formal, conventional content words |
| Emily Dickinson (DD) | −1.174 | +0.955 | Smooth despite unusual subject |
| Lawrence Ferlinghetti (DD) | −1.161 | +1.123 | "Beat-era polemics" is predictable |
| William Carlos Williams (DD) | −0.735 | +1.696 | "Concrete, particular" adds deviation |
| **Gerard Manley Hopkins (DD)** | **−0.297** | **+1.652** | "Tortured but beautiful," "Theologically" |

The Hopkins double dactyl is the highest-S₂ of the five (−0.297), due to:
- "Tortured but beautiful" — an unexpected contrastive construction
- "Theologically" — a 6-syllable technical adverb that GPT-2 doesn't predict
  in this "strangely anguished" context

Even within the double dactyl's extreme constraints, poets can express their
stylistic identities: a poem *about* Hopkins achieves higher S₂ than a poem
about Tennyson, mirroring the living poets' own S₂ profiles.

---

## The Complete Constraint Spectrum

From the combined data across all form experiments:

```
Form              | AF Mean S₂ | Key constraint
------------------|-----------|----------------
double dactyl     |   −0.955  | meter + name + single long word
cliché control    |   −0.870  | predictable phrasing (baseline)
limerick          |   −0.661  | AABBA + anapestic meter
fixed form        |   −0.560  | rhyme scheme (sonnet, villanelle)
found poetry      |   −0.614  | no constraint (bureaucratic prose)
romantic          |   −0.438  | iambic convention
prose poetry      |   −0.471  | prose rhythm
modernist         |   −0.340  | free verse
beat / german     |   +0.1 to +0.6 | anaphora / self-imposed structure
clerihew          |   +0.353  | no meter (humor + rare vocabulary)
control prose     |   −1.721  | none (baseline)
```

The surprise of this spectrum: the two most constrained forms (double dactyl and
limerick) occupy the lowest S₂ *within poetry*, while the *unmetered* clerihew
rivals modernist and Beat poetry for the highest. **Formal metric constraint is the
primary suppressor of S₂ in short poems** — more powerful than era, subject, or
even deliberate vocabulary choice.

---

## Summary of Findings

1. **Double dactyls extend the constraint spectrum** (AF = −0.955 < limerick's −0.661),
   confirming that greater formal constraint → lower S₂.

2. **The clerihew paradox**: removing meter from a humorous short form raises S₂ from
   −0.661 to +0.353 — a 1.0-bit swing — driven by freedom to use unusual vocabulary.

3. **Within double dactyls, the name line (line 2) is the most conformist** (−1.636),
   while the catalectic rhyme lines (4 and 6) are the least conformist.

4. **The nonsense phrase "Higgledy-piggledy" does not spike S₂**: GPT-2 cannot
   distinguish nonsense words from rare proper nouns, so the form's defining element
   is informationally invisible.

5. **Form imprints S₂ more powerfully than content**: even poems *about* highly
   deviant poets (Hopkins, Williams) produce low S₂ when constrained by the double
   dactyl form. The constraint overwhelms the stylistic subject matter.

---

## Suggested Next Steps

1. **Add more double dactyls** (n=10+) for statistical robustness — the current n=5
   is sufficient for pattern identification but not for fine-grained per-line analysis.

2. **Metrically stressed vs. unstressed positions**: For the double dactyl's dactylic
   dimeter (DUM-da-da DUM-da-da), do stressed syllables have higher S₂ than
   unstressed? This would directly test whether metrical stress and informational
   stress coincide.

3. **Real vs. synthetic double dactyls**: Compare S₂ profiles of the synthetic
   (research-composed) double dactyls here against published literary double dactyls
   (Hecht, Hollander, J.V. Cunningham). Do published examples have lower S₂ overall,
   or do their more polished rhymes raise it?

4. **The auto-detection test**: Can we reliably distinguish double dactyls from
   limericks by S₂ profile alone (without metadata)? If S₂ is truly lower on
   average for double dactyls, a classifier might work.
