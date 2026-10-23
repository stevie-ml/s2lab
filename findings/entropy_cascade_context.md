# Entropy Cascade: How Context Confidence Determines Whether Surprise Liberates or Anchors

**Date:** 2026-10-23  
**Experiments:** `experiments/entropy_after_surprise.py`, `experiments/entropy_after_surprise_v2.py`  
**Results:** `results/entropy_after_surprise.json`, `results/entropy_after_surprise_v2.json`  
**Corpus:** 328 texts, 40,205 consecutive artifact-cleaned token pairs  
**Builds on:** `s2_momentum_prose_poetry.md`, `confidence_trap_analysis.md`, `entropy_trajectory_analysis.md`

---

## Research Question

When a poet makes an unexpected choice (positive S₂ at position *t*), does this
**expand** the space of what can follow (liberation: more options, higher entropy at *t+1*)
or **contract** it (anchoring: fewer options, lower entropy at *t+1*)?

This experiment distinguishes two hypotheses:
- **Liberation hypothesis**: a surprising word departs from the predictable track, entering new semantic territory → GPT-2 becomes less certain about what follows
- **Anchoring hypothesis**: a surprising word establishes strong new context that makes subsequent tokens more constrained → GPT-2 becomes more certain about what follows

The twist: both effects exist simultaneously. Which one dominates depends on
**how certain the model was when the surprising choice was made**.

---

## Method

1. Load all 40,205 consecutive artifact-cleaned token pairs from 328 texts
2. Compute: S₂(t), entropy(t), entropy(t+1) for each pair
3. Compute partial correlation: r(S₂_t, Entropy_t+1 | Entropy_t)  
   This controls for the mathematical artifact (S₂ = surprisal − entropy implies
   low S₂ tokens occur in high-entropy contexts, which persist)
4. Split pairs by contextual certainty:
   - **Low entropy** at t (< 4 bits): model was confident
   - **Mid entropy** at t (4–7 bits): moderate uncertainty
   - **High entropy** at t (≥ 7 bits): model was highly uncertain

---

## Results

### 1. The Unconditional Correlation

| Correlation | r |
|-------------|---|
| r(S₂_t, Entropy_t+1) overall | **−0.1307** |
| partial r(S₂_t, Entropy_t+1 \| Entropy_t) | **−0.1252** |
| r(S₂_t, S₂_t+1) | **+0.0109** |
| r(Entropy_t, Entropy_t+1) | **+0.2537** |

After removing the mathematical confound (entropy at t), the partial correlation
is **−0.125**: surprise **slightly reduces** entropy at the next position, on average.
Entropy itself has stronger positive persistence (r=0.25).

---

### 2. The Context-Dependent Reversal

**This is the key finding.** The effect of a surprising choice on subsequent entropy
**completely reverses depending on contextual certainty:**

| Context | n | Mean Entropy_t | Effect Direction | Delta Entropy_t+1 | Partial r |
|---------|---|----------------|-----------------|-------------------|-----------|
| **Confident** (ent_t < 4) | 8,595 | 2.21 bits | **LIBERATION** | **+1.23 bits** | **+0.094** |
| **Moderate** (4 ≤ ent_t < 7) | 14,530 | 5.63 bits | **ANCHORING** | **−0.72 bits** | **−0.140** |
| **Uncertain** (ent_t ≥ 7) | 17,080 | 8.77 bits | **ANCHORING** | **−1.02 bits** | **−0.209** |

Reading the table:
- When the model was **confident** (low entropy context, e.g., after a common phrase), a
  **high-S₂ token** is followed by entropy +1.23 bits *higher* than a low-S₂ token in the same context.
  The surprising choice LIBERATES: it opens new territory with more possible continuations.

- When the model was **uncertain** (high entropy context, e.g., mid-sentence in complex syntax),
  a **high-S₂ token** is followed by entropy −1.02 bits *lower*.
  The surprising choice ANCHORS: it resolves ambiguity and establishes a clear trajectory.

---

### 3. Intuition: The Two Mechanisms

**Liberation (confident contexts):**  
The model is marching confidently down a well-worn syntactic/semantic path. A surprising
deviation is like stepping off that path into an open field — suddenly any direction is
equally possible. The model has no script for what follows an unexpected turn from a confident
context, so entropy explodes.

> *Example*: After "the flower" (confident: "of", "is", "blooms" expected), Dickinson writes
> "the flower remembered" — now anything can follow "remembered": "nothing", "the rain",
> "God", "me". Entropy after "remembered" would be high.

**Anchoring (uncertain contexts):**  
The model is already in uncertain territory — complex syntax, accumulating modifiers,
ambiguous reference. A surprising specific choice **pins the context**: it names something
concrete when the model had distributed probability across abstractions. This resolves
the ambiguity, establishing a strong frame for what follows.

> *Example*: After a long grammatically complex clause (high entropy), suddenly "Byzantium"
> appears — now the model knows exactly what world it's in, and the next token is more
> constrained: Byzantine imagery, proper nouns, specific historical register.

---

### 4. S₂ Bin Analysis: The Full Picture

| S₂ bin at t | n | Mean Entropy_t+1 | Mean S₂_t+1 |
|-------------|---|-----------------|-------------|
| Very negative (S₂ < −3) | 9,420 | **7.13** | −0.45 |
| Negative (−3 to 0) | 17,073 | **5.75** | −0.38 |
| Low positive (0 to 2) | 5,280 | **6.27** | −0.43 |
| Mid positive (2 to 5) | 4,848 | **6.06** | −0.43 |
| High positive (5 to 10) | 2,921 | **5.73** | −0.29 |
| Extreme (> 10) | 663 | **5.80** | −0.25 |

Note: The "very negative" bin's high entropy_next (7.13) is partly a mathematical consequence
— very negative S₂ tokens occur in already-high-entropy contexts (since S₂ = surprisal − entropy).
The partial correlation analysis above removes this confound.

**Regardless of S₂ level**, the next token has *negative* mean S₂ (−0.25 to −0.45). This
confirms the existing "negative autocorrelation" finding from `s2_momentum_prose_poetry.md`:
every token, however chosen, is followed by below-average S₂ on average.

---

### 5. S₂ Conservation: Poems Don't Have a "Surprise Budget"

A secondary test: do poems with high first-half S₂ compensate with lower second-half S₂?

**r(first-half avg S₂, second-half avg S₂) = +0.215** — a positive correlation.

This refutes the conservation hypothesis. A poem that is surprising in its first half tends
to remain surprising throughout. **High S₂ is a property of the poem (and poet), not a
resource that depletes.** Some poems maintain elevated surprise for their entire duration;
others don't, but this is stable across halves.

---

### 6. Era Profiles: Which Traditions Anchor vs. Liberate?

Partial r(S₂_t, Entropy_t+1 | Entropy_t) sorted by effect direction:

| Era | n | Partial r | Tendency |
|-----|---|-----------|----------|
| concrete | 114 | **+0.247** | Liberation |
| ballad | 909 | **+0.151** | Liberation |
| beat | 1,042 | **+0.103** | Liberation |
| song_lyrics | 538 | +0.006 | Neutral |
| oulipo | 484 | −0.045 | Mild anchoring |
| modernist | 2,764 | −0.065 | Mild anchoring |
| romantic | 2,464 | −0.186 | Anchoring |
| surrealist | 1,094 | −0.187 | Anchoring |
| dramatic_monologue | 2,561 | −0.190 | Anchoring |
| war_poetry | 636 | −0.242 | Strong anchoring |
| old_english | 414 | −0.252 | Strong anchoring |
| classical_chinese | 234 | −0.268 | Strong anchoring |
| german_modernist | 232 | −0.287 | Strong anchoring |
| deep_image | 60 | **−0.328** | Strongest anchoring |
| ghazal | 119 | **−0.340** | Strongest anchoring |

**Interpretation:**  
- **Liberation eras** (concrete, ballad, beat): Colloquial and/or rule-violating traditions where
  surprise disrupts established patterns, opening new territory.
- **Anchoring eras** (deep image, ghazal, old English, classical Chinese): Highly formalized or
  image-centered traditions where an unexpected image resolves semantic ambiguity rather than
  multiplying it. The surprising word in a ghazal or deep-image poem names a specific,
  concrete thing in an otherwise abstract or allusive context — it anchors rather than liberates.

---

## Interpretation: A Two-Phase Model of Surprise

These results suggest that S₂ operates via **two distinct mechanisms** depending on contextual
certainty:

1. **The Rupture** (confident context): When the model thinks it knows what's coming, a surprising
   choice shatters the model's confidence, spreading probability across new territory. This
   creates the "high S₂ → high entropy_next" liberation effect.

2. **The Pivot** (uncertain context): When the model is already at an interpretive crossroads,
   a surprising specific choice resolves the ambiguity in an unexpected direction. This
   creates the "high S₂ → low entropy_next" anchoring effect.

Poets who work in formal traditions (ghazal, old English) tend toward the Pivot model:
they exploit accumulated ambiguity to make a definitive, surprising commitment. Poets who
work in open forms (concrete, beat) tend toward the Rupture model: they shatter expected
trajectories to open multiple new paths.

---

## Suggested Next Steps

1. **Identify specific "rupture moments"** in individual poems: positions where confident-context
   surprise maximally expands entropy next. Map these to known poetic structures (volta, refrains).

2. **Test within individual poets**: does Dickinson consistently use the Rupture model while
   Yeats uses the Pivot? Could this distinguish poetic "strategies" at the individual level.

3. **Apply to prose**: does the context-dependent reversal hold in narrative prose?
   Prose may show a different profile since it operates at lower average S₂.

4. **Interaction with line position**: do ruptures concentrate at line beginnings (where the
   model is already confident about prosodic structure) and pivots at line endings?
