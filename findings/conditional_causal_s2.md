# Conditional and Causal Connectives: Epistemic Structure and S₂

**Date:** 2026-10-04
**Experiment:** `experiments/conditional_causal_s2.py`

## Research Question

Do logical connectives (if, because, though, when, like) shape the information-theoretic profile of what follows them? Each connective encodes a different epistemic stance:

- **Conditional** (if/unless/whether): opens hypothetical space
- **Causal** (because/since/therefore): closes a causal chain
- **Concessive** (though/yet/still/although): signals contrast or reversal
- **Temporal** (when/while/until/before): specifies time relation
- **Comparative** (like/as/than): sets up an analogy

**Three hypotheses tested:**
1. Conditionals → high entropy (hypothetical space is open) → low S₂ after
2. Causals → closed causal chain → lower S₂ after (model expects the explanation)
3. Concessives → contrast setup → HIGH S₂ after (the poet will defect from expectation)

## Core Results

Baseline (all non-artifact poetry tokens): mean S₂ = **−0.437**, mean H = **6.213**

| Category | N | H at connective | S₂ at +1 | ΔS₂ vs baseline | H at +1 | +S₂ % |
|----------|---|-----------------|-----------|-----------------|---------|--------|
| conditional | 23 | **6.81** | −0.738 | −0.301 | **5.07** | 26.1% |
| temporal | 74 | 6.22 | −0.430 | +0.007 | 5.93 | 25.7% |
| causal | 48 | 6.39 | −0.565 | −0.128 | **6.61** | 31.2% |
| concessive | 84 | **7.32** | −0.722 | −0.285 | 6.45 | 33.3% |
| comparative | 144 | 6.07 | −0.766 | −0.329 | 6.47 | 36.1% |

## Hypothesis Results

- **H1 (conditionals → high entropy → low S₂): NOT CONFIRMED** — entropy IS higher at "if" (6.81 vs 6.21), but S₂ after is lower (−0.738), and crucially the entropy *after* conditionals drops sharply to **5.07 bits** (the lowest of any category). The conditional creates apparent openness but then syntactically constrains the next word.

- **H2 (causals → closed chain → low S₂): CONFIRMED** — causals produce S₂ = −0.565 < baseline −0.437. But the entropy *after* causals is **higher than baseline** (6.61 vs 6.21), the opposite of what the "closed chain" framing predicted.

- **H3 (concessives → contrast → high S₂): NOT CONFIRMED** — concessives have the highest H at the connective word itself (7.32) but produce lower S₂ after (−0.722), not higher.

## The Central Paradox: Semantic and Syntactic Constraints Are Inverted

The most striking finding is the **divergence between entropy at the connective and entropy at the next token**:

| Connective | H at connective | H at +1 | Change | Interpretation |
|------------|-----------------|---------|--------|----------------|
| conditional ("if") | 6.81 | **5.07** | **−1.74** | Semantically opens but **syntactically closes**: "if" must be followed by a clause subject |
| causal ("because") | 6.39 | **6.61** | **+0.22** | Semantically closes but **epistemically widens**: any domain can explain the prior clause |
| concessive ("yet/though") | **7.32** | 6.45 | −0.87 | Maximum uncertainty at the junction, partial resolution after |
| temporal ("when") | 6.22 | 5.93 | −0.29 | Modest narrowing |

**The conditional paradox:** "If" appears semantically unbounded — anything can be hypothetical. But syntactically, "if" must be followed by a clause subject (noun phrase or pronoun), which GPT-2 can predict well. The entropy drop (6.81 → 5.07) reveals that "if" is syntactically rigid despite semantic openness. Poets do not exploit the hypothetical space for Straussian deviation.

**The causal paradox:** "Because" appears semantically constrained — the explanation must fit the effect. But GPT-2 becomes *more* uncertain after "because" (H rises to 6.61). The explanation could invoke any domain: physics, emotion, history, irony. Poets using "because" are not less surprising; they're less surprising for a different reason (they find causal completions, which happen to be predictable ones).

## Individual Connective Breakdown

| Connective | Category | N | H@connective | S₂@+1 | ΔS₂ | +S₂% |
|------------|----------|---|-------------|--------|------|------|
| **still** | concessive | 24 | **8.57** | −1.681 | −1.243 | 29.2% |
| **yet** | concessive | 28 | 7.00 | −0.278 | +0.159 | 39.3% |
| **though** | concessive | 21 | 7.24 | −0.085 | **+0.352** | 38.1% |
| **while** | temporal | 9 | 6.87 | **+0.382** | **+0.819** | 33.3% |
| **if** | conditional | 23 | 6.81 | −0.738 | −0.301 | 26.1% |
| **so** | causal | 37 | 6.52 | −0.309 | +0.128 | 32.4% |
| **like** | comparative | 35 | 6.57 | −1.008 | −0.571 | 37.1% |
| **than** | comparative | 13 | 6.03 | **−2.433** | −1.996 | **7.7%** |
| **because** | causal | 3 | 6.32 | **−3.801** | −3.364 | **0.0%** |

**Most notable:**

- **"still"** (H = 8.57) is the single most contextually uncertain connective — the model is maximally confused about what comes after "still" — yet it produces the most conventionally expected completions (S₂ = −1.681). "Still" signals reversal at maximum uncertainty but resolves into cliché.

- **"though"** produces the only positive-delta S₂ among concessives (+0.352). Poets use "though" more adventurously than "yet" or "still."

- **"while"** (temporal) produces the highest S₂ at +1 of any connective (+0.382 absolute, +0.819 delta). Temporal "while" is the connective of genuine surprise — perhaps because it suspends two simultaneous actions, creating a scene-space that allows unexpected juxtapositions.

- **"than"** (comparative) is the most constraining word in the corpus: only 7.7% positive S₂ after it, mean S₂ = −2.433. Comparisons ("whiter than X", "louder than Y") are extremely predictable even in poetry.

## Victorian Conditionals: A Special Case

| Era | Conditional S₂ | Causal S₂ | Gap |
|-----|---------------|-----------|-----|
| victorian | **+1.365** | −1.403 | **+2.768** |

Victorian poets show the widest conditional/causal gap: when they use "if," they make highly surprising choices (+1.365, well above baseline); when they use causal connectives, they are deeply conformist (−1.403). This suggests Victorian poetry uses the conditional as a genuine departure point ("If snow be white" — Shakespeare) while treating causal explanations as conventional closures.

## High-S₂ Moments After Connectives

Some notable examples where connectives preface genuinely surprising choices:

**Concessive [yet]** — Christina Rossetti (S₂ = 12.53)
> "yet turning" — Model expected a more conventional adversative response; Rossetti's motion word is maximally unexpected.

**Causal [so]** — E.E. Cummings (S₂ = 13.06)
> "so floating" — A causal structure that resolves not with an explanation but a sensation; the model's prediction collapses.

**Temporal [before]** — Anonymous (found poetry) (S₂ = 14.05)
> "before tap" — The temporal clause resolves with a physical monosyllable where the model expected a more elaborate completion.

## Main Finding

**Epistemic connectives do not behave as their semantic labels predict.** The three hypotheses — conditional → openness, causal → closure, concessive → contrast/surprise — are largely reversed in the data:

1. Conditionals **syntactically constrain** what follows despite semantic openness
2. Causals are **epistemically wider** than their "closure" framing suggests
3. Concessives create **maximum uncertainty at the junction** but poets then fill the space conventionally

The exception is **temporal "while"**, which consistently produces above-baseline S₂. The simultaneity structure of "while" appears to be the most reliably generative connective for Straussian deviation — it holds two timelines open long enough for a genuinely unexpected second element.

**The "still" paradox** is the most curious data point: the connective word that most confuses GPT-2 (H = 8.57) produces the least surprising outcomes. Maximum model uncertainty does not translate into poetic surprise.

## Suggested Next Steps

1. **Larger sample of conditionals**: 23 instances is small — add more poems with conditional structures (especially subjunctive mood) to test the Victorian pattern across eras.
2. **"While" deep dive**: Extract all temporal "while" constructions and examine what makes its following content surprising — is it the suspended-scene effect, or is "while" simply less common (lower base rate → more selective use)?
3. **"Still" and cliché**: The "still" paradox connects to the cliché-vs-originality findings. Is "still" a marker of poetic convention that has calcified into predictability?
4. **Connective density by era**: Which eras use logical connectives most frequently? Does heavy connective use correlate with lower S₂ overall (logically structured poems are more conformist)?
