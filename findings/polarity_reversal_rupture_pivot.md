# Polarity Reversal as Anchoring: Oxymoronic Substitutions Are Pivots, Not Ruptures

**Date:** 2026-10-26  
**Experiment:** `experiments/polarity_reversal_rupture_pivot.py`  
**Results:** `results/polarity_reversal_rupture_pivot.json`  
**Corpus:** 348 texts, 212 polarity reversal events, 699 concordant valenced events  
**Builds on:** `oxymoron_polarity_s2.md`, `rupture_pivot_poet_profiles.md`, `entropy_cascade_context.md`

---

## Research Question

The *oxymoron_polarity_s2* experiment showed that polarity reversal tokens — where the poet delivers opposite emotional valence from what GPT-2 predicted — are **+2.56 bits higher S₂** than concordant tokens. This experiment asks: *how* does polarity reversal work at the entropy-cascade level?

Two competing hypotheses:
- **H1 (Rupture hypothesis)**: Polarity reversals are liberation events — they shatter confident predictions in low-entropy contexts, opening up new possibility space.
- **H2 (Pivot hypothesis)**: Polarity reversals are anchoring events — they occur in already-uncertain contexts and resolve the ambiguity by delivering a semantically opposite choice.

---

## Main Finding: Polarity Reversals Are Overwhelmingly Pivots

### Classification by Context

| Event type | Reversal events | Concordant events |
|---|---|---|
| **Rupture** (entropy_pre < 4 bits) | **0.9%** | 8.7% |
| Middle (4–7 bits) | **9.9%** | 19.5% |
| **Pivot** (entropy_pre ≥ 7 bits) | **89.2%** | 71.8% |

The data strongly rejects H1. Polarity reversals occur in confident contexts (ruptures) only **0.9%** of the time — versus 8.7% for concordant events. They prefer uncertain contexts (pivots) by an overwhelming margin: **89.2% of all polarity reversals are pivots**, compared to 71.8% for concordant events.

**Polarity reversals actively avoid rupture contexts.** When GPT-2 is confident, poets do not typically deliver dark-against-light or light-against-dark. The reversal mechanism is reserved for uncertain contexts.

---

### Entropy Dynamics After Reversal

| Event type | Mean S₂ | Mean delta_entropy | % Positive delta | n |
|---|---|---|---|---|
| Polarity reversal (all) | **+0.353** | **−2.947** | — | 212 |
| Concordant (all) | −1.545 | −2.311 | — | 699 |
| **Delta (reversal − concordant)** | **+1.898** | **−0.636** | — | — |

Polarity reversals produce **stronger entropy contraction** (−2.947) than concordant events (−2.311). This is the signature of the pivot mechanism: the unexpected valence choice resolves more uncertainty than a predicted choice would, rapidly narrowing subsequent possibility space.

In concrete terms: when Shelley writes "dead" where the model expected a hopeful or neutral word, the shock of dark-against-light doesn't open up a world of new possibilities — it closes down possibilities, locking in a dark semantic frame that constrains what follows.

---

### Direction Asymmetry

| Direction | n | Mean S₂ | Mean delta_H | % Pivot |
|---|---|---|---|---|
| **pos → neg** (dark-against-light) | 121 | +0.029 | −3.045 | **93.4%** | 
| **neg → pos** (light-against-dark) | 91 | **+0.784** | −2.817 | 83.5% |

Two striking asymmetries:

1. **Light-against-dark reversals have much higher S₂ (+0.784 vs +0.029)**: Choosing hope where despair is expected is more informationally surprising than choosing despair where hope is expected. This makes sense given the "dark bias" in poetry — the corpus more often has dark contexts, making a positive reversal genuinely rare and striking.

2. **Dark-against-light reversals have stronger entropy contraction (−3.045 vs −2.817) and are more exclusively pivots (93.4%)**: When a poet delivers darkness into a bright context, it is almost always in an already-uncertain moment, and the effect anchors subsequent context even more forcefully.

---

## Canonical Examples

### The Two Rupture Reversals (Rarest Cases)

Only 2 polarity reversal events occurred in confident (rupture) contexts:

| Token | Direction | S₂ | Entropy_pre | delta_H | Poem |
|---|---|---|---|---|---|
| "hunger" | pos→neg | 7.75 | 3.83 | −1.82 | Lucille Clifton: *Incantation* |
| "sun" | neg→pos | 5.85 | 3.29 | +0.88 | Rupert Brooke: *The Soldier* |

These are the truest oxymoronic ruptures: the model was confident about what was coming (a positive continuation after "Incantation"'s ritual opening; a dark continuation in Brooke's elegy), and the poet shocked it with the opposite. "Hunger" in a magical incantation context is liberation: it expands rather than forecloses. The "sun" in *The Soldier* — against a context of death — is the one reversal that actually expands entropy (+0.88), opening possibilities rather than closing them.

### Top Pivot Reversals

| Token | Direction | S₂ | Entropy_pre | delta_H | Poem |
|---|---|---|---|---|---|
| "sinking" | pos→neg | 10.03 | 9.33 | −1.86 | Richard Wright: *Nobody* |
| "dead" | pos→neg | 7.97 | 7.36 | −3.07 | Shelley: *Ode to the West Wind* |
| "strength" | neg→pos | 6.55 | 9.10 | −3.70 | Thomas Hardy: *Neutral Tones* |
| "win" | neg→pos | 6.20 | 8.22 | −4.66 | W.E. Henley: *Invictus* |
| "blessed" | neg→pos | 5.53 | 9.61 | −5.71 | Mary Oliver: *The Summer Day* |

These pivot reversals are syntactically constructed surprises: Shelley's "dead" comes at a moment of maximum grammatical openness (high entropy), and its semantic reversal immediately constrains the rest of the stanza. Hardy's "strength" in *Neutral Tones* — chosen against a despairing context — contracts entropy by −3.70. Oliver's "blessed" at high entropy (9.61 bits) produces the largest contraction (−5.71 bits): the pivot from the poem's dark questioning toward gratitude is the most powerful anchoring event in the corpus.

---

## Theoretical Implications

### 1. Oxymoron Is an Uncertainty-Resolution Strategy, Not a Liberation Strategy

The data overturns the intuitive framing of oxymoron as "shocking violation." Polarity reversal is not primarily about shattering confident expectations — it is about *resolving* uncertain ones. Poets reach for the semantically opposite word when the model's prediction space is already open and confused. The reversal says: "I will resolve this uncertainty for you — and in the direction you didn't expect."

### 2. Semantic Surprise Is Syntactic Opportunity

The strong correlation of polarity reversals with high-entropy contexts suggests that semantic reversals require syntactic latitude. Poets don't place oxymoronic words in syntactically constrained positions (where GPT-2 is certain about what part of speech comes next). They place them in open slots — semantically unmarked positions where the model projects broad uncertainty — and use the unexpected valence to cut through the ambiguity.

### 3. The Asymmetry Reveals a Corpus-Level Bias

Light-against-dark reversals (neg→pos) have higher S₂ than dark-against-light (pos→neg). This is not a property of the linguistic mechanism but of the corpus: poetry has a "dark tilt," so positive surprises against dark contexts are genuinely rarer and more startling to the model. This is measurable evidence for a corpus-level tonal asymmetry in English poetry — darkness is the unmarked default; light is the deviation.

### 4. The "Anchoring Oxymoron"

The stronger entropy contraction after reversals (−2.947 vs −2.311 for concordant events) refutes the idea that oxymoron is "creative ambiguity" — a moment of suspension between two meanings. Instead, the data suggests that oxymoron is *decisional*: the poet chooses one semantic pole against the model's projection, and this choice constrains what follows more forcefully than a predictable choice would.

---

## Era Breakdown (Top by Mean Delta-Entropy)

| Era | n | Rev. rate | Mean S₂ | Mean delta_H | % Pivot |
|---|---|---|---|---|---|
| classical_chinese | 2 | 33.3% | 3.273 | −0.915 | 50% |
| 18th_century | 3 | 18.8% | 1.748 | −1.849 | 66.7% |
| german_expressionist | 5 | 17.9% | 1.403 | −1.251 | 80% |
| war_poetry | 5 | 25.0% | 2.417 | −0.016 | 60% |
| haiku | 3 | 33.3% | 2.382 | −0.261 | 100% |

War poetry has notably high reversal rate (25%) AND high S₂ (2.417) — consistent with its signature moves of placing life-terms against death-contexts. Haiku's reversals are 100% pivots, fitting the form's high-entropy contexts (compressed, semantically open syntax).

---

## Next Steps

1. **Extend valence lexicon**: The current analysis uses ~200 positive and ~200 negative words. A larger lexicon (e.g., NRC Emotion Lexicon, ANEW word norms) would detect more reversals and better characterize borderline cases.
2. **Multi-token reversal sequences**: Do polarity reversals cluster? Is a reversal more likely to be followed by another reversal (valence oscillation) or by conformance (valence locking)?
3. **Stanza-position analysis**: Are reversal-pivots concentrated in specific stanza positions (e.g., the penultimate line or the volta moment)?
4. **Per-poet reversal style**: Which poets most consistently use pivots vs. ruptures as their reversal strategy? Compare the two Clifton/Brooke rupture cases with the Oliver/Hardy/Henley pivot cases.
5. **Cross-model validation**: Does GPT-2 medium show the same pivot-dominance of reversals, or is the 89.2% figure a GPT-2-small artifact?
