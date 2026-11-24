# Surprise Decay Curve: The Temporal Half-Life of Poetic Surprise

**Date:** 2026-11-24  
**Experiment:** `experiments/surprise_decay_curve.py` → `results/surprise_decay_curve.json`  
**Corpus:** English-only texts, 11,613 high-S₂ events (S₂ ≥ 2.0, p_newline < 0.9), 42+ eras  
**Builds on:** `findings/post_surprise_signature.md` (t+1 only), `findings/entropy_after_surprise_liberation_vs_anchoring.md`  
**Extends:** tracks S₂ at lag 0, 1, 2, ..., 15 tokens after each spike

---

## Research Question

After a poet writes an unexpected word (high-S₂ token), how many tokens does it take before S₂ returns to the poem's baseline? Is surprise a **single-token event** (instantly resolved), a **wave** (reverberating for many tokens), or an **oscillation** (recovery followed by secondary spike)?

---

## Primary Finding: Surprise Is Overwhelmingly a Single-Token Event

| Lag | Mean S₂ | % of Spike Value | N |
|-----|---------|------------------|---|
| 0 (spike) | **5.25** | 100.0% | 11,613 |
| 1 | -0.40 | **-7.6%** | 11,613 |
| 2 | -0.42 | -7.9% | 11,613 |
| 3 | -0.46 | -8.8% | 11,542 |
| 4 | -0.43 | -8.2% | 11,462 |
| 5 | -0.41 | -7.9% | 11,386 |
| 10 | -0.41 | -7.9% | 11,019 |
| 15 | -0.49 | -9.3% | 10,638 |

**Poetic surprise drops to below-baseline S₂ in a single step.** The mean S₂ spike is 5.25 at lag 0, then immediately plummets to -0.40 at lag 1 — a drop of **5.65 S₂ units** in one token. The corpus-wide baseline S₂ is approximately -0.45, so by lag 1 the poem has already overshot baseline and sits at the typical level for non-spike tokens.

**Recovery time distribution:**

| Threshold | % of spikes recovered |
|-----------|----------------------|
| By lag 1 | **75.8%** |
| By lag 3 | **98.7%** |
| By lag 5 | **99.9%** |

Three-quarters of all poetic surprises are "paid for" within a single token. Effectively no spike persists beyond lag 5.

---

## Finding 2: Surprise Is "Paid For" With Below-Baseline Conformity

The post-spike mean S₂ (-0.40 to -0.50) is not just at baseline — it is *slightly below* baseline. This means high-S₂ moments are followed by tokens that are **more predictable than average**, not merely average. The poet's unexpected word creates a temporary "debt" of predictability: the reader receives an unexpected word, and then the poem delivers a brief run of highly expected words.

This is consistent with the `post_surprise_signature.md` finding that surprise is followed by punctuation (comma, period, dash) at 1.62× the baseline rate — grammatical closure as the mechanism of "debt repayment."

---

## Finding 3: Era Variation in Cascade vs. Isolation Patterns

While the global picture is single-token decay, eras differ substantially in whether the lag-1 token *overshoots* baseline (deep negative = strong isolation) or *barely drops* (near-zero or positive = potential cascade):

### Fast Crashers — Spikes That Immediately Trigger Conformity

| Era | lag-1 % | Interpretation |
|-----|---------|----------------|
| double_dactyl | -24.6% | Rigid meter forces immediate predictable continuation |
| metaphysical | -21.0% | Complex conceit requires syntactic follow-through |
| song_lyrics | -19.7% | Hooks followed by formulaic continuation |
| nonsense | -19.0% | Semantic rule-break resolved by grammatical regularity |
| imagist | -19.9% | Single striking image followed by pause/silence |

These eras treat surprise as a **bolt of lightning**: bright, brief, immediately closed.

### Slow Crashers / Potential Cascade Eras — Spikes That Don't Immediately Resolve

| Era | lag-1 % | Interpretation |
|-----|---------|----------------|
| **oulipo** | **+8.1%** | Constrained writing generates cascading surprises |
| **rondeau** | +5.6% | Refrain structure primes next surprise |
| **korean_modernist** | +5.9% | Small N (caution) |
| **beat** | +1.1% | Loose syntax allows continued drift |
| **classical_chinese** | +3.9% | (translation artifact likely) |
| black_arts | +5.3% | Rhetorical intensification chains |

**The oulipo anomaly**: Oulipo poetry actually has a *higher* mean S₂ at lag 1 than at any point except the spike itself (+8.1%). This means that in constraint-based writing, one unexpected word predicts another. The constrained generation procedure (N+7, lipogram, snowball) creates a **cascade architecture** where violation of one linguistic norm ripples into the next token.

---

## Finding 4: Long-Tail Oscillations — The "Bounce" Pattern

Some eras show an interesting reversal at longer lags: they recover by lag 5 but then show *renewed S₂ elevation* at lag 10, suggesting secondary mini-spikes:

| Era | lag-5 % | lag-10 % | Pattern |
|-----|---------|----------|---------|
| mid_century | +5.3% | -3.0% | Late elevation then recovery |
| ancient | -4.8% | +4.6% | U-curve (second spike at lag 10) |
| parody | -7.5% | +2.8% | Secondary lift |
| german_expressionist | -3.8% | +2.2% | Secondary lift |

**Ancient poetry and the "echo" bounce**: Ancient poetry (Homer, Sappho, biblical) shows near-flat lag-5 and then a secondary S₂ lift at lag 10. This may reflect formulaic structure — a Homeric epithet or repeated formula generates a local S₂ event at a characteristic distance from the first.

**The Harlem Renaissance reverb**: Harlem Renaissance poetry shows an unusually dramatic DELAYED drop:
- lag-1: -5.7% (mild initial drop)
- lag-10: -17.4% (much stronger drop later)

This "reverb" pattern suggests that in this tradition, the surprise token is embedded in a syntactic or rhetorical structure that only resolves many tokens later — surprise is spread across a phrase, not concentrated in a single word.

---

## Finding 5: Pantoum and Villanelle — Formal Structure Leaves No Room for Long-Term Surprise

| Era | lag-1 % | lag-5 % | lag-10 % |
|-----|---------|---------|----------|
| pantoum | -12.3% | +0.3% | **-20.3%** |
| villanelle | -15.7% | -9.2% | -11.0% |

Both highly repetitive forms (pantoum, villanelle) show strong **below-baseline** S₂ persistence at long lags. After an initial surprise, the repeating line structure creates sustained conformity — the reader learns the form's patterns and GPT-2's entropy drops systematically as refrain tokens approach. This is the information-theoretic signature of **learning within a poem**: as refrains repeat, the model (and perhaps the reader) becomes more confident about what comes next, pushing S₂ well below baseline for many tokens following any deviation.

---

## Synthesis: Two Architectures of Poetic Surprise

| Architecture | Characteristic | Eras |
|---|---|---|
| **Isolated spike** | Single-token event, immediate below-baseline recovery | Most eras (romantic, victorian, modernist, confessional) |
| **Cascade** | Post-spike token also above baseline | oulipo, beat, rondeau, black_arts |
| **Reverberation** | Mild initial drop, strong later drop | harlem_renaissance, pantoum |
| **Bounce** | Recovery then secondary elevation | ancient, mid_century, parody |

The dominant architecture is the **isolated spike** — consistent with the "post-surprise punctuation" finding that surprise is mechanically closed by a comma or period. But the minority architectures are theoretically important: they reveal different **rhetorical strategies** for deploying unexpectedness.

---

## Implications for the Straussian Gap

If the "Straussian gap" is the space between what language expects and what the poet writes, the decay curve characterizes how long that gap **stays open**. For most poetry, the gap is a pinhole — open for one token, closed by the next. For oulipo and constrained writing, the gap can extend over several tokens, creating what we might call **compound divergence**: not a single unexpected word but a chain of unexpected words that together constitute the deviation from language norms.

---

## Next Steps

1. **Classify individual poems** by their decay curve shape (isolated/cascade/reverberation/bounce) — do particular poems show strong signatures?
2. **Control for token frequency**: Are the lag-1 tokens "cheap" (function words) that happen to be S₂-negative, or genuinely low-surprisal content words?
3. **Compare within-poet variation**: Does a single poet use different surprise architectures in different poems?
4. **Phonological analysis of lag-1 tokens**: The punctuation finding suggests a specific sound/rhythm pattern — does the post-surprise token have distinctive phonological properties?
