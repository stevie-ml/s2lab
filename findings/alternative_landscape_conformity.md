# The Alternative Landscape: Why Line-Final Tokens Are Predictable

**Date:** 2026-09-27  
**Experiment:** `experiments/alternative_landscape.py`  
**Corpus:** 169 English poetry texts, 18,942 tokens  
**Builds on:** `line_position_analysis.md`, `straussian_gap_taxonomy.md`

---

## Research Question

We already know line-final tokens have lower S₂ (−1.20) and line-initial tokens have higher S₂ (+6.38). But *why*? Two competing mechanisms:

- **Hypothesis A (Prediction Narrowing):** GPT-2's prediction space is structurally constrained at line endings — the context forces only a limited set of alternatives. Poets conform because there's little choice.
- **Hypothesis B (Active Conformity):** GPT-2 offers a wide range of alternatives at line endings, but poets actively choose the expected word anyway — conformity is a deliberate formal decision.

---

## The Answer: Active Conformity (Hypothesis B)

The alternative landscape is actually **more dispersed** at line endings, not more constrained:

| Position | n | Avg S₂ | Alt Entropy | Top-1 Prob | Coverage (top-10) | Chosen in Top-10 |
|----------|---|--------|-------------|------------|-------------------|-----------------|
| **Initial** | 1,878 | **+6.38** | 1.0491 | **0.458** | 0.625 | **41.4%** |
| Medial | 13,324 | −0.27 | 1.5264 | 0.280 | 0.542 | 56.7% |
| **Final** | 3,740 | **−1.20** | **1.5515** | 0.424 | **0.711** | **82.6%** |

Key contrasts:
- **Alt entropy at final (+1.55) is HIGHER than at initial (+1.05)**: line endings have a *more dispersed* prediction landscape, not a narrower one.
- **Top-1 probability at final (0.424) is LOWER than at initial (0.458)**: GPT-2 is slightly *less* certain about its top prediction at line endings.
- **Yet: chosen-in-top-10 rate at final (82.6%) is 41pp higher than at initial (41.4%)**.
- **Avg rank of chosen token at final is 2.05** (extremely close to the top prediction).

**Conclusion: Line-final predictability is an active poet choice.** The freedom exists — GPT-2's predictions are spread across alternatives — but poets reliably select from the top alternatives and sit close to the #1 prediction.

---

## The Line-Initial Paradox

Line beginnings show the opposite pattern:
- GPT-2 is *more* concentrated on its top prediction (top-1 prob = 0.458, alt entropy = 1.049)
- Yet only **41.4%** of line-initial tokens are in the top-10 alternatives
- When chosen from top-10, the avg rank is 3.51 (further from the top prediction than at finals)

Likely mechanism: after a newline token, GPT-2 strongly predicts "The", "I", or another common line-opener. Poets almost always choose something else — exploiting the reset of context for maximum semantic surprise.

At line endings, GPT-2 has already processed the line content and sees many possible completions. Poets choose conventional endings (often for rhyme or meter), picking reliably from the top alternatives despite having more choices.

---

## Era Breakdown: Δ(Final − Initial) Chosen-in-Top-10

The conformity effect varies dramatically by tradition:

| Era | Initial | Final | Δ |
|-----|---------|-------|---|
| **Surrealist** | 60.0% | 55.6% | **−4.4** |
| 18th century | 90.9% | 95.3% | +4.4 |
| Haiku | 22.2% | 67.3% | +45.1 |
| Nursery rhyme | 22.2% | 92.3% | **+70.1** |
| Ballad | 43.8% | 90.6% | +46.8 |
| Romantic | 37.0% | 87.0% | +50.0 |
| Victorian | 39.3% | 82.0% | +42.7 |
| Modernist | 39.7% | 77.3% | +37.7 |
| Language poetry | 31.2% | 72.4% | +41.2 |
| Song lyrics | 57.4% | 95.0% | +37.6 |

**Surrealist** is the only era where line-final tokens are *less* conventional than line-initial tokens — the only tradition that systematically exploits endings for surprise rather than closure.

**Nursery rhymes** show the most extreme conformity gradient: initial tokens are only 22.2% conventional (maximum freedom at the start of each line), but final tokens are 92.3% conventional (near-total conformity to expected endings). This is the formal grammar of the nursery rhyme.

**Haiku** has the lowest initial conformity rate (22.2%) — consistent with haiku's aggressive use of unexpected opening images — but rises to 67.3% at finals. The kireji (cutting word) occupies a final or near-final position and often IS the expected ending.

---

## The Alt-Entropy / S₂ Relationship

Does the dispersion of GPT-2's prediction landscape predict S₂ at medial positions?

| Alt Entropy Quartile | Avg Alt Entropy | Avg S₂ |
|----------------------|-----------------|--------|
| Q1 (most concentrated) | 0.7351 | −0.142 |
| Q2 | 1.4112 | −0.410 |
| Q3 | 1.7819 | −0.335 |
| Q4 (most dispersed) | 2.1775 | −0.173 |

S₂ is highest at the *extremes* — when GPT-2 is very concentrated (Q1) AND when it is very dispersed (Q4). Middle-range prediction landscapes (Q2, Q3) produce the lowest average S₂.

Interpretation:
- **Very concentrated predictions (Q1):** GPT-2 strongly expects one specific word. If the poet deviates, S₂ spikes massively. If they conform, S₂ is very negative. The averaging pulls to a moderate negative value.
- **Very dispersed predictions (Q4):** GPT-2 has no strong opinion. Any chosen word can have high S₂ because the entropy term in S₂ = surprisal − entropy is large. The high entropy "forgives" any choice, but also means any choice is somewhat surprising.
- **Middle predictions:** GPT-2 has moderate confidence — not strong enough for big S₂ deviations, not dispersed enough for entropy-driven S₂.

---

## Synthesis: Two Modes of Formal Conformity

This analysis reveals two distinct mechanisms underlying poetic predictability:

1. **Constraint-from-below (line endings, fixed forms):** Poets choose conventional words not because they're forced to (the prediction space is actually wide) but because formal requirements (rhyme, meter, semantic closure) pull toward the expected. The conformity is *volitional*.

2. **Surprise-from-reset (line beginnings):** GPT-2 narrows on a few expected openers, and poets systematically reject all of them. The surprise is *oppositional* — working against the most concentrated predictions.

The two effects together generate the 7.58-bit S₂ gap between line-initial (+6.38) and line-final (−1.20) positions — a gap driven not by structural prediction differences but by **poet strategy**: maximal rejection of expected openers, maximal acceptance of expected closers.

---

## Suggested Next Steps

1. **Within-line gradients:** Is the conformity transition smooth (linear drop from initial to final) or is there a threshold at position 3-4 where conformity "kicks in"?
2. **Rhymed vs. free verse breakdown:** The conformity effect at finals should be stronger in rhymed verse. Can we separate these groups in the corpus?
3. **The surrealist exception:** Which specific poems drive the negative delta in surrealism? Are the line-final surprises in Breton's work semantically coherent or truly random?
4. **Chosen rank 2 vs. rank 1:** When poets choose from the top-10, they tend toward rank 2 at finals. Is rank-2 systematically different from rank-1 in a way that explains this preference?
