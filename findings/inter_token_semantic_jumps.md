# Inter-Token Semantic Jumps vs S₂: Two Different Kinds of Surprise

**Date:** 2026-10-04  
**Experiment:** `experiments/inter_token_semantic_jumps.py` → `results/inter_token_semantic_jumps.json`  
**Corpus:** 197 texts (202 total, 5 filtered for < 10 tokens), 16,590 adjacent content-token pairs  
**Stanza-break artifact removed:** p_newline < 0.9 filter applied  
**Builds on:** `semantic_vs_structural_surprise.md`, `haiku_kireji_s2.md`

---

## Research Question

When a poet places two semantically distant words next to each other — the **horizontal semantic jump** —
is this the same event as S₂, the **vertical prediction surprise**?

The haiku kireji study found that the word immediately after the structural cut has S₂ ~ +19.
But in the kireji case, the semantic jump (image A → image B) and the prediction surprise
(GPT-2 built predictions around image A, now gets image B) are aligned by design.
Does this alignment hold generally across the corpus?

This experiment computes the **cosine distance between adjacent token embeddings** (from GPT-2's
`wte` matrix, the token embedding layer) and asks: how strongly does this "horizontal" distance
correlate with the "vertical" S₂?

---

## Central Finding: Two Weakly Correlated Measures

| Measure | r with S₂ |
|---|---|
| Actual vs. predicted embedding distance (prior study) | **+0.55** |
| Adjacent (inter-token) embedding distance (this study) | **+0.171** |

**The horizontal (inter-token) distance and the vertical (prediction failure) distance are
largely independent.** S₂ is primarily driven by GPT-2's prediction failure — the semantic
gap between what was expected and what was written — not by whether adjacent words are
semantically dissimilar to each other.

A poet can place semantically distant words next to each other (e.g., "burning cold") without
creating S₂, if GPT-2 can predict the semantic jump in context. And a poet can generate
high S₂ with semantically related adjacent words, if the specific word chosen is unexpected
despite being close to its neighbor.

---

## Distribution of Inter-Token Distances

The median inter-token cosine distance across the corpus is **0.759** — most adjacent
token pairs in poetry are already semantically quite far in embedding space. The 10th
percentile is 0.608, so even "close" adjacent tokens are not particularly near.

| Percentile | Inter-token distance |
|---|---|
| 10th | 0.608 |
| 25th | 0.698 |
| 50th (median) | 0.759 |
| 75th | 0.807 |
| 90th | 0.853 |
| 95th | 0.886 |

This high baseline reflects both the geometry of GPT-2's embedding space (most tokens
are far from each other in 768 dimensions) and the nature of poetic language (adjacent
words often come from different semantic fields).

---

## Poetry vs. Prose: Prose is More Locally Coherent

| Era | Mean inter-token dist | Mean S₂ (clean) |
|---|---|---|
| **oulipo** | **0.805** | +0.32 |
| german_expressionist | 0.771 | +0.85 |
| romantic | 0.758 | −0.03 |
| german_symbolist | 0.754 | +0.46 |
| found_poetry | 0.754 | −0.53 |
| … | … | … |
| spoken_word | 0.724 | −0.34 |
| **prose poetry** | **0.713** | −0.31 |
| **new_york_school** | **0.710** | −0.34 |
| **prose control** | **0.714** | −1.77 |

**Prose has the lowest mean inter-token distance (0.714)** — adjacent words in prose are
more locally semantically coherent than adjacent words in poetry. Poetry imposes more
local semantic discontinuity, even when controlling for overall S₂.

Surprisingly, **New York School poetry** (0.710) and **prose poetry** (0.713) have
*lower* inter-token distances than prose controls — these forms are not only low-S₂
but also locally smooth. This fits their aesthetics: the New York School aimed for
a conversational, associative flow, not semantic shock.

**German Expressionism** leads in inter-token distance (0.771) while maintaining
positive mean S₂ (+0.85). These poems are both locally discontinuous AND statistically
surprising — a distinctive signature.

---

## The S₂–Distance Correlation Varies by Era

| Era | r(S₂, inter-token dist) | Character |
|---|---|---|
| 18th century | **+0.318** | High alignment |
| beat | **+0.310** | High alignment |
| confessional | **+0.299** | High alignment |
| surrealist | **+0.275** | High alignment |
| deep_image | **+0.247** | High alignment |
| concrete | **−0.056** | Decoupled |
| german_expressionist | **−0.058** | Decoupled |
| german_symbolist | **+0.021** | Decoupled |
| oulipo | **−0.219** | Inversely related |

Where the correlation is high (beat, confessional, deep image), semantic jumps and
prediction surprises tend to occur at the same moments — **the two forms of surprise
are aligned**. These are forms where imagery is primary and the juxtaposition of images
drives both discontinuity and statistical unexpectedness.

Where the correlation is low or negative (oulipo, German expressionist, symbolist),
the two measures diverge — **semantic jumps occur independently of prediction surprise**.
Oulipo's negative correlation (−0.219) suggests these poems use unexpected word choices
that are semantically *close* to their neighbors: the surprise is linguistic/formal,
not semantic.

---

## Two Types of Semantic Jump

**"Pure semantic jumps"** (inter-token distance > 0.90, S₂ < 0.0): adjacent tokens are
semantically far apart, but GPT-2 correctly anticipated the semantic field shift. This
happens most often at grammatical junctions — a content word followed by a conjunction
("and", "the", "a") that GPT-2 predicted. The semantic distance between a noun and a
following article is high by geometry (they're in different parts of the embedding space),
but the article is statistically expected.

**"Aligned surprises"** (inter-token distance > 0.65, S₂ > 3.0): both measures fire.
Representative examples:
- "glass" (modernist, S₂=+25.6, dist=0.724)
- "prank" (18th century, S₂=+22.0, dist=0.824)
- "shook" (victorian, S₂=+22.0, dist=0.783)
- "badly" (mid-century, S₂=+20.6, dist=0.830)

These are the moments where a poet installs a semantically foreign element at a point
where the model was both surprised AND where the word lands far from its neighbor. These
are not just unexpected choices — they are choices that rupture the local semantic fabric
in both directions.

---

## Interpretation

The weak global correlation (r = 0.171) between S₂ and inter-token distance resolves
an open question in this research program: **S₂ is primarily a measure of prediction
failure, not of local semantic discontinuity**.

Two adjacent semantically distant words (like "burning cold") can both be GPT-2-predictable
(if the model learned that temperature words follow each other), in which case neither has
high S₂. Conversely, a word can be highly surprising (high S₂) even when its neighbor is
semantically related — this is the "structural surprise" quadrant identified in
`semantic_vs_structural_surprise.md`.

The implication for S₂ as a measure of poetic surprise is that it captures the **pragmatic
unexpectedness** (what the model expected in context) more than the **presentational
discontinuity** (how jarring the local adjacency feels). These may both feel like "surprise"
to a reader, but they are computationally different — and the two forms vary independently
across eras and poets.

---

## Suggested Next Steps

1. **Filter out function words** from inter-token distance analysis — much of the "pure
   jump" signal is inflated by content-to-article transitions, where the grammatical
   distance is high but the prediction is trivial. Measuring content-to-content distance
   only would sharpen the analysis.

2. **Semantic arc within a poem**: Does a poem's mean inter-token distance follow a temporal
   arc? Does it peak at the volta or opening (consistent with the within_poem_type_arc finding)?

3. **Poet-level inter-token distance fingerprints**: The existing `poet_s2_fingerprints.md`
   tracks S₂. Adding inter-token distance would give poets a 2D signature: (S₂ level,
   local semantic discontinuity). Poets like the New York School and Whitman might separate
   in this space even though their S₂ values are similar.

4. **Era-level divergence score**: For each era, compute the fraction of tokens where
   inter-token distance and S₂ diverge most (one high, one low). This would operationalize
   the idea of "semantic coherence under prediction violation" (high S₂, low distance —
   structural surprise) vs. "semantic shock without prediction failure" (high distance,
   low S₂ — smooth semantic jumps).
