# Alternative Space Volatility: How Stable Is GPT-2's Prediction Window?

**Date:** 2026-11-25  
**Experiment:** `experiments/alternative_space_volatility.py` → `results/alternative_space_volatility.json`  
**Corpus:** 443 poems, 54,134 token transitions (artifact-free, non-whitespace)  
**Research Question:** How much does GPT-2's top-10 prediction set change between consecutive token positions? Does prediction-space stability or volatility predict when poets make surprising choices?

---

## Background

Previous work established *what* GPT-2 predicts at each token and whether the poet follows. This experiment asks a different question: **does the prediction space itself remain stable across consecutive positions, or does it fluctuate rapidly?**

We measure this with **Jaccard similarity** between the top-10 alternatives at position t and position t+1. Jaccard = 0 means no alternative appears in both windows; Jaccard = 1 means identical windows.

---

## Finding 1: The Prediction Window Is Extraordinarily Volatile

| Metric | Value |
|---|---|
| Mean Jaccard similarity | **0.087** |
| Transitions with zero overlap (Jaccard = 0) | **46.0%** |
| Transitions with full overlap (Jaccard = 1) | **< 0.1%** |
| Token-level r(Jaccard, S₂) | **−0.0001** |
| Poem-level r(avg Jaccard, avg S₂) | **+0.214** |

GPT-2's prediction window shares only **8.7% of its vocabulary** between consecutive positions on average. Nearly half of all consecutive positions have **zero alternatives in common** — the model's "vocabulary of expectation" is completely reshuffled at every other step in a poem.

There is effectively **no linear correlation at the token level** between prediction-space stability and S₂. Stability is not simply equivalent to conformity pressure.

However, at the **poem level**, more stable prediction spaces positively correlate with higher average S₂ (r = 0.214). Poems where the model repeatedly predicts from the same vocabulary tend to generate *more* poetic surprise — counterintuitive, but explained by Finding 3 below.

---

## Finding 2: A U-Shaped Relationship — Stability Polarizes Poetic Choice

| S₂ Band | n | Mean Jaccard |
|---|---|---|
| Very low (< −3) | 12,162 | **0.0949** |
| Low (−3 to −1) | 15,159 | 0.0873 |
| **Neutral (−1 to 1)** | 11,424 | **0.0760** ← *lowest* |
| High (1 to 3) | 6,245 | 0.0869 |
| Very high (3–5) | 4,013 | 0.0879 |
| **Extreme (5+)** | 5,131 | **0.0956** ← *highest* |

The relationship between prediction-space stability and S₂ is **U-shaped**: tokens with *neutral* S₂ (−1 to 1) follow the MOST volatile prediction spaces (Jaccard = 0.076), while tokens at the extremes — both very low S₂ AND very high S₂ — follow MORE STABLE prediction spaces (~0.095).

**Interpretation: Volatility Creates Middling Conformity.**
- When the prediction space is stable, the model is locked onto a coherent vocabulary. The poet faces a binary choice: follow the groove (very low S₂) or break it (very high S₂). Both extremes are easier to achieve from a stable baseline.
- When the prediction space is volatile, there's no coherent expectation to either conform to or violate. The poet's choices drift toward the neutral middle — neither obviously surprising nor obviously expected, because the model never committed to a prediction.

---

## Finding 3: The Stability-Surprise Paradox

Poems with more stable prediction spaces tend to have higher avg S₂ (r = 0.214). The most stable poems include:

| Avg Jaccard | Avg S₂ | Author | Title |
|---|---|---|---|
| **0.180** | +0.218 | Gertrude Stein | If I Told Him |
| **0.164** | +1.237 | Robert Creeley | The Language |
| **0.161** | −0.608 | Gertrude Stein | Susie Asado |
| **0.154** | +0.685 | Robert Creeley | I Know a Man |
| **0.149** | +1.901 | Synthetic (concrete) | Diamond Concrete Poem |
| **0.141** | −0.597 | Wisława Szymborska | Pi |
| **0.135** | +0.566 | Emily Dickinson | I heard a Fly buzz |

**The paradox explained:** Stein and Creeley both use highly repetitive, constrained vocabulary. GPT-2 "learns" this vocabulary and stabilizes its predictions around a narrow set of words. When the poet then deploys an unexpected word, the violation is registered as more surprising precisely *because* the prediction space was coherent and stable. High-S₂ effect requires a stable target to miss.

---

## Finding 4: Temporal Arc — Prediction Spaces Stabilize Across Poems

| Poem Decile | Mean Jaccard | Mean S₂ |
|---|---|---|
| 0 (opening) | 0.0812 | **+0.203** |
| 1 | 0.0834 | −0.205 |
| 2 | 0.0890 | −0.139 |
| 3 | 0.0890 | −0.297 |
| 4 | 0.0870 | −0.324 |
| 5 | 0.0877 | −0.339 |
| 6 | 0.0865 | −0.394 |
| 7 | 0.0877 | −0.309 |
| 8 | 0.0912 | −0.320 |
| 9 (ending) | 0.0911 | **−0.481** |

As a poem progresses:
1. **Prediction spaces stabilize** (Jaccard increases from 0.081 to 0.091): GPT-2 "learns" the poem's vocabulary as it accumulates in context, and starts recycling the same alternative words.
2. **S₂ drops** (from +0.203 at opening to −0.481 at ending): the poet increasingly works within the vocabulary the poem has established.

This is the information-theoretic signature of **poetic settling**: wild opening territory narrows into an established semantic world. The poem teaches both the reader and the model what vocabulary to expect — and then delivers it.

---

## Finding 5: Era Volatility Profiles

Sorted by mean Jaccard (prediction-space stability):

| Era | Jaccard | Avg S₂ | Zero-overlap% | Stable% |
|---|---|---|---|---|
| **Most Volatile Eras** | | | | |
| social_media_poetry | 0.053 | −0.882 | 62.1% | 3.5% |
| triolet | 0.057 | −0.624 | 52.1% | 0.9% |
| deep_image | 0.061 | +0.272 | 40.0% | 1.8% |
| concrete | 0.062 | −0.378 | 53.1% | 4.3% |
| japanese_classical | 0.064 | −0.546 | 59.2% | 8.2% |
| limerick | 0.067 | −0.637 | 56.6% | 4.8% |
| **Most Stable Eras** | | | | |
| 18th_century | 0.107 | −0.184 | 38.8% | 10.8% |
| ancient | 0.109 | −0.054 | 39.9% | 10.8% |
| rondeau | 0.124 | −0.151 | 40.5% | 13.8% |

**Pattern:** Experimental modern forms (social media poetry, concrete poetry, deep image) are the most volatile; ancient texts and 18th-century neoclassical poetry are the most stable.

Paradoxically, the **high-S₂ eras** (beat, german_modernist, clerihew) occupy the **middle range** of volatility (Jaccard 0.072–0.099). They are neither the most stable nor the most volatile — suggesting that high avg S₂ emerges not from extreme volatility or stability, but from a productive middle zone where the model has *some* expectations to violate but those expectations aren't so entrenched as to suppress surprise.

---

## Finding 6: Extreme Volatility and Extreme Stability Identified

**Most volatile poems** (prediction space reshuffled most rapidly):

| Jaccard | S₂ | Author | Title |
|---|---|---|---|
| 0.006 | −1.138 | Ezra Pound | In a Station of the Metro |
| 0.018 | −0.631 | Eugen Gomringer | silencio |
| 0.023 | −0.542 | Joy Harjo | She Had Some Horses |
| 0.026 | +0.686 | Synthetic | James Joyce (clerihew) |
| 0.030 | −0.515 | André Breton | Free Union (excerpt) |

Pound's imagist "In a Station of the Metro" is the single most volatile poem in the corpus (Jaccard = 0.006). Its radical semantic juxtaposition ("apparition" / "faces in the crowd" / "petals on a wet, black bough") cycles through completely non-overlapping prediction spaces at every step. Notably its avg S₂ is NEGATIVE (−1.138): the extreme volatility doesn't translate into positive S₂ because the model never builds expectations strong enough to violate forcefully.

---

## Synthesis: The Stability-Volatility Spectrum

| Property | Stable Prediction Space | Volatile Prediction Space |
|---|---|---|
| Jaccard | High (>0.10) | Low (<0.07) |
| Typical eras | Ancient, 18th century, rondeau | Social media, concrete, imagist |
| Effect on S₂ | Polarizes: very high or very low | Flattens: neutral conformity |
| Poem-level S₂ | Positively correlated | Negatively correlated |
| Temporal position | End of poems | Beginning of poems |
| Example poets | Stein, Creeley, Dickinson | Pound, Gomringer, Breton |

---

## Implications

1. **Poetic surprise requires a stable target.** A volatile prediction space provides nothing coherent to violate. High-impact S₂ events (the "Straussian gap") are more possible when the model has converged on strong expectations.

2. **Opening volatility is a structural feature, not a flaw.** Poems open in a volatile prediction space and then narrow to stability. This mirrors the reader's experience: initial disorientation gives way to familiarity with the poem's world.

3. **Experimentalism isn't always informationally surprising.** The most volatile eras (social media, concrete, imagist) often have *negative* avg S₂ after artifact removal. Radical juxtaposition can scatter predictions without generating positive S₂ — it spreads the fog rather than making sharp ambushes.

---

## Next Steps

- Measure volatility separately for punctuation-free tokens to isolate semantic vs. syntactic contributions to Jaccard.
- Track whether high-Jaccard "stable grooves" precede the highest-S₂ spikes (testing whether the ambush setup requires a stable prediction space).
- Correlate poem-level volatility with other measures: avg sentence length, type-token ratio, formal meter.
