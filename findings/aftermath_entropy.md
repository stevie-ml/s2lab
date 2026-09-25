# Aftermath Entropy: Does Poetic Surprise Crystallize or Dissolve?

**Date:** 2026-09-25  
**Experiment:** `experiments/aftermath_entropy.py`  
**Corpus:** 173 English poems (control excluded), 17,418 interior token positions  
**Builds on:** `surprise_decay_curves.md`, `pre_peak_setup.md`

---

## Research Question

After a high-S₂ token — a word the model didn't expect — does the surprise
**crystallize** (drop the next token's entropy, giving GPT-2 a more specific context to work from)
or **dissolve** (raise the next token's entropy, leaving the model less certain about what must follow)?

**ΔH = entropy(t+1) − entropy(t)**
- ΔH < 0 → *crystallizing*: the surprising word narrowed future uncertainty
- ΔH > 0 → *dissolving*: the surprising word opened future possibility

---

## Key Finding: A Bifurcation at S₂ ≈ 9–10

| S₂ Bucket | n | Mean ΔH | % Crystallize (ΔH<−0.5) | % Dissolve (ΔH>+0.5) |
|---|---|---|---|---|
| S₂ 3.0–4.2 | 783 | **−1.27** | **58.9%** | 27.7% |
| S₂ 4.2–6.0 | 783 | **−1.28** | **58.4%** | 28.5% |
| S₂ 6.0–9.5 | 783 | **−0.53** | **50.7%** | 34.5% |
| S₂ > 9.5   | 783 | **+4.80** | 13.4% | **79.8%** |

**Moderate surprise crystallizes. Extreme surprise dissolves.**

Up to S₂ ≈ 9, surprising tokens tend to *narrow* subsequent uncertainty — a surprising noun or adjective commits the poem to a specific direction that the model can partially anticipate. Above S₂ ≈ 9.5, the pattern *reverses completely*: 4 out of 5 extreme surprises dissolve context, leaving GPT-2 adrift.

---

## Global Numbers

| Group | n | Mean ΔH | Median ΔH | % H rises |
|---|---|---|---|---|
| Spike S₂ ≥ 3.0 | 3,132 | +0.43 | −0.12 | 48.5% |
| High spike S₂ ≥ 6.0 | 1,561 | +2.14 | +1.37 | 62.4% |
| Negative S₂ ≤ −3.0 | 3,946 | −0.36 | +0.18 | 52.4% |
| Neutral \|S₂\| < 1.5 | 5,388 | +0.01 | −0.07 | 48.5% |

The mean at moderate spikes is misleading: the *median* is −0.12 (crystallizing), but the mean is pulled positive by extreme-S₂ outliers. The bifurcation at S₂ ≈ 9.5 explains both numbers.

---

## What Tokens Crystallize vs. Dissolve?

### Crystallizing surprises
The top crystallizing tokens are **concrete nouns and sensory adjectives**:
`survey`, `air`, `dry`, `plain`, `summer`, `sweet`, `fair`, `prayer`, `nest`

These words, when surprising, specify a semantic field. "Nest" appearing where the model expected something abstract commits the poem to birds/shelter/nature and actually *narrows* what GPT-2 expects to follow (mean ΔH = −7.89).

### Dissolving surprises
The top dissolving tokens are overwhelmingly **function words and discourse connectives**:
`and`, `the`, `in`, `that`, `but`, `for`, `to`, `being`, `he`, `my`, `when`, `like`

These are syntactic open-frames: a surprising "and" (mean ΔH = +7.55) or a surprising "the" (mean ΔH = +9.42) introduces a new clause without committing to its content. After a function word that breaks expectation, GPT-2 has no lexical anchor for what noun/verb follows — maximal uncertainty.

**Summary: crystallizing = content words, dissolving = function words**

---

## Era Breakdown (sorted by mean ΔH)

| Era | n spikes | Mean ΔH | % Cryst | % Diss |
|---|---|---|---|---|
| **beat** | 41 | **−1.36** | **61.0%** | 22.0% |
| 18th_century | 37 | −0.81 | 48.6% | 40.5% |
| language | 34 | −0.57 | 52.9% | 38.2% |
| spoken_word | 32 | −0.40 | 46.9% | 40.6% |
| new_york_school | 245 | −0.15 | 52.2% | 37.1% |
| metaphysical | 90 | −0.12 | 54.4% | 33.3% |
| found_poetry | 119 | −0.10 | 46.2% | 39.5% |
| romantic | 348 | +0.04 | 48.6% | 38.8% |
| victorian | 406 | +0.23 | 47.0% | 41.1% |
| modernist | 306 | +0.62 | 45.1% | 44.4% |
| song_lyrics | 89 | +0.93 | 36.0% | 47.2% |
| fixed_form | 190 | +1.21 | 38.4% | **50.5%** |
| haiku | 37 | +2.22 | 32.4% | 56.8% |
| **ballad** | 194 | **+2.26** | 26.3% | **61.3%** |

**Beat poetry crystallizes most**: Ginsberg's surprises tend to be content-word pivots that commit the poem to a specific direction.  
**Ballads and haiku dissolve most**: The unexpected moment in a ballad or at the kireji opens narrative/receptive space rather than closing it.

The metaphysical poets (Donne, Herbert) are also crystallizing — their conceits work by surprising specificity that then commits you to elaborating one metaphor.

---

## Interpretation: Two Modes of Surprise

The bifurcation suggests two fundamentally different surprise functions in poetry:

**Mode 1 — Crystallizing Surprise (S₂ 3–9):**  
The poet chooses a word unexpected in the current context, but it is a *concrete* word that specifies a new direction. Once said, it generates its own certainty. This is the surprise of the *perfect image*: you couldn't have predicted "nest" here, but once you see it, you know where the poem is going.

**Mode 2 — Dissolving Surprise (S₂ > 9.5):**  
The poet chooses a word so far from the model's expectations that no context survives the disruption. These are often function words that open a syntactic frame without filling it — or content words so radical that GPT-2 has no familiar trajectory to project from them. This is the surprise of *rupture*: not the unexpected image, but the severing of the semantic fabric.

---

## Relationship to Existing Findings

- **surprise_decay_curves.md** showed S₂ collapses to near-zero one token after a spike (half-life = 1 token). This is compatible with both modes: crystallizing tokens reset the poem to normal S₂ by narrowing expectations; dissolving tokens also reset S₂ because the high-entropy aftermath means any token is roughly expected.
- **pre_peak_setup.md** showed the model becomes MORE confident just before a spike (entropy drops). The aftermath finding is asymmetric: confidence BEFORE the spike is universal, but what happens AFTER depends on the magnitude and type of surprise.
- **confidence_trap_analysis.md** identified confidence traps (H < 3, rank > 10) as the highest-S₂ positions. The quartile analysis here shows these extreme positions are also the most dissolving.

---

## Suggested Next Steps

1. **Content vs. function word classifier**: Formally test whether crystallizing ~ content words and dissolving ~ function words using POS tagging, controlling for S₂ level.
2. **Era analysis with S₂ controlled**: Are beat poets genuinely more crystallizing, or do they simply have lower absolute S₂ (putting them in the crystallizing regime by default)?
3. **The "committed turn"**: When a crystallizing surprise commits the poem to a semantic field, do subsequent tokens have lower entropy for longer? Does crystallization duration vary by era?
4. **Dissolution clusters**: Are dissolving surprises randomly distributed, or do they appear in clusters (multiple successive syntactic openers)?
