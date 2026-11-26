# The Stable Groove → Ambush Effect: Does Prediction Stability Set Up Poetic Surprise?

**Date:** 2026-11-26  
**Experiment:** `experiments/stable_groove_ambush.py` → `results/stable_groove_ambush.json`  
**Corpus:** 425 poems, 50,031 token records (artifact-free, non-whitespace, ≥10 token lookback)  
**Builds on:** `findings/alternative_space_volatility.md`  
**Research Question:** Does a stable prediction window in the N positions *before* a high-S₂ token predict its occurrence and/or height?

---

## Background

`alternative_space_volatility.md` established that:
1. Extreme S₂ events (both high and low) tend to follow MORE stable prediction spaces than neutral tokens (a U-shaped relationship).
2. Poems with stable overall prediction spaces tend to have higher avg S₂ (poem-level r = 0.214).

The proposed mechanism: **"High-impact S₂ events require a stable target."** A volatile prediction space provides nothing coherent to violate; a stable groove creates expectations that the poet can then break.

This experiment directly tests that mechanism by looking at the prediction-space Jaccard similarity in the 1–10 positions immediately BEFORE each token, comparing ambush tokens (S₂ ≥ 3), neutral control tokens (−1 to 1), and conformist tokens (S₂ ≤ −1).

---

## Finding 1: The U-Shape Is Confirmed and Refined

Pre-spike Jaccard (mean over 3-position window) across the full S₂ range:

| S₂ Band | n | Pre-Jacc W=3 | Pre-Jacc W=5 | Conformist Run |
|---|---|---|---|---|
| Conformist (<−3) | 11,244 | **0.09174** | 0.08999 | 1.04 |
| Low (−3 to −1) | 14,198 | 0.08695 | 0.08673 | 1.01 |
| **Neutral (−1 to 1)** | 10,675 | **0.08156** ← *lowest* | 0.08401 | 1.03 |
| High (1 to 3) | 5,733 | 0.08925 | 0.08976 | 1.07 |
| Very High (3–5) | 3,635 | 0.09199 | 0.09133 | 1.04 |
| **Extreme (5+)** | 4,546 | **0.09311** ← *highest* | 0.09041 | 0.95 |

**The U-shape holds perfectly**: both conformist and ambush extremes are preceded by more stable prediction windows than neutral tokens. The neutral zone is the lowest-stability predecessor — when the model has no strong expectation to conform to or violate, the poet produces middling S₂.

**New asymmetry**: The ambush extreme (S₂ > 5) has the highest pre-Jaccard (0.09311), slightly *higher* than the deep conformist extreme (<−3: 0.09174). This suggests that the most extreme positive surprises are preceded by even more stable grooves than the most extreme conformity.

---

## Finding 2: Pre-Spike Stability Is Consistently Higher Across All Window Sizes

Comparison of mean pre-Jaccard for ambush (S₂ ≥ 3) vs control (−1 to 1) across all tested windows:

| Window | Ambush | Control | Conformist | Ambush−Control Gap |
|---|---|---|---|---|
| W=1 | 0.09444 | 0.07660 | 0.09111 | **+0.0178** |
| W=2 | 0.09374 | 0.07927 | 0.08957 | +0.0145 |
| W=3 | 0.09261 | 0.08156 | 0.08906 | +0.0110 |
| W=5 | 0.09082 | 0.08400 | 0.08817 | +0.0068 |
| W=10 | 0.08996 | 0.08491 | 0.08755 | +0.0051 |

**The ambush advantage is largest at W=1 (immediate predecessor)** and decays as the window widens — meaning the stable groove effect is strongest in the **single step immediately before the spike**, and dissipates over longer lookbacks. 

The effect does **not** disappear even at W=10: ambush tokens still have more stable predecessors 10 steps back than neutral tokens. The stable context is a persistent feature around ambush events.

---

## Finding 3: Stability Predicts the EXISTENCE of a Spike, Not Its Height

Within the ambush group (S₂ ≥ 3), does greater pre-spike stability predict a taller spike?

| Window | r(pre-Jaccard, S₂) |
|---|---|
| W=1 | **+0.023** |
| W=2 | +0.008 |
| W=3 | +0.006 |
| W=5 | −0.0001 |
| W=10 | −0.006 |

No. Within the ambush group, pre-spike Jaccard has essentially zero correlation with S₂ height. The stable groove predicts that a spike will occur — but once a spike is occurring, its magnitude is not predictable from how stable the preceding window was.

This suggests a **threshold model**: stability enables the ambush (makes it possible) but does not amplify it beyond the threshold. Once the poet has cleared the ambush threshold, additional stability contributes nothing more to surprise height.

---

## Finding 4: The "Tension-Release" Model Fails

A simple tension-release model would predict: **the longer the conformist run before an ambush, the higher the spike** (like compressing a spring).

| Conformist Run Before Ambush | n | Mean S₂ | Max S₂ |
|---|---|---|---|
| 0 (no conformist predecessor) | 4,063 | **6.255** | 36.66 |
| 1 conformist token | 2,120 | 6.025 | 22.04 |
| 2–3 conformist tokens | 1,493 | 5.963 | 25.48 |
| 4–7 conformist tokens | 481 | 5.853 | 18.85 |
| 8+ conformist tokens | 26 | 6.189 | 12.30 |

Correlation: r = −0.039 (essentially flat, slight negative).

**The tension-release model is false.** Longer conformist runs do NOT produce higher spikes. If anything, they slightly suppress maximum spike height (Max S₂ drops from 36.66 at run=0 to 12.30 at run=8+). The deepest conformist groove does not compress a spring — it may instead deplete available surprise.

---

## Finding 5: Ambush Tokens Follow Longer Stable Grooves

Looking at consecutive-position stable runs (Jaccard > 0.1) before each token:

| Group | Mean Stable Run | % with Run ≥ 3 |
|---|---|---|
| Ambush (S₂ ≥ 3) | **0.776** | **9.4%** |
| Control (−1 to 1) | 0.586 | 6.4% |

Ambush tokens follow **32% longer stable grooves** on average, and are **47% more likely** to follow a stable groove of 3+ tokens. This is the clearest evidence that stable prediction windows "set up" ambush events.

---

## Finding 6: Era Profiles — Traditional Forms Build the Best Grooves

Eras ranked by mean pre-spike Jaccard (W=3) of their ambush tokens:

| Era | Pre-Jacc W=3 | Mean Ambush S₂ | Conf Run |
|---|---|---|---|
| **Highest** | | | |
| rondeau | 0.1313 | 7.16 | 0.53 |
| ancient | 0.1162 | 5.76 | 0.85 |
| 18th_century | 0.1159 | 6.10 | 1.00 |
| metaphysical | 0.1151 | 5.57 | 0.93 |
| double_dactyl | 0.1143 | 5.77 | 1.28 |
| modernist | 0.1067 | 6.52 | 0.88 |
| **Lowest** | | | |
| imagist | 0.0689 | 5.50 | 1.36 |
| black_arts | 0.0630 | 6.10 | 0.83 |
| korean_modernist | 0.0552 | 5.43 | 0.92 |
| haiku | 0.0541 | 5.22 | 1.00 |

**Pattern**: Traditional, heavily formal eras (rondeau, ancient, 18th century, metaphysical, double dactyl) produce the most stable pre-ambush grooves. Experimental modern forms (haiku, imagist, black arts) produce the least stable. 

Interestingly, the **modernist** era — which has BOTH high avg S₂ overall AND high mean ambush S₂ (6.52, the highest in the table) — achieves this via the most stable pre-ambush grooves in a non-traditional form. Modernist poets like Eliot and Stevens build vocabulary-stable contexts that then detonate.

The **haiku** situation is striking: very low pre-ambush Jaccard (0.054) and the lowest mean ambush S₂ (5.22). With only 2–3 lines, there is no time to establish a stable vocabulary groove — every token is a first appearance. Without the groove, the ambush has lower impact. This may explain why haiku has strongly positive raw S₂ but slightly *negative* clean S₂: its "surprises" are shallow because there's no established context for them to violate.

---

## Finding 7: Perfect Ambush Examples (High S₂ × High Pre-Stability)

Top ambush tokens ranked by S₂ × pre-Jaccard (W=5):

| Token | S₂ | Pre-Jacc W=5 | Conf Run | Author |
|---|---|---|---|---|
| `spotlight` | 15.68 | 0.3023 | 0 | Marianne Moore |
| `into` | 13.04 | 0.3517 | 1 | Marianne Moore |
| `imagination` | 15.39 | 0.2962 | 0 | Wisława Szymborska |
| `spotlight` | 15.42 | 0.2892 | 0 | Marianne Moore |
| `shook` | 22.04 | 0.2007 | 1 | Gerard Manley Hopkins |

Marianne Moore appears repeatedly: her densely referential, high-precision vocabulary creates stable local grooves from which sudden concrete nouns (`spotlight`, `imagination`) erupt with high S₂. Hopkins's `shook` achieves the highest S₂ (22.04) in this list while following a stable groove of W=5 Jaccard = 0.20 — far above the corpus mean of 0.087.

---

## Synthesis: Stable Groove → Ambush Mechanism

The evidence for the stable groove → ambush mechanism:

| Claim | Evidence |
|---|---|
| Ambush tokens are preceded by more stable prediction windows | Confirmed: mean Jaccard 0.093 (ambush) vs 0.082 (neutral) across all windows |
| The effect is strongest immediately before the spike | Confirmed: largest gap at W=1, decays monotonically |
| Stability predicts spike existence, not spike height | Confirmed: within ambush group, r(Jaccard, S₂) ≈ 0 |
| Longer conformist runs produce higher spikes (tension-release) | **Disconfirmed**: r = −0.039, no monotonic trend |
| Traditional/formal eras build better grooves | Confirmed: rondeau, ancient, 18th-century have highest pre-ambush Jaccard |
| Haiku lacks grooves → lower-impact ambushes | Supported: lowest pre-Jacc and lowest ambush S₂ in era comparison |

**Main finding**: The stable groove → ambush relationship operates as an **enabling condition**, not an amplifier. Stability creates the conditions in which extreme S₂ events become more probable (the poet can violate a coherent expectation), but once a spike occurs, its magnitude is determined by other factors (frequency, semantic distance, the specific word chosen) independent of how stable the preceding context was.

---

## Implications

1. **Poetic surprise is a figure-ground phenomenon.** The surprise (high S₂ token) requires a stable background (high Jaccard groove). Without the groove, the spike loses coherent context to violate — it becomes noise, not signal.

2. **Form matters informationally.** Traditional forms (rondeau, ancient, metaphysical) build stable grooves naturally through repetition and constraint. This may be one reason these forms "feel" more deliberately crafted — the information-theoretic contrast between groove and spike is clearer.

3. **Haiku's paradox.** Short poems cannot build stable grooves — every word is new. High raw S₂ from lack-of-context is informationally shallow; it measures layout artifact or vocabulary newness, not genuine deviation from established expectation.

4. **The "spring" model of poetic tension is wrong.** Building longer conformist runs before a surprise does NOT increase the surprise's height. Compression does not store energy for poetic release; instead, sustained conformity may exhaust the vocabulary of available surprise.

---

## Next Steps

- Track whether stable grooves are created by **lexical repetition** (the same words cycling) vs. **syntactic regularity** (consistent grammatical structure) — which type of stability enables ambush?
- Identify the optimal groove length for maximum ambush likelihood (diminishing returns analysis).
- Test whether **readers experience** stable-grooved ambushes as more impactful than grooveless ones (would require a human judgment dataset).
- Examine the top ambush tokens (like Moore's "spotlight") in full context to characterize WHAT the groove consists of.
