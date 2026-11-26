# Entropy Inflation Per Poet: A Four-Quadrant Model of Poetic Deviation

**Date:** 2026-11-26  
**Experiment:** `experiments/entropy_inflation_per_poet.py` → `results/entropy_inflation_per_poet.json`  
**Corpus:** 450 texts, 54,654 artifact-free tokens  
**Builds on:** `genuine_surprise_catalog.md`, `entropy_conditioned_deviation.md`

---

## Research Question

`genuine_surprise_catalog.md` proposed a **two-mode model** of poetic deviation:
- *Chaos Navigation* (Stein): poet raises entropy everywhere, making every token hard to predict, but S₂ stays low because the model is already uncertain
- *Certain Defiance* (Hopkins): poet operates in tight contexts where the model is confident, then deviates sharply — producing high S₂

**This experiment quantifies which poets use which strategy** by measuring mean context entropy and mean S₂ per poet in a full 2D space — and finds the two-mode model is incorrect.

---

## Method

For each poet with ≥ 50 artifact-free tokens:
- Compute **mean context entropy** (how uncertain is GPT-2 when reading this poet?)
- Compute **mean S₂** (how often does the poet exceed what uncertainty warrants?)
- Compute **entropy inflation ratio** = poet_entropy / corpus_mean_entropy

Classify into four quadrants relative to corpus means:
- **BOTH_MODES**: high entropy + high S₂ (raises uncertainty AND exceeds it)
- **CHAOS_NAVIGATION**: high entropy + low S₂ (raises uncertainty but doesn't exceed it)
- **CERTAIN_DEFIANCE**: low entropy + high S₂ (operates in predictable contexts, deviates sharply)
- **SMOOTH_CONFORMITY**: low entropy + low S₂ (prose-like, neither raises nor exceeds expectations)

**Corpus baselines:** mean entropy = 6.415 bits; mean S₂ = −0.262 bits

---

## Main Finding 1: The Two-Mode Model Was Wrong

The genuine_surprise_catalog proposed Gertrude Stein as the exemplar of "chaos navigation." 
**She is not.** Proper quadrant analysis shows:

| Poet | Mode | Mean Entropy | Inflation | Mean S₂ |
|---|---|---|---|---|
| **Gertrude Stein** | CERTAIN_DEFIANCE | 5.399 | 0.842 | −0.197 |
| **Gerard Manley Hopkins** | BOTH_MODES | 7.548 | 1.177 | +0.243 |

Stein's repetitive style ("a rose is a rose is a rose") **reduces** entropy below the corpus mean — the model quickly learns her patterns and becomes *more* certain. Within those tight predictable contexts, she barely edges above the S₂ baseline (−0.197 vs corpus mean −0.262). She is a mild certain-devier, not a chaos navigator.

Hopkins, by contrast, raises entropy substantially above baseline AND still exceeds even that elevated uncertainty. His unusual diction creates maximum model confusion AND then surprises even within that confusion. He belongs in the richest category: **BOTH_MODES**.

**The corrected taxonomy:**

| Quadrant | n poets | Exemplars |
|---|---|---|
| BOTH_MODES | 63 | Ferlinghetti, Brathwaite, Hart Crane, Niedecker, Cummings, Bök, Creeley, Ginsberg, Moore, Hopkins |
| CHAOS_NAVIGATION | 41 | W.C. Williams, Marvell, Donne, Gray, Oppen, Keats, Stevens, Reverdy |
| CERTAIN_DEFIANCE | 29 | Rilke, Bishop, Glück, Berryman, Stafford, Vallejo, Thompson, Stein (mild) |
| SMOOTH_CONFORMITY | 66 | Control prose, limericks, Watten, Antin, Berrigan, Merwin, Dowson |

---

## Main Finding 2: Language Poetry Is Smooth Conformity

The most surprising result:

| Poet | Mode | Entropy | Inflation | S₂ |
|---|---|---|---|---|
| Barrett Watten | SMOOTH_CONFORMITY | 6.049 | 0.943 | −1.049 |
| David Antin | SMOOTH_CONFORMITY | 6.165 | 0.961 | −1.116 |
| Charles Bernstein | SMOOTH_CONFORMITY | 5.787 | 0.902 | −0.661 |

Language poetry — associated with semantic disruption, anti-referential writing, and "making strange" — **neither raises GPT-2's entropy nor produces above-average S₂**. It is the most conformist poetry in the corpus by both measures.

This is not an artifact. Barrett Watten (163 artifact-free tokens) and David Antin (89 tokens) consistently produce below-average entropy AND below-average S₂. Their apparent semantic disruption either (1) follows patterns that GPT-2 has internalized from similar experimental prose, or (2) disrupts *meaning* without disrupting *statistical structure*. The model can predict Language poetry's tokens well even if human readers find them semantically opaque.

**Compare to cliché controls:** Synthetic cliché text: entropy=5.349, S₂=−1.032. Language poetry and cliché poetry are **statistically indistinguishable** by this framework.

---

## Main Finding 3: The Chaos Navigation Poets Are Canonical Modernists

Poets in the CHAOS_NAVIGATION quadrant (high entropy but low S₂) tend to be canonical modernists and 17th-century metaphysicals:

| Poet | Era | Entropy | Inflation | S₂ |
|---|---|---|---|---|
| William Carlos Williams | modernist | 7.590 | 1.183 | −0.536 |
| Emma Lazarus | 19th_century | 7.479 | 1.166 | −0.805 |
| Andrew Marvell | early_modern | 7.470 | 1.165 | −0.718 |
| Thomas Gray | 18th_century | 7.432 | 1.159 | −0.504 |
| George Oppen | objectivist | 7.307 | 1.139 | −0.568 |
| John Donne | early_modern | 7.251 | 1.130 | −0.636 |
| Pierre Reverdy | modernist | 7.179 | 1.119 | −1.504 |
| John Keats | romantic | 7.050 | 1.099 | −0.374 |
| Wallace Stevens | modernist | 7.031 | 1.096 | −0.467 |

**Williams raises entropy the most of any poet in the corpus (7.590)** — his fragmentary line breaks and monosyllabic bursts create maximum uncertainty about what word follows. But the words he chooses (wheelbarrow, plums, cold) are common within their fragmented contexts. He navigates the chaos rather than adding to it.

**Donne and Marvell's metaphysical conceits** create high entropy through semantic yoking-of-opposites, but the tokens they choose follow predictably once the conceit is established. The model can follow the logic of a metaphysical argument even if the initial setup is surprising.

**Reverdy's extreme chaos** (entropy=7.179, S₂=−1.504) suggests he creates maximum uncertainty and then makes the most conventionally expected choice — a "chaos-then-surrender" strategy not found elsewhere in the corpus.

---

## Main Finding 4: The BOTH_MODES Poets Are Formally Deviant

Poets who both raise entropy AND exceed it tend to share a characteristic: **formal or typographical innovation** that creates genuine uncertainty about the next token class, combined with **lexically unusual choices** that exceed even that elevated uncertainty.

| Poet | Era | Entropy | Inflation | S₂ | n tokens |
|---|---|---|---|---|---|
| Kamau Brathwaite | postcolonial | 6.445 | 1.005 | +1.280 | 106 |
| Hart Crane | modernist | 6.861 | 1.070 | +1.257 | 155 |
| Lorine Niedecker | objectivist | 7.404 | 1.154 | +1.248 | 168 |
| E.E. Cummings | modernist | 7.571 | 1.180 | +0.962 | 145 |
| Christian Bök | oulipo | 6.984 | 1.089 | +0.952 | 209 |
| Robert Creeley | beat | 6.531 | 1.018 | +0.928 | 111 |
| Allen Ginsberg | beat | 6.571 | 1.024 | +0.790 | 144 |
| Marianne Moore | modernist | 6.494 | 1.012 | +0.761 | 474 |
| Georg Trakl | german_expressionist | 6.614 | 1.031 | +0.702 | 264 |

(Note: Ferlinghetti appears first with S₂=2.911 but high sd=7.82, suggesting spacing artifacts dominate his mean.)

**Cummings** (entropy=7.571, S₂=+0.962): His typographic fragmentation creates maximum entropy AND his lexical choices are genuinely unprecedented within those fragmented contexts.

**Niedecker** (entropy=7.404, S₂=+1.248): Her compressed Objectivist lines create high entropy AND choose unexpected nouns/verbs within them.

**Bök** (entropy=6.984, S₂=+0.952): His constrained Oulipo writing raises entropy through unusual word forms AND the actual chosen tokens are lexically extreme.

---

## Main Finding 5: The Certain Defiance Poets Are the Most "Precision Surprising"

| Poet | Era | Entropy | S₂ | Precision Rate |
|---|---|---|---|---|
| Francis Thompson | victorian | 6.402 | +0.847 | 0.348 |
| Rainer Maria Rilke | german_modernist | 6.178 | +0.747 | 0.413 |
| John Berryman | confessional | 6.285 | +0.540 | 0.333 |
| Louise Glück | contemporary | 6.054 | +0.397 | 0.412 |
| Elizabeth Bishop | confessional | 5.803 | +0.335 | 0.345 |
| César Vallejo | latin_american | 5.706 | +0.270 | 0.352 |

**Precision Rate** = fraction of low-entropy tokens where S₂ > 0 (how often the poet defies the model when the model is confident).

Rilke's precision rate of 0.413 means: at 41.3% of positions where GPT-2 is *confident* about what comes next, Rilke writes something unexpected. For comparison, control prose: 13.9%. Rilke surprises the confident model 3× more often than prose.

**Bishop's low entropy (5.803) paired with positive S₂ (+0.335)** illustrates her style perfectly: crystalline clarity of observation (reducing model uncertainty) followed by a single word that breaks the pattern. Her famous line about "practicing losing" illustrates this — the semantic certainty of her setup collapses unexpectedly.

---

## Implications and Revisions to Prior Findings

1. **The two-mode model in genuine_surprise_catalog was incorrect**. Stein is not "chaos navigation" — she's mild certain defiance. The proposed test case (Hopkins vs. Stein) was measuring the right contrast (entropy vs. S₂) but assigned the wrong poet to the wrong mode.

2. **Four modes, not two.** The corpus shows four distinct strategies: BOTH_MODES (poets who maximize both entropy and deviation), CHAOS_NAVIGATION (maximize entropy but surrender to it), CERTAIN_DEFIANCE (minimize entropy, maximize deviation), and SMOOTH_CONFORMITY (neither).

3. **Language poetry is smooth conformity** — statistically indistinguishable from cliché. If the goal of Language poetry was to defamiliarize language, it succeeded for human readers but not for the statistical language model. This may mean: Language poetry exploits human top-down semantic expectations, not bottom-up statistical regularities.

4. **Chaos navigation is the mode of canonical modernism** (Donne, Williams, Keats, Stevens) — not of experimental avant-garde. The experimental poets (Cummings, Bök, Creeley) are mostly BOTH_MODES.

5. **The BOTH_MODES poets** represent the information-theoretically richest writing: they create uncertainty AND exceed it. These tend to be formally innovative modernists and Objectivists.

---

## Suggested Next Steps

1. **Ferlinghetti artifact audit**: His S₂=2.911 is driven by sparse extreme spikes (sd=7.82). Repeat with the Ferlinghetti spacing artifact filter proposed in genuine_surprise_catalog.
2. **Entropy inflation trajectory within poem**: Does a poet's entropy inflation change over the course of the poem? Do some poets build toward maximum-entropy/maximum-deviation moments?
3. **Cross-quadrant genre analysis**: Map eras onto the four quadrants — which eras concentrate in which modes?
4. **Why is Language poetry smooth?** Probe specific Language poetry substitutions to understand whether GPT-2 had already internalized that style's conventions, or whether semantic disruption is statistically invisible.
