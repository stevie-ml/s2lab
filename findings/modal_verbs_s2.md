# Modal Verbs and the Conditional Register in Poetry: An Information-Theoretic Analysis

**Date:** 2026-09-17  
**Experiment:** `experiments/modal_verbs_s2.py`  
**Corpus:** 128 texts (123 poetry, 5 prose control)  
**Research question:** Do modal auxiliaries create distinctive S₂ patterns? And does the 'counterfactual window' (what follows a modal) show elevated surprise?

---

## Motivation

Modal verbs are the grammar of possibility: *would, could, might, shall, must, should, may, can, will, ought*. When a poet enters the modal register, they suspend commitment to fact — they open a hypothetical space. This makes modals structurally similar to the Straussian gap itself: both are about "what didn't happen" or "what might." 

**Hypothesis 1 (Modal Entry):** The poet's *entry* into the conditional register — the modal token itself — is a Straussian move: surprising in context.  
**Hypothesis 2 (Counterfactual Window):** What *follows* a modal (the actualization of the possibility) should be the most creative, high-S₂ position in the poem. GPT-2 knows only that something will actualize the modality, not what.

---

## Modal Classification

| Class | Tokens | Meaning |
|---|---|---|
| **Deontic** | must, should, ought | obligation / necessity |
| **Epistemic** | might, may | possibility / probability |
| **Volitional** | would, could, shall, will | hypothetical / counterfactual / futurity |
| **Capability** | can | ability |

---

## Key Results

### 1. Modal Token S₂ by Class

| Class | n | mean S₂ | pos% | max S₂ |
|---|---|---|---|---|
| **Epistemic** (might, may) | 7 | **+1.058** | 57.1% | 7.39 |
| **Volitional** (would/could/shall/will) | 40 | **+0.096** | 40.0% | 23.63 |
| Baseline (all non-modal tokens) | 6,748 | **+0.951** | 45.8% | 39.62 |
| **Capability** (can) | 8 | **−1.458** | 12.5% | 4.73 |
| **Deontic** (must/should/ought) | 14 | **−1.896** | 7.1% | 1.80 |

**Deontic and capability modals are deeply expected**: GPT-2 confidently predicts "must," "should," and "can" when they appear. Their S₂ is nearly 3 bits below baseline — among the most predictable tokens in the corpus.

**Epistemic modals are the most surprising**: "might" and "may" carry genuine information (+1.058), slightly above the volitional class.

### 2. The Critical Finding: A Split Within Volitional Modals

Disaggregating the volitional class reveals a dramatic divide:

| Modal word | n | mean S₂ | pos% |
|---|---|---|---|
| **could** | 11 | **+2.086** | 36.4% |
| **would** | 6 | **+1.828** | 83.3% |
| **may** | 6 | **+1.381** | 66.7% |
| will | 17 | −1.178 | 29.4% |
| can | 8 | −1.458 | 12.5% |
| shall | 6 | −1.672 | 33.3% |
| should | 6 | −1.830 | 0.0% |
| must | 7 | −1.951 | 14.3% |

**The conditional/past-tense forms ("could", "would") are highly surprising in poetry, while their simple present counterparts ("can", "will", "shall") are highly expected.** This split tracks a distinction that is semantically real but not often grammatically formalized:

- **"Would/could"** = suspended commitment; they appear in contexts where the model predicts a different grammatical category or word entirely. The poet's use of counterfactual grammar is itself a Straussian choice.
- **"Will/can/shall"** = direct futurity or simple ability; these are predicted with confidence by GPT-2 when the syntactic frame is established.

The high positive rate for "would" (83.3%) is especially notable: in *most* of its poetry occurrences, "would" is informationally surprising.

### 3. The Counterfactual Window: Hypothesis Refuted

**Hypothesis 2 is wrong.** Post-modal tokens are *less* surprising than the corpus baseline:

| Class | n | post mean S₂ | post pos% | modal entropy |
|---|---|---|---|---|
| Deontic | 14 | −0.270 | 57.1% | 7.008 |
| Volitional | 40 | −0.427 | 35.0% | 6.792 |
| Capability | 8 | −1.373 | 25.0% | 7.995 |
| **Epistemic** | 7 | **−2.696** | 14.3% | 5.406 |
| Corpus baseline | — | +0.201 | 35.6% | — |

After "might" or "may," the following word is extremely predictable (S₂ = −2.696). This makes grammatical sense: "might be," "might have," "might seem," "may be," "may have" — the complement of an epistemic modal is drawn from a very small, predictable set of verb forms.

This is the inverse of the Straussian pattern: **the modal opens a grammatical constraint, not a freedom.** The modal itself may be surprising (especially "could," "would") but it then locks in a narrow syntactic path. The "window" closes, not opens.

### 4. Top Post-Modal Straussian Moments

These are the highest-S₂ tokens immediately following a modal — rare exceptions where the modal is followed by something genuinely unexpected:

| Rank | Context | S₂ | Era |
|---|---|---|---|
| 1 | **shall Death** | +6.56 | Victorian |
| 2 | **would weave** | +5.77 | Victorian |
| 3 | **must expire** | +5.15 | Victorian |
| 4 | **must some** | +4.73 | Harlem Renaissance |
| 5 | **shall myself** | +4.13 | Contemporary |
| 6 | **would I** | +3.93 | Prose Poetry |
| 7 | **shall assume** | +3.40 | 19th Century |
| 8 | **will come** | +3.17 | Romantic |
| 9 | **will feed** | +2.99 | New York School |

**Victorian poetry dominates the high-S₂ post-modal list.** Victorian poets favor inversions after modals ("shall Death" — personified and capitalized) and archaic/unexpected verb choices ("must expire," "would weave").

Most surprising post-modal patterns:
- **"shall Death"** (Christina Rossetti's "Remember"): GPT-2 expects a bare infinitive after "shall" ("shall be," "shall have"). Capitalizing "Death" and using it as a noun inverts the expected grammatical structure.
- **"would weave"** (Victorian): an unexpected verb choice at high model confidence.
- **"must expire"** (Victorian): the deontic "must" unexpectedly followed by an archaic Latinate verb.

### 5. Class Distribution at High- vs. Low-S₂ Post-Modal Moments

At the highest-S₂ post-modal positions, **volitional modals dominate (73.3%)**:

| | High-S₂ post-modal (>2.0) | Low-S₂ post-modal (<−1.0) |
|---|---|---|
| Volitional | **73.3%** | 56.4% |
| Deontic | 20.0% | 15.4% |
| Epistemic | 6.7% | 15.4% |
| Capability | 0.0% | 12.8% |

When a post-modal moment *is* surprising, it's almost always after a volitional modal. This suggests "would/could/shall" create the most creative space even if the average post-modal is predictable.

### 6. Era-Level Modal S₂

Which literary traditions use modal verbs most surprisingly?

| Era | n | mean S₂ |
|---|---|---|
| **Romantic** | 9 | **+1.616** |
| **New York School** | 10 | **+0.437** |
| Harlem Renaissance | 6 | −0.405 |
| 19th Century | 5 | −0.414 |
| Ballad | 3 | −0.490 |
| Victorian | 19 | −1.239 |
| Song lyrics | 4 | −1.275 |
| Modernist | 4 | −1.287 |
| **Contemporary** | 4 | **−2.176** |

**Romantic poetry uses modals most surprisingly** (mean S₂ = +1.616). Keats, Shelley, and Wordsworth deploy "would," "could," and "might" in contexts where GPT-2 expects something else. This is consistent with the Romantic valorization of subjunctivity — the elevated mode of hypothetical longing.

**Contemporary poetry uses modals most predictably** (mean S₂ = −2.176). This tracks contemporary poetry's embrace of plain speech and everyday register — modal verbs are used conversationally, in contexts where they are grammatically expected.

### 7. High Modal Density Poems

Poems with the most modal verbs per token:

| Poem | Era | Modal density | Mean poem S₂ |
|---|---|---|---|
| "Remember" (Rossetti) | Victorian | 3.6% | +0.086 |
| "Sonnet 18 (Shall I compare thee)" | Victorian | 3.1% | −0.452 |
| "The Day Lady Died" | New York School | 3.0% | +0.519 |
| "If We Must Die" (McKay) | Harlem Renaissance | 2.5% | −0.047 |

**The highest-modal-density poems are not the highest-S₂ poems** — using many modals seems to pull poem S₂ toward the lower end (average: "mid" density group has mean S₂ = 0.093, but "low" group has mean S₂ = 0.293). Heavy modal use seems to be a *closing* strategy rather than an *opening* one.

---

## Summary of Findings

1. **The conditional/past-tense split**: "Could" and "would" are **informationally surprising** in poetry (mean S₂ = +2.09, +1.83), while "can," "will," "shall," "should," "must" are **highly expected** (S₂ negative across the board). This tracks their semantic function: counterfactual/conditional modals signal the poet's *deviation* from default assertion, while simple-form modals are grammatically predictable in context.

2. **The counterfactual window is narrow, not open**: Despite the modal opening a hypothetical space, post-modal tokens are *less* surprising than baseline. The modal constrains, not liberates. The creative move is the modal itself, not what follows.

3. **Romantic poetry uses modals most Straussianly**: The Romantic tradition's investment in subjunctive longing ("I would," "could not," "might yet") deploys modals in surprising contexts, consistent with the era's valorization of hypothetical and counter-to-fact states.

4. **Victorian personification strategies**: The top post-modal surprises are dominated by Victorian poems using modals to introduce personified abstractions ("shall Death") or archaic verb choices, creating the highest-S₂ modal-complement moments.

---

## Suggested Next Steps

1. **Conditional clause analysis**: Look at full conditional constructions ("if... then") — does the apodosis (main clause with modal) show systematically different S₂ than the protasis (the "if" clause)?

2. **Negated modals**: "Would not," "could not," "shall not" — double negation in the hypothetical space. Does the negation compound the surprise?

3. **Archaic modals in contemporary poetry**: "Shall" in a contemporary poem may be a deliberate archaism (itself a Straussian move). Can we detect "register incongruity" via S₂?

4. **The "wishing" hypothesis**: Verbs of desire/volition (wish, hope, want) might parallel modal behavior — they also open hypothetical space. Compare their S₂ profiles to modals.
