# Entropy Decomposition: The Two Strategies of Poetic Surprise
**Date:** 2026-09-23
**Experiment:** `experiments/entropy_decomposition.py`
**Corpus:** 174 texts (169 poetry, 5 prose control), 17,905 non-artifact tokens

---

## Research Question

S₂ = surprisal − entropy. But *why* is a token surprising? There are two fundamentally different paths to high S₂:

1. **CERTAIN DEFIANCE** (low entropy + high surprisal): The model was confident about what should come next — its distribution was narrow, certain — and the poet defied it. This is the most willful form of deviation.

2. **CHAOS NAVIGATION** (high entropy + high surprisal): The model was already uncertain (many possible continuations), yet the poet still managed to choose something *even more* surprising than the uncertainty warranted.

By decomposing S₂ into its component axes, we can map where in the (entropy, surprisal) plane poetry operates, and identify what *kind* of surprise different poets and eras produce.

---

## Method

- All tokens filtered for stanza-break artifact (top prediction = `\n` with prob > 0.9)
- Median entropy (6.50) and median surprisal (4.99) used as quadrant thresholds
- Four quadrants defined:
  - **CERTAIN_DEFIANCE**: entropy < 6.50, surprisal > 4.99 → S₂ strongly positive
  - **CHAOS_NAVIGATION**: entropy ≥ 6.50, surprisal > 4.99 → S₂ positive but lower
  - **RIDING_WAVE**: entropy ≥ 6.50, surprisal ≤ 4.99 → S₂ negative (model uncertain, poet conformed)
  - **CONFORMITY**: entropy < 6.50, surprisal ≤ 4.99 → S₂ negative (model certain, poet agreed)

---

## Finding 1: Poetry Lives in the Chaos Navigation Quadrant

| Quadrant | Poetry % | Prose % |
|---|---|---|
| CHAOS_NAVIGATION | **36.6%** | 18.4% |
| CONFORMITY | 36.3% | **58.9%** |
| CERTAIN_DEFIANCE | 13.6% | 9.2% |
| RIDING_WAVE | 13.5% | 13.5% |

**The single largest difference between poetry and prose**: prose tokens occupy the CONFORMITY quadrant at 2× the rate of poetry (59% vs 36%). Poetry redirects this toward CHAOS_NAVIGATION (37% vs 18%).

The Defiance Ratio (CERTAIN_DEFIANCE / CONFORMITY):
- **Poetry: 0.374**
- **Prose: 0.156**

Poetry is 2.4× more likely to defy certainty than prose.

---

## Finding 2: Certain Defiance Produces the Highest S₂

| Quadrant | Mean S₂ | Mean Entropy | Mean Surprisal | n |
|---|---|---|---|---|
| CERTAIN_DEFIANCE | **+4.109** | 4.90 | 9.01 | 2,405 |
| CHAOS_NAVIGATION | **+0.954** | 8.73 | 9.68 | 6,502 |
| RIDING_WAVE | **−4.359** | 7.77 | 3.41 | 2,399 |
| CONFORMITY | **−1.966** | 3.73 | 1.76 | 6,436 |

**CERTAIN_DEFIANCE tokens carry 4.3× higher mean S₂ than CHAOS_NAVIGATION tokens.** When a poet defies the model's certainty, the gap between expectation and reality is maximal. The most "Straussian" moments — the widest gaps — are concentrated at positions where the model thought it knew what was coming.

This has a clean geometric interpretation: low entropy positions have narrow distributions. Choosing outside that narrow distribution requires going far away from the center, producing extreme surprisal. High-entropy positions already have spread-out distributions; you can only be somewhat more surprising than they are.

---

## Finding 3: Era Strategies Are Structured

| Era | CD% | CN% | DR | Dominant |
|---|---|---|---|---|
| german_symbolist | 15.2 | **50.3** | 0.635 | CHAOS |
| german_modernist | 19.7 | **41.0** | 0.630 | CHAOS |
| early_modern | 15.0 | **43.6** | 0.577 | CHAOS |
| mid_century | 16.3 | **37.4** | 0.519 | CHAOS |
| confessional | 14.6 | **41.1** | 0.487 | CHAOS |
| victorian | 13.2 | **43.6** | 0.465 | CHAOS |
| … | … | … | … | … |
| prose_poetry | **19.0** | 21.8 | 0.388 | CONFORMITY |
| found_poetry | **14.8** | 18.2 | 0.264 | CONFORMITY |
| song_lyrics | **13.5** | 18.8 | 0.235 | CONFORMITY |
| control prose | 9.2 | 18.4 | 0.156 | CONFORMITY |

Most poetry eras favor CHAOS_NAVIGATION. The exceptions — prose_poetry, found_poetry, song_lyrics — cluster with CONFORMITY. This aligns with the theoretical expectation: found texts and song lyrics operate in more statistically "normal" language spaces, while canonical verse pushes into high-entropy territory.

The German literary movements (Symbolist, Modernist, Expressionist) score highest for chaos navigation, reflecting their difficult, symbol-dense diction.

---

## Finding 4: Author Strategies Split Along "Sparse vs Dense" Lines

At **high-S₂ moments specifically** (S₂ ≥ 3.0), authors separate cleanly:

### Predominantly CERTAIN DEFIANCE (>70% of high-S₂ moments)
These poets achieve surprise by confronting positions where the model was confident:

| Author | High-S₂ | CD% | Profile |
|---|---|---|---|
| Rae Armantrout | 15 | 80% | Minimalist, spare language |
| Russell Edson | 19 | 79% | Prose-surrealist, short sentences |
| Anonymous (found texts) | 40 | 78% | Plain, functional language baseline |
| Elizabeth Bishop | 8 | 75% | Quiet precision |

### Predominantly CHAOS NAVIGATION (>80% of high-S₂ moments)
These poets achieve surprise by finding unexpected words in already uncertain positions:

| Author | High-S₂ | CN% | Profile |
|---|---|---|---|
| Alfred Lord Tennyson | 14 | 93% | Dense Victorian diction |
| Ernest Dowson | 12 | 92% | Rich, ornate Symbolist style |
| Ben Jonson | 7 | 86% | Complex early-modern syntax |
| George Herbert | 40 | 78% | Metaphysical intricacy |
| John Milton | 39 | 77% | Epic complexity |

**The pattern**: sparse, conversational, and minimalist poets favor CERTAIN DEFIANCE — they surprise you at moments of maximum certainty. Dense, ornate, and syntactically complex poets favor CHAOS NAVIGATION — they surprise you in the already-turbulent space of complex diction.

---

## Finding 5: Exemplary Moments

### CERTAIN DEFIANCE (model certain, poet defied)
- **Stefan George**: `…alone` → `' ferner'` [H=1.25, surprisal=24.65, S₂=23.40]
  Model was ~certain about a continuation; George inserts a German adverb that carries the poem elsewhere.
- **Gerard Manley Hopkins**: context → `' shook'` [H=3.60, surprisal=25.64, S₂=22.04]
  Hopkins at his most willful — the sprung-rhythm logic produces certainty-defying verbs.
- **Walt Whitman**: `…at my ease` → `'observing'` [H=2.39, surprisal=22.78, S₂=20.40]
  Whitman's famous participial extension — the model expected a sentence to end; he continues it.

### CHAOS NAVIGATION (model uncertain, poet still surprised)
- **Sylvia Plath**: `…Daddy` → `' Ach'` [H=8.44, surprisal=21.59, S₂=13.14]
  High-entropy position (anything could follow); Plath's German exclamation is still more surprising than the entropy admits.
- **Thomas Hardy**: context → `' solitude'` [H=8.65, surprisal=21.59, S₂=12.94]
  Hardy navigates uncertainty toward a philosophically weighted noun.
- **Robert Burns**: context → `' backward'` [H=8.33, surprisal=20.17, S₂=11.85]
  Burns's Scots vernacular deflects even uncertain predictions.

---

## Theoretical Implications

The decomposition reveals two distinct **aesthetic regimes** of surprise:

1. **The Confrontational Mode (Certain Defiance)**: The poet meets the model's certainty head-on, choosing against the grain at the most predictable positions. This is the "zero-entropy interrupt" — suppressing the inevitable. Minimalist, imagist, and contemporary lyric poets favor this strategy.

2. **The Immersive Mode (Chaos Navigation)**: The poet dwells in regions of high uncertainty and finds surprise even there. This is what happens in dense, complex, syntactically intricate verse — the model is already uncertain, and the poet compounds that uncertainty further. The German tradition, Metaphysical poets, and the Romantics use this mode.

Neither strategy is "more surprising" in some absolute sense: CERTAIN DEFIANCE produces higher raw S₂, but CHAOS NAVIGATION sustains a state of elevated entropy that may create a different cognitive experience — longer immersion in the unknown rather than a sharp interrupt.

---

## Suggested Next Steps

1. **Entropy trajectory analysis**: Does a poem's mean entropy increase or decrease as it progresses? Do high-CN poets create "entropy ramps" while CD poets create "entropy punctures"?
2. **Within-poem strategy mixing**: Which poems use *both* strategies deliberately, and how do they alternate?
3. **The 50-50 authors**: Several authors split evenly (Lyn Hejinian, Bruce Andrews, Isaac Newton). Are these truly hybrid strategists or is the split random?
4. **Era transition**: Does the shift from Romantic to Modernist represent a shift from CHAOS_NAVIGATION toward CERTAIN_DEFIANCE (as poetic language became sparser)?
