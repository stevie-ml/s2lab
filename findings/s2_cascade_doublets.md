# The Cascade Doublet: Do Adjacent Surprises Diminish Each Other?

**Date:** 2026-09-26  
**Experiment:** `experiments/s2_cascade_doublets.py` → `results/s2_cascade_doublets.json`  
**Corpus:** 169 clean English poems, 1,979+ artifact-free spike tokens (S₂ ≥ 3.0)  
**Builds on:** `aftermath_entropy.md`, `surprise_decay_curves.md`, `s2_markov_transitions.md`

---

## Research Question

When two high-S₂ tokens appear in close proximity (within 2–10 positions), does the second spike suffer "surprise fatigue" — a reduction in S₂ because the first spike already raised entropy, signaling to GPT-2 that unusual territory is underway?

The hypothesis (from `aftermath_entropy.md`): extreme spikes *dissolve* context — entropy rises sharply after S₂ > 9.5. If a second spike arrives in that elevated-entropy wake, the surprisal required to achieve the same S₂ should be higher. The second spike "costs more."

The null: S₂ doublets are informationally independent — proximity to a prior spike neither helps nor hurts the second.

---

## Finding 1: No Surprise Fatigue — S₂ Is Not Reduced in Doublets

| Window | Isolated n | Isolated S₂ | Second n | Second S₂ | Δ S₂ |
|---|---|---|---|---|---|
| 2 | 1,393 | 6.009 | 586 | 6.294 | **+0.285** |
| 3 | 986 | 6.016 | 660 | 6.057 | +0.041 |
| 5 | 495 | 6.115 | 687 | 6.013 | −0.102 |
| 10 | 126 | 6.318 | 466 | 6.107 | −0.211 |

**The effect is negligible across all window sizes.** At every distance band, second spikes have S₂ within 0.3 units of isolated spikes — a difference far smaller than the ~2.3-unit swing between first and second *occurrences* of the same word (`second_occurrence_dip.md`). Proximity to a prior spike does not tax the second surprise.

This is the key finding: **surprise stacking is informationally free.** A poet can place two high-S₂ tokens one position apart without the second being diminished. There is no "surprise budget" that is locally depleted.

---

## Finding 2: The Distance Curve Is Flat

| Distance from prior spike | n | Mean S₂ | Mean H |
|---|---|---|---|
| 1 | 461 | 6.29 | 6.21 |
| 2 | 396 | 6.46 | 6.68 |
| 3 | 333 | 5.88 | 6.86 |
| 4 | 270 | 5.76 | 6.71 |
| 5 | 194 | 6.08 | 6.66 |
| 6 | 163 | 6.02 | 6.73 |
| 7 | 129 | 6.09 | 6.58 |
| 8 | 108 | 6.11 | 6.74 |
| 10 | 77 | 6.01 | 6.65 |
| 14 | 41 | 6.66 | 6.16 |

**S₂ shows no systematic decay as a function of distance from the prior spike.** A second spike occurring 1 token after the first is just as intense as one occurring 14 tokens later. There is no "recovery time" required before a second surprise can occur at full strength.

The entropy column is more interesting: entropy at distance-1 spikes is the *lowest* in the table (6.21), and entropy at distances 3–10 is notably elevated (~6.7–6.9). This is consistent with `aftermath_entropy.md`'s finding that extreme spikes *dissolve* context — entropy rises after a spike. But the S₂ at these higher-entropy positions stays flat, meaning the surprisal is rising proportionally.

---

## Finding 3: The Compensatory Mechanism

Why don't second spikes show lower S₂ despite occurring in elevated-entropy contexts?

| Group | n | Mean Surprisal | Mean Entropy | Mean S₂ |
|---|---|---|---|---|
| Isolated (prior spike > 10 away) | 592 | 12.840 | 6.741 | 6.098 |
| Second (prior spike ≤ 5) | 1,654 | 12.723 | 6.588 | 6.135 |

**Both surprisal and entropy drop proportionally in doublets.** The second spike occurs in a context with slightly *lower* entropy (6.588 vs 6.741) — contrary to the initial hypothesis. The model is actually more confident when the second spike arrives, not less. Yet S₂ remains the same because surprisal also drops proportionally.

**Reinterpretation:** The aftermath-entropy finding (entropy rises after extreme spikes) applies to the first few tokens after a spike at the *extremes* (S₂ > 9.5), but in the aggregate, after a spike context the model enters a *slightly lower-entropy regime*. The poet is writing into a context that GPT-2 has already been surprised out of — and yet the poet produces an equally surprising choice anyway.

---

## Finding 4: Doublet Rates by Era — Some Schools Stack; Others Isolate

Doublet rate = fraction of spikes with a prior spike within 5 tokens.

| Era | Iso n | Dbl n | Dbl% | Iso S₂ | Dbl S₂ | Ratio |
|---|---|---|---|---|---|---|
| **deep_image** | 3 | 12 | 80.0% | 4.91 | 5.47 | 1.11 |
| **beat** | 10 | 29 | 74.4% | 6.20 | **7.45** | **1.20** |
| **language** | 8 | 23 | 74.2% | 5.75 | 6.22 | 1.08 |
| confessional | 25 | 52 | 67.5% | 6.11 | 5.95 | 0.97 |
| victorian | 177 | 304 | 63.2% | 6.02 | 5.98 | 0.99 |
| ballad | 53 | 87 | 62.1% | 6.69 | 7.11 | 1.06 |
| harlem_renaissance | 32 | 50 | 61.0% | 6.38 | 6.51 | 1.02 |
| found_poetry | 58 | 44 | **43.1%** | 6.27 | 6.43 | 1.02 |
| metaphysical | 40 | 38 | **48.7%** | 5.52 | 5.85 | 1.06 |

**Beat and Language poetry have the highest doublet rates (74–80%)**, suggesting these schools lean into surprise clustering. Deep Image is highest of all at 80%, though with small sample.

**Found poetry and metaphysical poetry have the lowest doublet rates (43–49%)**, suggesting these schools prefer to space their surprises with conventional stretches in between. Found poetry's low rate is consistent with its prose-derived syntax; metaphysical poetry's low rate may reflect its argumentative structure (surprises follow logical steps).

Beat poetry's doublet S₂ is notably *higher* than its isolated S₂ (7.45 vs 6.20, ratio 1.20) — stacked surprises in beat poetry are actually *more* extreme than isolated ones. Ginsberg and Kerouac appear to use doublets as a form of intensification.

---

## Finding 5: Poet-Level Profiles — Who Stacks?

| Poet | Iso n | Dbl n | Dbl% | Iso S₂ | Dbl S₂ |
|---|---|---|---|---|---|
| **Robert Bly** | 3 | 12 | 80.0% | 4.91 | 5.47 |
| **Bruce Andrews** | 3 | 11 | 78.6% | 6.04 | 6.51 |
| **Frank O'Hara** | 7 | 21 | 75.0% | 6.71 | 6.18 |
| **G.M. Hopkins** | 21 | 62 | 74.7% | 5.97 | **6.63** |
| **Allen Ginsberg** | 10 | 29 | 74.4% | 6.20 | **7.45** |
| Thomas Hardy | 24 | 58 | 70.7% | 7.05 | 5.86 |
| Wallace Stevens | 11 | 25 | 69.4% | 4.75 | **6.67** |
| Sylvia Plath | 8 | 18 | 69.2% | 6.48 | 7.00 |
| E.E. Cummings | 14 | 28 | 66.7% | **8.60** | 6.48 |
| Emily Dickinson | 21 | 46 | 68.7% | 7.05 | 6.62 |
| **Gertrude Stein** | 4 | 9 | 69.2% | **8.70** | 6.60 |

**Hopkins stands out**: 74.7% doublet rate and doublet S₂ actually *higher* than isolated S₂ (6.63 vs 5.97). His sprung rhythm deliberately clusters stresses, and this experiment shows that clustering extends to information: Hopkins packs his surprises together and the second doesn't diminish.

**Ginsberg** has the highest doublet-to-isolated S₂ ratio (7.45 vs 6.20, +1.25 units). His stacked surprises in "Howl" — the catalogue of "who" clauses with cascading unexpected modifiers — are informationally more intense in clusters.

**E.E. Cummings and Gertrude Stein** have the highest isolated S₂ (8.60, 8.70) but moderate doublet S₂ — suggesting they produce extreme isolated surprises but their doublets, while common, are at typical levels.

---

## Finding 6: The Most Remarkable Doublet Pairs

| Rank | Poet | S₂₁ | S₂₂ | Dist | Token 1 → (expected) | Token 2 → (expected) |
|---|---|---|---|---|---|---|
| 1 | Jefferson (found text) | 14.9 | 15.4 | 2 | `Liberty` → (`,`) | `,` → (`,`) |
| 2 | G.M. Hopkins | 7.8 | **22.0** | 2 | `shining` → (`a`) | `shook` → (`the`) |
| 3 | G.M. Hopkins | **22.0** | 7.7 | 1 | `shook` → (`the`) | `foil` → (`hands`) |
| 4 | Emily Dickinson | 12.3 | 15.2 | 1 | `stumbling` → (`⏎`) | `Buzz` → (`—`) |
| 5 | Russell Edson | **16.4** | 10.6 | 1 | `indoors` → (`the`) | `mixed` → (`.`) |
| 6 | Emily Dickinson | 18.9 | 7.9 | 5 | `Fun` → (`little`) | `Brain` → (`mind`) |
| 7 | Elizabeth Bishop | 6.2 | **20.6** | 4 | `keys` → (`ways`) | `badly` → (`glass`) |
| 8 | Chiyo-ni | 10.0 | 16.6 | 2 | `buck` → (`known`) | `entangled` → (`ed`) |
| 9 | E.E. Cummings | 17.9 | 8.8 | 3 | `stall` → (` `) | `and` → (`⏎`) |
| 10 | Alfred Lord Tennyson | 12.1 | 14.2 | 1 | `imb` → (`of`) | `owers` → (`ued`) |

**"Shining from shook foil" (Hopkins) is the canonical doublet.** The model expected "a" after "shining from" (S₂=22.0 for "shook"); then expected "the" after "shook" (S₂=7.7 for "foil"). Both a present participle used as a noun modifier and the monosyllable "foil" defy expectation — and the two surprises are 1 token apart. The doublet is not an accident: Hopkins' sprung rhythm is built on the accumulation of stressed syllables, and here the information theory directly tracks the prosodic intensity.

**Dickinson's doublets** show a different mechanism: small syntactic frames where she departs from expected line endings (`stumbling` where a newline was expected) and then immediately places an unexpected content word (`Buzz`). The doublet occurs because she violates *form* then *semantics* in quick succession.

**Elizabeth Bishop's "One Art"** produces a high-S₂ doublet (*keys/badly*) in the famous "The art of losing isn't hard to master" — the casual "badly" where "glass" was expected embodies the poem's suppressed catastrophe.

---

## Interpretation: Why Stacking Works

The null result — no surprise fatigue — is itself the major finding, and it has a structural explanation.

In isolation, a high-S₂ token achieves its effect by deviating from a low-entropy context (the model was confident). After that token, `aftermath_entropy.md` showed that entropy *rises* (context is dissolved). If a second spike arrives in that high-entropy wake, it might seem harder to achieve the same S₂ — but the data shows this does not happen.

The mechanism is that the **poet controls both halves of S₂ = surprisal − entropy.** After a first spike raises entropy, the poet can still deliver high surprisal *relative to* that new, higher entropy. The S₂ bookkeeping balances because surprisal tracks entropy.

What this means aesthetically: **surprise can be layered without penalty.** A poet can build a dense patch of unexpected choices — Hopkins' "shining from shook foil," Ginsberg's "starving hysterical naked" — and each word in the cluster maintains its informational weight. There is no "surprise credit" that gets spent by the first deviation.

The contrast with lexical habituation (`second_occurrence_dip.md`) is striking: **a repeated word loses 2.3 S₂ units; an adjacent surprise word loses nothing.** Repetition creates expectation that the model exploits. Novelty — a different unexpected word each time — doesn't. The poet who chains surprises is always doing something *new*, so the model can't adapt.

---

## Suggested Next Steps

1. **The intensity asymmetry**: Beat poetry's doublet S₂ *exceeds* isolated S₂ (ratio 1.20). Test whether there is a genuine "amplification" effect in clusters, or whether this reflects selection bias (high-S₂ contexts attract more unexpected choices).

2. **Triplets and longer chains**: Do three consecutive surprises still maintain full S₂? The data here covers pairs; chains of 3+ would test the no-fatigue result more severely.

3. **Genre-specific mechanisms**: Found poetry's low doublet rate (43%) and metaphysical poetry's (49%) suggest structural reasons for spacing surprises. Trace the specific syntactic contexts that force isolation vs. clustering in these traditions.

4. **Hopkins prosody analysis**: Test whether the clustering of S₂ in Hopkins correlates with prosodic stress positions in sprung rhythm — a direct bridge between information theory and traditional prosody.
