# Vocabulary Richness vs S₂ Profiles

**Date:** 2026-11-03  
**Experiment:** `experiments/vocab_richness.py`  
**Research Question:** Type-token ratio (TTR) vs S₂ — do poets with richer vocabulary have different information signatures? Does lexical repetition suppress or amplify surprise?

---

## Method

For each English-language poem in the corpus (excluding prose controls), computed:
- **TTR** (type-token ratio): unique word types / total word tokens (0 = fully repetitive, 1 = all unique)
- **Hapax ratio**: words appearing exactly once / total tokens
- **Repeat ratio**: fraction of tokens that recur in the poem

Correlated these with S₂ metrics from the precomputed corpus.

**Sample:** 391 poems (after excluding very short texts with < 5 words)

---

## Correlations (Pearson r)

| Metric Pair | r |
|---|---|
| TTR vs avg_S₂ | **+0.347** |
| TTR vs avg_surprisal | **+0.665** |
| TTR vs avg_entropy | **+0.558** |
| TTR vs pos_S₂_ratio | **+0.534** |
| repeat_ratio vs avg_S₂ | **-0.372** |

**Interpretation:**
- Lexical richness (high TTR) is a strong predictor of overall surprisal (+0.665) and proportion of positive-S₂ tokens (+0.534)
- The correlation with avg_S₂ itself is positive but more modest (+0.347) — vocabulary richness drives *surprisal* more than it drives the *gap between surprisal and entropy*
- Repetition (high repeat_ratio) is negatively correlated with avg_S₂ (r = -0.372) — but with an important exception (see below)

---

## Quartile Analysis

| Group | n | Avg TTR | Avg S₂ | Avg Surprisal | Avg Entropy | Pos-S₂ Ratio |
|---|---|---|---|---|---|---|
| Bottom 25% (most repetitive) | 97 | 0.524 | +0.052 | 5.326 | 5.274 | 0.310 |
| Top 25% (lexically richest) | 98 | 0.890 | +0.821 | 7.252 | 6.432 | 0.402 |
| **Gap** | | | **+0.769** | **+1.926** | **+1.158** | **+0.092** |

**Lexically rich poems have:**
- 0.769 bits more avg S₂ (massive effect)
- 1.926 bits more avg surprisal
- 1.158 bits more avg entropy
- 9.2 percentage points more positive-S₂ tokens

The surprisal gap (1.926 bits) is much larger than the S₂ gap (0.769 bits) — rich-vocabulary poems are surprising *and* high-entropy, not just surprising. High vocabulary = high surprisal + high entropy, but the entropy partly "explains" the surprisal.

---

## Spotlight: Most Repetitive vs. Most Lexically Rich

### 5 Most Repetitive Poems (lowest TTR)

| TTR | Avg S₂ | Repeat % | Author | Title |
|---|---|---|---|---|
| 0.119 | **+0.806** | 95% | Emmett Williams | For Spacious Skies |
| 0.133 | -0.166 | 93% | Eugen Gomringer | silencio |
| 0.234 | +0.153 | 91% | Gertrude Stein | If I Told Him… |
| 0.278 | -0.640 | 85% | Arthur Symons | The Wanderer's Litany |
| 0.290 | -0.212 | 83% | Anonymous (KJV) | Psalm 136 |

### 5 Most Lexically Rich Poems (highest TTR = 1.000, all hapax)

| TTR | Avg S₂ | Author | Title | Words |
|---|---|---|---|---|
| 1.000 | +3.594 | William Carlos Williams | The Red Wheelbarrow | 15 |
| 1.000 | +4.156 | Chiyo-ni | Morning Glory | 9 |
| 1.000 | +3.258 | Lorine Niedecker | Lorine's Work | 19 |
| 1.000 | +3.890 | E.E. Cummings | l(a | 9 |
| 1.000 | +2.031 | Richard Wright | Nobody | 11 |

---

## The Emmett Williams Anomaly

Emmett Williams' "For Spacious Skies" (TTR = 0.119, repeat ratio = 0.95) is an extreme outlier: the *most repetitive* poem in the corpus but with **+0.806 avg S₂** — well above the bottom-quartile average of +0.052.

This poem is a concrete poetry piece built almost entirely from the phrase "for spacious skies" repeated with minimal variation. The model expects the exact repetition, but the subtle departures (reordering, omitting words, inserting breaks) catch GPT-2 off guard. This suggests:

> **Repetition can create deviation**: in a highly repetitive context, the model's probability mass collapses onto the exact repetition pattern. Any departure, however small, yields disproportionately large S₂.

This is the inverse of the general trend — and reveals that TTR alone does not capture surprise. What matters is the *predictability of the next token given the specific context*, not aggregate vocabulary diversity.

---

## Length Confound

Short poems (haiku, imagist) tend to have TTR = 1.000 simply because they are too short for repetition to occur. The TTR vs S₂ correlation is partly a **length effect**: short poems have high TTR and high S₂ simply because every word is forced to carry maximum information load in a tight form.

To check: among poems with > 100 words, the TTR range collapses (0.3–0.7), and the S₂ correlation should weaken. This would separate genuine vocabulary strategy from form-length confound.

---

## Key Findings

1. **Lexical richness predicts surprisal more strongly than S₂**: TTR correlates with avg_surprisal at r = +0.665 but with avg_S₂ at only r = +0.347. Rich vocabulary raises both surprisal and entropy; the Straussian gap (S₂) is somewhat entropy-compensated.

2. **The quartile gap is huge**: richest-TTR vs. most-repetitive poems differ by **0.77 S₂ bits** on average — roughly the same magnitude as the poetry-vs-prose gap in some experiments.

3. **Repetition with strategic deviation beats flat vocabulary**: Emmett Williams' concrete poetry (TTR = 0.12) achieves +0.806 avg S₂ by using the exact repetition pattern as a high-confidence baseline, then violating it minimally. The *structure of repetition* creates surprise potential.

4. **Imagist / objectivist / haiku poetry clusters at TTR = 1.000**: extreme brevity + all-hapax vocabulary = maximum individual token pressure = highest S₂ values in the corpus. This is partly a length/form confound, not pure vocabulary strategy.

5. **Repetitive forms (litanies, anaphora, ballads, biblical parallelism) score low avg S₂** despite poetic intent — the model simply learns the pattern and is not surprised by continuations, regardless of meaning.

---

## Suggested Next Steps

- Partial correlation: TTR vs S₂ controlling for poem length — separates form effect from vocabulary strategy
- Compare TTR within a single poet's work across poems of similar length (e.g., Whitman's different poems) — holds form constant
- Test whether hapax ratio (rather than TTR) is a better predictor when poems are long enough for repetition to naturally occur
- Identify the "surprise leverage" of repetition: at what repeat_ratio does the model's certainty about the next repetition create the conditions for maximal deviation payoff?
