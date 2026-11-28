# The Precision-Shot Premium: How Probability Concentration Shapes Poetic Surprise

**Date:** 2026-11-28  
**Experiment:** `experiments/top10_concentration_s2.py` → `results/top10_concentration_s2.json`  
**Corpus:** 454 poems, 61,414 artifact-free tokens  
**Research question:** When GPT-2's probability mass is concentrated in its top-10 predictions vs. scattered across the vocabulary, how does that shape the intensity and character of poetic surprise?

---

## Background

Previous work established *what* poets choose at high-S2 moments (Straussian gap taxonomy) and *whether* the syntactic diversity of GPT-2's prediction space affects S2 (prediction_diversity — a null result). This experiment asks a different question: **does the *concentration* of probability mass in the top-10 alternatives predict how powerful a surprise is?**

Standard entropy (H) measures uncertainty over all ~50,000 vocabulary tokens. But we can also ask: what fraction of the total probability mass sits in just the top 10 alternatives?

```
top10_coverage = Σ p_i  for i in {top-10 alternatives}
```

A **high-coverage** position (top10_coverage ≥ 0.75) means the model's probability mass is tightly focused: 10 words account for 75%+ of all predictions. A **low-coverage** position (<0.45) means probability is diffused widely across the vocabulary — the model is scattering its bets.

**Hypotheses:**
1. Precision shots (high coverage + high S2) will be more extreme than scatter deviations (low coverage + high S2) — violating a concentrated prediction should amplify S2
2. Poetic genres will differ in what fraction of their token positions are "high coverage" (model most focused)
3. Authors will show characteristic signatures: "precision-shot poets" vs "scatter-deviation poets"

---

## Method

For each artifact-free token (p_newline < 0.90), computed:
- `top10_coverage` = sum of probabilities of the top-10 alternatives
- `top10_entropy` = entropy of the top-10 sub-distribution (normalized)
- Coverage tier: **high** (≥0.75), **medium** (0.45–0.75), **low** (<0.45)
- Precision-shot: tokens with high coverage AND S2 ≥ 5
- Scatter deviation: tokens with low coverage AND S2 ≥ 5

---

## Finding 1: The Precision-Shot Premium

The most dramatic poetic surprises happen when the model is most confident.

| Coverage Tier | n | Avg S₂ | % Positive | Avg Top-10 H |
|---|---|---|---|---|
| High (≥0.75) | 17,741 | **−0.215** | 22.5% | 1.433 |
| Medium (0.45–0.75) | 21,641 | −0.566 | 34.8% | 2.519 |
| Low (<0.45) | 22,032 | −0.449 | 41.4% | 2.942 |

At first glance: high-coverage positions show the *lowest* average S₂ and the *lowest* positive ratio. This makes sense: when GPT-2 is most confident (top-10 covers 75%+ of probability), poets often follow that confidence and choose one of the expected words.

**The key insight emerges in the cross-tabulation:**

| Coverage + S₂ Category | n | Avg S₂ |
|---|---|---|
| High coverage + Very high S₂ (>5) | 1,387 | **+9.14** |
| Medium coverage + Very high S₂ | 2,281 | +7.90 |
| Low coverage + Very high S₂ | 1,715 | +6.98 |
| High coverage + High S₂ (2–5) | 1,200 | +3.31 |
| Low coverage + Low S₂ (<−1) | 10,569 | −3.39 |

**Precision shots average +9.14 bits — 2.16 bits more than scatter deviations in the same tier (+6.98).** The most extreme surprises are systematically more extreme when the model was most focused. This confirms: when GPT-2 concentrates its bets on a small set of predictions and the poet violates all of them, the information-theoretic charge is highest.

---

## Finding 2: The Beat Paradox

The genre findings reveal a striking structural fact about Beat poetry.

**Eras with HIGHEST % high-coverage positions (model most focused):**

| Era | % High-cov | % Low-cov | Avg S₂ (clean) | n |
|---|---|---|---|---|
| triolet | 60.0% | 16.9% | −0.747 | 130 |
| **beat** | **56.1%** | **22.4%** | **+0.049** | **1,195** |
| concrete | 53.7% | 17.0% | −0.584 | 311 |
| song_lyrics | 51.4% | 20.7% | −0.678 | 541 |
| biblical | 50.6% | 15.9% | −0.453 | 1,331 |
| found_poetry | 49.7% | 18.1% | −0.615 | 1,204 |

**Eras with LOWEST % high-coverage positions (model most scattered):**

| Era | % High-cov | % Low-cov | Avg S₂ (clean) | n |
|---|---|---|---|---|
| german_symbolist | 17.1% | 48.3% | +0.452 | 356 |
| clerihew | 17.7% | 45.3% | +0.507 | 232 |
| haiku | 19.1% | 44.7% | −0.110 | 293 |
| metaphysical | 19.1% | 44.1% | −0.593 | 938 |
| ekphrastic | 19.1% | 46.4% | −0.508 | 1,901 |

**The Beat Paradox:** Beat poetry has 56% high-coverage positions — the model is concentrating on its top-10 predictions more often in Beat poems than in almost any other genre. Yet Beat poetry has the highest positive artifact-free avg S₂ (+0.049) among all large eras. Beat poets like Ginsberg and Ferlinghetti achieve high information-theoretic surprise precisely by operating in contexts where the model is MOST focused, then violating it. They write themselves into highly predictable syntactic situations, then swerve.

**The German Symbolist comparison:** With only 17% high-coverage positions, German Symbolist poetry (Rilke, George, Trakl) works in the opposite mode — their language is sufficiently unusual that the model rarely narrows its attention to any small set of predictions. Their surprises are more "field disruptions" than "precision shots."

---

## Finding 3: Two Poet Archetypes

Authors cluster into two distinct deviation signatures:

### Precision-Shot Poets (PS/SD ratio > 1.5)

| Author | PS Rate | SD Rate | Ratio | Avg Coverage | Avg S₂ |
|---|---|---|---|---|---|
| Emmett Williams | 10.91% | 3.64% | 2.0 | 0.747 | +0.010 |
| Claudia Rankine | 7.91% | 2.16% | 2.8 | 0.583 | +0.005 |
| Marianne Moore | 5.93% | 2.74% | 2.0 | 0.608 | −0.117 |
| Elizabeth Bishop | 5.00% | 1.67% | 1.5 | 0.605 | +0.175 |
| Francis Thompson | 5.59% | 4.66% | 1.1 | 0.576 | +0.473 |

These poets write in contexts where GPT-2 is focused, then fire precision shots against its concentrated predictions. Emmett Williams (concrete poetry), Claudia Rankine (documentary lyric), Marianne Moore (baroque specificity): all operate by establishing high predictability and then subverting it at key moments.

### Scatter-Deviation Poets (PS/SD ratio < 0.6)

| Author | PS Rate | SD Rate | Ratio | Avg Coverage | Avg S₂ |
|---|---|---|---|---|---|
| Allen Ginsberg | 4.73% | 8.78% | 0.5 | 0.556 | +0.685 |
| Raymond Queneau | 0.76% | 8.40% | 0.1 | 0.483 | −0.749 |
| OuLiPo N+7 (Dickinson) | 1.72% | 8.62% | 0.2 | 0.450 | +0.159 |
| Georg Trakl | 2.47% | 6.36% | 0.4 | 0.521 | +0.562 |
| Alexander Pope | 1.34% | 6.08% | 0.2 | 0.472 | −0.177 |

These poets write in contexts where the model's probability is already scattered, then deviate even further into the improbable. Ginsberg's improvisational catalogues, Pope's compressed antitheses, Trakl's color-saturated abstractions: all work in already-uncertain prediction spaces. Their surprises are more "field-level disruptions" than surgical violations.

---

## Finding 4: Highest-S₂ Precision Shots

The tokens where coverage was highest AND surprise was most extreme:

| Token | S₂ | Coverage | Expected | Prob | Author / Poem |
|---|---|---|---|---|---|
| ` gro` | +36.7 | 1.00 | ` ` | 1.00 | Ferlinghetti, "In Goya's greatest scenes" |
| ` climbs` | +28.2 | 0.99 | ` ` | 0.98 | Ferlinghetti, "Constantly Risking Absurdity" |
| ` pour` | +27.7 | 1.00 | `'m` | 1.00 | Bukowski, "Bluebird" |
| ` hum` | +25.6 | 0.99 | ` ` | 0.98 | Brathwaite, "Calypso" |
| ` glass` | +25.6 | 1.00 | ` ` | 0.99 | Marianne Moore, "The Fish" |
| `Fresh` | +25.5 | 0.98 | `\n` | 0.87 | Gerard Manley Hopkins, "Pied Beauty" |
| ` write` | +23.7 | 1.00 | ` ` | 0.99 | Lorine Niedecker, "My Life by Water" |
| ` ferner` | +23.4 | 0.97 | `t` | 0.82 | Stefan George, "Komm in den totgesagten park" |
| `jar` | +23.0 | 0.96 | `time` | 0.78 | Jean Lescure, S+7: Genesis (N+7 variant) |

The ` ` (space) predictions at coverage=1.00 represent GPT-2 at a word boundary where it was 99-100% sure the next character would begin a new word — but the poet wrote the second half of a word (like `gro` in `grotesque`). These are sub-token precision shots: the model never anticipated the word's full form.

The Bukowski example is particularly striking: `I` was followed by `pour`, but the model was 100% certain the next token would be `'m` (i.e., "I'm"). Bukowski chose the unexpected active verb instead of the expected contraction.

---

## Interpretive Framework: Two Architectures of Surprise

The findings suggest two fundamentally different modes of poetic surprise, now defined by the probability concentration landscape:

**Mode A — Precision Shot** (high coverage → high S₂):
> The model has focused its bets. The poet fires against the focus. The surprise is amplified by the model's confidence.
> *Characteristic genres: beat, concrete, song lyrics*  
> *Characteristic poets: Emmett Williams, Claudia Rankine, Marianne Moore*

**Mode B — Field Disruption** (low coverage → high S₂):
> The model's probability mass is already scattered. The poet disrupts the field further. The surprise is a broad-spectrum deviation.
> *Characteristic genres: german symbolist, haiku, metaphysical*  
> *Characteristic poets: Ginsberg (scatter), Pope, Trakl*

These modes are not mutually exclusive — many poets use both — but they represent distinct information-theoretic strategies for achieving surprise.

---

## Suggested Next Steps

1. **Longitudinal analysis**: Does a poet's PS/SD ratio shift over their career? Do poets move from scatter deviations to precision shots as they develop craft?
2. **Cluster analysis**: Can poems be reliably classified as "precision-shot dominant" vs "scatter-deviation dominant"? Do these clusters correlate with critical assessments of obscurity vs. accessibility?
3. **Sub-token vs. token-level shots**: The highest precision shots (Ferlinghetti's ` gro`) are sub-token (GPT-2 tokenization artifacts). Could these be filtered and the analysis redone on lexical precision shots only?
4. **Cross-model validation**: Does GPT-2 large or medium show the same Beat paradox? Or is this specific to small GPT-2's training data distribution?
