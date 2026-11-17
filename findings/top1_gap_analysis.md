# The Top-1 Gap: A New Metric for Poetic Deviation

**Date:** 2026-11-17  
**Experiment:** `experiments/top1_gap_analysis.py`  
**Results:** `results/top1_gap_analysis.json`  
**Corpus:** 431 poems, 55,822 English artifact-free tokens (p_newline < 0.9 filter applied)

---

## Motivation

S₂ = surprisal − entropy asks: *was this token more surprising than the model's overall uncertainty warranted?* But S₂ uses entropy — the average uncertainty — as its baseline. There is a second natural baseline: the model's **single best prediction** (rank-1 token).

The **Top-1 Gap (T1G)** = surprisal(actual) − surprisal(top-1) = log₂(prob_top1 / prob_actual)

This measures: *how many extra bits did the actual choice cost compared to the model's favorite?*

The relationship between T1G and S₂ is:

> **T1G − S₂ = entropy − surprisal(top-1)** = "top-1 concentration advantage"

This residual captures how much more probable the top-1 prediction was than the entropy average. High residual = the model had ONE dominant prediction but overall high uncertainty (a "peaked" distribution). The residual is distinct from either S₂ or T1G alone.

---

## Global Finding: T1G Tracks S₂ but Reveals a Hidden Population

| Corpus | Mean T1G | Mean S₂ | Mean Residual |
|---|---|---|---|
| Poetry (all) | **3.397 bits** | −0.388 | **3.785 bits** |
| Prose (control) | **1.543 bits** | −1.721 | **3.264 bits** |
| **Poetry−Prose gap** | **+1.854 bits** | +1.333 bits | +0.521 bits |

T1G and S₂ are strongly correlated: **r = 0.91** (n = 55,822 artifact-free tokens).

However, the 9% residual variance captures something S₂ misses — and that 9% contains the most theoretically interesting cases.

---

## T1G Distribution: The "Zero-Gap" Majority

| T1G Range | n | % | Mean S₂ |
|---|---|---|---|
| **Zero gap** (chose top-1, T1G < 0.1) | 18,159 | **32.5%** | −2.899 |
| Tiny gap (< 1 bit) | 4,297 | 7.7% | −3.099 |
| Small gap (1–3 bits) | 9,227 | 16.5% | −2.050 |
| Medium gap (3–6 bits) | 11,203 | 20.1% | 0.003 |
| **Large gap** (> 6 bits) | 12,936 | **23.2%** | +4.566 |

**32.5% of all tokens in the corpus chose the model's top-1 prediction.** These tokens have deeply negative S₂ (−2.899), confirming that conformist choices are not just "average" — they represent systematic under-surprise relative to entropy.

The **inflection point** is around 3–6 bits: tokens with T1G in this range have mean S₂ ≈ 0 (the neutral transition). Below 3 bits: negative S₂ (conformist). Above 3 bits: positive S₂ (deviant).

---

## The Four Quadrants of Poetic Deviation

Using T1G threshold = 3.0 bits and S₂ threshold = 1.0 bit:

| Quadrant | Description | % of Tokens | Interpretation |
|---|---|---|---|
| **Q3: Low T1G + Low S₂** | Conformist majority | **56.6%** | Chose near top-1, within entropy |
| **Q1: High T1G + High S₂** | Maximum Straussian | **26.3%** | Far from top-1 AND above entropy |
| **Q4: High T1G + Low S₂** | Second-tier deviants | **17.0%** | Far from top-1, but below entropy |
| **Q2: Low T1G + High S₂** | (Near-empty) | **0.1%** | Mathematically near-impossible |

**The surprising finding is Q4 (17% of tokens).**

Q4 tokens are "second-tier deviants": the poet avoided the model's top prediction but chose something that ended up MORE probable than entropy would predict (S₂ < 1). These are not random choices — they're the second or third most probable option, chosen over the dominant first choice.

**Why is Q2 near-empty?** If T1G is small (actual ≈ top-1 in probability) but S₂ is high (surprisal > entropy), then entropy < surprisal(actual) ≈ surprisal(top-1). But a model with low entropy by definition concentrates most probability on a few tokens — the top-1 would then have high probability (low surprisal), making T1G large. The Q2 corner is self-contradictory and topologically excluded.

---

## Era Analysis: Two Deviation Strategies

### By Mean T1G (top 10 eras)

| Era | n (tokens) | Mean T1G | Mean S₂ | Residual | Strategy |
|---|---|---|---|---|---|
| clerihew | 1,048 | **4.715** | +0.256 | 4.459 | Mixed |
| deep_image | 231 | **4.280** | +0.066 | 4.214 | Q1-dominant |
| haiku | 1,015 | **4.151** | −0.163 | 4.314 | **Q4-dominant** |
| ancient | 426 | 4.086 | −0.203 | 4.288 | Q4-dominant |
| persian | 230 | 3.967 | −0.235 | 4.202 | Q4-dominant |
| war_poetry | 348 | 3.894 | −0.375 | 4.270 | Q4-dominant |
| confessional | 740 | 3.848 | −0.307 | 4.154 | Q4/Q1 |
| german_expressionist | 824 | 3.766 | −0.163 | 3.929 | Q4-dominant |
| elegy | 965 | 3.741 | −0.493 | 4.234 | Q4-dominant |
| victorian | 3,802 | 3.737 | −0.323 | 4.060 | Q4-dominant |

**Key pattern:** Most eras with high mean T1G have NEGATIVE mean S₂. They systematically avoid the top prediction, but they DO NOT choose below the entropy baseline — they choose from the "second tier" of predictions.

### By Q1 Rate (% High T1G + High S₂)

| Era | Q1 Rate | Interpretation |
|---|---|---|
| deep_image | **37.7%** | Maximum Straussian strategy |
| clerihew | 35.5% | Ludic precision deviation |
| persian | 32.5% | Ghazal: formal + semantic surprise |
| confessional | 32.2% | Intimate vocabulary rupture |
| ancient | 31.4% | Translation artifacts? |
| haiku | 30.1% | Moderate Q1; majority in Q4 |
| mid_century | 30.0% | Compressed lyric |
| imagist | 29.6% | Precision image |

**Deep image poetry** (Bly, Kinnell, Wright) achieves the highest rate of Q1 deviation — maximum Straussian: choosing against the dominant prediction AND choosing something that exceeds entropy. This is consistent with the deep image aesthetic of "leaping" across expected semantic fields.

---

## The Core Typology: Two Routes to Deviation

The quadrant analysis reveals that high T1G does **not** reliably predict high S₂. Instead, two distinct deviation strategies emerge:

### Route 1: "Second-Tier" Deviation (Q4-dominant eras)
*High T1G, Low/Negative S₂: Haiku, Victorian, War poetry, Elegy, Ancient*

The model had one dominant prediction; the poet chose a runner-up. The choice is not random (S₂ ≤ 0 means it landed above the entropy average in probability), but it's not the "obvious" choice either. These poets navigate between the dominant prediction and the median — the word the model half-expected but didn't front-run.

> *The haiku poet avoids the dominant prediction but chooses within the model's secondary expectations — an unexpected-but-apt move.*

### Route 2: "Full Straussian" Deviation (Q1-dominant eras)
*High T1G, High S₂: Deep image, Clerihew, Confessional, Persian ghazal*

The model had one dominant prediction; the poet chose something that also exceeded the entropy average. These choices are doubly unexpected: the wrong choice AND an improbable one. This is the maximal form of the Straussian gap.

> *The confessional poet not only avoids the expected word but chooses from the low-probability tail — the "wrong" answer to a question the model felt confident about.*

---

## The Residual as a Quality Signal

All eras show residuals of approximately **4.0–4.5 bits**, meaning the top-1 prediction consistently holds about 2⁴ = 16× more probability than the "entropy-average" token. This is remarkably consistent:

- **Residual ≈ 4** means: "the model almost always has one dominant guess, and that guess is about 16× more likely than a random draw from the entropy distribution."
- Poets who ignore that dominant guess (high T1G) are overcoming a **16-to-1 pull** at every step.

The near-constant residual across all eras suggests this is a property of GPT-2's architecture when processing literary text, not a property of specific poetic styles.

---

## Highest T1G Tokens in the Corpus

| Token | T1G | S₂ | Residual | Era | Author |
|---|---|---|---|---|---|
| 'under' | 19.88 | 19.99 | −0.11 | beat | Ferlinghetti |
| 'torches' | 19.87 | 19.69 | +0.18 | ekphrastic | Browning |
| 'list' | 19.82 | 19.48 | +0.34 | early_modern | Wyatt |
| 'ashes' | 19.63 | 18.51 | +1.12 | ballad | Traditional |
| 'onward' | 19.57 | 18.04 | +1.53 | victorian | Tennyson |
| 'Bon' | 19.53 | 17.45 | +2.08 | ballad | Traditional |

The highest T1G tokens also have near-maximal S₂, confirming they fall in Q1. The residuals here range from −0.11 to +2.59, with small residuals meaning: the model's top prediction and the actual choice were both extremely low-probability (a nearly flat distribution at that position).

---

## Summary: What T1G Adds to the Picture

| Measure | Baseline | Captures |
|---|---|---|
| S₂ | Entropy (average uncertainty) | How much more surprising than typical? |
| **T1G** | **Top-1 probability** | **How far from the dominant guess?** |
| Residual | — | How peaked was the prediction? (top-1 concentration) |

T1G adds precision to S₂: it distinguishes tokens that are "above entropy" because the dominant prediction was very low-probability (high residual) from tokens that overcame a genuinely confident prediction (low residual). Two tokens with identical S₂ can have very different T1G values depending on whether the dominant prediction was clear or diffuse.

The **Q4 zone** (17% of tokens) is T1G's key contribution: a large population of "second-tier deviants" that S₂ labels as conformist (S₂ < 1) but T1G reveals as consistently avoiding the dominant prediction. These tokens are systematically interesting in traditions like haiku, Victorian verse, and elegy — forms where the aesthetic may require *avoiding the cliché* (top-1) without reaching for the *obscure* (above entropy).

---

## Suggested Next Steps

1. **Token-level T1G by rank**: Does T1G cluster at specific rank positions (e.g., 2nd, 3rd most probable)? Are Q4 tokens mostly rank=2–5?
2. **Residual as form signal**: Is the residual ≈ 4 bits constant or does it vary by poem length, era, or genre?
3. **Q4 vocabulary**: What semantic field do "second-tier deviants" occupy? Are they concrete nouns that GPT-2 would have predicted but didn't lead with?
4. **Combine with True Straussian Score**: The existing `entropy_conditioned_deviation.md` measures Q1-equivalent at low-entropy positions. T1G generalizes this to ALL positions.
5. **T1G volatility**: Within a poem, does T1G fluctuate more or less than S₂? A high-variance T1G poem might be one where the poet alternately submits to and departs from dominant predictions.
