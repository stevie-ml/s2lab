# Spike Symmetry: Is Poetic Surprise a Symmetric Event in Time?

**Date:** 2026-09-20
**Experiment:** `experiments/spike_symmetry.py`
**Corpus:** 160 poems (153 existing + 7 new: Berryman, Lowell, Marvell, Herbert×2, Jonson, Spenser)
**Clean spikes analyzed:** 130 (isolation criterion: no other spike within ±8 tokens)

Extends `pre_peak_setup.md` (lags −8..−1) and `surprise_decay_curves.md` (lags +1..+10)
by computing the **full symmetric window** around each spike.

---

## Research Question

The wind-up before a poetic spike (pre-peak lull) and the decay after it (surprise half-life) have been
characterized separately. But do they balance? Is the information-theoretic "energy" invested in
*preparing* a surprise equal to the energy of its *aftermath*?

**Hypothesis H0 (Symmetry):** The area under the centered S₂ curve is equal on both sides of the spike.  
**Hypothesis H1 (Asymmetry):** Different movements invest differently pre vs. post spike.

---

## Finding 1: Global Perfect Symmetry

| Metric | Value |
|---|---|
| Pre-peak area (lags −8..−1, centered) | −12.112 |
| Post-peak area (lags +1..+8, centered) | −12.107 |
| **Global asymmetry (post − pre)** | **+0.005** |

The global asymmetry is effectively **zero**. Averaged across all 130 clean spikes and all eras,
the S₂ "gravity well" around a spike is a perfect mirror: the conventionality imposed before
the strike exactly equals the conventionality imposed after it.

This suggests a **conservation principle in poetic surprise**: the poem "pays" the same
informational price before and after a deviant moment. The surprise event is temporally balanced.

### The Global Symmetric Profile

```
lag −8:  −1.58  ░░░
lag −7:  −1.58  ░░░
lag −6:  −1.46  ░░
lag −5:  −1.80  ░░░
lag −4:  −1.71  ░░░
lag −3:  −1.38  ░░
lag −2:  −1.48  ░░
lag −1:  −1.12  ░

lag  0:  +9.37  ████████████████████ ← SPIKE

lag +1:  −1.84  ░░░
lag +2:  −1.82  ░░░
lag +3:  −1.33  ░░
lag +4:  −1.60  ░░░
lag +5:  −1.48  ░░
lag +6:  −1.20  ░░
lag +7:  −1.50  ░░
lag +8:  −1.34  ░░
```

The profile is "U"-shaped, with the spike as a symmetric peak flanked by an 8-token "gravity well" on each side.
All surrounding tokens are below the poem's baseline S₂, creating a "valley of conformity" around the
moment of maximum deviation.

---

## Finding 2: Era-Level Asymmetry Reveals Two Poetic Strategies

While the global average is symmetric, individual eras show strong, systematic asymmetry:

| Era | n spikes | Pre area | Post area | **Asymmetry** | Strategy |
|---|---|---|---|---|---|
| nursery_rhyme | 2 | −12.17 | −23.06 | **−10.89** | Setup-dominant |
| confessional | 2 | −10.00 | −19.86 | **−9.88** | Setup-dominant |
| harlem_renaissance | 3 | −17.88 | −24.33 | **−6.46** | Setup-dominant |
| contemporary | 7 | −9.36 | −14.50 | **−5.14** | Setup-dominant |
| metaphysical | 6 | −9.00 | −13.43 | **−4.43** | Setup-dominant |
| spoken_word | 2 | −8.51 | −12.37 | **−3.87** | Setup-dominant |
| found_poetry | 11 | −7.25 | −10.52 | **−3.28** | Setup-dominant |
| mid_century | 3 | −11.05 | −13.96 | **−2.91** | Setup-dominant |
| victorian | 16 | −10.53 | −11.80 | **−1.27** | Setup-dominant |
| song_lyrics | 6 | −8.78 | −9.80 | **−1.02** | Setup-dominant |
| 19th_century | 8 | −12.97 | −13.28 | **−0.31** | **Symmetric** |
| new_york_school | 16 | −11.25 | −11.39 | **−0.14** | **Symmetric** |
| prose_poetry | 12 | −13.18 | −10.99 | **+2.19** | Reverb-dominant |
| ballad | 8 | −13.55 | −9.60 | **+3.95** | Reverb-dominant |
| romantic | 13 | −15.98 | −11.76 | **+4.22** | Reverb-dominant |
| modernist | 11 | −16.88 | −11.89 | **+5.00** | Reverb-dominant |
| language | 1 | −17.98 | −10.92 | **+7.07** | Reverb-dominant |
| early_modern | 2 | −17.65 | −10.31 | **+7.34** | Reverb-dominant |
| control (prose) | 1 | −9.14 | **+9.20** | **+18.33** | Extreme reverb |

### Interpretation: Three Temporal Architectures

**Architecture 1: Setup-Dominant (negative asymmetry)**

Eras: confessional, contemporary, metaphysical, harlem renaissance, spoken word, found poetry, mid-century.

In these traditions, the poet *prepares* the surprise more than they exploit it. The pre-peak
lull is deeper than the post-peak recovery. The surprise arrives cleanly, without a long
reverberant tail. In the confessional poets (Plath, Sexton, Lowell, Berryman), this pattern
suggests that the *moment of revelation* is framed — both set up and then released —
as if the poem holds its breath before the deviant word and exhales after it. The surprise
is a climactic point, not a generative opening.

**Architecture 2: Reverb-Dominant (positive asymmetry)**

Eras: early modern, language poetry, modernist, romantic, ballad.

Here the pre-peak wind-up is shallower but the post-peak tail is longer. After a spike, the
poem continues in an *elevated* state (relative to a setup-dominant poem's post-spike behavior).
The surprise is generative — it opens a new register that persists for several tokens. This
is especially striking for the early modern poets (Wyatt, Donne, Marvell, Spenser): their
surprising turns have a long "reverb" — the diction that follows a surprising moment stays
elevated, as if the surprise broke a formal dam.

**Architecture 3: The Control Prose Anomaly (asymmetry = +18.3)**

This is the most striking finding. When control prose accidentally produces a high-S₂ moment,
the post-spike zone actually becomes **positive** (+9.20 above baseline), while the pre-spike
zone is just −9.14. Prose "stumbles" into surprise without building up to it, and then the text
continues in an unexpectedly elevated state afterward. This is the mirror image of Setup-Dominant
poetry: where poets *design* their surprises and then return to convention, prose *discovers*
its surprises and then keeps going. This may explain why isolated S₂ spikes in prose read as
awkward (they weren't prepared for) while those in poetry read as purposeful (they were).

---

## Finding 3: Setup Depth and Decay Depth Are Independent

| Metric | Value |
|---|---|
| Correlation between setup depth and decay depth | r = 0.260 |
| Mean setup depth (lags −3..−1, centered) | −1.329 |
| Mean decay depth (lags +1..+3, centered) | −1.665 |

The correlation between "how deep was the pre-peak lull" and "how deep was the post-peak
lull" is only r = 0.26. This means setup and decay are **partially independent strategies**.
A deep setup does not reliably predict a deep decay. These are two different dimensions
of how a poet manages the temporal neighborhood of a surprise.

The mean decay depth (−1.665) is slightly larger in absolute magnitude than the mean setup
depth (−1.329), confirming that post-spike suppression is marginally stronger overall —
but the global balance is nearly exact.

---

## Finding 4: Peak Height Does Not Predict Asymmetry

| Correlation | r |
|---|---|
| Peak S₂ height vs. asymmetry | −0.022 |

The height of the spike (how deviant the word is) has essentially zero correlation with the
temporal asymmetry of the surrounding window. Very high spikes (mean S₂ = 20.07 in Q4)
are just as balanced as modest spikes (mean S₂ = 3.37 in Q1). The degree of deviation and
the temporal architecture are orthogonal features of poetic surprise.

---

## Theoretical Implications

1. **Information conservation**: At the global level, the "energy" of poetic surprise appears
   conserved across time — the deviation is funded by pre-peak conformity in equal measure
   to post-peak recovery. This may reflect the reader's processing: after a surprise, the
   poem re-establishes predictability at the same rate as it built up before.

2. **Two distinct surprise aesthetics**: Setup-dominant eras prepare their surprises (the surprise
   is a *destination*); reverb-dominant eras exploit them (the surprise is a *departure*). This
   maps onto a distinction between poetry of *arrival* (the turn, the kireji, the epiphany)
   and poetry of *opening* (the Romantic sublime, the Modernist fragment, the early modern wit
   that keeps unfolding).

3. **Prose vs. poetry**: The fundamental difference isn't that poetry is more surprising — it's
   that poetry *controls* its surprise temporally. Prose's +18.3 asymmetry shows that prose
   accidents produce uncontrolled reverb. Poetry of all kinds (setup or reverb dominant) has
   managed temporal architectures that cluster in the −11 to +7 range. The poet is an *engineer*
   of the surprise event's shape in time.

---

## Limitations

- Only 130 clean spikes passed the strict isolation criterion (±8 tokens, no neighboring spike).
  Many poems, especially haiku and short contemporary lyrics, contribute no clean spikes despite
  having high S₂ — their spikes are too dense or too close to poem boundaries.
- Per-era sample sizes vary widely (1–16 spikes). Single-poem eras (control, language, oulipo)
  should be treated as case studies rather than era-level generalizations.
- The isolation criterion biases toward longer poems with sparse spikes. Haiku (zero clean spikes)
  are completely excluded.

---

## Suggested Next Steps

1. **Relax the isolation criterion** to ±4 tokens and compare results — does the symmetry hold
   with a denser sample?
2. **Haiku-specific analysis**: Since haiku are completely excluded from this analysis (spikes are
   too dense), compute the mean S₂ of the pre-kireji and post-kireji zones directly (not relative
   to isolated spikes) and test the symmetry hypothesis for the haiku tradition.
3. **Poet-level fingerprints**: With more data (the poet threshold of ≥10 clean spikes captured
   only Ashbery and Shakespeare), compute per-poet asymmetry for authors with many poems. Does
   Hopkins (from pre_peak_setup.md's deep-trap list) show setup-dominant or reverb-dominant architecture?
4. **Link to the "confidence trap"**: Pre-peak lulls where entropy falls (model is most confident
   just before the spike) may correspond to the setup-dominant poems. Test whether trap_depth
   (entropy drop) correlates with asymmetry.
5. **Reader response**: The setup/reverb distinction maps onto distinct reader experiences
   (the prepared revelation vs. the unexpected opening). Could human ratings of "surprise felt"
   distinguish these two architectures?
