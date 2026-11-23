# Conjunction Deep-Dive: S₂ by Conjunction Type

**Date:** 2026-11-23  
**Method:** Direct token-text matching across 431 poetry texts + 5 prose controls. Classified each token as coordinating additive/adversative/disjunctive/causal or subordinating causal/temporal/concessive/conditional/relative. Computed artifact-free avg S₂ per conjunction type (p_newline < 0.9 filter).  
**Builds on:** `findings/syntactic_position_vs_s2.md` (conjunction group showed Δ = +2.918 poetry-vs-prose, the third-largest gap after ADJ and NOUN).

---

## Key Results

| Conjunction Type | n | Poetry Avg S₂ | Prose Avg S₂ | Δ S₂ | % Positive |
|------------------|---|--------------|-------------|------|-----------|
| **sub_concessive** (although, though, even, albeit) | 80 | **+1.776** | — | — | **69%** |
| **sub_temporal** (when, while, after, before, once) | 450 | **+0.202** | — | — | 45% |
| **coord_adversative** (but, yet, however, nevertheless) | 343 | **+0.163** | — | — | 48% |
| sub_causal (because, since, as, inasmuch) | 265 | -0.235 | — | — | 37% |
| sub_relative (that, which, who, whom, where) | 661 | -0.293 | -1.703 | **+1.410** | 37% |
| coord_causal (so, for, therefore, thus, hence) | 520 | -0.400 | — | — | 31% |
| sub_conditional (if, unless, whether, lest) | 79 | -0.962 | — | — | 29% |
| coord_disjunctive (or, nor, either, neither) | 189 | -0.129 | — | — | 42% |
| **coord_additive** (and, both, also, plus) | 1,347 | **-2.284** | -1.978 | **-0.306** | 16% |

---

## Finding 1: Concessive Conjunctions Are the Most Surprising

**Sub_concessive** (although, though, even, albeit) scores the highest average S₂ of any conjunction type (+1.776, 69% positive). This is higher than even adversative "but/yet" (+0.163).

**Interpretation:** Concessive constructions set up a logical "despite X, Y" structure — they explicitly signal an upcoming contradiction of the expected. When a poet writes "although," they're committing to a syntactic form that promises to overthrow what came before. Apparently poets use this form in highly unexpected contexts, so the word "although" itself arrives with surprise. The high positive-S₂ rate (69%) confirms this is not just a few outliers — most concessive conjunctions in poetry are genuinely unexpected positions.

This may reflect that *concessive* structures are inherently "meta-surprise" markers: the conjunction itself announces that conventional expectations will be violated.

---

## Finding 2: "And" Is the Most Predictable Word in Poetry

**Coord_additive** (dominated by "and") scores -2.284 — the most *negative* S₂ of any conjunction group, and even more negative than the same group in prose (-1.978). "And" in poetry is **more expected than "and" in prose**.

This inverts naive expectations. We might assume poetic "and" (Whitman's catalogs, biblical "and") is more surprising. Instead, it reflects that poetry uses "and" in highly regular positions: the onset of catalog lines, the continuation of parallel structures (anaphora), and biblical-style parataxis. These are all maximally predictable contexts. 

The implication: when poets reach for "and," they reach for it exactly where the model expects it. This is the conjunction of *compliance*, not creativity.

---

## Finding 3: Adversative "But/Yet" Is the Volta Marker — But Modestly

**Coord_adversative** (but, yet, however, nevertheless) scores +0.163 — above zero, with 48% positive tokens. This confirms that adversative conjunctions function as volta markers: when poets write "but" or "yet," they're often doing so at an unexpected position, signaling a semantic reversal.

However, the effect is *smaller* than expected (+0.163 vs sub_concessive's +1.776). This may be because "but" is so commonly used as a volta marker that it has become a *cliché* in its own right — the model has learned that "but" follows certain patterns in poetry, reducing its surprisal.

---

## Finding 4: Conditional Conjunctions Are Predictable

**Sub_conditional** (if, unless, whether, lest) scores -0.962 — unexpectedly *predictable*. Conditional structures in poetry appear in expected positions: "if" commonly starts lines (formulaic conditional openings), "whether" appears in predictable rhetorical contexts.

This suggests that conditional reasoning in poetry is more formulaic than concessive or temporal subordination.

---

## Era-Level Adversative Conjunction S₂

The most revealing breakdown: how does adversative "but/yet" work across literary eras?

| Era | Adversative S₂ | Interpretation |
|-----|----------------|----------------|
| **surrealist** | +2.737 | "But" arrives as jarring juxtaposition — maximum volta effect |
| **biblical** | +1.426 | "Yet" in psalms signals unexpected reversals of lament/praise |
| **fixed_form** | +1.230 | Structural adversatives in sonnets, etc. placed unexpectedly |
| Victorian | +0.814 | "But" used but still above baseline |
| **18th_century** | -1.606 | Neoclassical "but" is formulaic — expected rhetorical structure |
| **haiku** | -1.940 | Haiku rarely uses "but"; when it does, it's expected |

**Key contrast:** Surrealist poetry (+2.737) vs 18th-century poetry (-1.606) — a gap of 4.3 bits. The neoclassical "but" is a rhetorical cliché (Pope's balanced antitheses are maximally predictable); the surrealist "but" arrives as a rupture.

---

## Poet-Level Adversative Conjunction S₂

**Most surprising use of "but/yet":**
1. Ernest Dowson (+4.651) — his Victorian-to-fin-de-siècle transitions use "but" at peak emotional turns
2. Layli Long Soldier (+4.523) — her use of adversative conjunction is structurally defamiliarizing (official-language disruption)
3. Felicia Hemans (+3.045), Alfred Lord Tennyson (+2.265), Robert Frost (+2.250)

**Most predictable use of "but/yet":**
1. Robinson Jeffers (-3.751) — his "but" appears in expected narrative transitions
2. Kobayashi Issa (-2.621) — in translation, adversative conjunctions fall in expected positions
3. Alexander Pope (-1.865) — confirms the neoclassical "but" as formulaic

---

## Theoretical Synthesis

The conjunction S₂ profile reveals a **hierarchy of syntactic surprise**:

1. **Concessive** (although, though): highest surprise — explicitly announces that expectations will be violated
2. **Temporal** (when, while): moderate surprise — time markers placed at unexpected moments  
3. **Adversative** (but, yet): moderate surprise — volta markers, but partly formulaic from overuse
4. **Relative** (that, which): close to baseline when compared to prose
5. **Causal** (because, so): slightly negative — causal reasoning follows predictable patterns
6. **Conditional** (if, unless): quite negative — conditional poetry is formulaic
7. **Additive** (and): most negative — catalog/paratactic "and" is maximally expected

The paradox: poets use "and" (the least surprising conjunction) far more than "although" (the most surprising). This may reflect the **economics of surprise**: if every conjunction were maximally surprising, the effect would be lost. The catalog of "ands" creates a stable base against which the occasional "although" or "yet" can land with full force.

---

## Suggested Next Steps

1. **Concessive deep-dive**: Which poems use "although/though" most strikingly? Map the semantic content of what comes before vs. after
2. **The "and" economy**: Measure Whitman's catalog poems specifically — how does his additive "and" sequence set up the final volta?
3. **Temporal conjunction placement**: Are "when" and "while" surprising at the *start* of stanzas vs. mid-line? (These are common as opening gambits in elegies)
4. **Cross-poet concessive analysis**: Are there poets who use concessive constructions as their primary surprise vehicle?
5. **Interaction with S₂ cascade**: Does a high-S₂ "although" tend to be followed by an unusually high-S₂ clause (double surprise)?
