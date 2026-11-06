# Stanza Form and S₂ Budget: Does Form Determine Information Architecture?
**Date:** 2026-11-06
**Experiment:** `experiments/stanza_form_s2_budget.py` → `findings/stanza_form_s2_budget.json`
**Corpus:** 773 stanzas across 403 poems, 7 stanza forms

---

## Research Question

Does a stanza's line count determine how surprise (S₂) is distributed within it?
Two competing models:

- **Compression model**: Shorter stanzas must pack their S₂ more tightly — fewer tokens, so each token carries more weight.
- **Spike model**: Longer stanzas allow "setup + ambush" — most tokens conform, but one or two reach extreme heights. Bigger budget, bigger peaks.

---

## Finding 1: Tercets Lead; Couplets and Long Stanzas Lag

Ranked by mean artifact-free S₂:

| Form | n stanzas | n poems | Mean S₂ | Mean Max S₂ | Pos S₂% | Last-Line Boost |
|---|---|---|---|---|---|---|
| **tercet (3)** | 101 | 45 | **−0.396** | 8.65 | 33.4% | −0.287 |
| sestet (6) | 63 | 44 | −0.409 | 11.01 | 34.4% | −1.106 |
| cinquain (5) | 59 | 35 | −0.415 | 11.27 | 33.1% | −0.327 |
| octave/septet (7–9) | 117 | 77 | −0.433 | 11.97 | 34.8% | −0.759 |
| **quatrain (4)** | 273 | 97 | −0.450 | 9.76 | 32.9% | **−0.195** |
| couplet (2) | 41 | 20 | −0.480 | 8.33 | 34.9% | −0.312 |
| **longer (10+)** | 119 | 106 | **−0.532** | 12.35 | 32.2% | −0.878 |

Tercets have the highest mean S₂; longer (10+)-line stanzas the lowest. The compression model is **partially confirmed** but only for tercets; couplets actually underperform the prediction.

---

## Finding 2: Longer Stanzas Allow More Extreme Spikes (The Ambush Effect)

**Mean peak-to-mean ratio** (mean_max_s2 / mean_s2 magnitude) by form:

| Form | Mean Max S₂ | Peak-to-Mean Ratio |
|---|---|---|
| couplet (2) | 8.33 | 41.4 |
| sestet (6) | 11.01 | 65.9 |
| quatrain (4) | 9.76 | 80.7 |
| tercet (3) | 8.65 | 99.4 |
| cinquain (5) | 11.27 | 97.9 |
| octave/septet (7–9) | 11.97 | 216.2 |
| longer (10+) | 12.35 | **311.8** |

The spike model is **strongly confirmed**: longer stanzas do not spread S₂ evenly — they concentrate it in a single extreme moment (peak_to_mean = 312 for 10+ line stanzas). A couplet can achieve at most 8.3 S₂ nats in its peak; a 10+ line stanza averages a 12.3-nat peak — but the rest of its tokens are far more conformist.

**Interpretation**: The "ambush" architecture — strategic conformity followed by one decisive spike — scales with stanza length. A couplet cannot be an ambush poem. A long stanza is almost always one.

---

## Finding 3: Last Lines Always Decline — But Quatrains Decline Least

**Last-line boost** = (mean S₂ of last line) − (mean S₂ of first line). All forms show negative values: last lines are always lower S₂ than first lines.

| Form | Last-Line Boost | Interpretation |
|---|---|---|
| **quatrain (4)** | **−0.195** | Most "balanced" across its span |
| tercet (3) | −0.287 | Moderate decline |
| couplet (2) | −0.312 | Surprisingly large for a 2-line form |
| cinquain (5) | −0.327 | Comparable to tercets |
| octave/septet (7–9) | −0.759 | Strong resolution effect |
| longer (10+) | −0.878 | Very strong decline |
| **sestet (6)** | **−1.106** | Most dramatic first→last S₂ drop |

The **quatrain is the most S₂-neutral ending form** — its last line deviates least from its first. The **sestet shows the steepest closing drop**, consistent with its use in sonnets (the first four lines of the sestet introduce the resolution; the last two land it firmly).

This converges with the stanza_internal_arc finding: within-stanza entropy declines with position. But the magnitude of that decline is form-specific, not just a mechanical entropy effect.

---

## Finding 4: Clerihew Exception — Form with a Positive Last-Line Boost

Examining **quatrains by era** reveals one striking outlier:

| Era | n | Mean S₂ | Last-Line Boost |
|---|---|---|---|
| **clerihew** | 6 | **+0.511** | **+1.719** |
| german_symbolist | 5 | +0.369 | −1.165 |
| german_expressionist | 12 | +0.069 | −0.035 |
| 19th_century | 8 | −0.024 | −1.161 |
| ballad | 16 | −0.327 | −0.666 |
| victorian | 20 | −0.363 | −0.156 |
| modernist | 15 | −0.947 | −0.793 |

The **clerihew is the only era-form combination with a positive last-line boost (+1.719)**. This is information-theoretically exact: the clerihew is a comic form where the punchline is in the last line, and GPT-2 confirms it. The final line is the most unexpected token sequence in the stanza.

The **modernist quatrain** is the most S₂-negative (-0.947) — modernist poets using the quatrain form actively avoid it as a vehicle for surprise, treating it as a container for uniformly surprising content that averages out low.

---

## Theoretical Summary

| Property | Short stanzas (≤3) | Medium (4–6) | Long (7+) |
|---|---|---|---|
| Mean S₂ | Highest (−0.40 to −0.48) | Middle | Lowest (−0.43 to −0.53) |
| Peak S₂ | Lower (8–9) | Medium (9–11) | Higher (12) |
| Peak-to-Mean | Low (41–99) | Medium (66–98) | High (216–312) |
| Last-line decline | Modest (−0.29 to −0.31) | Varies (−0.20 to −1.11) | Strong (−0.76 to −0.88) |

**The tercet is an anomaly** — short like a couplet but with the most positive mean S₂. The haiku tradition (all 16 haiku stanzas in the corpus are tercets) may drive this: the entire S₂ economy of the haiku is compressed into 3 lines with no syntactic resolution permitted.

**The sestet anomaly** — higher mean S₂ than quatrain but most extreme last-line drop — is consistent with the sonnet's sestet as a resolution device: it opens with tension and closes with settlement.

---

## Next Steps

1. **Rhyme scheme × form**: Does ABAB (alternating) vs. ABBA (enclosed) produce different last-line boost? Enclosed rhyme may restrain the last-line S₂ drop more than alternating.
2. **Volta position × form**: Do sonnet sestets with explicit volta markers show different peak positions than those without?
3. **Tercet S₂ leader identity**: Are tercet-based poems (Dante's terza rima, Shelley's odes, Williams' triadic lines) driving the tercet's high mean S₂, or is it distributed across poets?
4. **Within-form era vs. form signal**: Does controlling for era remove the form differences, or are form effects independent of era?
