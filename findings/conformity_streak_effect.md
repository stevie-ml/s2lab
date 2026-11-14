# Conformity Streak Before Surprise: The U-Shaped Spring-Tension Model

**Date:** 2026-11-14  
**Experiment:** `experiments/conformity_streak_effect.py` → `results/conformity_streak_effect.json`  
**Corpus:** 419 poems, 11,363 high-S₂ spikes (S₂ ≥ 2.0, p_newline < 0.9)  
**Builds on:** `findings/pre_peak_setup.md` (8-token window average), `findings/post_surprise_signature.md` (what follows a spike)

---

## Research Question

`pre_peak_setup.md` established that S₂ decreases over the 8-token window before a spike — the poet "conforms" before striking. But that analysis used a fixed window. Here we ask: how long is the unbroken **conformity streak** (consecutive tokens with S₂ < 0.5) immediately preceding each spike? And does streak length predict spike height?

**Spring-tension hypothesis**: longer conformity runs → bigger releases.

We define **conformity streak** = the count of consecutive tokens with S₂ < 0.5 immediately preceding a spike. Zero means the previous token was itself a surprise.

---

## Finding 1: The Spring-Tension Hypothesis Is Wrong in the Middle — But True at the Extremes

| Streak bucket | n spikes | Mean S₂ | Median S₂ |
|:-------------:|:--------:|:-------:|:---------:|
| **0 (cascade)** | 3,589 | **5.32** | 3.42 |
| 1 | 2,572 | **5.35** | 3.57 |
| 2–3 | 2,747 | 5.18 | 3.47 |
| 4–6 | 1,610 | 5.08 | 3.37 |
| 7–10 | 580 | 4.93 | 3.14 |
| **11+** | 265 | **6.82** | 4.07 |

The relationship is **U-shaped**, not linear. Spikes after medium-length conformity runs (4–10 tokens) are *smaller* than spikes after short runs (0–1 tokens). But spikes after very long plateaus (11+ conforming tokens) are dramatically *larger* — a 38% increase over the minimum.

**Overall correlation** (streak length vs. spike S₂): r = 0.070 — essentially no linear relationship.  
**Poem-level correlation** (avg streak per poem vs. avg spike S₂): r = 0.131 — weak positive.

The two ends of the distribution operate by different mechanisms:

- **Cascade effect (streak = 0)**: When a surprise immediately follows another surprise, the second surprise lands with elevated S₂ ≈ 5.32. The model hasn't recovered from the first jolt, so contextual expectations remain scrambled.
- **Plateau effect (streak ≥ 11)**: After 11+ tokens of unbroken conformity, the model is *maximally confident* — and when the surprise arrives, it hits hardest: mean S₂ = 6.82.

---

## Finding 2: Most Spikes Follow Short Winds-Up

| Streak | % of all spikes |
|--------|:---------------:|
| 0 (immediate cascade) | 31.6% |
| 1 | 22.6% |
| 5+ | 14.9% |
| 10+ | 2.9% |
| Mean streak | 2.25 |
| Max streak | 60 |

**Nearly a third of all poetic surprises follow another surprise with no conforming token between them.** Most of the remaining two-thirds involve very short run-ups (1–3 tokens). True long plateaus (11+) are rare — only 2.9% of spikes — but when they occur, they produce the most extreme surprises.

---

## Finding 3: Beat Poetry Masters the Long Wind-Up; Imagism Doesn't Need It

Genre-level breakdown (top 10 by avg streak):

| Era / Genre | n poems | Avg streak | Avg spike S₂ |
|-------------|:-------:|:----------:|:------------:|
| Beat | 8 | **4.40** | **7.52** |
| Triolet | 2 | 4.13 | 4.38 |
| Song lyrics | 3 | 3.70 | 5.51 |
| Found poetry | 9 | 3.60 | 5.22 |
| Villanelle | 3 | 3.19 | 5.15 |
| Victorian | 30 | 2.14 | 5.24 |
| Imagist | 5 | **1.62** | 4.85 |
| Clerihew | 10 | **1.57** | **6.17** |
| Japanese classical | 2 | 1.42 | 4.17 |
| Deep image | 1 | 1.33 | 4.85 |

Beat poetry (Ferlinghetti, Ginsberg) uses the longest conformity runs before striking — averaging 4.40 tokens — and produces the highest average spike S₂ in the corpus. This matches Beat's characteristic long prosaic passages that suddenly fracture into an unexpected word or image.

**Imagism** does the opposite: shortest streaks (1.62), moderate spikes. Pound's "In a Station of the Metro" strategy — shock on impact, no wind-up.

**Clerihews** are the extreme outlier: very short streaks (1.57) but high spike S₂ (6.17). The comedic form generates maximum surprise through pure vocabulary choice alone, with no conformity build-up.

---

## Finding 4: Ferlinghetti as Master of Spring Tension

Top poems by tension score (avg_streak × avg_spike_S₂):

| Poem | Author | Avg streak | Avg S₂ | Score |
|------|--------|:----------:|:------:|:-----:|
| "Constantly Risking Absurdity" | Ferlinghetti | 15.9 | 12.04 | 191.96 |
| Cicadas (Bashō, trans.) | Matsuo Bashō | 9.0 | 10.62 | 95.59 |
| "In Goya's Greatest Scenes" | Ferlinghetti | 9.4 | 9.04 | 85.09 |
| "Buffalo Bill's" | E.E. Cummings | 7.7 | 8.30 | 64.10 |
| "Self-Evident Truths" (found poem) | Jefferson (found) | 6.3 | 7.95 | 49.83 |

Ferlinghetti dominates. "Constantly Risking Absurdity" — a shaped poem typographically performed on the page — achieves an average conformity streak of **15.9 tokens** between spikes, and when the spikes arrive they hit with mean S₂ of **12.04**. The poem's unusual layout and long syntactic riffs create extended model-conforming passages that make the surprise all the more violent.

The longest single plateau in the corpus: a **60-token conformity run** in one poem, followed by a dramatic spike.

---

## The Big Picture: Two Strategies for Poetic Surprise

| Strategy | Streak | S₂ profile | Genres |
|----------|:------:|:----------:|--------|
| **Cascade** (immediate re-spike) | 0 | 5.32 | Clerihew, Language poetry, German expressionist |
| **Short wind-up** (1–3 tokens) | 1–3 | 5.18–5.35 | Imagist, haiku, early modern |
| **Medium plateau** (4–10 tokens) | 4–10 | 4.93–5.08 | Victorian, contemporary |
| **Long plateau** (11+) | 11+ | 6.82 | Beat, found poetry, some concrete |

The spring-tension model is **confirmed at the extremes but reversed in the middle**. Very short and very long wind-ups both produce elevated spikes through different mechanisms (model disorientation vs. maximum model confidence). Medium-length wind-ups produce the *smallest* spikes — suggesting the model partially "adapts" to a poem's register within 4–10 tokens, blunting the eventual surprise.

---

## Suggested Next Steps

1. **Plateau-spike pairs**: Catalog the specific words at the end of longest plateaus (11+). What semantic or syntactic moves snap the model out of its confidence?
2. **Cascade runs**: Map the structure of multi-spike cascades (how long can a cascade continue before conformity resumes?).
3. **Within-poem plateau mapping**: For each poem, visualize alternating plateau/spike zones as a rhythm — does this rhythm correlate with meter or stanza structure?
4. **Cross-poet**: Why does Ferlinghetti consistently use longer plateaus than Ginsberg? Map plateau length as a poet fingerprint.
