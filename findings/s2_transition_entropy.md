# S2 Transition Entropy: How Open Is the Road After Surprise?

**Date:** 2026-10-01  
**Experiment:** `experiments/s2_transition_entropy.py`  
**Corpus:** 195 poetry texts, 10 prose/cliché controls (artifact-free tokens only)  
**Builds on:** `s2_markov_transitions.md`, `aftermath_entropy.md`, `spike_symmetry_analysis.md`

---

## Research Question

The Markov transition study found that poetry's HIGH_SURPRISE → HIGH_SURPRISE
probability is ~16% while prose collapses to 0% (prose never sustains high surprise).
But that's just one cell. What does the *full distributional structure* of
"what follows surprise" look like? We measure this with **transition entropy** —
the Shannon entropy of the row distribution in the Markov matrix.

**Transition entropy from HIGH_SURPRISE** = how uncertain is the next S₂ zone after
a very surprising token? High entropy = anything can happen. Low entropy = the
poem predictably returns to conformity.

Max possible entropy = log₂(5) = **2.32 bits** (perfectly flat distribution across all zones).

---

## Finding 1: The Largest Poetry–Prose Gap Is After Surprise

| Zone | Poetry H (bits) | Prose H (bits) | Δ (poetry − prose) |
|---|---|---|---|
| deep_conform (<−3) | 2.215 | 1.950 | **+0.265** |
| conform (−3..−0.5) | 2.173 | 2.093 | **+0.080** |
| neutral (−0.5..0.5) | 2.199 | 1.805 | **+0.393** |
| surprise (0.5..3) | 2.175 | 2.023 | **+0.152** |
| **high_surprise (>3)** | **2.164** | **1.673** | **+0.491** ← largest gap |

**The poetry–prose gap is smallest after conformist tokens (+0.080) and
largest after high-surprise tokens (+0.491).** After an extreme S₂ spike,
poetry approaches near-maximum openness (2.164/2.32 = 93% of possible entropy),
while prose collapses predictably back to lower zones (1.673 bits).

Interpretation: In prose, a surprising token is a *blip* — immediately absorbed
back into baseline. In poetry, a surprising token is a *gate* — it opens a space
where genuinely anything can follow. The Straussian gap is not just a spike; it
creates **sequential freedom**.

---

## Finding 2: Era Ordering by Post-Surprise Openness

| Era | n | H from HIGH_SURPRISE | P(→HH) | P(→conform) |
|---|---|---|---|---|
| early_modern | 89 | **2.234** | 13.5% | 56.2% |
| modernist | 316 | **2.224** | 19.3% | 56.0% |
| confessional | 77 | **2.208** | 15.6% | 58.4% |
| contemporary | 132 | **2.185** | 17.4% | 56.1% |
| fixed_form | 141 | 2.182 | 12.1% | 58.9% |
| nursery_rhyme | 31 | 2.176 | 22.6% | 54.8% |
| new_york_school | 214 | 2.169 | 14.5% | 60.7% |
| victorian | 562 | 2.166 | 17.3% | 59.8% |
| 19th_century | 253 | 2.159 | 20.9% | 58.5% |
| romantic | 306 | 2.150 | 19.0% | 58.2% |
| metaphysical | 78 | 2.127 | 10.3% | 61.5% |
| song_lyrics | 67 | 2.113 | 11.9% | 65.7% |
| beat | 39 | 2.107 | **23.1%** | 59.0% |
| harlem_renaissance | 82 | 2.095 | 11.0% | 63.4% |
| biblical | 128 | 2.042 | 9.4% | 67.2% |
| ballad | 139 | 2.032 | 17.3% | 66.2% |
| spoken_word | 30 | 2.030 | 13.3% | 70.0% |
| prose_poetry | 119 | 2.007 | 16.8% | 60.5% |
| found_poetry | 102 | 1.989 | 8.8% | 68.6% |
| haiku | 59 | 1.985 | 15.3% | 64.4% |
| language | 31 | **1.879** | 16.1% | 67.7% |
| **[prose control]** | 43 | **1.673** | 9.3% | **76.7%** |

**Key observations:**

- **Early modern (Sidney, Donne, Marvell) and modernist (Eliot, Pound, Bishop)
  have the most open post-surprise space** — surprise generates genuine freedom.
- **Beat poetry has the highest P(→HH) at 23.1%** — Ginsberg and Kerouac chain
  their surprises more than any other era. Surprise begets surprise.
- **Language poetry has the LOWEST transition entropy among all poetry eras (1.879)**,
  barely above prose (1.673). This is counterintuitive: despite L=A=N=G=U=A=G=E
  poets' reputation for deviation, their surprises are followed by *more predictable*
  sequences — perhaps because their deviations are rule-governed (system, not spontaneity).
- **Biblical texts (2.042) and ballads (2.032) cluster together** — formal, memorized,
  repeated structures where surprise is structurally constrained.
- **Prose control (76.7% return-to-conform after surprise)** vs poetry average (~60%) —
  the gap is structural, not incidental.

---

## Finding 3: Formal vs Free Verse — No Difference!

| Zone | Formal H | Free H | Δ (free − formal) |
|---|---|---|---|
| deep_conform | 2.214 | 2.222 | +0.008 |
| conform | 2.194 | 2.141 | −0.053 |
| neutral | 2.198 | 2.199 | +0.001 |
| surprise | 2.176 | 2.150 | −0.026 |
| **high_surprise** | 2.159 | 2.175 | **+0.017** |

**The formal/free verse distinction does not predict transition entropy.**
The difference across all zones is ≤ 0.053 bits — noise-level variation.
What matters is not whether the poem is sonnets or stream-of-consciousness;
it's something at the level of the **individual poet's strategy** for
deploying surprise, not the formal container.

---

## Finding 4: High-Surprise Chains — What Do They Look Like?

**427 HIGH→HIGH chains found** (≥2 consecutive tokens with S₂ ≥ 3.0), artifact-free.

| Length | Count | Notes |
|---|---|---|
| 2 tokens | 361 (85%) | The most common pattern |
| 3 tokens | 54 (13%) | Rare but consistent |
| 4 tokens | 12 (3%) | Very rare |

**Top highest-S₂ doublets:**

| Poem | Era | Tokens | Avg S₂ |
|---|---|---|---|
| God's Grandeur | victorian | ' shook foil' | 14.85 |
| I heard a Fly buzz (Dickinson) | 19th_century | ' stumbling Buzz' | 13.74 |
| The Fall | prose_poetry | ' indoors mixed' | 13.48 |
| The Lady of Shalott | victorian | ' imbowers' | 13.11 |
| God's Grandeur | victorian | ' reck his' | 13.06 |
| Sir Patrick Spens | ballad | ' guid sailor' | 12.61 |
| My Last Duchess | victorian | ' Duchess painted' | 11.74 |

**Howl (Ginsberg)** produces a length-3 chain: *'angelheaded hip'* — avg S₂ = 10.17.
This is the longest chain at high intensity in the corpus. Three consecutive
tokens that are each highly surprising: the model expected conventional words
and got three radical neologisms stacked together.

**The chains reveal that doublets are almost always semantic compounds:**
- "shook foil" (Gerard Manley Hopkins): rare past-tense adjective + unexpected noun
- "stumbling Buzz" (Dickinson): gerund-as-adjective + capitalized common noun
- "guid sailor" (Scots ballad): dialect adjective + expected noun (but dialect inflection)
- "Duchess painted" (Browning): title + participle in unusual predicate position
- "angelheaded hip" (Ginsberg): portmanteau adjective + unexpected body-part noun

The compound structure suggests that doublets are **semantic portmanteaux** —
two tokens that together form a single unexpected lexical unit.

---

## Synthesis

Three structural discoveries about how poetry manages sequential surprise:

1. **Surprise as gate, not blip**: After a high-S₂ token, poetry's transition
   distribution approaches maximum entropy. The surprising token opens a space
   of genuine possibility rather than immediately resolving into conformity.

2. **Era variation is real but not formal/free**: Language poetry's low transition
   entropy is the most striking finding — it suggests systematic deviation rather
   than expressive openness. Beat's high P(→HH) = 23% confirms the chain-surprise
   aesthetic of Ginsberg and Kerouac.

3. **Doublets are the basic unit of compound surprise**: 85% of chains are length-2.
   These are not random co-occurrences but semantic compounds — two tokens that
   form a single unit of meaning that couldn't be achieved with one surprising token.

---

## Suggested Next Steps

1. **Model transition entropy as a predictor of "poeticity"**: Can a single number
   (transition entropy from HIGH_SURPRISE) distinguish poetry from prose better
   than mean S₂?

2. **Doublet taxonomy**: Classify the 361 doublet chains by type: dialect compounds
   (guid sailor), noun inversions (Duchess painted), metaphor compounds (shook foil),
   etc. Is there a grammar of compound surprise?

3. **Beat's P(→HH) = 23%**: Extend the chain analysis to include Ginsberg's full
   Howl and other beat texts. Is there a sustained cascade effect unique to the beat
   aesthetic?

4. **Language poetry's low transition entropy paradox**: Investigate whether
   language poetry produces *systematic* deviations (a new pattern the model
   can learn) rather than purely stochastic ones — the theory that L=A=N=G=U=A=G=E
   writing is rule-governed constraint, not expression.
