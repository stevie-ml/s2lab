# Rereading Simulation: Does S₂ Survive a Second Reading?

**Date:** 2026-11-15  
**Experiment:** `experiments/rereading_simulation.py`  
**Results:** `results/rereading_simulation.json`

---

## Research Question

Is a poem's S₂ signature *robust* or *contingent*? Specifically: if GPT-2 has already seen a poem (the full text prepended as context), does it still find the poem deviant?

**Method:** For 40 poems, compare S₂ from two passes:
- **First reading**: cold context (standard analysis)
- **Second reading**: the full poem prepended as context, then re-analyzed

If surprisal and entropy both drop proportionally, S₂ stays constant. If surprisal drops faster than entropy (the model is now "surprised but expecting surprise"), S₂ falls. If entropy drops faster (the model overconfidently expects what it learned from the first reading), S₂ rises.

---

## Key Numbers

| Metric | First Reading | Second Reading | Δ |
|--------|--------------|----------------|---|
| Avg surprisal | ~6.1 bits | ~0.9 bits | **-5.2** |
| Avg entropy | ~6.0 bits | ~0.8 bits | **-5.1** |
| Avg S₂ | ~0.11 bits | ~0.02 bits | **-0.085** |

**The headline finding:** Surprisal drops by 5.2 bits and entropy drops by 5.1 bits — almost identically. The result: **S₂ barely changes on average** (ΔS₂ = -0.085 bits). Poetry's deviance signature is remarkably stable across readings.

Split: 19/40 poems (47%) show *increased* S₂ on second reading; 21/40 (53%) show *decreased* S₂.

---

## Poems Where S₂ Increases on Second Reading (Structural Deviance)

| ΔS₂ | Title | Era | 1st S₂ | 2nd S₂ |
|-----|-------|-----|---------|---------|
| +1.34 | Simple narrative prose | control | -2.09 | -0.75 |
| +0.67 | Jabberwocky | nonsense | 0.47 | 1.14 |
| +0.59 | Elegy Written in a Country Churchyard | elegy | 0.16 | 0.75 |
| +0.52 | Nursery Rhymes (compilation) | nursery_rhyme | 0.10 | 0.62 |
| +0.51 | Lord Randal | ballad | 0.02 | 0.53 |
| +0.48 | Harlem | harlem_renaissance | 1.40 | 1.87 |
| +0.39 | Death, Be Not Proud | metaphysical | -0.64 | -0.25 |
| +0.38 | On the Departure Platform | pantoum | 0.07 | 0.45 |
| +0.25 | The Taxi | imagist | -0.74 | -0.49 |
| +0.22 | Preface to a Twenty Volume Suicide Note | black_arts | 0.65 | 0.87 |

---

## Poems Where S₂ Collapses on Second Reading (Sequential Deviance)

| ΔS₂ | Title | Era | 1st S₂ | 2nd S₂ |
|-----|-------|-----|---------|---------|
| -2.00 | Howl (opening) | beat | 1.41 | -0.59 |
| -1.02 | Because I could not stop for Death | 19th_century | 0.54 | -0.48 |
| -0.96 | Three Haiku (Basho, translated) | haiku | 2.14 | 1.18 |
| -0.83 | Tanka on longing | japanese_classical | -0.25 | -1.08 |
| -0.71 | Caedmon's Hymn | old_english | 0.34 | -0.36 |
| -0.52 | Self-Portrait in a Convex Mirror | new_york_school | 0.01 | -0.51 |
| -0.49 | Driving Toward the Lac Qui Parle River | deep_image | 0.25 | -0.24 |
| -0.44 | One Art | mid_century | 1.22 | 0.77 |
| -0.43 | Mann und Frau gehn... (trans.) | german_expressionist | 0.46 | 0.03 |
| -0.37 | They Flee from Me | early_modern | 1.04 | 0.67 |

---

## Finding 1: Structural vs Sequential Deviance

The clearest pattern: poems with **formal/repetitive structure** tend to show *increased* S₂ on second reading, while **free verse and narrative poems** tend to show *decreased* S₂.

**Structurally deviant** poems (S₂ increases or stays stable):
- Ballad (Lord Randal: +0.51) — refrain structure baked in
- Nursery rhyme (+0.52) — meter and repetition
- Elegy (Gray: +0.59) — formal stanza, iambic pentameter
- Metaphysical sonnet (Death Be Not Proud: +0.39) — rhetorical scaffolding
- Pantoum (+0.38) — fixed repetition form

**Sequentially deviant** poems (S₂ collapses):
- Beat (Howl: -2.0) — surprise depends on the catalog accumulating
- 19th century lyric (Dickinson: -1.0) — idiosyncratic word choices depend on cold encounter
- Haiku (Basho: -0.96) — extremely compressed, single-shot surprise

---

## Finding 2: The Jabberwocky Paradox

Jabberwocky (nonsense) becomes *more* deviant on second reading (+0.67):

| Pass | Surprisal | Entropy | S₂ |
|------|-----------|---------|-----|
| First | 5.95 | 5.48 | 0.47 |
| Second | 1.41 | 0.27 | **1.14** |

After one reading, GPT-2 "knows" the nonsense words. Its predictions become hyper-confident within the nonsense register (entropy collapses to 0.27 bits — far below any other poem). But it's still making confident predictions about the WRONG words at key positions. The model overcorrects into a fantasy of certainty, and the nonsense words deviate against that overconfident background.

---

## Finding 3: The Prose Paradox

Control prose shows the *largest* S₂ increase on second reading (+1.34):

| Pass | Surprisal | Entropy | S₂ |
|------|-----------|---------|-----|
| First | 4.12 | 6.21 | -2.09 |
| Second | 0.26 | 1.01 | **-0.75** |

Prose is predictable the first time (low surprisal, high entropy = very negative S₂). On second reading, the model predicts prose almost perfectly (surprisal → 0.26 bits). But entropy also drops sharply (to 1.01). The model becomes confident in this specific text — but its residual uncertainty is now concentrated in the genuinely unusual moments. Hence S₂ improves from -2.09 to -0.75.

This is the inverse of poetry: **prose improves toward S₂ ≈ 0 on rereading; poetry maintains or fluctuates around its first-reading S₂.**

---

## Finding 4: Harlem's Rhetorical Stability

Langston Hughes's "Harlem" shows strong S₂ stability (+0.48), rising from 1.40 to 1.87 — the highest second-reading S₂ in the dataset:

| Pass | Surprisal | Entropy | S₂ |
|------|-----------|---------|-----|
| First | 6.70 | 5.30 | 1.40 |
| Second | 2.42 | 0.54 | **1.87** |

The rhetorical structure ("What happens to a dream deferred?... Does it...?") establishes a template on first reading. On second reading, the model *expects* the anaphoric pattern — but the specific word choices at each slot remain deviant. The model's confidence about the template backfires: it predicts the template but not the filling.

---

## Finding 5: One-Shot Memorization

A striking methodological finding: after just ONE reading in context, GPT-2 "remembers" texts almost perfectly. Second-reading surprisal ranges from 0.11 to 2.42 bits (down from 3.76–8.22 bits on first reading). This demonstrates the extreme sensitivity of transformer context windows — a single exposure nearly eliminates surprisal.

This has implications for evaluating S₂: the standard analysis (cold context) captures *first-encounter* deviance. But first-encounter S₂ might overstate the structural deviance of sequential poems (Howl, Dickinson) relative to formal ones (ballad, Gray's Elegy).

---

## Two Types of Poetic Surprise

| Type | Description | Examples | ΔS₂ on rereading |
|------|-------------|----------|-----------------|
| **Structural** | Deviance baked into form/template; persists or grows when model is familiar | Ballad, formal elegy, rhyme schemes, Jabberwocky | Positive |
| **Sequential** | Deviance depends on novelty; surprise is consumed by the first reading | Beat catalog, Dickinson's idiosyncratic choices, haiku | Negative |

The most "reread-worthy" poems in information-theoretic terms may be the structurally deviant ones — they offer fresh deviance even to a model that has seen them before.

---

## Suggested Next Steps

1. **Extend to larger sample**: Run on all 419 poems with an expanded context window (GPT-2 medium has 1024 tokens, same as small, but with better context use).
2. **Third reading**: Does S₂ stabilize after the second reading, or keep changing?
3. **Identify structural markers**: What syntactic features predict which poems are structurally vs sequentially deviant?
4. **Correlate with reader experience**: Do "rereadable" (structurally deviant) poems correlate with canonical status, critical praise, or pedagogical selection?
5. **Formal vs free verse split**: Confirm the structural/sequential pattern holds across a larger, more balanced sample.
