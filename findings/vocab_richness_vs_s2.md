# Vocabulary Richness vs S₂: Lexical Diversity and the Straussian Gap
**Date:** 2026-08-30  
**Experiment:** `experiments/vocab_richness.py`

## Question
Do poets with richer vocabulary (higher type-token ratio) have different information-theoretic signatures? Is lexical diversity a proxy for the Straussian gap — or are they orthogonal?

## Method
- Type-token ratio (TTR): unique word types / total word tokens  
- Hapax ratio: words appearing exactly once / total tokens  
- Repeat ratio: fraction of tokens that are repeated  
- Computed for all 51 English poems (excluding control prose)  
- Correlated with avg_S₂, avg_surprisal, avg_entropy  
- Length-stratified analysis (< 40 words vs ≥ 40 words)

---

## Results

### Overall Correlations (n=51)

| Metric | r (TTR vs …) |
|---|---|
| TTR vs avg_S₂ | **+0.254** |
| TTR vs avg_surprisal | **+0.428** |
| TTR vs avg_entropy | **+0.212** |
| repeat_ratio vs avg_S₂ | **−0.271** |

Lexically richer poems are more surprising overall (r=+0.43 for surprisal) but only moderately more "Straussian" (r=+0.25 for S₂).

---

## Core Finding: TTR Predicts Surprisal But Not S₂ in Longer Poems

When stratified by poem length, a striking dissociation appears:

| Subset | n | TTR vs avg_S₂ | TTR vs avg_surprisal |
|---|---|---|---|
| All poems | 51 | +0.254 | +0.428 |
| Short poems (< 40 words) | 14 | **+0.448** | **+0.529** |
| Long poems (≥ 40 words) | 37 | **−0.038** | **+0.258** |

**Among long poems, vocabulary richness has essentially zero correlation with the Straussian gap (r = −0.04).** Rich vocabulary and unexpected word choice are orthogonal for longer poems. A poet can command a vast vocabulary while still choosing statistically predictable words — and a poet with a small, repetitive vocabulary can still make maximally unexpected choices within that constraint.

This means the Straussian gap (S₂) is measuring something genuinely different from lexical variety: it is the *timing* and *targeting* of unexpected choices, not just the breadth of vocabulary.

---

## Quartile Analysis

| Group | n | avg_TTR | avg_S₂ | avg_surprisal | avg_entropy | pos_S₂_ratio |
|---|---|---|---|---|---|---|
| Bottom 25% TTR (most repetitive) | 12 | 0.604 | +0.173 | 5.999 | 5.825 | 0.352 |
| Top 25% TTR (most lexically rich) | 13 | 0.884 | +0.666 | 7.219 | 6.553 | 0.407 |

Lexically rich poems are more surprising (1.22 bits more avg surprisal), have more Straussian moments (+0.49 avg S₂), and cross the positive threshold more often (+5.5pp). But the effect shrinks dramatically when length is controlled.

---

## Spotlight: Extremes

### Most Lexically Rich (highest TTR):
| TTR | Avg S₂ | Poem |
|---|---|---|
| 1.000 | **+3.59** | Williams, "The Red Wheelbarrow" |
| 1.000 | +0.26 | Pound, "In a Station of the Metro" |
| 0.946 | +0.06 | Eliot, "The Waste Land (opening)" |
| 0.931 | +1.85 | Andrews, "Islets/Irritations" |

Note: The two TTR=1.000 poems have radically different S₂ (+3.59 vs +0.26). Maximum lexical richness does not determine maximum surprise — a poem where every word is unique can still be either very Straussian or not, depending on the *kind* of unique words chosen.

### Most Repetitive (lowest TTR):
| TTR | Avg S₂ | Poem |
|---|---|---|
| 0.463 | **+0.51** | Long Soldier, "Whereas (excerpt)" |
| 0.500 | −0.21 | Ashbery, "Leaving the Atocha Station" |
| 0.576 | +0.32 | Ashbery, "Paradoxes and Oxymorons" |

---

## Case Study: Layli Long Soldier's "Whereas"

The "Whereas" poems have the lowest TTR in the corpus (0.463, rank 1 most repetitive) but still positive S₂ (+0.51). This is anaphoric poetry: the legal formula "Whereas" repeats as a structural scaffold, suppressing entropy in the opening position. The scaffold is maximally predictable (GPT-2 easily anticipates "Whereas" once the pattern is established), but the *content* following each "Whereas" is maximally unexpected.

This is the inverse of passive voice (see `voice_active_passive.md`): where passive voice uses a predictable grammatical scaffold to hide the agent and detonate it at the end, anaphoric poetry uses a predictable syntactic scaffold to absorb expectation and then *fill it with anomaly*. Repetition of form enables surprise in content.

**Mechanism:** Low TTR + Positive S₂ = structured deviation. The form creates a predictable channel; the content pushes back against it.

---

## Interpretation

1. **Lexical richness inflates surprisal more than S₂.** Unique words are harder to predict (higher surprisal), but they also open up more possibilities (higher entropy), so the *excess* surprise (S₂) grows less dramatically. A rare word in a rich context may still feel "earned."

2. **For long poems, TTR and S₂ are orthogonal (r = −0.04).** The Straussian gap is not a property of vocabulary breadth — it's a property of strategic choice. A poet selects *when* to deviate, not how many different words to use.

3. **For short imagist poems, TTR and S₂ co-occur.** Short, compressed poems (Pound, Williams, Brooks) have high TTR because they can't afford repetition. These poems *also* tend to have high S₂ because their formal constraint demands that every word carry maximum weight.

4. **Anaphoric repetition is a Straussian mechanism.** Low-TTR poems with positive S₂ (Long Soldier, Ashbery's "Paradoxes and Oxymorons") use repetition as a scaffold that absorbs GPT-2's predictive capacity, then deploys surprise within the repetitive structure.

---

## Next Steps

- Test the anaphora hypothesis on more anaphoric poems (Whitman's "Out of the Cradle", Blake's "Songs of Innocence/Experience", parallelism in Psalms)
- Separate TTR into *function word TTR* vs *content word TTR* — are repeated function words (the/of/a) doing different work than repeated content words?
- Build a "repetition S₂ amplifier" metric: for each repeated word, compare S₂ on first occurrence vs. second/third — does repetition make a word *more* or *less* surprising over time?
- Test Long Soldier's "Whereas" against the full poem (not just excerpt) to see if the anaphoric pattern accumulates S₂ over the course of the poem
