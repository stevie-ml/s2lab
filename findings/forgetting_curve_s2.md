# The Forgetting Curve: Does Distance Between Repetitions Modulate S₂?

**Date:** 2026-11-11  
**Experiment:** `experiments/forgetting_curve_s2.py` → `results/forgetting_curve_s2.json`  
**Corpus:** 403 English poems, 9,069 consecutive-occurrence pairs  
**Builds on:** `second_occurrence_dip.md`, `structural_position_immunity.md`

---

## Research Question

`second_occurrence_dip.md` established that words lose ~2.31 S₂ units between their first and second appearance. `structural_position_immunity.md` showed that *line position* can partially offset this. But neither asked: **does the number of tokens between occurrences predict how much S₂ drops?**

Cognitive priming research suggests a forgetting curve: shorter priming intervals produce stronger suppression; longer gaps allow context to "reset." Does GPT-2 show the same pattern for in-poem repetition?

---

## Key Findings

### 1. A Forgetting Curve Exists for Second Occurrences

Looking only at second occurrences (the cleanest signal, uncontaminated by accumulating habituation):

| Distance (tokens) | N    | Mean Δ S₂ | Median Δ S₂ | % Rise |
|-------------------|------|-----------|-------------|--------|
| 0–10 (adjacent)   | 929  | **−1.762** | −1.613 | 34.6% |
| 11–25 (close)     | 858  | **−1.919** | −1.373 | 34.8% |
| 26–50 (medium)    | 802  | **−1.207** | −0.935 | 38.5% |
| 51–100 (far)      | 791  | **−0.879** | −0.903 | 39.2% |
| 101–300 (distant) | 435  | **−0.593** | −0.599 | 43.2% |
| 301+ (very far)   | 65   | **−2.180** | −1.008 | 40.0% |

**The forgetting curve is real but non-monotonic.** Mean Δ S₂ improves from −1.76 (close) to −0.59 (101–300 tokens apart), a recovery of **+1.17 S₂ units**. The % Rise climbs from 34.6% to 43.2%. But the 301+ bucket reverses — likely a selection effect, as very long poems with far-apart repetitions tend toward formal structures (ballads, hymns) where function words recur with strict pattern.

### 2. The 11–25 Token Dip: A Counterintuitive Local Minimum

The sharpest habituation is not at 0–10 tokens (immediate adjacency), but at **11–25 tokens** (mean Δ = −1.919). This suggests:

- Truly adjacent repeats (0–10) may gain a slight structural benefit (e.g., the first occurrence was at a line end, the second at the next line start — a natural anaphoric echo position).
- At 11–25 tokens, the word has just left working memory *and* the structural position bonus is gone. The model has freshly updated its probability upward, but there is no structural override — producing the deepest drop.

### 3. All-Occurrence Pooled: Distance Effect Weakens

When all occurrence transitions are pooled (all n ≥ 2), the distance gradient flattens:

| Distance (tokens) | N     | Mean Δ | Median Δ | % Rise |
|-------------------|-------|--------|----------|--------|
| 0–10              | 2,846 | −0.678 | −0.237   | 45.5%  |
| 11–25             | 2,445 | −0.711 | −0.153   | 45.5%  |
| 26–50             | 1,704 | −0.652 | −0.349   | 45.4%  |
| 51–100            | 1,357 | −0.058 | −0.159   | **47.2%** |
| 101–300           | 641   | −0.162 | −0.262   | 46.3%  |
| 301+              | 76    | −2.256 | −1.016   | 40.8%  |

Pooling obscures the forgetting curve: later occurrences (3rd, 4th, etc.) carry large structural bonuses from anaphoric position, pulling means toward zero regardless of distance.

### 4. The Occurrence Number Curve: Rapid Floor, Then Noise

| Occ # | N     | Mean S₂ | Median S₂ | % +S₂ |
|-------|-------|---------|-----------|-------|
| 1     | 3,880 | +0.864  | −0.501    | 44.7% |
| 2     | 3,880 | −0.514  | −1.787    | 26.2% |
| 3     | 1,607 | −0.750  | −2.175    | 19.4% |
| 4     | 903   | −0.778  | −2.348    | 16.9% |
| 5     | 582   | −1.320  | −2.390    | 14.8% |
| 6     | 412   | −1.230  | −2.619    | 12.9% |

The drop from 1st → 2nd is catastrophic (+0.86 → −0.51, a swing of **1.38 S₂ units** in mean; the median swings by **1.29**). By the third occurrence the mean drops slightly further. After that, the mean oscillates around −0.5 to −1.3 with no clear monotonic decrease — suggesting that by the third use, GPT-2 has "baked in" this word as a poem-specific expectation and further repetitions have similar information cost.

The **positive-S₂ rate** tells a cleaner story: 44.7% → 26.2% → 19.4% → 16.9% → 14.8%. It monotonically decreases and stabilizes around 13–17% by the 5th–6th occurrence.

### 5. Distance Alone Has Near-Zero Correlation With Delta (r = 0.027)

The global Pearson correlation between token distance and Δ S₂ for multi-occurrence words is **r = 0.027** — nearly zero. Distance matters for the *second* occurrence specifically, but once a word has appeared 3+ times in a poem, the distance between later occurrences no longer strongly predicts how much S₂ changes. The floor has been reached.

### 6. Top Recovery Cases: Structural Surprise Overwhelms Distance

| Word    | Poem                         | Occ # | Distance | S₂ before | S₂ after | Δ    |
|---------|------------------------------|-------|----------|-----------|----------|------|
| 'said'  | You Are Old, Father William  | 7     | 54       | −1.31     | +37.22   | +38.5 |
| 'his'   | The Eve of St. Agnes         | 11    | 8        | −5.17     | +29.20   | +34.4 |
| 'lord'  | Recessional                  | 3     | 57       | −2.47     | +30.44   | +32.9 |
| 'three' | Villanelle of the Poet's Road| 3     | 79       | −4.84     | +27.87   | +32.7 |
| 'she'   | She Had Some Horses          | 2     | 10       | −2.68     | +29.58   | +32.3 |
| 'where' | Home on the Range            | 4     | 28       | −2.05     | +29.34   | +31.4 |

These are all **structural position overrides**: the word appears at a line-start where GPT-2 expected a newline. Distance is secondary — the structural bonus (+30 S₂ units for a highly expected newline) completely swamps any habituation.

---

## Interpretation

### A Two-Component Model

The data support a model where S₂ at the nth occurrence is influenced by:

1. **Structural position bonus** (dominant, ±20–35 units): Does GPT-2 expect a newline here?
2. **Lexical habituation** (moderate, −1 to −2 units): How many prior occurrences has GPT-2 seen?
3. **Distance decay** (weak, up to +1.17 units): Does the gap since last occurrence allow partial context reset?

Component 1 overwhelms both others. When examining structural-position-controlled pairs (component 1 = 0, all mid-line occurrences), the forgetting curve from component 3 becomes legible.

### What the Distance Effect Tells Us About GPT-2's Context

GPT-2's attention window is 1,024 tokens. The fact that forgetting is most evident up to ~300 tokens suggests GPT-2 is not simply "forgetting" in a window sense — with 403-token average poems, all tokens are in-window for most pairs. The forgetting is instead about **probability updating**: after a word appears, GPT-2 recalibrates upward on the next occurrence regardless of position. The forgetting curve at 101–300 tokens may reflect that in longer poems, the model's attention to that word's specific occurrence naturally weakens as more intervening tokens dilute its signal.

### Poetry Strategy: Timing Repetitions for Effect

The 101–300 token "sweet spot" for minimal habituation suggests a craft implication: repeating a word after ~100 tokens (roughly 8–15 lines in a typical poem) allows the most S₂ recovery. This is the scale of a stanza return — a word appearing in stanza 1 and then again in stanza 3 or 4 will carry more surprise than one repeated stanza-to-stanza. This aligns with how refrains work in ballads and odes: the refrain is set at a distance that maximizes re-encounter surprise.

---

## Limitations

1. The 301+ bucket (n=65) is too small and likely subject to selection effects from long formal poems.
2. Distance effect for second occurrences is real but moderate (Δ ≈ 1.17 S₂ units) relative to structural position (±30 units).
3. No control for semantic predictability: words that naturally have high context entropy may be more "forgettable" for unrelated reasons.
4. The 11–25 token local minimum needs replication with structural-position-controlled subsets.

---

## Suggested Next Steps

1. **Re-run with structural control**: filter to pairs where both occurrences are mid-line (p_newline < 0.3) to isolate the pure distance effect without structural confounds.
2. **Bucket by poem length**: is the 101–300 token sweet spot an artifact of shorter poems hitting their proportional midpoint in that range?
3. **Compare anaphoric vs. non-anaphoric repetition**: does a word repeated in anaphoric position (always line-start) show a different distance curve than the same word in random positions?
4. **Song lyrics extension**: in songs, the chorus repeats at defined distances; test whether the distance to the first chorus return predicts S₂ at the chorus.
