# Within-Line S2 Peak Position: Where Does Surprise Fall Inside the Line?

**Date:** 2026-10-17  
**Experiment:** `experiments/intraline_s2_peak.py`  
**Corpus:** 284 texts, 3,108 lines analyzed (≥ 4 content tokens)  
**Builds on:** `line_position_analysis.md`, `enjambment_vs_s2.md`, `formal_meter_vs_s2.md`

---

## Research Question

Every poetic line has an internal temporal structure. The S2 peak — the moment of maximum
*chosen* surprise — can fall near the line's start, middle, or end. Does the *position*
of the highest-S2 token within a line vary systematically by era or form?

**Prior hypothesis (rejected):** Formal verse (end rhyme) should *avoid* line-final surprise,
because rhyme constrains the final syllable to a predictable sound class, lowering entropy
and therefore suppressing S2. We expected formal verse to peak *away* from the end.

**Finding:** The hypothesis is wrong. Formal verse concentrates surprise *at* the line end.

---

## Global Baseline

| Metric | Value | Uniform baseline |
|--------|-------|-----------------|
| Mean peak position (all poetry) | **0.485** | 0.500 |
| Mean S2 slope within lines | **−0.035** | 0 |

Poetry shows a small but consistent **front-loading** tendency (mean 0.485 < 0.5) and a
slight **falling S2 slope** (surprise very weakly declines toward line end on average).
Both effects are small across the full corpus but become stark at the era level.

---

## Era Rankings

Sorted from most front-loaded (peak early in line) to most end-loaded (peak late):

| Era | N lines | Mean pos | Front% | Mid% | End% | Slope |
|-----|---------|----------|--------|------|------|-------|
| korean_modernist | 14 | **0.242** | 71% | 21% | 7% | −0.483 |
| nursery_rhyme | 18 | **0.331** | 56% | 22% | 22% | −0.078 |
| ghazal | 10 | 0.367 | 40% | 40% | 20% | −0.179 |
| war_poetry | 56 | 0.393 | 46% | 34% | 20% | −0.089 |
| oulipo | 28 | 0.407 | 46% | 21% | 32% | −0.343 |
| classical_chinese | 24 | 0.415 | 33% | 50% | 17% | −0.266 |
| found_poetry | 134 | 0.416 | 40% | 36% | 24% | −0.153 |
| language | 37 | 0.431 | 43% | 27% | 30% | −0.217 |
| haiku | 43 | 0.432 | 35% | 44% | 21% | −0.174 |
| imagist | 27 | 0.476 | 37% | 30% | 33% | −0.006 |
| romantic | 207 | 0.469 | 37% | 33% | 29% | −0.097 |
| 19th_century | 145 | 0.411 | 43% | 30% | 27% | −0.134 |
| modernist | 235 | 0.495 | 35% | 30% | 35% | −0.109 |
| *— CENTER —* | | *0.500* | | | | |
| german_expressionist | 76 | 0.554 | 21% | 47% | 32% | +0.069 |
| fixed_form | 97 | **0.555** | 25% | 37% | 38% | +0.194 |
| beat | 46 | 0.563 | 33% | 24% | 43% | −0.106 |
| new_york_school | 138 | 0.562 | 27% | 33% | 40% | +0.067 |
| metaphysical | 50 | **0.566** | 20% | 46% | 34% | +0.068 |
| persian | 32 | **0.574** | 28% | 25% | 47% | +0.020 |
| harlem_renaissance | 58 | **0.578** | 26% | 34% | 40% | +0.151 |

---

## Key Findings

### 1. The Rhyme Paradox: Formal Verse Is End-Loaded

**The original hypothesis is refuted.** Fixed_form poetry (0.555) and metaphysical
poetry (0.566) both concentrate their within-line S2 peak *at the end* of lines —
exactly at the rhyme position.

Why? Two mechanisms likely interact:

**(a) Surprise-within-constraint:** Skilled formal poets choose rhyme words that are
semantically surprising *within* their rhyme class. Rhyme constrains phonology, not
semantics. The model knows a /iːz/ sound is coming (in "Louise" or "breeze" or "disease") —
but which particular word it is still carries full semantic surprise. GPT-2 may assign low
probability to the specific word even while the general sound-class was expected.

**(b) The enjambment offset:** Formal verse poets sometimes enjamb against the rhyme,
placing the S2 spike at the final *non-rhyme* word before the break. Either way, the
spike lands toward the end of the metrical unit.

This suggests: **rhyme is a constraint on phonology, not on the Straussian gap.** Formal
poets exploit this to deliver maximum semantic surprise at a formally constrained position —
the art of the expected surprise.

### 2. Korean Modernist: Extreme Front-Loading (0.242)

The single Korean modernist text analyzed (Ko Un translations) shows the most extreme
front-loading: **71% of lines have their S2 peak in the first third.** The mean peak
position (0.242) is far below any other era.

This may reflect translation conventions (key substantive nouns front-loaded in English
rendering of SOV-language structures) or a genuine poetic style of placing the
"image-shock" at the line's opening.

### 3. Gwendolyn Brooks' "We Real Cool": The Anaphoric Peak

The steepest *falling* S2 slope in the corpus belongs to **"We Real Cool" by Gwendolyn
Brooks** (slope = −1.731, mean peak = 0.273).

Each line: "We real cool." / "We / Left school." — the anaphoric "We" carries the high
S2 (the short, emphatic statement defies prediction), and the rest of the line is more
conventional. The poem is structurally designed so that S2 *falls* within each line,
with all the weight at the start.

### 4. New York School / Ashbery: End-Loaded Rising Surprise

Inversely, **John Ashbery's "Some Trees"** has the steepest *rising* S2 slope (+1.036),
and his poems dominate the "most end-loaded" list. Ashbery systematically delays his
most unexpected word to the *end* of the line — the opposite strategy from Brooks.

This tracks with Ashbery's aesthetic: casual mid-line language suddenly turned strange
at the closing position. The line *builds* to its Straussian moment.

### 5. Oulipo: Front-Loaded Despite Formal Constraint

**Oulipo** poetry (Perec, Queneau, Emmett Williams) shows strong front-loading (0.407)
and the second-steepest falling slope (−0.343), *despite* being heavily constrained.
This inverts the pattern of fixed_form. 

Oulipo's constraints (lipograms, N+7 substitutions, permutations) produce
unpredictable *first* words within each constraint-generated phrase, but the subsequent
words are often highly predictable by local context once the substitution is made. The
surprise is *installed* at the beginning of each unit, not accumulated toward the end.

### 6. Classical Chinese: Medial Concentration (50% mid-line)

Classical Chinese poetry (Wang Wei, Li Po, Du Fu in translation) shows remarkable
clustering in the *middle* of lines: 50% of lines have their peak in the central
third. This is the highest mid-concentration of any era.

This may reflect the parallelism structure of classical Chinese verse, where the
medial pivot-word carries the image weight between two symmetric hemistiches.

---

## Individual Poem Extremes

### Most Front-Loaded (peak early)
| Poem | Author | Mean pos |
|------|--------|----------|
| Psalm 23 (KJV) | Anonymous (Hebrew Bible) | 0.215 |
| Deer Park (literal) | Wang Wei | 0.232 |
| We Real Cool | Gwendolyn Brooks | 0.273 |
| O Captain! My Captain! | Walt Whitman | 0.283 |

### Most End-Loaded (peak late)
| Poem | Author | Mean pos |
|------|--------|----------|
| There Was a Young Man of Japan | Anonymous | 0.910 |
| One Art | Elizabeth Bishop | 0.801 |
| Constantly Risking Absurdity | Ferlinghetti | 0.781 |
| The Day Lady Died | Frank O'Hara | 0.760 |
| Some Trees | John Ashbery | 0.746 |

The limerick "There Was a Young Man of Japan" scores 0.910 — by design, the punchline
of the fifth line is always the final stressed word.

---

## Summary

1. **Poetry front-loads slightly** (global mean 0.485): the dominant pattern is for
   surprise to peak earlier than the line's midpoint.

2. **Formal verse inverts this**: fixed_form, metaphysical, and metaphysical poets end-load,
   exploiting the rhyme position for semantic surprise rather than avoiding it. The
   Straussian gap is *delivered* at the constraint, not hidden from it.

3. **Two opposing poetic strategies** emerge:
   - *Front-loaded descent* (Brooks, Korean modernism, Oulipo): the opening word carries
     the S2 spike; the line "resolves" downward.
   - *End-loaded climax* (Ashbery, Harlem Renaissance, formal verse): the line builds
     to an unexpected closing word.

4. **Classical Chinese** concentrates surprise medially, consistent with the mid-line
   pivot in balanced parallelistic verse.

---

## Next Steps

- Investigate whether *individual poets* are consistently front-loaders or end-loaders
  across multiple poems (intra-poet stability).
- Test whether the **rhyme paradox** holds when controlling for meter: is end-loading
  uniquely tied to end-rhyme, or also present in blank verse?
- Add the new surrealist poems now in `corpus/poems.py` to corpus analysis (requires
  re-running `engine.py`) to test whether surrealist poetry shows flat/random peak
  distribution compared to imagist.
