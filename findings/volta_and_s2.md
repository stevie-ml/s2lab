# The Volta and S₂: Where Does Surprise Live in a Sonnet?

**Date:** 2026-09-11
**Experiment:** `experiments/volta_experiment.py`
**Corpus additions:** 7 sonnets added (Shakespeare ×3, Milton, Keats, Shelley, Millay), total sonnet sample n=10
**Builds on:** `line_position_analysis.md`, `stanza_boundary_effects.md`

---

## Research Question

The **volta** (Italian: "turn") is the defining structural feature of the sonnet tradition. In Petrarchan sonnets, it falls between the octave (lines 1–8) and sestet (lines 9–14); in Shakespearean sonnets, the primary turn precedes the final couplet (lines 13–14).

If S₂ captures genuine poetic structure, the volta should be detectable as an information-theoretic event: the model, conditioned on the poem's opening argument, predicts a continuation — but the poet pivots, and the mismatch shows up as elevated S₂.

**The hypothesis**: volta lines have higher mean S₂ than the surrounding body.

---

## Method

- **Sample**: 10 sonnets (3 Petrarchan, 3 Shakespearean, 1 irregular, 3 unannotated)
- Sonnets analyzed token-by-token with GPT-2
- Tokens assigned to lines using character-offset mapping
- **Zones defined**:
  - Petrarchan: octave = lines 1–8, **volta = line 9**, sestet = lines 10–14
  - Shakespearean: quatrains = lines 1–12, **volta = lines 13–14**
  - Irregular (Ozymandias): volta = lines 9–10 (thematic turn)
- **Volta lift** = volta zone mean S₂ − body zone mean S₂

---

## Results

### Shakespearean Sonnets (volta at lines 13–14)

| Title | Body S₂ | Volta S₂ | Lift |
|-------|---------|---------|------|
| Sonnet 18 (Shall I compare thee) | -0.233 | -1.724 | **-1.492** |
| Sonnet 73 (That time of year) | -0.763 | -0.147 | **+0.616** |
| Sonnet 130 (My mistress' eyes) | -0.882 | +0.292 | **+1.174** |

**Mean volta lift: +0.099** — very weak positive signal overall, driven by two sonnets showing genuine couplet elevation.

### Petrarchan Sonnets (volta at line 9)

| Title | Body S₂ | Volta S₂ | Lift |
|-------|---------|---------|------|
| On His Blindness (Milton) | +0.172 | -0.132 | **-0.303** |
| On First Looking into Chapman's Homer (Keats) | +0.179 | -0.986 | **-1.165** |
| What lips my lips have kissed (Millay) | -0.654 | -0.918 | **-0.264** |

**Mean volta lift: -0.578** — consistently negative: line 9 has LOWER S₂ than the octave.

### Irregular (Ozymandias — Shelley)

| Title | Body S₂ | Volta S₂ | Lift |
|-------|---------|---------|------|
| Ozymandias | +0.386 | -1.344 | **-1.730** |

---

## Key Findings

### 1. The volta hypothesis is mostly *wrong* — and the failure is instructive

Line 9 is *not* where surprise peaks in Petrarchan sonnets. Instead, the octave itself carries the higher S₂ values. The sestet (including the volta line) tends to be more predictable.

**Why?** The octave is where poets introduce their central argument — often via surprising images, unexpected comparisons, or unusual diction. The sestet resolves, applies, or meditates on that argument, and resolution tends toward syntactically expected language.

GPT-2 can "handle" the sestet's syntax more easily than the octave's boldness. The model is not wrong in the way the poet needs to be wrong at the resolution.

### 2. Shakespearean sonnets show a weak positive volta signal

2 of 3 Shakespearean sonnets have higher S₂ at the couplet than in the preceding 12 lines:

- **Sonnet 130, line 14**: S₂ = **+2.315** — "As any she belied with false compare" is the highest-S₂ couplet line in the sample. This is Shakespeare's anti-blazon reversal: 12 lines of mock-deprecation pivot to genuine love, and the ironic surprise is real at the information-theoretic level.
- **Sonnet 73, line 14**: S₂ = **+0.211** — "To love that well which thou must leave ere long." The pivot to direct address after three quatrains of metaphorical distance registers as mildly elevated.

The shorter volta zone (2 lines vs. 6 in Petrarchan) forces higher compression; more surprise-per-token in less space.

### 3. The Keats volta puzzle

"On First Looking into Chapman's Homer" contains arguably the most celebrated volta in English:

> *Then felt I like some watcher of the skies / When a new planet swims into his ken*

Yet its S₂ at line 9 is **-0.986** — quite low. This is a beautiful failure of the hypothesis: the Keats volta works by introducing a *more accessible* simile. "Then felt I like" is syntactically predictable from "Then" after eight lines of first-person exploration. The surprise is conceptual (the astronomy metaphor, the geographical specificity of Darien) but not token-level.

**Implication**: S₂ cannot detect all aesthetic pivots, only those executed through statistically unexpected tokens. Conceptual surprise that uses expected syntax is invisible to GPT-2.

### 4. The octave carries the Straussian weight

Across all sonnet types, mean octave S₂ exceeds mean sestet S₂:

| Zone | Mean S₂ (Petrarchan, n=3) |
|------|--------------------------|
| Octave (lines 1–8) | +0.043 |
| Sestet (lines 9–14) | -0.554 |

This suggests the octave is where poets take the greatest *token-level* risks — unusual diction, unexpected images, syntactic inversions. The sestet lands. The risk-reward structure of the sonnet is front-loaded.

### 5. Line-by-line S₂ profiles reveal individual volta signatures

**Sonnet 130 line-by-line S₂** (selected to show the couplet spike):

| Line | Mean S₂ | Zone |
|------|---------|------|
| 1 | +1.724 | quatrains (bold opening) |
| 2 | -1.684 | quatrains |
| 13 | -0.954 | VOLTA |
| **14** | **+2.315** | **VOLTA** ← highest in poem |

The final line's spike reflects the sheer unexpectedness of the sincere reversal after 12 lines of mock-deprecation.

**Sonnet 73 opens with the corpus's highest single-line S₂**:
- Line 1: S₂ = **+3.005** — "That time of year thou mayst in me behold" is maximally unexpected from a standing start.

---

## Hypothesis Revision

The volta hypothesis needs reformulation:

> **Original**: *S₂ spikes at the volta.*
> **Revised**: *S₂ patterns distinguish sonnet type. Petrarchan voltas do not show S₂ elevation; Shakespearean couplet-voltas show weak elevation (mean +0.10), especially when the couplet executes an ironic reversal.*

A more productive question: **which sonnet feature does S₂ actually track?** The data suggest:
- S₂ is highest at unexpected *openings* (line 1 of Sonnet 73: +3.005)
- S₂ is highest at ironic *reversals* using unexpected vocabulary (Sonnet 130, line 14: +2.315)
- S₂ is NOT high at syntactically conventional pivots (Keats's "Then felt I like": -0.986)

---

## Suggested Next Steps

1. **Larger sonnet sample**: Add 20+ sonnets to improve statistical power and test Shakespearean volta hypothesis properly (current n=3 is marginal).

2. **Separate syntactic from semantic surprise**: Can we detect cases where conceptual surprise is high but token S₂ is low? (Keats volta is the paradigm case.)

3. **Spenserian sonnet test**: The Spenserian form (ABAB BCBC CDCD EE) has a more gradual turn structure — does S₂ reflect the linked rhymes?

4. **Within-octave structure**: Given that the octave carries the highest S₂, does S₂ peak at the opening (fresh start) or build through the octave?

5. **Couplet irony detection**: Can the combination of low S₂ in lines 1–12 followed by high S₂ in lines 13–14 serve as a statistical signature of ironic reversal?
