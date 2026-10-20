# Surprise Asymmetry: The Post-Spike Valley Is Deeper Than the Pre-Spike Setup

**Date:** 2026-10-20  
**Experiment:** `experiments/surprise_asymmetry.py`  
**Corpus:** 315 texts, 5,835 spikes (S₂ ≥ 3.0, artifact-free tokens only)  
**Extends:** `findings/pre_peak_setup.md` and `findings/surprise_decay_curves.md`

---

## Motivation

Two prior findings seemed to be in tension:
- `pre_peak_setup.md` found that poets *descend into* spikes over 8 tokens (S₂ drops ~0.6 units from lag −3 to lag −1).
- `surprise_decay_curves.md` found that S₂ collapses to near-zero at lag +1 ("universal half-life = 1").

This experiment overlays both curves to ask: **is the temporal structure around a surprise symmetric?** Does the poem "unwind" after a spike the same way it "wound up" before?

The answer is **no** — and the direction of asymmetry is surprising.

---

## Global Curves

| Lag | Direction | Mean S₂ | Mean H | N |
|:---:|:---:|:---:|:---:|:---:|
| −8 | pre | −0.449 | 6.261 | 3,409 |
| −7 | pre | −0.422 | 6.321 | 3,646 |
| −6 | pre | −0.295 | 6.415 | 3,919 |
| −5 | pre | −0.278 | 6.419 | 4,202 |
| −4 | pre | −0.255 | 6.439 | 4,507 |
| −3 | pre | −0.246 | 6.396 | 4,812 |
| −2 | pre | −0.303 | 6.506 | 5,157 |
| −1 | pre | −0.332 | 6.469 | 5,484 |
| **0** | **SPIKE** | **[≥3.0]** | | |
| +1 | post | −0.397 | **5.824** | 5,718 |
| +2 | post | −0.409 | 6.361 | 5,418 |
| +3 | post | −0.380 | 6.388 | 5,076 |
| +4 | post | −0.424 | 6.331 | 4,747 |
| +5 | post | −0.451 | 6.216 | 4,430 |
| +6 | post | −0.395 | 6.233 | 4,119 |
| +7 | post | −0.491 | 6.247 | 3,840 |
| +8 | post | −0.571 | 6.290 | 3,596 |

**AUC (sum lags 1–8):**
- Pre-peak: −2.58
- Post-peak: −3.52
- **Asymmetry ratio (post/pre AUC): 1.36**

---

## Finding 1: The Post-Spike Valley Is Deeper Than the Pre-Spike Setup

Prior work's "pre-peak cliff" described S₂ falling from the baseline as the spike approached. But the total area of suppression *after* the spike is 36% larger than before it. The poet does not simply "return to baseline" after a surprise — the poem becomes **measurably more conformist** than it was before the spike.

The pre-spike window (lags −8 to −1) has mean S₂ ≈ −0.32 (close to the corpus baseline of −0.34). The post-spike window (lags +1 to +8) has mean S₂ ≈ −0.44 — deeper below baseline.

This is the **post-spike conformity tax**: after paying the cost of an unexpected word, the poem compensates by becoming *more* predictable than its usual level.

---

## Finding 2: The Entropy Anomaly at Lag +1

The entropy curve shows a striking discontinuity:

- At lag −1 (just before spike): mean H = **6.469** — GPT-2 is relatively confident, having descended from lag −4's 6.439
- At lag **+1** (just after spike): mean H = **5.824** — GPT-2 is **significantly MORE confident** than at any point before the spike

This is counterintuitive. One might expect that after a poet's unexpected choice, the model would be *more* uncertain about what follows (the context has been disrupted). Instead, the spike **constrains** the subsequent context: an unusual word opens a narrower set of natural continuations, and GPT-2 responds with increased confidence.

Interpretation: high-S₂ tokens often function as "semantic anchors" — once the poet uses an unexpected word, the discourse frame narrows. "Wristwatch" in a pastoral poem is unexpected, but once it appears, the subsequent tokens are over-determined.

---

## Finding 3: Two Distinct Asymmetry Regimes by Era

**Asymmetry ratio < 1 (collapse faster than setup — "ramp-up crash"):**

| Era | Ratio | Pattern |
|---|---|---|
| ballad | −23.27 | Extreme ramp-up: pre-window POSITIVE AUC (+0.17), post-window highly negative (−4.02) |
| oulipo | −3.90 | Constraint-form ramp-up |
| concrete | −1.83 | Visual/spatial surprise then crash |
| ghazal | −0.87 | Refrain form ramp-up |

**Asymmetry ratio > 2.0 (post-spike much deeper — "extended valley"):**

| Era | Ratio | Pattern |
|---|---|---|
| haiku | 2.72 | Deep post-spike valley (−7.13) despite modest setup |
| confessional | 2.45 | Sustained post-spike conformity |
| contemporary | 2.18 | Long recovery window |
| postcolonial | 2.17 | Extended conformity zone |
| modernist | 2.06 | Broad post-spike suppression |

### The Ballad Paradox

Ballads (ratio = −23.27) are the extreme outlier. Their PRE-spike window has **positive AUC** (+0.17) — meaning the tokens leading up to a spike are slightly *above* the poem's average. This is because ballad meter creates a rhythmic "buildup" where adjacent tokens are more contextually predictable *from each other*, but the spike comes at a formulaic moment (e.g., "blood" at the end of a violent rhyme). After the spike, the formula immediately reasserts, crashing the post-window to −4.02.

The ballad pattern is: **rhythmic preparation → surprise → formula clamps down hard**.

### Haiku's Deep Valley

Haiku has a ratio of 2.72 (moderate setup, deep post-valley). The spike typically falls at the kireji (cutting word) or line break. After that moment, the final fragment of the haiku is short and semantically forced by the kireji — GPT-2 is very constrained, producing the deep post-spike valley of −7.13.

---

## Finding 4: Poet-Level Asymmetry as a Stylistic Signature

The most distinctive poets by asymmetry ratio:

**Extreme ramp-up / crash (ratio < 0):**

| Poet | Ratio | Setup (pre-AUC) | Post-AUC |
|---|---|---|---|
| Countee Cullen | −34.56 | +0.06 | −2.20 |
| Traditional (Scottish ballad) | −23.67 | +0.16 | −3.85 |
| Gerard Manley Hopkins | −1.14 | +0.85 | −0.97 |
| Gertrude Stein | −0.73 | +0.94 | −0.68 |

**Countee Cullen** shows the most extreme asymmetry in the corpus: his pre-spike context carries slight positive S₂ (building), then the spike crashes into a strongly conformist valley. This aligns with his formal use of the sonnet (Petrarchan structure = rhythmic buildup → voltaic moment → octave resolution).

**Hopkins** (−1.14): The "sprung rhythm" pattern from `pre_peak_setup.md` appears here. Hopkins builds metrically predictable lines up to the "sprung" stress, which arrives as a spike and is immediately followed by conventional resolution.

**Long recovery (ratio > 5):**

| Poet | Ratio | Pre-AUC | Post-AUC |
|---|---|---|---|
| Emily Dickinson | 28.72 | −0.04 | −1.23 |
| Wislawa Szymborska | 8.29 | −0.23 | −1.90 |
| Robert Burns | 7.26 | −0.78 | −5.69 |
| Marianne Moore | 6.34 | −0.37 | −2.37 |
| Matthew Arnold | 9.80 | −0.39 | −3.77 |

**Emily Dickinson** has the most extreme long-recovery ratio (28.72): her pre-spike window barely differs from her baseline, but after a spike, her poem drops into a **deep conformist valley**. This is the "isolated spike" pattern from `surprise_decay_curves.md` seen from a new angle: Dickinson's surprises are hermetically sealed — the context neither anticipates nor echoes them. Her dashes function as syntactic resets that make the post-spike context highly constrained for GPT-2 (the dash signals a specific grammatical resolution to follow).

**Allen Ginsberg** (ratio 1.57): The pre-spike AUC is a **positive** +3.62, meaning his pre-spike tokens are *above* baseline S₂ — already in a higher-surprise zone when the spike arrives. The post-spike zone is also positive (+5.67). This is the "sustained elevation" pattern: Ginsberg doesn't fall back to baseline after a spike. His cascading anaphora keeps S₂ elevated throughout, and spikes emerge from an already-elevated field.

---

## The Two Poetic Architectures

| Architecture | Asymmetry | Examples | Mechanism |
|---|---|---|---|
| **Ramp-up crash** (ratio < 0) | Pre-spike elevated, post-spike suppressed | Ballads, Hopkins, Cullen | Formal constraint reasserts after spike |
| **Symmetric** (ratio ~1.0) | Both windows near baseline | T.S. Eliot (1.03), Ashbery (1.02), Poe (1.01) | Steady-state language with isolated spikes |
| **Extended valley** (ratio > 2) | Modest setup, deep/long post-valley | Dickinson, confessional, haiku, Burns | Spike anchors narrow context; valley = forced resolution |
| **Sustained elevation** (ratio ~1.5, positive AUC both sides) | Both windows above baseline | Ginsberg, Claudia Rankine (1.40) | Accumulative surprise; no baseline recovery |

---

## Conclusion

The temporal envelope around a poetic surprise is **not symmetric**. In the global average, the post-spike conformity zone is 36% deeper than the pre-spike setup zone. This is the **post-spike conformity tax**: an unexpected word creates a narrower subsequent context, driving GPT-2 to higher confidence (lower entropy) and the poet to more predictable choices.

The asymmetry ratio is a new poet-level metric that complements the Aftershock Index from `surprise_decay_curves.md`:
- **Ramp-up crash** (ratio < 0): formal poets where constraint precedes and follows the spike
- **Extended valley** (ratio > 2): lyric poets where the spike constrains resolution
- **Symmetric** (ratio ≈ 1): poets with stable, baseline-hugging spike environments

The most striking exception is Allen Ginsberg: his spikes emerge from and recede into *above-baseline* S₂ fields, confirming the cascade-accumulation architecture described in `surprise_decay_curves.md`.

---

## Suggested Next Steps

1. **Stanza-aware windowing**: re-run stopping at stanza breaks, not just at artifact tokens (p_newline > 0.9). The current window stops at newlines but not at intentional stanza breaks.
2. **Sentence boundary analysis**: do spikes at sentence-final vs. sentence-medial positions show different asymmetry patterns?
3. **Spike height vs. asymmetry**: does the magnitude of the spike predict the depth of the post-valley? (higher spikes → deeper valley?)
4. **Line position confound**: are post-spike lags disproportionately line-initial (which tend to have lower S₂)? Control for line-position.
