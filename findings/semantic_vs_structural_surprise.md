# Semantic vs Structural Surprise: What Drives Poetic S₂?

**Date:** 2026-10-03  
**Experiment:** `experiments/semantic_embedding_distance.py` → `results/semantic_embedding_distance.json`  
**Corpus:** 200 texts, 16,540 content tokens (punctuation, whitespace, stanza-break artifact tokens excluded)  
**Builds on:** `straussian_gap_taxonomy.md`, `suppressed_lexicon.md`, `semantic_field_of_surprise.md`

---

## Research Question

When a poem achieves a high-S₂ moment — when the poet writes something more surprising than the context warranted — is that surprise *semantic* (the poet crossed into a different semantic field than expected) or *structural* (the poet used a word semantically close to the prediction, but the specific choice or grammatical role was unexpected)?

This question matters for our model of what poetry does. "Semantic surprise" = the poet imported something foreign; "structural surprise" = the poet used the right material in the wrong slot.

---

## Method

For each content token in the corpus:
1. Get S₂ from pre-computed results
2. Get GPT-2's top-1 predicted token (alternatives[0])
3. Compute cosine distance between GPT-2's input embeddings for the actual token vs the top-1 predicted token
4. This *semantic distance* measures: how far (in embedding space) is what the poet wrote from what the model expected?

**Quadrant classification:**
- **A** (Low-S₂, Low-dist): conformist — the expected word, semantically typical
- **B** (Low-S₂, High-dist): semantic match — unusual word, but somehow expected  
- **C** (High-S₂, Low-dist): *structural surprise* — unexpected, but semantically near the prediction
- **D** (High-S₂, High-dist): *semantic surprise* — unexpected AND semantically far from the prediction

Threshold: S₂ > 0 = "high"; semantic distance > corpus median (0.597) = "high".

---

## Main Finding: S₂ is a Semantic Measure

**Correlation r(S₂, semantic distance) = +0.55** across all content tokens.

This is a moderately strong positive relationship: the more surprising a token's S₂ value, the more likely the actual token is semantically far from the top-1 prediction. Poetic surprise is substantially *semantic displacement*, not just structural misfit.

The correlation is nearly identical for poetry (r = 0.553) and prose controls (r = 0.549). This is a property of the GPT-2 model itself: when a token has high surprisal and high entropy, the most likely reason is that it falls into a different part of the embedding space from what the model expected.

### Quadrant counts

| Quadrant | Description | n | % | Avg S₂ |
|---|---|---|---|---|
| **A** | Low-S₂, Low-dist (conformist) | 6,993 | 42.3% | −2.66 |
| **B** | Low-S₂, High-dist (semantic match) | 3,060 | 18.5% | −1.95 |
| **C** | High-S₂, Low-dist (structural) | 1,277 | 7.7% | +2.10 |
| **D** | High-S₂, High-dist (semantic) | 5,210 | 31.5% | +3.99 |

The largest share (42%) of tokens are simply conformist (A). Among the 38.8% of tokens with high-S₂:
- **80.3% are semantic surprises (D)** — the poet went somewhere else entirely
- **19.7% are structural surprises (C)** — the poet used a nearby word in an unexpected way

Semantic surprise is not just more common; it is also more intense: avg S₂ in quadrant D (+3.99) is nearly double quadrant C (+2.10).

### The top-100 highest-S₂ moments are overwhelmingly semantic

The top-100 highest-S₂ tokens have avg semantic distance **0.81**, compared to the overall median of 0.60. The most extreme poetic deviations correlate with the largest embedding-space jumps.

---

## Era Breakdown: Who Uses Structural vs Semantic Surprise?

Among each era's high-S₂ tokens, what fraction are structural (C) vs semantic (D)?

| Era | n | Hi-S₂ | Struct% | Sem% | Avg-dist (hi-S₂) |
|---|---|---|---|---|---|
| song_lyrics | 421 | 111 | **32.4%** | 67.6% | 0.644 |
| prose_poetry | 745 | 272 | **29.4%** | 70.6% | 0.652 |
| mid_century | 192 | 76 | **28.9%** | 71.1% | 0.693 |
| new_york_school | 1,134 | 432 | **28.9%** | 71.1% | 0.672 |
| biblical | 746 | 260 | **28.5%** | 71.5% | 0.666 |
| … | | | | | |
| haiku | 200 | 84 | 10.7% | **89.3%** | 0.740 |
| german_expressionist | 237 | 119 | 8.4% | **91.6%** | 0.726 |
| concrete | 89 | 19 | 5.3% | **94.7%** | 0.798 |
| german_symbolist | 299 | 144 | 4.9% | **95.1%** | 0.715 |

**Pattern:** Accessible, popular forms (song lyrics, prose poetry, New York School) achieve more of their surprise *structurally* — using familiar words in unfamiliar positions or combinations. Avant-garde and highly imagistic forms (haiku, concrete poetry, German symbolism/expressionism) achieve surprise almost entirely through *semantic displacement* — importing words from different semantic territories.

Notably, the **control** (prose) texts are 88% semantic surprise, close to the poetry average. This suggests the structural/semantic ratio is not what distinguishes poetry from prose — rather, prose has fewer high-S₂ moments overall, but when they occur, they're also mostly semantic.

---

## Exemplary Cases

### Structural surprise (C): high-S₂, semantically near
These tokens surprised the model statistically but stayed in the same semantic neighborhood as the prediction:

- `'which'` (expected `.`) in Gertrude Stein's *Susie Asado* (S₂=+15.1, dist=0.59) — a conjunction used where syntax expected closure
- `'three'` (expected `'an'`) in *The Wife of Usher's Well* (S₂=+14.9, dist=0.55) — a numeral vs indefinite article, both low-content function words
- `'could'` (expected `'with'`) in Countee Cullen's *Yet Do I Marvel* (S₂=+10.0, dist=0.58) — modal vs preposition

### Semantic surprise (D): high-S₂, semantically far
These tokens traveled into different semantic territory entirely:

- `'shook'` (expected `'the'`) in Hopkins's *God's Grandeur* (S₂=+22.0, dist=0.90) — concrete action verb vs determiner
- `'prank'` (expected `'the'`) in Smart's *For I Will Consider My Cat Jeoffry* (S₂=+22.0, dist=0.96) — rare noun vs common function word
- `'badly'` (expected `'glass'`) in Bishop's *One Art* (S₂=+20.6, dist=0.76) — adverb of quality vs concrete noun
- `'observing'` (expected `','`) in Whitman's *Song of Myself* (S₂=+20.4, dist=0.90) — gerund vs punctuation

---

## Interpretation

S₂ = surprisal − entropy is predominantly a *semantic* signal. When a poet earns a high-S₂ moment, they have usually crossed into a different part of the language's semantic space, not merely chosen an unusual word within the expected semantic field.

This has implications for the "Straussian gap" framework: the gap between what the model expected and what the poet wrote is, in 80% of cases, not just a different word from the same drawer but a word from a different room entirely. The unsaid and the said are semantically far apart.

The structural surprise cases (C) are also meaningful: they represent precision within a semantic field. Gertrude Stein's "which" is syntactically shocking but doesn't leap to a new semantic territory — this is the dissociative, grammatically-organized surprise characteristic of Language poetry and prose poetry. The haiku's and German symbolists' 95% semantic ratio reflects the opposite strategy: maximum semantic displacement, often within tightly controlled syntax.

---

## Next Steps

1. **Intra-poem arcs**: Does the structural/semantic ratio shift across a poem's phases? Are openings more structural (setting up a framework) and climaxes more semantic (the leap)?
2. **The B quadrant anomaly**: Tokens with low-S₂ but high semantic distance (3,060 tokens, 18.5%) — how can a word be semantically far from the prediction yet unsurprising? These may be cases where GPT-2's embedding space doesn't match its probability model (a word's embedding is distant, but many similar-embedding words were also plausible).
3. **Cross-poet analysis**: Do individual poets have stable structural/semantic ratios? Is this a signature of poetic voice — some poets are reliably structural surprisers, others semantic?
