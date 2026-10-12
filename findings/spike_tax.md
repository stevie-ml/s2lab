# The Spike Tax: Does Extreme S2 Create a Recovery Period?

**Date:** 2026-10-12  
**Experiment:** `experiments/spike_tax.py`  
**Results:** `results/spike_tax.json`  
**Corpus:** 235 poems analyzed (27,129 adjacent token pairs)  
**Builds on:** `surprise_economy_gini.md`, `s2_autocorrelation.md`

---

## Research Question

After a high-S2 token (extreme divergence from expectation), do subsequent tokens
show systematically lower S2 — a "recovery period" where the poet provides
predictable relief to re-anchor the reader?

**Two competing models:**
- **Spike Tax**: High surprise creates a local debt — next tokens are more predictable to compensate
- **Spike Freedom**: High surprise tokens are transitional moments that open up new possibility — next tokens can be surprising too

---

## Method

For each adjacent token pair (t, t+1) in artifact-free sequences:
1. **Global lag-1 correlation**: does S2(t) predict S2(t+1)?
2. **Spike recovery**: compare S2(t+1..t+3) after spike tokens (top 10% in their poem) vs. non-spike tokens
3. **Binned analysis**: mean S2(t+1) for each range of S2(t)
4. **Poem-level peak analysis**: for each poem's absolute maximum S2, trace the next 3 tokens

---

## Results

### 1. Global Lag-1 Correlation: Nearly Zero

| Statistic | Value |
|---|---|
| Pearson r | +0.017 |
| t-statistic | 2.72 |
| N pairs | 27,129 |

r = +0.017 is statistically significant but negligible in magnitude. Knowing the S2 at position t adds essentially no predictive power for S2 at t+1. **The sequence is near-Markovian at the token level.**

### 2. No Global Spike Tax

Comparing S2 of the k-th token after spike (top 10%) vs. non-spike tokens:

| Lag k | After spike | After non-spike | Δ |
|---|---|---|---|
| +1 | −0.349 | −0.394 | **+0.044** |
| +2 | −0.399 | −0.396 | −0.003 |
| +3 | −0.358 | −0.409 | **+0.051** |

Counter-intuitively, **tokens after spikes are very slightly LESS negative** than tokens after non-spikes (Δ = +0.044 at lag 1). There is no spike tax — high-S2 tokens do not force the next token into conventionality. If anything, spikes enable mildly positive neighboring tokens.

### 3. The Binned Analysis: Boring Begets Boring

The most striking finding is the **persistence of low S2**:

| S2(t) range | n | mean S2(t+1) | median S2(t+1) |
|---|---|---|---|
| < −5 (very boring) | 1,177 | −0.337 | −0.830 |
| −5 to −2 | 8,989 | **−0.495** | −1.324 |
| −2 to 0 | 7,762 | −0.329 | −0.916 |
| 0 to 2 | 3,561 | −0.355 | −1.220 |
| 2 to 5 | 3,220 | −0.405 | −1.321 |
| > 5 (very surprising) | 2,420 | **−0.245** | −1.199 |

**Key pattern**: the "−5 to −2" bin produces the most negative followers (mean −0.495). Very high S2 tokens (>5) produce the *least* negative followers (mean −0.245). The relationship is **non-monotonic and asymmetric**:
- Moderate negative S2 (−2 to 0) → moderate negative followers
- Very negative S2 (−5 to −2) → even more negative followers
- Positive S2 → slightly less negative followers
- Very positive S2 (>5) → least negative followers

This inverts the spike tax hypothesis: **boring tokens propagate boredom, while very surprising tokens open up the possibility space slightly.**

### 4. Poem-Level: Every Peak Falls

Analyzing the maximum-S2 token in each poem's aftermath:

| Position | Mean S2 |
|---|---|
| Peak token | +12.380 |
| Peak + 1 | −0.394 |
| Peak + 2 | **−0.570** |
| Peak + 3 | −0.130 |

- **100% of poem peaks are followed by lower S2** (trivial but confirms no "echo spike")
- **S2 deepens at t+2** before recovering — the valley is deepest one step after the immediate successor
- **Partial recovery by t+3** (−0.130 vs −0.570 at t+2)
- 67% of peaks >5 are followed by **negative** S2 at t+1

### 5. Two Distinct Post-Peak Patterns

The top-peak table reveals two strategies:

**Isolated Spike (crash pattern):**
| Poem | Peak S2 | Peak token | S2+1 | S2+2 |
|---|---|---|---|---|
| Buffalo Bill's (Cummings) | 19.03 | ' Jesus' | −8.01 | −6.08 |
| I felt a Funeral (Dickinson) | 18.90 | ' Fun' | −5.79 | −2.66 |
| The Congo (Lindsay) | 18.85 | 'lay' | −4.62 | −4.02 |
| One Art (Bishop) | 20.59 | ' badly' | −3.59 | −3.36 |

One extreme moment, then steep negative spiral. The peak is a **closed event** — isolated, singular.

**Cascade Spike (sustained pattern):**
| Poem | Peak S2 | Peak token | S2+1 | S2+2 |
|---|---|---|---|---|
| God's Grandeur (Hopkins) | 22.04 | ' shook' | +7.66 | +1.79 |
| Citizen (Rankine) | 18.16 | ' stacked' | +8.02 | −2.95 |
| Song of Myself (Whitman) | 20.40 | ' observing' | +2.86 | +4.79 |
| Komm in den totgesagten (George) | 23.39 | ' ferner' | +9.85 | −0.52 |

Here the peak launches adjacent high-S2 tokens — a **cascade**, not an isolated spike. The extreme deviation opens a space of possibility that persists for 1-2 tokens.

---

## Key Findings

### 1. No global spike tax
Spikes (top 10% S2) are not followed by significantly lower S2 than non-spikes. The hypothesis fails: extreme surprise does not deplete the surprise budget locally.

### 2. Boring begets boring
The −5 to −2 S2 bin shows the strongest downward pull on next-token S2 (−0.495). **The persistence of predictability** is more real than the persistence of surprise. Conventional sequences create local "gravity wells."

### 3. Extreme spikes release the gravity well
Tokens with S2 > 5 are followed by the least-negative S2 (−0.245). This suggests that extreme deviations **break the gravity well** of the preceding context, allowing the model's next-token distribution to spread out — higher entropy, which means the next choice is less constrained and slightly more positive in expectation.

### 4. Two-step valley
After a poem's peak, S2 dips and DEEPENS at t+2 before recovering at t+3. The "landing" takes longer than one step: the poet can't immediately return to neutral after an extreme moment; the context must re-stabilize over 2-3 tokens.

### 5. Isolated vs. cascade peaks
Some poets treat their peaks as singular events (Dickinson, Cummings): one moment of maximum departure, then immediate return to conventionality. Others use peaks as launchpads (Hopkins, Whitman): the extreme token licenses adjacent tokens to also deviate. This maps onto **different theories of poetic climax** — the pinpoint revelation vs. the sustained vision.

---

## Connection to Surprise Economy (Gini)

From `surprise_economy_gini.md`: high-mean-S2 poems have higher Gini inequality — their surprise is less uniformly distributed, concentrated in extreme spikes. But the spike tax finding shows there's no *local* mechanism enforcing this. The inequality isn't produced by individual spikes "consuming" surrounding tokens' surprise budget. It must arise from **compositional structure** — the poet clusters their high-S2 words into high-S2 passages, not through any local sequence mechanism.

---

## Suggested Next Steps

1. **Test "boring gravity wells"**: For sequences of consecutive negative-S2 tokens, plot mean length vs. mean S2 depth. Are deeper wells also wider?
2. **Cascade vs. isolated classifiers**: Can we predict which poems have isolated vs. cascade spikes from their era, author, or form? 
3. **The t+2 valley**: Why does the post-peak dip deepen at t+2? Is this a syntactic artifact (the peak word ends a phrase, t+1 begins a new phrase, and t+2 is mid-phrase where constraint is tightest)?
4. **Extreme-spike token grammar**: What part of speech are tokens with S2 > 10? Are they mostly nouns, verbs, or adjectives? Does the post-peak pattern differ by POS?
