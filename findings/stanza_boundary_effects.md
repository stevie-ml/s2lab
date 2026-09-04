# Stanza Boundary Effects: The Stanza Paradox

**Date:** 2026-09-04  
**Experiment:** `experiments/stanza_boundary_experiment.py`  
**Corpus:** 27 English poems with explicit stanza breaks (from 89-poem corpus)

---

## Research Question

The line-position experiment established that line-initial tokens have dramatically
higher S₂ (+5.57) than medial or final positions. But a stanza break is a *stronger*
structural boundary than a line break — it introduces silence, white space, and a
semantic reset. Do stanza-initial tokens show *even higher* S₂?

**H1 (Stanza Amplification):** Stanza-initial tokens have higher S₂ than mid-stanza
line-initial tokens.  
**H2 (Stanza Closure):** The final line of a stanza has lower average S₂ than
non-final stanza lines.  
**H3 (Stanza Arc):** S₂ follows an arc within each stanza: high at line openings,
low at line endings, with stanza boundaries acting as resolution points.

---

## Results: The Stanza Paradox

| Position | N | Avg Surprisal | Avg Entropy | **Avg S₂** | +S₂ Ratio |
|---|---|---|---|---|---|
| **Mid-stanza line-initial** (enjambment) | 182 | 16.84 | 3.11 | **+13.73** | 86.8% |
| Stanza-final line-initial (last line opening) | 45 | 13.93 | 4.02 | **+9.91** | 68.9% |
| **Stanza-initial** (first token of new stanza) | 46 | 7.07 | 7.43 | **−0.37** | 41.3% |
| Medial | 2220 | 5.99 | 6.34 | **−0.36** | 33.7% |
| Stanza-initial, line-final (last word of stanza's first line) | 45 | 5.71 | 6.12 | **−0.41** | 44.4% |
| Line-final (mid-stanza) | 182 | 4.96 | 5.70 | **−0.74** | 25.3% |
| **Stanza-final line-final** (last word before stanza break) | 43 | 3.61 | 5.19 | **−1.58** | 11.6% |

**H1 is REJECTED.** Stanza-initial tokens have *negative* average S₂ (−0.37) —
virtually identical to medial positions. **Mid-stanza line-initial tokens are vastly
more surprising (+13.73)**. The stronger boundary does NOT produce more surprise.

**H2 is CONFIRMED.** Stanza-final positions are the most predictable tokens in the
corpus. The last word before a stanza break averages S₂ = −1.58, with only 11.6%
positive S₂ — the strongest "closure" signal in the data.

---

## The Mechanism: Entropy Governs Surprise Exploitation

The key to understanding this paradox lies in entropy:

**At stanza breaks**, GPT-2 has HIGH entropy (7.43 bits). The model has just
finished processing a complete stanza and faces high uncertainty about how the
next stanza will begin. Because GPT-2 is uncertain, poets can satisfy it with
relatively conventional language — and they do. The actual surprisal (7.07) falls
*below* the model's uncertainty, yielding negative S₂.

**At mid-stanza line breaks**, GPT-2 has LOW entropy (3.11 bits). The model is
mid-sentence, following grammatical structure with high confidence — it "knows"
what word should come next. Poets exploit this certainty: by breaking the line
and choosing an unexpected word, they violate the model's confident prediction.
The actual surprisal (16.84) dramatically exceeds the model's low entropy, yielding
massive positive S₂ (+13.73).

**The core principle:** S₂ spikes when a poet defies a *confident* prediction, not
an uncertain one. Structural surprise (stanza break) correlates with model
uncertainty; grammatical surprise (enjambment) correlates with model confidence.

> "The most forceful Straussian move is not at the moment of maximum openness,
> but at the moment of maximum closure — when the model is most sure, and the poet
> refuses."

---

## Poem-Level Evidence: 27/27 Poems Confirm the Pattern

Across all 27 poems with stanza breaks, the stanza-initial average S₂ is
**lower than** the mid-stanza line-initial average S₂. The effect is 100% directionally
consistent, despite small N per poem.

| Poem | Stanza-Initial Avg S₂ | Mid-Stanza Line-Initial Avg S₂ | Δ |
|---|---|---|---|
| Daddy (Plath) | +7.89 | +12.47 | −4.58 |
| The Windhover (Hopkins) | +5.03 | +9.68 | −4.65 |
| Convergence of the Twain (Hardy) | +4.16 | +16.55 | −12.39 |
| The Raven, opening (Poe) | +3.89 | +13.28 | −9.39 |
| Harlem (Hughes) | −0.15 | +27.52 | −27.66 |
| We Real Cool (Brooks) | +0.12 | +19.05 | −18.94 |
| I felt a Funeral (Dickinson) | −4.36 | +15.23 | −19.59 |

The smallest gap (Plath's *Daddy*) is −4.58 bits. The average gap across all poems
is approximately −14 bits. No poem reverses the pattern.

---

## Top Stanza-Opening Moments

Even though stanza-initial tokens average negative S₂, the highest individual
stanza openings are still notable:

| S₂ | Token | Poem |
|---|---|---|
| +7.89 | **"Daddy"** | Plath, *Daddy* — the poem's title as its own stanza opener |
| +7.10 | **"Aut"** | Basho, *Three Haiku* — each haiku is a stanza, word = "Autumn" |
| +6.49 | **"Steel"** | Hardy, *Convergence of the Twain* — cold, harsh pivot word |
| +5.03 | **"Br"** | Hopkins, *The Windhover* — "Brute beauty and valour…" |
| +3.89 | **"Ah"** | Poe, *The Raven* — emotional apostrophe |

These high outliers tend to be cases where the poet's stanza-opening word is
itself the poem's central image or an exclamatory particle — i.e., where the
stanza opening IS the semantic surprise rather than structural.

---

## The S₂ Arc Within a Stanza

Reading S₂ through a stanza's positions reveals a consistent arc:

```
Stanza opening:          S₂ ≈ −0.37  (conventional, grounding)
    ↓ first line ends:   S₂ ≈ −0.41  (still predictable)
Mid-stanza lines open:   S₂ ≈ +13.73 *** (maximum surprise via enjambment)
Mid-stanza lines close:  S₂ ≈ −0.74  (landing, conventional)
Last line opens:         S₂ ≈ +9.91  (surprise before closure)
Last line closes:        S₂ ≈ −1.58  (strongest closure in data)
    ↓ [stanza break]
Next stanza opening:     S₂ ≈ −0.37  (reset to conventional)
```

The stanza is an information-theoretic unit with a characteristic "V-shape":
- starts low (conventional opening)
- climbs through enjambment surprise
- lands low (stanza-closing predictability)

---

## Implications

**For the Straussian gap framework:** The analysis confirms that S₂ spikes mark
moments of *exploited confidence*, not *exploited openness*. Poets use structural
boundaries to create openness, then use the model's grammatical certainty *within*
that structure to create surprise.

**For computational poetics:** Stanza segmentation alone does not predict S₂
peaks. Enjambment detection (identifying where a sentence continues across a line
break) is a better predictor of high-S₂ moments than stanza-boundary detection.

**For close reading:** When S₂ is high at a stanza opening, it signals unusual
behavior — the poet is not using the stanza break for cognitive grounding, but for
semantic shock (as in Plath's *Daddy*). Low stanza-initial S₂ is normal; high
stanza-initial S₂ marks a formal strategy.

---

## Limitations & Caveats

- Only 27 poems with explicit stanza breaks (`\n\n`) in the corpus. N=46 for
  stanza-initial is sufficient for directional findings but not fine-grained analysis.
- GPT-2's context window treats all prior text equally; it cannot "feel" the
  stanza break as a human reader does.
- The very high mid-stanza line-initial averages (+13.73) partly reflect a few
  extreme enjambment cases (e.g., Hughes' *Harlem* at +27.52). Median would be
  more robust; direction is unaffected.

---

## Next Steps

1. **Add more multi-stanza poems** to increase N at stanza boundaries.
2. **Enjambment tagging**: Formally identify run-on lines vs. end-stopped lines
   and test whether enjambed line-initials drive the +13.73 average.
3. **Stanza arc by length**: Does the arc shape differ for 2-line vs. 6-line stanzas?
4. **Compare stanza-initial types**: Opening with a content word (image) vs.
   a function word (continuation) — does the word class predict stanza-initial S₂?
