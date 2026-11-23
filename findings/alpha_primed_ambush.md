# The α-Primed Ambush: When Concentration Precedes Violation

**Date:** 2026-11-22  
**Experiment:** `experiments/alpha_primed_ambush.py`  
**Results:** `results/alpha_primed_ambush.json`  
**Corpus:** 436 texts, 56,118 artifact-filtered token positions (p_newline < 0.9)  
**Builds on:** `findings/zipf_prediction_coefficient.md`, `findings/alpha_arc_within_poem.md`, `findings/perfect_ambush_analysis.md`

---

## Research Question

The Zipf coefficient experiment established that some eras operate in high-α (concentrated prediction) regimes and others in low-α (diffuse/fog) regimes. The α arc experiment showed that α rises as a poem progresses. But neither asked: **when does a specifically concentrated prediction immediately precede a surprising token?**

This is the **α-primed ambush**: a Straussian deviance that defeats not just some prediction, but a *concentrated, specific* one — when GPT-2 narrows its probability mass to a single strong prediction and the poet writes something else entirely.

**New metric:** For each token position *i*:

> α-ambush score[i] = max(0, α[i-1]) × max(0, S₂[i])

This is the product of:
- The Zipf concentration of GPT-2's prediction *before* the token (how concentrated was the expectation?)
- The surprisal-minus-entropy of the actual token (how much did the poet violate it?)

Both factors must be positive to contribute: low-concentration or conformist tokens score zero.

---

## Finding 1: Ambush vs. Fog — The 70/30 Split

The first question is what fraction of high-S₂ tokens (S₂ > 2.0) are specifically α-primed (preceded by α > 1.5 — a hyper-Zipf, concentrated distribution).

| Mode | Count | % of high-S₂ tokens |
|------|-------|----------------------|
| **α-fog** (preceded by α ≤ 1.5) | 8,025 | **69.5%** |
| **α-primed ambush** (preceded by α > 1.5) | 3,529 | **30.5%** |

**The dominant mode of poetic surprise is fog, not ambush.**

Nearly 70% of all high-S₂ tokens occur when GPT-2's preceding prediction distribution was *diffuse* — spread across many alternatives with no strong concentration. Only 30% are "perfect ambushes" that defeat a specifically concentrated expectation.

This has a major theoretical implication: the intuitive mental model of poetic surprise as "beating a specific strong prediction" describes only a minority of Straussian moments. The majority happen when GPT-2 is already uncertain, and the poet still escapes *even that* diffuse probability field. The two modes are structurally different:

- **α-fog escape**: The poem has entered a semantic field where the model couldn't confidently predict anything. The poet's choice doesn't defeat a specific expectation — it departs from an entire neighborhood of roughly equally probable options. The surprise is horizontal (escaping the neighborhood) rather than vertical (overturning a confident prediction).
- **α-primed ambush**: The poem has established a specific, concentrated expectation (syntactic or formulaic pressure, rhyme anticipation, common phrase completion). The poet's choice directly violates that specific prediction. The surprise is vertical — a head-on conflict with the model's top guess.

---

## Finding 2: Eras Specializing in Ambush vs. Fog

| Era | n | mean α-ambush | mean S₂ | mean α | pct primed |
|-----|---|---------------|---------|--------|------------|
| **clerihew** | 222 | **2.448** | +0.47 | 1.213 | 7.2% |
| **beat** | 1,187 | **2.166** | +0.05 | 2.191 | 6.1% |
| **deep_image** | 60 | **2.129** | +0.10 | 1.224 | 8.3% |
| **concrete** | 306 | **2.067** | −0.57 | 2.025 | 11.8% |
| **haiku** | 279 | **1.987** | −0.07 | 1.241 | 6.8% |
| **confessional** | 391 | **1.962** | −0.20 | 1.248 | 9.2% |
| oulipo | 1,269 | 1.950 | −0.18 | 1.388 | 7.8% |
| latin_american | 457 | 1.889 | −0.45 | 1.362 | 10.5% |
| german_expressionist | 494 | 1.879 | −0.17 | 1.288 | 6.5% |
| modernist | 3,081 | 1.865 | −0.41 | 1.403 | 6.8% |
| postcolonial | 983 | 1.850 | −0.47 | 1.551 | 6.7% |
| ancient | 315 | 1.790 | −0.18 | 1.279 | 7.3% |
| spoken_word | 283 | 1.766 | −0.59 | 1.399 | 4.9% |

**Notable patterns:**

**Beat poetry** leads among major eras (n > 500). The zipf paper already established that beat has the highest mean α (2.191), and this translates directly into high ambush scores — beat's speech-like syntax creates concentrated predictions, and beat poets consistently violate them. The ambush is both frequent and high-stakes.

**Concrete poetry** has high ambush scores (2.067) despite *negative* mean S₂ (−0.57). This confirms what the Zipf paper hinted: concrete poetry creates very concentrated predictions (α = 2.025, nearly identical to beat) but its visual/spatial form means these predictions are *usually* fulfilled — negative mean S₂. When concrete poetry IS surprising (the 11.8% α-primed fraction, highest among the top tiers), the surprises are dramatic because they occur against maximally concentrated contexts.

**Clerihew** leads all eras despite moderate α (1.213). This is surprising: clerihews achieve the highest α-ambush score not through high-α prediction contexts but through *efficiently converting* moderate concentration into high S₂. The structured comic form creates expectation (a biographical statement following a name) that the clerihew systematically violates at the punch line.

---

## Finding 3: Poet-Level Decoupling — Ambush Score ≠ Mean S₂

| Poet | n | mean α-ambush | mean S₂ | pct primed |
|------|---|---------------|---------|------------|
| **Emmett Williams** | 54 | **3.540** | −0.004 | 16.7% |
| **Marianne Moore** | 373 | **3.462** | −0.041 | 12.1% |
| Christian Bök | 213 | **3.084** | +0.804 | 8.5% |
| Jean Lescure | 132 | **2.935** | −0.216 | 9.8% |
| Allen Ginsberg | 146 | **2.874** | +0.670 | 11.0% |
| Bruce Andrews | 43 | **2.823** | +0.638 | 7.0% |
| Kamau Brathwaite | 214 | **2.797** | −0.315 | 6.1% |
| Hart Crane | 168 | **2.712** | +0.983 | 10.1% |
| Charles Bukowski | 92 | **2.558** | −0.352 | 6.5% |
| Francis Thompson | 148 | **2.452** | +0.577 | 8.1% |
| Pablo Neruda | 302 | **2.369** | −0.185 | 13.6% |
| Robert Lowell | 88 | **2.359** | −0.153 | 13.6% |
| Gregory Corso | 228 | **2.325** | +0.274 | 7.0% |

The most striking finding is the **decoupling between α-ambush score and mean S₂** in the top poets.

**Emmett Williams** (concrete/Fluxus poet) leads by ambush score (3.540) but has essentially neutral mean S₂ (−0.004). **Marianne Moore** similarly leads with 3.462 but only −0.041 mean S₂.

This decoupling reveals a **distinctive poetic strategy**: Williams and Moore create extremely concentrated predictions at some positions (high α), violate them dramatically (very high S₂ at those moments), then return to conformity otherwise (pulling mean S₂ toward zero). Their surprise is *concentrated* and *prepared* — the ambush strategy in its purest form.

Compare **Hart Crane** (mean S₂ = +0.983, pct_primed = 10.1%): Crane maintains consistently high S₂ across many tokens (not just α-primed ones), suggesting he operates in a broader fog-escape mode while also occasionally mounting pure ambushes.

**Two poet archetypes emerge:**
1. **The Ambush Specialist** (Williams, Moore): Near-zero mean S₂ but high α-ambush score. The poem mostly conforms to expectation — then strikes precisely when the model is most concentrated.
2. **The Fog Escaper** (Crane, Ginsberg, Bök): Positive mean S₂ AND high ambush score. These poets sustain high surprise across both ambush and fog contexts — consistently off the map regardless of prediction concentration.

---

## Finding 4: Ambush Concentration at Poem Openings — the Front-Loaded Pattern

| Decile | mean α-ambush | n |
|--------|---------------|---|
| D1 (0–10%) | **1.902** | 5,764 |
| D2 (10–20%) | 1.673 | 5,545 |
| D3 (20–30%) | 1.710 | 5,594 |
| D4 (30–40%) | 1.626 | 5,551 |
| D5 (40–50%) | 1.521 | 5,502 |
| D6 (50–60%) | 1.525 | 5,632 |
| D7 (60–70%) | 1.512 | 5,590 |
| D8 (70–80%) | 1.547 | 5,555 |
| D9 (80–90%) | 1.530 | 5,584 |
| D10 (90–100%) | **1.450** | 5,801 |

**α-primed ambushes are front-loaded.** The opening decile (D1) has the highest α-ambush score (1.902), and scores decline fairly monotonically to the lowest at D10 (1.450) — a drop of 0.452 across the poem.

This pattern integrates three prior findings:

1. **α arc** (alpha_arc_within_poem.md): α *rises* across the poem (the model becomes *more* concentrated as it reads). This would predict MORE ambush opportunity late in the poem.

2. **Vocabulary bubble** (vocabulary_bubble.md): The bubble forms progressively — by D10, nearly 45% of GPT-2's top-10 predictions are words already used in the poem. High bubble = more accurate predictions = lower S₂ even when α is high.

3. **Result**: Even though α rises toward D10 (more concentration), the vocabulary bubble ensures those concentrated predictions are *correct* more often. The ambush score falls because the bubble captures the late-poem tokens within its web of entrainment.

**Interpretation:** The beginning of a poem is the most fertile ground for α-primed ambushes. The model opens with generic language predictions (high α from common-phrase-completion patterns), and the poet's initial word choices are least constrained by prior context (no bubble yet). As the poem progresses, the bubble forms and the poet's range narrows — late-poem departures from expectation must fight both the trained vocabulary and the model's own entrainment.

---

## Synthesis: Two Axes of Poetic Surprise

This experiment establishes that poetic S₂ can be decomposed along two orthogonal axes:

| | **Low α (fog context)** | **High α (concentrated context)** |
|---|---|---|
| **Positive S₂** | Fog escape: surprising in an already-uncertain field (69.5%) | **α-primed ambush**: defeating a specific strong prediction (30.5%) |
| **Negative S₂** | Fog conformity: following an uncertain prediction (the model was right anyway) | Bubble conformity: fulfilling a concentrated prediction |

The most common mode is **fog escape** (69.5% of high-S₂ tokens). The rarer but more "violent" mode is **α-primed ambush** (30.5%). Both are legitimate Straussian deviations, but they differ in what they reveal about the "unsaid":

- In fog escape, what the poet suppressed was not a specific word but a *semantic neighborhood* — the reader experiences disorientation, as though the poet swerved from a broad road.
- In α-primed ambush, what the poet suppressed was a *specific word* the model was confidently expecting. The reader experiences a specific click of violated anticipation — the word they were silently predicting does not come.

Different poets specialize in these modes, and different poetic forms afford them. The clerihew's structured setup → punchline format is an extreme case of α-primed ambush; symbolist poetry's diffuse word associations are the extreme case of fog escape.

---

## Suggested Next Steps

1. **α threshold sensitivity**: Test different α cutoffs (1.0, 1.5, 2.0, 2.5) for "α-primed" and check whether the 70/30 fog/ambush ratio is stable or shifts.
2. **Conditional α-ambush by syntactic class**: Are ambushes at NOUN positions after high-α contexts specifically different from ambushes at VERB positions?
3. **Line-boundary α spikes**: The vocabulary bubble paper noted a D10 prediction-concentration rise. Does α spike immediately at line boundaries (before the first token of a new line), giving that opening token a free ambush opportunity?
4. **The ambush specialist vs. fog escaper typology**: Apply this to individual poems to classify them, then ask whether critics' descriptions ("dense," "difficult," "surprising") correlate with the ambush-vs-fog ratio.
5. **α-ambush and affect**: Do α-primed ambushes produce different emotional effects than fog escapes? This would require linking to sentiment or reader response data.
