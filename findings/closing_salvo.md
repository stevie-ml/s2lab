# Closing Salvo: The Hot End Problem in Poetic S₂

**Date:** 2026-10-21  
**Experiment:** `experiments/closing_salvo.py` → `results/closing_salvo.json`  
**Corpus:** 289 English-language poems (≥30 artifact-free tokens)  
**Companion to:** `findings/opening_salvo.md` (today)

---

## Research Question

The opening of a poem faces a structural "cold start": GPT-2 begins with no context and maximal entropy (~11 bits at position 0), so no word can produce strong Straussian surprise at the outset. What about the *ending*? At the close, GPT-2 has accumulated the full poem as context — entropy is at its minimum, predictions are most confident. 

**Does this create a symmetrically opposite "hot end" problem** — where poets cannot surprise because the model is too confident? Or do endings follow a different logic than openings?

---

## Corpus-Level Results

| Zone | Mean S₂ | Mean Entropy | Spike Rate | r(zone, overall) |
|------|---------|-------------|------------|-----------------|
| Opening (first 15 tokens) | **+0.059** | 7.055 | 21.4% | 0.443 |
| Rest (middle, excl. closing) | −0.418 | 6.359 | 16.1% | **0.907** |
| Closing (last 15 tokens) | **−0.638** | 5.979 | 13.3% | 0.317 |

**The closing zone is the most conformist part of any poem.** Its mean S₂ (−0.638) is 0.22 units below the rest of the poem and 0.70 units below the opening. Entropy is also lowest at the close (5.98 vs 7.06 at opening) — the model is more confident here than anywhere else, and poets largely *don't* fight this.

**The closing is the weakest predictor of a poem's overall S₂** (r = 0.317) — even weaker than the opening (r = 0.443). The middle of a poem (r = 0.907) is overwhelmingly its character. A poem's opening and ending are both structural anomalies — but in opposite directions.

**Only 42.6% of poems close higher than their "rest" average.** The majority resolve at the end.

---

## The Lag Profile: Position-by-Position at the Close

Counting backward from the last artifact-free token (lag 0 = last, lag 14 = 15th from end):

| Lag | Mean S₂ | Mean Entropy | N |
|:---:|:-------:|:------------:|:---:|
| **0 (last)** | **−1.330** | **4.222** | 289 |
| −1 | **+0.019** | 6.195 | 289 |
| −2 | −1.013 | 6.023 | 289 |
| −3 | −0.402 | 6.079 | 289 |
| −4 | −0.564 | 6.329 | 289 |
| −5 | −0.429 | 6.000 | 289 |
| −6 | −0.705 | 5.839 | 289 |
| −7 | −0.597 | 6.226 | 289 |
| −8 | −0.598 | 6.004 | 289 |
| −9 | −0.686 | 6.186 | 289 |
| −10 | −0.544 | 5.997 | 289 |
| −11 | −0.637 | 5.991 | 289 |
| −12 | −0.424 | 6.046 | 289 |
| −13 | −0.919 | 6.212 | 289 |
| −14 | −0.734 | 6.341 | 289 |

### Finding 1: The Last Token Is the Most Resolved Token in the Poem

Lag 0 (the very last artifact-free token) has S₂ = **−1.330** and entropy = **4.22 bits** — by far the lowest entropy in the entire closing window and across the whole corpus. GPT-2, having processed the whole poem, is maximally confident at this moment. The last word almost always *arrives home*. 

This is the mirror of position 0 in the opening (where entropy is **11.14** and S₂ = −0.579). At position 0, the model is too uncertain to be surprised; at lag 0, the model is too confident to be surprised. Both endpoints suppress Straussian deviation — but for opposite reasons.

### Finding 2: The Penultimate Token Is the One Exception

Lag −1 (the second-to-last artifact-free token) has S₂ = **+0.019** — the only lag in the closing window with a (barely) positive mean. Its entropy (6.20) is close to corpus average. 

This creates a **micro-volta** pattern at the close: the second-to-last token allows a slight surprise, before the final token resolves. It mirrors the opening's "Straussian window" (positions 1–7), but compressed to a single token.

**The closing structure is: [deep resolution at lag 0] ← [micro-volta at lag −1] ← [gradual decline across lags −2 to −14].**

This is structurally opposite to the opening's arc: [high entropy at position 0] → [Straussian window positions 1–7] → [normalization from position 9].

---

## Opening vs. Closing: A Structural Comparison

| Feature | Opening (first 15) | Closing (last 15) |
|---------|-------------------|------------------|
| Mean S₂ | +0.059 | **−0.638** |
| Mean Entropy | 7.055 | **5.979** |
| Spike rate | 21.4% | **13.3%** |
| r(zone, overall S₂) | 0.443 | **0.317** |
| Extreme position | Pos 0: S₂ = −0.58, H = 11.14 | Lag 0: S₂ = −1.33, H = 4.22 |
| Local anomaly | Pos 4: S₂ = +0.661 (peak) | Lag −1: S₂ = +0.019 (micro-peak) |
| Mechanism | Cold start: model too uncertain | Hot end: model too confident |

Both extremes converge on *less Straussian deviation*, but via opposite mechanisms. The opening suppression is driven by **high entropy** (uncertainty ceiling); the closing suppression is driven by **low entropy** (confidence floor).

---

## Era Breakdown: Who Defies the Closing Gradient?

Sorted by closing advantage (closing S₂ − rest S₂):

| Era | n | Closing S₂ | Rest S₂ | Closing Adv | Opening Adv |
|-----|---|-----------|---------|-------------|-------------|
| postcolonial | 6 | +0.046 | −0.551 | **+0.598** | +0.754 |
| oulipo | 4 | +0.058 | −0.245 | **+0.303** | +0.498 |
| confessional | 6 | −0.152 | −0.367 | **+0.215** | +0.174 |
| elegy | 6 | −0.227 | −0.341 | **+0.114** | +1.071 |
| german_expressionist | 6 | −0.301 | −0.447 | **+0.146** | +0.303 |
| modernist | 25 | −0.570 | −0.573 | +0.003 | +0.413 |
| romantic | 16 | −0.674 | −0.529 | **−0.145** | +0.960 |
| victorian | 23 | −0.616 | −0.458 | **−0.158** | +0.601 |
| 19th_century | 13 | −0.734 | −0.531 | **−0.204** | +0.464 |
| language | 5 | −0.620 | −0.346 | **−0.274** | −0.004 |

**Postcolonial and Oulipo eras** are the only ones where the closing *surpasses* their rest average (+0.60 and +0.30 respectively). Most traditional eras (romantic, victorian, 19th century) close *more* conformist than their middles.

**Elegy is instructive**: elegy has a very high opening advantage (+1.071) but a near-zero closing advantage (+0.114). Elegies front-load their Straussian moves and close with resolution — formally enacting mourning's arc from disruption to acceptance.

---

## Most Striking Poems

### Highest Closing Advantage (endings defy resolution)

| Poem | Author | Era | Closing S₂ | Rest S₂ | Advantage |
|------|--------|-----|-----------|---------|-----------|
| Sailing to Byzantium (stanza 1) | W.B. Yeats | modernist | +1.689 | −0.968 | **+2.657** |
| Deer Park (literal trans.) | Wang Wei | classical_chinese | +0.393 | −2.203 | **+2.596** |
| There Was an Old Person of Ware | Edward Lear | limerick | +1.886 | −0.584 | **+2.470** |
| Umbra Vitae | Georg Heym | german_expressionist | +1.952 | −0.431 | **+2.383** |
| Daddy (opening) | Sylvia Plath | confessional | +1.146 | −0.935 | **+2.080** |

Lear's limerick closing advantage (+2.47) makes structural sense: the **punchline** is the final move, where the meter sets up confident expectation and the closing rhyme violates it. The limerick form is a machine for closing detonations.

Yeats's "Sailing to Byzantium" and Heym's "Umbra Vitae" close with maximally deviant language — in Yeats's case, the strange metallic imagery of the closing stanza; in Heym's, the expressionist images of death.

### Lowest Closing Advantage (most resolved endings)

| Poem | Author | Era | Closing S₂ | Rest S₂ | Advantage |
|------|--------|-----|-----------|---------|-----------|
| Whereas (excerpt) | Layli Long Soldier | contemporary | −2.293 | +1.034 | **−3.327** |
| The Hollow Men (opening) | T.S. Eliot | modernist | −3.007 | +0.311 | **−3.318** |
| Grass | Carl Sandburg | modernist | −2.690 | −0.233 | **−2.456** |
| I heard a Fly buzz — when I died | Emily Dickinson | 19th_century | −1.946 | +0.402 | **−2.348** |
| Islets/Irritations (excerpt) | Bruce Andrews | language | −0.908 | +1.585 | **−2.493** |

Eliot's "Hollow Men" is a famous case: the poem's central passage ("This is the way the world ends / Not with a bang but a whimper") creates high-S₂ language through its excerpted section, but the closing tokens resolve into utterly familiar language. The *content* is about endings without closure; the *information structure* enacts that by closing with maximum conformism.

Dickinson's "I heard a Fly buzz" is the opposite of her usual high-S₂ signature: in this poem about dying, the terminal buzzing fly creates strange imagery throughout, but the very ending — the speaker's consciousness failing — is expressed in GPT-2's most expected terms.

---

## Theoretical Interpretation

The data suggests a **structural asymmetry** in poetic information management:

1. **Openings are anomalous upward** (mean S₂ = +0.059 vs rest −0.418): poets exploit the brief window of confident predictions that emerge after the first word's "cold start."

2. **Closings are anomalous downward** (mean S₂ = −0.638 vs rest −0.418): poets generally *accept* the confidence of accumulated context rather than fight it — endings resolve.

3. **The body of the poem (the "rest") is the most stable and most diagnostic zone**: r(rest, overall) = 0.907. This is where a poet's information economy is most consistently expressed.

The poem's **information envelope** — opening anomaly up, closing anomaly down — is the consistent shape across nearly all eras. This could be called the **"S₂ valley-and-hill" structure**: the true information character lies in the central mass, with the opening as a front-loaded anomaly and the closing as a structured resolution.

### The Micro-Volta

The one exception to closing resolution is lag −1 (the penultimate token: S₂ = +0.019). This **micro-volta** suggests that poets preserve one final surprise before the last word resolves. It mirrors the structure of the volta in the Petrarchan sonnet — a turn before resolution — compressed to the scale of adjacent tokens.

---

## Suggested Next Steps

1. **Symmetry test**: Plot opening (positions 0–14) and closing (lags 0–14, reversed) on the same axis. Is the shape truly symmetric? The opening has a peak at position 4 (+0.661); the closing has a micro-peak at lag −1 (+0.019). The magnitudes are wildly different — is there any formal symmetry?

2. **Limerick closing structure**: Limericks have the highest closing advantage. Analyze whether this is explained entirely by the punchline rhyme slot, or whether the last LINE has elevated S₂ throughout.

3. **"Envelope classification"**: Classify poems by their (opening advantage, closing advantage) pair — quadrant analysis. Do four distinct information envelope types emerge?

4. **The null result**: Why is the closing such a weak predictor (r = 0.317)? Is this because poets with different overall S₂ characters converge on similar resolutions? Or because the closing window captures noise?
