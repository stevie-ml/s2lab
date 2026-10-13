# The Anatomical Turn: Body-Part Lexicon and S₂ in Poetry

**Date:** 2026-10-13  
**Experiment:** `experiments/body_part_lexicon_s2.py`  
**Corpus:** 277 texts; 225 English-language poems analyzed  
**Token occurrences:** 384 body-part tokens across 139 poems  

---

## Research Question

When a poem names a body part, is it using it conventionally (low S₂ — the model expected it) or as a vehicle for genuine surprise (high S₂ — the poet chose what the model did not anticipate)?

The **anatomical cliché hypothesis**: the most culturally saturated body parts in poetry (*heart*, *soul*, *hand*, *eyes*) should have the lowest S₂ — GPT-2 has learned to expect them so thoroughly that choosing them is informationally redundant. Conversely, less-expected body parts (*bones*, *chest*, *foot*) that poets use at structurally charged positions should score higher.

---

## Findings

### 1. Body Parts Ranked by Mean S₂ (artifact-free, n ≥ 3)

| Word | n | Mean S₂ | Median S₂ | Pos% | Top suppressed |
|---|---|---|---|---|---|
| **bones** | 6 | **+3.85** | +1.75 | 50% | 'body', 'lives' |
| foot | 6 | +1.88 | +2.27 | 83% | 'man', 'hand' |
| eye | 11 | +1.39 | +0.02 | 55% | 'eye', 'the' |
| chest | 5 | +1.32 | +1.03 | 80% | 'pond', '-' |
| feet | 4 | +1.29 | +2.80 | 75% | 'a', 'art' |
| arm | 3 | +1.22 | +1.13 | 100% | 'lip', 'ship' |
| flesh | 6 | +0.95 | +1.69 | 67% | 'and', 'the' |
| mouth | 6 | +0.52 | −0.83 | 50% | 'face', 'waist' |
| hips | 10 | +0.33 | −0.96 | 30% | 'hips', ',' |
| back | 15 | +0.30 | +0.19 | 53% | ',', 'to' |
| brow | 4 | −0.10 | −0.28 | 50% | 'ro', 'father' |
| neck | 3 | −0.36 | −0.98 | 33% | 'name', 'face' |
| body | 13 | −0.40 | −0.84 | 38% | 'head', 'own' |
| lips | 5 | −0.43 | −2.09 | 40% | 'hair', 'is' |
| belly | 17 | −0.45 | −0.67 | 12% | 'belly', 'sands' |
| ears | 4 | −0.59 | −0.95 | 25% | 'heart', '.' |
| bone | 5 | −0.59 | −0.19 | 40% | '.', '-' |
| ear | 5 | −0.79 | −2.04 | 40% | 'blood', 'ath' |
| skin | 4 | −0.90 | −0.71 | 50% | 'friend', 'lips' |
| arms | 9 | −0.99 | −1.07 | 33% | 'arms', 'eyes' |
| hair | 10 | −1.35 | −1.08 | 10% | 'hair', 'husband' |
| blood | 12 | −1.46 | −1.75 | 25% | 'the', 'life' |
| head | 18 | −1.49 | −3.40 | 28% | 'head', 'left' |
| eyes | 31 | −1.68 | −2.72 | 23% | 'eyes', '-' |
| voice | 11 | −2.18 | −2.66 | 18% | 'time', 'child' |
| hand | 38 | **−2.20** | −2.26 | 18% | 'hand', 'face' |
| face | 14 | −2.36 | −2.11 | 14% | 'face', 'left' |
| heart | 28 | **−2.47** | −3.94 | 18% | 'heart', 'o' |
| hands | 11 | −2.76 | −2.77 | 0% | 'hands', 'hand' |
| **soul** | 19 | **−3.32** | −3.97 | 11% | 'soul', 'heart' |

**Key finding:** `soul` (−3.32) is the single most *predictable* body part in the corpus — even more predictable than `heart` (−2.47). GPT-2 has absorbed so much conventional poetic usage ("soul" after "my", "soul" at line endings, "heart and soul") that the word has become informationally nearly free.

`bones` (+3.85) is the most *surprising* core body part. When poets write "bones," GPT-2 expects something else (typically "body" or "lives"). The plural anatomical form — hard, skeletal, stripped — resists the model's genre expectations.

---

### 2. The Self-Prediction Phenomenon

The most culturally saturated body parts **predict themselves** at body-part positions:

| Suppressed alternative | Times it was top prediction |
|---|---|
| 'heart' | 22 |
| 'hand' | 19 |
| 'eyes' | 16 |
| 'belly' | 14 |
| 'face' | 11 |
| 'head' | 11 |
| 'soul' | 7 |
| 'blood' | 6 |
| 'hips' | 6 |
| 'hands' | 5 |

When a position calls for a body part, GPT-2 defaults to the canonical poetic body parts: **heart** and **hand** above all. A poet who writes "throat" at such a position scores high S₂ not because "throat" is inherently rare, but because GPT-2 was confident the word would be "heart."

This is the **anatomical canon**: the model has internalized a hierarchy of poetically legitimate body parts, and any departure from this canon is a Straussian choice.

---

### 3. Heart by Literary Era — The Decline of the Cliché

| Era | n | Mean S₂ |
|---|---|---|
| spoken_word | 2 | **+0.69** |
| 19th_century | 8 | −1.30 |
| cliche_control | 3 | −3.57 |
| romantic | 5 | −4.48 |
| **victorian** | 3 | **−4.72** |

Victorian poets use "heart" at the most predictable level of any era in the corpus (−4.72). GPT-2 has learned the Victorian poetic register so thoroughly that "heart" is nearly the model's top prediction. Romantic poets (−4.48) are nearly as bad. Spoken-word poets (+0.69) have recovered "heart" as a surprise word by using it in unexpected syntactic positions or against unusual contexts.

The cliché is not intrinsic to the word but to its deployment in a register — spoken-word poets "defamiliarize" heart by using it differently.

---

### 4. Era Comparison: Body-Part S₂

| Era | n | Mean S₂ |
|---|---|---|
| **confessional** | 8 | **+3.03** |
| latin_american | 9 | +2.55 |
| german_expressionist | 18 | +1.58 |
| beat | 6 | +1.30 |
| oulipo | 9 | +0.15 |
| old_english | 10 | −0.07 |
| spoken_word | 14 | −0.21 |
| postcolonial | 9 | −0.29 |
| mid_century | 5 | −0.35 |
| modernist | 30 | −0.44 |
| 18th_century | 10 | −0.61 |
| **victorian** | 49 | −1.04 |
| prose_poetry | 14 | −1.07 |
| 19th_century | 25 | −1.19 |
| romantic | 26 | −1.37 |
| war_poetry | 14 | −1.46 |
| early_modern | 11 | −1.48 |
| contemporary | 17 | −1.71 |
| parody | 12 | −1.82 |
| harlem_renaissance | 9 | −1.96 |
| new_york_school | 11 | −2.03 |
| ancient | 7 | −2.22 |
| **classical_chinese** | 6 | −2.38 |
| **cliche_control** | 7 | **−2.84** |

**Confessional poetry** (+3.03) has the most surprising body-part usage. Sexton and Plath deploy body parts in frank, medical, non-metaphorical ways that violate the poetic canon — "throat" for strangling, "chest" for surgery, "bone" as literal anatomical material. The body is not metaphor but evidence.

**Latin American surrealism** (+2.55, led by Vallejo) and **German expressionism** (+1.58, Heym, Benn) use body parts as uncanny assemblages, disconnected from their conventional roles.

**Classical Chinese** (−2.38) and **cliché control** (−2.84) represent the poles of anatomical predictability. The ancient Chinese poetic convention of body reference (hands, eyes, face in fixed formulaic positions) and the deliberate cliché corpus both suppress surprise equally.

---

### 5. Most Surprising Body-Part Usages

| S₂ | Word | Poem | Poet | Era | Suppressed |
|---|---|---|---|---|---|
| +14.92 | **throat** | The Truth the Dead Know | Anne Sexton | confessional | 'and' |
| +12.58 | **bones** | Black Stone Lying on a White Stone | César Vallejo | latin_american | 'on' |
| +11.14 | **palm** | Recessional (stanzas 1-3) | Rudyard Kipling | victorian | 'the' |
| +10.79 | **bones** | Black Stone Lying on a White Stone | César Vallejo | latin_american | 'saturdays' |
| +8.20 | **thigh** | Mann und Frau gehn durch die Krebsbaracke | Gottfried Benn | german_expressionist | 'is' |
| +8.18 | **hip** | Howl (opening) | Allen Ginsberg | beat | ',' |
| +7.89 | **eye** | Constantly Risking Absurdity | Lawrence Ferlinghetti | beat | 'the' |
| +7.39 | **eye** | An Essay on Man (Epistle I) | Alexander Pope | 18th_century | 'and' |
| +7.19 | **eyes** | O Captain! My Captain! | Walt Whitman | 19th_century | 'the' |
| +7.17 | **mind** | The Wanderer (excerpt) | Anonymous (OE) | old_english | 'the' |
| +6.92 | **lips** | What lips my lips have kissed | Edna St. Vincent Millay | mid_century | 'is' |

**Sexton's "throat"** (+14.92) is the most extreme case in the corpus. The model overwhelmingly expected "and" — a grammatical continuation — but Sexton inserted "throat" at a position of maximum model confidence, forcing the reader into abrupt physical confrontation.

**Vallejo's "bones"** appears twice at +12.58 and +10.79 in the same poem. This is the *anatomical refrain* phenomenon: when an unusual body part defines a poem's key motif, it remains high-S₂ across multiple occurrences because the model never fully habituates.

---

### 6. Metaphor-Prone vs. Literal Body Parts

| Category | n | Mean S₂ |
|---|---|---|
| Metaphor-prone (heart/soul/blood/bone/flesh/mind/voice) | 156 | **−1.32** |
| Literal/physical (elbow/knee/ankle/chest/neck/back) | 228 | **−0.53** |

**Counter-intuitive finding:** The body parts conventionally used as metaphors are *more predictable* than the literal, physical body parts. Soul, blood, and heart — deployed as conventional symbols — have been absorbed into the model's poetic expectations. Literal, non-metaphorical body parts (ankle, elbow, chest, back) are less expected at those positions because they carry less symbolic load.

This inverts the naïve assumption that metaphorical usage = surprising usage. The cliché *is* the metaphor. Surprise, in poetry, often comes from the literal.

---

## Synthesis: The Anatomy of Poetic Convention

This experiment reveals a **hierarchy of anatomical cliché** in the English poetic tradition, as learned by GPT-2:

1. **Highest cliché:** soul, hands, heart, face, eyes — the "canonical" poetic body (the lyric self, the beloved's face, the emotional core)
2. **Middle ground:** blood, head, voice, hair — widely used but in more varied syntactic positions
3. **Most novel:** bones, chest, foot, arm, flesh — body parts that resist the canonical poetic role

The Straussian gap in anatomical poetry is the space between the body the lyric tradition expects and the body the poem actually presents. When Sexton writes "throat," she refuses the canonical lyric body (the heart, the face, the hand) and substitutes the raw anatomical one.

---

## Suggested Next Steps

1. **Track the canonical body across centuries**: Map the shift in which body part is most predictable from Medieval → Renaissance → Romantic → Modernist periods.
2. **The body in prose vs. poetry**: Does the prose corpus use the same body parts differently (lower S₂ vs. higher)?
3. **Gendered bodies**: Do male and female poets use body parts with different S₂ profiles? Is "breast" more or less surprising in poems by women?
4. **Body-part compounds**: What happens to S₂ at "heartbeat", "bloodstream", "fingertip"? Do compound body parts resist cliché better than simplex ones?
5. **Measure anatomical density**: Do poems with more body-part tokens have higher or lower overall S₂? Is there a tradeoff between physical concreteness and informational richness?
