# Spike Height Gradient: Does Larger Surprise Predict Deeper Post-Valley?

**Date:** 2026-10-22  
**Experiment:** `experiments/spike_height_gradient.py` → `results/spike_height_gradient.json`  
**Corpus:** 321 texts, 5,971 spikes (S₂ ≥ 3.0, artifact-free tokens only)  
**Extends:** `findings/surprise_asymmetry.md` (suggested this test explicitly)

---

## Research Question

`surprise_asymmetry.md` established that after a surprise spike, the poem becomes more conformist — the post-spike valley is 36% deeper than the pre-spike setup. It proposed the mechanism: "an unusual word opens a narrower set of natural continuations" (semantic anchoring). This experiment tests the direct prediction of that mechanism:

**If high-S₂ tokens anchor context more strongly, larger spikes should produce deeper post-valleys.**

---

## Spike Population

| Tier     | S₂ Range | N spikes | Mean spike S₂ | Poem baseline |
|----------|----------|----------|----------------|---------------|
| Low      | 3–6      | 3,547    | 4.32           | −0.362        |
| Medium   | 6–12     | 2,139    | 8.10           | −0.306        |
| High     | 12–20    | 269      | 14.32          | −0.214        |
| Extreme  | 20+      | 16       | 24.03          | −0.107        |

Note: extreme-tier poems have **higher poem baselines** (less negative = more surprising on average). High-spike poems are not random draws from the corpus — they are already the more surprise-rich texts.

---

## Core Finding: The Hypothesis Is Refuted

**Pearson r(spike_S₂, post_AUC) = 0.029** (n=5,854 spikes). 

There is essentially **no correlation** between how surprising a token is and how deep the subsequent conformity valley is. Larger spikes do not produce deeper post-valleys.

---

## Non-Linear Pattern by Tier

Post-valley depth at lag +1 (immediate aftermath):

| Tier    | Lag +1 S₂ | Lag +2 S₂ | Post AUC | Pre AUC | Ratio |
|---------|-----------|-----------|----------|---------|-------|
| Low     | **−0.516**| −0.432    | −3.018   | −2.359  | 1.279 |
| Medium  | **−0.227**| −0.305    | −2.422   | −1.392  | **1.741** |
| High    | **+0.078**| −0.954    | −2.645   | −2.096  | 1.262 |
| Extreme | **−0.530**| +0.173    | **+1.708** | +0.333 | **5.133** |

The counterintuitive finding: **low spikes produce the deepest immediate post-valleys (−0.516), while high spikes produce near-zero lag +1 (−0.078 → +0.078)**. Medium spikes show the strongest asymmetry between pre and post windows (ratio = 1.741).

---

## Binned Regression: The Non-Linear Shape

Examining lag +1 S₂ across deciles of spike height:

| Decile | Spike S₂ range  | Mean spike S₂ | Mean lag +1 S₂ |
|--------|-----------------|----------------|-----------------|
| 1      | [3.0 – 3.4]     | 3.18           | **−0.531**      |
| 2      | [3.4 – 3.8]     | 3.57           | **−0.596**      |
| 3      | [3.8 – 4.2]     | 4.01           | **−0.429**      |
| 4      | [4.3 – 4.8]     | 4.52           | **−0.420**      |
| 5      | [4.8 – 5.3]     | 5.06           | **−0.545**      |
| 6      | [5.3 – 6.0]     | 5.69           | **−0.551**      |
| 7      | [6.0 – 6.9]     | 6.45           | **−0.212**      |
| 8      | [6.9 – 8.1]     | 7.47           | **−0.059**      |
| 9      | [8.1 – 10.1]    | 9.00           | **−0.241**      |
| 10     | [10.1 – 25.6]   | 12.66          | **−0.273**      |

The pattern is **non-linear**: post-valley depth is roughly flat for low spikes (bins 1–6), then shallows for mid-range spikes (bins 7–8, S₂ ≈ 6–8), then returns to moderate negative for high spikes. This inverse-U shape at lag +1 contradicts the anchoring hypothesis in its simplest form.

---

## Three Regimes

The data reveals three distinct spike-behavior regimes:

### Regime 1: Low spikes (S₂ 3–6) — Embedded surprise
- Deepest immediate post-valley (lag +1 = −0.516)
- Deep pre-setup too (lag +1 pre = −0.466)
- Both windows well below baseline
- **Interpretation**: Low spikes are "conventional surprises" — they occur in constrained local contexts. The surrounding tokens are predictable; the spike is embedded in a predictable stream. GPT-2 recovers quickly with high confidence.

### Regime 2: Medium spikes (S₂ 6–12) — Asymmetric surprise  
- Moderate post-valley but highest asymmetry ratio (1.741)
- Near-zero pre-setup (lag +1 pre = −0.085)
- **Interpretation**: Medium spikes arrive with little preparation and leave the poem in a modestly deeper conformity well. This is the "classic" Straussian gap pattern — the poet deviates without warning, then returns to convention.

### Regime 3: High/extreme spikes (S₂ 12+) — Cascading surprise
- Shallow or positive post-valley at lag +1 (high: +0.078; extreme: −0.530 but noisy)
- Extreme tier has POSITIVE pre and post AUC (+0.333, +1.708)
- **Interpretation**: Very large spikes are not isolated events. They occur in poems already running at elevated surprise, and they are often followed by more surprising tokens (cascade architecture). The extreme spike does not anchor context in a narrow direction — it opens anomalous territory.

---

## The Extreme Tier: Sustained Elevation

The 16 extreme spikes (S₂ > 20) come from a narrow set of poets:

| Token         | S₂     | Post AUC | Author                  | Era            |
|---------------|--------|----------|-------------------------|----------------|
| ' gro'        | 36.66  | +8.711   | Lawrence Ferlinghetti   | beat           |
| ' climbs'     | 28.25  | −4.313   | Lawrence Ferlinghetti   | beat           |
| ' pour'       | 27.73  | +28.132  | Charles Bukowski        | spoken_word    |
| ' glass'      | 25.63  | +28.841  | Marianne Moore          | modernist      |
| ' whenever'   | 25.60  | −1.549   | Lawrence Ferlinghetti   | beat           |
| ' Pra'        | 22.09  | −1.597   | Gerard Manley Hopkins   | victorian      |

Ferlinghetti appears **three times** in the top 5. The post-AUC for Bukowski and Moore extreme spikes are **positive** — meaning the tokens after those spikes are themselves surprising. This is the cascade pattern documented in `surprise_decay_curves.md` for Ginsberg (who does not appear here because his corpus doesn't have single tokens this extreme, but rather sustained cascades).

Note: many extreme spike tokens are **subword fragments** (' gro', ' Pra', ' Gu', ' p') — cases where GPT-2's tokenizer splits an unusual word and the continuation is fully determined once the first fragment appears. The anomaly is real (GPT-2 was maximally surprised) but it generates artifactual post-AUC behavior because the continuations are over-determined.

---

## Revised Understanding of Semantic Anchoring

The anchoring mechanism from `surprise_asymmetry.md` holds for **medium spikes** (the typical case) but inverts for extremes. A more nuanced model:

| Spike level | GPT-2 response after spike | Post-valley | Mechanism |
|-------------|---------------------------|-------------|-----------|
| Low (3–6)   | High confidence           | Deep (−0.52) | Conventional context reasserts immediately |
| Medium (6–12)| Moderate confidence       | Moderate (−0.23) | Partial anchoring; moderate constraints on next token |
| High (12–20)| Uncertain (H ≈ 6.2)       | Near zero (+0.08) | Anomalous token disrupts model's schema entirely |
| Extreme (20+)| Very uncertain            | Often positive | Model enters unknown territory; subsequent tokens also surprising |

The "semantic anchor" metaphor works only for the middling cases. Truly extreme deviations do not anchor context narrowly — they blow it open.

---

## Suggested Next Steps

1. **Control for subword artifacts**: Filter extreme spikes where the token is a subword fragment (starts with ' ' but length < 4 chars, or contains no vowels). Re-test the non-linearity.
2. **Entropy profile by tier**: The post-lag +1 entropy column from `surprise_asymmetry.md` showed 5.824 (GPT-2 becomes MORE confident after a spike). Test whether this drops at the high and extreme tiers (i.e., GPT-2 becomes less confident after very large spikes — the anchor breaks).
3. **Genre interaction**: Does the three-regime pattern hold within eras? Is the low-spike embedded pattern more common in formal/metrical poetry and the cascade pattern in free verse?
4. **Spike clustering**: Are extreme spikes more likely to be adjacent to other spikes (cascade) vs. isolated? Count spike-to-spike distances by tier.
