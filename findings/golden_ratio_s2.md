# Golden Ratio and Peak S2 Position: Poetry Does NOT Follow φ

**Date:** 2026-10-14  
**Experiment:** `experiments/golden_ratio_s2.py`  
**Corpus:** 256 English poems, stanza-break artifacts filtered (p_newline < 0.9)

---

## Research Question

Does the token of maximum S2 in a poem tend to fall near the golden ratio position
φ ≈ 0.618 — the "divine proportion" of visual art, music, and classical narrative? Or
do poems peak earlier or later?

---

## Key Results

| Metric | Value |
|--------|-------|
| Mean peak S2 position (poetry) | **0.442** |
| Mean peak S2 position (prose control) | **0.787** |
| φ (golden ratio) | 0.618 |
| 1 − φ | 0.382 |
| t-statistic vs. null (0.5) | **−3.05** |
| % poems peaking near φ or 1−φ (±0.1) | **33.6%** |
| Expected by chance (uniform) | ~20% |

**The golden ratio hypothesis is rejected for poetry as a whole.**  
Peak S2 falls systematically *before* the midpoint (mean 0.442), not at φ (0.618).

---

## Distribution of Peak S2 Positions

```
Position   Count  
0.0–0.1    ███████████████████████████████  39  ← most common
0.1–0.2    ███████████████████████████      35  
0.2–0.3    ████████████████████████         31  
0.3–0.4    ████████████████████             25  ← 1−φ
0.4–0.5    ██████████████████               22  
0.5–0.6    ████████████████                 19  
0.6–0.7    █████████████                    16  ← φ
0.7–0.8    ████████████████                 21  
0.8–0.9    ████████████████████             25  
0.9–1.0    █████████████████                23  
```

**Shape:** roughly monotone decline from start to midpoint, with a slight U-shape
recovery at 0.7–1.0. The *opening* of a poem (0.0–0.1) is the most common location
for the single highest-S2 moment. This confirms the "deviate early, resolve late"
arc found in `within_poem_type_arc.md`, now at the single-token peak level.

---

## The Prose vs. Poetry Contrast

The most striking result in the era table:

| Category | Mean peak position |
|---|---|
| metaphysical | 0.139 |
| 18th century | 0.266 |
| victorian | 0.337 ≈ 1−φ |
| romantic | 0.398 ≈ 1−φ |
| modernist | 0.423 |
| contemporary | 0.469 |
| confessional | 0.657 ≈ φ |
| **prose control** | **0.787** |

**Prose peaks late; poetry peaks early.** Prose builds toward a climax at
~0.787, consistent with narrative arc theory. Poetry frontloads its maximum
deviation: the first 20% of poem tokens is the most common location for the
peak surprise moment.

---

## The 1−φ Cluster (Traditional Forms)

Several traditional poetry eras have mean peak positions near 1−φ ≈ 0.382:

| Era | Mean peak pos | Distance from 1−φ |
|---|---|---|
| victorian (n=21) | 0.337 | 0.045 |
| oulipo (n=4) | 0.350 | 0.032 |
| fixed_form (n=8) | 0.358 | 0.024 |
| ancient (n=3) | 0.358 | 0.024 |
| haiku (n=3) | 0.382 | **0.000** |
| war_poetry (n=3) | 0.394 | 0.012 |
| romantic (n=15) | 0.398 | 0.016 |

The 1−φ position appears as the preferred peak moment in older, more formal
traditions. Haiku lands at exactly 1−φ, consistent with the idea that haiku
place their *kigo* (seasonal word of maximum semantic weight) early in the poem,
approximately at the one-third mark.

---

## The φ Cluster (Modern / Post-Colonial Forms)

Modern and post-colonial forms show peaks nearer φ:

| Era | Mean peak pos | Distance from φ |
|---|---|---|
| spoken_word (n=3) | 0.568 | 0.050 |
| beat (n=6) | 0.581 | 0.037 |
| postcolonial (n=6) | 0.590 | 0.028 |
| early_modern (n=5) | 0.590 | 0.028 |
| classical_chinese (n=4) | 0.594 | 0.024 |
| confessional (n=6) | 0.657 | 0.039 |

Confessional poetry (Plath, Sexton, Lowell) and Beat poetry (Ginsberg) both peak
near φ, consistent with the narrative self-disclosure arc: build toward a
confession, then release. The classical Chinese cluster is unexpected and warrants
further study.

---

## Peak Complementarity

Do the two highest-S2 moments mirror each other (sum to ~1.0)?

> Mean |peak1_pos + peak2_pos − 1| = **0.377**  
> (random expectation ≈ 0.33; perfectly mirrored = 0.00)

The complementarity is slightly *worse* than random (0.377 > 0.33), suggesting
peaks do NOT form mirror pairs. The two highest-surprise moments are not
structurally complementary — they tend to cluster rather than balance.

---

## Poems Closest to φ

| Poem | Author | Peak pos | Δφ | Token |
|---|---|---|---|---|
| The Stranger (prose poem) | Baudelaire | 0.621 | 0.003 | 'willingly' |
| Psalm 23 (KJV) | Anonymous | 0.623 | 0.005 | 'prepare' |
| Kleine Aster | Gottfried Benn | 0.623 | 0.005 | 'lying' |
| She Had Some Horses | Joy Harjo | 0.623 | 0.005 | 'told' |
| How Doth the Little Busy Bee | Isaac Watts | 0.624 | 0.006 | 'Satan' |

**Psalm 23** places "prepare" (as in "I will prepare a table before you in the presence
of my enemies") at almost exactly φ — a striking instance of structural surprise.
**Isaac Watts's bee poem** has its peak surprise at "Satan" — the unexpected theological
turn at precisely the golden ratio moment.

---

## Theoretical Interpretation

### Why Poetry Frontloads Surprise

The "deviate early" dominance has a clear functional explanation: the opening gambit
theory. The first tokens of a poem must establish the poem's register, speaker, and
contract with the reader. This is done by *deviating from average language* — a high-S2
opening announces "this poem speaks differently." Once the contract is set, the poem
can work within its own grammar, and GPT-2 can calibrate to the poem's specific
probabilities. Opening surprise is a *registration event*, not a climactic one.

### Why Prose Peaks Late

Narrative prose builds information toward a climax or revelation. The late peak position
(0.787) corresponds to the classical three-act structure: exposition, rising action,
climax at ~80% through. Poetry does not follow this model — it is not optimized for
progressive revelation.

### Why Traditional Forms Peak at 1−φ

The 1−φ ≈ 0.382 position for traditional forms may reflect the volta position in
many fixed forms. In a 14-line sonnet, line 6 falls at ~0.43; in a 12-line poem,
line 5 at ~0.42. The 0.382 cluster could be capturing the early volta of
Petrarchan and related forms, where surprise marks the pivot after the octave.

---

## Next Steps

1. **Compute peak position for known volta poems separately** — test whether sonnet voltas
   at line 8→9 fall at ~0.618 (making them closer to φ than average).
2. **Control for poem length** — very short poems (haiku) have discretized positions
   that might skew era means.
3. **Test whether first-line vs. body peak matters**: poems where the peak is in line 1
   might be a distinct category (incipit surprise).
4. **Extend to German corpus** — do German poems, analyzed against the German GPT-2
   model, show the same frontloaded distribution?
