# The S₂ Arc: How Poets Budget Surprise Across the Poem

**Date:** 2026-10-24  
**Experiment:** `experiments/s2_arc_within_poem.py`  
**Results:** `results/s2_arc_within_poem.json`  
**Corpus:** 244 English-language poems (≥60 clean tokens), 84 skipped  
**Builds on:** `rupture_pivot_poet_profiles.md`, `entropy_trajectory_analysis.md`

---

## Research Question

The Rupture-Pivot framework established that poets differ in *how* they use surprise: ruptures (high-S₂ in confident contexts → entropy expands) vs. pivots (high-S₂ in uncertain contexts → entropy contracts). But do individual poets use these mechanisms uniformly *throughout* a poem, or does the balance shift as the poem progresses?

More broadly: do poems have a characteristic **S₂ arc** — a pattern of front-loading or back-loading their information-theoretic departures?

---

## Method

For each poem (≥60 artifact-cleaned tokens):
1. Remove stanza-break artifact positions (p_newline ≥ 0.9)
2. Divide remaining tokens into four quartiles (Q1=beginning, Q4=end)
3. Per quartile: mean S₂, mean entropy, positive-S₂ fraction, RP index

**S₂ arc** = Q4 mean S₂ − Q1 mean S₂ (negative = front-loaded, positive = back-loaded)

---

## Main Finding: Poems Are Systematically Front-Loaded

### Global Quartile Profiles

| Quartile | Mean S₂ | Mean H | Pos-S₂% | RP Index |
|----------|---------|--------|---------|---------|
| Q1 (beginning) | **−0.140** | 6.697 | 38.7% | **+6.69** |
| Q2 (early-mid) | −0.431 | 6.235 | 34.0% | +6.65 |
| Q3 (late-mid) | −0.553 | 6.072 | 32.3% | +6.29 |
| Q4 (end) | −0.546 | 6.031 | 31.8% | **+6.01** |

Three simultaneous gradients, all declining from Q1 to Q4:
- **S₂ declines** by 0.41 bits (poems become more conformist as they close)
- **Entropy declines** by 0.67 bits (the model grows more confident as context accumulates)
- **RP index declines** by 0.68 units (early surprises are more liberation-dominant; late surprises are more anchoring-dominant)

### Arc Distribution (244 poems)

| Direction | Definition | Count |
|-----------|-----------|-------|
| **Front-loaded** | Q4 < Q1 (arc < 0) | **67.6%** (165 poems) |
| Back-loaded | Q4 > Q1 (arc > 0) | 32.4% (79 poems) |
| Flat | \|arc\| < 0.3 | 21.3% (52 poems) |

**Mean arc: −0.41 bits; median: −0.39 bits.**  
Front-loading is the default mode of English-language poetry: two in three poems spend their highest S₂ currency in the opening quarter.

---

## Era-Level Arc Profiles

| Era | Q1 S₂ | Q2 S₂ | Q3 S₂ | Q4 S₂ | **Arc** | n |
|-----|--------|--------|--------|--------|---------|---|
| 19th_century | +0.46 | −0.47 | −0.49 | −0.75 | **−1.21** | 9 |
| new_york_school | +0.13 | −0.50 | −0.97 | −0.89 | **−1.02** | 16 |
| contemporary | +0.23 | −0.10 | −0.63 | −0.72 | **−0.95** | 6 |
| ballad | +0.21 | −0.35 | −0.70 | −0.70 | **−0.91** | 6 |
| harlem_renaissance | +0.04 | −0.54 | −0.52 | −0.84 | **−0.88** | 6 |
| elegy | +0.16 | −0.51 | −0.58 | −0.66 | **−0.82** | 7 |
| *(mid-range omitted)* | | | | | | |
| found_poetry | −0.71 | −0.61 | −0.56 | −0.59 | **+0.12** | 7 |
| prose_poetry | −0.48 | −0.53 | −0.61 | −0.30 | **+0.18** | 11 |
| beat | −0.15 | −0.05 | +0.74 | +0.04 | **+0.20** | 5 |

### Interpretation

**Most front-loaded**: The 19th century (-1.21) and New York School (-1.02) open with the highest S₂ and rapidly conform thereafter. 19th-century poetry often opens with its most striking image or declaration, then elaborates within established register. The New York School's conversational opening gambits are informationally adventurous before settling into catalog or narrative.

**Least front-loaded / back-loaded**: Beat poetry (+0.20), prose poetry (+0.18), and found poetry (+0.12) resist the front-loading pattern. Beat poems build toward their most deviant moments; found poetry — by appropriating existing text — starts low and may accumulate strangeness as context locks in.

---

## Extreme Poems

### Most Front-Loaded (S₂ Collapses from Beginning to End)

| Arc | Author | Title |
|-----|--------|-------|
| −3.22 | Wallace Stevens | The Emperor of Ice-Cream |
| −3.18 | Anne Carson | The Glass Essay (opening) |
| −3.01 | Walt Whitman | O Captain! My Captain! |
| −2.74 | Traditional (Scottish) | Bonnie George Campbell |
| −2.71 | John Ashbery | Wet Casements |
| −2.68 | Frank O'Hara | The Day Lady Died |

**"Emperor of Ice-Cream"** is the canonical example: Stevens opens with maximally unexpected diction ("concupiscent curds"), then consolidates into the repeated, metrically controlled refrain — an archetypal front-loaded poetic structure.

### Most Back-Loaded (S₂ Builds Toward the End)

| Arc | Author | Title |
|-----|--------|-------|
| +3.06 | Carolyn Forché | The Colonel (excerpt) |
| +2.40 | Lawrence Ferlinghetti | In Goya's greatest scenes |
| +1.87 | Frank O'Hara | Why I Am Not a Painter |
| +1.76 | Matthew Arnold | Dover Beach (closing stanzas) |
| +1.67 | Sylvia Plath | Daddy (opening) |
| +1.59 | W.B. Yeats | Sailing to Byzantium (stanza 1) |

**"The Colonel"** (Forché's prose poem) is back-loaded by design: it opens with ordinary domestic detail, then escalates to the bag of human ears — the high-S₂ horror concentrated at the end. The information-theoretic arc mirrors the rhetorical strategy exactly.

---

## The Declining RP Index Across Quartiles

The RP index (rupture score − pivot score) declines monotonically from Q1 (6.69) to Q4 (6.01). This means:

- **Early in poems**: high-S₂ events in confident contexts (ruptures) produce larger entropy expansions — the poet is more aggressively liberating when the model is most certain. These opening departures break from predictable tracks.
- **Late in poems**: the RP index contracts, meaning the rupture advantage over pivots shrinks. Surprising choices in uncertain contexts (pivots) become relatively more important near a poem's end — these anchor and constrain what follows, contributing to closure.

The **information-theoretic grammar of poetic closure** may be: spend ruptures early (to establish the poem's world), spend pivots late (to close down the possibility space).

---

## Theoretical Implications

**1. The Poem as Information Budget**  
Poems are not uniformly deviant from predictable language — they systematically concentrate deviation at the opening. This is an information budget with preferential spending in Q1.

**2. The Entropy Arc Parallels the S₂ Arc**  
The 0.67-bit entropy decline from Q1 to Q4 means the model's own uncertainty decreases as the poem's context accumulates. Poets exploit this: they make surprising choices when the model is still uncertain (Q1), and their choices ALSO become less surprising (lower S₂) as the poem's established register constrains expectations.

**3. Front-Loading Correlates with Genre**  
The front-loading effect is strongest for genres with dramatic opening conventions (19th-century odes, ballads) and weakest for processual, anti-climactic forms (found poetry, prose poetry, beat poetry). This suggests S₂ arc is a generic signature, not just an individual choice.

**4. RP Index as Temporal Process**  
The monotonic decline in RP index across quartiles suggests a poem's "surprise type" shifts: liberation dominates early, anchoring dominates late. This may be the information-theoretic correlate of the classic literary pattern of complication → resolution.

---

## Next Steps

- Extend to within-stanza analysis: does the front-loading repeat at the stanza level?
- Test whether the S₂ arc correlates with reader ratings of "closure" or "satisfaction"
- Check whether front-loading is a recent historical trend or consistent across eras
- Build a per-poet arc signature (some poets may systematically prefer back-loading)
- Model the RP decay across quartiles: is it linear or step-function at the Q3→Q4 boundary?
