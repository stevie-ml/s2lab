# Verbal Irony and S₂: Does Irony Hide Its Surprise?

**Date:** 2026-11-04  
**Experiment:** `experiments/irony_s2.py`  
**Data:** `results/irony_s2.json`

---

## Hypothesis

Verbal irony operates *above* the token level. Ironic lines use **conventional, predictable tokens** to express meaning that is semantically inverted. If so, GPT-2 (which has no access to pragmatic/contextual semantics) should *fail to detect* the semantic surprise — ironic tokens should have **lower S₂** than their literal counterparts expressing the same emotional content.

---

## Method

Five paired passages, each with an **ironic version** and a **literal paraphrase** expressing the same underlying meaning. For each pair, specific "key ironic tokens" were designated — the words whose ironic force is most concentrated. S₂ was compared at these tokens and over the full passage.

| Pair | Ironic Text | Irony Type |
|------|-------------|------------|
| `great_war_1` | Owen, "Dulce et Decorum Est" (closing lines) | Allusive / classical quotation |
| `swift_praise` | Swift, "On the Death of Dr. Swift" | Self-deprecatory irony |
| `mock_heroic_pope` | Pope, "The Rape of the Lock" | Mock-heroic register clash |
| `housman_bitter` | Housman, "Here Dead We Lie" | Understatement |
| `larkin_this_be` | Larkin, "This Be The Verse" | Ironic cliché |

---

## Results

### Grand Summary

| Metric | Ironic | Literal | Δ |
|--------|--------|---------|---|
| Avg S₂ (all tokens) | 0.9241 | 0.8281 | **+0.096** |
| Avg S₂ (key tokens) | 0.5651 | 1.6103 | **−1.045** |

The full-passage averages are nearly identical (+0.096), but **at designated ironic tokens specifically**, ironic versions score ~1 bit *lower* than their literal counterparts.

### Per-Pair Results

| Pair | Ironic avg S₂ | Literal avg S₂ | Ironic key S₂ | Literal key S₂ | Key Δ |
|------|---------------|----------------|----------------|-----------------|-------|
| Owen / Dulce | 1.482 | 0.548 | **−1.76** | **+1.33** | **−3.09** |
| Swift praise | 2.098 | 1.714 | +2.78 | +3.01 | −0.23 |
| Pope mock-heroic | 1.688 | 1.892 | **+3.70** | **+2.86** | **+0.84** |
| Housman | 0.106 | −0.130 | +2.06 | +2.19 | −0.12 |
| Larkin | −0.754 | 0.116 | **−3.96** | **−1.34** | **−2.62** |

---

## Key Token Detail

### Owen: The Latin Tag Is Perfectly Predicted

The word "est" appears twice in Owen's closing lines — both times as the final word of a phrase ("decorum est", "pro patria mori"). GPT-2's top prediction for both is "est" itself. S₂ = **−2.86** and **−3.53**.

GPT-2 has memorized "Dulce et decorum est" as a fixed phrase. The model *expects* the Latin tag — there is zero surface-level surprise. Yet this is the most ironic moment in the poem: Owen frames the Latin slogan as "The old Lie," and deploys it immediately after describing a soldier choking on gas.

**The irony is completely invisible to the surface model.** It operates entirely at the allusive/semantic level: the reader recognizes the phrase, knows its cultural meaning, and feels the gap between that meaning and the dying man. GPT-2 just sees a predicted completion.

By contrast, the literal paraphrase token "Truth" has S₂ = **+4.69** — the word is genuinely unusual in this syntactic position, the model expected "man" or "lie."

### Pope: Mock-Heroic Irony DOES Register

Pope's "What mighty contests rise from **trivial** things" — S₂ = **+5.08** at "trivial."  
"**dire** offence from am'rous causes" — S₂ = **+6.46** at "dire."

This is the **opposite** of the Owen pattern. Mock-heroic irony works by placing a semantically incongruous word in a context established by high-register diction. GPT-2 predicts "is" or "the" in those slots — "trivial" and "dire" are register-surprises the model detects.

The literal-epic paraphrase ("glorious things", "warlike causes") produces *lower* S₂ at key tokens (1.27, 2.04), because those words are conventionally expected after heroic setup.

### Larkin: The Cliché Conceals the Wound

"And add some **extra**, just for **you**" — the ironic tokens "extra" and "just" have S₂ = **−5.05** and **−2.88**.

GPT-2 predicted "more" for "extra" (top alternative) — these are functionally equivalent, and both are clichéd phrasing. The phrase "just for you" is so formulaic (gift-giving, promotional language) that the model predicts it essentially perfectly.

The ironic force of Larkin's closing line comes from applying the vocabulary of personal gifting to inherited psychological damage. But at the token level, the model sees only a string of very common words — the most "boring" S₂ in the poem.

### Housman: Understatement as High S₂

Housman's "To live and **shame** the land from which we sprung" — S₂ = **+10.85** at "shame."

GPT-2's top prediction: "**die**." The model expected the conventional war-poem sentiment ("To live and die for the land"). Housman writes "shame" instead — the word that says *dying was preferable to the dishonor of surviving*. This is not irony in the traditional sense but bitter understatement, and it registers as extreme surface surprise.

Meanwhile, "Life, to be **sure**, is nothing much to lose" — S₂ = **−4.90** at "sure." The hedge "to be sure" is extremely conventional, predicted by the model. The understatement is hidden in this token even as "shame" shouts.

---

## Two Mechanisms of Irony in S₂ Space

The data resolves into two distinct ironic strategies, with opposite S₂ signatures:

### Type 1: Allusive / Conventional Irony — HIDES in Low S₂

| Example | Key ironic token | S₂ |
|---------|-----------------|-----|
| Owen: "Dulce et decorum est" | "est" (×2) | −2.86, −3.53 |
| Larkin: "just for you" | "extra", "just" | −5.05, −2.88 |

Mechanism: Deploy a *recognized conventional phrase* (classical tag, cliché) in a context that inverts its meaning. GPT-2 predicts the phrase because it's high-frequency and formulaic. The semantic surprise is invisible to the surface model — it requires cultural competence to decode.

### Type 2: Register-Clash / Incongruity Irony — SHOWS as High S₂

| Example | Key ironic token | S₂ |
|---------|-----------------|-----|
| Pope: "mighty contests rise from trivial things" | "trivial" | +5.08 |
| Pope: "dire offence from am'rous causes" | "dire" | +6.46 |
| Housman: "To live and shame the land" | "shame" | +10.85 |

Mechanism: Place a semantically incongruous word into a context that creates register tension. The model predicts a contextually appropriate word ("die", "the", "is") and receives something that disrupts the register. The irony is visible as surface S₂ — but the model doesn't understand *why* it's surprising.

---

## Finding

**Verbal irony does not have a single S₂ signature — it has two opposing ones, depending on its mechanism:**

1. **Allusive irony** (quoting conventional phrases or deploying clichés to ironic ends): S₂ **below** the poem's baseline at ironic tokens. The irony is semantically invisible to the surface model. This is the "gap beneath the gap" — the Straussian gap operates between cultural knowledge and surface prediction, not between local context and token choice.

2. **Register-clash irony** (mock-heroic, bitter understatement): S₂ **above** baseline at ironic tokens. The model detects the register incongruity without comprehending the ironic intent. The Straussian gap is locally visible.

The aggregate key-token finding (ironic: 0.57 vs literal: 1.61, Δ = −1.05) is dominated by the allusive irony cases. The mock-heroic result runs counter to the main trend, complicating any single claim about irony and S₂.

---

## Theoretical Implications

The classic "Straussian gap" framing assumed that poets use high S₂ to encode surprise. But allusive irony inverts this: the poet uses *low* S₂ — conventional, expected language — as the vehicle of maximum semantic shock. Owen's decision to end the poem with the most *predictable* possible Latin phrase is the most radical choice in the poem.

This suggests a taxonomy of Straussian moves:
- **Active surprise**: poet writes unexpected token (high S₂) — standard Straussian gap
- **Passive irony**: poet writes expected token in semantically inverted context (low S₂, invisible to model) — irony that requires cultural literacy
- **Register incongruity**: poet writes unexpected register (high S₂, visible to model) — the model detects clash without understanding intent

---

## Suggested Next Steps

1. **Scale up**: Collect 20+ ironic poems across each type and test the two-mechanism taxonomy more rigorously
2. **Allusion detection**: Map all moments where S₂ is *very low* AND the token is part of a recognizable quoted phrase — these are candidate allusive ironies
3. **Mock-heroic vs. sincere heroic**: Extend the Pope analysis — does the full "Rape of the Lock" show systematically higher S₂ at incongruity tokens vs. sincere epic passages?
4. **Speaker reliability**: Does first-person unreliable narration in poetry follow the allusive or register-clash pattern?
5. **GPT-2 as cultural competence proxy**: Allusive irony depends on the model having memorized the alluded-to phrases. Can we test this — does irony based on *obscure* allusions have higher S₂ than irony based on *famous* ones (because the model doesn't recognize the obscure original)?
