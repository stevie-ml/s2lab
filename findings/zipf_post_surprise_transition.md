# Zipf Regime Transitions After Surprise: Anchoring vs Liberation

**Date:** 2026-11-23  
**Experiment:** `experiments/zipf_post_surprise_transition.py` → `results/zipf_post_surprise_transition.json`  
**Corpus:** 405 English texts, 56,118 consecutive token pairs (p_newline < 0.9)  
**Builds on:** `findings/zipf_prediction_coefficient.md`, `findings/post_surprise_signature.md`

---

## Research Question

After a poet makes an unexpected choice (high S₂ token at position i), does the model's
probability distribution at the NEXT position (i+1) become:

- **(a) More concentrated** — the unexpected word "anchors" grammar, narrowing what can follow
- **(b) More diffuse** — the unexpected word "liberates" possibilities, opening up the continuation space

Previous work established that hyper-Zipf contexts produce the most efficient positive S₂
(Zipf finding) and that after surprise the subsequent S₂ is elevated (post-surprise signature).
This experiment asks: **does the shape of prediction — not just its mean — change after surprise?**

---

## Metric: Δα = Zipf Alpha(i+1) − Zipf Alpha(i)

Positive Δα = model concentrates (anchoring effect).
Negative Δα = model diffuses (liberating effect).

---

## Finding 1: Mild-to-Moderate Surprise Anchors; Extreme Surprise Neutralizes

| S₂ at position i | n | mean_alpha(i+1) | Δα (i+1 − i) | concentrate% (Δα > 0.5) | diffuse% (Δα < −0.5) |
|---|---|---|---|---|---|
| **very_neg (<−3)** | 13,252 | 1.197 | +0.005 | 22.0% | 24.4% |
| **neg (−3 to 0)** | 23,973 | 1.496 | −0.101 | 23.8% | 29.3% |
| **low_pos (0–2)** | 7,248 | 1.313 | **+0.192** | 30.6% | 15.7% |
| **high_pos (2–5)** | 6,727 | 1.344 | **+0.180** | 30.0% | 16.3% |
| **extreme (≥5)** | 4,918 | 1.401 | +0.034 | 24.2% | 23.2% |

**The central finding:** S₂ in the range 0–5 produces **systematic anchoring** at the next position
(Δα ≈ +0.19). The model's next-step distribution becomes significantly more concentrated after
mild-to-moderate poetic surprise. At extreme S₂ (≥ 5), however, the anchoring effect collapses
to near-zero (Δα = +0.034), and the concentrate/diffuse ratio returns to roughly parity (24% vs 23%).

**Conformist choices diffuse.** When S₂ is in the negative range (the poet chose something the
model half-expected), the NEXT step becomes *more diffuse* (Δα = −0.101, 29.3% diffuse vs 23.8%
concentrate). After a predictable choice, grammar opens up — many continuations remain possible.

---

## Finding 2: The Sweet Spot — Why S₂ 0–5 Anchors

The anchoring effect is confined to the "sweet spot" of positive but not catastrophic surprise.
Two mechanisms explain this:

1. **Grammatical snap**: A mild surprise often involves choosing an unexpected word that still
   fits grammatically (e.g., an unusual noun in subject position). The grammar then constrains
   what must follow more tightly than a fully expected word would — the content choice is
   resolved, so structure constrains.

2. **Extreme surprise breaks grammar**: At S₂ ≥ 5 (catastrophic deviation — rank ~600+ when
   model top-1 had 85%+ probability), the choice is so unexpected that the model "resets"
   to its global distribution, losing any positional anchoring. The continuation is as
   open-ended as the beginning of a sentence.

---

## Finding 3: Sub-Zipf After Very Negative S₂

One of the most unexpected results: when the poet was **hyper-conformist** (S₂ < −3, i.e.,
chose a word that was not only expected but also fell below what entropy warranted), the
subsequent token has the **lowest mean alpha (1.197)** and highest sub-Zipf rate (29.4%).

This inverts the naive prediction. After an obviously expected word, the model should
"know where it is" and become more concentrated. Instead, deeply conformist choices often
appear at **semantic junctions** — articles before NPs, prepositions before PPs — where
the word type is fixed but the content is maximally open. The word "the" tells you a noun
follows; it doesn't tell you which noun.

---

## Finding 4: Zipf Regime Persistence and Self-Affinity

| From → | hyper | super | near | sub | anti |
|---|---|---|---|---|---|
| **hyper_zipf** | **39.5%** | 26.6% | 25.9% | 8.0% | 0.1% |
| **super_zipf** | 7.3% | **31.4%** | 42.2% | 18.6% | 0.5% |
| **near_zipf** | 3.7% | 25.2% | **49.6%** | 20.8% | 0.6% |
| **sub_zipf** | 3.7% | 24.2% | **50.2%** | 21.3% | 0.5% |
| **anti_zipf** | 4.2% | 29.8% | 48.5% | 17.5% | 0.0% |

**Hyper-Zipf is uniquely self-replicating**: 39.5% of hyper-Zipf tokens are followed by
another hyper-Zipf token — far above the base rate (~7% hyper-Zipf overall). Once the
model locks into a high-concentration state, it tends to stay there. Near- and sub-Zipf
are also persistent (≈50%), but the hyper-Zipf self-affinity is especially strong.

This suggests that **hyper-Zipf clusters in local runs** — the model enters moments of
laser-focused expectation and stays there for several tokens (grammatical dependencies,
metrically constrained slots, etc.).

---

## Finding 5: Era-Level Anchoring Profiles

| Era | n (high S₂) | mean Δα | anchor% | liberate% | Verdict |
|---|---|---|---|---|---|
| **nursery_rhyme** | 39 | **+0.410** | 35.9% | 15.4% | Strongest anchor |
| **classical_chinese** | 47 | **+0.286** | 29.8% | 12.8% | Strong anchor |
| **protest_political** | 48 | +0.252 | 33.3% | 12.5% | Strong anchor |
| **procedural** | 138 | +0.240 | 34.1% | 17.4% | Anchor |
| **german_expressionist** | 118 | +0.214 | 39.0% | 22.0% | Anchor |
| *(Victorian, romantic, confessional, contemporary)* | varied | +0.12–0.15 | ~28% | ~18% | Moderate anchor |
| **modernist** | 664 | +0.026 | 22.3% | 22.6% | **Neutral** |
| **oulipo** | 302 | −0.012 | 24.2% | 22.2% | Near-neutral |
| **beat** | 189 | −0.026 | 30.7% | 25.4% | Slight liberation |
| **haiku** | 73 | **−0.086** | 16.4% | 26.0% | Liberation |
| **ballad** | 179 | **−0.115** | 14.0% | 21.8% | Liberation |
| **concrete** | 52 | **−0.126** | 17.3% | 26.9% | Strongest liberation |

**Anchoring traditions** (nursery rhyme, classical Chinese, protest poetry, procedural):
Surprising moments in these forms lock down the continuation. The surprise is _local_ —
it shocks, then grammar reasserts itself with heightened force.

**Liberating traditions** (concrete, ballad, haiku, beat):
Surprising moments in these forms open up possibilities. The surprise propagates —
it doesn't settle back into grammar but creates genuine indeterminacy.

**Neutral traditions** (modernist, oulipo):
Surprise has no net effect on the prediction structure — surprises and continuations
are independent, suggesting a fully non-grammatical surprise strategy.

---

## Synthesis: Two Types of Poetic Surprise

The data supports a structural taxonomy based not on WHAT surprises (token identity)
but on WHAT FOLLOWS surprise (prediction structure):

| Type | Δα | Examples | Description |
|---|---|---|---|
| **Syntactic Ambush** | > +0.1 | Nursery rhyme, ballad refrain, procedural | Surprise is local; grammar snaps tighter after the unexpected word |
| **Semantic Liberation** | < −0.1 | Concrete, haiku, free verse | Surprise propagates forward; model enters diffuse uncertainty |
| **Information Neutrality** | ≈ 0 | Modernist, oulipo | Surprise is decoupled from continuation structure |

The sweet spot for maximum anchoring is S₂ in the 0–5 range — poetic surprise that is
real but not catastrophic. Extreme deviation (S₂ ≥ 5) instead neutralizes anchoring,
suggesting these moments fracture grammatical context rather than redirecting it.

---

## Suggested Next Steps

1. **Token-level case study**: Examine specific high-S₂ anchoring vs liberating tokens
   (what concrete words produce ≥ +1.0 Δα vs ≤ −1.0 Δα?)
2. **Clause boundary interaction**: Does anchoring correlate with syntactic closure
   (period, semicolon following the surprise token)?
3. **Volta as anchoring event**: Test whether sonnet volta tokens (high S₂ at line 9)
   produce the strongest anchoring — the formal resolution of the turn.
4. **Multi-step traces**: Extend to Δα at i+2 and i+3 to see how long the
   anchoring/liberation effect persists.
