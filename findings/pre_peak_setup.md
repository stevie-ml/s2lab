# Pre-Peak Setup: The Wind-Up Before the Strike

**Date:** 2026-09-18
**Corpus:** 141 poems (added 8 haiku, 2 spoken-word, 1 Wyatt sonnet this run)
**Method:** For every token with S₂ ≥ 3.0, aggregate the entropy, surprisal, and S₂ of the eight preceding tokens (`k = −8 … −1`). Compare mean values at each lag with the poem's overall baseline.

Companion / dual of the existing `surprise_decay.md` (post-peak dynamics).

---

## Central claim

Before a poet strikes with an unexpected word, they systematically conform.
Aggregated across **2 687 spikes**, S₂ falls from **+0.49** eight tokens
before the peak to **+0.09** immediately before it — the poet becomes almost
neutral just before subverting.

The corresponding entropy trajectory *drops* from **6.29** (k=−4) to **6.10**
(k=−1), so the model is actually *more* confident right before the strike
than a few tokens earlier. Confidence and conformity converge on the same
point, and that point is one token before the shock.

## The overall pre-peak curves

| lag k | Entropy | Surprisal | **S₂** |
|:---:|:---:|:---:|:---:|
| −8 | 6.16 | 6.65 | **+0.49** |
| −7 | 6.21 | 6.53 | +0.32 |
| −6 | 6.25 | 6.71 | +0.46 |
| −5 | 6.28 | 6.49 | +0.21 |
| −4 | 6.29 | 6.78 | +0.49 |
| −3 | 6.21 | 6.86 | +0.66 |
| −2 | 6.09 | 6.21 | +0.12 |
| **−1** | **6.10** | **6.19** | **+0.09** |
| **0 (peak)** | — | — | **≥ 3.0** |

Two features of the shape:

1. A mild bump at k=−3 (S₂ = 0.66, the highest in the whole run-up).
2. A sharp cliff into k=−2/−1, where S₂ collapses by roughly 0.6 units
   and entropy simultaneously falls ~0.2 bits.

The mini-bump at k=−3 is not visible at all in `surprise_decay.md`'s
symmetric post-peak curve — this is a *pre-peak* structural signature.

## Per-era: who sets up their surprises?

`lull_depth` = mean S₂ over lags −3…−1 minus the poem's baseline S₂
(negative = "the poet is quieter than usual right before the peak").
`trap_depth` = same, but for entropy (negative = "the model is more
confident than usual right before the peak").

| era | n_poems | n_spikes | trap | **lull** |
|---|---:|---:|---:|---:|
| mid_century      |  3 |  34 | +0.14 | **−0.76** |
| metaphysical     |  2 |  54 | −0.12 | **−0.72** |
| haiku            |  8 |  60 | +0.25 | **−0.69** |
| surrealist       |  1 |  11 | +0.82 | −0.60 |
| song_lyrics      |  3 |  89 | +0.57 | −0.57 |
| oulipo           |  1 |   9 | +0.14 | −0.46 |
| beat             |  2 |  41 | −0.15 | −0.44 |
| harlem_renaissance| 5 | 104 | +0.23 | −0.36 |
| victorian        | 14 | 407 | +0.07 | −0.34 |
| german_modernist |  2 |  59 | +0.23 | −0.32 |
| german_expressionist | 2 | 67 | +0.12 | −0.31 |
| modernist        | 18 | 306 | +0.33 | −0.14 |
| confessional     |  3 |  40 | **−0.46** | −0.12 |
| new_york_school  | 18 | 245 | +0.13 | −0.04 |
| 19th_century     |  9 | 189 | −0.11 | +0.01 |
| ballad           |  6 | 199 | +0.08 | +0.01 |
| **spoken_word**  | **2** | **33** | **+0.20** | **+0.01** |
| early_modern     |  2 |  80 | −0.15 | +0.02 |
| romantic         |  8 | 184 | −0.01 | +0.07 |
| language         |  3 |  34 | −0.28 | +0.15 |
| prose_poetry     |  9 | 138 | +0.21 | +0.18 |
| nursery_rhyme    |  1 |  42 | **−0.93** | +0.21 |
| contemporary     |  9 | 151 | −0.08 | +0.28 |
| ancient (Sappho) |  1 |  14 | −0.40 | **+1.04** |

Three groupings emerge:

**A. Setup poets (lull_depth ≪ 0).**
The mid-century masters (Bishop, Lowell, Berryman) and the metaphysicals
(Donne, Herbert) top the list. They spend the three tokens before a spike
being quieter than their own baseline S₂ by 0.7–0.8 units. So does haiku
— which was under-sampled before this run; with eight haiku now, the
lull-depth jumped from −0.24 to **−0.69**. This is the temporal fingerprint
of the *kireji* cut: two lines of syntactic conformity, then the pivot.

**B. Steady poets (lull_depth ≈ 0).**
Ballads, spoken word, 19th-century verse, early modern sonnets. These
forms distribute surprise more evenly; a spike is not a specially prepared
event, it's a routine tremor in a rougher landscape. Note that spoken
word — the era added this run — lands at +0.01, essentially at baseline.
Performance poetry does *not* use the setup-and-strike architecture; its
strikes are equally likely at any point.

**C. Inverted poets (lull_depth > 0).**
Prose poetry, contemporary free verse, ancient (Sappho). Here the poet is
actually *more* surprising than usual just before a spike — an escalation
rather than a setup. Sappho's ancient fragment shows the extreme:
lull_depth = **+1.04**. When the peak comes, it comes on top of an already
elevated plateau.

Note the *disagreement* between trap_depth and lull_depth in a few cells:
nursery_rhyme has the deepest trap (−0.93 entropy) but a positive lull
(+0.21 S₂). That is because when the entropy is extremely low (as with
"Twinkle, twinkle, little ___"), *any* small deviation shows up as a
positive S₂ pre-peak: the model is confident but the human is still
mildly playful. So trap_depth captures the *model's* pre-peak state and
lull_depth captures the *poet's*.

## Individual spikes with the deepest traps

The top-15 by trap_depth are almost all from strictly-metered forms:

| trap | S₂ | poet | poem | era |
|---:|---:|---|---|---|
| −7.06 | 5.48 | Hopkins | The Windhover | victorian |
| −5.95 | 15.07 | Stein | Susie Asado | modernist |
| −5.36 | 6.94 | *Sir Patrick Spens* | — | ballad |
| −5.33 | 10.45 | Hopkins | The Windhover | victorian |
| −5.29 | 5.14 | Frost | The Road Not Taken | modernist |
| −5.18 | 3.21 | Wyatt | They Flee from Me | early_modern |
| −5.11 | 5.51 | Arnold | Dover Beach | victorian |
| −5.06 | 15.80 | Burns | A Red, Red Rose | romantic |
| −5.00 | 9.31 | Hughes | The Negro Speaks of Rivers | harlem_renaissance |
| −4.92 | 32.75 | *Sir Patrick Spens* | — | ballad |
| −4.89 | 6.27 | Bishop | One Art | mid_century |
| −4.84 | 5.51 | Dickinson | I heard a Fly buzz | 19th_century |

Two Hopkins spikes in the top 4. The Windhover — famously a poem of
"sprung rhythm" surprise — is the extreme case of setup. Hopkins builds
his line in the most predictable meter he can manage right up to the
break-word, and then the break-word arrives at a moment when the model
was practically pinned.

## What this changes

Prior work in this repo characterises the S₂ *peak* (`straussian_gap_taxonomy`)
and the S₂ *decay after* the peak (`surprise_decay`). This finding pins
down the pre-peak arc:

- The average pre-peak curve is **asymmetric**: gentle over lags −8…−4,
  a small final rise at k=−3, then a cliff into k=−1.
- The cliff is **entropy-mediated**: the model becomes MORE confident just
  before the surprise, not less. So the "confidence trap" mechanism
  described statically at the token level (`confidence_trap.md`) is
  visible dynamically as a temporal pattern.
- The magnitude of the setup varies systematically by movement, and the
  ranking is not the same as the ranking by peak height. Haiku is *high*
  peak and *deep* setup. Ballads are *high* peak and *no* setup.
  Contemporary free verse is *modest* peak and *positive* pre-peak lull
  (escalation, not setup).

## Suggested next steps

1. **Symmetry check.** Overlay this pre-peak curve on the post-peak curve
   from `surprise_decay.md` and compute the setup/decay ratio. Is the
   "wind-up before the strike" comparable in duration to the "recovery after"?
2. **Poet-level fingerprints.** Compute per-poet lull_depth (Hopkins,
   Dickinson, Bishop, Stein, Burns). Some poets appear repeatedly in the
   top-15 — maybe individual style is a strong predictor of setup depth.
3. **Kireji localisation in haiku.** In our now-8-poem haiku sample, does
   the setup-cliff align mechanically with the classical L2→L3 break? A
   line-position analysis of pre-peak lags restricted to haiku would test this.
4. **Line-position confound.** Are pre-peak lags mostly line-medial
   tokens (which naturally have lower S₂) and peaks mostly line-initial?
   If so, part of the "cliff" is just line-position rhythm.
5. **Predictive use.** If lull_depth is real, one could try to *detect*
   an impending literary surprise from the S₂ signal alone (a 3-token
   dip below the poet's baseline). Testable as a binary classifier on
   held-out poems.
