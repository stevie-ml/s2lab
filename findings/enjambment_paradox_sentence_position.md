# The Enjambment Paradox: Sentence-Position × Line-Position S2 Analysis

**Date:** 2026-09-23  
**Experiment:** `experiments/sentence_position_experiment.py`  
**Corpus:** 166 English poems, 16,294 real (non-whitespace) tokens  
**Builds on:** `line_position_analysis.md`, `enjambment_vs_s2.md`, `enjambment_two_strategies.md`

---

## Research Question

The prior finding (`line_position_analysis.md`) established a powerful gradient: line-initial tokens average **+5.57 S2**, line-final tokens **-0.49 S2** — a 6-bit positional effect.

But line positions confound two distinct phenomena:
1. **Sentence boundaries**: End-stopped lines end at a full stop; the next line begins a new sentence (high entropy for GPT-2 — it truly doesn't know what comes next).
2. **Enjambment**: The sentence continues across the line break; the next line begins mid-sentence (lower entropy — GPT-2 has a confident prior about how the sentence will continue).

**Which drives the spike?** If it's the sentence boundary, end-stopped line-initial tokens should dominate. If it's the line break itself, both categories should spike equally. If enjambment exploits the mismatch between a confident model and an unexpected choice — enjambed line-initial tokens should spike *more*.

---

## Cross-Table: Sentence-Position × Line-Position

| Category | N | Mean S₂ | Std | %+S₂ |
|----------|---|---------|-----|-------|
| line=initial, sent=**medial** (enjambed) | 1,202 | **+7.27** | 10.81 | **64.0%** |
| line=initial, sent=**initial** (end-stopped) | 560 | **+2.74** | 8.24 | **49.8%** |
| line=medial, sent=initial (sentence mid-line) | 127 | +0.30 | 3.69 | 40.2% |
| line=medial, sent=medial (**baseline**) | 12,268 | **-0.27** | 3.73 | 36.2% |
| line=final, sent=medial | 1,211 | -0.48 | 3.48 | 32.2% |
| line=medial, sent=final (sentence ends mid-line) | 138 | -1.72 | 2.17 | 18.1% |
| line=final, sent=final (end-stopped end) | 537 | **-1.66** | 1.77 | **10.4%** |
| line=final, sent=initial (very rare) | 11 | -0.62 | 4.06 | 36.4% |

---

## The Enjambment Paradox

The central finding reverses the obvious intuition:

**Enjambed line-initial tokens (+7.27 S2) are 2.65× more surprising than end-stopped line-initial tokens (+2.74 S2).**

Both categories are at the start of a new line. The only difference is whether a sentence boundary preceded the line break.

### Why enjambment creates more surprise

The mechanism is S2's definition: **S2 = surprisal − entropy**.

| Situation | GPT-2 entropy | Poet's surprisal | S2 |
|-----------|--------------|-----------------|-----|
| **End-stopped line start** | *High* — after a full stop, almost anything could follow | Moderate | Moderate S2 |
| **Enjambed line start** | *Low* — mid-sentence, confident about grammatical continuations | *High* — poet chose unexpected | **High S2** |

When GPT-2 reaches a sentence boundary, it enters a high-entropy state — the next word could be nearly anything, so surprisal can't exceed entropy much. The poet has freedom but the model already "knows" it.

When GPT-2 is mid-sentence, it has a confident prior: given "My heart aches, and a drowsy", it strongly predicts a narrow set of continuations. The enjambing poet who then starts the next line with an unexpected word exploits the gap between the model's certainty and their own choice. **This gap is S2.**

Enjambment doesn't just create a pause — it creates a **context trap**: the reader/model expects the sentence to continue predictably, and the line-opening word violates that expectation.

---

## Sentence-Position Marginals

| Sent Position | N | Mean S₂ |
|--------------|---|---------|
| initial | 698 | +2.25 |
| medial | 14,681 | +0.33 |
| final | 675 | **-1.67** |

Sentence-initial tokens average **+2.25 S2** — well above baseline (-0.27) but far below enjambed line-initial (+7.27). The sentence-level position effect is real but modest compared to the line-level effect.

Sentence-final tokens are the most predictable class in the corpus (-1.67 S2). Poets end sentences with conventional words; GPT-2 predicts them accurately.

---

## Line-Position Marginals (Replication Check)

| Line Position | N | Mean S₂ |
|--------------|---|---------|
| initial | 1,762 | **+5.83** |
| medial | 12,533 | -0.28 |
| final | 1,759 | -0.84 |

This replicates the original line_position_analysis finding (+5.57 initial, -0.49 final) on this larger sample. The cross-table now shows this +5.83 average is a **weighted mix** of enjambed (+7.27) and end-stopped (+2.74) line-initial tokens.

---

## The Surprise Valley: Full Positional Spectrum

Ordering by mean S2 from most to least surprising:

1. **Enjambed line-initial** (+7.27) — poet exploits confident mid-sentence model
2. **End-stopped line-initial** (+2.74) — line break after full stop
3. **Sentence-initial mid-line** (+0.30) — sentence starts mid-line (unusual structure)
4. **Line-medial baseline** (-0.27) — the flow of ordinary discourse
5. **Line-final mid-sentence** (-0.48) — line ending before sentence ends
6. **End-stopped line-final** (-1.66) — most predictable position
7. **Sentence-final mid-line** (-1.72) — most constrained: sentence ending before line break

The endpoints tell the complete story: the moment of maximum poetic freedom is a **mid-sentence line start** (+7.27), and the moment of maximum constraint is a **mid-line sentence end** (-1.72). The gap between them is **9 bits of S2**.

---

## Implications

### For the theory of enjambment

Enjambment has traditionally been theorized in terms of reader expectation and rhythmic disruption. The S2 analysis provides a precise computational correlate: **enjambment maximizes S2 by exploiting the mismatch between the model's confident mid-sentence entropy and the poet's unexpected line-opening choice.** The "expected continuation" is GPT-2's top predictions; the "actual opening" is the poet's word. The S2 gap measures this mismatch.

### For the Straussian gap framework

The highest-S2 moments in poetry are concentrated at enjambment points. This means the "unsaid" (GPT-2's top predictions at these moments) represents **what a prose continuation of the sentence would have been** — the conventional syntactic path not taken. The enjambing poet suppresses the ordinary continuation and begins the new line differently.

### For computational form detection

The enjambed vs. end-stopped distinction can be operationalized via S2: poems with high average S2 at line-initial tokens that are also sentence-medial are poems that rely heavily on enjambment for their surprise structure.

---

## Suggested Next Steps

1. **Per-poem enjambment rate vs. average S2**: Do poems with higher enjambment rates have higher overall S2 signatures?
2. **Enjambment quality**: Not all enjambments are equal — an enjambment that carries a key noun to the next line may have higher S2 than one that enjambs a function word.
3. **Historical shift**: Has enjambment-driven S2 increased over literary history as poets moved from end-stopped Romantic verse to enjambed Modernist free verse?
4. **The "sentence-final mid-line" trap**: The -1.72 S2 of mid-line sentence endings suggests poets who use this device are "spending down" their surprise budget — is this used deliberately for anticlimax or emotional resolution?
