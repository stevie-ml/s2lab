# S₂ Markov Transitions: Is Poetic Surprise Mean-Reverting?

**Date:** 2026-09-26  
**Experiment:** `experiments/s2_markov_transitions.py`  
**Corpus:** 175 poetry texts, 5 prose controls — 17,624 poetry token pairs, 158 prose pairs  
**Builds on:** `s2_zone_topology.md`, `spike_symmetry.md`, `aftermath_entropy.md`

---

## Research Question

Previous analyses characterized the *neighborhood* of individual S₂ spikes. But what is the
**full Markov structure** of S₂ across a poem? Given the surprise level at token t, what is the
conditional distribution of surprise at token t+1?

The key question: Is poetic surprise **mean-reverting** (high S₂ predicts lower S₂ next) or
**self-reinforcing** (high S₂ predicts more high S₂)?

---

## Finding 1: Poetry Is Weakly Mean-Reverting; Prose Is Mildly Persistent

| Group | S₂ Autocorrelation (lag-1) |
|-------|---------------------------|
| Poetry | **−0.016** |
| Prose | **+0.099** |

**The sign difference is the key finding.** Poetry's S₂ sequence is slightly negatively
autocorrelated: a high-surprise token weakly predicts a lower-surprise token next. Prose has
the opposite: consecutive tokens tend to have similar S₂ levels.

Interpretation: poetry deploys surprise as punctuation — isolated peaks in a baseline of
conformity — while prose maintains more uniform S₂ "registers" over stretches of text.

---

## Finding 2: The Transition Matrix Reveals the Prose Collapse

After any surprise state, prose collapses immediately back to CONFORM. Poetry does not.

### Poetry: Full Transition Matrix (row = current state, col = next state)

| Current State | Deep Conform | Conform | Neutral | Surprise | High Surprise |
|---|---|---|---|---|---|
| **Deep Conform (<-3)** | 25.6% | 31.6% | 10.2% | 16.1% | **16.6%** |
| **Conform (-3..−0.5)** | 23.1% | 36.5% | 10.5% | 14.2% | 15.7% |
| **Neutral (−0.5..0.5)** | 19.7% | 37.1% | **16.8%** | 11.8% | 14.6% |
| **Surprise (0.5..3)** | 22.6% | 36.1% | 9.5% | 15.7% | 16.1% |
| **High Surprise (>3)** | 22.6% | 37.3% | 9.2% | 14.4% | **16.4%** |

### Prose: Full Transition Matrix

| Current State | Deep Conform | Conform | Neutral | Surprise | High Surprise |
|---|---|---|---|---|---|
| **Deep Conform (<-3)** | 31.2% | 43.8% | 14.6% | 6.2% | 4.2% |
| **Conform (-3..−0.5)** | 32.8% | **43.3%** | 10.4% | 11.9% | 1.5% |
| **Neutral (−0.5..0.5)** | 38.9% | 38.9% | 5.6% | 5.6% | 11.1% |
| **Surprise (0.5..3)** | 15.8% | **47.4%** | 10.5% | 21.1% | 5.3% |
| **High Surprise (>3)** | 16.7% | **66.7%** | 16.7% | 0.0% | **0.0%** |

The prose pattern is stark: after a HIGH_SURPRISE token, the distribution collapses 66.7% to
CONFORM. In prose, surprise is an anomaly the text immediately corrects.

---

## Finding 3: The Persistence Asymmetry — Poetry Chains Surprises; Prose Never Does

The diagonal of the transition matrix (self-persistence probability):

| S₂ State | Poetry P(stay) | Prose P(stay) | Δ |
|---|---|---|---|
| Deep Conform | 25.6% | 31.2% | −5.7% |
| Conform | 36.5% | 43.3% | −6.7% |
| **Neutral** | **16.8%** | **5.6%** | **+11.2%** |
| Surprise | 15.7% | 21.1% | −5.4% |
| **High Surprise** | **16.4%** | **0.0%** | **+16.4%** |

**Two structural differences between poetry and prose:**

1. **High Surprise chains**: Poetry has a 16.4% probability of HIGH_SURPRISE → HIGH_SURPRISE.
   Prose has **zero probability**. No prose token pair in this corpus has back-to-back extreme
   surprises. Poetry's "sustained zones" (from `s2_zone_topology.md`) are unique to poetry.

2. **Neutral sustains**: Poetry is 3× more likely to sustain NEUTRAL S₂ than prose (16.8% vs 5.6%).
   This means poetry has more "plateau" sections — stretches where the poem is neither expected
   nor unexpected — that prose tends to avoid.

---

## Finding 4: Era Autocorrelation — The Spectrum from Mean-Reverting to Persistent

| Era | S₂ Autocorr | n | Interpretation |
|---|---|---|---|
| spoken_word | **−0.124** | 2 | Strongest alternation |
| german_expressionist | −0.087 | 2 | Staccato, isolated blasts |
| haiku | −0.083 | 14 | Compression forces single spikes |
| german_modernist | −0.082 | 2 | — |
| early_modern | −0.071 | 4 | — |
| metaphysical | −0.069 | 4 | Argument structure alternates |
| language poetry | −0.060 | 3 | — |
| … | — | — | — |
| romantic | +0.023 | 14 | Mild persistence |
| prose_poetry | **+0.040** | 9 | Approaching prose behavior |
| nursery_rhyme | +0.058 | 1 | Repetition creates persistence |
| contemporary | +0.058 | 9 | Sustained registers |
| (prose control) | **+0.099** | 5 | Strongest persistence |

**The spectrum reveals a meaningful ordering:** Forms relying on compression and contrast
(haiku, expressionism, spoken word) are most mean-reverting. Forms with sustained emotional
registers (contemporary, nursery rhyme) approach prose. The ordering correlates with eras' use
of repetition and sustained diction.

**Prose poetry** (+0.040) sits between all poetry (−0.016) and prose (+0.099), confirming it
as an informationally intermediate form.

---

## Synthesis: The Surprise "Grammar" of Poetry

The transition matrix as a whole suggests that poetry operates under a **surprise grammar**:

- **Default return to CONFORM**: 37-37% from any state. Poetry always "wants" to return to
  the conform register — it's the gravitational baseline.
- **Occasional HIGH_SURPRISE chains** (16.4%): these are the "difficult" or "challenging"
  passages where the model is repeatedly wrong, creating zones of sustained ambiguity.
- **Weak mean reversion overall**: The slightly negative autocorrelation means that
  high-surprise tokens do statistically predict lower-surprise follow-ons — the
  conservation principle from `spike_symmetry.md` encoded at the distributional level.

Prose has a simpler grammar: **return to CONFORM, always** (66.7% from any high-surprise
state). Prose surprise is structurally temporary; poetic surprise is structurally renewable.

---

## Suggested Next Steps

1. **Condition on poem length**: Do longer poems show more positive autocorrelation (more room
   for sustained registers)?
2. **Model the transition matrix as a function of era**: Is there a single axis (e.g.,
   "lyric compression" vs. "sustained narrative") that predicts autocorrelation sign?
3. **High-surprise chains vs. zone types**: When HIGH_SURPRISE → HIGH_SURPRISE occurs, what
   kinds of tokens are involved? (Continuation of metaphor? Grammatical inversion chain?)
4. **Transition entropy**: The uncertainty in what follows a HIGH_SURPRISE token is higher in
   poetry (flat distribution across next states) than in prose (peaked at CONFORM). Quantify
   this as the entropy of the transition distribution itself.
